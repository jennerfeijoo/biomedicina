#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from advanced_unit_renderer import as_text_list, text_value  # noqa: E402


def main() -> int:
    structured = {
        "topic": "Medicina regenerativa",
        "connection": "La identidad celular no garantiza seguridad, integración o eficacia.",
    }
    expected = (
        "Medicina regenerativa: "
        "La identidad celular no garantiza seguridad, integración o eficacia."
    )
    assert text_value(structured) == expected
    assert as_text_list(["Conexión simple", structured, None, {}]) == [
        "Conexión simple",
        expected,
    ]

    javascript = (ROOT / "assets" / "js" / "generated-units.js").read_text(encoding="utf-8")
    assert "function textValue(value)" in javascript
    assert "const text = textValue(item);" in javascript
    assert 'for (const item of items || []) list.appendChild(element("li", "", item));' not in javascript
    assert "[object Object]" not in javascript

    print("[ok] las conexiones estructuradas se convierten en texto legible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
