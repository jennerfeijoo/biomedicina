#!/usr/bin/env python3
"""Validate the complete authoral draft of Bioinstrumentation Unit 1."""
from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from typing import Any

from build_bioinstrumentation_u1_authoral_unit import (
    DEFAULT_OUTPUT,
    DEFAULT_SOURCE,
    EXPECTED_FILES,
    BuildError,
    build_unit,
    canonical_bytes,
)

ROOT = Path(__file__).resolve().parents[1]
PREPARATION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-01.json"
PRACTICE_PATH = ROOT / "data" / "practice_implementations" / "bioinstrumentacion-unit-01.json"
ASSESSMENT_PATH = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-01.json"
FEEDBACK_PATH = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-01-feedback.json"
AUTHORIZATION_PATH = ROOT / "data" / "authoring_authorizations" / "bioinstrumentacion-unit-01-provisional.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
READINESS_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01" / "AUTHORING_READINESS.md"
IMPLEMENTATION_DOC = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01" / "AUTHORAL_UNIT_IMPLEMENTATION.md"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)

EXPECTED_REQUIRED = {
    "schema_version", "subject_id", "area_id", "unit", "slug", "title", "status",
    "purpose", "central_question", "prerequisite_recovery", "learning_objectives",
    "theory_sections", "conceptual_model", "glossary", "worked_examples",
    "guided_activities", "common_errors", "self_assessment", "biomedical_connections",
    "executable_practices", "assessment_alignment", "feedback_and_recovery", "sources",
    "authoring_traceability", "review_state", "editorial_notice",
}
EXPECTED_ASSESSMENTS = {"U1-A1", "U1-A2", "U1-A3", "U1-A4", "U1-A5"}
EXPECTED_PRACTICES = {"thermal-synthetic", "physionet-header-audit"}
EXPECTED_EXAMPLE_PREFIXES = {
    "Ejemplo 1 — Cadena térmica",
    "Ejemplo 2 — Registro ECG 100",
    "Ejemplo 3 — Presión arterial",
}


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def words(value: Any) -> int:
    return len(WORD_RE.findall(str(value or "")))


def normalized(value: Any) -> str:
    return " ".join(str(value or "").split()).casefold()


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} is insufficient")
    return text


def validate_identity(unit: dict[str, Any]) -> None:
    expected = {
        "schema_version": "2.0",
        "subject_id": "bioinstrumentacion",
        "area_id": "ingenieria-biomedica",
        "unit": 1,
        "slug": "mensurando-sistema-medicion-trazabilidad",
        "title": "Mensurando, sistema de medición y cadena de trazabilidad",
        "status": "review",
    }
    if set(unit) != EXPECTED_REQUIRED:
        raise ValueError(
            f"authoral unit top-level schema mismatch; missing={sorted(EXPECTED_REQUIRED-set(unit))}, "
            f"extra={sorted(set(unit)-EXPECTED_REQUIRED)}"
        )
    for field, value in expected.items():
        if unit.get(field) != value:
            raise ValueError(f"unexpected {field}: {unit.get(field)!r}")
    require_text(unit.get("purpose"), "purpose", 180)
    question = require_text(unit.get("central_question"), "central_question", 80)
    if not question.startswith("¿") or not question.endswith("?"):
        raise ValueError("central question must be an explicit question")
    for forbidden in ("estimated_hours", "weeks", "clinical_recommendation"):
        if forbidden in unit:
            raise ValueError(f"forbidden top-level field: {forbidden}")


