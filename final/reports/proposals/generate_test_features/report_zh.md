# Generate-and-Test Trace Features 中文报告

状态：独立 negative/redesign proposal。当前实验不是 generate-and-test 的正向证据；它说明 utility rule 和 testbed 在升级前必须重设计。

## 摘要

Continual agent 需要能在在线学习中改变的 representation。本 proposal 研究这个问题的最小形式：prediction agent 只有很小的 temporal trace feature budget，reward delay 在 stream 中改变，agent 必须决定保留或替换哪些 traces。原始假设是 utility-based generate-and-test replacement 会比 fixed trace banks 或 random replacement 更快恢复有用 timescales。Pilot 不支持这个假设。Generate-and-test 经常把 active trace timescales 移向新的 delay，但没有相对于 fixed 或 random baselines 降低 prediction error。因此它是一个 negative redesign result：研究问题是有效的 Core RL 问题，但当前 utility proxy 还没有和 downstream prediction improvement 对齐。

## Evidence Summary / 证据摘要

本报告是 negative generate-and-test pilot。它把两类证据分开：structural feature movement 和 downstream prediction error。当前 utility rule 可以改变 feature set，但 downstream error metric 没有改善。这个区分是本报告最主要的研究价值，因为 continual agent 应根据 feature 对 prediction 或 control 的贡献来选择 features，而不是因为 feature 看起来 plausible。

| 项目 | 当前证据 |
|---|---|
| RL question | 在固定 trace-feature budget 下，utility-based generate-and-test replacement 能否在 reward delay 改变后保留或恢复有用 temporal traces？ |
| Testbed | Streaming trace-conditioning prediction stream，包含 cue、delayed reward，以及从 `10` 到 `20` 的 midstream delay switch。 |
| Compared feature strategies | Fixed tight trace bank、oracle-style trace bank、random replacement 和 utility-based generate-and-test replacement。 |
| Seeds and horizon | 五个 seeds，`5000` online steps，feature budget `4`。 |
| Primary metric | Delay switch 后的 post-late absolute prediction error；replacement count 和 trace timescale movement 是诊断指标。 |
| Headline result | Post-late absolute error：random replacement 为 `0.0496 +/- 0.0004`，fixed tight traces 为 `0.0512 +/- 0.0000`，generate-and-test 为 `0.0518 +/- 0.0004`，当前 oracle-style bank 为 `0.0545`。Generate-and-test 会改变 features，但没有改善 behavioral metric。 |
| Conclusion boundary | 这是当前 utility rule 和 testbed 的 negative redesign result。它不否定 generate-and-test 一般方法，但在加入 validation stream 和 loss-aligned utility rule 前，不能提出正向 feature-learning claim。 |

## 研究主张与证据等级

这是独立 representation-learning proposal。它的主张必须保持窄：

> 在当前 delay-switch trace-prediction stream 中，已实现的 generate-and-test utility rule 会改变 feature set，但不会改善 downstream prediction error。

证据等级是 negative/redesign。它不能被写成成功的 feature-learning result，因为主要 behavioral metric 没有改善，oracle trace bank 也没有被验证为上界。

## Research Motivation/Question/Method / 研究动机/问题/方法

Alberta Plan 强调 ordinary experience、continual learning、limited computation、value functions、learned models、planning 和 feature finding。长期 agent 不可能保留所有可能 feature。Reward delays、sensor statistics 和 task-relevant history lengths 都可能在 agent 持续运行时改变。固定 representation 要么把容量浪费在 stale features 上，要么要求研究者手工 retune。

Generate-and-test 的吸引力在于把 representation maintenance 写成在线过程：生成候选 features，从数据流中测试 utility，并替换低 utility features。难点不在于生成看起来合理的 features，而在于判断一个 feature 是否改善 agent 的 prediction 或 control objective。一个 trace 的 timescale 接近 reward delay，仍然可能是冗余的、尺度不合适的，或与当前 update rule 耦合不好。本 proposal 直接检验这种 mismatch。

