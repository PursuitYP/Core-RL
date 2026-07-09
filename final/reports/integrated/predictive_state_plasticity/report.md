# Predictive State Plasticity

Status: integrated but high-risk proposal. The current submission-grade evidence is a 20-seed first-gate negative study: learned cue-GVF features do not yet become useful control state. Generate-and-test, TIDBD, and feature-replacement mechanisms are staged next steps, not completed evidence in the present report.

## Abstract

Predictive knowledge is a central Alberta Plan idea, but a prediction is valuable to an agent only if it improves learning or control. The extended GVF predictive-state experiment is a negative result: trace memory and oracle memory solve a partially observable T-maze, while the learned GVF state remains near chance even with 20 seeds, 20000 online steps, and maze lengths up to 30. This proposal turns that failure into a sharper research program: how can a streaming agent with limited features select, adapt, and retain predictions that carry control-relevant hidden information?


## Standalone Study Summary

This study asks whether learned predictions become useful state for control under partial observability. The RL problem is a T-maze with an early hidden cue and a delayed junction decision; raw observation is insufficient unless the agent retains cue information. The implemented comparison uses raw features, hand-coded trace memory, recurrent GVFs, redesigned cue GVFs, and oracle memory with online linear Sarsa control. The extended experiment varies maze length and representation mode over 20 seeds and 20000 online steps; the main metrics are trial accuracy, cue-alignment margin, GVF TD error, and control TD error. The result is a useful negative gate: cue-GVF outputs have some cue-aligned signal but do not improve control over chance, while trace and oracle memory solve the task. The next experiment must separate GVF question design, output scaling, control utilization, and feature-selection/plasticity mechanisms.

## Proposal Template Answers

Focused RL question: In a partially observable online control task, can learned predictions carry the hidden cue information needed for later action, or does the agent need a different state-construction mechanism? The present report answers this as a first-gate question about fixed learned GVF features, not as a completed feature-plasticity result.

Setting and testbed: The testbed is an aliased T-maze with an early binary cue and a delayed junction decision. It is intentionally sharper than a generic benchmark: raw observation is insufficient, trace/oracle memory can solve the task, and learned predictive state must prove that it carries useful hidden information.

Implemented comparison: The completed experiment compares raw observation, trace memory, recurrent GVF, cue GVF, and oracle memory with online linear Sarsa. Generate-and-test, TIDBD, feature replacement, and phase-change plasticity are staged next experiments, not current evidence.

Observation or figure that answers the question: The main evidence is trial accuracy by maze length, supported by cue-alignment margin and GVF TD error. A low GVF TD error or a small positive cue-alignment signal is not enough; the learned prediction must improve junction decisions over raw observation and move toward trace/oracle memory.

Compute need and fallback: The extended first-gate run is complete. If no further experiments are run, the honest fallback is to submit this as a negative/redesign proposal: current cue-GVF predictions do not yet become useful state, and the next work is diagnostic rather than performance polishing.

## Independent Research Scope

This proposal is an independent representation and partial-observability study. It does not depend on the ordinary GVF Predictive State report, although that report is a smaller precursor. It also should not be merged with Generate-and-Test or TIDBD reports as if those mechanisms already produced a successful predictive-state learner. The current scope is fixed predictive state under T-maze partial observability; feature replacement and per-feature step-size adaptation are later stages gated on whether a useful predictive feature can first be demonstrated.

The proposal explicitly does not claim that GVFs fail in general. It claims that the current cue-GVF and recurrent-GVF constructions do not carry or expose the cue strongly enough for downstream linear control in this setting. This boundary is important because it turns a negative result into a design constraint rather than a broad dismissal of predictive knowledge.

## Evidence Level

Evidence level: high-value negative gate with 20-seed extended evidence. The completed run covers maze lengths `8`, `12`, `20`, and `30`, five representation modes, and 20000 online steps per condition. The evidence is strong enough to say that the current learned GVF features do not become useful state in this T-maze.

The evidence is not a positive plasticity result. It does not yet include cue-decodability probes, oracle-prediction control, GVF output normalization, feature ablations, phase switches, generate-and-test replacement, or canonical TIDBD/AutoStep. Those missing experiments are not minor details; they are the necessary next gates for turning the negative result into a stronger research program.

## Research Motivation

Partial observability makes current observation insufficient. A long-lived agent must build state from history, but the course constraints rule out deep recurrent networks and replay. GVFs offer a Core RL alternative: predictions about future signals can become features. Generate-and-test offers a resource mechanism: create candidate features and discard weak ones. TIDBD offers a plasticity mechanism: adapt step sizes per feature. The interesting question is not whether any one mechanism looks plausible in isolation, but whether the agent can maintain useful predictive state under limited capacity.

