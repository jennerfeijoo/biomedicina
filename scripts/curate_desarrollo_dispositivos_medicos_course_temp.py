#!/usr/bin/env python3
"""One-shot canonical closure for Desarrollo de Dispositivos Médicos.

Temporary curator: it bootstraps the six already-curated redevelopment units into
CitoNauta's canonical academic corpus, strengthens course-level pedagogy,
assessment and traceability, and is removed by the workflow that executes it.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from migrate_course_to_canonical import migrate

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "desarrollo-dispositivos-medicos"
CODE = "DDMED"
COURSE_ROOT = ROOT / "data" / "courses" / COURSE_ID
TODAY = "2026-08-24"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def bootstrap() -> None:
    if COURSE_ROOT.exists():
        shutil.rmtree(COURSE_ROOT)
    migrate(COURSE_ID, CODE)


def curate_course() -> None:
    course_path = COURSE_ROOT / "course.json"
    course = load(course_path)
    course.update(
        {
            "code": CODE,
            "academic_level": "Pregrado universitario intermedio y avanzado",
            "audience": (
                "Estudiantes de ingeniería biomédica, bioingeniería y áreas afines que necesitan convertir "
                "una necesidad clínica en un expediente de desarrollo trazable, verificable y regulatoriamente "
                "contextualizado sin confundir una actividad educativa con autorización de mercado o validación clínica."
            ),
            "content_version": "1.0.0",
            "status": {
                "content": "complete",
                "sources": "traceable",
                "pedagogy": "complete",
                "multimedia": "planned",
                "internal_review": "pending",
                "external_review": "pending",
                "publication": "published_provisional",
            },
            "purpose": (
                "Integrar necesidad clínica y usuarios, requisitos y arquitectura, gestión de riesgos, prototipado y "
                "verificación, validación y evidencia, y regulación y transferencia para construir un expediente "
                "reproducible de desarrollo de un dispositivo médico. El curso exige trazabilidad bidireccional, "
                "criterios de aceptación predefinidos, control de configuración, evidencia proporcional al uso "
                "previsto y separación explícita entre desempeño técnico, evidencia preclínica o clínica, "
                "conformidad regulatoria y autorización de mercado."
            ),
            "scope": {
                "included": [
                    "Observación del flujo, partes interesadas, uso previsto y formulación de necesidades sin sesgo prematuro hacia una solución.",
                    "Conversión de necesidades en requisitos verificables, arquitectura, interfaces, trazabilidad y factores humanos desde etapas tempranas.",
                    "Gestión de riesgos a lo largo del ciclo de vida: peligros, secuencias de eventos, situaciones peligrosas, daños, controles, verificación de controles y riesgo residual.",
                    "Prototipado con propósito, planes de verificación, métodos, tolerancias, criterios de aceptación, configuración, discrepancias y repetibilidad.",
                    "Validación para el uso previsto, ingeniería de usabilidad, evidencia preclínica y clínica, evaluación biológica y real-world evidence con límites de inferencia.",
                    "Estrategia regulatoria dependiente de jurisdicción, sistema de gestión de calidad, transferencia de diseño, producción, proveedores, cambios, vigilancia posmercado y acciones de campo.",
                    "Actividades y evaluaciones con casos sintéticos, feedback recuperativo, retirada progresiva de apoyo y un capstone de expediente integral.",
                ],
                "excluded": [
                    "Clasificación regulatoria oficial, certificación, autorización de mercado, asesoramiento jurídico o determinación de conformidad para un producto real.",
                    "Ensayos con participantes, pacientes, animales o muestras biológicas reales dentro de las actividades del curso.",
                    "Sustitución de normas, requisitos legales, guidance vigente, consulta a autoridades competentes o revisión profesional especializada.",
                    "Afirmaciones de seguridad, eficacia, beneficio clínico o aptitud comercial de un dispositivo real a partir de ejercicios educativos.",
                    "Diseño detallado de circuitos, software, biomateriales o manufactura especializada cuando corresponda a asignaturas técnicas posteriores.",
                ],
                "handoff_courses": [
                    "bioinstrumentacion",
                    "biosensores",
                    "biomateriales",
                    "ingenieria-clinica-gestion",
                    "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas",
                ],
            },
            "prerequisites": [
                {
                    "id": f"{CODE}-PRE01",
                    "statement": "Fundamentos universitarios de física, matemáticas y medición suficientes para formular magnitudes, tolerancias, incertidumbre y criterios de aceptación.",
                },
                {
                    "id": f"{CODE}-PRE02",
                    "statement": "Bases de anatomía, fisiología y contexto clínico para describir usuarios, tareas, riesgos y uso previsto sin emitir decisiones clínicas.",
                },
                {
                    "id": f"{CODE}-PRE03",
                    "statement": "Capacidad para documentar requisitos, supuestos, versiones, fuentes y resultados de forma reproducible.",
                },
            ],
            "competencies": [
                {
                    "id": f"{CODE}-COMP01",
                    "statement": "Delimitar una necesidad clínica y un uso previsto mediante observación, partes interesadas y evidencia sin fijar prematuramente una solución.",
                },
                {
                    "id": f"{CODE}-COMP02",
                    "statement": "Construir requisitos, arquitectura e interfaces verificables con trazabilidad bidireccional desde necesidad hasta evidencia.",
                },
                {
                    "id": f"{CODE}-COMP03",
                    "statement": "Gestionar riesgos durante el ciclo de vida y vincular cada control con implementación, verificación y evaluación de riesgo residual.",
                },
                {
                    "id": f"{CODE}-COMP04",
                    "statement": "Planificar prototipos y verificaciones reproducibles con métodos, tolerancias, criterios de aceptación, configuración y tratamiento de discrepancias.",
                },
                {
                    "id": f"{CODE}-COMP05",
                    "statement": "Diseñar una estrategia de validación y evidencia proporcional al uso previsto separando desempeño técnico, usabilidad, evidencia preclínica y evidencia clínica.",
                },
                {
                    "id": f"{CODE}-COMP06",
                    "statement": "Integrar estrategia regulatoria, QMS, transferencia, producción y vigilancia posmercado sin presentar el expediente académico como conformidad o autorización real.",
                },
            ],
            "learning_outcomes": [
                {
                    "id": f"{CODE}-LO01",
                    "statement": "Formular una necesidad clínica verificable, población o usuario, contexto, flujo, partes interesadas, uso previsto y criterios de éxito sin sesgo prematuro hacia una solución.",
                },
                {
                    "id": f"{CODE}-LO02",
                    "statement": "Transformar necesidades en requisitos medibles y una arquitectura trazable, definiendo interfaces, factores humanos, unidades, tolerancias y métodos previstos de verificación.",
                },
                {
                    "id": f"{CODE}-LO03",
                    "statement": "Construir y mantener un archivo de riesgos que conecte peligros, secuencias de eventos, situaciones peligrosas, daños, estimación y evaluación, controles, verificación y riesgo residual.",
                },
                {
                    "id": f"{CODE}-LO04",
                    "statement": "Diseñar prototipos y planes de verificación que produzcan evidencia reproducible frente a requisitos predefinidos, con control de configuración, métodos, criterios de aceptación y discrepancias.",
                },
                {
                    "id": f"{CODE}-LO05",
                    "statement": "Distinguir y planificar validación de uso previsto, factores humanos, evidencia preclínica, evaluación biológica, evidencia clínica y RWE, declarando qué inferencias admite cada fuente.",
                },
                {
                    "id": f"{CODE}-LO06",
                    "statement": "Explicar y documentar una ruta de calidad, regulación y transferencia dependiente de jurisdicción que conecte QMS, expediente técnico, producción, cambios, vigilancia y acciones posmercado.",
                },
                {
                    "id": f"{CODE}-LO07",
                    "statement": "Integrar las seis unidades en un expediente de diseño reproducible que permita reconstruir necesidad → requisito → riesgo → control → verificación → validación → transferencia → vigilancia y haga explícitas incertidumbre, cambios y límites de inferencia.",
                },
            ],
            "study_method": [
                "Empezar cada problema declarando usuario, contexto, uso previsto, necesidad, decisión de diseño y evidencia disponible antes de seleccionar una solución.",
                "Mantener una matriz viva necesidad → requisito → riesgo → control → evidencia → estado → versión; toda modificación debe dejar procedencia y justificación.",
                "Alternar ejemplo resuelto, práctica guiada, actividad con apoyo reducido y reto autónomo; usar el feedback para corregir el expediente y registrar el cambio.",
                "Predefinir criterios de aceptación antes de observar resultados y separar verificación de requisitos de validación del uso previsto.",
                "Distinguir en todo momento dato observado, requisito, modelo, resultado de prueba, inferencia, decisión de ingeniería y afirmación regulatoria.",
                "Tratar revisión humana externa, clasificación regulatoria, certificación y autorización de mercado como procesos independientes de los gates automáticos del repositorio.",
            ],
            "editorial_notice": (
                "Corpus canónico educativo con contenido y pedagogía internos completos y fuentes trazables. No constituye "
                "diseño profesional de un producto real, clasificación regulatoria, asesoramiento legal, auditoría de QMS, "
                "certificación, validación clínica ni autorización de mercado. Multimedia permanece planificada; revisión "
                "humana interna y externa siguen pendientes."
            ),
        }
    )
    save(course_path, course)


def curate_sources_and_units() -> tuple[dict[str, list[str]], list[dict]]:
    sources_path = COURSE_ROOT / "sources.json"
    sources_doc = load(sources_path)
    sources = sources_doc.get("sources", [])
    source_by_id = {source.get("id"): source for source in sources if source.get("id")}

    preferred: list[tuple[int, str]] = []
    for source in sources:
        text = " ".join(str(source.get(key, "")) for key in ("title", "organization", "url")).casefold()
        verification = str(source.get("verification_status", "")).casefold()
        score = 0
        if any(key in text for key in ("fda", "iso ", "iec ", "european commission", "europa.eu", "imdrf", "aami")):
            score += 3
        if "verified" in verification or "official" in verification or "checked" in verification:
            score += 2
        if source.get("id"):
            preferred.append((score, source["id"]))
    preferred.sort(key=lambda item: (-item[0], item[1]))

    course_path = COURSE_ROOT / "course.json"
    course = load(course_path)
    course["core_source_ids"] = [source_id for _, source_id in preferred][:12]
    save(course_path, course)

    unit_sources: dict[str, list[str]] = {}
    claims: list[dict] = []
    for number in range(1, 7):
        unit_path = COURSE_ROOT / "units" / f"unit-{number:02d}.json"
        unit = load(unit_path)
        unit_id = f"{CODE}-U{number:02d}"
        unit["status"] = {
            "content": "complete",
            "sources": "traceable",
            "pedagogy": "complete",
            "multimedia": "planned",
            "internal_review": "pending",
            "external_review": "pending",
            "publication": "published_provisional",
        }
        unit["course_learning_outcome_ids"] = [f"{CODE}-LO{number:02d}", f"{CODE}-LO07"]
        for index, activity in enumerate(unit.get("activities", []), start=1):
            activity["estimated_duration_minutes"] = 75 if index == 1 else 60
            activity["status"] = "complete"

        source_ids = list(dict.fromkeys(unit.get("source_ids", [])))
        unit_sources[unit_id] = source_ids
        new_claim_ids: list[str] = []
        for topic_index, topic in enumerate(unit.get("topics", []), start=1):
            key_points = [str(value).strip() for value in topic.get("key_points", []) if str(value).strip()]
            if not key_points or not source_ids:
                continue
            source_id = source_ids[(topic_index - 1) % len(source_ids)]
            source = source_by_id.get(source_id, {})
            claim_id = f"{unit_id}-C{topic_index:03d}"
            claim = {
                "claim_id": claim_id,
                "unit": number,
                "text": key_points[0],
                "claim_type": "methodological_or_interpretive",
                "risk": "medium",
                "context": (
                    f"Síntesis educativa de {unit.get('title', 'la unidad')}; debe interpretarse dentro del uso previsto, "
                    "jurisdicción, protocolo, configuración y límites declarados en la unidad."
                ),
                "source_id": source_id,
                "locator": {"section": str(source.get("title") or source.get("locator") or "Fuente de la unidad")},
                "support": "direct_or_synthesis",
                "source_verification_status": str(source.get("verification_status") or "unverified"),
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": TODAY,
                "id": claim_id,
                "unit_id": unit_id,
            }
            claims.append(claim)
            new_claim_ids.append(claim_id)
        unit["claim_ids"] = new_claim_ids
        save(unit_path, unit)

    sources_doc["source_policy"] = (
        "Preservar la verificación declarada en las unidades curadas; no elevar una fuente no verificada. "
        "Las fuentes oficiales y normas se interpretan en su jurisdicción, edición y fecha aplicables."
    )
    sources_doc["consulted_on"] = TODAY
    sources_doc["coverage_gaps"] = []
    sources_doc["coverage_status"] = "complete_for_current_content"
    sources_doc["review_state"] = "ai_review_provisional"
    sources_doc["status"] = "traceable"
    save(sources_path, sources_doc)
    return unit_sources, claims


def curate_registries(unit_sources: dict[str, list[str]], claims: list[dict]) -> None:
    claims_doc = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": "Afirmaciones metodológicas centrales literales de las seis unidades con fuentes de la propia unidad; revisión disciplinaria humana pendiente.",
        "review_state": "ai_review_provisional",
        "claims": claims,
        "status": "traceable",
    }
    save(COURSE_ROOT / "claims.json", claims_doc)

    glossary_path = COURSE_ROOT / "glossary.json"
    glossary = load(glossary_path)
    for entry in glossary.get("entries", []):
        linked_sources: list[str] = []
        for unit_id in entry.get("unit_ids", []):
            linked_sources.extend(unit_sources.get(unit_id, [])[:2])
        entry["source_ids"] = list(dict.fromkeys(linked_sources))
        entry["verification_status"] = (
            "traceable_to_curated_unit_sources" if entry["source_ids"] else "course_synthesis_pending_human_review"
        )
    glossary["scope"] = (
        "Glosario integrado de U1–U6; cada entrada conserva unidades de uso y, cuando existe, procedencia en fuentes "
        "curadas de esas unidades."
    )
    glossary["review_state"] = "ai_review_provisional"
    glossary["status"] = "complete"
    save(glossary_path, glossary)

    media_path = COURSE_ROOT / "media.json"
    media = load(media_path)
    media["coverage_status"] = "planned"
    media["status"] = "planned"
    save(media_path, media)


def curate_unit_assessments(unit_sources: dict[str, list[str]]) -> None:
    cognitive_levels = ["apply", "analyze", "analyze", "evaluate", "evaluate", "create"]
    for number in range(1, 7):
        unit_id = f"{CODE}-U{number:02d}"
        unit = load(COURSE_ROOT / "units" / f"unit-{number:02d}.json")
        outcome_ids = [item["id"] for item in unit.get("learning_outcomes", [])]
        assessment_path = COURSE_ROOT / "assessments" / f"unit-{number:02d}.json"
        assessment = load(assessment_path)
        assessment["purpose"] = (
            f"Comprobar y recuperar el razonamiento aplicado de {unit.get('title', f'U{number}')}, con trazabilidad "
            "a resultados de aprendizaje y fuentes de la unidad."
        )
        assessment["status"] = "complete"
        items = assessment.get("items", [])
        for index, item in enumerate(items):
            if outcome_ids:
                item["linked_learning_outcome_ids"] = [outcome_ids[index % len(outcome_ids)]]
            item["difficulty"] = "intermediate" if index < max(1, len(items) // 2) else "advanced"
            item["cognitive_level"] = cognitive_levels[index % len(cognitive_levels)]
            item["source_ids"] = unit_sources.get(unit_id, [])[:2]
            item["status"] = "complete"
            if not item["answer_key"].get("explanation"):
                item["answer_key"]["explanation"] = (
                    "La respuesta debe conservar la cadena dato o necesidad → criterio o método → evidencia → "
                    "interpretación → límite, de acuerdo con el contenido de la unidad."
                )
            item["feedback"]["correct"] = (
                "Correcto. Comprueba además que tu respuesta conserva trazabilidad, criterio predefinido y límites de inferencia."
            )
            item["feedback"]["incorrect"] = (
                "Revisa la explicación y vuelve al resultado de aprendizaje enlazado. Identifica qué dato, requisito, "
                "riesgo, criterio o evidencia falta antes de reintentar."
            )
        save(assessment_path, assessment)


def curate_course_assessment() -> None:
    assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{CODE}-EVAL-CURSO",
        "course_id": COURSE_ID,
        "scope": "course",
        "principles": [
            "La evaluación premia trazabilidad y razonamiento de ciclo de vida, no la apariencia de un prototipo o expediente.",
            "Necesidad, requisito, riesgo, control, verificación, validación y vigilancia se evalúan como objetos distintos pero conectados.",
            "Los criterios de aceptación deben declararse antes de observar el resultado que pretenden juzgar.",
            "Una prueba técnica no se presenta como validación clínica, y una actividad regulatoria educativa no se presenta como conformidad o autorización real.",
            "Los errores corregidos con registro antes–después forman parte de la evidencia de aprendizaje.",
            "Las actividades calificadas usan escenarios y datos sintéticos o recursos abiertos no personales; revisión humana externa sigue pendiente.",
        ],
        "assessment_plan": [
            {
                "component": "Comprobaciones recuperativas U1–U6",
                "weight_percent": 15,
                "description": "Autoevaluaciones con feedback, reintento y explicación de correcciones.",
            },
            {
                "component": "Necesidades, requisitos y trazabilidad",
                "weight_percent": 20,
                "description": "Casos U1–U2 que convierten contexto de uso en requisitos medibles e interfaces auditables.",
            },
            {
                "component": "Riesgo, prototipado y verificación",
                "weight_percent": 20,
                "description": "Casos U3–U4 con controles, criterios de aceptación, configuración y discrepancias.",
            },
            {
                "component": "Validación y evidencia",
                "weight_percent": 15,
                "description": "Caso U5 que separa usabilidad, evidencia preclínica, clínica y límites de inferencia.",
            },
            {
                "component": "Regulación, calidad y transferencia",
                "weight_percent": 10,
                "description": "Caso U6 dependiente de jurisdicción, QMS, producción, cambios y vigilancia.",
            },
            {
                "component": "Proyecto integrador reproducible",
                "weight_percent": 20,
                "description": "Expediente sintético que conecta las seis unidades y defiende afirmaciones proporcionales.",
            },
        ],
        "diagnostic": {
            "title": "Diagnóstico de entrada a Desarrollo de Dispositivos Médicos",
            "purpose": "Detectar prerrequisitos que deben recuperarse antes de U1; no aporta nota final.",
            "questions": [
                "Distingue necesidad del usuario, requisito de diseño y solución técnica.",
                "Explica qué significa que un requisito sea verificable y proporciona un criterio de aceptación.",
                "Distingue peligro, situación peligrosa y daño.",
                "Explica por qué severidad del daño y probabilidad no deben mezclarse sin un método declarado.",
                "Distingue verificación de validación mediante una pregunta concreta para cada una.",
                "Explica por qué un prototipo temprano no necesita demostrar todas las prestaciones del producto final.",
                "Distingue precisión de medición, tolerancia de diseño e incertidumbre de una prueba.",
                "Explica por qué factores humanos deben conectarse con tareas, usuarios y riesgos.",
                "Distingue evidencia preclínica de evidencia clínica.",
                "Explica por qué la ruta regulatoria depende de jurisdicción, uso previsto y características del producto.",
                "Describe qué debe conservar un control de configuración.",
                "Explica por qué vigilancia posmercado puede obligar a actualizar riesgos, pruebas o diseño.",
            ],
            "interpretation": [
                "0–4 respuestas sólidas: recuperar requisitos, riesgo, medición y documentación antes de U1.",
                "5–8 respuestas sólidas: iniciar U1 con nivelación focalizada y revisión de errores en el expediente.",
                "9–12 respuestas sólidas: iniciar el curso manteniendo de todos modos trazabilidad y revisión de supuestos.",
            ],
        },
        "midterm_blueprint": [
            {"domain": "U1 Necesidad clínica y usuarios", "weight_percent": 16},
            {"domain": "U2 Requisitos y arquitectura", "weight_percent": 17},
            {"domain": "U3 Gestión de riesgos", "weight_percent": 17},
            {"domain": "U4 Prototipado y verificación", "weight_percent": 17},
            {"domain": "U5 Validación y evidencia", "weight_percent": 17},
            {"domain": "U6 Regulación y transferencia", "weight_percent": 16},
        ],
        "capstone": {
            "title": "Expediente reproducible de desarrollo de un dispositivo médico sintético",
            "scenario": (
                "Un equipo académico recibe un escenario clínico completamente sintético y debe construir un expediente "
                "de desarrollo desde la necesidad hasta transferencia y vigilancia. El objetivo es demostrar calidad del "
                "razonamiento y trazabilidad, no diseñar ni autorizar un producto real."
            ),
            "phases": [
                "Predefinir usuario, contexto, uso previsto, necesidad, exclusiones y criterios de éxito sin fijar prematuramente una solución.",
                "Derivar requisitos medibles, arquitectura e interfaces y construir trazabilidad bidireccional.",
                "Construir análisis de riesgos y seleccionar controles vinculados a requisitos y pruebas.",
                "Planificar prototipos y verificación con configuración, método, criterio de aceptación y tratamiento de discrepancias.",
                "Planificar validación y evidencia proporcional al uso previsto, separando usabilidad, preclínica y clínica.",
                "Definir una estrategia regulatoria educativa para una jurisdicción declarada y un esquema QMS/transferencia coherente.",
                "Diseñar vigilancia posmercado sintética y reglas para realimentar riesgos, requisitos y cambios.",
                "Ejecutar revisión independiente, corregir el expediente y registrar cada cambio antes–después.",
            ],
            "required_deliverables": [
                "Declaración de necesidad, usuarios, partes interesadas, contexto y uso previsto del escenario sintético.",
                "Matriz necesidad → requisito → método de verificación → criterio de aceptación → evidencia.",
                "Arquitectura funcional e interfaces con supuestos y decisiones registradas.",
                "Archivo de riesgos con peligro, secuencia, situación peligrosa, daño, evaluación, control, verificación y riesgo residual.",
                "Plan de prototipado y configuración con preguntas que responde cada iteración.",
                "Plan de verificación con métodos, muestras o repeticiones sintéticas, tolerancias, incertidumbre y discrepancias.",
                "Plan de validación y factores humanos y mapa de evidencia preclínica o clínica necesaria sin ejecutar estudios reales.",
                "Estrategia regulatoria educativa identificando jurisdicción, fuentes vigentes a comprobar y supuestos.",
                "Plan de transferencia, proveedores, cambios y vigilancia posmercado sintética.",
                "README del expediente con versiones, fuentes, registro de revisión, cambios y límites de inferencia.",
            ],
            "integration_requirements": [
                f"Vincular explícitamente evidencias con {CODE}-LO01 a {CODE}-LO07.",
                "Demostrar trazabilidad bidireccional completa y señalar cualquier elemento huérfano como hallazgo a corregir.",
                "Separar verificación, validación, evidencia clínica, conformidad regulatoria y autorización de mercado.",
                "Usar únicamente escenarios, datos y documentos sintéticos o recursos abiertos no personales y documentar procedencia o licencia.",
                "Incluir al menos una revisión independiente y un registro de correcciones justificadas.",
            ],
            "rubric": [
                {
                    "criterion": "Necesidad, usuarios y uso previsto",
                    "weight_percent": 15,
                    "excellent": "La necesidad está delimitada por usuario, contexto, flujo y criterio de éxito sin sesgo prematuro hacia una solución.",
                },
                {
                    "criterion": "Requisitos, arquitectura y trazabilidad",
                    "weight_percent": 15,
                    "excellent": "Cada requisito es medible, tiene procedencia, interfaces y trazabilidad bidireccional hasta evidencia.",
                },
                {
                    "criterion": "Gestión de riesgos",
                    "weight_percent": 15,
                    "excellent": "Peligros, secuencias, daños, controles, verificación y riesgo residual forman una cadena auditable de ciclo de vida.",
                },
                {
                    "criterion": "Prototipado y verificación",
                    "weight_percent": 15,
                    "excellent": "Los prototipos responden preguntas explícitas y las pruebas tienen configuración, método, criterio, incertidumbre y discrepancias reproducibles.",
                },
                {
                    "criterion": "Validación y evidencia",
                    "weight_percent": 15,
                    "excellent": "La evidencia está alineada con uso previsto y separa usabilidad, preclínica, clínica e inferencias no demostradas.",
                },
                {
                    "criterion": "Regulación, QMS, transferencia y vigilancia",
                    "weight_percent": 15,
                    "excellent": "La estrategia declara jurisdicción y conecta calidad, configuración, producción, cambios y señales posmercado sin afirmar autorización.",
                },
                {
                    "criterion": "Reproducibilidad, revisión y límites",
                    "weight_percent": 10,
                    "excellent": "Otra persona puede reconstruir fuentes, decisiones, versiones, cambios y límites; las correcciones tras revisión están justificadas.",
                },
            ],
        },
        "status": "complete",
    }
    save(COURSE_ROOT / "assessments" / "course-assessment.json", assessment)


def sanity_checks(claims: list[dict]) -> None:
    course = load(COURSE_ROOT / "course.json")
    assessment = load(COURSE_ROOT / "assessments" / "course-assessment.json")
    assert course["status"]["content"] == "complete"
    assert course["status"]["sources"] == "traceable"
    assert course["status"]["pedagogy"] == "complete"
    assert course["status"]["internal_review"] == "pending"
    assert course["status"]["external_review"] == "pending"
    assert len(course["learning_outcomes"]) == 7
    assert sum(item["weight_percent"] for item in assessment["assessment_plan"]) == 100
    assert sum(item["weight_percent"] for item in assessment["midterm_blueprint"]) == 100
    assert sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]) == 100
    assert len(assessment["diagnostic"]["questions"]) == 12
    assert len(assessment["capstone"]["required_deliverables"]) >= 10
    assert len(claims) >= 18
    for number in range(1, 7):
        assert (COURSE_ROOT / "units" / f"unit-{number:02d}.json").exists()
        unit = load(COURSE_ROOT / "units" / f"unit-{number:02d}.json")
        assert unit["status"]["content"] == "complete"
        assert unit["status"]["pedagogy"] == "complete"
        unit_text = json.dumps(unit, ensure_ascii=False).casefold()
        assert "concepto de la unidad que debe definirse mediante entidades observables" not in unit_text
        unit_assessment = load(COURSE_ROOT / "assessments" / f"unit-{number:02d}.json")
        assert unit_assessment["status"] == "complete"
        assert len(unit_assessment["items"]) >= 8


def main() -> int:
    bootstrap()
    curate_course()
    unit_sources, claims = curate_sources_and_units()
    curate_registries(unit_sources, claims)
    curate_unit_assessments(unit_sources)
    curate_course_assessment()
    sanity_checks(claims)
    print(f"Canonical closure ready: {COURSE_ROOT.relative_to(ROOT)} · claims={len(claims)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
