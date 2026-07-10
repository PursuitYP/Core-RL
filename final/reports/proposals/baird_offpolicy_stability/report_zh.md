# Baird Off-Policy Stability

状态：独立的 off-policy stability warning。当前证据是 Baird-style pilot diagnostic，不是宽泛理论 claim，也不是 control-performance result。

## 摘要

本研究考察持续预测型 agent 中一个窄但重要的失败模式：在线性函数逼近下，off-policy bootstrapped value learning 可能变得不稳定。Testbed 是 Baird-style seven-state prediction problem，包含 zero reward、behavior-target policy mismatch 和 online TD updates。这直接关联 GVF/Horde-style background prediction，因为 agent 可能在按一个 behavior policy 行动时，从 ordinary experience 中学习许多其他 policy 下的 predictions。

当前 pilot 在三个 step size 上比较 semi-gradient off-policy TD 和 TDC-style correction。Semi-gradient TD 出现严重 weight-norm growth。TDC-style learner 在较小 step size 下保持稳定，但在最大测试 step size 下也失败。因此本文贡献是一个受限 warning：off-policy predictions 在被当作 agent knowledge 之前，需要显式 stability checks。

## Evidence Summary / 证据摘要

本报告应被阅读为 stability diagnostic，而不是 performance proposal。整个实验被设计成 true value 为零；因此 weights 或 value estimates 增长是 update instability 的直接证据，而不是 reward maximization 失败。当前证据规模小，但问题明确：一个 continual agent 可能用来学习 background knowledge 的 off-policy prediction machinery，即使只使用 linear features 且没有 neural network，也可能失败。

| 项目 | 当前证据 |
|---|---|
| RL question | Baird-style counterexample 对从 ordinary experience 中学习的 off-policy linear value prediction 提供什么 stability warning？ |
| Testbed | Seven-state Baird-style off-policy prediction，包含 zero reward、behavior-target mismatch、linear features 和 online bootstrapping。 |
| Compared learners | Semi-gradient off-policy TD 与 TDC-style correction，alpha 为 `0.005`、`0.01` 和 `0.02`。 |
| Seeds and horizon | 五个 seeds，每个 condition `5000` online steps。 |
| Primary metric | Seed-tail weight norm；divergence flag 和 TD error 是辅助诊断。 |
| Headline result | Semi-gradient TD 的 weight norm 从 alpha `0.005` 下的 `1.12e4 +/- 2.18e3` 增长到 alpha `0.02` 下的 `3.57e7 +/- 3.62e6`；TDC-style correction 在 alpha `0.005/0.01` 时接近 `8.79`，但在 alpha `0.02` 时也失败，weight norm 为 `2.07e7 +/- 6.91e6`。 |
| Conclusion boundary | 可作为 off-policy stability warning；还不是 canonical Baird replication，不是 control result，也不是 TDC-style correction 解决所有 off-policy prediction 的证据。 |

## Claim 边界

本文只提出一个受限 claim：在当前 Baird-style implementation 中，普通 semi-gradient off-policy TD 出现严重 weight growth；TDC-style correction 扩大但没有消除 stable step-size region。

本文不声称每个 off-policy GVF 都会 diverge，不声称 TDC 足以解决所有 off-policy prediction，不声称当前实现已经是 canonical Baird replication，也不声称这个 diagnostic 测量了 control performance。

## 1. Proposal Template Answers / 提案模板回答

Focused RL question：Baird-style counterexample 对从 ordinary experience 中学习的 off-policy linear value prediction 提供什么 stability warning？

Setting/testbed：一个 seven-state Baird-style off-policy prediction task，使用 linear features、zero rewards、behavior-target mismatch、bootstrapped value targets 和 online updates。

Implemented comparison：Semi-gradient off-policy TD 与 TDC-style correction，alpha 取 `0.005`、`0.01` 和 `0.02`。

Observation or metric：Weight norm over time 是主要诊断；TD error、importance ratio 和 divergence flags 作为辅助信号。

Expected behavior：Semi-gradient off-policy TD 应在该 setting 中出现 weight-norm growth。Corrected method 应在某些 step-size 范围内减少失败，但 pilot 不假设它对所有 alpha 都稳定。

Compute need：小型 CPU-only runs，五个 seeds，5000 online steps。

Fallback：如果 canonical Baird verification 或额外 correction baselines 没有完成，结果应保持为 bounded stability warning，而不是一般定理或 GVF solution。

## 2. Research Motivation / Question / Method / 研究动机、问题与方法

Alberta Plan 强调 value functions、GVFs、learned models 和 ordinary experience 是长期 agent 的核心组成。在这样的 agent 中，许多有用 predictions 天然是 off-policy：agent 遵循一个 behavior policy，却询问另一个 policy、option 或 continuation condition 下会发生什么。从同一条 stream 中学习许多 predictions 很有吸引力，但它也暴露 deadly triad：bootstrapping、function approximation 和 off-policy sampling。

