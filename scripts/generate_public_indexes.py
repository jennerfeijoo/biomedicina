#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import generate_site


def read_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("courses"), list):
        raise ValueError("manifiesto inválido: se requiere una lista courses")
    return data


def expected_outputs(manifest_path: Path) -> dict[Path, str]:
    manifest = read_manifest(manifest_path)
    area_ids = {
        str(course.get("area_id") or "").strip()
        for course in manifest["courses"]
        if isinstance(course, dict)
    }
    area_ids.discard("")
    if not area_ids:
        raise ValueError("el manifiesto no contiene áreas")

    data = generate_site.load_json(generate_site.DATA_PATH)
    area_template = generate_site.load_template(generate_site.AREA_TEMPLATE_PATH)
    catalog_template = generate_site.load_template(generate_site.CATALOG_TEMPLATE_PATH)
    generate_site.validate_area_template(area_template)
    generate_site.validate_catalog_template(catalog_template)

    outputs: dict[Path, str] = {}
    known = set()
    for area in data.get("areas", []):
        area_id = str(area["id"])
        known.add(area_id)
        if area_id in area_ids:
            path = ROOT / area["path"]
            outputs[path] = generate_site.normalize_output(
                generate_site.render_area(area_template, area)
            )
    missing = sorted(area_ids - known)
    if missing:
        raise ValueError("áreas ausentes del currículo: " + ", ".join(missing))

    catalog_path = ROOT / "catalogo" / "index.html"
    outputs[catalog_path] = generate_site.render_catalog(catalog_template, data)
    return outputs


def run(manifest_path: Path, check: bool) -> None:
    mismatches: list[str] = []
    for path, expected in expected_outputs(manifest_path).items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current == expected:
            continue
        relative = path.relative_to(ROOT).as_posix()
        mismatches.append(relative)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
            print(f"[ok] {relative}")
    if check and mismatches:
        raise SystemExit("Índices públicos desincronizados:\n- " + "\n- ".join(mismatches))
    if check:
        print("Índices públicos sincronizados.")
    elif not mismatches:
        print("No hay cambios en índices públicos.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    run(args.manifest, args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
