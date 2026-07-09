# Reproduction Note

All experiments are online streaming Core RL experiments. No replay buffer and no deep network are used. Run every command from the repository root:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL
```

The dedicated Python environment is `/data/yupeng/conda_envs/core-rl/bin/python`. Use `PYTHONNOUSERSITE=1` so user-site packages do not leak into the run, and set `MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig` so plotting does not write outside the project. Conda environment details are in `conda-env-configs/README.md` and `conda-env-configs/core-rl.yml`.

## Local Smoke Test

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python -m compileall experiments/alberta_core_rl

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py
```

Latest verified local smoke run before this revision: 2026-07-09, with outputs under `experiments/alberta_core_rl/results/*/20260709T014901Z_smoke` and `experiments/alberta_core_rl/results/*/20260709T014902Z_smoke`.

These checks are intentionally not read-only: `compileall` creates `__pycache__` bytecode, and `smoke_test.py` creates new smoke result directories.

## Current Study Commands

Each command writes a new directory under `experiments/alberta_core_rl/results/<implementation_key>/<timestamp>_<suite>/` containing `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, `manifest.json`, and optional `figures/`. The current result path column is the candidate evidence indexed by `final/indexes/results.md`; rerunning will create a newer timestamped directory.

| Study | Config path | Exact local command | Expected output location | Current result path | Extended-run availability |
|---|---|---|---|---|---|
| Reward-Centered Sarsa | `experiments/alberta_core_rl/configs/reward_centered_sarsa/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_main.json` | `experiments/alberta_core_rl/results/reward_centered_sarsa/<timestamp>_main/` | `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main` | `config_extended.json` exists; 20 seeds and 20000 steps. |
| Output-Controlled TD | `experiments/alberta_core_rl/configs/output_controlled_td/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_main.json` | `experiments/alberta_core_rl/results/output_controlled_td/<timestamp>_main/` | `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main` | `config_extended.json` exists; 20 seeds and 20000 steps. |
| GVF Predictive State | `experiments/alberta_core_rl/configs/useful_gvfs_state/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/useful_gvfs_state/config_main.json` | `experiments/alberta_core_rl/results/useful_gvfs_state/<timestamp>_main/` | `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main` | No current extended config; redesign first. |
| Generate-and-Test Features | `experiments/alberta_core_rl/configs/generate_test_features/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/generate_test_features/config_main.json` | `experiments/alberta_core_rl/results/generate_test_features/<timestamp>_main/` | `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main` | No current extended config; utility redesign first. |
| Doorway Options | `experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json` | `experiments/alberta_core_rl/results/options_reusable_subtasks/<timestamp>_main/` | `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main` | No current extended config; fixed-goal sanity check first. |
| TIDBD Plasticity | `experiments/alberta_core_rl/configs/tidbd_plasticity/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/tidbd_plasticity/config_main.json` | `experiments/alberta_core_rl/results/tidbd_plasticity/<timestamp>_main/` | `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main` | No current extended config; canonical TIDBD/AutoStep audit first. |
| Baird Off-policy Stability | `experiments/alberta_core_rl/configs/baird_offpolicy_stability/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/baird_offpolicy_stability/config_main.json` | `experiments/alberta_core_rl/results/baird_offpolicy_stability/<timestamp>_main/` | `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main` | No current extended config; canonical Baird verification first. |
| Dyna Planning Budget | `experiments/alberta_core_rl/configs/dyna_planning_budget/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/dyna_planning_budget/config_main.json` | `experiments/alberta_core_rl/results/dyna_planning_budget/<timestamp>_main/` | `experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main` | `config_extended.json` exists; 20 seeds and 20000 steps. |
| Centered TD Diagnostics | `experiments/alberta_core_rl/configs/centered_td_diagnostics/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/centered_td_diagnostics/config_main.json` | `experiments/alberta_core_rl/results/centered_td_diagnostics/<timestamp>_main/` | `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main` | No current extended config; use as mechanism diagnostic. |
| On-policy Stability Atlas | `experiments/alberta_core_rl/configs/onpolicy_stability_atlas/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/onpolicy_stability_atlas/config_main.json` | `experiments/alberta_core_rl/results/onpolicy_stability_atlas/<timestamp>_main/` | `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main` | No current extended config; merge evidence into Output-Controlled TD if needed. |
| GVF Question Design | `experiments/alberta_core_rl/configs/gvf_question_design/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/gvf_question_design/config_main.json` | `experiments/alberta_core_rl/results/gvf_question_design/<timestamp>_main/` | `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main` | No current extended config; downstream cue/control probe first. |
| Nonstationary Bandit | `experiments/alberta_core_rl/configs/nonstationary_bandit/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/nonstationary_bandit/config_main.json` | `experiments/alberta_core_rl/results/nonstationary_bandit/<timestamp>_main/` | `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main` | No current extended config; dropped as final topic. |
| Streaming Representation | `experiments/alberta_core_rl/configs/streaming_representation/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/streaming_representation/config_main.json` | `experiments/alberta_core_rl/results/streaming_representation/<timestamp>_main/` | `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main` | No current extended config; auxiliary question redesign first. |
| Scale-Invariant Continuing Control | `experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_main.json` | `experiments/alberta_core_rl/results/scale_invariant_continuing_control/<timestamp>_main/` | `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main` | `config_extended.json` exists; 20 seeds, 20000 steps, broader reward-shift/scale/alpha grid triggered by `steps>=20000`. |
| Continual Dyna Model Aging | `experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_main.json` | `experiments/alberta_core_rl/results/continual_dyna_model_aging/<timestamp>_main/` | `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main` | `config_extended.json` exists; 20 seeds, 20000 steps, planning budget `0/1/5/20`, half-life sweep for aging modes. |
| Predictive State Plasticity | `experiments/alberta_core_rl/configs/predictive_state_plasticity/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/predictive_state_plasticity/config_main.json` | `experiments/alberta_core_rl/results/predictive_state_plasticity/<timestamp>_main/` | `experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main` | `config_extended.json` exists, but current recommendation is redesign before expensive sweep. |

Naming note: the report `final/reports/proposals/gvf_predictive_state/report.md` corresponds to implementation/config/result key `useful_gvfs_state`. This older implementation name was kept to preserve result provenance.

`config_extended.json` files currently use `"suite": "main"` intentionally. The extended status is identified by the config path and larger seed/step settings; the result directory suffix may still be `_main` unless the runner is later extended with a distinct suite label.

## Plotting

For ordinary learning-curve plots, use `plot_results.py`. For final report figures with many conditions, prefer `plot_report_figures.py`, which reads `condition_summary.json` and makes seed-tail summary plots with readable legends.

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py --result-dir experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main --y-key avg_unshifted_reward --group-keys algorithm reward_shift

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py --result-dir experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main --y-key rmse --group-keys algorithm scale alpha

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py --result-dir experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main --y-key avg_unshifted_reward --group-keys algorithm reward_shift scale

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main --y-key stale_backup_rate --group-keys planning_steps model_mode

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main --kind scale

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main --kind dyna-aging

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main --kind predictive-state
```

## CPU Task Runs

Longer sweeps should use CPU task queues rather than an interactive session. The wrapper submits to the configured namespace/partition:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PARTITION=safethm_cpu_task CPU=32 MEM=128000 bash experiments/alberta_core_rl/scripts/run_cpu_task.sh core-rl-output-extended "PYTHONNOUSERSITE=1 MPLCONFIGDIR=/tmp/core-rl-mplconfig python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_extended.json"
```

Supported partitions:

- `safethm_cpu_task` in namespace `ailab-safethm`.
- `safer2ai_cpu_task` in namespace `ailab-safer2ai`.

Current candidate main-pilot results are listed in `final/indexes/results.md`. Older `minimal` results and early `main` results before the main-environment upgrade are preliminary or obsolete and should not be used as final evidence unless a report explicitly says otherwise.
