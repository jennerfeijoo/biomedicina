#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/assessment_authorizations/bioinstrumentacion-unit-05.json"
PREPARATION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-05.json"
RESOLUTION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-05-blocker-resolution.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-05.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-05/ASSESSMENT_AUTHORIZATION.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    auth = load_object(AUTH)
    preparation = load_object(PREPARATION)
    resolution = load_object(RESOLUTION)
    practices = load_object(PRACTICES)

    assert auth["subject_id"] == "bioinstrumentacion"
    assert auth["unit"] == preparation["unit"] == resolution["unit"] == practices["unit"] == 5
    assert auth["status"] == "assessment_implementation_authorized_internal"
    assert auth["course_editorial_state"] == "pending"

    assessments = auth["authorized_assessments"]
    assert [item["id"] for item in assessments] == [f"U5-A{i}" for i in range(1, 6)]
    assert all(item["implementation_mode"] == "synthetic_only" for item in assessments)
    assert all(item["automatic_scoring_allowed"] is True for item in assessments[:4])
    assert assessments[4]["automatic_scoring_allowed"] is False
    assert assessments[4]["required_review"] == "real_human_review"

    authorization = auth["authorization"]
    assert authorization == {
        "assessment_implementation": True,
        "full_theory_drafting": False,
        "professional_review_claimed": False,
        "public_release": False,
        "course_completion": False,
    }

    limits = auth["limits"]
    assert limits["synthetic_only"] is True
    assert limits["human_or_device_acquisition"] is False
    assert limits["clinical_validity_claimed"] is False
    assert limits["electrical_safety_claimed"] is False
    assert limits["regulatory_conformity_claimed"] is False
    assert limits["U5-A5_real_human_review_required"] is True
    assert not UNIT.exists(), "unit-05.json must remain absent"

    text = AUTH.read_text(encoding="utf-8")
    for marker in (
        "pressure_reference",
        "thermal_first_order_response",
        "flow_quantity_separation",
        "optical_geometry_and_modalities",
        "multimodal_measurement_and_inference_limits",
        "real_human_review",
    ):
        assert marker in text, marker

    doc = DOC.read_text(encoding="utf-8")
    for marker in (
        "assessment_implementation_authorized: true",
        "full_theory_drafting_authorized: false",
        "professional_review_claimed: false",
        "public_release_authorized: false",
        "course_state: pending",
    ):
        assert marker in doc, marker

    print("OK Bioinstrumentation U5 assessment authorization")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
