#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from migrate_course_to_canonical import build_topics

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"
UNIT_PATH = COURSE / "units" / "unit-03.json"
ASSESSMENT_PATH = COURSE / "assessments" / "unit-03.json"
HIST_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-03.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


hist = load(HIST_PATH)
unit = load(UNIT_PATH)
sources_payload = load(COURSE / "sources.json")
glossary_payload = load(COURSE / "glossary.json")
claims_payload = load(COURSE / "claims.json")

# Integrate authoral theory.
unit["purpose"] = hist["purpose"]
unit["status"]["sources"] = "traceable"
for idx, statement in enumerate(hist["learning_objectives"], start=1):
    unit["learning_outcomes"][idx - 1]["statement"] = statement
unit["topics"] = build_topics(hist, "BIOINST-U03")

# Historical examples use prompt/solution_outline rather than the newer shape.
unit["examples"] = []
for idx, example in enumerate(hist["worked_examples"], start=1):
    unit["examples"].append({
        "id": f"BIOINST-U03-EJ{idx:02d}",
        "title": example["title"],
        "scenario": example["prompt"],
        "reasoning_steps": example["solution_outline"],
        "interpretation": [
            "La geometría y la referencia modifican la diferencia observada sin convertir el canal en una medición celular directa.",
            "El modelo equivalente se acepta solo dentro de la banda, condiciones y parámetros declarados; no representa anatomía exacta.",
            "Un patrón espectral compatible con red es una hipótesis técnica que necesita una prueba discriminante y causas alternativas."
        ][idx - 1],
        "limitations": [
            ["Fuente y conductor sintéticos simplificados.", "No resuelve el problema inverso ni localiza células."],
            ["Modelo Rs + (Rct || Cdl) didáctico y condicionado.", "No demuestra seguridad, conformidad ni comportamiento de una interfaz real concreta."],
            ["Señal y artefacto sintéticos.", "No establece autenticidad fisiológica ni diagnóstico clínico."]
        ][idx - 1],
    })

