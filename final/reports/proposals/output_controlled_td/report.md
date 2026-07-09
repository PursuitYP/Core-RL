# Output-Controlled TD

Status: independent main proposal with completed 20-seed primary evidence and completed 10-seed true-online fairness-audit evidence. The primary result path is `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`; the fairness-audit result path is `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended`. Both CPU tasks produced standard artifacts. Because rjob-owned result directories are not writable from the normal project shell, report-ready figures are stored in this report directory under `figures/` and `fairness_figures/`.

## Abstract

This proposal studies a practical instability in streaming temporal-difference learning: a fixed parameter step size does not correspond to a fixed prediction change. In linear function approximation, multiplying features by a constant can leave the represented prediction problem conceptually unchanged while changing the effect of the same alpha by orders of magnitude. We test fixed TD, normalized TD, trace-normalized TD(lambda), raw-alpha true-online TD(lambda), and a normalized true-online audit variant in a tile-coded random-walk prediction task with feature-scale stress. The extended 20-seed primary result shows a sharp stability split: normalized and trace-normalized TD have zero seed-level divergence across 400 seed-conditions each, while fixed TD and raw-alpha true-online TD(lambda) each diverge in 141/400 seed-conditions. The 10-seed fairness audit confirms that ordinary normalized and trace-normalized TD stay stable on a wider alpha grid, while naive normalized true-online TD(lambda) removes the uniform-scale failures but still diverges under lognormal feature scaling. The core claim is not that one alpha wins a benchmark, but that online TD needs update units tied to prediction/output effects rather than raw parameter displacement.

## Proposal Template Answers

What do we want to understand? We want to understand whether online TD prediction can be made robust to nuisance feature scaling when the learner receives one transition, updates once, and discards the transition.

What setting or testbed is used? The testbed is a tile-coded random-walk prediction problem. The underlying Markov chain and target value function are fixed, but the feature magnitudes are rescaled by uniform, uneven, and lognormal patterns.

What will we examine? We compare fixed-step TD, normalized TD, trace-normalized TD(lambda), true-online TD(lambda), and a normalized true-online audit variant under a grid of feature scales and alphas. The comparison is deliberately about stability regions, not only final RMSE under one tuned alpha.

What will we look at? The main evidence is a set of heatmaps and tables for RMSE, seed-level divergence, weight norms, prediction-change magnitude, and effective step size. A method is stronger if the same alpha range remains stable across feature scales.

## Independent Research Scope

This proposal is an independent study of update units in streaming value prediction. It isolates a feature-scale invariance problem: the underlying random-walk prediction problem is kept conceptually fixed while the feature vector is rescaled. Reward-origin effects, control behavior, and model-based planning are intentionally outside this report's scope, so the claims here are limited to streaming prediction with linear function approximation.

The proposal should also not be read as a general rejection of true-online TD(lambda). The current true-online condition is a raw-alpha trace baseline in a feature-scale stress test. Its divergence is evidence that raw parameter-space alpha is unfair under feature rescaling, not evidence that true-online TD(lambda) is intrinsically unstable when tuned or normalized appropriately.

## Evidence Level

Evidence level: strong independent main-candidate evidence for the prediction-side mechanism, with a completed fairness audit for the true-online trace baseline. The completed primary CPU run uses 20 seeds, 20000 steps, five feature-scale patterns, four alphas, and four algorithms. The key primary result is seed-level rather than row-level: normalized and trace-normalized TD have zero divergent seed-conditions across the full grid, while fixed TD and the raw-alpha true-online baseline diverge in 141 of 400 seed-conditions each.

The fairness audit uses 10 seeds, 150 condition groups, five feature-scale patterns, six alphas, and five algorithms: fixed TD, normalized TD, trace-normalized TD(lambda), raw-alpha true-online TD(lambda), and normalized true-online TD(lambda). It strengthens the main mechanism claim but also sharpens the limitation: normalized TD and trace-normalized TD have `0/300` divergent seed-conditions each; fixed TD and raw-alpha true-online TD(lambda) each have `81/300`; normalized true-online TD(lambda) improves to `34/300`, but all of those failures are concentrated in the lognormal feature-scale condition. The evidence is still prediction-side rather than control-side, so it should not be read as a completed control-agent solution.

## Paper-Style Contribution And Claim Boundaries

The contribution is an update-unit study for streaming TD with linear function approximation. The report turns feature scaling from a nuisance hyperparameter issue into a measurable stability question: does alpha specify a raw parameter displacement or an intended prediction change? The extended result contributes a seed-level stability atlas and shows that trace normalization and feature normalization can prevent entire classes of scale-induced divergence.

