# Scale-Invariant Continuing Control

## Abstract

Long-lived agents should not depend on arbitrary measurement units. In continuing control, adding a constant to all rewards does not change which behavior is desirable, yet ordinary discounted value methods can inflate their value scale and become harder to tune. Likewise, rescaling features does not change the represented value function, but it changes the effect of a fixed parameter step. This proposal asks whether reward centering and output-controlled updates can be combined into a small streaming Sarsa agent whose behavior is invariant to both reward translation and feature scaling.


## Standalone Study Summary

This study asks whether a continuing control agent can remain stable when two arbitrary units of the problem change: the zero point of reward and the scale of the feature vector. The RL problem is a continuing access-control queue with online accept/reject decisions. The implemented agents are discounted Sarsa, reward-centered Sarsa, normalized Sarsa, normalized reward-centered Sarsa, and normalized differential Sarsa. The experiment crosses reward shifts `-4, 0, 8` with feature scales `one, ten, hundred, uneven`; the main metrics are unshifted average reward, Q norm, prediction change, divergence, and policy probes. The current result shows that reward centering and feature normalization solve different failure modes and compose well in the combined normalized-centered variants. The key remaining experiment is a longer CPU sweep plus an in-stream nonstationary unit-change test.

## Research Motivation

The Alberta Plan treats intelligence as temporally uniform learning from ordinary experience. This makes unit sensitivity a central problem rather than a cosmetic one. A continual agent does not get a clean retuning phase whenever a sensor is rescaled or a reward baseline shifts. If reward origin and feature scale can change the effective learning problem, then the agent's competence depends on arbitrary conventions outside the task.

The existing Reward-Centered Sarsa proposal gives evidence for reward-shift robustness in an access-control queue. The existing Output-Controlled TD proposal gives evidence for feature-scale robustness in tile-coded prediction. This integrated proposal tests whether the two invariances interact cleanly inside a single continuing control loop.

## Research Question

Can a linear continuing Sarsa agent preserve task-relevant behavior under simultaneous reward translation and feature rescaling when it uses reward-centered TD errors and output-controlled step sizes?

The question is intentionally stronger than "which method scores higher." A positive result requires invariance of behavior and update scale across equivalent problem parameterizations.

## Related Work

The Alberta Plan motivates continuing agents, average reward, value functions, and temporally uniform learning from experience. Reward Centering shows that subtracting an empirical average reward can remove constant-shift sensitivity in continuing discounted methods. Bellman Error Centering clarifies related fixed-point issues. Intentional Updates argues that step sizes should specify an intended output change, not raw parameter motion. This project translates those ideas into tabular/linear Core RL settings rather than deep streaming agents.

Useful local sources:

- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`
- `resources/alberta_plan_related/reward_centering_2405.09999.pdf`
- `resources/alberta_plan_related/bellman_error_centering_2502.03104.pdf`
- `resources/alberta_plan_related/intentional_updates_streaming_rl_2604.19033.pdf`

## Research Method

The agent uses linear action values `q(s,a)=w_a^T x(s)` and on-policy epsilon-greedy control. The baseline update is ordinary discounted Sarsa. The centered variant subtracts an online estimate of average reward from the TD error. The output-controlled variant normalizes the update by the squared norm of the active feature vector or eligibility trace, so that alpha approximates a prediction-change fraction.

Core variants:

- Discounted Sarsa.
- Reward-centered Sarsa.
- Differential Sarsa.
- Normalized Sarsa.
- Normalized reward-centered Sarsa.
- Trace-normalized reward-centered Sarsa(lambda).

## Experimental Design

Primary environment:

- Continuing access-control queue with accept/reject actions.
- Linear/tile-coded representation of free servers and customer priority.
- Reward shifts `-8, -4, 0, 4, 8`.
- Feature scales `one`, `ten`, `hundred`, `uneven`, `lognormal` in the extended code path.
- Alpha grid `0.01`, `0.03`, `0.1` in the extended code path.
- Discount factors are currently fixed by algorithm family rather than swept: discounted/centered/normalized variants use `0.99`, while differential variants use `1.0`.
- Seeds `0-19` for the final CPU sweep.

Secondary environment:

- Planned, not yet implemented: a continuing queue variant with nonstationary feature scaling midway through the stream, used to test recovery without a reset.

Metrics:

- Unshifted average reward.
- Q norm and maximum absolute action value.
- TD-error scale.
- Approximate output change per update.
- Divergence rate.
- Policy invariance under reward shifts, measured by accept-probability probes.
- Recovery window after online scale or reward-origin change.

## Expected Results And Failure Modes

Expected positive pattern: ordinary discounted Sarsa should be sensitive to reward shifts and feature scales; reward centering should control reward-origin sensitivity; normalized updates should control feature-scale sensitivity; the combined method should control both.

Important failure modes:

- Centering may stabilize values but hurt adaptation if the average-reward estimator lags.
- Normalization may over-dampen sparse but important updates.
- Differential Sarsa may be more invariant but more sensitive to step-size coupling.
- Simultaneous reward and scale changes may reveal interaction effects hidden in separate experiments.

## Interpretation Standard

A result is meaningful only if it shows invariance across equivalent descriptions of the same continuing task. Higher reward in one condition is not enough. The final report should emphasize update geometry, value scale, and policy probes.

## Results

Existing Reward-Centered Sarsa results show stable Q norms around `20-22` across reward shifts, while ordinary discounted Sarsa grows from about `60` to about `345`. Existing Output-Controlled TD results show zero divergence for normalized variants across large feature-scale changes where fixed TD often diverges. These are separate experiments; the integrated proposal adds a combined continuing-control pilot:

`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`

The combined run crosses reward shifts `-4, 0, 8` with feature scales `one, ten, hundred, uneven` in access-control Sarsa. It shows that the two invariance mechanisms are complementary:

- Reward-centered Sarsa alone is stable at scale `one`, but diverges or develops extremely large Q norms at uniform scales `ten` and `hundred`.
- Normalized Sarsa controls feature scale but remains reward-shift sensitive, with tail unshifted reward falling to about `1.45` at shift `8`, scale `one`.
- Normalized reward-centered Sarsa keeps tail unshifted reward near `2.41-2.51` across all tested shifts and scales with zero divergence.
- Normalized differential Sarsa shows a similar robust pattern.

This is stronger than a portfolio synthesis: each single mechanism fails outside its own invariance dimension, while the combined mechanisms compose in the current pilot.

Main figures below use seed-tail condition summaries with 95% confidence intervals. They replace the earlier overloaded learning-curve plots whose legends compressed the plotting area.

![Tail unshifted reward by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_avg_unshifted_reward_by_scale.png)

![Tail Q norm by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_q_norm_by_scale.png)

![Tail output-change magnitude by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_prediction_change_by_scale.png)

## Reviewer Critique And Revisions

Strict reviewer challenge: "You are just combining two tricks." Response: the scientific object is not the trick but invariance under arbitrary problem units. The combined experiment is valuable if it reveals whether independently plausible normalizations compose or interfere.

Strict reviewer challenge: "Access-control is still small." Response: small is acceptable for Core RL if the manipulation is sharp and the diagnostics expose mechanism. The secondary nonstationary representation shift should be added before promoting the proposal as a full paper.

## Threats To Validity

The current evidence is a first main pilot, not a finished empirical paper. The access-control queue is larger and more meaningful than a two-state toy problem, but it is still a compact synthetic control task. The scale manipulation is also artificial by design: it tests whether the algorithm respects equivalent feature units, not whether natural sensors drift in exactly this way. The current sweep uses tenable but limited hyperparameters; a stricter version should include an alpha sweep for each update rule and a second environment where feature scales change during a single continuing stream rather than being fixed per run.

## Conclusion

This proposal is one of the strongest current integrated Core-RL topics. It gives a clear research question, an interpretable continuing-control environment, a meaningful stress test, and a nontrivial interaction: reward centering and output normalization solve different invariance failures, and the combined variants are strongest in the current pilot. The next step is a longer CPU-task sweep using `config_extended.json`, followed by a second nonstationary feature-scale experiment.

## Reproduction

Current main pilot:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_main.json
```

Extended sweep config:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_extended.json
```
