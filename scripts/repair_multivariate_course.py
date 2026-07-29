#!/usr/bin/env python3
"""Aplica correcciones editoriales deterministas al paquete multivariado."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_ROOT = ROOT / "data/course_redevelopment/analisis-estadistico-multivariado/units"

KEY_POINT_REPLACEMENTS = {
    1: (2, 1, "Imputar valores faltantes modifica covarianzas y relaciones entre variables."),
    2: (0, 0, "La covarianza conserva las unidades originales de ambas variables."),
    3: (2, 0, "Los biplots dependen de convenciones explícitas de escalado y representación."),
    4: (1, 2, "Los modelos de mezcla añaden supuestos distribucionales y de identificabilidad."),
    5: (2, 1, "PERMANOVA contrasta estructura conjunta definida mediante una matriz de distancias."),
    6: (1, 1, "La regularización reduce varianza a cambio de introducir sesgo controlado."),
    7: (0, 0, "CCA relaciona combinaciones lineales construidas a partir de dos bloques de variables."),
    6_004: (3, 1, "El dominio de aplicabilidad requiere soporte empírico suficiente."),
    7_003: (2, 1, "Concatenar bloques sin equilibrarlos puede sesgar las componentes estimadas."),
}

EXTRA_PARAGRAPHS = {
    5: (
        "Multiplicidad, tamaño de efecto y comunicación",
        "La robustez de una conclusión multivariada también se evalúa mediante análisis de sensibilidad preespecificados. Se comparan conjuntos de respuestas, estimadores de covarianza y esquemas de permutación razonables, sin seleccionar únicamente la variante más significativa. Cuando una conclusión cambia con decisiones menores, el informe debe presentarla como dependiente del análisis y no como evidencia confirmatoria estable.",
    ),
    6: (
        "Aplicabilidad, subgrupos y comunicación",
        "La evaluación debe conservar una tabla de errores por contexto de uso, no solo métricas agregadas. Examinar patrones de falsos positivos, falsos negativos y abstenciones permite identificar regiones donde las clases se solapan o el soporte es insuficiente. Estos análisis se realizan sin reajustar el conjunto de prueba y se utilizan para delimitar aplicaciones futuras, no para rescatar retrospectivamente el desempeño.",
    ),
    7: (
        "Estabilidad, selección y reporte",
        "La validación externa de una asociación multibloque requiere reproducir tanto la fuerza de relación como la estructura de las componentes. Una correlación global similar puede ocultar cargas completamente distintas entre cohortes. Por ello se comparan subespacios, contribuciones por bloque, signos alineados y estabilidad de variables, y se explica si la replicación sostiene una relación general o solo un resultado numérico superficial.",
    ),
    8: (
        "Reproducibilidad, visualización y decisión",
        "La validación externa debe conservar una separación estricta entre evaluación y adaptación. Si se corrigen lotes, recalibran parámetros o seleccionan variables usando la cohorte externa, esa cohorte deja de representar una prueba independiente. Cualquier adaptación se documenta como nueva fase de desarrollo y requiere otra evaluación. Esta regla evita presentar como transportabilidad un desempeño obtenido mediante ajustes retrospectivos.",
    ),
}


def load_unit(unit: int) -> tuple[Path, dict]:
    path = UNIT_ROOT / f"unit-{unit:02d}.json"
    return path, json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    changed = 0
    for key, (section_index, point_index, replacement) in KEY_POINT_REPLACEMENTS.items():
        unit = key if key < 100 else key // 1000
        path, data = load_unit(unit)
        points = data["theory_sections"][section_index]["key_points"]
        if points[point_index] != replacement:
            points[point_index] = replacement
            path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
            changed += 1

    for unit, (heading, paragraph) in EXTRA_PARAGRAPHS.items():
        path, data = load_unit(unit)
        section = next(item for item in data["theory_sections"] if item["heading"] == heading)
        if paragraph not in section["paragraphs"]:
            section["paragraphs"].append(paragraph)
            path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
            changed += 1

    print(f"Correcciones aplicadas: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
