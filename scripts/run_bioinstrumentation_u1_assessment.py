#!/usr/bin/env python3
"""Run deterministic assessment routing for Bioinstrumentation unit 1."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bioinstrumentation_assessment_core import (
    AssessmentError,
    evaluate_submission,
    load_json,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMPLEMENTATION = (
    ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-01.json"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path)
    parser.add_argument("--implementation", type=Path, default=DEFAULT_IMPLEMENTATION)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        implementation = load_json(args.implementation)
        submission = load_json(args.submission)
        result = evaluate_submission(submission, implementation)
    except (OSError, AssessmentError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
