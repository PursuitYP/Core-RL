# 原始需求覆盖审计（中文）

本项目已覆盖原始任务中的主要要求：围绕 Alberta Plan 和 Core RL，完成 Reward-Centered Sarsa 与 Output-Controlled TD 两条重点主线；补充多个课程资料推荐 proposal 和自设计 proposal；严格遵守 no replay buffer、no deep network、online streaming/continual learning；为每个正式 proposal 提供独立 report 和对应中文 `report_zh.md`。

当前材料诚实区分强 proposal、负结果、支持性诊断和 dropped sanity check。Reward-Centered Sarsa、Dyna Planning Budget、Predictive State Plasticity、Unit-Switching Continuing Control 和 Continual Dyna Model Aging 已有 20 seeds extended evidence；Output-Controlled TD 的 extended run 仍在运行，完成后需要纳入报告和索引。弱 proposal 没有被包装成正结果，而是记录失败原因、审稿批评和下一步 redesign。

结果索引、复现索引、中文总览、reviewer audit 和 archive proposal templates 已同步更新。所有正式中文报告已经从快速摘要扩展为可单独审阅的研究报告，包含研究动机、环境、方法、实验、结果、局限和复现命令。

剩余风险：Output-Controlled TD 的 extended 结果尚未索引；Scale-Invariant Continuing Control 的完整 fixed-condition extended grid 尚未运行；Dyna aging 仍缺 gradual/stochastic drift；许多 supporting/negative proposal 仍是 5-seed pilot，只能作为诊断或 redesign material；Predictive State Plasticity 当前是 extended negative gate，不是 learned-state 正结果；Options fixed-goal sanity、GVF cue-decodability、TIDBD canonical baseline 等仍需后续研究。
