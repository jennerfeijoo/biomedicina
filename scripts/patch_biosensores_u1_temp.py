from __future__ import annotations

import json
from pathlib import Path

SOURCE = Path("data/course_redevelopment/biosensores/units/unit-01.json")
MIRROR = Path("data/generated_units/biosensores/unit-01.json")

unit = json.loads(SOURCE.read_text(encoding="utf-8"))

terms = {entry["term"].casefold() for entry in unit["glossary"]}
if "efecto de matriz" not in terms:
    unit["glossary"].append(
        {
            "term": "Efecto de matriz",
            "definition": "Cambio de la respuesta causado por componentes o propiedades de la matriz distintos del analito, capaz de alterar fondo, recuperación, reconocimiento o transducción respecto de una calibración en una matriz diferente.",
        }
    )

if len(unit["worked_examples"]) < 4:
    unit["worked_examples"].append(
        {
            "title": "Detectar un efecto de matriz antes de cuantificar",
            "scenario": "Un biosensor sintético produce 0,10 unidades de señal para un blanco en tampón y 0,28 para una matriz artificial sin analito. Una adición conocida de 4 nM produce 1,08 en tampón y 1,20 en la matriz.",
            "reasoning_steps": [
                "Comparar primero ambos blancos y cuantificar el desplazamiento basal de 0,18 unidades asociado a la matriz.",
                "Separar ese desplazamiento de la respuesta producida por la adición conocida; no asumir que restar el blanco resuelve todas las diferencias.",
                "Calcular las respuestas corregidas por sus propios blancos: 0,98 en tampón y 0,92 en matriz.",
                "Reconocer que, además del fondo distinto, la matriz modifica ligeramente la respuesta neta y podría afectar una calibración transferida desde tampón.",
                "Proponer una calibración o estudio de recuperación en matriz antes de estimar concentraciones desconocidas y registrar esta necesidad como evidencia pendiente."
            ],
            "interpretation": "Una matriz puede cambiar tanto el fondo como la respuesta neta. Una calibración construida en tampón no debe trasladarse automáticamente a muestras complejas sin evaluar la equivalencia de respuesta.",
            "limitations": [
                "Los números son sintéticos y no caracterizan una matriz biológica real.",
                "El ejemplo no estima recuperación, precisión ni límite de detección formalmente; esas métricas corresponden a U5.",
                "No demuestra desempeño clínico ni utilidad diagnóstica."
            ]
        }
    )

existing_urls = {item["url"] for item in unit["sources"]}
extra_sources = [
    {
        "title": "Guide to Selecting a Biorecognition Element for Biosensors",
        "organization": "Bioconjugate Chemistry / PubMed Central",
        "year": 2019,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6416154/",
        "type": "revisión metodológica abierta",
        "description": "Revisa cómo la selección del elemento de reconocimiento condiciona selectividad, reproducibilidad, estabilidad y arquitectura; en U1 se usa para delimitar la función del bioreceptor y el traspaso a U2.",
        "verification_status": "verified_directly",
        "locator": "PMC6416154, guía de selección de elementos de bioreconocimiento",
        "limitations": "La selección detallada de enzimas, anticuerpos, ácidos nucleicos y aptámeros se desarrolla en U2 y no se convierte aquí en una receta universal."
    },
    {
        "title": "Overview of IVD Regulation",
        "organization": "U.S. Food and Drug Administration",
        "year": 2024,
        "url": "https://www.fda.gov/medical-devices/ivd-regulatory-assistance/overview-ivd-regulation",
        "type": "información regulatoria oficial",
        "description": "Distingue características de desempeño analítico de la información clínica que puede ser necesaria para determinados dispositivos de diagnóstico in vitro.",
        "verification_status": "verified_directly",
        "locator": "Overview of IVD Regulation → Studies to Demonstrate Substantial Equivalence",
        "limitations": "Describe el marco estadounidense y se usa solo para separar capas de evidencia; no constituye asesoramiento regulatorio para un producto."
    },
    {
        "title": "Electrochemical biosensor",
        "organization": "IUPAC Gold Book",
        "year": 2025,
        "url": "https://goldbook.iupac.org/terms/view/09071",
        "doi": "10.1351/goldbook.09071",
        "type": "terminología oficial",
        "description": "Define el biosensor electroquímico como un sensor electroquímico que incorpora un elemento de reconocimiento biológico.",
        "verification_status": "verified_directly",
        "locator": "IUPAC Compendium of Chemical Terminology, term 09071",
        "limitations": "Es una definición específica de biosensores electroquímicos; no debe generalizarse como definición exclusiva de todas las modalidades."
    }
]
for source in extra_sources:
    if source["url"] not in existing_urls:
        unit["sources"].append(source)
        existing_urls.add(source["url"])

unit["editorial_notice"] = (
    "Material educativo de Biosensores U1 con curación académica interna y estado review. No constituye revisión disciplinar externa, validación analítica o clínica, validación de un dispositivo, certificación, asesoramiento diagnóstico ni conformidad regulatoria. Las actividades usan exclusivamente datos y escenarios sintéticos y no autorizan recoger muestras humanas, medir participantes, diagnosticar, prescribir ni inferir utilidad clínica a partir de una señal analítica."
)

text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")

assert SOURCE.read_bytes() == MIRROR.read_bytes()
assert len(unit["glossary"]) >= 19
assert len(unit["worked_examples"]) >= 4
assert len(unit["sources"]) >= 10
print("Biosensores U1: complemento pedagógico y bibliográfico aplicado.")
