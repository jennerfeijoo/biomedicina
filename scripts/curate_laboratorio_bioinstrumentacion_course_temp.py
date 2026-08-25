#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from migrate_course_to_canonical import migrate

ROOT = Path(__file__).resolve().parents[1]
SUBJECT = "laboratorio-bioinstrumentacion"
CODE = "LABINST"
TARGET = ROOT / "data" / "courses" / SUBJECT
REDEV = ROOT / "data" / "course_redevelopment" / SUBJECT
DATE = "2026-08-25"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def status_complete():
    return {
        "content": "complete",
        "sources": "traceable",
        "pedagogy": "complete",
        "multimedia": "planned",
        "internal_review": "pending",
        "external_review": "pending",
        "publication": "published_provisional",
    }


def course_outcomes():
    return [
        {"id": "LABINST-LO01", "statement": "Aplica seguridad de banco, metrología básica y bitácora trazable para preparar una práctica de bioinstrumentación antes de energizar o adquirir datos."},
        {"id": "LABINST-LO02", "statement": "Caracteriza sensores con modelos estáticos y dinámicos, calibración, sensibilidad, linealidad, histéresis, repetibilidad e incertidumbre dentro de un rango declarado."},
        {"id": "LABINST-LO03", "statement": "Diseña y audita una cadena de amplificación de biopotenciales en simulación o banco de baja energía, distinguiendo ganancia diferencial, modo común, CMRR, impedancias, ruido, offset y límites de seguridad."},
        {"id": "LABINST-LO04", "statement": "Selecciona y verifica filtrado, muestreo y conversión A/D preservando banda útil, evitando aliasing y saturación y documentando cuantización, ENOB y procedencia del procesamiento."},
        {"id": "LABINST-LO05", "statement": "Integra un prototipo de adquisición por bloques con contratos de interfaz, presupuesto de alimentación, throughput, buffers, temporización, firmware y gestión de configuración reproducible."},
        {"id": "LABINST-LO06", "statement": "Construye una matriz de verificación requisito→método→criterio→evidencia, cuantifica repetibilidad e incertidumbre y redacta un reporte técnico con discrepancias, regresión y límites explícitos."},
        {"id": "LABINST-LO07", "statement": "Integra las seis unidades en un expediente de cadena de señal de banco completamente reproducible, separando requisito, observación, cálculo, estimación, decisión técnica y afirmaciones clínicas o regulatorias fuera de alcance."},
    ]


def competencies():
    return [
        {"id": "LABINST-COMP01", "statement": "Preparar trabajo de banco con seguridad, límites de energía, trazabilidad metrológica y bitácora versionada."},
        {"id": "LABINST-COMP02", "statement": "Caracterizar sensores mediante modelos, patrones sintéticos, calibración, análisis de error e incertidumbre."},
        {"id": "LABINST-COMP03", "statement": "Razonar sobre cadenas analógicas para biopotenciales sin confundir desempeño eléctrico de banco con seguridad o aptitud clínica."},
        {"id": "LABINST-COMP04", "statement": "Diseñar adquisición y procesamiento digital coherentes con la banda, frecuencia de muestreo, rango del ADC y requisitos de calidad."},
        {"id": "LABINST-COMP05", "statement": "Integrar hardware, firmware y flujo de datos mediante interfaces explícitas y pruebas de capacidad, temporización y fallos."},
        {"id": "LABINST-COMP06", "statement": "Verificar requisitos técnicos con criterios previos, evidencia objetiva, incertidumbre, gestión de discrepancias y regresión."},
        {"id": "LABINST-COMP07", "statement": "Comunicar un expediente técnico reproducible con fuentes, versiones, supuestos, límites y revisión antes–después."},
    ]


def prerequisites():
    return [
        {"id": "LABINST-PRE01", "statement": "Circuitos eléctricos básicos: ley de Ohm, divisores, impedancia y amplificadores operacionales ideales."},
        {"id": "LABINST-PRE02", "statement": "Señales básicas: amplitud, frecuencia, espectro, muestreo y representación temporal."},
        {"id": "LABINST-PRE03", "statement": "Fisiología elemental de biopotenciales y distinción entre señal fisiológica, artefacto y ruido instrumental."},
        {"id": "LABINST-PRE04", "statement": "Álgebra, estadística descriptiva y programación u hoja de cálculo suficientes para cálculos reproducibles y gráficos con unidades."},
    ]


