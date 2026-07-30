#!/usr/bin/env python3
"""Validate the authoring-preparation contract for Bioinstrumentation Unit 3."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREPARATION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-03.json"
SOURCES = ROOT / "data/source_registry/bioinstrumentacion-unit-03.json"
READINESS = ROOT / "docs/pilots/bioinstrumentacion/unit-03/AUTHORING_READINESS.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-03.json"
AUDIT = ROOT / "data/editorial_audits/bioinstrumentacion-unit-03.json"


def load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain an object")
    return payload


def main() -> int:
    preparation = load_object(PREPARATION)
    sources = load_object(SOURCES)

    assert preparation["subject_id"] == "bioinstrumentacion"
    assert preparation["unit_number"] == 3
    assert preparation["title"] == "Biopotenciales, electrodos e interfaz electrodo-tejido"
    assert preparation["status"] == "authoring_preparation_review"
    assert preparation["course_editorial_state"] == "pending"

    outcomes = preparation["learning_outcomes"]
    assert [item["id"] for item in outcomes] == [f"U3-LO{i}" for i in range(1, 6)]
    assert all(all(len(item[field].strip()) >= 40 for field in ("statement", "mastery_evidence", "criterion")) for item in outcomes)

    relations = " ".join(preparation["knowledge_model"]["required_relations"]).lower()
    for marker in ("potencial transmembrana", "fuentes distribuidas", "diferencia", "conducción iónica", "frecuencia", "desbalance", "tierra de protección", "autenticidad fisiológica"):
        assert marker in relations, marker

    assert {item["id"] for item in preparation["biomedical_case_models"]} == {
        "ecg-surface-difference", "eeg-low-amplitude-chain", "emg-motor-unit-superposition"
    }
    assert len(preparation["misconception_bank"]) == 12
    assert [item["id"] for item in preparation["planned_practices"]] == ["U3-P1", "U3-P2", "U3-P3"]

    assert sources["status"] == "verified_direct_sources"
    assert sources["unit_number"] == 3
    assert len(sources["sources"]) >= 6
    assert all(item["verification_status"] == "verified_directly" for item in sources["sources"])
    assert sources["editorial_state"]["course_state"] == "pending"

    readiness = READINESS.read_text(encoding="utf-8")
    for marker in ("Biopotenciales, electrodos e interfaz electrodo-tejido", "U3-P1", "U3-P2", "U3-P3", "Bloqueos técnicos pendientes", "sin adquisición con personas", "course_state: pending"):
        assert marker in readiness, marker

    if UNIT.exists():
        audit = load_object(AUDIT)
        authorization = audit["authorization_result"]
        assert authorization["full_theory_drafting_authorized"] is True
        assert authorization["authoral_unit_creation_authorized"] is True
        assert authorization["public_release_authorized"] is False
        unit = load_object(UNIT)
        assert unit["status"] == "review"
        assert unit["review_state"]["professional_review"] == "pending"
        assert unit["review_state"]["human_review_U3_A5"] == "pending"
        assert unit["review_state"]["public_release_authorized"] is False

    print("OK Bioinstrumentation U3 authoring preparation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
