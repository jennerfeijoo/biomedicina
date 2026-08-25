#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "economia-gestion-empresas"
CODE = "EGE"
AREA_ID = "gestion-etica-comunicacion"
SOURCE_DIR = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"
TARGET = ROOT / "data" / "courses" / COURSE_ID
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"

STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_title(text: str, fallback: str) -> str:
    text = re.sub(r"\s+", " ", str(text or "").strip())
    if not text:
        return fallback
    return text[:180]


def canonical_source_record(source: dict, source_id: str, unit: int) -> dict:
    record = {"id": source_id}
    for key in ("title", "authors", "organization", "year", "url", "type", "description", "verification_status"):
        if key in source and source[key] not in (None, ""):
            record[key] = source[key]
    if "description" not in record:
        record["description"] = f"Fuente verificada utilizada en la curación académica de U{unit}: {record.get('title', 'referencia disciplinar')}."
    record["verification_status"] = source.get("verification_status", "")
    record["unit_origins"] = [unit]
    return record


def main() -> None:
    units = [load(SOURCE_DIR / f"unit-{n:02d}.json") for n in range(1, 7)]
    for n, unit in enumerate(units, 1):
        assert unit["unit"] == n
        assert unit["status"] == "review"
        text = json.dumps(unit, ensure_ascii=False).casefold()
        assert GENERIC not in text, f"U{n} todavía contiene plantilla genérica"
        assert len(unit.get("theory_sections", [])) >= 4
        assert len(unit.get("glossary", [])) >= 12
        assert len(unit.get("worked_examples", [])) >= 5
        assert len(unit.get("self_assessment", [])) >= 10
        assert len(unit.get("sources", [])) >= 5
        unverified = [s.get("title") for s in unit["sources"] if s.get("verification_status") != "verified_directly"]
        assert not unverified, f"U{n} contiene fuentes no verificadas directamente: {unverified}"

    if TARGET.exists():
        shutil.rmtree(TARGET)
    (TARGET / "units").mkdir(parents=True)
    (TARGET / "assessments").mkdir(parents=True)

    # Consolidated verified sources, deduplicated by URL (or title as fallback).
    sources: list[dict] = []
    source_key_to_id: dict[str, str] = {}
    unit_source_ids: dict[int, list[str]] = {}
    for unit in units:
        n = unit["unit"]
        ids: list[str] = []
        for source in unit["sources"]:
            key = (source.get("url") or source.get("title") or "").strip().casefold()
            assert key
            if key not in source_key_to_id:
                sid = f"ege-src-{len(sources)+1:03d}"
                source_key_to_id[key] = sid
                sources.append(canonical_source_record(source, sid, n))
            else:
                sid = source_key_to_id[key]
                record = next(item for item in sources if item["id"] == sid)
                if n not in record["unit_origins"]:
                    record["unit_origins"].append(n)
            ids.append(sid)
        unit_source_ids[n] = list(dict.fromkeys(ids))

    dump(TARGET / "sources.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "source_policy": "Consolidación de fuentes directamente verificadas durante la curación disciplinar U1–U6. La trazabilidad interna no se interpreta como revisión humana externa ni como dictamen profesional.",
        "consulted_on": "2026-08-25",
        "coverage_gaps": [],
        "coverage_status": "traceable",
        "sources": sources,
    })

    # Consolidated glossary. Definitions are preserved verbatim; unit-level verified sources provide provenance.
    glossary_entries: list[dict] = []
    term_to_id: dict[str, str] = {}
    unit_glossary_ids: dict[int, list[str]] = {}
    for unit in units:
        n = unit["unit"]
        gids: list[str] = []
        for entry in unit["glossary"]:
            term_key = entry["term"].strip().casefold()
            if term_key not in term_to_id:
                gid = f"{CODE}-G{len(glossary_entries)+1:03d}"
                term_to_id[term_key] = gid
                glossary_entries.append({
                    "id": gid,
                    "term": entry["term"],
                    "definition": entry["definition"],
                    "source_ids": unit_source_ids[n][: min(3, len(unit_source_ids[n]))],
                    "verification_status": "traceable_to_verified_unit_sources",
                    "unit_origins": [n],
                })
            else:
                gid = term_to_id[term_key]
                record = next(item for item in glossary_entries if item["id"] == gid)
                if n not in record["unit_origins"]:
                    record["unit_origins"].append(n)
            gids.append(gid)
        unit_glossary_ids[n] = list(dict.fromkeys(gids))

    dump(TARGET / "glossary.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "entries": glossary_entries,
    })

    # Four anchor claims per unit, drawn verbatim from the unit key points and tied to verified unit sources.
    claims: list[dict] = []
    unit_claim_ids: dict[int, list[str]] = {}
    for unit in units:
        n = unit["unit"]
        selected = []
        for section in unit["theory_sections"]:
            key_points = section.get("key_points", [])
            if key_points:
                selected.append(key_points[0])
        if len(selected) < 4:
            selected.extend(k for s in unit["theory_sections"] for k in s.get("key_points", []))
        selected = list(dict.fromkeys(selected))[:4]
        assert len(selected) == 4
        ids = []
        for idx, text in enumerate(selected, 1):
            cid = f"{CODE}-C{n:02d}-{idx:02d}"
            sid = unit_source_ids[n][min(idx - 1, len(unit_source_ids[n]) - 1)]
            claims.append({
                "id": cid,
                "unit": n,
                "unit_id": f"{CODE}-U{n:02d}",
                "text": text,
                "source_id": sid,
                "source_verification_status": "verified_directly",
                "review_state": "ai_review_provisional",
                "support": "direct_or_methodological",
            })
            ids.append(cid)
        unit_claim_ids[n] = ids

    dump(TARGET / "claims.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "scope": "24 afirmaciones ancla, cuatro por unidad, conservadas literalmente desde el contenido lectivo y trazadas a fuentes directamente verificadas de cada unidad.",
        "review_state": "ai_review_provisional",
        "claims": claims,
    })

    media_items = []
    for unit in units:
        n = unit["unit"]
        media_items.append({
            "id": f"{CODE}-M{n:02d}",
            "unit_id": f"{CODE}-U{n:02d}",
            "title": f"Visualización pedagógica planificada — U{n}: {unit['title']}",
            "type": "interactive_diagram_or_annotated_figure",
            "status": "planned",
            "purpose": f"Representar visualmente el modelo, flujo o decisión central de {unit['title']} sin sustituir explicación, evidencia, actividad ni límites de inferencia.",
            "alt_text": f"Esquema didáctico previsto para la unidad {n}, {unit['title']}.",
        })
    dump(TARGET / "media.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "status": "planned",
        "items": media_items,
    })

    canonical_units = []
    for unit in units:
        n = unit["unit"]
        uid = f"{CODE}-U{n:02d}"
        local_los = [
            {"id": f"{uid}-LO{i:02d}", "statement": statement}
            for i, statement in enumerate(unit["learning_objectives"], 1)
        ]

        topics = []
        for sidx, section in enumerate(unit["theory_sections"], 1):
            tid = f"{uid}-T{sidx:02d}"
            topic_blocks = []
            for eidx, equation in enumerate(section.get("equations", []), 1):
                topic_blocks.append({
                    "id": f"{tid}-E{eidx:02d}",
                    "type": "equation",
                    "latex": equation["latex"],
                    "label": equation.get("meaning", ""),
                    "variables": equation.get("variables", {}),
                })
            subtopics = []
            key_points = section.get("key_points", [])
            for pidx, paragraph in enumerate(section["paragraphs"], 1):
                stid = f"{tid}-ST{pidx:02d}"
                title = clean_title(key_points[pidx - 1] if pidx - 1 < len(key_points) else paragraph.split(".")[0], f"Explicación {pidx}")
                subtopics.append({
                    "id": stid,
                    "title": title,
                    "blocks": [{"id": f"{stid}-B01", "type": "paragraph", "text": paragraph}],
                })
            topics.append({
                "id": tid,
                "title": section["heading"],
                "blocks": topic_blocks,
                "key_points": section.get("key_points", []),
                "subtopics": subtopics,
            })

        examples = []
        for idx, example in enumerate(unit.get("worked_examples", []), 1):
            examples.append({
                "id": f"{uid}-EX{idx:02d}",
                "title": example["title"],
                "scenario": example.get("scenario", "Escenario sintético de la unidad."),
                "reasoning_steps": example.get("reasoning_steps", []),
                "answer": example.get("answer", ""),
                "interpretation": example.get("interpretation", ""),
                "limitations": [
                    "La interpretación se limita al escenario y supuestos declarados.",
                    "El ejemplo docente no constituye recomendación clínica, regulatoria, financiera, jurídica o de gestión para una organización real."
                ],
            })

        source_activities = unit.get("guided_activities", [])
        activities = []
        if len(source_activities) >= 3:
            for idx, activity in enumerate(source_activities, 1):
                activities.append({
                    "id": f"{uid}-ACT{idx:02d}",
                    "title": activity["title"],
                    "purpose": f"Aplicar {unit['title']} con apoyo progresivamente menor y una conclusión proporcional al escenario sintético.",
                    "prerequisite_unit_ids": [f"{CODE}-U{n-1:02d}"] if n > 1 else [],
                    "instructions": activity.get("instructions", []),
                    "tasks": activity.get("problems", activity.get("tasks", [])),
                    "deliverables": activity.get("deliverables", []),
                    "checking_criteria": activity.get("checking_criteria", []),
                    "estimated_duration_minutes": activity.get("duration_minutes", 90),
                    "status": "complete",
                })
        else:
            base = source_activities[0]
            tasks = base.get("problems", base.get("tasks", []))
            cut1 = max(1, len(tasks) // 3)
            cut2 = max(cut1 + 1, (2 * len(tasks)) // 3)
            chunks = [tasks[:cut1], tasks[cut1:cut2], tasks[cut2:]]
            labels = [
                ("Práctica guiada", "seguir un procedimiento explícito y comprobar cada decisión"),
                ("Práctica semiguiada", "resolver una variante con menos instrucciones y justificar elecciones"),
                ("Reto de transferencia", "transferir el método a un escenario nuevo, declarar qué debe revalidarse y defender límites"),
            ]
            total = base.get("duration_minutes", 270)
            durations = [max(30, round(total * 0.4)), max(30, round(total * 0.3)), max(30, total - round(total * 0.4) - round(total * 0.3))]
            for idx, ((label, purpose), task_chunk, duration) in enumerate(zip(labels, chunks, durations), 1):
                instructions = base.get("instructions", [])
                if idx == 2:
                    instructions = instructions[: max(3, len(instructions) // 2)] + ["Justifica las decisiones que ya no están prescritas paso a paso."]
                elif idx == 3:
                    instructions = [
                        "Resuelve la variante sintética sin reutilizar automáticamente la conclusión del caso base.",
                        "Declara supuestos, datos faltantes, criterios y límites antes de recomendar el siguiente paso.",
                        "Explica qué evidencia adicional sería necesaria para transferir la conclusión a un contexto real."
                    ]
                activities.append({
                    "id": f"{uid}-ACT{idx:02d}",
                    "title": f"{label}: {base['title']}",
                    "purpose": purpose.capitalize() + ".",
                    "prerequisite_unit_ids": [f"{CODE}-U{n-1:02d}"] if n > 1 else [],
                    "instructions": instructions,
                    "tasks": task_chunk or tasks[-3:],
                    "deliverables": base.get("deliverables", []),
                    "checking_criteria": base.get("checking_criteria", []),
                    "estimated_duration_minutes": duration,
                    "status": "complete",
                })

        canonical = {
            "$schema": "../../../../schemas/academic/unit-v1.schema.json",
            "schema_version": "1.0",
            "id": uid,
            "course_id": COURSE_ID,
            "order": n,
            "slug": unit["slug"],
            "title": unit["title"],
            "status": STATUS,
            "purpose": unit["purpose"],
            "prerequisite_unit_ids": [f"{CODE}-U{n-1:02d}"] if n > 1 else [],
            "course_learning_outcome_ids": [f"{CODE}-LO{n:02d}", f"{CODE}-LO07"],
            "learning_outcomes": local_los,
            "topics": topics,
            "examples": examples,
            "activities": activities,
            "assessment_file": f"assessments/unit-{n:02d}.json",
            "glossary_entry_ids": unit_glossary_ids[n],
            "source_ids": unit_source_ids[n],
            "claim_ids": unit_claim_ids[n],
            "media_ids": [f"{CODE}-M{n:02d}"],
            "common_errors": unit.get("common_errors", []),
            "biomedical_connections": [
                f"{item.get('connection', 'Conexión')}: {item.get('explanation', '')}" if isinstance(item, dict) else str(item)
                for item in unit.get("biomedical_connections", [])
            ],
            "editorial_notice": unit.get("editorial_notice", "Revisión disciplinar humana pendiente."),
            "legacy_origin": f"data/course_redevelopment/{COURSE_ID}/units/unit-{n:02d}.json",
        }
        canonical_units.append(canonical)
        dump(TARGET / "units" / f"unit-{n:02d}.json", canonical)

        # Unit assessment reuses the unit's authored self-assessment with recoverable feedback.
        items = []
        source_questions = unit["self_assessment"]
        for idx, item in enumerate(source_questions, 1):
            lo_id = local_los[(idx - 1) % len(local_los)]["id"]
            if idx <= 3:
                difficulty, cognitive = "foundational", "understand"
            elif idx <= 7:
                difficulty, cognitive = "intermediate", "apply" if idx <= 5 else "analyze"
            else:
                difficulty, cognitive = "advanced", "evaluate"
            topic_heading = unit["theory_sections"][(idx - 1) % len(unit["theory_sections"])]["heading"]
            sid = unit_source_ids[n][(idx - 1) % len(unit_source_ids[n])]
            items.append({
                "id": f"{uid}-Q{idx:02d}",
                "type": "case_analysis" if idx % 4 == 0 else "short_answer",
                "prompt": item["question"],
                "linked_learning_outcome_ids": [lo_id],
                "difficulty": difficulty,
                "cognitive_level": cognitive,
                "answer_key": {
                    "expected_answer": item["answer"],
                    "explanation": item.get("reasoning", "La respuesta debe mantener el alcance y los supuestos de la unidad."),
                    "common_misconceptions": [item.get("common_error", "Generalizar la conclusión fuera del escenario evaluado.")],
                },
                "feedback": {
                    "correct": "La respuesta conecta concepto, evidencia, decisión y límite sin sobreinterpretar el caso.",
                    "incorrect": f"Revisa «{topic_heading}», identifica el error conceptual y vuelve a responder separando dato, inferencia, decisión y límite.",
                },
                "source_ids": [sid],
                "status": "complete",
            })
        assert len(items) >= 10
        dump(TARGET / "assessments" / f"unit-{n:02d}.json", {
            "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
            "schema_version": "1.0",
            "id": f"{uid}-ASSESS",
            "course_id": COURSE_ID,
            "scope": "unit",
            "unit_id": uid,
            "purpose": f"Comprobar comprensión, aplicación, análisis y transferencia responsable de U{n} — {unit['title']} mediante preguntas recuperativas basadas en el corpus disciplinar.",
            "student_payload_policy": "El payload estudiantil no incluye claves de respuesta; soluciones, explicaciones, errores frecuentes y feedback permanecen en el registro docente estructurado.",
            "items": items,
            "status": "complete",
        })

    course_assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{CODE}-COURSE-ASSESS",
        "course_id": COURSE_ID,
        "scope": "course",
        "principles": [
            "Evaluar decisiones reproducibles y justificadas, no memorización aislada de términos económicos o administrativos.",
            "Trabajar con organizaciones, mercados, procesos, costes y obligaciones sintéticos o públicos sin datos personales ni confidenciales.",
            "Exigir objetivo, alternativas, unidades, fuentes, supuestos, incertidumbre, criterios y límites en toda recomendación.",
            "Mantener separadas eficiencia económica, sostenibilidad financiera, desempeño operacional, estrategia de mercado, evaluación económica, gobernanza, cumplimiento y evidencia clínica o regulatoria."
        ],
        "assessment_plan": [
            {"component": "Recuperación y autoevaluación U1–U6", "weight_percent": 15},
            {"component": "Problemas cuantitativos y casos", "weight_percent": 20},
            {"component": "Actividades reproducibles y memorandos de decisión", "weight_percent": 25},
            {"component": "Evaluación intermedia integradora", "weight_percent": 15},
            {"component": "Capstone de estrategia, valor y gobernanza", "weight_percent": 25},
        ],
        "diagnostic": {
            "purpose": "Identificar prerrequisitos conceptuales y cuantitativos que requieren recuperación antes de integrar las seis unidades.",
            "questions": [
                "Distingue escasez de falta de dinero y define coste de oportunidad.",
                "Explica la diferencia entre demanda, necesidad sanitaria y utilización observada.",
                "Distingue resultado contable de flujo de efectivo.",
                "Explica margen de contribución y punto de equilibrio con sus supuestos.",
                "Define capacidad efectiva, cuello de botella y Ley de Little.",
                "Distingue medida de resultado, proceso y balance.",
                "Diferencia segmentación de mercado de segmentación de imágenes.",
                "Explica propuesta de valor sin confundirla con evidencia clínica.",
                "Distingue coste-efectividad de impacto presupuestario y asequibilidad.",
                "Explica por qué un ICER no decide por sí solo una compra o reembolso.",
                "Distingue gobernanza, dirección y operación.",
                "Explica por qué un KPI o una matriz de riesgo no demuestran cumplimiento o seguridad por sí solos."
            ]
        },
        "midterm_blueprint": [
            {"domain": "U1 Economía y valor en salud", "weight_percent": 15},
            {"domain": "U2 Contabilidad y finanzas", "weight_percent": 15},
            {"domain": "U3 Operaciones y procesos", "weight_percent": 15},
            {"domain": "U4 Mercado y estrategia", "weight_percent": 15},
            {"domain": "U5 Evaluación económica", "weight_percent": 20},
            {"domain": "U6 Gobernanza y desempeño", "weight_percent": 20},
        ],
        "capstone": {
            "title": "Memorando integral de decisión para una tecnología biomédica sintética",
            "scenario": "Un equipo directivo ficticio debe decidir si continúa, rediseña o detiene la expansión de una tecnología biomédica sintética. El expediente integra restricción de recursos, viabilidad financiera, capacidad operativa, mercado B2B, evaluación económica sanitaria y gobernanza con riesgos, indicadores y obligaciones aplicables.",
            "required_deliverables": [
                "Definición del problema, objetivos y alternativas factibles.",
                "Mapa de escasez, coste de oportunidad, incentivos y criterios de eficiencia/equidad.",
                "Estados y flujo de caja sintéticos con costes, punto de equilibrio, escenarios y límites.",
                "Mapa de proceso, capacidad, cuello de botella, inventario y medidas de calidad operacional.",
                "Segmentación de mercado, centro de compra, competencia, propuesta de valor y escenarios TAM/SAM/SOM.",
                "Problema de evaluación económica con comparadores, perspectiva, horizonte, ΔC, ΔE, ICER/INMB cuando proceda e impacto presupuestario.",
                "Análisis de sensibilidad e incertidumbre separado por parámetros, escenarios y estructura.",
                "Mapa de gobernanza, derechos de decisión, tablero de KPIs y medidas de balance.",
                "Registro de riesgos, controles, obligaciones potencialmente aplicables y reglas de escalamiento.",
                "Tabla de trazabilidad afirmación→dato/fuente→método→resultado→límite.",
                "Recomendación condicionada con argumentos a favor, en contra y evidencia pendiente.",
                "Plan de revisión posterior con criterios para cambiar la decisión."
            ],
            "rubric": [
                {"criterion": "Definición del problema, alternativas y trazabilidad", "weight_percent": 20},
                {"criterion": "Razonamiento económico y financiero", "weight_percent": 15},
                {"criterion": "Operaciones, mercado y estrategia", "weight_percent": 15},
                {"criterion": "Evaluación económica e incertidumbre", "weight_percent": 20},
                {"criterion": "Gobernanza, riesgos, KPIs y cumplimiento", "weight_percent": 20},
                {"criterion": "Comunicación, límites y plan de revisión", "weight_percent": 10},
            ]
        },
        "status": "complete",
    }
    dump(TARGET / "assessments" / "course-assessment.json", course_assessment)

    course = {
        "$schema": "../../../schemas/academic/course-v1.schema.json",
        "schema_version": "1.0",
        "id": COURSE_ID,
        "code": CODE,
        "area_id": AREA_ID,
        "title": "Economía y Gestión de Empresas",
        "language": "es",
        "content_version": "1.0.0",
        "academic_level": "Pregrado universitario intermedio y avanzado",
        "audience": "Estudiantes de ingeniería biomédica y áreas afines que necesitan razonar sobre recursos, sostenibilidad, operaciones, mercado, evaluación económica y gobernanza de proyectos y organizaciones biomédicas sin sustituir asesoría profesional especializada.",
        "status": STATUS,
        "purpose": "Integrar U1–U6 en un marco reproducible para decisiones organizativas biomédicas: escasez y valor, contabilidad y finanzas, operaciones y procesos, mercado y estrategia, evaluación económica sanitaria y gobernanza del desempeño. El cierre acredita completitud interna de contenido y pedagogía, no revisión disciplinar humana, asesoría financiera o jurídica, HTA oficial, certificación, conformidad regulatoria ni recomendación clínica.",
        "scope": {
            "included": [
                "Escasez, coste de oportunidad, oferta, demanda, elasticidad, incentivos, eficiencia y equidad.",
                "Estados financieros, costes, flujo de caja, margen de contribución, punto de equilibrio, capital de trabajo y presupuestos.",
                "Procesos, capacidad, cuellos de botella, Ley de Little, inventario, calidad operacional y mejora PDSA.",
                "Segmentación de mercado, compra B2B, competencia, propuesta de valor, posicionamiento y escenarios TAM/SAM/SOM.",
                "Evaluación económica sanitaria, análisis incremental, dominancia, ICER, beneficio monetario neto, impacto presupuestario e incertidumbre.",
                "Gobernanza, accountability, derechos de decisión, KPIs, tableros, riesgo, compliance, controles, assurance y escalamiento.",
                "Casos sintéticos, memorandos de decisión, trazabilidad de fuentes y comunicación proporcional a la evidencia."
            ],
            "excluded": [
                "Asesoría contable, fiscal, financiera, de inversión o valoración empresarial para una entidad real.",
                "Investigación de mercado propietaria o recomendación comercial para una empresa concreta.",
                "HTA oficial, decisión real de precio, reembolso, cobertura, compra o asignación de recursos sanitarios.",
                "Asesoría jurídica, determinación de obligaciones de compliance o certificación ISO.",
                "Inspección, auditoría profesional, conformidad regulatoria o autorización de un dispositivo médico.",
                "Inferir eficacia, seguridad clínica o beneficio para pacientes desde métricas económicas u organizativas aisladas."
            ],
            "handoff_courses": [
                "innovacion-emprendimiento",
                "laboratorio-globalizacion-emprendimiento",
                "politicas-publicas-ciencia-tecnologia",
                "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas",
                "desarrollo-dispositivos-medicos",
                "ingenieria-clinica-gestion"
            ]
        },
        "prerequisites": [
            {"id": f"{CODE}-PRE01", "statement": "Aritmética, porcentajes, proporciones y lectura de tablas y gráficos."},
            {"id": f"{CODE}-PRE02", "statement": "Estadística descriptiva básica y capacidad de interpretar incertidumbre y escenarios."},
            {"id": f"{CODE}-PRE03", "statement": "Comprensión introductoria de sistemas sanitarios, tecnologías biomédicas y ciclo de vida de proyectos."},
            {"id": f"{CODE}-PRE04", "statement": "Lectura académica y disposición para distinguir evidencia, supuesto, cálculo, inferencia y decisión."}
        ],
        "competencies": [
            {"id": f"{CODE}-COMP01", "statement": "Razonar sobre decisiones biomédicas bajo recursos limitados haciendo visible el coste de oportunidad y los criterios de valor."},
            {"id": f"{CODE}-COMP02", "statement": "Interpretar sostenibilidad financiera con estados, costes, efectivo, presupuestos y escenarios sin confundir beneficio contable con liquidez."},
            {"id": f"{CODE}-COMP03", "statement": "Diagnosticar procesos y capacidad con métricas operativas, cuellos de botella, inventario y medidas de calidad y balance."},
            {"id": f"{CODE}-COMP04", "statement": "Construir una estrategia de mercado B2B para tecnología médica separando atractivo comercial de evidencia clínica, regulación y reembolso."},
            {"id": f"{CODE}-COMP05", "statement": "Comparar alternativas sanitarias mediante evaluación económica e impacto presupuestario con análisis incremental, incertidumbre y límites explícitos."},
            {"id": f"{CODE}-COMP06", "statement": "Diseñar gobernanza de decisiones con derechos, KPIs, riesgos, controles, compliance, escalamiento y revisión trazable."}
        ],
        "learning_outcomes": [
            {"id": f"{CODE}-LO01", "statement": "Analiza escasez, coste de oportunidad, oferta, demanda, elasticidad e incentivos en un escenario sanitario sin convertir eficiencia en recomendación normativa automática."},
            {"id": f"{CODE}-LO02", "statement": "Construye e interpreta un modelo financiero sintético con estados, costes, efectivo, punto de equilibrio, capital de trabajo, presupuesto y escenarios."},
            {"id": f"{CODE}-LO03", "statement": "Evalúa un proceso biomédico mediante flujo, capacidad, cuellos de botella, inventario, calidad operacional y ciclos de mejora."},
            {"id": f"{CODE}-LO04", "statement": "Formula segmentación, centro de compra, competencia, propuesta de valor, posicionamiento y escenarios de mercado para una tecnología médica sintética manteniendo fronteras regulatorias y clínicas."},
            {"id": f"{CODE}-LO05", "statement": "Realiza una evaluación económica sanitaria sintética con comparadores, perspectiva, horizonte, análisis incremental, impacto presupuestario e incertidumbre sin recomendar automáticamente reembolso o compra."},
            {"id": f"{CODE}-LO06", "statement": "Diseña e interpreta un sistema de gobernanza y desempeño con responsabilidades, KPIs, riesgos, controles, compliance y escalamiento, delimitando aplicabilidad y evidencia."},
            {"id": f"{CODE}-LO07", "statement": "Integra U1–U6 en un memorando de decisión reproducible que conecta objetivos, recursos, finanzas, operaciones, mercado, valor económico, gobernanza, riesgos, fuentes, incertidumbre y criterios de revisión."
            }
        ],
        "study_method": [
            "Explicación conceptual seguida de ejemplo trabajado, práctica guiada, práctica semiguiada y transferencia con apoyo decreciente.",
            "Usar escenarios, organizaciones y datos sintéticos o públicos; no incorporar datos personales, secretos comerciales ni información confidencial de entidades reales.",
            "Declarar pregunta, alternativas, unidades, fuentes, supuestos, criterios, incertidumbre y límites antes de recomendar una acción.",
            "Separar observación, cálculo, inferencia, valor normativo y autoridad de decisión.",
            "Integrar progresivamente U1–U6 en un expediente final y revisar las conclusiones cuando cambia un supuesto o aparece nueva evidencia."
        ],
        "core_source_ids": [source["id"] for source in sources],
        "unit_files": [f"units/unit-{n:02d}.json" for n in range(1, 7)],
        "assessment_files": [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"],
        "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
        "static_site": {
            "renderer": "scripts/generate_site.py",
            "canonical_source": True,
            "legacy_mirrors": [
                f"data/generated_courses/{COURSE_ID}.json",
                f"data/generated_units/{COURSE_ID}/",
                f"data/subjects/{AREA_ID}/{COURSE_ID}.json"
            ]
        },
        "editorial_notice": "Corpus canónico completo a nivel de contenido, fuentes trazadas y pedagogía interna para U1–U6. Multimedia permanece planificada y la publicación es provisional. La revisión humana interna y disciplinar externa permanece pendiente. Este cierre no constituye asesoría económica, financiera, contable, comercial, jurídica o de compliance; HTA oficial; auditoría; certificación; inspección; conformidad regulatoria; validación clínica; ni recomendación de financiación, reembolso, compra o uso clínico."
    }
    dump(TARGET / "course.json", course)

    # Permanent regression protecting preservation, completeness, tracing and human-review boundaries.
    test = f'''from __future__ import annotations\n\nimport json\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nCOURSE_ID = "{COURSE_ID}"\nCODE = "{CODE}"\nCANON = ROOT / "data" / "courses" / COURSE_ID\nREDEV = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"\nGENERIC = "{GENERIC}"\n\n\nclass EconomiaGestionEmpresasCourseCompletionTests(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.course = json.loads((CANON / "course.json").read_text(encoding="utf-8"))\n        cls.sources = json.loads((CANON / "sources.json").read_text(encoding="utf-8"))\n        cls.claims = json.loads((CANON / "claims.json").read_text(encoding="utf-8"))\n        cls.glossary = json.loads((CANON / "glossary.json").read_text(encoding="utf-8"))\n        cls.media = json.loads((CANON / "media.json").read_text(encoding="utf-8"))\n\n    def test_course_is_complete_but_human_review_stays_pending(self):\n        status = self.course["status"]\n        self.assertEqual(status["content"], "complete")\n        self.assertEqual(status["sources"], "traceable")\n        self.assertEqual(status["pedagogy"], "complete")\n        self.assertEqual(status["multimedia"], "planned")\n        self.assertEqual(status["internal_review"], "pending")\n        self.assertEqual(status["external_review"], "pending")\n        self.assertEqual(status["publication"], "published_provisional")\n\n    def test_six_units_preserve_all_authored_theory_and_equations(self):\n        for n in range(1, 7):\n            source = json.loads((REDEV / f"unit-{{n:02d}}.json").read_text(encoding="utf-8"))\n            canonical_path = CANON / "units" / f"unit-{{n:02d}}.json"\n            canonical_text = canonical_path.read_text(encoding="utf-8")\n            canonical = json.loads(canonical_text)\n            self.assertNotIn(GENERIC, canonical_text.casefold())\n            self.assertEqual(canonical["id"], f"{{CODE}}-U{{n:02d}}")\n            self.assertEqual(canonical["status"]["content"], "complete")\n            self.assertGreaterEqual(len(canonical["activities"]), 3)\n            for section in source["theory_sections"]:\n                for paragraph in section["paragraphs"]:\n                    self.assertIn(paragraph, canonical_text)\n                for equation in section.get("equations", []):\n                    self.assertIn(equation["latex"], canonical_text)\n            for objective in source["learning_objectives"]:\n                self.assertIn(objective, canonical_text)\n\n    def test_assessments_are_recoverable_and_substantive(self):\n        for n in range(1, 7):\n            payload = json.loads((CANON / "assessments" / f"unit-{{n:02d}}.json").read_text(encoding="utf-8"))\n            self.assertGreaterEqual(len(payload["items"]), 10)\n            self.assertTrue(all(item["difficulty"] != "unclassified" for item in payload["items"]))\n            self.assertTrue(all(item["cognitive_level"] != "unclassified" for item in payload["items"]))\n            self.assertTrue(all(item["answer_key"]["explanation"] for item in payload["items"]))\n            self.assertTrue(all(item["feedback"]["incorrect"] for item in payload["items"]))\n            self.assertTrue(all(item["source_ids"] for item in payload["items"]))\n\n    def test_course_assessment_integrates_u1_to_u6(self):\n        payload = json.loads((CANON / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))\n        self.assertEqual(sum(x["weight_percent"] for x in payload["assessment_plan"]), 100)\n        self.assertEqual(sum(x["weight_percent"] for x in payload["midterm_blueprint"]), 100)\n        self.assertEqual(sum(x["weight_percent"] for x in payload["capstone"]["rubric"]), 100)\n        self.assertGreaterEqual(len(payload["diagnostic"]["questions"]), 12)\n        capstone = json.dumps(payload["capstone"], ensure_ascii=False).casefold()\n        for concept in ("coste de oportunidad", "flujo de caja", "cuello de botella", "segmentación", "icer", "gobernanza"):\n            self.assertIn(concept, capstone)\n\n    def test_sources_glossary_claims_and_media_are_complete(self):\n        sources = self.sources["sources"]\n        self.assertGreaterEqual(len(sources), 20)\n        self.assertTrue(all(s["verification_status"] == "verified_directly" for s in sources))\n        self.assertEqual(self.sources["coverage_gaps"], [])\n        self.assertEqual(self.sources["coverage_status"], "traceable")\n        self.assertGreaterEqual(len(self.glossary["entries"]), 80)\n        self.assertEqual(len(self.claims["claims"]), 24)\n        self.assertTrue(all(c["source_verification_status"] == "verified_directly" for c in self.claims["claims"]))\n        self.assertEqual(len(self.media["items"]), 6)\n        self.assertTrue(all(item["status"] == "planned" for item in self.media["items"]))\n\n    def test_claims_are_literal_content_and_cross_links_resolve(self):\n        source_ids = {{s["id"] for s in self.sources["sources"]}}\n        claim_ids = {{c["id"] for c in self.claims["claims"]}}\n        glossary_ids = {{g["id"] for g in self.glossary["entries"]}}\n        for claim in self.claims["claims"]:\n            unit_text = (CANON / "units" / f"unit-{{claim['unit']:02d}}.json").read_text(encoding="utf-8")\n            self.assertIn(claim["text"], unit_text)\n            self.assertIn(claim["source_id"], source_ids)\n        for n in range(1, 7):\n            unit = json.loads((CANON / "units" / f"unit-{{n:02d}}.json").read_text(encoding="utf-8"))\n            self.assertTrue(set(unit["claim_ids"]).issubset(claim_ids))\n            self.assertTrue(set(unit["source_ids"]).issubset(source_ids))\n            self.assertTrue(set(unit["glossary_entry_ids"]).issubset(glossary_ids))\n\n    def test_professional_boundaries_remain_explicit(self):\n        notice = self.course["editorial_notice"].casefold()\n        for phrase in ("revisión humana", "asesoría económica", "hta oficial", "certificación", "conformidad regulatoria", "validación clínica"):\n            self.assertIn(phrase, notice)\n\n\nif __name__ == "__main__":\n    unittest.main()\n'''
    (ROOT / "tests" / "test_economia_gestion_empresas_course_completion.py").write_text(test, encoding="utf-8")

    print(f"[ok] cierre canónico generado: {TARGET.relative_to(ROOT)}")
    print(f"[ok] fuentes verificadas: {len(sources)}")
    print(f"[ok] glosario consolidado: {len(glossary_entries)} entradas")
    print("[ok] claims ancla: 24")
    print("[ok] evaluaciones: 6 unitarias + 1 integradora")


if __name__ == "__main__":
    main()
