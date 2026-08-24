from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "courses" / "bioinstrumentacion" / "assessments" / "course-assessment.json"
assessment = json.loads(PATH.read_text(encoding="utf-8"))
for item in assessment["capstone"]["deliverables"]:
    if item["id"] == "BIOINST-CAP-D05":
        item["description"] = "Datos sintéticos y su procedencia, código, parámetros, dependencias, versiones, baseline, hashes y manifiesto."
        break
else:
    raise SystemExit("BIOINST-CAP-D05 not found")
PATH.write_text(json.dumps(assessment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Made capstone provenance explicit")
