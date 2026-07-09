# Reward-Centered Continuing Sarsa 中文报告

英文对应报告：`report.md`

状态：独立主 proposal，已完成 20 seeds、20000 steps 的 reward-shift / alpha extended sweep。

## 摘要

本课题研究 continuing reinforcement learning 中一个非常基础但容易被忽略的 invariance 要求：在 continuing control task 中，如果给所有 reward 加上同一个常数，任务相关行为原则上不应改变。普通 discounted action-value learning 并不自动满足这个要求，因为 reward offset 会进入 TD error 和 action values 的尺度，尤其当 gamma 接近 1 时，常数 reward shift 会积累成很大的 value offset。本课题在 access-control queue 中比较 discounted Sarsa、reward-centered Sarsa 和 differential Sarsa，检验 online reward centering 是否能减少任意 reward zero-point 带来的学习敏感性。extended 结果显示，discounted Sarsa 的 Q norm 会随着 reward shift 和 alpha 显著膨胀，而 reward-centered 和 differential variants 能保持更稳定的 value scale 和 unshifted reward。本研究不是比较“哪个算法分数更高”，而是问一个 continuing agent 能否用不依赖任意 reward baseline 的单位学习。

## 独立研究总结

本研究测试 continuing control 中的 reward-shift invariance。RL 问题是 access-control queue：agent 观察服务器空闲数量和当前 customer priority，然后持续在线决定 accept/reject，不存在离线训练阶段或 replay buffer。实现的方法是 discounted Sarsa、reward-centered Sarsa 和 differential Sarsa，均使用 tabular/linear action values。实验改变 constant reward shifts，并记录 unshifted reward、accept behavior、high-priority acceptance、reward baseline、TD error 和 Q norm。当前最强证据来自 20 seeds、20000 steps 的 alpha sweep：ordinary discounted Sarsa 会产生明显依赖 reward shift 的 value scale，而 centered 和 differential variants 在 value norm 与 unshifted reward 上更稳定。下一步需要继续补 beta/gamma sensitivity，并在同一条 stream 中途切换 reward origin，检查 reward baseline 的恢复速度。

## 研究动机

Alberta Plan 把智能体看作在 temporally uniform experience stream 中持续行动和持续学习的系统，而不是在 episodic benchmark 中反复 reset 的训练器。在这种设定下，reward origin 是一个很干净的压力测试：如果所有 reward 都平移同一个常数，average-reward continuing task 的 policy preference 不应该改变。长期运行的 agent 不应该因为工程师重新定义 reward sensor 的零点，就需要重新调 step size 或换 representation。

普通 discounted value methods 会破坏这种 practical invariance。gamma 接近 1 时，常数 reward shift 会给 value function 增加一个很大的常数分量；这个分量对 action choice 几乎没有任务信息，却会改变 TD-error magnitude、value norm，并通过 finite step-size effects 影响学习动态。Reward centering 有吸引力，是因为它小、在线、符合课程约束：不需要 replay buffer，不需要 deep network，也不需要 offline fitting。

## 研究问题

核心问题是：online reward centering 是否能让 Sarsa 在 non-episodic continuing control task 中对 constant reward shifts 更稳健？

具体假设是：与 ordinary discounted Sarsa 相比，reward-centered Sarsa 和 differential Sarsa 应该在不同 reward shifts 下表现出更低的 value-scale variation，并保持更稳定的 unshifted task reward。

这个假设关注 invariance 和 learning dynamics，而不是 shifted observed reward 的绝对值。因此所有主要结果都把 learner 看到的 shifted reward 和评价用的 unshifted reward 分开记录。

## Alberta Plan 关联

本课题对应 Alberta Plan 中几个核心主题：continuing problems 而不是 episodic reset tasks；value functions 作为 agent prediction/control 的核心对象；average-reward thinking；从 ordinary experience 中在线适应；用小机制减少 hand-tuned scales 的敏感性。环境和方法刻意保持在 Core RL 范围内，目的是让 value-scale failure 可以被解释，而不是用大模型把机制问题遮住。

