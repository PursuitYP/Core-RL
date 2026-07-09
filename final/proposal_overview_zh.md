# Core-RL Proposal 中文总览

本文档是当前项目的中文快速审阅入口。它不替代各个独立报告；正式细节仍以 `final/reports/**/report.md` 为准。这里的目标是让读者不用在很多文件之间跳转，也能快速知道每个 Proposal 为什么做、怎么做、跑了什么实验、现在结果说明什么、下一步应如何改进。

## 阅读路径

- 三个更大的独立 Core-RL 课题在 `final/reports/integrated/`：其中 Scale-Invariant Continuing Control 和 Continual Dyna With Model Aging 是当前最强的正向候选，Predictive State Plasticity 是有价值但高风险的负向 gate / redesign 候选。
- 十三个普通独立课题在 `final/reports/proposals/`，每个文件夹只保留一个主报告 `report.md`，旧的模板、结果摘要、批评记录和复现片段已归档到 `final/archive/`。
- 当前可引用的结果路径集中在 `final/indexes/results.md`。
- 运行和复现实验的统一说明在 `final/indexes/reproduction.md`。

## 总体研究约束

本项目严格限定在 Core RL 范围内：不使用 replay buffer，不使用 deep network，不做离线训练循环。所有实验都是 streaming / continual learning 风格，agent 持续与环境交互并在线更新。主要方法是 tabular 或 linear function approximation，环境包括 access-control queue、tile-coded random walk、changing continuing gridworld、T-maze partial observability、Baird counterexample、small nonstationary streams 等。

研究主线来自 Alberta Plan：普通经验流、持续学习、价值函数、平均奖励、learned models、planning、GVFs、有限计算、时间一致性和稳定更新。项目不以“某方法分数更高”为唯一评价，而是要求每个 Proposal 回答一个明确 Core-RL 问题。

## RL Environments 设计与研究用途

本项目没有把环境当作随意替换的 benchmark，而是为不同 Core-RL 问题设计不同层次的 testbed。选择原则是：环境必须足够小，使 value scale、TD error、model staleness、prediction utility、feature utility 等内部量可以解释；同时不能小到只能证明一个两状态 toy phenomenon。每个环境都对应一个主要研究用途，报告中应明确说明环境为什么能回答该 proposal 的问题。

Access-Control Queue 是 reward centering 和 continuing control invariance 的主环境。状态由 free servers 数量和当前 customer priority 组成，动作是 reject/accept，接受高 priority customer 得到更高 reward，服务器以概率释放。这个环境是 continuing average-reward 风格，不存在自然 episode reset，因此适合研究 reward origin、average reward baseline、policy probes 和长期在线控制。`Reward-Centered Continuing Sarsa` 使用原始 access-control queue 来测试 constant reward shift 是否只改变 value offset 而不应改变 task behavior；`Scale-Invariant Continuing Control` 在同一环境上额外缩放 one-hot features，用它测试 reward translation 和 feature scaling 是否会共同破坏 Sarsa 更新；新增的 `Unit-Switching Continuing Control` 在同一个 stream 中途改变 reward shift 或 feature scale，用来检查不重置 agent 时的 recovery window。

Tile-Coded Random Walk 是 output-controlled prediction 的主环境。底层过程是随机游走，agent 在线预测到达右终端的 value；实验把状态表示成 overlapping tile-coded features，并人为改变 feature magnitude，包括 uniform scale、uneven scale 和 lognormal scale。这个环境的研究用途不是追求复杂行为，而是把“同一个预测问题在不同 feature units 下应该等价”这个问题变得可测量。`Output-Controlled TD` 和 `On-Policy TD(lambda) Stability Atlas` 用它比较 fixed TD、normalized TD、trace-normalized TD 和 true-online TD(lambda) 在 alpha/scale/lambda 网格下的 RMSE、divergence、weight norm 和 prediction-change。

Changing Continuing Gridworld 是 Dyna planning 和 model staleness 的主环境。agent 在一个 continuing grid 中移动，达到 goal 后回到 start，hazards 给负 reward；stream 中途切换 goal/hazard layout，但 agent 的 Q values 和 learned model 不重置。这个环境比两状态变化更有结构，因为 model 中的某些 state-action entries 会从“曾经正确”变成“现在过时”，planning 会反复重用这些 entries。`Dyna Planning Budget` 用它研究 planning steps 带来的 pre-change benefit 和 post-change stale-backup cost；`Continual Dyna With Model Aging` 用它比较 keep-model、oracle flush、recency aging、recency/error gate，并把 stale-backup rate、mean model error、planning TD magnitude 和 recovery windows 作为核心证据。

T-Maze Cue Environment 是 GVF/predictive-state 方向的主环境。每个 trial 开始时短暂出现 left/right cue，之后 agent 进入 aliased corridor，直到 junction 才需要根据早期 cue 选择动作。当前 observation 在走廊中不包含 cue，因此 raw observation 不足以控制；hand-coded trace 和 oracle memory 是强 baseline。这个环境专门检验“prediction 是否真的成为 useful state”：一个 GVF 即使有低 TD error，如果不能把 cue 信息带到 junction，也不能改善 control。`GVF Predictive State` 和 `Predictive State Plasticity` 用它比较 raw、history/trace、recurrent GVF、cue-GVF 和 oracle；`GVF Question Design` 用同一类 T-maze cumulants 检查不同 GVF question 的 prediction error 与 downstream utility 是否一致。

Trace-Conditioning Stream 是 generate-and-test feature selection 的主环境。stream 中 cue 出现后，reward 在某个 delay 后出现，且 relevant delay 会在中途改变。agent 的 feature budget 有限，需要决定保留哪些 trace features。这个环境的研究用途是区分“feature 很活跃”与“feature 对当前预测有用”：如果 utility rule 不能在 delay shift 后替换到新 relevant trace，它就不是好的 continual representation mechanism。`Generate-and-Test Trace Features` 用它比较 fixed、random replacement、generate-test 和 oracle-like trace choices。

Nonstationary Sensor Stream 是 TIDBD 和 auxiliary representation 的主环境。环境产生连续特征流，phase change 后 relevant feature group 改变，agent 必须在线调整 value prediction 或 auxiliary prediction。这个环境适合研究 per-feature step-size adaptation、old/new/distractor feature groups 和 auxiliary target 是否真正服务主任务。`TIDBD-Lite Plasticity` 用它看 per-feature alpha 是否转移到新 relevant features；`Streaming Representation With Auxiliary Prediction` 用它检验 next-feature auxiliary prediction 是否能改善主 value error，当前结果是否定的。

Baird-Style Counterexample 是 off-policy stability 的诊断环境。它不是为了模拟真实控制任务，而是为了制造 semi-gradient off-policy TD 的经典不稳定结构：behavior distribution 和 target policy 不匹配，importance sampling ratio 稀疏但巨大，linear value function 可能发散。`Baird Off-Policy Stability` 用它提醒 GVF/off-policy prediction 不能只靠普通 TD，需要 TDC/GTD/emphatic-style 稳定机制；当前它更适合作为 stability warning，而不是最终正向 proposal。

Four Rooms / Doorway Navigation 是 options 和 temporal abstraction 的候选环境。状态是 grid position，primitive actions 是上下左右，doorway options 执行持续多步的 temporally extended action。这个环境本来用于研究 reusable subtasks 和 goal-change transfer，但当前实现还没有证明 options 在 environment-step accounting 下优于 primitive baseline。因此 `Doorway Options for Reusable Subtasks` 被保留为 quarantined proposal：它的环境是合理的，但需要先通过 fixed-goal sanity test、SMDP duration accounting 和 goal-change recovery 分析。

Nonstationary Bandit 是最小 sanity-check 环境。它没有 state bootstrapping、planning 或 GVF，因此不能支撑强 Core-RL 结论；它的用途只是验证 online tracking、constant-alpha update 和 sample-average update 在 drifting reward 下的基本差异。`Nonstationary Bandit Sanity Check` 应作为 introduction 或 pipeline check，而不是最终 proposal。

## 推荐等级与选题组合建议

本节给出当前最实际的选题推荐，而不是把所有 proposal 平铺成同等强度。推荐等级综合考虑四点：研究问题是否清楚、Alberta Plan/Core-RL 连接是否强、当前实验是否已经产生非平凡证据、后续两三周内是否能通过 CPU-scale sweep 和报告修改提升到较高质量。这里的等级不是永久结论；如果后续实验改变证据，proposal 可以升级或降级。

### 强烈推荐

