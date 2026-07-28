#!/usr/bin/env python3
"""Promueve asignaturas provisionales cuando su paquete reconstruido se publica.

La operación mantiene sincronizados el currículo canónico y el inventario
provisional. Solo actúa sobre asignaturas incluidas en el manifiesto de
publicación y conserva el estado editorial declarado por el paquete fuente.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = ROOT / "data" / "citonauta_curriculum.json"
PROVISIONAL_PATH = ROOT / "data" / "provisional_subjects.json"
REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"
DEFAULT_MANIFEST = ROOT / "publication-manifest.json"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)}: la raíz debe ser un objeto JSON")
    return data


def serialize(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def curriculum_subjects(curriculum: dict[str, Any]) -> dict[str, tuple[dict[str, Any], dict[str, Any]]]:
    subjects: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for area in curriculum.get("areas", []):
        if not isinstance(area, dict):
            continue
        for subject in area.get("subjects", []):
            if not isinstance(subject, dict):
                continue
            subject_id = str(subject.get("id", "")).strip()
            if subject_id:
                subjects[subject_id] = (area, subject)
    return subjects


def build_subject_entry(
    provisional: dict[str, Any],
    course: dict[str, Any],
    manifest_course: dict[str, Any],
) -> dict[str, Any]:
    subject_id = str(course["id"])
    area_id = str(course["area_id"])
    path = str(
        provisional.get("path")
        or manifest_course.get("public_path")
        or f"{area_id}/{subject_id}/index.html"
    )
    return {
        "id": subject_id,
        "title": str(course.get("title") or provisional.get("title") or subject_id),
        "path": path,
        "description": str(course.get("description") or provisional.get("description") or ""),
        "status": str(course.get("status") or "review"),
        "learning_objectives": list(course.get("learning_objectives") or []),
        "modules": list(course.get("modules") or []),
        "key_concepts": list(course.get("key_concepts") or []),
        "biomedical_connection": str(
            course.get("biomedical_connection")
            or provisional.get("biomedical_connection")
            or ""
        ),
    }


def promote(
    curriculum: dict[str, Any],
    provisional_data: dict[str, Any],
    manifest: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    curriculum = copy.deepcopy(curriculum)
    provisional_data = copy.deepcopy(provisional_data)
    existing = curriculum_subjects(curriculum)
    provisional_rows = [
        row for row in provisional_data.get("subjects", []) if isinstance(row, dict)
    ]
    provisional_by_id = {
        str(row.get("id", "")).strip(): row
        for row in provisional_rows
        if str(row.get("id", "")).strip()
    }
    areas = {
        str(area.get("id", "")).strip(): area
        for area in curriculum.get("areas", [])
        if isinstance(area, dict) and str(area.get("id", "")).strip()
    }

    promoted: list[str] = []
    for manifest_course in manifest.get("courses", []):
        if not isinstance(manifest_course, dict):
            continue
        subject_id = str(manifest_course.get("subject_id", "")).strip()
        if not subject_id or subject_id not in provisional_by_id:
            continue

        source = REDEVELOPMENT_ROOT / subject_id / "course.json"
        course = load_json(source)
        if str(course.get("id", "")).strip() != subject_id:
            raise ValueError(f"{source.relative_to(ROOT)}: id no coincide con {subject_id}")
        area_id = str(course.get("area_id", "")).strip()
        area = areas.get(area_id)
        if area is None:
            raise ValueError(f"{subject_id}: área curricular desconocida {area_id}")

        entry = build_subject_entry(provisional_by_id[subject_id], course, manifest_course)
        if subject_id in existing:
            existing_area, existing_entry = existing[subject_id]
            if str(existing_area.get("id")) != area_id:
                raise ValueError(f"{subject_id}: ya existe en otra área curricular")
            existing_entry.clear()
            existing_entry.update(entry)
        else:
            area.setdefault("subjects", []).append(entry)
            existing[subject_id] = (area, entry)

        promoted.append(subject_id)

    if promoted:
        promoted_set = set(promoted)
        provisional_data["subjects"] = [
            row
            for row in provisional_rows
            if str(row.get("id", "")).strip() not in promoted_set
        ]
        for area in curriculum.get("areas", []):
            if isinstance(area, dict) and isinstance(area.get("subjects"), list):
                area["subjects"].sort(
                    key=lambda row: (
                        str(row.get("title", "")).casefold(),
                        str(row.get("id", "")),
                    )
                )

    return curriculum, provisional_data, sorted(set(promoted))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promueve al currículo las asignaturas provisionales publicadas."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--check",
        action="store_true",
        help="No escribe; falla si la promoción esperada no está materializada.",
    )
    args = parser.parse_args()

    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    curriculum = load_json(CURRICULUM_PATH)
    provisional = load_json(PROVISIONAL_PATH)
    manifest = load_json(manifest_path)
    expected_curriculum, expected_provisional, promoted = promote(
        curriculum, provisional, manifest
    )

    if args.check:
        if serialize(curriculum) != serialize(expected_curriculum):
            print("ERROR: el currículo no contiene todas las promociones esperadas")
            return 1
        if serialize(provisional) != serialize(expected_provisional):
            print("ERROR: el inventario provisional conserva asignaturas ya promovibles")
            return 1
        print("Promoción provisional sincronizada.")
        return 0

    CURRICULUM_PATH.write_text(serialize(expected_curriculum), encoding="utf-8")
    PROVISIONAL_PATH.write_text(serialize(expected_provisional), encoding="utf-8")
    if promoted:
        print("Asignaturas promovidas: " + ", ".join(promoted))
    else:
        print("No hay asignaturas provisionales que promover en este manifiesto.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
