#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "ingenieria-clinica-gestion"
CODE = "ICG"
AREA_ID = "ingenieria-biomedica"
TITLE = "Ingeniería Clínica y Gestión"
REDEV_ROOT = ROOT / "data" / "course_redevelopment" / COURSE_ID
REDEV_UNITS = REDEV_ROOT / "units"
COURSE = ROOT / "data" / "courses" / COURSE_ID
GENERIC = "concepto de la unidad que debe definirse"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_text = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.casefold()).strip("-")
    return slug or "registro"


def unique(values):
    out = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out


def as_text(value, fallback="") -> str:
    if isinstance(value, str):
        return value.strip()
    if value is None:
        return fallback
    if isinstance(value, list):
        return "; ".join(as_text(item) for item in value if as_text(item))
    if isinstance(value, dict):
        for key in ("text", "statement", "description", "answer", "result", "interpretation", "reasoning"):
            if value.get(key):
                return as_text(value[key], fallback)
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def short_title(text: str, fallback: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return fallback
    sentence = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0]
    if len(sentence) <= 145:
        return sentence
    clipped = sentence[:142].rsplit(" ", 1)[0].rstrip(" ,;:")
    return clipped + "…"


def stable_source_key(source: dict) -> str:
    url = str(source.get("url") or "").strip()
    doi = str(source.get("doi") or "").strip().casefold()
    title = str(source.get("title") or "").strip().casefold()
    return url or doi or title


def source_id_for(source: dict, used: dict[str, str]) -> str:
    key = stable_source_key(source)
    base = slugify(str(source.get("title") or source.get("organization") or "fuente"))[:92]
    candidate = base
    if candidate in used and used[candidate] != key:
        suffix = hashlib.sha1(key.encode("utf-8")).hexdigest()[:8]
        candidate = f"{base[:82]}-{suffix}"
    used[candidate] = key
    return candidate


def example_record(example: dict, unit_id: str, index: int) -> dict:
    title = as_text(example.get("title"), f"Ejemplo trabajado {index}")
    scenario = as_text(example.get("scenario") or example.get("problem") or example.get("context"), title)
    reasoning = (
        example.get("reasoning_steps")
        or example.get("steps")
        or example.get("solution_steps")
        or example.get("reasoning")
        or example.get("solution")
        or []
    )
    reasoning_steps = [as_text(item) for item in as_list(reasoning) if as_text(item)]
    if not reasoning_steps:
        reasoning_steps = ["Identificar entradas, regla o método aplicable, salida esperada y límites de interpretación antes de concluir."]
    interpretation = as_text(
        example.get("interpretation") or example.get("result") or example.get("answer") or example.get("conclusion"),
        "Interpretar el resultado solo dentro de los supuestos, definiciones y alcance explícitos del ejemplo.",
    )
    limitations_raw = example.get("limitations") or example.get("limitation") or []
    limitations = [as_text(item) for item in as_list(limitations_raw) if as_text(item)]
    if not limitations:
        limitations = ["Caso educativo sintético: no autoriza una decisión operativa, contractual, regulatoria o clínica real."]
    return {
        "id": f"{unit_id}-EJ{index:02d}",
        "title": title,
        "scenario": scenario,
        "reasoning_steps": reasoning_steps,
        "interpretation": interpretation,
        "limitations": limitations,
    }


def flatten_connection(value) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        title = as_text(value.get("title") or value.get("area") or value.get("name"))
        desc = as_text(value.get("description") or value.get("connection") or value.get("text"))
        if title and desc:
            return f"{title}: {desc}"
        return title or desc or json.dumps(value, ensure_ascii=False)
    return as_text(value)


