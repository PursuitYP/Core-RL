# Useful Predictive Knowledge Under Partial Observability

Status: independent integrated Core-RL proposal with a new Gate-1/Gate-2 experiment in progress. This study asks when a learned prediction becomes usable state for online control, not whether adding a prediction head improves a score.

## Abstract

The Alberta Plan places predictive knowledge near the center of agent state, but the phrase "learned prediction" hides two different requirements: the prediction must contain information about what matters, and the control learner must be able to use that information at the decision time. This proposal studies those requirements in a partially observable T-maze where a cue appears only at the start and the agent must remember it until a later junction. The experiment compares raw observation, hand-coded trace memory, oracle memory, and GVFs with different cumulants and horizons. The main claim is not that GVFs are good or bad in general; the claim is that useful predictive knowledge should pass explicit information and control gates before it is promoted to agent state.

## Standalone Study Summary

This study asks whether online learned predictions can become useful state under partial observability and limited computation. The RL problem is an aliased T-maze: the observation at the junction does not reveal which action is correct, so successful control requires carrying an early cue through a corridor. The implemented comparison uses linear Sarsa control with raw observations, trace memory, oracle cue memory, and GVF features built from cue, terminal-outcome, or junction cumulants at horizons `gamma = 0.8, 0.95, 0.99`. The experiment varies maze length and measures trial accuracy, decision-time cue decodability, signed cue margin, GVF TD error, and control TD error. A positive result requires a learned prediction to be both cue-informative and control-useful; low prediction error alone is not enough.

## Proposal Template Answers

Focused RL question: When does learned predictive knowledge become usable state for an online control agent under partial observability?

Setting and testbed: The primary testbed is a continuing stream of T-maze trials with a transient binary cue, an aliased corridor, and a delayed junction decision. The setting is small enough for complete instrumentation but not vacuous: raw observation is insufficient, trace and oracle memory show the task is solvable without deep networks, and GVF features must prove that they preserve the control-relevant hidden cue.

Implemented comparison: The current experiment compares raw observation, trace memory, oracle cue memory, cue-GVFs, terminal-outcome GVFs, and junction/bias GVFs. GVF horizons are swept over `0.8`, `0.95`, and `0.99`. All agents learn online with linear TD/Sarsa, no replay buffer, no deep network, and no offline training loop.

Observation or figure that answers the question: The primary evidence is the pair of decision-time cue decoding and trial accuracy by maze length and predictive question. A prediction that is accurate but cue-undecodable fails the information gate. A prediction that is cue-decodable but does not improve action accuracy fails the control-utilization gate.

Compute need and fallback: The experiment is CPU-scale. The fallback is scientifically meaningful: if GVFs reduce TD error but do not improve decodability or control, the conclusion is that prediction accuracy is not sufficient for useful agent state in this setting.

## Independent Research Scope

This proposal is independent from the other reports. It does not rely on another proposal's result to define its question, method, or conclusion. It uses a single environment family and a single staged criterion: predictive knowledge is useful only if it carries the hidden variable and improves downstream control. Later feature-selection and plasticity mechanisms are natural extensions, but they are not needed to interpret the current Gate-1/Gate-2 experiment.

The scope is deliberately narrower than a full Oak-style utility agent. This report studies the first necessary gate for learned knowledge: information and usability. It does not claim to solve feature discovery, option discovery, off-policy GVF stability, or long-term component management.

## Evidence Level

Evidence level will be determined by the completed main run `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json`, which uses 10 seeds, 12000 online steps, maze lengths `8`, `12`, and `20`, three baseline state constructions, three GVF question types, and three GVF horizons. A smoke run has already verified the runner and plotting path. Until the main artifacts are written, this report should be read as an implemented study with pending main evidence rather than a completed result.

## Research Motivation

