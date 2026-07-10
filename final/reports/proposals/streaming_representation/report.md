# Streaming Representation With Auxiliary Prediction

Status: independent negative auxiliary-prediction study. The current target should be redesigned around task-relevant predictions before any positive representation claim.

## Abstract

This study tests a common representation-learning intuition in a small streaming RL setting: adding an auxiliary prediction objective might improve the representation used for online value prediction. The experiment compares value-only normalized TD with a value learner that also predicts next features, using a nonstationary sensor stream and no replay. The result is negative: the auxiliary next-feature target does not materially reduce the main value-prediction error.

The result is useful because it shows that an auxiliary loss is not automatically a useful prediction. The auxiliary target must be relevant to the value or control question the agent is trying to answer. This proposal is therefore an independent negative result and redesign target, not evidence against auxiliary learning or GVFs in general.

## Evidence Summary

This report is a negative representation diagnostic. It asks a narrow but important question: does a convenient auxiliary target improve the downstream value prediction that actually matters? The answer in the current stream is no. That negative answer is useful because it prevents a common overclaim: an auxiliary prediction can be learnable without being useful for the agent's value question.

| Item | Current evidence |
|---|---|
| RL question | Does an auxiliary next-feature prediction objective improve online value prediction in a streaming linear setting without replay or deep networks? |
| Testbed | Nonstationary sensor stream with a feature-relevance switch; the learner observes features online and cannot revisit past transitions. |
| Compared learners | Value-only normalized TD versus normalized TD with an auxiliary next-feature prediction head. |
| Seeds and horizon | Five seeds, `5000` online steps per learner. |
| Primary metric | Seed-tail absolute TD error for the downstream value predictor; auxiliary MSE and weight norm are diagnostics. |
| Headline result | In phase 1, auxiliary next-feature prediction has absolute TD error `0.5298 +/- 0.0243`, while value-only TD has `0.5301 +/- 0.0240`; auxiliary MSE is low (`0.0413 +/- 0.0002`) but does not produce a value-error gain. |
| Conclusion boundary | Negative result for this auxiliary target; not evidence against auxiliary learning or GVFs generally. A stronger version needs task-relevant auxiliary questions and ablations. |

## 1. Proposal Template Answers

Focused RL question: Does an auxiliary next-feature prediction objective improve online value prediction in a streaming linear setting without replay or deep networks?

Setting/testbed: A nonstationary sensor stream with a feature-relevance switch. The learner observes features online and cannot revisit past transitions.

Implemented comparison: Value-only normalized TD versus normalized TD with an auxiliary next-feature prediction head.

Observation or metric: Absolute TD error is the primary downstream value metric. Auxiliary MSE, TD error, weight norm, and phase-specific summaries are diagnostic support.

Expected behavior: If next-feature prediction captures value-relevant structure, the auxiliary learner should reduce value-prediction error or improve recovery after the feature-relevance switch.

Compute need: Small CPU-only run with five seeds and 5000 online steps.

Fallback: Treat the current result as a negative diagnostic. A stronger project should compare task-relevant, task-irrelevant, and shuffled auxiliary predictions or move to a small control task.

## 2. Research Motivation / Question / Method

Streaming RL needs representations that can be learned online from ordinary experience. Auxiliary prediction is attractive because it can add learning signal without replay, large models, or offline pretraining. In principle, predicting aspects of the future could make the current representation more useful for value learning.

The research question is whether a simple auxiliary next-feature target improves online value prediction in this setting. The intended hypothesis was positive but conditional: next-feature prediction should help only if it captures structure needed for the value question.

The method compares two online learners under the same stream. The value-only learner runs normalized TD. The auxiliary learner adds a next-feature prediction loss. The auxiliary target is local and convenient, but it is not derived from reward, hidden state, control consequences, or a GVF-style cumulant. That distinction is the core of the diagnostic.

## 3. Experimental Design

Main run:

- Seeds: `0-4`.
- Steps: `5000`.
- Environment label in config: `nonstationary_sensor_auxiliary_prediction`.
- Result path: `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main`.
- Primary metrics: `abs_td_error`, `aux_mse`, and `weight_norm`.

Primary figure:

![Auxiliary representation diagnostic absolute TD error.](../../../../experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main/figures/abs_td_error_by_algorithm-phase_curve.png)

The primary outcome is downstream value-prediction error. Auxiliary MSE is secondary because low auxiliary prediction error alone would not prove that the learned signal is useful for the value task.

## 4. Results

The auxiliary prediction objective does not materially improve value prediction. In phase 1, seed-tail mean absolute TD error is about `0.5298` for the auxiliary method and `0.5301` for value-only learning. In phase 0, the corresponding values are about `0.4885` for the auxiliary method and `0.4877` for value-only learning.

The auxiliary learner does learn its auxiliary target to a stable level: seed-tail mean auxiliary MSE is about `0.0480` in phase 0 and `0.0413` in phase 1. That does not translate into a downstream value-error improvement. Weight norms are also nearly identical in phase 1, about `3.34` for both learners.

The result is therefore negative but informative. The correct conclusion is not that auxiliary learning fails in general. The narrower conclusion is that this next-feature target is not useful enough for the downstream value task in the current streaming diagnostic.

## 5. Analysis

The likely failure mechanism is target mismatch. Next-feature prediction can optimize information that is irrelevant to reward, irrelevant to the hidden feature switch, or already available in the current feature vector. In that case, the auxiliary loss consumes learning capacity without moving the representation toward value-relevant structure.

This is aligned with the Alberta Plan lens only as a cautionary example. Useful predictions should be useful questions: they should expose state, reward-relevant structure, controllable consequences, or temporally extended knowledge that helps the agent act and learn. A generic next-feature target does not guarantee any of these properties.

The next version should redesign the auxiliary question before adding larger experiments. Reasonable follow-ups include GVF-style cumulants tied to reward, termination, hidden phase, or controllable events; ablation or freeze tests of learned auxiliary features; task-relevant versus task-irrelevant auxiliary targets; and a small control task where usefulness can be judged by policy quality or average reward.

## 6. Threats To Validity

- The auxiliary architecture is intentionally small and may be too weak.
- The auxiliary target is not tied to reward, hidden state, or control.
- Five seeds are enough for a diagnostic but not for a broad representation-learning claim.
- The experiment does not test deep representation learning, which is outside the current course scope.
- Absolute TD error may miss representational effects that only appear under control or after feature freezing.

## 7. Reviewer Critique

| Reviewer critique | Current response | Required next action |
|---|---|---|
| The auxiliary target is arbitrary. | The report treats this as the central negative finding. | Redesign the auxiliary question around downstream usefulness. |
| Low auxiliary MSE does not imply useful representation. | The primary metric is downstream absolute TD error, not auxiliary loss. | Add ablations showing whether auxiliary features help value prediction. |
| The result could be architecture-specific. | The claim is limited to this small linear streaming diagnostic. | Compare target relevance before increasing model complexity. |
| This should not be cited against GVFs broadly. | The conclusion explicitly avoids that claim. | Test GVF-style cumulants tied to reward, phase, or controllable events. |

## 8. Conclusion

This proposal is an independent negative diagnostic for streaming representation learning. The current auxiliary next-feature target is learnable but does not improve the downstream value metric. The useful lesson is methodological: auxiliary predictions should be chosen as task-relevant questions, not added merely because they are easy to define.

## 9. Reproduction

Run from the repository root:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/streaming_representation/config_main.json
```

Expected result directory: `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main`.
