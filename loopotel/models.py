"""LTF document builders and identifiers."""

from __future__ import annotations

import secrets
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def new_trace_id() -> str:
    return f"ltf-{uuid4()}"


def new_span_id() -> str:
    return secrets.token_hex(8)


def spec_pins() -> dict[str, str]:
    return {"lss": "lss@1.0.0", "les": "les@1.0.0", "ltf": "ltf@0.1.0"}


def otel_attributes(
    *,
    loop_name: str,
    env_id: str | None = None,
    task_id: str | None = None,
    iteration: int | None = None,
    goal_score: float | None = None,
    goal_target: float | None = None,
    tokens_delta: int | None = None,
    cost_usd: float | None = None,
    latency_ms: float | None = None,
    les_cumulative: float | None = None,
    les_effectiveness: float | None = None,
    worker_id: str | None = None,
    evaluator_id: str | None = None,
    outcome: str | None = None,
    termination_reason: str | None = None,
) -> dict[str, Any]:
    attrs: dict[str, Any] = {"loop.name": loop_name}
    mapping = {
        "loop.env_id": env_id,
        "loop.task_id": task_id,
        "loop.iteration": iteration,
        "loop.goal_score": goal_score,
        "loop.goal_target": goal_target,
        "loop.tokens_delta": tokens_delta,
        "loop.cost_usd": cost_usd,
        "loop.latency_ms": latency_ms,
        "loop.les.cumulative_normalized": les_cumulative,
        "loop.les.effectiveness": les_effectiveness,
        "loop.worker.id": worker_id,
        "loop.evaluator.id": evaluator_id,
        "loop.outcome": outcome,
        "loop.termination_reason": termination_reason,
        "loop.lss_version": "1.0.0",
        "loop.les_version": "1.0.0",
    }
    for key, value in mapping.items():
        if value is not None:
            attrs[key] = value
    return attrs
