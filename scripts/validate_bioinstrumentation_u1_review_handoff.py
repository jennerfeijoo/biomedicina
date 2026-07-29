#!/usr/bin/env python3
"""Validate the Bioinstrumentation U1 disciplinary review handoff."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from build_bioinstrumentation_u1_review_packet import PacketError, build_manifest, load_json
from evaluate_bioinstrumentation_u1_authorization import (
    AuthorizationError,
    evaluate_decision,
    pending_report,
)

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-01.json"
TEMPLATE_PATH = ROOT / "data" / "review_templates" / "bioinstrumentacion" / "unit-01" / "disciplinary-review-decision-template.json"
FIXTURE_PATH = ROOT / "data" / "review_fixtures" / "bioinstrumentacion" / "unit-01" / "synthetic-approval-claim.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01" / "REVIEW_HANDOFF_AND_AUTHORIZATION.md"
REQUEST_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01" / "DISCIPLINARY_REVIEW_REQUEST.md"
AUTHORAL_UNIT_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-01.json"
TEST_COMMIT = "1111111111111111111111111111111111111111"


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} is insufficient")
    return text


def validate_contract(handoff: dict[str, Any]) -> None:
    if handoff.get("handoff_id") != "bioinstrumentacion-unit-01-disciplinary-review":
        raise ValueError("unexpected handoff id")
    if handoff.get("status") != "ready_pending_external_review":
        raise ValueError("handoff must remain pending external review")
    if handoff.get("course_editorial_state") != "pending":
        raise ValueError("handoff changed the course state")
    if handoff.get("full_theory_drafting_authorized") is not False:
        raise ValueError("handoff prematurely authorizes theory drafting")
    artifacts = handoff.get("required_artifacts")
    if not isinstance(artifacts, list) or len(artifacts) < 20:
        raise ValueError("review packet is incomplete")
    if len(set(artifacts)) != len(artifacts):
        raise ValueError("review packet contains duplicated artifacts")
    for relative in artifacts:
        if not (ROOT / relative).is_file():
            raise ValueError(f"review artifact is missing: {relative}")
    competence = handoff.get("reviewer_competence")
    if not isinstance(competence, dict):
        raise ValueError("reviewer competence contract is missing")
    if competence.get("minimum_qualified_categories") != 2:
        raise ValueError("reviewer competence minimum changed")
    if len(set(competence.get("allowed_categories", []))) != 5:
        raise ValueError("reviewer competence categories changed")
    rule = handoff.get("authorization_rule")
    if not isinstance(rule, dict):
        raise ValueError("authorization rule is missing")
    expected = {
        "required_decision": "approve_for_controlled_drafting",
        "minimum_score_each_dimension": 4,
        "maximum_score": 5,
        "critical_findings_must_be_empty": True,
        "required_changes_must_be_empty": True,
        "reviewer_confirmation_required": True,
        "reviewed_commit_required": True,
        "packet_digest_required": True,
        "synthetic_or_template_records_can_authorize": False,
        "machine_or_ci_actor_can_authorize": False,
        "approval_scope": "controlled_full_theory_drafting_only",
        "course_promotion_authorized": False,
        "unit_developed_authorized": False,
    }
    if rule != expected:
        raise ValueError("authorization rule changed unexpectedly")


def validate_manifest(handoff: dict[str, Any]) -> dict[str, Any]:
    first = build_manifest(HANDOFF_PATH, TEST_COMMIT)
    second = build_manifest(HANDOFF_PATH, TEST_COMMIT)
    if first != second:
        raise ValueError("review packet manifest is not deterministic")
    if first.get("artifact_count") != len(handoff["required_artifacts"]):
        raise ValueError("review packet artifact count is incorrect")
    if first.get("contains_human_evidence") is not False:
        raise ValueError("packet manifest claims human evidence")
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
    fixture = load_json(FIXTURE_PATH)
    fixture = copy.deepcopy(fixture)
    fixture["review"]["packet_digest_sha256"] = manifest["packet_digest_sha256"]
    report = evaluate_decision(handoff, manifest, fixture)
    if report.get("controlled_full_theory_drafting_authorized") is not False:
        raise ValueError("synthetic approval claim authorized drafting")
    failed = set(report.get("failed_checks", []))
    required_failures = {"not_synthetic", "human_evidence", "human_actor"}
    if not required_failures.issubset(failed):
        raise ValueError("synthetic approval blockers were not detected")
    modified = copy.deepcopy(fixture)
    modified["synthetic"] = False
    modified["human_evidence"] = True
    modified["confirmation"]["actor_type"] = "human_reviewer"
    modified["review"]["decision"] = "approve_with_changes"
    changed = evaluate_decision(handoff, manifest, modified)
    if changed.get("status") != "changes_required_no_authorization":
        raise ValueError("approve_with_changes was not routed correctly")
    if changed.get("controlled_full_theory_drafting_authorized") is not False:
        raise ValueError("approve_with_changes authorized drafting")


def validate_repository_state(handoff: dict[str, Any]) -> None:
    future_decision = ROOT / str(handoff.get("future_decision_record"))
    future_manifest = ROOT / str(handoff.get("future_packet_manifest"))
    if future_decision.exists() or future_manifest.exists():
        raise ValueError("human review evidence must not be fabricated in this block")
    pending = pending_report(handoff)
    if pending.get("status") != "pending_human_review":
        raise ValueError("missing evidence did not produce pending status")
    if pending.get("controlled_full_theory_drafting_authorized") is not False:
        raise ValueError("missing evidence authorized drafting")

    package = load_json(PACKAGE_PATH)
    if package.get("current_phase") != "unit_01_authoring_preparation_review":
        raise ValueError("historical preparation phase changed")
    if package.get("human_review_workstream") != "unit_01_human_review_protocol_ready":
        raise ValueError("human review protocol workstream changed")
    if package.get("review_handoff_workstream") != "unit_01_disciplinary_review_handoff_ready":
        raise ValueError("review handoff workstream is not synchronized")
    handoff_section = package.get("disciplinary_review_handoff")
    if not isinstance(handoff_section, dict):
        raise ValueError("package disciplinary review handoff is missing")
    if handoff_section.get("status") != "ready_pending_external_review":
        raise ValueError("package handoff status is incorrect")
    if handoff_section.get("controlled_drafting_authorized") is not False:
        raise ValueError("package claims drafting authorization")
    if handoff_section.get("human_evidence_present") is not False:
        raise ValueError("package claims human evidence")

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if AUTHORAL_UNIT_PATH.exists():
        raise ValueError("authoral unit exists before disciplinary approval")

    for path, markers in (
        (
            DOC_PATH,
            (
                "Paquete de entrega y autorización",
                "approve_for_controlled_drafting",
                "manifiesto SHA-256",
                "no desarrolla la unidad",
                "pending_human_review",
            ),
        ),
        (
            REQUEST_PATH,
            (
                "review_handoffs/bioinstrumentacion-unit-01.json",
                "disciplinary-review-decision-template.json",
                "REVIEW_HANDOFF_AND_AUTHORIZATION.md",
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
    print("OK Bioinstrumentation U1 disciplinary review handoff")
    print("deterministic packet · synthetic approval rejected · human review pending · course pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