A long-lived agent cannot treat all predictions as useful knowledge. Some predictions are easy to learn because their cumulants are frequent, local, or low variance; others are useful because they reveal a hidden variable at the time a decision must be made. These are not the same property. The Alberta Plan motivates agents that learn many value functions from ordinary experience, but it also raises a utility question: which learned signals deserve to become part of the agent's state?

Partial observability makes the question concrete. In the T-maze, the current observation at the junction is aliased. The agent must carry information from the initial cue to the later action. A hand-coded trace can do this cheaply; oracle memory can do it perfectly. A learned predictive feature must therefore be judged against two standards: does it preserve the cue, and does linear control use it?

## Research Questions

RQ1: Which predictive questions preserve the hidden cue at decision time: immediate cue cumulants, delayed terminal-outcome cumulants, or generic junction/bias cumulants?

RQ2: How does prediction horizon affect the tradeoff between cue retention and prediction usability as maze length increases?

RQ3: Does cue decodability translate into control accuracy, or can a learned prediction contain weak hidden-state information that the control learner still fails to use?

RQ4: What failure mode should guide the next stage: poor predictive information, poor output scaling, poor control utilization, or the need for feature-selection/plasticity?

## Related Work

The Alberta Plan motivates ordinary experience, value functions, GVFs, and agent-state construction. Horde-style GVF work shows why many predictions can be learned in parallel, but the current study asks a different question: which predictions should be trusted as state? Work on finding useful predictions motivates the cue-decoding and downstream-control gates, because predictive accuracy alone can reward easy questions rather than useful questions. Online agent-state construction motivates the trace/oracle controls: a candidate state feature should be compared to cheap memory baselines before claiming that prediction has solved partial observability. Streaming RL work motivates the no-replay constraint and the decision to use online linear learners rather than offline representation learning.

Useful local sources include `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`, `resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`, `resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`, `resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf`, and `resources/alberta_plan_related/squeezing_more_from_stream_2602.09396.pdf`.

## Research Method

The environment emits a binary cue at position `0`, then hides it through an aliased corridor. At the terminal junction, action `0` is correct for one cue and action `1` is correct for the other. The control learner is linear Sarsa with epsilon-greedy actions. The prediction learners are normalized linear TD learners whose outputs are appended to the raw observation as candidate state features.

Baseline state constructions are raw observation, trace memory, and oracle memory. Raw observation is the lower bound because it cannot see the cue after the start. Trace memory is a cheap non-deep history baseline. Oracle memory is an upper diagnostic that proves the task is solvable with linear control when the hidden cue is exposed.

GVF state constructions use two learned prediction outputs. Cue-GVFs predict the left/right cue observations; terminal-outcome GVFs predict left/right terminal outcomes; junction/bias GVFs predict a generic junction signal and bias. The junction/bias condition is intentionally included as a contrast: it may be easy or stable to predict but should not carry the hidden cue.

## Experimental Design

Main implemented run:

| Design element | Value |
|---|---|
| Config | `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json` |
| Seeds | `0-9` |
| Steps | `12000` online steps per condition |
| Maze lengths | `8`, `12`, `20` |
| State constructions | raw, trace memory, oracle, cue-GVF, terminal-GVF, junction-GVF |
| GVF horizons | `0.8`, `0.95`, `0.99` |
| Learners | normalized linear TD for predictions; normalized linear Sarsa for control |
| Constraints | no replay buffer, no deep network, no offline fitting |

Primary metrics:

| Metric | Role in the argument |
|---|---|
| `trial_accuracy` | Downstream control success at the delayed junction. |
| `decision_cue_decoding_correct` | Whether the candidate state feature still identifies the hidden cue at the decision point. |
| `cue_alignment_margin` | Signed strength of cue information in trace/oracle/GVF outputs. |
| `gvf_abs_td_error` | Prediction-learning diagnostic; secondary because low error alone does not prove usefulness. |
| `control_td_error` | Control-learning diagnostic for instability or poor utilization. |

## Experiment Design Rationale

