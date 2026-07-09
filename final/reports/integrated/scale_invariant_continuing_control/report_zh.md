# Scale-Invariant Continuing Control 中文报告

英文对应报告：`report.md`

状态：独立综合 Core-RL proposal；已有 fixed-condition pilot 和 no-reset unit-switching extended evidence。当前结论应写成“组合方法防止灾难性不稳定，但 abrupt feature-unit change 后 recovery 仍未解决”，不能写成 unit invariance 已经完全解决。

## 摘要

长期运行的 agent 不应该依赖任意测量单位。在 continuing control 中，给所有 reward 加上常数不会改变任务相关行为；同一组 features 改变单位尺度，也不应改变表示的价值函数本质。但 ordinary discounted value methods 会把 reward shift 变成很大的 value offset，固定 parameter alpha 也会在 feature scale 变化时产生完全不同的 update effect。本课题问 reward centering 和 output-controlled/normalized updates 能否组合成一个小型 streaming Sarsa agent，使其同时对 reward translation 和 feature scaling 更稳健。

## 独立研究总结

本研究测试 continuing control agent 是否能在两个任意问题单位改变时保持稳定：reward zero-point 和 feature vector scale。RL 问题是 continuing access-control queue，agent 在线决定 accept/reject。实现的 agents 包括 discounted Sarsa、reward-centered Sarsa、normalized Sarsa、normalized reward-centered Sarsa 和 normalized differential Sarsa。fixed-condition pilot 交叉 reward shifts `-4, 0, 8` 与 feature scales `one, ten, hundred, uneven`，主要指标包括 unshifted average reward、Q norm、prediction change、divergence 和 policy probes。新增 unit-switching extension 在同一条 stream 中途改变 reward origin 和/或 feature scale，不重置 weights、traces 或 reward baseline。当前证据显示 reward centering 和 feature normalization 解决不同失败模式，并且组合机制明显更稳；但 abrupt no-reset feature-scale switch 后 long-run reward 仍可能下降，所以不能声称 unit invariance 已完全解决。

## Proposal Template Answers / 提案模板回答

Focused RL question：一个小型 online control agent 是否能在 reward origin 和 feature units 改变时保持行为和数值稳定，还是这些任意 measurement conventions 会泄漏进 learning dynamics？这是 combined invariance question，不是 benchmark score question。

Setting / testbed：主环境是 continuing access-control queue with linear action values。它有真实 policy tradeoff，同时足够小，可以检查 Q norm、prediction changes、reward baselines 和 divergence。第二环境是同一 stream 的 no-reset unit-switching 版本。

Implemented comparison：比较 discounted Sarsa、reward-centered Sarsa、differential Sarsa、normalized Sarsa、normalized reward-centered Sarsa 和 normalized differential variants。核心变量是 reward shifts 与 feature scales 的交叉，以及不重置 agent 的在线 reward/feature unit changes。

Metric / figure：只有当方法在 reward shifts 和 feature scales 下同时保持 unshifted reward、policy probes、Q norm、output-change magnitude 和 divergence 稳定时，才支持本 proposal。unit-switching figures 尤其重要，因为它们测试 continual recovery，而不是只测试单独固定条件下的 tuning。

Compute need / fallback：main pilot 和 unit-switching extension 已完成。fixed-condition 20-seed extended CPU sweep 作为 `core-rl-scale-invariant-extended-33723554` 正在运行；在 artifacts 写出前，fallback 是提交 fixed-condition pilot evidence 加更强的 no-reset unit-switching evidence，并明确 full-grid confirmation pending。

## 独立研究范围

这是一个关于 continuing control 中 unit sensitivity 的较大独立研究。它问一个单一 online control learner 在 reward origin 和 feature scale 两种任意 measurement conventions 改变时，是否仍能保持稳定。本研究包含自己的环境、方法、指标、fixed-condition experiment 和 no-reset unit-switching experiment。

本报告不声称一般意义上解决 unit invariance。当前范围是 synthetic but controlled unit manipulations 下的 linear access-control Sarsa。fixed-condition pilot 支持 compositional stability；no-reset extension 则显示 abrupt feature-unit changes 即使避免 catastrophic divergence，也仍会损害长期 reward。

