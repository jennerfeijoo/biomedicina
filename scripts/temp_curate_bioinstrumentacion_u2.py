#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from migrate_course_to_canonical import build_examples, build_topics

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"
UNIT_PATH = COURSE / "units" / "unit-02.json"
ASSESSMENT_PATH = COURSE / "assessments" / "unit-02.json"
HIST_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"
EXAMPLES_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "unit-02-source" / "examples.json"
GLOSSARY_PARTS = [
    ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "unit-02-source" / "glossary-01.json",
    ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "unit-02-source" / "glossary-02.json",
]
SOURCE_REGISTRY = ROOT / "data" / "source_registry" / "bioinstrumentacion-unit-02.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


hist = load(HIST_PATH)
unit = load(UNIT_PATH)
sources_payload = load(COURSE / "sources.json")
glossary_payload = load(COURSE / "glossary.json")
claims_payload = load(COURSE / "claims.json")
specific_sources = load(SOURCE_REGISTRY)

# --- Authoral theory and examples -------------------------------------------------
unit["purpose"] = hist["purpose"]
unit["status"]["sources"] = "traceable"
for index, statement in enumerate(hist["learning_objectives"], start=1):
    unit["learning_outcomes"][index - 1]["statement"] = statement
unit["topics"] = build_topics(hist, "BIOINST-U02")
unit["examples"] = build_examples(load(EXAMPLES_PATH), "BIOINST-U02")

unit["activities"] = [
    {
        "id": "BIOINST-U02-ACT01",
        "title": "Caracterización, dinámica y selección de transductores",
        "purpose": "Caracterizar de forma reproducible funciones estáticas y dinámicas, auditar mecanismos de carga y convertir requisitos de medición en una selección multicriterio sin transferir especificaciones de componente a desempeño de sistema o utilidad clínica.",
        "prerequisite_unit_ids": ["BIOINST-U01"],
        "instructions": [
            "Parte del mensurando y del uso previsto definidos en la Unidad 1. Declara rango, variable de entrada, salida esperada, condiciones y qué bloque considerarás sensor, transductor, interfaz y acondicionamiento.",
            "Ejecuta `scripts/generate_bioinstrumentation_u2_static_dataset.py` y analiza las curvas sintéticas conservando unidades, intervalo, dirección del barrido, residuos y controles que permitan distinguir linealidad local, saturación, zona muerta e histéresis.",
            "Ejecuta `scripts/generate_bioinstrumentation_u2_dynamic_dataset.py`; estima la constante de tiempo solo en el caso compatible con primer orden y usa los controles con retardo, sobreimpulso o ausencia de eje temporal para demostrar cuándo el modelo simple debe rechazarse.",
            "Ejecuta la auditoría offline `scripts/audit_bioinstrumentation_u2_datasheets.py` sobre los registros compactos del termistor, la galga y el fotodiodo. Separa valor típico, máximo, condición de ensayo, propiedad de componente y evidencia faltante de la cadena.",
            "Integra los resultados en una matriz de selección: requisitos obligatorios, criterios comparables, compensaciones, mecanismos de carga, evidencia disponible y plan de verificación. Cierra con límites explícitos de transferencia a sistema, seguridad y clínica."
        ],
        "tasks": [
            "Clasifica al menos dieciséis elementos de cadenas de ejemplo por función y formula dos fronteras alternativas coherentes, declarando qué cambia en las cantidades de entrada y salida.",
            "Para cada curva estática sintética identifica el patrón dominante, calcula o interpreta sensibilidad local, usa residuos o dirección del barrido y propone una prueba capaz de refutar tu diagnóstico.",
            "Distingue saturación, zona muerta, histéresis, deriva y no linealidad; explica por qué una única recta, un R² alto o una lectura de resolución no bastan para separar esos fenómenos.",
            "Estima tau en el caso dinámico compatible, calcula la fracción de respuesta esperada y explica por qué tiempo de respuesta al escalón, constante de tiempo y ancho de banda no son sinónimos universales.",
            "Rechaza explícitamente el modelo simple de primer orden cuando existan retardo no modelado, sobreimpulso/oscilación o ausencia de información temporal; propone qué modelo o evidencia adicional sería necesaria.",
            "Construye cuatro rutas de carga: eléctrica por impedancias, térmica por autocalentamiento, mecánica por montaje/masa/rigidez y óptica por geometría/fuente/ambiente. Identifica la cantidad perturbada y una mitigación no garantizada.",
            "Audita las fichas del NTCLG100E2103JB, CEA-06-125UNA-350 y S5821-03 distinguiendo magnitud, unidad, condición, categoría de especificación y aquello que no puede extrapolarse a otra pieza o a la cadena completa.",
            "Resuelve un caso nuevo de selección multicriterio con rango, sensibilidad, selectividad, carga, dinámica, entorno y calibrabilidad; justifica una alternativa elegida, una descartada y las pruebas pendientes antes de aceptar el diseño."
        ],
        "deliverables": [
            "Mapa funcional con sensor, transductor, interfaz, acondicionamiento, entradas, salidas y dos fronteras alternativas justificadas.",
            "Informe de caracterización estática con datos/manifiesto reproducibles, curvas, sensibilidad local, residuos, clasificación de no idealidades y pruebas de refutación.",
            "Informe dinámico con estimación de tau, criterio de aceptación del primer orden, controles negativos y límites de cualquier relación con tiempo de respuesta o ancho de banda.",
            "Mapa de carga con cuatro mecanismos, cantidad perturbada, evidencia faltante y mitigaciones formuladas como hipótesis de diseño.",
            "Auditoría documental de los tres componentes con procedencia, condiciones, categorías de especificación y prohibiciones de transferencia a sistema o clínica.",
            "Matriz final de selección y plan de verificación, acompañados de una conclusión que separe evidencia de componente, evidencia de cadena y afirmaciones todavía no demostradas."
        ],
        "checking_criteria": [
            "La clasificación funcional depende de entradas, salidas e interfaz y no del nombre comercial del componente.",
            "Toda sensibilidad conserva unidades, intervalo y condiciones; no se usa como sinónimo de resolución, exactitud o selectividad.",
            "Linealidad, saturación, zona muerta, histéresis y deriva se distinguen mediante patrones y pruebas diferentes.",
            "La interpretación estática declara modelo de referencia, dirección del barrido y dominio; no se globaliza un ajuste local.",
            "El modelo de primer orden solo se acepta cuando la evidencia temporal es compatible y sus supuestos quedan escritos.",
            "Tau, tiempo de respuesta al escalón y ancho de banda se mantienen conceptualmente separados salvo una relación derivada bajo un modelo explícito.",
            "La carga se analiza como interacción causal y se identifica qué cantidad del objeto, interfaz o cadena resulta perturbada.",
            "Las hojas de datos se citan con condición y categoría de especificación; los valores típicos no se convierten en garantías.",
            "La selección compara requisitos y compensaciones múltiples y no elige un sensor por una sola métrica.",
            "La conclusión no afirma desempeño de sistema, seguridad, conformidad o utilidad clínica a partir de datos sintéticos o especificaciones de componente."
        ],
        "estimated_duration_minutes": 240,
        "status": "curated_pending_expert_review",
    }
]
unit["editorial_notice"] = (
    "Contenido educativo canónico integrado desde la fuente autoral histórica y prácticas sintéticas/documentales existentes. "
    "La revisión disciplinaria humana sigue pendiente; esta curación no autoriza adquisición con personas, desempeño de sistema, "
    "seguridad, conformidad ni utilidad clínica. Procedencia: data/course_redevelopment/bioinstrumentacion/units/unit-02.json, "
    "data/practice_implementations/bioinstrumentacion-unit-02.json y data/assessment_implementations/bioinstrumentacion-unit-02.json."
)