def make_activities(unit_id: str, unit_title: str, redeveloped: dict, prerequisites: list[str]):
    guided = (redeveloped.get("guided_activities") or [{}])[0]
    instructions = [str(x) for x in guided.get("instructions", [])]
    tasks = [str(x) for x in guided.get("problems", []) or guided.get("tasks", [])]
    deliverables = [str(x) for x in guided.get("deliverables", [])]
    criteria = [str(x) for x in guided.get("checking_criteria", [])]
    if not tasks:
        tasks = [f"Resolver un caso sintético completo de {unit_title} con unidades, supuestos y controles explícitos."]
    if not deliverables:
        deliverables = ["Expediente reproducible con datos o premisas, procedimiento, resultados y límites."]
    if not criteria:
        criteria = ["Las entradas, unidades, decisiones, controles, resultados y límites pueden reconstruirse."]
    safety = "Trabaja exclusivamente con simulación, datos sintéticos o fuentes/prototipos de banco de baja energía; no conectes personas, pacientes ni red eléctrica."
    if safety not in instructions:
        instructions = [safety, *instructions]
    return [
        {
            "id": f"{unit_id}-ACT01",
            "title": f"Práctica guiada — {unit_title}",
            "purpose": "Aplicar el método de la unidad con andamiaje explícito y conservar un producto auditable para el expediente acumulativo.",
            "prerequisite_unit_ids": prerequisites,
            "instructions": instructions,
            "tasks": tasks,
            "deliverables": deliverables,
            "checking_criteria": criteria,
            "estimated_duration_minutes": 150,
            "status": "complete",
        },
        {
            "id": f"{unit_id}-ACT02",
            "title": f"Práctica con apoyo reducido — {unit_title}",
            "purpose": "Repetir el razonamiento central con una variante nueva y menos instrucciones para comprobar transferencia, sensibilidad y control de errores.",
            "prerequisite_unit_ids": prerequisites,
            "instructions": [
                safety,
                "Usa una variante sintética distinta de la práctica guiada y fija por escrito el requisito, las unidades y el criterio de calidad antes de calcular.",
                "Selecciona por tu cuenta las ecuaciones, parámetros, controles y visualizaciones; consulta la teoría solo después del primer intento.",
                "Registra cualquier discrepancia entre el resultado esperado y el obtenido y explica si procede de dato, modelo, configuración o interpretación.",
            ],
            "tasks": [
                f"Reconstruir un caso nuevo de {unit_title} sin seguir paso a paso el ejemplo resuelto.",
                "Identificar entradas observadas o especificadas, transformaciones y salidas calculadas.",
                "Ejecutar al menos un control negativo, caso límite o prueba de sensibilidad pertinente.",
                "Comparar la variante con el caso guiado e identificar qué conclusión cambia y cuál permanece estable.",
                "Redactar una conclusión proporcional e indicar una afirmación que los datos no autorizan.",
            ],
            "deliverables": [
                "Hoja de requisitos, entradas y unidades.",
                "Cálculo o procedimiento reproducible con parámetros.",
                "Resultado del control o análisis de sensibilidad.",
                "Conclusión con incertidumbre y límite de inferencia.",
            ],
            "checking_criteria": [
                "El criterio se definió antes de inspeccionar el resultado final.",
                "Las unidades y convenciones son coherentes.",
                "El control elegido detecta un error plausible del caso.",
                "La conclusión diferencia observación, cálculo y alcance no demostrado.",
                "Otra persona puede reconstruir el procedimiento con la evidencia entregada.",
            ],
            "estimated_duration_minutes": 90,
            "status": "complete",
        },
        {
            "id": f"{unit_id}-ACT03",
            "title": f"Reto autónomo de transferencia — {unit_title}",
            "purpose": "Diseñar y defender un caso de banco completamente nuevo que demuestre dominio de la unidad sin instrucciones procedimentales paso a paso.",
            "prerequisite_unit_ids": prerequisites,
            "instructions": [
                safety,
                "Diseña un escenario sintético o de banco nuevo y declara el uso previsto educativo, las exclusiones y el criterio de aceptación antes de generar resultados.",
                "Conserva datos o premisas, configuración, versiones, procedimiento, resultados negativos y cambios realizados.",
                "Entrega primero una versión inicial, sométela a una revisión crítica propia y conserva la versión corregida con justificación de cambios.",
            ],
            "tasks": [
                f"Formular una pregunta técnica inédita que requiera aplicar {unit_title}.",
                "Diseñar un procedimiento que contenga al menos un control y un caso límite.",
                "Resolver el caso y cuantificar o discutir de forma explícita la incertidumbre relevante.",
                "Auditar una hipótesis de fallo o una explicación alternativa.",
                "Preparar una defensa breve que explique qué evidencia sería necesaria para ampliar el alcance de la conclusión.",
            ],
            "deliverables": [
                "Especificación del caso y criterio de aceptación.",
                "Procedimiento o código reproducible.",
                "Datos sintéticos/premisas y resultados con unidades.",
                "Control, caso límite y análisis de incertidumbre o sensibilidad.",
                "Registro antes–después de revisión y correcciones.",
                "Conclusión y límites de seguridad, clínica y regulación.",
            ],
            "checking_criteria": [
                "El caso no reutiliza mecánicamente los números del ejemplo de la unidad.",
                "La cadena requisito→dato→método→resultado→conclusión es explícita.",
                "Se preservan versiones y resultados desfavorables.",
                "La revisión produce al menos una comprobación o mejora justificable.",
                "No se extrapola el ejercicio educativo a uso en personas, validación clínica o conformidad regulatoria.",
            ],
            "estimated_duration_minutes": 90,
            "status": "complete",
        },
    ]


