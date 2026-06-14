"""LoopGym integration — trace SimEnv / LiveEnv episodes."""

from __future__ import annotations

import time
from typing import Any

from loopotel.tracer import LoopTracer


def _worker_evaluator_ids(spec: dict[str, Any]) -> tuple[str | None, str | None]:
    workers = spec.get("workers") or []
    evaluators = spec.get("evaluators") or []
    worker_id = str(workers[0]["id"]) if workers and workers[0].get("id") else None
    evaluator_id = str(evaluators[0]["id"]) if evaluators and evaluators[0].get("id") else None
    return worker_id, evaluator_id


def _goal_target_from_spec(spec: dict[str, Any]) -> float:
    term = spec.get("termination_conditions")
    if isinstance(term, dict):
        for success in term.get("success") or []:
            if success.get("value") is not None:
                return float(success["value"])
    for ev in spec.get("evaluators") or []:
        rubric = ev.get("rubric") or {}
        if rubric.get("pass_threshold") is not None:
            return float(rubric["pass_threshold"])
    return 0.8


def run_traced_episode(
    env: Any,
    *,
    task_id: str = "",
    seed: int | None = None,
    enabled: bool = True,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run a LoopGym episode and return (episode_result, ltf_trace).

    Tracing is opt-in (`enabled=True`). Default off matches SimEnv policy;
    pass `enabled=True` explicitly or use `trace_live=True` wrappers.
    """
    spec = getattr(env, "spec", {}) or {}
    loop_name = str(spec.get("loop_name", "unknown-loop"))
    goal_target = _goal_target_from_spec(spec)
    worker_id, evaluator_id = _worker_evaluator_ids(spec)

    tracer = LoopTracer(
        loop_name=loop_name,
        env_id=getattr(env, "env_id", None),
        task_id=task_id or None,
        goal_target=goal_target,
        enabled=enabled,
    )

    with tracer:
        obs = env.reset(task_id=task_id, seed=seed)
        prev_tokens = 0
        if getattr(env, "_runtime", None) and getattr(env._runtime, "llm", None):
            prev_tokens = getattr(env._runtime.llm, "tokens_used", 0)

        last_latency_ms = 0.0
        while not env.done:
            t0 = time.perf_counter()
            obs, _reward, _done, info = env.step()
            last_latency_ms = (time.perf_counter() - t0) * 1000.0
            tokens_now = 0
            if getattr(env, "_runtime", None) and getattr(env._runtime, "llm", None):
                tokens_now = getattr(env._runtime.llm, "tokens_used", 0)
            tokens_delta = max(0, tokens_now - prev_tokens)
            prev_tokens = tokens_now

            if obs.iteration > 0:
                tracer.emit_iteration(
                    iteration=obs.iteration,
                    goal_score=obs.quality_score,
                    goal_target=goal_target,
                    tokens_delta=tokens_delta,
                    latency_ms=round(last_latency_ms, 2),
                    worker_id=worker_id,
                    evaluator_id=evaluator_id,
                )

        outcome = "success" if info.get("success") else "failure"
        tracer.finish(
            outcome=outcome,
            termination_reason=str(info.get("termination_reason", "")),
        )

    result = {
        "task_id": task_id,
        "seed": seed,
        "env_id": getattr(env, "env_id", None),
        "success": info.get("success", False),
        "quality_score": obs.quality_score,
        "termination_reason": info.get("termination_reason", ""),
    }
    return result, tracer.build_trace()


def trace_live_episode(env: Any, **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    """LiveEnv helper — tracing on by default."""
    return run_traced_episode(env, enabled=True, **kwargs)
