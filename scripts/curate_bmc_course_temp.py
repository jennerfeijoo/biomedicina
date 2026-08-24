from __future__ import annotations

import json
import re
import shutil
import unicodedata
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBJECT = "biomecanica-medios-continuos"
CODE = "BMC"
SRC = ROOT / "data" / "course_redevelopment" / SUBJECT / "units"
DST = ROOT / "data" / "courses" / SUBJECT
STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def norm(text: str) -> str:
    return " ".join(str(text or "").casefold().split())


def identity(src: dict) -> str:
    if src.get("doi"):
        return "doi:" + norm(src["doi"]).removeprefix("https://doi.org/").removeprefix("doi:")
    if src.get("pmid"):
        return "pmid:" + str(src["pmid"]).strip()
    if src.get("isbn"):
        return "isbn:" + re.sub(r"[^0-9xX]", "", str(src["isbn"])).casefold()
    if src.get("url"):
        return "url:" + str(src["url"]).strip().casefold().rstrip("/")
    return "citation:" + norm(src.get("citation", ""))


def title_from_source(src: dict) -> str:
    citation = str(src.get("citation") or src.get("title") or "Fuente académica").strip()
    pieces = [p.strip() for p in citation.split(". ") if p.strip()]
    if len(pieces) >= 2:
        return pieces[1][:180]
    return citation[:180]


def source_type(src: dict) -> str:
    url = str(src.get("url") or "").casefold()
    citation = str(src.get("citation") or "").casefold()
    if "fda.gov" in url or "asme.org" in url or "iso.org" in url or "who.int" in url:
        return "estándar o guía oficial"
    if src.get("pmid") or "pubmed" in url:
        return "artículo indexado"
    if "review" in citation or "revisión" in citation:
        return "revisión"
    return "fuente académica"


units_raw = [json.loads((SRC / f"unit-{n:02d}.json").read_text(encoding="utf-8")) for n in range(1, 7)]
assert all(GENERIC not in json.dumps(u, ensure_ascii=False).casefold() for u in units_raw)

# Build one deduplicated source registry and a per-unit old-id -> canonical-id map.
source_records: OrderedDict[str, dict] = OrderedDict()
identity_to_id: dict[str, str] = {}
source_maps: dict[int, dict[str, str]] = {}
for n, unit in enumerate(units_raw, 1):
    unit_id = f"{CODE}-U{n:02d}"
    source_maps[n] = {}
    for src in unit.get("sources", []):
        ident = identity(src)
        if ident not in identity_to_id:
            cid = f"bmc-src-{len(identity_to_id)+1:03d}"
            identity_to_id[ident] = cid
            record = {
                "id": cid,
                "title": title_from_source(src),
                "citation": src.get("citation", title_from_source(src)),
                "url": src.get("url", ""),
                "type": source_type(src),
                "description": f"Fuente trazable utilizada en la curación disciplinar de {unit['title']}.",
                "verification_status": "verified_directly" if str(src.get("verification_status", "")).startswith("verified_directly") else str(src.get("verification_status") or "traceable"),
                "used_by_unit_ids": [unit_id],
            }
            for field in ("doi", "pmid", "isbn", "registry_id", "organization"):
                if src.get(field):
                    record[field] = src[field]
            source_records[cid] = record
        else:
            cid = identity_to_id[ident]
            if unit_id not in source_records[cid]["used_by_unit_ids"]:
                source_records[cid]["used_by_unit_ids"].append(unit_id)
        source_maps[n][str(src.get("id") or cid)] = cid


def mapped_section_sources(n: int, section: dict) -> list[str]:
    mapped = [source_maps[n][sid] for sid in section.get("source_ids", []) if sid in source_maps[n]]
    if mapped:
        return list(dict.fromkeys(mapped))
    return list(dict.fromkeys(source_maps[n].values()))[:1]


def best_source(n: int, unit: dict, text: str) -> str:
    words = {w for w in re.findall(r"[a-záéíóúüñ]{4,}", norm(text)) if w not in {"para", "como", "entre", "debe", "puede", "porque", "sobre", "cuál", "donde", "cuando"}}
    best: tuple[int, str] | None = None
    for section in unit.get("theory_sections", []):
        corpus = norm(" ".join(section.get("paragraphs", []) + section.get("key_points", [])))
        score = sum(1 for w in words if w in corpus)
        sources = mapped_section_sources(n, section)
        if sources and (best is None or score > best[0]):
            best = (score, sources[0])
    if best:
        return best[1]
    return next(iter(source_maps[n].values()))

