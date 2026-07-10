# Reviewer Audit And Action Log

This log records the current multi-reviewer critique cycle for the Core-RL project. It is not a replacement for proposal reports; it tracks what was criticized, what was changed, and what still needs work.

## Review Cycle: 2026-07-09

### Strict Core-RL Reviewer

Main critique: the strongest reports were still written around 5-seed, 5000-step pilot evidence, while several conclusions used language stronger than the evidence justified. The reviewer recommended demoting current results to pilot evidence until extended sweeps are available.

Action taken: extended runs were launched for `reward_centered_sarsa`, `output_controlled_td`, `predictive_state_plasticity`, `continual_dyna_model_aging`, `dyna_planning_budget`, and `unit_switching_continuing_control`. Completed extended evidence has been incorporated or indexed for Reward-Centered Sarsa, Output-Controlled TD, Dyna Planning Budget, Continual Dyna Model Aging, Predictive State Plasticity, and Unit-Switching Continuing Control. Output-Controlled TD completed as CPU task `core-rl-output-extended-fixed-46602102`.

Main critique: `scale_invariant_continuing_control` needs an in-stream unit-change experiment, not only separate fixed-condition sweeps.

Action taken: a new runner `unit_switching_continuing_control` was implemented. It changes reward origin and/or feature scale halfway through a continuing access-control stream without resetting weights. The smoke config and 20-seed extended config have completed, and the result is incorporated into the Scale-Invariant Continuing Control report.

Main critique: `continual_dyna_model_aging` should claim stale-backup reduction more strongly than reward superiority unless reward recovery becomes robust.

Action taken: report updates will frame Dyna evidence around stale planning diagnostics and recovery windows. The completed `dyna_planning_budget` extended run confirms that keep-model planning can retain stale backups after change even when late reward recovers.

Main critique: `predictive_state_plasticity` is a valuable negative/redesign gate, not a positive final candidate yet.

Action taken: future report edits will keep this framing. The extended run now adds maze length `30`, but the criterion remains whether learned predictive state beats or approaches trace/oracle memory, not whether it merely has nonzero cue alignment.

### Reproducibility And Report-Quality Reviewer

Main critique: Chinese `report_zh.md` files started as short quick-review notes, not true counterparts to the English reports, and several reports still need stronger content matching.

Action taken: Chinese reports have been expanded substantially from quick-review notes, and many now include motivation, RL setting, method, experiment design, results, interpretation, threats, critique response, figures where available, and reproduction commands. This is not yet a completed consistency guarantee: the next revision must check each English/Chinese pair for matching result paths, claims, limitations, figures, and Proposal Template answers.

Main critique: `proposal_overview.md` was much shorter than `proposal_overview_zh.md`.

Action taken: both overview files now include a dedicated RL environment catalogue explaining each environment's state/observation, actions, reward/nonstationarity, and research role.

Main critique: integrated reports show report-ready figures, but reproduction sections do not include `plot_report_figures.py` commands.

Action taken: figure regeneration commands were added to the updated integrated reports where report figures are used, and the reproduction indexes now include report-figure commands. `dyna_planning_budget` also received new readable average-reward and stale-backup plots from the 20-seed extended run.

Main critique: `config_extended.json` outputs were confusing because they used `suite: main` and therefore created `_main` directories.

Action taken: `run_proposal` now labels outputs from `config_extended.json` with `_extended` while preserving `suite: main` for runner logic. Older runs launched before this patch are renamed after verification.

### Latest Multi-Role Follow-Up

Main critique: Output-Controlled TD had inconsistent evidence status. English and Chinese reports could be read as implying that extended evidence was available, while the actual `20260709T051934Z_extended` directory was incomplete at the time.

Action taken: CPU task `core-rl-output-extended-fixed-46602102` has now succeeded, and `20260709T051934Z_extended` contains the standard artifacts. Output-Controlled TD reports, result indexes, reproduction notes, and figures have been updated to use this extended evidence. Divergence is now summarized as a seed-level event rate.

Main critique: Dyna aging report figures silently dropped the `half_life` dimension.

Action taken: `plot_report_figures.py` was split into smaller modules and the Dyna aging report figures now include separate legend entries for aging half-lives. Captions explicitly say the plots are by planning budget, model mode, and half-life.

Main critique: several report figures were overloaded learning-curve plots rather than publication-quality evidence.

Action taken: report-ready summary figures were added for Output-Controlled TD, Reward-Centered Sarsa, On-policy Stability Atlas, Dyna Planning Budget, Unit-Switching Continuing Control, Scale-Invariant Continuing Control, Dyna Aging, Predictive State Plasticity, and Useful Predictive Knowledge. Reports now prefer heatmaps or tail-summary figures over old spaghetti plots where current data support them.