redevelopment_course = load(REDEV_ROOT / "course.json")
redevelopment_units = {n: load(REDEV_UNITS / f"unit-{n:02d}.json") for n in range(1, 7)}
for number, unit in redevelopment_units.items():
    serialized = json.dumps(unit, ensure_ascii=False).casefold()
    if GENERIC in serialized:
        raise RuntimeError(f"U{number}: todavía contiene marcador genérico")
    if unit.get("status") not in {"review", "complete"}:
        raise RuntimeError(f"U{number}: estado fuente inesperado {unit.get('status')!r}")
    if len(unit.get("theory_sections", [])) < 4:
        raise RuntimeError(f"U{number}: teoría insuficiente para cierre canónico")
    if len(unit.get("self_assessment", [])) < 10:
        raise RuntimeError(f"U{number}: autoevaluación insuficiente")
    if len(unit.get("sources", [])) < 5:
        raise RuntimeError(f"U{number}: bibliografía insuficiente")
    bad = [s.get("title") for s in unit.get("sources", []) if s.get("verification_status") != "verified_directly"]
    if bad:
        raise RuntimeError(f"U{number}: fuentes no verificadas directamente: {bad}")

COURSE.mkdir(parents=True, exist_ok=True)
(COURSE / "units").mkdir(parents=True, exist_ok=True)
(COURSE / "assessments").mkdir(parents=True, exist_ok=True)

# --- Sources: deduplicate without discarding provenance or unit use. ---
source_id_registry: dict[str, str] = {}
source_by_key: dict[str, dict] = {}
unit_source_ids: dict[int, list[str]] = {n: [] for n in range(1, 7)}
for number, source_unit in redevelopment_units.items():
    unit_id = f"{CODE}-U{number:02d}"
    for source in source_unit.get("sources", []):
        key = stable_source_key(source)
        if not key:
            raise RuntimeError(f"{unit_id}: fuente sin URL, DOI ni título")
        if key not in source_by_key:
            record = dict(source)
            record_id = source_id_for(source, source_id_registry)
            record["id"] = record_id
            record["verification_status"] = "verified_directly"
            record["used_by_unit_ids"] = [unit_id]
            record["why_relevant"] = as_text(
                record.get("why_relevant") or record.get("supports") or record.get("description") or record.get("locator"),
                f"Fuente directamente verificada y utilizada para sustentar contenido de {unit_id}.",
            )
            source_by_key[key] = record
        else:
            record = source_by_key[key]
            record["used_by_unit_ids"] = unique([*record.get("used_by_unit_ids", []), unit_id])
        unit_source_ids[number].append(record["id"])

source_records = list(source_by_key.values())
write(COURSE / "sources.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "source_policy": "Bootstrap desde las fuentes directamente verificadas de las seis unidades curadas; la etapa final restringe el registro a las fuentes efectivamente usadas por el corpus canónico.",
    "consulted_on": "2026-08-25",
    "coverage_gaps": [],
    "sources": source_records,
})

# --- Glossary: preserve definitions and merge repeated terms across units. ---
glossary_by_term: dict[str, dict] = {}
unit_glossary_terms: dict[int, list[str]] = {n: [] for n in range(1, 7)}
for number, source_unit in redevelopment_units.items():
    unit_id = f"{CODE}-U{number:02d}"
    for item in source_unit.get("glossary", []):
        term = as_text(item.get("term"))
        definition = as_text(item.get("definition"))
        if not term or not definition:
            raise RuntimeError(f"{unit_id}: entrada de glosario incompleta")
        key = term.casefold()
        unit_glossary_terms[number].append(key)
        if key not in glossary_by_term:
            glossary_by_term[key] = {
                "term": term,
                "definition": definition,
                "unit_ids": [unit_id],
                "source_ids": list(unit_source_ids[number][:2]),
                "verification_status": "traceable_to_verified_source",
            }
        else:
            entry = glossary_by_term[key]
            entry["unit_ids"] = unique([*entry["unit_ids"], unit_id])
            entry["source_ids"] = unique([*entry["source_ids"], *unit_source_ids[number][:2]])[:4]

glossary_entries = []
glossary_id_by_term: dict[str, str] = {}
for index, (key, entry) in enumerate(glossary_by_term.items(), start=1):
    entry_id = f"{CODE}-GLO-{index:03d}"
    glossary_id_by_term[key] = entry_id
    glossary_entries.append({"id": entry_id, **entry})

write(COURSE / "glossary.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "entries": glossary_entries,
    "status": "traceable",
})

