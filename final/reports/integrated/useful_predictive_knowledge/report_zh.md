# Useful Predictive Knowledge Under Partial Observability 中文报告

状态：独立的 integrated Core-RL proposal，新的 Gate-1/Gate-2 experiment 正在运行。本研究问 learned prediction 什么时候能成为 online control 可用的 state，而不是问“加一个 prediction head 会不会让分数更高”。

## 摘要

Alberta Plan 把 predictive knowledge 放在 agent state 的核心位置附近，但“learned prediction”至少包含两个不同要求：prediction 必须包含真正重要的信息，并且 control learner 必须能在决策时使用这部分信息。本 proposal 在一个 partially observable T-maze 中研究这两个要求：cue 只在开头出现，agent 必须把 cue 保留到后面的 junction decision。实验比较 raw observation、hand-coded trace memory、oracle memory，以及不同 cumulant 和 horizon 的 GVFs。核心 claim 不是 GVF 一般好或一般不好，而是 useful predictive knowledge 在被提升为 agent state 前，必须通过 explicit information gate 和 control gate。

## Standalone Study Summary / 独立研究概要

本研究问 online learned predictions 是否能在 partial observability 和 limited computation 下成为 useful state。RL 问题是 aliased T-maze：junction 处的 observation 不显示哪个 action 正确，因此 successful control 需要把 early cue 带过 corridor。实现比较包括 raw observations、trace memory、oracle cue memory，以及由 cue、terminal-outcome 或 junction cumulants 构造的 GVF features，horizon 为 `gamma = 0.8, 0.95, 0.99`。实验改变 maze length，并测量 trial accuracy、decision-time cue decodability、signed cue margin、GVF TD error 和 control TD error。正向结果要求 learned prediction 同时 cue-informative 和 control-useful；低 prediction error 本身不足以证明 usefulness。

## Proposal Template Answers / 提案模板回答

Focused RL question：在 partial observability 下，learned predictive knowledge 什么时候成为 online control agent 可用的 state？

Setting and testbed：主 testbed 是一系列 T-maze trials，包含 transient binary cue、aliased corridor 和 delayed junction decision。这个 setting 足够小，可以完整 instrumentation；但不是空洞 toy：raw observation 不充分，trace 和 oracle memory 证明不使用 deep networks 也能解任务，GVF features 必须证明自己保留了 control-relevant hidden cue。

Implemented comparison：当前实验比较 raw observation、trace memory、oracle cue memory、cue-GVFs、terminal-outcome GVFs 和 junction/bias GVFs。GVF horizons sweep `0.8`、`0.95`、`0.99`。所有 agents 都使用 online linear TD/Sarsa，不使用 replay buffer，不使用 deep network，也不使用 offline training loop。

Observation or figure that answers the question：主要证据是按 maze length 和 predictive question 展示的 decision-time cue decoding 与 trial accuracy。一个 prediction 如果准确但 cue-undecodable，就没通过 information gate。一个 prediction 如果 cue-decodable 但不能提升 action accuracy，就没通过 control-utilization gate。

Compute need and fallback：实验是 CPU-scale。Fallback 也有科学意义：如果 GVFs 降低 TD error 但不提升 decodability 或 control，结论就是在这个 setting 中 prediction accuracy 不足以定义 useful agent state。

## Independent Research Scope / 独立研究范围

本 proposal 独立于其他报告。它不依赖其他 proposal 的结果来定义自己的问题、方法或结论。它使用一个统一环境族和一个 staged criterion：predictive knowledge 只有在携带 hidden variable 并改善 downstream control 时才有用。后续 feature-selection 和 plasticity mechanisms 是自然扩展，但不是解释当前 Gate-1/Gate-2 实验所必需的条件。

本研究范围有意窄于完整 Oak-style utility agent。本文研究 learned knowledge 的第一个必要 gate：information 和 usability。它不声称解决 feature discovery、option discovery、off-policy GVF stability 或长期 component management。

## Evidence Level / 证据等级

证据等级将由已运行的 main run `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json` 决定。该 run 使用 10 seeds、12000 online steps、maze lengths `8`、`12`、`20`、三个 baseline state constructions、三类 GVF questions 和三个 GVF horizons。Smoke run 已经验证 runner 和 plotting path。在 main artifacts 写出之前，本报告应被读作已实现但 main evidence 待填充的 study，而不是 completed result。

