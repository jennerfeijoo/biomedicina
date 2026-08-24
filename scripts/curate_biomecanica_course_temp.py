from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_PATH = ROOT / "data" / "course_redevelopment" / "biomecanica" / "course.json"
UNIT_DIR = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


course = load_json(COURSE_PATH)
units = [load_json(UNIT_DIR / f"unit-{index:02d}.json") for index in range(1, 7)]

assert [unit["unit"] for unit in units] == list(range(1, 7))
assert all(unit["status"] == "review" for unit in units)

course["description"] = (
    "Curso estructurado de seis unidades que integra cinemática, cinética, mecánica musculoesquelética, "
    "mecánica de tejidos, medición multimodal y aplicaciones funcionales. El énfasis está en formular "
    "preguntas biomecánicas reproducibles, conservar marcos de referencia y unidades, distinguir medición "
    "de inferencia, cuantificar incertidumbre y comunicar resultados sin convertir una salida mecánica en "
    "diagnóstico, causalidad o recomendación terapéutica no demostrada."
)
course["biomedical_connection"] = (
    "Integra análisis del movimiento, estimación de cargas, función músculo-tendón, comportamiento mecánico "
    "de tejidos y medición biomecánica para problemas de rehabilitación, ortesis/prótesis, ergonomía y "
    "modelado musculoesquelético, manteniendo explícitos los límites de inferencia clínica."
)
course["course_competencies"] = [
    "Definir sistemas biomecánicos con marcos de referencia, fronteras, variables, unidades, convenciones y uso previsto explícitos.",
    "Construir y verificar descripciones cinemáticas y balances cinéticos sin confundir movimiento observado con sus causas mecánicas.",
    "Relacionar arquitectura músculo-tendón, geometría articular y redundancia muscular con producción de fuerza y momento bajo supuestos declarados.",
    "Comparar propiedades estructurales y materiales de tejidos biológicos incorporando anisotropía, heterogeneidad y dependencia temporal.",
    "Diseñar cadenas de medición que integren captura de movimiento, plataformas de fuerza y sEMG con calibración, sincronización, procesamiento y control de calidad.",
    "Evaluar sensibilidad e incertidumbre y rastrear cómo errores de medición, parámetros y convenciones afectan variables biomecánicas derivadas.",
    "Interpretar cambios y desviaciones funcionales con métricas apropiadas al uso previsto, separando error de medición, mecanismo plausible, utilidad y causalidad.",
    "Comunicar un expediente biomecánico reproducible con datos o premisas, método, controles, resultados, limitaciones y siguiente evidencia necesaria."
]
course["learning_objectives"] = [
    "Construir una descripción cinemática reproducible con marcos de referencia, transformaciones rígidas, derivadas temporales y comparación 2D/3D.",
    "Resolver balances cinéticos mediante diagramas de cuerpo libre, Newton-Euler, momentos de fuerza y dinámica inversa con incertidumbre explícita.",
    "Explicar la mecánica músculo-tendón y la redundancia muscular sin equiparar activación, sEMG, fuerza muscular ni momento articular neto.",
    "Caracterizar hueso, cartílago y tendón mediante tensión, deformación, propiedades materiales y viscoelasticidad dentro del régimen y dirección ensayados.",
    "Integrar plataformas de fuerza, captura de movimiento y sEMG en una cadena de medición sincronizada, calibrada y auditable.",
    "Evaluar escenarios funcionales de marcha, rehabilitación, prótesis/órtesis y ergonomía usando fiabilidad, cambio detectable y límites de validez."
]
course["learning_outcomes"] = [
    "Declara y transforma marcos de referencia y produce variables cinemáticas con unidades, procesamiento y error documentados.",
    "Construye diagramas de cuerpo libre y aplica Newton-Euler para obtener fuerzas y momentos resultantes sin atribuirlos indebidamente a estructuras individuales.",
    "Analiza brazos de momento, relaciones fuerza-longitud/fuerza-velocidad y redundancia muscular para comparar soluciones musculoesqueléticas plausibles.",
    "Interpreta curvas mecánicas de hueso, cartílago y tendón distinguiendo rigidez, módulo, anisotropía, creep, relajación e histéresis.",
    "Diseña y audita una adquisición multimodal con plataforma de fuerza, captura de movimiento y sEMG, incluyendo calibración, muestreo, filtrado y sincronización.",
    "Cuantifica error de medición y cambio mínimo detectable y limita la interpretación de una diferencia funcional a la evidencia disponible.",
    "Integra sensibilidad, incertidumbre, controles y trazabilidad en un expediente reproducible que otra persona puede reconstruir.",
    "Separa resultado técnico, interpretación biomecánica, hipótesis causal, utilidad funcional y decisión clínica o regulatoria."
]
course["modules"] = [
    f"Unidad {unit['unit']}: {unit['title']}. {unit['purpose']}" for unit in units
]
course["detailed_units"] = [
    {
        "unit": unit["unit"],
        "title": unit["title"],
        "description": unit["purpose"],
        "learning_outcomes": list(unit["learning_objectives"]),
    }
    for unit in units
]

