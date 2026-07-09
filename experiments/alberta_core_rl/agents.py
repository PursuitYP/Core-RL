from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .core import epsilon_greedy, softmax


@dataclass
class UpdateInfo:
    delta: float
    step_size: float
    weight_norm: float
    prediction_change: float


class LinearTD:
    def __init__(
        self,
        n_features: int,
        alpha: float = 0.05,
        gamma: float = 0.99,
        lam: float = 0.0,
        method: str = "fixed",
        eps: float = 1e-8,
        alpha_max: float = 1.0,
    ):
        self.w = np.zeros(n_features, dtype=float)
        self.alpha = alpha
        self.gamma = gamma
        self.lam = lam
        self.method = method
        self.eps = eps
        self.alpha_max = alpha_max
        self.z = np.zeros(n_features, dtype=float)
        self.v_old = 0.0

    def value(self, x: np.ndarray) -> float:
        return float(np.dot(self.w, x))

    def reset_trace(self) -> None:
        self.z *= 0.0
        self.v_old = 0.0

    def _step_size(self, x: np.ndarray, z: np.ndarray | None = None) -> float:
        if self.method == "fixed" or self.method == "true_online":
            return self.alpha
        if self.method in {"normalized", "true_online_normalized"}:
            denom = self.eps + float(np.dot(x, x))
            return min(self.alpha_max, self.alpha / denom)
        if self.method == "trace_normalized":
            target = z if z is not None else x
            denom = self.eps + float(np.dot(target, target))
            return min(self.alpha_max, self.alpha / denom)
        if self.method == "xtz_normalized":
            target = z if z is not None else x
            denom = self.eps + abs(float(np.dot(x, target)))
            return min(self.alpha_max, self.alpha / denom)
        raise ValueError(f"unknown TD method: {self.method}")

    def update(self, x: np.ndarray, reward: float, x_next: np.ndarray, terminal: bool = False) -> UpdateInfo:
        gamma = 0.0 if terminal else self.gamma
        v_before = self.value(x)
        v_next = self.value(x_next)
        delta = reward + gamma * v_next - v_before
        if self.method in {"true_online", "true_online_normalized"}:
            step_size = self._step_size(x)
            dot_zx = float(np.dot(self.z, x))
            self.z = gamma * self.lam * self.z + (1.0 - step_size * gamma * self.lam * dot_zx) * x
            self.w += step_size * (delta + v_before - self.v_old) * self.z - step_size * (v_before - self.v_old) * x
            self.v_old = 0.0 if terminal else v_next
        else:
            self.z = gamma * self.lam * self.z + x
            step_size = self._step_size(x, self.z)
            self.w += step_size * delta * self.z
        v_after = self.value(x)
        if terminal:
            self.reset_trace()
        return UpdateInfo(delta, step_size, float(np.linalg.norm(self.w)), abs(v_after - v_before))


class TIDBDLite:
    """Small per-feature adaptive TD step-size baseline."""

    def __init__(self, n_features: int, theta: float = 0.01, beta0: float = -5.0, gamma: float = 0.99):
        self.w = np.zeros(n_features)
        self.beta = np.ones(n_features) * beta0
        self.h = np.zeros(n_features)
        self.theta = theta
        self.gamma = gamma

    def value(self, x: np.ndarray) -> float:
        return float(np.dot(self.w, x))

    def update(self, x: np.ndarray, reward: float, x_next: np.ndarray) -> UpdateInfo:
        v_before = self.value(x)
        delta = reward + self.gamma * self.value(x_next) - v_before
        alpha = np.exp(np.clip(self.beta, -12.0, 2.0))
        self.beta += self.theta * delta * x * self.h
        self.w += alpha * delta * x
        self.h = self.h * (1.0 - alpha * x * x) + alpha * delta * x
        v_after = self.value(x)
        return UpdateInfo(delta, float(np.mean(alpha)), float(np.linalg.norm(self.w)), abs(v_after - v_before))


