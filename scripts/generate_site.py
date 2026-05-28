#!/usr/bin/env python3
"""Generador estático para páginas de asignatura de CitoNauta.

El script lee data/citonauta_curriculum.json y usa templates/asignatura.html
para generar páginas HTML de asignaturas. Por defecto funciona en modo seguro:
no sobrescribe archivos existentes salvo que se use --force.

También puede enriquecer asignaturas con archivos opcionales en:

data/subjects/<area_id>/<subject_id>.json
"""

from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "citonauta_curriculum.json"
TEMPLATE_PATH = ROOT / "templates" / "asignatura.html"
SUBJECT_DATA_DIR = ROOT / "data" / "subjects"
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
    "learning_objectives",
    "modules",
    "key_concepts",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo de datos: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"No existe la plantilla: {path}")
    return path.read_text(encoding="utf-8")


def escape(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def rel_path(from_file: Path, to_file: Path) -> str:
    """Devuelve una ruta relativa POSIX desde un HTML generado hacia otro archivo."""
    start_dir = from_file.parent
    return Path(os.path.relpath(to_file, start=start_dir)).as_posix()


def render_list(items: list[str], empty_message: str) -> str:
    if not items:
        return f'<p class="muted">{escape(empty_message)}</p>'
    rendered = "\n".join(f"        <li>{escape(item)}</li>" for item in items)
    return f"<ul>\n{rendered}\n      </ul>"


def subject_neighbors(subjects: list[dict[str, Any]], index: int) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    previous_subject = subjects[index - 1] if index > 0 else None
    next_subject = subjects[index + 1] if index < len(subjects) - 1 else None
    return previous_subject, next_subject


def render_nav_link(current_file: Path, subject: dict[str, Any] | None, label_prefix: str, css_class: str) -> str:
    if subject is None:
        return ""
    target = ROOT / subject["path"]
    href = rel_path(current_file, target)
    title = escape(subject.get("title", subject.get("id", "Asignatura")))
    css_classes = f"btn-link {css_class}".strip()
    label = f"{label_prefix} {title}".strip()
    return f'<a class="{css_classes}" href="{href}">{label}</a>'


def validate_template(template: str) -> None:
    missing = [key for key in REQUIRED_TEMPLATE_KEYS if "{{ " + key + " }}" not in template]
    if missing:
        raise ValueError("La plantilla no contiene estas variables requeridas: " + ", ".join(sorted(missing)))


def subject_overlay_path(area_id: str, subject_id: str) -> Path:
    return SUBJECT_DATA_DIR / area_id / f"{subject_id}.json"


def merge_subject_overlay(area: dict[str, Any], subject: dict[str, Any]) -> dict[str, Any]:
    """Combina metadatos centrales con contenido editorial opcional por asignatura."""
    merged = dict(subject)
    overlay_path = subject_overlay_path(area["id"], subject["id"])
    if not overlay_path.exists():
        return merged

    overlay = load_json(overlay_path)
    if overlay.get("id") != subject["id"]:
        raise ValueError(f"Overlay con id inconsistente en {overlay_path.relative_to(ROOT)}")
    if overlay.get("area_id") != area["id"]:
        raise ValueError(f"Overlay con area_id inconsistente en {overlay_path.relative_to(ROOT)}")

    for key, value in overlay.items():
        if key not in {"id", "area_id"}:
            merged[key] = value
    return merged


def render_subject(template: str, area: dict[str, Any], subject: dict[str, Any], subjects: list[dict[str, Any]], index: int) -> str:
    subject = merge_subject_overlay(area, subject)
    output_path = ROOT / subject["path"]
    home_path = rel_path(output_path, ROOT / "index.html")
    area_path = rel_path(output_path, ROOT / area["path"])
    css_path = rel_path(output_path, ROOT / "assets" / "css" / "style.css")
    editorial_css_path = rel_path(output_path, ROOT / "assets" / "css" / "editorial.css")
    previous_subject, next_subject = subject_neighbors(subjects, index)

    replacements = {
        "subject_title": escape(subject.get("title", subject.get("id", "Asignatura"))),
        "area_title": escape(area.get("title", area.get("id", "Área"))),
        "subject_description": escape(subject.get("description", "Página de asignatura de CitoNauta Biomedicina.")),
        "css_path": css_path,
        "editorial_css_path": editorial_css_path,
        "home_path": home_path,
        "area_path": area_path,
        "previous_link": render_nav_link(output_path, previous_subject, "←", "secondary"),
        "next_link": render_nav_link(output_path, next_subject, "", ""),
        "biomedical_connection": escape(subject.get("biomedical_connection", "Conexión biomédica pendiente de desarrollo.")),
        "learning_objectives": render_list(subject.get("learning_objectives", []), "Objetivos de aprendizaje pendientes de desarrollo."),
        "modules": render_list(subject.get("modules", []), "Módulos pendientes de desarrollo."),
        "key_concepts": render_list(subject.get("key_concepts", []), "Conceptos clave pendientes de desarrollo."),
    }

    html_output = template
    for key, value in replacements.items():
        html_output = html_output.replace("{{ " + key + " }}", value)
    return html_output


def iter_subjects(data: dict[str, Any]):
    for area in data.get("areas", []):
        subjects = area.get("subjects", [])
        for index, subject in enumerate(subjects):
            yield area, subjects, index, subject


def should_include_subject(subject: dict[str, Any], only_subjects: set[str]) -> bool:
    if not only_subjects:
        return True
    return subject.get("id") in only_subjects or subject.get("path") in only_subjects


def generate(dry_run: bool, force: bool, only_missing: bool, only_subjects: set[str]) -> dict[str, int]:
    data = load_json(DATA_PATH)
    template = load_template(TEMPLATE_PATH)
    validate_template(template)
    summary = {"generated": 0, "skipped_existing": 0, "skipped_filter": 0, "would_generate": 0, "errors": 0}

    for area, subjects, index, subject in iter_subjects(data):
        if not should_include_subject(subject, only_subjects):
            summary["skipped_filter"] += 1
            continue

        target_path = ROOT / subject["path"]
        exists = target_path.exists()

        if exists and only_missing:
            summary["skipped_existing"] += 1
            continue
        if exists and not force:
            summary["skipped_existing"] += 1
            continue

        rendered = render_subject(template, area, subject, subjects, index)

        if dry_run:
            print(f"[dry-run] generaría: {target_path.relative_to(ROOT)}")
            summary["would_generate"] += 1
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"[ok] generado: {target_path.relative_to(ROOT)}")
        summary["generated"] += 1

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera páginas HTML de asignaturas para CitoNauta.")
    parser.add_argument("--dry-run", action="store_true", help="Muestra qué se generaría sin escribir archivos.")
    parser.add_argument("--force", action="store_true", help="Sobrescribe páginas existentes. Usar solo con revisión previa.")
    parser.add_argument("--only-missing", action="store_true", help="Genera solo páginas que no existan.")
    parser.add_argument("--subject", action="append", default=[], help="Genera solo una asignatura por id o ruta. Puede repetirse.")
    args = parser.parse_args()

    summary = generate(
        dry_run=args.dry_run,
        force=args.force,
        only_missing=args.only_missing,
        only_subjects=set(args.subject),
    )
    print("\nResumen:")
    for key, value in summary.items():
        print(f"- {key}: {value}")

    if not args.force:
        print("\nModo seguro activo: las páginas existentes no se sobrescriben sin --force.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
