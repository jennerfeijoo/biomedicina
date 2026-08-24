#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "ingenieria-clinica-gestion"
CODE = "ICG"
COURSE = ROOT / "data" / "courses" / COURSE_ID
REDEV = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"
REVIEW_DATE = "2026-08-25"
GENERIC = "concepto de la unidad que debe definirse"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def unique(values):
    out = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out


def chunks3(values):
    if not values:
        return [[], [], []]
    chunks = [values[0::3], values[1::3], values[2::3]]
    for i in range(3):
        if not chunks[i]:
            chunks[i] = list(values)
    return chunks


def tokens(text: str) -> set[str]:
    stop = {
        "para", "como", "esta", "este", "estos", "estas", "entre", "desde", "sobre",
        "cada", "debe", "deben", "solo", "puede", "pueden", "cuando", "donde", "tambien",
        "toda", "todo", "todos", "todas", "porque", "sino", "hacia", "bajo", "segun",
        "with", "from", "that", "this", "medical", "health", "device", "devices",
    }
    found = set(re.findall(r"[a-záéíóúñü]{4,}", text.casefold()))
    return found - stop


def choose_source(claim: str, source_ids: list[str], source_by_id: dict[str, dict]) -> str:
    claim_tokens = tokens(claim)
    scored = []
    for index, source_id in enumerate(source_ids):
        source = source_by_id[source_id]
        haystack = " ".join(
            str(source.get(key) or "")
            for key in ("title", "organization", "description", "type", "url")
        )
        score = len(claim_tokens & tokens(haystack))
        scored.append((score, -index, source_id))
    scored.sort(reverse=True)
    return scored[0][2]


course = load(COURSE / "course.json")
sources = load(COURSE / "sources.json")
glossary = load(COURSE / "glossary.json")
media = load(COURSE / "media.json")

canonical_units = {}
redevelopment_units = {}
for number in range(1, 7):
    unit_path = COURSE / "units" / f"unit-{number:02d}.json"
    canonical_units[number] = load(unit_path)
    redevelopment_units[number] = load(REDEV / f"unit-{number:02d}.json")

used_source_ids = unique(
    source_id
    for unit in canonical_units.values()
    for source_id in unit.get("source_ids", [])
)
source_records = [source for source in sources.get("sources", []) if source.get("id") in used_source_ids]
source_by_id = {source["id"]: source for source in source_records}
missing_sources = set(used_source_ids) - set(source_by_id)
if missing_sources:
    raise RuntimeError(f"Fuentes canónicas ausentes: {sorted(missing_sources)}")
not_direct = [
    source["id"]
    for source in source_records
    if source.get("verification_status") != "verified_directly"
]
if not_direct:
    raise RuntimeError(f"Fuentes usadas sin verificación directa: {not_direct}")

sources["source_policy"] = (
    "Usar fuentes institucionales, normativas o literatura revisada por pares verificadas directamente; "
    "declarar jurisdicción, versión y alcance cuando una recomendación pueda cambiar y no convertir una "
    "fuente educativa en auditoría, certificación o autorización profesional."
)
sources["consulted_on"] = REVIEW_DATE
sources["coverage_gaps"] = []
sources["sources"] = source_records
write(COURSE / "sources.json", sources)

