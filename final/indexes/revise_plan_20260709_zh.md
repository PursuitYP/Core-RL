# 2026-07-09 全量 Revise Plan

本文档保存本轮大版本优化计划，方便后续继续执行、审阅和追踪。范围按用户确认执行：覆盖全部 16 个正式研究对象，包括 13 个 ordinary proposal 和 3 个 integrated proposal。每个 Proposal 都作为独立研究课题维护，不用总论文替代，不强行混杂；integrated proposal 继续作为更大、更综合但仍然独立的大 Proposal。

## 当前状态

CPU task `core-rl-output-extended-fixed-46602102` 已经完成，状态为 `Succeeded`。输出目录为 `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`，已经写出 `metrics.csv`、`summary.json`、`condition_summary.json`、`config_used.json`、`manifest.json`。`summary.json` 记录 `elapsed_sec` 约为 `2505`，`n_rows = 2672969`，`n_condition_groups = 80`。这份结果必须从 incomplete/running 状态改为 current evidence，并纳入 Output-Controlled TD 的报告、图表、索引和 PDF。

当前正式材料结构是：`final/reports/proposals/` 下有 13 个 ordinary proposal 报告，`final/reports/integrated/` 下有 3 个 integrated proposal 报告；每个正式报告目录应以 `report.md`、`report_zh.md`、`report.pdf` 为主入口。`final/archive/` 只保留历史碎片和审计材料，不作为当前结论来源。

长 CPU task `core-rl-scale-invariant-extended-33723554` 已成功。它在 `ailab-safethm/safethm_cpu_task` 上运行 `scale_invariant_continuing_control/config_extended.json`，并把标准 artifacts 写到 `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`。该目录现在已经是 evidence，并已纳入 Scale-Invariant report、figures 和 indexes。

## 诚实缺口声明

上一轮实际完成的是一部分基础清理和 Output-Controlled TD extended evidence 的纳入，而不是完成了用户原始需求中的“大幅重构每个 Proposal”。当前仍然存在明显缺口：多数 proposal 的研究动机、研究问题和实验设计仍偏短；很多弱 proposal 只有 5-seed pilot 或 single diagnostic figure；Proposal Template answers 没有在所有报告中以一致结构呈现；中英文虽然成对存在，但并非每一处都逐段完全一致；多角色审查主要在索引层记录，还没有逐个 proposal 形成系统的审查-修订闭环；新的更大综合课题还没有形成完整 proposal/report/实验计划。因此，后续不能把当前状态称为完成，只能称为一个经过初步证据同步和索引修复后的中间状态。

## 原始需求逐条执行矩阵

