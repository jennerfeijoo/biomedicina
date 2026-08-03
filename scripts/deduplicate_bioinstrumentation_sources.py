#!/usr/bin/env python3
"""Elimina referencias bibliográficas duplicadas por URL en las unidades canónicas.

Conserva la primera referencia y no modifica las fuentes autorales históricas.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "data" / "generated_units" / "bioinstrumentacion"


def main() -> int:
    changed = 0
    removed = 0
    for path in sorted(UNITS.glob("unit-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        sources = data.get("sources", [])
        if not isinstance(sources, list):
            raise SystemExit(f"ERROR: {path.relative_to(ROOT)}: sources no es una lista")
        seen: set[str] = set()
        unique = []
        for source in sources:
            if not isinstance(source, dict):
                unique.append(source)
                continue
            marker = str(source.get("url") or "").strip().rstrip("/").lower()
            if not marker:
                marker = "title:" + str(source.get("title") or "").strip().lower()
            if marker in seen:
                removed += 1
                continue
            seen.add(marker)
            unique.append(source)
        if unique != sources:
            data["sources"] = unique
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    print(f"Fuentes deduplicadas: {removed}; unidades modificadas: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