activities = []
for unit in units:
    guided = unit.get("guided_activities", [])
    assert guided, f"Unidad {unit['unit']} sin actividad guiada"
    activity = guided[0]
    deliverables = activity.get("deliverables", [])
    evidence = "; ".join(deliverables[:3])
    activities.append(
        {
            "title": f"Reto {unit['unit']}: {activity['title']}",
            "description": (
                f"Actividad reproducible de la Unidad {unit['unit']} con datos sintéticos o material abierto, "
                f"controles y límites explícitos. Evidencias principales: {evidence}."
            ),
            "type": "actividad guiada reproducible",
        }
    )
course["practical_activities"] = activities

course["assessment"] = [
    {
        "title": "Recuperación, conceptos y explicación",
        "weight": "15 %",
        "description": "Autoevaluaciones acumulativas y explicaciones breves que exigen unidades, convenciones, mecanismo y límites; los errores deben corregirse con justificación."
    },
    {
        "title": "Problemas biomecánicos y casos",
        "weight": "25 %",
        "description": "Problemas nuevos de cinemática, cinética, músculo-tendón y tejidos con procedimiento, controles, análisis de sensibilidad e interpretación proporcional."
    },
    {
        "title": "Expedientes reproducibles de medición y análisis",
        "weight": "25 %",
        "description": "Actividades con datos sintéticos o abiertos que documentan marcos, calibración, procesamiento, sincronización, parámetros, versiones y discrepancias."
    },
    {
        "title": "Revisión por pares y corrección",
        "weight": "10 %",
        "description": "Auditoría con rúbrica de un producto biomecánico, clasificación de hallazgos y entrega de una versión corregida con registro antes-después."
    },
    {
        "title": "Proyecto integrador",
        "weight": "25 %",
        "description": "Expediente que conecta las seis unidades, defiende una conclusión biomecánica limitada y especifica qué evidencia adicional sería necesaria para una decisión funcional o clínica."
    }
]

course["study_method"] = [
    "Comenzar cada problema declarando sistema, frontera, marco de referencia, unidades, tarea y uso previsto.",
    "Separar señal medida, variable derivada, salida de modelo, interpretación biomecánica y decisión fuera de alcance.",
    "Resolver primero un ejemplo trabajado, continuar con práctica guiada y retirar apoyo en un problema de transferencia.",
    "Predefinir controles de geometría, signos, unidades, calibración, sensibilidad y casos límite antes de interpretar resultados.",
    "Conservar datos o premisas, código o procedimiento, parámetros, versiones y transformaciones para que el análisis sea reproducible.",
    "Usar autoevaluación y revisión por pares para corregir errores conceptuales y de trazabilidad, no solo errores aritméticos.",
    "Cerrar cada actividad con una conclusión que indique resultado, incertidumbre, límites y siguiente evidencia necesaria."
]

