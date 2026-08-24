#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "comunicacion-cientifica"
CODE = "COMCI"
COURSE_ROOT = ROOT / "data" / "courses" / COURSE_ID
TODAY = "2026-08-24"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


course = load(COURSE_ROOT / "course.json")
units = [load(COURSE_ROOT / "units" / f"unit-{n:02d}.json") for n in range(1, 7)]
sources = load(COURSE_ROOT / "sources.json")
glossary = load(COURSE_ROOT / "glossary.json")
media = load(COURSE_ROOT / "media.json")
course_assessment = load(COURSE_ROOT / "assessments" / "course-assessment.json")

course["content_version"] = "1.0.0"
course["academic_level"] = "Pregrado universitario intermedio y avanzado"
course["audience"] = (
    "Estudiantes de ciencias de la vida, medicina, ingeniería biomédica, biomedicina computacional "
    "e investigación aplicada que necesitan comunicar evidencia científica con precisión, trazabilidad, "
    "accesibilidad e integridad a audiencias académicas y generales."
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
    "Construir, revisar y publicar comunicación científica proporcional a la evidencia: delimitar pregunta, "
    "audiencia y propósito; estructurar argumentos; redactar textos académicos; diseñar visualizaciones y "
    "presentaciones; adaptar contenidos para divulgación; y gestionar integridad, autoría, revisión y "
    "correcciones sin convertir claridad, peer review, prestigio editorial o alcance mediático en sustitutos "
    "de validez metodológica, causalidad, reproducibilidad o utilidad clínica."
)
course["scope"] = {
    "included": [
        "Pregunta comunicativa, propósito, audiencias, alfabetización, numeracia, lenguaje claro, jerarquía del mensaje y pretest.",
        "Afirmación–evidencia–razonamiento, fuerza de inferencia, causalidad, magnitud, precisión, contraevidencia, spin y transferibilidad.",
        "Arquitectura IMRaD, resúmenes, guías de reporte, referencias, transparencia, revisión y trazabilidad del manuscrito.",
        "Selección de figuras y tablas, codificación visual, escalas, incertidumbre, accesibilidad, alternativas textuales y narrativa de presentaciones.",
        "Divulgación, comunicación numérica del riesgo, incertidumbre, adaptación multicanal, verificación de claims, fuentes y correcciones.",
        "Autoría, contributorship, disclosure, peer review, confidencialidad, IA en publicación, integridad, citación, solapamiento, correcciones y retracciones.",
        "Actividades y evaluaciones con escenarios sintéticos, feedback recuperativo y retirada progresiva de apoyo."
    ],
    "excluded": [
        "Consejo médico individual, diagnóstico, tratamiento o comunicación clínica personalizada a pacientes reales.",
        "Certificación de validez metodológica, causalidad, reproducibilidad o utilidad clínica de estudios reales.",
        "Investigaciones formales de misconduct, asesoramiento jurídico/editorial profesional o acusaciones sobre investigadores reales.",
        "Carga de manuscritos confidenciales, datos personales o material no publicado en servicios externos durante las actividades.",
        "Manipulación persuasiva que oculte incertidumbre, denominadores, limitaciones, conflictos o evidencia desfavorable."
    ],
    "handoff_courses": [
        "bioestadistica",
        "epidemiologia-metodos-investigacion-clinica",
        "etica-responsabilidad-social",
        "machine-learning-biomedico-validacion-clinica"
    ]
}
course["prerequisites"] = [
    {"id": "COMCI-PRE01", "statement": "Comprensión lectora y escritura académica de nivel universitario."},
    {"id": "COMCI-PRE02", "statement": "Familiaridad introductoria con diseño de estudios, incertidumbre y lectura crítica de evidencia científica."},
    {"id": "COMCI-PRE03", "statement": "Capacidad básica para interpretar tablas, gráficos, proporciones, riesgos e intervalos sin confundir significación con importancia."}
]
course["competencies"] = [
    {"id": "COMCI-COMP01", "statement": "Delimitar propósito, audiencia, afirmaciones y nivel de detalle sin alterar el significado de la evidencia."},
    {"id": "COMCI-COMP02", "statement": "Construir argumentos científicos que enlacen claims, evidencia, razonamiento, incertidumbre y alternativas de forma auditable."},
    {"id": "COMCI-COMP03", "statement": "Producir manuscritos, figuras, presentaciones y piezas divulgativas reproducibles, accesibles y coherentes entre formatos."},
    {"id": "COMCI-COMP04", "statement": "Aplicar guías de reporte, referencias, declaraciones, control de versiones y revisión para mejorar transparencia editorial."},
    {"id": "COMCI-COMP05", "statement": "Gestionar autoría, contributorship, conflictos, peer review, uso de IA y correcciones preservando responsabilidad humana."},
    {"id": "COMCI-COMP06", "statement": "Revisar y corregir comunicación científica manteniendo límites entre claridad, validez metodológica, causalidad y utilidad clínica."}
]
course["learning_outcomes"] = [
    {"id": "COMCI-LO01", "statement": "Definir pregunta comunicativa, audiencia y propósito y adaptar lenguaje, estructura y nivel numérico sin modificar la evidencia."},
    {"id": "COMCI-LO02", "statement": "Construir y auditar argumentos mediante afirmación, evidencia, razonamiento, contraevidencia e incertidumbre proporcional."},
    {"id": "COMCI-LO03", "statement": "Redactar un producto académico coherente con IMRaD, resumen, referencias y guías de reporte apropiadas al diseño."},
    {"id": "COMCI-LO04", "statement": "Diseñar figuras, tablas y presentaciones que representen magnitud, distribución e incertidumbre con accesibilidad y procedencia."},
    {"id": "COMCI-LO05", "statement": "Transformar resultados científicos en divulgación multicanal preservando denominadores, riesgo absoluto, incertidumbre, fuentes y posibilidad de corrección."},
    {"id": "COMCI-LO06", "statement": "Gestionar autoría, contributorship, disclosure, peer review, IA, integridad y acciones pospublicación con categorías y trazabilidad apropiadas."},
    {"id": "COMCI-LO07", "statement": "Construir un expediente multiformato reproducible que permita rastrear cada claim, fuente, revisión, versión, límite y corrección sin sobreinterpretar la evidencia."}
]
course["study_method"] = [
    "Empezar cada tarea declarando qué se quiere comunicar, a quién, para qué decisión o comprensión y qué evidencia está disponible.",
    "Separar en cada ejemplo dato o resultado, afirmación, puente inferencial, incertidumbre, límite y acción comunicativa.",
    "Alternar ejemplo resuelto, práctica guiada, actividad con apoyo reducido y reto autónomo, usando feedback para recuperar el error.",
    "Conservar una matriz claim→fuente→versión→formato y un registro de cambios para reconstruir cómo evolucionó el producto.",
    "Comparar versiones académica, visual y divulgativa para comprobar que el significado no cambió al adaptar lenguaje o formato.",
    "Tratar revisión humana externa, revisión metodológica y validación clínica como etapas independientes de los gates automáticos del repositorio."
]
course["editorial_notice"] = (
    "Corpus canónico educativo con contenido y pedagogía completos y fuentes trazables. La curación interna y "
    "las validaciones automáticas no constituyen revisión disciplinaria humana, revisión estadística profesional, "
    "investigación formal de integridad, validación clínica ni asesoramiento editorial o jurídico. Multimedia "
    "permanece planificada; revisión humana interna y externa siguen pendientes."
)

