#!/usr/bin/env python3
"""Calculate exact agreement, weighted agreement and linear weighted kappa for U2 rubrics."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "data/review_protocols/bioinstrumentacion-unit-02-human-review.json"

class AgreementError(ValueError):
    pass

def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AgreementError(f"{path} must contain an object")
    return value

def thresholds(path: Path) -> dict[str, float | int]:
    value = load_json(path).get("inter_rater_review", {}).get("thresholds")
    if not isinstance(value, dict):
        raise AgreementError("protocol lacks thresholds")
    return value

def analyze(payload: dict[str, Any], limits: dict[str, float | int]) -> dict[str, Any]:
    scale = payload.get("scale")
    ratings = payload.get("ratings")
    if scale != [0, 1, 2] or not isinstance(ratings, list) or len(ratings) < 1:
        raise AgreementError("ratings require ordered scale [0,1,2] and paired rows")
    a: list[int] = []
    b: list[int] = []
    seen: set[str] = set()
    for row in ratings:
        if not isinstance(row, dict):
            raise AgreementError("rating rows must be objects")
        key = str(row.get("item_id", "")).strip()
        if not key or key in seen:
            raise AgreementError("item_id must be unique and non-empty")
        seen.add(key)
        left, right = row.get("rater_a"), row.get("rater_b")
        if left not in scale or right not in scale:
            raise AgreementError(f"invalid rating for {key}")
        a.append(left)
        b.append(right)
    n = len(a)
    exact = sum(x == y for x, y in zip(a, b, strict=True)) / n
    weighted = sum(1 - abs(x-y)/2 for x, y in zip(a, b, strict=True)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum((1-abs(x-y)/2)*(ca[x]/n)*(cb[y]/n) for x in scale for y in scale)
    kappa = None if abs(1-expected) < 1e-12 else (weighted-expected)/(1-expected)
    checks = {
        "minimum_double_rated_items": n >= int(limits["minimum_double_rated_items"]),
        "minimum_exact_agreement": exact >= float(limits["minimum_exact_agreement"]),
        "minimum_weighted_agreement": weighted >= float(limits["minimum_weighted_agreement"]),
        "minimum_weighted_kappa": kappa is not None and kappa >= float(limits["minimum_weighted_kappa"]),
    }
    return {
        "synthetic": payload.get("synthetic") is True,
        "rating_count": n,
        "exact_agreement": round(exact, 6),
        "weighted_agreement": round(weighted, 6),
        "linear_weighted_kappa": None if kappa is None else round(kappa, 6),
        "checks": checks,
        "gate_passed": all(checks.values()),
        "interpretation_limit": "Agreement metrics do not establish content validity, clinical competence or professional endorsement."
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    report = analyze(load_json(args.input), thresholds(args.protocol))
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 1 if args.enforce and not report["gate_passed"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
