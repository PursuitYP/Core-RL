# Scale-Invariant Continuing Control

## Abstract

Long-lived agents should not depend on arbitrary measurement units. In continuing control, adding a constant to all rewards does not change which behavior is desirable, yet ordinary discounted value methods can inflate their value scale and become harder to tune. Likewise, rescaling features does not change the represented value function, but it changes the effect of a fixed parameter step. This proposal asks whether reward centering and output-controlled updates can be combined into a small streaming Sarsa agent that is more stable under reward translation and feature scaling. The current evidence supports a stability improvement, not a claim that unit invariance or no-reset recovery is solved.


## Standalone Study Summary

This study asks whether a continuing control agent can remain stable when two arbitrary units of the problem change: the zero point of reward and the scale of the feature vector. The RL problem is a continuing access-control queue with online accept/reject decisions. The implemented agents are discounted Sarsa, reward-centered Sarsa, normalized Sarsa, normalized reward-centered Sarsa, and normalized differential Sarsa. The fixed-condition pilot crosses reward shifts `-4, 0, 8` with feature scales `one, ten, hundred, uneven`; the no-reset unit-switching extension changes reward origin and/or feature scale halfway through the same stream. The main metrics are unshifted average reward, Q norm, prediction change, divergence, and policy probes. The current result shows that reward centering and feature normalization solve different failure modes and compose well in the combined normalized-centered variants, but abrupt feature-unit recovery remains incomplete. The key remaining experiments are the running full fixed-condition CPU sweep, policy-distance probes, and gradual unit drift.

## Proposal Template Answers

Focused RL question: Can a small online control agent preserve behavior and numerical stability when reward origin and feature units change, or do these arbitrary measurement conventions leak into the learning dynamics? This is a combined invariance question, not a benchmark-score question.

Setting and testbed: The main testbed is the continuing access-control queue with linear action values. It is chosen because it is a real continuing control problem with a policy tradeoff, yet small enough to expose Q norms, prediction changes, reward baselines, and divergence. The secondary testbed is a no-reset unit-switching version of the same stream.

Implemented comparison: The study compares discounted Sarsa, reward-centered Sarsa, differential Sarsa, normalized Sarsa, normalized reward-centered Sarsa, and normalized differential variants. The key variation is the crossing of reward shifts and feature scales, followed by online reward/feature unit changes without resetting the agent.

Observation or figure that answers the question: The proposal is supported only if a method preserves unshifted reward and policy probes while keeping Q norm, output-change magnitude, and divergence stable across both reward shifts and feature scales. The unit-switching figures are especially important because they test continual recovery rather than separate fixed-condition tuning.

Compute need and fallback: The main pilot and unit-switching extension are complete. The fixed-condition 20-seed extended CPU sweep is running as `core-rl-scale-invariant-extended-33723554`; until its artifacts appear, the fallback is to present fixed-condition pilot evidence plus the stronger no-reset unit-switching evidence and state that full-grid confirmation is pending.

## Independent Research Scope

This is a larger independent study of unit sensitivity in continuing control. It asks whether a single online control learner can remain stable when two arbitrary measurement conventions change: reward origin and feature scale. The study contains its own environment, methods, metrics, fixed-condition experiment, and no-reset unit-switching experiment.

The report does not claim that unit invariance is solved in general. Its current scope is linear access-control Sarsa under synthetic but controlled unit manipulations. The fixed-condition pilot supports compositional stability, while the no-reset extension shows that abrupt feature-unit changes still damage long-run reward even when catastrophic divergence is avoided.

## Evidence Level

Evidence level: strong independent evidence, but not final full-grid evidence. The completed fixed-condition pilot demonstrates the interaction between reward centering and update normalization. The completed 20-seed unit-switching run is stronger for continual-learning relevance because it changes units inside the same stream without resetting weights. The running `20260709T063128Z_extended` fixed-condition sweep has no artifacts yet and must not be cited as evidence.

The current claim should be deliberately narrow: combined centering/normalization is necessary for stable unit changes, and it prevents severe numerical instability under no-reset switches, but it does not fully solve recovery after abrupt feature-scale changes. A mature final paper would add the running extended grid, gradual scale drift, beta sensitivity, and policy-distance probes.

## Paper-Style Contribution And Claim Boundaries

The contribution is to turn two local invariance mechanisms into a single continuing-control question: can an agent remain stable when both reward and feature units are arbitrary? The fixed-condition experiment tests compositionality, while the no-reset switch experiment tests whether the same mechanisms survive a more continual interpretation. This gives the proposal a stronger narrative than simply combining two methods.