1. Scale-Invariant Continuing Control：这是当前强独立大课题之一。它把 reward centering 和 output-controlled TD/Sarsa 的核心思想放进一个 continuing control invariance 问题中，研究对象清楚：reward zero-point 和 feature scale 都是任务描述单位，不应改变 agent 的实质学习能力。完成的 fixed-condition extended grid 显示单独机制各有失败区间，而 combined normalized-centered / normalized-differential variants 更稳：组合 normalized variants 都是 `0/1500` divergent seed-conditions，mean tail unshifted reward 约 `2.55`；discounted 和 reward-centered-only Sarsa 都是 `500/1500` divergent seed-conditions。新增 no-reset unit-switch extension 则给出更严格也更诚实的结论：组合方法能防止 catastrophic instability，但 abrupt feature-unit change 后 recovery 仍未解决。优化建议是继续做 gradual unit drift，而不是宣称 invariance 已完全解决。

2. Continual Dyna With Model Aging：这是 planning/model-based 方向最强候选。它不是泛泛地说 Dyna planning 有帮助，而是把问题改成“哪些 learned model entries 还值得 planning”。当前 20 seeds extended sweep 显示 freshness-aware sampling 稳定降低 stale-backup rate，尤其在 planning budget `20` 下，keep-model late stale-backup rate 为 `0.213 +/- 0.065`，较短 half-life 的 recency aging 或 recency/error gate 可以接近 0。stochastic/gradual drift extension 已实现并有 smoke result，extended CPU task 正在运行但尚无标准 artifacts；最终 claim 应写成 search-control freshness tradeoff，而不是简单 reward superiority。

3. Reward-Centered Continuing Sarsa：这是最清楚的独立主 proposal 之一，问题简洁但不 shallow：continuing control 中 reward origin 不应改变 policy preference，但 ordinary discounted Sarsa 会产生 value-scale inflation。当前 access-control 结果很有说服力，reward-centered/differential variants 在 reward shifts 下保持更稳定 Q norm 和 unshifted reward。beta/gamma/no-reset midstream reward-origin switch 已实现并有 smoke result，extended CPU task 正在运行但尚无标准 artifacts；完成后它可以从强机制实验进一步提升为更完整的 continual adaptation 研究。

4. Output-Controlled TD：这是 prediction/function approximation 方向最清楚的主 proposal。它把 step size 的单位从 parameter displacement 转到 prediction-output change，直接回应 streaming TD 在 feature scale 改变下的脆弱性。当前可引用 primary evidence 是 20 seeds extended CPU-task run：`experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`。Seed-level divergence 统计显示 normalized TD 和 trace-normalized TD 都是 `0/400` seed-conditions 发散，而 fixed TD 和 raw-alpha true-online baseline 都是 `141/400`。完成的 normalized true-online fairness audit `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended` 显示 normalized TD 与 trace-normalized TD(lambda) 都是 `0/300`，fixed 与 raw-alpha true-online 都是 `81/300`，naive normalized true-online 是 `34/300`，失败集中在 lognormal scaling。

5. Dyna Planning Budget and Model Staleness：如果需要保留一个普通 proposal 作为 planning 方向的独立材料，它是最值得保留的。它的研究问题比很多支持性诊断更接近完整 RL 课题：planning budget 有 pre-change benefit，但 stale model backups 会损害 post-change recovery。优化建议是不要和 Continual Dyna Model Aging 重复提交；更合理的方式是把它作为 model-aging 大课题的前置实验或第一节 mechanism diagnosis。

6. Predictive State Plasticity：这是高风险但很有 insight 的推荐方向。当前不是正结果，甚至可以说是负向 gate：cue-GVF 有 cue-aligned signal，但 control accuracy 仍接近 chance，而 trace/oracle memory 能解决任务。它的价值在于指出“prediction signal 不等于 useful state”。如果老师喜欢挑战性和研究味更强的题目，可以保留它作为 representation/GVF 方向的深度课题；优化建议是先做 cue decodability、oracle-prediction control、feature ablation，再考虑 generate-and-test/TIDBD，不要直接宣称成功。

### 可推荐但需要补强

GVF Predictive State 可以作为 Predictive State Plasticity 的具体前身或负结果章节。它独立打开也能说明一个清楚问题：GVF 是否能替代 trace memory 成为 agent state；但当前结果是否定的，适合和 GVF Question Design 合并成一个更系统的 “useful predictions are not just accurate predictions” 研究线。优化建议是补 GVF cumulant/horizon 的形式化定义、cue-decodability probe 和 downstream control ablation。

Generate-and-Test Trace Features 有研究价值，但当前 utility rule 不够好，甚至 random replacement 更强。它适合与 Predictive State Plasticity 或 TIDBD-Lite 合并，形成“limited feature budget 下如何选择有用 predictive features”的 representation plasticity 课题。优化建议是重写 utility：从 activity/trace quality 转向 downstream TD-error reduction、control value contribution 或 cue-information retention。

TIDBD-Lite Plasticity 适合作为 supporting mechanism，而不是单独主提交。当前 per-feature alpha dynamics 可见，但 normalized TD 的 error 更好。优化建议是实现 canonical TIDBD 或 AutoStep，明确 meta-update 方程，并把 per-feature alpha movement 和实际 prediction/control gain 绑定。

Baird Off-Policy Stability 适合作为 off-policy GVF 稳定性章节或 appendix。它是 Core RL 中非常重要的警示，但当前需要 canonical Baird verification。优化建议是升级成 “Off-policy GVF Stability Under Behavior Drift” 综合课题：把 Baird-style counterexample、GTD/TDC、emphatic TD 和 behavior drift 连接起来，否则单独提交会显得像经典 counterexample 复现。

GVF Question Design 是很好的 diagnostic，但不能单独当强结果。它可以和 GVF Predictive State 合并，构成“哪些 prediction questions 值得学习”的前置研究。优化建议是把 prediction error、cue information、downstream control improvement 三个指标并列，而不是只比较 abs TD error。

### 一般推荐或支持性材料

Centered TD Diagnostics 很适合作为 Reward-Centered Sarsa 的机制附录。它能清楚解释 reward centering 为什么降低 value-scale inflation，但环境太小，不适合单独提交。建议把关键表/图并入 Reward-Centered report，而不是保留为独立最终题目。

On-Policy TD(lambda) Stability Atlas 很适合作为 Output-Controlled TD 的背景证据。它说明固定 alpha 的稳定区间受 feature scale、alpha、lambda 共同影响，但它本身没有 intervention。建议合并到 Output-Controlled TD 的 related diagnostic 或 appendix。

Streaming Representation With Auxiliary Prediction 当前是负结果：auxiliary next-feature prediction 几乎没有改善主 value error。它可以作为 Predictive State Plasticity 的警示性附录，说明 auxiliary prediction 必须 task-relevant，不能简单假设“多一个 auxiliary loss 就有用”。如果单独保留，需要重设计为更有控制意义的 auxiliary target。

Nonstationary Bandit Sanity Check 只适合作为 introduction 或 pipeline sanity check。它展示 constant-alpha tracking 的基本现象，但没有 state、bootstrapping、planning、GVFs 或 temporal abstraction，不建议作为最终 proposal。

Doorway Options 当前被 quarantine。Options 是重要 Core-RL topic，但当前结果没有证明 option transfer，也没有 fixed-goal sanity win。建议先暂停，不要投入大量实验，除非先修好 SMDP update、duration accounting 和 fixed-goal baseline。

### 合并研究建议

最终如果需要少而强的提交组合，建议选择两个或三个强主线：`Scale-Invariant Continuing Control`、`Continual Dyna With Model Aging`、`Reward-Centered Continuing Sarsa` 或 `Output-Controlled TD`。如果希望形成一个更有雄心的 representation 方向，可以把 `Predictive State Plasticity`、`GVF Predictive State`、`GVF Question Design`、`Generate-and-Test`、`TIDBD-Lite` 合并成一个 staged research program，但必须明确当前主结论是 negative gate 和 redesign，不是成功结果。对于 weak proposal，不建议强行补大量实验来“凑齐十个强题目”；更专业的做法是诚实降级、合并或作为 appendix。

## 三个更大的独立 Core-RL 课题

### 1. Scale-Invariant Continuing Control

报告路径：`final/reports/integrated/scale_invariant_continuing_control/report.md`

