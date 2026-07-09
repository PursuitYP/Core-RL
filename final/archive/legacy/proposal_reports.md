# Proposal Reports

> Status note: this file is a legacy proposal-report draft from the initial minimal runs. Current final-facing evidence is indexed in `final/indexes/results.md`, and current gate decisions are in `final/archive/legacy/proposal_gate_review.md`. Paths to
> `*_minimal` runs below are preliminary/sanity evidence only.

This file records the early proposal set after initial implementation and refinement. It is kept only for audit history; the current proposal gate and result index supersede it.

## Portfolio Status

Primary proposals:

1. Reward-Centered Continuing Sarsa.
2. Output-Controlled TD.
3. Useful GVFs as Agent State.
4. Generate-and-Test Trace Features.
5. Options as Reusable Subtasks.
6. TIDBD Plasticity.
7. Baird Off-policy Stability.
8. Dyna Planning Budget.

Supporting diagnostics / fallbacks:

9. Centered TD Diagnostics.
10. GVF Question Design. 11. On-policy Stability Atlas. 12. Non-stationary Bandit. 13. Streaming Representation Diagnostic.

The supporting diagnostics are still implemented and runnable, but they should not all be presented as equally mature final projects.

## P1: Reward-Centered Continuing Sarsa

Working title: Reward-Centered Sarsa in Continuing Control.

What do we want to understand? Whether online reward centering removes irrelevant constant reward baselines from continuing discounted Sarsa, making learning curves, Q-value scale, and policy choice less sensitive to reward shifts.

Setting/testbed: Two-loop continuing MDP, with optional continuing gridworld extension.

What will we examine? Discounted Sarsa, reward-centered Sarsa, and differential Sarsa across reward shifts.

What will we look at? Unshifted average reward, policy choice at the decision state, Q norm, TD error, and reward baseline estimates.

Current implementation: `proposal_reward_centered_sarsa` in `experiments/alberta_core_rl/proposals.py`.

Latest result: `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T142324Z_minimal`

Figure: `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T142324Z_minimal/figures/avg_unshifted_reward_curve.png`

Interpretation focus: Do not report shifted reward as performance. The main claim is invariance to reward shifts, not merely higher observed reward.

## P2: Output-Controlled TD

Working title: Output-Controlled TD for Streaming Prediction.

What do we want to understand? Whether controlling prediction-output change makes online TD robust to feature scaling and trace magnitude.

Setting/testbed: Random walk prediction with one-hot features scaled by `one`, `ten`, `hundred`, and `uneven`.

What will we examine? Fixed TD, normalized TD, trace-normalized TD, and true-online TD(lambda).

What will we look at? RMSE, divergence indicator, weight norm, effective step-size, and prediction-change magnitude.

Current implementation: `proposal_output_controlled_td`.

Latest result: `experiments/alberta_core_rl/results/output_controlled_td/20260708T142128Z_minimal`

Figure: `experiments/alberta_core_rl/results/output_controlled_td/20260708T142128Z_minimal/figures/rmse_curve.png`

Interpretation focus: Normalized TD is the minimal linear intentional-update case. Trace-normalized TD should be described as a heuristic unless the full intentional trace formula is implemented.

## P3: Useful GVFs as Agent State

Working title: GVF Predictive State in a T-maze.

What do we want to understand? Whether learned GVF predictions can carry missing state information in a partially observable control problem.

Setting/testbed: T-maze cue task with aliased corridor observations.

What will we examine? Raw observation, short history, and raw observation plus learned GVF predictions.

What will we look at? Average reward, correctness at the junction, GVF TD error, and control TD error.

Current implementation: `proposal_useful_gvfs_state`.

Latest result: `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T142059Z_minimal`

Figure: `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T142059Z_minimal/figures/avg_reward_curve.png`

Interpretation focus: The report should ask whether predictions are useful as state, not only whether they are accurate.

## P4: Generate-and-Test Trace Features

Working title: Feature Generate-and-Test for Streaming Agent State.

What do we want to understand? Under a fixed feature budget, can utility-based replacement preserve useful traces when the reward delay changes?

