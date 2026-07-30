#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssessmentResult:
    accepted: bool
    feedback_route: str | None
    requires_human_review: bool = False


def evaluate(assessment_id: str, response: dict) -> AssessmentResult:
    if assessment_id == "U3-A1":
        required = {"membrane_potential", "distributed_source", "volume_conductor", "surface_difference"}
        present = set(response.get("chain", []))
        if required.issubset(present) and response.get("claims_direct_cell_measurement") is False:
            return AssessmentResult(True, None)
        return AssessmentResult(False, "U3-F01")

    if assessment_id == "U3-A2":
        elements = set(response.get("elements", []))
        if {"half_cell_potential", "Rs", "Rct", "Cdl"}.issubset(elements) and response.get("frequency_dependent") is True:
            return AssessmentResult(True, None)
        return AssessmentResult(False, "U3-F02")

    if assessment_id == "U3-A3":
        mapping = response.get("mapping", {})
        expected = {
            "measurement_reference": "reference",
            "bias_current_path": "return",
            "protective_conductor": "protective_earth",
            "field_screen": "shield",
        }
        if mapping == expected:
            return AssessmentResult(True, None)
        return AssessmentResult(False, "U3-F03")

    if assessment_id == "U3-A4":
        if response.get("pattern") and response.get("mechanism") and response.get("discriminating_test"):
            if response.get("claims_visual_certainty") is False:
                return AssessmentResult(True, None)
        return AssessmentResult(False, "U3-F04")

    if assessment_id == "U3-A5":
        required = {"source", "geometry", "scale", "band", "interface", "inference_limit"}
        if required.issubset(set(response.get("comparison_dimensions", []))):
            return AssessmentResult(False, None, requires_human_review=True)
        return AssessmentResult(False, "U3-F10", requires_human_review=True)

    raise ValueError(f"unknown assessment: {assessment_id}")


def feedback_for_attempt(route_id: str, attempt: int) -> dict:
    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    level = 1 if attempt == 1 else 2 if attempt == 2 else 3
    return {
        "route_id": route_id,
        "level": level,
        "reveals_complete_answer": False,
        "next_action": "revisar la relación causal y resolver un caso distinto",
    }
