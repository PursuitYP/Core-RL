# Core-RL Proposal Overview

This file is the English counterpart of `proposal_overview_zh.md`. It is a fast review entry, not a replacement for the standalone reports. Current claims should still cite `final/reports/**/report.md` and `final/indexes/results.md`.

## Reading Path

- Chinese quick review: `proposal_overview_zh.md`.
- Integrated proposal reports: `final/reports/integrated/*/report.md` and `report_zh.md`.
- Canonical proposal reports: `final/reports/proposals/*/report.md` and `report_zh.md`.
- Evidence index: `final/indexes/results.md` and `results_zh.md`.
- Reproduction index: `final/indexes/reproduction.md` and `reproduction_zh.md`.

## Project Constraints

All studies are Core RL studies under the Alberta Plan lens. They use online streaming interaction, no replay buffer, no deep network, no offline training loop, and CPU-scale tabular or linear methods. The main themes are continuing experience, value functions, average reward, learned models, planning, GVFs, feature utility, options, output-controlled updates, and continual adaptation.

## RL Environment Catalogue

The environments are not interchangeable benchmarks. Each one was chosen to expose a specific Core-RL mechanism while remaining small enough for internal diagnostics such as value scale, TD-error scale, stale backups, prediction utility, feature utility, and recovery windows. A proposal is considered stronger when its environment directly matches its research question.

Access-Control Queue is the main environment for reward centering and continuing-control invariance. The state is the number of free servers plus the current customer priority; actions are reject or accept; accepted high-priority customers produce larger rewards, and busy servers become free stochastically. The task is continuing and average-reward-like, with no natural episodic reset. `Reward-Centered Continuing Sarsa` uses it to test whether constant reward shifts create only nuisance value offsets; `Scale-Invariant Continuing Control` additionally rescales the one-hot features to test simultaneous reward-unit and feature-unit sensitivity; `Unit-Switching Continuing Control` changes reward origin or feature scale halfway through one stream without resetting the agent.

Tile-Coded Random Walk is the main prediction environment for output-controlled TD. The underlying process is a random walk where the agent predicts the probability of reaching the right terminal state, but the representation uses overlapping tile-coded features whose magnitudes are deliberately rescaled. This environment isolates the question of whether alpha controls a prediction change or merely a parameter displacement. `Output-Controlled TD` and `On-Policy TD(lambda) Stability Atlas` use it to compare fixed TD, normalized TD, trace-normalized TD, and true-online TD(lambda) over scale/alpha/lambda grids.

Changing Continuing Gridworld is the main model-based and planning environment. The agent moves in a continuing gridworld, receives step costs, hazard penalties, and goal rewards, and the goal/hazard layout changes midway through the stream without resetting values or the learned model. This creates model entries that were correct before the change but stale afterward. `Dyna Planning Budget` uses the environment to separate pre-change planning benefits from post-change stale-backup costs; `Continual Dyna With Model Aging` uses it to compare keep-model, oracle flush, recency aging, and recency/error gating with stale-backup rate, model error, planning TD magnitude, and recovery windows.

T-Maze Cue Environment is the main partial-observability and predictive-state environment. A transient left/right cue appears at the start of each trial, then disappears in an aliased corridor; at the junction the agent must choose according to the earlier cue. Raw observation is insufficient, while trace memory and oracle memory are strong baselines. `GVF Predictive State`, `Predictive State Plasticity`, `GVF Question Design`, and `Useful Predictive Knowledge` use this setting to test whether learned predictions become useful state, not merely accurate predictions.

Trace-Conditioning Stream is the main generate-and-test feature environment. A cue appears, reward arrives after a delay, and the relevant delay changes during the stream. With a limited feature budget, the learner must decide which trace features to keep or replace. `Generate-and-Test Trace Features` uses this stream to test whether a utility rule selects features that actually reduce downstream prediction error after delay shifts.

Nonstationary Sensor Stream is the main feature-plasticity and auxiliary-representation stream. The relevant feature group changes by phase, while old and distractor features remain present. `TIDBD-Lite Plasticity` uses it to test whether per-feature step sizes move toward newly relevant features; `Streaming Representation With Auxiliary Prediction` uses it to test whether an auxiliary next-feature prediction helps the main value predictor. Current evidence says the auxiliary target is not automatically useful.

