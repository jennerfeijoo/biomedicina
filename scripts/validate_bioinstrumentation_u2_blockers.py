#!/usr/bin/env python3
"""Validate technical-blocker resolution for Bioinstrumentation U2."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOLUTION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-02-blocker-resolution.json"
SOURCE_PATH = ROOT / "data" / "source_registry" / "bioinstrumentacion-unit-02-blockers.json"
AUTH_PATH = ROOT / "data" / "authoring_authorizations" / "bioinstrumentacion-unit-02-practices-provisional.json"
PRACTICE_PATH = ROOT / "data" / "practice_implementations" / "bioinstrumentacion-unit-02.json"
CATALOG_PATH = ROOT / "data" / "catalog_statuses.json"
AUTHORAL_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"
DOC_DIR = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02"
EXPECTED_SOURCES = {
    "vim3-step-response-4-23-u2-blocker",
    "jcgm-gum-6-u2-blocker",
    "vishay-ntclg100e2103jb-datasheet",
    "micro-measurements-cea-06-125una-350",
    "ni-strain-gage-loading-u2",
    "hamamatsu-s5821-03-product",
}
EXPECTED_MODELS = {"linear-local", "saturation", "dead-zone", "hysteresis"}
EXPECTED_NEGATIVES = {"pure-delay", "underdamped-second-order", "static-only"}
EXPECTED_COMPONENTS = {
    "thermistor": "NTCLG100E2103JB",
    "strain-gage": "CEA-06-125UNA-350",
    "photodiode": "S5821-03",
}
EXPECTED_LOADING = {"thermal-loading", "mechanical-loading", "electrical-loading", "optical-loading"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def require_list(value: Any, minimum: int, label: str) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"{label} requires at least {minimum} items")
    return value


def validate_sources() -> None:
    registry = load_json(SOURCE_PATH)
    sources = require_list(registry.get("sources"), 6, "sources")
    ids = {source.get("id") for source in sources if isinstance(source, dict)}
    if ids != EXPECTED_SOURCES:
        raise ValueError("blocker source registry changed unexpectedly")
    for source in sources:
        if source.get("verification_status") != "verified_directly":
            raise ValueError(f"source {source.get('id')} is not verified directly")
        if not str(source.get("url", "")).startswith("https://"):
            raise ValueError(f"source {source.get('id')} lacks an HTTPS URL")


def validate_resolution(resolution: dict[str, Any]) -> None:
    expected_identity = {
        "subject_id": "bioinstrumentacion",
        "unit_number": 2,
        "status": "technical_blockers_resolved_review_pending",
        "course_editorial_state": "pending",
    }
    for key, wanted in expected_identity.items():
        if resolution.get(key) != wanted:
            raise ValueError(f"resolution {key} is incorrect")

    static = resolution.get("static_synthetic_model", {})
    if static.get("status") != "resolved_for_practice_implementation" or static.get("seed") != 20260729:
        raise ValueError("static blocker resolution is invalid")
    models = require_list(static.get("models"), 4, "static models")
    if {item.get("id") for item in models if isinstance(item, dict)} != EXPECTED_MODELS:
        raise ValueError("static model set changed")
    if len(require_list(static.get("acceptance_tests"), 7, "static acceptance tests")) < 7:
        raise ValueError("static acceptance tests are incomplete")

    dynamic = resolution.get("first_order_dynamic_model", {})
    if dynamic.get("status") != "resolved_for_practice_implementation":
        raise ValueError("dynamic blocker resolution is invalid")
    if dynamic.get("continuous_model") != "tau*dy/dt + y = K*x(t) + b":
        raise ValueError("dynamic model changed")
    params = dynamic.get("parameters", {})
    if params != {"K": 1.5, "b": 0.2, "tau_s": 2.0, "dt_s": 0.02, "duration_s": 16.0, "step_time_s": 2.0, "step_amplitude": 1.0}:
        raise ValueError("dynamic parameters changed")
    relations = {item.get("name"): item for item in require_list(dynamic.get("derived_relations"), 4, "dynamic relations") if isinstance(item, dict)}
    if not math.isclose(float(relations["fraction_at_tau"]["expected"]), 1 - math.exp(-1), rel_tol=1e-9):
        raise ValueError("fraction at tau is incorrect")
    negatives = require_list(dynamic.get("negative_controls"), 3, "negative controls")
    if {item.get("id") for item in negatives if isinstance(item, dict)} != EXPECTED_NEGATIVES:
        raise ValueError("dynamic negative controls changed")

    selection = resolution.get("component_selection", {})
    components = require_list(selection.get("components"), 3, "components")
    found = {item.get("id"): item.get("model") for item in components if isinstance(item, dict)}
    if found != EXPECTED_COMPONENTS:
        raise ValueError("pinned component set changed")
    if len(require_list(selection.get("comparison_fields"), 11, "comparison fields")) != 11:
        raise ValueError("component comparison fields changed")
    if len(require_list(selection.get("forbidden_transfer"), 5, "forbidden transfers")) != 5:
        raise ValueError("component transfer boundaries changed")

    loading = resolution.get("loading_cases", {})
    cases = require_list(loading.get("cases"), 4, "loading cases")
    if {item.get("id") for item in cases if isinstance(item, dict)} != EXPECTED_LOADING:
        raise ValueError("loading cases changed")

    review = resolution.get("disciplinary_review", {})
    if review.get("status") != "pending_human_review":
        raise ValueError("disciplinary review must remain pending")
    if set(review.get("decision_options", [])) != {"approve_for_practice_implementation", "approve_with_changes", "do_not_approve"}:
        raise ValueError("review decisions changed")
    editorial = resolution.get("editorial_decision", {})
    if editorial.get("technical_blockers_resolved") is not True:
        raise ValueError("technical blockers are not marked resolved")
    if editorial.get("human_review_completed") is not False:
        raise ValueError("resolution fabricates human review")
    if editorial.get("full_theory_drafting_authorized") is not False:
        raise ValueError("resolution authorizes theory")


def validate_repository_state() -> None:
    statuses = load_json(CATALOG_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if AUTHORAL_PATH.exists():
        raise ValueError("Unit 2 authoral file exists before authorization")
    if PRACTICE_PATH.exists():
        auth = load_json(AUTH_PATH)
        if auth.get("status") != "authorized_for_controlled_practice_implementation_provisionally":
            raise ValueError("practices exist without provisional authorization")
        practice = load_json(PRACTICE_PATH)
        if practice.get("status") != "implemented_internal_review":
            raise ValueError("present practices have an invalid status")
        if practice.get("full_theory_drafting_authorized") is not False:
            raise ValueError("practice implementation expanded into theory")
    for filename, markers in {
        "STATIC_SYNTHETIC_MODEL_RESOLUTION.md": ["resolved_for_practice_implementation", "Histéresis"],
        "DYNAMIC_FIRST_ORDER_RESOLUTION.md": ["resolved_for_practice_implementation", "f_c = 1/(2πτ)"],
        "LOADING_CASES_RESOLUTION.md": ["resolved_for_safe_cases", "no incluyen personas"],
        "COMPONENT_SELECTION_SPEC.md": ["resolved_and_pinned", "S5821-03"],
        "DISCIPLINARY_REVIEW_REQUEST.md": ["pending_human_review", "Este documento **no es una revisión**"],
    }.items():
        text = (DOC_DIR / filename).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                raise ValueError(f"{filename} lacks marker: {marker}")


def main() -> int:
    try:
        validate_sources()
        validate_resolution(load_json(RESOLUTION_PATH))
        validate_repository_state()
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U2 technical blocker resolution")
    print("4 static models · 3 dynamic negative controls · 3 pinned components · 4 loading cases · external review pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