## Research Motivation / 研究动机

长期 agent 不能把所有 predictions 都当作 useful knowledge。有些 prediction 容易学习，因为 cumulant 频繁、局部、低方差；另一些 prediction 有用，因为它们在决策时揭示 hidden variable。这两种性质并不相同。Alberta Plan 鼓励 agent 从 ordinary experience 中学习许多 value functions，但它也提出一个 utility question：哪些 learned signals 值得成为 agent state 的一部分？

Partial observability 让这个问题具体化。在 T-maze 中，junction 处当前 observation 是 aliased。Agent 必须从 initial cue 把信息带到 later action。Hand-coded trace 可以廉价地做到这一点；oracle memory 可以完美做到这一点。因此 learned predictive feature 必须同时接受两个标准：它是否保留 cue，以及 linear control 是否能使用它。

## Research Questions / 研究问题

RQ1：哪些 predictive questions 能在 decision time 保留 hidden cue：immediate cue cumulants、delayed terminal-outcome cumulants，还是 generic junction/bias cumulants？

RQ2：当 maze length 增加时，prediction horizon 如何影响 cue retention 和 prediction usability 的 tradeoff？

RQ3：cue decodability 是否会转化为 control accuracy，还是 learned prediction 可能包含弱 hidden-state information，但 control learner 仍无法使用？

RQ4：下一阶段应该针对哪种 failure mode：poor predictive information、poor output scaling、poor control utilization，还是需要 feature-selection/plasticity？

## Related Work / 相关工作

Alberta Plan 提供 ordinary experience、value functions、GVFs 和 agent-state construction 的主框架。Horde-style GVF work 说明为什么可以并行学习许多 predictions，但本研究问的是另一个问题：哪些 predictions 应被信任为 state？Finding useful predictions 相关工作直接支持 cue-decoding 和 downstream-control gates，因为 prediction accuracy 本身可能奖励容易的问题，而不是有用的问题。Online agent-state construction 工作支持 trace/oracle controls：一个候选 state feature 在声称 prediction 解决 partial observability 前，应先与廉价 memory baselines 比较。Streaming RL 工作支持 no-replay constraint，以及使用 online linear learners 而不是 offline representation learning 的设计选择。

有用本地资料包括 `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`、`resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`、`resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`、`resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf` 和 `resources/alberta_plan_related/squeezing_more_from_stream_2602.09396.pdf`。

## Research Method / 研究方法

环境在 position `0` 发出 binary cue，之后在 aliased corridor 中隐藏 cue。在 terminal junction，action `0` 对一个 cue 正确，action `1` 对另一个 cue 正确。Control learner 是 epsilon-greedy linear Sarsa。Prediction learners 是 normalized linear TD learners，它们的输出被拼接到 raw observation 上作为 candidate state features。

Baseline state constructions 包括 raw observation、trace memory 和 oracle memory。Raw observation 是 lower bound，因为 cue 消失后它看不到 cue。Trace memory 是廉价的非 deep history baseline。Oracle memory 是 upper diagnostic，证明 hidden cue 暴露时 linear control 可以解任务。

GVF state constructions 使用两个 learned prediction outputs。Cue-GVFs 预测 left/right cue observations；terminal-outcome GVFs 预测 left/right terminal outcomes；junction/bias GVFs 预测 generic junction signal 和 bias。Junction/bias condition 被有意作为 contrast：它可能容易预测或稳定预测，但不应携带 hidden cue。

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

Primary metrics：

| Metric | Role in the argument |
|---|---|
| `trial_accuracy` | delayed junction 的 downstream control success。 |
| `decision_cue_decoding_correct` | candidate state feature 在 decision point 是否仍能识别 hidden cue。 |
| `cue_alignment_margin` | trace/oracle/GVF outputs 中 cue information 的 signed strength。 |
| `gvf_abs_td_error` | Prediction-learning diagnostic；secondary，因为低 error 本身不证明 usefulness。 |
| `control_td_error` | Control-learning diagnostic，用于发现 instability 或 poor utilization。 |

## Experiment Design Rationale / 实验设计依据

