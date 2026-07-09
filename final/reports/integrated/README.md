# Integrated Proposal Portfolio

This folder contains three larger independent Core-RL proposal candidates created after the first independent proposal pass. The original 13 proposal folders remain independent studies; these larger proposals do not replace them. Each integrated proposal is itself a standalone research topic with linked subquestions, richer experiments, and one primary `report.md`.

The integrated proposals are not a synthetic “one paper” assembled from unrelated pieces. Each one must be read as its own research topic: a focused RL problem, one or more testbeds, a defined algorithmic intervention, a metric that answers the question, and a candid interpretation of the current evidence. The integrated label only means that several Core RL mechanisms are studied together because the combined question is stronger than the isolated fragment.

- online/streaming interaction,
- no replay buffer,
- no deep networks,
- CPU-scale experiments,
- interpretable tabular or linear methods.

## Three Primary Integrated Candidates

| Integrated proposal | Core topics combined | Main research pressure | Status |
|---|---|---|---|
| Scale-Invariant Continuing Control | reward centering, average reward, output-controlled TD/Sarsa, continuing control | reward translation and feature-scale changes in one ongoing control stream | fixed-condition main pilot plus 20-seed no-reset unit-switch extension completed; full fixed-condition extended grid still open |
| Continual Dyna Model Aging | learned models, Dyna planning, nonstationarity, computation budget, average-reward control | stale model knowledge after world changes | 20-seed half-life/budget extended sweep completed; strongest planning-focused candidate |
| Predictive State Plasticity | GVFs, useful predictions, generate-and-test, TIDBD, partial observability | maintaining useful memory features under changing hidden-state relevance | 20-seed first-gate negative result completed; staged redesign candidate, not a solved plasticity method |

## How These Relate To Existing Proposals

The integrated proposals are larger standalone directions produced by critique of the existing portfolio. Current evidence differs by proposal: Scale-Invariant has a main pilot plus a unit-switch extension, Dyna Aging has completed extended evidence, and Predictive State Plasticity has a completed negative first-gate. Cite each proposal's `report.md` and the result directories indexed in `final/indexes/results.md` rather than treating this README as the evidence source:

- Reward-Centered Sarsa and Output-Controlled TD become a single invariance story.
- Dyna Planning Budget becomes a model-freshness and computation-allocation story.
- GVF Predictive State, GVF Question Design, Generate-and-Test, and TIDBD become a predictive-state plasticity story.

Each primary subfolder contains:

- `report.md`

Older supporting fragments were moved to `final/archive/integrated_fragments/<proposal>/`. The deferred off-policy GVF stability idea is in `final/archive/deferred_integrated/` and is not counted as one of the three new large proposals.