动机：一个持续学习 agent 面对的是长期运行的传感器和奖励流，而不是每次都由研究者重新整理好的 benchmark。如果同一个 continuing control 问题只是换了 reward zero-point，或者同一组特征只是换了单位尺度，agent 的学习稳定性和最终行为原则上不应该发生本质变化。Reward centering 主要解决 reward shift 带来的 value-scale inflation，output-controlled / normalized update 主要解决 feature scale 带来的 step-size mismatch，但这两个机制是否能在同一个控制问题中同时工作并不显然：centering 可能改变 TD error 分布，normalization 可能改变 reward baseline 的学习速度。因此本课题把两类“不该影响任务本质的单位变化”放进同一个 continuing access-control 问题中，研究小型在线 RL agent 是否能在 reward units 和 feature units 都变化时保持稳定。

研究问题：在 continuing access-control control 中，reward centering 和 output-controlled Sarsa 是否能组合成对 reward translation 与 feature scaling 都稳健的在线控制算法？

方法与实现：实现了 scaled access-control queue 环境。比较 `discounted_sarsa`、`reward_centered_sarsa`、`normalized_sarsa`、`normalized_reward_centered_sarsa`、`normalized_differential_sarsa`。每个 agent 都在线交互、在线更新；不存 replay，不用神经网络。实现位置在 `experiments/alberta_core_rl/studies/reward_centering.py`，配置在 `experiments/alberta_core_rl/configs/scale_invariant_continuing_control/`。

实验设计：fixed-condition extended sweep 交叉 reward shifts `-8, -4, 0, 4, 8`、feature scales `one, ten, hundred, uneven, lognormal` 和 alphas `0.01, 0.03, 0.1`，在 access-control queue 上评估 unshifted average reward、Q norm、TD-error scale、prediction change、divergence rate 和 policy probe。另一个已完成的 no-reset unit-switch extension 使用 20 seeds、20000 steps，在同一条 stream 中途改变 reward origin 或 feature scale。

当前结果：主结果目录是 `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`。结果显示 reward-centered Sarsa 单独能处理 reward shift，但在 feature scale 很大时仍会失败；normalized Sarsa 能控制 feature scale，但仍受 reward shift 影响；`normalized_reward_centered_sarsa` 和 `normalized_differential_sarsa` 在当前 sweep 中最稳健，mean tail unshifted reward 分别约 `2.556` 和 `2.554`，并且都是 `0/1500` divergent seed-conditions。

当前判断：这是强独立大课题之一，因为它把两个 Core-RL 更新机制放进同一个可解释的 invariance 问题里，而不是简单比较分数。当前 fixed-condition extended grid 已可作为 evidence；unit-switching 结果进一步说明组合机制能防止灾难性数值不稳定，但 abrupt feature-scale switch 后 reward recovery 仍会变差。下一步应该设计 gradual unit drift、recovery AUC 和 policy-distance probes，而不是继续强化“已经完全 invariant”的叙述。

### 2. Continual Dyna With Model Aging

报告路径：`final/reports/integrated/continual_dyna_model_aging/report.md`

动机：Dyna-style planning 对持续 agent 很有吸引力，因为 learned model 允许 agent 在真实交互之外做 background computation，用有限真实经验更新更多 value estimates。这很符合 Alberta Plan 中关于 learned models 和 planning 的长期愿景。但持续世界通常不是 stationary 的：门可能堵住，reward source 可能移动，transition probabilities 可能漂移。此时模型中最危险的部分不是没有学到的 entry，而是曾经正确、现在过时、却仍然被 planning 反复采样的 entry。如果只比较 planning backups 数量，就会把计算预算和模型可信度混在一起。本课题把 model freshness 作为 Dyna planning 的第一等问题，研究小型 online agent 能否不依赖 replay buffer、不依赖 oracle reset，而是通过 recency 和 model error 来决定哪些 learned transitions 仍值得 planning。

研究问题：一个小型 continual Dyna agent 如何在不知道 model entry 是否仍然新鲜的情况下分配 planning computation？

方法与实现：在 changing continuing gridworld 中维护 compact state-action model。比较 `keep_model`、`oracle_flush`、`recency_aging`、`recency_error_gate`。其中 `oracle_flush` 只作为上界/诊断，不作为现实方法；现实方法依赖在线 recency 和 model error。实现位置在 `experiments/alberta_core_rl/studies/planning_offpolicy.py`，配置在 `experiments/alberta_core_rl/configs/continual_dyna_model_aging/`。

实验设计：环境在 stream 中途改变 layout/hazard/goal dynamics，agent 继续学习不重置。实验交叉 planning budgets `0, 1, 5, 20` where applicable 和四种 model handling 策略。核心指标包括 real-step average reward、stale-backup rate、model one-step error、planning TD magnitude、model size、post-change recovery window。

当前结果：主结果目录是 `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`。在 planning budget `20` 时，`keep_model` 的 late post-change stale-backup rate 为 `0.213 +/- 0.065`；recency aging 可在较短 half-life 下把 stale rate 降到几乎 0，在 half-life `4000` 时仍只有约 `0.020 +/- 0.004`。同一 budget 下 late reward 最好约 `0.0925`，但 reward ranking 会随 half-life 和 model mode 改变，因此不能简单声称某个 aging rule 普遍最优。

当前判断：这是 planning 方向最清楚的课题。它把 Dyna 的“更多 planning”改写成“哪些 model entry 值得 planning”的问题。abrupt-change extended sweep 已完成，drift extension 已实现并在 CPU task 中运行；下一步应等待 artifacts 后更新 heatmaps 和报告，并继续设计 repeated-change 或 queue-like transition drift，避免结论只依赖单个 abrupt gridworld change。

### 3. Predictive State Plasticity

报告路径：`final/reports/integrated/predictive_state_plasticity/report.md`

动机：GVFs 在 Alberta Plan 中是构造 agent state 和世界知识的重要机制，但一个常见误区是把“能预测”直接等同于“对控制有用”。在 partial observability 下，agent 真正需要的是能把过去关键信息带到未来决策点的 state variable；一个预测如果只是在局部容易学习，却不携带 hidden cue 或不能被 downstream control update 利用，就不会改善行为。本课题选择 T-maze 作为刻意尖锐的测试：早期 cue 决定末端动作，但中间长走廊会抹掉 raw observation 中的 cue 信息。这个设置迫使我们区分 raw observation、hand-coded trace、oracle memory、learned GVF feature 和后续 plasticity 机制之间的作用。它的核心不是证明 GVF 一定有用，而是研究什么样的 predictive feature 才能变成 control 所需的 state。

研究问题：在部分可观测 T-maze 中，learned GVF features 能否携带并维持对控制有用的 hidden cue 信息，并胜过便宜的 trace memory baseline？

方法与实现：构造 T-maze cue 任务，比较 raw observation、trace memory、old recurrent GVF、redesigned cue-GVF 和 oracle memory。GVF 与 control learner 都在线更新。实现位置在 `experiments/alberta_core_rl/studies/predictive_state.py`，配置在 `experiments/alberta_core_rl/configs/predictive_state_plasticity/`。

实验设计：跨 maze lengths `8, 12, 20, 30` 评估 trial accuracy、average reward、GVF TD error、cue-alignment margin、hidden cue 信息是否进入控制 state，并补充 cue-decodability probe。当前还没有把 feature replacement / feature-wise plasticity 完整接入主实验，而是先做 first-gate：如果固定 cue-GVF 都不能成为有用 state，就不应直接上更复杂的 plasticity claim。

当前结果：主结果目录已更新为 `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`。20 seeds、maze lengths `8/12/20/30` 下，cue-GVF 仍接近 chance，trial accuracy 约 `0.504/0.508/0.505/0.494`；oracle 保持约 `0.931-0.950`，trace memory 在 length `30` 仍约 `0.827 +/- 0.013`。这比早期 pilot 更清楚地说明：当前 learned GVF feature 不是足够有用的 state。

当前判断：这是一个有价值但高风险的 negative gate。它明确说明“GVF 有一点预测信号”不等于“GVF 是有用 state”。下一步应加入更强的 oracle-prediction control、更直接的 cue information metric，并分阶段接入 feature selection 和 TIDBD，而不是直接宣称 predictive-state plasticity 成功。

## 十三个普通独立 Proposal

### 1. Reward-Centered Continuing Sarsa

报告路径：`final/reports/proposals/reward_centered_sarsa/report.md`

