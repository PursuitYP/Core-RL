# TIDBD-Lite Plasticity

Status: independent mechanism diagnostic; current evidence is not a positive performance proposal.

## Abstract

This proposal studies per-feature step-size adaptation as a possible mechanism for plasticity in streaming TD prediction. The setting is a nonstationary sensor stream where the relevant feature group changes after a phase switch. A TIDBD-style learner should increase step sizes for newly relevant features, keep distractor step sizes low, and recover prediction accuracy after the change.

The current pilot supports only the mechanism part of that story. TIDBD-lite shows interpretable feature-wise alpha dynamics after the switch, but normalized TD has slightly lower late prediction error. The proposal is therefore a mechanism diagnostic, not a performance victory. Its value is to separate "the learner changes its internal learning rates in a sensible way" from "the learner improves the prediction objective."

## Evidence Summary

This report is a mechanism study for adaptive step sizes. It does not claim that the simplified TIDBD-lite learner is already a better predictor. Instead, it separates two questions that are often blurred in continual-learning discussions: does the learner move feature-wise step sizes in a sensible direction, and does that movement improve the downstream TD prediction objective? The current evidence answers the first question partly yes and the second question no.

| Item | Current evidence |
|---|---|
| RL question | Can per-feature step-size adaptation track changing feature relevance in online TD prediction? |
| Testbed | Nonstationary sensor prediction stream with old-relevant, new-relevant, and distractor feature groups; relevance switches halfway through the stream. |
| Compared learners | Fixed-alpha TD (`0.01`, `0.03`, `0.1`), normalized TD, and simplified TIDBD-lite. |
| Seeds and horizon | Five seeds, `5000` online steps per learner. |
| Primary metric | Post-change absolute TD error, with group-wise alpha trajectories as mechanism diagnostics. |
| Headline result | TIDBD-lite raises new-feature alpha from about `0.0068` before the switch to about `0.0093` late after the switch, while distractor alpha stays near `0.0068`; however, normalized TD has lower late post-change absolute TD error (`0.4419 +/- 0.0085`) than TIDBD-lite (`0.4493 +/- 0.0119`). |
| Conclusion boundary | Evidence supports visible adaptive-step-size dynamics, not a performance advantage. Stronger claims require canonical TIDBD/AutoStep, repeated switches, recovery AUC, and alpha-utility correlation. |

## Claim Boundary

The report makes one bounded claim:

> In the current nonstationary stream, TIDBD-lite shows visible per-feature step-size adaptation, but this adaptation has not yet produced a prediction-error advantage over normalized TD.

The report deliberately does not claim:

- that TIDBD-lite is a canonical TIDBD reproduction;
- that per-feature adaptation already improves performance;
- that alpha movement alone proves useful plasticity;
- that alpha dynamics alone justify any broader plasticity conclusion.

## Research Motivation/Question/Method

Continual agents operate in streams where feature relevance changes. A fixed global step size is a compromise: if it is large, irrelevant or noisy features can destabilize learning; if it is small, newly relevant features may adapt too slowly. Per-feature step-size adaptation offers a local mechanism for plasticity: each feature can adjust its learning rate according to its recent contribution to prediction updates.

The Alberta Plan treats step-size adaptation and feature utility as early building blocks for long-lived agents. This proposal asks whether a lightweight adaptive TD learner can detect relevance change from the stream itself, before claiming any large control benefit.

### Focused RL Question

Main question:

> Can per-feature step-size adaptation track changing feature relevance in online TD prediction?

Subquestions:

- Do step sizes for newly relevant features increase after a switch?
- Do distractor features remain comparatively quiet?
- Does the mechanism improve recovery speed or late prediction error relative to fixed and normalized TD baselines?

Hypothesis:

> After a relevance switch, a TIDBD-style learner should increase step sizes for newly relevant features, maintain lower step sizes for distractors, and recover prediction accuracy faster than fixed-alpha TD.

The current result supports the first two mechanism claims, but not the stronger performance claim.

### Core RL Connection

This is a core RL proposal because it studies online TD prediction, step-size adaptation, and feature utility with linear function approximation. It connects to:

- meta-learning of step sizes;
- online prediction from a stream;
- continual adaptation under nonstationarity;
- feature relevance tracking;
- limited computation without replay.

The proposal is deliberately not a deep plasticity benchmark. It is a small inspection tool for feature-wise learning-rate dynamics.

### Related Work

TIDBD extends incremental delta-bar-delta ideas to TD learning with feature-wise step sizes. The Alberta Plan discusses per-weight step-size adaptation as part of early continual-learning machinery. Broader plasticity work motivates recovery after nonstationarity, but much of that literature uses deep networks or replay settings outside this project's preferred scope.

Local references:

- `resources/alberta_plan_related/tidbd_1804.03334.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

### Method

The setting is a nonstationary sensor prediction stream:

- one feature group is relevant before a switch;
- a different feature group becomes relevant after the switch;
- distractor features remain mostly irrelevant;
- updates are online, with no replay buffer and no offline refitting.

This is a mechanism environment. It creates controlled feature-relevance changes that can be measured directly.

Compared methods:

- fixed TD with alphas `0.01`, `0.03`, and `0.1`;
- normalized TD;
- TIDBD-lite.

The local adaptive method is intentionally called TIDBD-lite. It uses a simplified per-feature meta-gradient-like update and should not be presented as canonical TIDBD until the full algorithm is implemented and checked.

## Experimental Design

Current main pilot:

- Seeds: `0-4`.
- Steps: `5000`.
- Switch: halfway through the stream.
- Result path: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`.

