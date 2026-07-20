#!/usr/bin/env python3
"""Valida la cobertura lectiva unidad por unidad de las 84 asignaturas."""

from __future__ import annotations

import re
from pathlib import Path

import generate_site

ROOT = Path(__file__).resolve().parents[1]
GENERATED_MARKER = 'data-generated="citonauta-unit"'
REQUIRED_GENERATED_SECTIONS = (
    "Resultados de aprendizaje",
    "Desarrollo teórico",
    "Caso biomédico resuelto",
    "Actividad guiada",
    "Autoevaluación con respuestas",
    "Glosario operativo",
    "Fuentes y recursos para profundizar",
    "Respuesta esperada:",
)
FORBIDDEN_MARKERS = ("{{ ", " }}", "Próximamente", "Contenido pendiente")


def validate_units() -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    data = generate_site.load_json(generate_site.DATA_PATH)
    counts = {
        "subjects": 0,
        "expected_units": 0,
        "generated_units": 0,
        "authored_units": 0,
        "unit_indexes": 0,
        "concepts": 0,
        "curated_concepts": 0,
    }

    for area in data.get("areas", []):
        for subject in area.get("subjects", []):
            counts["subjects"] += 1
            course = generate_site.merge_subject_overlay(area, subject)
            frame = generate_site.pedagogical_frame_for(area["id"], course["id"])
            course_path = ROOT / course["path"]
            course_html = course_path.read_text(encoding="utf-8", errors="ignore") if course_path.exists() else ""
            units = course.get("detailed_units", [])
            counts["expected_units"] += len(units)
            unit_dir = course_path.parent / "unidades"
            index_path = unit_dir / "index.html"
            if not index_path.exists():
                errors.append(f"Falta índice de unidades: {index_path.relative_to(ROOT)}")
            else:
                counts["unit_indexes"] += 1
                index_html = index_path.read_text(encoding="utf-8", errors="ignore")
                for unit in units:
                    href = f'unidad-{int(unit["unit"]):02d}.html'
                    if href not in index_html:
                        errors.append(f"El índice {index_path.relative_to(ROOT)} no enlaza {href}")

            for unit in units:
                for topic in unit.get("topics", []):
                    counts["concepts"] += 1
                    if generate_site.concept_definition(topic, course, frame)[1]:
                        counts["curated_concepts"] += 1
                number = int(unit["unit"])
                unit_path = unit_dir / f"unidad-{number:02d}.html"
                counts_key = "generated_units"
                if not unit_path.exists():
                    errors.append(f"Falta unidad: {unit_path.relative_to(ROOT)}")
                    continue
                unit_html = unit_path.read_text(encoding="utf-8", errors="ignore")
                if len(unit_html) < 1400:
                    errors.append(f"Unidad demasiado breve: {unit_path.relative_to(ROOT)}")
                if any(marker in unit_html for marker in FORBIDDEN_MARKERS):
                    errors.append(f"Unidad con marcador pendiente: {unit_path.relative_to(ROOT)}")
                if f"unidad-{number:02d}.html" not in course_html:
                    errors.append(f"El curso {course_path.relative_to(ROOT)} no enlaza su unidad {number}")

                if GENERATED_MARKER in unit_html:
                    counts["generated_units"] += 1
                    for section in REQUIRED_GENERATED_SECTIONS:
                        if section not in unit_html:
                            errors.append(f"{unit_path.relative_to(ROOT)} no contiene la sección: {section}")
                    if unit_html.count('<article class="lesson-topic">') < 3:
                        errors.append(f"{unit_path.relative_to(ROOT)} requiere tres desarrollos conceptuales")
                    if unit_html.count('<details class="answer-panel">') < 7:
                        errors.append(f"{unit_path.relative_to(ROOT)} requiere caso y seis respuestas desplegables")
                    if len(re.findall(r'https://', unit_html)) < 5:
                        errors.append(f"{unit_path.relative_to(ROOT)} requiere cinco recursos enlazados")
                else:
                    counts["authored_units"] += 1

    if counts["subjects"] != 84:
        errors.append(f"Se esperaban 84 asignaturas y se encontraron {counts['subjects']}")
    if counts["generated_units"] + counts["authored_units"] != counts["expected_units"]:
        errors.append("La suma de unidades generadas y editoriales no coincide con el currículo")
    concept_coverage = counts["curated_concepts"] / max(counts["concepts"], 1)
    if concept_coverage < 0.40:
        errors.append(f"La cobertura de definiciones disciplinares es {concept_coverage:.1%}; se requiere al menos 40%")
    return errors, counts


def main() -> int:
    errors, counts = validate_units()
    if errors:
        print("Errores de cobertura por unidades:\n")
        for error in errors:
            print(f"- {error}")
        print(f"\nResumen: {counts}")
        return 1
    print("Validación de unidades completada.")
    for key, value in counts.items():
        print(f"- {key}: {value}")
    print("- resultado: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
