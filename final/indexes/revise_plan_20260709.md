# 2026-07-09 Full Revise Plan

This document preserves the current major revision plan for review and continuation. The confirmed scope is all 16 formal research objects: 13 ordinary proposals and 3 integrated proposals. Each proposal remains an independent research study. The integrated proposals are larger and more synthetic, but they do not replace the ordinary proposal reports.

## Current State

CPU task `core-rl-output-extended-fixed-46602102` has succeeded. Its output directory is `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`, with `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, and `manifest.json`. The summary records about `2505` elapsed seconds, `2672969` metrics rows, and `80` condition groups. This result must be treated as current evidence rather than as an incomplete run.

The final-facing structure is now `final/reports/proposals/` for the 13 ordinary reports and `final/reports/integrated/` for the 3 larger reports. Each formal report folder should use `report.md`, `report_zh.md`, and `report.pdf` as the main entry points. `final/archive/` is audit-only.

The next long CPU task has also been submitted: `core-rl-scale-invariant-extended-33723554` runs `scale_invariant_continuing_control/config_extended.json` on `ailab-safethm/safethm_cpu_task`. It was confirmed `RUNNING` at 2026-07-09 14:40 HKT on `lg-cmc-h-cpu-0058.host.h.pjlab.org.cn`, and logs confirm that it started `python experiments/alberta_core_rl/scripts/run_experiment.py --config experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_extended.json`. It has created `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`, but that directory currently has no standard artifacts. It is not evidence until `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, and `manifest.json` are written.

## Honest Gap Statement

The previous pass completed important infrastructure and evidence synchronization work, especially the Output-Controlled TD extended result incorporation. It did not complete the full user request to substantially restructure every proposal. Major gaps remain: many proposal reports still read like mini-reports; several weak proposals have only 5-seed pilot evidence or one diagnostic figure; Proposal Template answers are not explicit in every report; English and Chinese reports exist but are not guaranteed to be paragraph-by-paragraph consistent; multi-role critique exists mostly at the index level rather than as a per-proposal critique-revision loop; and the new larger integrated research question has not yet been turned into a full proposal/report/experiment package. The current state is therefore an improved intermediate state, not a completed final revision.

## Requirement Traceability Matrix

| Original requirement | Current reality | Gap | Required action | Acceptance criterion |
|---|---|---|---|---|
| 0. Every proposal is independent | The directory structure has 13 ordinary reports and 3 integrated reports. | Many reports still lack a full independent workflow, explicit template answers, and per-proposal critique logs. | Add `Proposal Template Answers`, `Independent Research Scope`, `Evidence Level`, `Required Next Experiments`, and `Reviewer Audit` to all 16 reports. | Any single report can be read alone to understand question, setting, methods, evidence, limits, and next steps. |
| 1. Rebuild motivations, questions, methods, experiments, results | Reward-Centered and Output-Controlled are clearer; Dyna Aging and Scale-Invariant are stronger; many others remain short. | Several proposals have weak storylines, shallow experiments, or underdeveloped failure analysis. | Review each proposal for keep/strengthen/demote/quarantine; add experiments for strong proposals; write failure mechanisms for weak proposals. | Every report has hypothesis, environment rationale, baseline rationale, metric rationale, interpretation, and threats. |
| 2. Combine into larger meaningful questions without patchwork | Three integrated proposals exist. | Integrated reports are not all paper-depth; weak representation work is not yet organized into a coherent larger topic. | Keep the three integrated proposals and add a candidate large topic: `Useful Predictive Knowledge Under Partial Observability and Resource Limits`. | The large topic has one motivation, one environment family, staged experiments, and explicit success/failure criteria. |
| 3. Go deeper into Alberta Plan/Core RL and propose a stronger large problem | Alberta Plan framing and literature lists exist. | Literature is not yet woven into each proposal's motivation and experiment design. | Tie reward centering, intentional updates, GVF/Horde, Dyna/search-control, emphatic/off-policy, options, and average-reward work to specific proposals. | Related work sections explain how each source changes the research question or experiment, not just that it exists. |
| 4. Use richer but clear figures/tables | Some reports now use heatmaps/summary figures; Output-Controlled has new figures. | Weak proposals often have only one figure; several reports need tables that match claims. | Assign 1-3 primary figures/tables to each proposal: heatmap, seed-level table, recovery plot, mechanism plot, or negative-result table. | Every figure answers a named question; no crowded spaghetti plot is used as primary evidence. |
| 5. Review from at least ten angles | `reviewer_audit` records global critiques. | There is no complete 12-role audit matrix per proposal. | Create per-proposal critique tables from Alberta Plan, Core RL, average reward, stability, GVF, planning, continual learning, statistics, reproducibility, code, writing, and strict instructor perspectives. | Each proposal records critique, action taken, and remaining risk. |
| 6. English/Chinese consistency; Proposal Template and final report consistency | All final reports have `_zh` counterparts and English PDFs. | The language pairs may not be fully content-matched; many reports lack explicit Proposal Template sections. | Update English first, then Chinese; add Proposal Template Answers to all reports. | Spot-check any five proposals: same result path, figures, conclusions, and limitations in both languages. |
| 7. Improve docs/files/directories/architecture | The final structure is cleaner than the early version. | Result directories are numerous; archive/final boundaries and status documents can still drift. | Maintain a source-of-truth contract: `results.md` for evidence, `status.md` for current state, archive as audit-only. | A reader can start at `final/README.md` and find reports, evidence, reproduction commands, and current gaps without guessing. |
| 8. Plan deeply first | Plan files exist. | The earlier plan was too high-level and lacked gap-by-gap acceptance criteria. | Upgrade this file into a gap-driven execution plan and keep an execution tracker current. | Another agent can execute the plan without inferring missing decisions. |

