from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


glossary_path = COURSE / "glossary.json"
glossary = load(glossary_path)
entries = {item["id"]: item for item in glossary["entries"]}

fixes = {
    "BIOINST-GLO-049": {
        "definition": "Obtención de valores de una señal en instantes definidos por un reloj o regla temporal de muestreo.",
        "source_ids": ["ni-analog-signal-acquisition"],
        "verification_status": "verified_contextually",
        "source_locators": [{"source_id": "ni-analog-signal-acquisition", "locator": "Bandwidth, sample rate, Nyquist Sampling Theorem and acquisition discussion"}],
    },
    "BIOINST-GLO-053": {
        "definition": "Incremento de código menos significativo usado para expresar el tamaño nominal de un paso de un convertidor ideal dentro de un rango declarado.",
        "source_ids": ["adi-adc-glossary"],
        "verification_status": "verified_directly",
        "source_locators": [{"source_id": "adi-adc-glossary", "locator": "ADC glossary: LSB / code-width terminology"}],
    },
    "BIOINST-GLO-055": {
        "definition": "Limitación de la representación cuando la señal excede el rango que una etapa o convertidor puede representar válidamente.",
        "source_ids": ["ni-analog-signal-acquisition"],
        "verification_status": "verified_contextually",
        "source_locators": [{"source_id": "ni-analog-signal-acquisition", "locator": "Analog input range and acquisition limits; clipping interpretation used contextually"}],
    },
    "BIOINST-GLO-058": {
        "definition": "Variación muestra a muestra del instante efectivo en que el ADC toma la muestra respecto del evento temporal ideal o de referencia.",
        "source_ids": ["adi-aperture-jitter"],
        "verification_status": "verified_directly",
        "source_locators": [{"source_id": "adi-aperture-jitter", "locator": "Aperture jitter: sample-to-sample variation in aperture delay"}],
    },
    "BIOINST-GLO-072": {
        "definition": "Radiación que no sigue la trayectoria óptica prevista y alcanza el sistema de detección por una ruta distinta, pudiendo rodear la muestra o aparecer en una región espectral no correspondiente.",
        "source_ids": ["iupac-stray-light-2025"],
        "verification_status": "verified_directly",
        "source_locators": [{"source_id": "iupac-stray-light-2025", "locator": "IUPAC Gold Book term 08293, stray light"}],
    },
    "BIOINST-GLO-073": {
        "definition": "Peligro cuya fuente potencial de daño está asociada a energía eléctrica; en el curso se analiza como parte de una cadena de riesgo y no como declaración de conformidad.",
        "source_ids": ["iso-14971-2019-current", "iec-60601-1-edition-3-2"],
        "verification_status": "verified_contextually",
        "source_locators": [
            {"source_id": "iso-14971-2019-current", "locator": "ISO 14971 official scope and risk-management terminology context"},
            {"source_id": "iec-60601-1-edition-3-2", "locator": "IEC 60601-1 consolidated edition 3.2 scope: basic safety and essential performance"},
        ],
    },
    "BIOINST-GLO-074": {
        "definition": "Camino conductivo completo considerado por el modelo para que circule corriente entre los nodos o dominios declarados.",
        "source_ids": ["circuits-and-electronics"],
        "verification_status": "verified_contextually",
        "source_locators": [{"source_id": "circuits-and-electronics", "locator": "Closed-circuit, current-path and Kirchhoff-law context"}],
    },
    "BIOINST-GLO-075": {
        "definition": "Parte de una trayectoria conductiva que permite cerrar el circuito y retornar corriente hacia la fuente o referencia del modelo.",
        "source_ids": ["circuits-and-electronics"],
        "verification_status": "verified_contextually",
        "source_locators": [{"source_id": "circuits-and-electronics", "locator": "Closed-circuit and current-return context"}],
    },
    "BIOINST-GLO-076": {
        "definition": "Medida física o funcional destinada a limitar una transferencia de energía o una exposición dentro de la arquitectura de riesgo declarada.",
        "source_ids": ["iso-14971-2019-current", "iec-60601-1-edition-3-2"],
        "verification_status": "verified_contextually",
        "source_locators": [
            {"source_id": "iso-14971-2019-current", "locator": "Risk-control framework and protective-measure context"},
            {"source_id": "iec-60601-1-edition-3-2", "locator": "General basic-safety architecture context; no numeric requirement reproduced"},
        ],
    },
    "BIOINST-GLO-077": {
        "definition": "Separación o sistema aislante destinado a restringir conducción eléctrica no prevista entre circuitos, partes o dominios definidos.",
        "source_ids": ["iec-60601-1-edition-3-2"],
        "verification_status": "verified_contextually",
        "source_locators": [{"source_id": "iec-60601-1-edition-3-2", "locator": "General electrical-safety and insulation context; no detailed test limit reproduced"}],
    },
    "BIOINST-GLO-083": {
        "definition": "Circuito, subsistema o función susceptible cuya respuesta puede alterarse por una perturbación electromagnética en el modelo de compatibilidad.",
        "source_ids": ["fda-emc-overview-2026"],
        "verification_status": "verified_contextually",
        "source_locators": [{"source_id": "fda-emc-overview-2026", "locator": "FDA EMC overview: electromagnetic disturbances, emissions and immunity context"}],
    },
}

for entry_id, patch in fixes.items():
    if entry_id not in entries:
        raise SystemExit(f"Missing glossary entry {entry_id}")
    entries[entry_id].update(patch)

dump(glossary_path, glossary)

sources_path = COURSE / "sources.json"
sources = load(sources_path)
source_ids = {item["id"] for item in sources["sources"]}
if "iupac-stray-light-2025" not in source_ids:
    sources["sources"].append({
        "id": "iupac-stray-light-2025",
        "title": "IUPAC Gold Book — stray light (08293)",
        "organization": "International Union of Pure and Applied Chemistry",
        "url": "https://goldbook.iupac.org/terms/view/08293",
        "type": "terminología científica oficial",
        "verification_status": "verified_directly",
        "locator": "Gold Book term 08293; online version 5.0.0 (2025), definition sourced to PAC 2021, 93, 647",
        "curricular_function": "Definir luz parásita en el contexto óptico de U6 y distinguir trayectorias ópticas no previstas de transmitancia/absorbancia idealizadas.",
        "limitations": "La definición espectroscópica no caracteriza por sí sola el diseño óptico de un sensor biomédico concreto.",
        "coverage": [6],
        "used_by_unit_ids": ["BIOINST-U06"],
    })
dump(sources_path, sources)

unit6_path = COURSE / "units" / "unit-06.json"
unit6 = load(unit6_path)
if "iupac-stray-light-2025" not in unit6["source_ids"]:
    unit6["source_ids"].append("iupac-stray-light-2025")
dump(unit6_path, unit6)

print("Resolved 11 Bioinstrumentation glossary content gaps")
