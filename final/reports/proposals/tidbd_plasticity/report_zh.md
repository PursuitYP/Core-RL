# TIDBD-Lite Plasticity 中文报告

状态：独立 mechanism diagnostic；当前证据不是正向性能 proposal。

## 摘要

本 proposal 研究 per-feature step-size adaptation 是否可以作为 streaming TD prediction 中的 plasticity mechanism。环境是一个 nonstationary sensor stream，相关 feature group 会在 phase switch 后改变。理想情况下，TIDBD-style learner 应提高 newly relevant features 的 step sizes，保持 distractor step sizes 较低，并在变化后恢复 prediction accuracy。

当前 pilot 只支持这个故事中的机制部分。TIDBD-lite 在 switch 后展示了可解释的 feature-wise alpha dynamics，但 normalized TD 的 late prediction error 略低。因此本 proposal 是 mechanism diagnostic，不是 performance victory。它的价值在于区分“learner 以合理方式改变 internal learning rates”和“learner 改善 prediction objective”。

## Evidence Summary / 证据摘要

本报告是 adaptive step sizes 的机制研究。它不声称简化的 TIDBD-lite learner 已经是更好的 predictor，而是分开考察 continual-learning 讨论中经常混在一起的两个问题：learner 是否以合理方向移动 feature-wise step sizes，以及这种移动是否改善 downstream TD prediction objective。当前证据对第一个问题是部分肯定，对第二个问题是否定。

| 项目 | 当前证据 |
|---|---|
| RL question | Per-feature step-size adaptation 能否在 online TD prediction 中追踪 changing feature relevance？ |
| Testbed | Nonstationary sensor prediction stream，包含 old-relevant、new-relevant 和 distractor feature groups；stream 中点发生 relevance switch。 |
| Compared learners | Fixed-alpha TD（`0.01`、`0.03`、`0.1`）、normalized TD 和简化 TIDBD-lite。 |
| Seeds and horizon | 五个 seeds，每个 learner `5000` online steps。 |
| Primary metric | Post-change absolute TD error；group-wise alpha trajectories 是机制诊断。 |
| Headline result | TIDBD-lite 把 new-feature alpha 从 switch 前约 `0.0068` 提高到 switch 后 late window 约 `0.0093`，同时 distractor alpha 接近 `0.0068`；但 normalized TD 的 late post-change absolute TD error（`0.4419 +/- 0.0085`）低于 TIDBD-lite（`0.4493 +/- 0.0119`）。 |
| Conclusion boundary | 证据支持可见 adaptive-step-size dynamics，但不支持 performance advantage。更强 claim 需要 canonical TIDBD/AutoStep、repeated switches、recovery AUC 和 alpha-utility correlation。 |

## Claim 边界

本报告只提出一个受限 claim：

> 在当前 nonstationary stream 中，TIDBD-lite 显示出可见 per-feature step-size adaptation，但这种 adaptation 尚未带来相对 normalized TD 的 prediction-error advantage。

本报告刻意不声称：

- TIDBD-lite 是 canonical TIDBD reproduction；
- per-feature adaptation 已经提升 performance；
- alpha movement alone 证明 useful plasticity；
- alpha dynamics alone 足以支持任何更广泛的 plasticity conclusion。

## Research Motivation/Question/Method / 研究动机/问题/方法

Continual agents 在 feature relevance 会变化的 streams 中运行。固定 global step size 是一种折中：太大会让 irrelevant 或 noisy features 破坏 learning，太小又会让 newly relevant features 适应太慢。Per-feature step-size adaptation 提供局部 plasticity mechanism：每个 feature 可以根据它最近对 prediction updates 的贡献调整自己的 learning rate。

Alberta Plan 把 step-size adaptation 和 feature utility 看作长期 agent 的早期 building blocks。本 proposal 问的是：在宣称任何大型 control benefit 前，一个轻量 adaptive TD learner 能否仅从 stream 中检测 relevance change。

### Focused RL Question / 聚焦 RL 问题

主问题：

> Per-feature step-size adaptation 能否在 online TD prediction 中追踪 changing feature relevance？

子问题：

