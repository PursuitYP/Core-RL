# Predictive State Plasticity

## Abstract

Predictive knowledge is a central Alberta Plan idea, but a prediction is valuable to an agent only if it improves learning or control. The current GVF predictive-state experiment is a negative result: a simple trace-memory baseline solves a T-maze, while the learned GVF state remains near chance. This proposal turns that failure into a richer research program: how can a streaming agent with limited features select, adapt, and retain predictions that carry control-relevant hidden information?


## Standalone Study Summary

This study asks whether learned predictions become useful state for control under partial observability. The RL problem is a T-maze with an early hidden cue and a delayed junction decision; raw observation is insufficient unless the agent retains cue information. The current implemented comparison uses raw features, hand-coded trace memory, recurrent GVFs, redesigned cue GVFs, and oracle memory with online linear Sarsa control. The experiment varies maze length and representation mode; the main metrics are trial accuracy, cue-alignment margin, GVF TD error, and control TD error. The current result is a useful negative gate: cue-GVF outputs contain some cue-aligned signal but do not yet improve control over chance, while trace and oracle memory solve the task. The next experiment must separate GVF question design, output scaling, control utilization, and feature-selection/plasticity mechanisms.

## Research Motivation

Partial observability makes current observation insufficient. A long-lived agent must build state from history, but the course constraints rule out deep recurrent networks and replay. GVFs offer a Core RL alternative: predictions about future signals can become features. Generate-and-test offers a resource mechanism: create candidate features and discard weak ones. TIDBD offers a plasticity mechanism: adapt step sizes per feature. The interesting question is not whether any one mechanism looks plausible in isolation, but whether the agent can maintain useful predictive state under limited capacity.

## Research Question

When observations are aliased and the relevant memory timescale changes, what combination of predictive question design, feature replacement, and step-size plasticity helps a streaming linear agent maintain useful state?

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
- Generate-and-test replacement based on downstream TD-error contribution.
- TIDBD-style per-feature step-size adaptation.
- Combined generate-and-test plus TIDBD, treated as exploratory.

## Experimental Design

Primary environment:

- Long aliased T-maze.
- Cue appears at start and is hidden during the corridor.
- Correct junction action depends on the cue.
- Current implemented pilot keeps cue semantics fixed and varies corridor length. Phase-change experiments are planned but not yet implemented.

Secondary environment:

- Planned, not yet implemented: sensor-chain prediction/control task where the relevant delay switches repeatedly.

Conditions:

- Current implemented modes: raw observation, trace memory, recurrent GVF, cue GVF, and oracle memory.
- Current implemented corridor lengths: `8`, `12`, `20`.
- Planned, not yet implemented: fixed feature budgets `8`, `16`, `32`.
- Planned, not yet implemented: scheduled but unannounced phase switches.
- Seeds `0-19` for final sweeps.

Metrics:

- Trial-end accuracy and reward.
- GVF TD error.
- Mutual-information proxy or correlation between features and hidden cue.
- Recovery after phase switch.
- Feature survival and replacement counts.
- Per-feature alpha trajectories.
- Downstream value loss with and without each feature group.

## Expected Results And Failure Modes

Expected positive pattern: oracle memory and fixed trace memory should define upper bounds. Naive GVFs may fail unless their questions align with hidden cue information. Generate-and- test should help only if utility is tied to downstream control; TIDBD should reveal which features remain plastic after a phase switch.

Failure modes:

- Prediction error may favor easy but useless cumulants.
- Generate-and-test may churn features and destabilize control.
- TIDBD may adapt step sizes without solving representation selection.
- A hand-coded trace may remain a stronger baseline than learned GVFs; that is a valid negative result.

## Interpretation Standard

The proposal should not claim "GVFs work" unless the learned predictions visibly carry the hidden variable and improve control over cheap memory baselines. A negative result is still valuable if it identifies a concrete design constraint for useful predictions.

## Results

The existing GVF predictive-state run shows trace memory and oracle memory near `0.94` trial accuracy, while recurrent GVF remains near chance. The GVF question-design diagnostic also shows that easy predictions are not necessarily useful. Generate-and-test and TIDBD runs provide mechanism evidence but not yet a positive integrated state-construction story.

A dedicated first-gate pilot was added:

`experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main`

This pilot compares raw observation, trace memory, old recurrent GVF, redesigned cue-GVF, and oracle memory across T-maze lengths `8`, `12`, and `20`.

Main result:

- Trace memory and oracle memory solve all tested lengths, with tail trial accuracy around `0.93-0.96`.
- Raw observation and old recurrent GVF remain near chance.
- Redesigned cue-GVF has positive cue-alignment margins, so it carries some hidden-cue signal.
- Despite that, cue-GVF control accuracy remains near chance, about `0.47-0.49`.

Interpretation: the redesigned GVF is a better diagnostic signal but still not sufficient state. The next stage must either strengthen the predictive feature, improve how control uses it, or add explicit feature-plasticity/selection mechanisms.

Main figures below use seed-tail condition summaries with 95% confidence intervals. They show the current negative gate more clearly than the earlier overloaded curve plots: cheap trace/oracle memory works, while learned GVF features remain near chance.

![Tail trial accuracy by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main/figures/report_trial_accuracy_by_maze_length.png)

![Tail cue-alignment margin by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main/figures/report_cue_alignment_margin_by_maze_length.png)

![Tail GVF absolute TD error by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main/figures/report_gvf_abs_td_error_by_maze_length.png)

## Reviewer Critique And Revisions

Strict reviewer challenge: "The GVF result is negative, so why continue?" Response: the negative result is exactly the design signal. It says current GVF questions do not carry the cue; the next experiment must measure cue information and downstream usefulness directly.

Strict reviewer challenge: "This is too broad." Response: the proposal should be run in layers: first fixed useful GVF questions, then limited-budget selection, then step-size plasticity. The combined variant is not promoted until earlier layers pass.

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
