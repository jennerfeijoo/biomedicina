#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


unit_path = COURSE / "units" / "unit-08.json"
assessment_path = COURSE / "assessments" / "unit-08.json"
glossary_path = COURSE / "glossary.json"
sources_path = COURSE / "sources.json"
claims_path = COURSE / "claims.json"
unit = load(unit_path)
assessment = load(assessment_path)
glossary = load(glossary_path)
sources = load(sources_path)
claims = load(claims_path)
migration = load(ROOT / "data/course_migrations/bioinstrumentacion-numbering-v1.json")

row = next(x for x in migration["canonical_sequence"] if x["canonical_unit"] == 8)
assert row["origin"] == "new" and row["action"] == "author"
assert not (ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-08.json").exists()


def upsert_source(record: dict) -> None:
    existing = next((s for s in sources["sources"] if s["id"] == record["id"]), None)
    if existing is None:
        sources["sources"].append(record)
        return
    used = sorted(set(existing.get("used_by_unit_ids", [])) | set(record.get("used_by_unit_ids", [])))
    existing.update(record)
    existing["used_by_unit_ids"] = used


source_records = [
    {
        "id":"bipm-vim-calibration","title":"VIM3 2.39 — calibration","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.39.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 2.39 and notes","curricular_function":"Distinguir calibración de ajuste y relacionar indicaciones, referencias e incertidumbres.",
        "coverage":[1,8],"limitations":"Definición terminológica; no sustituye un procedimiento de calibración específico.","used_by_unit_ids":["BIOINST-U01","BIOINST-U08"]
    },
    {
        "id":"bipm-vim-adjustment","title":"VIM3 3.11 — adjustment of a measuring system","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/3.11.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 3.11 and notes 1–3","curricular_function":"Definir ajuste y documentar que no debe confundirse con calibración; tras ajustar suele requerirse recalibración.",
        "coverage":[8],"limitations":"No prescribe cómo ajustar un instrumento concreto.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-verification","title":"VIM3 2.44 — verification","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.44.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 2.44 and notes","curricular_function":"Definir verificación como evidencia objetiva de satisfacción de requisitos especificados.",
        "coverage":[8,9],"limitations":"La definición no fija requisitos ni criterios de aceptación para un producto concreto.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-validation","title":"VIM3 2.45 — validation","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.45.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 2.45","curricular_function":"Separar validación de verificación y reservar la adecuación al uso especificado para la etapa correspondiente.",
        "coverage":[8,9],"limitations":"No constituye validación clínica ni regulatoria de ningún sistema.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-precision","title":"VIM3 2.15 — measurement precision","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.15.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 2.15 and notes","curricular_function":"Distinguir precisión de exactitud y organizar repetibilidad, precisión intermedia y reproducibilidad.",
        "coverage":[8],"limitations":"No prescribe un estimador estadístico universal.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-repeatability","title":"VIM3 2.21 — measurement repeatability","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.21.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entries 2.20–2.21","curricular_function":"Definir repetibilidad dentro de condiciones de repetibilidad declaradas.",
        "coverage":[8],"limitations":"Las condiciones concretas deben documentarse en cada experimento.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-reproducibility","title":"VIM3 2.25 — measurement reproducibility","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.25.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entries 2.24–2.25","curricular_function":"Definir reproducibilidad bajo condiciones deliberadamente cambiadas y declaradas.",
        "coverage":[8,10],"limitations":"No implica por sí sola exactitud, trazabilidad o validez de uso.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-standard-uncertainty","title":"VIM3 2.30 — standard measurement uncertainty","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.30.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 2.30","curricular_function":"Definir incertidumbre estándar como incertidumbre expresada como desviación estándar.",
        "coverage":[8],"limitations":"La entrada no sustituye la construcción del modelo ni la evaluación de componentes.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-combined-uncertainty","title":"VIM3 2.31 — combined standard measurement uncertainty","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.31.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 2.31","curricular_function":"Definir incertidumbre estándar combinada a partir de incertidumbres asociadas a cantidades de entrada.",
        "coverage":[8],"limitations":"La regla de propagación depende del modelo y de correlaciones.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-expanded-uncertainty","title":"VIM3 2.35 — expanded measurement uncertainty","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.35.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entries 2.35–2.38","curricular_function":"Distinguir incertidumbre expandida, intervalo de cobertura, probabilidad y factor de cobertura.",
        "coverage":[8],"limitations":"Un factor k aislado no determina universalmente una probabilidad exacta de cobertura.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-coverage-factor","title":"VIM3 2.38 — coverage factor","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.38.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 2.38 and notes","curricular_function":"Definir el factor usado para obtener incertidumbre expandida a partir de incertidumbre estándar combinada.",
        "coverage":[8],"limitations":"Debe declararse junto con el método y la interpretación de cobertura.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-sensitivity","title":"VIM3 4.12 — sensitivity of a measuring system","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/4.12.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 4.12 and notes","curricular_function":"Definir sensibilidad y separarla de resolución, precisión y exactitud.",
        "coverage":[2,8],"limitations":"La sensibilidad puede depender del valor de la cantidad medida.","used_by_unit_ids":["BIOINST-U02","BIOINST-U08"]
    },
    {
        "id":"bipm-vim-resolution","title":"VIM3 4.14 — resolution","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/4.14.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 4.14 and note","curricular_function":"Definir resolución como el menor cambio que produce un cambio perceptible en la indicación.",
        "coverage":[2,8],"limitations":"Puede depender de ruido, fricción y del valor medido.","used_by_unit_ids":["BIOINST-U02","BIOINST-U08"]
    },
    {
        "id":"bipm-vim-instrumental-drift","title":"VIM3 4.21 — instrumental drift","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/4.21.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 4.21 and note","curricular_function":"Definir deriva instrumental y separarla de cambios del mensurando o de influencias reconocidas.",
        "coverage":[2,8],"limitations":"La causa física de la deriva requiere evidencia adicional.","used_by_unit_ids":["BIOINST-U02","BIOINST-U08"]
    },
    {
        "id":"bipm-vim-step-response-time","title":"VIM3 4.23 — step response time","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/4.23.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 4.23","curricular_function":"Relacionar caracterización dinámica y criterio de establecimiento de la indicación tras un cambio de entrada.",
        "coverage":[2,8],"limitations":"No sustituye modelos dinámicos de orden superior ni criterios específicos de aplicación.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"bipm-vim-traceability","title":"VIM3 2.41 — metrological traceability","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://jcgm.bipm.org/vim/en/2.41.html","type":"terminología metrológica oficial","verification_status":"verified_directly",
        "locator":"VIM3 entry 2.41 and notes","curricular_function":"Vincular resultados con referencias mediante una cadena documentada de calibraciones con contribución de incertidumbre.",
        "coverage":[1,8],"limitations":"La trazabilidad es propiedad del resultado y no demuestra por sí sola aptitud para uso.","used_by_unit_ids":["BIOINST-U01","BIOINST-U08"]
    },
    {
        "id":"jcgm-gum-6-2020","title":"JCGM GUM-6:2020 — Developing and using measurement models","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://www.bipm.org/en/doi/10.59161/JCGMGUM-6-2020","type":"guía metrológica oficial","verification_status":"verified_directly",
        "locator":"JCGM GUM-6:2020, clauses on measurement models, input quantities and model adequacy","curricular_function":"Sustentar diseño del modelo de medición, cantidades de entrada e influencias para caracterización e incertidumbre.",
        "coverage":[1,2,8],"limitations":"No prescribe un procedimiento de ensayo biomédico específico.","used_by_unit_ids":["BIOINST-U01","BIOINST-U02","BIOINST-U08"]
    },
    {
        "id":"jcgm-100-2008","title":"JCGM 100:2008 — Guide to the expression of uncertainty in measurement","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://www.bipm.org/en/doi/10.59161/JCGM100-2008E","type":"guía metrológica oficial","verification_status":"verified_directly",
        "locator":"JCGM 100:2008 sections 4–6; 5.2.5 for correlations","curricular_function":"Evaluar componentes Tipo A/B, combinar incertidumbres, tratar correlaciones y declarar incertidumbre expandida.",
        "coverage":[8],"limitations":"La aproximación lineal debe revisarse cuando el modelo o las distribuciones hacen insuficiente la linealización.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"jcgm-100-amd1-2026","title":"JCGM 100:2008/Amd.1:2026 — Nonlinearity in measurement models","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://doi.org/10.59161/PPDI3267","type":"guía metrológica oficial","verification_status":"verified_directly",
        "locator":"BIPM Guides in Metrology; Amendment 1:2026 on nonlinearity in measurement models","curricular_function":"Advertir que la no linealidad del modelo puede requerir tratamiento más allá de la propagación lineal de primer orden.",
        "coverage":[8],"limitations":"Se usa para frontera metodológica; no se desarrolla aquí una implementación completa del amendment.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"jcgm-101-2008","title":"JCGM 101:2008 — Propagation of distributions using a Monte Carlo method","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://www.bipm.org/en/doi/10.59161/JCGM101-2008","type":"guía metrológica oficial","verification_status":"verified_directly",
        "locator":"Abstract and scope; propagation of distributions through a measurement model by Monte Carlo","curricular_function":"Introducir Monte Carlo como alternativa documentada para propagación de distribuciones cuando procede.",
        "coverage":[8],"limitations":"La unidad no convierte Monte Carlo en requisito universal ni sustituye el análisis del modelo.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"jcgm-gum-5-2026","title":"JCGM GUM-5:2026 — Guide to the expression of uncertainty in measurement — Part 5: Examples","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://doi.org/10.59161/YNLY8209","type":"guía metrológica oficial","verification_status":"verified_directly",
        "locator":"BIPM Guides in Metrology; GUM-5:2026 examples","curricular_function":"Aportar ejemplos actuales dentro de la familia GUM para contrastar presupuestos educativos.",
        "coverage":[8],"limitations":"Los ejemplos de la guía no convierten el ejercicio del curso en calibración acreditada.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"jcgm-106-2012","title":"JCGM 106:2012 — The role of measurement uncertainty in conformity assessment","organization":"Joint Committee for Guides in Metrology / BIPM",
        "url":"https://www.bipm.org/en/doi/10.59161/JCGM106-2012","type":"guía metrológica oficial","verification_status":"verified_directly",
        "locator":"JCGM 106:2012 section 5.1 and decision-rule framework","curricular_function":"Relacionar resultado, requisito, incertidumbre y regla de decisión en evaluación de conformidad.",
        "coverage":[8,9],"limitations":"La regla concreta depende del requisito, consecuencias y contexto; no hay una guard band universal.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"ilac-g8-2019","title":"ILAC G8:09/2019 — Guidelines on Decision Rules and Statements of Conformity","organization":"International Laboratory Accreditation Cooperation",
        "url":"https://ilac.org/publications-and-resources/ilac-guidance-series/","type":"guía de acreditación","verification_status":"verified_directly",
        "locator":"ILAC Guidance Series; G8:09/2019 current listed guidance on decision rules and statements of conformity","curricular_function":"Introducir reglas de decisión, riesgo de decisión y guard bands sin presentarlas como una única regla obligatoria.",
        "coverage":[8,9],"limitations":"Guía de laboratorios/acreditación; no autoriza declaraciones de conformidad del curso.","used_by_unit_ids":["BIOINST-U08"]
    },
    {
        "id":"nist-tn-2156-traceability","title":"NIST Technical Note 2156 — Metrological Traceability: Frequently Asked Questions and NIST Policy","organization":"National Institute of Standards and Technology",
        "url":"https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2156.pdf","type":"política y guía metrológica","verification_status":"verified_directly",
        "locator":"NIST TN 2156 section 5.4.3; calibrated artifact alone is insufficient for traceability of a user's result","curricular_function":"Reforzar que un certificado o instrumento calibrado no transfiere automáticamente trazabilidad ni aptitud al resultado del usuario.",
        "coverage":[1,8],"limitations":"Política NIST; la aptitud para un uso biomédico requiere evidencia adicional del sistema y contexto.","used_by_unit_ids":["BIOINST-U08"]
    },
]
for record in source_records:
    upsert_source(record)
sources["consulted_on"] = "2026-08-24"
for gap in sources.get("coverage_gaps", []):
    if gap.get("domain") == "calibración e incertidumbre en instrumentación fisiológica":
        gap["status"] = "general_framework_traceable_biomedical_review_pending"
        gap["need"] = "El marco general VIM/GUM/JCGM/ILAC está localizado y trazable; permanecen pendientes casos específicos de instrumentación fisiológica y revisión disciplinaria humana."

claim_specs = [
("Un plan de caracterización solo puede estimar las propiedades que su secuencia de entradas, repeticiones, direcciones, tiempos y condiciones permite separar.","jcgm-gum-6-2020","Measurement-model design and influence quantities","methodological_requirement","medium","indirect"),
("Los criterios de aceptación deben fijarse antes de inspeccionar los resultados cuando se pretende una decisión reproducible y auditable.","jcgm-106-2012","Section 5.1: specified requirement and previously established decision rule","decision_principle","medium","direct"),
("Las condiciones ambientales, el tiempo de estabilización y la identificación de la referencia forman parte del alcance del resultado de caracterización.","jcgm-gum-6-2020","Measurement model, influence quantities and conditions","methodological_requirement","medium","indirect"),
("La calibración establece, bajo condiciones especificadas, una relación entre valores de referencia con sus incertidumbres y las indicaciones correspondientes; no implica necesariamente modificar el instrumento.","bipm-vim-calibration","VIM3 entry 2.39 and notes","definition","low","direct"),
("El ajuste modifica el sistema de medición para obtener indicaciones prescritas y no debe confundirse con calibración; después de un ajuste suele ser necesaria una nueva calibración.","bipm-vim-adjustment","VIM3 entry 3.11 notes 2–3","definition","low","direct"),
("La verificación aporta evidencia objetiva de que se satisfacen requisitos especificados, mientras la validación es una verificación en la que esos requisitos son adecuados para un uso previsto.","bipm-vim-validation","VIM3 entries 2.44–2.45","definition","medium","direct"),
("Sensibilidad y resolución describen propiedades diferentes del sistema y ninguna de ellas equivale por sí sola a precisión, exactitud o incertidumbre.","bipm-vim-sensitivity","VIM3 entries 4.12 and 4.14","interpretation_boundary","medium","direct"),
("La precisión se evalúa bajo condiciones especificadas; repetibilidad y reproducibilidad se distinguen por qué condiciones permanecen constantes y cuáles cambian deliberadamente.","bipm-vim-precision","VIM3 entries 2.15, 2.20–2.25","definition","low","direct"),
("La deriva instrumental es un cambio temporal de la indicación debido a cambios en propiedades metrológicas del instrumento y no debe confundirse automáticamente con un cambio del mensurando.","bipm-vim-instrumental-drift","VIM3 entry 4.21 and note","definition","low","direct"),
("La linealidad solo tiene significado respecto de un modelo, un dominio y unas condiciones declaradas; un ajuste lineal con residuales pequeños no demuestra linealidad universal.","jcgm-100-amd1-2026","Amendment 1:2026 on nonlinearity in measurement models","interpretation_boundary","medium","indirect"),
("La caracterización dinámica necesita una entrada temporal definida, una salida observable y un criterio de establecimiento; el tiempo de respuesta no es intercambiable con sensibilidad o resolución.","bipm-vim-step-response-time","VIM3 entry 4.23 with entries 4.12 and 4.14","methodological_requirement","medium","direct"),
("Separar histéresis, deriva y dinámica requiere diseñar la secuencia de ensayo de modo que dirección de recorrido, tiempo y transitorios no queden confundidos.","jcgm-gum-6-2020","Measurement-model and influence-quantity design","methodological_requirement","medium","indirect"),
("Las evaluaciones Tipo A y Tipo B son métodos para evaluar componentes de incertidumbre y no son sinónimos de error aleatorio y error sistemático.","jcgm-100-2008","Sections 4.2–4.3","interpretation_boundary","medium","direct"),
("Las correlaciones entre cantidades de entrada no pueden ignorarse cuando son significativas; el modelo debe incluir covarianzas o reformular las influencias comunes.","jcgm-100-2008","Section 5.2.5","methodological_requirement","medium","direct"),
("La incertidumbre expandida requiere declarar el factor de cobertura y su interpretación; usar k=2 no garantiza por sí solo una probabilidad exacta universal de 95 %.","bipm-vim-expanded-uncertainty","VIM3 entries 2.35–2.38 and GUM section 6","interpretation_boundary","medium","direct"),
("Cuando la no linealidad del modelo vuelve insuficiente una propagación linealizada, deben considerarse métodos apropiados para el modelo, incluida la propagación de distribuciones cuando corresponda.","jcgm-101-2008","Scope of distribution propagation by Monte Carlo; JCGM 100 Amendment 1:2026","methodological_requirement","medium","direct"),
("Una evaluación de conformidad combina la propiedad medida, el requisito especificado y una regla de decisión previamente establecida que considere la incertidumbre y las consecuencias de decisiones incorrectas.","jcgm-106-2012","Sections 5.1.1–5.1.3","decision_principle","high","direct"),
("La trazabilidad metrológica y un certificado de calibración no demuestran por sí solos que un sistema sea apto para un uso biomédico definido ni que posea validez clínica.","nist-tn-2156-traceability","Section 5.4.3 plus VIM3 2.41 scope boundary","interpretation_boundary","high","direct"),
]


def block(tid: str, sid: int, text: str):
    return {"id":f"BIOINST-U08-T{tid}-ST{sid:02d}-B01","type":"paragraph","text":text}


def sub(tid: str, sid: int, title: str, text: str):
    return {"id":f"BIOINST-U08-T{tid}-ST{sid:02d}","title":title,"blocks":[block(tid,sid,text)]}


def topic(tid: str, title: str, subs: list, points: list, blocks=None):
    return {"id":f"BIOINST-U08-T{tid}","title":title,"blocks":blocks or [],"key_points":points,"subtopics":subs}


unit["status"] = {
    "content":"in_review","sources":"traceable","pedagogy":"in_review","multimedia":"planned",
    "internal_review":"pending","external_review":"pending","publication":"published_provisional"
}
unit["purpose"] = "Construir y auditar evidencia de desempeño metrológico mediante diseños de caracterización reproducibles, calibración, propiedades estáticas y dinámicas, presupuestos de incertidumbre y reglas de decisión, sin convertir una prueba educativa en acreditación o validación clínica."
unit["topics"] = [
    topic("01","1. Diseñar antes de medir",[
        sub("01",1,"El diseño determina qué propiedad puede estimarse",claim_specs[0][0]+" Una única curva ascendente puede mezclar respuesta a la entrada, deriva, calentamiento, historia y ruido; para separar efectos se necesitan repeticiones, direcciones, referencias intercaladas y una cronología explícita."),
        sub("01",2,"Los criterios se preespecifican",claim_specs[1][0]+" El requisito debe expresarse con magnitud, unidad, rango, condiciones y regla de comparación suficientes para que dos analistas puedan reproducir la decisión sin mover el umbral después de ver los datos."),
        sub("01",3,"Las condiciones pertenecen al resultado",claim_specs[2][0]+" Temperatura, alimentación, montaje, operador, procedimiento, tiempo desde encendido y versión de procesamiento pueden actuar como cantidades de influencia; registrarlas permite delimitar dónde son transferibles los resultados."),
    ],[claim_specs[0][0],claim_specs[1][0],claim_specs[2][0]]),
    topic("02","2. Calibración, ajuste, verificación y validación",[
        sub("02",1,"Calibrar establece una relación",claim_specs[3][0]+" La relación puede expresarse mediante una curva, corrección o función con su incertidumbre y dominio; calibrar no significa automáticamente que el dispositivo quede dentro de tolerancia."),
        sub("02",2,"Ajustar cambia el sistema",claim_specs[4][0]+" Un cero, offset o ganancia modificados cambian la respuesta y por tanto invalidan la suposición de que la calibración previa sigue describiendo el estado posterior."),
        sub("02",3,"Verificar no es validar",claim_specs[5][0]+" U8 usa verificación para comparar evidencia de desempeño con requisitos metrológicos predefinidos; la adecuación del conjunto de requisitos al uso previsto se profundiza en U9 y no se declara mediante una sola curva de calibración."),
    ],[claim_specs[3][0],claim_specs[4][0],claim_specs[5][0]]),
    topic("03","3. Desempeño estático, temporal e historia",[
        sub("03",1,"Sensibilidad y resolución responden preguntas distintas",claim_specs[6][0]+" La sensibilidad cuantifica cuánto cambia la indicación frente a un cambio de entrada; la resolución describe el cambio mínimo que produce una variación perceptible de indicación y puede depender del ruido o del punto de operación."),
        sub("03",2,"Precisión, repetibilidad, reproducibilidad y deriva",claim_specs[7][0]+" "+claim_specs[8][0]+" Un diseño que cambia operador, sesión o montaje sin registrarlo no permite saber si el aumento de dispersión proviene de reproducibilidad, deriva o una influencia no controlada."),
        sub("03",3,"La caracterización dinámica necesita un criterio temporal",claim_specs[10][0]+" Una respuesta escalón permite estimar retraso, sobreimpulso, constante de tiempo o tiempo de establecimiento según el modelo; esos parámetros deben vincularse al requisito temporal real del uso declarado."),
    ],[claim_specs[6][0],claim_specs[7][0],claim_specs[10][0]],blocks=[{"id":"BIOINST-U08-T03-B01","type":"equation","latex":"S=\\frac{\\Delta y}{\\Delta x},\\quad e_i=y_i-y_{ref,i}","label":"Sensibilidad local y error de indicación dentro de condiciones declaradas.","variables":{"S":"sensibilidad local","e_i":"error en el punto i"}}]),
    topic("04","4. Modelo, linealidad e incertidumbre",[
        sub("04",1,"La linealidad pertenece al modelo",claim_specs[9][0]+" Deben inspeccionarse residuales, dominio y patrón de error: un R² elevado puede coexistir con sesgo estructurado o errores relevantes cerca de los extremos."),
        sub("04",2,"Histéresis, deriva y dinámica se separan por diseño",claim_specs[11][0]+" Comparar subida y bajada dentro de un mismo ciclo explora dependencia de trayectoria; repetir referencias en distintos tiempos explora deriva; esperar o modelar el transitorio evita confundir dinámica con error estático."),
        sub("04",3,"Tipo A y Tipo B son rutas de evaluación",claim_specs[12][0]+" Una componente evaluada estadísticamente puede reflejar varias causas y una componente evaluada por certificado, especificación o conocimiento previo puede representar efectos sistemáticos o aleatorios; la clasificación describe el método de evaluación."),
    ],[claim_specs[9][0],claim_specs[11][0],claim_specs[12][0]]),
    topic("05","5. Combinar incertidumbre sin perder el modelo",[
        sub("05",1,"La covarianza importa cuando las entradas comparten influencias",claim_specs[13][0]+" Si dos correcciones dependen de la misma temperatura o referencia, tratarlas como independientes puede subestimar o sobreestimar la incertidumbre combinada."),
        sub("05",2,"Expandir no es aplicar un 2 automático",claim_specs[14][0]+" El informe debe distinguir incertidumbre estándar combinada, incertidumbre expandida, factor de cobertura y, cuando se declara, la base para una probabilidad o intervalo de cobertura."),
        sub("05",3,"La no linealidad puede exigir otra propagación",claim_specs[15][0]+" La elección entre linealización, métodos analíticos o Monte Carlo se justifica a partir del modelo y de la calidad de la aproximación, no por preferencia de software."),
    ],[claim_specs[13][0],claim_specs[14][0],claim_specs[15][0]],blocks=[{"id":"BIOINST-U08-T05-B01","type":"equation","latex":"u_c^2=\\sum_i c_i^2u_i^2+2\\sum_{i<j}c_ic_j\\,u(x_i,x_j),\\quad U=ku_c","label":"Combinación con términos de covarianza y expansión.","variables":{"c_i":"coeficiente de sensibilidad","u_i":"incertidumbre estándar","u(x_i,x_j)":"covarianza","k":"factor de cobertura"}}]),
    topic("06","6. Regla de decisión y aptitud limitada para el uso",[
        sub("06",1,"Medir, comparar y decidir son operaciones distintas",claim_specs[16][0]+" Un mismo resultado puede producir decisiones diferentes bajo reglas transparentes distintas; por eso la regla y el riesgo de decisión deben declararse antes de emitir una afirmación de conformidad."),
        sub("06",2,"Las guard bands gestionan riesgo de decisión", "Una zona de guarda desplaza el límite de aceptación respecto del límite de tolerancia para gestionar el riesgo de aceptar o rechazar incorrectamente; no cambia el requisito técnico original. La elección de la regla debe documentar quién asume el riesgo y qué incertidumbre se usa."),
        sub("06",3,"Trazable no significa automáticamente apto",claim_specs[17][0]+" La decisión de U8 se limita al desempeño medido bajo condiciones declaradas; seguridad, eficacia, validez clínica, acreditación y uso previsto completo requieren evidencia adicional y revisión competente."),
    ],[claim_specs[16][0],"Una zona de guarda desplaza el límite de aceptación respecto del límite de tolerancia para gestionar el riesgo de aceptar o rechazar incorrectamente; no cambia el requisito técnico original.",claim_specs[17][0]]),
]

unit["examples"] = [
    {
        "id":"BIOINST-U08-EJ01","title":"Calibrar, ajustar y recalibrar",
        "scenario":"Una cadena presenta +8 mV de offset en cinco puntos. Se mide primero, luego se corrige el cero y se quiere conservar la curva anterior.",
        "reasoning_steps":["Registrar la relación previa como calibración del estado inicial.","Clasificar la corrección de cero como ajuste porque modifica indicaciones.","Reconocer que el estado metrológico cambió.","Repetir la calibración/verificación pertinente antes de usar la nueva relación."],
        "interpretation":"La curva previa documenta el estado anterior; el ajuste no convierte automáticamente el estado posterior en calibrado.",
        "limitations":["Ejemplo educativo; no prescribe periodicidad ni procedimiento de calibración de un equipo real."]
    },
    {
        "id":"BIOINST-U08-EJ02","title":"Sensibilidad y residuales",
        "scenario":"Entradas 0, 25, 50, 75 y 100 unidades producen 0.02, 0.51, 1.01, 1.48 y 1.96 V.",
        "reasoning_steps":["Estimar una pendiente aproximada de 1.94/100 = 19.4 mV/unidad entre extremos.","Ajustar un modelo lineal y calcular residuales punto a punto.","Comparar residuales con el requisito, no solo con R².","Revisar extremos y patrón de residuales."],
        "interpretation":"La pendiente resume sensibilidad en el dominio, pero la decisión sobre linealidad depende de residuales y criterios predefinidos.",
        "limitations":["La pendiente por extremos no sustituye un ajuste con incertidumbre."]
    },
    {
        "id":"BIOINST-U08-EJ03","title":"Separar repetibilidad, reproducibilidad e historia",
        "scenario":"Cinco repeticiones consecutivas tienen SD 0.10 kPa; una segunda sesión con nuevo montaje tiene media desplazada +0.35 kPa y ciclos subida/bajada difieren 0.20 kPa.",
        "reasoning_steps":["Asignar la SD cercana a repetibilidad bajo las condiciones fijadas.","Tratar el cambio entre sesiones como evidencia a estudiar bajo condiciones cambiadas, no como repetibilidad.","Usar la diferencia subida/bajada como indicador de histéresis del protocolo.","No atribuir el desplazamiento a deriva sin controlar referencias y ambiente."],
        "interpretation":"Tres patrones distintos requieren diseños distintos para identificar sus causas.",
        "limitations":["Los números no identifican mecanismos físicos por sí solos."]
    },
    {
        "id":"BIOINST-U08-EJ04","title":"Respuesta temporal y criterio",
        "scenario":"Un modelo de primer orden pasa de 0 a 100 unidades con τ=2 s y el requisito exige quedar dentro de ±5 % del valor final.",
        "reasoning_steps":["A 1τ la respuesta ideal alcanza 63.2 %.","Resolver exp(-t/τ)≤0.05.","Obtener t≥-2 ln(0.05)≈5.99 s.","Comparar el tiempo calculado con el requisito declarado."],
        "interpretation":"El tiempo de establecimiento depende del criterio; τ y tiempo al ±5 % no son sinónimos.",
        "limitations":["Modelo ideal de primer orden sin sobreimpulso ni ruido."]
    },
    {
        "id":"BIOINST-U08-EJ05","title":"Incertidumbre independiente y correlacionada",
        "scenario":"Dos contribuciones estándar son 0.20 y 0.10 kPa. Se comparan independencia y correlación ρ=0.8 con coeficientes unitarios.",
        "reasoning_steps":["Independencia: uc=sqrt(0.20²+0.10²)=0.224 kPa.","Correlación: añadir 2ρu1u2=0.032 kPa².","Obtener uc=sqrt(0.082)=0.286 kPa.","Explicar por qué ignorar correlación cambia el resultado."],
        "interpretation":"La misma lista de componentes produce distinta incertidumbre si cambia la estructura de dependencia.",
        "limitations":["ρ es supuesto educativo y debe justificarse en un caso real."]
    },
    {
        "id":"BIOINST-U08-EJ06","title":"Regla de decisión cerca de un límite",
        "scenario":"Requisito y≤10.0 unidades; resultado 9.8 con incertidumbre expandida U=0.4. Una regla educativa predefinida acepta solo si y+U≤10.0.",
        "reasoning_steps":["Aplicar la regla definida antes de mirar el resultado.","Calcular 9.8+0.4=10.2.","Concluir que la regla no permite aceptar conformidad.","Distinguir la decisión de la afirmación de que el valor verdadero necesariamente incumple."],
        "interpretation":"La incertidumbre y la regla modifican el límite de aceptación sin cambiar el límite de tolerancia.",
        "limitations":["La regla es un ejemplo educativo, no una regla universal de laboratorio o regulación."]
    },
]

unit["activities"] = [{
    "id":"BIOINST-U08-ACT01","title":"Expediente reproducible de caracterización y decisión",
    "purpose":"Diseñar y ejecutar sobre datos sintéticos una caracterización que separe propiedades estáticas, temporales e históricas, construya un presupuesto de incertidumbre y aplique una regla de decisión preespecificada sin afirmar acreditación ni validez clínica.",
    "prerequisite_unit_ids":["BIOINST-U07"],"estimated_duration_minutes":240,
    "instructions":[
        "Antes de calcular, redactar el uso educativo, cinco requisitos medibles y la regla de decisión; fechar y bloquear esa especificación para no adaptarla a los resultados.",
        "Trabajar solo con un conjunto sintético que incluya cinco niveles de entrada, ciclos subida/bajada, repeticiones cercanas, dos sesiones, una respuesta escalón y metadatos ambientales.",
        "Mantener separadas calibración, ajuste, verificación y validación; si se simula un ajuste, generar un estado posterior y exigir una nueva relación de calibración.",
        "Para cada métrica registrar definición operativa, ecuación/código, unidad, condiciones, supuestos, incertidumbre y limitación de inferencia.",
        "Cerrar con una decisión limitada al requisito y regla predefinidos, dejando explícitamente fuera acreditación, certificación, seguridad y validez clínica."
    ],
    "tasks":[
        "Construir el plan de caracterización: rango, puntos, orden, repeticiones, dirección, tiempo de estabilización, referencias intercaladas y condiciones que se mantienen/cambian.",
        "Estimar una curva de calibración sintética con sensibilidad, offset, residuales y dominio; comparar un ajuste lineal con la evidencia de no linealidad en residuales.",
        "Separar resolución, repetibilidad, reproducibilidad, histéresis y deriva usando exclusivamente comparaciones que el diseño permita; marcar como no identificable cualquier causa confundida.",
        "Caracterizar la respuesta escalón con al menos τ o tiempo de establecimiento definido por un criterio y relacionarlo con un requisito temporal preespecificado.",
        "Construir un presupuesto de incertidumbre con al menos cinco componentes Tipo A/Tipo B, coeficientes, unidades, distribuciones o fuentes y combinación estándar.",
        "Recalcular un escenario con dos entradas correlacionadas y explicar cuándo la suma cuadrática independiente deja de ser defendible; añadir una nota sobre no linealidad/Monte Carlo si el modelo lo requiere.",
        "Aplicar dos reglas de decisión transparentes a un resultado cercano al límite —una sin guard band y otra con zona de guarda— y comparar riesgo/resultado sin cambiar el requisito original.",
        "Auditar la cadena de trazabilidad y redactar una matriz final `evidencia disponible → afirmación permitida → evidencia todavía necesaria`, incluyendo por qué un certificado no demuestra aptitud biomédica completa."
    ],
    "deliverables":[
        "Especificación bloqueada con uso educativo, requisitos, criterios y regla de decisión fechados antes del análisis.",
        "Dataset sintético y tabla de metadatos con orden, sesión, dirección, tiempo, referencia y condiciones.",
        "Notebook/hoja reproducible con curva, residuales, métricas estáticas y análisis temporal.",
        "Presupuesto de incertidumbre con componentes, unidades, coeficientes, correlaciones y resultado estándar/expandido.",
        "Tabla comparativa de decisiones con/sin guard band y explicación del riesgo de decisión.",
        "Informe final de 2–3 páginas con conclusión limitada, trazabilidad, brechas y preguntas para revisión humana."
    ],
    "checking_criteria":[
        "Requisitos y regla de decisión están fechados antes del análisis y no se modifican para acomodar resultados.",
        "Calibración, ajuste, verificación y validación se usan con significados distintos.",
        "Sensibilidad, resolución, precisión y exactitud no se presentan como sinónimos.",
        "Repetibilidad y reproducibilidad declaran explícitamente sus condiciones.",
        "Histéresis, deriva y dinámica se separan por diseño o se marcan como no identificables si están confundidas.",
        "La linealidad se evalúa con modelo, dominio y residuales, no solo con R².",
        "El presupuesto declara cada componente, unidad, método Tipo A/B, coeficiente y correlación pertinente.",
        "El factor de cobertura y la interpretación de incertidumbre expandida están declarados y no se promete 95 % universal por usar k=2.",
        "La regla de decisión distingue límite de tolerancia y límite de aceptación/guard band.",
        "La conclusión niega explícitamente que trazabilidad, calibración o la práctica demuestren acreditación, certificación, seguridad o validez clínica."
    ],
    "status":"curated_pending_expert_review"
}]

assessment["purpose"] = "Evaluar diseño de caracterización, vocabulario metrológico, desempeño, incertidumbre y reglas de decisión mediante casos que obligan a separar cálculo, evidencia y afirmaciones de aptitud."
assessment["student_payload_policy"] = "Las claves y explicaciones se excluyen del payload inicial del estudiante; la revisión disciplinaria humana y cualquier afirmación de uso biomédico real permanecen pendientes."
items = [
    ("Q01","Un laboratorio compara indicaciones con un patrón y después modifica el cero del instrumento. El informe llama 'calibración' a ambas operaciones y reutiliza la curva previa. Corrige la secuencia.",["BIOINST-U08-LO01"],"La comparación inicial puede formar parte de una calibración; modificar el cero es un ajuste. Como el ajuste cambia el sistema, la relación previa no debe asumirse válida y normalmente se requiere recalibrar/verificar el estado posterior.","VIM distingue explícitamente calibración y ajuste y señala que tras ajustar suele requerirse una nueva calibración.",["calibration-equals-adjustment","old-calibration-survives-adjustment"],["bipm-vim-calibration","bipm-vim-adjustment"]),
    ("Q02","Un equipo cumple todos los requisitos metrológicos escritos y concluye que el dispositivo está 'validado para su uso clínico'. Evalúa la afirmación.",["BIOINST-U08-LO01","BIOINST-U08-LO05"],"La evidencia puede apoyar verificación de requisitos especificados. No demuestra que esos requisitos sean suficientes para el uso clínico ni constituye validación clínica; esa adecuación exige evidencia adicional del uso previsto y revisión competente.","Verificación y validación no son equivalentes; la validación añade adecuación de requisitos para un uso especificado.",["verification-equals-validation","metrology-proves-clinical-use"],["bipm-vim-verification","bipm-vim-validation"]),
    ("Q03","Una curva de cinco puntos tiene R²=0.9999, pero los residuales son positivos en ambos extremos y negativos en el centro. ¿Puede declararse lineal sin más?",["BIOINST-U08-LO02"],"No. El patrón de residuales sugiere estructura no capturada por el modelo lineal. Deben declararse dominio, criterio de linealidad, magnitud de residuales e incertidumbre y considerar un modelo alternativo si el efecto es relevante.","Un R² alto no prueba adecuación del modelo; la no linealidad debe evaluarse respecto del modelo y de los requisitos.",["r2-proves-linearity","small-relative-error-everywhere"],["jcgm-gum-6-2020","jcgm-100-amd1-2026"]),
    ("Q04","Cinco repeticiones consecutivas son muy consistentes, pero una segunda sesión con nuevo montaje desplaza la media. El informe dice 'la reproducibilidad es excelente porque la repetibilidad fue excelente'. Corrige.",["BIOINST-U08-LO02"],"La baja dispersión de repeticiones próximas apoya repetibilidad bajo esas condiciones. La reproducibilidad requiere evaluar condiciones cambiadas y puede ser peor; el desplazamiento entre sesiones debe investigarse como efecto de condición, deriva o sesgo antes de atribuir causa.","Precisión depende de condiciones especificadas; repetibilidad y reproducibilidad responden a conjuntos de condiciones distintos.",["repeatability-equals-reproducibility","shift-must-be-random-noise"],["bipm-vim-repeatability","bipm-vim-reproducibility","bipm-vim-instrumental-drift"]),
    ("Q05","Dos componentes estándar de 0.20 y 0.10 kPa se combinan como independientes, aunque ambas dependen de la misma referencia y se estima ρ=0.8. ¿Qué está mal y cuál es uc con coeficientes unitarios?",["BIOINST-U08-LO03"],"La independencia no es defendible. Debe incluirse la covarianza: uc²=0.20²+0.10²+2·0.8·0.20·0.10=0.082 kPa², por lo que uc≈0.286 kPa.","JCGM 100 indica que correlaciones significativas no deben ignorarse; una influencia común puede modelarse explícitamente.",["rss-always-valid","correlation-only-affects-mean"],["jcgm-100-2008"]),
    ("Q06","Un informe multiplica uc por k=2 y escribe '95 % exacto garantizado' sin indicar distribución, grados de libertad ni método. Evalúa.",["BIOINST-U08-LO03"],"Debe reportar U=k·uc con k declarado y justificar la interpretación de cobertura. k=2 se usa con frecuencia, pero por sí solo no garantiza una probabilidad exacta universal de 95 % para cualquier modelo/distribución.","Factor de cobertura, intervalo y probabilidad de cobertura son conceptos relacionados pero no equivalentes por simple convención.",["k2-always-exact-95","expanded-uncertainty-is-standard-deviation"],["bipm-vim-expanded-uncertainty","bipm-vim-coverage-factor","jcgm-100-2008"]),
    ("Q07","El requisito es y≤10.0; se mide 9.8 con U=0.4. El analista decide después de ver el resultado usar la regla 'aceptar si y≤10'. ¿Qué problema existe?",["BIOINST-U08-LO04","BIOINST-U08-LO05"],"La regla de decisión no estaba preespecificada y omite cómo se usa la incertidumbre/riesgo de decisión. Debe declararse antes; una posible regla con guard band puede cambiar el límite de aceptación sin cambiar el límite de tolerancia, pero su elección debe justificarse.","Conformidad requiere propiedad medida, requisito y regla de decisión previamente establecida; adaptar la regla después del resultado introduce sesgo decisional.",["tolerance-equals-acceptance-limit","decision-rule-can-be-chosen-after-data"],["jcgm-106-2012","ilac-g8-2019"]),
    ("Q08","Un sensor tiene certificado de calibración trazable, baja incertidumbre y buena repetibilidad en banco. ¿Qué puede afirmarse y qué sigue sin demostrarse para un uso biomédico?",["BIOINST-U08-LO02","BIOINST-U08-LO03","BIOINST-U08-LO04","BIOINST-U08-LO05"],"Puede afirmarse el desempeño demostrado bajo las condiciones y alcance documentados, incluida la cadena de calibración pertinente. No se demuestra automáticamente desempeño del sistema completo, condiciones clínicas, seguridad, utilidad, validación del uso previsto o acreditación de la actividad del curso.","Trazabilidad pertenece al resultado y un artefacto calibrado no transfiere automáticamente trazabilidad ni aptitud al resultado del usuario.",["traceable-means-fit-for-use","certificate-proves-clinical-validity"],["bipm-vim-traceability","nist-tn-2156-traceability"]),
]
assessment["items"] = []
for qid,prompt,los,expected,explanation,misconceptions,source_ids in items:
    assessment["items"].append({
        "id":f"BIOINST-U08-{qid}","type":"case_analysis","prompt":prompt,
        "linked_learning_outcome_ids":los,"difficulty":"advanced","cognitive_level":"evaluate",
        "answer_key":{"expected_answer":expected,"explanation":explanation,"common_misconceptions":misconceptions},
        "feedback":{"correct":"La respuesta separa propiedad medida, condiciones, modelo/incertidumbre y alcance de la decisión.","incorrect":"Reformula el caso identificando qué se midió, bajo qué condiciones, qué requisito/regla se aplica y qué afirmación excede la evidencia."},
        "source_ids":source_ids,"status":"curated_pending_expert_review"
    })
assessment["status"] = "curated_pending_expert_review"


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().casefold())


