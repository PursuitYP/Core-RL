#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.plotting import plot_learning_curve
from alberta_core_rl.proposals import RUNNERS, run_proposal


def main() -> None:
    parser = argparse.ArgumentParser(description="Run all proposal experiments for a selected suite.")
    parser.add_argument("--suite", default="minimal", choices=["smoke", "minimal", "main"])
    parser.add_argument("--seeds", nargs="*", type=int, default=[0, 1, 2])
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--no-plots", action="store_true")
    args = parser.parse_args()
    outputs = {}
    for proposal in sorted(RUNNERS):
        command = " ".join(shlex.quote(arg) for arg in sys.argv)
        out = run_proposal(proposal, suite=args.suite, seeds=args.seeds, steps=args.steps, command=command)
        figure = None
        if not args.no_plots:
            figure = plot_learning_curve(out)
        outputs[proposal] = {"result_dir": str(out), "figure": str(figure) if figure else None}
    print(json.dumps(outputs, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
