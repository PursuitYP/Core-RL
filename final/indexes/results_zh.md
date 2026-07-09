# 当前结果索引（中文）

本文件是 `final/indexes/results.md` 的中文审阅版。最终引用仍以英文 result index 和各 report 为准；这里帮助快速理解每个结果到底说明了什么。

## 主线和综合候选

| Study | 当前结果路径 | 关键结果 | 限制和下一步 |
|---|---|---|---|
| Reward-Centered Sarsa | `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended` | 20 seeds、20000 steps、5 个 reward shifts、3 个 alpha 下，reward-centered Sarsa 的 unshifted reward 基本保持 `2.55-2.60`，Q norm 约 `22-35`；discounted Sarsa 在 shift `8`、alpha `0.1` 时 Q norm 约 `1876`，unshifted reward 约 `1.70`。 | standalone 版本仍缺 beta/gamma sweep 和中途 reward-origin switch。 |
| Output-Controlled TD | `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended` | 20 seeds、20000 steps extended sweep 覆盖 5 个 feature scales 和 4 个 alpha。按 seed-level divergence 统计，normalized TD 和 trace-normalized TD 都是 `0/400` seed-conditions 发散；fixed TD 和当前 raw-alpha true-online baseline 都有 `35.2%` seed-conditions 发散。在 scale `hundred` 下，normalized TD final RMSE 对 alpha `0.01/0.03/0.1/0.3` 约为 `0.56/0.53/0.44/0.28`，trace-normalized TD 约为 `0.56/0.54/0.49/0.40`。 | true-online TD(lambda) 结果只说明当前 raw-alpha baseline 不公平或不稳，不能泛化否定 true-online TD；下一步需要 max-stable-alpha table 和 no-reset feature-scale switch。 |
| Scale-Invariant Continuing Control | 固定条件 pilot：`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`；unit-switch extension：`experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended` | 固定条件下 normalized-centered/differential variants 最稳；no-reset unit-switch 中 fixed discounted Sarsa 在 feature/joint scale switch 后会出现巨大 Q norm 和非零 divergence，组合方法不发散，但 harsh `hundred` scale switch 后 late reward 仍可能降到约 `1.9-2.0`。 | 更诚实的结论是组合机制显著提高稳定性，但 abrupt feature-unit change 尚未完全解决。 |
| Continual Dyna Model Aging | `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended` | 20 seeds extended half-life/budget sweep 中，budget `20` 下 keep-model late stale-backup rate 为 `0.213 +/- 0.065`；recency aging 在 half-life `250` 时几乎为 `0`，half-life `4000` 时约 `0.020 +/- 0.004`。late reward 最好约 `0.0925`，出现在 recency/error gate half-life `250` 与 recency aging half-life `4000` 附近；oracle flush 约 `0.0906`，keep-model 约 `0.0828`。 | 更诚实的结论是 freshness-aware search control 稳定减少 stale backups，reward 排名依赖 budget 和 half-life；仍需 stochastic/gradual drift。 |
| Dyna Planning Budget | `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended` | 20 seeds larger-grid extended run 中，planning budget `20` 的 late reward 对 keep-model 和 flush 都约 `0.072`；但 keep-model late stale-backup rate 仍约 `0.294`，flush 为 `0`。 | 这是 model-aging 的前置诊断，不应单独夸大 reward superiority。 |
| Predictive State Plasticity | `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended` | 20 seeds、maze lengths `8/12/20/30` 下，cue-GVF trial accuracy 仍接近 chance：约 `0.504/0.508/0.505/0.494`；oracle 约 `0.931-0.950`，trace memory 在 length `30` 仍约 `0.827`。 | 这是更强的负向 gate；下一步应重设计 GVF question、feature scaling 和 control utilization。 |

## 支持性诊断和负结果

GVF Predictive State 证明当前 recurrent GVF 不能替代 trace/oracle memory；Generate-and-Test 当前 utility 不优于 random replacement；Options transfer claim 被 quarantine；TIDBD-lite 机制可见但不优于 normalized TD；Baird-style 结果作为 off-policy stability warning；Centered TD Diagnostics 支持 reward-centering 机制；On-policy Stability Atlas 支持 output-controlled update 的必要性；Nonstationary Bandit 与 Streaming Representation 只保留为 sanity/negative diagnostics。

正式引用请使用 `condition_summary.json` 中的 `*_seed_tail` 统计；如果指标是 divergence 这种 binary event，应优先使用从 `metrics.csv` 重新汇总的 seed-level event rate。旧 main pilots 多数为 seeds `0-4`、5000 online steps；带 `_extended` 的结果通常为 seeds `0-19`、20000 online steps。
