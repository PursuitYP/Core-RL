from __future__ import annotations

import numpy as np

from ..agents import LinearSarsa
from ..envs import FourRooms


def option_action_toward(env: FourRooms, target: tuple[int, int]) -> int:
    dr = target[0] - env.pos.row
    dc = target[1] - env.pos.col
    if abs(dr) > abs(dc):
        return 1 if dr > 0 else 0
    return 3 if dc > 0 else 2


def execute_doorway_option(env: FourRooms, door: tuple[int, int], max_duration: int, gamma: float) -> tuple[float, int, int]:
    total_reward = 0.0
    duration = 0
    for k in range(max_duration):
        action = option_action_toward(env, door)
        _, reward = env.step(action)
        total_reward += (gamma**k) * reward
        duration += 1
        if (env.pos.row, env.pos.col) == door:
            break
    return total_reward, duration, int((env.pos.row, env.pos.col) == door)


def proposal_options(seeds: list[int], suite: str, steps: int) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    algs = (
        ["primitive", "short_options", "long_options"]
        if suite == "main"
        else ["primitive", "doorway_options"]
        if suite != "smoke"
        else ["doorway_options"]
    )
    gamma = 0.99
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for alg in algs:
            env = FourRooms(size=13 if suite == "main" else 9, seed=seed)
            env.reset()
            doors = sorted(env.doors)
            n_top_actions = env.n_actions if alg == "primitive" else env.n_actions + len(doors)
            agent = LinearSarsa(env.n_states, n_top_actions, alpha=0.1, gamma=gamma, epsilon=0.1, method="normalized")
            avg_reward = 0.0
            env_step = 0
            decision_step = 0
            last_goal_index = env.goal_index
            steps_since_goal_switch = 0
            while env_step < steps:
                x = env.features()
                top_action = agent.choose_action(rng, x)
                option_used = 0
                option_success = np.nan
                if alg == "primitive" or top_action < env.n_actions:
                    primitive_action = top_action % env.n_actions
                    _, reward = env.step(primitive_action)
                    x_next = env.features()
                    next_action = agent.choose_action(rng, x_next)
                    info = agent.update_smdp(x, top_action, reward, 1, x_next, next_action)
                    duration = 1
                else:
                    option_used = 1
                    door = doors[top_action - env.n_actions]
                    max_duration = 4 if alg in {"short_options", "doorway_options"} else 10
                    reward, duration, option_success = execute_doorway_option(env, door, max_duration, gamma)
                    x_next = env.features()
                    next_action = agent.choose_action(rng, x_next)
                    info = agent.update_smdp(x, top_action, reward, duration, x_next, next_action)
                env_step += duration
                decision_step += 1
                goal_switched = int(env.goal_index != last_goal_index)
                steps_since_goal_switch = 0 if goal_switched else steps_since_goal_switch + duration
                last_goal_index = env.goal_index
                reward_per_env_step = reward / max(1, duration)
                avg_reward += 0.02 * (reward_per_env_step - avg_reward)
                rows.append(
                    {
                        "seed": seed,
                        "step": min(env_step, steps - 1),
                        "decision_step": decision_step,
                        "algorithm": alg,
                        "reward": reward,
                        "reward_per_env_step": reward_per_env_step,
                        "avg_reward": avg_reward,
                        "duration": duration,
                        "td_error": info.delta,
                        "goal_index": env.goal_index,
                        "goal_switched": goal_switched,
                        "steps_since_goal_switch": steps_since_goal_switch,
                        "option_used": option_used,
                        "option_success": option_success,
                    }
                )
    return rows, {"question": "Are doorway options reusable under changing goals?", "n_rows": len(rows)}

