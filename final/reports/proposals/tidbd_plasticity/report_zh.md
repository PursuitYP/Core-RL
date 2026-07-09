# TIDBD-Lite Plasticity 中文报告

状态：独立支持性机制研究；当前不是正向性能 proposal。

## 摘要

本 proposal 研究 per-feature step-size adaptation 是否能作为 streaming TD prediction 的轻量级 plasticity mechanism。在 nonstationary sensor stream 中，feature relevance 在 phase switch 后改变。TIDBD-style learner 理想上应提高新相关 features 的 step sizes，同时让 distractors 保持低 plasticity。当前 main pilot 显示了这种机制信号：switch 后 new-feature step size 上升，distractor step size 保持较低。但 normalized TD 的 late prediction error 仍低于当前 TIDBD-lite implementation。因此本 proposal 的当前定位是机制诊断，而不是性能胜利。

## 研究动机

持续学习 agent 会遇到 changing feature relevance。一个固定 global step size 是折中：太大可能让 irrelevant/noisy features 破坏稳定性，太小又会让新相关 features 学得太慢。Per-feature step-size adaptation 提供更局部的 plasticity：每个 feature 可以根据自己与 TD error 的历史关系调整学习速度。

Alberta Plan 把 step-size adaptation 和 feature utility 看作长期 agent 的早期 building blocks。本 proposal 问的是：一个小型在线 TD learner 能否仅从 stream 中识别 feature relevance 的改变，并产生可解释的 per-feature plasticity dynamics。

## 研究问题

主问题：per-feature step-size adaptation 能否在 streaming TD 中跟踪 changing feature relevance？

更具体地说，switch 后 TIDBD-style learner 是否会提高 newly relevant features 的 step sizes、保持 distractor step sizes 较低，并比 fixed-alpha TD 更快恢复 prediction accuracy？当前结果支持前两个机制性 claim，但不支持强 prediction-error claim。

## Alberta Plan 关联

这个 proposal 连接 meta-learning of step sizes、online prediction、continual adaptation、feature relevance tracking 和 limited computation with linear function approximation。它不是 deep plasticity study，也不使用 replay buffer。研究价值在于让 feature-wise learning-rate dynamics 可观察、可解释、可批评。

## 环境设计

环境是 nonstationary sensor prediction stream。一个 feature group 在 switch 前 relevant，另一个 feature group 在 switch 后 relevant，distractor features 始终基本无关。Learner 在线更新，没有 replay。这个环境是机制环境，故意制造可测的 feature-relevance change，用来检查 step-size adaptation 是否朝正确 feature group 移动。

## 方法

比较方法包括 fixed TD with alphas `0.01/0.03/0.1`、normalized TD 和 TIDBD-lite。TIDBD-lite 为每个 feature 维护可调 step size，并使用简化的 meta-gradient-like signal 调整 alpha。报告明确使用 “TIDBD-lite” 名称，不把它当作完整 canonical TIDBD reproduction。

## 实验设计

当前 main pilot 使用 seeds `0-4`，steps `5000`，switch 发生在 stream 中点。结果路径是 `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`。主要指标包括 absolute TD error、old-relevant feature step sizes、new-relevant feature step sizes、distractor step sizes 和 recovery windows。

![TIDBD-lite 与 TD baselines 的 absolute TD error。](../../../../experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main/figures/abs_td_error_by_algorithm_curve.png)

## 结果

TIDBD-lite 展示了预期的 feature-wise plasticity signal。New-feature step size 从 switch 前约 `0.0068` 上升到 late post-change window 的约 `0.0093`；distractor step size 仍接近 `0.0068`。这说明机制确实能对 feature groups 产生不同学习速度。

但 normalized TD 仍是更强 prediction-error baseline。Late post-change absolute TD error 对 normalized TD 约 `0.4419 +/- 0.0085`，对 TIDBD-lite 约 `0.4493 +/- 0.0119`，对 fixed alpha `0.01` 约 `0.4881 +/- 0.0122`。因此当前结果只能说 TIDBD-lite 有可见 plasticity，不能说它在预测性能上胜过 output-normalized update。

