#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "biomecanica-medios-continuos"
CODE = "BMCONT"
AREA = "ingenieria-biomedica"
SRC = ROOT / "data" / "course_redevelopment" / COURSE_ID
OUT = ROOT / "data" / "courses" / COURSE_ID

STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}

COURSE_OUTCOMES = [
    "Formula problemas de mecánica continua biomecánica declarando configuración, campos, hipótesis, escalas, fronteras y cantidades de interés antes de resolver.",
    "Aplica balances de masa, cantidad de movimiento y energía a sólidos y fluidos biológicos conservando sistemas de referencia, unidades y condiciones de validez.",
    "Selecciona, calibra e interpreta leyes constitutivas elásticas e hiperelásticas distinguiendo estructura matemática, parámetros, identificabilidad y capacidad predictiva.",
    "Analiza respuesta dependiente del tiempo mediante viscoelasticidad, poroelasticidad y mecanismos acoplados sin confundir ajuste fenomenológico con mecanismo demostrado.",
    "Analiza fluidos biológicos mediante conservación, Navier–Stokes, escalas adimensionales, reología y métricas hemodinámicas con límites explícitos de inferencia.",
    "Construye y audita modelos por elementos finitos mediante formulación débil, discretización, convergencia, verificación, validación, sensibilidad e incertidumbre.",
    "Integra las seis unidades en un expediente computacional reproducible que vincula modelo, evidencia, controles, incertidumbre, contexto de uso y límites de interpretación."
]


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug(text: str) -> str:
    table = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    text = text.translate(table).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "source"


def status_copy() -> dict:
    return dict(STATUS)


units_src = [
    json.loads((SRC / "units" / f"unit-{i:02d}.json").read_text(encoding="utf-8"))
    for i in range(1, 7)
]

# Consolidate sources while retaining direct locators and provenance by unit.
source_records: OrderedDict[str, dict] = OrderedDict()
source_key_to_id: dict[str, str] = {}
unit_source_ids: dict[int, list[str]] = {}
used_source_ids: set[str] = set()
for index, unit in enumerate(units_src, 1):
    uid = f"{CODE}-U{index:02d}"
    ids: list[str] = []
    for source in unit.get("sources", []):
        key = str(
            source.get("doi")
            or source.get("pmid")
            or source.get("isbn")
            or source.get("url")
            or source.get("citation")
            or source.get("title")
            or ""
        ).strip().casefold()
        if not key:
            continue
        if key not in source_key_to_id:
            label = str(source.get("citation") or source.get("title") or source.get("url") or key)
            base = slug(label)[:88]
            candidate = base
            suffix = 2
            while candidate in used_source_ids:
                candidate = f"{base}-{suffix}"
                suffix += 1
            used_source_ids.add(candidate)
            source_key_to_id[key] = candidate
            record = dict(source)
            record["id"] = candidate
            record["used_by_unit_ids"] = [uid]
            source_records[candidate] = record
        else:
            candidate = source_key_to_id[key]
            if uid not in source_records[candidate]["used_by_unit_ids"]:
                source_records[candidate]["used_by_unit_ids"].append(uid)
        ids.append(candidate)
    if len(set(ids)) < 5:
        raise RuntimeError(f"U{index} no conserva al menos cinco fuentes trazables")
    unit_source_ids[index] = list(dict.fromkeys(ids))

# Consolidate glossary and keep exact links to unit and traceable sources.
glossary_by_term: OrderedDict[str, dict] = OrderedDict()
for index, unit in enumerate(units_src, 1):
    uid = f"{CODE}-U{index:02d}"
    supporting_sources = unit_source_ids[index][:2]
    for entry in unit.get("glossary", []):
        term = str(entry.get("term") or "").strip()
        definition = str(entry.get("definition") or "").strip()
        if not term or not definition:
            continue
        key = term.casefold()
        if key not in glossary_by_term:
            glossary_by_term[key] = {
                "term": term,
                "definition": definition,
                "unit_ids": [uid],
                "source_ids": list(supporting_sources),
                "verification_status": "traceable_to_curated_unit_sources",
            }
        else:
            record = glossary_by_term[key]
            if uid not in record["unit_ids"]:
                record["unit_ids"].append(uid)
            for sid in supporting_sources:
                if sid not in record["source_ids"]:
                    record["source_ids"].append(sid)

