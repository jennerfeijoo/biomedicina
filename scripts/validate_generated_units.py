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
        output: list[str] = []
        for child_key, child in value.items():
            if child_key in {"schema_version", "subject_id", "area_id", "slug", "status"}:
                continue
            output.extend(collect_text(child, key=child_key))
        return output
    return []


def as_list(data: dict[str, Any], singular: str, plural: str) -> list[Any]:
    plural_value = data.get(plural)
    if isinstance(plural_value, list):
        return plural_value
    singular_value = data.get(singular)
    return [singular_value] if isinstance(singular_value, dict) else []


def practice_count(data: dict[str, Any]) -> int:
    total = 0
    for activity in as_list(data, "guided_activity", "guided_activities"):
        if not isinstance(activity, dict):
            continue
        for key in ("problems", "tasks", "exercises"):
            if isinstance(activity.get(key), list):
                total += len(activity[key])
    for practice_set in data.get("practice_sets", []):
        if isinstance(practice_set, dict) and isinstance(practice_set.get("problems"), list):
            total += len(practice_set["problems"])
    return total


def validate_common(path: Path, data: dict[str, Any]) -> None:
    required = {
        "schema_version", "subject_id", "area_id", "unit", "slug", "title",
        "status", "purpose", "learning_objectives", "theory_sections", "glossary",
        "common_errors", "self_assessment", "biomedical_connections", "sources",
        "editorial_notice",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError("faltan campos: " + ", ".join(missing))
    if not as_list(data, "worked_example", "worked_examples"):
        raise ValueError("falta worked_example o worked_examples")
    if not as_list(data, "guided_activity", "guided_activities"):
        raise ValueError("falta guided_activity o guided_activities")

    subject_id = str(data["subject_id"])
    if path.parent.name != subject_id:
        raise ValueError("subject_id no coincide con la carpeta")
    match = re.fullmatch(r"unit-(\d{2})\.json", path.name)
    if not match or int(match.group(1)) != int(data["unit"]):
        raise ValueError("el número de unidad no coincide con el nombre del archivo")

    for source in data["sources"]:
        if not URL_RE.match(str(source.get("url") or "")):
            raise ValueError("todas las fuentes deben tener URL HTTP válida")

    text = " ".join(collect_text(data)).casefold()
    for marker in ("lorem ipsum", "contenido pendiente", "por completar", "placeholder"):
        if marker in text:
            raise ValueError(f"marcador incompleto detectado: {marker}")


def validate_transitional(data: dict[str, Any]) -> None:
    if data["status"] != "complete":
        raise ValueError("en schema 1.0, status debe ser complete")
    if len(data["learning_objectives"]) < 4:
        raise ValueError("se requieren al menos cuatro objetivos")
    if len(data["theory_sections"]) < 3:
        raise ValueError("se requieren al menos tres secciones teóricas")
    for index, section in enumerate(data["theory_sections"], start=1):
        if len(section.get("paragraphs", [])) < 3:
            raise ValueError(f"la sección teórica {index} necesita al menos tres párrafos")
        if len(section.get("key_points", [])) < 3:
            raise ValueError(f"la sección teórica {index} necesita al menos tres puntos clave")
    if len(data["glossary"]) < 8:
        raise ValueError("se requieren al menos ocho términos de glosario")
    if len(data["self_assessment"]) < 5:
        raise ValueError("se requieren al menos cinco preguntas de autoevaluación")
    if len(data["sources"]) < 3:
        raise ValueError("se requieren al menos tres fuentes")


def validate_semester(data: dict[str, Any]) -> None:
    if data["status"] not in {"review", "complete"}:
        raise ValueError("en schema 2.0, status debe ser review o complete")
    if int(data.get("estimated_hours", 0) or 0) < 12:
        raise ValueError("schema 2.0 requiere al menos 12 horas estimadas")
    if not isinstance(data.get("weeks"), list) or not data["weeks"]:
        raise ValueError("schema 2.0 requiere semanas asignadas")
    if len(data["learning_objectives"]) < 5:
        raise ValueError("schema 2.0 requiere al menos cinco objetivos")
    if len(data["theory_sections"]) < 4:
        raise ValueError("schema 2.0 requiere al menos cuatro secciones teóricas")
    for index, section in enumerate(data["theory_sections"], start=1):
        if len(section.get("paragraphs", [])) < 4:
            raise ValueError(f"la sección teórica {index} necesita al menos cuatro párrafos")
        if len(section.get("key_points", [])) < 4:
            raise ValueError(f"la sección teórica {index} necesita al menos cuatro puntos clave")
    if len(data["glossary"]) < 12:
        raise ValueError("schema 2.0 requiere al menos doce términos de glosario")
    if len(as_list(data, "worked_example", "worked_examples")) < 2:
        raise ValueError("schema 2.0 requiere al menos dos ejemplos")
    if len(data["common_errors"]) < 5:
        raise ValueError("schema 2.0 requiere al menos cinco errores frecuentes")
    if len(data["self_assessment"]) < 8:
        raise ValueError("schema 2.0 requiere al menos ocho preguntas de autoevaluación")
    if len(data["sources"]) < 5:
        raise ValueError("schema 2.0 requiere al menos cinco fuentes")
    if practice_count(data) < 8:
        raise ValueError("schema 2.0 requiere al menos ocho problemas o tareas")


def validate_unit(path: Path) -> int:
    data = load_json(path)
    validate_common(path, data)
    words = len(WORD_RE.findall(" ".join(collect_text(data))))
    schema = str(data.get("schema_version"))
    if schema == "1.0":
        validate_transitional(data)
    elif schema == "2.0":
        validate_semester(data)
    else:
        raise ValueError(f"schema_version no soportado: {schema}")
    return words


def main() -> int:
    paths = sorted(UNIT_ROOT.glob("*/unit-*.json"))
    if not paths:
        print("No hay unidades generadas todavía.")
        return 0

    total_words = 0
    valid_count = 0
    errors: list[str] = []
    for path in paths:
        try:
            total_words += validate_unit(path)
            valid_count += 1
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            errors.append(f"ERROR {path.relative_to(ROOT)}: {error}")

    if errors:
        print("\n".join(errors))
        print(f"Validación fallida: {len(errors)} archivo(s) con errores · {valid_count} válidos")
        return 1

    print(f"Unidades válidas: {valid_count} · extensión descriptiva={total_words} palabras")
    print("La extensión no determina completitud ni impone límites máximos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
