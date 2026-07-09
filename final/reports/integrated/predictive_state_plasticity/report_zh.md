# Predictive State Plasticity 中文报告

英文对应报告：`report.md`

状态：独立高风险 proposal。当前可提交证据是 20-seed first-gate negative study：learned cue-GVF features 还没有成为 useful control state。cue-decodability analysis 已经作为机制 probe 加入。limited-budget feature replacement 和 feature-wise plasticity 是本研究内部的后续阶段，不是当前已经完成的正向证据。

## 摘要

Predictive knowledge 是 Alberta Plan 的核心思想之一，但一个 prediction 只有在改善 learning 或 control 时才对 agent 有价值。当前 extended GVF predictive-state 实验是一个明确的负结果：trace memory 和 oracle memory 能解决 partially observable T-maze，而 learned GVF state 即使在 20 seeds、20000 online steps、maze length 到 30 的设置下仍接近 chance。这个失败不是废结果，而是把研究问题变得更尖锐：streaming agent 在有限 features 下，如何选择、适应并保留真正携带 control-relevant hidden information 的 predictions？

## 独立研究总结

本研究问 learned predictions 是否能在 partial observability 下成为对 control 有用的 state。RL 问题是 T-maze：trial 开始时出现短暂 hidden cue，之后 agent 进入 aliased corridor，直到 junction 才需要根据早期 cue 做动作；如果 agent 没有保留 cue 信息，raw observation 不足以解决任务。当前实现比较 raw features、hand-coded trace memory、recurrent GVFs、redesigned cue GVFs 和 oracle memory，control learner 是 online linear Sarsa。extended experiment 使用 20 seeds 和 20000 online steps，跨 maze lengths `8, 12, 20, 30` 评估 representation mode；主要指标是 trial accuracy、cue-alignment margin、GVF TD error、control TD error 和 cue-decodability。结果是有价值的 negative gate：cue-GVF 含有弱 cue information，但没有把控制表现提升到 chance 以上；trace 和 oracle memory 能解决任务。下一步必须继续拆开 GVF output scaling、control utilization 和 feature-selection/plasticity mechanisms。

## Proposal Template Answers / 提案模板回答

Focused RL question：在 partially observable online control task 中，learned predictions 能否携带 later action 所需的 hidden cue information，还是 agent 需要不同的 state-construction mechanism？当前报告回答的是 fixed learned GVF features 的 first-gate question，不是已经完成的 feature-plasticity result。

Setting / testbed：testbed 是 aliased T-maze，包含 early binary cue 和 delayed junction decision。它不是普通 benchmark，而是 sharp diagnostic：raw observation 不足，trace/oracle memory 可以解决，learned predictive state 必须证明自己携带 useful hidden information。

Implemented comparison：已完成实验比较 raw observation、trace memory、recurrent GVF、cue GVF 和 oracle memory，并使用 online linear Sarsa。candidate-feature replacement、feature-wise step-size adaptation、feature ablation 和 phase-change plasticity 是 staged next experiments，不是当前 evidence。

Metric / figure：主证据是不同 maze length 下的 trial accuracy，并用 cue-alignment margin 和 GVF TD error 辅助解释。低 GVF TD error 或小的正 cue-alignment signal 不够；learned prediction 必须提高 junction decisions，相比 raw observation 更好并接近 trace/oracle memory。

Compute need / fallback：extended first-gate run 已完成。如果不继续跑新实验，诚实 fallback 是把它提交为 negative/redesign proposal：当前 cue-GVF predictions 尚未成为 useful state，下一步是 diagnostic，而不是 performance polishing。

## 独立研究范围

本 proposal 是独立的 representation/partial-observability study。当前范围是 T-maze partial observability 下的 fixed predictive state；limited-budget feature replacement、generated traces 和 feature-wise step-size adaptation 是同一研究计划内的后续阶段，必须等 useful predictive feature gate 更清楚后再推进。当前 claim 只基于 fixed predictive-state gate、trial accuracy 和 cue-decodability evidence。

