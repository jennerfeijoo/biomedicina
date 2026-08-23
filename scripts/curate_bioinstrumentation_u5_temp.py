#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"
UNIT_PATH = COURSE / "units" / "unit-05.json"
ASSESSMENT_PATH = COURSE / "assessments" / "unit-05.json"
GLOSSARY_PATH = COURSE / "glossary.json"
SOURCES_PATH = COURSE / "sources.json"
CLAIMS_PATH = COURSE / "claims.json"
MIGRATION_PATH = ROOT / "data" / "course_migrations" / "bioinstrumentacion-numbering-v1.json"
LEGACY_UNIT_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-04.json"
LEGACY_SOURCE_PATH = ROOT / "data" / "source_registry" / "bioinstrumentacion-unit-04.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


unit = load(UNIT_PATH)
assessment = load(ASSESSMENT_PATH)
glossary = load(GLOSSARY_PATH)
sources = load(SOURCES_PATH)
claims = load(CLAIMS_PATH)
migration = load(MIGRATION_PATH)
legacy = load(LEGACY_UNIT_PATH)
legacy_sources = load(LEGACY_SOURCE_PATH)

crosswalk = next(item for item in migration["canonical_sequence"] if item["canonical_unit"] == 5)
assert crosswalk["origin"] == "legacy_unit_4"
assert crosswalk["action"] == "migrate_without_rewriting"
assert legacy["unit"] == 4
assert legacy["limits"]["professional_review_claimed"] is False
assert legacy["limits"]["public_release_authorized"] is False
assert legacy["limits"]["U4-A5_status"] == "pending_real_human_review"

# --- Canonical source registry -------------------------------------------------

def add_or_update_source(record: dict) -> None:
    existing = next((x for x in sources["sources"] if x["id"] == record["id"]), None)
    if existing is None:
        sources["sources"].append(record)
        return
    for key, value in record.items():
        if key == "used_by_unit_ids":
            existing[key] = sorted(set(existing.get(key, [])) | set(value))
        elif key not in existing or existing[key] in (None, "", [], {}):
            existing[key] = value
    if "BIOINST-U05" not in existing.setdefault("used_by_unit_ids", []):
        existing["used_by_unit_ids"].append("BIOINST-U05")

legacy_org = {
    "ni-analog-signal-acquisition": "National Instruments",
    "ni-anti-alias-filters": "National Instruments",
    "adi-adc-glossary": "Analog Devices",
    "adi-quantization-glossary": "Analog Devices",
    "adi-data-conversion-calculator": "Analog Devices",
    "physionet-mit-bih-arrhythmia": "PhysioNet",
    "iec-60601-1-overview": "International Electrotechnical Commission",
}
for item in legacy_sources["sources"]:
    add_or_update_source({
        "id": item["id"],
        "title": item["title"],
        "organization": legacy_org.get(item["id"], "Fuente técnica institucional"),
        "url": item["url"],
        "type": item.get("type", "technical_reference"),
        "verification_status": item.get("verification_status", "verified_directly"),
        "locator": "; ".join(item.get("authorized_claims", []))[:900] or "Recurso consultado directamente",
        "curricular_function": "Respaldar la migración legacy U4 → canonical U5 sin reescribir la evidencia histórica.",
        "limitations": item.get("limitations", "Debe conservarse el alcance y las condiciones de la fuente."),
        "coverage": [5],
        "used_by_unit_ids": ["BIOINST-U05"],
    })

