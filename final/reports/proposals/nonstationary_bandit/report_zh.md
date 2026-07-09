# Nonstationary Bandit Sanity Check 中文报告

状态：独立 sanity diagnostic；不具备最终 Core RL 主 proposal 的深度。

## 摘要

本 proposal 使用 drifting multi-armed bandit 检验最小形式的 continual adaptation：当 best action 漂移时，action values 必须持续变化。当前 run 显示 constant-alpha action-value estimates 比 sample averages 更能适应非平稳 reward，而 sample averages 会变得 stale。这个实验适合教学和 pipeline sanity check，但它缺少 state、bootstrapping、time-extended value functions、planning、GVFs 和 temporal abstraction，因此不应作为强最终 Core RL project。

## 研究动机

在研究更复杂 continual RL mechanism 前，先验证一个最简单原则是有用的：nonstationary stream 中的 online learner 需要 persistent plasticity。Sample averages 会不断累积旧数据，在 reward drift 下可能变差；constant step sizes 让 learner 保持响应能力。

Bandit setting 很好地隔离了这个思想，但也正因为太隔离，它的科学深度有限。

## 研究问题

主问题：哪种简单 online bandit update 在 drifting action values 下保持 plasticity？

假设是：当 action values 漂移时，constant-alpha updates 应比 sample averages 更能适应。

## Alberta Plan 关联

该 proposal 与 continual adaptation 和 online learning 间接相关，但没有触及多数 Alberta Plan 组件：没有 state construction、没有 value-function bootstrapping、没有 learned model、没有 planning、没有 options。因此它应保留为 sanity diagnostic，除非扩展为 contextual bandit 或 continuing control problem。

## 环境与方法

环境是 drifting multi-armed bandit，stream 后半段发生 reward shift。没有 state 和 transition dynamics。比较方法包括 sample-average action values、constant-alpha action values、gradient bandit without baseline 和 gradient bandit with baseline。

## 实验设计

当前 main diagnostic 使用 seeds `0-4`、steps `5000`，结果路径是 `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`。主要指标包括 best-action rate、cumulative regret 和 reward。

![Best-action rate in drifting bandit.](../../../../experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main/figures/best_action_rate_by_algorithm_curve.png)

## 结果

Constant-alpha action values 是该 diagnostic 中最强方法，tail best-action rate 约 `0.306`。Sample-average updates 在 drift 下表现很差，tail best-action rate 约 `0.009`。结果支持预期 lesson：sample averaging 对 nonstationary stream 不够 plastic。

## 分析

结果是正确的，但很浅。它能帮助解释为什么后续 proposals 关注 constant step sizes、TIDBD、output control 和 recovery windows；但它本身没有回答足够丰富的 Core RL 问题。

升级方向是把它变成 contextual bandit 或 continuing access-control with drifting priorities，并引入 representation scale、reward centering 或 partial observability。否则它只适合作为 introduction 或 appendix。

## 有效性威胁

没有 state、没有 bootstrapping、没有 learned model 或 planning。Best-action rate 在 5 seeds 下较 noisy。Reward shift 比真实非平稳简单得多。整体距离 Alberta Plan 的 value-function spine 较远。

## 审稿式批评与回应

Course-project reviewer 会说：这个实验有用但太基础，不适合作为最终 proposal。回应是：报告明确把它降级为 independent sanity check，不作为 submission-grade project。

## 结论

Nonstationary Bandit 是有用的 plasticity sanity diagnostic，但不应升级为主要最终 Core RL study。它的角色是帮助读者理解 continual learners 为什么需要 persistent adaptation。

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/nonstationary_bandit/config_main.json
```
