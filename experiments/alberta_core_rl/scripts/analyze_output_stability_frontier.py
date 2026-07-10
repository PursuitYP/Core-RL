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


SCALE_ORDER = ["one", "ten", "hundred", "uneven", "lognormal"]


def _metric(record: dict, name: str, field: str = "mean") -> float:
    stats = record["metrics"].get(f"{name}_seed_tail", {})
    value = stats.get(field, math.nan)
    return float(value) if value is not None else math.nan


def _condition_rows(summary_path: Path) -> list[dict[str, float | str | bool]]:
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    rows: list[dict[str, float | str | bool]] = []
    for record in data:
        condition = record["condition"]
        diverged = _metric(record, "diverged")
        rows.append(
            {
                "algorithm": str(condition["algorithm"]),
                "scale": str(condition["scale"]),
                "alpha": float(condition["alpha"]),
                "lambda": float(condition.get("lambda", 0.0)),
                "stable": diverged == 0.0,
                "diverged_seed_tail_mean": diverged,
                "rmse_mean": _metric(record, "rmse"),
                "rmse_ci95": _metric(record, "rmse", "ci95"),
                "prediction_change_mean": _metric(record, "prediction_change"),
                "prediction_change_ci95": _metric(record, "prediction_change", "ci95"),
            }
        )
    return sorted(rows, key=lambda r: (str(r["algorithm"]), SCALE_ORDER.index(str(r["scale"])), float(r["alpha"])))


def _frontier(rows: list[dict[str, float | str | bool]]) -> list[dict[str, float | str | bool | int]]:
    out: list[dict[str, float | str | bool | int]] = []
    algorithms = sorted({str(row["algorithm"]) for row in rows})
    for algorithm in algorithms:
        for scale in SCALE_ORDER:
            group = [row for row in rows if row["algorithm"] == algorithm and row["scale"] == scale]
            stable = [row for row in group if bool(row["stable"])]
            best_rmse = min(stable, key=lambda row: float(row["rmse_mean"])) if stable else None
            out.append(
                {
                    "algorithm": algorithm,
                    "scale": scale,
                    "tested_cells": len(group),
                    "stable_cells": len(stable),
                    "max_stable_alpha": max((float(row["alpha"]) for row in stable), default=math.nan),
                    "best_stable_alpha": float(best_rmse["alpha"]) if best_rmse else math.nan,
                    "best_stable_rmse": float(best_rmse["rmse_mean"]) if best_rmse else math.nan,
                    "best_stable_rmse_ci95": float(best_rmse["rmse_ci95"]) if best_rmse else math.nan,
                    "mean_stable_prediction_change": sum(float(row["prediction_change_mean"]) for row in stable) / len(stable)
                    if stable
                    else math.nan,
                    "any_divergence": len(stable) < len(group),
                }
            )
    return out


def _write_csv(path: Path, rows: list[dict[str, float | str | bool | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _plot(frontier: list[dict[str, float | str | bool | int]], out: Path, title: str) -> None:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt
    import numpy as np

    algorithms = sorted({str(row["algorithm"]) for row in frontier})
    matrix = np.full((len(algorithms), len(SCALE_ORDER)), np.nan)
    for i, algorithm in enumerate(algorithms):
        for j, scale in enumerate(SCALE_ORDER):
            match = next(row for row in frontier if row["algorithm"] == algorithm and row["scale"] == scale)
            alpha = float(match["max_stable_alpha"])
            matrix[i, j] = math.log10(alpha) if math.isfinite(alpha) and alpha > 0.0 else np.nan
    fig, ax = plt.subplots(figsize=(8.8, 0.55 * len(algorithms) + 2.0), constrained_layout=True)
    im = ax.imshow(matrix, aspect="auto", cmap="viridis", vmin=-3.0, vmax=-0.5)
    ax.set_xticks(np.arange(len(SCALE_ORDER)))
    ax.set_xticklabels(SCALE_ORDER)
    ax.set_yticks(np.arange(len(algorithms)))
    ax.set_yticklabels([name.replace("_", "\n") for name in algorithms])
    ax.set_title(title)
    for i in range(len(algorithms)):
        for j in range(len(SCALE_ORDER)):
            value = matrix[i, j]
            text = "none" if not math.isfinite(float(value)) else f"{10 ** value:g}"
            ax.text(j, i, text, ha="center", va="center", color="white" if math.isfinite(float(value)) and value < -1.2 else "black", fontsize=8)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("log10(max stable alpha)")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180)
    plt.close(fig)


def _analyze_one(result_dir: Path, out_dir: Path, prefix: str, title: str) -> dict:
    rows = _condition_rows(result_dir / "condition_summary.json")
    frontier = _frontier(rows)
    _write_csv(out_dir / f"{prefix}_condition_stability.csv", rows)
    _write_csv(out_dir / f"{prefix}_max_stable_alpha_frontier.csv", frontier)
    _plot(frontier, out_dir / f"report_{prefix}_max_stable_alpha_frontier.png", title)
    return {
        "result_dir": str(result_dir),
        "condition_rows": len(rows),
        "frontier_rows": len(frontier),
        "outputs": [
            f"{prefix}_condition_stability.csv",
            f"{prefix}_max_stable_alpha_frontier.csv",
            f"report_{prefix}_max_stable_alpha_frontier.png",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze max-stable-alpha frontiers for Output-Controlled TD results.")
    parser.add_argument("--primary-result-dir", required=True)
    parser.add_argument("--fairness-result-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    manifest = {
        "primary": _analyze_one(Path(args.primary_result_dir), out_dir, "primary", "Primary sweep: max stable alpha by algorithm and scale"),
        "fairness": _analyze_one(Path(args.fairness_result_dir), out_dir, "fairness", "Fairness audit: max stable alpha by algorithm and scale"),
    }
    (out_dir / "output_stability_frontier_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