new_sources = [
    {
        "id": "adi-enob-dynamic-2019",
        "title": "How to Calculate ENOB for ADC Dynamic Performance Measurement",
        "organization": "Analog Devices",
        "url": "https://www.analog.com/en/resources/technical-articles/how-to-calculate-enob-for-adc-dynamic-performance-measurement.html",
        "type": "manufacturer_technical_article",
        "verification_status": "verified_directly",
        "locator": "Sections 'How Are SNR, SINAD, THD, and ENOB Related?' and 'Effective Number of Bits'",
        "curricular_function": "Relacionar SINAD y ENOB como métricas dinámicas del ADC bajo condiciones de prueba declaradas.",
        "limitations": "Fuente de fabricante; la relación matemática no convierte ENOB en exactitud DC ni en desempeño universal de una cadena biomédica.",
        "coverage": [5],
        "used_by_unit_ids": ["BIOINST-U05"],
    },
    {
        "id": "adi-adc-dynamic-parameters",
        "title": "Defining and Testing Dynamic Parameters in High-Speed ADCs, Part 1",
        "organization": "Analog Devices",
        "url": "https://www.analog.com/en/resources/technical-articles/defining-and-testing-dynamic-parameters-in-highspeed-adcs-part-1.html",
        "type": "manufacturer_technical_article",
        "verification_status": "verified_directly",
        "locator": "Sections 'Signal-to-Noise and Distortion Ratio (SINAD)' and 'Effective Number of Bits (ENOB)'",
        "curricular_function": "Documentar que SINAD/ENOB dependen de frecuencia, amplitud, muestreo y procedimiento de ensayo.",
        "limitations": "Se usa para principios de caracterización dinámica; no generaliza cifras de convertidores concretos.",
        "coverage": [5],
        "used_by_unit_ids": ["BIOINST-U05"],
    },
    {
        "id": "adi-aperture-jitter",
        "title": "Types of ADCs and DACs — Aperture Delay and Aperture Jitter",
        "organization": "Analog Devices",
        "url": "https://www.analog.com/en/resources/technical-articles/types-of-adcs-and-dacs.html",
        "type": "manufacturer_technical_reference",
        "verification_status": "verified_directly",
        "locator": "Sections 'Aperture Delay' and 'Aperture Jitter'",
        "curricular_function": "Distinguir instante de muestreo, retardo de apertura y variación muestra a muestra.",
        "limitations": "Referencia general; la contribución de jitter de una cadena real depende del ADC, reloj, señal y arquitectura.",
        "coverage": [5],
        "used_by_unit_ids": ["BIOINST-U05"],
    },
    {
        "id": "ni-sample-clock-2025",
        "title": "Sample Clock",
        "organization": "National Instruments",
        "url": "https://www.ni.com/docs/en-US/bundle/ni-scope/page/sample-clock.html/",
        "type": "official_technical_documentation",
        "verification_status": "verified_directly",
        "locator": "Sections 'Internal Sample Clock', 'Decimation Method' and 'External Sample Clock'",
        "curricular_function": "Distinguir el reloj que controla la adquisición de una simple marca temporal posterior.",
        "limitations": "La arquitectura descrita es propia de familias de digitizadores NI y no constituye una topología universal.",
        "coverage": [5],
        "used_by_unit_ids": ["BIOINST-U05"],
    },
    {
        "id": "ni-synchronization-explained",
        "title": "NI-DAQmx Synchronization of PXI Express Modules",
        "organization": "National Instruments",
        "url": "https://www.ni.com/en/support/documentation/supplemental/10/synchronization-explained.html",
        "type": "official_technical_documentation",
        "verification_status": "verified_directly",
        "locator": "Sections 'Synchronization Approaches and Options' and 'Sample Clock Synchronization'",
        "curricular_function": "Mostrar que sincronización requiere arquitectura de reloj/trigger y que pueden existir skew y retardos aun con señales compartidas.",
        "limitations": "Ejemplos de hardware NI; los conceptos se usan para razonar sobre arquitectura, no para prescribir dispositivos.",
        "coverage": [5],
        "used_by_unit_ids": ["BIOINST-U05"],
    },
    {
        "id": "nist-time-measurement",
        "title": "Time Measurement",
        "organization": "National Institute of Standards and Technology",
        "url": "https://www.nist.gov/publications/time-measurement",
        "type": "institutional_reference",
        "verification_status": "verified_directly",
        "locator": "Overview of time interval measurement, clocks, time transfer and synchronization",
        "curricular_function": "Respaldar la separación conceptual entre medición temporal, comparación de relojes y sincronización.",
        "limitations": "Referencia metrológica general; no define por sí sola el error temporal admisible de una aplicación biomédica.",
        "coverage": [5],
        "used_by_unit_ids": ["BIOINST-U05"],
    },
    {
        "id": "rfc3550-sequence-timestamp",
        "title": "RFC 3550 — RTP: A Transport Protocol for Real-Time Applications",
        "organization": "IETF / RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc3550.html",
        "type": "internet_standard",
        "verification_status": "verified_directly",
        "locator": "Section 5.1 sequence number and timestamp fields; Appendix A sequence validation",
        "curricular_function": "Proporcionar un ejemplo normativo de uso de contadores para detectar pérdida/orden y de timestamps derivados de un reloj de muestreo.",
        "limitations": "RTP no es un protocolo obligatorio para bioinstrumentación; se usa como ejemplo explícito de mecanismos de integridad temporal y no como arquitectura prescrita.",
        "coverage": [5],
        "used_by_unit_ids": ["BIOINST-U05"],
    },
]
for source in new_sources:
    add_or_update_source(source)

sources["consulted_on"] = "2026-08-24"

# --- Theory -------------------------------------------------------------------
claim_texts = [
    ("El muestreo representa una señal mediante valores asociados a instantes definidos por un reloj de adquisición.", "ni-sample-clock-2025", "Sample Clock overview", "definition", "medium", "direct"),
    ("La condición de Nyquist presupone una señal limitada en banda; en una cadena real también deben declararse la banda analógica presente y el filtrado previo.", "ni-analog-signal-acquisition", "Bandwidth, Nyquist Sampling Theorem, and Aliasing", "interpretation_boundary", "medium", "direct"),
    ("El filtro anti-alias debe actuar antes del muestreo y del ADC; un filtro digital posterior no recupera la identidad de componentes que ya se plegaron.", "ni-anti-alias-filters", "Overview and practical anti-alias filter discussion", "methodological_requirement", "high", "direct"),
    ("Una componente por encima de la frecuencia de Nyquist puede aparecer como una frecuencia inferior en los datos muestreados.", "ni-analog-signal-acquisition", "Aliasing examples and alias-frequency calculation", "methodological_requirement", "medium", "direct"),
    ("Un ADC asigna muestras analógicas a un conjunto finito de códigos digitales respecto de un rango y una referencia.", "adi-adc-glossary", "ADC definition", "definition", "low", "direct"),
    ("Para un cuantizador uniforme ideal, el LSB nominal se obtiene dividiendo el rango total entre 2^N códigos y no equivale a exactitud.", "adi-quantization-glossary", "Quantization definition and finite code intervals", "interpretation_boundary", "medium", "indirect"),
    ("La cuantización ideal debe mantenerse separada de offset, error de ganancia, no linealidad, ruido y saturación del convertidor real.", "adi-adc-dynamic-parameters", "Dynamic performance definitions and measured error discussion", "interpretation_boundary", "medium", "indirect"),
    ("Cuando el ADC satura, valores analógicos diferentes pueden producir el mismo código extremo y la información perdida no puede reconstruirse a partir de ese código.", "adi-adc-glossary", "ADC finite input range and coding boundary", "interpretation_boundary", "high", "indirect"),
    ("SINAD compara la señal con ruido y distorsión bajo una frecuencia, amplitud, tasa de muestreo y procedimiento de ensayo declarados.", "adi-adc-dynamic-parameters", "SINAD section", "definition", "medium", "direct"),
    ("La relación ENOB=(SINAD-1.76)/6.02 es una convención para desempeño dinámico con entrada senoidal y no una medida de exactitud en continua.", "adi-enob-dynamic-2019", "Effective Number of Bits section", "interpretation_boundary", "medium", "direct"),
    ("ENOB puede cambiar con la frecuencia y amplitud de entrada y con la configuración de muestreo, por lo que una cifra aislada no caracteriza todos los usos.", "adi-adc-dynamic-parameters", "ENOB discussion", "interpretation_boundary", "high", "direct"),
    ("El jitter de apertura describe variación muestra a muestra del instante de muestreo y es distinto del retardo de apertura medio.", "adi-aperture-jitter", "Aperture Delay and Aperture Jitter", "definition", "medium", "direct"),
    ("Timestamps iguales no demuestran por sí solos que dos conversiones analógicas ocurrieron simultáneamente.", "ni-synchronization-explained", "Sample clock synchronization and delay/skew discussion", "interpretation_boundary", "high", "indirect"),
    ("La sincronización multicanal debe documentar qué reloj, referencia y trigger controlan la adquisición y qué skew o retardo permanece.", "ni-synchronization-explained", "Synchronization approaches", "methodological_requirement", "high", "direct"),
    ("La deriva de reloj acumula error temporal entre relojes que avanzan a tasas ligeramente diferentes y debe distinguirse de variaciones rápidas de instante como el jitter.", "nist-time-measurement", "Time interval measurement and synchronization overview", "interpretation_boundary", "medium", "indirect"),
    ("Un contador de secuencia definido para avanzar de forma conocida permite detectar discontinuidades, duplicados o reordenamientos sin recuperar por ello el contenido ausente.", "rfc3550-sequence-timestamp", "RFC 3550 Section 5.1 and Appendix A", "methodological_requirement", "medium", "direct"),
    ("La interpolación de una muestra ausente produce una estimación derivada y no convierte el valor estimado en una observación originalmente adquirida.", "rfc3550-sequence-timestamp", "Sequence/loss semantics used as integrity boundary", "interpretation_boundary", "medium", "indirect"),
    ("Una simulación de adquisición o un enlace digital íntegro no demuestra seguridad eléctrica, conformidad normativa ni aptitud para conectar personas.", "iec-60601-1-overview", "Scope of IEC 60601-1 and unit safety boundary", "interpretation_boundary", "high", "indirect"),
]