实验采用 gate-structured 设计。第一道 gate 是 information：useful predictive state 必须能对 hidden cue 解码。第二道 gate 是 control：可解码信息必须改善 junction decisions。这避免了把低 TD error 当作 useful knowledge 证据的常见错误。一个 GVF 可能很好地预测频繁 junction event，却与 cue 无关。另一个 GVF 可能弱编码 cue，但如果输出尺度或噪声让 Sarsa 无法利用它，仍然不能作为 useful state。

Maze length 是 memory-pressure 变量。短 corridor 可能掩盖弱 prediction failure，因为粗糙 trace 仍能保留足够 cue information。更长 corridor 迫使 predictive feature 在更长 delay 上保留信息。Horizon sweep 用来检验 GVF timescale 是否需要匹配该 delay。

## Expected Results And Failure Modes / 预期结果与失败模式

预期 upper bound 是 oracle memory，其次是 trace memory。Raw observation 除了 cue 仍可见的位置外应接近 chance。Cue-GVFs 和 terminal-GVFs 可能保留部分 cue information，而 junction/bias GVFs 应作为 negative control。强正向结果需要 learned GVF condition 在不同 maze lengths 上同时表现出 above-chance decision cue decoding 和 improved trial accuracy。混合结果是 cue decoding 高于 chance 但 trial accuracy 接近 chance；这会指向 control-utilization 或 output-scale failure。负结果是 decodability 和 control 都接近 chance，说明需要重设计 cumulants 或 state-construction mechanisms。

## Current Results / 当前结果

Main run 已从 `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json` 启动。本节将在 `metrics.csv`、`condition_summary.json` 和 report figures 写出后，用 completed main-run numbers 和 figures 替换。

计划主图：

- `figures/report_upk_trial_accuracy_by_length.png`
- `figures/report_upk_decision_decoding_by_length.png`
- `figures/report_upk_cue_margin_by_length.png`

## Reviewer Critique And Revisions / 审稿批评与修订

| Reviewer angle | Critique | Current response | Remaining risk |
|---|---|---|---|
| Alberta Plan | Predictive knowledge 太宽，除非 utility 被 operationalized。 | 报告把 utility 定义为 information plus downstream control use。 | 后续 component-utility gates 仍不在当前实验内。 |
| Core RL | T-maze 可能太小。 | 它小但结构上有意义：raw observation 失败，trace/oracle baselines 解决 hidden-state problem。 | 第二个 delayed-cue stream 会增强 generality。 |
| GVF reviewer | Prediction error 不是正确目标。 | GVF TD error 是 secondary；cue decodability 和 trial accuracy 是 primary。 | 可能仍需要更好的 GVF question families。 |
| Statistics | 条件多，可能遮住主 claim。 | Figures 按 maze length 和 gate metric 分组，而不是展示所有 learning curves。 | 结果完成后应增加 best-GVF-per-length compact table。 |
| Strict instructor | 不要把它说成 agent-state construction 的解法。 | 报告只定位为 Gate 1 和 Gate 2。 | Feature-budget 和 plasticity stages 仍是 future work。 |

## Threats To Validity / 有效性威胁

T-maze 能隔离 partial observability，但不能覆盖 agent-state construction 的所有形式。当前 GVF designs 仍是 hand-selected；差结果可能反映 question design 差，而不是 predictive knowledge 本身的限制。Cue-decoding metric 是 information proxy，不能替代 downstream control。反过来，如果 control improvement 没有 decodability，也需要谨慎解释，因为 agent 可能利用的是 hidden cue 的 correlate，而不是 cue 本身。当前 main run 使用 10 seeds；如果第一轮结果显示某些条件最有信息量，最终更强证据可能需要 20 seeds 或 CPU-task extended sweep。

## Conclusion / 结论

本 proposal 把 Alberta Plan 中 broad predictive knowledge idea 转化为一个具体 Core-RL test：prediction 只有在保留 hidden variable 并改善 downstream control 时，才应成为 state。实验有意保持小型，但不是坏意义上的 toy；它有真实 partial-observability failure mode、有可解任务的非 deep baselines、有 GVF question 和 horizon ablations，并且 metrics 能区分 prediction accuracy 和 usefulness。科学价值在于 gate 本身：它可能支持正向 learned-state result，也可能明确指出当前 predictions 为什么还不够 useful。

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
