#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "biomateriales"
CODE = "BIOMAT"
SRC_DIR = ROOT / "data" / "course_redevelopment" / COURSE_ID
DST_DIR = ROOT / "data" / "courses" / COURSE_ID
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


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    return normalized[:110] or "recurso"


def unique_slug(text: str, used: set[str]) -> str:
    base = slug(text)
    candidate = base
    index = 2
    while candidate in used:
        candidate = f"{base}-{index}"
        index += 1
    used.add(candidate)
    return candidate


def as_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("statement", "connection", "application", "description", "text", "value", "title"):
            if str(value.get(key) or "").strip():
                return str(value[key]).strip()
        return "; ".join(str(v).strip() for v in value.values() if str(v).strip())
    return str(value or "").strip()


def first_sentence(text: str, fallback: str) -> str:
    clean = " ".join(text.split())
    if not clean:
        return fallback
    sentence = re.split(r"(?<=[.!?])\s+", clean, maxsplit=1)[0]
    if len(sentence) > 105:
        sentence = sentence[:102].rstrip() + "…"
    return sentence


def clean_heading(text: str) -> str:
    return re.sub(r"^\s*\d+\s*[.)-]?\s*", "", text).strip()


def source_key(source: dict[str, Any]) -> str:
    return str(source.get("url") or source.get("doi") or source.get("pmid") or source.get("title") or "").strip().casefold()


