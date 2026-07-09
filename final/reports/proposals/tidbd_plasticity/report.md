# TIDBD-Lite Plasticity

Status: independent supporting mechanism study; not yet a positive performance proposal.

## Abstract

This proposal studies per-feature step-size adaptation as a lightweight plasticity mechanism for streaming TD prediction. In a nonstationary sensor stream, feature relevance changes after a phase switch. A TIDBD-style learner should increase step sizes for newly useful features while keeping distractors quiet. The current main pilot shows this mechanism qualitatively: new-feature step size rises after the switch and distractor step size stays low. However, normalized TD still has lower late prediction error than the current TIDBD-lite implementation. The proposal is therefore a mechanism study, not a performance win.


## Standalone Study Summary

This study examines per-feature step-size plasticity in a streaming prediction setting. The RL problem is not a full control task; it is a diagnostic stream where feature relevance changes and a learner must adapt without replay. The implemented method is TIDBD-lite, compared with fixed or normalized TD baselines. The experiment records prediction/TD error, feature-group behavior, per-feature alpha trajectories, and post-change adaptation. The current evidence shows visible step-size adaptation but no clear prediction-error advantage over normalized TD. The study is therefore a supporting mechanism diagnostic, not a positive performance proposal.

## Research Motivation

Continual agents face changing feature relevance. A fixed global step size is a compromise: large enough to adapt quickly, but small enough not to destabilize irrelevant or noisy features. Per-feature step-size adaptation offers a more local form of plasticity.

The Alberta Plan treats step-size adaptation and feature utility as early building blocks for long-lived agents. This proposal asks whether a simple per-feature adaptive TD learner can detect changing relevance in the stream itself.

## Research Question

Can per-feature step-size adaptation track changing feature relevance in streaming TD?

Hypothesis:

> After a relevance switch, a TIDBD-style learner should increase step sizes for newly relevant features, maintain lower step sizes for distractors, and recover prediction accuracy faster than fixed-alpha TD.

The current result supports the first two mechanism claims but not the stronger prediction error claim.

## Alberta Plan Connection

The proposal connects to:

- meta-learning of step sizes;
- online prediction;
- continual adaptation;
- feature relevance tracking;
- limited computation with linear function approximation.

It is not a deep plasticity study. The point is to inspect feature-wise learning-rate dynamics in a small streaming setting.

## Related Work

TIDBD extends incremental delta-bar-delta ideas to TD learning with feature-wise step sizes. The Alberta Plan mentions per-weight step-size adaptation as part of early continual learning. Plasticity work in continual learning motivates recovery and feature-level diagnostics, though much of that literature uses deep networks outside this project.

Local references:

- `resources/alberta_plan_related/tidbd_1804.03334.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

## Environment

The setting is a nonstationary sensor prediction stream:

- one feature group is relevant before a switch;
- a different group becomes relevant after the switch;
- distractor features remain mostly irrelevant;
- the learner updates online without replay.

This is a mechanism environment. It creates controlled feature-relevance changes that can be measured directly.

## Methods

Compared methods:

- fixed TD with alphas `0.01`, `0.03`, `0.1`;
- normalized TD;
- TIDBD-lite.

The local implementation is deliberately labeled TIDBD-lite. It is not claimed to be a full canonical reproduction of all TIDBD details.

## Experimental Design

Current main pilot:

- Seeds: `0-4`.
- Steps: `5000`.
- Switch: halfway through the stream.
- Result path: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`.

Metrics:

- absolute TD error;
- old-relevant feature step sizes;
- new-relevant feature step sizes;
- distractor step sizes;
- recovery windows.

Primary figure:

![Absolute TD error for TIDBD-lite and TD baselines.](../../../../experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main/figures/abs_td_error_by_algorithm_curve.png)

## Results

TIDBD-lite shows the intended feature-wise plasticity signal. New-feature step size rises from about `0.0068` before the switch to about `0.0093` in the late post-change window. Distractor step size remains near `0.0068`.

However, normalized TD remains the stronger prediction-error baseline. Late post-change absolute TD error is about `0.4419` for normalized TD and about `0.4493` for TIDBD-lite. This means the mechanism signal does not yet justify a performance claim.

## Analysis

The proposal separates two claims that are often conflated:

- The learner changes step sizes in a sensible feature-specific direction.
- That adaptation improves the prediction objective.

The first claim is supported. The second is not yet supported. This distinction makes the proposal scientifically useful: it identifies a mechanism that behaves plausibly but is not strong enough under the current environment and implementation.

## Threats To Validity

The implementation is TIDBD-lite, not a canonical TIDBD reproduction.

The environment has one switch. Repeated changes may better expose plasticity advantages.

Normalized TD is a strong baseline because it controls update size directly; a fair final study should compare per-feature adaptation and output normalization more systematically.

The current metrics do not include feature correlation or utility contribution beyond step-size groups.

## Reviewer Critique And Revisions

Plasticity reviewer:

- Mean step size alone is insufficient.

Revision made:

- Added group-wise old/new/distractor step-size logs and recovery windows.

Strict reviewer concern:

- Do not call a local simplified algorithm "TIDBD" without qualification.

Revision made:

- The report uses TIDBD-lite terminology.

Required next revision:

- Implement canonical TIDBD or AutoStep, add repeated relevance switches, and report recovery AUC rather than only late error.

## Conclusion

TIDBD-Lite Plasticity is a valid independent mechanism proposal, but not yet a positive performance story. It shows meaningful per-feature step-size adaptation after a relevance switch, while normalized TD remains stronger on prediction error. The next version should upgrade the algorithm and environment before making broader claims about plasticity.

## Proposal Template Answers

Focused RL question: Can per-feature step-size adaptation track changing feature relevance in a streaming prediction/control setting? The current setting is a TIDBD-lite diagnostic, not canonical TIDBD. The comparison is TIDBD-lite versus fixed/normalized TD-style baselines; the metrics are prediction error, alpha trajectories, relevance switches, and recovery. Compute is modest; fallback is a mechanism diagnostic until canonical TIDBD or AutoStep is implemented.

## Independent Research Scope

This report studies feature-wise plasticity signals, not a finished performance method. It should not be merged into Predictive State Plasticity as completed positive evidence. Its role is to show whether alpha dynamics respond to relevance changes and what remains missing.

## Evidence Level

Evidence level: supporting mechanism diagnostic. The current TIDBD-lite implementation shows interpretable alpha dynamics, but normalized TD has stronger error in some conditions. Therefore the report cannot claim that TIDBD-lite improves performance.

## Experiment Design Rationale

The experiment is useful only if it separates "alpha changes visibly" from "learning improves." The next design should implement canonical TIDBD/AutoStep, add repeated relevance switches, and report recovery AUC, not only final error.

## Reviewer Audit

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| Algorithm | TIDBD-lite is not canonical TIDBD. | Evidence level is diagnostic. | Needs canonical TIDBD/AutoStep. |
| Performance | Alpha adaptation may not improve error. | Report distinguishes alpha dynamics from prediction gain. | Normalized TD may remain stronger. |
| Strict instructor | Do not use plasticity language without utility evidence. | Required next metrics include recovery AUC and repeated switches. | Current result is supporting only. |

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/tidbd_plasticity/config_main.json
```
