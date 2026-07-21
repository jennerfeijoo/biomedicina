#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "generated_units" / "quimica-ii" / "unit-05.json"
PARAGRAPH = "Todo potencial de electrodo se mide respecto a una referencia. La referencia debe mantener composición y contacto iónico estables; cambios en la unión líquida, evaporación o contaminación introducen potenciales adicionales y deriva. Una respuesta aparente del analito puede provenir de la referencia, por lo que su control forma parte de la trazabilidad de la medición."

def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    paragraphs = data["theory_sections"][2]["paragraphs"]
    if PARAGRAPH not in paragraphs:
        paragraphs.append(PARAGRAPH)
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(PATH.read_text(encoding="utf-8"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