Main critique: Predictive State Plasticity sounded broader than the evidence supported.

Action taken: the report now states that the current submission-grade evidence is a 20-seed first-gate negative result. Generate-and-test, TIDBD, and feature replacement are staged future work, not completed positive evidence.

Main critique: incomplete result directories could be mistaken for evidence.

Action taken: `experiments/alberta_core_rl/results/README.md` now lists known incomplete directories and separately lists current extended evidence. The completed rjob-created Output directory is noted as evidence, with report-ready figures stored in the report folder because the result directory is not writable from the normal shell.

Main critique: the requirement audit and status documents still overclaimed completion after the user explicitly asked for a stricter check against the original requirements.

Action taken: `final/indexes/requirements_audit.md` and `final/indexes/status.md` have been rewritten in a conservative gap-tracking form. They now distinguish structural coverage from completed research depth and record weak/quarantined proposals honestly. After later CPU completions, Scale-Invariant, Reward Sensitivity, Output Fairness, and Dyna Drift were upgraded from running/status records to completed evidence.

Main critique: even after the indexes were corrected, the formal reports themselves still lacked explicit Proposal Template answers, independent research scope, evidence level, experiment-design rationale, and per-proposal critique records.

Action taken: all 17 English reports and all 17 Chinese reports now include the required structural sections. Strong proposals were framed as strong with remaining experiments; weak proposals were explicitly marked as supporting, negative, dropped, or quarantined. The structural audit is recorded in `final/indexes/report_section_audit.md`.

### Parallel Independence And Overclaiming Audit

Main critique: a read-only parallel audit found no high-impact cross-report dependency, but it did find several remaining overclaiming risks. `GVF Predictive State` claimed that the learned GVF failed to carry cue information even though that report lacks a direct cue-decodability probe. `Nonstationary Bandit` used "confirms" language despite five seeds and wide uncertainty. `Reward-Centered Sarsa` and `Scale-Invariant Continuing Control` used "necessary" language that sounded broader than the tested access-control grids. `Predictive State Plasticity` still mentioned limited-budget replacement and feature-wise plasticity often enough that they could be mistaken for current evidence rather than future work.

Action taken: the relevant English and Chinese reports were revised. `GVF Predictive State` now states that the recurrent GVF does not become usable control state, while direct cue information remains unmeasured in that pilot. `Nonstationary Bandit` now uses "suggests" and "sanity-check observation" language. `Reward-Centered Sarsa` and `Scale-Invariant Continuing Control` now restrict their strongest wording to the tested access-control variants and combinations. `Predictive State Plasticity` now states that limited-budget replacement, generated traces, and feature-wise step-size adaptation are future-work mechanisms and not evidence for the current fixed predictive-state gate.

## Current Open Items

- Deepen the newly added Proposal Template/evidence/reviewer sections where they change scientific decisions; the first structural pass is complete, but not every report is paper-perfect.
- Continue the Output-Controlled TD follow-up after the completed fairness audit and max-stable-alpha frontier: add a more principled true-online TD(lambda) output-control derivation and a no-reset feature-scale switch experiment.
- Continue the Scale-Invariant follow-up after the completed fixed-condition grid: add gradual unit drift, recovery AUC, and policy-distance probes.
- Continue Reward-Centered beyond the completed beta/gamma/no-reset switch and early recovery score with matched-seed recovery analysis, policy-distance probes, and natural reward drift.
- Continue Dyna aging beyond the completed abrupt/gradual/stochastic drift sweep and reward/staleness frontier with repeated changes and true per-backup planning-utility logging.
- Add true-online TD(lambda) max-stable-alpha audit before treating that baseline as a strong negative comparison.
- Continue Useful Predictive Knowledge beyond the completed feature-budget gate with oracle-prediction scaling, GVF-output normalization, prediction-to-policy coupling, downstream-control ablations, and then plasticity stages before attempting a positive GVF predictive-state claim.

## Verification After This Revision

- Markdown image-link check passed for all files under `final/`.
- Report-image check passed for `final/reports/**/report*.md` with zero missing images after this repair pass.
- All 17 English `report.pdf` files were regenerated after the latest edits, with `missing_images=0` in `final/indexes/english_report_pdf_manifest.json`.
- `python -m compileall experiments/alberta_core_rl` completed without errors.
- Generated `__pycache__` directories were not fully cleaned: two directories under `experiments/alberta_core_rl/` are owned by `nobody:nogroup`, and normal-user cleanup fails with permission denied.
- Python source files remain under the 500-line guidance after splitting report plotting utilities; `envs.py` is the largest at 474 lines.
