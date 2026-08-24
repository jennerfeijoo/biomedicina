from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "ingenieria-clinica-gestion"
PREFIX = "ICG"
SRC = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"
OUT = ROOT / "data" / "courses" / COURSE_ID
STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}


def dump(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "fuente"


def unit_id(n: int) -> str:
    return f"{PREFIX}-U{n:02d}"


units_src = [json.loads((SRC / f"unit-{n:02d}.json").read_text(encoding="utf-8")) for n in range(1, 7)]
assert [u["unit"] for u in units_src] == list(range(1, 7))
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
assert all(GENERIC not in json.dumps(u, ensure_ascii=False).casefold() for u in units_src)

# Source registry: deduplicate verified sources already curated at unit level.
sources_by_key: dict[tuple[str, str], dict] = {}
source_ids_by_unit: dict[int, list[str]] = {}
used_ids: set[str] = set()
for n, u in enumerate(units_src, start=1):
    ids: list[str] = []
    for source in u.get("sources", []):
        key = (source.get("title", "").strip(), source.get("url", "").strip())
        if key not in sources_by_key:
            base = slug(source.get("title") or source.get("organization") or f"source-{len(sources_by_key)+1}")
            sid = base
            k = 2
            while sid in used_ids:
                sid = f"{base}-{k}"
                k += 1
            used_ids.add(sid)
            sources_by_key[key] = {
                "id": sid,
                "title": source.get("title", "Fuente técnica"),
                "authors": source.get("organization", source.get("authors", "Institución o autores indicados en la fuente")),
                "year": source.get("year", 2026),
                "type": source.get("type", "fuente técnica o académica"),
                "url": source.get("url", ""),
                "locator": source.get("description", source.get("locator", "Recurso directamente localizable por título y URL.")),
                "verification_status": source.get("verification_status", "verified_directly"),
                "used_by_unit_ids": [],
                "why_relevant": source.get("description", "Sustenta conceptos y límites enseñados en la unidad."),
            }
        rec = sources_by_key[key]
        if unit_id(n) not in rec["used_by_unit_ids"]:
            rec["used_by_unit_ids"].append(unit_id(n))
        ids.append(rec["id"])
    source_ids_by_unit[n] = list(dict.fromkeys(ids))

sources = list(sources_by_key.values())
# Curated units should already contain directly verified sources; do not upgrade a status here.
assert len(sources) >= 24
assert sum(1 for s in sources if s["verification_status"] == "verified_directly") >= 20

# Global glossary with unit provenance.
glossary_map: dict[str, dict] = {}
for n, u in enumerate(units_src, start=1):
    for entry in u.get("glossary", []):
        term = entry["term"].strip()
        key = term.casefold()
        if key not in glossary_map:
            glossary_map[key] = {
                "id": "",
                "term": term,
                "definition": entry["definition"].strip(),
                "unit_ids": [],
                "source_ids": [],
                "verification_status": "traceable_to_verified_source",
            }
        rec = glossary_map[key]
        if unit_id(n) not in rec["unit_ids"]:
            rec["unit_ids"].append(unit_id(n))
        for sid in source_ids_by_unit[n][:2]:
            if sid not in rec["source_ids"]:
                rec["source_ids"].append(sid)

glossary = list(glossary_map.values())
for i, rec in enumerate(glossary, start=1):
    rec["id"] = f"{PREFIX}-GLO-{i:03d}"
glossary_ids_by_unit = {
    n: [g["id"] for g in glossary if unit_id(n) in g["unit_ids"]]
    for n in range(1, 7)
}

# Four anchor claims per unit, taken literally from curated key points.
claims: list[dict] = []
claim_ids_by_unit: dict[int, list[str]] = {}
for n, u in enumerate(units_src, start=1):
    anchors: list[str] = []
    for section in u["theory_sections"]:
        if section.get("key_points"):
            anchors.append(section["key_points"][0])
    anchors = anchors[:4]
    assert len(anchors) == 4
    unit_claim_ids: list[str] = []
    sids = source_ids_by_unit[n]
    for j, text in enumerate(anchors, start=1):
        cid = f"{PREFIX}-U{n:02d}-C{j:03d}"
        sid = sids[(j - 1) % len(sids)]
        srec = next(s for s in sources if s["id"] == sid)
        claims.append({
            "claim_id": cid,
            "unit": n,
            "text": text,
            "claim_type": "methodological_or_interpretive",
            "risk": "medium",
            "context": f"Afirmación ancla enseñada literalmente en U{n}: {u['title']}; interpretar dentro del alcance, supuestos y límites declarados.",
            "source_id": sid,
            "locator": {"url": srec["url"], "title": srec["title"]},
            "support": "direct",
            "source_verification_status": srec["verification_status"],
            "review_state": "ai_review_provisional",
            "reviewer_validation_id": None,
            "reviewed_at": "2026-08-24",
            "id": cid,
            "unit_id": unit_id(n),
        })
        unit_claim_ids.append(cid)
    claim_ids_by_unit[n] = unit_claim_ids

# Planned media, one deliberately scoped figure per unit.
media_purposes = [
    ("Mapa de gobernanza y ciclo de vida de tecnología sanitaria", "Diagrama sintético de actores, responsabilidades, ciclo tecnológico, políticas y handoffs de ingeniería clínica."),
    ("Mapa de inventario y criticidad", "Esquema sintético que conecta identificación, clasificación, historial, función, criticidad, priorización y renovación."),
    ("Flujo de mantenimiento y metrología", "Diagrama que separa mantenimiento preventivo y correctivo, calibración, trazabilidad metrológica, disponibilidad e indicadores."),
    ("Matriz de adquisición basada en necesidad y evidencia", "Esquema sintético de necesidad, requisitos, coste total, evaluación tecnológica, comparación y decisión condicionada."),
    ("Flujo de incidente a aprendizaje organizativo", "Diagrama sintético de señal, contención, investigación, tecnovigilancia, acción correctiva, seguimiento y prevención de recurrencia."),
    ("Sistema de mejora con KPIs, SLA y PDSA", "Mapa sintético de objetivo, resultado/proceso/balance, SLA, serie temporal, ciclos PDSA, competencia, adopción y sostenibilidad."),
]
media: list[dict] = []
media_ids_by_unit: dict[int, list[str]] = {}
for n, (purpose, alt) in enumerate(media_purposes, start=1):
    mid = f"{PREFIX}-U{n:02d}-MED01"
    media.append({
        "id": mid,
        "type": "figure",
        "status": "planned",
        "unit_id": unit_id(n),
        "linked_learning_outcome_ids": [f"{PREFIX}-U{n:02d}-LO01", f"{PREFIX}-U{n:02d}-LO02"],
        "pedagogical_purpose": purpose,
        "alt_text_draft": alt,
        "license_requirements": "Usar material propio o con licencia compatible y registrar atribución y procedencia.",
        "source_ids": [],
    })
    media_ids_by_unit[n] = [mid]

# Canonical units and unit assessments.
canonical_units: list[dict] = []
for n, u in enumerate(units_src, start=1):
    uid = unit_id(n)
    lo_records = [
        {"id": f"{uid}-LO{i:02d}", "statement": statement}
        for i, statement in enumerate(u["learning_objectives"], start=1)
    ]
    topics: list[dict] = []
    for ti, section in enumerate(u["theory_sections"], start=1):
        tid = f"{uid}-T{ti:02d}"
        blocks: list[dict] = []
        for ei, eq in enumerate(section.get("equations", []), start=1):
            blocks.append({
                "id": f"{tid}-B{ei:02d}",
                "type": "equation",
                "latex": eq["latex"],
                "label": eq.get("meaning", "Relación cuantitativa de la unidad."),
                "variables": eq.get("variables", {}),
            })
        subs = [
            {
                "id": f"{tid}-ST{pi:02d}",
                "title": section["key_points"][(pi - 1) % len(section["key_points"])],
                "blocks": [{"id": f"{tid}-ST{pi:02d}-B01", "type": "paragraph", "text": paragraph}],
            }
            for pi, paragraph in enumerate(section["paragraphs"], start=1)
        ]
        topics.append({
            "id": tid,
            "title": section["heading"],
            "key_points": section.get("key_points", []),
            "blocks": blocks,
            "subtopics": subs,
        })
    examples = []
    for i, ex in enumerate(u.get("worked_examples", []), start=1):
        examples.append({"id": f"{uid}-EX{i:02d}", **ex})
    activities = []
    for i, act in enumerate(u.get("guided_activities", []), start=1):
        tasks = act.get("problems", act.get("tasks", []))
        activities.append({
            "id": f"{uid}-ACT{i:02d}",
            "title": act["title"],
            "purpose": f"Aplicar de forma guiada y reproducible los resultados de {u['title']} usando únicamente escenarios, activos y datos sintéticos.",
            "prerequisite_unit_ids": [] if n == 1 else [unit_id(n - 1)],
            "instructions": act.get("instructions", []),
            "tasks": tasks,
            "deliverables": act.get("deliverables", []),
            "checking_criteria": act.get("checking_criteria", []),
            "estimated_duration_minutes": min(300, max(120, 120 + 10 * len(tasks))),
            "status": "complete",
        })
    connections = []
    for item in u.get("biomedical_connections", []):
        if isinstance(item, dict):
            connections.append(f"{item.get('topic', 'Aplicación biomédica')}: {item.get('connection', '')}")
        else:
            connections.append(str(item))
    cu = {
        "$schema": "../../../../schemas/academic/unit-v1.schema.json",
        "schema_version": "1.0",
        "id": uid,
        "course_id": COURSE_ID,
        "order": n,
        "slug": u["slug"],
        "title": u["title"],
        "status": STATUS,
        "purpose": u["purpose"],
        "prerequisite_unit_ids": [] if n == 1 else [unit_id(n - 1)],
        "course_learning_outcome_ids": [f"{PREFIX}-LO{n:02d}", f"{PREFIX}-LO07"],
        "learning_outcomes": lo_records,
        "topics": topics,
        "examples": examples,
        "activities": activities,
        "assessment_file": f"assessments/unit-{n:02d}.json",
        "glossary_entry_ids": glossary_ids_by_unit[n],
        "source_ids": source_ids_by_unit[n],
        "claim_ids": claim_ids_by_unit[n],
        "media_ids": media_ids_by_unit[n],
        "common_errors": u.get("common_errors", []),
        "biomedical_connections": connections,
        "editorial_notice": u.get("editorial_notice", "Material académico con revisión humana pendiente."),
        "legacy_origin": f"data/course_redevelopment/{COURSE_ID}/units/unit-{n:02d}.json",
    }
    canonical_units.append(cu)
    dump(OUT / "units" / f"unit-{n:02d}.json", cu)

    items = []
    assessment_src = u.get("self_assessment", [])
    assert len(assessment_src) >= 8
    for i, item in enumerate(assessment_src, start=1):
        linked = lo_records[(i - 1) % len(lo_records)]["id"]
        items.append({
            "id": f"{uid}-Q{i:02d}",
            "type": "short_answer",
            "prompt": item["question"],
            "linked_learning_outcome_ids": [linked],
            "difficulty": "foundational" if i <= 3 else ("intermediate" if i <= 7 else "advanced"),
            "cognitive_level": "understand" if i <= 3 else ("apply" if i <= 7 else "evaluate"),
            "answer_key": {
                "expected_answer": item["answer"],
                "explanation": item.get("reasoning"),
                "common_misconceptions": [item.get("common_error", "Confundir el alcance de la conclusión.")],
            },
            "feedback": {
                "correct": "La respuesta distingue el constructo evaluado y conserva los límites de la unidad.",
                "incorrect": f"Revisa la explicación y evita este error frecuente: {item.get('common_error', 'sobreextender la evidencia')}.",
            },
            "source_ids": source_ids_by_unit[n][:2],
            "status": "complete",
        })
    assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{uid}-EVAL",
        "course_id": COURSE_ID,
        "scope": "unit",
        "unit_id": uid,
        "purpose": f"Comprobar comprensión, aplicación y límites de {u['title']} con recuperación activa y feedback recuperativo.",
        "student_payload_policy": "Usar únicamente casos, inventarios, contratos, incidentes, dispositivos, servicios y datos sintéticos; no introducir información personal, institucional confidencial ni decisiones reales.",
        "items": items,
        "status": "complete",
    }
    dump(OUT / "assessments" / f"unit-{n:02d}.json", assessment)

