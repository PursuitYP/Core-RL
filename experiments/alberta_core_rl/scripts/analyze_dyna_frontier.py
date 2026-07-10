#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.core import ensure_mpl_config, repo_root


def _metric(record: dict, name: str, field: str = "mean") -> float:
    stats = record["metrics"].get(f"{name}_seed_tail", {})
    value = stats.get(field, math.nan)
    return float(value) if value is not None else math.nan


def _rows(summary_path: Path) -> list[dict[str, float | str | int | bool]]:
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    rows: list[dict[str, float | str | int | bool]] = []
    for record in data:
        condition = record["condition"]
        if int(condition.get("phase", -1)) != 1:
            continue
        if condition.get("recovery_window") != "post_late":
            continue
        model_mode = str(condition["model_mode"])
        rows.append(
            {
                "drift_mode": str(condition["drift_mode"]),
                "algorithm": str(condition["algorithm"]),
                "planning_steps": int(condition["planning_steps"]),
                "model_mode": model_mode,
                "half_life": float(condition["half_life"]),
                "is_oracle": model_mode == "oracle_flush",
                "reward_mean": _metric(record, "avg_reward"),
                "reward_ci95": _metric(record, "avg_reward", "ci95"),
                "stale_mean": _metric(record, "stale_backup_rate"),
                "stale_ci95": _metric(record, "stale_backup_rate", "ci95"),
                "model_error_mean": _metric(record, "mean_model_error"),
                "planning_abs_td_mean": _metric(record, "planning_abs_td"),
                "q_norm_mean": _metric(record, "q_norm"),
                "n_seeds": int(record["metrics"]["avg_reward_seed_tail"].get("n", 0)),
            }
        )
    return sorted(rows, key=lambda r: (str(r["drift_mode"]), int(r["planning_steps"]), str(r["model_mode"]), float(r["half_life"])))


def _is_dominated(row: dict, others: list[dict]) -> bool:
    reward = float(row["reward_mean"])
    stale = float(row["stale_mean"])
    for other in others:
        if other is row:
            continue
        other_reward = float(other["reward_mean"])
        other_stale = float(other["stale_mean"])
        if not all(math.isfinite(v) for v in (reward, stale, other_reward, other_stale)):
            continue
        weakly_better = other_reward >= reward and other_stale <= stale
        strictly_better = other_reward > reward or other_stale < stale
        if weakly_better and strictly_better:
            return True
    return False


def _frontier(rows: list[dict[str, float | str | int | bool]]) -> list[dict[str, float | str | int | bool]]:
    out: list[dict[str, float | str | int | bool]] = []
    for drift_mode in sorted({str(row["drift_mode"]) for row in rows}):
        candidates = [row for row in rows if row["drift_mode"] == drift_mode and not row["is_oracle"]]
        for row in candidates:
            record = dict(row)
            record["pareto_frontier"] = not _is_dominated(row, candidates)
            out.append(record)
    return sorted(out, key=lambda r: (str(r["drift_mode"]), not bool(r["pareto_frontier"]), float(r["stale_mean"]), -float(r["reward_mean"])))


def _write_csv(path: Path, rows: list[dict[str, float | str | int | bool]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _label(row: dict[str, float | str | int | bool]) -> str:
    mode = str(row["model_mode"])
    budget = int(row["planning_steps"])
    half_life = float(row["half_life"])
    if mode in {"keep_model", "no_planning"}:
        return f"p{budget} {mode.replace('_', '-')}"
    return f"p{budget} {mode.replace('_', '-')}, h={int(half_life)}"


def _plot(rows: list[dict[str, float | str | int | bool]], out: Path) -> None:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    drift_modes = sorted({str(row["drift_mode"]) for row in rows})
    fig, axes = plt.subplots(1, len(drift_modes), figsize=(14, 4.2), sharey=True, constrained_layout=True)
    if len(drift_modes) == 1:
        axes = [axes]
    for ax, drift_mode in zip(axes, drift_modes):
        group = [row for row in rows if row["drift_mode"] == drift_mode]
        non_frontier = [row for row in group if not row["pareto_frontier"]]
        frontier = sorted(
            [row for row in group if row["pareto_frontier"]],
            key=lambda row: (float(row["stale_mean"]), float(row["reward_mean"])),
        )
        ax.scatter(
            [float(row["stale_mean"]) for row in non_frontier],
            [float(row["reward_mean"]) for row in non_frontier],
            c="#9ca3af",
            s=36,
            alpha=0.65,
            label="dominated",
        )
        ax.scatter(
            [float(row["stale_mean"]) for row in frontier],
            [float(row["reward_mean"]) for row in frontier],
            c="#d62728",
            s=58,
            alpha=0.9,
            label="Pareto frontier",
        )
        if len(frontier) > 1:
            ax.plot(
                [float(row["stale_mean"]) for row in frontier],
                [float(row["reward_mean"]) for row in frontier],
                c="#d62728",
                linewidth=1.0,
                alpha=0.55,
            )
        label_rows = []
        if frontier:
            label_rows.append(max(frontier, key=lambda item: float(item["reward_mean"])))
            min_stale = min(frontier, key=lambda item: (float(item["stale_mean"]), -float(item["reward_mean"])))
            if min_stale not in label_rows:
                label_rows.append(min_stale)
        for row in label_rows:
            ax.annotate(_label(row), (float(row["stale_mean"]), float(row["reward_mean"])), fontsize=7, xytext=(4, 4), textcoords="offset points")
        ax.set_title(drift_mode.replace("_", " "))
        ax.set_xlabel("post-late stale-backup rate")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("post-late average reward")
    axes[-1].legend(frameon=False, loc="best")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Dyna drift reward/staleness Pareto frontier from condition_summary.json.")
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    result_dir = Path(args.result_dir)
    out_dir = Path(args.out_dir)
    all_rows = _rows(result_dir / "condition_summary.json")
    frontier_rows = _frontier(all_rows)
    _write_csv(out_dir / "dyna_drift_postlate_candidates.csv", all_rows)
    _write_csv(out_dir / "dyna_drift_reward_stale_frontier.csv", frontier_rows)
    _plot(frontier_rows, out_dir / "report_drift_reward_stale_frontier.png")
    manifest = {
        "source_result_dir": str(result_dir),
        "candidate_rows": len(all_rows),
        "realistic_rows": len(frontier_rows),
        "frontier_rows": sum(1 for row in frontier_rows if row["pareto_frontier"]),
        "outputs": [
            "dyna_drift_postlate_candidates.csv",
            "dyna_drift_reward_stale_frontier.csv",
            "report_drift_reward_stale_frontier.png",
        ],
    }
    (out_dir / "dyna_drift_frontier_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
