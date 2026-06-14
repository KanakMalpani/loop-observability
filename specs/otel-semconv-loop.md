# OpenTelemetry semantic conventions — loops (draft)

**Status:** Draft v0.1 · **Namespace:** `loop.*` · **Pins:** `lss@1.0.0`, `les@1.0.0`, `ltf@0.1.0`

This document defines recommended span names and attributes for instrumenting autonomous agent loops with OpenTelemetry. Implementations should map [LTF 0.1](ltf-0.1.schema.json) spans to OTLP export via `loopotel`.

## Span naming

| Span name | OTel kind | Description |
|-----------|-----------|-------------|
| `loop.run` | `Internal` | Root span for one loop instance |
| `loop.iteration` | `Internal` | One Observe → Evaluate → Decide → Act cycle |
| `loop.worker` | `Internal` | Worker invocation (child of iteration) |
| `loop.evaluator` | `Internal` | Evaluator invocation (child of iteration) |

## Attributes — loop instance

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `loop.name` | string | yes | LSS `loop_name` |
| `loop.env_id` | string | no | LoopGym env id or service id |
| `loop.task_id` | string | no | Task / instance id |
| `loop.lss_version` | string | yes | e.g. `1.0.0` |
| `loop.les_version` | string | yes | e.g. `1.0.0` |
| `loop.outcome` | string | no | `success`, `failure`, `partial` |
| `loop.termination_reason` | string | no | Termination cause |

## Attributes — iteration

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `loop.iteration` | int | yes | 1-based iteration index |
| `loop.goal_score` | double | yes | Primary quality at end of iteration `[0,1]` |
| `loop.goal_target` | double | no | Success threshold |
| `loop.tokens_delta` | int | no | Tokens consumed this iteration |
| `loop.cost_usd` | double | no | Estimated cost this iteration |
| `loop.latency_ms` | double | no | Wall time for iteration |
| `loop.les.cumulative_normalized` | double | no | Running composite LES proxy `[0,1]` |
| `loop.les.effectiveness` | double | no | Category sub-score at this point |

## Attributes — worker / evaluator

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `loop.worker.id` | string | worker | LSS worker id |
| `loop.worker.role` | string | no | Worker role label |
| `loop.evaluator.id` | string | evaluator | LSS evaluator id |
| `loop.evaluator.type` | string | no | `deterministic`, `llm_rubric`, etc. |

## Events

| Event name | Parent span | Attributes |
|------------|-------------|------------|
| `loop.iteration.start` | iteration | `loop.iteration` |
| `loop.iteration.end` | iteration | `loop.iteration`, `loop.goal_score` |
| `loop.worker.complete` | iteration | `loop.worker.id` |
| `loop.evaluator.complete` | iteration | `loop.evaluator.id`, `loop.goal_score` |
| `loop.safety.violation` | iteration | `loop.failure.code` |

## Mapping LTF → OTLP

- LTF `trace_id` → OTel `trace_id` (hex, padded)
- LTF `span_id` → OTel `span_id`
- LTF `attributes` keys use the same `loop.*` names above
- Export via `loopotel.exporter.otlp.OtlpExporter` when `opentelemetry-sdk` is installed

## References

- [LES 1.0](../../01-loop-engineering-core/specs/les-1.0.md)
- [LTF schema](ltf-0.1.schema.json)
- [LES time-series](les-timeseries.md)
