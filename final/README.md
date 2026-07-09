# Final Materials

Start here when reviewing the RL course project.

## Main Reading Order

1. `proposal_overview_zh.md` is the Chinese quick-review document covering motivation, method, implementation, experiments, results, and current judgment for every proposal.
2. `proposal_overview.md` is the English counterpart of the Chinese overview.
3. `reports/integrated/` contains the three larger independent Core-RL proposals: two currently strong positive directions and one valuable negative/redesign direction.
4. `reports/proposals/` contains the thirteen standalone proposal reports. Each folder has one primary `report.md` and one Chinese `report_zh.md` so the reader does not have to assemble the story from fragments.
5. `indexes/results.md` lists the result directories that should be cited as current evidence.
6. `indexes/reproduction.md` gives the commands and environment assumptions for rerunning experiments.
7. `indexes/bilingual_coverage.md` records which important documents have matched English/Chinese versions.
8. `indexes/status.md` summarizes current proposal status and remaining gaps.

## Directory Contract

- `reports/`: final-facing proposal reports.
- `indexes/`: project-level status, result, reproduction, and requirement coverage indexes.
- `presentation/`: poster or presentation-facing material.
- `archive/`: historical drafts, old proposal fragments, and deferred ideas. These files are kept for auditability but are not the main reading path.

Source-of-truth rule:

- Current claims should cite `final/reports/**/report.md` plus `final/indexes/results.md`.
- `final/indexes/*.md` summarizes status, commands, and evidence, but it does not override a current report.
- `final/archive/` is audit-only. Use it to understand the evolution of an idea, not as the current proposal text.
- If an archived fragment conflicts with a current report, trust the current report and result index.
- Important final-facing documents should be maintained in matched English/Chinese pairs. See `indexes/bilingual_coverage.md`.

The previous extra `final/` nesting has been removed. The final-facing path is now simply `final/`.
