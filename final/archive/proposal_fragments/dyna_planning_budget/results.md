# Results: Dyna Planning Budget

Current result:

`experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main`

Key figure:

![Average reward by planning budget and model mode.](../../../../experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main/figures/avg_reward_by_planning_steps-model_mode_curve.png)

Seed-aware finding:

Planning helps before change, but keeping the old model creates high stale-backup rates after change. Flush-on-change removes stale backups but does not automatically solve recovery.
