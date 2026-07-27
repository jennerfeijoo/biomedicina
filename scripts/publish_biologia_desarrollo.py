#!/usr/bin/env python3
"""Promueve la reconstrucción de Biología del Desarrollo a las capas públicas.

La fuente académica permanece en data/course_redevelopment. Este script copia
las 14 unidades validadas a data/generated_units, crea el overlay editorial que
consume generate_site.py y sincroniza los metadatos compatibles del curso
avanzado. No genera HTML: esa fase corresponde a scripts/generate_site.py.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUBJECT_ID = "biologia-desarrollo"
AREA_ID = "biologicas-medicas"
EXPECTED_UNITS = list(range(1, 15))

SOURCE_ROOT = ROOT / "data" / "course_redevelopment" / SUBJECT_ID
SOURCE_COURSE = SOURCE_ROOT / "course.json"
SOURCE_UNITS = SOURCE_ROOT / "units"
TARGET_UNITS = ROOT / "data" / "generated_units" / SUBJECT_ID
OVERLAY_PATH = ROOT / "data" / "subjects" / AREA_ID / f"{SUBJECT_ID}.json"
GENERATED_COURSE = ROOT / "data" / "generated_courses" / f"{SUBJECT_ID}.json"
PUBLIC_COURSE_DIR = ROOT / AREA_ID / SUBJECT_ID
ADVANCED_MARKER = "<!-- advanced-unit-renderer:v1 -->"
GENERATED_MARKER = 'data-generated="citonauta-unit"'


def load_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)}: la raíz debe ser un objeto JSON")
    return data


def write_object(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_weight(value: Any) -> float:
    match = re.search(r"-?\d+(?:[.,]\d+)?", str(value or ""))
    if not match:
        raise ValueError(f"ponderación inválida: {value!r}")
    return float(match.group(0).replace(",", "."))


def source_unit_path(unit_number: int) -> Path:
    return SOURCE_UNITS / f"unit-{unit_number:02d}.json"


def target_unit_path(unit_number: int) -> Path:
    return TARGET_UNITS / f"unit-{unit_number:02d}.json"


def validate_source() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    course = load_object(SOURCE_COURSE)
    if course.get("id") != SUBJECT_ID:
        raise ValueError("course.json: id no coincide con la asignatura")
    if course.get("area_id") != AREA_ID:
        raise ValueError("course.json: area_id no coincide con el área pública")

    detailed_units = course.get("detailed_units")
    if not isinstance(detailed_units, list):
        raise ValueError("course.json: detailed_units debe ser una lista")
    declared_numbers = [int(item.get("unit", 0)) for item in detailed_units if isinstance(item, dict)]
    if declared_numbers != EXPECTED_UNITS:
        raise ValueError(
            f"course.json: secuencia de unidades {declared_numbers}; se esperaba {EXPECTED_UNITS}"
        )

    units: list[dict[str, Any]] = []
    declared_by_number = {int(item["unit"]): item for item in detailed_units}
    for number in EXPECTED_UNITS:
        path = source_unit_path(number)
        if not path.exists():
            raise FileNotFoundError(f"falta {path.relative_to(ROOT)}")
        unit = load_object(path)
        if unit.get("schema_version") != "2.0":
            raise ValueError(f"{path.relative_to(ROOT)}: schema_version debe ser 2.0")
        if unit.get("subject_id") != SUBJECT_ID or unit.get("area_id") != AREA_ID:
            raise ValueError(f"{path.relative_to(ROOT)}: identidad curricular inconsistente")
        if int(unit.get("unit", 0)) != number:
            raise ValueError(f"{path.relative_to(ROOT)}: número de unidad inconsistente")
        if unit.get("status") not in {"review", "complete"}:
            raise ValueError(f"{path.relative_to(ROOT)}: status debe ser review o complete")
        for key in ("title", "purpose", "learning_objectives", "theory_sections", "sources"):
            if unit.get(key) in (None, "", []):
                raise ValueError(f"{path.relative_to(ROOT)}: falta contenido en {key}")
        declared_title = str(declared_by_number[number].get("title", "")).strip()
        if declared_title and str(unit.get("title", "")).strip() != declared_title:
            raise ValueError(
                f"{path.relative_to(ROOT)}: el título no coincide con detailed_units del curso"
            )
        units.append(unit)
    return course, units


def assessment_plan(course: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in course.get("assessment", []):
        if not isinstance(item, dict):
            continue
        result.append(
            {
                "component": str(item.get("title", "Componente")).strip(),
                "weight_percent": parse_weight(item.get("weight")),
                "description": str(item.get("description", "")).strip(),
            }
        )
    total = sum(float(item["weight_percent"]) for item in result)
    if abs(total - 100.0) > 1e-9:
        raise ValueError(f"las ponderaciones del curso suman {total:g} %, no 100 %")
    return result


def expected_generated_course(existing: dict[str, Any], course: dict[str, Any]) -> dict[str, Any]:
    updated = dict(existing)
    updated.update(
        {
            "schema_version": "2.0",
            "subject_id": SUBJECT_ID,
            "title": course["title"],
            "status": "review",
            "academic_level": course["level"],
            "course_purpose": course["description"],
            "prerequisites": course["prerequisites"],
            "course_competencies": course["course_competencies"],
            "learning_outcomes": course["learning_outcomes"],
            "assessment_plan": assessment_plan(course),
        }
    )
    return updated


def promote() -> None:
    course, _ = validate_source()

    TARGET_UNITS.mkdir(parents=True, exist_ok=True)
    expected_names = {f"unit-{number:02d}.json" for number in EXPECTED_UNITS}
    for stale in TARGET_UNITS.glob("unit-*.json"):
        if stale.name not in expected_names:
            stale.unlink()

    for number in EXPECTED_UNITS:
        shutil.copyfile(source_unit_path(number), target_unit_path(number))

    OVERLAY_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_COURSE, OVERLAY_PATH)

    existing_course = load_object(GENERATED_COURSE)
    write_object(GENERATED_COURSE, expected_generated_course(existing_course, course))

    print("Promoción completada:")
    print(f"- overlay: {OVERLAY_PATH.relative_to(ROOT)}")
    print(f"- unidades avanzadas: {len(EXPECTED_UNITS)}")
    print(f"- curso avanzado: {GENERATED_COURSE.relative_to(ROOT)}")


def check_promoted() -> None:
    course, _ = validate_source()
    errors: list[str] = []

    if not OVERLAY_PATH.exists() or OVERLAY_PATH.read_bytes() != SOURCE_COURSE.read_bytes():
        errors.append("el overlay público no coincide exactamente con course.json")

    target_files = sorted(path.name for path in TARGET_UNITS.glob("unit-*.json"))
    expected_files = [f"unit-{number:02d}.json" for number in EXPECTED_UNITS]
    if target_files != expected_files:
        errors.append(f"generated_units contiene {target_files}; se esperaba {expected_files}")

    for number in EXPECTED_UNITS:
        source = source_unit_path(number)
        target = target_unit_path(number)
        if not target.exists() or target.read_bytes() != source.read_bytes():
            errors.append(f"unidad {number:02d}: la copia pública no coincide con la fuente")

    generated = load_object(GENERATED_COURSE)
    expected = expected_generated_course(generated, course)
    for key in (
        "schema_version",
        "subject_id",
        "title",
        "status",
        "academic_level",
        "course_purpose",
        "prerequisites",
        "course_competencies",
        "learning_outcomes",
        "assessment_plan",
    ):
        if generated.get(key) != expected.get(key):
            errors.append(f"generated_courses: el campo {key} no está sincronizado")

    if errors:
        raise SystemExit("Promoción desincronizada:\n- " + "\n- ".join(errors))
    print("Promoción sincronizada: 14 de 14 unidades y metadatos coherentes.")


def check_public_pages() -> None:
    errors: list[str] = []
    course_index = PUBLIC_COURSE_DIR / "index.html"
    units_index = PUBLIC_COURSE_DIR / "unidades" / "index.html"
    if not course_index.exists():
        errors.append("falta la página pública de la asignatura")
    if not units_index.exists():
        errors.append("falta el índice público de unidades")

    course_text = course_index.read_text(encoding="utf-8", errors="replace") if course_index.exists() else ""
    units_text = units_index.read_text(encoding="utf-8", errors="replace") if units_index.exists() else ""
    if "Unidad 14" not in course_text:
        errors.append("la página de asignatura no presenta la Unidad 14")
    if "14 unidades" not in units_text and "14" not in units_text:
        errors.append("el índice de unidades no declara la ruta de 14 unidades")

    for number in EXPECTED_UNITS:
        page = PUBLIC_COURSE_DIR / "unidades" / f"unidad-{number:02d}.html"
        if not page.exists():
            errors.append(f"falta {page.relative_to(ROOT)}")
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        if GENERATED_MARKER not in text:
            errors.append(f"{page.relative_to(ROOT)}: falta marcador de página generada")
        if ADVANCED_MARKER not in text:
            errors.append(f"{page.relative_to(ROOT)}: falta contenido del renderer avanzado")
        title = str(load_object(target_unit_path(number)).get("title", "")).strip()
        if title and title.casefold() not in text.casefold():
            errors.append(f"{page.relative_to(ROOT)}: no contiene el título avanzado")

    if errors:
        raise SystemExit("Publicación incompleta:\n- " + "\n- ".join(errors))
    print("Publicación verificada: asignatura e índice con 14 unidades avanzadas.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promueve y verifica la reconstrucción pública de Biología del Desarrollo."
    )
    parser.add_argument("--check", action="store_true", help="Comprueba la promoción sin escribir archivos.")
    parser.add_argument(
        "--check-public",
        action="store_true",
        help="Comprueba que las 14 páginas HTML públicas estén generadas y sincronizadas.",
    )
    args = parser.parse_args()

    if args.check_public:
        check_promoted()
        check_public_pages()
    elif args.check:
        check_promoted()
    else:
        promote()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
