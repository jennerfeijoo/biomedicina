#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "data" / "course_plan_packages"
OUTLINES_PATH = ROOT / "data" / "course_outlines.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_units(source: str, outlines: dict[str, Any]) -> list[dict[str, Any]]:
    path_text, separator, fragment = source.partition("#/")
    if not separator:
        raise ValueError(f"Fuente de unidades sin fragmento JSON: {source}")

    path = ROOT / path_text
    if path == OUTLINES_PATH:
        parts = fragment.split("/")
        if len(parts) != 2:
            raise ValueError(f"Referencia inválida a course_outlines: {source}")
        area_id, subject_id = parts
        raw_units = outlines.get(area_id, {}).get(subject_id)
        if not isinstance(raw_units, list):
            raise ValueError(f"No existen unidades para {area_id}/{subject_id}")
        units: list[dict[str, Any]] = []
        for number, raw in enumerate(raw_units, start=1):
            if not isinstance(raw, list) or len(raw) != 3:
                raise ValueError(f"Unidad {number} inválida en {source}")
            units.append(
                {
                    "unit": number,
                    "title": raw[0],
                    "core_topics": raw[1],
                    "biomedical_focus": raw[2],
                }
            )
        return units

    data = load_json(path)
    current: Any = data
    for part in fragment.split("/"):
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"Fragmento inexistente en {source}: {part}")
        current = current[part]
    if not isinstance(current, list):
        raise ValueError(f"La fuente no resuelve a una lista de unidades: {source}")
    return current


def validate_package(path: Path, outlines: dict[str, Any]) -> tuple[int, int]:
    package = load_json(path)
    subjects = package.get("subjects")
    order = package.get("generation_order")
    if not isinstance(subjects, list) or not subjects:
        raise ValueError(f"{path}: subjects debe ser una lista no vacía")
    if not isinstance(order, list):
        raise ValueError(f"{path}: generation_order debe ser una lista")

    ids = [str(item.get("id") or "") for item in subjects]
    if len(ids) != len(set(ids)) or "" in ids:
        raise ValueError(f"{path}: identificadores vacíos o duplicados")
    if set(order) != set(ids) or len(order) != len(ids):
        raise ValueError(f"{path}: generation_order no coincide con subjects")
    if package.get("subject_count") != len(subjects):
        raise ValueError(f"{path}: subject_count no coincide con subjects")

    position = {subject_id: index for index, subject_id in enumerate(order)}
    total_units = 0
    for subject in subjects:
        subject_id = str(subject["id"])
        prerequisites = subject.get("prerequisite_subjects", [])
        if not isinstance(prerequisites, list):
            raise ValueError(f"{path}: prerrequisitos inválidos en {subject_id}")
        for prerequisite in prerequisites:
            if prerequisite not in position:
                raise ValueError(
                    f"{path}: {subject_id} depende de una asignatura fuera del paquete: {prerequisite}"
                )
            if position[prerequisite] >= position[subject_id]:
                raise ValueError(
                    f"{path}: orden inválido; {prerequisite} debe preceder a {subject_id}"
                )

        units = resolve_units(str(subject.get("unit_source") or ""), outlines)
        expected_count = int(subject.get("unit_count") or 0)
        titles = subject.get("unit_titles")
        actual_titles = [str(unit.get("title") or "") for unit in units]
        if expected_count != len(units):
            raise ValueError(
                f"{path}: {subject_id} declara {expected_count} unidades y resuelve {len(units)}"
            )
        if titles != actual_titles:
            raise ValueError(f"{path}: títulos de unidades desincronizados en {subject_id}")
        if any(not title.strip() for title in actual_titles):
            raise ValueError(f"{path}: título de unidad vacío en {subject_id}")
        total_units += len(units)

    if package.get("planned_unit_count") != total_units:
        raise ValueError(
            f"{path}: planned_unit_count={package.get('planned_unit_count')} pero se resolvieron {total_units}"
        )

    contract = package.get("shared_unit_contract", {})
    required_sections = contract.get("required_sections", [])
    if not isinstance(required_sections, list) or len(required_sections) < 8:
        raise ValueError(f"{path}: contrato pedagógico incompleto")
    return len(subjects), total_units


def main() -> int:
    outlines = load_json(OUTLINES_PATH)
    package_paths = sorted(PACKAGE_DIR.glob("*.json"))
    if not package_paths:
        raise SystemExit("No se encontraron paquetes de planificación.")

    total_subjects = 0
    total_units = 0
    for path in package_paths:
        subjects, units = validate_package(path, outlines)
        total_subjects += subjects
        total_units += units
        print(f"OK {path.relative_to(ROOT)}: {subjects} asignaturas, {units} unidades")
    print(f"Paquetes válidos: {len(package_paths)} · {total_subjects} asignaturas · {total_units} unidades")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
