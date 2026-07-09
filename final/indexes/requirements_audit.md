# Original Requirements Coverage Audit

Date: 2026-07-09

This audit maps the original and follow-up user requirements to current project artifacts. It is meant to prevent the project from silently narrowing into only a few strong results.

## Coverage Summary

| Requirement | Current status | Artifact |
|---|---|---|
| Read course/project sources and Alberta Plan materials | Done; source map maintained | `AGENTS.md`, `resources/alberta_plan_related/README.md`, `draft/iterative_research_record.md` |
| Prioritize Reward-Centered Sarsa and Output-Controlled TD | Done; both implemented, rerun, and expanded into independent reports | `final/reports/proposals/reward_centered_sarsa/`, `final/reports/proposals/output_controlled_td/` |
| Analyze other proposals and design new angles | Done and continuing; all canonical proposals have independent folders and reports | `final/reports/proposals/` |
| Search Alberta Plan and follow-up work | Done and continuing; 2024-2026 reward-centering, intentional-update, streaming, GVF, continual-RL work cached | `resources/alberta_plan_related/README.md` |
| Complete Proposal Template questions for each proposal | Done for all 13 canonical proposals inside the current standalone reports; earlier template drafts are archived for audit | `final/reports/proposals/*/report.md`, `final/archive/proposal_fragments/*/proposal_template.md` |
| At least five reference/course-derived proposals | Covered: reward centering, output control, GVF state, generate-and-test, options | `final/reports/proposals/` |
| At least five self-designed or extended proposals | Covered: TIDBD, Baird, Dyna, centered TD, on-policy atlas, GVF question design, bandit, streaming representation | `final/reports/proposals/` |
| New larger integrated Core RL proposals | Three independent larger proposals created; all three now have main/first-gate pilots | `final/reports/integrated/` |
| No replay buffer and no deep network | Enforced in implementations and manifests | `experiments/alberta_core_rl/`, `final/indexes/reproduction.md` |
| Use richer environments beyond toy-only | Main studies use access-control, tile random walk, changing gridworld, long T-maze; diagnostics are clearly bounded | `final/indexes/results.md` |
| Continual improvement with critic rounds | Done; multiple critique rounds recorded, including independent-study gap audit | `draft/critique_round_9_independent_study_gap_matrix.md` |
| Professional project structure and clean environment | Done; dedicated conda env and modular implementation | `conda-env-configs/README.md`, `experiments/alberta_core_rl/studies/` |
| Each proposal independent | Done structurally through one canonical standalone `report.md` per proposal; earlier separate template/results/critique/reproduction fragments are archived, not current review files | `final/reports/proposals/`, `final/archive/proposal_fragments/` |
| Reports include figures/tables | Done via linked figures and result summaries; more polished tables can still be added after longer CPU sweeps | `final/reports/proposals/*/report.md`, `final/reports/integrated/*/report.md` |

## Current Deliverable Structure

- Canonical proposal index: `final/reports/proposals/README.md`
- Canonical proposal reports: `final/reports/proposals/<proposal>/report.md`
- Archived proposal fragments: `final/archive/proposal_fragments/<proposal>/`
- Three larger integrated proposals: `final/reports/integrated/`
- Current result index: `final/indexes/results.md`
- Reproduction note: `final/indexes/reproduction.md`
- Iterative research log: `draft/iterative_research_record.md`

## Remaining Risks

- Several proposals are still negative or diagnostic rather than strong positive studies. They are independent, but their conclusions must remain honest.
- Most existing main runs use five seeds. Longer CPU sweeps would strengthen final statistics.
- The three large integrated proposals now have at least first-gate pilots. Predictive State Plasticity is currently a negative gate result rather than a positive learned-state result.
- The overview paper may still use older two-main-study wording and should be revised after the per-proposal materials stabilize.