# --- Planned media: explicit but intentionally not presented as produced. ---
media_items = []
for number, source_unit in redevelopment_units.items():
    media_items.append({
        "id": f"{CODE}-MED-{number:02d}",
        "unit_id": f"{CODE}-U{number:02d}",
        "title": f"Diagrama pedagógico de U{number} — {source_unit['title']}",
        "type": "diagram",
        "purpose": "Visualizar el flujo de decisión, entradas, controles, salidas y límites de la unidad sin usar datos de pacientes, instituciones o equipos reales.",
        "status": "planned",
    })
write(COURSE / "media.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "coverage_status": "planned",
    "items": media_items,
})

# Empty bootstrap claims are replaced by the finalizer with literal, source-linked anchors.
write(COURSE / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "content_version": "0.9.0",
    "content_commit": None,
    "scope": "Bootstrap temporal; el finalizador genera afirmaciones ancla literales con trazabilidad.",
    "review_state": "ai_review_provisional",
    "claims": [],
})

# --- Canonical units and unit assessments. ---
unit_files = []
assessment_files = []
for number, source_unit in redevelopment_units.items():
    unit_id = f"{CODE}-U{number:02d}"
    unit_files.append(f"units/unit-{number:02d}.json")
    assessment_files.append(f"assessments/unit-{number:02d}.json")

    outcomes = [
        {"id": f"{unit_id}-LO{index:02d}", "statement": as_text(statement)}
        for index, statement in enumerate(source_unit.get("learning_objectives", []), start=1)
        if as_text(statement)
    ]
    if len(outcomes) < 5:
        raise RuntimeError(f"{unit_id}: menos de cinco resultados de aprendizaje")

    topics = []
    for topic_index, section in enumerate(source_unit.get("theory_sections", []), start=1):
        topic_id = f"{unit_id}-T{topic_index:02d}"
        topic_blocks = []
        for equation_index, equation in enumerate(section.get("equations", []), start=1):
            variables = equation.get("variables") if isinstance(equation.get("variables"), dict) else {}
            topic_blocks.append({
                "id": f"{topic_id}-EQ{equation_index:02d}",
                "type": "equation",
                "latex": as_text(equation.get("latex")),
                "label": as_text(equation.get("meaning") or equation.get("label")),
                "variables": {str(k): as_text(v) for k, v in variables.items()},
            })
        paragraphs = [as_text(p) for p in section.get("paragraphs", []) if as_text(p)]
        if len(paragraphs) < 3:
            raise RuntimeError(f"{topic_id}: menos de tres párrafos")
        key_points = [as_text(p) for p in section.get("key_points", []) if as_text(p)]
        subtopics = []
        for sub_index, paragraph in enumerate(paragraphs, start=1):
            sub_id = f"{topic_id}-ST{sub_index:02d}"
            fallback = f"{section.get('heading', 'Tema')} · desarrollo {sub_index}"
            title_source = key_points[sub_index - 1] if sub_index - 1 < len(key_points) else paragraph
            subtopics.append({
                "id": sub_id,
                "title": short_title(title_source, fallback),
                "blocks": [{"id": f"{sub_id}-B01", "type": "paragraph", "text": paragraph}],
            })
        topics.append({
            "id": topic_id,
            "title": as_text(section.get("heading"), f"Tema {topic_index}"),
            "key_points": key_points or [short_title(paragraphs[0], "Idea central")],
            "blocks": topic_blocks,
            "subtopics": subtopics,
        })

    examples = [
        example_record(example, unit_id, index)
        for index, example in enumerate(source_unit.get("worked_examples", []), start=1)
    ]

    guided = (source_unit.get("guided_activities") or [{}])[0]
    guided_activity = {
        "id": f"{unit_id}-ACT01",
        "title": as_text(guided.get("title"), f"Actividad guiada de {source_unit['title']}"),
        "purpose": as_text(guided.get("purpose"), "Construir un expediente sintético reproducible aplicando los conceptos y controles de la unidad."),
        "prerequisite_unit_ids": [] if number == 1 else [f"{CODE}-U{number-1:02d}"],
        "instructions": [as_text(x) for x in guided.get("instructions", []) if as_text(x)] or ["Trabaja exclusivamente con el escenario y los datos sintéticos proporcionados."],
        "tasks": [as_text(x) for x in (guided.get("problems") or guided.get("tasks") or []) if as_text(x)] or ["Resuelve el caso y documenta entradas, método, resultados, controles y límites."],
        "deliverables": [as_text(x) for x in guided.get("deliverables", []) if as_text(x)] or ["Expediente reproducible de la unidad."],
        "checking_criteria": [as_text(x) for x in guided.get("checking_criteria", []) if as_text(x)] or ["La entrega distingue datos, cálculo, interpretación y límites de autoridad."],
        "estimated_duration_minutes": 240,
        "status": "complete",
    }

    unit_glossary_ids = unique(glossary_id_by_term[key] for key in unit_glossary_terms[number])
    unit_payload = {
        "$schema": "../../../../schemas/academic/unit-v1.schema.json",
        "schema_version": "1.0",
        "id": unit_id,
        "course_id": COURSE_ID,
        "order": number,
        "slug": source_unit["slug"],
        "title": source_unit["title"],
        "status": {
            "content": "complete",
            "sources": "traceable",
            "pedagogy": "complete",
            "multimedia": "planned",
            "internal_review": "pending",
            "external_review": "pending",
            "publication": "published_provisional",
        },
        "purpose": source_unit["purpose"],
        "prerequisite_unit_ids": [] if number == 1 else [f"{CODE}-U{number-1:02d}"],
        "course_learning_outcome_ids": [f"{CODE}-LO{number:02d}", f"{CODE}-LO07"],
        "learning_outcomes": outcomes,
        "topics": topics,
        "examples": examples,
        "activities": [guided_activity],
        "assessment_file": f"assessments/unit-{number:02d}.json",
        "glossary_entry_ids": unit_glossary_ids,
        "source_ids": unique(unit_source_ids[number]),
        "claim_ids": [],
        "media_ids": [f"{CODE}-MED-{number:02d}"],
        "common_errors": source_unit.get("common_errors", []),
        "biomedical_connections": [flatten_connection(x) for x in source_unit.get("biomedical_connections", []) if flatten_connection(x)],
        "editorial_notice": source_unit.get("editorial_notice", "Revisión humana externa pendiente; actividad educativa con datos sintéticos."),
        "legacy_origin": f"data/course_redevelopment/{COURSE_ID}/units/unit-{number:02d}.json",
    }
    write(COURSE / "units" / f"unit-{number:02d}.json", unit_payload)

    self_assessment = source_unit.get("self_assessment", [])
    if len(self_assessment) < 10:
        raise RuntimeError(f"{unit_id}: se requieren al menos diez ítems de autoevaluación")
    assessment_items = []
    for index, source_item in enumerate(self_assessment, start=1):
        prompt = as_text(source_item.get("question") or source_item.get("prompt"))
        expected = as_text(source_item.get("answer") or source_item.get("expected_answer"))
        explanation = as_text(source_item.get("reasoning") or source_item.get("explanation"), expected)
        misconception = as_text(source_item.get("common_error") or source_item.get("misconception"))
        if not prompt or not expected:
            raise RuntimeError(f"{unit_id}: ítem {index} de autoevaluación incompleto")
        assessment_items.append({
            "id": f"{unit_id}-Q{index:02d}",
            "type": "short_answer",
            "prompt": prompt,
            "linked_learning_outcome_ids": [outcomes[(index - 1) % len(outcomes)]["id"]],
            "difficulty": "unclassified",
            "cognitive_level": "unclassified",
            "answer_key": {
                "expected_answer": expected,
                "explanation": explanation,
                "common_misconceptions": [misconception] if misconception else [],
            },
            "feedback": {"correct": "Revisa la explicación razonada.", "incorrect": "Contrasta la respuesta con la teoría y vuelve a intentarlo."},
            "source_ids": [unit_source_ids[number][(index - 1) % len(unit_source_ids[number])]],
            "status": "review",
        })
    write(COURSE / "assessments" / f"unit-{number:02d}.json", {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{unit_id}-EVAL",
        "course_id": COURSE_ID,
        "scope": "unit",
        "unit_id": unit_id,
        "purpose": f"Evaluación recuperativa de U{number} — {source_unit['title']} con trazabilidad a resultados y fuentes.",
        "student_payload_policy": "La interfaz estudiantil debe ocultar answer_key y feedback hasta registrar el intento; las actividades emplean solo escenarios y datos sintéticos.",
        "items": assessment_items,
        "status": "review",
    })

