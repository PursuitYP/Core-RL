# Useful Predictive Knowledge Under Partial Observability 中文报告

状态：独立的 integrated Core-RL proposal，已经完成 Gate-1/Gate-2 main evidence，并完成 Gate-3 feature-budget selection experiment。本研究问 learned prediction 什么时候能成为 online control 可用的 state，而不是问“加一个 prediction head 会不会让分数更高”。

## 摘要

Alberta Plan 把 predictive knowledge 放在 agent state 的核心位置附近，但“learned prediction”至少包含三个不同要求：prediction 必须包含真正重要的信息，control learner 必须能在决策时使用这部分信息，并且 resource-limited agent 必须优先保留这个 prediction，而不是保留容易预测但无关的 prediction。本 proposal 在一个 partially observable T-maze 中研究这些要求：cue 只在开头出现，agent 必须把 cue 保留到后面的 junction decision。实验比较 raw observation、hand-coded trace memory、oracle memory、不同 cumulant 和 horizon 的 GVFs，以及一个 two-feature budget gate。核心 claim 不是 GVF 一般好或一般不好，而是 useful predictive knowledge 在被提升为 agent state 前，必须通过 explicit information gate、control gate 和 feature-budget gate。

## Standalone Study Summary / 独立研究概要

本研究问 online learned predictions 是否能在 partial observability 和 limited computation 下成为 useful state。RL 问题是 aliased T-maze：junction 处的 observation 不显示哪个 action 正确，因此 successful control 需要把 early cue 带过 corridor。第一组实现比较包括 raw observations、trace memory、oracle cue memory，以及由 cue、terminal-outcome 或 junction cumulants 构造的 GVF features，horizon 为 `gamma = 0.8, 0.95, 0.99`。第二组实现把 controller 的额外 state budget 限制为两个 features，比较 fixed cue-GVF、fixed irrelevant GVFs、low-TD-error selector 和 oracle cue-decoding selector。实验改变 maze length，并测量 trial accuracy、decision-time cue decodability、selected-feature identity、selected-feature decoding、GVF TD error 和 control TD error。正向结果要求 learned prediction 同时 cue-informative、能在有限 budget 中被保留，并且 control-useful；低 prediction error 本身不足以证明 usefulness。

## Proposal Template Answers / 提案模板回答

Focused RL question：在 partial observability 下，learned predictive knowledge 什么时候成为 online control agent 可用的 state？

Setting and testbed：主 testbed 是一系列 T-maze trials，包含 transient binary cue、aliased corridor 和 delayed junction decision。这个 setting 足够小，可以完整 instrumentation；但不是空洞 toy：raw observation 不充分，trace 和 oracle memory 证明不使用 deep networks 也能解任务，GVF features 必须证明自己保留了 control-relevant hidden cue。

Implemented comparison：Gate-1/Gate-2 实验比较 raw observation、trace memory、oracle cue memory、cue-GVFs、terminal-outcome GVFs 和 junction/bias GVFs。GVF horizons sweep `0.8`、`0.95`、`0.99`。Gate-3 实验把额外 state budget 固定为两个 features，比较 raw budget zero、trace memory、oracle memory、fixed cue-GVF、fixed terminal-GVF、fixed junction-GVF、low-TD-error selector 和 oracle cue-decoding selector。所有 agents 都使用 online linear TD/Sarsa，不使用 replay buffer，不使用 deep network，也不使用 offline training loop。

Observation or figure that answers the question：主要证据是按 maze length 和 predictive question 展示的 decision-time cue decoding 与 trial accuracy，以及 feature-budget 条件下的 selected cue decoding、selected cue-GVF survival 和 trial accuracy。一个 prediction 如果准确但 cue-undecodable，就没通过 information gate。一个 prediction 如果 cue-decodable 但不能提升 action accuracy，就没通过 control-utilization gate。一个 prediction 如果能在 budget 中被选中但仍不能提升 trial accuracy，就没有通过 prediction-to-policy coupling gate。

Compute need and fallback：实验是 CPU-scale。Fallback 也有科学意义：如果 GVFs 降低 TD error 但不提升 decodability 或 control，结论就是在这个 setting 中 prediction accuracy 不足以定义 useful agent state。

