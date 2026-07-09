# GVF Question Design 中文报告

状态：独立 useful-prediction design diagnostic；当前证据用于 redesign，不是完成的 GVF control claim。

## 摘要

本 proposal 研究一个先于“把 GVFs 当作 agent state”出现的设计问题：哪些 predictive questions 值得学习？一个 GVF 可以有很低 prediction error，但如果它预测的是常数、局部可见信号，或与 control 所需 hidden information 无关的变量，它仍然没用。本文的中心信息是：

> prediction error != usefulness。

当前 diagnostic 使用 T-maze stream，并为不同 cumulants 和 discount horizons 训练 linear GVF predictors。Bias predictions 容易但无用；cue 和 junction questions 暴露出必须根据 hidden cue information 与 downstream junction action 来评价 prediction。本报告的贡献是 useful-prediction design diagnostic，而不是证明 GVF state 已经提升 control 的最终结果。

## Claim 边界

本报告只提出一个受限 claim：

> 在当前 T-maze question-design diagnostic 中，低 GVF prediction error 不足以识别 useful state features；GVF questions 需要 explicit usefulness probes，例如 cue decodability 和 downstream control ablations。

本报告刻意不声称：

- 测试的 GVFs 已经解决 T-maze control；
- 某个 cumulant/discount pair 普遍最好；
- TD error 是主要成功指标；
- 在没有 downstream probes 的情况下，GVF predictive state 已经被验证。

## Research Motivation/Question/Method / 研究动机/问题/方法

Alberta Plan 把 GVFs 看作通向丰富 predictive knowledge 的路径。这个路线不仅需要学习答案，也需要选择问题。如果 agent 学会成千上万个准确但无关的 predictions，得到的 state 可能更大、更慢，却对 decision-making 没有帮助。

T-maze 让这个问题具体化。这个任务可以通过 trace-like cue memory 解决，但 recurrent GVF design 如果没有提出能保留相关信息的问题，仍然可能失败。这不应只被解释为 algorithmic bug，也可能是 question-design failure：学到的 predictions 没有在 junction 保留 control-relevant hidden cue。

### Focused RL Question / 聚焦 RL 问题

主问题：

> 哪些 GVF cumulant 和 discount questions 只是 learnable，哪些才是 partially observable T-maze 中 useful predictive state 的合理候选？

子问题：

- 哪些 GVFs 有低 TD error？
- 哪些 GVFs 在 junction 保留 hidden cue 信息？
- 哪些 GVF feature sets 会改善、不影响或损害 downstream junction action？

假设：

> Prediction error alone 不能识别 useful GVF questions。Useful question 必须通过它与 hidden state information 或 downstream control 的关系来评价。

### Core RL Connection / 与 Core RL 的关联

这是 core RL proposal，因为它研究 partial observability 下的 prediction questions 和 state construction。它连接：

- GVFs 和 predictive knowledge；
- online agent-state construction；
- question discovery and evaluation；
- useful prediction 而不是 raw prediction accuracy；
- control-scale experiments 之前的小型可解释诊断。

该 proposal 是独立的，因为它回答一个 standalone design question：GVF-based state learner 应该预测什么？

### Related Work / 相关工作

Horde 和 GVF work 说明为什么要从 stream 中学习许多 predictions。Useful-prediction work 询问哪些 predictions 会改善 learning 或 behavior。Online agent-state work 则把 predictions 作为 partial observability 下的 state features。

本地参考：

- `resources/alberta_plan_related/finding_useful_predictions_2111.11212.pdf`
- `resources/alberta_plan_related/horde_lifelong_offpolicy_1206.6262.pdf`
- `resources/alberta_plan_related/learning_agent_state_online_2112.15236.pdf`

### Method / 环境与方法

环境是 T-maze stream，包含可观察 signals：

- left cue；
- right cue；
- junction；
- bias。

Hidden control-relevant variable 是早先出现、并应决定 junction action 的 cue。这使得该任务适合区分 easy prediction 和 useful memory。

方法是在每个 cumulant 和 discount combination 下训练 linear TD predictors。变化的设计因素是：

- cumulant identity；
- discount horizon。

当前 cumulants：

- `left_cue`；
- `right_cue`；
- `junction`；
- `bias`。

当前 discounts：

- `0`；
- `0.5`；
- `0.9`；
- `0.98`。

当前 learner 记录 prediction behavior。下一版必须加入 explicit usefulness tests。

## Experimental Design / 实验设计

当前 main diagnostic：

- Seeds：`0-4`。
- Steps：`5000`。
- Result path：`experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main`。

当前测量：

- absolute TD error；
- prediction value；
- weight norm。

主图：

![GVF TD error by cumulant and discount.](../../../../experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main/figures/abs_td_error_by_cumulant-gamma_curve.png)

设计逻辑：

| 设计元素 | 为什么需要 |
|---|---|
| Multiple cumulants | 区分 trivial signals、cue-related signals 和 decision-location signals。 |
| Multiple discounts | 测试 horizon choice 是否改变保留的信息。 |
| T-maze stream | 提供有已知 hidden cue 的简单 partial-observability problem。 |
| TD error | 测量 learnability，但不测量 usefulness。 |
| Planned cue probe | 测量 prediction 是否帮助恢复 hidden variable。 |
| Planned control ablation | 测量 prediction 是否影响 decision quality。 |

