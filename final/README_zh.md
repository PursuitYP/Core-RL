# Final Materials 中文入口

这是 `final/` 目录的中文审阅入口。英文 `README.md` 保留为 canonical directory contract；本文件用于快速说明应该从哪里读、哪些材料是正式材料、哪些只是历史归档。

## 推荐阅读顺序

1. `proposal_overview_zh.md`：中文总览，快速了解所有 proposal 的动机、方法、实验、结果和当前判断。
2. `proposal_overview.md`：中文总览的英文对应版本。
3. `reports/integrated/*/report_zh.md`：三个综合型课题的中文报告。Scale-Invariant Continuing Control 与 Continual Dyna With Model Aging 是当前最强正向候选；Predictive State Plasticity 是高风险但有价值的负向 gate。
4. `reports/proposals/*/report_zh.md`：十三个普通 proposal 的中文报告。每个 proposal 都独立说明研究问题、环境、方法、实验、结果和限制。
5. `indexes/results_zh.md`：当前可引用结果和关键数字。
6. `indexes/reproduction_zh.md`：复现实验的环境、命令和结果路径说明。
7. `indexes/bilingual_coverage_zh.md`：重要文档的中英文配套覆盖情况。

## Source-of-truth 规则

当前正式 claim 以 `final/reports/**/report.md` 和 `final/indexes/results.md` 为准；中文 `_zh.md` 是审阅辅助版本，与英文材料一一对应。`archive/` 下文件只做历史审计，不作为最终主阅读路径。若 archive 与当前 report 冲突，以当前 report 和 result index 为准。

后续如果更新重要结论、结果路径、图表或推荐等级，应同步更新英文和中文版本，避免两套材料出现 drift。