## 相关工作

主要参考是 Reward Centering，它说明 subtracting empirical average reward 可以改善 continuing discounted methods 并减少 constant reward-shift sensitivity。Average-reward RL 和 access-control queue 提供了经典 setting。Bellman Error Centering 给出了相关 centered fixed points 的理论视角。Alberta Plan 提供了 continuing agents 和 temporal uniformity 的总体动机。相关本地资料包括 `resources/alberta_plan_related/reward_centering_2405.09999.pdf`、`resources/alberta_plan_related/bellman_error_centering_2502.03104.pdf`、`resources/alberta_plan_related/average_reward_learning_planning_2006.16318.pdf` 和 `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`。

## 环境设计

主环境是 access-control queue。状态包含 free servers 数量和当前 customer priority；动作是 reject 或在 server available 时 accept。unshifted reward 是被接受 customer 的 priority，拒绝或无 server 时为 0。实验中 learner 看到的 reward 是 `observed_reward = unshifted_reward + reward_shift`。这样我们可以构造多个等价的任务描述：任务真实偏好不变，但 reward zero-point 改变。agent 必须在单条 online stream 中学习，没有 replay，没有离线训练，没有 train/test 分割。

这个环境比 two-loop toy 更合适，因为它是 continuing average-reward 风格，有状态分布、accept/reject tradeoff 和 high-priority policy probe；同时它仍然足够小，可以清楚检查 Q norm、reward_bar、TD error 和 policy probes。

## 方法

实验比较三个 on-policy control agents：discounted Sarsa 使用 gamma `0.99`；reward-centered discounted Sarsa 使用 online average-reward estimate；differential Sarsa 使用 gamma `1.0` 和 average-reward correction。所有方法都使用 one-hot state features、epsilon-greedy behavior，并且每个 environment step 只做一次在线更新。

普通 discounted Sarsa 的 TD error 是 `delta = R_{t+1} + gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)`。Reward-centered Sarsa 使用 `delta = (R_{t+1} - r_bar_t) + gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)`，其中 `r_bar <- r_bar + beta (R_{t+1} - r_bar)`。Differential Sarsa 使用 average-reward form：`delta = R_{t+1} - r_bar_t + Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)`，并从同一条 continuing stream 中更新 reward baseline。

## 实验设计

当前 extended sweep 使用 access-control queue，reward shifts 为 `-8, -4, 0, 4, 8`，alpha 为 `0.02, 0.05, 0.1`，seeds 为 `0-19`，每个 condition 运行 `20000` online steps。比较方法为 discounted Sarsa、reward-centered Sarsa 和 differential Sarsa。结果路径是 `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended`。

主要指标包括 unshifted average reward、Q norm、TD-error scale、reward-bar estimate、accept rate 和 policy probes。判断标准不是某个 shifted reward 更高，而是一个方法是否能在不同 reward shifts 下保持 unshifted reward 和 policy probes，同时让 Q norm 和 TD-error scale 近似 invariant。一个方法如果需要为每个 reward shift 单独调 alpha，或者 value norm 因任意 reward offset 膨胀，就不能算解决 continuing reward-origin 问题。

仍未完成的敏感性实验包括 beta values `0.003, 0.01, 0.03`，discounted/centered variants 的 gamma sweep，以及同一条 stream 中途切换 reward origin、不重置 weights 的 nonstationary extension。

## 结果

下面的报告图使用 seed-tail condition summaries，而不是把所有 learning curves 挤在一张图里。它们分别展示 reward、value scale、行为倾向和 divergence，因此更适合支撑 reward-origin invariance 的结论。

![Reward shifts 和 alpha values 下的 tail unshifted reward。](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended/figures/report_avg_unshifted_reward_by_reward_shift.png)

