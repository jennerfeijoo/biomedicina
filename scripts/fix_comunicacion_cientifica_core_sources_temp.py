#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "comunicacion-cientifica"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


course_path = COURSE_DIR / "course.json"
course = load(course_path)
core: list[str] = []
for number in range(1, 7):
    unit = load(COURSE_DIR / "units" / f"unit-{number:02d}.json")
    for source_id in unit.get("source_ids", []):
        if source_id not in core:
            core.append(source_id)
course["core_source_ids"] = core[:12]
if not course["core_source_ids"]:
    raise SystemExit("No se encontraron fuentes unitarias para core_source_ids")
save(course_path, course)
print(f"Fuentes núcleo enlazadas: {len(course['core_source_ids'])}")
