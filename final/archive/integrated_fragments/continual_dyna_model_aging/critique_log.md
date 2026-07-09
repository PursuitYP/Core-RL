# Critique Log: Continual Dyna Model Aging

## Round 1: Planning Reviewer

Concern: A stationary environment would only demonstrate known Dyna benefits.

Revision: The main task must include unsignaled nonstationarity and stale-backup metrics.

## Round 2: Continual-Learning Reviewer

Concern: Resetting the model after a known change violates temporal uniformity.

Revision: Flush is labeled oracle diagnostic; publishable variants use only online recency and prediction-error signals.

## Round 3: Statistics Reviewer

Concern: One layout change may be anecdotal.

Revision: Add change severity and gradual drift as extensions, plus repeated-change seeds.

## Round 4: Systems Reviewer

Concern: Prioritized sweeping can become a large framework.

Revision: Keep the implementation compact: random, recency-aged, and error-gated planning first; add predecessor priorities only if time remains.

## Round 5: Skeptical Reader

Concern: Aging may simply reduce planning.

Revision: Report actual number of backups used, planning utility per backup, and compare to lower-budget random Dyna.
