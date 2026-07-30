#!/usr/bin/env python3
"""Validate Bioinstrumentation U2 human-review protocols without fabricating human evidence."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from calculate_bioinstrumentation_u2_agreement import analyze, load_json, thresholds

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/review_protocols/bioinstrumentacion-unit-02-human-review.json"
COGNITIVE_TEMPLATE = ROOT / "data/review_templates/bioinstrumentacion/unit-02/cognitive-session-template.json"
RATER_TEMPLATE = ROOT / "data/review_templates/bioinstrumentacion/unit-02/inter-rater-round-template.json"
HIGH = ROOT / "data/review_fixtures/bioinstrumentacion/unit-02/high-agreement-synthetic.json"
LOW = ROOT / "data/review_fixtures/bioinstrumentacion/unit-02/low-agreement-synthetic.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-02.json"
AUDIT = ROOT / "data/course_audits/bioinstrumentacion/UNIT_02_AUTHORAL_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-30.json"
STATUS = ROOT / "data/catalog_statuses.json"
DOC = ROOT / "docs/pilots/bioinstrumentacion/unit-02/HUMAN_REVIEW_PROTOCOLS.md"
DECISION = ROOT / "data/review_evidence/bioinstrumentacion-unit-02-disciplinary-review.json"
MANIFEST = ROOT / "data/review_evidence/bioinstrumentacion-unit-02-review-packet.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_list(value: Any, minimum: int, label: str) -> list[Any]:
    require(isinstance(value, list) and len(value) >= minimum, f"{label} is incomplete")
    return value


def validate_protocol() -> None:
    protocol = load_json(PROTOCOL)
    expected = {
        "schema_version": "1.0",
        "protocol_id": "bioinstrumentacion-unit-02-human-review",
        "subject_id": "bioinstrumentacion",
        "unit": 2,
        "status": "protocol_ready_pending_human_execution",
        "course_editorial_state": "pending",
        "authoral_unit_status": "authored_internal_review",
        "external_professional_review": "pending_human_review",
        "operational_issue": 161,
    }
    for key, value in expected.items():
        require(protocol.get(key) == value, f"unexpected protocol field: {key}")
    require(protocol.get("source_unit") == str(UNIT.relative_to(ROOT)), "unit path changed")
    require(protocol.get("authoral_audit") == str(AUDIT.relative_to(ROOT)), "audit path changed")

    cognitive = protocol.get("cognitive_test")
    require(isinstance(cognitive, dict), "cognitive protocol missing")
    require(cognitive.get("status") == "pending_human_execution", "cognitive test is not pending")
    require(cognitive.get("minimum_completed_sessions_for_pilot_gate") == 3, "session minimum changed")
    require(cognitive.get("sampling_intent") == "purposive_problem_detection_not_population_estimation", "sampling intent changed")
    require_list(cognitive.get("participant_profile"), 3, "participant profile")
    require_list(cognitive.get("session_sequence"), 7, "session sequence")
    probes = cognitive.get("required_probes")
    require(isinstance(probes, dict) and set(probes) == {"comprehension", "retrieval", "judgment", "response"}, "probe domains incomplete")
    require(all(isinstance(items, list) and items for items in probes.values()), "probe questions missing")
    require_list(cognitive.get("pilot_acceptance_criteria"), 7, "cognitive acceptance criteria")
    require_list(cognitive.get("revision_triggers"), 6, "cognitive revision triggers")
    governance = cognitive.get("data_governance")
    require(isinstance(governance, dict), "data governance missing")
    for key in ("real_participant_data_committed_to_repository", "sensitive_or_clinical_data_requested"):
        require(governance.get(key) is False, f"{key} must remain false")
    for key in ("direct_identifiers_prohibited", "audio_or_video_requires_separate_consent", "repository_retains_only_empty_templates_and_synthetic_fixtures", "human_execution_records_stored_outside_public_repository"):
        require(governance.get(key) is True, f"{key} must remain true")

    usability = protocol.get("feedback_usability_review")
    require(isinstance(usability, dict) and usability.get("status") == "pending_human_execution", "feedback usability review is not pending")
    require(usability.get("reviewer_count_minimum") == 2, "feedback review requires two people")
    require_list(usability.get("review_targets"), 6, "feedback review targets")

    review = protocol.get("inter_rater_review")
    require(isinstance(review, dict) and review.get("status") == "pending_human_execution", "inter-rater review is not pending")
    require(review.get("reviewer_count") == 2, "inter-rater reviewer count changed")
    require(review.get("rating_scale") == [0, 1, 2], "rating scale changed")
    require(set(review.get("artifacts", [])) == {"U2-A1", "U2-A5"}, "human-scored assessment set changed")
    require_list(review.get("workflow"), 6, "inter-rater workflow")
    require(len(str(review.get("interpretation_limit", ""))) >= 100, "interpretation limit is insufficient")

    state = protocol.get("execution_state")
    require(isinstance(state, dict), "execution state missing")
    for key in ("cognitive_test_completed", "feedback_usability_review_completed", "inter_rater_review_completed", "disciplinary_review_completed", "human_evidence_present", "unit_developed", "public_release_authorized"):
        require(state.get(key) is False, f"{key} fabricates completion or authorization")
    require(state.get("synthetic_ci_validation_only") is True, "CI is not labelled synthetic-only")
    require(state.get("course_state_after_block") == "pending", "course state changed")


def validate_templates_and_controls() -> None:
    cognitive = load_json(COGNITIVE_TEMPLATE)
    require(cognitive.get("execution_status") == "not_started", "cognitive template claims execution")
    require(cognitive.get("contains_real_participant_data") is False, "cognitive template contains real data")
    require(cognitive.get("consent_documented") is False, "empty cognitive template claims consent")
    require(cognitive.get("session_id_pseudonymous") == "", "cognitive template contains an identifier")
    tasks = {item.get("task_id") for item in cognitive.get("tasks", []) if isinstance(item, dict)}
    require(tasks == {"U2-A1", "U2-A2", "U2-A3", "U2-A5"}, "cognitive task set changed")

    rater = load_json(RATER_TEMPLATE)
    require(rater.get("execution_status") == "not_started", "rater template claims execution")
    require(rater.get("contains_real_reviewer_data") is False, "rater template contains real data")
    require(rater.get("independent_scoring_completed") is False, "empty rater template claims scoring")
    require(rater.get("ratings") == [], "rater template must be empty")
    require(rater.get("scale") == [0, 1, 2], "rater scale changed")

    limits = thresholds(PROTOCOL)
    high = analyze(load_json(HIGH), limits)
    low = analyze(load_json(LOW), limits)
    require(high.get("synthetic") is True and high.get("gate_passed") is True, "high-agreement control must pass")
    require(low.get("synthetic") is True and low.get("gate_passed") is False, "low-agreement control must fail")


def validate_repository_state() -> None:
    require(UNIT.is_file(), "authoral Unit 2 is missing")
    audit = load_json(AUDIT)
    require(audit.get("status") == "passed_internal_review", "authoral audit no longer passes")
    require(audit.get("unresolved_critical_findings") == 0, "authoral audit has critical findings")
    require(audit.get("unresolved_major_findings") == 0, "authoral audit has major findings")
    statuses = load_json(STATUS)
    require("bioinstrumentacion" in set(statuses.get("pending", [])), "course must remain pending")
    require("bioinstrumentacion" not in set(statuses.get("developed", [])), "course was promoted")
    require(not DECISION.exists() and not MANIFEST.exists(), "protocol block fabricated external review evidence")
    text = DOC.read_text(encoding="utf-8")
    for marker in ("pending_human_execution", "purposive_problem_detection_not_population_estimation", "U2-A1", "U2-A5", "weighted kappa", "No constituye evidencia humana", "pending_human_review"):
        require(marker in text, f"protocol document lacks marker: {marker}")


def main() -> int:
    try:
        validate_protocol()
        validate_templates_and_controls()
        validate_repository_state()
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U2 human-review protocols")
    print("cognitive test · feedback usability · inter-rater agreement · synthetic controls")
    print("human execution pending · professional review pending · course pending")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
