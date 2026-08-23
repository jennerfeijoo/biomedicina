#!/usr/bin/env python3
"""Bootstrap a legacy course into the canonical academic corpus.

This is a one-way bootstrap tool. It refuses to overwrite an existing canonical
course unless ``--force`` is supplied. Once migrated, ``data/courses/<id>`` is
the authoring source and the legacy files are compatibility artifacts only.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import OrderedDict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = ROOT / "data" / "courses"


def load_json(path: Path, *, required: bool = True) -> dict[str, Any]:
    if not path.exists():
        if required:
            raise FileNotFoundError(path)
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.relative_to(ROOT)}: la raíz debe ser un objeto")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "-", ascii_value.casefold()).strip("-")


def stable_source_id(source: dict[str, Any], used: set[str]) -> str:
    explicit = str(source.get("registry_id") or source.get("id") or "").strip()
    base = explicit or slugify(str(source.get("title") or source.get("organization") or "fuente"))
    base = base or "fuente"
    candidate = base
    suffix = 2
    while candidate in used:
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate


def as_dict_list(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def as_text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def record_list(values: Any, prefix: str) -> list[dict[str, str]]:
    return [
        {"id": f"{prefix}{index:02d}", "statement": statement}
        for index, statement in enumerate(as_text_list(values), start=1)
    ]


def locate_subject(subject_id: str) -> tuple[Path, dict[str, Any]]:
    matches = sorted((ROOT / "data" / "subjects").glob(f"*/{subject_id}.json"))
    if len(matches) != 1:
        raise ValueError(f"se esperaba un overlay para {subject_id}; se encontraron {len(matches)}")
    return matches[0], load_json(matches[0])


def normalize_connection(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if not isinstance(value, dict):
        return ""
    title = str(value.get("topic") or value.get("title") or "").strip()
    detail = str(value.get("connection") or value.get("description") or value.get("text") or "").strip()
    return f"{title}: {detail}" if title and detail else title or detail


def build_topics(unit: dict[str, Any], unit_id: str) -> list[dict[str, Any]]:
    topics: list[dict[str, Any]] = []
    for topic_number, section in enumerate(as_dict_list(unit.get("theory_sections")), start=1):
        topic_id = f"{unit_id}-T{topic_number:02d}"
        paragraphs = as_text_list(section.get("paragraphs"))
        key_points = as_text_list(section.get("key_points"))
        subtopics = []
        for subtopic_number, paragraph in enumerate(paragraphs, start=1):
            title = (
                key_points[subtopic_number - 1].rstrip(".")
                if subtopic_number <= len(key_points)
                else f"Desarrollo conceptual {subtopic_number}"
            )
            subtopic_id = f"{topic_id}-ST{subtopic_number:02d}"
            subtopics.append(
                {
                    "id": subtopic_id,
                    "title": title,
                    "blocks": [
                        {
                            "id": f"{subtopic_id}-B01",
                            "type": "paragraph",
                            "text": paragraph,
                        }
                    ],
                }
            )

        blocks = []
        for block_number, equation in enumerate(section.get("equations", []), start=1):
            if isinstance(equation, str):
                equation = {"latex": equation}
            if not isinstance(equation, dict):
                continue
            block = {
                "id": f"{topic_id}-B{block_number:02d}",
                "type": "equation",
                "latex": str(equation.get("latex") or "").strip(),
            }
            label = str(
                equation.get("label") or equation.get("description") or equation.get("meaning") or ""
            ).strip()
            if label:
                block["label"] = label
            if isinstance(equation.get("variables"), dict) and equation["variables"]:
                block["variables"] = equation["variables"]
            blocks.append(block)

        topics.append(
            {
                "id": topic_id,
                "title": str(section.get("heading") or section.get("title") or f"Tema {topic_number}").strip(),
                "blocks": blocks,
                "key_points": key_points,
                "subtopics": subtopics,
            }
        )
    return topics


def build_examples(unit: dict[str, Any], unit_id: str) -> list[dict[str, Any]]:
    examples = as_dict_list(unit.get("worked_examples")) or as_dict_list(unit.get("worked_example"))
    output = []
    for index, example in enumerate(examples, start=1):
        output.append(
            {
                "id": f"{unit_id}-EJ{index:02d}",
                "title": str(example.get("title") or f"Ejemplo {index}").strip(),
                "scenario": str(example.get("scenario") or "").strip(),
                "reasoning_steps": as_text_list(example.get("reasoning_steps")),
                "interpretation": str(example.get("interpretation") or example.get("conclusion") or "").strip(),
                "limitations": as_text_list(example.get("limitations")),
            }
        )
    return output


def build_activities(unit: dict[str, Any], unit_id: str, prerequisites: list[str]) -> list[dict[str, Any]]:
    activities = as_dict_list(unit.get("guided_activities")) or as_dict_list(unit.get("guided_activity"))
    output = []
    for index, activity in enumerate(activities, start=1):
        tasks: list[str] = []
        for key in ("problems", "tasks", "exercises"):
            tasks.extend(as_text_list(activity.get(key)))
        output.append(
            {
                "id": f"{unit_id}-ACT{index:02d}",
                "title": str(activity.get("title") or f"Actividad {index}").strip(),
                "purpose": "Aplicar los resultados de aprendizaje de la unidad mediante un producto documentado y verificable.",
                "prerequisite_unit_ids": prerequisites,
                "instructions": as_text_list(activity.get("instructions")),
                "tasks": tasks,
                "deliverables": as_text_list(activity.get("deliverables")),
                "checking_criteria": as_text_list(activity.get("checking_criteria")),
                "estimated_duration_minutes": None,
                "status": "migrated_requires_pedagogical_review",
            }
        )
    return output


def build_unit_assessment(
    unit: dict[str, Any], unit_id: str, local_outcomes: list[dict[str, str]]
) -> dict[str, Any]:
    items = []
    outcomes = [item["id"] for item in local_outcomes]
    for index, item in enumerate(as_dict_list(unit.get("self_assessment")), start=1):
        linked = [outcomes[(index - 1) % len(outcomes)]] if outcomes else []
        items.append(
            {
                "id": f"{unit_id}-Q{index:02d}",
                "type": "short_answer",
                "prompt": str(item.get("question") or "").strip(),
                "linked_learning_outcome_ids": linked,
                "difficulty": "unclassified",
                "cognitive_level": "unclassified",
                "answer_key": {
                    "expected_answer": str(item.get("answer") or "").strip(),
                    "explanation": str(item.get("reasoning") or item.get("explanation") or "").strip() or None,
                    "common_misconceptions": [str(item["common_error"]).strip()] if item.get("common_error") else [],
                },
                "feedback": {"correct": None, "incorrect": None},
                "source_ids": [],
                "status": "migrated_requires_pedagogical_review",
            }
        )
    return {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{unit_id}-EVAL",
        "course_id": str(unit.get("subject_id") or ""),
        "scope": "unit",
        "unit_id": unit_id,
        "purpose": "Autoevaluación formativa de los resultados de aprendizaje de la unidad.",
        "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
        "items": items,
        "status": "migrated_requires_pedagogical_review",
    }


def migrate(subject_id: str, course_code: str, *, force: bool = False) -> Path:
    course_code = course_code.strip().upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9]{2,11}", course_code):
        raise ValueError("course-code debe contener entre 3 y 12 caracteres ASCII en mayúsculas")

    target = COURSE_ROOT / subject_id
    if target.exists() and not force:
        raise FileExistsError(f"{target.relative_to(ROOT)} ya existe; use --force solo para repetir el bootstrap")

    subject_path, subject = locate_subject(subject_id)
    area_id = subject_path.parent.name
    plan = load_json(ROOT / "data" / "course_plans" / f"{subject_id}.json", required=False)
    generated = load_json(ROOT / "data" / "generated_courses" / f"{subject_id}.json")
    source_registry = load_json(ROOT / "data" / "source_registry" / f"{subject_id}.json", required=False)
    claim_registry = load_json(ROOT / "data" / "claim_registry" / f"{subject_id}.json", required=False)
    legacy_units = sorted((ROOT / "data" / "generated_units" / subject_id).glob("unit-*.json"))
    if not legacy_units:
        raise ValueError(f"{subject_id}: no hay unidades avanzadas para migrar")

    unit_payloads = [load_json(path) for path in legacy_units]
    course_outcomes = record_list(
        generated.get("learning_outcomes") or plan.get("course_learning_outcomes"), f"{course_code}-LO"
    )
    competencies = record_list(
        generated.get("course_competencies") or plan.get("course_competencies"), f"{course_code}-COMP"
    )

    known_sources: OrderedDict[str, dict[str, Any]] = OrderedDict()
    source_keys: dict[tuple[str, str], str] = {}
    used_source_ids: set[str] = set()
    for source in as_dict_list(source_registry.get("sources")):
        source_id = stable_source_id(source, used_source_ids)
        used_source_ids.add(source_id)
        record = dict(source)
        record["id"] = source_id
        record.setdefault("verification_status", "unverified")
        record["used_by_unit_ids"] = []
        known_sources[source_id] = record
        source_keys[(str(source.get("registry_id") or source.get("id") or ""), str(source.get("url") or ""))] = source_id

    glossary_by_term: OrderedDict[str, dict[str, Any]] = OrderedDict()
    unit_outputs: list[dict[str, Any]] = []
    assessment_files: list[str] = []
    media_records: list[dict[str, Any]] = []
    claims_by_unit: dict[int, list[str]] = {}
    for claim in as_dict_list(claim_registry.get("claims")):
        try:
            number = int(claim.get("unit"))
        except (TypeError, ValueError):
            continue
        claims_by_unit.setdefault(number, []).append(str(claim.get("claim_id") or "").strip())

    for unit in unit_payloads:
        number = int(unit["unit"])
        unit_id = f"{course_code}-U{number:02d}"
        prerequisites = [f"{course_code}-U{int(value):02d}" for value in plan.get("units", [])[number - 1].get("prerequisite_units", [])] if len(plan.get("units", [])) >= number else []
        local_outcomes = record_list(unit.get("learning_objectives"), f"{unit_id}-LO")

        unit_source_ids: list[str] = []
        for source in as_dict_list(unit.get("sources")):
            registry_id = str(source.get("registry_id") or source.get("id") or "")
            url = str(source.get("url") or "")
            source_id = source_keys.get((registry_id, url))
            if source_id is None and registry_id:
                source_id = next((key for key in known_sources if key == registry_id), None)
            if source_id is None and url:
                source_id = next(
                    (key for key, record in known_sources.items() if str(record.get("url") or "") == url),
                    None,
                )
            if source_id is None:
                source_id = stable_source_id(source, used_source_ids)
                used_source_ids.add(source_id)
                record = dict(source)
                record["id"] = source_id
                record.setdefault("verification_status", "unverified")
                record["used_by_unit_ids"] = []
                known_sources[source_id] = record
            else:
                record = known_sources[source_id]
                for key, value in source.items():
                    upgrades_unverified = (
                        key == "verification_status"
                        and record.get(key) == "unverified"
                        and value != "unverified"
                    )
                    if value not in (None, "", []) and (not record.get(key) or upgrades_unverified):
                        record[key] = value
            unit_source_ids.append(source_id)
            used_by = known_sources[source_id].setdefault("used_by_unit_ids", [])
            if unit_id not in used_by:
                used_by.append(unit_id)

        glossary_ids = []
        for entry in as_dict_list(unit.get("glossary")):
            term = str(entry.get("term") or entry.get("title") or "").strip()
            definition = str(entry.get("definition") or entry.get("description") or "").strip()
            key = term.casefold()
            if key not in glossary_by_term:
                glossary_id = f"{course_code}-GLO-{len(glossary_by_term) + 1:03d}"
                glossary_by_term[key] = {
                    "id": glossary_id,
                    "term": term,
                    "definition": definition,
                    "unit_ids": [],
                    "source_ids": [],
                    "verification_status": "unverified",
                }
            record = glossary_by_term[key]
            if unit_id not in record["unit_ids"]:
                record["unit_ids"].append(unit_id)
            glossary_ids.append(record["id"])

        assessment_path = f"assessments/unit-{number:02d}.json"
        write_json(target / assessment_path, build_unit_assessment(unit, unit_id, local_outcomes))
        assessment_files.append(assessment_path)
        media_id = f"{unit_id}-MED01"
        media_records.append(
            {
                "id": media_id,
                "type": "figure",
                "status": "planned",
                "unit_id": unit_id,
                "linked_learning_outcome_ids": [item["id"] for item in local_outcomes[:2]],
                "pedagogical_purpose": f"Representar visualmente los conceptos centrales de {str(unit.get('title') or '').strip()}.",
                "alt_text_draft": None,
                "license_requirements": "Usar material propio o con licencia compatible y registrar atribución y procedencia.",
                "source_ids": [],
            }
        )

        output = {
            "$schema": "../../../../schemas/academic/unit-v1.schema.json",
            "schema_version": "1.0",
            "id": unit_id,
            "course_id": subject_id,
            "order": number,
            "slug": str(unit.get("slug") or f"unidad-{number:02d}"),
            "title": str(unit.get("title") or f"Unidad {number}"),
            "status": {
                "content": "in_review",
                "sources": "partial",
                "pedagogy": "in_review",
                "multimedia": "planned",
                "internal_review": "pending",
                "external_review": "pending",
                "publication": "published_provisional",
            },
            "purpose": str(unit.get("purpose") or "").strip(),
            "prerequisite_unit_ids": prerequisites,
            "course_learning_outcome_ids": [course_outcomes[number - 1]["id"]] if len(course_outcomes) >= number else [],
            "learning_outcomes": local_outcomes,
            "topics": build_topics(unit, unit_id),
            "examples": build_examples(unit, unit_id),
            "activities": build_activities(unit, unit_id, prerequisites),
            "assessment_file": assessment_path,
            "glossary_entry_ids": glossary_ids,
            "source_ids": unit_source_ids,
            "claim_ids": [value for value in claims_by_unit.get(number, []) if value],
            "media_ids": [media_id],
            "common_errors": unit.get("common_errors", []),
            "biomedical_connections": [
                text for text in (normalize_connection(item) for item in unit.get("biomedical_connections", [])) if text
            ],
            "editorial_notice": str(unit.get("editorial_notice") or "").strip(),
            "legacy_origin": str((ROOT / "data" / "generated_units" / subject_id / f"unit-{number:02d}.json").relative_to(ROOT)),
        }
        write_json(target / "units" / f"unit-{number:02d}.json", output)
        unit_outputs.append(output)

    core_source_ids: list[str] = []
    for source in as_dict_list(generated.get("core_resources")):
        url = str(source.get("url") or "")
        source_id = next(
            (key for key, record in known_sources.items() if url and str(record.get("url") or "") == url),
            None,
        )
        if source_id is None:
            source_id = stable_source_id(source, used_source_ids)
            used_source_ids.add(source_id)
            record = dict(source)
            record["id"] = source_id
            record.setdefault("verification_status", "unverified")
            record["used_by_unit_ids"] = []
            known_sources[source_id] = record
        if source_id not in core_source_ids:
            core_source_ids.append(source_id)

    glossary_file = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": subject_id,
        "entries": list(glossary_by_term.values()),
        "status": "migrated_requires_source_review",
    }
    write_json(target / "glossary.json", glossary_file)

    sources_file = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": subject_id,
        "source_policy": str(source_registry.get("source_policy") or ""),
        "consulted_on": source_registry.get("consulted_on") or source_registry.get("review_date"),
        "coverage_gaps": source_registry.get("coverage_gaps", []),
        "sources": list(known_sources.values()),
    }
    write_json(target / "sources.json", sources_file)

    canonical_claims = []
    for claim in as_dict_list(claim_registry.get("claims")):
        record = dict(claim)
        record["id"] = str(record.get("claim_id") or "").strip()
        try:
            record["unit_id"] = f"{course_code}-U{int(record.get('unit')):02d}"
        except (TypeError, ValueError):
            record["unit_id"] = None
        canonical_claims.append(record)
    write_json(
        target / "claims.json",
        {
            "$schema": "../../../schemas/academic/registry-v1.schema.json",
            "schema_version": "1.0",
            "course_id": subject_id,
            "content_version": claim_registry.get("content_version"),
            "content_commit": claim_registry.get("content_commit"),
            "scope": claim_registry.get("scope", "Sin registro de afirmaciones centrales."),
            "review_state": claim_registry.get("review_state", "not_started"),
            "claims": canonical_claims,
        },
    )
    write_json(
        target / "media.json",
        {
            "$schema": "../../../schemas/academic/registry-v1.schema.json",
            "schema_version": "1.0",
            "course_id": subject_id,
            "coverage_status": "planned",
            "items": media_records,
        },
    )

    course_assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{course_code}-EVAL-CURSO",
        "course_id": subject_id,
        "scope": "course",
        "principles": generated.get("assessment_principles", []),
        "assessment_plan": generated.get("assessment_plan", []),
        "diagnostic": generated.get("diagnostic_assessment", {}),
        "midterm_blueprint": generated.get("midterm_exam_blueprint", []),
        "capstone": generated.get("final_project", {}),
        "status": "migrated_requires_pedagogical_review",
    }
    write_json(target / "assessments" / "course-assessment.json", course_assessment)

    course = {
        "$schema": "../../../schemas/academic/course-v1.schema.json",
        "schema_version": "1.0",
        "id": subject_id,
        "code": course_code,
        "area_id": area_id,
        "title": str(plan.get("title") or generated.get("title") or subject_id),
        "language": "es",
        "content_version": "0.1.0",
        "academic_level": str(generated.get("academic_level") or "Pregrado universitario"),
        "audience": "Estudiantes de ciencias de la vida, medicina, ingeniería biomédica e investigación aplicada.",
        "status": {
            "content": "in_review",
            "sources": "partial",
            "pedagogy": "in_review",
            "multimedia": "planned",
            "internal_review": "pending",
            "external_review": "pending",
            "publication": "published_provisional",
        },
        "purpose": str(generated.get("course_purpose") or plan.get("course_scope") or ""),
        "scope": plan.get("scope_boundaries", {"included": [], "excluded": [], "handoff_courses": []}),
        "prerequisites": record_list(generated.get("prerequisites") or plan.get("prerequisites"), f"{course_code}-PRE"),
        "competencies": competencies,
        "learning_outcomes": course_outcomes,
        "study_method": generated.get("study_method", []),
        "core_source_ids": core_source_ids,
        "unit_files": [f"units/unit-{int(unit['order']):02d}.json" for unit in unit_outputs],
        "assessment_files": [*assessment_files, "assessments/course-assessment.json"],
        "registries": {
            "glossary": "glossary.json",
            "sources": "sources.json",
            "claims": "claims.json",
            "media": "media.json",
        },
        "static_site": {
            "renderer": "scripts/generate_site.py",
            "canonical_source": True,
            "legacy_mirrors": [
                f"data/generated_courses/{subject_id}.json",
                f"data/generated_units/{subject_id}/",
                f"data/subjects/{area_id}/{subject_id}.json",
                f"data/source_registry/{subject_id}.json",
                f"data/claim_registry/{subject_id}.json",
            ],
        },
        "editorial_notice": str(generated.get("editorial_notice") or ""),
    }
    write_json(target / "course.json", course)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Migra una asignatura al corpus académico canónico.")
    parser.add_argument("--subject", required=True, help="Identificador de la asignatura.")
    parser.add_argument("--course-code", required=True, help="Código estable usado en identificadores internos.")
    parser.add_argument("--force", action="store_true", help="Repite el bootstrap y sobrescribe el destino.")
    args = parser.parse_args()
    target = migrate(args.subject, args.course_code, force=args.force)
    print(f"Curso canónico creado: {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
