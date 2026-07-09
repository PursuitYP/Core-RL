# Generate-and-Test Trace Features 中文报告

状态：独立负结果 proposal；当前 utility 规则需要重设计后才能升级为正向 representation-learning 课题。

## 摘要

本 proposal 研究一个 streaming agent 在 feature capacity 受限时，能否在 reward delay 改变后替换 stale temporal traces。Generate-and-test 是 continual representation learning 的核心思想之一：agent 应该在线生成候选 features，估计它们的 usefulness，并丢弃低价值 features。当前 trace-conditioning experiment 中，utility-based replacement 确实会移动 active trace timescales，有时让它们更接近目标 delay；但它没有降低 prediction error，相比 fixed 或 random baselines 不占优。这个结果很有价值，因为它说明“feature 参数看起来合理”不等于“feature 对 downstream prediction/control 有用”。

## 研究动机

长期 agent 不可能保留所有可能 feature。Sensor statistics、reward delays、task-relevant history lengths 都可能在 agent 运行过程中改变。固定 representation 可能把有限容量浪费在 stale features 上；无限增加 features 又违反 limited computation 和 small-agent 约束。Generate-and-test 的吸引力在于把 representation maintenance 变成一个在线算法问题：从 stream 中产生候选 features，用 utility 评估它们，并替换低 utility feature。

真正困难的是 utility。一个 trace feature 很活跃、timescale 接近 reward delay、或短期与 TD error 相关，并不必然说明它改善当前 predictor。这个 proposal 通过 delay-shift stream 检验 utility 是否真正服务预测误差和 recovery，而不是只制造看似合理的 feature dynamics。

## 研究问题

主问题：在固定 trace-feature budget 下，utility-based generate-and-test replacement 能否在 reward delay 改变后维护有用的 temporal traces？

假设是：一个有效 generate-and-test rule 应当在 post-change recovery 和 late prediction error 上优于 fixed trace banks 与 random replacement。当前证据不支持这个假设，因此报告必须作为负结果呈现。

## Alberta Plan 关联

Alberta Plan 中 feature finding 和 generate-and-test 是早期 base-agent 能力的重要部分。一个长期 agent 应该能维护自己的 representations，而不是依赖研究者离线设计所有 features。本实验使用小型线性 setting，使 replacement events、active timescales、prediction error 和 recovery windows 都可以被审计。

## 环境设计

环境是 trace-conditioning stream。Cue 出现后，reward 在某个 delay 后出现；stream 中途 delay 从 `10` 改为 `20`；learner 只能在线看一次 stream，没有 replay buffer 或 stored dataset。Feature budget 设置为很小，迫使 agent 选择少量 temporal traces，而不是把所有 plausible timescales 全部纳入。

这个环境的目的不是模拟复杂 control，而是隔离 limited feature budget 下的 continual representation maintenance。如果一个 feature-selection method 在这种清晰 setting 中都不能改善 prediction error，就不能直接把它接入更复杂 GVF/control task 宣称成功。

## 方法

比较策略包括 fixed tight trace bank、oracle trace bank、random replacement 和 generate-and-test replacement。当前 generate-and-test rule 在线估计 feature utility，并用新采样的 trace 替换低 utility features。Oracle bank 是诊断条件，但当前结果显示它本身也没有形成强上界，因此环境和 oracle design 都需要进一步验证。

## 实验设计

当前 main pilot 使用 feature budget `4`，delay switch 在 stream 中点发生，seeds `0-4`，steps `5000`。主要指标包括 absolute prediction error、active trace timescale 到 target delay 的距离、replacement count、recovery-window summaries 和 pre/post phase labels。结果路径是 `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`。

![Delay-shift prediction error by feature strategy.](../../../../experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main/figures/abs_error_by_algorithm_curve.png)

## 结果

Generate-and-test 有时会让 active trace timescales 更接近 target delay，说明 replacement mechanism 不是完全静止的。然而这个 structural improvement 没有转化为更低 prediction error。Late post-change absolute error 大约为：generate-test `0.0518`，fixed-tight `0.0512`，random replacement `0.0496`，当前 oracle-bank `0.0545`。

Oracle-bank 结果尤其重要。如果 oracle-style trace bank 不能明确优于 generic baselines，那么这个 testbed 还不足以作为 generate-and-test 的正向 promotion environment。当前实验暴露的是设计缺陷，而不是 feature learning 的成功案例。

## 分析

这个负结果至少有两种解释。第一，utility measure 与 prediction error 不对齐；它可能奖励了 feature 活动或局部相关，而不是 downstream TD-error reduction。第二，当前环境可能过于容易或 poorly conditioned，许多 trace banks 的表现接近，导致 feature replacement 的真实差异被淹没。

这并不否定 generate-and-test 思路。它否定的是更强的说法：当前 utility 和 replacement mechanism 已足以解决 delay-switch stream。它也提醒我们不要只看 qualitative feature inspection。Trace timescale 靠近目标 delay 不够，feature 必须改善 prediction error、recovery time 或 downstream control。

## 有效性威胁

当前 stream 只有一次 delay switch。更严肃的 representation-adaptation 研究应加入 repeated changes 和 varied delays。Oracle baseline 没有被验证成真正上界；promotion 前必须建立一个 known trace bank 会稳定赢的 validation stream。当前 utility rule 很紧凑，不能代表更强 generate-and-test 方法。任务是 prediction-only，未来 control task 可能对 traces 有不同需求。

## 审稿式批评与回应

Feature-learning reviewer 会说：feature-generation proposal 必须展示 utility，而不是只展示 plausible feature parameters。回应是：报告加入 prediction error、recovery windows 和 active-timescale diagnostics，并诚实报告 utility 未转化为 error 改善。

Strict reviewer 会指出：oracle 比 random 还差时，这个实验不能支持强结论。回应是：报告把它作为 underpowered/design-flaw signal，而不是 positive result。

下一步需要先构建一个 oracle trace bank 明确胜出的 validation stream，再测试 generate-and-test 是否能在 repeated delay changes 下恢复这个 bank。

## 结论

Generate-and-Test Trace Features 是一个有效的独立负结果。它说明 limited-capacity feature adaptation 是有意义的 Core RL 问题，但当前实现没有改善 prediction error。下一版需要更强 oracle、重复非平稳变化，以及直接绑定 recovery 或 downstream control 的 utility metric。

## Proposal Template Answers / 提案模板回答

Focused RL question：在 limited feature budget 下，generate-and-test replacement 能否发现改善 nonstationary delay prediction 的 trace features？setting 是 delay-switch trace-prediction stream；比较 random replacement、utility replacement 和 oracle-style trace banks。主指标是 downstream prediction error、active trace timescale、feature survival 和 post-switch recovery。compute 小；fallback 是 negative redesign result。

## 独立研究范围

这是独立负结果 representation-learning proposal。它没有证明 generate-and-test 成功；它说明当前 utility rule 和 testbed 不足。它不应被并入 Predictive State Plasticity 当作正向 feature-selection evidence。

## 证据等级

证据等级：negative/redesign。当前 utility rule 没有清楚优于 random replacement，oracle trace bank 也不够强，无法验证环境。这是设计失败信号，不是方法成功。

## 实验设计依据

这个任务只有在存在已知应当获胜的 feature bank 时才有价值。没有这个 validation，generate-and-test 失败会很模糊。下一版必须先构造 oracle traces 稳定降低 downstream error 的 stream，再测试 utility replacement 是否能在预算下恢复这些 traces。

## 审查矩阵

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| Representation | utility replacement 没有明显优于 random。 | 证据等级写成 negative/redesign。 | 需要 validated oracle trace bank。 |
| 实验设计 | oracle 不是清楚上界。 | 要求先验证 testbed。 | 当前结果无法公平评价 generate-and-test。 |
| 严格老师 | plausible feature dynamics 不等于成功。 | 成功标准必须是 downstream error/control improvement。 | 需要 feature-budget sweep 和 repeated switches。 |

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/generate_test_features/config_main.json
```
