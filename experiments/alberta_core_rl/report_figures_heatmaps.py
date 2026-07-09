from __future__ import annotations

import csv
import math
from pathlib import Path
from collections import defaultdict

from .core import ensure_mpl_config, repo_root
from .report_figures_core import (
    _condition,
    _load_condition_summary,
    _mean_over,
    _metric,
    _save_heatmap,
    _short_label,
    _sorted_unique,
)

def plot_output_td(result_dir: Path, figure_dir: Path | None = None) -> list[Path]:
    rows = _load_condition_summary(result_dir)
    fig_dir = figure_dir or result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    algorithms = ["fixed", "normalized", "trace_normalized", "true_online", "true_online_normalized"]
    scales = ["one", "ten", "hundred", "uneven", "lognormal"]
    scales = [scale for scale in scales if any(_condition(row, "scale") == scale for row in rows)]
    alphas = _sorted_unique([_condition(row, "alpha") for row in rows])
    columns = [(scale, alpha) for scale in scales for alpha in alphas]
    labels = [f"{scale}\na={float(alpha):g}" for scale, alpha in columns]
    divergence = _seed_divergence_rates(result_dir)
    outputs: list[Path] = []
    specs = [
        ("rmse", "Tail RMSE stability atlas", "magma", True, "report_log_rmse_heatmap.png", "mean"),
        ("seed_divergence", "Seed-level divergence rate atlas", "Reds", False, "report_divergence_heatmap.png", "mean"),
        ("prediction_change", "Tail output-change atlas", "viridis", True, "report_prediction_change_heatmap.png", "mean"),
    ]
    for metric, title, cmap, log10, name, reducer in specs:
        matrix: list[list[float]] = []
        for alg in algorithms:
            row_vals = []
            for scale, alpha in columns:
                if metric == "seed_divergence":
                    row_vals.append(divergence.get((alg, scale, float(alpha)), math.nan))
                else:
                    matches = [
                        row
                        for row in rows
                        if _condition(row, "algorithm") == alg
                        and _condition(row, "scale") == scale
                        and math.isclose(float(_condition(row, "alpha")), float(alpha))
                    ]
                    row_vals.append(_mean_over(matches, metric, reducer=reducer))
            matrix.append(row_vals)
        outputs.append(
            _save_heatmap(
                matrix,
                [_short_label(alg) for alg in algorithms],
                labels,
                title,
                fig_dir / name,
                cmap=cmap,
                log10=log10,
                value_format=".2f",
            )
        )
    return outputs


def _seed_divergence_rates(result_dir: Path) -> dict[tuple[str, str, float], float]:
    metrics_path = result_dir / "metrics.csv"
    if not metrics_path.exists():
        return {}
    seed_events: dict[tuple[str, str, float, int], bool] = defaultdict(bool)
    with metrics_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["algorithm"], row["scale"], float(row["alpha"]), int(float(row["seed"])))
            seed_events[key] = seed_events[key] or float(row.get("diverged") or 0.0) > 0.0
    grouped: dict[tuple[str, str, float], list[bool]] = defaultdict(list)
    for (algorithm, scale, alpha, _seed), diverged in seed_events.items():
        grouped[(algorithm, scale, alpha)].append(diverged)
    return {key: sum(values) / len(values) for key, values in grouped.items() if values}


