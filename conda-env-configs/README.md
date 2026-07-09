# Conda Environment Configs

This directory stores conda environment configuration files. It is not an RL environment/testbed directory.

The project uses a dedicated conda environment, not base:

- Environment name: `core-rl`
- Environment path: `/data/yupeng/conda_envs/core-rl`
- Python executable: `/data/yupeng/conda_envs/core-rl/bin/python`
- Conda executable used to create it: `/mnt/shared-storage-user/yupeng/miniconda3/bin/conda`
- Conda package cache: `/data/yupeng/conda_pkgs`

The environment was created with:

```bash
/mnt/shared-storage-user/yupeng/miniconda3/bin/conda create -y -n core-rl \
  python=3.10 pip numpy pandas matplotlib scipy seaborn tabulate tqdm pypdf
```

The conda config includes:

```text
envs_dirs:
  - /data/yupeng/conda_envs
  - /mnt/shared-storage-user/yupeng/miniconda3/envs
pkgs_dirs:
  - /data/yupeng/conda_pkgs
```

Use this interpreter for local runs:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py
```

Current verified package versions:

```text
Python 3.10.20
numpy 2.2.5
pandas 2.3.3
matplotlib 3.10.9
scipy 1.15.3
seaborn 0.13.2
pypdf 6.8.0
```

Verification run:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python -m compileall experiments/alberta_core_rl

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py
```

The latest clean smoke test completed on 2026-07-09 and wrote current smoke outputs under `experiments/alberta_core_rl/results/*/20260709T014901Z_smoke` and `experiments/alberta_core_rl/results/*/20260709T014902Z_smoke`. This smoke run includes the new `scale_invariant_continuing_control`, `continual_dyna_model_aging`, and `predictive_state_plasticity` proposals.

`PYTHONNOUSERSITE=1` is required so the environment does not import packages from `/home/yupeng/.local/lib/python3.10/site-packages`.

Cluster jobs run inside an rjob image. Do not assume that local `/data/yupeng/conda_envs` is available inside every job container; either use an image with the required packages or explicitly prepare the same environment in the mounted GPFS workspace.
