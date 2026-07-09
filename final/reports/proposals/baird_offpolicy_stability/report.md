# Baird Off-Policy Stability

Status: independent supporting diagnostic; requires canonical verification before broad claims.

## Abstract

This proposal studies the classic off-policy instability caused by bootstrapping, function approximation, and behavior-target policy mismatch. Baird's counterexample is a minimal diagnostic for the deadly triad. The current pilot compares semi-gradient off-policy TD with a TDC-style correction across step sizes. Off-policy TD exhibits rapidly growing weight norms, while TDC is stable at smaller alphas but fails at a larger alpha. The study is useful as a warning for GVF/Horde-style background prediction: off-policy predictions need stability checks before they are used as agent knowledge.


## Standalone Study Summary

This study is a stability warning for off-policy learning with function approximation. The RL problem is a Baird-style counterexample where behavior and target distributions mismatch and semi-gradient off-policy TD can diverge. The implemented methods compare semi-gradient off-policy TD with a TDC-like correction across step sizes. The experiment tracks weight norm, TD error, importance ratio, and divergence. The current evidence supports the qualitative warning that naive off-policy TD is unstable in this setting. The next step is canonical verification before using the result for a broad theoretical claim.

## Research Motivation

The Alberta Plan places value functions and GVFs at the center of agent knowledge. Many background predictions will naturally be off-policy: the agent observes behavior from one policy while asking questions about another policy, option, or continuation condition. The deadly triad means these predictions are not automatically safe.

This proposal is not about benchmark return. It is about whether a small value-function learner remains numerically and theoretically stable under off-policy sampling.

## Research Question

Where does semi-gradient off-policy TD fail, and when does a TDC-style correction stabilize the update?

Hypothesis:

> Semi-gradient off-policy TD should show weight-norm growth in Baird-style settings, while a gradient-corrected method should enlarge the stable step-size region.

The current pilot supports this qualitative hypothesis but is not yet a full canonical study.

## Alberta Plan Connection

The proposal supports:

- GVFs and predictive knowledge;
- off-policy learning from ordinary experience;
- stable value-function learning;
- background prediction safety.

It is a diagnostic proposal. Its contribution is a stability map, not a control policy.

## Related Work

Baird's counterexample is the classic minimal divergence example. Gradient TD, GTD2, TDC, and emphatic TD were developed to address off-policy TD instability with linear function approximation. Horde-style GVF learning motivates why this matters in a predictive agent.

Local references:

- `resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`
- `resources/alberta_plan_related/regularized_centered_emphatic_td_2605.04100.pdf`

External anchors:

- Emphatic approach to off-policy TD: https://arxiv.org/abs/1503.04269
- Emphatic TD summary: https://arxiv.org/abs/1507.01569

## Environment

The setting is a Baird-style seven-state counterexample with:

- linear features;
- zero rewards;
- behavior/target mismatch;
- bootstrapped TD targets.

Because rewards are zero, divergence appears as value/weight growth rather than return differences.

## Methods

Compared methods:

- semi-gradient off-policy TD;
- TDC-style correction.

Alpha sweep:

- `0.005`;
- `0.01`;
- `0.02`.

## Experimental Design

Current main pilot:

- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`.

Metrics:

- weight norm;
- TD error;
- divergence flag;
- alpha-specific stability behavior.

Primary figure:

![Baird-style weight norm by algorithm and alpha.](../../../../experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main/figures/weight_norm_by_algorithm-alpha_curve.png)

## Results

Off-policy TD has rapidly growing weight norms: about `1.12e4` at alpha `0.005`, `1.73e6` at alpha `0.01`, and `3.57e7` at alpha `0.02`.

TDC remains stable at alpha `0.005` and `0.01`, with weight norm near `8.79`, but also fails at alpha `0.02`. This matters: correction methods improve stability regions, but they are not immune to bad step-size choices.

## Analysis

The result is a stability diagnostic. It should be interpreted as a warning label for off-policy background predictions. If a future GVF proposal uses off-policy demons, it should include a stability-region analysis rather than assume TD updates are safe.

The TDC result also prevents overclaiming. A correction changes the update geometry, but practical stability still depends on alpha and variance.

## Threats To Validity

The setup must be verified against the canonical Baird specification before making broad claims.

Only one correction family is implemented. GTD2, ETD, and emphatic variants should be added for a complete stability paper.

The task is a diagnostic counterexample, not a natural control problem.

The current run length may be too short to distinguish slow divergence from convergence in some settings.

## Reviewer Critique And Revisions

Theory reviewer:

- Canonical details matter. A small deviation in Baird's features or policies can change the expected behavior.

Revision required:

- Add a canonical-spec verification note and expected-update comparison.

GVF reviewer:

- Connect the diagnostic to off-policy background predictions, not just a textbook example.

Revision required:

- Add a small off-policy GVF stream if this proposal is promoted beyond supporting status.

## Conclusion

Baird Off-Policy Stability is a strong supporting independent diagnostic. It demonstrates why off-policy value learning cannot be treated casually in a continual predictive agent. Before promotion to a full main study, it needs canonical verification, more correction baselines, and a GVF-style behavior-drift extension.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/baird_offpolicy_stability/config_main.json
```
