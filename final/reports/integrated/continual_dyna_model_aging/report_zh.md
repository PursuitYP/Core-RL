# Continual Dyna With Model Aging 中文报告

英文原文：`report.md`

## 定位

综合型主线候选，planning/model-based 方向最清楚。

## 研究动机

Dyna planning 的吸引力在于用 learned model 做 background backups，从而让有限真实经验产生更多 value updates。但在 continual world 中，model entry 可能过时：过去正确的 transition 在环境改变后会变成 stale knowledge。如果 agent 继续从旧 model 中均匀抽样，planning budget 越大，旧知识被放大的机会越多。本课题把 model freshness 作为第一等 RL 问题，而不是只问 planning steps 越多是否越好。

## 研究问题

当 learned model 的 freshness 未知时，一个小型 continual Dyna agent 应该如何选择 planning backups，才能保留 planning 的 pre-change benefit，同时减少 post-change stale backups？

## 方法与实现

环境是 changing continuing gridworld，agent 维护 compact one-step state-action model。比较 keep_model、oracle_flush、recency_aging、recency_error_gate。oracle_flush 只作为上界诊断；现实方法只使用在线 last_seen recency 和 recent model error。

## 实验设计

当前 main pilot 使用 layout/hazard/goal dynamics 中途改变的 gridworld，不重置 agent。变量包括 planning budgets `1, 5, 20` 与四种 model handling 策略；extended code path 会加入 budget `0` 和 half-lives `250, 750, 1500, 4000`。指标包括 real-step avg reward、stale_backup_rate、mean_model_error、planning_abs_td、model_size 和 recovery window。

## 当前结果

结果路径：`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main`。在 planning budget `20` 时，keep_model 的 late stale-backup rate 约 `0.336`，recency aging 降到约 `0.0064`，recency/error gate 也接近零；late reward 在当前 pilot 中 recency aging 最好。budget `1` 和 `5` 下 stale backups 能减少，但 reward recovery 较弱。

## 可以声称与不能声称

可以声称：当前 pilot 说明 model freshness 是 planning computation 的关键变量，recency aging 可以在无需 oracle change detector 的情况下显著降低 stale backups。不能声称：已经解决一般非平稳 model-based RL；当前环境还是 abrupt deterministic change。

## 下一步

优先提交 extended CPU sweep；随后设计 stochastic/gradual drift 环境，验证 freshness heuristic 是否仍然有效。

## 复现

主复现命令见 `final/indexes/reproduction_zh.md` 与英文 `final/indexes/reproduction.md`。
