#!/usr/bin/env python3
"""Validate executable assessment and feedback for Bioinstrumentation unit 2."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from bioinstrumentation_u2_assessment_core import (
    AssessmentError,
    evaluate_submission,
    load_json,
)

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_PATH = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-02.json"
FEEDBACK_PATH = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-02-feedback.json"
PREPARATION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-02.json"
PRACTICE_PATH = ROOT / "data" / "practice_implementations" / "bioinstrumentacion-unit-02.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
HANDOFF_PATH = ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-02.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "ASSESSMENT_IMPLEMENTATION.md"
READINESS_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "AUTHORING_READINESS.md"
AUTHORAL_UNIT_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"
FIXTURE_DIR = ROOT / "data" / "assessment_fixtures" / "bioinstrumentacion" / "unit-02"

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
    "sensor-equals-system",
    "sensor-equals-transducer-always",
    "higher-sensitivity-is-better",
    "sensitivity-equals-resolution",
    "static-calibration-covers-dynamics",
    "response-time-equals-time-constant",
    "fast-means-accurate",
    "linearity-is-intrinsic-global",
    "hysteresis-is-random-noise",
    "loading-is-negligible",
    "datasheet-is-system-proof",
    "component-performance-is-clinical-utility",
}
EXPECTED_FIXTURES = {
    "mastery-static.json",
    "diagnostic-static.json",
    "mastery-dynamic.json",
    "diagnostic-dynamic.json",
    "mastery-loading.json",
    "diagnostic-loading.json",
    "mastery-human.json",
    "diagnostic-human.json",
}
PROHIBITED_OUTPUT_FIELDS = {
    "expected_pattern",
    "expected_refutation_test",
    "expected_decision",
    "expected_route",
    "expected_perturbed_quantity",
    "expected_missing_evidence",
    "tau_target_s",
    "answer_key",
    "complete_correct_response",
}


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} is insufficient")
    return text


def validate_identity(implementation: dict[str, Any]) -> None:
    expected = {
        "implementation_id": "bioinstrumentacion-unit-02-assessment",
        "subject_id": "bioinstrumentacion",
        "unit_number": 2,
        "status": "implemented_internal_review",
        "course_editorial_state": "pending",
        "source_blueprint": str(PREPARATION_PATH.relative_to(ROOT)),
        "practice_implementation": str(PRACTICE_PATH.relative_to(ROOT)),
        "feedback_bank": str(FEEDBACK_PATH.relative_to(ROOT)),
        "external_professional_review_status": "pending_human_review",
        "full_theory_drafting_authorized": False,
        "authoral_unit_present": False,
        "public_release_authorized": False,
        "editorial_effect": "internal_assessment_implementation_only",
    }
    for field, wanted in expected.items():
        if implementation.get(field) != wanted:
            raise ValueError(f"assessment {field} is incorrect")
    require_text(implementation.get("purpose"), "assessment purpose", 180)
    state = implementation.get("review_state")
    if not isinstance(state, dict):
        raise ValueError("review state is missing")
    expected_state = {
        "internal_technical_validation": "implemented",
        "disciplinary_review": "pending_human_review",
        "student_cognitive_test": "pending",
        "feedback_usability_review": "pending",
        "full_theory_drafting_authorized": False,
        "unit_developed": False,
        "public_release_authorized": False,
        "course_state_after_block": "pending",
    }
    if state != expected_state:
        raise ValueError("assessment review state changed unexpectedly")


def validate_feedback(implementation: dict[str, Any]) -> set[str]:
    payload = load_json(FEEDBACK_PATH)
    if payload.get("subject_id") != "bioinstrumentacion" or payload.get("unit_number") != 2:
        raise ValueError("feedback bank belongs to another unit")
    if payload.get("status") != "implemented_internal_review":
        raise ValueError("feedback bank status is incorrect")
    bank = payload.get("feedback")
    if not isinstance(bank, dict) or set(bank) != EXPECTED_MISCONCEPTIONS:
        raise ValueError("feedback bank must contain exactly twelve U2 misconceptions")
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
            raise ValueError(f"{misconception_id} recovery problem is not distinct")

    contract = implementation.get("feedback_contract")
    if not isinstance(contract, dict):
        raise ValueError("feedback contract is missing")
    if set(contract.get("required_fields", [])) != REQUIRED_FEEDBACK_FIELDS:
        raise ValueError("required feedback fields changed")
    if set(contract.get("prohibited_output_fields", [])) != PROHIBITED_OUTPUT_FIELDS:
        raise ValueError("prohibited output fields changed")
    release = contract.get("release_by_attempt")
    expected_release = {
        "1": [
            "diagnosed_misconception",
            "why_the_reasoning_fails",
            "first_hint",
            "source_or_section_to_review",
        ],
        "2": [
            "diagnosed_misconception",
            "why_the_reasoning_fails",
            "second_hint",
            "source_or_section_to_review",
        ],
        "3_plus": [
            "diagnosed_misconception",
            "why_the_reasoning_fails",
            "different_recovery_problem",
            "objective_continue_criterion",
            "source_or_section_to_review",
        ],
    }
    if release != expected_release:
        raise ValueError("feedback release policy changed unexpectedly")
    return set(bank)


def validate_blueprint_and_assessments(
    implementation: dict[str, Any], bank_ids: set[str]
) -> None:
    preparation = load_json(PREPARATION_PATH)
    blueprint_bank = preparation.get("misconception_bank")
    if not isinstance(blueprint_bank, list):
        raise ValueError("preparation misconception bank is missing")
    blueprint_ids = {
        str(entry.get("id"))
        for entry in blueprint_bank
        if isinstance(entry, dict) and entry.get("id")
    }
    if blueprint_ids != bank_ids:
        raise ValueError("executable feedback does not match the U2 preparation bank")

    blueprint = preparation.get("assessment_blueprint")
    if not isinstance(blueprint, list):
        raise ValueError("assessment blueprint is missing")
    blueprint_assessment_ids = {
        str(entry.get("id"))
        for entry in blueprint
        if isinstance(entry, dict) and entry.get("id")
    }
    if blueprint_assessment_ids != {"U2-A1", "U2-A2", "U2-A3", "U2-A4", "U2-A5"}:
        raise ValueError("assessment blueprint ids changed")
    routed_from_blueprint: set[str] = set()
    for entry in blueprint:
        if not isinstance(entry, dict):
            raise ValueError("invalid assessment blueprint entry")
        routed_from_blueprint.update(
            map(str, entry.get("misconceptions_discriminated", []))
        )
    if not routed_from_blueprint.issubset(bank_ids):
        raise ValueError("blueprint routes to unknown feedback")

    machine = implementation.get("machine_scored_assessments")
    human = implementation.get("human_scored_assessments")
    if not isinstance(machine, list) or not isinstance(human, list):
        raise ValueError("assessment implementation lists are missing")
    if {entry.get("id") for entry in machine if isinstance(entry, dict)} != {
        "U2-A2",
        "U2-A3",
        "U2-A4",
    }:
        raise ValueError("machine-scored U2 assessment set changed")
    if {entry.get("id") for entry in human if isinstance(entry, dict)} != {
        "U2-A1",
        "U2-A5",
    }:
        raise ValueError("human-scored U2 assessment set changed")
    if any(entry.get("automatic_semantic_grading") is not False for entry in human):
        raise ValueError("open responses cannot use automatic semantic grading")

    expected_types = {
        "U2-A2": "static_curve_audit",
        "U2-A3": "first_order_dynamic_model",
        "U2-A4": "loading_mechanism_review",
        "U2-A1": "functional_boundary_sort",
        "U2-A5": "multi_criteria_selection_transfer",
    }
    expected_practices = {
        "U2-A2": ["U2-P1"],
        "U2-A3": ["U2-P2"],
        "U2-A4": ["U2-P3"],
    }
    for entry in machine + human:
        assessment_id = str(entry.get("id"))
        if entry.get("type") != expected_types[assessment_id]:
            raise ValueError(f"{assessment_id} type is incorrect")
        if assessment_id in expected_practices and entry.get("practice_evidence") != expected_practices[assessment_id]:
            raise ValueError(f"{assessment_id} practice evidence is incorrect")
        routed: set[str] = set()
        for group in ("cases", "claims"):
            values = entry.get(group, [])
            if isinstance(values, list):
                for item in values:
                    if isinstance(item, dict):
                        routed.update(map(str, item.get("misconceptions", [])))
        routed.update(map(str, entry.get("allowed_misconceptions", [])))
        if not routed.issubset(bank_ids):
            raise ValueError(f"{assessment_id} routes to unknown misconceptions")

    static = next(entry for entry in machine if entry.get("id") == "U2-A2")
    if len(static.get("cases", [])) != 4 or set(static.get("allowed_patterns", [])) != {
        "linear_local",
        "saturation",
        "dead_zone",
        "hysteresis",
    }:
        raise ValueError("U2-A2 does not preserve four static patterns")
    dynamic = next(entry for entry in machine if entry.get("id") == "U2-A3")
    if len(dynamic.get("cases", [])) != 4:
        raise ValueError("U2-A3 must contain one positive and three negative cases")
    positive = next(case for case in dynamic["cases"] if case.get("id") == "DY01")
    if positive.get("tau_target_s") != 2.0 or positive.get("tau_tolerance_s") != 0.1:
        raise ValueError("U2-A3 tau target or tolerance changed")
    if {case.get("id") for case in dynamic["cases"]} != {"DY01", "DY02", "DY03", "DY04"}:
        raise ValueError("U2-A3 case ids changed")
    loading = next(entry for entry in machine if entry.get("id") == "U2-A4")
    if len(loading.get("claims", [])) != 4:
        raise ValueError("U2-A4 must preserve four loading claims")

    for entry in human:
        rubric = entry.get("rubric")
        if not isinstance(rubric, list) or len(rubric) < 7:
            raise ValueError(f"{entry.get('id')} rubric is incomplete")
        if not any(row.get("critical_if_zero") is True for row in rubric if isinstance(row, dict)):
            raise ValueError(f"{entry.get('id')} lacks critical rubric criteria")


def _assert_no_answer_leak(result: dict[str, Any]) -> None:
    payload = json.dumps(result, ensure_ascii=False)
    for forbidden in PROHIBITED_OUTPUT_FIELDS:
        if f'"{forbidden}"' in payload:
            raise ValueError(f"learner output leaks {forbidden}")


def _evaluate_fixture(
    implementation: dict[str, Any], filename: str
) -> dict[str, Any]:
    return evaluate_submission(load_json(FIXTURE_DIR / filename), implementation)


def validate_runtime(implementation: dict[str, Any]) -> None:
    existing = {path.name for path in FIXTURE_DIR.glob("*.json")}
    if not EXPECTED_FIXTURES.issubset(existing):
        raise ValueError(f"missing assessment fixtures: {sorted(EXPECTED_FIXTURES - existing)}")

    for filename in (
        "mastery-static.json",
        "mastery-dynamic.json",
        "mastery-loading.json",
        "mastery-human.json",
    ):
        result = _evaluate_fixture(implementation, filename)
        if result.get("mastered") is not True:
            raise ValueError(f"{filename} did not achieve mastery")
        if result.get("feedback") != []:
            raise ValueError(f"{filename} should not receive remediation")
        _assert_no_answer_leak(result)

    static = _evaluate_fixture(implementation, "diagnostic-static.json")
    expected_static = {
        "higher-sensitivity-is-better",
        "sensitivity-equals-resolution",
        "linearity-is-intrinsic-global",
        "hysteresis-is-random-noise",
    }
    if static.get("mastered") is not False or not expected_static.issubset(
        set(static.get("diagnosed_misconceptions", []))
    ):
        raise ValueError("static diagnostic fixture did not route expected errors")

    dynamic = _evaluate_fixture(implementation, "diagnostic-dynamic.json")
    expected_dynamic = {
        "static-calibration-covers-dynamics",
        "response-time-equals-time-constant",
        "fast-means-accurate",
    }
    if dynamic.get("mastered") is not False or not expected_dynamic.issubset(
        set(dynamic.get("diagnosed_misconceptions", []))
    ):
        raise ValueError("dynamic diagnostic fixture did not route expected errors")

    loading = _evaluate_fixture(implementation, "diagnostic-loading.json")
    expected_loading = {
        "loading-is-negligible",
        "higher-sensitivity-is-better",
        "datasheet-is-system-proof",
        "component-performance-is-clinical-utility",
    }
    if loading.get("mastered") is not False or not expected_loading.issubset(
        set(loading.get("diagnosed_misconceptions", []))
    ):
        raise ValueError("loading diagnostic fixture did not route expected errors")

    human = _evaluate_fixture(implementation, "diagnostic-human.json")
    if human.get("mastered") is not False:
        raise ValueError("human diagnostic fixture unexpectedly achieved mastery")
    if set(human.get("critical_zero_criteria", [])) != {
        "evidence_traceability",
        "unsupported_claims_list",
        "clinical_regulatory_boundary",
    }:
        raise ValueError("human rubric did not detect critical zero criteria")
    if human.get("automatic_semantic_grading") is not False:
        raise ValueError("human rubric claims automatic semantic grading")

    for result in (static, dynamic, loading, human):
        _assert_no_answer_leak(result)
        for item in result.get("feedback", []):
            if "first_hint" not in item:
                raise ValueError("attempt 1 feedback lacks first_hint")
            if "second_hint" in item or "different_recovery_problem" in item:
                raise ValueError("attempt 1 feedback release is incorrect")

    base = load_json(FIXTURE_DIR / "diagnostic-dynamic.json")
    second_submission = copy.deepcopy(base)
    second_submission["attempt"] = 2
    second = evaluate_submission(second_submission, implementation)
    for item in second.get("feedback", []):
        if "second_hint" not in item or "first_hint" in item:
            raise ValueError("attempt 2 feedback release is incorrect")
        if "different_recovery_problem" in item:
            raise ValueError("attempt 2 released recovery problem prematurely")
    _assert_no_answer_leak(second)

    third_submission = copy.deepcopy(base)
    third_submission["attempt"] = 3
    third = evaluate_submission(third_submission, implementation)
    for item in third.get("feedback", []):
        if "different_recovery_problem" not in item or "objective_continue_criterion" not in item:
            raise ValueError("attempt 3 recovery release is incomplete")
        if "first_hint" in item or "second_hint" in item:
            raise ValueError("attempt 3 should not repeat hints")
    _assert_no_answer_leak(third)

    missing_confirmation = load_json(FIXTURE_DIR / "mastery-human.json")
    missing_confirmation["human_reviewer_confirmed"] = False
    try:
        evaluate_submission(missing_confirmation, implementation)
    except AssessmentError as exc:
        if "human_reviewer_confirmed" not in str(exc):
            raise ValueError("missing human confirmation error is unclear") from exc
    else:
        raise ValueError("human rubric was accepted without human confirmation")


def validate_repository_state(implementation: dict[str, Any]) -> None:
    practice = load_json(PRACTICE_PATH)
    if practice.get("status") != "implemented_internal_review":
        raise ValueError("U2 practices are not available for assessment")
    practice_ids = {
        str(entry.get("id"))
        for entry in practice.get("practices", [])
        if isinstance(entry, dict)
    }
    if practice_ids != {"U2-P1", "U2-P2", "U2-P3"}:
        raise ValueError("U2 practice evidence set changed")

    handoff = load_json(HANDOFF_PATH)
    if handoff.get("status") != "ready_pending_external_review":
        raise ValueError("U2 disciplinary handoff is no longer pending")
    if handoff.get("practice_implementation_authorized") is not False:
        raise ValueError("external professional authorization was fabricated")
    if handoff.get("full_theory_drafting_authorized") is not False:
        raise ValueError("external handoff authorizes full theory")

    package = load_json(PACKAGE_PATH)
    if package.get("unit_02_assessment_workstream") != "unit_02_assessment_implementation_review":
        raise ValueError("U2 assessment workstream is not synchronized")
    section = package.get("unit_02_assessment_implementation")
    if not isinstance(section, dict):
        raise ValueError("package U2 assessment section is missing")
    expected_section = {
        "status": "implemented_internal_review",
        "contract": str(IMPLEMENTATION_PATH.relative_to(ROOT)),
        "feedback_bank": str(FEEDBACK_PATH.relative_to(ROOT)),
        "engine": "scripts/bioinstrumentation_u2_assessment_core.py",
        "evaluator": "scripts/evaluate_bioinstrumentation_u2_assessment.py",
        "validation": "scripts/validate_bioinstrumentation_u2_assessment.py",
        "document": str(DOC_PATH.relative_to(ROOT)),
        "machine_scored_assessments": ["U2-A2", "U2-A3", "U2-A4"],
        "human_scored_assessments": ["U2-A1", "U2-A5"],
        "automatic_semantic_grading": False,
        "answer_key_exposed_in_feedback": False,
        "feedback_route_count": 12,
        "student_cognitive_test": "pending",
        "feedback_usability_review": "pending",
        "external_professional_review_status": "pending_human_review",
        "full_theory_drafting_authorized": False,
        "authoral_unit_present": False,
        "public_release_authorized": False,
        "unit_developed": False,
        "course_state": "pending",
        "editorial_effect": "internal_assessment_implementation_only",
    }
    if section != expected_section:
        raise ValueError("package U2 assessment section is incorrect")
    preparation = package.get("unit_02_preparation")
    if not isinstance(preparation, dict):
        raise ValueError("package U2 preparation section is missing")
    if preparation.get("assessment_implementation") != str(IMPLEMENTATION_PATH.relative_to(ROOT)):
        raise ValueError("package preparation assessment path is incorrect")
    if preparation.get("assessment_implementation_present") is not True:
        raise ValueError("package does not register U2 assessment presence")

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentation was promoted prematurely")
    if AUTHORAL_UNIT_PATH.exists():
        raise ValueError("U2 authoral unit exists before separate authorization")

    for path, markers in (
        (
            DOC_PATH,
            (
                "Implementación de evaluación y feedback",
                "sin revelar la respuesta",
                "rúbrica humana",
                "pending_human_review",
                "prueba cognitiva con estudiantes",
            ),
        ),
        (
            READINESS_PATH,
            (
                "assessment_implementation_status: implemented_internal_review",
                "automatic_semantic_grading: false",
                "student_cognitive_test: pending",
                "feedback_usability_review: pending",
                "teoría completa",
            ),
        ),
    ):
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                raise ValueError(f"{path.name} lacks marker: {marker}")


def main() -> int:
    try:
        implementation = load_json(IMPLEMENTATION_PATH)
        validate_identity(implementation)
        bank_ids = validate_feedback(implementation)
        validate_blueprint_and_assessments(implementation, bank_ids)
        validate_runtime(implementation)
        validate_repository_state(implementation)
    except (OSError, ValueError, TypeError, AssessmentError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U2 assessment and feedback")
    print(
        "3 deterministic structured assessments · 2 human rubrics · "
        "12 recovery routes · no answer leakage · external review pending · course pending"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
