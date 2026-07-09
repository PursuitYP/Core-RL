#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _format_value(stats: dict[str, Any] | None) -> str:
    if not stats:
        return "NA"
    mean = stats.get("mean", stats.get("tail_mean"))
    ci95 = stats.get("ci95")
    n = stats.get("n")
    if not isinstance(mean, (int, float)):
        return "NA"
    if isinstance(ci95, (int, float)):
        return f"{mean:.6g} +/- {ci95:.3g} (n={n})"
    return f"{mean:.6g}"


def _condition_label(condition: dict[str, Any], keys: list[str] | None) -> str:
    selected = keys or [key for key, value in condition.items() if value is not None]
    parts = [f"{key}={condition.get(key)}" for key in selected if condition.get(key) is not None]
    return " | ".join(parts) if parts else "all"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract compact seed-tail results from condition_summary.json.")
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--metrics", nargs="+", required=True)
    parser.add_argument("--condition-keys", nargs="*", default=None)
    parser.add_argument("--limit", type=int, default=80)
    args = parser.parse_args()

    path = Path(args.result_dir) / "condition_summary.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    print(f"result_dir: {args.result_dir}")
    print("| condition | " + " | ".join(args.metrics) + " |")
    print("| --- | " + " | ".join("---" for _ in args.metrics) + " |")
    for row in rows[: args.limit]:
        metrics = row.get("metrics", {})
        values = []
        for metric in args.metrics:
            stats = metrics.get(f"{metric}_seed_tail") or metrics.get(f"{metric}_tail") or metrics.get(metric)
            values.append(_format_value(stats))
        print(f"| {_condition_label(row.get('condition', {}), args.condition_keys)} | " + " | ".join(values) + " |")


if __name__ == "__main__":
    main()
