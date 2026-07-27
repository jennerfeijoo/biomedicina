#!/usr/bin/env python3
from __future__ import annotations

import base64
import binascii
import hashlib
import importlib.util
import io
import lzma
import shutil
import string
import tarfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_fisiologia_i_bioinformatica_redevelopment.py"
BOOTSTRAP = ROOT / "data" / "bootstrap" / "fisiologia-bioinformatica"
PARTIAL_RECOVERY = ROOT / "partial-recovery"
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"


def load_generator():
    spec = importlib.util.spec_from_file_location("pending_course_generator", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("No se pudo cargar el generador académico")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decode_text(text: str) -> bytes:
    remainder = len(text) % 4
    if remainder == 1:
        raise binascii.Error("longitud Base64 irrecuperable")
    return base64.b64decode(text + "=" * ((4 - remainder) % 4), validate=True)


def validate_payload(compressed: bytes) -> bytes | None:
    if not compressed.startswith(b"\xfd7zXZ\x00"):
        return None
    try:
        raw = lzma.decompress(compressed)
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
            if not archive.getmembers():
                return None
    except (lzma.LZMAError, tarfile.TarError):
        return None
    return raw


def exact_error_offset(compressed: bytes) -> tuple[int, bytes]:
    decompressor = lzma.LZMADecompressor()
    output = bytearray()
    for offset, value in enumerate(compressed):
        try:
            output.extend(decompressor.decompress(bytes((value,))))
        except lzma.LZMAError:
            return offset, bytes(output)
    return len(compressed), bytes(output)


def list_complete_tar_entries(raw: bytes) -> list[str]:
    entries: list[str] = []
    offset = 0
    while offset + 512 <= len(raw):
        header = raw[offset : offset + 512]
        if header == b"\0" * 512:
            break
        name = header[:100].split(b"\0", 1)[0].decode("utf-8", errors="replace")
        size_field = header[124:136].split(b"\0", 1)[0].strip() or b"0"
        try:
            size = int(size_field, 8)
        except ValueError:
            break
        data_end = offset + 512 + size
        padded_end = offset + 512 + ((size + 511) // 512) * 512
        if data_end > len(raw):
            break
        entries.append(f"{name} ({size} bytes)")
        offset = padded_end
    return entries


def safe_destination(base: Path, member_name: str) -> Path:
    relative = PurePosixPath(member_name)
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError(f"Ruta insegura en tar parcial: {member_name}")
    return base.joinpath(*relative.parts)


def extract_partial_tar(raw: bytes) -> list[str]:
    if PARTIAL_RECOVERY.exists():
        shutil.rmtree(PARTIAL_RECOVERY)
    PARTIAL_RECOVERY.mkdir(parents=True)
    recovered: list[str] = []

    try:
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r|") as archive:
            while True:
                try:
                    member = archive.next()
                except (tarfile.ReadError, EOFError):
                    break
                if member is None:
                    break
                target = safe_destination(PARTIAL_RECOVERY, member.name)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    recovered.append(f"DIR {member.name}")
                    continue
                if not member.isfile():
                    continue
                try:
                    source = archive.extractfile(member)
                    if source is None:
                        continue
                    payload = source.read()
                except (tarfile.ReadError, EOFError):
                    break
                if len(payload) != member.size:
                    break
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
                recovered.append(f"FILE {member.name} {member.size}")
    except tarfile.ReadError:
        pass

    manifest = PARTIAL_RECOVERY / "RECOVERY_MANIFEST.txt"
    manifest.write_text("\n".join(recovered) + "\n", encoding="utf-8")
    return recovered


def patched_substitution(
    padded_text: str,
    compressed: bytes,
    full_position: int,
    character: str,
) -> bytes:
    quartet_start = (full_position // 4) * 4
    quartet = list(padded_text[quartet_start : quartet_start + 4])
    quartet[full_position - quartet_start] = character
    decoded = base64.b64decode("".join(quartet), validate=True)
    byte_start = (quartet_start // 4) * 3
    candidate = bytearray(compressed)
    candidate[byte_start : byte_start + len(decoded)] = decoded
    return bytes(candidate)


def search_repair(prefix: str, embedded: str) -> tuple[str, bytes, bytes] | None:
    canonical = prefix + embedded
    compressed = decode_text(canonical)
    error_byte, partial_raw = exact_error_offset(compressed)
    estimated_full = min(len(canonical) - 1, (error_byte * 4) // 3)
    estimated = max(0, estimated_full - len(prefix))

    print(
        f"[diagnóstico] error XZ exacto en byte {error_byte}; "
        f"posición Base64 estimada del bloque embebido={estimated}"
    )
    entries = list_complete_tar_entries(partial_raw)
    print(f"[diagnóstico] salida parcial: {len(partial_raw)} bytes; entradas tar completas={len(entries)}")
    for entry in entries[-12:]:
        print(f"  - {entry}")

    recovered = extract_partial_tar(partial_raw)
    print(f"[diagnóstico] entradas extraídas a partial-recovery: {len(recovered)}")

    positions = set(
        range(max(0, estimated - 192), min(len(embedded), estimated + 192) + 1)
    )
    positions.update(range(0, min(48, len(embedded)) + 1))
    positions.update(range(max(0, len(embedded) - 48), len(embedded) + 1))
    padded = canonical + "=" * ((4 - len(canonical) % 4) % 4)

    for position in sorted(p for p in positions if p < len(embedded)):
        full_position = len(prefix) + position
        original = embedded[position]
        for character in ALPHABET:
            if character == original:
                continue
            candidate = patched_substitution(padded, compressed, full_position, character)
            raw = validate_payload(candidate)
            if raw is not None:
                return f"substitution:{position}:{original}>{character}", candidate, raw

    for position in sorted(p for p in positions if p + 1 < len(embedded)):
        if embedded[position] == embedded[position + 1]:
            continue
        changed = (
            embedded[:position]
            + embedded[position + 1]
            + embedded[position]
            + embedded[position + 2 :]
        )
        candidate = decode_text(prefix + changed)
        raw = validate_payload(candidate)
        if raw is not None:
            return f"swap:{position}:{embedded[position:position + 2]}", candidate, raw

    for position in sorted(positions):
        left, right = embedded[:position], embedded[position:]
        for character in ALPHABET:
            candidate = decode_text(prefix + left + character + right)
            raw = validate_payload(candidate)
            if raw is not None:
                return f"insertion:{position}:{character}", candidate, raw

        if position < len(embedded):
            candidate = decode_text(prefix + embedded[:position] + embedded[position + 1 :])
            raw = validate_payload(candidate)
            if raw is not None:
                return f"deletion:{position}:{embedded[position]}", candidate, raw

    return None


def main() -> int:
    module = load_generator()
    part_paths = sorted(BOOTSTRAP.glob("part-*.txt"))
    if not part_paths:
        raise RuntimeError("No se encontraron fragmentos del paquete académico")

    parts = [(path.name, "".join(path.read_text(encoding="utf-8").split())) for path in part_paths]
    embedded = "".join(str(module.DATA).split())
    print("[diagnóstico] fragmentos:")
    for name, text in [*parts, ("embedded", embedded)]:
        payload = decode_text(text)
        print(
            f"  - {name}: chars={len(text)}, mod4={len(text) % 4}, "
            f"bytes={len(payload)}, prefix={payload[:8].hex()}, "
            f"sha256={hashlib.sha256(payload).hexdigest()[:16]}"
        )

    prefix = "".join(text for _, text in parts)
    direct = decode_text(prefix + embedded)
    raw = validate_payload(direct)
    strategy = "direct"
    compressed = direct

    if raw is None:
        repaired = search_repair(prefix, embedded)
        if repaired is None:
            raise RuntimeError("No se pudo reparar de forma unívoca el paquete académico")
        strategy, compressed, raw = repaired

    print(f"[ok] estrategia válida: {strategy}")
    print(f"[ok] archivo XZ: {len(compressed)} bytes")
    print(f"[ok] tar descomprimido: {len(raw)} bytes; sha256={hashlib.sha256(raw).hexdigest()}")

    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        members = archive.getmembers()
        archive.extractall(ROOT, filter="data")
        print(f"[ok] artefactos extraídos: {len(members)}")

    module.patch_publisher()
    print("[ok] paquetes académicos extraídos y publicador ampliado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
