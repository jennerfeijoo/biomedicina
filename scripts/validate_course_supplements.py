#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENT_ROOT = ROOT / "data" / "course_supplements"
COURSE_ROOT = ROOT / "data" / "generated_courses"
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
FORBIDDEN_MARKERS = ("lorem ipsum", "contenido pendiente", "por completar", "placeholder")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("la raíz debe ser un objeto JSON")
    return data


def require_list(value: Any, minimum: int, label: str) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"{label}: se requieren al menos {minimum}")
    return value


def validate_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: texto ausente")
    lowered = value.casefold()
    for marker in FORBIDDEN_MARKERS:
        if marker in lowered:
            raise ValueError(f"{label}: marcador incompleto detectado: {marker}")
    return value


def validate_module(module: dict[str, Any], module_ids: set[str]) -> tuple[int, int, int, int]:
    module_id = validate_text(module.get("module_id"), "module_id")
    if module_id in module_ids:
        raise ValueError(f"module_id duplicado: {module_id}")
    module_ids.add(module_id)
    validate_text(module.get("title"), f"{module_id}.title")

    outcomes = require_list(module.get("learning_outcomes"), 5, f"{module_id}.learning_outcomes")
    for index, outcome in enumerate(outcomes, start=1):
        validate_text(outcome, f"{module_id}.learning_outcomes[{index}]")

    sections = require_list(module.get("theory_sections"), 3, f"{module_id}.theory_sections")
    paragraph_count = 0
    for section_index, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            raise ValueError(f"{module_id}.theory_sections[{section_index}] no es un objeto")
        validate_text(section.get("heading"), f"{module_id}.section[{section_index}].heading")
        paragraphs = require_list(
            section.get("paragraphs"), 4, f"{module_id}.section[{section_index}].paragraphs"
        )
        key_points = require_list(
            section.get("key_points"), 4, f"{module_id}.section[{section_index}].key_points"
        )
        for paragraph_index, paragraph in enumerate(paragraphs, start=1):
            validate_text(paragraph, f"{module_id}.section[{section_index}].paragraph[{paragraph_index}]")
        for point_index, point in enumerate(key_points, start=1):
            validate_text(point, f"{module_id}.section[{section_index}].key_point[{point_index}]")
        paragraph_count += len(paragraphs)

    cases = require_list(module.get("worked_cases"), 2, f"{module_id}.worked_cases")
    for case_index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            raise ValueError(f"{module_id}.worked_cases[{case_index}] no es un objeto")
        validate_text(case.get("title"), f"{module_id}.case[{case_index}].title")
        validate_text(case.get("problem"), f"{module_id}.case[{case_index}].problem")
        validate_text(case.get("solution"), f"{module_id}.case[{case_index}].solution")

    workshops = require_list(
        module.get("practical_workshops"), 2, f"{module_id}.practical_workshops"
    )
    task_count = 0
    for workshop_index, workshop in enumerate(workshops, start=1):
        if not isinstance(workshop, dict):
            raise ValueError(f"{module_id}.practical_workshops[{workshop_index}] no es un objeto")
        validate_text(workshop.get("title"), f"{module_id}.workshop[{workshop_index}].title")
        tasks = require_list(
            workshop.get("tasks"), 4, f"{module_id}.workshop[{workshop_index}].tasks"
        )
        for task_index, task in enumerate(tasks, start=1):
            validate_text(task, f"{module_id}.workshop[{workshop_index}].task[{task_index}]")
        task_count += len(tasks)

    mastery = require_list(module.get("mastery_questions"), 8, f"{module_id}.mastery_questions")
    for question_index, question in enumerate(mastery, start=1):
        validate_text(question, f"{module_id}.mastery_questions[{question_index}]")

    return len(sections), paragraph_count, len(cases), task_count


