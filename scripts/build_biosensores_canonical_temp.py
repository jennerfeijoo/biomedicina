#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "course_redevelopment" / "biosensores" / "units"
COURSE_DIR = ROOT / "data" / "courses" / "biosensores"
CODE = "BIOSEN"
COURSE_ID = "biosensores"
GENERIC = "concepto de la unidad que debe definirse"
STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}

COURSE_LOS = [
    ("BIOSEN-LO01", "Construye una arquitectura de biosensor que conecta mensurando, bioreceptor, transductor, acondicionamiento y señal con unidades, controles y trazabilidad explícitos."),
    ("BIOSEN-LO02", "Selecciona y justifica estrategias de reconocimiento biológico mediante afinidad, cinética, catálisis, anticuerpos, sondas de ácidos nucleicos o aptámeros, distinguiendo selectividad, estabilidad y limitaciones."),
    ("BIOSEN-LO03", "Compara modalidades electroquímicas, ópticas, piezoeléctricas o acústicas y térmicas y determina qué magnitud física se transforma, cómo se calibra y qué interferencias condicionan la medida."),
    ("BIOSEN-LO04", "Diseña una interfaz de inmovilización y manejo de muestra que integra química de superficies, orientación, pasivación, biofouling, transporte de masa y microfluídica con parámetros reproducibles."),
    ("BIOSEN-LO05", "Caracteriza desempeño analítico mediante calibración, sensibilidad analítica, precisión, sesgo, intervalo, LoB/LoD/LoQ, interferencias y comparación de métodos sin confundir esas propiedades con desempeño diagnóstico."),
    ("BIOSEN-LO06", "Evalúa un uso point-of-care, portátil o wearable mediante uso previsto, desempeño clínico, valores predictivos, prevalencia, robustez, completitud, factores humanos, integridad de datos, riesgo y ciclo de vida."),
    ("BIOSEN-LO07", "Integra las seis unidades en un expediente reproducible de evidencia que separa desempeño técnico, analítico, clínico, utilidad y afirmaciones regulatorias y declara la evidencia adicional necesaria antes de transferir conclusiones."),
]

UNIT_TO_COURSE_LOS = {
    1: ["BIOSEN-LO01", "BIOSEN-LO07"],
    2: ["BIOSEN-LO02", "BIOSEN-LO07"],
    3: ["BIOSEN-LO03", "BIOSEN-LO07"],
    4: ["BIOSEN-LO04", "BIOSEN-LO07"],
    5: ["BIOSEN-LO05", "BIOSEN-LO07"],
    6: ["BIOSEN-LO06", "BIOSEN-LO07"],
}

