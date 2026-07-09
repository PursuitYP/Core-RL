# Current Status Report

Date: 2026-07-09

This status report reflects the latest correction from the user: the project is not finished just because every proposal has a folder or a first report. Every proposal must stand as an independent research topic with its own question, setting, method, experiment design, evidence, critique response, limitations, and reproduction path. The current state is an improved intermediate state, not a completed final revision.

## Current Research Shape

The project has two final-facing layers:

1. Thirteen canonical proposal studies under `final/reports/proposals/`.
2. Three larger integrated-but-independent Core RL studies under `final/reports/integrated/`.

The proposals are intentionally not treated as equally strong. Reward-Centered Sarsa, Output-Controlled TD, Scale-Invariant Continuing Control, and Continual Dyna Model Aging are the strongest current candidates. Several other proposals are negative results, diagnostics, redesign targets, or quarantined topics. Those weaker studies should remain independent, but their reports must not overclaim.

## Current Report Status

Each canonical proposal folder under `final/reports/proposals/<proposal>/` has a `report.md` and `report_zh.md`, and integrated reports follow the same pattern. The first structural repair pass is now complete: all 16 English reports and 16 Chinese reports contain visible Proposal Template answers, independent scope, evidence level, experiment-design rationale, and reviewer-audit style critique records. This does not make every report paper-perfect; weak proposals still need either deeper experiments or honest negative/quarantine framing, which is now stated inside the reports.

All 16 English `report.md` files were exported to `report.pdf` in the same report directories after the latest edits. The PDF manifest is `final/indexes/english_report_pdf_manifest.json`; the export recorded `missing_images=0` for every PDF.

Older split fragments are preserved for auditability under `final/archive/proposal_fragments/<proposal>/`. They are not the current source to cite. If an archived fragment conflicts with a current report, the current `final/reports/**/report.md` is the active artifact, but the active artifact may still need revision under `final/indexes/revise_plan_20260709.md`.

## Three Larger Independent Proposals

The three current integrated proposal candidates are:

1. Scale-Invariant Continuing Control.
2. Continual Dyna Model Aging.
3. Predictive State Plasticity.

Scale-Invariant Continuing Control has a completed full fixed-condition extended sweep:

`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`

It also has a completed no-reset unit-switch extension:

`experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`

The full fixed-condition CPU task `core-rl-scale-invariant-extended-33723554` in namespace `ailab-safethm` succeeded by 2026-07-09 17:45 HKT and wrote standard artifacts. It is now citable evidence: 375 condition groups and 7500 seed-conditions show `0/1500` divergent seed-conditions for normalized Sarsa, normalized reward-centered Sarsa, and normalized differential Sarsa, versus `500/1500` for discounted Sarsa and reward-centered Sarsa.

Three second-round extended sweeps were added after the latest reviewer-style critique:

- Reward-centered beta/gamma/no-reset switch: smoke result `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T084151Z_smoke`; rerun CPU task `core-rl-reward-sensitivity-extended-rerun-28457861`, recorded Running at 2026-07-09 17:19 HKT; rerun directory `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended` exists but has no standard artifacts yet.
- Output-controlled true-online fairness audit: smoke result `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T084151Z_smoke`; rerun CPU task `core-rl-output-fairness-extended-rerun-29576456`, succeeded by 2026-07-09 17:41 HKT; extended result `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended` has standard artifacts and is now evidence. Seed-level divergence is `0/300` for normalized TD and trace-normalized TD(lambda), `81/300` for fixed TD and raw-alpha true-online TD(lambda), and `34/300` for naive normalized true-online TD(lambda), with the normalized true-online failures concentrated in lognormal feature scaling.
- Dyna model-aging drift sweep: smoke result `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T084208Z_smoke`; rerun CPU task `core-rl-dyna-drift-extended-rerun-30016335`, recorded Running at 2026-07-09 17:19 HKT; rerun directory `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended` exists but has no standard artifacts yet.

