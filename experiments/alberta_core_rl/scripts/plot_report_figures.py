#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.report_figures_core import (
    plot_dyna_aging,
    plot_dyna_budget,
    plot_predictive_state,
    plot_scale_invariant,
)
from alberta_core_rl.report_figures_heatmaps import (
    plot_onpolicy_atlas,
    plot_output_td,
    plot_reward_centered,
    plot_unit_switching,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build report-ready summary figures from condition summaries.")
    parser.add_argument("--result-dir", required=True)
    parser.add_argument(
        "--kind",
        choices=[
            "scale",
            "dyna-aging",
            "dyna-budget",
            "predictive-state",
            "output-td",
            "reward-centered",
            "onpolicy-atlas",
            "unit-switching",
        ],
        required=True,
    )
    args = parser.parse_args()
    result_dir = Path(args.result_dir)
    if args.kind == "scale":
        outputs = plot_scale_invariant(result_dir)
    elif args.kind == "dyna-aging":
        outputs = plot_dyna_aging(result_dir)
    elif args.kind == "dyna-budget":
        outputs = plot_dyna_budget(result_dir)
    elif args.kind == "predictive-state":
        outputs = plot_predictive_state(result_dir)
    elif args.kind == "output-td":
        outputs = plot_output_td(result_dir)
    elif args.kind == "reward-centered":
        outputs = plot_reward_centered(result_dir)
    elif args.kind == "onpolicy-atlas":
        outputs = plot_onpolicy_atlas(result_dir)
    else:
        outputs = plot_unit_switching(result_dir)
    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()