# Integrated guided activity using the three existing deterministic/offline practices.
unit["activities"] = [{
    "id": "BIOINST-U03-ACT01",
    "title": "Auditoría reproducible de una cadena de biopotencial",
    "purpose": "Reconstruir cómo una fuente bioeléctrica distribuida llega a una medición diferencial, evaluar un modelo limitado de interfaz electrodo-electrolito y diagnosticar artefactos mediante pruebas discriminantes, manteniendo fuera de alcance la adquisición con personas, el diagnóstico y cualquier afirmación de seguridad o conformidad.",
    "prerequisite_unit_ids": ["BIOINST-U02"],
    "instructions": [
        "Empieza por separar escalas: potencial transmembrana, corrientes de membrana, fuentes distribuidas, conductor de volumen, potenciales extracelulares en puntos de observación y diferencia registrada. Declara qué variable existe en cada frontera.",
        "Ejecuta `scripts/bioinstrumentation_u3_practice_u3p1.py` y usa la geometría sintética para comprobar superposición, polaridad y dependencia de la derivación; no interpretes la salida como localización de una célula ni solución inversa.",
        "Ejecuta `scripts/bioinstrumentation_u3_practice_u3p2.py` y analiza magnitud y fase del modelo de interfaz. Modifica Rs, Rct y Cdl para demostrar dependencia de frecuencia y parámetros, registrando que el circuito es equivalente y no anatomía.",
        "Ejecuta `scripts/bioinstrumentation_u3_practice_u3p3.py`. Para cada patrón formula al menos un mecanismo plausible, una prueba discriminante y causas alternativas; una forma de onda limpia o un pico a frecuencia de red no se acepta como prueba suficiente.",
        "Integra la evidencia en un diagrama funcional que distinga entrada de medida, referencia, retorno, blindaje y tierra de protección; termina con una tabla técnica ECG–EEG–EMG por fuente, geometría, escala, banda, interfaz y límites, sin interpretación clínica."
    ],
    "tasks": [
        "Construye una cadena causal desde potencial transmembrana y corriente de membrana hasta dos puntos de observación superficial, señalando en qué transición aparecen superposición, geometría y conducción de volumen.",
        "Usa U3-P1 para comparar al menos dos derivaciones sintéticas; explica cambios de amplitud o polaridad por posiciones y pesos geométricos, no por aparición de una nueva fuente celular.",
        "Deriva e interpreta la diferencia `v_ch(t)=phi(r1,t)-phi(r2,t)` y explica por qué cambiar la referencia modifica el canal observado aunque las fuentes subyacentes no cambien.",
        "Con U3-P2 grafica o tabula magnitud y fase del modelo `Rs + (Rct || Cdl)` entre frecuencias; identifica qué parámetros dominan distintas regiones y qué condiciones impedirían extrapolarlo.",
        "Clasifica cinco nodos o funciones —entrada de medida, referencia de medición, retorno, blindaje y tierra de protección— e identifica qué error conceptual produciría tratarlos como sinónimos.",
        "Diagnostica al menos cuatro patrones de U3-P3 separando artefacto, interferencia y ruido; para cada caso registra mecanismo plausible, prueba que podría refutarlo y una causa alternativa.",
        "Analiza un caso de impedancias de contacto desbalanceadas bajo una perturbación común y explica cómo la asimetría puede convertir parte del modo común en error diferencial; indica qué medición adicional necesitarías.",
        "Construye una comparación ECG–EEG–EMG que incluya fuente distribuida dominante, geometría, orden de magnitud, banda educativa, interfaz y artefactos, y añade explícitamente tres inferencias clínicas prohibidas."
    ],
    "deliverables": [
        "Diagrama de seis capas desde membrana/fuente hasta canal diferencial, con variables, unidades conceptuales, fronteras y supuestos.",
        "Informe U3-P1 con potenciales superficiales, dos derivaciones, interpretación geométrica y límites de superposición/modelo directo.",
        "Informe U3-P2 con barrido complejo, magnitud, fase, comparación de parámetros y caja de límites del circuito equivalente.",
        "Matriz de nodos funcionales y rutas de corriente/información que mantenga separados referencia, retorno, blindaje y tierra de protección.",
        "Matriz U3-P3 de artefactos con patrón, mecanismo, prueba discriminante, alternativas y nivel de certeza.",
        "Tabla técnica ECG–EEG–EMG y síntesis final que declare qué se verificó offline y qué permanece fuera de alcance: adquisición humana, diagnóstico, seguridad, conformidad y utilidad clínica."
    ],
    "checking_criteria": [
        "El potencial transmembrana no se presenta como la tensión medida directamente sobre la piel.",
        "Las fuentes se tratan como distribuidas y la señal superficial conserva dependencia de geometría, conductor de volumen y referencia.",
        "Todo canal se formula como diferencia entre puntos o entradas definidos; la referencia no se considera silenciosa.",
        "El modelo de interfaz incluye media celda cuando corresponda y una impedancia dependiente de frecuencia, con parámetros condicionados y límites explícitos.",
        "Referencia de medición, retorno, blindaje y tierra de protección se distinguen por función y no se sugieren conexiones físicas con personas.",
        "Artefacto, interferencia y ruido no se usan como sinónimos y ninguna clasificación se basa solo en apariencia.",
        "Cada diagnóstico de artefacto incluye una prueba discriminante capaz de debilitar o refutar el mecanismo propuesto.",
        "El análisis de desbalance distingue modo común de error diferencial y no usa el CMRR nominal de un componente como prueba de desempeño del sistema.",
        "La comparación ECG–EEG–EMG conserva diferencias de fuente, geometría, escala, banda e interfaz y no se reduce a amplitud.",
        "La conclusión no afirma diagnóstico, seguridad eléctrica, conformidad normativa, aptitud clínica ni autorización para adquisición con personas."
    ],
    "estimated_duration_minutes": 240,
    "status": "curated_pending_expert_review",
}]
unit["editorial_notice"] = (
    "Contenido educativo canónico integrado desde la fuente autoral histórica, prácticas deterministas y fuentes externas especializadas. "
    "La revisión profesional externa y la revisión humana de la tarea comparativa siguen pendientes. No autoriza conexión de electrodos a personas, diagnóstico, "
    "declaraciones de seguridad ni conformidad. Procedencia histórica: data/course_redevelopment/bioinstrumentacion/units/unit-03.json, "
    "data/practice_implementations/bioinstrumentacion-unit-03.json, data/assessment_implementations/bioinstrumentacion-unit-03.json y "
    "data/editorial_audits/bioinstrumentacion-unit-03.json."
)

