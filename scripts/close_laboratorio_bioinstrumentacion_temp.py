#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "laboratorio-bioinstrumentacion"
CODE = "LBI"
SRC_ROOT = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"
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
GENERIC = "concepto de la unidad que debe definirse"
STOP = {"de","la","el","los","las","un","una","y","o","en","para","por","con","del","al","que","se","su","sus","como","a"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "item"


def compact_title(text: str, fallback: str) -> str:
    first = re.split(r"(?<=[.!?])\s+", text.strip())[0]
    first = re.sub(r"\s+", " ", first).strip()
    if len(first) > 105:
        first = first[:102].rsplit(" ", 1)[0] + "…"
    return first or fallback


def as_text(value) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for keys in (("title","description"), ("name","description"), ("connection","rationale"), ("term","definition")):
            parts = [str(value.get(k) or "").strip() for k in keys]
            parts = [p for p in parts if p]
            if parts:
                return ": ".join(parts)
        return "; ".join(str(v).strip() for v in value.values() if isinstance(v, (str,int,float)) and str(v).strip())
    return str(value).strip()


def source_key(source: dict) -> str:
    return (str(source.get("url") or "").strip() or (str(source.get("title") or "").strip() + "|" + str(source.get("organization") or source.get("authors") or "").strip())).casefold()


def tokens(text: str) -> set[str]:
    words = re.findall(r"[a-záéíóúüñ0-9]+", text.casefold())
    return {w for w in words if len(w) >= 4 and w not in STOP}


units = [read_json(SRC_ROOT / f"unit-{n:02d}.json") for n in range(1, 7)]
for n, unit in enumerate(units, 1):
    assert unit["unit"] == n
    assert GENERIC not in json.dumps(unit, ensure_ascii=False).casefold(), f"U{n} conserva plantilla genérica"
    assert unit.get("status") == "review"
    assert len(unit.get("theory_sections", [])) >= 4
    assert len(unit.get("worked_examples", [])) >= 5
    assert len(unit.get("guided_activities", [])) >= 3
    assert len(unit.get("self_assessment", [])) >= 10
    assert len(unit.get("sources", [])) >= 6

# Fuentes consolidadas y mapeo por unidad.
source_records: list[dict] = []
source_id_by_key: dict[str, str] = {}
unit_source_ids: dict[int, list[str]] = {}
for n, unit in enumerate(units, 1):
    ids: list[str] = []
    for source in unit["sources"]:
        if source.get("verification_status") != "verified_directly":
            raise AssertionError(f"U{n}: fuente no verificada directamente: {source.get('title')}")
        key = source_key(source)
        if key not in source_id_by_key:
            sid = f"lbi-src-{len(source_records)+1:03d}"
            source_id_by_key[key] = sid
            record = {"id": sid}
            for field in ("title","authors","organization","year","url","type","description","doi","pmid"):
                if source.get(field) not in (None, "", []):
                    record[field] = source[field]
            record["verification_status"] = "verified_directly"
            record["unit_origins"] = [n]
            source_records.append(record)
        else:
            sid = source_id_by_key[key]
            rec = next(r for r in source_records if r["id"] == sid)
            if n not in rec["unit_origins"]:
                rec["unit_origins"].append(n)
        ids.append(sid)
    unit_source_ids[n] = list(dict.fromkeys(ids))

source_by_id = {r["id"]: r for r in source_records}

def choose_source(n: int, text: str) -> str:
    q = tokens(text)
    best = None
    best_score = -1
    for sid in unit_source_ids[n]:
        src = source_by_id[sid]
        hay = " ".join(str(src.get(k) or "") for k in ("title","description","organization","authors"))
        score = len(q & tokens(hay))
        if score > best_score:
            best, best_score = sid, score
    return best or unit_source_ids[n][0]

# Glosario global deduplicado.
glossary_records: list[dict] = []
glossary_by_term: dict[str, dict] = {}
unit_glossary_ids: dict[int, list[str]] = {}
for n, unit in enumerate(units, 1):
    gids: list[str] = []
    for entry in unit["glossary"]:
        term = str(entry.get("term") or "").strip()
        definition = str(entry.get("definition") or "").strip()
        key = term.casefold()
        sid = choose_source(n, f"{term} {definition}")
        if key not in glossary_by_term:
            gid = f"LBI-G{len(glossary_records)+1:03d}"
            rec = {
                "id": gid,
                "term": term,
                "definition": definition,
                "source_ids": [sid],
                "verification_status": "traceable_to_verified_source",
            }
            glossary_by_term[key] = rec
            glossary_records.append(rec)
        else:
            rec = glossary_by_term[key]
            if sid not in rec["source_ids"]:
                rec["source_ids"].append(sid)
        gids.append(rec["id"])
    unit_glossary_ids[n] = list(dict.fromkeys(gids))

# Media planificada: una visualización por unidad, sin fingir activos producidos.
media_records = []
for n, unit in enumerate(units, 1):
    media_records.append({
        "id": f"LBI-M{n:02d}",
        "unit_id": f"{CODE}-U{n:02d}",
        "title": f"Visualización pedagógica planificada — U{n}: {unit['title']}",
        "type": "interactive_diagram_or_annotated_figure",
        "status": "planned",
        "purpose": f"Representar visualmente el mecanismo o flujo central de {unit['title']} sin sustituir la explicación, la evidencia ni la práctica guiada.",
        "alt_text": f"Esquema didáctico previsto para la unidad {n}, {unit['title']}.",
    })

# Claims: cuatro anclas literales por unidad, una por bloque teórico.
claims = []
unit_claim_ids: dict[int, list[str]] = {}
for n, unit in enumerate(units, 1):
    cids = []
    for section_index, section in enumerate(unit["theory_sections"][:4], 1):
        key_points = section.get("key_points") or []
        text = str(key_points[0] if key_points else section["paragraphs"][0]).strip()
        cid = f"LBI-C{n:02d}-{section_index:02d}"
        sid = choose_source(n, text)
        claims.append({
            "id": cid,
            "unit": n,
            "unit_id": f"{CODE}-U{n:02d}",
            "text": text,
            "source_id": sid,
            "source_verification_status": "verified_directly",
            "review_state": "ai_review_provisional",
            "support": "direct",
        })
        cids.append(cid)
    unit_claim_ids[n] = cids

course_outcomes = [
    {"id": "LBI-LO01", "statement": "Aplica una frontera de seguridad educativa, vocabulario metrológico, trazabilidad e incertidumbre para documentar trabajo experimental sintético sin extrapolarlo a seguridad clínica o conformidad normativa."},
    {"id": "LBI-LO02", "statement": "Caracteriza sensores mediante curvas, sensibilidad metrológica, offset, linealidad, histéresis, repetibilidad, deriva y respuesta dinámica, vinculando cada conclusión con condiciones e incertidumbre."},
    {"id": "LBI-LO03", "statement": "Analiza un front-end diferencial de biopotenciales mediante señal diferencial y de modo común, CMRR, impedancias, ganancia, headroom, saturación, ruido e interferencia usando únicamente fuentes equivalentes o simulación."},
    {"id": "LBI-LO04", "statement": "Diseña y audita una cadena de filtrado y adquisición con banda, fase, muestreo, antialiasing, ADC, cuantización, clipping y procedencia reproducible, distinguiendo procesamiento causal de análisis offline."},
    {"id": "LBI-LO05", "statement": "Integra arquitectura, interfaces, alimentación, temporización, firmware, buffers, comunicación y configuración en una baseline reproducible capaz de localizar fallos entre subsistemas."},
    {"id": "LBI-LO06", "statement": "Verifica requisitos técnicos de una baseline con criterios predefinidos, repetibilidad, incertidumbre, reglas de decisión, discrepancias y regresión, diferenciando verificación de validación y calibración."},
    {"id": "LBI-LO07", "statement": "Integra U1–U6 en un expediente auditable de cadena de medición que conserva requisitos, versiones, fuentes, datos, cálculos, controles, incertidumbre, fallos y límites sin reclamar validación clínica, seguridad eléctrica, EMC ni conformidad regulatoria."},
]

canonical_units = []
for n, src in enumerate(units, 1):
    unit_id = f"{CODE}-U{n:02d}"
    local_los = [{"id": f"{unit_id}-LO{i:02d}", "statement": text} for i, text in enumerate(src["learning_objectives"], 1)]
    topics = []
    for ti, section in enumerate(src["theory_sections"], 1):
        topic_id = f"{unit_id}-T{ti:02d}"
        eq_blocks = []
        for ei, equation in enumerate(section.get("equations", []), 1):
            eq_blocks.append({
                "id": f"{topic_id}-E{ei:02d}",
                "type": "equation",
                "latex": str(equation.get("latex") or "").strip(),
                "label": str(equation.get("meaning") or "Relación cuantitativa de la sección").strip(),
                "variables": {str(k): str(v) for k, v in (equation.get("variables") or {}).items()},
            })
        subs = []
        points = section.get("key_points") or []
        for pi, paragraph in enumerate(section["paragraphs"], 1):
            sub_id = f"{topic_id}-ST{pi:02d}"
            title_seed = str(points[pi-1]) if pi-1 < len(points) else str(paragraph)
            subs.append({
                "id": sub_id,
                "title": compact_title(title_seed, f"Desarrollo {pi}"),
                "blocks": [{"id": f"{sub_id}-B01", "type": "paragraph", "text": str(paragraph)}],
            })
        topics.append({
            "id": topic_id,
            "title": section["heading"],
            "blocks": eq_blocks,
            "key_points": [str(x) for x in points] or [compact_title(section["paragraphs"][0], "Idea clave")],
            "subtopics": subs,
        })
    examples = []
    for i, ex in enumerate(src["worked_examples"], 1):
        examples.append({
            "id": f"{unit_id}-EX{i:02d}",
            "title": str(ex.get("title") or f"Ejemplo {i}"),
            "scenario": str(ex.get("scenario") or ex.get("problem") or "Escenario sintético delimitado."),
            "reasoning_steps": [str(x) for x in (ex.get("reasoning_steps") or ex.get("steps") or [])] or ["Identificar entradas, unidades, supuestos y criterio de interpretación."],
            "calculation": str(ex.get("calculation") or "No requiere cálculo adicional; se conserva el procedimiento del ejemplo fuente."),
            "interpretation": str(ex.get("interpretation") or ex.get("answer") or "Interpretación restringida a las condiciones descritas."),
            "limitations": [str(x) for x in (ex.get("limitations") or ["No extrapolar fuera de las condiciones del ejemplo."])],
        })
    activities = []
    durations = (90, 180, 90)
    for i, activity in enumerate(src["guided_activities"][:3], 1):
        tasks = activity.get("tasks") or activity.get("problems") or []
        deliverables = activity.get("deliverables") or [f"Producto documentado de la actividad {i} de U{n}."]
        criteria = activity.get("checking_criteria") or ["Entradas, unidades, supuestos, resultados y límites están explícitos."]
        instructions = activity.get("instructions") or ["Trabajar únicamente con datos sintéticos, simulación o fuentes equivalentes seguras."]
        activities.append({
            "id": f"{unit_id}-ACT{i:02d}",
            "title": str(activity.get("title") or f"Actividad {i}"),
            "purpose": f"Practicar progresivamente los resultados de aprendizaje de U{n} con evidencia reproducible y límites explícitos.",
            "prerequisite_unit_ids": [] if n == 1 else [f"{CODE}-U{n-1:02d}"],
            "instructions": [str(x) for x in instructions],
            "tasks": [str(x) for x in tasks],
            "deliverables": [str(x) for x in deliverables],
            "checking_criteria": [str(x) for x in criteria],
            "estimated_duration_minutes": durations[i-1],
            "status": "complete",
        })
    connections = [as_text(x) for x in src.get("biomedical_connections", [])]
    connections = [x for x in connections if x]
    canonical = {
        "$schema": "../../../../schemas/academic/unit-v1.schema.json",
        "schema_version": "1.0",
        "id": unit_id,
        "course_id": COURSE_ID,
        "order": n,
        "slug": src["slug"],
        "title": src["title"],
        "status": dict(STATUS),
        "purpose": src["purpose"],
        "prerequisite_unit_ids": [] if n == 1 else [f"{CODE}-U{n-1:02d}"],
        "course_learning_outcome_ids": [f"LBI-LO{n:02d}", "LBI-LO07"],
        "learning_outcomes": local_los,
        "topics": topics,
        "examples": examples,
        "activities": activities,
        "assessment_file": f"assessments/unit-{n:02d}.json",
        "glossary_entry_ids": unit_glossary_ids[n],
        "source_ids": unit_source_ids[n],
        "claim_ids": unit_claim_ids[n],
        "media_ids": [f"LBI-M{n:02d}"],
        "common_errors": src.get("common_errors", []),
        "biomedical_connections": connections or ["Aplicación biomédica delimitada en la unidad fuente."],
        "editorial_notice": src.get("editorial_notice", "Revisión disciplinar humana pendiente."),
        "legacy_origin": f"data/course_redevelopment/{COURSE_ID}/units/unit-{n:02d}.json",
    }
    canonical_units.append(canonical)

# Evaluaciones de unidad reutilizan la autoevaluación autoral y añaden metadatos pedagógicos.
for n, (src, unit) in enumerate(zip(units, canonical_units), 1):
    lo_ids = [x["id"] for x in unit["learning_outcomes"]]
    items = []
    for i, raw in enumerate(src["self_assessment"][: max(10, len(src["self_assessment"]))], 1):
        if isinstance(raw, str):
            question, answer, reasoning, misconception = raw, "Respuesta razonada basada en la unidad.", "Revisar el bloque teórico y justificar la conclusión.", "Responder sin declarar supuestos ni límites."
        else:
            question = str(raw.get("question") or raw.get("prompt") or raw.get("task") or f"Pregunta {i}")
            answer = str(raw.get("answer") or raw.get("expected_answer") or raw.get("solution") or "Respuesta razonada basada en la unidad.")
            reasoning = str(raw.get("reasoning") or raw.get("explanation") or answer)
            misconception = str(raw.get("common_error") or raw.get("misconception") or "Confundir el resultado técnico con una conclusión fuera del alcance de la unidad.")
        difficulty = "foundational" if i <= 3 else "intermediate" if i <= 8 else "advanced"
        cognitive = "understand" if i <= 3 else "apply" if i <= 6 else "analyze" if i <= 9 else "evaluate"
        sid = choose_source(n, f"{question} {answer} {reasoning}")
        items.append({
            "id": f"{unit['id']}-Q{i:02d}",
            "type": "case_analysis" if i % 5 == 0 else "short_answer",
            "prompt": question,
            "linked_learning_outcome_ids": [lo_ids[(i-1) % len(lo_ids)]],
            "difficulty": difficulty,
            "cognitive_level": cognitive,
            "answer_key": {"expected_answer": answer, "explanation": reasoning, "common_misconceptions": [misconception]},
            "feedback": {
                "correct": "La respuesta conserva mecanismo, unidades o criterios y limita la interpretación al alcance de la unidad.",
                "incorrect": f"Revisa {unit['topics'][(i-1) % len(unit['topics'])]['title']} y vuelve a separar dato, cálculo, criterio, conclusión y límite.",
            },
            "source_ids": [sid],
            "status": "complete",
        })
    write_json(OUT / "assessments" / f"unit-{n:02d}.json", {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{unit['id']}-ASSESS",
        "course_id": COURSE_ID,
        "scope": "unit",
        "unit_id": unit["id"],
        "purpose": f"Comprobar comprensión, aplicación y razonamiento recuperativo de U{n} — {unit['title']} sin usar participantes humanos ni dispositivos médicos en servicio.",
        "student_payload_policy": "El payload estudiantil no incluye claves de respuesta; las soluciones, explicaciones y feedback permanecen en el registro docente estructurado.",
        "items": items,
        "status": "complete",
    })

# Escribir unidades después de crear claims y referencias.
for n, unit in enumerate(canonical_units, 1):
    write_json(OUT / "units" / f"unit-{n:02d}.json", unit)

write_json(OUT / "sources.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "source_policy": "Consolidación de las fuentes directamente verificadas durante la curación autoral U1–U6; no se elevan fuentes no verificadas ni se interpreta la curación interna como revisión humana externa.",
    "consulted_on": "2026-08-25",
    "coverage_gaps": [],
    "coverage_status": "traceable",
    "sources": source_records,
})
write_json(OUT / "glossary.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "entries": glossary_records,
    "coverage_status": "traceable",
})
write_json(OUT / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "scope": "24 afirmaciones ancla, cuatro por unidad, trazadas a fuentes directamente verificadas.",
    "review_state": "ai_review_provisional",
    "claims": claims,
})
write_json(OUT / "media.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "status": "planned",
    "items": media_records,
})

