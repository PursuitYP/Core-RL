# Critique: Reward-Centered Sarsa

## Reviewer Objections

- The result must be framed as reward-origin invariance, not as shifted-return improvement.
- Differential Sarsa is a serious average-reward baseline; reward centering should not be presented as uniquely solving the issue.
- Five seeds and `5000` steps are a pilot-level statistical base.
- Average-reward estimator step size `beta` may be a hidden tuning parameter.
- Constant reward shifts are cleaner than real nonstationarity; a stronger study should include midstream shifts.

## Revisions Already Made

- Moved the main result from a two-loop MDP to access-control.
- Logged shifted and unshifted rewards separately.
- Added Q norm, reward-bar, and policy-probe diagnostics.

## Next Required Iteration

- Run seeds `0-19`.
- Sweep `beta` and `gamma`.
- Add midstream reward-origin changes.
- Compare reward-centered and differential Sarsa by invariance, not only reward.
