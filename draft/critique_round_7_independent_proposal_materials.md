# Critique Round 7: Independent Proposal Materials

Date: 2026-07-09

## Trigger

The user clarified that each proposal must be an independent research topic with its own
code path, result artifacts, intermediate materials, final report, and reproduction command.
The previous state still over-relied on a portfolio-level overview.

## Reviewer Findings Incorporated

- `final/reports/proposals/` initially had empty folders.
- Global reports did not replace per-proposal mini-reports.
- Baird and Options cited older result directories without `config_used.json`.
- `reproduction_note.md` only listed a subset of proposal commands.
- The project needed a canonical proposal set table.

## Revisions Made

- Created `final/reports/proposals/README.md` as the canonical independent proposal
  index.
- Added `report.md`, `results.md`, and `reproduction.md` for each implemented proposal.
- Added main configs and reran previously minimal-only self-designed diagnostics:
  centered TD diagnostics, on-policy stability atlas, GVF question design, nonstationary
  bandit, and streaming representation.
- Reran Baird and Options to produce modern provenance artifacts:
  `config_used.json`, `manifest.json`, `condition_summary.json`, `metrics.csv`, and
  `summary.json`.
- Updated `result_index.md`, `current_status_report.md`, and `reproduction_note.md`.
- Marked `proposal_dossiers/` as historical planning briefs rather than canonical final
  materials.

## Current Self-Critique

- Many per-proposal reports are concise mini-reports, not full papers. This is acceptable as
  an intermediate state but should be expanded for any proposal selected for final
  presentation.
- Weak proposals are now independently documented, but some still need stronger negative
  framing and clearer "what would make this worth continuing" sections.
- The project still has old result directories on disk for auditability. Final-facing docs
  must keep warning readers to use `result_index.md` and `proposals/README.md`.
- Per-proposal code is still shared through modules. This is acceptable for maintainability,
  but each proposal report must explicitly identify its own workspace, config, result, and
  implementation module.

## Next Review Questions

1. Does every proposal report state one focused RL question?
2. Does every proposal have a result path with complete provenance artifacts?
3. Does every proposal have a figure or table?
4. Does every weak proposal have an honest negative or dropped-status interpretation?
5. Can a reviewer reproduce any proposal without reading the overview report?
