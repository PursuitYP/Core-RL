# Proposal Configs

Each subdirectory contains proposal-specific JSON configs. Results are written to `../results/<proposal>/...` so each topic can be run and analyzed separately.

Common names:

- `config_smoke.json`: quick smoke check.
- `config_minimal.json`: small sanity run.
- `config_main.json`: current main pilot.
- `config_extended.json`: longer sweep intended for CPU task queues.

The implementation lives in `experiments/alberta_core_rl/studies/`.
