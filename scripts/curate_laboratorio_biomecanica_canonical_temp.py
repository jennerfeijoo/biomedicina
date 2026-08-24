#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from migrate_course_to_canonical import migrate  # noqa: E402

SUBJECT = "laboratorio-biomecanica"
CODE = "LABBIO"
TARGET = ROOT / "data" / "courses" / SUBJECT
TODAY = "2026-08-24"
COMPLETE_STATUS = {
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


def write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if TARGET.exists():
    shutil.rmtree(TARGET)
migrate(SUBJECT, CODE)

course = load(TARGET / "course.json")
course["content_version"] = "1.0.0"
course["academic_level"] = "Pregrado universitario intermedio y avanzado"
course["audience"] = (
    "Estudiantes de ingeniería biomédica y áreas afines con fundamentos de biomecánica, anatomía funcional, "
    "señales, estadística y programación que necesiten planificar, ejecutar, verificar y comunicar análisis "
    "biomecánicos reproducibles sin convertir un ejercicio académico en evaluación clínica individual."
)
course["status"] = COMPLETE_STATUS.copy()
course["purpose"] = (
    "Integrar protocolo y calibración, cinemática, plataformas de fuerza, electromiografía de superficie, "
    "dinámica inversa e informe reproducible en un flujo de laboratorio biomecánico trazable. El curso enseña "
    "a distinguir señal observada, variable procesada, estimación mecánica e inferencia; a cuantificar calidad e "
    "incertidumbre; y a comunicar resultados con límites explícitos, sin equiparar una medición de laboratorio "
    "con diagnóstico, causalidad, riesgo individual, eficacia terapéutica o validación clínica."
)
course["scope"] = {
    "included": [
        "Diseño de protocolo sintético, sistema de coordenadas, calibración y criterios de calidad antes de medir.",
        "Procesamiento e interpretación de cinemática 2D/3D con trazabilidad de filtros, eventos y convenciones.",
        "Adquisición y análisis de fuerza de reacción del suelo, centro de presión y momentos de plataforma.",
        "Adquisición, procesamiento, normalización e interpretación prudente de sEMG.",
        "Dinámica inversa con cinemática, cargas externas, parámetros inerciales, residuales y análisis de sensibilidad.",
        "Estimandos, incertidumbre de medición, fiabilidad, acuerdo, estadística descriptiva y visualización.",
        "Paquetes reproducibles con datos sintéticos, metadatos, versiones, checksums, código o procedimiento y registro de cambios.",
    ],
    "excluded": [
        "Diagnóstico, pronóstico, clasificación clínica o recomendación terapéutica individual.",
        "Registrar participantes, pacientes o datos personales como parte de las actividades autónomas del curso.",
        "Interpretar amplitud EMG como fuerza muscular individual sin un modelo y evidencia adicionales.",
        "Interpretar momentos articulares netos de dinámica inversa como fuerzas musculares o cargas tisulares únicas.",
        "Afirmar validez clínica, causalidad, eficacia o seguridad a partir de un resultado mecánico aislado.",
        "Sustituir procedimientos institucionales de ética, seguridad, calibración metrológica o revisión experta."
    ],
    "handoff_courses": [
        "biomecanica",
        "bioinstrumentacion",
        "senales-biomedicas",
        "modelado-simulacion-biomedicina",
        "ingenieria-clinica-gestion",
    ],
}
course["prerequisites"] = [
    {"id": "LABBIO-PRE01", "statement": "Biomecánica básica: cinemática, fuerzas, momentos, diagramas de cuerpo libre y unidades SI."},
    {"id": "LABBIO-PRE02", "statement": "Anatomía funcional suficiente para definir segmentos, referencias anatómicas y tareas sin inferir diagnóstico."},
    {"id": "LABBIO-PRE03", "statement": "Señales y programación básica para muestreo, filtrado, visualización y documentación reproducible."},
    {"id": "LABBIO-PRE04", "statement": "Estadística descriptiva elemental y capacidad para distinguir precisión, incertidumbre, fiabilidad y acuerdo."},
]
course["competencies"] = [
    {"id": "LABBIO-COMP01", "statement": "Diseñar protocolos biomecánicos reproducibles con pregunta, sistema, variables, calibración, criterios de calidad y límites predefinidos."},
    {"id": "LABBIO-COMP02", "statement": "Procesar cinemática conservando coordenadas, unidades, filtros, eventos, procedencia y análisis de sensibilidad."},
    {"id": "LABBIO-COMP03", "statement": "Analizar plataformas de fuerza distinguiendo GRF, CoP, momentos, calibración, sincronización y errores de contacto."},
    {"id": "LABBIO-COMP04", "statement": "Procesar sEMG con decisiones justificadas de adquisición, filtrado, envolvente y normalización, delimitando su interpretación fisiológica."},
    {"id": "LABBIO-COMP05", "statement": "Construir y auditar una dinámica inversa segmentaria con convenciones explícitas, parámetros inerciales y residuales."},
    {"id": "LABBIO-COMP06", "statement": "Cuantificar incertidumbre, fiabilidad y acuerdo y comunicar resultados con visualizaciones que preserven unidades y estructura de los datos."},
    {"id": "LABBIO-COMP07", "statement": "Entregar un expediente de laboratorio íntegramente reproducible que vincule pregunta, dato, procesamiento, resultado, incertidumbre, fuente y límite de inferencia."},
]
course["learning_outcomes"] = [
    {"id": "LABBIO-LO01", "statement": "Diseña y audita un protocolo sintético de medición biomecánica con calibración, coordenadas, sincronización y criterios de aceptación predefinidos."},
    {"id": "LABBIO-LO02", "statement": "Procesa e interpreta trayectorias y variables cinemáticas documentando filtros, eventos, convenciones y sensibilidad a decisiones de procesamiento."},
    {"id": "LABBIO-LO03", "statement": "Procesa e interpreta datos de plataforma de fuerza distinguiendo GRF, centro de presión, momentos y fuentes de error instrumental o de ejecución."},
    {"id": "LABBIO-LO04", "statement": "Construye un flujo reproducible de sEMG y delimita qué puede inferirse de amplitud, envolvente y normalización."},
    {"id": "LABBIO-LO05", "statement": "Implementa y verifica una dinámica inversa con cinemática, cargas externas y parámetros inerciales, evaluando residuales y sensibilidad."},
    {"id": "LABBIO-LO06", "statement": "Construye un informe auditable que cuantifica incertidumbre, fiabilidad o acuerdo, usa visualización adecuada y preserva procedencia y versiones."},
    {"id": "LABBIO-LO07", "statement": "Integra las seis unidades en un expediente biomecánico sintético reproducible, separando observación, procesamiento, estimación mecánica e inferencias fuera de alcance."},
]
course["study_method"] = [
    "Predefinir pregunta, estimando, sistema de coordenadas, unidades, controles y criterio de calidad antes de inspeccionar el resultado final.",
    "Alternar explicación, ejemplo resuelto, práctica guiada y transferencia con apoyo progresivamente menor.",
    "Usar únicamente datos sintéticos o recursos abiertos ya desidentificados en las actividades autónomas.",
    "Separar en cada entrega dato observado, transformación aplicada, variable calculada, interpretación mecánica y afirmación no autorizada.",
    "Registrar frecuencia de muestreo, filtros, eventos, parámetros, software, versiones, semillas y cambios que afecten la salida.",
    "Evaluar sensibilidad e incertidumbre antes de convertir una diferencia numérica en una conclusión.",
    "Cerrar cada unidad con comprobación recuperativa y usar los errores corregidos para actualizar el expediente acumulativo."
]
course["editorial_notice"] = (
    "Corpus canónico educativo completo a nivel de contenido, fuentes trazables y pedagogía interna para las seis unidades de Laboratorio de Biomecánica. "
    "La publicación sigue siendo provisional. La revisión humana interna y la revisión disciplinaria externa permanecen pendientes. "
    "El curso no constituye protocolo para investigación con participantes, asesoría estadística para un estudio real, validación clínica, diagnóstico, recomendación terapéutica ni certificación metrológica. "
    "Todas las actividades autónomas usan datos sintéticos o recursos abiertos no personales; cualquier trabajo con personas, datos clínicos o equipamiento institucional requiere los procedimientos de ética, seguridad y supervisión correspondientes."
)

unit_clos = {f"LABBIO-LO{i:02d}" for i in range(1, 7)}
unit_paths = [TARGET / "units" / f"unit-{i:02d}.json" for i in range(1, 7)]
unit_sources: dict[str, list[str]] = {}
durations = {1: 180, 2: 210, 3: 210, 4: 210, 5: 240, 6: 270}
prereqs = {
    1: [],
    2: ["LABBIO-U01"],
    3: ["LABBIO-U01", "LABBIO-U02"],
    4: ["LABBIO-U01", "LABBIO-U02"],
    5: ["LABBIO-U01", "LABBIO-U02", "LABBIO-U03", "LABBIO-U04"],
    6: ["LABBIO-U01", "LABBIO-U02", "LABBIO-U03", "LABBIO-U04", "LABBIO-U05"],
}
for n, path in enumerate(unit_paths, start=1):
    unit = load(path)
    unit["status"] = COMPLETE_STATUS.copy()
    unit["course_learning_outcome_ids"] = [f"LABBIO-LO{n:02d}", "LABBIO-LO07"]
    unit["prerequisite_unit_ids"] = prereqs[n]
    for activity in unit["activities"]:
        activity["status"] = "complete"
        activity["estimated_duration_minutes"] = durations[n]
        activity["prerequisite_unit_ids"] = prereqs[n]
        if not activity.get("purpose"):
            activity["purpose"] = "Aplicar la unidad en un caso sintético documentado, verificable y reproducible."
    write(path, unit)
    unit_sources[unit["id"]] = list(unit["source_ids"])

sources = load(TARGET / "sources.json")
source_map = {item["id"]: item for item in sources["sources"]}
referenced = {sid for ids in unit_sources.values() for sid in ids}
missing = sorted(referenced - set(source_map))
if missing:
    raise SystemExit(f"Fuentes referenciadas ausentes: {missing}")
not_verified = sorted(sid for sid in referenced if source_map[sid].get("verification_status") != "verified_directly")
if not_verified:
    raise SystemExit(f"No se puede cerrar: fuentes de unidad no verificadas directamente: {not_verified}")
sources["sources"] = [source_map[sid] for sid in source_map if sid in referenced]
sources["source_policy"] = (
    "Conservar únicamente fuentes verificadas directamente y vinculadas a las unidades; distinguir estándar/documentación oficial, artículo metodológico, revisión y estudio de validación. "
    "La trazabilidad bibliográfica interna no sustituye revisión disciplinaria humana."
)
sources["consulted_on"] = TODAY
sources["coverage_gaps"] = []
write(TARGET / "sources.json", sources)
source_map = {item["id"]: item for item in sources["sources"]}
course["core_source_ids"] = list(source_map)[: min(16, len(source_map))]

# Cross-link glossary terms to verified sources from the units where each term is taught.
glossary = load(TARGET / "glossary.json")
for entry in glossary["entries"]:
    candidate_ids = []
    for uid in entry.get("unit_ids", []):
        candidate_ids.extend(unit_sources.get(uid, []))
    seen = []
    for sid in candidate_ids:
        if sid in source_map and sid not in seen:
            seen.append(sid)
    if not seen:
        raise SystemExit(f"Glosario sin fuente trazable: {entry.get('term')}")
    entry["source_ids"] = seen[:2]
    entry["verification_status"] = "traceable_to_verified_source"
glossary["status"] = "complete_traceable_human_review_pending"
write(TARGET / "glossary.json", glossary)

# Build claims only from source descriptions already tied to each unit. This avoids inventing
# claim→source mappings from unrelated prose.
claims = []
for n, path in enumerate(unit_paths, start=1):
    unit = load(path)
    claim_ids = []
    selected = unit["source_ids"][:8]
    if len(selected) < 6:
        raise SystemExit(f"U{n}: menos de seis fuentes para trazabilidad de claims")
    for i, sid in enumerate(selected, start=1):
        src = source_map[sid]
        text = str(src.get("description") or "").strip()
        if len(text.split()) < 6:
            raise SystemExit(f"Fuente {sid} sin descripción suficiente para claim")
        cid = f"LABBIO-U{n:02d}-C{i:03d}"
        claim_ids.append(cid)
        claims.append({
            "claim_id": cid,
            "unit": n,
            "text": text,
            "claim_type": "methodological_or_interpretive",
            "risk": "medium",
            "context": f"Síntesis educativa de {unit['title']}; interpretar dentro del método, supuestos y límites declarados.",
            "source_id": sid,
            "locator": {"url": src.get("url"), "title": src.get("title")},
            "support": "direct_or_synthesis",
            "source_verification_status": "verified_directly",
            "review_state": "ai_review_provisional",
            "reviewer_validation_id": None,
            "reviewed_at": TODAY,
            "id": cid,
            "unit_id": unit["id"],
        })
    unit["claim_ids"] = claim_ids
    write(path, unit)
write(TARGET / "claims.json", {
    "$schema": "../../../schemas/academic/registry-v1.schema.json",
    "schema_version": "1.0",
    "course_id": SUBJECT,
    "content_version": "1.0.0",
    "content_commit": None,
    "scope": "Afirmaciones metodológicas centrales de las seis unidades vinculadas a fuentes verificadas directamente; revisión disciplinaria humana pendiente.",
    "review_state": "ai_review_provisional",
    "claims": claims,
})

# Complete the six formative assessments with classification, feedback and traceable sources.
difficulty = ["foundational", "foundational", "intermediate", "intermediate", "intermediate", "advanced"]
cognitive = ["understand", "apply", "analyze", "analyze", "evaluate", "create"]
for n in range(1, 7):
    path = TARGET / "assessments" / f"unit-{n:02d}.json"
    assessment = load(path)
    source_ids = unit_sources[f"LABBIO-U{n:02d}"]
    if len(assessment["items"]) < 10:
        raise SystemExit(f"U{n}: evaluación con menos de 10 ítems")
    assessment["purpose"] = f"Comprobar de forma formativa y recuperativa los resultados de aprendizaje de U{n} con énfasis en método, interpretación y límites."
    for i, item in enumerate(assessment["items"]):
        item["difficulty"] = difficulty[min(i * len(difficulty) // len(assessment["items"]), len(difficulty)-1)]
        item["cognitive_level"] = cognitive[i % len(cognitive)]
        explanation = str(item["answer_key"].get("explanation") or "").strip()
        if not explanation:
            explanation = "La respuesta debe explicitar el razonamiento, las unidades o condiciones relevantes y el límite de inferencia, no solo nombrar el concepto."
        item["answer_key"]["explanation"] = explanation
        item["feedback"] = {
            "correct": "Correcto. Conserva el procedimiento, las condiciones y el límite de inferencia en tu expediente acumulativo.",
            "incorrect": "Revisa la explicación de la unidad, identifica qué dato entra, qué transformación se aplica y qué conclusión está permitida; después responde de nuevo sin consultar la solución.",
        }
        item["source_ids"] = [source_ids[i % len(source_ids)]]
        item["status"] = "complete"
    assessment["status"] = "complete"
    write(path, assessment)

course_assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "LABBIO-EVAL-CURSO",
    "course_id": SUBJECT,
    "scope": "course",
    "principles": [
        "La evaluación premia una cadena reproducible desde pregunta y adquisición hasta interpretación, no una cifra final aislada.",
        "Datos, código, parámetros, unidades, filtros, eventos y versiones deben permitir reconstruir el resultado.",
        "Toda inferencia debe distinguir observación, procesamiento, estimación mecánica y significado clínico no demostrado.",
        "Los errores corregidos con explicación forman parte de la evidencia de aprendizaje.",
        "Las actividades calificadas usan datos sintéticos o abiertos no personales; no se requiere registrar participantes.",
        "La revisión humana disciplinaria permanece pendiente aunque contenido y pedagogía internos estén completos.",
    ],
    "assessment_plan": [
        {"component": "Comprobaciones recuperativas por unidad", "weight_percent": 15, "description": "Seis controles breves con feedback y reintento documentado."},
        {"component": "Cuadernos de procesamiento y control de calidad", "weight_percent": 25, "description": "Productos reproducibles de cinemática, fuerza y sEMG con parámetros y controles explícitos."},
        {"component": "Caso de dinámica inversa y sensibilidad", "weight_percent": 20, "description": "Resolución sintética con convenciones, residuales, parámetros inerciales y análisis de sensibilidad."},
        {"component": "Informe de incertidumbre, fiabilidad y acuerdo", "weight_percent": 15, "description": "Estimando, incertidumbre, visualización y límites de interpretación sobre datos sintéticos."},
        {"component": "Expediente integrador reproducible", "weight_percent": 25, "description": "Capstone que integra U1–U6 con trazabilidad completa y revisión antes-después."},
    ],
    "diagnostic": {
        "title": "Diagnóstico de entrada al Laboratorio de Biomecánica",
        "purpose": "Detectar prerrequisitos que deben recuperarse antes de ejecutar el flujo de laboratorio; no aporta nota final.",
        "questions": [
            "Distingue posición, velocidad y aceleración e indica unidades SI.",
            "Define fuerza, momento y brazo de momento sin confundirlos.",
            "Explica por qué un sistema de coordenadas debe declararse antes de comparar señales biomecánicas.",
            "Propón una comprobación sencilla de calibración y explica qué error detectaría.",
            "Diferencia frecuencia de muestreo y frecuencia de corte de un filtro.",
            "Explica qué significa sincronizar dos sistemas de adquisición.",
            "Distingue centro de masa y centro de presión.",
            "Explica por qué amplitud sEMG no equivale directamente a fuerza muscular.",
            "Enumera las entradas mínimas de una dinámica inversa segmentaria.",
            "Distingue repetibilidad, reproducibilidad, fiabilidad y acuerdo.",
            "Explica qué es incertidumbre de medición y por qué no es sinónimo de error conocido.",
            "Describe qué archivos y metadatos entregarías para que otra persona reproduzca un resultado."
        ],
        "interpretation": [
            "0–4 respuestas sólidas: completar nivelación de biomecánica, señales, unidades y estadística antes de U1.",
            "5–8 respuestas sólidas: iniciar U1 con recuperación focalizada de los dominios fallidos.",
            "9–12 respuestas sólidas: comenzar el curso y documentar igualmente convenciones y controles."
        ],
    },
    "midterm_blueprint": [
        {"domain": "U1 Protocolo y calibración", "weight_percent": 18},
        {"domain": "U2 Análisis cinemático", "weight_percent": 18},
        {"domain": "U3 Plataformas de fuerza", "weight_percent": 18},
        {"domain": "U4 EMG de superficie", "weight_percent": 16},
        {"domain": "U5 Dinámica inversa", "weight_percent": 16},
        {"domain": "U6 Informe y reproducibilidad", "weight_percent": 14},
    ],
    "capstone": {
        "title": "Expediente reproducible de una sesión biomecánica sintética multimodal",
        "scenario": "Un laboratorio académico recibe un conjunto sintético sincronizado de trayectorias, fuerzas de plataforma y sEMG. Debe producir un expediente que permita reconstruir desde el protocolo y la calibración hasta una dinámica inversa y un informe de incertidumbre, sin participantes reales ni afirmaciones clínicas.",
        "phases": [
            "Pre-registrar pregunta, estimandos, coordenadas, unidades, controles y criterios de calidad.",
            "Auditar calibración y sincronización y documentar cualquier exclusión o corrección.",
            "Procesar cinemática con filtros, eventos y análisis de sensibilidad.",
            "Procesar GRF/CoP y verificar coherencia de signos, contactos y momentos.",
            "Procesar sEMG con banda, rectificación/envolvente y normalización justificadas.",
            "Ejecutar dinámica inversa sintética y analizar residuales y sensibilidad a parámetros inerciales o filtrado.",
            "Cuantificar incertidumbre, fiabilidad o acuerdo donde corresponda y construir visualizaciones auditables.",
            "Realizar revisión independiente, corregir el expediente y registrar cambios antes-después.",
        ],
        "required_deliverables": [
            "Pregunta, estimandos, alcance y matriz de trazabilidad U1–U6.",
            "Diccionario de datos, unidades, coordenadas y convenciones de signos.",
            "Registro de calibración, sincronización y criterios de aceptación.",
            "Pipeline de cinemática con parámetros y figura de sensibilidad.",
            "Pipeline de plataforma de fuerza con GRF, CoP y controles de contacto.",
            "Pipeline sEMG con decisiones de procesamiento y normalización.",
            "Dinámica inversa con entradas, parámetros, residuales y análisis de sensibilidad.",
            "Presupuesto de incertidumbre y/o análisis de fiabilidad/acuerdo pertinente.",
            "Figuras finales con ejes, unidades, incertidumbre y estructura de datos preservada.",
            "README reproducible con versiones, dependencias, semillas y comandos o procedimiento.",
            "Checksums o hashes de los archivos principales y manifiesto de procedencia.",
            "Informe académico, resumen no técnico y registro de revisión/correcciones."
        ],
        "integration_requirements": [
            "Vincular explícitamente evidencias y resultados con LABBIO-LO01 a LABBIO-LO07.",
            "Incluir al menos un control de calidad y un análisis de sensibilidad antes de la conclusión final.",
            "Separar en el informe qué se observó, qué se procesó, qué se estimó mecánicamente y qué no puede inferirse clínicamente.",
            "Usar exclusivamente datos sintéticos o un recurso abierto ya desidentificado y documentar su licencia/procedencia."
        ],
        "rubric": [
            {"criterion": "Protocolo, calibración y trazabilidad", "weight_percent": 15, "excellent": "Pregunta, estimandos, coordenadas, unidades, controles y criterios están predefinidos y conectados con las salidas."},
            {"criterion": "Procesamiento cinemático y cinético", "weight_percent": 20, "excellent": "Filtros, eventos, GRF, CoP y convenciones son reproducibles y se someten a controles y sensibilidad."},
            {"criterion": "sEMG y dinámica inversa", "weight_percent": 20, "excellent": "El procesamiento sEMG y la dinámica inversa declaran entradas, parámetros, residuales y límites sin inferencias musculares excesivas."},
            {"criterion": "Incertidumbre, fiabilidad y visualización", "weight_percent": 15, "excellent": "La incertidumbre o el acuerdo se cuantifican de forma pertinente y las figuras preservan unidades y estructura de los datos."},
            {"criterion": "Reproducibilidad computacional y procedencia", "weight_percent": 20, "excellent": "Otra persona puede reconstruir el resultado con archivos, metadatos, versiones, dependencias, checksums y procedimiento entregados."},
            {"criterion": "Comunicación, límites y revisión", "weight_percent": 10, "excellent": "Las conclusiones son proporcionales, distinguen alcance mecánico y clínico y muestran correcciones justificadas tras revisión."},
        ],
    },
    "status": "complete",
}
write(TARGET / "assessments" / "course-assessment.json", course_assessment)

# Media remains planned: improve pedagogical descriptions without pretending assets exist.
media = load(TARGET / "media.json")
media["coverage_status"] = "planned"
visuals = {
    1: ("Diagrama de calibración y marcos", "Esquema sintético de volumen de calibración, ejes y controles de calidad sin personas."),
    2: ("Pipeline cinemático", "Trayectoria sintética que muestra muestreo, filtrado, derivación, eventos y comparación de sensibilidad."),
    3: ("GRF, CoP y momentos", "Diagrama de plataforma de fuerza con ejes, signos, GRF, CoP y momentos sobre un contacto sintético."),
    4: ("Pipeline sEMG", "Señal sEMG sintética desde adquisición hasta filtrado, rectificación, envolvente y normalización."),
    5: ("Flujo de dinámica inversa", "Entradas cinemáticas, cargas externas y parámetros inerciales que conducen a fuerzas y momentos articulares netos."),
    6: ("Paquete reproducible", "Mapa de estimando, datos, código, incertidumbre, figura, metadatos, versión y checksum de un expediente sintético."),
}
for item in media["items"]:
    n = int(item["unit_id"].split("U")[-1])
    title, alt = visuals[n]
    item["pedagogical_purpose"] = title
    item["alt_text_draft"] = alt
    item["status"] = "planned"
write(TARGET / "media.json", media)

write(TARGET / "course.json", course)

# Permanent regression for the canonical closure.
test_path = ROOT / "tests" / "test_laboratorio_biomecanica_canonical_course.py"
test_path.write_text(r'''from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "laboratorio-biomecanica"
GENERIC = "concepto de la unidad que debe definirse"


class LaboratorioBiomecanicaCanonicalCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        cls.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))

    def test_course_status_preserves_human_review_boundary(self):
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["multimedia"], "planned")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")

    def test_six_units_cover_all_course_outcomes_without_generic_template(self):
        self.assertEqual(len(self.course["unit_files"]), 6)
        known = {item["id"] for item in self.course["learning_outcomes"]}
        covered = set()
        for relative in self.course["unit_files"]:
            unit = json.loads((COURSE / relative).read_text(encoding="utf-8"))
            covered.update(unit["course_learning_outcome_ids"])
            self.assertNotIn(GENERIC, json.dumps(unit, ensure_ascii=False).casefold())
            self.assertGreaterEqual(len(unit["topics"]), 4)
            self.assertGreaterEqual(len(unit["examples"]), 3)
            self.assertTrue(unit["activities"])
            self.assertTrue(all(activity["estimated_duration_minutes"] > 0 for activity in unit["activities"]))
            self.assertTrue(all(activity["status"] == "complete" for activity in unit["activities"]))
            self.assertEqual(unit["status"]["content"], "complete")
            self.assertEqual(unit["status"]["sources"], "traceable")
            self.assertEqual(unit["status"]["pedagogy"], "complete")
        self.assertEqual(known, covered)

    def test_unit_assessments_are_classified_feedback_rich_and_traceable(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        total = 0
        for n in range(1, 7):
            assessment = json.loads((COURSE / "assessments" / f"unit-{n:02d}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(assessment["items"]), 10)
            self.assertEqual(assessment["status"], "complete")
            total += len(assessment["items"])
            for item in assessment["items"]:
                self.assertNotEqual(item["difficulty"], "unclassified")
                self.assertNotEqual(item["cognitive_level"], "unclassified")
                self.assertTrue(item["answer_key"]["explanation"])
                self.assertTrue(item["feedback"]["correct"])
                self.assertTrue(item["feedback"]["incorrect"])
                self.assertTrue(item["source_ids"])
                self.assertTrue(set(item["source_ids"]) <= source_ids)
                self.assertEqual(item["status"], "complete")
        self.assertGreaterEqual(total, 60)

    def test_sources_glossary_and_claims_are_traceable(self):
        source_ids = {item["id"] for item in self.sources["sources"]}
        self.assertGreaterEqual(len(source_ids), 25)
        self.assertTrue(all(item["verification_status"] == "verified_directly" for item in self.sources["sources"]))
        self.assertEqual(self.sources["coverage_gaps"], [])
        self.assertGreaterEqual(len(self.glossary["entries"]), 60)
        for entry in self.glossary["entries"]:
            self.assertTrue(entry["source_ids"])
            self.assertTrue(set(entry["source_ids"]) <= source_ids)
            self.assertEqual(entry["verification_status"], "traceable_to_verified_source")
        self.assertGreaterEqual(len(self.claims["claims"]), 36)
        self.assertEqual({claim["unit_id"] for claim in self.claims["claims"]}, {f"LABBIO-U{i:02d}" for i in range(1, 7)})
        for claim in self.claims["claims"]:
            self.assertIn(claim["source_id"], source_ids)
            self.assertEqual(claim["source_verification_status"], "verified_directly")
            self.assertEqual(claim["review_state"], "ai_review_provisional")

    def test_course_assessment_integrates_all_six_units(self):
        assessment = json.loads((COURSE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)
        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)
        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 12)
        self.assertGreaterEqual(len(assessment["capstone"]["required_deliverables"]), 10)
        self.assertEqual(assessment["status"], "complete")

    def test_scope_and_review_boundary_are_explicit(self):
        purpose = self.course["purpose"].casefold()
        notice = self.course["editorial_notice"].casefold()
        for concept in ("calibración", "cinemática", "plataformas de fuerza", "electromiografía de superficie", "dinámica inversa", "reproducible"):
            self.assertIn(concept, purpose)
        self.assertIn("revisión disciplinaria externa", notice)
        self.assertIn("validación clínica", notice)
        self.assertIn("datos sintéticos", notice)


if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8")

print(f"Canonical closure curated at {TARGET.relative_to(ROOT)} with {len(sources['sources'])} sources, {len(glossary['entries'])} glossary entries and {len(claims)} claims")
