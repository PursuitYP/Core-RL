# 审查记录与改进行动

本文档记录当前 Core-RL 项目的多角色审查循环。它不替代各 proposal 的正式报告，而是追踪哪些问题被指出、哪些已经处理、哪些还需要继续改。

## 审查轮次：2026-07-09

### 严格 Core-RL 审稿人

主要批评：最强几个报告仍然主要基于 5 seeds、5000 steps 的 pilot evidence，但部分结论使用了比证据更强的措辞。审稿人建议在 extended sweep 完成前，把当前结果明确降级为 pilot evidence。

处理状态：已经启动 `reward_centered_sarsa`、`output_controlled_td`、`predictive_state_plasticity`、`continual_dyna_model_aging`、`dyna_planning_budget` 和 `unit_switching_continuing_control` 的 extended runs。Reward-Centered Sarsa、Output-Controlled TD、Dyna Planning Budget、Continual Dyna Model Aging、Predictive State Plasticity 和 Unit-Switching Continuing Control 的 extended evidence 已纳入报告或索引；Output-Controlled TD 的 CPU task `core-rl-output-extended-fixed-46602102` 已成功完成。

主要批评：`scale_invariant_continuing_control` 不能只做固定条件之间的 cross-run invariance，还需要同一条 stream 中途改变 reward/feature units 的 no-reset 实验。

处理状态：已经新增 `unit_switching_continuing_control` runner。该实验在 continuing access-control stream 中途改变 reward origin 和/或 feature scale，不重置 weights。smoke config 和 extended config 均已完成，结果已纳入 Scale-Invariant Continuing Control 报告。

主要批评：`continual_dyna_model_aging` 目前更强的证据是 stale-backup reduction，而不是 reward superiority；除非 reward recovery 在 extended run 中很稳健，否则不要夸大 reward claim。

处理状态：后续报告会把 Dyna 证据重点放在 stale planning diagnostics 和 recovery windows。已完成的 `dyna_planning_budget` extended run 显示，即使 late reward 后续恢复，keep-model planning 仍会保留明显 stale backups。

主要批评：`predictive_state_plasticity` 当前应作为有价值的 negative/redesign gate，而不是正向最终候选。

处理状态：后续报告会保持这个定位。extended run 增加 maze length `30`，但评价标准仍然是 learned predictive state 是否接近或超过 trace/oracle memory，而不是只看 cue alignment 是否非零。

### 复现与报告质量审查者

主要批评：中文 `report_zh.md` 一开始只是短的快速审阅笔记，不是英文报告的真正对应版本；即使扩展后，仍有若干报告需要更严格的中英文内容一致性检查。

处理状态：中文报告已经从快速摘要显著扩展，许多报告包含研究动机、RL setting、方法、实验设计、结果、解释、局限、审稿式批评回应、可用图表和复现命令。但这还不是完成的 consistency guarantee：下一轮必须逐个检查中英文报告的 result path、claim、limitations、figures 和 Proposal Template answers 是否一致。

主要批评：`proposal_overview.md` 比 `proposal_overview_zh.md` 简短太多。

处理状态：已经在两个 overview 文件中加入专门的 RL environment catalogue，解释每个环境的 state/observation、actions、reward/nonstationarity 和研究用途。

主要批评：integrated reports 展示了 report-ready figures，但 reproduction section 没有写出 `plot_report_figures.py` 的图表再生成命令。

处理状态：已经在更新后的 integrated 报告和复现索引中加入图表再生成命令。`dyna_planning_budget` 也基于 20-seed extended run 生成了更可读的 average-reward 和 stale-backup 图。

主要批评：`config_extended.json` 使用 `suite: main`，导致输出目录仍为 `_main`，容易和 pilot 混淆。

处理状态：`run_proposal` 已改为对来自 `config_extended.json` 的运行使用 `_extended` 输出后缀，同时保留 `suite: main` 给 runner 逻辑使用。补丁前已启动的旧进程会在完成后核对并重命名。

### 最新多角色复审跟进

主要批评：Output-Controlled TD 的 extended 状态在中英文报告和索引中容易被误读；此前磁盘上存在 `20260709T051934Z_extended`，但当时目录仍不完整。

处理状态：CPU task `core-rl-output-extended-fixed-46602102` 已成功完成，`20260709T051934Z_extended` 已包含标准 artifacts。Output-Controlled TD 的中英文报告、结果索引、复现说明和图表已更新为使用 extended evidence；divergence 现在按 seed-level event rate 汇总。

主要批评：Dyna aging 的报告图静默丢掉了 `half_life` 维度。

处理状态：已拆分 `plot_report_figures.py`，并重新生成 Dyna aging 报告图；图例现在显式区分 aging half-life，图注也写明按 planning budget、model mode 和 half-life 展示。

主要批评：多个报告仍使用过载 learning-curve 图，图例挤压主图，不能支撑最终报告结论。

处理状态：已为 Output-Controlled TD、Reward-Centered Sarsa、On-policy Stability Atlas、Dyna Planning Budget、Unit-Switching Continuing Control、Scale-Invariant Continuing Control、Dyna Aging、Predictive State Plasticity 和 Useful Predictive Knowledge 生成 report-ready summary figures 或 heatmaps，并替换正式报告引用。

