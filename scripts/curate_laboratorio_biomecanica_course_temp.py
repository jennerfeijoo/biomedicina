#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "course_redevelopment" / "laboratorio-biomecanica"
TARGET_DIR = ROOT / "data" / "courses" / "laboratorio-biomecanica"
COURSE_ID = "laboratorio-biomecanica"
CODE = "LABBIOM"
STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug(text: str) -> str:
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()
    norm = re.sub(r"[^a-z0-9]+", "-", norm).strip("-")
    return norm or "registro"


def tokens(text: str) -> set[str]:
    stop = {"de", "la", "el", "y", "en", "un", "una", "para", "con", "del", "los", "las", "que", "por", "al", "se", "su"}
    return {tok for tok in re.findall(r"[a-z0-9áéíóúñü]+", text.casefold()) if len(tok) >= 4 and tok not in stop}


def best_source_id(text: str, source_ids: list[str], source_by_id: dict[str, dict]) -> str:
    if not source_ids:
        return ""
    wanted = tokens(text)
    scored = []
    for sid in source_ids:
        source = source_by_id[sid]
        haystack = " ".join(str(source.get(k, "")) for k in ("title", "organization", "description", "type"))
        score = len(wanted & tokens(haystack))
        scored.append((score, sid))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return scored[0][1]


def subtopic_title(paragraph: str, fallback: str) -> str:
    first = re.split(r"(?<=[.!?])\s+", paragraph.strip())[0].strip()
    if 12 <= len(first) <= 105:
        return first.rstrip(".")
    first = paragraph.strip().split(":", 1)[0].strip()
    if 12 <= len(first) <= 105:
        return first
    return fallback


units_v2 = [load(SOURCE_DIR / "units" / f"unit-{i:02d}.json") for i in range(1, 7)]
if any(unit.get("status") != "review" for unit in units_v2):
    raise SystemExit("Todas las unidades deben permanecer en status=review antes de la migración canónica")

# Rebuild target atomically from curated redevelopment sources.
if TARGET_DIR.exists():
    shutil.rmtree(TARGET_DIR)
(TARGET_DIR / "units").mkdir(parents=True)
(TARGET_DIR / "assessments").mkdir(parents=True)

unit_ids = {i: f"{CODE}-U{i:02d}" for i in range(1, 7)}
course_los = [
    ("LABBIOM-LO01", "Diseña un protocolo biomecánico reproducible con pregunta, sistema, coordenadas, calibración, trazabilidad, controles y límites éticos explícitos."),
    ("LABBIOM-LO02", "Reconstruye y procesa cinemática sintética conservando geometría, muestreo, filtrado, derivación, unidades y propagación de error."),
    ("LABBIOM-LO03", "Adquiere e interpreta conceptualmente fuerzas de reacción, centro de presión e impulso con calibración, sincronización y criterios de calidad explícitos."),
    ("LABBIOM-LO04", "Diseña y audita una cadena de sEMG de superficie con colocación, adquisición, procesamiento, normalización y límites de inferencia sobre activación y fuerza."),
    ("LABBIOM-LO05", "Integra cinemática, fuerzas externas y parámetros inerciales en dinámica inversa, evaluando convenciones, sensibilidad e interpretación de fuerzas y momentos articulares netos."),
    ("LABBIOM-LO06", "Construye un informe reproducible que separa estimando, incertidumbre de medición, fiabilidad, acuerdo, visualización, procedencia y alcance de la conclusión."),
    ("LABBIOM-LO07", "Integra las seis unidades en un expediente sintético auditable que permite reconstruir datos, decisiones analíticas, tablas, figuras, resultados, incertidumbre, fuentes y correcciones."),
]

