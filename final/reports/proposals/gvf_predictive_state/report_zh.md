# GVF Predictive State 中文报告

状态：独立负结果 proposal；当前最适合作为 predictive-state redesign 的依据，而不是正向 GVF 成功案例。

## 摘要

本 proposal 检验 General Value Function predictions 是否能在 partial observability 下成为有用 agent state。T-maze 任务中，agent 在起点看到左右 cue，之后进入 aliased corridor，直到 junction 才需要根据早期 cue 选择动作。当前 main pilot 比较 raw observation、short history、trace memory、recurrent GVF features 和 oracle memory。Trace memory 与 oracle memory 能解决任务，而当前 recurrent GVF design 仍接近 chance。这个结果不说明 GVF 一般无用；它说明当前 GVF question/state design 没有携带 control 所需的 hidden cue 信息。

## 研究动机

在 partially observable environments 中，当前 observation 不是完整 state。长期 agent 必须从经验中构造可用于控制的 state。Alberta Plan 把 GVFs 视为一种重要路线：agent 可以通过预测未来信号形成知识，并把这些 predictions 用于后续决策。但这里有一个关键陷阱：一个 prediction 可以稳定、准确，却对当前 decision 完全无用。

本 proposal 的目标不是增加一个装饰性 auxiliary prediction，而是严格问：learned prediction 是否能补上 observation 中缺失的信息？在 T-maze 中，这个缺失信息很具体，就是早期 cue。若 GVF 不能把 cue 信息带到 junction，它就不能被称为 useful state。

## 研究问题

主问题：learned GVF predictions 能否在 partially observable T-maze 中提供缺失的 cue information，从而改善 trial-end control accuracy？

更具体地说，加入 recurrent GVF feature 是否能明显优于 raw observation 和 short history，并接近 cheap trace-memory baseline？Trace baseline 被故意设置得强而简单，因为如果一个非深度手写 trace 能解决任务，而 GVF 不能接近它，就不能把当前 GVF 设计包装成正结果。

## Alberta Plan 关联

这个 proposal 直接对应 GVFs、predictive knowledge、agent-state construction、partial observability 和 online value learning。它符合 Alberta Plan 的方向，但当前证据是负结果，因此最专业的处理方式是把它作为边界条件和 redesign target，而不是强行宣称 GVF state 成功。

## 环境设计

环境是 long aliased T-maze。Trial 开始时 observation 显示 binary cue；在 corridor 中 observation 不再显示 cue；到 junction 时 correct action 依赖早期 cue；junction decision 后 trial reset 并采样新 cue。Agent 持续在线学习，accuracy 在 trial-end decisions 上统计。

这个环境的研究用途很明确：raw observation 不足以控制；oracle memory 说明上界；trace memory 说明小型非深度记忆足够解决任务；GVF feature 必须证明自己能携带 hidden cue，而不是只降低某个预测误差。

## 方法

比较的 state constructions 包括 raw observation、short history、trace memory、recurrent GVF features 和 oracle cue memory。Control 使用 online linear Sarsa。Oracle 是上界，trace memory 是低成本强 baseline，recurrent GVF 是真正被测试的 proposal mechanism。

当前 implementation key 是 `useful_gvfs_state`，这与报告名 `GVF Predictive State` 不完全一致；保留该名字是为了保持已有 result provenance。

## 实验设计

当前 main pilot 使用 maze length `12`，seeds `0-4`，steps `5000`。主要指标包括 trial-end accuracy、average reward、GVF TD error、cue traces、position-level trajectories 和 control TD error。结果路径是 `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`。

![不同 state construction 的 trial accuracy。](../../../../experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main/figures/trial_accuracy_by_algorithm_curve.png)

![GVF values 和 cue traces 随 maze position 的变化。](../../../../experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main/figures/gvf_trace_by_position.png)

## 结果

Trace memory 与 oracle memory 能解决任务，seed-aware tail trial accuracy 分别约为 `0.944 +/- 0.018` 和 `0.939 +/- 0.027`。这说明在项目限制下，任务并不是不可解；小型非深度记忆足以提供所需 state augmentation。

Raw observation、short history 和 recurrent GVF 仍接近 chance，约为 `0.512`、`0.492` 和 `0.502`。当前 GVF state 因此没有携带 junction decision 所需的 cue information。Trajectory plot 也支持这个解释：learned GVF signal 没有像 hand-coded trace 那样形成清晰且持续到 junction 的 cue-dependent trace。

## 分析

这个负结果有价值，因为它排除了几个模糊解释。第一，任务不是无法被小 agent 解决，因为 trace/oracle 成功；第二，control learner 不是完全坏掉，因为在合适 state 下它能学；第三，失败集中指向当前 GVF question/state design 不足。

这也给 GVF 研究提出了更严格标准：不是所有 prediction 都值得进入 agent state。一个 useful GVF 应该同时满足至少三个条件：它预测的问题与 hidden variable 或未来 decision 有关；它的 output scale 和 dynamics 能被 control learner 使用；它在 downstream control 上接近或超过简单 memory baseline。

## 有效性威胁

当前只测试一种 recurrent GVF design，不能据此否定 GVFs。报告缺少直接 cue-decodability linear probe，因此“GVF 未携带 cue”主要由 control accuracy 和 trajectory plot 推断。Maze length 固定为 `12`，后续应扫 corridor length 和 cue semantics。GVF cumulant/discount 选择也可能不对，需要与 `GVF Question Design` 和 `Predictive State Plasticity` 结合重做。

## 审稿式批评与回应

GVF reviewer 会指出：预测一个容易但无关的信号不是 useful state。回应是：报告明确加入 trace/oracle baselines，并把 trial-end control accuracy 作为主要指标，而不是只看 GVF TD error。

Strict baseline reviewer 会指出：如果 trace memory 这么便宜，GVF 必须接近它才值得宣传。回应是：当前报告不宣传正结果，而把 recurrent GVF 降级为 redesign target。

下一步必须加入 cue-decodability probe、hidden-cue correlation plot 和更贴近未来 cue-relevant events 的 cumulant 设计。

## 结论

GVF Predictive State 是一个独立负结果。它说明当前 T-maze 任务可由 cheap memory 解决，但当前 learned GVF feature 不能解决。下一轮不应只调超参数，而应重新设计 GVF questions，使 learned prediction 明确携带 hidden cue，并在 junction decision 上产生可测的控制收益。

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/useful_gvfs_state/config_main.json
```
