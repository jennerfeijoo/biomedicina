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


def _text(value: Any, maximum: int) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= maximum:
        return text
    return text[: maximum - 1].rstrip() + "…"


def _list(value: Any, maximum_items: int, maximum_chars: int = 220) -> list[str]:
    if not isinstance(value, list):
        return []
    return [_text(item, maximum_chars) for item in value[:maximum_items] if str(item).strip()]


def _compact_baseline(baseline: dict[str, Any]) -> dict[str, Any]:
    """Keep curricular intent while excluding pre-existing long-form course bodies."""
    return {
        "id": baseline.get("id"),
        "area_id": baseline.get("area_id"),
        "status": baseline.get("status"),
        "description": _text(baseline.get("description"), 700),
        "level": _text(baseline.get("level"), 160),
        "estimated_workload": _text(baseline.get("estimated_workload"), 160),
        "biomedical_connection": _text(baseline.get("biomedical_connection"), 900),
        "prerequisites": _list(baseline.get("prerequisites"), 8),
        "course_competencies": _list(baseline.get("course_competencies"), 10),
        "learning_objectives": _list(baseline.get("learning_objectives"), 10),
        "learning_outcomes": _list(baseline.get("learning_outcomes"), 12),
        "modules": _list(baseline.get("modules"), 10),
        "key_concepts": _list(baseline.get("key_concepts"), 20, 100),
        "related_subjects": _list(baseline.get("related_subjects"), 10, 100),
    }


def _compact_source(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": _text(source.get("title"), 220),
        "url": str(source.get("url") or ""),
        "year": source.get("year"),
        "type": _text(source.get("type"), 80),
        "authors": _list(source.get("authors"), 4, 100),
        "abstract_excerpt": _text(
            source.get("abstract_excerpt") or source.get("description"),
            320,
        ),
    }


def _compact_related(item: dict[str, Any]) -> dict[str, Any]:
    baseline = item.get("baseline_summary")
    if not isinstance(baseline, dict):
        baseline = {}
    return {
        "similarity": item.get("similarity"),
        "id": item.get("id"),
        "title": item.get("title"),
        "area_id": item.get("area_id"),
        "description": _text(item.get("description"), 320),
        "biomedical_connection": _text(item.get("biomedical_connection"), 420),
        "modules": _list(baseline.get("modules"), 6, 140),
        "key_concepts": _list(baseline.get("key_concepts"), 10, 80),
    }


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
        "CONTENIDO_BASE": _compact_baseline(baseline),
        "FUENTES_PERMITIDAS": [_compact_source(item) for item in sources[:8]],
        "CURSOS_RELACIONADOS": [_compact_related(item) for item in related_context[:4]],
    }
    compact_payload = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f"""
Completa la asignatura indicada hasta convertirla en una guía educativa autosuficiente.
Conserva id={subject['id']!r} y area_id={subject['area_id']!r}. El estado final debe ser complete.

Requisitos editoriales y de tamaño:
- Genera exactamente 6 unidades progresivas y numéralas del 1 al 6.
- El campo description de cada unidad debe ser una síntesis sustantiva de entre 140 y 220
  caracteres; no uses frases telegráficas ni simples etiquetas temáticas.
- Cada unidad contiene exactamente 2 bloques explicativos; cada bloque incluye 2 o 3 párrafos
  sustantivos y entre 3 y 5 puntos clave.
- Cada unidad contiene exactamente 1 ejemplo guiado con entre 3 y 6 pasos de razonamiento.
- Cada unidad incluye 2 actividades, 2 preguntas de autoevaluación con respuesta, 2 errores
  frecuentes y entre 1 y 3 aplicaciones biomédicas.
- El curso completo debe contener entre 2200 y 3000 palabras sustantivas. Prioriza profundidad
  conceptual y precisión; evita redundancia, introducciones ceremoniales y listas infladas.
- Incluye 4 actividades prácticas globales, 3 componentes de evaluación cuyas ponderaciones
  sumen 100%, entre 10 y 18 conceptos clave y entre 4 y 8 asignaturas relacionadas.
- Incluye entre 5 y 8 fuentes y recursos, exclusivamente de FUENTES PERMITIDAS. No copies
  resúmenes largos ni repitas datos bibliográficos en las explicaciones.
- Las competencias, objetivos, resultados y evaluación deben estar alineados.
- En generation_metadata usa content_model={content_model!r} y review_model={review_model!r}.
- Cierra completamente el objeto JSON. No termines en mitad de una cadena, lista u objeto.

DATOS DE TRABAJO COMPACTADOS:
{compact_payload}
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
Mantén el resultado entre 2200 y 3000 palabras y devuelve el objeto JSON completo y cerrado.

CURSO ACTUAL:
{course_json}

INFORME DE REVISIÓN:
{review_json}

ERRORES DE VALIDACIÓN TÉCNICA:
{validator_errors or 'Ninguno'}
""".strip()
