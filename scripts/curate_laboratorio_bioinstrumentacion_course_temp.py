#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBJECT = "laboratorio-bioinstrumentacion"
CODE = "LABBIO"
TARGET = ROOT / "data" / "courses" / SUBJECT
REDEV = ROOT / "data" / "course_redevelopment" / SUBJECT / "units"
STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}
STOP = {
    "para", "como", "con", "sin", "del", "las", "los", "una", "uno", "unos", "unas", "que", "por", "sus", "entre",
    "desde", "sobre", "cada", "este", "esta", "estos", "estas", "the", "and", "for", "with", "from", "into", "using",
    "measurement", "system", "systems", "device", "devices", "method", "methods",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tokens(text: str) -> set[str]:
    words = re.findall(r"[a-záéíóúüñ0-9]+", text.casefold())
    return {word for word in words if len(word) >= 4 and word not in STOP}


def best_source(point: str, candidates: list[tuple[str, dict]]) -> tuple[str, dict]:
    point_tokens = tokens(point)
    scored = []
    for source_id, source in candidates:
        support_text = " ".join(
            [str(source.get("title") or ""), str(source.get("organization") or ""), *[str(x) for x in source.get("supports", [])]]
        )
        score = len(point_tokens & tokens(support_text))
        scored.append((score, source_id, source))
    scored.sort(key=lambda row: (-row[0], row[1]))
    return scored[0][1], scored[0][2]


def main() -> int:
    subprocess.run(
        ["python", "scripts/migrate_course_to_canonical.py", "--subject", SUBJECT, "--course-code", CODE],
        cwd=ROOT,
        check=True,
    )

    course = load(TARGET / "course.json")
    course.update(
        {
            "content_version": "1.0.0",
            "academic_level": "Pregrado universitario intermedio y avanzado",
            "audience": "Estudiantes de Ingeniería Biomédica que ya manejan fundamentos de circuitos, bioinstrumentación, señales y medición y necesitan construir, caracterizar, integrar y verificar una cadena de adquisición reproducible en un banco seguro.",
            "status": STATUS,
            "purpose": "Desarrollar competencia práctica para especificar, caracterizar, acondicionar, digitalizar, integrar y verificar una cadena de bioinstrumentación mediante bancos sintéticos o de baja energía, manteniendo trazabilidad metrológica, seguridad experimental, control de versiones, análisis de incertidumbre y límites explícitos de inferencia.",
            "scope": {
                "included": [
                    "Seguridad de banco, identificación de mensurando, trazabilidad, bitácora y criterios de aceptación.",
                    "Caracterización estática y dinámica de sensores con calibración, sensibilidad, linealidad, histéresis, repetibilidad y respuesta temporal.",
                    "Acondicionamiento de biopotenciales mediante modelos de electrodo, amplificación diferencial, CMRR, ruido, filtros y saturación en señales sintéticas.",
                    "Muestreo, cuantización, aliasing, filtrado digital, sincronización y reconstrucción de unidades en cadenas de adquisición.",
                    "Integración incremental de sensores, adquisición, firmware/software, telemetría y metadatos en una baseline reproducible.",
                    "Verificación contra requisitos, repetibilidad, incertidumbre, reglas de decisión, discrepancias, regresión y reporte auditable.",
                ],
                "excluded": [
                    "Conexión autónoma de prototipos a personas, pacientes o voluntarios.",
                    "Conexión directa a red eléctrica o ensayos de seguridad eléctrica/EMC que requieran infraestructura y supervisión especializada.",
                    "Validación clínica, diagnóstico, prescripción, certificación, conformidad regulatoria o declaración de aptitud para uso médico.",
                    "Diseño para fabricación o comercialización de un dispositivo médico.",
                ],
                "handoff_courses": [
                    "bioinstrumentacion",
                    "biosensores",
                    "senales-biomedicas",
                    "laboratorio-senales-biomedicas",
                    "desarrollo-dispositivos-medicos",
                    "ingenieria-clinica-gestion",
                ],
            },
            "prerequisites": [
                {"id": f"{CODE}-PRE01", "statement": "Manejar voltaje, corriente, impedancia, ganancia, filtros y análisis básico de circuitos."},
                {"id": f"{CODE}-PRE02", "statement": "Comprender muestreo, frecuencia, espectro, unidades y representación de señales discretas."},
                {"id": f"{CODE}-PRE03", "statement": "Aplicar conceptos básicos de sensores, calibración, incertidumbre y documentación de mediciones."},
                {"id": f"{CODE}-PRE04", "statement": "Usar Python, una hoja de cálculo u otra herramienta equivalente para analizar datos y conservar un procedimiento reproducible."},
                {"id": f"{CODE}-PRE05", "statement": "Reconocer límites de seguridad de un banco educativo y detener una práctica cuando la configuración real exceda el alcance autorizado."},
            ],
            "competencies": [
                {"id": f"{CODE}-COMP01", "statement": "Traducir una necesidad de medición en mensurando, rango, banda, unidades, arquitectura de cadena y criterios verificables."},
                {"id": f"{CODE}-COMP02", "statement": "Caracterizar sensores y etapas de acondicionamiento separando datos crudos, transformaciones, incertidumbre y conclusiones."},
                {"id": f"{CODE}-COMP03", "statement": "Diseñar y analizar una cadena de biopotenciales sintéticos con amplificación diferencial, rechazo de modo común, filtrado y control de saturación."},
                {"id": f"{CODE}-COMP04", "statement": "Seleccionar parámetros de adquisición digital y procesamiento justificando muestreo, resolución, filtros, sincronización y reconstrucción de escala."},
                {"id": f"{CODE}-COMP05", "statement": "Integrar subsistemas de forma incremental con contratos de interfaz, pruebas por etapa, metadatos, versiones y manejo explícito de fallos."},
                {"id": f"{CODE}-COMP06", "statement": "Verificar una baseline contra requisitos mediante procedimientos predefinidos, repetibilidad, incertidumbre, reglas de decisión, discrepancias y regresión."},
                {"id": f"{CODE}-COMP07", "statement": "Comunicar evidencia experimental de forma reproducible y proporcional sin convertir desempeño técnico de banco en validación clínica, regulatoria o de seguridad."},
            ],
            "learning_outcomes": [
                {"id": f"{CODE}-LO01", "statement": "Construir un plan de medición seguro y trazable con mensurando, arquitectura, bitácora, instrumentos, límites y criterios de aceptación explícitos."},
                {"id": f"{CODE}-LO02", "statement": "Caracterizar un sensor con modelos estáticos y dinámicos, estimando sensibilidad, linealidad, repetibilidad, histéresis, constante de tiempo e incertidumbre dentro de condiciones declaradas."},
                {"id": f"{CODE}-LO03", "statement": "Analizar y verificar una cadena sintética de biopotenciales desde la interfaz electrodo-equivalente hasta la salida acondicionada, incluyendo CMRR, ruido, filtros y saturación."},
                {"id": f"{CODE}-LO04", "statement": "Configurar y justificar una adquisición digital mediante frecuencia de muestreo, anti-aliasing, cuantización, filtrado, sincronización y reconstrucción de unidades."},
                {"id": f"{CODE}-LO05", "statement": "Integrar una baseline de instrumentación por etapas, con contratos de interfaz, telemetría, metadatos, control de versiones y pruebas de fallo reproducibles."},
                {"id": f"{CODE}-LO06", "statement": "Diseñar y ejecutar una campaña de verificación sintética que enlace requisitos con métodos, criterios, evidencia, incertidumbre, discrepancias y regresión."},
                {"id": f"{CODE}-LO07", "statement": "Defender un expediente experimental completo distinguiendo medición, cálculo, inferencia, cumplimiento técnico y afirmaciones clínicas, regulatorias o de seguridad que permanecen fuera de alcance."},
            ],
            "study_method": [
                "Antes de energizar o simular, declarar mensurando, arquitectura, límites, riesgos y criterio de parada.",
                "Trabajar con un flujo repetible: especificar → predecir → medir → comparar → explicar discrepancias → corregir → verificar de nuevo.",
                "Conservar datos crudos, unidades, calibraciones, configuración, scripts, versiones y resultados desfavorables junto con cada conclusión.",
                "Resolver primero un ejemplo guiado y después repetir el procedimiento con una variante donde disminuyan las ayudas.",
                "Separar en el cuaderno de laboratorio observación, cálculo, inferencia y decisión para localizar dónde entra cada supuesto.",
                "Usar revisión por pares y una bitácora antes-después para justificar correcciones, no para borrar evidencia que contradiga la hipótesis inicial.",
            ],
            "editorial_notice": "Corpus académico interno listo para revisión disciplinaria humana. Las prácticas autónomas se limitan a simulación, fuentes equivalentes y prototipos de baja energía dentro de un banco seguro. Este material no certifica seguridad eléctrica o EMC, no constituye validación clínica o regulatoria y no autoriza conexión a personas ni uso médico de prototipos.",
        }
    )

    # Canonical source lookup by URL and title.
    sources_path = TARGET / "sources.json"
    sources_registry = load(sources_path)
    canonical_sources = {source["id"]: source for source in sources_registry.get("sources", [])}
    by_url = {str(source.get("url") or ""): source_id for source_id, source in canonical_sources.items() if source.get("url")}
    by_title = {str(source.get("title") or "").casefold(): source_id for source_id, source in canonical_sources.items() if source.get("title")}

    all_claims = []
    source_ids_by_unit: dict[str, list[str]] = {}
    claim_ids_by_unit: dict[str, list[str]] = {}

    for number in range(1, 7):
        unit_id = f"{CODE}-U{number:02d}"
        source_unit = load(REDEV / f"unit-{number:02d}.json")
        canonical_unit_path = TARGET / "units" / f"unit-{number:02d}.json"
        unit = load(canonical_unit_path)
        unit["status"] = STATUS
        unit["prerequisite_unit_ids"] = [f"{CODE}-U{i:02d}" for i in range(1, number)]
        unit["course_learning_outcome_ids"] = [f"{CODE}-LO{number:02d}", f"{CODE}-LO07"] if number < 7 else [f"{CODE}-LO07"]
        unit["editorial_notice"] = (
            str(source_unit.get("editorial_notice") or "").strip()
            + " Revisión disciplinaria humana pendiente; las prácticas autónomas no autorizan uso con personas, certificación de seguridad, validación clínica ni conformidad regulatoria."
        ).strip()

        # Restore pedagogical duration lost by the generic bootstrap and keep status explicit.
        source_activities = source_unit.get("guided_activities") or source_unit.get("guided_activity") or []
        if isinstance(source_activities, dict):
            source_activities = [source_activities]
        for index, activity in enumerate(unit.get("activities", [])):
            original = source_activities[index] if index < len(source_activities) and isinstance(source_activities[index], dict) else {}
            duration = original.get("estimated_duration_minutes")
            if not isinstance(duration, int) or duration <= 0:
                duration = 120 if index == 0 else 150
            activity["estimated_duration_minutes"] = duration
            activity["status"] = "curated_internal_review_pending"
            activity["prerequisite_unit_ids"] = unit["prerequisite_unit_ids"]

        # Resolve unit sources back to canonical IDs.
        original_sources = source_unit.get("sources", []) if isinstance(source_unit.get("sources"), list) else []
        candidates: list[tuple[str, dict]] = []
        for original in original_sources:
            if not isinstance(original, dict):
                continue
            source_id = by_url.get(str(original.get("url") or "")) or by_title.get(str(original.get("title") or "").casefold())
            if source_id and source_id in canonical_sources:
                candidates.append((source_id, canonical_sources[source_id]))
        if not candidates:
            candidates = [(sid, canonical_sources[sid]) for sid in unit.get("source_ids", []) if sid in canonical_sources]
        source_ids_by_unit[unit_id] = [sid for sid, _ in candidates]

        # Trace central literal key points to the source whose declared supports overlap most strongly.
        claim_ids = []
        claim_counter = 0
        for section in source_unit.get("theory_sections", []):
            if not isinstance(section, dict):
                continue
            for point in (section.get("key_points") or [])[:2]:
                point = str(point).strip()
                if not point or not candidates:
                    continue
                source_id, source = best_source(point, candidates)
                claim_counter += 1
                claim_id = f"{unit_id}-C{claim_counter:03d}"
                all_claims.append(
                    {
                        "id": claim_id,
                        "claim_id": claim_id,
                        "unit": number,
                        "unit_id": unit_id,
                        "text": point,
                        "claim_type": "methodological_or_interpretive",
                        "risk": "medium",
                        "context": f"Afirmación educativa central de {unit['title']}; válida dentro de las condiciones, modelos y límites declarados en la unidad.",
                        "source_id": source_id,
                        "locator": {"section": "Fuente registrada en la unidad; emparejamiento por soporte temático declarado durante consolidación canónica."},
                        "support": "direct_or_synthesis_from_curated_unit",
                        "source_verification_status": str(source.get("verification_status") or "traceable"),
                        "review_state": "ai_review_provisional",
                        "reviewer_validation_id": None,
                        "reviewed_at": "2026-08-25",
                    }
                )
                claim_ids.append(claim_id)
        unit["claim_ids"] = claim_ids
        claim_ids_by_unit[unit_id] = claim_ids
        write(canonical_unit_path, unit)

        # Classify and enrich the unit assessment.
        assessment_path = TARGET / "assessments" / f"unit-{number:02d}.json"
        assessment = load(assessment_path)
        assessment["status"] = "curated_internal_review_pending"
        item_sources = list(dict.fromkeys(unit.get("source_ids", [])))[:4]
        cognitive_cycle = ["understand", "apply", "analyze", "evaluate"]
        for index, item in enumerate(assessment.get("items", [])):
            item["difficulty"] = "foundational" if index < 3 else "intermediate" if index < 8 else "advanced"
            item["cognitive_level"] = cognitive_cycle[index % len(cognitive_cycle)]
            item["status"] = "curated_internal_review_pending"
            item["source_ids"] = item_sources
            expected = item.get("answer_key", {}).get("expected_answer", "")
            item["feedback"] = {
                "correct": "Correcto. Conserva la distinción técnica y comprueba que tu explicación incluye condiciones, unidades o límites cuando correspondan.",
                "incorrect": f"Revisa la explicación de la unidad y reconstruye el razonamiento antes de volver a responder. Una respuesta defendible debe recuperar esta idea central: {expected}",
            }
        write(assessment_path, assessment)

    # Course-wide claim registry.
    claims = load(TARGET / "claims.json")
    claims.update(
        {
            "content_version": "1.0.0",
            "content_commit": None,
            "scope": "Afirmaciones centrales literales de U1–U6 consolidadas desde unidades ya curadas y enlazadas con fuentes declaradas en esas unidades; revisión disciplinaria humana pendiente.",
            "review_state": "ai_review_provisional",
            "claims": all_claims,
        }
    )
    write(TARGET / "claims.json", claims)

    # Make glossary traceable to the verified source set of the units where each term is used.
    glossary = load(TARGET / "glossary.json")
    for entry in glossary.get("entries", []):
        linked = []
        for unit_id in entry.get("unit_ids", []):
            linked.extend(source_ids_by_unit.get(unit_id, []))
        entry["source_ids"] = list(dict.fromkeys(linked))[:6]
        entry["verification_status"] = "traceable_to_curated_unit_sources"
    glossary["status"] = "curated_internal_review_pending"
    write(TARGET / "glossary.json", glossary)

    sources_registry["source_policy"] = "Las referencias se consolidan desde U1–U6. Se conserva el estado de verificación declarado en cada unidad y se evita elevar una fuente a revisión humana o validación externa sin evidencia documental." 
    sources_registry["consulted_on"] = "2026-08-25"
    sources_registry["coverage_gaps"] = []
    write(sources_path, sources_registry)

    media = load(TARGET / "media.json")
    media["coverage_status"] = "planned"
    for item in media.get("items", []):
        item["status"] = "planned"
        item["pedagogical_purpose"] = (
            "Diagrama o figura propia que haga visible el flujo entrada → transformación → medición → verificación de la unidad, "
            "con ejes, unidades, puntos de control y límites de seguridad cuando correspondan."
        )
    write(TARGET / "media.json", media)

    course["core_source_ids"] = list(dict.fromkeys(course.get("core_source_ids", [])))
    write(TARGET / "course.json", course)

    # Course assessment: retain the established 100% plan but make evidence, integration and rubric explicit.
    assessment = load(TARGET / "assessments" / "course-assessment.json")
    assessment.update(
        {
            "principles": [
                "La calificación se basa en evidencia reproducible: configuración, datos, procedimiento, cálculos, controles, incertidumbre y límites, no en una gráfica aislada ni en el volumen del informe.",
                "Toda práctica autónoma debe permanecer dentro del banco sintético o de baja energía definido; una configuración insegura se detiene y no se premia por producir datos.",
                "Los criterios de aceptación y las condiciones que invalidan una prueba se definen antes de observar el resultado que decidirá cumplimiento.",
                "Las unidades y la procedencia deben conservarse desde el mensurando hasta el archivo final; un número sin escala, versión o contexto recibe crédito limitado.",
                "Resultados desfavorables, saturaciones, pérdidas de datos, discrepancias y pruebas inválidas se conservan y explican; no se seleccionan únicamente ejecuciones favorables.",
                "Cumplimiento técnico de banco no equivale a seguridad eléctrica, EMC, validación clínica, eficacia, certificación o conformidad regulatoria.",
                "La retroalimentación exige una corrección documentada antes-después y una explicación de por qué la nueva versión es técnicamente más defendible.",
            ],
            "assessment_plan": [
                {"id": f"{CODE}-PLAN-01", "component": "Recuperación y explicación", "type": "formative_with_low_stakes_grade", "weight_percent": 15, "linked_learning_outcome_ids": [f"{CODE}-LO{i:02d}" for i in range(1, 7)], "evidence_files": [f"assessments/unit-{i:02d}.json" for i in range(1, 7)], "description": "Autoevaluaciones razonadas que exigen distinguir observación, cálculo, inferencia, criterio y límite.", "feedback_and_revision": "La clave se consulta después del primer intento; se registra el error principal y la corrección razonada."},
                {"id": f"{CODE}-PLAN-02", "component": "Problemas y casos", "type": "individual_problem_solving", "weight_percent": 25, "linked_learning_outcome_ids": [f"{CODE}-LO{i:02d}" for i in range(1, 7)], "description": "Problemas nuevos de calibración, ganancia, CMRR, muestreo, cuantización, integración, repetibilidad e incertidumbre con unidades y controles explícitos.", "feedback_and_revision": "Los errores de modelo, unidades, seguridad, criterios post hoc o inferencia reciben recuperación con un caso equivalente."},
                {"id": f"{CODE}-PLAN-03", "component": "Laboratorios reproducibles", "type": "performance_tasks", "weight_percent": 25, "linked_learning_outcome_ids": [f"{CODE}-LO{i:02d}" for i in range(1, 7)], "evidence_scope": "Actividades guiadas y de dominio de U1–U6.", "description": "Portafolio progresivo de banco con datos o señales sintéticas, configuración, scripts/procedimientos, controles, incertidumbre y registro de discrepancias.", "feedback_and_revision": "Cada entrega conserva una versión corregida y una nota antes-después; los datos desfavorables no se eliminan."},
                {"id": f"{CODE}-PLAN-04", "component": "Revisión por pares y bitácora", "type": "peer_review_and_process_evidence", "weight_percent": 10, "linked_learning_outcome_ids": [f"{CODE}-LO05", f"{CODE}-LO06", f"{CODE}-LO07"], "description": "Crítica técnica de trazabilidad, criterios, seguridad, reproducibilidad e inferencia sobre una entrega ajena y respuesta documentada a observaciones recibidas.", "feedback_and_revision": "Cada observación se clasifica como aceptada, parcialmente aceptada o no aceptada y se justifica con evidencia."},
                {"id": f"{CODE}-PLAN-05", "component": "Proyecto integrador", "type": "capstone_project", "weight_percent": 25, "linked_learning_outcome_ids": [f"{CODE}-LO{i:02d}" for i in range(1, 8)], "evidence_reference": "capstone", "description": "Expediente de una cadena sintética completa que integra especificación, caracterización, acondicionamiento, adquisición, integración y verificación.", "feedback_and_revision": "Protocolo y baseline preliminar se revisan antes de la campaña final; cualquier análisis añadido posteriormente se etiqueta como extensión exploratoria."},
            ],
            "diagnostic": {
                "id": f"{CODE}-DIAG-01",
                "title": "Diagnóstico de entrada al Laboratorio de Bioinstrumentación",
                "purpose": "Detectar necesidades de nivelación en circuitos, señales, metrología, seguridad y reproducibilidad. No aporta calificación sumativa.",
                "questions": [
                    "Distingue mensurando, indicación, valor medido y unidad en un ejemplo de tensión.",
                    "Calcula la ganancia de una etapa a partir de dos pares entrada-salida y explica qué información falta para hablar de linealidad.",
                    "Explica qué diferencia existe entre modo diferencial y modo común en una entrada de biopotencial.",
                    "Describe por qué una amplitud grande puede saturar una etapa aunque la señal final deseada sea pequeña.",
                    "Explica qué riesgo aparece si se muestrea una componente por encima de Nyquist sin filtrado anti-aliasing suficiente.",
                    "Distingue resolución de un ADC de exactitud global de la cadena de medición.",
                    "Enumera metadatos mínimos para reconstruir la escala física desde códigos digitales.",
                    "Propón un control de entrada cero y explica qué error detectaría.",
                    "Explica la diferencia entre repetibilidad e incertidumbre de medición.",
                    "Distingue verificación de calibración y validación.",
                    "Indica qué harías si un prototipo educativo requiere conexión a una persona para continuar una práctica autónoma.",
                    "Describe qué información debe conservarse para reproducir una corrida de adquisición una semana después."
                ],
                "interpretation": [
                    "0–4 respuestas sólidas: completar nivelación específica antes de U1.",
                    "5–8 respuestas sólidas: iniciar U1 con nivelación paralela de los dominios fallados.",
                    "9–12 respuestas sólidas: iniciar el curso y avanzar a retos de transferencia tras los ejemplos guiados."
                ],
            },
            "midterm_blueprint": [
                {"id": f"{CODE}-MID-01", "domain": "U1–U2: metrología, seguridad y caracterización de sensores", "weight_percent": 30, "evidence": "Problemas de mensurando, trazabilidad, sensibilidad, linealidad, histéresis, repetibilidad y respuesta temporal."},
                {"id": f"{CODE}-MID-02", "domain": "U3: biopotenciales y acondicionamiento", "weight_percent": 25, "evidence": "Caso de amplificación diferencial con CMRR, ruido, filtros, offset y saturación."},
                {"id": f"{CODE}-MID-03", "domain": "U4: adquisición digital", "weight_percent": 25, "evidence": "Caso de muestreo, anti-aliasing, cuantización, filtrado, sincronización y reconstrucción de unidades."},
                {"id": f"{CODE}-MID-04", "domain": "Integración metodológica", "weight_percent": 20, "evidence": "Identificación de controles, incertidumbre, metadatos y límites en una cadena parcial nueva."},
            ],
            "capstone": {
                "id": f"{CODE}-CAP-01",
                "title": "Expediente integrador de una cadena de bioinstrumentación sintética",
                "scenario": "Diseñar, integrar y verificar una cadena educativa para una señal sintética o fuente equivalente de baja energía. El producto debe ser reconstruible por otra persona y permanecer explícitamente fuera de uso humano o clínico.",
                "phases": [
                    "U1 — congelar mensurando, requisitos, límites de seguridad, instrumentos, bitácora y criterios de aceptación.",
                    "U2 — caracterizar el sensor o transductor equivalente y cuantificar desempeño estático/dinámico con incertidumbre.",
                    "U3 — diseñar y verificar el acondicionamiento del biopotencial o señal equivalente, incluyendo rechazo de modo común, ruido, filtros y saturación.",
                    "U4 — definir adquisición digital, anti-aliasing, resolución, filtrado, sincronización y reconstrucción de unidades.",
                    "U5 — integrar hardware/modelo, firmware/software, interfaces, telemetría y metadatos en una baseline versionada con pruebas de fallo.",
                    "U6 — convertir requisitos en una campaña de verificación, aplicar reglas de decisión, registrar discrepancias, ejecutar regresión y cerrar el reporte auditable."
                ],
                "deliverables": [
                    "Especificación del mensurando, arquitectura y requisitos identificados.",
                    "Bitácora de seguridad, configuración, calibraciones y versiones.",
                    "Datos crudos o señales sintéticas con diccionario, unidades y procedencia.",
                    "Análisis de caracterización, acondicionamiento y adquisición con scripts o procedimiento reproducible.",
                    "Baseline integrada con contratos de interfaz y pruebas de fallo.",
                    "Matriz requisito→método→criterio→evidencia→resultado.",
                    "Presupuesto de incertidumbre y análisis de sensibilidad para magnitudes críticas.",
                    "Registro de discrepancias, cambios y pruebas de regresión.",
                    "Informe final con resultados, limitaciones y siguiente evidencia necesaria.",
                    "Anexo antes-después de revisión por pares y correcciones."
                ],
                "integration_requirements": [
                    "Usar evidencia explícita de U1, U2, U3, U4, U5 y U6.",
                    "Incluir al menos un control negativo, un caso límite, una prueba inválida detectada y una discrepancia conservada.",
                    "Separar datos crudos, transformaciones, métricas, incertidumbre, decisión técnica y afirmaciones fuera de alcance.",
                    "No usar personas, pacientes ni conexión autónoma a red eléctrica; no presentar el producto como dispositivo médico validado."
                ],
                "rubric": [
                    {"criterion": "Especificación, seguridad y trazabilidad", "weight_percent": 20, "excellent": "Mensurando, requisitos, límites, configuración, unidades y procedencia quedan identificados y reconstruibles."},
                    {"criterion": "Caracterización y corrección técnica", "weight_percent": 20, "excellent": "Sensor, acondicionamiento y adquisición se justifican con modelos, cálculos, controles y casos límite coherentes."},
                    {"criterion": "Integración y reproducibilidad", "weight_percent": 20, "excellent": "La baseline, interfaces, versiones, datos y procedimiento permiten repetir la cadena sin decisiones ocultas."},
                    {"criterion": "Verificación, incertidumbre y regresión", "weight_percent": 25, "excellent": "Cada conclusión se vincula a criterio previo, evidencia, regla de decisión, incertidumbre y gestión explícita de discrepancias/cambios."},
                    {"criterion": "Interpretación, límites y comunicación", "weight_percent": 15, "excellent": "El informe separa desempeño técnico de seguridad, validación clínica y regulación y responde a la revisión sin exagerar alcance."}
                ]
            },
            "status": "curated_internal_review_pending",
        }
    )
    write(TARGET / "assessments" / "course-assessment.json", assessment)

    # Defensive assertions before validators.
    assert sum(item["weight_percent"] for item in assessment["assessment_plan"]) == 100
    assert sum(item["weight_percent"] for item in assessment["midterm_blueprint"]) == 100
    assert sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]) == 100
    assert all_claims, "course claims must not be empty"
    assert all(entry.get("source_ids") for entry in glossary.get("entries", [])), "glossary source mapping incomplete"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
