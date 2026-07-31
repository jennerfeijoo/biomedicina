#!/usr/bin/env python3
"""Validate Bioinstrumentation Unit 6 blocker-resolution contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/unit_preparation/bioinstrumentacion-unit-06-blocker-resolution.json"
FORBIDDEN_UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(CONTRACT.exists(), f"Missing contract: {CONTRACT}")
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    require(data.get("schema_version") == "1.0", "Unexpected schema version")
    require(data.get("subject_id") == "bioinstrumentacion", "Unexpected subject")
    require(data.get("unit") == 6, "Unexpected unit")
    require(data.get("status") == "technical_blockers_resolved_internal", "Invalid status")

    resolutions = data.get("resolutions", [])
    require(len(resolutions) == 4, "Exactly four blocker resolutions are required")
    require({item.get("id") for item in resolutions} == {"U6-B01", "U6-B02", "U6-B03", "U6-B04"}, "Unexpected blocker IDs")
    require(all(item.get("decision") in {"resolved_internal", "resolved_as_boundary"} for item in resolutions), "Every blocker must have a valid decision")

    leakage = next(item for item in resolutions if item["id"] == "U6-B02")
    cases = leakage.get("synthetic_cases", [])
    require(len(cases) == 2, "Two synthetic leakage-current cases are required")
    require(abs(cases[0].get("expected_current_uA", 0) - 0.5) < 1e-9, "Unexpected resistive current")
    require(abs(cases[1].get("expected_current_uA_approx", 0) - 7.23) < 0.02, "Unexpected capacitive current")

    emc = next(item for item in resolutions if item["id"] == "U6-B03").get("model_contract", {})
    for key in ("conducted", "capacitive", "inductive", "radiated", "required_metadata"):
        require(key in emc, f"Missing EMC contract field: {key}")

    decision = data.get("authorization_decision", {})
    require(decision.get("synthetic_practice_implementation_authorized") is True, "Synthetic practices must be authorized")
    require(decision.get("assessment_implementation_authorized") is False, "Assessments must remain unauthorized")
    require(decision.get("full_theory_drafting_authorized") is False, "Theory must remain unauthorized")
    require(decision.get("human_or_energized_medical_device_work_authorized") is False, "Human/device work must remain forbidden")
    require(decision.get("public_release_authorized") is False, "Publication must remain unauthorized")

    limits = data.get("limits", {})
    for key in ("synthetic_only", "no_people", "no_energized_medical_equipment", "no_safety_claim", "no_regulatory_conformity_claim"):
        require(limits.get(key) is True, f"Required limit missing: {key}")
    require(limits.get("professional_review_claimed") is False, "Professional review cannot be claimed")
    require(limits.get("course_completion_authorized") is False, "Course completion cannot be authorized")
    require(not FORBIDDEN_UNIT.exists(), "unit-06.json must remain absent at this stage")

    print("Bioinstrumentation Unit 6 blocker resolution validated.")


if __name__ == "__main__":
    main()
