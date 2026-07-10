# Continual Dyna With Model Aging 中文报告

状态：独立 planning/model-based proposal。当前已有 20-seed extended half-life/budget sweep，并已完成 abrupt/gradual/stochastic drift extension 的 extended CPU run。

## 摘要

Dyna-style planning 通过 learned model 做 background backups，让 agent 在不增加真实环境交互的情况下改进 value estimates。但在 nonstationary world 中，同一个机制也可能放大过期知识。本 proposal 把 model freshness 作为第一等 Core RL 问题：一个小型 online Dyna agent 能否根据 recency 或 prediction error 来 age/distrust model entries，使 planning 在环境改变后仍然有用？当前 20-seed fixed-change extended sweep 显示，recency aging 和 recency/error gating 能在不使用 oracle change detector 的情况下显著降低 stale-backup rate；reward 改善在部分 high-budget setting 中存在，但依赖 planning budget 和 half-life。第二轮 drift extension 已经完成，覆盖 abrupt、gradual 和 stochastic nonstationarity。结果支持在 abrupt/gradual drift 下使用 freshness-aware high-budget planning，但不支持“model aging 在 stochastic drift 中也普遍 reward 最优”的说法。新增 reward/staleness Pareto frontier 分析进一步把 reward winner 和 low-staleness computation tradeoff 分开，使最终结论更适合写成条件化的 freshness-aware search control，而不是某个 aging rule 普遍获胜。

## 独立研究总结

本研究问：continual Dyna agent 在世界变化后应当何时信任 learned model？RL 问题是一个 layout 会中途改变的 continuing gridworld，agent 不 reset，继续行动、学习和 planning。实现方法比较 no planning、random keep-model planning、oracle model flushing、recency-weighted model aging 和 recency/error-gated model aging。fixed-change extended experiment 改变 planning budgets `0, 1, 5, 20`、model-handling rules 和 aging half-lives `250, 750, 1500, 4000`；主要指标是 average reward、stale-backup rate、model error、planning TD magnitude 和 post-change recovery window。当前结果显示 freshness-aware sampling 能显著降低 stale backups；reward 改善在部分高 planning budget 条件下存在，但依赖 half-life 和 budget。drift extension 进一步测试 abrupt、gradual 和 stochastic nonstationarity：abrupt/gradual 条件支持 high-budget freshness-aware planning，stochastic 条件则低 reward、方差较大，并且 keep-model planning 仍然有竞争力。新增 Pareto-frontier analysis 明确显示 reward winner 与低 staleness computation tradeoff 不一定相同，因此最终 claim 应聚焦 search-control freshness 的适用边界，而不是 universal reward superiority。

## Proposal Template Answers / 提案模板回答

Focused RL question：在 continual Dyna agent 中，环境变化后 learned model entries 什么时候不应该继续获得 planning computation？本 proposal 研究 planning trust 和 search-control freshness，不只是问“more planning 是否提高 reward”。

Setting / testbed：主环境是 midstream layout change 的 continuing gridworld，不重置 agent。它大到 planning 有意义，小到可以标注 stale model entries，因此能做 model-freshness diagnostics。第二个已完成的 drift testbed 包含 abrupt、gradual 和 stochastic phase changes，用于测试 single clean switch 之外是否仍存在 model-aging tradeoff。

Implemented comparison：比较 no planning、keep-model Dyna、oracle model flushing、recency aging 和 recency/error gating，跨 planning budgets 和 aging half-lives。oracle flush 明确只是 diagnostic，不是现实算法。

Metric / figure：主要证据是 late reward、stale-backup rate、model error、planning budget 和 half-life 的关系。一个有价值的结果可以是 tradeoff curve，而不一定是单一 winner，因为核心问题是 model freshness 如何改变 computation 的价值。

Compute need / fallback：20-seed abrupt-change grid 已完成。drift extension 也已完成，配置 10 seeds，写出 `1,800,900` 行 metrics 和 `690` 个 condition groups。现在诚实 fallback 不再是“drift pending”，而是承认第一轮 drift extension 足以限定 claim，但仍不足以覆盖 repeated naturalistic changes 或更大的 stochastic state spaces。

