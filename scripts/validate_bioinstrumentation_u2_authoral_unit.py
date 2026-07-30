#!/usr/bin/env python3
"""Validate the complete internal authoral draft of Bioinstrumentation Unit 2."""
from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from typing import Any

from build_bioinstrumentation_u2_authoral_unit import (
    DEFAULT_OUTPUT,
    DEFAULT_SOURCE,
    EXPECTED_FILES,
    BuildError,
    build_unit,
    canonical_bytes,
)

ROOT = Path(__file__).resolve().parents[1]
PREPARATION = ROOT / "data/unit_preparation/bioinstrumentacion-unit-02.json"
BLOCKERS = ROOT / "data/unit_preparation/bioinstrumentacion-unit-02-blocker-resolution.json"
PRACTICES = ROOT / "data/practice_implementations/bioinstrumentacion-unit-02.json"
ASSESSMENTS = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-02.json"
FEEDBACK = ROOT / "data/assessment_implementations/bioinstrumentacion-unit-02-feedback.json"
AUTHORIZATION = ROOT / "data/authoring_authorizations/bioinstrumentacion-unit-02-provisional.json"
AUDIT = ROOT / "data/course_audits/bioinstrumentacion/UNIT_02_PRACTICES_ASSESSMENT_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json"
PACKAGE = ROOT / "data/course_plan_packages/package-04-bioinstrumentation-excellence-pilot.json"
STATUSES = ROOT / "data/catalog_statuses.json"
READINESS = ROOT / "docs/pilots/bioinstrumentacion/unit-02/AUTHORING_READINESS.md"
IMPLEMENTATION_DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-02/AUTHORAL_UNIT_IMPLEMENTATION.md"
DECISION = ROOT / "data/review_evidence/bioinstrumentacion-unit-02-disciplinary-review.json"
MANIFEST = ROOT / "data/review_evidence/bioinstrumentacion-unit-02-review-packet.json"

WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)
EXPECTED_TOP = {
    "schema_version", "subject_id", "area_id", "unit", "slug", "title", "status",
    "purpose", "central_question", "prerequisite_recovery", "learning_objectives",
    "theory_sections", "conceptual_model", "glossary", "worked_examples",
    "guided_activities", "common_errors", "self_assessment", "biomedical_connections",
    "executable_practices", "assessment_alignment", "feedback_and_recovery", "sources",
    "authoring_traceability", "review_state", "editorial_notice",
}
ASSESSMENT_IDS = {"U2-A1", "U2-A2", "U2-A3", "U2-A4", "U2-A5"}
PRACTICE_IDS = {"U2-P1", "U2-P2", "U2-P3"}
ERROR_IDS = {
    "sensor-equals-system", "sensor-equals-transducer-always", "higher-sensitivity-is-better",
    "sensitivity-equals-resolution", "static-calibration-covers-dynamics",
    "response-time-equals-time-constant", "fast-means-accurate",
    "linearity-is-intrinsic-global", "hysteresis-is-random-noise",
    "loading-is-negligible", "datasheet-is-system-proof",
    "component-performance-is-clinical-utility",
}
COMPONENTS = {"NTCLG100E2103JB", "CEA-06-125UNA-350", "S5821-03"}


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: Any, label: str, minimum: int = 20) -> str:
    result = str(value or "").strip()
    require(len(result) >= minimum, f"{label} is insufficient")
    return result


def words(value: Any) -> int:
    return len(WORD_RE.findall(str(value or "")))


def validate_identity_and_alignment(unit: dict[str, Any]) -> None:
    require(set(unit) == EXPECTED_TOP, "authoral top-level schema changed")
    expected = {
        "schema_version": "2.0", "subject_id": "bioinstrumentacion",
        "area_id": "ingenieria-biomedica", "unit": 2,
        "slug": "sensores-transductores-modelos-estaticos-dinamicos",
        "title": "Sensores, transductores y modelos estáticos y dinámicos", "status": "review",
    }
    for key, wanted in expected.items():
        require(unit.get(key) == wanted, f"unexpected {key}: {unit.get(key)!r}")
    text(unit.get("purpose"), "purpose", 250)
    question = text(unit.get("central_question"), "central question", 100)
    require(question.startswith("¿") and question.endswith("?"), "central question is not explicit")

    preparation = load(PREPARATION)
    require(unit["title"] == preparation.get("title"), "title differs from preparation")
    require(unit["central_question"] == preparation.get("central_question"), "central question differs")
    outcomes = [row.get("statement") for row in preparation.get("learning_outcomes", []) if isinstance(row, dict)]
    require(unit.get("learning_objectives") == outcomes and len(outcomes) == 5, "learning outcomes differ")
    recovery = unit.get("prerequisite_recovery")
    require(isinstance(recovery, list) and len(recovery) == 3, "three recovery routes required")

    decision = load(BLOCKERS).get("editorial_decision", {})
    require(decision.get("technical_blockers_resolved") is True, "technical blockers are not resolved")
    require(decision.get("full_theory_drafting_authorized") is False, "historical blocker record changed")