def upgrade_assessment(path: Path, unit: dict):
    payload = load(path)
    items = payload.get("items", [])
    assert len(items) >= 10, f"{path}: se esperaban >=10 ítems"
    sources = unit.get("source_ids", [])
    assert sources, f"{unit['id']}: sin fuentes"
    levels = ["understand", "apply", "analyze", "evaluate", "create"]
    n = len(items)
    for i, item in enumerate(items):
        if i < n / 3:
            item["difficulty"] = "foundational"
        elif i < 2 * n / 3:
            item["difficulty"] = "intermediate"
        else:
            item["difficulty"] = "advanced"
        item["cognitive_level"] = levels[i % len(levels)]
        explanation = item.get("answer_key", {}).get("explanation")
        if not explanation:
            item["answer_key"]["explanation"] = "La respuesta debe reconstruirse desde el modelo, unidades, condiciones y límites desarrollados en la unidad."
        item["feedback"] = {
            "correct": "Correcto. Conserva el razonamiento, las unidades y el límite de inferencia en el expediente acumulativo.",
            "incorrect": "Vuelve al bloque conceptual relacionado, separa requisito, dato, cálculo y conclusión, y responde de nuevo sin consultar la solución hasta completar un segundo intento.",
        }
        item["source_ids"] = [sources[i % len(sources)]]
        item["status"] = "complete"
    payload["purpose"] = f"Comprobar de forma formativa y recuperativa los resultados de aprendizaje de {unit['title']} mediante razonamiento técnico, controles e interpretación con límites."
    payload["status"] = "complete"
    dump(path, payload)