## Goals And Principles

The goal is not to make every proposal look equally positive. The goal is to make each proposal an independent, honest, reproducible, reviewable Core RL study. Strong proposals should be deepened with better evidence and clearer paper-style writing. Weak proposals may remain as negative results, diagnostics, supporting material, or quarantined topics, but their reports must not overclaim.

All experiments keep the project constraints: no replay buffer, no deep network, no offline training loop, CPU-scale tabular or linear methods, and online streaming interaction. Every report must state the focused RL question, explain why the environment answers that question, describe the compared methods, define the metrics, and interpret the result within the actual evidence level.

## Implementation Plan

1. Evidence and index cleanup: fix duplicated incomplete-result text in `experiments/alberta_core_rl/results/README.md`; remove stale statements that Output-Controlled TD is still running; update `results*.md`, `status*.md`, `reviewer_audit*.md`, and both proposal overviews.

2. Output-Controlled TD incorporation: generate report-ready heatmaps and seed-level divergence tables from `20260709T051934Z_extended`; update `report.md`, `report_zh.md`, and `report.pdf`; state clearly that RuntimeWarnings are evidence of divergent high-scale/high-alpha conditions, not job failure.

3. Per-proposal deep revise: keep Reward-Centered Sarsa and Output-Controlled TD as the strongest ordinary standalone proposals; keep Scale-Invariant Continuing Control and Continual Dyna Model Aging as the strongest integrated proposals; rewrite Predictive State Plasticity as a high-value negative gate; classify the remaining proposals as supporting, diagnostic, negative, or quarantined as the evidence requires.

4. Experiment expansion: add beta/gamma and reward-origin switch tests for Reward-Centered Sarsa; add true-online audit and no-reset feature-scale switch for Output-Controlled TD; run the full fixed-condition scale-invariant grid; add stochastic/gradual drift and planning-utility diagnostics for Dyna aging; add cue decodability and GVF horizon/cumulant ablations for predictive state; repair Options only after fixed-goal sanity succeeds; implement canonical TIDBD/AutoStep or demote TIDBD-lite.

5. Multi-reviewer audit: review every proposal from at least 12 angles: Alberta Plan, Core RL theory, average reward, function-approximation stability, GVF/predictive knowledge, planning/model-based RL, continual learning, nonstationarity, experimental statistics, reproducibility, code architecture, and strict course-instructor critique.