## Research Question

Current first-gate question:

> Before adding feature replacement or step-size plasticity, can fixed learned GVF features carry the hidden cue well enough to improve online linear control over raw observation and approach cheap trace memory?

Longer staged-program question:

> When observations are aliased and the relevant memory timescale changes, what combination of predictive question design, feature replacement, and step-size plasticity helps a streaming linear agent maintain useful state?

The present evidence answers only the first question. It is negative, and that negative result determines whether the larger staged program is worth pursuing.

## Related Work

The Alberta Plan emphasizes GVFs, feature finding, and agent-state construction. Horde shows that many off-policy predictions can be learned in parallel. Useful-prediction work warns that prediction accuracy alone is not the right objective. Recurrent generate-and-test and TIDBD provide two mechanisms for adapting state features and feature-wise learning rates.

Useful local sources:

- `resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`
- `resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`
- `resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf`
- `resources/alberta_plan_related/tidbd_1804.03334.pdf`
- `resources/alberta_plan_related/streaming_deep_rl_finally_works_2410.14606.pdf`
- `resources/alberta_plan_related/squeezing_more_from_stream_2602.09396.pdf`

## Research Method

The agent controls a partially observable task using linear action values over a fixed feature budget. Candidate features include:

- current observation,
- fixed decay traces,
- GVF predictions with cue/junction/reward cumulants,
- generated traces with learned decay parameters,
- generated GVF questions selected by usefulness.

Learning variants:

- Fixed feature set with ordinary TD/Sarsa.
- Fixed feature set with normalized updates.
- Planned generate-and-test replacement based on downstream TD-error contribution.
- Planned TIDBD-style per-feature step-size adaptation.
- Planned combined generate-and-test plus TIDBD, treated as exploratory and only worth running after the fixed useful-GVF gate is understood.

## Experimental Design

Primary environment:

- Long aliased T-maze.
- Cue appears at start and is hidden during the corridor.
- Correct junction action depends on the cue.
- Current implemented extended run keeps cue semantics fixed and varies corridor length. Phase-change experiments are planned but not yet implemented.

Secondary environment:

- Planned, not yet implemented: sensor-chain prediction/control task where the relevant delay switches repeatedly.

Conditions:

- Current implemented modes: raw observation, trace memory, recurrent GVF, cue GVF, and oracle memory.
- Current implemented corridor lengths: `8`, `12`, `20`, `30`.
- Planned, not yet implemented: fixed feature budgets `8`, `16`, `32`.
- Planned, not yet implemented: scheduled but unannounced phase switches.
- Seeds `0-19` and `20000` online steps in the extended first-gate run.

Metrics:

- Trial-end accuracy and reward.
- GVF TD error.
- Mutual-information proxy or correlation between features and hidden cue.
- Recovery after phase switch.
- Feature survival and replacement counts.
- Per-feature alpha trajectories.
- Downstream value loss with and without each feature group.

## Experiment Design Rationale

The T-maze is used because it forces a clean separation between observation and state. If the agent does not retain the initial cue, the junction action is close to chance. Trace and oracle memory are included not as strawmen but as necessary controls: they show that the task is solvable under the course constraints and define how far the learned predictive feature is from a cheap memory baseline.

The current extended run is a gate rather than a full program. Maze length tests whether cue retention survives longer delays. Cue-alignment margin asks whether the learned feature contains any hidden-cue signal. Trial accuracy asks the stricter question of whether control can use that signal. GVF TD error is deliberately secondary because an accurate prediction can still be useless for control.

## Expected Results And Failure Modes

Expected positive pattern: oracle memory and fixed trace memory should define upper bounds. Naive GVFs may fail unless their questions align with hidden cue information. Generate-and-test should help only if utility is tied to downstream control; TIDBD should reveal which features remain plastic after a phase switch.

Failure modes:

- Prediction error may favor easy but useless cumulants.
- Generate-and-test may churn features and destabilize control.
- TIDBD may adapt step sizes without solving representation selection.
- A hand-coded trace may remain a stronger baseline than learned GVFs; that is a valid negative result.

## Interpretation Standard

The proposal should not claim "GVFs work" unless the learned predictions visibly carry the hidden variable and improve control over cheap memory baselines. A negative result is still valuable if it identifies a concrete design constraint for useful predictions.

## Results

