#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "generated_units" / "quimica-ii" / "unit-05.json"
TERMS = [
    {"term": "Doble capa", "definition": "Distribución interfacial de carga en el electrodo y la solución."},
    {"term": "Sobrepotencial", "definition": "Diferencia entre el potencial aplicado y el reversible para sostener corriente."},
    {"term": "Corriente farádica", "definition": "Corriente asociada a una transformación electroquímica con transferencia de electrones."},
]

def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    existing = {item["term"] for item in data["glossary"]}
    data["glossary"].extend(item for item in TERMS if item["term"] not in existing)
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(PATH.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
