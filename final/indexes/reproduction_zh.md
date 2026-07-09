# 复现说明（中文）

所有实验都是 online streaming Core RL：不使用 replay buffer，不使用 deep network，不使用离线训练。运行前进入项目根目录：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL
```

使用专用环境，不使用 base conda：`/data/yupeng/conda_envs/core-rl/bin/python`。推荐统一环境变量：`PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig`。环境配置说明在 `conda-env-configs/README.md` 和 `conda-env-configs/core-rl.yml`。

## Smoke Test

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python -m compileall experiments/alberta_core_rl
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py
```

注意：这些命令不是只读检查。`compileall` 会生成 `__pycache__`，`smoke_test.py` 会写新的 smoke result directories。最近一次本地 smoke 已通过，结果在 `experiments/alberta_core_rl/results/*/20260709T014901Z_smoke` 和 `experiments/alberta_core_rl/results/*/20260709T014902Z_smoke` 附近。

## 当前主线实验

每个命令都会在 `experiments/alberta_core_rl/results/<implementation_key>/<timestamp>_<suite>/` 下创建新结果目录，里面应包含 `metrics.csv`、`summary.json`、`condition_summary.json`、`config_used.json`、`manifest.json`，以及可能的 `figures/`。正式结果解释应引用 `condition_summary.json` 里的 seed-tail 统计，而不是单条曲线截图。

| Study | 推荐运行命令 | 当前结果路径 | 研究用途 |
|---|---|---|---|
| Reward-Centered Sarsa | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_extended.json` | `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended` | 当前证据使用 20 seeds、20000 online steps、5 个 reward shifts、3 个 alpha。它检验 continuing control 是否应该把 reward origin 当成任意单位选择，而不是让绝对 reward offset 进入 value scale。 |
| Output-Controlled TD | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_main.json` | `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main` | 这是 prediction 侧的 scale-control 诊断，检验以 prediction output 的相对更新幅度控制 TD 步长是否能避免 raw feature scale 改变带来的发散。20-seed CPU-task extended run 正在运行，目标目录目前不完整，不能引用为完成证据。 |
| Scale-Invariant Continuing Control | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_main.json` | `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main` | 固定条件 pilot 用于检验 reward centering、feature normalization、differential/continuing objective 的组合是否能降低 reward origin 和 feature unit 对同一个 alpha 的敏感性。完整 extended 固定条件 sweep 还需要继续运行。 |
| Unit-Switching Continuing Control | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/unit_switching_continuing_control/config_extended.json` | `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended` | 这是 Scale-Invariant Continuing Control 的 no-reset extension：同一个 agent 在不中断学习的情况下经历 reward origin、feature scale 或二者同时改变，用来检查稳定方法是否真的能适应 streaming unit changes。 |
| Continual Dyna Model Aging | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_extended.json` | `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended` | 当前证据是 20 seeds、20000 steps 的 half-life/budget sweep。它检验 freshness-aware search control 是否能减少 stale model backups，并显示 reward ranking 会随 planning budget 和 half-life 改变。 |
| Dyna Planning Budget | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/dyna_planning_budget/config_extended.json` | `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended` | 这是 model-aging 前置诊断：在较大 grid 上扩大 planning budget，观察 planning 是否在 nonstationary change 后放大 stale model backup。它不作为强最终课题单独夸大，而是服务 Continual Dyna Model Aging。 |
| Predictive State Plasticity | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/predictive_state_plasticity/config_extended.json` | `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended` | 这是 predictive-state 方向的强负向 gate：如果 learned GVF feature 连 trace memory 都不能稳定替代，就不能轻易进入 generate-and-test 或复杂 representation plasticity。 |

## 支持性实验命令

下面这些结果主要用于机制诊断、负结果记录或 appendix，不建议作为最终主提交课题，除非后续重新设计实验问题和扩大证据。

| Study | 运行命令 | 当前结果路径 | 当前定位 |
|---|---|---|---|
| GVF Predictive State | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/useful_gvfs_state/config_main.json` | `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main` | 说明当前 recurrent GVF 不能替代 trace/oracle memory，是 predictive state 方向的早期负结果。 |
| Generate-and-Test Features | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/generate_test_features/config_main.json` | `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main` | 当前 utility rule 不优于 random replacement，应作为 redesign warning。 |
| Doorway Options | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/options_reusable_subtasks/config_main.json` | `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main` | option transfer claim 暂时不成立，后续需要固定目标 sanity test。 |
| TIDBD Plasticity | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/tidbd_plasticity/config_main.json` | `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main` | TIDBD-lite 有 plasticity 行为，但还不够严谨，不能替代 canonical TIDBD/AutoStep 审计。 |
| Baird Off-policy Stability | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/baird_offpolicy_stability/config_main.json` | `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main` | 作为 off-policy instability warning；正式使用前仍需 canonical Baird feature/policy audit。 |
| Centered TD Diagnostics | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/centered_td_diagnostics/config_main.json` | `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main` | 支持 reward-centering 机制解释，不作为独立主课题。 |
| On-policy Stability Atlas | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/onpolicy_stability_atlas/config_main.json` | `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main` | 支持 Output-Controlled TD 的动机，展示 feature scale 会缩小稳定 alpha 区域。 |
| GVF Question Design | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/gvf_question_design/config_main.json` | `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main` | 说明容易预测的 GVF 不一定是有用 state，需要下游解码或 control ablation。 |
| Nonstationary Bandit | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/nonstationary_bandit/config_main.json` | `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main` | 只作为 constant-alpha tracking 的 introductory sanity check。 |
| Streaming Representation | `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/streaming_representation/config_main.json` | `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main` | 当前 auxiliary target 没有改善 value prediction，保留为负结果和重设计依据。 |

## 报告图生成

普通 learning-curve 图使用 `plot_results.py`。条件很多的 integrated 报告优先使用 `plot_report_figures.py`，因为它读取 `condition_summary.json` 并生成更适合论文报告的 seed-tail summary figure，避免图例挤压主要图像。

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended --kind reward-centered
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main --kind output-td
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main --kind onpolicy-atlas
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended --kind dyna-budget
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended --kind unit-switching
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main --kind scale
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended --kind dyna-aging
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py --result-dir experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended --kind predictive-state
```

## CPU Task 状态

2026-07-09 已修正 `experiments/alberta_core_rl/scripts/run_cpu_task.sh` 的默认提交约束：不再默认强制 `--private-machine=group` 和 `brainpp.cn/fuse=1`，因为这些约束会让 `safethm_cpu_task` 出现 node-selector mismatch。旧的 `core-rl-infra-smoke-968081` 和 `core-rl-output-extended-131257-78853482` 已停止；修正后的 `core-rl-cpu-smoke-fixed-50275254` 已成功跑完全项目 smoke，证明 CPU task 通道、项目挂载和容器内 Python 依赖可用。

当前正在运行的长实验是 `core-rl-output-extended-fixed-46602102`，目标结果目录是 `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`。在该目录出现 `condition_summary.json` 和 figures 前，不要把它引用为已完成的 extended evidence；完成后需要同步更新 `final/indexes/results_zh.md`、`final/indexes/results.md`、Output-Controlled TD 中英文报告和总览。