## 证据等级

证据等级：强候选证据，但还不是 final full-grid evidence。已完成 fixed-condition pilot 展示 reward centering 和 update normalization 的 interaction；已完成 20-seed unit-switching run 对 continual-learning relevance 更强，因为它在同一 stream 中改变 units，不重置 weights。运行中的 `20260709T063128Z_extended` fixed-condition sweep 目前没有 artifacts，不能作为 evidence。

当前 claim 必须收紧：combined centering/normalization 在当前测试 variants 和 access-control 设置中对 stable unit changes 是必要的，并且能在 no-reset switches 下避免严重数值不稳定；但它没有完全解决 abrupt feature-scale changes 后的 reward recovery。成熟最终论文还需要 running extended grid、gradual scale drift、beta sensitivity 和 policy-distance probes。

## 论文式贡献与 Claim 边界

本报告的贡献是把两个局部 invariance mechanisms 推进成一个单一 continuing-control 问题：当 reward units 和 feature units 都是任意约定时，agent 能否保持稳定？fixed-condition experiment 测试两个机制是否能组合；no-reset switch experiment 测试这些机制是否能承受更接近 continual interpretation 的单位变化。这使本 proposal 不只是把两个方法拼在一起。

claim 边界是：当前证据支持 tested unit changes 下的稳定性改进，不支持“unit invariance 已解决”。在 access-control setting 中，combined centering/normalization 避免了最严重的 numerical failure，但 abrupt feature-scale switch 仍会降低 long-run reward。真正开放的问题是 unit change 后的 recalibration 和 recovery，而不仅是防止 divergence。

## 研究动机

Alberta Plan 强调从 ordinary experience 中持续学习。对于这样的 agent，单位敏感性不是 cosmetic issue，而是核心稳定性问题。一个长期 agent 不会在 sensor rescale 或 reward baseline shift 后获得干净的重新调参阶段。如果 reward origin 或 feature scale 改变了有效学习问题，那么 agent 的能力就依赖任务外的人为约定。

研究动机来自同一个 control loop 内的单位问题：access-control agent 应该从 reward differences 和 state-action evidence 中学习 accept/reject behavior，而不是依赖 reward zero point 或 one-hot features 的数值大小。combined stress test 有价值，是因为 reward translation 与 feature scaling 会通过 TD-error magnitude、action-value scale 和 effective step size 相互作用。

## 研究问题

核心问题是：linear continuing Sarsa agent 使用 reward-centered TD errors 和 output-controlled step sizes 时，能否在 simultaneous reward translation 与 feature rescaling 下保持 task-relevant behavior？

这个问题比“哪个方法 reward 更高”更严格。正结果必须体现 equivalent problem parameterizations 下 behavior 和 update scale 的 invariance；如果一个方法只在某个 reward shift 或 feature scale 下有效，或需要每个单位单独调 alpha，就不算真正解决。

## 相关工作与 Alberta Plan 关联

Alberta Plan 提供了 continuing agents、average reward、value functions 和 temporally uniform learning 的总体动机。Reward Centering 说明 empirical average reward subtraction 可以减少 continuing discounted methods 的 constant-shift sensitivity。Bellman Error Centering 解释相关 centered fixed point。Intentional Updates 强调 step size 应对应 output change 而不是 raw parameter movement。本项目把这些思想压缩到 tabular/linear Core RL setting 中，以便检查机制。

## 环境设计

主环境是 continuing access-control queue。状态包含 free servers 数量和当前 customer priority；动作是 reject 或 accept；接受高 priority customer 得到更高 unshifted reward；服务器随机释放。fixed-condition experiment 人为改变 reward shift 和 one-hot feature scale，创造等价或近似等价的问题单位变化。

新增 secondary environment 由同一个 access-control stream 构成，但中途改变 reward origin 和/或 feature scale。这个 no-reset unit-switching experiment 更接近 continual setting：agent 的 weights、traces 和 reward baseline 都不重置，必须从当前内部状态继续适应。

