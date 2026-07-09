# Reproduction: Doorway Options

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json
```

Expected artifacts:

- `metrics.csv`
- `summary.json`
- `condition_summary.json`
- `config_used.json`
- `manifest.json`
