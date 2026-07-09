# Results: Scale-Invariant Continuing Control

Current main pilot:

`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`

Figures:

![Unshifted reward by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_avg_unshifted_reward_by_scale.png)

![Q norm by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_q_norm_by_scale.png)

![Prediction change by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_prediction_change_by_scale.png)

## Seed-Aware Finding

This integrated proposal produces a real interaction result rather than a simple merge of two old experiments.

- Fixed discounted Sarsa is reward-shift sensitive and feature-scale fragile. At feature scale `hundred`, its tail Q norm is about `1.4e7` to `3.0e7` and divergence appears in several conditions.
- Reward-centered Sarsa alone fixes reward-origin sensitivity at scale `one`, but it still fails under large uniform feature scales such as `ten` and `hundred`.
- Normalized Sarsa controls feature scale, but without reward centering it still degrades under positive reward shifts. At shift `8`, scale `one`, tail unshifted reward is about `1.45`.
- Normalized reward-centered Sarsa keeps tail unshifted reward near `2.41-2.51` across all tested reward shifts and feature scales, with zero divergence.
- Normalized differential Sarsa shows a similar robust pattern, with tail reward around `2.40-2.50` and zero divergence.

## Interpretation

The main lesson is compositional invariance. Reward centering addresses arbitrary reward origin; normalized updates address arbitrary feature scale. Each partial fix fails outside its intended dimension. The combined variants are the first current evidence that the two invariances can compose in one continuing control stream.

## Current Limitations

The run uses five seeds and `5000` steps, so it is still a pilot. A final version should include more seeds, a finer scale/shift grid, midstream reward/scale changes, and policy probe plots.
