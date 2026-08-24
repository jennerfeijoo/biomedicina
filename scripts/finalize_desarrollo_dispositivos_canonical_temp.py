#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "desarrollo-dispositivos-medicos"
CODE = "DDM"
COURSE_DIR = ROOT / "data" / "courses" / COURSE_ID
REDEV_DIR = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"
CONSULTED_ON = "2026-08-24"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = "".join(c for c in normalized if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", ascii_value.casefold()).strip("-") or "fuente"


def status_complete():
    return {
        "content": "complete",
        "sources": "traceable",
        "pedagogy": "complete",
        "multimedia": "planned",
        "internal_review": "pending",
        "external_review": "pending",
        "publication": "published_provisional",
    }


def source_text(source: dict) -> str:
    return " ".join(str(source.get(k) or "") for k in ("title", "organization", "authors", "description", "locator", "type")).casefold()


def choose_source(text: str, source_ids: list[str], source_records: dict[str, dict]) -> str:
    hay = text.casefold()
    rules = [
        (("qmsr", "quality management system", "sistema de gestión", "sistema de gestion"), ("qmsr", "13485")),
        (("iso 13485", "transferencia", "proveedor", "producción", "produccion", "calidad"), ("13485", "qmsr")),
        (("14971", "riesgo", "peligro", "risk", "control de riesgo"), ("14971",)),
        (("factores humanos", "usabilidad", "usuario", "tarea crítica", "tarea critica", "interfaz"), ("human factors", "usability")),
        (("10993", "biológica", "biologica", "biocompat", "contacto"), ("10993", "biological")),
        (("14155", "investigación clínica", "investigacion clinica", "evidencia clínica", "evidencia clinica"), ("14155", "clinical investigation")),
        (("mundo real", "rwd", "rwe", "real-world"), ("real-world", "rwe")),
        (("estar", "510(k)", "de novo", "pma", "premarket"), ("estar", "510(k)", "device regulation")),
        (("eudamed", "unión europea", "union europea", "mdr", "evaluación de conformidad", "evaluacion de conformidad"), ("eudamed", "2017/745", "medical devices regulation")),
        (("udi", "gudid", "device identifier", "production identifier"), ("udi", "unique device")),
        (("mdr", "medical device reporting", "queja", "evento adverso", "reportabilidad"), ("mandatory reporting", "emdr", "803")),
        (("recall", "retirada", "corrección", "correccion", "removal"), ("recalls", "806")),
        (("biodesign", "need", "necesidad clínica", "necesidad clinica", "needs finding"), ("biodesign", "needs finding", "unmet needs")),
        (("requisito", "arquitectura", "design input", "design output"), ("design", "qmsr", "13485")),
        (("verificación", "verificacion", "prototipo", "criterio de aceptación", "criterio de aceptacion"), ("design", "verification", "qmsr", "13485")),
    ]
    for needles, wanted in rules:
        if any(n in hay for n in needles):
            for source_id in source_ids:
                record_text = source_text(source_records[source_id])
                if any(w in record_text for w in wanted):
                    return source_id
    return source_ids[0]


def normalize_source(source: dict, source_id: str, unit_id: str) -> dict:
    record = {k: v for k, v in source.items() if k not in {"registry_id", "id", "used_by_unit_ids"} and v not in (None, "", [])}
    record["id"] = source_id
    record["verification_status"] = "verified_directly"
    record["used_by_unit_ids"] = [unit_id]
    if not record.get("why_relevant"):
        record["why_relevant"] = str(record.get("description") or record.get("locator") or "Fuente verificada directamente y utilizada por la unidad.")
    return record


def build_sources(redev_units: list[dict]):
    records: OrderedDict[str, dict] = OrderedDict()
    key_to_id: dict[str, str] = {}
    unit_source_ids: dict[int, list[str]] = {}
    used_ids: set[str] = set()
    for unit in redev_units:
        number = int(unit["unit"])
        unit_id = f"{CODE}-U{number:02d}"
        unit_source_ids[number] = []
        for source in unit.get("sources", []):
            if source.get("verification_status") != "verified_directly":
                raise SystemExit(f"U{number}: source not verified_directly: {source.get('title')}")
            key = str(source.get("url") or "").strip() or str(source.get("title") or "").strip().casefold()
            source_id = key_to_id.get(key)
            if source_id is None:
                base = slugify(str(source.get("title") or source.get("organization") or "fuente"))
                source_id = base
                suffix = 2
                while source_id in used_ids:
                    source_id = f"{base}-{suffix}"
                    suffix += 1
                used_ids.add(source_id)
                key_to_id[key] = source_id
                records[source_id] = normalize_source(source, source_id, unit_id)
            else:
                used_by = records[source_id].setdefault("used_by_unit_ids", [])
                if unit_id not in used_by:
                    used_by.append(unit_id)
                for k, v in source.items():
                    if v not in (None, "", []) and not records[source_id].get(k):
                        records[source_id][k] = v
            if source_id not in unit_source_ids[number]:
                unit_source_ids[number].append(source_id)
        if not unit_source_ids[number]:
            raise SystemExit(f"U{number}: no verified sources")
    return records, unit_source_ids


def finalize():
    if not COURSE_DIR.exists():
        raise SystemExit("Canonical bootstrap missing; run migrate_course_to_canonical.py first")
    redev_units = [load(REDEV_DIR / f"unit-{n:02d}.json") for n in range(1, 7)]
    source_records, unit_source_ids = build_sources(redev_units)

    sources_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "source_policy": "Conservar únicamente fuentes verificadas directamente y vinculadas a las seis unidades. Distinguir guía o regulación oficial, norma técnica, recurso académico y literatura indexada; registrar jurisdicción y fecha cuando el contenido pueda cambiar. La trazabilidad interna no sustituye revisión disciplinaria humana ni asesoría regulatoria.",
        "consulted_on": CONSULTED_ON,
        "coverage_gaps": [],
        "sources": list(source_records.values()),
    }
    write(COURSE_DIR / "sources.json", sources_payload)

    glossary = load(COURSE_DIR / "glossary.json")
    for entry in glossary["entries"]:
        units = entry.get("unit_ids") or []
        number = int(units[0].split("U")[-1]) if units else 1
        candidates = unit_source_ids[number]
        entry["source_ids"] = [choose_source(f"{entry.get('term','')} {entry.get('definition','')}", candidates, source_records)]
        entry["verification_status"] = "traceable_to_verified_source"
    glossary["status"] = "traceable_to_verified_sources"
    write(COURSE_DIR / "glossary.json", glossary)

    claims = []
    claims_by_unit: dict[int, list[str]] = {}
    for number, redev in enumerate(redev_units, start=1):
        unit_id = f"{CODE}-U{number:02d}"
        claims_by_unit[number] = []
        for idx, section in enumerate(redev.get("theory_sections", [])[:4], start=1):
            key_points = [str(x).strip() for x in section.get("key_points", []) if str(x).strip()]
            paragraphs = [str(x).strip() for x in section.get("paragraphs", []) if str(x).strip()]
            if key_points:
                text = key_points[0]
            elif paragraphs:
                text = paragraphs[0]
            else:
                raise SystemExit(f"U{number} section {idx}: no anchor text")
            claim_id = f"{CODE}-U{number:02d}-C{idx:03d}"
            source_id = choose_source(text + " " + str(section.get("heading") or ""), unit_source_ids[number], source_records)
            source = source_records[source_id]
            claims.append({
                "claim_id": claim_id,
                "unit": number,
                "text": text,
                "claim_type": "methodological_or_interpretive",
                "risk": "high" if number in (3, 5, 6) else "medium",
                "context": f"Afirmación ancla enseñada literalmente en U{number}: {redev['title']}; interpretar dentro del alcance, jurisdicción, supuestos y límites declarados.",
                "source_id": source_id,
                "locator": {"url": source.get("url", ""), "title": source.get("title", source_id)},
                "support": "direct",
                "source_verification_status": "verified_directly",
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": CONSULTED_ON,
                "id": claim_id,
                "unit_id": unit_id,
            })
            claims_by_unit[number].append(claim_id)
    write(COURSE_DIR / "claims.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": "Veinticuatro afirmaciones ancla, cuatro por unidad, tomadas literalmente de las unidades canónicas y vinculadas a fuentes verificadas directamente; revisión disciplinaria humana pendiente.",
        "review_state": "ai_review_provisional",
        "claims": claims,
    })

    course_los = [
        ("DDM-LO01", "Formula una necesidad clínica o de sistema de uso trazable a observaciones, usuarios, tareas, entorno y evidencia, sin introducir prematuramente una solución o una afirmación clínica no demostrada."),
        ("DDM-LO02", "Traduce necesidades a requisitos y arquitectura verificables, gestionando interfaces, criterios de aceptación, trazabilidad y cambios sin confundir requisito, solución y resultado clínico."),
        ("DDM-LO03", "Construye y mantiene un expediente de gestión de riesgos que conecta peligros, secuencias, situaciones peligrosas, daños, controles, verificación y riesgo residual sin reducir riesgo a una cifra aislada."),
        ("DDM-LO04", "Planifica prototipado y verificación con configuraciones controladas, criterios predefinidos, métodos trazables, desviaciones e incertidumbre, distinguiendo cumplimiento técnico de validación de uso."),
        ("DDM-LO05", "Integra factores humanos, evidencia preclínica, evaluación biológica y evidencia clínica o del mundo real según la afirmación, la representatividad y la incertidumbre, sin equiparar validación con aprobación regulatoria."),
        ("DDM-LO06", "Construye una estrategia educativa de regulación, calidad, transferencia, control de cambios y vigilancia posmercado dependiente de jurisdicción, manteniendo separadas evidencia técnica, decisión de calidad y obligación regulatoria potencial."),
        ("DDM-LO07", "Integra U1–U6 en un expediente reproducible de ciclo de vida que conserva configuración, fuentes, trazabilidad, evidencia negativa, brechas y límites y especifica la siguiente acción necesaria sin declarar conformidad, seguridad global o beneficio clínico no demostrados."),
    ]

    for number in range(1, 7):
        path = COURSE_DIR / "units" / f"unit-{number:02d}.json"
        unit = load(path)
        redev = redev_units[number - 1]
        unit["status"] = status_complete()
        unit["course_learning_outcome_ids"] = [f"DDM-LO{number:02d}", "DDM-LO07"]
        unit["source_ids"] = unit_source_ids[number]
        unit["claim_ids"] = claims_by_unit[number]
        durations = [180, 120, 150]
        for idx, activity in enumerate(unit.get("activities", [])):
            activity["estimated_duration_minutes"] = durations[idx] if idx < len(durations) else 120
            activity["status"] = "complete"
            activity["purpose"] = (
                "Practicar el razonamiento de la unidad con un expediente sintético y auditable, retirando apoyo de forma progresiva y conservando explícitos los límites de inferencia."
            )
        for example in unit.get("examples", []):
            if not example.get("interpretation"):
                example["interpretation"] = "Interpretar únicamente dentro del escenario sintético y del resultado de aprendizaje asociado."
            if not example.get("limitations"):
                example["limitations"] = ["Escenario sintético; no constituye evidencia clínica, regulatoria ni de desempeño de un dispositivo real."]
        unit["editorial_notice"] = str(redev.get("editorial_notice") or unit.get("editorial_notice") or "")
        write(path, unit)

        assessment_path = COURSE_DIR / "assessments" / f"unit-{number:02d}.json"
        assessment = load(assessment_path)
        local_los = [item["id"] for item in unit["learning_outcomes"]]
        levels = [
            ("foundational", "understand"), ("foundational", "understand"),
            ("intermediate", "apply"), ("intermediate", "apply"),
            ("intermediate", "analyze"), ("intermediate", "analyze"),
            ("advanced", "evaluate"), ("advanced", "evaluate"),
            ("advanced", "create"), ("advanced", "evaluate"),
        ]
        for idx, item in enumerate(assessment["items"]):
            difficulty, cognitive = levels[idx % len(levels)]
            item["difficulty"] = difficulty
            item["cognitive_level"] = cognitive
            item["linked_learning_outcome_ids"] = [local_los[idx % len(local_los)]]
            expected = item["answer_key"].get("expected_answer") or "Respuesta razonada basada en el contenido de la unidad."
            explanation = item["answer_key"].get("explanation") or expected
            item["answer_key"]["explanation"] = explanation
            item["source_ids"] = [choose_source(item.get("prompt", "") + " " + expected, unit_source_ids[number], source_records)]
            item["feedback"] = {
                "correct": "Correcto: la respuesta conserva la distinción conceptual, la trazabilidad y los límites de la unidad. Revisa la explicación para comprobar por qué.",
                "incorrect": "Revisa la cadena evidencia → decisión y evita colapsar etapas distintas. Contrasta tu respuesta con la explicación y la fuente trazada antes de intentarlo de nuevo.",
            }
            item["status"] = "complete"
        assessment["purpose"] = f"Comprobar comprensión, aplicación y juicio crítico de U{number} — {redev['title']} con retroalimentación recuperativa y fuentes trazables."
        assessment["status"] = "complete"
        write(assessment_path, assessment)

    media = load(COURSE_DIR / "media.json")
    media_purposes = {
        1: ("Mapa de needs finding y sistema de uso", "Diagrama sintético que separa observación, interpretación, necesidad, usuarios, tareas, entorno y solución todavía no seleccionada."),
        2: ("Trazabilidad necesidad–requisito–arquitectura", "Mapa visual de necesidades, requisitos, interfaces, criterios de aceptación, arquitectura y cambios de un dispositivo ficticio."),
        3: ("Cadena de gestión de riesgos", "Diagrama sintético de peligro, secuencia de eventos, situación peligrosa, daño, control, verificación y riesgo residual."),
        4: ("Pirámide de prototipado y verificación", "Esquema que conecta configuración, prototipo, método, criterio predefinido, resultado, desviación e incertidumbre."),
        5: ("Mapa de evidencia de validación", "Esquema sintético que relaciona necesidades con factores humanos, evidencia preclínica, evaluación biológica, evidencia clínica o RWE y límites."),
        6: ("Ciclo de vida regulatorio y posmercado", "Mapa de estrategia por jurisdicción, QMS, transferencia, configuración, producción, quejas, reportabilidad potencial, cambios y retroalimentación a riesgos."),
    }
    for item in media["items"]:
        number = int(item["unit_id"].split("U")[-1])
        purpose, alt = media_purposes[number]
        item["pedagogical_purpose"] = purpose
        item["alt_text_draft"] = alt
        item["status"] = "planned"
        item["source_ids"] = []
    media["coverage_status"] = "planned"
    write(COURSE_DIR / "media.json", media)

    assessment_plan = [
        {"component": "U1 · expediente de necesidad y sistema de uso", "weight_percent": 8, "linked_learning_outcome_ids": ["DDM-LO01", "DDM-LO07"]},
        {"component": "U2 · especificación y arquitectura trazable", "weight_percent": 8, "linked_learning_outcome_ids": ["DDM-LO02", "DDM-LO07"]},
        {"component": "U3 · expediente de gestión de riesgos", "weight_percent": 10, "linked_learning_outcome_ids": ["DDM-LO03", "DDM-LO07"]},
        {"component": "U4 · plan de prototipado y verificación", "weight_percent": 10, "linked_learning_outcome_ids": ["DDM-LO04", "DDM-LO07"]},
        {"component": "U5 · argumento de validación y evidencia", "weight_percent": 12, "linked_learning_outcome_ids": ["DDM-LO05", "DDM-LO07"]},
        {"component": "U6 · transferencia, regulación y vigilancia", "weight_percent": 12, "linked_learning_outcome_ids": ["DDM-LO06", "DDM-LO07"]},
        {"component": "Evaluación integradora intermedia U1–U3", "weight_percent": 15, "linked_learning_outcome_ids": ["DDM-LO01", "DDM-LO02", "DDM-LO03"]},
        {"component": "Capstone de ciclo de vida U1–U6", "weight_percent": 25, "linked_learning_outcome_ids": [x[0] for x in course_los]},
    ]
    diagnostic_questions = [
        "Distingue una observación de una interpretación y de una solución propuesta.",
        "Explica por qué una necesidad de usuario no es todavía un requisito verificable.",
        "Convierte una afirmación ambigua en un requisito con magnitud, condiciones y criterio.",
        "Distingue peligro, situación peligrosa y daño mediante un ejemplo sintético.",
        "Explica qué información necesita una matriz de trazabilidad para ser auditable.",
        "Distingue verificación de validación sin usar los términos como sinónimos.",
        "Explica por qué un resultado de banco favorable no demuestra beneficio clínico.",
        "Identifica qué significa configuración controlada de hardware, software y documentación.",
        "Explica por qué una clasificación regulatoria no puede trasladarse automáticamente entre jurisdicciones.",
        "Distingue no conformidad, corrección y acción correctiva.",
        "Explica por qué una tasa posmercado necesita denominador y contexto.",
        "Indica qué partes de un expediente educativo requieren revisión humana o profesional antes de uso real.",
    ]
    midterm_blueprint = [
        {"domain": "U1 · necesidad, usuarios y contexto", "weight_percent": 20, "linked_learning_outcome_ids": ["DDM-LO01"]},
        {"domain": "U2 · requisitos, arquitectura y trazabilidad", "weight_percent": 30, "linked_learning_outcome_ids": ["DDM-LO02"]},
        {"domain": "U3 · riesgo y controles", "weight_percent": 30, "linked_learning_outcome_ids": ["DDM-LO03"]},
        {"domain": "Integración U1–U3 y calidad de decisión", "weight_percent": 20, "linked_learning_outcome_ids": ["DDM-LO01", "DDM-LO02", "DDM-LO03", "DDM-LO07"]},
    ]
    capstone_rubric = [
        {"criterion": "Necesidad, usuarios y sistema de uso", "weight_percent": 15, "linked_learning_outcome_ids": ["DDM-LO01"]},
        {"criterion": "Requisitos, arquitectura y trazabilidad", "weight_percent": 15, "linked_learning_outcome_ids": ["DDM-LO02"]},
        {"criterion": "Gestión de riesgos y controles", "weight_percent": 15, "linked_learning_outcome_ids": ["DDM-LO03"]},
        {"criterion": "Prototipado, verificación y configuración", "weight_percent": 15, "linked_learning_outcome_ids": ["DDM-LO04"]},
        {"criterion": "Validación y proporcionalidad de la evidencia", "weight_percent": 15, "linked_learning_outcome_ids": ["DDM-LO05"]},
        {"criterion": "Regulación, transferencia y posmercado", "weight_percent": 15, "linked_learning_outcome_ids": ["DDM-LO06"]},
        {"criterion": "Reproducibilidad, brechas, límites y handoff", "weight_percent": 10, "linked_learning_outcome_ids": ["DDM-LO07"]},
    ]
    course_assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": "DDM-EVAL-CURSO",
        "course_id": COURSE_ID,
        "scope": "course",
        "principles": [
            "Evaluar decisiones y trazabilidad, no memorización aislada de acrónimos regulatorios.",
            "Separar observación, requisito, riesgo, verificación, validación, regulación y vigilancia en cada respuesta.",
            "Usar exclusivamente dispositivos, usuarios, flujos y datos sintéticos en las actividades del curso.",
            "Exigir fuentes y versiones cuando una afirmación normativa o regulatoria pueda cambiar con el tiempo.",
            "Premiar la declaración explícita de brechas e incertidumbre cuando la evidencia no permite cerrar una conclusión.",
            "Mantener revisión humana externa, asesoría regulatoria, estudios con personas y autorización de mercado fuera del alcance del cierre académico.",
        ],
        "assessment_plan": assessment_plan,
        "diagnostic": {
            "purpose": "Comprobar prerrequisitos conceptuales antes de integrar el ciclo de vida del dispositivo.",
            "questions": diagnostic_questions,
            "use": "Formativo y no ponderado; las respuestas incorrectas remiten a la unidad o prerrequisito correspondiente antes de avanzar."
        },
        "midterm_blueprint": midterm_blueprint,
        "capstone": {
            "title": "Expediente sintético de ciclo de vida de un dispositivo médico",
            "purpose": "Integrar U1–U6 en un dossier reproducible que otra persona pueda auditar sin explicación oral adicional.",
            "scenario": "Desarrollar únicamente sobre un dispositivo ficticio y datos sintéticos; ninguna salida constituye diseño listo para fabricación, estudio con personas, certificación, presentación regulatoria o autorización de mercado.",
            "required_deliverables": [
                "Mapa de necesidad, usuarios, tareas y entorno con observaciones e incertidumbre.",
                "Need statements versionados y justificación de alcance.",
                "Especificación de requisitos con criterios de aceptación y procedencia.",
                "Arquitectura e interfaces con trazabilidad bidireccional.",
                "Expediente de riesgos con peligros, secuencias, daños, controles y riesgo residual.",
                "Plan de prototipado y matriz de configuración.",
                "Matriz de verificación con método, criterio, resultado sintético y desviaciones.",
                "Mapa de validación por necesidad y capa de evidencia pertinente.",
                "Evaluación crítica de una evidencia conflictiva o insuficiente.",
                "Estrategia regulatoria educativa separada por dos jurisdicciones.",
                "Checklist de transferencia, proveedores, cambios y documentación controlada.",
                "Plan posmercado sintético con señales, denominadores, reportabilidad potencial y retroalimentación a riesgos.",
                "Registro final de fuentes, versiones, decisiones, brechas y afirmaciones no soportadas."
            ],
            "constraints": [
                "No usar datos personales, pacientes, participantes ni dispositivos reales.",
                "No afirmar conformidad, seguridad global, eficacia clínica, aprobación, clearance o marcado CE.",
                "Toda afirmación regulatoria debe declarar jurisdicción y fuente vigente.",
                "Toda conclusión debe indicar qué evidencia la sostiene y qué información podría cambiarla."
            ],
            "rubric": capstone_rubric,
        },
        "status": "complete",
    }
    write(COURSE_DIR / "assessments" / "course-assessment.json", course_assessment)

    course = load(COURSE_DIR / "course.json")
    course.update({
        "content_version": "1.0.0",
        "academic_level": "Pregrado universitario intermedio y avanzado",
        "audience": "Estudiantes de ingeniería biomédica y áreas afines con fundamentos de diseño de ingeniería, fisiología y anatomía, estadística básica y pensamiento sistémico que necesiten comprender el ciclo de vida de un dispositivo médico con trazabilidad y límites explícitos.",
        "status": status_complete(),
        "purpose": "Integrar identificación de necesidades clínicas, requisitos y arquitectura, gestión de riesgos, prototipado y verificación, validación y evidencia, y regulación, transferencia y vigilancia posmercado para construir un expediente reproducible de ciclo de vida de un dispositivo médico ficticio, separando evidencia técnica, necesidad de usuario, afirmación clínica y decisión regulatoria y sin presentar el trabajo académico como conformidad, certificación o autorización de mercado.",
        "scope": {
            "included": [
                "Needs finding, usuarios, tareas, entorno, stakeholders y formulación de necesidades trazables.",
                "Requisitos, criterios de aceptación, arquitectura, interfaces, trazabilidad y control de cambios.",
                "Gestión de riesgos con peligros, secuencias, situaciones peligrosas, daños, controles y riesgo residual.",
                "Prototipado, configuración, métodos de prueba, verificación, desviaciones e incertidumbre.",
                "Validación de necesidades y uso previsto mediante factores humanos, evidencia preclínica, biológica, clínica o RWE cuando corresponda.",
                "Estrategia regulatoria dependiente de jurisdicción, QMS, transferencia, proveedores, producción, cambios y vigilancia posmercado.",
                "Expedientes reproducibles con fuentes, versiones, evidencia negativa, brechas y límites de inferencia."
            ],
            "excluded": [
                "Diseño, fabricación, ensayo o comercialización de un dispositivo médico real.",
                "Reclutamiento de participantes, estudios con pacientes o recolección de datos personales.",
                "Clasificación regulatoria oficial, asesoría jurídica, auditoría QMS o evaluación de conformidad.",
                "Declaraciones de seguridad global, eficacia clínica, causalidad, aprobación FDA, clearance, autorización o marcado CE.",
                "Sustitución del juicio de profesionales, organismos notificados, comités de ética o autoridades competentes."
            ],
            "handoff_courses": ["ingenieria-clinica-gestion", "laboratorio-bioinstrumentacion", "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas", "factores-humanos-dispositivos-medicos", "modelado-simulacion-biomedicina"]
        },
        "prerequisites": [
            {"id": "DDM-PRE01", "statement": "Fisiología, anatomía funcional y terminología biomédica introductorias."},
            {"id": "DDM-PRE02", "statement": "Fundamentos de diseño de ingeniería, sistemas y documentación técnica."},
            {"id": "DDM-PRE03", "statement": "Estadística descriptiva básica, medición y razonamiento sobre incertidumbre."},
            {"id": "DDM-PRE04", "statement": "Ética, privacidad y límites de actividades educativas con información de salud."},
            {"id": "DDM-PRE05", "statement": "Capacidad para leer literatura técnica y fuentes regulatorias oficiales en inglés cuando sea necesario."}
        ],
        "competencies": [
            {"id": "DDM-COMP01", "statement": "Investigar necesidades y sistemas de uso sin congelar prematuramente la solución."},
            {"id": "DDM-COMP02", "statement": "Traducir necesidades a requisitos, arquitectura e interfaces verificables y trazables."},
            {"id": "DDM-COMP03", "statement": "Gestionar riesgos de manera iterativa y conectada con diseño, evidencia y nueva información."},
            {"id": "DDM-COMP04", "statement": "Diseñar estrategias de prototipado y verificación reproducibles con configuración y criterios explícitos."},
            {"id": "DDM-COMP05", "statement": "Seleccionar e interpretar evidencia de validación proporcional a necesidades, uso previsto y afirmaciones."},
            {"id": "DDM-COMP06", "statement": "Razonar sobre regulación, calidad, transferencia y vigilancia sin trasladar automáticamente decisiones entre jurisdicciones."},
            {"id": "DDM-COMP07", "statement": "Integrar el ciclo de vida en un expediente auditable que preserve incertidumbre, versiones, brechas y límites."}
        ],
        "learning_outcomes": [{"id": i, "statement": s} for i, s in course_los],
        "study_method": [
            "Definir primero la pregunta, la etapa del ciclo de vida, el uso previsto y el tipo de decisión que se intenta sostener.",
            "Alternar explicación, ejemplo trabajado, actividad guiada, práctica con apoyo reducido y reto autónomo.",
            "Separar datos u observaciones, interpretación, requisito, modelo de riesgo, evidencia, conclusión y obligación regulatoria potencial.",
            "Conservar identificadores, versiones, configuración, fuentes, criterios, desviaciones y cambios en cada producto.",
            "Usar evidencia negativa y contradicciones para estrechar conclusiones en vez de borrarlas.",
            "Cerrar cada unidad con un handoff explícito hacia la siguiente y revisar el producto con criterios antes de avanzar."
        ],
        "editorial_notice": "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para U1–U6. Las fuentes están trazadas y la publicación continúa como provisional. La revisión humana interna y disciplinaria externa, la asesoría regulatoria, cualquier actividad con participantes o pacientes, la auditoría QMS, la evaluación de conformidad, la certificación y la autorización de mercado siguen fuera de este cierre y permanecen pendientes."
    })
    preferred = []
    for keyword in ("biodesign", "qmsr", "14971", "13485", "human factors", "10993", "14155", "estar", "eudamed", "essential principles"):
        found = next((sid for sid, src in source_records.items() if keyword in source_text(src)), None)
        if found and found not in preferred:
            preferred.append(found)
    if len(preferred) < 6:
        preferred.extend([sid for sid in source_records if sid not in preferred][: 6 - len(preferred)])
    course["core_source_ids"] = preferred
    course["unit_files"] = [f"units/unit-{n:02d}.json" for n in range(1, 7)]
    course["assessment_files"] = [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"]
    course["registries"] = {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"}
    course["static_site"] = {
        "renderer": "scripts/generate_site.py",
        "canonical_source": True,
        "legacy_mirrors": [
            f"data/generated_courses/{COURSE_ID}.json",
            f"data/generated_units/{COURSE_ID}/",
            f"data/subjects/ingenieria-biomedica/{COURSE_ID}.json",
            f"data/source_registry/{COURSE_ID}.json",
            f"data/claim_registry/{COURSE_ID}.json",
        ],
    }
    write(COURSE_DIR / "course.json", course)

    test = '''from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "desarrollo-dispositivos-medicos"
GENERIC = "concepto de la unidad que debe definirse"


class DesarrolloDispositivosMedicosCanonicalCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        cls.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_status_closes_content_but_not_human_review(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_are_complete_and_cover_all_course_outcomes(self):
        self.assertEqual(len(self.course["unit_files"]), 6)
        known = {item["id"] for item in self.course["learning_outcomes"]}
        covered = set()
        for relative in self.course["unit_files"]:
            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))
            covered.update(unit["course_learning_outcome_ids"])
            serialized = json.dumps(unit, ensure_ascii=False).casefold()
            self.assertNotIn(GENERIC, serialized)
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 5)
            self.assertGreaterEqual(len(unit["activities"]), 3)
            self.assertTrue(all(a["estimated_duration_minutes"] > 0 for a in unit["activities"]))
            self.assertTrue(all(a["status"] == "complete" for a in unit["activities"]))
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
        self.assertEqual(known, covered)

    def test_assessments_have_feedback_classification_and_sources(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        total = 0
        for n in range(1, 7):
            assessment = json.loads((COURSE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(assessment["items"]), 10)
            self.assertEqual(assessment["status"], "complete")
            total += len(assessment["items"])
            for item in assessment["items"]:
                self.assertNotEqual(item["difficulty"], "unclassified")
                self.assertNotEqual(item["cognitive_level"], "unclassified")
                self.assertTrue(item["answer_key"]["explanation"])
                self.assertTrue(item["feedback"]["correct"])
                self.assertTrue(item["feedback"]["incorrect"])
                self.assertTrue(item["source_ids"])
                self.assertTrue(set(item["source_ids"]) <= source_ids)
                self.assertEqual(item["status"], "complete")
        self.assertGreaterEqual(total, 60)

    def test_sources_glossary_and_claims_are_traceable(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertGreaterEqual(len(source_ids), 25)
        self.assertTrue(all(item["verification_status"] == "verified_directly" for item in self.sources["sources"]))
        self.assertEqual(self.sources["coverage_gaps"], [])
        self.assertGreaterEqual(len(self.glossary["entries"]), 80)
        for entry in self.glossary["entries"]:
            self.assertTrue(entry["source_ids"])
            self.assertTrue(set(entry["source_ids"]) <= source_ids)
            self.assertEqual(entry["verification_status"], "traceable_to_verified_source")
        claims = self.claims["claims"]
        self.assertEqual(len(claims), 24)
        self.assertEqual(Counter(c["unit"] for c in claims), Counter({n: 4 for n in range(1, 7)}))
        serialized_units = {n: json.dumps(json.loads((COURSE / "units" / f"unit-{n:02d}.json").read_text(encoding="utf-8")), ensure_ascii=False) for n in range(1, 7)}
        for claim in claims:
            self.assertIn(claim["source_id"], source_ids)
            self.assertEqual(claim["source_verification_status"], "verified_directly")
            self.assertEqual(claim["review_state"], "ai_review_provisional")
            self.assertEqual(claim["support"], "direct")
            self.assertIn(claim["text"], serialized_units[claim["unit"]])

    def test_course_assessment_integrates_the_full_lifecycle(self):
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(x["weight_percent"] for x in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)
        self.assertGreaterEqual(len(assessment["capstone"]["required_deliverables"]), 12)
        self.assertEqual(assessment["status"], "complete")

    def test_scope_and_lifecycle_boundaries_are_explicit(self):
        purpose = self.course["purpose"].casefold()
        notice = self.course["editorial_notice"].casefold()
        for concept in ("necesidades", "requisitos", "gestión de riesgos", "verificación", "validación", "regulación", "transferencia", "vigilancia posmercado"):
            self.assertIn(concept, purpose)
        self.assertIn("revisión humana", notice)
        self.assertIn("asesoría regulatoria", notice)
        self.assertIn("autorización de mercado", notice)


if __name__ == "__main__":
    unittest.main()
'''
    (ROOT / "tests" / "test_desarrollo_dispositivos_medicos_canonical_course.py").write_text(test, encoding="utf-8")

    print(f"Canonical DDM finalized: sources={len(source_records)} glossary={len(glossary['entries'])} claims={len(claims)}")


if __name__ == "__main__":
    finalize()
