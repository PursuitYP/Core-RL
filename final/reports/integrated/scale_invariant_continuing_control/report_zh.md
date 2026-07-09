# Scale-Invariant Continuing Control 中文报告

英文原文：`report.md`

## 定位

综合型主线候选，当前是最强正向方向之一。

## 研究动机

持续学习 agent 不应该依赖任意的测量单位。对于 continuing control，给所有 reward 加常数不应改变平均奖励意义下的最优行为；同一组线性特征整体放大也不应改变任务本质。但普通 discounted Sarsa 会把 reward shift 累积成巨大 value offset，固定 alpha 又会被 feature scale 放大。因此本课题把 reward translation 和 feature scaling 放进同一个 access-control 控制问题中，检验 reward centering 与 output-controlled update 是否能组合成真正更稳的在线控制机制。

## 研究问题

在线 linear Sarsa agent 在同时面对 reward zero-point 改变和 feature scale 改变时，能否通过 reward-centered TD error 和 normalized update 保持 unshifted reward、policy probes、Q norm 和 prediction-change 的稳定性？

## 方法与实现

环境是 continuing access-control queue，agent 持续观察 server availability 与 customer priority，并在线选择 accept/reject。比较 discounted Sarsa、reward-centered Sarsa、normalized Sarsa、normalized reward-centered Sarsa、normalized differential Sarsa。所有方法都是线性/表格 action-value 更新，不使用 replay buffer、deep network 或离线训练。

## 实验设计

当前 main pilot 交叉 reward shifts `-4, 0, 8` 与 feature scales `one, ten, hundred, uneven`，5 个 seeds，每个条件 5000 steps。核心指标是 tail unshifted reward、Q norm、prediction change、divergence 和 policy accept probes。已准备 extended config：20 seeds、20000 steps，并在代码中对 steps>=20000 的 main run 扩展 shifts/scales/alphas。

## 当前结果

结果路径：`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`。当前结果显示单独 reward centering 在 feature scale 很大时会失败，单独 normalized Sarsa 仍受 reward shift 影响；combined normalized-centered 和 normalized-differential variants 在当前 sweep 中最稳，tail unshifted reward 大致保持在 `2.4-2.5`，且没有 divergence。报告图已改用 `report_*.png` summary figures，避免原先大量图例压缩坐标区。

## 可以声称与不能声称

可以声称：reward centering 和 output normalization 解决的是两个不同的单位敏感性问题，当前 access-control pilot 中二者组合比单独机制更稳。不能声称：已经证明所有 continuing control 或所有 function approximation setting 下都 scale invariant；也不能声称已完成中途 sensor/reward unit change 的非平稳实验。

## 下一步

下一步优先跑 extended CPU sweep，再加入同一 stream 中途改变 reward origin 或 feature scale 的无重置实验，并补 alpha/gamma 公平性表。

## 复现

主复现命令见 `final/indexes/reproduction_zh.md` 与英文 `final/indexes/reproduction.md`。
