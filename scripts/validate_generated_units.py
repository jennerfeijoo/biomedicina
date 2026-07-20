#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
UNIT_ROOT = ROOT / "data" / "generated_units"
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("la raíz debe ser un objeto JSON")
    return data


def collect_text(value: Any, *, key: str = "") -> list[str]:
    if isinstance(value, str):
        if key == "url" or URL_RE.match(value):
            return []
        return [value]
    if isinstance(value, list):
        output: list[str] = []
        for item in value:
            output.extend(collect_text(item, key=key))
        return output
    if isinstance(value, dict):
        output = []
        for child_key, child in value.items():
            if child_key in {"schema_version", "subject_id", "area_id", "slug", "status"}:
                continue
            output.extend(collect_text(child, key=child_key))
        return output
    return []


def validate_unit(path: Path) -> int:
    data = load_json(path)
    required = {
        "schema_version",
        "subject_id",
        "area_id",
        "unit",
        "slug",
        "title",
        "status",
        "purpose",
        "learning_objectives",
        "theory_sections",
        "glossary",
        "worked_example",
        "guided_activity",
        "common_errors",
        "self_assessment",
        "biomedical_connections",
        "sources",
        "editorial_notice",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError("faltan campos: " + ", ".join(missing))

    subject_id = str(data["subject_id"])
    if path.parent.name != subject_id:
        raise ValueError("subject_id no coincide con la carpeta")
    match = re.fullmatch(r"unit-(\d{2})\.json", path.name)
    if not match or int(match.group(1)) != int(data["unit"]):
        raise ValueError("el número de unidad no coincide con el nombre del archivo")
    if data["status"] != "complete":
        raise ValueError("status debe ser complete")

    objectives = data["learning_objectives"]
    sections = data["theory_sections"]
    glossary = data["glossary"]
    self_assessment = data["self_assessment"]
    sources = data["sources"]
    if not isinstance(objectives, list) or len(objectives) < 4:
        raise ValueError("se requieren al menos cuatro objetivos")
    if not isinstance(sections, list) or len(sections) < 3:
        raise ValueError("se requieren al menos tres secciones teóricas")
    for index, section in enumerate(sections, start=1):
        if len(section.get("paragraphs", [])) < 3:
            raise ValueError(f"la sección teórica {index} necesita al menos tres párrafos")
        if len(section.get("key_points", [])) < 3:
            raise ValueError(f"la sección teórica {index} necesita al menos tres puntos clave")
    if not isinstance(glossary, list) or len(glossary) < 8:
        raise ValueError("se requieren al menos ocho términos de glosario")
    if not isinstance(self_assessment, list) or len(self_assessment) < 5:
        raise ValueError("se requieren al menos cinco preguntas de autoevaluación")
    if not isinstance(sources, list) or len(sources) < 3:
        raise ValueError("se requieren al menos tres fuentes")
    for source in sources:
        if not URL_RE.match(str(source.get("url") or "")):
            raise ValueError("todas las fuentes deben tener URL HTTP válida")

    text = " ".join(collect_text(data))
    words = len(WORD_RE.findall(text))
    if words < 900:
        raise ValueError(f"contenido insuficiente: {words} palabras")
    if words > 2300:
        raise ValueError(f"contenido excesivo para una unidad: {words} palabras")
    lowered = text.casefold()
    for marker in ("lorem ipsum", "contenido pendiente", "por completar", "placeholder"):
        if marker in lowered:
            raise ValueError(f"marcador incompleto detectado: {marker}")
    return words


def main() -> int:
    paths = sorted(UNIT_ROOT.glob("*/unit-*.json"))
    if not paths:
        print("No hay unidades generadas todavía.")
        return 0
    total_words = 0
    for path in paths:
        words = validate_unit(path)
        total_words += words
        print(f"OK {path.relative_to(ROOT)}: {words} palabras")
    print(f"Unidades válidas: {len(paths)} · {total_words} palabras")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
