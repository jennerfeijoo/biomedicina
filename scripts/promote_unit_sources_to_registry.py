#!/usr/bin/env python3
"""Promote complete unit-local sources into the canonical course registry.

The command groups unresolved unit references by connected DOI, PMID and URL
identifiers. It refuses to merge conflicting titles, authors, years, types or
verification states. Existing unit JSON is not edited; unit references continue
to resolve through their identifiers or local IDs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_course_bibliography as bibliography  # noqa: E402

REGISTRY_ROOT = ROOT / "data" / "source_registry"
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def slugify(value: str) -> str:
    text = unicodedata.normalize("NFKD", value.lower())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return NON_ALNUM_RE.sub("-", text).strip("-")


def as_list(value: Any) -> list[str]:
    if value in (None, "", []):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def unique(values: list[str]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def one_value(
    records: list[dict[str, Any]],
    label: str,
    *keys: str,
    normalize=lambda value: str(value).strip(),
) -> Any:
    observed: dict[str, Any] = {}
    for record in records:
        value = None
        for key in keys:
            candidate = record.get(key)
            if candidate not in (None, "", []):
                value = candidate
                break
        if value in (None, "", []):
            continue
        observed[normalize(value)] = value
    if len(observed) > 1:
        raise ValueError(
            f"conflicto en {label}: " + " | ".join(str(value) for value in observed.values())
        )
    return next(iter(observed.values()), None)


def unresolved_unit_raws(subject_id: str) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, set[str]]]:
    registry_records = bibliography.load_registry_records(subject_id)
    by_id, by_identifier, errors = bibliography.build_registry_index(registry_records)
    if errors:
        raise ValueError("; ".join(errors))
    unresolved: list[dict[str, Any]] = []
    for raw in bibliography.load_unit_records(subject_id):
        canonical_id, _, ambiguous = bibliography.resolve_canonical(
            raw["record"], by_id, by_identifier
        )
        if ambiguous:
            raise ValueError(
                f"{raw['origin']} fuente {raw['source_index']}: referencia ambigua {ambiguous}"
            )
        if canonical_id is None:
            unresolved.append(raw)
    return unresolved, by_id, by_identifier


def components(raws: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    union_find = UnionFind(len(raws))
    identifier_owner: dict[str, int] = {}
    for index, raw in enumerate(raws):
        ids = bibliography.identifiers(raw["record"])
        if not ids:
            raise ValueError(
                f"{raw['origin']} fuente {raw['source_index']}: falta identificador estable"
            )
        for identifier in ids:
            previous = identifier_owner.get(identifier)
            if previous is None:
                identifier_owner[identifier] = index
            else:
                union_find.union(index, previous)
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for index, raw in enumerate(raws):
        grouped[union_find.find(index)].append(raw)
    return list(grouped.values())


def choose_id(
    raws: list[dict[str, Any]],
    title: str,
    year: Any,
    reserved_names: set[str],
) -> tuple[str, list[str]]:
    proposed = unique(
        [
            str(raw["record"].get("id") or raw["record"].get("registry_id") or "").strip()
            for raw in raws
        ]
    )
    proposed = [value for value in proposed if value]
    base = proposed[0] if proposed else slugify(f"{title}-{year or 'undated'}")
    candidate = base
    suffix = 2
    while candidate in reserved_names:
        candidate = f"{base}-{suffix}"
        suffix += 1
    aliases = [value for value in proposed if value != candidate and value not in reserved_names]
    return candidate, aliases


def build_canonical_source(
    raws: list[dict[str, Any]], reserved_names: set[str]
) -> dict[str, Any]:
    records = [raw["record"] for raw in raws]
    title = one_value(records, "title", "title", normalize=bibliography.normalize_title)
    authors = one_value(
        records,
        "authors_or_organization",
        "authors_or_organization",
        "organization",
        normalize=lambda value: bibliography.normalize_title(value),
    )
    year = one_value(records, "year", "year", normalize=lambda value: str(value))
    source_type = one_value(records, "type", "type", normalize=lambda value: str(value).strip())
    verification = one_value(
        records,
        "verification_status",
        "verification_status",
        normalize=lambda value: str(value).strip(),
    )
    if not all((title, authors, source_type, verification)):
        raise ValueError(
            f"fuente sin metadatos mínimos en {', '.join(raw['origin'] for raw in raws)}"
        )

    canonical_id, aliases = choose_id(raws, str(title), year, reserved_names)
    all_identifiers = unique(
        [identifier for record in records for identifier in bibliography.identifiers(record)]
    )
    doi = next((value[4:] for value in all_identifiers if value.startswith("doi:")), None)
    pmid = next((value[5:] for value in all_identifiers if value.startswith("pmid:")), None)
    url = next((value[4:] for value in all_identifiers if value.startswith("url:")), None)

    roles: list[str] = []
    limitations: list[str] = []
    consulted_on: list[str] = []
    units: set[int] = set()
    citations: list[str] = []
    provenance: list[str] = []
    for raw, record in zip(raws, records):
        roles.extend(as_list(record.get("curricular_use") or record.get("role")))
        limitations.extend(as_list(record.get("limitations")))
        consulted_on.extend(as_list(record.get("consulted_on")))
        citations.extend(as_list(record.get("citation")))
        if raw.get("unit") is not None:
            units.add(int(raw["unit"]))
        provenance.append(f"{raw['origin']}#source-{raw['source_index']}")

    source: dict[str, Any] = {
        "id": canonical_id,
        "title": title,
        "authors_or_organization": authors,
    }
    if aliases:
        source["aliases"] = aliases
    if year is not None:
        source["year"] = year
    source["type"] = source_type
    if doi:
        source["doi"] = doi
    if pmid:
        source["pmid"] = pmid
    if url:
        source["url"] = url
    for record in records:
        if record.get("isbn"):
            source["isbn"] = record["isbn"]
            break
    source["verification_status"] = verification
    if consulted_on:
        source["consulted_on"] = max(consulted_on)
    source["units"] = sorted(units)
    source["curricular_role"] = unique(roles)
    source["limitations"] = " ".join(unique(limitations))
    if citations:
        source["citation_variants"] = unique(citations)
    source["source_provenance"] = unique(provenance)
    return source


def promote(subject_id: str) -> tuple[dict[str, Any], int]:
    main_path = REGISTRY_ROOT / f"{subject_id}.json"
    if not main_path.exists():
        raise FileNotFoundError(f"No existe {main_path}")
    registry = bibliography.load_json(main_path)
    sources = registry.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources debe ser una lista")

    unresolved, by_id, _ = unresolved_unit_raws(subject_id)
    reserved_names = set(by_id)
    additions: list[dict[str, Any]] = []
    for group in components(unresolved):
        source = build_canonical_source(group, reserved_names)
        additions.append(source)
        reserved_names.add(source["id"])
        reserved_names.update(source.get("aliases", []))

    additions.sort(key=lambda source: (min(source.get("units", [999])), source["id"]))
    output = dict(registry)
    output["sources"] = [*sources, *additions]
    output["last_reviewed"] = "2026-07-27"
    consolidation = dict(output.get("consolidation", {}))
    consolidation.update(
        {
            "status": "complete",
            "source_count": len(output["sources"]),
            "unit_source_promotion": "complete",
            "promoted_source_count": len(additions),
            "promotion_rule": "connected exact DOI, PMID and URL identifiers with conflict rejection",
        }
    )
    output["consolidation"] = consolidation
    errors = bibliography.build_registry_index(
        [
            {
                "origin_kind": "registry",
                "origin": str(main_path.relative_to(ROOT)),
                "unit": None,
                "source_index": index,
                "record": source,
            }
            for index, source in enumerate(output["sources"], start=1)
        ]
    )[2]
    if errors:
        raise ValueError("; ".join(errors))
    return output, len(additions)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", default="biologia-desarrollo")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        if args.check:
            unresolved, _, _ = unresolved_unit_raws(args.subject_id)
            if unresolved:
                print(
                    f"ERROR: quedan {len(unresolved)} usos de unidad sin registro canónico",
                    file=sys.stderr,
                )
                return 1
            print("unregistered_unit_occurrences: 0")
            return 0

        output, additions = promote(args.subject_id)
        path = REGISTRY_ROOT / f"{args.subject_id}.json"
        path.write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"promoted_canonical_sources: {additions}")
        print(f"canonical_sources: {len(output['sources'])}")
        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
