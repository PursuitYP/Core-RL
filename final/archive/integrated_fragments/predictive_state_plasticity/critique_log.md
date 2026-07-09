# Critique Log: Predictive State Plasticity

## Round 1: GVF Reviewer

Concern: The current GVF is not a fair test of predictive state if its cumulant is not tied to the hidden cue.

Revision: Add question-design diagnostics and require feature-cue correlation plots.

## Round 2: Baseline Reviewer

Concern: A learned GVF must beat cheap trace memory or at least explain when it cannot.

Revision: Trace memory and oracle memory remain mandatory baselines.

## Round 3: Scope Reviewer

Concern: GVF selection, generate-and-test, and TIDBD together may be too much for one course paper.

Revision: Use staged promotion. Fixed useful GVF is the first gate; plasticity mechanisms enter only after useful prediction is demonstrated.

## Round 4: Negative-Result Reviewer

Concern: The existing negative result may be hidden by a redesign.

Revision: Keep the negative result in the report as a boundary condition: accurate or stable predictions are insufficient without downstream usefulness.

## Round 5: Reproducibility Reviewer

Concern: Generated feature systems can become hard to reproduce.

Revision: Log every replacement event, feature parameter, utility score, and seed-specific phase recovery metric.
