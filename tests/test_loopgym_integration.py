"""LoopGym integration tests (optional dependency)."""

from __future__ import annotations

import pytest

pytest.importorskip("loopgym")

import loopgym as lg  # noqa: E402

from loopotel.exporter.jsonl import JsonlExporter  # noqa: E402
from loopotel.exporter.loopnet import trajectory_from_trace  # noqa: E402
from loopotel.integrations.loopgym import run_traced_episode  # noqa: E402
from loopotel.validate import validate_trace  # noqa: E402


def test_loopgym_simenv_exports_valid_ltf(tmp_path):
    env = lg.make("loopbench/code-repair-v1")
    result, trace = run_traced_episode(env, task_id="cr-001", seed=42, enabled=True)

    assert result["success"] is True
    valid, errors = validate_trace(trace)
    assert valid, errors

    iterations = [s for s in trace["spans"] if s["kind"] == "iteration"]
    assert len(iterations) >= 1
    assert trace["env_id"] == "loopbench/code-repair-v1"

    out = tmp_path / "trace.jsonl"
    JsonlExporter(out).export(trace)
    assert out.read_text(encoding="utf-8").strip().startswith("{")

    trajectory = trajectory_from_trace(trace)
    assert len(trajectory) == len(iterations)
    assert all("goal_score" in step for step in trajectory)