## 方法

比较方法包括 discounted Sarsa、reward-centered Sarsa、normalized Sarsa、normalized reward-centered Sarsa 和 normalized differential Sarsa。Reward centering 从 TD target 中减去在线 reward baseline，减少 reward-origin offset。Normalized update 用当前 feature/trace norm 调整 effective alpha，使 alpha 更接近 prediction-output change 的单位。Normalized reward-centered Sarsa 和 normalized differential Sarsa 分别组合 reward-origin correction 与 feature-scale correction。

所有方法都在线交互、在线更新，不使用 replay buffer、不使用 deep network、不做离线训练。这个设计让每个 failure mode 可以解释：reward shift 导致 value offset，feature scale 导致 parameter update 过大，二者同时出现时会暴露组合机制是否真正互补。

## 实验设计

fixed-condition pilot 使用 result path `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`。该 pilot 交叉 reward shifts `-4, 0, 8` 和 feature scales `one, ten, hundred, uneven`，评估 tail unshifted reward、Q norm、prediction change、divergence 和 policy probes。

unit-switching extension 使用 result path `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`。该 run 使用 seeds `0-19`、`20000` online steps、alpha values `0.01, 0.03, 0.1`，并在 stream 中途执行四类 switch：reward_shift_only、feature_scale_only、joint_reward_scale 和 joint_reward_lognormal。评价指标包括 recovery_window 中的 unshifted reward、Q norm、divergence 和 prediction_change。

尚未完成的是 full fixed-condition `scale_invariant_continuing_control/config_extended.json`，它会进一步扩展 shifts/scales/alphas。unit-switching 已经回答了一个更严格的问题，但不能替代完整 fixed-condition grid。

## 实验设计依据

设计刻意交叉两个 nuisance dimensions，因为单一机制各自有合理但不完整的故事。reward centering 在 scale one/current alpha 下能很好处理 reward-origin offset，但不能控制 feature-driven parameter update 的大小；normalization 应该控制 feature-scale effects，但不能移除 reward shift 引入的 constant value component。combined grid 因此是 compositional test：只处理一个 nuisance dimension 的方法应当在另一个 dimension 下失败。

no-reset unit-switching extension 用来避免 fixed-condition sweep 隐含的 retuning assumption。continual agent 不应在 sensor rescale 时获得 fresh weights。switch experiment 因此测量 early/late post-change reward、Q norm 和 divergence。`hundred` scale switch 是故意严苛的，用于区分“只避免 numerical explosion”和“真正恢复 useful behavior”。

## 结果

fixed-condition pilot 显示两个机制是互补的：reward-centered Sarsa 单独可以处理 reward shift，但在 feature scale `ten` 或 `hundred` 时会失败；normalized Sarsa 能控制 feature scale，但仍受 reward shift 影响；normalized reward-centered Sarsa 和 normalized differential Sarsa 在当前 sweep 中最稳，tail unshifted reward 大致保持 `2.4-2.5`，并且没有 divergence。

![Tail unshifted reward by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_avg_unshifted_reward_by_scale.png)

![Tail Q norm by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_q_norm_by_scale.png)

![Tail output-change magnitude by algorithm, reward shift, and feature scale.](../../../../experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main/figures/report_prediction_change_by_scale.png)

unit-switching extension 让结论更严格也更诚实。Fixed discounted Sarsa 在 feature-scale-only 或 joint_reward_scale switch 后可能出现巨大 Q norm，早期 post-change window 中 Q norm 可到约 `1e8` 并有非零 divergence。Normalized reward-centered 和 normalized differential variants 避免了 catastrophic divergence，支持核心 stability claim。但它们没有完全解决 abrupt `hundred`-scale no-reset recovery：在 feature-scale 或 joint-scale switch 后，late unshifted reward 经常降到约 `1.9-2.0`。相比之下，reward_shift_only 和 lognormal-scale switch 更容易恢复。

![No-reset unit switches 后的 post-late reward。](../../../../experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended/figures/report_unit_switch_reward_heatmap.png)

