# Parallel Worker Audit: Report Independence, Figures, And EN/ZH Parity

Scope audited: `final/reports/proposals/` and `final/reports/integrated/`.

Snapshot note: report files were being edited concurrently during this audit. Findings below are based on the current file contents observed after the latest read pass. I did not edit any report files.

## Summary

- No missing linked report images were found: 96 Markdown image links were checked and all resolved to existing files.
- I found no high-confidence individual-proposal independence violation where a proposal report depends on, compares itself to, or cites another proposal's result as evidence. Many search hits were shared RL vocabulary such as "reward centering", "normalized TD", "Dyna", "GVF", or "plasticity"; I do not count those as independence violations.
- The largest actionable problems are figure/evidence linkage and EN/ZH parity, especially in `continual_dyna_model_aging/report_zh.md`.

## Issues

### High: Chinese Dyna-aging report is stale and still shows a smoke figure as final-facing evidence

Files:

- `final/reports/integrated/continual_dyna_model_aging/report_zh.md:11`
- `final/reports/integrated/continual_dyna_model_aging/report_zh.md:17`
- `final/reports/integrated/continual_dyna_model_aging/report_zh.md:95`
- `final/reports/integrated/continual_dyna_model_aging/report_zh.md:97`
- English current counterpart: `final/reports/integrated/continual_dyna_model_aging/report.md:10`, `report.md:104`, `report.md:172`, `report.md:176`

Problem:

The English report now says the drift experiment is completed and includes completed drift result figures from `drift_figures/`:

- `report.md:104-109` records completed result `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`.
- `report.md:172-180` gives the drift interpretation and links `drift_figures/report_drift_reward_heatmap.png`, `report_drift_stale_heatmap.png`, and `report_drift_model_error_heatmap.png`.

The Chinese report still says the second drift environment is planned/pending and links a smoke-only image:

- `report_zh.md:17` says the stochastic/gradual drift environment is still planned.
- `report_zh.md:95` says interpretation must wait for extended artifacts.
- `report_zh.md:97` embeds `20260709T084208Z_smoke/figures/report_drift_reward_heatmap.png`.

Why it matters:

This is both a parity gap and a figure-evidence gap. The linked smoke figure is not the real result, while completed report-ready figures are already present in `final/reports/integrated/continual_dyna_model_aging/drift_figures/`.

Exact recommended fix:

Update `report_zh.md` to match the current English report:

- Replace the pending/smoke language at `report_zh.md:11`, `report_zh.md:17`, and `report_zh.md:95` with the completed drift-result statement from `report.md:10` and `report.md:104-109`.
- Remove the smoke figure at `report_zh.md:97`.
- Add the three local drift figures after the main fixed-change figures:
  - `drift_figures/report_drift_reward_heatmap.png`
  - `drift_figures/report_drift_stale_heatmap.png`
  - `drift_figures/report_drift_model_error_heatmap.png`
- Translate the drift interpretation from `report.md:172-180`, including the bounded conclusion: aging helps the search-control story in abrupt/gradual drift but does not show universal superiority under stochastic drift.

### Medium: Important Chinese reports are materially shorter than English reports

Files:

- `final/reports/integrated/continual_dyna_model_aging/report.md` vs `report_zh.md`: 235 EN lines vs 173 ZH lines.
- `final/reports/integrated/predictive_state_plasticity/report.md` vs `report_zh.md`: 241 EN lines vs 160 ZH lines.
- `final/reports/integrated/scale_invariant_continuing_control/report.md` vs `report_zh.md`: 254 EN lines vs 185 ZH lines.
- `final/reports/proposals/reward_centered_sarsa/report.md` vs `report_zh.md`: 283 EN lines vs 182 ZH lines.
- `final/reports/proposals/gvf_predictive_state/report.md` vs `report_zh.md`: 193 EN lines vs 119 ZH lines.
- `final/reports/proposals/centered_td_diagnostics/report.md` vs `report_zh.md`: 157 EN lines vs 89 ZH lines.
- `final/reports/proposals/onpolicy_stability_atlas/report.md` vs `report_zh.md`: 165 EN lines vs 93 ZH lines.

Problem:

The Chinese versions usually preserve image counts, but several important interpretation, reproduction, and critique sections are compressed or missing details. Examples:

- `scale_invariant_continuing_control/report.md:212-220` includes the extended sweep run command. The Chinese reproduction section at `report_zh.md:143-160` includes the fixed-condition pilot and unit-switching command, but not the extended sweep run command.
- `predictive_state_plasticity/report.md:148-160` gives a detailed numeric interpretation of trace/oracle/raw/GVF performance and cue-decodability. The Chinese result section at `report_zh.md:87-99` is much shorter and should be checked against the English numeric claims.
- `reward_centered_sarsa/report.md:156-180` separates experiment-design rationale, main fixed-condition figures, and the no-reset sensitivity interpretation. The Chinese report compresses this into `report_zh.md:93-119`.

Why it matters:

These are final-facing reports. If Chinese readers use `report_zh.md` as the authoritative report, they may miss claim boundaries, reproduction commands, or the exact interpretation of negative/partial results.

Exact recommended fix:

For each listed pair, do a section-by-section sync against the English report. Do not merely add prose length; make sure the Chinese report preserves:

- the focused RL question and claim boundary;
- completed result path(s), seeds, steps, and condition counts;
- all main numeric claims used in the conclusion;
- figure interpretation, not only image links;
- reproduction commands for every completed main/extended run;
- reviewer critique and threats-to-validity caveats.

### Medium: `gvf_question_design` primary figure is readable but weak for the report question

Files:

- `final/reports/proposals/gvf_question_design/report.md:36`
- `final/reports/proposals/gvf_question_design/report.md:118`
- `final/reports/proposals/gvf_question_design/report_zh.md:118`

Problem:

The report question at `report.md:36` asks which GVF cumulant/discount questions are learnable and plausible candidates for useful predictive state. The primary figure at `report.md:118` and `report_zh.md:118` is a single TD-error curve with many cumulant/gamma legend entries. The legend is large and consumes substantial horizontal space; more importantly, TD error alone does not show usefulness or cue relevance.

Why it matters:

The figure can support "learnable", but it is weak evidence for "useful predictive state". It risks inviting the exact over-interpretation the report warns against.

Exact recommended fix:

Keep the curve as a secondary diagnostic, but add a report-primary summary figure or table:

- final/tail absolute TD error as a `cumulant x gamma` heatmap;
- a cue-relevance or downstream proxy if available, such as cue correlation, cue decodability, or junction-control linkage;
- if only TD error exists, explicitly title the figure as "learnability diagnostic only" and state that usefulness remains untested.

For readability, move the legend below the plot or split by cumulant so each panel has only gamma entries.

### Medium: Several proposal reports still rely on single learning-curve figures as their main visual evidence

Files:

- `final/reports/proposals/baird_offpolicy_stability/report.md:53`
- `final/reports/proposals/centered_td_diagnostics/report.md:81`
- `final/reports/proposals/generate_test_features/report.md:85`
- `final/reports/proposals/nonstationary_bandit/report.md:47`
- `final/reports/proposals/options_reusable_subtasks/report.md:50`
- `final/reports/proposals/streaming_representation/report.md:47`
- `final/reports/proposals/tidbd_plasticity/report.md:107`

Problem:

These image links all resolve, but the reports depend on one time-series curve as the primary figure. That is acceptable for a quick diagnostic, but weaker for final-facing reports because the reader has to infer tail performance, recovery, divergence, or seed uncertainty from a curve.

Why it matters:

The course guidance asks for focused RL questions, metrics, and reproducible interpretation. Summary figures make the answer clearer than a dense or noisy curve, especially in PDFs.

Exact recommended fix:

Add one compact report-ready summary view per report, keeping the existing curve as secondary:

- Baird: final weight norm or divergence/stability by algorithm and alpha.
- Centered TD: tail value norm and tail TD error by reward shift and centering method.
- Generate-test features: pre/post-change error plus active trace timescale by method.
- Nonstationary bandit: post-change recovery AUC or tail best-action rate by learner.
- Options: reward per real environment step plus option-use/commitment-cost summary.
- Streaming representation: phase-split TD error and auxiliary-vs-value-only summary.
- TIDBD: late TD error plus feature-alpha dynamics summary; separate "mechanism moved" from "prediction improved".

### Low: One integrated report explicitly mentions other reports inside its independence paragraph

Files:

- `final/reports/integrated/useful_predictive_knowledge/report.md:27`
- `final/reports/integrated/useful_predictive_knowledge/report_zh.md:27`

Problem:

The paragraph says the proposal is independent from "the other reports" and does not rely on "another proposal's result". This is not a substantive independence violation because it does not cite or use another proposal's evidence. Still, individual final reports are cleaner if they state independence positively without referring to other reports.

Exact recommended fix:

Rewrite the paragraph as:

> The question, method, and conclusion are defined entirely within this T-maze predictive-state study. The experiment uses one environment family and one staged criterion: predictive knowledge is useful only if it carries the hidden variable and improves downstream control.

Apply the same idea in Chinese.

### Low: "Per-proposal audit matrix" labels are meta-report wording inside individual reports

Files:

- `final/reports/proposals/output_controlled_td/report.md:158`
- `final/reports/proposals/reward_centered_sarsa/report.md:224`
- `final/reports/integrated/scale_invariant_continuing_control/report.md:182`
- `final/reports/integrated/continual_dyna_model_aging/report.md:192`
- `final/reports/integrated/predictive_state_plasticity/report.md:182`

Problem:

These labels do not mention other proposals, but "Per-proposal audit matrix" reads like portfolio/index language rather than paper-style report language.

Exact recommended fix:

Rename the heading/lead-in to "Reviewer Audit Matrix" or "Reviewer Checklist" inside individual reports.

## Cleared Checks

- No broken Markdown image links were found in the audited report Markdown files.
- `output_controlled_td` figure links use local report-ready panel heatmaps in both English and Chinese; no missing image issue found there.
- `reward_centered_sarsa` figure links use the completed extended result and local sensitivity figures in both English and Chinese; no missing image issue found there.
- Shared method vocabulary across reports should not be treated as an independence violation by itself.