def plot_reward_centered(result_dir: Path) -> list[Path]:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    rows = _load_condition_summary(result_dir)
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    algorithms = ["discounted_sarsa", "reward_centered_sarsa", "differential_sarsa"]
    shifts = _sorted_unique([_condition(row, "reward_shift") for row in rows])
    alphas = _sorted_unique([_condition(row, "alpha") for row in rows])
    metrics = [
        ("avg_unshifted_reward", "Tail unshifted reward", False),
        ("q_norm", "Tail Q norm", True),
        ("high_priority_accept", "Tail high-priority accept rate", False),
        ("diverged", "Divergence rate", False),
    ]
    outputs: list[Path] = []
    for metric, ylabel, log_y in metrics:
        ncols = min(2, len(alphas))
        nrows = math.ceil(len(alphas) / ncols)
        fig, axes_arr = plt.subplots(nrows, ncols, figsize=(4.8 * ncols, 3.7 * nrows), sharey=not log_y)
        axes = list(axes_arr.flat) if hasattr(axes_arr, "flat") else [axes_arr]
        for ax, alpha in zip(axes, alphas):
            for alg in algorithms:
                xs: list[float] = []
                ys: list[float] = []
                es: list[float] = []
                for shift in shifts:
                    match = next(
                        (
                            row
                            for row in rows
                            if _condition(row, "algorithm") == alg
                            and math.isclose(float(_condition(row, "alpha")), float(alpha))
                            and math.isclose(float(_condition(row, "reward_shift")), float(shift))
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
                    ax.errorbar(xs, ys, yerr=es, marker="o", linewidth=1.7, capsize=3, label=_short_label(alg))
            ax.set_title(f"alpha={float(alpha):g}")
            ax.set_xlabel("reward shift")
            ax.grid(True, alpha=0.25)
            if log_y:
                ax.set_yscale("symlog", linthresh=1.0)
        for ax in axes[len(alphas) :]:
            ax.axis("off")
        axes[0].set_ylabel(ylabel)
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=8, frameon=False)
        fig.tight_layout(rect=(0.0, 0.12, 1.0, 1.0))
        out = fig_dir / f"report_{metric}_by_reward_shift.png"
        fig.savefig(out, dpi=180)
        plt.close(fig)
        outputs.append(out)
    return outputs


def plot_reward_centered_sensitivity(result_dir: Path) -> list[Path]:
    all_rows = _load_condition_summary(result_dir)
    rows = [
        row
        for row in all_rows
        if _condition(row, "recovery_window") == "post_late" and int(float(_condition(row, "phase"))) == 1
    ]
    if not rows:
        rows = [row for row in all_rows if int(float(_condition(row, "phase"))) == 1]
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    alphas = [float(alpha) for alpha in _sorted_unique([_condition(row, "alpha") for row in rows])]
    target_alpha = min(alphas, key=lambda value: abs(value - 0.05)) if alphas else math.nan
    rows = [row for row in rows if math.isclose(float(_condition(row, "alpha")), target_alpha)]
    algorithms = ["discounted_sarsa", "reward_centered_sarsa", "differential_sarsa"]
    betas = _sorted_unique([_condition(row, "beta") for row in rows])
    gammas = _sorted_unique([_condition(row, "gamma") for row in rows])
    switch_types = _sorted_unique([_condition(row, "switch_type") for row in rows])
    row_keys = [(algorithm, beta) for algorithm in algorithms for beta in betas]
    columns = [(switch_type, gamma) for switch_type in switch_types for gamma in gammas]
    col_labels = [f"{str(switch_type).replace('_', ' ')}\ng={float(gamma):g}" for switch_type, gamma in columns]
    outputs: list[Path] = []
    for metric, title, cmap, log10, name, reducer in [
        ("avg_unshifted_reward", f"Post-late reward sensitivity at alpha={target_alpha:g}", "viridis", False, "report_reward_sensitivity_reward.png", "mean"),
        ("reward_bar_abs_error_ema", f"Reward-rate tracking error at alpha={target_alpha:g}", "magma", True, "report_reward_sensitivity_bar_error.png", "mean"),
        ("q_norm", f"Post-late Q norm sensitivity at alpha={target_alpha:g}", "magma", True, "report_reward_sensitivity_q_norm.png", "mean"),
        ("diverged", f"Divergence sensitivity at alpha={target_alpha:g}", "Reds", False, "report_reward_sensitivity_divergence.png", "max"),
    ]:
        matrix: list[list[float]] = []
        for algorithm, beta in row_keys:
            values = []
            for switch_type, gamma in columns:
                matches = [
                    row
                    for row in rows
                    if _condition(row, "algorithm") == algorithm
                    and math.isclose(float(_condition(row, "beta")), float(beta))
                    and math.isclose(float(_condition(row, "gamma")), float(gamma))
                    and _condition(row, "switch_type") == switch_type
                ]
                values.append(_mean_over(matches, metric, reducer=reducer))
            matrix.append(values)
        row_labels = [f"{_short_label(algorithm)} b={float(beta):g}" for algorithm, beta in row_keys]
        outputs.append(
            _save_heatmap(
                matrix,
                row_labels,
                col_labels,
                title,
                fig_dir / name,
                cmap=cmap,
                log10=log10,
                value_format=".2f",
            )
        )
    return outputs


def plot_onpolicy_atlas(result_dir: Path) -> list[Path]:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt
    import numpy as np

    rows = _load_condition_summary(result_dir)
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    scales = ["one", "ten", "hundred", "uneven", "tabular"]
    scales = [scale for scale in scales if any(_condition(row, "scale") == scale for row in rows)]
    alphas = _sorted_unique([_condition(row, "alpha") for row in rows])
    lambdas = _sorted_unique([_condition(row, "lambda") for row in rows])
    outputs: list[Path] = []
    for metric, title, log10, name in [
        ("rmse", "TD(lambda) tail RMSE atlas", True, "report_log_rmse_atlas.png"),
        ("diverged", "TD(lambda) divergence atlas", False, "report_divergence_atlas.png"),
    ]:
        ncols = 2 if len(scales) > 1 else 1
        nrows = math.ceil(len(scales) / ncols)
        fig, axes_arr = plt.subplots(nrows, ncols, figsize=(4.8 * ncols, 3.9 * nrows))
        axes = list(axes_arr.flat) if hasattr(axes_arr, "flat") else [axes_arr]
        images = []
        for ax, scale in zip(axes, scales):
            mat = np.full((len(lambdas), len(alphas)), np.nan)
            for i, lam in enumerate(lambdas):
                for j, alpha in enumerate(alphas):
                    matches = [
                        row
                        for row in rows
                        if _condition(row, "scale") == scale
                        and math.isclose(float(_condition(row, "lambda")), float(lam))
                        and math.isclose(float(_condition(row, "alpha")), float(alpha))
                    ]
                    mat[i, j] = _mean_over(matches, metric)
            plot_mat = np.log10(np.maximum(mat, 1e-12)) if log10 else mat
            im = ax.imshow(plot_mat, aspect="auto", cmap="magma" if log10 else "Reds")
            images.append(im)
            ax.set_title(f"scale: {scale}")
            ax.set_xticks(range(len(alphas)))
            ax.set_xticklabels([f"{float(a):g}" for a in alphas], rotation=35, ha="right")
            ax.set_yticks(range(len(lambdas)))
            ax.set_yticklabels([f"{float(l):g}" for l in lambdas])
            ax.set_xlabel("alpha")
            ax.set_ylabel("lambda")
        for ax in axes[len(scales) :]:
            ax.axis("off")
        fig.suptitle(title)
        fig.colorbar(images[0], ax=axes[: len(scales)], shrink=0.8, label="log10(value)" if log10 else "value")
        fig.tight_layout()
        out = fig_dir / name
        fig.savefig(out, dpi=180)
        plt.close(fig)
        outputs.append(out)
    return outputs


def plot_unit_switching(result_dir: Path) -> list[Path]:
    rows = [
        row
        for row in _load_condition_summary(result_dir)
        if _condition(row, "recovery_window") == "post_late" and int(float(_condition(row, "phase"))) == 1
    ]
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    algorithms = [
        "discounted_sarsa",
        "reward_centered_sarsa",
        "normalized_sarsa",
        "normalized_reward_centered_sarsa",
        "normalized_differential_sarsa",
    ]
    switch_types = ["reward_shift_only", "feature_scale_only", "joint_reward_scale", "joint_reward_lognormal"]
    alphas = [alpha for alpha in _sorted_unique([_condition(row, "alpha") for row in rows]) if float(alpha) in {0.03, 0.1}]
    columns = [(switch_type, alpha) for switch_type in switch_types for alpha in alphas]
    labels = [f"{switch.replace('_', ' ')}\na={float(alpha):g}" for switch, alpha in columns]
    outputs: list[Path] = []
    for metric, title, cmap, log10, name, reducer in [
        ("avg_unshifted_reward", "Post-late reward after no-reset unit switch", "viridis", False, "report_unit_switch_reward_heatmap.png", "mean"),
        ("q_norm", "Max post-late Q norm after no-reset unit switch", "magma", True, "report_unit_switch_q_norm_heatmap.png", "max"),
        ("diverged", "Post-late divergence after no-reset unit switch", "Reds", False, "report_unit_switch_divergence_heatmap.png", "max"),
    ]:
        matrix: list[list[float]] = []
        for alg in algorithms:
            vals = []
            for switch_type, alpha in columns:
                matches = [
                    row
                    for row in rows
                    if _condition(row, "algorithm") == alg
                    and _condition(row, "switch_type") == switch_type
                    and math.isclose(float(_condition(row, "alpha")), float(alpha))
                ]
                vals.append(_mean_over(matches, metric, reducer=reducer))
            matrix.append(vals)
        outputs.append(
            _save_heatmap(
                matrix,
                [_short_label(alg) for alg in algorithms],
                labels,
                title,
                fig_dir / name,
                cmap=cmap,
                log10=log10,
                value_format=".2f",
            )
        )
    return outputs