动机：在 continuing task 中，reward 的零点通常是人为约定，而不是环境的本质属性。如果给所有 reward 加上同一个常数，平均奖励意义下的 policy preference 不应该改变；一个长期运行的 agent 也不应该因为工程师把 reward sensor 重新标定就需要重新调 alpha 或重新设计 representation。普通 discounted Sarsa 在 gamma 接近 1 时会把常数 reward shift 积累成很大的 value offset，这个 offset 对 action preference 没有实质帮助，却会改变 TD error 尺度、weight norm 和 finite-step-size learning dynamics。Reward centering 的吸引力在于它是一个非常小的在线机制，可以在不引入 replay buffer 或 deep network 的情况下，让 continuing control 更接近 average-reward 问题本身。

研究问题：online reward centering 是否能让 Sarsa 在 continuing access-control queue 中对 constant reward shifts 更稳健？

方法与实现：比较 `discounted_sarsa`、`reward_centered_sarsa`、`differential_sarsa`。环境是 access-control queue，agent 在线决定 accept/reject 不同 priority 的 customer。实现位于 `experiments/alberta_core_rl/studies/reward_centering.py`。

实验与指标：当前 extended evidence 跨 reward shifts `-8, -4, 0, 4, 8` 和 alphas `0.02, 0.05, 0.1`，记录 unshifted average reward、accept rate、high-priority accept、reward_bar、TD error、Q norm、divergence 和 policy probes。主配置在 `experiments/alberta_core_rl/configs/reward_centered_sarsa/config_extended.json`。

结果与分析：当前主结果已更新为 `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended`。20 seeds、20000 steps、reward shifts `-8/-4/0/4/8` 与 alphas `0.02/0.05/0.1` 下，reward-centered Sarsa 的 unshifted reward 基本保持在 `2.55-2.60`，Q norm 约 `22-35`；discounted Sarsa 在 shift `8`、alpha `0.1` 时 Q norm 约 `1876`，unshifted reward 约 `1.70`。该课题是主线候选；beta/gamma sensitivity 和 midstream reward-origin switch 已实现并处于 extended CPU run pending 状态，标准 artifacts 写出前不作为最终证据。

### 2. Output-Controlled TD

报告路径：`final/reports/proposals/output_controlled_td/report.md`

动机：线性 TD 看似简单，但它对 feature scale 极其敏感：同一个状态如果用放大十倍的 feature vector 表示，固定 alpha 的 parameter update 会造成完全不同的 prediction-output change。对持续学习 agent 来说，这很不合理，因为传感器单位、tile coding normalization 或人工特征缩放都可能改变 feature magnitude，而任务本身并没有变。Output-controlled update 的核心思想是把步长单位从 parameter space 转到 prediction/output space：我们真正想控制的是一次 update 对当前预测造成多大改变，而不是参数向量移动了多远。本课题用 tile-coded random walk 研究这种 output-level normalization 是否能让 streaming TD 在不同 feature units 下保持稳定。

研究问题：normalized / output-controlled TD 是否能让 streaming TD prediction 对 feature scaling 更稳健？

方法与实现：在 tile-coded random walk prediction 中比较 fixed TD、normalized TD、trace-normalized TD 和 true-online TD(lambda) baseline。实现位于 `experiments/alberta_core_rl/studies/prediction_scale.py`。

实验与指标：跨 feature scales `one, ten, hundred, uneven` 和 alphas `0.03, 0.1, 0.3`，评估 RMSE、divergence、weight norm、prediction_change、effective step size。主配置在 `experiments/alberta_core_rl/configs/output_controlled_td/config_main.json`。

结果与分析：当前主结果 `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended` 使用 20 seeds、20000 steps、5 个 feature scales 和 4 个 alpha。Seed-level divergence 结果显示 normalized variants 在完整 stress grid 下没有发散，而 fixed TD 和当前 raw-alpha true-online baseline 在 high scale/high alpha 条件下大量发散。该课题是主线候选，但仍需要进一步审计 true-online baseline，实现 max-stable-alpha comparison，并加入 no-reset feature-scale switch。

### 3. GVF Predictive State

报告路径：`final/reports/proposals/gvf_predictive_state/report.md`

动机：Alberta Plan 强调 agent 应该通过大量预测来构建对世界的持续理解，GVFs 因此常被视为 agent state 的重要组成部分。但这里有一个关键科学问题：预测准确本身并不保证预测对控制有用。一个 GVF 可能预测的是容易学习但与当前决策无关的 cumulant，也可能在局部状态上误差很低，却没有把早期 cue 信息传递到后续需要决策的位置。T-maze partial observability 正好暴露这个问题：如果 agent 只看当前 observation，它在走廊中无法知道终点应向左还是向右；如果 GVF 真能成为 useful state，它必须在 raw observation 丢失 cue 后仍然携带足够的 hidden-cue 信息。本课题的动机就是把“GVF as prediction”和“GVF as useful control state”明确区分开。

研究问题：在部分可观测 T-maze 中，GVF predictions 是否能替代显式 cue memory，成为 control 的有用 state？

方法与实现：比较 raw observation、short/history features、trace memory、recurrent GVF 和 oracle memory。环境是带 hidden cue 的 T-maze。实现位于 `experiments/alberta_core_rl/studies/predictive_state.py`。

实验与指标：评估 trial accuracy、avg reward、GVF values、cue trace、GVF TD error 和 control TD error。当前主结果路径是 `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`。

结果与分析：trace memory 和 oracle memory 能解决任务，而 recurrent GVF 仍接近 chance。这是明确的 negative result：当前 GVF question/design 不足以产生有用 state。该课题应作为 predictive-state redesign 的依据，而不是作为正结果提交。

### 4. Generate-and-Test Trace Features

报告路径：`final/reports/proposals/generate_test_features/report.md`

动机：持续学习 agent 长期运行时会不断遇到新统计结构，如果 representation 只能增加不能淘汰，计算和存储都会失控；如果 representation 固定不变，又可能无法适应新的相关特征。Generate-and-test 的思想是让 agent 在线生成候选 features，同时用某种 utility signal 淘汰低价值 features。这听起来很适合 continual learning，但真正困难的是 utility metric：一个 feature 活动频繁、短期 TD correlation 大，未必说明它对未来预测或控制有用。本课题用 delay-shift prediction stream 检查 generate-and-test 是否能在有限 feature budget 下找到当前 relevant trace，而不是只制造看似活跃但无效的 features。

研究问题：在 delay-shift streaming prediction 中，generate-and-test 是否能维护比 random/fixed features 更有用的 trace features？

方法与实现：构造 feature-budget 受限的 delay prediction stream。比较 fixed/random/generate-test/oracle-like trace choices。实现位于 `experiments/alberta_core_rl/studies/feature_plasticity.py`。

实验与指标：环境中 relevant delay 会变化；指标包括 absolute prediction error、feature utility、replacement count、post-change recovery。当前主结果是 `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`。

结果与分析：当前 generate-and-test utility 没有明显优于 random/fixed baseline，虽然能看到 feature replacement 机制在工作。结论是该设计目前不够好，需要重新设计 utility metric，不能作为强正结果。

### 5. Doorway Options for Reusable Subtasks

报告路径：`final/reports/proposals/options_reusable_subtasks/report.md`

动机：Options 和 temporal abstraction 是 Core RL 中连接短时动作和长时行为的重要机制。Alberta Plan 中长期 agent 不可能永远只用 primitive actions 进行逐步规划，它需要能复用 doorway、navigation、approach 等子任务结构。但 options 很容易产生虚假的好结果：如果只按 decision count 而不是 environment step 计数，或者只在固定 goal 下测试，一个 option 看起来更快并不说明它真的提高了学习效率。一个有研究价值的 options proposal 应该证明 temporal abstraction 在真实环境步数、goal change 和 subtask reuse 上都站得住。本课题原本想检验 doorway options 是否能在 Four Rooms 中复用，但当前证据要求先退回 fixed-goal sanity check。

研究问题：在 Four Rooms / doorway navigation 中，doorway options 是否能在 goal change 后改善 learning 或 transfer？

方法与实现：实现 doorway option style 的 SMDP control，对比 primitive actions 和 options。实现位于 `experiments/alberta_core_rl/studies/temporal_abstraction.py`。

实验与指标：评估 environment-step accounting、average reward、steps to goal、goal-change recovery。当前主结果是 `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`。

结果与分析：当前结果不支持 option-transfer claim，因此该 proposal 被 quarantined。下一步必须先建立 fixed-goal sanity case，证明 option 实现本身合理，再讨论 transfer。

### 6. TIDBD-Lite Plasticity

报告路径：`final/reports/proposals/tidbd_plasticity/report.md`

