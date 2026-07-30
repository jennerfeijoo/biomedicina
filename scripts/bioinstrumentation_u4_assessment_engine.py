#!/usr/bin/env python3
"""Deterministic internal assessment engine for Bioinstrumentation Unit 4."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-04.json"


def load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def feedback(item: dict[str, Any], observed: Any, passed: bool) -> dict[str, Any]:
    return {
        "criterion_id": item["criterion_id"],
        "observed_response": observed,
        "decision": "pass" if passed else "revise",
        "explanation": "Respuesta consistente con el criterio interno." if passed else "La respuesta no satisface el criterio interno.",
        "recovery_route": item["recovery_route"],
        "inference_limit": item["inference_limit"],
    }


def evaluate(assessment_id: str, response: str) -> dict[str, Any]:
    contract = load_contract()
    item = next(x for x in contract["assessments"] if x["id"] == assessment_id)
    if item["mode"] == "rubric_scored_human_review":
        return {
            "criterion_id": "integrative_design",
            "observed_response": response,
            "decision": "pending_human_review",
            "explanation": "U4-A5 requiere una revisión humana real con la rúbrica registrada.",
            "recovery_route": "Completar y documentar las seis dimensiones de la rúbrica.",
            "inference_limit": "No existe aprobación automática ni profesional.",
        }

    normalized = response.strip().lower()
    if assessment_id == "U4-A2":
        try:
            observed = float(normalized)
            passed = math.isclose(observed, float(item["accepted_answer"]), abs_tol=float(item["tolerance"]), rel_tol=0.0)
        except ValueError:
            observed, passed = normalized, False
    else:
        observed = normalized
        passed = normalized == str(item["accepted_answer"]).lower()
    return feedback(item, observed, passed)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: bioinstrumentation_u4_assessment_engine.py <U4-A1..U4-A5> <response>", file=sys.stderr)
        return 2
    try:
        result = evaluate(argv[1], argv[2])
    except (StopIteration, KeyError, json.JSONDecodeError) as exc:
        print(f"assessment error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
