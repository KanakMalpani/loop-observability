#!/usr/bin/env python3
"""Export a LoopGym SimEnv run as valid LTF JSONL."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "examples" / "sample-trace.jsonl"


def main() -> int:
    try:
        import loopgym as lg
    except ImportError:
        print("Install loopgym: pip install loopgym", file=sys.stderr)
        return 1

    from loopotel.exporter.jsonl import JsonlExporter
    from loopotel.integrations.loopgym import run_traced_episode
    from loopotel.validate import validate_trace

    env = lg.make("loopbench/code-repair-v1")
    _result, trace = run_traced_episode(env, task_id="cr-001", seed=42, enabled=True)

    valid, errors = validate_trace(trace)
    if not valid:
        print("LTF validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    JsonlExporter(out_path).export(trace)

    iterations = sum(1 for s in trace["spans"] if s["kind"] == "iteration")
    last_les = next(
        (
            s["attributes"].get("loop.les.cumulative_normalized")
            for s in reversed(trace["spans"])
            if s["kind"] == "iteration"
        ),
        0,
    )
    print(f"Wrote LTF trace -> {out_path}")
    print(f"  trace_id: {trace['trace_id']}")
    print(f"  iterations: {iterations}")
    print(f"  cumulative LES: {last_les}")
    print(f"  outcome: {trace['outcome']}")
    print()
    print("Iteration series (for Grafana):")
    for span in trace["spans"]:
        if span["kind"] != "iteration":
            continue
        attrs = span["attributes"]
        print(
            f"  iter={attrs['loop.iteration']} "
            f"goal={attrs['loop.goal_score']:.3f} "
            f"les={attrs['loop.les.cumulative_normalized']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
