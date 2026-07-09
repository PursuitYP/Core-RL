# GVF Predictive State

Status: independent negative-result proposal and redesign target.

## Abstract

This proposal tests whether learned General Value Function predictions can serve as useful agent state under partial observability. In a long aliased T-maze, the agent sees a cue at the start, loses direct access to it in the corridor, and must remember it at the junction. The current main pilot compares raw observation, short history, trace memory, recurrent GVF features, and oracle memory. Trace memory and oracle memory solve the task, while the current recurrent GVF design remains near chance. This is a valuable negative result: it does not refute GVFs, but it shows that the current GVF question/state design fails to carry the hidden cue information required for control.


## Standalone Study Summary

This study asks whether GVFs can serve as useful agent state in a partially observable control task. The RL problem is a T-maze where an early cue determines the correct later junction action. The implemented representations are raw observation, short history, hand-coded trace memory, recurrent GVF features, and oracle memory; control uses online linear Sarsa. The experiment measures trial-end accuracy, reward, GVF values, cue traces, GVF TD error, and control TD error. The current evidence is negative: trace and oracle memory solve the task, while the current recurrent GVF representation remains near chance. The result is valuable as a redesign target, not as a claim that GVFs generally fail.

## Proposal Template Answers

Focused RL question: Can a learned GVF feature supply the missing cue information needed for control in a partially observable T-maze? This is a useful-state question, not a prediction-error question.

Setting and testbed: The testbed is a long aliased T-maze. The agent sees a cue at the start, loses direct access to it in the corridor, and must act on that cue at the junction. This makes hidden-state retention observable through trial-end accuracy.

Implemented comparison: The pilot compares raw observation, short history, trace memory, recurrent GVF features, and oracle cue memory under online linear Sarsa. Trace and oracle are not decorative baselines; they show that the task is solvable without deep networks.

Observation or figure that answers the question: The main evidence is trial-end accuracy, supported by position-level GVF/trace trajectories. A GVF feature must approach trace memory or at least improve over raw observation; lower GVF TD error alone would not count.

Compute need and fallback: The current result is a five-seed pilot. The fallback is to report it as a negative redesign target and require stronger evidence from additional seeds, corridor lengths, and cue-decodability probes.

## Independent Research Scope

This proposal owns one narrow question: does the current recurrent GVF design become useful state in a T-maze? It does not evaluate broader representation-learning machinery beyond this GVF-state mechanism.

The scope is intentionally limited because the result is negative. It should not be used to claim that GVFs cannot construct state. It should be used to motivate better GVF question design, direct cue-decodability probes, and a stricter useful-prediction evaluation.

## Evidence Level

Evidence level: negative pilot/redesign target. The result is convincing enough to show that the current recurrent-GVF pilot should not be submitted as a positive GVF-state result. It remains limited by five seeds and one maze length.

The central failure mechanism is clear: cheap trace memory solves the task, while the current recurrent GVF does not. Any stronger claim about predictive state should require larger runs and direct cue-decodability evidence.

## Research Motivation

In partially observable environments, current observation is not state. A long-lived agent must construct state from experience. The Alberta Plan proposes GVFs as a major route: predictions about future signals can become knowledge used by the agent. This idea is powerful, but it has a sharp failure mode. A prediction can be accurate, stable, and still useless for the decision the agent must make.

The goal of this proposal is therefore not to make a decorative auxiliary prediction. The goal is to ask whether a learned prediction can carry missing information that the control policy needs.

## Research Question

Can learned GVF predictions supply missing cue information in a partially observable T-maze?

More specifically:

> Does adding a recurrent GVF feature improve trial-end control accuracy over raw observation and short history, and does it approach a cheap trace-memory baseline?

The trace-memory baseline is intentionally strong and cheap. A learned GVF state should not be promoted if a simple non-deep memory trace solves the task and the GVF does not.

## Alberta Plan Connection

This proposal targets:

- GVFs and predictive knowledge;
- agent-state construction;
- partial observability;
- online value learning;
- useful predictions rather than prediction accuracy alone.

It is highly aligned with the Alberta Plan, but the current result is negative and must be reported honestly.

## Related Work

GVF and Horde work motivates learning many predictive questions from experience. Work on useful predictions asks which predictions actually help an agent. Online agent-state work motivates recurrent trace-like state construction. Recent streaming partial-observability papers show that no-replay, batch-size-one memory remains an active problem, though those papers often use deep recurrent architectures outside this course project's constraints.

Local references:

- `resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`
- `resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`
- `resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf`

External context:

- Streaming RL under Partial Observability with Real-Time Recurrent Learning: https://arxiv.org/abs/2605.24709

## Environment

