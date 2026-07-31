#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/editorial_audits/bioinstrumentacion-unit-05.json"
PREPARATION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-05.json"
BLOCKERS = ROOT / "data/unit_preparation/bioinstrumentacion-unit-05-blocker-resolution.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-05.json"
AUTHORIZATION = ROOT / "data/assessment_authorizations/bioinstrumentacion-unit-05.json"
ASSESSMENTS = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-05.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-05/AUDIT.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def main() -> int:
    for path in (PREPARATION, BLOCKERS, PRACTICES, AUTHORIZATION, ASSESSMENTS, DOC):
        assert path.exists(), path

    audit = load(AUDIT)
    assert audit["subject_id"] == "bioinstrumentacion"
    assert audit["unit"] == 5
    assert audit["status"] == "scientific_editorial_audit_completed_internal"

    dimensions = audit["dimensions"]
    assert len(dimensions) == 8
    assert all(item["decision"] == "pass_internal" for item in dimensions)

    findings = audit["open_findings"]
    assert [item["id"] for item in findings] == ["U5-F01", "U5-F02"]
    assert all(item["severity"] == "minor" for item in findings)

    decision = audit["authorization_decision"]
    assert decision["full_theory_drafting_authorized"] is True
    assert decision["conditions"] == [
        "resolve_U5-F01_in_authoral_draft",
        "resolve_U5-F02_in_authoral_draft",
    ]
    assert decision["human_review_executed"] is False
    assert decision["professional_review_claimed"] is False
    assert decision["public_release_authorized"] is False
    assert not UNIT.exists(), "unit-05.json must remain absent before authoral drafting"

    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "full_theory_drafting_authorized: true",
        "human_review_executed: false",
        "professional_review_claimed: false",
        "public_release_authorized: false",
        "course_state: pending",
        "Presupuesto de incertidumbre",
        "Frontera multimodal",
    ):
        assert marker in text, marker

    print("OK Bioinstrumentation U5 scientific editorial audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