![No-reset unit switches 后的 post-late Q norm。](../../../../experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended/figures/report_unit_switch_q_norm_heatmap.png)

![No-reset unit switches 后的 post-late divergence。](../../../../experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended/figures/report_unit_switch_divergence_heatmap.png)

## 分析

最重要的 insight 不是“组合方法分数最高”，而是两个单独机制的失败边界不同。Reward centering 主要移除 reward-origin nuisance component，但不能控制 feature norm 变大导致的 update explosion。Normalization 主要控制 feature-scale sensitivity，但如果 reward baseline 产生巨大 value offset，它仍然不能保证 behavior invariance。组合机制在 fixed-condition pilot 中表现最好，说明两个 correction 方向可以组合。

unit-switching 进一步说明，稳定性和恢复性是两个层次。组合方法能避免 fixed discounted Sarsa 的灾难性发散，但 abrupt feature-scale switch 会让已学 value weights 与新 feature units 不匹配，导致 long-run reward 降低。这个结果很有研究价值，因为它把下一步问题从“是否需要 centering/normalization”推进到“如何在 no-reset unit change 后快速重新校准 internal values”。

## 局限

当前证据比初版 pilot 强，但仍不是完成版 empirical paper。Access-control queue 是有意义的 continuing-control testbed，但仍是 compact synthetic task。feature-scale manipulation 是人为设计的 invariance test，不代表真实 sensor drift 一定如此。unit-switching 使用 abrupt switch，比 gradual drift 更激烈；下一步应加入 gradual feature-scale drift、reward baseline beta sensitivity 和全状态 policy-distance probes。full fixed-condition 20-seed grid 也还没有完成。

## 审稿式批评与回应

批评一：“你只是把两个 tricks 组合起来。”回应：科学对象不是 trick，而是 arbitrary problem units 下的 invariance；组合实验有价值，因为它检验两个看似独立合理的 normalization 是否互补或干扰。批评二：“Access-control 还是小。”回应：Core RL 机制研究允许小环境，前提是 manipulation sharp 且 diagnostics 能解释机制。新增 unit-switching experiment 已经比 fixed-condition pilot 更严格，并且它暴露了组合方法仍未完全解决的恢复问题。

逐 proposal 审查矩阵：

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| Alberta Plan | unit invariance 必须服务 continual agents，而不是 synthetic stress。 | 加入 no-reset unit-switching stream，并以 temporal-uniform learning 下 measurement conventions 改变为问题。 | 真实 sensor drift 尚未建模。 |
| Core RL | 研究可能被误解成两个 tricks 的松散组合。 | 报告定义单一 combined invariance question，并在同一个 control setting 中测试 interaction failures。 | 仍需 running full-grid extended sweep。 |
| Stability | 避免 divergence 不等于 control 好。 | 报告 unshifted reward、Q norm、output change 和 divergence。 | 仍缺 policy-distance probes 和 recovery AUC。 |
| 统计 | fixed-condition pilot 弱于 unit-switch extension。 | 分离 pilot evidence 和 completed 20-seed unit-switch evidence。 | running extended fixed grid 尚无 artifacts。 |
| 严格老师 | 不要声称 unit invariance 已解决。 | 结论明确 abrupt feature-scale recovery 仍开放。 | 仍需 gradual drift 和 beta/gamma sensitivity。 |

## 结论

Scale-Invariant Continuing Control 有清晰问题、可解释 continuing-control environment、非平凡机制交互和严格的 no-reset extension。当前最诚实的结论是：centering 和 normalization 分别处理不同的 unit sensitivity，组合机制显著提高稳定性；但 abrupt feature-unit switch 后的完全恢复仍未解决。下一步应等待 full `scale_invariant_continuing_control/config_extended.json` 结果，并设计 gradual unit drift 版本。

## 复现

fixed-condition pilot：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_main.json
```

unit-switching extension：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/unit_switching_continuing_control/config_extended.json
```

再生成 fixed-condition 报告图：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind scale \
  --result-dir experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main
```
