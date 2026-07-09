# Dyna Planning Budget and Model Staleness 中文报告

状态：独立前置 proposal，已经完成 20 seeds extended run；最强用途是作为 integrated `Continual Dyna Model Aging` 的诊断基础，而不是单独作为最终正向结论提交。

## 摘要

Dyna planning 对 continual agent 很有吸引力，因为它把 ordinary experience 转成一个紧凑 learned model，然后用有限 background computation 改善 value，而不需要额外真实交互或 replay buffer。但在 changing world 中，更大的 planning budget 也可能把更多计算花在旧世界的 transition 上。本 proposal 研究 fixed per-step planning budget 是否会在 pre-change sample efficiency 与 post-change stale computation 之间产生 tradeoff。实验使用一个中途改变 goal 和 hazard layout 的 continuing gridworld。20 seeds extended run 显示：较大的 planning budget 在 change 前提升 reward，但 keep-model agent 在 change 后仍保留明显 stale-backup signal；即使 late reward 最终恢复，background computation 仍可能部分浪费在过期 model entry 上。因此这个 proposal 的价值不是证明 flush-on-change 是好算法，而是说明 model freshness 必须独立于 planning budget 被研究。

## Proposal Template Answers / 提案模板回答

Focused RL question：在 continuing nonstationary task 中，增加固定 Dyna planning budget 是否会造成 pre-change sample efficiency 与 post-change stale computation 的 tradeoff？本 proposal 研究 planning budget 和 model staleness，不是证明 oracle flush 是好算法。

Setting / testbed：testbed 是 changing continuing gridworld，使用 tabular Q-learning 和 compact one-step model。它让 planning 有意义，同时 model entries 可检查，layout change 后 stale backups 可计数。

Implemented comparison：实验改变 planning budget `0/1/5/20` 和 model handling `keep_model` vs `flush_on_change`。Flush 有 privileged information，只是 diagnostic；keep-model 是现实 precursor baseline。

Metric / figure：必须同时看 reward 和 stale-backup figures。只看 reward 无法回答问题，因为 policy 可以恢复，同时 background computation 仍在备份 obsolete model entries。

Compute need / fallback：20-seed extended result 已完成。诚实 fallback 是把它作为 Continual Dyna Model Aging 的 precursor diagnostic，而不是 final planning solution。

## 独立研究范围

本报告是独立前置研究。它负责回答为什么 model freshness 重要；integrated Continual Dyna Model Aging 报告负责研究 realistic aging 和 error-gating mechanisms。这个边界可以防止 oracle flush 被误读成算法贡献。

范围限制在 fixed planning budgets、uniform model sampling 和 abrupt gridworld change。本 proposal 不研究 learned search control、uncertainty-aware models 或 gradual drift；这些是 stale-backup failure mode 被建立后的自然下一步。

## 证据等级

证据等级：strong supporting/precursor evidence。完成的 20-seed、20000-step extended run 足以说明 planning 在 change 前有帮助，也足以说明 keep-model planning 在 change 后会继续把 computation 花在 old-phase entries 上。

但它不应被提升为 standalone positive planning algorithm。flush condition 使用 privileged change information，late reward differences 也不够稳健到支持 winner claim。强 claim 是 diagnostic：planning budget 和 model freshness 是不同设计变量。

## 研究动机

Alberta Plan 强调 learned models 和 background planning。经典 Dyna demonstration 往往强调 stationary setting 里的 sample efficiency：agent 学到模型后通过 simulated backups 比纯 model-free 更新学得更快。Continual learning 的问题更困难：模型不是永恒真理，而是 stream 的记忆；当世界改变后，过去正确的 transition 和 reward consequence 可能变成误导。如果 agent 仍然均匀抽样旧 model entry，planning 就可能从“加速学习”变成“强化过期知识”的机制。

因此这里的 Core RL 问题不是简单的“planning 是否有用”，而是“在有限 per-step computation 下，agent 应该如何把 planning 分配给 freshness 不同的 model entry”。这个前置 proposal 先隔离 planning-budget 和 staleness 的关系，为后续 model-aging mechanism 提供必要证据。

## 研究问题

主问题：在 continuing nonstationary task 中，planning budget 如何影响 change 前的学习速度和 change 后的 stale computation？

具体子问题包括：增加 Dyna backups 是否确实提高 change 前 reward；change 后 keep-model agent 是否继续从旧 phase 的 model entry 做 backups；oracle flush 是否能帮助区分“planning budget 本身”和“model freshness”这两个因素；只看 reward curve 是否会掩盖 planning computation 的过期使用问题。

## Alberta Plan 关联

