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

Older split fragments are preserved for auditability under `final/archive/proposal_fragments/<proposal>/`. They are not the current source to cite. If an archived fragment conflicts with a current report, the current `final/reports/**/report.md` is the active artifact, but the active artifact may still need revision under `final/indexes/revise_plan_20260709.md`.

## Three Larger Independent Proposals

The three current integrated proposal candidates are:

1. Scale-Invariant Continuing Control.
2. Continual Dyna Model Aging.
3. Predictive State Plasticity.

Scale-Invariant Continuing Control has a completed main pilot:

`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`

It also has a completed no-reset unit-switch extension:

`experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`

The full fixed-condition extended sweep has been submitted as CPU task `core-rl-scale-invariant-extended-33723554` in namespace `ailab-safethm`. It was confirmed RUNNING at 2026-07-09 14:40 HKT on `lg-cmc-h-cpu-0058.host.h.pjlab.org.cn`. The run has created `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`, but that directory currently has no standard artifacts, so it is not evidence yet.

Continual Dyna Model Aging has a completed extended half-life/budget sweep:

`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`

Predictive State Plasticity has a completed extended first-gate negative run:

`experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`

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
- Scale-Invariant Continuing Control: current evidence is `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`; running empty result directory is `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`
- Unit-Switching Continuing Control: `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`
- Continual Dyna Model Aging: `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`
- Predictive State Plasticity: `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`

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

- Python executable: `/data/yupeng/conda_envs/core-rl/bin/python`
- Use `PYTHONNOUSERSITE=1`
- Use `MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig`

Recent verification is mixed:

- Markdown image-link checks passed earlier for final-facing reports.
- `python -m compileall experiments/alberta_core_rl` completed earlier without code errors.
- Generated `__pycache__` directories remain under `experiments/alberta_core_rl/` because they are owned by `nobody:nogroup`; normal user cleanup failed with permission denied.
- Python source files remain under the 500-line guidance.

## Next Research Iteration

1. Monitor CPU task `core-rl-scale-invariant-extended-33723554`; if it succeeds, incorporate the new Scale-Invariant Continuing Control extended sweep into reports, figures, PDFs, and indexes.
2. Deepen the newly added Proposal Template, evidence-level, and reviewer-audit sections where they affect project decisions.
3. Extend Dyna aging to gradual drift, repeated changes, and planning-utility analysis.
4. Redesign GVF predictive-state questions with cue-decodability probes.
5. Add fixed-goal sanity experiments for the Options proposal.
6. Add canonical TIDBD or AutoStep for the plasticity proposal.
7. Keep negative proposals independent and honest; do not promote weak evidence.
