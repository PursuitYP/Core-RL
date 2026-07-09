# Critique Round 8: Integrated Reframing After Independent Proposal Pass

Date: 2026-07-09

This critique round responds to the user's requirement that the work should not stop at
mini-reports and should repeatedly challenge whether each proposal is meaningful. Three
independent reviewer passes converged on the same diagnosis: the project has many runnable
experiments, but the strongest academic shape is not a flat list of 13 equal proposals.

## Shared Diagnosis

The portfolio should be organized around larger questions about long-lived agents:

1. What invariances must a streaming value learner maintain?
2. How should learned models be trusted or aged after nonstationarity?
3. When are predictions useful as state rather than merely accurate?
4. Which off-policy/background predictions are stable enough to support GVF-style agents?
5. When do options or generated features pay their real environment-step and computation
   cost?

The current 13 proposal reports remain useful, but many are best interpreted as:

- mechanism evidence,
- negative evidence,
- redesign gates,
- or sanity checks.

## Promotion Decisions After Review

| Proposal | Decision | Rationale |
|---|---|---|
| Reward-Centered Sarsa | Promote | Access-control queue and reward-shift invariance form a strong continuing-control story. |
| Output-Controlled TD | Promote | Tile-coded scale-stability result strongly matches intentional-update motivation. |
| Dyna Planning Budget | Conditional promote | Strong Alberta planning angle if reframed around stale model knowledge, not just faster planning. |
| GVF Predictive State | Redesign/negative | Trace/oracle baselines solve; current GVF state does not. |
| Generate-and-Test Features | Negative/redesign | Plausible timescale adaptation did not improve prediction error. |
| TIDBD Plasticity | Supporting | Shows step-size plasticity but not a performance win over normalized TD. |
| Baird Off-policy Stability | Supporting | Valuable caution for off-policy GVFs; too narrow alone. |
| Doorway Options | Quarantine/redesign | Options are used but do not help under real-step accounting. |
| Centered TD Diagnostics | Merge | Mechanism appendix for reward centering. |
| On-policy Stability Atlas | Merge | Mechanism appendix for output control. |
| GVF Question Design | Merge | Redesign aid for GVF predictive state. |
| Nonstationary Bandit | Drop/sanity | Too shallow for final Core RL proposal. |
| Streaming Representation | Drop/redesign | Auxiliary prediction is not tightly coupled to useful representation. |

## New Integrated Proposal Set

Four larger proposals were created under `final/reports/integrated/`:

1. `scale_invariant_continuing_control`
2. `continual_dyna_model_aging`
3. `predictive_state_plasticity`
4. `offpolicy_gvf_stability_under_drift`

These are not completed evidence yet. They are stronger research candidates derived from
the critique of existing results and from the Alberta Plan literature.

## Ten-Perspective Review Checklist

Future revisions must check each promoted proposal against these perspectives:

1. Alberta Plan alignment: ordinary experience, temporal uniformity, value functions,
   planning, GVFs, or average reward.
2. Course rubric: focused RL question, setting, comparison, metric, reproducibility.
3. Sutton-style continuing-agent critique: no hidden episodic reset or shifted-return
   artifact.
4. Experimental statistician: condition-wise uncertainty and enough seeds for the claim.
5. Baseline fairness: cheap baselines and oracle ceilings are included where relevant.
6. Negative-result skeptic: failure modes are interpreted honestly.
7. Reproducibility engineer: exact config, command, result path, and schema are recorded.
8. Mechanism reviewer: plots explain why, not only whether, a curve is higher.
9. Scope reviewer: the proposal is neither too toy nor too broad to finish.
10. Writing reviewer: the story reads as a question-to-evidence argument, not a method list.

## Required Revisions From This Round

- Add `proposal_template.md` for every canonical proposal.
- Mark integrated proposals as research candidates, not completed results.
- Update canonical proposal index to include template files and integrated proposal links.
- Strengthen promoted reports with a full-paper narrative: motivation, threat model,
  related work, method, experiment, analysis, limitations, and next experiment.
- Strengthen negative reports by stating what was falsified and what was not.
- Remove language implying old legacy reports are final evidence.
