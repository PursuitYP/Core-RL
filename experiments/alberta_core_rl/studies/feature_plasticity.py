from __future__ import annotations

import numpy as np

from ..agents import ActionValueBandit, GradientBandit, LinearTD, TIDBDLite
from ..core import recovery_window
from ..envs import DriftingBandit, NonStationarySensorStream, TraceConditioningStream


def trace_features(x: np.ndarray, traces: np.ndarray, rhos: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    traces = rhos * traces + x[0]
    return np.concatenate([x, traces]), traces


def proposal_generate_test(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    if suite == "main":
        modes = ["fixed_tight", "oracle_bank", "random_replace", "generate_test"]
        base_rhos = {
            "fixed_tight": np.array([0.2, 0.45, 0.7, 0.88]),
            "oracle_bank": np.array([0.82, 0.9, 0.95, 0.975]),
            "random_replace": np.array([0.2, 0.45, 0.7, 0.88]),
            "generate_test": np.array([0.2, 0.45, 0.7, 0.88]),
        }
        replace_period = 250
    else:
        modes = ["fixed_traces", "generate_test"] if suite != "smoke" else ["generate_test"]
        base_rhos = {mode: np.linspace(0.2, 0.98, 16) for mode in modes}
        replace_period = 500
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for mode in modes:
            switch_step = steps // 2
            stream = TraceConditioningStream(switch_step=switch_step)
            rhos = base_rhos[mode].copy()
            traces = np.zeros(len(rhos))
            agent = LinearTD(n_features=2 + len(rhos), alpha=0.05, gamma=0.95, method="normalized")
            utilities = np.ones(len(rhos)) * 1e-3
            for t in range(steps):
                current_delay = stream.delay()
                x, reward, x_next_base = stream.step()
                phi, traces = trace_features(x, traces, rhos)
                phi_next, _ = trace_features(x_next_base, traces.copy(), rhos)
                info = agent.update(phi, reward, phi_next)
                utilities = 0.99 * utilities + 0.01 * np.abs(agent.w[2:]) * np.abs(traces)
                replaced = 0
                if mode in {"generate_test", "random_replace"} and t > 0 and t % replace_period == 0:
                    low = np.argsort(utilities)[: max(1, len(rhos) // 8)]
                    if mode == "random_replace":
                        low = rng.choice(len(rhos), size=len(low), replace=False)
                    rhos[low] = rng.uniform(0.05, 0.995, size=len(low))
                    traces[low] = 0.0
                    agent.w[2:][low] = 0.0
                    utilities[low] = np.median(utilities)
                    replaced = len(low)
                target_rho = float(np.exp(-1.0 / max(1, current_delay)))
                closest_rho_distance = float(np.min(np.abs(rhos - target_rho)))
                top_idx = int(np.argmax(utilities))
                rows.append(
                    {
                        "seed": seed,
                        "step": t,
                        "algorithm": mode,
                        "phase": int(t >= switch_step),
                        "steps_since_switch": t - switch_step,
                        "recovery_window": recovery_window(t, switch_step),
                        "delay": current_delay,
                        "feature_budget": len(rhos),
                        "reward": reward,
                        "td_error": info.delta,
                        "abs_error": abs(info.delta),
                        "weight_norm": info.weight_norm,
                        "replacement_count": replaced,
                        "mean_rho": float(np.mean(rhos)),
                        "target_rho": target_rho,
                        "closest_rho_distance": closest_rho_distance,
                        "max_utility_rho": float(rhos[top_idx]),
                        "max_utility": float(utilities[top_idx]),
                    }
                )
    return rows, {"question": "Can generate-and-test traces preserve online prediction plasticity?", "n_rows": len(rows)}


def proposal_streaming_representation(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    algs = ["value_only", "aux_next_feature"] if suite != "smoke" else ["aux_next_feature"]
    for seed in seeds:
        for alg in algs:
            stream = NonStationarySensorStream(seed=seed, switch_step=steps // 2)
            value_agent = LinearTD(stream.n_features, alpha=0.03, gamma=0.9, method="normalized")
            aux_w = np.zeros((stream.n_features, stream.n_features))
            for t in range(steps):
                phase = stream.phase()
                x, reward, x_next = stream.step()
                shaped_reward = reward
                aux_error = 0.0
                if alg == "aux_next_feature":
                    pred = aux_w @ x
                    err = x_next - pred
                    aux_w += 0.01 * np.outer(err, x) / (1e-8 + np.dot(x, x))
                    aux_error = float(np.mean(err**2))
                    shaped_reward = reward + 0.01 * float(np.dot(err, err))
                info = value_agent.update(x, shaped_reward, x_next)
                rows.append(
                    {
                        "seed": seed,
                        "step": t,
                        "algorithm": alg,
                        "phase": phase,
                        "reward": reward,
                        "td_error": info.delta,
                        "abs_td_error": abs(info.delta),
                        "aux_mse": aux_error,
                        "weight_norm": info.weight_norm,
                    }
                )
    return rows, {"question": "Can small auxiliary predictions improve streaming representation?", "n_rows": len(rows)}


def proposal_nonstationary_bandit(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    algs = ["sample_average", "constant_alpha", "gradient_no_baseline", "gradient_baseline"]
    for seed in seeds:
        for alg in algs:
            env = DriftingBandit(seed=seed, switch_period=max(200, steps // 4))
            if alg == "sample_average":
                agent = ActionValueBandit(env.n_actions, alpha=None, seed=seed)
            elif alg == "constant_alpha":
                agent = ActionValueBandit(env.n_actions, alpha=0.1, seed=seed)
            elif alg == "gradient_no_baseline":
                agent = GradientBandit(env.n_actions, alpha=0.1, use_baseline=False, seed=seed)
            else:
                agent = GradientBandit(env.n_actions, alpha=0.1, use_baseline=True, seed=seed)
            best_count = 0.0
            regret = 0.0
            for t in range(steps):
                action = agent.action()
                reward, best = env.step(action, reward_shift=5.0 if t >= steps // 2 else 0.0)
                agent.update(action, reward)
                best_count += 0.01 * ((1.0 if action == best else 0.0) - best_count)
                regret += float(env.q[best] - env.q[action])
                rows.append(
                    {
                        "seed": seed,
                        "step": t,
                        "algorithm": alg,
                        "reward": reward,
                        "best_action": best,
                        "chosen_action": action,
                        "best_action_rate": best_count,
                        "cumulative_regret": regret,
                    }
                )
    return rows, {"question": "Which simple online bandit update preserves plasticity?", "n_rows": len(rows)}


def proposal_tidbd_plasticity(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    algs = (
        ["fixed_td_0.01", "fixed_td_0.03", "fixed_td_0.1", "normalized_td", "tidbd_lite"]
        if suite == "main"
        else ["fixed_td", "normalized_td", "tidbd_lite"]
    )
    for seed in seeds:
        for alg in algs:
            switch_step = steps // 2
            stream = NonStationarySensorStream(n_features=40 if suite == "main" else 20, seed=seed, switch_step=switch_step)
            if alg == "tidbd_lite":
                agent = TIDBDLite(stream.n_features, theta=0.01, beta0=-5.0, gamma=0.9)
            else:
                method = "normalized" if alg == "normalized_td" else "fixed"
                alpha = 0.03
                if alg.startswith("fixed_td_"):
                    alpha = float(alg.rsplit("_", 1)[1])
                agent = LinearTD(stream.n_features, alpha=alpha, gamma=0.9, method=method)
            for t in range(steps):
                phase = stream.phase()
                x, reward, x_next = stream.step()
                info = agent.update(x, reward, x_next)
                feature_stepsize = np.nan
                old_feature_stepsize = info.step_size
                new_feature_stepsize = info.step_size
                distractor_feature_stepsize = info.step_size
                if isinstance(agent, TIDBDLite):
                    alphas = np.exp(np.clip(agent.beta, -12.0, 2.0))
                    feature_stepsize = float(np.mean(alphas[:10]))
                    old_feature_stepsize = float(np.mean(alphas[:5]))
                    new_feature_stepsize = float(np.mean(alphas[5:10]))
                    distractor_feature_stepsize = float(np.mean(alphas[10:]))
                rows.append(
                    {
                        "seed": seed,
                        "step": t,
                        "algorithm": alg,
                        "phase": phase,
                        "steps_since_switch": t - switch_step,
                        "recovery_window": recovery_window(t, switch_step),
                        "reward": reward,
                        "abs_td_error": abs(info.delta),
                        "td_error": info.delta,
                        "step_size": info.step_size,
                        "mean_feature_step_size": feature_stepsize,
                        "old_feature_step_size": old_feature_stepsize,
                        "new_feature_step_size": new_feature_stepsize,
                        "distractor_feature_step_size": distractor_feature_stepsize,
                        "weight_norm": info.weight_norm,
                    }
                )
    return rows, {"question": "Can per-feature step-size adaptation track changing feature relevance?", "n_rows": len(rows)}
