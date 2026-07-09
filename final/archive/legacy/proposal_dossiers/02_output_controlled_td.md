# Output-Controlled TD

> Status note, 2026-07-08: promoted to main story after clean full-config rerun. The old one-hot minimal run is only an introduction.

## Research Motivation

Fixed TD step-size is a parameter-space quantity. In streaming learning, the relevant object is often prediction-output change. Feature scaling can make a fixed alpha unstable.

## Research Question

Can normalized or output-controlled TD make streaming prediction robust to feature scale and trace magnitude?

## Method

Compare fixed TD, normalized TD, trace-normalized TD, and true-online TD(lambda).

## Experimental Design

Tile-coded random walk prediction with overlapping features scaled by one, ten, hundred, and uneven scales.

## Metrics

RMSE, weight norm, effective step-size, prediction-change magnitude, divergence flag.

## Current Result

`experiments/alberta_core_rl/results/output_controlled_td/20260708T153802Z_main`

## Result Analysis Plan

Show that fixed alpha's stable region moves under feature scaling, while normalized and trace-normalized TD are more invariant. Treat trace-normalized TD as a heuristic and report the current true-online TD(lambda) failures honestly.

## Summary

This is the second strongest proposal and pairs well with Reward-Centered Sarsa as a normalization/invariance story.