本 proposal 明确不声称 GVFs 一般失败。它只说明当前 cue-GVF 和 recurrent-GVF constructions 在这个 setting 中没有强到足以被 downstream linear control 使用。这个边界很重要，因为它把负结果变成设计约束，而不是对 predictive knowledge 的泛化否定。

## 证据等级

证据等级：高价值 negative gate，并有 20-seed extended evidence。完成 run 覆盖 maze lengths `8, 12, 20, 30`、5 种 representation modes，每个 condition 20000 online steps。证据足以说明当前 learned GVF features 没有在这个 T-maze 中成为 useful state。

证据还不是 positive plasticity result。当前已经加入 cue-decodability probe，但还没有 oracle-prediction control、GVF output normalization、feature ablations、phase switches、limited-budget feature replacement 或完整定义的 feature-wise step-size adaptation baseline。这些不是小细节，而是把负结果推进成完整研究计划所需的 next gates。

## 论文式贡献与 Claim 边界

本报告的贡献是 predictive-state research 的一个负向但有信息量的 gate。它在 partial observability 下定义 useful-prediction criterion：learned prediction 必须既携带 hidden cue information，又能被 control learner 使用。通过跨 maze length 比较 raw observation、trace memory、GVFs、cue-GVFs 和 oracle memory，报告把“任务不可解”和“representation failure”区分开。

claim 边界是：当前 GVF designs 没有通过这个 gate；这不是对 GVFs 或 predictive knowledge 的一般否定。学术价值在于提出更尖锐的下一步问题：什么 information probe、output normalization 或 feature-selection rule 才能让 learned predictions 与 cheap trace memory 竞争？

## 研究动机

Partial observability 让当前 observation 不足以定义 Markov state。长期 agent 必须从历史中构造 state，但课程约束排除了 deep recurrent networks 和 replay。GVFs 提供了一个 Core-RL 路线：关于未来 signals 的 predictions 可以成为 features。更深的问题不是 predictive features 能否被计算出来，而是它们是否以足够强、足够可用、尺度合适的方式携带 hidden variable，让下游 control learner 能利用它们。因此本报告先把 useful predictive state 当作一个可测量的 representation question，再考虑 replacement 或 plasticity 机制。

这个 proposal 的价值在于拒绝“加 GVF 就有用”的浅结论。一个 GVF 可能预测得很准，但预测的是容易学习、与控制无关的 cumulant；也可能在局部有 cue-aligned signal，却无法被 downstream control update 使用。T-maze cue task 专门把这个问题暴露出来：如果 prediction 不能把早期 cue 信息带到 junction，它就不是 useful state。

## 研究问题

核心问题是：在 observations aliased 且 memory timescale 变长时，什么样的 predictive question design 和 state-construction diagnostics 能帮助 streaming linear agent 维护 useful state？

当前 first-gate 子问题更具体：在没有复杂 feature plasticity 前，固定 learned GVF features 是否已经能胜过 raw observation，并接近 trace/oracle memory？如果这个 gate 都不过，就不应直接宣称 predictive-state plasticity 成功。

## 相关工作与 Alberta Plan 关联

Alberta Plan 强调 GVFs、feature finding 和 agent-state construction。Horde 展示了大量 off-policy predictions 可以并行学习。Useful-prediction 相关工作提醒我们，prediction accuracy 不是最终目标；prediction 必须对 agent 的后续 learning/control 有用。online agent-state construction 的相关工作支持一个分阶段研究路线：先测试 prediction 是否 informative 且 usable，再在 representation 通过 gate 后加入 capacity management 和 feature-wise plasticity。相关本地资料包括 `resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`、`resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`、`resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf`、`resources/alberta_plan_related/tidbd_1804.03334.pdf`、`resources/alberta_plan_related/streaming_deep_rl_finally_works_2410.14606.pdf` 和 `resources/alberta_plan_related/squeezing_more_from_stream_2602.09396.pdf`。

## 环境设计