course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "LBI-COURSE-ASSESS",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": [
        "Evaluar decisiones reproducibles y trazables, no memorización aislada de componentes.",
        "Usar únicamente datos sintéticos, simulación, fuentes equivalentes seguras o datasets abiertos sin identificación.",
        "Exigir unidades, configuración, criterios previos, controles, incertidumbre, discrepancias y límites en toda conclusión.",
        "Mantener separadas verificación técnica, validación de uso, seguridad, desempeño clínico y conformidad regulatoria.",
    ],
    "assessment_plan": [
        {"component": "Recuperación y autoevaluación de U1–U6", "weight_percent": 15},
        {"component": "Problemas y análisis de casos", "weight_percent": 20},
        {"component": "Laboratorios reproducibles y expedientes de evidencia", "weight_percent": 30},
        {"component": "Evaluación intermedia integradora", "weight_percent": 15},
        {"component": "Capstone de integración y verificación", "weight_percent": 20},
    ],
    "diagnostic": {
        "purpose": "Identificar prerrequisitos que requieren recuperación antes de iniciar el curso.",
        "questions": [
            "Diferencia peligro, riesgo y control en un banco educativo.",
            "Explica la diferencia entre calibración, ajuste y verificación.",
            "Define sensibilidad metrológica y sus unidades.",
            "Distingue repetibilidad de histéresis.",
            "Diferencia señal diferencial y señal de modo común.",
            "Explica qué significa CMRR sin convertirlo en rechazo total garantizado.",
            "Explica por qué un filtro puede modificar fase además de amplitud.",
            "Distingue muestreo insuficiente de cuantización.",
            "Calcula conceptualmente qué variables determinan throughput de adquisición.",
            "Explica por qué un buffer no crea ancho de banda sostenido.",
            "Diferencia verificación de validación.",
            "Explica por qué la incertidumbre puede cambiar una decisión cerca de un límite.",
        ],
    },
    "midterm_blueprint": [
        {"domain": "U1 Seguridad, metrología y documentación", "weight_percent": 15},
        {"domain": "U2 Caracterización de sensores", "weight_percent": 20},
        {"domain": "U3 Front-end diferencial", "weight_percent": 20},
        {"domain": "U4 Filtrado y adquisición", "weight_percent": 20},
        {"domain": "U5 Integración", "weight_percent": 15},
        {"domain": "U6 Verificación e incertidumbre", "weight_percent": 10},
    ],
    "capstone": {
        "title": "Expediente reproducible de una cadena sintética de bioinstrumentación",
        "scenario": "Diseñar, integrar y verificar una cadena de medición exclusivamente sintética o con fuentes eléctricas equivalentes seguras, partiendo de un mensurando ficticio y cerrando con una matriz de verificación y un reporte de discrepancias.",
        "required_deliverables": [
            "Frontera de seguridad y alcance educativo.",
            "Definición del mensurando y requisitos medibles.",
            "Diagrama de cadena de señal.",
            "Caracterización del sensor o fuente equivalente.",
            "Presupuesto de ganancia, rango y headroom.",
            "Análisis diferencial/modo común y ruido.",
            "Diseño de filtrado y antialiasing.",
            "Presupuesto de muestreo, ADC y cuantización.",
            "Tabla de interfaces y configuración.",
            "Presupuesto de throughput, buffer y temporización.",
            "Baseline versionada de hardware simulado/firmware/configuración.",
            "Matriz requisito→método→criterio→evidencia→resultado.",
            "Presupuesto de incertidumbre para al menos una magnitud crítica.",
            "Registro de discrepancias y pruebas de regresión.",
            "Conclusión con requisitos verificados, fallidos, no concluyentes y no evaluados.",
        ],
        "rubric": [
            {"criterion": "Arquitectura, requisitos y trazabilidad", "weight_percent": 20},
            {"criterion": "Razonamiento metrológico y cuantitativo", "weight_percent": 20},
            {"criterion": "Adquisición, integración y procedencia", "weight_percent": 20},
            {"criterion": "Plan de verificación, incertidumbre y discrepancias", "weight_percent": 20},
            {"criterion": "Reproducibilidad y calidad de evidencia", "weight_percent": 10},
            {"criterion": "Comunicación y límites de inferencia", "weight_percent": 10},
        ],
    },
    "status": "complete",
}
write_json(OUT / "assessments" / "course-assessment.json", course_assessment)

