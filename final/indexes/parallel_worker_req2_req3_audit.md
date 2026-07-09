# Parallel Worker Audit: Requirements 2 and 3

Date: 2026-07-09

Scope: audit only requirements 2 and 3 from `final/indexes/revise_plan_20260709.md` and `final/indexes/revise_plan_20260709_zh.md`. This file does not revise existing reports.

## Verdict

| Requirement | Verdict | Short reason |
|---|---|---|
| 2. Combine existing directions into larger meaningful independent research questions, without forcing patchwork combinations. | Partially done. | Three integrated proposals exist and two are coherent larger studies, but the representation/GVF/plasticity line is still mostly a negative gate plus separate diagnostics. Some ordinary proposals remain appendices or weak pilots rather than parts of a mature larger question. |
| 3. Deeply understand Alberta Plan Core RL issues and propose a more comprehensive, larger, well-motivated independent proposal with concrete research questions and richer experiments. | Partially done, weak. | Alberta Plan language is present, and the revise plan names `Useful Predictive Knowledge Under Partial Observability and Resource Limits`, but that larger proposal is not yet a full report, experiment plan, or implemented package. Current integrated reports are good starts, not a new comprehensive Alberta-Plan-level proposal. |

## Evidence From Current Materials

The revise plan is honest about the state. It says requirement 2 currently has three integrated proposals, but the gap is that they are not all paper-depth and the weak representation line has not yet been organized into a coherent larger topic. It also says requirement 3 has Alberta Plan framing and literature lists, but literature has not been woven deeply into motivation and experiment design. The execution tracker explicitly marks the new predictive-knowledge large topic as "Planned only."

`final/proposal_overview.md` confirms the current hierarchy. It strongly recommends `Scale-Invariant Continuing Control`, `Continual Dyna With Model Aging`, `Reward-Centered Continuing Sarsa`, and `Output-Controlled TD`. It treats `Predictive State Plasticity` as high-risk negative gate evidence, and says GVF Predictive State, GVF Question Design, Generate-and-Test, TIDBD-Lite, Streaming Representation, and related reports need redesign before they become strong final topics.

The integrated reports show real progress:

- `final/reports/integrated/scale_invariant_continuing_control/report.md` is a coherent larger question: reward-origin and feature-unit invariance in one continuing access-control control problem. It has completed fixed-condition and no-reset unit-switch evidence, and it explicitly limits the claim to stability rather than solved invariance.
- `final/reports/integrated/continual_dyna_model_aging/report.md` is a coherent planning question: when should a continual Dyna agent trust learned model entries after change? It has 20-seed abrupt-change evidence, model freshness diagnostics, and a pending drift extension.
- `final/reports/integrated/predictive_state_plasticity/report.md` is valuable but incomplete as a larger proposal. It is explicitly a 20-seed first-gate negative study: cue-GVF features carry weak cue information but do not improve control. It says feature replacement, feature-wise plasticity, phase switches, oracle-prediction control, and output normalization are future stages.

The ordinary reports support the same conclusion:

- `reward_centered_sarsa` and `output_controlled_td` are strong standalone mechanisms and already feed the scale-invariant integrated direction.
- `dyna_planning_budget` is a strong diagnostic precursor to model aging, but not itself the full search-control proposal.
- `gvf_predictive_state`, `gvf_question_design`, `generate_test_features`, `tidbd_plasticity`, and `streaming_representation` share a natural theme, but current evidence is fragmented: several are five-seed pilots, negative diagnostics, or planned usefulness probes.
- `baird_offpolicy_stability` is an important GVF/off-policy warning, but it remains a Baird-style pilot and not yet integrated into a coherent off-policy predictive-knowledge program.
- `options_reusable_subtasks` is quarantined. It should not be used as part of a larger proposal unless a fixed-goal SMDP sanity gate passes.

The Alberta Plan materials support a sharper standard. `AlbertaPlan.pdf` emphasizes ordinary experience, temporal uniformity, limited computation, online continual sensing and acting, value functions, learned transition models, planning, search control, average reward, GVFs, feature finding, options, and Oak-style utility assessment. The local conversation note similarly frames the course project around small Core RL modules: continuing average-reward control, GVF predictive state, feature finding, TIDBD, Dyna/search control, off-policy stability, options, and utility evaluation. Current reports touch many of these pieces, but only some are tied into larger research questions.

## Gaps And Risks

1. The current integrated set is uneven. Scale-Invariant Control and Dyna Model Aging are coherent. Predictive State Plasticity is more of a negative gate than a mature integrated research program.

2. The representation line risks becoming a patchwork. GVF Predictive State, GVF Question Design, Generate-and-Test, TIDBD-Lite, Streaming Representation, and Baird Stability all relate to useful predictions and state construction, but they currently live as separate diagnostics with different environments and evidence levels. They need one primary question and one environment family before they should be called a larger proposal.

