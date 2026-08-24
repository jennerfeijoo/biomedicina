from __future__ import annotations

import json
from pathlib import Path

PATH = Path("data/course_redevelopment/biomecanica/course.json")
RESOURCE = {
    "title": "The Turing Way — Guide for Reproducible Research",
    "organization": "The Turing Way Community",
    "url": "https://book.the-turing-way.org/reproducible-research/reproducible-research/",
    "type": "guía abierta de reproducibilidad",
    "description": "Guía para documentar datos, código, entornos y decisiones de análisis de forma que los resultados puedan reconstruirse y auditarse.",
    "verification_status": "verified_directly",
}

data = json.loads(PATH.read_text(encoding="utf-8"))
resources = data.setdefault("core_resources", [])
if not any(item.get("url") == RESOURCE["url"] for item in resources):
    resources.append(RESOURCE)
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert len(data["core_resources"]) >= 8
assert all(item.get("verification_status") == "verified_directly" for item in data["core_resources"])
