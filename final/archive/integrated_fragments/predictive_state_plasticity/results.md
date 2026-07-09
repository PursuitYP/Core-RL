# Results: Predictive State Plasticity

Current main pilot:

`experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main`

Figures:

![Trial accuracy by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main/figures/report_trial_accuracy_by_maze_length.png)

![Cue-alignment margin by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main/figures/cue_alignment_margin_by_algorithm-maze_length_curve.png)

![GVF TD error by state construction and maze length.](../../../../experiments/alberta_core_rl/results/predictive_state_plasticity/20260708T174842Z_main/figures/gvf_abs_td_error_by_algorithm-maze_length_curve.png)

## Seed-Aware Finding

The redesigned cue-GVF carries more cue-aligned signal than the old terminal-outcome GVF, but it still does not become useful control state.

Tail trial accuracy:

- Trace memory: about `0.957`, `0.929`, and `0.945` for maze lengths `8`, `12`, and `20`.
- Oracle memory: about `0.963`, `0.960`, and `0.951`.
- Raw observation: near chance, about `0.47-0.50`.
- Old recurrent GVF: near chance, about `0.49-0.50`.
- Redesigned cue-GVF: still near chance, about `0.47-0.49`.

Cue-alignment margin:

- Cue-GVF has positive margins around `0.19`, `0.18`, and `0.10` for lengths `8`, `12`, and `20`.
- Old recurrent GVF margins are near zero or negative.

## Interpretation

The redesigned cue-GVF is a better predictive signal than the old recurrent GVF, but the signal is too weak or too poorly used by the control learner to solve the task. This is a useful gate result: measurable hidden-cue information is necessary but not sufficient for a prediction to become useful state.

## Current Limitations

The pilot does not yet include feature replacement or TIDBD adaptation. It is the first stage of the larger proposal: validate useful predictive state before adding plasticity mechanisms.