## 独立研究范围

这是一个关于 model aging 下 search control 的独立 planning study。它问 continual agent 如何决定 learned model 的哪些部分值得 planning。核心对象不只是 planning budget 的大小，而是被选中进行 simulated backup 的 model entries 是否新鲜、可信、仍然值得消耗计算。

本报告不研究 replay buffers 或 offline model learning。model 是 compact、online updated，并被查询用于 planning backups。这与课程约束直接相关：agent 不存储旧 experience 并 replay，而是维护可能过时的 learned model entries。

## 证据等级

证据等级：强证据，支持 abrupt nonstationarity 和 model-freshness diagnostics。已完成结果包含 20 seeds、4 个 planning budgets、多种 model-handling rules 和 4 个 aging half-lives。它直接测量 stale-backup rate 和 model error，因此支持 mechanism claim，而不是只支持 reward claim。

drift extension 为 abrupt-change grid 之外提供了中等强度证据。对应结果路径是 `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`，包含 abrupt、gradual 和 stochastic nonstationarity。post-late headline comparisons 在检查到的关键条件中具有完整 seed coverage；部分 narrow early post-switch bins 因 gradual/stochastic switch timing 只有 partial seed coverage，因此不作为主结论依据。这个 extension 支持更精确的 claim：当 planning computation 较大且 nonstationarity 具有可恢复的时间结构时，model freshness 是有价值的 search-control 信息；但 stochastic drift 并没有显示清晰的 model-aging reward advantage。

## 论文式贡献与 Claim 边界

本报告的贡献是 planning-computation analysis，而不是又一条 Dyna reward curve。它把 model freshness 当成决定哪些 simulated backups 获得有限计算的变量，并且把 stale-backup rate 与 reward、model error 一起报告。这直接对应 Alberta Plan 中长期 agent 如何在 ordinary experience 下管理 learned models 的问题。

claim 边界是：当前结果最强地支持 stale entries 可诊断、且环境具有足够 temporal persistence 让 planning 有帮助的情形。它显示 recency 和 recency/error search control 可以在没有 oracle change signal 的情况下减少 stale computation，但没有证明某个 half-life 或 aging rule 普遍最优。drift extension 已经削弱了任何过度宽泛的 claim：stochastic drift 在当前实验中不是由 model aging 获胜，因此更 defensible 的贡献是一个条件化的 search-control account。

## 研究动机

Alberta Plan 把 learned models 和 background planning 放在长期 agent 的核心位置。一个 base agent 不应只被动更新当前 transition，还应利用已学到的模型在有限计算预算内做额外 value updates。经典 Dyna 的成功故事通常是 stationary world 中的 sample efficiency：模型越准，planning 越能加速学习。

Continual setting 改变了问题本质。长期 agent 的 model entry 是过去 experience 的总结，而不是永远正确的 world law。当 goal、hazard、transition probability 或 reward consequence 改变后，旧 model entry 可能仍然占据模型表。若 agent 继续均匀抽样这些 entries，planning budget 就可能从“加速新知识”变成“反复备份旧知识”。这正是 ordinary experience 和 temporal uniformity 下 model-based RL 的核心难点。

本 proposal 不是问“Dyna 是否比 Q-learning 更快”，而是问“当 model knowledge 的 freshness 未知时，agent 应该如何信任或折扣自己的模型”。这个角度比普通 changing-maze Dyna 更贴近 Alberta Plan：关键不只是有模型，而是如何管理模型、搜索控制和有限计算。

## 研究问题

主问题：在 continuing nonstationary task 中，小型 Dyna agent 能否通过 online model aging 或 error gating，在保留 planning benefit 的同时减少 stale model backups？

子问题包括：aggressive aging 是否会牺牲 change 前的 planning benefit；stale-backup rate 是否能解释 post-change recovery；oracle flush 是否过于粗糙且不 realistic；recency 和 model error 的组合是否比单纯 recency 更好；freshness control 是否需要足够 planning budget 才能体现在 reward 上；同样的 model-aging tradeoff 是否能延伸到 gradual 和 stochastic nonstationarity，还是主要只适用于 abrupt-change diagnostics。

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

