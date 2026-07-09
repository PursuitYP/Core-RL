#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.core import ensure_mpl_config, repo_root, write_csv, write_json


def _float(row: dict[str, str], key: str, default: float = math.nan) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _cue_score(row: dict[str, str]) -> float:
    algorithm = row["algorithm"]
    hidden_cue = int(_float(row, "hidden_cue", 0.0))
    if algorithm in {"recurrent_gvf", "cue_gvf"}:
        return _float(row, "gvf_left_value", 0.0) - _float(row, "gvf_right_value", 0.0)
    if algorithm == "trace_memory":
        return _float(row, "cue_trace_left", 0.0) - _float(row, "cue_trace_right", 0.0)
    if algorithm == "oracle":
        return 1.0 if hidden_cue == 0 else -1.0
    return 0.0


def _decoding_accuracy(score: float, hidden_cue: int) -> float:
    if abs(score) < 1e-12:
        return 0.5
    predicts_left = score > 0.0
    return float((hidden_cue == 0 and predicts_left) or (hidden_cue == 1 and not predicts_left))


def summarize_decodability(result_dir: Path) -> tuple[list[dict], dict]:
    rows_by_key: dict[tuple[str, int], list[dict[str, float]]] = defaultdict(list)
    max_step_by_key: dict[tuple[str, int, int], float] = defaultdict(float)
    metrics_path = result_dir / "metrics.csv"
    with metrics_path.open(newline="", encoding="utf-8") as f:
        raw_rows = list(csv.DictReader(f))
    for row in raw_rows:
        key = (row["algorithm"], int(_float(row, "maze_length", 0.0)), int(_float(row, "seed", 0.0)))
        max_step_by_key[key] = max(max_step_by_key[key], _float(row, "step", 0.0))
    for row in raw_rows:
        algorithm = row["algorithm"]
        maze_length = int(_float(row, "maze_length", 0.0))
        seed = int(_float(row, "seed", 0.0))
        step = _float(row, "step", 0.0)
        max_step = max_step_by_key[(algorithm, maze_length, seed)]
        if step < 0.8 * max_step:
            continue
        position = _float(row, "maze_position", 0.0)
        if not (1.0 <= position <= float(maze_length)):
            continue
        hidden_cue = int(_float(row, "hidden_cue", 0.0))
        score = _cue_score(row)
        rows_by_key[(algorithm, maze_length)].append(
            {
                "seed": float(seed),
                "score": score,
                "accuracy": _decoding_accuracy(score, hidden_cue),
                "margin": abs(score),
            }
        )
    summary_rows: list[dict] = []
    for (algorithm, maze_length), values in sorted(rows_by_key.items(), key=lambda item: (item[0][1], item[0][0])):
        if not values:
            continue
        accuracies = np.asarray([value["accuracy"] for value in values], dtype=float)
        margins = np.asarray([value["margin"] for value in values], dtype=float)
        seed_means = []
        by_seed: dict[int, list[float]] = defaultdict(list)
        for value in values:
            by_seed[int(value["seed"])].append(value["accuracy"])
        for seed_values in by_seed.values():
            seed_means.append(float(np.mean(seed_values)))
        seed_arr = np.asarray(seed_means, dtype=float)
        stderr = float(np.std(seed_arr, ddof=1) / np.sqrt(len(seed_arr))) if len(seed_arr) > 1 else 0.0
        summary_rows.append(
            {
                "algorithm": algorithm,
                "maze_length": maze_length,
                "n_rows": len(values),
                "n_seeds": len(seed_arr),
                "tail_cue_decoding_accuracy": float(np.mean(accuracies)),
                "tail_cue_decoding_ci95": float(1.96 * stderr),
                "tail_abs_cue_margin": float(np.mean(margins)),
            }
        )
    summary = {
        "question": "Do predictive features preserve cue information before the T-maze choice point?",
        "result_dir": str(result_dir),
        "metric": "tail_cue_decoding_accuracy",
        "n_groups": len(summary_rows),
    }
    return summary_rows, summary


def plot_decodability(result_dir: Path, summary_rows: list[dict]) -> Path:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    algorithms = ["raw", "trace_memory", "recurrent_gvf", "cue_gvf", "oracle"]
    lengths = sorted({int(row["maze_length"]) for row in summary_rows})
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    for algorithm in algorithms:
        xs: list[int] = []
        ys: list[float] = []
        es: list[float] = []
        for length in lengths:
            match = next(
                (row for row in summary_rows if row["algorithm"] == algorithm and int(row["maze_length"]) == length),
                None,
            )
            if match is None:
                continue
            xs.append(length)
            ys.append(float(match["tail_cue_decoding_accuracy"]))
            es.append(float(match["tail_cue_decoding_ci95"]))
        if xs:
            ax.errorbar(xs, ys, yerr=es, marker="o", linewidth=1.7, capsize=3, label=algorithm.replace("_", " "))
    ax.axhline(0.5, color="#666666", linestyle="--", linewidth=1.0, label="chance")
    ax.set_xlabel("T-maze corridor length")
    ax.set_ylabel("Tail cue-decoding accuracy")
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.25)
    ax.legend(loc="lower left", ncol=2, fontsize=8, frameon=False)
    fig.tight_layout()
    out = result_dir / "figures" / "report_cue_decodability_by_length.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze cue decodability in predictive-state T-maze runs.")
    parser.add_argument("--result-dir", required=True)
    args = parser.parse_args()
    result_dir = Path(args.result_dir)
    rows, summary = summarize_decodability(result_dir)
    write_csv(result_dir / "cue_decodability_summary.csv", rows)
    write_json(result_dir / "cue_decodability_summary.json", summary)
    figure = plot_decodability(result_dir, rows)
    print(result_dir / "cue_decodability_summary.csv")
    print(figure)


if __name__ == "__main__":
    main()
