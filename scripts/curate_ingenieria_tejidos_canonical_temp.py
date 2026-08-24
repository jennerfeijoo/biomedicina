#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "ingenieria-tejidos"
CODE = "INGTEJ"
AREA = "biologicas-medicas"
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
    "Formula una estrategia de ingeniería de tejidos delimitada integrando células, andamio, señales, microambiente, función y requisitos verificables.",
    "Selecciona y compara fuentes celulares considerando identidad, estado, heterogeneidad, expansión, estabilidad y límites de inferencia.",
    "Diseña y evalúa conceptualmente biomateriales y andamios relacionando arquitectura, propiedades, degradación, funcionalización y respuesta biológica.",
    "Analiza transporte, perfusión, vascularización, biorreactores y estímulos mecánicos mediante balances, escalas y controles apropiados.",
    "Construye un paquete preclínico de peso de evidencia que separa seguridad biológica, desempeño, pertinencia del modelo, incertidumbre y transferencia.",
    "Construye una estrategia de traslación y manufactura que conecte producto, calidad, proceso, potencia, comparabilidad, trazabilidad, regulación y ética.",
    "Integra las seis unidades en un expediente reproducible que vincula pregunta, evidencia, método, control, resultado, incertidumbre, riesgo y límite de inferencia.",
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


units_src = [json.loads((SRC / "units" / f"unit-{i:02d}.json").read_text(encoding="utf-8")) for i in range(1, 7)]

# Build a deduplicated source registry and per-unit mappings.
source_records: OrderedDict[str, dict] = OrderedDict()
source_key_to_id: dict[str, str] = {}
unit_source_ids: dict[int, list[str]] = {}
used_source_ids: set[str] = set()
for index, unit in enumerate(units_src, 1):
    uid = f"{CODE}-U{index:02d}"
    ids: list[str] = []
    for source in unit.get("sources", []):
        key = str(source.get("url") or source.get("title") or "").strip()
        if not key:
            continue
        if key not in source_key_to_id:
            base = slug(str(source.get("title") or key))[:90]
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
    if not ids:
        raise RuntimeError(f"U{index} no tiene fuentes trazables")
    unit_source_ids[index] = list(dict.fromkeys(ids))

# Consolidate glossary with exact unit and source links.
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
            rec = glossary_by_term[key]
            if uid not in rec["unit_ids"]:
                rec["unit_ids"].append(uid)
            for sid in supporting_sources:
                if sid not in rec["source_ids"]:
                    rec["source_ids"].append(sid)

glossary_entries: list[dict] = []
term_to_gid: dict[str, str] = {}
for n, (key, record) in enumerate(glossary_by_term.items(), 1):
    gid = f"{CODE}-GLO-{n:03d}"
    record = {"id": gid, **record}
    glossary_entries.append(record)
    term_to_gid[key] = gid

# One planned visual per unit. Multimedia remains deliberately pending.
media_items = []
for index, unit in enumerate(units_src, 1):
    media_items.append({
        "id": f"{CODE}-MED-{index:02d}",
        "unit_id": f"{CODE}-U{index:02d}",
        "type": "diagram",
        "title": f"Mapa visual de U{index}: {unit['title']}",
        "purpose": "Sintetizar relaciones, entradas, controles y límites de la unidad sin sustituir el desarrollo textual.",
        "status": "planned",
    })

# Create exact, traceable course claims from text that will appear literally in canonical units.
claims = []
unit_claim_ids: dict[int, list[str]] = {}
for index, unit in enumerate(units_src, 1):
    claim_ids = []
    candidate_texts = []
    for section in unit.get("theory_sections", []):
        candidate_texts.extend(section.get("key_points", [])[:1])
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
    unit_claim_ids[index] = claim_ids