STOPWORDS = {
    "para", "como", "con", "una", "uno", "unos", "unas", "del", "las", "los", "que", "por", "sin", "entre", "desde", "sobre",
    "esta", "este", "estos", "estas", "cada", "más", "menos", "debe", "puede", "cuando", "donde", "dentro", "fuera", "their", "the",
    "and", "with", "from", "this", "that", "into", "using", "used", "use", "un", "al", "el", "la", "en", "y", "o", "se", "su",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKD", str(text or "").casefold())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def slugify(text: str) -> str:
    value = normalize(text).replace(" ", "-")
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "source"


def keywords(text: str) -> set[str]:
    return {token for token in normalize(text).split() if len(token) >= 4 and token not in STOPWORDS}


def source_key(source: dict) -> str:
    doi = str(source.get("doi") or "").strip().casefold()
    if doi:
        return "doi:" + doi
    url = str(source.get("url") or "").strip().rstrip("/").casefold()
    if url:
        return "url:" + url
    return "title:" + normalize(source.get("title") or "")


def source_text(source: dict) -> str:
    return " ".join(
        str(source.get(key) or "")
        for key in ("title", "description", "type", "organization", "authors", "authors_or_organization", "journal")
    )


def best_source_id(text: str, candidates: list[str], source_by_id: dict[str, dict]) -> str:
    wanted = keywords(text)
    best = candidates[0]
    best_score = -1
    for candidate in candidates:
        score = len(wanted & keywords(source_text(source_by_id[candidate])))
        if score > best_score:
            best = candidate
            best_score = score
    return best


units = [load(SOURCE_DIR / f"unit-{n:02d}.json") for n in range(1, 7)]
assert all(unit["status"] == "review" for unit in units)
assert all(GENERIC not in json.dumps(unit, ensure_ascii=False).casefold() for unit in units)

# Rebuild the canonical directory atomically in the worktree.
if COURSE_DIR.exists():
    shutil.rmtree(COURSE_DIR)
(COURSE_DIR / "units").mkdir(parents=True)
(COURSE_DIR / "assessments").mkdir(parents=True)

# Aggregate and de-duplicate sources across all curated units.
source_by_key: dict[str, dict] = {}
source_units: dict[str, set[str]] = defaultdict(set)
unit_source_keys: dict[int, list[str]] = defaultdict(list)
for n, unit in enumerate(units, start=1):
    unit_id = f"{CODE}-U{n:02d}"
    for source in unit.get("sources", []):
        key = source_key(source)
        if key not in source_by_key:
            source_by_key[key] = dict(source)
        source_units[key].add(unit_id)
        if key not in unit_source_keys[n]:
            unit_source_keys[n].append(key)

used_source_ids: set[str] = set()
key_to_source_id: dict[str, str] = {}
canonical_sources: list[dict] = []
for key, source in source_by_key.items():
    base = slugify(source.get("title") or "source")[:90]
    candidate = base
    suffix = 2
    while candidate in used_source_ids:
        candidate = f"{base}-{suffix}"
        suffix += 1
    used_source_ids.add(candidate)
    key_to_source_id[key] = candidate
    record = dict(source)
    record["id"] = candidate
    if not record.get("authors_or_organization"):
        record["authors_or_organization"] = record.get("authors") or record.get("organization") or record.get("journal") or "Autoría u organización indicada en la fuente"
    record["locator"] = record.get("locator") or record.get("doi") or record.get("url") or record.get("title")
    record["limitations"] = record.get("limitations") or "La fuente respalda conceptos dentro de su diseño, versión y contexto; no sustituye la validación del biosensor, población o uso concreto descrito en otra evidencia."
    record["used_by_unit_ids"] = sorted(source_units[key])
    canonical_sources.append(record)

source_by_id = {record["id"]: record for record in canonical_sources}
unit_source_ids: dict[int, list[str]] = {
    n: [key_to_source_id[key] for key in unit_source_keys[n]] for n in range(1, 7)
}
assert all(unit_source_ids[n] for n in range(1, 7))

dump(COURSE_DIR / "sources.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "source_policy": "Fuentes procedentes de las seis unidades curadas. Se conservan identificadores estables, estado de verificación y unidades de uso; la revisión disciplinaria humana del conjunto permanece pendiente.",
    "consulted_on": "2026-08-24",
    "coverage_gaps": [],
    "sources": canonical_sources,
})

# Aggregate glossary entries while preserving all unit associations and traceability.
glossary_by_term: dict[str, dict] = {}
for n, unit in enumerate(units, start=1):
    unit_id = f"{CODE}-U{n:02d}"
    candidates = unit_source_ids[n]
    for entry in unit.get("glossary", []):
        key = normalize(entry.get("term") or "")
        if not key:
            continue
        source_id = best_source_id((entry.get("term") or "") + " " + (entry.get("definition") or ""), candidates, source_by_id)
        if key not in glossary_by_term:
            glossary_by_term[key] = {
                "term": entry["term"],
                "definition": entry["definition"],
                "unit_ids": [],
                "source_ids": [],
                "verification_status": "verified_directly",
            }
        record = glossary_by_term[key]
        if unit_id not in record["unit_ids"]:
            record["unit_ids"].append(unit_id)
        if source_id not in record["source_ids"]:
            record["source_ids"].append(source_id)

glossary_entries = []
for index, record in enumerate(glossary_by_term.values(), start=1):
    glossary_entries.append({"id": f"{CODE}-GLO-{index:03d}", **record})

glossary_ids_by_unit: dict[int, list[str]] = defaultdict(list)
for entry in glossary_entries:
    for unit_id in entry["unit_ids"]:
        glossary_ids_by_unit[int(unit_id[-2:])].append(entry["id"])

dump(COURSE_DIR / "glossary.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "entries": glossary_entries,
})

# Create claims from literal key points, with a source selected by thematic overlap.
claims: list[dict] = []
claim_ids_by_unit: dict[int, list[str]] = defaultdict(list)
for n, unit in enumerate(units, start=1):
    unit_id = f"{CODE}-U{n:02d}"
    candidates = unit_source_ids[n]
    selected_points: list[str] = []
    for section in unit["theory_sections"]:
        for point in section.get("key_points", [])[:2]:
            if point not in selected_points:
                selected_points.append(point)
    assert len(selected_points) >= 8, (n, len(selected_points))
    for index, text in enumerate(selected_points[:8], start=1):
        source_id = best_source_id(text, candidates, source_by_id)
        source = source_by_id[source_id]
        claim_id = f"{unit_id}-C{index:03d}"
        claim = {
            "claim_id": claim_id,
            "unit": n,
            "text": text,
            "claim_type": "methodological_or_interpretive",
            "risk": "medium",
            "context": f"Síntesis educativa de {unit['title']}; debe interpretarse dentro del propósito, supuestos, controles y límites declarados en la unidad.",
            "source_id": source_id,
            "locator": {"section": str(source.get("locator") or source.get("title") or "Fuente completa")},
            "support": "direct_or_synthesis",
            "source_verification_status": source.get("verification_status") or "verified_directly",
            "review_state": "ai_review_provisional",
            "reviewer_validation_id": None,
            "reviewed_at": "2026-08-24",
            "id": claim_id,
            "unit_id": unit_id,
        }
        claims.append(claim)
        claim_ids_by_unit[n].append(claim_id)

