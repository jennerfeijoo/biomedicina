#!/usr/bin/env python3
"""Empaqueta los artefactos derivados de una publicación curricular.

El paquete conserva únicamente archivos que el workflow puede regenerar desde
el manifiesto. Sirve para revisar y versionar en una rama de PR exactamente el
mismo contenido que validó el publicador en su workspace temporal.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "publication-manifest.json"
DEFAULT_OUTPUT = ROOT / "publication-preview"


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("courses"), list):
        raise ValueError("El manifiesto debe contener una lista courses")
    return data


def relative_path(raw: Any, field: str, subject_id: str) -> Path:
    value = Path(str(raw or "").strip())
    if not str(value) or value.is_absolute() or ".." in value.parts:
        raise ValueError(f"{subject_id}: ruta inválida en {field}: {raw}")
    return value


def copy_file(relative: Path, output: Path) -> None:
    source = ROOT / relative
    if not source.is_file():
        raise FileNotFoundError(f"Falta artefacto generado: {relative.as_posix()}")
    target = output / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_directory(relative: Path, output: Path) -> None:
    source = ROOT / relative
    if not source.is_dir():
        raise FileNotFoundError(f"Falta directorio generado: {relative.as_posix()}")
    shutil.copytree(source, output / relative, dirs_exist_ok=True)


def package(manifest: dict[str, Any], output: Path) -> list[str]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    common_files = (
        Path("data/catalog_statuses.json"),
        Path("data/citonauta_curriculum.json"),
        Path("data/course_outlines.json"),
        Path("data/provisional_subjects.json"),
        Path("catalogo/index.html"),
    )
    for relative in common_files:
        copy_file(relative, output)

    packaged_subjects: list[str] = []
    area_ids: set[str] = set()
    for raw_course in manifest["courses"]:
        if not isinstance(raw_course, dict):
            raise ValueError("Cada entrada courses debe ser un objeto")
        subject_id = str(raw_course.get("subject_id", "")).strip()
        area_id = str(raw_course.get("area_id", "")).strip()
        if not subject_id or not area_id:
            raise ValueError(f"Entrada de curso inválida: {raw_course}")

        overlay_path = relative_path(raw_course.get("overlay_path"), "overlay_path", subject_id)
        generated_course_path = relative_path(
            raw_course.get("generated_course_path"), "generated_course_path", subject_id
        )
        generated_units_path = relative_path(
            raw_course.get("generated_units_path"), "generated_units_path", subject_id
        )
        public_path = relative_path(raw_course.get("public_path"), "public_path", subject_id)

        copy_file(overlay_path, output)
        copy_file(generated_course_path, output)
        copy_directory(generated_units_path, output)
        copy_directory(public_path, output)
        area_ids.add(area_id)
        packaged_subjects.append(subject_id)

    for area_id in sorted(area_ids):
        copy_file(Path(area_id) / "index.html", output)

    manifest_target = output / "publication-manifest.json"
    manifest_target.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return sorted(packaged_subjects)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Empaqueta los artefactos derivados de una publicación curricular."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    output = args.output if args.output.is_absolute() else ROOT / args.output
    subjects = package(load_manifest(manifest_path), output)
    print("Vista previa empaquetada: " + ", ".join(subjects))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