Baird-Style Counterexample is an off-policy stability diagnostic rather than a realistic control task. It creates behavior-target mismatch and large sparse importance ratios, exposing why semi-gradient off-policy TD can diverge with linear value functions. `Baird Off-Policy Stability` uses it as a warning for GVF/off-policy prediction methods that lack a stable objective.

Four Rooms / Doorway Navigation is the candidate temporal-abstraction environment. States are grid positions, primitive actions move in four directions, and doorway options execute multi-step temporally extended behavior. It is appropriate for reusable-subtask questions, but the current `Doorway Options for Reusable Subtasks` evidence is quarantined until fixed-goal sanity, SMDP duration accounting, and goal-change recovery are repaired.

Nonstationary Bandit is a minimal tracking sanity check. It has no state bootstrapping, learned model, GVF, or temporal abstraction, so it cannot carry a final Core-RL claim. Its role is to verify basic online tracking behavior under drifting rewards.

## Recommendation Tiers

### Strongly Recommended

1. Scale-Invariant Continuing Control. This is a strong larger independent direction because it studies reward translation and feature-scale invariance in one continuing control problem. The completed fixed-condition extended grid shows that reward centering and output normalization fix different failure modes and compose well in normalized-centered/differential variants: the combined normalized variants have `0/1500` divergent seed-conditions and mean tail unshifted reward around `2.55`, while discounted and reward-centered-only Sarsa each diverge in `500/1500` seed-conditions. The no-reset unit-switch extension gives a stricter conclusion: combined variants prevent catastrophic instability, but abrupt feature-unit recovery remains open.

2. Continual Dyna With Model Aging. This is the strongest planning/model-based direction. It asks which model entries deserve planning after the world changes. Current 20-seed half-life/budget evidence shows recency aging sharply reduces stale backups, especially at planning budget `20`. The completed abrupt/gradual/stochastic drift extension strengthens the claim for abrupt and gradual drift but blocks a universal aging claim under stochastic drift. The added reward/staleness Pareto frontier makes the claim more precise: abrupt drift has a near-reward-preserving low-staleness alternative, gradual drift is won by high-budget recency/error gating, and stochastic drift remains a negative boundary case.

3. Reward-Centered Continuing Sarsa. This is a clean standalone main proposal. It asks whether continuing Sarsa should be invariant to arbitrary reward offsets. Current access-control evidence shows ordinary discounted Sarsa inflates value scale under reward shifts, while centered and differential variants remain more stable. The completed beta/gamma/no-reset reward-origin switch extension adds stronger continual evidence: reward-centered and differential variants keep high post-late reward under reward-origin switches, while discounted Sarsa can carry large nuisance Q norms without formal numerical divergence. The added early recovery analysis now shows that the first `1000` logged post-switch steps also favor centered and differential methods on down/up reward-origin changes, so the claim is no longer only a late-window scale claim.

4. Output-Controlled TD. This is the clean standalone prediction/function-approximation proposal. It asks whether alpha should control prediction change rather than raw parameter change. Current citable tile-coded random-walk evidence is the 20-seed extended CPU-task run `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`: normalized TD and trace-normalized TD have `0/400` seed-conditions diverged, while fixed TD and the raw-alpha true-online baseline each diverge in `141/400` seed-conditions. The completed normalized true-online fairness audit `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended` shows normalized TD and trace-normalized TD(lambda) at `0/300`, fixed and raw-alpha true-online at `81/300`, and naive normalized true-online at `34/300`, with failures concentrated in lognormal scaling. The added max-stable-alpha frontier makes the stability claim more readable: normalized and trace-normalized TD stay stable to alpha `0.3` on every scale, while raw-alpha methods require scale-specific shrinking and normalized true-online still has no fully stable lognormal alpha.

5. Dyna Planning Budget and Model Staleness. This is useful either as a standalone conditional proposal or as the first diagnostic section of Continual Dyna With Model Aging. It shows that more planning can help before change but stale model backups can harm post-change recovery.

6. Useful Predictive Knowledge. This is the strongest current representation/GVF framing because it makes prediction usefulness a gate rather than a slogan. The completed T-maze gate shows raw observation is near chance, trace/oracle solve the memory problem, and learned cue predictions are partially decodable but not yet control-useful. It is a high-value negative-to-redesign topic rather than a solved representation method.

7. Predictive State Plasticity. This is high-risk but insightful. It is currently a negative gate, not a positive result: cue-GVF carries some signal but does not improve T-maze control, while trace/oracle memory works. It is worth keeping if the project wants a challenging representation/GVF direction.

