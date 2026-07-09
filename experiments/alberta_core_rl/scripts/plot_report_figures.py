#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.core import ensure_mpl_config, repo_root


def _load_condition_summary(result_dir: Path) -> list[dict[str, Any]]:
    with (result_dir / "condition_summary.json").open("r", encoding="utf-8") as f:
        rows = json.load(f)
    if not isinstance(rows, list):
        raise TypeError(f"expected list condition summary in {result_dir}")
    return rows


def _metric(row: dict[str, Any], metric: str) -> tuple[float, float]:
    stats = row["metrics"].get(f"{metric}_seed_tail") or row["metrics"].get(metric)
    if not stats:
        return math.nan, math.nan
    return float(stats.get("mean", math.nan)), float(stats.get("ci95", math.nan))


def _condition(row: dict[str, Any], key: str) -> Any:
    return row["condition"].get(key)


def _sorted_unique(values: list[Any]) -> list[Any]:
    def key(v: Any) -> tuple[int, Any]:
        try:
            return 0, float(v)
        except Exception:
            return 1, str(v)

    return sorted(set(values), key=key)


def _safe_label(value: Any) -> str:
    text = str(value)
    return text.replace("_", " ")


def plot_scale_invariant(result_dir: Path) -> list[Path]:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    rows = _load_condition_summary(result_dir)
    outputs: list[Path] = []
    metrics = [
        ("avg_unshifted_reward", "Tail unshifted reward", False),
        ("q_norm", "Tail Q norm", True),
        ("prediction_change", "Tail output change", True),
    ]
    algorithms = [
        "discounted_sarsa",
        "reward_centered_sarsa",
        "normalized_sarsa",
        "normalized_reward_centered_sarsa",
        "normalized_differential_sarsa",
    ]
    scales = ["one", "ten", "hundred", "uneven", "lognormal"]
    present_scales = [scale for scale in scales if any(_condition(row, "scale") == scale for row in rows)]
    shifts = _sorted_unique([_condition(row, "reward_shift") for row in rows])
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    for metric, ylabel, log_y in metrics:
        fig, axes = plt.subplots(1, len(present_scales), figsize=(4.0 * len(present_scales), 3.7), sharey=not log_y)
        if len(present_scales) == 1:
            axes = [axes]
        for ax, scale in zip(axes, present_scales):
            for alg in algorithms:
                xs: list[float] = []
                ys: list[float] = []
                es: list[float] = []
                for shift in shifts:
                    match = next(
                        (
                            row
                            for row in rows
                            if _condition(row, "scale") == scale
                            and _condition(row, "algorithm") == alg
                            and float(_condition(row, "reward_shift")) == float(shift)
                        ),
                        None,
                    )
                    if match is None:
                        continue
                    mean, ci95 = _metric(match, metric)
                    xs.append(float(shift))
                    ys.append(mean)
                    es.append(0.0 if not math.isfinite(ci95) else ci95)
                if xs:
                    ax.errorbar(xs, ys, yerr=es, marker="o", linewidth=1.6, capsize=2.5, label=_safe_label(alg))
            ax.set_title(f"scale: {scale}")
            ax.set_xlabel("reward shift")
            ax.grid(True, alpha=0.25)
            if log_y:
                ax.set_yscale("symlog", linthresh=1e-2)
        axes[0].set_ylabel(ylabel)
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=8, frameon=False)
        fig.tight_layout(rect=(0.0, 0.12, 1.0, 1.0))
        out = fig_dir / f"report_{metric}_by_scale.png"
        fig.savefig(out, dpi=180)
        plt.close(fig)
        outputs.append(out)
    return outputs