3. Requirement 3 is not satisfied by citing Alberta Plan concepts. A stronger Alberta Plan proposal must choose one base-agent problem, then design experiments around it. Listing GVFs, feature finding, planning, options, average reward, and off-policy stability together is not enough.

4. Some proposed combinations would be forced. Doorway Options should stay quarantined until SMDP accounting and fixed-goal sanity pass. Nonstationary Bandit should remain a sanity check. Centered TD Diagnostics and On-Policy Stability Atlas are useful appendices, not main pillars.

5. Current evidence is not balanced across candidates. Invariance and Dyna have 20-seed extended evidence. Representation/plasticity has one stronger predictive-state extended run, but several supporting pieces are still five-seed pilots or planned analyses.

## Larger Proposal Candidates

### Candidate 1: Useful Predictive Knowledge Under Partial Observability And Resource Limits

Motivation: Alberta Plan predictive knowledge is only valuable if predictions become useful state, not just low-error auxiliary targets. The current reports already show the central failure: cue-GVF carries weak cue information but does not improve T-maze control, and generic auxiliary prediction or generate-and-test features do not automatically help.

Focused RL question: When does a learned prediction become a usable state feature for online control under partial observability and limited feature budget?

Environment/testbed: One environment family, not many unrelated tasks: T-maze cue stream plus a trace-conditioning delayed-cue stream. Both have an early signal that must be retained until a later prediction or control decision. Use the T-maze as the main control testbed and the trace-conditioning stream as the feature-budget diagnostic.

Algorithms/baselines: raw observation, short history, hand-coded trace memory, oracle memory, cue-GVF, recurrent GVF, normalized cue-GVF, oracle-prediction feature, generate-and-test trace features with downstream-loss utility, TIDBD/AutoStep only after the fixed predictive feature passes a utility gate.

Experiment design:

- Gate 1: cue decodability and control accuracy for raw/history/trace/oracle/GVF features across maze lengths.
- Gate 2: GVF question and horizon ablations; compare cue, junction, reward, and bias cumulants by decodability and control, not only TD error.
- Gate 3: output-scale and control-utilization audit; test whether normalized GVF outputs or oracle-prediction features become usable by Sarsa.
- Gate 4: limited feature budget with delay switches; compare fixed traces, random replacement, generate-and-test utility tied to downstream TD-error reduction, and canonical TIDBD/AutoStep.

Metrics: trial accuracy, unshifted reward, cue-decoding accuracy, hidden-cue mutual-information proxy, GVF TD error, downstream value loss with feature ablations, recovery AUC after cue/delay switches, feature survival/replacement count, per-feature alpha trajectories.

Expected insight: Prediction accuracy is not sufficient. A useful predictive feature must be informative about the hidden variable, scaled so control can use it, and retained under a feature budget. A negative result is still strong if it identifies which gate fails.

Why it is not patchwork: All components answer one question: how an online agent constructs useful state from predictions under partial observability. Generate-and-test and TIDBD are not separate add-ons; they enter only as capacity/plasticity mechanisms after the useful-prediction gate.

### Candidate 2: Unit-Robust Continuing Control Under Changing Measurement Conventions

Motivation: A temporally uniform continuing agent should not depend on arbitrary reward zero-points or feature units. Current `Reward-Centered Sarsa`, `Output-Controlled TD`, `Centered TD Diagnostics`, `On-Policy Stability Atlas`, and `Scale-Invariant Continuing Control` already form a coherent invariance family.

Focused RL question: Can a small online continuing-control agent keep stable values and behavior when reward origin and feature scale change, including changes inside the same stream without reset?

Environment/testbed: Continuing access-control queue as the main control task, plus tile-coded random walk only as the prediction-side update-unit diagnostic. The access-control queue should remain the central environment for final claims.

Algorithms/baselines: discounted Sarsa, reward-centered Sarsa, differential Sarsa, normalized Sarsa, normalized reward-centered Sarsa, normalized differential Sarsa, trace-normalized variants, and a carefully bounded true-online audit for prediction.

Experiment design:

- Fixed-condition grid over reward shifts, feature scales, and alphas.
- No-reset reward-origin switch and no-reset feature-scale switch in a single continuing stream.
- Gradual feature-unit drift and gradual reward-origin drift.
- Beta/gamma sensitivity for reward baseline adaptation.
- Policy-distance probes over all access-control states, not just average reward.

Metrics: unshifted average reward, Q norm, TD-error scale, output-change magnitude, divergence rate, accept-probability policy distance, high-priority accept rate, reward-baseline tracking error, recovery AUC after unit switches.

Expected insight: Reward centering and output normalization solve different nuisance-unit failures. Their composition is meaningful because arbitrary reward and feature units interact through TD-error scale and update size. The open problem is online recalibration after abrupt or gradual unit change.

Why it is not patchwork: The whole proposal is about one invariance principle: equivalent descriptions of the same continuing task should not require retuning. Reward centering, differential learning, and output control are separate mechanisms for one unit-robustness question.