The claim boundary is that the current evidence supports stability under tested unit changes, not solved invariance. Combined centering and normalization prevent the most severe numerical failures in this access-control setting, but abrupt feature-scale switches still reduce long-run reward. The open scientific problem is therefore recalibration and recovery after unit change, not just preventing divergence.

## Research Motivation

The Alberta Plan treats intelligence as temporally uniform learning from ordinary experience. This makes unit sensitivity a central problem rather than a cosmetic one. A continual agent does not get a clean retuning phase whenever a sensor is rescaled or a reward baseline shifts. If reward origin and feature scale can change the effective learning problem, then the agent's competence depends on arbitrary conventions outside the task.

The research motivation is therefore internal to the control problem: an access-control agent should learn accept/reject behavior from reward differences and state-action evidence, not from arbitrary choices about the zero of reward or the magnitude of one-hot features. The combined stress test is useful because reward translation and feature scaling can interact through TD-error magnitude, action-value scale, and effective step size.

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

- Implemented as `unit_switching_continuing_control`: the same continuing access-control stream changes reward origin and/or feature scale halfway through the run without resetting weights, traces, or reward baselines.

Metrics:

- Unshifted average reward.
- Q norm and maximum absolute action value.
- TD-error scale.
- Approximate output change per update.
- Divergence rate.
- Policy invariance under reward shifts, measured by accept-probability probes.
- Recovery window after online scale or reward-origin change.

## Experiment Design Rationale

The design deliberately crosses two nuisance dimensions because each single mechanism has a plausible but incomplete story. Reward centering should remove reward-origin offsets but does not control the magnitude of a feature-driven parameter update. Normalization should control feature-scale effects but does not remove the constant value component induced by reward shifts. The combined grid is therefore a compositional test: if a method handles only one nuisance dimension, it should fail in the other.

The no-reset unit-switching extension is included because fixed-condition sweeps can hide a retuning assumption. A continual agent should not get fresh weights when a sensor is rescaled. The switch experiment therefore measures early and late post-change reward, Q norm, and divergence. It is intentionally harsh: the `hundred` scale switch reveals whether an algorithm merely avoids numerical explosion or also recovers useful behavior.

## Expected Results And Failure Modes

Expected positive pattern: ordinary discounted Sarsa should be sensitive to reward shifts and feature scales; reward centering should control reward-origin sensitivity; normalized updates should control feature-scale sensitivity; the combined method should control both.

Important failure modes:

- Centering may stabilize values but hurt adaptation if the average-reward estimator lags.
- Normalization may over-dampen sparse but important updates.
- Differential Sarsa may be more invariant but more sensitive to step-size coupling.
- Simultaneous reward and scale changes may reveal interaction effects that are not visible when only one unit convention is perturbed.

## Interpretation Standard

A result is meaningful only if it shows invariance across equivalent descriptions of the same continuing task. Higher reward in one condition is not enough. The final report should emphasize update geometry, value scale, and policy probes.

## Results

The first completed experiment for this report is a combined continuing-control pilot:

`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`

The combined run crosses reward shifts `-4, 0, 8` with feature scales `one, ten, hundred, uneven` in access-control Sarsa. It shows that the two invariance mechanisms are complementary:

- Reward-centered Sarsa alone is stable at scale `one`, but diverges or develops extremely large Q norms at uniform scales `ten` and `hundred`.
- Normalized Sarsa controls feature scale but remains reward-shift sensitive, with tail unshifted reward falling to about `1.45` at shift `8`, scale `one`.
- Normalized reward-centered Sarsa keeps tail unshifted reward near `2.41-2.51` across all tested shifts and scales with zero divergence.
- Normalized differential Sarsa shows a similar robust pattern.

The important pattern is interaction-specific: each single mechanism fails outside its own invariance dimension, while the combined mechanisms compose in the current pilot.

A stricter no-reset unit-switching experiment was then added:

`experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`

This run uses seeds `0-19`, `20000` online steps, reward-origin and feature-scale switches halfway through the stream, and alpha values `0.01`, `0.03`, and `0.1`. It changes the interpretation in an important way. Fixed discounted Sarsa can become numerically unstable after a feature-scale or joint reward/scale switch, with post-switch Q norms reaching about `1e8` and nonzero divergence in the early post-change window. Normalized reward-centered and normalized differential variants avoid divergence, which supports the core stability claim. However, they do not fully solve recovery after the harsh `hundred`-scale switch: late unshifted reward for normalized-centered and normalized-differential variants often falls to about `1.9-2.0` under feature-scale or joint-scale switches, even though reward-shift-only and lognormal-scale switches recover much better. The stronger conclusion is therefore not "unit invariance is solved"; it is that combined centering/normalization is necessary for stability, but no-reset recovery under abrupt feature-unit changes remains an open design problem.

Unit-switching summary figures:

![Post-late reward after no-reset unit switches.](../../../../experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended/figures/report_unit_switch_reward_heatmap.png)

![Post-late Q norm after no-reset unit switches.](../../../../experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended/figures/report_unit_switch_q_norm_heatmap.png)

![Post-late divergence after no-reset unit switches.](../../../../experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended/figures/report_unit_switch_divergence_heatmap.png)

Main figures below use seed-tail condition summaries with 95% confidence intervals. They replace the earlier overloaded learning-curve plots whose legends compressed the plotting area.

![Tail unshifted reward by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_avg_unshifted_reward_by_scale.png)

![Tail Q norm by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_q_norm_by_scale.png)

![Tail output-change magnitude by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_prediction_change_by_scale.png)

## Analysis

The main insight is that reward-origin correction and feature-scale correction address different parts of the TD learning loop. Reward centering removes the constant component of the return that is irrelevant for average-reward control, but it does not prevent a large feature vector from producing an oversized parameter update. Output normalization controls the update direction's scale, but it does not remove the nuisance value offset created by shifted rewards. The fixed-condition pilot shows that the two mechanisms can compose: when both arbitrary units are stressed, the combined variants remain much more stable than either single correction.

The no-reset unit-switching result is the more important continual-learning test because it removes the hidden retuning assumption of fixed-condition sweeps. A stable method must continue from its current weights after the measurement convention changes. The result is mixed in a useful way: combined variants avoid the catastrophic Q-norm blow-up of fixed discounted Sarsa, but abrupt `hundred`-scale feature switches still reduce late unshifted reward. The open problem is therefore not whether unit correction matters; it is how an online control learner should recalibrate after a large unit change without replay, reset, or a special calibration phase.

## Reviewer Critique And Revisions

Strict reviewer challenge: "You are just combining two tricks." Response: the scientific object is not the trick but invariance under arbitrary problem units. The combined experiment is valuable if it reveals whether independently plausible normalizations compose or interfere.

Strict reviewer challenge: "Access-control is still small." Response: small is acceptable for Core RL if the manipulation is sharp and the diagnostics expose mechanism. The added unit-switching experiment now tests a harder no-reset adaptation case, and its mixed result prevents the report from overstating the fixed-condition pilot.

Per-proposal audit matrix:

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| Alberta Plan | Unit invariance must matter for continual agents, not only for synthetic stress tests. | Adds a no-reset unit-switching stream and frames the problem as temporal-uniform learning under changing measurement conventions. | Natural sensor drift is not yet modeled. |
| Core RL | The study could be mistaken for a loose combination of two tricks. | The report defines a single combined invariance question and tests interaction failures inside one control setting. | Needs the running full-grid extended sweep for stronger coverage. |
| Stability | Avoiding divergence may not imply good control. | Reports unshifted reward, Q norm, output change, and divergence. | Policy-distance probes and recovery AUC remain missing. |
| Statistics | Fixed-condition pilot is weaker than the unit-switch extension. | Separates pilot evidence from completed 20-seed unit-switch evidence. | The currently running extended fixed grid has no artifacts yet. |
| Strict instructor | Do not claim unit invariance is solved. | Conclusion states that abrupt feature-scale recovery remains open. | Gradual drift and beta/gamma sensitivity are still needed. |

## Threats To Validity

The current evidence is stronger than the first pilot but still not a finished empirical paper. The access-control queue is larger and more meaningful than a two-state toy problem, but it is still a compact synthetic control task. The scale manipulation is artificial by design: it tests whether the algorithm respects equivalent feature units, not whether natural sensors drift in exactly this way. The unit-switching run adds a no-reset adaptation test, but it uses abrupt changes; a stricter version should include gradual feature-scale drift, beta sensitivity for reward baselines, and policy-distance probes over all access-control states.

## Conclusion

This proposal remains a strong independent Core-RL candidate because it has a clear invariance question, an interpretable continuing-control environment, and a nontrivial interaction: reward centering and output normalization solve different failure modes and compose in the fixed-condition pilot. The stricter unit-switching extension prevents the conclusion from becoming too strong. Combined variants prevent the catastrophic numerical instability seen in fixed discounted Sarsa, but abrupt no-reset feature-scale changes can still reduce long-run unshifted reward. The current claim is therefore: centering plus normalization is necessary for stable unit changes, but recovery after abrupt feature-unit changes is still an open Core RL problem. The next step is the full `scale_invariant_continuing_control/config_extended.json` grid plus gradual feature-scale drift, not a claim that unit invariance is solved.

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

No-reset unit-switching extension:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/unit_switching_continuing_control/config_extended.json
```

Regenerate fixed-condition report figures:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind scale \
  --result-dir experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main
```