| 原始需求 | 当前真实状态 | 缺口 | 必须完成的动作 | 验收标准 |
|---|---|---|---|---|
| 0. 每个 Proposal 独立研究全流程 | 目录上已分为 13 个 ordinary + 3 个 integrated，每个有独立 report。 | 许多 report 仍像 mini-report，缺少完整 proposal-template answers、独立实验闭环和独立审查记录。 | 为 16 个 proposal 统一补 `Proposal Template Answers`、`Independent Research Scope`、`Evidence Level`、`Required Next Experiments`、`Reviewer Audit`。 | 单独打开任意 `report.md` 不依赖 overview 就能判断做了什么、为什么做、证据强弱和下一步。 |
| 1. 重构动机、问题、方案、实验和结果分析 | Reward-Centered 和 Output-Controlled 较清楚；Dyna Aging 和 Scale-Invariant 有较强主线；其他多为短报告。 | 许多 proposal 的故事线、研究问题、实验设计和失败分析仍不够论文级。 | 逐个 proposal 做 gap review：保留、补强、降级或 quarantine；为强 proposal 补实验；弱 proposal 写清失败机制和升级条件。 | 每个 report 至少包含明确 hypothesis、environment rationale、baseline rationale、metric rationale、result interpretation、threats。 |
| 2. 组合成更大问题但不拼凑 | 已有三个 integrated proposal。 | Integrated 还没有全部达到“更大但自洽”的论文深度；弱 representation 线尚未被组织成一个 coherent larger topic。 | 保留三个 integrated；新增一个候选大题 `Useful Predictive Knowledge Under Partial Observability and Resource Limits`，把 GVF Predictive State、GVF Question Design、Generate-Test、TIDBD 的共同问题收束为“prediction 何时成为 useful state”。 | 新大题必须有单一研究动机、统一环境族、分阶段实验和明确成功/失败判据，不是把多个旧结果拼接。 |
| 3. 深入 Alberta Plan/Core RL 并提出更综合大问题 | 已有 Alberta Plan lens 和若干文献列表。 | 文献还没有充分进入每个 proposal 的动机和实验设计；新综合问题还没有完整落地。 | 在每个强 proposal 中嵌入相关文献：reward centering、intentional updates、GVF/Horde、Dyna/search-control、emphatic/off-policy、options、average reward。 | 每个 report 的 related work 不只是列文献，而是解释该文献如何改变研究问题或实验设计。 |
| 4. 图表多样且清晰 | 部分图已换成 heatmap/summary figure；Output-Controlled 已有新图。 | 弱 proposal 图仍少，部分结果缺表，图表和结论的对应关系不够强。 | 为每个 proposal 指定 1-3 个主图/表：heatmap、seed-level table、recovery-window plot、mechanism diagnostic plot 或 negative result table。 | 每张图都有明确回答的问题；不使用挤压图例的 spaghetti plot 作为主证据。 |
| 5. 起码十多个角度审阅并完善 | `reviewer_audit` 有总体审查。 | 缺少每个 proposal 的 12-role audit matrix 和修订状态。 | 建立逐 proposal 审查表，角色包括 Alberta Plan、Core RL、average reward、stability、GVF、planning、continual learning、statistics、reproducibility、code、writing、strict instructor。 | 每个 proposal report 或 companion audit 中有“批评-处理-剩余风险”。 |
| 6. 中英文一致，Proposal Template 和 final report 一致 | 所有正式 report 有 `_zh` 和英文 PDF。 | 中英文可能不是逐段一致；许多 report 还没有显式 Proposal Template section。 | 强制每个英文 report 先更新，再同步中文；加入 Proposal Template Answers section。 | 抽查任意 5 个 proposal，中英文同一结论、同一 result path、同一图表、同一限制。 |
| 7. 文档、文件、目录、架构专业清晰 | 目录已比早期清晰；PDF 同目录；代码模块化。 | result dirs 很多，archive 与 final 的边界仍需更清楚；plan/status/overview 容易互相漂移。 | 增加 source-of-truth contract；把 current evidence、running jobs、dropped/quarantined proposal 状态集中维护；减少重复状态文字。 | `final/README.md` 能引导审阅；`results.md` 是唯一 evidence index；`status.md` 是唯一 current status。 |
| 8. 先 plan 模式深入思考 | 已有 plan 文件。 | 计划此前太粗，没有逐条差距和可验收 deliverable。 | 本文件升级为 gap-driven revise plan，并持续更新 execution tracker。 | 计划能直接交给另一个 agent 执行，不需要猜测下一步。 |

## 目标与原则

本轮 revise 的核心目标不是把所有 proposal 写成同样积极的结果，而是把每个 proposal 写成独立、诚实、可复现、可审查的 Core RL 研究记录。强 proposal 要继续补实验和论文深度；弱 proposal 可以独立保留为 negative result、diagnostic、supporting material 或 quarantined topic，但不能用报告语言把证据不足的结果包装成强结论。

所有实验继续遵守项目约束：不使用 replay buffer，不使用 deep network，不做 offline training loop；主要使用 tabular 或 linear function approximation；环境保持 streaming / continual learning 设置。每个报告必须明确回答：研究的 RL 问题是什么、环境为什么能回答这个问题、比较了什么、看什么指标、结果如何限制或支持结论。

## 实施计划

1. Evidence and index cleanup：修正 `experiments/alberta_core_rl/results/README.md` 中重复的 incomplete section；移除所有关于 Output-Controlled TD extended run 仍在运行或不可引用的旧说法；同步更新 `final/indexes/results.md`、`results_zh.md`、`status.md`、`status_zh.md`、`reviewer_audit.md`、`reviewer_audit_zh.md`、`proposal_overview.md`、`proposal_overview_zh.md`。

