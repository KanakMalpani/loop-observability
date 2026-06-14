"""Map LTF iteration spans to LoopNet trajectory steps."""

from __future__ import annotations

from typing import Any


def trajectory_from_trace(trace: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract ln/record-v1-compatible trajectory steps from iteration spans."""
    steps: list[dict[str, Any]] = []
    for span in trace.get("spans") or []:
        if span.get("kind") != "iteration":
            continue
        attrs = span.get("attributes") or {}
        iteration = int(attrs.get("loop.iteration", len(steps) + 1))
        goal_score = float(attrs.get("loop.goal_score", 0.0))
        steps.append(
            {
                "iteration": iteration,
                "goal_score": goal_score,
                "primary_quality": goal_score,
                "cost_usd": attrs.get("loop.cost_usd"),
                "latency_seconds": (
                    float(attrs["loop.latency_ms"]) / 1000.0
                    if attrs.get("loop.latency_ms") is not None
                    else None
                ),
                "tokens": attrs.get("loop.tokens_delta"),
                "failure_codes": [],
                "safety_events": 0,
                "human_intervention": False,
            }
        )
    steps.sort(key=lambda s: s["iteration"])
    return steps
