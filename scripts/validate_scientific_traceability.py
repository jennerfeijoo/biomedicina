#!/usr/bin/env python3
"""Valida registros afirmación–fuente y bloquea cursos completos sin trazabilidad."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIRECTORY = ROOT / "data" / "claim_registry"
ALLOWED_RISKS = {"low", "medium", "high"}
ALLOWED_TYPES = {
    "definition",
    "mechanism",
    "number",
    "equation",
    "inference",
    "recommendation",
    "regulation",
    "method",
    "safety",
    "clinical",
    "pedagogy",
}
ALLOWED_SUPPORT = {"direct", "partial", "contradictory", "unverifiable"}
ALLOWED_VERIFICATION = {
    "unverified",
    "verified_metadata",
    "verified_directly",
    "recommended_future_review",
    "superseded",
    "excluded",
}
LOCATOR_FIELDS = {"page", "section", "chapter", "table", "figure", "paragraph", "url_fragment"}


def validate_registry(payload: Any, label: str = "registry") -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return [f"{label} debe ser un objeto"]
    if payload.get("schema_version") != "1.0":
        errors.append(f"{label}.schema_version debe ser 1.0")
    for field in ("subject_id", "content_version", "content_commit"):
        if not str(payload.get(field) or "").strip():
            errors.append(f"{label}.{field} es obligatorio")

    claims = payload.get("claims")
    if not isinstance(claims, list):
        errors.append(f"{label}.claims debe ser una lista")
        return errors

    identifiers: set[str] = set()
    for index, claim in enumerate(claims):
        key = f"{label}.claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{key} debe ser un objeto")
            continue
        claim_id = str(claim.get("claim_id") or "").strip()
        if not claim_id:
            errors.append(f"{key}.claim_id es obligatorio")
        elif claim_id in identifiers:
            errors.append(f"{key}.claim_id está duplicado")
        identifiers.add(claim_id)

        if not str(claim.get("text") or "").strip():
            errors.append(f"{key}.text es obligatorio")
        if claim.get("claim_type") not in ALLOWED_TYPES:
            errors.append(f"{key}.claim_type no es válido")
        risk = claim.get("risk")
        if risk not in ALLOWED_RISKS:
            errors.append(f"{key}.risk no es válido")
        if claim.get("support") not in ALLOWED_SUPPORT:
            errors.append(f"{key}.support no es válido")
        verification = claim.get("source_verification_status")
        if verification not in ALLOWED_VERIFICATION:
            errors.append(f"{key}.source_verification_status no es válido")

        if risk in {"medium", "high"}:
            if not str(claim.get("source_id") or "").strip():
                errors.append(f"{key}: una afirmación {risk} requiere source_id")
            locator = claim.get("locator")
            if not isinstance(locator, dict) or not any(
                str(locator.get(field) or "").strip() for field in LOCATOR_FIELDS
            ):
                errors.append(f"{key}: una afirmación {risk} requiere localizador exacto")
        if risk == "high":
            if claim.get("support") != "direct":
                errors.append(f"{key}: una afirmación de riesgo alto requiere apoyo directo")
            if verification != "verified_directly":
                errors.append(
                    f"{key}: una afirmación de riesgo alto requiere fuente verificada directamente"
                )

        if claim.get("review_state") == "ai_review_validated" and not str(
            claim.get("reviewer_validation_id") or ""
        ).strip():
            errors.append(f"{key}: ai_review_validated requiere reviewer_validation_id")
    return errors


def complete_subject_ids() -> set[str]:
    subjects: set[str] = set()
    for path in (ROOT / "data" / "subjects").glob("*/*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if payload.get("status") == "complete":
            subjects.add(str(payload.get("id") or path.stem))
    for path in (ROOT / "data" / "course_redevelopment").glob("*/course.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if payload.get("status") == "complete":
            subjects.add(str(payload.get("id") or path.parent.name))
    return subjects


def validate_directory(directory: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    registered: set[str] = set()
    count = 0
    for path in sorted(directory.glob("*.json")):
        if path.name.startswith("_"):
            continue
        count += 1
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: JSON inválido: {exc}")
            continue
        label = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        errors.extend(validate_registry(payload, label))
        if isinstance(payload, dict):
            registered.add(str(payload.get("subject_id") or ""))

    missing = sorted(complete_subject_ids() - registered)
    if missing:
        errors.append(
            "Cursos complete sin registro de afirmaciones: " + ", ".join(missing)
        )
    return errors, count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=DEFAULT_DIRECTORY)
    args = parser.parse_args()
    directory = args.directory if args.directory.is_absolute() else ROOT / args.directory
    errors, count = validate_directory(directory)
    if errors:
        print("Errores de trazabilidad científica:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Trazabilidad científica: {count} registros activos · ningún complete sin evidencia")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
