# Nonstationary Bandit Plasticity Diagnostic

Status: independent plasticity sanity diagnostic. The result is useful and reproducible, but it remains too shallow for a submission-grade Core RL claim.

## Abstract

This mini-report evaluates a drifting multi-armed bandit as the smallest possible test of continual adaptation. The focused question is whether an elementary online learner can keep enough plasticity to track changing action values without replay. The experiment confirms the expected pattern: constant-alpha action-value estimates adapt better than sample averages after the reward distribution changes.

The result is a valid independent diagnostic with a deliberately narrow scope. It answers a small plasticity question and checks the experiment pipeline, plotting, and interpretation language. Its limitation is equally important: the task has no state, no temporal credit assignment, no bootstrapped value functions, no learned model, no planning, and no options. It should therefore be treated as a sanity diagnostic rather than promoted as a full Core RL project.

## 1. Proposal Template Answers

Focused RL question: In a nonstationary reward stream, which elementary online bandit update preserves plasticity after the identity of the best action changes?

Setting/testbed: A drifting multi-armed bandit with stochastic rewards and a reward-distribution shift in the second half of the stream.

Implemented comparison: Sample-average action values, constant-alpha action values, gradient bandit without a reward baseline, and gradient bandit with a reward baseline.

Observation or metric: Best-action rate is the main diagnostic, with cumulative regret and reward as supporting metrics.

Expected behavior: Constant-alpha updates should recover better after the shift because their effective step size does not vanish with time. Sample averages should adapt poorly because early rewards retain too much influence.

Compute need: Trivial CPU-only run with five seeds and 5000 online steps.

Fallback: Keep the result as an introductory plasticity diagnostic. A stronger project would need state, bootstrapping, value prediction, continuing control, or average-reward structure.

## 2. Research Motivation / Question / Method

Continual RL begins from a simple pressure: an agent must keep learning from a stream whose statistics may change. If an action that used to be good becomes poor, an estimator that averages all past rewards equally can become anchored to obsolete experience. A constant step size gives the learner finite memory and allows old evidence to fade.

The research question is deliberately minimal: which simple online update retains plasticity after the best arm changes? The hypothesis is that constant-alpha action-value learning will recover more readily than sample-average learning. Gradient bandit variants are included as lightweight comparisons, not as a claim about a new bandit algorithm.

The method uses online interaction only. At each step the learner selects one arm and receives a stochastic reward. There is no state observation beyond the action choice, no transition dynamic, and no long-horizon return. This isolates plasticity, but it also removes many mechanisms that define the stronger course themes.

## 3. Experimental Design

Main run:

- Seeds: `0-4`.
- Steps: `5000`.
- Environment label in config: `drifting_bandit_reward_shift`.
- Result path: `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`.
- Primary metrics: `best_action_rate`, `cumulative_regret`, and `reward`.

Primary figure:

![Best-action rate in drifting bandit.](../../../../experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main/figures/best_action_rate_by_algorithm_curve.png)

The design should be read as a sanity check. The main observation is whether a learning rule recovers after the reward shift, not whether the bandit setting is a sufficient model of continual RL.

## 4. Results

The observed ordering matches the hypothesis. Constant-alpha action values are strongest in this diagnostic, with seed-tail mean best-action rate about `0.306`. Sample-average updates are poor under drift, with seed-tail mean best-action rate about `0.009`.

The gradient bandit variants fall between those two in this run: the no-baseline variant has seed-tail mean best-action rate about `0.176`, and the baseline variant about `0.155`. Cumulative regret also favors constant-alpha learning in the seed-tail summary, with about `2838` for constant alpha versus about `4321` for sample averaging.

The evidence is noisy because there are only five seeds, and the confidence intervals for some learners are wide. Still, the qualitative pattern is enough for the diagnostic claim: persistent step sizes help preserve adaptation in this nonstationary bandit stream.

## 5. Analysis

The mechanism is straightforward. Sample averaging gives high cumulative weight to early rewards and gradually reduces the influence of new evidence. When the best action changes, the old estimate continues to dominate, so the learner adapts slowly or fails to revisit the new best arm often enough. Constant-alpha learning keeps a fixed learning rate and therefore tracks the changed reward distribution more readily.

This mechanism is relevant to persistent adaptation, step-size adaptation, reward centering, and recovery windows. However, the bandit does not test whether value predictions bootstrap over time, whether representations remain useful under changing observations, or whether planning and control improve ordinary experience. Adding more arms, seeds, or plots would make the diagnostic cleaner, but it would not by itself make the question a stronger Core RL study.

## 6. Threats To Validity

- The experiment has only five seeds, and best-action rate is noisy.
- The reward shift is simpler than realistic nonstationarity.
- The environment removes state, bootstrapping, delayed consequences, and function approximation.
- The gradient bandit settings are lightweight comparisons rather than tuned baselines.
- Best-arm identification is not the same as value prediction, average-reward control, or temporally extended behavior.

## 7. Reviewer Critique

| Reviewer critique | Current response | Required next action |
|---|---|---|
| The question is too shallow for Core RL. | The report explicitly labels the study as a plasticity sanity diagnostic. | Redesign around contextual prediction, continuing control, or average reward if revived. |
| Five seeds are too few for a strong empirical claim. | The claim is qualitative and bounded. | Add seeds only if the diagnostic itself remains useful. |
| Bandits have no temporal credit assignment. | This limitation is treated as a reason to quarantine the result. | Move to a small Markov or continuing-control task for a final project. |
| Gradient bandit comparisons are not deeply analyzed. | They are included only as lightweight references. | Do not build a final claim around them without a separate design. |

## 8. Conclusion

This proposal is an independent negative-bounded diagnostic: it confirms that constant step sizes preserve plasticity better than sample averages in a drifting bandit, but it does not establish a submission-grade Core RL result. Its best use is to document a minimal adaptation phenomenon and to motivate a richer redesign with state, value functions, or continuing control.

## 9. Reproduction

Run from the repository root:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/nonstationary_bandit/config_main.json
```

Expected result directory: `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`.
