#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import importlib.util
import io
import lzma
import shutil
import tarfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_fisiologia_i_bioinformatica_redevelopment.py"
BOOTSTRAP = ROOT / "data" / "bootstrap" / "fisiologia-bioinformatica"
PARTIAL_RECOVERY = ROOT / "partial-recovery"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decode_package(generator) -> bytes:
    parts = [
        "".join(path.read_text(encoding="utf-8").split())
        for path in sorted(BOOTSTRAP.glob("part-*.txt"))
    ]
    if not parts:
        raise FileNotFoundError("No se encontraron fragmentos del paquete académico")
    parts.append("".join(str(generator.DATA).split()))
    encoded = "".join(parts)
    remainder = len(encoded) % 4
    if remainder == 1:
        raise RuntimeError(f"Longitud Base64 irrecuperable: {len(encoded)}")
    encoded += "=" * ((4 - remainder) % 4)
    compressed = base64.b64decode(encoded, validate=True)
    if not compressed.startswith(b"\xfd7zXZ\x00"):
        raise RuntimeError("El paquete no contiene una cabecera XZ válida")
    return compressed


def exact_partial_output(compressed: bytes) -> tuple[int, bytes]:
    decompressor = lzma.LZMADecompressor()
    output = bytearray()
    for offset, value in enumerate(compressed):
        try:
            output.extend(decompressor.decompress(bytes((value,))))
        except lzma.LZMAError:
            return offset, bytes(output)
    return len(compressed), bytes(output)


def safe_target(base: Path, name: str) -> Path:
    relative = PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError(f"Ruta insegura en tar: {name}")
    return base.joinpath(*relative.parts)


def extract_complete_entries(raw: bytes) -> list[str]:
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
                target = safe_target(PARTIAL_RECOVERY, member.name)
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
    (PARTIAL_RECOVERY / "RECOVERY_MANIFEST.txt").write_text(
        "\n".join(recovered) + "\n", encoding="utf-8"
    )
    return recovered


def extract_full_archive(raw: bytes) -> int:
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        members = archive.getmembers()
        archive.extractall(ROOT, filter="data")
    return len(members)


def main() -> int:
    generator = load_module(GENERATOR, "pending_course_generator")
    compressed = decode_package(generator)
    print(f"[diagnóstico] archivo XZ ensamblado: {len(compressed)} bytes")

    try:
        raw = lzma.decompress(compressed)
    except lzma.LZMAError:
        error_offset, partial_raw = exact_partial_output(compressed)
        recovered = extract_complete_entries(partial_raw)
        print(
            f"[diagnóstico] XZ corrupto en byte {error_offset}; "
            f"salida parcial={len(partial_raw)} bytes; entradas íntegras={len(recovered)}"
        )
        builder = load_module(
            ROOT / "scripts" / "build_missing_bioinformatica_redevelopment.py",
            "bioinformatica_builder",
        )
        builder.build_from_partial_recovery()
        generator.patch_publisher()
        print("[ok] se conservó Fisiología Humana I y se reconstruyó Bioinformática")
        return 0

    count = extract_full_archive(raw)
    generator.patch_publisher()
    print(
        f"[ok] paquete completo extraído: {count} entradas; "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