claim_by_text = {x[0]: x for x in claim_texts}

def para(tid: str, sid: int, bid: int, text: str) -> dict:
    return {"id": f"BIOINST-U05-T{tid}-ST{sid:02d}-B{bid:02d}", "type": "paragraph", "text": text}

def sub(tid: str, sid: int, title: str, text: str) -> dict:
    return {"id": f"BIOINST-U05-T{tid}-ST{sid:02d}", "title": title, "blocks": [para(tid, sid, 1, text)]}

def topic(tid: str, title: str, subtopics: list[dict], key_points: list[str], blocks=None) -> dict:
    return {"id": f"BIOINST-U05-T{tid}", "title": title, "blocks": blocks or [], "key_points": key_points, "subtopics": subtopics}

unit["topics"] = [
    topic("01", "1. De la cadena analógica al dominio digital", [
        sub("01", 1, "El reloj define cuándo existe cada muestra", "El paso al dominio digital no empieza con un archivo ni con una gráfica, sino con una decisión física de cuándo observar la entrada. El muestreador, el ADC y el reloj forman una frontera que debe documentarse junto con la banda y el rango heredados de U4."),
        sub("01", 2, "Banda objetivo y banda presente no son lo mismo", "La señal de interés puede ocupar una banda estrecha mientras la entrada analógica contiene interferencias o ruido a frecuencias mayores. La selección de frecuencia de muestreo debe considerar lo que realmente llega al muestreador después del frente analógico."),
        sub("01", 3, "U5 conserva la frontera con U4", "U4 diseña el acondicionamiento y el filtro analógico; U5 audita qué ocurre al muestrear, codificar, temporizar y transportar la señal resultante. Esta separación evita tratar el ADC como si corrigiera saturación o filtrado insuficiente de etapas anteriores."),
    ], [claim_texts[0][0], claim_texts[1][0]]),
    topic("02", "2. Nyquist, aliasing y banda de guarda", [
        sub("02", 1, "Nyquist es una condición ideal, no una garantía de sistema", "Para una señal estrictamente limitada en banda, el criterio de Nyquist establece una relación mínima entre banda y frecuencia de muestreo. Un sistema real debe reservar transición para el filtro y margen para contenido fuera de banda y tolerancias."),
        sub("02", 2, "El aliasing destruye la identidad espectral", "Después del muestreo, componentes analógicas diferentes pueden generar la misma secuencia discreta. Por eso la causa debe controlarse antes de convertir; observar una línea digital a baja frecuencia no permite decidir si se originó dentro o fuera de banda sin información previa."),
        sub("02", 3, "El filtro anti-alias pertenece al lado analógico", "La atenuación relevante debe existir antes del muestreador. Una etapa digital puede filtrar la secuencia obtenida, pero no separar dos componentes analógicas que ya produjeron las mismas muestras."),
    ], [claim_texts[2][0], claim_texts[3][0]], blocks=[{"id":"BIOINST-U05-T02-B01","type":"equation","latex":"f_{alias}=|f-kf_s|","label":"Frecuencia alias ideal para un entero k que pliega la componente a la banda observable.","variables":{"f":"frecuencia analógica","f_s":"frecuencia de muestreo","k":"entero de plegamiento"}}]),
    topic("03", "3. ADC, códigos, cuantización y saturación", [
        sub("03", 1, "Rango, referencia y codificación definen el significado del código", "Un código digital no tiene unidades físicas por sí solo. Para reconstruir la entrada deben conocerse el rango, la referencia, la convención de codificación, el cero y cualquier transformación previa de ganancia u offset."),
        sub("03", 2, "LSB nominal no es exactitud ni detectabilidad", "En el modelo ideal uniforme, el tamaño de código se calcula a partir del rango y el número de bits. Ese valor no incorpora ruido, INL, DNL, offset, ganancia, estabilidad o incertidumbre del resto de la cadena."),
        sub("03", 3, "La saturación debe conservarse como evento de calidad", "Cuando la entrada sale del rango, el código extremo puede representar múltiples valores posibles. La adquisición debe marcar la saturación y evitar que una meseta digital se interprete como una señal físicamente constante."),
    ], [claim_texts[4][0], claim_texts[5][0], claim_texts[6][0], claim_texts[7][0]], blocks=[{"id":"BIOINST-U05-T03-B01","type":"equation","latex":"LSB=\\frac{V_{max}-V_{min}}{2^N}","label":"Tamaño nominal de código de un cuantizador uniforme ideal.","variables":{"N":"bits nominales","V_max":"límite superior ideal","V_min":"límite inferior ideal"}}]),
    topic("04", "4. SINAD, ENOB y desempeño dinámico", [
        sub("04", 1, "SINAD es una métrica de una prueba, no una propiedad sin condiciones", "La relación señal a ruido y distorsión se obtiene de una prueba definida. Frecuencia y amplitud de entrada, tasa de muestreo, ventana, longitud de registro y método de cálculo forman parte de la interpretación."),
        sub("04", 2, "ENOB deriva de la prueba dinámica", "La conversión convencional desde SINAD permite expresar el resultado como bits equivalentes para una entrada senoidal. Esto no convierte el resultado en exactitud DC, resolución metrológica o número garantizado de bits útiles en cualquier aplicación."),
        sub("04", 3, "Comparar convertidores exige condiciones comparables", "Dos cifras de ENOB no deben ordenarse sin revisar frecuencia, amplitud, tasa, rango, filtro y método. La cifra es útil cuando resume una prueba bien definida, no cuando oculta su contexto."),
    ], [claim_texts[8][0], claim_texts[9][0], claim_texts[10][0]], blocks=[{"id":"BIOINST-U05-T04-B01","type":"equation","latex":"ENOB=\\frac{SINAD-1.76}{6.02}","label":"Relación convencional para desempeño dinámico con entrada senoidal.","variables":{"SINAD":"relación señal a ruido y distorsión, dB"}}]),
    topic("05", "5. Reloj, jitter, deriva y simultaneidad", [
        sub("05", 1, "El reloj de adquisición no es el reloj de archivo", "La muestra se produce según un reloj que controla o referencia la conversión. Un timestamp escrito después puede provenir de otro reloj, tener otra resolución y describir empaquetado o recepción en lugar del instante físico de conversión."),
        sub("05", 2, "Jitter y deriva describen errores temporales diferentes", "El jitter representa variación rápida del instante de muestreo respecto de su posición ideal; la deriva aparece cuando dos relojes avanzan a tasas ligeramente distintas y la desalineación crece con el tiempo. Mezclarlos impide diseñar una prueba diagnóstica."),
        sub("05", 3, "Simultaneidad debe demostrarse con la arquitectura", "Canales multiplexados, convertidores simultáneos y dispositivos sincronizados pueden producir tablas con timestamps parecidos. Para sostener simultaneidad deben documentarse clocks, triggers, secuencia de conversión, retardos y skew residual."),
    ], [claim_texts[11][0], claim_texts[12][0], claim_texts[13][0], claim_texts[14][0]]),
    topic("06", "6. Integridad temporal, pérdida y procedencia de muestras", [
        sub("06", 1, "Una curva continua no demuestra que todas las muestras existieron", "La visualización puede unir puntos a través de huecos, duplicados o paquetes reordenados. La integridad se audita sobre identidad de canal, secuencia esperada y marcas temporales antes de interpolar o remuestrear."),
        sub("06", 2, "Contadores y timestamps responden preguntas distintas", "Un contador de secuencia ayuda a comprobar continuidad y orden; un timestamp ayuda a ubicar el dato en una escala temporal. Ninguno sustituye al otro y ambos deben tener semántica documentada."),
        sub("06", 3, "Dato observado y dato reconstruido deben conservar distinta procedencia", "Si falta una muestra puede estimarse un valor para ciertos análisis, pero la salida debe registrar que es derivada. Ocultar la interpolación destruye trazabilidad y puede falsear evaluaciones posteriores de calidad."),
    ], [claim_texts[15][0], claim_texts[16][0]]),
    topic("07", "7. Frontera de aislamiento y límites de inferencia", [
        sub("07", 1, "Integridad digital y seguridad eléctrica son dimensiones diferentes", "Que una transmisión conserve todos los bits no demuestra que una barrera de aislamiento cumpla requisitos eléctricos. La unidad trata la frontera solo como parte del mapa del sistema y remite seguridad a la evidencia y normas correspondientes."),
        sub("07", 2, "La práctica sintética no valida hardware", "Los scripts heredados de legacy U4 permiten comprobar conceptos de aliasing, cuantización e integridad temporal de forma determinista. No caracterizan un ADC físico, un aislador, un cable, un paciente ni una instalación real."),
        sub("07", 3, "La procedencia histórica forma parte del expediente", "Los identificadores U4-P1/U4-P2/U4-P3 y U4-A1…U4-A5 se conservan como evidencia histórica. En el corpus canónico pertenecen a U5 mediante el crosswalk y no deben renombrarse retroactivamente como si la auditoría original hubiera usado la nueva numeración."),
    ], [claim_texts[17][0]]),
]

