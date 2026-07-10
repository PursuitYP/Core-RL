# Parallel Worker Audit: Requirements 2 and 3, Round 2

Date: 2026-07-09

Scope: audited `final/indexes/revise_plan_20260709.md`, `final/indexes/revise_plan_20260709_zh.md`, `final/reports/integrated/`, `final/proposal_overview*.md`, `final/indexes/results*.md`, and relevant current configs/results. This memo only judges requirements 2 and 3.

## Executive Judgment

Requirement 2: **Partial pass**. The repository now has four larger integrated proposals that are mostly coherent independent studies rather than arbitrary bundles. Two are strong mature studies, and two are coherent representation/GVF gates. The remaining gap is not structure; it is experimental completion, especially for Useful Predictive Knowledge and Predictive State Plasticity.

Requirement 3: **Partial pass**. A stronger Alberta Plan/Core-RL large problem has been proposed and made concrete: useful predictive knowledge under partial observability and resource limits. It has a clear motivation, one environment family, gate metrics, and current evidence. It is not fully satisfied because the resource-limit, feature-budget, prediction-selection, and plasticity stages remain unimplemented, and the literature is still more framing text than experiment-changing design across all four integrated proposals.

Bottom line: the latest updates satisfy the "not patchwork" part better than before, but they do **not** yet satisfy the full "larger deeper proposal with multiple important experiments" requirement. The most valuable next work is a targeted Useful Predictive Knowledge follow-up that separates prediction information, output scaling, policy use, limited feature budget, and plasticity.

## Evidence Checked

- Plan gap source: `final/indexes/revise_plan_20260709.md` and `final/indexes/revise_plan_20260709_zh.md`.
- Integrated navigation: `final/reports/integrated/README.md` and `README_zh.md`.
- Integrated reports:
  - `final/reports/integrated/scale_invariant_continuing_control/report.md`
  - `final/reports/integrated/continual_dyna_model_aging/report.md`
  - `final/reports/integrated/predictive_state_plasticity/report.md`
  - `final/reports/integrated/useful_predictive_knowledge/report.md`
- Overview/indexes: `final/proposal_overview.md`, `final/proposal_overview_zh.md`, `final/indexes/results.md`, `final/indexes/results_zh.md`.
- Relevant implementation/config:
  - `experiments/alberta_core_rl/studies/predictive_state.py`
  - `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json`
  - `experiments/alberta_core_rl/configs/predictive_state_plasticity/config_extended.json`
  - `experiments/alberta_core_rl/configs/scale_invariant_continuing_control/config_extended.json`
  - `experiments/alberta_core_rl/configs/continual_dyna_model_aging_drift/config_extended.json`
- Current result artifacts:
  - `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main`
  - `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended`
  - `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended`
  - `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`
  - `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended`
  - `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`

All six inspected result directories have the standard evidence files: `metrics.csv`, `summary.json`, `condition_summary.json`, `config_used.json`, and `manifest.json`.

## Requirement 2: Larger Meaningful Questions Without Patchwork

Status: **Partial pass**.

### What now passes

The four integrated reports are no longer just old proposals pasted together. Each has a focused RL question, a testbed, a method family, and metrics that connect to the question.

1. **Scale-Invariant Continuing Control: pass.** This is a genuinely coherent larger study. It combines reward centering and output-controlled updates because both address arbitrary units in continuing control. Evidence is strong: fixed-condition extended run at `experiments/alberta_core_rl/results/scale_invariant_continuing_control/20260709T063128Z_extended` plus no-reset unit switch at `experiments/alberta_core_rl/results/unit_switching_continuing_control/20260709T024834Z_extended`. The report correctly narrows the claim: combined centering/normalization improves stability, but abrupt feature-scale recovery is not solved.

2. **Continual Dyna Model Aging: pass.** This is a coherent planning study, not a generic Dyna score comparison. The question is model trust/search-control freshness under nonstationarity. Evidence includes fixed-change half-life/budget results at `experiments/alberta_core_rl/results/continual_dyna_model_aging/20260709T024602Z_extended` and abrupt/gradual/stochastic drift at `experiments/alberta_core_rl/results/continual_dyna_model_aging_drift/20260709T085809Z_extended`. The report now honestly states the conditional result: aging helps under abrupt/gradual high-budget settings, not universally under stochastic drift.