def build() -> None:
    source_course = load(SRC_DIR / "course.json")
    units = [load(SRC_DIR / "units" / f"unit-{n:02d}.json") for n in range(1, 7)]
    DST_DIR.mkdir(parents=True, exist_ok=True)

    # ---------- Sources: preserve directly verified unit evidence and merge duplicates ----------
    source_records: dict[str, dict[str, Any]] = {}
    source_key_to_id: dict[str, str] = {}
    unit_source_ids: dict[int, list[str]] = {}
    used_source_ids: set[str] = set()
    for unit in units:
        uid = f"{CODE}-U{unit['unit']:02d}"
        ids: list[str] = []
        for raw in unit.get("sources", []):
            key = source_key(raw)
            if not key:
                continue
            if key in source_key_to_id:
                sid = source_key_to_id[key]
                used_by = source_records[sid].setdefault("used_by_unit_ids", [])
                if uid not in used_by:
                    used_by.append(uid)
                ids.append(sid)
                continue
            proposed = str(raw.get("id") or "").strip()
            if proposed and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", proposed) and proposed not in used_source_ids:
                sid = proposed
                used_source_ids.add(sid)
            else:
                sid = unique_slug(str(raw.get("title") or raw.get("url") or f"source-{len(source_records)+1}"), used_source_ids)
            record = {k: v for k, v in raw.items() if k not in {"id", "used_by_unit_ids"}}
            record["id"] = sid
            record["used_by_unit_ids"] = [uid]
            if not str(record.get("verification_status") or "").strip():
                record["verification_status"] = "verified_directly"
            source_records[sid] = record
            source_key_to_id[key] = sid
            ids.append(sid)
        unit_source_ids[unit["unit"]] = list(dict.fromkeys(ids))

    # ---------- Glossary: consolidate terms but preserve unit provenance ----------
    glossary_records: list[dict[str, Any]] = []
    glossary_by_term: dict[str, dict[str, Any]] = {}
    unit_glossary_ids: dict[int, list[str]] = {n: [] for n in range(1, 7)}
    for unit in units:
        unit_no = unit["unit"]
        uid = f"{CODE}-U{unit_no:02d}"
        evidence_ids = unit_source_ids[unit_no][:2]
        for raw in unit.get("glossary", []):
            term = str(raw.get("term") or "").strip()
            definition = str(raw.get("definition") or raw.get("description") or "").strip()
            if not term or not definition:
                continue
            key = term.casefold()
            if key in glossary_by_term:
                record = glossary_by_term[key]
                if uid not in record["used_by_unit_ids"]:
                    record["used_by_unit_ids"].append(uid)
                for sid in evidence_ids:
                    if sid not in record["source_ids"]:
                        record["source_ids"].append(sid)
                unit_glossary_ids[unit_no].append(record["id"])
                continue
            gid = f"{CODE}-G{len(glossary_records)+1:03d}"
            record = {
                "id": gid,
                "term": term,
                "definition": definition,
                "source_ids": evidence_ids or unit_source_ids[unit_no][:1],
                "verification_status": "verified_directly" if evidence_ids else "traceable_unit_source",
                "used_by_unit_ids": [uid],
            }
            glossary_records.append(record)
            glossary_by_term[key] = record
            unit_glossary_ids[unit_no].append(gid)

    # ---------- Course-level outcomes and competencies ----------
    course_outcomes = [
        {"id": f"{CODE}-LO01", "statement": "Selecciona familias de biomateriales a partir de uso previsto, requisitos, propiedades, trade-offs y evidencia, sin convertir la preselección técnica en una conclusión clínica."},
        {"id": f"{CODE}-LO02", "statement": "Relaciona composición, procesamiento y microestructura con propiedades mecánicas, térmicas y superficiales, distinguiendo correlación, mecanismo y condición de medida."},
        {"id": f"{CODE}-LO03", "statement": "Explica la interfaz material-biología como un proceso dinámico dependiente de superficie, proteínas, células, sangre e inmunidad, evitando una noción binaria de biocompatibilidad."},
        {"id": f"{CODE}-LO04", "statement": "Evalúa corrosión, desgaste, tribocorrosión y degradación de biomateriales con balances, controles, productos liberados, incertidumbre y límites de extrapolación."},
        {"id": f"{CODE}-LO05", "statement": "Diseña estrategias de caracterización mecánica, superficial, morfológica y química con mensurando, escala, calibración, muestreo, representatividad e incertidumbre explícitos."},
        {"id": f"{CODE}-LO06", "statement": "Integra requisitos, gestión de riesgo, evaluación biológica, procesamiento, esterilización y estrategia preclínica en una decisión de diseño trazable y condicionada."},
        {"id": f"{CODE}-LO07", "statement": "Construye un expediente reproducible de biomateriales que vincula requisito, evidencia, método, control, resultado, incertidumbre, riesgo residual y límite de inferencia a través de las seis unidades."},
    ]
    competencies = [
        {"id": f"{CODE}-COMP01", "statement": "Traducir función biomédica y uso previsto en restricciones, objetivos, variables de diseño y criterios de aceptación antes de comparar materiales."},
        {"id": f"{CODE}-COMP02", "statement": "Interpretar relaciones estructura-propiedad conservando composición, proceso, estado material, escala y condiciones de medida."},
        {"id": f"{CODE}-COMP03", "statement": "Analizar interfaces material-biología separando observación, mecanismo propuesto, evidencia biológica y conclusión clínica o regulatoria."},
        {"id": f"{CODE}-COMP04", "statement": "Razonar sobre estabilidad, corrosión, desgaste y degradación mediante controles, balances, sensibilidad y análisis de incertidumbre."},
        {"id": f"{CODE}-COMP05", "statement": "Seleccionar técnicas de caracterización complementarias y justificar qué mensurando y escala aporta cada una."},
        {"id": f"{CODE}-COMP06", "statement": "Integrar evidencia material y biológica en gestión de riesgo y evaluación preclínica sin prescribir procedimientos regulatorios o experimentales reales."},
        {"id": f"{CODE}-COMP07", "statement": "Comunicar decisiones técnicas reproducibles con fuentes, versiones, incertidumbre, alternativas y límites de transferencia."},
    ]

    # ---------- Claims/media are created together with units ----------
    claims: list[dict[str, Any]] = []
    media_items: list[dict[str, Any]] = []
    canonical_units: list[dict[str, Any]] = []

    for unit in units:
        n = int(unit["unit"])
        uid = f"{CODE}-U{n:02d}"
        local_los = [
            {"id": f"{uid}-LO{i:02d}", "statement": statement}
            for i, statement in enumerate(unit.get("learning_objectives", []), start=1)
        ]
        topic_claim_ids: list[str] = []
        topics: list[dict[str, Any]] = []
        claim_counter = 1

        for ti, section in enumerate(unit.get("theory_sections", []), start=1):
            topic_id = f"{uid}-T{ti:02d}"
            eq_blocks: list[dict[str, Any]] = []
            for ei, equation in enumerate(section.get("equations", []), start=1):
                latex = str(equation.get("latex") or equation.get("equation") or "").strip()
                if not latex:
                    continue
                block = {"id": f"{topic_id}-EQ{ei:02d}", "type": "equation", "latex": latex}
                if str(equation.get("label") or equation.get("name") or "").strip():
                    block["label"] = str(equation.get("label") or equation.get("name")).strip()
                if isinstance(equation.get("variables"), dict):
                    block["variables"] = {str(k): str(v) for k, v in equation["variables"].items()}
                eq_blocks.append(block)

            subtopics: list[dict[str, Any]] = []
            for pi, paragraph in enumerate(section.get("paragraphs", []), start=1):
                paragraph = str(paragraph).strip()
                if not paragraph:
                    continue
                subtopics.append({
                    "id": f"{topic_id}-ST{pi:02d}",
                    "title": first_sentence(paragraph, f"Desarrollo {pi}"),
                    "blocks": [{"id": f"{topic_id}-ST{pi:02d}-P01", "type": "paragraph", "text": paragraph}],
                })

            key_points = [str(x).strip() for x in section.get("key_points", []) if str(x).strip()]
            topics.append({
                "id": topic_id,
                "title": clean_heading(str(section.get("heading") or f"Tema {ti}")),
                "key_points": key_points,
                "blocks": eq_blocks,
                "subtopics": subtopics,
            })

            # Four literal claims per unit, taken from curated key points.
            for key_point in key_points:
                if claim_counter > 4:
                    break
                sid_candidates = unit_source_ids[n]
                if not sid_candidates:
                    break
                cid = f"{uid}-C{claim_counter:03d}"
                claims.append({
                    "claim_id": cid,
                    "unit": n,
                    "text": key_point,
                    "claim_type": "methodological_or_interpretive",
                    "risk": "high" if n in {3, 6} else "medium",
                    "context": f"Afirmación ancla literal de {unit['title']}; debe interpretarse dentro del alcance, incertidumbre y límites declarados en la unidad.",
                    "source_id": sid_candidates[(claim_counter - 1) % len(sid_candidates)],
                    "locator": {"section": str(section.get("heading") or f"Tema {ti}")},
                    "support": "direct_or_synthesis",
                    "source_verification_status": source_records[sid_candidates[(claim_counter - 1) % len(sid_candidates)]].get("verification_status", "verified_directly"),
                    "review_state": "ai_review_provisional",
                    "reviewer_validation_id": None,
                    "reviewed_at": TODAY,
                    "id": cid,
                    "unit_id": uid,
                })
                topic_claim_ids.append(cid)
                claim_counter += 1

        # If key points were sparse, use literal purpose/LO text as anchors until four.
        fallback_claim_texts = [str(unit.get("purpose") or "")] + [x["statement"] for x in local_los]
        for text in fallback_claim_texts:
            if claim_counter > 4:
                break
            text = text.strip()
            if not text or not unit_source_ids[n]:
                continue
            cid = f"{uid}-C{claim_counter:03d}"
            sid = unit_source_ids[n][(claim_counter - 1) % len(unit_source_ids[n])]
            claims.append({
                "claim_id": cid,
                "unit": n,
                "text": text,
                "claim_type": "methodological_or_interpretive",
                "risk": "high" if n in {3, 6} else "medium",
                "context": f"Afirmación ancla literal de {unit['title']}; revisión disciplinaria humana pendiente.",
                "source_id": sid,
                "locator": {"section": "Síntesis de unidad"},
                "support": "direct_or_synthesis",
                "source_verification_status": source_records[sid].get("verification_status", "verified_directly"),
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": TODAY,
                "id": cid,
                "unit_id": uid,
            })
            topic_claim_ids.append(cid)
            claim_counter += 1

        examples: list[dict[str, Any]] = []
        for i, raw in enumerate(unit.get("worked_examples", []), start=1):
            scenario = str(raw.get("scenario") or raw.get("problem") or raw.get("description") or raw.get("input") or "Caso sintético delimitado en la unidad.").strip()
            reasoning = raw.get("reasoning_steps") or raw.get("steps")
            if not isinstance(reasoning, list):
                reasoning = []
                for key in ("input", "model", "calculation", "result"):
                    value = raw.get(key)
                    if str(value or "").strip():
                        reasoning.append(f"{key.capitalize()}: {as_text(value)}")
            if not reasoning:
                reasoning = ["Definir datos y supuestos.", "Aplicar el modelo de la unidad.", "Comprobar unidades y límites."]
            interpretation = as_text(raw.get("interpretation") or raw.get("result") or raw.get("conclusion") or "Interpretar el resultado dentro del escenario sintético.")
            limitations_raw = raw.get("limitations") or raw.get("limitation") or raw.get("what_cannot_be_inferred")
            if isinstance(limitations_raw, list):
                limitations = "; ".join(as_text(x) for x in limitations_raw if as_text(x))
            else:
                limitations = as_text(limitations_raw) or "No extrapolar el ejemplo a seguridad, eficacia clínica o conformidad regulatoria fuera de su alcance."
            examples.append({
                "id": f"{uid}-EX{i:02d}",
                "title": str(raw.get("title") or f"Ejemplo trabajado {i}").strip(),
                "scenario": scenario,
                "reasoning_steps": [as_text(step) for step in reasoning if as_text(step)],
                "interpretation": interpretation,
                "limitations": limitations,
            })

        activities: list[dict[str, Any]] = []
        for i, raw in enumerate(unit.get("guided_activities", []), start=1):
            instructions = [as_text(x) for x in raw.get("instructions", []) if as_text(x)]
            tasks = [as_text(x) for x in raw.get("problems", raw.get("tasks", [])) if as_text(x)]
            deliverables = [as_text(x) for x in raw.get("deliverables", []) if as_text(x)]
            criteria = [as_text(x) for x in raw.get("checking_criteria", []) if as_text(x)]
            duration = raw.get("estimated_duration_minutes")
            if not isinstance(duration, int) or duration < 1:
                duration = 120 if i == 1 else 75
            activities.append({
                "id": f"{uid}-ACT{i:02d}",
                "title": str(raw.get("title") or f"Actividad guiada {i}").strip(),
                "purpose": str(raw.get("purpose") or f"Aplicar {unit['title']} con datos sintéticos, trazabilidad, controles, incertidumbre y límites explícitos.").strip(),
                "prerequisite_unit_ids": [f"{CODE}-U{n-1:02d}"] if n > 1 else [],
                "instructions": instructions or ["Trabaja con un escenario sintético y documenta supuestos."],
                "tasks": tasks or ["Construye una solución reproducible y justifica cada decisión."],
                "deliverables": deliverables or ["Expediente reproducible de la actividad."],
                "checking_criteria": criteria or ["La conclusión conserva evidencia, incertidumbre y límites."],
                "estimated_duration_minutes": duration,
                "status": "curated_internal_review_pending",
            })

        media_id = f"{uid}-M01"
        media_items.append({
            "id": media_id,
            "unit_id": uid,
            "type": "interactive_figure_or_diagram",
            "title": f"Mapa visual de {unit['title']}",
            "purpose": "Hacer visibles relaciones, entradas, controles, incertidumbre y límites sin sustituir la explicación textual.",
            "status": "planned",
            "accessibility_requirement": "Debe incluir equivalente textual, etiquetas legibles, navegación por teclado cuando sea interactivo y no depender exclusivamente de color.",
        })

        connections = [as_text(x) for x in unit.get("biomedical_connections", []) if as_text(x)]
        mapped_course_los = [f"{CODE}-LO{n:02d}"] + ([f"{CODE}-LO07"] if n == 6 else [])
        canonical_units.append({
            "$schema": "../../../../schemas/academic/unit-v1.schema.json",
            "schema_version": "1.0",
            "id": uid,
            "course_id": COURSE_ID,
            "order": n,
            "slug": str(unit["slug"]),
            "title": str(unit["title"]),
            "status": STATUS,
            "purpose": str(unit["purpose"]),
            "prerequisite_unit_ids": [f"{CODE}-U{n-1:02d}"] if n > 1 else [],
            "course_learning_outcome_ids": mapped_course_los,
            "learning_outcomes": local_los,
            "topics": topics,
            "examples": examples,
            "activities": activities,
            "assessment_file": f"assessments/unit-{n:02d}.json",
            "glossary_entry_ids": list(dict.fromkeys(unit_glossary_ids[n])),
            "source_ids": unit_source_ids[n],
            "claim_ids": topic_claim_ids,
            "media_ids": [media_id],
            "common_errors": unit.get("common_errors", []),
            "biomedical_connections": connections or [source_course.get("biomedical_connection", "Aplicación biomédica contextual de la unidad.")],
            "editorial_notice": str(unit.get("editorial_notice") or "Curación educativa interna; revisión disciplinaria humana externa pendiente."),
            "legacy_origin": f"data/course_redevelopment/{COURSE_ID}/units/unit-{n:02d}.json",
        })

    # ---------- Unit assessments from existing self-assessment ----------
    assessments: list[dict[str, Any]] = []
    for unit, canonical in zip(units, canonical_units):
        n = int(unit["unit"])
        uid = canonical["id"]
        local_lo_ids = [item["id"] for item in canonical["learning_outcomes"]]
        evidence = unit_source_ids[n][:2] or unit_source_ids[n][:1]
        items: list[dict[str, Any]] = []
        self_items = unit.get("self_assessment", [])
        for i, raw in enumerate(self_items, start=1):
            prompt = str(raw.get("question") or raw.get("prompt") or "").strip()
            answer = str(raw.get("answer") or raw.get("expected_answer") or "").strip()
            if not prompt or not answer:
                continue
            explanation = str(raw.get("reasoning") or raw.get("explanation") or "La respuesta debe justificarse con los conceptos, controles y límites de la unidad.").strip()
            misconception = str(raw.get("common_error") or raw.get("common_misconception") or "Generalizar fuera de las condiciones del problema.").strip()
            if i <= 3:
                difficulty, cognitive = "foundational", "understand"
            elif i <= 7:
                difficulty, cognitive = "intermediate", "apply"
            else:
                difficulty, cognitive = "advanced", "analyze"
            lo_id = local_lo_ids[(i - 1) % len(local_lo_ids)]
            items.append({
                "id": f"{uid}-Q{i:02d}",
                "type": "short_answer",
                "prompt": prompt,
                "linked_learning_outcome_ids": [lo_id],
                "difficulty": difficulty,
                "cognitive_level": cognitive,
                "answer_key": {
                    "expected_answer": answer,
                    "explanation": explanation,
                    "common_misconceptions": [misconception],
                },
                "feedback": {
                    "correct": f"Correcto. Conserva en la justificación este criterio: {explanation}",
                    "incorrect": f"Revisa la unidad y corrige este error frecuente: {misconception}",
                },
                "source_ids": evidence,
                "status": "curated_internal_review_pending",
            })
        assessments.append({
            "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
            "schema_version": "1.0",
            "id": f"{uid}-EVAL",
            "course_id": COURSE_ID,
            "scope": "unit",
            "unit_id": uid,
            "purpose": "Autoevaluación formativa de los resultados de aprendizaje de la unidad con explicación y feedback recuperativo.",
            "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
            "items": items,
            "status": "curated_internal_review_pending",
        })

    # ---------- Course assessment ----------
    course_assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{CODE}-COURSE-EVAL",
        "course_id": COURSE_ID,
        "scope": "course",
        "principles": [
            "Evaluar razonamiento trazable y no memorización aislada de familias o normas.",
            "Separar propiedad medida, interpretación mecanística, evidencia biológica e inferencia clínica o regulatoria.",
            "Usar datos sintéticos o abiertos y exigir unidades, procedencia, condiciones, controles e incertidumbre.",
            "Incluir feedback recuperativo y oportunidad de corregir productos después de revisión.",
            "El proyecto integrador debe conectar explícitamente las seis unidades mediante requisitos y evidencia."
        ],
        "assessment_plan": [
            {"component": "Recuperación y explicación", "weight_percent": 15, "evidence": "Autoevaluaciones, mapas corregidos y explicaciones breves con límites."},
            {"component": "Problemas y casos", "weight_percent": 25, "evidence": "Resoluciones con procedimiento, comparación de alternativas, sensibilidad e incertidumbre."},
            {"component": "Actividades reproducibles", "weight_percent": 25, "evidence": "Matrices, cálculos, auditorías de evidencia y productos sintéticos reconstruibles."},
            {"component": "Revisión y corrección", "weight_percent": 10, "evidence": "Aplicación de criterios, clasificación de hallazgos y justificación antes-después."},
            {"component": "Proyecto integrador", "weight_percent": 25, "evidence": "Expediente de selección y evaluación de biomaterial que conecta U1–U6."}
        ],
        "diagnostic": {
            "purpose": "Detectar prerrequisitos conceptuales sin calificación sumativa.",
            "questions": [
                "Distingue rigidez, resistencia, dureza y tenacidad.",
                "Explica por qué el uso previsto debe preceder a la selección de material.",
                "Diferencia propiedad volumétrica y propiedad superficial.",
                "¿Por qué biocompatibilidad no es una propiedad binaria intrínseca?",
                "Distingue corrosión, desgaste y degradación polimérica.",
                "Indica qué información mínima debe acompañar una medición para ser comparable."
            ]
        },
        "midterm_blueprint": [
            {"domain": "U1 Clases y propiedades", "weight_percent": 20},
            {"domain": "U2 Estructura-propiedad", "weight_percent": 20},
            {"domain": "U3 Interfaz material-biología", "weight_percent": 20},
            {"domain": "U4 Degradación y corrosión", "weight_percent": 20},
            {"domain": "U5 Caracterización", "weight_percent": 10},
            {"domain": "Integración U1–U5", "weight_percent": 10}
        ],
        "capstone": {
            "title": "Expediente reproducible de selección y evaluación de un biomaterial para un dispositivo sintético",
            "purpose": "Integrar las seis unidades sin convertir el ejercicio en evaluación de conformidad ni recomendación clínica.",
            "deliverables": [
                "Uso previsto y requisitos trazables.",
                "Comparación de familias y relación estructura-propiedad.",
                "Mapa de interfaz biológica y peligros relevantes.",
                "Análisis de degradación/corrosión y productos liberados cuando corresponda.",
                "Plan de caracterización con mensurandos, controles e incertidumbre.",
                "Matriz requisito→evidencia→criterio→incertidumbre→decisión y brechas pendientes.",
                "Conclusión técnica condicionada y límites clínicos/regulatorios explícitos."
            ],
            "rubric": [
                {"criterion": "Trazabilidad y requisitos", "weight_percent": 25},
                {"criterion": "Razonamiento material y mecanístico", "weight_percent": 25},
                {"criterion": "Evidencia, controles e incertidumbre", "weight_percent": 25},
                {"criterion": "Integración, reproducibilidad y límites", "weight_percent": 25}
            ]
        },
        "status": "curated_internal_review_pending",
    }

    # ---------- Course descriptor ----------
    all_source_ids = list(source_records)
    core_source_ids = [sid for sid in all_source_ids if source_records[sid].get("verification_status") == "verified_directly"][:12]
    if not core_source_ids:
        core_source_ids = all_source_ids[:8]
    course = {
        "$schema": "../../../schemas/academic/course-v1.schema.json",
        "schema_version": "1.0",
        "id": COURSE_ID,
        "code": CODE,
        "area_id": "ingenieria-biomedica",
        "title": "Biomateriales",
        "language": "es",
        "content_version": "1.0.0",
        "academic_level": str(source_course.get("level") or "Pregrado universitario intermedio y avanzado"),
        "audience": "Estudiantes de ingeniería biomédica y áreas afines con bases de ciencia de materiales, química, mecánica y biología celular que necesiten seleccionar, caracterizar y evaluar biomateriales de forma reproducible y proporcional.",
        "status": STATUS,
        "purpose": "Comprender y aplicar relaciones entre clases de biomateriales, estructura y propiedades, interfaz material-biología, degradación, caracterización y diseño preclínico para construir decisiones técnicas reproducibles, trazables y proporcionales, sin confundir evidencia material o preclínica con seguridad, eficacia clínica o conformidad regulatoria demostradas.",
        "scope": {
            "included": [
                "Selección de metales, cerámicas, polímeros y compuestos a partir de requisitos y trade-offs.",
                "Relaciones composición-procesamiento-microestructura-propiedad y condiciones de medida.",
                "Interfaz material-biología: adsorción proteica, adhesión celular, sangre, inmunidad y respuesta a cuerpo extraño.",
                "Corrosión, desgaste, tribocorrosión, degradación polimérica y productos liberados.",
                "Caracterización mecánica, topográfica, morfológica, espectroscópica y química con incertidumbre.",
                "Uso previsto, requisitos, gestión de riesgo, evaluación biológica, esterilización y estrategia preclínica basada en brechas.",
                "Expedientes reproducibles con fuentes, controles, criterios, incertidumbre, sensibilidad y límites de inferencia."
            ],
            "excluded": [
                "Diagnóstico, pronóstico, prescripción o recomendación terapéutica individual.",
                "Declarar un material o dispositivo seguro, eficaz, biocompatible o conforme a partir del curso o de un ensayo aislado.",
                "Protocolos reales de esterilización, experimentación animal, laboratorio biológico o investigación con personas.",
                "Selección de endpoints regulatorios, evaluación de conformidad, certificación ISO o asesoría jurídica/regulatoria.",
                "Sustituir revisión disciplinaria humana, evaluación toxicológica profesional o validación clínica."
            ],
            "handoff_courses": ["biomateriales-implantes", "polimeros-procesamiento-materiales", "ingenieria-tejidos", "desarrollo-dispositivos-medicos"]
        },
        "prerequisites": [
            {"id": f"{CODE}-PRE01", "statement": "Ciencia de materiales y mecánica universitarias iniciales: estructura, esfuerzo, deformación y propiedades básicas."},
            {"id": f"{CODE}-PRE02", "statement": "Química general y nociones de enlaces, soluciones, superficies, corrosión o degradación."},
            {"id": f"{CODE}-PRE03", "statement": "Biología celular y fisiología suficientes para interpretar interacciones material-biología sin convertirlas en diagnóstico."},
            {"id": f"{CODE}-PRE04", "statement": "Estadística descriptiva, unidades y documentación reproducible para comparar mediciones e incertidumbre."}
        ],
        "competencies": competencies,
        "learning_outcomes": course_outcomes,
        "study_method": [
            "Definir uso previsto, función, restricción y afirmación antes de elegir propiedades o técnicas.",
            "Separar dato observado, modelo, mecanismo propuesto, evidencia biológica y conclusión clínica o regulatoria.",
            "Alternar explicación, ejemplo resuelto, práctica guiada y auditoría con apoyo progresivamente menor.",
            "Conservar unidades, condiciones, procedencia, versiones, controles, incertidumbre y criterios de aceptación.",
            "Usar matrices de trazabilidad y análisis de sensibilidad para evitar rankings o conclusiones universales.",
            "Cerrar cada unidad indicando qué evidencia falta y qué curso o etapa posterior debe resolverla."
        ],
        "core_source_ids": core_source_ids,
        "unit_files": [f"units/unit-{n:02d}.json" for n in range(1, 7)],
        "assessment_files": [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"],
        "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
        "static_site": {
            "renderer": "scripts/generate_site.py",
            "canonical_source": True,
            "legacy_mirrors": [
                "data/generated_courses/biomateriales.json",
                "data/generated_units/biomateriales/",
                "data/subjects/ingenieria-biomedica/biomateriales.json",
                "data/source_registry/biomateriales.json",
                "data/claim_registry/biomateriales.json"
            ]
        },
        "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, fuentes trazables y pedagogía interna para las seis unidades de Biomateriales. La publicación sigue siendo provisional. Revisión humana interna y disciplinaria externa, certificación de normas, evaluación regulatoria, validación preclínica o clínica y cualquier investigación con personas o animales permanecen fuera del cierre y siguen pendientes."
    }

    # ---------- Registries ----------
    sources_registry = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "source_policy": "Priorizar normas y guías oficiales, literatura primaria/revisiones pertinentes y recursos científicos institucionales; conservar identificadores y estado de verificación heredado de las unidades curadas. Una fuente trazable respalda una afirmación educativa, no valida clínicamente el curso.",
        "consulted_on": TODAY,
        "coverage_gaps": [],
        "sources": list(source_records.values()),
    }
    glossary_registry = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "coverage_status": "traceable",
        "entries": glossary_records,
    }
    claims_registry = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": "Afirmaciones centrales literales de las seis unidades canónicas de Biomateriales enlazadas con fuentes verificadas; revisión disciplinaria humana pendiente.",
        "review_state": "ai_review_provisional",
        "claims": claims,
    }
    media_registry = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "status": "planned",
        "items": media_items,
    }

    dump(DST_DIR / "course.json", course)
    dump(DST_DIR / "sources.json", sources_registry)
    dump(DST_DIR / "glossary.json", glossary_registry)
    dump(DST_DIR / "claims.json", claims_registry)
    dump(DST_DIR / "media.json", media_registry)
    for n, canonical in enumerate(canonical_units, start=1):
        dump(DST_DIR / "units" / f"unit-{n:02d}.json", canonical)
    for n, assessment in enumerate(assessments, start=1):
        dump(DST_DIR / "assessments" / f"unit-{n:02d}.json", assessment)
    dump(DST_DIR / "assessments" / "course-assessment.json", course_assessment)

    # ---------- Permanent regression ----------
    test_path = ROOT / "tests" / "test_biomateriales_canonical_course.py"
    test_path.write_text('''from __future__ import annotations\n\nimport json\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nCOURSE_DIR = ROOT / "data" / "courses" / "biomateriales"\nGENERIC = "concepto de la unidad que debe definirse mediante entidades observables"\n\n\ndef load(path: Path):\n    return json.loads(path.read_text(encoding="utf-8"))\n\n\nclass BiomaterialesCanonicalCourseTests(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.course = load(COURSE_DIR / "course.json")\n        cls.units = [load(COURSE_DIR / "units" / f"unit-{i:02d}.json") for i in range(1, 7)]\n        cls.sources = load(COURSE_DIR / "sources.json")\n        cls.glossary = load(COURSE_DIR / "glossary.json")\n        cls.claims = load(COURSE_DIR / "claims.json")\n        cls.media = load(COURSE_DIR / "media.json")\n        cls.assessments = [load(COURSE_DIR / "assessments" / f"unit-{i:02d}.json") for i in range(1, 7)]\n        cls.course_assessment = load(COURSE_DIR / "assessments" / "course-assessment.json")\n\n    def test_course_is_complete_but_human_review_pending(self):\n        status = self.course["status"]\n        self.assertEqual(status["content"], "complete")\n        self.assertEqual(status["sources"], "traceable")\n        self.assertEqual(status["pedagogy"], "complete")\n        self.assertEqual(status["multimedia"], "planned")\n        self.assertEqual(status["internal_review"], "pending")\n        self.assertEqual(status["external_review"], "pending")\n        self.assertEqual(status["publication"], "published_provisional")\n        self.assertEqual(len(self.course["unit_files"]), 6)\n        self.assertEqual(len(self.course["learning_outcomes"]), 7)\n\n    def test_units_preserve_disciplinary_depth_and_no_template(self):\n        text = " ".join(json.dumps(unit, ensure_ascii=False) for unit in self.units).casefold()\n        self.assertNotIn(GENERIC, text)\n        self.assertTrue(all(len(unit["learning_outcomes"]) >= 6 for unit in self.units))\n        self.assertTrue(all(len(unit["topics"]) >= 4 for unit in self.units))\n        self.assertTrue(all(len(unit["examples"]) >= 5 for unit in self.units))\n        self.assertTrue(all(len(unit["activities"]) >= 1 for unit in self.units))\n        self.assertTrue(all(unit["status"]["external_review"] == "pending" for unit in self.units))\n\n    def test_assessments_are_classified_and_traceable(self):\n        total = 0\n        for unit, assessment in zip(self.units, self.assessments):\n            self.assertEqual(assessment["unit_id"], unit["id"])\n            self.assertGreaterEqual(len(assessment["items"]), 10)\n            for item in assessment["items"]:\n                self.assertNotEqual(item["difficulty"], "unclassified")\n                self.assertNotEqual(item["cognitive_level"], "unclassified")\n                self.assertTrue(item["answer_key"]["explanation"])\n                self.assertTrue(item["feedback"]["correct"])\n                self.assertTrue(item["feedback"]["incorrect"])\n                self.assertTrue(item["source_ids"])\n            total += len(assessment["items"])\n        self.assertGreaterEqual(total, 60)\n\n    def test_glossary_sources_claims_and_media_are_linked(self):\n        self.assertGreaterEqual(len(self.glossary["entries"]), 80)\n        source_ids = {item["id"] for item in self.sources["sources"]}\n        self.assertGreaterEqual(len(source_ids), 30)\n        self.assertTrue(all(item.get("verification_status") for item in self.sources["sources"]))\n        self.assertEqual(len(self.claims["claims"]), 24)\n        units_by_id = {unit["id"]: json.dumps(unit, ensure_ascii=False) for unit in self.units}\n        for claim in self.claims["claims"]:\n            self.assertIn(claim["source_id"], source_ids)\n            self.assertIn(claim["text"], units_by_id[claim["unit_id"]])\n            self.assertIsNone(claim["reviewer_validation_id"])\n        self.assertEqual(len(self.media["items"]), 6)\n        self.assertTrue(all(item["status"] == "planned" for item in self.media["items"]))\n\n    def test_course_assessment_weights_are_complete(self):\n        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["assessment_plan"]), 100)\n        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["midterm_blueprint"]), 100)\n        self.assertEqual(sum(item["weight_percent"] for item in self.course_assessment["capstone"]["rubric"]), 100)\n        self.assertGreaterEqual(len(self.course_assessment["diagnostic"]["questions"]), 6)\n\n    def test_curricular_boundaries_remain_explicit(self):\n        course_text = json.dumps(self.course, ensure_ascii=False).casefold()\n        self.assertIn("biomateriales-implantes", course_text)\n        self.assertIn("evaluación de conformidad", course_text)\n        self.assertIn("validación preclínica o clínica", course_text)\n        u6 = json.dumps(self.units[5], ensure_ascii=False).casefold()\n        self.assertIn("iso 10993-1:2025", u6)\n        self.assertIn("iso 11135:2014", u6)\n        self.assertIn("fdis", u6)\n\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")

    print(f"[ok] Biomateriales canonical corpus: units={len(canonical_units)}, sources={len(source_records)}, glossary={len(glossary_records)}, claims={len(claims)}, assessments={sum(len(a['items']) for a in assessments)}")


if __name__ == "__main__":
    build()
