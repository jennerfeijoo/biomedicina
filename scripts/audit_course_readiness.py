#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import validate_generated_units  # noqa: E402

UNIT_ROOT = ROOT / "data" / "generated_units"
COURSE_ROOT = ROOT / "data" / "generated_courses"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
COURSE_TIME_KEYS = {
    "estimated_workload",
    "duration_weeks",
    "weekly_hours",
    "total_workload_hours",
    "semester_plan",
}

MIN_UNITS = 6
MIN_DIAGNOSTIC_QUESTIONS = 10
MIN_COURSE_OUTCOMES = 6
MIN_COURSE_COMPETENCIES = 5
MIN_COURSE_RESOURCES = 8
MIN_PROJECT_PHASES = 4
MIN_PROJECT_DELIVERABLES = 3
MIN_RUBRIC_CRITERIA = 4


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("la raíz debe ser un objeto JSON")
    return data


def collect_text(value: Any, *, key: str = "") -> list[str]:
    if isinstance(value, str):
        if key == "url" or URL_RE.match(value):
            return []
        return [value]
    if isinstance(value, list):
        output: list[str] = []
        for item in value:
            output.extend(collect_text(item, key=key))
        return output
    if isinstance(value, dict):
        output: list[str] = []
        for child_key, child in value.items():
            if child_key in {"schema_version", "subject_id", "area_id", "slug", "status"}:
                continue
            output.extend(collect_text(child, key=child_key))
        return output
    return []


def count_words(data: dict[str, Any]) -> int:
    return len(WORD_RE.findall(" ".join(collect_text(data))))


def audit_course_architecture(subject_id: str) -> list[str]:
    path = COURSE_ROOT / f"{subject_id}.json"
    if not path.exists():
        return [f"falta {path.relative_to(ROOT)}"]
    try:
        data = load_json(path)
    except (ValueError, TypeError, json.JSONDecodeError) as error:
        return [f"curso JSON inválido: {error}"]

    issues: list[str] = []
    if data.get("schema_version") != "2.0":
        issues.append("el curso debe usar schema_version 2.0")
    if data.get("subject_id") != subject_id:
        issues.append("subject_id del curso no coincide con la carpeta")
    if data.get("status") not in {"review", "complete"}:
        issues.append("status del curso debe ser review o complete")

    forbidden = sorted(COURSE_TIME_KEYS & data.keys())
    if forbidden:
        issues.append("conserva metadatos temporales: " + ", ".join(forbidden))
    if len(data.get("course_competencies", [])) < MIN_COURSE_COMPETENCIES:
        issues.append(f"menos de {MIN_COURSE_COMPETENCIES} competencias")
    if len(data.get("learning_outcomes", [])) < MIN_COURSE_OUTCOMES:
        issues.append(f"menos de {MIN_COURSE_OUTCOMES} resultados de aprendizaje")

    diagnostic = data.get("diagnostic_assessment", {})
    if len(diagnostic.get("questions", [])) < MIN_DIAGNOSTIC_QUESTIONS:
        issues.append(f"diagnóstico con menos de {MIN_DIAGNOSTIC_QUESTIONS} preguntas")

    assessment = data.get("assessment_plan", [])
    if not assessment:
        issues.append("falta plan de evaluación")
    else:
        total_weight = sum(
            float(item.get("weight_percent", 0) or 0)
            for item in assessment
            if isinstance(item, dict)
        )
        if abs(total_weight - 100.0) > 1e-9:
            issues.append(f"ponderaciones de evaluación suman {total_weight:g} %, no 100 %")

    project = data.get("final_project", {})
    if len(project.get("phases", [])) < MIN_PROJECT_PHASES:
        issues.append(f"proyecto con menos de {MIN_PROJECT_PHASES} fases")
    if len(project.get("deliverables", [])) < MIN_PROJECT_DELIVERABLES:
        issues.append(f"proyecto con menos de {MIN_PROJECT_DELIVERABLES} entregables")
    rubric = project.get("rubric", [])
    if len(rubric) < MIN_RUBRIC_CRITERIA:
        issues.append(f"rúbrica con menos de {MIN_RUBRIC_CRITERIA} criterios")
    elif abs(
        sum(
            float(item.get("weight_percent", 0) or 0)
            for item in rubric
            if isinstance(item, dict)
        )
        - 100.0
    ) > 1e-9:
        issues.append("la rúbrica del proyecto no suma 100 %")

    if len(data.get("core_resources", [])) < MIN_COURSE_RESOURCES:
        issues.append(f"menos de {MIN_COURSE_RESOURCES} recursos centrales")
    return issues


def audit_units(subject_id: str) -> tuple[list[Path], int, set[str], int, list[str]]:
    paths = sorted((UNIT_ROOT / subject_id).glob("unit-*.json"))
    total_words = 0
    schema_versions: set[str] = set()
    mirrored_units = 0
    issues: list[str] = []
    for path in paths:
        try:
            data = load_json(path)
            schema_versions.add(str(data.get("schema_version", "")))
            total_words += count_words(data)
            _, mirrored = validate_generated_units.validate_unit(path)
            mirrored_units += int(mirrored)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            issues.append(f"{path.name}: {error}")
    return paths, total_words, schema_versions, mirrored_units, issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audita la arquitectura de curso y reutiliza el validador canónico de unidades. "
            "La extensión textual se informa, pero no determina completitud."
        )
    )
    parser.add_argument("--subject", help="Limita la auditoría a un subject_id.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Devuelve error cuando la estructura seleccionada no cumple.",
    )
    args = parser.parse_args()

    generated_subjects = sorted(path.stem for path in COURSE_ROOT.glob("*.json"))
    if args.subject:
        generated_subjects = [args.subject]
    if not generated_subjects:
        print("No hay arquitecturas de curso generadas para auditar.")
        return 1 if args.strict else 0

    failed_subjects = 0
    for subject_id in generated_subjects:
        paths, total_words, schema_versions, mirrored_units, unit_issues = audit_units(subject_id)
        course_issues = audit_course_architecture(subject_id)
        if len(paths) < MIN_UNITS:
            course_issues.append(f"{len(paths)} unidades; mínimo estructural {MIN_UNITS}")
        if schema_versions != {"2.0"}:
            course_issues.append("todas las unidades deben usar schema_version 2.0")

        ready = not course_issues and not unit_issues
        state = "ARQUITECTURA DEL CURSO VÁLIDA" if ready else "ESTRUCTURA PENDIENTE"
        print(f"\n{subject_id}: {state}")
        print(
            f"  unidades={len(paths)} · reconstrucciones trazables={mirrored_units} · "
            f"extensión descriptiva={total_words} palabras · "
            f"esquemas={','.join(sorted(schema_versions)) or 'ninguno'}"
        )
        for issue in course_issues:
            print(f"  CURSO: {issue}")
        for issue in unit_issues:
            print(f"  UNIDAD: {issue}")
        if not ready:
            failed_subjects += 1

    print("\nNota: esta auditoría valida estructura, no exhaustividad disciplinar ni revisión humana.")
    print(
        f"Asignaturas auditadas: {len(generated_subjects)} · "
        f"estructuras pendientes: {failed_subjects}"
    )
    return 1 if args.strict and failed_subjects else 0


if __name__ == "__main__":
    raise SystemExit(main())