当前 fixed-change extended run 的变量是 model mode、planning budget 和 half-life。主要指标包括 real-step average reward、stale-backup rate、model one-step prediction error、planning TD magnitude、model size、Q norm 和 recovery window。报告图使用 late post-change seed-tail condition summaries，并把 heatmap 作为主视图：行表示 planning budget 与 model handling，列表示 half-life 或非 aging controls，颜色表示 measured outcome。这样避免早期多曲线图被长图例压缩，也不会静默丢掉 half-life 维度。

第二轮 drift extension 使用 runner `continual_dyna_model_aging_drift`，结果路径为 `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`。该 run 配置 10 seeds、每 seed 20000 steps，共写出 `1,800,900` 行 metrics 和 `690` 个 condition groups。drift modes 包括 abrupt switch、gradual phase mixing 和 stochastic phase changes。它的作用不是替换主环境，而是回答一个更严格的问题：model aging 是否只是在 single clean switch 中好看，还是在更平滑或随机的变化中仍然有可解释价值。headline 使用 post-late comparisons；早期 post-switch 的少数 bins 有 partial seed coverage，不作为核心结论。

成功标准不是“某个方法在一个 budget 下 reward 稍高”。更严谨的判据是：方法是否在不用 oracle change detector 的情况下减少 stale backups；减少 stale backups 是否伴随 post-change recovery 改善或至少不显著破坏 pre-change benefit；不同 planning budget 下是否出现一致 tradeoff；半衰期是否过于敏感。当前日志可以支持 reward/staleness Pareto frontier 和 planning TD magnitude 诊断，但还不能支持严格的 per-backup causal utility claim，因为 runner 记录的是 aggregate planning TD magnitude，而不是每次 simulated backup 的 counterfactual value improvement。

Extended sweep 的作用是把早期 pilot 中固定 half-life 和 5 seeds 的证据升级成更可信的 sensitivity analysis。当前结果正好说明 reward 差异需要谨慎解释：freshness control 稳定减少 stale planning computation，但 reward ranking 会随 budget 和 half-life 改变。

## 实验设计依据

changing gridworld 的作用不是做传统 maze benchmark，而是让 stale model entries 可定义、可计数。这个 diagnostic visibility 对研究问题是必要的：单独 reward curve 无法告诉我们 planning 是因为 model useful 而有帮助，还是因为 model obsolete 而有害。planning budgets `0, 1, 5, 20` 分离 no-planning baseline、low-compute regime 和 high-compute regime，在 high-compute regime 中 stale backups 更可能主导结果。

half-life sweep 是主要科学控制。很短的 half-life 会快速不信任旧知识，但可能丢掉仍然有用的结构；很长的 half-life 会保留更多知识，但也可能继续规划 stale entries。因此正确结果不一定是一个最佳 half-life，而是展示 freshness 何时帮助、何时只是降低有效 planning 的 map。

## 当前结果

当前 fixed-change extended result path 是 `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`。

下面三张 heatmap 是当前主结果图。它们比早期多折线图更适合回答本课题问题：freshness-aware planning 是否减少 stale computation，以及这种减少是否能在不同 planning budget 和 half-life 下转化为 reward/recovery。

![Late average reward heatmap by planning budget, model mode, and half-life.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended/figures/report_dyna_aging_reward_heatmap.png)

![Late stale-backup rate heatmap by planning budget, model mode, and half-life.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended/figures/report_dyna_aging_stale_heatmap.png)

![Late model-error heatmap by planning budget, model mode, and half-life.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended/figures/report_dyna_aging_model_error_heatmap.png)

下面的 bar-summary figures 是 secondary check：它们更直接展示 seed uncertainty，因此适合用来确认 heatmap 中看到的 regime 是否跨 seeds 稳定。

![Late average reward by planning budget, model mode, and half-life.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended/figures/report_avg_reward_post_late_by_budget.png)

![Late stale-backup rate by planning budget, model mode, and half-life.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended/figures/report_stale_backup_rate_post_late_by_budget.png)

![Late model error by planning budget, model mode, and half-life.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended/figures/report_mean_model_error_post_late_by_budget.png)

