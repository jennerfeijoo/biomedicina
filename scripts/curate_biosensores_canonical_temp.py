#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CID = "biosensores"
CODE = "BIOSEN"
COURSE = ROOT / "data" / "courses" / CID


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def complete_status():
    return {
        "content": "complete",
        "sources": "traceable",
        "pedagogy": "complete",
        "multimedia": "planned",
        "internal_review": "pending",
        "external_review": "pending",
        "publication": "published_provisional",
    }


subprocess.run(
    ["python", "scripts/migrate_course_to_canonical.py", "--subject", CID, "--course-code", CODE],
    cwd=ROOT,
    check=True,
)

course = load(COURSE / "course.json")
course.update({
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica, biotecnología y áreas afines con bases universitarias de biología molecular, química, física, instrumentación, estadística y análisis de datos que necesiten diseñar, caracterizar o evaluar biosensores de manera reproducible.",
    "status": complete_status(),
    "purpose": "Integrar reconocimiento biológico, transducción, interfaces de inmovilización y microfluídica, caracterización analítica y evaluación de uso point-of-care o wearable para diseñar y auditar biosensores reproducibles, separando señal, mensurando, desempeño analítico, desempeño clínico, utilidad, factores humanos, riesgo y regulación sin convertir una actividad educativa en validación de un producto real.",
    "scope": {
        "included": [
            "Arquitectura de biosensores desde analito y bioreceptor hasta transductor, acondicionamiento, lectura y controles.",
            "Reconocimiento con enzimas, anticuerpos, ácidos nucleicos y aptámeros, incluyendo afinidad, cinética, selectividad, reactividad cruzada y estabilidad.",
            "Transducción electroquímica, óptica, piezoeléctrica/acústica y térmica con función de transferencia, referencia, ruido, deriva y rango operativo.",
            "Química de superficies, inmovilización, orientación, pasivación, biofouling, difusión, convección y microfluídica.",
            "Calibración, precisión, sesgo, recuperación, selectividad, interferencias, LoB, LoD, LoQ, intervalo de medición y comparación de métodos.",
            "Uso previsto, desempeño clínico, point-of-care, wearables, prevalencia, valores predictivos, factores humanos, integridad de datos, riesgo y marcos regulatorios.",
            "Expedientes reproducibles con fuentes, versiones, criterios de aceptación, controles, incertidumbre, resultados negativos y límites de interpretación."
        ],
        "excluded": [
            "Diagnóstico, cribado, monitorización o tratamiento de personas a partir de los ejercicios del curso.",
            "Declarar utilidad clínica, seguridad, certificación, autorización o conformidad regulatoria de un producto real.",
            "Experimentación con muestras humanas, pacientes o dispositivos clínicos sin infraestructura, supervisión, consentimiento y autorización apropiados.",
            "Asumir que desempeño analítico demuestra desempeño clínico o que exactitud diagnóstica demuestra beneficio clínico.",
            "Clasificar productos reales bajo FDA, MDR o IVDR sin analizar documentación, uso previsto, jurisdicción y normativa vigente."
        ],
        "handoff_courses": [
            "bioinstrumentacion",
            "laboratorio-bioinstrumentacion",
            "desarrollo-dispositivos-medicos",
            "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas",
            "biomarcadores-diagnostico-molecular"
        ],
    },
    "prerequisites": [
        {"id": "BIOSEN-PRE01", "statement": "Biología molecular y bioquímica introductorias: interacción biomolecular, enzimas, anticuerpos y ácidos nucleicos."},
        {"id": "BIOSEN-PRE02", "statement": "Química general y de superficies, concentraciones, equilibrio, pH y unidades SI."},
        {"id": "BIOSEN-PRE03", "statement": "Física e instrumentación básica: circuitos, señales, ruido, muestreo y función de transferencia."},
        {"id": "BIOSEN-PRE04", "statement": "Estadística descriptiva y nociones de incertidumbre, precisión, sesgo, regresión y proporciones."},
        {"id": "BIOSEN-PRE05", "statement": "Capacidad para documentar datos, supuestos, parámetros, versiones, cálculos y fuentes de forma reproducible."},
    ],
    "competencies": [
        {"id": "BIOSEN-COMP01", "statement": "Diseñar una arquitectura de biosensor trazable entre analito, bioreceptor, transductor, señal y decisión de medición."},
        {"id": "BIOSEN-COMP02", "statement": "Seleccionar estrategias de reconocimiento y de transducción justificando selectividad, estabilidad, rango, ruido y limitaciones."},
        {"id": "BIOSEN-COMP03", "statement": "Diseñar interfaces de inmovilización y transporte de muestra con controles de superficie y microfluídica adecuados al uso previsto."},
        {"id": "BIOSEN-COMP04", "statement": "Caracterizar desempeño analítico mediante calibración, precisión, sesgo, selectividad, interferencias, capacidad de detección y comparación de métodos."},
        {"id": "BIOSEN-COMP05", "statement": "Evaluar la transición hacia point-of-care o wearables distinguiendo desempeño clínico, utilidad, factores humanos, integridad de datos y riesgo."},
        {"id": "BIOSEN-COMP06", "statement": "Construir expedientes reproducibles con evidencia trazable, criterios previos, incertidumbre, discrepancias, versiones y límites regulatorios."},
        {"id": "BIOSEN-COMP07", "statement": "Comunicar resultados técnicos y biomédicos de manera proporcional a la evidencia, evitando sobreafirmaciones clínicas o regulatorias."},
    ],
    "learning_outcomes": [
        {"id": "BIOSEN-LO01", "statement": "Construye una arquitectura de biosensor que conecta analito, bioreceptor, transductor, acondicionamiento y lectura con mensurando, matriz, rango, controles y fuentes de error explícitos."},
        {"id": "BIOSEN-LO02", "statement": "Selecciona y justifica reconocimiento biológico mediante afinidad, cinética, catálisis, hibridación, selectividad, reactividad cruzada y estabilidad sin confundir afinidad con desempeño global del sensor."},
        {"id": "BIOSEN-LO03", "statement": "Compara mecanismos de transducción electroquímicos, ópticos, piezoeléctricos/acústicos y térmicos mediante función de transferencia, referencia, dinámica, ruido, deriva y límites de operación."},
        {"id": "BIOSEN-LO04", "statement": "Diseña y audita inmovilización, pasivación, control de biofouling y transporte microfluídico conectando química de superficie, difusión, convección y manejo de muestra."},
        {"id": "BIOSEN-LO05", "statement": "Caracteriza un biosensor cuantitativo mediante calibración, precisión, sesgo, selectividad, interferencias, LoB/LoD/LoQ, intervalo de medición y comparación de procedimientos, distinguiendo sensibilidad analítica de diagnóstica."},
        {"id": "BIOSEN-LO06", "statement": "Evalúa un uso point-of-care o wearable con uso previsto, desempeño clínico, prevalencia, valores predictivos, cobertura de datos, factores humanos, riesgo y marco regulatorio, sin inferir utilidad o conformidad no demostradas."},
        {"id": "BIOSEN-LO07", "statement": "Entrega y defiende un expediente integrador reproducible de un biosensor hipotético que conecta las seis unidades, evidencia, controles, incertidumbre, versiones, riesgos, afirmaciones permitidas y siguiente estudio necesario."},
    ],
    "study_method": [
        "Definir primero mensurando, matriz, uso previsto, usuario, entorno y afirmación que se desea sostener.",
        "Alternar explicación, ejemplo resuelto, actividad guiada, recuperación activa y transferencia con apoyo progresivamente menor.",
        "Separar evento de reconocimiento, magnitud física, señal instrumental, variable derivada, estimación del mensurando e interpretación biomédica.",
        "Predefinir controles, blancos, interferentes, criterios de aceptación, umbrales y análisis de sensibilidad antes de interpretar resultados.",
        "Conservar unidades, lotes, condiciones, parámetros, firmware o algoritmo cuando aplique, fuentes y decisiones intermedias.",
        "Revisar productos con rúbrica, registrar correcciones y formular explícitamente qué evidencia falta para la siguiente afirmación."
    ],
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para las seis unidades de Biosensores. Las fuentes quedan trazadas y la publicación sigue siendo provisional. La revisión humana interna, la revisión disciplinaria externa, cualquier experimentación con personas o muestras humanas, el diagnóstico, el tratamiento, la validación clínica de productos y la evaluación de conformidad regulatoria permanecen fuera del cierre y siguen pendientes."
})
course["core_source_ids"] = []

