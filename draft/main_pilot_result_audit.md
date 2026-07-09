# Main Pilot Result Audit

This audit records current main-pilot results after the main-environment upgrade. It separates
usable evidence from obsolete or failed pilot runs.

## Current Candidate Main Runs

- Reward-Centered Sarsa:
  `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main`
- Output-Controlled TD:
  `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`
- GVF Predictive State:
  `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`
- Generate-and-Test:
  `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`
- Options:
  `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`
- TIDBD Plasticity:
  `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`
- Baird:
  `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`
- Dyna:
  `experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main`

## Obsolete or Failed Main-Pilot Runs

- All `*_minimal` results are preliminary only.
- Early `*_main` runs before `condition_summary.json` and the main-environment upgrade are
  obsolete for final claims.
- `output_controlled_td/20260708T145946Z_main` is a failed pilot: the initial tile random
  walk was too sparse within the pilot budget, leaving most non-trace conditions with zero
  updates and constant RMSE.
- `output_controlled_td/20260708T150453Z_main` is superseded by the full current config run:
  it used three seeds and 2500 steps, while `config_main.json` now specifies five seeds and
  5000 steps.
- `reward_centered_sarsa/20260708T144536Z_main` and
  `output_controlled_td/20260708T152851Z_main` are superseded by clean-env reruns using
  `PYTHONNOUSERSITE=1`.
- `generate_test_features/20260708T144536Z_main`,
  `tidbd_plasticity/20260708T144651Z_main`, and
  `dyna_planning_budget/20260708T144742Z_main` are superseded by recovery-window reruns.
- `useful_gvfs_state/20260708T144536Z_main` is superseded by the trace-memory baseline
  rerun.

## Result Signals

### Reward-Centered Sarsa

Main setting: access-control queue with reward shifts.

Tail observations:

- Discounted Sarsa has strong Q-scale sensitivity: Q norm grows from about 62 at shift -4 to
  about 392 at shift +8.
- Reward-centered Sarsa and differential Sarsa keep Q norm around 20-21 across shifts.
- Unshifted average reward for reward-centered Sarsa is roughly stable and competitive across
  shifts.

Interpretation:

- This is a strong main-study candidate.
- The result supports the invariance story better than a simple "higher reward" story.

### Output-Controlled TD

Main setting: tile-coded random walk with alpha-by-scale grid.

Tail observations:

- Fixed TD is scale-sensitive. It stays finite for easy scales, but diverges in the full
  grid for `hundred`, `ten` at alpha 0.3, and several `uneven` conditions. Seed-aware tail
  RMSE reaches about `1e4` to `6e6` in those failed conditions.
- Normalized TD keeps seed-aware tail RMSE roughly in the `0.44-0.56` range across `one`,
  `ten`, `hundred`, and `uneven` scales, with zero divergence in the tested grid.
- Trace-normalized TD behaves similarly, with seed-aware tail RMSE roughly `0.49-0.56` and
  zero divergence in the tested grid.
- True-online TD(lambda), as currently implemented, is not scale-robust under large trace
  and scale conditions; it diverges under `hundred`, under `ten` at alpha 0.3, and under
  several `uneven` settings.

Interpretation:

- This is a strong main-study candidate.
- The honest claim is "normalization/output-level control stabilizes feature-scale changes";
  do not claim the current true-online implementation solves trace scaling.

### GVF Predictive State

Main setting: longer aliased T-maze.

Tail observations:

- Oracle memory and cheap trace memory solve the long T-maze. Seed-aware tail trial accuracy
  is about `0.939` for oracle and `0.944` for trace memory.
- Raw observation, short history, and recurrent GVF remain near chance: about `0.512`,
  `0.492`, and `0.502` respectively.
- The rerun adds cue-trace and maze-position logs plus a position-level trajectory figure.

Interpretation:

- This is a stronger negative result than the earlier pilot. The task is learnable with a
  simple non-deep memory trace, but the current recurrent GVF construction does not turn
  prediction into useful state.
- Do not use this as a claim against GVFs generally. Use it to motivate a better
  predictive-state design or keep it as an honest failed design.

### Generate-and-Test

Main setting: tight trace budget with delay shift.

Tail observations:

- The recovery-window rerun adds `recovery_window` and `steps_since_switch` to every row.
- Generate-test keeps closer trace timescales after the shift than fixed-tight and random
  replacement, but this does not translate into a prediction-error win.
- Post-late absolute error is about `0.0518` for generate-test, `0.0512` for fixed-tight,
  `0.0496` for random replacement, and `0.0545` for the current oracle-bank baseline.

Interpretation:

- This is not ready as a main story. The current utility/replacement mechanism should be
  treated as a failed design or redesigned around a sharper adaptive-timescale question.
- A useful redesign would need feature-survival plots and a setting where closer timescale
  selection is necessary for prediction improvement.

### Options

Main setting: larger Four Rooms, SMDP option execution, real environment-step accounting.

Tail observations:

- Primitive and option variants all have reward per environment step near the step cost.
- Options are selected about 17-19% of the time.

Interpretation:

- The current option result is weak. It may show that the agent does not learn to exploit the
  hand-coded options in this setting within the pilot budget.
- This should be supporting material unless the environment or option set is improved.

### TIDBD Plasticity

Main setting: nonstationary sensor prediction.

Tail observations:

- Normalized TD has lower absolute TD error than fixed-alpha baselines and TIDBD-lite in this
  pilot.
- TIDBD-lite increases new-feature step-size after the phase switch, from about `0.0068`
  pre-change to about `0.0093` in the late post-change window, while distractor feature
  step-size stays near `0.0068`.
- Late post-change absolute TD error is about `0.4419` for normalized TD and `0.4493` for
  TIDBD-lite.

Interpretation:

- This is a mixed result. It is useful as supporting evidence that per-feature adaptation
  changes in the expected direction, but normalized TD is currently the stronger baseline.

### Baird

Main setting: Baird-style off-policy TD vs TDC with alpha sweep.

Tail observations:

- Off-policy TD has rapidly growing weight norms.
- TDC is stable for alpha 0.005 and 0.01 but not for alpha 0.02.

Interpretation:

- Strong supporting diagnostic for off-policy instability.
- Keep claims cautious until canonical Baird details are fully verified.

### Dyna

Main setting: changing continuing gridworld with keep-model vs flush-on-change.

Tail observations:

- Planning helps before the phase change.
- After the phase change, stale backup rate is high when the old model is kept: late
  post-change stale backup rate is about `0.844` for one planning backup and `0.705` for
  five planning backups.
- Flush-on-change removes stale backups but does not automatically solve recovery. With five
  planning backups, late post-change average reward is about `-0.0220` for flush-on-change
  and `-0.0270` for keep-model; no-planning late reward is around `-0.0175` to `-0.0211`
  depending on the matched model-mode label.

Interpretation:

- Useful supporting result for the computation/model-staleness story.
- Good conditional third story if framed as a tradeoff between sample efficiency and stale
  model harm under nonstationary continuing control.

## Priority Revisions

1. Promote Reward-Centered Sarsa and Output-Controlled TD as the two strongest main stories.
2. Treat GVF predictive state as a negative result unless redesigned around a sharper
   question.
3. Treat Dyna as the only plausible compact third story; otherwise keep it supporting.
4. Keep Options and Baird as supporting or quarantined diagnostics, not main stories.
5. Prepare CPU-task scripts for longer seeds/sweeps if final figures need tighter statistics.
