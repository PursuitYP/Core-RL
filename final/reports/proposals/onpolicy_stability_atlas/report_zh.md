# On-Policy TD(lambda) Stability Atlas 中文报告

状态：独立诊断研究；支撑 Output-Controlled TD，但不能替代它。

## 摘要

本 proposal 绘制 on-policy TD(lambda) 在 feature scaling、step-size changes 和 eligibility traces 共同作用下的 practical stability region。它不是 intervention study，而是一个 atlas，用来说明 ordinary fixed-alpha TD 在什么条件下变得脆弱。当前 main run 发现 scale `one` 大多稳定，而更大或 uneven feature scale 会明显缩小稳定 alpha/lambda 区域。这个 diagnostic 强化了 Output-Controlled TD 的动机：feature-scale robustness 不是 cosmetic issue，而是 streaming value learning 的基础稳定性问题。

## 研究动机

TD(lambda) 把 bootstrapping 和 multi-step credit assignment 结合起来。在 linear prediction 中，它的稳定性依赖 alpha、lambda 和 feature geometry。一个 learner 在某个 representation 下稳定，并不意味着在同一 state information 被重新缩放后仍然稳定。

对 continual agent 来说，这很重要。Representation scale 可能来自 sensors、tile coders、learned features 或 normalization choices。Agent 不应该每次 feature scale 改变都重新做 exhaustive alpha sweep。Stability atlas 的作用是展示 fixed alpha 的脆弱性，从而为 output-controlled updates 提供背景证据。

## 研究问题

主问题：alpha、lambda 和 representation scale 如何共同决定 on-policy TD 的 stable region？

假设是：增大 feature scale 和 trace length 会缩小 fixed-alpha stable region。这个 atlas 只问 failures 出现在哪里，不直接提供新算法。

## Alberta Plan 关联

该 proposal 连接 value prediction、online TD learning、eligibility traces、representation sensitivity 和 streaming agents 的 diagnostic process metrics。它是独立 study，因为 stability map 对任何后续 continual value-function method 都有参考价值。

## 环境与方法

环境是 random-walk prediction problem，使用 scaled tabular features。它比 Output-Controlled TD 的 tile-coded main experiment 简单，因此适合做 dense alpha/lambda/scale atlas。Learner 在线从一个 transition 更新一次，预测 random-walk value function。

Diagnostic sweep 改变 feature scale、alpha 和 lambda。当前没有引入新算法，因此它的贡献是描述稳定边界，而不是提出干预方法。

## 实验设计

当前 main diagnostic 使用 scales `one/ten/uneven`，alphas `0.001/0.01/0.05/0.1/0.2`，lambdas `0/0.5/0.8/0.95`，seeds `0-4`，steps `5000`。结果路径是 `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main`。主要指标包括 RMSE、divergence 和 weight norm。

![TD(lambda) tail RMSE atlas by scale, alpha, and lambda.](../../../../experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main/figures/report_log_rmse_atlas.png)

![TD(lambda) divergence atlas by scale, alpha, and lambda.](../../../../experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main/figures/report_divergence_atlas.png)

## 结果

Scale `one` 在大多数测试 grid 中保持稳定。Scale `ten` 在较大 alpha 和高 lambda 下开始不稳定。`uneven` scale 更脆弱，许多条件出现大 RMSE 或非零 divergence。这个 pattern 支持假设：fixed alpha 不能跨 representation scale 和 trace accumulation 直接迁移。

## 分析

如果 alpha 是一种 representation-independent learning-progress unit，那么相同 alpha/lambda grid 在不同 scale 下应表现相似。但结果并非如此。特别是 lambda 的交互很重要，因为 eligibility traces 会放大实际 update direction norm，即使当前 feature vector 本身不大。

这个 atlas 的价值是解释 Output-Controlled TD 为什么需要。Normalized 或 intentional update 的目标就是让 alpha 更接近 prediction/output change，而不是 raw parameter displacement。Atlas 本身不解决问题，但清楚指出 fixed-alpha TD(lambda) 的危险区域。

## 有效性威胁

Representation 比主 Output-Controlled TD 的 tile coding 简单。Atlas 没有实现新方法，因此不应被当作 algorithmic contribution。这里只研究 on-policy prediction，off-policy traces 可能更脆弱。早期 learning-curve plot 过密，当前报告已改用 heatmap，避免图例压缩主要信息。

## 审稿式批评与回应

Stability reviewer 会说：atlas 只有在能指导方法设计时才有价值。回应是：报告明确把 atlas failures 连接到 Output-Controlled TD 的 normalization 动机。

Strict reviewer 会说：没有 intervention 的 study 不能作为主贡献。回应是：报告将其定位为 independent diagnostic appendix-style study，并完整保留复现路径。

## 结论

On-Policy TD(lambda) Stability Atlas 是聚焦的诊断 proposal。它展示 feature scale 和 trace length 会实质改变 fixed-alpha stability。结果支持 output-control argument，同时作为 TD(lambda) failure regions 的独立地图保留下来。

## Proposal Template Answers / 提案模板回答

Focused RL question：online prediction 中，TD(lambda) 的稳定性如何随 alpha、lambda 和 feature scale 改变？setting 是 tile-coded prediction stream；比较是 descriptive atlas，不是新算法。主证据应是 max-stable-alpha maps 或 heatmaps，而不是单条曲线。compute 小到中等；fallback 是作为 Output-Controlled TD 的 diagnostic appendix。

## 独立研究范围

这个 atlas 可以作为独立诊断图谱，但不是 intervention study。它解释为什么需要 output-controlled 或 normalized updates：ordinary parameter-step TD(lambda) 在某些 scale/alpha/lambda 下会变脆弱。

## 证据等级

证据等级：supporting atlas。它对机制和 baseline calibration 有价值，但不应作为主正向方法提交，因为它没有提出或测试 remedy。

## 实验设计依据

alpha/lambda/scale grid 本身就是科学对象。它把 stability 从个别 divergence 变成边界地图。下一步应把过载 learning curves 转成真正 atlas figures：tail RMSE 和 divergence heatmaps。

## 审查矩阵

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| Stability | curve 不是 atlas。 | 报告把 heatmaps/max-stable-alpha 写成下一步主图。 | 当前图仍可能过密。 |
| Method | 没有新算法。 | 证据等级写成 supporting diagnostic。 | 不能替代 Output-Controlled TD。 |
| 严格老师 | 不能只是画图。 | 用来动机化 normalized update units。 | 需要与 Output-Controlled metrics 对齐。 |

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/onpolicy_stability_atlas/config_main.json
```
