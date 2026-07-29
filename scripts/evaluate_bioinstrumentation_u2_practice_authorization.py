#!/usr/bin/env python3
"""Evaluate whether a disciplinary review authorizes U2 practice implementation."""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HANDOFF = ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-02.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
CONFIRMATION_METHODS = {
    "github_review",
    "verified_email_attestation",
    "signed_document_reference",
    "institutional_review_record",
    "other_verifiable",
}


class AuthorizationError(ValueError):
    """Raised when review evidence cannot be evaluated."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuthorizationError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AuthorizationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AuthorizationError(f"{path} must contain an object")
    return payload


def _nonempty(value: Any, minimum: int = 1) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum


def _valid_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def evaluate_decision(
    handoff: dict[str, Any], manifest: dict[str, Any], decision: dict[str, Any]
) -> dict[str, Any]:
    competence = handoff.get("reviewer_competence", {})
    rule = handoff.get("authorization_rule", {})
    dimensions = handoff.get("score_dimensions", [])
    reviewer = decision.get("reviewer", {})
    review = decision.get("review", {})
    confirmation = decision.get("confirmation", {})
    scores = review.get("scores", {})

    allowed_categories = set(competence.get("allowed_categories", []))
    selected_categories = reviewer.get("competence_categories", [])
    allowed_decisions = set(handoff.get("allowed_decisions", []))
    required_decision = rule.get("required_decision")
    minimum_score = int(rule.get("minimum_score_each_dimension", 0))
    maximum_score = int(rule.get("maximum_score", 0))

    checks: dict[str, bool] = {
        "handoff_matches": decision.get("handoff_id") == handoff.get("handoff_id")
        and manifest.get("handoff_id") == handoff.get("handoff_id"),
        "not_template": decision.get("template_only") is False,
        "not_synthetic": decision.get("synthetic") is False,
        "human_evidence": decision.get("human_evidence") is True,
        "human_actor": confirmation.get("actor_type") == "human_reviewer",
        "reviewer_name": _nonempty(reviewer.get("name"), 3),
        "reviewer_context": _nonempty(reviewer.get("affiliation_or_context"), 3),
        "competence_note": _nonempty(reviewer.get("competence_note"), 20),
        "competence_categories": isinstance(selected_categories, list)
        and len(set(selected_categories)) >= int(competence.get("minimum_qualified_categories", 0))
        and set(selected_categories).issubset(allowed_categories),
        "review_date": _valid_iso_date(review.get("review_date")),
        "reviewed_commit_format": isinstance(review.get("reviewed_commit"), str)
        and bool(HEX40.fullmatch(review["reviewed_commit"])),
        "packet_digest_format": isinstance(review.get("packet_digest_sha256"), str)
        and bool(HEX64.fullmatch(review["packet_digest_sha256"])),
        "reviewed_commit_matches_manifest": review.get("reviewed_commit")
        == manifest.get("reviewed_commit"),
        "packet_digest_matches_manifest": review.get("packet_digest_sha256")
        == manifest.get("packet_digest_sha256"),
        "manifest_scope": manifest.get("authorization_scope") == "practice_implementation_only",
        "decision_allowed": review.get("decision") in allowed_decisions,
        "decision_authorizes": review.get("decision") == required_decision,
        "score_dimensions_exact": isinstance(scores, dict)
        and set(scores) == set(dimensions),
        "scores_in_range": isinstance(scores, dict)
        and all(
            isinstance(scores.get(dimension), int)
            and 1 <= scores[dimension] <= maximum_score
            for dimension in dimensions
        ),
        "scores_meet_minimum": isinstance(scores, dict)
        and all(
            isinstance(scores.get(dimension), int)
            and scores[dimension] >= minimum_score
            for dimension in dimensions
        ),
        "critical_findings_empty": review.get("critical_findings") == [],
        "required_changes_empty": review.get("required_changes") == [],
        "confirmation_method": confirmation.get("method") in CONFIRMATION_METHODS,
        "confirmation_reference": _nonempty(confirmation.get("reference"), 8),
        "confirmation_statement": _nonempty(confirmation.get("statement"), 60),
        "authorization_requested": decision.get("authorization_requested") is True,
        "manifest_not_human_evidence": manifest.get("contains_human_evidence") is False,
    }
    authorization = all(checks.values())
    if authorization:
        status = "authorized_for_practice_implementation"
    elif review.get("decision") == "approve_with_changes":
        status = "changes_required_no_authorization"
    elif review.get("decision") == "do_not_approve":
        status = "not_approved"
    else:
        status = "invalid_or_incomplete_no_authorization"

    return {
        "schema_version": "1.0",
        "handoff_id": handoff.get("handoff_id"),
        "status": status,
        "practice_implementation_authorized": authorization,
        "controlled_full_theory_drafting_authorized": False,
        "unit_developed_authorized": False,
        "course_promotion_authorized": False,
        "public_release_authorized": False,
        "checks": checks,
        "failed_checks": sorted(name for name, passed in checks.items() if not passed),
        "reviewed_commit": review.get("reviewed_commit"),
        "packet_digest_sha256": review.get("packet_digest_sha256"),
        "interpretation": "Authorization is limited to implementing U2-P1, U2-P2 and U2-P3 under the reviewed contract. It does not authorize full theory, publication, clinical claims, development status or course promotion.",
    }


def pending_report(handoff: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "handoff_id": handoff.get("handoff_id"),
        "status": "pending_human_review",
        "practice_implementation_authorized": False,
        "controlled_full_theory_drafting_authorized": False,
        "unit_developed_authorized": False,
        "course_promotion_authorized": False,
        "public_release_authorized": False,
        "failed_checks": ["decision_record_missing", "packet_manifest_missing"],
        "interpretation": "No human review evidence is present. CI cannot authorize practice implementation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", type=Path, default=DEFAULT_HANDOFF)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--decision", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-authorization", action="store_true")
    args = parser.parse_args()

    try:
        handoff = load_json(args.handoff)
        if args.manifest is None and args.decision is None:
            report = pending_report(handoff)
        elif args.manifest is None or args.decision is None:
            raise AuthorizationError("manifest and decision must be supplied together")
        else:
            report = evaluate_decision(
                handoff, load_json(args.manifest), load_json(args.decision)
            )
    except AuthorizationError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.require_authorization and not report["practice_implementation_authorized"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
