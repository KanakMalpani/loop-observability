# 07 — loop-observability

## One-line purpose

**Loop Trace Format (LTF)** and OpenTelemetry conventions for production loop monitoring.

## Why this repo exists

Industry adopts what they can **operate**. SREs need spans for iterations, evaluators, token burn, LES deltas — not raw chat logs.

## Scope (in scope)

- LTF JSON schema (one span per iteration, child spans per worker/evaluator)
- OpenTelemetry semantic conventions draft (`loop.*` attributes)
- Exporters: OTLP, JSONL, LoopNet trajectory export
- Reference instrumentation for LoopGym / LangGraph
- Dashboard templates (Grafana JSON v0.1)
- LES time-series spec (point-in-loop metrics)

## Scope (out of scope)

- Full SaaS observability product
- Log storage infrastructure

## Deliverables v0.1

- [x] `specs/ltf-0.1.schema.json`
- [x] `specs/otel-semconv-loop.md`
- [x] `loopotel/` Python package — `@trace_loop`, `emit_iteration()`
- [x] `examples/grafana-dashboard.json`

## Status

✅ v0.1 shipped — see [STATUS.md](STATUS.md)

## Dependencies

- **01-loop-engineering-core** — LES dimensions, worker/evaluator IDs
- **05-loopgym** — instrumentation target

## Success criteria

One LoopGym run exports valid LTF; Grafana dashboard shows iterations vs cumulative LES.

## Agent instructions

Design for **minimal overhead**; default off in SimEnv, on in LiveEnv.

## Status

🟡 Planning only
