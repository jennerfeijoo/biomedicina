#!/usr/bin/env python3
# Wire catalog discovery into the generator and regenerate public pages.
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"No se encontró el bloque para {label}")
    if text.count(old) != 1:
        raise RuntimeError(f"El bloque para {label} aparece {text.count(old)} veces")
    return text.replace(old, new)


def patch_generator() -> None:
    path = ROOT / "scripts" / "generate_site.py"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        'AREA_TEMPLATE_PATH = ROOT / "templates" / "area.html"\nUNIT_TEMPLATE_PATH',
        'AREA_TEMPLATE_PATH = ROOT / "templates" / "area.html"\n'
        'CATALOG_TEMPLATE_PATH = ROOT / "templates" / "catalogo.html"\n'
        'TRACKS_PATH = ROOT / "data" / "tracks.json"\n'
        'UNIT_TEMPLATE_PATH',
        "constantes del catálogo",
    )

    validation_anchor = "\ndef validate_unit_templates(unit_template: str, units_template: str) -> None:\n"
    validation_block = '''
def validate_catalog_template(template: str) -> None:
    required = {
        "subject_count", "area_count", "track_count", "css_path", "editorial_css_path",
        "catalog_css_path", "catalog_js_path", "home_path", "area_options",
        "track_options", "track_cards", "subject_cards",
    }
    missing = [key for key in required if "{{ " + key + " }}" not in template]
    if missing:
        raise ValueError("La plantilla del catálogo no contiene: " + ", ".join(sorted(missing)))


'''
    if "def validate_catalog_template" not in text:
        text = text.replace(validation_anchor, "\n" + validation_block + validation_anchor.lstrip("\n"), 1)

    start = text.index("def render_area(template: str, area: dict[str, Any]) -> str:")
    end = text.index("\ndef iter_subjects", start)
    replacement = r'''def load_tracks_config() -> list[dict[str, Any]]:
    data = load_json(TRACKS_PATH)
    tracks = data.get("tracks", [])
    if not isinstance(tracks, list):
        raise ValueError("data/tracks.json debe contener una lista tracks")
    return tracks


def track_ids_for_subject(subject_id: str, tracks: list[dict[str, Any]]) -> list[str]:
    return [str(track["id"]) for track in tracks if subject_id in track.get("subjects", [])]


def render_track_options(tracks: list[dict[str, Any]]) -> str:
    return "\n".join(
        f'            <option value="{html.escape(str(track["id"]), quote=True)}">'
        f'{escape(str(track["title"]))}</option>'
        for track in tracks
    )


def render_course_card(
    output_path: Path,
    area: dict[str, Any],
    subject: dict[str, Any],
    tracks: list[dict[str, Any]],
) -> str:
    complete_subject = merge_subject_overlay(area, subject)
    href = rel_path(output_path, ROOT / subject["path"])
    title = str(complete_subject.get("title", subject["title"]))
    description = str(complete_subject.get("description", subject["description"]))
    connection = str(complete_subject.get("biomedical_connection", ""))
    track_ids = track_ids_for_subject(subject["id"], tracks)
    track_lookup = {str(track["id"]): str(track["title"]) for track in tracks}
    track_titles = [track_lookup[item] for item in track_ids if item in track_lookup]
    searchable = " ".join([title, description, connection, area["title"], *track_titles])
    chips = [f'<span class="catalog-chip">{escape(area["title"])}</span>']
    chips.extend(f'<span class="catalog-chip">{escape(label)}</span>' for label in track_titles[:2])
    if len(track_titles) > 2:
        chips.append(f'<span class="catalog-chip">+{len(track_titles) - 2} rutas</span>')
    return (
        f'      <a class="link-card course-card" href="{href}" data-course-card '
        f'data-subject="{html.escape(subject["id"], quote=True)}" '
        f'data-area="{html.escape(area["id"], quote=True)}" '
        f'data-tracks="{html.escape(" ".join(track_ids), quote=True)}" '
        f'data-search="{html.escape(searchable, quote=True)}">\n'
        f"        <strong>{escape(title)}</strong>\n"
        f"        <p>{escape(description)}</p>\n"
        f'        <span class="course-card-meta">{"".join(chips)}</span>\n'
        "      </a>"
    )


def render_area(template: str, area: dict[str, Any]) -> str:
    output_path = ROOT / area["path"]
    tracks = load_tracks_config()
    subject_ids = {subject["id"] for subject in area.get("subjects", [])}
    area_tracks = [
        track for track in tracks
        if subject_ids.intersection(set(track.get("subjects", [])))
    ]
    cards = [
        render_course_card(output_path, area, subject, tracks)
        for subject in area.get("subjects", [])
    ]
    replacements = {
        "area_title": escape(area["title"]),
        "area_description": escape(area["description"]),
        "css_path": rel_path(output_path, ROOT / "assets" / "css" / "style.css"),
        "editorial_css_path": rel_path(output_path, ROOT / "assets" / "css" / "editorial.css"),
        "catalog_css_path": rel_path(output_path, ROOT / "assets" / "css" / "catalog.css"),
        "catalog_js_path": rel_path(output_path, ROOT / "assets" / "js" / "catalog.js"),
        "catalog_path": rel_path(output_path, ROOT / "catalogo" / "index.html"),
        "home_path": rel_path(output_path, ROOT / "index.html"),
        "subject_count": str(len(area.get("subjects", []))),
        "track_options": render_track_options(area_tracks),
        "subject_cards": "\n".join(cards),
    }
    html_output = template
    for key, value in replacements.items():
        html_output = html_output.replace("{{ " + key + " }}", value)
    return html_output


def render_catalog(template: str, data: dict[str, Any]) -> str:
    output_path = ROOT / "catalogo" / "index.html"
    tracks = load_tracks_config()
    cards: list[str] = []
    subject_count = 0
    for area in data.get("areas", []):
        for subject in area.get("subjects", []):
            cards.append(render_course_card(output_path, area, subject, tracks))
            subject_count += 1

    area_options = "\n".join(
        f'            <option value="{html.escape(area["id"], quote=True)}">'
        f'{escape(area["title"])}</option>'
        for area in data.get("areas", [])
    )
    track_cards = "\n".join(
        (
            f'        <a class="track-card" href="?track={html.escape(str(track["id"]), quote=True)}#asignaturas">'
            f'<strong>{escape(str(track["title"]))}</strong>'
            f'<p>{escape(str(track["description"]))}</p>'
            f'<span>{len(track.get("subjects", []))} asignaturas relacionadas →</span></a>'
        )
        for track in tracks
    )
    replacements = {
        "subject_count": str(subject_count),
        "area_count": str(len(data.get("areas", []))),
        "track_count": str(len(tracks)),
        "css_path": rel_path(output_path, ROOT / "assets" / "css" / "style.css"),
        "editorial_css_path": rel_path(output_path, ROOT / "assets" / "css" / "editorial.css"),
        "catalog_css_path": rel_path(output_path, ROOT / "assets" / "css" / "catalog.css"),
        "catalog_js_path": rel_path(output_path, ROOT / "assets" / "js" / "catalog.js"),
        "home_path": rel_path(output_path, ROOT / "index.html"),
        "area_options": area_options,
        "track_options": render_track_options(tracks),
        "track_cards": track_cards,
        "subject_cards": "\n".join(cards),
    }
    html_output = template
    for key, value in replacements.items():
        html_output = html_output.replace("{{ " + key + " }}", value)
    return normalize_output(html_output)


'''
    text = text[:start] + replacement + text[end:]

    text = replace_once(
        text,
        '    area_template = load_template(AREA_TEMPLATE_PATH)\n'
        '    unit_template = load_template(UNIT_TEMPLATE_PATH) if with_units else ""\n'
        '    units_template = load_template(UNITS_TEMPLATE_PATH) if with_units else ""\n'
        '    validate_template(template)\n'
        '    validate_area_template(area_template)\n',
        '    area_template = load_template(AREA_TEMPLATE_PATH)\n'
        '    catalog_template = load_template(CATALOG_TEMPLATE_PATH)\n'
        '    unit_template = load_template(UNIT_TEMPLATE_PATH) if with_units else ""\n'
        '    units_template = load_template(UNITS_TEMPLATE_PATH) if with_units else ""\n'
        '    validate_template(template)\n'
        '    validate_area_template(area_template)\n'
        '    validate_catalog_template(catalog_template)\n',
        "carga de plantilla del catálogo",
    )

    text = replace_once(
        text,
        '        "generated_areas": 0,\n',
        '        "generated_areas": 0,\n'
        '        "generated_catalog": 0,\n',
        "resumen generado",
    )
    text = replace_once(
        text,
        '        "would_generate_areas": 0,\n',
        '        "would_generate_areas": 0,\n'
        '        "would_generate_catalog": 0,\n',
        "resumen dry-run",
    )

    catalog_generation = r'''
        catalog_path = ROOT / "catalogo" / "index.html"
        if catalog_path.exists() and not force:
            summary["skipped_existing_areas"] += 1
        else:
            rendered_catalog = render_catalog(catalog_template, data)
            if dry_run:
                print(f"[dry-run] generaría catálogo: {catalog_path.relative_to(ROOT)}")
                summary["would_generate_catalog"] += 1
            else:
                catalog_path.parent.mkdir(parents=True, exist_ok=True)
                catalog_path.write_text(rendered_catalog, encoding="utf-8")
                print(f"[ok] generado catálogo: {catalog_path.relative_to(ROOT)}")
                summary["generated_catalog"] += 1

'''
    marker = "\n    return summary\n\n\ndef main() -> int:"
    text = replace_once(
        text,
        marker,
        catalog_generation + "    return summary\n\n\ndef main() -> int:",
        "generación del catálogo",
    )
    path.write_text(text, encoding="utf-8")


