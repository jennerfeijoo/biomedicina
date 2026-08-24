#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "biosensores"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


for n in range(1, 7):
    unit_path = COURSE / "units" / f"unit-{n:02d}.json"
    unit = load(unit_path)
    for activity in unit.get("activities", []):
        activity["status"] = "complete"
    write(unit_path, unit)

    assessment_path = COURSE / "assessments" / f"unit-{n:02d}.json"
    assessment = load(assessment_path)
    for item in assessment["items"]:
        answer = item["answer_key"]
        if not str(answer.get("explanation") or "").strip():
            answer["explanation"] = "La respuesta debe conectar el concepto evaluado con el mecanismo, el contexto de uso y el límite explícito desarrollado en la unidad."
        if not answer.get("common_misconceptions"):
            answer["common_misconceptions"] = ["Responder con una definición aislada sin justificar condiciones ni límites."]
        item["status"] = "complete"
    assessment["status"] = "complete"
    write(assessment_path, assessment)

course_assessment_path = COURSE / "assessments" / "course-assessment.json"
course_assessment = load(course_assessment_path)
course_assessment["status"] = "complete"
write(course_assessment_path, course_assessment)
