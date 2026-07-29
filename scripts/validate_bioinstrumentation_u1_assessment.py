#!/usr/bin/env python3
"""Validate executable assessment and feedback for Bioinstrumentation U1."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bioinstrumentation_assessment_core import (
    AssessmentError,
    evaluate_submission,
    load_json,
)

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_PATH = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-01.json"
FEEDBACK_PATH = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-01-feedback.json"
PREPARATION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-01.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01" / "ASSESSMENT_IMPLEMENTATION.md"
AUTHORAL_UNIT_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-01.json"
FIXTURE_DIR = ROOT / "data" / "assessment_fixtures" / "bioinstrumentacion" / "unit-01"
REQUIRED_FEEDBACK_FIELDS = {
    "diagnosed_misconception",
    "why_the_reasoning_fails",
    "first_hint",
    "second_hint",
    "source_or_section_to_review",
    "different_recovery_problem",
    "objective_continue_criterion",
}
EXPECTED_MISCONCEPTIONS = {
    "digital-equals-measurand",
    "signal-equals-result",
    "analyte-equals-measurand",
    "name-is-specification",
    "method-is-measurand",
    "sensor-directly-measures-clinical-property",
    "chain-equals-model",
    "metadata-irrelevant",
    "repeatability-means-no-bias",
    "instrument-is-traceable",
    "certificate-guarantees-result",
    "traceability-means-fit",
    "memorized-vocabulary-without-transfer",
}


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} is insufficient")
    return text


def validate_identity(implementation: dict[str, Any]) -> None:
    if implementation.get("implementation_id") != "bioinstrumentacion-unit-01-assessment":
        raise ValueError("unexpected implementation id")
    if implementation.get("subject_id") != "bioinstrumentacion" or implementation.get("unit_number") != 1:
        raise ValueError("assessment belongs to another unit")
    if implementation.get("status") != "implemented_internal_review":
        raise ValueError("assessment must remain in internal review")
    if implementation.get("course_editorial_state") != "pending":
        raise ValueError("course editorial state must remain pending")
    if implementation.get("full_theory_drafting_authorized") is not False:
        raise ValueError("full theory drafting was authorized prematurely")
    if implementation.get("feedback_bank") != str(FEEDBACK_PATH.relative_to(ROOT)):
        raise ValueError("feedback bank path is not synchronized")


def validate_assessments(implementation: dict[str, Any], bank_ids: set[str]) -> None:
    machine = implementation.get("machine_scored_assessments")
    human = implementation.get("human_scored_assessments")
    if not isinstance(machine, list) or not isinstance(human, list):
        raise ValueError("assessment lists are missing")
    if {entry.get("id") for entry in machine if isinstance(entry, dict)} != {"U1-A1", "U1-A4"}:
        raise ValueError("machine-scored assessment set changed")
    if {entry.get("id") for entry in human if isinstance(entry, dict)} != {"U1-A2", "U1-A3", "U1-A5"}:
        raise ValueError("human-scored assessment set changed")
    if any(entry.get("automatic_semantic_grading") is not False for entry in human):
        raise ValueError("open responses cannot use automatic semantic grading")

    concept = next(entry for entry in machine if entry.get("id") == "U1-A1")
    items = concept.get("items")
    categories = concept.get("allowed_categories")
    if not isinstance(items, list) or len(items) != 18:
        raise ValueError("concept sort must contain exactly 18 items")
    if not isinstance(categories, list) or len(set(categories)) != 10:
        raise ValueError("concept sort must preserve ten categories")
    item_ids = [item.get("id") for item in items if isinstance(item, dict)]
    if len(set(item_ids)) != 18:
        raise ValueError("concept sort item ids are duplicated")
    if sum(item.get("critical") is True for item in items) < 6:
        raise ValueError("concept sort has too few critical distractors")
    routed: set[str] = set()
    for item in items:
        mapped = item.get("misconceptions_on_error")
        if not isinstance(mapped, list) or not mapped:
            raise ValueError(f"concept item {item.get('id')} lacks routing")
        routed.update(str(value) for value in mapped)
    if not routed.issubset(bank_ids):
        raise ValueError("concept sort routes to unknown misconceptions")

    traceability = next(entry for entry in machine if entry.get("id") == "U1-A4")
    claims = traceability.get("claims")
    if not isinstance(claims, list) or len(claims) != 4:
        raise ValueError("traceability review must contain four claims")
    for claim in claims:
        require_text(claim.get("statement"), f"{claim.get('id')}.statement", 40)
        if not isinstance(claim.get("required_findings"), list) or not claim["required_findings"]:
            raise ValueError(f"{claim.get('id')} lacks required findings")
        mapped = claim.get("misconceptions")
        if not isinstance(mapped, list) or not set(mapped).issubset(bank_ids):
            raise ValueError(f"{claim.get('id')} has invalid routing")

    for entry in human:
        rubric = entry.get("rubric")
        if not isinstance(rubric, list) or len(rubric) < 5:
            raise ValueError(f"{entry.get('id')} rubric is incomplete")
        if not any(row.get("critical_if_zero") is True for row in rubric if isinstance(row, dict)):
            raise ValueError(f"{entry.get('id')} lacks critical criteria")


def validate_feedback(implementation: dict[str, Any]) -> set[str]:
    payload = load_json(FEEDBACK_PATH)
    bank = payload.get("feedback")
    if not isinstance(bank, dict) or set(bank) != EXPECTED_MISCONCEPTIONS:
        raise ValueError("feedback bank must contain exactly thirteen misconceptions")
    for misconception_id, entry in bank.items():
        if not isinstance(entry, dict) or set(entry) != REQUIRED_FEEDBACK_FIELDS:
            raise ValueError(f"{misconception_id} feedback fields are incomplete")
        for field in REQUIRED_FEEDBACK_FIELDS:
            require_text(entry.get(field), f"{misconception_id}.{field}", 25)
        if entry["different_recovery_problem"] in {
            entry["first_hint"],
            entry["second_hint"],
            entry["why_the_reasoning_fails"],
        }:
            raise ValueError(f"{misconception_id} recovery is not distinct")
    contract = implementation.get("feedback_contract")
    if not isinstance(contract, dict):
        raise ValueError("feedback contract is missing")
    if set(contract.get("required_fields", [])) != REQUIRED_FEEDBACK_FIELDS:
        raise ValueError("required feedback fields changed")
    prohibited = set(contract.get("prohibited_output_fields", []))
    if prohibited != {"correct_category", "expected_decision", "answer_key", "complete_correct_response"}:
        raise ValueError("prohibited output fields changed")
    return set(bank)


def validate_blueprint_coverage(bank_ids: set[str]) -> None:
    preparation = load_json(PREPARATION_PATH)
    misconceptions = preparation.get("misconception_bank")
    if not isinstance(misconceptions, list):
        raise ValueError("preparation misconception bank is missing")
    blueprint_ids = {
        str(entry.get("id"))
        for entry in misconceptions
        if isinstance(entry, dict) and entry.get("id")
    }
    if blueprint_ids != bank_ids:
        raise ValueError("executable feedback does not match the preparation bank")
    assessment_ids: set[str] = set()
    for assessment in preparation.get("assessment_blueprint", []):
        if isinstance(assessment, dict):
            assessment_ids.update(
                str(value)
                for value in assessment.get("misconceptions_discriminated", [])
            )
    if not assessment_ids.issubset(bank_ids):
        raise ValueError("blueprint assessments reference missing feedback")


def validate_runtime(implementation: dict[str, Any]) -> None:
    mastery = load_json(FIXTURE_DIR / "mastery-concept-sort.json")
    mastery_result = evaluate_submission(mastery, implementation)
    if mastery_result.get("mastered") is not True or mastery_result.get("score") != {"correct": 18, "total": 18}:
        raise ValueError("mastery fixture did not achieve full mastery")
    if mastery_result.get("feedback") != []:
        raise ValueError("mastery fixture should not receive remediation")

    diagnostic = load_json(FIXTURE_DIR / "diagnostic-concept-sort.json")
    first = evaluate_submission(diagnostic, implementation)
    expected = {
        "digital-equals-measurand",
        "signal-equals-result",
        "method-is-measurand",
        "instrument-is-traceable",
        "certificate-guarantees-result",
    }
    if first.get("mastered") is not False or not expected.issubset(set(first.get("diagnosed_misconceptions", []))):
        raise ValueError("diagnostic concept fixture did not route expected errors")
    first_payload = json.dumps(first, ensure_ascii=False)
    for forbidden in ("correct_category", "expected_decision", "answer_key", "complete_correct_response"):
        if forbidden in first_payload:
            raise ValueError(f"learner output leaks {forbidden}")
    for item in first.get("feedback", []):
        if "first_hint" not in item or "second_hint" in item or "different_recovery_problem" in item:
            raise ValueError("attempt 1 feedback release is incorrect")

    second_submission = dict(diagnostic)
    second_submission["attempt"] = 2
    second = evaluate_submission(second_submission, implementation)
    for item in second.get("feedback", []):
        if "second_hint" not in item or "first_hint" in item or "different_recovery_problem" in item:
            raise ValueError("attempt 2 feedback release is incorrect")

    third_submission = dict(diagnostic)
    third_submission["attempt"] = 3
    third = evaluate_submission(third_submission, implementation)
    for item in third.get("feedback", []):
        if "different_recovery_problem" not in item or "objective_continue_criterion" not in item:
            raise ValueError("attempt 3 recovery release is incorrect")
        if "first_hint" in item or "second_hint" in item:
            raise ValueError("attempt 3 should not repeat hints")

    traceability = load_json(FIXTURE_DIR / "diagnostic-traceability.json")
    trace_result = evaluate_submission(traceability, implementation)
    trace_expected = {
        "instrument-is-traceable",
        "certificate-guarantees-result",
        "traceability-means-fit",
    }
    if trace_result.get("mastered") is not False or not trace_expected.issubset(set(trace_result.get("diagnosed_misconceptions", []))):
        raise ValueError("traceability fixture did not route expected errors")

    try:
        evaluate_submission({"assessment_id": "U1-A2", "attempt": 1, "responses": {}}, implementation)
    except AssessmentError as exc:
        if "requires human rubric scoring" not in str(exc):
            raise ValueError("open-response rejection is unclear") from exc
    else:
        raise ValueError("open response was graded automatically")


def validate_repository_state() -> None:
    package = load_json(PACKAGE_PATH)
    if package.get("current_phase") != "unit_01_authoring_preparation_review":
        raise ValueError("historical preparation phase changed")
    if package.get("active_workstream") != "unit_01_assessment_implementation_review":
        raise ValueError("assessment workstream is not synchronized")
    assessment = package.get("assessment_implementation")
    if not isinstance(assessment, dict):
        raise ValueError("package assessment implementation is missing")
    if assessment.get("contract") != str(IMPLEMENTATION_PATH.relative_to(ROOT)):
        raise ValueError("package assessment contract path is incorrect")
    if assessment.get("human_review_status") != "pending_human_review":
        raise ValueError("human review must remain pending")
    if assessment.get("automatic_semantic_grading") is not False:
        raise ValueError("package enables semantic auto-grading")
    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if AUTHORAL_UNIT_PATH.exists():
        raise ValueError("authoral unit exists before human review")
    text = DOC_PATH.read_text(encoding="utf-8")
    for marker in (
        "Implementación de evaluación y feedback",
        "sin revelar la respuesta",
        "rúbrica humana",
        "pending_human_review",
        "prueba cognitiva pendiente",
    ):
        if marker not in text:
            raise ValueError(f"assessment implementation document lacks: {marker}")


def main() -> int:
    try:
        implementation = load_json(IMPLEMENTATION_PATH)
        validate_identity(implementation)
        bank_ids = validate_feedback(implementation)
        validate_blueprint_coverage(bank_ids)
        validate_assessments(implementation, bank_ids)
        validate_runtime(implementation)
        validate_repository_state()
    except (OSError, ValueError, TypeError, AssessmentError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK assessment: Bioinstrumentación U1")
    print("18 concept items · 4 traceability claims · 13 feedback routes · open tasks human-scored · course pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
