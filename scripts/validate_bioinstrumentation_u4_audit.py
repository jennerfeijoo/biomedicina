#!/usr/bin/env python3
"""Validate the internal scientific/editorial audit for Bioinstrumentation Unit 4."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/editorial_audits/bioinstrumentacion-unit-04.json"
PREP = ROOT / "data/unit_preparation/bioinstrumentacion-unit-04.json"
BLOCKERS = ROOT / "data/unit_preparation/bioinstrumentacion-unit-04-blocker-resolution.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-04.json"
AUTH = ROOT / "data/assessment_authorizations/bioinstrumentacion-unit-04.json"
ASSESS = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-04.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-04/SCIENTIFIC_EDITORIAL_AUDIT.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-04.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def main() -> int:
    audit = load(AUDIT)
    prep = load(PREP)
    blockers = load(BLOCKERS)
    practices = load(PRACTICES)
    auth = load(AUTH)
    assessment = load(ASSESS)

    assert audit["subject_id"] == "bioinstrumentacion"
    assert audit["unit"] == 4
    assert audit["status"] == "scientific_editorial_audit_completed_internal"
    assert audit["course_editorial_state"] == "pending"

    assert prep.get("unit") == 4 or prep.get("unit_number") == 4
    assert blockers["status"] == "technical_blockers_resolved_internal_review"
    assert [item["id"] for item in practices["practices"]] == ["U4-P1", "U4-P2", "U4-P3"]
    assert auth["authorization_decision"]["assessment_implementation_authorized"] is True
    assert assessment["unit"] == 4

    dimensions = audit["dimensions"]
    assert [item["id"] for item in dimensions] == [f"U4-AUD-{i:02d}" for i in range(1, 9)]
    assert all(item["decision"] == "pass_internal" for item in dimensions)

    findings = audit["open_findings"]
    assert [item["id"] for item in findings] == ["U4-F01", "U4-F02"]
    assert all(item["severity"] == "minor" for item in findings)

    decision = audit["authorization_decision"]
    assert decision["full_theory_drafting_authorized"] is True
    assert decision["conditions"] == ["resolve_U4-F01_in_authoral_draft", "resolve_U4-F02_in_authoral_draft"]
    assert decision["human_review_executed"] is False
    assert decision["professional_review_claimed"] is False
    assert decision["public_release_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "U4-F01",
        "U4-F02",
        "full_theory_drafting_authorized: true",
        "human_review_executed: false",
        "professional_review_claimed: false",
        "public_release_authorized: false",
        "course_state: pending",
    ):
        assert marker in text, marker

    assert not UNIT.exists(), "Unit 4 authoral draft exists before audit merge"
    print("OK Bioinstrumentation U4 scientific/editorial audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