![Reward shifts 和 alpha values 下的 tail action-value norm。](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended/figures/report_q_norm_by_reward_shift.png)

![Reward shifts 和 alpha values 下的 high-priority accept rate。](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended/figures/report_high_priority_accept_by_reward_shift.png)

![Reward shifts 和 alpha values 下的 divergence rate。](../../../../experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended/figures/report_diverged_by_reward_shift.png)

核心结果是更大 seed/alpha sweep 下的 value-scale invariance。Discounted Sarsa 的 Q norm 随 reward shift 和 alpha 强烈增长：在 shift `8`、alpha `0.1` 时，tail Q norm 约 `1875.55 +/- 38.4`，unshifted reward 约 `1.697 +/- 0.147`。这个大 value scale 并不是有用任务知识，而主要是 shifted reward stream 引入的任意 offset。

Reward-centered Sarsa 的 Q norm 小得多，在当前 reward shifts 和 alphas 下大致为 `22-35`，并且没有 divergence。它的 unshifted reward 基本保持在 `2.55-2.60`。Differential Sarsa 也表现出类似的 scale-stability pattern，unshifted reward 约为 `2.55-2.61`，Q norm 也保持在较小范围。ordinary discounted Sarsa 在较大的正负 shifts 和较高 alpha 下明显退化。

## 分析

这个结果应该被理解为 invariance test。一个 robust continuing learner 不应该因为 reward origin 改变而大幅改变 value scale 或 unshifted behavior。Discounted Sarsa 在 extended sweep 中没有通过这个测试；reward-centered 和 differential variants 更接近通过。Differential baseline 很重要，因为如果 differential Sarsa 与 reward centering 表现相似，诚实结论不是 reward centering 唯一解决问题，而是 average-reward-style removal of reward offsets 对 continuing agents 是必要设计思想。Reward centering 是其中一种实用路线，优点是保留 discounted method 结构。

## 局限

当前 extended result 已经使用 20 seeds 和 20000 steps，但仍主要只 sweep alpha。beta 对 average reward estimator 很关键：太慢会在 nonstationary reward origin 下 lag，太快会引入 variance。gamma 也还没有系统 sweep。环境是 canonical access-control queue，适合 Core RL mechanism analysis，但不能直接泛化到 deep agents 或大规模机器人任务。reward shifts 目前在每个 run 内固定，下一步必须加入 midstream reward-origin changes，测试真正的 continual adaptation。

## 审稿式批评与修订

Sutton-style critique：报告不能声称 episodic return improvement，必须聚焦 continuing invariance 和 average-reward reasoning。Experimental critique：最初 5-seed pilot 不足以支撑最终统计结论；这一点已经通过 20-seed extended sweep 部分解决。Baseline critique：differential Sarsa 是严肃 baseline，不应当被放到 appendix。已经完成的修订包括：主环境从 two-loop MDP 升级到 access-control queue；shifted observed reward 和 unshifted task reward 分开记录；运行 seeds `0-19`、steps `20000`、alpha grid 的 extended sweep。仍需修订：beta/gamma ablations 和 midstream reward-shift changes。

## 结论

Reward-Centered Continuing Sarsa 是一个强独立 proposal，因为它提出了一个清楚的 continuing-RL 问题，并且现在有 20-seed extended evidence。结果支持 ordinary discounted Sarsa 对 reward origin 敏感，而 reward-centered 和 differential variants 在 reward shifts 与 alphas 下稳定得多。下一阶段应加入 beta/gamma sensitivity 和 nonstationary reward-origin changes，让课题从 fixed-condition invariance 进一步走向 continual adaptation。

## 复现

主实验：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_extended.json
```

再生成图表：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py \
  --result-dir experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended \
  --y-key avg_unshifted_reward \
  --group-keys algorithm reward_shift alpha

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py \
  --result-dir experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended \
  --y-key q_norm \
  --group-keys algorithm reward_shift alpha
```
