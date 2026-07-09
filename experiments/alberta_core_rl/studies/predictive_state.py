from __future__ import annotations

from collections import deque

import numpy as np

from ..core import should_log_step
from ..agents import LinearSarsa, LinearTD
from ..envs import TmazeCue


def make_tmaze_features(
    raw: np.ndarray,
    history: deque[np.ndarray],
    gvf_values: np.ndarray | None,
    mode: str,
    oracle: np.ndarray | None = None,
    cue_trace: np.ndarray | None = None,
) -> np.ndarray:
    if mode == "raw":
        return raw
    if mode in {"history", "short_history"}:
        parts = [raw] + list(history)
        return np.concatenate(parts)
    if mode in {"gvf", "recurrent_gvf", "cue_gvf"}:
        assert gvf_values is not None
        return np.concatenate([raw, gvf_values])
    if mode == "trace_memory":
        assert cue_trace is not None
        return np.concatenate([raw, cue_trace])
    if mode == "oracle":
        assert oracle is not None
        return np.concatenate([raw, oracle])
    raise ValueError(mode)


def update_cue_trace(raw: np.ndarray, cue_trace: np.ndarray, decay: float = 0.97) -> np.ndarray:
    trace = decay * cue_trace
    if raw[0] > 0.5 or raw[1] > 0.5:
        trace = np.zeros_like(trace)
        trace[:2] = raw[:2]
    return trace


