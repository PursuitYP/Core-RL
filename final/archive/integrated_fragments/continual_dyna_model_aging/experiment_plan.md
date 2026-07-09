# Experiment Plan: Continual Dyna Model Aging

## Minimum Credible Experiment

1. Add `last_seen` and `recent_model_error` fields to the compact Dyna model.
2. Implement random keep-model, flush oracle, and recency-aged planning.
3. Run a two-phase changing gridworld with planning budgets `0, 1, 5, 20`.
4. Report reward and stale-backup rate by phase.
5. Plot recovery windows with seed confidence intervals.

## Strong Experiment

Add a gradual-drift environment. Abrupt changes test stale memory; gradual drift tests whether model aging over-forgets useful structure.

## Baselines And Ablations

- No planning.
- Random Dyna keep-model.
- Oracle flush.
- Uniform aging only.
- Error gate only.
- Aging plus error gate.
- Optional prioritized sweeping without aging, if predecessor bookkeeping is kept compact.

## Figures

- Figure 1: reward by planning budget and model-freshness rule.
- Figure 2: stale-backup rate by time.
- Figure 3: model error and recovery time scatter.
- Figure 4: planning utility per backup.
- Figure 5: abrupt-change versus gradual-drift comparison.

## Promotion Criteria

Promote only if aging/error-gating improves the reward/stale-harm tradeoff over both keep-model and flush in at least one meaningful nonstationary setting. If it does not, report a negative conclusion: simple model freshness heuristics are insufficient without better change detection or exploration.
