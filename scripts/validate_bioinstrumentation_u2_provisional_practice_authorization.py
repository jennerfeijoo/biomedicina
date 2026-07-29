#!/usr/bin/env python3
"""Validate provisional owner authorization for Bioinstrumentation U2 practices."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH_PATH = ROOT / "data" / "authoring_authorizations" / "bioinstrumentacion-unit-02-practices-provisional.json"
INHERITED_AUTH_PATH = ROOT / "data" / "authoring_authorizations" / "bioinstrumentacion-unit-01-provisional.json"
HANDOFF_PATH = ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-02.json"
PRACTICE_PATH = ROOT / "data" / "practice_implementations" / "bioinstrumentacion-unit-02.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "PROVISIONAL_PRACTICE_IMPLEMENTATION_AUTHORIZATION.md"
READINESS_PATH = DOC_PATH.parent / "AUTHORING_READINESS.md"
AUTHORAL_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"
DECISION_PATH = ROOT / "data" / "review_evidence" / "bioinstrumentacion-unit-02-disciplinary-review.json"
MANIFEST_PATH = ROOT / "data" / "review_evidence" / "bioinstrumentacion-unit-02-review-packet.json"
EXPECTED_COMMIT = "b8134a50a9fea89fe896b167d5791d17ee055e5c"
EXPECTED_ISSUE = 161


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return payload


def require_true_map(value: Any, expected_keys: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected_keys:
        raise ValueError(f"{label} keys changed unexpectedly")
    if any(item is not True for item in value.values()):
        raise ValueError(f"{label} contains a disabled requirement")


def validate_authorization(auth: dict[str, Any]) -> None:
    expected_identity = {
        "authorization_id": "bioinstrumentacion-unit-02-provisional-practice-implementation",
        "subject_id": "bioinstrumentacion",
        "unit_number": 2,
        "status": "authorized_for_controlled_practice_implementation_provisionally",
        "effective_date": "2026-07-29",
    }
    for key, wanted in expected_identity.items():
        if auth.get(key) != wanted:
            raise ValueError(f"authorization {key} is incorrect")
    basis = auth.get("authorization_basis", {})
    if basis.get("technical_basis_commit") != EXPECTED_COMMIT or not re.fullmatch(r"[0-9a-f]{40}", EXPECTED_COMMIT):
        raise ValueError("authorization technical basis commit is incorrect")
    if basis.get("project_owner") != "jennerfeijoo" or basis.get("external_review_issue") != EXPECTED_ISSUE:
        raise ValueError("authorization basis owner or issue is incorrect")
    if basis.get("inherited_governance_record") != str(INHERITED_AUTH_PATH.relative_to(ROOT)):
        raise ValueError("inherited governance reference is incorrect")

    authority = auth.get("authority", {})
    if authority.get("type") != "project_owner_continuation_override":
        raise ValueError("authority type is incorrect")
    if authority.get("project_owner") != "jennerfeijoo":
        raise ValueError("authority owner is incorrect")
    if authority.get("assistant_internal_review_accepted_provisionally") is not True:
        raise ValueError("assistant review was not accepted provisionally")

    characterization = auth.get("review_characterization", {})
    if characterization.get("reviewer_system") != "GPT-5.6 Thinking":
        raise ValueError("reviewer system is incorrect")
    if characterization.get("human_disciplinary_review_completed") is not False:
        raise ValueError("authorization fabricates human review")
    if characterization.get("professional_endorsement_present") is not False:
        raise ValueError("authorization fabricates professional endorsement")
    if characterization.get("external_verification_deferred") is not True:
        raise ValueError("external verification is not deferred")

    require_true_map(
        auth.get("authorized_scope"),
        {
            "create_practice_implementation_contract",
            "implement_u2_p1_static_synthetic_characterization",
            "implement_u2_p2_first_order_dynamic_response",
            "implement_u2_p3_datasheet_audit",
            "create_synthetic_generators_and_negative_controls",
            "create_reproducibility_tests_and_internal_quality_gates",
            "revise_practice_documentation",
            "open_controlled_practice_pull_requests",
        },
        "authorized_scope",
    )
    require_true_map(
        auth.get("implementation_constraints"),
        {
            "synthetic_or_documentary_data_only",
            "human_data_forbidden",
            "connection_to_people_forbidden",
            "clinical_equipment_operation_forbidden",
            "network_independent_ci_required",
            "deterministic_seed_and_parameters_required",
            "negative_controls_required",
            "generated_outputs_must_not_be_committed",
            "component_claims_must_remain_conditioned_and_local",
            "no_clinical_or_regulatory_inference",
        },
        "implementation_constraints",
    )
    require_true_map(
        auth.get("not_authorized"),
        {
            "draft_full_theory",
            "create_authoral_unit_file",
            "public_release",
            "unit_developed_status",
            "course_promotion",
            "complete_status",
            "clinical_or_regulatory_validation_claims",
            "human_or_professional_endorsement_claims",
            "real_person_data_acquisition",
            "device_connection_to_people",
        },
        "not_authorized",
    )

    gate = auth.get("external_verification_gate", {})
    if gate.get("status") != "pending_external_professional_review":
        raise ValueError("external professional review is not pending")
    if gate.get("handoff") != str(HANDOFF_PATH.relative_to(ROOT)) or gate.get("operational_issue") != EXPECTED_ISSUE:
        raise ValueError("external review handoff or issue is incorrect")
    if not isinstance(gate.get("required_before"), list) or len(gate["required_before"]) != 6:
        raise ValueError("external verification boundaries are incomplete")


def validate_repository_state() -> None:
    inherited = load_json(INHERITED_AUTH_PATH)
    if inherited.get("authority", {}).get("project_owner") != "jennerfeijoo":
        raise ValueError("inherited governance record is invalid")
    handoff = load_json(HANDOFF_PATH)
    if handoff.get("status") != "ready_pending_external_review":
        raise ValueError("external handoff is not pending")
    if handoff.get("practice_implementation_authorized") is not False:
        raise ValueError("handoff fabricates professional practice authorization")
    if handoff.get("full_theory_drafting_authorized") is not False:
        raise ValueError("handoff authorizes theory")

    package = load_json(PACKAGE_PATH)
    if package.get("schema_version") != "2.0":
        raise ValueError("central package schema is not synchronized")
    if package.get("unit_02_provisional_practice_workstream") != "unit_02_practice_implementation_authorized_provisionally":
        raise ValueError("provisional workstream is not synchronized")
    section = package.get("unit_02_provisional_practice_authorization", {})
    if section.get("status") != "authorized_for_controlled_practice_implementation_provisionally":
        raise ValueError("central package authorization section is incorrect")
    if section.get("external_professional_review_status") != "pending_human_review":
        raise ValueError("central package erased pending external review")
    if section.get("full_theory_drafting_authorized") is not False:
        raise ValueError("central package authorizes theory")

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentation was promoted prematurely")
    if AUTHORAL_PATH.exists():
        raise ValueError("Unit 2 authoral file exists before theory authorization")
    if DECISION_PATH.exists() or MANIFEST_PATH.exists():
        raise ValueError("external review evidence was fabricated")

    if PRACTICE_PATH.exists():
        practice = load_json(PRACTICE_PATH)
        if practice.get("status") != "implemented_internal_review":
            raise ValueError("present practice implementation has an invalid status")
        if practice.get("provisional_internal_authorization") != str(AUTH_PATH.relative_to(ROOT)):
            raise ValueError("practice implementation does not reference this authorization")
        if practice.get("full_theory_drafting_authorized") is not False:
            raise ValueError("practice implementation expanded into theory")

    doc = DOC_PATH.read_text(encoding="utf-8")
    for marker in (
        "authorized_for_controlled_practice_implementation_provisionally",
        "project_owner_continuation_override",
        "issue `#161`",
        "No debe describirse como revisión humana",
        "full_theory_drafting_authorized: false",
    ):
        if marker not in doc:
            raise ValueError(f"authorization document lacks marker: {marker}")
    readiness = READINESS_PATH.read_text(encoding="utf-8")
    for marker in (
        "practice_implementation_authorized_provisionally: true",
        "external_professional_practice_authorization: false",
        "full_theory_drafting_authorized: false",
    ):
        if marker not in readiness:
            raise ValueError(f"AUTHORING_READINESS lacks marker: {marker}")


def main() -> int:
    try:
        validate_authorization(load_json(AUTH_PATH))
        validate_repository_state()
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U2 provisional practice authorization")
    print("owner override · internal practices allowed · external review pending · theory and publication blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
