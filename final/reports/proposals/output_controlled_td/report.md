# Output-Controlled TD

Status: independent main proposal with completed main pilot and required baseline audit.

## Abstract

This proposal studies a practical instability in streaming temporal-difference learning: fixed parameter step sizes do not correspond to fixed prediction changes. In linear function approximation, rescaling features leaves the represented prediction problem essentially unchanged but changes the effect of a fixed alpha. We test fixed TD, normalized TD, trace-normalized TD(lambda), and true-online TD(lambda) in a tile-coded random-walk prediction task with feature-scale stress. The current main pilot shows that normalized and trace-normalized TD remain stable across tested feature scales and alphas, while fixed TD and the current true-online baseline diverge in high-scale or high-alpha conditions. The proposal's core claim is about controlling update consequences in a stream, not about tuning one alpha for one representation.


## Standalone Study Summary

This study tests feature-scale robustness in online TD prediction. The RL problem is tile-coded random-walk value prediction, where the same underlying process can be represented with different feature magnitudes. The implemented learners are fixed-step TD, normalized TD, trace-normalized TD, and a true-online TD(lambda) baseline. The experiment crosses feature scales, alphas, and trace settings; the main metrics are RMSE, divergence, weight norm, prediction change, and effective step size. The current evidence shows that normalized updates are much more robust to large feature scales, while fixed-step methods can diverge or require retuning. The next step is a stronger baseline audit, especially for true-online TD(lambda), and a longer CPU sweep.

## Research Motivation

Streaming RL removes the smoothing effects of replay buffers and minibatches. Every update is made from the current transition, and unusual feature magnitudes can produce sudden, large parameter movements. If alpha is specified in parameter units, then the same alpha can mean a tiny prediction change in one representation and a catastrophic prediction change in another.

The Alberta Plan emphasizes continual value-function learning from ordinary experience. A long-lived learner cannot assume that every sensor or representation channel has been scaled to match a hand-tuned alpha. Output-controlled TD addresses this by making the update size depend on the feature or trace norm, so alpha more nearly describes an intended prediction change.

## Research Question

Can output-controlled or normalized TD make online prediction robust to feature scale and trace magnitude in a streaming setting?

Hypothesis:

> Normalized TD variants should have a larger stable region over feature scales and step sizes than fixed-step TD.

The proposal intentionally studies linear prediction rather than deep networks so the geometry of the update is inspectable.

## Alberta Plan Connection

This study connects to:

- value-function prediction as a core component of agents;
- continual one-sample learning;
- limited computation and online normalization;
- step-size adaptation as a mechanism rather than a post-hoc tuning detail.

It also provides a non-deep, course-compatible proxy for the intentional-update idea from recent streaming RL work.

## Related Work

Intentional Updates argues that learning should specify desired output changes rather than raw parameter displacement. Normalized LMS provides the classical supervised-learning precedent. True Online TD(lambda) is a strong trace baseline for online TD. Recent streaming RL papers motivate the no-replay, batch-size-one problem, though this project stays in linear Core RL.

Local references:

- `resources/alberta_plan_related/intentional_updates_streaming_rl_2604.19033.pdf`
- `resources/alberta_plan_related/true_online_td_1512.04087.pdf`
- `resources/alberta_plan_related/streaming_deep_rl_finally_works_2410.14606.pdf`
- `resources/alberta_plan_related/squeezing_more_from_stream_2602.09396.pdf`

## Environment

The main setting is a larger random-walk prediction task with overlapping tile-coded features. The agent predicts the probability of reaching the right terminal state under a random policy.

Feature scales:

- `one`;
- `ten`;
- `hundred`;
- `uneven`.

The underlying prediction problem is the same style of random walk, but the parameter-space geometry changes dramatically.

## Methods

Compared learners:

- Fixed-step TD.
- Normalized TD.
- Trace-normalized TD(lambda).
- True-online TD(lambda).

Fixed TD uses a constant alpha. Normalized TD divides alpha by the squared feature norm. Trace-normalized TD divides by the trace norm. True-online TD(lambda) is included because it is a principled online trace algorithm, but its current implementation and alpha scaling need a separate audit before broad claims are made.

