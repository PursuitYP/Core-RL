# Dyna Planning Budget and Model Staleness

Status: independent proposal with completed main pilot; needs model-aging extension for submission-grade strength.

## Abstract

This proposal studies a continual-learning failure mode for model-based RL. Dyna planning can improve sample efficiency by backing up from a learned model, but in a changing world the same model can become stale and amplify obsolete information. We test a small Dyna agent in a continuing gridworld whose goal and hazard layout change midstream. The current main pilot shows that planning improves pre-change reward, but keeping the old model after the change produces high stale-backup rates and weak recovery. Flush-on-change removes stale backups but is an oracle diagnostic, not a realistic continual mechanism. The study therefore motivates model freshness as a central planning question for long-lived agents.


## Standalone Study Summary

This study asks how a small learned model helps or hurts under a limited planning budget. The RL problem is a continuing gridworld that changes phase midstream; the agent keeps a learned one-step model and performs Dyna backups. The implemented comparison varies planning steps and simple model handling, including keeping stale entries or flushing on change. The experiment measures average reward, stale-backup rate, model size, Q norm, and post-change recovery windows. The current evidence shows a useful tradeoff: planning can help before change, but stale model backups remain high afterward. This study motivates the larger model-aging proposal.

## Research Motivation

The Alberta Plan assigns learned transition models and background planning an important role. A continual agent should use computation between real actions to improve its values and policies. But a model learned from a stream is not timeless truth. If the world changes, planning can spend computation reinforcing values for a world that no longer exists.

This proposal asks a more demanding question than the standard Dyna demonstration. It is not enough to show that planning speeds learning in a stationary gridworld. The real issue is how planning behaves when old model entries compete with new experience under a fixed per-step computation budget.

## Research Question

How does a fixed per-step planning budget trade off pre-change sample efficiency against post-change harm from stale model backups?

Subquestions:

- Does more planning always help before the change?
- Does more planning increase stale computation after the change?
- Does flushing the model expose an upper bound on freshness, and why is that not a realistic agent mechanism?
- What additional online diagnostics are needed before model planning can be trusted in a continual stream?

## Alberta Plan Connection

This proposal is directly connected to:

- learned models;
- background planning;
- limited computation;
- continuing control;
- nonstationarity and temporal uniformity.

The model is a compact transition table, not a replay buffer. The agent does not sample raw stored experience; it performs model-based TD backups from learned state-action entries.

## Related Work

Dyna unifies real experience, model learning, and planning updates. Prioritized sweeping adds search-control ideas about which backups deserve computation. Average-reward planning work supports the continuing-task framing. Continual RL methodology motivates recovery metrics and process diagnostics rather than final score alone.

Local references:

- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`
- `resources/alberta_plan_related/average_reward_learning_planning_2006.16318.pdf`
- `resources/alberta_plan_related/rethinking_foundations_continual_rl_2504.08161.pdf`

## Environment

The main environment is a continuing gridworld with:

- a start region;
- a goal;
- hazards;
- small step cost;
- no terminal training episode reset;
- a midstream phase change that moves the goal and hazards.

The agent uses tabular Q values. During each real step it updates the model for the current state-action pair and optionally performs model backups.

## Methods

Compared settings:

- no planning;
- one Dyna backup per real step;
- five Dyna backups per real step;
- keep the old model after change;
- flush the model at the change.

The flush-on-change condition is intentionally labeled as oracle. It gives the experiment a diagnostic ceiling for model freshness, but a real continual agent would not receive a perfect change signal.

## Experimental Design

Current main pilot:

- Environment size: `9 x 9`.
- Phase change at the midpoint of the stream.
- Planning budgets: `0`, `1`, `5`.
- Model modes: `keep_model`, `flush_on_change`.
- Seeds: `0-4`.
- Steps: `5000`.
- Result path: `experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main`.

Metrics:

- average reward;
- stale-backup rate;
- model size;
- Q norm;
- recovery-window summaries.

Primary figure:

![Dyna average reward by planning budget and model handling.](../../../../experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main/figures/avg_reward_by_planning_steps-model_mode_curve.png)

## Results

Planning improves pre-change reward. With five planning backups, pre-change average reward is about `0.099`, compared with about `0.004` without planning. This confirms that the model is useful before the change.

After the phase change, keeping the model produces high stale-backup rates. In the late post-change window, stale-backup rate is about `0.844` for one backup and about `0.705` for five backups. The exact rate differs by budget because the model and visitation pattern change, but the central problem is clear: a large fraction of planning computation can be spent on obsolete entries.

Flush-on-change removes stale backups but does not automatically solve recovery. Five backups with flush has late post-change reward about `-0.0220`, while five backups with keep-model has about `-0.0270`. The difference is not large enough to claim a solved adaptation mechanism.

## Analysis

The proposal's value is the tradeoff curve. Planning is beneficial when the model is fresh, but harmful or wasteful when the model is stale. This reframes Dyna as a computation allocation problem: the agent must decide not only how many backups to do, but which model entries still deserve trust.

The stale-backup metric is essential. Without it, a reward curve might only show that planning sometimes helps and sometimes does not. Stale-backup rate explains one mechanism behind poor recovery and points toward model aging or change detection.

## Threats To Validity

The change is scheduled and known to the experimenter. The keep-model agent does not know the change, but flush-on-change does. Therefore flush is an oracle diagnostic, not a final agent.

The model is deterministic and tabular. That makes staleness easy to define, but stochastic models may require uncertainty or prediction-error estimates.

The current planning budgets are small. A larger budget grid could reveal nonlinear effects.

The environment has one abrupt change. A stronger proposal should test gradual drift and repeated changes.

## Reviewer Critique And Revisions

Planning reviewer:

- A stationary gridworld would only show a known Dyna benefit.

Revision made:

- Added layout change, keep/flush model modes, stale-backup rate, and recovery windows.

Continual-agent reviewer:

- Flush-on-change violates temporal uniformity if treated as an algorithm.

Revision required:

- Add model-age decay or online model-error gating as realistic mechanisms.

Statistics reviewer:

- Five seeds and one change pattern are not enough for final paper confidence.

Revision required:

- Add seeds `0-19`, planning budgets `0/1/5/20`, change severity, and repeated-change variants.

## Conclusion

Dyna planning is a meaningful independent proposal when framed around model freshness, not just sample efficiency. The current evidence shows both sides of the tradeoff: planning helps before nonstationarity and can spend substantial computation on stale backups after nonstationarity. The next stage should implement model aging or error-gated planning and test whether it improves the reward/staleness tradeoff without relying on an oracle change signal.

## Reproduction

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/dyna_planning_budget/config_main.json
```
