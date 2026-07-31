from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/editorial_audits/bioinstrumentacion-unit-06.json"
PREP = ROOT / "data/unit_preparation/bioinstrumentacion-unit-06.json"
BLOCKERS = ROOT / "data/unit_preparation/bioinstrumentacion-unit-06-blocker-resolution.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-06.json"
AUTH = ROOT / "data/assessment_authorizations/bioinstrumentacion-unit-06.json"
ASSESSMENTS = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-06.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json"


def load(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    audit = load(AUDIT)
    for path in (PREP, BLOCKERS, PRACTICES, AUTH, ASSESSMENTS):
        load(path)

    assert audit["subject_id"] == "bioinstrumentacion"
    assert audit["unit"] == 6
    assert audit["status"] == "scientific_editorial_audit_passed_internal"
    assert audit["course_editorial_state"] == "pending"

    for value in audit["audit_dimensions"].values():
        assert value == "pass_internal"

    findings = {item["id"]: item["severity"] for item in audit["findings"]}
    assert findings == {"U6-F01": "resolved", "U6-F02": "resolved"}

    decision = audit["decision"]
    assert decision["controlled_full_theory_drafting_authorized"] is True
    assert decision["authoral_unit_creation_authorized"] is True
    for key in (
        "human_review_executed",
        "professional_review_claimed",
        "safety_conformity_claimed",
        "emc_conformity_claimed",
        "public_release_authorized",
        "course_completion_authorized",
    ):
        assert decision[key] is False, key

    if UNIT.exists():
        unit = load(UNIT)
        assert unit["status"] == "authoral_draft_internal"
        assert unit["course_editorial_state"] == "pending"
        assert unit["release_state"] == "not_authorized"
        assert unit["editorial_decision"]["human_review_executed"] is False
        assert unit["editorial_decision"]["professional_review_executed"] is False
        assert unit["editorial_decision"]["public_release_authorized"] is False
        assert unit["editorial_decision"]["course_completion_authorized"] is False

    print("Bioinstrumentation U6 scientific editorial audit validated.")


if __name__ == "__main__":
    main()
