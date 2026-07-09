from __future__ import annotations

from dataclasses import dataclass

import numpy as np


ACTIONS_4 = np.array([(-1, 0), (1, 0), (0, -1), (0, 1)], dtype=int)


class RandomWalkPrediction:
    """Classic episodic random walk used as a streaming prediction testbed."""

    def __init__(self, n_states: int = 19, scale: str = "one", seed: int = 0):
        self.n_states = n_states
        self.rng = np.random.default_rng(seed)
        self.state = (n_states + 1) // 2
        if scale == "one":
            self.scales = np.ones(n_states)
        elif scale == "ten":
            self.scales = np.ones(n_states) * 10.0
        elif scale == "hundred":
            self.scales = np.ones(n_states) * 100.0
        elif scale == "uneven":
            self.scales = np.geomspace(0.01, 100.0, n_states)
        else:
            raise ValueError(f"unknown scale: {scale}")

    @property
    def n_features(self) -> int:
        return self.n_states

    def reset(self) -> np.ndarray:
        self.state = (self.n_states + 1) // 2
        return self.features()

    def features(self) -> np.ndarray:
        x = np.zeros(self.n_states)
        x[self.state - 1] = self.scales[self.state - 1]
        return x

    def true_values(self) -> np.ndarray:
        return np.arange(1, self.n_states + 1, dtype=float) / (self.n_states + 1)

    def predicted_values(self, weights: np.ndarray) -> np.ndarray:
        return weights * self.scales

    def step(self) -> tuple[np.ndarray, float, bool]:
        move = -1 if self.rng.random() < 0.5 else 1
        self.state += move
        if self.state == 0:
            return np.zeros(self.n_states), 0.0, True
        if self.state == self.n_states + 1:
            return np.zeros(self.n_states), 1.0, True
        return self.features(), 0.0, False


class TileRandomWalkPrediction:
    """Large random walk with overlapping tile features for scale-sensitivity studies."""

    def __init__(
        self,
        n_states: int = 51,
        n_tilings: int = 8,
        n_tiles: int = 16,
        scale: str = "one",
        seed: int = 0,
        random_start: bool = True,
    ):
        self.n_states = n_states
        self.n_tilings = n_tilings
        self.n_tiles = n_tiles
        self.random_start = random_start
        self.rng = np.random.default_rng(seed)
        self.state = (n_states + 1) // 2
        n_features = n_tilings * n_tiles
        if scale == "one":
            self.scales = np.ones(n_features)
        elif scale == "ten":
            self.scales = np.ones(n_features) * 10.0
        elif scale == "hundred":
            self.scales = np.ones(n_features) * 100.0
        elif scale == "uneven":
            self.scales = np.geomspace(0.05, 50.0, n_features)
        elif scale == "lognormal":
            self.scales = np.exp(self.rng.normal(scale=1.0, size=n_features))
        else:
            raise ValueError(f"unknown scale: {scale}")

    @property
    def n_features(self) -> int:
        return self.n_tilings * self.n_tiles

    def reset(self) -> np.ndarray:
        if self.random_start:
            self.state = int(self.rng.integers(1, self.n_states + 1))
        else:
            self.state = (self.n_states + 1) // 2
        return self.features()

    def _active_tiles(self, state: int) -> list[int]:
        z = (state - 1) / max(1, self.n_states - 1)
        width = 1.0 / (self.n_tiles - 1)
        active = []
        for tiling in range(self.n_tilings):
            offset = (tiling / self.n_tilings) * width
            tile = int(np.floor((z + offset) / width))
            tile = int(np.clip(tile, 0, self.n_tiles - 1))
            active.append(tiling * self.n_tiles + tile)
        return active

    def features_for_state(self, state: int) -> np.ndarray:
        x = np.zeros(self.n_features)
        if 1 <= state <= self.n_states:
            active = self._active_tiles(state)
            x[active] = self.scales[active] / self.n_tilings
        return x

    def features(self) -> np.ndarray:
        return self.features_for_state(self.state)

    def true_values(self) -> np.ndarray:
        return np.arange(1, self.n_states + 1, dtype=float) / (self.n_states + 1)

    def predicted_values(self, weights: np.ndarray) -> np.ndarray:
        return np.array([float(np.dot(weights, self.features_for_state(s))) for s in range(1, self.n_states + 1)])

    def step(self) -> tuple[np.ndarray, float, bool]:
        move = -1 if self.rng.random() < 0.5 else 1
        self.state += move
        if self.state == 0:
            return np.zeros(self.n_features), 0.0, True
        if self.state == self.n_states + 1:
            return np.zeros(self.n_features), 1.0, True
        return self.features(), 0.0, False


class TwoLoopMDP:
    """Small continuing control problem with a short-low and long-high loop."""

    n_states = 5
    n_actions = 2

    def __init__(self, reward_shift: float = 0.0):
        self.reward_shift = reward_shift
        self.state = 0

    def reset(self) -> int:
        self.state = 0
        return self.state

    def features(self) -> np.ndarray:
        x = np.zeros(self.n_states)
        x[self.state] = 1.0
        return x

    def step(self, action: int) -> tuple[int, float]:
        s = self.state
        if s == 0:
            self.state = 1 if action == 0 else 2
            reward = 0.0
        elif s == 1:
            self.state = 0
            reward = 1.0
        elif s == 2:
            self.state = 3
            reward = 0.0
        elif s == 3:
            self.state = 4
            reward = 0.0
        else:
            self.state = 0
            reward = 3.0
        return self.state, reward + self.reward_shift


