# Baird Off-Policy Stability 中文报告

状态：独立支持性诊断；在做更宽泛理论或 GVF claim 前，需要 canonical Baird verification。

## 摘要

本 proposal 研究 bootstrapping、function approximation 与 behavior-target policy mismatch 共同导致的经典 off-policy instability。Baird counterexample 是 deadly triad 的最小诊断环境。当前 pilot 比较 semi-gradient off-policy TD 与 TDC-style correction，并扫描 step size。结果显示 off-policy TD 的 weight norm 快速增长；TDC 在较小 alpha 下稳定，但在较大 alpha 下也失败。这个研究最适合作为 GVF/Horde-style background prediction 的 warning：off-policy predictions 在被当作 agent knowledge 之前，必须做稳定性检查。

## 研究动机

Alberta Plan 把 value functions 和 GVFs 放在 agent knowledge 的中心。一个持续 agent 可能同时学习许多 predictions，其中很多自然是 off-policy：agent 由当前 behavior policy 产生 experience，但预测问题可能对应另一个 target policy、option 或 continuation condition。Deadly triad 说明这类学习不是自动安全的。

本 proposal 不关心 benchmark return，而关心一个小型 value-function learner 在 off-policy sampling 下是否数值稳定、理论上可解释。它为后续 GVF/off-policy proposal 设置底线：不能只看 prediction count 或短期 error，还要看 weight norm、divergence 和稳定区域。

## 研究问题

主问题：semi-gradient off-policy TD 在 Baird-style setting 中如何失败，TDC-style correction 在什么 alpha 范围内能稳定更新？

假设是：semi-gradient off-policy TD 会出现 weight-norm growth，而 gradient-corrected method 会扩大稳定 step-size region。当前 pilot 支持这个定性假设，但还不是完整 canonical study。

## Alberta Plan 关联

这个 proposal 支持 GVFs、predictive knowledge、ordinary experience 下的 off-policy learning、stable value-function learning 和 background prediction safety。它是诊断型 proposal，贡献是 stability map，而不是 control policy。

## 环境与方法

环境是 Baird-style seven-state counterexample，具有 linear features、zero rewards、behavior/target mismatch 和 bootstrapped TD targets。因为 reward 为零，divergence 不表现为 return 差异，而表现为 value/weight growth。

比较方法包括 semi-gradient off-policy TD 和 TDC-style correction。Alpha sweep 为 `0.005/0.01/0.02`。所有更新在线进行，不使用 replay 或 offline fitting。

## 实验设计

当前 main pilot 使用 seeds `0-4`，steps `5000`，结果路径是 `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`。主要指标包括 weight norm、TD error、importance ratio、divergence flag 和 alpha-specific stability behavior。

![Baird-style weight norm by algorithm and alpha.](../../../../experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main/figures/weight_norm_by_algorithm-alpha_curve.png)

## 结果

Off-policy TD 的 weight norm 快速增长：alpha `0.005` 时约 `1.12e4`，alpha `0.01` 时约 `1.73e6`，alpha `0.02` 时约 `3.57e7`。这符合 semi-gradient off-policy TD 在 Baird-style setting 中会发散的预期。

TDC 在 alpha `0.005` 和 `0.01` 下保持稳定，weight norm 约 `8.79`，但在 alpha `0.02` 下也失败。这个细节很重要：correction method 改善稳定区域，但不意味着可以任意选择 step size。

## 分析

这个结果应被解释为 stability diagnostic，而不是自然任务上的性能比较。它为 off-policy background predictions 加上警示标签：未来任何 GVF proposal 如果使用 off-policy demons，都应包含 stability-region analysis，而不是假设普通 TD 更新安全。

TDC 结果也防止过度宣传。Correction 改变了 update geometry，但 practical stability 仍依赖 alpha、variance 和 feature/policy details。

## 有效性威胁

当前 setup 需要继续与 canonical Baird specification 核对；feature 或 policy 的小偏差可能改变期望行为。只实现了一类 correction，完整 stability paper 应加入 GTD2、ETD、emphatic variants。当前任务是 diagnostic counterexample，不是自然控制环境。Run length 也可能不足以区分慢发散和收敛。

## 审稿式批评与回应

Theory reviewer 会说：Baird 的 canonical details 很重要。回应是：报告把当前结果称为 Baird-style，并要求补 expected-update comparison 和 canonical-spec verification。

GVF reviewer 会说：这不能只停留在教材例子。回应是：报告明确把该诊断连接到 off-policy background predictions；若升级，应加入一个 behavior-drift GVF stream。

## 结论

Baird Off-Policy Stability 是强支持性诊断。它展示了为什么 continual predictive agent 不能随意使用 off-policy TD。若要升级成主线研究，需要 canonical verification、更多 correction baselines 和 GVF-style behavior-drift extension。

## 复现

```bash
cd /mnt/shared-storage-user/yupeng/Core-RL

PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/baird_offpolicy_stability/config_main.json
```
