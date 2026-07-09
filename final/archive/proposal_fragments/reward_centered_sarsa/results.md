# Results: Reward-Centered Sarsa

Current result:

`experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main`

Key figure:

![Unshifted reward under reward shifts.](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main/figures/avg_unshifted_reward_by_algorithm-reward_shift_curve.png)

Seed-aware finding:

Reward-centered Sarsa keeps Q norm around `20-22` across reward shifts. Discounted Sarsa grows from about `60` at shift `-4` to about `345` at shift `8`.