def validate_theory(unit: dict[str, Any]) -> int:
    sections = unit.get("theory_sections")
    require(isinstance(sections, list) and len(sections) == 6, "six theory sections required")
    coverage = {
        1: ("sensor", "transductor", "interfaz", "frontera"),
        2: ("sensibilidad", "selectividad", "offset", "dominio"),
        3: ("saturación", "zona muerta", "histéresis", "no linealidad"),
        4: ("carga eléctrica", "térmica", "mecánica", "óptica"),
        5: ("primer orden", "constante de tiempo", "tiempo de respuesta", "retardo"),
        6: ("ancho de banda", "−3 db", "selección", "utilidad clínica"),
    }
    total = 0
    seen: set[str] = set()
    for number, section in enumerate(sections, 1):
        require(isinstance(section, dict), f"section {number} invalid")
        heading = text(section.get("heading"), f"section {number} heading", 25)
        require(heading.startswith(f"{number}."), f"section {number} order invalid")
        paragraphs = section.get("paragraphs")
        points = section.get("key_points")
        equations = section.get("equations")
        links = section.get("source_links")
        require(isinstance(paragraphs, list) and len(paragraphs) == 4, f"section {number} needs four paragraphs")
        require(isinstance(points, list) and len(points) == 4, f"section {number} needs four key points")
        require(isinstance(equations, list) and equations, f"section {number} lacks equations")
        require(isinstance(links, list) and len(links) >= 2, f"section {number} lacks source links")
        joined = " ".join(map(str, paragraphs)).casefold()
        for marker in coverage[number]:
            require(marker in joined, f"section {number} lacks {marker}")
        for index, paragraph in enumerate(paragraphs, 1):
            count = words(paragraph)
            require(count >= 70, f"section {number} paragraph {index} has {count} words")
            normalized = " ".join(str(paragraph).split()).casefold()
            require(normalized not in seen, "duplicated theory paragraph")
            seen.add(normalized)
            total += count
        for equation in equations:
            require(isinstance(equation, dict), f"section {number} equation invalid")
            text(equation.get("latex"), f"section {number} latex", 4)
            text(equation.get("meaning"), f"section {number} equation meaning", 60)
    require(total >= 2200, f"theory has only {total} words")
    return total


def validate_learning_assets(unit: dict[str, Any]) -> None:
    model = unit.get("conceptual_model")
    require(isinstance(model, dict) and len(model.get("layers", [])) == 10, "conceptual model needs ten layers")
    require(len(model.get("forbidden_shortcuts", [])) >= 6, "conceptual shortcuts incomplete")

    glossary = unit.get("glossary")
    require(isinstance(glossary, list) and len(glossary) == 20, "twenty glossary terms required")
    terms = [str(row.get("term", "")).casefold() for row in glossary if isinstance(row, dict)]
    require(len(terms) == 20 and len(set(terms)) == 20, "glossary terms invalid")
    for row in glossary:
        text(row.get("definition"), f"glossary {row.get('term')}", 80)

    examples = unit.get("worked_examples")
    require(isinstance(examples, list) and len(examples) == 3, "three worked examples required")
    example_text = json.dumps(examples, ensure_ascii=False)
    for component in COMPONENTS:
        require(component in example_text, f"worked examples lack {component}")
    for index, example in enumerate(examples, 1):
        text(example.get("scenario"), f"example {index} scenario", 150)
        require(len(example.get("reasoning_steps", [])) >= 6, f"example {index} lacks reasoning")
        require(len(example.get("limitations", [])) >= 3, f"example {index} lacks limitations")

    activities = unit.get("guided_activities")
    require(isinstance(activities, list), "guided activities missing")
    require({row.get("id") for row in activities if isinstance(row, dict)} == ASSESSMENT_IDS, "activity ids changed")
    for row in activities:
        require(len(row.get("instructions", [])) >= 3, f"{row.get('id')} lacks instructions")
        require(len(row.get("tasks", [])) >= 4, f"{row.get('id')} lacks tasks")
        require(len(row.get("deliverables", [])) >= 3, f"{row.get('id')} lacks deliverables")
        require(len(row.get("checking_criteria", [])) >= 3, f"{row.get('id')} lacks criteria")

    errors = unit.get("common_errors")
    require(isinstance(errors, list), "common errors missing")
    require({row.get("id") for row in errors if isinstance(row, dict)} == ERROR_IDS, "misconception set changed")
    feedback = load(FEEDBACK).get("feedback")
    require(isinstance(feedback, dict) and set(feedback) == ERROR_IDS, "feedback bank differs")
    require(isinstance(unit.get("self_assessment"), list) and len(unit["self_assessment"]) == 12, "twelve self-assessment questions required")


