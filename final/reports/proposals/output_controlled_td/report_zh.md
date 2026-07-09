# Output-Controlled TD 中文报告

状态：独立主线 proposal；当前可引用证据仍是 main pilot。20-seed CPU-task extended run `core-rl-output-extended-fixed-46602102` 正在运行，`experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended` 目前是不完整/空结果目录，不能引用为完成证据。它是最早指定的两个 Core RL 题目之一，研究重点是 streaming TD 更新的“输出效果”是否比 raw parameter step 更适合作为稳定学习单位。

## 摘要

在线 TD 学习里，固定参数步长 `alpha` 并不等价于固定 prediction change。在线性函数逼近中，如果把 feature vector 放大 10 倍或 100 倍，底层预测问题可以基本不变，但同一个 raw `alpha` 会造成完全不同的 parameter displacement 和 prediction displacement。这个 proposal 在 tile-coded random-walk prediction 中比较 fixed TD、normalized TD、trace-normalized TD(lambda) 和 true-online TD(lambda)，检验 output-controlled update 是否能在不同 feature scale 下保持稳定。当前 main pilot 显示：fixed TD 在 high-scale feature 下容易发散，normalized 和 trace-normalized TD 在测试的 scale/alpha grid 中保持稳定；true-online TD(lambda) 当前实现/参数网格下也会在 high-scale/high-alpha 条件发散，但这不能被解释成对 true-online TD 的一般否定，必须做更公平的 max-stable-alpha audit。

## 研究动机

Streaming RL 没有 replay buffer、minibatch 和离线多轮优化来平滑异常样本。Agent 每一步都从当前 transition 更新，任何 feature magnitude 的变化都可能直接变成一次很大的参数移动。对于长期存在的 continual agent，假设所有 sensor、representation channel、tile coding 或 auxiliary feature 都已经被人工缩放到匹配某个固定 `alpha`，并不现实。

Alberta Plan 强调 ordinary experience、continual value-function learning 和大量 predictions。这样的 agent 可能同时维护许多 value functions、GVFs、models 或 control values。若每个预测都需要手工调 `alpha` 才能适应 feature scale，系统就很难保持可扩展和可维护。Output-Controlled TD 的核心动机是把 `alpha` 解释成“希望 prediction output 改变多少”的单位，而不是“parameter vector 移动多少”的单位。

## 研究问题

主问题：在 streaming linear TD prediction 中，normalized 或 output-controlled updates 是否能显著扩大 feature scale 和 alpha 的稳定区域？

具体问题包括：固定 `alpha` 是否会因为 feature scale 改变而从稳定变成发散；把 update 除以当前 feature norm 或 eligibility trace norm 是否能让 prediction-change magnitude 更一致；trace-normalized TD(lambda) 是否能把这个思想推广到带 eligibility traces 的在线更新；true-online TD(lambda) 在公平 step-size 审计后是否仍然是强 baseline。

## Alberta Plan 关联

这个 proposal 直接关联 value functions、streaming one-sample learning、limited computation、step-size adaptation 和 temporal uniformity。它没有使用 deep network，也没有 replay buffer。虽然它是 prediction-only 任务，但研究的是一个会影响所有 continual RL value learning 的基础机制：更新的单位究竟应该是 parameter space 还是 prediction/output space。

## 环境设计

实验环境是 tile-coded random-walk value prediction。Agent 在随机策略下观察一维 random walk 的 transitions，并预测到达右端 terminal 的概率。这个任务本身简单，但使用 overlapping tile-coded features 让 representation scale 成为可控变量，从而隔离 feature magnitude 对 TD update 的影响。

当前 main pilot 使用四类 feature scale：`one` 表示正常尺度；`ten` 和 `hundred` 分别把 feature magnitude 放大 10 倍和 100 倍；`uneven` 使用非均匀 feature scaling，模拟不同 sensor/feature channel 尺度不一致的情况。Extended config 进一步加入 `lognormal` scale，并扩大 alpha/seeds/steps；该 CPU run 完成前，报告结论只基于 main pilot。