3. **Useful Predictive Knowledge: partial pass.** This is the cleanest new representation framing. It is coherent: one T-maze family, one staged criterion, and metrics for information and control use. Evidence path `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main` supports the current gate: raw observation is near chance, trace/oracle solve the memory problem, and cue-GVFs are above chance for cue decoding but not control-useful. However, the "resource limits" part is still mostly in the title and future-work text.

4. **Predictive State Plasticity: partial pass.** This is an independent high-risk negative gate. It has 20-seed evidence at `experiments/alberta_core_rl/results/predictive_state_plasticity/20260709T024517Z_extended` showing cue-GVF information is weakly decodable but does not solve control. It is coherent as a negative gate, but not yet coherent as a completed "plasticity" study because feature replacement, feature-wise step-size adaptation, phase switches, and limited-budget mechanisms are explicitly future work.

### Remaining Requirement 2 gap

The integrated portfolio is structurally credible, but the two representation proposals still overlap heavily. Both Useful Predictive Knowledge and Predictive State Plasticity are T-maze predictive-state gates. That overlap is acceptable only if the reports preserve different roles:

- Useful Predictive Knowledge should be the main integrated larger proposal about prediction usefulness under partial observability and resource limits.
- Predictive State Plasticity should be either the negative precursor/gate or the staged redesign companion, not a second broad positive proposal.

Current text mostly does this correctly, but the experiments have not yet separated the stages enough. Requirement 2 should remain partial until Useful Predictive Knowledge has at least one implemented resource-limit stage.

## Requirement 3: Deeper Alberta Plan/Core RL and Stronger Large Problem

Status: **Partial pass**.

### What now passes

The project now has a concrete large problem aligned with the Alberta Plan: when should learned predictions become agent state for a continuing/online learner? This is more meaningful than "method X scored higher" because it asks for a necessary gate: information about the hidden variable plus downstream control usefulness.

Evidence from `final/reports/integrated/useful_predictive_knowledge/report.md` and `final/indexes/results.md` supports a useful negative claim:

- Result path: `experiments/alberta_core_rl/results/useful_predictive_knowledge/20260709T102402Z_main`.
- Config: `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json`.
- Scale: 10 seeds, 12,000 online steps, maze lengths `8/12/20`, 36 condition groups, 1,041,120 metric rows.
- Implemented comparisons: raw, trace memory, oracle memory, cue-GVF, terminal-GVF, junction-GVF, with GVF horizons `0.8/0.95/0.99`.
- Key result: best learned cue decoders are above chance (`0.626/0.611/0.638`) but corresponding control accuracies remain near chance (`0.508/0.508/0.495`), while trace/oracle memory are high.

This is a real Core-RL question: online linear learners, no replay, no deep network, partial observability, GVF-style predictive features, and downstream control.

### What does not yet pass

Useful Predictive Knowledge still needs feature-budget and plasticity experiments. This is not a small polishing gap; it is the missing part of the requirement that asks for a larger, more comprehensive proposal with multiple important research questions and experiments.

Evidence:

- `final/reports/integrated/useful_predictive_knowledge/report.md` says feature-selection and plasticity are later natural extensions, and the reviewer table lists feature-budget/plasticity as future work.
- `final/indexes/results.md` labels the current result as a principled negative/control-usefulness gate and lists the next action as feature-budget/plasticity, stronger oracle-prediction control, and cue-information/control-use ablations.
- `experiments/alberta_core_rl/configs/useful_predictive_knowledge/config_main.json` contains only the Gate-1/Gate-2 run.
- `experiments/alberta_core_rl/studies/predictive_state.py` implements `proposal_useful_predictive_knowledge` as length x cumulant x horizon conditions; it does not implement limited feature budgets, selection, oracle-prediction controls, phase switches, generate-and-test, TIDBD, or AutoStep.
- `final/reports/integrated/predictive_state_plasticity/report.md` explicitly says the evidence is not a positive plasticity result and still lacks oracle-prediction control, GVF output normalization, feature ablations, phase switches, limited-budget feature replacement, and fully specified feature-wise step-size adaptation.

