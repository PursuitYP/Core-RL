# Continual Dyna With Model Aging 中文报告

状态：综合型主线候选；planning/model-based 方向中研究问题最清楚的 proposal 之一。当前已有 20-seed extended half-life/budget sweep。

## 摘要

Dyna-style planning 通过 learned model 做 background backups，让 agent 在不增加真实环境交互的情况下改进 value estimates。但在 nonstationary world 中，同一个机制也可能放大过期知识。本 proposal 把 model freshness 作为第一等 Core RL 问题：一个小型 online Dyna agent 能否根据 recency 或 prediction error 来 age/distrust model entries，使 planning 在环境改变后仍然有用？当前 20-seed extended sweep 显示，recency aging 和 recency/error gating 能在不使用 oracle change detector 的情况下显著降低 stale-backup rate；reward 改善在部分 high-budget setting 中存在，但依赖 planning budget 和 half-life。因此最终结论应聚焦 freshness-aware search control，而不是宣称某个 aging rule 普遍 reward 最优。

## 研究动机

Alberta Plan 把 learned models 和 background planning 放在长期 agent 的核心位置。一个 base agent 不应只被动更新当前 transition，还应利用已学到的模型在有限计算预算内做额外 value updates。经典 Dyna 的成功故事通常是 stationary world 中的 sample efficiency：模型越准，planning 越能加速学习。

Continual setting 改变了问题本质。长期 agent 的 model entry 是过去 experience 的总结，而不是永远正确的 world law。当 goal、hazard、transition probability 或 reward consequence 改变后，旧 model entry 可能仍然占据模型表。若 agent 继续均匀抽样这些 entries，planning budget 就可能从“加速新知识”变成“反复备份旧知识”。这正是 ordinary experience 和 temporal uniformity 下 model-based RL 的核心难点。

本 proposal 不是问“Dyna 是否比 Q-learning 更快”，而是问“当 model knowledge 的 freshness 未知时，agent 应该如何信任或折扣自己的模型”。这个角度比普通 changing-maze Dyna 更贴近 Alberta Plan：关键不只是有模型，而是如何管理模型、搜索控制和有限计算。

## 研究问题

主问题：在 continuing nonstationary task 中，小型 Dyna agent 能否通过 online model aging 或 error gating，在保留 planning benefit 的同时减少 stale model backups？

子问题包括：aggressive aging 是否会牺牲 change 前的 planning benefit；stale-backup rate 是否能解释 post-change recovery；oracle flush 是否过于粗糙且不 realistic；recency 和 model error 的组合是否比单纯 recency 更好；freshness control 是否需要足够 planning budget 才能体现在 reward 上。

## Alberta Plan 关联

这个 proposal 对应 Alberta Plan 的 learned models、planning、ordinary experience、limited computation、temporal abstraction 前的 base-agent computation allocation，以及 continuing control。模型是在线维护的 compact state-action transition/reward table，不是 replay buffer；agent 不从旧 raw experience dataset 做离线训练，而是从 learned model entry 做小规模 TD planning backups。

这个区别很重要。Replay-buffer framing 关注“旧样本是否还该训练”；这里关注“一个持续更新的模型中，哪些 compact entries 仍值得被分配 planning computation”。这是更加 Core-RL 的 search-control 和 model-management 问题。

## 环境设计

主环境是 changing continuing gridworld。Agent 在 grid 中持续行动，没有 episodic train/test reset。环境包含 goal、hazards 和 step cost；stream 进行到中点时，goal/hazard layout 改变。这个设计保留了清晰的 control structure，同时让 stale model entry 可以被定义和统计。

当前 extended result path 是 `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`。该 run 使用 seeds `0-19`、steps `20000`、planning budgets `0/1/5/20`，并 sweep aging half-lives `250/750/1500/4000`。更强的后续环境应加入 stochastic 或 gradual drift，例如 transition probabilities 缓慢变化的 queue/random-walk model，这样可以避免结果只依赖“单次 abrupt switch 很容易识别”的特性。

## 方法

所有 agent 都维护一个 compact one-step model。每个 state-action entry 记录 estimated next state、estimated reward、last update time、recent model prediction error 和 phase/diagnostic 信息。真实 transition 更新 Q 和 model；随后 agent 在固定 planning budget 内从 model 中选择 entries 做 Dyna backups。

比较方法包括：`keep_model`，即普通 Dyna 均匀保留并抽样旧 model entries；`oracle_flush`，即在 change 时清空模型，只作为诊断上界；`recency_aging`，即根据 entry 的 last_seen age 让旧条目被抽到的概率衰减；`recency_error_gate`，即同时使用 recency 和 recent model error 抑制不可信 entries。Planning budget 包括 `1/5/20`，extended path 还包括 `0` no-planning baseline。

`oracle_flush` 必须被明确标注为不 realistic。它违反 temporal uniformity，因为 agent 被给予完美 change signal。它的价值只是帮助解释：如果完全去掉旧模型，staleness 会怎样变化。真正候选方法必须只依赖 stream 中可在线计算的 recency/error signals。

## 实验设计

当前 extended run 的变量是 model mode、planning budget 和 half-life。主要指标包括 real-step average reward、stale-backup rate、model one-step prediction error、planning TD magnitude、model size、Q norm 和 recovery window。报告图使用 late post-change seed-tail condition summaries，并在图例中显式区分 `250/750/1500/4000` 等 half-life，而不是很多曲线挤在一张图里或静默丢掉 half-life 维度。

成功标准不是“某个方法在一个 budget 下 reward 稍高”。更严谨的判据是：方法是否在不用 oracle change detector 的情况下减少 stale backups；减少 stale backups 是否伴随 post-change recovery 改善或至少不显著破坏 pre-change benefit；不同 planning budget 下是否出现一致 tradeoff；半衰期是否过于敏感。

