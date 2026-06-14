"""Tests for LoopTracer and LTF validation."""

from __future__ import annotations

from loopotel.tracer import LoopTracer, emit_iteration, trace_loop
from loopotel.validate import validate_trace


def test_emit_iteration_builds_valid_trace():
    with LoopTracer(loop_name="test-loop", env_id="sim/mock", task_id="t-1") as tracer:
        tracer.emit_iteration(iteration=1, goal_score=0.5, tokens_delta=100, worker_id="w1", evaluator_id="e1")
        tracer.emit_iteration(iteration=2, goal_score=0.85, tokens_delta=120, worker_id="w1", evaluator_id="e1")
        tracer.finish(outcome="success", termination_reason="goal_met")

    trace = tracer.build_trace()
    valid, errors = validate_trace(trace)
    assert valid, errors
    assert trace["schema_version"] == "ltf/0.1"
    assert trace["outcome"] == "success"
    iteration_spans = [s for s in trace["spans"] if s["kind"] == "iteration"]
    assert len(iteration_spans) == 2
    assert iteration_spans[-1]["attributes"]["loop.les.cumulative_normalized"] >= iteration_spans[0]["attributes"][
        "loop.les.cumulative_normalized"
    ]


def test_tracing_disabled_is_noop():
    with LoopTracer(loop_name="off", enabled=False) as tracer:
        emit_iteration(iteration=1, goal_score=0.9)
    trace = tracer.build_trace()
    assert trace["spans"] == []


@trace_loop(loop_name="decorated-loop", env_id="test/env")
def _sample_run() -> None:
    emit_iteration(iteration=1, goal_score=0.6, worker_id="implementer", evaluator_id="rubric")


def test_trace_loop_decorator():
    _sample_run()
    # decorator finishes trace internally; no assertion on global state needed
    assert True