# --- Canonical sources ------------------------------------------------------------
existing = {item["id"]: item for item in sources_payload["sources"]}
url_to_id = {str(item.get("url") or ""): item["id"] for item in sources_payload["sources"] if item.get("url")}


def ensure_source(requested_id: str, record: dict) -> str:
    url = str(record.get("url") or "")
    if requested_id in existing:
        target = existing[requested_id]
    elif url and url in url_to_id:
        target = existing[url_to_id[url]]
        requested_id = target["id"]
    else:
        target = dict(record)
        target["id"] = requested_id
        target.setdefault("type", "fuente técnica")
        target.setdefault("verification_status", "verified_directly")
        target.setdefault("coverage", [2])
        target.setdefault("limitations", "Usar solo dentro del alcance y las condiciones documentadas.")
        target["used_by_unit_ids"] = []
        sources_payload["sources"].append(target)
        existing[requested_id] = target
        if url:
            url_to_id[url] = requested_id
    used = target.setdefault("used_by_unit_ids", [])
    if "BIOINST-U02" not in used:
        used.append("BIOINST-U02")
    return target["id"]

alias_request = {
    "vim3-transducer-3-7": "bipm-vim-transducer",
    "vim3-sensor-3-8": "bipm-vim-sensor",
    "vim3-sensitivity-4-12": "bipm-vim-sensitivity",
    "vim3-selectivity-4-13": "bipm-vim-selectivity",
    "vim3-step-response-4-23": "bipm-vim-step-response-time",
    "jcgm-gum-6-2020-u2": "jcgm-gum-6-2020",
    "mit-20-309-sensors": "mit-20-309",
    "nibib-sensors-u2": "nibib-sensors",
    "vishay-ntc-thermistor-u2": "vishay-ntc-thermistor-u2",
    "ni-strain-gage-u2": "ni-strain-gage-u2",
    "hamamatsu-photodiode-u2": "hamamatsu-photodiode-u2",
}
actual: dict[str, str] = {}
for src in specific_sources["sources"]:
    requested = alias_request[src["id"]]
    actual[requested] = ensure_source(requested, src)