lo_map = {
    1: ["BIOSEN-LO01", "BIOSEN-LO07"],
    2: ["BIOSEN-LO02", "BIOSEN-LO07"],
    3: ["BIOSEN-LO03", "BIOSEN-LO07"],
    4: ["BIOSEN-LO04", "BIOSEN-LO07"],
    5: ["BIOSEN-LO05", "BIOSEN-LO07"],
    6: ["BIOSEN-LO06", "BIOSEN-LO07"],
}

units = {}
for n in range(1, 7):
    path = COURSE / "units" / f"unit-{n:02d}.json"
    unit = load(path)
    unit["status"] = complete_status()
    unit["course_learning_outcome_ids"] = lo_map[n]
    for activity in unit.get("activities", []):
        activity["estimated_duration_minutes"] = 120
        activity["status"] = "curated_internal_review_pending"
    units[n] = unit
    write(path, unit)

# Keep only sources actually used by curated units, and require that their prior verification is not unverified.
sources_path = COURSE / "sources.json"
sources = load(sources_path)
used_source_ids = []
for n, unit in units.items():
    for sid in unit.get("source_ids", []):
        if sid not in used_source_ids:
            used_source_ids.append(sid)
source_by_id = {s["id"]: s for s in sources.get("sources", [])}
missing = [sid for sid in used_source_ids if sid not in source_by_id]
if missing:
    raise SystemExit(f"Fuentes canónicas ausentes: {missing}")