unit["examples"] = [
    {
        "id":"BIOINST-U05-EJ01","title":"Aliasing de 170 Hz al muestrear a 200 Hz","scenario":"Una componente senoidal de 170 Hz alcanza el muestreador y fs=200 Hz.",
        "reasoning_steps":["Calcular Nyquist=100 Hz.","Buscar k que pliegue la frecuencia al intervalo observable.","Obtener |170-200|=30 Hz.","Explicar por qué la secuencia no conserva la etiqueta de 170 Hz."],
        "interpretation":"La componente puede aparecer idealmente a 30 Hz; el control defendible es limitar el contenido antes del muestreo.",
        "limitations":["Ejemplo senoidal ideal.","No sustituye caracterización del filtro analógico real."]
    },
    {
        "id":"BIOINST-U05-EJ02","title":"LSB nominal de un ADC bipolar","scenario":"ADC ideal de -1 V a +1 V con 10 bits.",
        "reasoning_steps":["Rango total=2 V.","Códigos=1024.","LSB=2/1024=1.953125 mV.","Separar LSB de exactitud, ruido y ENOB."],
        "interpretation":"El tamaño nominal de código describe el cuantizador ideal; no garantiza cambios detectables de 1.953 mV en una cadena real.",
        "limitations":["No incluye offset, ganancia, INL, DNL, ruido ni deriva."]
    },
    {
        "id":"BIOINST-U05-EJ03","title":"ENOB a partir de SINAD","scenario":"Una prueba senoidal produce SINAD=61.96 dB bajo frecuencia, amplitud y tasa declaradas.",
        "reasoning_steps":["Usar la relación convencional ENOB=(SINAD-1.76)/6.02.","Obtener aproximadamente 10.0 bits.","Registrar las condiciones de prueba.","Negar la equivalencia con exactitud DC."],
        "interpretation":"El valor resume el desempeño dinámico observado en esa prueba y puede cambiar en otras condiciones.",
        "limitations":["No describe por sí solo linealidad estática, estabilidad o incertidumbre de cadena."]
    },
    {
        "id":"BIOINST-U05-EJ04","title":"Dos canales con timestamps iguales","scenario":"Dos canales muestran la misma marca de tiempo de software, pero un multiplexor convierte primero A y después B.",
        "reasoning_steps":["Identificar el reloj que genera el timestamp.","Identificar el reloj/orden que controla las conversiones.","Cuantificar o acotar el desfase entre A y B.","Definir qué evidencia demostraría sincronización suficiente."],
        "interpretation":"La igualdad de campos de tiempo no prueba conversión simultánea; la arquitectura temporal debe quedar documentada.",
        "limitations":["Caso conceptual; no fija un umbral universal de sincronía."]
    },
]

