# Independent Proposal Index

This folder is the final-facing location for the thirteen independent proposal reports. Each proposal is documented as a standalone study, but they are not all submission-grade final topics. The main review path is intentionally simple: open a proposal folder, then read `report.md`; the report itself states whether the study is a main candidate, a conditional proposal, a negative result, or a supporting diagnostic.

This distinction is deliberate. The project requirement asked for independent proposal workflows, not for artificially positive conclusions. A weak or negative proposal can still be useful if it states a focused RL question, gives a reproducible test, and explains why the result fails or should be demoted. For final submission, the strongest candidates are currently Reward-Centered Sarsa, Output-Controlled TD, Dyna Planning Budget as a precursor to model aging, and the larger integrated proposals in `../integrated/`.

## Canonical Proposal Set

| Proposal | Source | Status | Workspace | Current result | Report |
|---|---|---|---|---|---|
| Reward-Centered Sarsa | Reference/course-derived | Main study | `experiments/alberta_core_rl/configs/reward_centered_sarsa` | `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main` | `reward_centered_sarsa/report.md` |
| Output-Controlled TD | Reference/course-derived | Main study | `experiments/alberta_core_rl/configs/output_controlled_td` | `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main` | `output_controlled_td/report.md` |
| GVF Predictive State | Reference/course-derived | Negative/redesign | `experiments/alberta_core_rl/configs/useful_gvfs_state` | `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main` | `gvf_predictive_state/report.md` |
| Generate-and-Test Features | Reference/course-derived | Negative/redesign | `experiments/alberta_core_rl/configs/generate_test_features` | `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main` | `generate_test_features/report.md` |
| Doorway Options | Reference/course-derived | Quarantined | `experiments/alberta_core_rl/configs/options_reusable_subtasks` | `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main` | `options_reusable_subtasks/report.md` |
| TIDBD Plasticity | Self-designed/extended | Supporting | `experiments/alberta_core_rl/configs/tidbd_plasticity` | `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main` | `tidbd_plasticity/report.md` |
| Baird Off-policy Stability | Self-designed/extended | Supporting | `experiments/alberta_core_rl/configs/baird_offpolicy_stability` | `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main` | `baird_offpolicy_stability/report.md` |
| Dyna Planning Budget | Self-designed/extended | Conditional third study | `experiments/alberta_core_rl/configs/dyna_planning_budget` | `experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main` | `dyna_planning_budget/report.md` |
| Centered TD Diagnostics | Self-designed/extended | Supporting | `experiments/alberta_core_rl/configs/centered_td_diagnostics` | `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main` | `centered_td_diagnostics/report.md` |
| On-policy Stability Atlas | Self-designed/extended | Supporting | `experiments/alberta_core_rl/configs/onpolicy_stability_atlas` | `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main` | `onpolicy_stability_atlas/report.md` |
| GVF Question Design | Self-designed/extended | Supporting/redesign aid | `experiments/alberta_core_rl/configs/gvf_question_design` | `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main` | `gvf_question_design/report.md` |
| Nonstationary Bandit | Self-designed/extended | Dropped sanity check | `experiments/alberta_core_rl/configs/nonstationary_bandit` | `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main` | `nonstationary_bandit/report.md` |
| Streaming Representation | Self-designed/extended | Dropped diagnostic | `experiments/alberta_core_rl/configs/streaming_representation` | `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main` | `streaming_representation/report.md` |

## Evidence Tiers

Main independent candidates: Reward-Centered Sarsa and Output-Controlled TD have the cleanest standalone question, implementation, baseline comparison, current result, and direct Alberta Plan connection.

Conditional or upgradeable candidates: Dyna Planning Budget, GVF Predictive State, Generate-and-Test, TIDBD, Baird, Options, GVF Question Design, On-policy Stability Atlas, Centered TD Diagnostics, Streaming Representation, and Nonstationary Bandit each document an independent question, but some are currently negative, diagnostic, or too narrow to submit unchanged. Their reports should be read as honest research records, not as equally strong final proposals.

Integrated candidates: Scale-Invariant Continuing Control and Continual Dyna Model Aging currently look stronger than most weak single proposals because they combine several Core RL pressures into one coherent research question. Predictive State Plasticity is important but still high-risk because current evidence is a first-gate negative result.

## File Contract

Each proposal folder contains:

- `report.md`: standalone paper-style research report, including motivation, research question, RL problem definition, method, experiment design, current evidence, critique, and reproduction pointer.

Older supporting fragments were moved to `final/archive/proposal_fragments/<proposal>/`. They are retained for auditability, but the report is now the canonical document.

Weak proposals remain included only when they have an honest negative or dropped-status interpretation. They are still treated as independent studies, but their conclusions may be "not submission-grade as-is" rather than positive claims.

## Additional Large Independent Proposals

Three larger integrated-but-independent Core RL proposals live in `../integrated/`:

- Scale-Invariant Continuing Control.
- Continual Dyna Model Aging.
- Predictive State Plasticity.

These are additional independent research topics with their own standalone reports. They do not replace the 13 canonical proposal folders.
