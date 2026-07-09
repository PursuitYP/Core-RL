# Reward-Centered Continuing Sarsa Proposal Template 中文版

英文模板：`proposal_template.md`

## 当前归档状态

当前正式报告在 `final/reports/proposals/reward_centered_sarsa/report.md`，中文正式报告在 `final/reports/proposals/reward_centered_sarsa/report_zh.md`。本模板是历史 proposal fragment 的中文审阅版，不替代正式报告。

## 想理解什么

该 proposal 的核心问题是：在 `access-control queue continuing control` 中，`discounted Sarsa / reward-centered Sarsa / differential Sarsa` 是否能回答一个明确 Core-RL 机制问题。它不是为了展示某方法分数更高，而是为了检查 streaming online learning 中的稳定性、适应性、预测有用性或 planning computation 质量。

## 使用什么 testbed

Testbed：access-control queue continuing control。该设置遵守 no replay buffer、no deep network、online update 的约束。

## 检查什么变量

主要变量：reward shifts `-4, 0, 4, 8`。主要比较：discounted Sarsa / reward-centered Sarsa / differential Sarsa。

## 看什么指标

指标：avg_unshifted_reward, q_norm, td_error, reward_bar, policy probes。当前结果路径：`experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main`。当前关键结论：ordinary discounted Sarsa 的 Q norm 从 shift `-4` 的 `60.17` 增至 shift `8` 的 `344.6`；reward-centered Sarsa Q norm 保持约 `20-22`，unshifted reward 约 `2.47-2.54`。

## 当前判断

主线候选。可以声称 reward centering 减少 reward-origin sensitivity；不能声称已完成所有 alpha/beta/gamma 或中途 reward-origin switch。

## 还缺什么

正式提交前需要补清楚 update equation、baseline fairness、seed-tail statistics、结果图和 falsifier。对于 negative/supporting proposal，应明确说明失败暴露了什么设计问题，而不是强行写成正结果。
