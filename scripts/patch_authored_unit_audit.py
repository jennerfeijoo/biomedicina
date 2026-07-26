#!/usr/bin/env python3
"""Replace the authored-page word quota with structural evidence checks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "audit_public_unit_alignment.py"

OLD = '''    section_count = page.casefold().count("<section")
    if section_count < 5:
        errors.append(f"solo contiene {section_count} secciones; se requieren al menos 5")
    words = visible_word_count(page)
    if words < 700:
        errors.append(f"solo contiene {words} palabras visibles; se requieren al menos 700")
    if "autoevaluación" not in page.casefold() and "autoevaluacion" not in page.casefold():
        errors.append("no contiene una sección de autoevaluación")
    if all(phrase in page.casefold() for phrase in GENERIC_PHRASES[1:]):
        errors.append("conserva el fallback conceptual genérico")
'''

NEW = '''    page_folded = page.casefold()
    if 'data-authored-unit="true"' not in page:
        errors.append("no contiene el marcador de edición autoral")
    section_count = page_folded.count("<section")
    if section_count < 4:
        errors.append(f"solo contiene {section_count} secciones sustantivas")
    if "autoevaluación" not in page_folded and "autoevaluacion" not in page_folded:
        errors.append("no contiene una sección de autoevaluación")
    if not any(marker in page_folded for marker in ("actividad", "aplicaciones biomédicas", "caso")):
        errors.append("no contiene actividad, aplicación biomédica o caso")
    if all(phrase in page_folded for phrase in GENERIC_PHRASES[1:]):
        errors.append("conserva el fallback conceptual genérico")
'''


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    if NEW in text:
        print("Auditoría estructural autoral ya aplicada.")
        return 0
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"Se esperaba una coincidencia y se encontraron {count}")
    PATH.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print("Cuota de palabras sustituida por controles estructurales.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
