# 复现说明（中文）

所有实验都是 online streaming Core RL：不使用 replay buffer，不使用 deep network，不使用离线训练。运行前进入项目根目录：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL
```

使用专用环境，不使用 base conda：`/data/yupeng/conda_envs/core-rl/bin/python`。推荐统一环境变量：`PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig`。

## Smoke Test

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python -m compileall experiments/alberta_core_rl
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py
```

注意：这些命令不是只读检查。`compileall` 会生成 `__pycache__`，`smoke_test.py` 会写新的 smoke result directories。

## 主实验命令模式

每个 study 的完整命令见英文 `final/indexes/reproduction.md` 表格。通用形式如下：

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/<proposal>/config_main.json
```

重点 config：`reward_centered_sarsa/config_main.json`、`output_controlled_td/config_main.json`、`scale_invariant_continuing_control/config_main.json`、`continual_dyna_model_aging/config_main.json`、`predictive_state_plasticity/config_main.json`。GVF Predictive State 的实现 key 是 `useful_gvfs_state`，因此 config 和 result path 使用 `useful_gvfs_state`。

## 报告图生成

复杂 integrated 图建议使用 summary figure 脚本，而不是把几十条曲线和图例塞进一张 learning curve：

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main --kind scale
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main --kind dyna-aging
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main --kind predictive-state
```

## CPU Task 状态

已提交 `core-rl-infra-smoke-968081` 到 `ailab-safethm/safethm_cpu_task`，但截至最近检查仍处于 Inqueue/STARTING，且日志接口返回空数据错误。因此不要把 cpu_task 视为已验证通过；等 smoke 成功后再提交 extended sweep。
