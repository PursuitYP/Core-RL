# Critique: GVF Predictive State

## Reviewer Objections

- The current negative result only falsifies the implemented GVF question/state design.
- A GVF feature must be judged by hidden-cue information and downstream control, not TD error alone.
- Trace memory is a cheap and strong baseline; a positive GVF claim must approach it.
- The current report lacks cue-decodability probes.

## Revisions Already Made

- Added trace-memory and oracle-memory baselines.
- Added position-level GVF/trace trajectory plots.
- Corrected evaluation to focus on trial-end accuracy.

## Next Required Iteration

- Add cue linear-probe accuracy for learned features.
- Redesign cumulants to predict cue-relevant future events.
- Sweep maze length and cue semantics.
- Promote only if learned predictions beat raw/history and approach trace memory.
