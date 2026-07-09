# Reward Centering, Output-Controlled Prediction, and Model Staleness in Small Streaming RL

Author: Core RL Course Project

Status: historical overview report version, 2026-07-09

Update note, later 2026-07-09: the user clarified that every proposal must be treated as an independent research topic. This overview remains useful context, but the current canonical materials are the independent reports in `final/reports/proposals/` and the three large independent proposals in `final/reports/integrated/`.

Scope note: this is a portfolio overview paper. Standalone proposal reports, result summaries, and reproduction commands are in `final/reports/proposals/<proposal>/`.

## Abstract

This project studies small online reinforcement-learning mechanisms motivated by the Alberta Plan: reward normalization in continuing control, output-controlled temporal difference prediction, and limited model-based planning under nonstationarity. The project intentionally avoids replay buffers and deep networks. All agents learn from a single stream of experience using tabular or linear function approximation.

This historical overview was originally organized around a narrow reward/prediction thread. First, in a continuing access-control queue, reward-centered Sarsa and differential Sarsa remain stable under constant reward shifts, while ordinary discounted Sarsa develops large value scales and degraded unshifted reward at positive shifts. Second, in a tile-coded random-walk prediction problem, normalized and trace-normalized TD are robust to feature-scale changes, while fixed-step TD and the current true-online TD(lambda) baseline diverge in several large-scale or high-alpha conditions. A compact third diagnostic studies Dyna planning after a layout change: planning improves pre-change reward, but keeping an obsolete learned model causes high stale-backup rates and can hurt recovery. Additional proposal diagnostics are reported honestly as negative or supporting results: a GVF predictive-state design fails even though a cheap trace-memory baseline solves the task; generate-and-test feature replacement finds closer trace timescales but does not improve prediction error; TIDBD-lite adapts feature step sizes but does not beat normalized TD on error.

The main lesson is not that one algorithm wins a benchmark. The stronger conclusion is that small continual agents need normalization and diagnostic metrics that respect the quantities that matter in a stream: reward baselines, prediction-output change, value scale, recovery after change, and stale computation.

## 1. Research Motivation

The Alberta Plan frames intelligence as continual learning from ordinary experience. In that setting, the agent is not repeatedly reset into a clean episodic benchmark, and the learning problem is not only to maximize a final score. A long-lived agent must keep its updates numerically stable, preserve useful knowledge under changes, and allocate limited computation while it continues acting.

This project focuses on Core RL rather than embodied RL or LLM/agentic RL. It uses small environments and linear or tabular methods so that failures can be inspected. The project also follows two course constraints:

- No replay buffer is used.
- No deep network is used.

The motivating question is:

> Which small online RL mechanisms make a continual agent more robust to reward shifts, feature-scale changes, and stale model knowledge?

This broad question was decomposed into proposal-level questions. In this historical overview version, multi-role critique pruned the project into a narrow main thread plus supporting diagnostics, because treating all initial proposals as equal would have produced a shallow catalog rather than a focused overview.

## 2. Research Questions

### RQ1: Reward Centering in Continuing Control

What do we want to understand?

Can online reward centering make continuing Sarsa robust to arbitrary constant reward shifts?

Why it matters:

In a continuing task, adding a constant to all rewards should not change which behavior is good, but it can change the scale of discounted action values and TD errors. A continual agent should not become fragile merely because the reward origin is shifted.

### RQ2: Output-Controlled TD Under Feature Scaling

What do we want to understand?

Can controlling the size of the prediction-output change make streaming TD less sensitive to feature scale than controlling raw parameter movement with a fixed alpha?

Why it matters:

In linear function approximation, feature scaling changes how a fixed parameter step affects the prediction. A constant alpha is therefore not a stable unit of learning progress across representations. The Alberta Plan emphasizes simple, continual, value-function learning; output-level update control is a small mechanism in that spirit.

### RQ3: Model-Based Planning Under Nonstationarity

What do we want to understand?

When a continuing Dyna-style agent has a small learned model and a fixed planning budget, does planning help adaptation after the environment changes, or does stale model knowledge hurt recovery?

Why it matters:

The Alberta Plan gives learned models and planning an important role. In a continual stream, however, a learned model is not guaranteed to remain valid. The interesting question is not whether planning helps in a stationary grid, but how model-based computation behaves when the world changes.

### Supporting Questions

The project also implemented and evaluated several candidate proposals that are not promoted to the main story:

- GVF predictive state: can learned predictions supply missing state information in a partially observable control task?
- Generate-and-test traces: can a feature utility mechanism preserve useful prediction timescales after a delay change?
- TIDBD-lite plasticity: can per-feature step-size adaptation track changing feature relevance?
- Baird off-policy stability: where does off-policy semi-gradient TD fail?
- Doorway options: do hand-coded options help under environment-step accounting?

These supporting studies are used to guide future work and to prevent overclaiming.

## 3. Related Work and Alberta Plan Lens

The main conceptual source is the Alberta Plan, which argues for a long-term research path centered on continual learning, value functions, learned models, planning, and temporally uniform experience. This project uses that lens but stays deliberately small.

Reward centering is informed by recent work on centering rewards and Bellman errors in continuing reinforcement learning. Average-reward access-control is a standard continuing control example and gives a more meaningful testbed than a two-loop toy MDP.

Output-controlled TD is motivated by work on intentional updates and streaming RL. The core idea used here is small and linear: normalize updates by the feature or trace magnitude so that the same alpha corresponds more closely to a prediction-output change rather than a raw parameter displacement.

GVFs, Horde-style prediction, online agent-state construction, and feature generation are natural Alberta Plan directions. The current experiments show that these ideas are promising but easy to implement badly: a GVF that is accurate or stable is not automatically useful state, and a feature replacement rule that finds a more plausible timescale is not automatically better on prediction error.

## 4. Methods

### 4.1 Shared Experimental Protocol

All main experiments use the same basic protocol:

- Online stream interaction, one update per environment step.
- No replay buffer, no stored dataset, no offline training loop.
- No deep networks.
- Five seeds for current main runs.
- Metrics summarized by condition using seed-aware tail means and 95 percent normal confidence intervals.
- Each result directory contains `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, and `manifest.json`.

The current summary schema is `seed_tail_v1`. Final claims use `*_seed_tail` statistics from `condition_summary.json`.

### 4.2 Study 1: Reward-Centered Continuing Sarsa

Setting:

- Environment: continuing access-control queue.
- State: number of free servers and current customer priority.
- Actions: accept or reject.
- Reward: priority value if accepted, zero otherwise, plus an experimental constant reward shift.
- Objective: good continuing control measured by unshifted reward and stable value scale.

Compared algorithms:

- Discounted Sarsa.
- Reward-centered Sarsa.
- Differential Sarsa.

Experimental variation:

- Reward shifts: `-4`, `0`, `4`, `8`.
- Seeds: `0` to `4`.
- Steps: `5000` per condition in the current main run.

Primary metrics:

- Unshifted average reward.
- Q norm.
- TD error scale.

Result path:

`experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main`

Main figure:

`experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main/figures/avg_unshifted_reward_by_algorithm-reward_shift_curve.png`

![Figure 1. Access-control unshifted reward under reward shifts.](../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main/figures/avg_unshifted_reward_by_algorithm-reward_shift_curve.png)

### 4.3 Study 2: Output-Controlled TD

Setting:

- Environment: large random-walk prediction task.
- Representation: overlapping tile features.
- Objective: predict value under streaming transitions.

Compared algorithms:

- Fixed-step TD.
- Normalized TD.
- Trace-normalized TD(lambda).
- True-online TD(lambda) baseline.

Experimental variation:

- Feature scales: `one`, `ten`, `hundred`, `uneven`.
- Alphas: `0.03`, `0.1`, `0.3`.
- Lambda: `0.8` for trace methods, `0.0` for non-trace methods.
- Seeds: `0` to `4`.
- Steps: `5000` per condition in the current main run.

Primary metrics:

- RMSE across random-walk states.
- Divergence flag.
- Weight norm.
- Prediction-change magnitude.

Result path:

`experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`

Main figure:

`experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main/figures/rmse_by_algorithm-scale-alpha_curve.png`

![Figure 2. Tile-random-walk RMSE by algorithm, feature scale, and alpha.](../../../experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main/figures/rmse_by_algorithm-scale-alpha_curve.png)

### 4.4 Diagnostic Study: Dyna Planning Budget

Setting:

- Environment: continuing gridworld.
- Change: midway goal/hazard layout shift.
- Agent: Q-learning with a compact state-action model.
- Planning: zero, one, or five sampled model backups per real step.

Compared model modes:

- Keep the learned model after the change.
- Flush the model at the change.

Primary metrics:

- Average reward.
- Stale-backup rate.
- Q norm.
- Recovery windows after the change.

Result path:

`experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main`

Main figure:

`experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main/figures/avg_reward_by_planning_steps-model_mode_curve.png`

![Figure 3. Dyna average reward by planning budget and model handling.](../../../experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main/figures/avg_reward_by_planning_steps-model_mode_curve.png)

This is model-based planning, not a replay buffer: the stored object is a compact learned state-action transition model, and planning updates are intentional model backups.

### 4.5 Supporting and Negative Diagnostics

GVF predictive state:

- Long aliased T-maze.
- Raw observation, short history, trace memory, recurrent GVF, and oracle memory compared.
- Result path: `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`.

![Figure 4. T-maze trial accuracy by state construction.](../../../experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main/figures/trial_accuracy_by_algorithm_curve.png)

![Figure 5. GVF values and cue traces by maze position.](../../../experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main/figures/gvf_trace_by_position.png)

Generate-and-test:

- Delay-shift trace-conditioning prediction with a tight feature budget.
- Fixed-tight, oracle-bank, random replacement, and generate-test compared.
- Result path: `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`.

![Figure 6. Generate-and-test delay-shift prediction error.](../../../experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main/figures/abs_error_by_algorithm_curve.png)

TIDBD-lite:

- Nonstationary sensor prediction with old/new relevant feature groups.
- Fixed TD, normalized TD, and TIDBD-lite compared.
- Result path: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`.

