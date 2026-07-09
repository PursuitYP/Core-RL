# Streaming Representation With Auxiliary Prediction

状态：独立的 negative auxiliary-prediction diagnostic。当前 target 需要围绕 task-relevant predictions 重设计后，才能提出正向 representation claim。

## 摘要

这篇 mini-report 在一个小型 streaming RL setting 中检验一个常见 representation-learning 直觉：加入 auxiliary prediction objective 可能改善 online value prediction 所用的 representation。实验在 nonstationary sensor stream 中比较 value-only normalized TD 与同时预测 next features 的 value learner，并且不使用 replay。结果是负面的：auxiliary next-feature target 没有实质降低主 value-prediction error。

这个结果有用，因为它说明 auxiliary loss 不会自动成为 useful prediction。Auxiliary target 必须与 agent 要回答的 value 或 control question 相关。因此，这个 proposal 应被读作独立 negative diagnostic 和 redesign target，而不是反对 auxiliary learning 或 GVFs 的一般证据。

## 1. Proposal Template Answers / 提案模板回答

Focused RL question：在没有 replay 或 deep networks 的 streaming linear setting 中，auxiliary next-feature prediction objective 是否能改善 online value prediction？

Setting/testbed：一个包含 feature-relevance switch 的 nonstationary sensor stream。Learner 在线观察 features，不能回放过去 transitions。

Implemented comparison：Value-only normalized TD 与带 auxiliary next-feature prediction head 的 normalized TD。

Observation or metric：Absolute TD error 是主要 downstream value metric。Auxiliary MSE、TD error、weight norm 和 phase-specific summaries 作为辅助诊断。

Expected behavior：如果 next-feature prediction 捕获 value-relevant structure，auxiliary learner 应降低 value-prediction error，或改善 feature-relevance switch 后的 recovery。

Compute need：小型 CPU-only run，五个 seeds，5000 online steps。

Fallback：把当前结果视为 negative diagnostic。更强项目应比较 task-relevant、task-irrelevant 和 shuffled auxiliary predictions，或转向小型 control task。

## 2. Research Motivation / Question / Method / 研究动机、问题与方法

Streaming RL 需要能从 ordinary experience 中在线学习的 representations。Auxiliary prediction 很有吸引力，因为它能在不使用 replay、大模型或 offline pretraining 的情况下增加 learning signal。原则上，预测未来某些方面可能让当前 representation 对 value learning 更有用。

研究问题是：简单的 auxiliary next-feature target 是否能在这个 setting 中改善 online value prediction。原本假设是正向但有条件的：next-feature prediction 只有在捕获 value question 所需结构时才应有帮助。

方法比较同一 stream 下的两个 online learners。Value-only learner 运行 normalized TD。Auxiliary learner 增加 next-feature prediction loss。Auxiliary target 是局部且方便定义的，但它不是从 reward、hidden state、control consequences 或 GVF-style cumulant 推导出来的。这个区别是 diagnostic 的核心。

## 3. Experimental Design / 实验设计

Main run：

- Seeds：`0-4`。
- Steps：`5000`。
- Config 中的 environment label：`nonstationary_sensor_auxiliary_prediction`。
- Result path：`experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main`。
- Primary metrics：`abs_td_error`、`aux_mse` 和 `weight_norm`。

主图：

![Auxiliary representation diagnostic absolute TD error.](../../../../experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main/figures/abs_td_error_by_algorithm-phase_curve.png)

Primary outcome 是 downstream value-prediction error。Auxiliary MSE 是 secondary，因为低 auxiliary prediction error 本身不能证明 learned signal 对 value task 有用。

## 4. Results / 结果

Auxiliary prediction objective 没有实质改善 value prediction。Phase 1 中，auxiliary method 的 seed-tail mean absolute TD error 约为 `0.5298`，value-only learning 约为 `0.5301`。Phase 0 中，对应数值约为 auxiliary method `0.4885`，value-only learning `0.4877`。

Auxiliary learner 确实把辅助目标学到了稳定水平：seed-tail mean auxiliary MSE 在 phase 0 约为 `0.0480`，在 phase 1 约为 `0.0413`。但这没有转化为 downstream value-error improvement。Phase 1 的 weight norms 也几乎相同，两个 learners 都约为 `3.34`。

因此结果是负面的，但有信息量。正确结论不是 auxiliary learning 一般失败，而是更窄地说：当前 next-feature target 对该 streaming diagnostic 中的 downstream value task 不够有用。

## 5. Analysis / 分析

最可能的失败机制是 target mismatch。Next-feature prediction 可能优化的是与 reward 无关、与 hidden feature switch 无关，或已经存在于当前 feature vector 中的信息。在这种情况下，auxiliary loss 消耗 learning capacity，却没有把 representation 推向 value-relevant structure。

从 Alberta Plan 视角看，这更像一个 cautionary example。Useful predictions 应是 useful questions：它们应揭示 state、reward-relevant structure、controllable consequences，或帮助 agent 行动和学习的 temporally extended knowledge。Generic next-feature target 不保证这些性质。

下一版应先重设计 auxiliary question，而不是先扩大实验。合理后续包括：与 reward、termination、hidden phase 或 controllable events 绑定的 GVF-style cumulants；learned auxiliary features 的 ablation 或 freeze tests；task-relevant 与 task-irrelevant auxiliary targets 比较；以及用 policy quality 或 average reward 判断 usefulness 的小型 control task。

## 6. 局限与有效性威胁

- Auxiliary architecture 被刻意做得很小，可能过弱。
- Auxiliary target 没有绑定 reward、hidden state 或 control。
- 五个 seeds 足以做 diagnostic，但不足以支持广泛 representation-learning claim。
- 实验不测试 deep representation learning，因为这超出当前课程范围。
- Absolute TD error 可能遗漏只在 control 或 feature freezing 后才出现的 representational effects。

## 7. Reviewer Critique / 审稿批评

| Reviewer critique | 当前回应 | 必要下一步 |
|---|---|---|
| Auxiliary target 很任意。 | 报告把这点作为核心 negative finding。 | 围绕 downstream usefulness 重设计 auxiliary question。 |
| 低 auxiliary MSE 不代表 useful representation。 | Primary metric 是 downstream absolute TD error，而不是 auxiliary loss。 | 加入 ablations，说明 auxiliary features 是否帮助 value prediction。 |
| 结果可能是 architecture-specific。 | Claim 限定在这个小型 linear streaming diagnostic。 | 在增加模型复杂度前，先比较 target relevance。 |
| 不能把它引用为反对 GVFs 的一般证据。 | 结论明确避免这个 claim。 | 测试与 reward、phase 或 controllable events 绑定的 GVF-style cumulants。 |

## 8. Conclusion / 结论

这个 proposal 是 streaming representation learning 的独立 negative diagnostic。当前 auxiliary next-feature target 可被学习，但没有改善 downstream value metric。有用 lesson 是方法论上的：auxiliary predictions 应被选为 task-relevant questions，而不是仅因为容易定义就加入。

## 9. Reproduction / 复现

从仓库根目录运行：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/streaming_representation/config_main.json
```

预期 result directory：`experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main`。
