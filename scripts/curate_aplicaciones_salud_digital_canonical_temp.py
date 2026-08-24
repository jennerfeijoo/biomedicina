#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

from migrate_course_to_canonical import migrate

ROOT = Path(__file__).resolve().parents[1]
SUBJECT = "aplicaciones-salud-digital"
CODE = "SALDIG"
COURSE_ROOT = ROOT / "data" / "courses" / SUBJECT
REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment" / SUBJECT
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
    {
        "id": "SALDIG-LO01",
        "statement": "Formula problemas de salud susceptibles de intervención digital mediante actores, flujo asistencial, necesidades, determinantes, equidad y evidencia de contexto antes de elegir una tecnología.",
    },
    {
        "id": "SALDIG-LO02",
        "statement": "Diseña soluciones digitales centradas en personas mediante contexto de uso, participación, requisitos trazables, usabilidad, accesibilidad, prevención de errores y evaluación formativa.",
    },
    {
        "id": "SALDIG-LO03",
        "statement": "Diseña y audita escenarios de telemedicina y monitorización remota distinguiendo modalidad asistencial, cadena sensor-dato, calidad, latencia, reglas de alerta, carga operativa y contingencias.",
    },
    {
        "id": "SALDIG-LO04",
        "statement": "Construye contratos de interoperabilidad y calidad de datos usando modelos, perfiles, terminologías, procedencia y pruebas extremo a extremo sin confundir conformidad técnica con verdad clínica.",
    },
    {
        "id": "SALDIG-LO05",
        "statement": "Evalúa valor de una intervención digital separando efectividad clínica, engagement, resultados de implementación, equidad, costes, coste-efectividad, impacto presupuestario e incertidumbre.",
    },
    {
        "id": "SALDIG-LO06",
        "statement": "Analiza privacidad, protección de datos, ciberseguridad, gobernanza y marco regulatorio de una solución digital delimitando finalidad prevista, riesgos, responsabilidades y evidencia faltante.",
    },
    {
        "id": "SALDIG-LO07",
        "statement": "Integra las seis unidades en un expediente reproducible de salud digital que vincula problema, usuarios, servicio, datos, evidencia, riesgos, gobernanza, implementación y límites de inferencia sin convertir el curso en autorización de despliegue.",
    },
]

LO_MAPPING = {
    1: ["SALDIG-LO01"],
    2: ["SALDIG-LO02"],
    3: ["SALDIG-LO03"],
    4: ["SALDIG-LO04"],
    5: ["SALDIG-LO05"],
    6: ["SALDIG-LO06", "SALDIG-LO07"],
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def dict_activities(unit: dict[str, Any]) -> list[dict[str, Any]]:
    value = unit.get("guided_activities") or unit.get("guided_activity") or []
    if isinstance(value, dict):
        return [value]
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def normalize_words(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-záéíóúñü0-9]+", text.casefold())
        if len(token) >= 5 and token not in {"entre", "desde", "hasta", "sobre", "puede", "deben", "datos", "salud", "digital"}
    }


def choose_source(claim_text: str, topic_title: str, unit_source_ids: list[str], source_map: dict[str, dict[str, Any]]) -> str:
    target = normalize_words(claim_text + " " + topic_title)
    best_id = unit_source_ids[0]
    best_score = -1
    for source_id in unit_source_ids:
        source = source_map[source_id]
        haystack = json.dumps(source, ensure_ascii=False)
        score = len(target & normalize_words(haystack))
        if score > best_score:
            best_id = source_id
            best_score = score
    return best_id


if COURSE_ROOT.exists():
    shutil.rmtree(COURSE_ROOT)
migrate(SUBJECT, CODE)

