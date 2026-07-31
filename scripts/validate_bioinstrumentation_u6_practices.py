#!/usr/bin/env python3
"""Validate the synthetic practice implementation for Bioinstrumentation Unit 6."""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/practice_implementations/bioinstrumentacion-unit-06.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def close(actual: float, expected: float, *, rel_tol: float = 1e-12) -> None:
    require(math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=1e-15), f"Expected {expected}, got {actual}")


def main() -> None:
    require(CONTRACT.exists(), f"Missing {CONTRACT.relative_to(ROOT)}")
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    require(data["subject_id"] == "bioinstrumentacion", "Wrong subject_id")
    require(data["unit"] == 6, "Wrong unit")
    require(data["status"] == "implemented_internal_review", "Wrong implementation status")
    require(data["synthetic_only"] is True, "Practices must remain synthetic-only")
    require(data["network_required"] is False, "CI must remain offline")
    require(data["human_participants"] is False, "Human participation is prohibited")
    require(data["energized_medical_devices"] is False, "Energized medical-device work is prohibited")

    practices = {practice["id"]: practice for practice in data["practices"]}
    require(set(practices) == {"U6-P1", "U6-P2", "U6-P3"}, "Unexpected practice IDs")

    p1 = practices["U6-P1"]
    close(p1["inputs"]["source_voltage_v_rms"] / p1["inputs"]["path_impedance_ohm"], p1["deterministic_result"]["path_current_a_rms"])
    close(p1["deterministic_result"]["path_current_uA_rms"], 0.5)

    expected_by_mechanism = {
        "conducido": lambda p: p["I_interference_a_rms"] * p["Z_common_ohm"],
        "capacitivo": lambda p: 2 * math.pi * p["frequency_hz"] * p["C_mutual_f"] * p["V_source_v_rms"],
        "inductivo": lambda p: 2 * math.pi * p["frequency_hz"] * p["mutual_inductance_h"] * p["I_source_a_rms"],
        "radiado": lambda p: p["coupling_gain"] * p["V_source_v_rms"],
    }
    p2 = practices["U6-P2"]
    require({case["mechanism"] for case in p2["cases"]} == set(expected_by_mechanism), "Missing EMC mechanism")
    for case in p2["cases"]:
        calculated = expected_by_mechanism[case["mechanism"]](case["parameters"])
        expected_key = "expected_output_a_rms" if case["mechanism"] == "capacitivo" else "expected_output_v_rms"
        close(calculated, case[expected_key])

    p3 = practices["U6-P3"]["scenario"]
    nominal = p3["nominal"]["source_voltage_v_rms"] / p3["nominal"]["path_impedance_ohm"] * 1e6
    fault = p3["single_fault"]["source_voltage_v_rms"] / p3["single_fault"]["path_impedance_ohm"] * 1e6
    close(nominal, 0.5)
    close(fault, 5.0)
    close(fault / nominal, 10.0)

    limits = data["limits"]
    for key in (
        "clinical_safety_claimed",
        "regulatory_conformity_claimed",
        "emc_compliance_claimed",
        "professional_review_claimed",
        "public_release_authorized",
        "assessment_implementation_authorized",
        "full_theory_drafting_authorized",
    ):
        require(limits[key] is False, f"{key} must remain false")

    require(not UNIT.exists(), "unit-06.json must remain absent until theory drafting is authorized")
    print("Bioinstrumentation Unit 6 synthetic practices validated.")


if __name__ == "__main__":
    main()
