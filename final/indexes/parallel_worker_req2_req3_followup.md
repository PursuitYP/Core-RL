# Parallel Worker Follow-Up Audit: Requirements 2 and 3

Date: 2026-07-09

Scope: audit only requirements 2 and 3 from `final/indexes/revise_plan_20260709.md` and `final/indexes/revise_plan_20260709_zh.md`. I inspected `final/reports/integrated/`, `final/reports/proposals/`, `final/proposal_overview*.md`, `final/indexes/results*.md`, `final/indexes/status*.md`, and relevant config/result paths. I did not edit any other file.

Post-audit resolution note: the main continuation after this worker memo synchronized the integrated count to four, added Useful Predictive Knowledge to overview/results/status/reproduction indexes, incorporated completed Reward Sensitivity and Dyna Drift artifacts, and regenerated all 17 English report PDFs with `missing_images=0`. This memo remains useful as a record of what was found before those fixes.

## Verdict

| Requirement | Status | Substantive judgment |
|---|---|---|
| 2. Combine existing proposals into larger meaningful questions without patchwork. | Pass, with documentation drift. | The repository now has genuinely larger integrated questions, not just a scattered list of small proposals. `Scale-Invariant Continuing Control`, `Continual Dyna Model Aging`, and `Useful Predictive Knowledge Under Partial Observability` each define one combined research pressure, one main environment family, methods/baselines, metrics, and completed result artifacts. The caveat is that several index files still describe only three integrated proposals and do not yet recognize `useful_predictive_knowledge`, so navigation is stale. |
| 3. Go deeper into Alberta Plan/Core-RL and propose a stronger integrated problem with clear motivation, questions, experiments, and results. | Partial, materially improved. | The earlier gap was no longer merely planned: `final/reports/integrated/useful_predictive_knowledge/report.md` now exists, has English/Chinese reports, a config, a runner, report figures, and standard result artifacts. It is a real Alberta Plan/Core-RL proposal about predictive knowledge becoming useful state. It is still not fully satisfied because the current evidence covers Gate 1/2 only, uses one T-maze family and 10 seeds, and lacks the planned feature-budget/plasticity stages. Subsequent edits added the PDF and synchronized the main overview/results/status/reproduction indexes. |

## Evidence For Requirement 2

The integrated layer is no longer just an arbitrary merge of ordinary proposals.

- `final/reports/integrated/scale_invariant_continuing_control/report.md` combines reward centering, average-reward/differential thinking, and output-controlled updates around one question: can a continuing access-control agent remain stable under reward-origin and feature-unit changes? It has completed fixed-condition evidence at `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended` and no-reset unit-switch evidence at `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`.
- `final/reports/integrated/continual_dyna_model_aging/report.md` combines Dyna planning, learned models, model freshness, nonstationarity, and computation budget around one question: when should a continual Dyna agent trust learned model entries after change? The main evidence is `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`. The drift extension also has standard artifacts at `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`, and subsequent edits incorporated it into the report/index layer.
- `final/reports/integrated/useful_predictive_knowledge/report.md` converts the previously proposed larger representation topic into a concrete integrated study: learned predictions are judged by information and control gates, not TD error alone. The main evidence is `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main`.

The ordinary proposal layer still contains weak, negative, and quarantined studies, but that is no longer fatal to requirement 2. `final/reports/proposals/README.md` explicitly separates main studies, diagnostics, redesign targets, and quarantined items. This reduces the risk that the final project reads like a scattered set of equal-weight proposals.

Documentation drift found by this worker and resolved by subsequent edits:

- `final/reports/integrated/README.md`, `final/indexes/status.md`, `final/indexes/results.md`, `final/indexes/reproduction.md`, and `final/proposal_overview.md` were updated to recognize the fourth integrated proposal.
- `final/indexes/report_section_audit.md` and `final/indexes/english_report_pdf_manifest.json` were updated for 17 English reports/PDFs; `final/reports/integrated/useful_predictive_knowledge/report.pdf` now exists.

## Evidence For Requirement 3

The strongest new evidence is `Useful Predictive Knowledge Under Partial Observability`.

