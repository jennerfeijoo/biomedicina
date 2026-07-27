#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS_PATH = ROOT / "assets" / "js" / "generated-units.js"
PY_PATH = ROOT / "scripts" / "advanced_unit_renderer.py"

JS_ELEMENT_BLOCK = '''  function element(tag, className = "", text = null) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== null && text !== undefined) node.textContent = String(text);
    return node;
  }
'''

JS_ELEMENT_REPLACEMENT = '''  function element(tag, className = "", text = null) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== null && text !== undefined) node.textContent = String(text);
    return node;
  }

  function textValue(value) {
    if (typeof value === "string" || typeof value === "number") return String(value).trim();
    if (!value || typeof value !== "object" || Array.isArray(value)) return "";

    const label = [value.topic, value.title, value.name, value.domain]
      .find((candidate) => typeof candidate === "string" && candidate.trim());
    const detail = [value.connection, value.description, value.application, value.text, value.value]
      .find((candidate) => typeof candidate === "string" && candidate.trim());

    if (label && detail) return `${label.trim()}: ${detail.trim()}`;
    return String(detail || label || "").trim();
  }
'''

JS_LIST_BLOCK = '''  function appendList(parent, items, className = "") {
    const list = element("ul", className);
    for (const item of items || []) list.appendChild(element("li", "", item));
    parent.appendChild(list);
    return list;
  }
'''

JS_LIST_REPLACEMENT = '''  function appendList(parent, items, className = "") {
    const list = element("ul", className);
    for (const item of items || []) {
      const text = textValue(item);
      if (text) list.appendChild(element("li", "", text));
    }
    parent.appendChild(list);
    return list;
  }
'''

PY_LIST_BLOCK = '''def as_text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]
'''

PY_LIST_REPLACEMENT = '''def text_value(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value).strip()
    if not isinstance(value, dict):
        return ""

    label = next(
        (
            str(value.get(key)).strip()
            for key in ("topic", "title", "name", "domain")
            if isinstance(value.get(key), str) and str(value.get(key)).strip()
        ),
        "",
    )
    detail = next(
        (
            str(value.get(key)).strip()
            for key in ("connection", "description", "application", "text", "value")
            if isinstance(value.get(key), str) and str(value.get(key)).strip()
        ),
        "",
    )
    if label and detail:
        return f"{label}: {detail}"
    return detail or label


def as_text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [text for item in value if (text := text_value(item))]
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: se esperaba una coincidencia y se encontraron {count}")
    return text.replace(old, new, 1)


def main() -> int:
    js = JS_PATH.read_text(encoding="utf-8")
    js = replace_once(js, JS_ELEMENT_BLOCK, JS_ELEMENT_REPLACEMENT, "helper JavaScript")
    js = replace_once(js, JS_LIST_BLOCK, JS_LIST_REPLACEMENT, "lista JavaScript")
    JS_PATH.write_text(js, encoding="utf-8")

    py = PY_PATH.read_text(encoding="utf-8")
    py = replace_once(py, PY_LIST_BLOCK, PY_LIST_REPLACEMENT, "normalización Python")
    PY_PATH.write_text(py, encoding="utf-8")

    assert 'return `${label.trim()}: ${detail.trim()}`;' in js
    assert 'return f"{label}: {detail}"' in py
    print("[ok] renderers preparados para listas estructuradas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
