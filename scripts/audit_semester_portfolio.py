#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = ROOT / "data" / "generated_courses"
UNIT_ROOT = ROOT / "data" / "generated_units"
ASSET_ROOT = ROOT / "assets" / "js"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)
SPACE_RE = re.compile(r"\s+")

FORBIDDEN_PUBLIC_PHRASES = (
    "contenido desarrollado",
    "unidades desarrolladas",
    "ejemplo desarrollado",
    "en revisión académica",
    "pendiente de ampliación",
    "generado automáticamente",
)
GENERIC_SOURCE_PATHS = {
    "",
    "/",
    "/books/",
    "/books",
    "/search/",
    "/search",
}
MIN_SOURCE_DOMAINS_PER_UNIT = 3
MIN_COURSE_RESOURCE_DOMAINS = 4
MAX_HOUR_MISMATCH = 8
MIN_DUPLICATE_PARAGRAPH_CHARS = 180


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("la raíz debe ser un objeto")
    return data


def normalized(text: str) -> str:
    return SPACE_RE.sub(" ", text.strip().casefold())


def source_domain(url: str) -> str:
    host = urlparse(url).netloc.casefold()
    return host.removeprefix("www.")


def is_generic_source(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.path.casefold() in GENERIC_SOURCE_PATHS


def unit_paths(subject_id: str) -> list[Path]:
    return sorted((UNIT_ROOT / subject_id).glob("unit-*.json"))


def paragraph_records(subject_id: str, units: list[dict[str, Any]]) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    for unit in units:
        label = f"{subject_id}/unit-{int(unit.get('unit', 0)):02d}"
        for section in unit.get("theory_sections", []):
            for paragraph in section.get("paragraphs", []):
                if isinstance(paragraph, str) and len(normalized(paragraph)) >= MIN_DUPLICATE_PARAGRAPH_CHARS:
                    records.append((label, paragraph))
    return records


def audit_public_hygiene(errors: list[str]) -> None:
    candidates = list(ASSET_ROOT.glob("*.js"))
    candidates.extend(ROOT.glob("asignaturas/**/index.html"))
    for path in candidates:
        text = path.read_text(encoding="utf-8", errors="replace").casefold()
        for phrase in FORBIDDEN_PUBLIC_PHRASES:
            if phrase in text:
                errors.append(f"INTERFAZ {path.relative_to(ROOT)} contiene frase interna: {phrase}")

    workflow = ROOT / ".github" / "workflows" / "citonauta-quality.yml"
    if workflow.exists() and "contents: write" in workflow.read_text(encoding="utf-8"):
        errors.append("CI conserva permiso contents: write; los quality gates deben ser de solo lectura")


def audit_course(
    course_path: Path,
    errors: list[str],
    warnings: list[str],
    metrics: dict[str, Any],
    all_paragraphs: list[tuple[str, str]],
) -> None:
    subject_id = course_path.stem
    course = load_json(course_path)
    paths = unit_paths(subject_id)
    units = [load_json(path) for path in paths]
    prefix = subject_id

    if course.get("subject_id") != subject_id:
        errors.append(f"{prefix}: subject_id del curso no coincide con el archivo")
    if course.get("schema_version") != "2.0":
        errors.append(f"{prefix}: arquitectura sin schema_version 2.0")
    if course.get("status") != "review":
        errors.append(f"{prefix}: status interno debe permanecer en review hasta revisión humana externa")
    if not units:
        errors.append(f"{prefix}: no tiene unidades")
        return

    numbers = [int(unit.get("unit", 0) or 0) for unit in units]
    expected_numbers = list(range(1, len(units) + 1))
    if numbers != expected_numbers:
        errors.append(f"{prefix}: numeración de unidades no consecutiva: {numbers}")
    if any(unit.get("subject_id") != subject_id for unit in units):
        errors.append(f"{prefix}: alguna unidad tiene subject_id inconsistente")
    if any(unit.get("schema_version") != "2.0" for unit in units):
        errors.append(f"{prefix}: todas las unidades deben usar schema_version 2.0")
    if any(unit.get("status") != "review" for unit in units):
        errors.append(f"{prefix}: todas las unidades deben conservar status review")

    duration = int(course.get("duration_weeks", 0) or 0)
    expected_weeks = set(range(1, duration + 1))
    semester_plan = course.get("semester_plan", [])
    plan_weeks = [int(row.get("week", 0) or 0) for row in semester_plan if isinstance(row, dict)]
    if len(plan_weeks) != len(set(plan_weeks)):
        errors.append(f"{prefix}: el cronograma contiene semanas duplicadas")
    if set(plan_weeks) != expected_weeks:
        missing = sorted(expected_weeks - set(plan_weeks))
        extra = sorted(set(plan_weeks) - expected_weeks)
        errors.append(f"{prefix}: cobertura semanal incorrecta; faltan={missing}, sobran={extra}")

    unit_week_owner: dict[int, int] = {}
    for unit in units:
        number = int(unit["unit"])
        weeks = unit.get("weeks", [])
        if not isinstance(weeks, list) or not weeks:
            errors.append(f"{prefix}/unit-{number:02d}: no tiene semanas asignadas")
            continue
        for week in weeks:
            week = int(week)
            if week not in expected_weeks:
                errors.append(f"{prefix}/unit-{number:02d}: semana {week} fuera del semestre")
            if week in unit_week_owner:
                errors.append(
                    f"{prefix}: semana {week} asignada a unidades {unit_week_owner[week]} y {number}"
                )
            unit_week_owner[week] = number
    if set(unit_week_owner) != expected_weeks:
        missing = sorted(expected_weeks - set(unit_week_owner))
        errors.append(f"{prefix}: semanas no cubiertas por unidades: {missing}")

    for row in semester_plan:
        if not isinstance(row, dict):
            continue
        week = int(row.get("week", 0) or 0)
        planned_unit = int(row.get("unit", 0) or 0)
        owned_unit = unit_week_owner.get(week)
        if owned_unit is not None and planned_unit != owned_unit:
            errors.append(
                f"{prefix}: semana {week} apunta a unidad {planned_unit} en el cronograma y a {owned_unit} en la unidad"
            )

    course_hours = int(course.get("total_workload_hours", 0) or 0)
    unit_hours = sum(int(unit.get("estimated_hours", 0) or 0) for unit in units)
    if abs(course_hours - unit_hours) > MAX_HOUR_MISMATCH:
        errors.append(
            f"{prefix}: horas del curso ({course_hours}) y de las unidades ({unit_hours}) difieren en más de {MAX_HOUR_MISMATCH}"
        )
    elif course_hours != unit_hours:
        warnings.append(f"{prefix}: horas declaradas curso={course_hours}, unidades={unit_hours}")

    assessment = course.get("assessment_plan", [])
    assessment_total = sum(float(item.get("weight_percent", 0) or 0) for item in assessment if isinstance(item, dict))
    if abs(assessment_total - 100.0) > 1e-9:
        errors.append(f"{prefix}: evaluación suma {assessment_total:g} %, no 100 %")
    rubric = course.get("final_project", {}).get("rubric", [])
    rubric_total = sum(float(item.get("weight_percent", 0) or 0) for item in rubric if isinstance(item, dict))
    if abs(rubric_total - 100.0) > 1e-9:
        errors.append(f"{prefix}: rúbrica suma {rubric_total:g} %, no 100 %")

    resources = course.get("core_resources", [])
    resource_urls = [str(item.get("url", "")) for item in resources if isinstance(item, dict)]
    resource_domains = {source_domain(url) for url in resource_urls if source_domain(url)}
    if len(resource_domains) < MIN_COURSE_RESOURCE_DOMAINS:
        errors.append(f"{prefix}: bibliografía central usa solo {len(resource_domains)} dominios")
    for url in resource_urls:
        if is_generic_source(url):
            warnings.append(f"{prefix}: recurso central con URL genérica: {url}")

    all_source_urls: list[str] = []
    total_words = 0
    equation_count = 0
    for unit in units:
        number = int(unit["unit"])
        unit_prefix = f"{prefix}/unit-{number:02d}"
        sources = unit.get("sources", [])
        urls = [str(item.get("url", "")) for item in sources if isinstance(item, dict)]
        domains = {source_domain(url) for url in urls if source_domain(url)}
        if len(domains) < MIN_SOURCE_DOMAINS_PER_UNIT:
            errors.append(f"{unit_prefix}: fuentes concentradas en {len(domains)} dominio(s)")
        if len(urls) != len(set(urls)):
            errors.append(f"{unit_prefix}: contiene fuentes duplicadas")
        for url in urls:
            if is_generic_source(url):
                warnings.append(f"{unit_prefix}: fuente con URL genérica: {url}")
        all_source_urls.extend(urls)

        theory = unit.get("theory_sections", [])
        equation_count += sum(len(section.get("equations", [])) for section in theory if isinstance(section, dict))
        total_words += len(WORD_RE.findall(json.dumps(unit, ensure_ascii=False)))

        glossary_terms = [normalized(str(item.get("term", ""))) for item in unit.get("glossary", [])]
        if len(glossary_terms) != len(set(glossary_terms)):
            errors.append(f"{unit_prefix}: glosario con términos duplicados")
        questions = [normalized(str(item.get("question", ""))) for item in unit.get("self_assessment", [])]
        if len(questions) != len(set(questions)):
            errors.append(f"{unit_prefix}: autoevaluación con preguntas duplicadas")

    if equation_count == 0:
        errors.append(f"{prefix}: curso cuantitativo sin ecuaciones estructuradas para MathJax")
    repeated_source_count = sum(count - 1 for count in Counter(all_source_urls).values() if count > 1)
    if repeated_source_count > len(units) * 3:
        warnings.append(f"{prefix}: bibliografía muy repetitiva entre unidades ({repeated_source_count} repeticiones)")

    all_paragraphs.extend(paragraph_records(subject_id, units))
    metrics[subject_id] = {
        "units": len(units),
        "words": total_words,
        "course_hours": course_hours,
        "unit_hours": unit_hours,
        "equations": equation_count,
        "source_domains": len({source_domain(url) for url in all_source_urls if source_domain(url)}),
    }


def audit_duplicate_paragraphs(records: list[tuple[str, str]], errors: list[str]) -> None:
    by_text: dict[str, list[str]] = defaultdict(list)
    for label, paragraph in records:
        by_text[normalized(paragraph)].append(label)
    for labels in by_text.values():
        unique_labels = sorted(set(labels))
        if len(unique_labels) > 1:
            errors.append("PÁRRAFO duplicado en " + ", ".join(unique_labels))


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita coherencia y calidad transversal de cursos semestrales.")
    parser.add_argument("--strict", action="store_true", help="Devuelve error si existen hallazgos críticos.")
    parser.add_argument("--json-output", help="Ruta opcional para guardar el informe JSON.")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    metrics: dict[str, Any] = {}
    all_paragraphs: list[tuple[str, str]] = []

    course_paths = sorted(COURSE_ROOT.glob("*.json"))
    if not course_paths:
        print("No hay cursos semestrales para auditar.")
        return 1 if args.strict else 0

    for course_path in course_paths:
        try:
            audit_course(course_path, errors, warnings, metrics, all_paragraphs)
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
            errors.append(f"{course_path.stem}: auditoría interrumpida: {error}")

    audit_duplicate_paragraphs(all_paragraphs, errors)
    audit_public_hygiene(errors)

    report = {
        "courses": metrics,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "courses_audited": len(course_paths),
            "critical_findings": len(errors),
            "warnings": len(warnings),
        },
    }
    if args.json_output:
        output = ROOT / args.json_output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("AUDITORÍA DEL PORTAFOLIO SEMESTRAL")
    for subject_id, data in sorted(metrics.items()):
        print(
            f"- {subject_id}: unidades={data['units']} · palabras={data['words']} · "
            f"horas={data['unit_hours']}/{data['course_hours']} · ecuaciones={data['equations']} · "
            f"dominios={data['source_domains']}"
        )
    for warning in warnings:
        print(f"ADVERTENCIA: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Resumen: {len(course_paths)} cursos · {len(errors)} errores · {len(warnings)} advertencias")
    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
