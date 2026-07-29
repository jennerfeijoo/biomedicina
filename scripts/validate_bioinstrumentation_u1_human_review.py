#!/usr/bin/env python3
"""Validate human-review protocols for Bioinstrumentation unit 1."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from calculate_bioinstrumentation_u1_agreement import (
    AgreementError,
    analyze_agreement,
    load_json,
    load_thresholds,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = (
    ROOT
    / "data"
    / "review_protocols"
    / "bioinstrumentacion-unit-01-human-review.json"
)
SOURCE_PATH = (
    ROOT
    / "data"
    / "source_registry"
    / "bioinstrumentacion-unit-01-review-methods.json"
)
HIGH_FIXTURE = (
    ROOT
    / "data"
    / "review_fixtures"
    / "bioinstrumentacion"
    / "unit-01"
    / "high-agreement-synthetic.json"
)
LOW_FIXTURE = (
    ROOT
    / "data"
    / "review_fixtures"
    / "bioinstrumentacion"
    / "unit-01"
    / "low-agreement-synthetic.json"
)
COGNITIVE_TEMPLATE = (
    ROOT
    / "data"
    / "review_templates"
    / "bioinstrumentacion"
    / "unit-01"
    / "cognitive-session-template.json"
)
RATER_TEMPLATE = (
    ROOT
    / "data"
    / "review_templates"
    / "bioinstrumentacion"
    / "unit-01"
    / "inter-rater-round-template.json"
)
COGNITIVE_DOC = (
    ROOT
    / "docs"
    / "pilots"
    / "bioinstrumentacion"
    / "unit-01"
    / "COGNITIVE_TEST_PROTOCOL.md"
)
AGREEMENT_DOC = (
    ROOT
    / "docs"
    / "pilots"
    / "bioinstrumentacion"
    / "unit-01"
    / "INTER_RATER_AGREEMENT_PROTOCOL.md"
)
READINESS_PATH = (
    ROOT
    / "docs"
    / "pilots"
    / "bioinstrumentacion"
    / "unit-01"
    / "AUTHORING_READINESS.md"
)
PACKAGE_PATH = (
    ROOT
    / "data"
    / "course_plan_packages"
    / "package-04-bioinstrumentation-excellence-pilot.json"
)
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
AUTHORAL_UNIT_PATH = (
    ROOT
    / "data"
    / "course_redevelopment"
    / "bioinstrumentacion"
    / "units"
    / "unit-01.json"
)

EXPECTED_SOURCE_IDS = {
    "cdc-ccqder-cognitive-interviewing-2024",
    "us-census-questionnaire-testing-appendix-a2",
    "cohen-kappa-1960",
    "cohen-weighted-kappa-1968",
}


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} is insufficient")
    return text


def require_list(value: Any, label: str, minimum: int) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"{label} requires at least {minimum} entries")
    return value


def validate_sources() -> None:
    registry = load_json(SOURCE_PATH)
    if registry.get("status") != "verified_direct_sources":
        raise ValueError("review-method source registry is not verified")
    sources = require_list(registry.get("sources"), "sources", 4)
    ids = {entry.get("id") for entry in sources if isinstance(entry, dict)}
    if ids != EXPECTED_SOURCE_IDS:
        raise ValueError(f"unexpected review-method sources: {sorted(ids)}")
    for entry in sources:
        if not isinstance(entry, dict):
            raise ValueError("source entries must be objects")
        source_id = require_text(entry.get("id"), "source.id", 8)
        if entry.get("verification_status") != "verified_directly":
            raise ValueError(f"{source_id} was not verified directly")
        if not str(entry.get("url") or "").startswith("https://"):
            raise ValueError(f"{source_id} lacks a secure URL")
        require_text(entry.get("locator"), f"{source_id}.locator", 20)
        require_list(entry.get("authorized_claims"), f"{source_id}.claims", 2)
        require_text(entry.get("limitations"), f"{source_id}.limitations", 60)


def validate_protocol() -> dict[str, float | int]:
    protocol = load_json(PROTOCOL_PATH)
    if protocol.get("protocol_id") != "bioinstrumentacion-unit-01-human-review":
        raise ValueError("unexpected protocol id")
    if protocol.get("status") != "protocol_ready_pending_human_execution":
        raise ValueError("human review protocol status is incorrect")
    if protocol.get("course_editorial_state") != "pending":
        raise ValueError("protocol must preserve pending course state")
    if protocol.get("full_theory_drafting_authorized") is not False:
        raise ValueError("protocol authorized theory prematurely")
    if protocol.get("source_registry") != str(SOURCE_PATH.relative_to(ROOT)):
        raise ValueError("protocol source registry path is incorrect")

    cognitive = protocol.get("cognitive_test")
    if not isinstance(cognitive, dict):
        raise ValueError("cognitive test protocol is missing")
    if cognitive.get("status") != "pending_human_execution":
        raise ValueError("cognitive test must remain pending")
    if cognitive.get("sampling_intent") != "purposive_problem_detection_not_population_estimation":
        raise ValueError("cognitive test sampling intent is unsafe or ambiguous")
    if cognitive.get("minimum_completed_sessions_for_pilot_gate") != 1:
        raise ValueError("pilot cognitive session minimum changed")
    require_list(cognitive.get("participant_profile"), "participant_profile", 3)
    require_list(cognitive.get("session_sequence"), "session_sequence", 6)
    probes = cognitive.get("required_probes")
    if not isinstance(probes, dict) or set(probes) != {
        "comprehension",
        "retrieval",
        "judgment",
        "response",
    }:
        raise ValueError("cognitive probe domains are incomplete")
    for domain, questions in probes.items():
        require_list(questions, f"probes.{domain}", 1)
    require_list(cognitive.get("pilot_acceptance_criteria"), "acceptance", 5)
    require_list(cognitive.get("revision_triggers"), "revision_triggers", 5)
    governance = cognitive.get("data_governance")
    if not isinstance(governance, dict):
        raise ValueError("cognitive data governance is missing")
    for field in (
        "real_participant_data_committed_to_repository",
        "sensitive_or_clinical_data_requested",
    ):
        if governance.get(field) is not False:
            raise ValueError(f"{field} must remain false")
    for field in (
        "direct_identifiers_prohibited",
        "audio_or_video_requires_separate_consent",
        "repository_retains_only_empty_templates_and_synthetic_fixtures",
    ):
        if governance.get(field) is not True:
            raise ValueError(f"{field} must remain true")

    review = protocol.get("inter_rater_review")
    if not isinstance(review, dict):
        raise ValueError("inter-rater protocol is missing")
    if review.get("status") != "pending_human_execution":
        raise ValueError("inter-rater review must remain pending")
    if review.get("reviewer_count") != 2:
        raise ValueError("inter-rater review requires exactly two reviewers")
    if review.get("rating_scale") != [0, 1, 2]:
        raise ValueError("ordinal rating scale changed")
    require_list(review.get("required_reviewer_competence"), "reviewer competence", 3)
    require_list(review.get("workflow"), "inter-rater workflow", 5)
    require_text(review.get("interpretation_limit"), "interpretation_limit", 100)

    state = protocol.get("execution_state")
    if not isinstance(state, dict):
        raise ValueError("execution state is missing")
    for field in (
        "cognitive_test_completed",
        "inter_rater_review_completed",
        "disciplinary_review_completed",
        "human_evidence_present",
        "unit_developed",
    ):
        if state.get(field) is not False:
            raise ValueError(f"{field} must remain false")
    if state.get("synthetic_ci_validation_only") is not True:
        raise ValueError("CI must be labelled synthetic-only")
    if state.get("course_state_after_block") != "pending":
        raise ValueError("protocol changed course state")
    return load_thresholds(PROTOCOL_PATH)


def validate_templates() -> None:
    cognitive = load_json(COGNITIVE_TEMPLATE)
    if cognitive.get("execution_status") != "not_started":
        raise ValueError("cognitive template was marked as executed")
    if cognitive.get("contains_real_participant_data") is not False:
        raise ValueError("cognitive template claims real participant data")
    if cognitive.get("session_id_pseudonymous") != "":
        raise ValueError("cognitive template contains a session identifier")
    if cognitive.get("consent_documented") is not False:
        raise ValueError("empty template claims consent")
    tasks = require_list(cognitive.get("tasks"), "cognitive template tasks", 3)
    task_ids = {entry.get("task_id") for entry in tasks if isinstance(entry, dict)}
    if task_ids != {"U1-A1", "U1-A4", "U1-A2-instruction-comprehension"}:
        raise ValueError("cognitive template tasks changed")

    rater = load_json(RATER_TEMPLATE)
    if rater.get("execution_status") != "not_started":
        raise ValueError("inter-rater template was marked as executed")
    if rater.get("contains_real_reviewer_data") is not False:
        raise ValueError("inter-rater template claims real reviewer data")
    if rater.get("independent_scoring_completed") is not False:
        raise ValueError("empty template claims completed scoring")
    if rater.get("ratings") != []:
        raise ValueError("inter-rater template must not contain ratings")
    if rater.get("scale") != [0, 1, 2]:
        raise ValueError("inter-rater template scale changed")


def validate_synthetic_controls(thresholds: dict[str, float | int]) -> None:
    high_payload = load_json(HIGH_FIXTURE)
    low_payload = load_json(LOW_FIXTURE)
    for payload in (high_payload, low_payload):
        if payload.get("synthetic") is not True:
            raise ValueError("review fixture is not labelled synthetic")
        if payload.get("contains_human_data") is not False:
            raise ValueError("review fixture claims human data")
        if len(payload.get("ratings", [])) != 20:
            raise ValueError("synthetic agreement fixtures require 20 ratings")

    high = analyze_agreement(high_payload, thresholds)
    if high.get("gate_passed") is not True:
        raise ValueError(f"high-agreement control did not pass: {high}")
    if high.get("ordinal_exact_agreement") != 0.85:
        raise ValueError("high-control exact agreement changed")
    if high.get("ordinal_mean_absolute_difference") != 0.15:
        raise ValueError("high-control mean absolute difference changed")
    if high.get("ordinal_linear_weighted_kappa") != 0.814815:
        raise ValueError("high-control weighted kappa changed")
    if high.get("critical_flag_exact_agreement") != 1.0:
        raise ValueError("high-control critical agreement changed")
    if high.get("unresolved_critical_disagreements") != []:
        raise ValueError("high-control contains critical disagreements")

    low = analyze_agreement(low_payload, thresholds)
    if low.get("gate_passed") is not False:
        raise ValueError("low-agreement control passed unexpectedly")
    if low.get("ordinal_exact_agreement") != 0.1:
        raise ValueError("low-control exact agreement changed")
    if low.get("ordinal_linear_weighted_kappa") != -0.284916:
        raise ValueError("low-control weighted kappa changed")
    if len(low.get("unresolved_critical_disagreements", [])) != 6:
        raise ValueError("low-control critical disagreement count changed")


def validate_documents() -> None:
    documents = {
        COGNITIVE_DOC: [
            "prueba cognitiva",
            "detección de problemas",
            "pending_human_execution",
            "No deben versionarse",
            "CI solo puede comprobar",
        ],
        AGREEMENT_DOC: [
            "acuerdo entre revisores",
            "Kappa ponderado lineal",
            "matriz de confusión",
            "control negativo",
            "pendiente de ejecución humana",
        ],
    }
    for path, markers in documents.items():
        text = path.read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            raise ValueError(f"{path.relative_to(ROOT)} lacks: {', '.join(missing)}")


def validate_repository_state() -> None:
    package = load_json(PACKAGE_PATH)
    if package.get("current_phase") != "unit_01_authoring_preparation_review":
        raise ValueError("historical preparation phase changed")
    if package.get("active_workstream") != "unit_01_practice_implementation_review":
        raise ValueError("practice workstream changed")
    if package.get("assessment_workstream") != "unit_01_assessment_implementation_review":
        raise ValueError("assessment workstream changed")
    if package.get("human_review_workstream") != "unit_01_human_review_protocol_ready":
        raise ValueError("human review workstream is not synchronized")
    review = package.get("human_review_protocol")
    if not isinstance(review, dict):
        raise ValueError("package lacks human_review_protocol")
    expected_paths = {
        "contract": str(PROTOCOL_PATH.relative_to(ROOT)),
        "source_registry": str(SOURCE_PATH.relative_to(ROOT)),
        "cognitive_template": str(COGNITIVE_TEMPLATE.relative_to(ROOT)),
        "inter_rater_template": str(RATER_TEMPLATE.relative_to(ROOT)),
        "calculator": "scripts/calculate_bioinstrumentation_u1_agreement.py",
        "validation": "scripts/validate_bioinstrumentation_u1_human_review.py",
    }
    for field, expected in expected_paths.items():
        if review.get(field) != expected:
            raise ValueError(f"package human review {field} is incorrect")
    if review.get("status") != "protocol_ready_pending_human_execution":
        raise ValueError("package human review status is incorrect")
    if review.get("human_evidence_present") is not False:
        raise ValueError("package simulates human evidence")
    if review.get("synthetic_ci_validation_only") is not True:
        raise ValueError("package must label CI synthetic-only")
    if review.get("full_theory_drafting_authorized") is not False:
        raise ValueError("package authorized theory prematurely")

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if AUTHORAL_UNIT_PATH.exists():
        raise ValueError("authoral unit exists before human review")

    readiness = READINESS_PATH.read_text(encoding="utf-8")
    for marker in (
        "human_review_protocol_ready",
        "Protocolo de prueba cognitiva formalizado.",
        "Protocolo de acuerdo entre revisores formalizado.",
        "Ejecución de prueba cognitiva con participante humano.",
        "Ejecución de ronda independiente con dos revisores.",
        "La evidencia humana continúa pendiente",
    ):
        if marker not in readiness:
            raise ValueError(f"AUTHORING_READINESS lacks marker: {marker}")


def main() -> int:
    try:
        validate_sources()
        thresholds = validate_protocol()
        validate_templates()
        validate_synthetic_controls(thresholds)
        validate_documents()
        validate_repository_state()
    except (OSError, ValueError, TypeError, json.JSONDecodeError, AgreementError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK human review protocols: Bioinstrumentación U1")
    print(
        "cognitive protocol ready · inter-rater calculator validated · synthetic controls pass/fail as expected · human execution pending · course pending"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
