# Reward-Centered Continuing Sarsa

Status: independent main proposal with completed main pilot and planned larger sweep.

## Abstract

This proposal studies a basic invariance requirement for continual reinforcement learning: in a continuing control task, adding a constant to every reward should not change the task-relevant behavior. Ordinary discounted action-value learning does not automatically respect this invariance because reward offsets appear in the scale of TD errors and action values. We test whether online reward centering and differential Sarsa reduce this arbitrary reward-origin sensitivity in a continuing access-control queue. The current main pilot shows that discounted Sarsa's action-value norm grows sharply as the reward shift increases, while reward-centered and differential variants keep the value scale much more stable and preserve unshifted reward. The study is not framed as "one algorithm scores higher"; it asks whether a continuing agent can learn in units that do not depend on an arbitrary reward baseline.


## Standalone Study Summary

This study tests reward-shift invariance in continuing control. The RL problem is the access-control queue: the agent observes server availability and customer priority, then accepts or rejects each customer while learning online. The implemented methods are discounted Sarsa, reward-centered Sarsa, and differential Sarsa with linear/tabular action values. The experiment varies constant reward shifts and measures unshifted reward, accept behavior, high-priority acceptance, reward baseline, TD error, and Q norm. The main evidence is that ordinary discounted Sarsa develops large reward-shift-dependent value scales, while centered and differential variants keep value norms and unshifted reward more stable. The next step is a longer seed/step sweep and alpha sensitivity analysis.

## Research Motivation

The Alberta Plan frames intelligence as a temporally uniform stream of experience: the agent is always acting, always learning, and not periodically reset into a special training phase. In that setting, reward origin is an especially clean stress test. If every reward is translated by a constant, the preference ordering of policies in an average-reward continuing task should not change. A long-lived agent should therefore not require a new step size or a new representation merely because an engineer redefined the zero point of the reward sensor.

Discounted value methods can violate this practical invariance. With gamma near one, a constant reward shift contributes a large constant component to the value function. That component is not useful for choosing actions, but it changes TD-error magnitudes, value norms, and sometimes behavior through function approximation and finite step-size effects. Reward centering is attractive because it is small, online, and compatible with the course constraints: no replay buffer, no deep network, and no offline fitting.

## Research Question

Does online reward centering make Sarsa robust to constant reward shifts in a non-episodic continuing control task?

The precise hypothesis is:

> Reward-centered Sarsa and differential Sarsa should show lower variation in value scale and unshifted task reward across reward shifts than ordinary discounted Sarsa.

This hypothesis is about invariance and learning dynamics, not about final shifted return. All primary results therefore report unshifted reward separately from the shifted reward observed by the learner.

## Alberta Plan Connection

This proposal targets several Alberta Plan themes:

- continuing problems rather than episodic reset tasks;
- value functions as central predictive/control quantities;
- average-reward thinking for long-lived agents;
- online adaptation from ordinary experience;
- small mechanisms that reduce sensitivity to hand-tuned scales.

The task is deliberately not deep RL. The point is to inspect a Core RL mechanism with enough transparency that value-scale failures can be explained.

## Related Work

The main source is Reward Centering, which shows that subtracting an empirical average reward improves continuing discounted methods and removes constant reward-shift sensitivity. Average-reward RL and the access-control queue provide the canonical setting. Bellman Error Centering gives a more recent theoretical lens on related centered fixed points. The Alberta Plan supplies the broader motivation for continuing agents and temporal uniformity.

Local references:

