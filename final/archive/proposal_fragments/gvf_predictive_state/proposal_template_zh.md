# GVF Predictive State Proposal Template 中文版

英文模板：`proposal_template.md`

## 当前归档状态

当前正式报告在 `final/reports/proposals/gvf_predictive_state/report.md`，中文正式报告在 `final/reports/proposals/gvf_predictive_state/report_zh.md`。本模板是历史 proposal fragment 的中文审阅版，不替代正式报告。

## 想理解什么

该 proposal 的核心问题是：在 `partially observable T-maze` 中，`raw / short history / trace memory / recurrent GVF / oracle memory` 是否能回答一个明确 Core-RL 机制问题。它不是为了展示某方法分数更高，而是为了检查 streaming online learning 中的稳定性、适应性、预测有用性或 planning computation 质量。

## 使用什么 testbed

Testbed：partially observable T-maze。该设置遵守 no replay buffer、no deep network、online update 的约束。

## 检查什么变量

主要变量：representation mode in a long cue T-maze。主要比较：raw / short history / trace memory / recurrent GVF / oracle memory。

## 看什么指标

指标：trial_accuracy, avg_reward, GVF TD error, control TD error。当前结果路径：`experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`。当前关键结论：trace memory `0.944 +/- 0.018`、oracle `0.939 +/- 0.027`；recurrent GVF 约 `0.502 +/- 0.023`，接近 chance。

## 当前判断

负结果。可以声称当前 GVF question 不足以构成 useful state；不能泛化为 GVFs 一般无用。

## 还缺什么

正式提交前需要补清楚 update equation、baseline fairness、seed-tail statistics、结果图和 falsifier。对于 negative/supporting proposal，应明确说明失败暴露了什么设计问题，而不是强行写成正结果。