动机：持续学习中的 representation 往往不是静态的：一些 features 长期稳定但变化慢，另一些 features 新出现、短期相关、需要快速适应。使用单一全局 alpha 会把这些不同需求压成一个折中，可能导致旧知识被过快扰动，也可能导致新特征学得太慢。TIDBD 类方法的核心吸引力是把 plasticity 放到 feature level：每个 feature 都可以根据自己的历史误差信号调整 step size。本课题并不试图用 TIDBD-lite 直接解决大型控制问题，而是先问一个更基础的问题：在小型 streaming prediction 中，per-feature step-size adaptation 是否能产生可解释的 plasticity dynamics，并相对 normalized TD 带来实际预测收益。

研究问题：TIDBD-lite 是否能在 streaming prediction 中识别并提高新相关 features 的 plasticity，同时不破坏稳定性？

方法与实现：在线预测流中对不同 feature groups 使用 per-feature step-size adaptation，并与 normalized TD 等 baseline 比较。实现位于 `experiments/alberta_core_rl/studies/feature_plasticity.py`。

实验与指标：评估 abs TD error、per-feature alpha、old/new feature group dynamics、post-change recovery。当前主结果是 `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`。

结果与分析：TIDBD-lite 的 step-size 机制可见，但当前 error baseline 仍不优于 normalized TD。因此它是 supporting mechanism study，不是正向性能 proposal。

### 7. Baird Off-Policy Stability

报告路径：`final/reports/proposals/baird_offpolicy_stability/report.md`

动机：如果 agent 同时学习许多预测和许多行为相关的 value functions，它几乎不可避免会遇到 off-policy learning：当前行为产生的数据不一定来自目标预测或目标策略。Alberta Plan 的多预测愿景因此必须面对一个基础稳定性问题：线性 function approximation 加 bootstrapping 加 off-policy sampling 可能发散。Baird counterexample 的价值不在于它像真实环境，而在于它以最小形式暴露了 semi-gradient off-policy TD 的结构性风险。本课题把它作为警示性诊断，提醒后续 GVF/off-policy proposal 不能只看 prediction count 或 short-term error，而必须检查稳定性机制。

研究问题：在 Baird-style off-policy setting 中，semi-gradient off-policy TD 与 TDC 类修正方法的稳定性差异如何体现？

方法与实现：实现 Baird-style features、behavior/target mismatch 和 importance sampling ratio，比较 offpolicy TD 与 TDC。实现位于 `experiments/alberta_core_rl/studies/planning_offpolicy.py`。

实验与指标：跨 alpha sweep 记录 weight norm、TD error、divergence。当前主结果是 `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`。

结果与分析：结果支持“off-policy linear TD 需要非常谨慎”的诊断结论。但报告也明确指出 canonical setup 仍需进一步核查，因此不应做过宽泛理论 claim。

### 8. Dyna Planning Budget and Model Staleness

报告路径：`final/reports/proposals/dyna_planning_budget/report.md`

动机：Dyna 的经典优势是用 learned model 做额外 backups，从而用同样数量的真实交互获得更多 value updates。但在 continual learning 中，model 的价值不是单调增加的：过去学到的 transition 可能在环境变化后变成错误知识。如果 agent 继续从旧 model 中均匀抽样，planning budget 越大，错误 backups 被放大的机会也越多。因此本课题把 Dyna planning budget 和 model staleness 放在一起研究，先用一个 changing gridworld 诊断 stale-backup 问题是否真实存在，再为更完整的 model-aging proposal 提供依据。

研究问题：在 changing continuing gridworld 中，planning budget 和 model staleness 如何影响 pre-change performance 与 post-change recovery？

方法与实现：实现 continuing gridworld，中途改变 phase；比较不同 planning_steps 和 keep/flush model handling。实现位于 `experiments/alberta_core_rl/studies/planning_offpolicy.py`。

实验与指标：评估 avg reward、stale_backup_rate、model_size、q_norm、recovery windows。当前主结果已更新为 `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended`。

结果与分析：planning 能改善 pre-change reward，但 keep-model 在 change 后 stale backups 高，可能拖慢恢复。该 proposal 是 Dyna model aging 综合课题的直接基础。

### 9. Centered TD Diagnostics

报告路径：`final/reports/proposals/centered_td_diagnostics/report.md`

动机：Reward centering 如果只在完整 control task 中展示 reward 更高，很难说清楚它到底改变了什么：是 policy 变好了、value scale 稳了、TD error 变小了，还是只是某个 alpha 更合适。为了让 Reward-Centered Sarsa 的主结论可解释，需要一个更小的机制诊断实验，把 reward shift、TD target、value norm 和 baseline tracking 分开观察。本课题的价值在于提供“为什么 centering 有帮助”的证据，而不是作为独立 benchmark 追求最高分。

研究问题：reward centering 如何影响 value norm、TD error 和 reward shift sensitivity？

方法与实现：在小型 diagnostic prediction/control setting 中比较 centered 与 uncentered TD-style updates。实现位于 `experiments/alberta_core_rl/studies/diagnostics.py`。

实验与指标：跨 reward shifts 记录 value norm、centered target、TD error。当前主结果是 `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main`。

结果与分析：该实验支持 reward-centering 主线的机制解释，但本身不是完整 control proposal。它应作为 Reward-Centered Sarsa 的 supporting diagnostic。

### 10. On-Policy TD(lambda) Stability Atlas

报告路径：`final/reports/proposals/onpolicy_stability_atlas/report.md`

动机：TD(lambda) 在教学和实践中都很常用，但它的稳定性不是由一个 alpha 决定的，而是 alpha、lambda、feature scale、representation overlap 和 bootstrapping 共同作用的结果。很多时候算法失败不是因为 TD(lambda) 概念错，而是因为固定 step size 在某个 feature scale 下越过了稳定边界。Output-Controlled TD 的主张需要一个背景图谱来说明：为什么仅仅“调小 alpha”不是一个满意的 continual-learning 解决方案。本课题通过 stability atlas 展示不同 lambda/scale/alpha 组合下的稳定区域，为 normalized update 的必要性提供支持。

研究问题：在 on-policy linear prediction 中，alpha、lambda 和 feature scale 如何共同决定稳定或发散？

方法与实现：在 tile/random-walk style prediction 中系统扫描 alpha/lambda/scale。实现位于 `experiments/alberta_core_rl/studies/diagnostics.py`。

实验与指标：评估 RMSE、weight norm、divergence、TD error。当前主结果是 `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main`。

结果与分析：该 proposal 是 Output-Controlled TD 的 supporting atlas。它帮助说明固定 alpha 在不同 feature units 下很脆弱，但不应替代主 proposal。

### 11. GVF Question Design

报告路径：`final/reports/proposals/gvf_question_design/report.md`

动机：GVF 框架的灵活性既是优势也是风险：我们可以定义很多 cumulants、policies 和 horizons，但并不是每个 question 都会产生对 agent state 有价值的信息。一个容易预测的 cumulant 可能只是局部可见变量的平滑版本，对 hidden state 或 control decision 没有帮助；一个难预测但与未来决策高度相关的 question 反而更重要。本课题的动机是把 GVF design 从“多预测几个量”推进到“选择能改善下游 state 的问题”，并为 T-maze predictive-state 失败提供诊断工具。

研究问题：不同 GVF question 在预测误差和下游 state usefulness 上是否存在明显分离？

方法与实现：构造多个 GVF cumulants/questions，比较它们的 prediction error 与对 hidden cue/control 的帮助。实现位于 `experiments/alberta_core_rl/studies/diagnostics.py`。

实验与指标：评估 GVF prediction error，并把 cue relevance 和 downstream utility 明确标为下一步需要补的 probe。当前主结果是 `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main`。

结果与分析：结果支持一个重要 insight：prediction accuracy 不等于 useful state。它为 GVF Predictive State 和 Predictive State Plasticity 的 redesign 提供依据。

### 12. Nonstationary Bandit Sanity Check

报告路径：`final/reports/proposals/nonstationary_bandit/report.md`

动机：在进入复杂 continuing control、GVF 或 Dyna 之前，一个最小的 sanity check 是确认在线 learner 能否在非平稳 reward stream 中持续跟踪变化。Nonstationary bandit 没有状态、没有 bootstrapping，也没有 representation learning，因此它不够支撑最终 course project 主线；但它能用最简单的形式展示 constant-alpha tracking、adaptation lag 和 exploration/exploitation 在 drift 下的基本现象。本课题保留它的目的不是发表式创新，而是作为 continual-learning intuition 和代码管线 sanity check。

研究问题：在最小非平稳 reward stream 中，简单 online learner 能否跟踪 reward drift？

