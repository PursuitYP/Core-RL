# Research Journal

This journal records the evolving research process for the RL Course Project. It is meant to
capture decisions, literature findings, implementation changes, experiment outcomes, and
revisions to the proposal set. The project should stay open to refinement; weak proposals
should be merged, demoted, or replaced rather than defended mechanically.

## Research Standard

This project is treated as a small academic research project, not a programming exercise.
Every proposal must answer:

1. What focused Core RL mechanism is being studied?
2. Why does that mechanism matter for long-lived streaming agents in the Alberta Plan?
3. What is the smallest environment where the mechanism appears clearly?
4. What baseline and ablation isolate the mechanism?
5. What measurement would change our belief?
6. What failure mode would still be informative?

The project should avoid:

- Reporting only "method X scored higher."
- Treating all candidate proposals as equally mature.
- Using final return as the only metric.
- Introducing deep networks, replay buffers, or large benchmark engineering.
- Blind hyperparameter search.

## Current Research Thesis

The Alberta Plan can be studied through a set of small streaming RL mechanisms:

- Reward baselines: continuing agents should not be brittle to arbitrary reward offsets.
- Output-scale updates: online TD should control prediction change, not just parameter change.
- Predictive state: learned predictions may serve as compact memory under partial observability.
- Feature utility: long-lived agents must evaluate and replace state features over time.
- Temporal abstraction: options are useful only if their subtask utility survives goal changes.
- Planning budget: a compact model can help under limited computation, but stale models can hurt.

The deeper insight is that these are all resource-allocation problems over time: what signal
to subtract, how far to update, what to remember, which feature to keep, which option/model to
use, and where to spend computation.

## Timeline and Decisions

### Initial grounding

- Read local project requirements from `RL_Course_Project.pdf`.
- Read `Proposal_Template.md`; the proposal form requires four questions: understand,
  setting/testbed, examine, and look at.
- Read `AlbertaPlan.pdf`; the key lens is ordinary experience, temporal uniformity,
  continual learning, GVFs, average reward, planning, STOMP, and Oak.
- Read `resources/class-on-files/alberta_plan_rl_conversation.md`; it already contained strong designs
  for Reward-Centered Continuing Sarsa and Output-Controlled TD, plus additional proposal
  candidates.

### Literature search and refinement

Relevant external sources were checked and summarized in `literature_notes.md`, including:

- Alberta Plan.
- Reward Centering.
- Intentional Updates for Streaming RL.
- Streaming Deep RL Finally Works.
- Squeezing More from the Stream.
- TIDBD.
- True Online TD.
- Generate-and-Test agent state.
- GVF usefulness and prediction design.
- Continual RL foundations.

Two subagents reviewed literature and proposal quality. Their key impact:

- Reward-Centered Sarsa and Output-Controlled TD are the primary proposals.
- Centered TD diagnostics should support Reward-Centered Sarsa, not stand alone.
- On-policy stability atlas should support Output-Controlled TD, not stand alone.
- GVF question design should support GVFs-as-state.
- Added stronger proposals: TIDBD plasticity, Baird off-policy stability, and Dyna planning budget.

### Implementation decisions

- Implemented a shared codebase under `experiments/alberta_core_rl/`.
- Each proposal has its own workspace config under `configs/<proposal>/`.
- Each run writes to `results/<proposal>/<timestamp>_<suite>/`.
- Scripts support single proposal runs, all-proposal runs, plotting, and smoke tests.
- No replay buffers or deep networks are used.

## Current Proposal Portfolio

Primary:

1. Reward-Centered Continuing Sarsa.
2. Output-Controlled TD.
3. GVF Predictive State.
4. Generate-and-Test Trace Features.
5. Doorway Options for Transfer.
6. TIDBD Plasticity.
7. Baird Off-policy Stability.
8. Dyna Planning Budget.

Supporting / fallback:

1. Centered TD Diagnostics.
2. On-policy Stability Atlas.
3. GVF Question Design.
4. Non-stationary Bandit.
5. Streaming Representation Diagnostic.

## Open Research Risks

- Some current implementations are minimal prototypes; their results should be treated as
  initial observations, not final claims.
- Baird's counterexample implementation needs verification against the canonical feature
  and behavior/target policy specification.
- Trace-normalized TD is currently a heuristic inspired by intentional updates, not a full
  implementation of the intentional trace algorithm.
- The current Generate-and-Test utility is simple; final analysis should explain exactly
  what utility means and why replacement is meaningful.
- Dyna uses a compact learned model, which is Alberta Plan aligned, but it should be clearly
  distinguished from replay.

## Next Iteration Checklist

- Add proposal-specific analysis notebooks or scripts for the main figures.
- Add heatmap plots for Reward-Centered Sarsa and Output-Controlled TD.
- Validate Baird implementation.
- Improve Dyna by adding environment-change phase and model-error diagnostics.
- Improve GVF-state proposal by plotting GVF values over a T-maze trial.
- Rewrite final report after seeing stronger main-run results.
