# Agent Instructions

Scope: applies to the whole repository.

## Mission

This repository supports a three-week RL course project. Core RL is the default path. Embodied/simulation RL and LLM/agentic RL are exceptions that require prior approval and strict scope control.

Every proposal, experiment, poster, and report must state a focused RL question. Do not frame work only as "method X scored higher." Evaluate work by question clarity, connection to core RL, reproducibility, and honest interpretation.

Use `AlbertaPlan.pdf` as the main lens. Prefer small, online, continual-learning experiments about ordinary experience, temporal uniformity, limited computation, value functions, learned models, planning, GVFs, average reward, options, and continual actor-critic control.

## Agent Working Principles

Follow the Karpathy-style guidance in `resources/andrej-karpathy-skills/` when it helps the work:

- Think before coding: state assumptions, surface ambiguity, ask when a choice is risky, and push back when a simpler path fits better.
- Plan before large work: for broad tasks, write or update a concise planning document that captures scope, milestones, and open questions; refine it as subtasks progress.
- Simplicity first: implement the minimum solution that answers the request; avoid speculative features, unnecessary flexibility, and one-off abstractions.
- Surgical changes: touch only what the task requires, match existing style, and do not clean up unrelated code or imported materials.
- Goal-driven execution: turn non-trivial tasks into concrete success criteria, then loop until the relevant check passes.
- Verification discipline: for bugs, reproduce first when feasible; for edits, verify with the smallest useful test, command, or artifact check.

For trivial one-line fixes or simple file operations, stay lightweight.

## Resources

Use repository resources in this order:

- Framing: `AlbertaPlan.pdf`, `RL_Course_Project.pdf`, `Proposal_Template.md`.
- RL theory: `resources/class-on-files/Reinforcement_Learning-An_Introduction.pdf`.
- Course notes: `resources/class-on-files/0706_am_sutton_lecture.docx`, `resources/class-on-files/0706_pm_sutton_discussion.docx`, `resources/class-on-files/0708_am_sutton_lecture.docx`, `resources/class-on-files/0706_pm_project_discussion.docx`.
- Supplemental Alberta Plan notes: `resources/class-on-files/alberta_plan_rl_conversation.md`; `AlbertaPlan.pdf` remains canonical when sources differ.
- Slides/logistics: `resources/class-on-files/RL_Course_Project.pptx`, `resources/class-on-files/2026强化学习暑期学校后续事宜通知（英文版）.pdf`.
- Class materials: `resources/class-materials/`; another `AlbertaPlan.pdf` copy is in `resources/class-materials/class02-bitter-lesson,-big-world,-six-steps/`.
- 2026 RL Summer School shared materials: `resources/26_RLSS_Lecture_Talk_Notes/` mirrors the Feishu folder hierarchy with directory-name spaces normalized to underscores, and includes course PDFs/notebooks plus exported DOCX/PPTX copies of the native Research Seminar files.
- Implementation references: `resources/Hands-on-RL/` and `resources/spinningup/` contain RL-related resources, code, and reference implementations for building experiments.
- General coding/workflow reference: `resources/andrej-karpathy-skills/` may guide agent behavior and exposition style, but it is not a canonical RL/course source.
- Conda environment configuration files live in `conda-env-configs/`; this directory is not an RL environment/testbed collection.

Keep this map updated when resources are added, renamed, or materially changed.

## Project Guidance

For proposals or project direction, answer:

1. What focused RL question are we testing?
2. What setting or testbed is used?
3. What is implemented, varied, or compared?
4. What observation, metric, or figure would answer the question?

Default preferences:

- Define the RL problem first: environment, observations, actions, rewards, objective, and evaluation.
- Prefer online/streaming learning. Default to no stored dataset, no replay buffer, and no offline training loop unless explicitly justified.
- Prefer tile coding or linear function approximation; justify nonlinear methods before using them.
- Treat training/test language carefully: the agent is designed first, then learns while interacting with the world.
- Keep experiments small, local/CPU, reproducible, and interpretable. Avoid blind grid search and large-model training.
- Inspect simple cases deeply: state distributions, approximation errors, axes, failure modes, and surprising behavior.

Good areas include streaming learning, partial observability and representation, average reward, reward centering, step-size adaptation, n-step methods, eligibility traces, GVFs, off-policy stability, Dyna/planning, options, and temporal abstraction.

Good testbeds include random walk, gridworld, windy gridworld, cliff walking, Four Rooms, Baird's counterexample, tile-coding prediction/control, Mountain Car, continuing gridworld, access-control queuing, small Markov chains, synthetic sensor streams, and non-stationary bandits.

## Implementation Rules

- Keep changes small and match existing style.
- Keep directory structure reasonable and simple so agents can read it efficiently and the user can review it easily.
- Prefer one clear script, notebook cell, or function over a framework.
- Use clear comments when writing or changing code to explain non-obvious purpose, behavior, or improvement; avoid noisy comments that restate the code.
- Prefer existing repo references: `resources/Hands-on-RL/` for compact educational implementations, `resources/spinningup/` for established algorithm references, and `resources/class-materials/` plus `resources/class-on-files/` for course material.
- Do not modify imported course/reference materials unless explicitly asked.
- Keep new experiments, scripts, notes, and reports separate from imported materials.
- Put rough ideas, early notes, and collected related materials in `draft/`.
- Put mature summaries, important materials, and final-facing artifacts in `final/`.

## Deliverables And Done Criteria

- Proposal: question/hypothesis, setting/testbed, comparison or variation, expected behavior, metric, compute need, and fallback.
- Checkpoint: minimal reproducible baseline; simplify the topic or environment if no baseline exists.
- Final package: 4-6 page report, poster, code, exact run command, seed(s), result path, and short reproduction/reflection note.
- Report/poster opening: RL question, why it matters, environment, method/baseline, result or failure, interpretation, next step, and reproducibility.
- Experiment work must include a baseline, seed, exact command, metric, and result path when applicable.
- Code work should have the narrowest reasonable diff and a small smoke test or reproduction command when feasible.

## Operations And Safety

- Use `proxy_on` before external downloads/searches and `proxy_off` afterward when available.
- Dangerous deletion commands are forbidden by default.
- Any deletion outside this `Core-RL` project requires explicit user confirmation and approval.
- If conda storage is tight, create or move environments under `/data/yupeng/conda_envs` and register that location with conda, following the `jailbreak` and `sft-s2` pattern.
