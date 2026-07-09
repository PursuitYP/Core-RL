# Doorway Options for Reusable Subtasks 中文报告

英文原文：`report.md`

## 定位

quarantined independent proposal

## 研究动机

这个 proposal 关注一个具体 Core-RL 问题，而不是简单比较分数。它遵守项目约束：streaming/continual online learning，不使用 replay buffer，不使用 deep network，不使用离线训练循环。研究价值在于把 Alberta Plan 中关于 ordinary experience、value functions、稳定在线更新、预测知识或有限计算的主题落到一个可复现实验上。

## RL 问题

环境/任务：Four Rooms / doorway navigation。agent 与环境持续交互，在线更新，没有特殊训练/测试分割。这个设置用于检验一个明确机制，而不是追求大 benchmark 分数。

## Agent 与 Baseline

比较对象：primitive control / option-augmented SMDP control。所有方法都在同一 stream 上在线更新；关键差异是 proposal 要研究的机制，而不是额外数据或更大模型。

## 实验设计

主要变量：primitive vs short/long doorway options。主要指标：reward per environment step, option use, steps to goal, recovery。这些指标直接回答研究问题，例如稳定性、invariance、useful prediction、model freshness 或 adaptation，而不只是最终 reward。

## 当前结果

结果路径：`experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`。关键证据：late avg reward: primitive `-0.00920`、short options `-0.00935`、long options `-0.00995`；transfer claim 不成立。

## 可以声称与不能声称

隔离状态。必须先通过 fixed-goal sanity，再讨论 transfer。

## 下一步

优先补强 seed/step sweep、关键 baseline audit 和更直接的机制诊断。对于 negative/supporting proposal，下一步不是强行包装成正结果，而是说明失败暴露了哪个 Core-RL 设计约束。

## 复现

统一复现命令见 `final/indexes/reproduction_zh.md`；当前可引用证据见 `final/indexes/results_zh.md` 与英文 `final/indexes/results.md`。
