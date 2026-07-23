#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = ROOT / "data" / "generated_courses"
COVERAGE_ROOT = ROOT / "data" / "curriculum_coverage"
ALLOWED_STATES = {"missing", "partial", "implemented", "verified", "out_of_scope"}
MIN_CORE_DOMAINS = 5
MIN_TOPICS_PER_DOMAIN = 4
MIN_MASTERY_EVIDENCE = 1
MIN_PRACTICAL_REQUIREMENTS = 3
MIN_VISUAL_REQUIREMENTS = 2


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("la raíz debe ser un objeto JSON")
    return data


def load_coverage() -> tuple[dict[str, dict[str, Any]], list[str]]:
    courses: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    paths = sorted(COVERAGE_ROOT.glob("*.json"))
    if not paths:
        return {}, ["no existen matrices en data/curriculum_coverage"]

    for path in paths:
        try:
            data = load_json(path)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            errors.append(f"{path.relative_to(ROOT)}: JSON inválido: {error}")
            continue
        if data.get("schema_version") != "1.0":
            errors.append(f"{path.relative_to(ROOT)}: schema_version debe ser 1.0")
        if data.get("portfolio_standard") != "coverage-based":
            errors.append(f"{path.relative_to(ROOT)}: portfolio_standard debe ser coverage-based")
        file_courses = data.get("courses")
        if not isinstance(file_courses, dict):
            errors.append(f"{path.relative_to(ROOT)}: falta objeto courses")
            continue
        for subject_id, specification in file_courses.items():
            if subject_id in courses:
                errors.append(f"{subject_id}: aparece en más de una matriz")
            elif isinstance(specification, dict):
                courses[subject_id] = specification
            else:
                errors.append(f"{subject_id}: especificación no es un objeto")
    return courses, errors


def audit_spec(subject_id: str, spec: dict[str, Any], require_verified: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    state = str(spec.get("coverage_state", ""))
    if state not in ALLOWED_STATES:
        errors.append(f"coverage_state inválido: {state or 'ausente'}")
    elif require_verified and state != "verified":
        errors.append(f"coverage_state={state}; se requiere verified")
    elif state in {"partial", "missing"}:
        warnings.append(f"cobertura declarada como {state}")

    if not str(spec.get("title", "")).strip():
        errors.append("falta title")

    domains = spec.get("core_domains")
    if not isinstance(domains, list) or len(domains) < MIN_CORE_DOMAINS:
        errors.append(f"requiere al menos {MIN_CORE_DOMAINS} dominios nucleares")
        domains = domains if isinstance(domains, list) else []

    domain_ids: list[str] = []
    for index, domain in enumerate(domains, start=1):
        if not isinstance(domain, dict):
            errors.append(f"dominio {index} no es un objeto")
            continue
        domain_id = str(domain.get("id", "")).strip()
        if not domain_id:
            errors.append(f"dominio {index} sin id")
        else:
            domain_ids.append(domain_id)
        if not str(domain.get("title", "")).strip():
            errors.append(f"dominio {domain_id or index} sin title")
        topics = domain.get("required_topics")
        if not isinstance(topics, list) or len(topics) < MIN_TOPICS_PER_DOMAIN:
            errors.append(f"dominio {domain_id or index}: menos de {MIN_TOPICS_PER_DOMAIN} temas obligatorios")
        elif any(not isinstance(topic, str) or not topic.strip() for topic in topics):
            errors.append(f"dominio {domain_id or index}: tema vacío o no textual")
        mastery = domain.get("mastery_evidence")
        if not isinstance(mastery, list) or len(mastery) < MIN_MASTERY_EVIDENCE:
            errors.append(f"dominio {domain_id or index}: falta evidencia de dominio")

    if len(domain_ids) != len(set(domain_ids)):
        errors.append("ids de dominios duplicados")

    practical = spec.get("practical_requirements")
    if not isinstance(practical, list) or len(practical) < MIN_PRACTICAL_REQUIREMENTS:
        errors.append(f"requiere al menos {MIN_PRACTICAL_REQUIREMENTS} requisitos prácticos")

    visuals = spec.get("visual_requirements")
    if not isinstance(visuals, list) or len(visuals) < MIN_VISUAL_REQUIREMENTS:
        errors.append(f"requiere al menos {MIN_VISUAL_REQUIREMENTS} requisitos visuales")

    priorities = spec.get("expansion_priorities")
    if state != "verified" and (not isinstance(priorities, list) or not priorities):
        errors.append("una cobertura no verificada debe declarar expansion_priorities")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audita cobertura disciplinar declarada sin utilizar conteos de palabras."
    )
    parser.add_argument("--strict", action="store_true", help="Falla ante matrices ausentes o mal formadas.")
    parser.add_argument(
        "--require-verified",
        action="store_true",
        help="Falla si alguna asignatura no ha sido revisada externamente y marcada verified.",
    )
    parser.add_argument("--json-output", help="Ruta opcional para guardar el informe JSON.")
    args = parser.parse_args()

    specifications, load_errors = load_coverage()
    generated = {path.stem for path in COURSE_ROOT.glob("*.json")}
    specified = set(specifications)

    errors = list(load_errors)
    warnings: list[str] = []
    for missing in sorted(generated - specified):
        errors.append(f"{missing}: falta matriz de cobertura")
    for orphan in sorted(specified - generated):
        warnings.append(f"{orphan}: matriz sin curso generado")

    course_results: dict[str, Any] = {}
    for subject_id in sorted(generated & specified):
        course_errors, course_warnings = audit_spec(
            subject_id, specifications[subject_id], args.require_verified
        )
        errors.extend(f"{subject_id}: {item}" for item in course_errors)
        warnings.extend(f"{subject_id}: {item}" for item in course_warnings)
        course_results[subject_id] = {
            "coverage_state": specifications[subject_id].get("coverage_state"),
            "core_domains": len(specifications[subject_id].get("core_domains", [])),
            "errors": course_errors,
            "warnings": course_warnings,
        }

    report = {
        "standard": "coverage-based",
        "word_limits_used": False,
        "courses_generated": len(generated),
        "courses_with_coverage": len(generated & specified),
        "courses": course_results,
        "errors": errors,
        "warnings": warnings,
    }
    if args.json_output:
        output = ROOT / args.json_output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("AUDITORÍA DE COMPLETITUD CURRICULAR")
    print(f"Cursos generados: {len(generated)} · con matriz: {len(generated & specified)}")
    for subject_id, result in course_results.items():
        print(
            f"- {subject_id}: estado={result['coverage_state']} · "
            f"dominios={result['core_domains']} · errores={len(result['errors'])}"
        )
    for warning in warnings:
        print(f"ADVERTENCIA {warning}")
    for error in errors:
        print(f"ERROR {error}")
    print("La extensión textual se reporta fuera de esta auditoría y no determina completitud.")

    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
