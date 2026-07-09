# GVF Question Design

Status: independent useful-prediction design diagnostic; current evidence is for redesign, not for a completed GVF control claim.

## Abstract

This proposal studies a design problem that comes before using GVFs as agent state: which predictive questions are worth learning? A GVF can have low prediction error and still be useless if it predicts a constant, a locally visible signal, or a variable unrelated to the hidden information needed for control. The central message is therefore:

> prediction error != usefulness.

The current diagnostic uses a T-maze stream and trains linear GVF predictors for different cumulants and discount horizons. Bias predictions are easy but not useful; cue and junction questions expose the need to evaluate predictions by their relation to hidden cue information and downstream junction action. The contribution is a useful-prediction design diagnostic, not a final result showing that GVF state improves control.

## Claim Boundary

The report makes one bounded claim:

> In the current T-maze question-design diagnostic, low GVF prediction error is not enough to identify useful state features; GVF questions need explicit usefulness probes such as cue decodability and downstream control ablations.

The report deliberately does not claim:

- that the tested GVFs already solve T-maze control;
- that one cumulant/discount pair is universally best;
- that TD error is the main success metric;
- that predictive-state construction has been validated without downstream probes.

## Research Motivation/Question/Method

The Alberta Plan treats GVFs as a route toward rich predictive knowledge. That agenda requires not only learning answers, but also choosing questions. If an agent learns thousands of accurate but irrelevant predictions, the resulting state can be larger, slower, and no more useful for decision-making.

A T-maze makes the problem concrete. The task can be solved with a trace-like memory of the cue, but a recurrent GVF design can still fail if its questions do not preserve the relevant information. Such a failure should not be interpreted only as an algorithmic bug. It may indicate a question-design failure: the learned predictions did not preserve the control-relevant hidden cue at the junction.

### Focused RL Question

Main question:

> Which GVF cumulant and discount questions are merely learnable, and which are plausible candidates for useful predictive state in a partially observable T-maze?

Subquestions:

- Which GVFs have low TD error?
- Which GVFs preserve information about the hidden cue at the junction?
- Which GVF feature sets improve, do not affect, or harm downstream junction action?

Hypothesis:

> Prediction error alone will not identify useful GVF questions. A useful question must be evaluated by its relationship to hidden state information or downstream control.

### Core RL Connection

This is a core RL proposal because it studies prediction questions and state construction under partial observability. It connects to:

- GVFs and predictive knowledge;
- online agent-state construction;
- question discovery and evaluation;
- useful prediction rather than raw prediction accuracy;
- small interpretable diagnostics before control-scale experiments.

The proposal is independent because it asks a standalone design question: what should a GVF-based state learner predict?

### Related Work

Horde and GVF work motivate learning many predictions from a stream. Useful-prediction work asks which predictions improve learning or behavior. Online agent-state work motivates predictions as state features under partial observability.

Local references:

- `resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`
- `resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`
- `resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf`

### Method

The setting is a T-maze stream with observable signals:

- left cue;
- right cue;
- junction;
- bias.

The hidden control-relevant variable is the earlier cue that should determine the action at the junction. This makes the task useful for separating easy prediction from useful memory.

The method trains linear TD predictors for each cumulant and discount combination. The varied design factors are:

- cumulant identity;
- discount horizon.

Current cumulants:

- `left_cue`;
- `right_cue`;
- `junction`;
- `bias`.

Current discounts:

- `0`;
- `0.5`;
- `0.9`;
- `0.98`.

The current learner records prediction behavior. The next version must add explicit usefulness tests.

## Experimental Design

Current main diagnostic:

- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main`.

Current measurements:

- absolute TD error;
- prediction value;
- weight norm.

Primary figure:

![GVF TD error by cumulant and discount.](../../../../experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main/figures/abs_td_error_by_cumulant-gamma_curve.png)

Design logic:

| Design element | Why it is needed |
|---|---|
| Multiple cumulants | Separates trivial signals from cue-related and decision-location signals. |
| Multiple discounts | Tests whether horizon choice changes what information is preserved. |
| T-maze stream | Provides a simple partial-observability problem with known hidden cue. |
| TD error | Measures learnability, but not usefulness. |
| Planned cue probe | Measures whether the prediction helps recover the hidden variable. |
| Planned control ablation | Measures whether the prediction affects decision quality. |

## Results

The current run shows three qualitatively different categories:

- Bias GVFs are trivial and accurate, but not useful for cue memory.
- Cue GVFs have nontrivial errors and discount-dependent value profiles, making them plausible candidates for state features.
- Junction predictions are learnable, but by themselves do not solve the memory problem because the junction signal arrives where the decision is made rather than preserving the earlier cue.

The result supports the core diagnostic lesson: learnability and usefulness are different properties.

The current result summary gives this pattern in numerical form. Bias predictions at gamma `0`, `0.5`, and `0.9` have near-zero tail absolute TD error, while the long-horizon bias GVF at gamma `0.98` has tail absolute TD error around `0.1002`. Cue GVFs have tail absolute TD error around `0.0960-0.1666` across the tested discounts, and junction GVFs are around `0.1706-0.2563`. These numbers are useful for auditing learnability, but they do not answer whether the predictions preserve the hidden cue at the decision point.

## Analysis

The likely failure mechanism in the earlier GVF predictive-state design is not simply high prediction error. Several failure modes are possible:

- Trivial-prediction failure: a bias or local signal is predicted accurately but carries no hidden cue information.
- Horizon mismatch: the discount makes the prediction too myopic or too diffuse to preserve the cue until the junction.
- Location mismatch: a junction prediction marks the decision point but does not identify the correct action.
- Representation bottleneck: the GVF answer may be learned but not encoded in a way the controller can use.
- Objective mismatch: minimizing TD error can reward predictability rather than decision relevance.

These mechanisms explain why "low TD error" should not be treated as success. A useful-prediction proposal must ask "useful for what?" and answer with a measured probe.

## Next Experiments

The next experiments should make usefulness operational:

1. Cue-decodability probe: train a small linear probe from GVF outputs to the hidden cue at the junction.
2. Downstream control ablation: compare controllers with raw observations only, observations plus each GVF group, and observations plus trace-memory baseline.
3. Question-set ablation: test cue-only, junction-only, bias-only, and mixed GVF feature sets.
4. Horizon audit: measure how discount changes cue preservation at the decision point, not only TD error.
5. Negative controls: shuffle cue labels or use bias-only features to verify that probes do not report usefulness by accident.

The proposal should remain a design diagnostic until at least one usefulness metric is implemented.

## Threats To Validity

- Current usefulness is inferred, not directly measured.
- There is no hidden-cue linear probe yet.
- There is no downstream control ablation yet.
- The cumulant set is small and hand-designed.
- Current figures may overemphasize TD error because the usefulness metrics are still planned.

## Reviewer Critique

| Reviewer angle | Likely critique | Report response | Required next action |
|---|---|---|---|
| Useful prediction | Accuracy and usefulness are being conflated. | The report explicitly states prediction error != usefulness. | Add cue-decodability and control-usefulness metrics. |
| GVF reviewer | The question set is hand-designed and small. | The study is framed as a diagnostic, not automatic question discovery. | Add ablations and a principled question-selection table. |
| Control reviewer | No downstream decision test yet. | Evidence level is redesign guidance only. | Run junction-action ablations for each GVF feature set. |
| Strict instructor | Do not sell GVF state without showing state utility. | The claim is bounded to question-design diagnosis. | Keep final conclusion diagnostic unless usefulness probes pass. |

## Proposal Template Answers

Focused RL question: Which GVF questions are likely to become useful state rather than merely easy predictions?

Setting/testbed: A controlled T-maze prediction stream with cue, junction, and bias signals.

Implemented comparison: Linear GVF predictors over cumulant and discount choices.

Observation/metric: Current metrics are TD error, prediction value, and weight norm; required next metrics are cue decodability and downstream control ablation.

Compute need: Small CPU-only runs.

Fallback: Keep the study as a question-design diagnostic if downstream usefulness tests are not completed.

## Conclusion

This proposal is an independent focused study on GVF question design. Its current result is useful because it prevents a common mistake: treating accurate predictions as useful state without measuring what they preserve for control. The study remains a redesign target until it adds cue decodability and downstream action ablations; only then can it claim that a GVF question set improves state construction rather than merely producing learnable predictions.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/gvf_question_design/config_main.json
```