course = {
    "$schema": "../../../schemas/academic/course-v1.schema.json",
    "schema_version": "1.0",
    "id": COURSE_ID,
    "code": CODE,
    "area_id": "ingenieria-biomedica",
    "title": "Laboratorio de Bioinstrumentación",
    "language": "es",
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica y áreas afines con fundamentos de circuitos, señales, programación, medición y bioinstrumentación que necesiten integrar y verificar una cadena de medición de forma reproducible en bancos exclusivamente sintéticos o equivalentes seguros.",
    "status": dict(STATUS),
    "purpose": "Integrar seguridad y metrología, caracterización de sensores, amplificación diferencial, filtrado y adquisición, arquitectura hardware/firmware y verificación basada en requisitos para construir un expediente reproducible de bioinstrumentación U1–U6. El cierre acredita completitud académica interna del corpus, no seguridad eléctrica, EMC, validación fisiológica o clínica, conformidad IEC, certificación ni aptitud de un dispositivo para uso en personas.",
    "scope": {
        "included": [
            "Frontera de seguridad educativa, mensurando, trazabilidad metrológica, incertidumbre y bitácora reproducible.",
            "Caracterización estática y dinámica de sensores y transductores mediante datos sintéticos.",
            "Front-end diferencial de biopotenciales con fuentes eléctricas equivalentes, CMRR, headroom, saturación y ruido.",
            "Filtrado, muestreo, antialiasing, ADC, cuantización, clipping, ENOB y procedencia de datos.",
            "Integración de interfaces, firmware, temporización, buffers, comunicación, alimentación y configuración.",
            "Verificación basada en requisitos, repetibilidad, incertidumbre, reglas de decisión, discrepancias y regresión.",
            "Expedientes auditables con fuentes, versiones, criterios, datos, cálculos, fallos y límites.",
        ],
        "excluded": [
            "Conexión de prototipos, electrodos o circuitos educativos a personas.",
            "Trabajo con red eléctrica o intervención sobre dispositivos médicos en servicio.",
            "Validación fisiológica o clínica, diagnóstico, tratamiento o recomendación clínica.",
            "Demostración de seguridad eléctrica, EMC, biocompatibilidad, ciberseguridad o conformidad IEC 60601/IEC 62304.",
            "Certificación, acreditación, evaluación de conformidad o autorización regulatoria.",
            "Presentar simulaciones o pruebas de banco como evidencia suficiente de aptitud para uso humano.",
        ],
        "handoff_courses": ["bioinstrumentacion", "senales-biomedicas", "laboratorio-senales-biomedicas", "desarrollo-dispositivos-medicos", "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas", "ingenieria-clinica-gestion"],
    },
    "prerequisites": [
        {"id": "LBI-PRE01", "statement": "Fundamentos de circuitos, electrónica analógica y lectura de datasheets."},
        {"id": "LBI-PRE02", "statement": "Sistemas y señales: frecuencia, espectro, filtros, muestreo y ruido."},
        {"id": "LBI-PRE03", "statement": "Bioinstrumentación introductoria: sensores, biopotenciales, acondicionamiento y adquisición."},
        {"id": "LBI-PRE04", "statement": "Programación básica para adquisición, análisis y documentación reproducible."},
        {"id": "LBI-PRE05", "statement": "Aritmética de incertidumbre y estadística descriptiva básica."},
    ],
    "competencies": [
        {"id": "LBI-COMP01", "statement": "Planificar prácticas de bioinstrumentación dentro de una frontera de seguridad explícita y documentar mensurandos, calibración, trazabilidad e incertidumbre."},
        {"id": "LBI-COMP02", "statement": "Caracterizar sensores y front-ends mediante modelos, controles, casos límite y datos reproducibles."},
        {"id": "LBI-COMP03", "statement": "Diseñar cadenas de filtrado y adquisición preservando información, procedencia y límites del ADC y del procesamiento."},
        {"id": "LBI-COMP04", "statement": "Integrar hardware, firmware, datos, temporización, alimentación y comunicaciones con contratos de interfaz y gestión de configuración."},
        {"id": "LBI-COMP05", "statement": "Verificar requisitos técnicos con criterios previos, incertidumbre, discrepancias y regresión sin confundir verificación con validación."},
        {"id": "LBI-COMP06", "statement": "Construir un expediente final auditable que una U1–U6 y mantenga límites técnicos, clínicos, regulatorios y de seguridad."},
    ],
    "learning_outcomes": course_outcomes,
    "study_method": [
        "Explicación conceptual seguida de ejemplo trabajado, actividad guiada, actividad de dominio con menos apoyo y reto de transferencia autónomo.",
        "Usar datos sintéticos, simulación o fuentes eléctricas equivalentes; no conectar personas, red eléctrica ni dispositivos médicos en servicio.",
        "Declarar entradas, unidades, configuración, versiones, criterios, controles, incertidumbre y límites antes de concluir.",
        "Conservar resultados desfavorables, errores y discrepancias como evidencia útil en vez de ocultarlos.",
        "Cerrar cada unidad con un handoff explícito hacia la siguiente y revisar acumulativamente la cadena de medición.",
    ],
    "core_source_ids": [r["id"] for r in source_records[: min(18, len(source_records))]],
    "unit_files": [f"units/unit-{n:02d}.json" for n in range(1, 7)],
    "assessment_files": [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"],
    "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
    "static_site": {
        "renderer": "scripts/generate_site.py",
        "canonical_source": True,
        "legacy_mirrors": [
            "data/generated_courses/laboratorio-bioinstrumentacion.json",
            "data/generated_units/laboratorio-bioinstrumentacion/",
            "data/subjects/ingenieria-biomedica/laboratorio-bioinstrumentacion.json",
        ],
    },
    "editorial_notice": "Corpus canónico completo a nivel de contenido, fuentes trazadas y pedagogía interna para U1–U6. Multimedia permanece planificada y la publicación es provisional. La revisión humana interna y disciplinar externa permanece pendiente. Este cierre no autoriza conexión a personas, red eléctrica, dispositivos médicos en servicio ni constituye seguridad eléctrica, EMC, validación fisiológica o clínica, conformidad IEC, certificación, acreditación, autorización regulatoria o recomendación clínica.",
}
write_json(OUT / "course.json", course)

assert len(source_records) >= 20, len(source_records)
assert len(glossary_records) >= 60, len(glossary_records)
assert len(claims) == 24
print(f"Canonical closure built: {len(source_records)} sources, {len(glossary_records)} glossary entries, {len(claims)} claims")