assessment_files.append("assessments/course-assessment.json")
core_source_ids = unique(source_id for number in range(1, 7) for source_id in unit_source_ids[number][:2])[:12]
course_payload = {
    "$schema": "../../../schemas/academic/course-v1.schema.json",
    "schema_version": "1.0",
    "id": COURSE_ID,
    "code": CODE,
    "area_id": AREA_ID,
    "title": TITLE,
    "language": "es",
    "content_version": "0.9.0",
    "academic_level": redevelopment_course.get("level", "Pregrado universitario intermedio y avanzado"),
    "audience": "Estudiantes de ingeniería biomédica y áreas afines que necesiten integrar gestión tecnológica hospitalaria con trazabilidad, medición e incertidumbre.",
    "status": {
        "content": "complete",
        "sources": "traceable",
        "pedagogy": "complete",
        "multimedia": "planned",
        "internal_review": "pending",
        "external_review": "pending",
        "publication": "published_provisional",
    },
    "purpose": redevelopment_course.get("description", "Integrar la gestión de tecnología sanitaria de forma reproducible y auditable."),
    "scope": {
        "included": ["Gobernanza, inventario, mantenimiento, adquisición, seguridad y mejora de tecnología sanitaria mediante casos sintéticos."],
        "excluded": ["Intervención sobre equipos, pacientes, contratos o incidentes reales; auditoría, certificación o decisión clínica."],
        "handoff_courses": ["desarrollo-dispositivos-medicos", "bioinstrumentacion", "laboratorio-bioinstrumentacion"],
    },
    "prerequisites": [
        {"id": "ICG-PRE01", "statement": "Fundamentos de bioinstrumentación, medición y estadística descriptiva."},
        {"id": "ICG-PRE02", "statement": "Capacidad para documentar decisiones, supuestos, fuentes y resultados reproducibles."},
    ],
    "competencies": [
        {"id": f"ICG-COMP{i:02d}", "statement": as_text(text)}
        for i, text in enumerate(redevelopment_course.get("course_competencies", []), start=1)
        if as_text(text)
    ],
    "learning_outcomes": [
        {"id": f"ICG-LO{i:02d}", "statement": as_text(text)}
        for i, text in enumerate(redevelopment_course.get("learning_outcomes", [])[:7], start=1)
        if as_text(text)
    ],
    "study_method": [
        "Explicación → ejemplo trabajado → práctica guiada → apoyo reducido → reto autónomo → comprobación recuperativa.",
        "Toda decisión conserva datos de entrada, método, salida, incertidumbre, fuente y límites de autoridad.",
    ],
    "core_source_ids": core_source_ids,
    "unit_files": unit_files,
    "assessment_files": assessment_files,
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
    "editorial_notice": "Bootstrap canónico construido desde las seis unidades curadas; revisión humana interna y disciplinaria externa pendientes.",
}
if len(course_payload["competencies"]) < 1:
    raise RuntimeError("Sin competencias de curso")
if len(course_payload["learning_outcomes"]) < 7:
    raise RuntimeError("El curso fuente no aporta los siete resultados necesarios para el mapeo U1–U6 + integración")
write(COURSE / "course.json", course_payload)

# Placeholder course assessment replaced completely by finalizer in the same workflow.
write(COURSE / "assessments" / "course-assessment.json", {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "ICG-EVAL-CURSO",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": ["Bootstrap temporal"],
    "assessment_plan": [{"component": "Capstone temporal", "weight_percent": 100}],
    "diagnostic": {"questions": ["Bootstrap temporal"]},
    "midterm_blueprint": [],
    "capstone": {"rubric": [{"criterion": "Bootstrap temporal", "weight_percent": 100}]},
    "status": "review",
})

print(
    f"Bootstrap canónico ICG: unidades=6 fuentes={len(source_records)} glosario={len(glossary_entries)} "
    f"evaluaciones={sum(len(redevelopment_units[n].get('self_assessment', [])) for n in range(1, 7))}"
)
