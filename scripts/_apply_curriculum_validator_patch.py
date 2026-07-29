#!/usr/bin/env python3
"""Replace the historical all-generated assumption with manifest consistency."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "scripts" / "validate_curriculum.py"
text = path.read_text(encoding="utf-8")
old = '''    if course.get("status") not in {"generated", "complete"}:
        add_error(errors, f"{key} debe quedar en estado generated o complete")
'''
new = '''    try:
        expected_status = generate_site.catalog_editorial_status(subject["id"])
    except (KeyError, TypeError, ValueError) as exc:
        add_error(errors, f"No se pudo resolver el estado editorial de {key}: {exc}")
        return
    if course.get("status") != expected_status:
        add_error(
            errors,
            f"{key} tiene estado público {course.get('status')!r}; "
            f"se esperaba {expected_status!r} según data/catalog_statuses.json",
        )
'''
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected one historical status block, found {count}")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Updated curriculum validator to enforce authoritative editorial states")
