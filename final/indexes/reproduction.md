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
| Reward-Centered Sarsa | `experiments/alberta_core_rl/configs/reward_centered_sarsa/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_extended.json` | `experiments/alberta_core_rl/results/reward_centered_sarsa/<timestamp>_extended/` | `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended` | Current evidence is the 20-seed, 20000-step extended sweep. `config_main.json` remains as a quick pilot. |
| Reward-Centered Sensitivity | `experiments/alberta_core_rl/configs/reward_centered_sarsa_sensitivity/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/reward_centered_sarsa_sensitivity/config_extended.json` | `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/<timestamp>_extended/` | Smoke: `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T084151Z_smoke`; pending extended directory: `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended` | Second-round beta/gamma/no-reset reward-origin sensitivity smoke exists. The CPU rerun `core-rl-reward-sensitivity-extended-rerun-28457861` was Running at 2026-07-09 17:19 HKT; the pending extended directory has no standard artifacts and is not evidence. |
| Output-Controlled TD | `experiments/alberta_core_rl/configs/output_controlled_td/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_extended.json` | `experiments/alberta_core_rl/results/output_controlled_td/<timestamp>_extended/` | `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended` | Current evidence is the 20-seed, 20000-step extended sweep. The result directory is rjob-owned, so report figures are written to `final/reports/proposals/output_controlled_td/figures/`. |
| Output-Controlled TD Fairness Audit | `experiments/alberta_core_rl/configs/output_controlled_td_fairness_audit/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td_fairness_audit/config_extended.json` | `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/<timestamp>_extended/` | `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended` | Current evidence is the completed 10-seed fairness audit. The CPU rerun `core-rl-output-fairness-extended-rerun-29576456` succeeded by 2026-07-09 17:41 HKT. |
| GVF Predictive State | `experiments/alberta_core_rl/configs/useful_gvfs_state/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/useful_gvfs_state/config_main.json` | `experiments/alberta_core_rl/results/useful_gvfs_state/<timestamp>_main/` | `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main` | No current extended config; redesign first. |
| Generate-and-Test Features | `experiments/alberta_core_rl/configs/generate_test_features/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/generate_test_features/config_main.json` | `experiments/alberta_core_rl/results/generate_test_features/<timestamp>_main/` | `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main` | No current extended config; utility redesign first. |
| Doorway Options | `experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json` | `experiments/alberta_core_rl/results/options_reusable_subtasks/<timestamp>_main/` | `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main` | No current extended config; fixed-goal sanity check first. |
| TIDBD Plasticity | `experiments/alberta_core_rl/configs/tidbd_plasticity/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/tidbd_plasticity/config_main.json` | `experiments/alberta_core_rl/results/tidbd_plasticity/<timestamp>_main/` | `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main` | No current extended config; canonical TIDBD/AutoStep audit first. |
| Baird Off-policy Stability | `experiments/alberta_core_rl/configs/baird_offpolicy_stability/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/baird_offpolicy_stability/config_main.json` | `experiments/alberta_core_rl/results/baird_offpolicy_stability/<timestamp>_main/` | `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main` | No current extended config; canonical Baird verification first. |
| Dyna Planning Budget | `experiments/alberta_core_rl/configs/dyna_planning_budget/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/dyna_planning_budget/config_extended.json` | `experiments/alberta_core_rl/results/dyna_planning_budget/<timestamp>_extended/` | `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended` | Current evidence is the 20-seed, 20000-step larger-grid diagnostic. |
| Centered TD Diagnostics | `experiments/alberta_core_rl/configs/centered_td_diagnostics/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/centered_td_diagnostics/config_main.json` | `experiments/alberta_core_rl/results/centered_td_diagnostics/<timestamp>_main/` | `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main` | No current extended config; use as mechanism diagnostic. |
| On-policy Stability Atlas | `experiments/alberta_core_rl/configs/onpolicy_stability_atlas/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/onpolicy_stability_atlas/config_main.json` | `experiments/alberta_core_rl/results/onpolicy_stability_atlas/<timestamp>_main/` | `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main` | No current extended config; use as an independent scale-sensitivity diagnostic. |
| GVF Question Design | `experiments/alberta_core_rl/configs/gvf_question_design/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/gvf_question_design/config_main.json` | `experiments/alberta_core_rl/results/gvf_question_design/<timestamp>_main/` | `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main` | No current extended config; downstream cue/control probe first. |
| Nonstationary Bandit | `experiments/alberta_core_rl/configs/nonstationary_bandit/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/nonstationary_bandit/config_main.json` | `experiments/alberta_core_rl/results/nonstationary_bandit/<timestamp>_main/` | `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main` | No current extended config; dropped as final topic. |
| Streaming Representation | `experiments/alberta_core_rl/configs/streaming_representation/config_main.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/streaming_representation/config_main.json` | `experiments/alberta_core_rl/results/streaming_representation/<timestamp>_main/` | `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main` | No current extended config; auxiliary question redesign first. |
| Scale-Invariant Continuing Control | `experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_extended.json` | `experiments/alberta_core_rl/results/scale_invariant_continuing_control/<timestamp>_extended/` | `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended` | Current evidence is the completed 20-seed, 20000-step fixed-condition extended grid. `config_main.json` remains as the quick pilot. |
| Unit-Switching Continuing Control | `experiments/alberta_core_rl/configs/unit_switching_continuing_control/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/unit_switching_continuing_control/config_extended.json` | `experiments/alberta_core_rl/results/unit_switching_continuing_control/<timestamp>_extended/` | `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended` | This is the no-reset unit-change extension for the scale-invariant control report, not a separate final proposal. |
| Continual Dyna Model Aging | `experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_extended.json` | `experiments/alberta_core_rl/results/continual_dyna_model_aging/<timestamp>_extended/` | `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended` | Current evidence is the 20-seed, 20000-step half-life/budget sweep. |
| Continual Dyna Model Aging Drift | `experiments/alberta_core_rl/configs/continual_dyna_model_aging_drift/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/continual_dyna_model_aging_drift/config_extended.json` | `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/<timestamp>_extended/` | Smoke: `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T084208Z_smoke`; pending extended directory: `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended` | Drift-sweep smoke exists. The CPU rerun `core-rl-dyna-drift-extended-rerun-30016335` was Running at 2026-07-09 17:19 HKT; the pending extended directory has no standard artifacts and is not evidence. |
| Predictive State Plasticity | `experiments/alberta_core_rl/configs/predictive_state_plasticity/config_extended.json` | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/predictive_state_plasticity/config_extended.json` | `experiments/alberta_core_rl/results/predictive_state_plasticity/<timestamp>_extended/` | `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended` | Current evidence is the stronger 20-seed negative gate over maze lengths `8/12/20/30`. |

Naming note: the report `final/reports/proposals/gvf_predictive_state/report.md` corresponds to implementation/config/result key `useful_gvfs_state`. This older implementation name was kept to preserve result provenance.

`config_extended.json` files reuse the study's internal `"suite": "main"` logic so the implementation can trigger the same environment family with larger settings. The runner now labels outputs from `config_extended.json` with an `_extended` result-directory suffix, so result provenance should be checked by both directory name and `config_used.json`.

## Plotting

For ordinary learning-curve plots, use `plot_results.py`. For final report figures with many conditions, prefer `plot_report_figures.py`, which reads `condition_summary.json` and makes seed-tail summary plots with readable legends.

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended --kind reward-centered

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended --kind output-td --figure-dir final/reports/proposals/output_controlled_td/figures

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main --kind onpolicy-atlas

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended --kind dyna-budget

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended --kind unit-switching

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended --kind scale --figure-dir final/reports/integrated/scale_invariant_continuing_control/figures

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended --kind output-td --figure-dir final/reports/proposals/output_controlled_td/fairness_figures

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended --kind dyna-aging

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended --kind predictive-state
```

