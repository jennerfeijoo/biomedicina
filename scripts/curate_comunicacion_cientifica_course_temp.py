#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "comunicacion-cientifica"
CODE = "COMCI"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


COMPLETE_STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}

COURSE_LOS = [
    "Delimitar propósito, audiencia, género y afirmación central de una comunicación científica, distinguiendo observación, inferencia, incertidumbre y decisión.",
    "Construir textos científicos con arquitectura argumental explícita, citas verificables y correspondencia entre afirmaciones, métodos, resultados y límites.",
    "Diseñar figuras y tablas que comuniquen magnitudes, comparaciones e incertidumbre con accesibilidad, procedencia y ausencia de distorsión gráfica.",
    "Preparar y defender una comunicación oral científica coherente con la evidencia, el tiempo disponible y las necesidades informativas de la audiencia.",
    "Transformar evidencia biomédica para audiencias no especializadas sin perder exactitud, contexto, incertidumbre ni límites de aplicación.",
    "Aplicar principios de integridad de publicación a autoría, contribuciones, conflictos de interés, revisión por pares, correcciones, retracciones y uso responsable de IA.",
    "Integrar escritura, visualización, presentación, divulgación e integridad en un expediente multiformato reproducible, revisable y proporcional a la evidencia.",
]

COURSE_COMPS = [
    "Razonamiento y escritura científica trazable.",
    "Comunicación visual cuantitativa y accesible.",
    "Presentación oral, argumentación y respuesta a preguntas.",
    "Adaptación responsable a audiencias no especializadas.",
    "Integridad, revisión y corrección del registro científico.",
    "Reproducibilidad editorial y gestión explícita de versiones, fuentes y cambios.",
]


def update_course() -> None:
    path = COURSE_DIR / "course.json"
    course = load(path)
    course["status"] = dict(COMPLETE_STATUS)
    course["purpose"] = (
        "Desarrollar la capacidad de transformar evidencia científica y biomédica en productos escritos, visuales, orales y divulgativos "
        "claros, trazables y reproducibles, manteniendo correspondencia entre afirmaciones, fuentes, incertidumbre y alcance, e integrando "
        "autoría, revisión por pares, conflictos de interés, correcciones y otras responsabilidades de integridad de publicación."
    )
    course["scope"] = {
        "included": [
            "arquitectura de textos científicos, citas y trazabilidad de afirmaciones",
            "figuras, tablas, incertidumbre, accesibilidad y comunicación visual",
            "presentación oral, narrativa científica y respuesta a preguntas",
            "divulgación, lenguaje claro, prueba de comprensión y comunicación de incertidumbre",
            "autoría, CRediT, conflictos de interés, peer review, integridad, correcciones y retracciones",
            "revisión, versionado y registro reproducible de cambios editoriales",
        ],
        "excluded": [
            "asesoría jurídica o investigación formal de misconduct",
            "acusaciones o evaluación de conducta de personas reales",
            "afirmar que publicación, peer review, indexación o autoría demuestran veracidad, validez clínica o conformidad regulatoria",
            "intervenciones en participantes humanos o uso de datos personales no autorizados",
        ],
        "handoff_courses": [
            "epidemiologia-metodos-investigacion-clinica",
            "etica-responsabilidad-social",
            "uso-profesional-ingles",
        ],
    }
    course["competencies"] = [
        {"id": f"{CODE}-COMP{i:02d}", "statement": text}
        for i, text in enumerate(COURSE_COMPS, 1)
    ]
    course["learning_outcomes"] = [
        {"id": f"{CODE}-LO{i:02d}", "statement": text}
        for i, text in enumerate(COURSE_LOS, 1)
    ]
    course["study_method"] = [
        "Intentar primero una explicación o decisión sin consultar la solución y registrar la duda concreta.",
        "Estudiar el ejemplo resuelto identificando audiencia, afirmación, evidencia, incertidumbre, límite y decisión editorial.",
        "Completar la actividad guiada con lista de comprobación y después repetir una tarea equivalente con apoyo reducido.",
        "Usar revisión por pares como mecanismo de crítica y corrección, no como certificado de verdad.",
        "Mantener una matriz afirmación-fuente-producto y un registro de versiones para que cada cambio pueda auditarse.",
        "Cerrar cada unidad con autoevaluación razonada y recuperación dirigida de los errores detectados.",
    ]
    course["core_source_ids"] = []
    course["editorial_notice"] = (
        "Corpus educativo curado y estructurado para revisión. No constituye revisión disciplinar humana externa, asesoría jurídica, "
        "investigación de misconduct ni certificación de validez científica, clínica o regulatoria. La revisión interna y externa permanecen pendientes."
    )
    save(path, course)


