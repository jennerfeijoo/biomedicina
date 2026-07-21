#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("probabilidad-estadistica", "quimica-ii")


def main() -> int:
    changed = 0
    for subject_id in TARGETS:
        course_path = ROOT / "data" / "generated_courses" / f"{subject_id}.json"
        course = json.loads(course_path.read_text(encoding="utf-8"))
        weekly_hours = int(course["weekly_hours"])
        expected_total = int(course["total_workload_hours"])
        allocated = 0
        for path in sorted((ROOT / "data" / "generated_units" / subject_id).glob("unit-*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            expected = len(data["weeks"]) * weekly_hours
            allocated += expected
            if int(data.get("estimated_hours", 0)) != expected:
                data["estimated_hours"] = expected
                path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                changed += 1
                print(f"Corregida {path.relative_to(ROOT)}: {expected} horas")
        if allocated != expected_total:
            raise ValueError(
                f"{subject_id}: la asignación por semanas suma {allocated}, pero el curso declara {expected_total}"
            )
    print(f"Archivos modificados: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