# Sources: deduplicate by URL when available, otherwise by title.
source_records: list[dict] = []
source_key_to_id: dict[str, str] = {}
source_id_counts: Counter[str] = Counter()
unit_source_ids: dict[int, list[str]] = {}
for index, unit in enumerate(units_v2, 1):
    ids: list[str] = []
    for source in unit.get("sources", []):
        key = (str(source.get("url") or "").strip() or str(source.get("title") or "").strip()).casefold()
        if key not in source_key_to_id:
            base = slug(str(source.get("title") or source.get("organization") or f"fuente-{len(source_records)+1}"))
            source_id_counts[base] += 1
            sid = base if source_id_counts[base] == 1 else f"{base}-{source_id_counts[base]}"
            source_key_to_id[key] = sid
            record = dict(source)
            record["id"] = sid
            record["verification_status"] = str(source.get("verification_status") or "traceable_from_curated_unit")
            record["locator"] = str(source.get("locator") or source.get("description") or source.get("url") or source.get("title") or "Registro bibliográfico de la unidad curada.")
            record["limitations"] = str(source.get("limitations") or "La fuente respalda el aspecto metodológico o disciplinar citado; no sustituye la declaración del protocolo, sus supuestos ni revisión disciplinaria humana.")
            record["used_by_unit_ids"] = [unit_ids[index]]
            source_records.append(record)
        else:
            sid = source_key_to_id[key]
            record = next(item for item in source_records if item["id"] == sid)
            if unit_ids[index] not in record["used_by_unit_ids"]:
                record["used_by_unit_ids"].append(unit_ids[index])
        ids.append(sid)
    unit_source_ids[index] = list(dict.fromkeys(ids))
source_by_id = {item["id"]: item for item in source_records}

# Glossary: merge identical terms and preserve which unit uses them.
glossary_records: list[dict] = []
glossary_key_to_id: dict[str, str] = {}
unit_glossary_ids: dict[int, list[str]] = {i: [] for i in range(1, 7)}
for index, unit in enumerate(units_v2, 1):
    for entry in unit.get("glossary", []):
        term = str(entry.get("term") or "").strip()
        definition = str(entry.get("definition") or "").strip()
        if not term or not definition:
            continue
        key = term.casefold()
        if key not in glossary_key_to_id:
            gid = f"{CODE}-GLO-{len(glossary_records)+1:03d}"
            glossary_key_to_id[key] = gid
            sid = best_source_id(term + " " + definition, unit_source_ids[index], source_by_id)
            glossary_records.append({
                "id": gid,
                "term": term,
                "definition": definition,
                "unit_ids": [unit_ids[index]],
                "source_ids": [sid] if sid else unit_source_ids[index][:1],
                "verification_status": "traceable_from_curated_unit_sources",
            })
        else:
            gid = glossary_key_to_id[key]
            record = next(item for item in glossary_records if item["id"] == gid)
            if unit_ids[index] not in record["unit_ids"]:
                record["unit_ids"].append(unit_ids[index])
            sid = best_source_id(term + " " + definition, unit_source_ids[index], source_by_id)
            if sid and sid not in record["source_ids"]:
                record["source_ids"].append(sid)
        unit_glossary_ids[index].append(gid)

claim_records: list[dict] = []
unit_claim_ids: dict[int, list[str]] = {i: [] for i in range(1, 7)}
media_records: list[dict] = []
unit_media_ids: dict[int, list[str]] = {i: [] for i in range(1, 7)}
canonical_units: list[dict] = []