unit["activities"] = [{
    "id":"BIOINST-U05-ACT01",
    "title":"Auditoría reproducible de una cadena de adquisición digital",
    "purpose":"Integrar muestreo, aliasing, ADC, desempeño dinámico, sincronización e integridad temporal usando las prácticas sintéticas heredadas de legacy U4 y documentando explícitamente su correspondencia con canonical U5.",
    "prerequisite_unit_ids":["BIOINST-U04"],
    "estimated_duration_minutes":240,
    "instructions":[
        "Abrir `data/course_migrations/bioinstrumentacion-numbering-v1.json` y registrar que canonical U5 procede de legacy U4 sin reescribir la evidencia histórica.",
        "Ejecutar `scripts/bioinstrumentation_u4_practice_u4p1.py`, `u4p2.py` y `u4p3.py` en directorios temporales; conservar comandos, parámetros y salidas.",
        "Separar en todo el informe cuatro capas: señal analógica heredada de U4, muestreo/ADC, reloj/sincronización e integridad/transporte.",
        "Para cada resultado incluir unidades, supuestos, fuente de evidencia, criterio de aceptación y una afirmación que los datos NO permiten sostener.",
        "Cerrar con una decisión técnica limitada: aceptar el diseño sintético, revisarlo o rechazarlo para el propósito educativo declarado, sin inferir seguridad, conformidad ni validez clínica."
    ],
    "tasks":[
        "Trazar la cadena `banda analógica → filtro anti-alias → muestreador → ADC → paquetes/archivo` e identificar qué decisiones vienen de U4 y cuáles pertenecen a U5.",
        "Con U4-P1, predecir y comprobar al menos un alias, comparar condición con/sin prefiltrado y explicar por qué el filtrado digital posterior no recupera la frecuencia analógica original.",
        "Con U4-P2, calcular rango, número de códigos y LSB; cuantificar error de cuantización del fixture y separar explícitamente resolución nominal de exactitud.",
        "Localizar los casos saturados de U4-P2, explicar qué información se pierde y diseñar la bandera/metadato que debe acompañarlos.",
        "Calcular ENOB desde un SINAD proporcionado y redactar qué condiciones mínimas deben acompañar una comparación entre dos convertidores.",
        "Construir un diagrama de clocks que separe sample clock, reference clock/trigger y reloj de timestamp; incluir un caso de jitter, uno de deriva y uno de canales no simultáneos.",
        "Con U4-P3, detectar huecos, duplicados y reordenamientos por canal; marcar cualquier interpolación posterior como dato derivado y no como muestra recuperada.",
        "Auditar la frontera de aislamiento de manera documental y enumerar la evidencia adicional que sería necesaria antes de hablar de hardware, seguridad eléctrica, conformidad o uso con personas."
    ],
    "deliverables":[
        "Diagrama de cadena y tabla de procedencia `legacy U4 → canonical U5`.",
        "Notebook o informe reproducible de aliasing/anti-alias con comandos y resultados de U4-P1.",
        "Presupuesto de ADC con rango, códigos, LSB, cuantización, saturación y límites, basado en U4-P2.",
        "Ficha de desempeño dinámico con SINAD/ENOB y condiciones de comparación.",
        "Mapa temporal multicanal con clocks, timestamps, jitter, deriva, gaps, duplicados y reordenamientos de U4-P3.",
        "Informe final de 1–2 páginas con decisión, limitaciones, datos derivados y evidencia faltante para cualquier afirmación de sistema real."
    ],
    "checking_criteria":[
        "El crosswalk legacy U4 → canonical U5 aparece explícito y no se renombra la evidencia histórica.",
        "Nyquist no se presenta como garantía suficiente y el filtro anti-alias se ubica antes del muestreador.",
        "El cálculo de alias coincide con las muestras y se conserva la pérdida de identidad espectral.",
        "LSB se calcula con rango y 2^N sin llamarlo exactitud, ENOB o cambio mínimo detectable real.",
        "Saturación, cuantización, ruido y otros errores se mantienen como mecanismos distintos.",
        "SINAD/ENOB conservan frecuencia, amplitud, tasa y procedimiento de ensayo.",
        "Sample clock, timestamp, simultaneidad, jitter y deriva no se usan como sinónimos.",
        "Gaps, duplicados y reordenamientos se detectan mediante metadatos antes de interpolar.",
        "Toda interpolación se identifica como valor derivado y no como observación recuperada.",
        "El informe niega explícitamente que las simulaciones demuestren seguridad, conformidad, desempeño de hardware o validez clínica."
    ],
    "status":"curated_pending_expert_review"
}]
unit["status"]["sources"] = "traceable"
unit["status"]["content"] = "in_review"
unit["status"]["pedagogy"] = "in_review"
unit["status"]["internal_review"] = "pending"
unit["status"]["external_review"] = "pending"
unit["status"]["publication"] = "published_provisional"
unit["purpose"] = "Preservar y promover el contenido autoral de legacy U4 como canonical U5, dedicando la unidad a muestreo, aliasing, ADC, cuantización, desempeño dinámico, sincronización e integridad temporal sin reescribir la evidencia histórica ni inferir seguridad o validez clínica."