## Independent Research Scope / 独立研究范围

本研究的问题、方法和结论都在 T-maze predictive-state study 内部定义。它使用一个统一环境族和一个 staged criterion：predictive knowledge 只有在携带 hidden variable、能在有限 state budget 中保留，并改善 downstream control 时才有用。当前报告已经包含第一轮 feature-budget selection gate。Plasticity under changing cue relevance 仍然在已完成证据之外，应作为下一阶段，而不是已解决结果。

本研究范围有意窄于完整 Oak-style utility agent。本文研究 learned knowledge 的第一个必要 gate：information 和 usability。它不声称解决 feature discovery、option discovery、off-policy GVF stability 或长期 component management。

## Evidence Level / 证据等级

证据等级：已完成 10-seed Gate-1/Gate-2 main study，并完成 8-seed Gate-3 feature-budget study。Gate-1/Gate-2 run `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main` 使用 10 seeds、12000 online steps、maze lengths `8`、`12`、`20`、三个 baseline state constructions、三类 GVF questions 和三个 GVF horizons。Gate-3 run `experiments/alberta_core_rl/results/useful_predictive_knowledge_budget/20260709T132025Z_main` 使用 8 seeds、8000 online steps、相同 maze lengths，以及八种 budgeted state-construction 或 selection conditions。合起来的证据支持一个受限机制 claim：cue-GVFs 可以携带 above-chance hidden-cue information，并且可以被 cue-decoding criterion 选中，但在这个实验中，learned GVF condition 仍不能把这部分信息转化为可靠 control。

## Research Motivation / 研究动机

长期 agent 不能把所有 predictions 都当作 useful knowledge。有些 prediction 容易学习，因为 cumulant 频繁、局部、低方差；另一些 prediction 有用，因为它们在决策时揭示 hidden variable。这两种性质并不相同。Alberta Plan 鼓励 agent 从 ordinary experience 中学习许多 value functions，但它也提出一个 utility question：哪些 learned signals 值得成为 agent state 的一部分？

Partial observability 让这个问题具体化。在 T-maze 中，junction 处当前 observation 是 aliased。Agent 必须从 initial cue 把信息带到 later action。Hand-coded trace 可以廉价地做到这一点；oracle memory 可以完美做到这一点。因此 learned predictive feature 必须同时接受两个标准：它是否保留 cue，以及 linear control 是否能使用它。

## Research Questions / 研究问题

RQ1：哪些 predictive questions 能在 decision time 保留 hidden cue：immediate cue cumulants、delayed terminal-outcome cumulants，还是 generic junction/bias cumulants？

RQ2：当 maze length 增加时，prediction horizon 如何影响 cue retention 和 prediction usability 的 tradeoff？

RQ3：cue decodability 是否会转化为 control accuracy，还是 learned prediction 可能包含弱 hidden-state information，但 control learner 仍无法使用？

RQ4：在 two-feature state budget 下，selection criteria 会保留 cue-relevant predictions，还是偏向 easy-but-irrelevant predictions？

RQ5：下一阶段应该针对哪种 failure mode：poor predictive information、poor output scaling、poor control utilization，还是在 prediction-to-policy coupling 被解决后再进入 plasticity？

## Related Work / 相关工作

Alberta Plan 提供 ordinary experience、value functions、GVFs 和 agent-state construction 的主框架。Horde-style GVF work 说明为什么可以并行学习许多 predictions，但本研究问的是另一个问题：哪些 predictions 应被信任为 state？Finding useful predictions 相关工作直接支持 cue-decoding 和 downstream-control gates，因为 prediction accuracy 本身可能奖励容易的问题，而不是有用的问题。Online agent-state construction 工作支持 trace/oracle controls：一个候选 state feature 在声称 prediction 解决 partial observability 前，应先与廉价 memory baselines 比较。Streaming RL 工作支持 no-replay constraint，以及使用 online linear learners 而不是 offline representation learning 的设计选择。

有用本地资料包括 `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`、`resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`、`resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`、`resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf` 和 `resources/alberta_plan_related/squeezing_more_from_stream_2602.09396.pdf`。

## Research Method / 研究方法

