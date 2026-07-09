# Off-Policy GVF Stability Under Behavior Drift 中文说明

英文原文：`report.md`

## 当前状态

这是 deferred archive note，不是当前 final-facing proposal report。这个方向仍然有学术价值，但尚未完成当前项目结构下的实现、结果目录和 seed-aware analysis，因此没有进入 `final/reports/`。

## 研究动机

Alberta Plan 中的 GVF/Horde 式预测很可能包含大量 off-policy questions：agent 当前行为来自一个 policy，但背景预测可能询问另一个 policy、option 或 continuation condition 下会发生什么。Baird counterexample 和 deadly triad 提醒我们，off-policy bootstrapping with function approximation 可能不稳定。这个 deferred idea 的价值在于把 Baird-style stability warning 升级为更贴近 GVF 背景预测的行为漂移问题。

## 可能的研究问题

当 behavior policy 与 target question 的 mismatch 随时间变化时，哪些轻量线性 TD 修正能保持 GVF prediction 稳定？需要比较 semi-gradient off-policy TD、TDC/GTD、emphatic TD、possibly centered variants，并观察 drift 中的 transient instability。

## 为什么暂缓

当前项目已经有 Baird Off-Policy Stability 作为支持性诊断，但还没有实现完整的 off-policy GVF drift 环境。因此本方向先保留为 future work，不计入三个综合 proposal。

