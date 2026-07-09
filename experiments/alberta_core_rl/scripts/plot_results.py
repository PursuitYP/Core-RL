#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.plotting import plot_learning_curve


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot a result directory produced by run_experiment.py.")
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--y-key", default=None)
    parser.add_argument("--group-keys", nargs="*", default=None)
    args = parser.parse_args()
    out = plot_learning_curve(Path(args.result_dir), y_key=args.y_key, group_keys=args.group_keys)
    print(out)


if __name__ == "__main__":
    main()