主环境是 aliased T-maze。每个 trial 开始时 cue 指示左或右，cue 只在起点 observation 中出现；之后 agent 进入走廊，走廊 observation 被 alias，不能区分早期 cue；到 junction 时 agent 必须根据起点 cue 选择动作。正确选择得到正 reward，错误选择得到负 reward，然后新 trial 开始。这个环境专门用于区分 raw observation、cheap trace memory、oracle memory、learned GVF feature 和后续 plasticity 机制。

这个环境的研究用途很明确：它不是为了追求复杂 benchmark 分数，而是迫使 learned state 必须携带 hidden cue information。如果 trace/oracle 可以解决而 GVF 不行，那么失败点就在 predictive feature 的信息、尺度或 control utilization 上，而不是环境本身不可解。

## 方法

当前实现的 representation modes 包括 raw observation、trace memory、recurrent GVF、cue GVF 和 oracle memory。Raw observation 是最低 baseline；trace memory 是便宜但手工设计的 cue retention baseline；oracle memory 直接提供 hidden cue，是上界；recurrent GVF 尝试通过预测 terminal cue/outcome 维持信息；cue GVF 直接预测 cue cumulants，希望更明确地把 cue 信息带入 state。所有 control learners 都是 online linear Sarsa，不使用 replay，不使用 deep network。

GVF 与 control learner 都在线更新。评价不是 GVF TD error 单独低不低，而是 GVF output 是否携带 hidden cue，并且 downstream control 是否能利用它提高 trial accuracy。

## 实验设计

当前 extended first-gate run 使用 maze lengths `8, 12, 20, 30`，modes 为 raw、trace_memory、recurrent_gvf、cue_gvf 和 oracle，seeds 为 `0-19`，每个 condition 运行 `20000` online steps。结果路径是 `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`。

主要指标包括 trial-end accuracy、average reward、GVF TD error、cue-alignment margin、control TD error。解释标准是：只有 learned prediction 明显携带 hidden cue，并把 control accuracy 提升到 raw observation 以上且接近 cheap trace baseline，才可以说它是 useful state。只要 GVF 有非零 cue alignment 但 control 仍 near chance，就只能算 diagnostic signal，不算解决 predictive-state 问题。

## 实验设计依据

T-maze 的作用是清楚地区分 observation 和 state。如果 agent 没有保留初始 cue，junction action 就接近 chance。Trace 和 oracle memory 不是 strawman，而是必要 control：它们说明任务在课程约束下可解，也定义 learned predictive feature 距离 cheap memory baseline 有多远。

当前 extended run 是 gate，而不是完整 program。Maze length 测试 cue retention 是否能跨更长 delay。Cue-alignment margin 测试 learned feature 是否含有 hidden-cue signal。Trial accuracy 测试更严格的问题：control 是否能使用该 signal。GVF TD error 只是辅助指标，因为 accurate prediction 仍可能对 control 无用。

## 结果

![Tail trial accuracy by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_trial_accuracy_by_maze_length.png)

![GVF-based state constructions 的 tail cue-alignment margin。](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_cue_alignment_margin_by_maze_length.png)

![GVF-based state constructions 的 tail GVF absolute TD error。](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_gvf_abs_td_error_by_maze_length.png)

![不同 state construction 和 maze length 下的 tail cue-decoding accuracy。](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_cue_decodability_by_length.png)

extended 结果非常清楚。Oracle memory 在所有长度上保持高准确率，约 `0.931-0.950`。Trace memory 在短中长度上接近 oracle，在 length `30` 时下降到约 `0.827 +/- 0.013`，但仍明显高于 chance。Raw observation 接近 chance。Recurrent GVF 也接近 chance。Cue-GVF 在长度 `8,12,20,30` 上的 trial accuracy 分别约 `0.504, 0.508, 0.505, 0.494`，没有形成有效 control state。

新增 cue-decodability analysis 进一步拆开 information content 与 control usefulness。它检查 late-corridor features 是否能在 junction 前预测 hidden cue。Cue-GVF 的 tail cue-decoding accuracy 在 maze lengths `8,12,20,30` 上约为 `0.589, 0.589, 0.609, 0.622`，高于 chance 但远低于 trace/oracle 的 `1.0`。Raw observation 为 chance，recurrent GVF 也接近 chance。这说明 cue-GVF 不是完全没有信息；它携带弱 cue information，但 downstream control learner 没能把它稳定转化为正确 junction decision。

