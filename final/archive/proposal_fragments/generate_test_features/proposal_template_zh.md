# Generate-and-Test Trace Features Proposal Template 中文版

英文模板：`proposal_template.md`

## 当前归档状态

当前正式报告在 `final/reports/proposals/generate_test_features/report.md`，中文正式报告在 `final/reports/proposals/generate_test_features/report_zh.md`。本模板是历史 proposal fragment 的中文审阅版，不替代正式报告。

## 想理解什么

该 proposal 的核心问题是：在 `delay-shift streaming prediction with limited trace features` 中，`fixed bank / random replacement / generate-and-test / oracle-like bank` 是否能回答一个明确 Core-RL 机制问题。它不是为了展示某方法分数更高，而是为了检查 streaming online learning 中的稳定性、适应性、预测有用性或 planning computation 质量。

## 使用什么 testbed

Testbed：delay-shift streaming prediction with limited trace features。该设置遵守 no replay buffer、no deep network、online update 的约束。

## 检查什么变量

主要变量：delay changes and feature replacement strategies。主要比较：fixed bank / random replacement / generate-and-test / oracle-like bank。

## 看什么指标

指标：absolute prediction error, replacement behavior, recovery windows。当前结果路径：`experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`。当前关键结论：late abs error: generate-test `0.0518`，random replacement `0.0496`，fixed tight `0.0512`，没有优于 random/fixed。

## 当前判断

负结果。可以声称当前 utility rule 不够；不能声称 generate-and-test 思路无效。

## 还缺什么

正式提交前需要补清楚 update equation、baseline fairness、seed-tail statistics、结果图和 falsifier。对于 negative/supporting proposal，应明确说明失败暴露了什么设计问题，而不是强行写成正结果。