def proposal_useful_gvfs_state(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    if suite == "main":
        modes = ["raw", "short_history", "trace_memory", "recurrent_gvf", "oracle"]
        length = 12
        hist_len = 4
    elif suite == "smoke":
        modes = ["raw", "recurrent_gvf"]
        length = 5
        hist_len = 3
    else:
        modes = ["raw", "history", "recurrent_gvf", "oracle"]
        length = 7
        hist_len = 3
    rows: list[dict] = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for mode in modes:
            env = TmazeCue(length=length, seed=seed)
            raw = env.reset()
            history = deque([np.zeros_like(raw) for _ in range(hist_len)], maxlen=hist_len)
            gvfs = [LinearTD(env.n_raw_features + 2, alpha=0.08, gamma=0.95, method="normalized") for _ in range(2)]
            gvf_values = np.zeros(2)
            cue_trace = update_cue_trace(raw, np.zeros(2))
            oracle = np.zeros(2)
            oracle[env.cue] = 1.0
            n_features = len(make_tmaze_features(raw, history, gvf_values, mode, oracle, cue_trace))
            agent = LinearSarsa(
                n_features,
                env.n_actions,
                alpha=0.05,
                gamma=0.95,
                epsilon=0.1,
                method="normalized",
                alpha_max=0.1,
            )
            phi = make_tmaze_features(raw, history, gvf_values, mode, oracle, cue_trace)
            action = agent.choose_action(rng, phi)
            recent_reward = 0.0
            trial_accuracy = 0.5
            for t in range(steps):
                position = env.pos
                raw_next, reward, info_env = env.step(action)
                gvf_abs_error = 0.0
                gvf_values_next = gvf_values.copy()
                if mode == "recurrent_gvf":
                    terminal_cue = info_env["terminal_cue"]
                    left_outcome = 1.0 if terminal_cue == 0.0 else -1.0 if np.isfinite(terminal_cue) else 0.0
                    right_outcome = 1.0 if terminal_cue == 1.0 else -1.0 if np.isfinite(terminal_cue) else 0.0
                    x_gvf = np.concatenate([raw, gvf_values])
                    x_gvf_next = np.concatenate([raw_next, gvf_values])
                    deltas = []
                    for gvf, cumulant in zip(gvfs, [left_outcome, right_outcome]):
                        info = gvf.update(x_gvf, cumulant, x_gvf_next)
                        deltas.append(abs(info.delta))
                    gvf_abs_error = float(np.mean(deltas))
                    gvf_values_next = np.array([gvf.value(x_gvf_next) for gvf in gvfs])
                history.appendleft(raw)
                cue_trace_next = update_cue_trace(raw_next, cue_trace)
                oracle_next = np.zeros(2)
                oracle_next[env.cue] = 1.0
                phi_next = make_tmaze_features(raw_next, history, gvf_values_next, mode, oracle_next, cue_trace_next)
                action_next = agent.choose_action(rng, phi_next)
                update = agent.update(phi, action, reward, phi_next, action_next)
                recent_reward += 0.02 * (reward - recent_reward)
                if info_env["trial_end"]:
                    trial_accuracy += 0.05 * (info_env["correct"] - trial_accuracy)
                if should_log_step(t, steps) or info_env["trial_end"]:
                    rows.append(
                        {
                            "seed": seed,
                            "step": t,
                            "algorithm": mode,
                            "maze_length": length,
                            "maze_position": position,
                            "reward": reward,
                            "avg_reward": recent_reward,
                            "trial_end": info_env["trial_end"],
                            "correct": info_env["correct"],
                            "trial_accuracy": trial_accuracy if info_env["trial_end"] else np.nan,
                            "terminal_cue": info_env["terminal_cue"],
                            "cue_trace_left": cue_trace[0],
                            "cue_trace_right": cue_trace[1],
                            "junction_action": action if info_env["trial_end"] else np.nan,
                            "gvf_left_value": gvf_values[0] if len(gvf_values) > 0 else np.nan,
                            "gvf_right_value": gvf_values[1] if len(gvf_values) > 1 else np.nan,
                            "gvf_abs_td_error": gvf_abs_error,
                            "control_td_error": update.delta,
                        }
                    )
                raw, phi, action = raw_next, phi_next, action_next
                gvf_values, oracle, cue_trace = gvf_values_next, oracle_next, cue_trace_next
    return rows, {"question": "When are GVF predictions useful as agent state?", "n_rows": len(rows)}


def proposal_predictive_state_plasticity(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    """First gate for the larger predictive-state plasticity proposal."""
    rows: list[dict] = []
    modes = ["raw", "trace_memory", "recurrent_gvf", "cue_gvf", "oracle"]
    lengths = [8] if suite == "smoke" else [8, 12, 20]
    if suite == "main" and steps >= 20000:
        lengths = [8, 12, 20, 30]
    hist_len = 4
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for length in lengths:
            for mode in modes:
                env = TmazeCue(length=length, seed=seed)
                raw = env.reset()
                history = deque([np.zeros_like(raw) for _ in range(hist_len)], maxlen=hist_len)
                gvfs = [LinearTD(env.n_raw_features + 2, alpha=0.08, gamma=0.98, method="normalized") for _ in range(2)]
                gvf_values = np.zeros(2)
                cue_trace = update_cue_trace(raw, np.zeros(2), decay=0.97)
                oracle = np.zeros(2)
                oracle[env.cue] = 1.0
                n_features = len(make_tmaze_features(raw, history, gvf_values, mode, oracle, cue_trace))
                agent = LinearSarsa(
                    n_features,
                    env.n_actions,
                    alpha=0.05,
                    gamma=0.95,
                    epsilon=0.1,
                    method="normalized",
                    alpha_max=0.1,
                )
                phi = make_tmaze_features(raw, history, gvf_values, mode, oracle, cue_trace)
                action = agent.choose_action(rng, phi)
                trial_accuracy = 0.5
                recent_reward = 0.0
                for t in range(steps):
                    position = env.pos
                    hidden_cue = env.cue
                    raw_next, reward, info_env = env.step(action)
                    gvf_abs_error = 0.0
                    gvf_values_next = gvf_values.copy()
                    if mode in {"recurrent_gvf", "cue_gvf"}:
                        x_gvf = np.concatenate([raw, gvf_values])
                        x_gvf_next = np.concatenate([raw_next, gvf_values])
                        deltas = []
                        if mode == "cue_gvf":
                            cumulants = [float(raw[0]), float(raw[1])]
                        else:
                            terminal_cue = info_env["terminal_cue"]
                            cumulants = [
                                1.0 if terminal_cue == 0.0 else -1.0 if np.isfinite(terminal_cue) else 0.0,
                                1.0 if terminal_cue == 1.0 else -1.0 if np.isfinite(terminal_cue) else 0.0,
                            ]
                        for gvf, cumulant in zip(gvfs, cumulants):
                            info = gvf.update(x_gvf, cumulant, x_gvf_next)
                            deltas.append(abs(info.delta))
                        gvf_abs_error = float(np.mean(deltas))
                        gvf_values_next = np.array([gvf.value(x_gvf_next) for gvf in gvfs])
                    history.appendleft(raw)
                    cue_trace_next = update_cue_trace(raw_next, cue_trace, decay=0.97)
                    oracle_next = np.zeros(2)
                    oracle_next[env.cue] = 1.0
                    phi_next = make_tmaze_features(raw_next, history, gvf_values_next, mode, oracle_next, cue_trace_next)
                    action_next = agent.choose_action(rng, phi_next)
                    update = agent.update(phi, action, reward, phi_next, action_next)
                    recent_reward += 0.02 * (reward - recent_reward)
                    if info_env["trial_end"]:
                        trial_accuracy += 0.05 * (info_env["correct"] - trial_accuracy)
                    signed_margin = gvf_values[0] - gvf_values[1] if hidden_cue == 0 else gvf_values[1] - gvf_values[0]
                    if should_log_step(t, steps) or info_env["trial_end"]:
                        rows.append(
                            {
                                "seed": seed,
                                "step": t,
                                "algorithm": mode,
                                "environment": "tmaze_predictive_state_plasticity",
                                "maze_length": length,
                                "maze_position": position,
                                "phase": 0,
                                "reward": reward,
                                "avg_reward": recent_reward,
                                "trial_end": info_env["trial_end"],
                                "correct": info_env["correct"],
                                "trial_accuracy": trial_accuracy if info_env["trial_end"] else np.nan,
                                "hidden_cue": hidden_cue,
                                "terminal_cue": info_env["terminal_cue"],
                                "cue_trace_left": cue_trace[0],
                                "cue_trace_right": cue_trace[1],
                                "gvf_left_value": gvf_values[0],
                                "gvf_right_value": gvf_values[1],
                                "cue_alignment_margin": signed_margin,
                                "gvf_abs_td_error": gvf_abs_error,
                                "control_td_error": update.delta,
                            }
                        )
                    raw, phi, action = raw_next, phi_next, action_next
                    gvf_values, oracle, cue_trace = gvf_values_next, oracle_next, cue_trace_next
    return rows, {
        "question": "Can redesigned cue GVFs carry useful predictive state before feature-plasticity mechanisms are added?",
        "n_rows": len(rows),
    }


def _decode_signal(
    mode: str,
    hidden_cue: int,
    raw: np.ndarray,
    cue_trace: np.ndarray,
    oracle: np.ndarray,
    gvf_values: np.ndarray,
    position: int,
) -> tuple[float, float]:
    sign = 1.0 if hidden_cue == 0 else -1.0
    if mode == "raw":
        if position == 0:
            margin = sign * (raw[0] - raw[1])
        else:
            margin = 0.0
    elif mode == "trace_memory":
        margin = sign * (cue_trace[0] - cue_trace[1])
    elif mode == "oracle":
        margin = sign * (oracle[0] - oracle[1])
    else:
        margin = sign * (gvf_values[0] - gvf_values[1])
    correct = 1.0 if margin > 1e-8 else 0.0 if margin < -1e-8 else 0.5
    return float(correct), float(margin)


def _gvf_cumulants(kind: str, raw: np.ndarray, terminal_cue: float) -> list[float]:
    if kind == "cue":
        return [float(raw[0]), float(raw[1])]
    if kind == "terminal":
        return [
            1.0 if terminal_cue == 0.0 else -1.0 if np.isfinite(terminal_cue) else 0.0,
            1.0 if terminal_cue == 1.0 else -1.0 if np.isfinite(terminal_cue) else 0.0,
        ]
    if kind == "junction":
        return [float(raw[3]), 1.0]
    raise ValueError(kind)


def proposal_useful_predictive_knowledge(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    """Gate useful-prediction claims by cue information and downstream control."""
    lengths = [8] if suite == "smoke" else [8, 12, 20]
    if suite == "main" and steps >= 15000:
        lengths = [8, 12, 20, 30]
    conditions = [("raw", "none", 0.0), ("trace_memory", "none", 0.0), ("oracle", "none", 0.0)]
    for cumulant in ["cue", "terminal", "junction"]:
        for gamma in [0.8, 0.95, 0.99]:
            conditions.append((f"gvf_{cumulant}", cumulant, gamma))
    rows: list[dict] = []
    hist_len = 4
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for length in lengths:
            for mode, cumulant, gvf_gamma in conditions:
                env = TmazeCue(length=length, seed=seed)
                raw = env.reset()
                history = deque([np.zeros_like(raw) for _ in range(hist_len)], maxlen=hist_len)
                gvfs = [
                    LinearTD(env.n_raw_features + 2, alpha=0.06, gamma=gvf_gamma or 0.95, method="normalized")
                    for _ in range(2)
                ]
                gvf_values = np.zeros(2)
                cue_trace = update_cue_trace(raw, np.zeros(2), decay=0.97)
                oracle = np.zeros(2)
                oracle[env.cue] = 1.0
                feature_mode = mode if mode in {"raw", "trace_memory", "oracle"} else "recurrent_gvf"
                n_features = len(make_tmaze_features(raw, history, gvf_values, feature_mode, oracle, cue_trace))
                agent = LinearSarsa(
                    n_features,
                    env.n_actions,
                    alpha=0.05,
                    gamma=0.95,
                    epsilon=0.1,
                    method="normalized",
                    alpha_max=0.1,
                )
                phi = make_tmaze_features(raw, history, gvf_values, feature_mode, oracle, cue_trace)
                action = agent.choose_action(rng, phi)
                trial_accuracy = 0.5
                recent_reward = 0.0
                for t in range(steps):
                    position = env.pos
                    hidden_cue = env.cue
                    decode_correct, cue_margin = _decode_signal(
                        feature_mode, hidden_cue, raw, cue_trace, oracle, gvf_values, position
                    )
                    raw_next, reward, info_env = env.step(action)
                    gvf_abs_error = 0.0
                    gvf_values_next = gvf_values.copy()
                    if cumulant != "none":
                        x_gvf = np.concatenate([raw, gvf_values])
                        x_gvf_next = np.concatenate([raw_next, gvf_values])
                        deltas = []
                        for gvf, target in zip(gvfs, _gvf_cumulants(cumulant, raw, info_env["terminal_cue"])):
                            info = gvf.update(x_gvf, target, x_gvf_next)
                            deltas.append(abs(info.delta))
                        gvf_abs_error = float(np.mean(deltas))
                        gvf_values_next = np.array([gvf.value(x_gvf_next) for gvf in gvfs])
                    history.appendleft(raw)
                    cue_trace_next = update_cue_trace(raw_next, cue_trace, decay=0.97)
                    oracle_next = np.zeros(2)
                    oracle_next[env.cue] = 1.0
                    phi_next = make_tmaze_features(raw_next, history, gvf_values_next, feature_mode, oracle_next, cue_trace_next)
                    action_next = agent.choose_action(rng, phi_next)
                    update = agent.update(phi, action, reward, phi_next, action_next)
                    recent_reward += 0.02 * (reward - recent_reward)
                    if info_env["trial_end"]:
                        trial_accuracy += 0.05 * (info_env["correct"] - trial_accuracy)
                    if should_log_step(t, steps) or info_env["trial_end"]:
                        rows.append(
                            {
                                "seed": seed,
                                "step": t,
                                "algorithm": mode,
                                "environment": "tmaze_useful_predictive_knowledge",
                                "maze_length": length,
                                "cumulant": cumulant,
                                "gamma": gvf_gamma,
                                "maze_position": position,
                                "hidden_cue": hidden_cue,
                                "reward": reward,
                                "avg_reward": recent_reward,
                                "trial_end": info_env["trial_end"],
                                "correct": info_env["correct"],
                                "trial_accuracy": trial_accuracy if info_env["trial_end"] else np.nan,
                                "cue_decoding_correct": decode_correct,
                                "decision_cue_decoding_correct": decode_correct if info_env["trial_end"] else np.nan,
                                "cue_alignment_margin": cue_margin,
                                "gvf_abs_td_error": gvf_abs_error,
                                "control_td_error": update.delta,
                            }
                        )
                    raw, phi, action = raw_next, phi_next, action_next
                    gvf_values, oracle, cue_trace = gvf_values_next, oracle_next, cue_trace_next
    return rows, {
        "question": "When does learned predictive knowledge become usable state for online control?",
        "n_rows": len(rows),
    }
