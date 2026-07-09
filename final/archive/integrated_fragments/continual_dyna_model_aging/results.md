# Results: Continual Dyna Model Aging

Current main pilot:

`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main`

Figures:

![Average reward by planning budget and model mode.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main/figures/avg_reward_by_planning_steps-model_mode_curve.png)

![Stale-backup rate by planning budget and model mode.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main/figures/report_stale_backup_rate_post_late_by_budget.png)

![Model error by planning budget and model mode.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main/figures/mean_model_error_by_planning_steps-model_mode_curve.png)

## Seed-Aware Finding

The main pilot compares keep-model Dyna, oracle flush, recency aging, and recency/error gating under planning budgets `1`, `5`, and `20`.

Key post-change late-window results:

- With one planning backup, keep-model stale-backup rate is about `0.83`; recency aging reduces it to about `0.164`, but reward remains slightly negative.
- With five backups, keep-model stale-backup rate is about `0.691`; recency aging reduces it to about `0.020`, with only modest reward improvement.
- With twenty backups, keep-model stale-backup rate is about `0.336`; recency aging reduces it to about `0.0064` and has the best late reward among tested modes, about `0.073`.
- Oracle flush removes stale backups but does not dominate reward; at twenty backups its late reward is about `0.0566`.

## Interpretation

Recency aging is a realistic online freshness heuristic that substantially reduces stale planning without requiring oracle change detection. It is most useful when the planning budget is large enough for model planning to matter after the change. Error gating adds little in the current deterministic gridworld because many stale entries are harmful before they are revisited and assigned error.

## Current Limitations

The environment still has one scheduled abrupt change. The next version should add gradual drift, repeated changes, and planning-utility-per-backup analysis.
