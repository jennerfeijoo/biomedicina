#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/unit_preparation/bioinstrumentacion-unit-05.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-05/PREPARATION.md"
AUTHORAL = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    data = load_object(DATA)
    assert data["subject_id"] == "bioinstrumentacion"
    assert data["unit"] == 5
    assert data["title"] == "Sensores no eléctricos"
    assert data["status"] == "preparation_internal_review"
    assert data["course_editorial_state"] == "pending"

    scope = data["scope"]
    assert all(scope[key] is True for key in ("pressure", "temperature", "flow", "optics", "multimodal_monitoring_case"))

    blockers = data["technical_blockers"]
    assert [item["id"] for item in blockers] == [f"U5-B{i:02d}" for i in range(1, 7)]
    assert all(item["status"] == "open" for item in blockers)

    practices = data["candidate_practices"]
    assert [item["id"] for item in practices] == ["U5-P1", "U5-P2", "U5-P3"]
    assert all(item["mode"] == "synthetic_only" for item in practices)
    assert all(item["status"] == "not_authorized" for item in practices)
    assert data["candidate_assessments"] == ["U5-A1", "U5-A2", "U5-A3", "U5-A4", "U5-A5"]

    assert all(value is False for value in data["authorization"].values())
    limits = data["limits"]
    assert limits["synthetic_only"] is True
    assert all(limits[key] is False for key in (
        "human_or_device_acquisition",
        "clinical_validity_claimed",
        "electrical_safety_claimed",
        "regulatory_conformity_claimed",
    ))
    assert not AUTHORAL.exists(), "unit-05.json must remain absent during preparation"

    doc = DOC.read_text(encoding="utf-8")
    for marker in ("U5-B01", "U5-B06", "solo simulación y datos sintéticos", "course_state: pending"):
        assert marker in doc, marker

    print("OK Bioinstrumentation U5 preparation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