For fixed TD, the update direction is the current feature vector or eligibility trace, and the same raw alpha can produce very different prediction changes after feature rescaling. Normalized TD uses a denominator of approximately `epsilon + ||x_t||^2`, so the update is `w <- w + alpha * delta * x_t / (epsilon + ||x_t||^2)`. Trace-normalized TD replaces the current feature norm with the eligibility-trace norm, `epsilon + ||z_t||^2`, because the trace is the actual update direction when lambda is nonzero. The logged `prediction_change` metric estimates how much the value prediction moved on the current feature direction after the update; it is the central diagnostic for whether alpha has an output-level meaning.

## Experimental Design

Current main pilot:

- Feature scales: `one`, `ten`, `hundred`, `uneven`.
- Alphas: `0.03`, `0.1`, `0.3`.
- Lambda: `0.8` for trace variants.
- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`.

Primary metrics:

- RMSE over all random-walk states;
- divergence flag;
- weight norm;
- prediction-change magnitude;
- effective step size.

The decision rule is not simply lowest RMSE at one alpha. A method is considered more streaming-compatible if the same alpha range remains stable across feature scales and if prediction-change magnitudes stay comparable when features are multiplied by `10`, `100`, or uneven per-feature constants. A method that can be made stable only by retuning alpha separately for each scale is treated as less robust.

Planned extended CPU sweep:

- Scales: `one`, `ten`, `hundred`, `uneven`, and a lognormal scale pattern.
- Alphas: include smaller values for fixed and true-online baselines to estimate max stable alpha rather than only showing divergence.
- Lambda values: `0`, `0.8`, `0.95` for trace-aware methods.
- Seeds: `0-19`; steps: `20000`.
- Nonstationary extension: feature scale changes midway through the same prediction stream, with no reset of weights or traces.

Primary figure:

![Tile-random-walk RMSE by algorithm, scale, and alpha.](../../../../experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main/figures/rmse_by_algorithm-scale-alpha_curve.png)

## Results

Fixed TD diverges under scale `hundred` for all tested alphas, under scale `ten` at alpha `0.3`, and under several `uneven` conditions. This supports the core worry: raw alpha is not a stable unit of learning progress across feature scales.

Normalized TD keeps RMSE roughly between `0.44` and `0.56` across tested scales and alphas with zero divergence. Trace-normalized TD is similarly robust, with RMSE roughly `0.49-0.56`.

The current true-online TD(lambda) baseline performs well in easy scale conditions but diverges in high-scale/high-alpha cases. This is reported as a finding about the current baseline configuration, not as a general claim against true-online TD(lambda).

## Analysis

The most important figure is not a single learning curve but the stability atlas across scale and alpha. A method that is stable only after retuning alpha for every scale is less useful for streaming agents than one whose alpha has a consistent output-level meaning.

Normalized TD's advantage comes from changing the denominator of the update. In one-hot or low-scale settings, fixed TD and normalized TD can behave similarly. Under large or uneven scales, normalized TD prevents the same TD error from producing a much larger prediction change simply because the feature vector is larger.

Trace-normalized TD extends this idea to eligibility traces, where the relevant update direction is often the accumulated trace rather than the current feature vector alone.

## Threats To Validity

The task is prediction-only. That makes the mechanism clean, but a full control study should test whether output-controlled updates help Sarsa or actor-critic learning.

The current true-online TD(lambda) baseline may be unfair under the same raw alpha grid. The next report version should include a max-stable-alpha audit and a small known-case verification.

The current run uses five seeds. Divergence patterns are strong, but final confidence intervals should use more seeds and a larger alpha grid.

Feature scaling is synthetic. That is the point of the invariance test, but real sensor streams may have nonstationary scales, sparse features, and changing relevance.

## Reviewer Critique And Revisions

Strict reviewer concern:

- A one-hot random walk is too easy and can make the proposal look like a numerical trick.

Revision made:

- The main experiment uses overlapping tile coding and an alpha-by-scale grid.

Baseline concern:

- True-online TD(lambda) should be audited before using it as a negative comparison.

Required next revision:

- Add a small canonical true-online test, a max-stable-alpha table, and a nonstationary feature-scale shift without reset.

## Conclusion

The current evidence supports the proposal's main idea: streaming TD should control the effect of an update on predictions, not only the raw movement of parameters. Normalized and trace-normalized TD are robust in the tested scale-stress grid, while fixed TD is fragile. The proposal is strong as an independent Core RL study, but the next iteration must audit trace baselines and extend from prediction to at least one control setting.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/output_controlled_td/config_main.json
```

Longer seed/step sweep:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/output_controlled_td/config_extended.json
```
