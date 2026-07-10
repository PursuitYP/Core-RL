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


def plot_gvf_question_design(result_dir: Path, figure_dir: Path | None = None) -> list[Path]:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm

    rows = _load_condition_summary(result_dir)
    cumulants = ["bias", "left_cue", "right_cue", "junction"]
    gammas = _sorted_unique([_condition(row, "gamma") for row in rows])
    fig_dir = figure_dir or result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    values: list[list[float]] = []
    annotations: list[list[str]] = []
    for cumulant in cumulants:
        value_row: list[float] = []
        label_row: list[str] = []
        for gamma in gammas:
            match = next(
                (
                    row
                    for row in rows
                    if _condition(row, "cumulant") == cumulant
                    and float(_condition(row, "gamma")) == float(gamma)
                ),
                None,
            )
            if match is None:
                value = float("nan")
                label = ""
            else:
                mean, _ = _metric(match, "abs_td_error")
                value = max(mean, 1e-7)
                label = f"{mean:.3g}"
            value_row.append(value)
            label_row.append(label)
        values.append(value_row)
        annotations.append(label_row)

    finite_values = [value for row in values for value in row if math.isfinite(value)]
    vmin = max(min(finite_values), 1e-7)
    vmax = max(finite_values)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    im = ax.imshow(values, norm=LogNorm(vmin=vmin, vmax=vmax), cmap="viridis")
    ax.set_xticks(range(len(gammas)))
    ax.set_xticklabels([f"{float(gamma):g}" for gamma in gammas])
    ax.set_yticks(range(len(cumulants)))
    ax.set_yticklabels([_safe_label(cumulant) for cumulant in cumulants])
    ax.set_xlabel("discount gamma")
    ax.set_ylabel("cumulant")
    ax.set_title("Tail absolute TD error; learnability diagnostic only")
    for i, row in enumerate(annotations):
        for j, label in enumerate(row):
            ax.text(j, i, label, ha="center", va="center", color="white", fontsize=9)
    cbar = fig.colorbar(im, ax=ax, shrink=0.85)
    cbar.set_label("seed-tail abs TD error")
    fig.tight_layout()
    out = fig_dir / "report_gvf_question_tail_td_error_heatmap.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return [out]


def _upk_label(row: dict) -> str:
    alg = str(_condition(row, "algorithm"))
    base_labels = {
        "raw": "raw",
        "trace_memory": "trace",
        "oracle": "oracle",
        "gvf_cue": "cue GVF",
        "gvf_terminal": "terminal GVF",
        "gvf_junction": "junction GVF",
    }
    if alg.startswith("gvf_"):
        gamma = float(_condition(row, "gamma"))
        return f"{base_labels.get(alg, _safe_label(alg))}\ng={gamma:g}"
    return base_labels.get(alg, _safe_label(alg))


def _upk_color(label: str) -> str:
    text = label.lower()
    if text.startswith("raw"):
        return "#8c8c8c"
    if text.startswith("trace"):
        return "#4c78a8"
    if text.startswith("oracle"):
        return "#54a24b"
    if text.startswith("cue"):
        return "#f58518"
    if text.startswith("terminal"):
        return "#e45756"
    if text.startswith("junction"):
        return "#b279a2"
    if "low-td" in text:
        return "#72b7b2"
    if "decode" in text:
        return "#ff9da6"
    return "#9d755d"


def _budget_label(algorithm: str) -> str:
    labels = {
        "raw_budget0": "raw",
        "trace_budget2": "trace",
        "oracle_budget2": "oracle",
        "fixed_cue_gvf": "fixed cue",
        "fixed_terminal_gvf": "fixed term",
        "fixed_junction_gvf": "fixed junction",
        "low_td_error_selector": "low-TD sel.",
        "oracle_decode_selector": "decode sel.",
    }
    return labels.get(algorithm, _safe_label(algorithm))