主要批评：Predictive State Plasticity 题目大于当前证据。

处理状态：报告已明确当前可提交证据是 20-seed first-gate negative result；generate-and-test、TIDBD 和 feature replacement 是后续 staged program，不是当前已经完成的正向证据。

主要批评：不完整结果目录可能被误当作 evidence。

处理状态：`experiments/alberta_core_rl/results/README.md` 已把 known incomplete directories 和 current extended evidence 分开列出。完成的 Output extended 目录由 rjob 容器用户创建，因此数据作为 evidence 保留，report-ready figures 存放在 report 目录下。

主要批评：用户明确要求逐条核验原始需求后，`requirements_audit` 和 `status` 文档仍有过度完成表述。

处理状态：`final/indexes/requirements_audit_zh.md` 和 `final/indexes/status_zh.md` 已改成保守的 gap-tracking 口径。现在会区分“结构上覆盖”和“研究深度完成”，并诚实记录弱/暂停 proposal 的真实状态。后续 CPU 任务完成后，Scale-Invariant、Reward Sensitivity、Output Fairness 和 Dyna Drift 都已从 running/status 记录升级为 completed evidence。

主要批评：即使索引修正后，正式报告本体仍缺显式 Proposal Template answers、独立研究范围、证据等级、实验设计依据和逐 proposal 审查记录。

处理状态：17 个英文报告和 17 个中文报告现在都已经包含必要结构章节。强 proposal 按强证据但仍需补实验处理；弱 proposal 明确写成 supporting、negative、dropped 或 quarantined。结构审计记录在 `final/indexes/report_section_audit_zh.md`。

### 并行独立性与过度 claim 审查

主要批评：只读并行审查没有发现严重的跨报告依赖，但发现几个剩余 overclaim 风险。`GVF Predictive State` 在缺少 direct cue-decodability probe 的情况下，说 learned GVF 没有携带 cue information，证据只能支持“没有成为 usable control state”。`Nonstationary Bandit` 在只有五个 seeds 且置信区间很宽时使用了“确认”语言。`Reward-Centered Sarsa` 和 `Scale-Invariant Continuing Control` 的 “necessary” 表述听起来超过了当前 access-control grids 能证明的范围。`Predictive State Plasticity` 仍多次提到 limited-budget replacement 和 feature-wise plasticity，可能被误读成当前 evidence，而不是 future work。

处理状态：相关英文和中文报告已修订。`GVF Predictive State` 现在写成 recurrent GVF 没有成为 usable control state，并明确 direct cue information 在该 pilot 中尚未测量。`Nonstationary Bandit` 改用“提示”和 “sanity-check observation” 口径。`Reward-Centered Sarsa` 与 `Scale-Invariant Continuing Control` 把最强表述限制在 tested access-control variants 和 combinations 中。`Predictive State Plasticity` 明确 limited-budget replacement、generated traces 和 feature-wise step-size adaptation 是 future-work mechanisms，不是当前 fixed predictive-state gate 的证据。

## 当前待办

- 继续深化刚补上的 Proposal Template、证据等级和 reviewer sections；第一轮结构修复已经完成，但不是每个报告都已经 paper-perfect。
- 继续 Output-Controlled TD follow-up：在已完成 fairness audit 和 max-stable-alpha frontier 后，补更 principled 的 true-online TD(lambda) output-control derivation，以及 no-reset feature-scale switch 实验。
- 继续 Scale-Invariant follow-up：在已完成 fixed-condition grid 后，补 gradual unit drift、recovery AUC 和 policy-distance probes。
- Reward-Centered 已完成 beta/gamma/no-reset switch 和 early recovery score；下一步应补 matched-seed recovery analysis、policy-distance probes 和 natural reward drift。
- Dyna aging 已完成 abrupt/gradual/stochastic drift sweep 和 reward/staleness frontier；下一步应补 repeated changes 和 true per-backup planning-utility logging。
- 在把 true-online TD(lambda) 作为强负 baseline 前，需要补 max-stable-alpha audit。
- Useful Predictive Knowledge 在已完成 feature-budget gate 之后，下一步应补 oracle-prediction scaling、GVF-output normalization、prediction-to-policy coupling、downstream-control ablations 和后续 plasticity stages，然后才能尝试正向 predictive-state claim。

## 本轮验证记录

- `final/` 下所有 Markdown 图片链接检查通过。
- 本轮修复后 `final/reports/**/report*.md` 图片检查通过，缺失图片为 0。
- 本轮修改后 17 个英文 `report.pdf` 都已重新导出；`final/indexes/english_report_pdf_manifest.json` 记录每个 report 的 `missing_images=0`。
- `python -m compileall experiments/alberta_core_rl` 已完成且无报错。
- 编译检查生成的 `__pycache__` 没有完全清理：`experiments/alberta_core_rl/` 下两个目录由 `nobody:nogroup` 拥有，普通用户删除时会 permission denied。
- 拆分 report plotting utilities 后，Python 源文件仍满足每个文件低于 500 行的维护建议；当前最大文件是 `envs.py`，474 行。
