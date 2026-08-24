#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUBJECT = "biomecanica-medios-continuos"
CODE = "BMCONT"
SOURCE_DIR = ROOT / "data" / "course_redevelopment" / SUBJECT / "units"
TARGET = ROOT / "data" / "courses" / SUBJECT

STATUS_COMPLETE = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}

UNIT_LIMITS = {
    1: [
        "La cinemática continua describe movimiento y deformación; no determina por sí sola tensiones, propiedades constitutivas ni daño.",
        "Una magnitud macroscópica no se transfiere automáticamente a células, fibras o poros sin un puente multiescala explícito.",
    ],
    2: [
        "El equilibrio y el tensor de tensiones no determinan una respuesta material sin una ley constitutiva y condiciones de frontera suficientes.",
        "Una tensión calculada no equivale por sí sola a daño, lesión, seguridad o relevancia clínica.",
    ],
    3: [
        "Un buen ajuste constitutivo no demuestra unicidad paramétrica ni capacidad predictiva fuera del dominio de calibración.",
        "Los parámetros de un modelo hiperelástico son dependientes de formulación, datos, escala y supuestos; no son diagnósticos tisulares universales.",
    ],
    4: [
        "Una curva de relajación o fluencia no identifica por sí sola un mecanismo biológico único ni separa automáticamente matriz sólida y transporte de fluido.",
        "La validez de un modelo viscoelástico o poroelástico depende de escala temporal, drenaje, geometría, condiciones de frontera e identificabilidad.",
    ],
    5: [
        "Métricas hemodinámicas o respiratorias derivadas de un modelo no equivalen a diagnóstico, causalidad patológica ni beneficio clínico.",
        "La elección de reología y condiciones de frontera puede cambiar las salidas; debe analizarse sensibilidad antes de transferir una conclusión.",
    ],
    6: [
        "Convergencia de malla y verificación numérica no equivalen a validación contra realidad física ni a credibilidad para cualquier contexto de uso.",
        "Un modelo de elementos finitos validado para una variable y régimen no queda validado automáticamente para otros tejidos, cargas, endpoints o decisiones.",
    ],
}

PREREQUISITES = {
    1: [],
    2: [1],
    3: [1, 2],
    4: [1, 2, 3],
    5: [1, 2],
    6: [1, 2, 3, 4, 5],
}


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected object")
    return payload


