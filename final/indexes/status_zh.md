# 当前状态报告（中文）

日期：2026-07-09

这份状态报告按用户最新批评修正口径：项目不能因为每个 proposal 都有目录或初版 report 就算完成。每个 proposal 都必须作为独立研究课题，拥有自己的研究问题、环境、方法、实验设计、证据、审查回应、局限和复现路径。当前状态是经过一轮证据同步和目录整理后的中间状态，不是最终完成版。

## 当前研究结构

项目现在有两个 final-facing 层次：

1. `final/reports/proposals/` 下的 13 个 canonical proposal studies。
2. `final/reports/integrated/` 下的 4 个更大的 integrated-but-independent Core RL studies。

这些 proposal 的科学强度并不相同。Reward-Centered Sarsa、Output-Controlled TD、Scale-Invariant Continuing Control 和 Continual Dyna Model Aging 是当前最强候选。其他一些 proposal 是负结果、机制诊断、redesign target 或 quarantined topic。这些弱研究仍应独立记录，但报告不能夸大结论。

## 当前报告状态

每个正式 proposal 目录下都有 `report.md` 和 `report_zh.md`，integrated reports 也采用同样结构。第一轮结构修复已经完成：17 个英文报告和 17 个中文报告都已经显式包含 Proposal Template answers、独立范围、证据等级、实验设计依据和 reviewer-audit style 批评记录。第二轮清晰度修复已经为 `Baird Off-Policy Stability`、`GVF Predictive State`、`Generate-and-Test Trace Features`、`Nonstationary Bandit`、`Streaming Representation With Auxiliary Prediction`、`Doorway Options for Reusable Subtasks` 和 `TIDBD-Lite Plasticity` 增加前置 Evidence Summary tables，使这些报告在详细章节前就明确说明 question、testbed、comparison、seeds、metric、numerical headline 和 conclusion boundary。这不意味着每个 report 都已经 paper-perfect；弱 proposal 仍需要继续补实验，或者诚实保持 negative/quarantine 定位，而这些定位已经写进报告。

英文 `report.md` 在每次重要修改后都应同步导出为同目录下的 `report.pdf`。上一版 PDF manifest 是 `final/indexes/english_report_pdf_manifest.json`；由于本轮已经更新 Reward、Dyna 和 Useful Predictive Knowledge 报告，后续必须重新导出 PDF 并更新 manifest。

旧的 split fragments 保留在 `final/archive/proposal_fragments/<proposal>/` 用于审计，但不再是当前引用来源。如果 archived fragment 和当前 report 冲突，以当前 `final/reports/**/report.md` 为准；不过当前 report 本身仍要按照 `final/indexes/revise_plan_20260709_zh.md` 继续修订。

## 更大的独立 Proposal

当前四个 integrated proposal candidates 是：

1. Scale-Invariant Continuing Control。
2. Continual Dyna Model Aging。
3. Predictive State Plasticity。
4. Useful Predictive Knowledge。

Scale-Invariant Continuing Control 已有完整 fixed-condition extended sweep：

`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`

它还有 no-reset unit-switch extension：

`experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`

完整 fixed-condition CPU task `core-rl-scale-invariant-extended-33723554` 已在 2026-07-09 17:45 HKT 前成功，并写出标准 artifacts。它现在是可引用证据：375 个 condition groups、7500 个 seed-conditions 中，normalized Sarsa、normalized reward-centered Sarsa 和 normalized differential Sarsa 都是 `0/1500` divergent seed-conditions，而 discounted Sarsa 与 reward-centered Sarsa 都是 `500/1500`。

最近一轮 reviewer-style critique 后新增了三个 second-round extended sweeps：

- Reward-centered beta/gamma/no-reset switch：extended result `experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended` 已经有标准 artifacts，现在是 evidence。它包含 10 seeds、20000 steps、`8,112,150` 行 metrics 和 `1,575` 个 condition groups。所有 conditions 都没有记录 divergence；reward-centered 和 differential variants 在 no-reset reward-origin switches 下保持较高表现，而 discounted Sarsa 可能携带非常大的 Q norm。新增 recovery analysis 已写入 `final/reports/proposals/reward_centered_sarsa/sensitivity_figures/reward_recovery_compact_best_by_family.csv`，总结 switch 后前 `1000` 个 logged steps 的 early recovery score，并已纳入报告。
- Output-controlled true-online fairness audit：smoke result 是 `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T084151Z_smoke`；rerun CPU task `core-rl-output-fairness-extended-rerun-29576456` 已在 2026-07-09 17:41 HKT 前成功；extended result `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended` 已有标准 artifacts，现在是 evidence。Seed-level divergence 为：normalized TD 与 trace-normalized TD(lambda) 都是 `0/300`，fixed TD 与 raw-alpha true-online TD(lambda) 都是 `81/300`，naive normalized true-online TD(lambda) 是 `34/300`，且这些 normalized true-online failures 集中在 lognormal feature scaling。新增 max-stable-alpha frontier 已写入 `final/reports/proposals/output_controlled_td/stability_frontier/`。
- Dyna model-aging drift sweep：extended result `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended` 已经有标准 artifacts，现在是 evidence。它配置 10 seeds、20000 steps，写出 `1,800,900` 行 metrics 和 `690` 个 condition groups。它支持 abrupt/gradual drift 下的 model-aging tradeoff，但不支持 stochastic drift 下的普遍优势。新增 reward/staleness frontier analysis 已写入 `final/reports/integrated/continual_dyna_model_aging/drift_figures/dyna_drift_reward_stale_frontier.csv`。

