from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..agents import LinearSarsa, LinearTD
from ..envs import TmazeCue
from .predictive_state import _decode_signal, _gvf_cumulants, update_cue_trace


@dataclass
class CandidatePair:
    learners: list[LinearTD]
    values: np.ndarray
    td_error_ema: float = 1.0
    decode_ema: float = 0.5


def _budget_feature(raw: np.ndarray, extra: np.ndarray | None) -> np.ndarray:
    if extra is None:
        return raw
    return np.concatenate([raw, extra])


def _candidate_extra(
    mode: str,
    active_kind: str,
    cue_trace: np.ndarray,
    oracle: np.ndarray,
    candidates: dict[str, CandidatePair],
) -> np.ndarray | None:
    if mode == "raw_budget0":
        return None
    if mode == "trace_budget2":
        return cue_trace
    if mode == "oracle_budget2":
        return oracle
    if mode == "fixed_cue_gvf":
        return candidates["cue"].values
    if mode == "fixed_terminal_gvf":
        return candidates["terminal"].values
    if mode == "fixed_junction_gvf":
        return candidates["junction"].values
    if mode in {"low_td_error_selector", "oracle_decode_selector"}:
        return candidates[active_kind].values
    raise ValueError(mode)


def _select_kind(mode: str, candidates: dict[str, CandidatePair]) -> str:
    if mode == "fixed_cue_gvf":
        return "cue"
    if mode == "fixed_terminal_gvf":
        return "terminal"
    if mode == "fixed_junction_gvf":
        return "junction"
    if mode == "low_td_error_selector":
        return min(candidates, key=lambda name: candidates[name].td_error_ema)
    if mode == "oracle_decode_selector":
        return max(candidates, key=lambda name: candidates[name].decode_ema)
    return "none"


def _decode_for_mode(
    mode: str,
    active_kind: str,
    hidden_cue: int,
    raw: np.ndarray,
    cue_trace: np.ndarray,
    oracle: np.ndarray,
    candidates: dict[str, CandidatePair],
    position: int,
) -> tuple[float, float]:
    if mode == "trace_budget2":
        return _decode_signal("trace_memory", hidden_cue, raw, cue_trace, oracle, np.zeros(2), position)
    if mode == "oracle_budget2":
        return _decode_signal("oracle", hidden_cue, raw, cue_trace, oracle, np.zeros(2), position)
    if active_kind != "none":
        return _decode_signal(
            "recurrent_gvf",
            hidden_cue,
            raw,
            cue_trace,
            oracle,
            candidates[active_kind].values,
            position,
        )
    return _decode_signal("raw", hidden_cue, raw, cue_trace, oracle, np.zeros(2), position)


def _make_candidates(env: TmazeCue) -> dict[str, CandidatePair]:
    gammas = {"cue": 0.8, "terminal": 0.95, "junction": 0.95}
    return {
        kind: CandidatePair(
            learners=[
                LinearTD(env.n_raw_features + 2, alpha=0.06, gamma=gamma, method="normalized")
                for _ in range(2)
            ],
            values=np.zeros(2),
        )
        for kind, gamma in gammas.items()
    }


def _update_candidates(
    candidates: dict[str, CandidatePair],
    raw: np.ndarray,
    raw_next: np.ndarray,
    terminal_cue: float,
    hidden_cue: int,
    position: int,
) -> None:
    for kind, pair in candidates.items():
        x_gvf = np.concatenate([raw, pair.values])
        x_gvf_next = np.concatenate([raw_next, pair.values])
        errors: list[float] = []
        for learner, target in zip(pair.learners, _gvf_cumulants(kind, raw, terminal_cue)):
            info = learner.update(x_gvf, target, x_gvf_next)
            errors.append(abs(info.delta))
        pair.values = np.array([learner.value(x_gvf_next) for learner in pair.learners])
        mean_error = float(np.mean(errors))
        pair.td_error_ema = 0.98 * pair.td_error_ema + 0.02 * mean_error
        decode_correct, _ = _decode_signal("recurrent_gvf", hidden_cue, raw, np.zeros(2), np.zeros(2), pair.values, position)
        pair.decode_ema = 0.98 * pair.decode_ema + 0.02 * decode_correct