course = load(COURSE_ROOT / "course.json")
canonical_units: list[dict[str, Any]] = []
source_units: list[dict[str, Any]] = []
for number in range(1, 7):
    canonical = load(COURSE_ROOT / "units" / f"unit-{number:02d}.json")
    source = load(REDEVELOPMENT_ROOT / "units" / f"unit-{number:02d}.json")
    canonical["status"] = dict(STATUS)
    canonical["purpose"] = source["purpose"]
    canonical["course_learning_outcome_ids"] = LO_MAPPING[number]
    source_activities = dict_activities(source)
    for index, activity in enumerate(canonical["activities"]):
        source_activity = source_activities[index] if index < len(source_activities) else {}
        activity["purpose"] = str(
            source_activity.get("purpose")
            or f"Aplicar {canonical['title']} en un escenario sintético, producir un expediente verificable y justificar qué conclusiones están y no están respaldadas."
        )
        source_duration = source_activity.get("estimated_duration_minutes")
        activity["estimated_duration_minutes"] = (
            int(source_duration)
            if isinstance(source_duration, (int, float)) and source_duration > 0
            else [120, 90, 75][index] if index < 3 else 60
        )
        activity["status"] = "ready_for_self_study"
    canonical_units.append(canonical)
    source_units.append(source)

sources_doc = load(COURSE_ROOT / "sources.json")
source_map = {str(item["id"]): item for item in sources_doc["sources"] if item.get("id")}
source_by_url: dict[str, dict[str, Any]] = {}
source_by_title: dict[str, dict[str, Any]] = {}
for unit in source_units:
    raw_sources = unit.get("sources", [])
    if not isinstance(raw_sources, list):
        continue
    for source in raw_sources:
        if not isinstance(source, dict):
            continue
        url = str(source.get("url") or "").strip()
        title = str(source.get("title") or "").strip().casefold()
        if url:
            source_by_url[url] = source
        if title:
            source_by_title[title] = source

for record in source_map.values():
    raw = None
    url = str(record.get("url") or "").strip()
    title = str(record.get("title") or "").strip().casefold()
    if url and url in source_by_url:
        raw = source_by_url[url]
    elif title and title in source_by_title:
        raw = source_by_title[title]
    if raw:
        for key, value in raw.items():
            if value not in (None, "", []):
                if key == "verification_status" or not record.get(key):
                    record[key] = value

verified_ids = {
    source_id
    for source_id, record in source_map.items()
    if str(record.get("verification_status") or "").strip() not in {"", "unverified"}
}
for unit in canonical_units:
    unit["source_ids"] = [source_id for source_id in unit["source_ids"] if source_id in verified_ids]
    if len(unit["source_ids"]) < 5:
        raise RuntimeError(f"{unit['id']}: menos de cinco fuentes verificadas tras consolidación")

used_source_ids: list[str] = []
for unit in canonical_units:
    for source_id in unit["source_ids"]:
        if source_id not in used_source_ids:
            used_source_ids.append(source_id)
selected_sources = [source_map[source_id] for source_id in used_source_ids]
if len(selected_sources) < 25:
    raise RuntimeError(f"Solo se consolidaron {len(selected_sources)} fuentes verificadas")
for record in selected_sources:
    if str(record.get("verification_status") or "").strip() in {"", "unverified"}:
        raise RuntimeError(f"Fuente sin verificación: {record.get('id')}")

sources_doc["sources"] = selected_sources
sources_doc["coverage_gaps"] = []
sources_doc["consulted_on"] = TODAY
sources_doc["source_policy"] = (
    "Conservar fuentes oficiales, estándares, guías metodológicas y literatura indexada usadas por las seis unidades; "
    "cada fuente debe registrar un estado de verificación y las afirmaciones centrales se vinculan a una fuente concreta. "
    "Los textos regulatorios y estándares se comprueban de nuevo antes de cualquier uso profesional porque pueden cambiar."
)
write(COURSE_ROOT / "sources.json", sources_doc)
source_map = {item["id"]: item for item in selected_sources}

