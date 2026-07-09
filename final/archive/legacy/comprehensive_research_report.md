# Alberta Plan Core RL Course Project: Research Report

> Status note: this document is a legacy comprehensive draft from the initial minimal experiments. Current final-facing result status is indexed in
> `final/indexes/results.md`, current gate decisions are in
> `final/archive/legacy/proposal_gate_review.md`, and current reproduction commands are in
> `final/indexes/reproduction.md`. Old `*_minimal` paths below are
> preliminary and should not be used as final evidence.

## Abstract

This project studies small, streaming Core RL mechanisms motivated by the Alberta Plan. The central constraint is that agents learn continually from a single experience stream, without replay buffers or deep networks. Instead of asking which method achieves a larger benchmark score, the project asks how basic mechanisms behave under temporal uniformity: reward centering, output-controlled TD updates, predictive state construction, feature generate-and-test, options, per-feature step-size adaptation, off-policy stability, and model-based planning budget.

The current implementation provides a unified experimental package, proposal-specific configs, initial results, and report-ready materials. The proposal set is intentionally live: overlapping or weak proposals are merged into diagnostics, while stronger Alberta Plan questions are promoted.

## 1. Research Framing

The course project asks for a focused reinforcement learning question, a small testbed, a baseline, an ablation or extension, and reproducible code. The Alberta Plan adds a stricter research taste: a long-lived agent should learn from ordinary observation-action-reward experience, at all times, under limited computation.

The resulting research frame is:

> What basic mechanisms make a small RL agent more robust, interpretable, and continually adaptive when it learns online from a single stream?

This frame rules out replay-buffer-based deep RL and large benchmark engineering. It also rules out superficial comparisons that only report final return. The relevant measurements are online learning curves, value scale, TD error, update magnitude, recovery after change, feature utility, option usage, model budget, and policy invariance.

## 2. Literature Synthesis

The Alberta Plan argues for temporal uniformity: learning, planning, representation construction, and subtask construction should happen continually. Its roadmap starts from continual supervised learning and step-size adaptation, moves to feature finding and GVFs, then to average reward, continuing control, planning, options, STOMP, and Oak.

Reward Centering provides the cleanest project-level mechanism for continuing control. It shows that ordinary discounted methods can be brittle to constant reward shifts, while centering by empirical average reward removes the irrelevant baseline. This directly motivates Reward-Centered Continuing Sarsa.

Intentional Updates and Streaming Deep RL motivate the second main mechanism: in streaming learning, a parameter-space step-size does not reliably control the change in predictions. In linear TD, the minimal form of this idea is normalized TD, where the step-size is scaled by feature norm. TIDBD and True Online TD(lambda) provide non-deep baselines for adaptive step-sizes and traces.

GVF and generate-and-test work motivate the representation proposals. A prediction is not valuable just because it is accurate; it is valuable if it supports downstream learning or control. Generate-and-test adds the Oak-like idea that a long-lived agent must evaluate feature utility and replace weak features.

Options and Dyna represent two ways to reuse structure: temporal abstraction and learned models. In this project they are deliberately implemented in minimal tabular forms, so that the question remains about utility and computation rather than architecture scale.

## 3. Methodological Commitments

All experiments follow these rules:

- Streaming updates from the current step.
- No replay buffer.
- No deep networks.
- Small CPU-scale environments.
- Fixed seeds and result manifests.
- Baseline plus one or two mechanism-oriented ablations.
- Figures that explain behavior, not just final return.

The codebase reflects these commitments:

- Shared package: `experiments/alberta_core_rl/`
- Proposal-specific configs: `experiments/alberta_core_rl/configs/`
- Proposal-specific results: `experiments/alberta_core_rl/results/<proposal>/`
- Reproduction note: `final/indexes/reproduction.md`

## 4. Primary Proposal Dossiers

### 4.1 Reward-Centered Continuing Sarsa

Research motivation: Continuing agents should not change their essential behavior because a constant is added to every reward. In discounted learning, however, reward shifts change the value scale and can change TD-error magnitudes, action gaps, and step-size sensitivity. Alberta Plan agents are continuing agents, so this is a core problem rather than a cosmetic normalization issue.

Research question: Does online reward centering make continuing Sarsa insensitive to constant reward shifts?

Method: Compare discounted Sarsa, reward-centered Sarsa, and differential Sarsa. Reward-centered Sarsa subtracts an online average reward estimate before the discounted TD update. Differential Sarsa uses average-reward TD error and gamma equal to one.

Experimental design: Use a two-loop continuing MDP. Apply reward shifts such as `-5, 0, +5, +10`. Record both observed shifted reward and unshifted task reward.

Metrics:

- Unshifted average reward.
- Q-value norm.
- TD-error scale.
- Action choice at the decision state.
- Estimated reward baseline.