The literature connection is also better but not fully deep. The reports cite Alberta Plan, GVFs, useful predictions, agent-state construction, reward centering, intentional updates, and Dyna/search-control, but often as motivation. The strongest integrated reports do explain how sources change the experimental question. The representation reports still need the next experiment to make the Alberta Plan connection operational: which predictions should a resource-limited agent retain and use?

## Most Important Follow-Up Experiments

Priority 1: **Useful Predictive Knowledge oracle-prediction and output-scaling control.**

Run a 20-seed follow-up on the same T-maze lengths using:

- raw observation,
- trace memory,
- oracle memory,
- learned cue-GVF,
- learned cue-GVF with normalized/clipped output before Sarsa,
- oracle-prediction feature that feeds the true cue probability or one-hot cue at the same scale/dimensionality as the GVF output.

Metrics: trial accuracy, decision cue decoding, cue margin, control TD error, GVF output scale, and action-value feature ablation. This is the highest-leverage experiment because it diagnoses whether the current failure is weak information, bad scaling, or control learner non-use.

Priority 2: **Useful Predictive Knowledge limited feature-budget selection.**

After Priority 1, add a feature budget stage with budgets such as `2`, `4`, and `8` learned predictive candidates. Compare:

- fixed hand-selected cue-GVF candidates,
- random prediction selection,
- prediction-error-based selection,
- cue-information/decodability-based selection,
- downstream control-TD contribution or leave-one-feature-out utility.

Metrics: selected feature survival, feature turnover, decision cue decoding, trial accuracy, and post-selection recovery. This directly satisfies the "resource limits" part of the integrated proposal.

Priority 3: **Plasticity only after the useful-signal gate is clear.**

Do not start with TIDBD/AutoStep as the first next run. First prove that a scaled or oracle-like predictive signal can be used by Sarsa. Then add a phase-switch T-maze or delayed-cue stream where the relevant cue mapping or delay changes. Compare fixed alpha, normalized TD, generate-and-test with downstream utility, and canonical TIDBD/AutoStep if implementation time permits. The success criterion should be recovery of cue decodability and trial accuracy, not just visible alpha movement.

Priority 4: **Scale-Invariant gradual feature drift and policy-distance probes.**

This would improve an already strong integrated proposal. Use the existing unit-switching setup but replace abrupt `hundred`-scale switches with gradual drift. Add recovery AUC and accept-probability policy-distance probes over access-control states. This would turn the current "stable but incomplete recovery" conclusion into a sharper continual-learning result.

Priority 5: **Dyna repeated changes and planning-utility per backup.**

This would improve the strongest planning proposal. Add repeated layout changes and a table of planning utility per simulated backup by budget, half-life, and drift type. This is lower priority than Useful Predictive Knowledge because Dyna already satisfies requirements 2 and 3 better than the representation line.

## Recommended Pass/Partial/Fail Labels

| Item | Label | Reason |
|---|---|---|
| Four integrated proposals are coherent independent studies | **Partial pass** | Scale-Invariant and Dyna pass strongly; Useful Predictive Knowledge is coherent but only Gate-1/Gate-2; Predictive State Plasticity is coherent as a negative gate, not as completed plasticity. |
| Integrated proposals are not patchwork | **Mostly pass** | Each report now has one main question and one environment family or mechanism family. Representation proposals still need clearer separation to avoid duplication. |
| Useful Predictive Knowledge as stronger large Alberta Plan/Core-RL proposal | **Partial pass** | The framing is strong and evidence is real, but resource-limit, feature-budget, prediction-selection, and plasticity stages are missing. |
| Requirement 2 overall | **Partial pass** | Larger coherent studies exist, but the newest large representation study is not experimentally complete. |
| Requirement 3 overall | **Partial pass** | The larger problem is proposed and partly tested, but the full deeper program is still future work. |

## Final Recommendation

Treat the latest updates as a successful structural revision plus a completed first evidence gate, not as final satisfaction of requirements 2 and 3. The next CPU budget should go first to Useful Predictive Knowledge oracle-prediction/output-scaling and limited feature-budget experiments. Those runs would most directly convert the current negative gate into the larger coherent Alberta Plan study requested by requirement 3.
