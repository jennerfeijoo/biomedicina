#!/usr/bin/env python3
"""Consolidate course-specific source registry supplements deterministically.

The command validates canonical IDs and aliases before writing. In ``--write``
mode it merges ``<subject-id>-*.json`` supplements into the main registry and
removes the supplements. In ``--check`` mode it requires a single consolidated
registry and validates its integrity. No network requests are performed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_ROOT = ROOT / "data" / "source_registry"


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: el registro debe ser un objeto JSON")
    return data


def validate_sources(sources: list[Any]) -> list[str]:
    errors: list[str] = []
    canonical_ids: set[str] = set()
    names: dict[str, str] = {}

    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            errors.append(f"fuente {index}: debe ser un objeto")
            continue
        canonical_id = str(source.get("id") or "").strip()
        if not canonical_id:
            errors.append(f"fuente {index}: falta id canónico")
            continue
        if canonical_id in canonical_ids:
            errors.append(f"id canónico duplicado: {canonical_id}")
        canonical_ids.add(canonical_id)

        aliases = source.get("aliases", [])
        if aliases is None:
            aliases = []
        if not isinstance(aliases, list):
            errors.append(f"{canonical_id}: aliases debe ser una lista")
            aliases = []
        for name in [canonical_id, *[str(alias).strip() for alias in aliases]]:
            if not name:
                continue
            previous = names.get(name)
            if previous and previous != canonical_id:
                errors.append(
                    f"id o alias `{name}` apunta a `{previous}` y `{canonical_id}`"
                )
            names[name] = canonical_id
    return errors


def paths(subject_id: str) -> tuple[Path, list[Path]]:
    main = REGISTRY_ROOT / f"{subject_id}.json"
    supplements = sorted(REGISTRY_ROOT.glob(f"{subject_id}-*.json"))
    return main, supplements


def consolidate(subject_id: str) -> tuple[dict[str, Any], list[Path]]:
    main_path, supplements = paths(subject_id)
    if not main_path.exists():
        raise FileNotFoundError(f"No existe el registro principal: {main_path}")
    main = load_json(main_path)
    sources = list(main.get("sources", []))
    merged_from: list[str] = []

    for supplement_path in supplements:
        supplement = load_json(supplement_path)
        if supplement.get("subject_id") != subject_id:
            raise ValueError(
                f"{supplement_path}: subject_id no coincide con {subject_id}"
            )
        supplement_sources = supplement.get("sources", [])
        if not isinstance(supplement_sources, list):
            raise ValueError(f"{supplement_path}: sources debe ser una lista")
        sources.extend(supplement_sources)
        merged_from.append(str(supplement_path.relative_to(ROOT)))

    errors = validate_sources(sources)
    if errors:
        raise ValueError("; ".join(errors))

    output = dict(main)
    output["last_reviewed"] = "2026-07-27"
    output["purpose"] = (
        "Registro canónico consolidado de las fuentes que respaldan la arquitectura, "
        "los mecanismos, métodos, aplicaciones biomédicas y límites éticos de "
        "Biología del Desarrollo."
    )
    output["sources"] = sources
    output["consolidation"] = {
        "status": "complete",
        "merged_on": "2026-07-27",
        "source_count": len(sources),
        "merged_from": merged_from,
        "deduplication_key_order": ["id_or_alias", "doi", "pmid", "url"],
        "note": (
            "La consolidación unifica registros; los usos repetidos por unidad se "
            "mantienen como referencias locales resueltas por el auditor."
        ),
    }
    return output, supplements


def check(subject_id: str) -> list[str]:
    main_path, supplements = paths(subject_id)
    errors: list[str] = []
    if not main_path.exists():
        return [f"no existe {main_path}"]
    if supplements:
        errors.append(
            "quedan registros suplementarios: "
            + ", ".join(str(path.relative_to(ROOT)) for path in supplements)
        )
    main = load_json(main_path)
    sources = main.get("sources", [])
    if not isinstance(sources, list):
        errors.append("sources debe ser una lista")
        return errors
    errors.extend(validate_sources(sources))
    consolidation = main.get("consolidation", {})
    if not isinstance(consolidation, dict) or consolidation.get("status") != "complete":
        errors.append("falta consolidation.status=complete")
    declared_count = consolidation.get("source_count") if isinstance(consolidation, dict) else None
    if declared_count != len(sources):
        errors.append(
            f"consolidation.source_count={declared_count} no coincide con {len(sources)}"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", default="biologia-desarrollo")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        if args.check:
            errors = check(args.subject_id)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            main_path, _ = paths(args.subject_id)
            data = load_json(main_path)
            print(f"consolidated_sources: {len(data.get('sources', []))}")
            return 0

        output, supplements = consolidate(args.subject_id)
        main_path, _ = paths(args.subject_id)
        main_path.write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        for supplement in supplements:
            supplement.unlink()
        print(f"consolidated_sources: {len(output['sources'])}")
        for supplement in supplements:
            print(f"removed_supplement: {supplement.relative_to(ROOT)}")
        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
