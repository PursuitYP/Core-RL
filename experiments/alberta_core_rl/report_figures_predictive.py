from __future__ import annotations

import math
from pathlib import Path

from .core import ensure_mpl_config, repo_root
from .report_figures_core import (
    _condition,
    _load_condition_summary,
    _metric,
    _safe_label,
    _sorted_unique,
)


def plot_predictive_state(result_dir: Path, figure_dir: Path | None = None) -> list[Path]:
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
    fig_dir = figure_dir or result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for metric, ylabel in metrics:
        metric_algorithms = algorithms if metric == "trial_accuracy" else ["recurrent_gvf", "cue_gvf"]
        ncols = min(2, len(lengths))
        nrows = math.ceil(len(lengths) / ncols)
        fig, axes_arr = plt.subplots(nrows, ncols, figsize=(4.8 * ncols, 3.7 * nrows), sharey=True)
        axes = list(axes_arr.flat) if hasattr(axes_arr, "flat") else [axes_arr]
        for ax, length in zip(axes, lengths):
            means: list[float] = []
            errs: list[float] = []
            labels: list[str] = []
            for alg in metric_algorithms:
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
        for ax in axes[len(lengths) :]:
            ax.axis("off")
        axes[0].set_ylabel(ylabel)
        fig.tight_layout()
        out = fig_dir / f"report_{metric}_by_maze_length.png"
        fig.savefig(out, dpi=180)
        plt.close(fig)
        outputs.append(out)
    return outputs