研究问题是：Baird-style counterexample 对 linear function approximation 下的 off-policy value prediction 提供什么 stability warning？假设是 semi-gradient off-policy TD 会出现 weight-norm growth，而 gradient-corrected method 会在有限 step-size 范围内减少这种失败。

方法保持小型和在线。环境 rewards 全为零，因此 true value function 应为零。Value estimates 或 weights 增长就是直接 instability signal，而不是 reward optimization 的结果。Learners 是 semi-gradient off-policy TD 和 TDC-style correction，二者都不使用 replay buffer 或 offline fitting。

## 3. Experimental Design / 实验设计

Main run：

- Seeds：`0-4`。
- Steps：`5000`。
- Config 中的 environment label：`baird_star_diagnostic`。
- Result path：`experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`。
- Primary metrics：`weight_norm`、`diverged` 和 `td_error`。

主图：

![Baird-style weight norm by algorithm and alpha.](../../../../experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main/figures/weight_norm_by_algorithm-alpha_curve.png)

设计逻辑：

| 设计元素 | 原因 |
|---|---|
| Zero-reward prediction | 让 value growth 成为直接 warning sign，而不是 reward artifact。 |
| Linear features | 保持在经典 core RL 内，避免 neural-network confounds。 |
| Behavior-target mismatch | 产生该 diagnostic 需要的 off-policy pressure。 |
| Alpha sweep | 区分 correction-method behavior 与 step-size sensitivity。 |
| Weight norm | 捕捉 zero-reward prediction task 中 return 无法显示的不稳定性。 |

## 4. Results / 结果

Pilot 显示 semi-gradient off-policy TD 出现预期的不稳定性。Seed-tail mean weight norm 在 alpha `0.005` 时约为 `1.12e4`，alpha `0.01` 时约为 `1.73e6`，alpha `0.02` 时约为 `3.57e7`。

TDC-style learner 在两个较小 alpha 下稳定得多：alpha `0.005` 和 `0.01` 时的 seed-tail mean weight norm 都约为 `8.79`。但在 alpha `0.02` 时，TDC-style learner 也失败，seed-tail mean weight norm 约为 `2.07e7`，并出现非零 divergence signal。

核心经验结果并不是 correction method 解决了问题。结果是：普通 off-policy TD 在这个 diagnostic 中不安全；correction-style update 改善但没有消除 practical step-size sensitivity。

## 5. Analysis / 分析

失败机制不是 reward optimization 差，因为所有 rewards 都为零，target value 也是零。不稳定性来自 bootstrapped targets、behavior distribution 中的 samples、指向不同 target policy 的 updates，以及可能放大 errors 的 feature representation projected update 之间的交互。

这对 GVF-style background prediction 是有用诊断。Background prediction 看起来可能无害，因为它不直接选择 actions；但不稳定 predictions 仍会污染 state features、planning inputs、option models 或 auxiliary knowledge。该结果支持一个保守工程规则：off-policy predictions 在被作为可靠 agent knowledge 使用之前，应携带 stability diagnostics。

下一步分析应是 audit，而不是扩大到更大的环境。最直接的增强包括 canonical Baird verification、expected-update 或 MSPBE-style diagnostics、更细的 alpha 和 secondary-step-size map，以及与 GTD2 和 emphatic TD variants 比较。

## 6. 局限与有效性威胁

- 当前 setup 是 Baird-style，仍需 canonical verification 才能提出更宽 claim。
- 目前只代表了一类 correction family。
- 5000-step run 可能遗漏慢发散或延迟稳定。
- Weight norm 是必要但不充分的指标；MSPBE-style 或 expected-update diagnostics 会增强结果。
- 该任务是 diagnostic counterexample，不是自然 control environment。

## 7. Reviewer Critique / 审稿批评

| Reviewer critique | 当前回应 | 必要下一步 |
|---|---|---|
| Canonical Baird details 可能改变结果。 | Claim 被标为 Baird-style pilot evidence。 | 核对 features、policies、transition probabilities、importance ratios 和 expected-update behavior。 |
| Counterexample 只是 warning，不是 GVF solution。 | 报告把结果限定为 off-policy stability warning。 | 只有在 canonical audit 后才加入小型 GVF-style background prediction stream。 |
| TDC 在 high alpha 失败使故事复杂。 | 把该失败报告为防止过度 claim 的证据。 | 映射 alpha 和 correction parameters 下的 stable region。 |
| 一个 diagnostic 不应变成宽泛 deadly-triad theorem。 | 结论保持受限且 empirical。 | 除非更强 theory checks 通过，否则 final claim 保持 diagnostic。 |

## 8. Conclusion / 结论

这个 proposal 是独立的 off-policy stability study。当前 pilot 中，semi-gradient off-policy TD 在 Baird-style zero-reward prediction task 上出现严重 weight growth；TDC-style correction 只在部分测试 step-size 范围内稳定。诚实结论是 warning 而不是 solution：off-policy value predictions 对 continual agents 可能有用，但在被信任前需要显式 stability checks。

## 9. Reproduction / 复现

从仓库根目录运行：

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/baird_offpolicy_stability/config_main.json
```

预期 result directory：`experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`。