2. Output-Controlled TD immediate incorporation：从 `20260709T051934Z_extended` 生成新的 report-ready heatmaps 和 seed-level divergence table；更新 `final/reports/proposals/output_controlled_td/report.md`、`report_zh.md` 和同目录 `report.pdf`。报告中必须说明 RuntimeWarning 是高 scale/high alpha 发散条件的 evidence，不是 job failure；并且 true-online TD(lambda) 的负面结果只评价当前 raw-alpha baseline，不作为对算法本身的泛化否定。

3. Per-proposal deep revise：`reward_centered_sarsa` 和 `output_controlled_td` 是最强 ordinary standalone proposal；`scale_invariant_continuing_control` 和 `continual_dyna_model_aging` 是最强 integrated proposal；`predictive_state_plasticity` 是高价值 negative gate，需要重写为 “learned predictions do not automatically become useful state” 的 representation/GVF 研究。`centered_td_diagnostics`、`onpolicy_stability_atlas`、`dyna_planning_budget`、`gvf_question_design`、`baird_offpolicy_stability` 保持独立但定位为 supporting/diagnostic。`nonstationary_bandit`、`streaming_representation`、`options_reusable_subtasks`、`generate_test_features`、`tidbd_plasticity` 需要诚实标注为 weak/negative/quarantined 或待 redesign。

4. Experiment expansion：Reward-Centered Sarsa 补 beta/gamma sweep、midstream reward-origin switch 和 policy-probe stability；Output-Controlled TD 补 true-online audit、max-stable-alpha table 和 no-reset feature-scale switch；Scale-Invariant Control 补 full fixed-condition extended grid 和 gradual unit drift；Dyna Aging 补 stochastic/gradual drift、repeated changes 和 planning utility diagnostics；Predictive State 补 cue decodability、oracle-prediction control、GVF horizon/cumulant ablation；Options 先做 fixed-goal sanity 和 SMDP duration accounting；TIDBD 实现 canonical TIDBD/AutoStep 或明确降级为 TIDBD-lite diagnostic；Generate-Test 将 utility 改成 downstream error/control contribution。

5. Multi-reviewer audit：每个 proposal 至少经 12 个角度审查：Alberta Plan、Core RL theory、average reward、function approximation stability、GVF/predictive knowledge、planning/model-based RL、continual learning、nonstationarity、experimental statistics、reproducibility、code architecture、strict course instructor。每个报告加入“主要批评、已经修订、仍未解决”的明确记录。

6. Documentation and architecture cleanup：保持 final-facing 路径简单；重要文档中英文内容一致；所有正式英文 report 有同目录 PDF；所有 current evidence path 可从 result index 找到；所有代码文件继续保持清晰模块化，避免单文件膨胀。

## 16 个 Proposal 的独立修订矩阵

