#!/usr/bin/env python3
from __future__ import annotations

import base64
import binascii
import hashlib
import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNK_DIR = ROOT / ".citonauta-agent" / "aed-clean"
DEST = ROOT / "data" / "generated_units" / "algoritmos-estructuras-datos"
EXPECTED_ENCODED_LENGTH = 61_880
EXPECTED_PAYLOAD_LENGTH = 46_408
EXPECTED_CHUNK_LENGTHS = [6_000] * 10 + [1_880]
EXPECTED_UNIT_SHA256 = {
    1: "d518e968ca6a3e9c8f40e0c4191fcf2eb678b4bf8a60532b254c88e89df91672",
    2: "6bd54a0996b4f56c58f4f694e20151a1c5a7a8b3da62b6e800b13b7404d1bf0d",
    3: "322d1e35f0cd0b8a1a560f6c0150497e0ebf1b9c9c972aa4a7a4aeb5b68f9752",
    4: "455085ea06ce6e9263ff260392a6682dab85d62536da4a5e18fc099c23e7acd3",
    5: "3c31f00f8c23542d32dedabbf3fc5604cc9cf0d4dd242cdbacebd396acf18680",
    6: "20fa67501e32232bbefb94be5dcee1e443eb53b47767e18c77a164311eac33cd",
}
EXPECTED = {
    f"data/generated_units/algoritmos-estructuras-datos/unit-{number:02d}.json"
    for number in range(1, 7)
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def run() -> None:
    chunks = sorted(CHUNK_DIR.glob("chunk-*.txt"))
    chunk_lengths = [len(path.read_text(encoding="utf-8").strip()) for path in chunks]
    print(f"diagnostic.chunk_count={len(chunks)}")
    print(f"diagnostic.chunk_lengths={chunk_lengths}")
    require(len(chunks) == 11, f"se esperaban 11 fragmentos y se encontraron {len(chunks)}")
    require(chunk_lengths == EXPECTED_CHUNK_LENGTHS, f"longitudes de fragmentos inesperadas: {chunk_lengths}")

    encoded = "".join(path.read_text(encoding="utf-8").strip() for path in chunks)
    print(f"diagnostic.encoded_length={len(encoded)}")
    require(len(encoded) == EXPECTED_ENCODED_LENGTH, f"longitud base64 inesperada: {len(encoded)}")

    try:
        payload = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError(f"base64 inválido: {error}") from error

    container_digest = hashlib.sha256(payload).hexdigest()
    print(f"diagnostic.payload_length={len(payload)}")
    print(f"diagnostic.container_sha256={container_digest}")
    require(len(payload) == EXPECTED_PAYLOAD_LENGTH, f"tamaño de ZIP inesperado: {len(payload)}")

    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        print(f"diagnostic.bad_member={bad_member}")
        require(bad_member is None, f"CRC inválido en {bad_member}")
        require(set(archive.namelist()) == EXPECTED, "el ZIP no contiene exactamente las seis unidades esperadas")
        units: list[tuple[int, dict]] = []
        for number in range(1, 7):
            member = f"data/generated_units/algoritmos-estructuras-datos/unit-{number:02d}.json"
            raw = archive.read(member)
            unit_digest = hashlib.sha256(raw).hexdigest()
            print(f"diagnostic.unit_{number:02d}_sha256={unit_digest}")
            require(unit_digest == EXPECTED_UNIT_SHA256[number], f"unit-{number:02d}: SHA-256 de contenido inesperado: {unit_digest}")
            data = json.loads(raw.decode("utf-8"))
            require(isinstance(data, dict), f"unit-{number:02d}: raíz no es objeto")
            require(data.get("schema_version") == "2.0", f"unit-{number:02d}: esquema")
            require(data.get("subject_id") == "algoritmos-estructuras-datos", f"unit-{number:02d}: subject_id")
            require(data.get("unit") == number, f"unit-{number:02d}: número")
            require(data.get("status") == "review", f"unit-{number:02d}: estado")
            units.append((number, data))

    require(sum(int(data["estimated_hours"]) for _, data in units) == 128, "las horas de las unidades no suman 128")
    require(sorted(week for _, data in units for week in data["weeks"]) == list(range(1, 17)), "cobertura semanal incorrecta")
    DEST.mkdir(parents=True, exist_ok=True)
    for number, data in units:
        path = DEST / f"unit-{number:02d}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Materializada: {path.relative_to(ROOT)}")
    print(f"Paquete verificado por contenido: {container_digest}")


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        print(f"MATERIALIZATION_ERROR: {error}")
        raise SystemExit(1)
