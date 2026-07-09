# On-Policy TD(lambda) Stability Atlas

Status: independent diagnostic study of fixed-step-size on-policy TD(lambda) stability.

## Abstract

This study maps the practical stability region of on-policy TD(lambda) under feature scaling, step-size changes, and eligibility traces. It is not an intervention study; it is an atlas that shows where ordinary fixed-alpha TD becomes fragile. The current main run finds that scale `one` is mostly stable, while larger and uneven feature scales sharply shrink the stable alpha/lambda region. The diagnostic shows why feature-scale robustness is a central stability issue for streaming value learning.


## Standalone Study Summary

This diagnostic study maps stability boundaries for on-policy TD(lambda). The RL problem is linear value prediction under different feature scales and trace settings. The implemented sweep varies alpha, lambda, and feature scale for TD-style learners. The experiment measures RMSE, weight norm, TD error, and divergence. The current evidence shows that fixed step sizes have scale-dependent stability regions. The atlas is useful as a standalone diagnostic map of where ordinary parameter-step TD(lambda) becomes unreliable.

## Research Motivation

TD(lambda) combines bootstrapping with multi-step credit assignment. In linear prediction, its stability depends on alpha, lambda, and feature geometry. A learner that appears stable under one representation can fail when the same state information is rescaled.

For a continual agent, this matters because representation scale may come from sensors, tile coders, learned features, or normalization choices. The agent should not require a fresh exhaustive alpha sweep whenever feature scale changes.

## Research Question

How do alpha, lambda, and representation scale shape the stability region of on-policy TD?

Hypothesis:

> Increasing feature scale and trace length should reduce the stable fixed-alpha region.

The atlas asks where failures occur, not which new algorithm fixes them.

## Alberta Plan Connection

The study targets:

- value prediction;
- online TD learning;
- eligibility traces;
- representation sensitivity;
- diagnostic process metrics for streaming agents.

It is an independent study because stability maps are useful evidence for any later continual value-function method.

## Related Work

True Online TD(lambda) and TD(lambda) literature motivate trace-based prediction. Recent intentional-update work motivates controlling update consequences rather than raw parameter steps. The Alberta Plan motivates small online value-function mechanisms.

Local references:

- `resources/alberta_plan_related/true_online_td_1512.04087.pdf`
- `resources/alberta_plan_related/intentional_updates_streaming_rl_2604.19033.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

## Environment

The setting is a random-walk prediction problem with scaled tabular features. The small state space makes it suitable for a dense alpha/lambda/scale atlas while keeping every divergence and error pattern inspectable.

## Methods

The diagnostic sweeps fixed TD(lambda) across:

- feature scale;
- alpha;
- lambda.

The learner updates online from one transition at a time and predicts the random-walk value function.

## Experimental Design

Current main diagnostic:

- Scales: `one`, `ten`, `uneven`.
- Alphas: `0.001`, `0.01`, `0.05`, `0.1`, `0.2`.
- Lambdas: `0`, `0.5`, `0.8`, `0.95`.
- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main`.

Metrics:

- RMSE;
- divergence;
- weight norm.

Primary report figures:

![TD(lambda) tail RMSE atlas by scale, alpha, and lambda.](../../../../experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main/figures/report_log_rmse_atlas.png)

![TD(lambda) divergence atlas by scale, alpha, and lambda.](../../../../experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main/figures/report_divergence_atlas.png)

## Results

Scale `one` is stable across most of the tested grid. Scale `ten` becomes unstable for larger alphas and high lambda. The `uneven` scale is fragile even at smaller alpha settings, with many conditions showing large RMSE and nonzero divergence.

This pattern supports the hypothesis that fixed alpha is not portable across representation scale and trace accumulation.

## Analysis

The atlas shows why update magnitudes should be interpreted through their effects on predictions, not only through raw parameter displacement. If alpha were an intrinsic measure of learning progress, the same alpha/lambda grid would show similar behavior across scales. It does not. The interaction with lambda is especially important because traces can increase the effective update direction norm even when the current feature vector is small.

The atlas is descriptive by design. Its value is to identify dangerous regions and motivate normalization or intentional update mechanisms.

## Threats To Validity

The representation is simpler than many tile-coded prediction settings.

The atlas does not implement a new method. It should be judged as a diagnostic, not an algorithmic contribution.

Only on-policy prediction is studied. Off-policy traces can be more fragile.

The original learning-curve plot was too dense for a polished paper. The current report uses heatmaps so the atlas claim is visually inspectable.

## Reviewer Critique And Revisions

Stability reviewer:

- A stability atlas is valuable only if it informs method design.

Revision made:

- The analysis links atlas failures to normalization and update-size design.

Strict reviewer concern:

- Do not promote this as a standalone main contribution without an intervention.

Decision:

- Keep as an independent diagnostic study with full reproducibility.

## Conclusion

The On-Policy TD(lambda) Stability Atlas is a focused diagnostic study. It shows that feature scale and trace length materially change fixed-alpha stability. The result provides an independent map of TD(lambda) failure regions and a concrete basis for scale-aware update design.

## Proposal Template Answers

Focused RL question: How does TD(lambda) stability change across alpha, lambda, and feature scale in an online prediction problem? The setting is a scaled random-walk prediction stream; the comparison is descriptive rather than a new algorithm. The main evidence is max-stable-alpha maps or heatmaps, not a single curve. Compute is small to moderate; the fallback is to report the clearest heatmap and max-stable-alpha diagnostics without claiming a remedy.

## Independent Research Scope

This atlas is independent as a diagnostic map, but it is not an intervention study. It explains why scale-normalized or prediction-space update measures are needed by showing where ordinary parameter-step TD(lambda) becomes fragile.

## Evidence Level

Evidence level: diagnostic atlas. It is valuable for mechanism and baseline calibration, but it should not be presented as a positive method because it does not propose or test a remedy.

## Experiment Design Rationale

The alpha/lambda/scale grid is the scientific object. It turns stability from an anecdotal divergence into a map of boundaries. The final presentation should emphasize atlas figures: tail RMSE and divergence heatmaps by `scale x alpha x lambda`.

## Reviewer Audit

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| Stability | A curve is not an atlas. | Heatmaps/max-stable-alpha are framed as required next figures. | Current presentation may still rely on dense curves. |
| Method | No new algorithm is introduced. | Evidence level is diagnostic. | Cannot claim method improvement without an intervention. |
| Strict instructor | The study needs a reason beyond plotting. | It motivates normalized update units. | Needs direct connection between heatmap regions and stability metrics. |

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/onpolicy_stability_atlas/config_main.json
```
