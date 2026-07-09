# Iterative Research Record

This document records the live research process. It is not a polished final report. Its job is
to make every major design change, criticism, experiment result, and revision auditable while
the project evolves.

## Working Standard

The project should be treated as a small research paper, not as a collection of demos. A toy
environment is acceptable for a mechanism introduction or smoke test, but the main claim must
be tested in a larger or more canonical Core RL setting with meaningful baselines and
condition-specific analysis.

Update on 2026-07-09: the working standard is now stricter. Each proposal is treated as an
independent research topic, even when its conclusion is negative, diagnostic, or not
submission-grade as-is. A portfolio overview cannot substitute for per-proposal research
reports. Every proposal folder now needs a template, paper-style report, result summary,
critique log, and reproduction path.

Each proposal must keep answering:

1. What focused RL question is being tested?
2. Why does the question matter for continual agents under the Alberta Plan?
3. What setting creates real pressure on the mechanism?
4. Which baseline or ablation isolates the mechanism?
5. What metric would change our belief?
6. What negative result would still teach something?

## Research Tiers

The project now uses a two-tier experimental structure.

Tier 1: introduction and smoke tests.

- Small environments: two-loop MDP, 19-state random walk, short T-maze, simple trace
  conditioning, small Four Rooms.
- Purpose: catch implementation errors, demonstrate the mechanism, and produce quick
  sanity checks.
- Not enough for final claims.

Tier 2: main research experiments.

- Larger or canonical environments: access-control queue, tile-coded large random walk,
  longer aliased T-maze, tight-budget nonstationary trace conditioning, SMDP Four Rooms,
  nonstationary sensor prediction, Baird's star, changing Dyna gridworld.
- Purpose: evaluate whether the mechanism still matters when the setting has scale,
  partial observability, nonstationarity, temporal abstraction, off-policy instability, or
  model staleness.
- Final analysis must report per-condition mean and uncertainty rather than algorithm-only
  averages.

## Critique Round 1: Scope and Scientific Taste

Strict reviewer criticism:

- The proposal set is Core RL aligned but too broad for equal-depth final reporting.
- The strongest questions are invariance, output-change control, predictive state,
  plasticity, and computation allocation.
- Weak danger: turning the project into "method X got a higher curve."

Revision:

- Keep 8 proposal dossiers, but make the final story narrower.
- Primary spine candidates: Reward-Centered Sarsa, Output-Controlled TD, GVF Predictive
  State, Generate-and-Test or TIDBD plasticity.
- Options, Baird, and Dyna remain valuable, but they should support the broader argument
  unless their upgraded experiments become strong enough.

## Critique Round 2: Experimental Adequacy

Strict reviewer criticism:

- Current configs and runs were not aligned tightly enough.
- Summary statistics averaged across algorithms and treatment conditions.
- Plots grouped only by algorithm and hid reward shifts, feature scales, phases, and
  treatment variables.
- Several metrics were wrong for final analysis: T-maze correctness was logged on
  non-decision steps, options used decision steps instead of environment steps, and
  generate-and-test plotted reward/weight norm rather than switch recovery.
- Statistical evidence was too thin.

Revision:

- Add evaluation-grade per-condition summaries and grouped plots.
- Treat toy/minimal runs as preliminary.
- Upgrade main environments and metrics before interpreting main results.
- Record exact commands, condition grids, and result paths for each main run.

## User Direction Incorporated

The user explicitly required continual improvement, not a frozen plan. The project must
allow small metric and environment corrections to propagate back into higher-level proposal
design. The plan, proposal definitions, experiment details, and report materials can all be
changed when results show a weak or misleading design.

Current design implication:

- Do not defend weak initial proposal details.
- Improve or replace them when the RL question becomes clearer.
- Richer environments are required for main claims; toy environments remain as examples.

## Critique Round 10: Independent Proposal Standard Correction

User correction:

- New and existing proposals must remain independent research topics.
- Larger integrated proposals are allowed, but each must be its own independent study with
  a richer internal set of related questions.
- The task is not to collapse everything into one overview paper.

Revision:

