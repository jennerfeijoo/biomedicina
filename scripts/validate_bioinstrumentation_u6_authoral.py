from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json"
AUDIT = ROOT / "data/editorial_audits/bioinstrumentacion-unit-06.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-06.json"
ASSESSMENTS = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-06.json"


def load(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    unit = load(UNIT)
    load(AUDIT)
    load(PRACTICES)
    load(ASSESSMENTS)

    assert unit["subject_id"] == "bioinstrumentacion"
    assert unit["unit"] == 6
    assert unit["status"] == "authoral_draft_internal"
    assert unit["course_editorial_state"] == "pending"
    assert unit["release_state"] == "not_authorized"

    section_ids = [item["id"] for item in unit["sections"]]
    assert section_ids == [f"U6-S{i}" for i in range(1, 7)]

    practice_ids = [item["id"] for item in unit["practices"]]
    assert practice_ids == ["U6-P1", "U6-P2", "U6-P3"]

    assessment_ids = [item["id"] for item in unit["assessments"]]
    assert assessment_ids == ["U6-A1", "U6-A2", "U6-A3", "U6-A4", "U6-A5"]

    a5 = next(item for item in unit["assessments"] if item["id"] == "U6-A5")
    assert a5["status"] == "pending_human_execution"
    assert a5["automatic_semantic_approval"] is False

    boundary = unit["safety_boundary"]
    assert boundary["synthetic_offline_only"] is True
    for key in (
        "human_participants_allowed",
        "energized_medical_devices_allowed",
        "regulatory_limits_claimed",
        "safety_conformity_claimed",
        "emc_conformity_claimed",
        "professional_review_claimed",
    ):
        assert boundary[key] is False, key

    decision = unit["editorial_decision"]
    assert decision["authoral_draft_completed"] is True
    for key in (
        "human_review_executed",
        "professional_review_executed",
        "public_release_authorized",
        "course_completion_authorized",
    ):
        assert decision[key] is False, key

    text = json.dumps(unit, ensure_ascii=False)
    for token in ("0.5 µA", "7.23 µA", "10×", "fuente", "trayectoria", "víctima"):
        assert token in text, token

    print("Bioinstrumentation U6 authoral draft validated.")


if __name__ == "__main__":
    main()
