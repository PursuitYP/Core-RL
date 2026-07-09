from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from .core import ensure_mpl_config, repo_root


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


def _short_label(value: Any) -> str:
    labels = {
        "discounted_sarsa": "disc",
        "reward_centered_sarsa": "centered",
        "differential_sarsa": "diff",
        "normalized_sarsa": "norm",
        "normalized_reward_centered_sarsa": "norm+center",
        "normalized_differential_sarsa": "norm+diff",
        "fixed": "fixed",
        "normalized": "norm",
        "trace_normalized": "trace-norm",
        "true_online": "true-online",
        "true_online_normalized": "to-norm",
        "keep_model": "keep",
        "oracle_flush": "oracle flush",
        "recency_aging": "age",
        "recency_error_gate": "age+error",
        "flush_on_change": "oracle flush",
    }
    return labels.get(str(value), _safe_label(value))


def _rows_for(rows: list[dict[str, Any]], **conditions: Any) -> list[dict[str, Any]]:
    selected = []
    for row in rows:
        ok = True
        for key, expected in conditions.items():
            actual = _condition(row, key)
            if isinstance(expected, float):
                try:
                    ok = math.isclose(float(actual), expected)
                except Exception:
                    ok = False
            else:
                ok = actual == expected
            if not ok:
                break
        if ok:
            selected.append(row)
    return selected


def _mean_over(rows: list[dict[str, Any]], metric: str, reducer: str = "mean") -> float:
    vals = []
    for row in rows:
        mean, _ = _metric(row, metric)
        if math.isfinite(mean):
            vals.append(mean)
    if not vals:
        return math.nan
    if reducer == "max":
        return max(vals)
    return sum(vals) / len(vals)


def _save_heatmap(
    matrix: list[list[float]],
    row_labels: list[str],
    col_labels: list[str],
    title: str,
    out: Path,
    *,
    cmap: str = "viridis",
    value_format: str = ".2f",
    log10: bool = False,
) -> Path:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt
    import numpy as np

    raw = np.asarray(matrix, dtype=float)
    data = np.log10(np.maximum(raw, 1e-12)) if log10 else raw
    data = np.ma.masked_invalid(data)
    fig_w = max(7.0, 0.72 * len(col_labels) + 2.6)
    fig_h = max(3.6, 0.52 * len(row_labels) + 1.8)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    cmap_obj = plt.get_cmap(cmap).copy()
    cmap_obj.set_bad("#e8e8e8")
    im = ax.imshow(data, aspect="auto", cmap=cmap_obj)
    ax.set_title(title)
    ax.set_xticks(range(len(col_labels)))
    ax.set_xticklabels(col_labels, rotation=35, ha="right")
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels)
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            value = raw[i, j]
            if not math.isfinite(float(value)):
                text = "n/a"
                color = "black"
            elif log10:
                text = f"{value:.1e}"
                color = "white"
            else:
                text = format(float(value), value_format)
                color = "white"
            ax.text(j, i, text, ha="center", va="center", fontsize=7, color=color)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("log10(value)" if log10 else "value")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


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
        ncols = 2 if len(present_scales) > 1 else 1
        nrows = math.ceil(len(present_scales) / ncols)
        fig, axes_arr = plt.subplots(nrows, ncols, figsize=(5.0 * ncols, 3.9 * nrows), sharey=not log_y)
        axes = list(axes_arr.flat) if hasattr(axes_arr, "flat") else [axes_arr]
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
                    ax.errorbar(xs, ys, yerr=es, marker="o", linewidth=1.6, capsize=2.5, label=_short_label(alg))
            ax.set_title(f"scale: {scale}")
            ax.set_xlabel("reward shift")
            ax.grid(True, alpha=0.25)
            if log_y:
                ax.set_yscale("symlog", linthresh=1e-2)
        for ax in axes[len(present_scales) :]:
            ax.axis("off")
        axes[0].set_ylabel(ylabel)
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=8, frameon=False)
        fig.tight_layout(rect=(0.0, 0.09, 1.0, 1.0))
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
        fig, ax = plt.subplots(figsize=(8.4, 4.8))
        for mode in modes:
            half_lives = _sorted_unique(
                [
                    _condition(row, "half_life")
                    for row in rows
                    if _condition(row, "model_mode") == mode and float(_condition(row, "half_life") or 0.0) > 0.0
                ]
            )
            if not half_lives:
                half_lives = [0.0]
            for half_life in half_lives:
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
                            and math.isclose(float(_condition(row, "half_life") or 0.0), float(half_life))
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
                    suffix = "" if float(half_life) == 0.0 else f" h={int(float(half_life))}"
                    ax.errorbar(
                        xs,
                        ys,
                        yerr=es,
                        marker="o",
                        linewidth=1.6,
                        capsize=3,
                        label=f"{_short_label(mode)}{suffix}",
                    )
        ax.set_xlabel("planning backups per real step")
        ax.set_ylabel(ylabel)
        ax.set_xticks([float(b) for b in budgets])
        ax.grid(True, alpha=0.25)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, fontsize=7.5, frameon=False)
        fig.tight_layout(rect=(0.0, 0.13, 1.0, 1.0))
        out = fig_dir / f"report_{metric}_post_late_by_budget.png"
        fig.savefig(out, dpi=180)
        plt.close(fig)
        outputs.append(out)
    heatmap_metrics = [
        ("avg_reward", "Late reward by freshness rule and planning budget", "viridis", False, "report_dyna_aging_reward_heatmap.png"),
        ("stale_backup_rate", "Late stale-backup rate by freshness rule and planning budget", "Reds", False, "report_dyna_aging_stale_heatmap.png"),
        ("mean_model_error", "Late model error by freshness rule and planning budget", "magma", True, "report_dyna_aging_model_error_heatmap.png"),
    ]
    row_keys: list[tuple[str, float]] = []
    for mode in modes:
        half_lives = _sorted_unique(
            [
                _condition(row, "half_life")
                for row in rows
                if _condition(row, "model_mode") == mode and float(_condition(row, "half_life") or 0.0) > 0.0
            ]
        )
        if half_lives:
            row_keys.extend((mode, float(half_life)) for half_life in half_lives)
        elif any(_condition(row, "model_mode") == mode for row in rows):
            row_keys.append((mode, 0.0))
    row_labels = [
        f"{_short_label(mode)} h={int(half_life)}" if half_life > 0.0 else _short_label(mode)
        for mode, half_life in row_keys
    ]
    col_labels = [f"{int(float(budget))} backups" for budget in budgets]
    for metric, title, cmap, log10, name in heatmap_metrics:
        matrix: list[list[float]] = []
        for mode, half_life in row_keys:
            values = []
            for budget in budgets:
                matches = [
                    row
                    for row in rows
                    if int(float(_condition(row, "planning_steps"))) == int(float(budget))
                    and _condition(row, "model_mode") == mode
                    and math.isclose(float(_condition(row, "half_life") or 0.0), half_life)
                ]
                values.append(_mean_over(matches, metric))
            matrix.append(values)
        outputs.append(
            _save_heatmap(
                matrix,
                row_labels,
                col_labels,
                title,
                fig_dir / name,
                cmap=cmap,
                value_format=".2f",
                log10=log10,
            )
        )
    return outputs