## CPU Task Runs

Longer sweeps should use CPU task queues rather than an interactive session. The wrapper submits to the configured namespace/partition. The default wrapper path was verified on 2026-07-09 with `core-rl-cpu-smoke-fixed-50275254`; older jobs using forced `--private-machine=group` and `brainpp.cn/fuse=1` were stopped because those constraints made the CPU task unschedulable.

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PARTITION=safethm_cpu_task CPU=8 MEM=16000 bash experiments/alberta_core_rl/scripts/run_cpu_task.sh core-rl-output-extended-fixed "PYTHONNOUSERSITE=1 python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_extended.json"
```

Supported partitions:

- `safethm_cpu_task` in namespace `ailab-safethm`.
- `safer2ai_cpu_task` in namespace `ailab-safer2ai`.

Current candidate main-pilot results are listed in `final/indexes/results.md`. Older `minimal` results and early `main` results before the main-environment upgrade are preliminary or obsolete and should not be used as final evidence unless a report explicitly says otherwise.

Current CPU task status: `core-rl-output-extended-fixed-46602102` succeeded on 2026-07-09. Its completed result directory is `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`.

As of 2026-07-09 17:58 HKT, two second-round CPU jobs are still recorded as Running:

- Reward sensitivity: `core-rl-reward-sensitivity-extended-rerun-28457861`
- Dyna drift: `core-rl-dyna-drift-extended-rerun-30016335`

Scale `core-rl-scale-invariant-extended-33723554` succeeded by 2026-07-09 17:45 HKT, and Output fairness `core-rl-output-fairness-extended-rerun-29576456` succeeded by 2026-07-09 17:41 HKT. The two still-running rerun directories `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended` and `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended` have no standard artifacts yet, so they are not evidence. The older failed job IDs `21581151`, `20998802`, and `18940577` failed with `/data/yupeng/conda_envs/core-rl/bin/python: No such file or directory` inside the rjob container; keep them as audit-only records. For CPU tasks, use container `python`, not the host-only `/data/yupeng/conda_envs/core-rl/bin/python`.

Check active jobs with:

```bash
rjob get core-rl-reward-sensitivity-extended-rerun-28457861 --namespace ailab-safethm
rjob logs job core-rl-reward-sensitivity-extended-rerun-28457861 -n 120 --namespace ailab-safethm
rjob get core-rl-dyna-drift-extended-rerun-30016335 --namespace ailab-safethm
rjob logs job core-rl-dyna-drift-extended-rerun-30016335 -n 120 --namespace ailab-safethm
```