Current result path: `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T142324Z_minimal`

Current analysis: This proposal is mature and central. The most important reporting correction is to avoid using shifted reward as performance. The meaningful question is whether centering removes irrelevant reward baselines from updates and stabilizes learning across shifts.

Next refinement:

- Add reward-shift by algorithm heatmap.
- Add policy-invariance plot.
- Add continuing gridworld extension if time permits.

### 4.2 Output-Controlled TD

Research motivation: A fixed step-size in TD is not invariant to feature scale. If features are multiplied by ten, the induced prediction change can grow roughly by a factor of one hundred. In single-sample streaming learning, this can create instability that replay or batch averaging would otherwise hide.

Research question: Can output-level or normalized TD updates preserve prediction accuracy under arbitrary feature scaling?

Method: Compare fixed TD, normalized TD, trace-normalized TD, and true-online TD(lambda). Normalized TD chooses a per-step learning rate proportional to `1 / (epsilon + ||x||^2)`, making the step-size closer to a prediction-change parameter.

Experimental design: Use 19-state random walk prediction with one-hot features scaled by `one`, `ten`, `hundred`, and `uneven`.

Metrics:

- Online RMSE against known true values.
- Weight norm.
- Effective step-size.
- Prediction-change magnitude.
- Divergence flag.

Current result path: `experiments/alberta_core_rl/results/output_controlled_td/20260708T142128Z_minimal`

Current analysis: The proposal has a clear mechanism and expected visible phenomenon. The report should call the current trace-normalized method a heuristic, not a full intentional trace implementation.

Next refinement:

- Add alpha-scale stability heatmap.
- Add non-stationary sensor stream extension.
- Compare against TIDBD-lite under feature-relevance shift.

### 4.3 GVF Predictive State

Research motivation: In partial observability, current observation is not state. Alberta Plan perception should construct an agent state from the experience stream. GVFs are a natural candidate because they turn future predictions into current features.

Research question: Can learned GVF predictions supply missing state information in a partially observable control problem?

Method: In a cue-based T-maze, compare raw observation only, fixed short history, and raw observation plus learned GVF predictions. GVFs predict cue and junction cumulants over different discount horizons.

Experimental design: The agent observes a left/right cue at the start, then enters an aliased corridor. At the junction, the correct action depends on the earlier cue.

Metrics:

- Control average reward.
- Correct action rate at the junction.
- GVF TD error.
- GVF prediction trajectories over a trial.

Current result path: `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T142059Z_minimal`

Current analysis: This proposal is highly aligned with the Alberta Plan, but needs stronger visual diagnostics. It should not be framed as "GVFs are accurate"; it should be framed as "which predictions are useful as state?"

Next refinement:

- Plot GVF values across a trial.
- Add ablation removing individual GVFs.
- Connect GVF question design as supporting analysis.

### 4.4 Generate-and-Test Trace Features

Research motivation: A long-lived agent has limited representational capacity. Fixed features can become stale when temporal statistics change. Oak-style feedback suggests that features should be tested for utility and replaced when they are no longer useful.

Research question: Under a fixed feature budget, can utility-based replacement maintain useful trace features after temporal statistics change?

Method: Use trace-conditioning prediction. Maintain a bank of trace features with different decay rates. Compare a fixed trace bank to utility-based replacement of low-utility traces.

Experimental design: A cue appears, and reward appears after a delay. Halfway through the stream, the reward delay changes from 10 to 20.

Metrics:

- Absolute TD error around the switch.
- Recovery time.
- Replacement events.
- Distribution of active trace decays.
- Feature survival time.

Current result path: `experiments/alberta_core_rl/results/generate_test_features/20260708T142049Z_minimal`

Current analysis: The proposal is valuable if the utility measure is made explicit and interpretable. Without that, replacement can look arbitrary.

Next refinement:

- Plot `abs_error`, not raw reward.
- Add feature survival histogram.
- Compare utility replacement to random replacement.

### 4.5 Doorway Options for Transfer

Research motivation: Options are useful only if their temporal abstraction has reusable utility. Four Rooms provides a minimal setting where doorway structure is independent of the current goal.

Research question: When do doorway options help transfer across changing goals, and when do they hurt because of commitment cost?

Method: Compare primitive-action Sarsa with a minimal controller that uses hand-coded doorway options.

Experimental design: Four Rooms with alternating goals. Count environment steps and reward per environment step, not just option-decision steps.

Metrics:

- Average reward per environment step.
- Steps to goal.
- Option duration.
- Option usage.
- Recovery after goal change.

Current result path: `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T142054Z_minimal`

Current analysis: This is a reusable-subtask test, not option discovery. That limitation should be explicit.

Next refinement:

- Add option usage heatmap.
- Compare short vs long option commitment.
- Add reward-respecting option baseline if time permits.