def plot_dyna_drift(result_dir: Path) -> list[Path]:
    all_rows = _load_condition_summary(result_dir)
    rows = [
        row
        for row in all_rows
        if _condition(row, "recovery_window") == "post_late"
    ]
    if not rows:
        rows = all_rows
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    drift_modes = ["abrupt", "gradual", "stochastic"]
    drift_modes = [mode for mode in drift_modes if any(_condition(row, "drift_mode") == mode for row in rows)]
    budgets = _sorted_unique([_condition(row, "planning_steps") for row in rows])
    columns = [(mode, budget) for mode in drift_modes for budget in budgets]
    col_labels = [f"{mode}\n{int(float(budget))} backups" for mode, budget in columns]
    row_keys: list[tuple[str, float]] = []
    for mode in ["keep_model", "oracle_flush", "recency_aging", "recency_error_gate"]:
        half_lives = _sorted_unique(
            [
                _condition(row, "half_life")
                for row in rows
                if _condition(row, "model_mode") == mode and float(_condition(row, "half_life") or 0.0) > 0.0
            ]
        )
        if half_lives:
            row_keys.extend((mode, float(half_life)) for half_life in half_lives)
        elif any(_condition(row, "model_mode") == mode for row in rows):
            row_keys.append((mode, 0.0))
    outputs: list[Path] = []
    for metric, title, cmap, log10, name, reducer in [
        ("avg_reward", "Post-late reward under drift modes", "viridis", False, "report_drift_reward_heatmap.png", "mean"),
        ("stale_backup_rate", "Post-late stale-backup rate under drift modes", "Reds", False, "report_drift_stale_heatmap.png", "mean"),
        ("mean_model_error", "Post-late model error under drift modes", "magma", True, "report_drift_model_error_heatmap.png", "mean"),
    ]:
        matrix: list[list[float]] = []
        for model_mode, half_life in row_keys:
            values = []
            for drift_mode, budget in columns:
                matches = [
                    row
                    for row in rows
                    if _condition(row, "drift_mode") == drift_mode
                    and int(float(_condition(row, "planning_steps"))) == int(float(budget))
                    and _condition(row, "model_mode") == model_mode
                    and math.isclose(float(_condition(row, "half_life") or 0.0), half_life)
                ]
                values.append(_mean_over(matches, metric, reducer=reducer))
            matrix.append(values)
        row_labels = [
            f"{_short_label(model_mode)} h={int(half_life)}" if half_life > 0.0 else _short_label(model_mode)
            for model_mode, half_life in row_keys
        ]
        outputs.append(
            _save_heatmap(
                matrix,
                row_labels,
                col_labels,
                title,
                fig_dir / name,
                cmap=cmap,
                value_format=".2f",
                log10=log10,
            )
        )
    return outputs


def plot_dyna_budget(result_dir: Path) -> list[Path]:
    ensure_mpl_config(repo_root())
    import matplotlib.pyplot as plt

    rows = [
        row
        for row in _load_condition_summary(result_dir)
        if _condition(row, "recovery_window") == "post_late" and int(float(_condition(row, "phase"))) == 1
    ]
    budgets = _sorted_unique([_condition(row, "planning_steps") for row in rows])
    modes = _sorted_unique([_condition(row, "model_mode") for row in rows])
    metrics = [
        ("avg_reward", "Late average reward"),
        ("stale_backup_rate", "Late stale-backup rate"),
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
                matches = _rows_for(rows, planning_steps=budget, model_mode=mode)
                if not matches:
                    continue
                mean, ci95 = _metric(matches[0], metric)
                xs.append(float(budget))
                ys.append(mean)
                es.append(0.0 if not math.isfinite(ci95) else ci95)
            if xs:
                ax.errorbar(xs, ys, yerr=es, marker="o", linewidth=1.8, capsize=3, label=_short_label(mode))
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
