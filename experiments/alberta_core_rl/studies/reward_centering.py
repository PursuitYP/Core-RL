from __future__ import annotations

import numpy as np

from ..core import recovery_window, should_log_step
from ..agents import LinearSarsa
from ..envs import AccessControlQueue, TwoLoopMDP


def _scale_vector(n_features: int, scale: str) -> np.ndarray:
    if scale == "one":
        return np.ones(n_features)
    if scale == "ten":
        return np.ones(n_features) * 10.0
    if scale == "hundred":
        return np.ones(n_features) * 100.0
    if scale == "uneven":
        return np.geomspace(0.1, 10.0, n_features)
    if scale == "lognormal":
        grid = np.linspace(-1.5, 1.5, n_features)
        return np.exp(grid)
    raise ValueError(f"unknown feature scale: {scale}")


def _scaled_access_features(env: AccessControlQueue, scales: np.ndarray) -> np.ndarray:
    return env.features() * scales


def proposal_reward_centered_sarsa(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    shifts = [0.0, 10.0] if suite == "smoke" else [-5.0, 0.0, 5.0, 10.0]
    alphas = [0.05]
    algs = [
        ("discounted_sarsa", dict(centered=False, differential=False, gamma=0.99)),
        ("reward_centered_sarsa", dict(centered=True, differential=False, gamma=0.99)),
        ("differential_sarsa", dict(centered=False, differential=True, gamma=1.0)),
    ]
    rows: list[dict] = []
    if suite == "main":
        shifts = [-4.0, 0.0, 4.0, 8.0]
        if steps >= 20000:
            shifts = [-8.0, -4.0, 0.0, 4.0, 8.0]
            alphas = [0.02, 0.05, 0.1]
        for seed in seeds:
            rng = np.random.default_rng(seed)
            for shift in shifts:
                for alpha in alphas:
                    for name, kwargs in algs:
                        env = AccessControlQueue(reward_shift=shift, seed=seed)
                        env.reset()
                        x = env.features()
                        agent = LinearSarsa(env.n_states, env.n_actions, alpha=alpha, epsilon=0.1, beta=0.01, **kwargs)
                        a = agent.choose_action(rng, x)
                        avg_reward = 0.0
                        avg_unshifted_reward = 0.0
                        accept_rate = 0.0
                        diverged = 0.0
                        for t in range(steps):
                            _, reward, env_info = env.step(a)
                            unshifted_reward = reward - shift
                            x_next = env.features()
                            a_next = agent.choose_action(rng, x_next)
                            info = agent.update(x, a, reward, x_next, a_next)
                            q_norm = info.weight_norm
                            if (not np.isfinite(q_norm)) or q_norm > 1e8:
                                diverged = 1.0
                                q_norm = min(float(q_norm) if np.isfinite(q_norm) else 1e9, 1e9)
                            avg_reward += 0.005 * (reward - avg_reward)
                            avg_unshifted_reward += 0.005 * (unshifted_reward - avg_unshifted_reward)
                            accept_rate += 0.005 * (env_info["accepted"] - accept_rate)
                            high_accept = env_info["accepted"] if env_info["high_priority"] else np.nan
                            high_state = env.n_servers * len(env.priorities) + len(env.priorities) - 1
                            if should_log_step(t, steps) or diverged:
                                rows.append(
                                    {
                                        "seed": seed,
                                        "step": t,
                                        "environment": "access_control",
                                        "reward_shift": shift,
                                        "algorithm": name,
                                        "alpha": alpha,
                                        "reward": reward,
                                        "unshifted_reward": unshifted_reward,
                                        "avg_reward": avg_reward,
                                        "avg_unshifted_reward": avg_unshifted_reward,
                                        "accepted": env_info["accepted"],
                                        "accept_rate": accept_rate,
                                        "high_priority_accept": high_accept,
                                        "free_servers": env_info["free_servers"],
                                        "reward_bar": agent.reward_bar,
                                        "td_error": info.delta,
                                        "q_norm": q_norm,
                                        "diverged": diverged,
                                        "policy_accept_when_full": int(np.argmax(agent.q_values(np.eye(env.n_states)[0]))),
                                        "policy_accept_high_free": int(np.argmax(agent.q_values(np.eye(env.n_states)[high_state]))),
                                    }
                                )
                            if diverged:
                                break
                            x, a = x_next, a_next
        return rows, {
            "question": "Does reward centering improve reward-shift invariance in continuing access-control Sarsa?",
            "n_rows": len(rows),
        }
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for shift in shifts:
            for name, kwargs in algs:
                env = TwoLoopMDP(reward_shift=shift)
                s = env.reset()
                x = env.features()
                agent = LinearSarsa(env.n_states, env.n_actions, alpha=0.08, epsilon=0.1, beta=0.01, **kwargs)
                a = agent.choose_action(rng, x)
                avg_reward = 0.0
                avg_unshifted_reward = 0.0
                for t in range(steps):
                    _, reward = env.step(a)
                    unshifted_reward = reward - shift
                    x_next = env.features()
                    a_next = agent.choose_action(rng, x_next)
                    info = agent.update(x, a, reward, x_next, a_next)
                    avg_reward += 0.01 * (reward - avg_reward)
                    avg_unshifted_reward += 0.01 * (unshifted_reward - avg_unshifted_reward)
                    if should_log_step(t, steps):
                        rows.append(
                            {
                                "seed": seed,
                                "step": t,
                                "reward_shift": shift,
                                "algorithm": name,
                                "state": s,
                                "action": a,
                                "reward": reward,
                                "unshifted_reward": unshifted_reward,
                                "avg_reward": avg_reward,
                                "avg_unshifted_reward": avg_unshifted_reward,
                                "reward_bar": agent.reward_bar,
                                "td_error": info.delta,
                                "q_norm": info.weight_norm,
                                "policy_action_at_decision": int(np.argmax(agent.q_values(np.eye(env.n_states)[0]))),
                            }
                        )
                    s, x, a = env.state, x_next, a_next
    return rows, {"question": "Does reward centering remove reward-shift sensitivity in continuing Sarsa?", "n_rows": len(rows)}


def proposal_scale_invariant_control(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    """Cross reward-shift and feature-scale invariance in continuing Sarsa control."""
    rows: list[dict] = []
    shifts = [0.0, 8.0] if suite == "smoke" else [-4.0, 0.0, 8.0]
    scales = ["one", "ten"] if suite == "smoke" else ["one", "ten", "hundred", "uneven"]
    alphas = [0.05] if suite == "smoke" else [0.03]
    if suite == "main" and steps >= 20000:
        shifts = [-8.0, -4.0, 0.0, 4.0, 8.0]
        scales = ["one", "ten", "hundred", "uneven", "lognormal"]
        alphas = [0.01, 0.03, 0.1]
    algs = [
        ("discounted_sarsa", dict(centered=False, differential=False, method="fixed", gamma=0.99)),
        ("reward_centered_sarsa", dict(centered=True, differential=False, method="fixed", gamma=0.99)),
        ("normalized_sarsa", dict(centered=False, differential=False, method="normalized", gamma=0.99)),
        (
            "normalized_reward_centered_sarsa",
            dict(centered=True, differential=False, method="normalized", gamma=0.99),
        ),
        ("normalized_differential_sarsa", dict(centered=False, differential=True, method="normalized", gamma=1.0)),
    ]
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for shift in shifts:
            for scale in scales:
                for alpha in alphas:
                    for name, kwargs in algs:
                        env = AccessControlQueue(reward_shift=shift, seed=seed)
                        env.reset()
                        feature_scales = _scale_vector(env.n_states, scale)
                        x = _scaled_access_features(env, feature_scales)
                        agent = LinearSarsa(
                            env.n_states,
                            env.n_actions,
                            alpha=alpha,
                            epsilon=0.1,
                            beta=0.01,
                            alpha_max=1.0,
                            **kwargs,
                        )
                        a = agent.choose_action(rng, x)
                        avg_unshifted_reward = 0.0
                        accept_rate = 0.0
                        diverged = 0.0
                        high_state = env.n_servers * len(env.priorities) + len(env.priorities) - 1
                        full_state = 0
                        for t in range(steps):
                            _, reward, env_info = env.step(a)
                            unshifted_reward = reward - shift
                            x_next = _scaled_access_features(env, feature_scales)
                            a_next = agent.choose_action(rng, x_next)
                            info = agent.update(x, a, reward, x_next, a_next)
                            q_norm = info.weight_norm
                            if (not np.isfinite(q_norm)) or q_norm > 1e8:
                                diverged = 1.0
                                q_norm = min(float(q_norm) if np.isfinite(q_norm) else 1e9, 1e9)
                            avg_unshifted_reward += 0.005 * (unshifted_reward - avg_unshifted_reward)
                            accept_rate += 0.005 * (env_info["accepted"] - accept_rate)
                            high_x = np.eye(env.n_states)[high_state] * feature_scales
                            full_x = np.eye(env.n_states)[full_state] * feature_scales
                            if should_log_step(t, steps) or diverged:
                                rows.append(
                                    {
                                        "seed": seed,
                                        "step": t,
                                        "environment": "access_control_scaled",
                                        "reward_shift": shift,
                                        "scale": scale,
                                        "algorithm": name,
                                        "alpha": alpha,
                                        "reward": reward,
                                        "unshifted_reward": unshifted_reward,
                                        "avg_unshifted_reward": avg_unshifted_reward,
                                        "accepted": env_info["accepted"],
                                        "accept_rate": accept_rate,
                                        "reward_bar": agent.reward_bar,
                                        "td_error": info.delta,
                                        "step_size": info.step_size,
                                        "prediction_change": info.prediction_change,
                                        "q_norm": q_norm,
                                        "diverged": diverged,
                                        "policy_accept_when_full": int(np.argmax(agent.q_values(full_x))),
                                        "policy_accept_high_free": int(np.argmax(agent.q_values(high_x))),
                                    }
                                )
                            if diverged:
                                break
                            x, a = x_next, a_next
    return rows, {
        "question": "Do reward centering and output-controlled Sarsa compose into reward/feature-scale invariance?",
        "n_rows": len(rows),
    }


def proposal_unit_switching_control(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    """Single-stream unit-change stress test for continuing control."""
    rows: list[dict] = []
    schedules = [
        ("reward_shift_only", 0.0, 8.0, "one", "one"),
        ("feature_scale_only", 0.0, 0.0, "one", "hundred"),
        ("joint_reward_scale", 0.0, 8.0, "one", "hundred"),
        ("joint_reward_lognormal", 0.0, -4.0, "one", "lognormal"),
    ]
    if suite == "smoke":
        schedules = schedules[:2]
    algs = [
        ("discounted_sarsa", dict(centered=False, differential=False, method="fixed", gamma=0.99)),
        ("reward_centered_sarsa", dict(centered=True, differential=False, method="fixed", gamma=0.99)),
        ("normalized_sarsa", dict(centered=False, differential=False, method="normalized", gamma=0.99)),
        (
            "normalized_reward_centered_sarsa",
            dict(centered=True, differential=False, method="normalized", gamma=0.99),
        ),
        ("normalized_differential_sarsa", dict(centered=False, differential=True, method="normalized", gamma=1.0)),
    ]
    alphas = [0.03] if suite != "main" or steps < 20000 else [0.01, 0.03, 0.1]
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for switch_type, pre_shift, post_shift, pre_scale, post_scale in schedules:
            for alpha in alphas:
                for name, kwargs in algs:
                    env = AccessControlQueue(reward_shift=pre_shift, seed=seed)
                    env.reset()
                    switch_step = steps // 2
                    feature_scales = _scale_vector(env.n_states, pre_scale)
                    x = _scaled_access_features(env, feature_scales)
                    agent = LinearSarsa(
                        env.n_states,
                        env.n_actions,
                        alpha=alpha,
                        epsilon=0.1,
                        beta=0.01,
                        alpha_max=1.0,
                        **kwargs,
                    )
                    action = agent.choose_action(rng, x)
                    avg_unshifted_reward = 0.0
                    accept_rate = 0.0
                    diverged = 0.0
                    for t in range(steps):
                        phase = 0 if t < switch_step else 1
                        env.reward_shift = pre_shift if phase == 0 else post_shift
                        scale_name = pre_scale if phase == 0 else post_scale
                        feature_scales = _scale_vector(env.n_states, scale_name)
                        _, reward, env_info = env.step(action)
                        unshifted_reward = reward - env.reward_shift
                        x_next = _scaled_access_features(env, feature_scales)
                        action_next = agent.choose_action(rng, x_next)
                        info = agent.update(x, action, reward, x_next, action_next)
                        q_norm = info.weight_norm
                        if (not np.isfinite(q_norm)) or q_norm > 1e8:
                            diverged = 1.0
                            q_norm = min(float(q_norm) if np.isfinite(q_norm) else 1e9, 1e9)
                        avg_unshifted_reward += 0.005 * (unshifted_reward - avg_unshifted_reward)
                        accept_rate += 0.005 * (env_info["accepted"] - accept_rate)
                        if should_log_step(t, steps) or t in {switch_step - 1, switch_step, switch_step + 1} or diverged:
                            rows.append(
                                {
                                    "seed": seed,
                                    "step": t,
                                    "environment": "access_control_unit_switch",
                                    "switch_type": switch_type,
                                    "phase": phase,
                                    "steps_since_switch": t - switch_step,
                                    "recovery_window": recovery_window(t, switch_step),
                                    "reward_shift": env.reward_shift,
                                    "scale": scale_name,
                                    "algorithm": name,
                                    "alpha": alpha,
                                    "reward": reward,
                                    "unshifted_reward": unshifted_reward,
                                    "avg_unshifted_reward": avg_unshifted_reward,
                                    "accepted": env_info["accepted"],
                                    "accept_rate": accept_rate,
                                    "reward_bar": agent.reward_bar,
                                    "td_error": info.delta,
                                    "step_size": info.step_size,
                                    "prediction_change": info.prediction_change,
                                    "q_norm": q_norm,
                                    "diverged": diverged,
                                }
                            )
                        if diverged:
                            break
                        x, action = x_next, action_next
    return rows, {
        "question": "Can a continuing Sarsa agent recover when reward origin or feature scale changes inside one stream?",
        "n_rows": len(rows),
    }


def proposal_reward_centered_sarsa_sensitivity(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    """No-reset reward-origin switch with beta/gamma sensitivity for centered Sarsa."""
    rows: list[dict] = []
    schedules = [("up_shift", 0.0, 8.0), ("down_shift", 8.0, 0.0)] if suite != "smoke" else [("up_shift", 0.0, 8.0)]
    alphas = [0.03] if suite == "smoke" else [0.02, 0.05]
    betas = [0.003, 0.01, 0.03] if suite != "smoke" else [0.01]
    gammas = [0.9, 0.99] if suite != "smoke" else [0.99]
    if suite == "main" and steps >= 20000:
        schedules = [("up_shift", 0.0, 8.0), ("down_shift", 8.0, 0.0), ("sign_shift", -4.0, 8.0)]
        alphas = [0.02, 0.05, 0.1]
        betas = [0.001, 0.003, 0.01, 0.03, 0.1]
        gammas = [0.9, 0.97, 0.99]
    algs = [
        ("discounted_sarsa", dict(centered=False, differential=False)),
        ("reward_centered_sarsa", dict(centered=True, differential=False)),
        ("differential_sarsa", dict(centered=False, differential=True)),
    ]
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for switch_type, pre_shift, post_shift in schedules:
            for alpha in alphas:
                for gamma in gammas:
                    for beta in betas:
                        for name, kwargs in algs:
                            env = AccessControlQueue(reward_shift=pre_shift, seed=seed)
                            env.reset()
                            x = env.features()
                            agent_gamma = 1.0 if name == "differential_sarsa" else gamma
                            agent = LinearSarsa(
                                env.n_states,
                                env.n_actions,
                                alpha=alpha,
                                gamma=agent_gamma,
                                epsilon=0.1,
                                beta=beta,
                                **kwargs,
                            )
                            action = agent.choose_action(rng, x)
                            switch_step = steps // 2
                            avg_unshifted_reward = 0.0
                            accept_rate = 0.0
                            reward_bar_error = 0.0
                            diverged = 0.0
                            for t in range(steps):
                                phase = 0 if t < switch_step else 1
                                env.reward_shift = pre_shift if phase == 0 else post_shift
                                _, reward, env_info = env.step(action)
                                unshifted_reward = reward - env.reward_shift
                                x_next = env.features()
                                action_next = agent.choose_action(rng, x_next)
                                info = agent.update(x, action, reward, x_next, action_next)
                                q_norm = info.weight_norm
                                if (not np.isfinite(q_norm)) or q_norm > 1e8:
                                    diverged = 1.0
                                    q_norm = min(float(q_norm) if np.isfinite(q_norm) else 1e9, 1e9)
                                avg_unshifted_reward += 0.005 * (unshifted_reward - avg_unshifted_reward)
                                accept_rate += 0.005 * (env_info["accepted"] - accept_rate)
                                reward_bar_error += 0.01 * (abs(agent.reward_bar - reward) - reward_bar_error)
                                if should_log_step(t, steps) or t in {switch_step - 1, switch_step, switch_step + 1} or diverged:
                                    rows.append(
                                        {
                                            "seed": seed,
                                            "step": t,
                                            "environment": "access_control_reward_origin_switch",
                                            "switch_type": switch_type,
                                            "phase": phase,
                                            "steps_since_switch": t - switch_step,
                                            "recovery_window": recovery_window(t, switch_step),
                                            "reward_shift": env.reward_shift,
                                            "pre_reward_shift": pre_shift,
                                            "post_reward_shift": post_shift,
                                            "algorithm": name,
                                            "alpha": alpha,
                                            "beta": beta,
                                            "gamma": agent_gamma,
                                            "reward": reward,
                                            "unshifted_reward": unshifted_reward,
                                            "avg_unshifted_reward": avg_unshifted_reward,
                                            "accepted": env_info["accepted"],
                                            "accept_rate": accept_rate,
                                            "reward_bar": agent.reward_bar,
                                            "reward_bar_abs_error_ema": reward_bar_error,
                                            "td_error": info.delta,
                                            "q_norm": q_norm,
                                            "diverged": diverged,
                                        }
                                    )
                                if diverged:
                                    break
                                x, action = x_next, action_next
    return rows, {
        "question": "How sensitive is reward-centered continuing Sarsa to reward-rate tracking and discount choice under a no-reset reward-origin switch?",
        "n_rows": len(rows),
    }
