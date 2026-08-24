from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "bioinstrumentacion"


def dump(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


course_path = COURSE_DIR / "course.json"
course = json.loads(course_path.read_text(encoding="utf-8"))
course["content_version"] = "1.0.0"
course["status"] = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}
course["editorial_notice"] = (
    "Corpus canónico educativo completo a nivel de contenido estructurado y pedagogía interna. "
    "Las diez unidades, sus actividades, evaluaciones y el sistema de evaluación del curso están materializados y trazables. "
    "La revisión humana interna, la revisión disciplinaria externa, cualquier práctica con personas, la conformidad normativa y la validez clínica permanecen fuera del cierre y siguen pendientes."
)
dump(course_path, course)

assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "BIOINST-EVAL-CURSO",
    "course_id": "bioinstrumentacion",
    "scope": "course",
    "principles": [
        "La evaluación comienza por mensurando, uso previsto, arquitectura y condiciones declaradas; una cifra aislada no sustituye la especificación del sistema.",
        "Las unidades, referencias, versiones, configuraciones, parámetros y procedencia forman parte de la evidencia evaluable.",
        "Una mejora local en rango, ruido, banda, tiempo o incertidumbre no se considera mejora global sin revisar sus efectos sobre los demás presupuestos.",
        "Calibración, ajuste, verificación y validación se distinguen explícitamente y ninguna simulación se presenta como validación clínica o ensayo de conformidad.",
        "Las decisiones sobre riesgo conservan peligro, secuencia, situación peligrosa, daño, controles, riesgo residual y discrepancias; no se permite saltar del fallo al daño.",
        "Las actividades con datos o circuitos son sintéticas y reproducibles; el curso no autoriza conexión a personas ni a dispositivos médicos energizados.",
        "La retroalimentación formativa precede al cierre sumativo y las correcciones se versionan en lugar de sobrescribir silenciosamente resultados previos.",
        "El expediente final debe permitir reconstruir arquitectura, datos, código, configuración, pruebas, resultados, discrepancias, cambios y límites.",
        "La revisión automática comprueba estructura, cálculos y trazabilidad; el juicio profesional y la revisión disciplinaria permanecen humanos.",
        "Completar el curso no equivale a certificación, acreditación, conformidad regulatoria, seguridad demostrada ni autorización clínica.",
    ],
    "assessment_plan": [
        {
            "id": "BIOINST-PLAN-01",
            "component": "Autoevaluaciones razonadas de las diez unidades",
            "type": "formative_with_low_stakes_grade",
            "weight_percent": 15,
            "linked_learning_outcome_ids": [f"BIOINST-LO{i:02d}" for i in range(1, 9)],
            "evidence_files": [f"assessments/unit-{i:02d}.json" for i in range(1, 11)],
            "description": "Ochenta casos distribuidos en las diez unidades que exigen cálculo, clasificación, auditoría o decisión con explicación y límites.",
            "feedback_and_revision": "La clave razonada se consulta después del primer intento; errores conceptuales se corrigen antes de cerrar la unidad y la versión corregida conserva el razonamiento inicial.",
        },
        {
            "id": "BIOINST-PLAN-02",
            "component": "Portafolio de actividades guiadas y reproducibles",
            "type": "performance_tasks",
            "weight_percent": 25,
            "linked_learning_outcome_ids": [f"BIOINST-LO{i:02d}" for i in range(1, 9)],
            "evidence_ids": [f"BIOINST-U{i:02d}-ACT01" for i in range(1, 11)],
            "description": "Diez actividades progresivas que producen especificaciones, modelos, presupuestos, auditorías, matrices y expedientes con datos o escenarios sintéticos.",
            "feedback_and_revision": "Cada entrega se evalúa con criterios de comprobación explícitos; las revisiones conservan la versión anterior y una nota de cambios.",
        },
        {
            "id": "BIOINST-PLAN-03",
            "component": "Examen integrador intermedio",
            "type": "individual_integrative_exam",
            "weight_percent": 20,
            "linked_learning_outcome_ids": ["BIOINST-LO01", "BIOINST-LO02", "BIOINST-LO03", "BIOINST-LO04"],
            "evidence_reference": "midterm_blueprint",
            "description": "Caso nuevo después de U5 que integra mensurando, transducción, biopotenciales, acondicionamiento y adquisición digital sin reutilizar ejercicios resueltos.",
            "feedback_and_revision": "Se devuelve retroalimentación por dominio; errores de referencia, unidades, saturación, aliasing o frontera de inferencia requieren corrección razonada antes del bloque U6–U10.",
        },
        {
            "id": "BIOINST-PLAN-04",
            "component": "Proyecto integrador de expediente reproducible",
            "type": "capstone_project",
            "weight_percent": 30,
            "linked_learning_outcome_ids": [f"BIOINST-LO{i:02d}" for i in range(1, 9)],
            "evidence_reference": "capstone",
            "description": "Expediente completo de una cadena de bioinstrumentación sintética desde necesidad y mensurando hasta caracterización, riesgo, pruebas, reproducción y cierre limitado.",
            "feedback_and_revision": "La especificación, baseline y plan de pruebas se revisan antes de ejecutar el paquete final. Todo cambio posterior se registra mediante análisis de impacto y nueva versión.",
        },
        {
            "id": "BIOINST-PLAN-05",
            "component": "Defensa técnica y bitácora de decisiones",
            "type": "oral_and_process_evidence",
            "weight_percent": 10,
            "linked_learning_outcome_ids": ["BIOINST-LO01", "BIOINST-LO04", "BIOINST-LO06", "BIOINST-LO07", "BIOINST-LO08"],
            "evidence_ids": ["BIOINST-CAP-D06", "BIOINST-CAP-D07", "BIOINST-CAP-D08"],
            "description": "Defensa individual de supuestos, trade-offs, discrepancias, cambios y afirmaciones deliberadamente excluidas del alcance.",
            "feedback_and_revision": "La defensa puede descubrir una brecha que deba documentarse; no permite convertir evidencia sintética en aprobación clínica o regulatoria.",
        },
    ],
    "diagnostic": {
        "id": "BIOINST-DIAG-01",
        "title": "Diagnóstico de prerrequisitos de Bioinstrumentación",
        "purpose": "Identificar brechas en cantidades, circuitos, señales, muestreo, dinámica, metrología y riesgo antes de iniciar U1. No aporta calificación.",
        "administration": {
            "timing": "Antes de U1.",
            "conditions": "Intento individual sin consultar la clave; se solicita una justificación breve cuando la respuesta depende de supuestos.",
            "use_of_results": "Los dominios fallados generan nivelación y no excluyen del curso ni reducen la calificación.",
        },
        "scoring": {
            "points_per_question": 1,
            "maximum_points": 12,
            "rule": "Se concede el punto cuando la respuesta contiene la distinción conceptual indicada; diferencias de redacción no penalizan.",
            "partial_credit": "Las respuestas parciales orientan la nivelación aunque la clasificación usa puntos enteros.",
        },
        "questions": [
            {"id": "BIOINST-DIAG-Q01", "domain": "cantidad y señal", "question": "¿Qué diferencia una cantidad de una señal?", "answer": "La cantidad es una propiedad expresable con número y referencia; la señal es una representación física o digital que porta información."},
            {"id": "BIOINST-DIAG-Q02", "domain": "carga", "question": "¿Qué representa una impedancia de entrada?", "answer": "La relación tensión-corriente vista por la fuente y, por tanto, una posible carga introducida por la etapa siguiente."},
            {"id": "BIOINST-DIAG-Q03", "domain": "muestreo", "question": "¿Qué significa muestrear?", "answer": "Obtener valores de una señal en instantes definidos por un reloj y una frecuencia de muestreo."},
            {"id": "BIOINST-DIAG-Q04", "domain": "verificación y validación", "question": "¿Qué diferencia verificación y validación?", "answer": "La verificación aporta evidencia frente a requisitos especificados; la validación pregunta por necesidades y uso previsto bajo condiciones representativas."},
            {"id": "BIOINST-DIAG-Q05", "domain": "dinámica", "question": "¿Qué expresa una constante de tiempo?", "answer": "La escala temporal de un modelo de primer orden; no equivale por sí sola a todo tiempo de respuesta."},
            {"id": "BIOINST-DIAG-Q06", "domain": "modo común", "question": "¿Qué es el modo común en una entrada diferencial?", "answer": "La componente compartida por ambas entradas respecto de una referencia declarada."},
            {"id": "BIOINST-DIAG-Q07", "domain": "aliasing", "question": "¿Qué condición ideal relaciona banda y frecuencia de muestreo?", "answer": "Para una señal limitada en banda, la frecuencia de muestreo debe superar dos veces la frecuencia máxima; un sistema real además necesita margen y filtrado anti-alias."},
            {"id": "BIOINST-DIAG-Q08", "domain": "precisión", "question": "¿Qué diferencia repetibilidad y exactitud?", "answer": "La repetibilidad describe precisión bajo condiciones cercanas; la exactitud no se expresa como una dispersión y se relaciona con cercanía al valor de referencia."},
            {"id": "BIOINST-DIAG-Q09", "domain": "incertidumbre", "question": "¿Qué es incertidumbre de medición?", "answer": "Un parámetro no negativo que caracteriza la dispersión de valores atribuidos al mensurando con la información utilizada."},
            {"id": "BIOINST-DIAG-Q10", "domain": "riesgo", "question": "¿Qué es una cadena de riesgo?", "answer": "La relación documentada entre peligro, secuencia de eventos, situación peligrosa, posible daño y controles."},
            {"id": "BIOINST-DIAG-Q11", "domain": "reproducibilidad", "question": "¿Qué necesita una práctica reproducible?", "answer": "Datos y procedencia, código, parámetros, versiones, configuración, entorno y pasos de análisis identificables."},
            {"id": "BIOINST-DIAG-Q12", "domain": "límite de inferencia", "question": "¿Una simulación demuestra conformidad o utilidad clínica?", "answer": "No; solo aporta evidencia dentro del modelo, configuración, condiciones y alcance declarados."},
        ],
        "interpretation": [
            {"range": "10–12", "readiness": "preparado", "action": "Comenzar U1 y usar las rutas de recuperación solo si aparece una brecha específica."},
            {"range": "7–9", "readiness": "preparado con nivelación", "action": "Reforzar en paralelo circuitos, señales y metrología antes de los ejercicios integrativos."},
            {"range": "0–6", "readiness": "nivelación prioritaria", "action": "Completar fundamentos de circuitos, señales, física y análisis dimensional antes de avanzar a U3–U5."},
        ],
    },
    "midterm_blueprint": [
        {
            "id": "BIOINST-MID-01",
            "domain": "Mensurando, trazabilidad y modelo de transducción",
            "weight_percent": 20,
            "linked_learning_outcome_ids": ["BIOINST-LO01", "BIOINST-LO02"],
            "task": "A partir de un caso nuevo, especificar mensurando, referencia, cadena y modelo estático/dinámico con supuestos y unidades.",
            "evidence": "Especificación, diagrama de cadena, ecuaciones y lista de supuestos.",
        },
        {
            "id": "BIOINST-MID-02",
            "domain": "Biopotenciales e interfaz electrodo-tejido",
            "weight_percent": 20,
            "linked_learning_outcome_ids": ["BIOINST-LO03"],
            "task": "Auditar una cadena diferencial sintética e identificar interfaz, impedancias, referencia, modo común, artefactos y límites de interpretación.",
            "evidence": "Mapa fuente-interfaz-amplificador y clasificación razonada de perturbaciones.",
        },
        {
            "id": "BIOINST-MID-03",
            "domain": "Acondicionamiento analógico",
            "weight_percent": 30,
            "linked_learning_outcome_ids": ["BIOINST-LO04"],
            "task": "Dimensionar rango, ganancia, banda y ruido de una cadena analógica para evitar saturación prevista y preservar la banda útil declarada.",
            "evidence": "Presupuesto de rango/ganancia, análisis de ruido y justificación del filtrado.",
        },
        {
            "id": "BIOINST-MID-04",
            "domain": "Muestreo y adquisición digital",
            "weight_percent": 30,
            "linked_learning_outcome_ids": ["BIOINST-LO04"],
            "task": "Elegir frecuencia de muestreo, ADC y estrategia temporal para un caso sintético con interferencia, margen anti-alias, cuantización y sincronización.",
            "evidence": "Cálculo de aliasing, uso de rango ADC, resolución efectiva esperada y diagrama temporal.",
        },
    ],
    "capstone": {
        "id": "BIOINST-CAP-01",
        "title": "Expediente reproducible de una cadena de bioinstrumentación sintética",
        "purpose": "Integrar los ocho resultados de aprendizaje en un sistema educativo sintético cuya evidencia pueda reconstruirse sin ampliar indebidamente el alcance.",
        "linked_learning_outcome_ids": [f"BIOINST-LO{i:02d}" for i in range(1, 9)],
        "phases": [
            "necesidad y uso previsto",
            "mensurando y arquitectura",
            "transducción e interfaces",
            "presupuestos analógicos y digitales",
            "caracterización, calibración e incertidumbre",
            "riesgo, controles y pruebas",
            "baseline, procedencia y reproducción",
            "síntesis y cierre limitado",
        ],
        "deliverables": [
            {"id": "BIOINST-CAP-D01", "name": "Especificación y arquitectura", "description": "Necesidad, uso previsto educativo, mensurando, entradas/salidas, unidades, interfaces y exclusiones."},
            {"id": "BIOINST-CAP-D02", "name": "Presupuestos técnicos", "description": "Rango, ganancia, banda, ruido, muestreo, temporización e incertidumbre con supuestos."},
            {"id": "BIOINST-CAP-D03", "name": "Caracterización sintética", "description": "Datos, protocolo, calibración/ajuste cuando corresponda, residuales, repetibilidad y deriva/histéresis según el caso."},
            {"id": "BIOINST-CAP-D04", "name": "Matriz de riesgo y verificación", "description": "Necesidades, requisitos, peligros, controles, pruebas, resultados y discrepancias enlazados."},
            {"id": "BIOINST-CAP-D05", "name": "Paquete reproducible", "description": "Datos sintéticos, código, parámetros, dependencias, versiones, baseline, hashes y manifiesto."},
            {"id": "BIOINST-CAP-D06", "name": "Bitácora de decisiones y cambios", "description": "Decisiones, alternativas, cambios, análisis de impacto y disposición de discrepancias."},
            {"id": "BIOINST-CAP-D07", "name": "Informe técnico", "description": "Resultados, incertidumbre, criterios, cobertura, limitaciones y conclusiones proporcionales a la evidencia."},
            {"id": "BIOINST-CAP-D08", "name": "Defensa crítica", "description": "Defensa individual de trade-offs y de las afirmaciones que el expediente deliberadamente no permite realizar."},
        ],
        "rubric": [
            {"criterion": "Definición, arquitectura y trazabilidad", "weight_percent": 20, "description": "Conecta necesidad, uso previsto, mensurando, interfaces, requisitos y evidencia sin relaciones huérfanas."},
            {"criterion": "Fundamento técnico y presupuestos", "weight_percent": 25, "description": "Modelos, unidades, rango, ruido, banda, tiempo y adquisición son coherentes y revisan casos límite."},
            {"criterion": "Metrología y decisión", "weight_percent": 20, "description": "Caracterización, calibración cuando aplica, incertidumbre, criterios y decisiones se preespecifican e interpretan correctamente."},
            {"criterion": "Riesgo, verificación y límites", "weight_percent": 20, "description": "Riesgos, controles, pruebas, discrepancias y riesgo residual permanecen trazables; no se afirma conformidad o validez clínica."},
            {"criterion": "Reproducibilidad y comunicación", "weight_percent": 15, "description": "Baseline, procedencia, configuración y análisis pueden reconstruirse y las conclusiones son auditables."},
        ],
    },
    "completion_rules": {
        "minimum_total_percent": 60,
        "minimum_capstone_percent": 60,
        "critical_failures": [
            "Presentar datos sintéticos o simulaciones como evidencia clínica, de seguridad o de conformidad.",
            "Eliminar o sobrescribir una discrepancia relevante para aparentar cumplimiento.",
            "No poder identificar la configuración o procedencia del resultado final.",
            "Omitir una incompatibilidad de interfaz o saturación que invalide el resultado dentro del propio caso educativo.",
        ],
        "interpretation": "Estas reglas son criterios académicos internos del curso y no estándares profesionales, regulatorios ni institucionales.",
    },
    "status": "curated_pending_expert_review",
}

dump(COURSE_DIR / "assessments" / "course-assessment.json", assessment)
print("Curated Bioinstrumentation course assessment and completion metadata")