| Proposal | 当前证据级别 | 主要缺口 | 下一轮实验/分析 | 报告重构要求 |
|---|---|---|---|---|
| Reward-Centered Sarsa | 强；20-seed extended | 缺 beta/gamma sensitivity 和 no-reset reward-origin switch。 | 跑 beta/gamma sweep；同一 stream 中途改变 reward shift；报告 policy probes。 | 增加 Proposal Template Answers；把 reward origin invariance 作为主问题，不只写 reward 更高。 |
| Output-Controlled TD | 强；20-seed extended + fairness audit | true-online output control 仍需要更 principled 的推导；缺 no-reset feature-scale switch。 | max-stable-alpha audit；更严谨 true-online normalization；scale switch without reset。 | 保留 fairness evidence；后续有 switch result 再补。 |
| GVF Predictive State | 负结果/重设计 | GVF question 和 downstream utility 连接弱。 | cue decodability probe；oracle-prediction control；GVF horizon ablation。 | 写成“GVF 不自动成为 useful state”的独立负结果。 |
| Generate-and-Test Features | 负结果/重设计 | utility rule 不优于 random；任务贡献不清楚。 | downstream-error utility；feature budget sweep；delay drift/repeated switch。 | 明确当前失败机制，不把 generate-test 写成正结果。 |
| Doorway Options | quarantine | primitive baseline 和 option accounting 不充分。 | fixed-goal sanity；SMDP duration accounting；goal-change transfer after sanity pass。 | 不通过 sanity 前只保留为暂停课题。 |
| TIDBD Plasticity | 机制诊断 | TIDBD-lite 非 canonical；error 不优于 normalized TD。 | canonical TIDBD/AutoStep；meta-step sensitivity；feature relevance switch。 | 区分 alpha dynamics 可见和 prediction/control gain 不成立。 |
| Baird Off-policy Stability | 支持性稳定性警示 | 需要 canonical Baird audit；缺 emphatic/GTD 对比。 | 核对 feature/policy；加入 ETD/TDC/GTD variants；behavior drift。 | 从“复现 counterexample”升级为 off-policy GVF stability warning。 |
| Dyna Planning Budget | 较强前置诊断；20-seed extended | 与 Dyna Aging 重叠；单独 claim 不够强。 | budget × change severity；pre/post planning utility；stale backup mechanism table。 | 定位为 model-aging 第一实验或独立 precursor，不夸大奖励优势。 |
| Centered TD Diagnostics | 支持性机制 | 环境偏小；单独提交价值低。 | 保留小诊断；可补 analytic shift table。 | 作为 Reward-Centered 的机制附录式独立记录。 |
| On-policy Stability Atlas | 支持性 atlas | 没有 intervention。 | 增加 max-stable-alpha map；与 Output-Controlled TD 统一指标。 | 明确它解释为什么 normalized update 必要。 |
| GVF Question Design | 支持性/重设计工具 | 只看 prediction error，不看 useful state。 | cue information、decodability、control ablation。 | 写清“easy to predict != useful to control”。 |
| Nonstationary Bandit | dropped sanity | 太浅，没有 bootstrapping/state/planning。 | 不扩为主线；只作 intro sanity。 | 报告降级，避免冒充 Core RL 主课题。 |
| Streaming Representation | 负结果 | auxiliary target 不 task-relevant。 | 设计 task-relevant auxiliary；feature utility analysis。 | 合并到 predictive-state program 或保留负结果。 |
| Scale-Invariant Continuing Control | 强 integrated；fixed grid + unit-switch 已完成 | abrupt unit switch recovery 仍弱。 | 补 gradual unit drift、recovery AUC 和 policy-distance probes。 | 写成 reward-unit 和 feature-unit invariance 的单一大问题。 |
| Continual Dyna Model Aging | 强 integrated；20-seed extended | abrupt deterministic change 过窄。 | stochastic/gradual drift；repeated changes；planning utility diagnostics。 | 把 claim 聚焦 stale-backup reduction/search-control freshness。 |
| Predictive State Plasticity | 高价值负向 gate；20-seed extended | 题目大于当前成功证据。 | cue decodability；redesigned GVFs；limited feature budget; optional generate-test/TIDBD only after probe passes。 | 重写成 staged negative-to-redesign research program。 |

## 新综合大题候选

新增候选：`Useful Predictive Knowledge Under Partial Observability and Resource Limits`。这个题目不替代 16 个当前报告，而是作为一个后续 integrated proposal 候选，用来满足“突破现有框架但不拼凑”的要求。核心问题是：在部分可观测的 continuing/episodic stream 中，哪些 learned predictions 真正能成为 agent state，而不仅是低 TD-error 的 auxiliary quantities？

统一环境族：T-maze cue stream + delayed-cue trace-conditioning stream。统一研究对象：隐藏 cue 信息如何被 GVF、trace features、utility-selected features 或 per-feature step-size adaptation 保留到 control-relevant time。统一指标：cue decodability、junction action accuracy、trial reward、feature budget usage、prediction TD error、post-switch recovery。分阶段实验：先做 oracle/trace/GVF decodability gate；通过后再做 generate-test feature selection；最后再接 TIDBD/AutoStep plasticity。失败判据同样重要：如果 prediction error 降低但 decodability/control 不提高，则结论是 prediction accuracy 不足以定义 useful state。

## 执行追踪