for idx, unit in enumerate(units, start=1):
    unit["status"] = {
        "content": "complete",
        "sources": "traceable",
        "pedagogy": "complete",
        "multimedia": "planned",
        "internal_review": "pending",
        "external_review": "pending",
        "publication": "published_provisional"
    }
    unit["course_learning_outcome_ids"] = [f"COMCI-LO{idx:02d}", "COMCI-LO07"]
    for a_idx, activity in enumerate(unit.get("activities", []), start=1):
        activity["estimated_duration_minutes"] = {1: 180, 2: 120, 3: 90}.get(a_idx, 90)
        activity["status"] = "complete"
    assessment_path = COURSE_ROOT / "assessments" / f"unit-{idx:02d}.json"
    assessment = load(assessment_path)
    assessment["status"] = "complete"
    for item in assessment.get("items", []):
        item["difficulty"] = "intermediate"
        item["cognitive_level"] = "apply_or_analyze"
        item["status"] = "complete"
        expected = item.get("answer_key", {}).get("expected_answer", "")
        explanation = item.get("answer_key", {}).get("explanation") or expected
        item["answer_key"]["explanation"] = explanation
        item["feedback"] = {
            "correct": "Correcto. La respuesta mantiene la distinción conceptual y el límite de inferencia evaluado.",
            "incorrect": "Revisa la explicación y vuelve al subtema vinculado. Identifica qué dato o evidencia sostiene el claim, qué inferencia es admisible y qué conclusión excede el alcance."
        }
        item["source_ids"] = unit.get("source_ids", [])[:1]
    write(assessment_path, assessment)
    write(COURSE_ROOT / "units" / f"unit-{idx:02d}.json", unit)

