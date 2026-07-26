#!/usr/bin/env python3
"""Enforce the self-paced learning model and reject fixed study-time metadata."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COURSE_KEYS = {"estimated_workload", "duration_weeks", "weekly_hours", "total_workload_hours", "semester_plan"}
UNIT_KEYS = {"estimated_hours", "weeks"}
TEXT_SUFFIXES = {".py", ".js", ".css", ".html", ".md", ".yml", ".yaml", ".json"}
FORBIDDEN_UI = ("Carga estimada", "Tiempo sugerido", "horas estimadas", "horas semanales", "horas totales de estudio")
DUPLICATE_QUE = re.compile(r"\bque\s+que\b", re.IGNORECASE)

def find_keys(value: Any, forbidden: set[str], prefix: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            current = f"{prefix}.{key}" if prefix else key
            if key in forbidden:
                errors.append(current)
            errors.extend(find_keys(child, forbidden, current))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(find_keys(child, forbidden, f"{prefix}[{index}]"))
    return errors

def main() -> int:
    errors: list[str] = []
    old_paths = (
        "assets/js/semester-course.js",
        "assets/css/semester-course.css",
        "scripts/audit_semester_readiness.py",
        "scripts/audit_semester_portfolio.py",
    )
    for relative in old_paths:
        if (ROOT / relative).exists():
            errors.append(f"ruta temporal obsoleta presente: {relative}")

    for path in sorted((ROOT / "data" / "generated_courses").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for location in find_keys(data, COURSE_KEYS):
            errors.append(f"{path.relative_to(ROOT)} conserva {location}")
    for path in sorted((ROOT / "data" / "generated_units").glob("*/unit-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for location in find_keys(data, UNIT_KEYS):
            errors.append(f"{path.relative_to(ROOT)} conserva {location}")
    for path in sorted((ROOT / "data" / "subjects").glob("*/*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for location in find_keys(data, {"estimated_workload"}):
            errors.append(f"{path.relative_to(ROOT)} conserva {location}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if DUPLICATE_QUE.search(text):
            errors.append(f"duplicación tipográfica en {path.relative_to(ROOT)}")
        lowered = text.casefold()
        if path.suffix.lower() in {".html", ".js"} or path.name in {"asignatura.html", "unidad.html"}:
            for phrase in FORBIDDEN_UI:
                if phrase.casefold() in lowered:
                    errors.append(f"referencia temporal pública en {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("Errores del modelo autogestionado:\n")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1
    print("Modelo de aprendizaje autogestionado validado.")
    print("- sin cargas horarias ni calendarios estándar")
    print("- sin nomenclatura interna basada en cursos temporizados")
    print("- sin duplicación tipográfica consecutiva de 'que'")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
