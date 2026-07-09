# TIDBD Plasticity

> Status note, 2026-07-08: supporting diagnostic only. It shows step-size adaptation, but must not be oversold as canonical TIDBD or as an error-performance win over normalized TD.

## Research Motivation

Feature relevance changes in continual learning. Per-feature step-size adaptation is a small form of representation learning under a fixed feature set.

## Research Question

Can per-feature step-size adaptation track changing feature relevance in streaming TD?

## Method

Compare fixed TD, normalized TD, and TIDBD-lite.

## Experimental Design

Synthetic sensor stream where relevant feature groups switch halfway.

## Metrics

Online absolute TD error, recovery time, mean and per-feature step-size, weight norm.

## Current Result

`experiments/alberta_core_rl/results/tidbd_plasticity/20260708T154941Z_main`

## Result Analysis Plan

Use recovery-window summaries and feature-group step-size trajectories. The current result shows that new-feature step sizes rise after the switch, but normalized TD still has lower late absolute TD error.

## Summary

Useful mechanism support for continual plasticity, but not a main performance story.
