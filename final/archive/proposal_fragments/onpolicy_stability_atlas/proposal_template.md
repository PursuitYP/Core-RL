# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** On-Policy TD Stability Atlas for Scale and Traces

## What do you want to understand?

Which combinations of feature scale, step size, and eligibility traces cause instability in otherwise on-policy linear TD. The focused RL question is: where is the practical stability boundary for streaming TD with scaled features?

## What setting or testbed will you use?

A tile-coded random-walk prediction task used as a diagnostic companion to Output-Controlled TD.

## What will you examine?

Fixed TD and trace-based TD variants across feature scales, alphas, and lambdas.

## What will you look at?

RMSE, divergence, value/weight norms, and stability heatmaps. This proposal answers where normalization is needed, not whether it improves a downstream score.

## Expanded Template Details

### Focused RL Problem

This proposal maps the stability boundary of online TD(lambda) under feature-scale and trace-length changes. The environment is deliberately controlled so instability can be attributed to alpha, lambda, and representation scale.

### Agent And Update

Run fixed-step TD and trace-based TD variants over a grid of alphas, lambdas, and feature scales. The report should specify divergence thresholds and whether each result is seed-level or row-level.

### Experiment Plan

Use tabular and tile-coded random-walk prediction settings. Produce heatmaps of RMSE and divergence across alpha/lambda/scale. This atlas should be interpreted as supporting evidence for output-controlled updates.

### Metrics And Decision Rule

Metrics are RMSE, divergence fraction by seed, time to divergence, weight norm, and TD-error scale. The proposal succeeds as a diagnostic if it reveals clear stability regions and failure boundaries.

### Fallback

Do not submit as a standalone positive result unless it includes a clear stability-boundary theorem or more substantive empirical comparison.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/onpolicy_stability_atlas/report.md`. Current result: `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main`. This template is archived because the current report positions the atlas as support for Output-Controlled TD.

Current status: supporting diagnostic, not an intervention proposal. It maps where fixed-alpha TD(lambda) is fragile under feature scaling, but it does not itself propose a new update.

Specific missing details before promotion: feature construction, true values, alpha/lambda grid, divergence threshold, RMSE evaluation protocol, and a compact stability-boundary figure. It would become more independent if it compared several update geometries, not just mapped fixed TD(lambda). It would be weakened if scale changes did not meaningfully alter the stable alpha/lambda region.
