#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/biomateriales/units/unit-01.json"
MIRROR = ROOT / "data/generated_units/biomateriales/unit-01.json"

unit = json.loads(SOURCE.read_text(encoding="utf-8"))
activities = unit.setdefault("guided_activities", [])
titles = {item.get("title") for item in activities}

if "Actividad guiada: auditoría de datos de propiedades antes de comparar materiales" not in titles:
    activities.append({
        "title": "Actividad guiada: auditoría de datos de propiedades antes de comparar materiales",
        "instructions": [
            "Trabaja solo con una tabla sintética o con fuentes abiertas localizables; no uses datos de pacientes ni ensayos en personas.",
            "Antes de comparar números, escribe qué propiedad representa cada columna y qué modo de fallo o requisito ayuda a evaluar.",
            "Conserva unidad, método, temperatura, medio, orientación, estado del material y procedencia cuando estén disponibles.",
            "Marca como no comparable cualquier dato obtenido bajo condiciones incompatibles o cuya métrica no tenga el mismo significado físico entre familias.",
            "Distingue propiedad del material, geometría del componente, estado superficial y proceso de fabricación.",
            "Cierra con una tabla corregida y una lista de mediciones faltantes, no con un ranking forzado."
        ],
        "problems": [
            "Diferencia módulo elástico, límite de fluencia, resistencia última, dureza y tenacidad a fractura mediante una pregunta de diseño que responda cada magnitud.",
            "Identifica dos pares de valores que no deberían compararse directamente por diferencias de temperatura, medio, orientación o método.",
            "Explica por qué un límite de fluencia puede ser no aplicable a una cerámica que fractura sin plasticidad apreciable.",
            "Clasifica ocho variables del escenario como propiedad del material, geometría, superficie o proceso.",
            "Detecta qué dato revela anisotropía en un compuesto y qué dirección de carga debe declararse.",
            "Recalcula un módulo específico E/ρ y explica qué decisión puede informar y cuáles no.",
            "Identifica un caso en el que una propiedad superficial sea relevante aunque el módulo volumétrico no cambie.",
            "Redacta una regla para decidir cuándo un dato bibliográfico es solo orientativo y cuándo es suficientemente comparable para el cribado.",
            "Propón una medición adicional para discriminar dos candidatos que siguen técnicamente empatados."
        ],
        "deliverables": [
            "Diccionario de propiedades con definición, unidad y modo de fallo relacionado.",
            "Tabla de comparabilidad con condiciones y fuentes.",
            "Lista de datos no comparables y razón de exclusión.",
            "Clasificación de variables por nivel del sistema.",
            "Lista priorizada de mediciones faltantes."
        ],
        "checking_criteria": [
            "Rigidez, resistencia, dureza y tenacidad permanecen diferenciadas.",
            "Ningún valor se compara sin conservar unidad y condición pertinente.",
            "Las métricas no equivalentes se declaran como no aplicables o no comparables.",
            "La anisotropía se vincula a una dirección explícita.",
            "La conclusión identifica evidencia faltante en lugar de inventar precisión.",
            "No se infiere seguridad clínica a partir de propiedades de material."
        ]
    })

if "Actividad guiada: auditoría de una afirmación de biocompatibilidad" not in titles:
    activities.append({
        "title": "Actividad guiada: auditoría de una afirmación de biocompatibilidad",
        "instructions": [
            "Usa un escenario sintético y trata la palabra biocompatible como una afirmación que debe delimitarse, no como una propiedad binaria.",
            "Separa material constitutivo, componente, dispositivo final y uso previsto.",
            "Identifica tipo y duración de contacto, superficie expuesta, procesamiento y esterilización relevantes.",
            "Distingue evidencia previa del material de la evidencia necesaria para el dispositivo final.",
            "Clasifica cada conclusión como técnica, biológica, clínica o regulatoria y elimina saltos entre niveles.",
            "Conserva una versión antes-después de la afirmación y justifica cada corrección."
        ],
        "problems": [
            "Reescribe «este polímero es biocompatible» especificando dispositivo, contacto, duración y alcance de la evidencia.",
            "Enumera cuatro cambios de fabricación o superficie que podrían impedir transferir automáticamente evidencia previa.",
            "Explica por qué un historial de uso puede informar una evaluación sin demostrar seguridad universal.",
            "Construye una tabla que separe composición conocida, posibles extractables o productos de degradación, superficie, contacto previsto y evidencia pendiente.",
            "Identifica qué afirmaciones pueden sostenerse en U1 y cuáles pertenecen a evaluación biológica, desempeño clínico o conformidad regulatoria posterior.",
            "Propón dos preguntas de riesgo que deberían responderse antes de diseñar ensayos biológicos específicos.",
            "Detecta una frase que convierta una preselección de material en recomendación clínica y corrígela.",
            "Redacta un cierre de máximo 120 palabras que conserve incertidumbre y siguiente evidencia necesaria."
        ],
        "deliverables": [
            "Afirmación original y versión corregida.",
            "Mapa material-componente-dispositivo-uso previsto.",
            "Tabla de evidencia disponible y pendiente.",
            "Clasificación de conclusiones por nivel técnico, biológico, clínico o regulatorio.",
            "Cierre acotado con siguiente paso explícito."
        ],
        "checking_criteria": [
            "Biocompatibilidad no aparece como propiedad absoluta o casilla sí/no.",
            "El dispositivo final y su contacto están explícitos.",
            "Se distinguen evidencia material y evaluación biológica del dispositivo.",
            "No se afirma seguridad, eficacia ni conformidad que no hayan sido evaluadas.",
            "La corrección conserva trazabilidad entre evidencia, límite y siguiente paso.",
            "La actividad no usa personas, animales ni muestras biológicas."
        ]
    })

assert len(activities) >= 3, "Biomateriales U1 requires at least three guided activities"
text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