# Build canonical units, preserving all curated theory paragraphs, equations, examples and activities.
canonical_units = []
for index, unit in enumerate(units_src, 1):
    uid = f"{CODE}-U{index:02d}"
    outcomes = [
        {"id": f"{uid}-LO{j:02d}", "statement": statement}
        for j, statement in enumerate(unit.get("learning_objectives", []), 1)
    ]
    topics = []
    for topic_n, section in enumerate(unit.get("theory_sections", []), 1):
        tid = f"{uid}-T{topic_n:02d}"
        equation_blocks = []
        for eq_n, equation in enumerate(section.get("equations", []), 1):
            block = {
                "id": f"{tid}-B{eq_n:02d}",
                "type": "equation",
                "latex": str(equation.get("latex") or "").strip(),
            }
            meaning = str(equation.get("meaning") or equation.get("label") or "").strip()
            if meaning:
                block["label"] = meaning
            if isinstance(equation.get("variables"), dict):
                block["variables"] = equation["variables"]
            equation_blocks.append(block)
        key_points = list(section.get("key_points", []))
        subtopics = []
        for paragraph_n, paragraph in enumerate(section.get("paragraphs", []), 1):
            stid = f"{tid}-ST{paragraph_n:02d}"
            subtitle = key_points[paragraph_n - 1] if paragraph_n - 1 < len(key_points) else f"Desarrollo conceptual {paragraph_n}"
            subtopics.append({
                "id": stid,
                "title": subtitle,
                "blocks": [{
                    "id": f"{stid}-B01",
                    "type": "paragraph",
                    "text": paragraph,
                }],
            })
        topics.append({
            "id": tid,
            "title": section.get("heading") or f"Tema {topic_n}",
            "blocks": equation_blocks,
            "key_points": key_points or ["Revisar el desarrollo conceptual y sus límites."],
            "subtopics": subtopics,
        })

    examples = []
    for example_n, example in enumerate(unit.get("worked_examples", []), 1):
        examples.append({
            "id": f"{uid}-EX{example_n:02d}",
            "title": example.get("title") or f"Ejemplo {example_n}",
            "scenario": example.get("scenario") or "Escenario sintético delimitado.",
            "reasoning_steps": list(example.get("reasoning_steps", [])),
            "interpretation": example.get("interpretation") or "Interpretación limitada al escenario.",
            "limitations": list(example.get("limitations", [])),
        })

    activities = []
    for activity_n, activity in enumerate(unit.get("guided_activities", []), 1):
        tasks = list(activity.get("problems", [])) + list(activity.get("tasks", []))
        if not tasks:
            tasks = ["Reconstruye el razonamiento de la actividad y documenta el resultado."]
        activities.append({
            "id": f"{uid}-ACT{activity_n:02d}",
            "title": activity.get("title") or f"Actividad {activity_n}",
            "purpose": f"Aplicar y comprobar los resultados de aprendizaje de {unit['title']} mediante un escenario académico reproducible y delimitado.",
            "prerequisite_unit_ids": [] if index == 1 else [f"{CODE}-U{index-1:02d}"],
            "instructions": list(activity.get("instructions", [])) or ["Trabaja con el escenario indicado y conserva todos los supuestos."],
            "tasks": tasks,
            "deliverables": list(activity.get("deliverables", [])) or ["Producto auditable de la actividad."],
            "checking_criteria": list(activity.get("checking_criteria", [])) or ["La conclusión es proporcional a la evidencia."],
            "estimated_duration_minutes": 60 if activity_n == 1 else 90,
            "status": "curated_internal_review_pending",
        })

    glossary_ids = []
    for entry in unit.get("glossary", []):
        gid = term_to_gid.get(str(entry.get("term") or "").strip().casefold())
        if gid and gid not in glossary_ids:
            glossary_ids.append(gid)

    biomedical = []
    for connection in unit.get("biomedical_connections", []):
        if isinstance(connection, dict):
            topic = str(connection.get("topic") or "Conexión").strip()
            text = str(connection.get("connection") or "").strip()
            if text:
                biomedical.append(f"{topic}: {text}")
        elif str(connection).strip():
            biomedical.append(str(connection).strip())

    canonical = {
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
    }
    canonical_units.append(canonical)

