#!/usr/bin/env python3
"""Recognize applied authored sections without requiring one exact heading."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "audit_public_unit_alignment.py"
OLD = '("actividad", "aplicaciones biomédicas", "caso")'
NEW = '("actividad", "aplicaciones", "caso")'


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    if NEW in text:
        print("Marcador de aplicaciones ya generalizado.")
        return 0
    if text.count(OLD) != 1:
        raise RuntimeError(f"Se esperaba una coincidencia y se encontraron {text.count(OLD)}")
    PATH.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print("Marcador de aplicaciones generalizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
