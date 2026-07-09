# Critique: Output-Controlled TD

## Reviewer Objections

- True-online TD(lambda) may be unfairly represented if it uses the same raw alpha grid as normalized methods.
- The main result is prediction-only; control should be tested before broad RL claims.
- Feature-scale changes are synthetic and need interpretation as an invariance test.
- A stability atlas should include max-stable-alpha summaries, not only curves.

## Revisions Already Made

- Upgraded from one-hot random walk to overlapping tile coding.
- Added scale and alpha grids.
- Logged divergence, weight norm, and prediction-change magnitude.

## Next Required Iteration

- Audit true-online TD(lambda) on a known case.
- Report max stable alpha by method and scale.
- Add nonstationary feature-scale changes without reset.
- Test normalized Sarsa in at least one control setting.
