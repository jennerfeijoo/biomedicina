#!/usr/bin/env python3
"""Validate generated catalog, filters, editorial statuses, and track integrity."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = ROOT / "data" / "citonauta_curriculum.json"
TRACKS_PATH = ROOT / "data" / "tracks.json"
PROVISIONAL_PATH = ROOT / "data" / "provisional_subjects.json"
STATUSES_PATH = ROOT / "data" / "catalog_statuses.json"
MIN_INTERDISCIPLINARY_TRACKS = 6
MIN_SUBJECTS_PER_TRACK = 6


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def status_ids(
    payload: dict[str, Any],
    key: str,
    known_subjects: set[str],
    errors: list[str],
) -> set[str]:
    raw = payload.get(key)
    if not isinstance(raw, list):
        errors.append(f"catalog_statuses.json: {key} debe ser una lista")
        return set()
    values = [str(item).strip() for item in raw if str(item).strip()]
    if len(values) != len(set(values)):
        errors.append(f"catalog_statuses.json: {key} contiene identificadores duplicados")
    unknown = sorted(set(values) - known_subjects)
    if unknown:
        errors.append(
            f"catalog_statuses.json: {key} contiene asignaturas inexistentes: {', '.join(unknown)}"
        )
    return set(values)


def validate_status_manifest(
    core_subjects: dict[str, dict[str, Any]],
    errors: list[str],
) -> dict[str, set[str]]:
    empty = {"developed": set(), "complete": set(), "pending": set()}
    if not STATUSES_PATH.exists():
        errors.append("falta data/catalog_statuses.json")
        return empty

    payload = load_json(STATUSES_PATH)
    known = set(core_subjects)
    memberships = {
        key: status_ids(payload, key, known, errors)
        for key in ("developed", "complete", "pending")
    }
    developed = memberships["developed"]
    complete = memberships["complete"]
    pending = memberships["pending"]

    if not complete.issubset(developed):
        invalid = sorted(complete - developed)
        errors.append(
            "catalog_statuses.json: complete debe ser subconjunto de developed: "
            + ", ".join(invalid)
        )
    overlap = sorted(developed.intersection(pending))
    if overlap:
        errors.append(
            "catalog_statuses.json: developed y pending se superponen: " + ", ".join(overlap)
        )
    represented = developed.union(pending)
    missing = sorted(known - represented)
    if missing:
        errors.append(
            "catalog_statuses.json: asignaturas centrales sin estado: " + ", ".join(missing)
        )
    extra_partition = sorted(represented - known)
    if extra_partition:
        errors.append(
            "catalog_statuses.json: la partición contiene asignaturas inexistentes: "
            + ", ".join(extra_partition)
        )

    counts = payload.get("counts")
    if not isinstance(counts, dict):
        errors.append("catalog_statuses.json: falta el objeto counts")
    else:
        expected_counts = {
            "catalog_courses": len(known),
            "developed": len(developed),
            "complete": len(complete),
            "pending": len(pending),
        }
        for key, expected in expected_counts.items():
            if counts.get(key) != expected:
                errors.append(
                    f"catalog_statuses.json: counts.{key}={counts.get(key)!r}; se esperaba {expected}"
                )

    return memberships


def main() -> int:
    curriculum = load_json(CURRICULUM_PATH)
    tracks_data = load_json(TRACKS_PATH)
    provisional_data = load_json(PROVISIONAL_PATH) if PROVISIONAL_PATH.exists() else {"subjects": []}
    areas = curriculum.get("areas", [])
    core_subjects = {
        subject["id"]: {"area_id": area["id"], "subject": subject, "provisional": False}
        for area in areas
        for subject in area.get("subjects", [])
    }
    provisional_list = provisional_data.get("subjects", [])
    provisional_ids = [subject.get("id") for subject in provisional_list]
    provisional_subjects = {
        subject["id"]: {
            "area_id": subject.get("area_id"),
            "subject": subject,
            "provisional": True,
        }
        for subject in provisional_list
        if subject.get("id")
    }
    subjects = {**core_subjects, **provisional_subjects}
    area_ids = {area.get("id") for area in areas}
    errors: list[str] = []

    if len(provisional_ids) != len(set(provisional_ids)):
        errors.append("los identificadores de asignaturas provisionales no son únicos")
    collisions = sorted(set(core_subjects).intersection(provisional_subjects))
    if collisions:
        errors.append("asignaturas provisionales duplicadas en el currículo central: " + ", ".join(collisions))

    for subject_id, record in provisional_subjects.items():
        subject = record["subject"]
        if record["area_id"] not in area_ids:
            errors.append(f"{subject_id}: área provisional inexistente: {record['area_id']}")
        if subject.get("status") != "placeholder":
            errors.append(f"{subject_id}: una asignatura provisional debe permanecer en estado placeholder")
        path_value = str(subject.get("path", "")).strip()
        if not path_value:
            errors.append(f"{subject_id}: falta la ruta pública provisional")
        elif not (ROOT / path_value).exists():
            errors.append(f"{subject_id}: no existe la página pública {path_value}")
        for field in ("title", "description", "biomedical_connection"):
            if not str(subject.get(field, "")).strip():
                errors.append(f"{subject_id}: falta {field}")

    statuses = validate_status_manifest(core_subjects, errors)

    tracks = tracks_data.get("tracks", [])
    track_ids = [track.get("id") for track in tracks]
    if len(track_ids) != len(set(track_ids)):
        errors.append("los identificadores de rutas no son únicos")
    if len(tracks) < MIN_INTERDISCIPLINARY_TRACKS:
        errors.append(
            f"se requieren al menos {MIN_INTERDISCIPLINARY_TRACKS} rutas explícitas y se encontraron {len(tracks)}"
        )

    for track in tracks:
        track_id = str(track.get("id", "")).strip() or "ruta-sin-id"
        subject_ids = track.get("subjects", [])
        missing = sorted(set(subject_ids) - set(subjects))
        if missing:
            errors.append(f"{track_id}: asignaturas inexistentes: {', '.join(missing)}")
        if len(subject_ids) != len(set(subject_ids)):
            errors.append(f"{track_id}: contiene asignaturas duplicadas")
        represented_areas = {
            subjects[item]["area_id"]
            for item in subject_ids
            if item in subjects and subjects[item]["area_id"]
        }
        if len(represented_areas) < 2:
            errors.append(f"{track_id}: no es interdisciplinaria")
        if len(subject_ids) < MIN_SUBJECTS_PER_TRACK:
            errors.append(f"{track_id}: ruta insuficientemente definida")
        for field in ("title", "description"):
            if not str(track.get(field, "")).strip():
                errors.append(f"{track_id}: falta {field}")

    catalog_path = ROOT / "catalogo" / "index.html"
    if not catalog_path.exists():
        errors.append("falta catalogo/index.html")
    else:
        text = catalog_path.read_text(encoding="utf-8")
        found = set(re.findall(r'data-subject="([^"]+)"', text))
        if found != set(core_subjects):
            errors.append(
                f"catálogo estático desincronizado: {len(found)} tarjetas para {len(core_subjects)} asignaturas centrales"
            )
        for marker in ("data-course-search", "data-area-filter", "data-track-filter", "data-result-count"):
            if marker not in text:
                errors.append(f"catálogo sin control {marker}")

    for area in areas:
        path = ROOT / area["path"]
        text = path.read_text(encoding="utf-8")
        expected = {subject["id"] for subject in area.get("subjects", [])}
        found = set(re.findall(r'data-subject="([^"]+)"', text))
        if found != expected:
            errors.append(f"{area['id']}: catálogo de área desincronizado")
        for marker in ("data-course-search", "data-track-filter", "data-result-count"):
            if marker not in text:
                errors.append(f"{area['id']}: falta {marker}")

    catalog_script = ROOT / "assets" / "js" / "catalog.js"
    required_files = (
        catalog_script,
        ROOT / "assets" / "css" / "catalog.css",
        ROOT / "templates" / "catalogo.html",
    )
    for required in required_files:
        if not required.exists():
            errors.append(f"falta {required.relative_to(ROOT)}")

    if catalog_script.exists():
        script_text = catalog_script.read_text(encoding="utf-8")
        for marker in ("provisional_subjects.json", "tracks.json", "catalog_statuses.json"):
            if marker not in script_text:
                errors.append(f"assets/js/catalog.js no integra {marker}")

    if errors:
        print("Errores de navegación del catálogo:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Catálogo validado.")
    print(f"- {len(core_subjects)} asignaturas centrales")
    print(f"- {len(provisional_subjects)} asignaturas provisionales")
    print(f"- {len(subjects)} asignaturas catalogadas")
    print(f"- {len(statuses['developed'])} con material lectivo desarrollado")
    print(f"- {len(statuses['pending'])} dependientes de unidades de respaldo")
    print(f"- {len(statuses['complete'])} con revisión disciplinar documentada")
    print(f"- {len(areas)} áreas")
    print(f"- {len(tracks)} rutas interdisciplinarias")
    print("- búsqueda, filtros, estados y relaciones sincronizados con sus fuentes curriculares")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
