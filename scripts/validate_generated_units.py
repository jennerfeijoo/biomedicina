#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
UNIT_ROOT = ROOT / "data" / "generated_units"
REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"
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
    """Cuenta únicamente problemas y tareas para el contrato genérico existente."""
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


def reconstruction_activity_count(data: dict[str, Any]) -> int:
    """Cuenta el diseño completo de actividades de una reconstrucción trazable."""
    total = 0
    for activity in as_list(data, "guided_activity", "guided_activities"):
        if not isinstance(activity, dict):
            continue
        for key in (
            "instructions",
            "problems",
            "tasks",
            "exercises",
            "deliverables",
            "checking_criteria",
        ):
            value = activity.get(key)
            if isinstance(value, list):
                total += len([item for item in value if str(item).strip()])
    for practice_set in data.get("practice_sets", []):
        if not isinstance(practice_set, dict):
            continue
        for key in ("problems", "tasks", "exercises"):
            value = practice_set.get(key)
            if isinstance(value, list):
                total += len([item for item in value if str(item).strip()])
    return total


def normalize_prose(value: Any) -> str:
    return " ".join(str(value or "").split()).casefold()


def word_count(value: Any) -> int:
    return len(WORD_RE.findall(str(value or "")))


def has_bibliographic_locator(source: dict[str, Any]) -> bool:
    url = str(source.get("url") or "").strip()
    if URL_RE.match(url):
        return True
    if any(str(source.get(key) or "").strip() for key in ("doi", "pmid", "isbn")):
        return True
    citation = str(source.get("citation") or "").strip()
    verification = str(source.get("verification_status") or "").strip()
    return len(citation) >= 40 and bool(verification)