Extended run 中，planning budget `20` 时 keep-model 的 late stale-backup rate 为 `0.213 +/- 0.065`。Recency aging 在 half-life `250` 时几乎降到 `0`，在 half-life `1500` 时约 `0.00058 +/- 0.00017`，在 half-life `4000` 时约 `0.0204 +/- 0.0044`。这说明不依赖 oracle change detector 的 freshness weighting 可以显著改变 planning computation 的内容。

Reward 结果更微妙。Budget `20` 时，keep-model late reward 为 `0.0828 +/- 0.0113`，oracle flush 为 `0.0906 +/- 0.0060`。Recency aging 随 half-life 大约在 `0.0865` 到 `0.0925` 之间，recency/error gate 大约在 `0.0822` 到 `0.0925` 之间。最好的 freshness 条件与 oracle flush 接近或略高，但差异依赖 half-life，不应写成普遍 reward superiority。

Budget `5` 下，keep-model 和 oracle flush 的 late reward 都很强，约 `0.096-0.097`；aggressive half-life `250/750` 能减少 stale backups，但会明显伤害 late reward。Budget `1` 下，freshness methods 仍能降低 stale backups，但 reward recovery 对所有方法都较弱。这提示 model freshness 不是单独变量；它与 planning budget 和环境时间尺度强交互。

完成的 drift extension result path 是 `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`。下面的 headline comparison 使用 phase-1 post-late seed-tail groups，把 `oracle_flush` 只当作 diagnostic，不放入 realistic method 竞争。表中的最好 realistic method 是每种 drift mode 下 post-late reward 最高的非 oracle condition；如果 keep-model 本身获胜，表中就直接写 keep-model，并在 interpretation 中说明 model-aging tradeoff。

| Drift mode | 最好 realistic method | keep-model baseline | reward | stale-backup rate | model error | interpretation |
|---|---|---|---|---|---|---|
| Abrupt | `dyna_5_keep_model` | same | `0.09598 +/- 0.00112` | `0.28869` | `0.00762` | reward winner 是普通 Dyna，但 `dyna_20_recency_error_gate`、half-life `1500` 几乎持平（`0.09501 +/- 0.00141`），同时把 stale-backup rate 降到 `0.00056`。 |
| Gradual | `dyna_20_recency_error_gate`，half-life `1500` | `dyna_20_keep_model` | `0.09536 +/- 0.00141` vs `0.05945 +/- 0.03210` | `0.02092` vs `0.30444` | `0.01201` vs `0.01168` | freshness-aware high-budget planning 同时赢在 reward 和 stale computation；model error 接近，说明收益主要来自 search control。 |
| Stochastic | `dyna_5_keep_model` | same | `0.03370 +/- 0.01237` | `0.50431` | `0.01649` | 当前 stochastic setting 没有 model-aging winner；最好的 phase-1 aging condition 是 `dyna_20_recency_aging`、half-life `1500`，reward 更低（`0.02495 +/- 0.01113`），虽然 stale rate 较低（`0.45612`）。 |

在 gradual drift 中，最好条件是 `dyna_20_recency_error_gate`、half-life `1500`，post-late average reward `0.09536 +/- 0.00141`，stale-backup rate `0.02092`，mean model error `0.01201`。这比单次 abrupt switch 更有说服力，因为环境变化不是瞬间完成，agent 必须在旧知识仍部分可用、新知识逐渐显现的过程中分配 planning computation。

在 stochastic drift 中，结果并不支持 model aging 普遍有效。最好的 post-late condition 是 `dyna_5_keep_model`，mean `0.03370 +/- 0.01237`，stale-backup rate `0.50431`；`dyna_20_keep_model` 和 `dyna_20_recency_aging` 的均值更低且 CI 较宽。Aggregate planning-depth pattern 也显示差异：abrupt drift 中 planning `1/5/20` 的 post-late average reward 分别为 `-0.01772/0.06339/0.09155`，gradual drift 为 `-0.02145/0.01760/0.06365`，而 stochastic drift 为 `0.01737/0.01367/0.01183`。也就是说，只有当额外 planning 本身有帮助时，freshness-aware search control 才有机会改进 computation quality。

