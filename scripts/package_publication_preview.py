#!/usr/bin/env python3
"""Empaqueta los artefactos derivados que cambió una publicación curricular.

El workflow publica todos los paquetes reconstruidos para comprobar coherencia
global, pero una rama de PR solo debe versionar el diff derivado real. Este
script cruza el manifiesto con ``git status`` y empaqueta exclusivamente archivos
nuevos o modificados, además de registrar eliminaciones esperadas.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Iterable

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


def files_under(relative: Path) -> list[Path]:
    source = ROOT / relative
    if not source.is_dir():
        raise FileNotFoundError(f"Falta directorio generado: {relative.as_posix()}")
    return sorted(path.relative_to(ROOT) for path in source.rglob("*") if path.is_file())


def candidate_files(manifest: dict[str, Any]) -> set[Path]:
    candidates = {
        Path("data/catalog_statuses.json"),
        Path("data/citonauta_curriculum.json"),
        Path("data/course_outlines.json"),
        Path("data/provisional_subjects.json"),
        Path("catalogo/index.html"),
    }
    area_ids: set[str] = set()
    for raw_course in manifest["courses"]:
        if not isinstance(raw_course, dict):
            raise ValueError("Cada entrada courses debe ser un objeto")
        subject_id = str(raw_course.get("subject_id", "")).strip()
        area_id = str(raw_course.get("area_id", "")).strip()
        if not subject_id or not area_id:
            raise ValueError(f"Entrada de curso inválida: {raw_course}")

        candidates.add(relative_path(raw_course.get("overlay_path"), "overlay_path", subject_id))
        candidates.add(
            relative_path(
                raw_course.get("generated_course_path"),
                "generated_course_path",
                subject_id,
            )
        )
        candidates.update(
            files_under(
                relative_path(
                    raw_course.get("generated_units_path"),
                    "generated_units_path",
                    subject_id,
                )
            )
        )
        candidates.update(
            files_under(relative_path(raw_course.get("public_path"), "public_path", subject_id))
        )
        area_ids.add(area_id)

    candidates.update(Path(area_id) / "index.html" for area_id in area_ids)
    return candidates


def git_changes() -> tuple[set[Path], set[Path]]:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    changed: set[Path] = set()
    deleted: set[Path] = set()
    records = result.stdout.split(b"\0")
    index = 0
    while index < len(records):
        raw = records[index]
        index += 1
        if not raw:
            continue
        text = raw.decode("utf-8")
        status = text[:2]
        path_text = text[3:]
        if "R" in status or "C" in status:
            if index >= len(records) or not records[index]:
                raise ValueError(f"Registro git incompleto para {text}")
            path_text = records[index].decode("utf-8")
            index += 1
        path = Path(path_text)
        if "D" in status:
            deleted.add(path)
        else:
            changed.add(path)
    return changed, deleted


def copy_files(paths: Iterable[Path], output: Path) -> None:
    for relative in sorted(paths):
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(f"Falta artefacto generado: {relative.as_posix()}")
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def package(manifest: dict[str, Any], output: Path, include_all: bool) -> dict[str, Any]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    candidates = candidate_files(manifest)
    changed, deleted = git_changes()
    included = candidates if include_all else candidates & changed
    removed = candidates & deleted
    copy_files(included, output)

    report = {
        "schema_version": "1.0",
        "subjects": sorted(
            str(course.get("subject_id", ""))
            for course in manifest["courses"]
            if isinstance(course, dict)
        ),
        "included_paths": [path.as_posix() for path in sorted(included)],
        "deleted_paths": [path.as_posix() for path in sorted(removed)],
    }
    (output / "publication-preview-changes.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output / "publication-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Empaqueta el diff derivado de una publicación curricular."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--all-artifacts",
        action="store_true",
        help="Incluye todos los artefactos del manifiesto, no solo el diff de git.",
    )
    args = parser.parse_args()

    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    output = args.output if args.output.is_absolute() else ROOT / args.output
    report = package(load_manifest(manifest_path), output, args.all_artifacts)
    print(
        "Vista previa empaquetada: "
        f"{len(report['included_paths'])} modificados · "
        f"{len(report['deleted_paths'])} eliminados"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
