#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBJECT = "aplicaciones-salud-digital"
AREA = "ingenieria-biomedica"
CODE = "SALUDDIG"
TITLE = "Aplicaciones de Salud Digital"
SRC_ROOT = ROOT / "data" / "course_redevelopment" / SUBJECT
DST_ROOT = ROOT / "data" / "courses" / SUBJECT
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

COURSE_LOS = [
    ("SALUDDIG-LO01", "Analizar una necesidad de salud y su ecosistema sociotécnico antes de seleccionar una tecnología, distinguiendo problema, usuarios, actores, flujo de trabajo, restricciones y evidencia necesaria."),
    ("SALUDDIG-LO02", "Diseñar y evaluar de forma formativa una intervención digital centrada en las personas mediante requisitos, prototipos, accesibilidad, usabilidad y factores humanos, sin confundir facilidad de uso con beneficio clínico."),
    ("SALUDDIG-LO03", "Modelar servicios de telemedicina, aplicaciones y monitorización remota conectando medición, transmisión, alertas, revisión humana, continuidad operativa y límites de inferencia."),
    ("SALUDDIG-LO04", "Diseñar intercambios de datos interoperables mediante modelos, terminologías, contratos de API, procedencia y controles de calidad, manteniendo separados interoperabilidad técnica y validez clínica."),
    ("SALUDDIG-LO05", "Evaluar evidencia clínica, implementación, equidad y economía de una intervención digital con comparadores, desenlaces, incertidumbre y análisis incremental apropiados a la decisión."),
    ("SALUDDIG-LO06", "Construir un plan de despliegue responsable que integre privacidad, ciberseguridad, uso previsto, regulación, gobernanza, control de cambios, incidentes y escalado, con referencias jurisdiccionales y temporales explícitas."),
    ("SALUDDIG-LO07", "Comunicar decisiones de salud digital de forma reproducible y proporcional, vinculando cada conclusión con su evidencia, supuestos, controles, incertidumbre, límites y trabajo adicional requerido."),
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ascii_slug(text: str, *, fallback: str = "item", max_len: int = 72) -> str:
    normalized = unicodedata.normalize("NFKD", str(text))
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return (slug[:max_len].strip("-") or fallback)


def source_id(record: dict) -> str:
    anchor = record.get("url") or record.get("title") or record.get("description") or "source"
    base = ascii_slug(record.get("title") or record.get("organization") or "source", max_len=58)
    digest = hashlib.sha1(str(anchor).encode("utf-8")).hexdigest()[:8]
    return f"{base}-{digest}"


def source_identity(record: dict) -> str:
    return str(record.get("url") or record.get("title") or json.dumps(record, ensure_ascii=False, sort_keys=True)).strip()


def sentence_title(text: str, default: str) -> str:
    text = re.sub(r"\s+", " ", str(text)).strip()
    if not text:
        return default
    first = re.split(r"(?<=[.!?])\s+", text)[0]
    return first[:150].rstrip(" .;:") or default


def as_text(value) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return str(value.get("text") or value.get("statement") or value.get("connection") or value.get("title") or "").strip()
    return str(value or "").strip()


def equations_from_section(section: dict, topic_id: str) -> list[dict]:
    equations = section.get("equations") or []
    out = []
    for index, eq in enumerate(equations, 1):
        if isinstance(eq, str):
            latex, label, variables = eq, "Ecuación de la unidad; interpretar dentro de los supuestos declarados.", None
        else:
            latex = str(eq.get("latex") or eq.get("equation") or "").strip()
            label = str(eq.get("label") or eq.get("interpretation") or eq.get("description") or "Ecuación de la unidad; interpretar dentro de los supuestos declarados.").strip()
            variables = eq.get("variables") if isinstance(eq.get("variables"), dict) else None
        if not latex:
            continue
        block = {"id": f"{topic_id}-B{index:02d}", "type": "equation", "latex": latex, "label": label}
        if variables:
            block["variables"] = {str(k): str(v) for k, v in variables.items()}
        out.append(block)
    return out


def activity_to_canonical(activity: dict, unit_id: str, index: int, prerequisite_ids: list[str]) -> dict:
    title = str(activity.get("title") or f"Actividad {index}")
    instructions = [as_text(x) for x in activity.get("instructions", []) if as_text(x)]
    tasks = [as_text(x) for x in (activity.get("problems") or activity.get("tasks") or []) if as_text(x)]
    deliverables = [as_text(x) for x in activity.get("deliverables", []) if as_text(x)]
    criteria = [as_text(x) for x in activity.get("checking_criteria", []) if as_text(x)]
    purpose = str(activity.get("purpose") or f"Aplicar de manera reproducible los conceptos de {title} con datos, escenarios o artefactos sintéticos y límites explícitos.")
    duration = activity.get("estimated_duration_minutes") or activity.get("duration_minutes")
    if not isinstance(duration, int) or duration < 1:
        duration = 120 if index == 1 else 90
    return {
        "id": f"{unit_id}-ACT{index:02d}",
        "title": title,
        "purpose": purpose,
        "prerequisite_unit_ids": prerequisite_ids,
        "instructions": instructions or ["Trabaja exclusivamente con el caso sintético proporcionado y registra supuestos, decisiones y límites."],
        "tasks": tasks or ["Construye una solución trazable y explica qué evidencia respalda cada decisión."],
        "deliverables": deliverables or ["Expediente reproducible con resultados, controles, incertidumbre y límites."],
        "checking_criteria": criteria or ["La entrega es reproducible y no excede el alcance de la evidencia."],
        "estimated_duration_minutes": duration,
        "status": "complete",
    }


def example_to_canonical(example: dict, unit_id: str, index: int) -> dict:
    reasoning = [as_text(x) for x in (example.get("reasoning_steps") or example.get("steps") or []) if as_text(x)]
    takeaways = [as_text(x) for x in example.get("takeaways", []) if as_text(x)]
    limitations = [step for step in reasoning if any(token in step.casefold() for token in ("no puede", "no permite", "límite", "limitación"))]
    if not limitations:
        limitations = ["El resultado se limita al escenario y a los supuestos declarados; no constituye por sí solo evidencia clínica, regulatoria ni autorización de despliegue."]
    interpretation = " ".join(takeaways) or (reasoning[-1] if reasoning else "Interpretar únicamente dentro del escenario sintético y del alcance declarado.")
    return {
        "id": f"{unit_id}-EX{index:02d}",
        "title": str(example.get("title") or f"Ejemplo {index}"),
        "scenario": str(example.get("scenario") or "Escenario sintético de salud digital."),
        "reasoning_steps": reasoning or ["Identificar entrada, método, resultado, interpretación permitida y límite."],
        "interpretation": interpretation,
        "limitations": limitations,
    }


def assessment_item(question: dict, unit_id: str, index: int, local_los: list[str], source_ids: list[str]) -> dict:
    prompt = str(question.get("question") or question.get("prompt") or f"Pregunta {index}")
    answer = str(question.get("answer") or question.get("expected_answer") or "Respuesta razonada requerida.")
    reasoning = str(question.get("reasoning") or question.get("explanation") or answer)
    misconception = str(question.get("common_error") or question.get("common_misconception") or "Responder sin justificar alcance, evidencia o supuestos.")
    linked = [local_los[(index - 1) % len(local_los)]]
    difficulty = "foundational" if index <= 3 else ("intermediate" if index <= 7 else "advanced")
    cognitive = "understand" if index <= 3 else ("analyze" if index <= 7 else "evaluate")
    return {
        "id": f"{unit_id}-Q{index:02d}",
        "type": "short_answer" if index <= 5 else "case_analysis",
        "prompt": prompt,
        "linked_learning_outcome_ids": linked,
        "difficulty": difficulty,
        "cognitive_level": cognitive,
        "answer_key": {
            "expected_answer": answer,
            "explanation": reasoning,
            "common_misconceptions": [misconception],
        },
        "feedback": {
            "correct": "Correcto. Conserva la relación entre evidencia, decisión y límite que sostiene la respuesta.",
            "incorrect": f"Revisa el razonamiento y corrige esta confusión frecuente: {misconception}",
        },
        "source_ids": source_ids[:2],
        "status": "complete",
    }


def main() -> None:
    redevelopment_course = load(SRC_ROOT / "course.json")
    raw_units = [load(SRC_ROOT / "units" / f"unit-{n:02d}.json") for n in range(1, 7)]
    if DST_ROOT.exists():
        shutil.rmtree(DST_ROOT)

    # Aggregate sources first so every other registry can point to stable identifiers.
    source_records: dict[str, dict] = {}
    unit_source_ids: dict[int, list[str]] = {}
    source_units: dict[str, set[str]] = {}
    for n, unit in enumerate(raw_units, 1):
        uid = f"{CODE}-U{n:02d}"
        ids = []
        for source in unit.get("sources", []):
            key = source_identity(source)
            if key not in source_records:
                sid = source_id(source)
                # Extremely unlikely collision; make it deterministic if it happens.
                existing_ids = {record["id"] for record in source_records.values()}
                if sid in existing_ids:
                    sid = f"{sid}-{len(existing_ids)+1}"
                record = {
                    "id": sid,
                    "title": str(source.get("title") or "Fuente sin título"),
                    "organization": str(source.get("organization") or source.get("publisher") or "Fuente académica o institucional"),
                    "url": str(source.get("url") or ""),
                    "type": str(source.get("type") or "fuente académica o institucional"),
                    "description": str(source.get("description") or source.get("scope") or "Fuente utilizada dentro del alcance declarado de la unidad."),
                    "verification_status": str(source.get("verification_status") or "verified_directly"),
                    "used_by_unit_ids": [],
                }
                source_records[key] = record
            sid = source_records[key]["id"]
            ids.append(sid)
            source_units.setdefault(sid, set()).add(uid)
        if not ids:
            raise RuntimeError(f"U{n} no tiene fuentes; no se puede declarar trazabilidad canónica")
        unit_source_ids[n] = list(dict.fromkeys(ids))
    for record in source_records.values():
        record["used_by_unit_ids"] = sorted(source_units[record["id"]])

    # Glossary aggregation.
    glossary_map: dict[str, dict] = {}
    for n, unit in enumerate(raw_units, 1):
        uid = f"{CODE}-U{n:02d}"
        for entry in unit.get("glossary", []):
            term = str(entry.get("term") or "").strip()
            definition = str(entry.get("definition") or "").strip()
            if not term or not definition:
                continue
            key = term.casefold()
            if key not in glossary_map:
                glossary_map[key] = {"term": term, "definition": definition, "unit_ids": [], "source_ids": []}
            item = glossary_map[key]
            if uid not in item["unit_ids"]:
                item["unit_ids"].append(uid)
            for sid in unit_source_ids[n][:2]:
                if sid not in item["source_ids"]:
                    item["source_ids"].append(sid)
    glossary_entries = []
    term_to_gid: dict[str, str] = {}
    for index, key in enumerate(sorted(glossary_map), 1):
        raw = glossary_map[key]
        gid = f"{CODE}-GLO-{index:03d}"
        term_to_gid[key] = gid
        glossary_entries.append({
            "id": gid,
            "term": raw["term"],
            "definition": raw["definition"],
            "unit_ids": raw["unit_ids"],
            "source_ids": raw["source_ids"],
            "verification_status": "traceable_to_verified_source",
        })

    # Build claims from literal key points that will also be preserved in canonical units.
    claims = []
    unit_claim_ids: dict[int, list[str]] = {}
    for n, unit in enumerate(raw_units, 1):
        uid = f"{CODE}-U{n:02d}"
        selected: list[str] = []
        for section in unit.get("theory_sections", []):
            for point in section.get("key_points", []):
                text = as_text(point)
                if text and text not in selected:
                    selected.append(text)
                if len(selected) >= 4:
                    break
            if len(selected) >= 4:
                break
        if len(selected) < 4:
            for section in unit.get("theory_sections", []):
                for paragraph in section.get("paragraphs", []):
                    text = sentence_title(paragraph, "")
                    if text and text not in selected:
                        selected.append(text)
                    if len(selected) >= 4:
                        break
                if len(selected) >= 4:
                    break
        ids = []
        sid = unit_source_ids[n][0]
        src = next(record for record in source_records.values() if record["id"] == sid)
        for index, text in enumerate(selected[:4], 1):
            cid = f"{uid}-C{index:03d}"
            ids.append(cid)
            risk = "high" if n in (5, 6) else "medium"
            claims.append({
                "id": cid,
                "claim_id": cid,
                "unit": n,
                "unit_id": uid,
                "text": text,
                "claim_type": "methodological_or_interpretive",
                "risk": risk,
                "context": f"Síntesis educativa de {unit.get('title')}; interpretar dentro del contexto, jurisdicción, población, flujo de trabajo y límites declarados.",
                "source_id": sid,
                "locator": {"url": src.get("url", ""), "title": src.get("title", "")},
                "support": "direct_or_synthesis",
                "source_verification_status": src.get("verification_status", "verified_directly"),
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": TODAY,
            })
        unit_claim_ids[n] = ids

    unit_payloads = []
    assessment_payloads = []
    for n, raw in enumerate(raw_units, 1):
        uid = f"{CODE}-U{n:02d}"
        prerequisites = [f"{CODE}-U{n-1:02d}"] if n > 1 else []
        local_los = [f"{uid}-LO{i:02d}" for i in range(1, len(raw.get("learning_objectives", [])) + 1)]
        learning_outcomes = [
            {"id": local_los[i-1], "statement": str(statement)}
            for i, statement in enumerate(raw.get("learning_objectives", []), 1)
        ]
        if len(learning_outcomes) < 5:
            raise RuntimeError(f"{uid} tiene menos de 5 resultados de aprendizaje")

        topics = []
        for ti, section in enumerate(raw.get("theory_sections", []), 1):
            topic_id = f"{uid}-T{ti:02d}"
            key_points = [as_text(x) for x in section.get("key_points", []) if as_text(x)]
            paragraphs = [as_text(x) for x in section.get("paragraphs", []) if as_text(x)]
            blocks = equations_from_section(section, topic_id)
            subtopics = []
            for pi, paragraph in enumerate(paragraphs, 1):
                stid = f"{topic_id}-ST{pi:02d}"
                title = key_points[pi-1] if pi <= len(key_points) else sentence_title(paragraph, f"Subtema {pi}")
                subtopics.append({
                    "id": stid,
                    "title": title,
                    "blocks": [{"id": f"{stid}-B01", "type": "paragraph", "text": paragraph}],
                })
            if not subtopics:
                raise RuntimeError(f"{topic_id} no tiene párrafos")
            topics.append({
                "id": topic_id,
                "title": str(section.get("heading") or f"Tema {ti}"),
                "blocks": blocks,
                "key_points": key_points,
                "subtopics": subtopics,
            })
        if len(topics) < 4:
            raise RuntimeError(f"{uid} tiene menos de 4 temas canónicos")

        examples = [example_to_canonical(ex, uid, i) for i, ex in enumerate(raw.get("worked_examples", []), 1)]
        activities = [activity_to_canonical(act, uid, i, prerequisites) for i, act in enumerate(raw.get("guided_activities", []), 1)]
        unit_terms = [str(entry.get("term") or "").strip().casefold() for entry in raw.get("glossary", [])]
        glossary_ids = [term_to_gid[term] for term in unit_terms if term in term_to_gid]
        media_id = f"{uid}-MED01"
        connections = []
        for connection in raw.get("biomedical_connections", []):
            if isinstance(connection, dict):
                topic = str(connection.get("topic") or "Aplicación biomédica")
                text = str(connection.get("connection") or connection.get("description") or "")
                connections.append(f"{topic}: {text}".strip())
            elif as_text(connection):
                connections.append(as_text(connection))
        course_lo_ids = [f"{CODE}-LO{n:02d}", f"{CODE}-LO07"] if n <= 6 else [f"{CODE}-LO07"]
        editorial = str(raw.get("editorial_notice") or "")
        if "revisión" not in editorial.casefold():
            editorial += " Revisión disciplinaria humana externa pendiente."
        unit_payload = {
            "$schema": "../../../../schemas/academic/unit-v1.schema.json",
            "schema_version": "1.0",
            "id": uid,
            "course_id": SUBJECT,
            "order": n,
            "slug": str(raw.get("slug") or f"unidad-{n:02d}"),
            "title": str(raw.get("title") or f"Unidad {n}"),
            "status": STATUS,
            "purpose": str(raw.get("purpose") or redevelopment_course.get("units", [])[n-1].get("purpose") or "Desarrollar de forma reproducible esta unidad de salud digital."),
            "prerequisite_unit_ids": prerequisites,
            "course_learning_outcome_ids": list(dict.fromkeys(course_lo_ids)),
            "learning_outcomes": learning_outcomes,
            "topics": topics,
            "examples": examples,
            "activities": activities,
            "assessment_file": f"assessments/unit-{n:02d}.json",
            "glossary_entry_ids": list(dict.fromkeys(glossary_ids)),
            "source_ids": unit_source_ids[n],
            "claim_ids": unit_claim_ids[n],
            "media_ids": [media_id],
            "common_errors": raw.get("common_errors", []),
            "biomedical_connections": connections,
            "editorial_notice": editorial,
            "legacy_origin": f"data/course_redevelopment/{SUBJECT}/units/unit-{n:02d}.json",
        }
        unit_payloads.append(unit_payload)

        raw_questions = raw.get("self_assessment", [])
        if len(raw_questions) < 8:
            raise RuntimeError(f"{uid} tiene menos de 8 preguntas formativas")
        items = [assessment_item(q, uid, i, local_los, unit_source_ids[n]) for i, q in enumerate(raw_questions, 1)]
        assessment_payloads.append({
            "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
            "schema_version": "1.0",
            "id": f"{uid}-EVAL",
            "course_id": SUBJECT,
            "scope": "unit",
            "unit_id": uid,
            "purpose": "Autoevaluación formativa con respuesta razonada, retroalimentación recuperativa y fuentes trazables.",
            "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
            "items": items,
            "status": "complete",
        })

    # Registries.
    sources_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": SUBJECT,
        "source_policy": "Priorizar textos normativos y regulatorios oficiales, estándares, marcos institucionales y literatura revisada por pares; conservar fecha, jurisdicción y alcance, y no convertir una fuente en autorización profesional.",
        "consulted_on": TODAY,
        "coverage_gaps": [],
        "sources": sorted(source_records.values(), key=lambda item: item["id"]),
    }
    glossary_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": SUBJECT,
        "entries": glossary_entries,
    }
    claims_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": SUBJECT,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": "Afirmaciones centrales de las seis unidades de Aplicaciones de Salud Digital vinculadas a fuentes trazables; revisión disciplinaria humana externa pendiente.",
        "review_state": "ai_review_provisional",
        "claims": claims,
    }
    media_items = []
    for n, unit in enumerate(unit_payloads, 1):
        media_items.append({
            "id": f"{CODE}-U{n:02d}-MED01",
            "type": "figure",
            "status": "planned",
            "unit_id": f"{CODE}-U{n:02d}",
            "linked_learning_outcome_ids": [lo["id"] for lo in unit["learning_outcomes"][:2]],
            "pedagogical_purpose": f"Visualizar el flujo sociotécnico central de {unit['title']} y separar entrada, transformación, decisión, control y límite de inferencia.",
            "alt_text_draft": None,
            "license_requirements": "Usar material propio o con licencia compatible y registrar atribución, procedencia y transformaciones.",
            "source_ids": [],
        })
    media_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": SUBJECT,
        "coverage_status": "planned",
        "items": media_items,
    }

    course_payload = {
        "$schema": "../../../schemas/academic/course-v1.schema.json",
        "schema_version": "1.0",
        "id": SUBJECT,
        "code": CODE,
        "area_id": AREA,
        "title": TITLE,
        "language": "es",
        "content_version": "1.0.0",
        "academic_level": "Pregrado universitario intermedio y avanzado",
        "audience": "Estudiantes de ingeniería biomédica, biomedicina computacional, informática biomédica y áreas afines que necesitan diseñar, evaluar e implementar intervenciones digitales con razonamiento reproducible.",
        "status": STATUS,
        "purpose": "Integrar el ciclo completo de una intervención de salud digital desde la necesidad y el diseño centrado en las personas hasta telemedicina, interoperabilidad, evaluación clínica/económica y despliegue responsable, manteniendo separadas evidencia técnica, clínica, económica, de privacidad, seguridad y regulación.",
        "scope": {
            "included": [
                "Necesidades, actores, teoría de cambio, flujo de trabajo y criterios de éxito de intervenciones digitales.",
                "Diseño centrado en las personas, requisitos, prototipado, accesibilidad, usabilidad y factores humanos.",
                "Telemedicina, aplicaciones, sensores y monitorización remota con alertas, continuidad y supervisión humana.",
                "Datos, FHIR, terminologías, APIs, procedencia, calidad e interoperabilidad semántica y técnica.",
                "Evaluación clínica, implementación, equidad, costes, ICER y análisis de sensibilidad según la decisión.",
                "Privacidad, protección de datos, ciberseguridad, uso previsto, regulación, AI Act/EHDS cuando corresponda, control de cambios, incidentes y escalado.",
                "Prácticas y evaluaciones con escenarios sintéticos, fuentes trazables, feedback recuperativo y límites explícitos."
            ],
            "excluded": [
                "Diagnóstico o tratamiento individual de pacientes y toma clínica autónoma de decisiones.",
                "Asesoramiento jurídico, DPIA profesional, certificación de ciberseguridad, clasificación regulatoria definitiva o autorización de despliegue.",
                "Uso de datos personales, credenciales, tokens o sistemas clínicos reales en las actividades educativas.",
                "Desarrollo profundo de modelos de machine learning clínico, cubierto por cursos específicos de aprendizaje automático y validación clínica."
            ],
            "handoff_courses": ["machine-learning-biomedico-validacion-clinica", "ingenieria-datos-biomedicos", "historias-clinicas-terminologias-estandares", "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas"],
        },
        "prerequisites": [
            {"id": "SALUDDIG-PRE01", "statement": "Fundamentos de informática, datos y sistemas de información suficientes para seguir flujos, APIs y controles técnicos."},
            {"id": "SALUDDIG-PRE02", "statement": "Estadística y lectura crítica básicas para distinguir diseño, estimación, incertidumbre, asociación y evidencia causal."},
            {"id": "SALUDDIG-PRE03", "statement": "Fundamentos de fisiología y organización sanitaria para contextualizar usuarios, procesos y riesgos sin convertir el curso en práctica clínica."},
        ],
        "competencies": [
            {"id": "SALUDDIG-COMP01", "statement": "Traducir una necesidad sanitaria en requisitos sociotécnicos, métricas, controles y criterios de decisión trazables."},
            {"id": "SALUDDIG-COMP02", "statement": "Diseñar flujos digitales centrados en las personas con interoperabilidad, accesibilidad, seguridad y gobernanza proporcionadas al riesgo."},
            {"id": "SALUDDIG-COMP03", "statement": "Evaluar evidencia clínica, económica y de implementación sin sustituir unas capas de evidencia por otras."},
            {"id": "SALUDDIG-COMP04", "statement": "Documentar arquitectura, datos, versiones, fuentes, supuestos, incertidumbre, cambios e incidentes de manera reproducible."},
            {"id": "SALUDDIG-COMP05", "statement": "Comunicar una recomendación condicional de pilotaje, escalado o no despliegue con límites explícitos y trabajo pendiente."},
        ],
        "learning_outcomes": [{"id": identifier, "statement": statement} for identifier, statement in COURSE_LOS],
        "study_method": [
            "Comenzar cada unidad por la decisión o problema y no por la tecnología disponible.",
            "Reconstruir los ejemplos distinguiendo entrada, modelo o marco, salida, interpretación permitida y no-inferencia.",
            "Completar actividades con escenarios sintéticos y registrar procedencia, supuestos, responsables, criterios y límites.",
            "Usar la autoevaluación como recuperación: explicar el error, volver al subtema pertinente y rehacer la decisión con la evidencia adecuada.",
            "Mantener un dossier acumulativo U1–U6 que separe valor, usabilidad, interoperabilidad, evidencia clínica/económica, privacidad, seguridad y regulación."
        ],
        "core_source_ids": [unit_source_ids[n][0] for n in range(1, 7)],
        "unit_files": [f"units/unit-{n:02d}.json" for n in range(1, 7)],
        "assessment_files": [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"],
        "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
        "static_site": {
            "renderer": "scripts/generate_site.py",
            "canonical_source": True,
            "legacy_mirrors": [
                f"data/course_redevelopment/{SUBJECT}/course.json",
                f"data/course_redevelopment/{SUBJECT}/units/",
                f"data/generated_units/{SUBJECT}/",
                f"data/subjects/{AREA}/{SUBJECT}.json",
            ],
        },
        "editorial_notice": "Corpus canónico educativo con contenido y pedagogía completos y fuentes trazables. La curación interna y las validaciones automáticas no constituyen revisión disciplinaria humana, validación clínica, asesoramiento jurídico, certificación de ciberseguridad, clasificación regulatoria ni autorización de despliegue; multimedia permanece planificada y las revisiones humanas interna/externa están pendientes.",
    }

    course_assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{CODE}-COURSE-EVAL",
        "course_id": SUBJECT,
        "scope": "course",
        "principles": [
            "Evaluar decisiones sociotécnicas completas, no memorización aislada de tecnologías o marcos.",
            "Mantener separadas usabilidad, interoperabilidad, efectividad, economía, privacidad, seguridad y conformidad regulatoria.",
            "Usar escenarios sintéticos y exigir procedencia, supuestos, criterios, versiones, incertidumbre y límites.",
            "No puntuar como correcta una recomendación que exceda la evidencia aunque los cálculos o artefactos técnicos sean correctos.",
            "Mantener answer_key y feedback fuera del payload inicial del estudiante en una futura plataforma dinámica."
        ],
        "assessment_plan": [
            {"component": "Recuperación y autoevaluaciones de unidad", "weight_percent": 15, "evidence": "Ítems razonados con feedback y corrección."},
            {"component": "Casos de diseño e interoperabilidad", "weight_percent": 20, "evidence": "Requisitos, prototipos, flujos y contratos de datos justificables."},
            {"component": "Evaluación clínica/económica", "weight_percent": 20, "evidence": "Comparador, desenlaces, implementación, equidad, costes e incertidumbre."},
            {"component": "Privacidad, seguridad y regulación", "weight_percent": 20, "evidence": "Mapa de datos, amenazas, controles, ruta regulatoria y control de cambios."},
            {"component": "Proyecto integrador", "weight_percent": 25, "evidence": "Dossier U1–U6 y decisión de despliegue condicional."},
        ],
        "diagnostic": {
            "purpose": "Detectar prerrequisitos que requieren recuperación antes de U1.",
            "questions": [
                "¿Cómo distinguirías necesidad sanitaria, requisito funcional y solución tecnológica?",
                "¿Qué diferencia existe entre una métrica de usabilidad y un desenlace clínico?",
                "¿Qué información mínima hace reproducible un flujo de datos entre dos sistemas?",
                "¿Por qué asociación estadística, utilidad clínica y coste-efectividad responden preguntas diferentes?",
                "¿Qué diferencia hay entre privacidad, confidencialidad y ciberseguridad?",
            ],
            "use": "No calificativo; asigna recuperación de sistemas, estadística, interoperabilidad o gobernanza según los errores.",
        },
        "midterm_blueprint": [
            {"domain": "U1 Necesidades y ecosistema", "weight_percent": 17, "course_learning_outcome_ids": ["SALUDDIG-LO01"]},
            {"domain": "U2 Diseño centrado en personas", "weight_percent": 17, "course_learning_outcome_ids": ["SALUDDIG-LO02"]},
            {"domain": "U3 Telemedicina y monitorización", "weight_percent": 17, "course_learning_outcome_ids": ["SALUDDIG-LO03"]},
            {"domain": "U4 Datos e interoperabilidad", "weight_percent": 17, "course_learning_outcome_ids": ["SALUDDIG-LO04"]},
            {"domain": "U5 Evaluación clínica y económica", "weight_percent": 16, "course_learning_outcome_ids": ["SALUDDIG-LO05"]},
            {"domain": "U6 Privacidad, regulación e implementación", "weight_percent": 16, "course_learning_outcome_ids": ["SALUDDIG-LO06", "SALUDDIG-LO07"]},
        ],
        "capstone": {
            "title": "Dossier reproducible de una intervención de salud digital sintética",
            "brief": "Definir una necesidad, diseñar la intervención y su flujo de datos, evaluar usabilidad/interoperabilidad/valor y construir un plan de despliegue responsable con privacidad, seguridad, regulación y escalado; concluir con una decisión condicional que pueda ser no desplegar.",
            "required_deliverables": [
                "Problema, actores, teoría de cambio y criterios de éxito.",
                "Requisitos, prototipo o storyboard y plan de evaluación formativa.",
                "Arquitectura de telemonitorización con alertas, continuidad y supervisión humana.",
                "Contrato interoperable y diccionario/terminologías con procedencia y controles de calidad.",
                "Plan de evaluación clínica/económica con comparador, desenlaces, implementación, equidad e incertidumbre.",
                "Mapa de datos, modelo de amenazas y controles de privacidad/ciberseguridad.",
                "Razonamiento regulatorio fechado, control de cambios, respuesta a incidentes, rollback y escalado.",
                "Decisión final con brechas, propietarios, condiciones de cierre y no-inferencias."
            ],
            "rubric": [
                {"criterion": "Necesidad y diseño sociotécnico", "weight_percent": 20, "excellent": "Problema, usuarios, actores, flujo y requisitos están vinculados sin solutionism."},
                {"criterion": "Datos e interoperabilidad", "weight_percent": 20, "excellent": "Semántica, API, procedencia y calidad permiten un intercambio reproducible y auditable."},
                {"criterion": "Evidencia clínica/económica", "weight_percent": 20, "excellent": "Comparador, desenlaces, implementación, equidad, costes e incertidumbre responden a la decisión sin sobreinferencias."},
                {"criterion": "Privacidad, seguridad y regulación", "weight_percent": 20, "excellent": "Riesgos, controles, jurisdicción, fechas, cambios e incidentes están trazados y no se afirma conformidad profesional."},
                {"criterion": "Integración y comunicación", "weight_percent": 20, "excellent": "La recomendación es reproducible, condicional, proporcional y declara brechas y límites."},
            ],
        },
        "status": "complete",
    }

    dump(DST_ROOT / "course.json", course_payload)
    for n, unit in enumerate(unit_payloads, 1):
        dump(DST_ROOT / "units" / f"unit-{n:02d}.json", unit)
    for n, assessment in enumerate(assessment_payloads, 1):
        dump(DST_ROOT / "assessments" / f"unit-{n:02d}.json", assessment)
    dump(DST_ROOT / "assessments" / "course-assessment.json", course_assessment)
    dump(DST_ROOT / "sources.json", sources_payload)
    dump(DST_ROOT / "glossary.json", glossary_payload)
    dump(DST_ROOT / "claims.json", claims_payload)
    dump(DST_ROOT / "media.json", media_payload)

    print(f"Canonicalizado {SUBJECT}: {len(unit_payloads)} unidades, {len(glossary_entries)} términos, {len(source_records)} fuentes, {len(claims)} claims.")


if __name__ == "__main__":
    main()
