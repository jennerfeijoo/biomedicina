#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/final_authoral_audits/bioinstrumentacion-unit-04.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-04.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-04.json"
ASSESSMENTS = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-04.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-04/FINAL_AUTHORAL_AUDIT.md"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    audit = load_object(AUDIT)
    unit = load_object(UNIT)
    practices = load_object(PRACTICES)
    assessments = load_object(ASSESSMENTS)

    assert audit["subject_id"] == "bioinstrumentacion"
    assert audit["unit"] == 4
    assert audit["status"] == "final_authoral_audit_passed_internal"
    assert audit["course_editorial_state"] == "pending"

    dimensions = audit["dimensions"]
    assert [item["id"] for item in dimensions] == [f"U4-FINAL-{i:02d}" for i in range(1, 9)]
    assert all(item["decision"] == "pass_internal" for item in dimensions)

    assert audit["binding_findings"] == {
        "U4-F01": "resolved_in_authoral_draft",
        "U4-F02": "resolved_in_authoral_draft",
    }

    packages = audit["review_packages"]
    assert packages["U4-A5"]["status"] == "prepared_not_executed"
    assert packages["U4-A5"]["automatic_approval_allowed"] is False
    assert packages["disciplinary_review"]["status"] == "prepared_not_executed"
    assert packages["disciplinary_review"]["approval_claimed"] is False

    decision = audit["release_decision"]
    assert decision == {
        "internal_authoral_audit_passed": True,
        "human_review_executed": False,
        "professional_review_executed": False,
        "professional_approval_claimed": False,
        "public_release_authorized": False,
        "course_completion_authorized": False,
    }

    assert unit["unit"] == 4
    assert practices["unit"] == 4
    assert assessments["unit"] == 4

    unit_text = UNIT.read_text(encoding="utf-8")
    for marker in ("SINAD", "ENOB", "Frontera conceptual de aislamiento", "U4-A5"):
        assert marker in unit_text, marker

    doc_text = DOC.read_text(encoding="utf-8")
    for marker in (
        "prepared_not_executed",
        "human_review_executed: false",
        "professional_review_executed: false",
        "public_release_authorized: false",
        "course_state: pending",
    ):
        assert marker in doc_text, marker

    print("OK Bioinstrumentation U4 final authoral audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
