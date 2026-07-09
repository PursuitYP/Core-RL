# GVF Predictive State

> Status note, 2026-07-08: negative result after trace-memory rerun. Oracle memory and a cheap cue trace solve the task, but the current recurrent GVF design remains near chance.

## Research Motivation

Observation is not state under partial observability. GVFs can turn future predictions into state features, which is central to the Alberta Plan view of predictive knowledge.

## Research Question

Can learned GVF predictions supply missing state information in a partially observable control task?

## Method

Compare raw observation, short history, trace memory, GVF-augmented features, and oracle memory in a cue-based T-maze.

## Experimental Design

The cue appears at the start; the corridor is aliased; the correct junction action depends on the cue.

## Metrics

Average reward, junction correctness, GVF TD error, cue-trace values, and position-level GVF/trace trajectories.

## Current Result

`experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`

## Result Analysis Plan

Use the result as a failure localization: the task is learnable with simple memory, but the current recurrent GVF state is not carrying the cue. Any future positive GVF claim needs a new question design and trajectory evidence.

## Summary

Conceptually Alberta-style, but currently a negative result rather than a main story.
