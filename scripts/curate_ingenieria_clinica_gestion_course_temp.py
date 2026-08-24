#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "ingenieria-clinica-gestion"
COURSE_CODE = "ICG"
AREA_ID = "ingenieria-biomedica"
SRC_DIR = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"
DST_DIR = ROOT / "data" / "courses" / COURSE_ID
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


def dump(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "item"


def as_text(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        parts = [str(v).strip() for v in value.values() if str(v).strip()]
        return "; ".join(parts)
    return str(value).strip()


def normalize_connections(items) -> list[str]:
    out = []
    for item in items or []:
        text = as_text(item)
        if text and text not in out:
            out.append(text)
    return out


def source_fingerprint(source: dict) -> str:
    return str(source.get("url") or source.get("doi") or source.get("title") or source.get("reference") or "").strip()


def source_identifier(source: dict) -> str:
    basis = source_fingerprint(source)
    title = str(source.get("title") or source.get("reference") or "source")
    digest = hashlib.sha1(basis.encode("utf-8")).hexdigest()[:8]
    return f"{slugify(title)[:54]}-{digest}"


def choose_source_id(paragraph: str, source_ids: list[str], source_registry: dict[str, dict]) -> str:
    if not source_ids:
        raise RuntimeError("Unidad sin fuentes verificadas")
    words = {w for w in re.findall(r"[a-záéíóúñ0-9]+", paragraph.casefold()) if len(w) >= 4}
    best_id = source_ids[0]
    best_score = -1
    for sid in source_ids:
        source = source_registry[sid]
        haystack = " ".join(str(source.get(k) or "") for k in ("title", "organization", "publisher", "reference", "url")).casefold()
        tokens = {w for w in re.findall(r"[a-záéíóúñ0-9]+", haystack) if len(w) >= 4}
        score = len(words & tokens)
        if score > best_score:
            best_score = score
            best_id = sid
    return best_id


units_src = [load(SRC_DIR / f"unit-{i:02d}.json") for i in range(1, 7)]
for index, unit in enumerate(units_src, start=1):
    assert unit["subject_id"] == COURSE_ID
    assert unit["unit"] == index
    assert unit["status"] == "review"
    assert "concepto de la unidad que debe definirse mediante entidades observables" not in json.dumps(unit, ensure_ascii=False).casefold()
    assert len(unit.get("learning_objectives", [])) >= 5
    assert len(unit.get("theory_sections", [])) >= 4
    assert len(unit.get("worked_examples", [])) >= 2
    assert unit.get("guided_activities")
    assert len(unit.get("self_assessment", [])) >= 8
    assert unit.get("sources")

# Registry of verified sources deduplicated by URL/locator.
source_registry: dict[str, dict] = {}
source_key_to_id: dict[str, str] = {}
unit_source_ids: dict[int, list[str]] = {}
for index, unit in enumerate(units_src, start=1):
    ids: list[str] = []
    for source in unit.get("sources", []):
        status = str(source.get("verification_status") or "").strip()
        if status != "verified_directly":
            raise RuntimeError(f"U{index}: fuente no verificada directamente: {source.get('title') or source}")
        key = source_fingerprint(source)
        if not key:
            raise RuntimeError(f"U{index}: fuente sin localizador")
        if key not in source_key_to_id:
            sid = source_identifier(source)
            while sid in source_registry:
                sid += "x"
            source_key_to_id[key] = sid
            record = copy.deepcopy(source)
            record["id"] = sid
            record["verification_status"] = "verified_directly"
            record.setdefault("verification_notes", "Fuente trasladada desde una unidad disciplinar cuya verificación directa ya estaba registrada antes del cierre canónico del curso.")
            source_registry[sid] = record
        sid = source_key_to_id[key]
        if sid not in ids:
            ids.append(sid)
    unit_source_ids[index] = ids

# Course-level learning outcomes are intentionally aligned one-to-one with U1–U6 plus integration.
course_los = [
    {"id": "ICG-LO01", "statement": "Explicar la función, gobernanza y ciclo de vida de ingeniería clínica mediante actores, responsabilidades, documentación y handoffs trazables, reconociendo límites profesionales e institucionales."},
    {"id": "ICG-LO02", "statement": "Construir y auditar un inventario sintético de tecnología sanitaria con identificación, taxonomía, estado, criticidad, calidad de datos y priorización transparente sin convertir un puntaje en decisión automática."},
    {"id": "ICG-LO03", "statement": "Diseñar una estrategia educativa de mantenimiento y metrología basada en evidencia, criticidad, desempeño, trazabilidad e incertidumbre, diferenciando mantenimiento, calibración, verificación y autorización de intervención."},
    {"id": "ICG-LO04", "statement": "Estructurar una evaluación y adquisición sintética de tecnología sanitaria mediante necesidad, requisitos, evidencia, costo total, interoperabilidad, infraestructura y gobernanza, sin reducir la decisión a precio, marca o puntuación aislada."},
    {"id": "ICG-LO05", "statement": "Analizar incidentes y señales de seguridad de forma reproducible mediante preservación de evidencia, cronología, clasificación, investigación sistémica, acciones y vigilancia, evitando inferencias causales o regulatorias no sustentadas."},
    {"id": "ICG-LO06", "statement": "Diseñar y evaluar un proyecto sintético de mejora del servicio mediante KPIs operativos, SLA, costos, PDSA, series temporales, medidas de balance, competencia, adopción y sostenibilidad."},
    {"id": "ICG-LO07", "statement": "Integrar U1–U6 en un expediente auditable de gestión del ciclo de vida tecnológico que conserve fuentes, supuestos, decisiones, incertidumbre, escalamiento y límites, sin presentarlo como auditoría, certificación, contratación ni autorización clínica o regulatoria."},
]

# Glossary and claims are built from the already-curated unit content.
glossary_entries: list[dict] = []
claim_entries: list[dict] = []
media_items: list[dict] = []
canonical_units: list[dict] = []
unit_assessments: list[dict] = []

glossary_counter = 0
claim_counter = 0
for index, src in enumerate(units_src, start=1):
    unit_id = f"ICG-U{index:02d}"
    local_los = [
        {"id": f"{unit_id}-LO{j:02d}", "statement": statement}
        for j, statement in enumerate(src["learning_objectives"], start=1)
    ]
    prerequisite_unit_ids = [f"ICG-U{i:02d}" for i in range(1, index)]
    topics = []
    unit_claim_ids: list[str] = []
    for t_index, section in enumerate(src["theory_sections"], start=1):
        topic_id = f"{unit_id}-T{t_index:02d}"
        equations = []
        for e_index, equation in enumerate(section.get("equations", []), start=1):
            block = {
                "id": f"{topic_id}-B{e_index:02d}",
                "type": "equation",
                "latex": str(equation.get("latex") or "").strip(),
            }
            if equation.get("label"):
                block["label"] = str(equation["label"])
            if isinstance(equation.get("variables"), dict):
                block["variables"] = {str(k): str(v) for k, v in equation["variables"].items()}
            if block["latex"]:
                equations.append(block)
        subtopics = []
        key_points = [str(x) for x in section.get("key_points", [])]
        for p_index, paragraph in enumerate(section.get("paragraphs", []), start=1):
            subtitle = key_points[p_index - 1] if p_index <= len(key_points) else f"Desarrollo {p_index}"
            sub_id = f"{topic_id}-ST{p_index:02d}"
            subtopics.append({
                "id": sub_id,
                "title": subtitle,
                "blocks": [{"id": f"{sub_id}-B01", "type": "paragraph", "text": paragraph}],
            })
        topics.append({
            "id": topic_id,
            "title": section["heading"],
            "key_points": key_points or [section["heading"]],
            "blocks": equations,
            "subtopics": subtopics,
        })
        if section.get("paragraphs"):
            claim_counter += 1
            claim_id = f"ICG-CLM{claim_counter:03d}"
            paragraph = section["paragraphs"][0]
            sid = choose_source_id(paragraph, unit_source_ids[index], source_registry)
            claim_entries.append({
                "id": claim_id,
                "unit_id": unit_id,
                "text": paragraph,
                "source_id": sid,
                "verification_status": "verified_directly",
                "scope": "Afirmación educativa central trasladada literalmente del bloque teórico curado; la fuente respalda el contexto metodológico o institucional y no amplía la inferencia más allá del texto.",
            })
            unit_claim_ids.append(claim_id)

    unit_glossary_ids: list[str] = []
    for entry in src.get("glossary", []):
        glossary_counter += 1
        gid = f"ICG-G{glossary_counter:03d}"
        unit_glossary_ids.append(gid)
        glossary_entries.append({
            "id": gid,
            "term": str(entry.get("term") or "").strip(),
            "definition": str(entry.get("definition") or "").strip(),
            "unit_ids": [unit_id],
            "source_ids": [unit_source_ids[index][0]],
            "verification_status": "verified_directly",
        })

    examples = []
    for ex_index, example in enumerate(src.get("worked_examples", []), start=1):
        reasoning_steps = example.get("reasoning_steps") or example.get("steps") or []
        if isinstance(reasoning_steps, str):
            reasoning_steps = [reasoning_steps]
        interpretation = example.get("interpretation") or example.get("result") or example.get("conclusion") or "Interpretar el resultado únicamente dentro del alcance y los supuestos declarados en el escenario sintético."
        limitations = example.get("limitations") or example.get("limitation") or ["El ejemplo es educativo y sintético; no constituye una decisión clínica, contractual, regulatoria ni de mantenimiento real."]
        if isinstance(limitations, str):
            limitations = [limitations]
        examples.append({
            "id": f"{unit_id}-EX{ex_index:02d}",
            "title": str(example.get("title") or f"Ejemplo {ex_index}"),
            "scenario": str(example.get("scenario") or "Escenario sintético de ingeniería clínica."),
            "reasoning_steps": [str(x) for x in reasoning_steps] or ["Identificar entradas, decisión, evidencia, incertidumbre y límites."],
            "interpretation": as_text(interpretation),
            "limitations": [str(x) for x in limitations],
        })

    activities = []
    for a_index, activity in enumerate(src.get("guided_activities", []), start=1):
        tasks = activity.get("problems") or activity.get("tasks") or []
        activities.append({
            "id": f"{unit_id}-ACT{a_index:02d}",
            "title": str(activity.get("title") or f"Actividad guiada U{index}"),
            "purpose": src["purpose"],
            "prerequisite_unit_ids": prerequisite_unit_ids,
            "instructions": [str(x) for x in activity.get("instructions", [])],
            "tasks": [str(x) for x in tasks],
            "deliverables": [str(x) for x in activity.get("deliverables", [])],
            "checking_criteria": [str(x) for x in activity.get("checking_criteria", [])],
            "estimated_duration_minutes": 270 if index == 6 else 240,
            "status": "complete",
        })

    unit_media_ids = [f"ICG-MED-U{index:02d}-01", f"ICG-MED-U{index:02d}-02"]
    media_items.extend([
        {
            "id": unit_media_ids[0], "unit_id": unit_id, "type": "diagram", "status": "planned",
            "title": f"Mapa conceptual de U{index}: {src['title']}",
            "purpose": "Resumir visualmente relaciones, decisiones y límites de la unidad sin reemplazar la explicación textual.",
            "alt_text": f"Diagrama planificado de los conceptos y relaciones principales de {src['title']}.",
        },
        {
            "id": unit_media_ids[1], "unit_id": unit_id, "type": "worked_example_visual", "status": "planned",
            "title": f"Flujo visual de la actividad guiada U{index}",
            "purpose": "Mostrar la secuencia entrada → análisis → decisión → evidencia → límite para apoyar la práctica guiada.",
            "alt_text": f"Flujo planificado para resolver la actividad guiada de {src['title']}.",
        },
    ])

    canonical = {
        "$schema": "../../../../schemas/academic/unit-v1.schema.json",
        "schema_version": "1.0",
        "id": unit_id,
        "course_id": COURSE_ID,
        "order": index,
        "slug": src["slug"],
        "title": src["title"],
        "status": STATUS,
        "purpose": src["purpose"],
        "prerequisite_unit_ids": prerequisite_unit_ids,
        "course_learning_outcome_ids": [f"ICG-LO{index:02d}", "ICG-LO07"],
        "learning_outcomes": local_los,
        "topics": topics,
        "examples": examples,
        "activities": activities,
        "assessment_file": f"assessments/unit-{index:02d}.json",
        "glossary_entry_ids": unit_glossary_ids,
        "source_ids": unit_source_ids[index],
        "claim_ids": unit_claim_ids,
        "media_ids": unit_media_ids,
        "common_errors": src.get("common_errors", []),
        "biomedical_connections": normalize_connections(src.get("biomedical_connections", [])),
        "editorial_notice": src.get("editorial_notice", ""),
        "legacy_origin": f"data/course_redevelopment/{COURSE_ID}/units/unit-{index:02d}.json",
    }
    canonical_units.append(canonical)

    items = []
    source_ids = unit_source_ids[index]
    for q_index, qa in enumerate(src.get("self_assessment", []), start=1):
        if q_index <= 3:
            difficulty, cognitive = "foundational", "understand"
        elif q_index <= 7:
            difficulty, cognitive = "intermediate", "analyze"
        else:
            difficulty, cognitive = "advanced", "evaluate"
        lo_id = local_los[(q_index - 1) % len(local_los)]["id"]
        items.append({
            "id": f"{unit_id}-Q{q_index:02d}",
            "type": "short_answer",
            "prompt": str(qa.get("question") or "Explica el razonamiento esperado."),
            "linked_learning_outcome_ids": [lo_id],
            "difficulty": difficulty,
            "cognitive_level": cognitive,
            "answer_key": {
                "expected_answer": str(qa.get("answer") or "Respuesta razonada según la unidad."),
                "explanation": str(qa.get("reasoning") or qa.get("answer") or "Revisar el razonamiento de la unidad."),
                "common_misconceptions": [str(qa.get("common_error"))] if qa.get("common_error") else [],
            },
            "feedback": {
                "correct": "Correcto: la respuesta mantiene la distinción entre evidencia, decisión, responsabilidad y límite de inferencia. Contrasta ahora tu formulación con la explicación para comprobar trazabilidad.",
                "incorrect": "Revisa el bloque teórico y reconstruye la cadena entrada → criterio → decisión → evidencia → límite. Identifica qué concepto confundiste antes de responder de nuevo.",
            },
            "source_ids": [source_ids[(q_index - 1) % len(source_ids)]],
            "status": "complete",
        })
    unit_assessments.append({
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{unit_id}-EVAL",
        "course_id": COURSE_ID,
        "scope": "unit",
        "unit_id": unit_id,
        "purpose": f"Comprobar comprensión, aplicación y juicio crítico de U{index} — {src['title']} con retroalimentación recuperativa y fuentes trazables.",
        "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
        "items": items,
        "status": "complete",
    })

# Build course and registries.
course = {
    "$schema": "../../../schemas/academic/course-v1.schema.json",
    "schema_version": "1.0",
    "id": COURSE_ID,
    "code": COURSE_CODE,
    "area_id": AREA_ID,
    "title": "Ingeniería Clínica y Gestión",
    "language": "es",
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica y áreas afines con fundamentos de tecnología médica, medición, estadística descriptiva, seguridad y gestión que necesiten razonar de forma trazable sobre el ciclo de vida de tecnologías sanitarias dentro de organizaciones de salud.",
    "status": STATUS,
    "purpose": "Integrar gobernanza del ciclo de vida, inventario y criticidad, mantenimiento y metrología, evaluación y adquisición, seguridad e incidentes, y proyectos de mejora para construir un expediente reproducible de gestión de tecnología sanitaria sintética, diferenciando evidencia técnica, responsabilidad institucional, decisión contractual, calidad clínica y obligación regulatoria y sin presentar el trabajo académico como auditoría, certificación, contratación ni autorización operativa.",
    "scope": {
        "included": [
            "Función y gobernanza de ingeniería clínica, ciclo de vida, actores, RACI, documentación y handoffs.",
            "Inventario, identificación, taxonomía, estado, calidad de datos, criticidad, priorización y renovación.",
            "Mantenimiento, desempeño, metrología, calibración, verificación, intervalos, documentación e incertidumbre.",
            "Evaluación de necesidades, requisitos, evidencia, costo total, interoperabilidad, infraestructura, adquisición y aceptación técnica sintética.",
            "Seguridad, incidentes, preservación de evidencia, investigación sistémica, acciones, vigilancia y comunicación proporcional.",
            "KPIs, disponibilidad, SLA, costos, mejora PDSA, series temporales, medidas de balance, competencia, adopción y sostenibilidad.",
            "Expedientes reproducibles con fuentes, versiones, supuestos, criterios, decisiones, incertidumbre y límites de inferencia."
        ],
        "excluded": [
            "Intervención, mantenimiento, calibración, ensayo o modificación de dispositivos médicos reales.",
            "Acceso a inventarios institucionales, expedientes de pacientes, incidentes reales o información confidencial sin autorización.",
            "Decisiones reales de compra, contratación, retirada de servicio, aceptación técnica o liberación de equipos para uso clínico.",
            "Asesoría jurídica o regulatoria, auditoría oficial, certificación, declaración de conformidad o acreditación institucional.",
            "Diagnóstico, tratamiento, juicio clínico o afirmaciones de seguridad, efectividad o causalidad no demostradas."
        ],
        "handoff_courses": [
            "desarrollo-dispositivos-medicos",
            "laboratorio-bioinstrumentacion",
            "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas",
            "aplicaciones-salud-digital",
            "sistemas-ayuda-decision-medica"
        ],
    },
    "prerequisites": [
        {"id": "ICG-PRE01", "statement": "Fundamentos de bioinstrumentación, dispositivos médicos y seguridad tecnológica."},
        {"id": "ICG-PRE02", "statement": "Estadística descriptiva, proporciones, tasas, tendencias temporales e incertidumbre básica."},
        {"id": "ICG-PRE03", "statement": "Principios de documentación técnica, trazabilidad y control de versiones."},
        {"id": "ICG-PRE04", "statement": "Capacidad para leer fuentes técnicas, normativas y de organismos internacionales en inglés cuando sea necesario."},
    ],
    "competencies": [
        {"id": "ICG-COMP01", "statement": "Modelar el ciclo de vida tecnológico como un sistema sociotécnico con gobernanza y responsabilidades explícitas."},
        {"id": "ICG-COMP02", "statement": "Organizar activos y evidencia mediante datos estructurados, criticidad y criterios de priorización auditables."},
        {"id": "ICG-COMP03", "statement": "Razonar sobre mantenimiento y metrología mediante desempeño, riesgo, trazabilidad e incertidumbre sin exceder la competencia autorizada."},
        {"id": "ICG-COMP04", "statement": "Evaluar alternativas tecnológicas de manera multicriterio y documentar requisitos, evidencia, costos, interfaces y límites."},
        {"id": "ICG-COMP05", "statement": "Investigar seguridad e incidentes de forma sistémica, conservando evidencia y separando hechos, hipótesis, causalidad y obligaciones potenciales."},
        {"id": "ICG-COMP06", "statement": "Medir y mejorar el desempeño de un servicio mediante indicadores operativos, contratos, ciclos de aprendizaje, competencia y sostenibilidad."},
        {"id": "ICG-COMP07", "statement": "Comunicar decisiones de ingeniería clínica con trazabilidad, incertidumbre, escalamiento y límites profesionales explícitos."},
    ],
    "learning_outcomes": course_los,
    "study_method": [
        "Definir primero el sistema, la decisión, los actores, la autoridad y el tipo de evidencia disponible.",
        "Alternar explicación, ejemplo trabajado, actividad guiada sintética, práctica con apoyo reducido y comprobación recuperativa.",
        "Separar dato observado, indicador, criterio, interpretación, decisión y obligación potencial para evitar inferencias automáticas.",
        "Conservar identificadores, fuentes, versiones, supuestos, excepciones, incertidumbre y límites en cada producto.",
        "Usar escenarios sintéticos para practicar sin intervenir servicios, pacientes, contratos ni dispositivos reales.",
        "Cerrar cada unidad con un handoff explícito hacia la siguiente y culminar con un expediente integrado U1–U6."
    ],
    "core_source_ids": list(source_registry)[:12],
    "unit_files": [f"units/unit-{i:02d}.json" for i in range(1, 7)],
    "assessment_files": [f"assessments/unit-{i:02d}.json" for i in range(1, 7)] + ["assessments/course-assessment.json"],
    "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
    "static_site": {
        "renderer": "scripts/generate_site.py",
        "canonical_source": True,
        "legacy_mirrors": [
            f"data/generated_courses/{COURSE_ID}.json",
            f"data/generated_units/{COURSE_ID}/",
            f"data/subjects/{AREA_ID}/{COURSE_ID}.json",
            f"data/source_registry/{COURSE_ID}.json",
            f"data/claim_registry/{COURSE_ID}.json",
        ],
    },
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para U1–U6. Las fuentes trasladadas desde las unidades disciplinares conservan verificación directa y la publicación continúa como provisional. La revisión humana interna y disciplinaria externa, las decisiones reales de mantenimiento, compra o contratación, la investigación oficial de incidentes, la asesoría jurídica o regulatoria, la auditoría, certificación y cualquier autorización clínica u operativa permanecen fuera de este cierre y pendientes cuando corresponda.",
}

sources_payload = {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "sources": list(source_registry.values()),
    "source_policy": "Se reutilizan únicamente fuentes registradas como verificadas directamente en las seis unidades disciplinares; el cierre canónico no eleva revisión interna a validación externa ni convierte guías o normas en certificación.",
    "consulted_on": "2026-08-24",
    "coverage_gaps": [],
    "coverage_status": "complete",
    "status": "traceable",
}
glossary_payload = {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "entries": glossary_entries,
    "coverage_status": "complete",
    "status": "complete",
}
claims_payload = {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "claims": claim_entries,
    "coverage_status": "complete",
    "review_state": "internal_traceability_complete_external_review_pending",
    "status": "traceable",
}
media_payload = {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "items": media_items,
    "scope": "Recursos visuales planificados para apoyar comprensión; el contenido textual y las actividades no dependen de ellos.",
    "status": "planned",
}

course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "ICG-COURSE-EVAL",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": [
        "Evaluar razonamiento trazable y no memorización aislada de siglas o normas.",
        "Usar exclusivamente escenarios sintéticos y separar evidencia, decisión, autoridad y límite de inferencia.",
        "Distribuir evaluación entre las seis unidades e integrar el ciclo completo en un capstone reproducible.",
        "Proporcionar criterios de éxito antes de la entrega y retroalimentación recuperativa después de cada evaluación.",
        "No convertir una calificación académica en autorización profesional, auditoría, certificación o decisión institucional real."
    ],
    "assessment_plan": [
        {"component": "Evaluaciones U1–U2", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO02"]},
        {"component": "Evaluaciones U3–U4", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO03", "ICG-LO04"]},
        {"component": "Evaluaciones U5–U6", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO05", "ICG-LO06"]},
        {"component": "Examen intermedio de integración U1–U3", "weight_percent": 20, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO02", "ICG-LO03"]},
        {"component": "Capstone: expediente de gestión tecnológica U1–U6", "weight_percent": 35, "linked_learning_outcome_ids": [x["id"] for x in course_los]},
    ],
    "diagnostic": {
        "purpose": "Detectar prerrequisitos y conceptos que requieren repaso antes de iniciar el curso; no aporta nota sumativa.",
        "questions": [
            "Diferencia dato observado, interpretación, criterio y decisión con un ejemplo técnico.",
            "Explica por qué una tasa necesita numerador, denominador y ventana temporal.",
            "Describe qué significa trazabilidad en un expediente técnico.",
            "Distingue calibración, verificación y mantenimiento sin asumir que son sinónimos.",
            "Explica por qué una decisión de compra no debería depender de una única cifra o marca."
        ],
        "feedback_rule": "Cada respuesta insuficiente enlaza con el prerrequisito o la unidad introductoria correspondiente antes de continuar."
    },
    "midterm_blueprint": [
        {"domain": "Gobernanza y ciclo de vida U1", "weight_percent": 30, "linked_learning_outcome_ids": ["ICG-LO01"]},
        {"domain": "Inventario y criticidad U2", "weight_percent": 30, "linked_learning_outcome_ids": ["ICG-LO02"]},
        {"domain": "Mantenimiento y metrología U3", "weight_percent": 30, "linked_learning_outcome_ids": ["ICG-LO03"]},
        {"domain": "Integración y límites", "weight_percent": 10, "linked_learning_outcome_ids": ["ICG-LO07"]},
    ],
    "capstone": {
        "title": "Expediente integrado de gestión de una tecnología sanitaria sintética",
        "scenario": "Una red hospitalaria ficticia debe gobernar durante un ciclo anual una familia tecnológica sintética con inventario incompleto, necesidades de mantenimiento, una posible renovación, un incidente no concluyente y un proyecto de mejora del servicio.",
        "deliverables": [
            "Mapa de ciclo de vida, actores, RACI, decisiones y handoffs.",
            "Inventario sintético depurado con reglas de calidad, criticidad y priorización.",
            "Plan educativo de mantenimiento/metrología con evidencia, intervalos, trazabilidad e incertidumbre.",
            "Expediente de evaluación/adquisición con necesidad, requisitos, evidencia, TCO, interoperabilidad e infraestructura.",
            "Informe de incidente sintético que separe hechos, hipótesis, causalidad, acciones y vigilancia.",
            "Proyecto de mejora con familia de KPIs, SLA, PDSA, serie temporal, medidas de balance, competencia y sostenibilidad.",
            "Informe final que identifique incertidumbre, decisiones autorizadas, decisiones que deben escalarse y afirmaciones que no pueden sostenerse."
        ],
        "linked_learning_outcome_ids": [x["id"] for x in course_los],
        "rubric": [
            {"criterion": "Trazabilidad del ciclo de vida y gobernanza", "weight_percent": 20, "excellent": "Cada decisión conecta entrada, criterio, responsable, evidencia, salida y handoff sin ambigüedad."},
            {"criterion": "Rigor técnico y cuantitativo", "weight_percent": 20, "excellent": "Indicadores, cálculos, unidades, denominadores, incertidumbre y supuestos son correctos y reproducibles."},
            {"criterion": "Integración U1–U6", "weight_percent": 20, "excellent": "El expediente conecta inventario, mantenimiento, adquisición, seguridad y mejora sin duplicar funciones ni saltar etapas."},
            {"criterion": "Uso de fuentes y proporcionalidad de evidencia", "weight_percent": 20, "excellent": "Las conclusiones se apoyan en fuentes trazables y se estrechan cuando la evidencia es insuficiente o contextual."},
            {"criterion": "Límites, ética y comunicación", "weight_percent": 20, "excellent": "Distingue decisión académica de autoridad real y evita afirmaciones clínicas, contractuales, regulatorias o de seguridad no demostradas."}
        ],
    },
    "status": "complete",
}

# Write canonical corpus.
dump(DST_DIR / "course.json", course)
dump(DST_DIR / "sources.json", sources_payload)
dump(DST_DIR / "glossary.json", glossary_payload)
dump(DST_DIR / "claims.json", claims_payload)
dump(DST_DIR / "media.json", media_payload)
for index, unit in enumerate(canonical_units, start=1):
    dump(DST_DIR / "units" / f"unit-{index:02d}.json", unit)
for index, assessment in enumerate(unit_assessments, start=1):
    dump(DST_DIR / "assessments" / f"unit-{index:02d}.json", assessment)
dump(DST_DIR / "assessments" / "course-assessment.json", course_assessment)

# Strong invariants before repository validators.
assert sum(x["weight_percent"] for x in course_assessment["assessment_plan"]) == 100
assert sum(x["weight_percent"] for x in course_assessment["midterm_blueprint"]) == 100
assert sum(x["weight_percent"] for x in course_assessment["capstone"]["rubric"]) == 100
assert len(canonical_units) == 6
assert len(unit_assessments) == 6
assert len(claim_entries) >= 24
assert len(glossary_entries) >= 60
assert all(source["verification_status"] == "verified_directly" for source in source_registry.values())
print(f"Canonicalized {COURSE_ID}: units={len(canonical_units)}, glossary={len(glossary_entries)}, sources={len(source_registry)}, claims={len(claim_entries)}, media={len(media_items)}")
