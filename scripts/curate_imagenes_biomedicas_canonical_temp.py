#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas"
OUT_ROOT = ROOT / "data" / "courses" / "imagenes-biomedicas"
CODE = "IMGBIO"
COURSE_ID = "imagenes-biomedicas"
TODAY = "2026-08-24"
STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(text))
    ascii_text = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.casefold()).strip("-")
    return slug or "recurso"


def tokens(text: str) -> set[str]:
    ignored = {"para", "como", "desde", "esta", "este", "entre", "sobre", "donde", "cuando", "porque", "mediante", "cada", "una", "uno", "unos", "unas", "del", "las", "los", "con", "sin", "por", "que", "sus", "segun", "según"}
    return {t for t in re.findall(r"[a-z0-9áéíóúñü]+", str(text).casefold()) if len(t) >= 4 and t not in ignored}


def best_source(text: str, source_ids: list[str], source_records: dict[str, dict]) -> str:
    if not source_ids:
        raise RuntimeError("Una unidad canónica no puede quedar sin fuentes")
    wanted = tokens(text)
    scored: list[tuple[int, int, str]] = []
    for position, source_id in enumerate(source_ids):
        source = source_records[source_id]
        haystack = " ".join(str(source.get(k) or "") for k in ("title", "organization", "type", "description"))
        score = len(wanted & tokens(haystack))
        scored.append((score, -position, source_id))
    return max(scored)[2]


def make_unique_id(base: str, used: set[str]) -> str:
    candidate = base
    n = 2
    while candidate in used:
        candidate = f"{base}-{n}"
        n += 1
    used.add(candidate)
    return candidate


def normalize_source(source: dict, unit_id: str, source_records: dict[str, dict], used_ids: set[str], url_to_id: dict[str, str]) -> str:
    url = str(source.get("url") or "").strip()
    title = str(source.get("title") or source.get("name") or "Fuente académica").strip()
    identity = url or title.casefold()
    if identity in url_to_id:
        source_id = url_to_id[identity]
        record = source_records[source_id]
        if unit_id not in record["used_by_unit_ids"]:
            record["used_by_unit_ids"].append(unit_id)
        return source_id
    source_id = make_unique_id(slugify(title)[:96], used_ids)
    record = {
        "id": source_id,
        "title": title,
        "organization": str(source.get("organization") or source.get("authors") or "Fuente académica o institucional").strip(),
        "url": url,
        "type": str(source.get("type") or "referencia académica").strip(),
        "description": str(source.get("description") or "Fuente utilizada para sustentar conceptos y métodos de la unidad.").strip(),
        "verification_status": str(source.get("verification_status") or "verified_directly").strip(),
        "used_by_unit_ids": [unit_id],
    }
    if not record["url"]:
        locator = str(source.get("doi") or source.get("pmid") or source.get("citation") or "").strip()
        record["locator"] = locator
    source_records[source_id] = record
    url_to_id[identity] = source_id
    return source_id


