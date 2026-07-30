#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-03.json"
ENGINE = ROOT / "scripts/bioinstrumentation_u3_assessment.py"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-03.json"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("u3assessment", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    practices = json.loads(PRACTICES.read_text(encoding="utf-8"))
    assert contract["status"] == "unit_03_assessment_implemented_internal_review"
    assert contract["course_editorial_state"] == "pending"
    assert practices["status"] == "unit_03_practices_implemented_internal_review"
    assessments = contract["assessments"]
    assert [a["id"] for a in assessments] == ["U3-A1", "U3-A2", "U3-A3", "U3-A4", "U3-A5"]
    assert {a["learning_outcome"] for a in assessments} == {f"U3-LO{i}" for i in range(1, 6)}
    routes = contract["feedback_routes"]
    assert len(routes) == 12
    assert len({r["misconception"] for r in routes}) == 12
    policy = contract["answer_key_policy"]
    assert policy["student_payload_contains_complete_keys"] is False
    assert policy["semantic_scoring_is_automatic"] is False
    assert policy["human_confirmation_required_for_U3_A5"] is True

    engine = load_module(ENGINE)
    assert engine.evaluate("U3-A1", {"chain":["membrane_potential","distributed_source","volume_conductor","surface_difference"],"claims_direct_cell_measurement":False}).accepted
    assert engine.evaluate("U3-A1", {"chain":["membrane_potential"],"claims_direct_cell_measurement":True}).feedback_route == "U3-F01"
    assert engine.evaluate("U3-A2", {"elements":["half_cell_potential","Rs","Rct","Cdl"],"frequency_dependent":True}).accepted
    assert engine.evaluate("U3-A3", {"mapping":{"measurement_reference":"reference","bias_current_path":"return","protective_conductor":"protective_earth","field_screen":"shield"}}).accepted
    assert engine.evaluate("U3-A4", {"pattern":"50 Hz peak","mechanism":"mains coupling","discriminating_test":"change coupling condition","claims_visual_certainty":False}).accepted
    human = engine.evaluate("U3-A5", {"comparison_dimensions":["source","geometry","scale","band","interface","inference_limit"]})
    assert human.requires_human_review is True and human.accepted is False
    assert engine.feedback_for_attempt("U3-F01", 1)["level"] == 1
    assert engine.feedback_for_attempt("U3-F01", 3)["level"] == 3
    assert not (ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-03.json").exists()
    print("OK Bioinstrumentation U3 assessment")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
