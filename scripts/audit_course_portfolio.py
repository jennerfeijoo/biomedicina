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
REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"
ASSET_ROOT = ROOT / "assets" / "js"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)
SPACE_RE = re.compile(r"\s+")
COURSE_TIME_KEYS = {
    "estimated_workload", "duration_weeks", "weekly_hours",
    "total_workload_hours", "semester_plan",
}
UNIT_TIME_KEYS = {"estimated_hours", "weeks"}
FORBIDDEN_PUBLIC_PHRASES = (
    "contenido desarrollado", "unidades desarrolladas", "ejemplo desarrollado",
    "en revisión académica", "pendiente de ampliación", "generado automáticamente",
)
GENERIC_SOURCE_PATHS = {"", "/", "/books/", "/books", "/search/", "/search"}
MIN_SOURCE_ORIGINS_PER_UNIT = 3
MIN_COURSE_RESOURCE_DOMAINS = 4
MIN_DUPLICATE_PARAGRAPH_CHARS = 180


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("la raíz debe ser un objeto")
    return data


def normalized(text: str) -> str:
    return SPACE_RE.sub(" ", text.strip().casefold())


def source_domain(url: str) -> str:
    return urlparse(url).netloc.casefold().removeprefix("www.")


def is_generic_source(url: str) -> bool:
    return bool(url) and urlparse(url).path.casefold() in GENERIC_SOURCE_PATHS


def normalize_doi(value: str) -> str:
    doi = value.strip().casefold()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
    return doi.strip()


def bibliographic_identity(source: dict[str, Any]) -> str:
    """Devuelve la identidad más específica disponible para detectar duplicados reales."""
    doi = normalize_doi(str(source.get("doi") or ""))
    if doi:
        return "doi:" + doi
    pmid = str(source.get("pmid") or "").strip().casefold()
    if pmid:
        return "pmid:" + pmid
    isbn = re.sub(r"[^0-9xX]", "", str(source.get("isbn") or ""))
    if isbn:
        return "isbn:" + isbn.casefold()
    url = str(source.get("url") or "").strip().casefold().rstrip("/")
    if url:
        return "url:" + url
    registry = str(source.get("registry_id") or source.get("id") or "").strip().casefold()
    if registry:
        return "registry:" + registry
    citation = normalized(str(source.get("citation") or source.get("title") or ""))
    return "citation:" + citation if citation else ""


def bibliographic_origin(source: dict[str, Any]) -> str:
    doi = normalize_doi(str(source.get("doi") or ""))
    if doi:
        return "doi-prefix:" + doi.split("/", 1)[0]
    url = str(source.get("url") or "").strip()
    domain = source_domain(url)
    if domain and domain != "doi.org":
        return "domain:" + domain
    organization = normalized(str(source.get("organization") or ""))
    if organization:
        return "organization:" + organization
    if str(source.get("pmid") or "").strip():
        return "index:pubmed"
    if str(source.get("isbn") or "").strip():
        return "format:isbn"
    registry = str(source.get("registry_id") or "").strip().casefold()
    return "registry:" + registry.split("-", 1)[0] if registry else ""


def unit_paths(subject_id: str) -> list[Path]:
    return sorted((UNIT_ROOT / subject_id).glob("unit-*.json"))


def is_exact_redevelopment_mirror(subject_id: str, unit_path: Path) -> bool:
    source = REDEVELOPMENT_ROOT / subject_id / "units" / unit_path.name
    return source.exists() and source.read_bytes() == unit_path.read_bytes()


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


