# Doorway Options for Transfer

> Status note, 2026-07-08: quarantined as a main proposal. Current SMDP Four Rooms evidence does not show options beating primitives under environment-step accounting.

## Research Motivation

Temporal abstraction is useful only when a subtask remains useful across changes in reward or goal. Doorway options are a minimal structural abstraction in Four Rooms.

## Research Question

When do doorway options help transfer across changing goals, and when does commitment cost hurt performance?

## Method

Compare primitive Sarsa and a minimal doorway-option controller.

## Experimental Design

Four Rooms with alternating goals.

## Metrics

Average reward per environment step, steps-to-goal, option duration, option usage.

## Current Result

`experiments/alberta_core_rl/results/options_reusable_subtasks/20260708T161717Z_main`

## Result Analysis Plan

Count environment steps, not only decision steps. A long option is not free computation.

## Summary

Useful for poster visualization, but must be framed as hand-coded option evaluation, not option discovery.
