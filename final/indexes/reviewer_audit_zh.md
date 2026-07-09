# 审查记录与改进行动

本文档记录当前 Core-RL 项目的多角色审查循环。它不替代各 proposal 的正式报告，而是追踪哪些问题被指出、哪些已经处理、哪些还需要继续改。

## 审查轮次：2026-07-09

### 严格 Core-RL 审稿人

主要批评：最强几个报告仍然主要基于 5 seeds、5000 steps 的 pilot evidence，但部分结论使用了比证据更强的措辞。审稿人建议在 extended sweep 完成前，把当前结果明确降级为 pilot evidence。

处理状态：已经启动 `reward_centered_sarsa`、`output_controlled_td`、`predictive_state_plasticity`、`continual_dyna_model_aging`、`dyna_planning_budget` 和 `unit_switching_continuing_control` 的 extended runs。Reward-Centered Sarsa、Dyna Planning Budget、Continual Dyna Model Aging、Predictive State Plasticity 和 Unit-Switching Continuing Control 的 extended evidence 已纳入报告或索引；Output-Controlled TD 现在通过已验证的 CPU task 通道运行，任务名为 `core-rl-output-extended-fixed-46602102`。

主要批评：`scale_invariant_continuing_control` 不能只做固定条件之间的 cross-run invariance，还需要同一条 stream 中途改变 reward/feature units 的 no-reset 实验。

处理状态：已经新增 `unit_switching_continuing_control` runner。该实验在 continuing access-control stream 中途改变 reward origin 和/或 feature scale，不重置 weights。smoke config 和 extended config 均已完成，结果已纳入 Scale-Invariant Continuing Control 报告。

主要批评：`continual_dyna_model_aging` 目前更强的证据是 stale-backup reduction，而不是 reward superiority；除非 reward recovery 在 extended run 中很稳健，否则不要夸大 reward claim。

处理状态：后续报告会把 Dyna 证据重点放在 stale planning diagnostics 和 recovery windows。已完成的 `dyna_planning_budget` extended run 显示，即使 late reward 后续恢复，keep-model planning 仍会保留明显 stale backups。

主要批评：`predictive_state_plasticity` 当前应作为有价值的 negative/redesign gate，而不是正向最终候选。

处理状态：后续报告会保持这个定位。extended run 增加 maze length `30`，但评价标准仍然是 learned predictive state 是否接近或超过 trace/oracle memory，而不是只看 cue alignment 是否非零。

### 复现与报告质量审查者

主要批评：中文 `report_zh.md` 只是短的快速审阅笔记，不是英文报告的真正对应版本，并且缺少图表。

处理状态：所有 `final/reports/**/report_zh.md` 都已经从快速摘要扩展为可单独审阅的中文报告，包含研究动机、RL setting、方法、实验设计、结果、解释、局限、审稿式批评回应、可用图表和复现命令。强主线报告有更完整的中文对应版本；支持性和负结果 proposal 也以诚实的独立研究记录呈现，而不是模板化摘要。

主要批评：`proposal_overview.md` 比 `proposal_overview_zh.md` 简短太多。

处理状态：已经在两个 overview 文件中加入专门的 RL environment catalogue，解释每个环境的 state/observation、actions、reward/nonstationarity 和研究用途。

主要批评：integrated reports 展示了 report-ready figures，但 reproduction section 没有写出 `plot_report_figures.py` 的图表再生成命令。

处理状态：已经在更新后的 integrated 报告和复现索引中加入图表再生成命令。`dyna_planning_budget` 也基于 20-seed extended run 生成了更可读的 average-reward 和 stale-backup 图。

主要批评：`config_extended.json` 使用 `suite: main`，导致输出目录仍为 `_main`，容易和 pilot 混淆。

处理状态：`run_proposal` 已改为对来自 `config_extended.json` 的运行使用 `_extended` 输出后缀，同时保留 `suite: main` 给 runner 逻辑使用。补丁前已启动的旧进程会在完成后核对并重命名。

### 最新多角色复审跟进

主要批评：Output-Controlled TD 的 extended 状态在中英文报告和索引中容易被误读，磁盘上存在 `20260709T051934Z_extended`，但该目录目前仍不完整。

处理状态：Output-Controlled TD 报告和索引已经统一写成：当前可引用 evidence 仍是 `20260708T153802Z_main`；CPU task `core-rl-output-extended-fixed-46602102` 正在运行；`20260709T051934Z_extended` 在标准 artifacts 写出前不能引用。

主要批评：Dyna aging 的报告图静默丢掉了 `half_life` 维度。

处理状态：已拆分 `plot_report_figures.py`，并重新生成 Dyna aging 报告图；图例现在显式区分 aging half-life，图注也写明按 planning budget、model mode 和 half-life 展示。

主要批评：多个报告仍使用过载 learning-curve 图，图例挤压主图，不能支撑最终报告结论。

处理状态：已为 Output-Controlled TD、Reward-Centered Sarsa、On-policy Stability Atlas、Dyna Planning Budget、Unit-Switching Continuing Control、Scale-Invariant Continuing Control、Dyna Aging 和 Predictive State Plasticity 生成 report-ready summary figures 或 heatmaps，并替换正式报告引用。

主要批评：Predictive State Plasticity 题目大于当前证据。

处理状态：报告已明确当前可提交证据是 20-seed first-gate negative result；generate-and-test、TIDBD 和 feature replacement 是后续 staged program，不是当前已经完成的正向证据。

主要批评：不完整结果目录可能被误当作 evidence。

处理状态：`experiments/alberta_core_rl/results/README.md` 已列出已知 incomplete directories；可写的旧目录加入 `INCOMPLETE.md` marker。当前 Output extended 目录由 rjob 容器用户创建，因此只在 README 和索引中标明 incomplete/running。

## 当前待办

- 等待仍在运行的 CPU-task extended job 完成：`output_controlled_td/config_extended.json`。目标结果目录是 `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`；完成后需要核对 `config_used.json`、`condition_summary.json` 和 figures，再写入报告。
- 对 `scale_invariant_continuing_control/config_extended.json` 决定运行范围；这是最大的 fixed-condition sweep，应在当前任务完成后再安排，或迁移到已验证可用的 CPU-task 队列。
- `output_controlled_td` extended summary 可用后，更新对应结果索引和报告；当前报告已经标明 extended 目录仍不完整。
- 如果 `reward_centered_sarsa` 被选为最终独立题目，需要补 beta/gamma sweep 和 midstream reward-origin switch。
- Dyna aging 在做一般化结论前，需要加入 gradual/stochastic drift environments。
- 在把 true-online TD(lambda) 作为强负 baseline 前，需要补 max-stable-alpha audit。
- 在尝试把 GVF predictive-state 写成正结果前，需要补 cue-decodability 和 downstream-control ablations。

## 本轮验证记录

- `final/` 下所有 Markdown 图片链接检查通过。
- `python -m compileall experiments/alberta_core_rl` 已完成且无报错。
- 编译检查生成的 `__pycache__` 目录已清理。
- 拆分 report plotting utilities 后，Python 源文件仍满足每个文件低于 500 行的维护建议；当前最大文件是 `envs.py`，474 行。