方法与实现：实现 small nonstationary bandit，对比 tracking-style updates。实现位于 `experiments/alberta_core_rl/studies/feature_plasticity.py`。

实验与指标：评估 regret/reward tracking、adaptation after shift。当前主结果是 `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`。

结果与分析：这是 sanity check，不够支撑最终 Core-RL 研究 proposal。它保留为最小背景实验，但已经被降级为 dropped diagnostic。

### 13. Streaming Representation With Auxiliary Prediction

报告路径：`final/reports/proposals/streaming_representation/report.md`

动机：在深度 RL 和 representation learning 中，auxiliary prediction 经常被认为可以帮助主任务学习更好的 state representation。但在本项目限制下，没有 replay buffer、没有 deep network、没有大规模共享表示，辅助预测是否仍然有用就不是显然的。一个 next-feature prediction 任务可能只是学习了容易预测的局部动态，却没有改善主 value prediction；也可能因为共享有限 features 而和主任务竞争学习资源。本课题用小型 streaming setting 检验辅助预测是否真正改善主任务，而不是默认“多一个 auxiliary loss 就更好”。

研究问题：在 streaming prediction setting 中，加入 auxiliary next-feature prediction 是否能改善主 value prediction，而不是只降低 auxiliary error？

方法与实现：在线维护 value predictor 和 auxiliary predictor，比较是否使用 auxiliary representation。实现位于 `experiments/alberta_core_rl/studies/feature_plasticity.py`。

实验与指标：评估主 prediction error、auxiliary error、representation-related metrics。当前主结果是 `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main`。

结果与分析：当前 auxiliary next-feature prediction 没有明显改善 value prediction，因此作为 negative diagnostic 保留，不作为最终提交主线。

## 逐课题详细审阅卡片

本节比前面的快速总览更细，目的是支持逐个 Proposal 审稿。每张卡片都按同一个逻辑读：这个课题研究什么 RL 问题，环境和 agent 是什么，实验变量是什么，指标怎么回答问题，当前证据说明什么，以及主要风险在哪里。

### A1. Scale-Invariant Continuing Control 详细卡片

核心定位：这是一个更大的独立主线候选，综合 reward centering 和 output-controlled update 的思想，但研究对象不是两个方法的简单拼接，而是 continuing control 中“任务单位变化不应改变学习结论”的 invariance 问题。

RL problem：环境是 continuing access-control queue。状态表示 free servers 与 customer priority 的组合；动作是 accept 或 reject；reward 是接受 customer 后的 priority-dependent payoff 加上可控 reward shift；目标是持续在线学习一个 accept/reject policy，使 unshifted long-run reward 稳定。没有 episode reset、没有 replay、没有 offline data。

Agent 与算法：固定 step-size Sarsa、reward-centered Sarsa、normalized Sarsa、normalized reward-centered Sarsa、normalized differential Sarsa 都使用线性 action-value approximation。Reward centering 维护在线 reward baseline；normalized update 用 feature norm 控制每次 update 的输出变化；differential variant 使用平均奖励思想避免 discount value 被 reward offset 放大。

实验变量：reward shift 取 `-4, 0, 8`，feature scale 取 `one, ten, hundred, uneven`。这些变量故意改变问题描述单位，而不是改变任务语义。好的算法应当在这些等价或近似等价的问题描述下保持相似 policy、value scale 和 unshifted reward。

主要指标：`avg_unshifted_reward` 回答行为质量是否稳定；`q_norm` 回答 value scale 是否被 reward/feature units 放大；`prediction_change` 和 `step_size` 回答 update geometry 是否受控；`diverged` 回答算法是否进入数值失败区；policy probes 回答是否学到相似 accept/reject 决策。

当前证据：结果目录 `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`。单独 reward centering 在 feature scale 很大时不够；单独 normalization 仍然对 reward shift 敏感；combined normalized-centered 和 normalized-differential variants 在当前 extended sweep 中表现最稳。这个交互是该课题最有价值的 insight。

主要风险：当前环境仍是小型 synthetic queue，feature scaling 是人为 stress test；还需要一个 stream 中途改变 scale/reward-origin 的非平稳实验，以及 alpha sweep，避免结论只是某组超参数下成立。

### A2. Continual Dyna With Model Aging 详细卡片

核心定位：这是 planning/model-based 方向的主线候选。它把 Dyna 的问题从“planning backup 越多越好吗”改成“持续 agent 应该信任哪些 model entry”。

RL problem：环境是 changing continuing gridworld。agent 在线移动并获得 reward，stream 中途环境 phase 改变；agent 不重置，需要继续在新 dynamics 下控制。learned model 是 state-action 到 next-state/reward 的小表，不是 replay buffer。

Agent 与算法：基础 Dyna-Q control 使用真实 step 更新 Q，再从 learned model 中抽样做 planning backup。比较四种 model handling：`keep_model` 保留旧模型，`oracle_flush` 在变化时清空模型，`recency_aging` 按 last_seen 降低旧 entry 的 sampling probability，`recency_error_gate` 同时考虑 recency 和 model error。

实验变量：planning budget 为 `1, 5, 20`；model mode 为四种 freshness 策略；环境在 run 中途切换 phase。这个设计可以分离三个问题：planning 是否有 pre-change benefit，旧 model 是否造成 post-change harm，aging 是否在保留有用 model 与避免 stale backup 之间形成更好 tradeoff。

主要指标：`avg_reward` 衡量真实行为；`stale_backup_rate` 是核心机制指标，直接测 planning 是否浪费在旧 phase entry 上；`mean_model_error` 衡量模型预测质量；`planning_abs_td` 衡量 backup 强度；`recovery_window` 支持 pre/post 分段解释。

当前证据：结果目录 `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`。在 planning budget `20` 时，freshness-aware methods 把 keep-model 的 `0.213 +/- 0.065` late stale-backup rate 降到接近 0 或约 `0.020`；reward 差异依赖 half-life 和 budget，说明“减少 stale backup”与“提高 reward”之间存在 search-control tradeoff。

主要风险：当前是 abrupt gridworld change，staleness 定义清楚但也偏理想化；需要 stochastic/gradual drift 环境和 half-life sweep。`oracle_flush` 只能作为诊断上界，不能作为现实方法宣传。

### A3. Predictive State Plasticity 详细卡片

核心定位：这是 representation/GVF 方向的高风险综合课题。它的价值在于严格区分“预测误差低”“预测携带 hidden cue”“预测能改善 control state”三件事。

RL problem：环境是部分可观测 T-maze。起点附近有 cue，之后 agent 进入长走廊，最后在 junction 做选择；如果没有记住 cue，末端动作接近随机。agent 需要在线构造 state representation 支撑 control。

Agent 与算法：比较 raw observation、trace memory、old recurrent GVF、redesigned cue-GVF、oracle memory。control learner 是 normalized linear Sarsa；GVF learner 是 online TD。trace/oracle 是强 baseline，用来避免把一个弱 GVF 误判为正结果。

实验变量：maze length 为 `8, 12, 20`；representation mode 为五种。当前 first-gate 还没有完整接入 generate-and-test 和 TIDBD，因为如果固定 cue-GVF 都不能产生有用 state，直接上 feature plasticity 会让失败原因不可解释。

主要指标：`trial_accuracy` 是最终 control 指标；`cue_alignment_margin` 衡量 learned GVF output 是否朝正确 hidden cue 方向分离；`gvf_abs_td_error` 衡量预测学习本身；`avg_reward` 和 `control_td_error` 支持学习动态分析。

当前证据：结果目录 `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`。trace/oracle memory 明显优于 chance，cue-GVF 在 maze lengths `8/12/20/30` 下仍约 `0.50`，说明当前 GVF 有局部信号但不是足够有用的 state。

主要风险：negative result 的解释空间很大，可能是 GVF question 不对、GVF output scale 不对、control learner 不会利用小 margin、或者 memory mechanism 结构不够。下一步必须加 oracle-prediction control、cue information metric 和 representation ablation。

### B1. Reward-Centered Continuing Sarsa 详细卡片

核心定位：这是最清楚的 Core RL 主线之一，研究 continuing control 中 reward baseline 对 Sarsa learning dynamics 的影响。

RL problem：access-control queue 是平均奖励经典环境。服务器数量有限，customer 有不同 priority；agent 决定 accept/reject。加入 constant reward shift 后，真实任务偏好不应变化，因此 unshifted reward 是主要评价对象。

Agent 与算法：`discounted_sarsa` 使用 gamma 接近 1 的 ordinary action-value update；`reward_centered_sarsa` 从 reward 中减去在线估计的 reward_bar；`differential_sarsa` 用 gamma=1 和 average-reward/differential 思路更新。所有算法都是 online Sarsa，无 replay。

