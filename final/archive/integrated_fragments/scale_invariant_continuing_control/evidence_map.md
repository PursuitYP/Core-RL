# Evidence Map: Scale-Invariant Continuing Control

## Existing Evidence

Dedicated main pilot:

`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`

Component studies:

- Reward-Centered Sarsa: `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main`
- Output-Controlled TD: `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`
- Centered TD Diagnostics: `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main`
- On-policy Stability Atlas: `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main`

## What This Evidence Supports

- Reward centering controls reward-origin sensitivity in continuing access-control when features are well-scaled.
- Normalized TD controls feature-scale sensitivity in prediction.
- In the combined control pilot, single mechanisms fail outside their own invariance dimension.
- Normalized reward-centered and normalized differential variants are robust across the tested reward-shift by feature-scale grid.

## What It Does Not Yet Support

- The current pilot has five seeds and `5000` steps.
- It does not yet test midstream reward-origin or feature-scale changes.
- It does not include a full gamma/beta sweep.

## Required New Experiments

1. Seeds `0-19`.
2. Midstream reward-shift changes.
3. Midstream feature-scale changes.
4. Gamma and reward-baseline step-size sweeps.
5. Policy-probe and accept-rate invariance tables.

## Promotion Rule

This is currently the strongest new large independent proposal. Promote if the longer sweep confirms that combined normalized-centered variants preserve unshifted reward, value scale, and update scale under simultaneous reward and representation changes.