### Candidate 3: Freshness-Aware Planning And Search Control In Continual Dyna

Motivation: Alberta Plan planning is continual and budget-limited. A learned model is useful only if the agent allocates planning computation to entries that still describe the current world. Current Dyna Planning Budget and Continual Dyna Model Aging already support this line.

Focused RL question: Under limited per-step planning computation, how should a continual Dyna agent decide which learned model entries still deserve simulated backups after the world changes?

Environment/testbed: Changing continuing gridworld as the inspectable primary setting, with an added stochastic/gradual drift version and optional repeated layout switches. Keep all experiments online with a compact learned model, not replay.

Algorithms/baselines: no planning, keep-model random Dyna, oracle flush diagnostic, recency aging, recency/error gating, TD-priority search control, stale-error-priority search control, and possibly small-backup/prioritized-sweeping variants if implementation remains simple.

Experiment design:

- Budget x model-handling sweep over planning budgets `0/1/5/20`.
- Half-life sweep for recency aging and recency/error gating.
- Abrupt, gradual, stochastic, and repeated nonstationarity.
- Planning utility table: reward improvement or value-target improvement per simulated backup.
- Model-entry audit by age, recent error, visitation, and stale-backup label.

Metrics: average reward, pre-change AUC, post-change recovery AUC/time, stale-backup rate, model one-step error, planning TD magnitude, planning utility per backup, fraction of planning spent on recently observed entries, model size.

Expected insight: More planning is not the real variable. The real variable is search control under model freshness uncertainty. A useful result can be a tradeoff map, not one universally best half-life.

Why it is not patchwork: Dyna budget, model aging, and search control are all parts of one learned-model computation-allocation question. The proposal does not need options unless temporally abstract model entries are introduced later as a separate extension.

### Candidate 4: Oak-Lite Utility Gates For Learned Agent Components

Motivation: Alberta Plan Step 11, Oak, asks the agent to continually assess the utility of features, subtasks, options, and option models. This is the most comprehensive candidate, but also the highest risk for a three-week course project.

Focused RL question: Can a small online agent use explicit utility gates to decide which learned components deserve capacity or computation?

Environment/testbed: Do not mix all current environments. Use one controlled continuing gridworld with partial observability and a change point, or split into two clearly staged tasks: T-maze for feature/prediction utility and changing gridworld for model/planning utility.

Algorithms/baselines: fixed components, random replacement/sampling, oracle diagnostic, utility-gated prediction features, utility-gated model entries, and only later utility-gated options after the options sanity gate passes.

Experiment design: Start with features and model entries only. Compare utility rules based on downstream TD-error reduction, cue decodability, model error, recency, and planning benefit. Add subtasks/options only if fixed-goal SMDP sanity passes.

Metrics: downstream reward or accuracy, component utility score calibration, replacement/deletion count, recovery AUC, planning utility per backup, feature ablation loss, computation spent on useful versus stale components.

Expected insight: The Alberta Plan's broad Oak idea can be made empirical by asking whether component utility scores predict downstream contribution. The most likely useful result is a set of gate criteria and failure modes, not a complete Oak agent.

Why it is not patchwork: It is unified by utility assessment. However, it is only non-patchwork if the first version restricts itself to one or two component types. Including GVFs, generate-and-test, TIDBD, Dyna, options, and off-policy learning all at once would become patchwork.

## Prioritized Recommendation

1. Implement next: Candidate 1, `Useful Predictive Knowledge Under Partial Observability And Resource Limits`, but only as a staged report skeleton plus Gate 1 and Gate 2 experiments first. This is the clearest unmet requirement 3 target because the revise plan already names it but has not turned it into a full independent proposal. It also organizes the most fragmented current materials into one legitimate larger question.

2. Preserve and deepen, not rebuild: Candidate 2. `Scale-Invariant Continuing Control` is already strong and mostly satisfies requirement 2. The next implementation should be gradual feature/reward drift plus recovery AUC and policy-distance probes, not another broad fixed grid.

3. Continue after pending artifacts: Candidate 3. `Continual Dyna Model Aging` is coherent and strong, but the drift extension should be incorporated only after standard artifacts exist. The next design addition should be planning utility per backup and repeated/non-clean changes.

4. Defer: Candidate 4. Oak-lite is the deepest Alberta Plan connection, but it is too broad unless narrowed sharply. It should influence framing and reviewer critique, not become the immediate implementation target.

Immediate main-agent action: create a full report skeleton for Candidate 1 under `final/reports/integrated/useful_predictive_knowledge/` only if the user permits adding a new integrated report. Before code, write its proposal-template answers, staged gates, success/failure criteria, and exact links to existing reports. Then implement the smallest Gate 1/2 diagnostic that can reuse the existing T-maze runner: cue-decoding plus GVF question/horizon ablations with trial accuracy, cue decodability, and GVF TD error in the same condition summary.
