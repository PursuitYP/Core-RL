# 十三个普通 Proposal 中文索引

每个子目录包含英文 `report.md` 和中文 `report_zh.md`。这些 proposal 都有独立研究问题，但证据强度不同：Reward-Centered Sarsa 与 Output-Controlled TD 是主线候选；Dyna Planning Budget 是独立 planning 诊断；GVF、generate-and-test、TIDBD、options、bandit、streaming representation 等方向目前包含负结果、独立机制诊断或需要 redesign 的材料。

不要把所有 proposal 等同为 submission-grade 正结果。当前项目更重视诚实解释：强 proposal 要突出机制与证据；弱 proposal 要说明为什么弱、失败暴露了什么 Core-RL 问题、下一步如何升级。除了本目录十三个普通 proposal，`../integrated/` 还包含四个更大的独立 Core-RL 课题：Scale-Invariant Continuing Control、Continual Dyna Model Aging、Predictive State Plasticity 和 Useful Predictive Knowledge。它们不是普通 proposal 的简单拼接，也不替代这里的十三个目录，而是各自有独立研究问题、实验流程和报告的更综合候选。

## 当前 Proposal 表

| Proposal | 当前定位 | 当前结果路径 | 报告入口 |
|---|---|---|---|
| Reward-Centered Sarsa | 独立主线，已有 20-seed extended evidence | `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended` | `reward_centered_sarsa/report.md` / `report_zh.md` |
| Output-Controlled TD | 独立主线，已有 20-seed extended evidence | `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended` | `output_controlled_td/report.md` / `report_zh.md` |
| GVF Predictive State | 负结果 / redesign | `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main` | `gvf_predictive_state/report.md` / `report_zh.md` |
| Generate-and-Test Features | 负结果 / redesign | `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main` | `generate_test_features/report.md` / `report_zh.md` |
| Doorway Options | 暂停 / quarantine，需 fixed-goal sanity | `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main` | `options_reusable_subtasks/report.md` / `report_zh.md` |
| TIDBD Plasticity | 支持性机制诊断 | `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main` | `tidbd_plasticity/report.md` / `report_zh.md` |
| Baird Off-policy Stability | 支持性稳定性警示 | `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main` | `baird_offpolicy_stability/report.md` / `report_zh.md` |
| Dyna Planning Budget | 独立 planning 诊断，已有 20-seed extended evidence | `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended` | `dyna_planning_budget/report.md` / `report_zh.md` |
| Centered TD Diagnostics | 独立 reward-centering 机制诊断 | `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main` | `centered_td_diagnostics/report.md` / `report_zh.md` |
| On-policy Stability Atlas | 独立 feature-scale stability atlas | `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main` | `onpolicy_stability_atlas/report.md` / `report_zh.md` |
| GVF Question Design | GVF useful prediction redesign aid | `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main` | `gvf_question_design/report.md` / `report_zh.md` |
| Nonstationary Bandit | limited-scope plasticity study | `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main` | `nonstationary_bandit/report.md` / `report_zh.md` |
| Streaming Representation | dropped auxiliary-prediction diagnostic | `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main` | `streaming_representation/report.md` / `report_zh.md` |

最终审阅时，优先读 `final/indexes/status_zh.md`、`final/indexes/results_zh.md` 和每个 proposal 的 `report_zh.md`。`final/archive/` 只保留早期碎片和审计记录，不作为当前结论来源。

## 更大独立 Proposal 入口

`../integrated/` 下目前共有四个更大独立 proposal。Scale-Invariant Continuing Control 和 Continual Dyna Model Aging 的完成度最高，分别对应 continuing-control invariance 和 continual planning/model freshness。Predictive State Plasticity 与 Useful Predictive Knowledge 更偏 representation/GVF 方向，已经有 staged evidence，但仍需要严格阅读各自报告中的限制、负结果和后续实验边界。最终选择题目时，不应把普通目录中的机制诊断和 integrated 目录中的大课题重复计数；例如某些 GVF/T-maze 诊断材料应作为 supporting evidence，而不是和更大的 predictive-knowledge 课题同时当作独立最终提交。
