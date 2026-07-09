# Evidence Map: Continual Dyna Model Aging

## Existing Evidence

This large proposal builds on the completed Dyna Planning Budget pilot:

`experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main`

Existing finding:

- Planning improves pre-change reward in a changing gridworld.
- Keeping the old model produces high stale-backup rates after the layout change.
- Flush-on-change removes stale backups but is an oracle diagnostic and does not fully solve recovery.

Dedicated large-proposal pilot:

`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main`

New finding:

- Recency aging gives a realistic online freshness mechanism.
- At planning budget `20`, it reduces late stale-backup rate from about `0.336` to about `0.0064` and improves late reward relative to keep-model and oracle flush.

## What This Evidence Supports

The current evidence supports the problem formulation and a first online mitigation:

- model-based planning can help while the model is fresh;
- stale model entries are measurable;
- stale planning is a real post-change risk.
- recency aging can sharply reduce stale computation without an oracle change signal.

## What It Does Not Yet Support

The current evidence does not yet show robustness across many types of nonstationarity. The result is currently strongest for a single abrupt layout change and large planning budget.

## Required New Experiments

1. Recency-aged Dyna.
2. Model-error-gated Dyna.
3. Planning budget sweep `0, 1, 5, 20`.
4. Abrupt and gradual nonstationarity.
5. Repeated changes.
6. Planning utility per backup.

## Promotion Rule

Promote this large proposal only if a realistic freshness mechanism improves recovery or stale-computation tradeoff relative to both keep-model and lower-budget Dyna.
