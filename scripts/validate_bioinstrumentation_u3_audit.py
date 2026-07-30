#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/editorial_audits/bioinstrumentacion-unit-03.json"
PREPARATION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-03.json"
BLOCKERS = ROOT / "data/unit_preparation/bioinstrumentacion-unit-03-blocker-resolution.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-03.json"
ASSESSMENT = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-03.json"
AUTHORAL = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-03.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    audit = read_json(AUDIT)
    preparation = read_json(PREPARATION)
    blockers = read_json(BLOCKERS)
    practices = read_json(PRACTICES)
    assessment = read_json(ASSESSMENT)

    assert audit["subject_id"] == "bioinstrumentacion"
    assert audit["unit_number"] == 3
    assert audit["status"] == "passed_internal_scientific_editorial_audit"
    assert audit["course_editorial_state"] == "pending"

    assert preparation["status"] == "authoring_preparation_review"
    assert blockers["status"] == "technical_blockers_resolved_internal_review"
    assert practices["status"] == "unit_03_practices_implemented_internal_review"
    assert assessment["status"] == "unit_03_assessment_implemented_internal_review"

    dimensions = audit["audit_dimensions"]
    assert [item["id"] for item in dimensions] == [f"U3-AUD-{i:02d}" for i in range(1, 9)]
    assert all(item["decision"] == "pass" for item in dimensions)
    assert all(item["evidence"] for item in dimensions)

    findings = audit["findings"]
    assert findings["critical"] == []
    assert findings["major"] == []
    assert len(findings["minor"]) == 2
    assert all(item["required_action"] for item in findings["minor"])

    authorization = audit["authorization_result"]
    assert authorization == {
        "full_theory_drafting_authorized": True,
        "authoral_unit_creation_authorized": True,
        "professional_review_required_before_publication": True,
        "human_review_required_for_U3_A5": True,
        "public_release_authorized": False,
    }

    claims = audit["review_claims"]
    assert claims["internal_scientific_editorial_review_completed"] is True
    assert claims["external_professional_review_completed"] is False
    assert claims["human_assessment_review_completed"] is False
    assert audit["unit_developed"] is False
    assert not AUTHORAL.exists()

    assert len(preparation["learning_outcomes"]) == 5
    assert len(preparation["misconception_bank"]) == 12
    assert [p["id"] for p in practices["practices"]] == ["U3-P1", "U3-P2", "U3-P3"]
    assert [a["id"] for a in assessment["assessments"]] == ["U3-A1", "U3-A2", "U3-A3", "U3-A4", "U3-A5"]
    assert len(assessment["feedback_routes"]) == 12

    print("OK Bioinstrumentation U3 scientific editorial audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
