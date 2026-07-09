# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Centered TD as a Mechanism Diagnostic for Reward Translation

## What do you want to understand?

How reward or Bellman-error centering changes the scale of TD learning in a continuing prediction problem. The focused RL question is: does centering remove arbitrary offset terms from the learned value scale?

## What setting or testbed will you use?

A compact continuing Markov chain with controlled reward shifts, used as a mechanism diagnostic rather than the main control study.

## What will you examine?

Ordinary TD, reward-centered TD, and centered variants under different reward offsets.

## What will you look at?

Value norm, TD-error offset, and prediction error across reward shifts. The figure should explain why centering stabilizes the main Reward-Centered Sarsa experiment.

## Expanded Template Details

### Focused RL Problem

This is a mechanism diagnostic for reward centering. The environment is intentionally small so reward translation can be isolated from exploration and policy-learning complications. The learner receives a continuing stream with controlled reward offsets and predicts values using TD-style updates.

### Agent And Update

The comparison should include uncentered TD, reward-centered TD, and any Bellman-error-centered variant used in the report. The template should state the TD target, how the average reward or centering baseline is estimated, and which terms are subtracted from the update.

### Experiment Plan

Sweep reward offsets and step sizes while keeping the underlying transition structure fixed. The key manipulation is that the task-relevant prediction differences should remain the same while raw reward origin changes.

### Metrics And Decision Rule

The main metrics are value norm, TD-error mean/variance, baseline tracking, and prediction error. The proposal succeeds if centering reduces arbitrary value-scale inflation without hiding true prediction error.

### Fallback

This should remain an appendix-style mechanism study supporting Reward-Centered Sarsa unless it is expanded into a richer continuing prediction/control environment.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/centered_td_diagnostics/report.md`. Current result: `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main`. This template is archived because the current report has absorbed the template answers and the mechanism interpretation.

Current status: mechanism diagnostic for Reward-Centered Sarsa. It is independent enough to reproduce, but it should not be presented as a full course-project main topic because the environment is deliberately small and explanatory.

Specific missing details before promotion: exact prediction problem, ordinary TD target, reward-centered TD target, Bellman-error-centered diagnostic target, value-norm definition, and the reason unshifted reward is not the right primary metric here. The proposal succeeds only if centering reduces shift-induced value-scale inflation without hiding unstable TD errors. It would be weakened if centered TD simply changes the scale by using a much smaller effective alpha.
