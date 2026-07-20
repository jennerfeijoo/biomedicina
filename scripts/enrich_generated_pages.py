#!/usr/bin/env python3
"""Inserta contenido pedagógico enriquecido en el HTML generado.

El generador base mantiene compatibilidad con los overlays antiguos. Este postprocesador
solo actúa sobre archivos que contienen generation_metadata.autonomous_agent=true y es
idempotente gracias a marcadores HTML explícitos.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = ROOT / "data" / "citonauta_curriculum.json"
OVERLAYS_DIR = ROOT / "data" / "subjects"
UNIT_MARKER_RE = re.compile(
    r"\n?\s*<!-- agent-unit-enrichment:start -->.*?<!-- agent-unit-enrichment:end -->\n?",
    re.DOTALL,
)
SOURCE_MARKER_RE = re.compile(
    r"\n?\s*<!-- agent-sources:start -->.*?<!-- agent-sources:end -->\n?",
    re.DOTALL,
)
ARTICLE_RE = re.compile(r"<article class=\"course-unit\">.*?</article>", re.DOTALL)
RESOURCE_SECTION_RE = re.compile(
    r"(<section id=\"recursos\" class=\"section\">.*?)(\n\s*</section>)",
    re.DOTALL,
)


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def render_list(items: list[Any], ordered: bool = False) -> str:
    if not items:
        return ""
    tag = "ol" if ordered else "ul"
    body = "\n".join(f"              <li>{esc(item)}</li>" for item in items)
    return f"            <{tag}>\n{body}\n            </{tag}>"


def render_explanation(block: dict[str, Any]) -> str:
    paragraphs = "\n".join(
        f"            <p>{esc(paragraph)}</p>" for paragraph in block.get("paragraphs", [])
    )
    points = render_list(block.get("key_points", []))
    return (
        "          <section class=\"concept-block\">\n"
        f"            <h4>{esc(block.get('title', 'Desarrollo conceptual'))}</h4>\n"
        f"{paragraphs}\n"
        f"{points}\n"
        "          </section>"
    )


def render_example(example: dict[str, Any]) -> str:
    steps = render_list(example.get("reasoning_steps", []), ordered=True)
    return (
        "          <section class=\"worked-example\">\n"
        f"            <h4>{esc(example.get('title', 'Ejemplo guiado'))}</h4>\n"
        f"            <p><strong>Situación:</strong> {esc(example.get('scenario'))}</p>\n"
        f"{steps}\n"
        f"            <p><strong>Conclusión:</strong> {esc(example.get('conclusion'))}</p>\n"
        "          </section>"
    )


def render_self_check(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    details = []
    for item in items:
        details.append(
            "            <details>\n"
            f"              <summary>{esc(item.get('question', 'Pregunta'))}</summary>\n"
            f"              <p>{esc(item.get('answer'))}</p>\n"
            "            </details>"
        )
    return (
        "          <section class=\"self-check\">\n"
        "            <h4>Comprueba tu aprendizaje</h4>\n"
        + "\n".join(details)
        + "\n          </section>"
    )


def render_unit_enrichment(unit: dict[str, Any]) -> str:
    sections = [render_explanation(block) for block in unit.get("explanations", [])]
    sections.extend(render_example(item) for item in unit.get("worked_examples", []))
    misconceptions = unit.get("common_misconceptions", [])
    if misconceptions:
        sections.append(
            "          <section class=\"misconceptions\">\n"
            "            <h4>Errores frecuentes</h4>\n"
            f"{render_list(misconceptions)}\n"
            "          </section>"
        )
    self_check = render_self_check(unit.get("self_check", []))
    if self_check:
        sections.append(self_check)
    return (
        "\n        <!-- agent-unit-enrichment:start -->\n"
        "        <div class=\"unit-enrichment\">\n"
        + "\n".join(sections)
        + "\n        </div>\n"
        "        <!-- agent-unit-enrichment:end -->\n"
    )


def render_sources(sources: list[dict[str, Any]]) -> str:
    if not sources:
        return ""
    items = []
    for source in sources:
        title = esc(source.get("title") or source.get("url"))
        url = esc(source.get("url"))
        meta = " · ".join(
            str(value) for value in (source.get("year"), source.get("type")) if value
        )
        meta_html = f" <small>({esc(meta)})</small>" if meta else ""
        items.append(
            f'        <li><a class="resource-link" href="{url}">{title}</a>{meta_html}</li>'
        )
    return (
        "\n      <!-- agent-sources:start -->\n"
        "      <div class=\"agent-sources\">\n"
        "        <h3>Fuentes consultadas para esta edición</h3>\n"
        "        <ol>\n"
        + "\n".join(items)
        + "\n        </ol>\n"
        "      </div>\n"
        "      <!-- agent-sources:end -->"
    )


def enrich_html(original: str, overlay: dict[str, Any]) -> str:
    cleaned = UNIT_MARKER_RE.sub("\n", original)
    cleaned = SOURCE_MARKER_RE.sub("\n", cleaned)
    units = overlay.get("detailed_units", [])
    article_matches = list(ARTICLE_RE.finditer(cleaned))
    if len(article_matches) != len(units):
        raise ValueError(
            f"El HTML contiene {len(article_matches)} unidades y el overlay {len(units)}"
        )

    pieces: list[str] = []
    cursor = 0
    for match, unit in zip(article_matches, units, strict=True):
        article = match.group(0)
        anchor = "        <h4>Temas</h4>"
        if anchor not in article:
            raise ValueError("No se encontró el ancla <h4>Temas</h4> en una unidad")
        article = article.replace(anchor, render_unit_enrichment(unit) + anchor, 1)
        pieces.append(cleaned[cursor : match.start()])
        pieces.append(article)
        cursor = match.end()
    pieces.append(cleaned[cursor:])
    enriched = "".join(pieces)

    sources_html = render_sources(overlay.get("sources_used", []))
    if sources_html:
        enriched, count = RESOURCE_SECTION_RE.subn(
            lambda match: match.group(1) + sources_html + match.group(2),
            enriched,
            count=1,
        )
        if count != 1:
            raise ValueError("No se encontró la sección de recursos en el HTML")
    return "\n".join(line.rstrip() for line in enriched.splitlines()).rstrip() + "\n"


def catalog_paths() -> dict[str, tuple[str, str]]:
    curriculum = json.loads(CURRICULUM_PATH.read_text(encoding="utf-8"))
    result: dict[str, tuple[str, str]] = {}
    for area in curriculum.get("areas", []):
        for subject in area.get("subjects", []):
            result[subject["id"]] = (area["id"], subject["path"])
    return result


def process(subject_ids: set[str], check: bool) -> tuple[int, list[str]]:
    paths = catalog_paths()
    changed = 0
    errors: list[str] = []
    for subject_id, (area_id, html_relative) in paths.items():
        if subject_ids and subject_id not in subject_ids:
            continue
        overlay_path = OVERLAYS_DIR / area_id / f"{subject_id}.json"
        if not overlay_path.exists():
            continue
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        if not (overlay.get("generation_metadata") or {}).get("autonomous_agent"):
            continue
        html_path = ROOT / html_relative
        try:
            original = html_path.read_text(encoding="utf-8")
            enriched = enrich_html(original, overlay)
            if enriched != original:
                changed += 1
                if not check:
                    html_path.write_text(enriched, encoding="utf-8")
                    print(f"[ok] enriquecido: {html_relative}")
                else:
                    errors.append(f"HTML enriquecido desactualizado: {html_relative}")
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"{subject_id}: {exc}")
    return changed, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Enriquece HTML generado con contenido del agente.")
    parser.add_argument("--subject", action="append", default=[], help="ID de asignatura; repetible.")
    parser.add_argument("--check", action="store_true", help="No escribe; falla si el HTML está desactualizado.")
    args = parser.parse_args()
    changed, errors = process(set(args.subject), args.check)
    if errors:
        print("Errores de enriquecimiento:\n")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Enriquecimiento completado. Páginas modificadas: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