manual_sources = [
    {
        "id": "bipm-vim-input-quantity",
        "title": "VIM3 2.50 — input quantity in a measurement model",
        "organization": "Joint Committee for Guides in Metrology / BIPM",
        "url": "https://jcgm.bipm.org/vim/en/2.50.html",
        "type": "terminología metrológica oficial",
        "verification_status": "verified_directly",
        "locator": "VIM3 entry 2.50 and notes",
        "curricular_function": "Definir cantidad de entrada del modelo y distinguirla de la salida y de la mera variable de software.",
        "coverage": [2],
        "limitations": "La entrada no especifica por sí sola el modelo físico ni la calidad de las cantidades de entrada."
    },
    {
        "id": "bipm-vim-output-quantity",
        "title": "VIM3 2.51 — output quantity in a measurement model",
        "organization": "Joint Committee for Guides in Metrology / BIPM",
        "url": "https://jcgm.bipm.org/vim/en/2.51.html",
        "type": "terminología metrológica oficial",
        "verification_status": "verified_directly",
        "locator": "VIM3 entry 2.51",
        "curricular_function": "Definir cantidad de salida del modelo de medición.",
        "coverage": [2],
        "limitations": "No equivale necesariamente a la salida eléctrica del transductor ni a una indicación intermedia."
    },
    {
        "id": "bipm-vim-measuring-interval",
        "title": "VIM3 4.7 — measuring interval",
        "organization": "Joint Committee for Guides in Metrology / BIPM",
        "url": "https://jcgm.bipm.org/vim/en/4.7.html",
        "type": "terminología metrológica oficial",
        "verification_status": "verified_directly",
        "locator": "VIM3 entry 4.7 and notes",
        "curricular_function": "Distinguir intervalo de medición bajo condiciones e incertidumbre especificadas de una cifra de rango sin contexto.",
        "coverage": [2, 8],
        "limitations": "No implica desempeño uniforme en todo el intervalo ni equivale a límite de detección."
    },
    {
        "id": "bipm-vim-dead-band",
        "title": "VIM3 4.17 — dead band",
        "organization": "Joint Committee for Guides in Metrology / BIPM",
        "url": "https://jcgm.bipm.org/vim/en/4.17.html",
        "type": "terminología metrológica oficial",
        "verification_status": "verified_directly",
        "locator": "VIM3 entry 4.17 and note",
        "curricular_function": "Sostener la distinción entre banda/zona muerta, resolución, umbral y detectabilidad.",
        "coverage": [2],
        "limitations": "La actividad usa una zona muerta sintética como caso pedagógico; la definición formal de dead band depende del cambio en ambas direcciones y de detectabilidad."
    },
    {
        "id": "bipm-vim-instrumental-drift",
        "title": "VIM3 4.21 — instrumental drift",
        "organization": "Joint Committee for Guides in Metrology / BIPM",
        "url": "https://jcgm.bipm.org/vim/en/4.21.html",
        "type": "terminología metrológica oficial",
        "verification_status": "verified_directly",
        "locator": "VIM3 entry 4.21 and note",
        "curricular_function": "Distinguir deriva instrumental de cambio del mensurando, influencia reconocida, ruido e histéresis.",
        "coverage": [2, 8],
        "limitations": "No identifica por sí sola el mecanismo físico de una deriva observada."
    },
]
for record in manual_sources:
    actual[record["id"]] = ensure_source(record["id"], record)

requested_unit_sources = [
    "bipm-vim-sensor", "bipm-vim-transducer", "bipm-vim-input-quantity", "bipm-vim-output-quantity",
    "bipm-vim-sensitivity", "bipm-vim-selectivity", "bipm-vim-measuring-interval", "bipm-vim-dead-band",
    "bipm-vim-instrumental-drift", "bipm-vim-step-response-time", "jcgm-gum-6-2020", "mit-20-309",
    "nibib-sensors", "vishay-ntc-thermistor-u2", "ni-strain-gage-u2", "hamamatsu-photodiode-u2",
]
unit["source_ids"] = [actual.get(source_id, source_id) for source_id in requested_unit_sources]

# --- Glossary: promote the 20 authoral terms --------------------------------------
other_refs = set()
for path in sorted((COURSE / "units").glob("unit-*.json")):
    if path.name == "unit-02.json":
        continue
    other_refs.update(load(path)["glossary_entry_ids"])
for entry in glossary_payload["entries"]:
    entry["unit_ids"] = [uid for uid in entry.get("unit_ids", []) if uid != "BIOINST-U02"]
