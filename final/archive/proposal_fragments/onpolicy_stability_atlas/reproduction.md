# Reproduction: On-policy Stability Atlas

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/onpolicy_stability_atlas/config_main.json
```

Expected artifacts: `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, `manifest.json`.
