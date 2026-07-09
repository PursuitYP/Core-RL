# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** GVF Predictive State Under Partial Observability

## What do you want to understand?

Whether learned predictions can become useful state, not merely accurate auxiliary quantities. The focused RL question is: can a small GVF feature carry hidden cue information needed for control in an online partially observable task?

## What setting or testbed will you use?

A long aliased T-maze. The agent observes a start cue, then traverses an aliased corridor where the cue is absent, and must choose the correct turn at the junction.

## What will you examine?

Raw observation, short history, hand-coded trace memory, recurrent GVF features, and oracle cue memory. The comparison separates task impossibility from failure of the learned predictive-state construction.

## What will you look at?

Trial-end accuracy, average reward, GVF TD error, cue-trace trajectories, and values by maze position. A useful result must show whether the learned prediction actually carries the information that the control decision needs.

## Expanded Template Details

### Focused RL Problem

The agent acts in a partially observable T-maze. An early cue determines the correct later turn, but the cue disappears from raw observation during the corridor. The question is whether learned GVF predictions can carry this hidden information as useful state for control.

### Agent And Update

The control learner is online linear Sarsa over different representations: raw observation, short history, hand-coded trace memory, recurrent GVF features, and oracle cue memory. GVF learners use TD updates for cue- or outcome-related cumulants. The report must specify cumulants, discounts, recurrence, and how GVF outputs enter the control feature vector.

### Experiment Plan

Run multiple maze lengths and representation modes. Trace and oracle baselines are required to prove the task is solvable. A stronger version adds cue-decodability probes and ablations where GVF outputs are scaled, removed, or replaced with oracle predictions.

### Metrics And Decision Rule

Metrics are trial-end accuracy, reward, GVF TD error, cue-alignment/decode accuracy, and junction action correctness. A positive GVF result requires improved control over cheap memory baselines or at least clear hidden-cue information in the learned prediction.

### Fallback

The current result is negative. It should motivate GVF question redesign rather than be reported as evidence that GVFs succeed.

## Additional Writing Guidance

A strong version of this proposal should read as a focused Core-RL research plan, not as an algorithm demo. The final write-up should explicitly define the observation stream, action or prediction target, reward/cumulant, update rule, baseline methods, changed variables, and decision criterion. It should also say what result would falsify the idea. For negative or diagnostic proposals, the report should not hide the weakness; it should explain what the failed mechanism teaches about continual online learning.

The experiment should be presented with seed-level statistics, exact result directory, exact config path, and at least one figure that directly answers the research question. If the main metric is not enough to answer the question, the template should name the missing diagnostic before the experiment is promoted. A strict reviewer should be able to ask “what would convince me?” and find a direct answer in the design.

## Archive Status And Specific Reviewer Notes

Canonical report: `final/reports/proposals/gvf_predictive_state/report.md`. Current result: `experiments/alberta_core_rl/results/useful_gvfs_state/20260708T155740Z_main`. This template is archived because the final report now explains the negative result and maps the report name to implementation key `useful_gvfs_state`.

Current status: negative result and redesign target. Trace memory and oracle memory solve the T-maze, while the current recurrent GVF remains near chance; this shows that the implemented GVF question does not carry useful control state.

Specific missing details before promotion: GVF cumulant definition, discount/horizon, recurrent feature construction, whether the GVF output is normalized for control, cue-decodability probe, and an ablation that removes each feature group from the control state. The proposal would become positive only if learned GVF features improve trial accuracy over raw/short-history baselines and approach cheap trace memory.