class AccessControlQueue:
    """Continuing access-control task from average-reward RL examples."""

    n_actions = 2

    def __init__(
        self,
        n_servers: int = 10,
        priorities: tuple[int, ...] = (1, 2, 4, 8),
        free_prob: float = 0.06,
        reward_shift: float = 0.0,
        seed: int = 0,
    ):
        self.n_servers = n_servers
        self.priorities = priorities
        self.free_prob = free_prob
        self.reward_shift = reward_shift
        self.rng = np.random.default_rng(seed)
        self.free_servers = n_servers
        self.priority_index = 0
        self.reset()

    @property
    def n_states(self) -> int:
        return (self.n_servers + 1) * len(self.priorities)

    def reset(self) -> int:
        self.free_servers = self.n_servers
        self.priority_index = int(self.rng.integers(len(self.priorities)))
        return self.state_index()

    def state_index(self) -> int:
        return self.free_servers * len(self.priorities) + self.priority_index

    def features(self) -> np.ndarray:
        x = np.zeros(self.n_states)
        x[self.state_index()] = 1.0
        return x

    def step(self, action: int) -> tuple[int, float, dict[str, float]]:
        priority = self.priorities[self.priority_index]
        accepted = int(action == 1 and self.free_servers > 0)
        reward = float(priority if accepted else 0.0)
        if accepted:
            self.free_servers -= 1
        busy = self.n_servers - self.free_servers
        freed = int(self.rng.binomial(busy, self.free_prob))
        self.free_servers = min(self.n_servers, self.free_servers + freed)
        self.priority_index = int(self.rng.integers(len(self.priorities)))
        info = {
            "accepted": float(accepted),
            "priority": float(priority),
            "high_priority": float(priority == max(self.priorities)),
            "free_servers": float(self.free_servers),
        }
        return self.state_index(), reward + self.reward_shift, info


