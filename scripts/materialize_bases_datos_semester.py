#!/usr/bin/env python3
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_DIR = ROOT / ".citonauta-agent" / "payloads" / "bases-datos"
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
    1: "30ad93d145e4ef2234928e71c1467424610943aee0c64aab40f42154cb45d9b4",
    2: "39f2357fefbbbfc742b5adc643a627afdae6fdba7d6179f892640cab2fa5f102",
    3: "b2fb66a27eba7433672d32fd5b5cdf1b4f72919d7ffb53605958ef3943271383",
    4: "516803bcdde851be547a6b92238714895f4b2a6a40ff892576f9ab176348ec52",
    5: "cd893adb7b7d76132c20845ad89e9ac0fb83b568c6528d9135cf94477ecfa7b3",
    6: "742520d10695891702298ad6ee51a60f12ef2486223d22e92641526ed06eaedf",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_verified_unit(number: int) -> dict[str, Any]:
    label = f"unit-{number:02d}"
    path = PAYLOAD_DIR / f"{label}.json.gz.b64"
    require(path.exists(), f"{label}: falta payload")

    encoded = path.read_text(encoding="utf-8").strip()
    compressed = base64.b64decode(encoded, validate=True)
    compressed_sha = hashlib.sha256(compressed).hexdigest()
    raw = gzip.decompress(compressed)
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
    units = [(number, load_verified_unit(number)) for number in range(1, 7)]
    require(sum(data["estimated_hours"] for _, data in units) == 128, "horas totales")
    require(
        sorted(week for _, data in units for week in data["weeks"]) == list(range(1, 17)),
        "cobertura semanal",
    )

    DEST.mkdir(parents=True, exist_ok=True)
    for number, data in units:
        path = DEST / f"unit-{number:02d}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Materializado: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