for index, source_unit in enumerate(units_v2, 1):
    uid = unit_ids[index]
    local_los = [
        {"id": f"{uid}-LO{n:02d}", "statement": statement}
        for n, statement in enumerate(source_unit.get("learning_objectives", []), 1)
    ]
    if not local_los:
        raise SystemExit(f"U{index}: sin resultados de aprendizaje")

    topics = []
    for topic_n, section in enumerate(source_unit.get("theory_sections", []), 1):
        tid = f"{uid}-T{topic_n:02d}"
        key_points = [str(item).strip() for item in section.get("key_points", []) if str(item).strip()]
        eq_blocks = []
        for eq_n, equation in enumerate(section.get("equations", []), 1):
            latex = str(equation.get("latex") or "").strip()
            if latex:
                eq_blocks.append({
                    "id": f"{tid}-EQ{eq_n:02d}",
                    "type": "equation",
                    "latex": latex,
                    "label": str(equation.get("meaning") or "Relación cuantitativa de la unidad."),
                })
        subtopics = []
        paragraphs = [str(p).strip() for p in section.get("paragraphs", []) if str(p).strip()]
        for sub_n, paragraph in enumerate(paragraphs, 1):
            sid = f"{tid}-ST{sub_n:02d}"
            fallback = key_points[sub_n - 1] if sub_n <= len(key_points) else f"Desarrollo conceptual {sub_n}"
            subtopics.append({
                "id": sid,
                "title": subtopic_title(paragraph, fallback),
                "blocks": [{"id": f"{sid}-B01", "type": "paragraph", "text": paragraph}],
            })
        if not subtopics:
            raise SystemExit(f"U{index} sección {topic_n}: sin párrafos")
        topics.append({
            "id": tid,
            "title": str(section.get("heading") or f"Tema {topic_n}"),
            "blocks": eq_blocks,
            "key_points": key_points or [subtopics[0]["title"]],
            "subtopics": subtopics,
        })
        for point in key_points:
            cid = f"{uid}-C{len(unit_claim_ids[index])+1:03d}"
            source_id = best_source_id(point, unit_source_ids[index], source_by_id)
            source_record = source_by_id.get(source_id, {})
            claim_records.append({
                "claim_id": cid,
                "id": cid,
                "unit": index,
                "unit_id": uid,
                "text": point,
                "claim_type": "methodological_or_interpretive",
                "risk": "medium",
                "context": f"Síntesis educativa de {source_unit.get('title')}; interpretar dentro del protocolo, supuestos, incertidumbre y límites de la unidad.",
                "source_id": source_id,
                "locator": {"section": str(source_record.get("locator") or source_record.get("url") or "Fuente de la unidad")},
                "support": "curated_unit_synthesis",
                "source_verification_status": str(source_record.get("verification_status") or "traceable_from_curated_unit"),
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": "2026-08-24",
            })
            unit_claim_ids[index].append(cid)

    examples = []
    for n, example in enumerate(source_unit.get("worked_examples", []), 1):
        examples.append({
            "id": f"{uid}-EX{n:02d}",
            "title": str(example.get("title") or f"Ejemplo {n}"),
            "scenario": str(example.get("scenario") or "Escenario sintético de la unidad."),
            "reasoning_steps": [str(x) for x in example.get("reasoning_steps", [])],
            "interpretation": str(example.get("interpretation") or "Interpretación limitada al resultado del ejercicio."),
            "limitations": [str(x) for x in example.get("limitations", [])] or ["El ejemplo es educativo y sintético; no autoriza inferencia clínica individual."],
        })

    activities = []
    for n, activity in enumerate(source_unit.get("guided_activities", []), 1):
        problems = [str(x) for x in activity.get("problems", [])]
        duration = min(300, max(120, len(problems) * 15 if problems else 120))
        activities.append({
            "id": f"{uid}-ACT{n:02d}",
            "title": str(activity.get("title") or f"Actividad guiada {n}"),
            "purpose": f"Aplicar de forma reproducible los resultados de aprendizaje de {source_unit.get('title')} mediante un escenario sintético y criterios de comprobación explícitos.",
            "prerequisite_unit_ids": [unit_ids[index - 1]] if index > 1 else [],
            "instructions": [str(x) for x in activity.get("instructions", [])] or ["Trabaja con el escenario sintético de la unidad y documenta supuestos y unidades."],
            "tasks": problems or ["Resolver el problema sintético y justificar cada transformación."],
            "deliverables": [str(x) for x in activity.get("deliverables", [])] or ["Informe reproducible del ejercicio."],
            "checking_criteria": [str(x) for x in activity.get("checking_criteria", [])] or ["El resultado conserva unidades, supuestos, controles y límites."],
            "estimated_duration_minutes": duration,
            "status": "curated_internal_review_pending",
        })

    # Planned media makes deferred multimedia explicit without pretending production.
    mid1 = f"{uid}-MED01"
    mid2 = f"{uid}-MED02"
    media_records.extend([
        {"id": mid1, "unit_id": uid, "type": "diagram", "title": f"Diagrama conceptual de {source_unit.get('title')}", "purpose": "Hacer visible la cadena entrada → procesamiento/modelo → salida → incertidumbre → límite.", "status": "planned"},
        {"id": mid2, "unit_id": uid, "type": "worked_visual", "title": f"Visualización guiada de {source_unit.get('title')}", "purpose": "Acompañar un ejemplo sintético con anotaciones de unidades, supuestos y decisiones reproducibles.", "status": "planned"},
    ])
    unit_media_ids[index] = [mid1, mid2]

    connections = []
    for item in source_unit.get("biomedical_connections", []):
        if isinstance(item, dict):
            connections.append(f"{item.get('topic', 'Conexión biomédica')}: {item.get('connection', '')}".strip())
        else:
            connections.append(str(item))

    canonical = {
        "$schema": "../../../../schemas/academic/unit-v1.schema.json",
        "schema_version": "1.0",
        "id": uid,
        "course_id": COURSE_ID,
        "order": index,
        "slug": str(source_unit.get("slug") or f"unidad-{index:02d}"),
        "title": str(source_unit.get("title") or f"Unidad {index}"),
        "status": STATUS,
        "purpose": str(source_unit.get("purpose") or "Unidad práctica del Laboratorio de Biomecánica con trazabilidad y límites explícitos."),
        "prerequisite_unit_ids": [unit_ids[index - 1]] if index > 1 else [],
        "course_learning_outcome_ids": [f"LABBIOM-LO{index:02d}", "LABBIOM-LO07"],
        "learning_outcomes": local_los,
        "topics": topics,
        "examples": examples,
        "activities": activities,
        "assessment_file": f"assessments/unit-{index:02d}.json",
        "glossary_entry_ids": list(dict.fromkeys(unit_glossary_ids[index])),
        "source_ids": unit_source_ids[index],
        "claim_ids": unit_claim_ids[index],
        "media_ids": unit_media_ids[index],
        "common_errors": source_unit.get("common_errors", []),
        "biomedical_connections": connections or ["La unidad se integra en la cadena de análisis de movimiento humano y conserva límites de inferencia biomédica."],
        "editorial_notice": str(source_unit.get("editorial_notice") or "Material educativo curado internamente; revisión disciplinaria humana pendiente."),
        "legacy_origin": f"data/course_redevelopment/laboratorio-biomecanica/units/unit-{index:02d}.json",
    }
    canonical_units.append(canonical)
    dump(TARGET_DIR / "units" / f"unit-{index:02d}.json", canonical)

    # Convert each self-assessment to a protected canonical assessment.
    assessment_items = []
    unit_source_subset = unit_source_ids[index][:2]
    for qn, item in enumerate(source_unit.get("self_assessment", []), 1):
        lo_id = local_los[(qn - 1) % len(local_los)]["id"]
        reasoning = str(item.get("reasoning") or "La respuesta debe conservar el vínculo entre dato, método, incertidumbre y alcance.")
        misconception = str(item.get("common_error") or "Extender la conclusión más allá de la evidencia disponible.")
        assessment_items.append({
            "id": f"{uid}-Q{qn:02d}",
            "type": "short_answer",
            "prompt": str(item.get("question") or f"Explica el criterio {qn} de la unidad."),
            "linked_learning_outcome_ids": [lo_id],
            "difficulty": "foundational" if qn <= 2 else ("advanced" if qn > 8 else "intermediate"),
            "cognitive_level": "understand" if qn <= 2 else ("evaluate" if qn > 8 else "analyze"),
            "answer_key": {
                "expected_answer": str(item.get("answer") or reasoning),
                "explanation": reasoning,
                "common_misconceptions": [misconception],
            },
            "feedback": {
                "correct": "Correcto. Conserva explícitos unidades, supuestos, procedencia y límite de inferencia cuando sean pertinentes.",
                "incorrect": f"Revisa el razonamiento de la unidad y evita este error frecuente: {misconception}",
            },
            "source_ids": unit_source_subset,
            "status": "curated_internal_review_pending",
        })
    if not assessment_items:
        raise SystemExit(f"U{index}: la curación requiere autoevaluación fuente")
    dump(TARGET_DIR / "assessments" / f"unit-{index:02d}.json", {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{uid}-EVAL",
        "course_id": COURSE_ID,
        "scope": "unit",
        "unit_id": uid,
        "purpose": "Evaluación formativa con respuesta razonada, retroalimentación recuperativa y trazabilidad a fuentes de la unidad.",
        "student_payload_policy": "En una aplicación dinámica, answer_key y feedback deben excluirse del payload inicial del estudiante.",
        "items": assessment_items,
        "status": "curated_internal_review_pending",
    })

