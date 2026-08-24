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
        "Trabaja únicamente con la tabla sintética proporcionada; no uses datos de pacientes, personas, animales ni muestras biológicas.",
        "La tabla contiene deliberadamente unidades, temperaturas, orientaciones y métodos de ensayo incompatibles: no calcules un ranking antes de auditar su comparabilidad.",
        "Para cada dato conserva material, estado, unidad, método, temperatura, medio, orientación y fuente simulada cuando correspondan.",
        "Convierte unidades solo cuando la transformación preserve el significado físico de la magnitud.",
        "Separa datos utilizables, datos comparables después de corrección y datos que deben quedar pendientes por falta de información.",
        "Documenta cada corrección y no rellenes valores ausentes con supuestos no declarados."
    ],
    "problems": [
        "Detecta al menos seis incompatibilidades de unidades, condiciones, orientaciones o definiciones y explica por qué afectan la comparación.",
        "Convierte únicamente las magnitudes que puedan armonizarse sin cambiar su significado físico y muestra las unidades intermedias.",
        "Separa módulo elástico, resistencia, dureza y tenacidad a fractura y asigna a cada una una pregunta de diseño distinta.",
        "Identifica dos propiedades cuyo valor dependa especialmente del tiempo, temperatura, medio u orientación y enumera los metadatos faltantes.",
        "Explica por qué un valor longitudinal de un compuesto no debe reutilizarse como propiedad transversal sin evidencia.",
        "Identifica un caso en el que dos valores numéricos tengan la misma unidad pero no sean comparables por corresponder a métodos o condiciones diferentes.",
        "Construye una tabla final de datos utilizables con material, propiedad, valor o rango, unidad, condición y marca de confianza.",
        "Construye una tabla separada de datos rechazados o pendientes e indica para cada fila qué evidencia permitiría recuperarla.",
        "Repite una comparación usando el límite inferior y superior del rango de una propiedad incierta y registra si cambia el orden de candidatos.",
        "Selecciona una propiedad cuya incertidumbre afecte al ranking y justifica qué nuevo ensayo reduciría mejor esa incertidumbre.",
        "Redacta una regla de control de calidad que impida comparar automáticamente datos sin metadatos mínimos.",
        "Cierra con una conclusión que distinga qué comparación es defendible, cuál es provisional y cuál no puede hacerse con los datos disponibles."
    ],
    "deliverables": [
        "Tabla de inconsistencias detectadas y correcciones justificadas.",
        "Registro de conversiones con unidades iniciales, operación y unidades finales.",
        "Tabla armonizada de datos utilizables con condiciones y marca de confianza.",
        "Tabla de datos rechazados o pendientes y evidencia necesaria para recuperarlos.",
        "Comparación nominal y de sensibilidad para al menos una propiedad incierta.",
        "Regla mínima de control de calidad para futuros datos de propiedades.",
        "Conclusión acotada sobre comparaciones defendibles y no defendibles."
    ],
    "checking_criteria": [
        "No se comparan números que representen magnitudes, métodos, orientaciones o condiciones incompatibles.",
        "Todas las conversiones conservan unidades y no inventan precisión.",
        "Rigidez, resistencia, dureza y tenacidad a fractura permanecen diferenciadas.",
        "Los datos ausentes o insuficientes se reconocen explícitamente en lugar de imputarse sin justificación.",
        "La anisotropía se conserva cuando una propiedad depende de la orientación.",
        "Cada dato utilizable mantiene metadatos suficientes para reconstruir su contexto.",
        "La sensibilidad muestra si una incertidumbre plausible cambia la comparación.",
        "La conclusión identifica la principal incertidumbre residual y la medición que podría reducirla.",
        "No se utilizan datos de pacientes, personas, animales ni muestras biológicas.",
        "Otra persona puede reconstruir qué datos fueron aceptados, corregidos o rechazados."
    ]
}

