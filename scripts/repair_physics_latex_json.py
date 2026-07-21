#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "fisica-i"
ISOLATED_BACKSLASH = re.compile(r"(?<!\\)\\(?!\\)")


def close_incomplete_inline_objects(text: str) -> str:
    lines = text.splitlines()
    for index in range(len(lines) - 1):
        current = lines[index]
        following = lines[index + 1].strip()
        stripped = current.strip()
        if stripped.startswith("{") and stripped.endswith('"') and following in {"]", "],"}:
            lines[index] = current + "}"
    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + suffix


def repair(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    repaired = ISOLATED_BACKSLASH.sub(r"\\\\", original)
    repaired = close_incomplete_inline_objects(repaired)
    json.loads(repaired)
    if repaired == original:
        return False
    path.write_text(repaired, encoding="utf-8")
    return True


def main() -> int:
    changed: list[Path] = []
    for path in sorted(UNIT_DIR.glob("unit-*.json")):
        if repair(path):
            changed.append(path)
    for path in changed:
        print(f"Reparado: {path.relative_to(ROOT)}")
    print(f"Archivos modificados: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