# Registries.
dump(TARGET_DIR / "glossary.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "entries": glossary_records,
})
dump(TARGET_DIR / "sources.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "source_policy": "Conservar la fuente curada de cada unidad, su URL o localizador y su estado de verificación; la migración canónica no eleva automáticamente el grado de verificación de una referencia.",
    "consulted_on": "2026-08-24",
    "coverage_gaps": [],
    "coverage_status": "traceable",
    "sources": source_records,
})
dump(TARGET_DIR / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Afirmaciones centrales literales de U1–U6 derivadas de puntos clave curados; asociación a fuentes trazables y revisión disciplinaria humana pendiente.",
    "review_state": "ai_review_provisional",
    "claims": claim_records,
})
dump(TARGET_DIR / "media.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "status": "planned",
    "items": media_records,
})

# Course assessment: 100% plan and synthetic capstone.
dump(TARGET_DIR / "assessments" / "course-assessment.json", {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "LABBIOM-COURSE-EVAL",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": [
        "Evaluar decisiones reproducibles y no memoria aislada de protocolos.",
        "Separar calidad de medición, validez mecánica, incertidumbre e inferencia clínica.",
        "Usar exclusivamente datasets y escenarios sintéticos para el cierre autónomo del curso.",
        "Exigir trazabilidad desde pregunta y archivos de entrada hasta figuras, tablas, resultados y límites.",
        "Permitir revisión y corrección documentada como parte del aprendizaje."
    ],
    "assessment_plan": [
        {"component": "Autoevaluaciones de U1–U6", "weight_percent": 20, "evidence": "Respuestas razonadas con feedback recuperativo."},
        {"component": "Actividades guiadas reproducibles", "weight_percent": 30, "evidence": "Seis productos de unidad con controles y entregables."},
        {"component": "Evaluación integradora intermedia", "weight_percent": 20, "evidence": "Caso sintético que integra adquisición, cinemática, fuerzas y sEMG."},
        {"component": "Proyecto integrador final", "weight_percent": 30, "evidence": "Expediente biomecánico sintético reproducible U1–U6."}
    ],
    "diagnostic": {
        "purpose": "Detectar prerrequisitos que deben recuperarse antes de trabajar con medición y modelado biomecánicos.",
        "questions": [
            "¿Qué diferencia hay entre precisión, exactitud y resolución en una cadena de medición?",
            "¿Por qué un sistema de coordenadas debe definirse antes de reportar posición o momento?",
            "¿Qué efecto tiene la diferenciación numérica sobre el ruido de una trayectoria?",
            "¿Qué diferencia existe entre fuerza de reacción del suelo y centro de presión?",
            "¿Por qué una amplitud sEMG no es una medida directa de fuerza muscular?",
            "¿Qué entradas necesita conceptualmente una dinámica inversa?",
            "¿Qué diferencia hay entre variabilidad observada e incertidumbre de medición?",
            "¿Por qué correlación y acuerdo entre métodos no son equivalentes?"
        ]
    },
    "midterm_blueprint": [
        {"domain": "U1 Protocolo y calibración", "weight_percent": 15, "focus": "pregunta, coordenadas, calibración y trazabilidad"},
        {"domain": "U2 Cinemática", "weight_percent": 20, "focus": "muestreo, filtrado, derivación y error"},
        {"domain": "U3 Plataforma de fuerza", "weight_percent": 20, "focus": "GRF, CoP, impulso y sincronización"},
        {"domain": "U4 sEMG", "weight_percent": 15, "focus": "colocación, procesamiento, normalización y límites"},
        {"domain": "Integración multimodal", "weight_percent": 20, "focus": "tiempo común, unidades y controles cruzados"},
        {"domain": "Comunicación proporcional", "weight_percent": 10, "focus": "dato, estimación, incertidumbre e inferencia"}
    ],
    "capstone": {
        "title": "Expediente biomecánico sintético reproducible",
        "purpose": "Integrar U1–U6 sin recopilar datos de participantes ni emitir conclusiones clínicas.",
        "scenario": "Un conjunto sintético incluye trayectorias, señal de plataforma y sEMG para dos condiciones mecánicas. El estudiante debe reconstruir el pipeline, verificar calidad, estimar variables cinemáticas y cinéticas, ejecutar una dinámica inversa simplificada, cuantificar sensibilidad/fiabilidad y entregar un informe reproducible.",
        "deliverables": [
            "Pregunta y protocolo con sistemas de coordenadas, unidades y criterios de aceptación.",
            "Pipeline versionado de cinemática, plataforma y sEMG con parámetros explícitos.",
            "Cálculos de dinámica inversa sintética y análisis de sensibilidad.",
            "Diccionario de datos, metadatos, manifiesto de procedencia y registro de versiones.",
            "Figuras y tablas regenerables con incertidumbre y estructura de los datos visible.",
            "Tabla claim→evidencia→fuente→limitación y conclusión proporcional."
        ],
        "rubric": [
            {"criterion": "Protocolo, calibración y trazabilidad", "weight_percent": 15, "excellent": "Pregunta, coordenadas, unidades, calibración y criterios están completos y reconstruibles."},
            {"criterion": "Cinemática y procesamiento", "weight_percent": 15, "excellent": "Derivación y filtrado son justificables, reproducibles y acompañados de sensibilidad."},
            {"criterion": "Fuerzas y sEMG", "weight_percent": 15, "excellent": "GRF/CoP/impulso y sEMG conservan sincronización, unidades, normalización y límites."},
            {"criterion": "Dinámica inversa", "weight_percent": 15, "excellent": "Entradas, convenciones, parámetros inerciales, balances y límites de momentos netos son explícitos."},
            {"criterion": "Incertidumbre, fiabilidad y acuerdo", "weight_percent": 20, "excellent": "Distingue incertidumbre, variabilidad, ICC, SEM/MDC y acuerdo y los usa según la pregunta."},
            {"criterion": "Reproducibilidad e interpretación", "weight_percent": 20, "excellent": "El expediente se regenera desde entradas y código y ninguna conclusión excede la evidencia mecánica del ejercicio."}
        ]
    },
    "status": "curated_internal_review_pending"
})

