# Predictive State Plasticity 中文报告

英文原文：`report.md`

## 定位

综合型高风险方向，当前是有价值的负向 gate / redesign 候选。

## 研究动机

GVFs 是 Alberta Plan 中构造 agent state 的核心想法，但“能预测”不等于“对控制有用”。在 partial observability 中，agent 需要把早期 cue 信息维持到后续决策点；一个低误差预测如果不携带 hidden cue，或不能被 control learner 利用，就不是 useful state。本课题用 T-maze 把这个问题尖锐化。

## 研究问题

在带 hidden cue 的 T-maze 中，learned GVF features 是否能携带控制所需的 cue information，并接近 cheap trace memory 或 oracle memory baseline？

## 方法与实现

比较 raw observation、trace memory、old recurrent GVF、redesigned cue-GVF 和 oracle memory。control learner 是 normalized linear Sarsa；GVF learner 是在线 TD。当前阶段先做 first-gate，没有把 generate-and-test/TIDBD 全部接入，避免失败原因不可解释。

## 实验设计

当前 main pilot 跨 maze lengths `8, 12, 20` 和五种 representation mode，5 seeds，5000 steps。指标包括 trial_accuracy、avg_reward、cue_alignment_margin、gvf_abs_td_error 和 control_td_error。

## 当前结果

结果路径：`experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main`。trace memory 和 oracle memory 在三个长度下 trial accuracy 约 `0.93-0.96`；cue-GVF 虽有正 cue-alignment margin，但 control accuracy 仍接近 chance，约 `0.47-0.49`。这说明当前 GVF output 有一点 cue 信号，但还不是足够有用的 control state。

## 可以声称与不能声称

可以声称：当前实验揭示了 GVF prediction signal 与 useful state 之间的缺口。不能声称：GVFs 一般失败，也不能声称 predictive-state plasticity 已经成功。

## 下一步

补 oracle-prediction control、cue information/decode metric、feature ablation，再决定是否接入 generate-and-test 与 TIDBD。

## 复现

主复现命令见 `final/indexes/reproduction_zh.md` 与英文 `final/indexes/reproduction.md`。
