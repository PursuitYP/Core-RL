# Baird Off-policy Stability

> Status note, 2026-07-08: supporting diagnostic. Keep it as a cautionary off-policy stability figure after canonical setup verification; do not make it a main project story.

## Research Motivation

GVFs and background learning often require off-policy updates. Baird's counterexample is a minimal demonstration that off-policy bootstrapping with function approximation can diverge.

## Research Question

Where does semi-gradient off-policy TD fail, and which corrections stabilize it?

## Method

Compare off-policy TD with a TDC-style correction.

## Experimental Design

Baird-style seven-state counterexample with linear features and zero rewards.

## Metrics

Weight norm, TD error, importance ratio, divergence flag.

## Current Result

`experiments/alberta_core_rl/results/baird_offpolicy_stability/20260708T161717Z_main`

## Result Analysis Plan

Verify canonical Baird details before final claims. Add alpha sweep and GTD2/ETD if time permits.

## Summary

Theoretically valuable, but should be positioned carefully because it is off-policy.
