#!/usr/bin/env python3
"""Core assessment logic for Bioinstrumentation unit 1."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


class AssessmentError(ValueError):
    """Raised when an assessment contract or submission is invalid."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssessmentError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AssessmentError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AssessmentError(f"{path} must contain an object")
    return payload


def machine_index(implementation: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = implementation.get("machine_scored_assessments")
    if not isinstance(entries, list):
        raise AssessmentError("machine assessments must be a list")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise AssessmentError("invalid machine assessment entry")
        result[entry["id"]] = entry
    return result


def human_ids(implementation: dict[str, Any]) -> set[str]:
    entries = implementation.get("human_scored_assessments")
    if not isinstance(entries, list):
        raise AssessmentError("human assessments must be a list")
    return {
        str(entry["id"])
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }


def feedback_bank(implementation: dict[str, Any]) -> dict[str, dict[str, str]]:
    relative = implementation.get("feedback_bank")
    if not isinstance(relative, str) or not relative:
        raise AssessmentError("feedback bank path is missing")
    payload = load_json(ROOT / relative)
    bank = payload.get("feedback")
    if not isinstance(bank, dict):
        raise AssessmentError("feedback bank is invalid")
    return bank


def release_feedback(
    implementation: dict[str, Any], misconception_ids: list[str], attempt: int
) -> list[dict[str, str]]:
    contract = implementation.get("feedback_contract")
    if not isinstance(contract, dict):
        raise AssessmentError("feedback contract is missing")
    release = contract.get("release_by_attempt")
    if not isinstance(release, dict):
        raise AssessmentError("feedback release policy is missing")
    stage = "1" if attempt == 1 else "2" if attempt == 2 else "3_plus"
    fields = release.get(stage)
    if not isinstance(fields, list) or not fields:
        raise AssessmentError(f"invalid feedback stage: {stage}")
    bank = feedback_bank(implementation)
    result: list[dict[str, str]] = []
    for misconception_id in sorted(set(misconception_ids)):
        source = bank.get(misconception_id)
        if not isinstance(source, dict):
            raise AssessmentError(f"unknown misconception: {misconception_id}")
        item = {"id": misconception_id}
        for field in fields:
            value = source.get(field)
            if not isinstance(value, str) or not value.strip():
                raise AssessmentError(f"missing feedback field: {misconception_id}.{field}")
            item[field] = value
        result.append(item)
    return result


def validate_submission(submission: dict[str, Any]) -> tuple[str, int, dict[str, Any]]:
    assessment_id = submission.get("assessment_id")
    attempt = submission.get("attempt")
    responses = submission.get("responses")
    if not isinstance(assessment_id, str) or not assessment_id:
        raise AssessmentError("assessment_id is required")
    if not isinstance(attempt, int) or attempt < 1:
        raise AssessmentError("attempt must be an integer greater than zero")
    if not isinstance(responses, dict):
        raise AssessmentError("responses must be an object")
    return assessment_id, attempt, responses


def evaluate_concept_sort(
    assessment: dict[str, Any], responses: dict[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    items = assessment.get("items")
    categories = assessment.get("allowed_categories")
    rule = assessment.get("mastery_rule")
    if not isinstance(items, list) or not isinstance(categories, list) or not isinstance(rule, dict):
        raise AssessmentError("invalid concept-sort contract")
    expected_ids = {str(item.get("id")) for item in items if isinstance(item, dict)}
    if set(responses) != expected_ids:
        raise AssessmentError("concept-sort response ids do not match the contract")
    allowed = {str(value) for value in categories}
    correct = 0
    incorrect: list[str] = []
    critical: list[str] = []
    misconceptions: list[str] = []
    for item in items:
        item_id = str(item["id"])
        response = responses[item_id]
        if response not in allowed:
            raise AssessmentError(f"invalid category for {item_id}")
        if response == item.get("correct_category"):
            correct += 1
            continue
        incorrect.append(item_id)
        if item.get("critical") is True:
            critical.append(item_id)
        mapped = item.get("misconceptions_on_error")
        if not isinstance(mapped, list) or not mapped:
            raise AssessmentError(f"missing routing for {item_id}")
        misconceptions.extend(str(value) for value in mapped)
    minimum = int(rule.get("minimum_correct", 0))
    require_critical = rule.get("critical_items_must_be_correct") is True
    summary = {
        "assessment_id": assessment["id"],
        "score": {"correct": correct, "total": len(items)},
        "mastered": correct >= minimum and (not require_critical or not critical),
        "incorrect_item_ids": incorrect,
        "critical_error_item_ids": critical,
    }
    return summary, misconceptions


def evaluate_traceability(
    assessment: dict[str, Any], responses: dict[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    claims = assessment.get("claims")
    decisions = assessment.get("allowed_decisions")
    findings = assessment.get("allowed_findings")
    rule = assessment.get("mastery_rule")
    if not isinstance(claims, list) or not isinstance(decisions, list) or not isinstance(findings, list) or not isinstance(rule, dict):
        raise AssessmentError("invalid traceability contract")
    expected_ids = {str(claim.get("id")) for claim in claims if isinstance(claim, dict)}
    if set(responses) != expected_ids:
        raise AssessmentError("traceability response ids do not match the contract")
    allowed_decisions = {str(value) for value in decisions}
    allowed_findings = {str(value) for value in findings}
    fully_correct = 0
    incorrect: list[str] = []
    misconceptions: list[str] = []
    for claim in claims:
        claim_id = str(claim["id"])
        response = responses[claim_id]
        if not isinstance(response, dict):
            raise AssessmentError(f"{claim_id} response must be an object")
        decision = response.get("decision")
        selected = response.get("findings")
        if decision not in allowed_decisions:
            raise AssessmentError(f"invalid decision for {claim_id}")
        if not isinstance(selected, list) or any(value not in allowed_findings for value in selected):
            raise AssessmentError(f"invalid findings for {claim_id}")
        required = {str(value) for value in claim.get("required_findings", [])}
        if decision == claim.get("expected_decision") and required.issubset(set(selected)):
            fully_correct += 1
            continue
        incorrect.append(claim_id)
        mapped = claim.get("misconceptions")
        if not isinstance(mapped, list) or not mapped:
            raise AssessmentError(f"missing routing for {claim_id}")
        misconceptions.extend(str(value) for value in mapped)
    minimum = int(rule.get("minimum_claims_fully_correct", 0))
    summary = {
        "assessment_id": assessment["id"],
        "score": {"fully_correct": fully_correct, "total": len(claims)},
        "mastered": fully_correct >= minimum,
        "incorrect_claim_ids": incorrect,
    }
    return summary, misconceptions


def evaluate_submission(
    submission: dict[str, Any], implementation: dict[str, Any]
) -> dict[str, Any]:
    assessment_id, attempt, responses = validate_submission(submission)
    if assessment_id in human_ids(implementation):
        raise AssessmentError(f"{assessment_id} requires human rubric scoring")
    assessment = machine_index(implementation).get(assessment_id)
    if assessment is None:
        raise AssessmentError(f"unknown assessment: {assessment_id}")
    kind = assessment.get("type")
    if kind == "diagnostic_concept_sort":
        summary, misconceptions = evaluate_concept_sort(assessment, responses)
    elif kind == "traceability_claim_review":
        summary, misconceptions = evaluate_traceability(assessment, responses)
    else:
        raise AssessmentError(f"unsupported assessment type: {kind}")
    summary["attempt"] = attempt
    summary["diagnosed_misconceptions"] = sorted(set(misconceptions))
    summary["feedback"] = release_feedback(
        implementation, summary["diagnosed_misconceptions"], attempt
    )
    summary["feedback_policy"] = "diagnostic_and_recovery_without_answer_key"
    return summary
