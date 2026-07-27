#!/usr/bin/env python3
"""Audita paquetes reconstruidos y asignaturas con contenido desarrollado.

La auditoría combina dos inventarios:

1. paquetes de ``data/course_redevelopment`` y su sincronización pública;
2. cursos del catálogo que poseen unidades avanzadas o autorales reales.

No equipara integridad técnica con madurez académica. Un curso puede estar
publicado y seguir en estado ``review`` hasta completar revisión disciplinar.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_course_completion  # noqa: E402
import publish_courses  # noqa: E402


def artifact_presence(package: publish_courses.CoursePackage) -> dict[str, bool]:
    source = package.source_dir
    return {
        "source_registry": (ROOT / "data" / "source_registry" / f"{package.subject_id}.json").exists(),
        "curriculum_decision": (ROOT / "data" / "curriculum_decisions" / f"{package.subject_id}.json").exists(),
        "scope_or_coverage": any(
            path.exists()
            for path in (
                source / "SCOPE_RESOLUTIONS.md",
                source / "CURRICULUM_ALIGNMENT_MATRIX.md",
                ROOT / "data" / "curriculum_coverage" / f"{package.subject_id}.json",
            )
        ),
        "curriculum_audit": any(source.glob("CURRICULUM_AUDIT*.md")),
        "bibliography_audit": any(source.glob("BIBLIOGRAPHY_AUDIT*.md")),
        "review_readiness": (source / "REVIEW_READINESS.md").exists(),
        "assessment_rubrics": (source / "ASSESSMENT_RUBRICS.md").exists(),
    }


def audit_redevelopment_packages() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_dir in publish_courses.source_directories():
        subject_hint = source_dir.name
        try:
            package = publish_courses.load_package(source_dir)
            promotion_errors = publish_courses.promotion_errors(package)
            public_errors = publish_courses.public_page_errors(package)
            artifacts = artifact_presence(package)
            published = not promotion_errors and not public_errors
            rows.append(
                {
                    "subject_id": package.subject_id,
                    "title": package.course.get("title", package.subject_id),
                    "area_id": package.area_id,
                    "editorial_status": package.course.get("status", "unknown"),
                    "unit_count": len(package.units),
                    "source_valid": True,
                    "promotion_synchronized": not promotion_errors,
                    "public_pages_synchronized": not public_errors,
                    "published": published,
                    "promotion_errors": promotion_errors,
                    "public_errors": public_errors,
                    "artifacts": artifacts,
                    "artifact_coverage": round(sum(artifacts.values()) / len(artifacts), 4),
                    "academic_review_complete": package.course.get("status") == "complete",
                }
            )
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as error:
            rows.append(
                {
                    "subject_id": subject_hint,
                    "title": subject_hint,
                    "area_id": "unknown",
                    "editorial_status": "invalid",
                    "unit_count": 0,
                    "source_valid": False,
                    "promotion_synchronized": False,
                    "public_pages_synchronized": False,
                    "published": False,
                    "promotion_errors": [str(error)],
                    "public_errors": [],
                    "artifacts": {},
                    "artifact_coverage": 0.0,
                    "academic_review_complete": False,
                }
            )
    return rows


def audit_catalog_developed_courses() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    completion = audit_course_completion.audit()
    developed = [
        row
        for row in completion["courses"]
        if row["developed_units"] > 0 or row["fully_developed"]
    ]
    developed.sort(
        key=lambda row: (
            not row["fully_developed"],
            -row["completion_ratio"],
            row["area_id"],
            row["subject_id"],
        )
    )
    summary = {
        "catalog_course_count": completion["summary"]["course_count"],
        "courses_with_developed_content": len(developed),
        "fully_developed_courses": sum(row["fully_developed"] for row in developed),
        "partially_developed_courses": sum(not row["fully_developed"] for row in developed),
        "developed_units": sum(row["developed_units"] for row in developed),
        "advanced_units": sum(row["advanced_units"] for row in developed),
        "authored_units": sum(row["authored_units"] for row in developed),
        "fallback_units_inside_developed_courses": sum(row["fallback_units"] for row in developed),
        "missing_pages_inside_developed_courses": sum(row["missing_pages"] for row in developed),
    }
    return summary, developed


def build_report() -> dict[str, Any]:
    packages = audit_redevelopment_packages()
    catalog_summary, developed_courses = audit_catalog_developed_courses()
    package_summary = {
        "package_count": len(packages),
        "valid_packages": sum(row["source_valid"] for row in packages),
        "published_packages": sum(row["published"] for row in packages),
        "stale_or_unpublished_packages": sum(not row["published"] for row in packages),
        "academic_review_complete": sum(row["academic_review_complete"] for row in packages),
        "academic_review_pending": sum(not row["academic_review_complete"] for row in packages),
    }
    return {
        "schema_version": "1.0",
        "summary": {**package_summary, **catalog_summary},
        "redevelopment_packages": packages,
        "developed_courses": developed_courses,
        "interpretation": {
            "fully_developed": "Todas las unidades son avanzadas o autorales y no existen páginas fallback o ausentes.",
            "published_package": "La fuente reconstruida, las capas JSON y todas las páginas HTML están sincronizadas.",
            "academic_review_complete": "Solo es verdadero cuando el estado editorial documentado es complete.",
        },
    }


def yes_no(value: bool) -> str:
    return "sí" if value else "no"


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Auditoría de asignaturas desarrolladas",
        "",
        "Esta auditoría separa publicación técnica, desarrollo lectivo y revisión académica.",
        "",
        "## Resumen",
        "",
        f"- Paquetes reconstruidos: {summary['package_count']}",
        f"- Paquetes publicados y sincronizados: {summary['published_packages']}",
        f"- Paquetes sin publicar o desincronizados: {summary['stale_or_unpublished_packages']}",
        f"- Paquetes con revisión académica completa: {summary['academic_review_complete']}",
        f"- Asignaturas del catálogo con contenido desarrollado: {summary['courses_with_developed_content']}",
        f"- Asignaturas completamente desarrolladas: {summary['fully_developed_courses']}",
        f"- Asignaturas parcialmente desarrolladas: {summary['partially_developed_courses']}",
        f"- Unidades avanzadas: {summary['advanced_units']}",
        f"- Unidades autorales: {summary['authored_units']}",
        f"- Unidades fallback dentro de cursos desarrollados: {summary['fallback_units_inside_developed_courses']}",
        f"- Páginas ausentes dentro de cursos desarrollados: {summary['missing_pages_inside_developed_courses']}",
        "",
        "## Paquetes reconstruidos",
        "",
        "| Asignatura | Estado | Unidades | Fuente válida | JSON sincronizado | HTML sincronizado | Revisión completa |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in report["redevelopment_packages"]:
        lines.append(
            f"| {row['title']} (`{row['subject_id']}`) | {row['editorial_status']} | "
            f"{row['unit_count']} | {yes_no(row['source_valid'])} | "
            f"{yes_no(row['promotion_synchronized'])} | {yes_no(row['public_pages_synchronized'])} | "
            f"{yes_no(row['academic_review_complete'])} |"
        )
        for error in [*row["promotion_errors"], *row["public_errors"]]:
            lines.append(f"  - **{row['subject_id']}**: {error}")

    lines.extend(
        [
            "",
            "## Asignaturas con contenido desarrollado",
            "",
            "| Área | Asignatura | Avanzadas | Autorales | Fallback | Ausentes | Total | Desarrollo completo |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in report["developed_courses"]:
        lines.append(
            f"| {row['area_id']} | {row['title']} (`{row['subject_id']}`) | "
            f"{row['advanced_units']} | {row['authored_units']} | {row['fallback_units']} | "
            f"{row['missing_pages']} | {row['expected_units']} | {yes_no(row['fully_developed'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretación",
            "",
            "- Una página generada o una asignatura catalogada no implica desarrollo académico completo.",
            "- Un paquete publicado puede permanecer en `review`; CI no puede promoverlo automáticamente a `complete`.",
            "- Los cursos parcialmente desarrollados requieren completar o reemplazar unidades fallback antes de declararse terminados.",
        ]
    )
    return "\n".join(lines) + "\n"


def strict_errors(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for row in report["redevelopment_packages"]:
        if not row["source_valid"]:
            errors.append(f"{row['subject_id']}: paquete fuente inválido")
        elif not row["published"]:
            errors.append(f"{row['subject_id']}: paquete no publicado o desincronizado")
    for row in report["developed_courses"]:
        if row["fully_developed"] and row["missing_pages"]:
            errors.append(f"{row['subject_id']}: curso desarrollado con páginas ausentes")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita asignaturas reconstruidas y contenido lectivo desarrollado.")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))

    errors = strict_errors(report) if args.strict else []
    for error in errors:
        print(f"ERROR: {error}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
