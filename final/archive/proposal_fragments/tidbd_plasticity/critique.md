# Critique: TIDBD-Lite Plasticity

## Reviewer Objections

- TIDBD-lite must not be described as canonical TIDBD.
- Feature-wise alpha movement is not enough; prediction error or recovery must improve.
- One relevance switch may be too easy or too narrow.
- Normalized TD is a strong baseline and currently has lower error.

## Revisions Already Made

- Added old/new/distractor step-size groups.
- Added recovery-window summaries.
- Reframed as mechanism evidence without performance win.

## Next Required Iteration

- Implement canonical TIDBD or AutoStep.
- Add repeated relevance switches.
- Report recovery AUC and feature utility contribution.
- Compare with output-controlled updates under identical streams.
