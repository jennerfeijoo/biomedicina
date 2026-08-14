#!/usr/bin/env python3
"""Valida el contenido enriquecido producido por el agente autónomo.

Solo examina overlays con generation_metadata.autonomous_agent=true. De este modo puede
incorporarse antes de que todas las asignaturas hayan sido regeneradas por el agente.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from citonauta_agent.reviewer_validation import find_applicable_validation  # noqa: E402

SUBJECTS_DIR = ROOT / "data" / "subjects"
REVIEWER_VALIDATIONS = ROOT / "data" / "reviewer_validations"
WORD_RE = re.compile(r"\b[\wáéíóúüñÁÉÍÓÚÜÑ]+\b", re.UNICODE)


def require_list(
    data: dict[str, Any],
    field: str,
    minimum: int,
    key: str,
    errors: list[str],
) -> list[Any]:
    value = data.get(field)
    if not isinstance(value, list) or len(value) < minimum:
        length = len(value) if isinstance(value, list) else "no es lista"
        errors.append(f"{key}.{field} requiere al menos {minimum} elementos; tiene {length}")
        return []
    return value


def validate_overlay(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    metadata = data.get("generation_metadata")
    if not isinstance(metadata, dict) or not metadata.get("autonomous_agent"):
        return errors

    key = path.relative_to(ROOT).as_posix()
    status = data.get("status")
    if status not in {"review", "complete"}:
        errors.append(f"{key}.status debe ser review o complete")
    review_state = metadata.get("review_state")
    validation_id = metadata.get("reviewer_validation_id")
    if status == "review" and review_state != "ai_review_provisional":
        errors.append(f"{key}: review requiere ai_review_provisional")
    if status == "complete":
        if review_state != "ai_review_validated":
            errors.append(f"{key}: complete requiere ai_review_validated")
        if not str(validation_id or "").strip():
            errors.append(f"{key}: complete requiere reviewer_validation_id")
        applicable = find_applicable_validation(
            REVIEWER_VALIDATIONS,
            provider=str(metadata.get("review_provider") or ""),
            model=str(metadata.get("review_model") or ""),
            model_version=str(metadata.get("review_model_version") or ""),
            prompt_id=str(metadata.get("review_prompt_id") or ""),
            rubric_version=str(metadata.get("review_rubric_version") or ""),
            domain=str(metadata.get("review_domain") or ""),
            risk_level=str(metadata.get("review_risk_level") or ""),
            claim_types=[str(item) for item in metadata.get("review_claim_types") or []],
            language="es",
            source_access=str(metadata.get("source_access") or ""),
            author_context_isolated=True,
            blind_to_author_rationale=True,
        )
        if applicable is None or applicable.get("validation_id") != validation_id:
            errors.append(f"{key}: reviewer_validation_id no es aplicable o está vencido")

    minimums = {
        "prerequisites": 3,
        "course_competencies": 4,
        "learning_objectives": 4,
        "learning_outcomes": 6,
        "modules": 6,
        "detailed_units": 6,
        "practical_activities": 4,
        "assessment": 3,
        "key_concepts": 10,
        "related_subjects": 4,
        "suggested_resources": 5,
        "sources_used": 5,
    }
    for field, minimum in minimums.items():
        require_list(data, field, minimum, key, errors)

    units = data.get("detailed_units", [])
    if isinstance(units, list) and len(units) > 10:
        errors.append(f"{key}.detailed_units no puede superar 10 unidades")
    expected_numbers = list(range(1, len(units) + 1)) if isinstance(units, list) else []
    actual_numbers = [unit.get("unit") for unit in units if isinstance(unit, dict)]
    if actual_numbers != expected_numbers:
        errors.append(f"{key}.detailed_units debe numerarse consecutivamente")

    text_fragments: list[str] = []
    for field in (
        "description",
        "biomedical_connection",
        "level",
    ):
        text_fragments.append(str(data.get(field, "")))

    for index, unit in enumerate(units, start=1):
        if not isinstance(unit, dict):
            errors.append(f"{key}.detailed_units[{index}] debe ser un objeto")
            continue
        text_fragments.extend([str(unit.get("title", "")), str(unit.get("description", ""))])
        for field, minimum in (
            ("explanations", 2),
            ("topics", 3),
            ("learning_outcomes", 2),
            ("worked_examples", 1),
            ("activities", 2),
            ("self_check", 2),
            ("common_misconceptions", 2),
            ("biomedical_applications", 1),
        ):
            require_list(unit, field, minimum, f"{key}.detailed_units[{index}]", errors)

        for block_index, block in enumerate(unit.get("explanations", []), start=1):
            if not isinstance(block, dict):
                errors.append(
                    f"{key}.detailed_units[{index}].explanations[{block_index}] debe ser un objeto"
                )
                continue
            paragraphs = require_list(
                block,
                "paragraphs",
                2,
                f"{key}.detailed_units[{index}].explanations[{block_index}]",
                errors,
            )
            require_list(
                block,
                "key_points",
                3,
                f"{key}.detailed_units[{index}].explanations[{block_index}]",
                errors,
            )
            text_fragments.extend(str(value) for value in paragraphs)

        for example in unit.get("worked_examples", []):
            if isinstance(example, dict):
                text_fragments.extend(
                    [
                        str(example.get("scenario", "")),
                        str(example.get("conclusion", "")),
                        *[str(value) for value in example.get("reasoning_steps", [])],
                    ]
                )
        for check in unit.get("self_check", []):
            if isinstance(check, dict):
                text_fragments.extend(
                    [str(check.get("question", "")), str(check.get("answer", ""))]
                )

    word_count = len(WORD_RE.findall(" ".join(text_fragments)))
    if word_count < 2200:
        errors.append(f"{key} contiene {word_count} palabras enriquecidas; mínimo: 2200")

    weights: list[int] = []
    for item in data.get("assessment", []):
        if not isinstance(item, dict):
            continue
        raw = str(item.get("weight", "")).strip().rstrip("%")
        if raw.isdigit():
            weights.append(int(raw))
    if not weights or sum(weights) != 100:
        errors.append(f"{key}.assessment debe incluir pesos que sumen 100%")

    for resource in data.get("suggested_resources", []) + data.get("sources_used", []):
        if isinstance(resource, dict):
            url = str(resource.get("url", ""))
            if not url.startswith(("https://", "http://")):
                errors.append(f"{key} contiene una fuente sin URL HTTP segura: {url!r}")

    return errors


def main() -> int:
    paths = sorted(SUBJECTS_DIR.glob("*/*.json"))
    errors: list[str] = []
    validated = 0
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        if (data.get("generation_metadata") or {}).get("autonomous_agent"):
            validated += 1
        errors.extend(validate_overlay(path))

    if errors:
        print("Errores en contenido enriquecido:\n")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validación de contenido enriquecido completada.")
    print(f"- overlays autónomos validados: {validated}")
    print("- resultado: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
