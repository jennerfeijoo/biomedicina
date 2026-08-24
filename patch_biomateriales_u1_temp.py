#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data/course_redevelopment/biomateriales/units/unit-01.json"
MIRROR = ROOT / "data/generated_units/biomateriales/unit-01.json"

unit = json.loads(SOURCE.read_text(encoding="utf-8"))
activities = unit.setdefault("guided_activities", [])
titles = {item.get("title") for item in activities}

activity_2 = {
    "title": "Actividad guiada: auditoría de datos de propiedades antes de comparar materiales",
    "instructions": [
        "Trabaja con la tabla sintética proporcionada; contiene deliberadamente unidades, temperaturas y métodos de ensayo incompatibles.",
        "No calcules un ranking hasta haber identificado qué datos son comparables y cuáles requieren conversión, contexto adicional o exclusión.",
        "Para cada propiedad conserva material, estado, unidad, método, temperatura, medio y fuente simulada.",
        "Documenta cada corrección y deja como dato faltante cualquier valor que no pueda armonizarse sin inventar información."
    ],
    "problems": [
        "Detecta al menos seis incompatibilidades de unidades, condiciones o definiciones y explica por qué afectan la comparación.",
        "Convierte únicamente las magnitudes que puedan transformarse sin cambiar su significado físico y muestra las unidades intermedias.",
        "Separa rigidez, resistencia, dureza y tenacidad a fractura y asigna a cada una una pregunta de diseño distinta.",
        "Identifica dos propiedades cuyo valor dependa especialmente del tiempo, temperatura, medio u orientación y propone qué metadatos faltan.",
        "Construye una tabla final de datos utilizables y otra de datos rechazados o pendientes, indicando la razón de cada decisión.",
        "Redacta qué medición adicional reduciría más la incertidumbre entre los dos candidatos mejor posicionados."
    ],
    "deliverables": [
        "Tabla de inconsistencias detectadas y correcciones justificadas.",
        "Tabla armonizada con unidades, condiciones, fuente y marca de confianza.",
        "Registro de datos excluidos o pendientes con la evidencia necesaria para recuperarlos.",
        "Conclusión sobre qué comparación es defendible y cuál todavía no lo es."
    ],
    "checking_criteria": [
        "No se comparan números que representen magnitudes o condiciones incompatibles.",
        "Todas las conversiones conservan unidades y no inventan precisión.",
        "Rigidez, resistencia, dureza y tenacidad permanecen diferenciadas.",
        "Los datos ausentes se reconocen explícitamente en lugar de imputarse sin justificación.",
        "La conclusión identifica la principal fuente de incertidumbre residual y la medición que la reduciría."
    ]
}

activity_3 = {
    "title": "Actividad guiada: auditoría de una afirmación de biocompatibilidad",
    "instructions": [
        "Analiza una ficha sintética que afirma que un material es «biocompatible y seguro para implantes» sin aportar contexto suficiente.",
        "Descompón la afirmación en material, componente o dispositivo, forma final, superficie, proceso, tipo y duración de contacto y uso previsto.",
        "Clasifica qué evidencia podría apoyar una preselección de material y qué evidencia pertenece a evaluación biológica, verificación del dispositivo o estudios clínicos.",
        "No emitas una conclusión de seguridad; produce una lista de preguntas y evidencia necesaria para evaluar el riesgo de forma proporcional."
    ],
    "problems": [
        "Identifica al menos cinco datos ausentes que impiden interpretar la palabra «biocompatible» como propiedad universal.",
        "Explica cómo un cambio de recubrimiento, esterilización o residuo de fabricación podría modificar la evaluación aunque el material base conserve el mismo nombre.",
        "Reescribe la afirmación comercial como una afirmación técnica limitada que solo describa lo demostrado por los datos sintéticos disponibles.",
        "Construye una matriz pregunta-evidencia-riesgo que separe caracterización química/física, desempeño mecánico y evaluación biológica.",
        "Propón el siguiente estudio o dato necesario para cada brecha sin afirmar que una norma o guía por sí sola demuestra conformidad.",
        "Redacta una conclusión final que distinga selección de material, seguridad del dispositivo, beneficio clínico y decisión regulatoria."
    ],
    "deliverables": [
        "Lista priorizada de información faltante sobre forma final, contacto, proceso y uso previsto.",
        "Matriz pregunta-evidencia-riesgo con responsables o etapa de evaluación correspondiente.",
        "Versión corregida de la afirmación y conclusión acotada sin lenguaje clínico no sustentado."
    ],
    "checking_criteria": [
        "La biocompatibilidad se trata como relación contextual y no como atributo binario del material.",
        "Se distingue material de dispositivo terminado y se consideran superficie, proceso y esterilización.",
        "Las fuentes normativas o regulatorias se usan para orientar evaluación, no como prueba automática de seguridad o eficacia.",
        "La matriz separa evidencia disponible de evidencia faltante y relaciona cada brecha con un riesgo o pregunta.",
        "La conclusión no recomienda uso clínico ni declara conformidad regulatoria."
    ]
}

for activity in (activity_2, activity_3):
    if activity["title"] not in titles:
        activities.append(activity)

assert len(activities) >= 3
text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
print(f"Biomateriales U1: {len(activities)} actividades guiadas sincronizadas.")
