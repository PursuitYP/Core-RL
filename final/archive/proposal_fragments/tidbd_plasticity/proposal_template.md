# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Per-Feature Step-Size Plasticity in Nonstationary TD Prediction

## What do you want to understand?

Whether per-feature step-size adaptation can act as a small continual-learning mechanism for changing feature relevance. The focused RL question is: does TIDBD-style adaptation raise learning rates on newly useful features while suppressing distractors in a stream?

## What setting or testbed will you use?

A nonstationary linear TD prediction stream with informative, delayed, and distractor features whose relevance changes during learning.

## What will you examine?

Fixed-alpha TD, normalized TD, and a compact TIDBD-lite implementation. The main analysis tracks both prediction error and the feature-wise step-size dynamics.

## What will you look at?

Absolute TD error, per-feature alpha trajectories, switch recovery windows, and distractor-versus-signal alpha separation. A convincing result must show useful plasticity, not only a different final error.

## Expanded Template Details

### Focused RL Problem

The learner predicts from a feature stream whose relevant components change over time. The question is whether per-feature step sizes provide useful plasticity without replay or nonlinear representation learning.

### Agent And Update

Compare fixed-alpha TD, normalized TD, and TIDBD-lite. The template should state the meta-update, beta/meta step size, alpha parameterization, and how this simplified implementation differs from canonical TIDBD or AutoStep.

### Experiment Plan

Use repeated switches in feature relevance and include distractor features. Track both prediction performance and whether feature-wise alphas separate signal from distractors. A stronger version should include canonical TIDBD/AutoStep as a baseline.

### Metrics And Decision Rule

Metrics are absolute TD error, recovery AUC, per-feature alpha trajectories, signal/distractor alpha separation, and stability. The proposal succeeds only if plasticity improves recovery or prediction, not merely if alphas move.

### Fallback

If normalized TD remains better, report TIDBD-lite as a mechanism diagnostic and avoid performance claims.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/tidbd_plasticity/report.md`. Current result: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`. This template is archived because the current report now gives the mechanism-study interpretation.

Current status: supporting mechanism study. TIDBD-lite shows visible step-size adaptation, but normalized TD currently has slightly lower late absolute TD error.

Specific missing details before promotion: canonical TIDBD equations, meta-step-size update, per-feature alpha initialization and clipping, old/new/distractor feature definitions, and a performance metric beyond alpha movement. The proposal would be weakened if per-feature alpha changes remain visible but never improve prediction error or recovery against normalized TD.
