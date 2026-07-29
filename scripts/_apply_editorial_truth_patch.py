#!/usr/bin/env python3
"""Apply the one-time editorial-state migration, then remove this helper in CI."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "generate_site.py"

text = PATH.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one occurrence, found {count}")
    text = text.replace(old, new, 1)


replace_once(
    'OUTLINES_PATH = ROOT / "data" / "course_outlines.json"\n',
    'OUTLINES_PATH = ROOT / "data" / "course_outlines.json"\n'
    'CATALOG_STATUSES_PATH = ROOT / "data" / "catalog_statuses.json"\n',
    "catalog statuses path",
)

replace_once(
    '    "placeholder": "Contenido pendiente",\n',
    '    "placeholder": "Contenido de respaldo · desarrollo académico pendiente",\n',
    "placeholder label",
)

replace_once(
    '    "unit_number", "unit_count", "unit_title", "unit_description",\n'
    '    "subject_title", "subject_id", "area_title", "css_path", "editorial_css_path",\n',
    '    "unit_number", "unit_count", "unit_title", "unit_description",\n'
    '    "unit_status", "unit_status_label",\n'
    '    "subject_title", "subject_id", "area_title", "css_path", "editorial_css_path",\n',
    "unit template keys",
)

replace_once(
    '        "status": "generated",\n        "level": (\n',
    '        "status": "placeholder",\n        "level": (\n',
    "fallback synthesized status",
)

marker = 'def subject_overlay_path(area_id: str, subject_id: str) -> Path:\n'
helpers = '''@cache
def load_catalog_statuses() -> dict[str, Any]:
    """Load the authoritative editorial manifest."""
    return load_json(CATALOG_STATUSES_PATH)


def catalog_editorial_status(subject_id: str) -> str:
    """Map catalog maturity to the public page status used by the generator."""
    statuses = load_catalog_statuses()
    memberships = {
        "complete": subject_id in set(statuses.get("complete", [])),
        "generated": subject_id in set(statuses.get("developed", [])),
        "placeholder": subject_id in set(statuses.get("pending", [])),
    }
    selected = [status for status, present in memberships.items() if present]
    if len(selected) != 1:
        raise ValueError(
            f"{subject_id}: expected exactly one editorial state in {CATALOG_STATUSES_PATH.relative_to(ROOT)}; "
            f"found {selected}"
        )
    return selected[0]


def unit_status_label(status: str) -> str:
    """Return an honest unit-level label derived from course maturity."""
    if status == "complete":
        return "Lección revisada por especialista"
    if status in {"generated", "review"}:
        return "Lección desarrollada · revisión experta pendiente"
    return "Contenido de respaldo · desarrollo académico pendiente"


'''
replace_once(marker, helpers + marker, "editorial status helpers")

replace_once(
    '    if not overlay_path.exists():\n'
    '        merged = merge_advanced_unit_summaries(ROOT, merged)\n'
    '        merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])\n'
    '        return merged\n',
    '    if not overlay_path.exists():\n'
    '        merged = merge_advanced_unit_summaries(ROOT, merged)\n'
    '        merged["status"] = catalog_editorial_status(subject["id"])\n'
    '        merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])\n'
    '        return merged\n',
    "fallback overlay status",
)

replace_once(
    '    merged = merge_advanced_unit_summaries(ROOT, merged)\n'
    '    if merged.get("status") != "complete":\n'
    '        merged["status"] = "generated"\n'
    '    merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])\n'
    '    return merged\n',
    '    merged = merge_advanced_unit_summaries(ROOT, merged)\n'
    '    merged["status"] = catalog_editorial_status(subject["id"])\n'
    '    merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])\n'
    '    return merged\n',
    "overlay status enforcement",
)

replace_once(
    '        "subject_title": escape(course["title"]),\n'
    '        "subject_id": escape(course["id"]),\n'
    '        "area_title": escape(area["title"]),\n',
    '        "subject_title": escape(course["title"]),\n'
    '        "subject_id": escape(course["id"]),\n'
    '        "unit_status": escape(course.get("status", "placeholder")),\n'
    '        "unit_status_label": escape(unit_status_label(course.get("status", "placeholder"))),\n'
    '        "area_title": escape(area["title"]),\n',
    "unit status replacements",
)

if text == original:
    raise SystemExit("no generator changes applied")
PATH.write_text(text, encoding="utf-8")

validator_path = ROOT / "scripts" / "validate_pilot_foundations.py"
validator = validator_path.read_text(encoding="utf-8")
old = '["foundation_review", "Unidades desarrolladas en este bloque: ninguna", "Gates antes de complete", "Riesgos abiertos"]'
new = '["foundation_review", "Unidades desarrolladas en este bloque", "ninguna", "Gates antes de complete", "Riesgos abiertos"]'
if validator.count(old) != 1:
    raise SystemExit(f"readiness validation marker: expected one occurrence, found {validator.count(old)}")
validator_path.write_text(validator.replace(old, new, 1), encoding="utf-8")

print("Applied authoritative editorial state migration")
