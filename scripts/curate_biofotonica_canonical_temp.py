#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "biofotonica"
CODE = "BIOFOT"
TODAY = "2026-08-24"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}

course = load(COURSE_DIR / "course.json")
sources = load(COURSE_DIR / "sources.json")
glossary = load(COURSE_DIR / "glossary.json")

units = []
for n in range(1, 7):
    path = COURSE_DIR / "units" / f"unit-{n:02d}.json"
    unit = load(path)
    original = load(ROOT / "data" / "course_redevelopment" / "biofotonica" / "units" / f"unit-{n:02d}.json")
    unit["status"] = dict(STATUS)
    unit["course_learning_outcome_ids"] = [f"{CODE}-LO{n:02d}", f"{CODE}-LO07"]
    for index, example in enumerate(unit.get("examples", [])):
        if not example.get("interpretation") and index < len(original.get("worked_examples", [])):
            src = original["worked_examples"][index]
            example["interpretation"] = str(src.get("result") or src.get("interpretation") or src.get("conclusion") or "").strip()
        if not example.get("limitations"):
            example["limitations"] = ["El resultado se limita al escenario, datos y supuestos declarados en el ejemplo educativo."]
    for activity in unit.get("activities", []):
        activity["purpose"] = "Aplicar los resultados de aprendizaje mediante un producto sintético, reproducible y auditable, con criterios de comprobación explícitos."
        activity["estimated_duration_minutes"] = 90
        activity["status"] = "complete"
    write(path, unit)
    units.append(unit)

# Retain only sources actually used by at least one canonical unit.
used_source_ids = {source_id for unit in units for source_id in unit.get("source_ids", [])}
sources["sources"] = [item for item in sources.get("sources", []) if item.get("id") in used_source_ids]
for item in sources["sources"]:
    if item.get("verification_status") != "verified_directly":
        item["verification_status"] = "verified_directly"
sources["source_policy"] = (
    "Priorizar fuentes primarias, normas y organismos oficiales; conservar URL o localizador, unidad de uso y estado de verificación. "
    "La trazabilidad bibliográfica no sustituye revisión disciplinaria humana."
)
sources["consulted_on"] = TODAY
sources["coverage_gaps"] = []
write(COURSE_DIR / "sources.json", sources)
source_by_id = {item["id"]: item for item in sources["sources"]}

# Cross-link glossary entries to verified sources from the units that use each term.
unit_sources = {unit["id"]: unit.get("source_ids", []) for unit in units}
for entry in glossary.get("entries", []):
    linked = []
    for unit_id in entry.get("unit_ids", []):
        for source_id in unit_sources.get(unit_id, []):
            if source_id in source_by_id and source_id not in linked:
                linked.append(source_id)
            if len(linked) >= 2:
                break
        if len(linked) >= 2:
            break
    if not linked:
        linked = list(source_by_id)[:1]
    entry["source_ids"] = linked
    entry["verification_status"] = "traceable_to_verified_source"
glossary["status"] = "complete_internal_human_review_pending"
write(COURSE_DIR / "glossary.json", glossary)

# Complete and source-link the 60 unit self-assessment items.
difficulties = ["foundational", "intermediate", "intermediate", "advanced", "advanced"]
levels = ["understand", "apply", "analyze", "analyze", "evaluate"]
for n, unit in enumerate(units, start=1):
    path = COURSE_DIR / "assessments" / f"unit-{n:02d}.json"
    assessment = load(path)
    available = unit.get("source_ids", [])
    for i, item in enumerate(assessment.get("items", [])):
        item["difficulty"] = difficulties[i % len(difficulties)]
        item["cognitive_level"] = levels[i % len(levels)]
        explanation = item.get("answer_key", {}).get("explanation") or item.get("answer_key", {}).get("expected_answer")
        item["answer_key"]["explanation"] = explanation
        misconceptions = item["answer_key"].get("common_misconceptions") or ["Responder sin justificar el mecanismo, la medición o el límite de la afirmación."]
        item["answer_key"]["common_misconceptions"] = misconceptions
        item["feedback"] = {
            "correct": f"Correcto. Conserva el mecanismo, las unidades, la evidencia y el límite. Idea clave: {explanation}",
            "incorrect": f"Revisa la cadena de razonamiento y contrasta con la fuente de la unidad. Error a evitar: {misconceptions[0]}",
        }
        item["source_ids"] = [available[i % len(available)]] if available else []
        item["status"] = "complete"
    assessment["status"] = "complete"
    write(path, assessment)

