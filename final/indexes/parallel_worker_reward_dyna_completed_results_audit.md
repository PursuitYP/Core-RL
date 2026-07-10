# Parallel Worker Audit: Completed CPU Result Directories

Audit date: 2026-07-09

Scope: audited only these two completed result directories:

- `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended`
- `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`

No report, code, figure, or shared index files were edited.

## Reward-Centered Sarsa Sensitivity

Directory: `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended`

Question recorded in `summary.json`: "How sensitive is reward-centered continuing Sarsa to reward-rate tracking and discount choice under a no-reset reward-origin switch?"

### Artifact Completeness

Standard artifacts are complete.

- Present: `config_used.json`, `summary.json`, `condition_summary.json`, `metrics.csv`, plus `manifest.json`.
- `config_used.json` records command `experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/reward_centered_sarsa_sensitivity/config_extended.json`.
- `metrics.csv` has 8,112,150 data rows plus header.
- `condition_summary.json` has 1,575 condition groups.
- `condition_summary_version` is `seed_tail_v1`.
- Elapsed runtime recorded: 5,380.18 sec.

### Condition Dimensions And Evidence Scale

Evidence scale is strong for the intended CPU sweep: 10 seeds, 20,000 steps per seed, all 1,575 condition groups report `n_seeds = 10`.

Condition dimensions:

- Environment: `access_control_reward_origin_switch`.
- Algorithms: `differential_sarsa`, `discounted_sarsa`, `reward_centered_sarsa`.
- Step sizes: `alpha = {0.02, 0.05, 0.1}`.
- Reward-rate step sizes: `beta = {0.001, 0.003, 0.01, 0.03, 0.1}`.
- Discount factors: `gamma = {0.9, 0.97, 0.99, 1.0}`; `gamma=1.0` appears for differential Sarsa.
- Reward-origin switches: `up_shift`, `down_shift`, `sign_shift`; shifts include `-4.0`, `0.0`, `8.0`.
- Windows: `pre`, `post_0_250`, `post_250_500`, `post_500_1000`, `post_late`; phases 0 and 1.

### Main Numerical Findings

No divergence was recorded: global `diverged` mean/tail/max are all 0.

Overall `summary.json` scale:

- `n_rows = 8,112,150`, `n_condition_groups = 1,575`.
- Global tail means: `avg_unshifted_reward = 2.6056`, `unshifted_reward = 2.95`, `reward_bar = 10.6122`, `reward_bar_abs_error_ema = 2.4553`, `q_norm = 26.5413`.

Post-late seed-tail findings are the most useful report numbers:

- Best post-late `unshifted_reward_seed_tail.mean`: `reward_centered_sarsa`, `alpha=0.1`, `beta=0.03`, `gamma=0.99`, `sign_shift`, mean `2.6825`, CI95 `0.0939`.
- Best post-late `avg_unshifted_reward_seed_tail.mean`: `reward_centered_sarsa`, `alpha=0.05`, `beta=0.001`, `gamma=0.97`, `down_shift`, mean `2.6364`, CI95 `0.0280`.
- Close baseline: `differential_sarsa`, `alpha=0.05`, `beta=0.001`, `gamma=1.0`, `down_shift`, post-late `avg_unshifted_reward_seed_tail.mean = 2.6338`, CI95 `0.0155`.
- Discounted Sarsa is much less robust under `down_shift`; worst post-late `avg_unshifted_reward_seed_tail.mean` is `discounted_sarsa`, `alpha=0.02`, `beta=0.001`, `gamma=0.99`, `down_shift`, mean `1.5814`, CI95 `0.2210`.
- Reward-centered Sarsa is consistently high across `gamma/beta` settings in post-late windows: aggregate post-late `unshifted_reward_seed_tail.mean` is roughly `2.52-2.59` across reward-centered groups, while discounted Sarsa drops to about `2.10-2.36` depending on gamma and beta.
- Discounted Sarsa shows very large value scale under high gamma. Top post-late `q_norm_seed_tail.mean` values are all discounted Sarsa with `alpha=0.1`, `gamma=0.99`, `up_shift`, around `1339-1354`; this is not marked as divergence but should be plotted or called out as value-scale blowup.