course["diagnostic_assessment"] = {
    "title": "Diagnóstico de entrada a Biomecánica",
    "purpose": "Identificar prerrequisitos mecánicos, matemáticos, de medición y razonamiento; orienta nivelación y no se usa como calificación final.",
    "questions": [
        "Dibuja un marco cartesiano dextrógiro y explica qué información falta si se reporta un punto (x,y,z) sin origen, ejes ni unidades.",
        "Distingue posición, velocidad y aceleración y explica por qué derivar numéricamente puede amplificar ruido.",
        "Construye un diagrama de cuerpo libre simple e identifica qué hace que una fuerza sea externa o interna respecto del sistema elegido.",
        "Explica la diferencia entre fuerza, momento de fuerza y momento articular neto.",
        "Distingue rigidez estructural de módulo material y tensión de deformación.",
        "Explica por qué sEMG, activación neural y fuerza muscular no son magnitudes equivalentes.",
        "Distingue una medición directa de una variable derivada en una plataforma de fuerza o un sistema de captura de movimiento.",
        "Propón un control para detectar un error de signo, un error de unidades y un desfase temporal entre dos señales.",
        "Explica la diferencia entre repetibilidad, error estándar de medida y cambio mínimo detectable.",
        "Interpreta una diferencia pre/post sin asumir automáticamente causalidad ni importancia clínica.",
        "Describe cómo registrarías parámetros de filtrado, frecuencia de muestreo y versiones para reproducir un resultado.",
        "Reescribe una afirmación clínica exagerada para limitarla a la evidencia biomecánica observada."
    ],
    "interpretation": [
        "0-4 respuestas sólidas: completar nivelación en vectores, mecánica, unidades y señales antes de los retos acumulativos.",
        "5-8 respuestas sólidas: iniciar el curso con refuerzo focal en los dominios fallidos y repetir preguntas equivalentes.",
        "9-12 respuestas sólidas: avanzar a problemas de transferencia y concentrar el apoyo en incertidumbre, modelado y límites de inferencia."
    ]
}

course["assessment_principles"] = [
    "La evidencia de dominio es una producción verificable con procedimiento, no el tiempo empleado ni el volumen de texto.",
    "Una respuesta numérica sin marco, unidades, convención de signos, método e interpretación recibe crédito limitado.",
    "La recuperación sin apoyo precede a la consulta de ejemplos o soluciones.",
    "Los errores corregidos con explicación causal y control preventivo forman parte de la evaluación.",
    "Las actividades autónomas usan datos sintéticos o abiertos; no requieren grabar personas, prescribir intervenciones ni operar equipos clínicos.",
    "Una diferencia estadística o biomecánica no se presenta como diagnóstico, efecto causal ni relevancia clínica sin evidencia independiente adecuada.",
    "El estado review se mantiene hasta una revisión disciplinar humana externa documentada."
]