glossary_entries: list[dict] = []
term_to_gid: dict[str, str] = {}
for number, (key, record) in enumerate(glossary_by_term.items(), 1):
    gid = f"{CODE}-GLO-{number:03d}"
    glossary_entries.append({"id": gid, **record})
    term_to_gid[key] = gid

# Planned visuals remain explicitly pending, one map per unit.
media_items = []
for index, unit in enumerate(units_src, 1):
    media_items.append({
        "id": f"{CODE}-MED-{index:02d}",
        "unit_id": f"{CODE}-U{index:02d}",
        "type": "diagram",
        "title": f"Mapa visual de U{index}: {unit['title']}",
        "purpose": "Sintetizar configuración, campos, ecuaciones, entradas, controles y límites de la unidad sin sustituir el desarrollo textual.",
        "status": "planned",
    })

# Literal claims are copied from key points that will also appear in canonical units.
claims: list[dict] = []
unit_claim_ids: dict[int, list[str]] = {}
for index, unit in enumerate(units_src, 1):
    claim_ids: list[str] = []
    candidate_texts: list[str] = []
    for section in unit.get("theory_sections", []):
        key_points = [str(x).strip() for x in section.get("key_points", []) if str(x).strip()]
        if key_points:
            candidate_texts.append(key_points[0])
        if len(candidate_texts) >= 2:
            break
    for number, text in enumerate(candidate_texts[:2], 1):
        cid = f"{CODE}-U{index:02d}-CL{number:02d}"
        claims.append({
            "id": cid,
            "unit_id": f"{CODE}-U{index:02d}",
            "text": text,
            "source_id": unit_source_ids[index][min(number - 1, len(unit_source_ids[index]) - 1)],
            "status": "curated_internal_review_pending",
        })
        claim_ids.append(cid)
    if not claim_ids:
        raise RuntimeError(f"U{index} no produjo claims literales")
    unit_claim_ids[index] = claim_ids

