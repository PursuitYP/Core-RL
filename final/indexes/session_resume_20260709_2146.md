# Session Resume 2026-07-09 21:46 HKT

This note records the continuation after the user asked to keep improving according to the prior requirements and plan files. It should be read together with `final/indexes/session_resume_20260709_1830.md`, `final/indexes/revise_plan_20260709.md`, and `final/indexes/status.md`.

## Current Request Being Served

The active instruction is to continue the major RL Course Project revision rather than stop at an intermediate draft. The key constraints remain unchanged: each proposal is an independent research topic, individual reports should stand alone like academic mini-papers, weak proposals must not be oversold, English and Chinese materials should stay synchronized, and code/results/document structure should remain clean and reproducible.

## CPU Task Status Checked

Direct `rjob get` queries were initially blocked in the sandbox by DNS resolution failure. The same queries succeeded after approved non-sandbox rjob access. Confirmed statuses:

| CPU task | Namespace | Status |
|---|---|---|
| `core-rl-reward-sensitivity-extended-rerun-28457861` | `ailab-safethm` | Succeeded |
| `core-rl-dyna-drift-extended-rerun-30016335` | `ailab-safethm` | Succeeded |
| `core-rl-output-fairness-extended-rerun-29576456` | `ailab-safethm` | Succeeded |
| `core-rl-scale-invariant-extended-33723554` | `ailab-safethm` | Succeeded |

These checks support the existing status that the extended Reward sensitivity, Dyna drift, Output fairness, and Scale-Invariant sweeps are current evidence rather than running or stuck jobs.

## Report Improvements Completed In This Continuation

A second report-clarity pass was applied to seven supporting, negative, or quarantined proposal reports that were previously structurally valid but still too slow to read from the top. Each now has a front-loaded `Evidence Summary` in both English and Chinese:

| Proposal | English report | Chinese report | Purpose of the edit |
|---|---|---|---|
| Baird Off-Policy Stability | `final/reports/proposals/baird_offpolicy_stability/report.md` | `final/reports/proposals/baird_offpolicy_stability/report_zh.md` | States the zero-reward stability diagnostic, three-alpha comparison, weight-norm headline, and canonical-Baird boundary. |
| GVF Predictive State | `final/reports/proposals/gvf_predictive_state/report.md` | `final/reports/proposals/gvf_predictive_state/report_zh.md` | States the partial-observability useful-state question and avoids claiming absent cue information without direct cue probes. |
| Generate-and-Test Trace Features | `final/reports/proposals/generate_test_features/report.md` | `final/reports/proposals/generate_test_features/report_zh.md` | Separates structural trace movement from the missing downstream prediction-error improvement. |
| Nonstationary Bandit | `final/reports/proposals/nonstationary_bandit/report.md` | `final/reports/proposals/nonstationary_bandit/report_zh.md` | States that this is a minimal plasticity sanity check, not a submission-grade Core RL claim. |
| Streaming Representation | `final/reports/proposals/streaming_representation/report.md` | `final/reports/proposals/streaming_representation/report_zh.md` | States the negative auxiliary-prediction result and the difference between learnable auxiliary loss and useful value-state signal. |
| Doorway Options | `final/reports/proposals/options_reusable_subtasks/report.md` | `final/reports/proposals/options_reusable_subtasks/report_zh.md` | States the real environment-step accounting result and keeps the transfer claim quarantined. |
| TIDBD-Lite Plasticity | `final/reports/proposals/tidbd_plasticity/report.md` | `final/reports/proposals/tidbd_plasticity/report_zh.md` | Separates visible feature-wise alpha dynamics from the missing prediction-error advantage over normalized TD. |

The edits deliberately do not upgrade these proposals into strong positive claims. They make each report more independently readable and easier to audit.

## Index And Audit Updates

Updated:

- `final/indexes/report_section_audit.md`
- `final/indexes/report_section_audit_zh.md`
- `final/indexes/status.md`
- `final/indexes/status_zh.md`
- `final/indexes/README.md`
- `final/indexes/README_zh.md`

The updated wording records the second clarity pass and keeps the distinction between structural completeness and final paper-level depth.

## Verification Completed

The English report PDFs were regenerated after the latest report edits:

```bash
PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/core-rl-pycache MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/export_english_report_pdfs.py
```

Verification results:

| Check | Result |
|---|---|
| English PDF manifest | `17` entries |
| Existing PDFs | `17/17` |
| Missing images in PDF export | `0` |
| Total exported PDF pages | `133` |
| Markdown image links under `final/reports` | `104` links, `0` missing |
| `git diff --check -- final experiments/alberta_core_rl` | Passed |
| Touched Python compile check | Passed |

After incorporating the parallel audit fixes, the English PDFs were regenerated again. Final post-audit verification in this continuation:

| Check | Result |
|---|---|
| English PDF manifest | `17` entries |
| Existing PDFs | `17/17` |
| Missing images in PDF export | `0` |
| Total exported PDF pages | `135` |
| Markdown image links under `final/reports` | `104` links, `0` missing |
| `git diff --check -- final experiments/alberta_core_rl` | Passed |
| Touched Python compile check | Passed |

## Parallel Audit Worker

Spawned read-only explorer `Sagan` to audit final reports for remaining independence, overclaiming, and opening-clarity problems. The worker was instructed not to edit files. It reported no high-impact cross-report dependency, but flagged several claim-strength issues. The following fixes were applied:

| Finding | Files revised | Resolution |
|---|---|---|
| GVF Predictive State overclaimed absence of cue information without direct cue-decodability in that report. | `final/reports/proposals/gvf_predictive_state/report.md`, `report_zh.md` | Reworded to "does not become usable control state"; direct cue information remains unmeasured in this pilot. |
| Nonstationary Bandit used "confirms" language despite five seeds and wide uncertainty. | `final/reports/proposals/nonstationary_bandit/report.md`, `report_zh.md` | Reworded to "suggests" and "sanity-check observation." |
| Reward-Centered Sarsa used overly broad "necessary" language. | `final/reports/proposals/reward_centered_sarsa/report.md`, `report_zh.md` | Restricted the claim to tested access-control streams and tested design families. |
| Scale-Invariant Continuing Control used overly broad "necessary for stable unit changes" language. | `final/reports/integrated/scale_invariant_continuing_control/report.md`, `report_zh.md` | Reworded as the only tested family/combination that stabilized both nuisance dimensions in the access-control grid. |
| Predictive State Plasticity future mechanisms could read like current evidence. | `final/reports/integrated/predictive_state_plasticity/report.md`, `report_zh.md` | Moved limited-budget replacement, generated traces, and feature-wise step-size adaptation fully into future-work language. |

## Best Next Steps

1. Incorporate the parallel audit worker findings when available, especially any remaining individual report that refers to another proposal in a way that weakens independence.
2. Continue from the stronger experimental gaps already recorded: Reward-Centered now has an early recovery score, but still needs matched-seed recovery and policy probes; Output-Controlled true-online fairness refinements; Dyna repeated-change planning utility; Useful Predictive Knowledge oracle-prediction scaling, GVF-output normalization, and prediction-to-policy coupling.
3. Keep updating both English and Chinese versions for every final-facing report or index touched.
