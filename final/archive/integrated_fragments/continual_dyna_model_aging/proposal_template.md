# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Continual Dyna With Model Aging and Stale-Backup Control

## What do you want to understand?

Whether a continual agent should treat learned model entries as durable knowledge or as aging hypotheses. The focused RL question is: can model-aging or uncertainty-aware search control preserve Dyna's pre-change sample-efficiency benefit while reducing stale planning harm after nonstationarity?

## What setting or testbed will you use?

A continuing gridworld or access-control-like environment with layout/reward dynamics that change without an episode reset. The agent learns a compact one-step model and performs a limited number of planning backups per real step.

## What will you examine?

No-planning control, random Dyna, keep-model Dyna, flush-on-change Dyna, recency-aged Dyna, and stale-error-prioritized Dyna. The core variables are planning budget, model aging rate, and change severity.

## What will you look at?

Pre-change reward, post-change recovery, stale-backup rate, model prediction error, planning backup utility, and real-step sample efficiency. The central result is a planning-benefit versus stale-harm tradeoff curve.