### Focused RL Question / 聚焦 RL 问题

Focused RL question 是：

> 在固定 trace-feature budget 下，utility-based generate-and-test replacement 能否在 reward delay 改变后保留或恢复有用 temporal traces？

操作性假设是：

> 有用的 generate-and-test rule 应该比 fixed trace banks 和 random replacement 改善 post-change recovery 与 late prediction error。

Pilot 对当前 utility rule 否定了这个操作性假设。它不否定 generate-and-test 这一类方法。

### RL Setting / RL 设置

环境是 streaming trace-conditioning prediction problem：

- observation stream 中出现 cue；
- reward 在某个 delay 后出现；
- stream 中点以后 delay 从 `10` 变为 `20`；
- learner 只能在线看一次 stream，没有 replay buffer，也没有 offline training phase；
- feature budget 很小，因此 learner 不能包含所有 plausible trace timescales。

这个 setting 隔离了 continual representation 问题。它故意比 control task 小，使 feature replacement events、trace timescales 和 prediction errors 都可以直接审计。

### Method / 方法

比较的 feature strategies 包括：

- fixed tight trace bank；
- oracle-style trace bank；
- random replacement；
- generate-and-test replacement。

所有方法使用同一个 streaming prediction problem 和同一个有限 feature budget。Generate-and-test condition 在线估计 feature utility，并用新采样 traces 替换低 utility traces。Random replacement 用来检验单纯 churn 是否有帮助。Oracle-style bank 本意是 matched-feature diagnostic，而不是已证明的上界；它在 pilot 中表现弱，正是本 proposal 仍需 redesign 的原因之一。

本研究区分两类证据：

- structural evidence：active trace timescales 是否靠近当前 delay；
- behavioral evidence：prediction error 和 recovery 是否改善。

只有第二类证据能支持正向 representation-learning claim。

## Experimental Design / 实验设计

当前 main pilot：

- Feature budget：`4` traces。
- Delay switch：stream 中点。
- Seeds：`0-4`。
- Steps：`5000`。
- Result path：`experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`。

主要指标：

- absolute prediction error；
- late post-change absolute prediction error；
- delay switch 周围的 recovery-window summaries；
- active trace timescales 到当前 target delay 的距离；
- replacement count 和 feature survival。

主图：

![Delay-shift prediction error by feature strategy.](../../../../experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main/figures/abs_error_by_algorithm_curve.png)

## Results / 结果

Generate-and-test 经常让 active trace timescales 比 fixed 或 random traces 更接近 target delay。这个 diagnostic 说明 replacement 确实产生了可解释行为。然而这种改善是 structural，而不是 behavioral。它没有带来更低 prediction error。

Late post-change absolute error 约为：

| Strategy | Late post-change absolute error |
|---|---:|
| Random replacement | `0.0496` |
| Fixed tight traces | `0.0512` |
| Generate-and-test | `0.0518` |
| Current oracle-style bank | `0.0545` |

Oracle-style result 是警告信号。如果 supposedly matched trace bank 不能明确优于 generic baselines，这个环境还不是干净的 feature-selection test。Pilot 因此暴露的是 design failure，而不是成功的 generate-and-test mechanism。

## Analysis / 分析

这个负结果有信息量，因为 feature diagnostics 和 prediction metric 发生了分歧。可能机制包括：

1. Utility 与 prediction objective 不对齐。当前 score 可能偏好活跃或 timing 看似正确的 traces，而不是估计它们对 prediction error 的边际降低。
2. Feature bank 可能冗余。多个 trace timescales 可以支持相似预测，因此靠近 nominal delay 未必足以改变 linear predictor 的 error。
3. Stream 可能 underpowered。单次 delay switch 不一定产生足够持续的压力，让 utility replacement 显示优势。
4. Oracle 没有被验证。如果 oracle-style bank 不是稳定赢家，testbed 就无法区分弱 utility rule 和 trace choice 本身不重要这两种情况。
5. Replacement 可能扰乱学习。替换 features 会在 weights 仍适应时改变 input basis，因此结构上更好的 feature 可能暂时伤害 prediction。

