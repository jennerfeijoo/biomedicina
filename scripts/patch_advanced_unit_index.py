#!/usr/bin/env python3
"""Expose every validated advanced unit in course summaries and navigation."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts" / "advanced_unit_renderer.py"
GENERATOR = ROOT / "scripts" / "generate_site.py"

HELPER = r'''

def advanced_unit_summaries(root: Path, subject_id: str) -> list[dict[str, Any]]:
    """Build course-outline summaries from validated advanced unit files."""
    directory = root / ADVANCED_UNIT_ROOT / subject_id
    if not directory.exists():
        return []
    summaries: list[dict[str, Any]] = []
    for path in sorted(directory.glob("unit-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{path.relative_to(root)}: la raíz debe ser un objeto JSON")
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
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: se esperaba una coincidencia y se encontraron {count}")
    return text.replace(old, new)


def patch_renderer() -> None:
    text = RENDERER.read_text(encoding="utf-8")
    if "def advanced_unit_summaries(" not in text:
        text = text.rstrip() + HELPER + "\n"
    text = text.replace(
        'description = str(equation.get("description") or equation.get("label") or "").strip()',
        'description = str(equation.get("description") or equation.get("label") or equation.get("meaning") or "").strip()',
    )
    RENDERER.write_text(text, encoding="utf-8")


def patch_generator() -> None:
    text = GENERATOR.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "from advanced_unit_renderer import advanced_replacements, load_advanced_unit\n",
        "from advanced_unit_renderer import (\n"
        "    advanced_replacements,\n"
        "    load_advanced_unit,\n"
        "    merge_advanced_unit_summaries,\n"
        ")\n",
        "importación de resúmenes avanzados",
    )
    text = replace_once(
        text,
        '''    if not overlay_path.exists():
        merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])
        return merged
''',
        '''    if not overlay_path.exists():
        merged = merge_advanced_unit_summaries(ROOT, merged)
        merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])
        return merged
''',
        "unión avanzada sin overlay",
    )
    text = replace_once(
        text,
        '''    if merged.get("status") != "complete":
        merged["status"] = "generated"
    merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])
    return merged
''',
        '''    merged = merge_advanced_unit_summaries(ROOT, merged)
    if merged.get("status") != "complete":
        merged["status"] = "generated"
    merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])
    return merged
''',
        "unión avanzada con overlay",
    )
    GENERATOR.write_text(text, encoding="utf-8")


def main() -> int:
    patch_renderer()
    patch_generator()
    print("Índices de unidades avanzadas integrados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