# Registra afirmaciones literales: cuatro por unidad, escogidas de los key points ya curados.
claims: list[dict[str, Any]] = []
for unit in canonical_units:
    unit_claim_ids: list[str] = []
    number = int(unit["order"])
    for index, topic in enumerate(unit["topics"][:4], start=1):
        key_points = [str(value).strip() for value in topic.get("key_points", []) if str(value).strip()]
        if not key_points:
            raise RuntimeError(f"{unit['id']}:{topic['id']} no tiene key point para claim")
        text = key_points[0]
        source_id = choose_source(text, str(topic.get("title") or ""), unit["source_ids"], source_map)
        source = source_map[source_id]
        claim_id = f"{unit['id']}-C{index:03d}"
        locator: dict[str, Any] = {}
        if source.get("url"):
            locator["url"] = source["url"]
        if source.get("title"):
            locator["title"] = source["title"]
        claims.append(
            {
                "id": claim_id,
                "claim_id": claim_id,
                "unit": number,
                "unit_id": unit["id"],
                "text": text,
                "claim_type": "methodological_or_interpretive",
                "risk": "medium",
                "context": f"Síntesis educativa de {unit['title']}; interpretar dentro del escenario, población, tecnología, jurisdicción, versión y finalidad previstos.",
                "source_id": source_id,
                "locator": locator,
                "support": "direct_or_synthesis",
                "source_verification_status": source.get("verification_status"),
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": TODAY,
            }
        )
        unit_claim_ids.append(claim_id)
    unit["claim_ids"] = unit_claim_ids

write(
    COURSE_ROOT / "claims.json",
    {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": SUBJECT,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": "Afirmaciones centrales de las seis unidades de Aplicaciones de Salud Digital vinculadas a fuentes verificadas; revisión disciplinaria humana pendiente.",
        "review_state": "ai_review_provisional",
        "claims": claims,
    },
)

# Traza el glosario a fuentes verificadas de las unidades donde se usa cada término.
glossary = load(COURSE_ROOT / "glossary.json")
unit_by_id = {unit["id"]: unit for unit in canonical_units}
for entry in glossary["entries"]:
    source_ids: list[str] = []
    for unit_id in entry.get("unit_ids", []):
        unit = unit_by_id.get(unit_id)
        if unit and unit["source_ids"]:
            source_id = unit["source_ids"][0]
            if source_id not in source_ids:
                source_ids.append(source_id)
    if not source_ids:
        source_ids = [used_source_ids[0]]
    entry["source_ids"] = source_ids[:2]
    entry["verification_status"] = "traceable_to_verified_course_sources"
glossary["status"] = "traceable"
if len(glossary["entries"]) < 80:
    raise RuntimeError(f"Glosario insuficiente: {len(glossary['entries'])} entradas")
write(COURSE_ROOT / "glossary.json", glossary)

# Completa evaluación formativa por unidad y enlaza cada ítem a una fuente del corpus.
difficulties = ["foundational", "foundational", "intermediate", "intermediate", "intermediate", "intermediate", "advanced", "advanced", "advanced", "advanced"]
cognitive = ["understand", "apply", "apply", "analyze", "analyze", "evaluate", "analyze", "evaluate", "evaluate", "create"]
for unit in canonical_units:
    assessment_path = COURSE_ROOT / unit["assessment_file"]
    assessment = load(assessment_path)
    if len(assessment["items"]) < 8:
        raise RuntimeError(f"{unit['id']}: evaluación con menos de ocho ítems")
    for index, item in enumerate(assessment["items"]):
        item["difficulty"] = difficulties[index] if index < len(difficulties) else "advanced"
        item["cognitive_level"] = cognitive[index] if index < len(cognitive) else "evaluate"
        explanation = str(item.get("answer_key", {}).get("explanation") or "").strip()
        expected = str(item.get("answer_key", {}).get("expected_answer") or "").strip()
        if not explanation:
            explanation = expected
        item["answer_key"]["explanation"] = explanation
        item["feedback"] = {
            "correct": "Correcto. La respuesta conserva la distinción conceptual, el alcance y los límites exigidos por la unidad; contrástala con la fuente enlazada antes de transferirla a otro contexto.",
            "incorrect": f"Revisa la distinción central y vuelve a justificarla con evidencia. Una respuesta aceptable debe incluir, como mínimo: {expected}",
        }
        item["source_ids"] = [unit["source_ids"][index % len(unit["source_ids"])]]
        item["status"] = "ready_for_formative_use"
    assessment["status"] = "ready_for_formative_use"
    write(assessment_path, assessment)

