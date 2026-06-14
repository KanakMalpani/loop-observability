# LES time-series (point-in-loop metrics)

**Version:** 0.1 · **Pins:** `les@1.0.0`, `ltf@0.1.0`

Observability tooling records **partial LES** at each iteration so operators can see convergence without waiting for run completion.

## Canonical fields (per iteration)

| Field | Type | Description |
|-------|------|-------------|
| `loop.iteration` | int | 1-based index |
| `loop.goal_score` | float | `G_t` at iteration end |
| `loop.les.effectiveness` | float | `clamp(G_t / G_target, 0, 1)` when target known |
| `loop.les.cumulative_normalized` | float | Running composite proxy (v0.1: effectiveness-only) |

Full eight-category LES requires run-level baselines (see LoopBench). LTF v0.1 exports **observable** categories at iteration granularity; v0.2 will add speed/cost from token and latency deltas.

## Cumulative composite (v0.1 proxy)

```
N_effectiveness_t = clamp(goal_score_t / goal_target, 0, 1)
les_cumulative_t = mean(N_effectiveness_1 .. N_effectiveness_t)
```

When `goal_target` is unknown, use `0.8` (LoopBench default).

## Grafana panels

Import [`examples/grafana-dashboard.json`](../examples/grafana-dashboard.json):

1. **Goal score by iteration** — `loop.goal_score` vs `loop.iteration`
2. **Cumulative LES** — `loop.les.cumulative_normalized` vs `loop.iteration`
3. **Token burn** — cumulative `loop.tokens_delta`

## LoopNet export

`loopotel.exporter.loopnet.trajectory_from_trace()` maps iteration spans to `ln/record-v1` trajectory steps for corpus ingestion (redaction required for production).