def audit_unit_sources(
    subject_id: str,
    unit_path: Path,
    unit: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> tuple[list[str], set[str]]:
    prefix = f"{subject_id}/unit-{int(unit['unit']):02d}"
    sources = [source for source in unit.get("sources", []) if isinstance(source, dict)]
    identities = [bibliographic_identity(source) for source in sources]
    missing = sum(not identity for identity in identities)
    if missing:
        errors.append(f"{prefix}: {missing} fuente(s) sin identidad bibliográfica estable")
    stable = [identity for identity in identities if identity]
    duplicates = sum(count - 1 for count in Counter(stable).values() if count > 1)
    if duplicates:
        errors.append(f"{prefix}: contiene {duplicates} referencia(s) bibliográfica(s) duplicada(s)")

    origins = {origin for source in sources if (origin := bibliographic_origin(source))}
    if len(origins) < MIN_SOURCE_ORIGINS_PER_UNIT:
        message = f"{prefix}: bibliografía concentrada en {len(origins)} origen(es)"
        if is_exact_redevelopment_mirror(subject_id, unit_path):
            warnings.append(message + "; revisar diversidad editorial en la próxima revisión disciplinar")
        else:
            errors.append(message)
    for source in sources:
        url = str(source.get("url") or "").strip()
        if url and is_generic_source(url):
            warnings.append(f"{prefix}: fuente con URL genérica: {url}")
    return stable, origins


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

    if course.get("subject_id") != subject_id:
        errors.append(f"{subject_id}: subject_id del curso no coincide con el archivo")
    if course.get("schema_version") != "2.0":
        errors.append(f"{subject_id}: arquitectura sin schema_version 2.0")
    if course.get("status") != "review":
        errors.append(f"{subject_id}: status interno debe permanecer en review hasta revisión humana externa")
    if not units:
        errors.append(f"{subject_id}: no tiene unidades")
        return

    numbers = [int(unit.get("unit", 0) or 0) for unit in units]
    if numbers != list(range(1, len(units) + 1)):
        errors.append(f"{subject_id}: numeración de unidades no consecutiva: {numbers}")
    if any(unit.get("subject_id") != subject_id for unit in units):
        errors.append(f"{subject_id}: alguna unidad tiene subject_id inconsistente")
    if any(unit.get("schema_version") != "2.0" for unit in units):
        errors.append(f"{subject_id}: todas las unidades deben usar schema_version 2.0")
    if any(unit.get("status") != "review" for unit in units):
        errors.append(f"{subject_id}: todas las unidades deben conservar status review")

    forbidden = sorted(COURSE_TIME_KEYS & course.keys())
    if forbidden:
        errors.append(f"{subject_id}: conserva metadatos temporales: {', '.join(forbidden)}")

    assessment_total = sum(
        float(item.get("weight_percent", 0) or 0)
        for item in course.get("assessment_plan", []) if isinstance(item, dict)
    )
    if abs(assessment_total - 100.0) > 1e-9:
        errors.append(f"{subject_id}: evaluación suma {assessment_total:g} %, no 100 %")
    rubric_total = sum(
        float(item.get("weight_percent", 0) or 0)
        for item in course.get("final_project", {}).get("rubric", []) if isinstance(item, dict)
    )
    if abs(rubric_total - 100.0) > 1e-9:
        errors.append(f"{subject_id}: rúbrica suma {rubric_total:g} %, no 100 %")

    resource_urls = [
        str(item.get("url", "")) for item in course.get("core_resources", []) if isinstance(item, dict)
    ]
    resource_domains = {source_domain(url) for url in resource_urls if source_domain(url)}
    if len(resource_domains) < MIN_COURSE_RESOURCE_DOMAINS:
        errors.append(f"{subject_id}: bibliografía central usa solo {len(resource_domains)} dominios")
    for url in resource_urls:
        if is_generic_source(url):
            warnings.append(f"{subject_id}: recurso central con URL genérica: {url}")

    all_identities: list[str] = []
    all_origins: set[str] = set()
    total_words = 0
    equation_count = 0
    for unit_path, unit in zip(paths, units, strict=True):
        unit_prefix = f"{subject_id}/unit-{int(unit['unit']):02d}"
        forbidden = sorted(UNIT_TIME_KEYS & unit.keys())
        if forbidden:
            errors.append(f"{unit_prefix}: conserva metadatos temporales: {', '.join(forbidden)}")
        identities, origins = audit_unit_sources(subject_id, unit_path, unit, errors, warnings)
        all_identities.extend(identities)
        all_origins.update(origins)
        theory = unit.get("theory_sections", [])
        equation_count += sum(
            len(section.get("equations", [])) for section in theory if isinstance(section, dict)
        )
        total_words += len(WORD_RE.findall(json.dumps(unit, ensure_ascii=False)))

        glossary = [normalized(str(item.get("term", ""))) for item in unit.get("glossary", [])]
        if len(glossary) != len(set(glossary)):
            errors.append(f"{unit_prefix}: glosario con términos duplicados")
        questions = [
            normalized(str(item.get("question", ""))) for item in unit.get("self_assessment", [])
        ]
        if len(questions) != len(set(questions)):
            errors.append(f"{unit_prefix}: autoevaluación con preguntas duplicadas")

    if equation_count == 0:
        errors.append(f"{subject_id}: curso cuantitativo sin ecuaciones estructuradas para MathJax")
    repeated = sum(count - 1 for count in Counter(all_identities).values() if count > 1)
    if repeated > len(units) * 3:
        warnings.append(f"{subject_id}: bibliografía muy repetitiva entre unidades ({repeated} repeticiones)")

    all_paragraphs.extend(paragraph_records(subject_id, units))
    metrics[subject_id] = {
        "units": len(units),
        "words": total_words,
        "equations": equation_count,
        "source_origins": len(all_origins),
        "bibliographic_identities": len(set(all_identities)),
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
    parser = argparse.ArgumentParser(description="Audita coherencia y calidad transversal del portafolio.")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json-output")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    metrics: dict[str, Any] = {}
    paragraphs: list[tuple[str, str]] = []
    course_paths = sorted(COURSE_ROOT.glob("*.json"))
    if not course_paths:
        print("No hay cursos generados para auditar.")
        return 1 if args.strict else 0

    for course_path in course_paths:
        try:
            audit_course(course_path, errors, warnings, metrics, paragraphs)
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
            errors.append(f"{course_path.stem}: auditoría interrumpida: {error}")
    audit_duplicate_paragraphs(paragraphs, errors)
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

    print("AUDITORÍA DEL PORTAFOLIO DE CURSOS")
    for subject_id, data in sorted(metrics.items()):
        print(
            f"- {subject_id}: unidades={data['units']} · palabras={data['words']} · "
            f"ecuaciones={data['equations']} · orígenes={data['source_origins']} · "
            f"referencias={data['bibliographic_identities']}"
        )
    for warning in warnings:
        print(f"ADVERTENCIA: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Resumen: {len(course_paths)} cursos · {len(errors)} errores · {len(warnings)} advertencias")
    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
