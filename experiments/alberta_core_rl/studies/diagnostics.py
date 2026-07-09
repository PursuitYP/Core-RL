from __future__ import annotations

import numpy as np

from ..agents import LinearTD
from ..envs import TmazeCue, TwoLoopMDP
from .prediction_scale import run_random_walk_td


def proposal_centered_td_diagnostics(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    algs = ["ordinary_td", "reward_centered_td", "bellman_error_centered"]
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for shift in ([0.0, 5.0] if suite == "smoke" else [-5.0, 0.0, 5.0]):
            for alg in algs:
                env = TwoLoopMDP(reward_shift=shift)
                env.reset()
                agent = LinearTD(env.n_states, alpha=0.05, gamma=0.99, method="fixed")
                reward_bar = 0.0
                delta_bar = 0.0
                for t in range(steps):
                    x = env.features()
                    action = int(rng.integers(env.n_actions))
                    _, reward = env.step(action)
                    unshifted_reward = reward - shift
                    x_next = env.features()
                    used_reward = reward
                    if alg == "reward_centered_td":
                        used_reward = reward - reward_bar
                    info = agent.update(x, used_reward, x_next)
                    if alg == "bellman_error_centered":
                        agent.w -= 0.01 * delta_bar * x
                    reward_bar += 0.01 * (reward - reward_bar)
                    delta_bar += 0.01 * (info.delta - delta_bar)
                    rows.append(
                        {
                            "seed": seed,
                            "step": t,
                            "algorithm": alg,
                            "reward_shift": shift,
                            "reward": reward,
                            "unshifted_reward": unshifted_reward,
                            "reward_bar": reward_bar,
                            "delta_bar": delta_bar,
                            "td_error": info.delta,
                            "value_norm": info.weight_norm,
                        }
                    )
    return rows, {"question": "What offset does each centering method remove?", "n_rows": len(rows)}


def proposal_stability_atlas(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    alphas = [0.01, 0.05, 0.1] if suite != "main" else [0.001, 0.01, 0.05, 0.1, 0.2]
    lams = [0.0, 0.8] if suite != "main" else [0.0, 0.5, 0.8, 0.95]
    for seed in seeds:
        for scale in ["one", "ten", "uneven"]:
            for alpha in alphas:
                for lam in lams:
                    rows.extend(run_random_walk_td(seed, steps, scale, "fixed", alpha=alpha, lam=lam))
    for row in rows:
        row["algorithm"] = "td_lambda_stability"
        row["diverged"] = float(not np.isfinite(row["rmse"]) or row["weight_norm"] > 1e6)
    return rows, {"question": "How do alpha, lambda, and representation scale shape on-policy TD stability?", "n_rows": len(rows)}


def proposal_gvf_question_design(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    discounts = [0.0, 0.5, 0.9, 0.98]
    cumulants = ["left_cue", "right_cue", "junction", "bias"]
    for seed in seeds:
        env = TmazeCue(seed=seed)
        raw = env.reset()
        learners = {(c, g): LinearTD(env.n_raw_features, alpha=0.05, gamma=g, method="normalized") for c in cumulants for g in discounts}
        for t in range(steps):
            action = int(env.rng.integers(2))
            raw_next, reward, info_env = env.step(action)
            c_next = env.cumulants()
            for (c, gamma), learner in learners.items():
                info = learner.update(raw, c_next[c], raw_next)
                rows.append(
                    {
                        "seed": seed,
                        "step": t,
                        "cumulant": c,
                        "gamma": gamma,
                        "reward": reward,
                        "trial_end": info_env["trial_end"],
                        "prediction": learner.value(raw),
                        "abs_td_error": abs(info.delta),
                        "weight_norm": info.weight_norm,
                    }
                )
            raw = raw_next
    return rows, {"question": "Which GVF questions are accurate and which are useful?", "n_rows": len(rows)}

