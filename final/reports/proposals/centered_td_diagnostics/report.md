# Centered TD Diagnostics

Status: independent mechanism diagnostic; bounded supporting study for reward centering.

## Abstract

This proposal isolates the mechanism behind reward centering in a small continuing prediction problem. By comparing ordinary TD, reward-centered TD, and Bellman-error-centered diagnostic updates under reward translation, it shows how centering changes value scale. The current run demonstrates that reward-centered TD keeps value norms small across reward shifts, while ordinary TD develops large shift-dependent values. The study is intentionally not a main control claim; its contribution is mechanistic explanation for the larger Reward-Centered Sarsa proposal.


## Standalone Study Summary

This diagnostic study isolates the mechanism behind reward centering. The RL problem is a small prediction/control stream with controlled reward shifts, designed to expose value-scale effects rather than to be a final benchmark. The implemented comparison contrasts centered and uncentered TD-style updates. The experiment measures value norm, TD error, reward baseline behavior, and sensitivity to reward translation. The current evidence supports the claim that centering reduces arbitrary value-scale inflation. The study is best used as a mechanism appendix for Reward-Centered Sarsa.

## Research Motivation

Reward centering can look like a small algebraic trick unless its effect is isolated. In a continuing task, adding a constant to all rewards introduces a large constant component into discounted value predictions. That component is mostly irrelevant for behavior but can dominate value norms and TD errors.

This diagnostic uses a tiny controlled MDP to make the effect visible before moving to access-control control experiments.

## Research Question

Which offset does each centering method remove, and how does that affect value scale under reward translation?

Hypothesis:

> Reward-centered TD should reduce the dependence of learned value scale on additive reward shifts compared with ordinary TD.

## Alberta Plan Connection

The proposal supports:

- continuing prediction;
- average-reward-style normalization;
- value-function diagnostics;
- interpretable small experiments before larger control claims.

It is small by design and should not be oversold.

## Related Work

Reward Centering motivates subtracting empirical average reward in continuing discounted methods. Bellman Error Centering clarifies related centered TD fixed points. The Alberta Plan motivates continuing value prediction as a core component.

Local references:

- `resources/alberta_plan_related/reward_centering_2405.09999.pdf`
- `resources/alberta_plan_related/bellman_error_centering_2502.03104.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

## Environment

The setting is a two-loop continuing MDP with random behavior and reward shifts. It is smaller than access-control and is used to expose value-scale mechanics in a controlled way.

## Methods

Compared methods:

- ordinary TD;
- reward-centered TD;
- Bellman-error-centered diagnostic update.

Each learner updates online from the stream. No replay or offline fitting is used.

## Experimental Design

Current main diagnostic:

- Reward shifts: `-5`, `0`, `5`.
- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main`.

Metrics:

- value norm;
- TD error;
- reward baseline;
- delta baseline.

Primary figure:

![Value norm by centering method and reward shift.](../../../../experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main/figures/value_norm_by_algorithm-reward_shift_curve.png)

## Results

Reward-centered TD keeps value norm small across shifts: about `6.43` at shift `-5`, `2.24` at shift `0`, and `8.58` at shift `5`.

Ordinary TD value norm grows to about `353` and `462` at shifts `-5` and `5`. The values are large because the learner is representing the reward offset, not because the task contains useful additional structure.

## Analysis

This diagnostic explains why the access-control result matters. Reward centering removes a nuisance offset from the prediction target, reducing value scale without changing the task-relevant dynamics.

The result also distinguishes mechanism evidence from final control evidence. A tiny MDP can show why a method behaves as it does; it cannot establish that the method is robust in larger continuing control.

## Threats To Validity

The environment is deliberately tiny and should not be used as a final main result.

The diagnostic behavior may be simpler than in control, where policy changes affect the reward distribution.

The Bellman-error-centered variant is used as a diagnostic and should not be overclaimed as a fully tuned algorithm.

## Reviewer Critique And Revisions

Mechanism reviewer:

- This study should answer "why" for reward centering, not compete with access-control.

Revision made:

- Report status is explicitly bounded as mechanism diagnostic.

Strict reviewer concern:

- Toy settings can make weak proposals look stronger than they are.

Decision:

- Keep as standalone mechanism paper material, but cite access-control as the main control evidence.

## Conclusion

Centered TD Diagnostics is a useful independent mechanism study. It clearly shows how centering controls value scale under reward translation. Its scope is intentionally limited: it supports, but does not replace, the Reward-Centered Continuing Sarsa proposal.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/centered_td_diagnostics/config_main.json
```