## 方法

比较方法包括 fixed TD、normalized TD、trace-normalized TD(lambda) 和 true-online TD(lambda)。Fixed TD 使用固定 raw `alpha`，update 方向是当前 feature 或 eligibility trace，因此同一个 TD error 在大尺度 feature 下会造成更大的 prediction movement。Normalized TD 使用近似 `alpha / (epsilon + ||x_t||^2)` 的缩放，使同一个 `alpha` 更接近对当前 prediction 的 output-level change 控制。Trace-normalized TD(lambda) 则用 `epsilon + ||z_t||^2`，因为带 trace 时实际 update direction 是 accumulated eligibility trace 而不是当前 feature 本身。

True-online TD(lambda) 被纳入是因为它是重要的 online trace baseline。但当前报告对它保持谨慎：如果直接使用同一 raw alpha grid，它在 high-scale/high-alpha 下发散，并不能自动说明 true-online TD 不好；更合理的批评是本 proposal 必须补充 true-online 的 max-stable-alpha 和 canonical sanity audit。

## 实验设计

当前可引用 main pilot result path 是 `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`。实验变量包括 feature scales `one/ten/hundred/uneven`，alphas `0.03/0.1/0.3`，lambda 对 trace variants 使用 `0.8`，seeds `0-4`，steps `5000`。主要指标包括 RMSE、divergence flag、weight norm、prediction_change 和 effective step size。

这个实验不把“某个 alpha 下最低 RMSE”作为唯一成功标准。更重要的判据是同一 alpha range 是否能跨 feature scales 稳定工作，以及 prediction-change magnitude 是否因为 feature scale 变化而失控。一个方法如果只要每换一个 scale 就重新调 alpha 才能稳定，就不适合被解释成 streaming-compatible。

Extended 设计包括 seeds `0-19`、steps `20000`、scales `one/ten/hundred/uneven/lognormal`、alphas `0.01/0.03/0.1/0.3`。当前 CPU task 名为 `core-rl-output-extended-fixed-46602102`，目标目录是 `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`。在该目录出现 `condition_summary.json`、`config_used.json` 和 figures 前，它只能算 running/incomplete，不应写进结果索引。

## 当前结果

![不同 algorithm、scale 和 alpha 下的 tail RMSE stability atlas。](../../../../experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main/figures/report_log_rmse_heatmap.png)

![不同 algorithm、scale 和 alpha 下的 divergence-rate atlas。](../../../../experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main/figures/report_divergence_heatmap.png)

![不同 algorithm、scale 和 alpha 下的 output-change atlas。](../../../../experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main/figures/report_prediction_change_heatmap.png)

Main pilot 中，fixed TD 在 `hundred` scale 下对所有测试 alpha 都发散，在 `ten` scale 且 alpha `0.3` 时也发散，并且在若干 `uneven` 条件下出现非常大的 RMSE 或 weight norm。这支持核心担忧：raw `alpha` 并不是跨 feature scale 稳定的学习单位。

Normalized TD 在所有测试 scale 和 alpha 下保持 finite，RMSE 大致处于 `0.44-0.56` 范围；trace-normalized TD(lambda) 也保持相近稳定区间。这个结果说明用 feature norm 或 trace norm 控制 update magnitude，可以显著降低 feature scale 对 TD stability 的影响。

True-online TD(lambda) 在 easy scale 条件表现正常，但在 high-scale/high-alpha 条件发散。当前报告只把它当作 baseline audit 的提示：需要更小 alpha、更多 lambda 条件和 canonical true-online verification 后，才能对其公平评价。

## 分析

这个 proposal 的核心 insight 不是 normalized TD 在某个曲线上 RMSE 更低，而是 `alpha` 的语义不同。Fixed TD 的 `alpha` 是 parameter-space multiplier；当 feature scale 改变时，它对 prediction output 的影响随之改变。Normalized TD 尝试让 `alpha` 更接近 output-space unit，使更新行为对 feature scaling 更鲁棒。

