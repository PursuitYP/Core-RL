# Critic Round 5 Proposal Triage

Date: 2026-07-08

This note records the current multi-role critique after the recovery-window reruns. The goal
is to avoid defending weak proposal ideas just because they were in the initial plan.

## Reviewer Roles

Alberta Plan reviewer:

- Favors ordinary-experience, continuing, online learning with value functions, learned
  models, average reward, GVFs, and limited computation.
- Rejects proposals that are only episodic score comparisons or that depend on replay/deep
  networks.

Experimental reviewer:

- Requires seed-aware condition summaries, explicit baselines, and metrics that answer the
  stated RL question.
- For nonstationarity, requires recovery windows rather than only final tail averages.

Proposal-pruning reviewer:

- Looks for a coherent final story, not a catalog of every implemented idea.
- Pushes to merge or drop overlapping weak proposals.

Engineering reviewer:

- Requires exact commands, reproducible configs, clean environment records, and result paths
  that match the current code.

## Current Gate Decisions

| Proposal | Current decision | Main reason |
|---|---|---|
| Reward-Centered Sarsa | Main story | Clean continuing-control question; strong reward-shift invariance and Q-scale stability in access-control. |
| Output-Controlled TD | Main story | Clean streaming prediction question; normalized output-control prevents feature-scale divergence in tile-coded random walk. |
| Dyna Planning Budget | Conditional third/support | Recovery-window evidence supports a model-staleness tradeoff story, but not a simple "more planning is better" story. |
| TIDBD Plasticity | Supporting only | Per-feature adaptation signal is visible, but normalized TD has lower prediction error. |
| Generate-and-Test | Downgrade/redesign | Better trace-timescale proximity does not become a prediction-error win in the current setting. |
| GVF Predictive State | Negative result/redesign target | Trace memory and oracle solve the task, but the current recurrent GVF state remains near chance. |
| Baird Off-policy Stability | Supporting diagnostic | Useful warning about off-policy bootstrapping with function approximation; keep claims canonical and narrow. |
| Options | Quarantine | Current Four Rooms options do not yet answer reusable subtask learning. |
| Centered TD Diagnostics | Merge | Mechanism support for Reward-Centered Sarsa, not independent. |
| On-policy Stability Atlas | Merge | Mechanism support for Output-Controlled TD, not independent. |
| GVF Question Design | Merge/redesign aid | Useful for repairing GVF, not independent. |
| Streaming Representation | Drop | Too vague and overlaps stronger plasticity/GVF directions. |
| Nonstationary Bandit | Drop | Useful sanity check, but too shallow for the final Core RL project. |

## Proposal-Specific Critiques

### Reward-Centered Sarsa

Strongest defense:

- The question is focused: in continuing control, does reward centering remove sensitivity to
  arbitrary constant reward shifts?
- The access-control queue is a recognized average-reward control setting and is not merely a
  toy loop.
- The main result is mechanism-specific: discounted Sarsa's Q norm grows with the reward
  shift, while reward-centered and differential methods keep value scale stable.

Main remaining risk:

- Do not oversell the result as universally better control. The defensible claim is
  invariance and numerical stability under reward translation.

### Output-Controlled TD

Strongest defense:

- The question is focused: in streaming TD, should step size control parameter motion or the
  intended prediction/output change?
- The feature-scale stress test creates a real failure mode for fixed TD.
- Normalized and trace-normalized TD have zero divergence in the tested grid, while fixed TD
  and current true-online TD(lambda) fail in high-scale/high-alpha conditions.

Main remaining risk:

- The current implementation is a compact linear study inspired by intentional updates, not
  the full deep intentional-update algorithm. Report this precisely.

### Dyna Planning Budget

Strongest defense:

- It tests an Alberta Plan issue that the two main stories do not cover: learned models and
  computation allocation in a continuing stream.
- The recovery-window rerun shows the key tradeoff: planning improves pre-change reward, but
  stale backups remain high when the old model is kept after a layout change.

Main remaining risk:

- Late post-change reward does not show a clean planning win. The proposal is valuable only
  if framed around stale-model harm and recovery, not around generic sample efficiency.

### Generate-and-Test

Strongest defense:

- It is aligned with feature utility and continual representation adaptation.
- It can adapt trace timescales under a delay change.

Reason for downgrade:

- The current utility/replacement rule does not improve the metric that matters: prediction
  error. In the recovery-window rerun, random replacement and fixed-tight traces are at least
  as good as generate-test in late absolute error.
- Continuing to tune this exact setup would be low-value unless the question is reframed.

Possible redesign:

- Ask a sharper question: under a very small trace budget and multiple unsignaled delay
  changes, can utility-based feature generation discover and preserve predictive timescales?
- Add feature-survival curves and time-to-recover thresholds.

### TIDBD Plasticity

Strongest defense:

- It gives an interpretable mechanism signal: newly relevant feature step sizes rise after
  the switch while distractor step sizes remain low.

Reason for keeping only as support:

- Normalized TD has lower late post-change error in the current setting.
- The implemented method is `TIDBDLite`, so the report must not treat it as a full canonical
  TIDBD result.

### GVF Predictive State

Strongest defense:

- Conceptually very Alberta Plan aligned: learned predictions as state under partial
  observability.

Reason for negative result:

- The current result is not a positive GVF result. Oracle memory and a cheap trace memory
  baseline solve the T-maze; the current recurrent GVF does not.

Required repair:

- Use a new GVF question design where the learned prediction can be visually and
  quantitatively tied to the hidden cue needed for control.
- Keep trajectory plots as a promotion requirement for any future GVF variant.

### Options

Reason for quarantine:

- Options are selected, but reward per environment step stays near the step cost.
- The current study does not establish reusable subtask value or option discovery.

Possible repair:

- First prove a fixed-goal sanity case where SMDP option execution beats primitives under
  environment-step accounting. Only then test goal changes.

## Current Final-Report Shape

Recommended:

1. Main study 1: Reward-Centered Continuing Sarsa.
2. Main study 2: Output-Controlled TD.
3. Optional compact study: Dyna planning budget and model staleness.

Do not present all implemented proposals as equal. The remaining proposals should be
appendix diagnostics, redesign notes, or honest negative results.
