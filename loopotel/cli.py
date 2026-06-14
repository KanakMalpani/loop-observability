"""CLI for LTF validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from loopotel.validate import validate_trace


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate LTF trace JSON or JSONL")
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)

    if not args.path.exists():
        print(f"Missing: {args.path}", file=sys.stderr)
        return 1

    lines = args.path.read_text(encoding="utf-8").strip().splitlines()
    docs = [json.loads(line) for line in lines if line.strip()] if args.path.suffix == ".jsonl" else [json.loads(args.path.read_text(encoding="utf-8"))]

    failed = False
    for index, doc in enumerate(docs, start=1):
        valid, errors = validate_trace(doc)
        label = str(args.path) if len(docs) == 1 else f"{args.path}#{index}"
        if valid:
            print(f"VALID: {label}")
        else:
            failed = True
            print(f"INVALID: {label}", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
