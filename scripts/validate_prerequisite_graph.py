#!/usr/bin/env python3
"""Validate curated prerequisite relations without imposing semester sequencing."""
from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = ROOT / "data" / "citonauta_curriculum.json"
GRAPH_PATH = ROOT / "data" / "prerequisite_graph.json"
MAP_PATH = ROOT / "mapa" / "index.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    curriculum = load_json(CURRICULUM_PATH)
    graph = load_json(GRAPH_PATH)

    subjects: dict[str, dict] = {}
    area_by_subject: dict[str, str] = {}
    for area in curriculum.get("areas", []):
        for subject in area.get("subjects", []):
            subject_id = subject.get("id")
            if not subject_id:
                errors.append(f"asignatura sin id en el área {area.get('id')}")
                continue
            if subject_id in subjects:
                errors.append(f"id de asignatura duplicado: {subject_id}")
            subjects[subject_id] = subject
            area_by_subject[subject_id] = area.get("id", "")

    relation_types = graph.get("relation_types", {})
    edges = graph.get("edges", [])
    if graph.get("schema_version") != "1.0":
        errors.append("schema_version de prerequisite_graph.json debe ser 1.0")
    if "recommended_foundation" not in relation_types:
        errors.append("falta el tipo de relación recommended_foundation")
    if len(edges) < 40:
        errors.append(f"la red contiene solo {len(edges)} aristas; se esperaban al menos 40 relaciones curadas")

    seen: set[tuple[str, str, str]] = set()
    adjacency: dict[str, list[str]] = defaultdict(list)
    indegree: dict[str, int] = {subject_id: 0 for subject_id in subjects}
    covered: set[str] = set()
    cross_area_edges = 0

    for index, edge in enumerate(edges, start=1):
        source = edge.get("from")
        target = edge.get("to")
        relation = edge.get("relation")
        rationale = str(edge.get("rationale", "")).strip()
        label = f"arista {index} ({source} -> {target})"

        if source not in subjects:
            errors.append(f"{label}: origen desconocido")
        if target not in subjects:
            errors.append(f"{label}: destino desconocido")
        if source == target:
            errors.append(f"{label}: auto-dependencia no permitida")
        if relation not in relation_types:
            errors.append(f"{label}: tipo de relación desconocido: {relation}")
        if len(rationale) < 35:
            errors.append(f"{label}: justificación demasiado breve")

        marker = (str(source), str(target), str(relation))
        if marker in seen:
            errors.append(f"{label}: relación duplicada")
        seen.add(marker)

        if source in subjects and target in subjects and source != target:
            adjacency[source].append(target)
            indegree[target] += 1
            covered.update((source, target))
            if area_by_subject[source] != area_by_subject[target]:
                cross_area_edges += 1

    if len(covered) < 45:
        errors.append(f"la red solo cubre {len(covered)} asignaturas; se esperaban al menos 45")
    if cross_area_edges < 8:
        errors.append(f"solo hay {cross_area_edges} relaciones entre áreas; el andamiaje debe ser interdisciplinario")

    queue = deque(sorted(subject_id for subject_id, degree in indegree.items() if degree == 0))
    visited = 0
    while queue:
        current = queue.popleft()
        visited += 1
        for target in adjacency.get(current, []):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited != len(subjects):
        cyclic = sorted(subject_id for subject_id, degree in indegree.items() if degree > 0)
        errors.append("la red contiene ciclos: " + ", ".join(cyclic))

    required_files = (
        MAP_PATH,
        ROOT / "assets" / "js" / "prerequisite-map.js",
        ROOT / "assets" / "css" / "prerequisite-map.css",
    )
    for path in required_files:
        if not path.exists():
            errors.append(f"falta archivo público: {path.relative_to(ROOT)}")

    if MAP_PATH.exists():
        html = MAP_PATH.read_text(encoding="utf-8")
        for marker in (
            "data-subject-select",
            "data-foundations",
            "data-next-courses",
            "data-ancestors",
            "data-descendants",
            "prerequisite-map.js",
        ):
            if marker not in html:
                errors.append(f"mapa/index.html no contiene {marker}")
        forbidden_claims = ("prerrequisito obligatorio", "debes completar", "duración estimada", "semanas")
        lowered = html.casefold()
        for phrase in forbidden_claims:
            if phrase.casefold() in lowered:
                errors.append(f"mapa/index.html contiene una prescripción no permitida: {phrase}")

    if errors:
        print("Errores en el mapa de dependencias curriculares:\n")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1

    print("Mapa de dependencias curriculares validado.")
    print(f"- {len(subjects)} asignaturas en la fuente curricular")
    print(f"- {len(edges)} relaciones recomendadas")
    print(f"- {len(covered)} asignaturas cubiertas por al menos una relación")
    print(f"- {cross_area_edges} relaciones entre áreas")
    print("- red acíclica y sin secuencia temporal obligatoria")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
