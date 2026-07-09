# On-Policy TD(lambda) Stability Atlas

Status: independent diagnostic study; supports but does not replace Output-Controlled TD.

## Abstract

This proposal maps the practical stability region of on-policy TD(lambda) under feature scaling, step-size changes, and eligibility traces. It is not an intervention study; it is an atlas that shows where ordinary fixed-alpha TD becomes fragile. The current main run finds that scale `one` is mostly stable, while larger and uneven feature scales sharply shrink the stable alpha/lambda region. This diagnostic strengthens the Output-Controlled TD proposal by showing why feature-scale robustness is not a cosmetic issue.


## Standalone Study Summary

This diagnostic study maps stability boundaries for on-policy TD(lambda). The RL problem is linear value prediction under different feature scales and trace settings. The implemented sweep varies alpha, lambda, and feature scale for TD-style learners. The experiment measures RMSE, weight norm, TD error, and divergence. The current evidence supports the broader Output-Controlled TD story: fixed step sizes have scale-dependent stability regions. The atlas is useful as supporting evidence but is not itself a complete final proposal.

## Research Motivation

TD(lambda) combines bootstrapping with multi-step credit assignment. In linear prediction, its stability depends on alpha, lambda, and feature geometry. A learner that appears stable under one representation can fail when the same state information is rescaled.

For a continual agent, this matters because representation scale may come from sensors, tile coders, learned features, or normalization choices. The agent should not require a fresh exhaustive alpha sweep whenever feature scale changes.

## Research Question

How do alpha, lambda, and representation scale shape the stability region of on-policy TD?

Hypothesis:

> Increasing feature scale and trace length should reduce the stable fixed-alpha region.

The atlas asks where failures occur, not which new algorithm fixes them.

## Alberta Plan Connection

The proposal targets:

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

The setting is a random-walk prediction problem with scaled tabular features. It is simpler than the tile-coded Output-Controlled TD main experiment, which makes it suitable for a dense alpha/lambda/scale atlas.

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

The atlas explains why output-controlled updates are needed. If alpha were an intrinsic measure of learning progress, the same alpha/lambda grid would show similar behavior across scales. It does not. The interaction with lambda is especially important because traces can increase the effective update direction norm even when the current feature vector is small.

The atlas is descriptive by design. Its value is to identify dangerous regions and motivate normalization or intentional update mechanisms.

## Threats To Validity

The representation is simpler than the main tile-coded prediction experiment.

The atlas does not implement a new method. It should be judged as a diagnostic, not an algorithmic contribution.

Only on-policy prediction is studied. Off-policy traces can be more fragile.

The original learning-curve plot was too dense for a polished paper. The current report uses heatmaps so the atlas claim is visually inspectable.

## Reviewer Critique And Revisions

Stability reviewer:

- A stability atlas is valuable only if it informs method design.

Revision made:

- The report explicitly links atlas failures to output-controlled TD.

Strict reviewer concern:

- Do not promote this as a standalone main contribution without an intervention.

Decision:

- Keep as an independent diagnostic appendix-style study with full reproducibility.

## Conclusion

The On-Policy TD(lambda) Stability Atlas is a focused diagnostic proposal. It shows that feature scale and trace length materially change fixed-alpha stability. The result supports the broader output-control argument while remaining an independent map of TD(lambda) failure regions.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/onpolicy_stability_atlas/config_main.json
```
