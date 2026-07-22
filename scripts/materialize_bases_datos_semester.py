#!/usr/bin/env python3
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEGACY_PAYLOAD_DIR = ROOT / ".citonauta-agent" / "payloads" / "bases-datos"
CHUNK_DIR = ROOT / ".citonauta-agent" / "payloads" / "bases-datos-v2"
V4_DIR = ROOT / ".citonauta-agent" / "payloads" / "bases-datos-v4"
DEST = ROOT / "data" / "generated_units" / "bases-datos"
EXPECTED_TITLES = {
    1: "Modelado de datos",
    2: "Modelo relacional y normalización",
    3: "SQL para consulta y análisis",
    4: "Transacciones y concurrencia",
    5: "Índices, seguridad y rendimiento",
    6: "Datos biomédicos heterogéneos",
}
EXPECTED_WEEKS = {1: [1, 2], 2: [3, 4, 5], 3: [6, 7, 8], 4: [9, 10, 11], 5: [12, 13], 6: [14, 15, 16]}
EXPECTED_HOURS = {1: 16, 2: 24, 3: 24, 4: 24, 5: 16, 6: 24}
EXPECTED_RAW_SHA256 = {
    1: "1b8b8fc3835e13124c1fab20db89e3c574bd66086f2a0f9f4e4390f27e284de9",
    2: "e19d0f3c2fb099de019d3840c988bedbaab7aa78a6931ea91ca3c51119619dd8",
    3: "2cff40606b42580019fafc7d3bbab7f2da4bf7b1d14b85f79da42677eadd843a",
    4: "1d626065f52a8ab9ad5573e48480b487444b8c17fd3a2d04a480c88253714e9d",
    5: "ba9e71c6848125330728c74a8932c78af8ff6d0921c09e79e193170ae9f4ef7f",
    6: "8e3b7283e4d73e3702ffb66461e733b46e5ee1150a7d47787f342a1ebf551229",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_encoded_payload(number: int) -> str:
    if number == 2:
        v4_parts = [V4_DIR / f"unit-02-part-{part:02d}.txt" for part in range(1, 6)]
        if all(path.exists() for path in v4_parts):
            print("2: usando payload corregido v4")
            return "".join(path.read_text(encoding="utf-8").strip() for path in v4_parts)

    part_paths = [
        CHUNK_DIR / f"unit-{number:02d}-part-01.txt",
        CHUNK_DIR / f"unit-{number:02d}-part-02.txt",
    ]
    if all(path.exists() for path in part_paths):
        print(f"{number}: usando payload fragmentado v2")
        return "".join(path.read_text(encoding="utf-8").strip() for path in part_paths)

    legacy = LEGACY_PAYLOAD_DIR / f"unit-{number:02d}.json.gz.b64"
    require(legacy.exists(), f"unit-{number:02d}: falta payload")
    print(f"{number}: usando payload gzip histórico")
    return legacy.read_text(encoding="utf-8").strip()


def load_verified_unit(number: int) -> dict[str, Any]:
    label = f"unit-{number:02d}"
    encoded = read_encoded_payload(number)
    try:
        compressed = base64.b64decode(encoded, validate=True)
    except Exception as error:
        raise ValueError(f"{label}: base64 inválido: {error}") from error
    compressed_sha = hashlib.sha256(compressed).hexdigest()
    try:
        raw = gzip.decompress(compressed)
    except Exception as error:
        raise ValueError(f"{label}: gzip inválido: {error}; gzip_sha256={compressed_sha}") from error
    raw_sha = hashlib.sha256(raw).hexdigest()
    require(raw_sha == EXPECTED_RAW_SHA256[number], f"{label}: SHA-256 JSON inesperado: {raw_sha}")
    data = json.loads(raw.decode("utf-8"))
    require(isinstance(data, dict), f"{label}: la raíz debe ser un objeto")

    require(data.get("schema_version") == "2.0", f"{label}: schema_version")
    require(data.get("subject_id") == "bases-datos", f"{label}: subject_id")
    require(data.get("area_id") == "ciencias-basicas", f"{label}: area_id")
    require(data.get("unit") == number, f"{label}: número")
    require(data.get("title") == EXPECTED_TITLES[number], f"{label}: título")
    require(data.get("status") == "review", f"{label}: status")
    require(data.get("weeks") == EXPECTED_WEEKS[number], f"{label}: semanas")
    require(data.get("estimated_hours") == EXPECTED_HOURS[number], f"{label}: horas")
    require(len(data.get("learning_objectives", [])) >= 5, f"{label}: objetivos")
    require(len(data.get("theory_sections", [])) >= 4, f"{label}: teoría")
    require(len(data.get("worked_examples", [])) >= 2, f"{label}: ejemplos")
    require(len(data.get("guided_activities", [])) >= 1, f"{label}: actividad guiada")
    require(len(data.get("practice_sets", [])) >= 1, f"{label}: práctica")
    require(len(data.get("self_assessment", [])) >= 8, f"{label}: autoevaluación")
    require(len(data.get("sources", [])) >= 5, f"{label}: fuentes")
    print(f"Verificado {label}: gzip_sha256={compressed_sha} raw_sha256={raw_sha}")
    return data


def main() -> int:
    units: list[tuple[int, dict[str, Any]]] = []
    for number in range(1, 7):
        units.append((number, load_verified_unit(number)))
    require(sum(data["estimated_hours"] for _, data in units) == 128, "horas totales")
    require(sorted(week for _, data in units for week in data["weeks"]) == list(range(1, 17)), "cobertura semanal")

    DEST.mkdir(parents=True, exist_ok=True)
    for number, data in units:
        path = DEST / f"unit-{number:02d}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Materializado: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"MATERIALIZATION_ERROR: {error}")
        raise SystemExit(1)
