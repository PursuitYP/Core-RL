# Reward-Centered Continuing Sarsa

> Status note, 2026-07-08: promoted to main story. The current evidence is the access-control main run in `final/indexes/results.md`, not the older two-loop minimal run.

## Research Motivation

Continuing agents should be robust to arbitrary constant shifts in reward. Discounted Sarsa does not naturally have this invariance because a reward shift changes the value scale and TD error magnitude. Reward centering makes the update closer to an average-reward view.

## Research Question

Does online reward centering make continuing Sarsa insensitive to constant reward shifts?

## Method

Compare discounted Sarsa, reward-centered Sarsa, and differential Sarsa in continuing access-control.

## Experimental Design

Use an access-control queue with constant reward shifts. Record observed reward and unshifted reward separately.

## Metrics

Unshifted average reward, Q norm, TD error, action choice, reward baseline.

## Current Result

`experiments/alberta_core_rl/results/reward_centered_sarsa/20260708T153802Z_main`

## Result Analysis Plan

Look for policy and learning-curve invariance across reward shifts. If centered methods do not win final return but maintain stable value scale and policy, that is still a meaningful positive result.

## Summary

This is one of the two strongest proposals and should receive final-report priority.
