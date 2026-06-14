"""Validate LTF documents against ltf-0.1.schema.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

def load_schema() -> dict[str, Any]:
    bundled = Path(__file__).resolve().parent / "schemas" / "ltf-0.1.schema.json"
    repo = Path(__file__).resolve().parents[2] / "specs" / "ltf-0.1.schema.json"
    path = bundled if bundled.exists() else repo
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_trace(trace: dict[str, Any]) -> tuple[bool, list[str]]:
    try:
        import jsonschema
    except ImportError as exc:
        raise SystemExit("jsonschema required: pip install loopotel[dev]") from exc

    schema = load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted({f"{e.json_path}: {e.message}" for e in validator.iter_errors(trace)})
    return len(errors) == 0, errors


def validate_file(path: Path) -> tuple[bool, list[str]]:
    with path.open(encoding="utf-8") as handle:
        trace = json.load(handle)
    return validate_trace(trace)
