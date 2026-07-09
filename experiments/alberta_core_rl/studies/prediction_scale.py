from __future__ import annotations

import time

import numpy as np

from ..core import should_log_step
from ..agents import LinearTD
from ..envs import RandomWalkPrediction, TileRandomWalkPrediction


def run_random_walk_td(
    seed: int,
    steps: int,
    scale: str,
    method: str,
    alpha: float,
    lam: float = 0.0,
    representation: str = "tabular",
) -> list[dict]:
    if representation == "tile":
        env = TileRandomWalkPrediction(scale=scale, seed=seed)
    else:
        env = RandomWalkPrediction(scale=scale, seed=seed)
    agent = LinearTD(env.n_features, alpha=alpha, gamma=1.0, lam=lam, method=method, alpha_max=1.0)
    rows = []
    x = env.reset()
    true_values = env.true_values()
    eval_period = 200 if representation == "tile" and steps >= 20000 else 20 if representation == "tile" else 1
    rmse = float("nan")
    for t in range(steps):
        x_next, reward, done = env.step()
        info = agent.update(x, reward, x_next, terminal=done)
        diverged = float((not np.all(np.isfinite(agent.w))) or np.max(np.abs(agent.w)) > 1e8)
        if diverged:
            rmse = 1e6
        elif t % eval_period == 0:
            preds = env.predicted_values(agent.w)
            rmse = float(np.sqrt(np.mean((preds - true_values) ** 2)))
        if should_log_step(t, steps) or diverged:
            rows.append(
                {
                    "seed": seed,
                    "step": t,
                    "scale": scale,
                    "representation": representation,
                    "algorithm": method,
                    "alpha": alpha,
                    "lambda": lam,
                    "rmse": rmse,
                    "td_error": info.delta,
                    "step_size": info.step_size,
                    "weight_norm": info.weight_norm,
                    "prediction_change": info.prediction_change,
                    "diverged": diverged,
                    "rmse_eval_period": eval_period,
                }
            )
        if diverged:
            break
        x = env.reset() if done else x_next
    return rows


def proposal_output_controlled_td(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    scales = ["one", "ten"] if suite == "smoke" else ["one", "ten", "hundred", "uneven"]
    methods = ["fixed", "normalized"] if suite != "main" else ["fixed", "normalized", "trace_normalized", "true_online"]
    alphas = [0.1] if suite != "main" else [0.03, 0.1, 0.3]
    representation = "tile" if suite == "main" else "tabular"
    if suite == "main" and steps >= 20000:
        scales = ["one", "ten", "hundred", "uneven", "lognormal"]
        alphas = [0.01, 0.03, 0.1, 0.3]
    rows: list[dict] = []
    total = len(seeds) * len(scales) * len(methods) * len(alphas)
    condition_index = 0
    for seed in seeds:
        for scale in scales:
            for method in methods:
                for alpha in alphas:
                    condition_index += 1
                    lam = 0.8 if "trace" in method or method == "true_online" else 0.0
                    start = time.perf_counter()
                    print(
                        "[output_controlled_td] "
                        f"start {condition_index}/{total} seed={seed} scale={scale} "
                        f"method={method} alpha={alpha} lambda={lam} steps={steps}",
                        flush=True,
                    )
                    condition_rows = run_random_walk_td(
                        seed,
                        steps,
                        scale,
                        method,
                        alpha=alpha,
                        lam=lam,
                        representation=representation,
                    )
                    rows.extend(condition_rows)
                    elapsed = time.perf_counter() - start
                    tail = condition_rows[-1] if condition_rows else {}
                    print(
                        "[output_controlled_td] "
                        f"done {condition_index}/{total} seed={seed} scale={scale} "
                        f"method={method} alpha={alpha} lambda={lam} "
                        f"rows={len(condition_rows)} last_step={tail.get('step')} "
                        f"rmse={tail.get('rmse')} diverged={tail.get('diverged')} "
                        f"elapsed_sec={elapsed:.2f}",
                        flush=True,
                    )
    summary = {
        "question": "Can output-level step-size control make streaming TD robust to feature scale?",
        "main_metric": "rmse",
        "n_rows": len(rows),
    }
    return rows, summary


def proposal_output_controlled_td_fairness(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    """Audit true-online TD against output-controlled variants over the same scale/alpha grid."""
    scales = ["one", "ten"] if suite == "smoke" else ["one", "ten", "hundred", "uneven", "lognormal"]
    methods = ["fixed", "normalized", "trace_normalized", "true_online", "true_online_normalized"]
    alphas = [0.03, 0.1] if suite == "smoke" else [0.003, 0.01, 0.03, 0.1, 0.3]
    representation = "tile"
    if suite == "main" and steps >= 20000:
        alphas = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3]
    rows: list[dict] = []
    total = len(seeds) * len(scales) * len(methods) * len(alphas)
    condition_index = 0
    for seed in seeds:
        for scale in scales:
            for method in methods:
                lam = 0.8 if "trace" in method or "true_online" in method else 0.0
                for alpha in alphas:
                    condition_index += 1
                    start = time.perf_counter()
                    print(
                        "[output_controlled_td_fairness] "
                        f"start {condition_index}/{total} seed={seed} scale={scale} "
                        f"method={method} alpha={alpha} lambda={lam} steps={steps}",
                        flush=True,
                    )
                    condition_rows = run_random_walk_td(
                        seed,
                        steps,
                        scale,
                        method,
                        alpha=alpha,
                        lam=lam,
                        representation=representation,
                    )
                    for row in condition_rows:
                        row["environment"] = "tile_random_walk_true_online_fairness"
                        row["fairness_audit"] = 1.0
                    rows.extend(condition_rows)
                    elapsed = time.perf_counter() - start
                    tail = condition_rows[-1] if condition_rows else {}
                    print(
                        "[output_controlled_td_fairness] "
                        f"done {condition_index}/{total} seed={seed} scale={scale} "
                        f"method={method} alpha={alpha} lambda={lam} "
                        f"rows={len(condition_rows)} last_step={tail.get('step')} "
                        f"rmse={tail.get('rmse')} diverged={tail.get('diverged')} "
                        f"elapsed_sec={elapsed:.2f}",
                        flush=True,
                    )
    return rows, {
        "question": "Is true-online TD's apparent scale sensitivity an algorithmic issue or an unfair fixed-step-size comparison?",
        "main_metric": "rmse",
        "n_rows": len(rows),
    }
