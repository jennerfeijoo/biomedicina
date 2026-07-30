#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-04.json"


def main() -> int:
    data = json.loads(UNIT.read_text(encoding="utf-8"))
    assert data["subject_id"] == "bioinstrumentacion"
    assert data["unit"] == 4
    assert data["status"] == "authoral_draft_internal_review"
    assert data["course_editorial_state"] == "pending"
    assert len(data["learning_outcomes"]) == 5
    assert [s["id"] for s in data["sections"]] == [f"U4-S{i}" for i in range(1, 8)]
    assert [e["id"] for e in data["worked_examples"]] == [f"U4-E{i}" for i in range(1, 5)]
    assert data["practices"] == ["U4-P1", "U4-P2", "U4-P3"]
    assert data["assessments"] == [f"U4-A{i}" for i in range(1, 6)]
    assert data["audit_findings_resolved"]["U4-F01"].startswith("resolved")
    assert data["audit_findings_resolved"]["U4-F02"].startswith("resolved")
    text = UNIT.read_text(encoding="utf-8").lower()
    for marker in ("sinad", "enob", "61.96", "10.0 bits", "frontera", "no demuestra seguridad", "timestamps iguales no prueban"):
        assert marker in text, marker
    limits = data["limits"]
    assert limits["synthetic_only"] is True
    assert limits["human_or_device_acquisition"] is False
    assert limits["clinical_validity_claimed"] is False
    assert limits["electrical_safety_claimed"] is False
    assert limits["regulatory_conformity_claimed"] is False
    assert limits["professional_review_claimed"] is False
    assert limits["public_release_authorized"] is False
    assert limits["U4-A5_status"] == "pending_real_human_review"
    print("OK Bioinstrumentation U4 authoral draft")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