![Figure 7. TIDBD-lite and baseline TD absolute TD error.](../../../experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main/figures/abs_td_error_by_algorithm_curve.png)

## 5. Results

### 5.1 Reward Centering Stabilizes Value Scale Under Reward Shifts

The key result is value-scale stability. In access-control, discounted Sarsa is strongly sensitive to constant reward shifts. Its seed-aware tail Q norm increases from about `60.17 +/- 1.89` at shift `-4` to `344.59 +/- 15.3` at shift `8`. Its unshifted average reward also drops at positive shifts, from about `2.39 +/- 0.14` at shift `-4` to `1.68 +/- 0.31` at shift `8`.

Reward-centered Sarsa keeps the Q norm near `20` to `22` across the same shifts:

| Algorithm | Shift | Tail unshifted reward | Tail Q norm |
|---|---:|---:|---:|
| Discounted Sarsa | -4 | 2.395 +/- 0.136 | 60.17 +/- 1.89 |
| Discounted Sarsa | 0 | 2.239 +/- 0.144 | 90.21 +/- 3.67 |
| Discounted Sarsa | 4 | 1.482 +/- 0.196 | 184.47 +/- 10.1 |
| Discounted Sarsa | 8 | 1.679 +/- 0.311 | 344.59 +/- 15.3 |
| Reward-centered Sarsa | -4 | 2.468 +/- 0.107 | 20.38 +/- 0.54 |
| Reward-centered Sarsa | 0 | 2.540 +/- 0.102 | 20.02 +/- 0.33 |
| Reward-centered Sarsa | 4 | 2.508 +/- 0.079 | 20.70 +/- 0.24 |
| Reward-centered Sarsa | 8 | 2.504 +/- 0.077 | 21.63 +/- 0.58 |
| Differential Sarsa | -4 | 2.538 +/- 0.080 | 20.36 +/- 0.67 |
| Differential Sarsa | 0 | 2.534 +/- 0.102 | 19.81 +/- 0.25 |
| Differential Sarsa | 4 | 2.475 +/- 0.085 | 20.82 +/- 0.45 |
| Differential Sarsa | 8 | 2.542 +/- 0.094 | 21.55 +/- 0.73 |

Interpretation:

The important claim is not merely that reward-centered Sarsa has a higher curve in this run. The defensible claim is narrower and stronger: reward centering and differential updates remove most of the arbitrary reward-shift effect on the value scale and TD-error baseline. This is exactly the kind of invariance a continual agent should have.

### 5.2 Output-Controlled TD Is Robust to Feature Scale

Fixed TD behaves acceptably when the scale is easy, but its stable region changes sharply with feature scaling. At scale `hundred`, fixed TD diverges for all tested alphas, with tail RMSE around `1.1e4`. At scale `ten`, alpha `0.3` diverges with RMSE around `6.45e6`. Uneven feature scales also cause divergence for alpha `0.1` and `0.3`.

Normalized TD keeps RMSE in a narrow range across feature scales and alphas, with zero divergence in the tested grid. Trace-normalized TD behaves similarly.

Representative results:

| Algorithm | Scale | Alpha | Tail RMSE | Divergence |
|---|---|---:|---:|---:|
| Fixed TD | one | 0.3 | 0.559 +/- 0.005 | 0 |
| Fixed TD | ten | 0.3 | 6.45e6 +/- 2.43e6 | nonzero |
| Fixed TD | hundred | 0.03 | 1.13e4 +/- 6.98e3 | nonzero |
| Fixed TD | uneven | 0.1 | 1.43e6 +/- 1.91e6 | nonzero |
| Normalized TD | one | 0.3 | 0.524 +/- 0.015 | 0 |
| Normalized TD | ten | 0.3 | 0.471 +/- 0.029 | 0 |
| Normalized TD | hundred | 0.3 | 0.471 +/- 0.029 | 0 |
| Normalized TD | uneven | 0.3 | 0.442 +/- 0.033 | 0 |
| Trace-normalized TD | one | 0.3 | 0.528 +/- 0.014 | 0 |
| Trace-normalized TD | ten | 0.3 | 0.505 +/- 0.016 | 0 |
| Trace-normalized TD | hundred | 0.3 | 0.505 +/- 0.016 | 0 |
| Trace-normalized TD | uneven | 0.3 | 0.489 +/- 0.020 | 0 |

The current true-online TD(lambda) baseline must be reported honestly. It performs well in some easy conditions, but diverges under large feature scales and high trace/alpha conditions in this implementation. It is therefore not used as evidence that traces solve scale sensitivity.

Interpretation:

The result supports the output-control view: when the effective update is normalized by the input or trace magnitude, alpha becomes closer to a control knob for prediction change. This is more stable than treating parameter-space movement as the primitive learning unit.

### 5.3 Planning Helps Before Change but Stale Models Hurt Recovery

In the Dyna gridworld, planning gives clear pre-change benefit. With five planning backups, pre-change average reward is about `0.099`, compared with about `0.004` without planning. However, after the layout changes, keeping the old model leads to high stale-backup rates:

- One planning backup, keep model: late stale-backup rate about `0.844 +/- 0.016`.
- Five planning backups, keep model: late stale-backup rate about `0.705 +/- 0.025`.

Flush-on-change removes stale backups, but it does not automatically solve recovery. With five planning backups, late post-change average reward is about `-0.0220 +/- 0.0025` for flush-on-change and `-0.0270 +/- 0.0027` for keep-model. No-planning late reward ranges from about `-0.0175` to `-0.0211` depending on the matched label.

Interpretation:

This is a useful Alberta Plan diagnostic. Learned models and planning can improve sample efficiency, but under nonstationarity, planning can also amplify obsolete knowledge. The right next question is not "more planning or less planning" but how to age, test, flush, or prioritize model knowledge in a stream.

### 5.4 GVF Predictive State: A Useful Negative Result

The GVF proposal is conceptually close to the Alberta Plan: predictive knowledge should help construct state under partial observability. The current design does not achieve that.

In the long aliased T-maze:

| Agent state | Tail trial accuracy |
|---|---:|
| Raw observation | 0.512 +/- 0.038 |
| Short history | 0.492 +/- 0.043 |
| Recurrent GVF | 0.502 +/- 0.023 |
| Trace memory | 0.944 +/- 0.018 |
| Oracle memory | 0.939 +/- 0.027 |

The important part is the trace-memory baseline. It shows that the task is learnable with a small non-deep memory mechanism. Therefore the recurrent GVF failure is not because the task is impossible; it is because the current GVF question/state design is not carrying cue information in a useful way.

This result should not be presented as evidence against GVFs generally. It is a localized failure that sets a clear standard for future GVF designs: the learned prediction must be visibly tied to the hidden cue and must improve downstream control, not merely exist as an auxiliary value.

### 5.5 Generate-and-Test and TIDBD: Mechanism Signals Are Not Enough

Generate-and-test:

The current generate-and-test trace replacement mechanism finds trace timescales closer to the post-change target than fixed or random baselines, but it does not improve prediction error. In the late post-change window, absolute error is approximately:

- Fixed-tight: `0.0512`.
- Generate-test: `0.0518`.
- Random replacement: `0.0496`.
- Oracle bank: `0.0545`.

This is a failed current design, not a main story. Future work should redesign the setting around multiple delay changes and feature-survival curves if adaptive timescale discovery is still desired.

TIDBD-lite:

