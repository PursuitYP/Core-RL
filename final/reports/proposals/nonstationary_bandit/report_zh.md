# Nonstationary Bandit Sanity Check 中文报告

英文原文：`report.md`

## 定位

dropped sanity diagnostic

## 研究动机

这个 proposal 关注一个具体 Core-RL 问题，而不是简单比较分数。它遵守项目约束：streaming/continual online learning，不使用 replay buffer，不使用 deep network，不使用离线训练循环。研究价值在于把 Alberta Plan 中关于 ordinary experience、value functions、稳定在线更新、预测知识或有限计算的主题落到一个可复现实验上。

## RL 问题

环境/任务：drifting/switching k-armed bandit。agent 与环境持续交互，在线更新，没有特殊训练/测试分割。这个设置用于检验一个明确机制，而不是追求大 benchmark 分数。

## Agent 与 Baseline

比较对象：sample-average / constant-alpha / gradient bandit variants。所有方法都在同一 stream 上在线更新；关键差异是 proposal 要研究的机制，而不是额外数据或更大模型。

## 实验设计

主要变量：nonstationary reward stream。主要指标：reward, best_action_rate, regret-like loss。这些指标直接回答研究问题，例如稳定性、invariance、useful prediction、model freshness 或 adaptation，而不只是最终 reward。

## 当前结果

结果路径：`experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`。关键证据：constant alpha reward `5.95`、best-action rate `0.306`；sample average reward `5.04`、best-action rate `0.0094`。

## 可以声称与不能声称

只是 sanity check，缺少 state、bootstrapping、planning、GVFs 等 Core-RL 深度。

## 下一步

优先补强 seed/step sweep、关键 baseline audit 和更直接的机制诊断。对于 negative/supporting proposal，下一步不是强行包装成正结果，而是说明失败暴露了哪个 Core-RL 设计约束。

## 复现

统一复现命令见 `final/indexes/reproduction_zh.md`；当前可引用证据见 `final/indexes/results_zh.md` 与英文 `final/indexes/results.md`。