glossary_payload["entries"] = [
    entry for entry in glossary_payload["entries"] if entry.get("unit_ids") or entry["id"] in other_refs
]

terms = []
for path in GLOSSARY_PARTS:
    terms.extend(load(path)["glossary"])
next_glossary = max(int(entry["id"].rsplit("-", 1)[1]) for entry in glossary_payload["entries"]) + 1
by_term = {entry["term"].casefold(): entry for entry in glossary_payload["entries"]}
term_source = {
    "sensor": ("bipm-vim-sensor", "VIM3 entry 3.8 and examples", "verified_directly"),
    "transductor de medición": ("bipm-vim-transducer", "VIM3 entry 3.7 and examples", "verified_directly"),
    "interfaz": ("jcgm-gum-6-2020", "JCGM GUM-6:2020 clauses 5.6–6.6", "verified_contextually"),
    "cantidad de entrada": ("bipm-vim-input-quantity", "VIM3 entry 2.50 and notes", "verified_directly"),
    "cantidad de salida": ("bipm-vim-output-quantity", "VIM3 entry 2.51", "verified_directly"),
    "función estática": ("jcgm-gum-6-2020", "JCGM GUM-6:2020 clauses 5.3, 5.6–6.6", "verified_contextually"),
    "sensibilidad": ("bipm-vim-sensitivity", "VIM3 entry 4.12 and notes", "verified_directly"),
    "selectividad": ("bipm-vim-selectivity", "VIM3 entry 4.13 and notes", "verified_directly"),
    "offset": ("jcgm-gum-6-2020", "JCGM GUM-6:2020 model effects and corrections", "verified_contextually"),
    "rango": ("bipm-vim-measuring-interval", "VIM3 entry 4.7 and notes", "verified_contextually"),
    "no linealidad": ("jcgm-gum-6-2020", "JCGM GUM-6:2020 model adequacy and omitted effects", "verified_contextually"),
    "saturación": ("vishay-ntc-thermistor-u2", "Product datasheet/application-note conditions; used only as component context", "verified_contextually"),
    "zona muerta": ("bipm-vim-dead-band", "VIM3 entry 4.17 and note; pedagogical mapping is limited", "verified_contextually"),
    "histéresis": ("ni-strain-gage-u2", "Measurement implementation context; synthetic practice supplies the pattern", "verified_contextually"),
    "deriva": ("bipm-vim-instrumental-drift", "VIM3 entry 4.21 and note", "verified_directly"),
    "carga": ("jcgm-gum-6-2020", "Model effects and interaction boundary; component cases add mechanisms", "verified_contextually"),
    "modelo de orden cero": ("jcgm-gum-6-2020", "Model simplification and adequacy clauses", "verified_contextually"),
    "constante de tiempo": ("vishay-ntc-thermistor-u2", "Datasheet dynamic specifications plus limited first-order educational model", "verified_contextually"),
    "tiempo de respuesta al escalón": ("bipm-vim-step-response-time", "VIM3 entry 4.23", "verified_directly"),
    "ancho de banda": ("hamamatsu-photodiode-u2", "Cut-off specification under stated component conditions; chain transfer prohibited", "verified_contextually"),
}
unit_glossary_ids = []
source_lookup = {item["id"]: item for item in sources_payload["sources"]}
for item in terms:
    key = item["term"].casefold()
    entry = by_term.get(key)
    if entry is None:
        entry = {
            "id": f"BIOINST-GLO-{next_glossary:03d}",
            "term": item["term"],
            "definition": item["definition"],
            "unit_ids": [],
            "source_ids": [],
            "verification_status": "unverified",
        }
        next_glossary += 1
        glossary_payload["entries"].append(entry)
        by_term[key] = entry
    entry["definition"] = item["definition"]
    if "BIOINST-U02" not in entry["unit_ids"]:
        entry["unit_ids"].append("BIOINST-U02")
    requested, locator, verification = term_source[key]
    sid = actual.get(requested, requested)
    entry["source_ids"] = [sid]
    entry["verification_status"] = verification
    entry["source_locators"] = [{"source_id": sid, "locator": locator}]
    unit_glossary_ids.append(entry["id"])
unit["glossary_entry_ids"] = unit_glossary_ids

# --- Claims: exact first sentences from the authoral theory -----------------------
def first_sentence(text: str) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text.strip(), maxsplit=1)
    return parts[0].strip()