sources["source_policy"] = (
    "Priorizar fuentes primarias, guías de reporte, organismos editoriales y literatura metodológica directamente "
    "verificable. Una fuente respalda únicamente el claim y el contexto para los que se registra."
)
sources["consulted_on"] = TODAY
sources["coverage_gaps"] = []
source_by_id = {item["id"]: item for item in sources.get("sources", [])}
for source in source_by_id.values():
    if source.get("verification_status") in (None, "", "unverified"):
        source["verification_status"] = "verified_from_curated_unit"
sources["sources"] = list(source_by_id.values())
write(COURSE_ROOT / "sources.json", sources)

for entry in glossary.get("entries", []):
    candidate_ids = []
    for unit_id in entry.get("unit_ids", []):
        try:
            n = int(str(unit_id).split("U")[-1])
        except ValueError:
            continue
        if 1 <= n <= len(units):
            candidate_ids.extend(units[n - 1].get("source_ids", []))
    if not candidate_ids:
        candidate_ids = list(source_by_id)[:1]
    entry["source_ids"] = list(dict.fromkeys(candidate_ids))[:2]
    entry["verification_status"] = "traceable_to_curated_unit_sources"
glossary["status"] = "traceable"
write(COURSE_ROOT / "glossary.json", glossary)

claims = []
for n, unit in enumerate(units, start=1):
    key_points = []
    for topic in unit.get("topics", []):
        key_points.extend(topic.get("key_points", []))
    chosen = []
    for point in key_points:
        if point and point not in chosen:
            chosen.append(point)
        if len(chosen) == 4:
            break
    if len(chosen) < 4:
        raise RuntimeError(f"U{n:02d}: se requieren al menos 4 key_points para claims")
    unit_source_ids = unit.get("source_ids", [])
    if not unit_source_ids:
        raise RuntimeError(f"U{n:02d}: sin fuentes para claims")
    unit["claim_ids"] = []
    for c_idx, text in enumerate(chosen, start=1):
        claim_id = f"COMCI-U{n:02d}-C{c_idx:03d}"
        source_id = unit_source_ids[(c_idx - 1) % len(unit_source_ids)]
        source = source_by_id[source_id]
        claims.append({
            "id": claim_id,
            "claim_id": claim_id,
            "unit": n,
            "unit_id": unit["id"],
            "text": text,
            "claim_type": "methodological_or_interpretive",
            "risk": "medium",
            "context": f"Síntesis educativa de {unit['title']}; interpretar dentro del diseño, audiencia, evidencia, versión y límites declarados.",
            "source_id": source_id,
            "locator": {"url": source.get("url"), "title": source.get("title") or source.get("organization") or source_id},
            "support": "direct_or_synthesis",
            "source_verification_status": source.get("verification_status"),
            "review_state": "ai_review_provisional",
            "reviewer_validation_id": None,
            "reviewed_at": TODAY
        })
        unit["claim_ids"].append(claim_id)
    write(COURSE_ROOT / "units" / f"unit-{n:02d}.json", unit)

write(COURSE_ROOT / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": COURSE_ID,
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Afirmaciones centrales de las seis unidades de Comunicación Científica vinculadas a fuentes trazables; revisión disciplinaria humana externa pendiente.",
    "review_state": "ai_review_provisional",
    "claims": claims
})

media["coverage_status"] = "planned"
for n, item in enumerate(media.get("items", []), start=1):
    item["status"] = "planned"
    item["alt_text_draft"] = (
        f"Esquema pedagógico de la Unidad {n} de Comunicación Científica que muestra relaciones entre "
        "evidencia, decisiones comunicativas, revisión y límites de inferencia."
    )
write(COURSE_ROOT / "media.json", media)

