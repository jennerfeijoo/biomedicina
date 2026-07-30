#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/authoral_audits/bioinstrumentacion-unit-03.json"
HUMAN = ROOT / "data/review_protocols/bioinstrumentacion-unit-03-human-review.json"
PRO = ROOT / "data/review_packets/bioinstrumentacion-unit-03-professional-review.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-03/REVIEW_PACKAGE.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-03.json"


def load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def main() -> int:
    audit = load(AUDIT)
    human = load(HUMAN)
    pro = load(PRO)
    unit = load(UNIT)

    assert audit["status"] == "passed_internal_authoral_audit"
    assert len(audit["dimensions"]) == 8
    assert all(item["decision"] == "pass" for item in audit["dimensions"])
    assert audit["authorization_result"] == {
        "human_review_packet_authorized": True,
        "professional_review_packet_authorized": True,
        "public_release_authorized": False,
    }
    assert audit["review_claims"]["professional_review_completed"] is False
    assert audit["review_claims"]["human_review_U3_A5_completed"] is False

    assert human["assessment_id"] == "U3-A5"
    assert human["status"] == "ready_for_real_human_execution"
    assert len(human["rubric_dimensions"]) == 6
    assert {item["id"] for item in human["rubric_dimensions"]} == {
        "source", "geometry", "scale", "band", "interface", "inference_limit"
    }
    assert human["decision_rule"]["automatic_pass_allowed"] is False
    assert human["claims"] == {
        "human_review_completed": False,
        "participant_data_collected": False,
        "assessment_validated": False,
        "public_release_authorized": False,
    }

    assert pro["status"] == "ready_for_external_professional_review"
    assert len(pro["review_questions"]) >= 7
    assert pro["required_output"]["line_level_findings_required"] is True
    assert pro["current_claims"]["external_professional_review_completed"] is False
    assert pro["current_claims"]["professional_approval_obtained"] is False
    assert pro["current_claims"]["public_release_authorized"] is False

    assert unit["status"] == "review"
    assert unit["review_state"]["professional_review"] == "pending"
    assert unit["review_state"]["human_review_U3_A5"] == "pending"
    assert unit["review_state"]["public_release_authorized"] is False

    text = DOC.read_text(encoding="utf-8").lower()
    for marker in (
        "revisión humana de `u3-a5`",
        "revisión profesional",
        "no se afirma",
        "no se autoriza publicación",
        "public_release_authorized: false",
    ):
        assert marker in text, marker

    print("OK Bioinstrumentation U3 review package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
