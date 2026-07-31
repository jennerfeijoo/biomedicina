#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREPARATION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-05.json"
RESOLUTION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-05-blocker-resolution.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-05/BLOCKER_RESOLUTION.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    preparation = load_object(PREPARATION)
    resolution = load_object(RESOLUTION)

    assert preparation["subject_id"] == resolution["subject_id"] == "bioinstrumentacion"
    assert preparation["unit"] == resolution["unit"] == 5
    assert resolution["status"] == "technical_blockers_resolved_internal_review"

    expected = [f"U5-B{i:02d}" for i in range(1, 7)]
    items = resolution["resolutions"]
    assert [item["id"] for item in items] == expected
    assert all(item["status"] == "resolved_internal" for item in items)
    assert all(item["resolution"] and item["inference_limit"] for item in items)

    authorization = resolution["practice_authorization"]
    assert authorization["authorized"] is True
    assert authorization["scope"] == ["U5-P1", "U5-P2", "U5-P3"]
    assert authorization["mode"] == "synthetic_only"

    assert resolution["assessment_implementation_authorized"] is False
    assert resolution["full_theory_drafting_authorized"] is False
    assert resolution["professional_review_claimed"] is False
    assert resolution["public_release_authorized"] is False
    assert resolution["course_completion_authorized"] is False
    assert not UNIT.exists(), "unit-05.json must remain absent"

    text = RESOLUTION.read_text(encoding="utf-8")
    for marker in (
        "absoluta",
        "manométrica",
        "diferencial",
        "constante de tiempo",
        "flujo volumétrico",
        "flujo másico",
        "velocidad local",
        "absorbancia",
        "reflectancia",
        "trazabilidad",
        "incertidumbre",
        "validez clínica",
    ):
        assert marker in text, marker

    doc = DOC.read_text(encoding="utf-8")
    for marker in (
        "practice_implementation_authorized: true",
        "assessment_implementation_authorized: false",
        "professional_review_claimed: false",
        "public_release_authorized: false",
        "course_state: pending",
    ):
        assert marker in doc, marker

    print("OK Bioinstrumentation U5 blocker resolution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