The experiment is intentionally gate-structured. The first gate is information: a useful predictive state must be decodable with respect to the hidden cue. The second gate is control: the decodable information must improve junction decisions. This avoids the common mistake of treating low TD error as evidence of useful knowledge. A GVF that predicts a frequent junction event may have low error while still being irrelevant to the cue. A GVF that weakly encodes the cue may pass the information gate but fail the control gate if its output scale or noise prevents Sarsa from exploiting it.

Maze length is the memory-pressure variable. A short corridor can hide weak prediction failures because even crude traces retain enough cue information. Longer corridors force the predictive feature to preserve information over a longer delay. The horizon sweep asks whether the GVF timescale must match that delay.

## Expected Results And Failure Modes

The expected upper bound is oracle memory, followed by trace memory. Raw observation should approach chance except where the cue is still visible. Cue-GVFs and terminal-GVFs might retain some cue information, while junction/bias GVFs should be a negative control. A strong positive result would show both above-chance decision cue decoding and improved trial accuracy for a learned GVF condition across maze lengths. A mixed result would show cue decoding above chance but trial accuracy near chance; that would identify control-utilization or output-scale failure. A negative result would show both decodability and control near chance, motivating redesigned cumulants or different state-construction mechanisms.

## Current Results

The main run was launched from `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json`. This section will be replaced with completed main-run numbers and figures after `metrics.csv`, `condition_summary.json`, and report figures are written.

Planned primary figures:

- `figures/report_upk_trial_accuracy_by_length.png`
- `figures/report_upk_decision_decoding_by_length.png`
- `figures/report_upk_cue_margin_by_length.png`

## Reviewer Critique And Revisions

| Reviewer angle | Critique | Current response | Remaining risk |
|---|---|---|---|
| Alberta Plan | Predictive knowledge is too broad unless utility is operationalized. | The report defines utility as information plus downstream control use. | Later component-utility gates are still outside this experiment. |
| Core RL | The T-maze could be too small. | It is small but structurally meaningful: raw observation fails and trace/oracle baselines solve the hidden-state problem. | A second delayed-cue stream would strengthen generality. |
| GVF reviewer | Prediction error is not the right target. | GVF TD error is secondary; cue decodability and trial accuracy are primary. | Better GVF question families may be needed. |
| Statistics | Many conditions can obscure the main claim. | The figures group by maze length and gate metric rather than showing every learning curve. | A compact table of best GVF per length should be added after results. |
| Strict instructor | Do not call this a solution to agent-state construction. | The report is framed as Gate 1 and Gate 2 only. | Feature-budget and plasticity stages remain future work. |

## Threats To Validity

The T-maze isolates partial observability but does not cover all forms of agent-state construction. The GVF designs are still hand-selected; a poor result might reflect poor question design rather than a limitation of predictive knowledge. The cue-decoding metric is a proxy for information and does not replace downstream control. Conversely, a control improvement without decodability would require careful interpretation because it might exploit a correlate rather than the hidden cue. The current main run uses 10 seeds; stronger final evidence may require 20 seeds or a CPU-task extended sweep once the first results identify the most informative conditions.

## Conclusion

This proposal converts the broad Alberta Plan idea of predictive knowledge into a concrete Core-RL test: a prediction should become state only if it preserves the hidden variable and improves downstream control. The experiment is deliberately small but not toy in the bad sense; it has a real partial-observability failure mode, solvable non-deep baselines, GVF question and horizon ablations, and metrics that distinguish prediction accuracy from usefulness. The scientific value is the gate itself: it can support a positive learned-state result, or it can identify exactly why the current predictions are not yet useful enough.

## Reproduction

Run the main experiment:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json
```

Generate report figures:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind useful-predictive-knowledge \
  --result-dir experiments/alberta_core_rl/results/useful_predictive_knowledge/<timestamp>_main \
  --figure-dir final/reports/integrated/useful_predictive_knowledge/figures
```