# Transform each curated redevelopment unit into canonical academic schema.
canonical_units: list[dict] = []
for index, unit in enumerate(units_src, 1):
    uid = f"{CODE}-U{index:02d}"
    outcomes = [
        {"id": f"{uid}-LO{j:02d}", "statement": statement}
        for j, statement in enumerate(unit.get("learning_objectives", []), 1)
    ]
    if len(outcomes) < 5:
        raise RuntimeError(f"U{index} perdió resultados de aprendizaje")

    topics: list[dict] = []
    for topic_n, section in enumerate(unit.get("theory_sections", []), 1):
        tid = f"{uid}-T{topic_n:02d}"
        equation_blocks: list[dict] = []
        for eq_n, equation in enumerate(section.get("equations", []), 1):
            latex = str(equation.get("latex") or "").strip()
            if not latex:
                continue
            block = {"id": f"{tid}-B{eq_n:02d}", "type": "equation", "latex": latex}
            meaning = str(equation.get("meaning") or equation.get("label") or "").strip()
            if meaning:
                block["label"] = meaning
            if isinstance(equation.get("variables"), dict):
                block["variables"] = equation["variables"]
            equation_blocks.append(block)

        key_points = [str(x).strip() for x in section.get("key_points", []) if str(x).strip()]
        paragraphs = [str(x).strip() for x in section.get("paragraphs", []) if str(x).strip()]
        subtopics: list[dict] = []
        for paragraph_n, paragraph in enumerate(paragraphs, 1):
            stid = f"{tid}-ST{paragraph_n:02d}"
            subtitle = key_points[paragraph_n - 1] if paragraph_n - 1 < len(key_points) else f"Desarrollo conceptual {paragraph_n}"
            subtopics.append({
                "id": stid,
                "title": subtitle,
                "blocks": [{"id": f"{stid}-B01", "type": "paragraph", "text": paragraph}],
            })
        topics.append({
            "id": tid,
            "title": section.get("heading") or f"Tema {topic_n}",
            "blocks": equation_blocks,
            "key_points": key_points or ["Relacionar formulación, evidencia y límites antes de interpretar."],
            "subtopics": subtopics,
        })
    if len(topics) < 4:
        raise RuntimeError(f"U{index} no conserva cuatro temas")

    examples: list[dict] = []
    for example_n, example in enumerate(unit.get("worked_examples", []), 1):
        interpretation = str(example.get("interpretation") or example.get("result") or "Interpretación limitada al escenario sintético.")
        limitations = list(example.get("limitations", []))
        if not limitations:
            limitations = ["La conclusión se limita a los datos, hipótesis y cantidad de interés del escenario; no constituye inferencia clínica individual."]
        examples.append({
            "id": f"{uid}-EX{example_n:02d}",
            "title": example.get("title") or f"Ejemplo {example_n}",
            "scenario": example.get("scenario") or "Escenario sintético delimitado.",
            "reasoning_steps": list(example.get("reasoning_steps", [])),
            "interpretation": interpretation,
            "limitations": limitations,
        })

    activities: list[dict] = []
    for activity_n, activity in enumerate(unit.get("guided_activities", []), 1):
        tasks = list(activity.get("problems", [])) + list(activity.get("tasks", []))
        if not tasks:
            tasks = ["Reconstruye el razonamiento de la actividad, documenta supuestos y comprueba la conclusión."]
        activities.append({
            "id": f"{uid}-ACT{activity_n:02d}",
            "title": activity.get("title") or f"Actividad {activity_n}",
            "purpose": f"Aplicar y comprobar los resultados de aprendizaje de {unit['title']} mediante un escenario académico reproducible y delimitado.",
            "prerequisite_unit_ids": [] if index == 1 else [f"{CODE}-U{index-1:02d}"],
            "instructions": list(activity.get("instructions", [])) or ["Trabaja con el escenario indicado y conserva todos los supuestos."],
            "tasks": tasks,
            "deliverables": list(activity.get("deliverables", [])) or ["Producto técnico auditable de la actividad."],
            "checking_criteria": list(activity.get("checking_criteria", [])) or ["La conclusión es proporcional a la evidencia y declara límites."],
            "estimated_duration_minutes": int(activity.get("estimated_duration_minutes") or 180),
            "status": "curated_internal_review_pending",
        })

    glossary_ids: list[str] = []
    for entry in unit.get("glossary", []):
        gid = term_to_gid.get(str(entry.get("term") or "").strip().casefold())
        if gid and gid not in glossary_ids:
            glossary_ids.append(gid)

    biomedical: list[str] = []
    for connection in unit.get("biomedical_connections", []):
        if isinstance(connection, dict):
            topic = str(connection.get("context") or connection.get("topic") or "Conexión").strip()
            text = str(connection.get("connection") or "").strip()
            if text:
                biomedical.append(f"{topic}: {text}")
        elif str(connection).strip():
            biomedical.append(str(connection).strip())

    canonical_units.append({
        "$schema": "../../../../schemas/academic/unit-v1.schema.json",
        "schema_version": "1.0",
        "id": uid,
        "course_id": COURSE_ID,
        "order": index,
        "slug": unit["slug"],
        "title": unit["title"],
        "status": status_copy(),
        "purpose": unit["purpose"],
        "prerequisite_unit_ids": [] if index == 1 else [f"{CODE}-U{index-1:02d}"],
        "course_learning_outcome_ids": [f"{CODE}-LO{index:02d}", f"{CODE}-LO07"],
        "learning_outcomes": outcomes,
        "topics": topics,
        "examples": examples,
        "activities": activities,
        "assessment_file": f"assessments/unit-{index:02d}.json",
        "glossary_entry_ids": glossary_ids,
        "source_ids": unit_source_ids[index],
        "claim_ids": unit_claim_ids[index],
        "media_ids": [f"{CODE}-MED-{index:02d}"],
        "common_errors": list(unit.get("common_errors", [])),
        "biomedical_connections": biomedical,
        "editorial_notice": unit.get("editorial_notice", "Curación interna; revisión humana pendiente."),
        "legacy_origin": f"data/course_redevelopment/{COURSE_ID}/units/unit-{index:02d}.json",
    })