# Register/merge sources.
existing = {item["id"]: item for item in sources_payload["sources"]}
url_to_id = {str(item.get("url") or ""): item["id"] for item in sources_payload["sources"] if item.get("url")}

def ensure_source(record: dict) -> str:
    sid = record["id"]
    url = str(record.get("url") or "")
    if sid in existing:
        target = existing[sid]
    elif url and url in url_to_id:
        sid = url_to_id[url]
        target = existing[sid]
    else:
        target = dict(record)
        target["used_by_unit_ids"] = []
        sources_payload["sources"].append(target)
        existing[sid] = target
        if url:
            url_to_id[url] = sid
    for k, v in record.items():
        if v not in (None, "", []) and (not target.get(k) or k in {"verification_status", "locator", "limitations", "curricular_function"}):
            target[k] = v
    if "BIOINST-U03" not in target.setdefault("used_by_unit_ids", []):
        target["used_by_unit_ids"].append("BIOINST-U03")
    return sid

source_records = [
    {"id":"openstax-ap2e-action-potential","type":"open_textbook","title":"Anatomy and Physiology 2e, 12.4 The Action Potential","organization":"OpenStax","url":"https://openstax.org/books/anatomy-and-physiology-2e/pages/12-4-the-action-potential","verification_status":"verified_directly","locator":"Section 12.4 on membrane potential, ionic currents and action potentials","curricular_function":"Ground the cellular scale of transmembrane potential and action potentials before separating it from surface recordings.","coverage":[3],"limitations":"Introductory physiology; does not by itself establish volume-conductor or electrode-interface models."},
    {"id":"malmivuo-plonsey-volume-conductor","type":"academic_textbook","title":"Bioelectromagnetism, Chapter 7 — Volume Source and Volume Conductor","organization":"Malmivuo & Plonsey / Oxford University Press web edition","url":"https://www.bem.fi/book/07/07.htm","verification_status":"verified_directly","locator":"Chapter 7, especially 7.1 concepts of volume source and volume conductor","curricular_function":"Support distributed bioelectric sources, three-dimensional volume conduction, field dependence on source/conductor geometry and limits of forward/inverse interpretation.","coverage":[3],"limitations":"Classical modeling reference; simplified synthetic practice does not reproduce a full anatomical volume conductor or solve an inverse problem."},
    {"id":"body-electrode-interface-review-2021","type":"peer_reviewed_review","title":"Human Body–Electrode Interfaces for Wide-Frequency Sensing and Communication: A Review","organization":"Sensors / PMC","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC8401560/","verification_status":"verified_directly","locator":"Section 2.1: current transfer mechanisms, half-cell potential and equivalent interface models","curricular_function":"Support ion-electron transfer, half-cell potential, double-layer capacitance, charge-transfer resistance and condition-dependent equivalent interface models.","coverage":[3],"limitations":"Review covers broad sensing/communication interfaces; the course uses a deliberately limited Rs + (Rct || Cdl) educational model and does not infer universal parameter values."},
    {"id":"hyoung-koo-common-mode-2026","type":"peer_reviewed_review","title":"Common-Mode Interference in Biopotential Amplifiers: Modeling, Analysis, and Design Strategies for Various Recording Setups","organization":"IEEE Transactions on Biomedical Circuits and Systems","url":"https://pubmed.ncbi.nlm.nih.gov/41129458/","verification_status":"verified_directly","locator":"Abstract and review scope; DOI 10.1109/TBCAS.2025.3624394","curricular_function":"Support common-mode interference reasoning and the effect of asymmetric contact impedance on total common-mode rejection in biopotential recording setups.","coverage":[3,4],"limitations":"Used for conceptual interference/imbalance reasoning, not as a complete design prescription or proof of safety/performance."},
    {"id":"physionet-mit-bih-arrhythmia","type":"open_dataset_documentation","title":"MIT-BIH Arrhythmia Database","organization":"PhysioNet","url":"https://physionet.org/content/mitdb/1.0.0/","verification_status":"verified_directly","locator":"Database description: ECG records, channels, sampling and provenance","curricular_function":"Provide nonclinical/open documentation for ECG channel metadata and technical signal exercises.","coverage":[1,3],"limitations":"No diagnostic interpretation or claim that the historical database represents current populations or devices."},
    {"id":"physionet-eegmmidb","type":"open_dataset_documentation","title":"EEG Motor Movement/Imagery Dataset","organization":"PhysioNet","url":"https://physionet.org/content/eegmmidb/1.0.0/","verification_status":"verified_directly","locator":"Dataset description, EEG channels, electrode configuration and metadata","curricular_function":"Support technical comparison of EEG channel/reference structure using open documentation without new acquisition.","coverage":[3],"limitations":"No neurological classification, diagnosis or generalization of device performance."},
    {"id":"lou-bioelectric-monitoring-2026","type":"peer_reviewed_review","title":"Towards bioelectric signal-enabled human healthcare monitoring: state-of-the-art, design strategies, challenge, and future","organization":"npj Biomedical Innovations","url":"https://doi.org/10.1038/s44385-025-00061-7","verification_status":"verified_directly","locator":"Review sections covering acquisition/front-end considerations for EEG, ECG and EMG","curricular_function":"Contextual comparison of multiple bioelectric modalities and their acquisition challenges while preserving modality-specific sources and interfaces.","coverage":[3,4],"limitations":"Broad review; not used to derive diagnostic criteria or universal amplitude/band values."},
    {"id":"iec-60601-1-overview","type":"standard_metadata","title":"IEC 60601-1 — Medical electrical equipment: general requirements for basic safety and essential performance","organization":"IEC","url":"https://webstore.iec.ch/en/publication/2606","verification_status":"verified_directly","locator":"Official standard page and general scope","curricular_function":"Establish that patient-connected medical electrical equipment has dedicated safety/essential-performance requirements outside the scope of offline educational simulations.","coverage":[3,7,9],"limitations":"Metadata only; no clause-level compliance interpretation, no safety threshold derivation and no conformity claim."},
]
source_ids = [ensure_source(r) for r in source_records]
unit["source_ids"] = list(dict.fromkeys(source_ids))
sources_payload["consulted_on"] = "2026-08-23"