环境在 position `0` 发出 binary cue，之后在 aliased corridor 中隐藏 cue。在 terminal junction，action `0` 对一个 cue 正确，action `1` 对另一个 cue 正确。Control learner 是 epsilon-greedy linear Sarsa。Prediction learners 是 normalized linear TD learners，它们的输出被拼接到 raw observation 上作为 candidate state features。

Baseline state constructions 包括 raw observation、trace memory 和 oracle memory。Raw observation 是 lower bound，因为 cue 消失后它看不到 cue。Trace memory 是廉价的非 deep history baseline。Oracle memory 是 upper diagnostic，证明 hidden cue 暴露时 linear control 可以解任务。

GVF state constructions 使用两个 learned prediction outputs。Cue-GVFs 预测 left/right cue observations；terminal-outcome GVFs 预测 left/right terminal outcomes；junction/bias GVFs 预测 generic junction signal 和 bias。Junction/bias condition 被有意作为 contrast：它可能容易预测或稳定预测，但不应携带 hidden cue。

Feature-budget 实验使用同一个 T-maze dynamics，但把 controller 限制为 raw observation 加最多两个额外 features。Fixed cue/terminal/junction GVF conditions 检验手工选择某类 predictive feature 是否足够。Low-TD-error selector 选择 online TD-error exponential moving average 最小的 candidate GVF pair，用来测试 learnability 是否会选择 useful knowledge。Oracle cue-decoding selector 选择 online cue-decoding exponential moving average 最好的 candidate pair，用来测试直接 information criterion 是否能选到正确 prediction，即使 controller 之后仍可能无法利用它。

## Experimental Design / 实验设计

Main implemented run：

| Design element | Value |
|---|---|
| Config | `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json` |
| Seeds | `0-9` |
| Steps | `12000` online steps per condition |
| Maze lengths | `8`, `12`, `20` |
| State constructions | raw, trace memory, oracle, cue-GVF, terminal-GVF, junction-GVF |
| GVF horizons | `0.8`, `0.95`, `0.99` |
| Learners | normalized linear TD for predictions; normalized linear Sarsa for control |
| Constraints | no replay buffer, no deep network, no offline fitting |

Feature-budget implemented run：

| Design element | Value |
|---|---|
| Config | `experiments/alberta_core_rl/configs/useful_predictive_knowledge_budget/config_main.json` |
| Result path | `experiments/alberta_core_rl/results/useful_predictive_knowledge_budget/20260709T132025Z_main` |
| Seeds | `0-7` |
| Steps | 每个 condition `8000` online steps |
| Maze lengths | `8`, `12`, `20` |
| Conditions | raw budget zero、trace memory、oracle memory、fixed cue-GVF、fixed terminal-GVF、fixed junction-GVF、low-TD-error selector、oracle cue-decoding selector |
| Learners | candidate predictions 使用 normalized linear TD；control 使用 normalized linear Sarsa |
| Logged evidence | 153792 行 metrics、24 个 condition groups，并包含标准 `summary.json`、`condition_summary.json`、`metrics.csv`、`config_used.json` 和 `manifest.json` artifacts |

Primary metrics：

| Metric | Role in the argument |
|---|---|
| `trial_accuracy` | delayed junction 的 downstream control success。 |
| `decision_cue_decoding_correct` | candidate state feature 在 decision point 是否仍能识别 hidden cue。 |
| `cue_alignment_margin` | trace/oracle/GVF outputs 中 cue information 的 signed strength。 |
| `gvf_abs_td_error` | Prediction-learning diagnostic；secondary，因为低 error 本身不证明 usefulness。 |
| `control_td_error` | Control-learning diagnostic，用于发现 instability 或 poor utilization。 |
| `selected_is_cue` | budgeted selector 是否保留 cue-GVF pair。 |
| `decision_selected_cue_decoding_correct` | selected budgeted feature 在 decision point 是否识别 hidden cue。 |
| `selector_switch_count` | online feature selection 的稳定性诊断。 |

## Experiment Design Rationale / 实验设计依据