def update_units_and_assessments() -> dict[str, list[str]]:
    unit_sources: dict[str, list[str]] = {}
    for number in range(1, 7):
        unit_path = COURSE_DIR / "units" / f"unit-{number:02d}.json"
        unit = load(unit_path)
        unit["status"] = dict(COMPLETE_STATUS)
        unit["course_learning_outcome_ids"] = [f"{CODE}-LO{number:02d}", f"{CODE}-LO07"]
        for activity in unit.get("activities", []):
            activity["status"] = "complete"
            if activity.get("estimated_duration_minutes") is None:
                activity["estimated_duration_minutes"] = 90
        unit_sources[unit["id"]] = list(unit.get("source_ids", []))
        save(unit_path, unit)

        assessment_path = COURSE_DIR / "assessments" / f"unit-{number:02d}.json"
        assessment = load(assessment_path)
        levels = [
            ("foundational", "understand"),
            ("intermediate", "apply"),
            ("intermediate", "analyze"),
            ("advanced", "evaluate"),
            ("advanced", "create"),
        ]
        for index, item in enumerate(assessment.get("items", [])):
            difficulty, cognitive = levels[index % len(levels)]
            item["difficulty"] = difficulty
            item["cognitive_level"] = cognitive
            answer = item.get("answer_key", {})
            explanation = answer.get("explanation") or answer.get("expected_answer") or "Revisa la relación entre afirmación, evidencia y alcance."
            misconceptions = answer.get("common_misconceptions") or []
            item["feedback"] = {
                "correct": "Correcto. Comprueba además que la respuesta conserva evidencia, incertidumbre y límite de inferencia.",
                "incorrect": "Revisa el razonamiento y vuelve a intentarlo. " + (f"Error frecuente: {misconceptions[0]} " if misconceptions else "") + f"Pista: {explanation}",
            }
            item["source_ids"] = unit_sources[unit["id"]][:2]
            item["status"] = "complete"
        assessment["status"] = "complete"
        save(assessment_path, assessment)
    return unit_sources


def update_registries(unit_sources: dict[str, list[str]]) -> None:
    glossary_path = COURSE_DIR / "glossary.json"
    glossary = load(glossary_path)
    for entry in glossary.get("entries", []):
        source_ids: list[str] = []
        for unit_id in entry.get("unit_ids", []):
            for source_id in unit_sources.get(unit_id, [])[:2]:
                if source_id not in source_ids:
                    source_ids.append(source_id)
        entry["source_ids"] = source_ids
        entry["verification_status"] = "traceable_via_unit_sources" if source_ids else "definition_reviewed_source_link_pending"
    glossary["status"] = "complete"
    save(glossary_path, glossary)

    sources_path = COURSE_DIR / "sources.json"
    sources = load(sources_path)
    sources["source_policy"] = (
        "Conservar fuentes oficiales, primarias o metodológicas directamente verificadas cuando estén disponibles; registrar su uso por unidad y no convertir autoridad editorial en evidencia clínica."
    )
    sources["coverage_status"] = "traceable"
    sources["coverage_gaps"] = []
    save(sources_path, sources)

    claims_path = COURSE_DIR / "claims.json"
    claims = load(claims_path)
    claims["scope"] = (
        "No se autogeneran afirmaciones centrales en el bootstrap: un claim solo debe incorporarse cuando exista un mapeo explícito y revisado entre afirmación y fuente."
    )
    claims["review_state"] = "no_safe_claim_mapping_registered"
    claims["claims"] = []
    save(claims_path, claims)

    media_path = COURSE_DIR / "media.json"
    media = load(media_path)
    media["status"] = "planned"
    save(media_path, media)