The first submissions for these three sweeps failed immediately because the command used the host-only Python path `/data/yupeng/conda_envs/core-rl/bin/python`, which does not exist inside the rjob container. Failed job IDs `21581151`, `20998802`, and `18940577` are audit-only records and must not be mixed into current evidence. They were resubmitted with container `python`; the rerun tasks listed above are the active ones.

Continual Dyna Model Aging has a completed extended half-life/budget sweep:

`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`

Predictive State Plasticity has a completed extended first-gate negative run:

`experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`

It also has a completed cue-decodability analysis:

- `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/cue_decodability_summary.csv`
- `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_cue_decodability_by_length.png`

## Current Result Index

Final-facing result index:

`final/indexes/results.md`

Important current result directories:

- Reward-Centered Sarsa: `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended`
- Output-Controlled TD: `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`
- Dyna Planning Budget: `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended`
- GVF Predictive State: `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`
- Generate-and-Test: `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`
- TIDBD: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`
- Options: `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`
- Baird: `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`
- Scale-Invariant Continuing Control: fixed-condition evidence `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`; no-reset unit-switch evidence `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`
- Unit-Switching Continuing Control: `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`
- Continual Dyna Model Aging: `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`
- Predictive State Plasticity: `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`
- Reward-Centered Sensitivity smoke: `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T084151Z_smoke`
- Reward-Centered Sensitivity pending extended directory: `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended` (no standard artifacts; not evidence)
- Output TD Fairness smoke: `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T084151Z_smoke`
- Output TD Fairness extended evidence: `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended`
- Dyna Drift smoke: `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T084208Z_smoke`
- Dyna Drift pending extended directory: `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended` (no standard artifacts; not evidence)

## Evidence Quality Summary

Strong positive candidates:

- Reward-Centered Sarsa.
- Output-Controlled TD.
- Scale-Invariant Continuing Control.
- Continual Dyna Model Aging.

Promising but needs extension:

- Dyna Planning Budget.
- Predictive State Plasticity as a negative first-gate result needing redesign.

Important negative, diagnostic, or quarantined studies:

- GVF Predictive State.
- Generate-and-Test Features.
- Doorway Options.
- TIDBD-Lite Plasticity.
- Baird Off-policy Stability.
- Centered TD Diagnostics.
- On-policy Stability Atlas.
- GVF Question Design.
- Nonstationary Bandit.
- Streaming Representation.

## Code And Reproduction Status

Code remains modular:

- `experiments/alberta_core_rl/proposals.py` is the proposal registry/runner.
- Proposal implementations live in `experiments/alberta_core_rl/studies/`.
- Configs live under `experiments/alberta_core_rl/configs/`.
- Result directories are expected to include `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, and `manifest.json`.

Environment:

- Local Python executable: `/data/yupeng/conda_envs/core-rl/bin/python`
- CPU-task container command: use `python`, not `/data/yupeng/conda_envs/core-rl/bin/python`, because the rjob container only mounts the project storage path.
- Use `PYTHONNOUSERSITE=1`
- Use `MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig`

Recent verification is mixed:

- Markdown image-link checks passed earlier for final-facing reports.
- `python -m compileall experiments/alberta_core_rl` completed earlier without code errors.
- Generated `__pycache__` directories remain under `experiments/alberta_core_rl/` because they are owned by `nobody:nogroup`; normal user cleanup failed with permission denied.
- Python source files remain under the 500-line guidance.

## Next Research Iteration

1. Use the completed Scale-Invariant extended sweep as current evidence, while adding gradual drift, recovery AUC, and policy-distance probes for the next research iteration.
2. Deepen the newly added Proposal Template, evidence-level, and reviewer-audit sections where they affect project decisions.
3. Monitor the reward-sensitivity and Dyna-drift rerun CPU tasks; if they finish, generate figures and incorporate only completed standard artifacts into the relevant reports.
4. Extend Dyna aging beyond the current drift runner with repeated changes and planning-utility analysis.
5. Redesign GVF predictive-state questions using the completed cue-decodability probe.
6. Add fixed-goal sanity experiments for the Options proposal.
7. Add canonical TIDBD or AutoStep for the plasticity proposal.
8. Keep negative proposals independent and honest; do not promote weak evidence.