TIDBD-lite shows a meaningful plasticity signal. Newly relevant feature step sizes rise from about `0.0068` before the switch to about `0.0093` in the late post-change window, while distractor step sizes stay near `0.0068`. However, normalized TD remains the better error baseline: late post-change absolute TD error is about `0.4419` for normalized TD and `0.4493` for TIDBD-lite.

This should be reported as mechanism support, not as a performance win.

## 6. Discussion

### 6.1 What the Early Overview Results Say

The early overview studies support a common claim: in streaming RL, the units of update control matter.

Reward centering changes the reward baseline so that arbitrary reward shifts do not inflate value estimates and TD errors. Output-controlled TD changes the effective unit of step size so that arbitrary feature scaling does not destabilize prediction. Both mechanisms are small, online, and compatible with continual learning.

### 6.2 Why the Negative Results Matter

The negative diagnostics prevent the project from becoming a list of superficial proposals. The GVF result shows that "using predictions as state" is not enough; the prediction must be the right question and must be useful for control. The generate-and-test result shows that an apparently sensible feature-allocation signal is not enough if it does not improve prediction error. The Dyna result shows that planning is not automatically beneficial when models become stale.

These are useful research outcomes because they clarify what would need to change in the next iteration.

### 6.3 Scope of Claims

The claims are deliberately narrow:

- Reward-centered Sarsa is robust to constant reward shifts in the tested continuing access-control setting.
- Normalized and trace-normalized TD are robust to feature-scale stress tests in the tested tile-coded random walk.
- Current Dyna planning has a model-staleness tradeoff in a changing gridworld.
- Current recurrent GVF state, current generate-and-test replacement, and current TIDBD-lite implementation are not promoted as positive final stories.

The project does not claim a general solution to continual RL, GVF state construction, option discovery, or model-based adaptation.

## 7. Limitations

The experiments are intentionally small. That improves interpretability but limits external validity. The main runs use five seeds, which is acceptable for a course project but not a complete statistical study. Some baselines are compact local implementations rather than full canonical algorithms; for example, `TIDBDLite` should not be described as a complete TIDBD result, and trace-normalized TD is a heuristic inspired by output-control ideas rather than a full deep intentional-update method.

The Dyna experiment uses a simple model and uniform model backups. More serious continual planning would need model aging, uncertainty, change detection, or prioritized stale-error updates. The GVF experiment needs redesigned questions and trajectory diagnostics before it can support a positive predictive-state claim.

## 8. Reproducibility

Environment:

- Conda environment: `/data/yupeng/conda_envs/core-rl`.
- Python executable recorded in manifests: `/data/yupeng/conda_envs/core-rl/bin/python`.
- Required environment variable: `PYTHONNOUSERSITE=1`.
- Matplotlib cache: `MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig`.

Verification commands:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python -m compileall experiments/alberta_core_rl

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py
```

Main run examples:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_main.json

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/output_controlled_td/config_main.json
```

Current result status is indexed in:

`final/indexes/results.md`

Detailed reproduction notes are in:

`final/indexes/reproduction.md`

## 9. Conclusion

This project began as a broad set of Alberta Plan inspired Core RL proposals. After implementation, critique, reruns, and proposal triage, the strongest report is narrower: reward centering and output-controlled prediction are the main stories. Both show that small normalization mechanisms can make online learning more invariant to arbitrary scale choices in a continuing stream.

The supporting studies add important caution. Model-based planning can amplify stale knowledge after change. GVFs require careful question design before they become useful state. Feature generation and per-feature step-size adaptation need evidence on prediction error and recovery, not only mechanism-level signals.

The final research message is therefore practical: continual RL progress should be judged by focused questions and diagnostic metrics, not by broad algorithm labels. For small streaming agents, the useful questions are often about invariance, stability, recovery, and whether each unit of computation still refers to the current world.

## References

- Sutton, R. S. "The Alberta Plan for AI Research." https://arxiv.org/abs/2208.11173
- Naik et al. "Reward Centering." https://arxiv.org/abs/2405.09999
- Bellman-error centering follow-up. https://arxiv.org/abs/2502.03104
- Intentional updates / output-control motivation. https://arxiv.org/abs/2604.19033
- Streaming RL motivation. https://arxiv.org/abs/2602.09396
- True online TD(lambda). https://arxiv.org/abs/1512.04087
- TIDBD and feature-wise step-size adaptation. https://arxiv.org/abs/1804.03334
- GVF/Horde background. https://arxiv.org/abs/1206.6262
- Online agent-state learning. https://arxiv.org/abs/2112.15236
- Average-reward learning and planning. https://arxiv.org/abs/2006.16318
