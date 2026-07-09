# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Predictive State Plasticity: Useful GVFs Under Limited Feature Capacity

## What do you want to understand?

Whether a continual agent can maintain predictions that are useful as state when partial observability and feature relevance change. The focused RL question is: can GVF question selection, generate-and-test feature replacement, and per-feature step-size adaptation jointly preserve control-relevant memory in a streaming task?

## What setting or testbed will you use?

A family of partially observable T-mazes or sensor-chain tasks where the relevant cue, delay length, or hidden variable changes across phases without replay or resets.

## What will you examine?

Raw observation, fixed trace memory, oracle memory, fixed GVF questions, generated GVF/trace features, and TIDBD-style per-feature adaptation. Each method has a fixed feature budget.

## What will you look at?

Trial accuracy, prediction usefulness, cue-information carried by features, recovery after hidden-variable changes, feature survival/replacement, and per-feature step-size dynamics. The key result is whether learned predictive features become useful state, not whether they minimize an auxiliary prediction error alone.
