#!/usr/bin/env python3
"""Validate the authoring-preparation contract for Bioinstrumentation Unit 4."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREPARATION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-04.json"
SOURCES = ROOT / "data/source_registry/bioinstrumentacion-unit-04.json"
READINESS = ROOT / "docs/pilots/bioinstrumentacion/unit-04/AUTHORING_READINESS.md"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-04.json"


def load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain an object")
    return payload


def main() -> int:
    preparation = load_object(PREPARATION)
    sources = load_object(SOURCES)

    assert preparation["subject_id"] == "bioinstrumentacion"
    assert preparation["unit_number"] == 4
    assert preparation["title"] == "Conversión y procesamiento de señales biomédicas"
    assert preparation["status"] == "authoring_preparation_review"
    assert preparation["course_editorial_state"] == "pending"

    outcomes = preparation["learning_outcomes"]
    assert [item["id"] for item in outcomes] == [f"U4-LO{i}" for i in range(1, 6)]
    for item in outcomes:
        for field in ("statement", "mastery_evidence", "criterion"):
            assert len(item[field].strip()) >= 40

    relations = preparation["knowledge_model"]["required_relations"]
    assert len(relations) == 8
    joined = " ".join(relations).lower()
    for marker in (
        "filtro anti-alias",
        "aliasing",
        "periodo de muestreo",
        "rango del adc",
        "lsb",
        "enob",
        "pérdida",
        "aislamiento",
    ):
        assert marker in joined, marker

    cases = preparation["biomedical_case_models"]
    assert {item["id"] for item in cases} == {
        "ecg-digitization-chain",
        "emg-aliasing-case",
        "multichannel-timing-case",
    }
    assert all(item["forbidden_inference"] for item in cases)

    misconceptions = preparation["misconception_bank"]
    assert len(misconceptions) == 12
    assert len({item["id"] for item in misconceptions}) == 12

    practices = preparation["planned_practices"]
    assert [item["id"] for item in practices] == ["U4-P1", "U4-P2", "U4-P3"]
    assert all(item["data_policy"] == "synthetic_only" for item in practices)

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
    assert sources["unit_number"] == 4
    entries = sources["sources"]
    assert len(entries) >= 7
    source_ids = {item["id"] for item in entries}
    assert {
        "ni-analog-signal-acquisition",
        "ni-anti-alias-filters",
        "adi-adc-glossary",
        "adi-quantization-glossary",
        "adi-data-conversion-calculator",
        "physionet-mit-bih-arrhythmia",
        "iec-60601-1-overview",
    } <= source_ids
    for item in entries:
        assert item["verification_status"] == "verified_directly"
        assert item["url"].startswith("https://")
        assert len(item["authorized_claims"]) >= 2
        assert len(item["limitations"]) >= 80

    assert len(sources["source_gaps"]) == 3
    editorial = sources["editorial_state"]
    assert editorial == {
        "technical_blockers_resolved": False,
        "practice_implementation_authorized": False,
        "full_theory_drafting_authorized": False,
        "public_release_authorized": False,
        "course_state": "pending",
    }

    text = READINESS.read_text(encoding="utf-8")
    for marker in (
        "Conversión y procesamiento de señales biomédicas",
        "U4-P1",
        "U4-P2",
        "U4-P3",
        "Bloqueos técnicos pendientes",
        "sin implementar",
        "course_state: pending",
    ):
        assert marker in text, marker

    assert not UNIT.exists(), "Unit 4 authoral file was created before authorization"
    print("OK Bioinstrumentation U4 authoring preparation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