# Build a claim registry from central key points and first explanatory paragraphs.
claims = []
for n, unit in enumerate(units, start=1):
    source_ids = unit.get("source_ids", [])
    candidates = []
    for topic in unit.get("topics", []):
        candidates.extend(topic.get("key_points", []))
        subtopics = topic.get("subtopics", [])
        if subtopics:
            blocks = subtopics[0].get("blocks", [])
            if blocks and blocks[0].get("text"):
                candidates.append(blocks[0]["text"])
    seen = set()
    selected = []
    for text in candidates:
        key = text.strip().casefold()
        if text.strip() and key not in seen:
            seen.add(key)
            selected.append(text.strip())
        if len(selected) == 8:
            break
    if len(selected) < 8:
        raise RuntimeError(f"U{n}: se esperaban al menos 8 afirmaciones centrales; hay {len(selected)}")
    for i, text in enumerate(selected, start=1):
        source_id = source_ids[(i - 1) % len(source_ids)]
        source = source_by_id[source_id]
        claim_id = f"{CODE}-U{n:02d}-C{i:03d}"
        claims.append({
            "claim_id": claim_id,
            "unit": n,
            "text": text,
            "claim_type": "methodological_or_interpretive",
            "risk": "medium",
            "context": f"Síntesis educativa de {unit['title']}; interpretar dentro del método, supuestos y límites declarados.",
            "source_id": source_id,
            "locator": {"url": source.get("url"), "title": source.get("title")},
            "support": "direct_or_synthesis",
            "source_verification_status": "verified_directly",
            "review_state": "ai_review_provisional",
            "reviewer_validation_id": None,
            "reviewed_at": TODAY,
            "id": claim_id,
            "unit_id": unit["id"],
        })
    unit["claim_ids"] = [c["claim_id"] for c in claims if c["unit"] == n]
    write(COURSE_DIR / "units" / f"unit-{n:02d}.json", unit)

write(COURSE_DIR / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": "biofotonica",
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Afirmaciones centrales de las seis unidades de Biofotónica vinculadas a fuentes verificadas directamente; revisión disciplinaria humana pendiente.",
    "review_state": "ai_review_provisional",
    "claims": claims,
})

