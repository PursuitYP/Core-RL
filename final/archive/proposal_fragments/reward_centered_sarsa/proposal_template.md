# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Reward-Centered Sarsa for Translation-Robust Continuing Control

## What do you want to understand?

Whether a continuing control agent can be made insensitive to arbitrary additive reward offsets without changing the task or relying on episodic resets. The focused RL question is: does online reward centering preserve learning scale and behavior when all observed rewards are shifted by a constant?

## What setting or testbed will you use?

A continuing access-control queue with accept/reject decisions, customer priorities, server availability, and no terminal episodes. This setting is large enough to require nontrivial control but still small enough for transparent tabular Sarsa diagnostics.

## What will you examine?

Discounted Sarsa, reward-centered Sarsa, and differential Sarsa under several constant reward shifts. The main variation is reward translation, while the task-relevant unshifted reward remains the same.

## What will you look at?

Unshifted average reward, action-value norm, TD-error scale, and seed-aware tail summaries. A convincing figure should show whether reward-centered and differential methods keep similar value scales and rewards across shifts while ordinary discounted Sarsa does not.

## Expanded Template Details

### Focused RL Problem

The agent controls a continuing access-control queue. A constant reward shift changes the observed reward stream but should not change the task-relevant average-reward control problem. The proposal tests whether online reward centering reduces sensitivity to this arbitrary reward origin.

### Agent And Update

Compare discounted Sarsa, reward-centered Sarsa, and differential Sarsa. The report should state the TD errors, average-reward baseline update, alpha, beta, gamma, epsilon, and how unshifted reward is logged separately from observed reward.

### Experiment Plan

Sweep reward shifts, seeds, step budgets, and eventually alpha/beta/gamma. A stronger version should include a midstream reward-origin change without resetting weights, because that better reflects continual operation.

### Metrics And Decision Rule

Metrics are unshifted average reward, Q norm, TD-error scale, reward_bar lag, accept rate, high-priority accept, and policy probes. The proposal succeeds if centered/differential methods keep value scale and behavior stable across shifts while discounted Sarsa does not.

### Fallback

If centered and differential Sarsa behave similarly, the honest conclusion is not that one method wins, but that average-reward-style removal of reward offsets is necessary for continuing agents.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/reward_centered_sarsa/report.md`. Current result: `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended`; older `results.md` fragments in this archive preserve pilot evidence only. This template is archived because the current report now states the continuing-control question, TD equations, evidence, and reproduction command.

Current status: main proposal. The result supports the claim that reward centering and differential Sarsa reduce reward-origin sensitivity in continuing access-control control, especially in value scale and unshifted reward stability.

Specific missing details before final submission: beta/gamma/alpha sensitivity, midstream reward-origin change, policy-invariance probes summarized as a table, and a clearer distinction between observed shifted reward and unshifted evaluation reward. The proposal would be weakened if discounted Sarsa matches centered variants after fair alpha retuning across reward shifts without value-scale instability.
