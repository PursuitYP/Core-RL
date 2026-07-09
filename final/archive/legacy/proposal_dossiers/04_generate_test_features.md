# Generate-and-Test Trace Features

> Status note, 2026-07-08: downgraded after recovery-window rerun. The current utility/replacement design improves trace-timescale proximity but does not improve prediction error over fixed or random baselines. Treat it as a negative diagnostic unless redesigned.

## Research Motivation

Long-lived agents cannot keep every feature. They need a utility mechanism to discard weak features and introduce new ones when temporal statistics change.

## Research Question

Under a fixed feature budget, can utility-based feature replacement maintain useful trace features after the reward delay changes?

## Method

Compare fixed trace features with generate-and-test replacement in trace-conditioning prediction.

## Experimental Design

Reward delay switches from 10 to 20 halfway through the stream.

## Metrics

Absolute TD error, recovery time, replacement events, trace decay distribution.

## Current Result

`experiments/alberta_core_rl/results/generate_test_features/20260708T154941Z_main`

## Result Analysis Plan

Current recovery-window summaries already show no prediction-error win. A redesign should add feature-survival curves, multiple delay changes, and a stronger reason why closer trace timescales should improve the value target.

## Summary

Strong conceptual fit, but the current implementation should not be defended as a final positive result.