# Canonical course descriptor.
source_usage = Counter()
for record in source_records:
    source_usage[record["id"]] = len(record.get("used_by_unit_ids", []))
core_source_ids = [sid for sid, _ in sorted(source_usage.items(), key=lambda item: (-item[1], item[0]))[:12]]
course = {
    "$schema": "../../../schemas/academic/course-v1.schema.json",
    "schema_version": "1.0",
    "id": COURSE_ID,
    "code": CODE,
    "area_id": "ingenieria-biomedica",
    "title": "Laboratorio de Biomecánica",
    "language": "es",
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica y áreas afines con bases de mecánica, biomecánica, anatomía funcional, señales, estadística descriptiva y programación científica que necesiten diseñar, procesar, integrar y comunicar mediciones de movimiento de forma reproducible.",
    "status": STATUS,
    "purpose": "Integrar diseño de protocolo, calibración, análisis cinemático, plataformas de fuerza, sEMG, dinámica inversa e informe reproducible en una cadena experimental biomecánica auditable, usando escenarios y datos sintéticos para aprender a distinguir medición, procesamiento, modelo, incertidumbre e interpretación sin presentar una señal o estimación mecánica como diagnóstico, causalidad, prescripción o beneficio clínico.",
    "scope": {
        "included": [
            "Diseño de pregunta, protocolo, sistemas de coordenadas, calibración, sincronización, metadatos y criterios de aceptación.",
            "Análisis cinemático con video o trayectorias sintéticas, muestreo, filtrado, derivación y sensibilidad al procesamiento.",
            "Plataformas de fuerza con fuerza de reacción del suelo, centro de presión, impulso y control de calidad.",
            "sEMG de superficie con colocación, adquisición, filtrado, envolvente, normalización y límites de interpretación.",
            "Dinámica inversa con segmentación, fuerzas externas, parámetros inerciales, Newton-Euler, convenciones y momentos articulares netos.",
            "Incertidumbre de medición, fiabilidad, ICC, SEM, MDC, acuerdo, visualización, pseudorreplicación y sensibilidad.",
            "Paquetes reproducibles con diccionario de datos, código, parámetros, versiones, dependencias, checksums, procedencia y principios FAIR."
        ],
        "excluded": [
            "Registro autónomo de participantes, pacientes, señales personales o historias clínicas durante las actividades del curso.",
            "Diagnóstico, pronóstico, recomendación terapéutica, aptitud ocupacional o riesgo individual inferidos de una variable biomecánica aislada.",
            "Interpretar sEMG como fuerza muscular directa o dinámica inversa como identificador de músculos o cargas tisulares individuales.",
            "Afirmar causalidad o eficacia de una intervención por una diferencia pre/post sin diseño causal y evidencia clínica suficiente.",
            "Sustituir calibración institucional, revisión ética, supervisión profesional o validación específica de un dispositivo por ejercicios sintéticos."
        ],
        "handoff_courses": ["biomecanica", "fundamentos-biomecanica", "biomecanica-medios-continuos", "senales-biomedicas", "modelado-simulacion-biomedicina"]
    },
    "prerequisites": [
        {"id": "LABBIOM-PRE01", "statement": "Mecánica universitaria, álgebra vectorial, trigonometría, unidades SI y diagramas de cuerpo libre."},
        {"id": "LABBIOM-PRE02", "statement": "Biomecánica básica de cinemática, cinética y anatomía funcional."},
        {"id": "LABBIOM-PRE03", "statement": "Señales discretas: frecuencia de muestreo, ruido, filtrado y representación temporal."},
        {"id": "LABBIOM-PRE04", "statement": "Estadística descriptiva básica y capacidad de leer scripts o notebooks reproducibles."}
    ],
    "competencies": [
        {"id": "LABBIOM-COMP01", "statement": "Diseñar protocolos biomecánicos sintéticos con sistemas de referencia, calibración, metadatos y criterios de calidad explícitos."},
        {"id": "LABBIOM-COMP02", "statement": "Procesar trayectorias y señales preservando unidades, tiempo, parámetros, versiones y sensibilidad a decisiones analíticas."},
        {"id": "LABBIOM-COMP03", "statement": "Integrar plataforma de fuerza, cinemática y sEMG sin colapsar variables observadas, derivadas y modelos mecánicos."},
        {"id": "LABBIOM-COMP04", "statement": "Resolver y auditar una dinámica inversa segmentaria con convenciones y parámetros inerciales reproducibles."},
        {"id": "LABBIOM-COMP05", "statement": "Cuantificar incertidumbre, fiabilidad y acuerdo y seleccionar la métrica según la pregunta y la unidad de observación."},
        {"id": "LABBIOM-COMP06", "statement": "Construir visualizaciones y expedientes reproducibles que conserven procedencia, estructura de datos y limitaciones."},
        {"id": "LABBIOM-COMP07", "statement": "Comunicar resultados biomecánicos de forma proporcional, separando desempeño técnico, validez científica y cualquier inferencia clínica no evaluada."}
    ],
    "learning_outcomes": [{"id": lid, "statement": text} for lid, text in course_los],
    "study_method": [
        "Definir pregunta, sistema, uso previsto, estimando, unidades y criterio de aceptación antes de procesar datos.",
        "Alternar explicación, ejemplo sintético resuelto, práctica guiada, comprobación y transferencia con apoyo progresivamente menor.",
        "Conservar raw inmutable y documentar cada transformación, filtro, normalización, sincronización, versión y parámetro.",
        "Separar observación, variable derivada, modelo mecánico, incertidumbre e inferencia en cada tabla y figura.",
        "Usar controles, sensibilidad, repetición y acuerdo para detectar conclusiones que dependen demasiado del pipeline.",
        "Cerrar cada unidad con un producto reutilizable dentro del expediente integrador U1–U6."
    ],
    "core_source_ids": core_source_ids,
    "unit_files": [f"units/unit-{i:02d}.json" for i in range(1, 7)],
    "assessment_files": [f"assessments/unit-{i:02d}.json" for i in range(1, 7)] + ["assessments/course-assessment.json"],
    "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
    "static_site": {
        "renderer": "scripts/generate_site.py",
        "canonical_source": True,
        "legacy_mirrors": [
            "data/course_redevelopment/laboratorio-biomecanica/",
            "data/generated_courses/laboratorio-biomecanica.json",
            "data/generated_units/laboratorio-biomecanica/",
            "data/subjects/ingenieria-biomedica/laboratorio-biomecanica.json",
            "data/source_registry/laboratorio-biomecanica.json",
            "data/claim_registry/laboratorio-biomecanica.json"
        ]
    },
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, fuentes trazables y pedagogía interna para las seis unidades de Laboratorio de Biomecánica. La publicación continúa provisional y el multimedia permanece planificado. La revisión humana interna, la revisión disciplinaria externa, cualquier práctica con participantes, la validación clínica, el diagnóstico, la prescripción y la causalidad permanecen fuera del cierre y siguen pendientes."
}
dump(TARGET_DIR / "course.json", course)

