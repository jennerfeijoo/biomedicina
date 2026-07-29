#!/usr/bin/env python3
"""Completa la densidad residual del paquete multivariado."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_ROOT = ROOT / "data/course_redevelopment/analisis-estadistico-multivariado/units"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)

EXTRA = {
    6: (
        "Aplicabilidad, subgrupos y comunicación",
        "La transportabilidad también se examina comparando la distribución de variables y puntuaciones entre desarrollo y evaluación. Un cambio de prevalencia, protocolo o rango puede alterar probabilidades y errores aunque la frontera matemática permanezca fija. El informe identifica estas diferencias, evalúa su efecto mediante análisis de sensibilidad y evita atribuir cualquier deterioro a una sola causa sin evidencia adicional.",
    ),
    7: (
        "Estabilidad, selección y reporte",
        "La incertidumbre de las asociaciones latentes debe mostrarse con intervalos o distribuciones de remuestreo. Reportar únicamente la solución de mayor correlación oculta la variabilidad de pesos y cargas. Cuando varias soluciones presentan desempeño similar, el informe conserva esa equivalencia y evita seleccionar una narrativa biológica única a partir de diferencias numéricas pequeñas e inestables.",
    ),
    8: (
        "Reproducibilidad, visualización y decisión",
        "La auditoría final reconstruye paso a paso la cohorte analítica, incluidos criterios de inclusión, exclusiones, muestras repetidas, variables descartadas y transformaciones aprendidas. También compara conteos y distribuciones con la fuente original. Esta reconciliación permite detectar pérdidas silenciosas, duplicados o cambios de población que podrían explicar resultados aparentemente biológicos y fortalece la trazabilidad de cada afirmación.",
    ),
}


def load(unit: int) -> tuple[Path, dict]:
    path = UNIT_ROOT / f"unit-{unit:02d}.json"
    return path, json.loads(path.read_text(encoding="utf-8"))


def theory_words(data: dict) -> int:
    return sum(len(WORD_RE.findall(paragraph)) for section in data["theory_sections"] for paragraph in section["paragraphs"])


def main() -> int:
    changed = 0
    path, data = load(2)
    replacement = "La colinealidad condiciona la interpretación y la estabilidad numérica."
    if data["theory_sections"][2]["key_points"][0] != replacement:
        data["theory_sections"][2]["key_points"][0] = replacement
        path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        changed += 1

    for unit, (heading, paragraph) in EXTRA.items():
        path, data = load(unit)
        section = next(item for item in data["theory_sections"] if item["heading"] == heading)
        if paragraph not in section["paragraphs"]:
            section["paragraphs"].append(paragraph)
            path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
            changed += 1
        print(f"unit-{unit:02d}: {theory_words(data)} palabras teóricas")

    print(f"Correcciones aplicadas: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
