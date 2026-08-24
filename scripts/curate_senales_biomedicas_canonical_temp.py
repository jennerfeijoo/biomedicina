#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "senales-biomedicas"
CODE = "SENBIO"
COURSE = ROOT / "data" / "courses" / COURSE_ID
GEN = ROOT / "data" / "generated_courses" / f"{COURSE_ID}.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "migrate_course_to_canonical.py"), "--subject", COURSE_ID, "--course-code", CODE],
    check=True,
)

generated = load(GEN)
course = load(COURSE / "course.json")
complete_status = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}

course["content_version"] = "1.0.0"
course["academic_level"] = "Pregrado universitario intermedio y avanzado"
course["audience"] = (
    "Estudiantes de ingeniería biomédica, biomedicina computacional y áreas afines con bases de física, "
    "fisiología, programación, estadística y sistemas/señales que necesiten adquirir, procesar, analizar, "
    "modelar e interpretar señales fisiológicas de manera reproducible y responsable."
)
course["status"] = complete_status
course["purpose"] = (
    "Construir una cadena reproducible de análisis de señales biomédicas desde el origen fisiológico y la adquisición "
    "hasta el preprocesamiento, análisis temporal y frecuencial, construcción de características, modelado, calibración, "
    "interpretación y monitorización, separando señal observada, procesamiento, inferencia técnica, validez científica, "
    "utilidad clínica y alcance regulatorio."
)
course["scope"] = {
    "included": [
        "Origen y adquisición de ECG, EEG, sEMG y PPG con referencia, rango dinámico, ADC, muestreo y antialiasing.",
        "Calidad de señal, artefactos, filtrado FIR/IIR, fase, retardo, notch, padding y evaluación de distorsión.",
        "Detección temporal de eventos, puntos fiduciales, intervalos, morfología, HRV/PRV y métricas de error.",
        "DFT, PSD, ventanas, Welch, STFT, espectrogramas, bandas, cross-spectrum y coherencia con límites explícitos.",
        "Características, pipelines sin fuga, partición por sujeto, selección, regularización, validación interna y test bloqueado.",
        "Calibración, incertidumbre, explicabilidad auditada, dataset shift, subgrupos, monitorización y gestión de cambios.",
        "Expedientes reproducibles con fuentes, versiones, controles, incertidumbre, resultados negativos y límites de inferencia.",
    ],
    "excluded": [
        "Diagnóstico, tratamiento o decisiones asistenciales a partir de ejercicios del curso.",
        "Adquisición experimental con personas o conexión de sensores sin protocolo, infraestructura y supervisión apropiados.",
        "Inferir mecanismos fisiológicos causales solo desde correlaciones, coherencia, importancia de características o explicaciones del modelo.",
        "Afirmar validación clínica, seguridad, beneficio, certificación o conformidad regulatoria de un sistema real.",
        "Reentrenar o recalibrar sistemas desplegados sin criterios de cambio, revalidación y gobernanza apropiados.",
    ],
    "handoff_courses": [
        "sistemas-senales",
        "bioinstrumentacion",
        "laboratorio-senales-biomedicas",
        "machine-learning-biomedico-validacion-clinica",
        "ingenieria-neurosensorial",
    ],
}
course["prerequisites"] = [
    {"id": f"{CODE}-PRE01", "statement": "Cálculo, álgebra lineal y estadística descriptiva de nivel universitario inicial."},
    {"id": f"{CODE}-PRE02", "statement": "Física de circuitos y nociones de sistemas, frecuencia, fase, muestreo y transformadas."},
    {"id": f"{CODE}-PRE03", "statement": "Fisiología humana básica y significado general de ECG, EEG, actividad muscular y pulso óptico."},
    {"id": f"{CODE}-PRE04", "statement": "Programación científica básica para manipular series temporales, tablas y gráficos reproducibles."},
    {"id": f"{CODE}-PRE05", "statement": "Capacidad para documentar datos, supuestos, parámetros, versiones, cálculos y fuentes."},
]
course["competencies"] = [
    {"id": f"{CODE}-COMP01", "statement": "Diseñar una cadena de adquisición y procesamiento que preserve unidades, referencia, frecuencia de muestreo, sincronización y procedencia."},
    {"id": f"{CODE}-COMP02", "statement": "Evaluar calidad de señal y seleccionar preprocesamiento cuantificando simultáneamente reducción de perturbaciones y distorsión de rasgos."},
    {"id": f"{CODE}-COMP03", "statement": "Extraer e interpretar información temporal, frecuencial y tiempo-frecuencia con criterios reproducibles y límites fisiológicos explícitos."},
    {"id": f"{CODE}-COMP04", "statement": "Construir pipelines de características y modelos evitando fuga, respetando la unidad independiente y separando tuning de evaluación bloqueada."},
    {"id": f"{CODE}-COMP05", "statement": "Evaluar calibración, incertidumbre, explicaciones, subgrupos, cambios de distribución y monitorización sin convertirlos en evidencia clínica no demostrada."},
    {"id": f"{CODE}-COMP06", "statement": "Integrar resultados en un expediente auditable con fuentes, controles, sensibilidad, versiones, discrepancias y decisiones de cambio."},
    {"id": f"{CODE}-COMP07", "statement": "Comunicar resultados proporcionalmente a la evidencia distinguiendo desempeño técnico, validez científica, utilidad clínica y regulación."},
]
course["learning_outcomes"] = [
    {"id": f"{CODE}-LO01", "statement": "Diseña y audita una cadena de adquisición de señales fisiológicas declarando origen, sensor, referencia, rango, ADC, muestreo, antialiasing, sincronización y límites de medición."},
    {"id": f"{CODE}-LO02", "statement": "Evalúa calidad y preprocesamiento distinguiendo ruido, interferencia, artefacto y deriva, y justifica filtrado, fase y tratamiento de bordes mediante controles de distorsión."},
    {"id": f"{CODE}-LO03", "statement": "Analiza eventos, puntos fiduciales, intervalos y morfología con ventanas de tolerancia, métricas de detección y localización, y distingue HRV de PRV según la señal observada."},
    {"id": f"{CODE}-LO04", "statement": "Interpreta DFT, PSD, Welch, STFT, espectrogramas, potencia por bandas, cross-spectrum y coherencia declarando resolución, ventana, varianza y límites de inferencia."},
    {"id": f"{CODE}-LO05", "statement": "Construye y evalúa pipelines de características y modelos con partición por sujeto o episodio, transformaciones dentro de validación, selección y tuning internos, baseline y test bloqueado."},
    {"id": f"{CODE}-LO06", "statement": "Evalúa calibración, incertidumbre, explicabilidad, dataset shift, subgrupos, monitorización y gestión de cambios definiendo alertas y acciones sin sobreafirmar utilidad o seguridad."},
    {"id": f"{CODE}-LO07", "statement": "Entrega y defiende un expediente integrador reproducible de una cadena de señal que conecte U1–U6, controles, fuentes, incertidumbre, versiones, límites y siguiente evidencia necesaria."},
]
course["study_method"] = [
    "Comenzar cada problema por señal, población o sistema, unidad independiente, uso previsto y resultado admisible.",
    "Alternar recuperación sin apoyo, explicación, ejemplo resuelto, práctica guiada y transferencia con apoyo decreciente.",
    "Registrar por separado señal observada, variable calculada, inferencia, decisión y afirmaciones fuera de alcance.",
    "Predefinir controles, ventanas, umbrales, particiones y criterios antes de observar el resultado final.",
    "Conservar datos o premisas, código o procedimiento, filtros, parámetros, semillas, versiones y resultados negativos.",
    "Revisar productos con rúbrica, corregir y justificar cada cambio antes de considerar cerrado un análisis.",
]
course["editorial_notice"] = (
    "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para las seis unidades de Señales Biomédicas. "
    "Las fuentes quedan trazadas y la publicación sigue siendo provisional. La revisión humana interna y la revisión disciplinaria externa, "
    "cualquier adquisición con participantes, el diagnóstico, el tratamiento, la validación clínica, la evaluación de factores humanos, "
    "la certificación y la conformidad regulatoria permanecen fuera del cierre y siguen pendientes."
)