这个 proposal 直接对应 Alberta Plan 中的 learned models、background planning、ordinary experience、limited computation、continuing control 和 temporal uniformity。这里的 model 是在线学到的一步 transition/reward table，不是 replay buffer。Agent 没有保存 dataset 后离线训练，而是在每个真实 transition 后做一次在线 value/model update，并在固定 computation budget 内做少量 model-based TD backups。

## 环境设计

实验环境是 continuing gridworld。环境包含 start region、rewarding goal region、hazards 和 small step cost；没有 terminal training episode reset，agent 持续交互。Stream 进行到一半时环境切换 phase，goal 和 hazards 位置改变。这种设计比二状态 toy problem 更有结构，但仍足够简单，可以明确记录 Q norm、model size、stale-backup rate 和 recovery windows。

当前 extended run 使用 `11 x 11` grid、seeds `0-19`、每个 seed/condition `20000` online steps，phase change 在 midpoint 发生。这个 setting 的作用不是制造大 benchmark，而是让 Dyna planning 在一个可解释的 continual control stream 中暴露 model staleness。

## Agent 与 Baseline

所有 agent 都使用 tabular Q-learning 处理真实 transition，行为策略为 epsilon-greedy，参数为 `alpha = 0.1`、`gamma = 0.95`、`epsilon = 0.1`。每次真实交互后，agent 把当前 state-action 的 next state、reward 和 phase label 写入 learned model，然后执行 `0`、`1`、`5` 或 `20` 次 sampled planning backups。

`keep_model` 是现实 baseline：agent 不知道 change 发生，继续保留所有旧 model entries。`flush_on_change` 是 oracle diagnostic：它在 phase change 时准确清空模型。这个条件不是可部署算法，因为真实 continual agent 通常没有完美 change signal。它的作用是提供一个上界诊断，帮助判断 post-change 行为有多少来自 stale model entries。

## 实验设计

当前可引用 extended result path 是 `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended`。实验变量包括 planning budgets `0/1/5/20` 和 model modes `keep_model/flush_on_change`。主要指标包括 online average reward、stale-backup rate、model size、Q norm、phase 和 recovery window。

这里 reward 不是唯一指标。Reward 回答 policy 是否恢复；stale-backup rate 回答 planning computation 是否仍在使用与当前环境不匹配的 model entries。一个方法可能 late reward 恢复，但仍把一部分有限计算浪费在过期知识上；在更大的 Alberta Plan 风格 agent 中，这种计算分配问题会影响 predictions、options、planning tasks 之间的资源竞争。

## 实验设计依据

设计刻意把 reward 与 process diagnostics 配对。changing gridworld 让我们能标注 model backup 是否来自 old phase，因此 stale-backup rate 是 planning relevance 的直接指标。Planning budgets `0`、`1`、`5`、`20` 分离 no-planning behavior、low-compute planning 和 high-compute planning；后者最容易暴露 stale search control 的问题。

oracle flush baseline 的作用是诊断 model contents，而不是提出 realistic agent。如果 flush 和 keep-model 的 late reward 类似，但 stale-backup rate 差异很大，那么结论就是 reward 会隐藏 computation misuse。这正是后续 model-aging proposal 的动机。

## 结果

![20 seeds extended run 中不同 planning budget 和 model handling 的 late average reward。](../../../../experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended/figures/report_avg_reward_post_late_by_budget.png)

![20 seeds extended run 中不同 planning budget 和 model handling 的 late stale-backup rate。](../../../../experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended/figures/report_stale_backup_rate_post_late_by_budget.png)

Change 前，planning 明显提高 reward。No planning 的 pre-change average reward 约为 `0.070`；one backup 约为 `0.078`；five backups 约为 `0.078-0.079`；twenty backups 约为 `0.079`。这个收益很快饱和，但足以说明在模型新鲜时 Dyna planning 是有用的。

Change 后，所有 planning setting 都受到冲击。更关键的是 stale-backup signal。在 keep-model 条件下，budget `20` 的 stale-backup rate 在 post-change 前 250 步约为 `0.749`，在 250-500 步约为 `0.910`，在 500-1000 步约为 `0.835`，late post-change window 中仍约为 `0.294 +/- 0.049`。Budget `5` 的 late stale-backup rate 约为 `0.267 +/- 0.021`，budget `1` 的 late stale-backup rate 约为 `0.675 +/- 0.010`。这说明 keep-model agent 即使继续学习新经验，仍会把一部分 background computation 分配给旧 phase 条目。

Flush-on-change 按定义消除了 stale backups，但它不是最终方案，也不提供简单 reward 胜利。Budget `20` 下，late reward 对 flush 约为 `0.07198 +/- 0.00847`，对 keep-model 约为 `0.07217 +/- 0.00870`。Budget `5` 下，late reward 对 flush 约为 `0.03855 +/- 0.0145`，对 keep-model 约为 `0.03924 +/- 0.00981`。也就是说，在这个扩展实验中，late reward 可以恢复到相近水平，但 stale computation 问题仍然存在。

