#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/assessment_authorizations/bioinstrumentacion-unit-05.json"
IMPLEMENTATION = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-05.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-05/ASSESSMENTS.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    authorization = load_object(AUTH)
    implementation = load_object(IMPLEMENTATION)

    assert authorization["subject_id"] == implementation["subject_id"] == "bioinstrumentacion"
    assert authorization["unit"] == implementation["unit"] == 5
    assert implementation["status"] == "assessment_implementation_internal_review"

    assessments = implementation["assessments"]
    expected_ids = [f"U5-A{i}" for i in range(1, 6)]
    assert [item["id"] for item in assessments] == expected_ids
    assert all(item["mode"] == "synthetic_only" for item in assessments)

    for item in assessments[:4]:
        assert item["scoring"] == "deterministic"
        assert item["task"]
        assert len(item["criteria"]) >= 4
        feedback = item["feedback"]
        assert set(feedback) == {"conceptual", "numerical", "interpretive"}
        assert all(feedback.values())

    integrative = assessments[4]
    assert integrative["scoring"] == "human_review_only"
    assert integrative["automatic_approval_allowed"] is False
    assert integrative["review_status"] == "prepared_not_executed"
    assert integrative["required_human_review"]["type"] == "real_human_review"
    assert len(integrative["required_human_review"]["reviewer_must_assess"]) >= 5

    required_dimensions = {
        "measurement_definition",
        "reference_and_units",
        "dynamic_response",
        "metrological_limits",
        "geometry_or_flow_assumptions",
        "inference_limits",
    }
    covered = {criterion for item in assessments for criterion in item["criteria"]}
    assert required_dimensions <= covered

    limits = implementation["limits"]
    assert limits["synthetic_only"] is True
    for key in (
        "human_participants",
        "physical_sensor_acquisition",
        "biomedical_hardware_connection",
        "clinical_validity_claimed",
        "electrical_safety_claimed",
        "regulatory_conformity_claimed",
        "professional_review_claimed",
        "public_release_authorized",
        "course_completion_authorized",
    ):
        assert limits[key] is False, key

    assert not UNIT.exists(), "unit-05.json must remain absent"

    text = IMPLEMENTATION.read_text(encoding="utf-8")
    for marker in (
        "presión absoluta",
        "manométrica",
        "diferencial",
        "constante de tiempo",
        "flujo volumétrico",
        "flujo másico",
        "velocidad local",
        "transmitancia",
        "absorbancia",
        "reflectancia",
        "dispersión",
        "real_human_review",
        "prepared_not_executed",
    ):
        assert marker in text, marker

    doc = DOC.read_text(encoding="utf-8")
    for marker in (
        "automatic_approval_allowed: false",
        "required_review: real_human_review",
        "professional_review_claimed: false",
        "public_release_authorized: false",
        "course_state: pending",
    ):
        assert marker in doc, marker

    print("OK Bioinstrumentation U5 assessments")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