### 4.6 TIDBD Plasticity

Research motivation: Alberta Plan Step 1 emphasizes step-size adaptation and feature relevance. TIDBD is a direct non-deep method for adapting TD step-sizes per feature.

Research question: Can per-feature step-size adaptation track changing feature relevance in online TD prediction?

Method: Compare fixed TD, normalized TD, and TIDBD-lite on a synthetic sensor stream where the relevant feature group switches halfway.

Experimental design: Features 1-5 predict the target in phase 1. Features 6-10 predict the target in phase 2. Other features are noise.

Metrics:

- Online absolute TD error.
- Recovery time after switch.
- Per-feature or grouped step-size.
- Weight norm.

Current result path: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T142244Z_minimal`

Current analysis: This is a stronger replacement for a vague streaming-representation proposal. It has a clear mechanism and a direct Alberta Plan connection.

Next refinement:

- Store per-feature step-size vectors, not only their mean.
- Plot feature relevance switch.
- Compare against output-controlled TD on the same stream.

### 4.7 Baird Off-policy Stability

Research motivation: GVFs and background predictions often require off-policy learning. Baird's counterexample is the minimal warning that semi-gradient off-policy TD can diverge with function approximation and bootstrapping.

Research question: Where does semi-gradient off-policy TD fail, and which corrections stabilize it?

Method: Compare off-policy TD and a small TDC-style correction on Baird-style linear features.

Experimental design: Seven-state counterexample with zero rewards and behavior/target policy mismatch.

Metrics:

- Weight norm.
- TD error.
- Importance ratio.
- Divergence flag.

Current result path: `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T142244Z_minimal`

Current analysis: This proposal is theoretically important, but because it is off-policy it should be positioned carefully relative to the course constraints. It is still no-replay and non-deep.

Next refinement:

- Verify exact canonical Baird implementation.
- Add GTD2 or ETD if time permits.
- Plot stability over alpha.

### 4.8 Dyna Planning Budget

Research motivation: The Alberta Plan includes continual planning with learned models. Planning is not replay if the agent stores a compact transition model rather than raw experience. The question becomes where limited computation should go.

Research question: How much does a tiny learned model help under a fixed per-step planning budget?

Method: Compare tabular Q-learning with zero, one, and five model backups per real step.

Experimental design: Continuing gridworld with compact state-action model.

Metrics:

- Average reward.
- Model size.
- Q norm.
- Performance per real environment step.
- Later extension: recovery after environment change.

Current result path: `experiments/alberta_core_rl/results/dyna_planning_budget/20260708T142244Z_minimal`

Current analysis: This proposal provides planning coverage. It should clearly disclose that model-based updates are allowed as planning, while raw transition replay remains forbidden.

Next refinement:

- Add shortcut/blocking environment change.
- Track model error.
- Add prioritized planning as extension.

## 5. Supporting Diagnostics

Centered TD Diagnostics supports Reward-Centered Sarsa by showing what offsets centering removes. On-policy Stability Atlas supports Output-Controlled TD by visualizing alpha/lambda fragility. GVF Question Design supports GVF-state by separating prediction accuracy from downstream usefulness. Non-stationary Bandit is useful as a warm-up for plasticity, but it is too weak as a main Core RL proposal because it lacks bootstrapping and sequential state.

## 6. Current Implementation Status

Implemented:

- Environments: random walk, two-loop MDP, continuing gridworld, T-maze, trace conditioning, non-stationary sensor stream, drifting bandit, Four Rooms.
- Agents: TD, TD(lambda), true-online TD(lambda), Sarsa, reward-centered Sarsa, differential Sarsa, normalized TD, TIDBD-lite, gradient bandit, action-value bandit.
- Scripts: single run, run all, plot results, smoke test.
- Result manifests and proposal-specific configs.

Validation:

- `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python -m compileall experiments/alberta_core_rl` passes.
- `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py` passes.
- Minimal runs were produced for all primary and supporting proposals.
- Current clean main result paths are maintained in `final/indexes/results.md`.

## 7. Research Summary

The strongest insight so far is that the Alberta Plan is not one topic; it is a set of constraints that force basic RL mechanisms to become online, resource-aware, and temporally uniform. Reward centering asks what reward baseline should be removed. Output-controlled TD asks what an update should mean. GVFs and generate-and-test ask what state features are worth keeping. Options ask when temporal abstraction remains useful. Dyna asks how limited planning computation should be spent.

The project should now move from "all proposals runnable" to "a few proposals deeply analyzed." The most report-ready pair is Reward-Centered Sarsa and Output-Controlled TD. GVF-state and Generate-and-Test are the most Alberta-style representation studies. TIDBD, Baird, and Dyna round out plasticity, off-policy stability, and planning.
