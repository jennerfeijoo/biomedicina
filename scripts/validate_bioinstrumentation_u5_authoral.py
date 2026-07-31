#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json"
AUDIT = ROOT / "data/editorial_audits/bioinstrumentacion-unit-05.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-05/AUTHORAL_DRAFT.md"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    unit = load_object(UNIT)
    audit = load_object(AUDIT)

    assert unit["subject_id"] == "bioinstrumentacion"
    assert unit["unit"] == 5
    assert unit["status"] == "authoral_draft_internal_review"
    assert audit["authorization_decision"]["full_theory_drafting_authorized"] is True

    assert len(unit["learning_outcomes"]) >= 5
    assert [item["id"] for item in unit["sections"]] == [f"U5-S{i}" for i in range(1, 7)]
    assert [item["id"] for item in unit["worked_examples"]] == [f"U5-E{i}" for i in range(1, 7)]
    assert unit["practices"] == ["U5-P1", "U5-P2", "U5-P3"]
    assert unit["assessments"] == [f"U5-A{i}" for i in range(1, 6)]

    resolved = unit["audit_findings_resolved"]
    assert resolved["U5-F01"] == "resolved_with_numeric_uncertainty_budget_example_U5-E5"
    assert resolved["U5-F02"] == "resolved_with_multimodal_inference_boundary_example_U5-E6"

    limits = unit["limits"]
    assert limits["synthetic_only"] is True
    assert limits["human_or_device_acquisition"] is False
    assert limits["clinical_validity_claimed"] is False
    assert limits["professional_review_claimed"] is False
    assert limits["public_release_authorized"] is False
    assert limits["U5-A5_status"] == "pending_real_human_review"

    text = UNIT.read_text(encoding="utf-8")
    for marker in (
        "presión absoluta",
        "constante de tiempo",
        "flujo volumétrico",
        "absorbancia",
        "presupuesto de incertidumbre",
        "0.229 kPa",
        "afirmación clínica no demostrada",
    ):
        assert marker in text, marker

    doc = DOC.read_text(encoding="utf-8")
    for marker in (
        "status: authoral_draft_internal_review",
        "professional_review_claimed: false",
        "public_release_authorized: false",
        "course_state: pending",
    ):
        assert marker in doc, marker

    print("OK Bioinstrumentation U5 authoral draft")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