The testbed is a long aliased T-maze:

- At the start, the observation reveals a binary cue.
- Along the corridor, observations are aliased and do not reveal the cue.
- At the junction, the correct action depends on the cue.
- After the junction decision, the trial resets with a new cue.

The task is continuing in the sense that the agent keeps learning over many trials, but the accuracy metric is measured at trial-end decisions.

## Methods

State constructions compared:

- raw observation;
- short history;
- trace memory;
- recurrent GVF features;
- oracle cue memory.

The oracle defines an upper bound. The trace memory baseline asks whether the task is solvable by simple non-deep memory. The GVF variant is the actual proposal mechanism.

## Experimental Design

Current main pilot:

- Maze length: `12`.
- Seeds: `0-4`.
- Steps: `5000`.
- Metrics: trial-end accuracy, average reward, GVF TD error, cue traces, position-level trajectories.
- Result path: `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`.

Figures:

![Trial accuracy by state construction.](../../../../experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main/figures/trial_accuracy_by_algorithm_curve.png)

![GVF values and cue traces by maze position.](../../../../experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main/figures/gvf_trace_by_position.png)

## Experiment Design Rationale

The T-maze creates a minimal but meaningful partial-observability problem. Raw observation is insufficient by construction, but trace and oracle memory make the task solvable with small non-deep features. This lets the experiment ask whether the GVF mechanism adds useful state rather than whether the task is impossible.

The current design is a pilot because it tests one maze length and one GVF design. It is still useful because the negative result is sharp: the recurrent GVF does not improve control over chance while trace memory succeeds. The next design should not merely tune alpha; it should add hidden-cue probes and redesign cumulants/discounts so the learned prediction is explicitly tied to the cue.

## Results

Trace memory and oracle memory solve the task, with seed-aware tail trial accuracy about `0.944 +/- 0.018` and `0.939 +/- 0.027`. This establishes that the task is learnable with small non-deep state augmentation.

Raw observation, short history, and recurrent GVF remain near chance: about `0.512`, `0.492`, and `0.502`. The current GVF state therefore does not carry the cue information needed by the control decision.

The trajectory figure supports this interpretation. The learned GVF signal does not show a clean cue-dependent trace that persists to the junction in the way the hand-coded trace does.

## Analysis

This is not a failed experiment; it is a useful negative result. It separates three possibilities:

- The task might be impossible under the course constraints.
- The control algorithm might be broken.
- The current GVF question/state design might be insufficient.

The trace and oracle baselines rule out the first possibility. The remaining conclusion is that the GVF feature, as designed, is not the right predictive state. That is exactly the kind of boundary condition a serious GVF proposal should expose.

## Threats To Validity

The current GVF design is only one design. It should not be used to claim that GVFs cannot construct state.

The report currently lacks a direct linear probe of cue information from the GVF feature. The conclusion is inferred from control accuracy and trajectory plots.

The maze has a fixed length. A richer result should sweep corridor length and cue semantics.

The GVF cumulant/discount choices may not be aligned with the hidden variable. A fairer positive test requires question-design diagnostics before control evaluation.

## Reviewer Critique And Revisions

GVF reviewer:

- A GVF that predicts an easy but irrelevant signal is not useful state.

Revision made:

- Added trace memory and oracle memory, plus position-level trajectory plots.

Strict baseline reviewer:

- If trace memory solves the task, the GVF must approach or beat that baseline to be promoted as a positive state-construction result.

Revision required:

- Add cue-decodability probes, hidden-cue correlation plots, and redesigned cumulants tied to future cue-relevant events.

Reviewer audit matrix:

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| GVF | Prediction accuracy is not the same as useful state. | Reports trial accuracy and trace/oracle baselines. | Direct cue-decodability is still missing. |
| Baseline | If trace memory solves the task, GVF must approach it. | Trace and oracle are included as strong baselines. | GVF remains near chance. |
| Evidence | Five seeds and one maze length are limited. | Report is framed as a negative pilot. | Needs more seeds, maze lengths, and direct cue probes. |
| Alberta Plan | GVFs are important, so negative evidence must be precise. | Conclusion limits the claim to the current GVF design. | Better GVF questions may succeed. |
| Strict instructor | Do not present this as a positive proposal. | Status and conclusion call it a redesign target. | Final materials must preserve the negative evidence level. |

## Conclusion

The current GVF Predictive State proposal is an independent negative result. It shows that the task is solvable by cheap memory but not by the current learned GVF feature. The next iteration should not merely tune hyperparameters; it should redesign the GVF questions so that the learned prediction is demonstrably tied to the hidden cue and useful for the junction decision.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/useful_gvfs_state/config_main.json
```