cue-GVF 的 cue-alignment margin 在较短长度上有一些正信号，但随 maze length 增长变弱，而且这点信号没有转化为 control accuracy。这正是本课题的核心 insight：prediction signal 不等于 useful state；一个 feature 只有在 downstream control update 能稳定使用它时才有意义。

## 分析

这个结果应被视为 negative gate，而不是失败后放弃。cue-decodability probe 缩小了失败原因：当前 cue-GVF 确实携带弱 hidden-cue information，但该信息没有成为有效 control state。可能原因包括：GVF cumulant/horizon 设计不对；GVF output scale 不适合 Sarsa control；control step size 没有针对 predictive feature 调整；cue signal 虽然存在但不够 linearly separable；或者 cheap trace memory 本身就是这个任务的强 baseline。

因此，下一个严谨版本应先加入 oracle-prediction control、GVF output normalization、feature ablation，再考虑有限 feature budget 下的 candidate-feature replacement 和 feature-wise step-size adaptation。

## 局限

当前实验是 controlled partial-observability test，不是大型真实世界任务。它只证明当前 GVF 设计在这个尖锐 setting 下没有成为 useful state，不能证明所有 GVF 都无用。trace memory 是 hand-coded strong baseline，可能过强，但它恰好提供了重要标准：如果 learned prediction 连 cheap trace 都比不过，就不能声称 predictive state construction 成功。当前还没有 phase-change experiment，也没有完整接入 limited-budget feature replacement 和 feature-wise step-size adaptation。

## 审稿式批评与修订

严格审稿人可能会问：“GVF 是负结果，为什么还继续？”回答是：负结果正是设计信号，说明当前 GVF question 没有把 cue 信息变成可用控制 state。另一个批评是课题太大。对此，proposal 应分层推进：先验证 fixed useful GVF questions，再做 limited-budget selection，最后做 step-size plasticity；不能在第一层没通过时直接宣传 combined plasticity 成功。当前修订已经把报告明确定位为 negative/redesign gate，并通过 20-seed extended run 加强证据。

逐 proposal 审查矩阵：

| 审查角度 | 批评 | 已处理 | 剩余风险 |
|---|---|---|---|
| Alberta Plan | GVFs 只有在 predictions 成为 useful state 时才重要。 | 报告评价 control accuracy，而不是只看 prediction error。 | 当前 GVF questions 仍未通过 useful-state gate。 |
| Partial observability | 任务可能在无 deep recurrence 下不可解。 | Trace 和 oracle baselines 能解决任务。 | learned prediction 仍需更强 information probe。 |
| Representation | cue alignment 可能存在但 control 用不了。 | 同时报告 cue-alignment margin、cue-decodability 和 trial accuracy。 | 仍需要 GVF output normalization 和 oracle-prediction control。 |
| Plasticity | generated features 和 feature-wise step-size adaptation 尚未在 full control loop 中测试。 | 报告明确它们是内部 next-stage mechanisms，而不是当前 evidence。 | positive plasticity claim 需要新实验。 |
| 严格老师 | 不要把当前负结果泛化成 GVF 总体结论。 | 结论限定在当前 cue-GVF/recurrent-GVF designs。 | 更好的 GVF questions 可能改变结论。 |

## 结论

Predictive State Plasticity 是一个有野心但高风险的课题。它的价值不是证明“加 GVF 有用”，而是严肃检验 predictions 是否真的能成为 partial observability 下的 useful state。extended first-gate 与 cue-decodability 结果显示，当前 cue-GVF 含有弱 cue information，但还不是有用 control state。这个负结果很有研究价值，因为它明确提出下一步设计约束：predictive feature 必须既包含 hidden variable information，又能被 downstream control update 使用。

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

重新生成 cue-decodability summary 和 figure：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/analyze_predictive_state_decodability.py \
  --result-dir experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended
```