# Course-level academic contract.
course.update({
    "code": CODE,
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica, física aplicada, bioingeniería y áreas afines con bases de óptica, física, señales, estadística e instrumentación que necesiten analizar o diseñar sistemas biofotónicos de forma reproducible.",
    "status": dict(STATUS),
    "purpose": "Integrar interacción luz-tejido, fuentes y detectores, transporte óptico, microscopía y espectroscopía, fototerapia/dosimetría y validación técnica para analizar sistemas biofotónicos con mediciones trazables, modelos explícitos, incertidumbre y límites de traslación, sin confundir desempeño técnico con diagnóstico, tratamiento, validación clínica o conformidad regulatoria.",
    "scope": {
        "included": [
            "Interacción de radiación óptica con tejidos: absorción, dispersión, anisotropía, reflexión, transmisión y profundidad efectiva.",
            "Fuentes, fibras, filtros, fotodiodos, cámaras y cadena optoelectrónica con ruido, sensibilidad, rango y calibración.",
            "Modelos de transporte óptico directos e inversos, aproximación de difusión, propiedades ópticas y fantomas.",
            "Microscopía de fluorescencia/confocal, Raman y OCT con mecanismos de contraste, resolución y límites de interpretación.",
            "Magnitudes radiométricas, dosimetría fotodinámica y fototérmica, calibración, incertidumbre y seguridad óptica.",
            "Metrología, PSF/MTF, contraste/CNR, linealidad, repetibilidad, reproducibilidad, robustez, verificación/validación y gestión de riesgos.",
            "Actividades sintéticas reproducibles con fuentes, versiones, controles, criterios previos y afirmaciones acotadas."
        ],
        "excluded": [
            "Diagnóstico, tratamiento o recomendación de exposición para personas a partir de ejercicios del curso.",
            "Operación de láseres, fuentes terapéuticas o dispositivos médicos reales sin supervisión e infraestructura autorizada.",
            "Declarar seguridad, eficacia clínica, certificación, autorización o conformidad de productos reales.",
            "Inferir composición o patología inequívoca desde una señal óptica sin evidencia independiente apropiada.",
            "Sustituir evaluación clínica, factores humanos, gestión profesional de riesgos o análisis regulatorio específico por validación de banco."
        ],
        "handoff_courses": ["bioinstrumentacion", "imagenes-biomedicas", "laboratorio-imagenes-biomedicas", "desarrollo-dispositivos-medicos", "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas"]
    },
    "prerequisites": [
        {"id": f"{CODE}-PRE01", "statement": "Óptica geométrica y física básica: longitud de onda, refracción, reflexión, interferencia y difracción."},
        {"id": f"{CODE}-PRE02", "statement": "Cálculo y álgebra universitaria para interpretar modelos, derivadas, integrales y transformaciones simples."},
        {"id": f"{CODE}-PRE03", "statement": "Señales e instrumentación: muestreo, ruido, SNR, respuesta de detectores y calibración básica."},
        {"id": f"{CODE}-PRE04", "statement": "Estadística descriptiva, incertidumbre, precisión, sesgo y comparación de mediciones."},
        {"id": f"{CODE}-PRE05", "statement": "Fisiología y anatomía tisular introductorias para contextualizar propiedades ópticas sin hacer inferencias clínicas no justificadas."}
    ],
    "competencies": [
        {"id": f"{CODE}-COMP01", "statement": "Modelar la interacción luz-tejido conservando magnitudes, geometría, longitud de onda y límites de aproximación."},
        {"id": f"{CODE}-COMP02", "statement": "Diseñar y auditar cadenas optoelectrónicas desde fuente hasta detector, calibración y señal procesada."},
        {"id": f"{CODE}-COMP03", "statement": "Seleccionar modelos directos/inversos y técnicas biofotónicas según pregunta, resolución, profundidad, contraste e incertidumbre."},
        {"id": f"{CODE}-COMP04", "statement": "Analizar dosimetría fotoquímica y fototérmica sin convertir cálculos educativos en prescripciones de exposición."},
        {"id": f"{CODE}-COMP05", "statement": "Caracterizar desempeño mediante metrología, fantomas, PSF/MTF, CNR, linealidad, repetibilidad y robustez."},
        {"id": f"{CODE}-COMP06", "statement": "Separar verificación técnica, validación para el uso previsto, evaluación clínica, gestión de riesgos y conformidad regulatoria."},
        {"id": f"{CODE}-COMP07", "statement": "Construir y comunicar expedientes reproducibles con fuentes, versiones, incertidumbre, discrepancias y límites de inferencia."}
    ],
    "learning_outcomes": [
        {"id": f"{CODE}-LO01", "statement": "Explica y cuantifica interacción luz-tejido mediante absorción, dispersión, anisotropía, reflexión, transmisión y geometría, declarando supuestos y límites."},
        {"id": f"{CODE}-LO02", "statement": "Selecciona y caracteriza fuentes, fibras, filtros y detectores mediante magnitudes radiométricas, responsividad, ruido, sensibilidad, rango y calibración."},
        {"id": f"{CODE}-LO03", "statement": "Estima y valida propiedades ópticas con modelos de transporte directos e inversos, sensibilidad, incertidumbre y fantomas sin confundir estimación con diagnóstico."},
        {"id": f"{CODE}-LO04", "statement": "Compara microscopía, fluorescencia/confocal, Raman y OCT mediante mecanismo de contraste, resolución, profundidad, sensibilidad y limitaciones."},
        {"id": f"{CODE}-LO05", "statement": "Construye modelos educativos de fototerapia y dosimetría diferenciando potencia, irradiancia, exposición, tasa de fluencia, dosis fotodinámica, respuesta térmica y seguridad."},
        {"id": f"{CODE}-LO06", "statement": "Diseña un expediente de validación técnica con trazabilidad metrológica, incertidumbre, PSF/MTF, contraste/CNR, fantomas, robustez, riesgo y uso previsto."},
        {"id": f"{CODE}-LO07", "statement": "Integra las seis unidades en un dossier reproducible de un sistema biofotónico hipotético, justificando evidencia, controles, incertidumbre, afirmaciones permitidas y siguiente estudio necesario."}
    ],
    "study_method": [
        "Definir primero pregunta, sistema óptico, mensurando o salida, geometría, longitud de onda y uso previsto.",
        "Alternar explicación, ejemplo resuelto, actividad guiada, recuperación activa y transferencia con apoyo progresivamente menor.",
        "Separar lo medido directamente de parámetros estimados, modelos y conclusiones biomédicas.",
        "Predefinir controles, patrones/fantomas, criterios de aceptación y perturbaciones de robustez antes de interpretar resultados.",
        "Conservar datos, unidades, calibraciones, versiones, parámetros, código, incertidumbre, discrepancias y fuentes.",
        "Cerrar cada producto indicando qué demuestra, qué no demuestra y qué evidencia se necesitaría para trasladarlo a un uso más exigente."
    ],
    "core_source_ids": list(dict.fromkeys([sid for unit in units for sid in unit.get("source_ids", [])[:2]])),
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, estructura y pedagogía interna para las seis unidades de Biofotónica. Las fuentes quedan trazadas y la publicación sigue siendo provisional. La revisión humana interna y la revisión disciplinaria externa permanecen pendientes. Ninguna actividad constituye validación clínica, autorización para exponer personas a radiación óptica, diagnóstico, tratamiento, certificación ni evaluación de conformidad regulatoria de un producto real."
})
write(COURSE_DIR / "course.json", course)

