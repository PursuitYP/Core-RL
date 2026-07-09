# Nonstationary Bandit Plasticity 诊断

状态：独立的 limited-scope plasticity study。结果有用且可复现，但仍不足以支撑 submission-grade Core RL claim。

## 摘要

本研究把 drifting multi-armed bandit 作为 continual adaptation 的最小测试。聚焦问题是：一个基础 online learner 在没有 replay 的情况下，是否还能保持足够 plasticity 来跟踪变化中的 action values。实验确认了预期现象：reward distribution 改变后，constant-alpha action-value estimates 比 sample averages 更能适应。

这个结果是有效的独立 study，其范围刻意保持狭窄。它回答了一个窄 plasticity question，并检查了 experiment pipeline、绘图和解释语言。它的限制同样重要：该任务没有 state、没有 temporal credit assignment、没有 bootstrapped value functions、没有 learned model、没有 planning，也没有 options。因此它应作为 bounded plasticity result 来推动更丰富的 Core RL settings，而不是单独作为完整 Core RL project。

## 1. Proposal Template Answers / 提案模板回答

Focused RL question：在 nonstationary reward stream 中，哪种基础 online bandit update 能在 best action 改变后保持 plasticity？

Setting/testbed：一个 drifting multi-armed bandit，具有 stochastic rewards，并在 stream 后半段发生 reward-distribution shift。

Implemented comparison：Sample-average action values、constant-alpha action values、gradient bandit without reward baseline、gradient bandit with reward baseline。

Observation or metric：Best-action rate 是主诊断指标；cumulative regret 和 reward 是辅助指标。

Expected behavior：Constant-alpha updates 应在 shift 后恢复更好，因为有效 step size 不会随时间趋近于零。Sample averages 应适应较差，因为早期 rewards 保留了过多影响。

Compute need：很小的 CPU-only run，五个 seeds，5000 online steps。

Fallback：把结果保留为 introductory plasticity diagnostic。更强项目需要 state、bootstrapping、value prediction、continuing control 或 average-reward structure。

## 2. Research Motivation / Question / Method / 研究动机、问题与方法

Continual RL 面临一个基本压力：agent 必须持续从统计性质可能变化的 stream 中学习。如果一个过去好的 action 后来变差，平均所有过去 rewards 的 estimator 就会被过时经验锚定。Constant step size 给 learner 一个有限记忆，使旧证据逐渐衰减。

研究问题被刻意保持为最小形式：best arm 改变后，哪种简单 online update 保持 plasticity？假设是 constant-alpha action-value learning 会比 sample-average learning 更容易恢复。Gradient bandit variants 作为轻量比较加入，而不是作为新 bandit algorithm 的 claim。

方法只使用 online interaction。每一步 learner 选择一个 arm 并得到 stochastic reward。除了 action choice 以外没有 state observation，没有 transition dynamic，也没有 long-horizon return。这隔离了 plasticity，但也移除了更强课程主题中的许多机制。

## 3. Experimental Design / 实验设计

Main run：

- Seeds：`0-4`。
- Steps：`5000`。
- Config 中的 environment label：`drifting_bandit_reward_shift`。
- Result path：`experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`。
- Primary metrics：`best_action_rate`、`cumulative_regret` 和 `reward`。

主图：

![Best-action rate in drifting bandit.](../../../../experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main/figures/best_action_rate_by_algorithm_curve.png)

这个设计是最小机制检查。主要观察是 learning rule 在 reward shift 后是否恢复，而不是 bandit setting 是否足以建模 continual RL。

## 4. Results / 结果

观察到的排序符合假设。Constant-alpha action values 在该 diagnostic 中最强，seed-tail mean best-action rate 约为 `0.306`。Sample-average updates 在 drift 下很差，seed-tail mean best-action rate 约为 `0.009`。

两个 gradient bandit variants 在这次 run 中位于二者之间：no-baseline variant 的 seed-tail mean best-action rate 约为 `0.176`，baseline variant 约为 `0.155`。Seed-tail summary 的 cumulative regret 也支持 constant-alpha learning，constant alpha 约为 `2838`，sample averaging 约为 `4321`。

由于只有五个 seeds，且部分 learners 的 confidence intervals 很宽，证据有噪声。但定性模式足以支持 diagnostic claim：persistent step sizes 有助于在该 nonstationary bandit stream 中保持 adaptation。

## 5. Analysis / 分析

机制很直接。Sample averaging 给早期 rewards 较高累积权重，并逐渐降低新证据的影响。Best action 改变后，旧 estimate 仍然主导，因此 learner 恢复缓慢，或没有足够频率重新访问新的 best arm。Constant-alpha learning 保持固定 learning rate，因此更容易跟踪改变后的 reward distribution。

这个机制与 persistent adaptation、step-size adaptation、reward centering 和 recovery windows 有关。但 bandit 没有测试 value predictions 是否跨时间 bootstrap，representations 在 observation 改变时是否仍有用，也没有测试 planning 和 control 是否改善 ordinary experience。增加 arms、seeds 或 plots 会让 diagnostic 更干净，但本身不会使问题成为更强 Core RL study。

## 6. 局限与有效性威胁

- 实验只有五个 seeds，best-action rate 比较 noisy。
- Reward shift 比真实 nonstationarity 简单。
- 环境移除了 state、bootstrapping、delayed consequences 和 function approximation。
- Gradient bandit settings 是轻量比较，不是充分调参的 baselines。
- Best-arm identification 不等同于 value prediction、average-reward control 或 temporally extended behavior。

## 7. Reviewer Critique / 审稿批评

| Reviewer critique | 当前回应 | 必要下一步 |
|---|---|---|
| 问题对 Core RL 来说太浅。 | 报告明确标为 limited-scope plasticity result。 | 若恢复，应围绕 contextual prediction、continuing control 或 average reward 重设计。 |
| 五个 seeds 太少，不能支撑强 empirical claim。 | Claim 是定性且受限的。 | 只有在 diagnostic 本身仍有价值时再增加 seeds。 |
| Bandit 没有 temporal credit assignment。 | 该限制被作为隔离结果的理由。 | Final project 应转向小型 Markov 或 continuing-control task。 |
| Gradient bandit comparisons 没有深入分析。 | 它们只作为轻量参考。 | 没有单独设计前，不围绕它们建立 final claim。 |

## 8. Conclusion / 结论

这个 proposal 是独立且结论受限的 plasticity study：它确认在 drifting bandit 中，constant step sizes 比 sample averages 更能保持 plasticity，但不建立 submission-grade Core RL result。它最合适的用途是记录一个最小 adaptation phenomenon，并推动带 state、value functions 或 continuing control 的更丰富重设计。

## 9. Reproduction / 复现

从仓库根目录运行：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/nonstationary_bandit/config_main.json
```

预期 result directory：`experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`。
