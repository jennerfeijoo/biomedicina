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
    for item in outcomes:
        for field in ("statement", "mastery_evidence", "criterion"):
            assert len(item[field].strip()) >= 40

    relations = preparation["knowledge_model"]["required_relations"]
    assert len(relations) == 8
    joined = " ".join(relations).lower()
    for marker in (
        "potencial transmembrana",
        "fuentes distribuidas",
        "diferencia",
        "conducción iónica",
        "frecuencia",
        "desbalance",
        "tierra de protección",
        "autenticidad fisiológica",
    ):
        assert marker in joined, marker

    cases = preparation["biomedical_case_models"]
    assert {item["id"] for item in cases} == {
        "ecg-surface-difference",
        "eeg-low-amplitude-chain",
        "emg-motor-unit-superposition",
    }
    assert all(item["forbidden_inference"] for item in cases)

    misconceptions = preparation["misconception_bank"]
    assert len(misconceptions) == 12
    assert len({item["id"] for item in misconceptions}) == 12

    practices = preparation["planned_practices"]
    assert [item["id"] for item in practices] == ["U3-P1", "U3-P2", "U3-P3"]
    assert all(item["data_policy"] in {"synthetic_only", "open_or_synthetic_nonclinical_only"} for item in practices)

    gates = preparation["authoring_gates"]
    assert gates == {
        "source_registry_required": True,
        "technical_blocker_resolution_required": True,
        "practice_implementation_authorized": False,
        "full_theory_drafting_authorized": False,
        "public_release_authorized": False,
        "human_or_professional_review_claimed": False,
    }

    assert sources["status"] == "verified_direct_sources"
    assert sources["unit_number"] == 3
    entries = sources["sources"]
    assert len(entries) >= 6
    source_ids = {item["id"] for item in entries}
    assert {
        "openstax-ap2e-action-potential",
        "ncbi-purves-electrical-signals",
        "physionet-mit-bih-arrhythmia",
        "physionet-eegmmidb",
        "sensors-2025-electrode-impedance-analyzer",
        "iec-60601-1-overview",
    } <= source_ids
    for item in entries:
        assert item["verification_status"] == "verified_directly"
        assert item["url"].startswith("https://")
        assert len(item["authorized_claims"]) >= 2
        assert len(item["limitations"]) >= 80

    assert len(sources["source_gaps"]) == 3
    editorial = sources["editorial_state"]
    assert editorial["technical_blockers_resolved"] is False
    assert editorial["practice_implementation_authorized"] is False
    assert editorial["full_theory_drafting_authorized"] is False
    assert editorial["public_release_authorized"] is False
    assert editorial["course_state"] == "pending"

    text = READINESS.read_text(encoding="utf-8")
    for marker in (
        "Biopotenciales, electrodos e interfaz electrodo-tejido",
        "U3-P1",
        "U3-P2",
        "U3-P3",
        "Bloqueos técnicos pendientes",
        "sin adquisición con personas",
        "course_state: pending",
    ):
        assert marker in text, marker

    assert not UNIT.exists(), "Unit 3 authoral file was created before authorization"
    print("OK Bioinstrumentation U3 authoring preparation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