Extended sweep 的作用是把早期 pilot 中固定 half-life 和 5 seeds 的证据升级成更可信的 sensitivity analysis。当前结果正好说明 reward 差异需要谨慎解释：freshness control 稳定减少 stale planning computation，但 reward ranking 会随 budget 和 half-life 改变。

## 当前结果

当前 extended result path 是 `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`。

![Late average reward by planning budget, model mode, and half-life.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended/figures/report_avg_reward_post_late_by_budget.png)

![Late stale-backup rate by planning budget, model mode, and half-life.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended/figures/report_stale_backup_rate_post_late_by_budget.png)

![Late model error by planning budget and model mode.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended/figures/report_mean_model_error_post_late_by_budget.png)

Extended run 中，planning budget `20` 时 keep-model 的 late stale-backup rate 为 `0.213 +/- 0.065`。Recency aging 在 half-life `250` 时几乎降到 `0`，在 half-life `1500` 时约 `0.00058 +/- 0.00017`，在 half-life `4000` 时约 `0.0204 +/- 0.0044`。这说明不依赖 oracle change detector 的 freshness weighting 可以显著改变 planning computation 的内容。

Reward 结果更微妙。Budget `20` 时，keep-model late reward 为 `0.0828 +/- 0.0113`，oracle flush 为 `0.0906 +/- 0.0060`。Recency aging 随 half-life 大约在 `0.0865` 到 `0.0925` 之间，recency/error gate 大约在 `0.0822` 到 `0.0925` 之间。最好的 freshness 条件与 oracle flush 接近或略高，但差异依赖 half-life，不应写成普遍 reward superiority。

Budget `5` 下，keep-model 和 oracle flush 的 late reward 都很强，约 `0.096-0.097`；aggressive half-life `250/750` 能减少 stale backups，但会明显伤害 late reward。Budget `1` 下，freshness methods 仍能降低 stale backups，但 reward recovery 对所有方法都较弱。这提示 model freshness 不是单独变量；它与 planning budget 和环境时间尺度强交互。

## 分析

本 proposal 的主要 insight 是：planning 的质量不只由模型是否存在或 planning steps 数量决定，还由 search-control distribution 是否尊重模型新鲜度决定。普通 keep-model Dyna 在 nonstationary change 后仍然可能把相当比例 backup 分配给旧 phase entries。Recency aging 把“最近真实观察过的 entry 更可信”这个弱但可在线计算的原则引入 search control，从而显著降低 stale computation。

为什么 oracle flush 不一定最好？Flush 会清空所有旧知识，包括一些仍可复用的 transition structure。Recency aging 更平滑：旧而未再观察的 entries 概率衰减，但新近访问和更新过的 entries 会重新获得 planning 权重。因此它可能在避免 stale backups 与保留 reusable structure 之间形成中间区域。

为什么 stale-backup rate 比 reward 更关键？在小 gridworld 中，agent 可能靠真实交互逐渐恢复 reward，即使 planning 仍有浪费。但 Alberta Plan 设想的 agent 会有许多 predictions、models、options 和 control values 竞争有限计算。即使 reward 没有立刻崩溃，把 background computation 花在过期知识上也会降低整个 agent 的长期可扩展性。

## 有效性威胁

第一，当前环境是 abrupt deterministic change，因此 stale model entries 比较容易定义。这对机制诊断有用，但可能高估 freshness heuristic 在 stochastic/gradual drift 中的清晰性。

第二，reward ranking 对 half-life 和 planning budget 敏感。报告应把最稳健 claim 放在 stale-backup reduction、model error 和 recovery diagnostics 上，而不是把 mean reward 小差异写成普遍胜利。

第三，extended run 已经显示 `250/750/1500/4000` 等 half-life 会导致不同 tradeoff。最终报告必须讨论这个 sensitivity，而不是只报告最好的一条曲线。

第四，当前 model 是 tabular deterministic one-step model。更复杂状态抽象或随机 transitions 下，model error 和 recency 的解释会更困难，需要 uncertainty-aware 或 distributional model diagnostics。

## 审稿式批评与回应

严格 reviewer 可能说：“这只是 changing maze 上的 Dyna-Q。”回应是：报告不把分数作为唯一结果，而是记录 stale-backup rate、planning TD magnitude、model error 和 recovery window，把问题定义为 model freshness 和 search control。

另一个 reviewer 会说：“flush-on-change 不 realistic。”回应是：flush 只保留为 oracle diagnostic，用来解释 freshness 上界；真正方法只使用 online recency 和 prediction error。

Sutton-style reviewer 会问：“这个机制是否符合 ordinary experience 和 temporal uniformity？”回应是：recency 和 model-error signals 都来自 agent 自身的 stream，不需要 replay buffer、offline training 或外部 change labels。

Statistics reviewer 会指出：“reward winner 依赖 half-life。”回应是：报告已经把 strong claim 收紧为 freshness-aware search control reduces stale backups；reward 部分作为 budget/half-life tradeoff 解释。

## 结论

Continual Dyna Model Aging 把 Dyna 从“多做 planning 是否更快”的熟悉故事推进到更有 Alberta Plan 意义的问题：长期 agent 什么时候应该信任自己的 learned model？当前 extended sweep 支持 model freshness 是 first-class planning variable：recency aging 和 recency/error gating 能显著减少 stale backups，不需要 oracle change detector。Reward 结论更条件化，取决于 planning budget 与 half-life。下一步应加入 gradual/stochastic drift；即使 reward winner 改变，freshness-aware search control 减少过期 planning computation 仍是清晰且有价值的 Core RL 结论。

## 复现

当前 extended result：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_extended.json

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended --kind dyna-aging
```