这三个 sweep 的第一次提交立即失败，原因是命令使用了宿主机专用 Python 路径 `/data/yupeng/conda_envs/core-rl/bin/python`，该路径在 rjob 容器内不存在。失败 job IDs `21581151`、`20998802`、`18940577` 只作为 audit 记录，不能混入当前 evidence。它们已经改用容器内 `python` 重新提交；以上 rerun tasks 才是当前有效任务。

Continual Dyna Model Aging 已有 extended half-life/budget sweep：

`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`

Predictive State Plasticity 已有 extended first-gate negative run：

`experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`

它还新增了 cue-decodability analysis：

- `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/cue_decodability_summary.csv`
- `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended/figures/report_cue_decodability_by_length.png`

Useful Predictive Knowledge 已完成第一轮和第三轮 integrated gate result：

`experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main`

`experiments/alberta_core_rl/results/useful_predictive_knowledge_budget/20260709T132025Z_main`

第一轮 run 检验 learned predictions 是否能在 T-maze cue 环境中通过 decodability 和 control-usefulness gates。Budget run 进一步检验 cue-GVF features 是否能在 two-feature state budget 中被保留。Trace 和 oracle controls 能解决任务，raw observation 接近 chance，cue-GVF features 可以被选中并被解码，但 learned predictive features 仍没有通过 control-usefulness gate。因此它是一个有原则的 negative-to-redesign integrated topic，不是已经解决的 representation 方法。

## 当前结果索引

正式结果索引：

`final/indexes/results.md`

当前重要结果目录：

- Reward-Centered Sarsa：`experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended`
- Output-Controlled TD：`experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`
- Dyna Planning Budget：`experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended`
- GVF Predictive State：`experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`
- Generate-and-Test：`experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`
- TIDBD：`experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`
- Options：`experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`
- Baird：`experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`
- Scale-Invariant Continuing Control：fixed-condition evidence 是 `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`；no-reset unit-switch evidence 是 `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`
- Unit-Switching Continuing Control：`experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`
- Continual Dyna Model Aging：`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`
- Continual Dyna Model Aging Drift：`experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`
- Predictive State Plasticity：`experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`
- Useful Predictive Knowledge：Gate-1/Gate-2 `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main`；Gate-3 budget `experiments/alberta_core_rl/results/useful_predictive_knowledge_budget/20260709T132025Z_main`
- Reward-Centered Sensitivity extended evidence：`experiments/alberta_core_rl/results/reward_centered_sarsa_sensitivity/20260709T085747Z_extended`
- Output TD Fairness smoke：`experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T084151Z_smoke`
- Output TD Fairness extended evidence：`experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended`

## 证据质量概览

强正向候选：

- Reward-Centered Sarsa。
- Output-Controlled TD。
- Scale-Invariant Continuing Control。
- Continual Dyna Model Aging。

有潜力但需扩展：

- Dyna Planning Budget。
- Predictive State Plasticity，目前是 negative first-gate result，需要 redesign。
- Useful Predictive Knowledge，目前是已有 feature-budget evidence 的 principled negative/control-usefulness gate，仍需要 oracle-prediction scaling、prediction-to-policy coupling 和 plasticity extension。

重要负结果、诊断或 quarantine 研究：

- GVF Predictive State。
- Generate-and-Test Features。
- Doorway Options。
- TIDBD-Lite Plasticity。
- Baird Off-policy Stability。
- Centered TD Diagnostics。
- On-policy Stability Atlas。
- GVF Question Design。
- Nonstationary Bandit。
- Streaming Representation。

## 代码与复现状态

代码仍保持模块化：

- `experiments/alberta_core_rl/proposals.py` 是 proposal registry/runner。
- 各 proposal 实现在 `experiments/alberta_core_rl/studies/`。
- 配置在 `experiments/alberta_core_rl/configs/`。
- 结果目录应包含 `metrics.csv`、`summary.json`、`condition_summary.json`、`config_used.json` 和 `manifest.json`。

运行环境：

- 本地 Python executable：`/data/yupeng/conda_envs/core-rl/bin/python`
- CPU-task 容器命令：使用 `python`，不要使用 `/data/yupeng/conda_envs/core-rl/bin/python`，因为 rjob 容器只挂载项目存储路径。
- 使用 `PYTHONNOUSERSITE=1`
- 使用 `MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig`

最近验证需要保守表述：

- 此前 final-facing 报告的 Markdown 图片链接检查通过。
- 此前 `python -m compileall experiments/alberta_core_rl` 无代码错误。
- `experiments/alberta_core_rl/` 下仍有两个 `__pycache__` 目录，因为它们由 `nobody:nogroup` 拥有，普通用户清理时遇到 permission denied。
- Python 源文件仍满足每个文件低于 500 行的维护建议。

## 下一轮研究迭代

1. 使用已完成的 Scale-Invariant extended sweep 作为当前证据，同时在下一轮补 gradual drift、recovery analysis 和 policy-distance probes。
2. 继续深化刚补上的 Proposal Template、证据等级和 reviewer-audit sections，尤其是会影响项目取舍的部分。
3. 使用已完成的 reward-sensitivity 和 Dyna-drift artifacts 作为当前证据；重新导出 PDF，并保持 reports、overview、reproduction notes 的结果摘要一致。
4. Dyna aging 在当前 drift runner 和 reward/staleness frontier 之外继续补 repeated changes 和 true per-backup planning-utility logging。
5. Useful Predictive Knowledge 在已完成 feature-budget gate 之后，继续补 oracle-prediction scaling、GVF-output normalization、prediction-to-policy coupling，然后再进入 plasticity/phase-switch stage。
6. Options proposal 先补 fixed-goal sanity experiments。
7. TIDBD/plasticity proposal 补 canonical TIDBD 或 AutoStep。
8. 负结果 proposal 继续独立且诚实记录，不能包装成强证据。
