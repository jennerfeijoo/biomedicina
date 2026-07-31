#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/unit_preparation/bioinstrumentacion-unit-05-blocker-resolution.json"
IMPLEMENTATION = ROOT / "data/practice_implementations/bioinstrumentacion-unit-05.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-05/PRACTICES.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    auth = load_object(AUTH)
    implementation = load_object(IMPLEMENTATION)

    assert auth["subject_id"] == implementation["subject_id"] == "bioinstrumentacion"
    assert auth["unit"] == implementation["unit"] == 5
    assert auth["practice_authorization"]["authorized"] is True
    assert auth["practice_authorization"]["scope"] == ["U5-P1", "U5-P2", "U5-P3"]
    assert implementation["status"] == "implemented_internal_review"

    practices = implementation["practices"]
    assert [item["id"] for item in practices] == ["U5-P1", "U5-P2", "U5-P3"]
    assert all(item["mode"] == "synthetic_only" for item in practices)
    assert all(item["status"] == "implemented_internal_review" for item in practices)
    assert all(item["objective"] and item["inputs"] and item["tasks"] and item["outputs"] and item["acceptance_criteria"] for item in practices)

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
        "geometría",
        "luz parásita",
    ):
        assert marker in text, marker

    limits = implementation["global_limits"]
    for key in (
        "human_participants",
        "physical_sensor_acquisition",
        "biomedical_hardware_connection",
        "clinical_validity_claimed",
        "electrical_safety_claimed",
        "regulatory_conformity_claimed",
        "professional_review_claimed",
        "public_release_authorized",
    ):
        assert limits[key] is False, key
    assert limits["synthetic_only"] is True

    next_auth = implementation["next_authorization"]
    assert next_auth == {
        "assessment_implementation": False,
        "full_theory_drafting": False,
        "course_completion": False,
    }
    assert not UNIT.exists(), "unit-05.json must remain absent"

    doc = DOC.read_text(encoding="utf-8")
    for marker in (
        "mode: synthetic_only",
        "human_participants: false",
        "physical_sensor_acquisition: false",
        "professional_review_claimed: false",
        "public_release_authorized: false",
        "course_state: pending",
    ):
        assert marker in doc, marker

    print("OK Bioinstrumentation U5 synthetic practices")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