def next_glossary_id() -> str:
    nums=[]
    for e in glossary["entries"]:
        m=re.fullmatch(r"BIOINST-GLO-(\d+)",e.get("id",""))
        if m: nums.append(int(m.group(1)))
    return f"BIOINST-GLO-{max(nums, default=0)+1:03d}"


def ensure_glossary(term: str, definition: str, source_ids: list[str], locators: list[tuple[str,str]], status: str="verified_directly") -> str:
    entry = next((e for e in glossary["entries"] if norm(e.get("term","")) == norm(term)), None)
    if entry is None:
        entry={"id":next_glossary_id(),"term":term,"definition":definition,"unit_ids":[],"source_ids":[],"verification_status":status}
        glossary["entries"].append(entry)
    entry["definition"] = definition
    entry["unit_ids"] = sorted(set(entry.get("unit_ids", [])) | {"BIOINST-U08"})
    entry["source_ids"] = source_ids
    entry["verification_status"] = status
    entry["source_locators"] = [{"source_id":sid,"locator":loc} for sid,loc in locators]
    return entry["id"]


gloss_specs = [
("Caracterización","Determinación experimental y documentada del comportamiento de un sistema bajo entradas, condiciones, secuencias y criterios declarados.",["jcgm-gum-6-2020"],[('jcgm-gum-6-2020','Measurement models and influence quantities')],"verified_contextually"),
("Calibración","Operación que establece bajo condiciones especificadas la relación entre valores de referencia con sus incertidumbres y las indicaciones correspondientes, y usa esa relación para obtener resultados desde indicaciones.",["bipm-vim-calibration"],[('bipm-vim-calibration','VIM3 entry 2.39 and notes')],"verified_directly"),
("Ajuste","Conjunto de operaciones que modifica un sistema de medición para proporcionar indicaciones prescritas; no debe confundirse con calibración.",["bipm-vim-adjustment"],[('bipm-vim-adjustment','VIM3 entry 3.11 and notes')],"verified_directly"),
("Verificación","Aporte de evidencia objetiva de que una entidad dada satisface requisitos especificados.",["bipm-vim-verification"],[('bipm-vim-verification','VIM3 entry 2.44')],"verified_directly"),
("Repetibilidad","Precisión de medición bajo un conjunto de condiciones de repetibilidad declarado.",["bipm-vim-repeatability"],[('bipm-vim-repeatability','VIM3 entries 2.20–2.21')],"verified_directly"),
("Reproducibilidad","Precisión de medición bajo condiciones de reproducibilidad en las que se declaran las condiciones que cambian.",["bipm-vim-reproducibility"],[('bipm-vim-reproducibility','VIM3 entries 2.24–2.25')],"verified_directly"),
("Linealidad","Adecuación de una relación lineal declarada dentro de un dominio y condiciones; se evalúa mediante el modelo y sus residuales, no como propiedad universal.",["jcgm-gum-6-2020","jcgm-100-amd1-2026"],[('jcgm-gum-6-2020','Measurement-model framework'),('jcgm-100-amd1-2026','Amendment 1:2026 on nonlinearity')],"verified_contextually"),
("Deriva","Cambio continuo o incremental en el tiempo de la indicación debido a cambios en propiedades metrológicas del instrumento, no a un cambio del mensurando o influencia reconocida.",["bipm-vim-instrumental-drift"],[('bipm-vim-instrumental-drift','VIM3 entry 4.21 and note')],"verified_directly"),
("Incertidumbre estándar","Incertidumbre de medición expresada como desviación estándar.",["bipm-vim-standard-uncertainty"],[('bipm-vim-standard-uncertainty','VIM3 entry 2.30')],"verified_directly"),
("Incertidumbre combinada","Incertidumbre estándar obtenida usando las incertidumbres estándar asociadas a las cantidades de entrada de un modelo de medición.",["bipm-vim-combined-uncertainty"],[('bipm-vim-combined-uncertainty','VIM3 entry 2.31')],"verified_directly"),
("Incertidumbre expandida","Producto de una incertidumbre estándar combinada por un factor mayor que uno para expresar un intervalo de cobertura bajo una interpretación declarada.",["bipm-vim-expanded-uncertainty"],[('bipm-vim-expanded-uncertainty','VIM3 entries 2.35–2.38')],"verified_directly"),
("Criterio de aceptación","Condición predefinida usada para decidir aceptación dentro de una regla de decisión, distinguida del límite de tolerancia cuando se aplica una zona de guarda.",["jcgm-106-2012","ilac-g8-2019"],[('jcgm-106-2012','Section 5.1 decision rule'),('ilac-g8-2019','Guidance on decision rules and guard bands')],"verified_contextually"),
("Sensibilidad","Cociente entre el cambio de una indicación y el cambio correspondiente de la cantidad medida.",["bipm-vim-sensitivity"],[('bipm-vim-sensitivity','VIM3 entry 4.12')],"verified_directly"),
("Resolución","Menor cambio de la cantidad medida que causa un cambio perceptible en la indicación, dependiente potencialmente de ruido, fricción o punto de operación.",["bipm-vim-resolution"],[('bipm-vim-resolution','VIM3 entry 4.14 and note')],"verified_directly"),
("Histéresis","Dependencia de la indicación respecto de la historia o dirección de recorrido dentro de un protocolo declarado; debe separarse experimentalmente de deriva y dinámica.",["jcgm-gum-6-2020"],[('jcgm-gum-6-2020','Influence quantities and measurement-model design')],"verified_contextually"),
("Trazabilidad metrológica","Propiedad de un resultado de medición por la que puede relacionarse con una referencia mediante una cadena documentada e ininterrumpida de calibraciones, cada una contribuyendo a la incertidumbre.",["bipm-vim-traceability"],[('bipm-vim-traceability','VIM3 entry 2.41 and notes')],"verified_directly"),
("Precisión de medición","Proximidad del acuerdo entre indicaciones o valores medidos obtenidos mediante mediciones repetidas bajo condiciones especificadas.",["bipm-vim-precision"],[('bipm-vim-precision','VIM3 entry 2.15 and notes')],"verified_directly"),
("Factor de cobertura","Número mayor que uno por el que se multiplica una incertidumbre estándar combinada para obtener una incertidumbre expandida.",["bipm-vim-coverage-factor"],[('bipm-vim-coverage-factor','VIM3 entry 2.38')],"verified_directly"),
]
unit["glossary_entry_ids"] = [ensure_glossary(*spec) for spec in gloss_specs]