Switch-specific best post-late `avg_unshifted_reward_seed_tail.mean`:

- `up_shift`: `reward_centered_sarsa`, `alpha=0.1`, `beta=0.03`, `gamma=0.99`, mean `2.6057`, CI95 `0.0273`.
- `down_shift`: `reward_centered_sarsa`, `alpha=0.05`, `beta=0.001`, `gamma=0.97`, mean `2.6364`, CI95 `0.0280`.
- `sign_shift`: `reward_centered_sarsa`, `alpha=0.05`, `beta=0.1`, `gamma=0.99`, mean `2.6089`, CI95 `0.0274`.

### Incorporate Into Reports And Indexes

- Replace any "pending CPU result" note for this run with "completed; standard artifacts present; 10 seeds; 8,112,150 rows; 1,575 condition groups."
- Report the question as reward-rate/discount sensitivity under a no-reset reward-origin switch, not simply an algorithm leaderboard.
- Use post-late seed-tail means with CI95 as the main evidence table.
- Include one sensitivity plot over beta/gamma, separated by algorithm and switch type.
- Include a value-scale diagnostic plot or note for discounted Sarsa `q_norm`, because the high-gamma discounted conditions produce very large Q norms without formal divergence.

### Risks, Weird Values, Plotting Needs

- `discounted_sarsa` `q_norm` reaching about `1,354` in post-late seed-tail means is the main weird value. It likely reflects discount/value-scale sensitivity rather than a run failure, but it needs a diagnostic figure.
- `reward_bar_abs_error_ema` is lower for some discounted conditions because discounted Sarsa is not solving the same reward-centered tracking problem; avoid interpreting lower tracking error alone as better control.
- Plot needs: post-late `avg_unshifted_reward` or `unshifted_reward` with CI95 by `beta/gamma`, plus a separate `q_norm` heatmap or small multiples.

## Continual Dyna Model Aging Drift

Directory: `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`

Question recorded in `summary.json`: "Does model aging remain useful when nonstationarity is gradual or stochastic rather than one abrupt switch?"

### Artifact Completeness

Standard artifacts are complete.

- Present: `config_used.json`, `summary.json`, `condition_summary.json`, `metrics.csv`, plus `manifest.json`.
- `config_used.json` records command `experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/continual_dyna_model_aging_drift/config_extended.json`.
- `metrics.csv` has 1,800,900 data rows plus header.
- `condition_summary.json` has 690 condition groups.
- `condition_summary_version` is `seed_tail_v1`.
- Elapsed runtime recorded: 7,965.97 sec.

### Condition Dimensions And Evidence Scale

Evidence scale is mostly 10 seeds, 20,000 steps per seed, but some narrow early post-switch groups have fewer than 10 seeds because gradual/stochastic switch timing does not place every seed into every recovery bin.

Condition dimensions:

- Environment: `changing_gridworld_model_aging_drift`.
- Drift modes: `abrupt`, `gradual`, `stochastic`.
- Model modes: `keep_model`, `oracle_flush`, `recency_aging`, `recency_error_gate`.
- Planning steps: `1`, `5`, `20`.
- Half-lives: `0.0`, `100.0`, `250.0`, `750.0`, `1500.0`.
- Windows: `pre`, `post_0_250`, `post_250_500`, `post_500_1000`, `post_late`; phases 0 and 1.
- Algorithm labels combine planning steps and model mode, e.g. `dyna_20_recency_error_gate`.

Seed coverage:

