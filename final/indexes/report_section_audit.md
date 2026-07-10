# Report Section Audit

Date: 2026-07-09

This audit checks whether the 17 final-facing reports visibly contain the sections required by the latest revision plan. It is a heading/content-presence audit, not a claim that every section is already paper-perfect. Current result: all 17 English reports and all 17 Chinese reports contain the required structural signals after the latest repair pass. A second clarity pass has also added front-loaded evidence-summary tables to seven supporting or negative proposal reports whose results were previously too easy to miss on first reading.

## Latest Clarity Pass

The second pass focused on independent readability, especially for reports that should not be oversold as strong final submissions. `Baird Off-Policy Stability`, `GVF Predictive State`, `Generate-and-Test Trace Features`, `Nonstationary Bandit`, `Streaming Representation With Auxiliary Prediction`, `Doorway Options for Reusable Subtasks`, and `TIDBD-Lite Plasticity` now each include an `Evidence Summary` section near the top of both English and Chinese reports. These sections state the focused RL question, testbed, compared learners or controllers, seeds and horizon, primary metric, headline numerical result, and conclusion boundary. This does not upgrade weak evidence into strong evidence; it makes the evidence level and limitations clearer.

## English Reports

| Report | Required-section status |
|---|---|
| `final/reports/integrated/continual_dyna_model_aging/report.md` | OK after first repair pass |
| `final/reports/integrated/predictive_state_plasticity/report.md` | OK after first repair pass |
| `final/reports/integrated/scale_invariant_continuing_control/report.md` | OK after first repair pass |
| `final/reports/integrated/useful_predictive_knowledge/report.md` | OK after first repair pass |
| `final/reports/proposals/baird_offpolicy_stability/report.md` | OK after first repair pass |
| `final/reports/proposals/centered_td_diagnostics/report.md` | OK after first repair pass |
| `final/reports/proposals/dyna_planning_budget/report.md` | OK after first repair pass |
| `final/reports/proposals/generate_test_features/report.md` | OK after first repair pass |
| `final/reports/proposals/gvf_predictive_state/report.md` | OK after first repair pass |
| `final/reports/proposals/gvf_question_design/report.md` | OK after first repair pass |
| `final/reports/proposals/nonstationary_bandit/report.md` | OK after first repair pass |
| `final/reports/proposals/onpolicy_stability_atlas/report.md` | OK after first repair pass |
| `final/reports/proposals/options_reusable_subtasks/report.md` | OK after first repair pass |
| `final/reports/proposals/output_controlled_td/report.md` | OK after first repair pass |
| `final/reports/proposals/reward_centered_sarsa/report.md` | OK after first repair pass |
| `final/reports/proposals/streaming_representation/report.md` | OK after first repair pass |
| `final/reports/proposals/tidbd_plasticity/report.md` | OK after first repair pass |

## Chinese Reports

| Report | Required-section status |
|---|---|
| `final/reports/integrated/continual_dyna_model_aging/report_zh.md` | OK after first repair pass |
| `final/reports/integrated/predictive_state_plasticity/report_zh.md` | OK after first repair pass |
| `final/reports/integrated/scale_invariant_continuing_control/report_zh.md` | OK after first repair pass |
| `final/reports/integrated/useful_predictive_knowledge/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/baird_offpolicy_stability/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/centered_td_diagnostics/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/dyna_planning_budget/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/generate_test_features/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/gvf_predictive_state/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/gvf_question_design/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/nonstationary_bandit/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/onpolicy_stability_atlas/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/options_reusable_subtasks/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/output_controlled_td/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/reward_centered_sarsa/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/streaming_representation/report_zh.md` | OK after first repair pass |
| `final/reports/proposals/tidbd_plasticity/report_zh.md` | OK after first repair pass |

## What This Does And Does Not Mean

The first repair pass fixed a real structural problem: every report now visibly states proposal-template answers, independent scope, evidence level, experiment-design rationale, and a reviewer-audit style critique record. The second pass improves first-page readability for the weaker or supporting reports by adding compact evidence summaries with exact result paths and numerical headlines in the body of each independent report.

It does not mean every proposal is equally strong. Reward-Centered Sarsa, Output-Controlled TD, Scale-Invariant Continuing Control, and Continual Dyna Model Aging remain the strongest candidates. Useful Predictive Knowledge is the strongest current representation/GVF gate and now includes a completed feature-budget extension, but still needs oracle-prediction scaling, prediction-to-policy coupling, and plasticity extensions. Predictive State Plasticity is a high-value negative gate. Dyna Planning Budget and several others are supporting diagnostics. Generate-and-Test, Options, Streaming Representation, and Nonstationary Bandit remain negative, quarantined, or dropped unless redesigned.

## Verification

- Structural audit: no required-section signal missing across the 17 English and 17 Chinese reports.
- Image audit: no missing report image links under `final/reports`.
- PDF export: all 17 English `report.pdf` files were regenerated after the latest edits; `final/indexes/english_report_pdf_manifest.json` records `missing_images=0` for every report.
