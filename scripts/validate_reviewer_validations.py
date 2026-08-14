#!/usr/bin/env python3
"""Valida registros que habilitan o bloquean la revisión científica mediante IA."""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIRECTORY = ROOT / "data" / "reviewer_validations"
ALLOWED_STATUSES = {"unvalidated", "validated_for_scope", "expired", "out_of_scope"}
ALLOWED_RISKS = {"low", "medium", "high"}
REQUIRED_COMPARISONS = {"ai_human", "human_human", "ai_ai"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _mapping(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} debe ser un objeto")
        return {}
    return value


def _nonempty_list(value: Any, label: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list) or not value:
        errors.append(f"{label} debe ser una lista no vacía")
        return []
    return value


def _iso_date(value: Any, label: str, errors: list[str]) -> date | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} debe ser una fecha ISO")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label} no es una fecha ISO válida")
        return None


def validate_manifest(payload: Any, label: str = "manifest") -> list[str]:
    errors: list[str] = []
    data = _mapping(payload, label, errors)
    if not data:
        return errors

    if data.get("schema_version") != "1.0":
        errors.append(f"{label}.schema_version debe ser 1.0")
    if not str(data.get("validation_id") or "").strip():
        errors.append(f"{label}.validation_id es obligatorio")

    status = data.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"{label}.status no pertenece al vocabulario permitido")

    reviewer = _mapping(data.get("reviewer"), f"{label}.reviewer", errors)
    for field in ("system_id", "provider", "model", "model_version", "prompt_id", "rubric_version"):
        if not str(reviewer.get(field) or "").strip():
            errors.append(f"{label}.reviewer.{field} es obligatorio")

    scope = _mapping(data.get("scope"), f"{label}.scope", errors)
    _nonempty_list(scope.get("domains"), f"{label}.scope.domains", errors)
    risks = _nonempty_list(
        scope.get("claim_risk_levels"), f"{label}.scope.claim_risk_levels", errors
    )
    invalid_risks = sorted({str(item) for item in risks} - ALLOWED_RISKS)
    if invalid_risks:
        errors.append(f"{label}.scope contiene riesgos inválidos: {', '.join(invalid_risks)}")
    _nonempty_list(scope.get("claim_types"), f"{label}.scope.claim_types", errors)
    _nonempty_list(scope.get("languages"), f"{label}.scope.languages", errors)
    if scope.get("source_access_required") not in {
        "metadata_or_abstract",
        "localized_excerpt",
        "localized_full_text",
    }:
        errors.append(f"{label}.scope.source_access_required no es válido")

    independence = _mapping(data.get("independence"), f"{label}.independence", errors)
    for field in (
        "author_context_isolated",
        "blind_to_author_rationale",
        "reviewer_does_not_edit_before_decision",
        "shared_base_model",
    ):
        if not isinstance(independence.get(field), bool):
            errors.append(f"{label}.independence.{field} debe ser booleano")

    evidence = _mapping(data.get("evidence"), f"{label}.evidence", errors)
    validity = _mapping(data.get("validity"), f"{label}.validity", errors)
    authorization = _mapping(data.get("authorization"), f"{label}.authorization", errors)
    for field in (
        "can_authorize_publication",
        "can_auto_merge",
        "requires_zero_critical_findings",
        "abstain_out_of_scope",
    ):
        if not isinstance(authorization.get(field), bool):
            errors.append(f"{label}.authorization.{field} debe ser booleano")

    if status != "validated_for_scope":
        if authorization.get("can_authorize_publication") is not False:
            errors.append(f"{label}: un revisor no validado no puede autorizar publicación")
        if authorization.get("can_auto_merge") is not False:
            errors.append(f"{label}: un revisor no validado no puede autorizar auto-merge")
        return errors

    configuration_sha = reviewer.get("configuration_sha256")
    if not isinstance(configuration_sha, str) or not SHA256_RE.fullmatch(configuration_sha):
        errors.append(f"{label}.reviewer.configuration_sha256 debe congelar la configuración")
    if evidence.get("study_status") != "completed":
        errors.append(f"{label}.evidence.study_status debe ser completed")
    if not str(evidence.get("preregistration") or "").strip():
        errors.append(f"{label}.evidence.preregistration es obligatoria")
    if not isinstance(evidence.get("sample_size"), int) or evidence.get("sample_size", 0) <= 0:
        errors.append(f"{label}.evidence.sample_size debe ser positivo")
    if (
        not isinstance(evidence.get("human_reference_reviewers"), int)
        or evidence.get("human_reference_reviewers", 0) < 2
    ):
        errors.append(f"{label}: se requieren al menos dos revisores humanos de referencia")

    comparisons = set(evidence.get("comparisons") or [])
    missing_comparisons = sorted(REQUIRED_COMPARISONS - comparisons)
    if missing_comparisons:
        errors.append(f"{label}: faltan comparaciones: {', '.join(missing_comparisons)}")

    margin = evidence.get("noninferiority_margin_critical_error_sensitivity")
    if not isinstance(margin, (int, float)) or isinstance(margin, bool) or not 0 < margin < 1:
        errors.append(f"{label}: el margen de no inferioridad debe estar entre 0 y 1")

    sensitivity = _mapping(
        evidence.get("critical_error_sensitivity"),
        f"{label}.evidence.critical_error_sensitivity",
        errors,
    )
    values = [sensitivity.get(field) for field in ("estimate", "ci_low", "ci_high")]
    if any(
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not 0 <= value <= 1
        for value in values
    ):
        errors.append(f"{label}: sensibilidad e intervalo deben estar entre 0 y 1")
    elif not values[1] <= values[0] <= values[2]:
        errors.append(f"{label}: intervalo de sensibilidad incoherente")
    if evidence.get("noninferiority_passed") is not True:
        errors.append(f"{label}: la no inferioridad no está demostrada")

    valid_from = _iso_date(validity.get("valid_from"), f"{label}.validity.valid_from", errors)
    valid_until = _iso_date(validity.get("valid_until"), f"{label}.validity.valid_until", errors)
    if valid_from and valid_until and valid_until < valid_from:
        errors.append(f"{label}: valid_until precede a valid_from")
    if not str(validity.get("content_commit") or "").strip():
        errors.append(f"{label}.validity.content_commit es obligatorio")

    if authorization.get("can_authorize_publication") is not True:
        errors.append(f"{label}: validated_for_scope debe declarar la decisión de publicación")
    if authorization.get("requires_zero_critical_findings") is not True:
        errors.append(f"{label}: debe exigir cero hallazgos críticos")
    if authorization.get("abstain_out_of_scope") is not True:
        errors.append(f"{label}: debe abstenerse fuera de alcance")
    return errors


def validate_directory(directory: Path) -> list[str]:
    errors: list[str] = []
    paths = sorted(directory.glob("*.json"))
    if not paths:
        return [f"No existen manifiestos en {directory}"]
    identifiers: set[str] = set()
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: JSON inválido: {exc}")
            continue
        label = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        errors.extend(validate_manifest(payload, label))
        validation_id = str(payload.get("validation_id") or "") if isinstance(payload, dict) else ""
        if validation_id in identifiers:
            errors.append(f"{label}: validation_id duplicado")
        identifiers.add(validation_id)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=DEFAULT_DIRECTORY)
    args = parser.parse_args()
    directory = args.directory if args.directory.is_absolute() else ROOT / args.directory
    errors = validate_directory(directory)
    if errors:
        print("Errores en registros de validez del revisor:")
        for error in errors:
            print(f"- {error}")
        return 1
    count = len(list(directory.glob("*.json")))
    print(f"Registros de validez del revisor: {count} · contrato válido")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
