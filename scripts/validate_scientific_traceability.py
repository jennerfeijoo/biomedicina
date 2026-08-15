#!/usr/bin/env python3
"""Valida afirmaciones, fuentes canónicas y correspondencia con el contenido."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIRECTORY = ROOT / "data" / "claim_registry"
SOURCE_DIRECTORY = ROOT / "data" / "source_registry"
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


def collect_strings(value: Any) -> list[str]:
    """Collect every authored string without flattening its semantic structure."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in collect_strings(item)]
    if isinstance(value, dict):
        return [text for item in value.values() for text in collect_strings(item)]
    return []


def load_source_records(subject_id: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    records: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    paths = [SOURCE_DIRECTORY / f"{subject_id}.json"]
    paths.extend(sorted(SOURCE_DIRECTORY.glob(f"{subject_id}-*.json")))
    paths = [path for path in paths if path.exists()]
    if not paths:
        return {}, [f"{subject_id}: falta registro canónico de fuentes"]

    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: JSON inválido: {exc}")
            continue
        if not isinstance(payload, dict) or payload.get("subject_id") != subject_id:
            errors.append(f"{path.relative_to(ROOT)}: subject_id inconsistente")
            continue
        sources = payload.get("sources")
        if not isinstance(sources, list):
            errors.append(f"{path.relative_to(ROOT)}: sources debe ser una lista")
            continue
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"{path.relative_to(ROOT)}.sources[{index}] debe ser un objeto")
                continue
            source_id = str(source.get("id") or "").strip()
            if not source_id:
                errors.append(f"{path.relative_to(ROOT)}.sources[{index}].id es obligatorio")
                continue
            if source_id in records:
                errors.append(f"{subject_id}: source_id duplicado: {source_id}")
                continue
            verification = source.get("verification_status")
            if verification not in ALLOWED_VERIFICATION:
                errors.append(
                    f"{path.relative_to(ROOT)}.sources[{index}].verification_status no es válido"
                )
            records[source_id] = source
    return records, errors


def load_unit_strings(subject_id: str) -> dict[int, list[str]]:
    by_unit: dict[int, list[str]] = {}
    directories = (
        ROOT / "data" / "generated_units" / subject_id,
        ROOT / "data" / "course_redevelopment" / subject_id / "units",
    )
    for directory in directories:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("unit-*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if not isinstance(payload, dict):
                continue
            try:
                unit = int(payload.get("unit"))
            except (TypeError, ValueError):
                continue
            by_unit.setdefault(unit, []).extend(collect_strings(payload))
    return by_unit


def validate_registry(
    payload: Any,
    label: str = "registry",
    *,
    source_records: dict[str, dict[str, Any]] | None = None,
    content_strings: dict[int, list[str]] | None = None,
) -> list[str]:
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
        try:
            unit = int(claim.get("unit"))
        except (TypeError, ValueError):
            unit = 0
        if unit < 1:
            errors.append(f"{key}.unit debe ser un entero positivo")
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
            source_id = str(claim.get("source_id") or "").strip()
            if not source_id:
                errors.append(f"{key}: una afirmación {risk} requiere source_id")
            locator = claim.get("locator")
            if not isinstance(locator, dict) or not any(
                str(locator.get(field) or "").strip() for field in LOCATOR_FIELDS
            ):
                errors.append(f"{key}: una afirmación {risk} requiere localizador exacto")
            if source_records is not None:
                source = source_records.get(source_id)
                if source is None:
                    errors.append(f"{key}: source_id `{source_id}` no existe en el registro canónico")
                elif (
                    verification == "verified_directly"
                    and source.get("verification_status") != "verified_directly"
                ):
                    errors.append(
                        f"{key}: la afirmación declara verificación directa, pero `{source_id}` "
                        "no está verificada directamente"
                    )
        if risk == "high":
            if claim.get("support") != "direct":
                errors.append(f"{key}: una afirmación de riesgo alto requiere apoyo directo")
            if verification != "verified_directly":
                errors.append(
                    f"{key}: una afirmación de riesgo alto requiere fuente verificada directamente"
                )

        if content_strings is not None and unit > 0:
            text = str(claim.get("text") or "").strip()
            unit_strings = content_strings.get(unit)
            if not unit_strings:
                errors.append(f"{key}: no existe contenido canónico para la unidad {unit}")
            elif text and not any(text in authored for authored in unit_strings):
                errors.append(f"{key}: el texto no aparece en la unidad canónica {unit}")

        if claim.get("review_state") == "ai_review_validated" and not str(
            claim.get("reviewer_validation_id") or ""
        ).strip():
            errors.append(f"{key}: ai_review_validated requiere reviewer_validation_id")
    return errors


def validate_repository_registry(payload: Any, label: str = "registry") -> list[str]:
    if not isinstance(payload, dict):
        return validate_registry(payload, label)
    subject_id = str(payload.get("subject_id") or "").strip()
    if not subject_id:
        return validate_registry(payload, label)
    sources, source_errors = load_source_records(subject_id)
    return [
        *source_errors,
        *validate_registry(
            payload,
            label,
            source_records=sources,
            content_strings=load_unit_strings(subject_id),
        ),
    ]


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
        errors.extend(validate_repository_registry(payload, label))
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
