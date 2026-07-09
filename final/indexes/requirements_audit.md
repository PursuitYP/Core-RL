# Original Requirements Coverage Audit

Date: 2026-07-09

This audit is deliberately conservative. It maps the user's original and follow-up requirements to the current project artifacts, but it does not claim that the full research revision is complete. The source-of-truth plan for the current large revision is `final/indexes/revise_plan_20260709.md`; this file records coverage status and remaining gaps.

## Coverage Summary

| Requirement | Current status | Main artifact | Remaining gap |
|---|---|---|---|
| Read course/project sources and Alberta Plan materials | Covered, but still needs deeper per-proposal integration | `AGENTS.md`, `resources/alberta_plan_related/README.md`, `draft/iterative_research_record.md` | Many reports cite the Alberta Plan lens too generally; each strong report should explain exactly how the source changes the research question or experimental design. |
| Prioritize Reward-Centered Sarsa and Output-Controlled TD | Covered with implementation, reports, figures, and extended evidence | `final/reports/proposals/reward_centered_sarsa/`, `final/reports/proposals/output_controlled_td/` | Reward-Centered still needs beta/gamma and no-reset reward-origin switch experiments; Output-Controlled still needs a fair true-online audit and no-reset feature-scale switch. |
| Analyze other proposals and design new angles | Partially covered | `final/reports/proposals/`, `final/reports/integrated/` | Several reports remain diagnostic or negative; their reports must explicitly say whether they are submission-grade, support material, redesign targets, or quarantined. |
| Search Alberta Plan and follow-up work | Covered and continuing | `resources/alberta_plan_related/README.md`, `final/indexes/revise_plan_20260709.md` | The new literature needs to be threaded into individual proposal reports rather than only stored in index-level notes. |
| Complete Proposal Template questions for each proposal | First structural pass covered | `final/reports/**/report.md`, `final/reports/**/report_zh.md`, `final/indexes/report_section_audit.md` | The sections now exist in all reports; the next gap is depth, content matching, and experiment follow-through. |
| At least five reference/course-derived proposals | Structurally covered | Reward centering, output control, GVF state, generate-and-test, options | Some course-derived proposals are weak or quarantined; they should not be presented as equally mature research studies. |
| At least five self-designed or extended proposals | Structurally covered | TIDBD, Baird, Dyna, centered TD, on-policy atlas, GVF question design, streaming representation, integrated proposals | Several self-designed proposals need deeper experiments or honest demotion to diagnostic/negative material. |
| New larger integrated Core RL proposals | Partially covered | `final/reports/integrated/` | Three integrated reports exist, but the new `Useful Predictive Knowledge Under Partial Observability and Resource Limits` candidate is only planned, not implemented as a full report/experiment package. |
| No replay buffer and no deep network | Covered | `experiments/alberta_core_rl/`, `final/indexes/reproduction.md` | Continue checking this constraint whenever adding experiments. |
| Use richer environments beyond toy-only | Partially covered | Access-control, tile random walk, changing gridworld, T-maze streams | Some weaker proposals remain too toy-like and should either be upgraded with richer environments or demoted. |
| Continual improvement with critic rounds | Partially covered | `final/indexes/reviewer_audit.md`, `draft/critique_round_9_independent_study_gap_matrix.md` | The current audit is mostly global; the new plan requires per-proposal 12-role critique/action/risk tables. |
| Professional project structure and clean environment | Partially covered | `conda-env-configs/README.md`, `experiments/alberta_core_rl/studies/`, `final/README.md` | The final structure is improved, but status/index files still need stricter source-of-truth discipline. Two `__pycache__` directories are owned by `nobody:nogroup` and cannot be removed by the normal user. |
| Each proposal independent | First structural pass covered | `final/reports/proposals/`, `final/reports/integrated/` | Every report now states independent scope and evidence level; strong reports still need deeper experiments and weak reports need continued honest framing. |
| Reports include figures/tables | Covered for several strong reports; partial overall | `final/reports/**/figures/`, report PDFs | Some weak/supporting reports still need clearer primary tables or diagnostic figures tied to named research questions. |
| Current CPU-task tracking | Covered for status only | `final/indexes/status.md`, `final/indexes/revise_plan_20260709.md` | `core-rl-scale-invariant-extended-33723554` is RUNNING as of 2026-07-09 14:40 HKT; its result directory exists but has no standard artifacts yet, so it is not evidence. |

## Current Deliverable Structure

- Canonical proposal index: `final/reports/proposals/README.md`
- Canonical proposal reports: `final/reports/proposals/<proposal>/report.md`
- Chinese proposal reports: `final/reports/proposals/<proposal>/report_zh.md`
- Archived proposal fragments: `final/archive/proposal_fragments/<proposal>/`
- Larger integrated reports: `final/reports/integrated/`
- Current result index: `final/indexes/results.md`
- Reproduction note: `final/indexes/reproduction.md`
- Current major revision plan: `final/indexes/revise_plan_20260709.md`
- Iterative research log: `draft/iterative_research_record.md`

## Highest-Priority Remaining Work

1. Add explicit Proposal Template Answers, independent scope, evidence level, required next experiments, and reviewer-audit sections to all 16 current reports.
2. Deepen the strongest proposals with targeted experiments rather than only polishing text.
3. Recast weak proposals as negative/diagnostic/quarantined where appropriate, with failure mechanisms and upgrade conditions.
4. Make English and Chinese report pairs content-consistent, not merely parallel in filename.
5. Integrate current literature into each proposal's motivation and design instead of keeping it only in global notes.
6. Monitor `core-rl-scale-invariant-extended-33723554` and incorporate it only after `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, and `manifest.json` are present.
