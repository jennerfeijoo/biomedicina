#!/usr/bin/env python3
"""Genera una vista previa temporal de páginas y verifica que no queden placeholders.

No escribe dentro del árbol público del sitio. Usa un directorio temporal para renderizar
una muestra de páginas con el generador y revisar variables sin reemplazar.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import generate_site

ROOT = Path(__file__).resolve().parents[1]
UNRESOLVED_MARKERS = ("{{ ", " }}")


def check_preview(limit: int) -> list[str]:
    errors: list[str] = []
    data = generate_site.load_json(generate_site.DATA_PATH)
    template = generate_site.load_template(generate_site.TEMPLATE_PATH)
    generate_site.validate_template(template)

    rendered_count = 0
    with tempfile.TemporaryDirectory(prefix="citonauta-preview-") as tmpdir:
        preview_root = Path(tmpdir)
        for area, subjects, index, subject in generate_site.iter_subjects(data):
            if rendered_count >= limit:
                break
            rendered = generate_site.render_subject(template, area, subject, subjects, index)
            preview_path = preview_root / subject["path"]
            preview_path.parent.mkdir(parents=True, exist_ok=True)
            preview_path.write_text(rendered, encoding="utf-8")
            rendered_count += 1

            if any(marker in rendered for marker in UNRESOLVED_MARKERS):
                errors.append(f"Variables sin reemplazar en vista previa: {subject['path']}")
            if "editorial.css" not in rendered:
                errors.append(f"Falta editorial.css en vista previa: {subject['path']}")
            if "style.css" not in rendered:
                errors.append(f"Falta style.css en vista previa: {subject['path']}")

    if rendered_count == 0:
        errors.append("No se generó ninguna página de vista previa")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica una muestra de páginas generadas en un directorio temporal.")
    parser.add_argument("--limit", type=int, default=8, help="Número máximo de asignaturas a renderizar temporalmente.")
    args = parser.parse_args()

    errors = check_preview(args.limit)
    if errors:
        print("Errores en vista previa generada:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Vista previa generada correctamente.")
    print(f"- páginas temporales revisadas: {args.limit}")
    print("- resultado: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
