# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** GVF Question Design: Accurate Predictions Versus Useful State

## What do you want to understand?

Why some predictions are useful for control while others are merely easy to learn. The focused RL question is: which cumulants and discounts produce predictions that align with the hidden variable needed by a downstream agent?

## What setting or testbed will you use?

Small controlled GVF prediction streams derived from the partial-observability setting, with different cumulants and horizons.

## What will you examine?

Bias cumulants, cue cumulants, junction-related cumulants, and different discounts. The experiment is a design diagnostic for a future GVF predictive-state study.

## What will you look at?

GVF absolute TD error, spatial/temporal prediction profiles, and correlation with the control-relevant hidden cue. Low prediction error alone is not a success criterion.

## Expanded Template Details

### Focused RL Problem

This proposal studies GVF question selection. The stream supports multiple possible cumulants and discounts, but only some predictions should help a downstream partially observable control task. The problem is to distinguish easy predictions from useful state variables.

### Agent And Update

Multiple GVF learners are trained online with different cumulants, discounts, and horizons. The experiment should log both prediction quality and relevance to the hidden cue or downstream decision.

### Experiment Plan

Compare bias-like cumulants, cue cumulants, terminal-outcome cumulants, and junction-related cumulants. The minimal version is a prediction diagnostic; the stronger version plugs each GVF group into the T-maze control learner and measures ablation effects.

### Metrics And Decision Rule

Metrics are GVF TD error, prediction profiles by position/time, cue-decodability, and downstream control utility. Low prediction error alone is not success. A useful GVF should either improve control or encode information the control problem actually needs.

### Fallback

If downstream utility is not implemented, classify this proposal as a design diagnostic rather than an independent positive result.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/gvf_question_design/report.md`. Current result: `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main`. This template is archived because the current report treats the idea as a diagnostic for GVF redesign rather than a final control result.

Current status: supporting diagnostic. The result suggests that easy-to-predict questions are not automatically useful, but downstream control utility is not yet directly measured.

Specific missing details before promotion: exact cumulants, discounts, termination/continuation functions, prediction target semantics, cue-relevance metric, and downstream control ablation. The proposal would be falsified if prediction error alone reliably selected the same GVF questions as downstream cue/control utility; it would be strengthened if low-error bias questions were shown to be useless while harder cue-relevant questions improved T-maze control.