- 632 of 690 condition groups have `n_seeds = 10`.
- 58 groups have fewer than 10 seeds, concentrated in early post-switch windows such as `post_0_250` and `post_250_500` for gradual/stochastic settings.
- Post-late comparisons used for headline findings have `n_seeds = 10` in the inspected best/worst conditions.

### Main Numerical Findings

Overall `summary.json` scale:

- `n_rows = 1,800,900`, `n_condition_groups = 690`.
- Global tail means: `avg_reward = -0.00694`, `reward = 0.0100`, `mean_model_error = 0.02042`, `stale_backup_rate = 0.4887`, `q_norm = 18.1485`.

Best post-late `avg_reward_seed_tail.mean` by drift mode:

- Abrupt: `dyna_5_oracle_flush`, mean `0.09666`, CI95 `0.00101`, stale backup rate `0.00000`, model error `0.00000`.
- Abrupt close alternatives: `dyna_5_keep_model`, mean `0.09598`, CI95 `0.00112`, stale backup rate `0.28869`; `dyna_20_recency_error_gate`, half-life `1500`, mean `0.09501`, CI95 `0.00141`, stale backup rate `0.00056`.
- Gradual: `dyna_20_recency_error_gate`, half-life `1500`, mean `0.09536`, CI95 `0.00141`, stale backup rate `0.02092`, model error `0.01201`.
- Gradual close alternative: `dyna_20_recency_aging`, half-life `1500`, mean `0.09239`, CI95 `0.00436`.
- Stochastic: `dyna_5_keep_model`, mean `0.03370`, CI95 `0.01237`, stale backup rate `0.50431`, model error `0.01649`.
- Stochastic next-best: `dyna_20_keep_model`, mean `0.02811`, CI95 `0.01211`; `dyna_20_recency_aging`, half-life `1500`, mean `0.02495`, CI95 `0.01113`.

Post-late aggregate pattern:

- Planning depth matters strongly. Aggregate `avg_reward_seed_tail.mean` by drift/planning:
  - Abrupt: planning 1 `-0.01772`, planning 5 `0.06339`, planning 20 `0.09155`.
  - Gradual: planning 1 `-0.02145`, planning 5 `0.01760`, planning 20 `0.06365`.
  - Stochastic: planning 1 `0.01737`, planning 5 `0.01367`, planning 20 `0.01183`.
- Long half-life (`1500`) is best among recency methods in gradual and stochastic aggregates, but stochastic performance remains low and noisy.
- `oracle_flush` is a useful upper/control condition for abrupt and gradual settings, but not a realistic method for the stochastic setting.

### Incorporate Into Reports And Indexes

- Replace any "pending CPU result" note for this run with "completed; standard artifacts present; 10 seeds configured; 1,800,900 rows; 690 condition groups; early post-switch windows have partial seed coverage."
- Frame the result around the RL question: whether model-aging helps under different temporal structures of nonstationarity.
- Use post-late seed-tail `avg_reward` with CI95 as the headline metric.
- Report planning depth as a central factor: 20 planning steps helps abrupt/gradual, while stochastic drift does not benefit in the same way.
- Include `stale_backup_rate` and `mean_model_error` beside reward, because they explain why recency methods help or fail.

### Risks, Weird Values, Plotting Needs

- Early recovery windows in gradual/stochastic conditions have partial seed coverage and sometimes tiny row counts; do not use those windows for headline claims without showing coverage.
- Stochastic drift has low and noisy reward differences. The best stochastic post-late condition is `keep_model`, not a recency-aging method, so claims that model aging "remains useful" must be qualified.
- `stale_backup_rate` can be near zero for long-half-life recency methods in abrupt/gradual post-late windows but remains around `0.45-0.56` for several stochastic/keep-model comparisons; this should be plotted.
- Plot needs: faceted post-late `avg_reward` by drift mode, planning steps, model mode, and half-life; companion plots for `stale_backup_rate` and `mean_model_error`; coverage annotations for early post-switch windows.