## 分析

这个结果最重要的 insight 是 reward 与 planning quality 可以分离。如果只看 budget `20` 的 late reward，可能会误以为 keep-model 没有问题，因为它与 oracle flush 几乎一样。但 stale-backup rate 说明另一件事：agent 的 planning computation 仍有非平凡比例落在旧 phase model entries 上。在小 gridworld 中这种浪费未必立刻拖垮 reward；但在更大 continual agent 中，有限 computation 要在很多 predictions、options、models 和 value updates 之间分配，stale planning 就会变成真实资源浪费和错误知识保留问题。

实验还说明 larger planning budget 不是单调好事。更多 backups 在 change 前提高模型使用效率，但 change 后也放大了不良 search control 的后果。因此最终问题不应写成“选择多少 budget”，而应写成“在固定 budget 下学习或设计一个尊重 model freshness 的 search-control distribution”。

这也是为什么本 proposal 更适合作为 `Continual Dyna Model Aging` 的前置证据。它回答“为什么需要 freshness mechanism”，而不是直接提供最终 mechanism。后续更有价值的工作应该比较 age-weighted sampling、prediction-error gating 或其他在线 freshness estimates，而不是把 oracle flush 包装成算法。

## 有效性威胁

Phase change 是 abrupt 且由实验者安排的。Keep-model agent 不知道 change signal，但 flush diagnostic 知道，这使得 flush 只能作为诊断上界，而不能作为 temporal-uniform continual agent 方法。

模型是 deterministic tabular model，因此可以通过 phase label 明确定义 stale entry。更真实的 stochastic environment 需要 uncertainty、recency statistics 或 prediction-error traces，而不能直接依赖干净的 phase label。

当前实验只有一次 change。更强的 planning 研究应加入 repeated changes、gradual drift 和 stochastic transition changes，检验 freshness mechanism 是否只是适配单次 switch。

当前 keep/flush 条件使用简单 uniform model sampling 和固定 learning rate。后续研究需要直接比较 search-control mechanisms，而不仅仅改变 model content。

## 审稿式批评与回应

Planning reviewer 会指出：stationary Dyna result 太常见，不足以构成 Alberta Plan 相关研究。回应是：本实验使用 continuing nonstationary gridworld，增加 post-change recovery windows 和 stale-backup diagnostics，关注 model freshness 而非普通 sample efficiency。

Continual-agent reviewer 会指出：flush-on-change 如果当成算法就违反 ordinary experience 和 temporal uniformity。回应是：报告明确把 flush 标成 oracle diagnostic，不把它作为可部署 solution。

Statistics reviewer 会指出：早期 5 seeds pilot 太弱。回应是：当前引用结果已经更新为 20 seeds、20000 steps、larger grid extended run，且结论只保留稳健部分：change 前 planning 有用，change 后 keep-model 有 persistent stale-backup signal。

Sutton-style reviewer 会追问：你到底在研究 reward score，还是研究 agent 如何组织和使用知识？回应是：报告把 stale-backup rate 和 model freshness 放在中心，reward 只是一个结果指标，不是唯一评价标准。

逐 proposal 审查矩阵：

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| Planning | stationary Dyna result 太常见。 | 使用 nonstationary continuing gridworld 和 stale-backup diagnostics。 | 仍只有一次 abrupt change。 |
| Continual learning | flush-on-change 不符合 temporal uniformity。 | 明确 flush 只是 oracle diagnostic。 | realistic aging/search-control 交给 integrated proposal。 |
| 统计 | 5-seed pilot 太弱。 | 使用 20-seed extended run。 | recovery-window tables 还可更清楚。 |
| Computation | reward 会隐藏 stale planning。 | stale-backup rate 是主指标。 | planning utility per backup 仍较粗。 |
| 严格老师 | 不要把 precursor 包装成 final algorithm。 | 结论明确它是 model-aging 的诊断基础。 | 若不强调 evidence level，读者仍可能过度关注 flush。 |

## 结论

Dyna Planning Budget 是有价值的独立前置课题，因为它展示了一个 Core RL 失败模式：planning budget 和 model freshness 是不同的设计变量。Planning 在模型新鲜时有用，但在 changing stream 中，keep-model agent 可以在 late reward 恢复的同时仍然把一部分 planning computation 花在过期条目上。最有价值的下一步不是继续比较 flush，而是实现真实在线 freshness mechanism，这正是 integrated `Continual Dyna Model Aging` proposal 的研究对象。

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/dyna_planning_budget/config_extended.json

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py --result-dir experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended --y-key avg_reward --group-keys planning_steps model_mode

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py --result-dir experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended --y-key stale_backup_rate --group-keys planning_steps model_mode
```
