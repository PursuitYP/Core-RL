# Results: Baird Off-policy Stability

Current result:

`experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`

Key figure:

![Weight norm by algorithm and alpha.](../../../../experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main/figures/weight_norm_by_algorithm-alpha_curve.png)

Seed-aware finding:

Off-policy TD weight norms grow rapidly. TDC is stable at alphas `0.005` and `0.01` but also fails at `0.02`.
