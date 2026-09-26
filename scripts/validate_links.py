#!/usr/bin/env python3
"""Validador básico de enlaces internos para CitoNauta.

Recorre archivos HTML del repositorio y detecta enlaces locales rotos.
Comprueba href, src y anclas; reconoce las rutas de GitHub Pages y el origen público.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE_HOST = "jennerfeijoo.github.io"
SITE_PREFIX = "/biomedicina/"


class DocumentLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])


@lru_cache(maxsize=None)
def document(path):
    parser = DocumentLinks()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def is_local_link(href: str) -> bool:
    parsed = urlparse(href.strip())
    if parsed.netloc:
        return parsed.netloc == SITE_HOST and parsed.path.startswith(SITE_PREFIX)
    return not parsed.scheme and bool(href.strip())


def resolve_link(source: Path, href: str) -> Path:
    parsed = urlparse(href)
    clean_path = unquote(parsed.path)
    if not clean_path:
        return source
    if clean_path.startswith("/"):
        return ROOT / clean_path.removeprefix(SITE_PREFIX).lstrip("/")
    return (source.parent / clean_path).resolve()


def html_files() -> list[Path]:
    ignored_dirs = {".git", "node_modules", "__pycache__", "templates"}
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def validate() -> list[tuple[Path, str, Path]]:
    document.cache_clear()
    broken: list[tuple[Path, str, Path]] = []
    for file_path in html_files():
        for href in document(file_path).links:
            if not is_local_link(href):
                continue
            target = resolve_link(file_path, href)
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                broken.append((file_path, href, target))
                continue
            fragment = unquote(urlparse(href).fragment)
            if fragment and target.suffix == ".html" and fragment not in document(target).ids:
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