def plot_useful_predictive_knowledge(result_dir: Path, figure_dir: Path | None = None) -> list[Path]:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    rows = _load_condition_summary(result_dir)
    lengths = _sorted_unique([_condition(row, "maze_length") for row in rows])
    fig_dir = figure_dir or result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    metrics = [
        ("trial_accuracy", "Tail trial accuracy", "report_upk_trial_accuracy_by_length.png", (0.0, 1.05)),
        (
            "decision_cue_decoding_correct",
            "Decision-time cue decoding",
            "report_upk_decision_decoding_by_length.png",
            (0.0, 1.05),
        ),
        ("cue_alignment_margin", "Tail signed cue margin", "report_upk_cue_margin_by_length.png", None),
    ]
    for metric, ylabel, filename, ylim in metrics:
        ncols = min(2, len(lengths))
        nrows = math.ceil(len(lengths) / ncols)
        fig, axes_arr = plt.subplots(nrows, ncols, figsize=(6.6 * ncols, 4.4 * nrows), sharey=ylim is not None)
        axes = list(axes_arr.flat) if hasattr(axes_arr, "flat") else [axes_arr]
        for ax, length in zip(axes, lengths):
            length_rows = [row for row in rows if int(float(_condition(row, "maze_length"))) == int(float(length))]
            length_rows = sorted(length_rows, key=lambda row: (_condition(row, "algorithm"), float(_condition(row, "gamma") or 0.0)))
            labels = [_upk_label(row) for row in length_rows]
            means = []
            errs = []
            for row in length_rows:
                mean, ci95 = _metric(row, metric)
                means.append(mean)
                errs.append(0.0 if not math.isfinite(ci95) else ci95)
            ax.bar(range(len(labels)), means, yerr=errs, capsize=2.5, color=[_upk_color(label) for label in labels])
            if metric in {"trial_accuracy", "decision_cue_decoding_correct"}:
                ax.axhline(0.5, color="black", linestyle="--", linewidth=1.0, alpha=0.55)
            ax.set_title(f"maze length {int(float(length))}")
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=38, ha="right", fontsize=8)
            ax.grid(True, axis="y", alpha=0.25)
            if ylim is not None:
                ax.set_ylim(*ylim)
        for ax in axes[len(lengths) :]:
            ax.axis("off")
        axes[0].set_ylabel(ylabel)
        fig.tight_layout()
        out = fig_dir / filename
        fig.savefig(out, dpi=180)
        plt.close(fig)
        outputs.append(out)
    return outputs


def plot_useful_predictive_knowledge_budget(result_dir: Path, figure_dir: Path | None = None) -> list[Path]:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    rows = _load_condition_summary(result_dir)
    lengths = _sorted_unique([_condition(row, "maze_length") for row in rows])
    algorithms = [
        "raw_budget0",
        "trace_budget2",
        "oracle_budget2",
        "fixed_cue_gvf",
        "fixed_terminal_gvf",
        "fixed_junction_gvf",
        "low_td_error_selector",
        "oracle_decode_selector",
    ]
    fig_dir = figure_dir or result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    metrics = [
        ("trial_accuracy", "Tail trial accuracy", "report_upk_budget_trial_accuracy.png", (0.0, 1.05)),
        (
            "decision_selected_cue_decoding_correct",
            "Selected feature cue decoding",
            "report_upk_budget_selected_decoding.png",
            (0.0, 1.05),
        ),
        ("selected_is_cue", "Fraction selected cue-GVF pair", "report_upk_budget_selected_cue.png", (0.0, 1.05)),
    ]
    for metric, ylabel, filename, ylim in metrics:
        ncols = min(2, len(lengths))
        nrows = math.ceil(len(lengths) / ncols)
        fig, axes_arr = plt.subplots(nrows, ncols, figsize=(7.0 * ncols, 4.4 * nrows), sharey=True)
        axes = list(axes_arr.flat) if hasattr(axes_arr, "flat") else [axes_arr]
        for ax, length in zip(axes, lengths):
            labels: list[str] = []
            means: list[float] = []
            errs: list[float] = []
            for algorithm in algorithms:
                match = next(
                    (
                        row
                        for row in rows
                        if int(float(_condition(row, "maze_length"))) == int(float(length))
                        and _condition(row, "algorithm") == algorithm
                    ),
                    None,
                )
                if match is None:
                    continue
                mean, ci95 = _metric(match, metric)
                labels.append(_budget_label(algorithm))
                means.append(mean)
                errs.append(0.0 if not math.isfinite(ci95) else ci95)
            ax.bar(range(len(labels)), means, yerr=errs, capsize=2.5, color=[_upk_color(label) for label in labels])
            if metric in {"trial_accuracy", "decision_selected_cue_decoding_correct"}:
                ax.axhline(0.5, color="black", linestyle="--", linewidth=1.0, alpha=0.55)
            ax.set_title(f"maze length {int(float(length))}")
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
            ax.set_ylim(*ylim)
            ax.grid(True, axis="y", alpha=0.25)
        for ax in axes[len(lengths) :]:
            ax.axis("off")
        axes[0].set_ylabel(ylabel)
        fig.tight_layout()
        out = fig_dir / filename
        fig.savefig(out, dpi=180)
        plt.close(fig)
        outputs.append(out)
    return outputs