activity_3 = {
    "title": "Actividad guiada: auditoría de una afirmación de biocompatibilidad",
    "instructions": [
        "Analiza únicamente una ficha sintética; no uses datos de pacientes, personas, animales ni muestras biológicas.",
        "La ficha afirma que un material es «biocompatible y seguro para implantes» sin aportar contexto suficiente.",
        "Descompón la afirmación en material, componente o dispositivo, forma final, superficie, proceso, esterilización, tipo y duración de contacto y uso previsto.",
        "Clasifica qué evidencia puede apoyar una preselección técnica y qué evidencia pertenece a caracterización, evaluación biológica, verificación del dispositivo o estudios clínicos.",
        "Usa normas y guías solo para identificar preguntas y evidencia necesaria; no las presentes como prueba automática de seguridad o conformidad.",
        "No emitas una conclusión de seguridad: produce una lista priorizada de brechas y una versión corregida de la afirmación."
    ],
    "problems": [
        "Identifica al menos cinco datos ausentes que impiden interpretar la palabra «biocompatible» como propiedad universal.",
        "Explica por qué debe distinguirse el material de la forma final del dispositivo.",
        "Describe cómo un cambio de recubrimiento podría modificar la interfaz aunque el material base conserve el mismo nombre.",
        "Describe cómo esterilización, residuos de fabricación o productos de degradación podrían cambiar la exposición biológica.",
        "Clasifica cada afirmación de la ficha como demostrada, plausible pero no demostrada, fuera de alcance o insuficientemente especificada.",
        "Reescribe la frase comercial como una afirmación técnica limitada que solo describa lo respaldado por la ficha sintética.",
        "Construye una matriz pregunta-evidencia-riesgo que separe caracterización química y física, desempeño mecánico, evaluación biológica y evidencia clínica.",
        "Para cada brecha de la matriz propone el siguiente dato o estudio necesario sin afirmar que una norma por sí sola demuestra conformidad.",
        "Explica qué parte de la evaluación dependería del tipo y duración de contacto con el cuerpo.",
        "Identifica dos cambios de diseño o proceso que obligarían a revisar la evidencia previamente reunida.",
        "Distingue explícitamente selección de material, seguridad del dispositivo, beneficio clínico y decisión regulatoria.",
        "Redacta una conclusión final de máximo 150 palabras que conserve esas cuatro fronteras y priorice la siguiente evidencia necesaria."
    ],
    "deliverables": [
        "Lista priorizada de información faltante sobre forma final, contacto, proceso, superficie, esterilización y uso previsto.",
        "Tabla de clasificación de afirmaciones con justificación.",
        "Matriz pregunta-evidencia-riesgo separada por etapa de evaluación.",
        "Versión técnica corregida de la afirmación comercial.",
        "Lista de cambios de diseño o proceso que exigirían reevaluar evidencia.",
        "Conclusión acotada sin lenguaje clínico o regulatorio no sustentado.",
        "Siguiente evidencia priorizada para reducir la incertidumbre."
    ],
    "checking_criteria": [
        "La biocompatibilidad se trata como relación contextual y no como atributo binario del material.",
        "Se distingue material constitutivo de componente y dispositivo terminado.",
        "Superficie, proceso, esterilización y productos de degradación se consideran parte del contexto de exposición.",
        "Las fuentes normativas o regulatorias orientan la evaluación y no se usan como prueba automática de seguridad o eficacia.",
        "La matriz separa evidencia disponible de evidencia faltante y relaciona cada brecha con una pregunta o riesgo.",
        "La versión corregida no afirma más de lo respaldado por los datos sintéticos.",
        "Se distinguen preselección técnica, seguridad del dispositivo, beneficio clínico y conformidad regulatoria.",
        "La conclusión no recomienda uso clínico ni declara conformidad regulatoria.",
        "No se utilizan datos de pacientes, personas, animales ni muestras biológicas.",
        "La siguiente evidencia propuesta corresponde a la brecha identificada y no a una lista genérica de ensayos."
    ]
}

for activity in (activity_2, activity_3):
    if activity["title"] not in titles:
        activities.append(activity)

assert len(activities) >= 3
assert any("no uses datos de pacientes" in instruction.casefold() for activity in activities for instruction in activity.get("instructions", []))
text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
print(f"Biomateriales U1: {len(activities)} actividades guiadas sincronizadas.")