dump(COURSE_DIR / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Afirmaciones centrales literales de las seis unidades de Biosensores con fuentes verificadas; revisión disciplinaria humana pendiente.",
    "review_state": "ai_review_provisional",
    "claims": claims,
})

# Planned media registry; multimedia remains deliberately outside strict content closure.
media_items = []
for n, unit in enumerate(units, start=1):
    unit_id = f"{CODE}-U{n:02d}"
    media_items.append({
        "id": f"{unit_id}-MED01",
        "type": "figure",
        "status": "planned",
        "unit_id": unit_id,
        "linked_learning_outcome_ids": [f"{unit_id}-LO01", f"{unit_id}-LO02"],
        "pedagogical_purpose": f"Representar visualmente los conceptos y la cadena de evidencia centrales de {unit['title']}.",
        "alt_text_draft": None,
        "license_requirements": "Usar material propio o con licencia compatible y registrar atribución, procedencia y versión.",
        "source_ids": [],
    })
dump(COURSE_DIR / "media.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "coverage_status": "planned",
    "items": media_items,
})

# Canonicalize units and their unit assessments.
for n, unit in enumerate(units, start=1):
    unit_id = f"{CODE}-U{n:02d}"
    local_los = [
        {"id": f"{unit_id}-LO{i:02d}", "statement": statement}
        for i, statement in enumerate(unit["learning_objectives"], start=1)
    ]
    topics = []
    for topic_index, section in enumerate(unit["theory_sections"], start=1):
        topic_id = f"{unit_id}-T{topic_index:02d}"
        equations = []
        for eq_index, equation in enumerate(section.get("equations", []), start=1):
            equations.append({
                "id": f"{topic_id}-B{eq_index:02d}",
                "type": "equation",
                "latex": equation["latex"],
                "label": equation.get("meaning") or "Relación cuantitativa utilizada en la unidad.",
                "variables": {str(k): str(v) for k, v in (equation.get("variables") or {}).items()},
            })
        key_points = list(section.get("key_points", []))
        subtopics = []
        for sub_index, paragraph in enumerate(section["paragraphs"], start=1):
            if sub_index <= len(key_points):
                sub_title = key_points[sub_index - 1].rstrip(".")
            else:
                sentence = re.split(r"(?<=[.!?])\s+", paragraph.strip(), maxsplit=1)[0]
                sub_title = sentence[:140].rstrip(".")
            subtopics.append({
                "id": f"{topic_id}-ST{sub_index:02d}",
                "title": sub_title,
                "blocks": [{
                    "id": f"{topic_id}-ST{sub_index:02d}-B01",
                    "type": "paragraph",
                    "text": paragraph,
                }],
            })
        topics.append({
            "id": topic_id,
            "title": section["heading"],
            "blocks": equations,
            "key_points": key_points,
            "subtopics": subtopics,
        })

    examples = []
    for index, example in enumerate(unit.get("worked_examples", []), start=1):
        examples.append({"id": f"{unit_id}-EX{index:02d}", **example})

    activities = []
    for index, activity in enumerate(unit.get("guided_activities", []), start=1):
        activities.append({
            "id": f"{unit_id}-ACT{index:02d}",
            "title": activity["title"],
            "purpose": f"Practicar de forma guiada y reproducible los resultados de {unit['title']} con datos o escenarios sintéticos y una conclusión proporcional al alcance de la evidencia.",
            "prerequisite_unit_ids": [] if n == 1 else [f"{CODE}-U{n-1:02d}"],
            "instructions": activity["instructions"],
            "tasks": activity["problems"],
            "deliverables": activity["deliverables"],
            "checking_criteria": activity["checking_criteria"],
            "estimated_duration_minutes": 120 if n >= 5 else 90,
            "status": "curated_internal_review_pending",
        })

    biomedical_connections = []
    for connection in unit.get("biomedical_connections", []):
        if isinstance(connection, dict):
            biomedical_connections.append(f"{connection.get('topic', 'Conexión biomédica')}: {connection.get('connection', '')}".strip())
        else:
            biomedical_connections.append(str(connection))

    canonical_unit = {
        "$schema": "../../../../schemas/academic/unit-v1.schema.json",
        "schema_version": "1.0",
        "id": unit_id,
        "course_id": COURSE_ID,
        "order": n,
        "slug": unit["slug"],
        "title": unit["title"],
        "status": STATUS,
        "purpose": unit["purpose"],
        "prerequisite_unit_ids": [] if n == 1 else [f"{CODE}-U{n-1:02d}"],
        "course_learning_outcome_ids": UNIT_TO_COURSE_LOS[n],
        "learning_outcomes": local_los,
        "topics": topics,
        "examples": examples,
        "activities": activities,
        "assessment_file": f"assessments/unit-{n:02d}.json",
        "glossary_entry_ids": glossary_ids_by_unit[n],
        "source_ids": unit_source_ids[n],
        "claim_ids": claim_ids_by_unit[n],
        "media_ids": [f"{unit_id}-MED01"],
        "common_errors": unit.get("common_errors", []),
        "biomedical_connections": biomedical_connections,
        "editorial_notice": unit.get("editorial_notice", "Material educativo con revisión humana pendiente."),
        "legacy_origin": f"data/course_redevelopment/biosensores/units/unit-{n:02d}.json",
    }
    dump(COURSE_DIR / "units" / f"unit-{n:02d}.json", canonical_unit)

    self_assessment = unit.get("self_assessment", [])
    assert len(self_assessment) == 10, (n, len(self_assessment))
    items = []
    for index, question in enumerate(self_assessment, start=1):
        if index <= 2:
            difficulty, cognitive = "foundational", "understand"
        elif index <= 5:
            difficulty, cognitive = "intermediate", "apply"
        elif index <= 8:
            difficulty, cognitive = "intermediate", "analyze"
        else:
            difficulty, cognitive = "advanced", "evaluate"
        linked_lo = local_los[(index - 1) % len(local_los)]["id"]
        source_id = best_source_id(question.get("question", "") + " " + question.get("answer", ""), unit_source_ids[n], source_by_id)
        misconception = str(question.get("common_error") or "Confundir una definición o resultado local con una conclusión más amplia que la evidencia disponible.")
        reasoning = str(question.get("reasoning") or "La respuesta requiere conservar la definición, condiciones y límites trabajados en la unidad.")
        items.append({
            "id": f"{unit_id}-Q{index:02d}",
            "type": "short_answer",
            "prompt": question["question"],
            "linked_learning_outcome_ids": [linked_lo],
            "difficulty": difficulty,
            "cognitive_level": cognitive,
            "answer_key": {
                "expected_answer": question["answer"],
                "explanation": reasoning,
                "common_misconceptions": [misconception],
            },
            "feedback": {
                "correct": f"Correcto. Conserva este criterio en tu justificación: {reasoning}",
                "incorrect": f"Revisa el razonamiento y evita este error frecuente: {misconception}",
            },
            "source_ids": [source_id],
            "status": "curated_internal_review_pending",
        })
    dump(COURSE_DIR / "assessments" / f"unit-{n:02d}.json", {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{unit_id}-EVAL",
        "course_id": COURSE_ID,
        "scope": "unit",
        "unit_id": unit_id,
        "purpose": "Autoevaluación formativa de los resultados de aprendizaje de la unidad con retroalimentación y fuentes trazables.",
        "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
        "items": items,
        "status": "curated_internal_review_pending",
    })