def validate_common(
    path: Path,
    data: dict[str, Any],
    *,
    allow_bibliographic_locators: bool = False,
) -> None:
    required = {
        "schema_version", "subject_id", "area_id", "unit", "slug", "title",
        "status", "purpose", "learning_objectives", "theory_sections", "glossary",
        "common_errors", "self_assessment", "biomedical_connections", "sources",
        "editorial_notice",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError("faltan campos: " + ", ".join(missing))
    forbidden_time_fields = sorted({"estimated_hours", "weeks"} & data.keys())
    if forbidden_time_fields:
        raise ValueError("metadatos temporales no permitidos: " + ", ".join(forbidden_time_fields))
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
        if URL_RE.match(str(source.get("url") or "")):
            continue
        if allow_bibliographic_locators and has_bibliographic_locator(source):
            continue
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


def validate_course(data: dict[str, Any]) -> None:
    """Mantiene el contrato genérico existente para unidades schema 2.0."""
    if data["status"] not in {"review", "complete"}:
        raise ValueError("en schema 2.0, status debe ser review o complete")
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


def redevelopment_source_path(path: Path, data: dict[str, Any]) -> Path:
    return REDEVELOPMENT_ROOT / str(data["subject_id"]) / "units" / path.name


def is_exact_redevelopment_mirror(path: Path, data: dict[str, Any]) -> bool:
    source = redevelopment_source_path(path, data)
    return source.exists() and source.read_bytes() == path.read_bytes()


def validate_redevelopment_mirror(path: Path, data: dict[str, Any]) -> None:
    """Valida una copia exacta de una reconstrucción académica trazable.

    Este perfil no altera el contrato genérico. Evalúa estructura mínima por
    sección, densidad teórica agregada, unicidad, evaluación y actividad completa.
    """
    source = redevelopment_source_path(path, data)
    if not source.exists() or source.read_bytes() != path.read_bytes():
        raise ValueError("la unidad no es una copia exacta de course_redevelopment")
    if data["status"] not in {"review", "complete"}:
        raise ValueError("la reconstrucción debe conservar status review o complete")
    if len(data["learning_objectives"]) < 5:
        raise ValueError("la reconstrucción requiere al menos cinco objetivos")

    sections = data["theory_sections"]
    if len(sections) < 4:
        raise ValueError("la reconstrucción requiere al menos cuatro secciones teóricas")

    seen_paragraphs: set[str] = set()
    seen_key_points: set[str] = set()
    theory_words = 0
    for index, section in enumerate(sections, start=1):
        paragraphs = section.get("paragraphs", [])
        key_points = section.get("key_points", [])
        if len(paragraphs) < 3:
            raise ValueError(f"la sección teórica {index} necesita al menos tres párrafos")
        if len(key_points) < 3:
            raise ValueError(f"la sección teórica {index} necesita al menos tres puntos clave")

        for paragraph_number, paragraph in enumerate(paragraphs, start=1):
            count = word_count(paragraph)
            theory_words += count
            if count < 30:
                raise ValueError(
                    f"la sección {index}, párrafo {paragraph_number}, tiene {count} palabras; mínimo 30"
                )
            marker = normalize_prose(paragraph)
            if marker in seen_paragraphs:
                raise ValueError(f"párrafo teórico duplicado en la sección {index}")
            seen_paragraphs.add(marker)

        for point_number, point in enumerate(key_points, start=1):
            if word_count(point) < 4:
                raise ValueError(
                    f"la sección {index}, punto clave {point_number}, es demasiado breve"
                )
            marker = normalize_prose(point)
            if marker in seen_key_points:
                raise ValueError(f"punto clave duplicado en la sección {index}")
            seen_key_points.add(marker)

    if theory_words < 750:
        raise ValueError(f"desarrollo teórico insuficiente: {theory_words} palabras; mínimo 750")
    if len(data["glossary"]) < 12:
        raise ValueError("la reconstrucción requiere al menos doce términos de glosario")
    if len(as_list(data, "worked_example", "worked_examples")) < 2:
        raise ValueError("la reconstrucción requiere al menos dos ejemplos")
    if len(data["common_errors"]) < 5:
        raise ValueError("la reconstrucción requiere al menos cinco errores frecuentes")
    if len(data["self_assessment"]) < 8:
        raise ValueError("la reconstrucción requiere al menos ocho preguntas de autoevaluación")
    if len(data["sources"]) < 5:
        raise ValueError("la reconstrucción requiere al menos cinco fuentes")
    activity_items = reconstruction_activity_count(data)
    if activity_items < 8:
        raise ValueError(
            f"la reconstrucción requiere al menos ocho elementos de actividad; contiene {activity_items}"
        )


def validate_unit(path: Path) -> tuple[int, bool]:
    data = load_json(path)
    schema = str(data.get("schema_version"))
    mirrored = schema == "2.0" and is_exact_redevelopment_mirror(path, data)
    validate_common(path, data, allow_bibliographic_locators=mirrored)
    words = len(WORD_RE.findall(" ".join(collect_text(data))))
    if schema == "1.0":
        validate_transitional(data)
    elif schema == "2.0":
        if mirrored:
            validate_redevelopment_mirror(path, data)
        else:
            validate_course(data)
    else:
        raise ValueError(f"schema_version no soportado: {schema}")
    return words, mirrored


def main() -> int:
    paths = sorted(UNIT_ROOT.glob("*/unit-*.json"))
    if not paths:
        print("No hay unidades generadas todavía.")
        return 0

    total_words = 0
    valid_count = 0
    mirrored_count = 0
    errors: list[str] = []
    for path in paths:
        try:
            words, mirrored = validate_unit(path)
            total_words += words
            valid_count += 1
            mirrored_count += int(mirrored)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            errors.append(f"ERROR {path.relative_to(ROOT)}: {error}")

    if errors:
        print("\n".join(errors))
        print(f"Validación fallida: {len(errors)} archivo(s) con errores · {valid_count} válidos")
        return 1

    print(
        f"Unidades válidas: {valid_count} · reconstrucciones trazables={mirrored_count} · "
        f"extensión descriptiva={total_words} palabras"
    )
    print("La extensión no determina completitud ni impone límites máximos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
