# Core RL Course Project

This repository contains a Core-RL course project centered on the Alberta Plan. The project studies small online agents that learn continually from ordinary experience, with no replay buffer, no deep network, and no offline training loop. The current work emphasizes continuing control, average reward, reward centering, output-controlled TD updates, learned models, Dyna planning, GVFs, feature utility, and partial observability.

## Where To Start

Start with `final/` if you want to review the project as a course deliverable. The most useful entry points are `final/proposal_overview_zh.md` for a detailed Chinese overview, `final/proposal_overview.md` for the English overview, `final/reports/` for standalone proposal reports, and `final/indexes/results.md` plus `final/indexes/reproduction.md` for evidence and exact commands.

Start with `experiments/alberta_core_rl/` if you want to run or inspect code. The experiment package contains proposal-specific runners, configs, generated results, plotting scripts, and small tabular/linear environments. The top-level `experiments/` directory is only a workspace; the Python package is `alberta_core_rl`.

## Repository Layout

- `AlbertaPlan.pdf`, `RL_Course_Project.pdf`, `Proposal_Template.md`: original course and framing materials.
- `resources/`: imported papers, course notes, class materials, and related references. Imported resources should not be edited.
- `draft/`: planning notes, rough research material, and intermediate work.
- `experiments/alberta_core_rl/`: runnable online Core-RL experiments, configs, result directories, and plotting/summarization scripts.
- `final/`: final-facing reports, proposal overviews, indexes, archive notes, and presentation material.
- `conda-env-configs/`: environment records for reproducing the Python setup.

## Current Strong Proposal Lines

The strongest current line is `Scale-Invariant Continuing Control`, a larger independent continuing-control study that combines reward centering and output-controlled Sarsa in access-control. The main scientific question is whether an online control agent can stay stable when arbitrary reward origins and feature units change.

The strongest planning line is `Continual Dyna With Model Aging`, which asks when a learned model entry should still be trusted for planning after the environment changes. The most reliable current signal is stale-backup reduction, not simple reward superiority.

`Reward-Centered Continuing Sarsa` and `Output-Controlled TD` are strong independent mechanism studies. `Predictive State Plasticity` is currently a valuable negative/redesign gate: learned GVF state remains near chance in T-maze control while trace/oracle memory works.

## Running Experiments

Use the dedicated conda environment rather than base:

```bash
PYTHONNOUSERSITE=1 MPLCONFIGDIR=/mnt/shared-storage-user/yupeng/Core-RL/.mplconfig \
  /data/yupeng/conda_envs/core-rl/bin/python experiments/alberta_core_rl/scripts/run_experiment.py \
  --config experiments/alberta_core_rl/configs/reward_centered_sarsa/config_main.json
```

Extended runs use `config_extended.json` when available. Outputs from extended configs are labeled with `_extended` in new runs. Older extended runs launched before this labeling change may have been manually renamed after verifying `config_used.json`.

## Reports And Indexes

Each standalone proposal should be readable by opening its own `report.md`. Important final-facing documents should have matching English and Chinese versions. Current bilingual coverage is tracked in `final/indexes/bilingual_coverage.md` and `final/indexes/bilingual_coverage_zh.md`.

The current review cycle is tracked in `final/indexes/reviewer_audit.md`, `final/indexes/status.md`, and their Chinese counterparts. These files record reviewer criticisms, actions already taken, open CPU jobs, generated PDFs, and pending extended results.

## Project Constraints

The project deliberately stays within Core RL. It uses streaming online updates, tabular or linear function approximation, CPU-scale experiments, explicit seeds, and result directories with `manifest.json`, `config_used.json`, `summary.json`, `condition_summary.json`, and `metrics.csv`. Do not introduce replay buffers, deep networks, or offline training unless the project scope is explicitly changed.