# Make all U3 glossary entries traceable without inventing new historical terms.
entries = {entry["id"]: entry for entry in glossary_payload["entries"]}
for entry_id in unit["glossary_entry_ids"]:
    entry = entries[entry_id]
    term = entry["term"].casefold()
    if any(k in term for k in ["membrana", "ión", "potencial de acción"]):
        sid, loc, status = "openstax-ap2e-action-potential", "OpenStax A&P 2e, section 12.4", "verified_contextually"
    elif any(k in term for k in ["volumen", "fuente", "extracelular", "derivación", "diferencial"]):
        sid, loc, status = "malmivuo-plonsey-volume-conductor", "Bioelectromagnetism, chapter 7", "verified_contextually"
    elif any(k in term for k in ["electrodo", "media celda", "doble capa", "rct", "cdl", "impedancia", "polarización"]):
        sid, loc, status = "body-electrode-interface-review-2021", "Review section 2.1 on electrode–body/electrolyte interfaces", "verified_contextually"
    elif any(k in term for k in ["modo común", "desbalance", "blindaje", "retorno", "referencia", "interferencia"]):
        sid, loc, status = "hyoung-koo-common-mode-2026", "Review scope on common-mode interference and asymmetric contact impedance", "verified_contextually"
    elif "eeg" in term:
        sid, loc, status = "physionet-eegmmidb", "PhysioNet EEGMMIDB data description", "verified_contextually"
    elif "ecg" in term:
        sid, loc, status = "physionet-mit-bih-arrhythmia", "PhysioNet MIT-BIH data description", "verified_contextually"
    elif "emg" in term:
        sid, loc, status = "lou-bioelectric-monitoring-2026", "Review sections comparing bioelectric acquisition modalities", "verified_contextually"
    elif any(k in term for k in ["artefact", "ruido"]):
        sid, loc, status = "hyoung-koo-common-mode-2026", "Review of interference mechanisms; unit taxonomy adds broader artifact classes", "verified_contextually"
    else:
        sid, loc, status = "lou-bioelectric-monitoring-2026", "Review of bioelectric acquisition systems and challenges", "verified_contextually"
    entry["source_ids"] = [sid]
    entry["verification_status"] = status
    entry["source_locators"] = [{"source_id": sid, "locator": loc}]

