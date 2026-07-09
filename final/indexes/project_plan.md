# Project Plan Snapshot

See `draft/live_plan.md` for the evolving plan. This snapshot records the current implementation direction after the latest structure and report-review pass:

- A live portfolio of streaming Core RL proposals under an Alberta Plan lens.
- Main canonical proposal candidates after multi-role critique: Reward-Centered Sarsa and Output-Controlled TD.
- Major integrated positive candidates: Scale-Invariant Continuing Control and Continual Dyna Model Aging.
- Major integrated redesign/negative-gate candidate: Predictive State Plasticity.
- Conditional canonical precursor: Dyna Planning Budget/model staleness, now supported by a 20-seed larger-grid extended diagnostic and best used as the first section of the model-aging line.
- Supporting or merged diagnostics: Baird off-policy stability, centered TD diagnostics, on-policy stability atlas, GVF question design, TIDBD plasticity, and the negative Generate-and-Test plasticity diagnostic.
- Dropped as independent final proposals: non-stationary bandit and streaming representation diagnostic. Doorway options are quarantined unless a fixed-goal sanity test first works.
- Shared implementation in `experiments/alberta_core_rl/`, with proposal implementations split under `experiments/alberta_core_rl/studies/`.
- Separate proposal configs and result directories for independent runs.
- Main configs use `config_main.json`; `config_minimal.json` is preliminary only. `config_extended.json` files reuse internal `"suite": "main"` logic where needed, but new runner outputs from extended configs are labeled with `_extended`.
- Completed extended evidence currently exists for Reward-Centered Sarsa, Output-Controlled TD, Dyna Planning Budget, Continual Dyna Model Aging, Predictive State Plasticity, and Unit-Switching Continuing Control. Output-Controlled TD now uses the completed CPU-task result `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`.
- The full fixed-condition Scale-Invariant Continuing Control extended sweep has been submitted as CPU task `core-rl-scale-invariant-extended-33723554`; it is not evidence until standard artifacts are produced.
- Constraints: no replay buffer, no deep networks, CPU-scale experiments, exact commands and seed/result manifests for each run.

This snapshot is intentionally brief; the current review entry point is `final/README.md`. Historical gate decisions are archived in `final/archive/legacy/proposal_gate_review.md`.