Setting/testbed: Trace-conditioning stream with reward delay switching from 10 to 20.

What will we examine? Fixed trace bank vs utility-based generate-and-test trace replacement.

What will we look at? Absolute TD error around the delay switch, recovery time, replacement events, and active trace decay values.

Current implementation: `proposal_generate_test`.

Latest result: `experiments/alberta_core_rl/results/generate_test_features/20260708T142049Z_minimal`

Figure: `experiments/alberta_core_rl/results/generate_test_features/20260708T142049Z_minimal/figures/reward_curve.png`

Needed refinement: Plot `abs_error` instead of reward for final analysis.

## P5: Options as Reusable Subtasks

Working title: Doorway Options for Goal Transfer in Four Rooms.

What do we want to understand? When do doorway options help transfer across changing goals, and when do they hurt because of commitment cost?

Setting/testbed: Four Rooms with alternating goals.

What will we examine? Primitive Sarsa vs a minimal doorway-option controller.

What will we look at? Average reward per environment step, option duration, goal-change recovery, and option usage.

Current implementation: `proposal_options`.

Latest result: `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T142054Z_minimal`

Figure: `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T142054Z_minimal/figures/avg_reward_curve.png`

Needed refinement: The current option policy is a minimal hand-coded doorway option. The report must not imply autonomous option discovery.

## P6: TIDBD Plasticity

Working title: Per-feature Step-size Adaptation in Non-stationary TD.

What do we want to understand? Whether per-feature step-size adaptation tracks changing feature relevance in streaming TD.

Setting/testbed: Non-stationary synthetic sensor stream with relevant feature groups switching halfway.

What will we examine? Fixed TD, normalized TD, and TIDBD-lite.

What will we look at? Online TD error, recovery after the switch, mean feature step-size, and weight norm.

Current implementation: `proposal_tidbd_plasticity`.

Latest result: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T142244Z_minimal`

Figure: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T142244Z_minimal/figures/abs_td_error_curve.png`

## P7: Baird Off-policy Stability

Working title: Off-policy TD Stability on Baird's Counterexample.

What do we want to understand? Where semi-gradient off-policy TD becomes unstable, and whether a correction such as TDC is more stable.

Setting/testbed: Baird-style seven-state counterexample with linear features and zero rewards.

What will we examine? Off-policy TD and a small TDC implementation.

What will we look at? Weight norm, TD error, importance ratio, and divergence indicator.

Current implementation: `proposal_baird_offpolicy_stability`.

Latest result: `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T142244Z_minimal`

Figure: `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T142244Z_minimal/figures/weight_norm_curve.png`

Needed refinement: Validate the exact Baird feature/action specification against Sutton and Barto before using this as a final result.

## P8: Dyna Planning Budget

Working title: Compact Model-based Planning Without Replay.

What do we want to understand? How much a tiny learned model helps under a fixed per-step planning budget.

Setting/testbed: Continuing gridworld.

What will we examine? Q-learning with planning budgets 0, 1, and 5 model backups per real step.

What will we look at? Average reward, model size, Q norm, and performance per real environment step.

Current implementation: `proposal_dyna_planning_budget`.

Latest result: `experiments/alberta_core_rl/results/dyna_planning_budget/20260708T142244Z_minimal`

Figure: `experiments/alberta_core_rl/results/dyna_planning_budget/20260708T142244Z_minimal/figures/avg_reward_curve.png`

Constraint note: The model stores compact transition/reward estimates keyed by state-action, not a replay dataset of raw transitions.

## Supporting Analyses

Centered TD Diagnostics: Use as explanatory support for P1. Current result: `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T142039Z_minimal`

GVF Question Design: Use as support for P3. Current result: `experiments/alberta_core_rl/results/gvf_question_design/20260708T142049Z_minimal`

On-policy Stability Atlas: Use as support for P2. Current result: `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T142128Z_minimal`

Non-stationary Bandit: Keep as fallback or warm-up. Current result: `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T142051Z_minimal`

Streaming Representation Diagnostic: Needs reframing; current auxiliary shaping changes the task. Current result: `experiments/alberta_core_rl/results/streaming_representation/20260708T142059Z_minimal`