# --- Assessment ---------------------------------------------------------------
def q(qid, prompt, los, difficulty, cognitive, expected, explanation, misconceptions, source_ids):
    return {
        "id": f"BIOINST-U05-Q{qid:02d}", "type":"case_analysis", "prompt":prompt,
        "linked_learning_outcome_ids":los, "difficulty":difficulty, "cognitive_level":cognitive,
        "answer_key":{"expected_answer":expected,"explanation":explanation,"common_misconceptions":misconceptions},
        "feedback":{"correct":"La respuesta conserva la frontera analógico-digital, las condiciones de ensayo y la procedencia temporal de cada dato.","incorrect":"Reconstruye la cadena desde la banda analógica hasta los metadatos temporales y separa qué información fue observada, cuantizada, sincronizada, perdida o estimada."},
        "source_ids":source_ids, "status":"curated_pending_expert_review"
    }
assessment["purpose"] = "Evaluar razonamiento sobre muestreo, ADC, desempeño dinámico, sincronización e integridad temporal preservando el crosswalk legacy U4 → canonical U5 y sin convertir simulación en evidencia de hardware o seguridad."
assessment["student_payload_policy"] = "Las claves y explicaciones se reservan del payload inicial; decisiones integradoras y cualquier juicio de aptitud siguen requiriendo revisión humana."
assessment["items"] = [
    q(1,"Una señal contiene 30 Hz y 170 Hz y se muestrea a 200 Hz sin anti-alias. Ambas pueden contribuir a una componente digital de 30 Hz. ¿Qué puedes concluir de esa línea digital y qué cambio en la cadena permite distinguir el problema antes de muestrear?",["BIOINST-U05-LO01"],"intermediate","analyze","La línea digital por sí sola no identifica el origen analógico. Debe limitarse la banda antes del muestreo y documentar el filtro/banda presente; alternativamente se cambia fs de forma controlada para una prueba diagnóstica.","El aliasing hace no invertible la identificación espectral una vez que distintas componentes producen muestras indistinguibles.",["digital-filter-recovers-alias","observed-frequency-equals-analog-origin"],["ni-analog-signal-acquisition","ni-anti-alias-filters"]),
    q(2,"Un ADC ideal cubre -1 V a +1 V con 12 bits. Un informe afirma: 'su exactitud es 0,488 mV porque ese es el LSB'. Corrige la afirmación y enumera al menos tres contribuciones que el LSB no describe.",["BIOINST-U05-LO02"],"intermediate","apply","LSB=2/4096≈0,488 mV es tamaño nominal de código del modelo ideal, no exactitud. No describe, por ejemplo, offset, error de ganancia, INL/DNL, ruido, referencia, deriva o incertidumbre de etapas previas.","Resolución nominal y exactitud son métricas distintas; el código representa un intervalo y el sistema real añade errores no incluidos en el cuantizador ideal.",["lsb-equals-accuracy","bits-equal-detectability"],["adi-adc-glossary","adi-quantization-glossary"]),
    q(3,"En una adquisición aparecen 40 muestras consecutivas en el código máximo del ADC durante un transitorio. Después vuelven a valores normales. ¿Por qué no debe interpolarse el valor real durante ese intervalo como si solo faltaran muestras?",["BIOINST-U05-LO02","BIOINST-U05-LO05"],"advanced","evaluate","El clipping sí produjo códigos observados, pero múltiples entradas fuera de rango son compatibles con el mismo código extremo; se perdió amplitud. Debe marcarse saturación y tratar el intervalo como información censurada/limitada, no como un simple gap recuperable.","Un gap de transporte y una saturación del convertidor pierden información por mecanismos distintos y requieren metadatos distintos.",["clipping-is-gap","interpolation-restores-clipped-signal"],["adi-adc-glossary","adi-quantization-glossary"]),
    q(4,"Dos ADC anuncian 10,8 y 11,2 ENOB. El primero fue ensayado a 1 kHz y el segundo a 100 kHz con amplitudes y tasas distintas. ¿Es válida la conclusión 'el segundo es mejor'?",["BIOINST-U05-LO03"],"advanced","evaluate","No. Antes de comparar deben armonizarse o al menos documentarse frecuencia/amplitud de entrada, tasa de muestreo, rango, ventana, banda y procedimiento. ENOB resume una prueba dinámica y puede variar con esas condiciones.","Una cifra de ENOB sin contexto no es una clasificación universal ni exactitud DC.",["enob-is-universal","enob-equals-dc-accuracy"],["adi-enob-dynamic-2019","adi-adc-dynamic-parameters"]),
    q(5,"Un reloj tiene error sistemático de +20 ppm y además variación aleatoria muestra a muestra. Después de una hora dos dispositivos están desalineados. Se etiqueta todo como 'jitter'. ¿Qué está mal?",["BIOINST-U05-LO04"],"advanced","analyze","La componente sistemática de frecuencia produce deriva acumulada entre relojes; la variación rápida del instante corresponde a jitter. Deben estimarse y probarse por separado porque tienen firmas temporales y mitigaciones diferentes.","Jitter no es un nombre genérico para todo error de tiempo; deriva y variación muestra a muestra son fenómenos distintos.",["all-time-error-is-jitter","timestamps-remove-clock-error"],["adi-aperture-jitter","nist-time-measurement"]),
    q(6,"Dos canales tienen exactamente el mismo timestamp para cada fila, pero un multiplexor convierte A y B con 50 µs de separación. ¿Son físicamente simultáneos? ¿Qué metadatos necesitarías?",["BIOINST-U05-LO04"],"intermediate","evaluate","No necesariamente. Se necesita arquitectura de conversión, sample clock, orden de multiplexación, trigger/referencia, skew/retardo y semántica del timestamp. Un reloj de etiquetado común puede ocultar el desfase físico.","La simultaneidad es propiedad de la adquisición y su arquitectura temporal, no de que dos campos de software coincidan.",["same-timestamp-means-simultaneous","software-time-is-sample-clock"],["ni-sample-clock-2025","ni-synchronization-explained"]),
    q(7,"Por canal se reciben secuencias 100,101,103,103,102. Diseña una auditoría que identifique gap, duplicado y reordenamiento y explica por qué rellenar 102.5 por interpolación no recupera una muestra original.",["BIOINST-U05-LO05"],"advanced","create","Mantener estado por canal con contador esperado, registrar gap al saltar 102, duplicado para el segundo 103 y llegada tardía/reordenada de 102. Cualquier valor interpolado debe marcarse como derivado; no existe evidencia de cuál fue la muestra ausente.","Los metadatos permiten detectar fallos de continuidad, no recrear información que nunca llegó.",["continuous-plot-proves-integrity","interpolation-is-recovery"],["rfc3550-sequence-timestamp"]),
    q(8,"Un equipo demuestra en simulación que no hay aliasing, que los contadores no pierden paquetes y que dos streams se alinean. Concluye: 'la cadena está validada para conectarse a pacientes'. Evalúa la conclusión y redacta el siguiente paso defendible.",["BIOINST-U05-LO01","BIOINST-U05-LO02","BIOINST-U05-LO03","BIOINST-U05-LO04","BIOINST-U05-LO05"],"advanced","create","La conclusión excede la evidencia. La simulación apoya coherencia del modelo educativo y controles de datos, pero no caracteriza hardware, aislamiento, seguridad eléctrica, EMC, desempeño metrológico ni validez clínica. El siguiente paso es definir requisitos y ensayos específicos con revisión competente; no conectar personas desde esta unidad.","Integridad de datos y seguridad/aptitud son dimensiones distintas y requieren evidencia distinta.",["simulation-proves-safety","data-integrity-proves-device-validity"],["iec-60601-1-overview","ni-synchronization-explained"]),
]
assessment["status"] = "curated_pending_expert_review"

