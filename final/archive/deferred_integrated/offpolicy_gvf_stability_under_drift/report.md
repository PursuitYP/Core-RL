# Off-Policy GVF Stability Under Behavior Drift

Status: deferred archive note, not a current final-facing proposal report. This idea remains scientifically relevant, but it has not yet been promoted to `final/reports/` because it lacks a completed implementation, reproducible result directory, and seed-aware analysis under the current project structure. Use this file as a design fragment only.

## Abstract

The Alberta Plan imagines agents learning many predictions in the background from ordinary experience. Many such predictions are naturally off-policy: they ask what would happen under some other policy, option, or continuation condition. Off-policy TD with function approximation is structurally unstable in classic counterexamples. This proposal studies a small but important safety condition for predictive knowledge: when behavior drifts, which linear TD corrections keep background GVFs stable?

## Motivation

GVFs and Horde-style architectures are compelling because they allow an agent to learn many questions in parallel. But adding many background predictions is not automatically benign. If their learning updates are off-policy and unstable, the predictive layer can corrupt the agent's representation or consume computation. Baird's counterexample is not merely an old toy; it is a warning about the deadly triad that any streaming prediction architecture must answer.

The existing Baird proposal demonstrates a stability diagnostic. This integrated proposal connects that diagnostic to GVFs and behavior drift, making it more directly relevant to Alberta-style predictive knowledge.

## Research Question

Which lightweight linear update rules keep off-policy GVF predictions stable under changing behavior-policy mismatch?

Subquestions:

- How does the stability region change as behavior-target mismatch increases?
- Does output normalization help or merely slow divergence?
- Do centered TD errors interact safely with emphatic or gradient-corrected updates?
- Can behavior drift create transient instability even when fixed-policy settings appear stable?

## Related Work

Baird's counterexample demonstrates off-policy TD divergence under linear function approximation. Gradient TD/TDC and emphatic TD provide stability-oriented alternatives. Horde and GVF work motivate off-policy background predictions. Recent centered emphatic TD work suggests that centering and off-policy stability interact nontrivially.

Useful local sources:

- `resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`
- `resources/alberta_plan_related/regularized_centered_emphatic_td_2605.04100.pdf`
- `resources/alberta_plan_related/bellman_error_centering_2502.03104.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

External anchors:

- Emphatic TD: https://arxiv.org/abs/1503.04269
- Emphatic TD summary: https://arxiv.org/abs/1507.01569

## Method

The project uses two testbeds:

1. Canonical Baird-style linear prediction.
2. A small GVF stream in which cumulants and discounts define background predictions and the target policy differs from the behavior policy.

Algorithms:

- Off-policy semi-gradient TD.
- TDC or GTD-style gradient correction.
- Emphatic TD.
- Normalized off-policy TD diagnostic.
- Centered variants only after the uncentered stability behavior is verified.

Behavior drift:

- fixed mild mismatch,
- fixed severe mismatch,
- scheduled drift from mild to severe,
- oscillating mismatch.

## Experimental Design

Metrics:

- weight norm and divergence time,
- value error or MSPBE proxy,
- follow-on trace scale for emphatic variants,
- prediction TD error,
- stability-region heatmaps over alpha and mismatch,
- recovery after mismatch changes.

Final sweep:

- alphas `0.001, 0.003, 0.005, 0.01, 0.02, 0.05`;
- mismatch levels from near-on-policy to severe;
- seeds `0-19`;
- at least `20000` streaming steps for stability diagnostics.

## Expected Results And Failure Modes

Expected pattern: ordinary off-policy TD should diverge in severe mismatch settings. TDC and emphatic variants should enlarge the stability region but may require smaller step sizes or suffer high-variance traces. Normalization may delay divergence without fixing the projected update geometry.

Failure modes:

- Implementation details of Baird's example can invalidate claims.
- Emphatic traces may become high variance and make the practical result ambiguous.
- Centering may interact with off-policy correction in unsafe ways; it should be reported cautiously.

## Interpretation Standard

This proposal is a diagnostic stability study, not a performance benchmark. A useful conclusion maps safe and unsafe regimes for background predictions. The result should make future GVF proposals more disciplined by requiring stability checks before adding many off-policy demons.

## Current Evidence From Existing Runs

Existing Baird runs show off-policy TD weight-norm growth while TDC is stable at smaller alphas and fails at larger alpha. That supports keeping off-policy stability in the portfolio, but a GVF drift test remains to be implemented before this becomes a complete integrated proposal.

## Reviewer-Centered Revision Notes

Strict reviewer challenge: "Baird is too classic to be novel." Response: the novelty for this course project is the connection to streaming GVF background learning under behavior drift, plus careful stability-region diagnostics.

Strict reviewer challenge: "No control task, no reward." Response: the Alberta Plan also prioritizes value functions and predictions. Stable prediction is a prerequisite for control and planning components.