6. Documentation and architecture cleanup: keep final-facing paths simple; maintain content-matched English and Chinese versions; regenerate English report PDFs; keep code modular and avoid single-file growth.

## Independent Proposal Revision Matrix

| Proposal | Current evidence level | Main gap | Next experiment/analysis | Report rewrite requirement |
|---|---|---|---|---|
| Reward-Centered Sarsa | Strong; 20-seed extended | Missing beta/gamma sensitivity and no-reset reward-origin switch. | Run beta/gamma sweep; switch reward origin midstream; report policy probes. | Make reward-origin invariance the central question, not just higher reward. |
| Output-Controlled TD | Strong; 20-seed extended | True-online baseline is unfair; no no-reset feature-scale switch. | Max-stable-alpha audit; normalized true-online variant; scale switch without reset. | Add true-online fairness and switch-result sections. |
| GVF Predictive State | Negative/redesign | GVF question is weakly connected to downstream utility. | Cue decodability; oracle-prediction control; GVF horizon ablation. | Frame as evidence that GVFs do not automatically become useful state. |
| Generate-and-Test Features | Negative/redesign | Utility rule does not beat random replacement. | Downstream-error utility; feature-budget sweep; repeated delay switches. | Explain failure mechanism rather than presenting generate-test as positive. |
| Doorway Options | Quarantined | Primitive baseline and option accounting are insufficient. | Fixed-goal sanity; SMDP duration accounting; goal-change transfer only after sanity passes. | Keep quarantined until the sanity test succeeds. |
| TIDBD Plasticity | Mechanism diagnostic | TIDBD-lite is not canonical; error does not beat normalized TD. | Canonical TIDBD/AutoStep; meta-step sensitivity; feature relevance switch. | Separate visible alpha dynamics from actual prediction/control gain. |
| Baird Off-policy Stability | Supporting warning | Needs canonical Baird audit; lacks emphatic/GTD comparison. | Verify feature/policy details; add ETD/TDC/GTD; behavior drift. | Upgrade from counterexample reproduction to off-policy GVF stability warning. |
| Dyna Planning Budget | Strong precursor; 20-seed extended | Overlaps Dyna Aging; standalone claim is limited. | Budget by change severity; pre/post planning utility; stale-backup mechanism table. | Position as the first experiment of the model-aging line or as a constrained precursor. |
| Centered TD Diagnostics | Supporting mechanism | Environment is too small for standalone submission. | Keep small diagnostic; optionally add analytic shift table. | Treat as Reward-Centered mechanism appendix-style independent record. |
| On-policy Stability Atlas | Supporting atlas | No intervention. | Add max-stable-alpha map; align metrics with Output-Controlled TD. | Explain why normalized update is needed. |
| GVF Question Design | Supporting/redesign tool | Prediction error is measured without useful-state metrics. | Cue information, decodability, control ablation. | Center the claim "easy to predict is not the same as useful to control." |
| Nonstationary Bandit | Dropped sanity | Too shallow; no bootstrapping, state, planning, or GVF. | Do not expand as a main topic; keep only as introductory sanity. | Demote clearly. |
| Streaming Representation | Negative | Auxiliary target is not task-relevant. | Design task-relevant auxiliary target; analyze feature utility. | Merge into predictive-state program or keep as negative result. |
| Scale-Invariant Continuing Control | Strong integrated; pilot + unit-switch; extended running | Full fixed-condition grid is not complete; abrupt switch recovery remains weak. | Monitor `core-rl-scale-invariant-extended-33723554`; update heatmaps after success; design gradual unit drift. | Present one coherent reward-unit and feature-unit invariance question. |
| Continual Dyna Model Aging | Strong integrated; 20-seed extended | Abrupt deterministic change is narrow. | Stochastic/gradual drift; repeated changes; planning-utility diagnostics. | Focus on stale-backup reduction and freshness-aware search control. |
| Predictive State Plasticity | High-value negative gate; 20-seed extended | Title is broader than positive evidence. | Cue decodability; redesigned GVFs; limited feature budget; generate-test/TIDBD only after probes pass. | Rewrite as a staged negative-to-redesign research program. |

