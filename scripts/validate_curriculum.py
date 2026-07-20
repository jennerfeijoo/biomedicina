#!/usr/bin/env python3
"""Valida el archivo curricular central de CitoNauta.

Este script comprueba estructura mínima, rutas, duplicados y consistencia
entre áreas y asignaturas antes de generar páginas HTML.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import generate_site

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "citonauta_curriculum.json"
TEMPLATE_PATH = ROOT / "templates" / "asignatura.html"
AREA_TEMPLATE_PATH = ROOT / "templates" / "area.html"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_SUBJECT_FIELDS = {
    "id",
    "title",
    "path",
    "description",
    "status",
    "learning_objectives",
    "modules",
    "key_concepts",
    "biomedical_connection",
}
REQUIRED_TEMPLATE_KEYS = {
    "subject_title",
    "area_title",
    "subject_description",
    "css_path",
    "editorial_css_path",
    "home_path",
    "area_path",
    "previous_link",
    "next_link",
    "biomedical_connection",
    "level",
    "estimated_workload",
    "status",
    "status_label",
    "prerequisites",
    "course_competencies",
    "learning_objectives",
    "learning_outcomes",
    "modules",
    "detailed_units",
    "practical_activities",
    "assessment",
    "key_concepts",
    "related_subjects",
    "suggested_resources",
}
OPTIONAL_LIST_FIELDS = {
    "prerequisites",
    "course_competencies",
    "learning_outcomes",
    "detailed_units",
    "practical_activities",
    "assessment",
    "related_subjects",
    "suggested_resources",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo curricular: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_slug(value: str, label: str, errors: list[str]) -> None:
    if not SLUG_RE.match(value):
        add_error(errors, f"{label} debe ser un slug kebab-case válido: {value!r}")


def validate_template(errors: list[str]) -> None:
    if not TEMPLATE_PATH.exists():
        add_error(errors, f"No existe la plantilla: {TEMPLATE_PATH.relative_to(ROOT)}")
        return
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    for key in sorted(REQUIRED_TEMPLATE_KEYS):
        if "{{ " + key + " }}" not in template:
            add_error(errors, f"La plantilla no contiene la variable requerida: {key}")
    if not AREA_TEMPLATE_PATH.exists():
        add_error(errors, f"No existe la plantilla: {AREA_TEMPLATE_PATH.relative_to(ROOT)}")
        return
    try:
        generate_site.validate_area_template(AREA_TEMPLATE_PATH.read_text(encoding="utf-8"))
    except ValueError as exc:
        add_error(errors, str(exc))


def validate_subject(area_id: str, subject: dict[str, Any], index: int, errors: list[str]) -> None:
    missing = REQUIRED_SUBJECT_FIELDS - set(subject)
    if missing:
        add_error(errors, f"{area_id}.subjects[{index}] no contiene campos requeridos: {sorted(missing)}")
        return

    subject_id = subject.get("id", "")
    validate_slug(subject_id, f"{area_id}.subjects[{index}].id", errors)

    path = subject.get("path", "")
    expected_prefix = f"{area_id}/{subject_id}/"
    if not path.startswith(expected_prefix):
        add_error(errors, f"Ruta inconsistente para {area_id}/{subject_id}: {path!r}; se esperaba prefijo {expected_prefix!r}")
    if not path.endswith("index.html"):
        add_error(errors, f"La ruta de {area_id}/{subject_id} debe terminar en index.html: {path!r}")
    if path.startswith("/") or ".." in Path(path).parts:
        add_error(errors, f"La ruta de {area_id}/{subject_id} debe ser relativa y segura: {path!r}")

    for text_field in ("title", "description", "biomedical_connection"):
        if not str(subject.get(text_field, "")).strip():
            add_error(errors, f"{area_id}/{subject_id} requiere contenido en {text_field}")

    for list_field in ("learning_objectives", "modules", "key_concepts"):
        if not isinstance(subject.get(list_field), list):
            add_error(errors, f"{area_id}/{subject_id}.{list_field} debe ser una lista")

    for list_field in OPTIONAL_LIST_FIELDS:
        if list_field in subject and not isinstance(subject.get(list_field), list):
            add_error(errors, f"{area_id}/{subject_id}.{list_field} debe ser una lista")


def validate_complete_course(area: dict[str, Any], subject: dict[str, Any], errors: list[str]) -> None:
    key = f"{area['id']}/{subject['id']}"
    try:
        course = generate_site.merge_subject_overlay(area, subject)
    except (FileNotFoundError, KeyError, TypeError, ValueError) as exc:
        add_error(errors, f"No se pudo construir el curso {key}: {exc}")
        return

    if course.get("status") not in {"review", "complete"}:
        add_error(errors, f"{key} debe quedar en estado review o complete")

    minimums = {
        "prerequisites": 3,
        "course_competencies": 4,
        "learning_objectives": 4,
        "learning_outcomes": 6,
        "modules": 6,
        "detailed_units": 6,
        "practical_activities": 4,
        "assessment": 3,
        "key_concepts": 10,
        "related_subjects": 4,
        "suggested_resources": 5,
    }
    for field, minimum in minimums.items():
        value = course.get(field)
        if not isinstance(value, list) or len(value) < minimum:
            length = len(value) if isinstance(value, list) else "no es lista"
            add_error(errors, f"{key}.{field} requiere al menos {minimum} elementos; tiene {length}")

    units = course.get("detailed_units", [])
    if isinstance(units, list) and len(units) > 10:
        add_error(errors, f"{key}.detailed_units debe contener entre 6 y 10 unidades; tiene {len(units)}")
    for unit_index, unit in enumerate(units, start=1):
        if not isinstance(unit, dict):
            add_error(errors, f"{key}.detailed_units[{unit_index}] debe ser un objeto")
            continue
        for text_field in ("title", "description"):
            if not str(unit.get(text_field, "")).strip():
                add_error(errors, f"{key}.detailed_units[{unit_index}] requiere {text_field}")
        for list_field, minimum in (("topics", 3), ("learning_outcomes", 2), ("activities", 2), ("biomedical_applications", 1)):
            value = unit.get(list_field)
            if not isinstance(value, list) or len(value) < minimum:
                add_error(errors, f"{key}.detailed_units[{unit_index}].{list_field} requiere al menos {minimum} elementos")

    weights: list[int] = []
    for item in course.get("assessment", []):
        raw_weight = str(item.get("weight", "")).strip().rstrip("%") if isinstance(item, dict) else ""
        if raw_weight.isdigit():
            weights.append(int(raw_weight))
    if weights and sum(weights) != 100:
        add_error(errors, f"{key}.assessment suma {sum(weights)}%; debe sumar 100%")

    for resource_index, resource in enumerate(course.get("suggested_resources", []), start=1):
        if not isinstance(resource, dict):
            add_error(errors, f"{key}.suggested_resources[{resource_index}] debe ser un objeto")
            continue
        url = str(resource.get("url", "")).strip()
        if url and not url.startswith(("https://", "http://")):
            add_error(errors, f"{key}.suggested_resources[{resource_index}] contiene URL no segura: {url!r}")


def validate_curriculum(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if "project" not in data:
        add_error(errors, "Falta la sección project")
    if "areas" not in data or not isinstance(data.get("areas"), list):
        add_error(errors, "Falta la sección areas o no es una lista")
        return errors

    allowed_statuses = set(data.get("editorial_model", {}).get("statuses", []))
    if not allowed_statuses:
        add_error(errors, "editorial_model.statuses debe definir estados editoriales")

    area_ids: set[str] = set()
    subject_paths: set[str] = set()
    global_subject_ids: set[str] = set()

    for area_index, area in enumerate(data["areas"]):
        area_id = area.get("id", "")
        if not area_id:
            add_error(errors, f"areas[{area_index}] no tiene id")
            continue
        validate_slug(area_id, f"areas[{area_index}].id", errors)
        if area_id in area_ids:
            add_error(errors, f"Área duplicada: {area_id}")
        area_ids.add(area_id)

        area_path = area.get("path", "")
        if area_path != f"{area_id}/index.html":
            add_error(errors, f"Ruta de área inconsistente para {area_id}: {area_path!r}")

        subjects = area.get("subjects", [])
        if not isinstance(subjects, list) or not subjects:
            add_error(errors, f"El área {area_id} debe contener una lista de asignaturas")
            continue

        local_subject_ids: set[str] = set()
        for subject_index, subject in enumerate(subjects):
            validate_subject(area_id, subject, subject_index, errors)
            validate_complete_course(area, subject, errors)
            subject_id = subject.get("id", "")
            subject_path = subject.get("path", "")
            subject_status = subject.get("status")

            if subject_id in local_subject_ids:
                add_error(errors, f"Asignatura duplicada dentro de {area_id}: {subject_id}")
            local_subject_ids.add(subject_id)

            global_key = f"{area_id}/{subject_id}"
            if global_key in global_subject_ids:
                add_error(errors, f"Asignatura global duplicada: {global_key}")
            global_subject_ids.add(global_key)

            if subject_path in subject_paths:
                add_error(errors, f"Ruta de asignatura duplicada: {subject_path}")
            subject_paths.add(subject_path)

            if allowed_statuses and subject_status not in allowed_statuses:
                add_error(errors, f"Estado editorial no permitido en {global_key}: {subject_status!r}")

    validate_template(errors)
    return errors


def main() -> int:
    data = load_json(DATA_PATH)
    errors = validate_curriculum(data)

    if errors:
        print("Errores de validación curricular:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    total_subjects = sum(len(area.get("subjects", [])) for area in data.get("areas", []))
    print("Validación curricular completada.")
    print(f"- áreas: {len(data.get('areas', []))}")
    print(f"- asignaturas: {total_subjects}")
    print("- resultado: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