# --- Glossary -----------------------------------------------------------------
source_locators = {
    "ni-analog-signal-acquisition":"Bandwidth, Nyquist Sampling Theorem, and Aliasing",
    "ni-anti-alias-filters":"Overview and practical transition-band discussion",
    "adi-adc-glossary":"ADC definition and coding context",
    "adi-quantization-glossary":"Quantization definition",
    "adi-enob-dynamic-2019":"Effective Number of Bits section",
    "adi-adc-dynamic-parameters":"SINAD and ENOB sections",
    "adi-aperture-jitter":"Aperture Delay and Aperture Jitter sections",
    "ni-sample-clock-2025":"Sample Clock overview",
    "ni-synchronization-explained":"Synchronization approaches and sample-clock synchronization",
    "nist-time-measurement":"Time interval measurement and synchronization overview",
    "rfc3550-sequence-timestamp":"Section 5.1 and Appendix A",
    "iec-60601-1-overview":"Scope boundary",
}
term_specs = [
    ("Banda analógica presente","Intervalo de frecuencias que alcanza físicamente al muestreador después del acondicionamiento, incluyendo componentes útiles y no deseadas.",["ni-analog-signal-acquisition"]),
    ("Frecuencia de muestreo","Número de muestras por unidad de tiempo controlado por el reloj de adquisición o por una arquitectura equivalente.",["ni-sample-clock-2025"]),
    ("Frecuencia de Nyquist","Mitad de la frecuencia de muestreo; frontera del intervalo base para una representación muestreada ideal.",["ni-analog-signal-acquisition"]),
    ("Aliasing","Plegamiento por el cual contenido analógico fuera del intervalo de Nyquist aparece como contenido a otra frecuencia en las muestras.",["ni-analog-signal-acquisition"]),
    ("Filtro anti-alias","Filtro analógico situado antes del muestreador/ADC para atenuar contenido que podría plegarse dentro de la banda digital de interés.",["ni-anti-alias-filters"]),
    ("ADC","Convertidor analógico-digital que asigna muestras de una entrada analógica a códigos digitales según rango, referencia y arquitectura.",["adi-adc-glossary"]),
    ("LSB nominal","Tamaño ideal de un intervalo de código, igual al rango total dividido entre 2^N en un cuantizador uniforme; no es exactitud.",["adi-quantization-glossary"]),
    ("Cuantización","Asignación de un intervalo continuo de entrada a un conjunto finito de niveles o códigos discretos.",["adi-quantization-glossary"]),
    ("Saturación del ADC","Condición en la que la entrada excede el intervalo codificable y distintos valores pueden quedar representados por un código extremo.",["adi-adc-glossary"]),
    ("SINAD","Relación entre la componente de señal y la combinación de ruido y distorsión bajo una prueba y banda definidas.",["adi-adc-dynamic-parameters"]),
    ("ENOB","Número efectivo de bits derivado del desempeño dinámico, habitualmente de SINAD bajo una prueba senoidal declarada; no equivale a exactitud DC.",["adi-enob-dynamic-2019"]),
    ("Jitter de apertura","Variación muestra a muestra del retardo entre el evento de reloj y el instante efectivo en que se toma la muestra.",["adi-aperture-jitter"]),
    ("Deriva de reloj","Acumulación de desalineación temporal causada por diferencias de frecuencia o estabilidad entre relojes.",["nist-time-measurement"]),
    ("Sample clock","Señal o referencia temporal que controla los instantes o la tasa a la que se realizan las conversiones.",["ni-sample-clock-2025"]),
    ("Timestamp","Marca temporal con semántica y reloj de origen declarados; puede describir adquisición, empaquetado, transmisión o recepción y no prueba por sí sola simultaneidad.",["rfc3550-sequence-timestamp","ni-synchronization-explained"]),
    ("Sincronización","Arquitectura y proceso por los que dos o más operaciones de adquisición quedan relacionadas en el tiempo con precisión y error residual documentados.",["ni-synchronization-explained"]),
    ("Contador de secuencia","Identificador ordenado que, cuando sigue una regla conocida, permite detectar discontinuidades, duplicados y reordenamientos.",["rfc3550-sequence-timestamp"]),
    ("Interpolación","Estimación de valores entre observaciones disponibles; una interpolación de un dato ausente es derivada y no una recuperación de la observación original.",["rfc3550-sequence-timestamp"]),
]
entries = glossary["entries"]
max_id = max([int(m.group(1)) for e in entries if (m := re.search(r"(\d+)$", e["id"]))] or [0])
selected_ids=[]
for term, definition, sids in term_specs:
    entry = next((e for e in entries if e["term"].strip().casefold() == term.casefold()), None)
    if entry is None:
        max_id += 1
        entry = {"id":f"BIOINST-GLO-{max_id:03d}","term":term,"definition":definition,"unit_ids":["BIOINST-U05"],"source_ids":sids,"verification_status":"verified_directly"}
        entries.append(entry)
    entry["definition"] = definition
    entry["unit_ids"] = sorted(set(entry.get("unit_ids", [])) | {"BIOINST-U05"})
    entry["source_ids"] = sids
    entry["verification_status"] = "verified_directly" if len(sids)==1 else "verified_contextually"
    entry["source_locators"] = [{"source_id":sid,"locator":source_locators[sid]} for sid in sids]
    selected_ids.append(entry["id"])
