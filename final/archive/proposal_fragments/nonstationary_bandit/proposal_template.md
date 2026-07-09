# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Nonstationary Bandit as a Minimal Continual-Adaptation Sanity Check

## What do you want to understand?

How constant step-size learning, sample averaging, and simple exploration behave when the best action changes. The focused RL question is: what minimal diagnostics reveal adaptation versus stale averaging in an online learner?

## What setting or testbed will you use?

A drifting or switching k-armed bandit with no state and no replay. It is intentionally a sanity check, not a full final proposal.

## What will you examine?

Sample-average action values, constant-alpha estimates, epsilon-greedy variants, and change rates.

## What will you look at?

Best-action rate, online regret, recovery after switches, and estimate lag. This proposal is useful only as a baseline intuition for larger continual RL proposals.

## Expanded Template Details

### Focused RL Problem

This is a minimal continual-adaptation sanity check. The agent repeatedly selects among arms while reward means drift or switch. There is no state representation, bootstrapping, planning, or value function over states, so the proposal is intentionally limited.

### Agent And Update

Compare sample-average estimates with constant-alpha estimates and epsilon-greedy exploration. The update is online and one-sample-at-a-time. The key mechanism is tracking versus stale averaging.

### Experiment Plan

Vary drift rate, switch frequency, alpha, and exploration. The experiment should be used to validate logging, seed handling, and recovery-window analysis before moving to richer RL tasks.

### Metrics And Decision Rule

Metrics are best-action rate, online reward, regret-like loss, recovery time after switches, and estimate lag. A positive result only shows adaptation intuition; it does not constitute a full Core-RL research contribution.

### Fallback

Keep as appendix or intro example. If promoted, upgrade to contextual bandit or continuing control with value learning.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/nonstationary_bandit/report.md`. Current result: `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`. This template is archived because the current report demotes the study to a sanity diagnostic.

Current status: dropped as a final Core-RL proposal. The stream is useful for demonstrating constant-alpha tracking, but it lacks state, bootstrapping, planning, GVFs, options, learned models, or temporal abstraction. The current result shows the expected sanity pattern, not a deep course-project contribution.

Specific missing details if kept as appendix: exact arm reward means, drift/switch schedule, exploration rule, step-size update, regret definition, and best-action computation. To become submission-grade, it would need to become a contextual/continuing control problem with state and bootstrapped value learning. As written, it is falsified only as a sanity check if constant-alpha tracking fails to outperform sample averages under drift.
