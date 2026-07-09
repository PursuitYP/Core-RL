# 当前状态报告（中文）

当前项目已经重构为清晰的 final-facing 结构：正式报告在 `final/reports/`，索引在 `final/indexes/`，历史碎片在 `final/archive/`。每个正式 report 都新增了 `report_zh.md` 中文审阅版本。

强主线候选包括 Reward-Centered Sarsa、Output-Controlled TD、Scale-Invariant Continuing Control、Continual Dyna Model Aging。Predictive State Plasticity 是高价值但当前为负向 gate 的综合方向。GVF Predictive State、Generate-and-Test、Options、TIDBD、Baird、Centered TD、On-policy Atlas、Bandit、Streaming Representation 等材料以负结果、支持性诊断或 redesign target 的方式保留。

代码仍位于 `experiments/alberta_core_rl/`，各 proposal 的实现拆在 `studies/` 下，配置在 `configs/` 下，结果在 `results/` 下。当前 indexed main results 主要是 5 seeds、5000 steps；extended CPU sweep 仍需等待 cpu_task 通道确认可用。
