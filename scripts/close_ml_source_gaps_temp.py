from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"
PATH = COURSE / "sources.json"
registry = json.loads(PATH.read_text(encoding="utf-8"))
registry["consulted_on"] = "2026-08-24"
by_id = {item["id"]: item for item in registry["sources"]}

updates = {
    "consort-ai": {
        "title": "Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension",
        "organization": "Nature Medicine / SPIRIT-AI and CONSORT-AI Working Group",
        "year": 2020,
        "doi": "10.1038/s41591-020-1034-x",
        "verification_status": "verified_directly",
        "locator": "Nature Medicine 26:1364–1374 (2020); abstract and CONSORT-AI extension checklist/explanation; DOI 10.1038/s41591-020-1034-x",
        "role": "Extiende CONSORT para reportar ensayos clínicos de intervenciones con componente de IA, incluyendo sistema, entradas y salidas, interacción humano-IA, errores y análisis.",
        "curricular_function": "Sustentar el diseño y reporte del ensayo de impacto como evaluación prospectiva del sistema en uso frente a un comparador, no solo de la predicción aislada.",
        "limitations": "Es una guía de reporte para ensayos clínicos; no determina por sí sola el diseño causal adecuado, la eficacia, la seguridad, la regulación aplicable ni la monitorización del ciclo de vida.",
    },
    "spirit-ai": {
        "title": "Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI extension",
        "organization": "Nature Medicine / SPIRIT-AI and CONSORT-AI Working Group",
        "year": 2020,
        "doi": "10.1038/s41591-020-1037-7",
        "verification_status": "verified_directly",
        "locator": "Nature Medicine 26:1351–1363 (2020); abstract and SPIRIT-AI extension checklist/explanation; DOI 10.1038/s41591-020-1037-7",
        "role": "Extiende SPIRIT para protocolos de ensayos de intervenciones con IA, incluyendo especificación del sistema, uso previsto, interacción, adquisición de datos y manejo de errores.",
        "curricular_function": "Fundamentar la preespecificación de estudios prospectivos y ensayos de impacto antes de exponer usuarios o pacientes a una nueva versión del sistema.",
        "limitations": "Es una guía de protocolo y reporte; no sustituye gestión de riesgos, aprobación ética, requisitos regulatorios, evaluación temprana ni vigilancia del ciclo de vida.",
    },
    "who-ethics-and-governance-of-artificial-intelligence-for-health": {
        "title": "Ethics and governance of artificial intelligence for health: WHO guidance",
        "organization": "World Health Organization",
        "year": 2021,
        "type": "guía ética y de gobernanza",
        "verification_status": "verified_directly",
        "locator": "WHO publication page, 28 June 2021; ISBN 9789240029200; overview and six consensus principles",
        "role": "Describe desafíos éticos y de gobernanza de la IA para salud y formula seis principios y recomendaciones orientados a diseño, despliegue y uso responsables.",
        "curricular_function": "Aportar el marco de derechos, responsabilidad, transparencia, equidad y gobernanza que limita la evaluación y el ciclo de vida de sistemas de IA en salud.",
        "limitations": "Es orientación ética y de gobernanza de alto nivel; no valida un modelo concreto ni sustituye evaluación clínica, regulación, gestión de riesgos o políticas institucionales.",
    },
}

for source_id, patch in updates.items():
    if source_id not in by_id:
        raise SystemExit(f"Missing source: {source_id}")
    by_id[source_id].update(patch)

PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Closed three Machine Learning source verification gaps")