def validate_supplement(path: Path) -> dict[str, int]:
    data = load_json(path)
    required = {
        "schema_version",
        "subject_id",
        "title",
        "status",
        "purpose",
        "modules",
        "integrative_assessment",
        "sources",
        "editorial_notice",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError("faltan campos: " + ", ".join(missing))
    if data.get("schema_version") != "1.0":
        raise ValueError("schema_version debe ser 1.0")
    if data.get("status") != "review":
        raise ValueError("status debe permanecer en review")

    subject_id = validate_text(data.get("subject_id"), "subject_id")
    if path.parent.name != subject_id:
        raise ValueError("subject_id no coincide con la carpeta")
    if not (COURSE_ROOT / f"{subject_id}.json").exists():
        raise ValueError("no existe la arquitectura generada de la asignatura")
    validate_text(data.get("title"), "title")
    validate_text(data.get("purpose"), "purpose")
    validate_text(data.get("editorial_notice"), "editorial_notice")

    modules = require_list(data.get("modules"), 1, "modules")
    module_ids: set[str] = set()
    section_count = 0
    paragraph_count = 0
    case_count = 0
    task_count = 0
    for module_index, module in enumerate(modules, start=1):
        if not isinstance(module, dict):
            raise ValueError(f"modules[{module_index}] no es un objeto")
        sections, paragraphs, cases, tasks = validate_module(module, module_ids)
        section_count += sections
        paragraph_count += paragraphs
        case_count += cases
        task_count += tasks

    assessment = data.get("integrative_assessment")
    if not isinstance(assessment, dict):
        raise ValueError("integrative_assessment debe ser un objeto")
    validate_text(assessment.get("title"), "integrative_assessment.title")
    validate_text(assessment.get("scenario"), "integrative_assessment.scenario")
    deliverables = require_list(
        assessment.get("deliverables"), 4, "integrative_assessment.deliverables"
    )
    criteria = require_list(
        assessment.get("mastery_criteria"), 4, "integrative_assessment.mastery_criteria"
    )
    for index, item in enumerate(deliverables, start=1):
        validate_text(item, f"integrative_assessment.deliverables[{index}]")
    for index, item in enumerate(criteria, start=1):
        validate_text(item, f"integrative_assessment.mastery_criteria[{index}]")

    sources = require_list(data.get("sources"), 5, "sources")
    urls: list[str] = []
    domains: set[str] = set()
    for source_index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            raise ValueError(f"sources[{source_index}] no es un objeto")
        validate_text(source.get("title"), f"sources[{source_index}].title")
        validate_text(source.get("organization"), f"sources[{source_index}].organization")
        url = validate_text(source.get("url"), f"sources[{source_index}].url")
        if not URL_RE.match(url):
            raise ValueError(f"sources[{source_index}].url no es HTTP(S)")
        urls.append(url)
        domain = urlparse(url).netloc.casefold().removeprefix("www.")
        if domain:
            domains.add(domain)
    if len(urls) != len(set(urls)):
        raise ValueError("sources contiene URL duplicadas")
    if len(domains) < 3:
        raise ValueError("sources debe cubrir al menos tres dominios")

    serialized = json.dumps(data, ensure_ascii=False).casefold()
    for marker in FORBIDDEN_MARKERS:
        if marker in serialized:
            raise ValueError(f"marcador incompleto detectado: {marker}")

    return {
        "modules": len(modules),
        "sections": section_count,
        "paragraphs": paragraph_count,
        "worked_cases": case_count,
        "workshop_tasks": task_count,
        "sources": len(sources),
        "source_domains": len(domains),
    }


def validate_index(paths: list[Path]) -> None:
    index_path = SUPPLEMENT_ROOT / "index.json"
    if not index_path.exists():
        raise ValueError("falta data/course_supplements/index.json")
    index = load_json(index_path)
    if index.get("schema_version") != "1.0":
        raise ValueError("index.schema_version debe ser 1.0")
    entries = require_list(index.get("supplements"), 1, "index.supplements")
    indexed_paths: set[str] = set()
    indexed_subjects: set[str] = set()
    for entry_index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"index.supplements[{entry_index}] no es un objeto")
        subject_id = validate_text(entry.get("subject_id"), f"index[{entry_index}].subject_id")
        relative_path = validate_text(entry.get("path"), f"index[{entry_index}].path")
        if entry.get("status") != "review":
            raise ValueError(f"index[{entry_index}].status debe ser review")
        require_list(entry.get("scope"), 1, f"index[{entry_index}].scope")
        if subject_id in indexed_subjects:
            raise ValueError(f"subject_id duplicado en index: {subject_id}")
        if relative_path in indexed_paths:
            raise ValueError(f"path duplicado en index: {relative_path}")
        indexed_subjects.add(subject_id)
        indexed_paths.add(relative_path)
        if not (ROOT / relative_path).exists():
            raise ValueError(f"ruta indexada inexistente: {relative_path}")

    actual_paths = {str(path.relative_to(ROOT)).replace("\\", "/") for path in paths}
    if indexed_paths != actual_paths:
        missing = sorted(actual_paths - indexed_paths)
        orphan = sorted(indexed_paths - actual_paths)
        raise ValueError(f"index no coincide con suplementos; faltan={missing}, sobran={orphan}")


def main() -> int:
    paths = sorted(SUPPLEMENT_ROOT.glob("*/advanced-core.json"))
    if not paths:
        print("No hay suplementos académicos para validar.")
        return 0

    errors: list[str] = []
    metrics: dict[str, dict[str, int]] = {}
    try:
        validate_index(paths)
    except (ValueError, TypeError, json.JSONDecodeError) as error:
        errors.append(f"INDEX: {error}")

    for path in paths:
        try:
            metrics[path.parent.name] = validate_supplement(path)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            errors.append(f"ERROR {path.relative_to(ROOT)}: {error}")

    print("VALIDACIÓN DE SUPLEMENTOS ACADÉMICOS")
    for subject_id, values in sorted(metrics.items()):
        print(
            f"- {subject_id}: módulos={values['modules']} · secciones={values['sections']} · "
            f"párrafos={values['paragraphs']} · casos={values['worked_cases']} · "
            f"tareas={values['workshop_tasks']} · fuentes={values['sources']} "
            f"({values['source_domains']} dominios)"
        )
    print("La extensión textual no se utiliza como requisito ni como límite.")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"Suplementos válidos: {len(metrics)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
