# GVF Question Design Proposal Template 中文版

英文模板：`proposal_template.md`

## 当前归档状态

当前正式报告在 `final/reports/proposals/gvf_question_design/report.md`，中文正式报告在 `final/reports/proposals/gvf_question_design/report_zh.md`。本模板是历史 proposal fragment 的中文审阅版，不替代正式报告。

## 想理解什么

该 proposal 的核心问题是：在 `online GVF prediction-question comparison` 中，`multiple cumulants/questions and horizons` 是否能回答一个明确 Core-RL 机制问题。它不是为了展示某方法分数更高，而是为了检查 streaming online learning 中的稳定性、适应性、预测有用性或 planning computation 质量。

## 使用什么 testbed

Testbed：online GVF prediction-question comparison。该设置遵守 no replay buffer、no deep network、online update 的约束。

## 检查什么变量

主要变量：cumulant type and gamma。主要比较：multiple cumulants/questions and horizons。

## 看什么指标

指标：abs TD error, cue relevance proxy, downstream utility gap。当前结果路径：`experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main`。当前关键结论：bias cumulant 几乎零误差，但不代表有用；cue/junction questions 更难却可能更相关。当前只支持“suggests”，下游 utility 未直接证明。

## 当前判断

诊断结果。不能声称已找到 useful GVF question；需要 cue-decodability/control ablation。

## 还缺什么

正式提交前需要补清楚 update equation、baseline fairness、seed-tail statistics、结果图和 falsifier。对于 negative/supporting proposal，应明确说明失败暴露了什么设计问题，而不是强行写成正结果。