## 分析

本 proposal 的价值在于分离两个经常被混在一起的 claim。第一，learner 是否以合理方向改变 feature-specific step sizes；第二，这种 adaptation 是否改善 prediction objective。当前第一点有证据，第二点没有。

这对后续研究很重要。一个 method 的 internal dynamics 看起来符合直觉，并不自动说明它解决了 continual learning。Normalized TD 是强 baseline，因为它直接控制 update magnitude；per-feature adaptation 若要成为主线，必须证明它在 repeated relevance shifts、不同 feature scales 或 downstream control 中提供额外收益。

## 有效性威胁

当前 implementation 是 TIDBD-lite，不是 canonical TIDBD。环境只有一次 switch，可能不足以展示 plasticity 优势。Meta step-size 与 normalization baseline 的公平比较还不充分。当前 metrics 主要看 group-wise alpha 和 error，还缺少 feature correlation、utility contribution 和 recovery AUC 等更细指标。

## 审稿式批评与回应

Plasticity reviewer 会说：mean step size 不足以证明 feature plasticity。回应是：报告记录 old/new/distractor group-wise step-size trajectories 和 recovery windows。

Strict reviewer 会说：不能把本地简化算法叫作 TIDBD。回应是：报告使用 TIDBD-lite，并明确需要 canonical TIDBD 或 AutoStep 才能升级结论。

Performance reviewer 会说：normalized TD 已经更好，为什么保留这个 proposal？回应是：它作为 mechanism diagnostic 有价值，因为它展示 per-feature plasticity 的可观察信号；但最终主线应诚实承认当前不是 performance win。

## 结论

TIDBD-Lite Plasticity 是有效的独立机制 proposal，但不是正向性能故事。它显示 relevance switch 后 per-feature step sizes 会朝合理方向变化，同时 normalized TD 在 prediction error 上更强。下一版应实现 canonical TIDBD/AutoStep，加入 repeated switches，并报告 recovery AUC，而不是只看 late error 或 mean alpha。

## Proposal Template Answers / 提案模板回答

Focused RL question：per-feature step-size adaptation 能否在 streaming prediction/control setting 中追踪 changing feature relevance？当前 setting 是 TIDBD-lite diagnostic，不是 canonical TIDBD。比较 TIDBD-lite 与 fixed/normalized TD-style baselines；指标是 prediction error、alpha trajectories、relevance switches 和 recovery。compute 中等；fallback 是 mechanism diagnostic，直到实现 canonical TIDBD 或 AutoStep。

## 独立研究范围

本报告研究 feature-wise plasticity signals，不是完成的 performance method。它不应被并入 Predictive State Plasticity 当作已完成正向证据。它的角色是说明 alpha dynamics 是否响应 relevance changes，以及还缺什么。

## 证据等级

证据等级：supporting mechanism diagnostic。当前 TIDBD-lite implementation 展示了可解释 alpha dynamics，但 normalized TD 在部分条件下 error 更好。因此报告不能声称 TIDBD-lite 提高性能。

## 实验设计依据

实验只有在区分“alpha visibly changes”和“learning improves”时才有价值。下一步应实现 canonical TIDBD/AutoStep，加入 repeated relevance switches，并报告 recovery AUC，而不只是 final error。

## 审查矩阵

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| Algorithm | TIDBD-lite 不是 canonical TIDBD。 | 证据等级写成 diagnostic。 | 需要 canonical TIDBD/AutoStep。 |
| Performance | alpha adaptation 不一定改善 error。 | 区分 alpha dynamics 和 prediction gain。 | normalized TD 可能仍更强。 |
| 严格老师 | 没有 utility evidence 不应过度使用 plasticity 语言。 | 下一步指标包含 recovery AUC 和 repeated switches。 | 当前结果只能 supporting。 |

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/tidbd_plasticity/config_main.json
```