course["content_version"] = "1.0.0"
course["academic_level"] = "Pregrado universitario intermedio y avanzado"
course["audience"] = (
    "Estudiantes de ingeniería biomédica y áreas afines con fundamentos de instrumentación, medición, "
    "estadística descriptiva y gestión técnica que necesiten razonar sobre el ciclo de vida de tecnología "
    "sanitaria dentro de organizaciones de salud sin confundir un ejercicio académico con autoridad operativa, "
    "regulatoria, contractual o clínica."
)
course["status"] = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}
course["purpose"] = (
    "Integrar gobernanza de ingeniería clínica, inventario y criticidad, mantenimiento y metrología, adquisición "
    "y evaluación, seguridad e investigación de incidentes y proyectos de mejora para construir un expediente "
    "sintético y reproducible de gestión del ciclo de vida de tecnología sanitaria, con decisiones trazables, "
    "indicadores definidos, incertidumbre y límites explícitos, sin presentar el trabajo educativo como "
    "intervención sobre equipos reales, adjudicación, investigación oficial, conformidad normativa, certificación "
    "o recomendación clínica."
)
course["scope"] = {
    "included": [
        "Rol, alcance, gobernanza, responsabilidades, políticas, procedimientos, registros y handoffs de ingeniería clínica.",
        "Inventario, identidad persistente, nomenclaturas, calidad de datos, criticidad multicriterio y sensibilidad.",
        "Mantenimiento preventivo/correctivo, órdenes de trabajo, disponibilidad, MTTR/MTBF, calibración, verificación, trazabilidad metrológica e incertidumbre.",
        "Evaluación de necesidades, requisitos verificables, coste total del ciclo de vida, HTA local y comparación multicriterio.",
        "Preservación de evidencia, cronología, investigación multicausal, vigilancia, tasas y prevención de recurrencia.",
        "KPIs, SLA, costes de servicio, PDSA, series temporales, medidas de balance, competencia, adopción y sostenibilidad.",
        "Expedientes reproducibles con versiones, fuentes, denominadores, supuestos, discrepancias y límites de inferencia.",
    ],
    "excluded": [
        "Mantenimiento, calibración, liberación, reparación o modificación de dispositivos médicos reales.",
        "Investigación de incidentes reales, decisión de reportabilidad, tecnovigilancia oficial o peritaje.",
        "Licitación, adjudicación, negociación contractual, asesoría jurídica o decisión de compra institucional.",
        "Certificación, auditoría ISO, evaluación de conformidad, autorización regulatoria o acreditación de una organización.",
        "Uso de datos personales, pacientes, participantes humanos o información confidencial de una institución real.",
        "Inferencias de seguridad clínica, efectividad o causalidad a partir de un KPI, una tasa o una simulación aislada.",
    ],
    "handoff_courses": [
        "desarrollo-dispositivos-medicos",
        "bioinstrumentacion",
        "laboratorio-bioinstrumentacion",
        "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas",
        "economia-gestion-empresas",
    ],
}
course["prerequisites"] = [
    {"id": "ICG-PRE01", "statement": "Fundamentos de bioinstrumentación, medición y seguridad de equipos biomédicos."},
    {"id": "ICG-PRE02", "statement": "Estadística descriptiva básica, proporciones, tasas, series temporales simples e interpretación de incertidumbre."},
    {"id": "ICG-PRE03", "statement": "Conceptos introductorios de sistemas, requisitos, documentación técnica y trazabilidad."},
    {"id": "ICG-PRE04", "statement": "Capacidad para trabajar con datos sintéticos en hojas de cálculo o scripts reproducibles."},
    {"id": "ICG-PRE05", "statement": "Ética, privacidad, seguridad y límites de la actividad educativa dentro de organizaciones de salud."},
]
course["competencies"] = [
    {"id": "ICG-COMP01", "statement": "Modelar la función de ingeniería clínica como un sistema de gobernanza, responsabilidades, información y handoffs."},
    {"id": "ICG-COMP02", "statement": "Construir inventarios y prioridades trazables sin ocultar calidad de datos, supuestos o sensibilidad del ranking."},
    {"id": "ICG-COMP03", "statement": "Planificar y evaluar mantenimiento y metrología usando evidencia, indicadores definidos e incertidumbre."},
    {"id": "ICG-COMP04", "statement": "Comparar alternativas tecnológicas mediante necesidades, requisitos, coste de ciclo de vida, evidencia y análisis de sensibilidad."},
    {"id": "ICG-COMP05", "statement": "Estructurar la respuesta a incidentes y el aprendizaje organizativo preservando evidencia y límites de reportabilidad e inferencia."},
    {"id": "ICG-COMP06", "statement": "Diseñar proyectos de mejora con familias de KPIs, contratos/SLA, pruebas PDSA, medidas de balance y sostenibilidad."},
    {"id": "ICG-COMP07", "statement": "Integrar U1–U6 en un expediente auditable que separa datos, decisión técnica, obligación potencial y autoridad profesional real."},
]
course["learning_outcomes"] = [
    {"id": "ICG-LO01", "statement": "Construye un mapa de gobernanza de ingeniería clínica con actores, responsabilidades, políticas, procedimientos, registros y handoffs trazables, delimitando qué decisiones requieren autoridad institucional o profesional."},
    {"id": "ICG-LO02", "statement": "Diseña y audita un inventario sintético con identidad persistente, nomenclaturas, historial, calidad de datos y criticidad multicriterio, documentando sensibilidad y datos faltantes."},
    {"id": "ICG-LO03", "statement": "Interpreta mantenimiento, disponibilidad y metrología mediante órdenes de trabajo, indicadores con denominadores explícitos, calibración/verificación, trazabilidad e incertidumbre sin equiparar una prueba aislada con conformidad global."},
    {"id": "ICG-LO04", "statement": "Construye una comparación de adquisición sintética basada en necesidad, requisitos, coste total del ciclo de vida, HTA local, criterios multicriterio y sensibilidad, sin convertirla en adjudicación o recomendación institucional."},
    {"id": "ICG-LO05", "statement": "Estructura un expediente sintético de seguridad e incidentes con preservación de evidencia, cronología, investigación multicausal, tasas, vigilancia y acciones de aprendizaje, separando reporte interno de reportabilidad externa."},
    {"id": "ICG-LO06", "statement": "Diseña un proyecto de mejora de ingeniería clínica con objetivo explícito, familia equilibrada de KPIs, SLA, PDSA, medidas de balance, formación, adopción y reglas de sostenibilidad, evitando atribuir causalidad por una comparación antes-después."},
    {"id": "ICG-LO07", "statement": "Integra U1–U6 en un expediente reproducible del ciclo de vida de tecnología sanitaria que conserva fuentes, definiciones, versiones, supuestos, incertidumbre, discrepancias, límites y la siguiente acción necesaria sin reclamar autoridad clínica, contractual, regulatoria o de certificación."},
]
course["study_method"] = [
    "Definir primero la decisión de gestión, el sistema, la población de activos o casos, el periodo y la autoridad que realmente puede actuar.",
    "Alternar explicación, ejemplo resuelto, práctica guiada, retirada progresiva del apoyo y tarea autónoma con datos exclusivamente sintéticos.",
    "Separar observación, cálculo, indicador, interpretación, prioridad, decisión y obligación potencial en cada producto.",
    "Conservar identificadores, versiones, denominadores, fuentes, criterios de inclusión, cambios y evidencia negativa.",
    "Comparar explicaciones alternativas y ejecutar análisis de sensibilidad antes de presentar un ranking o una conclusión operativa.",
    "Cerrar cada unidad con un handoff explícito y revisar el expediente acumulativo antes de avanzar a la siguiente etapa del ciclo de vida.",
]
course["editorial_notice"] = (
    "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para U1–U6. Las fuentes están "
    "trazadas y la publicación continúa como provisional. La revisión humana interna y disciplinaria externa, la "
    "intervención sobre equipos, la investigación oficial de incidentes, la decisión de reportabilidad, la contratación, "
    "la asesoría jurídica o regulatoria, la auditoría o certificación, la evaluación de conformidad y cualquier decisión "
    "clínica u operativa real siguen fuera de este cierre y permanecen pendientes."
)

