from __future__ import annotations

import csv
import importlib.metadata as metadata
import json
import math
import os
import platform
import sys
import time
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np


def ensure_mpl_config(root: Path) -> None:
    """Keep matplotlib from trying to write into the user's home directory."""
    mpl_dir = root / ".mplconfig"
    mpl_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(mpl_dir))


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, Path):
        return str(value)
    return value


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(json_ready(payload), f, indent=2, sort_keys=True)
        f.write("\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def softmax(values: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    z = values / max(temperature, 1e-8)
    z = z - np.max(z)
    exp = np.exp(z)
    return exp / np.sum(exp)


def epsilon_greedy(rng: np.random.Generator, values: np.ndarray, epsilon: float) -> int:
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        raise ValueError("epsilon_greedy requires at least one action value")
    if rng.random() < epsilon:
        return int(rng.integers(len(values)))
    finite = np.isfinite(values)
    if not np.any(finite):
        return int(rng.integers(len(values)))
    safe_values = np.where(finite, values, -np.inf)
    max_value = np.max(safe_values)
    choices = np.flatnonzero(np.isclose(safe_values, max_value))
    return int(rng.choice(choices))


def moving_average(values: Iterable[float], width: int) -> np.ndarray:
    arr = np.asarray(list(values), dtype=float)
    if len(arr) == 0 or width <= 1:
        return arr
    width = min(width, len(arr))
    kernel = np.ones(width) / width
    return np.convolve(arr, kernel, mode="valid")


def summarize_series(values: Iterable[float], tail: int = 100) -> dict[str, float]:
    arr = np.asarray(list(values), dtype=float)
    finite = arr[np.isfinite(arr)]
    if len(finite) == 0:
        return {"mean": math.nan, "tail_mean": math.nan, "min": math.nan, "max": math.nan}
    return {
        "mean": float(np.mean(finite)),
        "tail_mean": float(np.mean(finite[-min(tail, len(finite)) :])),
        "min": float(np.min(finite)),
        "max": float(np.max(finite)),
    }


def recovery_window(step: int, switch_step: int) -> str:
    """Coarse windows for judging adaptation after a nonstationary change."""
    offset = int(step) - int(switch_step)
    if offset < 0:
        return "pre"
    if offset < 250:
        return "post_0_250"
    if offset < 500:
        return "post_250_500"
    if offset < 1000:
        return "post_500_1000"
    return "post_late"


def should_log_step(step: int, steps: int, target_rows: int = 2000) -> bool:
    interval = max(1, int(steps) // max(1, int(target_rows)))
    return step == 0 or step == steps - 1 or step % interval == 0


def base_manifest(proposal: str, suite: str, seeds: list[int], config: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal": proposal,
        "suite": suite,
        "seeds": seeds,
        "config": config,
        "created_utc": timestamp(),
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "packages": package_versions(["numpy", "pandas", "matplotlib", "scipy", "seaborn", "pypdf"]),
        "notes": [
            "No replay buffer is used.",
            "No deep network is used.",
            "All main updates are online streaming updates from the current step.",
        ],
    }


def package_versions(names: list[str]) -> dict[str, str]:
    versions = {"numpy": np.__version__}
    for name in names:
        if name in versions:
            continue
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "not-installed"
    return versions


class Timer:
    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        self.elapsed = 0.0
        return self

    def __exit__(self, *_exc: object) -> None:
        self.elapsed = time.perf_counter() - self.start
