# 报告章节审计（中文）

日期：2026-07-09

这份审计检查 16 个 final-facing reports 是否显式包含最新 revise plan 要求的关键章节。它只是 heading/content-presence audit，不代表每个章节已经达到论文最终深度。当前结果：经过第一轮结构修复，16 个英文报告和 16 个中文报告都已经包含必要结构信号。

## 英文报告

| 报告 | 必要章节状态 |
|---|---|
| `final/reports/integrated/continual_dyna_model_aging/report.md` | 第一轮修复后 OK |
| `final/reports/integrated/predictive_state_plasticity/report.md` | 第一轮修复后 OK |
| `final/reports/integrated/scale_invariant_continuing_control/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/baird_offpolicy_stability/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/centered_td_diagnostics/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/dyna_planning_budget/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/generate_test_features/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/gvf_predictive_state/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/gvf_question_design/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/nonstationary_bandit/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/onpolicy_stability_atlas/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/options_reusable_subtasks/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/output_controlled_td/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/reward_centered_sarsa/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/streaming_representation/report.md` | 第一轮修复后 OK |
| `final/reports/proposals/tidbd_plasticity/report.md` | 第一轮修复后 OK |

## 中文报告

| 报告 | 必要章节状态 |
|---|---|
| `final/reports/integrated/continual_dyna_model_aging/report_zh.md` | 第一轮修复后 OK |
| `final/reports/integrated/predictive_state_plasticity/report_zh.md` | 第一轮修复后 OK |
| `final/reports/integrated/scale_invariant_continuing_control/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/baird_offpolicy_stability/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/centered_td_diagnostics/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/dyna_planning_budget/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/generate_test_features/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/gvf_predictive_state/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/gvf_question_design/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/nonstationary_bandit/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/onpolicy_stability_atlas/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/options_reusable_subtasks/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/output_controlled_td/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/reward_centered_sarsa/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/streaming_representation/report_zh.md` | 第一轮修复后 OK |
| `final/reports/proposals/tidbd_plasticity/report_zh.md` | 第一轮修复后 OK |

## 这代表什么和不代表什么

第一轮修复解决了真实结构问题：每个报告现在都显式说明 proposal-template answers、独立范围、证据等级、实验设计依据和审稿式批评记录。这样单独打开任意 report 都能更清楚地审阅。

这不代表每个 proposal 一样强。Reward-Centered Sarsa、Output-Controlled TD、Scale-Invariant Continuing Control 和 Continual Dyna Model Aging 仍是最强候选。Predictive State Plasticity 是高价值负向 gate。Dyna Planning Budget 和若干其他 proposal 是 supporting diagnostics。Generate-and-Test、Options、Streaming Representation 和 Nonstationary Bandit 仍是 negative、quarantined 或 dropped，除非后续重设计。

## 验证

- 结构审计：16 个英文和 16 个中文报告都没有缺必要章节信号。
- 图片审计：`final/reports` 下 report 图片链接无断链。
- PDF 导出：16 个英文 `report.pdf` 已重新生成，`missing_images=0`。
