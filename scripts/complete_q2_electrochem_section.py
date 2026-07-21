#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "generated_units" / "quimica-ii" / "unit-05.json"
PARAGRAPH = "El voltaje terminal de una celda bajo carga difiere del potencial reversible por resistencia interna, sobrepotenciales y gradientes de concentración. Medir en circuito abierto aproxima el equilibrio; extraer corriente perturba la interfaz. Por ello una batería, electrodo o biosensor no se caracteriza con un único potencial estándar."

def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    paragraphs = data["theory_sections"][1]["paragraphs"]
    if PARAGRAPH not in paragraphs:
        paragraphs.append(PARAGRAPH)
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(PATH.read_text(encoding="utf-8"))
    print("Electroquímica ampliada y validada")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
