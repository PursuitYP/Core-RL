#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from alberta_core_rl.proposals import summarize_by_condition
from alberta_core_rl.core import write_json


def parse_value(value: str):
    try:
        return float(value)
    except ValueError:
        return value


def read_rows(result_dir: Path) -> list[dict]:
    metrics_path = result_dir / "metrics.csv"
    with metrics_path.open("r", encoding="utf-8") as f:
        return [{key: parse_value(value) for key, value in row.items()} for row in csv.DictReader(f)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild seed-aware condition_summary.json from metrics.csv.")
    parser.add_argument("result_dirs", nargs="+")
    args = parser.parse_args()
    for item in args.result_dirs:
        result_dir = Path(item)
        rows = read_rows(result_dir)
        condition_summary = summarize_by_condition(rows)
        write_json(result_dir / "condition_summary.json", condition_summary)
        summary_path = result_dir / "summary.json"
        if summary_path.exists():
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary["n_condition_groups"] = len(condition_summary)
            summary["condition_summary_version"] = "seed_tail_v1"
            write_json(summary_path, summary)
        print(result_dir)


if __name__ == "__main__":
    main()