def validate_assessment_practice_and_sources(unit: dict[str, Any]) -> None:
    alignment = unit.get("assessment_alignment")
    require(isinstance(alignment, list), "assessment alignment missing")
    require({row.get("id") for row in alignment if isinstance(row, dict)} == ASSESSMENT_IDS, "assessment ids changed")
    types = {row.get("id"): row.get("type") for row in alignment}
    require(types == {"U2-A1": "human_rubric", "U2-A2": "machine_scored", "U2-A3": "machine_scored", "U2-A4": "machine_scored", "U2-A5": "human_rubric"}, "scoring modes changed")
    contract = load(ASSESSMENTS)
    machine_ids = {row.get("id") for row in contract.get("machine_scored_assessments", []) if isinstance(row, dict)}
    human_ids = {row.get("id") for row in contract.get("human_scored_assessments", []) if isinstance(row, dict)}
    require(machine_ids == {"U2-A2", "U2-A3", "U2-A4"} and human_ids == {"U2-A1", "U2-A5"}, "assessment contract changed")
    recovery = unit.get("feedback_and_recovery")
    require(isinstance(recovery, dict) and recovery.get("misconception_bank") == str(FEEDBACK.relative_to(ROOT)), "recovery contract invalid")
    require(set(recovery.get("release_policy", {})) == {"attempt_1", "attempt_2", "attempt_3_plus"}, "feedback release incomplete")
    require(len(recovery.get("prohibited", [])) >= 5, "answer leakage controls incomplete")

    practices = unit.get("executable_practices")
    require(isinstance(practices, list), "executable practices missing")
    require({row.get("id") for row in practices if isinstance(row, dict)} == PRACTICE_IDS, "practice ids changed")
    implemented = {row.get("id") for row in load(PRACTICES).get("practices", []) if isinstance(row, dict)}
    require(implemented == PRACTICE_IDS, "practice contract changed")
    for row in practices:
        require(row.get("network_required") is False and row.get("human_data") is False, f"{row.get('id')} violates data boundary")
        require((ROOT / str(row.get("entrypoint"))).is_file(), f"{row.get('id')} entrypoint missing")
        text(row.get("safety_limit"), f"{row.get('id')} safety limit", 90)

    require(isinstance(unit.get("biomedical_connections"), list) and len(unit["biomedical_connections"]) == 5, "five biomedical connections required")
    sources = unit.get("sources")
    require(isinstance(sources, list) and len(sources) == 12, "twelve sources required")
    source_ids: set[str] = set()
    for row in sources:
        source_id = text(row.get("id"), "source id", 3)
        require(source_id not in source_ids, f"duplicated source {source_id}")
        source_ids.add(source_id)
        require(row.get("verification_status") == "verified_directly", f"unverified source {source_id}")
        require(str(row.get("url", "")).startswith("https://"), f"invalid URL {source_id}")
        require(isinstance(row.get("locators"), list) and row["locators"], f"source {source_id} lacks locators")


