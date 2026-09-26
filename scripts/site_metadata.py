"""Deterministic metadata for public pages, independent of their renderer."""
from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re

BASE_URL = 'https://jennerfeijoo.github.io/biomedicina/'


class PageHead(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.description = ''
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = attrs.get('content', '')

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def add_metadata(source: str, relative_path: str) -> str:
    source = re.sub(r'\n?\s*<!-- site-metadata:start -->.*?<!-- site-metadata:end -->', '', source, flags=re.S)
    # Normalize pre-existing tags rather than duplicating canonical/social values.
    source = re.sub(r'\s*<link\b[^>]*rel=["\'](?:canonical|icon)["\'][^>]*>', '', source, flags=re.I)
    source = re.sub(r'\s*<meta\b[^>]*(?:property=["\']og:[^"\']+|name=["\']twitter:[^"\']+)["\'][^>]*>', '', source, flags=re.I)
    head = PageHead()
    head.feed(source.split('</head>')[0])
    url = BASE_URL + relative_path
    title = escape(head.title, quote=True)
    description = escape(head.description, quote=True)
    tags = [
        '<!-- site-metadata:start -->',
        f'<link rel="canonical" href="{url}" />',
        f'<link rel="icon" type="image/svg+xml" href="{BASE_URL}assets/favicon.svg" />',
        f'<meta property="og:title" content="{title}" />',
        f'<meta property="og:description" content="{description}" />',
        '<meta property="og:type" content="website" />',
        f'<meta property="og:url" content="{url}" />',
        '<meta property="og:locale" content="es_ES" />',
        '<meta name="twitter:card" content="summary" />',
        f'<meta name="twitter:title" content="{title}" />',
        f'<meta name="twitter:description" content="{description}" />',
        '<!-- site-metadata:end -->',
    ]
    return re.sub(r'\s*</head>', lambda _: '\n  ' + '\n  '.join(tags) + '\n</head>', source, count=1)


def write_discovery_files(root: Path) -> None:
    paths = [root / 'index.html', root / 'mapa/index.html', root / 'catalogo/index.html']
    for folder in ('ciencias-basicas', 'biologicas-medicas', 'ingenieria-biomedica', 'gestion-etica-comunicacion'):
        paths.extend((root / folder).rglob('*.html'))
    urls = sorted({BASE_URL + p.relative_to(root).as_posix() for p in paths if p.exists()})
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += ''.join(f'  <url><loc>{escape(url)}</loc></url>\n' for url in urls) + '</urlset>\n'
    (root / 'sitemap.xml').write_text(xml, encoding='utf-8')
    (root / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + BASE_URL + 'sitemap.xml\n', encoding='utf-8')