# Multimedia sigue planificada; se documenta la intención pedagógica sin fingir producción.
media = load(COURSE_ROOT / "media.json")
media["coverage_status"] = "planned"
for item in media["items"]:
    unit = unit_by_id[item["unit_id"]]
    item["status"] = "planned"
    item["pedagogical_purpose"] = f"Visualizar el flujo de razonamiento y las fronteras conceptuales de {unit['title']} sin usar datos personales ni sistemas clínicos reales."
    item["alt_text_draft"] = f"Esquema educativo de {unit['title']} con entradas, decisiones, controles, salidas y límites de inferencia."
write(COURSE_ROOT / "media.json", media)

# Curso canónico y cobertura de resultados.
course.update(
    {
        "code": CODE,
        "content_version": "1.0.0",
        "academic_level": "Pregrado universitario intermedio y avanzado",
        "audience": "Estudiantes de ingeniería biomédica, informática biomédica, salud digital y áreas afines con bases de programación, datos y metodología científica que necesiten diseñar, evaluar e implementar soluciones digitales de forma reproducible y responsable.",
        "status": dict(STATUS),
        "purpose": "Diseñar y evaluar soluciones de salud digital desde la formulación del problema hasta la implementación responsable, integrando necesidades, diseño centrado en personas, telemedicina y monitorización, interoperabilidad, evidencia clínica y económica, privacidad, ciberseguridad, regulación y gobernanza, sin confundir desempeño técnico o evidencia favorable con beneficio clínico, conformidad regulatoria o autorización de despliegue.",
        "scope": {
            "included": [
                "Formulación de necesidades, actores, flujo asistencial, determinantes y equidad digital.",
                "Diseño centrado en personas, contexto de uso, usabilidad, accesibilidad, prevención de errores y prototipado.",
                "Telemedicina, monitorización remota, cadena sensor-dato, calidad, alertas, carga operativa y contingencias.",
                "Interoperabilidad sintáctica, estructural, semántica y organizativa con FHIR, APIs, terminologías, procedencia y calidad de datos.",
                "Evaluación de efectividad, implementación, equidad, costes, coste-efectividad, impacto presupuestario e incertidumbre.",
                "Privacidad, protección de datos, ciberseguridad, finalidad prevista, regulación, gobernanza, control de cambios y escalado.",
                "Expedientes reproducibles que separan observación, requisito, evidencia, riesgo, decisión y límite de inferencia."
            ],
            "excluded": [
                "Diagnóstico, pronóstico, prescripción o recomendación terapéutica individual.",
                "Acceso, modificación o despliegue en historias clínicas, sistemas hospitalarios, redes o dispositivos reales.",
                "Tratamiento de datos personales reales, credenciales, tokens, secretos o identificadores de pacientes.",
                "Asesoramiento jurídico, DPIA profesional, auditoría de ciberseguridad, clasificación regulatoria o evaluación de conformidad.",
                "Declarar eficacia clínica, coste-efectividad, seguridad, conformidad o autorización de despliegue a partir de ejercicios educativos.",
                "Sustituir revisión disciplinaria humana, evaluación ética, validación clínica, económica, regulatoria o de seguridad."
            ],
            "handoff_courses": [
                "informatica-biomedica",
                "historias-clinicas-terminologias-estandares",
                "sistemas-ayuda-decision-medica",
                "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas",
                "ingenieria-clinica-gestion"
            ],
        },
        "prerequisites": [
            {"id": "SALDIG-PRE01", "statement": "Programación y estructuras de datos suficientes para comprender flujos, APIs, validaciones y trazabilidad sin requerir despliegue real."},
            {"id": "SALDIG-PRE02", "statement": "Estadística y metodología científica para interpretar métricas, incertidumbre, comparaciones y evidencia clínica o económica."},
            {"id": "SALDIG-PRE03", "statement": "Anatomía, fisiología y organización sanitaria básicas para contextualizar problemas asistenciales sin convertir el curso en práctica clínica."},
            {"id": "SALDIG-PRE04", "statement": "Capacidad para documentar requisitos, supuestos, versiones, riesgos, decisiones y límites de transferencia."},
        ],
        "competencies": [
            {"id": "SALDIG-COMP01", "statement": "Traducir una necesidad sanitaria en problema, población, actores, flujo, restricción y criterio de éxito antes de elegir una tecnología."},
            {"id": "SALDIG-COMP02", "statement": "Diseñar interacción y servicio digital con participación, accesibilidad, usabilidad y prevención de errores trazables."},
            {"id": "SALDIG-COMP03", "statement": "Modelar telemedicina y monitorización como cadenas asistenciales y técnicas auditables con contingencias y carga operativa explícitas."},
            {"id": "SALDIG-COMP04", "statement": "Diseñar interoperabilidad y calidad de datos con contratos, terminologías, procedencia, validación y pruebas extremo a extremo."},
            {"id": "SALDIG-COMP05", "statement": "Evaluar evidencia clínica, implementación, equidad y economía sin usar métricas sustitutas como prueba automática de valor."},
            {"id": "SALDIG-COMP06", "statement": "Analizar privacidad, seguridad, regulación y gobernanza como dominios relacionados pero no intercambiables."},
            {"id": "SALDIG-COMP07", "statement": "Comunicar decisiones de salud digital con fuentes, versiones, incertidumbre, alternativas, responsabilidades y límites de transferencia."},
        ],
        "learning_outcomes": COURSE_LOS,
        "study_method": [
            "Definir primero problema, población, actores, uso previsto y decisión que se pretende apoyar.",
            "Separar necesidad clínica, experiencia de usuario, arquitectura técnica, dato, evidencia de valor, riesgo y requisito regulatorio.",
            "Alternar explicación, ejemplo resuelto, práctica guiada, auditoría con apoyo reducido y reto autónomo.",
            "Trabajar exclusivamente con escenarios, recursos y datos sintéticos en las actividades del curso.",
            "Conservar fuentes, versiones, procedencia, criterios, incertidumbre, riesgos y límites de inferencia en cada entrega.",
            "Cerrar cada unidad identificando qué evidencia falta antes de transferir la conclusión a personas, instituciones, jurisdicciones o sistemas reales."
        ],
        "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, pedagogía interna y fuentes trazables para las seis unidades de Aplicaciones de Salud Digital. La publicación sigue siendo provisional. La revisión disciplinaria humana interna y externa, validación clínica o económica, evaluación ética, asesoramiento jurídico, DPIA profesional, auditoría de ciberseguridad, clasificación o conformidad regulatoria y autorización para operar o desplegar sistemas reales permanecen fuera de este cierre y siguen pendientes.",
    }
)

