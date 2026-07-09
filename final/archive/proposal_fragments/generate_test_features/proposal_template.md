# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Generate-and-Test Trace Features in a Nonstationary Prediction Stream

## What do you want to understand?

Whether a continual learner with limited feature capacity can replace stale features with more useful temporal traces after the world changes. The focused RL question is: can a streaming utility test discover trace timescales that improve online prediction after a delay shift?

## What setting or testbed will you use?

A synthetic sensor-prediction stream in which the relevant delay changes during learning. The task is online prediction with no stored dataset and no replay.

## What will you examine?

Fixed trace banks, random replacement, and generate-and-test replacement using feature utility. The main variables are trace timescale capacity, replacement rule, and the pre/post-change recovery window.

## What will you look at?

Absolute prediction error, learned trace timescales, replacement events, and recovery after the delay change. The proposal is only successful if feature utility improves prediction, not merely if it selects plausible-looking timescales.

## Expanded Template Details

### Focused RL Problem

The learner observes a streaming sensor process where the useful predictive delay changes over time. It has a limited feature budget and must decide which trace features to keep, replace, or generate online. There is no stored dataset and no replay.

### Agent And Update

A linear TD/prediction learner uses a feature set containing candidate temporal traces. Generate-and-test assigns each feature a utility score, removes low-utility features, and samples replacements from a distribution over trace timescales. The final report must state the utility formula, replacement cadence, initialization of new features, and candidate distribution.

### Experiment Plan

First verify a testbed where an oracle trace bank clearly outperforms random features; otherwise generate-and-test cannot be fairly evaluated. Then compare fixed traces, random replacement, generate-and-test, and oracle-like banks before and after a delay shift.

### Metrics And Decision Rule

Metrics are absolute prediction error, recovery AUC after delay shift, selected trace timescales, replacement count, and utility trajectories. A positive result requires lower prediction error or faster recovery, not merely plausible-looking feature choices.

### Fallback

The current evidence is negative. If oracle/fixed sanity checks fail, the proposal should be rewritten as a negative testbed-design lesson rather than a method success.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/generate_test_features/report.md`. Current result: `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`. This template is archived because the current report now gives the negative-result interpretation and reproduction path.

Current status: independent negative result and redesign target. The current utility rule performs feature replacement, but late absolute error does not beat random replacement; the oracle-like feature bank also does not validate the testbed strongly enough.

Specific missing details before promotion: exact candidate-generation distribution, utility update formula, replacement schedule, trace parameterization, fixed/random/oracle baselines, and a downstream value/control metric. The proposal would be falsified as a positive generate-and-test result if utility-guided replacement keeps failing to beat random replacement on post-change prediction error or recovery.
