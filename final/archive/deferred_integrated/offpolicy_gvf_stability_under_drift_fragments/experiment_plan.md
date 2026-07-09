# Experiment Plan: Off-Policy GVF Stability Under Behavior Drift

## Minimum Credible Experiment

1. Verify the canonical Baird setup and document feature/policy details.
2. Re-run off-policy TD and TDC with longer steps and alpha sweeps.
3. Add a behavior-mismatch axis and plot stability regions.
4. Report divergence time and weight norm with seed-aware summaries.

## Strong Experiment

Add a small GVF stream:

- target questions predict cumulants under a target policy;
- behavior policy drifts from near-target to far-target;
- algorithms learn continuously without replay.

## Baselines And Ablations

- Off-policy TD.
- TDC/GTD.
- Emphatic TD.
- Normalized off-policy TD.
- Centered TD only as a cautious extension.
- On-policy TD sanity baseline.

## Figures

- Figure 1: Baird weight-norm curves by algorithm.
- Figure 2: alpha-by-mismatch stability heatmap.
- Figure 3: behavior-drift recovery/divergence timeline.
- Figure 4: emphatic follow-on trace scale.
- Figure 5: GVF prediction error under behavior drift.

## Promotion Criteria

Promote if the GVF drift test reveals a clear stability boundary and at least one corrected method reliably expands that boundary. If the result stays only at canonical Baird, keep it as an appendix diagnostic.