source_by_section = [
    ["bipm-vim-sensor", "bipm-vim-transducer", "jcgm-gum-6-2020"],
    ["jcgm-gum-6-2020", "bipm-vim-sensitivity", "jcgm-gum-6-2020"],
    ["jcgm-gum-6-2020", "vishay-ntc-thermistor-u2", "bipm-vim-dead-band"],
    ["bipm-vim-step-response-time", "bipm-vim-step-response-time", "jcgm-gum-6-2020"],
    ["ni-strain-gage-u2", "vishay-ntc-thermistor-u2", "hamamatsu-photodiode-u2"],
    ["jcgm-gum-6-2020", "mit-20-309", "nibib-sensors"],
]
claims_payload["claims"] = [claim for claim in claims_payload.get("claims", []) if claim.get("unit_id") != "BIOINST-U02"]
u2_claims = []
for section_index, section in enumerate(hist["theory_sections"]):
    for paragraph_index, paragraph in enumerate(section["paragraphs"][:3]):
        number = section_index * 3 + paragraph_index + 1
        requested = source_by_section[section_index][paragraph_index]
        sid = actual.get(requested, requested)
        source = source_lookup.get(sid) or next(item for item in sources_payload["sources"] if item["id"] == sid)
        text = first_sentence(paragraph)
        direct_vim = sid.startswith("bipm-vim-")
        claim = {
            "claim_id": f"BIOINST-U02-C{number:03d}",
            "unit": 2,
            "text": text,
            "claim_type": "definition" if direct_vim else "methodological_or_interpretive",
            "risk": "low" if direct_vim else "medium",
            "context": "Afirmación integrada desde la fuente autoral histórica de U2; se limita al modelo, componente, condiciones y frontera declarados y no demuestra desempeño clínico o de sistema.",
            "source_id": sid,
            "locator": {"section": str(source.get("locator") or "fuente localizada en registro U2")},
            "support": "direct" if direct_vim else "indirect",
            "source_verification_status": str(source.get("verification_status") or "verified_directly"),
            "review_state": "ai_review_provisional",
            "reviewer_validation_id": None,
            "reviewed_at": "2026-08-23",
            "id": f"BIOINST-U02-C{number:03d}",
            "unit_id": "BIOINST-U02",
        }
        u2_claims.append(claim)
claims_payload["claims"].extend(u2_claims)
claims_payload["scope"] = "Afirmaciones centrales de las Unidades 1 y 2 con fuente y localizador; revisión disciplinaria humana pendiente."
claims_payload["review_state"] = "ai_review_provisional"
claims_payload["content_version"] = "units-01-02-review-2026-08-23"
unit["claim_ids"] = [claim["id"] for claim in u2_claims]

# --- Assessment -------------------------------------------------------------------
def case(qid, prompt, outcomes, difficulty, cognitive, expected, explanation, misconceptions, source_ids):
    return {
        "id": qid,
        "type": "case_analysis",
        "prompt": prompt,
        "linked_learning_outcome_ids": outcomes,
        "difficulty": difficulty,
        "cognitive_level": cognitive,
        "answer_key": {
            "expected_answer": expected,
            "explanation": explanation,
            "common_misconceptions": misconceptions,
        },
        "feedback": {
            "correct": "La respuesta distingue propiedades, condiciones y nivel de evidencia sin extrapolar más allá de la cadena analizada.",
            "incorrect": "Reconstruye primero la frontera, las cantidades y las condiciones; después decide qué propiedad o modelo puede sostener realmente la evidencia."
        },
        "source_ids": [actual.get(source_id, source_id) for source_id in source_ids],
        "status": "curated_pending_expert_review",
    }

assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "BIOINST-U02-EVAL",
    "course_id": "bioinstrumentacion",
    "scope": "unit",
    "unit_id": "BIOINST-U02",
    "purpose": "Evaluar si el estudiante puede clasificar funciones, caracterizar comportamiento estático y dinámico, diagnosticar carga y seleccionar transductores con evidencia y límites explícitos.",
    "student_payload_policy": "En una aplicación dinámica, answer_key y feedback se excluyen del payload inicial; los razonamientos abiertos y la selección multicriterio siguen requiriendo revisión humana cuando corresponda.",
    "items": [
        case(
            "BIOINST-U02-Q01",
            "Una galga resistiva está adherida a una viga y conectada a un puente cuya salida entra en un amplificador. Propón dos fronteras válidas para el análisis y clasifica sensor, transductor, interfaz y acondicionamiento en cada una. ¿Qué no puede decidirse solo por el nombre comercial?",
            ["BIOINST-U02-LO01"], "intermediate", "analyze",
            "Debe identificarse el elemento directamente afectado, las cantidades de entrada/salida y la interfaz. Una frontera puede terminar en el cambio de resistencia y otra incluir el puente para producir tensión; la clasificación cambia con la frontera, pero no puede ocultar adhesivo, excitación, conductores ni acondicionamiento.",
            "Sensor y transductor son roles funcionales. Una pieza puede participar en más de una frontera sin que ambos términos se vuelvan sinónimos universales.",
            ["Llamar sensor a toda la cadena.", "Suponer que sensor y transductor son siempre equivalentes.", "Clasificar por marca o encapsulado."],
            ["bipm-vim-sensor", "bipm-vim-transducer", "ni-strain-gage-u2"],
        ),
        case(
            "BIOINST-U02-Q02",
            "Una curva entrada–salida se aproxima linealmente entre 20 y 40 °C. Calculas una pendiente de 45 mV/K y un offset. Explica qué debe acompañar a esos números y por qué 45 mV/K no significa mejor resolución, exactitud o selectividad.",
            ["BIOINST-U02-LO02"], "intermediate", "analyze",
            "La sensibilidad debe declararse con unidades, intervalo, referencia, condiciones y método de estimación; el offset requiere una condición de referencia. Resolución, exactitud y selectividad son propiedades distintas y no se deducen de una pendiente grande.",
            "Una función estática es local al dominio y condiciones ensayados; una métrica aislada no caracteriza toda la cadena.",
            ["Mayor sensibilidad implica siempre mejor sensor.", "Confundir offset con error total.", "Extrapolar una pendiente local fuera del intervalo."],
            ["bipm-vim-sensitivity", "bipm-vim-selectivity", "bipm-vim-measuring-interval"],
        ),
        case(
            "BIOINST-U02-Q03",
            "Cuatro curvas sintéticas muestran: mesetas en extremos; salida constante alrededor de cero; ramas distintas al subir y bajar; y un desplazamiento gradual entre bloques temporales. Identifica el mecanismo dominante de cada patrón y propone una prueba que pueda refutar tu diagnóstico.",
            ["BIOINST-U02-LO03"], "advanced", "evaluate",
            "Los patrones son compatibles respectivamente con saturación, zona/banda muerta, histéresis y deriva. Deben usarse extensión de rango, inspección de pendiente cerca de cero, inversión/repetición de barrido y controles temporales/ambientales para intentar refutarlos.",
            "No idealidades distintas requieren diseños de prueba distintos; una curva o un R² aislado no identifica mecanismos.",
            ["Llamar ruido a toda separación de ramas.", "Confundir zona muerta con resolución.", "Tratar deriva como cambio del mensurando sin control temporal."],
            ["bipm-vim-dead-band", "bipm-vim-instrumental-drift", "jcgm-gum-6-2020"],
        ),
        case(
            "BIOINST-U02-Q04",
            "Tras un escalón, DY01 es monótono y compatible con tau≈2 s; DY02 tiene 0,4 s de retardo puro; DY03 presenta sobreimpulso; DY04 no tiene eje temporal. Decide en cuáles aceptarías un modelo simple de primer orden y por qué.",
            ["BIOINST-U02-LO04"], "advanced", "evaluate",
            "Solo DY01 admite aceptación limitada del primer orden si la fracción de respuesta y residuos son compatibles. Retardo no modelado, sobreimpulso/oscilación y ausencia de información temporal invalidan el modelo simple declarado y requieren un modelo compuesto o evidencia adicional.",
            "Aceptar un modelo significa que es adecuado dentro del dominio y criterios ensayados, no que describa toda la física del transductor.",
            ["Forzar un ajuste de primer orden a cualquier transición.", "Ignorar retardo porque la curva final parece exponencial.", "Usar datos estacionarios para inferir dinámica."],
            ["bipm-vim-step-response-time", "jcgm-gum-6-2020"],
        ),
        case(
            "BIOINST-U02-Q05",
            "Un fabricante publica «response time» y otra ficha ofrece una frecuencia de corte típica. Un estudiante afirma que ambos valores determinan directamente tau y el ancho de banda de la cadena. Evalúa la afirmación.",
            ["BIOINST-U02-LO04", "BIOINST-U02-LO05"], "advanced", "evaluate",
            "El tiempo de respuesta al escalón depende del cambio y del criterio de asentamiento especificados y no equivale automáticamente a tau. La relación fc=1/(2πτ) solo deriva de un modelo lineal de primer orden bajo supuestos explícitos. Una frecuencia de corte del componente no es el ancho de banda de la cadena completa.",
            "Las métricas dinámicas dependen de modelo, criterio y condiciones de ensayo; no se transfieren mecánicamente entre componente y sistema.",
            ["Response time siempre equivale a tau.", "Frecuencia de corte del componente equivale a ancho de banda del sistema.", "Rápido significa exacto."],
            ["bipm-vim-step-response-time", "vishay-ntc-thermistor-u2", "hamamatsu-photodiode-u2"],
        ),
        case(
            "BIOINST-U02-Q06",
            "Analiza cuatro afirmaciones: una entrada de amplificador nunca carga una red resistiva; aumentar excitación de un termistor no cambia su temperatura; una galga no modifica una estructura pequeña; la frecuencia de corte del fotodiodo demuestra la de toda la cadena. Para cada una identifica ruta de carga, cantidad perturbada y evidencia faltante.",
            ["BIOINST-U02-LO03", "BIOINST-U02-LO05"], "advanced", "analyze",
            "Deben distinguirse carga eléctrica por divisor de impedancias, autocalentamiento/transferencia térmica, masa-rigidez-montaje mecánico y geometría/fuente/carga electrónica óptica. Cada ruta necesita parámetros y medidas propias; las mitigaciones son propuestas que deben verificarse.",
            "Medir modifica o puede modificar el objeto y la cadena de formas específicas; «carga» no es un único mecanismo.",
            ["Suponer interacción despreciable sin parámetros.", "Mezclar carga eléctrica y mecánica.", "Usar una ficha como prueba del sistema."],
            ["jcgm-gum-6-2020", "vishay-ntc-thermistor-u2", "ni-strain-gage-u2", "hamamatsu-photodiode-u2"],
        ),
        case(
            "BIOINST-U02-Q07",
            "Compara un termistor NTCLG100E2103JB, una galga CEA-06-125UNA-350 y un fotodiodo S5821-03 usando sus registros documentales. ¿Qué campos debes conservar para que una especificación sea interpretable y cuáles no pueden generalizarse a la familia o a la cadena?",
            ["BIOINST-U02-LO02", "BIOINST-U02-LO05"], "intermediate", "evaluate",
            "Deben conservarse propiedad, magnitud, unidad, condición de ensayo, categoría típica/máxima/garantizada cuando exista, modelo exacto, versión y procedencia. Valores del componente no se generalizan a otros modelos ni prueban desempeño de la cadena, montaje, algoritmo o aplicación biomédica.",
            "Una hoja de datos es evidencia de componente bajo condiciones documentadas, no certificado de desempeño de un sistema construido con ese componente.",
            ["Copiar un valor típico como garantía.", "Omitir longitud de onda, excitación o medio.", "Generalizar una cifra a todos los sensores de la misma familia."],
            ["vishay-ntc-thermistor-u2", "ni-strain-gage-u2", "hamamatsu-photodiode-u2"],
        ),
        case(
            "BIOINST-U02-Q08",
            "Debes elegir un transductor para una cadena educativa nueva. Dos candidatos intercambian mayor sensibilidad por más carga y menor margen dinámico. Diseña una regla de selección y explica qué pruebas deben ocurrir antes de declarar que la alternativa elegida es adecuada.",
            ["BIOINST-U02-LO01", "BIOINST-U02-LO02", "BIOINST-U02-LO03", "BIOINST-U02-LO04", "BIOINST-U02-LO05"], "advanced", "create",
            "La selección debe partir de requisitos priorizados y comparar rango, sensibilidad, selectividad, carga, dinámica, entorno, alimentación, calibrabilidad y evidencia con definiciones/condiciones compatibles. Después debe verificarse el componente integrado en la interfaz y cadena. No se concluyen seguridad, conformidad o utilidad clínica.",
            "No existe un sensor universalmente mejor; la elección es una hipótesis de diseño condicionada por requisitos y necesita verificación integrada.",
            ["Elegir por la mayor sensibilidad.", "Usar una sola métrica agregada sin requisitos obligatorios.", "Convertir desempeño de componente en utilidad clínica."],
            ["jcgm-gum-6-2020", "mit-20-309", "nibib-sensors"],
        ),
    ],
    "status": "curated_pending_expert_review",
}