实验采用 gate-structured 设计。第一道 gate 是 information：useful predictive state 必须能对 hidden cue 解码。第二道 gate 是 control：可解码信息必须改善 junction decisions。这避免了把低 TD error 当作 useful knowledge 证据的常见错误。一个 GVF 可能很好地预测频繁 junction event，却与 cue 无关。另一个 GVF 可能弱编码 cue，但如果输出尺度或噪声让 Sarsa 无法利用它，仍然不能作为 useful state。

Maze length 是 memory-pressure 变量。短 corridor 可能掩盖弱 prediction failure，因为粗糙 trace 仍能保留足够 cue information。更长 corridor 迫使 predictive feature 在更长 delay 上保留信息。Horizon sweep 用来检验 GVF timescale 是否需要匹配该 delay。

## Expected Results And Failure Modes / 预期结果与失败模式

预期 upper bound 是 oracle memory，其次是 trace memory。Raw observation 除了 cue 仍可见的位置外应接近 chance。Cue-GVFs 和 terminal-GVFs 可能保留部分 cue information，而 junction/bias GVFs 应作为 negative control。强正向结果需要 learned GVF condition 在不同 maze lengths 上同时表现出 above-chance decision cue decoding 和 improved trial accuracy。混合结果是 cue decoding 高于 chance 但 trial accuracy 接近 chance；这会指向 control-utilization 或 output-scale failure。负结果是 decodability 和 control 都接近 chance，说明需要重设计 cumulants 或 state-construction mechanisms。

## Results / 结果

完成的 main result path 是：

`experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main`

结果是一个清晰的 mixed negative。任务本身可解：trace memory 在 maze lengths `8`、`12`、`20` 上的 trial accuracy 分别为 `0.945 +/- 0.012`、`0.928 +/- 0.015`、`0.892 +/- 0.018`；oracle memory 分别为 `0.943 +/- 0.008`、`0.941 +/- 0.013`、`0.943 +/- 0.016`。Raw observation 保持在 chance 附近，accuracy 分别为 `0.506 +/- 0.026`、`0.511 +/- 0.012`、`0.486 +/- 0.031`。

Learned GVF conditions 没有改善 control。所有 maze lengths 中，best learned-GVF trial accuracy 只有 length `8` 的 `0.518 +/- 0.018`、length `12` 的 `0.512 +/- 0.010` 和 length `20` 的 `0.507 +/- 0.017`。这些结果都接近 chance，并且远低于 trace/oracle memory。因此当前实验中没有 GVF condition 通过 control-utilization gate。

Information gate 给出更细的结论。`gamma=0.8` 的 cue-GVFs 是 learned predictions 中最稳定的 cue decoder：decision-time cue decoding 在 lengths `8`、`12`、`20` 上分别为 `0.626 +/- 0.009`、`0.611 +/- 0.015`、`0.638 +/- 0.015`。但它们的 trial accuracies 仍只有 `0.508 +/- 0.022`、`0.508 +/- 0.014`、`0.495 +/- 0.028`。这是核心 insight：learned cue prediction 不是空的，但 downstream control learner 没有利用这个弱 predictive signal。

Terminal-outcome 和 junction/bias GVFs 是有用的 negative controls。Terminal GVFs 通常在 cue decoding 上接近 chance；length-8 的 `terminal, gamma=0.99` 条件出现严重 instability signal，seed-tail cue margin 为 `2515.272 +/- 3484.339`，GVF absolute TD error 为 `37.199 +/- 47.238`。Junction/bias GVFs 有时产生 learned GVFs 中最高的表面 trial accuracy，但 decision-time cue decoding 仍接近 chance，因此这些小的 accuracy differences 不应被解释为 useful state。

| Maze length | Raw accuracy | Trace accuracy | Oracle accuracy | Best learned cue decoding | Accuracy of best decoder | Interpretation |
|---:|---:|---:|---:|---:|---:|---|
| `8` | `0.506 +/- 0.026` | `0.945 +/- 0.012` | `0.943 +/- 0.008` | cue-GVF gamma `0.8`: `0.626 +/- 0.009` | `0.508 +/- 0.022` | Information above chance, control at chance. |
| `12` | `0.511 +/- 0.012` | `0.928 +/- 0.015` | `0.941 +/- 0.013` | cue-GVF gamma `0.8`: `0.611 +/- 0.015` | `0.508 +/- 0.014` | Same failure mode under longer delay. |
| `20` | `0.486 +/- 0.031` | `0.892 +/- 0.018` | `0.943 +/- 0.016` | cue-GVF gamma `0.8`: `0.638 +/- 0.015` | `0.495 +/- 0.028` | Cue signal persists, but control still fails. |

