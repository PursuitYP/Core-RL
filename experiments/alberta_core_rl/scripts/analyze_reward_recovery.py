#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.core import ensure_mpl_config, repo_root


EARLY_LIMIT = 1000.0
KEYS = ("algorithm", "switch_type", "alpha", "beta", "gamma")


def _float(row: dict[str, str], name: str, default: float = math.nan) -> float:
    value = row.get(name)
    if value in {None, ""}:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _seed_key(row: dict[str, str]) -> tuple:
    return (
        row["algorithm"],
        row["switch_type"],
        float(row["alpha"]),
        float(row["beta"]),
        float(row["gamma"]),
        int(float(row["seed"])),
    )


def _summ(values: list[float]) -> dict[str, float]:
    clean = [v for v in values if math.isfinite(v)]
    if not clean:
        return {"n": 0, "mean": math.nan, "std": math.nan, "stderr": math.nan, "ci95": math.nan}
    mean = sum(clean) / len(clean)
    if len(clean) == 1:
        return {"n": 1, "mean": mean, "std": 0.0, "stderr": 0.0, "ci95": 0.0}
    var = sum((v - mean) ** 2 for v in clean) / (len(clean) - 1)
    std = math.sqrt(var)
    stderr = std / math.sqrt(len(clean))
    return {"n": len(clean), "mean": mean, "std": std, "stderr": stderr, "ci95": 1.96 * stderr}


