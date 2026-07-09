# Critique: Dyna Planning Budget

## Reviewer Objections

- Stationary Dyna would be too shallow; nonstationarity is required.
- Flush-on-change is oracle knowledge and cannot be treated as an agent mechanism.
- Stale-backup rate is necessary to explain reward curves.
- One abrupt change is not enough for a complete continual-planning claim.

## Revisions Already Made

- Added layout change.
- Added keep-model versus flush-on-change comparison.
- Added stale-backup rate and recovery windows.

## Next Required Iteration

- Add model aging or online error gating.
- Sweep planning budgets `0, 1, 5, 20`.
- Add gradual drift and repeated changes.
- Report planning utility per backup.
