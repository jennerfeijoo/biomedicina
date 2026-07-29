#!/usr/bin/env python3
"""Assessment engine for Bioinstrumentation unit 2."""
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


def _index(entries: Any, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(entries, list):
        raise AssessmentError(f"{label} must be a list")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise AssessmentError(f"invalid {label} entry")
        if entry["id"] in result:
            raise AssessmentError(f"duplicated assessment id: {entry['id']}")
        result[entry["id"]] = entry
    return result


def machine_index(implementation: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _index(implementation.get("machine_scored_assessments"), "machine assessments")


def human_index(implementation: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _index(implementation.get("human_scored_assessments"), "human assessments")


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
        item: dict[str, str] = {"id": misconception_id}
        for field in fields:
            value = source.get(field)
            if not isinstance(value, str) or not value.strip():
                raise AssessmentError(f"missing feedback field: {misconception_id}.{field}")
            item[field] = value
        result.append(item)
    return result


def _base_submission(submission: dict[str, Any]) -> tuple[str, int]:
    assessment_id = submission.get("assessment_id")
    attempt = submission.get("attempt")
    if not isinstance(assessment_id, str) or not assessment_id:
        raise AssessmentError("assessment_id is required")
    if not isinstance(attempt, int) or attempt < 1:
        raise AssessmentError("attempt must be an integer greater than zero")
    return assessment_id, attempt


def _validate_response_ids(responses: Any, expected_ids: set[str], label: str) -> dict[str, Any]:
    if not isinstance(responses, dict):
        raise AssessmentError("responses must be an object")
    if set(responses) != expected_ids:
        raise AssessmentError(f"{label} response ids do not match the contract")
    return responses


def _string_set(value: Any, allowed: set[str], label: str) -> set[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise AssessmentError(f"{label} must be a list of strings")
    selected = set(value)
    if len(selected) != len(value):
        raise AssessmentError(f"{label} contains duplicates")
    if not selected.issubset(allowed):
        raise AssessmentError(f"{label} contains unsupported values")
    return selected


def evaluate_static(
    assessment: dict[str, Any], responses: Any
) -> tuple[dict[str, Any], list[str]]:
    cases = assessment.get("cases")
    if not isinstance(cases, list):
        raise AssessmentError("invalid static assessment contract")
    selected = _validate_response_ids(
        responses, {str(case.get("id")) for case in cases}, "static audit"
    )
    patterns = set(map(str, assessment.get("allowed_patterns", [])))
    evidence_allowed = set(map(str, assessment.get("allowed_evidence", [])))
    tests = set(map(str, assessment.get("allowed_refutation_tests", [])))
    fully_correct = 0
    incorrect: list[str] = []
    misconceptions: list[str] = []
    for case in cases:
        case_id = str(case["id"])
        response = selected[case_id]
        if not isinstance(response, dict):
            raise AssessmentError(f"{case_id} response must be an object")
        pattern = response.get("pattern")
        evidence = _string_set(response.get("evidence"), evidence_allowed, f"{case_id}.evidence")
        refutation = response.get("refutation_test")
        if pattern not in patterns or refutation not in tests:
            raise AssessmentError(f"invalid static response for {case_id}")
        correct = (
            pattern == case.get("expected_pattern")
            and set(map(str, case.get("required_evidence", []))).issubset(evidence)
            and refutation == case.get("expected_refutation_test")
        )
        if correct:
            fully_correct += 1
        else:
            incorrect.append(case_id)
            misconceptions.extend(map(str, case.get("misconceptions", [])))
    minimum = int(assessment.get("mastery_rule", {}).get("minimum_cases_fully_correct", 0))
    return {
        "assessment_id": assessment["id"],
        "score": {"fully_correct": fully_correct, "total": len(cases)},
        "mastered": fully_correct >= minimum,
        "incorrect_case_ids": incorrect,
    }, misconceptions


def evaluate_dynamic(
    assessment: dict[str, Any], responses: Any
) -> tuple[dict[str, Any], list[str]]:
    cases = assessment.get("cases")
    if not isinstance(cases, list):
        raise AssessmentError("invalid dynamic assessment contract")
    selected = _validate_response_ids(
        responses, {str(case.get("id")) for case in cases}, "dynamic model"
    )
    decisions = set(map(str, assessment.get("allowed_decisions", [])))
    reasons_allowed = set(map(str, assessment.get("allowed_reasons", [])))
    response_interpretations = set(
        map(str, assessment.get("allowed_response_time_interpretations", []))
    )
    bandwidth_interpretations = set(
        map(str, assessment.get("allowed_bandwidth_interpretations", []))
    )
    fully_correct = 0
    incorrect: list[str] = []
    misconceptions: list[str] = []
    tau_errors: dict[str, float] = {}
    for case in cases:
        case_id = str(case["id"])
        response = selected[case_id]
        if not isinstance(response, dict):
            raise AssessmentError(f"{case_id} response must be an object")
        decision = response.get("decision")
        reasons = _string_set(response.get("reasons"), reasons_allowed, f"{case_id}.reasons")
        response_interpretation = response.get("response_time_interpretation")
        bandwidth_interpretation = response.get("bandwidth_interpretation")
        if decision not in decisions:
            raise AssessmentError(f"invalid decision for {case_id}")
        if response_interpretation not in response_interpretations:
            raise AssessmentError(f"invalid response-time interpretation for {case_id}")
        if bandwidth_interpretation not in bandwidth_interpretations:
            raise AssessmentError(f"invalid bandwidth interpretation for {case_id}")
        target = case.get("tau_target_s")
        tau_value = response.get("tau_estimate_s")
        tau_ok = False
        if target is None:
            if tau_value is not None:
                raise AssessmentError(f"{case_id}.tau_estimate_s must be null when the model is rejected")
            tau_ok = True
        else:
            if not isinstance(tau_value, (int, float)) or isinstance(tau_value, bool):
                raise AssessmentError(f"{case_id}.tau_estimate_s must be numeric")
            error = abs(float(tau_value) - float(target))
            tau_errors[case_id] = error
            tau_ok = error <= float(case.get("tau_tolerance_s", 0.0))
        correct = (
            decision == case.get("expected_decision")
            and set(map(str, case.get("required_reasons", []))).issubset(reasons)
            and response_interpretation == case.get("expected_response_time_interpretation")
            and bandwidth_interpretation == case.get("expected_bandwidth_interpretation")
            and tau_ok
        )
        if correct:
            fully_correct += 1
        else:
            incorrect.append(case_id)
            misconceptions.extend(map(str, case.get("misconceptions", [])))
    minimum = int(assessment.get("mastery_rule", {}).get("minimum_cases_fully_correct", 0))
    return {
        "assessment_id": assessment["id"],
        "score": {"fully_correct": fully_correct, "total": len(cases)},
        "mastered": fully_correct >= minimum,
        "incorrect_case_ids": incorrect,
        "tau_absolute_error_s": tau_errors,
    }, misconceptions


def evaluate_loading(
    assessment: dict[str, Any], responses: Any
) -> tuple[dict[str, Any], list[str]]:
    claims = assessment.get("claims")
    if not isinstance(claims, list):
        raise AssessmentError("invalid loading assessment contract")
    selected = _validate_response_ids(
        responses, {str(claim.get("id")) for claim in claims}, "loading review"
    )
    allowed = {
        "decision": set(map(str, assessment.get("allowed_decisions", []))),
        "route": set(map(str, assessment.get("allowed_routes", []))),
        "perturbed_quantity": set(map(str, assessment.get("allowed_perturbed_quantities", []))),
        "missing_evidence": set(map(str, assessment.get("allowed_missing_evidence", []))),
        "mitigation_status": set(map(str, assessment.get("allowed_mitigation_status", []))),
    }
    fully_correct = 0
    incorrect: list[str] = []
    misconceptions: list[str] = []
    expected_fields = {
        "decision": "expected_decision",
        "route": "expected_route",
        "perturbed_quantity": "expected_perturbed_quantity",
        "missing_evidence": "expected_missing_evidence",
        "mitigation_status": "expected_mitigation_status",
    }
    for claim in claims:
        claim_id = str(claim["id"])
        response = selected[claim_id]
        if not isinstance(response, dict):
            raise AssessmentError(f"{claim_id} response must be an object")
        for field, options in allowed.items():
            if response.get(field) not in options:
                raise AssessmentError(f"invalid {field} for {claim_id}")
        correct = all(
            response.get(field) == claim.get(expected)
            for field, expected in expected_fields.items()
        )
        if correct:
            fully_correct += 1
        else:
            incorrect.append(claim_id)
            misconceptions.extend(map(str, claim.get("misconceptions", [])))
    minimum = int(assessment.get("mastery_rule", {}).get("minimum_claims_fully_correct", 0))
    return {
        "assessment_id": assessment["id"],
        "score": {"fully_correct": fully_correct, "total": len(claims)},
        "mastered": fully_correct >= minimum,
        "incorrect_claim_ids": incorrect,
    }, misconceptions


def evaluate_human(
    assessment: dict[str, Any], submission: dict[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    if submission.get("human_reviewer_confirmed") is not True:
        raise AssessmentError("human_reviewer_confirmed must be true for rubric scoring")
    notes = submission.get("reviewer_notes")
    if not isinstance(notes, str) or len(notes.strip()) < 20:
        raise AssessmentError("reviewer_notes must contain a substantive human note")
    rubric = assessment.get("rubric")
    if not isinstance(rubric, list) or not rubric:
        raise AssessmentError("human assessment rubric is missing")
    scores = submission.get("rubric_scores")
    if not isinstance(scores, dict):
        raise AssessmentError("rubric_scores must be an object")
    criteria = {str(row.get("criterion")): row for row in rubric if isinstance(row, dict)}
    if set(scores) != set(criteria):
        raise AssessmentError("rubric score ids do not match the contract")
    total = 0
    maximum = 0
    critical_zeros: list[str] = []
    for criterion, row in criteria.items():
        score = scores[criterion]
        max_points = int(row.get("max_points", 0))
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= max_points:
            raise AssessmentError(f"invalid rubric score for {criterion}")
        total += score
        maximum += max_points
        if score == 0 and row.get("critical_if_zero") is True:
            critical_zeros.append(criterion)
    diagnosed = submission.get("diagnosed_misconceptions")
    allowed = set(map(str, assessment.get("allowed_misconceptions", [])))
    misconceptions = _string_set(diagnosed, allowed, "diagnosed_misconceptions")
    rule = assessment.get("mastery_rule")
    if not isinstance(rule, dict):
        raise AssessmentError("human mastery rule is missing")
    minimum = int(rule.get("minimum_points", 0))
    forbid_zeros = rule.get("critical_zeros_forbidden") is True
    mastered = total >= minimum and (not forbid_zeros or not critical_zeros)
    return {
        "assessment_id": assessment["id"],
        "score": {"points": total, "maximum": maximum},
        "mastered": mastered,
        "critical_zero_criteria": critical_zeros,
        "scoring_mode": "human_rubric",
        "automatic_semantic_grading": False,
    }, sorted(misconceptions)


def evaluate_submission(
    submission: dict[str, Any], implementation: dict[str, Any]
) -> dict[str, Any]:
    assessment_id, attempt = _base_submission(submission)
    machines = machine_index(implementation)
    humans = human_index(implementation)
    if assessment_id in machines:
        assessment = machines[assessment_id]
        kind = assessment.get("type")
        responses = submission.get("responses")
        if kind == "static_curve_audit":
            summary, misconceptions = evaluate_static(assessment, responses)
        elif kind == "first_order_dynamic_model":
            summary, misconceptions = evaluate_dynamic(assessment, responses)
        elif kind == "loading_mechanism_review":
            summary, misconceptions = evaluate_loading(assessment, responses)
        else:
            raise AssessmentError(f"unsupported assessment type: {kind}")
        summary["scoring_mode"] = "deterministic_structured"
    elif assessment_id in humans:
        summary, misconceptions = evaluate_human(humans[assessment_id], submission)
    else:
        raise AssessmentError(f"unknown assessment: {assessment_id}")
    summary["attempt"] = attempt
    summary["diagnosed_misconceptions"] = sorted(set(misconceptions))
    summary["feedback"] = release_feedback(
        implementation, summary["diagnosed_misconceptions"], attempt
    )
    summary["feedback_policy"] = "diagnostic_and_recovery_without_answer_key"
    return summary
