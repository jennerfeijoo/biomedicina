#!/usr/bin/env python3
"""Validate the provisional owner authorization for Bioinstrumentation unit 1."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH_PATH = ROOT / "data" / "authoring_authorizations" / "bioinstrumentacion-unit-01-provisional.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
HANDOFF_PATH = ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-01.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01" / "PROVISIONAL_AUTHORING_AUTHORIZATION.md"
READINESS_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01" / "AUTHORING_READINESS.md"
AUTHORAL_UNIT_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-01.json"
EXPECTED_BASE_COMMIT = "e702bf18af9f5bdce189ffd7ceda3aa378753945"


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


def require_text(value: Any, label: str, minimum: int = 10) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} is insufficient")
    return text


def validate_authorization(auth: dict[str, Any]) -> None:
    expected_identity = {
        "authorization_id": "bioinstrumentacion-unit-01-provisional-authoring",
        "subject_id": "bioinstrumentacion",
        "unit_number": 1,
        "status": "authorized_for_controlled_drafting_provisionally",
        "effective_date": "2026-07-29",
        "authorization_basis_commit": EXPECTED_BASE_COMMIT,
    }
    for field, expected in expected_identity.items():
        if auth.get(field) != expected:
            raise ValueError(f"authorization {field} is incorrect")
    if not re.fullmatch(r"[0-9a-f]{40}", str(auth.get("authorization_basis_commit", ""))):
        raise ValueError("authorization basis commit is invalid")

    authority = auth.get("authority")
    if not isinstance(authority, dict):
        raise ValueError("authority contract is missing")
    if authority.get("type") != "project_owner_override":
        raise ValueError("authorization must be a project owner override")
    if authority.get("project_owner") != "jennerfeijoo":
        raise ValueError("project owner is incorrect")
    if authority.get("instruction_recorded_by") != "OpenAI assistant":
        raise ValueError("instruction recorder is incorrect")
    if authority.get("assistant_review_accepted_provisionally") is not True:
        raise ValueError("assistant review was not accepted provisionally")
    require_text(authority.get("instruction_summary"), "authority.instruction_summary", 100)

    characterization = auth.get("review_characterization")
    if not isinstance(characterization, dict):
        raise ValueError("review characterization is missing")
    if characterization.get("review_type") != "internal_ai_review_accepted_by_project_owner":
        raise ValueError("review type is incorrect")
    if characterization.get("human_disciplinary_review_completed") is not False:
        raise ValueError("authorization fabricates completed human review")
    if characterization.get("professional_endorsement_present") is not False:
        raise ValueError("authorization fabricates professional endorsement")
    if characterization.get("external_verification_deferred") is not True:
        raise ValueError("external verification must remain deferred")
    if characterization.get("external_review_issue") != 154:
        raise ValueError("external review issue is not preserved")
    require_text(characterization.get("claim_limit"), "review_characterization.claim_limit", 100)

    scope = auth.get("authorized_scope")
    expected_scope = {
        "create_authoral_unit_draft",
        "draft_full_theory",
        "revise_examples_assessments_feedback_and_practices",
        "open_controlled_authoring_pull_requests",
        "run_internal_quality_gates",
    }
    if not isinstance(scope, dict) or set(scope) != expected_scope:
        raise ValueError("authorized scope changed unexpectedly")
    if any(value is not True for value in scope.values()):
        raise ValueError("controlled authoring scope is incomplete")

    prohibited = auth.get("not_authorized")
    expected_prohibitions = {
        "public_release",
        "unit_developed_status",
        "course_promotion",
        "complete_status",
        "clinical_or_regulatory_validation_claims",
        "human_or_professional_endorsement_claims",
    }
    if not isinstance(prohibited, dict) or set(prohibited) != expected_prohibitions:
        raise ValueError("prohibition contract changed unexpectedly")
    if any(value is not True for value in prohibited.values()):
        raise ValueError("a prohibited editorial effect was enabled")

    external = auth.get("external_verification_gate")
    if not isinstance(external, dict):
        raise ValueError("external verification gate is missing")
    if external.get("status") != "pending_external_professional_review":
        raise ValueError("external review is not pending")
    if external.get("operational_issue") != 154:
        raise ValueError("operational issue is incorrect")
    required_before = external.get("required_before")
    if not isinstance(required_before, list) or len(required_before) < 5:
        raise ValueError("external verification boundaries are incomplete")

    state = auth.get("editorial_state_after_authorization")
    expected_state = {
        "course_state": "pending",
        "unit_state": "controlled_authoring_authorized",
        "publication_state": "blocked_pending_external_verification",
        "professional_review_state": "pending_human_review",
    }
    if state != expected_state:
        raise ValueError("editorial state after authorization is incorrect")


def validate_repository_state(auth: dict[str, Any]) -> None:
    package = load_json(PACKAGE_PATH)
    if package.get("current_phase") != "unit_01_authoring_preparation_review":
        raise ValueError("historical preparation phase changed")
    if package.get("provisional_authoring_workstream") != "unit_01_controlled_authoring_authorized_provisionally":
        raise ValueError("provisional authoring workstream is not synchronized")
    section = package.get("provisional_authoring_authorization")
    if not isinstance(section, dict):
        raise ValueError("package authorization section is missing")
    expected_package = {
        "status": "authorized_for_controlled_drafting_provisionally",
        "record": str(AUTH_PATH.relative_to(ROOT)),
        "authority": "project_owner_override",
        "assistant_review_accepted_provisionally": True,
        "controlled_authoring_authorized": True,
        "external_professional_review_status": "pending_human_review",
        "professional_endorsement_present": False,
        "public_release_authorized": False,
        "unit_developed": False,
        "course_state": "pending",
        "editorial_effect": "controlled_authoring_only",
    }
    if section != expected_package:
        raise ValueError("package authorization section is incorrect")

    handoff = load_json(HANDOFF_PATH)
    if handoff.get("status") != "ready_pending_external_review":
        raise ValueError("external handoff no longer remains pending")
    if handoff.get("full_theory_drafting_authorized") is not False:
        raise ValueError("historical external handoff was rewritten")

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentation was promoted prematurely")
    if AUTHORAL_UNIT_PATH.exists():
        raise ValueError("this authorization block must not create the authoral unit")

    doc = DOC_PATH.read_text(encoding="utf-8")
    for marker in (
        "authorized_for_controlled_drafting_provisionally",
        "project_owner_override",
        "No constituye revisión humana disciplinar",
        "crear `data/course_redevelopment/bioinstrumentacion/units/unit-01.json`",
        "publicación: `blocked_pending_external_verification`",
    ):
        if marker not in doc:
            raise ValueError(f"authorization document lacks marker: {marker}")

    readiness = READINESS_PATH.read_text(encoding="utf-8")
    for marker in (
        "Autorización provisional de autoría",
        "controlled_authoring_authorized",
        "revisión profesional externa sigue pendiente",
        "curso permanece `pending`",
    ):
        if marker not in readiness:
            raise ValueError(f"AUTHORING_READINESS lacks marker: {marker}")


def main() -> int:
    try:
        auth = load_json(AUTH_PATH)
        validate_authorization(auth)
        validate_repository_state(auth)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U1 provisional authoring authorization")
    print("owner override · AI review accepted provisionally · controlled authoring enabled · external review pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
