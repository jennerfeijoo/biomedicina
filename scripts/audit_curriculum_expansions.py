#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COVERAGE_ROOT = ROOT / "data" / "curriculum_coverage"
EXPANSION_ROOT = ROOT / "data" / "curriculum_expansions"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("la raíz debe ser un objeto JSON")
    return data


def coverage_specs() -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for path in sorted(COVERAGE_ROOT.glob("*.json")):
        data = load_json(path)
        for subject_id, spec in data.get("courses", {}).items():
            if subject_id in merged:
                raise ValueError(f"{subject_id}: matriz duplicada")
            merged[subject_id] = spec
    return merged


def nonempty_list(value: Any, minimum: int = 1) -> bool:
    return isinstance(value, list) and len(value) >= minimum and all(item not in (None, "") for item in value)


def audit_expansion(path: Path, coverage: dict[str, dict[str, Any]]) -> dict[str, Any]:
    data = load_json(path)
    subject_id = str(data.get("subject_id", "")).strip()
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("schema_version") != "1.0":
        errors.append("schema_version debe ser 1.0")
    if not subject_id:
        errors.append("falta subject_id")
        return {"subject_id": subject_id, "errors": errors, "warnings": warnings}
    spec = coverage.get(subject_id)
    if not spec:
        errors.append("no existe matriz de cobertura correspondiente")
        return {"subject_id": subject_id, "errors": errors, "warnings": warnings}
    if data.get("implementation_state") not in {"implemented", "verified"}:
        errors.append("implementation_state debe ser implemented o verified")
    if data.get("academic_status") != "review" and data.get("implementation_state") != "verified":
        errors.append("una expansión no verificada debe conservar academic_status=review")
    if not nonempty_list(data.get("source_basis"), 2):
        errors.append("requiere al menos dos fuentes base")

    required_domains = {d.get("id"): d for d in spec.get("core_domains", []) if isinstance(d, dict)}
    implementations = data.get("domain_implementation")
    if not isinstance(implementations, list):
        implementations = []
        errors.append("falta domain_implementation")
    by_id = {d.get("domain_id"): d for d in implementations if isinstance(d, dict)}
    missing = sorted(set(required_domains) - set(by_id))
    extra = sorted(set(by_id) - set(required_domains))
    if missing:
        errors.append("dominios sin implementación: " + ", ".join(missing))
    if extra:
        errors.append("dominios no definidos en matriz: " + ", ".join(extra))

    for domain_id, required in required_domains.items():
        impl = by_id.get(domain_id)
        if not impl:
            continue
        required_topics = set(required.get("required_topics", []))
        implemented_topics = set(impl.get("required_topics", []))
        absent_topics = sorted(required_topics - implemented_topics)
        if absent_topics:
            errors.append(f"{domain_id}: temas obligatorios ausentes: {', '.join(absent_topics)}")
        if not nonempty_list(impl.get("course_units")):
            errors.append(f"{domain_id}: falta mapeo a unidades")
        if not nonempty_list(impl.get("mastery_evidence"), 2):
            errors.append(f"{domain_id}: requiere dos evidencias de dominio")
        if not nonempty_list(impl.get("lecture_expansions"), 2):
            errors.append(f"{domain_id}: requiere al menos dos expansiones teóricas")
        if not nonempty_list(impl.get("quantitative_tasks"), 2):
            errors.append(f"{domain_id}: requiere tareas cuantitativas")
        workshop = impl.get("literature_workshop")
        if not isinstance(workshop, dict) or not nonempty_list(workshop.get("evidence_to_extract"), 4):
            errors.append(f"{domain_id}: taller de literatura insuficiente")
        if not nonempty_list(impl.get("visual_assets"), 2):
            errors.append(f"{domain_id}: recursos visuales insuficientes")

    labs = data.get("laboratory_program")
    if not isinstance(labs, list) or len(labs) < 8:
        errors.append("requiere al menos ocho laboratorios o análisis prácticos")
        labs = labs if isinstance(labs, list) else []
    lab_ids = [lab.get("id") for lab in labs if isinstance(lab, dict)]
    if len(lab_ids) != len(set(lab_ids)):
        errors.append("ids de laboratorio duplicados")
    for lab in labs:
        if not isinstance(lab, dict):
            errors.append("laboratorio no es un objeto")
            continue
        for field in ("id", "title", "basis", "mode"):
            if not str(lab.get(field, "")).strip():
                errors.append(f"laboratorio {lab.get('id','?')}: falta {field}")
        if not nonempty_list(lab.get("measurements")) or not nonempty_list(lab.get("controls")):
            errors.append(f"laboratorio {lab.get('id','?')}: faltan mediciones o controles")
        if not nonempty_list(lab.get("deliverables")):
            errors.append(f"laboratorio {lab.get('id','?')}: faltan entregables")

    literature = data.get("literature_program", {})
    if int(literature.get("minimum_primary_articles", 0)) < len(required_domains):
        errors.append("el mínimo de artículos primarios debe cubrir todos los dominios")
    if not nonempty_list(literature.get("reading_template"), 6):
        errors.append("plantilla de lectura primaria insuficiente")

    visuals = data.get("visual_program", {})
    if int(visuals.get("required_asset_count", 0)) < 2 * len(required_domains):
        errors.append("cantidad de activos visuales insuficiente")

    mastery = data.get("mastery_assessment", {})
    checks = mastery.get("domain_checks") if isinstance(mastery, dict) else None
    check_ids = {item.get("domain_id") for item in checks or [] if isinstance(item, dict)}
    if check_ids != set(required_domains):
        errors.append("mastery_assessment no cubre exactamente los dominios de la matriz")

    if data.get("implementation_state") == "verified" and not nonempty_list(data.get("external_review_evidence")):
        errors.append("verified requiere external_review_evidence")
    elif data.get("implementation_state") == "implemented":
        warnings.append("implementación completa pendiente de revisión académica externa")

    return {
        "subject_id": subject_id,
        "implementation_state": data.get("implementation_state"),
        "domains": len(by_id),
        "laboratories": len(labs),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita expansiones disciplinares contra matrices de cobertura.")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--subject")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    coverage = coverage_specs()
    paths = sorted(EXPANSION_ROOT.glob("*.json"))
    if args.subject:
        paths = [p for p in paths if p.stem == args.subject]
    results = []
    errors: list[str] = []
    warnings: list[str] = []
    for path in paths:
        try:
            result = audit_expansion(path, coverage)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            result = {"subject_id": path.stem, "errors": [f"JSON inválido: {exc}"], "warnings": []}
        results.append(result)
        errors.extend(f"{result['subject_id']}: {msg}" for msg in result.get("errors", []))
        warnings.extend(f"{result['subject_id']}: {msg}" for msg in result.get("warnings", []))
    if args.subject and not paths:
        errors.append(f"{args.subject}: no existe expansión disciplinar")
    report = {"standard":"discipline-expansion-1.0","expansions":results,"errors":errors,"warnings":warnings}
    if args.json_output:
        output = ROOT / args.json_output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("AUDITORÍA DE EXPANSIONES DISCIPLINARES")
    for result in results:
        print(f"- {result['subject_id']}: estado={result.get('implementation_state')} · dominios={result.get('domains',0)} · laboratorios={result.get('laboratories',0)} · errores={len(result.get('errors',[]))}")
    for warning in warnings:
        print("ADVERTENCIA", warning)
    for error in errors:
        print("ERROR", error)
    return 1 if args.strict and errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
