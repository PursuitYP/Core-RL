# Reviewer Audit And Action Log

This log records the current multi-reviewer critique cycle for the Core-RL project. It is not a replacement for proposal reports; it tracks what was criticized, what was changed, and what still needs work.

## Review Cycle: 2026-07-09

### Strict Core-RL Reviewer

Main critique: the strongest reports were still written around 5-seed, 5000-step pilot evidence, while several conclusions used language stronger than the evidence justified. The reviewer recommended demoting current results to pilot evidence until extended sweeps are available.

Action taken: extended runs were launched for `reward_centered_sarsa`, `output_controlled_td`, `predictive_state_plasticity`, `continual_dyna_model_aging`, `dyna_planning_budget`, and `unit_switching_continuing_control`. Completed extended evidence has been incorporated for Reward-Centered Sarsa, Dyna Planning Budget, Continual Dyna Model Aging, Predictive State Plasticity, and Unit-Switching Continuing Control. Output-Controlled TD is now running as CPU task `core-rl-output-extended-fixed-46602102` after a successful CPU smoke validation.

Main critique: `scale_invariant_continuing_control` needs an in-stream unit-change experiment, not only separate fixed-condition sweeps.

Action taken: a new runner `unit_switching_continuing_control` was implemented. It changes reward origin and/or feature scale halfway through a continuing access-control stream without resetting weights. The smoke config and 20-seed extended config have completed, and the result is incorporated into the Scale-Invariant Continuing Control report.

Main critique: `continual_dyna_model_aging` should claim stale-backup reduction more strongly than reward superiority unless reward recovery becomes robust.

Action taken: report updates will frame Dyna evidence around stale planning diagnostics and recovery windows. The completed `dyna_planning_budget` extended run confirms that keep-model planning can retain stale backups after change even when late reward recovers.

Main critique: `predictive_state_plasticity` is a valuable negative/redesign gate, not a positive final candidate yet.

Action taken: future report edits will keep this framing. The extended run now adds maze length `30`, but the criterion remains whether learned predictive state beats or approaches trace/oracle memory, not whether it merely has nonzero cue alignment.

### Reproducibility And Report-Quality Reviewer

Main critique: Chinese `report_zh.md` files are short quick-review notes, not true counterparts to the English reports, and they do not include figures.

Action taken: all `final/reports/**/report_zh.md` files have been expanded from quick-review notes into standalone Chinese review reports with motivation, RL setting, method, experiment design, results, interpretation, threats, critique response, figures where available, and reproduction commands. The strongest reports now have fuller Chinese counterparts; supporting and negative proposals are also written as honest independent studies rather than generic summaries.

Main critique: `proposal_overview.md` was much shorter than `proposal_overview_zh.md`.

Action taken: both overview files now include a dedicated RL environment catalogue explaining each environment's state/observation, actions, reward/nonstationarity, and research role.

Main critique: integrated reports show report-ready figures, but reproduction sections do not include `plot_report_figures.py` commands.

Action taken: figure regeneration commands were added to the updated integrated reports where report figures are used, and the reproduction indexes now include report-figure commands. `dyna_planning_budget` also received new readable average-reward and stale-backup plots from the 20-seed extended run.

Main critique: `config_extended.json` outputs were confusing because they used `suite: main` and therefore created `_main` directories.

Action taken: `run_proposal` now labels outputs from `config_extended.json` with `_extended` while preserving `suite: main` for runner logic. Older runs launched before this patch are renamed after verification.

### Latest Multi-Role Follow-Up

Main critique: Output-Controlled TD had inconsistent evidence status. English and Chinese reports could be read as implying that extended evidence was available, while the actual `20260709T051934Z_extended` directory is still incomplete.

Action taken: Output-Controlled TD reports and indexes now state that the citable evidence is still `20260708T153802Z_main`; CPU task `core-rl-output-extended-fixed-46602102` is running, and `20260709T051934Z_extended` must not be cited until standard artifacts exist.

Main critique: Dyna aging report figures silently dropped the `half_life` dimension.

Action taken: `plot_report_figures.py` was split into smaller modules and the Dyna aging report figures now include separate legend entries for aging half-lives. Captions explicitly say the plots are by planning budget, model mode, and half-life.

Main critique: several report figures were overloaded learning-curve plots rather than publication-quality evidence.

Action taken: report-ready summary figures were added for Output-Controlled TD, Reward-Centered Sarsa, On-policy Stability Atlas, Dyna Planning Budget, Unit-Switching Continuing Control, Scale-Invariant Continuing Control, Dyna Aging, and Predictive State Plasticity. Reports now prefer heatmaps or tail-summary figures over old spaghetti plots.

Main critique: Predictive State Plasticity sounded broader than the evidence supported.

Action taken: the report now states that the current submission-grade evidence is a 20-seed first-gate negative result. Generate-and-test, TIDBD, and feature replacement are staged future work, not completed positive evidence.

Main critique: incomplete result directories could be mistaken for evidence.

Action taken: `experiments/alberta_core_rl/results/README.md` now lists known incomplete directories. Local old incomplete directories have `INCOMPLETE.md` markers where writable; the active rjob-created Output directory is noted in the README because it is owned by the container user.

## Current Open Items

- Finish the still-running CPU-task extended job: `output_controlled_td/config_extended.json`. The expected result directory is `experiments/alberta_core_rl/results/output_controlled_td/20260709T051934Z_extended`; verify `config_used.json`, `condition_summary.json`, and generated figures before citing it.
- Run or decide scope for `scale_invariant_continuing_control/config_extended.json`; it is the largest fixed-condition sweep and should be scheduled after current jobs finish or moved to a verified CPU-task queue.
- Update `output_controlled_td` result indexes and reports once its extended summary is available; the current reports already mark the extended directory as incomplete.
- Add beta/gamma and midstream reward-origin tests for `reward_centered_sarsa` if the standalone paper is selected as a final topic.
- Add gradual/stochastic drift environments for Dyna aging before making general claims beyond abrupt changing gridworlds.
- Add true-online TD(lambda) max-stable-alpha audit before treating that baseline as a strong negative comparison.
- Add cue-decodability and downstream-control ablations before attempting a positive GVF predictive-state claim.

## Verification After This Revision

- Markdown image-link check passed for all files under `final/`.
- `python -m compileall experiments/alberta_core_rl` completed without errors.
- Generated `__pycache__` directories were cleaned after the compile check.
- Python source files remain under the 500-line guidance after splitting report plotting utilities; `envs.py` is the largest at 474 lines.
