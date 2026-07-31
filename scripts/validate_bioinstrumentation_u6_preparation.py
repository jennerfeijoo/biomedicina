#!/usr/bin/env python3
"""Validate the controlled preparation contract for Bioinstrumentation Unit 6."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/unit_preparation/bioinstrumentacion-unit-06.json"
AUTHORAL_UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json"
AUDIT = ROOT / "data/editorial_audits/bioinstrumentacion-unit-06.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(CONTRACT.is_file(), f"Missing contract: {CONTRACT}")
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    require(data.get("subject_id") == "bioinstrumentacion", "Unexpected subject_id")
    require(data.get("unit") == 6, "Unexpected unit number")
    require(data.get("status") == "authoring_preparation_review", "Unexpected status")
    require(data.get("course_editorial_state") == "pending", "Course must remain pending")

    outcomes = data.get("learning_outcomes", [])
    require(len(outcomes) == 5, "Unit 6 must declare five learning outcomes")

    practices = data.get("planned_practices", [])
    require([item.get("id") for item in practices] == ["U6-P1", "U6-P2", "U6-P3"], "Unexpected practice IDs")
    require(data.get("planned_assessments") == ["U6-A1", "U6-A2", "U6-A3", "U6-A4", "U6-A5"], "Unexpected assessment IDs")

    blockers = data.get("technical_blockers", [])
    require(len(blockers) == 4, "Four technical blockers are required")
    require(all(item.get("status") == "open" for item in blockers), "Preparation contract must preserve its original open-blocker snapshot")

    decision = data.get("authoring_decision", {})
    for key in (
        "full_theory_drafting_authorized",
        "practice_implementation_authorized",
        "assessment_implementation_authorized",
        "professional_review_claimed",
        "public_release_authorized",
    ):
        require(decision.get(key) is False, f"Preparation snapshot requires {key}=false")

    if AUTHORAL_UNIT.exists():
        require(AUDIT.is_file(), "Authoral unit requires a completed editorial audit")
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        require(audit.get("decision", {}).get("authoral_unit_creation_authorized") is True, "Audit must authorize authoral unit creation")
        unit = json.loads(AUTHORAL_UNIT.read_text(encoding="utf-8"))
        require(unit.get("status") == "authoral_draft_internal", "Unexpected authoral unit status")
        require(unit.get("release_state") == "not_authorized", "Authoral unit must remain unreleased")
        require(unit.get("course_editorial_state") == "pending", "Course must remain pending")

    print("Bioinstrumentation Unit 6 preparation contract is valid.")


if __name__ == "__main__":
    main()
