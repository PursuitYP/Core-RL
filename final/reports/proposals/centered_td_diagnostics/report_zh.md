# Centered TD Diagnostics 中文报告

状态：独立机制诊断；作为 Reward-Centered Sarsa 的 supporting study，而不是主控制结论。

## 摘要

本 proposal 在小型 continuing prediction problem 中隔离 reward centering 的机制。通过比较 ordinary TD、reward-centered TD 和 Bellman-error-centered diagnostic updates 在 reward translation 下的行为，它展示 centering 如何改变 value scale。当前 run 表明 reward-centered TD 在不同 reward shifts 下保持较小 value norms，而 ordinary TD 学到很大的 shift-dependent values。这个 study 的贡献是解释 Reward-Centered Sarsa 为什么更稳定，而不是单独作为最终主 benchmark。

## 研究动机

Reward centering 如果只在完整 control task 中展示 reward 更好，很难说清它到底改变了什么：是 policy 更好、value scale 更稳、TD error 更小，还是只是某个 alpha 更合适。在 continuing task 中，给所有 rewards 加一个常数会向 discounted value prediction 注入巨大常数项。这个常数项通常对行为偏好没有帮助，却会主导 value norms 和 TD errors。

因此需要一个更小的 diagnostic MDP，把 reward shift、TD target、value norm 和 baseline tracking 分开观察。这个 proposal 的价值就在于回答“为什么 centering 会帮助主实验”。

## 研究问题

主问题：不同 centering method 移除了什么 offset，它们如何影响 reward translation 下的 value scale？

假设是：相比 ordinary TD，reward-centered TD 应显著降低 learned value scale 对 additive reward shifts 的依赖。

## Alberta Plan 关联

该 proposal 支持 continuing prediction、average-reward-style normalization、value-function diagnostics 和“先用可解释小实验理解机制，再进入较大 control task”的研究方式。它刻意很小，不应被过度包装。

## 环境与方法

环境是 two-loop continuing MDP，使用 random behavior 和可控 reward shifts。它比 access-control 小得多，专门用于暴露 value-scale mechanics。比较方法包括 ordinary TD、reward-centered TD 和 Bellman-error-centered diagnostic update。每个 learner 都从 stream 在线更新，不使用 replay 或 offline fitting。

## 实验设计

当前 main diagnostic 使用 reward shifts `-5/0/5`，seeds `0-4`，steps `5000`，结果路径为 `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main`。主要指标包括 value norm、TD error、reward baseline 和 delta baseline。

![Value norm by centering method and reward shift.](../../../../experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main/figures/value_norm_by_algorithm-reward_shift_curve.png)

## 结果

Reward-centered TD 在不同 shifts 下保持较小 value norm：shift `-5` 时约 `6.43`，shift `0` 时约 `2.24`，shift `5` 时约 `8.58`。Ordinary TD 的 value norm 在 shifts `-5` 和 `5` 时分别增长到约 `353` 和 `462`。这些大 values 并不是任务结构更复杂，而是 learner 在表示 reward offset。

## 分析

这个 diagnostic 解释了 access-control 结果的重要性。Reward centering 从 prediction target 中移除 nuisance offset，降低 value scale，同时保留与任务动态相关的信息。这样可以减少 finite-step-size learning 中由任意 reward origin 造成的数值压力。

它也区分了 mechanism evidence 与 final control evidence。小型 MDP 可以解释方法行为，但不能证明方法在更大 continuing control 中普遍稳健。因此本报告应作为 Reward-Centered Continuing Sarsa 的机制附录，而不是替代主实验。

## 有效性威胁

环境刻意很小，不能作为最终主结果。Control 中 policy changes 会改变 reward distribution，使 diagnostic 行为更复杂。Bellman-error-centered variant 只是诊断，不应被过度宣传成已调好的算法。后续若要写进主报告，应把该实验作为“why” figure，而不是单独 claim。

## 审稿式批评与回应

Mechanism reviewer 会问：这个 study 是否回答了 reward centering 的 why，而不是又做一个小 benchmark？回应是：报告明确限定为 mechanism diagnostic，并把 access-control 作为主要控制证据。

Strict reviewer 会说：toy setting 容易让弱 proposal 看起来强。回应是：报告不把它列为强提交主线，只把它用于解释 value-scale inflation。

## 结论

Centered TD Diagnostics 是有用的独立机制研究。它清楚展示 centering 如何在 reward translation 下控制 value scale。它的范围有意受限：支持但不替代 Reward-Centered Continuing Sarsa。

## Proposal Template Answers / 提案模板回答

Focused RL question：在一个很小的 continuing prediction problem 中，centering Bellman error 是否能去掉任意 reward offset 对 TD learning dynamics 的影响？setting 是 two-loop MDP，比较 ordinary TD 与 centered variants，证据是 value scale、TD error 和 reward baseline behavior。compute 很小；fallback 是把它作为 Reward-Centered Sarsa 的机制附录。

## 独立研究范围

这是独立机制诊断，不是主控制 proposal。它研究 centering 为什么可能影响 continuing prediction，应服务 Reward-Centered Sarsa 的解释，而不是替代 access-control 控制实验。

## 证据等级

证据等级：supporting diagnostic。环境刻意很小，不应被写成完整 project-scale result。它的价值是清楚隔离 reward-offset mechanism。

## 实验设计依据

two-loop MDP 的作用是让 reward offsets 可以变化而不引入复杂 control。这样 value scale 和 TD-error 的变化更容易归因。更强版本可以加入 analytic shift table，但更大环境反而会遮住这个机制。

## 审查矩阵

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| Core RL | 环境太 toy。 | 明确写成 mechanism diagnostic。 | 不能作为主 proposal。 |
| Reward-centering | update 必须连接到控制结果。 | 报告把 Reward-Centered Sarsa 作为主研究。 | 仍可补 analytic table。 |
| 严格老师 | 不要从 tiny MDP 过度泛化。 | 证据等级写成 supporting diagnostic。 | 适合作为 appendix-style material。 |

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/centered_td_diagnostics/config_main.json
```
