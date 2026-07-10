# Reward-Centered Continuing Sarsa

Status: independent main proposal with completed extended reward-shift/alpha sweep and completed beta/gamma/no-reset reward-origin switch sweep. The strongest claim is reward-origin invariance and value-scale control in an access-control continuing stream, not a universal reward-centering solution.

## Abstract

This proposal studies a basic invariance requirement for continual reinforcement learning: in a continuing control task, adding a constant to every reward should not change the task-relevant behavior. Ordinary discounted action-value learning does not automatically respect this invariance because reward offsets appear in the scale of TD errors and action values. We test whether online reward centering and differential Sarsa reduce this arbitrary reward-origin sensitivity in a continuing access-control queue. The extended run shows that discounted Sarsa's action-value norm grows sharply across reward shifts and alphas, while reward-centered and differential variants keep value scale much more stable and preserve unshifted reward. The study is not framed as "one algorithm scores higher"; it asks whether a continuing agent can learn in units that do not depend on an arbitrary reward baseline.


## Standalone Study Summary

This study tests reward-shift invariance in continuing control. The RL problem is the access-control queue: the agent observes server availability and customer priority, then accepts or rejects each customer while learning online. The implemented methods are discounted Sarsa, reward-centered Sarsa, and differential Sarsa with linear/tabular action values. The experiment varies constant reward shifts and measures unshifted reward, accept behavior, high-priority acceptance, reward baseline, TD error, and Q norm. The main fixed-condition evidence is a 20-seed, 20000-step alpha sweep: ordinary discounted Sarsa develops large reward-shift-dependent value scales, while centered and differential variants keep value norms and unshifted reward more stable. The completed second-round experiment tests beta/gamma sensitivity under a no-reset reward-origin switch inside one continuing stream and strengthens the same mechanism claim within this access-control setting: centered and differential variants keep post-late reward high while discounted Sarsa can carry a large nuisance value scale.

## Proposal Template Answers

Focused RL question: In an online continuing control task, can an agent learn action values whose scale and behavior are insensitive to an arbitrary constant added to every reward? The question is not whether reward-centered Sarsa has the highest shifted return, but whether the learning dynamics respect the reward-origin invariance expected in an average-reward continuing problem.

Setting and testbed: The testbed is the access-control queue from tabular continuing RL. It is larger and more meaningful than a two-state diagnostic because it has state-dependent action feasibility, priority-dependent rewards, and a real accept/reject control tradeoff, while still being interpretable enough to audit TD errors and value norms.

Implemented comparison: The implemented comparison is discounted Sarsa versus reward-centered Sarsa versus differential Sarsa, all trained online from a single stream with no replay buffer and no deep network. The first completed run varies reward shift and alpha across separate streams. The second completed run varies beta, gamma, alpha, switch direction, and midstream reward-origin changes without resetting the learner.

Observation or figure that answers the question: The main figures must jointly show unshifted reward, Q norm, high-priority acceptance, and divergence as a function of reward shift. The proposal is supported only if centered methods maintain behavior while preventing value-scale inflation; a reward-only table would not answer the invariance question.

Compute need and fallback: Both CPU-scale sweeps are now complete. The honest fallback is no longer "switching remains future work"; instead, the limitation is that the switch experiment uses a controlled access-control stream and does not yet include full statewise policy-distance probes or larger continuing tasks.

## Independent Research Scope

This proposal is an independent study of reward-origin invariance in continuing control. It deliberately does not claim to solve all continuing average-reward learning, all reward shaping, or all nonstationarity. Its scope is narrower and sharper: a constant reward translation should not force a retuned step size, distorted value scale, or changed accept/reject behavior in access-control Sarsa.

The study includes both mechanism-level measurements and control-level measurements. The value-scale, TD-error, reward-baseline, policy-probe, and accept-rate diagnostics form a single evidence chain for the reward-origin invariance claim.

## Evidence Level

Evidence level: strong independent main-candidate evidence with two completed sweeps. The fixed-condition result uses 20 seeds, 20000 online steps per condition, five reward shifts, three alphas, and three algorithms. The no-reset switch result uses 10 seeds, 20000 online steps, 1575 condition groups, and 8,112,150 logged rows. Together they support the claim that ordinary discounted Sarsa is reward-origin sensitive, while centered and differential variants are much less sensitive in both fixed-origin and midstream reward-origin switch settings.