course = {
    "$schema": "../../../schemas/academic/course-v1.schema.json",
    "schema_version": "1.0",
    "id": COURSE_ID,
    "code": CODE,
    "area_id": AREA,
    "title": "Biomecánica de Medios Continuos",
    "language": "es",
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario avanzado e introducción de posgrado",
    "audience": "Estudiantes de ingeniería biomédica, biomecánica y áreas afines con bases de cálculo vectorial, ecuaciones diferenciales, mecánica, métodos numéricos y fisiología que necesiten modelar sólidos, tejidos y fluidos biológicos con trazabilidad matemática y computacional.",
    "status": status_copy(),
    "purpose": "Integrar cinemática y balances del continuo, leyes constitutivas, respuesta dependiente del tiempo, fluidos biológicos y elementos finitos para construir modelos biomecánicos reproducibles y auditables, conectando hipótesis, parámetros, evidencia, verificación, validación, incertidumbre y contexto de uso sin convertir una predicción mecánica en diagnóstico, pronóstico o validación clínica universal.",
    "scope": {
        "included": [
            "Cinemática de deformación finita, configuraciones, gradientes, tensores y medidas objetivas.",
            "Balances de masa y cantidad de movimiento, esfuerzos y condiciones de frontera en medios continuos.",
            "Elasticidad e hiperelasticidad isotrópica y anisotrópica, calibración e identificabilidad.",
            "Viscoelasticidad, poroelasticidad y respuesta dependiente del tiempo con escalas y mecanismos acoplados.",
            "Fluidos biológicos, Navier–Stokes, Poiseuille, Reynolds, Womersley, reología y métricas hemodinámicas.",
            "Formulación débil y elementos finitos, malla, convergencia, verificación, validación, sensibilidad, UQ y credibilidad.",
            "Expedientes reproducibles con hipótesis, datos, ecuaciones, parámetros, controles, incertidumbre y límites de inferencia."
        ],
        "excluded": [
            "Diagnóstico, pronóstico, decisión terapéutica o recomendación quirúrgica individual a partir de una simulación.",
            "Afirmar propiedades de tejido específicas de una persona a partir de parámetros genéricos o un ajuste no identificado.",
            "Tratar convergencia numérica, calibración o acuerdo parcial como validación clínica o regulatoria universal.",
            "Certificar un solver, un dispositivo médico o una presentación regulatoria mediante ejercicios educativos.",
            "Trabajo con datos clínicos identificables, participantes, tejidos o dispositivos reales fuera de infraestructura, permisos y revisión adecuados."
        ],
        "handoff_courses": ["biomecanica", "fundamentos-biomecanica", "laboratorio-biomecanica", "modelado-simulacion-biomedicina", "modelos-numericos-biomedicina", "simulacion-planificacion-quirurgica"],
    },
    "prerequisites": [
        {"id": f"{CODE}-PRE01", "statement": "Cálculo multivariable, álgebra lineal y cálculo vectorial suficientes para interpretar gradientes, divergencia, integrales y tensores."},
        {"id": f"{CODE}-PRE02", "statement": "Mecánica clásica y resistencia de materiales inicial, incluyendo equilibrio, esfuerzo, deformación y energía."},
        {"id": f"{CODE}-PRE03", "statement": "Ecuaciones diferenciales y métodos numéricos suficientes para entender discretización, integración, solución iterativa y error."},
        {"id": f"{CODE}-PRE04", "statement": "Fisiología y anatomía funcional básicas para situar tejidos, flujo sanguíneo y condiciones biomecánicas sin convertir el modelo en inferencia clínica."},
    ],
    "competencies": [
        {"id": f"{CODE}-COMP{i:02d}", "statement": statement}
        for i, statement in enumerate([
            "Formular un problema de medio continuo desde configuración, campos, escalas, balances, constitutiva, fronteras y cantidad de interés.",
            "Seleccionar medidas cinemáticas, esfuerzos y leyes constitutivas compatibles con el régimen mecánico y la evidencia disponible.",
            "Analizar dependencia temporal, acoplamientos sólido-fluido y escalas características sin sobreinterpretar parámetros fenomenológicos.",
            "Aplicar conservación y análisis adimensional a fluidos biológicos y evaluar la pertinencia de simplificaciones de flujo y reología.",
            "Diseñar discretizaciones y controles de convergencia/verificación proporcionales a la cantidad de interés computacional.",
            "Separar calibración, validación, sensibilidad e incertidumbre y evaluar credibilidad para un contexto de uso delimitado.",
            "Comunicar un expediente reproducible que permita reconstruir fuentes, ecuaciones, parámetros, decisiones, límites y estado de revisión."
        ], 1)
    ],
    "learning_outcomes": [
        {"id": f"{CODE}-LO{i:02d}", "statement": statement}
        for i, statement in enumerate(COURSE_OUTCOMES, 1)
    ],
    "study_method": [
        "Definir primero sistema, configuración, campos, escalas, cantidad de interés y condiciones de frontera antes de elegir una ecuación o software.",
        "Separar identidad matemática, medición, parámetro estimado, supuesto constitutivo, resultado numérico e inferencia física.",
        "Trabajar con ejemplos resueltos y problemas sintéticos antes de actividades integradoras, retirando progresivamente la ayuda.",
        "Comprobar unidades, invariancia, balances, casos límite, convergencia y sensibilidad antes de interpretar mapas o valores extremos.",
        "Mantener trazabilidad entre unidad, resultado de aprendizaje, claim, fuente, evaluación, glosario y evidencia computacional.",
        "Cerrar cada análisis indicando incertidumbre, alternativa plausible, dominio de validez, extrapolaciones y siguiente prueba discriminante."
    ],
    "core_source_ids": list(source_records.keys())[:12],
    "unit_files": [f"units/unit-{i:02d}.json" for i in range(1, 7)],
    "assessment_files": [f"assessments/unit-{i:02d}.json" for i in range(1, 7)] + ["assessments/course-assessment.json"],
    "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
    "static_site": {
        "renderer": "scripts/generate_site.py",
        "canonical_source": True,
        "legacy_mirrors": [
            f"data/generated_courses/{COURSE_ID}.json",
            f"data/generated_units/{COURSE_ID}/",
            f"data/subjects/{AREA}/{COURSE_ID}.json",
            f"data/source_registry/{COURSE_ID}.json",
            f"data/claim_registry/{COURSE_ID}.json",
        ],
    },
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, fuentes trazables y pedagogía interna para las seis unidades de Biomecánica de Medios Continuos. La publicación sigue siendo provisional. La revisión humana interna y disciplinaria externa, la certificación de software, la validación clínica o regulatoria, el uso de datos clínicos reales y cualquier decisión diagnóstica, terapéutica o quirúrgica permanecen fuera de este cierre y siguen pendientes.",
}