# Glossary registry, preserving every curated definition with source traceability.
glossary_entries: list[dict] = []
glossary_ids_by_unit: dict[int, list[str]] = {}
for n, unit in enumerate(units_raw, 1):
    unit_id = f"{CODE}-U{n:02d}"
    ids: list[str] = []
    for idx, entry in enumerate(unit.get("glossary", []), 1):
        gid = f"{CODE}-GLO-{n:02d}-{idx:02d}"
        ids.append(gid)
        glossary_entries.append({
            "id": gid,
            "term": entry["term"],
            "definition": entry["definition"],
            "unit_ids": [unit_id],
            "source_ids": [best_source(n, unit, entry["term"] + " " + entry["definition"])],
            "verification_status": "traceable_to_curated_unit_sources",
        })
    glossary_ids_by_unit[n] = ids

# Four literal anchor claims per unit, one from each theory section.
claims: list[dict] = []
claim_ids_by_unit: dict[int, list[str]] = {}
for n, unit in enumerate(units_raw, 1):
    unit_id = f"{CODE}-U{n:02d}"
    ids: list[str] = []
    for idx, section in enumerate(unit.get("theory_sections", [])[:4], 1):
        text = section.get("key_points", [])[0] if section.get("key_points") else section.get("paragraphs", [""])[0]
        cid = f"{CODE}-U{n:02d}-CL{idx:02d}"
        ids.append(cid)
        sources = mapped_section_sources(n, section)
        claims.append({
            "id": cid,
            "unit_id": unit_id,
            "text": text,
            "source_id": sources[0] if sources else next(iter(source_maps[n].values())),
            "status": "curated_internal_review_pending",
        })
    assert len(ids) == 4, f"U{n} lacks four claim anchors"
    claim_ids_by_unit[n] = ids

media_items: list[dict] = []
media_ids_by_unit: dict[int, list[str]] = {}
media_purposes = {
    1: ("Mapa cinemático del continuo", "Esquema sintético de configuración de referencia, configuración actual, gradiente de deformación y medidas de deformación."),
    2: ("Tensor de tensiones y equilibrio", "Elemento diferencial sintético con tracciones, tensor de Cauchy, normales y condiciones de frontera."),
    3: ("Mapa de modelos constitutivos", "Comparación visual de elasticidad lineal, hiperelasticidad, anisotropía y grandes deformaciones para tejidos."),
    4: ("Respuesta dependiente del tiempo", "Curvas sintéticas de relajación, fluencia, viscoelasticidad y comportamiento bipásico con parámetros identificables."),
    5: ("Flujo biológico y escalas adimensionales", "Esquema sintético que relaciona Navier–Stokes, Reynolds, Womersley, WSS, reología y FSI."),
    6: ("Flujo V&V de elementos finitos", "Diagrama sintético desde formulación débil y malla hasta convergencia, verificación, validación, sensibilidad e incertidumbre."),
}

