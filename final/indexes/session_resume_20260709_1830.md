# Session Resume Note / 会话恢复记录

Timestamp: 2026-07-09 18:30 HKT

This file records the current state before pausing the session. Use it as the first file to read after resuming work. The project is not complete; this note preserves exactly what was finished, what is running, and what should happen next.

Post-resume resolution note: this file is a historical pause snapshot. The subsequent continuation completed the Useful Predictive Knowledge main run, the Reward-Centered sensitivity sweep, and the Dyna drift sweep; current evidence/status should be read from `final/indexes/status.md`, `final/indexes/results.md`, and `final/indexes/reproduction.md`.

## Current User Priority

The active task is the large revision requested by the user: every proposal must remain an independent academic-style study, reports must be clearer and more paper-like, figures must be readable, requirements 2 and 3 in `final/indexes/revise_plan_20260709.md` and `final/indexes/revise_plan_20260709_zh.md` must be genuinely addressed, and the work should keep iterating instead of stopping after superficial edits.

特别注意：每个 proposal 的独立报告不能把自己写成其他 proposal 的附录，也不应在正文中串题。综合型报告可以存在，但它们也必须是独立课题，不是把多个小题强行拼成一个总论文。

## Completed In This Session

1. Parallel worker audits were completed.
   - `final/indexes/parallel_worker_req2_req3_audit.md`: Requirement 2 is partially done; Requirement 3 is partially done and weak. It recommends the larger topic `Useful Predictive Knowledge Under Partial Observability And Resource Limits`.
   - `final/indexes/parallel_worker_independence_figure_audit.md`: individual reports mostly preserve independence, but some reports had internal status language such as `mini-report`, `quarantined`, and `sanity diagnostic`; it also found a Dyna English/Chinese figure mismatch.

2. Report independence language was repaired in multiple formal reports.
   - Replaced `mini-report` style wording in Streaming Representation, Baird Off-policy Stability, GVF Question Design, and Nonstationary Bandit.
   - Replaced `quarantined` formal-report wording in Doorway Options with `bounded negative-result study` language.
   - Replaced some `sanity diagnostic/check` wording with `limited-scope study`, `mechanism check`, `validation`, or `consistency check`.
   - Remaining uses of words like `diagnostic` mostly refer to legitimate scientific diagnostics rather than weak report status.

3. Figure readability fixes were applied.
   - Output-Controlled TD primary report figures now link to square panel heatmaps:
     - `final/reports/proposals/output_controlled_td/figures/report_log_rmse_heatmap_panels.png`
     - `final/reports/proposals/output_controlled_td/figures/report_divergence_heatmap_panels.png`
     - `final/reports/proposals/output_controlled_td/figures/report_prediction_change_heatmap_panels.png`
   - GVF Predictive State now uses a report-local vertical panel figure:
     - `final/reports/proposals/gvf_predictive_state/figures/gvf_trace_by_position_panels.png`
   - The markdown image check found no missing linked report images after these changes.

4. Dyna Aging English/Chinese parity was improved.
   - `final/reports/integrated/continual_dyna_model_aging/report_zh.md` now includes the smoke drift figure and caveat that the figure is validation-only until the extended drift artifacts are written.
   - The Chinese model-error caption now includes half-life, matching the English report.

5. Integrated README wording was revised to avoid patchwork framing.
   - `final/reports/integrated/README.md`
   - `final/reports/integrated/README_zh.md`
   These now describe the integrated reports as independent research topics rather than saying ordinary proposal titles “become” new proposals.

6. A new formal integrated topic was implemented to address the requirement-3 gap.
   - New runner: `useful_predictive_knowledge`
   - Code changes:
     - `experiments/alberta_core_rl/studies/predictive_state.py`
     - `experiments/alberta_core_rl/proposals.py`
     - `experiments/alberta_core_rl/report_figures_predictive.py`
     - `experiments/alberta_core_rl/scripts/plot_report_figures.py`
   - New configs:
     - `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_smoke.json`
     - `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json`
   - New reports:
     - `final/reports/integrated/useful_predictive_knowledge/report.md`
     - `final/reports/integrated/useful_predictive_knowledge/report_zh.md`
   - Smoke experiment passed:
     - `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102313Z_smoke`
   - Smoke report figures were generated successfully.

7. Code size remains acceptable.
   - `experiments/alberta_core_rl/studies/predictive_state.py`: 377 lines
   - `experiments/alberta_core_rl/report_figures_predictive.py`: 135 lines
   - `experiments/alberta_core_rl/scripts/plot_report_figures.py`: 77 lines
   - `experiments/alberta_core_rl/proposals.py`: 251 lines

## Historical Running Work And Current Resolution

1. `useful_predictive_knowledge` main run completed after resume. Current evidence path: `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main`.

2. CPU job `core-rl-reward-sensitivity-extended-rerun-28457861` produced standard artifacts after resume. Current evidence path: `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended`.

3. CPU job `core-rl-dyna-drift-extended-rerun-30016335` produced standard artifacts after resume. Current evidence path: `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`.

4. `__pycache__` cleanup remains blocked by file ownership.
   - Remaining directories:
     - `experiments/alberta_core_rl/__pycache__`
     - `experiments/alberta_core_rl/studies/__pycache__`
   - They are owned by `nobody:nogroup`; normal deletion and escalated sandbox deletion both returned permission denied. Future verification should use `PYTHONPYCACHEPREFIX=/tmp/core-rl-pycache` to avoid writing new cache files into the repo.

