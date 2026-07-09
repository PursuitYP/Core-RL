# Parallel Worker Independence And Figure Audit

Date: 2026-07-09

Scope audited: current `final/reports/proposals/*/report.md`, `report_zh.md`, and `final/reports/integrated/*/report.md`, `report_zh.md`, plus report READMEs only where they affect independence framing. No fixes were applied.

## Summary

- Report-level independence is mostly satisfied: the 16 report files generally state a focused question, setting, comparison, evidence level, and independent scope.
- Main remaining independence risk is not cross-title citation inside individual reports; it is internal portfolio/status language that makes some reports read like screening notes rather than standalone academic papers.
- Figure-link health is good: all scanned markdown image links resolve. English reports contain 42 image links; Chinese reports contain 41. No missing images, tiny rasters, or extreme aspect-ratio failures were found.
- Requirements 2 and 3 in `revise_plan_20260709.md` / `_zh.md` are partially satisfied. The current materials have coherent integrated directions and Alberta Plan/Core RL links, but the new larger predictive-knowledge topic is still mostly represented as a plan/staged direction rather than a fully independent report.

## Independence And Role-Language Risks

### Confirmed Report-Level Issues

1. `final/reports/proposals/streaming_representation/report.md:7` uses "This mini-report..." and `:9` says the proposal "should therefore be read as an independent negative diagnostic and redesign target." This is honest, but "mini-report" weakens the academic-paper frame. Recommended fix: rewrite as "This study..." and keep the redesign status in claim-boundary or limitations language.

2. `final/reports/proposals/baird_offpolicy_stability/report.md:7` also uses "This mini-report..." for a formal proposal report. Recommended fix: replace with paper-style study language while retaining the bounded Baird-style warning claim from `:3` and `:13-15`.

3. `final/reports/proposals/nonstationary_bandit/report.md:3`, `:7`, and `:9` frame the report as a "sanity diagnostic," "mini-report," and "not promoted as a full Core RL project." This is scientifically honest, but it reads like portfolio triage rather than an independent academic paper. Recommended fix: title/status can remain negative/limited, but abstract language should present a limited-scope bandit adaptation study, with the "not submission-grade" judgment moved to a final limitations paragraph.

4. `final/reports/proposals/options_reusable_subtasks/report.md:3`, `:7`, and `:19` repeatedly use "quarantined." This is useful project-management language, but formal reports should not sound quarantined as artifacts. Recommended fix: replace with "negative-result study" or "conditional proposal"; keep fixed-goal sanity and SMDP-accounting gates as limitations and next experiments.

### Cross-Proposal Title References

- Individual proposal reports do not show a serious pattern of mentioning other proposal titles as separate proposals. Most title hits are self-references or method/theory references.
- The READMEs still contain portfolio mapping language. `final/reports/integrated/README.md:25-27` says Reward-Centered/Output-Controlled, Dyna Planning Budget, and GVF/TIDBD lines "become" integrated stories. This is acceptable as navigation, but it can undermine the instruction that ordinary proposals remain independent if copied into reports or final-facing summaries. Recommended fix: say these integrated reports "study related mechanisms" rather than old proposal titles "become" new proposals.
- `final/reports/proposals/README.md:27-31` ranks candidates and compares larger proposals against "weak single proposals." This is useful for internal review but should stay out of individual report abstracts/conclusions.

## Figure Link And Readability Audit

### Link And Dimension Results

- English reports: 16 files, 42 markdown image links, all resolved.
- Chinese reports: 16 files, 41 markdown image links, all resolved.
- No linked raster was below 500 px width or 300 px height.
- No linked raster exceeded a 3:1 wide/tall aspect ratio. The widest notable figures are:
  - `final/reports/proposals/gvf_predictive_state/report.md:117`: `gvf_trace_by_position.png`, 1440x560, aspect 2.57.
  - `final/reports/proposals/gvf_question_design/report.md:118`: `abs_td_error_by_cumulant-gamma_curve.png`, 1472x672, aspect 2.19.
  These are not automatic failures, but they should be visually checked in PDF because they may become horizontally compressed on narrow pages.

### Caption / Pairing Issues

