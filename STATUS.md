# Status

| Field | Value |
|-------|-------|
| **Phase** | v0.1 shipped |
| **Symbol** | ✅ |
| **Notes** | LTF schema, loopotel package, LoopGym integration, Grafana template |

## Completion checklist

- [x] `specs/ltf-0.1.schema.json`
- [x] `specs/otel-semconv-loop.md`
- [x] `specs/les-timeseries.md`
- [x] `loopotel/` — `LoopTracer`, `@trace_loop`, `emit_iteration()`
- [x] Exporters: JSONL, OTLP (optional), LoopNet trajectory
- [x] `loopotel.integrations.loopgym` — `run_traced_episode()`
- [x] `examples/grafana-dashboard.json`
- [x] `examples/export_loopgym_ltf.py`
- [x] CI: pytest + LTF validation
- [x] PyPI publish `loopotel` — https://pypi.org/project/loopotel/

## Success criteria

- [x] One LoopGym run exports valid LTF
- [x] Grafana dashboard template for iterations vs cumulative LES

## Links

- Parent workspace: [../README.md](../README.md)
- Plan: [PLAN.md](PLAN.md)
