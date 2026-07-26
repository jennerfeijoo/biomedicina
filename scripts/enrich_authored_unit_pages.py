#!/usr/bin/env python3
"""Enrich registered authored unit pages without replacing their manual prose.

Only missing pedagogical blocks are added, using text already present in the
validated advanced unit JSON. Explicit markers make the transformation
idempotent and auditable.
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
OVERRIDES_PATH = ROOT / "data" / "authored_unit_overrides.json"
ADVANCED_ROOT = ROOT / "data" / "generated_units"
START_MARKER = "<!-- authored-unit-enrichment:start -->"
END_MARKER = "<!-- authored-unit-enrichment:end -->"
BLOCK_RE = re.compile(
    rf"\s*{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}\s*",
    re.DOTALL,
)


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)}: la raíz debe ser un objeto")
    return data


def course_directories() -> dict[str, Path]:
    curriculum = load_json(CURRICULUM_PATH)
    result: dict[str, Path] = {}
    for area in curriculum.get("areas", []):
        for subject in area.get("subjects", []):
            subject_id = str(subject.get("id", "")).strip()
            course_path = str(subject.get("path", "")).strip()
            if subject_id and course_path:
                result[subject_id] = (ROOT / course_path).parent
    return result


def override_keys() -> list[tuple[str, int]]:
    data = load_json(OVERRIDES_PATH)
    keys: list[tuple[str, int]] = []
    for entry in data.get("overrides", []):
        if not isinstance(entry, dict):
            continue
        subject_id = str(entry.get("subject_id", "")).strip()
        for raw_unit in entry.get("units", []):
            keys.append((subject_id, int(raw_unit)))
    return keys


def render_self_assessment(unit: dict[str, Any]) -> str:
    questions = unit.get("self_assessment")
    if not isinstance(questions, list) or not questions:
        return ""
    panels: list[str] = []
    for number, item in enumerate(questions, start=1):
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip()
        reasoning = str(item.get("reasoning") or item.get("explanation") or "").strip()
        if not question:
            continue
        body = f"<p><strong>Respuesta:</strong> {esc(answer)}</p>" if answer else ""
        if reasoning:
            body += f"<p><strong>Razonamiento:</strong> {esc(reasoning)}</p>"
        panels.append(
            f'<details class="answer-panel"><summary>{number}. {esc(question)}</summary>{body}</details>'
        )
    if not panels:
        return ""
    return (
        f"\n{START_MARKER}\n"
        '<section class="section authored-self-assessment">'
        '<div class="section-header"><h2>Autoevaluación con respuestas</h2>'
        '<p>Las respuestas proceden del contenido avanzado validado de esta unidad.</p></div>'
        '<div class="assessment-panels">'
        + "".join(panels)
        + "</div></section>\n"
        f"{END_MARKER}\n"
    )


def expected_page(original: str, unit: dict[str, Any]) -> str:
    cleaned = BLOCK_RE.sub("\n", original)
    if 'data-authored-unit="true"' not in cleaned:
        cleaned = cleaned.replace(
            '<main id="contenido"',
            '<main id="contenido" data-authored-unit="true"',
            1,
        )
    folded = cleaned.casefold()
    has_self_assessment = "autoevaluación" in folded or "autoevaluacion" in folded
    if not has_self_assessment:
        block = render_self_assessment(unit)
        if not block:
            raise ValueError("la página carece de autoevaluación y el JSON no aporta preguntas")
        if "</main>" not in cleaned:
            raise ValueError("no se encontró el cierre </main>")
        cleaned = cleaned.replace("</main>", block + "</main>", 1)
    return "\n".join(line.rstrip() for line in cleaned.splitlines()).rstrip() + "\n"


def process(check: bool) -> tuple[int, list[str]]:
    directories = course_directories()
    changed = 0
    errors: list[str] = []
    for subject_id, unit_number in override_keys():
        course_dir = directories.get(subject_id)
        if course_dir is None:
            errors.append(f"{subject_id}: no existe ruta curricular")
            continue
        page_path = course_dir / "unidades" / f"unidad-{unit_number:02d}.html"
        unit_path = ADVANCED_ROOT / subject_id / f"unit-{unit_number:02d}.json"
        if not page_path.exists() or not unit_path.exists():
            errors.append(f"{subject_id}/unidad-{unit_number:02d}: falta HTML o JSON avanzado")
            continue
        try:
            original = page_path.read_text(encoding="utf-8")
            unit = load_json(unit_path)
            expected = expected_page(original, unit)
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
            errors.append(f"{page_path.relative_to(ROOT)}: {error}")
            continue
        if expected != original:
            changed += 1
            if check:
                errors.append(f"página autoral desactualizada: {page_path.relative_to(ROOT)}")
            else:
                page_path.write_text(expected, encoding="utf-8")
                print(f"[ok] enriquecida: {page_path.relative_to(ROOT)}")
    return changed, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Sincroniza bloques faltantes en páginas autorales registradas.")
    parser.add_argument("--check", action="store_true", help="No escribe y falla si hay deriva.")
    args = parser.parse_args()
    changed, errors = process(args.check)
    if errors:
        print("Errores de sincronización autoral:\n")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Sincronización autoral completada. Páginas modificadas: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
