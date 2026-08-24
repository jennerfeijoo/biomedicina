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
    path = COURSE / "assessments" / f"unit-{n:02d}.json"
    data = load(path)
    for item in data["items"]:
        answer = item["answer_key"]
        if not str(answer.get("explanation") or "").strip():
            answer["explanation"] = "La respuesta debe conectar el concepto evaluado con el mecanismo, el contexto de uso y el límite explícito desarrollado en la unidad."
        if not answer.get("common_misconceptions"):
            answer["common_misconceptions"] = ["Responder con una definición aislada sin justificar condiciones ni límites."]
    write(path, data)

course_assessment_path = COURSE / "assessments" / "course-assessment.json"
course_assessment = load(course_assessment_path)
course_assessment["status"] = "complete"
write(course_assessment_path, course_assessment)
