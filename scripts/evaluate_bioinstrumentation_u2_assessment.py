#!/usr/bin/env python3
"""Evaluate one structured Bioinstrumentation U2 assessment submission."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bioinstrumentation_u2_assessment_core import AssessmentError, evaluate_submission, load_json

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMPLEMENTATION = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-02.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path)
    parser.add_argument("--implementation", type=Path, default=DEFAULT_IMPLEMENTATION)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = evaluate_submission(load_json(args.submission), load_json(args.implementation))
    except AssessmentError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