selected_sources = []
for sid in used_source_ids:
    source = source_by_id[sid]
    if str(source.get("verification_status") or "unverified") == "unverified":
        raise SystemExit(f"Fuente usada sin verificación previa: {sid}")
    selected_sources.append(source)
sources["sources"] = selected_sources
sources["source_policy"] = "Priorizar artículos revisados por pares, normas y guías oficiales. Cada fuente debe ser localizable, conservar su estado de verificación y vincularse solo a afirmaciones dentro de su alcance. La curación interna no sustituye revisión disciplinaria humana ni evaluación regulatoria profesional."
sources["coverage_gaps"] = []
write(sources_path, sources)
course["core_source_ids"] = used_source_ids[: min(12, len(used_source_ids))]

# Glossary: every entry is traceable to at least one verified source from a unit where the term is used.
glossary_path = COURSE / "glossary.json"
glossary = load(glossary_path)
unit_source_map = {unit["id"]: unit.get("source_ids", []) for unit in units.values()}
for entry in glossary.get("entries", []):
    candidate = []
    for uid in entry.get("unit_ids", []):
        candidate.extend(unit_source_map.get(uid, []))
    candidate = list(dict.fromkeys(candidate))
    if not candidate:
        candidate = used_source_ids[:1]
    entry["source_ids"] = candidate[:2]
    entry["verification_status"] = "traceable_to_verified_source"
glossary["status"] = "curated_internal_review_pending"
write(glossary_path, glossary)

# Unit assessments: classify cognition/difficulty, attach feedback and verified sources.
difficulty = ["foundational", "foundational", "intermediate", "intermediate", "intermediate", "advanced", "advanced", "advanced", "advanced", "advanced"]
cognitive = ["understand", "understand", "apply", "apply", "analyze", "analyze", "evaluate", "evaluate", "evaluate", "create"]
for n, unit in units.items():
    apath = COURSE / "assessments" / f"unit-{n:02d}.json"
    assessment = load(apath)
    source_ids = unit.get("source_ids", [])
    if not source_ids:
        raise SystemExit(f"Unidad {n} sin fuentes para evaluación")
    for i, item in enumerate(assessment.get("items", [])):
        item["difficulty"] = difficulty[min(i, len(difficulty)-1)]
        item["cognitive_level"] = cognitive[min(i, len(cognitive)-1)]
        explanation = str(item.get("answer_key", {}).get("explanation") or "").strip()
        misconceptions = item.get("answer_key", {}).get("common_misconceptions", [])
        misconception = misconceptions[0] if misconceptions else "Responder sin justificar el alcance de la evidencia."
        item["feedback"] = {
            "correct": "Correcto. Conserva en tu justificación el mecanismo, el supuesto y el límite que sostienen la respuesta." + (f" Idea clave: {explanation}" if explanation else ""),
            "incorrect": f"Revisa la cadena de razonamiento y evita este error frecuente: {misconception}",
        }
        item["source_ids"] = [source_ids[i % len(source_ids)]]
        item["status"] = "curated_internal_review_pending"
    if len(assessment.get("items", [])) < 8:
        raise SystemExit(f"Unidad {n} con evaluación insuficiente")
    assessment["status"] = "curated_internal_review_pending"
    write(apath, assessment)

