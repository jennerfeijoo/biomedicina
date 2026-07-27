#!/usr/bin/env python3
"""Audit bibliography for a course redevelopment package.

The audit resolves unit-local references against canonical registry records by
``registry_id``, canonical ``id``, aliases, DOI, PMID or URL. It distinguishes
expected repeated uses of one canonical source from unresolved identifier
collisions. It never edits bibliography records and makes no network requests.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"
REGISTRY_ROOT = ROOT / "data" / "source_registry"
DOI_PREFIX_RE = re.compile(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", re.IGNORECASE)
PMID_RE = re.compile(r"\d+")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
SPACE_RE = re.compile(r"\s+")
REQUIRED_FIELDS = ("title", "authors_or_organization", "type", "verification_status")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {path}: {exc}") from exc


def normalize_doi(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    return DOI_PREFIX_RE.sub("", text).strip().lower().rstrip("./") or None


def normalize_pmid(value: Any) -> str | None:
    text = str(value or "").strip()
    return text if PMID_RE.fullmatch(text) else None


def normalize_url(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        split = urlsplit(text)
    except ValueError:
        return text.rstrip("/")
    if not split.scheme or not split.netloc:
        return text.rstrip("/")
    path = split.path.rstrip("/") or "/"
    query = urlencode(sorted(parse_qsl(split.query, keep_blank_values=True)), doseq=True)
    return urlunsplit((split.scheme.lower(), split.netloc.lower(), path, query, ""))


def normalize_title(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return SPACE_RE.sub(" ", NON_ALNUM_RE.sub(" ", text)).strip()


def identifiers(record: dict[str, Any]) -> list[str]:
    values: list[str] = []
    doi = normalize_doi(record.get("doi"))
    pmid = normalize_pmid(record.get("pmid"))
    url = normalize_url(record.get("url"))
    if doi:
        values.append(f"doi:{doi}")
    if pmid:
        values.append(f"pmid:{pmid}")
    if url:
        values.append(f"url:{url}")
    return values


def registry_paths(subject_id: str) -> list[Path]:
    paths = [REGISTRY_ROOT / f"{subject_id}.json"]
    paths.extend(sorted(REGISTRY_ROOT.glob(f"{subject_id}-*.json")))
    return list(dict.fromkeys(path for path in paths if path.exists()))


def load_registry_records(subject_id: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in registry_paths(subject_id):
        data = load_json(path)
        sources = data.get("sources", [])
        if not isinstance(sources, list):
            raise ValueError(f"{path}: sources debe ser una lista")
        for index, source in enumerate(sources, start=1):
            if not isinstance(source, dict):
                continue
            records.append(
                {
                    "origin_kind": "registry",
                    "origin": str(path.relative_to(ROOT)),
                    "unit": None,
                    "source_index": index,
                    "record": source,
                }
            )
    return records


def load_unit_records(subject_id: str) -> list[dict[str, Any]]:
    units_dir = REDEVELOPMENT_ROOT / subject_id / "units"
    if not units_dir.exists():
        raise FileNotFoundError(f"No existe el directorio de unidades: {units_dir}")
    records: list[dict[str, Any]] = []
    for path in sorted(units_dir.glob("unit-*.json")):
        unit = load_json(path)
        sources = unit.get("sources", [])
        if not isinstance(sources, list):
            raise ValueError(f"{path}: sources debe ser una lista")
        for index, source in enumerate(sources, start=1):
            if not isinstance(source, dict):
                continue
            records.append(
                {
                    "origin_kind": "unit",
                    "origin": str(path.relative_to(ROOT)),
                    "unit": unit.get("unit"),
                    "source_index": index,
                    "record": source,
                }
            )
    return records


def build_registry_index(
    registry_records: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]], list[str]]:
    by_id: dict[str, dict[str, Any]] = {}
    by_identifier: dict[str, set[str]] = defaultdict(set)
    errors: list[str] = []

    for raw in registry_records:
        record = raw["record"]
        canonical_id = str(record.get("id") or "").strip()
        if not canonical_id:
            errors.append(f"{raw['origin']}: fuente {raw['source_index']} sin id canónico")
            continue
        names = [canonical_id]
        aliases = record.get("aliases", [])
        if isinstance(aliases, list):
            names.extend(str(alias).strip() for alias in aliases if str(alias).strip())
        for name in names:
            previous = by_id.get(name)
            if previous and previous["record"].get("id") != canonical_id:
                errors.append(f"alias o id duplicado `{name}` en registros centrales")
            else:
                by_id[name] = raw
        for identifier in identifiers(record):
            by_identifier[identifier].add(canonical_id)
    return by_id, by_identifier, errors


def resolve_canonical(
    record: dict[str, Any],
    by_id: dict[str, dict[str, Any]],
    by_identifier: dict[str, set[str]],
) -> tuple[str | None, dict[str, Any] | None, list[str]]:
    candidates: set[str] = set()
    reference_id = str(record.get("registry_id") or record.get("id") or "").strip()
    if reference_id and reference_id in by_id:
        candidates.add(str(by_id[reference_id]["record"]["id"]))
    for identifier in identifiers(record):
        candidates.update(by_identifier.get(identifier, set()))
    if len(candidates) == 1:
        canonical_id = next(iter(candidates))
        return canonical_id, by_id[canonical_id]["record"], []
    if len(candidates) > 1:
        return None, None, sorted(candidates)
    return None, None, []


def first_value(local: dict[str, Any], canonical: dict[str, Any] | None, *keys: str) -> Any:
    for key in keys:
        value = local.get(key)
        if value not in (None, "", []):
            return value
    if canonical:
        for key in keys:
            value = canonical.get(key)
            if value not in (None, "", []):
                return value
    return None


def build_entry(
    raw: dict[str, Any],
    by_id: dict[str, dict[str, Any]],
    by_identifier: dict[str, set[str]],
) -> dict[str, Any]:
    local = raw["record"]
    if raw["origin_kind"] == "registry":
        canonical_id = str(local.get("id") or "").strip() or None
        canonical = local
        ambiguous: list[str] = []
    else:
        canonical_id, canonical, ambiguous = resolve_canonical(local, by_id, by_identifier)

    title = str(first_value(local, canonical, "title") or "").strip()
    authors = first_value(local, canonical, "authors_or_organization", "organization")
    source_type = first_value(local, canonical, "type")
    verification = first_value(local, canonical, "verification_status")
    year = first_value(local, canonical, "year")

    merged_identifiers = sorted(set(identifiers(local) + identifiers(canonical or {})))
    doi = next((item[4:] for item in merged_identifiers if item.startswith("doi:")), None)
    pmid = next((item[5:] for item in merged_identifiers if item.startswith("pmid:")), None)
    url = next((item[4:] for item in merged_identifiers if item.startswith("url:")), None)

    missing_fields: list[str] = []
    values = {
        "title": title,
        "authors_or_organization": authors,
        "type": source_type,
        "verification_status": verification,
    }
    for field in REQUIRED_FIELDS:
        if not str(values[field] or "").strip():
            missing_fields.append(field)
    if not merged_identifiers:
        missing_fields.append("stable_identifier")

    return {
        "origin_kind": raw["origin_kind"],
        "origin": raw["origin"],
        "unit": raw["unit"],
        "source_index": raw["source_index"],
        "local_id": local.get("registry_id") or local.get("id"),
        "canonical_id": canonical_id,
        "ambiguous_canonical_ids": ambiguous,
        "title": title,
        "normalized_title": normalize_title(title),
        "authors_or_organization": authors,
        "year": year,
        "type": source_type,
        "verification_status": verification,
        "doi": doi,
        "pmid": pmid,
        "url": url,
        "identifiers": merged_identifiers,
        "missing_fields": missing_fields,
    }


def classify_identifier_groups(entries: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        for identifier in entry["identifiers"]:
            groups[identifier].append(entry)

    resolved: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for identifier, occurrences in sorted(groups.items()):
        if len(occurrences) < 2:
            continue
        canonical_ids = {entry["canonical_id"] for entry in occurrences if entry["canonical_id"]}
        group = {"identifier": identifier, "occurrences": occurrences}
        if len(canonical_ids) == 1 and all(entry["canonical_id"] in canonical_ids for entry in occurrences):
            group["canonical_id"] = next(iter(canonical_ids))
            resolved.append(group)
        else:
            group["canonical_ids"] = sorted(canonical_ids)
            unresolved.append(group)
    return resolved, unresolved


def possible_title_duplicates(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        if entry["normalized_title"]:
            groups[entry["normalized_title"]].append(entry)
    output: list[dict[str, Any]] = []
    for title, occurrences in sorted(groups.items()):
        if len(occurrences) < 2:
            continue
        canonical_ids = {entry["canonical_id"] for entry in occurrences if entry["canonical_id"]}
        if len(canonical_ids) == 1 and all(entry["canonical_id"] in canonical_ids for entry in occurrences):
            continue
        shared_identifiers = set(occurrences[0]["identifiers"])
        for entry in occurrences[1:]:
            shared_identifiers.intersection_update(entry["identifiers"])
        if shared_identifiers:
            continue
        output.append(
            {
                "normalized_title": title,
                "occurrences": occurrences,
                "review_reason": "same_normalized_title_without_shared_canonical_reference",
            }
        )
    return output


def audit(subject_id: str) -> dict[str, Any]:
    registry_records = load_registry_records(subject_id)
    by_id, by_identifier, registry_errors = build_registry_index(registry_records)
    if registry_errors:
        raise ValueError("; ".join(registry_errors))
    raw_records = registry_records + load_unit_records(subject_id)
    entries = [build_entry(raw, by_id, by_identifier) for raw in raw_records]

    resolved_groups, unresolved_groups = classify_identifier_groups(entries)
    title_duplicates = possible_title_duplicates(entries)
    incomplete = [entry for entry in entries if entry["missing_fields"]]
    ambiguous = [entry for entry in entries if entry["ambiguous_canonical_ids"]]
    unit_entries = [entry for entry in entries if entry["origin_kind"] == "unit"]
    registry_entries = [entry for entry in entries if entry["origin_kind"] == "registry"]

    unit_counts: dict[str, int] = defaultdict(int)
    registry_counts: dict[str, int] = defaultdict(int)
    for entry in unit_entries:
        unit_counts[str(entry["unit"])] += 1
    for entry in registry_entries:
        registry_counts[entry["origin"]] += 1

    unique_identifiers = {identifier for entry in entries for identifier in entry["identifiers"]}
    summary = {
        "subject_id": subject_id,
        "total_occurrences": len(entries),
        "unit_occurrences": len(unit_entries),
        "registry_occurrences": len(registry_entries),
        "canonical_sources": len({entry["canonical_id"] for entry in registry_entries if entry["canonical_id"]}),
        "unit_occurrences_resolved_to_registry": sum(bool(entry["canonical_id"]) for entry in unit_entries),
        "unit_occurrences_without_registry_match": sum(not entry["canonical_id"] for entry in unit_entries),
        "unique_exact_identifiers": len(unique_identifiers),
        "resolved_reference_groups": len(resolved_groups),
        "unresolved_exact_duplicate_groups": len(unresolved_groups),
        "possible_title_duplicate_groups": len(title_duplicates),
        "ambiguous_reference_occurrences": len(ambiguous),
        "incomplete_occurrences_after_resolution": len(incomplete),
        "units_with_sources": len(unit_counts),
        "registries_scanned": len(registry_counts),
    }
    return {
        "summary": summary,
        "unit_counts": dict(sorted(unit_counts.items(), key=lambda item: int(item[0]))),
        "registry_counts": dict(sorted(registry_counts.items())),
        "resolved_reference_groups": resolved_groups,
        "unresolved_exact_duplicates": unresolved_groups,
        "possible_title_duplicates": title_duplicates,
        "ambiguous_references": ambiguous,
        "incomplete_entries": incomplete,
    }


def occurrence_label(entry: dict[str, Any]) -> str:
    unit = f"; unidad {entry['unit']}" if entry["unit"] is not None else ""
    canonical = f"; canónica `{entry['canonical_id']}`" if entry["canonical_id"] else ""
    return f"`{entry['origin']}`{unit}; fuente {entry['source_index']}{canonical}"


def render_groups(lines: list[str], groups: Iterable[dict[str, Any]]) -> None:
    for group in groups:
        lines.extend([f"### `{group['identifier']}`", ""])
        for entry in group["occurrences"]:
            lines.append(f"- {entry['title'] or '(sin título)'} — {occurrence_label(entry)}")
        lines.append("")


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        f"# Auditoría bibliográfica — {summary['subject_id']}",
        "",
        "Las repeticiones resueltas representan usos de una misma fuente canónica. Solo los grupos no resueltos requieren deduplicación manual.",
        "",
        "## Resumen",
        "",
    ]
    labels = [
        ("Ocurrencias totales", "total_occurrences"),
        ("Ocurrencias en unidades", "unit_occurrences"),
        ("Ocurrencias en registros", "registry_occurrences"),
        ("Fuentes canónicas", "canonical_sources"),
        ("Usos de unidad resueltos contra registro", "unit_occurrences_resolved_to_registry"),
        ("Usos de unidad aún sin registro", "unit_occurrences_without_registry_match"),
        ("Identificadores exactos únicos", "unique_exact_identifiers"),
        ("Grupos repetidos resueltos", "resolved_reference_groups"),
        ("Grupos duplicados no resueltos", "unresolved_exact_duplicate_groups"),
        ("Posibles duplicados por título", "possible_title_duplicate_groups"),
        ("Referencias ambiguas", "ambiguous_reference_occurrences"),
        ("Ocurrencias incompletas tras resolución", "incomplete_occurrences_after_resolution"),
    ]
    lines.extend(f"- {label}: {summary[key]}" for label, key in labels)
    lines.extend(["", "## Fuentes por unidad", "", "| Unidad | Ocurrencias |", "|---:|---:|"])
    lines.extend(f"| {unit} | {count} |" for unit, count in report["unit_counts"].items())
    lines.extend(["", "## Registros escaneados", ""])
    lines.extend(f"- `{origin}`: {count} fuentes" for origin, count in report["registry_counts"].items())

    lines.extend(["", "## Repeticiones resueltas por referencia canónica", ""])
    if not report["resolved_reference_groups"]:
        lines.append("No se detectaron usos repetidos resueltos.")
    render_groups(lines, report["resolved_reference_groups"])

    lines.extend(["## Duplicados exactos no resueltos", ""])
    if not report["unresolved_exact_duplicates"]:
        lines.append("No se detectaron colisiones de identificador pendientes.")
    render_groups(lines, report["unresolved_exact_duplicates"])

    lines.extend(["", "## Posibles duplicados por título", ""])
    if not report["possible_title_duplicates"]:
        lines.append("No se detectaron coincidencias de título pendientes.")
    for group in report["possible_title_duplicates"]:
        lines.extend([f"### {group['normalized_title']}", ""])
        for entry in group["occurrences"]:
            lines.append(f"- {entry['title']} — {occurrence_label(entry)}")
        lines.append("")

    lines.extend(["## Referencias ambiguas", ""])
    if not report["ambiguous_references"]:
        lines.append("No se detectaron referencias compatibles con más de una fuente canónica.")
    for entry in report["ambiguous_references"]:
        candidates = ", ".join(entry["ambiguous_canonical_ids"])
        lines.append(f"- {entry['title'] or '(sin título)'} — {occurrence_label(entry)}; candidatas: {candidates}")

    lines.extend(["", "## Metadatos incompletos", ""])
    if not report["incomplete_entries"]:
        lines.append("No se detectaron campos obligatorios ausentes después de resolver los registros canónicos.")
    for entry in report["incomplete_entries"]:
        lines.append(
            f"- {entry['title'] or '(sin título)'} — {occurrence_label(entry)}; faltan: {', '.join(entry['missing_fields'])}"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", default="biologia-desarrollo")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--fail-on-exact-duplicates", action="store_true", help="Falla solo por duplicados exactos no resueltos.")
    parser.add_argument("--fail-on-incomplete", action="store_true")
    parser.add_argument("--fail-on-ambiguous", action="store_true")
    args = parser.parse_args()

    try:
        report = audit(args.subject_id)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(report), encoding="utf-8")

    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    errors: list[str] = []
    if args.fail_on_exact_duplicates and report["unresolved_exact_duplicates"]:
        errors.append(f"hay {len(report['unresolved_exact_duplicates'])} grupos duplicados no resueltos")
    if args.fail_on_incomplete and report["incomplete_entries"]:
        errors.append(f"hay {len(report['incomplete_entries'])} ocurrencias incompletas")
    if args.fail_on_ambiguous and report["ambiguous_references"]:
        errors.append(f"hay {len(report['ambiguous_references'])} referencias ambiguas")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
