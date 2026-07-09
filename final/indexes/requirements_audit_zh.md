# 原始需求覆盖审计（中文）

本项目已覆盖原始任务中的主要要求：围绕 Alberta Plan 和 Core RL，完成 Reward-Centered Sarsa 与 Output-Controlled TD 两条重点主线；补充多个课程资料推荐 proposal 和自设计 proposal；严格遵守 no replay buffer、no deep network、online streaming/continual learning；为每个正式 proposal 提供独立 report，并新增中文 `report_zh.md`。

当前材料还诚实区分了强 proposal、负结果、支持性诊断和 dropped sanity check。强主线已经有可复现实验和图表；弱 proposal 没有被包装成正结果，而是记录失败原因、审稿批评和下一步 redesign。结果索引、复现索引、中文总览和 archive fragments 都已同步更新。

剩余风险：大多数 main runs 仍是 5 seeds、5000 steps；extended CPU sweep 尚未完成；Predictive State Plasticity 仍是 first-gate negative；Options fixed-goal sanity、GVF cue-decodability、TIDBD canonical baseline 等仍需后续研究。