def patch_homepage() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    if 'href="catalogo/index.html">Catálogo' not in text:
        text = text.replace(
            '<li><a href="#areas">Áreas clave</a></li>',
            '<li><a href="#areas">Áreas clave</a></li>\n'
            '            <li><a href="catalogo/index.html">Catálogo</a></li>',
            1,
        )
    if 'Explorar las 84 asignaturas' not in text:
        text = text.replace(
            '        </ul>\n      </div>\n      <div class="hero-visual"',
            '        </ul>\n'
            '        <div class="page-actions"><a class="btn-link" href="catalogo/index.html">'
            'Explorar las 84 asignaturas</a></div>\n'
            '      </div>\n      <div class="hero-visual"',
            1,
        )
    path.write_text(text, encoding="utf-8")


def patch_quality_workflow() -> None:
    path = ROOT / ".github" / "workflows" / "citonauta-quality.yml"
    text = path.read_text(encoding="utf-8")
    if "Validate catalog discovery" not in text:
        anchor = (
            "      - name: Enforce self-paced learning model\n"
            "        run: python scripts/validate_self_paced_model.py\n"
        )
        replacement = (
            anchor
            + "\n"
            + "      - name: Validate catalog discovery\n"
            + "        run: python scripts/validate_catalog.py\n"
        )
        text = replace_once(text, anchor, replacement, "quality gate del catálogo")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    patch_generator()
    patch_homepage()
    patch_quality_workflow()
    subprocess.run([sys.executable, "scripts/generate_site.py", "--force"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/validate_catalog.py"], cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