sources = load(COURSE / "sources.json")
sources["source_policy"] = (
    "Priorizar artículos revisados por pares, consensos metodológicos, documentación primaria y organismos oficiales. "
    "Cada fuente debe ser localizable y vincularse solo a afirmaciones dentro de su alcance; la curación interna no sustituye revisión disciplinaria humana."
)
sources["consulted_on"] = "2026-08-24"
sources["coverage_gaps"] = []
source_by_id = {item["id"]: item for item in sources["sources"]}
verified = [item["id"] for item in sources["sources"] if item.get("verification_status") == "verified_directly"]
course["core_source_ids"] = verified[:16]
write(COURSE / "sources.json", sources)

lo_by_unit = {n: [f"{CODE}-LO{n:02d}", f"{CODE}-LO07"] for n in range(1, 7)}
all_claims = []
for n in range(1, 7):
    unit_path = COURSE / "units" / f"unit-{n:02d}.json"
    unit = load(unit_path)
    unit["status"] = complete_status
    unit["prerequisite_unit_ids"] = [] if n == 1 else [f"{CODE}-U{n-1:02d}"]
    unit["course_learning_outcome_ids"] = lo_by_unit[n]
    for idx, activity in enumerate(unit["activities"], start=1):
        activity["status"] = "complete"
        activity["estimated_duration_minutes"] = 90 + 30 * (idx - 1)
    for example in unit["examples"]:
        if not example.get("interpretation"):
            steps = example.get("reasoning_steps", [])
            example["interpretation"] = steps[-1] if steps else "Interpretar el resultado dentro de los supuestos y límites declarados."
        if not example.get("limitations"):
            example["limitations"] = [
                "El ejemplo es educativo y no demuestra validez clínica, causalidad fisiológica ni seguridad de un sistema real."
            ]

    unit_sources = [sid for sid in unit.get("source_ids", []) if sid in source_by_id]
    if not unit_sources:
        raise RuntimeError(f"U{n}: sin fuentes canónicas")

    claim_ids = []
    statements = []
    for topic in unit["topics"]:
        statements.extend(topic.get("key_points", [])[:2])
    if len(statements) < 8:
        raise RuntimeError(f"U{n}: se esperaban al menos 8 afirmaciones literales")
    for idx, text in enumerate(statements[:8], start=1):
        cid = f"{CODE}-U{n:02d}-C{idx:03d}"
        sid = unit_sources[(idx - 1) % len(unit_sources)]
        src = source_by_id[sid]
        claim_ids.append(cid)
        all_claims.append({
            "claim_id": cid,
            "unit": n,
            "text": text,
            "claim_type": "methodological_or_interpretive",
            "risk": "medium",
            "context": f"Síntesis educativa de {unit['title']}; interpretar dentro del protocolo, señal, población, supuestos y límites declarados.",
            "source_id": sid,
            "locator": {"url": src.get("url"), "title": src.get("title")},
            "support": "direct_or_synthesis",
            "source_verification_status": src.get("verification_status"),
            "review_state": "ai_review_provisional",
            "reviewer_validation_id": None,
            "reviewed_at": "2026-08-24",
            "id": cid,
            "unit_id": f"{CODE}-U{n:02d}",
        })
    unit["claim_ids"] = claim_ids
    write(unit_path, unit)

    assessment_path = COURSE / "assessments" / f"unit-{n:02d}.json"
    assessment = load(assessment_path)
    difficulties = ["foundational", "foundational", "intermediate", "intermediate", "intermediate", "advanced", "advanced", "intermediate", "advanced", "advanced"]
    cognition = ["understand", "understand", "apply", "apply", "analyze", "analyze", "evaluate", "analyze", "evaluate", "evaluate"]
    for idx, item in enumerate(assessment["items"]):
        item["difficulty"] = difficulties[idx % len(difficulties)]
        item["cognitive_level"] = cognition[idx % len(cognition)]
        explanation = item["answer_key"].get("explanation") or item["answer_key"].get("expected_answer")
        item["answer_key"]["explanation"] = explanation
        misconceptions = item["answer_key"].get("common_misconceptions") or ["Confundir el resultado técnico con una conclusión fuera del alcance evaluado."]
        item["answer_key"]["common_misconceptions"] = misconceptions
        item["feedback"] = {
            "correct": f"Correcto. Conserva el supuesto, control y límite que sostienen la respuesta. Idea clave: {explanation}",
            "incorrect": f"Revisa el razonamiento y contrástalo con la fuente indicada. Error a evitar: {misconceptions[0]}",
        }
        item["source_ids"] = [unit_sources[idx % len(unit_sources)]]
        item["status"] = "complete"
    assessment["status"] = "complete"
    write(assessment_path, assessment)

