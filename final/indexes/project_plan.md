# Project Plan Snapshot

See `draft/live_plan.md` for the evolving plan. This snapshot records the current implementation direction after the latest structure and report-review pass:

- A live portfolio of streaming Core RL proposals under an Alberta Plan lens.
- Main canonical proposal candidates after multi-role critique: Reward-Centered Sarsa and Output-Controlled TD.
- Major integrated positive candidates: Scale-Invariant Continuing Control and Continual Dyna Model Aging.
- Major integrated representation/GVF gate: Useful Predictive Knowledge.
- Major integrated redesign/negative-gate candidate: Predictive State Plasticity.
- Conditional canonical precursor: Dyna Planning Budget/model staleness, now supported by a 20-seed larger-grid extended diagnostic and best used as the first section of the model-aging line.
- Supporting or merged diagnostics: Baird off-policy stability, centered TD diagnostics, on-policy stability atlas, GVF question design, TIDBD plasticity, and the negative Generate-and-Test plasticity diagnostic.
- Dropped as independent final proposals: non-stationary bandit and streaming representation diagnostic. Doorway options are quarantined unless a fixed-goal sanity test first works.
- Shared implementation in `experiments/alberta_core_rl/`, with proposal implementations split under `experiments/alberta_core_rl/studies/`.
- Separate proposal configs and result directories for independent runs.
- Main configs use `config_main.json`; `config_minimal.json` is preliminary only. `config_extended.json` files reuse internal `"suite": "main"` logic where needed, but new runner outputs from extended configs are labeled with `_extended`.
- Completed evidence currently exists for Reward-Centered Sarsa, Reward-Centered Sensitivity, Output-Controlled TD, Output-Controlled TD Fairness Audit, Dyna Planning Budget, Continual Dyna Model Aging, Continual Dyna Model Aging Drift, Predictive State Plasticity, Useful Predictive Knowledge, Unit-Switching Continuing Control, and Scale-Invariant Continuing Control.
- Output-Controlled TD uses the completed CPU-task result `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`; Scale-Invariant uses `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`; Reward Sensitivity uses `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended`; Dyna Drift uses `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`.
- Constraints: no replay buffer, no deep networks, CPU-scale experiments, exact commands and seed/result manifests for each run.

This snapshot is intentionally brief; the current review entry point is `final/README.md`. Historical gate decisions are archived in `final/archive/legacy/proposal_gate_review.md`.