def build() -> None:
    source_course = json.loads((SRC_ROOT / "course.json").read_text(encoding="utf-8"))
    source_units = [json.loads((SRC_ROOT / "units" / f"unit-{n:02d}.json").read_text(encoding="utf-8")) for n in range(1, 7)]

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for child in OUT_ROOT.rglob("*.json"):
        child.unlink()

    source_records: dict[str, dict] = {}
    used_source_ids: set[str] = set()
    source_identity: dict[str, str] = {}
    unit_source_ids: dict[int, list[str]] = {}
    for n, unit in enumerate(source_units, 1):
        unit_id = f"{CODE}-U{n:02d}"
        ids: list[str] = []
        for source in unit.get("sources", []):
            source_id = normalize_source(source, unit_id, source_records, used_source_ids, source_identity)
            if source_id not in ids:
                ids.append(source_id)
        if not ids:
            raise RuntimeError(f"U{n}: sin fuentes trazables")
        unit_source_ids[n] = ids

    glossary_records: list[dict] = []
    glossary_by_term: dict[str, dict] = {}
    unit_glossary_ids: dict[int, list[str]] = {n: [] for n in range(1, 7)}
    glossary_counter = 1
    for n, unit in enumerate(source_units, 1):
        unit_id = f"{CODE}-U{n:02d}"
        for entry in unit.get("glossary", []):
            term = str(entry.get("term") or "").strip()
            definition = str(entry.get("definition") or "").strip()
            if not term or not definition:
                continue
            key = term.casefold()
            if key in glossary_by_term:
                record = glossary_by_term[key]
                if unit_id not in record["unit_ids"]:
                    record["unit_ids"].append(unit_id)
                for sid in unit_source_ids[n]:
                    if sid not in record["source_ids"]:
                        record["source_ids"].append(sid)
                unit_glossary_ids[n].append(record["id"])
                continue
            gid = f"{CODE}-GLO-{glossary_counter:03d}"
            glossary_counter += 1
            sid = best_source(term + " " + definition, unit_source_ids[n], source_records)
            record = {
                "id": gid,
                "term": term,
                "definition": definition,
                "unit_ids": [unit_id],
                "source_ids": [sid],
                "verification_status": "traceable_to_verified_source",
            }
            glossary_records.append(record)
            glossary_by_term[key] = record
            unit_glossary_ids[n].append(gid)

    claim_records: list[dict] = []
    unit_claim_ids: dict[int, list[str]] = {n: [] for n in range(1, 7)}
    for n, unit in enumerate(source_units, 1):
        unit_id = f"{CODE}-U{n:02d}"
        selected: list[str] = []
        for section in unit.get("theory_sections", []):
            for point in section.get("key_points", [])[:1]:
                text = str(point).strip()
                if text and text not in selected:
                    selected.append(text)
        for index, text in enumerate(selected[:6], 1):
            claim_id = f"{CODE}-U{n:02d}-C{index:03d}"
            sid = best_source(text, unit_source_ids[n], source_records)
            source = source_records[sid]
            record = {
                "id": claim_id,
                "claim_id": claim_id,
                "unit": n,
                "unit_id": unit_id,
                "text": text,
                "claim_type": "methodological_or_interpretive",
                "risk": "medium",
                "context": f"Síntesis educativa de {unit.get('title')}; interpretar dentro de la modalidad, protocolo, tarea y límites declarados.",
                "source_id": sid,
                "locator": {"url": source.get("url", ""), "title": source.get("title", "")},
                "support": "direct_or_synthesis",
                "source_verification_status": source.get("verification_status", "verified_directly"),
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": TODAY,
            }
            claim_records.append(record)
            unit_claim_ids[n].append(claim_id)

    media_records: list[dict] = []
    unit_media_ids: dict[int, list[str]] = {}
    for n, unit in enumerate(source_units, 1):
        unit_id = f"{CODE}-U{n:02d}"
        media_id = f"{CODE}-U{n:02d}-MED01"
        media_records.append({
            "id": media_id,
            "type": "figure",
            "status": "planned",
            "unit_id": unit_id,
            "linked_learning_outcome_ids": [f"{CODE}-U{n:02d}-LO01", f"{CODE}-U{n:02d}-LO02"],
            "pedagogical_purpose": f"Representar visualmente el flujo físico y computacional central de {unit.get('title')} y sus principales fuentes de error.",
            "alt_text_draft": None,
            "license_requirements": "Usar material propio o con licencia compatible y registrar atribución, procedencia y transformaciones.",
            "source_ids": [],
        })
        unit_media_ids[n] = [media_id]

    course_los = [
        ("LO01", "Explicar cómo formación física, muestreo, geometría, reconstrucción y visualización determinan qué representa una imagen biomédica y qué información puede perderse."),
        ("LO02", "Analizar radiografía y CT desde atenuación y proyecciones hasta reconstrucción, números de imagen, calidad y descriptores de exposición, manteniendo separados desempeño técnico y decisión clínica."),
        ("LO03", "Explicar MRI desde magnetización, relajación, excitación y codificación espacial hasta contraste, k-space, reconstrucción, artefactos y restricciones de seguridad."),
        ("LO04", "Explicar ultrasonido desde propagación acústica y transducción hasta formación de imagen, Doppler, resolución, artefactos e indicadores de exposición."),
        ("LO05", "Comparar medicina nuclear y modalidades ópticas a partir de trazadores o interacción luz-tejido, detección, formación de imagen, cuantificación, resolución y límites de interpretación."),
        ("LO06", "Evaluar calidad, artefactos, QA/QC y seguridad de forma dependiente de tarea y modalidad mediante métricas, fantomas, líneas base, controles y trazabilidad."),
        ("LO07", "Construir y comunicar análisis reproducibles con datos sintéticos o abiertos, fuentes trazables, supuestos, incertidumbre, controles y límites, sin extrapolar resultados técnicos a recomendaciones clínicas no sustentadas."),
    ]
    course_learning_outcomes = [{"id": f"{CODE}-{suffix}", "statement": statement} for suffix, statement in course_los]

    canonical_units: list[dict] = []
    for n, unit in enumerate(source_units, 1):
        unit_id = f"{CODE}-U{n:02d}"
        local_los = [{"id": f"{unit_id}-LO{i:02d}", "statement": str(text).strip()} for i, text in enumerate(unit.get("learning_objectives", []), 1)]
        if len(local_los) < 5:
            raise RuntimeError(f"U{n}: learning outcomes insuficientes")
        topics: list[dict] = []
        for t_index, section in enumerate(unit.get("theory_sections", []), 1):
            topic_id = f"{unit_id}-T{t_index:02d}"
            equations = []
            for e_index, eq in enumerate(section.get("equations", []), 1):
                equations.append({
                    "id": f"{topic_id}-B{e_index:02d}",
                    "type": "equation",
                    "latex": str(eq.get("latex") or "").strip(),
                    "label": str(eq.get("meaning") or eq.get("label") or "").strip(),
                })
            paragraphs = [str(p).strip() for p in section.get("paragraphs", []) if str(p).strip()]
            key_points = [str(p).strip() for p in section.get("key_points", []) if str(p).strip()]
            if not paragraphs:
                raise RuntimeError(f"U{n} T{t_index}: sin párrafos")
            subtopics = []
            for s_index, paragraph in enumerate(paragraphs, 1):
                title = key_points[s_index - 1] if s_index - 1 < len(key_points) else f"Desarrollo conceptual {s_index}"
                subtopic_id = f"{topic_id}-ST{s_index:02d}"
                subtopics.append({
                    "id": subtopic_id,
                    "title": title,
                    "blocks": [{"id": f"{subtopic_id}-B01", "type": "paragraph", "text": paragraph}],
                })
            topics.append({
                "id": topic_id,
                "title": str(section.get("heading") or f"Tema {t_index}").strip(),
                "blocks": equations,
                "key_points": key_points or [subtopics[0]["title"]],
                "subtopics": subtopics,
            })
        examples = []
        for e_index, example in enumerate(unit.get("worked_examples", []), 1):
            examples.append({
                "id": f"{unit_id}-EX{e_index:02d}",
                "title": str(example.get("title") or f"Ejemplo {e_index}").strip(),
                "scenario": str(example.get("scenario") or "Escenario sintético de la unidad.").strip(),
                "reasoning_steps": [str(x).strip() for x in example.get("reasoning_steps", []) if str(x).strip()],
                "interpretation": str(example.get("answer") or example.get("interpretation") or "Interpretación limitada al escenario y supuestos declarados.").strip(),
                "limitations": [str(x).strip() for x in example.get("limitations", []) if str(x).strip()] or ["No extrapolar el resultado técnico a una decisión clínica no evaluada."],
            })
        if not examples:
            raise RuntimeError(f"U{n}: sin ejemplos")
        activities = []
        for a_index, activity in enumerate(unit.get("guided_activities", []), 1):
            activities.append({
                "id": f"{unit_id}-ACT{a_index:02d}",
                "title": str(activity.get("title") or f"Actividad {a_index}").strip(),
                "purpose": "Practicar de forma reproducible los resultados de aprendizaje de la unidad mediante datos, fantomas o escenarios sintéticos y una interpretación proporcional.",
                "prerequisite_unit_ids": [f"{CODE}-U{n-1:02d}"] if n > 1 else [],
                "instructions": [str(x).strip() for x in activity.get("instructions", []) if str(x).strip()],
                "tasks": [str(x).strip() for x in activity.get("problems", []) if str(x).strip()],
                "deliverables": [str(x).strip() for x in activity.get("deliverables", []) if str(x).strip()],
                "checking_criteria": [str(x).strip() for x in activity.get("checking_criteria", []) if str(x).strip()],
                "estimated_duration_minutes": max(90, 20 * len(activity.get("problems", []))),
                "status": "complete",
            })
        if not activities:
            raise RuntimeError(f"U{n}: sin actividades")
        mapped_los = [f"{CODE}-LO{n:02d}", f"{CODE}-LO07"]
        canonical = {
            "$schema": "../../../../schemas/academic/unit-v1.schema.json",
            "schema_version": "1.0",
            "id": unit_id,
            "course_id": COURSE_ID,
            "order": n,
            "slug": str(unit.get("slug") or slugify(unit.get("title", "unidad"))).strip(),
            "title": str(unit.get("title") or f"Unidad {n}").strip(),
            "status": STATUS,
            "purpose": str(unit.get("purpose") or "").strip(),
            "prerequisite_unit_ids": [f"{CODE}-U{n-1:02d}"] if n > 1 else [],
            "course_learning_outcome_ids": mapped_los,
            "learning_outcomes": local_los,
            "topics": topics,
            "examples": examples,
            "activities": activities,
            "assessment_file": f"assessments/unit-{n:02d}.json",
            "glossary_entry_ids": list(dict.fromkeys(unit_glossary_ids[n])),
            "source_ids": unit_source_ids[n],
            "claim_ids": unit_claim_ids[n],
            "media_ids": unit_media_ids[n],
            "common_errors": unit.get("common_errors", []),
            "biomedical_connections": [
                f"{item.get('topic')}: {item.get('connection')}" if isinstance(item, dict) else str(item)
                for item in unit.get("biomedical_connections", [])
            ],
            "editorial_notice": str(unit.get("editorial_notice") or "Material educativo en revisión; revisión disciplinaria humana pendiente.").strip(),
            "legacy_origin": f"data/course_redevelopment/imagenes-biomedicas/units/unit-{n:02d}.json",
        }
        canonical_units.append(canonical)
        dump(OUT_ROOT / "units" / f"unit-{n:02d}.json", canonical)

        self_assessment = unit.get("self_assessment", [])
        if not self_assessment:
            raise RuntimeError(f"U{n}: sin autoevaluación")
        items = []
        for q_index, item in enumerate(self_assessment, 1):
            prompt = str(item.get("question") or "").strip()
            answer = str(item.get("answer") or "").strip()
            explanation = str(item.get("reasoning") or "").strip()
            misconception = str(item.get("common_error") or "").strip()
            lo_id = local_los[(q_index - 1) % len(local_los)]["id"]
            sid = best_source(prompt + " " + answer + " " + explanation, unit_source_ids[n], source_records)
            items.append({
                "id": f"{unit_id}-Q{q_index:02d}",
                "type": "short_answer",
                "prompt": prompt,
                "linked_learning_outcome_ids": [lo_id],
                "difficulty": "foundational" if q_index <= 3 else "intermediate" if q_index <= 7 else "advanced",
                "cognitive_level": "understand" if q_index <= 3 else "apply" if q_index <= 6 else "analyze",
                "answer_key": {
                    "expected_answer": answer,
                    "explanation": explanation or "La respuesta debe conservar mecanismo, supuesto y límite descritos en la unidad.",
                    "common_misconceptions": [misconception or "Responder sin declarar el alcance de la inferencia."],
                },
                "feedback": {
                    "correct": "Correcto. Conserva el mecanismo, la evidencia y el límite que sostienen la respuesta.",
                    "incorrect": f"Revisa la explicación y contrástala con la fuente indicada. Error a evitar: {misconception or 'confundir descripción técnica con conclusión clínica.'}",
                },
                "source_ids": [sid],
                "status": "complete",
            })
        assessment = {
            "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
            "schema_version": "1.0",
            "id": f"{unit_id}-EVAL",
            "course_id": COURSE_ID,
            "scope": "unit",
            "unit_id": unit_id,
            "purpose": "Autoevaluación formativa con respuesta razonada, retroalimentación recuperativa y fuentes trazables.",
            "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
            "items": items,
            "status": "complete",
        }
        dump(OUT_ROOT / "assessments" / f"unit-{n:02d}.json", assessment)

    sources_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "source_policy": "Priorizar organismos oficiales, estándares, documentación técnica primaria y literatura revisada por pares; vincular cada afirmación solo dentro del alcance de la fuente y mantener revisión disciplinaria humana pendiente.",
        "consulted_on": TODAY,
        "coverage_gaps": [],
        "sources": list(source_records.values()),
    }
    glossary_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "entries": glossary_records,
    }
    claims_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": "Afirmaciones centrales de las seis unidades de Imágenes Biomédicas vinculadas a fuentes verificadas; revisión disciplinaria humana pendiente.",
        "review_state": "ai_review_provisional",
        "claims": claim_records,
    }
    media_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "coverage_status": "planned",
        "items": media_records,
    }
    dump(OUT_ROOT / "sources.json", sources_payload)
    dump(OUT_ROOT / "glossary.json", glossary_payload)
    dump(OUT_ROOT / "claims.json", claims_payload)
    dump(OUT_ROOT / "media.json", media_payload)

    course_assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{CODE}-COURSE-EVAL",
        "course_id": COURSE_ID,
        "scope": "course",
        "principles": [
            "Separar física de formación, procesamiento, métrica técnica e inferencia clínica.",
            "Evaluar razonamiento reproducible, no memorización aislada de modalidades.",
            "Usar datos abiertos o sintéticos y mantener procedencia, parámetros, unidades, controles e incertidumbre.",
            "No puntuar como correcta una conclusión que exceda el alcance de la evidencia aunque el cálculo intermedio sea correcto.",
            "Mantener respuesta y feedback separados del payload inicial en una futura plataforma dinámica."
        ],
        "assessment_plan": [
            {"component": "Recuperación y autoevaluaciones de unidad", "weight_percent": 15, "evidence": "Ítems razonados con feedback y corrección."},
            {"component": "Problemas y casos multimodales", "weight_percent": 25, "evidence": "Cálculos, mecanismos, controles y límites."},
            {"component": "Actividades reproducibles", "weight_percent": 25, "evidence": "Fantomas/datos sintéticos, metadatos, métricas y trazabilidad."},
            {"component": "Revisión y corrección argumentada", "weight_percent": 10, "evidence": "Antes-después con clasificación de hallazgos."},
            {"component": "Proyecto integrador", "weight_percent": 25, "evidence": "Comparación responsable de modalidades para una tarea definida."}
        ],
        "diagnostic": {
            "purpose": "Detectar prerrequisitos que requieren recuperación antes de U1.",
            "questions": [
                "¿Qué diferencia hay entre fenómeno físico, señal medida y píxel reconstruido?",
                "¿Qué significa muestrear una variable continua y qué es aliasing?",
                "¿Cómo interpretarías una exponencial de atenuación sin confundir parámetro físico con diagnóstico?",
                "¿Qué información debe acompañar a una imagen para que un análisis sea reproducible?",
                "¿Por qué una modalidad sin radiación ionizante puede seguir teniendo riesgos?"
            ],
            "use": "No calificativo; asigna recuperación de física, muestreo, anatomía o trazabilidad según los errores."
        },
        "midterm_blueprint": [
            {"domain": "U1 Formación y representación", "weight_percent": 17, "course_learning_outcome_ids": [f"{CODE}-LO01"]},
            {"domain": "U2 Radiografía y CT", "weight_percent": 17, "course_learning_outcome_ids": [f"{CODE}-LO02"]},
            {"domain": "U3 MRI", "weight_percent": 17, "course_learning_outcome_ids": [f"{CODE}-LO03"]},
            {"domain": "U4 Ultrasonido", "weight_percent": 17, "course_learning_outcome_ids": [f"{CODE}-LO04"]},
            {"domain": "U5 Nuclear y óptica", "weight_percent": 16, "course_learning_outcome_ids": [f"{CODE}-LO05"]},
            {"domain": "U6 Calidad, QA y seguridad", "weight_percent": 16, "course_learning_outcome_ids": [f"{CODE}-LO06", f"{CODE}-LO07"]}
        ],
        "capstone": {
            "title": "Expediente multimodal reproducible para una tarea de imagen sintética",
            "brief": "Definir una tarea, comparar al menos tres modalidades desde física y cadena de formación hasta calidad, artefactos, QA y seguridad; justificar qué modalidad o combinación responde mejor a la tarea técnica sin convertir el resultado en recomendación clínica.",
            "required_deliverables": [
                "Pregunta y tarea de imagen operacionalizadas.",
                "Mapa físico-computacional de cada modalidad seleccionada.",
                "Datos, fantomas o simulaciones sintéticas con procedencia y parámetros.",
                "Métricas de resolución/contraste/ruido apropiadas a la tarea.",
                "Análisis de artefactos, sensibilidad e incertidumbre.",
                "Matriz de QA/QC y seguridad con límites de interpretación.",
                "Conclusión proporcional y lista de evidencia adicional necesaria para una decisión clínica."
            ],
            "rubric": [
                {"criterion": "Física y representación correctas", "weight_percent": 25, "excellent": "Relaciona mecanismo, observable y reconstrucción sin saltos causales."},
                {"criterion": "Método y reproducibilidad", "weight_percent": 25, "excellent": "Procedencia, parámetros, métricas y controles permiten reproducir el análisis."},
                {"criterion": "Calidad, artefactos e incertidumbre", "weight_percent": 20, "excellent": "Separa métricas, identifica mecanismos y cuantifica sensibilidad cuando corresponde."},
                {"criterion": "Seguridad y QA/QC", "weight_percent": 15, "excellent": "Diferencia riesgos por modalidad y propone controles sin prescribir operación clínica."},
                {"criterion": "Interpretación y comunicación", "weight_percent": 15, "excellent": "La conclusión responde solo a la tarea y declara límites y evidencia faltante."}
            ]
        },
        "status": "complete",
    }
    dump(OUT_ROOT / "assessments" / "course-assessment.json", course_assessment)

    course = {
        "$schema": "../../../schemas/academic/course-v1.schema.json",
        "schema_version": "1.0",
        "id": COURSE_ID,
        "code": CODE,
        "area_id": "ingenieria-biomedica",
        "title": "Imágenes Biomédicas",
        "language": "es",
        "content_version": "1.0.0",
        "academic_level": "Pregrado universitario intermedio y avanzado",
        "audience": "Estudiantes de ingeniería biomédica, biomedicina computacional y áreas afines que requieren fundamentos reproducibles de formación, análisis, calidad y seguridad en imagen biomédica.",
        "status": STATUS,
        "purpose": "Construir una comprensión integrada y reproducible de la imagen biomédica desde la formación física y representación digital hasta radiografía/CT, MRI, ultrasonido, medicina nuclear, óptica, calidad, artefactos, QA/QC y seguridad, manteniendo separados desempeño técnico, validez científica y decisión clínica.",
        "scope": {
            "included": [
                "Formación y representación digital de imagen, muestreo espacial, resolución, contraste y metadatos.",
                "Radiografía y CT: atenuación, proyecciones, reconstrucción, calidad y descriptores de exposición.",
                "MRI: magnetización, relajación, secuencias, codificación espacial, k-space, artefactos y seguridad.",
                "Ultrasonido: propagación, transducción, formación de imagen, Doppler, artefactos y exposición acústica.",
                "Medicina nuclear y óptica: trazadores o interacción luz-tejido, detección, imagen funcional/molecular y cuantificación.",
                "Calidad dependiente de tarea, MTF/NPS/SNR/CNR, artefactos, QA/QC, fantomas y seguridad multimodal.",
                "Actividades reproducibles con datos abiertos o sintéticos y comunicación proporcional."
            ],
            "excluded": [
                "Diagnóstico de pacientes o interpretación clínica autónoma de estudios reales.",
                "Prescripción de protocolos, dosis, actividades administradas, parámetros MRI, índices acústicos o límites de exposición.",
                "Operación de equipos clínicos sin formación, supervisión y procedimientos institucionales.",
                "Técnicas avanzadas especializadas de reconstrucción, aprendizaje profundo o imagen cuantitativa que pertenecen a cursos posteriores."
            ],
            "handoff_courses": ["imagenes-biomedicas-avanzadas-i", "imagenes-biomedicas-avanzadas-ii", "laboratorio-imagenes-biomedicas", "tratamiento-digital-imagenes"]
        },
        "prerequisites": [
            {"id": f"{CODE}-PRE01", "statement": "Álgebra, funciones, exponenciales, logaritmos y trigonometría de nivel universitario inicial."},
            {"id": f"{CODE}-PRE02", "statement": "Fundamentos de física, ondas, energía y electricidad suficientes para seguir modelos de interacción materia-energía."},
            {"id": f"{CODE}-PRE03", "statement": "Anatomía y fisiología básicas para reconocer que una imagen representa propiedades físicas relacionadas con estructura o función, no diagnósticos automáticos."}
        ],
        "competencies": [
            {"id": f"{CODE}-COMP01", "statement": "Construir modelos físico-computacionales que conecten objeto, interacción, detector, muestreo, reconstrucción y representación."},
            {"id": f"{CODE}-COMP02", "statement": "Seleccionar métricas, controles y fantomas acordes con una tarea de imagen y explicar sus límites."},
            {"id": f"{CODE}-COMP03", "statement": "Analizar artefactos y errores por mecanismo, proponiendo pruebas discriminantes y análisis de sensibilidad."},
            {"id": f"{CODE}-COMP04", "statement": "Documentar un análisis de imagen con procedencia, unidades, parámetros, versiones, incertidumbre y registro de decisiones."},
            {"id": f"{CODE}-COMP05", "statement": "Comparar modalidades sin confundir calidad técnica, seguridad, validez científica y utilidad clínica."}
        ],
        "learning_outcomes": course_learning_outcomes,
        "study_method": [
            "Leer cada unidad preguntando qué propiedad física se observa, cómo se codifica y qué información se pierde.",
            "Rehacer los ejemplos antes de consultar la interpretación y contrastar supuestos y unidades.",
            "Completar actividades con datos sintéticos o abiertos y registrar parámetros, métricas, controles y limitaciones.",
            "Usar la autoevaluación como recuperación: explicar por qué una respuesta incorrecta falla y volver al subtema relevante.",
            "Cerrar cada modalidad con una tabla de qué mide, qué reconstruye, qué artefactos admite, qué riesgos posee y qué no puede inferirse."
        ],
        "core_source_ids": list(dict.fromkeys(unit_source_ids[n][0] for n in range(1, 7))),
        "unit_files": [f"units/unit-{n:02d}.json" for n in range(1, 7)],
        "assessment_files": [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"],
        "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
        "static_site": {
            "renderer": "scripts/generate_site.py",
            "canonical_source": True,
            "legacy_mirrors": [
                "data/course_redevelopment/imagenes-biomedicas/course.json",
                "data/course_redevelopment/imagenes-biomedicas/units/",
                "data/generated_units/imagenes-biomedicas/",
                "data/subjects/ingenieria-biomedica/imagenes-biomedicas.json"
            ]
        },
        "editorial_notice": "Corpus canónico educativo con contenido y pedagogía completos y fuentes trazables. La revisión interna automática y la curación editorial no constituyen revisión disciplinaria humana, validación clínica, certificación de seguridad ni autorización para operar equipos o prescribir protocolos; multimedia permanece planificada y las revisiones interna/externa humanas están pendientes."
    }
    dump(OUT_ROOT / "course.json", course)

    print(f"[ok] cierre canónico {COURSE_ID}: {len(canonical_units)} unidades, {len(source_records)} fuentes, {len(glossary_records)} términos, {len(claim_records)} claims")


if __name__ == "__main__":
    build()
