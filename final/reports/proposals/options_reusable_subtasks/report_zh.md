# Doorway Options for Reusable Subtasks

状态：quarantined negative-result study。本报告是一个独立 proposal，研究 doorway options 在 Four Rooms 中是否真的表现为 reusable subtasks。当前证据不支持 transfer claim；它说明在提出任何正向 reusable options 结论前，必须先通过 fixed-goal sanity checks，并显式验证 SMDP accounting。

## 摘要

Options 常被用来说明 temporally extended actions 可以改善 exploration、planning 和 transfer。本研究在一个有意保持小型的 Four Rooms navigation task 中，用 hand-coded doorway options 测试这个想法。核心方法规则是真实 environment-step accounting：option 可能把多个 primitive moves 压缩成一个 high-level decision，但它仍然消耗同样的 interaction steps。在当前 changing-goal pilot 中，如果按 reward per real environment step 衡量，primitive control 略优于 short 和 long doorway-option controllers。Options 会被选择，也有时能到达局部 doorway target，但它们的 commitment cost 没有换来更好的 goal recovery 或 final reward。因此当前结果应作为 quarantined negative pilot，而不是 reusable-subtask transfer 的证据。

## Proposal Template Answers / 提案模板回答

Focused RL question：在 Four Rooms 中，如果 performance 和 learning 都按真实 environment-step 和 SMDP duration accounting 评价，hand-coded doorway options 是否提供 reusable subtasks？

Setting/testbed：一个 larger Four Rooms navigation task，包含 primitive movement actions、连接房间的 doorways，以及 alternating goals。Agent 在线交互学习；main pilot 使用 seeds `0-4`，共 `5000` environment steps。

Implemented comparison：primitive control 与两个 option-augmented SMDP controllers 比较：primitive actions 加 short doorway options，以及 primitive actions 加 long doorway options。

Observation or metric：主指标是 reward per real environment step。诊断指标包括 option usage rate、option duration、option success、steps since goal switch，以及 goal changes 后的 recovery。

Compute need and fallback：实验是 CPU-scale，并可用 Reproduction 章节中的命令复现。Fallback 是在 fixed-goal sanity case 和 SMDP backup audit 通过前，将本研究保持为 quarantined negative accounting result。

## Research Motivation/Question/Method / 研究动机、问题与方法

Alberta Plan 的 STOMP/Oak 方向把 subtasks、options、option models 和 planning 看作 long-lived agents 的潜在组件。这个动机与本研究相关，但它并不意味着一个 option 只要在人看来 subgoal 自然就一定有用。Doorway 在 Four Rooms 中是 plausible subtask，但选择 doorway option 会让 agent 承诺执行多个真实 environment steps。如果 option 朝错误 doorway 移动、terminate 在无用状态，或者只按 decision count 评价，它可能看起来高效，但实际损失真实交互时间。

研究问题是：在真实 SMDP duration accounting 下，hand-coded doorway options 是否在 Four Rooms 中提供 reusable subtasks？

原始正向假设是：doorway options 会改善 navigation efficiency 和 goal changes 后的 recovery，因为移动到 doorways 是可复用 navigation subproblem。当前 pilot 不支持这个假设。它更保守地说明：如果按 real environment step 评价，option commitment 可能没有帮助，甚至会伤害表现。

方法是 Four Rooms 中的 online control。Primitive controller 选择四个 movement actions 之一。Option controllers 从 primitive actions 加 doorway-directed options 中选择。一个 option 会执行朝目标 doorway 移动的 primitive moves，直到 terminate 或达到 duration cap；随后 high-level learner 接收 accumulated option transition，并记录 duration。本报告的主张依赖这些 logged real-step metrics，但不声称所有 SMDP edge cases 已经完全验证。

正向未来版本的 accounting standard 必须比好看的曲线更严格：option duration `k` 必须进入 backup；option 执行期间的 cumulative reward 必须归入该 option transition；performance 必须按 environment step 报告；terminal 或 goal-change cases 不能隐藏额外 primitive steps。

## Experimental Design / 实验设计

当前 main pilot 是本报告使用的唯一结果。

| Item | Value |
|---|---|
| Environment | `larger_four_rooms` |
| Goal regime | Alternating goals |
| Algorithms | `primitive`, `short_options`, `long_options` |
| Seeds | `0-4` |
| Steps | `5000` |
| Result path | `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main` |

Independent variable 是 online learner 可用的 action set：只用 primitive actions、primitive actions 加 short doorway options，或 primitive actions 加 long doorway options。Primary dependent variable 是 reward per real environment step。Option usage、duration 和 success 是诊断变量，用来解释 option controller 为什么有用或无用。

主图：

![Reward per environment step with primitive actions and options.](../../../../experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main/figures/reward_per_env_step_by_algorithm_curve.png)

## Results / 结果

最终 seed-tail summaries 没有显示正向 option result。按 reward per real environment step 衡量，primitive control 仍然略优于 option variants。

| Controller | Reward per environment step | Diagnostic interpretation |
|---|---:|---|
| Primitive actions | `-0.00919` | 在已测试 controllers 中 final mean 最好。 |
| Short doorway options | `-0.00935` | Options 可用且被使用，但没有改善主指标。 |
| Long doorway options | `-0.00995` | 在 real-step accounting 下，较长 commitment 的成本最大。 |

