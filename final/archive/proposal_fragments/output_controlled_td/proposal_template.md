# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Output-Controlled TD for Scale-Robust Streaming Prediction

## What do you want to understand?

Whether a TD learner should control the intended change in its prediction output rather than the raw Euclidean movement of its weights. The focused RL question is: can normalization make online TD robust to feature-scale changes in a one-sample-at-a-time stream?

## What setting or testbed will you use?

A continuing random-walk prediction task with overlapping tile-coded features. The feature representation is deliberately rescaled to create identical prediction problems with different parameter-space geometry.

## What will you examine?

Fixed-step TD, normalized TD, trace-normalized TD(lambda), and true-online TD(lambda) across feature scales, step sizes, and trace settings. The central manipulation is representation scale, not environment dynamics.

## What will you look at?

RMSE over states, divergence flags, weight norm, and prediction-change magnitude. The key figure is an alpha-by-scale stability atlas showing whether output-controlled updates remove feature-scale sensitivity.

## Expanded Template Details

### Focused RL Problem

The learner performs online value prediction with linear function approximation. The same prediction problem is represented using feature vectors with different magnitudes, testing whether the algorithm's step-size unit is meaningful across representations.

### Agent And Update

Compare fixed TD, normalized TD, trace-normalized TD(lambda), and true-online TD(lambda). The report should state the update denominator for normalized variants, the trace definition, and how alpha maps to prediction-output change.

### Experiment Plan

Cross feature scale, alpha, lambda, and representation type. A stronger version adds a midstream feature-rescale event without resetting weights. True-online TD(lambda) needs a separate max-stable-alpha audit so baseline failure is not confused with implementation or tuning unfairness.

### Metrics And Decision Rule

Metrics are RMSE, divergence fraction by seed, time to divergence, weight norm, prediction-change magnitude, and stability heatmaps. The proposal succeeds if normalized methods keep a wider stable region under equivalent feature rescalings.

### Fallback

If true-online baseline audit changes the picture, revise the claim to compare update units rather than to rank algorithms.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/output_controlled_td/report.md`. Current result: `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`. This template is archived because the current report contains the full motivation, equations, current evidence, and reproduction command.

Current status: main proposal. The current evidence supports feature-scale robustness for normalized and trace-normalized TD in tile-coded random-walk prediction.

Specific missing details before final submission: exact normalized TD denominator, trace update, true-online TD(lambda) formula, divergence threshold, max-stable-alpha table, and a nonstationary feature-scale switch without reset. The proposal would be weakened if a fair alpha-scaled true-online TD baseline matches normalized TD across all scale conditions.
