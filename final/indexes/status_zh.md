# 当前状态报告（中文）

日期：2026-07-09

当前项目已经重构为清晰的 final-facing 结构：正式报告在 `final/reports/`，索引在 `final/indexes/`，历史碎片在 `final/archive/`。每个正式 proposal 都有独立 `report.md` 和 `report_zh.md`，不需要从旧 fragment 拼装故事。

## 当前强主线

强主线候选包括 Reward-Centered Sarsa、Output-Controlled TD、Scale-Invariant Continuing Control、Continual Dyna Model Aging。Predictive State Plasticity 是高价值但当前为负向 gate 的综合方向。GVF Predictive State、Generate-and-Test、Options、TIDBD、Baird、Centered TD、On-policy Atlas、Bandit、Streaming Representation 等材料以负结果、支持性诊断或 redesign target 的方式保留。

## 当前重要结果

- Reward-Centered Sarsa 已有 20 seeds、20000 steps extended evidence：`experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended`。
- Output-Controlled TD 当前正式索引仍是 main pilot：`experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`；CPU-task extended run `core-rl-output-extended-fixed-46602102` 正在运行，目标结果目录是 `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`，完成后需要核对并更新报告。
- Scale-Invariant Continuing Control 当前固定条件证据仍是 main pilot：`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`；no-reset unit-switch extension 已完成：`experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`。
- Continual Dyna Model Aging 已有 20 seeds extended half-life/budget evidence：`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`。
- Dyna Planning Budget 已有 20 seeds larger-grid extended evidence：`experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended`。
- Predictive State Plasticity 已有 20 seeds extended negative gate：`experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`。

## 代码与复现状态

代码位于 `experiments/alberta_core_rl/`，各 proposal 的实现拆在 `studies/` 下，配置在 `configs/` 下，结果在 `results/` 下。当前 Python 环境是 `/data/yupeng/conda_envs/core-rl/bin/python`，运行时使用 `PYTHONNOUSERSITE=1` 和 `MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig`。

最近验证：Markdown 图片链接检查通过；`python -m compileall experiments/alberta_core_rl` 无报错；编译生成的 `__pycache__` 已清理；Python 文件仍低于 500 行。

## 仍需继续

当前最重要的开放项是等待 `output_controlled_td/config_extended.json` CPU-task 长实验完成，然后更新 `results.md`、`results_zh.md`、对应报告和图表。`scale_invariant_continuing_control/config_extended.json` 的完整固定条件大 sweep 仍未运行，应在当前任务完成后再安排或提交到验证可用的 CPU task 队列。