# Add exact claims from authoral theory: first sentence of each of 18 paragraphs.
def first_sentence(text: str) -> str:
    return re.split(r"(?<=[.!?])\s+", text.strip(), maxsplit=1)[0]

claims_payload["claims"] = [c for c in claims_payload.get("claims", []) if c.get("unit_id") != "BIOINST-U03"]
section_sources = [
    ["openstax-ap2e-action-potential", "malmivuo-plonsey-volume-conductor", "malmivuo-plonsey-volume-conductor"],
    ["malmivuo-plonsey-volume-conductor", "hyoung-koo-common-mode-2026", "malmivuo-plonsey-volume-conductor"],
    ["body-electrode-interface-review-2021"] * 3,
    ["hyoung-koo-common-mode-2026", "hyoung-koo-common-mode-2026", "iec-60601-1-overview"],
    ["hyoung-koo-common-mode-2026", "hyoung-koo-common-mode-2026", "lou-bioelectric-monitoring-2026"],
    ["physionet-mit-bih-arrhythmia", "lou-bioelectric-monitoring-2026", "lou-bioelectric-monitoring-2026"],
]
source_lookup = {s["id"]: s for s in sources_payload["sources"]}
u3_claims = []
for si, section in enumerate(hist["theory_sections"]):
    for pi, paragraph in enumerate(section["paragraphs"]):
        n = si * 3 + pi + 1
        sid = section_sources[si][pi]
        src = source_lookup[sid]
        u3_claims.append({
            "claim_id": f"BIOINST-U03-C{n:03d}", "unit": 3, "text": first_sentence(paragraph),
            "claim_type": "methodological_or_interpretive", "risk": "medium" if si < 4 else "high",
            "context": "Afirmación integrada desde la fuente autoral U3; válida solo dentro del marco de adquisición técnica y modelos declarados, sin inferencia diagnóstica ni de seguridad.",
            "source_id": sid, "locator": {"section": str(src.get("locator") or "fuente localizada")},
            "support": "direct" if si in (0,2) else "indirect", "source_verification_status": src["verification_status"],
            "review_state": "ai_review_provisional", "reviewer_validation_id": None, "reviewed_at": "2026-08-23",
            "id": f"BIOINST-U03-C{n:03d}", "unit_id": "BIOINST-U03"
        })
claims_payload["claims"].extend(u3_claims)
claims_payload["scope"] = "Afirmaciones centrales de las Unidades 1–3 con fuentes y localizadores; revisión profesional externa pendiente."
claims_payload["review_state"] = "ai_review_provisional"
claims_payload["content_version"] = "units-01-03-review-2026-08-23"
unit["claim_ids"] = [c["id"] for c in u3_claims]

# Case-based assessment.
def case(qid, prompt, los, difficulty, cognitive, expected, explanation, misconceptions, sids):
    return {"id":qid,"type":"case_analysis","prompt":prompt,"linked_learning_outcome_ids":los,"difficulty":difficulty,"cognitive_level":cognitive,
            "answer_key":{"expected_answer":expected,"explanation":explanation,"common_misconceptions":misconceptions},
            "feedback":{"correct":"La respuesta conserva escalas, geometría, interfaz y nivel de evidencia sin convertir una observación técnica en diagnóstico o seguridad.","incorrect":"Reconstruye la cadena por capas y añade una prueba discriminante o evidencia faltante antes de asignar un mecanismo o significado."},
            "source_ids":sids,"status":"curated_pending_expert_review"}
