#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales" / "unit-01.json"

unit = json.loads(SOURCE.read_text(encoding="utf-8"))
activities = unit.setdefault("guided_activities", [])

if len(activities) < 2:
    activities.append({
        "title": "Actividad guiada: propiedades, modos de fallo y comparabilidad",
        "instructions": [
            "Usa únicamente los datos sintéticos de la actividad y conserva todas las unidades.",
            "Para cada propiedad, escribe primero qué fenómeno representa y qué modo de fallo ayuda a evaluar.",
            "Marca como no comparable cualquier métrica que no tenga el mismo significado físico entre candidatos.",
            "Separa siempre propiedad del material, geometría de la pieza y condición de ensayo.",
            "Corrige la tabla inicial antes de redactar cualquier conclusión."
        ],
        "problems": [
            "Explica con un ejemplo por qué módulo elástico y resistencia última pueden ordenar dos materiales de forma diferente.",
            "Construye una mini tabla que diferencie módulo, límite de fluencia, resistencia última, dureza y tenacidad a fractura.",
            "Identifica qué propiedad sería prioritaria ante deformación elástica excesiva y cuál ante propagación de una grieta.",
            "Detecta por qué no es válido comparar un límite elástico metálico con una cerámica sin plasticidad apreciable.",
            "Describe cómo orientación y arquitectura pueden producir propiedades longitudinales y transversales distintas en un compuesto.",
            "Propón dos condiciones de ensayo que deban coincidir antes de comparar valores publicados de una propiedad.",
            "Clasifica como material, geometría, superficie o proceso ocho variables del escenario suministrado.",
            "Redacta una conclusión que indique qué propiedad falta medir para discriminar entre dos candidatos técnicamente cercanos."
        ],
        "deliverables": [
            "Tabla corregida de propiedad-definición-unidad-modo de fallo.",
            "Lista de métricas comparables y no comparables con justificación.",
            "Clasificación de variables por nivel del sistema.",
            "Conclusión acotada con una medición pendiente explícita."
        ],
        "checking_criteria": [
            "No se usan rigidez, resistencia, dureza y tenacidad como sinónimos.",
            "Las unidades y condiciones de ensayo permanecen visibles.",
            "Las celdas no comparables se declaran en vez de rellenarse artificialmente.",
            "La conclusión se limita al modo de fallo evaluado y no implica seguridad clínica."
        ]
    })

if len(activities) < 3:
    activities.append({
        "title": "Actividad guiada: auditoría y revisión de una decisión de materiales",
        "instructions": [
            "Parte de la matriz producida en la primera actividad y no cambies criterios sin registrar el motivo.",
            "Audita cada dato mediante fuente, unidad, condición, rango e incertidumbre.",
            "Repite la selección con un escenario alternativo de ponderaciones y con una propiedad crítica perturbada.",
            "Clasifica los hallazgos como crítico, importante o editorial.",
            "Conserva una tabla antes-después de todas las correcciones."
        ],
        "problems": [
            "Localiza tres datos cuya procedencia o condición de ensayo sería insuficiente para una decisión real.",
            "Identifica una restricción que nunca debería compensarse con una puntuación alta en otros criterios.",
            "Cambia de forma razonable los pesos y determina si el primer candidato permanece estable.",
            "Perturba en ±10 % la propiedad más incierta y documenta si algún candidato cruza un umbral de exclusión.",
            "Busca una afirmación que trate biocompatibilidad como propiedad absoluta y reescríbela en términos de dispositivo, contacto y duración.",
            "Añade una columna de evidencia pendiente para fatiga o fractura, superficie, degradación y evaluación biológica.",
            "Distingue qué parte de la decisión corresponde a selección de material y cuál deberá resolverse mediante diseño geométrico o procesamiento.",
            "Redacta una conclusión final que incluya candidato preferido o empate, sensibilidad, incertidumbre y siguiente prueba necesaria."
        ],
        "deliverables": [
            "Lista priorizada de hallazgos de auditoría.",
            "Matriz revisada con trazabilidad de cambios.",
            "Comparación del ranking nominal y los escenarios de sensibilidad.",
            "Declaración final de límites y evidencia pendiente."
        ],
        "checking_criteria": [
            "Cada corrección tiene una razón técnica localizable.",
            "La sensibilidad se informa aunque debilite el ranking inicial.",
            "Biocompatibilidad se formula de manera contextual y no binaria.",
            "La revisión diferencia selección de material, diseño del componente y evaluación posterior."
        ]
    })

assert len(unit["guided_activities"]) >= 3
text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
