#!/usr/bin/env python3
"""Render advanced unit JSON into the public static lesson structure.

The renderer is deliberately schema-tolerant across the validated 1.0 and 2.0
unit formats. It preserves supplied scientific text and does not invent missing
content. Generic course-outline rendering remains available only when no
advanced unit JSON exists.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ADVANCED_UNIT_ROOT = Path("data/generated_units")
CANONICAL_COURSE_ROOT = Path("data/courses")
ADVANCED_MARKER = "<!-- advanced-unit-renderer:v1 -->"


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def as_dict_list(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def as_text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def as_biomedical_connection_list(value: Any) -> list[str]:
    """Normaliza conexiones biomédicas sin exponer representaciones internas."""
    if not isinstance(value, list):
        return []
    output: list[str] = []
    for item in value:
        if isinstance(item, dict):
            topic = str(item.get("topic") or item.get("title") or item.get("label") or "").strip()
            connection = str(
                item.get("connection")
                or item.get("description")
                or item.get("text")
                or item.get("value")
                or ""
            ).strip()
            text = f"{topic}: {connection}" if topic and connection else topic or connection
        else:
            text = str(item or "").strip()
        if text:
            output.append(text)
    return output


def load_json_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: la raíz debe ser un objeto JSON")
    return data


def canonical_course_directory(root: Path, subject_id: str) -> Path:
    return root / CANONICAL_COURSE_ROOT / subject_id


def canonical_records(course_dir: Path, filename: str, field: str) -> dict[str, dict[str, Any]]:
    path = course_dir / filename
    if not path.exists():
        return {}
    payload = load_json_object(path)
    records = payload.get(field)
    if not isinstance(records, list):
        return {}
    return {
        str(item.get("id") or "").strip(): item
        for item in records
        if isinstance(item, dict) and str(item.get("id") or "").strip()
    }


def canonical_unit_to_advanced(root: Path, unit: dict[str, Any]) -> dict[str, Any]:
    """Project canonical topic blocks and registries into the legacy renderer API."""
    subject_id = str(unit.get("course_id") or "").strip()
    course_dir = canonical_course_directory(root, subject_id)
    theory_sections: list[dict[str, Any]] = []
    for topic in as_dict_list(unit.get("topics")):
        paragraphs: list[str] = []
        key_points: list[str] = []
        for subtopic in as_dict_list(topic.get("subtopics")):
            title = str(subtopic.get("title") or "").strip()
            if title:
                key_points.append(title.rstrip(".") + ".")
            for block in as_dict_list(subtopic.get("blocks")):
                if block.get("type") == "paragraph" and str(block.get("text") or "").strip():
                    paragraphs.append(str(block["text"]).strip())
        equations = []
        for block in as_dict_list(topic.get("blocks")):
            if block.get("type") != "equation":
                continue
            equation = {"latex": str(block.get("latex") or "").strip()}
            if block.get("label"):
                equation["label"] = block["label"]
            if isinstance(block.get("variables"), dict):
                equation["variables"] = block["variables"]
            equations.append(equation)
        theory_sections.append(
            {
                "heading": str(topic.get("title") or "Tema").strip(),
                "paragraphs": paragraphs,
                "equations": equations,
                "key_points": key_points,
            }
        )

    assessment_path = course_dir / str(unit.get("assessment_file") or "")
    assessment = load_json_object(assessment_path) if assessment_path.exists() else {}
    self_assessment = []
    for item in as_dict_list(assessment.get("items")):
        answer_key = item.get("answer_key") if isinstance(item.get("answer_key"), dict) else {}
        misconceptions = as_text_list(answer_key.get("common_misconceptions"))
        self_assessment.append(
            {
                "question": str(item.get("prompt") or "").strip(),
                "answer": str(answer_key.get("expected_answer") or "").strip(),
                "explanation": str(answer_key.get("explanation") or "").strip(),
                "common_error": misconceptions[0] if misconceptions else "",
            }
        )

    glossary_records = canonical_records(course_dir, "glossary.json", "entries")
    source_records = canonical_records(course_dir, "sources.json", "sources")
    glossary = [glossary_records[item] for item in unit.get("glossary_entry_ids", []) if item in glossary_records]
    sources = [source_records[item] for item in unit.get("source_ids", []) if item in source_records]
    learning_outcomes = [
        str(item.get("statement") or "").strip()
        for item in as_dict_list(unit.get("learning_outcomes"))
        if str(item.get("statement") or "").strip()
    ]
    return {
        "schema_version": "canonical-1.0",
        "subject_id": subject_id,
        "area_id": str(unit.get("area_id") or ""),
        "unit": int(unit.get("order", 0)),
        "slug": str(unit.get("slug") or ""),
        "title": str(unit.get("title") or ""),
        "status": str((unit.get("status") or {}).get("content") or "in_review")
        if isinstance(unit.get("status"), dict)
        else str(unit.get("status") or "in_review"),
        "purpose": str(unit.get("purpose") or ""),
        "learning_objectives": learning_outcomes,
        "theory_sections": theory_sections,
        "worked_examples": as_dict_list(unit.get("examples")),
        "guided_activities": as_dict_list(unit.get("activities")),
        "common_errors": unit.get("common_errors", []),
        "self_assessment": self_assessment,
        "glossary": glossary,
        "biomedical_connections": unit.get("biomedical_connections", []),
        "sources": sources,
        "editorial_notice": str(unit.get("editorial_notice") or ""),
    }


def load_advanced_unit(root: Path, subject_id: str, unit_number: int) -> dict[str, Any] | None:
    canonical_path = (
        canonical_course_directory(root, subject_id) / "units" / f"unit-{unit_number:02d}.json"
    )
    if canonical_path.exists():
        data = load_json_object(canonical_path)
        if str(data.get("course_id") or "").strip() != subject_id:
            raise ValueError(f"{canonical_path.relative_to(root)}: course_id no coincide")
        if int(data.get("order", 0)) != unit_number:
            raise ValueError(f"{canonical_path.relative_to(root)}: orden de unidad no coincide")
        return canonical_unit_to_advanced(root, data)

    path = root / ADVANCED_UNIT_ROOT / subject_id / f"unit-{unit_number:02d}.json"
    if not path.exists():
        return None
    data = load_json_object(path)
    if str(data.get("subject_id", "")).strip() != subject_id:
        raise ValueError(f"{path.relative_to(root)}: subject_id no coincide")
    if int(data.get("unit", 0)) != unit_number:
        raise ValueError(f"{path.relative_to(root)}: número de unidad no coincide")
    return data


def render_text_list(items: list[str], *, ordered: bool = False, css_class: str = "") -> str:
    tag = "ol" if ordered else "ul"
    class_attr = f' class="{esc(css_class)}"' if css_class else ""
    if not items:
        return '<p class="muted">No se proporcionó contenido para este bloque.</p>'
    body = "\n".join(f"        <li>{esc(item)}</li>" for item in items)
    return f"      <{tag}{class_attr}>\n{body}\n      </{tag}>"


def normalize_latex(value: Any) -> str:
    latex = str(value or "").strip()
    if latex.startswith("\\[") and latex.endswith("\\]"):
        latex = latex[2:-2].strip()
    if latex.startswith("$$") and latex.endswith("$$") and len(latex) >= 4:
        latex = latex[2:-2].strip()
    elif latex.startswith("$") and latex.endswith("$") and len(latex) >= 2:
        latex = latex[1:-1].strip()
    return latex


def render_equation(equation: Any) -> str:
    if isinstance(equation, str):
        raw = equation.strip()
        description = ""
        if raw.startswith("$"):
            closing = raw.find("$", 1)
            if closing > 1:
                latex = normalize_latex(raw[: closing + 1])
                description = raw[closing + 1 :].strip(" .")
            else:
                latex = normalize_latex(raw)
        elif "$" in raw:
            latex_text, description_text = raw.split("$", 1)
            latex = normalize_latex(latex_text)
            description = description_text.strip(" .")
        else:
            latex = normalize_latex(raw)
        variables: dict[str, Any] = {}
    elif isinstance(equation, dict):
        latex = normalize_latex(equation.get("latex"))
        description = str(equation.get("description") or equation.get("label") or equation.get("meaning") or "").strip()
        raw_variables = equation.get("variables")
        variables = raw_variables if isinstance(raw_variables, dict) else {}
    else:
        return ""
    if not latex:
        return ""

    variable_items = ""
    if variables:
        rows = "\n".join(
            f"              <li><code>{esc(symbol)}</code>: {esc(meanings)}</li>"
            for symbol, meanings in variables.items()
        )
        variable_items = f"\n            <ul class=\"equation-variables\">\n{rows}\n            </ul>"
    description_html = f"\n            <figcaption>{esc(description)}</figcaption>" if description else ""
    return (
        "          <figure class=\"lesson-equation\">\n"
        f"            <div class=\"math-display\">\\[{esc(latex)}\\]</div>"
        f"{description_html}{variable_items}\n"
        "          </figure>"
    )


def render_theory_sections(unit: dict[str, Any]) -> str:
    rendered: list[str] = [f"      {ADVANCED_MARKER}"]
    for index, section in enumerate(as_dict_list(unit.get("theory_sections")), start=1):
        heading = str(section.get("heading") or section.get("title") or f"Sección {index}").strip()
        paragraphs = as_text_list(section.get("paragraphs"))
        equations = section.get("equations") if isinstance(section.get("equations"), list) else []
        key_points = as_text_list(section.get("key_points"))

        rendered.append('      <article class="lesson-topic advanced-theory-section">')
        rendered.append(f'        <p class="eyebrow">Desarrollo {index}</p>')
        rendered.append(f"        <h3>{esc(heading)}</h3>")
        rendered.extend(f"        <p>{esc(paragraph)}</p>" for paragraph in paragraphs)

        equation_html = [render_equation(item) for item in equations]
        equation_html = [item for item in equation_html if item]
        if equation_html:
            rendered.append("        <div class=\"equation-set\">")
            rendered.extend(equation_html)
            rendered.append("        </div>")

        if key_points:
            rendered.append("        <h4>Puntos de integración</h4>")
            rendered.append(render_text_list(key_points))
        rendered.append("      </article>")

    if len(rendered) == 1:
        rendered.append('<p class="muted">La unidad avanzada no contiene secciones teóricas.</p>')
    return "\n".join(rendered)


def render_worked_examples(unit: dict[str, Any]) -> str:
    examples = as_dict_list(unit.get("worked_examples")) or as_dict_list(unit.get("worked_example"))
    if not examples:
        return '<p class="muted">La unidad no proporciona ejemplos resueltos.</p>'

    rendered: list[str] = []
    for index, example in enumerate(examples, start=1):
        title = str(example.get("title") or f"Ejemplo {index}").strip()
        scenario = str(example.get("scenario") or "").strip()
        steps = as_text_list(example.get("reasoning_steps"))
        interpretation = str(example.get("interpretation") or example.get("conclusion") or "").strip()
        limitations = as_text_list(example.get("limitations"))

        rendered.append('      <article class="worked-example advanced-worked-example">')
        rendered.append(f"        <h3>{esc(title)}</h3>")
        if scenario:
            rendered.append(f"        <p><strong>Situación.</strong> {esc(scenario)}</p>")
        if steps:
            rendered.append("        <h4>Razonamiento paso a paso</h4>")
            rendered.append(render_text_list(steps, ordered=True, css_class="case-steps"))
        if interpretation:
            rendered.append(f"        <p><strong>Interpretación.</strong> {esc(interpretation)}</p>")
        if limitations:
            rendered.append("        <h4>Limitaciones</h4>")
            rendered.append(render_text_list(limitations))
        rendered.append("      </article>")
    return "\n".join(rendered)


def activity_task_items(activity: dict[str, Any]) -> list[str]:
    items: list[str] = []
    for key in ("problems", "tasks", "exercises"):
        items.extend(as_text_list(activity.get(key)))
    return items


def render_guided_activities(unit: dict[str, Any]) -> str:
    activities = as_dict_list(unit.get("guided_activities")) or as_dict_list(unit.get("guided_activity"))
    if not activities:
        return '<p class="muted">La unidad no proporciona una actividad guiada.</p>'

    rendered: list[str] = []
    for index, activity in enumerate(activities, start=1):
        title = str(activity.get("title") or f"Actividad {index}").strip()
        instructions = as_text_list(activity.get("instructions"))
        tasks = activity_task_items(activity)
        criteria = as_text_list(activity.get("checking_criteria"))
        deliverables = as_text_list(activity.get("deliverables"))

        rendered.append('      <article class="guided-activity advanced-guided-activity">')
        rendered.append(f"        <h3>{esc(title)}</h3>")
        if instructions:
            rendered.append("        <h4>Procedimiento</h4>")
            rendered.append(render_text_list(instructions, ordered=True, css_class="activity-steps"))
        if tasks:
            rendered.append("        <h4>Problemas y tareas</h4>")
            rendered.append(render_text_list(tasks))
        if deliverables:
            rendered.append("        <h4>Entregables</h4>")
            rendered.append(render_text_list(deliverables))
        if criteria:
            rendered.append("        <h4>Criterios de comprobación</h4>")
            rendered.append(render_text_list(criteria))
        rendered.append("      </article>")
    return "\n".join(rendered)


def render_common_errors(unit: dict[str, Any]) -> str:
    errors = unit.get("common_errors")
    if not isinstance(errors, list) or not errors:
        return ""

    items: list[str] = []
    for item in errors:
        if isinstance(item, dict):
            error = str(item.get("error") or item.get("misconception") or "").strip()
            correction = str(item.get("correction") or item.get("explanation") or "").strip()
            if error and correction:
                items.append(
                    "        <li>"
                    f"<strong>{esc(error)}</strong>"
                    f"<p>{esc(correction)}</p>"
                    "</li>"
                )
            elif error:
                items.append(f"        <li>{esc(error)}</li>")
        elif str(item).strip():
            items.append(f"        <li>{esc(item)}</li>")
    if not items:
        return ""
    return (
        "      <section class=\"common-errors\">\n"
        "        <h3>Errores frecuentes y corrección</h3>\n"
        "        <ul class=\"rich-list\">\n"
        + "\n".join(items)
        + "\n        </ul>\n"
        "      </section>"
    )


def render_self_assessment(unit: dict[str, Any]) -> str:
    questions = as_dict_list(unit.get("self_assessment"))
    panels: list[str] = []
    for number, item in enumerate(questions, start=1):
        question = str(item.get("question") or "").strip()
        answer = str(item.get("answer") or "").strip()
        reasoning = str(item.get("reasoning") or item.get("explanation") or "").strip()
        common_error = str(item.get("common_error") or "").strip()
        if not question:
            continue
        body = [f"        <p><strong>Respuesta:</strong> {esc(answer)}</p>"] if answer else []
        if reasoning:
            body.append(f"        <p><strong>Razonamiento:</strong> {esc(reasoning)}</p>")
        if common_error:
            body.append(f"        <p><strong>Error que evita:</strong> {esc(common_error)}</p>")
        panels.append(
            "      <details class=\"answer-panel\">\n"
            f"        <summary>{number}. {esc(question)}</summary>\n"
            + "\n".join(body)
            + "\n      </details>"
        )

    blocks = [render_common_errors(unit)]
    if panels:
        blocks.append('<div class="assessment-panels">\n' + "\n".join(panels) + "\n      </div>")
    if not any(blocks):
        return '<p class="muted">La unidad no proporciona autoevaluación.</p>'
    return "\n".join(block for block in blocks if block)


def render_glossary(unit: dict[str, Any]) -> str:
    glossary = as_dict_list(unit.get("glossary"))
    if not glossary:
        return '<p class="muted">La unidad no proporciona glosario.</p>'
    items: list[str] = []
    for entry in glossary:
        term = str(entry.get("term") or entry.get("title") or "").strip()
        definition = str(entry.get("definition") or entry.get("description") or "").strip()
        if term and definition:
            items.append(f"        <li><strong>{esc(term)}</strong><p>{esc(definition)}</p></li>")
    return '<ul class="rich-list advanced-glossary">\n' + "\n".join(items) + "\n      </ul>"


def render_sources(unit: dict[str, Any]) -> str:
    sources = as_dict_list(unit.get("sources"))
    if not sources:
        return '<p class="muted">La unidad no proporciona fuentes específicas.</p>'
    items: list[str] = []
    for source in sources:
        title = str(source.get("title") or source.get("url") or "Fuente").strip()
        url = str(source.get("url") or "").strip()
        organization = str(source.get("organization") or "").strip()
        source_type = str(source.get("type") or "").strip()
        year = str(source.get("year") or "").strip()
        metadata = " · ".join(item for item in (organization, source_type, year) if item)
        title_html = (
            f'<a class="resource-link" href="{esc(url)}" rel="noopener noreferrer">{esc(title)}</a>'
            if url.startswith(("https://", "http://"))
            else esc(title)
        )
        meta_html = f'<span class="course-tag">{esc(metadata)}</span>' if metadata else ""
        items.append(f"        <li><strong>{title_html}</strong>{meta_html}</li>")
    return '<ol class="rich-list advanced-sources">\n' + "\n".join(items) + "\n      </ol>"


def render_topics(unit: dict[str, Any]) -> str:
    headings = [
        str(section.get("heading") or section.get("title") or "").strip()
        for section in as_dict_list(unit.get("theory_sections"))
    ]
    headings = [item for item in headings if item]
    if not headings:
        headings = as_text_list(unit.get("topics"))
    return render_text_list(headings)


def render_synthesis(unit: dict[str, Any]) -> str:
    purpose = str(unit.get("purpose") or "").strip()
    connections = as_biomedical_connection_list(unit.get("biomedical_connections"))
    notice = str(unit.get("editorial_notice") or "").strip()
    parts: list[str] = []
    if purpose:
        parts.append(purpose.rstrip(".") + ".")
    if connections:
        parts.append("Conecta especialmente con " + ", ".join(item.rstrip(".") for item in connections[:4]) + ".")
    if notice:
        parts.append(notice.rstrip(".") + ".")
    return " ".join(parts)


def advanced_replacements(unit: dict[str, Any]) -> dict[str, str]:
    objectives = as_text_list(unit.get("learning_objectives")) or as_text_list(unit.get("learning_outcomes"))
    title = str(unit.get("title") or "Unidad").strip()
    purpose = str(unit.get("purpose") or unit.get("description") or "").strip()
    return {
        "unit_title": esc(title),
        "unit_description": esc(purpose),
        "learning_outcomes": render_text_list(objectives),
        "topics": render_topics(unit),
        "theory_sections": render_theory_sections(unit),
        "worked_case": render_worked_examples(unit),
        "guided_activity": render_guided_activities(unit),
        "self_assessment": render_self_assessment(unit),
        "glossary": render_glossary(unit),
        "resources": render_sources(unit),
        "synthesis": esc(render_synthesis(unit)),
    }

def advanced_unit_summaries(root: Path, subject_id: str) -> list[dict[str, Any]]:
    """Build course-outline summaries from validated advanced unit files."""
    canonical_directory = canonical_course_directory(root, subject_id) / "units"
    directory = canonical_directory if canonical_directory.exists() else root / ADVANCED_UNIT_ROOT / subject_id
    if not directory.exists():
        return []
    summaries: list[dict[str, Any]] = []
    for path in sorted(directory.glob("unit-*.json")):
        raw = load_json_object(path)
        data = canonical_unit_to_advanced(root, raw) if directory == canonical_directory else raw
        unit_number = int(data.get("unit", 0))
        if unit_number < 1 or str(data.get("subject_id", "")).strip() != subject_id:
            raise ValueError(f"{path.relative_to(root)}: identidad de unidad inconsistente")
        headings = [
            str(section.get("heading") or section.get("title") or "").strip()
            for section in as_dict_list(data.get("theory_sections"))
        ]
        topics = [heading for heading in headings if heading]
        activities: list[str] = []
        for activity in as_dict_list(data.get("guided_activities")) or as_dict_list(data.get("guided_activity")):
            activities.extend(as_text_list(activity.get("instructions"))[:2])
            activities.extend(activity_task_items(activity)[:2])
        summaries.append({
            "unit": unit_number,
            "title": str(data.get("title") or f"Unidad {unit_number}").strip(),
            "description": str(data.get("purpose") or data.get("description") or "").strip(),
            "topics": [item.rstrip(".") + "." for item in topics],
            "learning_outcomes": as_text_list(data.get("learning_objectives")) or as_text_list(data.get("learning_outcomes")),
            "activities": activities,
            "biomedical_applications": as_text_list(data.get("biomedical_connections")),
        })
    return summaries


def canonical_course_overlay(root: Path, subject_id: str) -> dict[str, Any] | None:
    """Return a generator-compatible course view from the canonical corpus."""
    course_dir = canonical_course_directory(root, subject_id)
    course_path = course_dir / "course.json"
    if not course_path.exists():
        return None
    course = load_json_object(course_path)
    if str(course.get("id") or "").strip() != subject_id:
        raise ValueError(f"{course_path.relative_to(root)}: id no coincide")
    summaries = advanced_unit_summaries(root, subject_id)
    glossary = canonical_records(course_dir, "glossary.json", "entries")
    sources = canonical_records(course_dir, "sources.json", "sources")
    course_assessment_path = course_dir / "assessments" / "course-assessment.json"
    course_assessment = load_json_object(course_assessment_path) if course_assessment_path.exists() else {}

    practical_activities: list[dict[str, str]] = []
    for unit_file in course.get("unit_files", []):
        unit_path = course_dir / str(unit_file)
        if not unit_path.exists():
            continue
        unit = load_json_object(unit_path)
        for activity in as_dict_list(unit.get("activities")):
            practical_activities.append(
                {
                    "title": str(activity.get("title") or "Actividad").strip(),
                    "description": str(activity.get("purpose") or "").strip(),
                    "type": "actividad canónica",
                }
            )

    assessment = []
    for component in as_dict_list(course_assessment.get("assessment_plan")):
        weight = component.get("weight_percent")
        assessment.append(
            {
                "title": str(component.get("component") or component.get("title") or "Evaluación").strip(),
                "description": str(component.get("description") or "").strip(),
                "weight": f"{weight}%" if isinstance(weight, (int, float)) else str(weight or ""),
            }
        )

    prerequisite_statements = [
        str(item.get("statement") or "").strip()
        for item in as_dict_list(course.get("prerequisites"))
        if str(item.get("statement") or "").strip()
    ]
    competency_statements = [
        str(item.get("statement") or "").strip()
        for item in as_dict_list(course.get("competencies"))
        if str(item.get("statement") or "").strip()
    ]
    outcome_statements = [
        str(item.get("statement") or "").strip()
        for item in as_dict_list(course.get("learning_outcomes"))
        if str(item.get("statement") or "").strip()
    ]
    core_source_ids = as_text_list(course.get("core_source_ids"))
    suggested_resources = [
        {
            "title": str(source.get("title") or source_id),
            "organization": str(source.get("organization") or ""),
            "url": str(source.get("url") or ""),
            "type": str(source.get("type") or ""),
            "description": str(source.get("curricular_function") or source.get("description") or ""),
        }
        for source_id in core_source_ids
        if (source := sources.get(source_id)) is not None
        if str(source.get("url") or "").startswith(("https://", "http://"))
    ]
    return {
        "title": str(course.get("title") or subject_id),
        "description": str(course.get("purpose") or ""),
        "level": str(course.get("academic_level") or ""),
        "prerequisites": prerequisite_statements,
        "course_competencies": competency_statements,
        "learning_objectives": outcome_statements,
        "learning_outcomes": outcome_statements,
        "modules": [
            f"{item['title']}: {'; '.join(topic.rstrip('.') for topic in item.get('topics', []))}."
            for item in summaries
        ],
        "detailed_units": summaries,
        "practical_activities": practical_activities,
        "assessment": assessment,
        "key_concepts": [str(entry.get("term") or "") for entry in glossary.values() if entry.get("term")][:24],
        "suggested_resources": suggested_resources,
    }


def merge_advanced_unit_summaries(root: Path, course: dict[str, Any]) -> dict[str, Any]:
    """Merge advanced summaries without dropping existing authored course metadata."""
    subject_id = str(course.get("id") or course.get("subject_id") or "").strip()
    if not subject_id:
        return course
    advanced = advanced_unit_summaries(root, subject_id)
    if not advanced:
        return course

    merged_course = dict(course)
    current = {
        int(item.get("unit", 0)): dict(item)
        for item in course.get("detailed_units", [])
        if isinstance(item, dict) and int(item.get("unit", 0)) > 0
    }
    for summary in advanced:
        number = int(summary["unit"])
        if number in current:
            combined = dict(current[number])
            for key, value in summary.items():
                if value not in (None, "", []):
                    combined[key] = value
            current[number] = combined
        else:
            current[number] = summary
    merged_course["detailed_units"] = [current[number] for number in sorted(current)]
    return merged_course
