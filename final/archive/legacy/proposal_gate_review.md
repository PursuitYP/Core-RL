# Proposal Gate Review

Status note, later 2026-07-09: this gate review is a historical triage artifact. The current deliverable standard treats each proposal as an independent research topic with its own report, results, critique, and reproduction files under `final/reports/proposals/`. The gate labels below remain useful as evidence-strength judgments, not as permission to omit independent proposal materials.

This gate consolidates multi-role critique on 2026-07-08: Alberta Plan alignment, experimental/statistical validity, proposal pruning, and engineering/reproducibility.

## Gate Decisions

| Proposal | Gate | Decision |
|---|---|---|
| Reward-Centered Sarsa | A | Promote as the cleanest main story. Claim reward-shift robustness and value-scale stability in continuing access-control. |
| Output-Controlled TD | A | Promote as second main story after full `config_main.json` rerun. Claim feature-scale robustness and explicitly report divergence. |
| Dyna Planning Budget | B+ | Conditional third story after recovery-window rerun. Focus on model staleness and recovery tradeoffs, not generic planning speed. |
| Baird Off-policy Stability | B | Keep as supporting diagnostic for off-policy value-function risk. |
| Generate-and-Test | C+ | Do not continue as currently framed. Recovery-window rerun shows no prediction-error win; keep only as a negative diagnostic or redesign the utility/replacement mechanism. |
| TIDBD Plasticity | B- | Mechanism-only support. It adapts feature step sizes, but normalized TD remains the stronger error baseline. |
| GVF Predictive State | C | Negative result after trace-memory rerun. Trace memory solves the task; current recurrent GVF does not. Redesign before any positive GVF claim. |
| Options | C/D | Quarantine. Current Four Rooms result does not answer the reusable-subtask question. |
| Centered TD Diagnostics | Support | Merge into Reward-Centered Sarsa. |
| On-policy Stability Atlas | Support | Merge into Output-Controlled TD. |
| GVF Question Design | Support | Use only to repair GVF proposal. |
| Streaming Representation | Drop | Too vague and overlaps better plasticity/representation proposals. |
| Non-stationary Bandit | Drop | Useful sanity check, not final proposal material. |

## Immediate Fixes Required

1. Use seed-level condition summaries for final claims.
2. Redesign GVF only if pursuing a sharper predictive-state question; current trace-memory rerun makes it a negative result, not a promotion candidate.
3. Keep final report to two main studies unless Dyna is needed as a compact third planning story.
4. Preserve result provenance with `config_used.json`, manifest package versions, and exact command.
5. Treat Generate-and-Test as a failed current design unless a sharper recovery or feature-survival metric motivates a redesign.

## Alternative Directions Worth Keeping

- Adaptive timescale prediction under delay change.
- GVF predictive state with verifiable memory.
- Continual Dyna with model aging, decay, or stale-error prioritization.
- Off-policy GVF stability under behavior drift.
