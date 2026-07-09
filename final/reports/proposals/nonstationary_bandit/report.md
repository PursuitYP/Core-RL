# Nonstationary Bandit Sanity Check

Status: independent sanity diagnostic; not submission-grade as a final Core RL proposal.

## Abstract

This proposal uses a drifting multi-armed bandit to test the most minimal form of continual adaptation: action values must keep changing when the best action drifts. The current run shows that constant-alpha action-value estimates adapt better than sample averages, while sample averages become stale. This is useful pedagogy and a sanity check for plasticity, but it is not a strong final Core RL project because it lacks state, bootstrapping, value functions over time, planning, GVFs, or temporal abstraction.


## Standalone Study Summary

This study is a minimal sanity check for continual adaptation. The RL problem is a nonstationary bandit with drifting or switching reward distributions. The implemented learner uses simple online action-value tracking without replay or function approximation. The experiment measures reward tracking, adaptation after change, and simple regret-like behavior. The current evidence shows the expected tracking behavior, but the setting is too shallow for a main Core-RL proposal. It should remain an introductory sanity check or appendix.

## Research Motivation

Before studying complex continual RL mechanisms, it is useful to verify the simplest principle: an online learner in a nonstationary stream needs persistent plasticity. Sample averages converge toward old data and can become poor under drift. Constant step sizes keep the learner responsive.

The bandit setting isolates this idea, but isolation also limits the scientific depth.

## Research Question

Which simple online bandit update preserves plasticity under drifting action values?

Hypothesis:

> Constant-alpha updates should adapt better than sample averages when action values drift.

## Alberta Plan Connection

The connection is indirect. The proposal reflects continual adaptation and online learning, but it does not exercise most Alberta Plan components. It has no value-function bootstrapping, no state construction, no model, no planning, and no options.

For that reason, it should remain a sanity diagnostic unless expanded into a contextual or continuing control problem.

## Related Work

The bandit setting is a standard introductory RL testbed. It connects to step-size adaptation and nonstationary online learning. It is not a primary Alberta Plan research area by itself.

## Environment

The setting is a drifting multi-armed bandit with a reward shift in the second half of the stream. There is no state and no transition dynamics.

## Methods

Compared methods:

- sample-average action values;
- constant-alpha action values;
- gradient bandit without baseline;
- gradient bandit with baseline.

## Experimental Design

Current main diagnostic:

- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`.

Metrics:

- best-action rate;
- cumulative regret;
- reward.

Primary figure:

![Best-action rate in drifting bandit.](../../../../experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main/figures/best_action_rate_by_algorithm_curve.png)

## Results

Constant-alpha action values are strongest in this diagnostic, with tail best-action rate about `0.306`. Sample-average updates are poor under drift, with tail best-action rate about `0.009`.

The result supports the expected lesson: sample averaging is not plastic enough for nonstationary streams.

## Analysis

The result is correct but shallow. It helps motivate why later proposals care about constant step sizes, TIDBD, output control, and recovery windows. It does not by itself address a rich Core RL question.

The best way to upgrade this proposal would be to turn it into a contextual bandit or continuing control task with representation scale, reward centering, or partial observability.

## Threats To Validity

No state or bootstrapping is present.

The best-action rate is noisy and confidence intervals are large with five seeds.

The reward shift is simpler than realistic nonstationarity.

The proposal is too far from the main Alberta Plan value-function spine.

## Reviewer Critique And Revisions

Course-project reviewer:

- This is useful but too elementary for a final proposal.

Decision:

- Keep as an independent sanity check, not as a submission-grade project.

Upgrade path:

- Convert to contextual bandits or continuing access-control with drifting priorities.

## Conclusion

The Nonstationary Bandit proposal is a useful sanity diagnostic for plasticity, but it should not be promoted as a major final Core RL study. Its role is to motivate why continual learners need persistent adaptation.

## Proposal Template Answers

Focused RL question: As a minimal sanity check, does a simple online agent adapt to nonstationary reward probabilities without replay? The setting is a nonstationary bandit, the comparison is lightweight exploration/adaptation rules, and the metrics are regret and best-action rate. Compute is trivial; fallback is to keep it as an introductory sanity check only.

## Independent Research Scope

This is not a full Core RL proposal. It lacks state, bootstrapping, value functions over time, planning, GVFs, and control dynamics. Its independent role is to sanity-check plasticity language and to provide a simple introductory example, not to serve as a final research topic.

## Evidence Level

Evidence level: dropped sanity diagnostic. The result may be useful pedagogically, but it is too shallow for the course project's main Core RL standard.

## Experiment Design Rationale

The bandit is useful only because it is simple enough to expose adaptation speed and exploration tradeoffs. It should not be expanded by adding more arms or seeds alone. If revived, it should become a contextual bandit or continuing control task with value-function learning.

## Reviewer Audit

| Reviewer angle | Critique | Action taken | Remaining risk |
|---|---|---|---|
| Core RL | No bootstrapping or state. | Evidence level is dropped sanity. | Not submission-grade. |
| Continual learning | Adaptation is present but shallow. | Report limits scope to sanity check. | Needs richer environment to matter. |
| Strict instructor | Do not count this as one of the strong proposals. | Marked as diagnostic only. | Should be appendix/intro if used. |

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/nonstationary_bandit/config_main.json
```
