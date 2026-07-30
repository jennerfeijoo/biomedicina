#!/usr/bin/env python3
"""Validate Unit 4 assessment implementation and deterministic feedback."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-04.json"
AUTHORIZATION = ROOT / "data/assessment_authorizations/bioinstrumentacion-unit-04.json"
ENGINE = ROOT / "scripts/bioinstrumentation_u4_assessment_engine.py"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-04/ASSESSMENT_IMPLEMENTATION.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-04.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def run(aid: str, response: str) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(ENGINE), aid, response],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    implementation = load(IMPLEMENTATION)
    authorization = load(AUTHORIZATION)
    assert authorization["authorization_decision"]["assessment_implementation_authorized"] is True
    assert implementation["subject_id"] == "bioinstrumentacion"
    assert implementation["unit"] == 4
    assert implementation["status"] == "assessment_implemented_internal_review"
    assessments = implementation["assessments"]
    assert [x["id"] for x in assessments] == [f"U4-A{i}" for i in range(1, 6)]
    assert all(x["mode"] == "deterministic_auto_scored" for x in assessments[:4])
    assert assessments[4]["mode"] == "rubric_scored_human_review"
    assert assessments[4]["automatic_pass_allowed"] is False
    assert assessments[4]["review_status"] == "pending_real_human_review"

    for aid, answer in (("U4-A1", "30"), ("U4-A2", "0.001953125"), ("U4-A3", "gap:1"), ("U4-A4", "false")):
        result = run(aid, answer)
        assert result["decision"] == "pass", (aid, result)
        assert set(result) == {"criterion_id", "observed_response", "decision", "explanation", "recovery_route", "inference_limit"}

    assert run("U4-A1", "70")["decision"] == "revise"
    assert run("U4-A2", "0.002")["decision"] == "revise"
    human = run("U4-A5", "design submission")
    assert human["decision"] == "pending_human_review"
    assert "revisión humana real" in human["explanation"]

    state = implementation["authorization_state"]
    assert state == {
        "full_theory_drafting_authorized": False,
        "professional_review_claimed": False,
        "public_release_authorized": False,
        "human_review_executed": False,
    }
    text = DOC.read_text(encoding="utf-8")
    for marker in ("U4-A1", "U4-A5", "pending_human_review", "public_release_authorized: false", "course_state: pending"):
        assert marker in text, marker
    assert not UNIT.exists(), "Unit 4 authoral file exists before theory authorization"
    print("OK Bioinstrumentation U4 assessment implementation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
