#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREP = ROOT / "data/unit_preparation/bioinstrumentacion-unit-03.json"
RESOLUTION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-03-blocker-resolution.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-03.json"


def main() -> int:
    prep = json.loads(PREP.read_text(encoding="utf-8"))
    resolution = json.loads(RESOLUTION.read_text(encoding="utf-8"))

    assert prep["subject_id"] == "bioinstrumentacion"
    assert prep["unit_number"] == 3
    assert resolution["status"] == "technical_blockers_resolved_internal_review"
    assert resolution["course_editorial_state"] == "pending"

    blockers = resolution["resolved_blockers"]
    assert [item["id"] for item in blockers] == [f"U3-B0{i}" for i in range(1, 7)]
    assert {item["topic"] for item in blockers} == {
        "modelo_equivalente_interfaz",
        "fuentes_distribuidas_sinteticas",
        "datos_abiertos",
        "taxonomia_artefactos",
        "referencia_retorno_tierra_blindaje",
        "seguridad_documental",
    }
    for item in blockers:
        assert item["resolution"].strip()
        assert len(item["acceptance_tests"]) >= 4
        assert all(test.strip() for test in item["acceptance_tests"])

    constraints = resolution["practice_constraints"]
    assert set(constraints) == {"U3-P1", "U3-P2", "U3-P3"}
    assert "synthetic_only" in constraints["U3-P1"]
    assert "complex_impedance" in constraints["U3-P2"]
    assert "no_diagnosis" in constraints["U3-P3"]

    auth = resolution["authorization"]
    assert auth == {
        "practice_implementation_authorized": True,
        "assessment_implementation_authorized": False,
        "full_theory_drafting_authorized": False,
        "public_release_authorized": False,
    }
    assert resolution["human_or_professional_review"] == "not_claimed"
    assert resolution["unit_authoral_file"] == "absent"
    assert resolution["unit_developed"] is False
    assert not UNIT.exists(), "unit-03.json must remain absent during blocker resolution"

    text = RESOLUTION.read_text(encoding="utf-8").lower()
    required = [
        "potencial de media celda",
        "impedancia compleja",
        "superposición",
        "prueba discriminante",
        "referencia de medición",
        "tierra de protección",
        "sin conexión física de electrodos",
        "ninguna simulación",
    ]
    for marker in required:
        assert marker in text, marker

    print("OK Bioinstrumentation U3 technical blockers resolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
