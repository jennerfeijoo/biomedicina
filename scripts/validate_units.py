#!/usr/bin/env python3
"""Valida la cobertura pública unidad por unidad del currículo canónico.

La validación distingue tres arquitecturas:
- páginas generadas desde JSON avanzado;
- páginas generadas mediante el renderer de respaldo;
- páginas autorales, con o sin una fuente JSON avanzada equivalente.

La profundidad científica del JSON avanzado se comprueba en
validate_generated_units.py y su correspondencia pública en
audit_public_unit_alignment.py. Este script valida cobertura, navegación y
estructura sin imponer cuotas homogéneas de palabras, ecuaciones o enlaces ni
mantener conteos históricos fijos de asignaturas.
"""

from __future__ import annotations

from pathlib import Path

import generate_site

ROOT = Path(__file__).resolve().parents[1]
GENERATED_MARKER = 'data-generated="citonauta-unit"'
ADVANCED_MARKER = "<!-- advanced-unit-renderer:v1 -->"
AUTHORED_MARKER = 'data-authored-unit="true"'
REQUIRED_PUBLIC_SECTIONS = (
    "Objetivos y resultados esperados",
    "Desarrollo teórico",
    "Ejemplos y casos resueltos",
    "Actividad aplicada",
    "Errores frecuentes y autoevaluación",
    "Glosario disciplinar",
    "Fuentes específicas de la unidad",
)
FORBIDDEN_MARKERS = ("{{ ", " }}", "Próximamente", "Contenido pendiente")


def validate_units() -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    data = generate_site.load_json(generate_site.DATA_PATH)
    counts = {
        "subjects": 0,
        "expected_units": 0,
        "advanced_generated_units": 0,
        "fallback_generated_units": 0,
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
            course_html = (
                course_path.read_text(encoding="utf-8", errors="ignore")
                if course_path.exists()
                else ""
            )
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
                if not unit_path.exists():
                    errors.append(f"Falta unidad: {unit_path.relative_to(ROOT)}")
                    continue
                unit_html = unit_path.read_text(encoding="utf-8", errors="ignore")
                relative = unit_path.relative_to(ROOT)
                advanced_source = generate_site.load_advanced_unit(ROOT, course["id"], number)

                if any(marker in unit_html for marker in FORBIDDEN_MARKERS):
                    errors.append(f"Unidad con marcador pendiente: {relative}")
                if f"unidad-{number:02d}.html" not in course_html:
                    errors.append(f"El curso {course_path.relative_to(ROOT)} no enlaza su unidad {number}")

                if GENERATED_MARKER in unit_html:
                    for section in REQUIRED_PUBLIC_SECTIONS:
                        if section not in unit_html:
                            errors.append(f"{relative} no contiene la sección pública: {section}")

                    if advanced_source is not None:
                        counts["advanced_generated_units"] += 1
                        if ADVANCED_MARKER not in unit_html:
                            errors.append(f"{relative} no contiene el renderer avanzado")
                        if 'class="lesson-topic advanced-theory-section"' not in unit_html:
                            errors.append(f"{relative} no publica secciones teóricas avanzadas")
                    else:
                        counts["fallback_generated_units"] += 1
                        if '<article class="lesson-topic' not in unit_html:
                            errors.append(f"{relative} no contiene desarrollo conceptual de respaldo")
                else:
                    counts["authored_units"] += 1
                    if advanced_source is not None and AUTHORED_MARKER not in unit_html:
                        errors.append(
                            f"Unidad autoral avanzada no registrada o sin sincronizar: {relative}"
                        )

    if counts["subjects"] == 0:
        errors.append("El currículo canónico no contiene asignaturas")

    published = (
        counts["advanced_generated_units"]
        + counts["fallback_generated_units"]
        + counts["authored_units"]
    )
    if published != counts["expected_units"]:
        errors.append(
            "La suma de unidades avanzadas, de respaldo y autorales no coincide con el currículo"
        )
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
    coverage = counts["curated_concepts"] / max(counts["concepts"], 1)
    print(f"- cobertura diagnóstica de definiciones curadas: {coverage:.1%}")
    print("- resultado: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
