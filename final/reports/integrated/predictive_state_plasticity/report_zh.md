# Predictive State Plasticity 中文报告

英文对应报告：`report.md`

## 摘要

Predictive knowledge 是 Alberta Plan 的核心思想之一，但一个 prediction 只有在改善 learning 或 control 时才对 agent 有价值。当前 extended GVF predictive-state 实验是一个明确的负结果：trace memory 和 oracle memory 能解决 partially observable T-maze，而 learned GVF state 即使在 20 seeds、20000 online steps、maze length 到 30 的设置下仍接近 chance。这个失败不是废结果，而是把研究问题变得更尖锐：streaming agent 在有限 features 下，如何选择、适应并保留真正携带 control-relevant hidden information 的 predictions？

## 独立研究总结

本研究问 learned predictions 是否能在 partial observability 下成为对 control 有用的 state。RL 问题是 T-maze：trial 开始时出现短暂 hidden cue，之后 agent 进入 aliased corridor，直到 junction 才需要根据早期 cue 做动作；如果 agent 没有保留 cue 信息，raw observation 不足以解决任务。当前实现比较 raw features、hand-coded trace memory、recurrent GVFs、redesigned cue GVFs 和 oracle memory，control learner 是 online linear Sarsa。extended experiment 使用 20 seeds 和 20000 online steps，跨 maze lengths `8, 12, 20, 30` 评估 representation mode；主要指标是 trial accuracy、cue-alignment margin、GVF TD error 和 control TD error。结果是有价值的 negative gate：cue-GVF 有一些 cue-aligned signal，但没有把控制表现提升到 chance 以上；trace 和 oracle memory 能解决任务。下一步必须拆开 GVF question design、output scaling、control utilization 和 feature-selection/plasticity mechanisms。

## 研究动机

Partial observability 让当前 observation 不足以定义 Markov state。长期 agent 必须从历史中构造 state，但课程约束排除了 deep recurrent networks 和 replay。GVFs 提供了一个 Core-RL 路线：关于未来 signals 的 predictions 可以成为 features。Generate-and-test 提供了资源机制：生成 candidate features 并淘汰弱 features。TIDBD 提供了 plasticity 机制：按 feature 调整 step sizes。但真正重要的问题不是每个机制单独看起来是否合理，而是 agent 能否在有限容量下保持 useful predictive state。

这个 proposal 的价值在于拒绝“加 GVF 就有用”的浅结论。一个 GVF 可能预测得很准，但预测的是容易学习、与控制无关的 cumulant；也可能在局部有 cue-aligned signal，却无法被 downstream control update 使用。T-maze cue task 专门把这个问题暴露出来：如果 prediction 不能把早期 cue 信息带到 junction，它就不是 useful state。

## 研究问题

核心问题是：在 observations aliased 且 memory timescale 变长时，什么样的 predictive question design、feature replacement 和 step-size plasticity 能帮助 streaming linear agent 维护 useful state？

当前 first-gate 子问题更具体：在没有复杂 feature plasticity 前，固定 learned GVF features 是否已经能胜过 raw observation，并接近 trace/oracle memory？如果这个 gate 都不过，就不应直接宣称 predictive-state plasticity 成功。

## 相关工作与 Alberta Plan 关联

Alberta Plan 强调 GVFs、feature finding 和 agent-state construction。Horde 展示了大量 off-policy predictions 可以并行学习。Useful-prediction 相关工作提醒我们，prediction accuracy 不是最终目标；prediction 必须对 agent 的后续 learning/control 有用。Recurrent generate-and-test 和 TIDBD 分别提供 state features 与 feature-wise learning rates 的 adaptation 机制。相关本地资料包括 `resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`、`resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`、`resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf`、`resources/alberta_plan_related/tidbd_1804.03334.pdf`、`resources/alberta_plan_related/streaming_deep_rl_finally_works_2410.14606.pdf` 和 `resources/alberta_plan_related/squeezing_more_from_stream_2602.09396.pdf`。

## 环境设计

主环境是 aliased T-maze。每个 trial 开始时 cue 指示左或右，cue 只在起点 observation 中出现；之后 agent 进入走廊，走廊 observation 被 alias，不能区分早期 cue；到 junction 时 agent 必须根据起点 cue 选择动作。正确选择得到正 reward，错误选择得到负 reward，然后新 trial 开始。这个环境专门用于区分 raw observation、cheap trace memory、oracle memory、learned GVF feature 和后续 plasticity 机制。

这个环境的研究用途很明确：它不是为了追求复杂 benchmark 分数，而是迫使 learned state 必须携带 hidden cue information。如果 trace/oracle 可以解决而 GVF 不行，那么失败点就在 predictive feature 的信息、尺度或 control utilization 上，而不是环境本身不可解。

## 方法