实验变量：当前索引结果使用 reward shifts `-8, -4, 0, 4, 8`，alphas `0.02, 0.05, 0.1`，seeds `0-19`，steps `20000`。每个 run 记录 online update 后的 reward、policy probe、value norm、divergence 和 accept statistics。

主要指标：`avg_unshifted_reward` 是任务表现；`q_norm` 是 reward-origin sensitivity 的核心诊断；`reward_bar` 观察 centering baseline 是否跟踪；`high_priority_accept` 和 policy probes 检查策略是否被 shift 干扰。

当前证据：结果目录 `experiments/alberta_core_rl/results/reward_centered_sarsa/20260709T024517Z_extended`。ordinary discounted Sarsa 的 value norm 随 reward shift 大幅增长；centered/differential variants 在 20-seed extended sweep 中保持更稳定 value scale 和 unshifted reward。

主要风险：需要更长 seeds/steps 和 alpha sweep。当前结论主要是机制稳定性，不应过度包装成所有 continuing tasks 上的性能提升。

### B2. Output-Controlled TD 详细卡片

核心定位：这是 prediction / function approximation 方向的主线，研究 streaming TD 如何摆脱 feature scale 对 step size 的任意影响。

RL problem：tile-coded random walk prediction。agent 观察当前 state 的 tile features，在线预测 value；环境产生 transition 和 terminal reward。任务重点不是 control，而是稳定的 online value prediction。

Agent 与算法：比较 fixed TD、normalized TD、trace-normalized TD 和 true-online TD(lambda) baseline。normalized variants 按 feature norm 或 trace norm 控制 update，使 prediction output change 更接近固定单位。

实验变量：feature scale 为 `one, ten, hundred, uneven`；alpha 为 `0.03, 0.1, 0.3`；main representation 是 tile coding。这个 sweep 直接测试“同一预测问题用不同 feature units 表示时算法是否仍稳定”。

主要指标：`rmse` 衡量预测质量；`diverged` 和 `weight_norm` 衡量数值稳定；`prediction_change` 衡量单步输出扰动；`step_size` 记录 normalized update 的有效步长。

当前证据：primary result 目录 `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`；fairness audit 目录 `experiments/alberta_core_rl/results/output_controlled_td_fairness_audit/20260709T085746Z_extended`。primary run 中 normalized 和 trace-normalized TD 在 400 个 seed-conditions 中均没有发散；fixed TD 和 raw-alpha true-online baseline 各有 141/400 个 seed-conditions 发散。fairness audit 中 normalized TD 和 trace-normalized TD(lambda) 仍为 `0/300`，fixed 与 raw-alpha true-online 为 `81/300`，naive normalized true-online 为 `34/300`。由于结果目录由 rjob 容器用户创建，正式报告图存放在 `final/reports/proposals/output_controlled_td/figures/` 和 `final/reports/proposals/output_controlled_td/fairness_figures/`。

主要风险：true-online baseline 需要继续谨慎解释，避免把 raw-alpha 单位不公平写成算法本身失败；已完成的 normalized true-online fairness audit 说明 naive normalization 能修复 uniform-scale failures，但在 lognormal scaling 下仍不完整。

### B3. GVF Predictive State 详细卡片

核心定位：这是 GVF-as-state 的直接检验，当前是 negative/redesign proposal。

RL problem：长 T-maze partial observability。cue 在早期出现，后续 observation aliasing，末端动作必须依赖记忆。问题是 learned prediction 能否代替手写 memory。

Agent 与算法：比较 raw、history/short_history、trace_memory、recurrent_gvf、oracle。GVF learner 在线预测与 cue/outcome 相关 cumulants，control learner 使用 raw+GVF values 作为 state。

实验变量：main run 使用较长 maze 和多种 representation modes。trace memory 与 oracle 是必要 baseline，因为它们证明环境本身可解。

主要指标：`trial_accuracy`、`avg_reward`、GVF value by position、cue traces、`gvf_abs_td_error`、`control_td_error`。如果 GVF 有用，应同时看到 cue-related signal 和 improved trial accuracy。

当前证据：结果目录 `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`。trace/oracle 成功，recurrent GVF 失败。结论是当前 GVF question 不足以成为 useful state。

主要风险：不能把“GVF 失败”泛化成“GVF 不行”。它只说明当前 question/architecture/update coupling 不够，需要 GVF Question Design 和 Predictive State Plasticity 继续拆解。

### B4. Generate-and-Test Trace Features 详细卡片

核心定位：这是 feature construction/plasticity 方向的机制实验，当前是负结果。

RL problem：delay-shift prediction stream。真实有用信息来自某个 delay trace，但 relevant delay 会变化；agent 的 feature budget 有限，必须替换或选择 features。

Agent 与算法：比较 fixed feature bank、random replacement、generate-and-test、oracle-like trace selection。generate-and-test 根据 utility score 删除低效 feature 并生成新 trace feature。

实验变量：feature budget、delay/recovery window、replacement strategy。环境变化让旧 feature 可能失效，新 feature 需要被发现。

主要指标：`abs_error` 是预测误差；replacement count 显示机制是否活跃；utility trajectory 显示 feature selection 是否识别有用 trace；post-change recovery 显示 plasticity 是否真的帮助适应。

当前证据：结果目录 `experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`。机制能替换 feature，但当前 utility 没有带来比 random/fixed 更好的预测误差。

主要风险：utility metric 可能错把高活动或短期相关当成有用；实验若只看 abs error，会遗漏 feature-selection dynamics。下一版应把 utility 与 downstream value/control improvement 绑定。

### B5. Doorway Options for Reusable Subtasks 详细卡片

核心定位：这是 temporal abstraction/options 方向的独立课题，但当前被 quarantine。

RL problem：Four Rooms / doorway navigation。agent 需要到达目标，doorway option 本应封装“走到门口/穿过门”的 reusable subtask。

Agent 与算法：primitive-action control 与 option-augmented SMDP control 比较。option 执行期间消耗真实 environment steps，更新时应按 SMDP target 处理 duration。

实验变量：是否启用 options，goal 是否改变，fixed-goal sanity 与 transfer setting。一个合格实验必须先证明 fixed-goal 下 options 没有实现错误，再讨论 transfer。

主要指标：steps-to-goal、average reward、environment step count、option duration、post-goal-change recovery。不能只按 decision count 计，因为 option 会隐藏真实环境步数。

当前证据：结果目录 `experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`。当前结果不支持 option-transfer claim。

主要风险：option 实现、termination、step accounting、goal-change protocol 都可能导致假失败或假成功。下一步必须先做 fixed-goal sanity case。

### B6. TIDBD-Lite Plasticity 详细卡片

核心定位：这是 per-feature step-size adaptation 的机制研究，支持 representation plasticity 主线。

RL problem：streaming prediction 中 feature relevance 会变化。固定全局 alpha 可能让旧 feature 学太慢或新 feature 过快发散。

Agent 与算法：TIDBD-lite 为每个 feature 维护可调 step size，使用 meta-gradient-like signal 调整 alpha；baseline 包括 fixed/normalized TD。实现强调在线更新，不保存过去样本。

实验变量：feature groups、change point、old/new relevance、meta step-size。当前是小型机制实验，不是大规模 control task。

主要指标：prediction error、TD error、per-feature alpha trajectories、old/new feature group dynamics、recovery after change。重点是看 step-size adaptation 是否有解释性，而非单一 reward。

当前证据：结果目录 `experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`。TIDBD-lite 的 alpha 变化可见，但 error 没有超过 normalized TD。

主要风险：TIDBD-lite 不是 canonical 完整 TIDBD；meta-parameter tuning 可能影响很大。当前只能作为 supporting mechanism，不适合作为主 claim。

### B7. Baird Off-Policy Stability 详细卡片

核心定位：这是 off-policy stability 的警示性诊断，提醒 Alberta Plan 中大量预测/多策略学习不能忽略 off-policy divergence。

RL problem：Baird-style counterexample。behavior distribution 与 target update 不匹配，线性 function approximation 下 semi-gradient TD 会出现不稳定。

Agent 与算法：比较 semi-gradient off-policy TD 和 TDC-like correction。使用 importance sampling ratio、Baird features、alpha sweep。

实验变量：alpha 取多个值；算法为 offpolicy TD/TDC；steps 记录持续更新过程。

主要指标：`weight_norm` 和 `diverged` 是核心；TD error 辅助说明更新压力；不同 alpha 下稳定区间是主要结论。