- Expanded all 13 canonical proposal `report.md` files into standalone paper-style reports.
- Added `proposal_template.md` for all 13 canonical proposals.
- Added `critique.md` for all 13 canonical proposals.
- Created three larger independent Core RL proposals under
  `final/reports/integrated/`.
- Marked the off-policy GVF integrated topic as deferred/supporting so the new large-topic
  set stays at three.

New experiment:

- Implemented and ran `scale_invariant_continuing_control`.
- Result path:
  `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`.
- Key finding: reward centering alone fails under large feature scales, normalized Sarsa
  alone remains reward-shift sensitive, and normalized reward-centered/differential Sarsa
  variants are robust across the tested reward-shift by feature-scale grid.

Remaining issue:

- The overview paper still reflects an earlier two-main-study story and should be treated
  as context until rewritten around independent proposal deliverables.

## Proposal-Level Revisions

### P1 Reward-Centered Continuing Sarsa

Initial version:

- Two-loop continuing MDP with constant reward shifts.

Criticism:

- Too toy for final analysis.
- Performance must be unshifted reward and policy/update invariance, not shifted return.

Revision:

- Main experiment moves to the access-control queue, a canonical continuing average-reward
  control task.
- Compare discounted Sarsa, reward-centered Sarsa, and differential Sarsa across reward
  shifts.
- Report unshifted average reward, accept rate, high-priority acceptance, Q norm, TD-error
  scale, and policy probes.

### P2 Output-Controlled TD

Initial version:

- 19-state random walk with scaled one-hot features.

Criticism:

- One-hot scale sensitivity is a useful introduction but too easy.
- Need stability regions and uneven-feature failures.

Revision:

- Main experiment uses a larger tile-coded random walk with overlapping features.
- Compare fixed TD, normalized TD, trace-normalized TD, and true-online TD(lambda).
- Add alpha-by-scale stability analysis and divergence time.

### P3 GVF Predictive State

Initial version:

- Short T-maze with raw observation, history, and GVF feature variants.

Criticism:

- A GVF that is only a function of the current aliased observation cannot fairly be expected
  to remember the cue.
- Correctness must be measured only at trial end.

Revision:

- Main experiment uses a longer T-maze where short history cannot solve the problem.
- Add recurrent GVF predictive state and oracle cue-memory ceiling.
- Log trial-end correctness, GVF value trajectories, terminal cue, and junction action.

### P4 Generate-and-Test Trace Features

Initial version:

- Fixed trace bank and utility replacement in delay-shift prediction.

Criticism:

- Utility replacement is underdefined and broad fixed banks may already contain both delays.

Revision:

- Main experiment should use a tight trace budget.
- Add random replacement and oracle trace-bank baselines.
- Report switch-window absolute error, recovery time, active rho values, and replacements.

### P5 Options as Reusable Subtasks

Initial version:

- Doorway options in Four Rooms, one row per option decision.

Criticism:

- Environment-step accounting was wrong for option duration.
- Need SMDP discounting and goal-change frequency analysis.

Revision:

- Log real environment steps, option duration, option use, goal switches, and recovery after
  switches.
- Compare primitive actions, short doorway options, and long committed doorway options.

### P6 TIDBD Plasticity

Initial version:

- Nonstationary sensor stream with fixed TD, normalized TD, and TIDBD-lite.

Criticism:

- Mean step-size is insufficient evidence.
- "TIDBD-lite" must not be oversold as canonical TIDBD.

Revision:

- Log group-wise feature step-sizes for old-relevant and new-relevant features.
- Report post-switch recovery, not just overall average error.

### P7 Baird Off-policy Stability

Initial version:

- Baird-style off-policy TD vs TDC.

Criticism:

- Must be canonical before making claims.
- Need longer runs, alpha sweep, and stability regions.

Revision:

- Verify feature/action/importance-ratio setup.
- Use Baird as a theoretical diagnostic unless canonical behavior is demonstrated.

### P8 Dyna Planning Budget

Initial version:

- Stationary continuing gridworld with 0/1/5 planning backups.

Criticism:

- "More planning learns faster" is too shallow in a stationary deterministic grid.

Revision:

- Add a phase change in goal/hazard layout.
- Report sample efficiency before change, recovery after change, model staleness, and backup
  budget.

## Current Implementation Changes

- Added `AccessControlQueue` for main reward-centering experiments.
- Added `TileRandomWalkPrediction` for larger output-control experiments.
- Added phase changes to `ContinuingGridworld` for Dyna model-staleness analysis.
- Fixed T-maze correctness logging so non-terminal steps do not count as incorrect actions.
- Stabilized epsilon-greedy and normalized Sarsa control when feature augmentation creates
  large or non-finite values.

## Result Status Policy

The project now distinguishes result levels explicitly.

Preliminary:

- All `*_minimal` results.
- Toy/smoke results from two-loop MDP, 19-state one-hot random walk, short T-maze, and early
  Four Rooms option prototypes.
- These can be used to explain the mechanism or implementation debugging, but not as final
  evidence for the main claims.

Obsolete:

- Any `*_main` result produced before the main-environment upgrade and per-condition summary
  change.
- These runs may have `suite: main` in the manifest but lack the current fields such as
  `environment=access_control`, `representation=tile`, `model_mode`, or corrected
  trial-end metrics.

Current candidate main evidence:

- Only runs produced after the `config_main.json` files were added and after
  `condition_summary.json` became part of every result directory.
- These must still be checked proposal by proposal before final reporting.

## Critique Round 3: Synchronization and Project Hygiene

Strict reviewer criticism:

- Research narrative, implementation, and existing results were no longer synchronized.
- Final-facing documents still referred to older minimal results as current evidence.
- `summary.json` global aggregates are not evaluation-grade.
- Code files were becoming too large, making ongoing research iteration harder.

Revision:

- Added `config_main.json` for primary proposal workspaces.
- Marked old minimal and old main results as preliminary or obsolete.
- Added `condition_summary.json` per run to support condition-specific analysis.
- Planned a code organization pass: keep reusable agents/core utilities shared, but split
  proposal environments and proposal experiments into clearer modules once current runs are
  complete.

## Project Hygiene Revision

User criticism:

- Files were becoming too large.
- Proposals should remain independently understandable, with separate environments, configs,
  metrics, and reports when possible.
- Code and documents should be clearly separated.

Revision:

- Split `experiments/alberta_core_rl/proposals.py` into a thin registry/runner plus
  proposal-specific modules under `experiments/alberta_core_rl/studies/`.
- Current file sizes: proposal implementation modules are under 250 lines; `envs.py` is
  474 lines and should be split if more environments are added.
- Added `experiments/alberta_core_rl/scripts/summarize_results.py` for reproducible
  condition-level result audits.
- Added `experiments/alberta_core_rl/scripts/run_cpu_task.sh` for CPU cluster runs on
  `safethm_cpu_task` or `safer2ai_cpu_task`.

Cluster note:

- For longer sweeps, use CPU task queues instead of long interactive local runs.
- Supported partitions in the project script:
  `safethm_cpu_task` in namespace `ailab-safethm`, and `safer2ai_cpu_task` in namespace
  `ailab-safer2ai`.
- Based on `verl` project notes, rjob runs should use gpfs-mounted project paths and should
  not depend on `/data`.

## Main-Pilot Audit Revision

The current main-pilot audit is recorded in `draft/main_pilot_result_audit.md`.

Key decision:

- Promote Reward-Centered Sarsa and Output-Controlled TD as strongest main stories.
- Treat GVF and plasticity proposals as active research revisions.
- Keep Options, Baird, and Dyna as supporting diagnostics unless further iterations make
  them strong enough for the final report.

## Next Required Records

- Add per-condition summary artifacts after each main run.
- Add exact command records to proposal workspaces.
- Update proposal dossiers after each experiment iteration.
- Distinguish preliminary, revised, and final-facing results.

## Critique Round 4: Proposal Gate and Reproducibility

Multi-role critique:

- Alberta Plan alignment review: Reward-Centered Sarsa and Output-Controlled TD are the only
  current A-grade main stories. GVF and Options should not be defended as positive results in
  their current form.
- Experimental-design review: final claims must use per-seed summaries. File-order tail
  means can overweight the last seed and are not acceptable final statistics.
- Proposal-pruning review: use two main studies, with Dyna as a possible third only after a
  recovery-window redesign. Merge plasticity diagnostics rather than keeping Generate-and-Test
  and TIDBD as separate main stories.
- Engineering review: run artifacts need `config_used.json`, exact command, package versions,
  and clear result indexing. The Output-Controlled candidate run does not match its current
  `config_main.json` and must be rerun or marked conditional.

Revision:

- Added seed-aware `*_seed_tail` summaries to `condition_summary.json`.
- Added `experiments/alberta_core_rl/scripts/rebuild_condition_summary.py` for old result
  directories.
- Added `config_used.json` and richer manifest provenance for new runs.
- Added `.gitignore` for caches and generated result outputs.
- Added final-facing `result_index.md` and `proposal_gate_review.md`.
- Marked old proposal dossiers as legacy/currently gated where needed.
- Reran Reward-Centered Sarsa and Output-Controlled TD with clean conda environment
  settings: `PYTHONNOUSERSITE=1` and `MPLCONFIGDIR` set to the project cache.
- Clean main runs:
  `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main` and
  `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`.

## Critique Round 5: Recovery Windows and Proposal Triage

Reviewer criticism:

- Nonstationary proposals cannot be judged by final tail averages alone. They need
  post-change recovery windows.
- Dyna should not claim "planning helps" unless it also accounts for stale learned models.
- Generate-and-Test should not be defended just because it moves trace parameters closer to
  a target timescale; the prediction error must improve.
- TIDBD-lite should not be oversold as canonical TIDBD or as a performance win when
  normalized TD has lower error.

Revision:

- Added `recovery_window` and `steps_since_switch` fields to Dyna, Generate-and-Test, and
  TIDBD result rows.
- Added `recovery_window` to condition-level summaries.
- Fixed a one-step logging mismatch in stream phase/delay records by reading current
  phase/delay before calling `step()`.
- Reran recovery-window main experiments:
  `experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main`,
  `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`, and
  `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`.

Current interpretation:

- Dyna is still useful and may be a compact third story. Planning improves the pre-change
  reward, but keeping the old model gives high stale-backup rates after the change. The
  proper claim is a tradeoff between planning budget, model staleness, and recovery.
- Generate-and-Test is downgraded. It improves closest-rho distance but does not improve
  prediction error over fixed or random baselines in the current setting.
- TIDBD remains supporting. It shows sensible per-feature step-size adaptation after the
  switch, especially for newly relevant features, but normalized TD remains the better error
  baseline.

Decision:

- Keep the final spine as Reward-Centered Sarsa and Output-Controlled TD.
- Add Dyna only if the final report needs a third Alberta Plan pillar on learned models and
  computation.
- Do not spend more time on the current Generate-and-Test design unless it is reframed as a
  sharper adaptive-timescale discovery study.

## Critique Round 6: GVF Predictive-State Failure Localization

Reviewer criticism:

- The earlier GVF result could not distinguish "the task needs memory" from "the current
  GVF construction is not useful state."
- A fair negative result needs a cheap non-GVF memory baseline and interpretable trajectory
  diagnostics.

Revision:

- Added `trace_memory` to the long T-maze GVF proposal.
- Logged cue traces and maze position for trajectory analysis.
- Generated a position-level figure:
  `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main/figures/gvf_trace_by_position.png`.
- Reran the main GVF config:
  `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`.

Current interpretation:

- Oracle and trace memory solve the task, with seed-aware tail trial accuracy around `0.94`.
- Raw observation, short history, and recurrent GVF remain near chance.
- This is not evidence that GVFs are useless. It is evidence that the current recurrent-GVF
  state design does not carry the cue information needed for control.

Decision:

- Keep GVF as a negative result/redesign target.
- Do not promote it to the final main story unless a new GVF question design produces a
  clear positive result quickly.
