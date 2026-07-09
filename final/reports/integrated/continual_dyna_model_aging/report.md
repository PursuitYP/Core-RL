# Continual Dyna With Model Aging

## Abstract

Dyna-style planning is attractive for a continual agent because it reuses a learned model to improve value estimates without requiring more real interaction. In a nonstationary world, the same mechanism can amplify obsolete knowledge. This proposal studies model freshness as a first-class Core RL question: can a small online agent age or distrust model entries so that planning remains useful after the environment changes?


## Standalone Study Summary

This study asks when a continual Dyna agent should trust its learned model after the world changes. The RL problem is a continuing gridworld whose layout changes midstream; the agent keeps acting and learning without reset. The implemented methods compare random keep-model planning, oracle model flushing, recency-weighted model aging, and recency/error-gated model aging. The experiment varies planning budgets `1, 5, 20` and model-handling rules; the main metrics are average reward, stale-backup rate, model error, planning TD magnitude, and post-change recovery window. The current result shows that recency aging sharply reduces stale backups and can improve late reward at high planning budget. The key remaining experiment is a longer sweep plus a stochastic or gradually drifting environment where staleness is less artificially clean.

## Research Motivation

The Alberta Plan gives learned models and planning a central role in a long-lived agent. The hard version of planning is not stationary gridworld acceleration; it is deciding which learned predictions still deserve computation. A replay-buffer framing would store old experience and sample it later, but this project instead uses a compact learned model whose entries are updated online. That distinction matters: the question is not how to train from old data, but how a streaming agent should allocate background computation when its model may be wrong.

The current Dyna Planning Budget study already shows a tradeoff: planning helps before a change, but keeping the old model produces high stale-backup rates afterward. The integrated proposal turns that diagnostic into a stronger research problem by testing model aging, recency weighting, and search-control rules.

## Research Question

How should a small continual Dyna agent allocate planning backups when model knowledge has unknown freshness?

Subquestions:

- How much pre-change benefit is lost when model entries are aged aggressively?
- Can stale-backup diagnostics predict post-change recovery?
- Is flushing the model too crude compared with gradual aging?
- Does prioritizing recent model error improve real-step reward or only make planning look cleaner?

## Related Work

The Alberta Plan frames transition models and background planning as components of a base agent. Average-reward learning/planning work motivates continuing objectives. Classic Dyna and prioritized sweeping motivate model-based backups and search control. Continual RL foundations motivate process metrics such as recovery time and adaptation rather than final policy score alone.

Useful local sources:

- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`
- `resources/alberta_plan_related/average_reward_learning_planning_2006.16318.pdf`
- `resources/alberta_plan_related/rethinking_foundations_continual_rl_2504.08161.pdf`

## Research Method

The agent maintains a compact state-action model:

- estimated next state,
- estimated reward,
- last update time,
- count or confidence,
- recent prediction error.

Planning variants:

- No planning.
- Random Dyna with kept model.
- Flush-on-change oracle diagnostic.
- Recency-aged Dyna: planning priority decays with time since real observation.
- Error-gated Dyna: entries with recent high model error are temporarily suppressed.
- Stale-error-prioritized Dyna: backups are chosen by a mixture of TD priority and model freshness.

The flush-on-change variant is not realistic; it is an upper-bound diagnostic showing what would happen if the agent had a perfect change detector.

## Experimental Design

Primary environment:

- Continuing gridworld with goals and hazards.
- Midstream layout change with no reset.
- Planning budgets `0, 1, 5, 20`.
- Aging half-lives `250, 750, 1500, 4000` steps in the extended code path.
- Seeds `0-19` for final results.

Secondary environment:

- Planned, not yet implemented: a small stochastic queue or random-walk model where transition probabilities drift gradually instead of changing abruptly. This prevents the result from depending only on a single blocked-maze event.

Metrics:

- Real-step average reward.
- Pre-change AUC.
- Post-change recovery time.
- Stale-backup rate.
- Model one-step prediction error.
- Planning utility: improvement in TD target or value estimate per backup.
- Fraction of planning spent on entries not observed recently.

## Expected Results And Failure Modes

Expected pattern: random keep-model Dyna should achieve strong pre-change performance but high stale-backup rates after change. Flush should remove stale backups but may lose useful knowledge. Aging should form an intermediate regime: less harmful than keep-model and less forgetful than flush.

Failure modes:

- Aging may be equivalent to lowering planning budget.
- Model error may be delayed because the agent stops visiting changed states.
- A deterministic gridworld may make stale detection too easy.
- Stochastic drift may make aggressive aging unnecessarily pessimistic.

## Interpretation Standard

The proposal succeeds if it explains when planning computation should be trusted. It does not need a universally best aging rate; a tradeoff curve is scientifically valuable if it reveals how model freshness, planning budget, and recovery interact.

## Results

The current Dyna result shows that five planning backups improve pre-change reward relative to no planning, but stale backups remain high after a layout change when the model is kept. This is evidence that the problem is real.

The dedicated large-proposal pilot now adds online model-freshness heuristics:

`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main`

Main result:

- Recency aging reduces stale-backup rate without oracle change detection.
- At planning budget `20`, keep-model stale-backup rate in the late post-change window is about `0.336`, while recency aging reduces it to about `0.0064`.
- At the same budget, recency aging has the best late reward among tested modes, about `0.073`, compared with about `0.068` for keep-model and `0.057` for oracle flush.
- At planning budgets `1` and `5`, stale backups are reduced but reward recovery remains weak. This suggests that freshness control needs enough planning budget to matter.

Main figures below use late post-change seed-tail condition summaries with 95% confidence intervals. This is more readable than the earlier many-series learning curves and focuses the plot on the research question: whether fresh model selection reduces stale planning after change.

![Late average reward by planning budget and model mode.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main/figures/report_avg_reward_post_late_by_budget.png)

![Late stale-backup rate by planning budget and model mode.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main/figures/report_stale_backup_rate_post_late_by_budget.png)

![Late model error by planning budget and model mode.](../../../../experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main/figures/report_mean_model_error_post_late_by_budget.png)

## Reviewer Critique And Revisions

Strict reviewer challenge: "This is just Dyna-Q with a changing maze." Response: the proposal must report model-freshness diagnostics and planning utility, not only reward.

Strict reviewer challenge: "Flush-on-change is unrealistic." Response: it is retained only as an oracle diagnostic; realistic variants must use recency or prediction error computed from the stream.

## Threats To Validity

The current environment uses an abrupt gridworld layout change, which makes stale model entries easy to define and inspect. That is useful for mechanism diagnosis but may overstate how cleanly freshness can be detected in stochastic or gradually drifting worlds. The reward differences are also small, so conclusions should emphasize stale-backup rate, model error, and recovery windows rather than only mean reward. Finally, the recency half-life is fixed; a fuller study should sweep half-life and add a drifting queue or stochastic transition stream to test whether the same planning-control pattern survives outside a maze.

## Conclusion

This proposal turns Dyna from a generic "more planning helps" story into a sharper Core-RL question about when a continual agent should trust its learned model. The first pilot supports the idea that model freshness is a first-class planning variable: recency aging sharply reduces stale backups and can outperform both keeping the model and oracle flushing in the tested setting. The next step is an extended CPU-task sweep and a second nonstationary environment with gradual drift.

## Reproduction

Current main pilot:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_main.json
```

Extended sweep config:

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/continual_dyna_model_aging/config_extended.json
```