def proposal_useful_predictive_knowledge_budget(
    seeds: list[int], suite: str, steps: int
) -> tuple[list[dict], dict]:
    """Gate useful predictions under a two-feature control budget."""
    lengths = [8] if suite == "smoke" else [8, 12, 20]
    log_interval = max(1, steps // 800)
    modes = [
        "raw_budget0",
        "trace_budget2",
        "oracle_budget2",
        "fixed_cue_gvf",
        "fixed_terminal_gvf",
        "fixed_junction_gvf",
        "low_td_error_selector",
        "oracle_decode_selector",
    ]
    rows: list[dict] = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for length in lengths:
            for mode in modes:
                env = TmazeCue(length=length, seed=seed)
                raw = env.reset()
                candidates = _make_candidates(env)
                cue_trace = update_cue_trace(raw, np.zeros(2), decay=0.97)
                oracle = np.zeros(2)
                oracle[env.cue] = 1.0
                active_kind = _select_kind(mode, candidates)
                extra = _candidate_extra(mode, active_kind, cue_trace, oracle, candidates)
                n_features = len(_budget_feature(raw, extra))
                agent = LinearSarsa(
                    n_features,
                    env.n_actions,
                    alpha=0.05,
                    gamma=0.95,
                    epsilon=0.1,
                    method="normalized",
                    alpha_max=0.1,
                )
                phi = _budget_feature(raw, extra)
                action = agent.choose_action(rng, phi)
                trial_accuracy = 0.5
                recent_reward = 0.0
                selector_switches = 0.0
                last_active_kind = active_kind
                for t in range(steps):
                    position = env.pos
                    hidden_cue = env.cue
                    decode_correct, cue_margin = _decode_for_mode(
                        mode,
                        active_kind,
                        hidden_cue,
                        raw,
                        cue_trace,
                        oracle,
                        candidates,
                        position,
                    )
                    raw_next, reward, info_env = env.step(action)
                    _update_candidates(
                        candidates,
                        raw,
                        raw_next,
                        info_env["terminal_cue"],
                        hidden_cue,
                        position,
                    )
                    cue_trace_next = update_cue_trace(raw_next, cue_trace, decay=0.97)
                    oracle_next = np.zeros(2)
                    oracle_next[env.cue] = 1.0
                    next_active_kind = _select_kind(mode, candidates)
                    selector_switches += float(next_active_kind != last_active_kind)
                    last_active_kind = next_active_kind
                    extra_next = _candidate_extra(mode, next_active_kind, cue_trace_next, oracle_next, candidates)
                    phi_next = _budget_feature(raw_next, extra_next)
                    action_next = agent.choose_action(rng, phi_next)
                    update = agent.update(phi, action, reward, phi_next, action_next)
                    recent_reward += 0.02 * (reward - recent_reward)
                    if info_env["trial_end"]:
                        trial_accuracy += 0.05 * (info_env["correct"] - trial_accuracy)
                    if t == 0 or t == steps - 1 or t % log_interval == 0:
                        selected_error = (
                            candidates[active_kind].td_error_ema if active_kind != "none" else np.nan
                        )
                        selected_decode = (
                            candidates[active_kind].decode_ema if active_kind != "none" else np.nan
                        )
                        rows.append(
                            {
                                "seed": seed,
                                "step": t,
                                "algorithm": mode,
                                "environment": "tmaze_useful_predictive_knowledge_budget",
                                "maze_length": length,
                                "feature_budget": 0 if mode == "raw_budget0" else 2,
                                "maze_position": position,
                                "active_prediction": active_kind,
                                "selected_is_cue": float(active_kind == "cue"),
                                "selector_switch_count": selector_switches,
                                "reward": reward,
                                "avg_reward": recent_reward,
                                "trial_end": info_env["trial_end"],
                                "correct": info_env["correct"],
                                "trial_accuracy": trial_accuracy if info_env["trial_end"] else np.nan,
                                "selected_cue_decoding_correct": decode_correct,
                                "decision_selected_cue_decoding_correct": decode_correct
                                if info_env["trial_end"]
                                else np.nan,
                                "selected_cue_margin": cue_margin,
                                "selected_gvf_td_error_ema": selected_error,
                                "selected_decode_ema": selected_decode,
                                "control_td_error": update.delta,
                            }
                        )
                    raw, phi, action = raw_next, phi_next, action_next
                    cue_trace, oracle, active_kind = cue_trace_next, oracle_next, next_active_kind
    return rows, {
        "question": "Which predictive feature pair survives a two-feature state budget and improves T-maze control?",
        "n_rows": len(rows),
    }
