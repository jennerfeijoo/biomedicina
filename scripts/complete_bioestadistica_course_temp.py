from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "courses" / "bioestadistica" / "course.json"
course = json.loads(PATH.read_text(encoding="utf-8"))
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
PATH.write_text(json.dumps(course, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Promoted Bioestadistica course corpus to structured academic completion")