The evidence still has boundaries. The switch sweep shows post-switch recovery under controlled reward-origin changes, but it does not prove one universally optimal beta or gamma. It also does not yet report full policy-distance probes across all access-control states. The final claim should therefore remain an invariance and value-scale claim, not a general theorem that reward centering solves all nonstationary continuing control.

## Paper-Style Contribution And Claim Boundaries

This report's contribution is a controlled invariance analysis for continuing control. It formulates reward-origin sensitivity as a Core RL question, implements the access-control queue as an interpretable continuing testbed, and separates task reward from the arbitrary reward signal observed by the learner. The most important empirical contribution is not that reward-centered Sarsa has a higher average in one table; it is that centered and differential updates keep value scale, TD-error scale, and behavior substantially more stable across reward translations.

The claim boundary is equally important. The report does not prove that reward centering is always preferable to differential methods, nor that a single beta works under all nonstationarity. The academically defensible claim is narrower: in the tested continuing access-control streams, average-reward-style removal of reward offsets is the only tested design family that consistently produces practical reward-origin invariance, while ordinary discounted Sarsa encodes a large nuisance value component.

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

Current extended sweep:

- Environment: access-control queue.
- Reward shifts: `-8`, `-4`, `0`, `4`, `8`.
- Alphas: `0.02`, `0.05`, `0.1`.
- Seeds: `0-19`.
- Steps: `20000` per condition.
- Algorithms: discounted Sarsa, reward-centered Sarsa, differential Sarsa.
- Result path: `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended`.

Primary metrics:

- unshifted average reward;
- Q norm;
- TD-error scale;
- reward-bar estimate;
- accept rate;
- simple policy probes.

The decision rule is: a method supports the hypothesis only if it preserves unshifted reward and policy probes while keeping Q norm and TD-error scale approximately invariant across reward shifts. A method that earns high shifted reward but changes behavior, explodes in value norm, or needs a different alpha for each shift does not count as solving the continuing reward-origin problem.

Second-round sensitivity extension:

- Proposal runner: `reward_centered_sarsa_sensitivity`.
- Smoke result: `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T084151Z_smoke`.
- Extended CPU task: `core-rl-reward-sensitivity-extended-rerun-28457861`.
- Extended result: `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended`.
- Extended config: `experiments/alberta_core_rl/configs/reward_centered_sarsa_sensitivity/config_extended.json`.
- Design: reward-origin switches occur halfway through one continuing access-control stream without resetting weights; the sweep varies beta, gamma, alpha, switch direction, and algorithm.
- Primary additional metrics: post-switch unshifted reward, accept rate, reward-bar absolute tracking error, Q norm, divergence, and recovery window.

The report-ready sensitivity figures below use the completed extended result. The reward heatmap is the primary view. The divergence heatmap is not used as a primary figure because every condition has zero divergence; the important failure is value-scale inflation, not numerical crash.

The compact switch table below is the primary reading aid for the dense sensitivity heatmaps. For each no-reset reward-origin switch, it reports the best reward-centered and differential post-late condition, plus the best and worst discounted-Sarsa conditions. This makes the mechanism visible without asking the reader to inspect all beta/gamma/alpha cells. Centered and differential variants keep post-late reward in a narrow high range with Q norms around tens, while discounted Sarsa can either recover under favorable low-gamma settings or carry a much larger nuisance Q scale under unfavorable settings.

| Switch type | Best reward-centered condition | Best differential condition | Best discounted condition | Weak discounted condition | Interpretation |
|---|---|---|---|---|---|
| Down-shift | `alpha=0.05`, `beta=0.001`, `gamma=0.97`: reward `2.636 +/- 0.028`, Q `41.1` | `alpha=0.05`, `beta=0.001`: reward `2.634 +/- 0.016`, Q `41.1` | `alpha=0.1`, `gamma=0.9`: reward `2.447 +/- 0.031`, Q `263.8` | `alpha=0.02`, `gamma=0.99`: reward `1.581 +/- 0.221`, Q `290.6` | Centering and differential updates recover high reward; discounted Sarsa is sensitive to gamma and alpha. |
| Sign-shift | `alpha=0.05`, `beta=0.1`, `gamma=0.99`: reward `2.609 +/- 0.027`, Q `28.0` | `alpha=0.05`, `beta=0.001`: reward `2.592 +/- 0.025`, Q `87.9` | `alpha=0.1`, `gamma=0.9`: reward `2.580 +/- 0.037`, Q `480.4` | `alpha=0.1`, `gamma=0.99`: reward `1.834 +/- 0.256`, Q `862.5` | Discounted Sarsa can match reward only with much larger value scale in favorable settings. |
| Up-shift | `alpha=0.1`, `beta=0.03`, `gamma=0.99`: reward `2.606 +/- 0.027`, Q `32.3` | `alpha=0.1`, `beta=0.03`: reward `2.598 +/- 0.017`, Q `30.0` | `alpha=0.1`, `gamma=0.9`: reward `2.410 +/- 0.065`, Q `507.1` | `alpha=0.05`, `gamma=0.97`: reward `2.093 +/- 0.129`, Q `634.1` | Reward centering avoids storing the positive offset as a large action-value component. |

