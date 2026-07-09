# Dyna Planning Budget

> Status note, 2026-07-08: conditional third story after recovery-window rerun. The current evidence supports a model-staleness/recovery tradeoff, not a generic "more planning is better" claim.

## Research Motivation

The Alberta Plan includes learned models and continual planning. The key practical question is how much planning computation is worth spending per real step.

## Research Question

How does a fixed per-step planning budget trade off pre-change sample efficiency against post-change stale-model harm in a continuing control stream?

## Method

Compare no-planning Q-learning to Dyna-style updates with one or five model backups per step, with either a kept model or model flush at the environment change.

## Experimental Design

Continuing gridworld with compact state-action transition model and a midway goal/hazard layout change.

## Metrics

Average reward, model size, Q norm, stale-backup rate, and recovery-window reward after the layout change.

## Current Result

`experiments/alberta_core_rl/results/dyna_planning_budget/20260708T154815Z_main`

## Result Analysis Plan

Report pre-change planning gains, post-change recovery windows, stale-backup rates, and the keep-model versus flush-on-change contrast. Make clear this is model-based planning, not a replay buffer.

## Summary

This gives the project planning coverage and a direct bridge to Alberta Plan later steps, but only as a compact third story if report space allows.