![Tail trial accuracy by state construction, GVF question, horizon, and maze length.](figures/report_upk_trial_accuracy_by_length.png)

![Decision-time cue decoding by state construction, GVF question, horizon, and maze length.](figures/report_upk_decision_decoding_by_length.png)

第三张生成的 diagnostic figure `figures/report_upk_cue_margin_by_length.png` 不作为主报告图，因为 unstable terminal-GVF `gamma=0.99` 条件产生了非常大的 outlier，导致 useful range 被压缩。该 outlier 已在上文用数值报告，作为 instability warning。

完成的 feature-budget result path 是：

`experiments/alberta_core_rl/results/useful_predictive_knowledge_budget/20260709T132025Z_main`

Feature-budget gate 加强了负向结论，而不是推翻它。Trace 和 oracle memory 在只有两个额外 features 的预算下仍然很强：maze lengths `8`、`12`、`20` 上，trace memory trial accuracy 分别为 `0.947 +/- 0.010`、`0.927 +/- 0.007`、`0.906 +/- 0.039`，oracle memory 分别为 `0.954 +/- 0.018`、`0.952 +/- 0.011`、`0.924 +/- 0.012`。Raw observation 仍接近 chance。这说明 two-feature budget 本身不是障碍；真正障碍是 learned predictive feature 是否对 policy 有用。

Cue-GVF 和 selectors 比 irrelevant GVFs 更能保留 cue information，但仍不能改善 control。Fixed cue-GVF 的 trial accuracy 是 `0.511 +/- 0.012`、`0.504 +/- 0.022`、`0.496 +/- 0.053`，而 decision-time selected-feature cue decoding 是 `0.596 +/- 0.040`、`0.625 +/- 0.107`、`0.714 +/- 0.130`。Low-TD-error selector 在 tail 几乎总是选到 cue-GVF pair（三个 length 的 selected-cue fraction 为 `1.000`、`1.000`、`0.988`），但 trial accuracy 只有 `0.504 +/- 0.027`、`0.501 +/- 0.029`、`0.514 +/- 0.027`。Oracle cue-decoding selector 也几乎总是选到 cue-GVF features（`0.974`、`0.953`、`0.986`），并且 learned features 中 cue decoding 最好，但 trial accuracy 仍接近 chance：`0.519 +/- 0.028`、`0.521 +/- 0.026`、`0.508 +/- 0.027`。

| Maze length | Trace accuracy | Oracle accuracy | Fixed cue-GVF accuracy | Low-TD selector accuracy | Decode selector accuracy | Main interpretation |
|---:|---:|---:|---:|---:|---:|---|
| `8` | `0.947 +/- 0.010` | `0.954 +/- 0.018` | `0.511 +/- 0.012` | `0.504 +/- 0.027` | `0.519 +/- 0.028` | Budgeted memory 能解决任务，但 budgeted cue-GVF 不能。 |
| `12` | `0.927 +/- 0.007` | `0.952 +/- 0.011` | `0.504 +/- 0.022` | `0.501 +/- 0.029` | `0.521 +/- 0.026` | Selection 能保留 cue predictions，但不能让它们成为 policy-usable state。 |
| `20` | `0.906 +/- 0.039` | `0.924 +/- 0.012` | `0.496 +/- 0.053` | `0.514 +/- 0.027` | `0.508 +/- 0.027` | 更长 memory pressure 增加 decodability 方差，但没有带来 control success。 |

![Feature-budget trial accuracy by selected state construction.](budget_figures/report_upk_budget_trial_accuracy.png)

![Feature-budget selected-feature cue decoding by selected state construction.](budget_figures/report_upk_budget_selected_decoding.png)

![Fraction of time that each online selector keeps the cue-GVF pair.](budget_figures/report_upk_budget_selected_cue.png)

