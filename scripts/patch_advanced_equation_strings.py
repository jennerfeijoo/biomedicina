#!/usr/bin/env python3
"""Normalize legacy equation strings that combine LaTeX and prose."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "advanced_unit_renderer.py"

OLD = '''    if isinstance(equation, str):
        latex = normalize_latex(equation)
        description = ""
        variables: dict[str, Any] = {}
'''

NEW = '''    if isinstance(equation, str):
        raw = equation.strip()
        description = ""
        if raw.startswith("$"):
            closing = raw.find("$", 1)
            if closing > 1:
                latex = normalize_latex(raw[: closing + 1])
                description = raw[closing + 1 :].strip(" .")
            else:
                latex = normalize_latex(raw)
        elif "$" in raw:
            latex_text, description_text = raw.split("$", 1)
            latex = normalize_latex(latex_text)
            description = description_text.strip(" .")
        else:
            latex = normalize_latex(raw)
        variables: dict[str, Any] = {}
'''


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    if NEW in text:
        print("Compatibilidad de ecuaciones ya aplicada.")
        return 0
    if text.count(OLD) != 1:
        raise RuntimeError(f"Se esperaba una coincidencia del bloque y se encontraron {text.count(OLD)}")
    PATH.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print("Compatibilidad de ecuaciones aplicada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