# Course descriptor is deliberately authored at course level; unit detail comes from curated sources below.
course_outcomes = [
    ("BMC-LO01", "Construye una descripción continua de sólidos y fluidos biológicos mediante configuración, movimiento, gradiente de deformación, medidas tensoriales y balances de conservación, declarando marcos y supuestos."),
    ("BMC-LO02", "Formula y resuelve equilibrio y balance de cantidad de movimiento con tensor de tensiones, tracciones, fuerzas de volumen y condiciones de frontera, verificando signos, unidades y consistencia física."),
    ("BMC-LO03", "Selecciona, parametriza e interpreta leyes constitutivas elásticas e hiperelásticas, isotrópicas o anisotrópicas, diferenciando ajuste, identificabilidad, extrapolación y validez para grandes deformaciones."),
    ("BMC-LO04", "Modela respuesta temporal de tejidos mediante viscoelasticidad, relajación, fluencia y formulaciones poro/bifásicas, relacionando escalas de tiempo, protocolo experimental e incertidumbre paramétrica."),
    ("BMC-LO05", "Formula e interpreta modelos de fluidos biológicos con conservación, Navier–Stokes, reología no newtoniana, números adimensionales, tensiones de pared e interacción fluido-estructura dentro del dominio evaluado."),
    ("BMC-LO06", "Construye y audita una simulación por elementos finitos distinguiendo discretización, verificación, convergencia, calibración, validación, sensibilidad, incertidumbre y credibilidad ligada al contexto de uso."),
    ("BMC-LO07", "Integra U1–U6 en un expediente de modelado reproducible que conecta pregunta, idealización, ecuaciones, parámetros, solución, controles, evidencia, incertidumbre y límites sin convertir credibilidad mecánica en conclusión clínica o regulatoria."),
]

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
    "audience": "Estudiantes de ingeniería biomédica y áreas afines con cálculo multivariable, álgebra lineal, mecánica, métodos numéricos y fundamentos de fisiología o biomateriales que necesiten formular y auditar modelos continuos de tejidos y fluidos biológicos.",
    "status": STATUS,
    "purpose": "Integrar cinemática de deformación, esfuerzo y equilibrio, elasticidad, viscoelasticidad y poroelasticidad, fluidos biológicos y elementos finitos con verificación, validación e incertidumbre para construir modelos continuos reproducibles de sistemas biomédicos. El curso separa formulación física, aproximación numérica, evidencia experimental y contexto de uso, y evita presentar una simulación como diagnóstico, eficacia clínica o aprobación regulatoria no demostrados.",
    "scope": {
        "included": [
            "Configuraciones, movimiento, gradiente de deformación, tensores y conservación en medios continuos.",
            "Tensor de tensiones de Cauchy, tracciones, equilibrio, balance de cantidad de movimiento y condiciones de frontera.",
            "Elasticidad lineal, hiperelasticidad, anisotropía, grandes deformaciones e identificación constitutiva.",
            "Relajación, fluencia, modelos viscoelásticos y formulaciones poro/bifásicas para respuesta dependiente del tiempo.",
            "Conservación y Navier–Stokes, reología sanguínea, Reynolds, Womersley, esfuerzo cortante de pared e interacción fluido-estructura.",
            "Formulación débil, discretización por elementos finitos, calidad de malla, convergencia y verificación.",
            "Calibración frente a validación, sensibilidad, cuantificación de incertidumbre y credibilidad proporcional al contexto de uso.",
        ],
        "excluded": [
            "Diagnóstico, pronóstico o recomendación terapéutica individual a partir de una simulación mecánica.",
            "Declarar un modelo universalmente validado fuera de las cantidades de interés, condiciones y evidencia evaluadas.",
            "Usar convergencia de malla como sustituto de validación física o un buen ajuste como sustituto de predicción independiente.",
            "Presentar el cumplimiento de una actividad educativa como certificación de software, dispositivo o conformidad regulatoria.",
            "Trabajar con datos personales, pacientes o ensayos institucionales en las actividades autónomas; se emplean casos sintéticos o abiertos no personales.",
        ],
        "handoff_courses": ["biomecanica", "biomateriales-implantes", "modelado-simulacion-biomedicina", "simulacion-planificacion-quirurgica", "ingenieria-tejidos"],
    },
    "prerequisites": [
        {"id": "BMC-PRE01", "statement": "Cálculo diferencial e integral multivariable y ecuaciones diferenciales ordinarias introductorias."},
        {"id": "BMC-PRE02", "statement": "Álgebra lineal, vectores, matrices, productos tensoriales básicos y cambio de base."},
        {"id": "BMC-PRE03", "statement": "Mecánica universitaria: fuerza, momento, energía, equilibrio y leyes de conservación."},
        {"id": "BMC-PRE04", "statement": "Programación o cálculo científico básico para resolver ecuaciones, explorar parámetros y visualizar resultados."},
        {"id": "BMC-PRE05", "statement": "Fundamentos de fisiología, anatomía o biomateriales suficientes para interpretar tejidos y fluidos biológicos sin inferir clínica individual."},
    ],
    "competencies": [
        {"id": "BMC-COMP01", "statement": "Traducir un sistema biológico a un dominio continuo con variables, coordenadas, balances y fronteras explícitos."},
        {"id": "BMC-COMP02", "statement": "Seleccionar leyes constitutivas y escalas temporales de acuerdo con mecanismo, protocolo y cantidad de interés."},
        {"id": "BMC-COMP03", "statement": "Analizar sólidos y fluidos biológicos manteniendo coherencia dimensional, tensorial y energética."},
        {"id": "BMC-COMP04", "statement": "Diseñar discretizaciones y controles numéricos capaces de distinguir error de solución de error de modelo."},
        {"id": "BMC-COMP05", "statement": "Separar calibración, verificación, validación, sensibilidad e incertidumbre y documentar la evidencia de cada capa."},
        {"id": "BMC-COMP06", "statement": "Comunicar credibilidad y límites en función del contexto de uso sin extrapolar a decisiones clínicas o regulatorias no evaluadas."},
        {"id": "BMC-COMP07", "statement": "Entregar un expediente reproducible de modelado continuo que otra persona pueda reconstruir y auditar."},
    ],
    "learning_outcomes": [{"id": i, "statement": s} for i, s in course_outcomes],
    "study_method": [
        "Definir sistema, cantidad de interés, variables, dominio, fronteras y uso previsto antes de seleccionar ecuaciones o solver.",
        "Alternar explicación, ejemplo resuelto, actividad guiada y transferencia con apoyo progresivamente menor.",
        "Comprobar unidades, simetrías, balances, límites y casos analíticos antes de interpretar una simulación compleja.",
        "Separar parámetros calibrados de evidencia reservada para validación y bloquear el modelo antes de evaluar predicción.",
        "Conservar ecuaciones, geometría, materiales, malla, solver, tolerancias, versiones, datos, scripts y registro de cambios.",
        "Evaluar sensibilidad e incertidumbre sobre la cantidad de interés y declarar explícitamente las extrapolaciones.",
    ],
    "core_source_ids": list(source_records)[: min(18, len(source_records))],
    "unit_files": [f"units/unit-{n:02d}.json" for n in range(1, 7)],
    "assessment_files": [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"],
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
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, fuentes trazables y pedagogía interna para U1–U6. La publicación permanece provisional y la revisión humana interna y disciplinaria externa siguen pendientes. El curso no constituye validación clínica, certificación de un solver, aprobación regulatoria ni recomendación para un paciente o dispositivo real; la credibilidad computacional solo se interpreta dentro de la cantidad de interés, condiciones, evidencia y contexto de uso evaluados.",
}