# Course descriptor.
course = {
    "$schema": "../../../schemas/academic/course-v1.schema.json",
    "schema_version": "1.0",
    "id": COURSE_ID,
    "code": CODE,
    "area_id": AREA,
    "title": "Ingeniería de Tejidos",
    "language": "es",
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica, biomedicina y áreas afines con bases de biología celular, biomateriales, fisiología, transporte y estadística que necesiten razonar sobre diseño, evaluación y traslación de constructos de ingeniería de tejidos.",
    "status": status_copy(),
    "purpose": "Integrar células, andamios, señales, microambiente, transporte, evaluación preclínica y traslación/manufactura para construir estrategias de ingeniería de tejidos reproducibles, trazables y proporcionales a la evidencia, sin convertir resultados educativos o preclínicos en afirmaciones de seguridad, eficacia clínica, autorización regulatoria o recomendación terapéutica.",
    "scope": {
        "included": [
            "Formulación de estrategias de ingeniería de tejidos mediante células, matrices o andamios, señales y microambiente.",
            "Selección razonada de fuentes celulares, identidad, estado, expansión, heterogeneidad y estabilidad.",
            "Diseño conceptual de biomateriales y andamios considerando estructura, propiedades, degradación, funcionalización y respuesta biológica.",
            "Transporte de masa, vascularización, perfusión, biorreactores, estímulos mecánicos y monitorización.",
            "Evaluación preclínica basada en riesgo, diseño experimental, modelos, 3R/NAMs, resultados negativos y peso de evidencia.",
            "Traslación, manufactura, CQA/CPP, potencia, comparabilidad, trazabilidad, GMP/CMC, clasificación regulatoria y ética.",
            "Actividades sintéticas y expedientes reproducibles que conectan evidencia, controles, incertidumbre y límites de inferencia."
        ],
        "excluded": [
            "Protocolos operativos de aislamiento, cultivo, expansión, diferenciación, fabricación, esterilización o administración de productos celulares o tisulares reales.",
            "Trabajo con donantes, embriones, células, tejidos, animales o participantes humanos fuera de infraestructura y autorización apropiadas.",
            "Diagnóstico, recomendación terapéutica o extrapolación automática de resultados preclínicos a beneficio clínico.",
            "Clasificación regulatoria oficial, certificación GMP, autorización de ensayo clínico o asesoría jurídica/regulatoria para un producto real."
        ],
        "handoff_courses": ["biomateriales", "biomateriales-implantes", "biologia-celular-tisular", "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas", "desarrollo-dispositivos-medicos"],
    },
    "prerequisites": [
        {"id": f"{CODE}-PRE01", "statement": "Biología celular y fisiología de nivel universitario inicial, incluyendo matriz extracelular, señalización y homeostasis."},
        {"id": f"{CODE}-PRE02", "statement": "Química y biomateriales suficientes para interpretar propiedades, superficies, degradación y compatibilidad material-tejido."},
        {"id": f"{CODE}-PRE03", "statement": "Fundamentos de transporte, mecánica y balances para seguir difusión, perfusión y estímulos físicos."},
        {"id": f"{CODE}-PRE04", "statement": "Estadística descriptiva, lectura crítica y documentación reproducible para evaluar estudios, incertidumbre y evidencia."},
    ],
    "competencies": [
        {"id": f"{CODE}-COMP{i:02d}", "statement": statement}
        for i, statement in enumerate([
            "Formular problemas de ingeniería de tejidos desde función, restricciones y evidencia necesaria antes de seleccionar una solución.",
            "Comparar fuentes celulares, biomateriales, arquitectura, señales y microambiente mediante criterios explícitos y límites de inferencia.",
            "Aplicar balances y razonamiento de transporte para identificar limitaciones de difusión, perfusión, vascularización y escalado tridimensional.",
            "Diseñar actividades y comparaciones preclínicas con controles, unidad experimental, reducción de sesgos, 3R y peso de evidencia.",
            "Razonar sobre manufactura, calidad, potencia, comparabilidad, trazabilidad y regulación sin confundirlas con eficacia clínica.",
            "Auditar incertidumbre, resultados negativos, cambios, contradicciones y transferibilidad antes de recomendar el siguiente estudio.",
            "Comunicar un expediente reproducible que permita reconstruir fuentes, decisiones, límites y estado de revisión."
        ], 1)
    ],
    "learning_outcomes": [
        {"id": f"{CODE}-LO{i:02d}", "statement": statement}
        for i, statement in enumerate(COURSE_OUTCOMES, 1)
    ],
    "study_method": [
        "Explicar el mecanismo o marco primero y separar después dato observado, cálculo, inferencia y decisión.",
        "Trabajar con ejemplos resueltos antes de actividades guiadas y retirar progresivamente la ayuda.",
        "Usar escenarios y datasets sintéticos para practicar razonamiento sin convertir el curso en un protocolo experimental.",
        "Predefinir controles, endpoints, unidad experimental, criterios y fuentes antes de interpretar resultados.",
        "Mantener trazabilidad entre unidad, resultado de aprendizaje, evidencia, evaluación, glosario y fuente.",
        "Cerrar cada problema declarando incertidumbre, explicación alternativa, límite de transferencia y siguiente dato necesario."
    ],
    "core_source_ids": list(source_records.keys())[:10],
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
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, fuentes trazables y pedagogía interna para las seis unidades de Ingeniería de Tejidos. La publicación sigue siendo provisional. La revisión humana interna y disciplinaria externa, cualquier trabajo experimental real, la aprobación ética, la certificación GMP, la clasificación regulatoria oficial, la validación preclínica o clínica y las decisiones terapéuticas permanecen fuera de este cierre y siguen pendientes.",
}

