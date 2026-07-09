# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Dyna Planning Budget and Model Staleness in a Changing World

## What do you want to understand?

Whether a learned model remains a computational asset when a continual environment changes. The focused RL question is: how does planning budget trade off pre-change sample efficiency against post-change harm from obsolete model backups?

## What setting or testbed will you use?

A continuing gridworld whose goal and hazard layout change midstream. The agent keeps a compact learned model for Dyna backups; this model is not a replay buffer of raw experience.

## What will you examine?

No-planning Q-learning, Dyna with one backup, and Dyna with five backups, each with keep-model versus flush-model behavior after the change. This archived template reflects the older baseline scope; the later integrated model-aging study adds budget `20` and recency/error-based model selection.

## What will you look at?

Average reward, stale-backup rate, Q norm, and recovery-window summaries. The central figure should show both the pre-change benefit of planning and the post-change risk of planning from stale model entries.

## Expanded Template Details

### Focused RL Problem

The agent learns online in a continuing gridworld that changes partway through the stream. It maintains a one-step learned model and uses that model for Dyna backups. The central question is whether extra planning computation helps or hurts once some model entries become stale.

### Agent And Update

The baseline is Q-learning without planning. Dyna variants use the same real-step update plus sampled model backups. The model stores next state, reward, and the phase in which the transition was observed so stale backups can be diagnosed. Flush-on-change is an oracle diagnostic, not a realistic method.

### Experiment Plan

Vary planning budget, model handling, and change severity. The first version uses one abrupt layout change; the stronger version should include repeated or gradual changes. All runs should be evaluated by pre-change performance and post-change recovery, not just global average reward.

### Metrics And Decision Rule

Primary metrics are real-step average reward, stale-backup rate, model size, Q norm, and recovery-window summaries. The proposal is convincing only if it shows both sides of the tradeoff: planning benefit before change and stale-computation cost after change.

### Fallback

If the model-staleness story is weak, merge this proposal into Continual Dyna Model Aging as a baseline/diagnostic rather than submitting it independently.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/dyna_planning_budget/report.md`. Current result: `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended`; older `results.md` fragments in this archive preserve pilot evidence only. This template is archived because the proposal has been rewritten as a standalone report and partly superseded by `final/reports/integrated/continual_dyna_model_aging/report.md`.

Current status: conditional/precursor proposal. It demonstrates that model staleness is a real planning problem, but it does not yet offer a realistic freshness mechanism beyond keep-model and oracle-style flushing.

Specific missing details before promotion: formal Dyna backup equation, model-entry schema, staleness definition, phase-change protocol, planning-budget accounting, and a planning-utility measure. The proposal would be upgraded if increasing planning budget improved pre-change learning while freshness-aware handling reduced post-change stale backups and recovery time. It would be weakened if stale-backup rate did not predict recovery or if flushing always dominated realistic online heuristics.