- Report path: `final/reports/integrated/useful_predictive_knowledge/report.md`.
- Chinese report path: `final/reports/integrated/useful_predictive_knowledge/report_zh.md`.
- Config: `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json`.
- Runner/registry evidence: `experiments/alberta_core_rl/proposals.py` registers `useful_predictive_knowledge`; `experiments/alberta_core_rl/studies/predictive_state.py` implements `proposal_useful_predictive_knowledge`.
- Result path: `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main`.
- Standard artifacts present: `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, and `manifest.json`.
- Figure paths: `final/reports/integrated/useful_predictive_knowledge/figures/report_upk_trial_accuracy_by_length.png`, `report_upk_decision_decoding_by_length.png`, and `report_upk_cue_margin_by_length.png`.

This report is a real Core-RL/Alberta Plan proposal rather than a literature wrapper. It defines a focused question, a partial-observability T-maze testbed, online linear Sarsa and normalized TD/GVF learners, explicit information/control gates, and four research questions. It also reports a clear mixed negative result: trace and oracle memory solve the task, raw observation stays near chance, cue-GVFs carry above-chance cue information, but no learned GVF condition improves control.

Key numbers from the report/result:

- Result scale: `summary.json` records 10 seeds, 12000 online steps, 36 condition groups, and 1041120 metric rows.
- Trace memory trial accuracy is about `0.945`, `0.928`, and `0.892` for maze lengths `8`, `12`, and `20`.
- Oracle memory is about `0.943`, `0.941`, and `0.943`.
- Raw observation is near chance at about `0.506`, `0.511`, and `0.486`.
- Best learned cue decoding is cue-GVF `gamma=0.8`, about `0.626`, `0.611`, and `0.638`, but its trial accuracy remains near chance at about `0.508`, `0.508`, and `0.495`.

This satisfies the most important spirit of requirement 3: it takes an Alberta Plan idea, predictive knowledge as agent state, and turns it into a small, online, interpretable Core-RL experiment with honest failure analysis.

Why requirement 3 is still partial:

- The report covers Gate 1/2 only: information and control usability. It does not yet implement the planned feature-budget, generate-and-test, TIDBD/AutoStep, or component-utility stages.
- The report uses one environment family. The revise plan asked for a larger proposal with multiple important research questions and richer experiment scale; a delayed-cue trace-conditioning stream or feature-budget stream is still needed to test whether the conclusion survives outside the T-maze.
- The evidence is 10 seeds, not the 20-seed level used by the strongest integrated evidence.
- It was not yet first-class in project navigation when this worker audited it; subsequent edits synchronized overview, results/status/reproduction indexes, integrated README, PDF manifest, and report-section audit.

## Additional Current-Evidence Notes

Two result directories that some indexes still called pending at audit time now contain standard artifacts and have been synchronized:

- `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended`: `summary.json` records 8112150 rows and 1575 condition groups. This strengthens the unit/continuing-control line but should be synchronized by the main agent currently editing reward-centered reports.
- `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`: `summary.json` records 1800900 rows and 690 condition groups. This strengthens the Dyna integrated line and has since been incorporated into the current Dyna reports.

I did not change those reports because the requested write scope is only this memo and the main agent is assumed to be editing reward-centered and Dyna reports.

## Follow-Up Directions

1. Complete the `Useful Predictive Knowledge` integrated proposal as the requirement-3 target.
   - Run a 20-seed focused replication of the key T-maze conditions: raw, trace, oracle, best cue-GVF `gamma=0.8`, and one terminal/junction negative control.
   - Add an oracle-prediction feature and GVF-output normalization/scaling audit to test whether the failure is information quality or control utilization.
   - Add one feature-budget stage on a delayed-cue trace-conditioning stream: fixed traces, random replacement, downstream-error generate-and-test, and canonical TIDBD/AutoStep only if the useful-prediction gate improves.

2. Finish the Dyna integrated line with completed drift evidence.
   - Incorporate `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended` into the report and figures.
   - Emphasize the sharper question: planning utility per simulated backup under abrupt, gradual, and stochastic nonstationarity.
   - Add one repeated-change run if time permits; otherwise report drift as the main generalization test and reserve repeated changes as future work.

3. Synchronize the integrated portfolio contract.
   - Decide whether the final integrated count is now four or whether `useful_predictive_knowledge` replaces/renames `predictive_state_plasticity`.
   - Update `final/reports/integrated/README.md`, `final/proposal_overview*.md`, `final/indexes/results*.md`, `status*.md`, `reproduction*.md`, `report_section_audit*.md`, and the PDF manifest accordingly.
   - Generate `final/reports/integrated/useful_predictive_knowledge/report.pdf` after the index decision.

## Bottom Line

Requirement 2 is substantively satisfied: the repository now contains coherent larger Core-RL questions rather than only scattered proposals. Requirement 3 is substantively started and much stronger than the earlier audit, but not fully complete: the new predictive-knowledge proposal has a real report and result, yet still needs the planned second-stage feature-budget/plasticity experiments and index/PDF synchronization before it can be called fully satisfied.
