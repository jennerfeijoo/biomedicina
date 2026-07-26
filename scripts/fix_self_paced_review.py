#!/usr/bin/env python3
"""Repair review findings from the self-paced curriculum migration.

This script is intentionally idempotent. It removes study-duration metadata from
public course/unit metadata and restores Spanish connectives damaged by the old
substring replacement ``que que -> que``.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".py", ".js", ".css", ".html", ".md", ".yml", ".yaml", ".json"}
RISKY_BASE_LINE = re.compile(r"\bque\s+que\w+", re.IGNORECASE)
DURATION_META = re.compile(
    r"<div>\s*<dt>\s*Duraci[oó]n\s*</dt>\s*<dd>.*?</dd>\s*</div>",
    re.IGNORECASE | re.DOTALL,
)

KNOWN_REPAIRS = {
    "Las precondiciones describen propiedades que deben cumplirse antes de ejecutar el algoritmo; las postcondiciones describen lo queda garantizado":
        "Las precondiciones describen propiedades que deben cumplirse antes de ejecutar el algoritmo; las postcondiciones describen lo que queda garantizado",
    "dos operadores verifican queda al menos una alícuota disponible":
        "dos operadores verifican que queda al menos una alícuota disponible",
    "menos torque una fuerza": "menos torque que una fuerza",
    "por lo quedan 18": "por lo que quedan 18",
    '"aprendizaje supervisado": "Enfoque ajusta un modelo':
        '"aprendizaje supervisado": "Enfoque que ajusta un modelo',
}


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True)


def changed_paths() -> list[Path]:
    names = git_output("diff", "--name-only", "origin/main...HEAD").splitlines()
    return [ROOT / name for name in names if name]


def base_text(relative: Path) -> str | None:
    try:
        return git_output("show", f"origin/main:{relative.as_posix()}")
    except subprocess.CalledProcessError:
        return None


def restore_connectives(path: Path, text: str) -> str:
    relative = path.relative_to(ROOT)
    original = base_text(relative)
    if original is not None:
        for line in original.splitlines(keepends=True):
            if not RISKY_BASE_LINE.search(line):
                continue
            damaged = line.replace("que que", "que").replace("Que que", "Que")
            if damaged != line and damaged in text and line not in text:
                text = text.replace(damaged, line)
    for damaged, corrected in KNOWN_REPAIRS.items():
        text = text.replace(damaged, corrected)
    return text


def strengthen_validator() -> None:
    path = ROOT / "scripts" / "validate_self_paced_model.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        'FORBIDDEN_UI = ("Carga estimada", "Tiempo sugerido", "horas estimadas", "horas semanales", "horas totales de estudio")',
        'FORBIDDEN_UI = ("Carga estimada", "Tiempo sugerido", "horas estimadas", "horas semanales", "horas totales de estudio")',
    )
    marker = 'DUPLICATE_QUE = re.compile(r"\\bque\\s+que\\b", re.IGNORECASE)\n'
    addition = (
        marker
        + 'COURSE_META = re.compile(r\'<dl[^>]*class="[^"]*course-meta[^"]*"[^>]*>(.*?)</dl>\', re.IGNORECASE | re.DOTALL)\n'
        + 'DURATION_LABEL = re.compile(r"<dt>\\s*Duraci[oó]n\\s*</dt>", re.IGNORECASE)\n'
        + 'STUDY_RANGE = re.compile(r"\\b\\d+(?:\\s*[–-]\\s*\\d+)?\\s*(?:horas?|semanas?)\\b", re.IGNORECASE)\n'
    )
    if "COURSE_META = re.compile" not in text:
        text = text.replace(marker, addition)

    marker2 = "        lowered = text.casefold()\n"
    addition2 = (
        marker2
        + '        if path.suffix.lower() == ".html":\n'
        + '            for meta_block in COURSE_META.findall(text):\n'
        + '                if DURATION_LABEL.search(meta_block) or STUDY_RANGE.search(meta_block):\n'
        + '                    errors.append(f"metadato temporal público en {path.relative_to(ROOT)}")\n'
    )
    if "for meta_block in COURSE_META.findall" not in text:
        text = text.replace(marker2, addition2)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    repaired = 0
    for path in changed_paths():
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        updated = restore_connectives(path, text)
        if path.suffix.lower() == ".html":
            updated = DURATION_META.sub("", updated)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            repaired += 1

    # The authored Bioinformatics unit was not initially part of the generated diff.
    authored = ROOT / "ingenieria-biomedica" / "bioinformatica" / "unidades" / "unidad-01.html"
    if authored.exists():
        text = authored.read_text(encoding="utf-8")
        updated = DURATION_META.sub("", restore_connectives(authored, text))
        if updated != text:
            authored.write_text(updated, encoding="utf-8")
            repaired += 1

    strengthen_validator()
    print(f"Archivos reparados: {repaired}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