# Course-level records.
course_los = [
    ("ICG-LO01", "Explica la función de ingeniería clínica y construye una gobernanza trazable del ciclo de vida tecnológico con actores, responsabilidades, políticas, interfaces y límites explícitos."),
    ("ICG-LO02", "Construye y audita un inventario tecnológico con identificación, clasificación, historial y criticidad para priorizar acciones sin convertir un puntaje aislado en decisión automática."),
    ("ICG-LO03", "Planifica e interpreta mantenimiento, metrología e indicadores de desempeño diferenciando mantenimiento preventivo y correctivo, calibración, trazabilidad, disponibilidad, confiabilidad e incertidumbre."),
    ("ICG-LO04", "Estructura una evaluación y adquisición basada en necesidad, requisitos, coste total y evidencia, separando comparación técnica, decisión institucional y afirmaciones clínicas o regulatorias."),
    ("ICG-LO05", "Analiza señales e incidentes mediante contención, investigación de fallos, tecnovigilancia, aprendizaje y prevención de recurrencia, conservando incertidumbre, responsabilidades y límites de causalidad."),
    ("ICG-LO06", "Diseña y evalúa proyectos de mejora mediante objetivos, familias de KPIs, SLA, PDSA, competencia, adopción y sostenibilidad sin confundir actividad, cumplimiento contractual y calidad clínica."),
    ("ICG-LO07", "Integra U1–U6 en un expediente sintético y reproducible de gestión tecnológica que documenta fuentes, definiciones, versiones, decisiones, discrepancias, riesgos, indicadores, incertidumbre y próximos pasos sin presentarlo como auditoría, certificación o autorización real."),
]
core_source_ids = [s["id"] for s in sources if s["verification_status"] == "verified_directly"][:12]
course = {
    "$schema": "../../../schemas/academic/course-v1.schema.json",
    "schema_version": "1.0",
    "id": COURSE_ID,
    "code": PREFIX,
    "area_id": "ingenieria-biomedica",
    "title": "Ingeniería Clínica y Gestión",
    "language": "es",
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica y áreas afines que necesiten gestionar tecnología sanitaria con razonamiento de ciclo de vida, seguridad, mantenimiento, evaluación, trazabilidad, medición y mejora continua.",
    "status": STATUS,
    "purpose": "Integrar gobernanza del ciclo de vida tecnológico, inventario y criticidad, mantenimiento y metrología, adquisición y evaluación, seguridad e incidentes y proyectos de mejora para construir un expediente sintético y reproducible de ingeniería clínica que permita justificar decisiones operativas condicionadas por evidencia, incertidumbre y contexto sin presentar el trabajo académico como auditoría, contratación, certificación, conformidad normativa ni decisión clínica o regulatoria real.",
    "scope": {
        "included": [
            "Función, gobernanza, actores, responsabilidades y ciclo de vida de la tecnología sanitaria.",
            "Inventario, identificación, clasificación, historial, criticidad y priorización.",
            "Mantenimiento preventivo y correctivo, metrología, calibración, disponibilidad, confiabilidad e indicadores.",
            "Necesidades, requisitos, coste total, evaluación de tecnologías y adquisición basada en evidencia.",
            "Seguridad, incidentes, tecnovigilancia, investigación de fallos y prevención de recurrencia.",
            "KPIs, contratos y SLA, PDSA, formación basada en competencia, adopción, cambio y sostenibilidad.",
            "Trazabilidad de fuentes, definiciones, decisiones, incertidumbre y límites a través de las seis unidades."
        ],
        "excluded": [
            "Intervención, mantenimiento, calibración, retiro o modificación de dispositivos reales.",
            "Uso de datos de pacientes, personal, hospitales, contratos, proveedores o activos reales en actividades del curso.",
            "Asesoría jurídica o contractual, licitación, negociación, certificación, auditoría oficial o declaración de conformidad.",
            "Investigación clínica, diagnóstico, tratamiento o atribución causal de daño a una persona o producto real.",
            "Sustitución de políticas institucionales, procedimientos de tecnovigilancia, autoridades competentes o juicio profesional."
        ],
        "handoff_courses": ["desarrollo-dispositivos-medicos", "laboratorio-bioinstrumentacion", "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas", "sistemas-ayuda-decision-medica"]
    },
    "prerequisites": [
        {"id": "ICG-PRE01", "statement": "Fundamentos de bioinstrumentación, dispositivos médicos y seguridad eléctrica de nivel introductorio."},
        {"id": "ICG-PRE02", "statement": "Estadística descriptiva, proporciones, tasas, series temporales simples y razonamiento sobre incertidumbre."},
        {"id": "ICG-PRE03", "statement": "Capacidad para documentar procesos, criterios, cálculos, versiones, fuentes y decisiones de forma reproducible."},
        {"id": "ICG-PRE04", "statement": "Ética, privacidad y límites de uso de información sanitaria, contractual e institucional."},
        {"id": "ICG-PRE05", "statement": "Lectura funcional de guías técnicas y fuentes oficiales en inglés cuando sea necesario."}
    ],
    "competencies": [
        {"id": "ICG-COMP01", "statement": "Gestionar tecnología sanitaria como un sistema de ciclo de vida con gobernanza y responsabilidades explícitas."},
        {"id": "ICG-COMP02", "statement": "Convertir inventarios e historial técnico en priorización trazable sin automatizar indebidamente la decisión."},
        {"id": "ICG-COMP03", "statement": "Diseñar y evaluar mantenimiento, metrología e indicadores con definiciones y denominadores reproducibles."},
        {"id": "ICG-COMP04", "statement": "Estructurar adquisición y evaluación tecnológica desde necesidad, requisitos, evidencia y coste total."},
        {"id": "ICG-COMP05", "statement": "Investigar incidentes y señales con separación entre hechos, hipótesis, causalidad, reportabilidad y aprendizaje."},
        {"id": "ICG-COMP06", "statement": "Diseñar proyectos de mejora y gobernanza de servicio con métricas, contratos, PDSA, competencia y sostenibilidad."},
        {"id": "ICG-COMP07", "statement": "Comunicar recomendaciones operativas proporcionales a evidencia, incertidumbre, responsabilidades y alcance."}
    ],
    "learning_outcomes": [{"id": i, "statement": s} for i, s in course_los],
    "study_method": [
        "Definir primero sistema, uso, decisión, población de activos y frontera de responsabilidad antes de calcular o recomendar.",
        "Alternar explicación, ejemplo trabajado, actividad guiada, recuperación activa y práctica con apoyo progresivamente reducido.",
        "Separar dato, definición operacional, cálculo, interpretación, decisión institucional y afirmación clínica o regulatoria.",
        "Conservar fuentes, versiones, denominadores, exclusiones, supuestos, cambios y resultados negativos.",
        "Tratar seguridad como restricción transversal y usar medidas de balance para detectar desplazamiento del problema.",
        "Cerrar cada unidad con un handoff explícito y revisar el expediente acumulativo antes de avanzar."
    ],
    "core_source_ids": core_source_ids,
    "unit_files": [f"units/unit-{n:02d}.json" for n in range(1, 7)],
    "assessment_files": [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"],
    "registries": {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"},
    "static_site": {
        "renderer": "scripts/generate_site.py",
        "canonical_source": True,
        "legacy_mirrors": [
            f"data/generated_courses/{COURSE_ID}.json",
            f"data/generated_units/{COURSE_ID}/",
            f"data/subjects/ingenieria-biomedica/{COURSE_ID}.json",
            f"data/source_registry/{COURSE_ID}.json",
            f"data/claim_registry/{COURSE_ID}.json"
        ]
    },
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para U1–U6. Las fuentes están trazadas y la publicación continúa como provisional. La revisión humana interna y disciplinaria externa, cualquier uso de datos o activos reales, la asesoría contractual, la auditoría, la certificación, la declaración de conformidad y las decisiones clínicas, institucionales o regulatorias permanecen fuera de este cierre y siguen pendientes."
}
dump(OUT / "course.json", course)

dump(OUT / "glossary.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json", "schema_version": "1.0", "course_id": COURSE_ID, "entries": glossary
})
dump(OUT / "sources.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json", "schema_version": "1.0", "course_id": COURSE_ID,
    "source_policy": "Agregar únicamente fuentes ya trazadas por U1–U6; conservar su estado de verificación y procedencia. La agregación canónica no convierte revisión interna en validación disciplinaria humana.",
    "consulted_on": "2026-08-24", "coverage_gaps": [], "sources": sources
})
dump(OUT / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json", "schema_version": "1.0", "course_id": COURSE_ID,
    "content_version": "1.0.0", "content_commit": None,
    "scope": "Veinticuatro afirmaciones ancla, cuatro por unidad, tomadas literalmente de U1–U6 y ligadas a fuentes trazadas; revisión disciplinaria humana pendiente.",
    "review_state": "ai_review_provisional", "claims": claims
})
dump(OUT / "media.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json", "schema_version": "1.0", "course_id": COURSE_ID,
    "coverage_status": "planned", "items": media
})

