from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

import numpy as np

from .core import Timer, base_manifest, repo_root, summarize_series, timestamp, write_csv, write_json
from .studies.diagnostics import (
    proposal_centered_td_diagnostics,
    proposal_gvf_question_design,
    proposal_stability_atlas,
)
from .studies.feature_plasticity import (
    proposal_generate_test,
    proposal_nonstationary_bandit,
    proposal_streaming_representation,
    proposal_tidbd_plasticity,
)
from .studies.planning_offpolicy import (
    proposal_baird_offpolicy_stability,
    proposal_continual_dyna_model_aging,
    proposal_continual_dyna_model_aging_drift,
    proposal_dyna_planning_budget,
)
from .studies.prediction_scale import proposal_output_controlled_td, proposal_output_controlled_td_fairness
from .studies.predictive_state import proposal_predictive_state_plasticity, proposal_useful_gvfs_state
from .studies.reward_centering import (
    proposal_reward_centered_sarsa,
    proposal_reward_centered_sarsa_sensitivity,
    proposal_scale_invariant_control,
    proposal_unit_switching_control,
)
from .studies.temporal_abstraction import proposal_options


DEFAULT_STEPS = {
    "smoke": 300,
    "minimal": 2000,
    "main": 8000,
}

RUNNERS: dict[str, Callable[[list[int], str, int], tuple[list[dict], dict]]] = {
    "output_controlled_td": proposal_output_controlled_td,
    "output_controlled_td_fairness_audit": proposal_output_controlled_td_fairness,
    "reward_centered_sarsa": proposal_reward_centered_sarsa,
    "reward_centered_sarsa_sensitivity": proposal_reward_centered_sarsa_sensitivity,
    "scale_invariant_continuing_control": proposal_scale_invariant_control,
    "unit_switching_continuing_control": proposal_unit_switching_control,
    "useful_gvfs_state": proposal_useful_gvfs_state,
    "predictive_state_plasticity": proposal_predictive_state_plasticity,
    "generate_test_features": proposal_generate_test,
    "options_reusable_subtasks": proposal_options,
    "streaming_representation": proposal_streaming_representation,
    "centered_td_diagnostics": proposal_centered_td_diagnostics,
    "nonstationary_bandit": proposal_nonstationary_bandit,
    "onpolicy_stability_atlas": proposal_stability_atlas,
    "gvf_question_design": proposal_gvf_question_design,
    "tidbd_plasticity": proposal_tidbd_plasticity,
    "baird_offpolicy_stability": proposal_baird_offpolicy_stability,
    "dyna_planning_budget": proposal_dyna_planning_budget,
    "continual_dyna_model_aging": proposal_continual_dyna_model_aging,
    "continual_dyna_model_aging_drift": proposal_continual_dyna_model_aging_drift,
}


def output_suite_label(suite: str, config_path: str | None) -> str:
    if config_path and Path(config_path).name == "config_extended.json":
        return "extended"
    return suite


def result_dir(proposal: str, suite_label: str) -> Path:
    root = repo_root() / "experiments" / "alberta_core_rl" / "results"
    path = root / proposal / f"{timestamp()}_{suite_label}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_proposal(
    proposal: str,
    suite: str = "minimal",
    seeds: list[int] | None = None,
    steps: int | None = None,
    config: dict[str, Any] | None = None,
    config_path: str | None = None,
    command: str | None = None,
) -> Path:
    if proposal not in RUNNERS:
        raise ValueError(f"unknown proposal {proposal}. Valid: {sorted(RUNNERS)}")
    seeds = [0, 1, 2] if seeds is None else seeds
    steps = DEFAULT_STEPS.get(suite, DEFAULT_STEPS["minimal"]) if steps is None else steps
    suite_label = output_suite_label(suite, config_path)
    out = result_dir(proposal, suite_label)
    config_used = dict(config or {})
    config_used.update(
        {
            "proposal": proposal,
            "suite": suite,
            "output_suite": suite_label,
            "seeds": seeds,
            "steps": steps,
            "config_path": config_path,
            "command": command,
        }
    )
    manifest = base_manifest(proposal, suite_label, seeds, config_used)
    manifest["condition_summary_version"] = "seed_tail_v1"
    with Timer() as timer:
        rows, summary = RUNNERS[proposal](seeds, suite, steps)
    summary["elapsed_sec"] = timer.elapsed
    summary["metrics_summary"] = summarize_numeric_rows(rows)
    condition_summary = summarize_by_condition(rows)
    summary["n_condition_groups"] = len(condition_summary)
    summary["condition_summary_version"] = "seed_tail_v1"
    write_csv(out / "metrics.csv", rows)
    write_json(out / "summary.json", summary)
    write_json(out / "condition_summary.json", condition_summary)
    write_json(out / "config_used.json", config_used)
    write_json(out / "manifest.json", manifest)
    return out


