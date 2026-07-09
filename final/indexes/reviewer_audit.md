# Reviewer Audit And Action Log

This log records the current multi-reviewer critique cycle for the Core-RL project. It is not a replacement for proposal reports; it tracks what was criticized, what was changed, and what still needs work.

## Review Cycle: 2026-07-09

### Strict Core-RL Reviewer

Main critique: the strongest reports were still written around 5-seed, 5000-step pilot evidence, while several conclusions used language stronger than the evidence justified. The reviewer recommended demoting current results to pilot evidence until extended sweeps are available.

Action taken: extended local runs were launched for `reward_centered_sarsa`, `output_controlled_td`, `predictive_state_plasticity`, `continual_dyna_model_aging`, `dyna_planning_budget`, and `unit_switching_continuing_control`. `dyna_planning_budget` completed first and was renamed to an `_extended` result directory after verifying that it came from `config_extended.json`.

Main critique: `scale_invariant_continuing_control` needs an in-stream unit-change experiment, not only separate fixed-condition sweeps.

Action taken: a new runner `unit_switching_continuing_control` was implemented. It changes reward origin and/or feature scale halfway through a continuing access-control stream without resetting weights. The smoke config passed; the extended config is running.

Main critique: `continual_dyna_model_aging` should claim stale-backup reduction more strongly than reward superiority unless reward recovery becomes robust.

Action taken: report updates will frame Dyna evidence around stale planning diagnostics and recovery windows. The completed `dyna_planning_budget` extended run confirms that keep-model planning can retain stale backups after change even when late reward recovers.

Main critique: `predictive_state_plasticity` is a valuable negative/redesign gate, not a positive final candidate yet.

Action taken: future report edits will keep this framing. The extended run now adds maze length `30`, but the criterion remains whether learned predictive state beats or approaches trace/oracle memory, not whether it merely has nonzero cue alignment.

### Reproducibility And Report-Quality Reviewer

Main critique: Chinese `report_zh.md` files are short quick-review notes, not true counterparts to the English reports, and they do not include figures.

Action pending: expand final-facing Chinese reports so they mirror the English report structure, including motivation, environment, methods, experimental design, results, threats, critique response, figures, and reproduction commands.

Main critique: `proposal_overview.md` was much shorter than `proposal_overview_zh.md`.

Action taken: both overview files now include a dedicated RL environment catalogue explaining each environment's state/observation, actions, reward/nonstationarity, and research role.

Main critique: integrated reports show report-ready figures, but reproduction sections do not include `plot_report_figures.py` commands.

Action pending: add figure regeneration commands to integrated report reproduction sections and the Chinese counterparts.

Main critique: `config_extended.json` outputs were confusing because they used `suite: main` and therefore created `_main` directories.

Action taken: `run_proposal` now labels outputs from `config_extended.json` with `_extended` while preserving `suite: main` for runner logic. Older runs launched before this patch are renamed after verification.

## Current Open Items

- Finish all launched extended runs and extract seed-tail summaries.
- Run or decide scope for `scale_invariant_continuing_control/config_extended.json`; it is the largest sweep and should be scheduled after current jobs finish.
- Update English reports with executed extended evidence and more conservative claims.
- Expand Chinese reports into true counterparts, including figures.
- Update `final/indexes/results.md`, `results_zh.md`, `reproduction.md`, and `reproduction_zh.md` with new result paths and commands.
- Re-run markdown pairing and figure-link checks.
