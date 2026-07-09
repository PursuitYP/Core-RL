#!/usr/bin/env python
from __future__ import annotations

import json
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.proposals import RUNNERS, run_proposal


def main() -> None:
    outputs = {}
    command = " ".join(shlex.quote(arg) for arg in sys.argv)
    for proposal in sorted(RUNNERS):
        out = run_proposal(proposal, suite="smoke", seeds=[0], steps=120, command=command)
        outputs[proposal] = str(out)
    print(json.dumps(outputs, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
