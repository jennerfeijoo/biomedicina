#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/practice_implementations/bioinstrumentacion-unit-04.json"
BLOCKERS = ROOT / "data/unit_preparation/bioinstrumentacion-unit-04-blocker-resolution.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-04.json"


def run(script: str, output: Path) -> list[dict[str, str]]:
    subprocess.run([sys.executable, str(ROOT / script), "--output", str(output)], check=True)
    with output.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    blockers = json.loads(BLOCKERS.read_text(encoding="utf-8"))
    assert contract["subject_id"] == "bioinstrumentacion"
    assert contract["unit"] == 4
    assert contract["course_editorial_state"] == "pending"
    assert [p["id"] for p in contract["practices"]] == ["U4-P1", "U4-P2", "U4-P3"]
    assert all(p["data_policy"] == "synthetic_only" for p in contract["practices"])
    assert blockers["authorization"]["practice_implementation_authorized"] is True
    assert blockers["authorization"]["assessment_implementation_authorized"] is False
    assert blockers["authorization"]["full_theory_drafting_authorized"] is False
    assert blockers["authorization"]["public_release_authorized"] is False
    assert not UNIT.exists()

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        p1 = run("scripts/bioinstrumentation_u4_practice_u4p1.py", base / "u4p1.csv")
        p2 = run("scripts/bioinstrumentation_u4_practice_u4p2.py", base / "u4p2.csv")
        p3 = run("scripts/bioinstrumentation_u4_practice_u4p3.py", base / "u4p3.csv")

    assert len(p1) == 200
    assert {row["alias_frequency_hz"] for row in p1} == {"30.000000"}
    assert any(abs(float(row["sampled_unfiltered"]) - float(row["sampled_filtered"])) > 0.1 for row in p1)

    assert len(p2) == 9
    assert {row["lsb_v"] for row in p2} == {"0.001953125"}
    assert sum(row["saturated"] == "true" for row in p2) == 2
    assert all(0 <= int(row["code"]) <= 1023 for row in p2)

    statuses = {row["status"] for row in p3}
    assert "duplicate" in statuses
    assert "reordered" in statuses
    assert "gap:1" in statuses

    print("OK Bioinstrumentation U4 practices")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
