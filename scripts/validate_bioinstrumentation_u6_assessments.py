from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-06.json"
AUTH = ROOT / "data/assessment_authorizations/bioinstrumentacion-unit-06.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-06.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-06/ASSESSMENT_IMPLEMENTATION.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json"


def load(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    implementation = load(ASSESSMENTS)
    authorization = load(AUTH)
    load(PRACTICES)

    assert implementation["subject_id"] == "bioinstrumentacion"
    assert implementation["unit"] == 6
    assert implementation["status"] == "implemented_internal_review"
    assert implementation["course_editorial_state"] == "pending"
    assert authorization["decision"]["assessment_implementation_authorized"] is True

    assessments = implementation["assessments"]
    ids = [item["id"] for item in assessments]
    assert ids == ["U6-A1", "U6-A2", "U6-A3", "U6-A4", "U6-A5"]

    automatic = [item["id"] for item in assessments if item.get("automatic_scoring")]
    assert automatic == ["U6-A1", "U6-A2"]
    for item in assessments[2:]:
        assert item["automatic_scoring"] is False

    limits = implementation["safety_limits"]
    assert limits["synthetic_offline_only"] is True
    for key in (
        "human_participants_allowed",
        "energized_medical_devices_allowed",
        "regulatory_limits_claimed",
        "safety_conformity_claimed",
        "emc_conformity_claimed",
    ):
        assert limits[key] is False, key

    decision = implementation["decision"]
    assert decision["assessment_implementation_completed_internal"] is True
    for key in (
        "full_theory_drafting_authorized",
        "human_review_executed",
        "professional_review_claimed",
        "public_release_authorized",
        "course_completion_authorized",
    ):
        assert decision[key] is False, key

    assert DOC.exists()
    assert not UNIT.exists(), "unit-06.json must remain absent at this gate"
    print("Bioinstrumentation U6 assessments validated.")


if __name__ == "__main__":
    main()
