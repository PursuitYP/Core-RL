# Baird Off-Policy Stability

Status: independent off-policy stability warning. The current evidence is a Baird-style pilot diagnostic, not a broad theory claim and not a control-performance result.

## Abstract

This mini-report studies a narrow failure mode for continual predictive agents: off-policy bootstrapped value learning can become unstable under linear function approximation. The testbed is a Baird-style seven-state prediction problem with zero reward, behavior-target policy mismatch, and online TD updates. This is directly relevant to GVF/Horde-style background prediction, where an agent may learn many predictions from ordinary experience while behaving according to a different policy.

The pilot compares semi-gradient off-policy TD with a TDC-style correction across three step sizes. Semi-gradient TD shows severe weight-norm growth. The TDC-style learner remains stable at smaller tested step sizes but also fails at the largest tested step size. The contribution is therefore a bounded warning: off-policy predictions need explicit stability checks before they are treated as agent knowledge.

## Claim Boundary

The report makes one bounded claim: in the current Baird-style implementation, ordinary semi-gradient off-policy TD exhibits severe weight growth, and a TDC-style correction enlarges but does not eliminate the stable step-size region.

It does not claim that every off-policy GVF diverges, that TDC is sufficient for all off-policy prediction, that the implementation is already a canonical Baird replication, or that the diagnostic measures control performance.

## 1. Proposal Template Answers

Focused RL question: What stability warning does a Baird-style counterexample provide for off-policy linear value prediction learned from ordinary experience?

Setting/testbed: A seven-state Baird-style off-policy prediction task with linear features, zero rewards, behavior-target mismatch, bootstrapped value targets, and online updates.

Implemented comparison: Semi-gradient off-policy TD versus a TDC-style correction over alpha values `0.005`, `0.01`, and `0.02`.

Observation or metric: Weight norm over time is the primary diagnostic, with TD error, importance ratio, and divergence flags as supporting signals.

Expected behavior: Semi-gradient off-policy TD should show weight-norm growth in this setting. A corrected method should reduce the failure over some step-size range, but the pilot does not assume it will be stable for every alpha.

Compute need: Small CPU-only runs with five seeds and 5000 online steps.

Fallback: If canonical Baird verification or additional correction baselines are not completed, the result remains a bounded stability warning rather than a general theorem or GVF solution.

## 2. Research Motivation / Question / Method

The Alberta Plan emphasizes value functions, GVFs, learned models, and ordinary experience as central ingredients of long-lived agents. Many useful predictions in such agents are naturally off-policy: the agent follows one behavior policy while asking what would happen under another policy, option, or continuation condition. Learning many predictions from the same stream is attractive, but it exposes the deadly triad of bootstrapping, function approximation, and off-policy sampling.

The research question is: what stability warning does a Baird-style counterexample provide for off-policy value prediction with linear function approximation? The hypothesis is that semi-gradient off-policy TD will show weight-norm growth, while a gradient-corrected method will reduce this failure over a restricted step-size range.

The method keeps the diagnosis small and online. The environment has zero reward, so the true value function should be zero. This makes growth in value estimates or weights a direct instability signal rather than a reward-optimization result. The learners are semi-gradient off-policy TD and a TDC-style correction, both run without replay buffers or offline fitting.

## 3. Experimental Design

Main run:

- Seeds: `0-4`.
- Steps: `5000`.
- Environment label in config: `baird_star_diagnostic`.
- Result path: `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`.
- Primary metrics: `weight_norm`, `diverged`, and `td_error`.

Primary figure:

![Baird-style weight norm by algorithm and alpha.](../../../../experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main/figures/weight_norm_by_algorithm-alpha_curve.png)

Design logic:

| Design element | Reason |
|---|---|
| Zero-reward prediction | Makes value growth a direct warning sign instead of a reward artifact. |
| Linear features | Keeps the study in classic core RL and avoids neural-network confounds. |
| Behavior-target mismatch | Creates the off-policy pressure needed for the diagnostic. |
| Alpha sweep | Separates correction-method behavior from step-size sensitivity. |
| Weight norm | Captures instability that return cannot show in a zero-reward prediction task. |

## 4. Results

The pilot shows the expected instability for semi-gradient off-policy TD. The seed-tail mean weight norms are approximately `1.12e4` at alpha `0.005`, `1.73e6` at alpha `0.01`, and `3.57e7` at alpha `0.02`.

The TDC-style learner is much more stable at the two smaller alphas: its seed-tail mean weight norm is about `8.79` at alpha `0.005` and `8.79` at alpha `0.01`. At alpha `0.02`, however, the TDC-style learner also fails, with seed-tail mean weight norm about `2.07e7` and a nonzero divergence signal.

The central empirical result is therefore not that the correction method solves the problem. The result is that ordinary off-policy TD is unsafe in this diagnostic, and the correction-style update improves but does not remove practical step-size sensitivity.

## 5. Analysis

The failure mechanism is not poor reward optimization, because all rewards are zero and the target value is zero. The instability comes from the interaction between bootstrapped targets, samples from the behavior distribution, updates aimed at a different target policy, and a feature representation whose projected update can amplify errors.

This is a useful diagnostic for GVF-style background prediction. A background prediction may look harmless because it does not directly choose actions, but unstable predictions can still contaminate state features, planning inputs, option models, or auxiliary knowledge. The result supports a conservative engineering rule: off-policy predictions should carry stability diagnostics before they are used as reliable agent knowledge.

The next analysis should be an audit, not a larger environment. The strongest immediate additions would be canonical Baird verification, expected-update or MSPBE-style diagnostics, a finer alpha and secondary-step-size map, and comparison to GTD2 and emphatic TD variants.

## 6. Threats To Validity

- The setup is Baird-style and still needs canonical verification before broader claims.
- Only one correction family is currently represented.
- A 5000-step run can miss slow divergence or delayed stabilization.
- Weight norm is necessary but not sufficient; MSPBE-style or expected-update diagnostics would strengthen the result.
- The task is a diagnostic counterexample, not a natural control environment.

## 7. Reviewer Critique

| Reviewer critique | Current response | Required next action |
|---|---|---|
| Canonical Baird details can change the result. | The claim is labeled as Baird-style pilot evidence. | Verify features, policies, transition probabilities, importance ratios, and expected-update behavior. |
| A counterexample is only a warning, not a GVF solution. | The report frames the result as an off-policy stability warning. | Add a small GVF-style background prediction stream only after the canonical audit. |
| TDC failure at high alpha complicates the story. | The failure is reported as evidence against overclaiming. | Map the stable region across alpha and correction parameters. |
| One diagnostic should not become a broad deadly-triad theorem. | The conclusion remains bounded and empirical. | Keep the final claim diagnostic unless stronger theory checks pass. |

## 8. Conclusion

This proposal is an independent off-policy stability study. In the current pilot, semi-gradient off-policy TD shows severe weight growth on a Baird-style zero-reward prediction task, while a TDC-style correction is stable only over part of the tested step-size range. The honest conclusion is a warning rather than a solution: off-policy value predictions can be useful for continual agents, but they need explicit stability checks before they are trusted.

## 9. Reproduction

Run from the repository root:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/baird_offpolicy_stability/config_main.json
```

Expected result directory: `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`.