def plot_dyna_aging(result_dir: Path) -> list[Path]:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    rows = [
        row
        for row in _load_condition_summary(result_dir)
        if _condition(row, "recovery_window") == "post_late" and int(float(_condition(row, "phase"))) == 1
    ]
    budgets = _sorted_unique([_condition(row, "planning_steps") for row in rows])
    modes = ["keep_model", "oracle_flush", "recency_aging", "recency_error_gate"]
    metrics = [
        ("stale_backup_rate", "Late stale-backup rate"),
        ("avg_reward", "Late average reward"),
        ("mean_model_error", "Late mean model error"),
    ]
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for metric, ylabel in metrics:
        fig, ax = plt.subplots(figsize=(7.2, 4.2))
        for mode in modes:
            xs: list[float] = []
            ys: list[float] = []
            es: list[float] = []
            for budget in budgets:
                match = next(
                    (
                        row
                        for row in rows
                        if int(float(_condition(row, "planning_steps"))) == int(float(budget))
                        and _condition(row, "model_mode") == mode
                    ),
                    None,
                )
                if match is None:
                    continue
                mean, ci95 = _metric(match, metric)
                xs.append(float(budget))
                ys.append(mean)
                es.append(0.0 if not math.isfinite(ci95) else ci95)
            if xs:
                ax.errorbar(xs, ys, yerr=es, marker="o", linewidth=1.8, capsize=3, label=_safe_label(mode))
        ax.set_xlabel("planning backups per real step")
        ax.set_ylabel(ylabel)
        ax.set_xticks([float(b) for b in budgets])
        ax.grid(True, alpha=0.25)
        ax.legend(loc="best", fontsize=8)
        fig.tight_layout()
        out = fig_dir / f"report_{metric}_post_late_by_budget.png"
        fig.savefig(out, dpi=180)
        plt.close(fig)
        outputs.append(out)
    return outputs


def plot_predictive_state(result_dir: Path) -> list[Path]:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    rows = _load_condition_summary(result_dir)
    lengths = _sorted_unique([_condition(row, "maze_length") for row in rows])
    algorithms = ["raw", "trace_memory", "recurrent_gvf", "cue_gvf", "oracle"]
    metrics = [
        ("trial_accuracy", "Tail trial accuracy"),
        ("cue_alignment_margin", "Tail cue-alignment margin"),
        ("gvf_abs_td_error", "Tail GVF absolute TD error"),
    ]
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for metric, ylabel in metrics:
        fig, axes = plt.subplots(1, len(lengths), figsize=(4.2 * len(lengths), 3.9), sharey=True)
        if len(lengths) == 1:
            axes = [axes]
        for ax, length in zip(axes, lengths):
            means: list[float] = []
            errs: list[float] = []
            labels: list[str] = []
            for alg in algorithms:
                match = next(
                    (
                        row
                        for row in rows
                        if int(float(_condition(row, "maze_length"))) == int(float(length))
                        and _condition(row, "algorithm") == alg
                    ),
                    None,
                )
                if match is None:
                    continue
                mean, ci95 = _metric(match, metric)
                labels.append(_safe_label(alg))
                means.append(mean)
                errs.append(0.0 if not math.isfinite(ci95) else ci95)
            ax.bar(range(len(labels)), means, yerr=errs, capsize=3)
            ax.set_title(f"length: {int(float(length))}")
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=35, ha="right")
            ax.grid(True, axis="y", alpha=0.25)
            if metric == "trial_accuracy":
                ax.axhline(0.5, color="black", linestyle="--", linewidth=1.0, alpha=0.6)
                ax.set_ylim(0.0, 1.05)
        axes[0].set_ylabel(ylabel)
        fig.tight_layout()
        out = fig_dir / f"report_{metric}_by_maze_length.png"
        fig.savefig(out, dpi=180)
        plt.close(fig)
        outputs.append(out)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Build report-ready summary figures from condition summaries.")
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--kind", choices=["scale", "dyna-aging", "predictive-state"], required=True)
    args = parser.parse_args()
    result_dir = Path(args.result_dir)
    if args.kind == "scale":
        outputs = plot_scale_invariant(result_dir)
    elif args.kind == "dyna-aging":
        outputs = plot_dyna_aging(result_dir)
    else:
        outputs = plot_predictive_state(result_dir)
    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()
