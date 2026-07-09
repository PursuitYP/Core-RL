# Critique Log: Scale-Invariant Continuing Control

## Round 1: Alberta Plan Reviewer

Concern: The proposal must not become ordinary hyperparameter robustness.

Revision: Frame the question as invariance under arbitrary reward and feature units in a temporally uniform continuing stream.

## Round 2: Sutton-Style Average-Reward Reviewer

Concern: Discounted Sarsa with centering should not be oversold as a replacement for average-reward learning.

Revision: Keep differential Sarsa as a serious baseline and report unshifted reward, not shifted observed return.

## Round 3: Experimental Statistician

Concern: A four-condition reward-shift curve is too thin.

Revision: Add feature-scale crossed design, seeds `0-19` for final sweeps, and condition wise confidence intervals.

## Round 4: Reproducibility Engineer

Concern: The current code has separate reward-centering and output-control modules.

Revision: The experiment needs an independent workspace and config; it should not silently reuse prediction-only metrics.

## Round 5: Skeptical Reader

Concern: If the combined method wins, maybe it is simply using a smaller effective alpha.

Revision: Log intended output change, TD-error scale, and normalized denominator so the analysis can distinguish smaller steps from scale-invariant steps.