The claim boundary is that this is a prediction-side mechanism result. It does not yet establish a control improvement, and it does not fairly rank true-online TD(lambda) as an algorithm family. The primary true-online condition is a raw-alpha baseline; the fairness audit adds a normalized variant and shows that true-online output control needs a more careful derivation under heterogeneous feature scales.

## Research Motivation

Streaming RL removes the stabilizing effects of replay buffers, minibatches, and repeated passes over data. Every update is made from the current transition. If a feature vector is unusually large, a parameter-space alpha can produce a huge prediction change before the learner sees any corrective sample. This is not a cosmetic scaling issue: a long-lived agent in the Alberta Plan sense may maintain many value functions, GVFs, and learned models over sensory channels whose units drift or differ by construction.

The Alberta Plan emphasizes ordinary experience, temporal uniformity, continual value-function learning, and limited computation. Those commitments make manual per-sensor alpha tuning unattractive. A more scalable principle is to define the size of an update by its intended effect on the prediction, echoing normalized LMS and recent intentional-update arguments for streaming RL. This proposal tests that idea in the simplest setting where feature scale and prediction error can be inspected exactly.

## Research Question

Can output-controlled or normalized TD make streaming value prediction robust to feature scale and trace magnitude?

Hypothesis: normalized TD variants should have a larger stable region over feature scales and step sizes than fixed-step TD, because their alpha approximately controls an output change rather than a raw parameter movement.

## Alberta Plan Connection

This study connects to the value-functions component of the Alberta Plan base agent. A continual agent may learn many predictions from the same stream, and those predictions must be updated every time step with limited computation. The proposal also connects to temporal uniformity: there is no special calibration phase, no replay buffer, and no retrospective rescaling of the dataset. The agent must learn as experience arrives.

## Related Work

The closest recent motivation is Intentional Updates for Streaming Reinforcement Learning, which argues that parameter-space step sizes can produce unpredictable output changes in batch-size-one learning and proposes specifying the intended outcome of an update first. Normalized least-mean-squares methods provide an older prediction-learning precedent for scale-aware updates. Streaming Deep RL Finally Works and Squeezing More from the Stream define the broader no-replay streaming regime, though this project intentionally stays with linear Core RL. True Online TD(lambda) is included as an important online trace baseline; the current raw-alpha implementation must be interpreted carefully because true-online methods were designed to be strong and stable when step sizes are used appropriately.

## Environment

The environment is a larger random-walk prediction task with overlapping tile-coded features. The agent predicts the probability of reaching the right terminal state under a random policy. The true values are known, so RMSE can be measured over all states during the stream.

The feature-scale conditions are `one`, `ten`, `hundred`, `uneven`, and `lognormal`. These conditions keep the qualitative prediction task fixed while changing the geometry of the feature vectors. The `hundred` condition is an intentionally harsh uniform rescaling; `uneven` and `lognormal` make some dimensions much larger than others, which is closer to a multi-sensor setting.

## Methods

Fixed TD uses a constant alpha and the update direction `x_t` or `z_t`. Normalized TD divides alpha by approximately `epsilon + ||x_t||^2`, so a larger feature vector does not automatically imply a larger prediction movement. Trace-normalized TD(lambda) divides by the trace norm because the eligibility trace, not the current feature alone, is the actual update direction when lambda is nonzero. True-online TD(lambda) is included with lambda `0.8` as a principled trace method. The primary run uses it as a raw-alpha baseline; the fairness audit adds a normalized true-online variant to test whether the raw-alpha failure is mainly a unit mismatch.

The logged `prediction_change` metric estimates how much the current prediction moved after the update. This metric is central: an update rule can look reasonable in parameter space while being unstable in prediction space.

## Experimental Design

The completed extended sweep uses:

- result path: `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`;
- CPU task: `core-rl-output-extended-fixed-46602102`;
- seeds: `0-19`;
- steps per seed-condition: `20000`;
- representation: tile coding;
- feature scales: `one`, `ten`, `hundred`, `uneven`, `lognormal`;
- alphas: `0.01`, `0.03`, `0.1`, `0.3`;
- algorithms: fixed TD, normalized TD, trace-normalized TD(lambda), raw-alpha true-online TD(lambda);
- lambda: `0.8` for trace-normalized and true-online variants, `0` otherwise.

The decision rule is not simply lowest RMSE. A streaming-compatible update is expected to preserve stability across nuisance feature-unit changes. Divergence is therefore evaluated as a seed-level event: a seed-condition counts as divergent if any logged row for that seed-condition has `diverged = 1`.

The completed fairness audit uses result path `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended`, CPU task `core-rl-output-fairness-extended-rerun-29576456`, seeds `0-9`, steps per seed-condition `30000`, feature scales `one`, `ten`, `hundred`, `uneven`, and `lognormal`, alphas `0.001`, `0.003`, `0.01`, `0.03`, `0.1`, and `0.3`, and the five algorithms listed above. It is intentionally a fairness and failure-mode audit rather than a replacement for the primary 20-seed run.

