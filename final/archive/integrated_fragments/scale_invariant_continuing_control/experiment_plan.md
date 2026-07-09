# Experiment Plan: Scale-Invariant Continuing Control

## Minimum Credible Experiment

1. Extend Reward-Centered Sarsa to support normalized action-value updates.
2. Add feature scaling to the access-control representation.
3. Run reward shifts by feature scales by algorithms with at least 10 seeds.
4. Plot unshifted reward and Q norm in the same condition grid.
5. Report divergence and policy-probe invariance.

## Strong Experiment

Add a midstream intervention:

- first half: reward shift `0`, feature scale `1`;
- second half: reward shift `8` or feature scale `100`;
- no reset and no retuning.

Primary recovery metric:

- steps until rolling unshifted reward returns to 90 percent of pre-change baseline;
- steps until Q norm returns to a stable range.

## Baselines And Ablations

- Discounted Sarsa: shows raw sensitivity.
- Reward-centered Sarsa: isolates reward-origin correction.
- Normalized Sarsa: isolates feature-scale correction.
- Normalized reward-centered Sarsa: tests composition.
- Differential Sarsa: average-reward baseline.
- No-average-update ablation: freezes the reward baseline to test estimator lag.

## Figures

- Figure 1: reward-shift by algorithm curve for unshifted reward.
- Figure 2: reward-shift by algorithm curve for Q norm.
- Figure 3: alpha/feature-scale stability atlas.
- Figure 4: combined reward-shift x feature-scale heatmap.
- Figure 5: midstream change recovery curves.

## Promotion Criteria

Promote to a main paper only if the combined method improves invariance on both dimensions without hiding a large reward or recovery penalty. If it only reproduces the two separate effects, keep it as a synthesis/extension rather than the final main claim.
