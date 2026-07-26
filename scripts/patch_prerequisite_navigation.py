#!/usr/bin/env python3
"""Synchronize prerequisite-map links in generated navigation."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: se esperaba una coincidencia y se encontraron {count}")
    return text.replace(old, new)


def patch_catalog() -> None:
    path = ROOT / "catalogo" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        '            <li><a href="index.html" aria-current="page">Catálogo</a></li>\n',
        '            <li><a href="index.html" aria-current="page">Catálogo</a></li>\n'
        '            <li><a href="../mapa/index.html">Mapa curricular</a></li>\n',
        "enlace del mapa en la navegación del catálogo",
    )
    text = replace_once(
        text,
        "      </dl>\n    </section>\n\n    <section class=\"section\" aria-labelledby=\"tracks-title\">",
        "      </dl>\n"
        "      <div class=\"page-actions\">\n"
        "        <a class=\"btn-link\" href=\"../mapa/index.html\">Explorar dependencias curriculares</a>\n"
        "        <a class=\"btn-link secondary\" href=\"../index.html\">Volver al inicio</a>\n"
        "      </div>\n"
        "    </section>\n\n"
        "    <section class=\"section\" aria-labelledby=\"tracks-title\">",
        "acciones del mapa en el catálogo",
    )
    path.write_text(text, encoding="utf-8")


def main() -> int:
    patch_catalog()
    print("Navegación del mapa curricular sincronizada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
