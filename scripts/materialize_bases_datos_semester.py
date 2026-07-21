#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / ".citonauta-agent" / "payloads" / "bases-datos-semester.b64"
DEST = ROOT / "data" / "generated_units" / "bases-datos"
EXPECTED_SHA256 = "0f82340df691021cc5254a1105bef4df2f69f28657258c9374261704affc91d0"
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> int:
    encoded = PAYLOAD.read_text(encoding="utf-8").strip()
    payload = base64.b64decode(encoded, validate=True)
    actual_sha = hashlib.sha256(payload).hexdigest()
    require(actual_sha == EXPECTED_SHA256, f"SHA-256 inesperado: {actual_sha}")

    expected_members = {f"data/generated_units/bases-datos/unit-{number:02d}.json" for number in range(1, 7)}
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        require(archive.testzip() is None, "CRC inválido en el paquete")
        require(set(archive.namelist()) == expected_members, "miembros inesperados en el ZIP")
        units: list[tuple[int, dict]] = []
        for number in range(1, 7):
            member = f"data/generated_units/bases-datos/unit-{number:02d}.json"
            data = json.loads(archive.read(member).decode("utf-8"))
            require(data.get("schema_version") == "2.0", f"unit-{number:02d}: schema_version")
            require(data.get("subject_id") == "bases-datos", f"unit-{number:02d}: subject_id")
            require(data.get("area_id") == "ciencias-basicas", f"unit-{number:02d}: area_id")
            require(data.get("unit") == number, f"unit-{number:02d}: número")
            require(data.get("title") == EXPECTED_TITLES[number], f"unit-{number:02d}: título")
            require(data.get("status") == "review", f"unit-{number:02d}: status")
            require(data.get("weeks") == EXPECTED_WEEKS[number], f"unit-{number:02d}: semanas")
            require(data.get("estimated_hours") == EXPECTED_HOURS[number], f"unit-{number:02d}: horas")
            require(len(data.get("theory_sections", [])) >= 4, f"unit-{number:02d}: teoría")
            require(len(data.get("worked_examples", [])) >= 2, f"unit-{number:02d}: ejemplos")
            require(len(data.get("sources", [])) >= 5, f"unit-{number:02d}: fuentes")
            units.append((number, data))

    require(sum(data["estimated_hours"] for _, data in units) == 128, "horas totales")
    require(sorted(week for _, data in units for week in data["weeks"]) == list(range(1, 17)), "cobertura semanal")
    DEST.mkdir(parents=True, exist_ok=True)
    for number, data in units:
        path = DEST / f"unit-{number:02d}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Materializado: {path.relative_to(ROOT)}")
    print(f"Paquete verificado: sha256={actual_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