# Unit records + assessments.
for n, unit in enumerate(units_raw, 1):
    unit_id = f"{CODE}-U{n:02d}"
    local_los = [{"id": f"{unit_id}-LO{i:02d}", "statement": statement} for i, statement in enumerate(unit.get("learning_objectives", []), 1)]
    topics: list[dict] = []
    for ti, section in enumerate(unit.get("theory_sections", []), 1):
        key_points = section.get("key_points", [])
        topic = {
            "id": f"{unit_id}-T{ti:02d}",
            "title": section["heading"],
            "blocks": [
                {"id": f"{unit_id}-T{ti:02d}-E{ei:02d}", "type": "equation", "latex": eq["latex"]}
                for ei, eq in enumerate(section.get("equations", []), 1)
            ],
            "key_points": key_points,
            "subtopics": [],
        }
        for si, paragraph in enumerate(section.get("paragraphs", []), 1):
            st_title = key_points[si-1].rstrip(".") if si <= len(key_points) else f"Concepto disciplinar {si}"
            topic["subtopics"].append({
                "id": f"{unit_id}-T{ti:02d}-ST{si:02d}",
                "title": st_title,
                "blocks": [{"id": f"{unit_id}-T{ti:02d}-ST{si:02d}-B01", "type": "paragraph", "text": paragraph}],
            })
        topics.append(topic)

    examples = []
    for ei, ex in enumerate(unit.get("worked_examples", []), 1):
        examples.append({
            "id": f"{unit_id}-EX{ei:02d}",
            "title": ex["title"],
            "scenario": ex["scenario"],
            "reasoning_steps": ex.get("reasoning_steps", []),
            "interpretation": ex.get("result", "El resultado debe interpretarse dentro del modelo y supuestos declarados."),
            "limitations": "Ejemplo sintético para aprendizaje: ilustra el método y la interpretación mecánica descrita, pero no demuestra por sí solo validez clínica, causalidad, seguridad o conformidad regulatoria.",
        })

    activities = []
    for ai, act in enumerate(unit.get("guided_activities", []), 1):
        activities.append({
            "id": f"{unit_id}-ACT{ai:02d}",
            "title": act["title"],
            "purpose": f"Aplicar de forma reproducible los métodos de {unit['title']} sobre un caso sintético, con controles, incertidumbre y límites explícitos.",
            "prerequisite_unit_ids": [] if n == 1 else [f"{CODE}-U{n-1:02d}"],
            "instructions": act.get("instructions", []),
            "tasks": act.get("problems", []),
            "deliverables": act.get("deliverables", []),
            "checking_criteria": act.get("checking_criteria", []),
            "estimated_duration_minutes": 270,
            "status": "complete",
        })
    assert activities, f"U{n} lacks guided activity"

    mapped_sources = list(dict.fromkeys(source_maps[n].values()))
    media_id = f"{unit_id}-MED01"
    media_ids_by_unit[n] = [media_id]
    purpose, alt = media_purposes[n]
    media_items.append({
        "id": media_id,
        "type": "figure",
        "status": "planned",
        "unit_id": unit_id,
        "linked_learning_outcome_ids": [item["id"] for item in local_los[:2]],
        "pedagogical_purpose": purpose,
        "alt_text_draft": alt,
        "license_requirements": "Usar material propio o con licencia compatible y registrar atribución y procedencia.",
        "source_ids": mapped_sources[:2],
    })

    canonical = {
        "$schema": "../../../../schemas/academic/unit-v1.schema.json",
        "schema_version": "1.0",
        "id": unit_id,
        "course_id": SUBJECT,
        "order": n,
        "slug": unit["slug"],
        "title": unit["title"],
        "status": STATUS,
        "purpose": unit["purpose"],
        "prerequisite_unit_ids": [] if n == 1 else [f"{CODE}-U{n-1:02d}"],
        "course_learning_outcome_ids": [f"BMC-LO{n:02d}", "BMC-LO07"],
        "learning_outcomes": local_los,
        "topics": topics,
        "examples": examples,
        "activities": activities,
        "assessment_file": f"assessments/unit-{n:02d}.json",
        "glossary_entry_ids": glossary_ids_by_unit[n],
        "source_ids": mapped_sources,
        "claim_ids": claim_ids_by_unit[n],
        "media_ids": [media_id],
        "common_errors": unit.get("common_errors", []),
        "biomedical_connections": [f"{x.get('context', 'Aplicación')}: {x.get('connection', '')}" if isinstance(x, dict) else str(x) for x in unit.get("biomedical_connections", [])],
        "editorial_notice": unit.get("editorial_notice", "Curación interna; revisión humana externa pendiente."),
        "legacy_origin": f"data/course_redevelopment/{SUBJECT}/units/unit-{n:02d}.json",
    }
    dump(DST / "units" / f"unit-{n:02d}.json", canonical)

    assessment_items = []
    for qi, item in enumerate(unit.get("self_assessment", []), 1):
        src_id = best_source(n, unit, item.get("question", "") + " " + item.get("reasoning", ""))
        lo_id = local_los[(qi - 1) % len(local_los)]["id"]
        assessment_items.append({
            "id": f"{unit_id}-Q{qi:02d}",
            "type": "short_answer",
            "prompt": item["question"],
            "linked_learning_outcome_ids": [lo_id],
            "difficulty": "foundational" if qi <= 3 else ("intermediate" if qi <= 7 else "advanced"),
            "cognitive_level": ["understand", "apply", "analyze", "evaluate"][(qi - 1) % 4],
            "answer_key": {
                "expected_answer": item["answer"],
                "explanation": item.get("reasoning", "Justificar desde el modelo, los datos y los límites de la unidad."),
                "common_misconceptions": [item.get("common_error", "Confundir la salida del modelo con una conclusión fuera de alcance.")],
            },
            "feedback": {
                "correct": "Correcto. Conserva ecuaciones, unidades, supuestos, controles y límite de inferencia en tu expediente acumulativo.",
                "incorrect": "Revisa el tema correspondiente, identifica dato de entrada, ecuación o modelo, control y conclusión permitida; después responde de nuevo sin consultar la solución.",
            },
            "source_ids": [src_id],
            "status": "complete",
        })
    assert len(assessment_items) >= 8, f"U{n} needs >=8 assessment items"
    dump(DST / "assessments" / f"unit-{n:02d}.json", {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{unit_id}-EVAL",
        "course_id": SUBJECT,
        "scope": "unit",
        "unit_id": unit_id,
        "purpose": f"Comprobar de forma formativa y recuperativa los resultados de aprendizaje de {unit['title']} con énfasis en formulación, controles, interpretación y límites.",
        "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial del estudiante.",
        "items": assessment_items,
        "status": "complete",
    })