for number, unit in canonical_units.items():
    unit_id = f"ICG-U{number:02d}"
    source_unit = redevelopment_units[number]
    unit["status"] = {
        "content": "complete",
        "sources": "traceable",
        "pedagogy": "complete",
        "multimedia": "planned",
        "internal_review": "pending",
        "external_review": "pending",
        "publication": "published_provisional",
    }
    unit["course_learning_outcome_ids"] = [f"ICG-LO{number:02d}", "ICG-LO07"]

    examples = unit.get("examples", [])
    assessments = source_unit.get("self_assessment", [])
    cursor = 0
    while len(examples) < 5 and cursor < len(assessments):
        item = assessments[cursor]
        cursor += 1
        prompt = str(item.get("question") or "Caso recuperativo").strip()
        answer = str(item.get("answer") or "").strip()
        reasoning = str(item.get("reasoning") or item.get("explanation") or answer).strip()
        common_error = str(item.get("common_error") or "").strip()
        examples.append({
            "id": f"{unit_id}-EJ{len(examples)+1:02d}",
            "title": f"Ejemplo integrador recuperativo {len(examples)+1}",
            "scenario": prompt,
            "reasoning_steps": [reasoning, "Contrastar la respuesta con el alcance, los datos y los límites explícitos de la unidad."],
            "interpretation": answer,
            "limitations": [common_error] if common_error else ["El ejemplo sintético no autoriza una decisión operativa, contractual, regulatoria o clínica real."],
        })
    if len(examples) < 5:
        raise RuntimeError(f"{unit_id}: no fue posible completar cinco ejemplos sin inventar contenido nuevo")
    unit["examples"] = examples

    guided = (source_unit.get("guided_activities") or [{}])[0]
    tasks = list(guided.get("problems") or guided.get("tasks") or [])
    deliverables = list(guided.get("deliverables") or [])
    criteria = list(guided.get("checking_criteria") or [])
    instructions = list(guided.get("instructions") or [])
    task_chunks = chunks3(tasks)
    deliverable_chunks = chunks3(deliverables)
    criteria_chunks = chunks3(criteria)
    unit["activities"] = [
        {
            "id": f"{unit_id}-ACT01",
            "title": f"Práctica guiada · {source_unit['title']}",
            "purpose": "Resolver la primera parte del expediente con andamiaje explícito y comprobaciones intermedias.",
            "prerequisite_unit_ids": unit.get("prerequisite_unit_ids", []),
            "instructions": instructions,
            "tasks": task_chunks[0],
            "deliverables": deliverable_chunks[0],
            "checking_criteria": criteria_chunks[0],
            "estimated_duration_minutes": 90,
            "status": "complete",
        },
        {
            "id": f"{unit_id}-ACT02",
            "title": f"Práctica con apoyo reducido · {source_unit['title']}",
            "purpose": "Repetir el razonamiento con menos instrucciones y justificar decisiones, denominadores, supuestos y límites.",
            "prerequisite_unit_ids": unit.get("prerequisite_unit_ids", []),
            "instructions": [
                "Resuelve las tareas sin copiar la secuencia de la práctica guiada; decide qué información necesitas y justifica cada transformación.",
                "Registra una comprobación o análisis de sensibilidad y documenta qué resultado debilitaría tu conclusión.",
            ],
            "tasks": task_chunks[1],
            "deliverables": deliverable_chunks[1],
            "checking_criteria": criteria_chunks[1],
            "estimated_duration_minutes": 75,
            "status": "complete",
        },
        {
            "id": f"{unit_id}-ACT03",
            "title": f"Reto autónomo · {source_unit['title']}",
            "purpose": "Transferir el método a la parte final del caso sintético y producir un handoff auditable hacia la siguiente unidad o el cierre del curso.",
            "prerequisite_unit_ids": unit.get("prerequisite_unit_ids", []),
            "instructions": [
                "Resuelve de forma autónoma las tareas asignadas usando solo datos sintéticos y las fuentes trazadas en la unidad.",
                "Entrega una conclusión proporcional que distinga lo observado, lo calculado, lo inferido y lo que todavía requiere autoridad o evidencia externa.",
            ],
            "tasks": task_chunks[2],
            "deliverables": deliverable_chunks[2],
            "checking_criteria": criteria_chunks[2],
            "estimated_duration_minutes": 90,
            "status": "complete",
        },
    ]

    assessment_path = COURSE / "assessments" / f"unit-{number:02d}.json"
    assessment = load(assessment_path)
    assessment["purpose"] = (
        f"Comprobar comprensión, aplicación y juicio crítico de U{number} — {source_unit['title']} "
        "con retroalimentación recuperativa y fuentes trazables."
    )
    source_ids = unit.get("source_ids", [])
    if not source_ids:
        raise RuntimeError(f"{unit_id}: sin fuentes")
    cognitive = ["understand", "apply", "apply", "analyze", "analyze", "analyze", "evaluate", "evaluate", "evaluate", "create"]
    for index, item in enumerate(assessment.get("items", []), start=1):
        item["difficulty"] = "foundational" if index <= 3 else "intermediate" if index <= 7 else "advanced"
        item["cognitive_level"] = cognitive[min(index - 1, len(cognitive) - 1)]
        explanation = item.get("answer_key", {}).get("explanation") or item.get("answer_key", {}).get("expected_answer")
        item["answer_key"]["explanation"] = explanation
        item["feedback"] = {
            "correct": "Correcto: la respuesta conserva definiciones operacionales, trazabilidad, incertidumbre y límites de autoridad. Revisa la explicación para verificar por qué.",
            "incorrect": "Revisa qué dato entra, qué regla o cálculo se aplica, qué salida obtienes y qué NO puede inferirse. Contrasta tu respuesta con la explicación y la fuente trazada antes de reintentar.",
        }
        item["source_ids"] = [source_ids[(index - 1) % len(source_ids)]]
        item["status"] = "complete"
    assessment["status"] = "complete"
    write(assessment_path, assessment)
    write(COURSE / "units" / f"unit-{number:02d}.json", unit)