| 工作项 | 状态 | 证据或阻塞 | 下一步 |
|---|---|---|---|
| 保存本轮 revise plan 的中英文版本 | 已完成 | `final/indexes/revise_plan_20260709.md`、`final/indexes/revise_plan_20260709_zh.md` | 保持“原始用户需求”作为最后一个 section。 |
| 修正误导性的 requirements/status 文档 | 第一轮已完成 | `final/indexes/requirements_audit.md`、`final/indexes/status.md` 及中文版本已改成 gap-tracking 口径。 | 后续每次实验和报告更新后继续同步。 |
| 审计报告缺失章节 | 第一轮机械检查已完成 | `final/indexes/report_section_audit.md` 和 `_zh.md` 显示多数报告缺显式 Proposal Template、独立范围、证据等级、实验设计或审查信号。 | 用该审计作为 report rewrite checklist；修订后重新检查。 |
| 监控 Scale-Invariant extended CPU task | 已完成 | `core-rl-scale-invariant-extended-33723554` 已成功；`20260709T063128Z_extended` 包含标准 artifacts 并已纳入报告和索引。 | 继续做 gradual drift 和 recovery diagnostics。 |
| 清理 `__pycache__` | 受权限阻塞 | `experiments/alberta_core_rl/` 下两个 `__pycache__` 目录由 `nobody:nogroup` 拥有，普通用户删除会 permission denied。 | 除非用户允许特权清理，否则只记录该问题。 |
| 给所有报告补 Proposal Template Answers | 第一轮结构修复已完成 | 16 个英文报告和 16 个中文报告都已有显式 Proposal Template、独立范围、证据等级、实验设计依据和审查章节。 | 继续提升内容深度，并保持中英文 claim 同步。 |
| 给每个 proposal 补 critique/action/risk 表 | 第一轮简洁版已完成 | 每个正式报告都有 reviewer-audit style 表或矩阵。 | 只在能改变研究决策时继续扩展，避免泛泛填充。 |
| 深化强 proposal 的实验 | 部分完成 | Output-Controlled extended evidence 已纳入；Reward-Centered、Dyna、Predictive State 有 extended evidence；但多个 follow-up sweep 未完成。 | 优先做能改变结论的 targeted sweeps，而不是盲目扩大 grid。 |
| 新的 predictive-knowledge 大题 | 仅计划 | 上文已定义候选问题、环境族和 staged gates；当前 Predictive State Plasticity 仍是 negative gate，不等于完整新大题。 | 先写 report skeleton、gate experiments 和验收标准，再实现。 |

## 新调研资料与作用

- Alberta Plan for AI Research, Sutton/Bowling/Pilarski, arXiv:2208.11173, https://arxiv.org/abs/2208.11173。本项目的主框架来源：ordinary experience、temporal uniformity、continual learning、value functions、learned models、planning、GVFs、average reward。
- Intentional Updates for Streaming Reinforcement Learning, Sharifnassab/Elsayed/De Asis/Mahmood/Sutton, arXiv:2604.19033, https://arxiv.org/abs/2604.19033。直接支撑 Output-Controlled TD 和 Scale-Invariant Control：step size 不应只表示 parameter displacement，而应表示 intended output change。
- Squeezing More from the Stream: Learning Representation Online for Streaming Reinforcement Learning, arXiv:2602.09396, https://arxiv.org/abs/2602.09396。支撑 representation/GVF/auxiliary prediction 方向：streaming agent 丢弃每个 transition 后必须从单次经验中挤出更多 representation signal，但 auxiliary objective 需要处理 streaming instability 和 utility。
- Streaming Deep Reinforcement Learning Finally Works, Elsayed/Vasan/Mahmood, arXiv:2410.14606, https://arxiv.org/abs/2410.14606。提供 streaming RL 背景和 “stream barrier” 论述；本项目不使用 deep network，但可以借用其问题定义来解释为什么无 replay、batch-size-one 是核心约束。
- Reward Centering, Naik/Wan/Tomar/Sutton, arXiv:2405.09999, https://arxiv.org/abs/2405.09999。直接支撑 Reward-Centered Sarsa 和 Scale-Invariant Control：continuing discounted methods 在 reward shift 下会退化，reward centering 应降低对 reward origin 的敏感性。
- True Online Temporal-Difference Learning, van Seijen/Mahmood/Pilarski/Machado/Sutton, arXiv:1512.04087, https://arxiv.org/abs/1512.04087；以及 An Empirical Evaluation of True Online TD(lambda), arXiv:1507.00353, https://arxiv.org/abs/1507.00353。支撑 Output-Controlled TD 的 trace baseline，但也提醒报告不能把当前 raw-alpha true-online baseline 的发散泛化为算法本身缺陷。
- Dyna-Style Planning with Linear Function Approximation and Prioritized Sweeping, Sutton/Szepesvari/Geramifard/Bowling, arXiv:1206.3285, https://arxiv.org/abs/1206.3285。支撑 Dyna Planning Budget 和 Continual Dyna Model Aging：online setting 下 model-based planning 和 search-control 是核心问题。
- Frequency-based Search-control in Dyna, Pan/Mei/Farahmand, arXiv:2002.05822, https://arxiv.org/abs/2002.05822。支撑 Dyna aging 的 search-control framing：planning 效果取决于从哪里采样 model queries，而不只是 planning backups 数量。
- Almost Sure Convergence of Differential Temporal Difference Learning for Average Reward Markov Decision Processes, Blaser/Wang/Zhang, arXiv:2602.16629, https://arxiv.org/abs/2602.16629。支撑 average-reward/differential TD 方向，用于完善 Reward-Centered 和 continuing-control 报告的理论背景。

