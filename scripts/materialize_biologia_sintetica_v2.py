#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import json
import lzma
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "data" / "bootstrap" / "biologia-sintetica-v2"
MANIFEST_PATH = BOOTSTRAP / "manifest.json"
COVERAGE_PATH = ROOT / "data" / "curriculum_coverage" / "biological-medical.json"
PATCH_PATH = ROOT / "coverage_patch.json"


def load_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: la raíz debe ser un objeto JSON")
    return data


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def verified_archive() -> bytes:
    manifest = load_object(MANIFEST_PATH)
    parts = sorted(BOOTSTRAP.glob("part-*.txt"))
    expected_count = int(manifest["chunks"])
    if len(parts) != expected_count:
        raise RuntimeError(
            f"Número de fragmentos inválido: {len(parts)}; se esperaban {expected_count}"
        )

    chunks: list[str] = []
    for index, path in enumerate(parts):
        text = "".join(path.read_text(encoding="utf-8").split())
        expected_length = int(manifest["chunk_lengths"][index])
        expected_sha = str(manifest["chunk_sha256"][index])
        actual_sha = sha256_bytes(text.encode("ascii"))
        if len(text) != expected_length:
            raise RuntimeError(
                f"{path.name}: longitud {len(text)}; se esperaba {expected_length}"
            )
        if actual_sha != expected_sha:
            raise RuntimeError(
                f"{path.name}: SHA-256 {actual_sha}; se esperaba {expected_sha}"
            )
        chunks.append(text)
        print(f"[ok] {path.name}: {len(text)} caracteres; sha256={actual_sha}")

    encoded = "".join(chunks)
    if len(encoded) != int(manifest["base64_chars"]):
        raise RuntimeError("Longitud Base64 agregada inválida")
    if sha256_bytes(encoded.encode("ascii")) != manifest["base64_sha256"]:
        raise RuntimeError("SHA-256 Base64 agregado inválido")

    compressed = base64.b64decode(encoded, validate=True)
    if len(compressed) != int(manifest["xz_bytes"]):
        raise RuntimeError("Longitud XZ inválida")
    if sha256_bytes(compressed) != manifest["xz_sha256"]:
        raise RuntimeError("SHA-256 XZ inválido")
    if not compressed.startswith(b"\xfd7zXZ\x00"):
        raise RuntimeError("Cabecera XZ inválida")

    raw = lzma.decompress(compressed)
    if len(raw) != int(manifest["tar_bytes"]):
        raise RuntimeError("Longitud tar inválida")
    if sha256_bytes(raw) != manifest["tar_sha256"]:
        raise RuntimeError("SHA-256 tar inválido")
    return raw


def extract_archive(raw: bytes) -> int:
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        members = archive.getmembers()
        for member in members:
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or ".." in relative.parts:
                raise RuntimeError(f"Ruta insegura en el paquete: {member.name}")
            if not (member.isfile() or member.isdir()):
                raise RuntimeError(f"Tipo de miembro no permitido: {member.name}")
        archive.extractall(ROOT, filter="data")
    return len(members)


def update_coverage() -> None:
    patch = load_object(PATCH_PATH)
    coverage = load_object(COVERAGE_PATH)
    subject_id = str(patch["subject_id"])
    specification = coverage.get("courses", {}).get(subject_id)
    if not isinstance(specification, dict):
        raise RuntimeError(f"No existe matriz curricular para {subject_id}")

    expected_ids = [f"BS-{number:02d}" for number in range(1, 9)]
    actual_ids = [str(item.get("id")) for item in specification.get("core_domains", [])]
    if actual_ids != expected_ids:
        raise RuntimeError(
            f"Dominios inesperados: {actual_ids}; se esperaban {expected_ids}"
        )

    specification["title"] = patch["title"]
    specification["coverage_state"] = "implemented"
    for key in ("practical_requirements", "visual_requirements", "expansion_priorities"):
        specification[key] = patch[key]

    COVERAGE_PATH.write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    PATCH_PATH.unlink()
    print(f"[ok] {subject_id}: cobertura curricular actualizada a implemented")


def main() -> int:
    raw = verified_archive()
    count = extract_archive(raw)
    update_coverage()
    print(f"[ok] paquete académico extraído: {count} entradas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
