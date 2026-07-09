# 当前项目计划快照（中文）

当前计划以四条强主线为优先级：Continual Dyna Model Aging、Reward-Centered Sarsa、Output-Controlled TD、Scale-Invariant Continuing Control。Dyna aging 优先级最高，因为 extended code path 真正扩展了 planning budgets 和 half-life sweep；Reward-Centered Sarsa 与 Output-Controlled TD 是最清楚的独立主 proposal；Scale-Invariant Continuing Control 虽然价值高，但 extended grid 较大，应在更小 sweep 验证后提交。

Predictive State Plasticity 暂不优先跑长 sweep，应先 redesign：加 cue-decodability、oracle-prediction control、feature ablation，再决定是否接入 generate-and-test/TIDBD。Options 必须先做 fixed-goal sanity。弱 proposal 的下一步是澄清机制和失败原因，而不是硬凑正结果。

文档计划：所有正式英文 report 已对应新增 `report_zh.md`；关键 index/README 已新增 `_zh.md`；中文总览 `proposal_overview_zh.md` 作为快速审阅入口继续保留。