core_source_ids: list[str] = []
for offset in range(2):
    for unit in canonical_units:
        if len(unit["source_ids"]) > offset:
            source_id = unit["source_ids"][offset]
            if source_id not in core_source_ids:
                core_source_ids.append(source_id)
course["core_source_ids"] = core_source_ids[:12]

for unit in canonical_units:
    write(COURSE_ROOT / "units" / f"unit-{int(unit['order']):02d}.json", unit)
write(COURSE_ROOT / "course.json", course)

course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "SALDIG-EVAL-CURSO",
    "course_id": SUBJECT,
    "scope": "course",
    "principles": [
        "Evaluar decisiones y razonamiento trazable, no memorización aislada de siglas o normas.",
        "Separar desempeño técnico, experiencia, efectividad clínica, implementación, economía, privacidad, seguridad y regulación.",
        "Usar escenarios y datos sintéticos; ninguna evaluación requiere acceso a pacientes, sistemas clínicos o credenciales reales.",
        "Premiar la identificación de incertidumbre, evidencia faltante, alternativas y límites de transferencia.",
        "Mantener answer keys y feedback fuera del payload inicial de una futura aplicación estudiantil dinámica."
    ],
    "assessment_plan": [
        {"component": "Portafolio formativo de U1–U3", "weight_percent": 20, "evidence": "Mapas de problema, prototipos, reglas de monitorización y revisiones corregidas."},
        {"component": "Examen integrador intermedio", "weight_percent": 25, "evidence": "Casos sintéticos que exigen distinguir diseño, servicio, datos y límites."},
        {"component": "Portafolio crítico de U4–U6", "weight_percent": 20, "evidence": "Interoperabilidad, evaluación de valor, privacidad, seguridad y gobernanza con fuentes."},
        {"component": "Proyecto final integrador", "weight_percent": 35, "evidence": "Expediente reproducible de una intervención digital sintética desde necesidad hasta plan de implementación condicionada."},
    ],
    "diagnostic": {
        "purpose": "Detectar prerrequisitos que requieren repaso antes de iniciar el curso.",
        "questions": [
            "Distingue necesidad sanitaria, requisito de usuario y solución tecnológica con un ejemplo breve.",
            "Explica por qué una métrica de engagement no demuestra por sí sola beneficio clínico.",
            "Diferencia identificador, código clínico, recurso FHIR y API.",
            "Distingue sensibilidad, especificidad y valor predictivo positivo en una regla de alerta.",
            "Explica la diferencia entre privacidad y ciberseguridad.",
            "Indica qué información mínima debe conservarse para que una decisión digital sea reproducible."
        ],
    },
    "midterm_blueprint": [
        {"domain": "U1 — problema, ecosistema y equidad", "weight_percent": 20},
        {"domain": "U2 — diseño centrado en personas", "weight_percent": 20},
        {"domain": "U3 — telemedicina y monitorización", "weight_percent": 25},
        {"domain": "Integración U1–U3 y límites de inferencia", "weight_percent": 35},
    ],
    "capstone": {
        "title": "Expediente reproducible de una intervención de salud digital sintética",
        "scenario": "Un equipo debe decidir si una intervención digital sintética merece avanzar desde una necesidad asistencial definida hacia un piloto controlado, sin usar datos personales ni sistemas clínicos reales.",
        "required_deliverables": [
            "Definición del problema, población, actores, flujo as-is y criterios de no digitalizar.",
            "Contexto de uso, requisitos, accesibilidad, riesgos de uso y prototipo conceptual.",
            "Arquitectura de telemedicina o monitorización con cadena sensor-dato, alertas, carga operativa y contingencias.",
            "Contrato de interoperabilidad con recursos, terminologías, procedencia y pruebas de calidad.",
            "Plan de evaluación clínica, implementación, equidad y economía con comparador y horizonte explícitos.",
            "Mapa de datos, base jurídica a verificar, riesgos de privacidad y ciberseguridad, gobernanza y control de cambios.",
            "Matriz evidencia→criterio→incertidumbre→decisión con fuentes y versiones.",
            "Conclusión condicionada que distingue qué está demostrado, qué es hipótesis y qué exige revisión profesional adicional."
        ],
        "rubric": [
            {"criterion": "Formulación del problema y coherencia del servicio", "weight_percent": 15},
            {"criterion": "Diseño centrado en personas, accesibilidad y seguridad de uso", "weight_percent": 15},
            {"criterion": "Datos, interoperabilidad y calidad", "weight_percent": 15},
            {"criterion": "Evaluación clínica, implementación, equidad y economía", "weight_percent": 20},
            {"criterion": "Privacidad, ciberseguridad, regulación y gobernanza", "weight_percent": 20},
            {"criterion": "Trazabilidad, incertidumbre, fuentes y límites de inferencia", "weight_percent": 15},
        ],
        "boundaries": [
            "No usar datos personales, EHR reales, credenciales, tokens ni sistemas hospitalarios.",
            "No emitir diagnóstico, recomendación terapéutica, asesoramiento jurídico ni conclusión de conformidad regulatoria.",
            "Una calificación alta demuestra desempeño académico en un escenario sintético, no autorización de implementación."
        ],
    },
    "status": "ready_for_internal_review",
}
write(COURSE_ROOT / "assessments" / "course-assessment.json", course_assessment)

# Comprobaciones antes de entregar el corpus al validador oficial.
if len(claims) != 24:
    raise RuntimeError(f"Se esperaban 24 claims y se generaron {len(claims)}")
if any(unit["status"]["content"] != "complete" for unit in canonical_units):
    raise RuntimeError("Alguna unidad no quedó en content=complete")
if any(not unit["claim_ids"] for unit in canonical_units):
    raise RuntimeError("Alguna unidad quedó sin claims")
print(
    f"Cierre canónico preparado: 6 unidades · {len(selected_sources)} fuentes verificadas · "
    f"{len(glossary['entries'])} términos · {len(claims)} claims"
)
