from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/assessment_authorizations/bioinstrumentacion-unit-06.json"
PREP = ROOT / "data/unit_preparation/bioinstrumentacion-unit-06.json"
BLOCKERS = ROOT / "data/unit_preparation/bioinstrumentacion-unit-06-blocker-resolution.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-06.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json"


def load(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    auth = load(AUTH)
    load(PREP)
    load(BLOCKERS)
    load(PRACTICES)

    assert auth["subject_id"] == "bioinstrumentacion"
    assert auth["unit"] == 6
    assert auth["status"] == "assessment_implementation_authorized_internal"
    assert auth["course_editorial_state"] == "pending"

    ids = [item["id"] for item in auth["authorized_assessments"]]
    assert ids == ["U6-A1", "U6-A2", "U6-A3", "U6-A4", "U6-A5"]

    decision = auth["decision"]
    assert decision["assessment_implementation_authorized"] is True
    for key in (
        "full_theory_drafting_authorized",
        "human_review_executed",
        "professional_review_claimed",
        "safety_conformity_claimed",
        "emc_conformity_claimed",
        "public_release_authorized",
        "course_completion_authorized",
    ):
        assert decision[key] is False, key

    feedback = auth["feedback_policy"]
    assert feedback["answer_key_exposed_in_feedback"] is False
    assert feedback["error_specific_feedback_required"] is True
    assert feedback["recovery_required"] is True
    assert feedback["professional_judgment_simulated"] is False

    assert not UNIT.exists(), "unit-06.json must remain absent at this gate"
    print("Bioinstrumentation U6 assessment authorization validated.")


if __name__ == "__main__":
    main()
