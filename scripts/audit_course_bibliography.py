#!/usr/bin/env python3
"""Audit and inventory bibliography for a course redevelopment package.

The audit reads unit-local ``sources`` arrays and one or more central source
registries. It normalizes DOI, PMID and URL identifiers, reports exact duplicate
identifier groups, flags possible title duplicates for manual review, and
identifies incomplete metadata. It never merges records automatically and does
not make network requests.
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
DEFAULT_REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"
DEFAULT_REGISTRY_ROOT = ROOT / "data" / "source_registry"

DOI_PREFIX_RE = re.compile(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", re.IGNORECASE)
PMID_RE = re.compile(r"\d+")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
SPACE_RE = re.compile(r"\s+")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {path}: {exc}") from exc


def normalize_doi(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    text = DOI_PREFIX_RE.sub("", text).strip().lower()
    return text.rstrip("./") or None


def normalize_pmid(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    match = PMID_RE.fullmatch(text)
    return match.group(0) if match else None


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
    scheme = split.scheme.lower()
    host = split.netloc.lower()
    path = split.path.rstrip("/") or "/"
    query_pairs = sorted(parse_qsl(split.query, keep_blank_values=True))
    query = urlencode(query_pairs, doseq=True)
    return urlunsplit((scheme, host, path, query, ""))


def normalize_title(value: Any) -> str:
    text = str(value or "").strip().lower()
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = NON_ALNUM_RE.sub(" ", text)
    return SPACE_RE.sub(" ", text).strip()


def iter_source_records(subject_id: str) -> Iterable[dict[str, Any]]:
    package = DEFAULT_REDEVELOPMENT_ROOT / subject_id
    units_dir = package / "units"
    if not units_dir.exists():
        raise FileNotFoundError(f"No existe el directorio de unidades: {units_dir}")

    for unit_path in sorted(units_dir.glob("unit-*.json")):
        unit = load_json(unit_path)
        unit_number = unit.get("unit")
        sources = unit.get("sources", [])
        if not isinstance(sources, list):
            raise ValueError(f"{unit_path}: sources debe ser una lista")
        for index, source in enumerate(sources, start=1):
            if not isinstance(source, dict):
                continue
            yield {
                "origin_kind": "unit",
                "origin": str(unit_path.relative_to(ROOT)),
                "unit": unit_number,
                "source_index": index,
                "record": source,
            }

    registry_paths = [DEFAULT_REGISTRY_ROOT / f"{subject_id}.json"]
    registry_paths.extend(sorted(DEFAULT_REGISTRY_ROOT.glob(f"{subject_id}-*.json")))
    seen_paths: set[Path] = set()
    for registry_path in registry_paths:
        if registry_path in seen_paths or not registry_path.exists():
            continue
        seen_paths.add(registry_path)
        registry = load_json(registry_path)
        sources = registry.get("sources", [])
        if not isinstance(sources, list):
            raise ValueError(f"{registry_path}: sources debe ser una lista")
        for index, source in enumerate(sources, start=1):
            if not isinstance(source, dict):
                continue
            yield {
                "origin_kind": "registry",
                "origin": str(registry_path.relative_to(ROOT)),
                "unit": None,
                "source_index": index,
                "record": source,
            }


def build_entry(raw: dict[str, Any]) -> dict[str, Any]:
    record = raw["record"]
    title = str(record.get("title") or "").strip()
    doi = normalize_doi(record.get("doi"))
    pmid = normalize_pmid(record.get("pmid"))
    url = normalize_url(record.get("url"))
    identifiers: list[str] = []
    if doi:
        identifiers.append(f"doi:{doi}")
    if pmid:
        identifiers.append(f"pmid:{pmid}")
    if url:
        identifiers.append(f"url:{url}")

    missing_fields: list[str] = []
    for field in ("title", "authors_or_organization", "type", "verification_status"):
        if not str(record.get(field) or "").strip():
            missing_fields.append(field)
    if not identifiers:
        missing_fields.append("stable_identifier")

    return {
        "origin_kind": raw["origin_kind"],
        "origin": raw["origin"],
        "unit": raw["unit"],
        "source_index": raw["source_index"],
        "id": record.get("id"),
        "title": title,
        "normalized_title": normalize_title(title),
        "authors_or_organization": record.get("authors_or_organization"),
        "year": record.get("year"),
        "type": record.get("type"),
        "verification_status": record.get("verification_status"),
        "doi": doi,
        "pmid": pmid,
        "url": url,
        "identifiers": identifiers,
        "missing_fields": missing_fields,
    }


def audit(subject_id: str) -> dict[str, Any]:
    entries = [build_entry(raw) for raw in iter_source_records(subject_id)]
    identifier_groups: dict[str, list[int]] = defaultdict(list)
    title_groups: dict[str, list[int]] = defaultdict(list)

    for index, entry in enumerate(entries):
        for identifier in entry["identifiers"]:
            identifier_groups[identifier].append(index)
        title = entry["normalized_title"]
        if title:
            title_groups[title].append(index)

    exact_duplicates = []
    for identifier, indices in sorted(identifier_groups.items()):
        if len(indices) < 2:
            continue
        exact_duplicates.append(
            {
                "identifier": identifier,
                "occurrences": [entries[index] for index in indices],
            }
        )

    possible_title_duplicates = []
    for title, indices in sorted(title_groups.items()):
        if len(indices) < 2:
            continue
        group_entries = [entries[index] for index in indices]
        group_identifiers = {
            identifier
            for entry in group_entries
            for identifier in entry["identifiers"]
        }
        if any(
            duplicate["identifier"] in group_identifiers
            for duplicate in exact_duplicates
        ):
            continue
        possible_title_duplicates.append(
            {
                "normalized_title": title,
                "occurrences": group_entries,
                "review_reason": "same_normalized_title_without_shared_identifier",
            }
        )

    incomplete_entries = [entry for entry in entries if entry["missing_fields"]]
    unit_counts: dict[str, int] = defaultdict(int)
    registry_counts: dict[str, int] = defaultdict(int)
    for entry in entries:
        if entry["origin_kind"] == "unit":
            unit_counts[str(entry["unit"])] += 1
        else:
            registry_counts[entry["origin"]] += 1

    summary = {
        "subject_id": subject_id,
        "total_occurrences": len(entries),
        "unit_occurrences": sum(unit_counts.values()),
        "registry_occurrences": sum(registry_counts.values()),
        "unique_exact_identifiers": len(identifier_groups),
        "exact_duplicate_groups": len(exact_duplicates),
        "possible_title_duplicate_groups": len(possible_title_duplicates),
        "incomplete_occurrences": len(incomplete_entries),
        "units_with_sources": len(unit_counts),
        "registries_scanned": len(registry_counts),
    }
    return {
        "summary": summary,
        "unit_counts": dict(sorted(unit_counts.items(), key=lambda item: int(item[0]))),
        "registry_counts": dict(sorted(registry_counts.items())),
        "exact_duplicates": exact_duplicates,
        "possible_title_duplicates": possible_title_duplicates,
        "incomplete_entries": incomplete_entries,
    }


def occurrence_label(entry: dict[str, Any]) -> str:
    unit = f"; unidad {entry['unit']}" if entry["unit"] is not None else ""
    return f"`{entry['origin']}`{unit}; fuente {entry['source_index']}"


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        f"# Auditoría bibliográfica — {summary['subject_id']}",
        "",
        "El informe inventaría ocurrencias; no fusiona referencias automáticamente. "
        "Una coincidencia por título requiere revisión humana.",
        "",
        "## Resumen",
        "",
        f"- Ocurrencias totales: {summary['total_occurrences']}",
        f"- Ocurrencias en unidades: {summary['unit_occurrences']}",
        f"- Ocurrencias en registros centrales: {summary['registry_occurrences']}",
        f"- Identificadores exactos únicos: {summary['unique_exact_identifiers']}",
        f"- Grupos duplicados por identificador: {summary['exact_duplicate_groups']}",
        f"- Posibles duplicados por título: {summary['possible_title_duplicate_groups']}",
        f"- Ocurrencias con metadatos incompletos: {summary['incomplete_occurrences']}",
        "",
        "## Fuentes por unidad",
        "",
        "| Unidad | Ocurrencias |",
        "|---:|---:|",
    ]
    for unit, count in report["unit_counts"].items():
        lines.append(f"| {unit} | {count} |")

    lines.extend(["", "## Registros escaneados", ""])
    for origin, count in report["registry_counts"].items():
        lines.append(f"- `{origin}`: {count} ocurrencias")

    lines.extend(["", "## Duplicados exactos", ""])
    if not report["exact_duplicates"]:
        lines.append("No se detectaron duplicados por DOI, PMID o URL normalizados.")
    for group in report["exact_duplicates"]:
        lines.append(f"### `{group['identifier']}`")
        lines.append("")
        for entry in group["occurrences"]:
            lines.append(f"- {entry['title']} — {occurrence_label(entry)}")
        lines.append("")

    lines.extend(["## Posibles duplicados por título", ""])
    if not report["possible_title_duplicates"]:
        lines.append("No se detectaron coincidencias de título pendientes de revisión.")
    for group in report["possible_title_duplicates"]:
        lines.append(f"### {group['normalized_title']}")
        lines.append("")
        for entry in group["occurrences"]:
            lines.append(f"- {entry['title']} — {occurrence_label(entry)}")
        lines.append("")

    lines.extend(["## Metadatos incompletos", ""])
    if not report["incomplete_entries"]:
        lines.append("No se detectaron campos obligatorios ausentes.")
    for entry in report["incomplete_entries"]:
        missing = ", ".join(entry["missing_fields"])
        lines.append(
            f"- {entry['title'] or '(sin título)'} — {occurrence_label(entry)}; "
            f"faltan: `{missing}`"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", default="biologia-desarrollo")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--fail-on-exact-duplicates", action="store_true")
    parser.add_argument("--fail-on-incomplete", action="store_true")
    args = parser.parse_args()

    try:
        report = audit(args.subject_id)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(report), encoding="utf-8")

    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    errors: list[str] = []
    if args.fail_on_exact_duplicates and report["exact_duplicates"]:
        errors.append(
            f"hay {len(report['exact_duplicates'])} grupos duplicados por identificador"
        )
    if args.fail_on_incomplete and report["incomplete_entries"]:
        errors.append(
            f"hay {len(report['incomplete_entries'])} ocurrencias con metadatos incompletos"
        )
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
