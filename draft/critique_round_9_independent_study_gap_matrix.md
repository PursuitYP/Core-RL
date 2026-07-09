# Critique Round 9: Independent Proposal Depth Audit

Date: 2026-07-09

The user clarified that each proposal must be treated as an independent academic study, not
as a small component of a single portfolio paper. This audit resets the deliverable
standard.

## New Standard For Every Proposal

Each canonical proposal needs its own:

1. focused RL question;
2. academic motivation;
3. Alberta Plan connection;
4. related-work anchors;
5. environment definition;
6. method and baselines;
7. experimental design with variables, seeds, and metrics;
8. result analysis with figure references;
9. limitations and threats to validity;
10. reviewer-style critique and revision plan;
11. reproduction command and result path;
12. honest final conclusion for that proposal alone.

The current reports are useful briefs, but most are too short to meet this standard.

## Proposal-Specific Gaps

| Proposal | Current evidence | Missing depth | Required revision |
|---|---|---|---|
| Reward-Centered Sarsa | Strong access-control reward-shift result | Needs fuller average-reward motivation, reward-origin invariance framing, beta/gamma threats, differential comparison | Expand to standalone paper with invariance hypothesis and longer-run plan |
| Output-Controlled TD | Strong tile random-walk scale result | Needs true-online baseline audit, stability-region framing, feature-scale geometry explanation | Expand as standalone streaming prediction paper |
| GVF Predictive State | Strong negative with trace/oracle baselines | Needs careful statement of what is falsified, useful-prediction theory, redesign route | Expand as negative paper on predictive-state question design |
| Generate-and-Test Features | Negative current design | Needs oracle validation, repeated shifts, utility-target critique | Expand as negative feature-utility study |
| Doorway Options | Negative under real-step accounting | Needs fixed-goal sanity gate, SMDP accounting explanation, option-cost story | Expand as independent temporal-abstraction failure analysis |
| TIDBD Plasticity | Mechanism signal, no error win | Needs canonical TIDBD caution, plasticity metrics, feature-relevance story | Expand as plasticity mechanism paper |
| Baird Off-policy Stability | Good diagnostic | Needs canonical verification, relationship to GVF background predictions, ETD/GTD context | Expand as off-policy stability diagnostic paper |
| Dyna Planning Budget | Good planning/staleness diagnostic | Needs model-freshness framing and oracle-flush caveat | Expand as continual model-staleness paper |
| Centered TD Diagnostics | Clear mechanism toy | Too small as independent claim | Expand as mechanism paper, explicitly bounded |
| On-policy Stability Atlas | Good descriptive atlas | Needs intervention/fairness framing and relation to output control | Expand as stability-map paper |
| GVF Question Design | Useful redesign diagnostic | Needs downstream usefulness metric and question taxonomy | Expand as GVF design-method paper |
| Nonstationary Bandit | Minimal sanity check | Too shallow for final, but can be independent negative/sanity study | Expand honestly or mark as not submission-grade |
| Streaming Representation | Weak auxiliary result | Auxiliary target not sufficiently coupled to representation | Expand as negative auxiliary-task design study |

## Correction To Previous Integrated Reframing

Integrated proposals are useful additions, but they do not replace independent proposal
reports. The canonical deliverable now requires full standalone treatment for every
proposal folder under `final/reports/proposals/`.

## Immediate Revision Plan

1. Replace short `report.md` files with full paper-style reports.
2. Keep `proposal_template.md`, `results.md`, and `reproduction.md` as supporting files.
3. Add `critique.md` for each proposal to record multi-role reviewer objections.
4. Update the proposal index so it no longer describes `report.md` as a mini-report.
5. Add stronger experiment plans for proposals whose current evidence is insufficient.
