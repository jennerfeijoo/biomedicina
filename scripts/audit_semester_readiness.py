#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
UNIT_ROOT = ROOT / "data" / "generated_units"
COURSE_ROOT = ROOT / "data" / "generated_courses"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)
URL_RE = re.compile(r"^https?://", re.IGNORECASE)

MIN_UNITS = 6
MIN_THEORY_SECTIONS = 4
MIN_OBJECTIVES = 5
MIN_GLOSSARY = 12
MIN_SELF_ASSESSMENT = 8
MIN_SOURCES = 5
MIN_WORKED_EXAMPLES = 2
MIN_GUIDED_ACTIVITIES = 1
MIN_PRACTICE_ITEMS = 8
MIN_COMMON_ERRORS = 5
MIN_DURATION_WEEKS = 12
MAX_DURATION_WEEKS = 16
MIN_TOTAL_HOURS = 90
MIN_SEMESTER_PLAN_ROWS = 12
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


def as_list(data: dict[str, Any], singular: str, plural: str) -> list[Any]:
    plural_value = data.get(plural)
    if isinstance(plural_value, list):
        return plural_value
    singular_value = data.get(singular)
    return [singular_value] if isinstance(singular_value, dict) else []


def practice_item_count(data: dict[str, Any]) -> int:
    total = 0
    for activity in as_list(data, "guided_activity", "guided_activities"):
        if not isinstance(activity, dict):
            continue
        for key in ("problems", "tasks", "exercises"):
            value = activity.get(key)
            if isinstance(value, list):
                total += len(value)
    for practice_set in data.get("practice_sets", []):
        if isinstance(practice_set, dict) and isinstance(practice_set.get("problems"), list):
            total += len(practice_set["problems"])
    return total


def audit_unit(data: dict[str, Any]) -> tuple[int, list[str]]:
    words = count_words(data)
    issues: list[str] = []
    if len(data.get("learning_objectives", [])) < MIN_OBJECTIVES:
        issues.append(f"menos de {MIN_OBJECTIVES} objetivos")
    if len(data.get("theory_sections", [])) < MIN_THEORY_SECTIONS:
        issues.append(f"menos de {MIN_THEORY_SECTIONS} secciones teóricas")
    if len(data.get("glossary", [])) < MIN_GLOSSARY:
        issues.append(f"menos de {MIN_GLOSSARY} términos de glosario")
    if len(data.get("self_assessment", [])) < MIN_SELF_ASSESSMENT:
        issues.append(f"menos de {MIN_SELF_ASSESSMENT} preguntas de autoevaluación")
    if len(data.get("sources", [])) < MIN_SOURCES:
        issues.append(f"menos de {MIN_SOURCES} fuentes")
    if len(as_list(data, "worked_example", "worked_examples")) < MIN_WORKED_EXAMPLES:
        issues.append(f"menos de {MIN_WORKED_EXAMPLES} ejemplos resueltos")
    if len(as_list(data, "guided_activity", "guided_activities")) < MIN_GUIDED_ACTIVITIES:
        issues.append("falta actividad guiada")
    if practice_item_count(data) < MIN_PRACTICE_ITEMS:
        issues.append(f"menos de {MIN_PRACTICE_ITEMS} problemas o tareas")
    if len(data.get("common_errors", [])) < MIN_COMMON_ERRORS:
        issues.append(f"menos de {MIN_COMMON_ERRORS} errores frecuentes")
    return words, issues


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

    duration = int(data.get("duration_weeks", 0) or 0)
    if not MIN_DURATION_WEEKS <= duration <= MAX_DURATION_WEEKS:
        issues.append(f"duración={duration}; debe estar entre {MIN_DURATION_WEEKS} y {MAX_DURATION_WEEKS} semanas")
    total_hours = int(data.get("total_workload_hours", 0) or 0)
    if total_hours < MIN_TOTAL_HOURS:
        issues.append(f"carga total={total_hours}; mínimo {MIN_TOTAL_HOURS} horas")
    if len(data.get("semester_plan", [])) < MIN_SEMESTER_PLAN_ROWS:
        issues.append(f"cronograma con menos de {MIN_SEMESTER_PLAN_ROWS} semanas")
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
        total_weight = sum(float(item.get("weight_percent", 0) or 0) for item in assessment if isinstance(item, dict))
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
    elif abs(sum(float(item.get("weight_percent", 0) or 0) for item in rubric if isinstance(item, dict)) - 100.0) > 1e-9:
        issues.append("la rúbrica del proyecto no suma 100 %")

    if len(data.get("core_resources", [])) < MIN_COURSE_RESOURCES:
        issues.append(f"menos de {MIN_COURSE_RESOURCES} recursos centrales")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audita la integridad de la arquitectura semestral sin usar extensión textual como criterio de completitud."
    )
    parser.add_argument("--subject", help="Limita la auditoría a un subject_id.")
    parser.add_argument("--strict", action="store_true", help="Devuelve error cuando la estructura seleccionada no cumple.")
    args = parser.parse_args()

    grouped: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(UNIT_ROOT.glob("*/unit-*.json")):
        grouped[path.parent.name].append(path)
    if args.subject:
        grouped = {args.subject: grouped.get(args.subject, [])}
    if not grouped:
        print("No hay unidades para auditar.")
        return 1 if args.strict else 0

    failed_subjects = 0
    for subject_id, paths in sorted(grouped.items()):
        total_words = 0
        unit_issues: list[str] = []
        schema_versions: set[str] = set()
        for path in paths:
            try:
                data = load_json(path)
                schema_versions.add(str(data.get("schema_version", "")))
                words, issues = audit_unit(data)
                total_words += words
                if issues:
                    unit_issues.append(f"{path.name}: " + "; ".join(issues))
            except (ValueError, TypeError, json.JSONDecodeError) as error:
                unit_issues.append(f"{path.name}: JSON inválido: {error}")

        course_issues = audit_course_architecture(subject_id)
        if len(paths) < MIN_UNITS:
            course_issues.append(f"{len(paths)} unidades; mínimo estructural {MIN_UNITS}")
        if schema_versions != {"2.0"}:
            course_issues.append("todas las unidades deben usar schema_version 2.0")

        ready = not course_issues and not unit_issues
        state = "ARQUITECTURA SEMESTRAL VÁLIDA" if ready else "ESTRUCTURA PENDIENTE"
        print(f"\n{subject_id}: {state}")
        print(f"  unidades={len(paths)} · extensión descriptiva={total_words} palabras · esquemas={','.join(sorted(schema_versions)) or 'ninguno'}")
        for issue in course_issues:
            print(f"  CURSO: {issue}")
        for issue in unit_issues:
            print(f"  UNIDAD: {issue}")
        if not ready:
            failed_subjects += 1

    print("\nNota: esta auditoría valida estructura, no exhaustividad disciplinar ni revisión humana.")
    print(f"Asignaturas auditadas: {len(grouped)} · estructuras pendientes: {failed_subjects}")
    return 1 if args.strict and failed_subjects else 0


if __name__ == "__main__":
    raise SystemExit(main())
