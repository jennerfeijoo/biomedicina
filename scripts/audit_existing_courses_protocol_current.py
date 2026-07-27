#!/usr/bin/env python3
"""Run the protocol audit using redevelopment packages as academic canonical data.

The base audit inventories the public/generated repository state. This layer
recalculates any subject with ``data/course_redevelopment/<subject>`` from that
review package, while preserving public counts and treating publication
synchronization as a separate required artefact.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import audit_existing_courses_protocol as base

ROOT = Path(__file__).resolve().parents[1]
REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"


def load_unit_paths(subject_id: str) -> list[Path]:
    return sorted((REDEVELOPMENT_ROOT / subject_id / "units").glob("unit-*.json"))


def recalculate_redevelopment_row(row: dict[str, Any]) -> dict[str, Any]:
    subject_id = row["subject_id"]
    package = REDEVELOPMENT_ROOT / subject_id
    course_path = package / "course.json"
    unit_paths = load_unit_paths(subject_id)
    if not course_path.exists() or not unit_paths:
        return row

    technical_errors: list[str] = []
    try:
        course_data = base.load_json(course_path)
        if not isinstance(course_data, dict):
            raise ValueError("la raíz de course.json no es un objeto")
    except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        technical_errors.append(f"curso de reconstrucción inválido: {exc}")
        course_data = {}

    units: list[dict[str, Any]] = []
    for path in unit_paths:
        try:
            value = base.load_json(path)
            if not isinstance(value, dict):
                raise ValueError("la raíz no es un objeto")
            units.append(value)
        except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            technical_errors.append(f"{path.name}: {exc}")

    component_counts: Counter[str] = Counter()
    for unit_data in units:
        for component, present in base.unit_component_coverage(unit_data).items():
            component_counts[component] += int(present)
    denominator = len(units) * len(base.UNIT_COMPONENT_ALIASES)
    component_ratio = sum(component_counts.values()) / denominator if denominator else 0.0

    expected_units = len(unit_paths)
    public_expected = int(row["expected_units"])
    public_developed = int(row["developed_units"])
    public_sync = (
        public_expected == expected_units
        and public_developed == expected_units
        and int(row["missing_public_pages"]) == 0
    )

    evaluation = base.assess_evaluation(course_data, units)
    artefacts = dict(row["protocol_artefacts"])
    artefacts.update(
        {
            "course_profile": True,
            "unit_program": expected_units > 0,
            "units": len(units) == expected_units > 0,
            "practices_evaluations": evaluation["assessment_plan"]
            and base.key_present(units, {"guided_activity", "guided_activities", "practice_sets"}),
            "mastery_criteria": evaluation["achievement_criteria"],
            "public_page_sync": public_sync,
        }
    )
    missing_protocol = [name for name, present in artefacts.items() if not present]
    declared_status = str(course_data.get("status") or row["declared_status"])
    review_path = base.find_review_artifact(subject_id)
    mismatches = base.status_mismatch(declared_status, review_path, missing_protocol)
    if not public_sync:
        mismatches.append(
            f"paquete de reconstrucción con {expected_units} unidades no sincronizado con publicación de {public_expected}"
        )

    updated = dict(row)
    updated.update(
        {
            "declared_status": declared_status,
            "audit_band": base.classify_band(
                expected_units=expected_units,
                developed_units=len(units),
                missing_protocol=missing_protocol,
                component_ratio=component_ratio,
                review_artifact=review_path,
                technical_errors=technical_errors,
            ),
            "expected_units": expected_units,
            "developed_units": len(units),
            "protocol_artefacts": artefacts,
            "missing_protocol_artefacts": missing_protocol,
            "course_scope_coverage": base.course_scope_coverage(course_data),
            "unit_component_coverage": dict(component_counts),
            "unit_component_ratio": round(component_ratio, 4),
            "evaluation_coverage": evaluation,
            "technical_errors": technical_errors,
            "status_mismatches": mismatches,
            "academic_source": "redevelopment_package",
            "public_state": {
                "catalog_units": public_expected,
                "developed_public_units": public_developed,
                "missing_public_pages": row["missing_public_pages"],
                "synchronized": public_sync,
            },
            "paths": {
                **row["paths"],
                "course": str(course_path.relative_to(ROOT)),
            },
        }
    )
    return updated


def rebuild_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    band_counts = Counter(row["audit_band"] for row in rows)
    declared_counts = Counter(row["declared_status"] for row in rows)
    missing_counts = Counter(
        artefact
        for row in rows
        for artefact in row["missing_protocol_artefacts"]
    )
    return {
        "course_count": len(rows),
        "band_counts": dict(sorted(band_counts.items())),
        "declared_status_counts": dict(sorted(declared_counts.items())),
        "courses_with_technical_errors": sum(bool(row["technical_errors"]) for row in rows),
        "courses_with_status_mismatches": sum(bool(row["status_mismatches"]) for row in rows),
        "courses_with_all_units_developed": sum(row["developed_units"] == row["expected_units"] > 0 for row in rows),
        "courses_protocol_complete": sum(not row["missing_protocol_artefacts"] for row in rows),
        "redevelopment_packages_used": sum(row.get("academic_source") == "redevelopment_package" for row in rows),
        "missing_artefact_counts": dict(sorted(missing_counts.items(), key=lambda item: (-item[1], item[0]))),
        "disclaimer": "El informe prioriza paquetes de reconstrucción como evidencia académica y evalúa la publicación por separado; no certifica suficiencia disciplinar ni revisión humana.",
    }


def audit() -> dict[str, Any]:
    report = base.audit()
    rows = [recalculate_redevelopment_row(row) for row in report["courses"]]
    rows.sort(
        key=lambda row: (
            row["audit_band"] not in {"technical_failure", "content_present_protocol_incomplete", "architecture_incomplete"},
            -row["developed_units"],
            row["area_id"],
            row["subject_id"],
        )
    )
    return {"summary": rebuild_summary(rows), "courses": rows}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--require-course-count", type=int, default=84)
    parser.add_argument("--fail-on-technical-errors", action="store_true")
    args = parser.parse_args()

    report = audit()
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(base.render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))

    errors: list[str] = []
    if report["summary"]["course_count"] != args.require_course_count:
        errors.append(f"se esperaban {args.require_course_count} asignaturas")
    if args.fail_on_technical_errors and report["summary"]["courses_with_technical_errors"]:
        errors.append("existen asignaturas con errores técnicos")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
