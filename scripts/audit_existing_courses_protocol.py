#!/usr/bin/env python3
"""Audit existing courses against the academic content development protocol.

This audit separates repository integrity from academic maturity. It inventories
required artefacts, unit architecture, evidence traceability, editorial status
and public synchronization. It does not promote any course to ``complete`` and
cannot replace disciplinary review.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_course_completion  # noqa: E402
import generate_site  # noqa: E402

DATA = ROOT / "data"
GENERATED_COURSES = DATA / "generated_courses"
GENERATED_UNITS = DATA / "generated_units"
SUBJECTS = DATA / "subjects"
SOURCE_REGISTRY = DATA / "source_registry"
CURRICULUM_DECISIONS = DATA / "curriculum_decisions"
CURRICULUM_COVERAGE = DATA / "curriculum_coverage"
COURSE_REDEVELOPMENT = DATA / "course_redevelopment"

COURSE_SCOPE_ALIASES = {
    "purpose": {"purpose", "course_purpose", "description"},
    "level_audience": {"level", "academic_level", "audience", "target_audience"},
    "prerequisites": {"prerequisites", "entry_competencies", "prior_knowledge"},
    "learning_outcomes": {"learning_outcomes", "course_outcomes"},
    "relationships": {"course_relationships", "related_courses", "curricular_connections"},
    "exclusions": {"exclusions", "out_of_scope", "scope_limits"},
    "biomedical_applications": {"biomedical_applications", "applications", "clinical_context"},
}

UNIT_COMPONENT_ALIASES = {
    "central_question": {"central_question", "guiding_question", "question"},
    "purpose": {"purpose"},
    "learning_objectives": {"learning_objectives"},
    "prior_knowledge": {"prior_knowledge", "prerequisites", "required_knowledge"},
    "concepts_mechanisms": {"theory_sections", "concepts", "mechanisms"},
    "mental_model": {"mental_model", "visual_model", "representation", "visualization"},
    "methods": {"methods", "study_methods", "experimental_methods", "computational_methods"},
    "evidence": {"evidence", "experimental_evidence", "computational_evidence", "worked_examples"},
    "guided_activity": {"guided_activity", "guided_activities"},
    "reproducible_practice": {"practice", "practice_sets", "reproducible_activity", "notebook"},
    "biomedical_example": {"biomedical_connections", "biomedical_example", "clinical_example"},
    "limitations_errors": {"limitations", "common_errors", "pitfalls"},
    "formative_assessment": {"self_assessment", "formative_assessment", "quiz"},
    "specific_references": {"sources", "references"},
}

REVIEW_NAMES = {
    "review_log.json",
    "review_registry.json",
    "review_readiness.md",
    "academic_review.md",
    "curriculum_audit.md",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def key_present(data: Any, aliases: set[str]) -> bool:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in aliases and nonempty(value):
                return True
            if key_present(value, aliases):
                return True
    elif isinstance(data, list):
        return any(key_present(item, aliases) for item in data)
    return False


def find_subject_artifact(root: Path, subject_id: str) -> Path | None:
    if not root.exists():
        return None
    direct_candidates = [
        root / f"{subject_id}.json",
        root / f"{subject_id}.md",
        root / subject_id / "index.json",
        root / subject_id / "README.md",
    ]
    for candidate in direct_candidates:
        if candidate.exists():
            return candidate
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md"}:
            continue
        if subject_id in path.stem or subject_id in path.parts:
            return path
        if path.suffix.lower() == ".json":
            try:
                data = load_json(path)
            except (OSError, json.JSONDecodeError, UnicodeDecodeError):
                continue
            serialized = json.dumps(data, ensure_ascii=False)
            if f'"{subject_id}"' in serialized:
                return path
    return None


def find_review_artifact(subject_id: str) -> Path | None:
    roots = [
        DATA / "course_reviews",
        DATA / "reviews",
        DATA / "review_registry",
        COURSE_REDEVELOPMENT / subject_id,
        ROOT / "docs" / "reviews",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            normalized = path.name.lower()
            if normalized in REVIEW_NAMES or "review" in normalized or "audit" in normalized:
                if subject_id in path.parts or subject_id in path.stem or root == COURSE_REDEVELOPMENT / subject_id:
                    return path
    return None


def load_optional_json(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, None
    try:
        data = load_json(path)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        return None, str(exc)
    if not isinstance(data, dict):
        return None, "la raíz no es un objeto JSON"
    return data, None


def course_scope_coverage(course_data: dict[str, Any] | None) -> dict[str, bool]:
    if course_data is None:
        return {name: False for name in COURSE_SCOPE_ALIASES}
    return {
        name: key_present(course_data, aliases)
        for name, aliases in COURSE_SCOPE_ALIASES.items()
    }


def unit_component_coverage(unit_data: dict[str, Any]) -> dict[str, bool]:
    return {
        name: key_present(unit_data, aliases)
        for name, aliases in UNIT_COMPONENT_ALIASES.items()
    }


def assess_evaluation(course_data: dict[str, Any] | None, units: list[dict[str, Any]]) -> dict[str, bool]:
    aggregate: dict[str, Any] = {"course": course_data or {}, "units": units}
    return {
        "assessment_plan": key_present(aggregate, {"assessment_plan", "evaluation_plan"}),
        "competency_mapping": key_present(aggregate, {"competency", "competencies", "learning_outcomes", "evaluated_outcome"}),
        "expected_evidence": key_present(aggregate, {"expected_evidence", "deliverables", "evidence_expected"}),
        "achievement_criteria": key_present(aggregate, {"achievement_criteria", "checking_criteria", "rubric", "mastery_criteria"}),
        "critical_errors": key_present(aggregate, {"critical_errors", "common_errors", "failure_conditions"}),
        "assessment_limits": key_present(aggregate, {"assessment_limitations", "limitations"}),
    }


def status_mismatch(status: str, review_artifact: Path | None, missing_protocol: list[str]) -> list[str]:
    issues: list[str] = []
    if status == "complete" and review_artifact is None:
        issues.append("status complete sin registro de revisión identificable")
    if status == "complete" and missing_protocol:
        issues.append("status complete con artefactos mínimos ausentes")
    if status in {"generated", "review", "complete"} and "units" in missing_protocol:
        issues.append(f"status {status} sin unidades desarrolladas suficientes")
    return issues


def classify_band(
    *,
    expected_units: int,
    developed_units: int,
    missing_protocol: list[str],
    component_ratio: float,
    review_artifact: Path | None,
    technical_errors: list[str],
) -> str:
    if technical_errors:
        return "technical_failure"
    if developed_units == 0:
        return "catalog_or_placeholder"
    if developed_units < expected_units:
        return "partial_development"
    if missing_protocol:
        return "content_present_protocol_incomplete"
    if component_ratio < 0.85:
        return "architecture_incomplete"
    if review_artifact is None:
        return "ready_for_documented_review"
    return "protocol_ready_for_human_review"


def audit() -> dict[str, Any]:
    curriculum = generate_site.load_json(generate_site.DATA_PATH)
    authored_overrides = audit_course_completion.load_authored_overrides()
    rows: list[dict[str, Any]] = []

    for area in curriculum.get("areas", []):
        area_id = str(area["id"])
        for subject in area.get("subjects", []):
            merged = generate_site.merge_subject_overlay(area, subject)
            subject_id = str(merged["id"])
            title = str(merged.get("title") or subject_id)
            expected_units = len(merged.get("detailed_units", []))

            counts = Counter()
            for unit in merged.get("detailed_units", []):
                classification = audit_course_completion.classify_unit(
                    area_id,
                    subject_id,
                    int(unit["unit"]),
                    authored_overrides,
                )
                counts[classification] += 1
            developed_units = counts["advanced"] + counts["authored"]

            overlay_path = SUBJECTS / area_id / f"{subject_id}.json"
            course_path = GENERATED_COURSES / f"{subject_id}.json"
            decision_path = find_subject_artifact(CURRICULUM_DECISIONS, subject_id)
            coverage_path = find_subject_artifact(CURRICULUM_COVERAGE, subject_id) or find_subject_artifact(CURRICULUM_COVERAGE, area_id)
            source_path = SOURCE_REGISTRY / f"{subject_id}.json"
            review_path = find_review_artifact(subject_id)
            redevelopment_path = COURSE_REDEVELOPMENT / subject_id / "course.json"

            canonical_course_path = course_path if course_path.exists() else redevelopment_path if redevelopment_path.exists() else overlay_path if overlay_path.exists() else None
            course_data, course_error = load_optional_json(canonical_course_path)

            unit_paths = sorted((GENERATED_UNITS / subject_id).glob("unit-*.json"))
            if not unit_paths and (COURSE_REDEVELOPMENT / subject_id / "units").exists():
                unit_paths = sorted((COURSE_REDEVELOPMENT / subject_id / "units").glob("unit-*.json"))

            units: list[dict[str, Any]] = []
            technical_errors: list[str] = []
            if course_error:
                technical_errors.append(f"curso JSON inválido: {course_error}")
            for path in unit_paths:
                try:
                    value = load_json(path)
                    if not isinstance(value, dict):
                        raise ValueError("la raíz no es un objeto")
                    units.append(value)
                except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                    technical_errors.append(f"{path.name}: {exc}")

            component_counts = Counter()
            for unit_data in units:
                for component, present in unit_component_coverage(unit_data).items():
                    component_counts[component] += int(present)
            denominator = len(units) * len(UNIT_COMPONENT_ALIASES)
            component_ratio = sum(component_counts.values()) / denominator if denominator else 0.0

            scope = course_scope_coverage(course_data)
            evaluation = assess_evaluation(course_data, units)
            public_course = ROOT / area_id / subject_id / "index.html"

            artefacts = {
                "course_profile": canonical_course_path is not None,
                "coverage_matrix": coverage_path is not None,
                "architecture_decision": decision_path is not None,
                "source_registry": source_path.exists(),
                "unit_program": expected_units > 0,
                "units": len(unit_paths) >= expected_units > 0,
                "practices_evaluations": evaluation["assessment_plan"] and key_present(units, {"guided_activity", "guided_activities", "practice_sets"}),
                "mastery_criteria": evaluation["achievement_criteria"],
                "review_record": review_path is not None,
                "public_page_sync": public_course.exists() and counts["missing"] == 0,
            }
            missing_protocol = [name for name, present in artefacts.items() if not present]

            declared_status = str(
                (course_data or {}).get("status")
                or merged.get("status")
                or "unknown"
            )
            mismatches = status_mismatch(declared_status, review_path, missing_protocol)
            band = classify_band(
                expected_units=expected_units,
                developed_units=developed_units,
                missing_protocol=missing_protocol,
                component_ratio=component_ratio,
                review_artifact=review_path,
                technical_errors=technical_errors,
            )

            rows.append(
                {
                    "area_id": area_id,
                    "subject_id": subject_id,
                    "title": title,
                    "declared_status": declared_status,
                    "audit_band": band,
                    "expected_units": expected_units,
                    "advanced_units": counts["advanced"],
                    "authored_units": counts["authored"],
                    "fallback_units": counts["fallback"],
                    "missing_public_pages": counts["missing"],
                    "developed_units": developed_units,
                    "protocol_artefacts": artefacts,
                    "missing_protocol_artefacts": missing_protocol,
                    "course_scope_coverage": scope,
                    "unit_component_coverage": dict(component_counts),
                    "unit_component_ratio": round(component_ratio, 4),
                    "evaluation_coverage": evaluation,
                    "technical_errors": technical_errors,
                    "status_mismatches": mismatches,
                    "paths": {
                        "course": str(canonical_course_path.relative_to(ROOT)) if canonical_course_path else None,
                        "coverage": str(coverage_path.relative_to(ROOT)) if coverage_path else None,
                        "decision": str(decision_path.relative_to(ROOT)) if decision_path else None,
                        "sources": str(source_path.relative_to(ROOT)) if source_path.exists() else None,
                        "review": str(review_path.relative_to(ROOT)) if review_path else None,
                    },
                }
            )

    band_counts = Counter(row["audit_band"] for row in rows)
    declared_counts = Counter(row["declared_status"] for row in rows)
    missing_counts = Counter(
        artefact
        for row in rows
        for artefact in row["missing_protocol_artefacts"]
    )
    summary = {
        "course_count": len(rows),
        "band_counts": dict(sorted(band_counts.items())),
        "declared_status_counts": dict(sorted(declared_counts.items())),
        "courses_with_technical_errors": sum(bool(row["technical_errors"]) for row in rows),
        "courses_with_status_mismatches": sum(bool(row["status_mismatches"]) for row in rows),
        "courses_with_all_units_developed": sum(row["developed_units"] == row["expected_units"] > 0 for row in rows),
        "courses_protocol_complete": sum(not row["missing_protocol_artefacts"] for row in rows),
        "missing_artefact_counts": dict(sorted(missing_counts.items(), key=lambda item: (-item[1], item[0]))),
        "disclaimer": "El informe valida evidencia documental y estructura observable; no certifica suficiencia disciplinar ni revisión humana.",
    }
    rows.sort(
        key=lambda row: (
            row["audit_band"] not in {"technical_failure", "content_present_protocol_incomplete", "architecture_incomplete"},
            -row["developed_units"],
            row["area_id"],
            row["subject_id"],
        )
    )
    return {"summary": summary, "courses": rows}


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Auditoría de asignaturas existentes contra el protocolo académico",
        "",
        "Esta auditoría separa integridad técnica, presencia de artefactos y preparación para revisión humana. No declara validez académica automática.",
        "",
        "## Resumen",
        "",
        f"- Asignaturas inventariadas: {summary['course_count']}",
        f"- Con todas las unidades desarrolladas o autorales: {summary['courses_with_all_units_developed']}",
        f"- Con los diez artefactos mínimos identificados: {summary['courses_protocol_complete']}",
        f"- Con errores técnicos: {summary['courses_with_technical_errors']}",
        f"- Con discrepancias entre estado declarado y evidencia: {summary['courses_with_status_mismatches']}",
        "",
        "### Bandas de auditoría",
        "",
    ]
    for band, count in summary["band_counts"].items():
        lines.append(f"- `{band}`: {count}")
    lines.extend(["", "### Artefactos ausentes", ""])
    for artefact, count in summary["missing_artefact_counts"].items():
        lines.append(f"- `{artefact}`: {count}")

    lines.extend(
        [
            "",
            "## Inventario por asignatura",
            "",
            "| Área | Asignatura | Estado | Banda | Unidades | Arquitectura de unidad | Artefactos ausentes | Alertas |",
            "|---|---|---|---|---:|---:|---|---|",
        ]
    )
    for row in report["courses"]:
        missing = ", ".join(row["missing_protocol_artefacts"]) or "—"
        alerts = "; ".join(row["technical_errors"] + row["status_mismatches"]) or "—"
        lines.append(
            f"| {row['area_id']} | {row['title']} (`{row['subject_id']}`) | "
            f"{row['declared_status']} | `{row['audit_band']}` | "
            f"{row['developed_units']}/{row['expected_units']} | "
            f"{row['unit_component_ratio']:.0%} | {missing} | {alerts} |"
        )

    lines.extend(
        [
            "",
            "## Interpretación",
            "",
            "- `protocol_ready_for_human_review` significa que la evidencia documental observable está completa; todavía requiere revisión disciplinar.",
            "- `ready_for_documented_review` indica contenido y artefactos suficientes, pero sin registro de revisión identificable.",
            "- `content_present_protocol_incomplete` indica que existe contenido desarrollado, pero faltan artefactos exigidos por el protocolo.",
            "- `architecture_incomplete` indica que las unidades no cubren de forma consistente los componentes pedagógicos mínimos.",
            "- `partial_development` y `catalog_or_placeholder` no deben presentarse como asignaturas completas.",
            "- `technical_failure` exige corrección antes de cualquier revisión académica.",
            "",
            summary["disclaimer"],
        ]
    )
    return "\n".join(lines) + "\n"


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
        args.markdown_output.write_text(render_markdown(report), encoding="utf-8")

    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    errors: list[str] = []
    if report["summary"]["course_count"] != args.require_course_count:
        errors.append(f"se esperaban {args.require_course_count} asignaturas")
    if args.fail_on_technical_errors and report["summary"]["courses_with_technical_errors"]:
        errors.append("existen asignaturas con errores técnicos")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