## Resume Steps

Start here after resuming:

1. Check whether the local useful-predictive-knowledge run survived and completed.

```bash
find experiments/alberta_core_rl/results/useful_predictive_knowledge -maxdepth 2 -type f -printf '%TY-%Tm-%Td %TH:%TM:%TS %p\n' | sort | tail -80
```

If the local exec session is still available, poll it:

```text
write_stdin session_id=86697 chars="" yield_time_ms=30000
```

If no `*_main` artifacts exist, rerun locally or submit to CPU task. CPU-task submission command:

```bash
PARTITION=safethm_cpu_task CPU=16 MEM=64000 \
  bash experiments/alberta_core_rl/scripts/run_cpu_task.sh \
  core-rl-useful-predictive-main \
  "PYTHONNOUSERSITE=1 python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json"
```

2. Once `useful_predictive_knowledge` main artifacts exist, generate report figures into the report directory.

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind useful-predictive-knowledge \
  --result-dir experiments/alberta_core_rl/results/useful_predictive_knowledge/<timestamp>_main \
  --figure-dir final/reports/integrated/useful_predictive_knowledge/figures
```

3. Extract the key useful-predictive-knowledge numbers from `condition_summary.json`.
   - Required metrics:
     - best and worst `trial_accuracy_seed_tail` by maze length and algorithm,
     - best and worst `decision_cue_decoding_correct_seed_tail`,
     - `cue_alignment_margin_seed_tail`,
     - whether any GVF condition passes both information and control gates.
   - Update both `report.md` and `report_zh.md` with identical claims, result paths, figures, and limitations.

4. Update the global documents so the new integrated topic is no longer “planned only.”
   - `final/reports/integrated/README.md`
   - `final/reports/integrated/README_zh.md`
   - `final/indexes/status.md`
   - `final/indexes/status_zh.md`
   - `final/indexes/results.md`
   - `final/indexes/results_zh.md`
   - `final/indexes/reproduction.md`
   - `final/indexes/reproduction_zh.md`
   - `final/proposal_overview.md`
   - `final/proposal_overview_zh.md`
   - `final/indexes/revise_plan_20260709.md`
   - `final/indexes/revise_plan_20260709_zh.md`

5. Poll the two CPU jobs and incorporate them only if standard artifacts exist.

```bash
rjob get core-rl-reward-sensitivity-extended-rerun-28457861 --namespace ailab-safethm
rjob logs job core-rl-reward-sensitivity-extended-rerun-28457861 -n 120 --namespace ailab-safethm
rjob get core-rl-dyna-drift-extended-rerun-30016335 --namespace ailab-safethm
rjob logs job core-rl-dyna-drift-extended-rerun-30016335 -n 120 --namespace ailab-safethm
```

If those commands fail with DNS/network errors inside sandbox, rerun with escalation.

6. Regenerate English PDFs after report edits.

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/export_english_report_pdfs.py
```

7. Run verification.

```bash
PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/core-rl-pycache \
  /data/yupeng/conda_envs/core-rl/bin/python -m py_compile \
  experiments/alberta_core_rl/proposals.py \
  experiments/alberta_core_rl/studies/predictive_state.py \
  experiments/alberta_core_rl/report_figures_predictive.py \
  experiments/alberta_core_rl/scripts/plot_report_figures.py

git diff --check -- README.md README_zh.md final experiments/alberta_core_rl
```

Also rerun the markdown-image existence audit and report-section audit before declaring the revision pass complete.

## Files Changed In This Pause Point

Current `git status --short` shows modified or new files in:

- `experiments/alberta_core_rl/proposals.py`
- `experiments/alberta_core_rl/report_figures_predictive.py`
- `experiments/alberta_core_rl/scripts/plot_report_figures.py`
- `experiments/alberta_core_rl/studies/predictive_state.py`
- `experiments/alberta_core_rl/configs/useful_predictive_knowledge/`
- `final/reports/integrated/useful_predictive_knowledge/`
- `final/reports/integrated/README.md`
- `final/reports/integrated/README_zh.md`
- `final/reports/integrated/continual_dyna_model_aging/report_zh.md`
- multiple proposal reports under `final/reports/proposals/`
- `final/indexes/parallel_worker_independence_figure_audit.md`
- `final/reports/proposals/gvf_predictive_state/figures/`

No commit has been made.

## Chinese Short Resume / 中文简版恢复说明

下次恢复后先读本文件。当前最大新增是 `useful_predictive_knowledge`：它已经有代码、config、plotting、英文/中文 report skeleton，smoke run 通过；main run 在本地 session `86697` 中仍在跑，但退出外层 session 后不保证继续。恢复后第一件事是检查 `experiments/alberta_core_rl/results/useful_predictive_knowledge/` 是否出现新的 `*_main` 目录和标准 artifacts。如果没有，就重新本地运行或提交到 `safethm_cpu_task`。主结果出来后，生成 report figures，补 `report.md` / `report_zh.md` 的真实数值和图，再同步所有 status/results/reproduction/overview/revise_plan 文档，并重新导出英文 PDFs。