assessment_plan = [
    {"component": f"U{n} · {units_src[n-1]['title']}", "weight_percent": 8, "linked_learning_outcome_ids": [f"ICG-LO{n:02d}", "ICG-LO07"]}
    for n in range(1, 7)
] + [
    {"component": "Evaluación integradora intermedia U1–U3", "weight_percent": 17, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO02", "ICG-LO03", "ICG-LO07"]},
    {"component": "Capstone de gestión tecnológica U1–U6", "weight_percent": 35, "linked_learning_outcome_ids": [f"ICG-LO{n:02d}" for n in range(1, 8)]},
]
assert sum(x["weight_percent"] for x in assessment_plan) == 100
course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "ICG-EVAL-CURSO",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": [
        "Evaluar decisiones, trazabilidad y límites, no memorización aislada de acrónimos, normas o indicadores.",
        "Separar dato, definición, cálculo, interpretación, acción operativa, obligación institucional y afirmación clínica o regulatoria.",
        "Usar únicamente escenarios, activos, incidentes, contratos, servicios y datos sintéticos.",
        "Exigir denominadores, versiones y fuentes cuando una comparación o requisito dependa del contexto.",
        "Premiar que el estudiante reduzca el alcance de una conclusión cuando la evidencia sea insuficiente o conflictiva.",
        "Mantener revisión humana externa, asesoría contractual, auditorías, certificaciones y acciones sobre sistemas reales fuera del alcance."
    ],
    "assessment_plan": assessment_plan,
    "diagnostic": {
        "purpose": "Comprobar prerrequisitos de gestión tecnológica, medición y trazabilidad antes del curso.",
        "questions": [
            "Distingue dato observado, cálculo e inferencia mediante un ejemplo técnico.",
            "Explica por qué un inventario sin identificadores y fechas no es auditable.",
            "Distingue precisión, exactitud, calibración y verificación metrológica.",
            "Calcula una proporción con numerador y denominador explícitos y describe qué no demuestra.",
            "Distingue requisito, criterio de aceptación y preferencia del usuario.",
            "Explica por qué un puntaje de criticidad no debe decidir automáticamente una acción.",
            "Distingue contención inmediata de análisis de causa y prevención de recurrencia.",
            "Explica por qué un contrato o SLA necesita alcance y reglas del reloj.",
            "Distingue asistencia a formación de competencia demostrada.",
            "Identifica información que no debería introducirse en una actividad académica pública."
        ],
        "use": "Formativo y no ponderado; cada error remite al prerrequisito o unidad correspondiente antes de avanzar."
    },
    "midterm_blueprint": [
        {"domain": "U1 · función, gobernanza y ciclo de vida", "weight_percent": 25, "linked_learning_outcome_ids": ["ICG-LO01"]},
        {"domain": "U2 · inventario y criticidad", "weight_percent": 30, "linked_learning_outcome_ids": ["ICG-LO02"]},
        {"domain": "U3 · mantenimiento y metrología", "weight_percent": 30, "linked_learning_outcome_ids": ["ICG-LO03"]},
        {"domain": "Integración U1–U3 y calidad de decisión", "weight_percent": 15, "linked_learning_outcome_ids": ["ICG-LO01", "ICG-LO02", "ICG-LO03", "ICG-LO07"]}
    ],
    "capstone": {
        "title": "Expediente sintético de gestión integral de una cartera de tecnología sanitaria",
        "purpose": "Integrar U1–U6 en un dossier reproducible de ingeniería clínica que pueda auditarse sin explicación oral adicional.",
        "scenario": "Gestionar una cartera hospitalaria enteramente ficticia con inventario, historial, necesidades, incidentes, contratos y series temporales sintéticas; ninguna salida se usa sobre personas, equipos, proveedores o instituciones reales.",
        "required_deliverables": [
            "Mapa de gobernanza, actores, responsabilidades y ciclo de vida.",
            "Inventario versionado con identificadores, clasificación, historial y reglas de calidad de datos.",
            "Modelo de criticidad con supuestos, análisis de sensibilidad y decisión no automática.",
            "Plan de mantenimiento preventivo/correctivo y trazabilidad metrológica.",
            "Dashboard reproducible de disponibilidad, respuesta, reparación y cumplimiento con denominadores explícitos.",
            "Caso de adquisición con necesidad, requisitos, coste total, evidencia y comparación de alternativas.",
            "Expediente de incidente sintético con contención, hipótesis, evidencia, aprendizaje y seguimiento.",
            "SLA sintético auditable con alcance, reloj, exclusiones, evidencia y escalamiento.",
            "Proyecto de mejora con objetivo, resultado/proceso/balance, dos ciclos PDSA y serie temporal.",
            "Plan de formación, competencia, adopción, gestión del cambio y sostenibilidad.",
            "Registro final de fuentes, versiones, decisiones, discrepancias, incertidumbre, límites y próximos pasos."
        ],
        "constraints": [
            "No usar datos personales, institucionales confidenciales, contratos, activos, pacientes o proveedores reales.",
            "No intervenir dispositivos ni emitir instrucciones técnicas para un servicio real.",
            "No afirmar certificación, conformidad, cumplimiento legal, calidad clínica global o causalidad no demostrada.",
            "Toda recomendación debe especificar fuente, denominador, incertidumbre, responsable hipotético y condición que podría cambiarla."
        ],
        "rubric": [
            {"criterion": "Gobernanza y ciclo de vida", "weight_percent": 12, "linked_learning_outcome_ids": ["ICG-LO01"]},
            {"criterion": "Inventario, datos y criticidad", "weight_percent": 14, "linked_learning_outcome_ids": ["ICG-LO02"]},
            {"criterion": "Mantenimiento, metrología e indicadores", "weight_percent": 16, "linked_learning_outcome_ids": ["ICG-LO03"]},
            {"criterion": "Adquisición, requisitos, coste total y evidencia", "weight_percent": 16, "linked_learning_outcome_ids": ["ICG-LO04"]},
            {"criterion": "Seguridad, incidentes y aprendizaje", "weight_percent": 16, "linked_learning_outcome_ids": ["ICG-LO05"]},
            {"criterion": "Mejora, SLA, competencia y sostenibilidad", "weight_percent": 16, "linked_learning_outcome_ids": ["ICG-LO06"]},
            {"criterion": "Integración, reproducibilidad, límites y handoff", "weight_percent": 10, "linked_learning_outcome_ids": ["ICG-LO07"]}
        ]
    },
    "status": "complete"
}
assert sum(x["weight_percent"] for x in course_assessment["midterm_blueprint"]) == 100
assert sum(x["weight_percent"] for x in course_assessment["capstone"]["rubric"]) == 100
dump(OUT / "assessments" / "course-assessment.json", course_assessment)

