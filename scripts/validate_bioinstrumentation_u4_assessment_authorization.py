#!/usr/bin/env python3
"""Validate internal assessment authorization for Bioinstrumentation Unit 4."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/assessment_authorizations/bioinstrumentacion-unit-04.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-04.json"
BLOCKERS = ROOT / "data/unit_preparation/bioinstrumentacion-unit-04-blocker-resolution.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-04/ASSESSMENT_AUTHORIZATION.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-04.json"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    auth = load_object(AUTH)
    practices = load_object(PRACTICES)
    blockers = load_object(BLOCKERS)

    assert auth["subject_id"] == "bioinstrumentacion"
    assert auth["unit"] == 4
    assert auth["status"] == "assessment_implementation_authorized_internal_only"
    assert auth["course_editorial_state"] == "pending"

    assert blockers["resolution_status"] == "resolved_for_synthetic_practice_implementation"
    assert practices["unit"] == 4
    assert [item["id"] for item in practices["practices"]] == ["U4-P1", "U4-P2", "U4-P3"]

    assessments = auth["authorized_assessments"]
    assert [item["id"] for item in assessments] == [f"U4-A{i}" for i in range(1, 6)]
    assert all(not item["human_review_required"] for item in assessments[:4])
    assert assessments[4]["human_review_required"] is True
    assert assessments[4]["mode"] == "rubric_scored_human_review"

    feedback = auth["feedback_contract"]
    assert feedback["required_fields"] == [
        "criterion_id",
        "observed_response",
        "decision",
        "explanation",
        "recovery_route",
        "inference_limit",
    ]
    assert {
        "clinical_validity",
        "diagnostic_performance",
        "electrical_safety",
        "regulatory_conformity",
        "professional_approval",
    } == set(feedback["prohibited_claims"])

    decision = auth["authorization_decision"]
    assert decision == {
        "assessment_implementation_authorized": True,
        "automatic_scoring_authorized_for": ["U4-A1", "U4-A2", "U4-A3", "U4-A4"],
        "human_review_required_for": ["U4-A5"],
        "full_theory_drafting_authorized": False,
        "professional_review_claimed": False,
        "public_release_authorized": False,
    }

    constraints = auth["implementation_constraints"]
    assert constraints["network_required"] is False
    assert constraints["external_packages_required"] is False
    assert constraints["personal_data_allowed"] is False
    assert constraints["human_or_device_acquisition_allowed"] is False
    assert constraints["unit_authoring_authorized"] is False
    assert constraints["public_release_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "U4-A1",
        "U4-A5",
        "revisión humana real",
        "assessment_implementation_authorized: true",
        "public_release_authorized: false",
        "course_state: pending",
    ):
        assert marker in text, marker

    assert not UNIT.exists(), "Unit 4 authoral file exists before theory authorization"
    print("OK Bioinstrumentation U4 assessment authorization")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
