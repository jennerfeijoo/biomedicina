#!/usr/bin/env python3
"""Validador básico de enlaces internos para CitoNauta.

Recorre archivos HTML del repositorio y detecta enlaces locales rotos.
Ignora enlaces externos, mailto, tel, javascript, anchors internos puros y rutas vacías.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
HREF_RE = re.compile(r'''href=["']([^"']+)["']''', re.IGNORECASE)
IGNORE_PREFIXES = ("http://", "https://", "mailto:", "tel:", "javascript:", "#")


def is_local_link(href: str) -> bool:
    href = href.strip()
    if not href:
        return False
    lowered = href.lower()
    return not lowered.startswith(IGNORE_PREFIXES)


def resolve_link(source: Path, href: str) -> Path:
    parsed = urlparse(href)
    clean_path = unquote(parsed.path)
    if not clean_path:
        return source
    if clean_path.startswith("/"):
        return ROOT / clean_path.lstrip("/")
    return (source.parent / clean_path).resolve()


def html_files() -> list[Path]:
    ignored_dirs = {".git", "node_modules", "__pycache__"}
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def validate() -> list[tuple[Path, str, Path]]:
    broken: list[tuple[Path, str, Path]] = []
    for file_path in html_files():
        text = file_path.read_text(encoding="utf-8", errors="replace")
        for href in HREF_RE.findall(text):
            if not is_local_link(href):
                continue
            target = resolve_link(file_path, href)
            if not target.exists():
                broken.append((file_path, href, target))
    return broken


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida enlaces internos en archivos HTML.")
    parser.add_argument("--quiet", action="store_true", help="Muestra solo el resumen final.")
    args = parser.parse_args()

    broken = validate()
    if broken and not args.quiet:
        print("Enlaces internos rotos detectados:\n")
        for source, href, target in broken:
            print(f"- {source.relative_to(ROOT)} -> {href} [no existe: {target.relative_to(ROOT) if target.is_relative_to(ROOT) else target}]")

    print("\nResumen de validación:")
    print(f"- archivos HTML revisados: {len(html_files())}")
    print(f"- enlaces internos rotos: {len(broken)}")

    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