当前证据：结果目录 `experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`。结果支持 off-policy semi-gradient TD 的不稳定警告。

主要风险：当前实现称为 Baird-style，需要继续核查是否完全 canonical。报告必须把结论限制在 diagnostic level。

### B8. Dyna Planning Budget and Model Staleness 详细卡片

核心定位：这是 Dyna model-aging 综合课题的基础版本。

RL problem：changing continuing gridworld。agent 在线学习 Q 和 one-step model；环境中途改变；agent 不重置。

Agent 与算法：Dyna-Q with planning budget。比较 planning steps `0, 1, 5` 以及 keep/flush model handling。

实验变量：planning budget、model mode、pre/post recovery window。该设计先验证“stale model backup 是否真实存在”。

主要指标：average reward、stale-backup rate、model size、q norm、recovery window。stale-backup rate 是该 proposal 最重要的机制指标。

当前证据：结果目录 `experiments/alberta_core_rl/results/dyna_planning_budget/20260709T024602Z_extended`。20-seed larger-grid run 显示 planning 有 pre-change benefit；在 budget `20` 时 keep-model late stale-backup rate 仍约 `0.294`，flush 为 `0`，但 late reward 对 keep/flush 相近，因此它更适合作为 model-aging 前置诊断，而不是单独夸大 reward superiority。

主要风险：基础版本 model handling 太粗；需要 recency aging / model-error gating，这已经在综合课题中实现。

### B9. Centered TD Diagnostics 详细卡片

核心定位：这是 Reward-Centered Sarsa 的机制解释实验。

RL problem：小型 prediction/control diagnostic，人工 reward shift 可控。目标不是创造新 benchmark，而是隔离 reward centering 对 value scale 的作用。

Agent 与算法：centered TD-style update 与 uncentered update 比较，观察同一任务在不同 reward origin 下的 value dynamics。

实验变量：reward shift、centering method、alpha。实验规模小，但变量指向明确。

主要指标：value norm、TD error、centered target、reward baseline。value norm 是解释 reward shift sensitivity 的核心。

当前证据：结果目录 `experiments/alberta_core_rl/results/centered_td_diagnostics/20260708T160958Z_main`。结果支持 centering 能降低 value-scale inflation。

主要风险：这是 diagnostic，不是完整 control study。应作为 Reward-Centered Sarsa 的补充图/附录，而非独立强提交主线。

### B10. On-Policy TD(lambda) Stability Atlas 详细卡片

核心定位：这是 Output-Controlled TD 的稳定性背景图谱。

RL problem：on-policy linear prediction。任务本身简单，但系统扫描 alpha/lambda/scale 暴露稳定性边界。

Agent 与算法：TD(lambda) variants，重点比较 fixed step-size 在不同 lambda 和 feature scale 下的表现。

实验变量：alpha、lambda、feature scale。该 proposal 的价值来自 sweep 结构，而不是单个 run。

主要指标：RMSE、weight norm、divergence、TD error。stability boundary 是主要输出。

当前证据：结果目录 `experiments/alberta_core_rl/results/onpolicy_stability_atlas/20260708T160958Z_main`。结果支持固定 alpha 对 feature scale 敏感。

主要风险：如果不和 Output-Controlled TD 主线结合，它只是 atlas，不是完整研究问题。应作为 supporting diagnostic。

### B11. GVF Question Design 详细卡片

核心定位：这是 GVF 方向最重要的设计诊断之一。

RL problem：agent 学多个 GVF question，但这些 question 的预测误差和 control usefulness 可能不一致。

Agent 与算法：多个 GVF learner 在线更新不同 cumulants/questions；用 downstream cue relevance 或 utility proxy 评估是否真的有用。

实验变量：cumulant/question 类型、prediction horizon、hidden cue relevance。实验目标是区分 easy prediction 和 useful prediction。

主要指标：GVF prediction error、cue relevance、downstream utility proxy。低 error 但低 utility 是关键反例。

当前证据：结果目录 `experiments/alberta_core_rl/results/gvf_question_design/20260708T160958Z_main`。结果支持“prediction accuracy 不等于 useful state”的判断。

主要风险：utility proxy 仍然间接；最终需要在 T-maze control task 中验证某个 GVF question 是否提高 trial accuracy。

### B12. Nonstationary Bandit Sanity Check 详细卡片

核心定位：这是最小 continual-learning sanity check，已降级。

RL problem：nonstationary bandit reward means change over time；agent 需要持续选择 action 并跟踪变化。

Agent 与算法：简单 online action-value learner / tracking update。无 state representation，无 bootstrapping control 结构。

实验变量：reward drift/change、step size、seeds。设计足够说明 tracking，但不足以代表 Alberta Plan Core RL 主问题。

主要指标：average reward、regret/tracking error、adaptation after shift。

当前证据：结果目录 `experiments/alberta_core_rl/results/nonstationary_bandit/20260708T160958Z_main`。结果可作为 sanity，但研究深度不足。

主要风险：太 toy，容易被老师质疑不是 course project 级别的 Core RL 研究。只适合作为 introduction 或 appendix。

### B13. Streaming Representation With Auxiliary Prediction 详细卡片

核心定位：这是 auxiliary prediction 是否改善 representation 的负结果诊断。

RL problem：streaming prediction setting 中，agent 同时学主 value prediction 和辅助 next-feature prediction。问题是辅助任务是否真的改善主任务。

Agent 与算法：主 value predictor 加 auxiliary predictor，与无 auxiliary baseline 对比。所有更新在线进行。

实验变量：是否使用 auxiliary representation、feature/prediction target、stream change。当前实验偏小。

主要指标：主 prediction error、auxiliary error、representation diagnostic、recovery after change。关键是主任务是否受益，而不是 auxiliary error 是否下降。

当前证据：结果目录 `experiments/alberta_core_rl/results/streaming_representation/20260708T160958Z_main`。auxiliary next-feature prediction 没有明显改善 value prediction。

主要风险：auxiliary target 可能太弱或与主任务无关。当前只能作为 negative diagnostic，不能说明 auxiliary prediction 一般无用。

## 当前总体判断

最强的研究主线是 Scale-Invariant Continuing Control、Reward-Centered Continuing Sarsa、Output-Controlled TD 和 Continual Dyna With Model Aging。它们的问题清楚、Core-RL 连接强、实验可解释，并且已有非平凡结果。

Predictive State Plasticity、GVF Predictive State、GVF Question Design、Generate-and-Test 和 TIDBD-Lite 共同形成一个 representation / GVF / plasticity 研究群，但当前更多是负结果和 redesign signal。它们有研究价值，但不能强行包装成正结果。

Options、Nonstationary Bandit、Streaming Representation 当前不适合作为强提交主线。它们可以作为 appendix、negative result 或 future work。

## 下一步建议

1. 当前真正未完成的重点不再是 Output-Controlled TD extended run、Scale-Invariant fixed-condition grid 或 Output-Controlled TD fairness audit；这三项已经完成并纳入 evidence。接下来需要处理的是 Reward-Centered sensitivity 和 Dyna drift 两个仍在运行的 rerun，以及 Output-Controlled TD 的 no-reset feature-scale switch、Scale-Invariant 的 gradual unit drift。`reward_centered_sarsa`、`output_controlled_td`、`output_controlled_td_fairness_audit`、`scale_invariant_continuing_control`、`continual_dyna_model_aging`、`dyna_planning_budget`、`predictive_state_plasticity` 和 `unit_switching_continuing_control` 已有 extended evidence，后续重点是分析深化和图表/报告一致性。
2. 对 report 继续做中文/英文双语梳理，确保每个 report 单独打开就能看懂环境、agent、指标、结果和结论。
3. 对 Predictive State Plasticity 先做 stronger oracle-prediction control 和 cue information metric，再决定是否接入 generate-and-test/TIDBD。
4. 对 Options 先修 fixed-goal sanity case；如果 fixed-goal 都不成立，不继续讨论 transfer。
5. CPU task 通道已经重新验证：旧的 `core-rl-infra-smoke-968081` 和 `core-rl-output-extended-131257-78853482` 使用过强节点约束，已停止；修正后的 `core-rl-cpu-smoke-fixed-50275254` 在 `ailab-safethm/safethm_cpu_task` 成功跑完整个 smoke suite。Output-Controlled TD extended run `core-rl-output-extended-fixed-46602102` 已成功完成，目标结果目录 `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended` 已写出标准 artifacts；由于目录不可写，report figures 放在正式报告目录。