def validate_alignment(unit: dict[str, Any]) -> None:
    preparation = load_object(PREPARATION_PATH)
    if unit["title"] != preparation.get("title") or unit["central_question"] != preparation.get("central_question"):
        raise ValueError("authoral identity is not aligned with the preparation contract")
    objectives = unit.get("learning_objectives")
    if not isinstance(objectives, list) or len(objectives) != 5:
        raise ValueError("exactly five learning objectives are required")
    objective_text = " ".join(map(str, objectives)).casefold()
    for marker in ("mensurando", "indicación", "cadena", "modelo", "trazabilidad"):
        if marker not in objective_text:
            raise ValueError(f"learning objectives do not cover {marker}")
    recovery = unit.get("prerequisite_recovery")
    if not isinstance(recovery, list) or len(recovery) != 3:
        raise ValueError("exactly three prerequisite recovery routes are required")
    for index, item in enumerate(recovery, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"prerequisite recovery {index} is invalid")
        for field in ("topic", "diagnostic_prompt", "recovery"):
            require_text(item.get(field), f"prerequisite_recovery[{index}].{field}", 20)


def validate_theory(unit: dict[str, Any]) -> int:
    sections = unit.get("theory_sections")
    if not isinstance(sections, list) or len(sections) != 6:
        raise ValueError("exactly six theory sections are required")
    seen_headings: set[str] = set()
    seen_paragraphs: set[str] = set()
    seen_points: set[str] = set()
    total = 0
    for section_number, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            raise ValueError(f"theory section {section_number} is invalid")
        heading = require_text(section.get("heading"), f"section {section_number} heading", 20)
        if not heading.startswith(f"{section_number}."):
            raise ValueError(f"section {section_number} heading is not ordered")
        if normalized(heading) in seen_headings:
            raise ValueError("duplicated theory heading")
        seen_headings.add(normalized(heading))
        paragraphs = section.get("paragraphs")
        points = section.get("key_points")
        equations = section.get("equations")
        links = section.get("source_links")
        if not isinstance(paragraphs, list) or len(paragraphs) != 4:
            raise ValueError(f"section {section_number} must contain exactly four paragraphs")
        if not isinstance(points, list) or len(points) != 4:
            raise ValueError(f"section {section_number} must contain exactly four key points")
        if not isinstance(equations, list) or not equations:
            raise ValueError(f"section {section_number} lacks formalization")
        if not isinstance(links, list) or len(links) < 2:
            raise ValueError(f"section {section_number} lacks localized source links")
        for paragraph_number, paragraph in enumerate(paragraphs, start=1):
            count = words(paragraph)
            if count < 70:
                raise ValueError(f"section {section_number} paragraph {paragraph_number} has only {count} words")
            total += count
            key = normalized(paragraph)
            if key in seen_paragraphs:
                raise ValueError("duplicated theory paragraph")
            seen_paragraphs.add(key)
        for point in points:
            if words(point) < 8:
                raise ValueError(f"section {section_number} has an underspecified key point")
            key = normalized(point)
            if key in seen_points:
                raise ValueError("duplicated key point")
            seen_points.add(key)
        for equation in equations:
            if not isinstance(equation, dict):
                raise ValueError(f"section {section_number} equation is invalid")
            require_text(equation.get("latex"), f"section {section_number} equation latex", 4)
            require_text(equation.get("meaning"), f"section {section_number} equation meaning", 40)
    if total < 2200:
        raise ValueError(f"theory is insufficient: {total} words; minimum 2200")
    return total