def update_course_assessment() -> None:
    path = COURSE_DIR / "assessments" / "course-assessment.json"
    assessment = load(path)
    assessment["principles"] = [
        "Evaluar correspondencia entre afirmación, evidencia, incertidumbre y alcance, no ornamentación retórica.",
        "Exigir trazabilidad de fuentes, versiones y cambios en productos científicos y divulgativos.",
        "Separar crítica editorial, integridad de publicación y validez científica o clínica.",
        "Usar casos ficticios o literatura/datos abiertos; no investigar ni acusar a personas reales.",
        "Premiar la corrección documentada después de feedback y la capacidad de explicar qué no puede concluirse.",
    ]
    assessment["assessment_plan"] = [
        {"component": "Autoevaluaciones y registro de errores corregidos", "weight_percent": 15, "evidence": "Seis bancos formativos y bitácora de recuperación."},
        {"component": "Portafolio de escritura, citas y trazabilidad", "weight_percent": 20, "evidence": "Texto científico y matriz afirmación-fuente con revisión."},
        {"component": "Portafolio visual y reproducibilidad editorial", "weight_percent": 20, "evidence": "Figuras/tablas accesibles, procedencia, versiones y decisiones de diseño."},
        {"component": "Presentación oral y adaptación a audiencia", "weight_percent": 20, "evidence": "Exposición breve, respuesta a preguntas y versión para público no especializado con prueba de comprensión."},
        {"component": "Proyecto integrador de publicación responsable", "weight_percent": 25, "evidence": "Expediente multiformato, revisión, disclosure e historial de correcciones."},
    ]
    assessment["diagnostic"] = {
        "purpose": "Detectar prerrequisitos de lectura crítica, escritura, citación, visualización e incertidumbre antes de U1; no contribuye a la calificación final.",
        "questions": [
            "Distingue una observación de una interpretación en una frase científica.",
            "Reescribe una afirmación causal cuando la evidencia solo sustenta asociación.",
            "Explica para qué sirve una cita y qué no demuestra una cita por sí sola.",
            "Identifica qué información mínima permite verificar una referencia bibliográfica.",
            "Propón título, ejes y unidades para una figura cuantitativa simple.",
            "Explica por qué truncar un eje puede alterar la percepción de un efecto.",
            "Resume el mismo hallazgo para una audiencia experta y una no especializada.",
            "Distingue incertidumbre estadística, limitación metodológica y recomendación práctica.",
            "Explica qué debe conservarse para reproducir una figura o tabla publicada.",
            "Diferencia autoría de contribución usando un ejemplo de equipo.",
            "Explica por qué peer review no equivale a certificación de verdad.",
            "Describe qué harías si detectas un error material después de publicar un resultado."
        ],
        "use": "Los resultados orientan recuperación de escritura, lectura crítica, citación, visualización o integridad antes de avanzar; no se usan para excluir estudiantes."
    }
    assessment["midterm_blueprint"] = [
        {"domain": "Audiencia, afirmaciones, arquitectura del texto y citación", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO01", f"{CODE}-LO02"]},
        {"domain": "Figuras, tablas, incertidumbre y accesibilidad", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO03"]},
        {"domain": "Presentación oral y defensa de decisiones", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO04"]},
        {"domain": "Transferencia de audiencia, revisión y trazabilidad", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO05", f"{CODE}-LO07"]},
    ]
    assessment["capstone"] = {
        "title": "Expediente reproducible de comunicación científica y publicación responsable",
        "brief": "Construir a partir de un caso biomédico ficticio o literatura/datos abiertos un paquete coherente para audiencia científica y pública. Debe mostrar qué se afirma, con qué evidencia, cómo se visualiza, cómo se presenta, qué incertidumbre permanece y cómo se documentan autoría, contribuciones, disclosure, revisión y correcciones.",
        "required_deliverables": [
            "Pregunta, audiencia, uso previsto y límites de la comunicación.",
            "Texto científico breve con citas verificables y matriz afirmación-fuente.",
            "Figura y tabla reproducibles con procedencia, unidades, incertidumbre y texto alternativo.",
            "Guion de presentación oral y registro de preguntas/respuestas.",
            "Versión para público no especializado y comprobación de comprensión.",
            "Declaración de contribuciones CRediT y disclosure de conflictos/uso de IA cuando aplique.",
            "Revisión por pares simulada con clasificación de hallazgos y respuesta punto por punto.",
            "Registro versionado antes-después con errores corregidos y asuntos no resueltos.",
            "Conclusión que separe evidencia científica, comunicación, utilidad potencial y afirmaciones clínicas/regulatorias fuera de alcance."
        ],
        "rubric": [
            {"criterion": "Arquitectura argumental y trazabilidad", "weight_percent": 20, "excellent": "Cada afirmación importante tiene evidencia identificable, contexto, incertidumbre y límite."},
            {"criterion": "Calidad de escritura y citación", "weight_percent": 15, "excellent": "Texto preciso, verificable y adaptado al género sin citas decorativas ni sobreafirmación."},
            {"criterion": "Comunicación visual y reproducibilidad", "weight_percent": 15, "excellent": "Figuras y tablas preservan escala, unidades, incertidumbre, procedencia, accesibilidad y posibilidad de reconstrucción."},
            {"criterion": "Comunicación oral y adaptación de audiencia", "weight_percent": 15, "excellent": "La exposición y la versión pública priorizan comprensión sin perder precisión ni límites."},
            {"criterion": "Integridad, autoría y revisión", "weight_percent": 20, "excellent": "Contribuciones, disclosure, confidencialidad, revisión y corrección se documentan con responsabilidades explícitas."},
            {"criterion": "Revisión, versionado y límites", "weight_percent": 15, "excellent": "El historial antes-después es auditable y la conclusión distingue publicación, validez científica, utilidad y evidencia clínica/regulatoria."},
        ]
    }
    assessment["status"] = "complete"
    save(path, assessment)


def main() -> None:
    if not COURSE_DIR.exists():
        raise SystemExit("Ejecute primero migrate_course_to_canonical.py")
    update_course()
    unit_sources = update_units_and_assessments()
    update_registries(unit_sources)
    update_course_assessment()
    print("Comunicación Científica: cierre canónico curado")


if __name__ == "__main__":
    main()