def validate_state_and_limits(unit: dict[str, Any]) -> None:
    expected_trace = {
        "preparation_contract": str(PREPARATION.relative_to(ROOT)),
        "blocker_resolution": str(BLOCKERS.relative_to(ROOT)),
        "practice_contract": str(PRACTICES.relative_to(ROOT)),
        "assessment_contract": str(ASSESSMENTS.relative_to(ROOT)),
        "feedback_bank": str(FEEDBACK.relative_to(ROOT)),
        "scientific_editorial_audit": str(AUDIT.relative_to(ROOT)),
        "provisional_authorization": str(AUTHORIZATION.relative_to(ROOT)),
    }
    require(unit.get("authoring_traceability") == expected_trace, "traceability paths changed")
    review = unit.get("review_state", {})
    require(review.get("external_professional_review") == "pending_human_review", "external review state changed")
    require(review.get("cognitive_test") == "pending_human_execution", "cognitive evidence fabricated")
    require(review.get("feedback_usability_review") == "pending_human_execution", "usability evidence fabricated")
    require(review.get("inter_rater_round") == "pending_human_execution", "inter-rater evidence fabricated")
    require(review.get("public_release") is False and review.get("unit_developed") is False and review.get("course_state") == "pending", "editorial state promoted")

    authorization = load(AUTHORIZATION)
    require(authorization.get("status") == "authorized_for_controlled_drafting_provisionally", "authorization missing")
    scope = authorization.get("authorized_scope", {})
    require(scope.get("create_authoral_unit_draft") is True and scope.get("draft_full_theory") is True, "authoring scope incomplete")
    require(authorization.get("review_characterization", {}).get("human_disciplinary_review_completed") is False, "human review fabricated")
    audit = load(AUDIT)
    require(audit.get("status") == "passed_with_corrections_applied", "audit basis invalid")
    require(audit.get("unresolved_critical_findings") == 0 and audit.get("unresolved_major_findings") == 0, "audit findings remain")
    require(len(audit.get("findings", [])) == 6, "audit finding count changed")

    package = load(PACKAGE)
    require(package.get("unit_02_authoral_unit_workstream") == "unit_02_authoral_draft_review", "package workstream missing")
    section = package.get("unit_02_authoral_unit", {})
    require(section.get("status") == "authored_internal_review_pending_external_verification", "package authoral status invalid")
    require(section.get("source_dir") == str(DEFAULT_SOURCE.relative_to(ROOT)), "package source path invalid")
    require(section.get("canonical_unit") == str(DEFAULT_OUTPUT.relative_to(ROOT)), "package canonical path invalid")
    require(section.get("theory_section_count") == 6 and section.get("minimum_theory_words") == 2200, "package theory metrics invalid")
    require(section.get("glossary_term_count") == 20 and section.get("worked_example_count") == 3 and section.get("source_count") == 12, "package metrics invalid")
    require(section.get("public_release_authorized") is False and section.get("unit_developed") is False and section.get("course_state") == "pending", "package promoted unit")

    statuses = load(STATUSES)
    require("bioinstrumentacion" in set(statuses.get("pending", [])), "course not pending")
    require("bioinstrumentacion" not in set(statuses.get("developed", [])), "course developed prematurely")
    require(not DECISION.exists() and not MANIFEST.exists(), "external review evidence fabricated")

    full = json.dumps(unit, ensure_ascii=False).casefold()
    for forbidden in ("consulte a su médico", "debe tomar", "dosis recomendada", "diagnóstico definitivo"):
        require(forbidden not in full, f"clinical recommendation detected: {forbidden}")
    for marker in ("no constituye respaldo profesional externo", "publicación", "validación clínica", "pending_human_review", "modelo simple declarado", "carga eléctrica", "carga térmica", "carga mecánica", "cadena óptica"):
        require(marker in full, f"scientific or editorial limit missing: {marker}")

    readiness = READINESS.read_text(encoding="utf-8")
    for marker in ("Borrador autoral completo", "La evidencia humana continúa pendiente", "curso permanece `pending`", "publicación continúa bloqueada", "authoral_unit_status: authored_internal_review_pending_external_verification"):
        require(marker in readiness, f"readiness lacks marker: {marker}")
    implementation = IMPLEMENTATION_DOC.read_text(encoding="utf-8")
    for marker in ("2.200 palabras", "U2-A1", "U2-P1", "NTCLG100E2103JB", "pending_human_review", "no publica la unidad"):
        require(marker in implementation, f"implementation document lacks marker: {marker}")


def main() -> int:
    try:
        require({path.name for path in DEFAULT_SOURCE.glob("*.json")} == EXPECTED_FILES, "source inventory is not exact")
        unit = build_unit(DEFAULT_SOURCE)
        expected = canonical_bytes(unit)
        require(DEFAULT_OUTPUT.is_file() and DEFAULT_OUTPUT.read_bytes() == expected, "canonical unit is missing or out of sync")
        validate_identity_and_alignment(unit)
        theory_words = validate_theory(unit)
        validate_learning_assets(unit)
        validate_assessment_practice_and_sources(unit)
        validate_state_and_limits(unit)
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "unit-02.json"
            copy.write_bytes(expected)
            require(copy.read_bytes() == DEFAULT_OUTPUT.read_bytes(), "independent serialization differs")
    except (OSError, ValueError, TypeError, json.JSONDecodeError, BuildError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    print("OK Bioinstrumentation U2 complete authoral draft")
    print(f"6 theory sections · {theory_words} theory words · 20 glossary terms · 3 worked examples · 5 assessments · 3 practices · 12 sources")
    print("course pending · public release blocked · external professional review pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
