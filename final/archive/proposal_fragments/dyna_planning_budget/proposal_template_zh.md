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

指标：avg_reward, stale_backup_rate, model_size, recovery window。当前结果路径已更新为 `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended`；本 archive 中的 `results.md` 仍保留早期 pilot 证据。当前关键结论：20 seeds larger-grid run 中 planning budget `20` 的 keep-model late stale-backup rate 仍约 `0.294`，flush 为 `0`，但 late reward 对 keep/flush 相近，因此它更适合作为 model-aging 的前置诊断。

## 当前判断

可作为 model-aging 的基础诊断；单独提交还不够强。

## 还缺什么

正式提交前需要补清楚 update equation、baseline fairness、seed-tail statistics、结果图和 falsifier。对于 negative/supporting proposal，应明确说明失败暴露了什么设计问题，而不是强行写成正结果。

## 归档模板审阅补充

阅读这个历史模板时，应先定位它回答的 focused RL question，而不是只看算法名字。一个合格 proposal template 需要说明环境为什么能暴露该机制，agent 在线观察什么、采取什么动作或预测什么、reward/cumulant 是什么，以及哪些变量被有意改变。还需要写清楚 baseline 是否公平，指标如何直接回答问题，什么结果会支持 proposal，什么结果会推翻 proposal。当前正式报告已经承担这些职责；本归档模板用于追踪早期设计如何演化，不应作为最终提交文本引用。