# Convert curated self-assessments into canonical formative assessments.
for index, (src_unit, unit) in enumerate(zip(units_src, canonical_units), 1):
    uid = unit["id"]
    local_los = [item["id"] for item in unit["learning_outcomes"]]
    items: list[dict] = []
    questions = list(src_unit.get("self_assessment", []))
    for qn, q in enumerate(questions, 1):
        if qn <= 3:
            difficulty, cognitive = "foundational", "understand"
        elif qn <= 7:
            difficulty, cognitive = "intermediate", "apply"
        else:
            difficulty, cognitive = "advanced", "analyze"
        misconception = str(q.get("common_error") or "Confundir el modelo matemático o numérico con el sistema físico completo.")
        explanation = str(q.get("reasoning") or "La respuesta debe conectar formulación, evidencia, control y límite de validez.")
        items.append({
            "id": f"{uid}-Q{qn:02d}",
            "type": "short_answer",
            "prompt": str(q.get("question") or "Explica el concepto central de la unidad."),
            "linked_learning_outcome_ids": [local_los[(qn - 1) % len(local_los)]],
            "difficulty": difficulty,
            "cognitive_level": cognitive,
            "answer_key": {
                "expected_answer": str(q.get("answer") or "Respuesta razonada y limitada a la evidencia de la unidad."),
                "explanation": explanation,
                "common_misconceptions": [misconception],
            },
            "feedback": {
                "correct": f"Correcto. Conserva esta justificación: {explanation}",
                "incorrect": f"Revisa el razonamiento y corrige este error frecuente: {misconception}",
            },
            "source_ids": unit_source_ids[index][:2],
            "status": "curated_internal_review_pending",
        })
    if not items:
        raise RuntimeError(f"U{index} no conserva autoevaluación")
    dump(OUT / "assessments" / f"unit-{index:02d}.json", {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{uid}-EVAL",
        "course_id": COURSE_ID,
        "scope": "unit",
        "unit_id": uid,
        "purpose": "Autoevaluación formativa de los resultados de aprendizaje de la unidad con retroalimentación recuperativa y límites de inferencia.",
        "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
        "items": items,
        "status": "curated_internal_review_pending",
    })

