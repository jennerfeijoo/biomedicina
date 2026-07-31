#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/final_authoral_audits/bioinstrumentacion-unit-06.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json"
EDITORIAL = ROOT / "data/editorial_audits/bioinstrumentacion-unit-06.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-06.json"
ASSESSMENTS = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-06.json"


def load(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"Missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    audit = load(AUDIT)
    unit = load(UNIT)
    load(EDITORIAL)
    load(PRACTICES)
    load(ASSESSMENTS)

    assert audit["subject_id"] == "bioinstrumentacion"
    assert audit["unit"] == 6
    assert audit["status"] == "final_authoral_audit_passed_internal"
    assert audit["course_editorial_state"] == "pending"
    assert unit["unit"] == 6

    assert all(value == "pass_internal" for value in audit["audit_dimensions"].values())
    findings = {item["id"]: item["severity"] for item in audit["findings"]}
    assert findings == {"U6-FA01": "resolved", "U6-FA02": "resolved"}

    decision = audit["decision"]
    assert decision["authoral_draft_accepted_internal"] is True
    assert decision["internal_development_complete"] is True
    for key in (
        "human_review_executed",
        "professional_review_executed",
        "professional_approval_claimed",
        "safety_conformity_claimed",
        "emc_conformity_claimed",
        "public_release_authorized",
        "course_completion_authorized",
    ):
        assert decision[key] is False, key

    assert audit["next_required_gate"] == "real_human_and_professional_review"
    print("Bioinstrumentation U6 final authoral audit validated.")


if __name__ == "__main__":
    main()
