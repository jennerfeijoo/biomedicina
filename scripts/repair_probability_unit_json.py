#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "probabilidad-estadistica"


def repair(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    changed = False
    for index in range(len(lines) - 1):
        current = lines[index]
        following = lines[index + 1].strip()
        stripped = current.strip()
        if stripped.startswith("{") and stripped.endswith('"') and following in {"]", "],"}:
            lines[index] = current + "}"
            changed = True
    repaired = "\n".join(lines) + ("\n" if original.endswith("\n") else "")
    json.loads(repaired)
    if changed:
        path.write_text(repaired, encoding="utf-8")
    return changed


def main() -> int:
    changed = []
    for path in sorted(UNIT_DIR.glob("unit-*.json")):
        if repair(path):
            changed.append(path)
    for path in changed:
        print(f"Reparado: {path.relative_to(ROOT)}")
    print(f"Archivos modificados: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