Option diagnostics 说明负结果不只是因为 options 不可用。在 tail summaries 中，short options 的 decision 使用率约为 `0.222`，mean duration 约为 `1.576`，success 约为 `0.209`；long options 的 decision 使用率约为 `0.176`，mean duration 约为 `2.054`，success 约为 `0.438`。这些数字说明 options 确实参与了行为，但局部 option execution 没有转化为更好的 task reward。

这个结果应被理解为 unsupported transfer claim，而不是反对 options 的一般定理。当前 pilot 中的 option definitions、goal schedule、budget 和 accounting 没有产生相对 primitive control 的提升。

## Analysis / 分析

主要教训是：option availability 不等于 reusable-subtask evidence。Doorway option 也许解决了一个局部有意义的问题，但任务目标是在真实 interaction budget 下最大化 cumulative reward。如果 controller 花多个 steps 移动到一个对当前 goal 没用的 doorway，这个 abstraction 可能减少 decision count，却降低 reward per environment step。

有几个机制可以解释当前 pilot。第一，commitment cost 可能占主导：option 会花多个真实 steps 跟随一个可能与当前 goal 不一致的 subpolicy。第二，changing-goal regime 可能让先前合理的 doorway 在局部变 stale。第三，更大的 top-level action set 可能拖慢 value learning，特别是 option values 没有足够快学到时。第四，long options 可能在 decision-step plots 中看起来更好，因为它们减少 high-level choices，但 environment-step accounting 会暴露真实 interaction cost。

决定性限制是缺少 fixed-goal sanity case。Changing-goal transfer experiment 很难解释；除非相同 option definitions 先在 stationary setting 中有效，而在该 setting 里 doorway travel 本应有用。因此当前正确解释是 quarantined negative pilot：当前 setup 不支持 reusable-subtask transfer，而且 implementation/evaluation pipeline 仍需要一个更简单的 sanity win。

Fixed-goal sanity gate 应要求：固定 start-goal distribution；使用同一组 short 和 long doorway options；报告 reward per real environment step、steps to goal、option duration、option termination locations；并显式审计 SMDP backup 是否使用 duration 和 accumulated reward。如果 options 在该 setting 中都不能 match 或 beat primitive control，本研究就应继续作为 negative accounting result，而不是 transfer study。

## 局限与有效性威胁

当前 pilot 缺少 fixed-goal sanity case，因此无法区分失败来自 transfer 难度，还是 option implementation 本身普遍无用。

Options 是 hand-coded，因此本研究测试的是 option utility 和 accounting，不是 option discovery。

Learning budget 较小，可能不足以可靠估计 option values。

Goal-change schedule 可能比 stationary navigation task 更惩罚 commitment。

结果只使用五个 seeds 和一个 Four Rooms configuration，因此方向对诊断有用，但不足以支撑 general option claim。

当前报告强调 real-step performance 和 logged diagnostics，但任何正向未来版本都应更完整地审计 SMDP backup equations、discounting、accumulated reward，以及 terminal 或 goal-switch handling。

## Reviewer Critique / 审稿式批评

| Reviewer angle | Critique | Current treatment | Remaining risk |
|---|---|---|---|
| Research question | 题目容易变成“options 分数更高”，而不是 focused RL question。 | 报告明确为 real-step SMDP accounting 下 reusable subtasks 的窄问题。 | 正向版本仍需要更干净的 sanity experiment。 |
| Temporal abstraction | Doorway options 很 plausible，但 plausibility 不是 utility。 | 证据等级写成 quarantined negative。 | Transfer language 前需要 fixed-goal sanity win。 |
| Accounting | Decision-step metrics 会虚假偏向 options。 | Reward per real environment step 是主指标。 | 正向 claim 前需要 backup details 和 edge-case audit。 |
| Transfer | 没有 stationary success 时 changing-goal results 太早。 | Transfer 在 fixed-goal sanity 前被显式阻断。 | Sanity 后可能仍需重设 goal schedule。 |
| Interpretation | Negative pilot 可能被过度解释为“options 不工作”。 | 结论限制在当前 tested setup。 | 一般结论需要更多 environments 和 option definitions。 |

## Alberta Plan Connection / Alberta Plan 关联

本研究关联 temporal abstraction、reusable subtasks、option models、planning，以及 learned components 的 utility evaluation。它遵循 Alberta Plan 的纪律：组件应根据它们在 limited computation 和真实 interaction cost 下对 agent objective 的贡献来评价。当前结果有价值，因为它防止 overclaim：plausible subtask 不会自动成为 useful abstraction。

本地参考：

- `resources/alberta_plan_related/average_reward_options_2110.13855.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

## Conclusion / 结论

独立结论是保守的：在已测试的 changing-goal Four Rooms pilot 中，hand-coded doorway options 没有在 reward per real environment step 上优于 primitive control。当前 transfer claim 不受支持，应保持 quarantined。下一步不应扩大比较范围，而应先做 fixed-goal sanity experiment，并显式完成 SMDP accounting audit。只有相同 options 在干净 stationary 条件下确实有帮助后，才应重新打开 changing-goal transfer claim。

## Reproduction / 复现

现有结果路径：

```text
experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main
```

复现命令：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json
```

该命令会在 `experiments/alberta_core_rl/results/options_reusable_subtasks/` 下写入新的 timestamped directory。可将新的 `condition_summary.json`、`summary.json`、`metrics.csv` 和 reward curve 与上方现有 result path 对比。