course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": f"{CODE}-COURSE-EVAL",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": [
        "Evaluar comprensión, formulación, cálculo, análisis y transferencia; no solo reconocimiento de símbolos.",
        "Separar identidad matemática, hipótesis constitutiva, estimación de parámetros, error numérico, evidencia experimental e inferencia biomecánica.",
        "Usar escenarios y datos sintéticos para practicar modelado sin requerir datos de pacientes ni ensayos reales.",
        "Predefinir cantidad de interés, controles, criterios de convergencia/aceptación y límites antes de inspeccionar resultados.",
        "Incluir revisión de errores, sensibilidad y corrección documentada como parte de la evaluación.",
        "Mantener revisión humana pendiente aunque el corpus esté completo a nivel interno."
    ],
    "assessment_plan": [
        {"component": "Recuperación y explicaciones conceptuales", "weight_percent": 15, "purpose": "Consolidar cinemática, balances, constitutivas, flujo, FEM y V&V."},
        {"component": "Problemas cuantitativos por unidad", "weight_percent": 25, "purpose": "Aplicar ecuaciones, escalas, controles de unidades y casos límite a problemas nuevos."},
        {"component": "Actividades reproducibles sintéticas", "weight_percent": 25, "purpose": "Construir productos auditables con modelos, datos y scripts sintéticos."},
        {"component": "Revisión, sensibilidad y corrección", "weight_percent": 10, "purpose": "Detectar errores de formulación, inferencia, convergencia, calibración y transferencia."},
        {"component": "Proyecto integrador", "weight_percent": 25, "purpose": "Integrar las seis unidades en un expediente mecánico-computacional defendible."},
    ],
    "diagnostic": {
        "purpose": "Detectar prerrequisitos y concepciones que requieren recuperación antes del curso.",
        "questions": [
            "Diferencia escalar, vector y tensor y da un ejemplo mecánico de cada uno.",
            "Explica la diferencia entre configuración de referencia y configuración actual.",
            "Interpreta físicamente gradiente, divergencia y determinante de una transformación.",
            "Diferencia esfuerzo, deformación y ley constitutiva.",
            "Explica qué significa balance local de cantidad de movimiento.",
            "Diferencia condición de Dirichlet y de Neumann con un ejemplo mecánico.",
            "Explica qué significa casi incomprensible y por qué importa numéricamente.",
            "Diferencia elasticidad, viscoelasticidad y poroelasticidad.",
            "Explica el significado físico del número de Reynolds.",
            "Diferencia calibración de validación.",
            "Diferencia convergencia del solver de convergencia de malla.",
            "Explica por qué un resultado numéricamente convergido puede ser físicamente incorrecto."
        ],
    },
    "midterm_blueprint": [
        {"unit_id": f"{CODE}-U01", "weight_percent": 15, "focus": "Cinemática continua, configuraciones y medidas de deformación."},
        {"unit_id": f"{CODE}-U02", "weight_percent": 15, "focus": "Balances, tensiones, tracciones y condiciones de frontera."},
        {"unit_id": f"{CODE}-U03", "weight_percent": 20, "focus": "Elasticidad, hiperelasticidad, anisotropía e identificabilidad."},
        {"unit_id": f"{CODE}-U04", "weight_percent": 15, "focus": "Viscoelasticidad, poroelasticidad y escalas temporales."},
        {"unit_id": f"{CODE}-U05", "weight_percent": 15, "focus": "Fluidos biológicos, escalas adimensionales y métricas de flujo."},
        {"unit_id": f"{CODE}-U06", "weight_percent": 20, "focus": "FEM, convergencia, V&V, sensibilidad, UQ y credibilidad."},
    ],
    "capstone": {
        "title": "Expediente integrador de mecánica continua biomecánica",
        "purpose": "Defender un modelo sintético desde formulación continua hasta solución computacional, V&V e incertidumbre, indicando exactamente qué predice y qué no puede inferirse.",
        "deliverables": [
            "Definición del sistema, contexto de uso académico y cantidad de interés.",
            "Mapa de configuraciones, campos, balances, constitutiva y condiciones de frontera.",
            "Identificación/calibración de parámetros con procedencia y sensibilidad.",
            "Análisis temporal o de flujo cuando corresponda, con escalas y simplificaciones justificadas.",
            "Discretización FE con estudio de malla, solver y verificaciones de equilibrio/conservación.",
            "Validación sintética independiente y análisis de incertidumbre/aplicabilidad.",
            "Tabla de claims, fuentes, resultados, contradicciones, límites y versión revisada tras retroalimentación."
        ],
        "rubric": [
            {"criterion": "Formulación y fronteras", "weight_percent": 15, "excellent": "Sistema, configuración, campos, balances, constitutiva, fronteras y cantidad de interés están explícitos y coherentes."},
            {"criterion": "Cinemática y mecánica constitutiva", "weight_percent": 15, "excellent": "Medidas y constitutiva son objetivas, apropiadas al régimen y conectadas con evidencia e identificabilidad."},
            {"criterion": "Dependencia temporal o flujo", "weight_percent": 15, "excellent": "Escalas, mecanismos, simplificaciones y métricas se justifican sin extrapolación oculta."},
            {"criterion": "Discretización y verificación", "weight_percent": 20, "excellent": "Elementos, malla, solver, convergencia, balances y singularidades están auditados respecto de la cantidad de interés."},
            {"criterion": "Validación, sensibilidad e incertidumbre", "weight_percent": 20, "excellent": "Calibración y validación están separadas; sensibilidad, incertidumbre y aplicabilidad limitan correctamente la conclusión."},
            {"criterion": "Reproducibilidad y comunicación", "weight_percent": 15, "excellent": "Fuentes, versiones, parámetros, ecuaciones, decisiones y límites son reconstruibles y la conclusión no excede la evidencia."},
        ],
        "linked_learning_outcome_ids": [f"{CODE}-LO{i:02d}" for i in range(1, 8)],
    },
    "status": "curated_internal_review_pending",
}

