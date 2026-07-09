# Experiment Plan: Predictive State Plasticity

## Minimum Credible Experiment

1. Redesign GVF cumulants so one question predicts the hidden cue-relevant future event.
2. Add feature-cue correlation diagnostics to the T-maze run.
3. Compare raw, trace memory, oracle, fixed useful GVF, and fixed useless GVF.
4. Require that the useful GVF improves trial accuracy over raw/history baselines.

## Strong Experiment

Add limited feature capacity and phase changes:

- corridor length changes from `8` to `24`;
- cue semantics reverse;
- feature budget remains fixed.

Then evaluate generate-and-test replacement and TIDBD step-size adaptation.

## Baselines And Ablations

- Raw observation.
- Short history.
- Fixed trace memory.
- Oracle cue memory.
- Fixed GVF questions selected by hand.
- GVF questions chosen by prediction error only.
- GVF/trace features chosen by downstream utility.
- TIDBD with fixed features.
- Generate-and-test plus TIDBD.

## Figures

- Figure 1: trial accuracy by state construction.
- Figure 2: feature-cue correlation by maze position.
- Figure 3: GVF predictions by position and cue.
- Figure 4: recovery after corridor-length or cue-semantics change.
- Figure 5: feature replacement timeline and per-feature alpha trajectories.

## Promotion Criteria

Promote only if learned predictive features beat raw/history and approach trace-memory performance on at least one nontrivial phase, while retaining interpretable evidence that they encode the hidden variable. If not, publish as a negative paper about why useful prediction selection is hard.
