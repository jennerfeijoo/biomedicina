#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "fisica-i"
LATEX_FIELD = re.compile(r'("latex"\s*:\s*")(.*?)("(?=\s*[},]))')


def escape_unescaped_backslashes(value: str) -> str:
    output: list[str] = []
    index = 0
    while index < len(value):
        char = value[index]
        if char != "\\":
            output.append(char)
            index += 1
            continue
        if index + 1 < len(value) and value[index + 1] == "\\":
            output.extend(("\\", "\\"))
            index += 2
            continue
        output.extend(("\\", "\\"))
        index += 1
    return "".join(output)


def repair(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        return match.group(1) + escape_unescaped_backslashes(match.group(2)) + match.group(3)

    repaired = LATEX_FIELD.sub(replace, original)
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