course["final_project"] = {
    "title": "Expediente integrador reproducible de Biomecánica",
    "scenario": (
        "Un equipo académico recibe un caso funcional simulado o un conjunto de datos abiertos con cinemática y, cuando corresponda, fuerzas externas y señales complementarias. "
        "Debe construir un expediente que conecte movimiento, cargas, hipótesis musculoesqueléticas, propiedades tisulares, calidad de medición y una interpretación funcional limitada, sin intervenir en personas ni emitir diagnóstico, causalidad terapéutica o prescripción."
    ),
    "phases": [
        "Definir pregunta, tarea, sistema, marcos, variables, uso previsto y afirmaciones fuera de alcance.",
        "Construir la descripción cinemática y verificar transformaciones, unidades, derivadas y sensibilidad al procesamiento.",
        "Formular el balance cinético o la dinámica inversa pertinente y separar momento articular neto de fuerzas musculares individuales.",
        "Incorporar una hipótesis musculoesquelética y un razonamiento tisular compatibles con el nivel de evidencia y los parámetros disponibles.",
        "Auditar la cadena de medición o procedencia de datos, incluyendo calibración declarada, sincronización, filtrado, errores y variables derivadas.",
        "Interpretar el resultado funcional usando incertidumbre, cambio detectable o límites de la herramienta elegida y proponer la siguiente evidencia necesaria.",
        "Realizar revisión por pares, corregir hallazgos y defender la versión final con trazabilidad completa."
    ],
    "deliverables": [
        "Pregunta y diagrama del sistema con marcos, fronteras, variables, unidades y supuestos.",
        "Análisis cinemático reproducible y verificado.",
        "Diagrama de cuerpo libre y análisis cinético o justificación explícita de por qué no procede.",
        "Interpretación musculoesquelética y tisular con parámetros, incertidumbre y alternativas plausibles.",
        "Expediente de medición/procedencia con controles de calidad, procesamiento, sincronización y versiones.",
        "Informe funcional con resultado, error o cambio detectable, límites de inferencia y siguiente evidencia necesaria.",
        "Registro de revisión y correcciones antes-después, más un resumen divulgativo coherente con el informe técnico."
    ],
    "integration_requirements": [
        "Incluir evidencia o una decisión metodológica explícita de cada una de las unidades 1, 2, 3, 4, 5 y 6.",
        "Incluir al menos un control geométrico o de unidades, un análisis de sensibilidad y una explicación alternativa.",
        "Separar dato observado, variable calculada, salida de modelo, interpretación biomecánica y afirmaciones clínicas fuera de alcance.",
        "Usar únicamente datos sintéticos o abiertos en el trabajo autónomo y documentar su procedencia.",
        "Defender qué resultado cambiaría la conclusión y qué evidencia adicional sería necesaria para una decisión de mayor alcance."
    ],
    "rubric": [
        {
            "criterion": "Corrección biomecánica y trazabilidad",
            "weight_percent": 30,
            "excellent": "Marcos, fuerzas, momentos, propiedades y variables derivadas son coherentes; cada afirmación se vincula con dato o premisa, método, control y límite."
        },
        {
            "criterion": "Método y reproducibilidad",
            "weight_percent": 25,
            "excellent": "Otra persona puede reconstruir transformaciones, procesamiento y cálculos con los datos, parámetros, versiones y decisiones documentados."
        },
        {
            "criterion": "Controles, incertidumbre y sensibilidad",
            "weight_percent": 20,
            "excellent": "Verifica unidades, signos, geometría y calidad de datos, analiza sensibilidad y demuestra qué supuestos dominan la conclusión."
        },
        {
            "criterion": "Integración y transferencia funcional responsable",
            "weight_percent": 15,
            "excellent": "Conecta las seis unidades y limita la interpretación a la pregunta y el uso previsto sin convertir diferencias biomecánicas en diagnóstico o causalidad no demostrada."
        },
        {
            "criterion": "Comunicación, revisión y corrección",
            "weight_percent": 10,
            "excellent": "El informe y el resumen son claros, accesibles y coherentes; la revisión por pares produce correcciones justificadas y trazables."
        }
    ]
}

course["completion_criteria"] = [
    "Demostrar los resultados de las seis unidades en evidencias verificables y corregir los errores conceptuales críticos detectados.",
    "Entregar actividades con marcos, unidades, procedimiento, controles, sensibilidad, incertidumbre y límites explícitos.",
    "Obtener una ponderación total de evaluación del 100 % sin sustituir el proyecto integrador por una prueba aislada.",
    "Completar el proyecto integrador con trazabilidad de U1–U6 y datos sintéticos o abiertos reproducibles.",
    "Aprobar una defensa que incluya un caso nuevo o una perturbación no ensayada y explique qué cambiaría la conclusión.",
    "Mantener coherencia entre resultado técnico, interpretación biomecánica, figuras y resumen divulgativo.",
    "No presentar el cierre del contenido como revisión disciplinar externa, validación clínica ni autorización de uso profesional."
]

dump_json(COURSE_PATH, course)

# El descriptor curricular es un espejo editorial del curso redevelopment; mantenerlo alineado
# evita que el catálogo muestre objetivos genéricos después de cerrar las seis unidades.
subject_path = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "biomecanica.json"
dump_json(subject_path, course)

# Invariantes básicas antes de permitir que el workflow continúe.
assert len(course["detailed_units"]) == 6
assert all(detail["description"] == units[i]["purpose"] for i, detail in enumerate(course["detailed_units"]))
assert all(detail["learning_outcomes"] == units[i]["learning_objectives"] for i, detail in enumerate(course["detailed_units"]))
assert sum(int(item["weight"].split()[0]) for item in course["assessment"]) == 100
assert sum(item["weight_percent"] for item in course["final_project"]["rubric"]) == 100

print("Biomecánica: cierre de asignatura alineado con U1-U6.")
