# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Auxiliary Prediction for Streaming Representation

## What do you want to understand?

Whether an auxiliary next-feature prediction target improves a small streaming value learner when data cannot be revisited. The focused RL question is: does an auxiliary prediction create more useful linear features, or does it add optimization burden without control/prediction benefit?

## What setting or testbed will you use?

A nonstationary streaming prediction diagnostic with simple linear features and no stored transitions. The current evidence is prediction-only; a control link would require a redesigned environment.

## What will you examine?

Base TD learning versus TD with an auxiliary prediction update, under the same one-pass stream.

## What will you look at?

TD error, auxiliary prediction error, recovery after nonstationarity, and feature/weight norms. A positive story requires downstream improvement, not just a decreasing auxiliary loss.

## Expanded Template Details

### Focused RL Problem

This is a streaming prediction study asking whether an auxiliary next-feature prediction improves the main value prediction. It is prediction-focused; current evidence should not be described as full control improvement.

### Agent And Update

A main TD/value learner is compared with a learner that also updates auxiliary prediction weights. The report must state how auxiliary predictions enter the feature vector or shared representation, and whether the auxiliary update competes with or augments the main update.

### Experiment Plan

Run streams with and without nonstationary feature relevance. Compare no-auxiliary, next-feature auxiliary, and more task-relevant auxiliary targets if available. The current next-feature target is a weak first test.

### Metrics And Decision Rule

Metrics are main prediction error, auxiliary prediction error, recovery after change, and weight/feature diagnostics. Auxiliary loss decreasing is not success unless the main prediction improves.

### Fallback

Current evidence is negative. Keep as a redesign target unless a more relevant auxiliary question is introduced.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/streaming_representation/report.md`. Current result: `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main`. This template is archived because the current report demotes the study to a negative diagnostic.

Current status: dropped/redesign target. Auxiliary next-feature prediction does not materially improve the main value prediction in the current stream; phase-1 absolute TD error is essentially tied with value-only learning.

Specific missing details before promotion: exact auxiliary target, how auxiliary predictions enter the representation, whether parameters are shared or separate, main value target, nonstationary stream protocol, and a downstream control metric. The proposal would be falsified as an auxiliary-representation claim if auxiliary loss decreases but the main value/control metric does not improve.