关键修订是：feature selection alone 不再只是未测试的 future-work explanation。在这个实验中，即使用直接 cue-decoding selector 通常也能选到 cue-GVF pair，controller 仍然接近 chance。剩余 failure mode 因此更具体：GVF outputs 可能太弱、scale 不合适或噪声太大，Sarsa 需要 explicit coupling/normalization mechanism，或者 prediction 本身需要比 passive cue cumulant 更 action-relevant。

## Reviewer Critique And Revisions / 审稿批评与修订

| Reviewer angle | Critique | Current response | Remaining risk |
|---|---|---|---|
| Alberta Plan | Predictive knowledge 太宽，除非 utility 被 operationalized。 | 报告把 utility 定义为 information plus downstream control use。 | 后续 component-utility gates 仍不在当前实验内。 |
| Core RL | T-maze 可能太小。 | 它小但结构上有意义：raw observation 失败，trace/oracle baselines 解决 hidden-state problem。 | 第二个 delayed-cue stream 会增强 generality。 |
| GVF reviewer | Prediction error 不是正确目标。 | GVF TD error 是 secondary；cue decodability 和 trial accuracy 是 primary。 | 可能仍需要更好的 GVF question families。 |
| Statistics | 条件多，可能遮住主 claim。 | Figures 按 maze length 和 gate metric 分组，compact tables 汇总 GVF-horizon gate 和 feature-budget gate。 | 如果作为最终提交，应对最强 budget conditions 做 20-seed replication 或 power analysis。 |
| Strict instructor | 不要把它说成 agent-state construction 的解法。 | 报告写成 staged gates，并且 Gate 3 是负向证据，不做过度 claim。 | Plasticity 和 oracle-prediction scaling 仍是 future work。 |

## Threats To Validity / 有效性威胁

T-maze 能隔离 partial observability，但不能覆盖 agent-state construction 的所有形式。当前 GVF designs 仍是 hand-selected；负向 control result 反映的是已测试 question family，不是 predictive knowledge 的普遍限制。Cue-decoding metric 是 information proxy，不能替代 downstream control。反过来，如果 control improvement 没有 decodability，也需要谨慎解释，因为 agent 可能利用的是 hidden cue 的 correlate，而不是 cue 本身。Gate-3 feature-budget run 使用 8 seeds 和 8000 steps，足以暴露主要 failure mode；如果作为最终提交，应扩展到 20 seeds。更严格的 follow-up 应增加 GVF values before Sarsa 的 output normalization，加入一个 oracle-prediction control，让 true cue probability 以和 GVF output 相同的 scale 输入 controller，并且只有在 prediction-to-policy coupling mechanism 明确后再进入 phase-switch/plasticity stage。

## Conclusion / 结论

本 proposal 把 Alberta Plan 中 broad predictive knowledge idea 转化为一个具体 Core-RL test：prediction 只有在保留 hidden variable、能在有限 state budget 中保留，并改善 downstream control 时，才应成为 state。完成的 runs 给出更尖锐的有价值负结果。Cue-GVFs 通过了弱 information gate；direct decoding selector 可以在 two-feature budget 下保留它们；trace 和 oracle memory 证明任务可解；但 learned predictive features 仍不能成为可靠 control state。下一步有意义的研究不再是泛泛 feature selection，而是测试 GVF output scaling、oracle-prediction controls 和 prediction-to-policy coupling mechanisms，然后只有在 budgeted predictive signal 真能改善 control 后再加入 plasticity。

## Reproduction / 复现

运行 main experiment：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json
```

生成报告图：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind useful-predictive-knowledge \
  --result-dir experiments/alberta_core_rl/results/useful_predictive_knowledge/<timestamp>_main \
  --figure-dir final/reports/integrated/useful_predictive_knowledge/figures
```

运行 feature-budget gate：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/useful_predictive_knowledge_budget/config_main.json
```

生成 feature-budget figures：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_report_figures.py \
  --kind useful-predictive-knowledge-budget \
  --result-dir experiments/alberta_core_rl/results/useful_predictive_knowledge_budget/20260709T132025Z_main \
  --figure-dir final/reports/integrated/useful_predictive_knowledge/budget_figures
```