![Post-late unshifted reward under beta/gamma/no-reset reward-origin switches.](sensitivity_figures/report_reward_sensitivity_reward.png)

![Post-late reward-baseline tracking error under beta/gamma/no-reset reward-origin switches.](sensitivity_figures/report_reward_sensitivity_bar_error.png)

![Post-late Q norm under beta/gamma/no-reset reward-origin switches.](sensitivity_figures/report_reward_sensitivity_q_norm.png)

The recovery-AUC follow-up directly analyzes the completed sensitivity run's `metrics.csv` instead of rerunning a smaller pilot. For each seed and condition, the early recovery score is the mean `avg_unshifted_reward` during the first `1000` logged steps after the reward-origin switch. This view asks a stricter continual-learning question than the post-late table: after the reward sensor changes and the learner is not reset, which family recovers useful task reward quickly without carrying a large arbitrary value offset?

![Best early post-switch recovery score by algorithm family.](sensitivity_figures/report_reward_recovery_auc_best_by_family.png)

![Early post-switch accept behavior by algorithm family.](sensitivity_figures/report_reward_recovery_accept_best_by_family.png)

| Switch type | Discounted best early score / Q norm | Reward-centered best early score / Q norm | Differential best early score / Q norm | Interpretation |
|---|---|---|---|---|
| Down-shift | `2.025 +/- 0.126` / `480.7` | `2.549 +/- 0.049` / `24.7` | `2.517 +/- 0.032` / `23.5` | Centered and differential methods recover much more reward while keeping value scale small. |
| Sign-shift | `2.535 +/- 0.060` / `88.4` | `2.583 +/- 0.041` / `59.9` | `2.573 +/- 0.043` / `85.9` | Discounted Sarsa can recover early reward under favorable gamma, but the value scale is still larger. |
| Up-shift | `2.378 +/- 0.050` / `183.0` | `2.580 +/- 0.068` / `76.5` | `2.557 +/- 0.039` / `33.7` | The positive-offset switch exposes the nuisance-value problem most clearly. |

The report-ready figures below use seed-tail condition summaries rather than dense learning-curve overlays. They show reward, value scale, behavior, and divergence separately, which is the right evidence for an invariance claim.

## Experiment Design Rationale

The environment, variables, and metrics were chosen to separate three explanations that a skeptical reviewer would otherwise conflate. First, unshifted reward and high-priority acceptance test task behavior rather than the shifted scalar reward observed by the learner. Second, Q norm and TD-error scale test whether the learner has encoded an arbitrary reward offset as a large value component. Third, divergence and policy probes test whether the effect is merely cosmetic or can change actual control. The access-control queue is therefore not being used as a benchmark leaderboard; it is being used as a controlled continuing system in which reward-origin invariance can be measured.

The grids are deliberately targeted rather than blind. Reward shifts `-8` through `8` are large relative to access-control priorities, so they stress the nuisance value offset. The alpha grid includes settings where ordinary Sarsa still learns and settings where value-scale inflation becomes severe. The sensitivity extension then targets three causal gaps: beta controls baseline lag, gamma controls discounted offset amplification, and a midstream shift tests continual recovery without resetting weights.

![Tail unshifted reward under reward shifts and alpha values.](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended/figures/report_avg_unshifted_reward_by_reward_shift.png)

![Tail action-value norm under reward shifts and alpha values.](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended/figures/report_q_norm_by_reward_shift.png)

![Tail high-priority accept rate under reward shifts and alpha values.](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended/figures/report_high_priority_accept_by_reward_shift.png)