# Course-level assessment integrates all six units and the seven course outcomes.
course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "BIOSEN-EVAL-CURSO",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": [
        "La evidencia de dominio es un expediente verificable que conecta mensurando, reconocimiento, transducción, interfaz, calibración, desempeño y uso previsto.",
        "Una cifra correcta sin unidades, procedimiento, controles, incertidumbre y límites recibe crédito parcial.",
        "Las actividades autónomas usan datos o escenarios sintéticos; no recogen muestras ni datos de pacientes ni sustentan decisiones de salud.",
        "La evaluación separa desempeño técnico, analítico, clínico, utilidad y afirmaciones regulatorias.",
        "Los criterios de aceptación se definen antes de inspeccionar resultados y las desviaciones se conservan como evidencia.",
        "La revisión humana interna y externa permanece pendiente y no se sustituye por controles automáticos del repositorio.",
    ],
    "assessment_plan": [
        {"component": "Recuperación y explicación", "weight_percent": 15, "description": "Preguntas conceptuales y mapas de cadena de medida con corrección razonada."},
        {"component": "Problemas y casos", "weight_percent": 20, "description": "Cálculos y decisiones de diseño con unidades, supuestos, controles y límites."},
        {"component": "Expedientes reproducibles", "weight_percent": 25, "description": "Actividades sintéticas con trazabilidad de datos, parámetros, calibración, procesamiento y evidencia."},
        {"component": "Revisión por pares", "weight_percent": 10, "description": "Aplicación de rúbrica, clasificación de hallazgos y corrección antes-después."},
        {"component": "Proyecto integrador", "weight_percent": 30, "description": "Expediente completo de un biosensor sintético que conecta U1–U6 sin sobreafirmar uso clínico o regulatorio."},
    ],
    "diagnostic": {
        "title": "Diagnóstico de entrada a Biosensores",
        "purpose": "Identificar prerrequisitos de química, biología, instrumentación, cálculo, estadística y razonamiento de evidencia; no cuenta como calificación final.",
        "questions": [
            "Distingue mensurando, analito, señal y resultado reportado en un ejemplo sencillo.",
            "Explica qué función cumple un bioreceptor y qué no demuestra por sí solo.",
            "Distingue precisión, sesgo y sensibilidad de una cadena de medición.",
            "Interpreta una curva de calibración con unidades y un caso fuera del intervalo demostrado.",
            "Explica por qué un control negativo y un blanco responden a preguntas diferentes.",
            "Distingue transporte convectivo y difusivo en un microcanal.",
            "Explica la diferencia entre sensibilidad analítica y sensibilidad diagnóstica.",
            "Indica por qué PPV depende de prevalencia o probabilidad preprueba.",
            "Propón un riesgo de error de uso en un dispositivo point-of-care y un control plausible.",
            "Describe cómo registrarías versión de firmware, algoritmo y parámetros para reproducir una métrica wearable.",
            "Reescribe una afirmación de 'biosensor clínicamente validado' para ajustarla a evidencia únicamente analítica.",
            "Explica por qué consultar una norma o guía no equivale a demostrar conformidad regulatoria.",
        ],
        "interpretation": [
            "0-4 respuestas sólidas: realizar nivelación antes de iniciar los retos cuantitativos.",
            "5-8 respuestas sólidas: iniciar el curso y reforzar los dominios fallidos con práctica guiada.",
            "9-12 respuestas sólidas: comenzar con problemas de transferencia y documentar explícitamente límites y supuestos.",
        ],
    },
    "midterm_blueprint": [
        {"domain": "U1 Arquitectura", "weight_percent": 15, "learning_outcome_ids": ["BIOSEN-LO01"], "evidence": "Mensurando, bioreceptor, transductor, señal, sensibilidad y presupuesto de cadena."},
        {"domain": "U2 Reconocimiento biológico", "weight_percent": 15, "learning_outcome_ids": ["BIOSEN-LO02"], "evidence": "Afinidad, cinética, catálisis, anticuerpos, sondas y aptámeros."},
        {"domain": "U3 Transducción", "weight_percent": 15, "learning_outcome_ids": ["BIOSEN-LO03"], "evidence": "Modalidades electroquímica, óptica, acústica/piezoeléctrica y térmica."},
        {"domain": "U4 Inmovilización y microfluídica", "weight_percent": 15, "learning_outcome_ids": ["BIOSEN-LO04"], "evidence": "Superficies, orientación, antifouling, transporte y manejo de muestra."},
        {"domain": "U5 Desempeño analítico", "weight_percent": 20, "learning_outcome_ids": ["BIOSEN-LO05"], "evidence": "Calibración, precisión, sesgo, LoB/LoD/LoQ, interferencias y comparación de métodos."},
        {"domain": "U6 Uso clínico y portátil", "weight_percent": 20, "learning_outcome_ids": ["BIOSEN-LO06", "BIOSEN-LO07"], "evidence": "Uso previsto, métricas diagnósticas, prevalencia, robustez, factores humanos, datos y límites regulatorios."},
    ],
    "capstone": {
        "title": "Expediente integrador de evidencia para un biosensor sintético",
        "scenario": "Un equipo académico recibe una necesidad biomédica ficticia y datos sintéticos de un prototipo. Debe definir el mensurando, seleccionar reconocimiento y transducción, diseñar interfaz y manejo de muestra, caracterizar desempeño analítico y proponer la evidencia necesaria para un uso point-of-care o wearable, sin afirmar validación clínica, utilidad ni conformidad no demostradas.",
        "phases": [
            "Definir necesidad, uso previsto, mensurando, población o muestra y criterios de aceptación.",
            "Construir la arquitectura y justificar reconocimiento, transducción, inmovilización y transporte.",
            "Ejecutar con datos sintéticos la caracterización analítica y los controles previstos.",
            "Evaluar escenarios de robustez, factores humanos, datos faltantes y desempeño clínico simulado cuando corresponda.",
            "Realizar revisión independiente, corregir el expediente y registrar cambios.",
            "Defender qué se ha demostrado, qué no se ha evaluado y cuál sería la siguiente evidencia necesaria.",
        ],
        "deliverables": [
            "Especificación de uso previsto, mensurando y arquitectura del biosensor.",
            "Matriz de selección de bioreceptor, transductor, superficie y manejo de muestra.",
            "Expediente analítico con calibración, precisión, sesgo, límites e interferencias aplicables.",
            "Matriz de evidencia técnica-analítica-clínica-utilidad-regulación y riesgos.",
            "Datos, parámetros, versiones, procedimiento reproducible y registro de cambios.",
            "Informe académico y resumen divulgativo coherentes y acotados.",
        ],
        "integration_requirements": [
            "Usar explícitamente procedimientos o evidencia de las seis unidades y mapearlos a BIOSEN-LO01–BIOSEN-LO07.",
            "Incluir al menos un control de reconocimiento o matriz, un caso límite de transducción, un análisis de sensibilidad y una explicación alternativa.",
            "Separar señal medida, cantidad estimada, desempeño analítico, desempeño clínico simulado, utilidad no demostrada y estado regulatorio.",
            "Registrar unidades, materiales o premisas, parámetros, versiones, exclusiones y discrepancias.",
            "Cerrar con una conclusión proporcional y una lista priorizada de estudios o evidencia que faltaría para un uso real.",
        ],
        "rubric": [
            {"criterion": "Arquitectura, mensurando y reconocimiento", "weight_percent": 20, "excellent": "La cadena se define con entidades, unidades, interfaces, supuestos y selección de bioreceptor justificables."},
            {"criterion": "Transducción, superficie y transporte", "weight_percent": 15, "excellent": "La conversión física y el manejo de muestra están conectados con controles, límites y parámetros reproducibles."},
            {"criterion": "Desempeño analítico", "weight_percent": 20, "excellent": "Calibración, precisión, sesgo, capacidad de detección, interferencias e intervalo se interpretan con criterios previos."},
            {"criterion": "Uso previsto, desempeño clínico y factores humanos", "weight_percent": 15, "excellent": "El contexto de uso, métricas diagnósticas y riesgos operativos se evalúan sin extrapolar utilidad o beneficio."},
            {"criterion": "Reproducibilidad, trazabilidad e incertidumbre", "weight_percent": 15, "excellent": "Otra persona puede reconstruir datos, versiones, cálculos, decisiones, sensibilidad y discrepancias."},
            {"criterion": "Comunicación, límites y revisión", "weight_percent": 15, "excellent": "La conclusión distingue evidencia de afirmación, incorpora revisión y evita aprobación o conformidad no demostradas."},
        ],
    },
    "status": "curated_internal_review_pending",
}
dump(COURSE_DIR / "assessments" / "course-assessment.json", course_assessment)