## New Larger Proposal Candidate

New candidate: `Useful Predictive Knowledge Under Partial Observability and Resource Limits`. This does not replace the 16 current reports; it is a follow-up integrated proposal candidate meant to satisfy the requirement to break out of the current fragmented frame without creating a patchwork. The focused question is: when do learned predictions become useful agent state under partial observability and limited feature/computation budgets?

Unified environment family: T-maze cue stream plus delayed-cue trace-conditioning stream. Unified object of study: whether hidden cue information can be retained until control-relevant time by GVFs, trace features, utility-selected features, or per-feature step-size adaptation. Unified metrics: cue decodability, junction action accuracy, trial reward, feature-budget usage, prediction TD error, and post-switch recovery. Staged experiments: first run oracle/trace/GVF decodability gates; then feature-selection through generate-test; finally TIDBD/AutoStep plasticity only after the probe passes. Failure is informative: if prediction error drops but decodability/control does not improve, the conclusion is that prediction accuracy is not sufficient for useful state.

## Execution Tracker

| Work item | Status | Evidence or blocker | Next action |
|---|---|---|---|
| Save this revise plan in English and Chinese | Done | `final/indexes/revise_plan_20260709.md`, `final/indexes/revise_plan_20260709_zh.md` | Keep the Original User Requirements as the final section. |
| Correct misleading requirement/status documents | Done for the first correction pass | `final/indexes/requirements_audit.md`, `final/indexes/status.md`, and Chinese counterparts now use gap-tracking language. | Keep these documents synchronized after each experiment/report update. |
| Audit missing report sections | Done for the first mechanical pass | `final/indexes/report_section_audit.md` and `_zh.md` show that most reports lack explicit Proposal Template, independent scope, evidence level, experiment-design, or reviewer-audit signals. | Use this audit as the checklist for report rewrites; repeat after edits. |
| Monitor Scale-Invariant extended CPU task | Running | `core-rl-scale-invariant-extended-33723554` is RUNNING as of 2026-07-09 14:40 HKT; `20260709T063128Z_extended` exists but has no artifacts. | Re-check job state and artifacts; incorporate only after standard files exist. |
| Clean `__pycache__` directories | Blocked by permissions | Two `__pycache__` directories under `experiments/alberta_core_rl/` are owned by `nobody:nogroup`; normal-user cleanup fails with permission denied. | Leave documented unless the user approves a privileged cleanup path. |
| Add Proposal Template Answers to all reports | First structural pass done | All 16 English reports and 16 Chinese reports now contain visible Proposal Template/independent scope/evidence/experiment-design/reviewer-audit sections. | Continue deepening content quality and keep English/Chinese claims synchronized. |
| Add per-proposal critique/action/risk tables | First concise pass done | Each formal report now has a reviewer-audit style table or matrix. | Expand only where it changes decisions; avoid generic filler. |
| Deepen strong proposal experiments | Partially done | Output-Controlled extended evidence is incorporated; Reward-Centered, Dyna, and Predictive State have extended evidence; several requested follow-up sweeps remain. | Prioritize targeted sweeps that change conclusions rather than broad blind grids. |
| New large predictive-knowledge proposal | Planned only | Candidate question and environment family are defined above; the current Predictive State Plasticity report remains a negative gate, not this full new proposal. | Build the report skeleton, gate experiments, and acceptance criteria before implementation. |

## Literature Update