assessment = {
 "$schema":"../../../../schemas/academic/assessment-v1.schema.json","schema_version":"1.0","id":"BIOINST-U03-EVAL","course_id":"bioinstrumentacion","scope":"unit","unit_id":"BIOINST-U03",
 "purpose":"Evaluar razonamiento técnico sobre generación, conducción, interfaz, referencia y artefactos de biopotenciales sin interpretación diagnóstica ni instrucciones de conexión con personas.",
 "student_payload_policy":"Las claves y feedback se excluyen del payload inicial. La comparación integradora ECG–EEG–EMG y cualquier razonamiento abierto pueden requerir revisión humana; no se automatiza aprobación semántica profesional.",
 "items":[
 case("BIOINST-U03-Q01","Un estudiante afirma que un electrodo superficial de ECG mide directamente el potencial de acción de cardiomiocitos. Reconstruye la cadena física correcta desde membrana hasta canal superficial y señala al menos tres transformaciones que invalidan esa equivalencia.",["BIOINST-U03-LO01"],"intermediate","analyze","Debe separar potencial transmembrana/corrientes, fuente tisular distribuida, conductor de volumen, potenciales extracelulares en posiciones y diferencia registrada. Geometría, superposición y referencia impiden equiparar señal superficial con una célula.","El registro superficial es un campo/diferencia resultante de fuentes distribuidas y del conductor, no una lectura intracelular.",["surface-equals-membrane","single-source"],["openstax-ap2e-action-potential","malmivuo-plonsey-volume-conductor"]),
 case("BIOINST-U03-Q02","En U3-P1 dos derivaciones cambian de polaridad al intercambiar posiciones mientras la fuente sintética permanece idéntica. Explica el resultado y qué conclusión sobre localización o identidad de la fuente sería ilegítima.",["BIOINST-U03-LO01"],"intermediate","evaluate","La diferencia observada depende de los puntos de observación y la geometría. Cambiar la derivación puede cambiar signo y amplitud sin cambiar la fuente. El modelo sintético no resuelve el problema inverso ni localiza células.","La geometría de la derivación forma parte de la medición; una topografía o canal no identifica de manera única una fuente interna.",["electrode-placement-universal","single-source"],["malmivuo-plonsey-volume-conductor"]),
 case("BIOINST-U03-Q03","El barrido U3-P2 se ajusta con una fuente de media celda y `Rs + (Rct || Cdl)`. Interpreta qué representa cada elemento, por qué la impedancia es compleja y dependiente de frecuencia y qué sería incorrecto afirmar sobre piel, gel o electrodo real.",["BIOINST-U03-LO02"],"advanced","analyze","Rs resume una contribución serie; Rct representa transferencia de carga y Cdl la doble capa en el modelo; el paralelo produce dependencia de magnitud/fase con frecuencia. Los parámetros dependen de material, área, preparación, tiempo y condiciones y no son anatomía ni constantes universales.","El circuito es un modelo equivalente de comportamiento electroquímico, no un mapa físico exacto de capas tisulares.",["electrode-ideal-conductor","dc-offset-is-physiology"],["body-electrode-interface-review-2021"]),
 case("BIOINST-U03-Q04","En un diagrama aparecen `REF`, `BIAS/RETURN`, `SHIELD` y `PE`. Un alumno une todos porque «son tierra». Clasifica sus funciones y explica por qué el esquema no debe convertirse en instrucciones físicas de conexión a una persona.",["BIOINST-U03-LO03"],"advanced","evaluate","La referencia define la diferencia de medición; el retorno proporciona una ruta funcional de corrientes de polarización/control según arquitectura; el blindaje controla acoplamiento; la tierra de protección pertenece a seguridad. No son sinónimos ni necesariamente equipotenciales. La unidad no autoriza conexión humana.","Los nombres de nodo no sustituyen función, trayectoria ni arquitectura de aislamiento; seguridad real pertenece a requisitos específicos de equipos médicos.",["reference-equals-ground","reference-is-silent","simulation-proves-safety"],["hyoung-koo-common-mode-2026","iec-60601-1-overview"]),
 case("BIOINST-U03-Q05","Dos contactos tienen impedancias muy distintas y existe una perturbación común de red. El canal muestra más componente de 50 Hz. Explica un mecanismo plausible y diseña una prueba discriminante sin atribuir automáticamente el pico a la red.",["BIOINST-U03-LO02","BIOINST-U03-LO04"],"advanced","create","La asimetría de contacto/fuente puede degradar el rechazo total y convertir parte del modo común en diferencial. Una prueba puede equilibrar/intercambiar impedancias o modificar el acoplamiento y observar si la componente cambia como predice el mecanismo; deben mantenerse alternativas.","La frecuencia visible sugiere un mecanismo pero no lo demuestra; el análisis necesita perturbación controlada y comparación.",["high-impedance-only-amplitude","clean-waveform-is-physiology"],["hyoung-koo-common-mode-2026"]),
 case("BIOINST-U03-Q06","Una señal sintética presenta deriva lenta, ráfagas asociadas a movimiento y una línea estrecha a frecuencia de red. Clasifica observaciones como artefacto/interferencia/ruido solo cuando la evidencia lo permita y propone una prueba discriminante y una alternativa para cada patrón.",["BIOINST-U03-LO04"],"advanced","evaluate","Debe separar patrones y mecanismos, no usar categorías como sinónimos. Movimiento/contacto pueden explicar transitorios o deriva; una línea estrecha puede ser interferencia acoplada; ruido describe variabilidad más amplia. Cada hipótesis necesita prueba y alternativa.","La apariencia aislada es insuficiente y múltiples mecanismos pueden coexistir.",["artifact-equals-noise","clean-waveform-is-physiology","dc-offset-is-physiology"],["hyoung-koo-common-mode-2026","lou-bioelectric-monitoring-2026"]),
 case("BIOINST-U03-Q07","Construye una comparación técnica de ECG, EEG y EMG. Un compañero propone ordenarlas solo por amplitud y usar esa amplitud para inferir corazón normal, estado neurológico o fuerza muscular. Corrige la comparación y esas inferencias.",["BIOINST-U03-LO05"],"advanced","evaluate","La comparación debe incluir fuente distribuida, geometría/derivación, escala, banda, referencia, interfaz, acondicionamiento y artefactos. Amplitud aislada no autoriza diagnóstico cardíaco, estado neurológico ni equivalencia directa entre EMG y fuerza.","Las modalidades comparten principios de adquisición pero no fuente, geometría ni significado; calidad técnica no equivale a interpretación clínica.",["ecg-eeg-emg-differ-only-amplitude","component-performance-is-clinical-utility"],["physionet-mit-bih-arrhythmia","physionet-eegmmidb","lou-bioelectric-monitoring-2026"]),
 case("BIOINST-U03-Q08","El paquete offline produce señales limpias, un ajuste razonable de impedancia y baja interferencia. El equipo quiere afirmar que el sistema es seguro para conectar a pacientes y que sirve para diagnóstico. Evalúa la conclusión y define qué evidencia faltaría antes de cualquiera de esas afirmaciones.",["BIOINST-U03-LO01","BIOINST-U03-LO02","BIOINST-U03-LO03","BIOINST-U03-LO04","BIOINST-U03-LO05"],"advanced","evaluate","La conclusión excede totalmente la evidencia. Simulaciones y datos abiertos verifican ejercicios técnicos limitados. Seguridad exige arquitectura y ensayos aplicables; diagnóstico/validez clínica exige evidencia y procesos clínicos apropiados. La unidad prohíbe conexión humana.","Reproducibilidad offline no sustituye conformidad, evaluación profesional, validación clínica ni autorización institucional.",["simulation-proves-safety","clean-waveform-is-physiology"],["iec-60601-1-overview","physionet-mit-bih-arrhythmia","physionet-eegmmidb"])
 ],"status":"curated_pending_expert_review"}

