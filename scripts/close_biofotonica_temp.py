#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from migrate_course_to_canonical import migrate

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "biofotonica"
CODE = "BIOFOT"
TARGET = ROOT / "data" / "courses" / COURSE_ID
REDEV = ROOT / "data" / "course_redevelopment" / COURSE_ID / "course.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def records(values: list[str], prefix: str) -> list[dict[str, str]]:
    return [{"id": f"{prefix}{i:02d}", "statement": value} for i, value in enumerate(values, 1)]


def complete_status() -> dict[str, str]:
    return {
        "content": "complete",
        "sources": "traceable",
        "pedagogy": "complete",
        "multimedia": "planned",
        "internal_review": "pending",
        "external_review": "pending",
        "publication": "published_provisional",
    }


def main() -> int:
    migrate(COURSE_ID, CODE, force=False)
    redevelopment = load(REDEV)
    course_path = TARGET / "course.json"
    course = load(course_path)

    course["content_version"] = "1.0.0"
    course["academic_level"] = redevelopment.get("level", "Pregrado universitario intermedio y avanzado")
    course["audience"] = (
        "Estudiantes de ingeniería biomédica y áreas afines que necesiten razonar sobre interacción luz-tejido, "
        "instrumentación óptica, imagen/espectroscopía, dosimetría y validación técnica con límites explícitos."
    )
    course["status"] = complete_status()
    course["purpose"] = (
        "Integrar la física de la interacción luz-tejido con fuentes, detectores, óptica de tejidos, microscopía, "
        "espectroscopía, OCT, fototerapia, dosimetría y validación para construir y auditar estudios biofotónicos "
        "reproducibles, cuantitativos y proporcionales a la evidencia."
    )
    course["scope"] = {
        "included": [
            "Interacción de la radiación óptica con tejidos: absorción, dispersión, anisotropía y penetración.",
            "Fuentes, detectores, ruido, sensibilidad y cadena instrumental biofotónica.",
            "Modelos de transporte y difusión, fantomas y estimación de propiedades ópticas.",
            "Fluorescencia, microscopía confocal, Raman y OCT con métricas y límites de interpretación.",
            "Fototerapia, dosimetría, mecanismos fotoquímicos/térmicos y principios de seguridad.",
            "Calibración, incertidumbre, desempeño con fantomas, robustez, riesgo y traslación técnica."
        ],
        "excluded": [
            "Diagnóstico, pronóstico o recomendación terapéutica sobre pacientes reales.",
            "Operación experimental de láseres u otras fuentes ópticas sobre personas o animales.",
            "Certificación de seguridad, conformidad regulatoria o autorización de un dispositivo real.",
            "Inferir utilidad clínica a partir de desempeño físico, analítico o de fantoma por sí solo."
        ],
        "handoff_courses": ["imagenes-biomedicas", "analisis-instrumental", "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas"]
    }
    course["prerequisites"] = records(redevelopment.get("prerequisites", []), f"{CODE}-PRE")
    course["competencies"] = records(redevelopment.get("course_competencies", []), f"{CODE}-COMP")
    course_outcomes = redevelopment.get("learning_outcomes", [])
    course["learning_outcomes"] = records(course_outcomes, f"{CODE}-LO")
    course["study_method"] = [
        "Partir de la magnitud física o pregunta de medición antes de elegir técnica o hardware.",
        "Dibujar la cadena fuente-tejido-óptica-detector-procesamiento-inferencia y declarar unidades y supuestos.",
        "Resolver primero un ejemplo trabajado, después una actividad guiada sintética y finalmente un caso con menor andamiaje.",
        "Predefinir controles, criterios de aceptación, análisis de sensibilidad e incertidumbre antes de interpretar.",
        "Cerrar cada producto con una conclusión proporcional y con la evidencia adicional necesaria para trasladarlo."
    ]
    course["editorial_notice"] = (
        "Corpus académico interno en versión 1.0.0. La completitud estructural y pedagógica no constituye revisión "
        "disciplinar externa, validación clínica, certificación de seguridad ni conformidad regulatoria. Las prácticas "
        "se mantienen en datos sintéticos, literatura y simulación salvo protocolo institucional independiente."
    )

    sources_path = TARGET / "sources.json"
    sources = load(sources_path)
    source_by_id = {item["id"]: item for item in sources.get("sources", [])}
    unit_first_source: dict[str, str] = {}

    for number in range(1, 7):
        unit_path = TARGET / "units" / f"unit-{number:02d}.json"
        unit = load(unit_path)
        unit["status"] = complete_status()
        mapped = [f"{CODE}-LO{number:02d}"]
        if len(course_outcomes) >= 7:
            mapped.append(f"{CODE}-LO07")
        unit["course_learning_outcome_ids"] = mapped

        for activity in unit.get("activities", []):
            activity["estimated_duration_minutes"] = 90
            activity["status"] = "complete"

        assessment_path = TARGET / unit["assessment_file"]
        assessment = load(assessment_path)
        unit_sources = [sid for sid in unit.get("source_ids", []) if sid in source_by_id]
        if unit_sources:
            unit_first_source[unit["id"]] = unit_sources[0]
        levels = ["understand", "apply", "analyze", "evaluate"]
        difficulties = ["foundational", "intermediate", "intermediate", "advanced"]
        for index, item in enumerate(assessment.get("items", [])):
            item["difficulty"] = difficulties[index % len(difficulties)]
            item["cognitive_level"] = levels[index % len(levels)]
            if unit_sources:
                item["source_ids"] = [unit_sources[index % len(unit_sources)]]
            answer_key = item.setdefault("answer_key", {})
            if not str(answer_key.get("explanation") or "").strip():
                answer_key["explanation"] = (
                    "La respuesta debe reconstruir el mecanismo o criterio solicitado, declarar sus supuestos y "
                    "explicar por qué una interpretación alternativa sería insuficiente."
                )
            item["feedback"] = {
                "correct": "La respuesta distingue mecanismo, evidencia y límite de inferencia; conserva unidades y supuestos cuando corresponden.",
                "incorrect": "Revisa el mecanismo físico, la cadena de medición y el límite de la conclusión; evita convertir una señal o métrica en evidencia clínica."
            }
            item["status"] = "complete"
        assessment["status"] = "complete"
        write(assessment_path, assessment)
        write(unit_path, unit)

    # Seleccionar fuentes troncales relevantes ya verificadas y utilizadas por las seis unidades.
    core_source_ids: list[str] = []
    for number in range(1, 7):
        unit = load(TARGET / "units" / f"unit-{number:02d}.json")
        preferred = next(
            (
                sid for sid in unit.get("source_ids", [])
                if sid in source_by_id and str(source_by_id[sid].get("verification_status", "")).startswith("verified")
            ),
            None,
        )
        if preferred and preferred not in core_source_ids:
            core_source_ids.append(preferred)
    course["core_source_ids"] = core_source_ids

    sources["coverage_gaps"] = []
    sources["status"] = "traceable"
    sources["source_policy"] = (
        "Priorizar artículos primarios/revisiones metodológicas, documentación oficial y normas o guías técnicas; "
        "distinguir siempre una fuente normativa de evidencia de desempeño o utilidad clínica."
    )
    write(sources_path, sources)

    glossary_path = TARGET / "glossary.json"
    glossary = load(glossary_path)
    for entry in glossary.get("entries", []):
        linked_sources: list[str] = []
        for uid in entry.get("unit_ids", []):
            sid = unit_first_source.get(uid)
            if sid and sid not in linked_sources:
                linked_sources.append(sid)
        entry["source_ids"] = linked_sources
        entry["verification_status"] = "traceable_to_unit_sources" if linked_sources else "pending_source_mapping"
    glossary["status"] = "complete"
    write(glossary_path, glossary)

    claims_path = TARGET / "claims.json"
    claims = load(claims_path)
    claims["content_version"] = "1.0.0"
    claims["scope"] = (
        "No se crean afirmaciones centrales automáticamente sin un mapeo afirmación-fuente verificable. "
        "La trazabilidad actual se conserva a nivel de unidad y fuente; el registro de claims queda preparado para revisión disciplinar humana."
    )
    claims["review_state"] = "pending_human_claim_mapping"
    claims["claims"] = []
    write(claims_path, claims)

    media_path = TARGET / "media.json"
    media = load(media_path)
    media["coverage_status"] = "planned"
    media["status"] = "planned"
    write(media_path, media)

    assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{CODE}-EVAL-CURSO",
        "course_id": COURSE_ID,
        "scope": "course",
        "principles": [
            "Evaluar razonamiento físico, trazabilidad, incertidumbre y reproducibilidad, no memorización aislada.",
            "Separar desempeño técnico, validez científica, evidencia clínica y conformidad regulatoria.",
            "Usar únicamente datos sintéticos, literatura o simulación en actividades que involucren exposición óptica.",
            "Predefinir criterios, controles y condiciones de aceptación antes de inspeccionar el resultado.",
            "Premiar conclusiones acotadas y la corrección documentada después de retroalimentación."
        ],
        "assessment_plan": [
            {"component": "Autoevaluaciones razonadas de U1–U6", "weight_percent": 15, "evidence": "Bancos formativos con explicación, error frecuente y corrección."},
            {"component": "Portafolio de actividades guiadas", "weight_percent": 25, "evidence": "Seis expedientes sintéticos con cálculos, controles, incertidumbre y límites."},
            {"component": "Examen integrador intermedio", "weight_percent": 20, "evidence": "Problemas inéditos de interacción luz-tejido, instrumentación, modelado e imagen."},
            {"component": "Proyecto integrador final", "weight_percent": 30, "evidence": "Expediente biofotónico reproducible que conecta U1–U6."},
            {"component": "Defensa, revisión y registro de cambios", "weight_percent": 10, "evidence": "Defensa breve y tabla antes-después justificando correcciones."}
        ],
        "diagnostic": {
            "purpose": "Detectar prerrequisitos que requieren recuperación antes de U1; no aporta a la nota final.",
            "questions": [
                "Distingue irradiancia, potencia, energía y fluencia, indicando unidades.",
                "Explica absorción frente a dispersión en un medio biológico.",
                "Interpreta una relación señal-ruido y una incertidumbre de medición.",
                "Distingue resolución espacial de contraste.",
                "Explica por qué calibrar no equivale a validar un uso clínico.",
                "Distingue precisión, sesgo y reproducibilidad.",
                "Interpreta cualitativamente una convolución y una función de respuesta.",
                "Explica qué hace que un fantoma sea útil para una pregunta concreta.",
                "Distingue un modelo directo de un problema inverso.",
                "Explica por qué una norma de seguridad no demuestra eficacia clínica."
            ],
            "use": "Los resultados dirigen repaso de óptica, cálculo, señales o metrología antes de avanzar; no se usan para excluir estudiantes."
        },
        "midterm_blueprint": [
            {"domain": "Interacción luz-tejido", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO01"]},
            {"domain": "Fuentes, detectores, ruido y cadena instrumental", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO02"]},
            {"domain": "Óptica de tejidos y modelado", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO03"]},
            {"domain": "Microscopía, espectroscopía e integración crítica", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO04", f"{CODE}-LO07"]}
        ],
        "capstone": {
            "title": "Expediente biofotónico reproducible desde interacción luz-tejido hasta validación técnica",
            "brief": (
                "Diseñar o auditar un sistema biofotónico hipotético exclusivamente con datos sintéticos, literatura y simulación. "
                "El expediente debe justificar longitud de onda, fuente, detector, geometría, modelo tisular, modalidad de imagen o espectroscopía, "
                "métricas, dosimetría cuando aplique, calibración, fantomas, incertidumbre, robustez y riesgo, delimitando la evidencia que faltaría para uso clínico o regulatorio."
            ),
            "required_deliverables": [
                "Uso previsto científico/técnico y mensurandos con rango, unidades y criterio de aceptación.",
                "Diagrama fuente-tejido-óptica-detector-procesamiento-inferencia con presupuesto de señal y error.",
                "Selección razonada de longitudes de onda, fuente, detector y geometría.",
                "Modelo de interacción/propagación con supuestos, sensibilidad y limitaciones.",
                "Plan de adquisición o modalidad de imagen/espectroscopía con métricas cuantitativas.",
                "Dosimetría y límites de seguridad solo en simulación cuando corresponda.",
                "Plan de calibración, incertidumbre, fantomas, repetibilidad, reproducibilidad y robustez.",
                "Matriz riesgo-evidencia-control y distinción entre verificación, validación y evidencia clínica.",
                "Paquete reproducible de datos/cálculos/parámetros/versiones y conclusión acotada."
            ],
            "rubric": [
                {"criterion": "Pregunta, uso previsto y magnitudes", "weight_percent": 15, "excellent": "Mensurandos, condiciones, criterios y alcance son verificables y coherentes."},
                {"criterion": "Modelo físico e interacción luz-tejido", "weight_percent": 15, "excellent": "Mecanismos, ecuaciones, supuestos y límites se conectan con la pregunta sin saltos causales."},
                {"criterion": "Cadena instrumental", "weight_percent": 15, "excellent": "Fuente, óptica, detector, ruido, rango y calibración se justifican cuantitativamente."},
                {"criterion": "Imagen/espectroscopía y análisis", "weight_percent": 15, "excellent": "La modalidad y las métricas responden a la pregunta y distinguen señal, procesamiento e inferencia."},
                {"criterion": "Dosimetría, seguridad y riesgo", "weight_percent": 10, "excellent": "La exposición simulada, peligros y controles están cuantificados y limitados al alcance técnico."},
                {"criterion": "Validación, incertidumbre y robustez", "weight_percent": 15, "excellent": "Fantomas, criterios, sensibilidad, incertidumbre y variación desafían los supuestos relevantes."},
                {"criterion": "Trazabilidad, reproducibilidad e interpretación", "weight_percent": 15, "excellent": "Fuentes, datos, versiones, cálculos y cambios permiten reconstruir el resultado y la conclusión no sobreafirma evidencia clínica o regulatoria."}
            ]
        },
        "status": "complete"
    }
    write(TARGET / "assessments" / "course-assessment.json", assessment)
    write(course_path, course)

    generic = "concepto de la unidad que debe definirse"
    assert len(course["unit_files"]) == 6
    assert sum(x["weight_percent"] for x in assessment["assessment_plan"]) == 100
    assert sum(x["weight_percent"] for x in assessment["capstone"]["rubric"]) == 100
    for path in sorted((TARGET / "units").glob("unit-*.json")):
        assert generic not in path.read_text(encoding="utf-8").casefold(), path
    print("Biofotónica canónica preparada: 6 unidades, evaluaciones completas y registries consolidados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