这些资料需要在后续报告中按 proposal 选择性引用，不要简单堆 bibliography。每个引用都应该服务一个具体研究动机或实验设计选择。

## 验证计划

- `python -m compileall experiments/alberta_core_rl`
- `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py`
- 检查所有 current result dirs 含 `metrics.csv`、`summary.json`、`condition_summary.json`、`config_used.json`、`manifest.json`。
- 检查所有 report 图片链接存在。
- 检查每个英文 `report.md` 有对应 `report_zh.md` 和同目录 `report.pdf`。
- 运行 PDF 导出脚本后确认 missing images 为 0，并清理 `__pycache__`。

## 原始用户需求（按要求附在最后）

最后这个 cpu job 继续等待，同时这次引入一个新的 revise 计划，请以下面这个新的需求为主进行大幅优化，同时记录上面那个 cpu task 的进度，最后要汇总到这个新的需求中。

现在深入理解初始需求和当前每个 Proposal 的内容、实现和报告，尝试大幅重构每个 Proposal：

0. 每个 Proposal 都是独立的分开的研究，不要混杂起来，也不要强行联系，每个 Proposal 独立研究全流程。
1. 优化完善重构现有每个 Proposal 的研究动机、研究问题、研究方案、实验设计、结果分析等等的内容，看看是不是有些没意义或者太 toy example，或者现在的实验和分析内容不够，考虑深度优化每个 Proposal 大补实验。
2. 组合成更大的问题，深入理解现有的材料以及拟定的 Proposal，分析是否过于零散，尝试结合初始方向和现有课题，将一个课题组合起来从而研究一个更大的更有意义的大课题，但是要继续保持其合理性，需要详细研究细节。
3. 尝试更深入理解 Alberta Plan - Core RL 研究议题，结合已有的 Proposal，深入分析，突破现有框架和课题限制，从而提出一个更综合的更大问题的 Proposal，但是要求具体研究内容不是拼凑，要求研究动机明确、研究问题合理、研究脉络清晰，实验设计紧扣研究动机和问题，设计多个重要研究问题，实验数量规模分析都多一点。
4. 实验结果的呈现效果可以多样一些，比如各种样式的图表，但是要求丰富而不是花哨，图表不要主次不分，要清晰。
5. 其他各项内容，方方面面，都再深入细致地审查，设置多个不同的角色（起码十多个角度）进行审阅，然后完善。
6. 文档的中英文版要求是完全一致的内容并且清晰专业，Proposal Template 和 final report 应该一致。
7. 完善优化所有的文档、文件、目录和整个的项目架构和结构，使其更专业更清晰更好读，可以方便后续持续优化。
8. 请先进入 plan 模式进行深入的思考、分析、设计和完善。
