"""Optional OTLP export (requires opentelemetry-sdk)."""

from __future__ import annotations

from typing import Any


class OtlpExporter:
    """Export LTF spans to an OTLP endpoint via OpenTelemetry SDK."""

    def __init__(self, endpoint: str | None = None, service_name: str = "loop-runtime") -> None:
        self.endpoint = endpoint
        self.service_name = service_name
        self._provider = None

    def _ensure_provider(self) -> None:
        if self._provider is not None:
            return
        try:
            from opentelemetry import trace
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
        except ImportError as exc:
            raise SystemExit(
                "OTLP export requires: pip install loopotel[otlp]"
            ) from exc

        resource = Resource.create({"service.name": self.service_name})
        provider = TracerProvider(resource=resource)
        kwargs: dict[str, Any] = {}
        if self.endpoint:
            kwargs["endpoint"] = self.endpoint
        exporter = OTLPSpanExporter(**kwargs)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        self._provider = provider

    def export(self, trace_doc: dict[str, Any]) -> None:
        """Best-effort map of LTF document to OTel spans."""
        self._ensure_provider()
        from opentelemetry import trace

        otel = trace.get_tracer("loopotel")
        root = next((s for s in trace_doc.get("spans", []) if s.get("kind") == "loop"), None)
        if root is None:
            return
        with otel.start_as_current_span(root["name"]) as span:
            for key, value in (root.get("attributes") or {}).items():
                span.set_attribute(key, value)
            for child in trace_doc.get("spans") or []:
                if child.get("parent_span_id") != root.get("span_id"):
                    continue
                with otel.start_as_current_span(child["name"]) as child_span:
                    for key, value in (child.get("attributes") or {}).items():
                        child_span.set_attribute(key, value)