![Divergence rate under reward shifts and alpha values.](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended/figures/report_diverged_by_reward_shift.png)

## Results

The main result is value-scale invariance under a larger seed and alpha sweep. Discounted Sarsa's Q norm grows strongly with reward shift and alpha: at shift `8`, alpha `0.1`, its tail Q norm is about `1875.55 +/- 38.4`, and its unshifted reward is about `1.697 +/- 0.147`. This is not useful task knowledge; it is largely the arbitrary value offset induced by the shifted reward stream.

Reward-centered Sarsa keeps Q norm much smaller, roughly `22-35` across the tested reward shifts and alphas, with zero divergence. Its unshifted reward remains around `2.55-2.60` across reward shifts. Differential Sarsa shows the same qualitative scale-stability pattern, with unshifted reward around `2.55-2.61` and similarly modest Q norms. Ordinary discounted Sarsa degrades under large positive and negative shifts, especially at higher alpha.

The high-priority accept-rate figure is included to guard against a misleading reward-only interpretation. Reward centering is not counted as successful merely because it improves a scalar average; it must also preserve the task-relevant accept/reject tendency under reward translations. The divergence panel is mostly a consistency check for this run, but it makes explicit that the key difference is value-scale inflation rather than many hard numerical crashes.

The key interpretation is that reward centering removes most of the nuisance component of the TD target. It does not change the environment or provide extra samples; it changes the learning signal so that the learner focuses on reward deviations rather than reward origin.

The completed no-reset sensitivity sweep strengthens the continual-learning claim. It writes standard artifacts at `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended`, with 10 seeds, 20000 steps, and 1575 condition groups. No condition records divergence. Post-late results show reward-centered Sarsa remains high across beta/gamma/switch settings: the best post-late average unshifted reward is `2.6364 +/- 0.0280` for reward-centered Sarsa with `alpha=0.05`, `beta=0.001`, `gamma=0.97` on a down-shift; the best sign-shift setting is reward-centered Sarsa with `alpha=0.05`, `beta=0.1`, `gamma=0.99`, mean `2.6089 +/- 0.0274`; the best up-shift setting is reward-centered Sarsa with `alpha=0.1`, `beta=0.03`, `gamma=0.99`, mean `2.6057 +/- 0.0273`. Differential Sarsa is a close average-reward baseline, with `2.6338 +/- 0.0155` in the best down-shift condition. Discounted Sarsa is less robust, especially under down-shifts; one poor post-late condition reaches only `1.5814 +/- 0.2210`.

The recovery analysis adds a stricter early-window view. In the first `1000` logged steps after the switch, the best reward-centered condition reaches early recovery scores `2.549 +/- 0.049`, `2.583 +/- 0.041`, and `2.580 +/- 0.068` for down-, sign-, and up-shifts. The corresponding best discounted scores are `2.025 +/- 0.126`, `2.535 +/- 0.060`, and `2.378 +/- 0.050`. Discounted Sarsa can be competitive on sign-shift reward under a favorable gamma, but its early Q norm remains larger than the centered variant. The down- and up-shift results strengthen the central mechanism claim: centering is not only a late-value-scale fix; it preserves useful reward during early no-reset adaptation.

The accept-behavior recovery figure is a guard against a reward-only story. Down-shift early accept rates are higher for reward-centered and differential variants (`0.527 +/- 0.013` and `0.531 +/- 0.009`) than for discounted Sarsa (`0.493 +/- 0.024`), matching the reward-recovery result. In the up-shift case discounted Sarsa has a higher early accept rate (`0.543 +/- 0.013`) but lower early reward, which shows that crude acceptance frequency is not enough; the learner must accept the right priority classes under the new reward origin. Full statewise policy-distance probes remain the better final behavior diagnostic, but this behavior-side summary reduces the risk that the recovery result is only a value-scale artifact.

The switch sweep also clarifies the mechanism. Discounted Sarsa can avoid formal divergence while still carrying a huge nuisance value scale: high-gamma, high-alpha up-shift conditions have post-late Q norms around `1339-1354`. This is why the report treats Q norm as a primary diagnostic. A method that does not diverge but stores the arbitrary reward origin as a large value offset has not solved reward-origin invariance.

## Analysis

The result should be read as an invariance test. If a method is robust, changing reward origin should not greatly affect value scale or unshifted behavior. Discounted Sarsa fails this test in the extended sweep. Reward-centered and differential variants pass it much more closely.

