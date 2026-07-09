# Current Status Report

Date: 2026-07-09

This status report reflects the latest user clarification: every proposal is an independent research topic and needs its own paper-style report, critique record, result summary, and reproduction path. The overview paper is only an overview; it does not replace per-proposal work.

## Current Research Shape

The project now has two independent layers:

1. Thirteen canonical proposal studies under `final/reports/proposals/`.
2. Three larger integrated-but-independent Core RL studies under `final/reports/integrated/`.

The proposals are not equally strong scientifically. Some are positive candidates, some are mechanism diagnostics, and some are negative or not submission-grade as-is. They are still documented independently.

## Canonical Proposal Materials

Each canonical proposal folder under `final/reports/proposals/<proposal>/` is now intentionally simple: the primary review artifact is `report.md`. The report must stand alone and include the proposal-template answers, motivation, research question, method, environment, experiment design, result interpretation, limitations, critique response, and reproduction command.

Older split fragments are preserved for auditability under `final/archive/proposal_fragments/<proposal>/`. Those archived files include the earlier `proposal_template.md`, `results.md`, `critique.md`, and `reproduction.md` drafts, but they are no longer the main review path. If a claim differs between an archived fragment and the current report, the current `final/reports/**/report.md` is the source to cite.

The short mini-report pass has been replaced with paper-style standalone reports. The reports are still bounded by the evidence actually available; weak proposals are not promoted artificially.

## Three New Larger Independent Proposals

The three larger proposal candidates are:

1. Scale-Invariant Continuing Control.
2. Continual Dyna Model Aging.
3. Predictive State Plasticity.

Scale-Invariant Continuing Control now has a completed main pilot:

`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`

The pilot shows a meaningful interaction: reward centering alone fails under high feature scale, normalized Sarsa alone remains reward-shift sensitive, and combined normalized-centered/differential variants are robust across tested shifts and scales.

Continual Dyna Model Aging now has a completed extended half-life/budget sweep:

`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`

This extended run shows that freshness-aware sampling can sharply reduce stale backups without oracle change detection. At planning budget `20`, keep-model late stale-backup rate is `0.213 +/- 0.065`; recency and recency/error methods can reduce it to near zero under shorter half-lives. Reward ranking depends on budget and half-life.

Predictive State Plasticity now has a completed extended first-gate run:

`experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`

The extended run covers maze lengths `8/12/20/30`. Cue-GVF remains near chance, while trace and oracle memory remain far stronger. This is a useful negative gate: weak hidden-cue information is not enough to become useful state.

## Current Result Index

Final-facing result index:

`final/indexes/results.md`

Important current result directories:

- Reward-Centered Sarsa: `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended`
- Output-Controlled TD: current indexed evidence remains `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`; the extended CPU task `core-rl-output-extended-fixed-46602102` is running, with expected output under `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`.
- Dyna Planning Budget: `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended`
- GVF Predictive State: `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`
- Generate-and-Test: `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`
- TIDBD: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`
- Options: `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`
- Baird: `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`
- Scale-Invariant Continuing Control: `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`
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

Important negative or diagnostic studies:

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
- Workspaces and configs live under `experiments/alberta_core_rl/configs/`.
- Result directories include `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, and `manifest.json`.

Environment:

- Python executable: `/data/yupeng/conda_envs/core-rl/bin/python`
- Use `PYTHONNOUSERSITE=1`
- Use `MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig`

## Next Research Iteration

1. Finish and incorporate the CPU-task extended sweep for Output-Controlled TD; then update result indexes, figures, and reports.
2. Extend Dyna aging to gradual drift, repeated changes, and planning-utility analysis.
3. Redesign GVF predictive-state questions with cue-decodability probes.
4. Add fixed-goal sanity experiments for the Options proposal.
5. Add canonical TIDBD or AutoStep for the plasticity proposal.
6. Keep negative proposals independent and honest; do not promote weak evidence.
