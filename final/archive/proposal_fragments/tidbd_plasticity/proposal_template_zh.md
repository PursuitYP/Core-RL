# TIDBD-Lite Plasticity Proposal Template 中文版

英文模板：`proposal_template.md`

## 当前归档状态

当前正式报告在 `final/reports/proposals/tidbd_plasticity/report.md`，中文正式报告在 `final/reports/proposals/tidbd_plasticity/report_zh.md`。本模板是历史 proposal fragment 的中文审阅版，不替代正式报告。

## 想理解什么

该 proposal 的核心问题是：在 `nonstationary streaming prediction with changing feature relevance` 中，`fixed TD / normalized TD / TIDBD-lite` 是否能回答一个明确 Core-RL 机制问题。它不是为了展示某方法分数更高，而是为了检查 streaming online learning 中的稳定性、适应性、预测有用性或 planning computation 质量。

## 使用什么 testbed

Testbed：nonstationary streaming prediction with changing feature relevance。该设置遵守 no replay buffer、no deep network、online update 的约束。

## 检查什么变量

主要变量：feature relevance switch and recovery windows。主要比较：fixed TD / normalized TD / TIDBD-lite。

## 看什么指标

指标：abs_td_error, per-feature alpha, recovery after change。当前结果路径：`experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`。当前关键结论：late abs TD error: normalized TD `0.4419`，TIDBD-lite `0.4493`，fixed alpha `0.01` 为 `0.4881`。机制可见但不是性能胜利。

## 当前判断

支持性机制研究。不能作为正向性能 proposal 提交，除非实现 canonical TIDBD/AutoStep 并证明收益。

## 还缺什么

正式提交前需要补清楚 update equation、baseline fairness、seed-tail statistics、结果图和 falsifier。对于 negative/supporting proposal，应明确说明失败暴露了什么设计问题，而不是强行写成正结果。