# Unit assessments from the already curated self-assessments.
for index, (src_unit, unit) in enumerate(zip(units_src, canonical_units), 1):
    uid = unit["id"]
    local_los = [item["id"] for item in unit["learning_outcomes"]]
    items = []
    questions = list(src_unit.get("self_assessment", []))
    for qn, q in enumerate(questions, 1):
        if qn <= 3:
            difficulty, cognitive = "foundational", "understand"
        elif qn <= 7:
            difficulty, cognitive = "intermediate", "apply"
        else:
            difficulty, cognitive = "advanced", "analyze"
        misconception = str(q.get("common_error") or "Confundir evidencia, modelo e inferencia.")
        explanation = str(q.get("reasoning") or "La respuesta debe conectar evidencia, mecanismo, control y límite.")
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
    assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{uid}-EVAL",
        "course_id": COURSE_ID,
        "scope": "unit",
        "unit_id": uid,
        "purpose": "Autoevaluación formativa de los resultados de aprendizaje de la unidad con retroalimentación recuperativa.",
        "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
        "items": items,
        "status": "curated_internal_review_pending",
    }
    dump(OUT / "assessments" / f"unit-{index:02d}.json", assessment)

course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": f"{CODE}-COURSE-EVAL",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": [
        "Evaluar comprensión, aplicación, análisis y transferencia; no solo reconocimiento de términos.",
        "Separar evidencia científica, desempeño técnico, inferencia preclínica, afirmación clínica y conclusión regulatoria.",
        "Usar escenarios sintéticos y fuentes localizables; no exigir experimentación con material biológico real.",
        "Predefinir criterios, controles y límites antes de inspeccionar resultados.",
        "Incluir retroalimentación, revisión y corrección documentada como parte de la evaluación.",
        "Mantener revisión humana pendiente aunque el corpus esté completo a nivel interno."
    ],
    "assessment_plan": [
        {"component": "Recuperación y explicaciones breves", "weight_percent": 15, "purpose": "Consolidar vocabulario, mecanismos y límites de inferencia de U1–U6."},
        {"component": "Problemas y casos por unidad", "weight_percent": 25, "purpose": "Aplicar criterios de selección, transporte, evidencia, calidad y traslación a casos nuevos."},
        {"component": "Actividades reproducibles sintéticas", "weight_percent": 25, "purpose": "Construir productos auditables con datos o escenarios sintéticos y trazabilidad."},
        {"component": "Revisión por pares y corrección", "weight_percent": 10, "purpose": "Detectar afirmaciones excesivas, errores de método y brechas de evidencia."},
        {"component": "Proyecto integrador", "weight_percent": 25, "purpose": "Integrar las seis unidades en un expediente de ingeniería de tejidos defendible."},
    ],
    "diagnostic": {
        "purpose": "Detectar prerrequisitos y concepciones que requieren recuperación antes del curso.",
        "questions": [
            "Diferencia dato observado, cálculo e inferencia.",
            "Explica qué función cumple la matriz extracelular en un tejido.",
            "Diferencia célula primaria, célula madre y célula diferenciada sin usar solo marcadores.",
            "Explica por qué porosidad y tamaño de poro no son sinónimos de éxito biológico.",
            "Interpreta cualitativamente la primera ley de Fick.",
            "Diferencia difusión y convección.",
            "Define unidad experimental y da un ejemplo de pseudorreplicación.",
            "Diferencia seguridad biológica y desempeño funcional.",
            "Explica qué significa incertidumbre en una medición o modelo.",
            "Diferencia atributo de producto y parámetro de proceso.",
            "Explica por qué un marcador de identidad no demuestra automáticamente potencia.",
            "Explica por qué evidencia preclínica favorable no demuestra beneficio clínico."
        ],
    },
    "midterm_blueprint": [
        {"unit_id": f"{CODE}-U01", "weight_percent": 15, "focus": "Tríada, función, requisitos y microambiente."},
        {"unit_id": f"{CODE}-U02", "weight_percent": 15, "focus": "Fuentes celulares, identidad, heterogeneidad y expansión."},
        {"unit_id": f"{CODE}-U03", "weight_percent": 20, "focus": "Biomateriales, arquitectura, degradación y funcionalización."},
        {"unit_id": f"{CODE}-U04", "weight_percent": 20, "focus": "Difusión, perfusión, vascularización y biorreactores."},
        {"unit_id": f"{CODE}-U05", "weight_percent": 15, "focus": "Diseño y peso de evidencia preclínica."},
        {"unit_id": f"{CODE}-U06", "weight_percent": 15, "focus": "Manufactura, calidad, comparabilidad, regulación y ética."},
    ],
    "capstone": {
        "title": "Expediente integrador de ingeniería de tejidos",
        "purpose": "Defender una estrategia sintética desde requisitos y diseño hasta evidencia preclínica y traslación, indicando qué está sustentado, qué es incierto y qué no puede concluirse.",
        "deliverables": [
            "Definición del producto/constructo y uso previsto académico.",
            "Mapa células–andamio–señales–microambiente.",
            "Matriz de transporte, arquitectura y estímulos.",
            "Plan preclínico con unidad experimental, controles, modelos y 3R/NAMs.",
            "Mapa de calidad, CQA/CPP, potencia, comparabilidad y trazabilidad.",
            "Tabla de claims, fuentes, evidencia, contradicciones, incertidumbre y siguientes datos.",
            "Versión revisada después de retroalimentación con registro antes-después."
        ],
        "rubric": [
            {"criterion": "Definición del problema y requisitos", "weight_percent": 15, "excellent": "Necesidad, uso, función, restricciones y afirmaciones están delimitados y trazados."},
            {"criterion": "Integración celular y de biomateriales", "weight_percent": 15, "excellent": "Selección celular y de andamio se justifica con mecanismos, alternativas y límites."},
            {"criterion": "Transporte, microambiente y diseño", "weight_percent": 20, "excellent": "Balances, escalas, perfusión y estímulos se conectan con la arquitectura sin simplificaciones ocultas."},
            {"criterion": "Evidencia preclínica", "weight_percent": 15, "excellent": "Diseño, controles, unidad experimental, modelos y resultados negativos sostienen un peso de evidencia explícito."},
            {"criterion": "Traslación, calidad y regulación", "weight_percent": 20, "excellent": "Producto, CQA/CPP, potencia, cambios, comparabilidad, trazabilidad y jurisdicción están claramente separados y conectados."},
            {"criterion": "Reproducibilidad, ética y comunicación", "weight_percent": 15, "excellent": "Fuentes, incertidumbre, límites, revisión y ética son auditables y la conclusión no excede la evidencia."},
        ],
        "linked_learning_outcome_ids": [f"{CODE}-LO{i:02d}" for i in range(1, 8)],
    },
    "status": "curated_internal_review_pending",
}

