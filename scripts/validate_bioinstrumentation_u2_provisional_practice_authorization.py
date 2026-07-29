#!/usr/bin/env python3
"""Validate the provisional owner authorization for Bioinstrumentation U2 practices."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH_PATH = ROOT / "data" / "authoring_authorizations" / "bioinstrumentacion-unit-02-practices-provisional.json"
INHERITED_AUTH_PATH = ROOT / "data" / "authoring_authorizations" / "bioinstrumentacion-unit-01-provisional.json"
HANDOFF_PATH = ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-02.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "PROVISIONAL_PRACTICE_IMPLEMENTATION_AUTHORIZATION.md"
READINESS_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "AUTHORING_READINESS.md"
HANDOFF_DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "REVIEW_HANDOFF_AND_AUTHORIZATION.md"
PRACTICE_PATH = ROOT / "data" / "practice_implementations" / "bioinstrumentacion-unit-02.json"
AUTHORAL_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"
DECISION_PATH = ROOT / "data" / "review_evidence" / "bioinstrumentacion-unit-02-disciplinary-review.json"
MANIFEST_PATH = ROOT / "data" / "review_evidence" / "bioinstrumentacion-unit-02-review-packet.json"
EXPECTED_BASE_COMMIT = "b8134a50a9fea89fe896b167d5791d17ee055e5c"
EXPECTED_ISSUE = 161


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return payload


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} is insufficient")
    return text


def validate_identity(auth: dict[str, Any]) -> None:
    expected = {
        "authorization_id": "bioinstrumentacion-unit-02-provisional-practice-implementation",
        "subject_id": "bioinstrumentacion",
        "unit_number": 2,
        "status": "authorized_for_controlled_practice_implementation_provisionally",
        "effective_date": "2026-07-29",
    }
    for field, wanted in expected.items():
        if auth.get(field) != wanted:
            raise ValueError(f"authorization {field} is incorrect")

    basis = auth.get("authorization_basis")
    if not isinstance(basis, dict):
        raise ValueError("authorization basis is missing")
    if basis.get("technical_basis_commit") != EXPECTED_BASE_COMMIT:
        raise ValueError("technical basis commit is incorrect")
    if not re.fullmatch(r"[0-9a-f]{40}", str(basis.get("technical_basis_commit", ""))):
        raise ValueError("technical basis commit format is invalid")
    if basis.get("continuation_instruction_at") != "2026-07-29T19:27:11Z":
        raise ValueError("continuation instruction timestamp is incorrect")
    if basis.get("project_owner") != "jennerfeijoo":
        raise ValueError("project owner is incorrect")
    if basis.get("inherited_governance_record") != str(INHERITED_AUTH_PATH.relative_to(ROOT)):
        raise ValueError("inherited governance record is incorrect")
    if basis.get("external_review_issue") != EXPECTED_ISSUE:
        raise ValueError("external review issue is incorrect")
    require_text(basis.get("interpretation"), "authorization_basis.interpretation", 150)


def validate_authority(auth: dict[str, Any]) -> None:
    authority = auth.get("authority")
    if not isinstance(authority, dict):
        raise ValueError("authority contract is missing")
    if authority.get("type") != "project_owner_continuation_override":
        raise ValueError("authority type is incorrect")
    if authority.get("project_owner") != "jennerfeijoo":
        raise ValueError("authority project owner is incorrect")
    if authority.get("instruction_recorded_by") != "OpenAI assistant":
        raise ValueError("instruction recorder is incorrect")
    if authority.get("assistant_internal_review_accepted_provisionally") is not True:
        raise ValueError("assistant internal review was not accepted provisionally")
    require_text(authority.get("instruction_summary"), "authority.instruction_summary", 180)

    characterization = auth.get("review_characterization")
    if not isinstance(characterization, dict):
        raise ValueError("review characterization is missing")
    if characterization.get("review_type") != "internal_ai_and_ci_review_accepted_by_project_owner":
        raise ValueError("review characterization type is incorrect")
    if characterization.get("reviewer_system") != "GPT-5.6 Thinking":
        raise ValueError("reviewer system is incorrect")
    if characterization.get("human_disciplinary_review_completed") is not False:
        raise ValueError("authorization fabricates human review")
    if characterization.get("professional_endorsement_present") is not False:
        raise ValueError("authorization fabricates professional endorsement")
    if characterization.get("external_verification_deferred") is not True:
        raise ValueError("external verification must remain deferred")
    if characterization.get("external_review_issue") != EXPECTED_ISSUE:
        raise ValueError("review characterization issue is incorrect")
    require_text(characterization.get("claim_limit"), "review_characterization.claim_limit", 150)


def validate_scope(auth: dict[str, Any]) -> None:
    expected_scope = {
        "create_practice_implementation_contract",
        "implement_u2_p1_static_synthetic_characterization",
        "implement_u2_p2_first_order_dynamic_response",
        "implement_u2_p3_datasheet_audit",
        "create_synthetic_generators_and_negative_controls",
        "create_reproducibility_tests_and_internal_quality_gates",
        "revise_practice_documentation",
        "open_controlled_practice_pull_requests",
    }
    scope = auth.get("authorized_scope")
    if not isinstance(scope, dict) or set(scope) != expected_scope:
        raise ValueError("authorized scope changed unexpectedly")
    if any(value is not True for value in scope.values()):
        raise ValueError("controlled practice scope is incomplete")

    expected_constraints = {
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
    }
    constraints = auth.get("implementation_constraints")
    if not isinstance(constraints, dict) or set(constraints) != expected_constraints:
        raise ValueError("implementation constraints changed unexpectedly")
    if any(value is not True for value in constraints.values()):
        raise ValueError("an implementation constraint was disabled")

    expected_prohibitions = {
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
    }
    prohibited = auth.get("not_authorized")
    if not isinstance(prohibited, dict) or set(prohibited) != expected_prohibitions:
        raise ValueError("prohibition contract changed unexpectedly")
    if any(value is not True for value in prohibited.values()):
        raise ValueError("a prohibited effect was enabled")


def validate_external_gate(auth: dict[str, Any]) -> None:
    gate = auth.get("external_verification_gate")
    if not isinstance(gate, dict):
        raise ValueError("external verification gate is missing")
    if gate.get("status") != "pending_external_professional_review":
        raise ValueError("external professional review is not pending")
    if gate.get("handoff") != str(HANDOFF_PATH.relative_to(ROOT)):
        raise ValueError("external handoff reference is incorrect")
    if gate.get("decision_template") != "data/review_templates/bioinstrumentacion/unit-02/disciplinary-review-decision-template.json":
        raise ValueError("external decision template reference is incorrect")
    if gate.get("operational_issue") != EXPECTED_ISSUE:
        raise ValueError("external operational issue is incorrect")
    required_before = gate.get("required_before")
    if not isinstance(required_before, list) or len(required_before) != 6:
        raise ValueError("external verification boundaries are incomplete")

    state = auth.get("editorial_state_after_authorization")
    expected_state = {
        "course_state": "pending",
        "unit_state": "practice_implementation_authorized_provisionally",
        "practice_state": "controlled_internal_implementation_authorized",
        "theory_state": "blocked_pending_separate_authorization",
        "publication_state": "blocked_pending_external_verification",
        "professional_review_state": "pending_human_review",
    }
    if state != expected_state:
        raise ValueError("editorial state after authorization is incorrect")

    revocation = auth.get("revocation")
    expected_revocation = {
        "revocable_by_project_owner": True,
        "superseded_by_verified_external_decision": True,
        "material_scope_change_requires_new_authorization": True,
        "failed_internal_gate_suspends_implementation": True,
    }
    if revocation != expected_revocation:
        raise ValueError("revocation contract is incorrect")


def validate_package_state(auth: dict[str, Any]) -> None:
    package = load_json(PACKAGE_PATH)
    if package.get("schema_version") != "1.9":
        raise ValueError("central package schema version is not synchronized")
    expected_workstreams = {
        "unit_02_preparation_workstream": "unit_02_authoring_preparation_review",
        "unit_02_blocker_workstream": "unit_02_technical_blockers_resolved_review_pending",
        "unit_02_review_handoff_workstream": "unit_02_disciplinary_review_handoff_ready",
        "unit_02_provisional_practice_workstream": "unit_02_practice_implementation_authorized_provisionally",
    }
    for field, wanted in expected_workstreams.items():
        if package.get(field) != wanted:
            raise ValueError(f"central package {field} is not synchronized")

    preparation = package.get("unit_02_preparation")
    if not isinstance(preparation, dict):
        raise ValueError("central package lacks Unit 2 preparation")
    if preparation.get("status") != "authoring_preparation_review":
        raise ValueError("central package changed Unit 2 preparation status")
    if preparation.get("practice_implementation_present") is not False:
        raise ValueError("authorization block claims Unit 2 practices are already implemented")
    if preparation.get("authoral_unit_present") is not False:
        raise ValueError("central package claims a Unit 2 authoral file")

    blockers = package.get("unit_02_blocker_resolution")
    if not isinstance(blockers, dict) or blockers.get("technical_blockers_resolved") is not True:
        raise ValueError("central package does not preserve resolved Unit 2 blockers")
    if blockers.get("practice_implementation_authorized_professionally") is not False:
        raise ValueError("central package fabricates professional practice authorization")

    handoff = package.get("unit_02_disciplinary_review_handoff")
    if not isinstance(handoff, dict):
        raise ValueError("central package lacks Unit 2 handoff")
    if handoff.get("status") != "ready_pending_external_review":
        raise ValueError("central package changed external review status")
    if handoff.get("operational_issue") != EXPECTED_ISSUE:
        raise ValueError("central package external issue is incorrect")
    if handoff.get("human_evidence_present") is not False:
        raise ValueError("central package fabricates human evidence")
    if handoff.get("practice_implementation_authorized_professionally") is not False:
        raise ValueError("central package fabricates professional approval")

    section = package.get("unit_02_provisional_practice_authorization")
    expected_section = {
        "status": "authorized_for_controlled_practice_implementation_provisionally",
        "record": str(AUTH_PATH.relative_to(ROOT)),
        "document": str(DOC_PATH.relative_to(ROOT)),
        "validation": "scripts/validate_bioinstrumentation_u2_provisional_practice_authorization.py",
        "authority": "project_owner_continuation_override",
        "technical_basis_commit": EXPECTED_BASE_COMMIT,
        "operational_issue": EXPECTED_ISSUE,
        "practice_ids": ["U2-P1", "U2-P2", "U2-P3"],
        "controlled_internal_practice_implementation_authorized": True,
        "external_professional_review_status": "pending_human_review",
        "professional_endorsement_present": False,
        "full_theory_drafting_authorized": False,
        "authoral_unit_present": False,
        "public_release_authorized": False,
        "unit_developed": False,
        "course_state": "pending",
        "editorial_effect": "internal_practice_implementation_only",
    }
    if section != expected_section:
        raise ValueError("central package provisional practice section is incorrect")

    if auth.get("status") != section.get("status"):
        raise ValueError("authorization record and central package disagree")


def validate_repository_state(auth: dict[str, Any]) -> None:
    inherited = load_json(INHERITED_AUTH_PATH)
    if inherited.get("authority", {}).get("project_owner") != "jennerfeijoo":
        raise ValueError("inherited owner governance record is invalid")
    if inherited.get("review_characterization", {}).get("human_disciplinary_review_completed") is not False:
        raise ValueError("inherited governance record fabricates human review")

    handoff = load_json(HANDOFF_PATH)
    if handoff.get("status") != "ready_pending_external_review":
        raise ValueError("U2 handoff must remain pending external review")
    if handoff.get("practice_implementation_authorized") is not False:
        raise ValueError("external handoff was rewritten as professionally authorized")
    if handoff.get("full_theory_drafting_authorized") is not False:
        raise ValueError("external handoff authorizes theory")
    if handoff.get("decision_state_now", {}).get("disciplinary_review_completed") is not False:
        raise ValueError("handoff fabricates completed disciplinary review")

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentation was promoted prematurely")

    if PRACTICE_PATH.exists():
        raise ValueError("authorization block must not implement U2 practices")
    if AUTHORAL_PATH.exists():
        raise ValueError("authorization block must not create the U2 authoral unit")
    if DECISION_PATH.exists() or MANIFEST_PATH.exists():
        raise ValueError("authorization block must not fabricate external review evidence")

    doc = DOC_PATH.read_text(encoding="utf-8")
    for marker in (
        "authorized_for_controlled_practice_implementation_provisionally",
        "project_owner_continuation_override",
        "issue `#161`",
        "crear `data/practice_implementations/bioinstrumentacion-unit-02.json`",
        "No debe describirse como revisión humana",
        "full_theory_drafting_authorized: false",
    ):
        if marker not in doc:
            raise ValueError(f"provisional authorization document lacks marker: {marker}")

    readiness = READINESS_PATH.read_text(encoding="utf-8")
    for marker in (
        "practice_implementation_authorized_provisionally: true",
        "external_professional_practice_authorization: false",
        "Autorización provisional de prácticas",
        "implementar U2-P1",
        "teoría completa y la publicación continúan bloqueadas",
    ):
        if marker not in readiness:
            raise ValueError(f"AUTHORING_READINESS lacks marker: {marker}")

    handoff_doc = HANDOFF_DOC_PATH.read_text(encoding="utf-8")
    for marker in (
        "authorized_provisionally_by_project_owner",
        "Autorización provisional del propietario",
        "no debe registrarse como `approve_for_practice_implementation`",
        "external_professional_review: pending_human_review",
        "provisional_internal_practice_authorization: true",
    ):
        if marker not in handoff_doc:
            raise ValueError(f"review handoff document lacks marker: {marker}")


def main() -> int:
    try:
        auth = load_json(AUTH_PATH)
        validate_identity(auth)
        validate_authority(auth)
        validate_scope(auth)
        validate_external_gate(auth)
        validate_package_state(auth)
        validate_repository_state(auth)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U2 provisional practice authorization")
    print("owner continuation override · internal practices enabled · external review pending · theory and publication blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
