# Reproduction: Continual Dyna Model Aging

Dedicated large-proposal runner:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_main.json
```

Current dedicated result:

`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main`

Component command:

Current component command:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/dyna_planning_budget/config_main.json
```

Current component result:

`experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main`

Plot commands:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py \
  --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main \
  --y-key avg_reward --group-keys planning_steps model_mode
```

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py \
  --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main \
  --y-key stale_backup_rate --group-keys planning_steps model_mode
```

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py \
  --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main \
  --y-key mean_model_error --group-keys planning_steps model_mode
```