def validate_concepts_and_examples(unit: dict[str, Any]) -> None:
    model = unit.get("conceptual_model")
    if not isinstance(model, dict) or len(model.get("layers", [])) != 10:
        raise ValueError("conceptual model must preserve ten functional layers")
    for field in ("reading_rule", "visual_accessibility"):
        require_text(model.get(field), f"conceptual_model.{field}", 60)
    if len(model.get("forbidden_shortcuts", [])) < 4:
        raise ValueError("conceptual model does not block the required shortcuts")

    glossary = unit.get("glossary")
    if not isinstance(glossary, list) or len(glossary) != 20:
        raise ValueError("exactly twenty glossary terms are required")
    terms = [normalized(item.get("term")) for item in glossary if isinstance(item, dict)]
    if len(terms) != 20 or len(set(terms)) != 20:
        raise ValueError("glossary terms are invalid or duplicated")
    for item in glossary:
        require_text(item.get("definition"), f"glossary {item.get('term')}", 50)

    examples = unit.get("worked_examples")
    if not isinstance(examples, list) or len(examples) != 3:
        raise ValueError("exactly three worked examples are required")
    prefixes = {next((p for p in EXPECTED_EXAMPLE_PREFIXES if str(example.get("title", "")).startswith(p)), "") for example in examples}
    if prefixes != EXPECTED_EXAMPLE_PREFIXES:
        raise ValueError("worked examples do not cover thermal, ECG and pressure cases")
    for index, example in enumerate(examples, start=1):
        require_text(example.get("scenario"), f"example {index} scenario", 120)
        if len(example.get("reasoning_steps", [])) < 6:
            raise ValueError(f"example {index} lacks stepwise reasoning")
        require_text(example.get("interpretation"), f"example {index} interpretation", 100)
        if len(example.get("limitations", [])) < 3:
            raise ValueError(f"example {index} lacks limitations")


def validate_assessment_and_recovery(unit: dict[str, Any]) -> None:
    activities = unit.get("guided_activities")
    if not isinstance(activities, list) or {item.get("id") for item in activities if isinstance(item, dict)} != EXPECTED_ASSESSMENTS:
        raise ValueError("guided activities must be exactly U1-A1 through U1-A5")
    for activity in activities:
        if len(activity.get("instructions", [])) < 3:
            raise ValueError(f"{activity.get('id')} lacks instructions")
        task_count = sum(len(activity.get(field, [])) for field in ("tasks", "problems"))
        if task_count < 3:
            raise ValueError(f"{activity.get('id')} lacks substantive tasks")
        if len(activity.get("deliverables", [])) < 2 or len(activity.get("checking_criteria", [])) < 3:
            raise ValueError(f"{activity.get('id')} lacks deliverables or checking criteria")

    alignment = unit.get("assessment_alignment")
    if not isinstance(alignment, list) or {item.get("id") for item in alignment if isinstance(item, dict)} != EXPECTED_ASSESSMENTS:
        raise ValueError("assessment alignment must be exactly U1-A1 through U1-A5")
    if {item.get("type") for item in alignment} != {"machine_scored", "human_rubric"}:
        raise ValueError("assessment scoring modes are incomplete")

    feedback_bank = load_object(FEEDBACK_PATH).get("feedback")
    if not isinstance(feedback_bank, dict) or len(feedback_bank) != 13:
        raise ValueError("feedback bank must contain exactly thirteen misconceptions")
    errors = unit.get("common_errors")
    if not isinstance(errors, list):
        raise ValueError("common_errors is missing")
    error_ids = {item.get("id") for item in errors if isinstance(item, dict)}
    if error_ids != set(feedback_bank):
        raise ValueError("common errors are not an exact mirror of the misconception bank")
    for item in errors:
        require_text(item.get("error"), f"common error {item.get('id')}", 30)
        require_text(item.get("correction"), f"common correction {item.get('id')}", 50)

    feedback = unit.get("feedback_and_recovery")
    if not isinstance(feedback, dict):
        raise ValueError("feedback and recovery contract is missing")
    if feedback.get("misconception_bank") != str(FEEDBACK_PATH.relative_to(ROOT)):
        raise ValueError("feedback bank path is incorrect")
    if set(feedback.get("release_policy", {})) != {"attempt_1", "attempt_2", "attempt_3_plus"}:
        raise ValueError("progressive feedback release is incomplete")
    if len(feedback.get("prohibited", [])) < 4:
        raise ValueError("answer-revealing feedback is not sufficiently blocked")

    self_assessment = unit.get("self_assessment")
    if not isinstance(self_assessment, list) or len(self_assessment) != 12:
        raise ValueError("exactly twelve self-assessment questions are required")
    for index, item in enumerate(self_assessment, start=1):
        require_text(item.get("question"), f"self assessment {index} question", 20)
        require_text(item.get("answer"), f"self assessment {index} answer", 25)


