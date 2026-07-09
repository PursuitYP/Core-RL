# 当前状态报告（中文）

日期：2026-07-09

这份状态报告按用户最新批评修正口径：项目不能因为每个 proposal 都有目录或初版 report 就算完成。每个 proposal 都必须作为独立研究课题，拥有自己的研究问题、环境、方法、实验设计、证据、审查回应、局限和复现路径。当前状态是经过一轮证据同步和目录整理后的中间状态，不是最终完成版。

## 当前研究结构

项目现在有两个 final-facing 层次：

1. `final/reports/proposals/` 下的 13 个 canonical proposal studies。
2. `final/reports/integrated/` 下的 3 个更大的 integrated-but-independent Core RL studies。

这些 proposal 的科学强度并不相同。Reward-Centered Sarsa、Output-Controlled TD、Scale-Invariant Continuing Control 和 Continual Dyna Model Aging 是当前最强候选。其他一些 proposal 是负结果、机制诊断、redesign target 或 quarantined topic。这些弱研究仍应独立记录，但报告不能夸大结论。

## 当前报告状态

每个正式 proposal 目录下都有 `report.md` 和 `report_zh.md`，integrated reports 也采用同样结构。第一轮结构修复已经完成：16 个英文报告和 16 个中文报告都已经显式包含 Proposal Template answers、独立范围、证据等级、实验设计依据和 reviewer-audit style 批评记录。这不意味着每个 report 都已经 paper-perfect；弱 proposal 仍需要继续补实验，或者诚实保持 negative/quarantine 定位，而这些定位已经写进报告。

旧的 split fragments 保留在 `final/archive/proposal_fragments/<proposal>/` 用于审计，但不再是当前引用来源。如果 archived fragment 和当前 report 冲突，以当前 `final/reports/**/report.md` 为准；不过当前 report 本身仍要按照 `final/indexes/revise_plan_20260709_zh.md` 继续修订。

## 三个更大的独立 Proposal

当前三个 integrated proposal candidates 是：

1. Scale-Invariant Continuing Control。
2. Continual Dyna Model Aging。
3. Predictive State Plasticity。

Scale-Invariant Continuing Control 已有 main pilot：

`experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`

它还有 no-reset unit-switch extension：

`experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`

完整 fixed-condition extended sweep 已提交为 CPU task `core-rl-scale-invariant-extended-33723554`，namespace 是 `ailab-safethm`。该任务在 2026-07-09 14:40 HKT 确认为 RUNNING，节点是 `lg-cmc-h-cpu-0058.host.h.pjlab.org.cn`。它已经创建目录 `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`，但该目录目前没有标准 artifacts，因此还不是 evidence。

Continual Dyna Model Aging 已有 extended half-life/budget sweep：

`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`

Predictive State Plasticity 已有 extended first-gate negative run：

`experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`

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
- Scale-Invariant Continuing Control：当前 evidence 是 `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260708T172151Z_main`；运行中的空目录是 `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`
- Unit-Switching Continuing Control：`experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`
- Continual Dyna Model Aging：`experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`
- Predictive State Plasticity：`experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`

## 证据质量概览

强正向候选：

- Reward-Centered Sarsa。
- Output-Controlled TD。
- Scale-Invariant Continuing Control。
- Continual Dyna Model Aging。

有潜力但需扩展：

- Dyna Planning Budget。
- Predictive State Plasticity，目前是 negative first-gate result，需要 redesign。

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

- Python executable：`/data/yupeng/conda_envs/core-rl/bin/python`
- 使用 `PYTHONNOUSERSITE=1`
- 使用 `MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig`

最近验证需要保守表述：

- 此前 final-facing 报告的 Markdown 图片链接检查通过。
- 此前 `python -m compileall experiments/alberta_core_rl` 无代码错误。
- `experiments/alberta_core_rl/` 下仍有两个 `__pycache__` 目录，因为它们由 `nobody:nogroup` 拥有，普通用户清理时遇到 permission denied。
- Python 源文件仍满足每个文件低于 500 行的维护建议。

## 下一轮研究迭代

1. 继续监控 CPU task `core-rl-scale-invariant-extended-33723554`；如果成功完成，把新的 Scale-Invariant Continuing Control extended sweep 纳入报告、图表、PDF 和索引。
2. 继续深化刚补上的 Proposal Template、证据等级和 reviewer-audit sections，尤其是会影响项目取舍的部分。
3. Dyna aging 补 gradual drift、repeated changes 和 planning-utility analysis。
4. GVF predictive-state 方向补 cue-decodability probes。
5. Options proposal 先补 fixed-goal sanity experiments。
6. TIDBD/plasticity proposal 补 canonical TIDBD 或 AutoStep。
7. 负结果 proposal 继续独立且诚实记录，不能包装成强证据。
