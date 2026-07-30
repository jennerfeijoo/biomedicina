#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import json
import math
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/practice_implementations/bioinstrumentacion-unit-03.json"
BLOCKERS = ROOT / "data/unit_preparation/bioinstrumentacion-unit-03-blocker-resolution.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    blockers = json.loads(BLOCKERS.read_text(encoding="utf-8"))
    assert contract["status"] == "unit_03_practices_implemented_internal_review"
    assert contract["course_editorial_state"] == "pending"
    assert blockers["authorization_result"]["practice_implementation_authorized"] is True
    assert [p["id"] for p in contract["practices"]] == ["U3-P1", "U3-P2", "U3-P3"]
    assert contract["reproducibility"] == {
        "network_required": False,
        "external_packages_required": False,
        "randomness": "none",
        "outputs_generated_outside_source_tree": True,
    }
    authorization = contract["authorization_state"]
    assert authorization == {
        "assessment_implementation_authorized": False,
        "full_theory_drafting_authorized": False,
        "public_release_authorized": False,
        "human_or_professional_review_claimed": False,
    }

    p1 = load_module(ROOT / contract["practices"][0]["script"], "u3p1")
    rows = p1.generate()
    assert len(rows) == 500
    assert abs(rows[0]["lead_12_v"] - (rows[0]["e1_v"] - rows[0]["e2_v"])) < 1e-12
    assert max(abs(r["lead_12_v"]) for r in rows) > 0.1
    assert any(abs(r["lead_12_v"] - r["lead_34_v"]) > 0.05 for r in rows)

    p2 = load_module(ROOT / contract["practices"][1]["script"], "u3p2")
    sweep = p2.sweep()
    assert len(sweep) == 11
    assert sweep[0]["magnitude_ohm"] > sweep[-1]["magnitude_ohm"]
    assert sweep[0]["phase_deg"] < 0
    assert sweep[-1]["magnitude_ohm"] > 1200.0

    p3 = load_module(ROOT / contract["practices"][2]["script"], "u3p3")
    results = {name: p3.diagnose(features) for name, features in p3.fixtures().items()}
    assert results["line_interference"]["dominant"] == "power_line_interference"
    assert results["contact_motion"]["dominant"] == "motion_or_contact_artifact"
    assert results["clipping"]["dominant"] == "saturation_or_clipping"
    assert results["ambiguous_burst"]["dominant"] == "cable_or_non_target_biological_activity"
    assert all(r["requires_discriminating_test"] is True for r in results.values())
    assert all(r["diagnostic_claim_is_not_clinical"] is True for r in results.values())

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        p1_path = out / "u3p1.csv"
        with p1_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        assert p1_path.is_file()

    assert not (ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-03.json").exists()
    print("OK Bioinstrumentation U3 practices")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
