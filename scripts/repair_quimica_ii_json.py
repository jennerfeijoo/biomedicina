#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "quimica-ii"

EXTRA = {
    5: "El balance redox debe especificar además el medio químico. Protonación, complejación y actividad pueden cambiar las especies disponibles y el potencial medido, por lo que una ecuación formal se interpreta siempre junto con pH, composición y referencia.",
    6: "La representación molecular debe conservar conectividad, carga y estereoquímica. Una fórmula molecular no distingue isómeros y una proyección plana puede ocultar conformaciones; por ello se selecciona la notación según la pregunta química.",
}


def repair_text(text: str) -> str:
    lines = text.splitlines()
    for index in range(len(lines) - 1):
        current = lines[index]
        following = lines[index + 1].strip()
        stripped = current.strip()
        if stripped.startswith("{") and stripped.endswith('"') and following in {"]", "],"}:
            lines[index] = current + "}"
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    for unit in range(1, 7):
        path = UNIT_DIR / f"unit-{unit:02d}.json"
        repaired = repair_text(path.read_text(encoding="utf-8"))
        data = json.loads(repaired)
        if unit in EXTRA:
            paragraphs = data["theory_sections"][0]["paragraphs"]
            if EXTRA[unit] not in paragraphs:
                paragraphs.append(EXTRA[unit])
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        json.loads(path.read_text(encoding="utf-8"))
        print(f"Validada: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
