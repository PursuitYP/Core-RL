# 当前项目计划快照（中文）

当前计划仍以四条强主线为优先级：Continual Dyna Model Aging、Reward-Centered Sarsa、Output-Controlled TD、Scale-Invariant Continuing Control。Reward-Centered Sarsa 已完成 20 seeds extended sweep；Output-Controlled TD 已完成 CPU-task 20 seeds extended sweep，当前结果为 `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`；Dyna Planning Budget 已完成 20 seeds larger-grid precursor diagnostic；Continual Dyna Model Aging 已完成 20 seeds half-life/budget extended sweep；Predictive State Plasticity 已完成 20 seeds negative gate；Unit-Switching Continuing Control 已完成 no-reset unit-change extension。

Scale-Invariant Continuing Control 仍是最强综合控制方向，完整 fixed-condition extended grid 已提交到 CPU task：`core-rl-scale-invariant-extended-33723554`。该任务在标准 artifacts 写出前不能作为 evidence。Reward-Centered Sarsa 与 Output-Controlled TD 是最清楚的独立主 proposal；Dyna aging 是 planning/model-based 方向最强主线，但最终结论应优先看 stale-backup reduction、recovery windows 和 half-life sensitivity，而不是只看 reward。

Predictive State Plasticity 当前是高价值 negative/redesign gate，不应写成正结果。下一步应加 cue-decodability、oracle-prediction control、feature ablation，再决定是否接入 generate-and-test/TIDBD。Options 必须先做 fixed-goal sanity。弱 proposal 的下一步是澄清机制和失败原因，而不是硬凑正结果。

文档计划：所有正式英文 report 都已有 `report_zh.md`，并且中文报告已从快速摘要扩展为可单独审阅的研究报告。关键 index/README 已配备 `_zh.md`；中文总览 `proposal_overview_zh.md` 作为详细快速审阅入口继续保留。