- Alberta Plan for AI Research, Sutton/Bowling/Pilarski, arXiv:2208.11173, https://arxiv.org/abs/2208.11173. Main framing source for ordinary experience, temporal uniformity, continual learning, value functions, learned models, planning, GVFs, and average reward.
- Intentional Updates for Streaming Reinforcement Learning, Sharifnassab/Elsayed/De Asis/Mahmood/Sutton, arXiv:2604.19033, https://arxiv.org/abs/2604.19033. Direct support for Output-Controlled TD and Scale-Invariant Control.
- Squeezing More from the Stream: Learning Representation Online for Streaming Reinforcement Learning, arXiv:2602.09396, https://arxiv.org/abs/2602.09396. Supports representation/GVF/auxiliary-prediction revisions under the streaming constraint.
- Streaming Deep Reinforcement Learning Finally Works, Elsayed/Vasan/Mahmood, arXiv:2410.14606, https://arxiv.org/abs/2410.14606. Provides broader streaming RL context and the stream-barrier framing.
- Reward Centering, Naik/Wan/Tomar/Sutton, arXiv:2405.09999, https://arxiv.org/abs/2405.09999. Direct support for Reward-Centered Sarsa and reward-origin invariance.
- True Online Temporal-Difference Learning, arXiv:1512.04087, https://arxiv.org/abs/1512.04087, and An Empirical Evaluation of True Online TD(lambda), arXiv:1507.00353, https://arxiv.org/abs/1507.00353. Support the trace baseline and caution against over-interpreting the raw-alpha true-online result.
- Dyna-Style Planning with Linear Function Approximation and Prioritized Sweeping, arXiv:1206.3285, https://arxiv.org/abs/1206.3285. Supports Dyna Planning Budget and Continual Dyna Model Aging.
- Frequency-based Search-control in Dyna, arXiv:2002.05822, https://arxiv.org/abs/2002.05822. Supports the search-control framing for model-aging experiments.
- Almost Sure Convergence of Differential Temporal Difference Learning for Average Reward Markov Decision Processes, arXiv:2602.16629, https://arxiv.org/abs/2602.16629. Supports average-reward and differential-TD background for continuing-control reports.

These sources should be cited selectively in proposal reports only when they directly support a motivation, method choice, or limitation.

## Verification Plan

- `python -m compileall experiments/alberta_core_rl`
- `PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/smoke_test.py`
- Check that current result directories contain the standard artifacts.
- Check that all report image links exist.
- Check that every English `report.md` has a matching `report_zh.md` and same-directory `report.pdf`.
- Regenerate PDFs and confirm missing images are zero.
- Clean generated `__pycache__` directories after verification.

## Original User Requirements

最后这个 cpu job 继续等待，同时这次引入一个新的 revise 计划，请以下面这个新的需求为主进行大幅优化，同时记录上面那个 cpu task 的进度，最后要汇总到这个新的需求中。

现在深入理解初始需求和当前每个 Proposal 的内容、实现和报告，尝试大幅重构每个 Proposal：

0. 每个 Proposal 都是独立的分开的研究，不要混杂起来，也不要强行联系，每个 Proposal 独立研究全流程。
1. 优化完善重构现有每个 Proposal 的研究动机、研究问题、研究方案、实验设计、结果分析等等的内容，看看是不是有些没意义或者太 toy example，或者现在的实验和分析内容不够，考虑深度优化每个 Proposal 大补实验。
2. 组合成更大的问题，深入理解现有的材料以及拟定的 Proposal，分析是否过于零散，尝试结合初始方向和现有课题，将一个课题组合起来从而研究一个更大的更有意义的大课题，但是要继续保持其合理性，需要详细研究细节。
3. 尝试更深入理解 Alberta Plan - Core RL 研究议题，结合已有的 Proposal，深入分析，突破现有框架和课题限制，从而提出一个更综合的更大问题的 Proposal，但是要求具体研究内容不是拼凑，要求研究动机明确、研究问题合理、研究脉络清晰，实验设计紧扣研究动机和问题，设计多个重要研究问题，实验数量规模分析都多一点。
4. 实验结果的呈现效果可以多样一些，比如各种样式的图表，但是要求丰富而不是花哨，图表不要主次不分，要清晰。
5. 其他各项内容，方方面面，都再深入细致地审查，设置多个不同的角色（起码十多个角度）进行审阅，然后完善。
6. 文档的中英文版要求是完全一致的内容并且清晰专业，Proposal Template 和 final report 应该一致。
7. 完善优化所有的文档、文件、目录和整个的项目架构和结构，使其更专业更清晰更好读，可以方便后续持续优化。
8. 请先进入 plan 模式进行深入的思考、分析、设计和完善。