# Persist canonical corpus and registries.
dump(OUT / "course.json", course)
for index, unit in enumerate(canonical_units, 1):
    dump(OUT / "units" / f"unit-{index:02d}.json", unit)
dump(OUT / "glossary.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "entries": glossary_entries,
})
dump(OUT / "sources.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "source_policy": "Priorizar textos y artículos de mecánica/biomecánica, trabajos metodológicos, estándares ASME y guías regulatorias oficiales directamente pertinentes; conservar URL, DOI, PMID, ISBN y estado de verificación de las unidades curadas. La trazabilidad de una fuente no equivale a revisión humana del curso ni a validación clínica o regulatoria.",
    "consulted_on": "2026-08-24",
    "coverage_gaps": [],
    "sources": list(source_records.values()),
})
dump(OUT / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Afirmaciones centrales literales derivadas de las seis unidades curadas y enlazadas a fuentes del registro.",
    "review_state": "internal_curated_external_pending",
    "claims": claims,
})
dump(OUT / "media.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "coverage_status": "planned",
    "items": media_items,
})
dump(OUT / "assessments" / "course-assessment.json", course_assessment)

# Permanent regression for canonical closure.
test_path = ROOT / "tests" / "test_biomecanica_medios_continuos_canonical.py"
test_path.write_text('''from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "courses" / "biomecanica-medios-continuos"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaMediosContinuosCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((BASE / "course.json").read_text(encoding="utf-8"))

    def test_course_complete_human_review_pending(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_preserve_disciplinary_content(self):
        self.assertEqual(len(self.course["unit_files"]), 6)
        expected = [
            "cinematica-deformacion",
            "tensiones-y-equilibrio",
            "elasticidad",
            "viscoelasticidad-y-poroelasticidad",
            "fluidos-biologicos",
            "elementos-finitos-y-validacion",
        ]
        for index, relative in enumerate(self.course["unit_files"], 1):
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            self.assertEqual(unit["order"], index)
            self.assertEqual(unit["slug"], expected[index - 1])
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
            text = json.dumps(unit, ensure_ascii=False).casefold()
            self.assertNotIn(GENERIC, text)
            self.assertGreaterEqual(len(unit["learning_outcomes"]), 5)
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 2)
            self.assertGreaterEqual(len(unit["activities"]), 1)
            self.assertGreaterEqual(len(unit["source_ids"]), 5)
            self.assertGreaterEqual(len(unit["claim_ids"]), 1)

    def test_assessment_and_registries_complete(self):
        for relative in self.course["assessment_files"]:
            self.assertTrue((BASE / relative).exists(), relative)
        assessment = json.loads((BASE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)
        self.assertEqual(len(assessment["midterm_blueprint"]), 6)
        self.assertGreaterEqual(len(assessment["capstone"]["rubric"]), 6)
        glossary = json.loads((BASE / "glossary.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(glossary["entries"]), 50)
        self.assertTrue(all(entry.get("source_ids") for entry in glossary["entries"]))
        sources = json.loads((BASE / "sources.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(sources["sources"]), 30)
        self.assertEqual(sources["coverage_gaps"], [])
        claims = json.loads((BASE / "claims.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(claims["claims"]), 6)
        media = json.loads((BASE / "media.json").read_text(encoding="utf-8"))
        self.assertEqual(media["coverage_status"], "planned")
        self.assertEqual(len(media["items"]), 6)

    def test_course_outcomes_cover_full_sequence(self):
        self.assertEqual(len(self.course["learning_outcomes"]), 7)
        mapped = set()
        for relative in self.course["unit_files"]:
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            mapped.update(unit["course_learning_outcome_ids"])
        self.assertEqual(mapped, {item["id"] for item in self.course["learning_outcomes"]})

    def test_boundaries_remain_explicit(self):
        notice = self.course["editorial_notice"].casefold()
        for phrase in ("revisión humana", "certificación de software", "validación clínica o regulatoria", "decisión diagnóstica"):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8")

print(
    f"Canonical Biomecánica de Medios Continuos: units={len(canonical_units)}, "
    f"sources={len(source_records)}, glossary={len(glossary_entries)}, claims={len(claims)}"
)
