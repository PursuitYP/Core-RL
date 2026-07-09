# Evidence Map: Predictive State Plasticity

## Existing Evidence

This large proposal builds on four completed component studies:

- GVF Predictive State: `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`
- GVF Question Design: `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main`
- Generate-and-Test Features: `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`
- TIDBD-Lite Plasticity: `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`
- Predictive State Plasticity first-gate pilot: `experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main`

## What This Evidence Supports

- Partial observability is real: raw/history state fails in the long T-maze.
- The task is solvable without deep networks: trace memory and oracle memory solve it.
- The current recurrent GVF state does not carry enough cue information.
- Easy GVF questions are not necessarily useful.
- Generate-and-test can move feature parameters but may not improve prediction error.
- TIDBD-lite adapts feature step sizes but does not beat normalized TD on error.
- Redesigned cue-GVF carries a positive cue-alignment margin but still fails to improve T-maze control accuracy.

## What It Does Not Yet Support

The current evidence does not show a positive learned predictive-state/plasticity system. It identifies design constraints and failure modes. In particular, weak hidden-cue signal is not enough; the learned feature must be strong enough and usable enough for control.

## Required New Experiments

1. Stronger GVF cue-decodability probe and explicit linear readout.
2. Better fixed useful-GVF question set tied to hidden cue.
3. Corridor-length and cue-semantics phase changes.
4. Limited feature-budget generate-and-test after useful GVF questions are validated.
5. Canonical TIDBD or AutoStep comparison.
6. Downstream control ablation for each learned feature group.

## Promotion Rule

Promote only if learned predictive features improve downstream trial accuracy over raw and short-history baselines and approach trace-memory performance, with interpretable evidence that they encode the hidden cue.
