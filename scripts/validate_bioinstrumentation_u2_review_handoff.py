#!/usr/bin/env python3
"""Validate the Bioinstrumentation U2 disciplinary review handoff."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from build_bioinstrumentation_u2_review_packet import PacketError, build_manifest, load_json
from evaluate_bioinstrumentation_u2_practice_authorization import (
    AuthorizationError,
    evaluate_decision,
    pending_report,
)

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-02.json"
TEMPLATE_PATH = ROOT / "data" / "review_templates" / "bioinstrumentacion" / "unit-02" / "disciplinary-review-decision-template.json"
FIXTURE_PATH = ROOT / "data" / "review_fixtures" / "bioinstrumentacion" / "unit-02" / "synthetic-approval-claim.json"
PROVISIONAL_AUTH_PATH = ROOT / "data" / "authoring_authorizations" / "bioinstrumentacion-unit-02-practices-provisional.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "REVIEW_HANDOFF_AND_AUTHORIZATION.md"
REQUEST_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "DISCIPLINARY_REVIEW_REQUEST.md"
READINESS_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "AUTHORING_READINESS.md"
AUTHORAL_UNIT_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"
PRACTICE_PATH = ROOT / "data" / "practice_implementations" / "bioinstrumentacion-unit-02.json"
TEST_COMMIT = "1111111111111111111111111111111111111111"


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} is insufficient")
    return text


def validate_contract(handoff: dict[str, Any]) -> None:
    expected_identity = {
        "handoff_id": "bioinstrumentacion-unit-02-disciplinary-review",
        "subject_id": "bioinstrumentacion",
        "unit_number": 2,
        "title": "Sensores, transductores y modelos estáticos y dinámicos",
        "status": "ready_pending_external_review",
        "course_editorial_state": "pending",
        "practice_implementation_authorized": False,
        "full_theory_drafting_authorized": False,
    }
    for key, value in expected_identity.items():
        if handoff.get(key) != value:
            raise ValueError(f"unexpected {key}: {handoff.get(key)!r}")
    require_text(handoff.get("purpose"), "purpose", 180)

    expected_paths = {
        "packet_builder": "scripts/build_bioinstrumentation_u2_review_packet.py",
        "decision_evaluator": "scripts/evaluate_bioinstrumentation_u2_practice_authorization.py",
        "validation": "scripts/validate_bioinstrumentation_u2_review_handoff.py",
        "decision_template": "data/review_templates/bioinstrumentacion/unit-02/disciplinary-review-decision-template.json",
        "future_decision_record": "data/review_evidence/bioinstrumentacion-unit-02-disciplinary-review.json",
        "future_packet_manifest": "data/review_evidence/bioinstrumentacion-unit-02-review-packet.json",
    }
    for key, value in expected_paths.items():
        if handoff.get(key) != value:
            raise ValueError(f"unexpected handoff path {key}")

    artifacts = handoff.get("required_artifacts")
    if not isinstance(artifacts, list) or len(artifacts) < 14:
        raise ValueError("review packet is incomplete")
    if len(set(artifacts)) != len(artifacts):
        raise ValueError("review packet contains duplicated artifacts")
    for relative in artifacts:
        if not isinstance(relative, str) or not (ROOT / relative).is_file():
            raise ValueError(f"review artifact is missing: {relative}")

    competence = handoff.get("reviewer_competence")
    if not isinstance(competence, dict):
        raise ValueError("reviewer competence contract is missing")
    if competence.get("minimum_qualified_categories") != 2:
        raise ValueError("reviewer competence minimum changed")
    if len(set(competence.get("allowed_categories", []))) != 5:
        raise ValueError("reviewer competence categories changed")

    allowed_decisions = handoff.get("allowed_decisions")
    if allowed_decisions != [
        "approve_for_practice_implementation",
        "approve_with_changes",
        "do_not_approve",
    ]:
        raise ValueError("allowed decisions changed unexpectedly")

    dimensions = handoff.get("score_dimensions")
    if dimensions != [
        "scientific_accuracy",
        "model_validity_and_limits",
        "source_traceability",
        "practice_reproducibility",
        "safety_and_scope",
        "learning_alignment",
    ]:
        raise ValueError("score dimensions changed unexpectedly")

    rule = handoff.get("authorization_rule")
    expected_rule = {
        "required_decision": "approve_for_practice_implementation",
        "minimum_score_each_dimension": 4,
        "maximum_score": 5,
        "critical_findings_must_be_empty": True,
        "required_changes_must_be_empty": True,
        "reviewer_confirmation_required": True,
        "reviewed_commit_required": True,
        "packet_digest_required": True,
        "synthetic_or_template_records_can_authorize": False,
        "machine_or_ci_actor_can_authorize": False,
        "approval_scope": "practice_implementation_only",
        "full_theory_drafting_authorized": False,
        "course_promotion_authorized": False,
        "unit_developed_authorized": False,
        "public_release_authorized": False,
    }
    if rule != expected_rule:
        raise ValueError("authorization rule changed unexpectedly")

    state = handoff.get("decision_state_now")
    expected_state = {
        "decision_record_present": False,
        "packet_manifest_present": False,
        "disciplinary_review_completed": False,
        "practice_implementation_authorized": False,
        "full_theory_drafting_authorized": False,
        "unit_developed": False,
        "course_state_after_block": "pending",
    }
    if state != expected_state:
        raise ValueError("current external decision state changed unexpectedly")


def validate_manifest(handoff: dict[str, Any]) -> dict[str, Any]:
    first = build_manifest(HANDOFF_PATH, TEST_COMMIT)
    second = build_manifest(HANDOFF_PATH, TEST_COMMIT)
    if first != second:
        raise ValueError("review packet manifest is not deterministic")
    if first.get("artifact_count") != len(handoff["required_artifacts"]):
        raise ValueError("review packet artifact count is incorrect")
    if first.get("contains_human_evidence") is not False:
        raise ValueError("packet manifest claims human evidence")
    if first.get("authorization_scope") != "practice_implementation_only":
        raise ValueError("packet manifest changed its authorization scope")
    if len(str(first.get("packet_digest_sha256", ""))) != 64:
        raise ValueError("packet digest is invalid")
    return first


def validate_template() -> None:
    template = load_json(TEMPLATE_PATH)
    if template.get("template_only") is not True:
        raise ValueError("decision template must be marked template_only")
    if template.get("synthetic") is not False:
        raise ValueError("decision template synthetic flag is incorrect")
    if template.get("human_evidence") is not False:
        raise ValueError("empty template claims human evidence")
    if template.get("authorization_requested") is not False:
        raise ValueError("empty template requests authorization")
    reviewer = template.get("reviewer", {})
    review = template.get("review", {})
    confirmation = template.get("confirmation", {})
    if any(reviewer.get(field) for field in ("name", "affiliation_or_context", "competence_note")):
        raise ValueError("decision template contains reviewer identity")
    if reviewer.get("competence_categories") != []:
        raise ValueError("decision template contains competence claims")
    if any(review.get(field) for field in ("review_date", "reviewed_commit", "packet_digest_sha256", "decision")):
        raise ValueError("decision template contains a review decision")
    if confirmation.get("actor_type") or confirmation.get("method") or confirmation.get("reference"):
        raise ValueError("decision template contains a confirmation")


def validate_synthetic_rejection(handoff: dict[str, Any], manifest: dict[str, Any]) -> None:
    fixture = copy.deepcopy(load_json(FIXTURE_PATH))
    fixture["review"]["packet_digest_sha256"] = manifest["packet_digest_sha256"]
    report = evaluate_decision(handoff, manifest, fixture)
    if report.get("practice_implementation_authorized") is not False:
        raise ValueError("synthetic approval claim authorized practices")
    failed = set(report.get("failed_checks", []))
    required_failures = {"not_synthetic", "human_evidence", "human_actor"}
    if not required_failures.issubset(failed):
        raise ValueError("synthetic approval blockers were not detected")

    modified = copy.deepcopy(fixture)
    modified["synthetic"] = False
    modified["human_evidence"] = True
    modified["confirmation"]["actor_type"] = "human_reviewer"
    modified["review"]["decision"] = "approve_with_changes"
    modified["review"]["required_changes"] = ["Revisar una tolerancia antes de implementar."]
    changed = evaluate_decision(handoff, manifest, modified)
    if changed.get("status") != "changes_required_no_authorization":
        raise ValueError("approve_with_changes was not routed correctly")
    if changed.get("practice_implementation_authorized") is not False:
        raise ValueError("approve_with_changes authorized practices")


def validate_provisional_separation() -> dict[str, Any]:
    authorization = load_json(PROVISIONAL_AUTH_PATH)
    if authorization.get("status") != "authorized_for_controlled_practice_implementation_provisionally":
        raise ValueError("provisional internal authorization is missing or invalid")
    characterization = authorization.get("review_characterization", {})
    if characterization.get("human_disciplinary_review_completed") is not False:
        raise ValueError("provisional authorization fabricates human review")
    if characterization.get("professional_endorsement_present") is not False:
        raise ValueError("provisional authorization fabricates professional endorsement")
    if authorization.get("external_verification_gate", {}).get("status") != "pending_external_professional_review":
        raise ValueError("provisional authorization erased the external gate")
    if authorization.get("not_authorized", {}).get("draft_full_theory") is not True:
        raise ValueError("provisional authorization expanded into theory drafting")
    return authorization


def validate_repository_state(handoff: dict[str, Any]) -> None:
    future_decision = ROOT / str(handoff.get("future_decision_record"))
    future_manifest = ROOT / str(handoff.get("future_packet_manifest"))
    if future_decision.exists() or future_manifest.exists():
        raise ValueError("human review evidence must not be fabricated in this block")

    pending = pending_report(handoff)
    if pending.get("status") != "pending_human_review":
        raise ValueError("missing evidence did not produce pending status")
    if pending.get("practice_implementation_authorized") is not False:
        raise ValueError("missing professional evidence authorized practices")
    if pending.get("controlled_full_theory_drafting_authorized") is not False:
        raise ValueError("missing evidence authorized full theory")

    provisional = validate_provisional_separation()
    scope = provisional.get("authorized_scope", {})
    if not all(
        scope.get(key) is True
        for key in (
            "implement_u2_p1_static_synthetic_characterization",
            "implement_u2_p2_first_order_dynamic_response",
            "implement_u2_p3_datasheet_audit",
        )
    ):
        raise ValueError("provisional practice scope is incomplete")

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentation was promoted prematurely")
    if AUTHORAL_UNIT_PATH.exists():
        raise ValueError("U2 authoral unit exists before theory authorization")
    if PRACTICE_PATH.exists() and provisional.get("status") != "authorized_for_controlled_practice_implementation_provisionally":
        raise ValueError("U2 practices exist without provisional or professional authorization")

    for path, markers in (
        (
            DOC_PATH,
            (
                "Paquete de entrega y autorización",
                "approve_for_practice_implementation",
                "manifiesto SHA-256",
                "Autorización provisional del propietario",
                "external_professional_review: pending_human_review",
            ),
        ),
        (
            REQUEST_PATH,
            (
                "review_handoffs/bioinstrumentacion-unit-02.json",
                "disciplinary-review-decision-template.json",
                "REVIEW_HANDOFF_AND_AUTHORIZATION.md",
                "issue `#161`",
                "authoring_authorizations/bioinstrumentacion-unit-02-practices-provisional.json",
            ),
        ),
        (
            READINESS_PATH,
            (
                "technical_blockers_resolved: true",
                "review_handoff: ready_pending_external_review",
                "practice_implementation_authorized_provisionally: true",
                "external_professional_practice_authorization: false",
                "full_theory_drafting_authorized: false",
            ),
        ),
    ):
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                raise ValueError(f"{path.name} lacks marker: {marker}")


def main() -> int:
    try:
        handoff = load_json(HANDOFF_PATH)
        validate_contract(handoff)
        manifest = validate_manifest(handoff)
        validate_template()
        validate_synthetic_rejection(handoff, manifest)
        validate_repository_state(handoff)
    except (OSError, ValueError, TypeError, json.JSONDecodeError, PacketError, AuthorizationError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U2 disciplinary review handoff")
    print("deterministic packet · synthetic approval rejected · professional review pending · provisional internal practice scope separated · course pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