## Results / 结果

当前 run 显示三个定性类别：

- Bias GVFs trivial 且 accurate，但对 cue memory 无用。
- Cue GVFs 有更非平凡的 errors 和 discount-dependent value profiles，因此是 state features 的可能候选。
- Junction predictions 是 learnable 的，但它们本身不能解决 memory problem，因为 junction signal 到达的是 decision point，而不是保留 earlier cue。

结果支持核心诊断结论：learnability 和 usefulness 是不同性质。

当前 result summary 也以数字形式体现了这种模式。Gamma 为 `0`、`0.5` 和 `0.9` 的 bias predictions 有接近零的 tail absolute TD error，而 long-horizon bias GVF 在 gamma `0.98` 时 tail absolute TD error 约为 `0.1002`。Cue GVFs 在测试的 discounts 上 tail absolute TD error 约为 `0.0960-0.1666`，junction GVFs 约为 `0.1706-0.2563`。这些数字适合审计 learnability，但不能回答 predictions 是否在 decision point 保留 hidden cue。

## Analysis / 分析

早先 GVF predictive-state design 的可能失败机制不只是 high prediction error。至少有几类可能：

- Trivial-prediction failure：bias 或局部 signal 被准确预测，但不携带 hidden cue information。
- Horizon mismatch：discount 让 prediction 过于 myopic 或过于 diffuse，无法把 cue 保留到 junction。
- Location mismatch：junction prediction 标记了 decision point，但不识别正确 action。
- Representation bottleneck：GVF answer 被学到，但没有以 controller 可用的方式编码。
- Objective mismatch：最小化 TD error 可能奖励 predictability，而不是 decision relevance。

这些机制解释了为什么“低 TD error”不应被当作成功。Useful-prediction proposal 必须问“useful for what?”，并用 measured probe 回答。

## Next Experiments / 下一步实验

下一步实验应把 usefulness 操作化：

1. Cue-decodability probe：从 GVF outputs 到 junction 处 hidden cue 训练一个小 linear probe。
2. Downstream control ablation：比较 raw observations only、observations plus each GVF group，以及 observations plus trace-memory baseline 的 controllers。
3. Question-set ablation：测试 cue-only、junction-only、bias-only 和 mixed GVF feature sets。
4. Horizon audit：测量 discount 如何改变 decision point 的 cue preservation，而不只看 TD error。
5. Negative controls：shuffle cue labels 或使用 bias-only features，确认 probe 不会意外报告 usefulness。

在至少一个 usefulness metric 实现前，本 proposal 应保持为 design diagnostic。

## 局限与有效性威胁

- 当前 usefulness 是推断的，还没有直接测量。
- 还没有 hidden-cue linear probe。
- 还没有 downstream control ablation。
- Cumulant set 小且由人工设计。
- 因为 usefulness metrics 仍是 planned，当前图可能过度强调 TD error。

## Reviewer Critique / 审稿批评

| 审查角度 | 可能批评 | 报告回应 | 必要下一步 |
|---|---|---|---|
| Useful prediction | Accuracy 与 usefulness 被混淆。 | 报告明确写出 prediction error != usefulness。 | 加入 cue-decodability 和 control-usefulness metrics。 |
| GVF reviewer | Question set 是人工设计且很小。 | Study 被定位为 diagnostic，不是 automatic question discovery。 | 加入 ablations 和 principled question-selection table。 |
| Control reviewer | 还没有 downstream decision test。 | 证据等级只是 redesign guidance。 | 为每个 GVF feature set 运行 junction-action ablations。 |
| Strict instructor | 没有 state utility 就不要推销 GVF state。 | Claim 限定在 question-design diagnosis。 | 除非 usefulness probes 通过，否则 final conclusion 保持 diagnostic。 |

## Proposal Template Answers / 提案模板回答

Focused RL question：哪些 GVF questions 更可能成为 useful state，而不只是 easy predictions？

Setting/testbed：一个 controlled T-maze prediction stream，包含 cue、junction 和 bias signals。

Implemented comparison：在不同 cumulant 和 discount choices 下训练 linear GVF predictors。

Observation/metric：当前指标是 TD error、prediction value 和 weight norm；必要下一步指标是 cue decodability 和 downstream control ablation。

Compute need：小型 CPU-only runs。

Fallback：如果 downstream usefulness tests 来不及完成，就把本研究保持为 question-design diagnostic。

## Conclusion / 结论

本 proposal 是关于 GVF question design 的独立 mini-study。当前结果有价值，因为它避免一个常见错误：在没有测量 predictions 对 control 保留了什么信息时，就把准确 predictions 当作 useful state。本研究应保持为 redesign target，直到加入 cue decodability 和 downstream action ablations；只有那时才能声称某个 GVF question set 改善了 state construction，而不只是产生了 learnable predictions。

## Reproduction / 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/gvf_question_design/config_main.json
```