## Experiment Design Rationale

The random-walk prediction task is intentionally simpler than a control benchmark because the research question is about update geometry. A known value function lets the report measure RMSE directly, while tile coding supplies overlapping linear features where feature norms and trace norms matter. This makes it possible to distinguish three mechanisms: prediction error, raw weight movement, and actual output change.

The scale conditions are not meant to be realistic sensor models by themselves. They are invariance tests. Uniform scaling asks whether the same represented prediction can be learned under a different unit. Uneven and lognormal scaling ask whether a few large components can dominate a streaming update. The alpha grid is chosen to reveal stability boundaries, not to crown one tuned setting. The correct figure is therefore a stability atlas and divergence table, not a single final-RMSE leaderboard.

## Results

![Tail RMSE stability atlas shown as readable panels by algorithm, scale, and alpha.](figures/report_log_rmse_heatmap_panels.png)

![Seed-level divergence-rate atlas shown as readable panels by algorithm, scale, and alpha.](figures/report_divergence_heatmap_panels.png)

![Tail output-change atlas shown as readable panels by algorithm, scale, and alpha.](figures/report_prediction_change_heatmap_panels.png)

| Algorithm | Lambda | Seed-conditions diverged | Non-diverged final RMSE mean | Interpretation |
|---|---:|---:|---:|---|
| fixed TD | 0.0 | `141/400` (`35.2%`) | `0.551` | Stable in easy scales but catastrophically scale-sensitive. |
| normalized TD | 0.0 | `0/400` (`0.0%`) | `0.461` | Stable across every tested scale and alpha. |
| trace-normalized TD(lambda) | 0.8 | `0/400` (`0.0%`) | `0.497` | Stable with traces when the trace direction is normalized. |
| true-online TD(lambda), raw alpha | 0.8 | `141/400` (`35.2%`) | `0.382` | Low RMSE on surviving easy conditions, but many high-scale conditions diverge. |

Fixed TD diverges for all seeds at scale `hundred` for every tested alpha, at scale `ten` for alpha `0.3`, and at scale `uneven` for alphas `0.1` and `0.3`. It also has a small but real divergence rate under `lognormal` at alpha `0.3`.

Normalized TD has no seed-level divergence across the full grid. At scale `hundred`, its final RMSE is approximately `0.56`, `0.53`, `0.44`, and `0.28` for alphas `0.01`, `0.03`, `0.1`, and `0.3`. Trace-normalized TD(lambda) also has no divergence; at scale `hundred`, its final RMSE is approximately `0.56`, `0.54`, `0.49`, and `0.40`.

The raw-alpha true-online TD(lambda) baseline should be read carefully. It diverges in the same number of seed-conditions as fixed TD, including all `hundred` conditions, yet its non-diverged RMSE is low because the surviving conditions are the easier scale settings. This makes it a warning about fair step-size comparison, not a claim that true-online TD(lambda) is generally poor.

### Second-Round Fairness Audit

The fairness audit is a completed second experiment inside the same research question. It adds a normalized true-online TD(lambda) variant and a broader alpha/scale grid so that the raw-alpha trace baseline is not treated as the final word on true-online TD(lambda). It also changes the figure design: the report uses per-scale panel heatmaps instead of a single very wide atlas, because the wide atlas is useful for audit but too compressed in a paper-style PDF.

Extended result path: `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended`

CPU task: `core-rl-output-fairness-extended-rerun-29576456`, succeeded on 2026-07-09 17:41 HKT.

![Fairness-audit tail RMSE panels by scale, algorithm, and alpha.](fairness_figures/report_log_rmse_heatmap_panels.png)

![Fairness-audit seed-level divergence panels by scale, algorithm, and alpha.](fairness_figures/report_divergence_heatmap_panels.png)

![Fairness-audit output-change panels by scale, algorithm, and alpha.](fairness_figures/report_prediction_change_heatmap_panels.png)

| Algorithm | Lambda | Fairness-audit seed-conditions diverged | Main interpretation |
|---|---:|---:|---|
| fixed TD | 0.0 | `81/300` (`27.0%`) | Fails under large uniform feature scale and also under high-alpha uneven/ten-scale settings. |
| normalized TD | 0.0 | `0/300` (`0.0%`) | Stable across all tested scales and alphas in this prediction audit. |
| trace-normalized TD(lambda) | 0.8 | `0/300` (`0.0%`) | The trace-normalized update direction remains stable across the wider grid. |
| true-online TD(lambda), raw alpha | 0.8 | `81/300` (`27.0%`) | Matches fixed TD's seed-level failure count under feature-scale stress. |
| true-online TD(lambda), normalized audit | 0.8 | `34/300` (`11.3%`) | Removes the uniform-scale failures but still fails under lognormal feature scaling, so naive normalization is not a complete true-online answer. |