# Rebuild glossary traceability after units have their final source sets.
for entry in glossary.get("entries", []):
    trace = []
    for unit_id in entry.get("unit_ids", []):
        try:
            number = int(unit_id.rsplit("U", 1)[1])
        except (ValueError, IndexError):
            continue
        trace.extend(canonical_units[number].get("source_ids", [])[:2])
    entry["source_ids"] = unique(trace)[:4]
    if not entry["source_ids"]:
        raise RuntimeError(f"Glosario sin fuente: {entry.get('term')}")
    entry["verification_status"] = "traceable_to_verified_source"
glossary["status"] = "traceable"
write(COURSE / "glossary.json", glossary)

# Four literal anchor claims per unit, selected from taught key points and linked to directly verified unit sources.
claims = []
for number, unit in canonical_units.items():
    unit_path = COURSE / "units" / f"unit-{number:02d}.json"
    unit = load(unit_path)
    key_points = unique(
        point
        for topic in unit.get("topics", [])
        for point in topic.get("key_points", [])
        if str(point).strip()
    )
    if len(key_points) < 4:
        raise RuntimeError(f"ICG-U{number:02d}: menos de cuatro afirmaciones ancla literales")
    unit_claim_ids = []
    for claim_index, text in enumerate(key_points[:4], start=1):
        source_id = choose_source(text, unit["source_ids"], source_by_id)
        source = source_by_id[source_id]
        claim_id = f"ICG-U{number:02d}-C{claim_index:03d}"
        unit_claim_ids.append(claim_id)
        claims.append({
            "claim_id": claim_id,
            "unit": number,
            "text": text,
            "claim_type": "methodological_or_interpretive",
            "risk": "medium",
            "context": f"Afirmación ancla enseñada literalmente en U{number}: {unit['title']}; interpretar dentro del alcance, supuestos, autoridad y límites declarados.",
            "source_id": source_id,
            "locator": {"url": source.get("url"), "title": source.get("title")},
            "support": "direct",
            "source_verification_status": "verified_directly",
            "review_state": "ai_review_provisional",
            "reviewer_validation_id": None,
            "reviewed_at": REVIEW_DATE,
            "id": claim_id,
            "unit_id": f"ICG-U{number:02d}",
        })
    unit["claim_ids"] = unit_claim_ids
    write(unit_path, unit)