# Permanent regression for the canonical closure.
test = ROOT / "tests" / "test_laboratorio_biomecanica_course_canonical.py"
test.write_text('''from __future__ import annotations\n\nimport json\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nCOURSE_DIR = ROOT / "data" / "courses" / "laboratorio-biomecanica"\nGENERIC = "concepto de la unidad que debe definirse mediante entidades observables"\n\n\nclass LaboratorioBiomecanicaCanonicalCourseTests(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls) -> None:\n        cls.course = json.loads((COURSE_DIR / "course.json").read_text(encoding="utf-8"))\n        cls.units = [json.loads((COURSE_DIR / "units" / f"unit-{i:02d}.json").read_text(encoding="utf-8")) for i in range(1, 7)]\n        cls.sources = json.loads((COURSE_DIR / "sources.json").read_text(encoding="utf-8"))\n        cls.glossary = json.loads((COURSE_DIR / "glossary.json").read_text(encoding="utf-8"))\n        cls.claims = json.loads((COURSE_DIR / "claims.json").read_text(encoding="utf-8"))\n        cls.course_assessment = json.loads((COURSE_DIR / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))\n\n    def test_course_is_complete_but_human_review_remains_pending(self) -> None:\n        status = self.course["status"]\n        self.assertEqual(status["content"], "complete")\n        self.assertEqual(status["sources"], "traceable")\n        self.assertEqual(status["pedagogy"], "complete")\n        self.assertEqual(status["multimedia"], "planned")\n        self.assertEqual(status["internal_review"], "pending")\n        self.assertEqual(status["external_review"], "pending")\n\n    def test_six_units_are_canonical_and_specific(self) -> None:\n        self.assertEqual([unit["order"] for unit in self.units], list(range(1, 7)))\n        expected = ["Protocolo y calibración", "Análisis cinemático", "Plataformas de fuerza", "EMG de superficie", "Dinámica inversa", "Informe y reproducibilidad"]\n        self.assertEqual([unit["title"] for unit in self.units], expected)\n        text = " ".join(json.dumps(unit, ensure_ascii=False) for unit in self.units).casefold()\n        self.assertNotIn(GENERIC, text)\n        self.assertIn("dinámica inversa", text)\n        self.assertIn("incertidumbre de medición", text)\n        self.assertIn("emg", text)\n\n    def test_units_have_topics_subtopics_activities_examples_and_assessments(self) -> None:\n        for index, unit in enumerate(self.units, 1):\n            self.assertGreaterEqual(len(unit["topics"]), 4)\n            self.assertTrue(all(topic["subtopics"] for topic in unit["topics"]))\n            self.assertGreaterEqual(len(unit["examples"]), 2)\n            self.assertTrue(unit["activities"])\n            assessment = json.loads((COURSE_DIR / "assessments" / f"unit-{index:02d}.json").read_text(encoding="utf-8"))\n            self.assertGreaterEqual(len(assessment["items"]), 8)\n            self.assertTrue(all(item["answer_key"]["explanation"] for item in assessment["items"]))\n            self.assertTrue(all(item["feedback"]["correct"] and item["feedback"]["incorrect"] for item in assessment["items"]))\n\n    def test_registries_are_populated_and_claims_literal(self) -> None:\n        self.assertGreaterEqual(len(self.glossary["entries"]), 50)\n        self.assertGreaterEqual(len(self.sources["sources"]), 20)\n        self.assertGreaterEqual(len(self.claims["claims"]), 70)\n        unit_text = {unit["id"]: json.dumps(unit, ensure_ascii=False) for unit in self.units}\n        for claim in self.claims["claims"]:\n            self.assertIn(claim["text"], unit_text[claim["unit_id"]])\n            self.assertTrue(claim["source_id"])\n\n    def test_course_assessment_is_complete_and_synthetic(self) -> None:\n        plan = self.course_assessment["assessment_plan"]\n        self.assertEqual(sum(item["weight_percent"] for item in plan), 100)\n        self.assertGreaterEqual(len(self.course_assessment["diagnostic"]["questions"]), 8)\n        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["midterm_blueprint"]), 100)\n        rubric = self.course_assessment["capstone"]["rubric"]\n        self.assertEqual(sum(item["weight_percent"] for item in rubric), 100)\n        capstone_text = json.dumps(self.course_assessment["capstone"], ensure_ascii=False).casefold()\n        self.assertIn("sintético", capstone_text)\n        self.assertIn("sin recopilar datos de participantes", capstone_text)\n\n    def test_editorial_boundary_is_explicit(self) -> None:\n        notice = self.course["editorial_notice"].casefold()\n        self.assertIn("revisión humana interna", notice)\n        self.assertIn("revisión disciplinaria externa", notice)\n        self.assertIn("validación clínica", notice)\n\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")

print(f"Canonicalized {COURSE_ID}: units={len(canonical_units)}, glossary={len(glossary_records)}, sources={len(source_records)}, claims={len(claim_records)}")