- Newly relevant features 的 step sizes 是否在 switch 后上升？
- Distractor features 是否保持相对安静？
- 该机制是否相对 fixed 和 normalized TD baselines 改善 recovery speed 或 late prediction error？

假设：

> Relevance switch 后，TIDBD-style learner 应提高 newly relevant features 的 step sizes，保持 distractors 的 step sizes 较低，并比 fixed-alpha TD 更快恢复 prediction accuracy。

当前结果支持前两个机制性 claim，但不支持更强 performance claim。

### Core RL Connection / 与 Core RL 的关联

这是 core RL proposal，因为它研究 online TD prediction、step-size adaptation 和 linear function approximation 下的 feature utility。它连接：

- meta-learning of step sizes；
- stream 中的 online prediction；
- nonstationarity 下的 continual adaptation；
- feature relevance tracking；
- 无 replay 的 limited computation。

该 proposal 刻意不是 deep plasticity benchmark。它是一个用于检查 feature-wise learning-rate dynamics 的小型工具。

### Related Work / 相关工作

TIDBD 把 incremental delta-bar-delta ideas 扩展到具有 feature-wise step sizes 的 TD learning。Alberta Plan 讨论 per-weight step-size adaptation，把它作为早期 continual-learning machinery 的一部分。更广泛的 plasticity work 关注 nonstationarity 后的 recovery，但其中许多工作使用 deep networks 或 replay settings，超出本项目偏好的范围。

本地参考：

- `resources/alberta_plan_related/tidbd_1804.03334.pdf`
- `resources/alberta_plan_related/alberta_plan_2208.11173.pdf`

### Method / 环境与方法

环境是 nonstationary sensor prediction stream：

- 一个 feature group 在 switch 前 relevant；
- 另一个 feature group 在 switch 后变为 relevant；
- distractor features 始终基本无关；
- updates 在线进行，不使用 replay buffer 或 offline refitting。

这是机制环境。它故意制造可直接测量的 feature-relevance changes。

比较方法：

- fixed TD with alphas `0.01`、`0.03` 和 `0.1`；
- normalized TD；
- TIDBD-lite。

本地 adaptive method 被有意称为 TIDBD-lite。它使用简化的 per-feature meta-gradient-like update；在完整算法实现和核对之前，不应把它写成 canonical TIDBD。

## Experimental Design / 实验设计

当前 main pilot：

- Seeds：`0-4`。
- Steps：`5000`。
- Switch：发生在 stream 中点。
- Result path：`experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`。

主要测量：

- absolute TD error；
- old-relevant feature step sizes；
- new-relevant feature step sizes；
- distractor step sizes；
- post-switch recovery windows。

主图：

![Absolute TD error for TIDBD-lite and TD baselines.](../../../../experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main/figures/abs_td_error_by_algorithm_curve.png)

设计逻辑：

| 设计元素 | 为什么需要 |
|---|---|
| Feature relevance switch | 制造已知 plasticity challenge。 |
| Group-wise alpha logs | 测试 adaptation 是否朝 newly relevant features 移动。 |
| Distractor group | 检测 indiscriminate alpha growth。 |
| Normalized TD baseline | 测试更简单的 update scaling 是否已解释收益。 |
| Recovery windows | 区分 immediate adaptation 和 late steady-state error。 |

## Results / 结果

TIDBD-lite 展示了预期的 feature-wise mechanism：

- New-feature step size 从 switch 前约 `0.0068` 上升到 late post-change window 的约 `0.0093`。
- Distractor step size 保持在约 `0.0068`。

但 normalized TD 仍是更强 prediction-error baseline：

- normalized TD 的 late post-change absolute TD error 约为 `0.4419`；
- TIDBD-lite 的 late post-change absolute TD error 约为 `0.4493`。

这说明 internal mechanism 可见，但 external prediction objective 尚未改善到足以支持 performance claim。

Late post-change error comparison 如下：

| Strategy | Late post-change absolute TD error |
|---|---:|
| Normalized TD | `0.4419` |
| TIDBD-lite | `0.4493` |
| Fixed TD, alpha `0.01` | `0.4881` |
| Fixed TD, alpha `0.03` | `0.6279` |
| Fixed TD, alpha `0.1` | `0.6591` |