- `resources/alberta_plan_related/reward_centering_2405.09999.pdf`
- `resources/alberta_plan_related/bellman_error_centering_2502.03104.pdf`
- `resources/alberta_plan_related/average_reward_learning_planning_2006.16318.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

## Environment

The main environment is an access-control queue. The agent observes:

- number of free servers;
- priority class of the current customer.

The agent chooses:

- reject;
- accept if a server is free.

The unshifted reward is the accepted customer's priority, or zero for rejection. The experimental observed reward is:

`observed_reward = unshifted_reward + reward_shift`.

This creates several equivalent descriptions of the same decision problem. The agent must learn online from a single stream with no replay.

## Methods

The study compares three on-policy control agents:

- Discounted Sarsa with gamma `0.99`.
- Reward-centered discounted Sarsa with an online average-reward estimate.
- Differential Sarsa with gamma `1.0` and average-reward correction.

All methods use tabular one-hot state features, epsilon-greedy behavior, and one update per environment step. Reward centering updates an average reward estimate online and subtracts that estimate from the immediate reward term. Differential Sarsa uses the average-reward style TD error.

The update details are deliberately kept explicit because the proposal is about the unit of the learning signal. Ordinary discounted Sarsa uses `delta = R_{t+1} + gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)`. Reward-centered Sarsa uses `delta = (R_{t+1} - r_bar_t) + gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)` with an online baseline update `r_bar <- r_bar + beta (R_{t+1} - r_bar)`. Differential Sarsa uses the average-reward form `delta = R_{t+1} - r_bar_t + Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)` and updates the reward baseline from the same continuing stream. The report logs observed shifted reward and unshifted task reward separately, so the evaluation is not accidentally rewarding the algorithm for seeing a larger arbitrary constant.

## Experimental Design

Current main pilot:

- Environment: access-control queue.
- Reward shifts: `-4`, `0`, `4`, `8`.
- Seeds: `0-4`.
- Steps: `5000` per condition.
- Algorithms: discounted Sarsa, reward-centered Sarsa, differential Sarsa.
- Result path: `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main`.

Primary metrics:

- unshifted average reward;
- Q norm;
- TD-error scale;
- reward-bar estimate;
- accept rate;
- simple policy probes.

The decision rule is: a method supports the hypothesis only if it preserves unshifted reward and policy probes while keeping Q norm and TD-error scale approximately invariant across reward shifts. A method that earns high shifted reward but changes behavior, explodes in value norm, or needs a different alpha for each shift does not count as solving the continuing reward-origin problem.

Planned extended CPU sweep:

- Reward shifts: `-8`, `-4`, `0`, `4`, `8`.
- Seeds: `0-19`.
- Steps: `20000` per condition.
- Additional sensitivity target: alpha `0.01`, `0.03`, `0.05`, `0.1` and beta `0.003`, `0.01`, `0.03`.
- Nonstationary extension: switch reward origin midway through a single stream without resetting weights, then measure reward-bar lag and recovery window.

The primary figure is:

![Access-control unshifted reward under reward shifts.](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main/figures/avg_unshifted_reward_by_algorithm-reward_shift_curve.png)

## Results

The main result is value-scale invariance. Discounted Sarsa's Q norm grows strongly with the reward shift: about `60.17 +/- 1.89` at shift `-4` and about `344.59 +/- 15.3` at shift `8`. This is not useful task knowledge; it is largely the arbitrary value offset induced by the shifted reward stream.

Reward-centered Sarsa keeps Q norm near `20-22` across tested shifts. Differential Sarsa shows the same qualitative scale-stability pattern. Unshifted reward for reward-centered Sarsa remains around `2.47-2.54` across reward shifts in the current pilot, while ordinary discounted Sarsa degrades at positive shifts.

The key interpretation is that reward centering removes most of the nuisance component of the TD target. It does not change the environment or provide extra samples; it changes the learning signal so that the learner focuses on reward deviations rather than reward origin.

## Analysis

The result should be read as an invariance test. If a method is robust, changing reward origin should not greatly affect value scale or unshifted behavior. Discounted Sarsa fails this test in the current pilot. Reward-centered and differential variants pass it more closely.

The differential baseline is important. If differential Sarsa performs similarly to reward centering, the conclusion is not that reward centering uniquely solves the problem. The stronger and more honest conclusion is that average-reward-style removal of reward offsets is a necessary design idea for continuing agents. Reward centering is one practical route that preserves a discounted method structure.

## Threats To Validity

The current pilot uses five seeds and a compact step budget. It is enough to establish the mechanism, but a high-confidence course-paper version should use more seeds and longer runs.

The environment is canonical but still small and tabular. That is appropriate for Core RL mechanism analysis, but claims should not be generalized to deep agents or large robotics tasks.

The beta step size for the average reward estimator is not fully swept. A slow estimator may lag under nonstationary rewards; a fast estimator may inject variance.

Reward shifts are constant. A stronger study should include midstream reward-origin changes without resetting the agent.

## Reviewer Critique And Revisions

Sutton-style critique:

- The report must not claim episodic return improvements; it must focus on continuing invariance and average-reward reasoning.

Experimental critique:

- Five seeds are a pilot, not a final statistical sweep.

Baseline critique:

- Differential Sarsa is a serious competitor, not an appendix baseline.

Revision already made:

- The initial two-loop MDP was replaced by access-control for the main claim.
- Shifted observed reward and unshifted task reward are logged separately.

Next required revision:

- Run a longer sweep with seeds `0-19`, beta/gamma ablations, and midstream reward-shift changes.

## Conclusion

Reward centering is a strong independent proposal because it asks a clean continuing-RL question and has interpretable evidence. The current result supports the claim that ordinary discounted Sarsa is reward-origin sensitive, while reward-centered and differential variants are far more stable. The next stage should enlarge the seed count and add nonstationary reward-origin changes so the proposal reaches full paper strength.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_main.json
```

Longer seed/step sweep:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_extended.json
```