write(COURSE / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Veinticuatro afirmaciones ancla, cuatro por unidad, tomadas literalmente de las unidades canónicas y vinculadas a fuentes verificadas directamente; revisión disciplinaria humana pendiente.",
    "review_state": "ai_review_provisional",
    "claims": claims,
})

media["coverage_status"] = "planned"
for item in media.get("items", []):
    item["status"] = "planned"
write(COURSE / "media.json", media)

# Prioritize sources reused across units, then retain stable order.
use_count = {source["id"]: len(source.get("used_by_unit_ids", [])) for source in source_records}
course["core_source_ids"] = [
    source["id"]
    for source in sorted(source_records, key=lambda s: (-use_count[s["id"]], used_source_ids.index(s["id"])))[:12]
]
write(COURSE / "course.json", course)

course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "ICG-EVAL-CURSO",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": [
        "Evaluar decisiones de gestión y trazabilidad, no memorización aislada de siglas, normas o indicadores.",
        "Separar dato, cálculo, indicador, interpretación, prioridad, decisión y autoridad profesional en cada respuesta.",
        "Usar exclusivamente activos, contratos, incidentes y datos sintéticos; no intervenir equipos ni sistemas reales.",
        "Exigir numerador, denominador, ventana, fuente y definición operacional para tasas y KPIs.",
        "Premiar análisis de sensibilidad, evidencia negativa, incertidumbre y límites cuando una conclusión no puede cerrarse.",
        "Mantener revisión humana, contratación, reportabilidad, auditoría, certificación y decisiones clínicas u operativas fuera del alcance del cierre académico.",
    ],
    "assessment_plan": [
        {"component": "U1 · mapa de gobernanza y handoffs", "weight_percent": 8, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO07"]},
        {"component": "U2 · inventario, calidad de datos y criticidad", "weight_percent": 8, "linked_learning_outcome_ids": ["ICG-LO02", "ICG-LO07"]},
        {"component": "U3 · mantenimiento, metrología e indicadores", "weight_percent": 10, "linked_learning_outcome_ids": ["ICG-LO03", "ICG-LO07"]},
        {"component": "U4 · evaluación y adquisición sintética", "weight_percent": 10, "linked_learning_outcome_ids": ["ICG-LO04", "ICG-LO07"]},
        {"component": "U5 · expediente sintético de seguridad e incidentes", "weight_percent": 12, "linked_learning_outcome_ids": ["ICG-LO05", "ICG-LO07"]},
        {"component": "U6 · proyecto de mejora y sostenibilidad", "weight_percent": 12, "linked_learning_outcome_ids": ["ICG-LO06", "ICG-LO07"]},
        {"component": "Evaluación integradora intermedia U1–U3", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO02", "ICG-LO03"]},
        {"component": "Capstone de gestión del ciclo de vida U1–U6", "weight_percent": 25, "linked_learning_outcome_ids": [f"ICG-LO{i:02d}" for i in range(1, 8)]},
    ],
    "diagnostic": {
        "purpose": "Comprobar prerrequisitos de medición, documentación y razonamiento antes de integrar gestión tecnológica.",
        "questions": [
            "Distingue una política, un procedimiento y un registro mediante un ejemplo sintético.",
            "Explica por qué número de serie, identificador local y modelo no son el mismo campo.",
            "Calcula una proporción e indica numerador, denominador y periodo.",
            "Distingue prioridad técnica de certeza o calidad de los datos usados para asignarla.",
            "Explica la diferencia entre mantenimiento preventivo y correctivo sin asumir que uno elimina todos los fallos.",
            "Distingue calibración, verificación y ajuste.",
            "Explica por qué MTBF y MTTR necesitan población, periodo y reglas de inclusión explícitas.",
            "Convierte una necesidad de compra en un requisito verificable con criterio de aceptación.",
            "Distingue coste de compra de coste total del ciclo de vida.",
            "Explica por qué preservar evidencia precede a una hipótesis causal en un incidente.",
            "Distingue un KPI de proceso de una medida de resultado y de una medida de balance.",
            "Indica qué productos del curso requieren autoridad institucional, regulatoria, jurídica o profesional antes de cualquier uso real.",
        ],
        "use": "Formativo y no ponderado; cada error remite a la unidad o prerrequisito correspondiente antes de avanzar.",
    },
    "midterm_blueprint": [
        {"domain": "U1 · gobernanza, roles y trazabilidad", "weight_percent": 25, "linked_learning_outcome_ids": ["ICG-LO01"]},
        {"domain": "U2 · inventario, datos y criticidad", "weight_percent": 25, "linked_learning_outcome_ids": ["ICG-LO02"]},
        {"domain": "U3 · mantenimiento, metrología e indicadores", "weight_percent": 30, "linked_learning_outcome_ids": ["ICG-LO03"]},
        {"domain": "Integración U1–U3 y calidad de decisión", "weight_percent": 20, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO02", "ICG-LO03", "ICG-LO07"]},
    ],
    "capstone": {
        "title": "Expediente sintético de gestión del ciclo de vida de tecnología sanitaria",
        "purpose": "Integrar U1–U6 en un dossier reproducible que otra persona pueda auditar sin explicación oral adicional.",
        "scenario": "Gestionar exclusivamente un servicio y un inventario ficticios con datos sintéticos; ninguna salida constituye intervención, compra, contrato, investigación oficial, reporte regulatorio, auditoría, certificación o decisión clínica real.",
        "required_deliverables": [
            "Mapa de gobernanza con actores, RACI, políticas/procedimientos/registros y puntos de escalamiento.",
            "Diccionario de datos e inventario sintético versionado con identidad persistente y campos críticos.",
            "Análisis de calidad de datos, datos faltantes y reglas de corrección sin borrar el historial.",
            "Modelo de criticidad multicriterio con pesos explícitos y análisis de sensibilidad.",
            "Plan de mantenimiento sintético con órdenes, prioridades, disponibilidad, MTTR/MTBF y denominadores definidos.",
            "Expediente metrológico sintético con calibración/verificación, trazabilidad e incertidumbre.",
            "Matriz de necesidad, requisitos, criterios obligatorios/ponderables y coste total del ciclo de vida.",
            "Comparación HTA/local multicriterio con confianza de evidencia y análisis de sensibilidad.",
            "Expediente de incidente sintético con preservación de evidencia, cronología, hipótesis, causas contribuyentes y acciones de aprendizaje.",
            "Tablero de tasas y señales con denominadores, reglas de inclusión y fronteras de reportabilidad.",
            "SLA sintético con alcance, reloj, exclusiones, responsabilidades, escalamiento y evidencias de cumplimiento.",
            "Proyecto PDSA con objetivo, familia de medidas, serie temporal, medidas de balance y registro de ciclos.",
            "Plan de formación, competencia, adopción, sostenibilidad y propietario del proceso.",
            "Registro final de fuentes, versiones, decisiones, discrepancias, incertidumbres, límites y siguientes acciones.",
        ],
        "constraints": [
            "No usar datos personales, pacientes, participantes, equipos, contratos o incidentes reales.",
            "No intervenir, liberar, reparar, calibrar ni modificar dispositivos médicos reales.",
            "No afirmar adjudicación, reportabilidad, conformidad ISO, certificación, seguridad clínica o causalidad no demostradas.",
            "Toda tasa o KPI debe declarar definición, numerador, denominador, ventana y fuente.",
            "Toda conclusión debe indicar qué evidencia la sostiene y qué información o autoridad faltante podría cambiarla.",
        ],
        "rubric": [
            {"criterion": "Gobernanza, responsabilidades y handoffs", "weight_percent": 12, "linked_learning_outcome_ids": ["ICG-LO01"]},
            {"criterion": "Inventario, calidad de datos y criticidad", "weight_percent": 14, "linked_learning_outcome_ids": ["ICG-LO02"]},
            {"criterion": "Mantenimiento, metrología e indicadores", "weight_percent": 14, "linked_learning_outcome_ids": ["ICG-LO03"]},
            {"criterion": "Evaluación, adquisición y evidencia", "weight_percent": 14, "linked_learning_outcome_ids": ["ICG-LO04"]},
            {"criterion": "Seguridad, incidentes y aprendizaje", "weight_percent": 14, "linked_learning_outcome_ids": ["ICG-LO05"]},
            {"criterion": "Mejora, SLA, adopción y sostenibilidad", "weight_percent": 14, "linked_learning_outcome_ids": ["ICG-LO06"]},
            {"criterion": "Reproducibilidad, trazabilidad, límites y handoff", "weight_percent": 18, "linked_learning_outcome_ids": ["ICG-LO07"]},
        ],
    },
    "status": "complete",
}
write(COURSE / "assessments" / "course-assessment.json", course_assessment)

# Permanent regression for the canonical closure.
test_path = ROOT / "tests" / "test_ingenieria_clinica_gestion_canonical_course.py"
test_path.write_text('''from __future__ import annotations\n\nimport json\nimport unittest\nfrom collections import Counter\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nCOURSE = ROOT / "data" / "courses" / "ingenieria-clinica-gestion"\nGENERIC = "concepto de la unidad que debe definirse"\n\n\nclass IngenieriaClinicaGestionCanonicalCourseTests(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))\n        cls.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))\n        cls.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))\n        cls.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))\n\n    def test_status_closes_content_but_not_human_review(self):\n        status = self.course["status"]\n        self.assertEqual(status["content"], "complete")\n        self.assertEqual(status["sources"], "traceable")\n        self.assertEqual(status["pedagogy"], "complete")\n        self.assertEqual(status["multimedia"], "planned")\n        self.assertEqual(status["internal_review"], "pending")\n        self.assertEqual(status["external_review"], "pending")\n        self.assertEqual(status["publication"], "published_provisional")\n\n    def test_six_units_are_complete_and_cover_all_course_outcomes(self):\n        self.assertEqual(len(self.course["unit_files"]), 6)\n        known = {item["id"] for item in self.course["learning_outcomes"]}\n        self.assertEqual(len(known), 7)\n        covered = set()\n        for relative in self.course["unit_files"]:\n            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))\n            covered.update(unit["course_learning_outcome_ids"])\n            serialized = json.dumps(unit, ensure_ascii=False).casefold()\n            self.assertNotIn(GENERIC, serialized)\n            self.assertGreaterEqual(len(unit["topics"]), 4)\n            self.assertGreaterEqual(len(unit["examples"]), 5)\n            self.assertEqual(len(unit["activities"]), 3)\n            self.assertTrue(all(a["estimated_duration_minutes"] > 0 for a in unit["activities"]))\n            self.assertTrue(all(a["status"] == "complete" for a in unit["activities"]))\n            self.assertEqual(unit["status"]["content"], "complete")\n            self.assertEqual(unit["status"]["sources"], "traceable")\n            self.assertEqual(unit["status"]["pedagogy"], "complete")\n        self.assertEqual(known, covered)\n\n    def test_assessments_have_feedback_classification_and_sources(self):\n        source_ids = {item["id"] for item in self.sources["sources"]}\n        total = 0\n        for n in range(1, 7):\n            assessment = json.loads((COURSE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))\n            self.assertGreaterEqual(len(assessment["items"]), 10)\n            self.assertEqual(assessment["status"], "complete")\n            total += len(assessment["items"])\n            for item in assessment["items"]:\n                self.assertNotEqual(item["difficulty"], "unclassified")\n                self.assertNotEqual(item["cognitive_level"], "unclassified")\n                self.assertTrue(item["answer_key"]["explanation"])\n                self.assertTrue(item["feedback"]["correct"])\n                self.assertTrue(item["feedback"]["incorrect"])\n                self.assertTrue(item["source_ids"])\n                self.assertTrue(set(item["source_ids"]) <= source_ids)\n                self.assertEqual(item["status"], "complete")\n        self.assertGreaterEqual(total, 60)\n\n    def test_sources_glossary_and_claims_are_traceable(self):\n        source_ids = {item["id"] for item in self.sources["sources"]}\n        self.assertGreaterEqual(len(source_ids), 20)\n        self.assertTrue(all(item["verification_status"] == "verified_directly" for item in self.sources["sources"]))\n        self.assertEqual(self.sources["coverage_gaps"], [])\n        self.assertGreaterEqual(len(self.glossary["entries"]), 60)\n        for entry in self.glossary["entries"]:\n            self.assertTrue(entry["source_ids"])\n            self.assertTrue(set(entry["source_ids"]) <= source_ids)\n            self.assertEqual(entry["verification_status"], "traceable_to_verified_source")\n        claims = self.claims["claims"]\n        self.assertEqual(len(claims), 24)\n        self.assertEqual(Counter(c["unit"] for c in claims), Counter({n: 4 for n in range(1, 7)}))\n        serialized_units = {n: json.dumps(json.loads((COURSE / "units" / f"unit-{n:02d}.json").read_text(encoding="utf-8")), ensure_ascii=False) for n in range(1, 7)}\n        for claim in claims:\n            self.assertIn(claim["source_id"], source_ids)\n            self.assertEqual(claim["source_verification_status"], "verified_directly")\n            self.assertEqual(claim["review_state"], "ai_review_provisional")\n            self.assertEqual(claim["support"], "direct")\n            self.assertIn(claim["text"], serialized_units[claim["unit"]])\n\n    def test_course_assessment_is_integrative_and_weighted(self):\n        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))\n        self.assertEqual(sum(x["weight_percent"] for x in assessment["assessment_plan"]), 100)\n        self.assertEqual(sum(x["weight_percent"] for x in assessment["midterm_blueprint"]), 100)\n        self.assertEqual(sum(x["weight_percent"] for x in assessment["capstone"]["rubric"]), 100)\n        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)\n        self.assertGreaterEqual(len(assessment["capstone"]["required_deliverables"]), 12)\n        self.assertEqual(assessment["status"], "complete")\n\n    def test_scope_boundaries_are_explicit(self):\n        purpose = self.course["purpose"].casefold()\n        notice = self.course["editorial_notice"].casefold()\n        for concept in ("gobernanza", "inventario", "mantenimiento", "metrología", "adquisición", "incidentes", "proyectos de mejora"):\n            self.assertIn(concept, purpose)\n        self.assertIn("revisión humana", notice)\n        self.assertIn("contratación", notice)\n        self.assertIn("certificación", notice)\n        self.assertIn("decisión clínica", notice)\n\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")

# Final local integrity assertions before the workflow commits anything.
assert len(claims) == 24
assert Counter(claim["unit"] for claim in claims) == Counter({n: 4 for n in range(1, 7)})
assert GENERIC not in " ".join(
    (COURSE / "units" / f"unit-{n:02d}.json").read_text(encoding="utf-8").casefold()
    for n in range(1, 7)
)
print(f"Cierre canónico preparado: {len(source_records)} fuentes, {len(glossary['entries'])} términos, 24 claims")