# Registries.
dump(DST / "sources.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": SUBJECT,
    "source_policy": "Priorizar estándares, guías oficiales, artículos indexados, revisiones y literatura metodológica directamente pertinente. Las fuentes se deduplican por DOI, PMID, ISBN o URL y conservan la verificación heredada de U1–U6. La trazabilidad no equivale a revisión humana ni a validación clínica/regulatoria.",
    "consulted_on": "2026-08-24",
    "coverage_gaps": [],
    "sources": list(source_records.values()),
})
dump(DST / "glossary.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": SUBJECT,
    "entries": glossary_entries,
})
dump(DST / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": SUBJECT,
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Cuatro afirmaciones metodológicas literales por unidad, derivadas de key_points del corpus curado y vinculadas a una fuente trazable.",
    "review_state": "internal_curated_external_pending",
    "claims": claims,
})
dump(DST / "media.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": SUBJECT,
    "coverage_status": "planned",
    "items": media_items,
})
dump(DST / "course.json", course)

# Integrated course assessment.
course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "BMC-EVAL-CURSO",
    "course_id": SUBJECT,
    "scope": "course",
    "principles": [
        "La evaluación premia la cadena pregunta → modelo → ecuaciones → parámetros → solución → control → evidencia → interpretación, no una figura final aislada.",
        "Toda cantidad debe conservar unidades, convención tensorial, sistema de referencia y dominio de validez.",
        "Verificación, calibración, validación y cuantificación de incertidumbre se evalúan como actividades distintas.",
        "Los errores corregidos con explicación y registro antes-después forman parte de la evidencia de aprendizaje.",
        "Las actividades calificadas emplean datos, geometrías y experimentos sintéticos o recursos abiertos no personales.",
        "La revisión disciplinaria humana permanece pendiente aunque contenido, fuentes y pedagogía internos estén completos.",
    ],
    "assessment_plan": [
        {"component": "Comprobaciones recuperativas U1–U6", "weight_percent": 15, "description": "Controles breves con explicación, feedback y reintento documentado."},
        {"component": "Problemas de sólidos y leyes constitutivas", "weight_percent": 25, "description": "Balances, tensiones, elasticidad y respuesta temporal con verificación dimensional y casos límite."},
        {"component": "Caso de fluidos biológicos", "weight_percent": 15, "description": "Conservación, escalas adimensionales, reología y WSS/FSI con límites de interpretación."},
        {"component": "Expediente FEM, V&V y UQ", "weight_percent": 20, "description": "Malla, convergencia, verificación, calibración, validación, sensibilidad e incertidumbre."},
        {"component": "Proyecto integrador reproducible", "weight_percent": 25, "description": "Capstone que conecta las seis unidades y defiende una predicción delimitada con trazabilidad completa."},
    ],
    "diagnostic": {
        "title": "Diagnóstico de entrada a Biomecánica de Medios Continuos",
        "purpose": "Detectar prerrequisitos que deben recuperarse antes de iniciar U1; no aporta nota final.",
        "questions": [
            "Distingue escalar, vector, matriz y tensor de segundo orden y da un ejemplo mecánico de cada uno.",
            "Explica la diferencia entre configuración de referencia y configuración actual.",
            "Interpreta físicamente un gradiente espacial y sus unidades.",
            "Formula equilibrio de fuerzas para un volumen de control simple.",
            "Distingue esfuerzo normal, esfuerzo cortante y tracción sobre un plano.",
            "Explica qué significa una condición de frontera esencial y una natural en un problema mecánico.",
            "Distingue material isotrópico de anisotrópico.",
            "Explica por qué un buen ajuste de parámetros no demuestra capacidad predictiva.",
            "Distingue relajación de tensiones y fluencia.",
            "Escribe qué términos físicos aparecen en la ecuación de Navier–Stokes y qué balance representan.",
            "Explica qué significa refinar una malla y por qué más elementos no corrigen una física equivocada.",
            "Distingue verificación, validación, sensibilidad e incertidumbre en una simulación.",
        ],
        "interpretation": [
            "0–4 respuestas sólidas: completar nivelación de cálculo, álgebra lineal y mecánica antes de U1.",
            "5–8 respuestas sólidas: iniciar U1 con recuperación focalizada de tensores, balances y ecuaciones diferenciales.",
            "9–12 respuestas sólidas: comenzar el curso y documentar igualmente convenciones y supuestos.",
        ],
    },
    "midterm_blueprint": [
        {"domain": "U1 Descripción continua de tejidos", "weight_percent": 16},
        {"domain": "U2 Esfuerzo y equilibrio", "weight_percent": 16},
        {"domain": "U3 Elasticidad", "weight_percent": 17},
        {"domain": "U4 Viscoelasticidad y poroelasticidad", "weight_percent": 17},
        {"domain": "U5 Fluidos biológicos", "weight_percent": 17},
        {"domain": "U6 Elementos finitos y validación", "weight_percent": 17},
    ],
    "capstone": {
        "title": "Expediente reproducible de un modelo continuo biomecánico sintético",
        "scenario": "Un equipo académico debe explicar y predecir una cantidad de interés mecánica en un sistema biológico sintético. Debe elegir una idealización continua, justificar constitutiva y fronteras, resolverla analítica o numéricamente, verificar la solución y contrastar la predicción con evidencia sintética independiente sin realizar afirmaciones clínicas.",
        "phases": [
            "Predefinir pregunta, contexto de uso académico, cantidad de interés, dominio, variables y criterio de aceptación.",
            "Construir cinemática y balances y verificar unidades, simetrías y casos límite.",
            "Seleccionar y justificar constitutiva sólida o fluida y separar parámetros conocidos de calibrados.",
            "Resolver un caso base y un benchmark o solución simplificada antes del modelo complejo.",
            "Construir discretización FEM cuando corresponda y ejecutar estudio de convergencia sobre la cantidad de interés.",
            "Bloquear parámetros y comparar con evidencia sintética de validación no usada en calibración.",
            "Cuantificar sensibilidad e incertidumbre de entradas dominantes y evaluar si cambia la conclusión.",
            "Realizar revisión independiente, corregir el expediente y registrar cambios antes-después.",
        ],
        "required_deliverables": [
            "Pregunta, cantidad de interés, contexto de uso y matriz de trazabilidad U1–U6.",
            "Definición de dominio, coordenadas, configuración de referencia y condiciones de frontera.",
            "Balances y constitutiva con variables, unidades, parámetros, supuestos y rango de aplicabilidad.",
            "Caso analítico, benchmark o control de verificación equivalente.",
            "Archivos o tablas de malla, solver, tolerancias y estudio de convergencia cuando se use FEM.",
            "Registro separado de calibración y validación con criterio predefinido.",
            "Análisis de sensibilidad e incertidumbre de la cantidad de interés.",
            "Figuras y tablas con unidades, procedencia y metadatos suficientes para reproducir el resultado.",
            "README con versiones, dependencias, parámetros y procedimiento de reconstrucción.",
            "Informe académico y registro de revisión/correcciones con límites explícitos.",
        ],
        "integration_requirements": [
            "Vincular explícitamente evidencias con BMC-LO01 a BMC-LO07.",
            "Incluir al menos un control analítico o benchmark, un estudio de sensibilidad y una comprobación de conservación o equilibrio.",
            "Separar formulación física, error numérico, calibración, validación e inferencia fuera de alcance.",
            "Usar únicamente datos y geometrías sintéticas o recursos abiertos no personales y documentar procedencia/licencia.",
        ],
        "rubric": [
            {"criterion": "Formulación del continuo y balances", "weight_percent": 18, "excellent": "Dominio, variables, coordenadas, cinemática, balances y fronteras son coherentes y auditables."},
            {"criterion": "Constitutiva y parámetros", "weight_percent": 16, "excellent": "La constitutiva responde al mecanismo/rango, los parámetros tienen procedencia y la calibración está separada de validación."},
            {"criterion": "Solución numérica y verificación", "weight_percent": 18, "excellent": "Benchmark, conservación, malla, tolerancias y convergencia sostienen la cantidad de interés sin ocultar singularidades."},
            {"criterion": "Validación, sensibilidad e incertidumbre", "weight_percent": 18, "excellent": "La predicción bloqueada se contrasta con evidencia independiente y se cuantifican entradas dominantes e incertidumbre."},
            {"criterion": "Reproducibilidad y trazabilidad", "weight_percent": 18, "excellent": "Otra persona puede reconstruir ecuaciones, archivos, parámetros, solver, versiones, datos y decisiones."},
            {"criterion": "Interpretación, límites y revisión", "weight_percent": 12, "excellent": "Las conclusiones son proporcionales al contexto de uso y muestran correcciones justificadas tras revisión."},
        ],
    },
    "status": "complete",
}
dump(DST / "assessments" / "course-assessment.json", course_assessment)