class LinearSarsa:
    def __init__(
        self,
        n_features: int,
        n_actions: int,
        alpha: float = 0.1,
        gamma: float = 0.99,
        epsilon: float = 0.1,
        lam: float = 0.0,
        centered: bool = False,
        differential: bool = False,
        beta: float = 0.01,
        method: str = "fixed",
        alpha_max: float = 1.0,
    ):
        self.w = np.zeros((n_actions, n_features), dtype=float)
        self.z = np.zeros_like(self.w)
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.lam = lam
        self.centered = centered
        self.differential = differential
        self.beta = beta
        self.reward_bar = 0.0
        self.method = method
        self.alpha_max = alpha_max

    def q_values(self, x: np.ndarray) -> np.ndarray:
        return np.nan_to_num(self.w @ x, nan=0.0, posinf=1e9, neginf=-1e9)

    def choose_action(self, rng: np.random.Generator, x: np.ndarray) -> int:
        return epsilon_greedy(rng, self.q_values(x), self.epsilon)

    def reset_trace(self) -> None:
        self.z *= 0.0

    def update(self, x: np.ndarray, action: int, reward: float, x_next: np.ndarray, next_action: int) -> UpdateInfo:
        q = float(np.dot(self.w[action], x))
        q_next = float(np.dot(self.w[next_action], x_next))
        centered_reward = reward
        if self.centered or self.differential:
            centered_reward = reward - self.reward_bar
        gamma = 1.0 if self.differential else self.gamma
        delta = centered_reward + gamma * q_next - q
        self.reward_bar += self.beta * delta if self.differential else self.beta * (reward - self.reward_bar)
        self.z *= gamma * self.lam
        self.z[action] += x
        alpha = self.alpha
        if self.method == "normalized":
            alpha = min(self.alpha_max, self.alpha / (1e-8 + float(np.dot(self.z[action], self.z[action]))))
        before = q
        self.w += alpha * delta * self.z
        after = float(np.dot(self.w[action], x))
        return UpdateInfo(delta, alpha, float(np.linalg.norm(self.w)), abs(after - before))

    def update_smdp(
        self,
        x: np.ndarray,
        action: int,
        reward: float,
        duration: int,
        x_next: np.ndarray,
        next_action: int,
    ) -> UpdateInfo:
        q = float(np.dot(self.w[action], x))
        q_next = float(np.dot(self.w[next_action], x_next))
        discount = self.gamma ** max(1, duration)
        delta = reward + discount * q_next - q
        alpha = self.alpha
        if self.method == "normalized":
            alpha = min(self.alpha_max, self.alpha / (1e-8 + float(np.dot(x, x))))
        before = q
        self.w[action] += alpha * delta * x
        after = float(np.dot(self.w[action], x))
        return UpdateInfo(delta, alpha, float(np.linalg.norm(self.w)), abs(after - before))


class GradientBandit:
    def __init__(self, n_actions: int, alpha: float = 0.1, use_baseline: bool = True, seed: int = 0):
        self.h = np.zeros(n_actions)
        self.alpha = alpha
        self.use_baseline = use_baseline
        self.reward_bar = 0.0
        self.t = 0
        self.rng = np.random.default_rng(seed)

    def action(self) -> int:
        return int(self.rng.choice(len(self.h), p=softmax(self.h)))

    def update(self, action: int, reward: float) -> None:
        probs = softmax(self.h)
        baseline = self.reward_bar if self.use_baseline else 0.0
        one_hot = np.zeros_like(self.h)
        one_hot[action] = 1.0
        self.h += self.alpha * (reward - baseline) * (one_hot - probs)
        self.t += 1
        self.reward_bar += (reward - self.reward_bar) / max(1, self.t)


class ActionValueBandit:
    def __init__(self, n_actions: int, alpha: float | None, epsilon: float = 0.1, seed: int = 0):
        self.q = np.zeros(n_actions)
        self.counts = np.zeros(n_actions)
        self.alpha = alpha
        self.epsilon = epsilon
        self.rng = np.random.default_rng(seed)

    def action(self) -> int:
        return epsilon_greedy(self.rng, self.q, self.epsilon)

    def update(self, action: int, reward: float) -> None:
        self.counts[action] += 1
        alpha = self.alpha if self.alpha is not None else 1.0 / self.counts[action]
        self.q[action] += alpha * (reward - self.q[action])