Primary measurements:

- absolute TD error;
- old-relevant feature step sizes;
- new-relevant feature step sizes;
- distractor step sizes;
- post-switch recovery windows.

Primary figure:

![Absolute TD error for TIDBD-lite and TD baselines.](../../../../experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main/figures/abs_td_error_by_algorithm_curve.png)

Design logic:

| Design element | Why it is needed |
|---|---|
| Feature relevance switch | Creates a known plasticity challenge. |
| Group-wise alpha logs | Tests whether adaptation moves toward the newly relevant features. |
| Distractor group | Detects indiscriminate alpha growth. |
| Normalized TD baseline | Tests whether simpler update scaling explains the benefit. |
| Recovery windows | Separates immediate adaptation from late steady-state error. |

## Results

TIDBD-lite shows the intended feature-wise mechanism:

- New-feature step size rises from about `0.0068` before the switch to about `0.0093` in the late post-change window.
- Distractor step size remains near `0.0068`.

However, normalized TD remains the stronger prediction-error baseline:

- late post-change absolute TD error for normalized TD is about `0.4419`;
- late post-change absolute TD error for TIDBD-lite is about `0.4493`.

This means the internal mechanism is visible, but the external prediction objective has not improved enough to support a performance claim.

The late post-change error comparison is:

| Strategy | Late post-change absolute TD error |
|---|---:|
| Normalized TD | `0.4419` |
| TIDBD-lite | `0.4493` |
| Fixed TD, alpha `0.01` | `0.4881` |
| Fixed TD, alpha `0.03` | `0.6279` |
| Fixed TD, alpha `0.1` | `0.6591` |

## Analysis

The current result suggests several possible failure mechanisms:

- Meta-update lag: alpha changes may occur, but not quickly enough to improve recovery after a single switch.
- Scale competition: normalized TD may already solve much of the update-magnitude problem that TIDBD-lite is trying to solve.
- Weak utility signal: the simplified meta-gradient may not separate useful features from correlated distractors strongly enough.
- One-switch environment: a single change may be too limited to expose cumulative plasticity benefits.
- Algorithm gap: TIDBD-lite may miss important details from canonical TIDBD or AutoStep.

These mechanisms are the reason the report treats alpha dynamics as evidence of mechanism behavior, not as evidence of a better learner.

## Next Experiments

The next experiments should test mechanism and performance separately:

1. Canonical algorithm check: implement full TIDBD or AutoStep and verify update equations against the reference.
2. Repeated switches: use multiple relevance changes to test whether per-feature adaptation accumulates an advantage over fixed or normalized TD.
3. Recovery AUC: report error area after each switch, not only late-window mean error.
4. Alpha-utility correlation: measure whether features with increased alpha also contribute more to prediction improvement.
5. Normalization ablation: compare per-feature adaptation with and without output/update normalization.
6. Control transfer only after success: test a small control task only if prediction recovery improves in the diagnostic stream.

## Threats To Validity

- The implementation is TIDBD-lite, not canonical TIDBD.
- The environment has only one switch.
- Normalized TD is a strong baseline and may explain much of the observed adaptation need.
- Current metrics do not yet include feature correlation, utility contribution, or recovery AUC.
- Mean group alpha can hide feature-level variance inside each group.

## Reviewer Critique

| Reviewer angle | Likely critique | Report response | Required next action |
|---|---|---|---|
| Algorithm reviewer | TIDBD-lite is not canonical TIDBD. | The report uses TIDBD-lite terminology throughout. | Implement canonical TIDBD or AutoStep. |
| Plasticity reviewer | Alpha movement alone is not utility evidence. | The report separates mechanism dynamics from prediction improvement. | Add alpha-utility correlation and recovery AUC. |
| Baseline reviewer | Normalized TD is already better on error. | The report treats this as a limit, not as a nuisance. | Add normalization ablations and repeated switches. |
| Strict instructor | Do not present a mechanism as a performance win. | The claim is explicitly diagnostic. | Keep final framing as mechanism study unless performance metrics improve. |

## Proposal Template Answers

Focused RL question: Can per-feature step-size adaptation track changing feature relevance in streaming TD prediction?

Setting/testbed: A nonstationary sensor prediction stream with an old-relevant group, a new-relevant group, and distractors.

Implemented comparison: TIDBD-lite versus fixed-alpha TD and normalized TD baselines.

Observation/metric: Prediction error, group-wise alpha trajectories, recovery windows, and planned recovery AUC and alpha-utility correlation.

Compute need: Small CPU-only runs.

Fallback: Keep the report as a mechanism diagnostic until canonical TIDBD or AutoStep and stronger recovery metrics are implemented.

## Conclusion

This proposal is an independent mechanism study of plasticity in streaming TD prediction. The current evidence supports a narrow conclusion: TIDBD-lite adapts feature-wise step sizes in an interpretable direction, but normalized TD still has slightly lower late prediction error. The project should therefore be reported as diagnostic evidence and a redesign target, with any stronger plasticity claim deferred until canonical adaptive step-size algorithms and recovery-focused metrics show a behavioral advantage.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/tidbd_plasticity/config_main.json
```
