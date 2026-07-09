# 当前项目计划快照（中文）

当前计划仍以四条强主线为优先级：Continual Dyna Model Aging、Reward-Centered Sarsa、Output-Controlled TD、Scale-Invariant Continuing Control。Reward-Centered Sarsa 已完成 20 seeds extended sweep；Dyna Planning Budget 已完成 20 seeds larger-grid precursor diagnostic；Continual Dyna Model Aging 已完成 20 seeds half-life/budget extended sweep；Predictive State Plasticity 已完成 20 seeds negative gate；Unit-Switching Continuing Control 已完成 no-reset unit-change extension。Output-Controlled TD 的 extended run 仍在运行，完成后需要更新报告、索引和图表。

Scale-Invariant Continuing Control 仍是最强综合控制方向，但完整 fixed-condition extended grid 较大，应在当前两个长任务完成后再安排，或提交到验证可用的 CPU task 队列。Reward-Centered Sarsa 与 Output-Controlled TD 是最清楚的独立主 proposal；Dyna aging 是 planning/model-based 方向最强主线，但最终结论应优先看 stale-backup reduction、recovery windows 和 half-life sensitivity，而不是只看 reward。

Predictive State Plasticity 当前是高价值 negative/redesign gate，不应写成正结果。下一步应加 cue-decodability、oracle-prediction control、feature ablation，再决定是否接入 generate-and-test/TIDBD。Options 必须先做 fixed-goal sanity。弱 proposal 的下一步是澄清机制和失败原因，而不是硬凑正结果。

文档计划：所有正式英文 report 都已有 `report_zh.md`，并且中文报告已从快速摘要扩展为可单独审阅的研究报告。关键 index/README 已配备 `_zh.md`；中文总览 `proposal_overview_zh.md` 作为详细快速审阅入口继续保留。