def validate_practices_sources_and_limits(unit: dict[str, Any]) -> None:
    practices = unit.get("executable_practices")
    if not isinstance(practices, list) or {item.get("id") for item in practices if isinstance(item, dict)} != EXPECTED_PRACTICES:
        raise ValueError("executable practices must be thermal-synthetic and physionet-header-audit")
    contract_ids = {item.get("id") for item in load_object(PRACTICE_PATH).get("practices", [])}
    if contract_ids != EXPECTED_PRACTICES:
        raise ValueError("practice implementation contract changed")
    for practice in practices:
        if practice.get("network_required") is not False or practice.get("human_data") is not False:
            raise ValueError(f"{practice.get('id')} violates offline/no-human-data boundaries")
        entrypoint = ROOT / str(practice.get("entrypoint"))
        if not entrypoint.is_file():
            raise ValueError(f"practice entrypoint is missing: {entrypoint.relative_to(ROOT)}")
        require_text(practice.get("safety_limit"), f"practice {practice.get('id')} safety limit", 60)

    connections = unit.get("biomedical_connections")
    if not isinstance(connections, list) or len(connections) != 5:
        raise ValueError("exactly five bounded biomedical connections are required")
    for index, connection in enumerate(connections, start=1):
        for field in ("topic", "connection", "mechanism", "limit"):
            require_text(connection.get(field), f"biomedical connection {index} {field}", 20)

    sources = unit.get("sources")
    if not isinstance(sources, list) or len(sources) != 8:
        raise ValueError("exactly eight localized sources are required")
    source_ids: set[str] = set()
    for source in sources:
        source_id = require_text(source.get("id"), "source id", 3)
        if source_id in source_ids:
            raise ValueError(f"duplicated source: {source_id}")
        source_ids.add(source_id)
        if source.get("verification_status") != "verified_directly":
            raise ValueError(f"source is not directly verified: {source_id}")
        if not str(source.get("url", "")).startswith("https://"):
            raise ValueError(f"source URL is invalid: {source_id}")
        if not isinstance(source.get("locators"), list) or not source["locators"]:
            raise ValueError(f"source lacks locators: {source_id}")
        require_text(source.get("role"), f"source role {source_id}", 40)

    full_text = json.dumps(unit, ensure_ascii=False).casefold()
    for prohibited in ("consulte a su médico", "debe tomar", "dosis recomendada", "diagnóstico definitivo"):
        if prohibited in full_text:
            raise ValueError(f"clinical recommendation marker detected: {prohibited}")
    for required_limit in (
        "no constituye respaldo profesional externo",
        "publicación",
        "validación clínica",
        "pending_human_review",
    ):
        if required_limit.casefold() not in full_text:
            raise ValueError(f"editorial or clinical limit is missing: {required_limit}")


