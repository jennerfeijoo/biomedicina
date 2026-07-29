#!/usr/bin/env python3
"""Validate the joint internal scientific/editorial audit of Bioinstrumentation U2."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from bioinstrumentation_u2_assessment_core import AssessmentError, evaluate_submission

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "data" / "course_audits" / "bioinstrumentacion" / "UNIT_02_PRACTICES_ASSESSMENT_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json"
REPORT_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "INTERNAL_SCIENTIFIC_EDITORIAL_AUDIT.md"
ASSESSMENT_PATH = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-02.json"
FEEDBACK_PATH = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-02-feedback.json"
PREPARATION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-02.json"
PRACTICE_PATH = ROOT / "data" / "practice_implementations" / "bioinstrumentacion-unit-02.json"
READINESS_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "AUTHORING_READINESS.md"
ASSESSMENT_DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "ASSESSMENT_IMPLEMENTATION.md"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
AUTHORAL_UNIT_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"
DECISION_PATH = ROOT / "data" / "review_evidence" / "bioinstrumentacion-unit-02-disciplinary-review.json"
MANIFEST_PATH = ROOT / "data" / "review_evidence" / "bioinstrumentacion-unit-02-review-packet.json"
FIXTURE_DIR = ROOT / "data" / "assessment_fixtures" / "bioinstrumentacion" / "unit-02"

EXPECTED_FINDINGS = {"U2-SE-01", "U2-SE-02", "U2-SE-03", "U2-SE-04", "U2-SE-05", "U2-SE-06"}
EXPECTED_ASSESSMENTS = {"U2-A1", "U2-A2", "U2-A3", "U2-A4", "U2-A5"}
EXPECTED_CLAIMS = {"U2-C1", "U2-C2", "U2-C3", "U2-C4", "U2-C5", "U2-C6"}
EXPECTED_PRACTICES = {"U2-P1", "U2-P2", "U2-P3"}


class AuditError(ValueError):
    """Raised when the audit record or its corrections are incomplete."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuditError(f"missing file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise AuditError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuditError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def machine_index(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = contract.get("machine_scored_assessments")
    require(isinstance(entries, list), "machine assessments are missing")
    return {
        str(entry.get("id")): entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("id")
    }


def human_index(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = contract.get("human_scored_assessments")
    require(isinstance(entries, list), "human assessments are missing")
    return {
        str(entry.get("id")): entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("id")
    }


def validate_audit_record() -> None:
    audit = load_object(AUDIT_PATH)
    expected_identity = {
        "schema_version": "1.0",
        "audit_id": "bioinstrumentacion-u2-practices-assessment-scientific-editorial-2026-07-29",
        "subject_id": "bioinstrumentacion",
        "unit": 2,
        "audit_type": "internal_scientific_editorial_joint_practices_assessment_feedback",
        "actor_type": "internal_ai_review_accepted_by_project_owner",
        "date": "2026-07-29",
        "status": "passed_with_corrections_applied",
    }
    for field, expected in expected_identity.items():
        require(audit.get(field) == expected, f"unexpected audit field {field}: {audit.get(field)!r}")

    reviewed = audit.get("reviewed_artifacts")
    require(isinstance(reviewed, list) and len(reviewed) >= 11, "reviewed artifact inventory is incomplete")
    for path_text in reviewed:
        require((ROOT / str(path_text)).is_file(), f"reviewed artifact does not exist: {path_text}")

    findings = audit.get("findings")
    require(isinstance(findings, list), "audit findings must be a list")
    ids = {finding.get("id") for finding in findings if isinstance(finding, dict)}
    require(ids == EXPECTED_FINDINGS, f"unexpected audit findings: {sorted(ids)}")
    for finding in findings:
        require(finding.get("severity") in {"major", "minor"}, f"invalid severity: {finding.get('id')}")
        require(finding.get("status") == "resolved", f"unresolved finding: {finding.get('id')}")
        corrected = finding.get("corrected_paths")
        require(isinstance(corrected, list) and corrected, f"finding lacks corrected paths: {finding.get('id')}")
        for path_text in corrected:
            require((ROOT / str(path_text)).is_file(), f"corrected path does not exist: {path_text}")

    require(audit.get("unresolved_critical_findings") == 0, "critical findings remain open")
    require(audit.get("unresolved_major_findings") == 0, "major findings remain open")
    require(audit.get("external_professional_review") == "pending_human_review", "external review state changed")
    require(audit.get("student_cognitive_test") == "pending_human_execution", "cognitive test state changed")
    require(audit.get("feedback_usability_review") == "pending_human_execution", "feedback usability state changed")
    require(audit.get("inter_rater_round") == "pending_human_execution", "inter-rater state changed")
    require(audit.get("full_theory_drafting_authorized") is False, "audit authorizes theory")
    require(audit.get("public_release_authorized") is False, "audit authorizes publication")
    require(audit.get("unit_developed") is False, "audit promotes the unit")
    require(audit.get("course_state") == "pending", "audit changes the course state")

    limitations = " ".join(map(str, audit.get("limitations", []))).casefold()
    for marker in (
        "no constituye revisión profesional externa",
        "no reemplaza pruebas cognitivas",
        "no valida sensores",
        "no autoriza la teoría completa",
    ):
        require(marker in limitations, f"audit limitation missing: {marker}")


def validate_scientific_corrections(contract: dict[str, Any]) -> None:
    machines = machine_index(contract)
    humans = human_index(contract)
    require(set(machines) == {"U2-A2", "U2-A3", "U2-A4"}, "machine assessment set changed")
    require(set(humans) == {"U2-A1", "U2-A5"}, "human assessment set changed")
    require(all(item.get("automatic_semantic_grading") is False for item in humans.values()), "human responses enable semantic auto-grading")

    static = machines["U2-A2"]
    static_cases = {str(case.get("id")): case for case in static.get("cases", []) if isinstance(case, dict)}
    require(static_cases.get("SC01", {}).get("misconceptions") == ["linearity-is-intrinsic-global"], "SC01 still routes irrelevant sensitivity feedback")
    require("higher-sensitivity-is-better" in static_cases.get("SC02", {}).get("misconceptions", []), "sensitivity route disappeared from the saturation case")

    dynamic = machines["U2-A3"]
    require(
        dynamic.get("allowed_decisions") == ["accept_first_order_limited", "reject_declared_simple_first_order"],
        "dynamic decision scope is not corrected",
    )
    dynamic_cases = {str(case.get("id")): case for case in dynamic.get("cases", []) if isinstance(case, dict)}
    for case_id in ("DY02", "DY03", "DY04"):
        require(dynamic_cases.get(case_id, {}).get("expected_decision") == "reject_declared_simple_first_order", f"{case_id} retains an overbroad rejection label")
    scope_note = str(dynamic.get("decision_scope_note", "")).casefold()
    require(
        "modelo simple declarado" in scope_note
        and ("modelo compuesto" in scope_note or "modelos compuestos" in scope_note),
        "dynamic decision scope note is incomplete",
    )

    loading = machines["U2-A4"]
    quantities = set(map(str, loading.get("allowed_perturbed_quantities", [])))
    require("bridge_output_voltage" in quantities, "electrical loading quantity is missing")
    require("bridge_voltage_and_strain_transfer" not in quantities, "electrical and mechanical quantities remain conflated")
    claims = {str(claim.get("id")): claim for claim in loading.get("claims", []) if isinstance(claim, dict)}
    require(claims.get("LG01", {}).get("expected_perturbed_quantity") == "bridge_output_voltage", "LG01 electrical loading correction is missing")

    audit_state = contract.get("internal_scientific_editorial_audit")
    require(isinstance(audit_state, dict), "assessment contract lacks audit state")
    require(audit_state.get("status") == "passed_with_corrections_applied", "assessment audit status is incorrect")
    require(audit_state.get("record") == str(AUDIT_PATH.relative_to(ROOT)), "assessment audit record path is incorrect")
    require(audit_state.get("report") == str(REPORT_PATH.relative_to(ROOT)), "assessment audit report path is incorrect")
    require(audit_state.get("full_theory_drafting_authorized") is False, "assessment audit authorizes theory")
    require(audit_state.get("public_release_authorized") is False, "assessment audit authorizes publication")


def validate_evidence_crosswalk(contract: dict[str, Any]) -> None:
    crosswalk = contract.get("evidence_crosswalk")
    require(isinstance(crosswalk, dict) and set(crosswalk) == EXPECTED_ASSESSMENTS, "assessment evidence crosswalk is incomplete")

    preparation = load_object(PREPARATION_PATH)
    assertions = preparation.get("source_assertions")
    require(isinstance(assertions, list), "preparation source assertions are missing")
    available_claims = {
        str(item.get("claim_id"))
        for item in assertions
        if isinstance(item, dict) and item.get("claim_id")
    }
    require(available_claims == EXPECTED_CLAIMS, "preparation claim set changed")

    practices = load_object(PRACTICE_PATH).get("practices")
    require(isinstance(practices, list), "practice contract is missing practices")
    available_practices = {
        str(item.get("id"))
        for item in practices
        if isinstance(item, dict) and item.get("id")
    }
    require(available_practices == EXPECTED_PRACTICES, "practice set changed")

    expected_outcomes = {
        "U2-A1": {"U2-LO1"},
        "U2-A2": {"U2-LO2", "U2-LO3"},
        "U2-A3": {"U2-LO4"},
        "U2-A4": {"U2-LO3", "U2-LO5"},
        "U2-A5": {"U2-LO1", "U2-LO2", "U2-LO3", "U2-LO4", "U2-LO5"},
    }
    claim_union: set[str] = set()
    practice_union: set[str] = set()
    for assessment_id, row in crosswalk.items():
        require(isinstance(row, dict), f"crosswalk row is invalid: {assessment_id}")
        require(set(map(str, row.get("outcomes", []))) == expected_outcomes[assessment_id], f"outcome crosswalk mismatch: {assessment_id}")
        claims = set(map(str, row.get("source_claims", [])))
        require(claims and claims.issubset(available_claims), f"source claim crosswalk mismatch: {assessment_id}")
        claim_union.update(claims)
        practice_ids = set(map(str, row.get("practice_ids", [])))
        require(practice_ids.issubset(available_practices), f"practice crosswalk mismatch: {assessment_id}")
        practice_union.update(practice_ids)
        artifacts = row.get("artifacts")
        require(isinstance(artifacts, list) and artifacts, f"crosswalk artifacts missing: {assessment_id}")
        for path_text in artifacts:
            require((ROOT / str(path_text)).is_file(), f"crosswalk artifact does not exist: {path_text}")
    require(claim_union == EXPECTED_CLAIMS, "crosswalk does not cover all source claims")
    require(practice_union == EXPECTED_PRACTICES, "crosswalk does not cover all practices")


def validate_answer_key_governance(contract: dict[str, Any]) -> None:
    feedback_contract = contract.get("feedback_contract")
    require(isinstance(feedback_contract, dict), "feedback contract is missing")
    prohibited = set(map(str, feedback_contract.get("prohibited_output_fields", [])))
    require(len(prohibited) == 9, "prohibited output field set changed")

    policy = contract.get("answer_key_distribution_policy")
    require(isinstance(policy, dict), "answer-key distribution policy is missing")
    require(policy.get("storage") == "internal_server_side_or_private_evaluation_service", "answer-key storage policy is unsafe")
    require(set(map(str, policy.get("learner_payload_excludes", []))) == prohibited, "learner payload exclusion is incomplete")
    require(policy.get("public_client_bundle_authorized") is False, "public answer-key bundle was authorized")
    require(policy.get("requires_separate_release_review") is True, "separate release review is not required")

    implementation = contract
    for fixture_name in ("diagnostic-static.json", "diagnostic-dynamic.json", "diagnostic-loading.json"):
        result = evaluate_submission(load_object(FIXTURE_DIR / fixture_name), implementation)
        serialized = json.dumps(result, ensure_ascii=False)
        for field in prohibited:
            require(field not in serialized, f"runtime output leaks {field} through {fixture_name}")


def validate_runtime_regressions(contract: dict[str, Any]) -> None:
    mastery_dynamic = load_object(FIXTURE_DIR / "mastery-dynamic.json")
    dynamic_result = evaluate_submission(mastery_dynamic, contract)
    require(dynamic_result.get("mastered") is True, "corrected dynamic fixture no longer reaches mastery")
    require(dynamic_result.get("score") == {"fully_correct": 4, "total": 4}, "dynamic mastery score changed")

    mastery_loading = load_object(FIXTURE_DIR / "mastery-loading.json")
    loading_result = evaluate_submission(mastery_loading, contract)
    require(loading_result.get("mastered") is True, "corrected loading fixture no longer reaches mastery")
    require(loading_result.get("score") == {"fully_correct": 4, "total": 4}, "loading mastery score changed")

    targeted = copy.deepcopy(load_object(FIXTURE_DIR / "mastery-static.json"))
    targeted["responses"]["SC01"]["pattern"] = "saturation"
    targeted_result = evaluate_submission(targeted, contract)
    require(targeted_result.get("mastered") is False, "targeted SC01 error unexpectedly reaches mastery")
    require(targeted_result.get("diagnosed_misconceptions") == ["linearity-is-intrinsic-global"], "SC01 emits an irrelevant diagnostic route")

    old_dynamic = copy.deepcopy(mastery_dynamic)
    old_dynamic["responses"]["DY02"]["decision"] = "reject_first_order"
    try:
        evaluate_submission(old_dynamic, contract)
    except AssessmentError as exc:
        require("invalid decision" in str(exc), "legacy dynamic rejection fails unclearly")
    else:
        raise AuditError("legacy overbroad dynamic decision remains accepted")

    old_loading = copy.deepcopy(mastery_loading)
    old_loading["responses"]["LG01"]["perturbed_quantity"] = "bridge_voltage_and_strain_transfer"
    try:
        evaluate_submission(old_loading, contract)
    except AssessmentError as exc:
        require("invalid perturbed_quantity" in str(exc), "legacy loading quantity fails unclearly")
    else:
        raise AuditError("legacy conflated loading quantity remains accepted")


def validate_feedback_and_documents() -> None:
    feedback = load_object(FEEDBACK_PATH)
    bank = feedback.get("feedback")
    require(isinstance(bank, dict) and len(bank) == 12, "feedback bank must retain twelve routes")
    for misconception_id, item in bank.items():
        require(isinstance(item, dict), f"invalid feedback entry: {misconception_id}")
        source = str(item.get("source_or_section_to_review", ""))
        require(len(source) >= 20, f"feedback source locator is insufficient: {misconception_id}")

    assessment_doc = ASSESSMENT_DOC_PATH.read_text(encoding="utf-8")
    for marker in (
        "Correcciones de auditoría científica y editorial interna",
        "tensión de salida del puente",
        "reject_declared_simple_first_order",
        "evidence_crosswalk",
        "payload del estudiante",
        "identificadores de máquina permanecen en inglés",
    ):
        require(marker in assessment_doc, f"assessment document lacks marker: {marker}")

    readiness = READINESS_PATH.read_text(encoding="utf-8")
    for marker in (
        "scientific_editorial_audit: passed_with_corrections_applied",
        "unresolved_critical_findings: 0",
        "unresolved_major_findings: 0",
        "Auditoría científica y editorial interna",
        "Preparar una autorización provisional separada",
        "full_theory_drafting_authorized: false",
    ):
        require(marker in readiness, f"readiness document lacks marker: {marker}")

    report = REPORT_PATH.read_text(encoding="utf-8")
    for marker in (
        "aprobada con correcciones aplicadas",
        "Hallazgos críticos sin resolver: **0**",
        "Hallazgos mayores sin resolver: **0**",
        "Teoría completa: **no autorizada**",
        "Revisión profesional externa: **pending_human_review**",
    ):
        require(marker in report, f"audit report lacks marker: {marker}")


def validate_repository_state(contract: dict[str, Any]) -> None:
    require(contract.get("full_theory_drafting_authorized") is False, "assessment contract authorizes theory")
    require(contract.get("public_release_authorized") is False, "assessment contract authorizes publication")
    review = contract.get("review_state")
    require(isinstance(review, dict), "assessment review state is missing")
    require(review.get("disciplinary_review") == "pending_human_review", "assessment contract erases external review")
    require(review.get("student_cognitive_test") == "pending", "assessment contract fabricates cognitive evidence")
    require(review.get("feedback_usability_review") == "pending", "assessment contract fabricates usability evidence")

    statuses = load_object(STATUS_PATH)
    require("bioinstrumentacion" in set(statuses.get("pending", [])), "Bioinstrumentation must remain pending")
    require("bioinstrumentacion" not in set(statuses.get("developed", [])), "Bioinstrumentation was promoted")
    require(not AUTHORAL_UNIT_PATH.exists(), "Unit 2 authoral file exists without theory authorization")
    require(not DECISION_PATH.exists() and not MANIFEST_PATH.exists(), "audit fabricated external review evidence")


def main() -> int:
    try:
        validate_audit_record()
        contract = load_object(ASSESSMENT_PATH)
        validate_scientific_corrections(contract)
        validate_evidence_crosswalk(contract)
        validate_answer_key_governance(contract)
        validate_runtime_regressions(contract)
        validate_feedback_and_documents()
        validate_repository_state(contract)
    except (OSError, TypeError, json.JSONDecodeError, AssessmentError, AuditError, ValueError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    print("OK Bioinstrumentation U2 internal scientific and editorial audit")
    print("6 resolved findings · 0 critical open · 0 major open")
    print("practice/assessment corrections active · course pending · theory and publication blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
