# 原始需求覆盖审计（中文）

日期：2026-07-09

这份审计现在采用保守口径：它记录原始需求目前覆盖到哪里、证据在哪里、还缺什么；它不再把“有文件”直接写成“已完成”。当前大版本修订的 source of truth 是 `final/indexes/revise_plan_20260709_zh.md`；本文件用于快速检查需求覆盖和剩余缺口。

## 覆盖概览

| 需求 | 当前状态 | 主要材料 | 剩余缺口 |
|---|---|---|---|
| 阅读课程/project 原始资料和 Alberta Plan 材料 | 已覆盖，但仍需更深入进入每个 proposal | `AGENTS.md`、`resources/alberta_plan_related/README.md`、`draft/iterative_research_record.md` | 很多报告仍只是总体使用 Alberta Plan 视角，需要在每个强 proposal 中解释资料如何改变研究问题和实验设计。 |
| 重点实现 Reward-Centered Sarsa 和 Output-Controlled TD | 已覆盖，并已有实现、报告、图表和 extended evidence | `final/reports/proposals/reward_centered_sarsa/`、`final/reports/proposals/output_controlled_td/` | Reward-Centered 仍需 beta/gamma sweep 和 no-reset reward-origin switch；Output-Controlled 仍需 true-online 公平审计和 no-reset feature-scale switch。 |
| 分析其他 proposal 并设计新角度 | 部分覆盖 | `final/reports/proposals/`、`final/reports/integrated/` | 多个 proposal 仍是 diagnostic 或 negative，需要在报告中明确它们是可提交主线、支持材料、redesign target 还是 quarantine。 |
| 搜索 Alberta Plan 后续工作和相关文献 | 已覆盖且继续进行 | `resources/alberta_plan_related/README.md`、`final/indexes/revise_plan_20260709_zh.md` | 新文献还需要写进各个 proposal 的 related work、motivation 和实验选择，而不是只停留在索引文档。 |
| 每个 proposal 完成 Proposal Template 问题 | 第一轮结构覆盖 | `final/reports/**/report.md`、`final/reports/**/report_zh.md`、`final/indexes/report_section_audit_zh.md` | 所有 report 现在都有显式章节；下一步缺口是内容深度、中英文一致性和实验跟进。 |
| 至少五个课程/资料推荐 proposal | 结构上已覆盖 | reward centering、output control、GVF state、generate-and-test、options | 其中一些 proposal 证据弱或已 quarantine，不能当成同等成熟的主研究。 |
| 至少五个自设计或扩展 proposal | 结构上已覆盖 | TIDBD、Baird、Dyna、centered TD、on-policy atlas、GVF question design、streaming representation、integrated proposals | 多个自设计 proposal 需要补实验，或者诚实降级为诊断/负结果材料。 |
| 新的更大 integrated Core RL proposal | 部分覆盖 | `final/reports/integrated/` | 三个 integrated report 已存在，但新的 `Useful Predictive Knowledge Under Partial Observability and Resource Limits` 仍只是计划候选，还没有完整 report 和实验包。 |
| 不使用 replay buffer、不使用 deep network | 已覆盖 | `experiments/alberta_core_rl/`、`final/indexes/reproduction.md` | 后续新增实验仍要持续检查这个约束。 |
| 主实验不能只是 toy example | 部分覆盖 | access-control、tile random walk、changing gridworld、T-maze streams | 一些弱 proposal 仍偏 toy，需要升级环境或明确降级。 |
| 持续多轮审查和批评者机制 | 部分覆盖 | `final/indexes/reviewer_audit_zh.md`、`draft/critique_round_9_independent_study_gap_matrix.md` | 当前审查主要是全局审查；新计划要求每个 proposal 有 12-role critique/action/risk 表。 |
| 专业项目结构和独立环境 | 部分覆盖 | `conda-env-configs/README.md`、`experiments/alberta_core_rl/studies/`、`final/README.md` | 结构已明显改善，但 status/index 文件还要更严格保持 source-of-truth；两个 `__pycache__` 目录由 `nobody:nogroup` 拥有，普通用户无法删除。 |
| 每个 proposal 独立 | 第一轮结构覆盖 | `final/reports/proposals/`、`final/reports/integrated/` | 每个 report 已写独立范围和证据等级；强报告仍需补深实验，弱报告仍需继续诚实保持 negative/quarantine framing。 |
| 报告包含图表 | 强报告已覆盖，整体仍是部分覆盖 | `final/reports/**/figures/`、report PDFs | 一些 supporting/negative 报告仍需要更清晰的主表或机制图，并且每个图表要对应明确研究问题。 |
| 当前 CPU task 追踪 | 状态层面已覆盖 | `final/indexes/status_zh.md`、`final/indexes/revise_plan_20260709_zh.md` | Scale-Invariant 和 Output-Fairness extended jobs 已成功并作为 evidence；Reward-Sensitivity 和 Dyna-Drift reruns 仍在运行，在标准 artifacts 写出前不是 evidence。 |

## 当前交付结构

- 正式 proposal 索引：`final/reports/proposals/README.md`
- 正式英文 proposal 报告：`final/reports/proposals/<proposal>/report.md`
- 正式中文 proposal 报告：`final/reports/proposals/<proposal>/report_zh.md`
- 历史 proposal fragments：`final/archive/proposal_fragments/<proposal>/`
- integrated reports：`final/reports/integrated/`
- 当前结果索引：`final/indexes/results.md`
- 复现说明：`final/indexes/reproduction.md`
- 当前大修计划：`final/indexes/revise_plan_20260709_zh.md`
- 迭代研究记录：`draft/iterative_research_record.md`

## 最高优先级剩余工作

1. 给 16 个当前报告补显式 Proposal Template Answers、独立研究范围、证据等级、下一步实验和 reviewer-audit sections。
2. 对强 proposal 补针对性实验，而不是只润色文字。
3. 对弱 proposal 诚实写成 negative、diagnostic 或 quarantined，并给出失败机制和升级条件。
4. 让英文和中文报告做到内容一致，而不是只有文件名成对。
5. 把当前调研文献写进各 proposal 的 motivation、related work 和实验设计。
6. 继续监控 `core-rl-scale-invariant-extended-33723554`，只有等 `metrics.csv`、`summary.json`、`condition_summary.json`、`config_used.json`、`manifest.json` 都出现后才能纳入 evidence。
