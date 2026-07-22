#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import importlib.util
import io
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "scripts" / "materialize_aed_semester.py"
SPEC = importlib.util.spec_from_file_location("aed_legacy", LEGACY)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("No se pudo cargar el validador académico existente")
legacy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(legacy)

chunks = sorted(legacy.CHUNK_DIR.glob("chunk-*.txt"))
legacy.require(len(chunks) == 9, f"se esperaban 9 fragmentos y se encontraron {len(chunks)}")
encoded = "".join(path.read_text(encoding="utf-8").strip() for path in chunks)
MEMBER_RE = re.compile(
    rf"^data/generated_units/{re.escape(legacy.SUBJECT_ID)}/unit-?(\d{{2}})\.json$"
)


def inspect_payload(payload: bytes) -> list[tuple[int, dict]]:
    try:
        archive = zipfile.ZipFile(io.BytesIO(payload))
    except zipfile.BadZipFile as error:
        raise ValueError(f"ZIP inválido: {error}") from error

    with archive:
        bad_member = archive.testzip()
        legacy.require(bad_member is None, f"CRC inválido en {bad_member}")

        member_by_number: dict[int, str] = {}
        for member in archive.namelist():
            match = MEMBER_RE.fullmatch(member)
            legacy.require(match is not None, f"miembro inesperado: {member}")
            number = int(match.group(1))
            legacy.require(1 <= number <= 6, f"número de unidad inesperado: {number}")
            legacy.require(number not in member_by_number, f"unidad duplicada en ZIP: {number}")
            member_by_number[number] = member

        legacy.require(set(member_by_number) == set(range(1, 7)), f"unidades incompletas: {sorted(member_by_number)}")

        validated: list[tuple[int, dict]] = []
        for number in range(1, 7):
            data = json.loads(archive.read(member_by_number[number]).decode("utf-8"))
            legacy.require(isinstance(data, dict), f"unit-{number:02d}: raíz no es objeto")
            legacy.validate_unit(data, number)
            validated.append((number, data))

        legacy.require(sum(data["estimated_hours"] for _, data in validated) == 128, "horas totales")
        legacy.require(
            sorted(week for _, data in validated for week in data["weeks"]) == list(range(1, 17)),
            "cobertura semanal",
        )
        return validated


def add_candidate(
    candidates: dict[str, tuple[int | None, bytes, list[tuple[int, dict]]]],
    removed_index: int | None,
    candidate_text: str,
) -> None:
    try:
        payload = base64.b64decode(candidate_text, validate=True)
        validated = inspect_payload(payload)
    except Exception:
        return
    digest = hashlib.sha256(payload).hexdigest()
    candidates.setdefault(digest, (removed_index, payload, validated))


candidates: dict[str, tuple[int | None, bytes, list[tuple[int, dict]]]] = {}
add_candidate(candidates, None, encoded)

for index in range(len(encoded)):
    add_candidate(candidates, index, encoded[:index] + encoded[index + 1 :])

legacy.require(
    len(candidates) == 1,
    f"se esperó una recuperación única y se encontraron {len(candidates)} payloads válidos",
)
actual_sha, (removed_index, payload, validated) = next(iter(candidates.items()))
legacy.DEST_DIR.mkdir(parents=True, exist_ok=True)
for number, data in validated:
    destination = legacy.DEST_DIR / f"unit-{number:02d}.json"
    destination.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Materializado y validado: {destination.relative_to(ROOT)}")

print(f"Recuperación única eliminando posición: {removed_index}")
print(f"Paquete validado estructuralmente: sha256={actual_sha}")
print(f"SHA histórico registrado: {legacy.EXPECTED_SHA256}")
