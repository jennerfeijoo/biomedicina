#!/usr/bin/env python3
"""Compare redevelopment packages with catalog, generated data and public pages.

The audit reports count-level publication consistency. Matching counts do not
prove semantic synchronization, while mismatched counts are a definite signal
that the reviewed package has not been migrated to the public course.
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

REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"
GENERATED_COURSES = ROOT / "data" / "generated_courses"
GENERATED_UNITS = ROOT / "data" / "generated_units"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: la raíz debe ser un objeto JSON")
    return data


def curriculum_index() -> dict[str, dict[str, Any]]:
    curriculum = generate_site.load_json(generate_site.DATA_PATH)
    output: dict[str, dict[str, Any]] = {}
    for area in curriculum.get("areas", []):
        for subject in area.get("subjects", []):
            merged = generate_site.merge_subject_overlay(area, subject)
            output[str(merged["id"])] = {
                "area_id": str(area["id"]),
                "course": merged,
            }
    return output


def audit() -> dict[str, Any]:
    index = curriculum_index()
    rows: list[dict[str, Any]] = []
    technical_errors: list[str] = []

    if not REDEVELOPMENT_ROOT.exists():
        return {
            "summary": {
                "packages": 0,
                "count_aligned": 0,
                "migration_pending": 0,
                "technical_errors": 0,
            },
            "packages": [],
            "technical_errors": [],
        }

    for package in sorted(path for path in REDEVELOPMENT_ROOT.iterdir() if path.is_dir()):
        course_path = package / "course.json"
        if not course_path.exists():
            technical_errors.append(f"{package.relative_to(ROOT)}: falta course.json")
            continue
        try:
            course = load_json(course_path)
        except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            technical_errors.append(str(exc))
            continue

        subject_id = str(course.get("subject_id") or package.name)
        area_id = str(course.get("area_id") or index.get(subject_id, {}).get("area_id") or "")
        redevelopment_units = sorted((package / "units").glob("unit-*.json"))
        redevelopment_count = len(redevelopment_units)

        catalog = index.get(subject_id)
        catalog_count = len(catalog["course"].get("detailed_units", [])) if catalog else 0
        generated_course_path = GENERATED_COURSES / f"{subject_id}.json"
        generated_course_count = 0
        if generated_course_path.exists():
            try:
                generated_course = load_json(generated_course_path)
                generated_course_count = len(
                    generated_course.get("units")
                    or generated_course.get("unit_program")
                    or generated_course.get("detailed_units")
                    or []
                )
            except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                technical_errors.append(str(exc))

        generated_unit_count = len(list((GENERATED_UNITS / subject_id).glob("unit-*.json")))
        public_unit_dir = ROOT / area_id / subject_id / "unidades"
        public_unit_count = len(list(public_unit_dir.glob("unidad-*.html"))) if public_unit_dir.exists() else 0
        public_course_exists = (ROOT / area_id / subject_id / "index.html").exists() if area_id else False

        counts = {
            "redevelopment_units": redevelopment_count,
            "catalog_units": catalog_count,
            "generated_course_units": generated_course_count,
            "generated_unit_json": generated_unit_count,
            "public_unit_pages": public_unit_count,
        }
        public_counts = [catalog_count, generated_unit_count, public_unit_count]
        count_aligned = redevelopment_count > 0 and all(value == redevelopment_count for value in public_counts)
        issues: list[str] = []
        if catalog is None:
            issues.append("el paquete no corresponde a una asignatura del catálogo")
        if redevelopment_count == 0:
            issues.append("el paquete no contiene unidades")
        if catalog_count != redevelopment_count:
            issues.append(f"catálogo {catalog_count} ≠ reconstrucción {redevelopment_count}")
        if generated_unit_count != redevelopment_count:
            issues.append(f"JSON públicos {generated_unit_count} ≠ reconstrucción {redevelopment_count}")
        if public_unit_count != redevelopment_count:
            issues.append(f"páginas públicas {public_unit_count} ≠ reconstrucción {redevelopment_count}")
        if not public_course_exists:
            issues.append("falta página pública de asignatura")
        if generated_course_count and generated_course_count != redevelopment_count:
            issues.append(f"arquitectura generada {generated_course_count} ≠ reconstrucción {redevelopment_count}")

        rows.append(
            {
                "subject_id": subject_id,
                "area_id": area_id,
                "package_status": course.get("status", "unknown"),
                "counts": counts,
                "count_aligned": count_aligned,
                "migration_state": "count_aligned_semantic_review_required" if count_aligned else "migration_pending",
                "issues": issues,
                "course_path": str(course_path.relative_to(ROOT)),
            }
        )

    summary = {
        "packages": len(rows),
        "count_aligned": sum(row["count_aligned"] for row in rows),
        "migration_pending": sum(not row["count_aligned"] for row in rows),
        "technical_errors": len(technical_errors),
        "disclaimer": "La igualdad de recuentos no demuestra equivalencia semántica; una diferencia confirma migración pendiente.",
    }
    return {"summary": summary, "packages": rows, "technical_errors": technical_errors}


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Sincronización entre reconstrucción y publicación",
        "",
        summary["disclaimer"],
        "",
        f"- Paquetes de reconstrucción: {summary['packages']}",
        f"- Recuentos alineados: {summary['count_aligned']}",
        f"- Migraciones pendientes: {summary['migration_pending']}",
        f"- Errores técnicos: {summary['technical_errors']}",
        "",
        "| Asignatura | Estado del paquete | Reconstrucción | Catálogo | JSON públicos | Páginas públicas | Estado | Problemas |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in report["packages"]:
        counts = row["counts"]
        issues = "; ".join(row["issues"]) or "—"
        lines.append(
            f"| `{row['subject_id']}` | {row['package_status']} | "
            f"{counts['redevelopment_units']} | {counts['catalog_units']} | "
            f"{counts['generated_unit_json']} | {counts['public_unit_pages']} | "
            f"`{row['migration_state']}` | {issues} |"
        )
    if report["technical_errors"]:
        lines.extend(["", "## Errores técnicos", ""])
        lines.extend(f"- {error}" for error in report["technical_errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--fail-on-technical-errors", action="store_true")
    args = parser.parse_args()

    report = audit()
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    if args.fail_on_technical_errors and report["summary"]["technical_errors"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
