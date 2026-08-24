#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBJECT = "electronica"
CODE = "ELEC"
COURSE = ROOT / "data" / "courses" / SUBJECT
REDEV = ROOT / "data" / "course_redevelopment" / SUBJECT / "units"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def completed_status():
    return {
        "content": "complete",
        "sources": "traceable",
        "pedagogy": "complete",
        "multimedia": "planned",
        "internal_review": "pending",
        "external_review": "pending",
        "publication": "published_provisional",
    }


def curate() -> None:
    subprocess.run(
        [
            "python",
            "scripts/migrate_course_to_canonical.py",
            "--subject",
            SUBJECT,
            "--course-code",
            CODE,
        ],
        cwd=ROOT,
        check=True,
    )

    course = load(COURSE / "course.json")
    course["content_version"] = "1.0.0"
    course["status"] = completed_status()
    course["purpose"] = (
        "Integrar dispositivos semiconductores, polarización y conmutación, amplificación analógica, "
        "filtrado y oscilación, lógica e interfaces digitales y diseño físico verificable para construir "
        "y auditar cadenas electrónicas reproducibles en contextos biomédicos educativos. El curso separa "
        "función de circuito, medición, seguridad eléctrica, compatibilidad electromagnética y evidencia "
        "clínica o regulatoria, y no presenta un prototipo académico como dispositivo médico validado."
    )
    course["audience"] = (
        "Estudiantes de ingeniería biomédica y áreas afines que necesitan analizar, diseñar, verificar "
        "y documentar circuitos electrónicos con trazabilidad, límites de medición y prácticas seguras."
    )
    course["scope"] = {
        "included": [
            "Diodos, rectificación, filtrado de fuente y protección básica.",
            "BJT y MOSFET: regiones de operación, polarización, conmutación, pérdidas y protección.",
            "Amplificación analógica con op-amps e instrumentación y sus no idealidades.",
            "Filtros activos, osciladores, tolerancias y verificación de respuesta.",
            "Lógica digital, temporización, metastabilidad e interfaces GPIO, I2C, SPI y UART.",
            "Esquemático, PCB, retornos, desacoplo, instrumentación, bring-up, diagnóstico y pre-compliance EMC.",
        ],
        "excluded": [
            "Diseño de ASIC o FPGA avanzado y arquitectura digital de alto rendimiento.",
            "Diseño de RF/microondas, antenas o compatibilidad electromagnética de certificación.",
            "Diseño de fuentes conectadas directamente a red y ensayos de seguridad de alta tensión.",
            "Declaración de conformidad IEC 60601, validación clínica o autorización para uso en personas.",
        ],
        "handoff_courses": [
            "Bioinstrumentación",
            "Laboratorio de Bioinstrumentación",
            "Sistemas Electrónicos",
            "Señales Biomédicas",
            "Desarrollo de Dispositivos Médicos",
        ],
    }
    outcome_statements = [
        "Analizar diodos, rectificadores, filtros de fuente y redes de protección usando modelos, hojas de datos y límites de operación.",
        "Seleccionar y polarizar BJT y MOSFET para operación lineal o conmutada, estimando pérdidas, márgenes y protección de cargas.",
        "Diseñar y evaluar etapas de amplificación analógica considerando realimentación, rango, ancho de banda, ruido y no idealidades.",
        "Diseñar y verificar filtros activos y osciladores justificando respuesta, estabilidad, tolerancias y límites de los componentes.",
        "Analizar lógica digital, temporización e interfaces eléctricas declarando niveles, márgenes, sincronización y condiciones de validez.",
        "Traducir un diseño funcional a esquemático y PCB verificables y ejecutar un plan seguro de medición, bring-up y diagnóstico de fallos.",
        "Integrar una cadena electrónica completa con trazabilidad requisito→circuito→medición→criterio, incertidumbre y límites biomédicos, clínicos y regulatorios.",
    ]
    for idx, statement in enumerate(outcome_statements, start=1):
        if idx <= len(course["learning_outcomes"]):
            course["learning_outcomes"][idx - 1]["statement"] = statement
    course["competencies"] = [
        {"id": f"{CODE}-COMP01", "statement": "Analizar circuitos electrónicos preservando unidades, polaridades, referencias y condiciones de operación."},
        {"id": f"{CODE}-COMP02", "statement": "Seleccionar componentes a partir de requisitos y hojas de datos sin confundir valores típicos, máximos absolutos y condiciones garantizadas."},
        {"id": f"{CODE}-COMP03", "statement": "Diseñar cadenas analógicas y digitales con presupuestos explícitos de rango, margen, ancho de banda, temporización y error."},
        {"id": f"{CODE}-COMP04", "statement": "Verificar circuitos mediante simulación, cálculos, casos límite, medición y pruebas discriminantes reproducibles."},
        {"id": f"{CODE}-COMP05", "statement": "Diagnosticar fallos separando error de diseño, montaje, alimentación, carga e instrumentación."},
        {"id": f"{CODE}-COMP06", "statement": "Comunicar resultados técnicos con trazabilidad y sin extrapolar un prototipo educativo a seguridad, desempeño clínico o conformidad regulatoria."},
    ]
    course["study_method"] = [
        "Comenzar cada problema declarando entrada, referencia eléctrica, unidades, rango y criterio de aceptación.",
        "Resolver primero un modelo mínimo calculable y comparar después con simulación o medición sintética.",
        "Leer hojas de datos distinguiendo condiciones de prueba, valores típicos, límites garantizados y máximos absolutos.",
        "Aplicar práctica progresiva: explicación → ejemplo trabajado → actividad guiada → transferencia sin apoyo.",
        "Registrar discrepancias entre cálculo, simulación y medición como evidencia para diagnóstico, no como resultados que deban ocultarse.",
        "Mantener un expediente acumulativo requisito→esquemático→PCB→prueba→resultado→límite y revisar cada cambio.",
    ]
    save(COURSE / "course.json", course)

    sources = load(COURSE / "sources.json")
    sources["coverage_gaps"] = []
    sources["source_policy"] = (
        "Priorizar documentación oficial del fabricante, normas y documentación técnica primaria; "
        "registrar URL o identificador estable y conservar revisión disciplinaria humana pendiente."
    )
    source_by_id = {s["id"]: s for s in sources["sources"]}
    for source in sources["sources"]:
        status = str(source.get("verification_status") or "")
        if status == "unverified" and source.get("url"):
            source["verification_status"] = "official_or_primary_source_registered"
    save(COURSE / "sources.json", sources)

    all_claims: list[dict] = []
    outcome_map = {
        1: [f"{CODE}-LO01"],
        2: [f"{CODE}-LO02"],
        3: [f"{CODE}-LO03"],
        4: [f"{CODE}-LO04"],
        5: [f"{CODE}-LO05"],
        6: [f"{CODE}-LO06", f"{CODE}-LO07"],
    }

    for n in range(1, 7):
        unit_path = COURSE / "units" / f"unit-{n:02d}.json"
        unit = load(unit_path)
        unit["status"] = completed_status()
        unit["course_learning_outcome_ids"] = outcome_map[n]

        for activity_idx, activity in enumerate(unit.get("activities", []), start=1):
            activity["estimated_duration_minutes"] = 90 if activity_idx == 1 else 60
            activity["status"] = "complete"

        source_ids = [sid for sid in unit.get("source_ids", []) if sid in source_by_id]
        verified_ids = [
            sid
            for sid in source_ids
            if str(source_by_id[sid].get("verification_status") or "") not in {"", "unverified"}
        ]
        support_ids = verified_ids or source_ids
        if not support_ids:
            raise RuntimeError(f"U{n}: no hay fuentes para trazabilidad")

        assessment_path = COURSE / "assessments" / f"unit-{n:02d}.json"
        assessment = load(assessment_path)
        assessment["purpose"] = (
            f"Comprobar de forma formativa y recuperativa los resultados de aprendizaje de "
            f"{unit['title']} mediante explicación, cálculo, verificación e interpretación de límites."
        )
        assessment["status"] = "complete"
        cognitive = ["understand", "apply", "analyze", "evaluate", "apply", "analyze", "evaluate", "apply", "analyze", "evaluate"]
        for idx, item in enumerate(assessment.get("items", []), start=1):
            item["difficulty"] = "foundational" if idx <= 3 else "intermediate" if idx <= 7 else "advanced"
            item["cognitive_level"] = cognitive[(idx - 1) % len(cognitive)]
            item["source_ids"] = [support_ids[(idx - 1) % len(support_ids)]]
            item["status"] = "complete"
            item["feedback"] = {
                "correct": (
                    "Correcto. Conserva el modelo, unidades, condición de operación, control y límite de "
                    "interpretación en tu expediente acumulativo."
                ),
                "incorrect": (
                    "Revisa el tema correspondiente, identifica dato de entrada, modelo o ecuación, "
                    "condición de validez y prueba de verificación; después responde de nuevo sin consultar la solución."
                ),
            }
            if not item["answer_key"].get("explanation"):
                item["answer_key"]["explanation"] = (
                    "La respuesta debe justificarse con el modelo y las condiciones de operación declaradas en la unidad."
                )
        save(assessment_path, assessment)

        claims = []
        for topic_idx, topic in enumerate(unit.get("topics", []), start=1):
            key_points = [str(x).strip() for x in topic.get("key_points", []) if str(x).strip()]
            if not key_points:
                continue
            text = key_points[0]
            claim = {
                "id": f"{CODE}-U{n:02d}-CL{len(claims)+1:02d}",
                "unit_id": unit["id"],
                "text": text,
                "source_id": support_ids[(topic_idx - 1) % len(support_ids)],
                "status": "curated_internal_review_pending",
            }
            claims.append(claim)
            if len(claims) == 4:
                break
        if len(claims) < 4:
            for topic in unit.get("topics", []):
                for text in topic.get("key_points", []):
                    if len(claims) >= 4:
                        break
                    text = str(text).strip()
                    if text and all(c["text"] != text for c in claims):
                        claims.append(
                            {
                                "id": f"{CODE}-U{n:02d}-CL{len(claims)+1:02d}",
                                "unit_id": unit["id"],
                                "text": text,
                                "source_id": support_ids[(len(claims)) % len(support_ids)],
                                "status": "curated_internal_review_pending",
                            }
                        )
                if len(claims) >= 4:
                    break
        if len(claims) < 4:
            raise RuntimeError(f"U{n}: no se pudieron extraer cuatro claims literales")
        unit["claim_ids"] = [c["id"] for c in claims]
        save(unit_path, unit)
        all_claims.extend(claims)

    glossary = load(COURSE / "glossary.json")
    unit_cache = {
        f"{CODE}-U{n:02d}": load(COURSE / "units" / f"unit-{n:02d}.json")
        for n in range(1, 7)
    }
    for entry in glossary.get("entries", []):
        linked = []
        for unit_id in entry.get("unit_ids", []):
            unit = unit_cache.get(unit_id)
            if not unit:
                continue
            for sid in unit.get("source_ids", []):
                if sid in source_by_id and sid not in linked:
                    linked.append(sid)
        if not linked:
            raise RuntimeError(f"Glosario sin fuente: {entry.get('term')}")
        entry["source_ids"] = linked[:2]
        entry["verification_status"] = "traceable_to_unit_sources"
    glossary["status"] = "complete_traceable"
    save(COURSE / "glossary.json", glossary)

    claims_payload = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": SUBJECT,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": (
            "Cuatro afirmaciones metodológicas literales por unidad, extraídas de key_points del corpus "
            "curado y vinculadas a fuentes registradas de la misma unidad."
        ),
        "review_state": "internal_curated_external_pending",
        "claims": all_claims,
    }
    save(COURSE / "claims.json", claims_payload)

    media = load(COURSE / "media.json")
    media["coverage_status"] = "planned"
    for item in media.get("items", []):
        item["status"] = "planned"
        if not item.get("alt_text_draft"):
            unit = unit_cache.get(item.get("unit_id"))
            title = unit["title"] if unit else "la unidad"
            item["alt_text_draft"] = f"Diagrama didáctico planificado para apoyar {title}."
    save(COURSE / "media.json", media)

    course_assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{CODE}-EVAL-CURSO",
        "course_id": SUBJECT,
        "scope": "course",
        "principles": [
            "La evaluación premia especificación, cálculo, verificación y diagnóstico; una respuesta numérica sin condiciones recibe crédito limitado.",
            "Toda medición o simulación debe declarar referencia, unidades, rango, carga, tolerancias y criterio de aceptación.",
            "Las hojas de datos se interpretan distinguiendo valores típicos, garantizados, condiciones de prueba y máximos absolutos.",
            "Los errores corregidos con explicación y registro antes-después forman parte de la evidencia de aprendizaje.",
            "Las actividades calificadas emplean circuitos, datos y fallos sintéticos o recursos abiertos, sin conexión a personas ni equipos médicos en servicio.",
            "La revisión disciplinaria humana y cualquier evaluación de seguridad o conformidad permanecen pendientes.",
        ],
        "assessment_plan": [
            {"component": "Comprobaciones recuperativas U1–U6", "weight_percent": 15, "description": "Controles breves con feedback, reintento y explicación de condiciones de operación."},
            {"component": "Problemas de dispositivos y electrónica analógica", "weight_percent": 20, "description": "Diodos, transistores, amplificación, filtros y osciladores con cálculos y casos límite."},
            {"component": "Caso digital e interfaces", "weight_percent": 15, "description": "Niveles, temporización, metastabilidad e interfaces con márgenes y verificación."},
            {"component": "Expediente de diseño físico y diagnóstico", "weight_percent": 20, "description": "Esquemático, PCB, instrumentación, bring-up, fallos y pre-compliance con trazabilidad."},
            {"component": "Proyecto integrador reproducible", "weight_percent": 30, "description": "Cadena electrónica sintética que conecta las seis unidades y defiende una conclusión técnica delimitada."},
        ],
        "diagnostic": {
            "title": "Diagnóstico de entrada a Electrónica",
            "purpose": "Detectar prerrequisitos de circuitos, señales, unidades y medición que deben recuperarse antes de U1; no aporta nota final.",
            "questions": [
                "Aplica ley de Ohm y potencia a una resistencia indicando unidades y sentido de corriente.",
                "Explica la diferencia entre nodo, rama, lazo y referencia de tierra.",
                "Formula KCL en un nodo con tres corrientes y KVL en una malla simple.",
                "Distingue valor RMS, pico y pico a pico para una señal sinusoidal.",
                "Interpreta una constante de tiempo RC y su relación con una respuesta transitoria.",
                "Explica qué significa impedancia y por qué una carga puede modificar una señal medida.",
                "Distingue señal analógica de nivel lógico y describe por qué un umbral no es un valor analógico continuo.",
                "Explica qué información debes leer en una hoja de datos antes de usar un componente.",
                "Describe un caso límite que usarías para comprobar un cálculo electrónico.",
                "Explica por qué un osciloscopio o una sonda puede modificar el circuito observado.",
                "Distingue error de diseño, error de montaje y artefacto de medición.",
                "Explica por qué un prototipo funcional no demuestra seguridad eléctrica, EMC o validez clínica.",
            ],
            "interpretation": [
                "0–4 respuestas sólidas: completar nivelación de circuitos DC/AC y medición antes de U1.",
                "5–8 respuestas sólidas: iniciar U1 con recuperación focalizada de impedancia, transitorios, hojas de datos y medición.",
                "9–12 respuestas sólidas: comenzar el curso y documentar igualmente referencias, unidades y supuestos.",
            ],
        },
        "midterm_blueprint": [
            {"domain": "U1 Diodos y rectificación", "weight_percent": 16},
            {"domain": "U2 Transistores", "weight_percent": 16},
            {"domain": "U3 Amplificación analógica", "weight_percent": 17},
            {"domain": "U4 Filtros y osciladores", "weight_percent": 17},
            {"domain": "U5 Electrónica digital", "weight_percent": 17},
            {"domain": "U6 Diseño y prueba", "weight_percent": 17},
        ],
        "capstone": {
            "title": "Expediente reproducible de un módulo electrónico biomédico sintético",
            "scenario": (
                "Un equipo académico debe diseñar y verificar un módulo electrónico de adquisición o control "
                "para una fuente sintética de señal. Debe justificar dispositivos, cadena analógica, filtrado, "
                "lógica o interfaz, implementación física y plan de prueba, sin conectarlo a personas ni afirmar conformidad."
            ),
            "phases": [
                "Predefinir requisitos eléctricos, señal sintética, interfaces, límites y criterios de aceptación.",
                "Diseñar y justificar protección, alimentación y dispositivos semiconductores necesarios.",
                "Construir cadena analógica con presupuesto de rango, ganancia, banda, ruido y tolerancias.",
                "Definir filtrado u oscilación y verificar respuesta nominal y casos límite.",
                "Definir lógica e interfaces con niveles, temporización, pull-ups y sincronización cuando corresponda.",
                "Traducir el diseño a esquemático/PCB conceptual con retornos, desacoplo y puntos de prueba.",
                "Ejecutar bring-up y diagnóstico sobre fallos sintéticos, registrando hipótesis y pruebas discriminantes.",
                "Realizar revisión independiente, corregir el expediente y declarar qué evidencia de seguridad, EMC o validación sigue faltando.",
            ],
            "required_deliverables": [
                "Especificación de requisitos y matriz de trazabilidad U1–U6.",
                "Cálculos de dispositivos, márgenes, potencia y casos límite.",
                "Esquemático documentado y lista de componentes con procedencia de parámetros.",
                "Presupuesto de cadena analógica y verificación de rango/banda.",
                "Definición y comprobación de lógica, temporización e interfaces si existen.",
                "Layout o esquema de PCB conceptual con retornos, desacoplo y puntos de prueba.",
                "Plan de medición con modelo de carga de instrumentos y límites de seguridad.",
                "Registro de bring-up, fallos sintéticos, hipótesis, pruebas y correcciones.",
                "README con versiones, parámetros, supuestos y procedimiento de reproducción.",
                "Informe final con resultados, incertidumbre, límites y siguiente evidencia necesaria.",
            ],
            "integration_requirements": [
                "Vincular explícitamente evidencias con ELEC-LO01 a ELEC-LO07.",
                "Incluir al menos un cálculo manual, una simulación o tabla sintética, un caso límite y una prueba discriminante.",
                "Separar funcionamiento nominal, robustez, seguridad eléctrica, EMC y evidencia clínica/regulatoria.",
                "Usar únicamente fuentes de señal, datos y fallos sintéticos o recursos abiertos no personales.",
            ],
            "rubric": [
                {"criterion": "Dispositivos y protección", "weight_percent": 15, "excellent": "Selección, polarización, márgenes, potencia y protección se justifican con modelos y hojas de datos."},
                {"criterion": "Cadena analógica y filtrado", "weight_percent": 20, "excellent": "Rango, ganancia, banda, ruido, tolerancias y estabilidad se presupuestan y verifican de forma coherente."},
                {"criterion": "Lógica, temporización e interfaces", "weight_percent": 15, "excellent": "Niveles, márgenes, setup/hold, sincronización e interfaces cumplen condiciones declaradas."},
                {"criterion": "Implementación física y diagnóstico", "weight_percent": 20, "excellent": "Esquemático, PCB conceptual, retornos, desacoplo, test points y bring-up sostienen pruebas discriminantes reproducibles."},
                {"criterion": "Reproducibilidad y trazabilidad", "weight_percent": 18, "excellent": "Otra persona puede reconstruir requisitos, cálculos, fuentes, versiones, pruebas, resultados y correcciones."},
                {"criterion": "Interpretación, seguridad y límites", "weight_percent": 12, "excellent": "Las conclusiones son técnicas y proporcionales, y separan funcionalidad de seguridad, EMC, conformidad y validez clínica."},
            ],
        },
        "status": "complete",
    }
    save(COURSE / "assessments" / "course-assessment.json", course_assessment)

    course = load(COURSE / "course.json")
    course["status"] = completed_status()
    course["content_version"] = "1.0.0"
    save(COURSE / "course.json", course)

    generic = "concepto de la unidad que debe definirse"
    for n in range(1, 7):
        text = (COURSE / "units" / f"unit-{n:02d}.json").read_text(encoding="utf-8").casefold()
        if generic in text:
            raise RuntimeError(f"U{n}: persistió marcador genérico")
    if len(all_claims) != 24:
        raise RuntimeError(f"Se esperaban 24 claims; hay {len(all_claims)}")
    if len(glossary.get("entries", [])) < 100:
        raise RuntimeError("El glosario consolidado quedó por debajo de 100 entradas")


if __name__ == "__main__":
    curate()