unit["glossary_entry_ids"] = selected_ids

# --- Claims -------------------------------------------------------------------
claims["claims"] = [c for c in claims["claims"] if c.get("unit_id") != "BIOINST-U05"]
new_claims=[]
for idx, (text, source_id, locator, ctype, risk, support) in enumerate(claim_texts, 1):
    cid=f"BIOINST-U05-C{idx:03d}"
    new_claims.append({
        "claim_id":cid,"unit":5,"text":text,"claim_type":ctype,"risk":risk,
        "context":"Aplicado a una cadena educativa de adquisición digital; toda conclusión depende de banda, rango, reloj, arquitectura, condiciones de prueba y uso previsto.",
        "source_id":source_id,"locator":{"section":locator},"support":support,
        "source_verification_status":"verified_directly","review_state":"ai_review_provisional",
        "reviewer_validation_id":None,"reviewed_at":"2026-08-24","id":cid,"unit_id":"BIOINST-U05"
    })
claims["claims"].extend(new_claims)
claims["scope"] = "Afirmaciones centrales de Bioinstrumentación con fuente y localizador; Unidades 1–5 integradas y revisión disciplinaria humana pendiente."
claims["review_state"] = "ai_review_provisional"
unit["claim_ids"]=[c["id"] for c in new_claims]

source_ids = [
    "ni-analog-signal-acquisition","ni-anti-alias-filters","adi-adc-glossary","adi-quantization-glossary",
    "adi-enob-dynamic-2019","adi-adc-dynamic-parameters","adi-aperture-jitter","ni-sample-clock-2025",
    "ni-synchronization-explained","nist-time-measurement","rfc3550-sequence-timestamp","physionet-mit-bih-arrhythmia","iec-60601-1-overview"
]
unit["source_ids"] = source_ids
for sid in source_ids:
    src=next((x for x in sources["sources"] if x["id"]==sid),None)
    assert src is not None, sid
    src["used_by_unit_ids"] = sorted(set(src.get("used_by_unit_ids",[])) | {"BIOINST-U05"})

# Preserve historical numbering in the canonical prose and tests, without changing old artifacts.
unit["status"]["multimedia"] = "planned"

dump(UNIT_PATH, unit)
dump(ASSESSMENT_PATH, assessment)
dump(GLOSSARY_PATH, glossary)
dump(SOURCES_PATH, sources)
dump(CLAIMS_PATH, claims)

print("Curated canonical Bioinstrumentation U5 from preserved legacy U4 provenance")
