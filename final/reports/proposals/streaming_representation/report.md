# Streaming Representation With Auxiliary Prediction

Status: independent negative diagnostic; dropped as a final proposal unless redesigned.

## Abstract

This proposal asks whether a small auxiliary next-feature prediction objective improves streaming value prediction without replay or deep networks. The current nonstationary sensor-stream experiment finds no material improvement: auxiliary prediction and value-only learning have nearly identical late value-prediction error. The negative result is useful because it warns against a common shortcut: adding an auxiliary loss is not the same as learning a useful representation. The auxiliary question must be coupled to the downstream value problem.


## Standalone Study Summary

This study tests whether auxiliary prediction improves a streaming representation. The RL problem is an online prediction/control stream where the agent learns a main value prediction and an auxiliary next-feature prediction. The implemented comparison adds or removes auxiliary prediction features under the same online constraints. The experiment measures main prediction error, auxiliary error, and representation-related diagnostics. The current evidence is negative: the auxiliary next-feature prediction does not materially improve the main value prediction. The proposal should remain a redesign target unless a more relevant auxiliary question is introduced.

## Research Motivation

Recent streaming RL work often uses auxiliary prediction to improve representations from single-pass data. Under the course constraints, we cannot use deep encoders or replay, but we can test the underlying idea in a linear setting: does an auxiliary next-feature target provide useful information for value prediction in a nonstationary stream?

The answer in the current design is essentially no.

## Research Question

Can a small auxiliary next-feature prediction improve streaming value prediction without replay or deep networks?

Hypothesis:

> If the auxiliary target captures structure useful for value prediction, the auxiliary learner should reduce value TD error or improve recovery after a feature-relevance switch.

The current result does not support this hypothesis.

## Alberta Plan Connection

The proposal connects loosely to representation learning and streaming ordinary experience. However, it is weaker than the GVF and generate-and-test proposals because the auxiliary target is not clearly tied to a control-relevant question.

## Related Work

Streaming representation papers motivate auxiliary objectives under no-replay constraints. GVF/useful-prediction work provides a stricter lens: auxiliary predictions should be judged by downstream usefulness, not by auxiliary loss alone.

Local references:

- `resources/alberta_plan_related/squeezing_more_from_stream_2602.09396.pdf`
- `resources/alberta_plan_related/streaming_deep_rl_finally_works_2410.14606.pdf`
- `resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`

## Environment

The setting is a nonstationary sensor stream with a feature-relevance switch. The learner updates online and cannot revisit past transitions.

## Methods

Compared methods:

- value-only normalized TD;
- value TD with auxiliary next-feature prediction.

The auxiliary target is intentionally small and linear. This keeps the experiment within Core RL constraints but limits representational capacity.

## Experimental Design

Current main diagnostic:

- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main`.

Metrics:

- absolute TD error;
- auxiliary MSE;
- weight norm;
- phase.

Primary figure:

![Auxiliary representation diagnostic absolute TD error.](../../../../experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main/figures/abs_td_error_by_algorithm-phase_curve.png)

## Results

The auxiliary prediction objective does not materially improve value prediction. Phase-1 absolute TD error is about `0.5298` for the auxiliary method and `0.5301` for value-only.

The difference is too small to support a positive claim.

## Analysis

The result suggests that the auxiliary target is not sufficiently aligned with the value task. A next-feature prediction can be easy or well-optimized without improving the value learner's state.

This is closely related to the GVF Question Design result: useful representation requires useful questions. Auxiliary prediction should be selected because it helps a downstream agent, not because it is available.

## Threats To Validity

The auxiliary representation is minimal and may be too weak.

The auxiliary target is not explicitly tied to reward, hidden state, or control.

The experiment does not test deep representation learning, which is outside course scope.

The result is not a general negative claim about auxiliary learning.

## Reviewer Critique And Revisions

Representation reviewer:

- The proposal is too vague unless the auxiliary target is tied to downstream usefulness.

Decision:

- Drop as a final standalone proposal unless redesigned around a GVF-style useful prediction or a shared representation with measurable downstream benefit.

Upgrade path:

- Replace next-feature prediction with task-relevant GVF cumulants and add ablation of learned features in control.

## Conclusion

Streaming Representation With Auxiliary Prediction is a useful negative diagnostic. It shows that auxiliary prediction alone is not a research contribution unless the auxiliary question is connected to downstream value or control. The proposal should be redesigned or merged conceptually with GVF Question Design.

## Proposal Template Answers

Focused RL question: Does an auxiliary next-feature prediction target improve online value prediction in a streaming linear setting? The setting is a streaming prediction task with an auxiliary head; the comparison is value-only versus value-plus-auxiliary learning. The metrics are value error, auxiliary error, and phase/switch recovery. Compute is small; fallback is a negative diagnostic for useful-auxiliary-question design.

## Independent Research Scope

This proposal studies one auxiliary target, not representation learning in general. It should not be used as evidence against auxiliary learning or GVFs broadly. Its role is to show that an auxiliary target must be task-relevant to improve the main prediction/control objective.

## Evidence Level

Evidence level: negative diagnostic / redesign target. The current auxiliary prediction does not materially improve value error. That is useful because it prevents the shallow conclusion that any extra prediction makes representation better.

## Experiment Design Rationale

The experiment should be judged by downstream value error, not only auxiliary MSE. A future version needs task-relevant cumulants, learned-feature ablations, and downstream control metrics. Without those, the correct conclusion is that the chosen auxiliary question is not useful enough.

## Reviewer Audit

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| Representation | Auxiliary accuracy may not imply usefulness. | Evidence level is negative diagnostic. | Needs task-relevant GVF targets. |
| Metrics | Auxiliary MSE is not the main outcome. | Value error is emphasized. | Control metric remains absent. |
| Strict instructor | Do not call this representation learning success. | Report frames it as redesign target. | Should merge with GVF useful-question line if expanded. |

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/streaming_representation/config_main.json
```