The differential baseline is important. If differential Sarsa performs similarly to reward centering, the conclusion is not that reward centering uniquely solves the problem. The stronger and more honest conclusion is that average-reward-style removal of reward offsets is the effective design idea in these tested continuing streams. Reward centering is one practical route that preserves a discounted method structure.

## Threats To Validity

The fixed-condition extended result uses 20 seeds and 20000 steps, and the sensitivity result adds beta, gamma, and no-reset reward-origin switches with 10 seeds. The early recovery score now reduces one gap, but it is still based on logged points rather than full per-step integration. A high-confidence course-paper version should still add full statewise policy-distance probes and a paired-seed recovery analysis that compares methods under identical behavior-stream randomness.

The environment is canonical but still small and tabular. That is appropriate for Core RL mechanism analysis, but claims should not be generalized to deep agents or large robotics tasks.

The beta step size for the average reward estimator is now swept over a useful range, but the result does not prove a universal beta. A slow estimator may lag under different nonstationarity; a fast estimator may inject variance in noisier tasks.

Reward-origin switches are now tested midstream without reset, but the switches are controlled and synthetic. A stronger continual study should include natural reward-sensor drift or state-dependent reward offsets.

## Reviewer Critique And Revisions

Sutton-style critique:

- The report must not claim episodic return improvements; it must focus on continuing invariance and average-reward reasoning.

Experimental critique:

- The first five-seed pilot was not enough for final statistical claims; this has been addressed with a 20-seed extended sweep.

Baseline critique:

- Differential Sarsa is a serious competitor, not a weak secondary baseline.

Revision already made:

- The initial two-loop MDP was replaced by access-control for the main claim.
- Shifted observed reward and unshifted task reward are logged separately.

Next required revision:

- Add full statewise policy-distance probes between fixed-origin and switched-origin settings.
- Add a stricter paired-seed recovery analysis under matched behavior-stream randomness; the current early recovery score is useful but not yet a paired causal comparison.
- Add statewise policy-distance probes to ensure similar unshifted reward does not hide different accept/reject behavior.

Reviewer Audit Matrix:

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| Alberta Plan | The study must be about continual ordinary experience, not episodic score. | Uses a continuing access-control stream, reports unshifted task reward separately from observed reward, and includes a completed midstream reward-origin switch sweep. | Natural reward drift is still untested. |
| Average-reward RL | Discounted Sarsa is not the only relevant baseline. | Adds differential Sarsa as a serious average-reward baseline and reports the completed beta/gamma switch sweep. | Differential and centered variants remain close; the report should frame both as average-reward-style offset removal. |
| Statistics | Five seeds were insufficient. | Completed a 20-seed extended sweep. | Confidence intervals are tail summaries; AUC and paired seed effects would strengthen the report. |
| Mechanism | Reward improvements alone could hide behavior changes. | Adds Q norm, high-priority acceptance, accept rate, and divergence figures. | Full policy-distance probes over all states are not yet reported. |
| Strict instructor | The proposal should not overclaim a universal reward-centering solution. | Conclusion is limited to reward-origin invariance in access-control Sarsa, now with completed fixed-origin and no-reset switch evidence. | Larger continuing environments would be needed for a broader claim. |

## Conclusion

Reward centering is a strong independent proposal because it asks a clean continuing-RL question and now has both fixed-condition and no-reset switch evidence. The results support the claim that ordinary discounted Sarsa is reward-origin sensitive, while reward-centered and differential variants are far more stable across reward shifts, alphas, beta/gamma settings, and midstream reward-origin switches. The conclusion remains bounded: average-reward-style removal of reward offsets is the effective mechanism among tested variants for practical reward-origin invariance in this access-control setting, but it is not a universal solution for every form of nonstationarity.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_main.json
```

Extended seed/step sweep:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_extended.json
```

Regenerate the report figures:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind reward-centered \
  --result-dir experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended
```

Second-round sensitivity extended sweep:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa_sensitivity/config_extended.json

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind reward-sensitivity \
  --result-dir experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended \
  --figure-dir final/reports/proposals/reward_centered_sarsa/sensitivity_figures

PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/core-rl-pycache MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/analyze_reward_recovery.py \
  --result-dir experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended \
  --out-dir final/reports/proposals/reward_centered_sarsa/sensitivity_figures
```
