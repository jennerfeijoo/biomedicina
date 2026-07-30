#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREP = ROOT / "data/unit_preparation/bioinstrumentacion-unit-04.json"
RESOLUTION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-04-blocker-resolution.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-04.json"


def main() -> int:
    prep = json.loads(PREP.read_text(encoding="utf-8"))
    resolution = json.loads(RESOLUTION.read_text(encoding="utf-8"))

    assert prep["subject_id"] == "bioinstrumentacion"
    assert prep["unit_number"] == 4
    assert resolution["status"] == "technical_blockers_resolved_internal_review"
    assert resolution["course_editorial_state"] == "pending"

    blockers = resolution["resolved_blockers"]
    assert [item["id"] for item in blockers] == [f"U4-B0{i}" for i in range(1, 7)]
    assert {item["topic"] for item in blockers} == {
        "muestreo_y_anti_alias",
        "rango_cuantizacion_y_saturacion",
        "enob_y_desempeno_dinamico",
        "sincronizacion_y_tiempo",
        "integridad_de_datos_y_comunicacion",
        "aislamiento_y_seguridad_documental",
    }
    for item in blockers:
        assert item["resolution"].strip()
        assert len(item["acceptance_tests"]) >= 4
        assert all(test.strip() for test in item["acceptance_tests"])

    constraints = resolution["practice_constraints"]
    assert set(constraints) == {"U4-P1", "U4-P2", "U4-P3"}
    assert "anti_alias_before_sampling" in constraints["U4-P1"]
    assert "explicit_adc_range" in constraints["U4-P2"]
    assert "sequence_counters" in constraints["U4-P3"]

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
    assert not UNIT.exists(), "unit-04.json must remain absent during blocker resolution"

    text = RESOLUTION.read_text(encoding="utf-8").lower()
    for marker in (
        "filtro anti-alias",
        "lsb",
        "enob",
        "marcas de tiempo",
        "contadores de secuencia",
        "sin conexión física",
        "ninguna simulación",
    ):
        assert marker in text, marker

    print("OK Bioinstrumentation U4 technical blockers resolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