def _read_seed_stats(metrics_path: Path) -> dict[tuple, dict[str, float]]:
    stats: dict[tuple, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    with metrics_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(float(row.get("phase", 0.0))) != 1:
                continue
            key = _seed_key(row)
            steps_since = _float(row, "steps_since_switch")
            reward = _float(row, "avg_unshifted_reward")
            accept = _float(row, "accept_rate")
            q_norm = _float(row, "q_norm")
            bar_error = _float(row, "reward_bar_abs_error_ema")
            diverged = _float(row, "diverged", 0.0)
            stats[key]["diverged"] = max(stats[key]["diverged"], diverged)
            if 0.0 <= steps_since <= EARLY_LIMIT:
                stats[key]["early_reward_sum"] += reward
                stats[key]["early_accept_sum"] += accept
                stats[key]["early_q_sum"] += q_norm
                stats[key]["early_bar_error_sum"] += bar_error
                stats[key]["early_count"] += 1.0
            if row.get("recovery_window") == "post_late":
                stats[key]["late_reward_sum"] += reward
                stats[key]["late_accept_sum"] += accept
                stats[key]["late_q_sum"] += q_norm
                stats[key]["late_bar_error_sum"] += bar_error
                stats[key]["late_count"] += 1.0
    return stats


def _seed_rows(seed_stats: dict[tuple, dict[str, float]]) -> list[dict[str, float | str | int]]:
    rows: list[dict[str, float | str | int]] = []
    for key, vals in sorted(seed_stats.items(), key=lambda item: str(item[0])):
        algorithm, switch_type, alpha, beta, gamma, seed = key
        early_count = vals.get("early_count", 0.0)
        late_count = vals.get("late_count", 0.0)
        rows.append(
            {
                "algorithm": algorithm,
                "switch_type": switch_type,
                "alpha": alpha,
                "beta": beta,
                "gamma": gamma,
                "seed": seed,
                "early_reward_auc": vals.get("early_reward_sum", math.nan) / early_count
                if early_count
                else math.nan,
                "early_accept_auc": vals.get("early_accept_sum", math.nan) / early_count
                if early_count
                else math.nan,
                "early_q_norm": vals.get("early_q_sum", math.nan) / early_count if early_count else math.nan,
                "early_reward_bar_abs_error": vals.get("early_bar_error_sum", math.nan) / early_count
                if early_count
                else math.nan,
                "late_reward": vals.get("late_reward_sum", math.nan) / late_count if late_count else math.nan,
                "late_accept_rate": vals.get("late_accept_sum", math.nan) / late_count if late_count else math.nan,
                "late_q_norm": vals.get("late_q_sum", math.nan) / late_count if late_count else math.nan,
                "late_reward_bar_abs_error": vals.get("late_bar_error_sum", math.nan) / late_count
                if late_count
                else math.nan,
                "diverged": vals.get("diverged", 0.0),
                "early_points": int(early_count),
                "late_points": int(late_count),
            }
        )
    return rows


def _aggregate(seed_rows: list[dict[str, float | str | int]]) -> list[dict[str, float | str]]:
    grouped: dict[tuple, list[dict[str, float | str | int]]] = defaultdict(list)
    for row in seed_rows:
        key = tuple(row[name] for name in KEYS)
        grouped[key].append(row)
    metrics = [
        "early_reward_auc",
        "early_accept_auc",
        "early_q_norm",
        "early_reward_bar_abs_error",
        "late_reward",
        "late_accept_rate",
        "late_q_norm",
        "late_reward_bar_abs_error",
        "diverged",
    ]
    out: list[dict[str, float | str]] = []
    for key, rows in sorted(grouped.items(), key=lambda item: str(item[0])):
        record = {name: value for name, value in zip(KEYS, key)}
        record["n_seeds"] = len(rows)
        for metric in metrics:
            summary = _summ([float(row[metric]) for row in rows])
            record[f"{metric}_mean"] = summary["mean"]
            record[f"{metric}_ci95"] = summary["ci95"]
        out.append(record)
    return out


def _compact(aggregate_rows: list[dict[str, float | str]]) -> list[dict[str, float | str]]:
    grouped: dict[tuple[str, str], list[dict[str, float | str]]] = defaultdict(list)
    for row in aggregate_rows:
        grouped[(str(row["switch_type"]), str(row["algorithm"]))].append(row)
    selected: list[dict[str, float | str]] = []
    for key, rows in sorted(grouped.items()):
        best = max(rows, key=lambda row: float(row["early_reward_auc_mean"]))
        record = dict(best)
        record["selection_rule"] = "max early_reward_auc_mean within switch_type and algorithm"
        selected.append(record)
    return selected


def _write_csv(path: Path, rows: list[dict[str, float | str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _plot_grouped(
    rows: list[dict[str, float | str]],
    out: Path,
    metric: str,
    ylabel: str,
    title: str,
) -> None:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt
    import numpy as np

    algorithms = ["discounted_sarsa", "reward_centered_sarsa", "differential_sarsa"]
    switches = sorted({str(row["switch_type"]) for row in rows})
    labels = {"discounted_sarsa": "discounted", "reward_centered_sarsa": "reward-centered", "differential_sarsa": "differential"}
    x = np.arange(len(switches))
    width = 0.24
    fig, ax = plt.subplots(figsize=(8.4, 4.2), constrained_layout=True)
    for i, algorithm in enumerate(algorithms):
        means = []
        errors = []
        for switch in switches:
            match = next((row for row in rows if row["switch_type"] == switch and row["algorithm"] == algorithm), None)
            means.append(float(match[f"{metric}_mean"]) if match else math.nan)
            errors.append(float(match[f"{metric}_ci95"]) if match else 0.0)
        ax.bar(x + (i - 1) * width, means, width, yerr=errors, capsize=3, label=labels[algorithm])
    ax.set_xticks(x)
    ax.set_xticklabels([switch.replace("_", " ") for switch in switches])
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncol=3)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze reward-origin switch recovery from metrics.csv.")
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    result_dir = Path(args.result_dir)
    out_dir = Path(args.out_dir)
    metrics_path = result_dir / "metrics.csv"
    seed_rows = _seed_rows(_read_seed_stats(metrics_path))
    aggregate_rows = _aggregate(seed_rows)
    compact_rows = _compact(aggregate_rows)
    _write_csv(out_dir / "reward_recovery_seed_summary.csv", seed_rows)
    _write_csv(out_dir / "reward_recovery_condition_summary.csv", aggregate_rows)
    _write_csv(out_dir / "reward_recovery_compact_best_by_family.csv", compact_rows)
    _plot_grouped(
        compact_rows,
        out_dir / "report_reward_recovery_auc_best_by_family.png",
        "early_reward_auc",
        f"early recovery reward score, first {int(EARLY_LIMIT)} steps",
        "Best early post-switch recovery by algorithm family",
    )
    _plot_grouped(
        compact_rows,
        out_dir / "report_reward_recovery_accept_best_by_family.png",
        "early_accept_auc",
        f"early accept rate, first {int(EARLY_LIMIT)} steps",
        "Early post-switch accept behavior by algorithm family",
    )
    manifest = {
        "source_result_dir": str(result_dir),
        "early_limit_steps": EARLY_LIMIT,
        "seed_rows": len(seed_rows),
        "condition_rows": len(aggregate_rows),
        "compact_rows": len(compact_rows),
        "outputs": [
            "reward_recovery_seed_summary.csv",
            "reward_recovery_condition_summary.csv",
            "reward_recovery_compact_best_by_family.csv",
            "report_reward_recovery_auc_best_by_family.png",
            "report_reward_recovery_accept_best_by_family.png",
        ],
    }
    (out_dir / "reward_recovery_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