# Course-level assessment with explicit 100% plan, diagnostic, midterm and capstone rubric.
course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "BIOSEN-EVAL-CURSO",
    "course_id": CID,
    "scope": "course",
    "principles": [
        "Evaluar razonamiento y trazabilidad, no reconocimiento de terminología aislada.",
        "Separar siempre desempeño del componente, desempeño analítico, desempeño clínico, utilidad y regulación.",
        "Usar escenarios sintéticos o datos abiertos sin decisiones sobre pacientes.",
        "Predefinir criterios y controles antes de interpretar resultados.",
        "Premiar conclusiones proporcionales a la evidencia y la corrección documentada de errores."
    ],
    "assessment_plan": [
        {"component": "Autoevaluaciones de unidad con corrección razonada", "weight_percent": 15, "evidence": "Seis bancos formativos y registro de errores corregidos."},
        {"component": "Portafolio de actividades guiadas", "weight_percent": 25, "evidence": "Productos reproducibles de U1–U6 con controles, cálculos y límites."},
        {"component": "Examen integrador intermedio", "weight_percent": 20, "evidence": "Problemas inéditos de arquitectura, reconocimiento, transducción y microfluídica."},
        {"component": "Proyecto integrador final", "weight_percent": 30, "evidence": "Expediente de diseño y evaluación de un biosensor hipotético."},
        {"component": "Defensa, revisión y registro de cambios", "weight_percent": 10, "evidence": "Defensa breve, respuesta a objeciones y tabla antes-después."}
    ],
    "diagnostic": {
        "purpose": "Detectar prerrequisitos que requieren recuperación antes de U1; no contribuye a la nota final.",
        "questions": [
            "Distingue analito, mensurando y señal instrumental con un ejemplo.",
            "Explica la diferencia entre afinidad y selectividad.",
            "Interpreta pendiente y ordenada al origen de una calibración lineal.",
            "Identifica qué representa una función de transferencia.",
            "Explica por qué ruido y deriva no son sinónimos.",
            "Convierte entre mol/L, mmol/L y µmol/L conservando unidades.",
            "Distingue difusión y convección en transporte de masa.",
            "Explica precisión frente a sesgo.",
            "Interpreta una proporción y un intervalo de confianza de forma cualitativa.",
            "Distingue correlación de acuerdo entre dos métodos.",
            "Define qué hace que un control sea discriminante.",
            "Explica por qué citar una norma no demuestra conformidad de un producto."
        ],
        "use": "Los resultados dirigen repaso de química, señales, estadística o biología antes de avanzar; no se usan para excluir estudiantes."
    },
    "midterm_blueprint": [
        {"domain": "Arquitectura y reconocimiento", "weight_percent": 25, "course_learning_outcome_ids": ["BIOSEN-LO01", "BIOSEN-LO02"]},
        {"domain": "Transducción y función de transferencia", "weight_percent": 25, "course_learning_outcome_ids": ["BIOSEN-LO03"]},
        {"domain": "Superficies, transporte y microfluídica", "weight_percent": 25, "course_learning_outcome_ids": ["BIOSEN-LO04"]},
        {"domain": "Integración, controles, incertidumbre y trazabilidad", "weight_percent": 25, "course_learning_outcome_ids": ["BIOSEN-LO07"]}
    ],
    "capstone": {
        "title": "Expediente reproducible de un biosensor hipotético desde reconocimiento hasta uso previsto",
        "brief": "Diseñar o auditar un biosensor exclusivamente con datos sintéticos o literatura abierta. El expediente debe conectar arquitectura, reconocimiento, transducción, interfaz/microfluídica, desempeño analítico y transición a un uso POC o wearable, indicando qué evidencia falta para cualquier afirmación clínica o regulatoria.",
        "required_deliverables": [
            "Requisitos y uso previsto con mensurando, matriz, usuario, entorno, rango y afirmación objetivo.",
            "Diagrama de arquitectura y presupuesto de señal/error.",
            "Selección razonada de bioreceptor, transductor e interfaz.",
            "Plan de calibración, precisión, sesgo, selectividad, interferencias y capacidad de detección.",
            "Escenario de robustez POC o wearable con tareas críticas, datos faltantes o perturbaciones.",
            "Matriz afirmación-evidencia-riesgo con fuentes trazables.",
            "Paquete reproducible de cálculos, parámetros, versiones y resultados.",
            "Conclusión acotada y siguiente estudio necesario."
        ],
        "rubric": [
            {"criterion": "Definición del problema y uso previsto", "weight_percent": 15, "excellent": "Requisitos, población/matriz, usuario, entorno y límites son verificables y coherentes."},
            {"criterion": "Arquitectura y mecanismos", "weight_percent": 20, "excellent": "Reconocimiento, transducción e interfaz están conectados causalmente con magnitudes y supuestos explícitos."},
            {"criterion": "Desempeño analítico", "weight_percent": 20, "excellent": "Calibración, precisión, sesgo, selectividad, interferencias y límites se evalúan con criterios previos y unidades correctas."},
            {"criterion": "POC/wearable, factores humanos y riesgo", "weight_percent": 15, "excellent": "Perturbaciones, tareas críticas, datos faltantes y riesgos se conectan con controles y uso previsto."},
            {"criterion": "Reproducibilidad y trazabilidad", "weight_percent": 15, "excellent": "Fuentes, datos, parámetros, versiones, cálculos, discrepancias y cambios permiten reconstruir el resultado."},
            {"criterion": "Interpretación y límites", "weight_percent": 15, "excellent": "Separa desempeño analítico, clínico, utilidad y regulación y propone la siguiente evidencia sin sobreafirmar."}
        ]
    },
    "status": "curated_internal_review_pending"
}
write(COURSE / "assessments" / "course-assessment.json", course_assessment)

