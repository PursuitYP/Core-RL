# Live Plan: Alberta Plan Core RL Course Project

This is a working plan, not a frozen specification. The proposal set should be revised as
experiments and literature review reveal clearer questions, dead ends, or better small
testbeds. The project should optimize for clear RL questions, reproducibility, honest
interpretation, and connection to the Alberta Plan rather than for the largest experiment.

## Current Direction

Build a lightweight, CPU-only, no-replay, no-deep-network experiment package for a live
portfolio of Core RL proposals. The initial implementation covers ten proposal directions:

1. Reward-Centered Continuing Sarsa.
2. Output-Controlled TD.
3. Useful GVFs as Agent State.
4. Online Feature Generate-and-Test.
5. Options as Reusable Subtasks.
6. Streaming Representation Without Replay.
7. Centered TD Diagnostics.
8. Non-stationary Bandit as a Minimal Continual Agent.
9. On-policy Function Approximation Stability Atlas.
10. GVF Question Design and Usefulness.

The first five are grounded in `resources/class-on-files/alberta_plan_rl_conversation.md`. The later
proposals are current additions based on course materials, literature review, and ongoing
refinement. The first implementation was intentionally small, but it is not sufficient for
final claims. The project now separates introductory/smoke settings from upgraded main
research settings.

After multi-role critique and clean reruns, the final report should prioritize two main
studies:

1. Reward centering in continuing Sarsa.
2. Feature-scale robustness in streaming TD.

The only conditional third story is Dyna planning budget/model staleness. Post-change
recovery metrics have been added, so the remaining question is whether the final report
needs a compact planning pillar.

The following are supporting, redesign, negative-result, or dropped topics rather than
primary proposals: GVF predictive state, generate-and-test, TIDBD plasticity, Baird
off-policy stability, options, centered TD diagnostics, non-stationary bandit, on-policy
stability atlas, streaming representation diagnostics, and GVF question design. Current gate
decisions are in `final/archive/legacy/proposal_gate_review.md`.

## Main Research Upgrade

Toy experiments remain useful for sanity checks and introduction figures, but final analysis
must use richer Core RL settings:

- Reward-Centered Sarsa: from two-loop MDP to access-control queue.
- Output-Controlled TD: from 19-state one-hot random walk to larger tile-coded random walk.
- GVF Predictive State: from short T-maze to longer aliased T-maze with recurrent GVFs and
  oracle cue-memory ceiling.
- Generate-and-Test: from broad trace bank to tight feature-budget delay-shift prediction
  with random and oracle baselines.
- Options: from one-row-per-option logging to SMDP Four Rooms with real environment-step
  accounting and goal-change analysis.
- TIDBD: from mean step-size logging to group-wise old/new feature step-size trajectories.
- Baird: from Baird-style diagnostic to canonical setup and alpha-sweep stability check.
- Dyna: from stationary gridworld to changed goal/hazard layout with model-staleness
  analysis.

The final paper-style report should not give all proposals equal depth. It should use the
two clean main stories as the spine, with other proposals used as diagnostics, appendices, or
negative-result analyses.

## Implementation Layout

- Shared code: `experiments/alberta_core_rl/`
- Proposal-specific configs and notes: `experiments/alberta_core_rl/configs/<proposal>/`
- Proposal-specific results: `experiments/alberta_core_rl/results/<proposal>/`
- Draft notes and evolving analysis: `draft/`
- Final-facing report, poster, and reproduction notes: `final/`

Each proposal should have a config, exact command, result directory, and short local notes.
Shared code is preferred when the environment or agent is reusable; proposal-specific code
should be added only when it prevents confusion or makes independent execution clearer.

## Revision Policy

- If a proposal has no baseline signal after a small smoke/main run, simplify the environment
  first, then simplify the algorithm, then demote the proposal to conceptual analysis.
- Do not blind grid search. Use small sweeps that answer a mechanism question.
- Keep searching during implementation when a result changes the question or exposes a gap.
- Keep all imported course/reference materials unchanged.

## Core Constraints

- No replay buffer.
- No deep network.
- Streaming updates from the current experience.
- Small, interpretable, local CPU experiments.
- Every report/poster starts with a focused RL question.