当前实现的 representation modes 包括 raw observation、trace memory、recurrent GVF、cue GVF 和 oracle memory。Raw observation 是最低 baseline；trace memory 是便宜但手工设计的 cue retention baseline；oracle memory 直接提供 hidden cue，是上界；recurrent GVF 尝试通过预测 terminal cue/outcome 维持信息；cue GVF 直接预测 cue cumulants，希望更明确地把 cue 信息带入 state。所有 control learners 都是 online linear Sarsa，不使用 replay，不使用 deep network。

GVF 与 control learner 都在线更新。评价不是 GVF TD error 单独低不低，而是 GVF output 是否携带 hidden cue，并且 downstream control 是否能利用它提高 trial accuracy。

## 实验设计

当前 extended first-gate run 使用 maze lengths `8, 12, 20, 30`，modes 为 raw、trace_memory、recurrent_gvf、cue_gvf 和 oracle，seeds 为 `0-19`，每个 condition 运行 `20000` online steps。结果路径是 `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`。

主要指标包括 trial-end accuracy、average reward、GVF TD error、cue-alignment margin、control TD error。解释标准是：只有 learned prediction 明显携带 hidden cue，并把 control accuracy 提升到 raw observation 以上且接近 cheap trace baseline，才可以说它是 useful state。只要 GVF 有非零 cue alignment 但 control 仍 near chance，就只能算 diagnostic signal，不算解决 predictive-state 问题。

## 结果

![Tail trial accuracy by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_trial_accuracy_by_maze_length.png)

![Tail cue-alignment margin by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_cue_alignment_margin_by_maze_length.png)

![Tail GVF absolute TD error by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_gvf_abs_td_error_by_maze_length.png)

extended 结果非常清楚。Oracle memory 在所有长度上保持高准确率，约 `0.931-0.950`。Trace memory 在短中长度上接近 oracle，在 length `30` 时下降到约 `0.827 +/- 0.013`，但仍明显高于 chance。Raw observation 接近 chance。Recurrent GVF 也接近 chance。Cue-GVF 在长度 `8,12,20,30` 上的 trial accuracy 分别约 `0.504, 0.508, 0.505, 0.494`，没有形成有效 control state。

cue-GVF 的 cue-alignment margin 在较短长度上有一些正信号，但随 maze length 增长变弱，而且这点信号没有转化为 control accuracy。这正是本课题的核心 insight：prediction signal 不等于 useful state；一个 feature 只有在 downstream control update 能稳定使用它时才有意义。

## 分析

这个结果应被视为 negative gate，而不是失败后放弃。它告诉我们当前 GVF question 和 feature scaling 不足以支撑控制，下一步应该先做更细的 diagnostic，而不是直接堆 generate-and-test 或 TIDBD。可能的失败原因包括：GVF cumulant/horizon 设计不对；GVF output scale 不适合 Sarsa control；control step size 没有针对 predictive feature 调整；cue signal 虽然存在但不够 linearly separable；或者 cheap trace memory 本身就是这个任务的强 baseline。

因此，下一个严谨版本应先加入 oracle-prediction control、cue decodability probe、GVF output normalization、feature ablation，再考虑有限 feature budget 下的 generate-and-test 和 per-feature step-size adaptation。

## 局限

当前实验是 controlled partial-observability test，不是大型真实世界任务。它只证明当前 GVF 设计在这个尖锐 setting 下没有成为 useful state，不能证明所有 GVF 都无用。trace memory 是 hand-coded strong baseline，可能过强，但它恰好提供了重要标准：如果 learned prediction 连 cheap trace 都比不过，就不能声称 predictive state construction 成功。当前还没有 phase-change experiment，也没有完整接入 feature replacement 和 TIDBD。

## 审稿式批评与修订

严格审稿人可能会问：“GVF 是负结果，为什么还继续？”回答是：负结果正是设计信号，说明当前 GVF question 没有把 cue 信息变成可用控制 state。另一个批评是课题太大。对此，proposal 应分层推进：先验证 fixed useful GVF questions，再做 limited-budget selection，最后做 step-size plasticity；不能在第一层没通过时直接宣传 combined plasticity 成功。当前修订已经把报告明确定位为 negative/redesign gate，并通过 20-seed extended run 加强证据。

## 结论

Predictive State Plasticity 是一个有野心但高风险的课题。它的价值不是证明“加 GVF 有用”，而是严肃检验 predictions 是否真的能成为 partial observability 下的 useful state。extended first-gate 结果显示，当前 cue-GVF 有一点 cue-aligned information，但不是有用 control state。这个负结果很有研究价值，因为它明确提出下一步设计约束：predictive feature 必须既包含 hidden variable information，又能被 downstream control update 使用。

## 复现

运行 extended first-gate：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/predictive_state_plasticity/config_extended.json
```

再生成报告图：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind predictive-state \
  --result-dir experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended
```
