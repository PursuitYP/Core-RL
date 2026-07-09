#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.proposals import RUNNERS, run_proposal


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a streaming Core RL proposal experiment.")
    parser.add_argument("--proposal", choices=sorted(RUNNERS))
    parser.add_argument("--suite", default="minimal", choices=["smoke", "minimal", "main"])
    parser.add_argument("--seeds", nargs="*", type=int, default=None)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--config", default=None, help="Optional JSON config with proposal/suite/seeds/steps.")
    args = parser.parse_args()
    raw_config = None
    if args.config:
        with Path(args.config).open("r", encoding="utf-8") as f:
            raw_config = json.load(f)
        proposal = raw_config.get("proposal", args.proposal)
        suite = raw_config.get("suite", args.suite)
        seeds = raw_config.get("seeds", args.seeds)
        steps = raw_config.get("steps", args.steps)
    else:
        proposal, suite, seeds, steps = args.proposal, args.suite, args.seeds, args.steps
    if not proposal:
        parser.error("--proposal is required unless --config supplies proposal")
    command = " ".join(shlex.quote(arg) for arg in sys.argv)
    out = run_proposal(
        proposal,
        suite=suite,
        seeds=seeds,
        steps=steps,
        config=raw_config,
        config_path=args.config,
        command=command,
    )
    print(out)


if __name__ == "__main__":
    main()
