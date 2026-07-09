# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Doorway Options as Reusable Subtasks in Four Rooms

## What do you want to understand?

Whether temporally extended actions help a small continuing/online agent by creating reusable subtask structure, or whether option execution cost and option bias erase the benefit. The focused RL question is: when do doorway options improve real environment-step learning rather than just decision-step curves?

## What setting or testbed will you use?

A Four Rooms navigation problem with primitive movement actions and hand-coded doorway options. Goal placement can change to test transfer rather than only first-task speed.

## What will you examine?

Primitive-action control versus a policy that can also choose doorway options. Evaluation counts real environment steps, option usage, and behavior after goal/layout changes.

## What will you look at?

Reward per environment step, steps-to-goal, option-use rate, and post-change recovery. A positive option story requires faster or more robust learning after accounting for the real cost of executing an option.

## Expanded Template Details

### Focused RL Problem

The agent navigates a Four Rooms environment using primitive actions and optional doorway-directed temporally extended actions. The research question is whether options improve learning in real environment steps and transfer across goal changes.

### Agent And Update

Primitive control is compared with an SMDP option agent. The template must specify each option's initiation set, internal policy, termination condition, duration handling, discounting through the option, and update target. Without these details, a negative result cannot be interpreted.

### Experiment Plan

First run a fixed-goal sanity case to verify options are implemented correctly. Only then run goal-switch or layout-change tests. Track real environment steps, not only high-level decisions, because options hide multiple primitive transitions.

### Metrics And Decision Rule

Metrics are reward per environment step, steps to goal, option success rate, option duration, option-use frequency, and recovery after goal switch. A positive result requires improvement after accounting for option execution cost.

### Fallback

Current evidence is negative. If fixed-goal sanity fails, quarantine the proposal and report it as an implementation/design lesson rather than an option-transfer result.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/options_reusable_subtasks/report.md`. Current result: `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`. This template is archived because the current report quarantines the claim and explains why the transfer result is not trustworthy yet.

Current status: quarantined. The option-transfer claim is not supported; primitive actions are not clearly beaten, and a fixed-goal sanity win has not been established. This is still a useful record because it states what a fair options experiment must control.

Specific missing details before promotion: option initiation sets, termination conditions, intra-option policy, SMDP target with duration, environment-step accounting, fixed-goal baseline, goal-change protocol, and whether options are learned or hand-coded. The proposal would be falsified as an option-transfer result if options do not first improve or match fixed-goal learning under fair environment-step accounting.
