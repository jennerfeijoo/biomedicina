"""Render home navigation from the same pathways used by the catalog."""
from html import escape
import re


def render_discovery(payload):
    tracks = {track['id']: track for track in payload['tracks']}
    families, sections = [], []
    for number, group in enumerate(payload['groups'], 1):
        group_id = escape(group['id'], quote=True)
        title = escape(group['title'])
        description = escape(group['description'])
        families.append(
            f'<a class="entry-card" href="#rutas-{group_id}">'
            f'<span class="entry-number">{number:02d}</span>'
            f'<div><h3>{title}</h3><p>{description}</p></div>'
            f'<span class="entry-action">Explorar {len(group["tracks"])} rutas →</span></a>'
        )
        links = []
        for track_id in group['tracks']:
            track = tracks[track_id]
            safe_id = escape(track_id, quote=True)
            scope = track.get('scope_note', '')
            scope_html = f'<small class="route-scope">{escape(scope)}</small>' if scope else ''
            links.append(
                f'<a class="route-link" href="catalogo/index.html?track={safe_id}#asignaturas">'
                f'<strong>{escape(track["title"])}</strong>'
                f'<p>{escape(track["question"])}</p>{scope_html}'
                f'<small data-track-count="{safe_id}">{len(track["subjects"])} asignaturas →</small></a>'
            )
        sections.append(
            f'<section class="route-group" id="rutas-{group_id}" aria-labelledby="group-{group_id}">'
            f'<h3 id="group-{group_id}">{title}</h3>'
            f'<div class="route-list">{"".join(links)}</div></section>'
        )
    references = ''.join(
        f'<li><a href="{escape(source["url"], quote=True)}">{escape(source["institution"])}</a>'
        f' — {escape(source["contribution"])}</li>'
        for source in payload['curricular_references']
    )
    sections.append(
        '<details class="curriculum-references"><summary>Cómo se organizan estas rutas</summary>'
        '<p>La organización conecta las asignaturas de CitoNauta y se contrastó con programas universitarios '
        'de distintas regiones. Las familias se solapan y no agotan todos los campos de la biomedicina.</p>'
        f'<ul>{references}</ul><p>{escape(payload["editorial_basis"])}</p></details>'
    )
    return {'families': '<div class="entry-grid">' + '\n'.join(families) + '</div>',
            'routes': '\n'.join(sections)}


def update_home(source, payload):
    for name, rendered in render_discovery(payload).items():
        pattern = rf'<!-- home-{name}:start -->.*?<!-- home-{name}:end -->'
        replacement = f'<!-- home-{name}:start -->\n{rendered}\n<!-- home-{name}:end -->'
        source, count = re.subn(pattern, lambda _: replacement, source, flags=re.S)
        if count != 1:
            raise ValueError(f'Expected one home-{name} block, found {count}')
    return source
