#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-03.json"
AUDIT = ROOT / "data/editorial_audits/bioinstrumentacion-unit-03.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-03.json"
ASSESSMENT = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-03.json"


def main() -> int:
    unit = json.loads(UNIT.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    practices = json.loads(PRACTICES.read_text(encoding="utf-8"))
    assessment = json.loads(ASSESSMENT.read_text(encoding="utf-8"))

    assert unit["schema_version"] == "2.0"
    assert unit["subject_id"] == "bioinstrumentacion"
    assert unit["unit"] == 3
    assert unit["status"] == "review"
    assert len(unit["learning_objectives"]) == 5
    assert len(unit["theory_sections"]) >= 6
    assert len(unit["worked_examples"]) >= 3
    assert [p["id"] for p in unit["practices"]] == ["U3-P1", "U3-P2", "U3-P3"]
    assert [a["id"] for a in unit["assessments"]] == ["U3-A1", "U3-A2", "U3-A3", "U3-A4", "U3-A5"]
    assert len(unit["misconception_feedback"]) == 12
    assert unit["assessments"][-1]["requires_human_review"] is True
    assert unit["review_state"] == {
        "internal_scientific_editorial_audit": "passed",
        "professional_review": "pending",
        "human_review_U3_A5": "pending",
        "public_release_authorized": False,
        "course_editorial_state": "pending",
    }

    text = UNIT.read_text(encoding="utf-8").lower()
    for required in [
        "potencial transmembrana",
        "fuente distribuida",
        "conducción de volumen",
        "medición diferencial",
        "potencial de media celda",
        "rct",
        "cdl",
        "prueba discriminante",
        "no diagnóstica",
    ]:
        assert required in text, required

    assert practices["status"] == "unit_03_practices_implemented_internal_review"
    assert assessment["status"] == "unit_03_assessment_implemented_internal_review"
    authorization = audit["authorization_result"]
    assert authorization["full_theory_drafting_authorized"] is True
    assert authorization["authoral_unit_creation_authorized"] is True
    assert authorization["public_release_authorized"] is False
    assert audit["review_claims"]["external_professional_review_completed"] is False
    assert audit["review_claims"]["human_assessment_review_completed"] is False

    print("OK Bioinstrumentation U3 authoral unit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