claims["claims"] = [c for c in claims["claims"] if c.get("unit_id") != "BIOINST-U08"]
new_claims=[]
for i,(text,source_id,locator,claim_type,risk,support) in enumerate(claim_specs,1):
    cid=f"BIOINST-U08-C{i:03d}"
    source=next(s for s in sources["sources"] if s["id"]==source_id)
    new_claims.append({
        "claim_id":cid,"unit":8,"text":text,"claim_type":claim_type,"risk":risk,
        "context":"Aplicado a caracterización educativa de Bioinstrumentación U8; la conclusión concreta depende del mensurando, modelo, condiciones, requisito y regla de decisión declarados.",
        "source_id":source_id,"locator":{"section":locator},"support":support,
        "source_verification_status":source["verification_status"],"review_state":"ai_review_provisional",
        "reviewer_validation_id":None,"reviewed_at":"2026-08-24","id":cid,"unit_id":"BIOINST-U08"
    })
claims["claims"].extend(new_claims)
claims["content_version"] = "units-01-08-review-2026-08-24"
claims["scope"] = "Afirmaciones centrales de Bioinstrumentación con fuente y localizador; Unidades 1–8 integradas y revisión disciplinaria humana pendiente."
unit["claim_ids"] = [c["id"] for c in new_claims]
unit["source_ids"] = [
    "bipm-vim-calibration","bipm-vim-adjustment","bipm-vim-verification","bipm-vim-validation",
    "bipm-vim-precision","bipm-vim-repeatability","bipm-vim-reproducibility","bipm-vim-standard-uncertainty",
    "bipm-vim-combined-uncertainty","bipm-vim-expanded-uncertainty","bipm-vim-coverage-factor",
    "bipm-vim-sensitivity","bipm-vim-resolution","bipm-vim-instrumental-drift","bipm-vim-step-response-time","bipm-vim-traceability",
    "jcgm-gum-6-2020","jcgm-100-2008","jcgm-100-amd1-2026","jcgm-101-2008","jcgm-gum-5-2026","jcgm-106-2012","ilac-g8-2019","nist-tn-2156-traceability"
]
unit["common_errors"] = [
    {"error":"Usar calibración y ajuste como sinónimos.","correction":"Registrar primero la relación de calibración; si se modifica cero/ganancia, documentar el ajuste y recalibrar el estado posterior."},
    {"error":"Concluir linealidad por un R² alto.","correction":"Examinar modelo, dominio, residuales y criterio de error máximo."},
    {"error":"Llamar reproducibilidad a repeticiones consecutivas.","correction":"Declarar qué condiciones permanecen constantes y cuáles cambian."},
    {"error":"Combinar incertidumbres como independientes por defecto.","correction":"Buscar influencias comunes y añadir covarianzas o reformular el modelo cuando proceda."},
    {"error":"Interpretar k=2 como 95 % exacto universal.","correction":"Declarar factor, método y base de la interpretación de cobertura."},
    {"error":"Elegir la regla de decisión después de ver el resultado.","correction":"Preespecificar requisito, incertidumbre utilizada, guard band y consecuencias de decisión."},
]
unit["biomedical_connections"] = [
    "Calibración de sensores fisiológicos: la cadena de referencia y la incertidumbre pertenecen al resultado, no al nombre comercial del instrumento.",
    "Monitoreo biomédico: repetibilidad de banco no garantiza reproducibilidad entre sesiones, montajes o entornos.",
    "Validación posterior: U8 produce evidencia metrológica que U9 debe relacionar con requisitos, riesgos y uso previsto antes de cualquier conclusión de aptitud amplia."
]
unit["editorial_notice"] = "Autoría canónica nueva conforme al mapa de migración: canonical U8 tiene origin=new y action=author, sin unidad autoral histórica equivalente en data/course_redevelopment. El marco metrológico general queda trazable, pero la revisión disciplinaria humana, los casos biomédicos específicos, la acreditación, la conformidad y la validez clínica permanecen pendientes o fuera de alcance."
unit["legacy_origin"] = "data/generated_units/bioinstrumentacion/unit-08.json (bootstrap público; no existe equivalente autoral legacy)"

# Internal consistency checks before writing.
assert len(unit["topics"]) == 6
assert sum(len(t["subtopics"]) for t in unit["topics"]) == 18
assert len(unit["examples"]) == 6
assert len(unit["activities"][0]["instructions"]) == 5
assert len(unit["activities"][0]["tasks"]) == 8
assert len(unit["activities"][0]["deliverables"]) == 6
assert len(unit["activities"][0]["checking_criteria"]) == 10
assert len(assessment["items"]) == 8
assert len(unit["glossary_entry_ids"]) == 18
assert len(new_claims) == 18
serialized=json.dumps(unit,ensure_ascii=False)
for c in new_claims:
    assert c["text"] in serialized

# Sanity-check numeric examples.
assert abs(math.sqrt(0.20**2+0.10**2)-0.2236067977) < 1e-6
assert abs(math.sqrt(0.20**2+0.10**2+2*0.8*0.20*0.10)-0.2863564213) < 1e-6

dump(unit_path,unit)
dump(assessment_path,assessment)
dump(glossary_path,glossary)
dump(sources_path,sources)
dump(claims_path,claims)
print("Curated canonical Bioinstrumentation U8 as new authoring unit")
