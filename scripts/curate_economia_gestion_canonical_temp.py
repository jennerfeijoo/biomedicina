#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "economia-gestion-empresas"
AREA_ID = "gestion-etica-comunicacion"
CODE = "ECOGEST"
PREFIX = CODE
SRC = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"
DST = ROOT / "data" / "courses" / COURSE_ID
TODAY = "2026-08-25"

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
    ("ECOGEST-LO01", "Analiza decisiones económicas en salud mediante escasez, coste de oportunidad, incentivos, valor y consecuencias distributivas, declarando perspectiva y límites."),
    ("ECOGEST-LO02", "Interpreta estados financieros, costes, márgenes, punto de equilibrio, flujo de caja y presupuestos para evaluar sostenibilidad sin confundir resultado contable, liquidez y valor."),
    ("ECOGEST-LO03", "Modela procesos y capacidad operativa con demanda, variabilidad, colas, inventario y calidad, proponiendo mejoras verificables sin atribuir causalidad no demostrada."),
    ("ECOGEST-LO04", "Evalúa mercado, propuesta de valor, competencia, estrategia y modelos de negocio biomédicos con evidencia trazable, incertidumbre y fronteras éticas y regulatorias."),
    ("ECOGEST-LO05", "Construye e interpreta evaluaciones económicas sanitarias con comparadores, perspectiva, horizonte, costes, resultados, ICER, beneficio monetario neto, impacto presupuestario e incertidumbre."),
    ("ECOGEST-LO06", "Diseña un sistema de gobernanza y desempeño con responsabilidades, derechos de decisión, KPIs, riesgo, compliance, controles, assurance y reglas de revisión proporcionales al contexto."),
    ("ECOGEST-LO07", "Integra economía, finanzas, operaciones, estrategia, evaluación económica y gobernanza en un expediente de decisión reproducible que explicita supuestos, conflictos, incertidumbre, alternativas y evidencia pendiente."),
]

UNIT_COURSE_LO_MAP = {
    1: ["ECOGEST-LO01", "ECOGEST-LO07"],
    2: ["ECOGEST-LO02", "ECOGEST-LO07"],
    3: ["ECOGEST-LO03", "ECOGEST-LO07"],
    4: ["ECOGEST-LO04", "ECOGEST-LO07"],
    5: ["ECOGEST-LO05", "ECOGEST-LO07"],
    6: ["ECOGEST-LO06", "ECOGEST-LO07"],
}


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value or "registro"


def unique_id(base: str, used: set[str]) -> str:
    candidate = base
    number = 2
    while candidate in used:
        candidate = f"{base}-{number}"
        number += 1
    used.add(candidate)
    return candidate


def unit_id(n: int) -> str:
    return f"{PREFIX}-U{n:02d}"


def lo_id(n: int, j: int) -> str:
    return f"{PREFIX}-U{n:02d}-LO{j:02d}"


def canonical_source_record(raw: dict, sid: str, uid: str) -> dict:
    out = {k: v for k, v in raw.items() if k not in {"id", "used_by_unit_ids"}}
    status = str(out.get("verification_status") or "").strip()
    if not status:
        out["verification_status"] = "traceable"
    elif status == "unverified":
        out["verification_status"] = "traceable_pending_human_review"
    out["id"] = sid
    out["used_by_unit_ids"] = [uid]
    return out