### Recommended With Redesign

GVF Predictive State and GVF Question Design can be read together in the overview because they support the lesson that prediction accuracy is not the same as useful state. Generate-and-Test and TIDBD-Lite are independent representation-plasticity records that need a better downstream utility target before they become strong final topics. Baird Off-Policy Stability is valuable as a stability warning, but should be verified against canonical Baird details or upgraded into an off-policy GVF stability study.

### Supporting Or Appendix Material

Centered TD Diagnostics supports Reward-Centered Sarsa. On-Policy TD(lambda) Stability Atlas supports Output-Controlled TD. Streaming Representation is a negative auxiliary-prediction diagnostic. Nonstationary Bandit is a minimal sanity check. Doorway Options is quarantined until a fixed-goal sanity test succeeds.

## Integrated Proposals

### Scale-Invariant Continuing Control

Report: `final/reports/integrated/scale_invariant_continuing_control/report.md`. The study asks whether reward centering and output-controlled Sarsa can jointly make a continuing access-control agent robust to reward shifts and feature scaling. Current fixed-condition result: `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`. No-reset unit-switch extension: `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`. The combined normalized-centered and normalized-differential variants preserve mean tail unshifted reward around `2.55` across the extended grid and avoid catastrophic Q-norm growth in the unit-switch extension, but harsh abrupt feature-scale switches still reduce recovery reward.

### Continual Dyna With Model Aging

Report: `final/reports/integrated/continual_dyna_model_aging/report.md`. The study asks when a continual Dyna agent should distrust old model entries after a world change. Fixed-change result: `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`. Drift result: `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`. At planning budget `20`, keep-model late stale-backup rate is `0.213 +/- 0.065`; freshness-aware sampling reduces it to near zero for shorter aging half-lives, while reward ranking depends on budget and half-life. The drift extension shows the idea survives abrupt and gradual drift in high-budget settings, but stochastic drift is noisy and is not won by aging.

### Predictive State Plasticity

Report: `final/reports/integrated/predictive_state_plasticity/report.md`. The study asks whether learned predictions can become useful state under partial observability. Current result: `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`. In the 20-seed extended gate over maze lengths `8/12/20/30`, cue-GVF remains near chance, while oracle memory stays near `0.93-0.95` trial accuracy and trace memory remains above chance even at length `30`.

### Useful Predictive Knowledge

Report: `final/reports/integrated/useful_predictive_knowledge/report.md`. The study asks when a learned prediction deserves to become part of agent state under partial observability and resource limits. Current evidence includes Gate-1/Gate-2 result `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main` and Gate-3 feature-budget result `experiments/alberta_core_rl/results/useful_predictive_knowledge_budget/20260709T132025Z_main`. In T-maze lengths `8/12/20`, raw observation remains near chance, trace/oracle controls solve the task, and the best learned cue decoder is above chance but does not improve control. Under a two-feature budget, low-TD and oracle-decoding selectors usually keep the cue-GVF pair, yet trial accuracy remains near chance. This makes the proposal a clean useful-state gate and a prediction-to-policy redesign target rather than a solved GVF-state method.

## Canonical Proposals

Reward-Centered Sarsa and Output-Controlled TD are the strongest canonical proposals. GVF Predictive State, Generate-and-Test, Options, TIDBD, Baird, Dyna Planning Budget, Centered TD Diagnostics, On-Policy Stability Atlas, GVF Question Design, Nonstationary Bandit, and Streaming Representation remain useful as independent records, but several are negative, supporting, quarantined, or dropped diagnostics. Their `report_zh.md` files give Chinese quick-review versions, while `report.md` files remain the canonical English reports.

## Current Evidence Standard

All current results use online interaction and seed-aware tail summaries in `condition_summary.json`. Reward-Centered Sarsa, Reward-Centered Sensitivity, Output-Controlled TD, Output-Controlled TD Fairness Audit, Dyna Planning Budget, Scale-Invariant Continuing Control, Continual Dyna Model Aging, Dyna Drift, Predictive State Plasticity, Useful Predictive Knowledge, and Unit-Switching Continuing Control now have completed evidence directories with standard artifacts. Report-ready figures are generated with `experiments/alberta_core_rl/scripts/plot_report_figures.py`; rjob-owned result directories are handled by writing figures into the relevant report folders.