这些机制把解释限制在合理范围内。本研究说明当前 utility rule 对这个 stream 不够，而不是说明 feature generation 不重要。

## 局限与有效性威胁

Pilot 只有一次 delay switch，seed 数也少。更强研究应测试 repeated switches、多组 delay pairs 和 feature-budget sweeps。

Oracle-style baseline 还不是真正上界。任何正向 claim 前，都必须包含一个已知 trace bank，且它能稳定改善 prediction error。

当前 utility rule 很紧凑，不能代表所有 generate-and-test 方法。

任务是 prediction-only。下游 control setting 可能以不同方式评价 traces，但那需要新的实验，不能重新解释这个 pilot。

## Next Experiments / 下一步实验

这个 proposal 只能以 redesign 方式推进：

1. 构建 validation stream，使一个 hand-specified trace bank 能稳定在 prediction error 上击败 generic trace banks。
2. 加入 repeated nonstationary delay changes，让 stale features 形成持续压力。
3. 用直接绑定 downstream loss 的 utility 替换当前 proxy，例如估计 feature 对 TD-error reduction 或 recovery speed 的贡献。
4. 做 budget sweep，确认 trace capacity 什么时候真的稀缺。
5. 保留 random replacement 和 fixed banks 作为 baselines，同时报告 feature diagnostics 与 prediction metrics。

升级标准很简单：在同样 online、limited-budget 条件下，generate-and-test 必须改善 recovery 或 late prediction error。

## Alberta Plan Connection / Alberta Plan 关联

该 proposal 关联 Alberta Plan 的 feature finding、ordinary experience、continual adaptation 和 limited computation。它也遵循“learned components 应按 utility 而非 plausibility 评价”的思想。实验保持小型线性 setting，是为了在进入更复杂 prediction 或 control setting 前先检查机制。

本地参考：

- `resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

## Reviewer Critique / 审稿批评

| 审查角度 | 批评 | 本报告修订 | 剩余风险 |
|---|---|---|---|
| Representation learning | Plausible feature dynamics 不是 useful representation learning 的证据。 | 报告区分 structural diagnostics 和 downstream prediction error。 | 需要与 loss reduction 绑定的 utility。 |
| 实验设计 | Oracle-style bank 不是清楚上界。 | 证据等级写为 negative/redesign，而非 positive。 | 需要 known traces 稳定胜出的 validation stream。 |
| Core RL scope | Proposal 必须提出 focused RL question，而不是只排名方法。 | 问题限定为 delay change 后的 limited-budget online feature adaptation。 | 需要 repeated nonstationarity 才更强。 |
| 严格解释 | 不要把 structural feature movement 夸大为正向证据。 | 报告标记为 independent 和 negative。 | 后续写作必须保持这个证据等级。 |

## Proposal Template Answers / 提案模板回答

Focused RL question：在 limited feature budget 下，generate-and-test replacement 能否发现改善 nonstationary delay prediction 的 temporal trace features？

Setting/testbed：reward delay 从 `10` 切到 `20` 的 streaming trace-conditioning prediction task。

Implemented comparison：fixed tight traces、oracle-style traces、random replacement 和 utility-based generate-and-test replacement。

Observation or metric：absolute prediction error、delay switch 后 recovery、active trace timescale、replacement behavior 和 feature survival。

Compute and fallback：CPU-scale，seeds `0-4`，`5000` steps。当前 fallback 是 negative redesign result，不是正向 feature-learning claim。

## Conclusion / 结论

这是关于 limited-capacity online representation adaptation 的独立 proposal。它的贡献是诊断：当前 utility mechanism 产生了可解释的 trace movement，但没有带来 downstream error improvement。正确下一步不是推广当前 generate-and-test rule，而是重设计 utility measure 和 validation stream，使任何正向结果都必须在同样 online feature budget 下体现为更好的 recovery 或更低 late prediction error。

## Reproduction / 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/generate_test_features/config_main.json
```
