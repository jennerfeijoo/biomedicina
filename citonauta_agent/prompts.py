from __future__ import annotations

import json
from typing import Any


SYSTEM_PROMPT = """
Eres el editor académico autónomo de CitoNauta Biomedicina. Produces cursos universitarios
abiertos, claros, rigurosos y progresivos en español. No escribes esquemas vacíos: cada unidad
debe enseñar, explicar, ejemplificar, corregir errores frecuentes y permitir autoevaluación.

Reglas obligatorias:
1. Mantén el alcance exacto de la asignatura y evita invadir cursos posteriores.
2. Explica primero la intuición y después la formalización técnica.
3. Distingue hechos, modelos, supuestos, correlación, predicción, mecanismo y causalidad.
4. No inventes referencias, DOI, URL, autores ni instituciones.
5. Usa exclusivamente los recursos incluidos en FUENTES PERMITIDAS.
6. Evita recomendaciones clínicas personales y presenta el contenido como educación científica.
7. No repitas párrafos, actividades ni ejemplos entre unidades.
8. Cada ejemplo debe mostrar el razonamiento, no solo la respuesta.
9. Devuelve exclusivamente JSON válido conforme al esquema solicitado.
""".strip()


def generation_prompt(
    subject: dict[str, Any],
    baseline: dict[str, Any],
    sources: list[dict[str, Any]],
    related_context: list[dict[str, Any]],
    content_model: str,
    review_model: str,
) -> str:
    payload = {
        "ASIGNATURA": subject,
        "CONTENIDO_BASE": baseline,
        "FUENTES_PERMITIDAS": sources,
        "CURSOS_RELACIONADOS": related_context,
    }
    return f"""
Completa la asignatura indicada hasta convertirla en una guía educativa autosuficiente.
Conserva id={subject['id']!r} y area_id={subject['area_id']!r}. El estado final debe ser complete.

Requisitos editoriales:
- 6 a 10 unidades progresivas.
- Cada unidad contiene 2 a 4 bloques explicativos, con al menos dos párrafos claros por bloque.
- Cada unidad contiene al menos un ejemplo guiado con pasos de razonamiento.
- Incluye preguntas de autoevaluación con respuesta, errores frecuentes y aplicaciones biomédicas.
- El curso completo debe superar aproximadamente 2200 palabras de contenido sustantivo.
- Las competencias, objetivos, resultados y evaluación deben estar alineados.
- Las referencias y recursos deben proceder solo de FUENTES PERMITIDAS.
- En generation_metadata usa content_model={content_model!r} y review_model={review_model!r}.

DATOS DE TRABAJO:
{json.dumps(payload, ensure_ascii=False, indent=2)}
""".strip()


def review_prompt(course_json: str, source_json: str) -> str:
    return f"""
Audita el curso como revisor independiente. Evalúa claridad, rigor científico, progresión
pedagógica, completitud y respaldo por las fuentes permitidas. Rechaza el curso si contiene
explicaciones genéricas, repeticiones, saltos conceptuales, afirmaciones médicas no respaldadas,
referencias inventadas o ejemplos que no muestran razonamiento.

CURSO:
{course_json}

FUENTES PERMITIDAS:
{source_json}
""".strip()


def repair_prompt(course_json: str, review_json: str, validator_errors: str = "") -> str:
    return f"""
Corrige el curso completo conservando sus partes correctas. Resuelve todos los problemas del
informe y de los validadores. No reduzcas la profundidad ni elimines campos obligatorios.
Devuelve nuevamente el curso completo en JSON.

CURSO ACTUAL:
{course_json}

INFORME DE REVISIÓN:
{review_json}

ERRORES DE VALIDACIÓN TÉCNICA:
{validator_errors or 'Ninguno'}
""".strip()
