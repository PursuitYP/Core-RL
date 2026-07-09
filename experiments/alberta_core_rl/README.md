# Alberta Core RL Experiments

Lightweight streaming RL experiments for the course project. The code uses tabular or linear learners only: no replay buffers, no deep networks.

## Code Layout

- `agents.py`: shared tabular/linear learners.
- `envs.py`: small Core RL environments and streams.
- `studies/`: proposal-specific experiment implementations, split by research question.
- `proposals.py`: thin registry plus run and summary utilities.
- `configs/<proposal>/`: per-proposal configs.
- `results/<proposal>/`: run outputs.

`experiments/` itself is intentionally not a Python package. Script entry points add `experiments/` to `sys.path` and import `alberta_core_rl` directly, so the only package boundary is this directory.

## Run One Proposal

Use the project conda environment for local runs:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_main.json
```

Minimal configs are for sanity checks only:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_minimal.json
```

or:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --proposal output_controlled_td --suite minimal --seeds 0 1 2 --steps 2000
```

## Plot Results

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py \
  --result-dir experiments/alberta_core_rl/results/output_controlled_td/<run_dir>
```

## Run All Smoke Tests

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py
```

## Run All Minimal Experiments

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_all.py \
  --suite minimal --seeds 0 1 2 --steps 1000
```

Results are written under `experiments/alberta_core_rl/results/<proposal>/<timestamp>_<suite>/`. Each result directory contains `manifest.json`, `summary.json`, `condition_summary.json`, `metrics.csv`, and optional figures.

## Main Configs

Main configs are separate from minimal configs:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/output_controlled_td/config_main.json
```

Minimal runs are preliminary sanity checks. Main conclusions should use current `main` runs with `condition_summary.json`.

## CPU Task Runs

Longer CPU sweeps can be submitted to cluster CPU task partitions. Cluster jobs run inside the rjob image, so do not assume the local `/data/yupeng/conda_envs/core-rl` environment is mounted there unless the job image or launch command explicitly provides it. The default wrapper path was verified with `core-rl-cpu-smoke-fixed-50275254` on 2026-07-09; keep `PRIVATE_MACHINE` and `USE_FUSE` unset unless a queue administrator asks for them.

```bash
PARTITION=safethm_cpu_task CPU=8 MEM=16000 \
  bash experiments/alberta_core_rl/scripts/run_cpu_task.sh \
  core-rl-output-extended-fixed \
  "PYTHONNOUSERSITE=1 python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_extended.json"
```

Supported `PARTITION` values:

- `safethm_cpu_task` for namespace `ailab-safethm`.
- `safer2ai_cpu_task` for namespace `ailab-safer2ai`.

Optional queue constraints:

- `PRIVATE_MACHINE=group` adds `--private-machine=group`.
- `USE_FUSE=1` adds `--custom-resources brainpp.cn/fuse=1`.

These options can make CPU jobs unschedulable on ordinary CPU task nodes, so use them only when a specific cluster path requires them.
