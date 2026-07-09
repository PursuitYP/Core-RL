# GVF Question Design 中文报告

状态：独立 GVF 设计诊断；服务 GVF Predictive State 和 Predictive State Plasticity 的 redesign。

## 摘要

本 proposal 研究 GVFs 能成为 agent state 之前的一个更基础问题：哪些 predictive questions 值得学习？在 T-maze stream 中，我们为不同 cumulants 和 discounts 训练 linear GVF predictors。当前 run 显示有些问题很容易预测但不一定有用，例如 bias prediction；cue 和 junction questions 则揭示 prediction accuracy 与 downstream state relevance 之间的差异。本 study 不是最终 control result，而是一个用于设计 useful predictive state 的诊断。

## 研究动机

GVFs 常被描述为 predictive knowledge，但 prediction 对 agent 有用的前提是它能回答 decision-relevant question。低误差 GVF 可能只是预测常数、局部可见信号或与 hidden variable 无关的量。这样的预测即使稳定，也不能帮助 control。

GVF Predictive State 的失败让这个设计问题变得具体：T-maze 可以由 trace memory 解决，但当前 recurrent GVF 没有解决。于是问题变成：在把 GVF output 插入 control state 前，我们应该如何选择和评价 GVF questions？

## 研究问题

主问题：哪些 GVF cumulant/discount questions 容易预测，哪些看起来可能对 T-maze state construction 有用？

核心假设是：prediction error alone 不能识别 useful GVF questions。Useful questions 必须通过它们与 hidden cue information 或 downstream control 的关系来评价。

## Alberta Plan 关联

该 proposal 直接对应 GVFs、predictive knowledge、agent-state construction、question discovery/evaluation 和 useful prediction。它是独立 study，因为 question design 是任何 GVF-based state proposal 的前置条件。

## 环境与方法

环境是 T-maze stream，包含 left cue、right cue、junction 和 bias 等信号。Hidden control-relevant variable 是决定 junction action 的 cue。方法是在不同 cumulant identity 和 discount horizon 下训练 linear TD predictors，记录 prediction errors、value profiles 和 weight norms，然后从 usefulness 的角度解释它们。

## 实验设计

当前 main diagnostic 使用 cumulants `left_cue/right_cue/junction/bias`，discounts `0/0.5/0.9/0.98`，seeds `0-4`，steps `5000`。结果路径为 `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main`。主要指标包括 absolute TD error、prediction value 和 weight norm。

![GVF TD error by cumulant and discount.](../../../../experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main/figures/abs_td_error_by_cumulant-gamma_curve.png)

## 结果

Bias GVFs 非常容易学习，误差很低，但它们不携带 hidden cue，因此不是有用 state。Cue GVFs 有更非平凡的 error 和 discount-dependent predictions，可能更接近 state-construction 需求。Junction predictions 可预测，但它们本身不能直接解决 cue memory。结果支持一个重要区分：easy prediction 与 useful prediction 是不同类别。

## 分析

这个 diagnostic 解释了为什么当前 GVF predictive-state design 失败。如果因为某个 GVF 容易学或稳定就把它加入 state，可能得到对 control 无用的 feature。对 T-maze control 来说，正确诊断不是只看 TD error，而是看 prediction 是否帮助在 junction 解码 cue。

下一版应为每个 cumulant/discount group 增加 explicit cue-decodability metric 和 downstream junction-action ablation。只有同时在 prediction 和 control-usefulness 两边通过的 GVF question，才值得进入 predictive-state proposal。

## 有效性威胁

当前 study 主要推断 usefulness，还没有把每个 GVF feature set 直接放进 control 中测试。它也缺少 hidden cue 的 linear probe。Cumulant set 较小且由人工设计。结果只能作为诊断，不能当作最终 GVF state-construction claim。

## 审稿式批评与回应

Useful-prediction reviewer 会说：accuracy 和 usefulness 必须分开。回应是：报告明确把 bias GVFs 标为 easy but not useful。

Strict reviewer 会说：question-design study 需要 downstream usefulness metric。回应是：下一步明确要求 cue-decodability 和 downstream control ablations。

## 结论

GVF Question Design 是有价值的独立诊断。它提醒我们，在把 predictions 当作 state 前必须问“这个 prediction 用来做什么”。该 study 应直接反馈到 redesigned GVF Predictive State proposal 中，并用 usefulness metrics 选择 GVF questions。

## Proposal Template Answers / 提案模板回答

Focused RL question：哪些 GVF questions 更可能成为 useful state，而不只是 easy predictions？setting 是 controlled GVF question-design diagnostic；比较不同 cumulants/discounts，并检查 prediction behavior。必要指标是 prediction error 加 downstream usefulness probes，例如 cue decodability 和 control ablation。compute 中等偏小；fallback 是作为 GVF Predictive State 的 redesign guide。

## 独立研究范围

本报告是 GVF design diagnostic。它不应被写成 GVF state 已经帮助 control 的证据，因为当前证据主要是 prediction behavior。它的角色是筛选哪些 GVF questions 值得进入 downstream control evaluation。

## 证据等级

证据等级：supporting redesign tool。报告有价值，因为它区分 easy-to-predict cumulants 和 potentially useful cumulants。但在加入 cue-decodability 或 control-ablation metrics 之前，它不是正向 useful-state evidence。

## 实验设计依据

prediction error 单独不够，因为容易预测的信号可能与控制无关。下一步应把每个 cumulant/discount 与 hidden-cue probe 和 downstream-control ablation 配对。这样实验回答的是“对什么有用”，而不仅是“学得多好”。

## 审查矩阵

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| GVF | easy prediction 不等于 useful prediction。 | 报告定位为 design diagnostic。 | 需要 cue decodability。 |
| Control | 还没有 downstream ablation。 | 证据等级为 supporting/redesign。 | 不能声称 useful state。 |
| 严格老师 | 不要把 TD error 当主要成功指标。 | 下一步指标包括 control relevance。 | 当前图仍可能过度强调 prediction error。 |

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/gvf_question_design/config_main.json
```
