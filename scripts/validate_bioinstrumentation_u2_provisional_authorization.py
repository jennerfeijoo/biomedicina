#!/usr/bin/env python3
"""Validate the provisional owner authorization for Bioinstrumentation unit 2 authoring."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH_PATH = ROOT / "data/authoring_authorizations/bioinstrumentacion-unit-02-provisional.json"
AUDIT_PATH = ROOT / "data/course_audits/bioinstrumentacion/UNIT_02_PRACTICES_ASSESSMENT_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json"
PACKAGE_PATH = ROOT / "data/course_plan_packages/package-04-bioinstrumentation-excellence-pilot.json"
HANDOFF_PATH = ROOT / "data/review_handoffs/bioinstrumentacion-unit-02.json"
STATUS_PATH = ROOT / "data/catalog_statuses.json"
DOC_PATH = ROOT / "docs/pilots/bioinstrumentacion/unit-02/PROVISIONAL_AUTHORING_AUTHORIZATION.md"
READINESS_PATH = ROOT / "docs/pilots/bioinstrumentacion/unit-02/AUTHORING_READINESS.md"
AUTHORAL_UNIT_PATH = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-02.json"
AUTHORAL_SOURCE_DIR = ROOT / "data/course_redevelopment/bioinstrumentacion/unit-02-source"
AUTHORAL_BUILDER = ROOT / "scripts/build_bioinstrumentation_u2_authoral_unit.py"
AUTHORAL_VALIDATOR = ROOT / "scripts/validate_bioinstrumentation_u2_authoral_unit.py"
DECISION_PATH = ROOT / "data/review_evidence/bioinstrumentacion-unit-02-disciplinary-review.json"
MANIFEST_PATH = ROOT / "data/review_evidence/bioinstrumentacion-unit-02-review-packet.json"
EXPECTED_BASE_COMMIT = "a29fcedce078de03976970cdb8ce21a10b300245"
EXPECTED_SCOPE = {
    "create_modular_authoral_source",
    "create_authoral_unit_draft",
    "draft_full_theory",
    "integrate_existing_practices_assessments_and_feedback",
    "revise_examples_glossary_recovery_and_biomedical_connections",
    "create_deterministic_builder_and_validator",
    "open_controlled_authoring_pull_requests",
    "run_internal_quality_gates",
}
EXPECTED_CONSTRAINTS = {
    "source_traceability_for_scientific_claims",
    "sensor_transducer_and_system_boundaries_must_be_declared",
    "static_properties_must_include_model_domain_reference_and_conditions",
    "dynamic_rejection_limited_to_declared_simple_first_order_model",
    "electrical_mechanical_thermal_and_optical_loading_paths_must_remain_separate",
    "component_specifications_must_not_be_transferred_to_system_or_clinical_performance",
    "answer_key_fields_must_remain_internal",
    "human_data_samples_and_subject_connected_hardware_prohibited",
    "clinical_regulatory_safety_and_utility_claims_prohibited",
    "unit_must_remain_internal_and_unpublished",
}
EXPECTED_PROHIBITIONS = {
    "public_release",
    "unit_developed_status",
    "course_promotion",
    "complete_status",
    "clinical_regulatory_or_safety_validation_claims",
    "human_or_professional_endorsement_claims",
    "fabricated_human_review_evidence",
    "deployment_of_answer_keys_in_public_client_assets",
    "modification_of_external_review_status",
}


def load_json(path: Path) -> dict[str, Any]:
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


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    require(len(text) >= minimum, f"{label} is insufficient")
    return text


def require_true_map(value: Any, expected_keys: set[str], label: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label} is missing")
    require(set(value) == expected_keys, f"{label} changed unexpectedly")
    require(all(item is True for item in value.values()), f"{label} is incomplete")
    return value


def validate_authorization(auth: dict[str, Any]) -> None:
    expected_identity = {
        "schema_version": "1.0",
        "authorization_id": "bioinstrumentacion-unit-02-provisional-authoring",
        "subject_id": "bioinstrumentacion",
        "unit_number": 2,
        "status": "authorized_for_controlled_drafting_provisionally",
        "effective_date": "2026-07-30",
        "owner_instruction_timestamp_utc": "2026-07-29T22:44:45Z",
        "authorization_basis_commit": EXPECTED_BASE_COMMIT,
    }
    for field, expected in expected_identity.items():
        require(auth.get(field) == expected, f"authorization {field} is incorrect")
    require(bool(re.fullmatch(r"[0-9a-f]{40}", str(auth.get("authorization_basis_commit", "")))), "authorization basis commit is invalid")

    authority = auth.get("authority")
    require(isinstance(authority, dict), "authority contract is missing")
    require(authority.get("type") == "project_owner_continuation_override", "authority type is incorrect")
    require(authority.get("project_owner") == "jennerfeijoo", "project owner is incorrect")
    require(authority.get("instruction_recorded_by") == "OpenAI assistant", "instruction recorder is incorrect")
    require(authority.get("assistant_review_accepted_provisionally") is True, "internal review was not accepted provisionally")
    require_text(authority.get("instruction_summary"), "authority.instruction_summary", 180)

    characterization = auth.get("review_characterization")
    require(isinstance(characterization, dict), "review characterization is missing")
    expected_review = {
        "review_type": "internal_ai_scientific_editorial_audit_accepted_by_project_owner",
        "reviewer_system": "GPT-5.6 Thinking",
        "audit_record": str(AUDIT_PATH.relative_to(ROOT)),
        "audit_status": "passed_with_corrections_applied",
        "resolved_findings": 6,
        "unresolved_critical_findings": 0,
        "unresolved_major_findings": 0,
        "human_disciplinary_review_completed": False,
        "student_cognitive_test_completed": False,
        "feedback_usability_review_completed": False,
        "inter_rater_round_completed": False,
        "professional_endorsement_present": False,
        "external_verification_deferred": True,
        "external_review_issue": 161,
    }
    for field, expected in expected_review.items():
        require(characterization.get(field) == expected, f"review characterization {field} is incorrect")
    require_text(characterization.get("claim_limit"), "review_characterization.claim_limit", 120)

    require_true_map(auth.get("authorized_scope"), EXPECTED_SCOPE, "authorized scope")
    require_true_map(auth.get("mandatory_authoring_constraints"), EXPECTED_CONSTRAINTS, "mandatory authoring constraints")
    require_true_map(auth.get("not_authorized"), EXPECTED_PROHIBITIONS, "prohibition contract")

    external = auth.get("external_verification_gate")
    require(isinstance(external, dict), "external verification gate is missing")
    require(external.get("status") == "pending_external_professional_review", "external review is not pending")
    require(external.get("existing_handoff") == str(HANDOFF_PATH.relative_to(ROOT)), "external handoff path is incorrect")
    require(external.get("operational_issue") == 161, "operational issue is incorrect")
    required_before = external.get("required_before")
    require(isinstance(required_before, list) and len(required_before) == 6, "external verification boundaries are incomplete")

    expected_state = {
        "course_state": "pending",
        "unit_state": "controlled_authoring_authorized",
        "authoral_unit_present_in_authorization_block": False,
        "publication_state": "blocked_pending_external_verification",
        "professional_review_state": "pending_human_review",
        "cognitive_test_state": "pending_human_execution",
        "feedback_usability_state": "pending_human_execution",
        "inter_rater_state": "pending_human_execution",
    }
    require(auth.get("editorial_state_after_authorization") == expected_state, "editorial state after authorization is incorrect")

    next_gate = auth.get("next_gate")
    require(isinstance(next_gate, dict), "next gate is missing")
    expected_gate = {
        "required_artifact": str(AUTHORAL_UNIT_PATH.relative_to(ROOT)),
        "required_source_directory": str(AUTHORAL_SOURCE_DIR.relative_to(ROOT)),
        "required_builder": str(AUTHORAL_BUILDER.relative_to(ROOT)),
        "required_validator": str(AUTHORAL_VALIDATOR.relative_to(ROOT)),
        "required_internal_review": "scientific_editorial_authoral_audit_before_any_publication_or_status_change",
    }
    require(next_gate == expected_gate, "next authoring gate is incorrect")


def validate_audit_basis() -> None:
    audit = load_json(AUDIT_PATH)
    require(audit.get("audit_id") == "bioinstrumentacion-u2-practices-assessment-scientific-editorial-2026-07-29", "audit identity is incorrect")
    require(audit.get("status") == "passed_with_corrections_applied", "audit basis did not pass")
    findings = audit.get("findings")
    require(isinstance(findings, list) and len(findings) == 6, "audit finding count changed")
    require(all(isinstance(item, dict) and item.get("status") == "resolved" for item in findings), "audit contains unresolved findings")
    require(audit.get("unresolved_critical_findings") == 0, "audit has unresolved critical findings")
    require(audit.get("unresolved_major_findings") == 0, "audit has unresolved major findings")
    require(audit.get("external_professional_review") == "pending_human_review", "audit external review state changed")
    require(audit.get("student_cognitive_test") == "pending_human_execution", "audit fabricates cognitive evidence")
    require(audit.get("feedback_usability_review") == "pending_human_execution", "audit fabricates feedback usability evidence")
    require(audit.get("inter_rater_round") == "pending_human_execution", "audit fabricates inter-rater evidence")
    require(audit.get("public_release_authorized") is False, "audit authorizes publication")
    require(audit.get("unit_developed") is False, "audit promotes the unit")
    require(audit.get("course_state") == "pending", "audit changes the course state")


def validate_package() -> None:
    package = load_json(PACKAGE_PATH)
    require(package.get("schema_version") == "2.0", "central package schema changed")
    require(package.get("unit_02_provisional_authoring_workstream") == "unit_02_controlled_authoring_authorized_provisionally", "provisional authoring workstream is not synchronized")
    section = package.get("unit_02_provisional_authoring_authorization")
    expected_section = {
        "status": "authorized_for_controlled_drafting_provisionally",
        "record": str(AUTH_PATH.relative_to(ROOT)),
        "document": str(DOC_PATH.relative_to(ROOT)),
        "validation": "scripts/validate_bioinstrumentation_u2_provisional_authorization.py",
        "authority": "project_owner_continuation_override",
        "authorization_basis_commit": EXPECTED_BASE_COMMIT,
        "operational_issue": 161,
        "assistant_review_accepted_provisionally": True,
        "controlled_authoring_authorized": True,
        "full_theory_drafting_authorized_provisionally": True,
        "authoral_unit_present_in_authorization_block": False,
        "external_professional_review_status": "pending_human_review",
        "professional_endorsement_present": False,
        "student_cognitive_test": "pending_human_execution",
        "feedback_usability_review": "pending_human_execution",
        "inter_rater_round": "pending_human_execution",
        "public_release_authorized": False,
        "unit_developed": False,
        "course_state": "pending",
        "editorial_effect": "controlled_authoring_only",
    }
    require(section == expected_section, "central package provisional authoring section is incorrect")

    historical = package.get("unit_02_preparation")
    require(isinstance(historical, dict), "Unit 2 preparation section is missing")
    require(historical.get("full_theory_drafting_authorized") is False, "historical preparation record was rewritten")
    require(historical.get("authoral_unit_present") is False, "authorization block claims an authoral file")


def validate_repository_state() -> None:
    handoff = load_json(HANDOFF_PATH)
    require(handoff.get("status") == "ready_pending_external_review", "external handoff no longer remains pending")
    require(handoff.get("practice_implementation_authorized") is False, "external handoff fabricates professional authorization")
    require(handoff.get("full_theory_drafting_authorized") is False, "historical external handoff was rewritten")
    decision_state = handoff.get("decision_state_now")
    require(isinstance(decision_state, dict), "external handoff decision state is missing")
    require(decision_state.get("decision_record_present") is False, "external decision record is unexpectedly present")
    require(decision_state.get("packet_manifest_present") is False, "external packet manifest is unexpectedly present")
    require(decision_state.get("disciplinary_review_completed") is False, "external disciplinary review was marked complete")
    require(decision_state.get("practice_implementation_authorized") is False, "external decision state fabricates professional authorization")
    require(decision_state.get("full_theory_drafting_authorized") is False, "external decision state authorizes full theory")

    statuses = load_json(STATUS_PATH)
    require("bioinstrumentacion" in set(statuses.get("pending", [])), "Bioinstrumentation must remain pending")
    require("bioinstrumentacion" not in set(statuses.get("developed", [])), "Bioinstrumentation was promoted prematurely")
    require(not DECISION_PATH.exists() and not MANIFEST_PATH.exists(), "authorization fabricated external review evidence")

    authoral_present = AUTHORAL_UNIT_PATH.exists()
    source_present = AUTHORAL_SOURCE_DIR.is_dir()
    builder_present = AUTHORAL_BUILDER.is_file()
    validator_present = AUTHORAL_VALIDATOR.is_file()
    if authoral_present or source_present or builder_present or validator_present:
        require(authoral_present and source_present and builder_present and validator_present, "future authoral bundle is incomplete")
        package = load_json(PACKAGE_PATH)
        authoral_section = package.get("unit_02_authoral_unit")
        require(isinstance(authoral_section, dict), "future authoral bundle lacks a central package section")
        require(authoral_section.get("status") in {"authored_internal_review", "authored_internal_review_pending_external_verification"}, "future authoral status is invalid")
    else:
        package = load_json(PACKAGE_PATH)
        require("unit_02_authoral_unit" not in package, "authorization block contains a premature authoral section")

    document = DOC_PATH.read_text(encoding="utf-8")
    for marker in (
        "authorized_for_controlled_drafting_provisionally",
        "project_owner_continuation_override",
        "a29fcedce078de03976970cdb8ce21a10b300245",
        "crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json`",
        "No constituye revisión humana disciplinar",
        "public_release_authorized: false",
        "pending_human_review",
    ):
        require(marker in document, f"authorization document lacks marker: {marker}")

    readiness = READINESS_PATH.read_text(encoding="utf-8")
    for marker in (
        "provisional_authoring_authorized: true",
        "controlled_authoring_authorized",
        "full_theory_drafting_authorized_provisionally: true",
        "external_professional_review: pending_human_review",
        "course_editorial_state: pending",
        "Autorización provisional de autoría controlada",
    ):
        require(marker in readiness, f"AUTHORING_READINESS lacks marker: {marker}")


def main() -> int:
    try:
        authorization = load_json(AUTH_PATH)
        validate_authorization(authorization)
        validate_audit_basis()
        validate_package()
        validate_repository_state()
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    print("OK Bioinstrumentation U2 provisional authoring authorization")
    print("owner continuation override · six audit findings resolved · controlled authoring enabled")
    print("course pending · publication blocked · human and professional review pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
