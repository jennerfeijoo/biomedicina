from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioestadistica"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


course_path = COURSE / "course.json"
course = load(course_path)
course["content_version"] = "1.0.0"
course["status"] = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}
course["editorial_notice"] = (
    "Corpus canónico educativo completo a nivel de contenido estructurado y pedagogía interna. "
    "Las ocho unidades, sus actividades, evaluaciones y la evaluación integradora del curso están materializadas y sin brechas explícitas de contenido. "
    "La revisión humana interna y la revisión académica externa permanecen pendientes; los resultados educativos no sustituyen asesoría bioestadística, revisión ética, protocolo, decisión clínica ni validación institucional."
)
dump(course_path, course)

# U1–U8 were individually curated and the strict canonical audit reports zero
# content/traceability gaps. Normalize only the source-status flag; keep unit
# content/pedagogy in_review and all human-review boundaries unchanged.
for unit_file in course["unit_files"]:
    unit_path = COURSE / unit_file
    unit = load(unit_path)
    if unit["status"]["internal_review"] != "pending" or unit["status"]["external_review"] != "pending":
        raise SystemExit(f"Unexpected human-review state in {unit_file}")
    unit["status"]["sources"] = "traceable"
    dump(unit_path, unit)

assessment_path = COURSE / "assessments" / "course-assessment.json"
assessment = load(assessment_path)
assessment["capstone"]["linked_learning_outcome_ids"] = [f"BIOEST-LO{i:02d}" for i in range(1, 9)]
dump(assessment_path, assessment)

print("Promoted Bioestadistica course corpus and normalized traceability metadata")