这对 continual RL 很重要。Long-lived agent 可能不断加入新 features、改变 sensory preprocessing、生成 auxiliary predictions，或者从环境中遇到 scale 变化。如果每次 representation scale 改变都要人工重新调所有 `alpha`，agent 的学习系统就不是 self-maintaining 的。Output-controlled update 提供了一种低计算成本的机制，让 value learning 更适合 streaming setting。

Trace-normalized TD(lambda) 的意义在于 eligibility traces 会改变 update direction 的 scale。只归一化当前 feature 不一定足够，因为真正写入 weights 的是 trace。当前 pilot 显示 trace normalization 能继承 normalized TD 的稳定性，但还需要更系统地扫 lambda 和 alpha。

## 有效性威胁

第一，当前任务是 prediction-only。它让机制更干净，但不能自动证明 control 中 policy improvement 也更稳定。后续应连接到 normalized Sarsa、actor-critic 或 reward-centered continuing control。

第二，true-online TD(lambda) baseline 还不够公平。当前 raw alpha grid 可能对 fixed/true-online baseline 太粗，应加入 max-stable-alpha 表和已知小任务 sanity check。

第三，当前 main pilot 只有 5 seeds 和 5000 steps。Divergence 模式强，但最终报告应等待正在运行的 extended 20-seed 结果完成后再升级主要证据。

第四，feature scaling 是 synthetic stress test。它适合研究 invariance，但真实 sensor stream 可能同时有 nonstationary scale、sparse features 和 changing relevance。更强实验应加入 midstream scale switch 且不 reset weights/traces。

## 审稿式批评与回应

严格 reviewer 可能会说：random walk prediction 太简单，像数值技巧。回应是：本 proposal 的问题本来就是 update geometry 和 scale robustness；tile-coded overlapping features、scale/alpha grid、prediction-change logging 让这个问题可解释。下一步需要把机制迁移到 control，但不应在机制没弄清前直接上复杂 benchmark。

Baseline reviewer 会指出：true-online TD(lambda) 不能被随便当作负结果。回应是：报告已经明确这只是当前配置下的 baseline warning；后续必须补 max-stable-alpha audit。

Alberta Plan reviewer 会追问：这个 prediction-only 题目为什么有长期 agent 意义。回应是：Alberta Plan 的许多组件都依赖持续学习的 value functions 和 predictions。如果基础 TD update 的 step-size 语义随 representation scale 任意改变，后续 GVF、model、option value 或 actor-critic 都会继承这个不稳定性。

## 结论

当前证据支持 Output-Controlled TD 的基本观点：streaming TD 不应只控制 raw parameter movement，还应控制 update 对 prediction output 的影响。Normalized 和 trace-normalized TD 在测试的 feature-scale stress grid 中更稳，而 fixed TD 明显脆弱。作为独立 Core RL 课题，它的研究问题清晰、机制可解释、与 Alberta Plan 的 value-function learning 关系直接；但最终版本仍需要 extended 结果、true-online baseline audit，以及至少一个 control-side extension 才能达到更强论文级证据。

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_main.json

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/plot_results.py --result-dir experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main --y-key rmse --group-keys algorithm scale alpha
```

Extended run 当前通过 CPU task wrapper 提交。若当前长实验完成，应先核对 `config_used.json`、`condition_summary.json` 和 figures，再把新 result path 回填到本报告、`final/indexes/results_zh.md` 和 `final/indexes/reproduction_zh.md`。

```bash
PARTITION=safethm_cpu_task CPU=8 MEM=16000 bash experiments/alberta_core_rl/scripts/run_cpu_task.sh core-rl-output-extended-fixed "PYTHONNOUSERSITE=1 python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/output_controlled_td/config_extended.json"
```