# Permanent regression for this canonical closure.
test_text = '''from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "courses" / "biomecanica-medios-continuos"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomecanicaMediosContinuosCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((BASE / "course.json").read_text(encoding="utf-8"))

    def test_course_complete_human_review_pending(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_are_disciplinary_and_structured(self):
        expected = ["Descripción continua de tejidos", "Esfuerzo y equilibrio", "Elasticidad", "Viscoelasticidad y poroelasticidad", "Fluidos biológicos", "Elementos finitos y validación"]
        self.assertEqual(len(self.course["unit_files"]), 6)
        for n, relative in enumerate(self.course["unit_files"], 1):
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            self.assertEqual(unit["order"], n)
            self.assertEqual(unit["title"], expected[n-1])
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertGreaterEqual(len(unit["learning_outcomes"]), 5)
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 3)
            self.assertGreaterEqual(len(unit["activities"]), 1)
            self.assertGreaterEqual(len(unit["source_ids"]), 5)
            self.assertEqual(len(unit["claim_ids"]), 4)
            self.assertNotIn(GENERIC, json.dumps(unit, ensure_ascii=False).casefold())

    def test_registries_trace_every_unit(self):
        sources = json.loads((BASE / "sources.json").read_text(encoding="utf-8"))
        self.assertEqual(sources["coverage_gaps"], [])
        self.assertGreaterEqual(len(sources["sources"]), 30)
        self.assertTrue(all(s.get("verification_status") != "unverified" for s in sources["sources"]))
        glossary = json.loads((BASE / "glossary.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(glossary["entries"]), 70)
        self.assertTrue(all(e.get("source_ids") for e in glossary["entries"]))
        claims = json.loads((BASE / "claims.json").read_text(encoding="utf-8"))
        self.assertEqual(len(claims["claims"]), 24)
        by_unit = {}
        for claim in claims["claims"]:
            by_unit.setdefault(claim["unit_id"], []).append(claim)
            unit_n = int(claim["unit_id"].split("U")[-1])
            unit = json.loads((BASE / "units" / f"unit-{unit_n:02d}.json").read_text(encoding="utf-8"))
            self.assertIn(claim["text"], json.dumps(unit, ensure_ascii=False))
        self.assertTrue(all(len(v) == 4 for v in by_unit.values()))
        media = json.loads((BASE / "media.json").read_text(encoding="utf-8"))
        self.assertEqual(media["coverage_status"], "planned")
        self.assertEqual(len(media["items"]), 6)

    def test_unit_and_course_assessments_are_recoverable(self):
        for n in range(1, 7):
            assessment = json.loads((BASE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(assessment["items"]), 8)
            self.assertTrue(all(i.get("answer_key", {}).get("explanation") for i in assessment["items"]))
            self.assertTrue(all(i.get("feedback", {}).get("incorrect") for i in assessment["items"]))
            self.assertTrue(all(i.get("source_ids") for i in assessment["items"]))
        assessment = json.loads((BASE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(x["weight_percent"] for x in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(x["weight_percent"] for x in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)

    def test_all_course_outcomes_have_unit_coverage(self):
        mapped = set()
        for relative in self.course["unit_files"]:
            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))
            mapped.update(unit["course_learning_outcome_ids"])
        self.assertEqual(mapped, {x["id"] for x in self.course["learning_outcomes"]})

    def test_boundaries_are_explicit(self):
        notice = self.course["editorial_notice"].casefold()
        for phrase in ("revisión humana", "validación clínica", "certificación", "aprobación regulatoria"):
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
'''
(ROOT / "tests" / "test_biomecanica_medios_continuos_canonical.py").write_text(test_text, encoding="utf-8")

# Sanity checks before CI.
assert len(source_records) >= 30, len(source_records)
assert len(glossary_entries) >= 70, len(glossary_entries)
assert len(claims) == 24
assert sum(x["weight_percent"] for x in course_assessment["assessment_plan"]) == 100
assert sum(x["weight_percent"] for x in course_assessment["midterm_blueprint"]) == 100
assert sum(x["weight_percent"] for x in course_assessment["capstone"]["rubric"]) == 100
print(f"Canonical BMC built: {len(source_records)} sources, {len(glossary_entries)} glossary entries, {len(claims)} claims")
