#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = ROOT / "data" / "course_redevelopment"

PATCHES: dict[str, dict[str, Any]] = {
    "bioinformatica": {
        "questions": [
            {
                "question": "¿Por qué una accesión y su versión no deben tratarse como equivalentes?",
                "answer": "La accesión identifica un registro; la versión identifica un estado concreto de su contenido. Omitir la versión impide reconstruir con precisión qué secuencia o anotación fue utilizada.",
            },
            {
                "question": "¿Por qué las lecturas de secuenciación no son réplicas biológicas?",
                "answer": "Las lecturas son observaciones técnicas derivadas de una muestra. La replicación biológica requiere unidades independientes del proceso o intervención que se estudia.",
            },
            {
                "question": "¿Qué expresa una puntuación Phred?",
                "answer": "Expresa en escala logarítmica una probabilidad estimada de error; su interpretación depende de que la puntuación esté adecuadamente calibrada.",
            },
            {
                "question": "¿Qué elementos deben fijarse para que un pipeline pueda reproducirse?",
                "answer": "Datos y referencias versionados, software y entorno, parámetros, metadatos, semillas cuando correspondan, controles, logs y procedencia de cada artefacto.",
            },
        ],
        "interpretation": [
            "8–10 respuestas correctas: preparación suficiente para iniciar el curso.",
            "5–7: realizar nivelación paralela en biología molecular, programación, estadística y reproducibilidad.",
            "0–4: reforzar prerrequisitos antes de abordar las unidades avanzadas.",
        ],
        "resources": [
            {
                "title": "Bioconductor Workflows",
                "organization": "Bioconductor",
                "url": "https://bioconductor.org/help/workflows/",
                "type": "workflows reproducibles",
                "verification_status": "verified_directly",
            },
            {
                "title": "GATK Documentation and Best Practices",
                "organization": "Broad Institute",
                "url": "https://gatk.broadinstitute.org/hc/en-us",
                "type": "documentación oficial de genómica",
                "verification_status": "verified_directly",
            },
            {
                "title": "Nextflow Documentation",
                "organization": "Nextflow / Seqera",
                "url": "https://www.nextflow.io/docs/latest/",
                "type": "documentación de workflows",
                "verification_status": "verified_directly",
            },
        ],
    },
    "fisiologia-humana-i": {
        "questions": [
            {
                "question": "¿En qué se diferencia un estado estacionario de un equilibrio?",
                "answer": "En estado estacionario una variable permanece aproximadamente constante porque entradas y salidas se compensan; en equilibrio no existe una fuerza neta que sostenga un flujo.",
            },
            {
                "question": "¿Qué es una fuerza impulsora fisiológica?",
                "answer": "Es una diferencia de potencial químico, eléctrico, de presión o concentración que puede producir transporte o flujo cuando existe una vía conductora.",
            },
            {
                "question": "¿Por qué flujo y concentración no son magnitudes intercambiables?",
                "answer": "La concentración describe cantidad por volumen, mientras el flujo describe cantidad transferida por unidad de tiempo; pueden cambiar de forma independiente según volumen, conductancia y gradiente.",
            },
            {
                "question": "¿Por qué un rango de referencia no establece por sí solo un diagnóstico?",
                "answer": "Describe una distribución en una población y método concretos. La interpretación individual requiere contexto, calidad de medición, probabilidad previa, síntomas, mecanismos y evidencia adicional.",
            },
        ],
        "interpretation": [
            "8–10 respuestas correctas: preparación suficiente para iniciar el curso.",
            "5–7: realizar nivelación paralela en biología celular, anatomía, química, álgebra y lectura de gráficos.",
            "0–4: reforzar prerrequisitos antes de abordar integración fisiológica cuantitativa.",
        ],
        "resources": [
            {
                "title": "APS Learning Center",
                "organization": "American Physiological Society",
                "url": "https://learning.physiology.org/",
                "type": "recursos educativos de fisiología",
                "verification_status": "verified_directly",
            },
            {
                "title": "Physiology, Skeletal Muscle",
                "organization": "NCBI Bookshelf",
                "url": "https://www.ncbi.nlm.nih.gov/books/NBK537139/",
                "type": "revisión educativa",
                "verification_status": "verified_directly",
            },
            {
                "title": "Physiology, Pulmonary Ventilation and Perfusion",
                "organization": "NCBI Bookshelf",
                "url": "https://www.ncbi.nlm.nih.gov/books/NBK539907/",
                "type": "revisión educativa",
                "verification_status": "verified_directly",
            },
        ],
    },
}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: la raíz debe ser un objeto")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_course(subject_id: str, patch: dict[str, Any]) -> None:
    path = COURSE_ROOT / subject_id / "course.json"
    course = load_json(path)

    diagnostic = course.setdefault("diagnostic_assessment", {})
    questions = diagnostic.setdefault("questions", [])
    existing_questions = {
        str(item.get("question") or "").strip()
        for item in questions
        if isinstance(item, dict)
    }
    for item in patch["questions"]:
        if item["question"] not in existing_questions:
            questions.append(item)
    diagnostic["interpretation"] = patch["interpretation"]

    resources = course.setdefault("core_resources", [])
    existing_urls = {
        str(item.get("url") or "").strip()
        for item in resources
        if isinstance(item, dict)
    }
    for item in patch["resources"]:
        if item["url"] not in existing_urls:
            resources.append(item)

    if len(questions) < 10:
        raise ValueError(f"{subject_id}: diagnóstico incompleto ({len(questions)}/10)")
    if len(resources) < 8:
        raise ValueError(f"{subject_id}: recursos centrales incompletos ({len(resources)}/8)")

    write_json(path, course)
    print(
        f"[ok] {subject_id}: diagnóstico={len(questions)} preguntas; "
        f"recursos centrales={len(resources)}"
    )


def main() -> int:
    for subject_id, patch in PATCHES.items():
        patch_course(subject_id, patch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