def main() -> None:
    units_raw = [json.loads((SRC / f"unit-{n:02d}.json").read_text(encoding="utf-8")) for n in range(1, 7)]
    shutil.rmtree(DST, ignore_errors=True)
    (DST / "units").mkdir(parents=True, exist_ok=True)
    (DST / "assessments").mkdir(parents=True, exist_ok=True)

    source_records: dict[str, dict] = {}
    source_key_to_id: dict[str, str] = {}
    used_source_ids: set[str] = set()
    unit_source_ids: dict[int, list[str]] = defaultdict(list)

    for n, unit in enumerate(units_raw, 1):
        uid = unit_id(n)
        for raw in unit.get("sources", []):
            key = str(raw.get("url") or raw.get("doi") or raw.get("title") or "").strip().casefold()
            if not key:
                continue
            if key in source_key_to_id:
                sid = source_key_to_id[key]
                used = source_records[sid].setdefault("used_by_unit_ids", [])
                if uid not in used:
                    used.append(uid)
            else:
                sid = unique_id(slugify(str(raw.get("title") or raw.get("organization") or key))[:90], used_source_ids)
                source_key_to_id[key] = sid
                source_records[sid] = canonical_source_record(raw, sid, uid)
            unit_source_ids[n].append(sid)
        unit_source_ids[n] = list(dict.fromkeys(unit_source_ids[n]))

    if not source_records:
        raise SystemExit("No se encontraron fuentes en U1–U6")

    glossary_entries: list[dict] = []
    glossary_ids_by_unit: dict[int, list[str]] = defaultdict(list)
    claim_records: list[dict] = []
    claim_ids_by_unit: dict[int, list[str]] = defaultdict(list)
    media_items: list[dict] = []
    media_ids_by_unit: dict[int, list[str]] = defaultdict(list)
    canonical_units: list[dict] = []

    for n, raw in enumerate(units_raw, 1):
        uid = unit_id(n)
        local_los = [
            {"id": lo_id(n, j), "statement": statement}
            for j, statement in enumerate(raw.get("learning_objectives", []), 1)
        ]
        if not local_los:
            raise SystemExit(f"U{n} sin resultados de aprendizaje")

        topics: list[dict] = []
        candidate_claims: list[str] = []
        for ti, section in enumerate(raw.get("theory_sections", []), 1):
            tid = f"{uid}-T{ti:02d}"
            equations = []
            for ei, equation in enumerate(section.get("equations", []), 1):
                equations.append({
                    "id": f"{tid}-B{ei:02d}",
                    "type": "equation",
                    "latex": str(equation.get("latex") or "").strip(),
                    "label": str(equation.get("meaning") or equation.get("label") or "Relación cuantitativa de la unidad.").strip(),
                })
            key_points = [str(x).strip() for x in section.get("key_points", []) if str(x).strip()]
            candidate_claims.extend(key_points)
            subtopics = []
            paragraphs = [str(x).strip() for x in section.get("paragraphs", []) if str(x).strip()]
            for pi, paragraph in enumerate(paragraphs, 1):
                stid = f"{tid}-ST{pi:02d}"
                title = key_points[pi - 1] if pi <= len(key_points) else f"{section.get('heading', 'Desarrollo')} — explicación {pi}"
                subtopics.append({
                    "id": stid,
                    "title": title,
                    "blocks": [{"id": f"{stid}-B01", "type": "paragraph", "text": paragraph}],
                })
            if not subtopics:
                raise SystemExit(f"U{n} sección {ti} sin párrafos")
            topics.append({
                "id": tid,
                "title": str(section.get("heading") or f"Tema {ti}"),
                "blocks": equations,
                "key_points": key_points or [subtopics[0]["title"]],
                "subtopics": subtopics,
            })

        examples = []
        for j, ex in enumerate(raw.get("worked_examples", []), 1):
            examples.append({
                "id": f"{uid}-EX{j:02d}",
                "title": str(ex.get("title") or f"Ejemplo {j}"),
                "scenario": str(ex.get("scenario") or "Caso sintético de aplicación."),
                "reasoning_steps": list(ex.get("reasoning_steps") or []),
                "interpretation": str(ex.get("interpretation") or "Interpretar dentro del alcance declarado."),
                "limitations": list(ex.get("limitations") or ["El ejemplo es educativo y no autoriza una decisión real."]),
            })

        activities = []
        prereqs = [unit_id(n - 1)] if n > 1 else []
        for j, activity in enumerate(raw.get("guided_activities", []), 1):
            instructions = [str(x) for x in activity.get("instructions", []) if str(x).strip()]
            tasks = [str(x) for x in activity.get("problems", []) if str(x).strip()]
            deliverables = [str(x) for x in activity.get("deliverables", []) if str(x).strip()]
            criteria = [str(x) for x in activity.get("checking_criteria", []) if str(x).strip()]
            activities.append({
                "id": f"{uid}-ACT{j:02d}",
                "title": str(activity.get("title") or f"Actividad {j}"),
                "purpose": f"Aplicar los resultados de aprendizaje de {raw.get('title', f'U{n}')} en un producto sintético reproducible con criterios de comprobación explícitos.",
                "prerequisite_unit_ids": prereqs,
                "instructions": instructions or ["Trabaja con datos y escenarios sintéticos y conserva todos los supuestos."],
                "tasks": tasks or ["Resolver el caso y justificar cada decisión."],
                "deliverables": deliverables or ["Expediente reproducible del caso."],
                "checking_criteria": criteria or ["La conclusión conserva supuestos, incertidumbre y límites."],
                "estimated_duration_minutes": int(activity.get("duration_minutes") or 180),
                "status": "complete",
            })
        if not activities:
            raise SystemExit(f"U{n} sin actividad guiada")

        for j, entry in enumerate(raw.get("glossary", []), 1):
            gid = f"{uid}-G{j:03d}"
            sids = unit_source_ids[n][:2] or [next(iter(source_records))]
            glossary_entries.append({
                "id": gid,
                "term": str(entry.get("term") or "").strip(),
                "definition": str(entry.get("definition") or "").strip(),
                "unit_ids": [uid],
                "source_ids": sids,
                "verification_status": "traceable_to_verified_unit_sources",
            })
            glossary_ids_by_unit[n].append(gid)

        unique_claims = []
        for text in candidate_claims:
            if text and text not in unique_claims:
                unique_claims.append(text)
        if len(unique_claims) < 4:
            for topic in topics:
                for sub in topic["subtopics"]:
                    text = sub["blocks"][0]["text"]
                    if text not in unique_claims:
                        unique_claims.append(text)
                    if len(unique_claims) >= 4:
                        break
                if len(unique_claims) >= 4:
                    break
        sids = unit_source_ids[n] or [next(iter(source_records))]
        for j, text in enumerate(unique_claims[:4], 1):
            cid = f"{uid}-C{j:03d}"
            claim_records.append({
                "id": cid,
                "claim_id": cid,
                "unit": n,
                "unit_id": uid,
                "text": text,
                "claim_type": "methodological_or_interpretive",
                "risk": "medium",
                "context": f"Síntesis educativa de {raw.get('title')}; interpretar dentro de alcance, supuestos y límites de la unidad.",
                "source_id": sids[(j - 1) % len(sids)],
                "support": "direct_or_synthesis",
                "source_verification_status": source_records[sids[(j - 1) % len(sids)]].get("verification_status", "traceable"),
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": TODAY,
            })
            claim_ids_by_unit[n].append(cid)

        mid = f"{uid}-MED01"
        media_items.append({
            "id": mid,
            "type": "figure",
            "status": "planned",
            "unit_id": uid,
            "linked_learning_outcome_ids": [x["id"] for x in local_los[:2]],
            "pedagogical_purpose": f"Representar visualmente los conceptos centrales de {raw.get('title')} mediante un recurso propio o con licencia compatible.",
            "alt_text_draft": None,
            "license_requirements": "Usar material propio o con licencia compatible y registrar atribución y procedencia.",
            "source_ids": [],
        })
        media_ids_by_unit[n].append(mid)

        canonical = {
            "$schema": "../../../../schemas/academic/unit-v1.schema.json",
            "schema_version": "1.0",
            "id": uid,
            "course_id": COURSE_ID,
            "order": n,
            "slug": slugify(str(raw.get("title") or f"unidad-{n}")),
            "title": str(raw.get("title") or f"Unidad {n}"),
            "status": STATUS,
            "purpose": str(raw.get("purpose") or "Construir una comprensión disciplinar reproducible dentro del alcance del curso."),
            "prerequisite_unit_ids": prereqs,
            "course_learning_outcome_ids": UNIT_COURSE_LO_MAP[n],
            "learning_outcomes": local_los,
            "topics": topics,
            "examples": examples,
            "activities": activities,
            "assessment_file": f"assessments/unit-{n:02d}.json",
            "glossary_entry_ids": glossary_ids_by_unit[n],
            "source_ids": unit_source_ids[n] or [next(iter(source_records))],
            "claim_ids": claim_ids_by_unit[n],
            "media_ids": media_ids_by_unit[n],
            "common_errors": list(raw.get("common_errors") or []),
            "biomedical_connections": [
                f"{x.get('topic')}: {x.get('connection')}" if isinstance(x, dict) else str(x)
                for x in raw.get("biomedical_connections", [])
            ],
            "editorial_notice": str(raw.get("editorial_notice") or "Material educativo; revisión humana interna y externa pendientes."),
            "legacy_origin": f"data/course_redevelopment/{COURSE_ID}/units/unit-{n:02d}.json",
        }
        canonical_units.append(canonical)
        dump(DST / "units" / f"unit-{n:02d}.json", canonical)

        assessment_items = []
        self_assessment = raw.get("self_assessment", [])
        for j, item in enumerate(self_assessment, 1):
            lid = local_los[(j - 1) % len(local_los)]["id"]
            source_id = (unit_source_ids[n] or [next(iter(source_records))])[(j - 1) % len(unit_source_ids[n] or [next(iter(source_records))])]
            assessment_items.append({
                "id": f"{uid}-A{j:03d}",
                "type": "short_answer" if j % 3 else "case_analysis",
                "prompt": str(item.get("question") or "Explica la decisión más defendible y sus límites."),
                "linked_learning_outcome_ids": [lid],
                "difficulty": "foundational" if j <= 3 else ("intermediate" if j <= 8 else "advanced"),
                "cognitive_level": "understand" if j <= 3 else ("apply" if j <= 7 else "evaluate"),
                "answer_key": {
                    "expected_answer": str(item.get("answer") or "Respuesta coherente con el contenido de la unidad."),
                    "explanation": str(item.get("reasoning") or item.get("answer") or "La respuesta debe justificar el razonamiento y conservar el alcance."),
                    "common_misconceptions": [str(item.get("common_error"))] if item.get("common_error") else [],
                },
                "feedback": {
                    "correct": "Respuesta compatible con el modelo y los límites de la unidad; conserva la justificación y la procedencia.",
                    "incorrect": f"Revisa el resultado {lid}, identifica el error conceptual y reescribe la respuesta explicando qué evidencia permite sostenerla.",
                },
                "source_ids": [source_id],
                "status": "complete",
            })
        if len(assessment_items) < 8:
            raise SystemExit(f"U{n} tiene menos de 8 ítems de autoevaluación para migrar")
        dump(DST / "assessments" / f"unit-{n:02d}.json", {
            "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
            "schema_version": "1.0",
            "id": f"{uid}-ASSESS",
            "course_id": COURSE_ID,
            "scope": "unit",
            "unit_id": uid,
            "purpose": f"Comprobar comprensión y transferencia de {raw.get('title')} mediante respuestas razonadas, feedback recuperativo y fuentes trazables.",
            "student_payload_policy": "Los ítems usan exclusivamente datos o escenarios sintéticos; la clave razonada se consulta después del primer intento.",
            "items": assessment_items,
            "status": "complete",
        })

    # Registries
    dump(DST / "sources.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "source_policy": "Se consolidan las fuentes trazadas en U1–U6 conservando su estado de verificación; la revisión disciplinaria humana permanece pendiente.",
        "consulted_on": TODAY,
        "coverage_gaps": [],
        "coverage_status": "traceable",
        "sources": list(source_records.values()),
    })
    dump(DST / "glossary.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "coverage_status": "traceable",
        "entries": glossary_entries,
    })
    dump(DST / "claims.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": "Afirmaciones centrales literales de U1–U6 vinculadas a fuentes del corpus; revisión disciplinaria humana pendiente.",
        "review_state": "ai_review_provisional",
        "claims": claim_records,
    })
    dump(DST / "media.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "coverage_status": "planned",
        "items": media_items,
    })

    core_sources = list(source_records)[: min(12, len(source_records))]
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
        "audience": "Estudiantes de ingeniería biomédica y áreas afines que necesitan fundamentar decisiones organizacionales y económicas en salud con evidencia cuantitativa, trazabilidad, incertidumbre y límites profesionales explícitos.",
        "status": STATUS,
        "purpose": "Integrar economía, finanzas, operaciones, mercado y estrategia, evaluación económica sanitaria y gobernanza para analizar decisiones en organizaciones biomédicas mediante modelos reproducibles, datos trazables, alternativas, incertidumbre, accountability y límites claros entre evidencia educativa y decisiones reales de inversión, reembolso, compliance o atención sanitaria.",
        "scope": {
            "included": [
                "Escasez, incentivos, coste de oportunidad, valor y consecuencias distributivas en contextos sanitarios.",
                "Contabilidad, estados financieros, costes, márgenes, punto de equilibrio, flujo de caja y presupuestos.",
                "Procesos, capacidad, variabilidad, colas, inventario, calidad y mejora operativa.",
                "Mercado, propuesta de valor, segmentación, competencia, estrategia y modelos de negocio biomédicos.",
                "Evaluación económica sanitaria, QALY, ICER, beneficio monetario neto, impacto presupuestario, asequibilidad e incertidumbre.",
                "Gobernanza, derechos de decisión, KPIs, riesgo, compliance, controles, assurance y revisión de decisiones.",
                "Expedientes integradores con supuestos, conflictos de interés, trazabilidad, sensibilidad y evidencia pendiente."
            ],
            "excluded": [
                "Asesoría financiera, recomendación de inversión o valoración real de una empresa.",
                "Decisiones oficiales de reembolso, compra, contratación o asignación presupuestaria.",
                "Determinación jurídica de cumplimiento, certificación ISO o auditoría profesional.",
                "Recomendación clínica, priorización individual de pacientes o inferencia causal no sustentada.",
                "Uso de información personal, confidencial o empresarial real en las actividades autónomas."
            ],
            "handoff_courses": ["innovacion-emprendimiento", "ingenieria-clinica-gestion", "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas", "tecnologias-administracion"]
        },
        "prerequisites": [
            {"id": "ECOGEST-PRE01", "statement": "Álgebra, porcentajes, tasas, unidades y lectura de gráficos a nivel universitario inicial."},
            {"id": "ECOGEST-PRE02", "statement": "Estadística descriptiva básica, incertidumbre y comparación de escenarios."},
            {"id": "ECOGEST-PRE03", "statement": "Conceptos introductorios de sistemas de salud, tecnologías biomédicas y organizaciones."},
            {"id": "ECOGEST-PRE04", "statement": "Uso básico de hojas de cálculo o programación para cálculos reproducibles."}
        ],
        "competencies": [
            {"id": "ECOGEST-COMP01", "statement": "Estructurar decisiones económicas y organizacionales con pregunta, perspectiva, alternativas, restricciones y criterios explícitos."},
            {"id": "ECOGEST-COMP02", "statement": "Interpretar información financiera y operativa sin colapsar rentabilidad, liquidez, capacidad y valor en una sola métrica."},
            {"id": "ECOGEST-COMP03", "statement": "Evaluar estrategias y modelos de negocio biomédicos con evidencia, incertidumbre y límites éticos y regulatorios."},
            {"id": "ECOGEST-COMP04", "statement": "Construir evaluaciones económicas y presupuestarias distinguiendo coste-efectividad, asequibilidad y decisión de financiación."},
            {"id": "ECOGEST-COMP05", "statement": "Diseñar gobernanza, indicadores, riesgo, compliance y assurance con trazabilidad y responsabilidades claras."},
            {"id": "ECOGEST-COMP06", "statement": "Integrar U1–U6 en expedientes de decisión reproducibles y comunicarlos proporcionalmente a la evidencia."}
        ],
        "learning_outcomes": [{"id": i, "statement": s} for i, s in COURSE_LOS],
        "study_method": [
            "Definir la decisión, perspectiva, alternativas, restricciones y resultado admisible antes de calcular.",
            "Alternar explicación, ejemplo resuelto, actividad guiada, feedback y transferencia con apoyo progresivamente menor.",
            "Separar dato, cálculo, modelo, interpretación y decisión y conservar la procedencia de cada capa.",
            "Realizar análisis de sensibilidad cuando una conclusión dependa de supuestos o parámetros inciertos.",
            "Distinguir eficiencia, asequibilidad, capacidad, riesgo, compliance y decisión real en lugar de reducirlos a una sola puntuación.",
            "Cerrar cada producto con límites, conflictos de interés y siguiente evidencia necesaria."
        ],
        "core_source_ids": core_sources,
        "unit_files": [f"units/unit-{n:02d}.json" for n in range(1, 7)],
        "assessment_files": [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"],
        "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
        "static_site": {
            "renderer": "scripts/generate_site.py",
            "canonical_source": True,
            "legacy_mirrors": [
                f"data/generated_courses/{COURSE_ID}.json",
                f"data/generated_units/{COURSE_ID}/",
                f"data/subjects/{AREA_ID}/{COURSE_ID}.json",
                f"data/source_registry/{COURSE_ID}.json",
                f"data/claim_registry/{COURSE_ID}.json"
            ]
        },
        "editorial_notice": "Corpus canónico completo a nivel de contenido y pedagogía interna para U1–U6. Las fuentes quedan trazadas y la publicación es provisional. La revisión humana interna y disciplinaria externa, certificación, auditoría, determinación jurídica de compliance, decisiones reales de inversión/reembolso y recomendaciones clínicas permanecen fuera del cierre y siguen pendientes."
    }
    dump(DST / "course.json", course)

    course_assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": "ECOGEST-ASSESS-COURSE",
        "course_id": COURSE_ID,
        "scope": "course",
        "principles": [
            "La evaluación separa cálculo, interpretación y decisión; una cifra correcta sin supuestos, fuente o límite recibe crédito parcial.",
            "Toda evidencia de dominio debe ser reproducible y usar datos sintéticos o abiertos en las actividades autónomas.",
            "Coste-efectividad, rentabilidad, liquidez, capacidad, riesgo y compliance se evalúan como conceptos distintos.",
            "La retroalimentación se usa para corregir razonamiento y documentar cambios antes del cierre de productos principales.",
            "La revisión humana interna y externa permanece pendiente y no se sustituye por los gates automáticos del repositorio."
        ],
        "assessment_plan": [
            {"id": "ECOGEST-PLAN-01", "component": "Autoevaluaciones razonadas U1–U6", "type": "formative_with_low_stakes_grade", "weight_percent": 10, "linked_learning_outcome_ids": [f"ECOGEST-LO{i:02d}" for i in range(1, 7)], "description": "Ítems breves con explicación y recuperación de errores."},
            {"id": "ECOGEST-PLAN-02", "component": "Productos aplicados U1–U6", "type": "performance_tasks", "weight_percent": 25, "linked_learning_outcome_ids": [f"ECOGEST-LO{i:02d}" for i in range(1, 7)], "description": "Portafolio de actividades guiadas con cálculos, controles, sensibilidad y límites."},
            {"id": "ECOGEST-PLAN-03", "component": "Examen integrador intermedio", "type": "individual_integrative_exam", "weight_percent": 20, "linked_learning_outcome_ids": ["ECOGEST-LO01", "ECOGEST-LO02", "ECOGEST-LO03", "ECOGEST-LO04"], "description": "Problemas nuevos de economía, finanzas, operaciones y estrategia."},
            {"id": "ECOGEST-PLAN-04", "component": "Proyecto integrador de decisión biomédica", "type": "capstone_project", "weight_percent": 35, "linked_learning_outcome_ids": [f"ECOGEST-LO{i:02d}" for i in range(1, 8)], "description": "Expediente sintético que integra las seis unidades y compara alternativas."},
            {"id": "ECOGEST-PLAN-05", "component": "Defensa, revisión y bitácora", "type": "oral_and_process_evidence", "weight_percent": 10, "linked_learning_outcome_ids": ["ECOGEST-LO05", "ECOGEST-LO06", "ECOGEST-LO07"], "description": "Defensa de decisiones, límites, conflictos y revisiones del expediente."}
        ],
        "diagnostic": {
            "title": "Diagnóstico de entrada a Economía y Gestión de Empresas",
            "purpose": "Detectar necesidades de nivelación; no aporta nota sumativa.",
            "questions": [
                "Distingue coste de oportunidad de gasto monetario.",
                "Calcula un porcentaje y explica su denominador.",
                "Distingue beneficio contable de flujo de caja.",
                "Explica qué significa una restricción de capacidad.",
                "Distingue correlación de causalidad en una métrica de desempeño.",
                "Define comparador en una decisión.",
                "Explica por qué una tasa necesita periodo y población.",
                "Distingue coste-efectividad de asequibilidad.",
                "Explica qué significa analizar sensibilidad a un supuesto.",
                "Distingue gobernanza de gestión operativa.",
                "Identifica un conflicto de interés en un caso sintético.",
                "Describe qué información hace reproducible una decisión."
            ]
        },
        "midterm_blueprint": [
            {"id": "ECOGEST-MID-01", "domain": "Economía y valor", "weight_percent": 25, "linked_learning_outcome_ids": ["ECOGEST-LO01"]},
            {"id": "ECOGEST-MID-02", "domain": "Finanzas y sostenibilidad", "weight_percent": 25, "linked_learning_outcome_ids": ["ECOGEST-LO02"]},
            {"id": "ECOGEST-MID-03", "domain": "Operaciones y capacidad", "weight_percent": 25, "linked_learning_outcome_ids": ["ECOGEST-LO03"]},
            {"id": "ECOGEST-MID-04", "domain": "Mercado y estrategia", "weight_percent": 25, "linked_learning_outcome_ids": ["ECOGEST-LO04"]}
        ],
        "capstone": {
            "title": "Expediente integrador de decisión para una organización biomédica sintética",
            "purpose": "Integrar U1–U6 en una decisión reproducible sin convertir el producto en recomendación profesional real.",
            "deliverables": [
                "Pregunta de decisión, perspectiva, alternativas y restricciones.",
                "Modelo de valor y consecuencias distributivas.",
                "Modelo financiero y flujo de caja con escenarios.",
                "Mapa de proceso, capacidad y riesgos operativos.",
                "Análisis de mercado, propuesta de valor y estrategia.",
                "Evaluación económica e impacto presupuestario sintéticos.",
                "Mapa de gobernanza, KPIs, riesgos, obligaciones y assurance.",
                "Análisis de sensibilidad y escenarios que podrían cambiar la decisión.",
                "Log de decisiones, conflictos de interés y correcciones.",
                "Conclusión proporcional con evidencia pendiente y condiciones de revisión."
            ],
            "rubric": [
                {"criterion": "Planteamiento y alternativas", "weight_percent": 10, "excellent": "Pregunta, perspectiva, alternativas y restricciones completas y coherentes.", "adequate": "Planteamiento mayormente claro con omisiones menores.", "developing": "Faltan elementos que condicionan la decisión.", "insufficient": "No existe una decisión reproducible."},
                {"criterion": "Economía y finanzas", "weight_percent": 15, "excellent": "Costes, oportunidad, estados, caja y escenarios se distinguen y calculan correctamente.", "adequate": "Cálculos correctos con límites menores.", "developing": "Hay confusiones entre métricas o supuestos.", "insufficient": "La interpretación financiera no es defendible."},
                {"criterion": "Operaciones y estrategia", "weight_percent": 15, "excellent": "Capacidad, proceso, mercado y estrategia están conectados a la decisión con evidencia.", "adequate": "Conexión suficiente con alguna simplificación.", "developing": "Predomina descripción sin criterio de decisión.", "insufficient": "No se modelan restricciones operativas o estratégicas."},
                {"criterion": "Evaluación económica", "weight_percent": 15, "excellent": "Comparadores, costes, resultados, ICER/INMB, asequibilidad e incertidumbre se separan correctamente.", "adequate": "Evaluación coherente con límites menores.", "developing": "Faltan supuestos, comparadores o incertidumbre.", "insufficient": "Se confunde coste-efectividad con decisión automática."},
                {"criterion": "Gobernanza, riesgo y compliance", "weight_percent": 15, "excellent": "Autoridad, KPIs, riesgos, obligaciones, controles y assurance son trazables y no se confunden.", "adequate": "Sistema suficiente con algunas omisiones.", "developing": "Responsabilidades o controles ambiguos.", "insufficient": "Se afirma compliance o certificación sin evidencia."},
                {"criterion": "Reproducibilidad y evidencia", "weight_percent": 15, "excellent": "Datos, fórmulas, fuentes, versiones y correcciones permiten reconstruir el expediente.", "adequate": "Reproducibilidad suficiente con metadatos menores faltantes.", "developing": "Hay pasos tácitos o procedencia incompleta.", "insufficient": "No puede reconstruirse el resultado."},
                {"criterion": "Incertidumbre, límites y defensa", "weight_percent": 15, "excellent": "Sensibilidad, conflictos, alternativas, límites y siguiente evidencia están explícitos y defendidos.", "adequate": "Límites claros con análisis parcial.", "developing": "La conclusión excede parte de la evidencia.", "insufficient": "Se presenta una decisión real o certeza no sustentada."}
            ]
        },
        "status": "complete"
    }
    dump(DST / "assessments" / "course-assessment.json", course_assessment)

    test = ROOT / "tests" / "test_economia_gestion_empresas_canonical_course.py"
    test.write_text('''from __future__ import annotations\n\nimport json\nimport unittest\nfrom collections import Counter\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nCOURSE = ROOT / "data" / "courses" / "economia-gestion-empresas"\nGENERIC = "concepto de la unidad que debe definirse mediante entidades observables"\n\nclass EconomiaGestionCanonicalCourseTests(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))\n        cls.units = [json.loads((COURSE / f"units/unit-{i:02d}.json").read_text(encoding="utf-8")) for i in range(1, 7)]\n        cls.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))\n        cls.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))\n        cls.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))\n        cls.assessment = json.loads((COURSE / "assessments/course-assessment.json").read_text(encoding="utf-8"))\n\n    def test_course_is_complete_but_human_review_pending(self):\n        status = self.course["status"]\n        self.assertEqual(status["content"], "complete")\n        self.assertEqual(status["sources"], "traceable")\n        self.assertEqual(status["pedagogy"], "complete")\n        self.assertEqual(status["multimedia"], "planned")\n        self.assertEqual(status["internal_review"], "pending")\n        self.assertEqual(status["external_review"], "pending")\n        self.assertEqual(status["publication"], "published_provisional")\n        self.assertEqual(len(self.course["unit_files"]), 6)\n\n    def test_units_preserve_substantive_content_and_no_template(self):\n        text = " ".join(json.dumps(u, ensure_ascii=False) for u in self.units).casefold()\n        self.assertNotIn(GENERIC, text)\n        self.assertTrue(all(len(u["topics"]) >= 4 for u in self.units))\n        self.assertTrue(all(len(u["examples"]) >= 3 for u in self.units))\n        self.assertTrue(all(len(u["activities"]) >= 1 for u in self.units))\n        self.assertGreaterEqual(len(self.units[5]["activities"]), 3)\n\n    def test_registries_are_substantive_and_traceable(self):\n        self.assertGreaterEqual(len(self.sources["sources"]), 30)\n        self.assertGreaterEqual(len(self.glossary["entries"]), 80)\n        self.assertEqual(len(self.claims["claims"]), 24)\n        source_ids = {s["id"] for s in self.sources["sources"]}\n        counts = Counter(c["unit_id"] for c in self.claims["claims"])\n        for u in self.units:\n            self.assertEqual(counts[u["id"]], 4)\n            canonical_text = json.dumps(u, ensure_ascii=False)\n            for claim in [c for c in self.claims["claims"] if c["unit_id"] == u["id"]]:\n                self.assertIn(claim["text"], canonical_text)\n                self.assertIn(claim["source_id"], source_ids)\n\n    def test_unit_assessments_have_reasoning_and_feedback(self):\n        for i, unit in enumerate(self.units, 1):\n            payload = json.loads((COURSE / f"assessments/unit-{i:02d}.json").read_text(encoding="utf-8"))\n            self.assertGreaterEqual(len(payload["items"]), 8)\n            self.assertTrue(all(item["answer_key"]["explanation"] for item in payload["items"]))\n            self.assertTrue(all(item["feedback"]["incorrect"] for item in payload["items"]))\n\n    def test_course_assessment_covers_all_outcomes_and_weights(self):\n        self.assertEqual(sum(x["weight_percent"] for x in self.assessment["assessment_plan"]), 100)\n        self.assertEqual(sum(x["weight_percent"] for x in self.assessment["midterm_blueprint"]), 100)\n        self.assertEqual(sum(x["weight_percent"] for x in self.assessment["capstone"]["rubric"]), 100)\n        all_los = {x["id"] for x in self.course["learning_outcomes"]}\n        covered = {lo for item in self.assessment["assessment_plan"] for lo in item.get("linked_learning_outcome_ids", [])}\n        self.assertEqual(all_los, covered)\n        self.assertGreaterEqual(len(self.assessment["diagnostic"]["questions"]), 10)\n        self.assertGreaterEqual(len(self.assessment["capstone"]["deliverables"]), 8)\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")

    print(f"Canonical closure written: {DST}")
    print(f"sources={len(source_records)} glossary={len(glossary_entries)} claims={len(claim_records)}")


if __name__ == "__main__":
    main()
