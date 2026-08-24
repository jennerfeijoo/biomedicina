from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"
SOURCES_PATH = COURSE / "sources.json"

payload = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
sources = {item["id"]: item for item in payload["sources"]}

consort = sources["consort-ai"]
consort["verification_status"] = "verified_directly"
consort["locator"] = "Abstract; CONSORT-AI extension checklist and explanation, Nature Medicine 26:1364–1374 (2020)"
consort["limitations"] = "Es una guía de reporte para ensayos clínicos con un componente de IA; no determina por sí sola la elección del diseño, la regulación aplicable, la monitorización posdespliegue ni la eficacia clínica."

spirit = sources["spirit-ai"]
spirit["verification_status"] = "verified_directly"
spirit["locator"] = "Abstract; SPIRIT-AI extension checklist and explanation, Nature Medicine 26:1351–1363 (2020)"
spirit["limitations"] = "Es una guía para protocolos de ensayos clínicos con un componente de IA; no sustituye gestión de riesgos, requisitos regulatorios, evaluación clínica temprana ni vigilancia del ciclo de vida."

who = sources["who-ethics-and-governance-of-artificial-intelligence-for-health"]
who.update(
    {
        "registry_id": "who-ethics-and-governance-of-artificial-intelligence-for-health",
        "title": "Ethics and governance of artificial intelligence for health",
        "organization": "World Health Organization",
        "year": 2021,
        "url": "https://www.who.int/publications/i/item/9789240029200",
        "type": "guía de ética y gobernanza",
        "verification_status": "verified_directly",
        "locator": "Overview; six consensus principles; WHO guidance, 28 June 2021, ISBN 9789240029200",
        "role": "Proporciona un marco de ética, derechos humanos y gobernanza para el diseño, despliegue y uso de inteligencia artificial en salud.",
        "curricular_function": "Servir como fuente transversal para discutir autonomía, bienestar y seguridad, transparencia, responsabilidad, equidad y sostenibilidad sin convertir principios éticos en métricas técnicas automáticas.",
        "limitations": "Es una guía internacional de ética y gobernanza; no sustituye legislación local, evaluación regulatoria, validación clínica, gestión de riesgos específica ni evidencia de desempeño de un sistema concreto.",
        "used_by_unit_ids": [],
    }
)

payload["consulted_on"] = "2026-08-24"
SOURCES_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Closed the three remaining Machine Learning source-verification gaps")