def summarize_numeric_rows(rows: list[dict]) -> dict[str, dict[str, float]]:
    by_key: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        for key, value in row.items():
            if isinstance(value, (int, float, np.integer, np.floating)) and key not in {"seed", "step"}:
                by_key[key].append(float(value))
    return {key: summarize_series(values) for key, values in by_key.items()}


def summarize_by_condition(rows: list[dict]) -> list[dict]:
    condition_keys = [
        "algorithm",
        "environment",
        "scale",
        "representation",
        "alpha",
        "beta",
        "lambda",
        "gamma",
        "reward_shift",
        "maze_length",
        "phase",
        "recovery_window",
        "delay",
        "feature_budget",
        "cumulant",
        "planning_steps",
        "model_mode",
        "half_life",
        "switch_type",
        "drift_mode",
    ]
    present = [key for key in condition_keys if any(key in row for row in rows)]
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = tuple(row.get(k, None) for k in present)
        grouped[key].append(row)
    output = []
    for key, group_rows in sorted(grouped.items(), key=lambda item: str(item[0])):
        max_step = max(float(row.get("step", 0.0)) for row in group_rows)
        tail_start = max_step - max(50.0, 0.2 * max_step)
        condition = {name: value for name, value in zip(present, key)}
        metrics = _condition_metrics(group_rows, present, tail_start)
        seeds = sorted({int(row["seed"]) for row in group_rows if "seed" in row})
        output.append(
            {
                "condition": condition,
                "n_rows": len(group_rows),
                "n_seeds": len(seeds),
                "seeds": seeds,
                "metrics": metrics,
            }
        )
    return output


def _condition_metrics(group_rows: list[dict], condition_keys: list[str], tail_start: float) -> dict:
    numeric_keys: list[str] = []
    for row in group_rows:
        for name, value in row.items():
            if name in {"seed", "step"} or name in condition_keys:
                continue
            if isinstance(value, (int, float, np.integer, np.floating)) and name not in numeric_keys:
                numeric_keys.append(name)
    metrics = {}
    for name in numeric_keys:
        values = [float(row[name]) for row in group_rows if name in row]
        tail_values = [
            float(row[name])
            for row in group_rows
            if name in row and float(row.get("step", 0.0)) >= tail_start
        ]
        metrics[name] = summarize_series(values)
        metrics[f"{name}_tail"] = summarize_series(tail_values)
        seed_tail_means = _seed_tail_means(group_rows, name)
        metrics[f"{name}_seed_tail"] = summarize_seed_estimates(seed_tail_means)
    return metrics


def _seed_tail_means(group_rows: list[dict], metric: str) -> list[float]:
    by_seed: dict[int, list[dict]] = defaultdict(list)
    for row in group_rows:
        if "seed" in row and metric in row:
            by_seed[int(row["seed"])].append(row)
    means = []
    for seed_rows in by_seed.values():
        max_step = max(float(row.get("step", 0.0)) for row in seed_rows)
        tail_start = max_step - max(50.0, 0.2 * max_step)
        values = [
            float(row[metric])
            for row in seed_rows
            if float(row.get("step", 0.0)) >= tail_start and np.isfinite(float(row[metric]))
        ]
        if values:
            means.append(float(np.mean(values)))
    return means


def summarize_seed_estimates(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return {
            "n": 0,
            "mean": float("nan"),
            "std": float("nan"),
            "stderr": float("nan"),
            "ci95": float("nan"),
            "min": float("nan"),
            "max": float("nan"),
        }
    std = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    stderr = float(std / np.sqrt(len(arr))) if len(arr) > 1 else 0.0
    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "std": std,
        "stderr": stderr,
        "ci95": float(1.96 * stderr),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }
