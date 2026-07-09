# Streaming Representation With Auxiliary Prediction 中文报告

状态：独立负结果诊断；除非重新设计 auxiliary question，否则不作为最终 proposal。

## 摘要

本 proposal 问一个小型 auxiliary next-feature prediction objective 是否能在无 replay、无 deep network 的 streaming setting 中改善 value prediction。当前 nonstationary sensor-stream experiment 没有发现实质改善：auxiliary prediction 与 value-only learning 的 late value-prediction error 几乎相同。这个负结果有用，因为它警告一个常见捷径：加一个 auxiliary loss 不等于学到 useful representation。Auxiliary question 必须与 downstream value problem 绑定。

## 研究动机

很多 streaming RL 和 representation learning 工作使用 auxiliary prediction 来改善 single-pass data 下的表示学习。在本课程约束下，我们不能使用 deep encoders 或 replay，但可以在线性 setting 中检验底层想法：一个 auxiliary next-feature target 是否真的为 nonstationary stream 中的 value prediction 提供有用信息？

当前设计的答案基本是否定的。这并不否定 auxiliary learning 一般有用，而是说明 auxiliary target 的选择必须严肃设计。

## 研究问题

主问题：一个小型 auxiliary next-feature prediction 能否在不使用 replay 或 deep networks 的情况下改善 streaming value prediction？

假设是：如果 auxiliary target 捕获了对 value prediction 有用的结构，那么 auxiliary learner 应降低 value TD error 或改善 feature-relevance switch 后的 recovery。当前结果不支持该假设。

## Alberta Plan 关联

该 proposal 与 representation learning 和 ordinary streaming experience 有一定关系，但弱于 GVF 和 generate-and-test proposals，因为 auxiliary target 没有明确绑定 control-relevant question。它适合保留为 negative diagnostic，提醒后续 predictive representation 研究必须定义 usefulness。

## 环境与方法

环境是 nonstationary sensor stream，包含 feature-relevance switch。Learner 在线更新，不能回放过去 transitions。比较方法包括 value-only normalized TD 和带 auxiliary next-feature prediction 的 value TD。Auxiliary target 是小型线性 target，符合 Core RL 约束，但 representation capacity 有限。

## 实验设计

当前 main diagnostic 使用 seeds `0-4`、steps `5000`，结果路径是 `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main`。主要指标包括 absolute TD error、auxiliary MSE、weight norm 和 phase。

![Auxiliary representation diagnostic absolute TD error.](../../../../experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main/figures/abs_td_error_by_algorithm-phase_curve.png)

## 结果

Auxiliary prediction objective 没有实质改善 value prediction。Phase-1 absolute TD error 对 auxiliary method 约 `0.5298`，对 value-only method 约 `0.5301`。差异太小，不能支持正向结论。

## 分析

结果表明 auxiliary target 与 value task 不够对齐。Next-feature prediction 可以容易学习，也可以优化自己的 auxiliary error，但这并不意味着它改善 value learner 的 state。这与 GVF Question Design 的结论一致：useful representation 需要 useful questions，而不是“能预测什么就预测什么”。

如果要升级这个 proposal，应把 next-feature prediction 换成 task-relevant GVF cumulants，或者加入 control ablation，直接检查 learned auxiliary features 是否改善 downstream behavior。

## 有效性威胁

Auxiliary representation 很小，可能太弱。Auxiliary target 没有显式绑定 reward、hidden state 或 control。实验不测试 deep representation learning，因为这超出课程范围。结果不能作为 auxiliary learning 的一般负面结论。

## 审稿式批评与回应

Representation reviewer 会说：除非 auxiliary target 与 downstream usefulness 绑定，否则 proposal 太模糊。回应是：报告将其降级为 negative diagnostic，并建议与 GVF Question Design 合并。

Upgrade path 是把 next-feature prediction 替换为 task-relevant GVF cumulants，并在 control 中 ablate learned features。

## 结论

Streaming Representation With Auxiliary Prediction 是有用的负结果诊断。它说明 auxiliary prediction 本身不是研究贡献，除非 auxiliary question 与 downstream value/control 明确相关。该 proposal 应被重新设计，或概念上并入 GVF Question Design。

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/streaming_representation/config_main.json
```