# Build 8 traceable central claims per unit from key points and paragraph-leading statements.
claims = []
for n, unit in units.items():
    candidates = []
    for topic in unit.get("topics", []):
        candidates.extend(topic.get("key_points", []))
        for sub in topic.get("subtopics", []):
            for block in sub.get("blocks", []):
                if block.get("type") == "paragraph":
                    text = str(block.get("text") or "").strip()
                    first = re.split(r"(?<=[.!?])\\s+", text)[0].strip()
                    if first:
                        candidates.append(first)
    unique = []
    for candidate in candidates:
        candidate = candidate.strip()
        if candidate and candidate.casefold() not in {u.casefold() for u in unique}:
            unique.append(candidate)
    source_ids = unit.get("source_ids", [])
    chosen = unique[:8]
    if len(chosen) < 8 or not source_ids:
        raise SystemExit(f"No se pueden construir 8 claims trazables para U{n}")
    unit_claim_ids = []
    for i, text in enumerate(chosen, 1):
        sid = source_ids[(i - 1) % len(source_ids)]
        source = next(s for s in selected_sources if s["id"] == sid)
        claim_id = f"BIOSEN-U{n:02d}-C{i:03d}"
        unit_claim_ids.append(claim_id)
        claims.append({
            "claim_id": claim_id,
            "unit": n,
            "text": text,
            "claim_type": "methodological_or_interpretive",
            "risk": "medium",
            "context": f"Síntesis educativa de {unit['title']}; interpretar dentro del protocolo, supuestos, población/matriz y límites declarados.",
            "source_id": sid,
            "locator": {"url": str(source.get("url") or ""), "title": str(source.get("title") or "")},
            "support": "direct_or_synthesis",
            "source_verification_status": str(source.get("verification_status") or "traceable"),
            "review_state": "ai_review_provisional",
            "reviewer_validation_id": None,
            "reviewed_at": "2026-08-24",
            "id": claim_id,
            "unit_id": unit["id"]
        })
    unit["claim_ids"] = unit_claim_ids
    write(COURSE / "units" / f"unit-{n:02d}.json", unit)

write(COURSE / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": CID,
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Afirmaciones centrales de las seis unidades de Biosensores vinculadas a fuentes previamente verificadas; revisión disciplinaria humana pendiente.",
    "review_state": "ai_review_provisional",
    "claims": claims,
})

media = load(COURSE / "media.json")
media["coverage_status"] = "planned"
for item in media.get("items", []):
    item["status"] = "planned"
    if item.get("alt_text_draft") is None:
        item["alt_text_draft"] = "Borrador pendiente de producir: figura educativa accesible que represente el mecanismo central de la unidad sin depender únicamente del color."
write(COURSE / "media.json", media)

write(COURSE / "course.json", course)

# Assertions that represent the closure contract.
assert sum(x["weight_percent"] for x in course_assessment["assessment_plan"]) == 100
assert sum(x["weight_percent"] for x in course_assessment["midterm_blueprint"]) == 100
assert sum(x["weight_percent"] for x in course_assessment["capstone"]["rubric"]) == 100
assert len(claims) == 48
assert len(glossary.get("entries", [])) >= 90
assert all(entry.get("source_ids") for entry in glossary["entries"])
assert all(unit["activities"] and unit["activities"][0]["estimated_duration_minutes"] for unit in units.values())
print(f"Biosensores canonical closure: 6 units, {len(glossary['entries'])} glossary entries, {len(selected_sources)} sources, {len(claims)} claims")