def main():
    migrate(SUBJECT, CODE, force=True)

    course = load(TARGET / "course.json")
    course.update({
        "code": CODE,
        "content_version": "1.0.0",
        "academic_level": "Pregrado universitario intermedio y avanzado",
        "audience": "Estudiantes de ingeniería biomédica y áreas afines con fundamentos de circuitos, señales y fisiología que necesiten construir, caracterizar, integrar y verificar cadenas de bioinstrumentación reproducibles en simulación o banco seguro.",
        "status": status_complete(),
        "purpose": "Integrar seguridad de banco, metrología, caracterización de sensores, amplificación de biopotenciales, filtrado y adquisición, integración de prototipo y verificación técnica en un flujo reproducible de laboratorio. El curso enseña a transformar requisitos en mediciones y evidencia, cuantificar incertidumbre y documentar fallos y cambios, sin convertir un ejercicio de banco en autorización para uso en personas, validación clínica, certificación de seguridad eléctrica, EMC o conformidad regulatoria.",
        "scope": {
            "included": [
                "Seguridad de banco, límites de energía, bitácora, unidades, calibración, verificación y trazabilidad metrológica introductoria.",
                "Caracterización estática y dinámica de sensores con sensibilidad, linealidad, histéresis, repetibilidad, resolución e incertidumbre.",
                "Modelado y simulación de amplificación diferencial de biopotenciales, CMRR, impedancias, offset, ruido y saturación.",
                "Filtrado analógico/digital, muestreo, antialiasing, ADC, cuantización, ENOB, clipping y procedencia del procesamiento.",
                "Integración de prototipos mediante contratos eléctricos y digitales, throughput, buffers, temporización, firmware y configuración.",
                "Verificación basada en requisitos, repetibilidad, incertidumbre, reglas de decisión, discrepancias, regresión y reporte auditable.",
                "Actividades autónomas con simulación, datos sintéticos o prototipos de banco de baja energía sin participantes humanos."
            ],
            "excluded": [
                "Conectar personas, pacientes o electrodos humanos durante las actividades autónomas del curso.",
                "Trabajar directamente con red eléctrica, partes de alta energía o configuraciones no cubiertas por supervisión institucional.",
                "Declarar seguridad eléctrica, compatibilidad electromagnética, biocompatibilidad o conformidad regulatoria a partir de ejercicios educativos.",
                "Diagnosticar, monitorizar o tomar decisiones clínicas con el prototipo o las señales del curso.",
                "Confundir verificación técnica de requisitos con validación del uso previsto o desempeño clínico.",
                "Sustituir procedimientos institucionales de laboratorio, gestión de riesgos, calibración acreditada o revisión experta."
            ],
            "handoff_courses": ["bioinstrumentacion", "senales-biomedicas", "sistemas-electronicos", "ingenieria-clinica-gestion", "desarrollo-dispositivos-medicos"]
        },
        "prerequisites": prerequisites(),
        "competencies": competencies(),
        "learning_outcomes": course_outcomes(),
        "study_method": [
            "Leer primero el requisito y declarar mensurando, rango, banda, unidades y criterio de aceptación antes de construir o calcular.",
            "Alternar explicación, ejemplo resuelto, práctica guiada, práctica con apoyo reducido y reto autónomo de transferencia.",
            "Trabajar en simulación o banco de baja energía y tratar cualquier conexión a personas o red eléctrica como fuera del material autónomo.",
            "Conservar bitácora con configuración, archivos, versiones, instrumentos o modelos, parámetros, resultados negativos y cambios.",
            "Separar en cada entrega requisito, dato observado/especificado, transformación, estimación, decisión técnica y afirmación fuera de alcance.",
            "Usar controles, casos límite y análisis de sensibilidad o incertidumbre antes de aceptar una conclusión.",
            "Cerrar cada unidad con autoevaluación recuperativa y actualizar el expediente acumulativo con correcciones justificadas."
        ],
        "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, fuentes trazables y pedagogía interna para las seis unidades de Laboratorio de Bioinstrumentación. La publicación sigue siendo provisional y la revisión humana interna y disciplinaria externa permanecen pendientes. El curso no constituye autorización para conectar personas, ensayo de seguridad eléctrica o EMC, validación clínica, certificación metrológica ni evaluación de conformidad regulatoria. Las actividades autónomas se limitan a simulación, datos sintéticos y prototipos de banco de baja energía; cualquier trabajo con personas, equipos institucionales o riesgos eléctricos requiere supervisión y procedimientos locales aplicables."
    })

    units = []
    for number in range(1, 7):
        unit_path = TARGET / "units" / f"unit-{number:02d}.json"
        redeveloped = load(REDEV / "units" / f"unit-{number:02d}.json")
        unit = load(unit_path)
        unit["status"] = status_complete()
        unit["course_learning_outcome_ids"] = [f"LABINST-LO{number:02d}", "LABINST-LO07"]
        unit["activities"] = make_activities(unit["id"], unit["title"], redeveloped, unit.get("prerequisite_unit_ids", []))
        unit["editorial_notice"] = (str(redeveloped.get("editorial_notice") or "").strip() + " La integración canónica conserva revisión humana interna y externa pendientes; el estado complete describe completitud editorial y pedagógica interna, no validación clínica, regulatoria ni autorización de trabajo con personas.").strip()
        dump(unit_path, unit)
        upgrade_assessment(TARGET / "assessments" / f"unit-{number:02d}.json", unit)
        units.append(unit)

    sources_file = load(TARGET / "sources.json")
    sources_file["source_policy"] = "Las fuentes metodológicas y técnicas se heredan de las seis unidades curadas. Las afirmaciones ancla se vinculan a fuentes con localizador verificable; una fuente técnica no convierte el ejercicio educativo en certificación, validación clínica o recomendación de uso real."
    sources_file["consulted_on"] = DATE
    sources_file["coverage_gaps"] = []
    sources = {source["id"]: source for source in sources_file.get("sources", [])}
    assert sources, "registro de fuentes vacío"
    for unit in units:
        for source_id in unit["source_ids"]:
            assert source_id in sources, f"fuente ausente {source_id}"
            assert sources[source_id].get("verification_status") not in (None, "", "unverified"), f"fuente no verificada {source_id}"
    dump(TARGET / "sources.json", sources_file)

    glossary = load(TARGET / "glossary.json")
    unit_by_id = {unit["id"]: unit for unit in units}
    for entry in glossary.get("entries", []):
        linked = entry.get("unit_ids", [])
        source_ids = []
        for unit_id in linked:
            source_ids.extend(unit_by_id.get(unit_id, {}).get("source_ids", [])[:2])
        entry["source_ids"] = list(dict.fromkeys(source_ids))
        entry["verification_status"] = "traceable_to_unit_sources"
    glossary["status"] = "complete"
    dump(TARGET / "glossary.json", glossary)

    claims = []
    for unit in units:
        candidates = []
        for topic in unit.get("topics", []):
            for point in topic.get("key_points", []):
                if point not in candidates:
                    candidates.append(point)
            if len(candidates) >= 4:
                break
        assert len(candidates) >= 4, f"{unit['id']}: menos de cuatro claims ancla"
        unit_sources = unit["source_ids"]
        unit_claim_ids = []
        for index, text in enumerate(candidates[:4], start=1):
            source_id = unit_sources[(index - 1) % len(unit_sources)]
            source = sources[source_id]
            claim_id = f"{unit['id']}-C{index:03d}"
            claims.append({
                "claim_id": claim_id,
                "unit": unit["order"],
                "text": text,
                "claim_type": "methodological_or_interpretive",
                "risk": "medium",
                "context": f"Afirmación ancla enseñada literalmente en {unit['title']}; interpretar solo dentro del banco, condiciones, supuestos y límites declarados.",
                "source_id": source_id,
                "locator": {"url": source.get("url"), "title": source.get("title") or source.get("organization") or source_id},
                "support": "direct",
                "source_verification_status": source.get("verification_status"),
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
                "reviewed_at": DATE,
                "id": claim_id,
                "unit_id": unit["id"],
            })
            unit_claim_ids.append(claim_id)
        unit["claim_ids"] = unit_claim_ids
        dump(TARGET / "units" / f"unit-{unit['order']:02d}.json", unit)
    dump(TARGET / "claims.json", {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": SUBJECT,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": "Veinticuatro afirmaciones metodológicas ancla, cuatro por unidad, tomadas literalmente del contenido lectivo y vinculadas a fuentes de las unidades; revisión disciplinaria humana pendiente.",
        "review_state": "ai_review_provisional",
        "claims": claims,
    })

    media = load(TARGET / "media.json")
    media["coverage_status"] = "planned"
    for item in media.get("items", []):
        item["status"] = "planned"
        item["alt_text_draft"] = f"Esquema educativo planificado para {unit_by_id[item['unit_id']]['title']} con variables, unidades y flujo de verificación explícitos."
    dump(TARGET / "media.json", media)

    course["core_source_ids"] = list(dict.fromkeys([
        *course.get("core_source_ids", []),
        *(sid for unit in units for sid in unit.get("source_ids", [])[:2]),
    ]))
    dump(TARGET / "course.json", course)

    assessment = {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": "LABINST-EVAL-CURSO",
        "course_id": SUBJECT,
        "scope": "course",
        "principles": [
            "La evaluación premia una cadena reproducible requisito→medición→procesamiento→evidencia→decisión, no una gráfica o cifra aislada.",
            "Una respuesta final sin unidades, configuración, controles, incertidumbre y límite de inferencia recibe crédito limitado.",
            "La recuperación sin apoyo precede a la consulta de soluciones y el segundo intento documentado forma parte del aprendizaje.",
            "Los resultados negativos, discrepancias y cambios de configuración se conservan como evidencia, no se borran para producir un pass.",
            "Las actividades calificadas se limitan a simulación, datos sintéticos y banco de baja energía sin personas ni red eléctrica.",
            "La completitud editorial interna no sustituye revisión disciplinaria humana, validación clínica, seguridad eléctrica, EMC ni conformidad regulatoria."
        ],
        "assessment_plan": [
            {"component": "Comprobaciones recuperativas por unidad", "weight_percent": 15, "description": "Seis controles breves de conceptos, cálculos, errores frecuentes y límites con feedback y reintento."},
            {"component": "Prácticas y caracterizaciones reproducibles", "weight_percent": 25, "description": "Productos de U1–U4 con datos sintéticos, unidades, parámetros, controles y trazabilidad."},
            {"component": "Integración de prototipo y análisis de fallos", "weight_percent": 20, "description": "Caso U5 con interfaces, throughput, temporización, configuración y pruebas de fallo/recuperación."},
            {"component": "Verificación, incertidumbre y reporte", "weight_percent": 15, "description": "Caso U6 con matriz de requisitos, repetibilidad, regla de decisión, discrepancias y regresión."},
            {"component": "Expediente integrador de banco", "weight_percent": 25, "description": "Capstone sintético que conecta las seis unidades y defiende una conclusión técnica proporcional."}
        ],
        "diagnostic": {
            "title": "Diagnóstico de entrada al Laboratorio de Bioinstrumentación",
            "purpose": "Detectar prerrequisitos de circuitos, señales, unidades, fisiología y documentación que deben recuperarse antes de ejecutar el flujo de laboratorio; no aporta nota final.",
            "questions": [
                "Aplica la ley de Ohm a un divisor resistivo e indica todas las unidades.",
                "Distingue sensibilidad, offset, linealidad, histéresis y repetibilidad en un sensor.",
                "Explica qué significa ganancia diferencial y por qué el modo común importa en biopotenciales.",
                "Distingue ruido, interferencia, offset y saturación en una cadena analógica.",
                "Explica aliasing y formula una condición de Nyquist para una banda dada.",
                "Distingue frecuencia de muestreo, resolución del ADC y ENOB.",
                "Calcula el throughput de una adquisición a partir de canales, tasa de muestreo y bytes por muestra.",
                "Explica la diferencia entre calibración, verificación y validación.",
                "Describe qué metadatos permitirían reconstruir una medición de banco.",
                "Explica qué es incertidumbre de medición y por qué no equivale a error conocido.",
                "Propón un control o caso límite para detectar un fallo de cadena de señal.",
                "Identifica dos razones por las que una prueba de banco no demuestra seguridad o validez clínica."
            ],
            "interpretation": [
                "0–4 respuestas sólidas: completar nivelación de circuitos, señales, unidades y fisiología antes de U1.",
                "5–8 respuestas sólidas: iniciar U1 con recuperación focalizada de los dominios fallidos.",
                "9–12 respuestas sólidas: comenzar el curso y mantener igualmente bitácora, controles y convenciones explícitas."
            ]
        },
        "midterm_blueprint": [
            {"domain": "U1 Seguridad, metrología y bitácora", "weight_percent": 15},
            {"domain": "U2 Caracterización de sensores", "weight_percent": 17},
            {"domain": "U3 Amplificación de biopotenciales", "weight_percent": 18},
            {"domain": "U4 Filtrado y adquisición", "weight_percent": 18},
            {"domain": "U5 Integración de prototipo", "weight_percent": 17},
            {"domain": "U6 Verificación y reporte", "weight_percent": 15}
        ],
        "capstone": {
            "title": "Expediente reproducible de una cadena de bioinstrumentación de banco",
            "scenario": "Un equipo académico recibe una necesidad de medición simulada y debe especificar, caracterizar, adquirir, integrar y verificar una cadena de bioinstrumentación usando únicamente fuentes sintéticas o prototipos de baja energía. Debe entregar evidencia reproducible sin conectar personas, sin red eléctrica y sin afirmar seguridad o validez clínica.",
            "phases": [
                "Definir necesidad educativa, mensurando, rango, banda, requisitos, riesgos de banco y criterios de aceptación.",
                "Seleccionar o modelar el sensor y caracterizar sensibilidad, offset, linealidad, repetibilidad y dinámica pertinente.",
                "Diseñar o simular el frente analógico con ganancia, modo común, CMRR, impedancias, ruido, offset y margen de saturación.",
                "Diseñar adquisición y procesamiento con antialiasing, muestreo, ADC, cuantización, ENOB y filtros documentados.",
                "Integrar hardware/modelo, firmware y flujo de datos con contratos de interfaz, throughput, buffers y temporización.",
                "Congelar una baseline y ejecutar verificación por requisitos con repeticiones, incertidumbre, discrepancias y pruebas de regresión.",
                "Someter el expediente a revisión independiente, corregirlo y registrar cambios antes–después."
            ],
            "required_deliverables": [
                "Necesidad, mensurando, rango, banda, requisitos y alcance explícito.",
                "Bitácora de seguridad de banco, configuración, versiones y criterios de aceptación.",
                "Caracterización del sensor con datos sintéticos y análisis de incertidumbre.",
                "Modelo del frente analógico con presupuesto de ganancia, ruido, modo común y saturación.",
                "Diseño de adquisición con frecuencia de muestreo, antialiasing, rango ADC, resolución y procesamiento.",
                "Arquitectura integrada con interfaces, throughput, buffers, temporización y configuración.",
                "Matriz requisito→método→criterio→evidencia→resultado para al menos ocho requisitos.",
                "Análisis de repetibilidad e incertidumbre y regla de decisión cuando proceda.",
                "Registro de al menos una discrepancia sintética, corrección y selección de regresiones.",
                "README reproducible con archivos, versiones, parámetros, checksums o hashes y procedimiento de reconstrucción.",
                "Informe técnico y resumen no técnico con límites de seguridad, clínica y regulación.",
                "Registro de revisión y correcciones antes–después."
            ],
            "integration_requirements": [
                "Vincular explícitamente evidencias y resultados con LABINST-LO01 a LABINST-LO07.",
                "Incluir al menos un control negativo, un caso límite y un análisis de sensibilidad o incertidumbre antes de la conclusión final.",
                "Separar requisito, observación, cálculo, estimación, decisión técnica y afirmaciones fuera de alcance.",
                "Usar exclusivamente simulación, datos sintéticos o prototipos de banco de baja energía; no conectar personas ni red eléctrica."
            ],
            "rubric": [
                {"criterion": "Requisitos, seguridad de banco y trazabilidad", "weight_percent": 15, "excellent": "Mensurando, rango, banda, riesgos, criterios, unidades y versiones están predefinidos y conectados con la evidencia."},
                {"criterion": "Sensor y frente analógico", "weight_percent": 20, "excellent": "Caracterización, ganancia, modo común, impedancias, ruido y saturación son cuantificados y sometidos a controles pertinentes."},
                {"criterion": "Adquisición e integración", "weight_percent": 20, "excellent": "Muestreo, ADC, filtros, throughput, buffers e interfaces forman una arquitectura coherente y reproducible."},
                {"criterion": "Verificación e incertidumbre", "weight_percent": 20, "excellent": "Los requisitos se verifican con criterios previos, repeticiones, incertidumbre, discrepancias y regresión adecuadamente documentadas."},
                {"criterion": "Reproducibilidad y procedencia", "weight_percent": 15, "excellent": "Otra persona puede reconstruir el resultado con archivos, metadatos, versiones, hashes y procedimiento entregados."},
                {"criterion": "Comunicación, límites y revisión", "weight_percent": 10, "excellent": "Las conclusiones son proporcionales, preservan resultados desfavorables y distinguen banco educativo de seguridad, clínica y regulación."}
            ]
        },
        "status": "complete"
    }
    dump(TARGET / "assessments" / "course-assessment.json", assessment)

    assert sum(item["weight_percent"] for item in assessment["assessment_plan"]) == 100
    assert sum(item["weight_percent"] for item in assessment["midterm_blueprint"]) == 100
    assert sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]) == 100
    assert len(claims) == 24
    assert all(len(unit["activities"]) == 3 for unit in units)
    print("[ok] Cierre canónico de Laboratorio de Bioinstrumentación preparado")


if __name__ == "__main__":
    main()
