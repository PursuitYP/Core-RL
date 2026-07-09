# Experiments

Start with `alberta_core_rl/`. The top-level `experiments/` directory is only a workspace for runnable experiment suites; it is not a Python package. The actual package is `alberta_core_rl`, which keeps the Core-RL code, configs, scripts, and generated results together without flattening them into the repository root.

The important subdirectories are:

- `alberta_core_rl/configs/`: per-proposal JSON configs.
- `alberta_core_rl/studies/`: proposal-specific experiment implementations.
- `alberta_core_rl/scripts/`: run, plot, summarize, smoke-test, and CPU-task helper scripts.
- `alberta_core_rl/results/`: generated experiment outputs.

Final-facing interpretation lives in `final/reports/` and `final/indexes/`.
