from __future__ import annotations

import numpy as np

from ..core import recovery_window, should_log_step
from ..envs import ContinuingGridworld


def baird_features(state: int) -> np.ndarray:
    x = np.zeros(8)
    if state < 6:
        x[state] = 2.0
        x[6] = 1.0
    else:
        x[6] = 2.0
        x[7] = 1.0
    return x


def proposal_baird_offpolicy_stability(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    gamma = 0.99
    algs = ["offpolicy_td", "tdc"]
    alphas = [0.01] if suite != "main" else [0.005, 0.01, 0.02]
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for alpha in alphas:
            for alg in algs:
                w = np.ones(8)
                w[6] = 10.0
                h = np.zeros(8)
                state = int(rng.integers(7))
                for t in range(steps):
                    solid = rng.random() < (1.0 / 7.0)
                    rho = 7.0 if solid else 0.0
                    next_state = 6 if solid else int(rng.integers(6))
                    x = baird_features(state)
                    xp = baird_features(next_state)
                    delta = gamma * float(np.dot(w, xp)) - float(np.dot(w, x))
                    if alg == "offpolicy_td":
                        w += alpha * rho * delta * x
                    else:
                        beta = 5.0 * alpha
                        correction = gamma * xp * float(np.dot(x, h))
                        w += alpha * rho * (delta * x - correction)
                        h += beta * rho * (delta - float(np.dot(h, x))) * x
                    norm = float(np.linalg.norm(w))
                    rows.append(
                        {
                            "seed": seed,
                            "step": t,
                            "algorithm": alg,
                            "alpha": alpha,
                            "state": state,
                            "next_state": next_state,
                            "rho": rho,
                            "td_error": delta,
                            "weight_norm": min(norm, 1e9),
                            "diverged": float((not np.isfinite(norm)) or norm > 1e8),
                        }
                    )
                    if not np.isfinite(norm) or norm > 1e8:
                        break
                    state = next_state
    return rows, {"question": "Where does semi-gradient off-policy TD fail on Baird's counterexample?", "n_rows": len(rows)}


def proposal_dyna_planning_budget(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    planning_steps_set = [0, 1, 5] if suite != "smoke" else [0, 1]
    model_modes = ["keep_model", "flush_on_change"] if suite == "main" else ["keep_model"]
    if suite == "main" and steps >= 20000:
        planning_steps_set = [0, 1, 5, 20]
    alpha = 0.1
    gamma = 0.95
    epsilon = 0.1
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for planning_steps in planning_steps_set:
            for model_mode in model_modes:
                grid_size = 11 if suite == "main" and steps >= 20000 else 9 if suite == "main" else 7
                env = ContinuingGridworld(size=grid_size, seed=seed)
                env.reset()
                q = np.zeros((env.n_states, env.n_actions))
                model: dict[tuple[int, int], tuple[int, float, int]] = {}
                avg_reward = 0.0
                phase = 0
                stale_backup_rate = 0.0
                switch_step = steps // 2
                for t in range(steps):
                    if suite == "main" and t == switch_step:
                        phase = 1
                        env.set_phase(phase)
                        if model_mode == "flush_on_change":
                            model.clear()
                    s = env.state_index()
                    if rng.random() < epsilon:
                        a = int(rng.integers(env.n_actions))
                    else:
                        a = int(np.argmax(q[s]))
                    sp, r = env.step(a)
                    q[s, a] += alpha * (r + gamma * float(np.max(q[sp])) - q[s, a])
                    model[(s, a)] = (sp, r, phase)
                    keys = list(model.keys())
                    stale_backups = 0
                    for _ in range(planning_steps):
                        if not keys:
                            break
                        ms, ma = keys[int(rng.integers(len(keys)))]
                        msp, mr, mphase = model[(ms, ma)]
                        stale = int(mphase != phase)
                        stale_backups += stale
                        q[ms, ma] += alpha * (mr + gamma * float(np.max(q[msp])) - q[ms, ma])
                    if planning_steps > 0:
                        stale_backup_rate += 0.02 * ((stale_backups / planning_steps) - stale_backup_rate)
                    avg_reward += 0.02 * (r - avg_reward)
                    if should_log_step(t, steps):
                        rows.append(
                            {
                                "seed": seed,
                                "step": t,
                                "algorithm": f"dyna_{planning_steps}_{model_mode}",
                                "planning_steps": planning_steps,
                                "model_mode": model_mode,
                                "grid_size": grid_size,
                                "phase": phase,
                                "steps_since_switch": t - switch_step,
                                "recovery_window": recovery_window(t, switch_step),
                                "reward": r,
                                "avg_reward": avg_reward,
                                "model_size": len(model),
                                "stale_backup_rate": stale_backup_rate,
                                "q_norm": float(np.linalg.norm(q)),
                            }
                        )
    return rows, {"question": "How much does a tiny learned model help under a fixed planning budget?", "n_rows": len(rows)}


def _model_key_probabilities(
    keys: list[tuple[int, int]],
    model: dict[tuple[int, int], dict[str, float]],
    t: int,
    mode: str,
    half_life: float,
) -> np.ndarray | None:
    if not keys:
        return None
    if mode == "keep_model" or mode == "oracle_flush":
        return None
    weights = []
    for key in keys:
        entry = model[key]
        age = max(0.0, float(t) - float(entry["last_seen"]))
        recency = np.exp(-age / max(1.0, half_life))
        error_weight = 1.0
        if mode == "recency_error_gate":
            error_weight = 1.0 / (1.0 + float(entry["model_error"]))
        weights.append(recency * error_weight)
    probs = np.asarray(weights, dtype=float)
    if not np.any(np.isfinite(probs)) or float(np.sum(probs)) <= 0.0:
        return None
    return probs / float(np.sum(probs))


def proposal_continual_dyna_model_aging(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    """Dyna with online model-freshness heuristics under nonstationarity."""
    rows: list[dict] = []
    planning_steps_set = [1, 5] if suite == "smoke" else [1, 5, 20]
    model_modes = ["keep_model", "oracle_flush", "recency_aging", "recency_error_gate"]
    alpha = 0.1
    gamma = 0.95
    epsilon = 0.1
    half_lives = [80.0] if suite == "smoke" else [750.0]
    if suite == "main" and steps >= 20000:
        planning_steps_set = [0, 1, 5, 20]
        half_lives = [250.0, 750.0, 1500.0, 4000.0]
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for planning_steps in planning_steps_set:
            modes_for_budget = ["no_planning"] if planning_steps == 0 else model_modes
            for model_mode in modes_for_budget:
                half_life_values = half_lives if model_mode in {"recency_aging", "recency_error_gate"} else [0.0]
                for half_life in half_life_values:
                    env = ContinuingGridworld(size=9 if suite == "main" else 7, seed=seed)
                    env.reset()
                    q = np.zeros((env.n_states, env.n_actions))
                    model: dict[tuple[int, int], dict[str, float]] = {}
                    avg_reward = 0.0
                    stale_backup_rate = 0.0
                    planning_abs_td = 0.0
                    phase = 0
                    switch_step = steps // 2
                    for t in range(steps):
                        if t == switch_step:
                            phase = 1
                            env.set_phase(phase)
                            if model_mode == "oracle_flush":
                                model.clear()
                        s = env.state_index()
                        a = int(rng.integers(env.n_actions)) if rng.random() < epsilon else int(np.argmax(q[s]))
                        sp, r = env.step(a)
                        real_td = r + gamma * float(np.max(q[sp])) - q[s, a]
                        q[s, a] += alpha * real_td
                        key = (s, a)
                        previous = model.get(key)
                        model_error = 0.0
                        if previous is not None:
                            model_error = abs(float(previous["reward"]) - r) + float(int(previous["next_state"]) != sp)
                            model_error = 0.8 * float(previous["model_error"]) + 0.2 * model_error
                        model[key] = {
                            "next_state": float(sp),
                            "reward": float(r),
                            "phase": float(phase),
                            "last_seen": float(t),
                            "model_error": float(model_error),
                        }
                        keys = list(model.keys())
                        stale_backups = 0
                        backup_abs_td_values = []
                        probs = _model_key_probabilities(keys, model, t, model_mode, half_life)
                        for _ in range(planning_steps):
                            if not keys:
                                break
                            if probs is None:
                                sampled = keys[int(rng.integers(len(keys)))]
                            else:
                                sampled = keys[int(rng.choice(len(keys), p=probs))]
                            ms, ma = sampled
                            entry = model[(ms, ma)]
                            msp = int(entry["next_state"])
                            mr = float(entry["reward"])
                            stale = int(int(entry["phase"]) != phase)
                            stale_backups += stale
                            td = mr + gamma * float(np.max(q[msp])) - q[ms, ma]
                            q[ms, ma] += alpha * td
                            backup_abs_td_values.append(abs(td))
                        stale_fraction = stale_backups / max(1, planning_steps)
                        stale_backup_rate += 0.02 * (stale_fraction - stale_backup_rate)
                        if backup_abs_td_values:
                            planning_abs_td += 0.02 * (float(np.mean(backup_abs_td_values)) - planning_abs_td)
                        avg_reward += 0.02 * (r - avg_reward)
                        if should_log_step(t, steps):
                            rows.append(
                                {
                                    "seed": seed,
                                    "step": t,
                                    "algorithm": f"dyna_{planning_steps}_{model_mode}",
                                    "environment": "changing_gridworld_model_aging",
                                    "planning_steps": planning_steps,
                                    "model_mode": model_mode,
                                    "half_life": half_life,
                                    "phase": phase,
                                    "steps_since_switch": t - switch_step,
                                    "recovery_window": recovery_window(t, switch_step),
                                    "reward": r,
                                    "avg_reward": avg_reward,
                                    "real_abs_td": abs(real_td),
                                    "planning_abs_td": planning_abs_td,
                                    "model_size": len(model),
                                    "stale_backup_rate": stale_backup_rate,
                                    "mean_model_error": float(np.mean([entry["model_error"] for entry in model.values()])),
                                    "q_norm": float(np.linalg.norm(q)),
                                }
                            )
    return rows, {
        "question": "Can online model aging reduce stale Dyna backups without discarding the whole model?",
        "n_rows": len(rows),
    }