class ContinuingGridworld:
    n_actions = 4

    def __init__(self, size: int = 7, reward_shift: float = 0.0, seed: int = 0):
        self.size = size
        self.reward_shift = reward_shift
        self.rng = np.random.default_rng(seed)
        self.start = (size // 2, size // 2)
        self.mid = size // 2
        self.goal = (0, size - 1)
        self.hazards = {(size - 2, 1), (size - 2, 2), (size - 3, 2)}
        self.phase_id = 0
        self.pos = self.start

    @property
    def n_states(self) -> int:
        return self.size * self.size

    def reset(self) -> int:
        self.pos = self.start
        return self.state_index()

    def state_index(self) -> int:
        return self.pos[0] * self.size + self.pos[1]

    def features(self) -> np.ndarray:
        x = np.zeros(self.n_states)
        x[self.state_index()] = 1.0
        return x

    def step(self, action: int) -> tuple[int, float]:
        move = ACTIONS_4[action]
        nr = int(np.clip(self.pos[0] + move[0], 0, self.size - 1))
        nc = int(np.clip(self.pos[1] + move[1], 0, self.size - 1))
        self.pos = (nr, nc)
        reward = -0.01
        if self.pos in self.hazards:
            reward -= 1.0
        if self.pos == self.goal:
            reward += 1.0
            self.pos = self.start
        return self.state_index(), reward + self.reward_shift

    def set_phase(self, phase_id: int) -> None:
        self.phase_id = phase_id
        if phase_id == 0:
            self.goal = (0, self.size - 1)
            self.hazards = {(self.size - 2, 1), (self.size - 2, 2), (self.size - 3, 2)}
        else:
            self.goal = (self.size - 1, self.size - 1)
            self.hazards = {(1, self.size - 3), (2, self.size - 3), (3, self.size - 4), (self.mid, self.mid - 1)}


class TmazeCue:
    """Continuing T-maze with a transient cue and aliased corridor."""

    n_actions = 2

    def __init__(self, length: int = 5, seed: int = 0):
        self.length = length
        self.rng = np.random.default_rng(seed)
        self.cue = 0
        self.pos = 0
        self.reset()

    @property
    def n_raw_features(self) -> int:
        return 5

    def reset(self) -> np.ndarray:
        self.cue = int(self.rng.integers(2))
        self.pos = 0
        return self.observation()

    def observation(self) -> np.ndarray:
        x = np.zeros(self.n_raw_features)
        if self.pos == 0:
            x[self.cue] = 1.0
        elif self.pos < self.length:
            x[2] = 1.0
        else:
            x[3] = 1.0
        x[4] = 1.0
        return x

    def cumulants(self) -> dict[str, float]:
        obs = self.observation()
        return {
            "left_cue": float(obs[0]),
            "right_cue": float(obs[1]),
            "junction": float(obs[3]),
            "bias": 1.0,
        }

    def step(self, action: int) -> tuple[np.ndarray, float, dict[str, float]]:
        if self.pos < self.length:
            self.pos += 1
            reward = 0.0
            info = {"trial_end": 0.0, "correct": np.nan, "terminal_cue": np.nan}
            return self.observation(), reward, info
        terminal_cue = self.cue
        correct = int(action == self.cue)
        reward = 1.0 if correct else -1.0
        info = {"trial_end": 1.0, "correct": float(correct), "terminal_cue": float(terminal_cue)}
        self.reset()
        return self.observation(), reward, info


class TraceConditioningStream:
    """Online prediction stream: cue now, reward after a delay."""

    def __init__(self, delay_a: int = 10, delay_b: int = 20, switch_step: int = 5000):
        self.delay_a = delay_a
        self.delay_b = delay_b
        self.switch_step = switch_step
        self.t = 0

    @property
    def n_features(self) -> int:
        return 2

    def delay(self) -> int:
        return self.delay_a if self.t < self.switch_step else self.delay_b

    def features(self) -> np.ndarray:
        phase_t = self.t % 40
        return np.array([1.0 if phase_t == 0 else 0.0, 1.0])

    def step(self) -> tuple[np.ndarray, float, np.ndarray]:
        x = self.features()
        phase_t = self.t % 40
        reward = 1.0 if phase_t == self.delay() else 0.0
        self.t += 1
        return x, reward, self.features()


class NonStationarySensorStream:
    def __init__(self, n_features: int = 20, switch_step: int = 5000, seed: int = 0):
        self.n_features = n_features
        self.switch_step = switch_step
        self.rng = np.random.default_rng(seed)
        self.t = 0
        self.phase_weights = np.zeros((2, n_features))
        self.phase_weights[0, :5] = np.linspace(0.2, 1.0, 5)
        self.phase_weights[1, 5:10] = np.linspace(1.0, 0.2, 5)
        self.current_x = self.rng.normal(size=n_features)

    def phase(self) -> int:
        return int(self.t >= self.switch_step)

    def features(self) -> np.ndarray:
        return self.current_x.copy()

    def step(self) -> tuple[np.ndarray, float, np.ndarray]:
        x = self.current_x.copy()
        reward = float(np.dot(self.phase_weights[self.phase()], x) + self.rng.normal(scale=0.05))
        self.t += 1
        self.current_x = 0.8 * self.current_x + 0.2 * self.rng.normal(size=self.n_features)
        return x, reward, self.current_x.copy()


class DriftingBandit:
    def __init__(self, n_actions: int = 10, drift: float = 0.01, switch_period: int = 2000, seed: int = 0):
        self.n_actions = n_actions
        self.drift = drift
        self.switch_period = switch_period
        self.rng = np.random.default_rng(seed)
        self.t = 0
        self.q = self.rng.normal(scale=0.1, size=n_actions)
        self.q[0] = 1.0

    def step(self, action: int, reward_shift: float = 0.0) -> tuple[float, int]:
        if self.t > 0 and self.t % self.switch_period == 0:
            self.q = np.roll(self.q, 1)
        reward = float(self.rng.normal(self.q[action], 0.1) + reward_shift)
        self.q += self.rng.normal(scale=self.drift, size=self.n_actions)
        self.t += 1
        return reward, int(np.argmax(self.q))


@dataclass
class FourRoomsState:
    row: int
    col: int


class FourRooms:
    n_actions = 4

    def __init__(self, size: int = 9, seed: int = 0):
        self.size = size
        self.rng = np.random.default_rng(seed)
        self.mid = size // 2
        self.doors = {(self.mid, 1), (self.mid, size - 2), (1, self.mid), (size - 2, self.mid)}
        self.start = FourRoomsState(size - 2, 1)
        self.goals = [FourRoomsState(1, size - 2), FourRoomsState(size - 2, size - 2)]
        self.goal_index = 0
        self.pos = self.start

    @property
    def n_states(self) -> int:
        return self.size * self.size

    def reset(self) -> int:
        self.pos = self.start
        return self.state_index()

    def is_wall(self, row: int, col: int) -> bool:
        if row < 0 or col < 0 or row >= self.size or col >= self.size:
            return True
        if row == self.mid and (row, col) not in self.doors:
            return True
        if col == self.mid and (row, col) not in self.doors:
            return True
        return False

    def state_index(self) -> int:
        return self.pos.row * self.size + self.pos.col

    def features(self) -> np.ndarray:
        x = np.zeros(self.n_states)
        x[self.state_index()] = 1.0
        return x

    def current_goal(self) -> FourRoomsState:
        return self.goals[self.goal_index]

    def step(self, action: int) -> tuple[int, float]:
        dr, dc = ACTIONS_4[action]
        nr = self.pos.row + int(dr)
        nc = self.pos.col + int(dc)
        if not self.is_wall(nr, nc):
            self.pos = FourRoomsState(nr, nc)
        reward = -0.01
        goal = self.current_goal()
        if self.pos.row == goal.row and self.pos.col == goal.col:
            reward = 1.0
            self.goal_index = 1 - self.goal_index
            self.pos = self.start
        return self.state_index(), reward
