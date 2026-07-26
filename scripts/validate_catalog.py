#!/usr/bin/env python3
"""Validate generated catalog, filters, and interdisciplinary track integrity."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    curriculum = json.loads((ROOT / "data" / "citonauta_curriculum.json").read_text(encoding="utf-8"))
    tracks_data = json.loads((ROOT / "data" / "tracks.json").read_text(encoding="utf-8"))
    areas = curriculum.get("areas", [])
    subjects = {
        subject["id"]: (area["id"], subject)
        for area in areas
        for subject in area.get("subjects", [])
    }
    errors: list[str] = []

    tracks = tracks_data.get("tracks", [])
    track_ids = [track.get("id") for track in tracks]
    if len(track_ids) != len(set(track_ids)):
        errors.append("los identificadores de rutas no son únicos")
    if len(tracks) != 6:
        errors.append(f"se esperaban 6 rutas explícitas y se encontraron {len(tracks)}")

    for track in tracks:
        subject_ids = track.get("subjects", [])
        missing = sorted(set(subject_ids) - set(subjects))
        if missing:
            errors.append(f"{track.get('id')}: asignaturas inexistentes: {', '.join(missing)}")
        if len(subject_ids) != len(set(subject_ids)):
            errors.append(f"{track.get('id')}: contiene asignaturas duplicadas")
        represented_areas = {subjects[item][0] for item in subject_ids if item in subjects}
        if len(represented_areas) < 2:
            errors.append(f"{track.get('id')}: no es interdisciplinaria")
        if len(subject_ids) < 6:
            errors.append(f"{track.get('id')}: ruta insuficientemente definida")

    catalog_path = ROOT / "catalogo" / "index.html"
    if not catalog_path.exists():
        errors.append("falta catalogo/index.html")
    else:
        text = catalog_path.read_text(encoding="utf-8")
        found = set(re.findall(r'data-subject="([^"]+)"', text))
        if found != set(subjects):
            errors.append(
                f"catálogo desincronizado: {len(found)} tarjetas para {len(subjects)} asignaturas"
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

    for required in (
        ROOT / "assets" / "js" / "catalog.js",
        ROOT / "assets" / "css" / "catalog.css",
        ROOT / "templates" / "catalogo.html",
    ):
        if not required.exists():
            errors.append(f"falta {required.relative_to(ROOT)}")

    if errors:
        print("Errores de navegación del catálogo:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Catálogo validado.")
    print(f"- {len(subjects)} asignaturas")
    print(f"- {len(areas)} áreas")
    print(f"- {len(tracks)} rutas interdisciplinarias")
    print("- búsqueda y filtros sincronizados con la fuente curricular")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
