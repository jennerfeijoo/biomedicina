#!/usr/bin/env python3
"""Corrige y audita el renderizado de conexiones biomédicas estructuradas.

Las unidades avanzadas pueden declarar ``biomedical_connections`` como cadenas o
como objetos con ``topic`` y ``connection``. La capa pública debe conservar esa
estructura en JSON y convertirla en texto legible únicamente al renderizar.

El script aplica de forma idempotente dos correcciones de renderer, enumera las
asignaturas afectadas y bloquea artefactos como ``[object Object]`` o la
representación Python de diccionarios en HTML público.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS_PATH = ROOT / "assets" / "js" / "generated-units.js"
PY_RENDERER_PATH = ROOT / "scripts" / "advanced_unit_renderer.py"
UNIT_ROOT = ROOT / "data" / "generated_units"

JS_OLD = '''  function appendList(parent, items, className = "") {
    const list = element("ul", className);
    for (const item of items || []) list.appendChild(element("li", "", item));
    parent.appendChild(list);
    return list;
  }
'''

JS_NEW = '''  function listItemText(item) {
    if (item === null || item === undefined) return "";
    if (typeof item !== "object") return String(item).trim();

    const topic = String(item.topic || item.title || item.label || "").trim();
    const connection = String(
      item.connection || item.description || item.text || item.value || ""
    ).trim();
    if (topic && connection) return `${topic}: ${connection}`;
    return topic || connection;
  }

  function appendList(parent, items, className = "") {
    const list = element("ul", className);
    for (const item of items || []) {
      const text = listItemText(item);
      if (text) list.appendChild(element("li", "", text));
    }
    parent.appendChild(list);
    return list;
  }
'''

PY_HELPER_OLD = '''def as_text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]
'''

PY_HELPER_NEW = '''def as_text_list(value: Any) -> list[str]:
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
'''

PY_SYNTHESIS_OLD = '''def render_synthesis(unit: dict[str, Any]) -> str:
    purpose = str(unit.get("purpose") or "").strip()
    connections = as_text_list(unit.get("biomedical_connections"))
    notice = str(unit.get("editorial_notice") or "").strip()
'''

PY_SYNTHESIS_NEW = '''def render_synthesis(unit: dict[str, Any]) -> str:
    purpose = str(unit.get("purpose") or "").strip()
    connections = as_biomedical_connection_list(unit.get("biomedical_connections"))
    notice = str(unit.get("editorial_notice") or "").strip()
'''

BAD_PUBLIC_MARKERS = (
    "[object Object]",
    "{&#x27;topic&#x27;:",
    "{&#39;topic&#39;:",
    "{'topic':",
    "{&quot;topic&quot;:",
)


def replace_once(path: Path, old: str, new: str, marker: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    if old not in text:
        raise RuntimeError(f"{path.relative_to(ROOT)}: no se encontró el bloque esperado para aplicar la corrección")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def apply_fixes() -> list[str]:
    changed: list[str] = []
    if replace_once(JS_PATH, JS_OLD, JS_NEW, "function listItemText(item)"):
        changed.append(JS_PATH.relative_to(ROOT).as_posix())
    if replace_once(PY_RENDERER_PATH, PY_HELPER_OLD, PY_HELPER_NEW, "def as_biomedical_connection_list"):
        changed.append(PY_RENDERER_PATH.relative_to(ROOT).as_posix())
    text = PY_RENDERER_PATH.read_text(encoding="utf-8")
    if PY_SYNTHESIS_NEW not in text:
        if PY_SYNTHESIS_OLD not in text:
            raise RuntimeError("scripts/advanced_unit_renderer.py: no se encontró render_synthesis esperado")
        PY_RENDERER_PATH.write_text(text.replace(PY_SYNTHESIS_OLD, PY_SYNTHESIS_NEW, 1), encoding="utf-8")
        if PY_RENDERER_PATH.relative_to(ROOT).as_posix() not in changed:
            changed.append(PY_RENDERER_PATH.relative_to(ROOT).as_posix())
    return changed


def structured_subjects() -> list[str]:
    subjects: set[str] = set()
    if not UNIT_ROOT.exists():
        return []
    for path in UNIT_ROOT.glob("*/unit-*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        connections = data.get("biomedical_connections")
        if isinstance(connections, list) and any(isinstance(item, dict) for item in connections):
            subjects.add(str(data.get("subject_id") or path.parent.name))
    return sorted(subjects)


def source_errors() -> list[str]:
    errors: list[str] = []
    js = JS_PATH.read_text(encoding="utf-8")
    renderer = PY_RENDERER_PATH.read_text(encoding="utf-8")
    if "function listItemText(item)" not in js:
        errors.append("generated-units.js no normaliza elementos estructurados")
    if "def as_biomedical_connection_list" not in renderer:
        errors.append("advanced_unit_renderer.py no normaliza conexiones estructuradas")
    if PY_SYNTHESIS_NEW not in renderer:
        errors.append("render_synthesis no usa el normalizador de conexiones biomédicas")
    return errors


def public_errors(subjects: list[str]) -> list[str]:
    errors: list[str] = []
    for subject_id in subjects:
        for unit_path in (UNIT_ROOT / subject_id).glob("unit-*.json"):
            data = json.loads(unit_path.read_text(encoding="utf-8"))
            area_id = str(data.get("area_id") or "").strip()
            number = int(data.get("unit", 0) or 0)
            if not area_id or not number:
                errors.append(f"{unit_path.relative_to(ROOT)}: faltan area_id o unit")
                continue
            html_path = ROOT / area_id / subject_id / "unidades" / f"unidad-{number:02d}.html"
            if not html_path.exists():
                errors.append(f"falta {html_path.relative_to(ROOT)}")
                continue
            text = html_path.read_text(encoding="utf-8")
            for marker in BAD_PUBLIC_MARKERS:
                if marker in text:
                    errors.append(f"{html_path.relative_to(ROOT)} contiene artefacto de objeto: {marker}")
                    break
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Aplica correcciones idempotentes a ambos renderers.")
    parser.add_argument("--list-subjects", action="store_true", help="Imprime asignaturas con conexiones estructuradas.")
    parser.add_argument("--check-public", action="store_true", help="Valida renderers y HTML de asignaturas afectadas.")
    args = parser.parse_args()

    if args.apply:
        changed = apply_fixes()
        print("Archivos corregidos: " + (", ".join(changed) if changed else "ninguno; ya estaban actualizados"))

    subjects = structured_subjects()
    if args.list_subjects:
        print("\n".join(subjects))

    errors = source_errors()
    if args.check_public:
        errors.extend(public_errors(subjects))
    for error in errors:
        print(f"ERROR: {error}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