## Analysis / 分析

当前结果暗示几种可能失败机制：

- Meta-update lag：alpha 确实变化，但在单次 switch 后不够快，无法改善 recovery。
- Scale competition：normalized TD 可能已经解决了 TIDBD-lite 想解决的大部分 update-magnitude problem。
- Weak utility signal：简化 meta-gradient 可能无法足够强地区分 useful features 和 correlated distractors。
- One-switch environment：单次变化可能太有限，不足以暴露累积 plasticity benefits。
- Algorithm gap：TIDBD-lite 可能缺少 canonical TIDBD 或 AutoStep 的重要细节。

这些机制解释了为什么本报告把 alpha dynamics 当作 mechanism behavior 的证据，而不是 better learner 的证据。

## Next Experiments / 下一步实验

下一步实验应分别测试 mechanism 和 performance：

1. Canonical algorithm check：实现 full TIDBD 或 AutoStep，并根据参考核对 update equations。
2. Repeated switches：使用多次 relevance changes，测试 per-feature adaptation 是否相对 fixed 或 normalized TD 累积优势。
3. Recovery AUC：报告每次 switch 后的 error area，而不只看 late-window mean error。
4. Alpha-utility correlation：测量 alpha 上升的 features 是否也对 prediction improvement 贡献更多。
5. Normalization ablation：比较带和不带 output/update normalization 的 per-feature adaptation。
6. Control transfer only after success：只有在 diagnostic stream 中 prediction recovery 改善后，才测试小型 control task。

## 局限与有效性威胁

- 当前 implementation 是 TIDBD-lite，不是 canonical TIDBD。
- 环境只有一次 switch。
- Normalized TD 是强 baseline，可能解释了大部分 observed adaptation need。
- 当前 metrics 还没有 feature correlation、utility contribution 或 recovery AUC。
- Mean group alpha 可能隐藏每个 group 内部的 feature-level variance。

## Reviewer Critique / 审稿批评

| 审查角度 | 可能批评 | 报告回应 | 必要下一步 |
|---|---|---|---|
| Algorithm reviewer | TIDBD-lite 不是 canonical TIDBD。 | 报告全程使用 TIDBD-lite terminology。 | 实现 canonical TIDBD 或 AutoStep。 |
| Plasticity reviewer | Alpha movement alone 不是 utility evidence。 | 报告区分 mechanism dynamics 与 prediction improvement。 | 加入 alpha-utility correlation 和 recovery AUC。 |
| Baseline reviewer | Normalized TD 在 error 上已经更好。 | 报告把这视为限制，而不是干扰项。 | 加入 normalization ablations 和 repeated switches。 |
| Strict instructor | 不要把 mechanism 写成 performance win。 | Claim 明确是 diagnostic。 | 除非 performance metrics 改善，否则 final framing 保持 mechanism study。 |

## Proposal Template Answers / 提案模板回答

Focused RL question：Per-feature step-size adaptation 能否在 streaming TD prediction 中追踪 changing feature relevance？

Setting/testbed：一个 nonstationary sensor prediction stream，包含 old-relevant group、new-relevant group 和 distractors。

Implemented comparison：TIDBD-lite 对比 fixed-alpha TD 和 normalized TD baselines。

Observation/metric：Prediction error、group-wise alpha trajectories、recovery windows，以及计划加入的 recovery AUC 和 alpha-utility correlation。

Compute need：小型 CPU-only runs。

Fallback：在 canonical TIDBD 或 AutoStep 以及更强 recovery metrics 完成前，把本报告保持为 mechanism diagnostic。

## Conclusion / 结论

本 proposal 是关于 streaming TD prediction 中 plasticity mechanism 的独立研究。当前证据支持一个窄结论：TIDBD-lite 的 feature-wise step sizes 朝可解释方向适应，但 normalized TD 的 late prediction error 仍略低。因此该项目应被报告为 diagnostic evidence 和 redesign target；任何更强的 plasticity claim 都应推迟到 canonical adaptive step-size algorithms 与 recovery-focused metrics 显示 behavioral advantage 之后。

## Reproduction / 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/tidbd_plasticity/config_main.json
```