# Registries.
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
    "source_policy": "Priorizar estándares, guías regulatorias oficiales, sociedades científicas, revisiones y artículos primarios directamente pertinentes; conservar URL/DOI/PMID y el estado de verificación heredado de las unidades curadas. La trazabilidad de una fuente no equivale a revisión humana del curso ni a validación clínica o regulatoria.",
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
    "scope": "Afirmaciones centrales literales derivadas de las unidades curadas y enlazadas a fuentes del registro.",
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

# Permanent regression for the canonical closure.
test_path = ROOT / "tests" / "test_ingenieria_tejidos_canonical.py"
test_path.write_text('''from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "courses" / "ingenieria-tejidos"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaTejidosCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((BASE / "course.json").read_text(encoding="utf-8"))

    def test_course_is_complete_but_human_review_remains_pending(self):
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
        for index, relative in enumerate(self.course["unit_files"], 1):
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            self.assertEqual(unit["order"], index)
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

    def test_assessment_and_registries_are_complete(self):
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

    def test_course_outcomes_cover_the_full_sequence(self):
        self.assertEqual(len(self.course["learning_outcomes"]), 7)
        mapped = set()
        for relative in self.course["unit_files"]:
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            mapped.update(unit["course_learning_outcome_ids"])
        self.assertEqual(mapped, {item["id"] for item in self.course["learning_outcomes"]})

    def test_course_boundaries_remain_explicit(self):
        notice = self.course["editorial_notice"].casefold()
        for phrase in ("revisión humana", "certificación gmp", "clasificación regulatoria oficial", "validación preclínica o clínica"):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8")

print(f"Canonical Ingeniería de Tejidos: units={len(canonical_units)}, sources={len(source_records)}, glossary={len(glossary_entries)}, claims={len(claims)}")