1. English/Chinese figure parity mismatch in Dyna Aging: English includes the smoke drift figure at `final/reports/integrated/continual_dyna_model_aging/report.md:111`, but the Chinese report starts the figure block with the three extended heatmaps at `final/reports/integrated/continual_dyna_model_aging/report_zh.md:97-101`. Recommended fix: either add the smoke drift figure and its caveat to Chinese, or remove it from English if it is no longer part of final-facing evidence.

2. Minor Chinese caption mismatch: `final/reports/integrated/continual_dyna_model_aging/report_zh.md:109` says "Late model error by planning budget and model mode," while English `report.md:172` includes "and half-life." Recommended fix: align the Chinese alt text/caption with the English caption and the plotted grouping.

3. Output-Controlled TD appears improved: English and Chinese now link panel figures at `final/reports/proposals/output_controlled_td/report.md:95-99` and `report_zh.md:95-99`, all 1944x1944. This addresses the prior wide-compressed heatmap risk.

## Requirement 2 Check: Larger Meaningful Questions Without Patchwork

Plan requirement: `final/indexes/revise_plan_20260709.md:23` and `_zh.md:23` require integrated topics that are not patchwork, plus a candidate large topic, `Useful Predictive Knowledge Under Partial Observability and Resource Limits`.

High-level status: partially satisfied.

- Satisfied: the three integrated reports each have an explicit standalone question and internal experiment logic. Predictive State Plasticity is especially close to the intended new large topic: it asks whether learned predictions become useful state under partial observability (`final/reports/integrated/predictive_state_plasticity/report.md:7`, `:12`, `:16-22`).
- Remaining gap: the exact new candidate large topic is still plan-level rather than a separate formal report. The execution tracker says it is "Planned only" at `final/indexes/revise_plan_20260709.md:90` and `_zh.md:90`.
- Remaining gap: integrated README wording at `final/reports/integrated/README.md:25-27` still describes old proposal titles as becoming integrated stories. That reads slightly patchwork even if the individual integrated reports are stronger.

Recommended fixes:

- Either create a formal standalone report for `Useful Predictive Knowledge Under Partial Observability and Resource Limits`, or explicitly state that `predictive_state_plasticity/report.md` is the renamed/contained version of that candidate.
- Revise integrated README mapping language so it emphasizes one unified question, environment family, staged gates, and success/failure criteria rather than old-proposal title aggregation.

## Requirement 3 Check: Deeper Alberta Plan / Core RL Framing

Plan requirement: `final/indexes/revise_plan_20260709.md:24` and `_zh.md:24` require related work to explain how each source changes the research question or experiment, not merely list sources.

High-level status: partially satisfied.

- Strong examples: Output-Controlled TD explains how Intentional Updates changes the step-size interpretation and baseline choice (`final/reports/proposals/output_controlled_td/report.md:49-55`). Reward-Centered Sarsa connects Alberta Plan themes and reward-centering literature to continuing reward-origin invariance (`final/reports/proposals/reward_centered_sarsa/report.md:60-74`).
- Adequate but still list-like: Dyna Planning Budget explains Dyna/search-control motivation at `final/reports/proposals/dyna_planning_budget/report.md:54-60`, then still has a local-reference list at `:62`. This is acceptable but could be sharper by saying exactly which reference motivates half-life aging, stale-backup rate, or recovery-window metrics.
- Weakest coverage: the small negative/diagnostic reports often have minimal Alberta Plan integration or use it mostly as a boundary condition. This is tolerable for honest negative studies, but if they remain formal proposal papers, each should include one concrete sentence: "this source changed the experiment by making us measure X or compare Y."

Recommended fixes:

- For each report, add or tighten one related-work sentence that maps source -> design consequence -> metric. Example pattern: "Because search-control work treats planning queries as scarce computation, this report measures stale-backup rate in addition to reward."
- Avoid expanding bibliographies. The gap is not citation count; it is whether the cited idea visibly changes the experiment.

## Action Priorities

1. Remove "mini-report," "quarantined," and "sanity diagnostic" from formal report abstracts/status lines, replacing them with paper-style negative-result or limited-scope language.
2. Align Dyna Aging English/Chinese figure parity and the half-life caption.
3. Clarify whether `Predictive State Plasticity` is the current formal version of the planned `Useful Predictive Knowledge...` topic; if yes, say so in the integrated README without using "become" title-aggregation language.
4. Add one source-to-design sentence per weaker report to satisfy requirement 3 without bloating the reports.
