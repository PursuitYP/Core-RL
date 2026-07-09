# 当前结果索引（中文）

本文件是 `final/indexes/results.md` 的中文审阅版。最终引用仍以英文 result index 和各 report 为准；这里帮助快速理解每个结果到底说明了什么。

## 主线和综合候选

| Study | 当前结果路径 | 关键结果 | 限制和下一步 |
|---|---|---|---|
| Reward-Centered Sarsa | `experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main` | discounted Sarsa 的 Q norm 随 reward shift 从 `60.17` 增到 `344.6`；reward-centered Sarsa 保持约 `20-22`，unshifted reward 约 `2.47-2.54`。 | 需要 extended seeds/steps、alpha/beta/gamma sweep 和中途 reward-origin switch。 |
| Output-Controlled TD | `experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main` | fixed TD 在 high feature scale 下发散；normalized TD 在 scale `hundred` 下 RMSE 约 `0.56/0.53/0.47`。 | true-online baseline 需要公平审计；需要 nonstationary feature-scale switch。 |
| Scale-Invariant Continuing Control | `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main` | normalized-centered 和 normalized-differential variants 在 reward shifts/scales 下保持 tail unshifted reward 约 `2.4-2.5` 且无 divergence。 | 当前是 5 seeds fixed-gamma pilot；需要 extended sweep 和 in-stream unit change。 |
| Continual Dyna Model Aging | `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260708T174237Z_main` | budget `20` 时 keep-model late stale-backup rate 约 `0.336`，recency aging 降至约 `0.0064`。 | 需要 extended half-life sweep 和 stochastic/gradual drift 环境。 |
| Predictive State Plasticity | `experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main` | trace/oracle memory trial accuracy 约 `0.93-0.96`；cue-GVF 仍接近 chance `0.47-0.49`。 | 当前是负向 gate；需要 cue decoding、oracle-prediction control 和 ablation。 |

## 支持性诊断和负结果

GVF Predictive State 证明当前 recurrent GVF 不能替代 trace/oracle memory；Generate-and-Test 当前 utility 不优于 random replacement；Options transfer claim 被 quarantine；TIDBD-lite 机制可见但不优于 normalized TD；Baird-style 结果作为 off-policy stability warning；Centered TD Diagnostics 支持 reward-centering 机制；On-policy Stability Atlas 支持 output-controlled update 的必要性；Nonstationary Bandit 与 Streaming Representation 只保留为 sanity/negative diagnostics。

正式引用请使用 `condition_summary.json` 中的 `*_seed_tail` 统计。所有当前 main results 均为 seeds `0-4`、5000 online steps，除非后续 extended run 更新本索引。