def validate_repository_state(unit: dict[str, Any]) -> None:
    trace = unit.get("authoring_traceability")
    expected_trace = {
        "preparation_contract": str(PREPARATION_PATH.relative_to(ROOT)),
        "blocker_resolution": "data/unit_preparation/bioinstrumentacion-unit-01-blocker-resolution.json",
        "practice_contract": str(PRACTICE_PATH.relative_to(ROOT)),
        "assessment_contract": str(ASSESSMENT_PATH.relative_to(ROOT)),
        "feedback_bank": str(FEEDBACK_PATH.relative_to(ROOT)),
        "provisional_authorization": str(AUTHORIZATION_PATH.relative_to(ROOT)),
    }
    if trace != expected_trace:
        raise ValueError("authoring traceability paths are incorrect")

    review = unit.get("review_state")
    expected_review = {
        "internal_authoring_review": "implemented",
        "technical_practices": "implemented_and_ci_validated",
        "closed_assessment": "implemented_and_ci_validated",
        "external_professional_review": "pending_human_review",
        "cognitive_test": "pending_human_execution",
        "inter_rater_round": "pending_human_execution",
        "public_release": False,
        "unit_developed": False,
        "course_state": "pending",
    }
    if review != expected_review:
        raise ValueError("authoral review state is incorrect")

    authorization = load_object(AUTHORIZATION_PATH)
    if authorization.get("status") != "authorized_for_controlled_drafting_provisionally":
        raise ValueError("provisional drafting authorization is missing")
    if authorization.get("authorized_scope", {}).get("create_authoral_unit_draft") is not True:
        raise ValueError("authorization does not permit an authoral unit draft")

    package = load_object(PACKAGE_PATH)
    if package.get("authoral_unit_workstream") != "unit_01_authoral_draft_review":
        raise ValueError("package authoral workstream is not synchronized")
    package_unit = package.get("authoral_unit")
    if not isinstance(package_unit, dict):
        raise ValueError("package authoral unit section is missing")
    if package_unit.get("status") != "authored_internal_review_pending_external_verification":
        raise ValueError("package authoral unit status is incorrect")
    if package_unit.get("public_release_authorized") is not False or package_unit.get("unit_developed") is not False:
        raise ValueError("package prematurely promotes the unit")
    if package_unit.get("course_state") != "pending":
        raise ValueError("package changed the course state")

    statuses = load_object(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentation was promoted prematurely")

    readiness = READINESS_PATH.read_text(encoding="utf-8")
    for marker in (
        "Borrador autoral completo",
        "La evidencia humana continúa pendiente",
        "curso permanece `pending`",
        "publicación continúa bloqueada",
    ):
        if marker not in readiness:
            raise ValueError(f"AUTHORING_READINESS lacks marker: {marker}")
    implementation = IMPLEMENTATION_DOC.read_text(encoding="utf-8")
    for marker in (
        "2.200 palabras teóricas",
        "U1-A1",
        "thermal-synthetic",
        "pending_human_review",
        "no publica la unidad",
    ):
        if marker not in implementation:
            raise ValueError(f"AUTHORAL_UNIT_IMPLEMENTATION lacks marker: {marker}")


def validate_canonical(unit: dict[str, Any]) -> None:
    expected = canonical_bytes(unit)
    if not DEFAULT_OUTPUT.is_file():
        raise ValueError(f"canonical authoral unit is missing: {DEFAULT_OUTPUT.relative_to(ROOT)}")
    if DEFAULT_OUTPUT.read_bytes() != expected:
        raise ValueError("canonical authoral unit is not the deterministic source build")
    loaded = load_object(DEFAULT_OUTPUT)
    if loaded != unit:
        raise ValueError("canonical authoral unit changed after serialization")


def main() -> int:
    try:
        actual_source_files = {path.name for path in DEFAULT_SOURCE.glob("*.json")}
        if actual_source_files != EXPECTED_FILES:
            raise ValueError("authoral source fragment inventory is not exact")
        unit = build_unit(DEFAULT_SOURCE)
        validate_canonical(unit)
        validate_identity(unit)
        validate_alignment(unit)
        theory_words = validate_theory(unit)
        validate_concepts_and_examples(unit)
        validate_assessment_and_recovery(unit)
        validate_practices_sources_and_limits(unit)
        validate_repository_state(unit)
        with tempfile.TemporaryDirectory() as directory:
            copy_path = Path(directory) / "unit-01.json"
            copy_path.write_bytes(canonical_bytes(unit))
            if copy_path.read_bytes() != DEFAULT_OUTPUT.read_bytes():
                raise ValueError("independent deterministic serialization differs")
    except (OSError, ValueError, TypeError, json.JSONDecodeError, BuildError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    print("OK Bioinstrumentation U1 complete authoral draft")
    print(
        f"6 theory sections · {theory_words} theory words · 20 glossary terms · "
        "3 worked examples · 5 aligned assessments · 8 localized sources"
    )
    print("course pending · public release blocked · external professional review pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
