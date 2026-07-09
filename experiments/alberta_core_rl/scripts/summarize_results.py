#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def condition_label(condition: dict) -> str:
    parts = [f"{key}={value}" for key, value in condition.items() if value is not None]
    return " | ".join(parts) if parts else "all"


def main() -> None:
    parser = argparse.ArgumentParser(description="Print per-condition tail summaries for a result directory.")
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--metrics", nargs="+", required=True)
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()

    path = Path(args.result_dir) / "condition_summary.json"
    if not path.exists():
        sys.exit(f"missing {path}")
    groups = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for group in groups:
        metrics = group.get("metrics", {})
        values = []
        for metric in args.metrics:
            seed_stats = metrics.get(f"{metric}_seed_tail")
            if seed_stats is not None:
                values.append((seed_stats.get("mean"), seed_stats.get("ci95"), seed_stats.get("n")))
                continue
            stats = metrics.get(f"{metric}_tail") or metrics.get(metric)
            value = None if stats is None else stats.get("tail_mean")
            values.append((value, None, None))
        rows.append((condition_label(group.get("condition", {})), group.get("n_rows", 0), group.get("n_seeds"), values))

    for label, n_rows, n_seeds, values in rows[: args.limit]:
        rendered_parts = []
        for metric, (mean, ci95, stat_n) in zip(args.metrics, values):
            if not isinstance(mean, (int, float)):
                rendered_parts.append(f"{metric}=NA")
            elif isinstance(ci95, (int, float)):
                rendered_parts.append(f"{metric}={mean:.6g}±{ci95:.3g} seed_n={stat_n}")
            else:
                rendered_parts.append(f"{metric}={mean:.6g}")
        rendered = ", ".join(rendered_parts)
        print(f"{label} | rows={n_rows} | seeds={n_seeds} | {rendered}")


if __name__ == "__main__":
    main()
