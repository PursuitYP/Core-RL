# Dyna Planning Budget and Model Staleness Proposal Template 中文版

英文模板：`proposal_template.md`

## 当前归档状态

当前正式报告在 `final/reports/proposals/dyna_planning_budget/report.md`，中文正式报告在 `final/reports/proposals/dyna_planning_budget/report_zh.md`。本模板是历史 proposal fragment 的中文审阅版，不替代正式报告。

## 想理解什么

该 proposal 的核心问题是：在 `changing continuing gridworld` 中，`Q-learning / Dyna with keep model / flush-on-change diagnostic` 是否能回答一个明确 Core-RL 机制问题。它不是为了展示某方法分数更高，而是为了检查 streaming online learning 中的稳定性、适应性、预测有用性或 planning computation 质量。

## 使用什么 testbed

Testbed：changing continuing gridworld。该设置遵守 no replay buffer、no deep network、online update 的约束。

## 检查什么变量

主要变量：planning budgets and model handling before/after phase change。主要比较：Q-learning / Dyna with keep model / flush-on-change diagnostic。

## 看什么指标

指标：avg_reward, stale_backup_rate, model_size, recovery window。当前结果路径：`experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main`。当前关键结论：planning budget `1` keep-model late stale rate 约 `0.844 +/- 0.0158`，显示 stale planning 是真实问题。

## 当前判断

可作为 model-aging 的基础诊断；单独提交还不够强。

## 还缺什么

正式提交前需要补清楚 update equation、baseline fairness、seed-tail statistics、结果图和 falsifier。对于 negative/supporting proposal，应明确说明失败暴露了什么设计问题，而不是强行写成正结果。
