# 审查记录与改进行动

本文档记录当前 Core-RL 项目的多角色审查循环。它不替代各 proposal 的正式报告，而是追踪哪些问题被指出、哪些已经处理、哪些还需要继续改。

## 审查轮次：2026-07-09

### 严格 Core-RL 审稿人

主要批评：最强几个报告仍然主要基于 5 seeds、5000 steps 的 pilot evidence，但部分结论使用了比证据更强的措辞。审稿人建议在 extended sweep 完成前，把当前结果明确降级为 pilot evidence。

处理状态：已经启动 `reward_centered_sarsa`、`output_controlled_td`、`predictive_state_plasticity`、`continual_dyna_model_aging`、`dyna_planning_budget` 和 `unit_switching_continuing_control` 的本地 extended runs。`dyna_planning_budget` 最先完成，核对来自 `config_extended.json` 后已把输出目录重命名为 `_extended`。

主要批评：`scale_invariant_continuing_control` 不能只做固定条件之间的 cross-run invariance，还需要同一条 stream 中途改变 reward/feature units 的 no-reset 实验。

处理状态：已经新增 `unit_switching_continuing_control` runner。该实验在 continuing access-control stream 中途改变 reward origin 和/或 feature scale，不重置 weights。smoke config 已通过，extended config 正在运行。

主要批评：`continual_dyna_model_aging` 目前更强的证据是 stale-backup reduction，而不是 reward superiority；除非 reward recovery 在 extended run 中很稳健，否则不要夸大 reward claim。

处理状态：后续报告会把 Dyna 证据重点放在 stale planning diagnostics 和 recovery windows。已完成的 `dyna_planning_budget` extended run 显示，即使 late reward 后续恢复，keep-model planning 仍会保留明显 stale backups。

主要批评：`predictive_state_plasticity` 当前应作为有价值的 negative/redesign gate，而不是正向最终候选。

处理状态：后续报告会保持这个定位。extended run 增加 maze length `30`，但评价标准仍然是 learned predictive state 是否接近或超过 trace/oracle memory，而不是只看 cue alignment 是否非零。

### 复现与报告质量审查者

主要批评：中文 `report_zh.md` 只是短的快速审阅笔记，不是英文报告的真正对应版本，并且缺少图表。

待处理：扩展正式中文报告，使其对应英文报告结构，包括研究动机、环境、方法、实验设计、结果、局限、批评回应、图表和复现命令。

主要批评：`proposal_overview.md` 比 `proposal_overview_zh.md` 简短太多。

处理状态：已经在两个 overview 文件中加入专门的 RL environment catalogue，解释每个环境的 state/observation、actions、reward/nonstationarity 和研究用途。

主要批评：integrated reports 展示了 report-ready figures，但 reproduction section 没有写出 `plot_report_figures.py` 的图表再生成命令。

待处理：在 integrated 英文报告和中文对应报告中加入图表再生成命令。

主要批评：`config_extended.json` 使用 `suite: main`，导致输出目录仍为 `_main`，容易和 pilot 混淆。

处理状态：`run_proposal` 已改为对来自 `config_extended.json` 的运行使用 `_extended` 输出后缀，同时保留 `suite: main` 给 runner 逻辑使用。补丁前已启动的旧进程会在完成后核对并重命名。

## 当前待办

- 等待所有已启动 extended runs 完成，并抽取 seed-tail summaries。
- 对 `scale_invariant_continuing_control/config_extended.json` 决定运行范围；这是最大 sweep，应在当前任务完成后再安排。
- 用 extended 证据更新英文报告，并收紧结论措辞。
- 把中文报告扩展为真正的对应报告，加入图表。
- 更新 `final/indexes/results.md`、`results_zh.md`、`reproduction.md` 和 `reproduction_zh.md` 的新结果路径和命令。
- 重新检查 markdown 中英文配对和图表链接。