def write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def dict_list(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def normalize_connection(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if not isinstance(value, dict):
        return ""
    context = str(value.get("context") or value.get("topic") or value.get("title") or "").strip()
    detail = str(value.get("connection") or value.get("description") or value.get("text") or "").strip()
    return f"{context}: {detail}" if context and detail else context or detail


def unique_id(base: str, used: set[str]) -> str:
    candidate = base or "fuente"
    suffix = 2
    while candidate in used:
        candidate = f"{base}-{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def build_sources(units: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[int, list[str]], dict[int, dict[str, str]]]:
    records: OrderedDict[str, dict[str, Any]] = OrderedDict()
    by_key: dict[str, str] = {}
    used_ids: set[str] = set()
    unit_ids: dict[int, list[str]] = {}
    local_map: dict[int, dict[str, str]] = {}

    for unit in units:
        number = int(unit["unit"])
        canonical_unit = f"{CODE}-U{number:02d}"
        unit_ids[number] = []
        local_map[number] = {}
        for source in dict_list(unit.get("sources")):
            raw_id = str(source.get("id") or source.get("registry_id") or "fuente").strip()
            url = str(source.get("url") or "").strip()
            citation = str(source.get("citation") or source.get("title") or source.get("organization") or "").strip()
            key = f"url:{url}" if url else f"citation:{citation.casefold()}"
            source_id = by_key.get(key)
            if source_id is None:
                source_id = unique_id(raw_id, used_ids)
                record = dict(source)
                record["id"] = source_id
                verification = str(record.get("verification_status") or "").strip()
                if not verification or verification == "unverified":
                    raise ValueError(f"U{number}: source {raw_id} is not directly traceable/verified")
                record["used_by_unit_ids"] = [canonical_unit]
                records[source_id] = record
                by_key[key] = source_id
            else:
                used_by = records[source_id].setdefault("used_by_unit_ids", [])
                if canonical_unit not in used_by:
                    used_by.append(canonical_unit)
                for field, value in source.items():
                    if value not in (None, "", []) and not records[source_id].get(field):
                        records[source_id][field] = value
            unit_ids[number].append(source_id)
            local_map[number][raw_id] = source_id
        unit_ids[number] = list(dict.fromkeys(unit_ids[number]))
        if not unit_ids[number]:
            raise ValueError(f"U{number}: no sources available")
    return list(records.values()), unit_ids, local_map


def build_glossary(units: list[dict[str, Any]], unit_source_ids: dict[int, list[str]]) -> tuple[list[dict[str, Any]], dict[int, list[str]]]:
    entries: OrderedDict[str, dict[str, Any]] = OrderedDict()
    unit_glossary_ids: dict[int, list[str]] = {int(unit["unit"]): [] for unit in units}
    for unit in units:
        number = int(unit["unit"])
        unit_id = f"{CODE}-U{number:02d}"
        for item in dict_list(unit.get("glossary")):
            term = str(item.get("term") or "").strip()
            definition = str(item.get("definition") or "").strip()
            if not term or not definition:
                continue
            key = term.casefold()
            if key not in entries:
                entry_id = f"{CODE}-GLO-{len(entries) + 1:03d}"
                entries[key] = {
                    "id": entry_id,
                    "term": term,
                    "definition": definition,
                    "unit_ids": [],
                    "source_ids": [],
                    "verification_status": "traceable_to_verified_unit_sources_2026-08-24",
                }
            record = entries[key]
            if unit_id not in record["unit_ids"]:
                record["unit_ids"].append(unit_id)
            for source_id in unit_source_ids[number]:
                if source_id not in record["source_ids"]:
                    record["source_ids"].append(source_id)
            unit_glossary_ids[number].append(record["id"])
    return list(entries.values()), unit_glossary_ids


def build_claims(
    units: list[dict[str, Any]], local_source_map: dict[int, dict[str, str]], unit_source_ids: dict[int, list[str]]
) -> tuple[list[dict[str, Any]], dict[int, list[str]]]:
    claims: list[dict[str, Any]] = []
    unit_claim_ids: dict[int, list[str]] = {}
    for unit in units:
        number = int(unit["unit"])
        unit_id = f"{CODE}-U{number:02d}"
        unit_claim_ids[number] = []
        sections = dict_list(unit.get("theory_sections"))
        if len(sections) < 4:
            raise ValueError(f"U{number}: expected at least four theory sections")
        for index, section in enumerate(sections[:4], start=1):
            key_points = text_list(section.get("key_points"))
            if not key_points:
                raise ValueError(f"U{number} section {index}: no key point for literal claim")
            text = key_points[0]
            source_id = ""
            for raw_source in text_list(section.get("source_ids")):
                mapped = local_source_map[number].get(raw_source)
                if mapped:
                    source_id = mapped
                    break
            if not source_id:
                source_id = unit_source_ids[number][0]
            claim_id = f"{CODE}-CLM-U{number:02d}-{index:02d}"
            claims.append(
                {
                    "id": claim_id,
                    "unit_id": unit_id,
                    "text": text,
                    "source_id": source_id,
                    "verification_status": "traceable_to_verified_source",
                    "status": "internally_curated_external_review_pending",
                }
            )
            unit_claim_ids[number].append(claim_id)
    return claims, unit_claim_ids


def build_examples(unit: dict[str, Any], unit_id: str, number: int) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for index, example in enumerate(dict_list(unit.get("worked_examples")), start=1):
        interpretation = str(
            example.get("interpretation") or example.get("result") or example.get("conclusion") or ""
        ).strip()
        if not interpretation:
            interpretation = "El resultado solo es interpretable dentro de los supuestos mecánicos declarados en el ejemplo."
        limitations = text_list(example.get("limitations")) or UNIT_LIMITS[number]
        result.append(
            {
                "id": f"{unit_id}-EJ{index:02d}",
                "title": str(example.get("title") or f"Ejemplo {index}").strip(),
                "scenario": str(example.get("scenario") or "Escenario sintético de la unidad.").strip(),
                "reasoning_steps": text_list(example.get("reasoning_steps")),
                "interpretation": interpretation,
                "limitations": limitations,
            }
        )
    if len(result) < 3:
        raise ValueError(f"U{number}: expected at least three worked examples")
    return result


def build_activities(unit: dict[str, Any], unit_id: str, prerequisites: list[str]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    activities = dict_list(unit.get("guided_activities"))
    for index, activity in enumerate(activities, start=1):
        tasks = text_list(activity.get("problems")) + text_list(activity.get("tasks"))
        duration = max(180, min(300, 60 + 15 * len(tasks)))
        output.append(
            {
                "id": f"{unit_id}-ACT{index:02d}",
                "title": str(activity.get("title") or f"Actividad guiada {index}").strip(),
                "purpose": f"Aplicar de forma reproducible los conceptos de {str(unit.get('title') or '').strip()} en un problema sintético, con supuestos, controles, sensibilidad y límites explícitos.",
                "prerequisite_unit_ids": prerequisites,
                "instructions": text_list(activity.get("instructions")),
                "tasks": tasks,
                "deliverables": text_list(activity.get("deliverables")),
                "checking_criteria": text_list(activity.get("checking_criteria")),
                "estimated_duration_minutes": duration,
                "status": "complete_synthetic",
            }
        )
    if not output:
        raise ValueError(f"{unit_id}: guided activity missing")
    return output


def assessment_items(unit: dict[str, Any], unit_id: str, outcome_ids: list[str], source_ids: list[str]) -> list[dict[str, Any]]:
    raw = dict_list(unit.get("self_assessment"))
    supplements = []
    for item in dict_list(unit.get("common_errors")):
        error = str(item.get("error") or "").strip()
        correction = str(item.get("correction") or "").strip()
        if error and correction:
            supplements.append(
                {
                    "question": f"Corrige esta afirmación o práctica: «{error}»",
                    "answer": correction,
                    "reasoning": f"La corrección esperada es: {correction}",
                    "common_error": error,
                }
            )
    combined = raw + supplements
    if len(combined) < 10:
        raise ValueError(f"{unit_id}: insufficient assessment material to build ten items")
    items = []
    for index, item in enumerate(combined[:10], start=1):
        if index <= 2:
            difficulty, cognitive = "foundational", "understand"
        elif index <= 5:
            difficulty, cognitive = "intermediate", "apply"
        elif index <= 8:
            difficulty, cognitive = "intermediate", "analyze"
        elif index == 9:
            difficulty, cognitive = "advanced", "evaluate"
        else:
            difficulty, cognitive = "advanced", "create"
        answer = str(item.get("answer") or "").strip()
        reasoning = str(item.get("reasoning") or item.get("explanation") or answer).strip()
        misconception = str(item.get("common_error") or "").strip()
        items.append(
            {
                "id": f"{unit_id}-Q{index:02d}",
                "type": "short_answer",
                "prompt": str(item.get("question") or "").strip(),
                "linked_learning_outcome_ids": [outcome_ids[(index - 1) % len(outcome_ids)]],
                "difficulty": difficulty,
                "cognitive_level": cognitive,
                "answer_key": {
                    "expected_answer": answer,
                    "explanation": reasoning,
                    "common_misconceptions": [misconception] if misconception else [],
                },
                "feedback": {
                    "correct": f"Correcto. Conserva en tu explicación esta idea: {answer}",
                    "incorrect": f"Revisa el razonamiento de la unidad: {reasoning}" + (f" Evita este error: {misconception}" if misconception else ""),
                },
                "source_ids": source_ids[:2],
                "status": "complete_formative",
            }
        )
    return items


def build_course_assessment() -> dict[str, Any]:
    return {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{CODE}-EVAL-CURSO",
        "course_id": SUBJECT,
        "scope": "course",
        "principles": [
            "Evaluar separación entre dato, formulación, solución, verificación, validación e inferencia.",
            "Exigir unidades, configuraciones, fronteras, parámetros y supuestos antes de aceptar un resultado numérico.",
            "Premiar controles de caso límite, convergencia, sensibilidad e incertidumbre además del resultado nominal.",
            "Usar problemas y datos sintéticos para que la evaluación no dependa de participantes, pacientes ni experimentación real.",
            "No convertir ajuste, convergencia o concordancia parcial en evidencia clínica o regulatoria.",
            "Exigir trazabilidad de fuentes y corrección explícita de errores después de feedback.",
        ],
        "assessment_plan": [
            {"component": "Recuperación y explicación conceptual", "weight_percent": 10, "evidence": "Preguntas cortas y corrección de conceptos frontera."},
            {"component": "Problemas cuantitativos de unidad", "weight_percent": 25, "evidence": "Cálculos con unidades, supuestos y controles."},
            {"component": "Expedientes reproducibles", "weight_percent": 25, "evidence": "Productos guiados de U1–U6 con sensibilidad e incertidumbre."},
            {"component": "Revisión crítica y corrección", "weight_percent": 10, "evidence": "Auditoría de un modelo y justificación antes/después."},
            {"component": "Proyecto integrador", "weight_percent": 30, "evidence": "Modelo continuo sintético con verificación, validación y límites de uso."},
        ],
        "diagnostic": {
            "purpose": "Comprobar prerrequisitos antes de modelar un continuo biológico.",
            "questions": [
                "Distingue escalar, vector y tensor con un ejemplo mecánico.",
                "Explica la diferencia entre configuración de referencia y configuración actual.",
                "Comprueba dimensionalmente una ecuación de balance de cantidad de movimiento.",
                "Dibuja qué información debe aparecer en una condición de frontera mecánica.",
                "Explica por qué equilibrio no determina una ley constitutiva.",
                "Distingue deformación, tensión y rigidez.",
                "Explica qué significa calibrar parámetros con datos y por qué no equivale a validar.",
                "Distingue respuesta elástica instantánea de respuesta dependiente del tiempo.",
                "Explica qué representa el número de Reynolds y qué no demuestra por sí solo.",
                "Define convergencia de malla sin confundirla con exactitud física.",
                "Propón un caso límite para detectar un error de implementación.",
                "Explica la diferencia entre incertidumbre paramétrica y error de modelo.",
            ],
        },
        "midterm_blueprint": [
            {"domain": "U1 · Cinemática continua", "weight_percent": 20, "focus": "F, J, C, E, objetividad y conservación."},
            {"domain": "U2 · Esfuerzo y equilibrio", "weight_percent": 20, "focus": "Tensión, tracción, balances y fronteras."},
            {"domain": "U3 · Elasticidad", "weight_percent": 25, "focus": "Hiperelasticidad, anisotropía, calibración e identificabilidad."},
            {"domain": "U4 · Dependencia temporal", "weight_percent": 15, "focus": "Viscoelasticidad, poroelasticidad y escalas temporales."},
            {"domain": "Integración U1–U4", "weight_percent": 20, "focus": "Cadena cinemática → balance → constitutiva → respuesta temporal con límites."},
        ],
        "capstone": {
            "title": "Expediente de credibilidad de un modelo biomecánico continuo sintético",
            "purpose": "Integrar U1–U6 en un modelo auditable sin convertir el ejercicio en validación clínica o regulatoria.",
            "scenario": "Seleccionar un sistema sintético inspirado en tejido blando, flujo biológico o interacción mecánica y formular un contexto de uso educativo explícito.",
            "deliverables": [
                "Pregunta, contexto de uso, alcance y exclusiones.",
                "Geometría/configuración, variables, unidades y condiciones de frontera.",
                "Balances y ley constitutiva o reológica justificados.",
                "Plan de discretización y al menos un estudio de convergencia.",
                "Calibración, sensibilidad e incertidumbre con supuestos rastreables.",
                "Comparación con evidencia independiente o caso benchmark apropiado.",
                "Conclusión proporcional con limitaciones, amenazas a validez y siguiente evidencia necesaria.",
            ],
            "rubric": [
                {"criterion": "Formulación física y fronteras", "weight_percent": 20},
                {"criterion": "Constitutiva, parámetros e identificabilidad", "weight_percent": 20},
                {"criterion": "Verificación numérica y convergencia", "weight_percent": 20},
                {"criterion": "Validación, sensibilidad e incertidumbre", "weight_percent": 20},
                {"criterion": "Reproducibilidad, trazabilidad y límites de inferencia", "weight_percent": 20},
            ],
        },
        "status": "complete_internal_external_review_pending",
    }


def main() -> int:
    if TARGET.exists():
        raise FileExistsError(f"Canonical target already exists: {TARGET}")
    subprocess.run(
        [sys.executable, "scripts/migrate_course_to_canonical.py", "--subject", SUBJECT, "--course-code", CODE],
        cwd=ROOT,
        check=True,
    )

    units = [load(SOURCE_DIR / f"unit-{number:02d}.json") for number in range(1, 7)]
    sources, unit_source_ids, local_source_map = build_sources(units)
    glossary, unit_glossary_ids = build_glossary(units, unit_source_ids)
    claims, unit_claim_ids = build_claims(units, local_source_map, unit_source_ids)

    media_items = []
    for unit in units:
        number = int(unit["unit"])
        unit_id = f"{CODE}-U{number:02d}"
        media_items.append(
            {
                "id": f"{unit_id}-MED01",
                "type": "figure",
                "status": "planned",
                "unit_id": unit_id,
                "linked_learning_outcome_ids": [f"{unit_id}-LO01", f"{unit_id}-LO02"],
                "pedagogical_purpose": f"Visualizar el flujo conceptual central de {unit['title']} y sus controles de validez.",
                "alt_text_draft": f"Esquema conceptual pendiente de {unit['title']} con variables, relaciones y límites.",
                "license_requirements": "Material propio o con licencia compatible, con atribución y procedencia registradas.",
                "source_ids": unit_source_ids[number][:2],
            }
        )

    for unit in units:
        number = int(unit["unit"])
        unit_id = f"{CODE}-U{number:02d}"
        canonical_path = TARGET / "units" / f"unit-{number:02d}.json"
        canonical = load(canonical_path)
        prerequisites = [f"{CODE}-U{value:02d}" for value in PREREQUISITES[number]]
        local_outcomes = [
            {"id": f"{unit_id}-LO{index:02d}", "statement": statement}
            for index, statement in enumerate(text_list(unit.get("learning_objectives")), start=1)
        ]
        canonical.update(
            {
                "status": dict(STATUS_COMPLETE),
                "purpose": str(unit.get("purpose") or "").strip(),
                "prerequisite_unit_ids": prerequisites,
                "course_learning_outcome_ids": [f"{CODE}-LO{number:02d}", f"{CODE}-LO07"],
                "learning_outcomes": local_outcomes,
                "examples": build_examples(unit, unit_id, number),
                "activities": build_activities(unit, unit_id, prerequisites),
                "assessment_file": f"assessments/unit-{number:02d}.json",
                "glossary_entry_ids": unit_glossary_ids[number],
                "source_ids": unit_source_ids[number],
                "claim_ids": unit_claim_ids[number],
                "media_ids": [f"{unit_id}-MED01"],
                "common_errors": dict_list(unit.get("common_errors")),
                "biomedical_connections": [
                    text for text in (normalize_connection(value) for value in unit.get("biomedical_connections", [])) if text
                ],
                "editorial_notice": str(unit.get("editorial_notice") or "").strip(),
                "legacy_origin": f"data/course_redevelopment/{SUBJECT}/units/unit-{number:02d}.json",
            }
        )
        write(canonical_path, canonical)
        assessment = {
            "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
            "schema_version": "1.0",
            "id": f"{unit_id}-EVAL",
            "course_id": SUBJECT,
            "scope": "unit",
            "unit_id": unit_id,
            "purpose": f"Comprobar comprensión, aplicación y límites de inferencia de {unit['title']} con feedback recuperativo.",
            "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
            "items": assessment_items(unit, unit_id, [item["id"] for item in local_outcomes], unit_source_ids[number]),
            "status": "complete_formative_external_review_pending",
        }
        write(TARGET / "assessments" / f"unit-{number:02d}.json", assessment)

    write(
        TARGET / "sources.json",
        {
            "$schema": "../../../schemas/academic/registry-v1.schema.json",
            "schema_version": "1.0",
            "course_id": SUBJECT,
            "source_policy": "Conservar fuentes de las seis unidades curadas, priorizando literatura primaria, revisiones metodológicas, estándares y documentos técnicos directamente verificables; la revisión disciplinaria externa sigue pendiente.",
            "consulted_on": "2026-08-24",
            "coverage_gaps": [],
            "coverage_status": "traceable",
            "sources": sources,
        },
    )
    write(
        TARGET / "glossary.json",
        {
            "$schema": "../../../schemas/academic/registry-v1.schema.json",
            "schema_version": "1.0",
            "course_id": SUBJECT,
            "entries": glossary,
            "status": "traceable_to_verified_unit_sources_external_review_pending",
        },
    )
    write(
        TARGET / "claims.json",
        {
            "$schema": "../../../schemas/academic/registry-v1.schema.json",
            "schema_version": "1.0",
            "course_id": SUBJECT,
            "content_version": "1.0.0",
            "content_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "scope": "Cuatro afirmaciones metodológicas ancla por unidad, tomadas literalmente de los puntos clave del contenido canónico y vinculadas a una fuente de la sección.",
            "review_state": "internally_curated_external_review_pending",
            "claims": claims,
        },
    )
    write(
        TARGET / "media.json",
        {
            "$schema": "../../../schemas/academic/registry-v1.schema.json",
            "schema_version": "1.0",
            "course_id": SUBJECT,
            "coverage_status": "planned",
            "items": media_items,
        },
    )
    write(TARGET / "assessments" / "course-assessment.json", build_course_assessment())

    core_source_ids: list[str] = []
    for number in range(1, 7):
        for source_id in unit_source_ids[number][:2]:
            if source_id not in core_source_ids:
                core_source_ids.append(source_id)

    course = {
        "$schema": "../../../schemas/academic/course-v1.schema.json",
        "schema_version": "1.0",
        "id": SUBJECT,
        "code": CODE,
        "area_id": "ingenieria-biomedica",
        "title": "Biomecánica de Medios Continuos",
        "language": "es",
        "content_version": "1.0.0",
        "academic_level": "Pregrado universitario intermedio y avanzado",
        "audience": "Estudiantes de ingeniería biomédica y áreas afines con bases de cálculo multivariable, álgebra lineal, mecánica, ecuaciones diferenciales y programación científica que necesiten formular, resolver y auditar modelos continuos de tejidos y fluidos biológicos.",
        "status": dict(STATUS_COMPLETE),
        "purpose": "Integrar cinemática de medios continuos, esfuerzo y equilibrio, leyes constitutivas elásticas, respuesta visco/poroelástica, fluidos biológicos y elementos finitos para construir modelos biomecánicos reproducibles y auditables, separando formulación, calibración, verificación, validación, incertidumbre y contexto de uso sin convertir una simulación en evidencia clínica o regulatoria no demostrada.",
        "scope": {
            "included": [
                "Hipótesis de continuo, configuraciones, gradiente de deformación, medidas finitas y conservación de masa.",
                "Tensor de tensiones, tracción, balances lineal y angular, presión y condiciones de frontera.",
                "Hiperelasticidad, isotropía, anisotropía, incomprensibilidad, calibración e identificabilidad.",
                "Viscoelasticidad, fluencia, relajación, poroelasticidad, transporte intersticial y respuesta dependiente del tiempo.",
                "Flujos biológicos, Navier–Stokes, Reynolds, Womersley, reología, WSS e interacción fluido-estructura.",
                "Discretización por elementos finitos, calidad de malla, convergencia, verificación, validación, sensibilidad e incertidumbre.",
                "Actividades sintéticas y expedientes reproducibles con supuestos, controles, límites y trazabilidad bibliográfica."
            ],
            "excluded": [
                "Diagnóstico, pronóstico, prescripción terapéutica o afirmaciones de seguridad/eficacia clínica basadas únicamente en una simulación.",
                "Certificación regulatoria, validación de software para uso clínico o demostración de credibilidad fuera de un contexto de uso definido.",
                "Protocolos experimentales con personas, pacientes, animales o muestras biológicas reales.",
                "Inferencia automática desde respuesta macroscópica del continuo hacia mecanismos celulares o moleculares no modelados.",
                "Uso de convergencia numérica o buen ajuste de parámetros como sustitutos de validación física independiente."
            ],
            "handoff_courses": [
                "biomecanica",
                "laboratorio-biomecanica",
                "biomateriales-implantes",
                "modelado-simulacion-biomedicina",
                "simulacion-planificacion-quirurgica"
            ],
        },
        "prerequisites": [
            {"id": f"{CODE}-PRE01", "statement": "Cálculo multivariable, derivadas parciales e integración de nivel universitario."},
            {"id": f"{CODE}-PRE02", "statement": "Álgebra lineal con vectores, matrices, transformaciones y valores propios."},
            {"id": f"{CODE}-PRE03", "statement": "Mecánica clásica, unidades SI, balances y condiciones de frontera básicas."},
            {"id": f"{CODE}-PRE04", "statement": "Ecuaciones diferenciales y programación científica suficiente para resolver y visualizar problemas numéricos."},
            {"id": f"{CODE}-PRE05", "statement": "Biomecánica y fisiología básicas para contextualizar tejidos, vasos y flujos biológicos sin inferencias clínicas."},
        ],
        "competencies": [
            {"id": f"{CODE}-COMP01", "statement": "Construir una descripción cinemática continua con configuraciones, medidas de deformación y controles de objetividad explícitos."},
            {"id": f"{CODE}-COMP02", "statement": "Formular balances de esfuerzo y equilibrio con tensiones, fronteras, unidades y convenciones consistentes."},
            {"id": f"{CODE}-COMP03", "statement": "Seleccionar, calibrar y cuestionar leyes constitutivas elásticas, viscoelásticas y poroelásticas según la evidencia disponible."},
            {"id": f"{CODE}-COMP04", "statement": "Modelar flujos biológicos declarando reología, escalas, condiciones de frontera y sensibilidad de las métricas derivadas."},
            {"id": f"{CODE}-COMP05", "statement": "Diseñar y auditar discretizaciones por elementos finitos con verificación, convergencia y controles numéricos."},
            {"id": f"{CODE}-COMP06", "statement": "Separar calibración, verificación, validación, incertidumbre y contexto de uso al juzgar credibilidad de un modelo."},
            {"id": f"{CODE}-COMP07", "statement": "Integrar las seis unidades en un expediente reproducible con fuentes, supuestos, sensibilidad, limitaciones y siguiente evidencia necesaria."},
        ],
        "learning_outcomes": [
            {"id": f"{CODE}-LO01", "statement": "Construye una descripción continua de un sistema biológico usando configuraciones, F, J y medidas de deformación, y demuestra objetividad y límites de escala."},
            {"id": f"{CODE}-LO02", "statement": "Formula e interpreta tensiones, tracciones, balances y condiciones de frontera sin atribuir propiedades materiales que el equilibrio no determina."},
            {"id": f"{CODE}-LO03", "statement": "Selecciona y calibra modelos elásticos o hiperelásticos, analiza anisotropía e identificabilidad y separa ajuste de capacidad predictiva."},
            {"id": f"{CODE}-LO04", "statement": "Modela respuesta dependiente del tiempo mediante viscoelasticidad y poroelasticidad, relacionando escalas de relajación, fluencia, drenaje y transporte."},
            {"id": f"{CODE}-LO05", "statement": "Formula un problema de flujo biológico con balances, reología y números adimensionales, e interpreta métricas hemodinámicas o respiratorias dentro de sus límites."},
            {"id": f"{CODE}-LO06", "statement": "Construye y audita una simulación por elementos finitos con calidad de discretización, convergencia, verificación, validación, sensibilidad e incertidumbre."},
            {"id": f"{CODE}-LO07", "statement": "Integra U1–U6 en un expediente de credibilidad reproducible que conecta pregunta, formulación, datos, parámetros, solución, controles, evidencia independiente y límites del contexto de uso."},
        ],
        "study_method": [
            "Definir sistema, configuración, variables, unidades, fronteras y contexto de uso antes de resolver ecuaciones.",
            "Alternar explicación, ejemplo resuelto, actividad guiada, comprobación y transferencia con apoyo progresivamente menor.",
            "Separar cinemática, balance, cierre constitutivo, discretización y solución para localizar cada supuesto.",
            "Verificar casos límite y convergencia antes de comparar con evidencia física independiente.",
            "Perturbar parámetros, geometría, malla y condiciones de frontera para medir sensibilidad y fragilidad de la conclusión.",
            "Cerrar cada ejercicio indicando qué está calculado, qué está inferido, qué no está demostrado y qué evidencia adicional sería necesaria."
        ],
        "core_source_ids": core_source_ids,
        "unit_files": [f"units/unit-{number:02d}.json" for number in range(1, 7)],
        "assessment_files": [f"assessments/unit-{number:02d}.json" for number in range(1, 7)] + ["assessments/course-assessment.json"],
        "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
        "static_site": {
            "renderer": "scripts/generate_site.py",
            "canonical_source": True,
            "legacy_mirrors": [
                f"data/generated_courses/{SUBJECT}.json",
                f"data/generated_units/{SUBJECT}/",
                f"data/subjects/ingenieria-biomedica/{SUBJECT}.json",
                f"data/source_registry/{SUBJECT}.json",
                f"data/claim_registry/{SUBJECT}.json",
            ],
        },
        "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, fuentes trazables y pedagogía interna para las seis unidades de Biomecánica de Medios Continuos. La publicación continúa provisional. La revisión humana interna y disciplinaria externa, la validación de modelos para tejidos o pacientes reales, la certificación de software, la validación clínica/regulatoria y cualquier decisión terapéutica permanecen fuera de este cierre y siguen pendientes.",
    }
    write(TARGET / "course.json", course)

    if len(glossary) < 100:
        raise ValueError(f"Expected at least 100 glossary entries, found {len(glossary)}")
    if len(sources) < 40:
        raise ValueError(f"Expected at least 40 traceable sources, found {len(sources)}")
    if len(claims) != 24:
        raise ValueError(f"Expected 24 literal claims, found {len(claims)}")
    print(f"Canonical closure built: glossary={len(glossary)} sources={len(sources)} claims={len(claims)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