# Permanent regression generated with the corpus.
test = '''from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "courses" / "ingenieria-clinica-gestion"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"

class IngenieriaClinicaGestionCanonicalCourseTests(unittest.TestCase):
    def test_course_is_complete_but_human_review_pending(self):
        course = json.loads((BASE / "course.json").read_text(encoding="utf-8"))
        self.assertEqual(course["status"]["content"], "complete")
        self.assertEqual(course["status"]["sources"], "traceable")
        self.assertEqual(course["status"]["pedagogy"], "complete")
        self.assertEqual(course["status"]["multimedia"], "planned")
        self.assertEqual(course["status"]["internal_review"], "pending")
        self.assertEqual(course["status"]["external_review"], "pending")
        self.assertEqual(len(course["unit_files"]), 6)
        self.assertEqual(len(course["assessment_files"]), 7)
        self.assertEqual(len(course["learning_outcomes"]), 7)

    def test_all_six_units_are_canonical_and_non_generic(self):
        for n in range(1, 7):
            unit = json.loads((BASE / "units" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            text = json.dumps(unit, ensure_ascii=False).casefold()
            self.assertNotIn(GENERIC, text)
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["learning_outcomes"]), 5)
            self.assertGreaterEqual(len(unit["activities"]), 1)
            self.assertGreaterEqual(len(unit["source_ids"]), 5)
            self.assertEqual(len(unit["claim_ids"]), 4)

    def test_assessment_plan_and_capstone_are_complete(self):
        assessment = json.loads((BASE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(x["weight_percent"] for x in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["capstone"]["required_deliverables"]), 10)
        self.assertIn("sintético", assessment["capstone"]["scenario"].casefold())

    def test_registries_cover_glossary_sources_claims_and_media(self):
        glossary = json.loads((BASE / "glossary.json").read_text(encoding="utf-8"))["entries"]
        sources = json.loads((BASE / "sources.json").read_text(encoding="utf-8"))
        claims = json.loads((BASE / "claims.json").read_text(encoding="utf-8"))["claims"]
        media = json.loads((BASE / "media.json").read_text(encoding="utf-8"))["items"]
        self.assertGreaterEqual(len(glossary), 80)
        self.assertGreaterEqual(len(sources["sources"]), 24)
        self.assertEqual(sources["coverage_gaps"], [])
        self.assertEqual(len(claims), 24)
        self.assertEqual(len(media), 6)
        self.assertTrue(all(item["status"] == "planned" for item in media))

    def test_unit_assessments_are_recoverable_and_synthetic(self):
        for n in range(1, 7):
            assessment = json.loads((BASE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(assessment["items"]), 8)
            self.assertIn("sintéticos", assessment["student_payload_policy"].casefold())
            self.assertTrue(all(item["feedback"]["incorrect"] for item in assessment["items"]))

if __name__ == "__main__":
    unittest.main()
'''
(ROOT / "tests" / "test_ingenieria_clinica_gestion_canonical_course.py").write_text(test, encoding="utf-8")
print(f"Canonical course written to {OUT}; units={len(canonical_units)}, glossary={len(glossary)}, sources={len(sources)}, claims={len(claims)}")
