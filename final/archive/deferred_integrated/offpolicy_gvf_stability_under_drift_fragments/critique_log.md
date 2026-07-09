# Critique Log: Off-Policy GVF Stability Under Drift

## Round 1: Theory Reviewer

Concern: Off-policy stability claims require canonical setup.

Revision: Baird verification is a gate before any broader claim.

## Round 2: GVF Reviewer

Concern: A pure Baird report does not show why this matters for Alberta Plan predictive knowledge.

Revision: Add a small off-policy GVF stream with behavior drift.

## Round 3: Practical Reviewer

Concern: Emphatic TD may be theoretically stable but practically high variance.

Revision: Report follow-on trace scale and not only value error.

## Round 4: Centering Reviewer

Concern: Centered off-policy variants can be mathematically delicate.

Revision: Keep centered variants as exploratory after stable uncentered baselines are verified.

## Round 5: Course Reviewer

Concern: This proposal might look too theory-heavy.

Revision: Use figures that explain instability visually: weight norms, stability maps, and behavior-drift timelines.