## Analysis

The heatmaps support the central mechanism: fixed alpha is a poor unit for streaming prediction progress when feature scale changes. Under large or uneven scales, the same TD error can create a much larger output change simply because the feature vector is larger. Normalized TD changes the denominator of the update so the effective step size contracts when the feature direction is large. Trace-normalized TD applies the same idea to the accumulated eligibility trace.

The result also clarifies why a one-alpha leaderboard would be misleading. True-online TD(lambda) has strong theory and prior empirical support, but a raw-alpha comparison against normalized methods is not fair when the experimental manipulation is feature magnitude. The completed fairness audit shows that a simple normalized true-online variant does fix the harsh uniform-scale failures, but it is not a universal repair: lognormal feature scaling can still create trace-correction/output-control interactions that ordinary normalized TD and trace-normalized TD(lambda) avoid in this testbed.

## Threats To Validity

The task is prediction-only. That makes the feature-scale mechanism clean, but a full control study is needed to test whether output-controlled updates help Sarsa or actor-critic learning.

Feature scaling is synthetic. This is appropriate for an invariance test, but real sensor streams may have drifting scale, changing relevance, and partial observability. A no-reset feature-scale switch remains the most important next experiment.

The divergence metric is now seed-level, which is more interpretable than logged-row averages, but final RMSE is still measured at the last logged point rather than as an area-under-learning-curve statistic. Future analysis should report both stability and learning speed.

## Reviewer Critique And Revisions

Strict Core-RL reviewer: a random-walk prediction task can look toy-like. Response: the final experiment uses overlapping tile coding, five feature-scale patterns, 20 seeds, and a 4-by-5 scale/alpha stress grid. The environment is simple because the question is about update geometry, not behavior complexity.

Function-approximation reviewer: true-online TD(lambda) should not be treated unfairly. Response: the report now labels the primary condition as a raw-alpha baseline and adds a completed normalized true-online fairness audit. The audit improves the interpretation rather than giving true-online TD(lambda) a blanket pass: naive normalized true-online TD(lambda) still fails in lognormal feature scaling.

Reproducibility reviewer: the CPU job looked stuck because the old runner wrote results only at the end. Response: the job succeeded; future Output-Controlled TD runs now print condition-level progress. The report also records the rjob ownership issue and stores figures in the report folder.

Per-proposal audit matrix:

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| Core RL | Random walk may look too simple. | Uses tile coding, feature-scale stress, seed-level divergence, and known-value RMSE to isolate the update-unit mechanism. | Control transfer still needs a Sarsa or actor-critic experiment. |
| Function approximation | Raw-alpha true-online TD(lambda) is not a fair final baseline. | Adds a normalized true-online fairness audit and avoids broad claims against true-online TD(lambda). | Still needs a more principled true-online output-control derivation and max-stable-alpha analysis. |
| Streaming learning | A fixed scale per run is weaker than sensor drift. | Frames current result as fixed-condition invariance. | Needs no-reset feature-scale switch. |
| Statistics | Divergence row counts can exaggerate long runs. | Uses seed-level divergence events. | Time-to-divergence and AUC remain useful additions. |
| Strict instructor | The report should answer a question, not say normalized TD wins. | Main claim is about output-controlled update units preserving stability under nuisance feature scaling. | Needs tighter connection to downstream control for final project selection. |

## Conclusion

The extended evidence supports the proposal's main claim: streaming TD should control update consequences in prediction space, not only raw parameter movement. Normalized TD and trace-normalized TD(lambda) remain stable across all tested feature scales and alphas in both the primary run and the fairness audit, while fixed TD is fragile under scale stress. The fairness audit narrows the true-online interpretation: raw-alpha true-online TD(lambda) is not a fair final comparison, but naive normalized true-online TD(lambda) is also not a complete solution under lognormal feature scaling.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/output_controlled_td/config_extended.json
```

CPU-task command used for the current extended evidence:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PARTITION=safethm_cpu_task CPU=8 MEM=16000 \
  bash experiments/alberta_core_rl/scripts/run_cpu_task.sh \
  core-rl-output-extended-fixed \
  "PYTHONNOUSERSITE=1 python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_extended.json"
```

Report figures were generated into the report folder because the rjob result directory is not writable:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind output-td \
  --result-dir experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended \
  --figure-dir final/reports/proposals/output_controlled_td/figures
```

Fairness audit extended command:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/output_controlled_td_fairness_audit/config_extended.json
```

Fairness audit figure command:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind output-td \
  --result-dir experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended \
  --figure-dir final/reports/proposals/output_controlled_td/fairness_figures
```