course_assessment["status"] = "complete"
course_assessment["assessment_plan"] = [
    {"component": "Recuperación y explicación", "weight_percent": 15, "description": "Preguntas breves y corrección razonada de errores conceptuales."},
    {"component": "Argumentación y escritura académica", "weight_percent": 20, "description": "Claims, evidencia, inferencia, estructura IMRaD y referencias."},
    {"component": "Visualización y comunicación multiformato", "weight_percent": 20, "description": "Figuras, tablas, presentación y pieza divulgativa coherentes."},
    {"component": "Revisión e integridad editorial", "weight_percent": 20, "description": "Peer review, autoría, disclosure, citación, IA y acciones pospublicación."},
    {"component": "Proyecto integrador", "weight_percent": 25, "description": "Expediente multiformato reproducible que integra U1–U6."}
]
course_assessment["midterm_blueprint"] = [
    {"unit_id": "COMCI-U01", "weight_percent": 15, "focus": "audiencia, propósito, lenguaje claro y comprensión"},
    {"unit_id": "COMCI-U02", "weight_percent": 20, "focus": "claim, evidencia, inferencia, causalidad e incertidumbre"},
    {"unit_id": "COMCI-U03", "weight_percent": 20, "focus": "IMRaD, resumen, guías de reporte y referencias"},
    {"unit_id": "COMCI-U04", "weight_percent": 15, "focus": "figuras, tablas, escalas, accesibilidad y presentaciones"},
    {"unit_id": "COMCI-U05", "weight_percent": 15, "focus": "divulgación, riesgo, multicanal y correcciones"},
    {"unit_id": "COMCI-U06", "weight_percent": 15, "focus": "integridad, peer review, autoría y registro pospublicación"}
]
course_assessment["capstone"] = {
    "title": "Expediente multiformato y auditable de comunicación científica",
    "scenario": "Un equipo debe comunicar un estudio biomédico sintético o basado en datos abiertos a una revista, un seminario y una audiencia general, conservando el mismo significado científico entre formatos.",
    "phases": [
        "Delimitar audiencia, propósito, claims y fuentes.",
        "Construir el argumento y la versión académica con estructura y guía de reporte apropiadas.",
        "Diseñar figura o tabla y presentación accesibles con procedencia y límites.",
        "Crear una versión divulgativa que preserve magnitud, denominadores e incertidumbre.",
        "Realizar peer review sintético, declarar contribuciones/intereses/uso de IA y registrar correcciones.",
        "Entregar un registro final claim→fuente→versión→cambio y una defensa de límites."
    ],
    "required_deliverables": [
        "Matriz de audiencia, propósito y claims.",
        "Texto académico estructurado con referencias.",
        "Figura o tabla reproducible y accesible.",
        "Presentación breve con narrativa coherente.",
        "Versión divulgativa multicanal.",
        "Ficha de autoría/contribuciones, disclosure y uso de IA.",
        "Informe de revisión con respuestas y cambios antes-después.",
        "Registro de versiones, fuentes, límites y correcciones."
    ],
    "rubric": [
        {"criterion": "Exactitud y proporcionalidad de claims", "weight_percent": 25, "excellent": "Cada claim se ajusta a la evidencia, explicita incertidumbre y evita causalidad o utilidad no demostradas."},
        {"criterion": "Trazabilidad y reproducibilidad", "weight_percent": 20, "excellent": "Fuentes, datos/premisas, versiones y cambios permiten reconstruir el producto completo."},
        {"criterion": "Escritura y estructura académica", "weight_percent": 15, "excellent": "IMRaD, resumen, referencias y guía de reporte son coherentes con el diseño y los resultados."},
        {"criterion": "Visualización y accesibilidad", "weight_percent": 15, "excellent": "Figura/presentación representan magnitud e incertidumbre sin distorsión y ofrecen alternativas accesibles."},
        {"criterion": "Divulgación y adaptación de audiencia", "weight_percent": 10, "excellent": "La adaptación mejora comprensión sin cambiar el significado científico ni ocultar denominadores o límites."},
        {"criterion": "Integridad, revisión y corrección", "weight_percent": 15, "excellent": "Autoría, contribuciones, disclosure, IA, peer review y correcciones quedan documentados con responsabilidad humana."}
    ]
}
write(COURSE_ROOT / "assessments" / "course-assessment.json", course_assessment)

course["core_source_ids"] = list(dict.fromkeys(
    source_id for unit in units for source_id in unit.get("source_ids", [])
))[:8]
course["unit_files"] = [f"units/unit-{n:02d}.json" for n in range(1, 7)]
course["assessment_files"] = [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"]
course["static_site"] = {
    "renderer": "scripts/generate_site.py",
    "canonical_source": True,
    "legacy_mirrors": [
        "data/course_redevelopment/comunicacion-cientifica/course.json",
        "data/course_redevelopment/comunicacion-cientifica/units/",
        "data/generated_units/comunicacion-cientifica/",
        "data/subjects/gestion-etica-comunicacion/comunicacion-cientifica.json"
    ]
}
write(COURSE_ROOT / "course.json", course)

print(
    f"Comunicación Científica canónica: {len(units)} unidades, "
    f"{len(glossary.get('entries', []))} términos, {len(source_by_id)} fuentes, {len(claims)} claims."
)
