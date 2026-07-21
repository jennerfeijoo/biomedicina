#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "fundamentos-programacion"
COURSE_PATH = ROOT / "data" / "generated_courses" / "fundamentos-programacion.json"


def add_unique_source(sources: list[dict], source: dict) -> None:
    if source["url"] not in {item.get("url") for item in sources}:
        sources.append(source)


def main() -> int:
    unit1_path = UNIT_DIR / "unit-01.json"
    unit1 = json.loads(unit1_path.read_text(encoding="utf-8"))
    unit1["theory_sections"][0]["equations"] = [
        {
            "label": "Promedio de n mediciones",
            "latex": "\\bar{x}=\\frac{1}{n}\\sum_{i=1}^{n}x_i",
            "interpretation": "La expresión resume n valores comparables; el programa debe validar n>0 y conservar la unidad de x.",
        },
        {
            "label": "Concentración másica educativa",
            "latex": "C=\\frac{m}{V},\\qquad V>0",
            "interpretation": "La restricción del volumen pertenece al contrato y evita una división indefinida.",
        },
    ]
    unit1["theory_sections"][1]["equations"] = [
        {
            "label": "Conversión de miligramos a gramos",
            "latex": "m_{\\mathrm{g}}=\\frac{m_{\\mathrm{mg}}}{1000}",
            "interpretation": "La variable y el subíndice hacen visible la unidad antes y después de la conversión.",
        }
    ]
    unit1["theory_sections"][2]["equations"] = [
        {
            "label": "Comparación aproximada",
            "latex": "|a-b|\\leq\\max(\\varepsilon_{\\mathrm{abs}},\\varepsilon_{\\mathrm{rel}}\\max(|a|,|b|))",
            "interpretation": "Una tolerancia combina escala absoluta y relativa; sus valores deben justificarse para el cálculo.",
        }
    ]
    add_unique_source(unit1["sources"], {
        "title": "Programming with Python — Analyzing Patient Data",
        "organization": "Software Carpentry",
        "url": "https://swcarpentry.github.io/python-novice-inflammation/",
        "type": "lección abierta",
    })
    add_unique_source(unit1["sources"], {
        "title": "CS50's Introduction to Programming with Python",
        "organization": "Harvard University",
        "url": "https://cs50.harvard.edu/python/2022/",
        "type": "curso universitario abierto",
    })
    unit1_path.write_text(json.dumps(unit1, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unit3_path = UNIT_DIR / "unit-03.json"
    unit3 = json.loads(unit3_path.read_text(encoding="utf-8"))
    add_unique_source(unit3["sources"], {
        "title": "Functions — Programming with Python",
        "organization": "Software Carpentry",
        "url": "https://swcarpentry.github.io/python-novice-inflammation/08-func.html",
        "type": "lección abierta",
    })
    add_unique_source(unit3["sources"], {
        "title": "Packaging Python Projects",
        "organization": "Python Packaging Authority",
        "url": "https://packaging.python.org/en/latest/tutorials/packaging-projects/",
        "type": "guía oficial",
    })
    unit3_path.write_text(json.dumps(unit3, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unit5_path = UNIT_DIR / "unit-05.json"
    unit5 = json.loads(unit5_path.read_text(encoding="utf-8"))
    unit5["theory_sections"][1]["equations"] = [
        {
            "label": "Media muestral",
            "latex": "\\bar{x}=\\frac{1}{n}\\sum_{i=1}^{n}x_i",
            "interpretation": "El denominador es el número de observaciones incluidas después de aplicar una política de faltantes explícita.",
        },
        {
            "label": "Desviación estándar muestral",
            "latex": "s=\\sqrt{\\frac{1}{n-1}\\sum_{i=1}^{n}(x_i-\\bar{x})^2}",
            "interpretation": "La fórmula resume dispersión alrededor de la media y requiere al menos dos observaciones válidas.",
        },
    ]
    unit5_path.write_text(json.dumps(unit5, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    course = json.loads(COURSE_PATH.read_text(encoding="utf-8"))
    for resource in course["core_resources"]:
        if resource["url"] == "https://packaging.python.org/":
            resource["url"] = "https://packaging.python.org/en/latest/tutorials/packaging-projects/"
        if resource["url"] == "https://docs.pytest.org/":
            resource["url"] = "https://docs.pytest.org/en/stable/getting-started.html"
    COURSE_PATH.write_text(json.dumps(course, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Corregidas fuentes, ecuaciones y recursos de Fundamentos de Programación")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
