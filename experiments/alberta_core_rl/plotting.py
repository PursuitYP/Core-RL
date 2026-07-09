from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

from .core import ensure_mpl_config, moving_average, repo_root


def read_metrics(path: Path) -> list[dict[str, str]]:
    metrics = path / "metrics.csv" if path.is_dir() else path
    with metrics.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(row: dict[str, str], key: str, default: float = np.nan) -> float:
    try:
        return float(row[key])
    except Exception:
        return default


def plot_learning_curve(result_dir: Path, y_key: str | None = None, group_keys: list[str] | None = None) -> Path:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    rows = read_metrics(result_dir)
    numeric_keys = [
        key
        for key in rows[0].keys()
        if key not in {"seed", "step"} and any(np.isfinite(to_float(row, key)) for row in rows[:100])
    ]
    if y_key is None:
        for candidate in [
            "rmse",
            "avg_unshifted_reward",
            "avg_reward",
            "best_action_rate",
            "abs_td_error",
            "abs_error",
            "td_error",
            "value_norm",
            "q_norm",
        ]:
            if candidate in numeric_keys:
                y_key = candidate
                break
    if y_key is None:
        y_key = numeric_keys[0]
    if group_keys is None:
        group_keys = ["algorithm"] if "algorithm" in rows[0] else ["cumulant"]
    grouped: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        label_parts = [row.get(key, "na") for key in group_keys if key in row]
        label = " | ".join(label_parts) if label_parts else "series"
        grouped[label][int(float(row["step"]))].append(to_float(row, y_key))

    n_series = len(grouped)
    fig_width = 7.0 if n_series <= 12 else 12.0 if n_series <= 32 else 15.0
    fig_height = 4.2 if n_series <= 12 else 6.2 if n_series <= 32 else 7.8
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    for label, by_step in sorted(grouped.items()):
        step_values = []
        for step in sorted(by_step):
            arr = np.asarray(by_step[int(step)], dtype=float)
            arr = arr[np.isfinite(arr)]
            if len(arr):
                step_values.append((int(step), float(np.mean(arr))))
        if not step_values:
            continue
        steps = np.array([item[0] for item in step_values], dtype=int)
        values = np.array([item[1] for item in step_values], dtype=float)
        if len(values) > 20:
            smooth = moving_average(values, max(5, len(values) // 60))
            plot_steps = steps[-len(smooth) :]
        else:
            smooth = values
            plot_steps = steps
        ax.plot(plot_steps, smooth, label=label)
    ax.set_xlabel("stream step")
    ax.set_ylabel(y_key)
    ax.grid(True, alpha=0.25)
    if n_series > 12:
        ncol = 2 if n_series <= 24 else 3 if n_series <= 48 else 4
        ax.legend(fontsize=6.5, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=ncol, frameon=False)
        fig.tight_layout(rect=(0.0, 0.16, 1.0, 1.0))
    else:
        ax.legend(fontsize=8)
        fig.tight_layout()
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    suffix = "_by_" + "-".join(group_keys) if group_keys else ""
    out = fig_dir / f"{y_key}{suffix}_curve.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out