# Finalize source lookup after additions.
source_lookup = {item["id"]: item for item in sources_payload["sources"]}
for claim in u2_claims:
    source = source_lookup[claim["source_id"]]
    claim["locator"] = {"section": str(source.get("locator") or "fuente localizada")}

# Course source registry state remains partial until all units are curated.
sources_payload["consulted_on"] = "2026-08-23"
dump(UNIT_PATH, unit)
dump(ASSESSMENT_PATH, assessment)
dump(COURSE / "sources.json", sources_payload)
dump(COURSE / "glossary.json", glossary_payload)
dump(COURSE / "claims.json", claims_payload)

# Permanent regression.
test_path = ROOT / "tests" / "test_bioinstrumentacion_unit_02_curated.py"
test_path.write_text('''from __future__ import annotations\n\nimport json\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nCOURSE = ROOT / "data" / "courses" / "bioinstrumentacion"\n\n\nclass BioinstrumentacionUnit02CuratedTests(unittest.TestCase):\n    def setUp(self) -> None:\n        self.unit = json.loads((COURSE / "units" / "unit-02.json").read_text(encoding="utf-8"))\n        self.assessment = json.loads((COURSE / "assessments" / "unit-02.json").read_text(encoding="utf-8"))\n        self.glossary = json.loads((COURSE / "glossary.json").read_text(encoding="utf-8"))\n        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))\n        self.claims = json.loads((COURSE / "claims.json").read_text(encoding="utf-8"))\n\n    def test_authoral_theory_and_examples_are_integrated(self) -> None:\n        self.assertEqual(len(self.unit["topics"]), 6)\n        self.assertEqual(sum(len(topic["subtopics"]) for topic in self.unit["topics"]), 24)\n        paragraphs = [block["text"] for topic in self.unit["topics"] for sub in topic["subtopics"] for block in sub["blocks"] if block["type"] == "paragraph"]\n        self.assertEqual(len(paragraphs), 24)\n        self.assertGreaterEqual(sum(len(text.split()) for text in paragraphs), 2200)\n        self.assertEqual(len(self.unit["examples"]), 3)\n        self.assertEqual(self.unit["status"]["sources"], "traceable")\n        self.assertEqual(self.unit["status"]["internal_review"], "pending")\n        self.assertEqual(self.unit["status"]["external_review"], "pending")\n        handoff = json.loads((ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-02.json").read_text(encoding="utf-8"))\n        self.assertFalse(handoff["decision_state_now"]["disciplinary_review_completed"])\n\n    def test_activity_is_reproducible_and_scaffolded(self) -> None:\n        activity = self.unit["activities"][0]\n        self.assertEqual(activity["status"], "curated_pending_expert_review")\n        self.assertEqual(activity["estimated_duration_minutes"], 240)\n        self.assertEqual(len(activity["instructions"]), 5)\n        self.assertEqual(len(activity["tasks"]), 8)\n        self.assertEqual(len(activity["deliverables"]), 6)\n        self.assertEqual(len(activity["checking_criteria"]), 10)\n        joined = " ".join(activity["instructions"] + activity["tasks"] + activity["deliverables"]).lower()\n        self.assertIn("static_dataset", joined)\n        self.assertIn("dynamic_dataset", joined)\n        self.assertIn("datasheets", joined)\n\n    def test_assessment_covers_all_outcomes_with_sources_and_feedback(self) -> None:\n        self.assertEqual(self.assessment["status"], "curated_pending_expert_review")\n        self.assertEqual(len(self.assessment["items"]), 8)\n        covered = set()\n        for item in self.assessment["items"]:\n            self.assertEqual(item["type"], "case_analysis")\n            self.assertEqual(item["status"], "curated_pending_expert_review")\n            self.assertNotEqual(item["difficulty"], "unclassified")\n            self.assertNotEqual(item["cognitive_level"], "unclassified")\n            self.assertTrue(item["answer_key"]["explanation"])\n            self.assertTrue(item["answer_key"]["common_misconceptions"])\n            self.assertTrue(item["feedback"]["correct"])\n            self.assertTrue(item["feedback"]["incorrect"])\n            self.assertTrue(item["source_ids"])\n            covered.update(item["linked_learning_outcome_ids"])\n        self.assertEqual(covered, {f"BIOINST-U02-LO{i:02d}" for i in range(1, 6)})\n\n    def test_twenty_authoral_glossary_terms_are_traceable(self) -> None:\n        entries = {entry["id"]: entry for entry in self.glossary["entries"]}\n        self.assertEqual(len(self.unit["glossary_entry_ids"]), 20)\n        for entry_id in self.unit["glossary_entry_ids"]:\n            entry = entries[entry_id]\n            self.assertIn("BIOINST-U02", entry["unit_ids"])\n            self.assertNotEqual(entry["verification_status"], "unverified")\n            self.assertTrue(entry["source_ids"])\n            self.assertTrue(entry.get("source_locators"))\n\n    def test_claims_are_exactly_present_and_traceable(self) -> None:\n        u2_claims = [claim for claim in self.claims["claims"] if claim.get("unit_id") == "BIOINST-U02"]\n        self.assertEqual(len(u2_claims), 18)\n        self.assertEqual(self.unit["claim_ids"], [claim["id"] for claim in u2_claims])\n        serialized = json.dumps(self.unit, ensure_ascii=False)\n        for claim in u2_claims:\n            self.assertIn(claim["text"], serialized)\n            self.assertEqual(claim["review_state"], "ai_review_provisional")\n            self.assertTrue(claim["source_id"])\n            self.assertTrue(claim["locator"])\n\n    def test_specific_metrology_and_component_sources_are_registered(self) -> None:\n        source_ids = {item["id"] for item in self.sources["sources"]}\n        required = {\n            "bipm-vim-sensor", "bipm-vim-transducer", "bipm-vim-sensitivity", "bipm-vim-selectivity",\n            "bipm-vim-input-quantity", "bipm-vim-output-quantity", "bipm-vim-measuring-interval",\n            "bipm-vim-dead-band", "bipm-vim-instrumental-drift", "bipm-vim-step-response-time",\n            "vishay-ntc-thermistor-u2", "ni-strain-gage-u2", "hamamatsu-photodiode-u2"\n        }\n        self.assertTrue(required.issubset(source_ids))\n        self.assertTrue(required.issubset(set(self.unit["source_ids"])))\n\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")

print("Curated Bioinstrumentation U2 canonical corpus")