# Course descriptor uses curated unit content, not the old generic redevelopment summary.
core_source_ids = []
for n in range(1, 7):
    for source_id in unit_source_ids[n][:2]:
        if source_id not in core_source_ids:
            core_source_ids.append(source_id)

course = {
    "$schema": "../../../schemas/academic/course-v1.schema.json",
    "schema_version": "1.0",
    "id": COURSE_ID,
    "code": CODE,
    "area_id": "ingenieria-biomedica",
    "title": "Biosensores",
    "language": "es",
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica y áreas afines con bases universitarias de química, biología, física, instrumentación, cálculo y estadística que necesiten diseñar, analizar y comunicar biosensores con trazabilidad y límites de uso explícitos.",
    "status": STATUS,
    "purpose": "Integrar mensurando, reconocimiento biológico, transducción, inmovilización y transporte de muestra, desempeño analítico y transición a usos point-of-care o wearables para construir expedientes reproducibles de biosensores con controles, incertidumbre, factores humanos y trazabilidad, separando con rigor desempeño técnico, analítico, clínico, utilidad y afirmaciones regulatorias.",
    "scope": {
        "included": [
            "Arquitectura de biosensores con mensurando, analito, bioreceptor, transductor, acondicionamiento y señal.",
            "Reconocimiento biológico mediante afinidad, cinética, catálisis, anticuerpos, ácidos nucleicos y aptámeros.",
            "Transducción electroquímica, óptica, piezoeléctrica/acústica y térmica con calibración, ruido e interferencias.",
            "Inmovilización, orientación, densidad superficial, pasivación, biofouling, transporte de masa y microfluídica.",
            "Desempeño analítico con calibración, precisión, sesgo, intervalo, LoB/LoD/LoQ, selectividad, interferencias y comparación de métodos.",
            "Uso previsto, point-of-care, wearables, desempeño clínico, prevalencia, valores predictivos, robustez, completitud, factores humanos, integridad de datos y ciclo de vida.",
            "Expedientes reproducibles que relacionan pregunta, evidencia, método, control, resultado, incertidumbre, riesgo y límite.",
        ],
        "excluded": [
            "Diagnóstico, tratamiento o decisiones de salud para una persona a partir de actividades o datos del curso.",
            "Recogida de muestras humanas, datos de pacientes o pruebas con participantes fuera de infraestructura, supervisión, consentimiento y autorizaciones apropiadas.",
            "Afirmar utilidad clínica, seguridad, eficacia, aprobación, certificación o conformidad regulatoria de un prototipo a partir de ejercicios educativos.",
            "Usar sensibilidad analítica, LoD, correlación o una métrica técnica aislada como sustituto de desempeño diagnóstico o beneficio clínico.",
            "Ejecutar procedimientos de laboratorio húmedo o ensayos con dispositivos reales sin la formación y controles de seguridad correspondientes.",
        ],
        "handoff_courses": [
            "bioinstrumentacion",
            "laboratorio-bioinstrumentacion",
            "biomateriales",
            "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas",
            "aplicaciones-salud-digital",
        ],
    },
    "prerequisites": [
        {"id": "BIOSEN-PRE01", "statement": "Química general y bioquímica introductoria, incluidas concentraciones, equilibrio y biomoléculas."},
        {"id": "BIOSEN-PRE02", "statement": "Biología celular y molecular introductoria para comprender interacciones de reconocimiento."},
        {"id": "BIOSEN-PRE03", "statement": "Física, circuitos e instrumentación básica con unidades, ruido, muestreo y adquisición."},
        {"id": "BIOSEN-PRE04", "statement": "Cálculo, álgebra y estadística descriptiva para interpretar calibración, variabilidad y probabilidad."},
        {"id": "BIOSEN-PRE05", "statement": "Capacidad para documentar datos, parámetros, versiones, controles y resultados reproducibles."},
    ],
    "competencies": [
        {"id": "BIOSEN-COMP01", "statement": "Especificar una cadena de biosensor desde el mensurando hasta el resultado reportado con interfaces y unidades explícitas."},
        {"id": "BIOSEN-COMP02", "statement": "Seleccionar reconocimiento y transducción en función de mecanismo, rango, selectividad, interferencias y uso previsto."},
        {"id": "BIOSEN-COMP03", "statement": "Diseñar superficies y transporte de muestra que conserven acceso al bioreceptor y controlen limitaciones de masa y biofouling."},
        {"id": "BIOSEN-COMP04", "statement": "Caracterizar desempeño analítico con diseños, criterios, controles y comparación apropiados."},
        {"id": "BIOSEN-COMP05", "statement": "Evaluar portabilidad, point-of-care y wearables incorporando contexto, factores humanos, datos faltantes, versiones y riesgos."},
        {"id": "BIOSEN-COMP06", "statement": "Separar niveles de evidencia y comunicar conclusiones sin convertir desempeño técnico en validación clínica o conformidad regulatoria."},
        {"id": "BIOSEN-COMP07", "statement": "Integrar las seis unidades en un expediente reproducible susceptible de revisión, corrección y transferencia responsable."},
    ],
    "learning_outcomes": [{"id": identifier, "statement": statement} for identifier, statement in COURSE_LOS],
    "study_method": [
        "Definir primero mensurando, matriz o señal, uso previsto, usuario, entorno y criterio de aceptación.",
        "Alternar explicación, ejemplo resuelto, práctica guiada, comprobación y transferencia con apoyo progresivamente menor.",
        "Separar observación, transformación, cantidad estimada, modelo, interpretación y decisión.",
        "Predefinir blancos, controles, interferentes, perturbaciones y criterios antes de inspeccionar resultados.",
        "Conservar unidades, lotes o premisas, parámetros, versiones, reglas de exclusión y discrepancias.",
        "Revisar cada producto con rúbrica y justificar las correcciones antes de cerrar una conclusión.",
    ],
    "core_source_ids": core_source_ids,
    "unit_files": [f"units/unit-{n:02d}.json" for n in range(1, 7)],
    "assessment_files": [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"],
    "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
    "static_site": {
        "renderer": "scripts/generate_site.py",
        "canonical_source": True,
        "legacy_mirrors": [
            "data/generated_courses/biosensores.json",
            "data/generated_units/biosensores/",
            "data/subjects/ingenieria-biomedica/biosensores.json",
            "data/source_registry/biosensores.json",
            "data/claim_registry/biosensores.json",
        ],
    },
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para las seis unidades. Las fuentes quedan trazadas y la publicación sigue siendo provisional. La revisión humana interna y la revisión disciplinaria externa permanecen pendientes. Las actividades usan datos o escenarios sintéticos y no constituyen validación analítica o clínica de un producto real, consejo diagnóstico o terapéutico, estudio con participantes, evaluación de conformidad, certificación ni autorización de comercialización.",
}
dump(COURSE_DIR / "course.json", course)

# Permanent regression for the canonical closure.
test_path = ROOT / "tests" / "test_biosensores_canonical_course.py"
test_path.write_text('''from __future__ import annotations\n\nimport json\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nCOURSE = ROOT / "data" / "courses" / "biosensores"\nGENERIC = "concepto de la unidad que debe definirse"\n\n\nclass BiosensoresCanonicalCourseTests(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))\n        cls.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))\n        cls.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))\n        cls.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))\n\n    def test_course_status_preserves_human_review_boundary(self):\n        status = self.course["status"]\n        self.assertEqual(status["content"], "complete")\n        self.assertEqual(status["sources"], "traceable")\n        self.assertEqual(status["pedagogy"], "complete")\n        self.assertEqual(status["multimedia"], "planned")\n        self.assertEqual(status["internal_review"], "pending")\n        self.assertEqual(status["external_review"], "pending")\n\n    def test_six_units_cover_all_course_outcomes_without_generic_text(self):\n        self.assertEqual(len(self.course["unit_files"]), 6)\n        known = {item["id"] for item in self.course["learning_outcomes"]}\n        covered = set()\n        for relative in self.course["unit_files"]:\n            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))\n            covered.update(unit["course_learning_outcome_ids"])\n            self.assertNotIn(GENERIC, json.dumps(unit, ensure_ascii=False).casefold())\n            self.assertGreaterEqual(len(unit["topics"]), 4)\n            self.assertTrue(unit["activities"][0]["estimated_duration_minutes"] > 0)\n        self.assertEqual(known, covered)\n\n    def test_assessments_have_ten_classified_items_with_feedback(self):\n        source_ids = {item["id"] for item in self.sources["sources"]}\n        for n in range(1, 7):\n            assessment = json.loads((COURSE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))\n            self.assertEqual(len(assessment["items"]), 10)\n            for item in assessment["items"]:\n                self.assertNotEqual(item["difficulty"], "unclassified")\n                self.assertNotEqual(item["cognitive_level"], "unclassified")\n                self.assertTrue(item["feedback"]["correct"])\n                self.assertTrue(item["feedback"]["incorrect"])\n                self.assertTrue(item["source_ids"])\n                self.assertTrue(set(item["source_ids"]) <= source_ids)\n\n    def test_glossary_sources_and_claims_are_traceable(self):\n        source_ids = {item["id"] for item in self.sources["sources"]}\n        self.assertGreaterEqual(len(self.glossary["entries"]), 80)\n        for entry in self.glossary["entries"]:\n            self.assertTrue(entry["source_ids"])\n            self.assertTrue(set(entry["source_ids"]) <= source_ids)\n            self.assertNotEqual(entry["verification_status"], "unverified")\n        self.assertEqual(len(self.claims["claims"]), 48)\n        self.assertEqual({claim["unit_id"] for claim in self.claims["claims"]}, {f"BIOSEN-U{i:02d}" for i in range(1, 7)})\n\n    def test_course_assessment_integrates_all_units(self):\n        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)\n        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 10)\n        mapped = {lo for row in assessment["midterm_blueprint"] for lo in row["learning_outcome_ids"]}\n        self.assertEqual(mapped, {item["id"] for item in self.course["learning_outcomes"]})\n\n    def test_unit_five_and_six_keep_analytical_clinical_boundary(self):\n        u5 = json.loads((COURSE / "units" / "unit-05.json").read_text(encoding="utf-8"))\n        u6 = json.loads((COURSE / "units" / "unit-06.json").read_text(encoding="utf-8"))\n        self.assertIn("sensibilidad analítica", json.dumps(u5, ensure_ascii=False).casefold())\n        self.assertIn("sensibilidad diagnóstica", json.dumps(u6, ensure_ascii=False).casefold())\n        self.assertIn("conformidad regulatoria", json.dumps(u6, ensure_ascii=False).casefold())\n        self.assertIn("sin confundir", u5["purpose"].casefold())\n\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")

print(f"Canonical Biosensores built: {len(canonical_sources)} sources, {len(glossary_entries)} glossary entries, {len(claims)} claims")
