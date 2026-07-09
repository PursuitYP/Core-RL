# Doorway Options for Reusable Subtasks

Status: independent negative-result proposal; quarantined until a fixed-goal sanity case is established.

## Abstract

Options are often motivated as reusable temporally extended actions that can improve exploration and transfer. This proposal tests a minimal version of that idea in Four Rooms with doorway options and real environment-step accounting. The current main pilot finds that primitive actions slightly outperform short and long doorway options. Options are used, but they do not produce a positive transfer or sample-efficiency result under the tested setup. The proposal is therefore an honest temporal-abstraction failure analysis: options must pay for their commitment cost, and a future option study must first show a fixed-goal sanity win before claiming transfer.


## Standalone Study Summary

This study asks whether doorway options provide reusable temporal abstraction in Four Rooms style navigation. The RL problem is a continuing navigation task with primitive actions and temporally extended doorway options; the agent should improve environment-step efficiency and recover after goal changes. The implemented comparison is primitive control versus option-augmented SMDP control. The experiment tracks reward, steps to goal, option duration, environment-step accounting, and goal-change recovery. The current evidence does not support the option-transfer claim, so the proposal is quarantined. The next required step is a fixed-goal sanity experiment proving that option definitions and SMDP updates work before testing transfer.

## Research Motivation

The Alberta Plan's STOMP/Oak direction treats subtasks, options, option models, and planning as components that a long-lived agent may learn and evaluate. But temporal abstraction is not free. An option commits the agent to a behavior for multiple real environment steps. If that commitment is poorly matched to the current goal or if learning updates count only option decisions, options can appear useful while actually wasting interaction.

This proposal asks a practical Core RL question: do hand-coded doorway options help when we count the real cost of executing them?

## Research Question

When do doorway options help transfer across changing goals, and when does option commitment hurt performance per real environment step?

The current experiment answers the second half more clearly than the first: in the tested setup, option commitment does not help under real-step accounting.

## Alberta Plan Connection

The proposal targets:

- temporal abstraction;
- reusable subtasks;
- continuing control;
- computation and interaction cost;
- utility evaluation of learned components.

Although the options are hand-coded rather than discovered, the experiment is still useful because it tests whether the proposed temporal abstraction has measurable utility.

## Related Work

The options framework formalizes temporally extended actions. Average-reward option work supports continuing SMDP framing. The Alberta Plan's STOMP/Oak progression motivates evaluating subtasks and options by utility rather than assuming they help.

Local references:

- `resources/alberta_plan_related/average_reward_options_2110.13855.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

## Environment

The setting is Four Rooms. The agent navigates through rooms connected by doorways. The main run uses changing goals to test whether doorway options transfer.

Actions:

- primitive movements;
- short doorway options;
- long doorway options.

The key accounting rule is that performance is measured per real environment step, not per decision. This prevents long options from looking artificially efficient.

## Methods

Compared controllers:

- primitive action controller;
- controller with short doorway options;
- controller with long doorway options.

The option controllers use SMDP-style updates with option duration. Option usage, duration, and success are logged so that a negative result can be interpreted mechanistically.

## Experimental Design

Current main pilot:

- Larger Four Rooms setting.
- Alternating goals.
- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`.

Metrics:

- reward per environment step;
- option usage;
- option duration;
- option success;
- recovery after goal changes.

Primary figure:

![Reward per environment step with primitive actions and options.](../../../../experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main/figures/reward_per_env_step_by_algorithm_curve.png)

## Results

Primitive control remains slightly better than the option variants. Primitive reward per environment step is about `-0.00919`. Short options reach about `-0.00935`, and long options about `-0.00995`. The differences are small, but the direction is not a positive options result.

The important qualitative finding is that options are selected but do not help. Option availability alone is not enough; option policies and initiation/termination structure must match the task and learning budget.

## Analysis

This negative result is useful because it corrects a common reporting mistake. If option decision steps are counted as if they were environment steps, options can look better simply because they compress many actions into one decision. Real-step accounting removes that artifact.

The result does not show that options are bad. It shows that this option set, in this goal schedule, with this learning budget, does not justify its commitment cost.

## Threats To Validity

The current experiment does not include a fixed-goal sanity case where doorway options are expected to help. Without that gate, the transfer failure is hard to interpret.

The options are hand-coded. This tests option utility, not option discovery.

The learning budget may be too short for option-value learning.

The goal-change schedule may punish commitment more than a stationary navigation task would.

## Reviewer Critique And Revisions

Temporal-abstraction reviewer:

- The study must count real environment steps, not just option decisions.

Revision made:

- Main metrics use environment-step accounting and SMDP-style updates.

Strict reviewer concern:

- A transfer experiment is premature if options have not first helped in a fixed-goal task.

Required next revision:

- Add fixed-goal Four Rooms, prove the doorway options can help there, then test goal transfer with the same accounting.

## Conclusion

Doorway Options is an independent negative proposal. It contributes a useful lesson: options must be evaluated by real interaction cost and cannot be assumed helpful because they encode reasonable subtasks. The next version needs a fixed-goal sanity win, duration caps, and a clean transfer protocol before it can become a positive temporal-abstraction study.

## Proposal Template Answers

Focused RL question: Do hand-coded doorway options provide reusable subtasks under real environment-step accounting in a changing Four Rooms task? The setting is Four Rooms with changing goals; the comparison is primitive control versus option-augmented control. The main metrics are reward per real environment step, option duration, option success, and goal-switch recovery. Compute is small; fallback is quarantine until fixed-goal sanity passes.

## Independent Research Scope

This report studies hand-coded option utility and accounting, not option discovery. It is independent but currently quarantined because the primitive baseline is not beaten and the fixed-goal sanity check is missing.

## Evidence Level

Evidence level: quarantined negative result. The current evidence is useful mainly because it prevents an overclaim: options can look better under decision-step accounting while being worse or neutral under real environment-step accounting.

## Experiment Design Rationale

The next experiment must start with a fixed-goal sanity case. If doorway options cannot help or at least behave correctly in a stationary Four Rooms goal under real-step accounting, then goal-transfer results are uninterpretable. SMDP duration accounting and option termination diagnostics are required before reopening this as a positive temporal-abstraction proposal.

## Reviewer Audit

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| Options | No fixed-goal sanity check. | Evidence level is quarantined. | Must pass sanity before transfer claims. |
| Accounting | Decision-step metrics can falsely favor options. | Real environment-step reward is emphasized. | SMDP duration details need fuller reporting. |
| Strict instructor | Do not submit a failed options result as reusable-subtask evidence. | Report frames it as negative/quarantine. | Requires new experiment to revive. |

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json
```
