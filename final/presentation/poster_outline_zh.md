# 海报大纲（中文）

## 标题

Small Streaming RL Studies Through the Alberta Plan Lens

## 开场问题

当 agent 必须从单一经验流中持续学习，并且不能使用 replay buffer 或 deep network 时，简单的 online RL 机制会表现出哪些稳定性、适应性和表示学习问题？

## 主面板

1. Alberta Plan framing：ordinary experience、temporal uniformity、value functions、representation、planning、options。
2. Reward-centered continuing control：reward origin 不应改变 continuing control 的实质问题；展示 unshifted reward 和 Q norm 随 reward shifts 的变化。
3. Output-controlled streaming prediction：step size 应控制 parameter change 还是 prediction change；展示 feature scale 改变下的 RMSE/divergence。
4. Predictive state and feature utility：T-maze 中 GVF state 的负向 gate，以及 generate-and-test/TIDBD 对 useful features 的启发。
5. Reusable structure and planning：doorway options 的审慎结论，以及 Dyna planning budget/model aging 的 stale-backup 结果。
6. Reproducibility：exact commands、seed list、result paths、no replay、no deep networks。

## Takeaway

小型 online 实验能直接暴露 Alberta Plan 关心的机制问题：reward baseline、output-scale update、predictive state、feature utility、temporal abstraction 和 planning budget 在进入大规模工程之前就已经很关键。

