# 更大独立 Proposal 中文索引

`integrated/` 包含三个更大的独立 Core-RL 课题。它们不是把多个小实验拼成一篇总论文，而是各自提出更综合但仍然独立的研究问题。Scale-Invariant Continuing Control 研究 reward translation 与 feature scale 同时变化时的 continuing control invariance，目前已有 fixed-condition pilot 和 20-seed no-reset unit-switch extension，但 full fixed-condition extended grid 仍未完成；Continual Dyna With Model Aging 研究非平稳环境中 model freshness 如何影响 planning backups，目前已有 20-seed half-life/budget extended sweep；Predictive State Plasticity 研究 learned predictions 是否能成为有用 state，目前是 20-seed 负向 first-gate 和 redesign 方向，不是 solved plasticity 方法。

导航时应把这些目录看成独立研究主题，而不是把普通 proposal 合并替换成一个总论文。Scale-Invariant report 研究 reward-origin 与 feature-unit mechanisms；Dyna Aging report 研究 model freshness 与 computation allocation；Predictive State Plasticity report 研究 learned predictions 在 partial observability 和 plasticity pressure 下是否成为可用 control state。普通 proposal 目录仍然是独立研究材料，应按各自 report 引用。

每个目录包含英文 `report.md` 与中文 `report_zh.md`，报告中的图片已经换成 `report_*.png` summary figures，避免大量图例压缩坐标区。
