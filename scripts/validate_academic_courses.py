#!/usr/bin/env python3
"""Validate canonical academic courses and their cross-file relationships."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = ROOT / "data" / "courses"
COURSE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CODE_RE = re.compile(r"^[A-Z][A-Z0-9]{2,11}$")
UNIT_ID_RE = re.compile(r"^(?P<code>[A-Z][A-Z0-9]{2,11})-U(?P<number>\d{2})$")
GENERIC_MARKERS = (
    "lorem ipsum",
    "contenido pendiente",
    "por completar",
    "concepto de la unidad que debe definirse",
)
STATUS_KEYS = {
    "content",
    "sources",
    "pedagogy",
    "multimedia",
    "internal_review",
    "external_review",
    "publication",
}


@dataclass
class Report:
    course_id: str
    errors: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    multimedia_gaps: list[str] = field(default_factory=list)
    counts: Counter[str] = field(default_factory=Counter)

    def error(self, location: str, message: str) -> None:
        self.errors.append(f"{self.course_id}:{location}: {message}")

    def gap(self, location: str, message: str, *, category: str = "content") -> None:
        target = self.multimedia_gaps if category == "multimedia" else self.gaps
        target.append(f"{self.course_id}:{location}: {message}")


def load_json(path: Path, report: Report, location: str) -> dict[str, Any]:
    if not path.exists():
        report.error(location, f"falta {path.relative_to(ROOT)}")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(location, f"JSON inválido: {exc}")
        return {}
    if not isinstance(payload, dict):
        report.error(location, "la raíz debe ser un objeto")
        return {}
    return payload


def require_fields(payload: dict[str, Any], fields: set[str], report: Report, location: str) -> None:
    missing = sorted(field for field in fields if field not in payload)
    if missing:
        report.error(location, "faltan campos: " + ", ".join(missing))


def require_nonempty_text(payload: dict[str, Any], field_name: str, report: Report, location: str) -> str:
    value = str(payload.get(field_name) or "").strip()
    if not value:
        report.error(f"{location}.{field_name}", "debe contener texto")
    return value


def dict_list(value: Any, report: Report, location: str, *, minimum: int = 0) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        report.error(location, "debe ser una lista")
        return []
    output = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            report.error(f"{location}[{index}]", "debe ser un objeto")
        else:
            output.append(item)
    if len(output) < minimum:
        report.error(location, f"requiere al menos {minimum} elemento(s)")
    return output


def text_list(value: Any, report: Report, location: str, *, minimum: int = 0) -> list[str]:
    if not isinstance(value, list):
        report.error(location, "debe ser una lista")
        return []
    output = []
    for index, item in enumerate(value):
        text = str(item or "").strip()
        if not text:
            report.error(f"{location}[{index}]", "no puede estar vacío")
        else:
            output.append(text)
    if len(output) < minimum:
        report.error(location, f"requiere al menos {minimum} elemento(s)")
    return output


def record_ids(
    value: Any,
    report: Report,
    location: str,
    *,
    minimum: int = 0,
) -> set[str]:
    records = dict_list(value, report, location, minimum=minimum)
    identifiers: set[str] = set()
    for index, record in enumerate(records):
        record_id = require_nonempty_text(record, "id", report, f"{location}[{index}]")
        require_nonempty_text(record, "statement", report, f"{location}[{index}]")
        if record_id in identifiers:
            report.error(f"{location}[{index}].id", f"identificador duplicado {record_id}")
        identifiers.add(record_id)
    return identifiers


def validate_status(value: Any, report: Report, location: str) -> None:
    if not isinstance(value, dict):
        report.error(location, "debe ser un objeto multidimensional")
        return
    missing = sorted(STATUS_KEYS - value.keys())
    extra = sorted(value.keys() - STATUS_KEYS)
    if missing:
        report.error(location, "faltan dimensiones: " + ", ".join(missing))
    if extra:
        report.error(location, "dimensiones desconocidas: " + ", ".join(extra))


def safe_child(course_dir: Path, relative: str, report: Report, location: str) -> Path:
    candidate = (course_dir / relative).resolve()
    try:
        candidate.relative_to(course_dir.resolve())
    except ValueError:
        report.error(location, "la ruta sale del directorio del curso")
        return course_dir / "__invalid__"
    return candidate


def collect_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in collect_strings(item)]
    if isinstance(value, dict):
        return [text for item in value.values() for text in collect_strings(item)]
    return []


def indexed_records(payload: dict[str, Any], field_name: str, report: Report, location: str) -> dict[str, dict[str, Any]]:
    records = dict_list(payload.get(field_name), report, f"{location}.{field_name}")
    output: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        record_id = require_nonempty_text(record, "id", report, f"{location}.{field_name}[{index}]")
        if record_id in output:
            report.error(f"{location}.{field_name}[{index}].id", f"identificador duplicado {record_id}")
        output[record_id] = record
    return output


def validate_assessment(
    payload: dict[str, Any],
    report: Report,
    location: str,
    *,
    course_id: str,
    unit_id: str,
    learning_outcomes: set[str],
    source_ids: set[str],
) -> None:
    require_fields(
        payload,
        {"$schema", "schema_version", "id", "course_id", "scope", "unit_id", "purpose", "student_payload_policy", "items", "status"},
        report,
        location,
    )
    if payload.get("schema_version") != "1.0":
        report.error(f"{location}.schema_version", "debe ser 1.0")
    if payload.get("$schema") != "../../../../schemas/academic/assessment-v1.schema.json":
        report.error(f"{location}.$schema", "referencia de esquema inconsistente")
    if payload.get("course_id") != course_id or payload.get("unit_id") != unit_id:
        report.error(location, "identidad de curso o unidad inconsistente")
    if payload.get("scope") != "unit":
        report.error(f"{location}.scope", "debe ser unit")
    items = dict_list(payload.get("items"), report, f"{location}.items", minimum=1)
    seen: set[str] = set()
    for index, item in enumerate(items):
        item_location = f"{location}.items[{index}]"
        require_fields(
            item,
            {"id", "type", "prompt", "linked_learning_outcome_ids", "difficulty", "cognitive_level", "answer_key", "feedback", "source_ids", "status"},
            report,
            item_location,
        )
        item_id = require_nonempty_text(item, "id", report, item_location)
        if item_id in seen:
            report.error(f"{item_location}.id", f"identificador duplicado {item_id}")
        seen.add(item_id)
        require_nonempty_text(item, "prompt", report, item_location)
        linked = set(text_list(item.get("linked_learning_outcome_ids"), report, f"{item_location}.linked_learning_outcome_ids", minimum=1))
        for outcome_id in sorted(linked - learning_outcomes):
            report.error(f"{item_location}.linked_learning_outcome_ids", f"resultado inexistente {outcome_id}")
        answer_key = item.get("answer_key")
        if not isinstance(answer_key, dict):
            report.error(f"{item_location}.answer_key", "debe ser un objeto separado del payload estudiantil")
        else:
            require_nonempty_text(answer_key, "expected_answer", report, f"{item_location}.answer_key")
            if not str(answer_key.get("explanation") or "").strip():
                report.gap(f"{item_location}.answer_key.explanation", "falta explicación razonada")
        feedback = item.get("feedback")
        if not isinstance(feedback, dict) or not all(str(feedback.get(key) or "").strip() for key in ("correct", "incorrect")):
            report.gap(f"{item_location}.feedback", "falta retroalimentación específica")
        if item.get("difficulty") == "unclassified":
            report.gap(f"{item_location}.difficulty", "dificultad sin clasificar")
        if item.get("cognitive_level") == "unclassified":
            report.gap(f"{item_location}.cognitive_level", "nivel cognitivo sin clasificar")
        for source_id in text_list(item.get("source_ids"), report, f"{item_location}.source_ids"):
            if source_id not in source_ids:
                report.error(f"{item_location}.source_ids", f"fuente inexistente {source_id}")
    report.counts["assessment_items"] += len(items)


def validate_course_assessment(payload: dict[str, Any], report: Report, location: str, course_id: str) -> None:
    require_fields(
        payload,
        {"$schema", "schema_version", "id", "course_id", "scope", "principles", "assessment_plan", "diagnostic", "midterm_blueprint", "capstone", "status"},
        report,
        location,
    )
    if payload.get("course_id") != course_id or payload.get("scope") != "course":
        report.error(location, "identidad o alcance inconsistente")
    if payload.get("$schema") != "../../../../schemas/academic/assessment-v1.schema.json":
        report.error(f"{location}.$schema", "referencia de esquema inconsistente")
    plan = dict_list(payload.get("assessment_plan"), report, f"{location}.assessment_plan", minimum=1)
    weights = [item.get("weight_percent") for item in plan]
    if all(isinstance(value, (int, float)) for value in weights) and sum(weights) != 100:
        report.error(f"{location}.assessment_plan", f"los pesos suman {sum(weights)}, no 100")
    diagnostic = payload.get("diagnostic")
    if not isinstance(diagnostic, dict) or not as_nonempty_list(diagnostic.get("questions")):
        report.gap(f"{location}.diagnostic", "diagnóstico sin preguntas")
    blueprint = dict_list(payload.get("midterm_blueprint"), report, f"{location}.midterm_blueprint")
    blueprint_weights = [item.get("weight_percent") for item in blueprint]
    if blueprint and all(isinstance(value, (int, float)) for value in blueprint_weights) and sum(blueprint_weights) != 100:
        report.error(f"{location}.midterm_blueprint", "los pesos del examen intermedio no suman 100")
    capstone = payload.get("capstone")
    if not isinstance(capstone, dict):
        report.error(f"{location}.capstone", "debe ser un objeto")
    else:
        rubric = dict_list(capstone.get("rubric"), report, f"{location}.capstone.rubric", minimum=1)
        rubric_weights = [item.get("weight_percent") for item in rubric]
        if all(isinstance(value, (int, float)) for value in rubric_weights) and sum(rubric_weights) != 100:
            report.error(f"{location}.capstone.rubric", "los pesos de la rúbrica no suman 100")


def as_nonempty_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) and value else []


def validate_unit(
    payload: dict[str, Any],
    report: Report,
    location: str,
    *,
    course_dir: Path,
    course_id: str,
    code: str,
    course_outcomes: set[str],
    all_unit_ids: set[str],
    glossary_ids: set[str],
    source_ids: set[str],
    claim_ids: set[str],
    media_ids: set[str],
) -> tuple[str, set[str]]:
    require_fields(
        payload,
        {
            "$schema", "schema_version", "id", "course_id", "order", "slug", "title", "status", "purpose",
            "prerequisite_unit_ids", "course_learning_outcome_ids", "learning_outcomes", "topics",
            "examples", "activities", "assessment_file", "glossary_entry_ids", "source_ids",
            "claim_ids", "media_ids", "common_errors", "biomedical_connections", "editorial_notice",
        },
        report,
        location,
    )
    unit_id = require_nonempty_text(payload, "id", report, location)
    match = UNIT_ID_RE.fullmatch(unit_id)
    if not match or match.group("code") != code or int(match.group("number")) != payload.get("order"):
        report.error(f"{location}.id", "no coincide con code y order")
    if payload.get("course_id") != course_id:
        report.error(f"{location}.course_id", "no coincide con course.json")
    if payload.get("$schema") != "../../../../schemas/academic/unit-v1.schema.json":
        report.error(f"{location}.$schema", "referencia de esquema inconsistente")
    validate_status(payload.get("status"), report, f"{location}.status")
    require_nonempty_text(payload, "purpose", report, location)

    prerequisites = set(text_list(payload.get("prerequisite_unit_ids"), report, f"{location}.prerequisite_unit_ids"))
    for prerequisite in sorted(prerequisites - all_unit_ids):
        report.error(f"{location}.prerequisite_unit_ids", f"unidad inexistente {prerequisite}")
    if unit_id in prerequisites:
        report.error(f"{location}.prerequisite_unit_ids", "una unidad no puede ser prerrequisito de sí misma")
    mapped_course_outcomes = set(text_list(payload.get("course_learning_outcome_ids"), report, f"{location}.course_learning_outcome_ids", minimum=1))
    for outcome_id in sorted(mapped_course_outcomes - course_outcomes):
        report.error(f"{location}.course_learning_outcome_ids", f"resultado de curso inexistente {outcome_id}")
    local_outcomes = record_ids(payload.get("learning_outcomes"), report, f"{location}.learning_outcomes", minimum=1)

    seen_content_ids: set[str] = set()
    topics = dict_list(payload.get("topics"), report, f"{location}.topics", minimum=1)
    for topic_index, topic in enumerate(topics):
        topic_location = f"{location}.topics[{topic_index}]"
        topic_id = require_nonempty_text(topic, "id", report, topic_location)
        require_nonempty_text(topic, "title", report, topic_location)
        if "key_points" in topic:
            text_list(topic.get("key_points"), report, f"{topic_location}.key_points", minimum=1)
        if topic_id in seen_content_ids:
            report.error(f"{topic_location}.id", f"identificador duplicado {topic_id}")
        seen_content_ids.add(topic_id)
        blocks = dict_list(topic.get("blocks"), report, f"{topic_location}.blocks")
        for block_index, block in enumerate(blocks):
            block_location = f"{topic_location}.blocks[{block_index}]"
            block_id = require_nonempty_text(block, "id", report, block_location)
            if block_id in seen_content_ids:
                report.error(f"{block_location}.id", f"identificador duplicado {block_id}")
            seen_content_ids.add(block_id)
            if block.get("type") != "equation" or not str(block.get("latex") or "").strip():
                report.error(block_location, "el bloque de tema debe ser una ecuación con LaTeX")
            report.counts["equations"] += 1
        subtopics = dict_list(topic.get("subtopics"), report, f"{topic_location}.subtopics", minimum=1)
        for subtopic_index, subtopic in enumerate(subtopics):
            sub_location = f"{topic_location}.subtopics[{subtopic_index}]"
            subtopic_id = require_nonempty_text(subtopic, "id", report, sub_location)
            require_nonempty_text(subtopic, "title", report, sub_location)
            if subtopic_id in seen_content_ids:
                report.error(f"{sub_location}.id", f"identificador duplicado {subtopic_id}")
            seen_content_ids.add(subtopic_id)
            paragraph_blocks = dict_list(subtopic.get("blocks"), report, f"{sub_location}.blocks", minimum=1)
            for block_index, block in enumerate(paragraph_blocks):
                block_location = f"{sub_location}.blocks[{block_index}]"
                block_id = require_nonempty_text(block, "id", report, block_location)
                if block_id in seen_content_ids:
                    report.error(f"{block_location}.id", f"identificador duplicado {block_id}")
                seen_content_ids.add(block_id)
                if block.get("type") != "paragraph" or not str(block.get("text") or "").strip():
                    report.error(block_location, "el subtema requiere bloques paragraph con texto")
                report.counts["paragraphs"] += 1
            report.counts["subtopics"] += 1
        report.counts["topics"] += 1

    examples = dict_list(payload.get("examples"), report, f"{location}.examples", minimum=1)
    activities = dict_list(payload.get("activities"), report, f"{location}.activities", minimum=1)
    report.counts["examples"] += len(examples)
    report.counts["activities"] += len(activities)
    for index, activity in enumerate(activities):
        activity_location = f"{location}.activities[{index}]"
        for field_name in ("id", "title", "purpose"):
            require_nonempty_text(activity, field_name, report, activity_location)
        text_list(activity.get("instructions"), report, f"{activity_location}.instructions", minimum=1)
        text_list(activity.get("tasks"), report, f"{activity_location}.tasks", minimum=1)
        text_list(activity.get("checking_criteria"), report, f"{activity_location}.checking_criteria", minimum=1)
        if not as_nonempty_list(activity.get("deliverables")):
            report.gap(f"{activity_location}.deliverables", "falta producto esperado explícito")
        if activity.get("estimated_duration_minutes") is None:
            report.gap(f"{activity_location}.estimated_duration_minutes", "duración aún no estimada")

    for field_name, known_ids in (
        ("glossary_entry_ids", glossary_ids),
        ("source_ids", source_ids),
        ("claim_ids", claim_ids),
        ("media_ids", media_ids),
    ):
        for record_id in text_list(payload.get(field_name), report, f"{location}.{field_name}"):
            if record_id not in known_ids:
                report.error(f"{location}.{field_name}", f"identificador inexistente {record_id}")

    assessment_relative = str(payload.get("assessment_file") or "")
    assessment_path = safe_child(course_dir, assessment_relative, report, f"{location}.assessment_file")
    assessment = load_json(assessment_path, report, assessment_relative)
    if assessment:
        validate_assessment(
            assessment,
            report,
            assessment_relative,
            course_id=course_id,
            unit_id=unit_id,
            learning_outcomes=local_outcomes,
            source_ids=source_ids,
        )
    report.counts["units"] += 1
    return unit_id, mapped_course_outcomes


def validate_course_directory(course_dir: Path) -> Report:
    course_id = course_dir.name
    report = Report(course_id)
    course = load_json(course_dir / "course.json", report, "course.json")
    if not course:
        return report
    require_fields(
        course,
        {
            "$schema", "schema_version", "id", "code", "area_id", "title", "language", "content_version",
            "academic_level", "audience", "status", "purpose", "scope", "prerequisites",
            "competencies", "learning_outcomes", "core_source_ids", "unit_files", "assessment_files", "registries", "static_site",
        },
        report,
        "course.json",
    )
    if course.get("schema_version") != "1.0":
        report.error("course.json.schema_version", "debe ser 1.0")
    if course.get("$schema") != "../../../schemas/academic/course-v1.schema.json":
        report.error("course.json.$schema", "referencia de esquema inconsistente")
    if course.get("id") != course_id or not COURSE_ID_RE.fullmatch(course_id):
        report.error("course.json.id", "debe coincidir con el directorio y usar un slug estable")
    code = str(course.get("code") or "")
    if not CODE_RE.fullmatch(code):
        report.error("course.json.code", "código estable inválido")
    validate_status(course.get("status"), report, "course.json.status")
    require_nonempty_text(course, "purpose", report, "course.json")
    record_ids(course.get("prerequisites"), report, "course.json.prerequisites")
    record_ids(course.get("competencies"), report, "course.json.competencies", minimum=1)
    course_outcomes = record_ids(course.get("learning_outcomes"), report, "course.json.learning_outcomes", minimum=1)
    registries = course.get("registries")
    if not isinstance(registries, dict):
        report.error("course.json.registries", "debe ser un objeto")
        registries = {}

    glossary = load_json(safe_child(course_dir, str(registries.get("glossary") or ""), report, "course.json.registries.glossary"), report, "glossary.json")
    sources = load_json(safe_child(course_dir, str(registries.get("sources") or ""), report, "course.json.registries.sources"), report, "sources.json")
    claims = load_json(safe_child(course_dir, str(registries.get("claims") or ""), report, "course.json.registries.claims"), report, "claims.json")
    media = load_json(safe_child(course_dir, str(registries.get("media") or ""), report, "course.json.registries.media"), report, "media.json")
    for name, payload in (("glossary.json", glossary), ("sources.json", sources), ("claims.json", claims), ("media.json", media)):
        if payload and payload.get("course_id") != course_id:
            report.error(f"{name}.course_id", "no coincide con course.json")
        if payload and payload.get("$schema") != "../../../schemas/academic/registry-v1.schema.json":
            report.error(f"{name}.$schema", "referencia de esquema inconsistente")

    glossary_records = indexed_records(glossary, "entries", report, "glossary.json") if glossary else {}
    source_records = indexed_records(sources, "sources", report, "sources.json") if sources else {}
    claim_records = indexed_records(claims, "claims", report, "claims.json") if claims else {}
    media_records = indexed_records(media, "items", report, "media.json") if media else {}
    report.counts.update(
        glossary_entries=len(glossary_records),
        sources=len(source_records),
        claims=len(claim_records),
        media=len(media_records),
    )
    for source_id in text_list(course.get("core_source_ids"), report, "course.json.core_source_ids", minimum=1):
        if source_id not in source_records:
            report.error("course.json.core_source_ids", f"fuente inexistente {source_id}")
    for source_id, source in source_records.items():
        verification_status = str(source.get("verification_status") or "").strip()
        if not verification_status:
            report.gap(f"sources.json.sources[{source_id}]", "estado de verificación no declarado")
        elif verification_status == "unverified":
            report.gap(f"sources.json.sources[{source_id}]", "fuente aún no verificada")
    if not claim_records:
        report.gap("claims.json.claims", "sin afirmaciones centrales trazadas")
    for glossary_id, entry in glossary_records.items():
        if entry.get("verification_status") == "unverified" or not entry.get("source_ids"):
            report.gap(f"glossary.json.entries[{glossary_id}]", "definición sin fuente exacta verificada")

    unit_files = text_list(course.get("unit_files"), report, "course.json.unit_files", minimum=1)
    if len(unit_files) != len(set(unit_files)):
        report.error("course.json.unit_files", "contiene rutas duplicadas")
    unit_preloads: list[tuple[str, dict[str, Any]]] = []
    all_unit_ids: set[str] = set()
    for relative in unit_files:
        unit = load_json(safe_child(course_dir, relative, report, f"course.json.unit_files[{relative}]"), report, relative)
        if unit:
            unit_preloads.append((relative, unit))
            unit_id = str(unit.get("id") or "")
            if unit_id in all_unit_ids:
                report.error(f"{relative}.id", f"unidad duplicada {unit_id}")
            all_unit_ids.add(unit_id)

    mapped_course_outcomes: set[str] = set()
    canonical_text_by_unit: dict[str, str] = {}
    for relative, unit in unit_preloads:
        _, mapped = validate_unit(
            unit,
            report,
            relative,
            course_dir=course_dir,
            course_id=course_id,
            code=code,
            course_outcomes=course_outcomes,
            all_unit_ids=all_unit_ids,
            glossary_ids=set(glossary_records),
            source_ids=set(source_records),
            claim_ids=set(claim_records),
            media_ids=set(media_records),
        )
        mapped_course_outcomes.update(mapped)
        canonical_text_by_unit[str(unit.get("id") or "")] = " ".join(collect_strings(unit))
    for outcome_id in sorted(course_outcomes - mapped_course_outcomes):
        report.error("course.json.learning_outcomes", f"resultado sin cobertura en unidades: {outcome_id}")

    for claim_id, claim in claim_records.items():
        unit_id = str(claim.get("unit_id") or "")
        source_id = str(claim.get("source_id") or "")
        text = str(claim.get("text") or "").strip()
        if unit_id not in all_unit_ids:
            report.error(f"claims.json.claims[{claim_id}].unit_id", f"unidad inexistente {unit_id}")
        if source_id and source_id not in source_records:
            report.error(f"claims.json.claims[{claim_id}].source_id", f"fuente inexistente {source_id}")
        if text and text not in canonical_text_by_unit.get(unit_id, ""):
            report.error(f"claims.json.claims[{claim_id}].text", "la afirmación no aparece literalmente en la unidad canónica")

    for media_id, item in media_records.items():
        unit_id = str(item.get("unit_id") or "")
        if unit_id not in all_unit_ids:
            report.error(f"media.json.items[{media_id}].unit_id", f"unidad inexistente {unit_id}")
        if item.get("status") == "planned":
            report.gap(
                f"media.json.items[{media_id}]",
                "recurso multimedia planificado, aún no producido",
                category="multimedia",
            )

    assessment_files = text_list(course.get("assessment_files"), report, "course.json.assessment_files", minimum=1)
    referenced_unit_assessments = {str(unit.get("assessment_file") or "") for _, unit in unit_preloads}
    for relative in referenced_unit_assessments - set(assessment_files):
        report.error("course.json.assessment_files", f"falta la evaluación de unidad {relative}")
    course_assessment_paths = []
    for relative in assessment_files:
        payload = load_json(safe_child(course_dir, relative, report, f"course.json.assessment_files[{relative}]"), report, relative)
        if payload.get("scope") == "course":
            course_assessment_paths.append((relative, payload))
    if len(course_assessment_paths) != 1:
        report.error("course.json.assessment_files", "debe existir exactamente una evaluación de alcance course")
    elif course_assessment_paths:
        validate_course_assessment(course_assessment_paths[0][1], report, course_assessment_paths[0][0], course_id)

    authored_text = " ".join(collect_strings([course, *[unit for _, unit in unit_preloads]])).casefold()
    for marker in GENERIC_MARKERS:
        if marker in authored_text:
            report.error("contenido", f"marcador genérico detectado: {marker}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida el corpus académico canónico.")
    parser.add_argument("--course", action="append", default=[], help="Valida solo este course_id; puede repetirse.")
    parser.add_argument(
        "--strict-content",
        action="store_true",
        help="Exige cerrar brechas de contenido, fuentes, actividades y evaluación; permite diferir multimedia.",
    )
    parser.add_argument("--strict-academic", action="store_true", help="Convierte brechas académicas explícitas en errores.")
    args = parser.parse_args()

    requested = set(args.course)
    directories = sorted(path for path in COURSE_ROOT.iterdir() if path.is_dir()) if COURSE_ROOT.exists() else []
    if requested:
        directories = [path for path in directories if path.name in requested]
        missing = sorted(requested - {path.name for path in directories})
        if missing:
            print("Cursos canónicos inexistentes: " + ", ".join(missing))
            return 1
    if not directories:
        print("No hay cursos académicos canónicos.")
        return 0

    reports = [validate_course_directory(path) for path in directories]
    errors = [error for report in reports for error in report.errors]
    gaps = [gap for report in reports for gap in report.gaps]
    multimedia_gaps = [gap for report in reports for gap in report.multimedia_gaps]
    if args.strict_content:
        errors.extend("BRECHA DE CONTENIDO " + gap for gap in gaps)
    if args.strict_academic:
        errors.extend("BRECHA " + gap for gap in gaps)
        errors.extend("BRECHA MULTIMEDIA " + gap for gap in multimedia_gaps)

    for report in reports:
        counts = " · ".join(f"{key}={value}" for key, value in sorted(report.counts.items()))
        print(
            f"{report.course_id}: {counts} · brechas_contenido={len(report.gaps)} · "
            f"brechas_multimedia={len(report.multimedia_gaps)}"
        )
    if gaps and not (args.strict_content or args.strict_academic):
        print(f"Brechas de contenido explícitas: {len(gaps)} (use --strict-content para exigir su cierre)")
    if multimedia_gaps and not args.strict_academic:
        print(f"Brechas multimedia diferibles: {len(multimedia_gaps)} (use --strict-academic para exigir su cierre)")
    if errors:
        print("\n".join(errors))
        print(f"Validación canónica fallida: {len(errors)} error(es)")
        return 1
    print(f"Cursos canónicos estructuralmente válidos: {len(reports)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