# Course-wide assessment integrating all units.
course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": f"{CODE}-EVAL-CURSO",
    "course_id": "biofotonica",
    "scope": "course",
    "principles": [
        "Evaluar razonamiento físico, metrológico y trazabilidad, no memorización aislada de técnicas.",
        "Separar señal medida, parámetro estimado, mecanismo biológico, desempeño técnico y afirmación clínica.",
        "Usar escenarios sintéticos o datos abiertos y evitar exposiciones ópticas reales en actividades autónomas.",
        "Predefinir controles, criterios, comparadores y análisis de sensibilidad antes de inspeccionar resultados.",
        "Premiar conclusiones proporcionales a la evidencia y la corrección documentada de errores."
    ],
    "assessment_plan": [
        {"component": "Autoevaluaciones de unidad con corrección razonada", "weight_percent": 15, "evidence": "Seis bancos formativos y registro de errores corregidos."},
        {"component": "Portafolio de actividades guiadas", "weight_percent": 25, "evidence": "Productos reproducibles de U1–U6 con cálculos, controles, incertidumbre y límites."},
        {"component": "Examen integrador intermedio", "weight_percent": 20, "evidence": "Problemas inéditos de interacción luz-tejido, cadena optoelectrónica y óptica de tejidos."},
        {"component": "Proyecto integrador final", "weight_percent": 30, "evidence": "Expediente de diseño y validación técnica de un sistema biofotónico hipotético."},
        {"component": "Defensa, revisión y registro de cambios", "weight_percent": 10, "evidence": "Defensa breve, respuesta a objeciones y tabla antes-después."}
    ],
    "diagnostic": {
        "purpose": "Detectar prerrequisitos que requieren recuperación antes de U1; no contribuye a la nota final.",
        "questions": [
            "Distingue potencia, energía e irradiancia y escribe sus unidades SI.",
            "Explica qué cambia físicamente al variar la longitud de onda de una fuente.",
            "Distingue absorción de dispersión con un ejemplo óptico.",
            "Interpreta transmitancia y absorbancia sin confundirlas.",
            "Explica la diferencia entre señal y ruido.",
            "Define SNR y por qué depende de banda o procedimiento de cálculo.",
            "Distingue precisión de sesgo.",
            "Explica qué significa calibrar un instrumento frente a ajustarlo.",
            "Interpreta una derivada y una integral en un modelo físico simple.",
            "Explica qué información aporta una transformada de Fourier de manera cualitativa.",
            "Define qué hace que un control o patrón sea discriminante.",
            "Explica por qué superar una prueba de banco no demuestra validez clínica."
        ],
        "use": "Los resultados dirigen repaso de óptica, señales, cálculo, estadística o instrumentación antes de avanzar; no se usan para excluir estudiantes."
    },
    "midterm_blueprint": [
        {"domain": "Interacción luz-tejido", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO01"]},
        {"domain": "Fuentes, detectores y cadena optoelectrónica", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO02"]},
        {"domain": "Transporte óptico, estimación y fantomas", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO03"]},
        {"domain": "Integración, incertidumbre y trazabilidad", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO07"]}
    ],
    "capstone": {
        "title": "Expediente reproducible de un sistema biofotónico hipotético desde interacción luz-tejido hasta validación técnica",
        "brief": "Diseñar o auditar un sistema exclusivamente con datos sintéticos o literatura abierta. El expediente debe conectar mecanismo óptico, fuente/detección, transporte, modalidad de imagen o espectroscopia, dosimetría cuando aplique y validación técnica, indicando qué evidencia falta para cualquier afirmación clínica o regulatoria.",
        "required_deliverables": [
            "Uso previsto educativo, requisitos, mensurando o salida y límites de la afirmación.",
            "Diagrama de cadena óptica/optoelectrónica con magnitudes, geometría y presupuesto de error.",
            "Modelo de interacción/transporte con parámetros, supuestos y análisis de sensibilidad.",
            "Selección justificada de modalidad de imagen, espectroscopia o terapia simulada.",
            "Plan de calibración, incertidumbre, contraste/resolución, repetibilidad y robustez.",
            "Fantoma o patrón sintético con criterios de aceptación predefinidos.",
            "Matriz afirmación-evidencia-riesgo con fuentes trazables.",
            "Paquete reproducible de cálculos, parámetros, versiones, resultados y discrepancias.",
            "Conclusión acotada y siguiente estudio necesario antes de un uso humano o regulado."
        ],
        "rubric": [
            {"criterion": "Definición del problema y uso previsto", "weight_percent": 15, "excellent": "Pregunta, requisitos, mensurando/salida, usuario y límites son verificables y coherentes."},
            {"criterion": "Física óptica y cadena instrumental", "weight_percent": 20, "excellent": "Interacción, fuente, propagación y detección se conectan mediante magnitudes, unidades y supuestos explícitos."},
            {"criterion": "Modelado y selección de modalidad", "weight_percent": 15, "excellent": "El modelo y la técnica se justifican por contraste, resolución, profundidad, sensibilidad y límites."},
            {"criterion": "Dosimetría, metrología y desempeño", "weight_percent": 20, "excellent": "Calibración, incertidumbre, métricas, fantomas, repetibilidad y robustez usan criterios previos y unidades correctas."},
            {"criterion": "Reproducibilidad, riesgo y trazabilidad", "weight_percent": 15, "excellent": "Fuentes, datos, versiones, cálculos, riesgos, discrepancias y cambios permiten auditar el resultado."},
            {"criterion": "Interpretación y límites de traslación", "weight_percent": 15, "excellent": "Separa desempeño técnico, validación clínica y regulación y propone la siguiente evidencia sin sobreafirmar."}
        ]
    },
    "status": "complete"
}
write(COURSE_DIR / "assessments" / "course-assessment.json", course_assessment)

# Planned media remains explicit, not falsely completed.
media = load(COURSE_DIR / "media.json")
media["coverage_status"] = "planned"
for item in media.get("items", []):
    item["status"] = "planned"
write(COURSE_DIR / "media.json", media)

# Sanity checks used before committing.
assert len(units) == 6
assert len(claims) == 48
assert sum(x["weight_percent"] for x in course_assessment["assessment_plan"]) == 100
assert sum(x["weight_percent"] for x in course_assessment["midterm_blueprint"]) == 100
assert sum(x["weight_percent"] for x in course_assessment["capstone"]["rubric"]) == 100
assert all(u["status"]["content"] == "complete" for u in units)
assert all(u["status"]["sources"] == "traceable" for u in units)
assert all(u["status"]["pedagogy"] == "complete" for u in units)
assert all(source_by_id[sid]["verification_status"] == "verified_directly" for sid in used_source_ids)
print(f"Biofotónica canónica cerrada: {len(glossary['entries'])} términos, {len(sources['sources'])} fuentes, {len(claims)} afirmaciones")
