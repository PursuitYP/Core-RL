# Doorway Options for Reusable Subtasks

Status: quarantined negative-result study. This is an independent proposal about whether doorway options behave like reusable subtasks in Four Rooms. The current evidence does not support a transfer claim; it shows that fixed-goal sanity checks and explicit SMDP accounting must pass before any positive claim about reusable options.

## Abstract

Options are often motivated as temporally extended actions that can make exploration, planning, and transfer easier. This study tests that idea in a deliberately small Four Rooms navigation task using hand-coded doorway options. The core methodological rule is real environment-step accounting: an option may compress several primitive moves into one high-level decision, but it still consumes the same interaction steps. In the current changing-goal pilot, primitive control slightly outperforms both short and long doorway-option controllers when reward is measured per real environment step. Options are selected and sometimes reach their local doorway targets, but their commitment cost is not repaid by better goal recovery or better final reward. The result is therefore quarantined as a negative pilot rather than evidence for reusable-subtask transfer.

## Proposal Template Answers

Focused RL question: Do hand-coded doorway options provide reusable subtasks in Four Rooms when performance and learning are evaluated with real environment-step and SMDP duration accounting?

Setting/testbed: A larger Four Rooms navigation task with primitive movement actions, doorways connecting rooms, and alternating goals. The agent learns online from interaction; the main pilot uses seeds `0-4` for `5000` environment steps.

Implemented comparison: Primitive control is compared with two option-augmented SMDP controllers: primitive actions plus short doorway options, and primitive actions plus long doorway options.

Observation or metric: The primary metric is reward per real environment step. Diagnostic metrics include option usage rate, option duration, option success, steps since goal switch, and recovery after goal changes.

Compute need and fallback: The experiment is CPU-scale and reproducible with the command in the Reproduction section. The fallback is to keep the study quarantined as a negative accounting result until a fixed-goal sanity case and SMDP backup audit pass.

## Research Motivation/Question/Method

The Alberta Plan's STOMP/Oak direction treats subtasks, options, option models, and planning as possible components of long-lived agents. That motivation is relevant here, but it does not imply that an option is useful just because its subgoal looks natural to a human. A doorway is a plausible subtask in Four Rooms, yet choosing a doorway option commits the agent to several real environment steps. If the option heads toward the wrong doorway, terminates at an unhelpful state, or is evaluated only by decision count, it can appear efficient while losing real interaction time.

The research question is: do hand-coded doorway options provide reusable subtasks in Four Rooms under real SMDP duration accounting?

The intended positive hypothesis was that doorway options would improve navigation efficiency and recovery after goal changes because moving to doorways is a reusable navigation subproblem. The current pilot does not support that hypothesis. It instead supports the conservative interpretation that option commitment can fail to help, or can hurt, when evaluated per real environment step.

The method is online control in Four Rooms. The primitive controller selects one of the four movement actions. The option controllers select from the primitive actions plus doorway-directed options. An option executes primitive moves toward a selected doorway until it terminates or reaches its duration cap; the high-level learner then receives the accumulated option transition and logs its duration. The report's claim relies on the logged real-step metrics. It does not claim that every SMDP edge case has been fully validated.

The accounting standard for a positive future version is stricter than a good-looking plot: option duration `k` must enter the backup, cumulative reward during the option must be attributed to the option transition, performance must be reported per environment step, and terminal or goal-change cases must not hide extra primitive steps.

## Experimental Design

The current main pilot is the only result used in this report.

| Item | Value |
|---|---|
| Environment | `larger_four_rooms` |
| Goal regime | Alternating goals |
| Algorithms | `primitive`, `short_options`, `long_options` |
| Seeds | `0-4` |
| Steps | `5000` |
| Result path | `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main` |

The independent variable is the action set available to the online learner: primitive actions only, primitive actions plus short doorway options, or primitive actions plus long doorway options. The primary dependent variable is reward per real environment step. Option usage, duration, and success are diagnostic variables used to interpret why an option controller did or did not help.

Primary figure:

![Reward per environment step with primitive actions and options.](../../../../experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main/figures/reward_per_env_step_by_algorithm_curve.png)

## Results

The final seed-tail summaries do not show a positive option result. Primitive control remains slightly better than the option variants on reward per real environment step.

| Controller | Reward per environment step | Diagnostic interpretation |
|---|---:|---|
| Primitive actions | `-0.00919` | Best final mean among the tested controllers. |
| Short doorway options | `-0.00935` | Options are available and used, but do not improve the primary metric. |
| Long doorway options | `-0.00995` | Longer commitment is most costly under real-step accounting. |

The option diagnostics confirm that the negative result is not simply caused by options being unavailable. In the tail summaries, short options are used at about `0.222` of decisions with mean duration about `1.576` and success about `0.209`; long options are used at about `0.176` of decisions with mean duration about `2.054` and success about `0.438`. These numbers show that options are part of the behavior, but local option execution does not translate into better task reward.

The result should be read as an unsupported transfer claim, not as a general theorem against options. The tested option definitions, goal schedule, budget, and accounting produce no improvement over primitive control in this pilot.

## Analysis

The main lesson is that option availability is not the same as reusable-subtask evidence. A doorway option may solve a locally meaningful problem, but the task objective is cumulative reward under a real interaction budget. If a controller spends several steps moving toward a doorway that is not useful for the current goal, the abstraction can reduce decision count while still reducing reward per environment step.

Several mechanisms plausibly explain the pilot. First, commitment cost may dominate: an option spends multiple real steps following a subpolicy that can become misaligned with the current goal. Second, the changing-goal regime can make a previously sensible doorway locally stale. Third, the larger top-level action set may slow value learning if option values are not learned quickly enough. Fourth, long options can look better under decision-step plots because they make fewer top-level choices, while environment-step accounting exposes the true interaction cost.

The decisive limitation is the missing fixed-goal sanity case. A changing-goal transfer experiment is hard to interpret unless the same option definitions first help in a stationary setting where doorway travel should be useful. Until that gate passes, the correct interpretation is a quarantined negative pilot: the current setup does not support reusable-subtask transfer, and the implementation/evaluation pipeline still needs a simpler sanity win.

The fixed-goal sanity gate should require a fixed start-goal distribution, the same short and long doorway options, reward per real environment step, steps to goal, option duration, option termination locations, and an explicit audit that the SMDP backup uses duration and accumulated reward. If options cannot match or beat primitive control there, the study should remain a negative accounting result rather than a transfer study.

## Threats To Validity

The current pilot lacks the fixed-goal sanity case, so it cannot separate transfer difficulty from a generally unhelpful option implementation.

The options are hand-coded. This tests option utility and accounting, not option discovery.

The learning budget is small and may be too short for reliable option-value estimation.

The goal-change schedule may punish commitment more than a stationary navigation task would.

The result uses five seeds and one Four Rooms configuration, so the direction is useful for diagnosis but not broad enough for a general option claim.

The current report emphasizes real-step performance and logged diagnostics, but a positive future version should include a fuller audit of SMDP backup equations, discounting, accumulated reward, and terminal or goal-switch handling.

## Reviewer Critique

| Reviewer angle | Critique | Current treatment | Remaining risk |
|---|---|---|---|
| Research question | The topic can easily become "options scored higher" rather than a focused RL question. | The report states a narrow question about reusable subtasks under real-step SMDP accounting. | A positive version still needs a cleaner sanity experiment. |
| Temporal abstraction | Doorway options are plausible, but plausibility is not utility. | The evidence level is quarantined negative. | Needs a fixed-goal sanity win before transfer language. |
| Accounting | Decision-step metrics can falsely favor options. | Reward per real environment step is the primary metric. | Backup details and edge cases need audit detail before a positive claim. |
| Transfer | Changing-goal results are premature without stationary success. | Transfer is explicitly blocked until fixed-goal sanity passes. | The goal schedule may need redesign after sanity. |
| Interpretation | A negative pilot can be oversold as evidence that options do not work. | The conclusion is limited to this tested setup. | More environments and option definitions would be needed for a general conclusion. |

## Alberta Plan Connection

This study connects to temporal abstraction, reusable subtasks, option models, planning, and utility evaluation of learned components. It follows the Alberta Plan discipline that components should be judged by their contribution to an agent's objective under limited computation and real interaction cost. The current result is useful because it prevents an overclaim: a plausible subtask is not automatically a useful abstraction.

Local references:

- `resources/alberta_plan_related/average_reward_options_2110.13855.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

## Conclusion

The independent conclusion is conservative: in the tested changing-goal Four Rooms pilot, hand-coded doorway options do not improve reward per real environment step over primitive control. The current transfer claim is unsupported and should remain quarantined. The next valid step is not a broader comparison; it is a fixed-goal sanity experiment plus an explicit SMDP accounting audit. Only after the same options help under clean stationary conditions should the changing-goal transfer claim be reopened.

## Reproduction

Existing result path:

```text
experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main
```

Rerun command:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json
```

The command writes a fresh timestamped directory under `experiments/alberta_core_rl/results/options_reusable_subtasks/`. Compare the new `condition_summary.json`, `summary.json`, `metrics.csv`, and reward curve against the existing result path above.
