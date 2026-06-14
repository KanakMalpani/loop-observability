"""Write LTF traces to JSONL."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonlExporter:
    """Append LTF trace documents to a JSONL file."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def export(self, trace: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(trace, separators=(",", ":")) + "\n")

    def export_tracer(self, tracer: Any) -> None:
        self.export(tracer.build_trace())
