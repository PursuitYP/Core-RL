# GVF Question Design

Status: independent diagnostic study for GVF redesign.

## Abstract

This proposal studies a design problem that sits before GVFs can be used as agent state: which predictive questions are worth learning? In a T-maze stream, we train linear GVF predictors for different cumulants and discounts. The current run shows that some questions are easy but not useful, such as bias predictions, while cue and junction questions expose the difference between prediction accuracy and downstream state relevance. The study is not a final control result; it is a principled diagnostic for designing useful predictive state.


## Standalone Study Summary

This diagnostic study asks which GVF questions are useful, not merely predictable. The RL problem is a controlled prediction setting where different cumulants/questions can be learned online and compared for downstream relevance. The implemented GVF learners differ in cumulant and horizon. The experiment measures GVF prediction error, cue relevance, and utility proxies for downstream state construction. The current evidence supports an important design lesson: easy predictions are not necessarily useful state. The next step is to connect the best question candidates to the T-maze control task.

## Research Motivation

GVFs are often described as predictive knowledge, but a prediction is only useful to an agent if it helps answer a decision-relevant question. A low-error GVF can be useless if it predicts a constant or a signal unrelated to the hidden variable needed for control.

The failed GVF Predictive State experiment makes this design issue concrete. A recurrent GVF did not solve the T-maze even though the task was solvable by trace memory. This diagnostic asks what questions should be considered before inserting GVFs into the control state.

## Research Question

Which GVF cumulant/discount questions are easy to predict, and which look potentially useful for T-maze state construction?

Hypothesis:

> Prediction error alone will not identify useful GVF questions. Useful questions must be evaluated by their relation to hidden cue information or downstream control.

## Alberta Plan Connection

The proposal targets:

- GVFs;
- predictive knowledge;
- agent-state construction;
- question discovery and evaluation;
- useful prediction rather than raw prediction accuracy.

It is an independent study because question design is a prerequisite for any GVF-based state proposal.

## Related Work

Horde and GVF work motivate learning many predictions. Useful-prediction work asks which predictions improve learning or behavior. Online agent-state work motivates predictions as state features under partial observability.

Local references:

- `resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`
- `resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`
- `resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf`

## Environment

The setting is a T-maze stream with signals:

- left cue;
- right cue;
- junction;
- bias.

The hidden control-relevant variable is the cue that should determine the junction action.

## Methods

Linear TD predictors are trained for each cumulant and discount combination. The study varies:

- cumulant identity;
- discount horizon.

It records prediction errors and value profiles, but interprets them through the lens of usefulness.

## Experimental Design

Current main diagnostic:

- Cumulants: `left_cue`, `right_cue`, `junction`, `bias`.
- Discounts: `0`, `0.5`, `0.9`, `0.98`.
- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main`.

Metrics:

- absolute TD error;
- prediction value;
- weight norm.

Primary figure:

![GVF TD error by cumulant and discount.](../../../../experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main/figures/abs_td_error_by_cumulant-gamma_curve.png)

## Results

Bias GVFs are trivial and accurate, but they are not useful state. Cue GVFs have nontrivial errors and discount-dependent predictions. Junction predictions are predictable, but they do not directly solve cue memory.

The result shows that easy prediction and useful prediction are different categories.

## Analysis

The diagnostic explains why the current GVF predictive-state design failed. Selecting GVFs because they are easy or stable can produce features that do not preserve the hidden cue. For T-maze control, the right diagnostic is not just TD error; it is whether a prediction helps decode the cue at the junction.

The next version should add explicit cue-decodability metrics and downstream junction-action tests for each GVF feature set.

## Threats To Validity

The current study infers usefulness rather than directly testing each GVF feature in control.

It does not yet include a linear probe for hidden cue information.

The cumulant set is small and hand-designed.

The result is diagnostic; it should not be treated as a final GVF state-construction claim.

## Reviewer Critique And Revisions

Useful-prediction reviewer:

- Accuracy and usefulness must be separated.

Revision made:

- The report explicitly labels bias GVFs as easy but not useful.

Strict reviewer concern:

- A GVF question-design study needs a downstream usefulness metric.

Required next revision:

- Add cue-decodability and downstream control ablations for each cumulant/discount group.

## Conclusion

GVF Question Design is a valuable independent diagnostic. It shows why a GVF proposal must ask "what is this prediction for?" before adding predictions as state. The study should feed directly into a redesigned GVF Predictive State proposal with usefulness metrics.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/gvf_question_design/config_main.json
```
