#!/usr/bin/env python3
"""Validate an LTF JSON or JSONL trace file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from loopotel.validate import validate_trace  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="LTF JSON file or JSONL (validates each line)")
    args = parser.parse_args(argv)

    if not args.path.exists():
        print(f"Missing file: {args.path}", file=sys.stderr)
        return 1

    text = args.path.read_text(encoding="utf-8").strip()
    docs: list[dict] = []
    if args.path.suffix == ".jsonl":
        for line_no, line in enumerate(text.splitlines(), start=1):
            line = line.strip()
            if line:
                try:
                    docs.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    print(f"{args.path}:{line_no}: invalid JSON — {exc}", file=sys.stderr)
                    return 1
    else:
        docs.append(json.loads(text))

    failed = False
    for index, doc in enumerate(docs, start=1):
        valid, errors = validate_trace(doc)
        label = f"{args.path}" if len(docs) == 1 else f"{args.path}#{index}"
        if valid:
            print(f"VALID: {label} ({doc.get('trace_id', '?')})")
        else:
            failed = True
            print(f"INVALID: {label}", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
