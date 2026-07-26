#!/usr/bin/env python3
"""Audit actual course development beyond catalog presence.

A course is fully developed only when every expected unit has either validated
advanced JSON or an explicitly authored public lesson. Merely having a course
page or a fallback-generated lesson does not count as full development.
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

import generate_site  # noqa: E402

ADVANCED_ROOT = ROOT / "data" / "generated_units"
AUTHORED_OVERRIDES = ROOT / "data" / "authored_unit_overrides.json"
GENERATED_MARKER = 'data-generated="citonauta-unit"'
AUTHORED_MARKER = 'data-authored-unit="true"'


def load_authored_overrides() -> set[tuple[str, int]]:
    if not AUTHORED_OVERRIDES.exists():
        return set()
    data = json.loads(AUTHORED_OVERRIDES.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        items = data.get("overrides", [])
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError("authored_unit_overrides.json debe contener un objeto o una lista")
    keys: set[tuple[str, int]] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        subject_id = str(item.get("subject_id") or "").strip()
        unit = int(item.get("unit") or 0)
        if subject_id and unit > 0:
            keys.add((subject_id, unit))
    return keys


def classify_unit(
    area_id: str,
    subject_id: str,
    unit_number: int,
    authored_overrides: set[tuple[str, int]],
) -> str:
    advanced_path = ADVANCED_ROOT / subject_id / f"unit-{unit_number:02d}.json"
    page_path = ROOT / area_id / subject_id / "unidades" / f"unidad-{unit_number:02d}.html"
    if not page_path.exists():
        return "missing"
    page = page_path.read_text(encoding="utf-8", errors="ignore")
    if advanced_path.exists():
        return "advanced"
    if AUTHORED_MARKER in page or (subject_id, unit_number) in authored_overrides:
        return "authored"
    if GENERATED_MARKER not in page:
        return "authored"
    return "fallback"


def audit() -> dict[str, Any]:
    curriculum = generate_site.load_json(generate_site.DATA_PATH)
    authored_overrides = load_authored_overrides()
    courses: list[dict[str, Any]] = []

    for area in curriculum.get("areas", []):
        area_id = str(area["id"])
        for subject in area.get("subjects", []):
            course = generate_site.merge_subject_overlay(area, subject)
            subject_id = str(course["id"])
            units = course.get("detailed_units", [])
            counts = {"advanced": 0, "authored": 0, "fallback": 0, "missing": 0}
            for unit in units:
                classification = classify_unit(
                    area_id,
                    subject_id,
                    int(unit["unit"]),
                    authored_overrides,
                )
                counts[classification] += 1

            expected = len(units)
            developed = counts["advanced"] + counts["authored"]
            fully_developed = (
                expected > 0
                and counts["fallback"] == 0
                and counts["missing"] == 0
                and developed == expected
            )
            courses.append(
                {
                    "area_id": area_id,
                    "area_title": area.get("title", area_id),
                    "subject_id": subject_id,
                    "title": course.get("title", subject_id),
                    "status": course.get("status", "unknown"),
                    "expected_units": expected,
                    "advanced_units": counts["advanced"],
                    "authored_units": counts["authored"],
                    "fallback_units": counts["fallback"],
                    "missing_pages": counts["missing"],
                    "developed_units": developed,
                    "completion_ratio": round(developed / expected, 4) if expected else 0.0,
                    "has_generated_course": (
                        ROOT / "data" / "generated_courses" / f"{subject_id}.json"
                    ).exists(),
                    "has_subject_overlay": (
                        ROOT / "data" / "subjects" / area_id / f"{subject_id}.json"
                    ).exists(),
                    "fully_developed": fully_developed,
                }
            )

    courses.sort(
        key=lambda row: (
            row["fully_developed"],
            row["completion_ratio"],
            -row["fallback_units"],
            row["area_id"],
            row["subject_id"],
        )
    )
    summary = {
        "course_count": len(courses),
        "fully_developed_courses": sum(row["fully_developed"] for row in courses),
        "incomplete_courses": sum(not row["fully_developed"] for row in courses),
        "expected_units": sum(row["expected_units"] for row in courses),
        "advanced_units": sum(row["advanced_units"] for row in courses),
        "authored_units": sum(row["authored_units"] for row in courses),
        "fallback_units": sum(row["fallback_units"] for row in courses),
        "missing_pages": sum(row["missing_pages"] for row in courses),
    }
    return {"summary": summary, "courses": courses}


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Inventario real de desarrollo de asignaturas",
        "",
        "Una asignatura solo se considera completamente desarrollada cuando todas sus unidades "
        "son avanzadas o autorales; una página de catálogo o una lección de respaldo no es suficiente.",
        "",
        f"- Asignaturas inventariadas: {summary['course_count']}",
        f"- Asignaturas completamente desarrolladas: {summary['fully_developed_courses']}",
        f"- Asignaturas incompletas: {summary['incomplete_courses']}",
        f"- Unidades esperadas: {summary['expected_units']}",
        f"- Unidades avanzadas: {summary['advanced_units']}",
        f"- Unidades autorales: {summary['authored_units']}",
        f"- Unidades con renderer de respaldo: {summary['fallback_units']}",
        f"- Páginas ausentes: {summary['missing_pages']}",
        "",
        "| Área | Asignatura | Avanzadas | Autorales | Respaldo | Total | Desarrollo |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in report["courses"]:
        lines.append(
            f"| {row['area_id']} | {row['title']} (`{row['subject_id']}`) | "
            f"{row['advanced_units']} | {row['authored_units']} | "
            f"{row['fallback_units']} | {row['expected_units']} | "
            f"{row['completion_ratio']:.0%} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--require-course-count", type=int, default=84)
    parser.add_argument("--fail-on-missing-pages", action="store_true")
    args = parser.parse_args()

    report = audit()
    summary = report["summary"]
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(report), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    errors: list[str] = []
    if summary["course_count"] != args.require_course_count:
        errors.append(
            f"se esperaban {args.require_course_count} asignaturas y se encontraron "
            f"{summary['course_count']}"
        )
    if args.fail_on_missing_pages and summary["missing_pages"]:
        errors.append(f"hay {summary['missing_pages']} páginas de unidad ausentes")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
