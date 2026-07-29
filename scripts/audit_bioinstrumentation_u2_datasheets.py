#!/usr/bin/env python3
"""Audit compact offline datasheet records for Bioinstrumentation U2 practice U2-P3."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

EXPECTED_MODELS = {
    "thermistor": "NTCLG100E2103JB",
    "strain-gage": "CEA-06-125UNA-350",
    "photodiode": "S5821-03",
}
ALLOWED_CATEGORIES = {
    "nominal",
    "datasheet_declared",
    "catalog_descriptor",
    "missing_required_lot_or_package_value",
    "nominal_geometry",
    "range",
    "typical",
    "maximum",
}
REQUIRED_FORBIDDEN_TRANSFERS = {
    "component_property_equals_system_performance",
    "typical_value_equals_guarantee",
    "laboratory_condition_equals_biomedical_condition",
    "component_cutoff_equals_chain_bandwidth",
    "commercial_specification_equals_clinical_validation",
}


class AuditError(ValueError):
    """Raised when the documentary fixture cannot be audited."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuditError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AuditError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AuditError("fixture must contain a JSON object")
    return payload


def _nonempty(value: Any, minimum: int = 1) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum


def audit_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if fixture.get("fixture_type") != "compact_documentary_metadata":
        errors.append("fixture_type must be compact_documentary_metadata")
    if fixture.get("human_data") is not False:
        errors.append("human_data must be false")
    if fixture.get("clinical_device_data") is not False:
        errors.append("clinical_device_data must be false")
    if fixture.get("network_required") is not False:
        errors.append("network_required must be false")

    components = fixture.get("components")
    if not isinstance(components, list) or len(components) != 3:
        errors.append("exactly three component records are required")
        components = []
    found_models: dict[str, str] = {}
    field_count = 0
    category_counts: dict[str, int] = {}
    missing_count = 0

    for component in components:
        if not isinstance(component, dict):
            errors.append("component records must be objects")
            continue
        component_id = component.get("component_id")
        model = component.get("model")
        if isinstance(component_id, str) and isinstance(model, str):
            found_models[component_id] = model
        else:
            errors.append("component_id and model must be non-empty strings")
            continue
        for key in (
            "manufacturer",
            "source_id",
            "document",
            "input_quantity",
            "output_quantity",
            "transduction_principle",
        ):
            if not _nonempty(component.get(key), 5):
                errors.append(f"{component_id}.{key} is missing or insufficient")
        boundaries = component.get("claim_boundaries")
        if not isinstance(boundaries, list) or len(boundaries) < 2 or not all(
            _nonempty(item, 20) for item in boundaries
        ):
            errors.append(f"{component_id}.claim_boundaries are incomplete")
        unresolved = component.get("missing_or_unresolved")
        if not isinstance(unresolved, list) or len(unresolved) < 2:
            errors.append(f"{component_id}.missing_or_unresolved is incomplete")

        fields = component.get("fields")
        if not isinstance(fields, list) or len(fields) < 5:
            errors.append(f"{component_id} requires at least five fields")
            continue
        for field in fields:
            field_count += 1
            if not isinstance(field, dict):
                errors.append(f"{component_id} contains a non-object field")
                continue
            name = field.get("name")
            category = field.get("category")
            if not _nonempty(name, 2):
                errors.append(f"{component_id} field name is missing")
            if category not in ALLOWED_CATEGORIES:
                errors.append(f"{component_id}.{name} has unsupported category {category!r}")
            else:
                category_counts[category] = category_counts.get(category, 0) + 1
            if not _nonempty(field.get("unit"), 1):
                errors.append(f"{component_id}.{name} lacks a unit or descriptor")
            if not _nonempty(field.get("conditions"), 20):
                errors.append(f"{component_id}.{name} lacks measurement conditions")
            evidence = field.get("evidence_status")
            if evidence not in {"pinned", "intentionally_unresolved"}:
                errors.append(f"{component_id}.{name} has invalid evidence_status")
            if category == "missing_required_lot_or_package_value":
                missing_count += 1
                if field.get("value") is not None or evidence != "intentionally_unresolved":
                    errors.append(f"{component_id}.{name} must remain explicitly unresolved")
            elif field.get("value") is None:
                errors.append(f"{component_id}.{name} has no value despite being pinned")
            if category == "typical" and field.get("guaranteed") is True:
                errors.append(f"{component_id}.{name} converts a typical value into a guarantee")

    if found_models != EXPECTED_MODELS:
        errors.append(f"unexpected component models: {found_models!r}")
    if category_counts.get("typical", 0) < 3:
        errors.append("the fixture must preserve at least three typical values")
    if category_counts.get("maximum", 0) < 1:
        errors.append("the fixture must preserve at least one maximum value")
    if category_counts.get("nominal", 0) < 3:
        errors.append("the fixture must preserve nominal values separately")
    if missing_count != 1:
        errors.append("the lot-specific gauge factor must be the single intentionally unresolved value")

    transfers = fixture.get("forbidden_transfers")
    if not isinstance(transfers, list) or set(transfers) != REQUIRED_FORBIDDEN_TRANSFERS:
        errors.append("forbidden_transfers are incomplete or altered")
    comparisons = fixture.get("comparison_fields")
    if not isinstance(comparisons, list) or len(comparisons) != 11:
        errors.append("comparison_fields must contain exactly eleven fields")

    if not errors:
        warnings.extend(
            [
                "The audit verifies documentary structure, not component authenticity or system performance.",
                "The unresolved gauge factor must be obtained from the actual package or lot certificate.",
                "No component value may be transferred automatically to a complete measurement chain.",
            ]
        )
    return {
        "schema_version": "1.0",
        "practice_id": "U2-P3",
        "status": "pass" if not errors else "fail",
        "component_count": len(components),
        "field_count": field_count,
        "models": found_models,
        "category_counts": dict(sorted(category_counts.items())),
        "intentionally_unresolved_field_count": missing_count,
        "errors": errors,
        "warnings": warnings,
        "clinical_or_regulatory_validation": False,
        "interpretation": "This offline audit checks traceability fields, categories, conditions and scope boundaries. It does not validate a component, measurement chain or clinical use.",
    }


def report_bytes(report: dict[str, Any]) -> bytes:
    return (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_report(fixture_path: Path, output: Path) -> dict[str, Any]:
    fixture = load_json(fixture_path)
    report = audit_fixture(fixture)
    fixture_bytes = fixture_path.read_bytes()
    report["fixture"] = {
        "fixture_id": fixture.get("fixture_id"),
        "sha256": hashlib.sha256(fixture_bytes).hexdigest(),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(report_bytes(report))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        fixture = load_json(args.fixture)
        report = audit_fixture(fixture)
        if args.output:
            report["fixture"] = {
                "fixture_id": fixture.get("fixture_id"),
                "sha256": hashlib.sha256(args.fixture.read_bytes()).hexdigest(),
            }
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(report_bytes(report))
        else:
            print(report_bytes(report).decode("utf-8"), end="")
    except AuditError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