The existing GVF predictive-state run shows trace memory and oracle memory near `0.94` trial accuracy, while recurrent GVF remains near chance. The GVF question-design diagnostic also shows that easy predictions are not necessarily useful. Generate-and-test and TIDBD runs provide mechanism evidence but not yet a positive integrated state-construction story.

A dedicated extended first-gate run was added:

`experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`

This run compares raw observation, trace memory, old recurrent GVF, redesigned cue-GVF, and oracle memory across T-maze lengths `8`, `12`, `20`, and `30`, using seeds `0-19` and `20000` online steps per condition.

Main result:

- Trace memory and oracle memory solve the shorter and medium lengths; trace memory remains far above chance even at length `30`, though it drops to about `0.827 +/- 0.013`.
- Oracle memory remains near `0.931-0.950` across all tested lengths.
- Raw observation and old recurrent GVF remain near chance.
- Redesigned cue-GVF has some positive cue-alignment margin at shorter lengths, but the margin weakens as length grows.
- Cue-GVF control accuracy remains near chance across all tested lengths: about `0.504`, `0.508`, `0.505`, and `0.494` for lengths `8`, `12`, `20`, and `30`.

Interpretation: the redesigned GVF is a better diagnostic signal but still not sufficient state. The current result should be stated as "the learned GVF does not carry or expose the cue strongly enough for control," not as "GVFs cannot carry the cue." The next stage must separate information content from control utilization by adding cue-decodability probes, oracle-prediction controls, GVF output normalization, and then feature-plasticity/selection mechanisms.

Main figures below use seed-tail condition summaries with 95% confidence intervals. They show the current negative gate more clearly than the earlier overloaded curve plots: cheap trace/oracle memory works, while learned GVF features remain near chance.

![Tail trial accuracy by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_trial_accuracy_by_maze_length.png)

![Tail cue-alignment margin for GVF-based state constructions.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_cue_alignment_margin_by_maze_length.png)

![Tail GVF absolute TD error for GVF-based state constructions.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_gvf_abs_td_error_by_maze_length.png)

## Reviewer Critique And Revisions

Strict reviewer challenge: "The GVF result is negative, so why continue?" Response: the negative result is exactly the design signal. It says current GVF questions do not carry the cue; the next experiment must measure cue information and downstream usefulness directly.

Strict reviewer challenge: "This is too broad." Response: the proposal should be run in layers: first fixed useful GVF questions, then limited-budget selection, then step-size plasticity. The combined variant is not promoted until earlier layers pass.

Per-proposal audit matrix:

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| Alberta Plan | GVFs matter only if predictions become useful state. | The report evaluates control accuracy, not only prediction error. | Current GVF questions still fail the useful-state gate. |
| Partial observability | The task could be impossible without deep recurrence. | Trace and oracle baselines solve the task. | Learned prediction needs a stronger information probe. |
| Representation | Cue alignment may exist but be unusable by control. | Reports both cue-alignment margin and trial accuracy. | Needs cue decodability and GVF output normalization. |
| Plasticity | Generate-and-test and TIDBD are not yet tested in the integrated loop. | The report now marks them as staged future work. | A positive plasticity claim requires new experiments. |
| Strict instructor | Do not sell a broad negative result as a broad GVF conclusion. | Conclusion is limited to the current cue-GVF/recurrent-GVF designs. | Better GVF questions may reverse the result. |

## Threats To Validity

The current result is intentionally a gate, not a positive final claim. The T-maze is a controlled partial-observability test, but the learned GVF design is still weak and the control learner may not use small predictive margins effectively. A negative cue-GVF result could mean the GVF question is wrong, the representation of the GVF output is poorly scaled, the control step size is wrong, or the task requires a different memory mechanism. The next version must separate these possibilities by adding stronger oracle-prediction controls, an explicit cue-information metric, and feature-selection/plasticity ablations.

## Conclusion

This proposal remains ambitious and risky. Its value is that it refuses the shallow claim that "adding GVFs helps"; instead it asks whether predictions become useful state for control under partial observability. The first-gate pilot shows that the current cue-GVF has some cue-aligned information but is not yet a useful control state. That negative result is scientifically useful because it identifies the next design constraint: a predictive feature must be both informative about the hidden variable and usable by the downstream control update.

## Reproduction

Current first-gate pilot:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/predictive_state_plasticity/config_main.json
```

Extended sweep config:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/predictive_state_plasticity/config_extended.json
```

Regenerate the report figures:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind predictive-state \
  --result-dir experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended
```
