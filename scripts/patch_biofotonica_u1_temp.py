#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paths = [
    ROOT / "data/course_redevelopment/biofotonica/units/unit-01.json",
    ROOT / "data/generated_units/biofotonica/unit-01.json",
]
for path in paths:
    unit = json.loads(path.read_text(encoding="utf-8"))
    paragraph = unit["theory_sections"][0]["paragraphs"][0]
    unit["theory_sections"][0]["paragraphs"][0] = paragraph.replace(
        "los estima mediante un modelo inverso",
        "los estima como un problema inverso mediante un modelo de transporte",
    )
    path.write_text(json.dumps(unit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