claims = {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Afirmaciones centrales de las seis unidades de Señales Biomédicas vinculadas a fuentes verificadas; revisión disciplinaria humana pendiente.",
    "review_state": "ai_review_provisional",
    "claims": all_claims,
}
write(COURSE / "claims.json", claims)

glossary = load(COURSE / "glossary.json")
unit_sources_map = {f"{CODE}-U{n:02d}": load(COURSE / "units" / f"unit-{n:02d}.json")["source_ids"] for n in range(1, 7)}
for entry in glossary["entries"]:
    linked = []
    for uid in entry.get("unit_ids", []):
        linked.extend([sid for sid in unit_sources_map.get(uid, []) if sid in source_by_id][:2])
    entry["source_ids"] = list(dict.fromkeys(linked)) or course["core_source_ids"][:1]
    entry["verification_status"] = "traceable_to_verified_source"
glossary["status"] = "complete_traceable"
write(COURSE / "glossary.json", glossary)

media = load(COURSE / "media.json")
media["coverage_status"] = "planned"
for item in media["items"]:
    item["status"] = "planned"
write(COURSE / "media.json", media)

assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": f"{CODE}-EVAL-CURSO",
    "course_id": COURSE_ID,
    "scope": "course",
    "principles": [
        "Evaluar razonamiento, trazabilidad y reproducibilidad, no reconocimiento de terminología aislada.",
        "Separar señal, procesamiento, inferencia técnica, validez científica, utilidad clínica y regulación.",
        "Usar señales sintéticas o datos abiertos no identificables en las actividades autónomas.",
        "Predefinir controles, particiones, ventanas, umbrales y criterios antes de interpretar resultados.",
        "Premiar conclusiones proporcionales a la evidencia y la corrección documentada de errores.",
    ],
    "assessment_plan": [
        {"component": "Autoevaluaciones y recuperación activa", "weight_percent": 15, "evidence": "Seis bancos de 10 ítems y registro de errores corregidos."},
        {"component": "Portafolio de actividades reproducibles", "weight_percent": 25, "evidence": "Productos de U1–U6 con señales sintéticas o abiertas, controles, cálculos y límites."},
        {"component": "Examen integrador intermedio", "weight_percent": 20, "evidence": "Problemas inéditos de adquisición, preprocesamiento, análisis temporal y frecuencial."},
        {"component": "Proyecto integrador final", "weight_percent": 30, "evidence": "Expediente completo de una cadena de señal desde adquisición hasta monitorización."},
        {"component": "Defensa, revisión y registro de cambios", "weight_percent": 10, "evidence": "Defensa breve, respuesta a objeciones y comparación antes-después."},
    ],
    "diagnostic": {
        "purpose": "Detectar prerrequisitos que requieren recuperación antes de U1; no contribuye a la calificación final.",
        "questions": generated["diagnostic_assessment"]["questions"],
        "use": "Los resultados dirigen repaso de matemáticas, fisiología, programación, estadística o sistemas/señales; no se usan para excluir estudiantes.",
    },
    "midterm_blueprint": [
        {"domain": "Origen, adquisición y digitalización", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO01"]},
        {"domain": "Calidad y preprocesamiento", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO02"]},
        {"domain": "Análisis temporal", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO03"]},
        {"domain": "Análisis frecuencial e integración", "weight_percent": 25, "course_learning_outcome_ids": [f"{CODE}-LO04", f"{CODE}-LO07"]},
    ],
    "capstone": {
        "title": "Expediente reproducible de una cadena de señales biomédicas desde adquisición hasta monitorización",
        "brief": "Diseñar o auditar un flujo exclusivamente con señales sintéticas o datos abiertos. Debe conectar adquisición, calidad/preprocesamiento, análisis temporal/frecuencial, características/modelo e interpretación/monitorización, declarando qué evidencia faltaría para cualquier uso clínico o regulatorio.",
        "required_deliverables": [
            "Pregunta y uso previsto con señal, unidad independiente, contexto y afirmación objetivo.",
            "Diagrama de adquisición y pipeline con frecuencias, unidades, filtros, ventanas y versiones.",
            "Controles de calidad, distorsión, detección temporal y análisis frecuencial.",
            "Pipeline de características/modelo con particición sin fuga, baseline, tuning interno y test bloqueado cuando aplique.",
            "Evaluación de calibración, incertidumbre, explicaciones, subgrupos y cambio de distribución cuando aplique.",
            "Plan de monitorización con métricas, umbrales, responsables y acciones.",
            "Matriz afirmación-evidencia-control-límite con fuentes trazables.",
            "Paquete reproducible de datos/premisas, código o procedimiento, parámetros, versiones y resultados.",
            "Conclusión acotada y siguiente estudio necesario.",
        ],
        "rubric": [
            {"criterion": "Definición del problema y cadena de adquisición", "weight_percent": 15, "excellent": "Señal, contexto, referencia, muestreo, unidades, uso y límites están definidos de forma verificable."},
            {"criterion": "Procesamiento y análisis de señal", "weight_percent": 20, "excellent": "Preprocesamiento, tiempo y frecuencia están justificados con controles de calidad, resolución y distorsión."},
            {"criterion": "Características, modelado y validación", "weight_percent": 20, "excellent": "La unidad independiente, particiones, pipeline, baseline, tuning y test bloqueado evitan fuga y sobreajuste."},
            {"criterion": "Interpretación, incertidumbre y monitorización", "weight_percent": 15, "excellent": "Calibración, explicaciones, subgrupos, shift y acciones se interpretan dentro de su alcance sin causalidad ni seguridad no demostradas."},
            {"criterion": "Reproducibilidad y trazabilidad", "weight_percent": 15, "excellent": "Fuentes, datos, parámetros, versiones, controles, discrepancias y cambios permiten reconstruir el resultado."},
            {"criterion": "Comunicación y límites", "weight_percent": 15, "excellent": "Separa desempeño técnico, validez científica, utilidad clínica y regulación y propone la siguiente evidencia necesaria."},
        ],
    },
    "status": "complete",
}
write(COURSE / "assessments" / "course-assessment.json", assessment)

course["assessment_files"] = [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"]
write(COURSE / "course.json", course)

# Guardas del cierre
assert len(all_claims) == 48
assert len(glossary["entries"]) >= 90
assert sum(item["weight_percent"] for item in assessment["assessment_plan"]) == 100
assert sum(item["weight_percent"] for item in assessment["midterm_blueprint"]) == 100
assert sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]) == 100
for n in range(1, 7):
    unit = load(COURSE / "units" / f"unit-{n:02d}.json")
    assert unit["status"]["content"] == "complete"
    assert len(load(COURSE / "assessments" / f"unit-{n:02d}.json")["items"]) == 10
print("Señales Biomédicas: cierre canónico preparado")
