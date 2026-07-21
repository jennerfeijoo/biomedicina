#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CHUNK_DIR = ROOT / ".citonauta-agent" / "payloads" / "aed"
DEST_DIR = ROOT / "data" / "generated_units" / "algoritmos-estructuras-datos"
EXPECTED_SHA256 = "02e130c49ed6798842797b6879eb22c653e2d6d0b0d7f24799ab77c76f74d27f"
SUBJECT_ID = "algoritmos-estructuras-datos"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)
FORBIDDEN = (
    "contenido desarrollado",
    "unidades desarrolladas",
    "ejemplo desarrollado",
    "en revisión académica",
    "pendiente de ampliación",
    "generado automáticamente",
)
TITLES = {
    1: "Pensamiento algorítmico",
    2: "Complejidad y eficiencia",
    3: "Estructuras lineales",
    4: "Árboles y grafos",
    5: "Ordenamiento y búsqueda",
    6: "Diseño, pruebas y reproducibilidad",
}
WEEKS = {
    1: [1, 2],
    2: [3, 4, 5],
    3: [6, 7, 8],
    4: [9, 10, 11],
    5: [12, 13],
    6: [14, 15, 16],
}
HOURS = {1: 16, 2: 24, 3: 24, 4: 24, 5: 16, 6: 24}


def normalized(value: str) -> str:
    return " ".join(value.casefold().split())


def domain(url: str) -> str:
    return urlparse(url).netloc.casefold().removeprefix("www.")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_unit(data: dict, number: int) -> None:
    prefix = f"unit-{number:02d}"
    require(data.get("schema_version") == "2.0", f"{prefix}: schema_version")
    require(data.get("subject_id") == SUBJECT_ID, f"{prefix}: subject_id")
    require(data.get("area_id") == "ciencias-basicas", f"{prefix}: area_id")
    require(data.get("status") == "review", f"{prefix}: status")
    require(data.get("unit") == number, f"{prefix}: número")
    require(data.get("title") == TITLES[number], f"{prefix}: título")
    require(data.get("weeks") == WEEKS[number], f"{prefix}: semanas")
    require(data.get("estimated_hours") == HOURS[number], f"{prefix}: horas")
    require(len(data.get("learning_objectives", [])) >= 8, f"{prefix}: objetivos")
    theory = data.get("theory_sections", [])
    require(len(theory) >= 4, f"{prefix}: secciones teóricas")
    require(all(len(section.get("paragraphs", [])) >= 4 for section in theory), f"{prefix}: profundidad teórica")
    require(sum(len(section.get("equations", [])) for section in theory) >= 1, f"{prefix}: ecuaciones MathJax")
    require(len(data.get("glossary", [])) >= 10, f"{prefix}: glosario")
    require(len(data.get("worked_examples", [])) >= 2, f"{prefix}: ejemplos")
    require(len(data.get("guided_activities", [])) >= 1, f"{prefix}: actividad guiada")
    require(len(data.get("practice_sets", [])) >= 3, f"{prefix}: práctica escalonada")
    require(sum(len(item.get("problems", [])) for item in data.get("practice_sets", [])) >= 12, f"{prefix}: problemas")
    require(len(data.get("common_errors", [])) >= 6, f"{prefix}: errores frecuentes")
    require(len(data.get("self_assessment", [])) >= 10, f"{prefix}: autoevaluación")
    require(len(data.get("biomedical_connections", [])) >= 4, f"{prefix}: conexiones biomédicas")
    sources = data.get("sources", [])
    require(len(sources) >= 5, f"{prefix}: fuentes")
    urls = [str(item.get("url", "")) for item in sources]
    require(len(urls) == len(set(urls)), f"{prefix}: fuentes duplicadas")
    require(len({domain(url) for url in urls if domain(url)}) >= 3, f"{prefix}: dominios de fuentes")
    glossary = [normalized(str(item.get("term", ""))) for item in data.get("glossary", [])]
    questions = [normalized(str(item.get("question", ""))) for item in data.get("self_assessment", [])]
    require(len(glossary) == len(set(glossary)), f"{prefix}: glosario duplicado")
    require(len(questions) == len(set(questions)), f"{prefix}: preguntas duplicadas")
    serialized = json.dumps(data, ensure_ascii=False)
    require(len(WORD_RE.findall(serialized)) >= 2200, f"{prefix}: extensión insuficiente")
    lowered = serialized.casefold()
    for phrase in FORBIDDEN:
        require(phrase not in lowered, f"{prefix}: frase interna prohibida: {phrase}")
    notice = str(data.get("editorial_notice", "")).casefold()
    require("revisión docente experta" in notice, f"{prefix}: aviso editorial")
    clinical_limits = (
        "no constituyen software clínico validado",
        "no constituyen validación de software clínico",
    )
    require(any(phrase in notice for phrase in clinical_limits), f"{prefix}: límite clínico")


def main() -> int:
    chunks = sorted(CHUNK_DIR.glob("chunk-*.txt"))
    require(len(chunks) == 9, f"se esperaban 9 fragmentos y se encontraron {len(chunks)}")
    encoded = "".join(path.read_text(encoding="utf-8").strip() for path in chunks)
    payload = base64.b64decode(encoded, validate=True)
    actual_sha = hashlib.sha256(payload).hexdigest()
    require(actual_sha == EXPECTED_SHA256, f"SHA-256 inesperado: {actual_sha}")

    expected_members = {
        f"data/generated_units/{SUBJECT_ID}/unit{number:02d}.json"
        for number in range(1, 7)
    }
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        members = set(archive.namelist())
        require(members == expected_members, f"miembros inesperados: {sorted(members ^ expected_members)}")
        validated: list[tuple[int, dict]] = []
        for number in range(1, 7):
            member = f"data/generated_units/{SUBJECT_ID}/unit{number:02d}.json"
            data = json.loads(archive.read(member).decode("utf-8"))
            require(isinstance(data, dict), f"unit-{number:02d}: raíz no es objeto")
            validate_unit(data, number)
            validated.append((number, data))

    require(sum(data["estimated_hours"] for _, data in validated) == 128, "horas totales")
    all_weeks = [week for _, data in validated for week in data["weeks"]]
    require(sorted(all_weeks) == list(range(1, 17)), "cobertura semanal")

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    for number, data in validated:
        destination = DEST_DIR / f"unit-{number:02d}.json"
        destination.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Materializado y validado: {destination.relative_to(ROOT)}")
    print(f"Paquete verificado: sha256={actual_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
