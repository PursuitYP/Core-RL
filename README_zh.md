# Core RL Course Project 中文入口

本仓库是一个围绕 Alberta Plan 的 Core-RL 课程项目。项目研究小型 online agent 如何从 ordinary experience 中持续学习，严格不使用 replay buffer、不使用 deep network、不做离线训练循环。当前重点包括 continuing control、average reward、reward centering、output-controlled TD updates、learned models、Dyna planning、GVFs、feature utility 和 partial observability。

## 从哪里开始看

如果你想按课程交付物审阅项目，先看 `final/`。最重要的入口是 `final/proposal_overview_zh.md` 中文详细总览、`final/proposal_overview.md` 英文总览、`final/reports/` 下各 proposal 的独立报告，以及 `final/indexes/results.md` 和 `final/indexes/reproduction.md` 里的结果路径与精确复现命令。

如果你想看代码或运行实验，先看 `experiments/alberta_core_rl/`。这里是实际 Python package，包含 proposal-specific runners、configs、results、plotting scripts 和小型 tabular/linear RL environments。顶层 `experiments/` 只是实验工作区，不是 Python 包。

## 目录结构

- `AlbertaPlan.pdf`, `RL_Course_Project.pdf`, `Proposal_Template.md`：课程与任务原始材料。
- `resources/`：导入的论文、课程笔记、class materials 和相关参考资料；这些 imported resources 不应被随意修改。
- `draft/`：计划、粗略研究记录和中间材料。
- `experiments/alberta_core_rl/`：可运行的 online Core-RL 实验、配置、结果目录和绘图/汇总脚本。
- `final/`：面向最终审阅的报告、proposal overview、索引、归档说明和展示材料。
- `conda-env-configs/`：Python 环境与 conda 配置记录。

## 当前最强研究主线

当前最强主线是 `Scale-Invariant Continuing Control`，这是一个更大的独立 continuing-control 课题，把 reward centering 和 output-controlled Sarsa 放进同一个 access-control task，研究在线控制 agent 能否在 reward origin 和 feature unit 变化时仍保持稳定。

planning 方向最强主线是 `Continual Dyna With Model Aging`，它研究环境变化后哪些 learned model entries 仍值得用于 planning。当前最可靠的信号是 stale-backup reduction，而不是简单声称 reward 更高。

`Reward-Centered Continuing Sarsa` 和 `Output-Controlled TD` 是强独立机制研究。`Predictive State Plasticity` 当前是有价值的 negative/redesign gate：在 T-maze control 中 learned GVF state 仍接近 chance，而 trace/oracle memory 能解决任务。

## 运行实验

不要使用 base conda 环境，使用项目专用环境：

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_main.json
```

有 `config_extended.json` 的 proposal 可以运行 extended sweep。新的 extended run 会输出 `_extended` 后缀；少数在后缀逻辑修复前启动的 extended run，已经在核对 `config_used.json` 后手动重命名。

## 报告和索引

每个 proposal 的 `report.md` 应该能独立说明研究动机、研究问题、环境、方法、实验设计、结果、分析、局限和复现命令。重要 final-facing 文档应尽量同时维护英文和中文版本；覆盖情况记录在 `final/indexes/bilingual_coverage.md` 和 `final/indexes/bilingual_coverage_zh.md`。

当前多角色审查和任务状态记录在 `final/indexes/reviewer_audit.md`、`final/indexes/status.md` 以及对应中文文件中。这些文件记录审查者提出的问题、已经采取的行动、运行中的 CPU jobs、已生成 PDF 和仍待处理的 extended results。

## 项目约束

本项目刻意保持在 Core RL 范围内：streaming online updates、tabular 或 linear function approximation、CPU-scale experiments、显式 seeds，以及带 `manifest.json`、`config_used.json`、`summary.json`、`condition_summary.json`、`metrics.csv` 的结果目录。除非明确改变项目范围，不要引入 replay buffer、deep network 或 offline training。