![Drift-extension post-late average reward heatmap.](drift_figures/report_drift_reward_heatmap.png)

![Drift-extension post-late stale-backup heatmap.](drift_figures/report_drift_stale_heatmap.png)

![Drift-extension post-late model-error heatmap.](drift_figures/report_drift_model_error_heatmap.png)

新增 Pareto-frontier analysis 提供了 drift extension 的更清晰视角。每个点是一个 realistic non-oracle post-late condition；如果同一个 drift mode 中不存在另一个 realistic condition 同时拥有更高 reward 和更低 stale-backup rate，那么该点就在 frontier 上。这个图比只报告最高 reward 条件更适合 search-control 讨论，因为 model aging 的价值有时不是直接成为 reward winner，而是在几乎不损失 reward 的情况下降低 stale computation。

![Drift-extension reward/staleness Pareto frontier.](drift_figures/report_drift_reward_stale_frontier.png)

| Drift mode | Highest-reward frontier point | Lowest-stale frontier point | Interpretation |
|---|---|---|---|
| Abrupt | `dyna_5_keep_model`: reward `0.09598 +/- 0.00112`, stale `0.28869` | `dyna_20_recency_error_gate`, half-life `100`: reward `0.09118 +/- 0.00551`, stale `0.00000` | keep-model 的 reward 略高，但 freshness-aware high-budget planning 提供了几乎保留 reward、同时显著降低 stale backups 的替代点。 |
| Gradual | `dyna_20_recency_error_gate`, half-life `1500`: reward `0.09536 +/- 0.00141`, stale `0.02092` | `dyna_1_recency_aging`, half-life `100`: reward `-0.02317 +/- 0.00132`, stale `0.00000` | 真正有用的 frontier 区域是 high-budget recency/error gating；zero-stale endpoint reward 很差，说明过度 aging 会丢掉 planning value。 |
| Stochastic | `dyna_5_keep_model`: reward `0.03370 +/- 0.01237`, stale `0.50431` | `dyna_5_recency_aging`, half-life `100`: reward `0.00886 +/- 0.00318`, stale `0.33054` | frontier 明确显示 stochastic setting 的负结果：降低 stale backups 没有转化为更好的 control reward。 |

## 分析

本 proposal 的主要 insight 是：planning 的质量不只由模型是否存在或 planning steps 数量决定，还由 search-control distribution 是否尊重模型新鲜度决定。普通 keep-model Dyna 在 nonstationary change 后仍然可能把相当比例 backup 分配给旧 phase entries。Recency aging 把“最近真实观察过的 entry 更可信”这个弱但可在线计算的原则引入 search control，从而显著降低 stale computation。Pareto frontier 进一步细化了这个结论：abrupt drift 中存在 near-reward-preserving low-staleness alternative；gradual drift 中 high-reward frontier 本身就是 recency/error gating；stochastic drift 中 stale reduction 只形成弱 tradeoff，没有带来更好 control performance。

为什么 oracle flush 不一定最好？Flush 会清空所有旧知识，包括一些仍可复用的 transition structure。Recency aging 更平滑：旧而未再观察的 entries 概率衰减，但新近访问和更新过的 entries 会重新获得 planning 权重。因此它可能在避免 stale backups 与保留 reusable structure 之间形成中间区域。

为什么 stale-backup rate 比 reward 更关键？在小 gridworld 中，agent 可能靠真实交互逐渐恢复 reward，即使 planning 仍有浪费。但 Alberta Plan 设想的 agent 会有许多 predictions、models、options 和 control values 竞争有限计算。即使 reward 没有立刻崩溃，把 background computation 花在过期知识上也会降低整个 agent 的长期可扩展性。drift extension 进一步说明，stale-backup reduction 与 reward improvement 不是同义词；stochastic drift 下 freshness diagnostics 可能更干净，但 control reward 并没有随之改善。

## 局限与有效性威胁

第一，fixed-change 环境是 abrupt deterministic change，因此 stale model entries 比较容易定义。这对机制诊断有用，但可能高估 freshness heuristic 在更自然 stochastic worlds 中的清晰性。drift extension 已经部分处理这个问题，并给出 mixed answer：abrupt/gradual drift 仍支持 high-budget freshness-aware planning，stochastic drift 则低 reward、噪声大，并且没有由 model aging 获胜。

