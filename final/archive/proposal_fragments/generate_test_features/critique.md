# Critique: Generate-and-Test Features

## Reviewer Objections

- Plausible trace timescales are not evidence of useful representation.
- The current oracle-bank baseline does not clearly outperform random replacement.
- A single delay switch is too narrow for a continual feature-replacement claim.
- Utility must be tied to prediction error or downstream control.

## Revisions Already Made

- Added recovery-window metrics.
- Logged active timescale proximity and replacement behavior.
- Reframed the result as negative rather than positive.

## Next Required Iteration

- Build a validation stream where a known trace bank wins.
- Add repeated delay changes.
- Evaluate recovery AUC and downstream control utility.
- Redesign utility to estimate contribution to prediction loss.
