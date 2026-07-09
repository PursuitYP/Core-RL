# Doorway Options for Reusable Subtasks 中文报告

状态：独立负结果 proposal；在固定目标 sanity case 通过前保持 quarantined。

## 摘要

Options 常被用来说明 reusable temporally extended actions 可以改善 exploration 和 transfer。本 proposal 在 Four Rooms 中测试一个最小版本：hand-coded doorway options 与真实 environment-step accounting。当前 main pilot 发现 primitive actions 略优于 short 和 long doorway options。Options 确实被使用，但在测试设置下没有产生正向 transfer 或 sample-efficiency 结果。因此本 proposal 是一个 honest temporal-abstraction failure analysis：options 必须为 commitment cost 付费；未来 option study 必须先证明 fixed-goal sanity win，再讨论 transfer。

## 研究动机

Alberta Plan 的 STOMP/Oak 方向把 subtasks、options、option models 和 planning 看作 long-lived agent 的组件。但 temporal abstraction 不是免费的。Option 会让 agent 承诺执行多步真实环境动作；如果 option policy 与当前 goal 不匹配，或实验只按 decision count 而不是 environment step 计数，options 会看起来高效但实际浪费交互。

本 proposal 的实际问题是：当我们诚实计算真实 environment steps 时，hand-coded doorway options 是否仍然有 utility？

## 研究问题

主问题：doorway options 在 changing-goal Four Rooms 中何时帮助 transfer，何时因为 commitment cost 伤害 per-real-step performance？

当前实验更清楚地回答了第二部分：在测试设置下，real-step accounting 下 option commitment 没有帮助。

## Alberta Plan 关联

该 proposal 关联 temporal abstraction、reusable subtasks、continuing control、interaction cost 和 learned component utility evaluation。尽管 options 是 hand-coded 而非 learned，实验仍有价值，因为它测试 proposed abstraction 是否真正有可测 utility。

## 环境与方法

环境是 Four Rooms navigation。Agent 在房间之间通过 doorways 移动，goal 会变化以测试 doorway options 是否 transfer。动作包括 primitive movements、short doorway options 和 long doorway options。关键 accounting rule 是 performance 按真实 environment step 衡量，而不是按 option decision 数衡量，以避免 long option 因隐藏多个 primitive steps 而被虚假奖励。

比较 controllers 包括 primitive action controller、short-option SMDP controller 和 long-option SMDP controller。Option usage、duration 和 success 都被记录，用于解释负结果。

## 实验设计

当前 main pilot 使用 larger Four Rooms setting、alternating goals、seeds `0-4`、steps `5000`。结果路径是 `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`。主要指标包括 reward per environment step、option usage、option duration、option success 和 goal-change recovery。

![Reward per environment step with primitive actions and options.](../../../../experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main/figures/reward_per_env_step_by_algorithm_curve.png)

## 结果

Primitive control 略优于 option variants。Primitive reward per environment step 约 `-0.00919`；short options 约 `-0.00935`；long options 约 `-0.00995`。差异不大，但方向不是 positive options result。定性上更重要的是：options 被选择了，但没有帮助。这说明 option availability 本身不够，option policy、initiation/termination structure 和 learning budget 必须与任务匹配。

## 分析

这个负结果纠正了 options 实验中常见的报告错误。如果只按 decision steps 计数，options 可能显得更快，因为一次 option decision 包含多个 primitive actions。按 real environment steps 计数后，这个 artifact 被移除。

结果不说明 options 一般无用。它说明当前 option set、goal schedule 和 learning budget 下，doorway options 没有证明自己值得付出 commitment cost。

## 有效性威胁

当前实验还缺 fixed-goal sanity case。如果 doorway options 在固定目标任务中都不能稳定帮助，那么 transfer failure 很难解释。Options 是 hand-coded，因此测试的是 option utility，不是 option discovery。Learning budget 可能太短，goal-change schedule 也可能过度惩罚 commitment。

## 审稿式批评与回应

Temporal-abstraction reviewer 会要求按真实 environment steps 评估，而不是 option decisions。回应是：当前指标已经使用 environment-step accounting 和 SMDP-style updates。

Strict reviewer 会指出：没有 fixed-goal sanity win 就谈 transfer 太早。回应是：报告把 proposal quarantined，并要求先做 fixed-goal Four Rooms。

## 结论

Doorway Options 是独立负结果。它贡献的教训是：options 必须按真实 interaction cost 评估，不能因为它们编码了合理 subtask 就假设有用。下一版需要 fixed-goal sanity win、duration caps 和更干净的 transfer protocol。

## Proposal Template Answers / 提案模板回答

Focused RL question：hand-coded doorway options 在 changing Four Rooms task 中，按真实 environment-step accounting 是否提供 reusable subtasks？setting 是 changing-goal Four Rooms；比较 primitive control 和 option-augmented control。主指标是 reward per real environment step、option duration、option success 和 goal-switch recovery。compute 小；fallback 是 fixed-goal sanity 通过前 quarantine。

## 独立研究范围

本报告研究 hand-coded option utility 和 accounting，不研究 option discovery。它是独立课题，但当前 quarantined，因为 primitive baseline 没有被击败，而且 fixed-goal sanity check 缺失。

## 证据等级

证据等级：quarantined negative result。当前证据主要用于防止 overclaim：options 在 decision-step accounting 下可能看起来更好，但在真实 environment-step accounting 下可能更差或无优势。

## 实验设计依据

下一步必须从 fixed-goal sanity case 开始。如果 doorway options 在 stationary Four Rooms goal 下按 real-step accounting 都不能帮忙或至少行为正确，那么 goal-transfer result 无法解释。重新作为正向 temporal-abstraction proposal 前，必须补 SMDP duration accounting 和 option termination diagnostics。

## 审查矩阵

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| Options | 没有 fixed-goal sanity check。 | 证据等级为 quarantined。 | transfer claim 前必须通过 sanity。 |
| Accounting | decision-step metrics 会虚假偏向 options。 | 强调 real environment-step reward。 | SMDP duration 仍需更完整报告。 |
| 严格老师 | 不要把失败 options 结果写成 reusable-subtask evidence。 | 报告定位为 negative/quarantine。 | 需要新实验才能恢复。 |

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json
```
