#!/usr/bin/env python3
"""Wire the advanced-unit renderer into the static site generator."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_site.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: se esperaba una coincidencia y se encontraron {count}")
    return text.replace(old, new)


def main() -> int:
    text = GENERATOR.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "from typing import Any\n\nROOT = Path(__file__).resolve().parents[1]\n",
        "from typing import Any\n\n"
        "from advanced_unit_renderer import advanced_replacements, load_advanced_unit\n\n"
        "ROOT = Path(__file__).resolve().parents[1]\n",
        "importación del renderer avanzado",
    )

    old_render_page = '''def render_unit_page(template: str, area: dict[str, Any], course: dict[str, Any], unit: dict[str, Any], index: int) -> str:
    units = course.get("detailed_units", [])
    output_path = ROOT / area["id"] / course["id"] / "unidades" / f"unidad-{int(unit['unit']):02d}.html"
    previous_unit = units[index - 1] if index > 0 else None
    next_unit = units[index + 1] if index < len(units) - 1 else None
    previous_link = render_unit_nav_link(int(previous_unit["unit"]), previous_unit["title"], "previous") if previous_unit else ""
    next_link = render_unit_nav_link(int(next_unit["unit"]), next_unit["title"], "next") if next_unit else ""
    frame = pedagogical_frame_for(area["id"], course["id"])
    replacements = {
        "unit_number": str(unit["unit"]),
        "unit_count": str(len(units)),
        "unit_title": escape(unit["title"]),
        "unit_description": escape(unit["description"]),
        "subject_title": escape(course["title"]),
        "subject_id": escape(course["id"]),
        "area_title": escape(area["title"]),
        "css_path": rel_path(output_path, ROOT / "assets" / "css" / "style.css"),
        "editorial_css_path": rel_path(output_path, ROOT / "assets" / "css" / "editorial.css"),
        "home_path": rel_path(output_path, ROOT / "index.html"),
        "area_path": rel_path(output_path, ROOT / area["path"]),
        "subject_path": rel_path(output_path, ROOT / course["path"]),
        "units_index_path": "index.html",
        "previous_unit_link": previous_link,
        "next_unit_link": next_link,
        "learning_outcomes": render_list(unit.get("learning_outcomes", []), "Resultados pendientes."),
        "topics": render_list(unit.get("topics", []), "Temas pendientes."),
        "theory_sections": render_theory_sections(area, course, unit),
        "worked_case": render_worked_case(area, course, unit),
        "guided_activity": render_guided_activity(area, course, unit),
        "self_assessment": render_self_assessment(area, course, unit),
        "glossary": render_glossary(area, course, unit),
        "resources": render_key_value_list(course.get("suggested_resources", []), "Recursos pendientes."),
        "synthesis": escape(
            f"La unidad integra {natural_join(unit.get('topics', []))} mediante {frame['name']}. "
            f"El criterio de cierre es poder explicar, aplicar, comprobar y limitar una conclusión vinculada con "
            f"{clean_topic((unit.get('biomedical_applications') or [course['biomedical_connection']])[0]).lower()}."
        ),
    }
    output = template
    for key, value in replacements.items():
        output = output.replace("{{ " + key + " }}", value)
    return normalize_output(output)
'''

    new_render_page = '''def render_unit_page(template: str, area: dict[str, Any], course: dict[str, Any], unit: dict[str, Any], index: int) -> str:
    units = course.get("detailed_units", [])
    unit_number = int(unit["unit"])
    output_path = ROOT / area["id"] / course["id"] / "unidades" / f"unidad-{unit_number:02d}.html"
    previous_unit = units[index - 1] if index > 0 else None
    next_unit = units[index + 1] if index < len(units) - 1 else None
    previous_link = render_unit_nav_link(int(previous_unit["unit"]), previous_unit["title"], "previous") if previous_unit else ""
    next_link = render_unit_nav_link(int(next_unit["unit"]), next_unit["title"], "next") if next_unit else ""
    frame = pedagogical_frame_for(area["id"], course["id"])
    replacements = {
        "unit_number": str(unit_number),
        "unit_count": str(len(units)),
        "unit_title": escape(unit["title"]),
        "unit_description": escape(unit["description"]),
        "subject_title": escape(course["title"]),
        "subject_id": escape(course["id"]),
        "area_title": escape(area["title"]),
        "css_path": rel_path(output_path, ROOT / "assets" / "css" / "style.css"),
        "editorial_css_path": rel_path(output_path, ROOT / "assets" / "css" / "editorial.css"),
        "home_path": rel_path(output_path, ROOT / "index.html"),
        "area_path": rel_path(output_path, ROOT / area["path"]),
        "subject_path": rel_path(output_path, ROOT / course["path"]),
        "units_index_path": "index.html",
        "previous_unit_link": previous_link,
        "next_unit_link": next_link,
        "learning_outcomes": render_list(unit.get("learning_outcomes", []), "Resultados pendientes."),
        "topics": render_list(unit.get("topics", []), "Temas pendientes."),
        "theory_sections": render_theory_sections(area, course, unit),
        "worked_case": render_worked_case(area, course, unit),
        "guided_activity": render_guided_activity(area, course, unit),
        "self_assessment": render_self_assessment(area, course, unit),
        "glossary": render_glossary(area, course, unit),
        "resources": render_key_value_list(course.get("suggested_resources", []), "Recursos pendientes."),
        "synthesis": escape(
            f"La unidad integra {natural_join(unit.get('topics', []))} mediante {frame['name']}. "
            f"El criterio de cierre es poder explicar, aplicar, comprobar y limitar una conclusión vinculada con "
            f"{clean_topic((unit.get('biomedical_applications') or [course['biomedical_connection']])[0]).lower()}."
        ),
    }
    advanced_unit = load_advanced_unit(ROOT, course["id"], unit_number)
    if advanced_unit is not None:
        replacements.update(advanced_replacements(advanced_unit))
    output = template
    for key, value in replacements.items():
        output = output.replace("{{ " + key + " }}", value)
    return normalize_output(output)
'''
    text = replace_once(text, old_render_page, new_render_page, "render_unit_page")

    old_index_loop = '''    cards = []
    for unit in course.get("detailed_units", []):
        cards.append(
            f'        <a class="link-card unit-index-card" href="unidad-{int(unit["unit"]):02d}.html">'
            f'<span class="course-tag">Unidad {int(unit["unit"])}</span>'
            f'<strong>{escape(unit["title"])}</strong><p>{escape(unit["description"])}</p>'
            '<span class="unit-index-action">Abrir lección →</span></a>'
        )
'''
    new_index_loop = '''    cards = []
    for unit in course.get("detailed_units", []):
        unit_number = int(unit["unit"])
        advanced_unit = load_advanced_unit(ROOT, course["id"], unit_number)
        display_title = advanced_unit.get("title", unit["title"]) if advanced_unit else unit["title"]
        display_description = advanced_unit.get("purpose", unit["description"]) if advanced_unit else unit["description"]
        cards.append(
            f'        <a class="link-card unit-index-card" href="unidad-{unit_number:02d}.html">'
            f'<span class="course-tag">Unidad {unit_number}</span>'
            f'<strong>{escape(display_title)}</strong><p>{escape(display_description)}</p>'
            '<span class="unit-index-action">Abrir lección →</span></a>'
        )
'''
    text = replace_once(text, old_index_loop, new_index_loop, "índice de unidades avanzadas")

    GENERATOR.write_text(text, encoding="utf-8")
    print("Renderer avanzado integrado en scripts/generate_site.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