第二，reward ranking 对 half-life 和 planning budget 敏感。报告应把最稳健 claim 放在 stale-backup reduction、model error 和 recovery diagnostics 上，而不是把 mean reward 小差异写成普遍胜利。

第三，extended run 已经显示 `250/750/1500/4000` 等 half-life 会导致不同 tradeoff。最终报告必须讨论这个 sensitivity，而不是只报告最好的一条曲线。

第四，当前 model 是 tabular deterministic one-step model。更复杂状态抽象或随机 transitions 下，model error 和 recency 的解释会更困难，需要 uncertainty-aware 或 distributional model diagnostics。后续最值得补的是 repeated changes、具有更清晰 controllability structure 的 stochastic transition family，以及 per-backup planning utility diagnostics。

## 审稿式批评与回应

严格 reviewer 可能说：“这只是 changing maze 上的 Dyna-Q。”回应是：报告不把分数作为唯一结果，而是记录 stale-backup rate、planning TD magnitude、model error 和 recovery window，把问题定义为 model freshness 和 search control。

另一个 reviewer 会说：“flush-on-change 不 realistic。”回应是：flush 只保留为 oracle diagnostic，用来解释 freshness 上界；真正方法只使用 online recency 和 prediction error。

Sutton-style reviewer 会问：“这个机制是否符合 ordinary experience 和 temporal uniformity？”回应是：recency 和 model-error signals 都来自 agent 自身的 stream，不需要 replay buffer、offline training 或外部 change labels。

Statistics reviewer 会指出：“reward winner 依赖 half-life。”回应是：报告已经把 strong claim 收紧为 freshness-aware search control reduces stale backups；reward 部分作为 budget/half-life tradeoff 解释。

逐 proposal 审查矩阵：

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| Alberta Plan | planning 应是 ordinary experience 中 learned models 的问题，不是 offline replay。 | 使用 online learned model 和 planning backups，不使用 replay buffer。 | 环境仍是 compact synthetic gridworld。 |
| Planning reviewer | reward alone 无法诊断 stale planning。 | 报告 stale-backup rate、model error、planning budget、half-life 和 reward/staleness Pareto frontier。 | true counterfactual planning utility per backup 仍未记录。 |
| Nonstationarity reviewer | abrupt change 可能让 aging 看起来太容易。 | 完成第一轮 abrupt/gradual/stochastic drift extension，并据此收紧结论。 | 仍需 repeated changes 和更大的 stochastic transition settings。 |
| 统计 | half-life sensitivity 可能被单条曲线隐藏。 | 主结果改为 heatmap，报告数值例子，并加入 reward/staleness frontier。 | repeated-change statistics 仍缺。 |
| 严格老师 | 不要声称 universal reward superiority。 | 报告强调 stale-backup reduction 和 tradeoffs。 | 部分 reward comparison 仍依赖 budget。 |

## 结论

Continual Dyna Model Aging 把 Dyna 从“多做 planning 是否更快”的熟悉故事推进到更有 Alberta Plan 意义的问题：长期 agent 什么时候应该信任自己的 learned model？当前 extended sweep 支持 model freshness 是 first-class planning variable：recency aging 和 recency/error gating 能显著减少 stale backups，不需要 oracle change detector。Reward 结论更条件化，取决于 planning budget、half-life 和 nonstationarity 的时间结构。完成的 drift extension 显示，abrupt-change 结论部分延伸到 gradual drift，但不能在 stochastic drift 中写成清晰 reward advantage。这个 mixed result 反而让课题更有学术价值，因为它找到了 model freshness 作为 search-control information 的适用边界。

## 复现

当前 extended result：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_extended.json

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended --kind dyna-aging

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/continual_dyna_model_aging_drift/config_extended.json

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended --kind dyna-aging-drift --figure-dir final/reports/integrated/continual_dyna_model_aging/drift_figures

PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/core-rl-pycache MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/analyze_dyna_frontier.py --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended --out-dir final/reports/integrated/continual_dyna_model_aging/drift_figures
```