dump(UNIT_PATH, unit); dump(ASSESSMENT_PATH, assessment); dump(COURSE/"sources.json", sources_payload); dump(COURSE/"glossary.json", glossary_payload); dump(COURSE/"claims.json", claims_payload)

# Permanent regression.
(ROOT/"tests"/"test_bioinstrumentacion_unit_03_curated.py").write_text('''from __future__ import annotations\n\nimport json\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nCOURSE = ROOT / "data" / "courses" / "bioinstrumentacion"\n\nclass BioinstrumentacionUnit03CuratedTests(unittest.TestCase):\n    def setUp(self):\n        self.unit=json.loads((COURSE/"units"/"unit-03.json").read_text(encoding="utf-8"))\n        self.assessment=json.loads((COURSE/"assessments"/"unit-03.json").read_text(encoding="utf-8"))\n        self.glossary=json.loads((COURSE/"glossary.json").read_text(encoding="utf-8"))\n        self.sources=json.loads((COURSE/"sources.json").read_text(encoding="utf-8"))\n        self.claims=json.loads((COURSE/"claims.json").read_text(encoding="utf-8"))\n    def test_theory_examples_and_review_boundary(self):\n        self.assertEqual(len(self.unit["topics"]),6)\n        self.assertEqual(sum(len(t["subtopics"]) for t in self.unit["topics"]),18)\n        self.assertEqual(len(self.unit["examples"]),3)\n        self.assertEqual(self.unit["status"]["sources"],"traceable")\n        packet=json.loads((ROOT/"data/review_packets/bioinstrumentacion-unit-03-professional-review.json").read_text(encoding="utf-8"))\n        self.assertFalse(packet["current_claims"]["external_professional_review_completed"])\n        self.assertFalse(packet["current_claims"]["professional_approval_obtained"])\n    def test_activity_contract(self):\n        a=self.unit["activities"][0]\n        self.assertEqual(a["status"],"curated_pending_expert_review")\n        self.assertEqual(a["estimated_duration_minutes"],240)\n        self.assertEqual((len(a["instructions"]),len(a["tasks"]),len(a["deliverables"]),len(a["checking_criteria"])),(5,8,6,10))\n        text=" ".join(a["instructions"]+a["tasks"]).lower()\n        self.assertIn("u3_practice_u3p1",text); self.assertIn("u3_practice_u3p2",text); self.assertIn("u3_practice_u3p3",text)\n    def test_assessment(self):\n        self.assertEqual(self.assessment["status"],"curated_pending_expert_review")\n        self.assertEqual(len(self.assessment["items"]),8)\n        covered=set()\n        for q in self.assessment["items"]:\n            self.assertEqual(q["type"],"case_analysis"); self.assertTrue(q["source_ids"]); self.assertTrue(q["answer_key"]["explanation"]); self.assertTrue(q["answer_key"]["common_misconceptions"]); covered.update(q["linked_learning_outcome_ids"])\n        self.assertEqual(covered,{f"BIOINST-U03-LO{i:02d}" for i in range(1,6)})\n    def test_glossary_claims_sources(self):\n        entries={e["id"]:e for e in self.glossary["entries"]}\n        self.assertTrue(self.unit["glossary_entry_ids"])\n        for eid in self.unit["glossary_entry_ids"]:\n            e=entries[eid]; self.assertNotEqual(e["verification_status"],"unverified"); self.assertTrue(e["source_ids"]); self.assertTrue(e.get("source_locators"))\n        u3=[c for c in self.claims["claims"] if c.get("unit_id")=="BIOINST-U03"]\n        self.assertEqual(len(u3),18); self.assertEqual(self.unit["claim_ids"],[c["id"] for c in u3])\n        serialized=json.dumps(self.unit,ensure_ascii=False)\n        for c in u3: self.assertIn(c["text"],serialized); self.assertEqual(c["review_state"],"ai_review_provisional"); self.assertTrue(c["locator"])\n        sids={s["id"] for s in self.sources["sources"]}\n        required={"malmivuo-plonsey-volume-conductor","body-electrode-interface-review-2021","hyoung-koo-common-mode-2026","openstax-ap2e-action-potential","physionet-mit-bih-arrhythmia","physionet-eegmmidb","lou-bioelectric-monitoring-2026","iec-60601-1-overview"}\n        self.assertTrue(required.issubset(sids)); self.assertTrue(required.issubset(set(self.unit["source_ids"])))\n\nif __name__=="__main__": unittest.main()\n''',encoding="utf-8")
print("Curated Bioinstrumentation U3")
