#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

unit_path = COURSE / "units" / "unit-06.json"
assessment_path = COURSE / "assessments" / "unit-06.json"
glossary_path = COURSE / "glossary.json"
sources_path = COURSE / "sources.json"
claims_path = COURSE / "claims.json"
unit = load(unit_path)
assessment = load(assessment_path)
glossary = load(glossary_path)
sources = load(sources_path)
claims = load(claims_path)
legacy = load(ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json")
migration = load(ROOT / "data/course_migrations/bioinstrumentacion-numbering-v1.json")
practices = load(ROOT / "data/practice_implementations/bioinstrumentacion-unit-05.json")
legacy_assessment = load(ROOT / "data/assessment_implementations/bioinstrumentacion-unit-05.json")

row = next(x for x in migration["canonical_sequence"] if x["canonical_unit"] == 6)
assert row["origin"] == "legacy_unit_5" and row["action"] == "migrate_without_rewriting"
assert legacy["unit"] == 5 and legacy["limits"]["professional_review_claimed"] is False
assert legacy["limits"]["public_release_authorized"] is False
assert legacy["limits"]["U5-A5_status"] == "pending_real_human_review"
assert practices["global_limits"]["synthetic_only"] is True
assert legacy_assessment["limits"]["professional_review_claimed"] is False


def upsert_source(record):
    existing = next((s for s in sources["sources"] if s["id"] == record["id"]), None)
    if existing is None:
        sources["sources"].append(record)
        return
    for k, v in record.items():
        if k == "used_by_unit_ids":
            existing[k] = sorted(set(existing.get(k, [])) | set(v))
        elif k not in existing or existing[k] in (None, "", [], {}):
            existing[k] = v
    existing["used_by_unit_ids"] = sorted(set(existing.get("used_by_unit_ids", [])) | {"BIOINST-U06"})

new_sources = [
    {"id":"nist-pressure-vacuum-calibrations","title":"Pressure/Vacuum Calibrations","organization":"National Institute of Standards and Technology","url":"https://www.nist.gov/programs-projects/pressurevacuum-calibrations","type":"institutional_metrology_reference","verification_status":"verified_directly","locator":"Low Pressure Manometry and calibration-service descriptions; page updated 2026-05-11","curricular_function":"Respaldar que presión absoluta y diferencial requieren modos/referencias de medición explícitos y que la calibración se realiza en rangos/condiciones definidos.","limitations":"La página describe capacidades NIST; no fija una arquitectura universal de sensor biomédico.","coverage":[6],"used_by_unit_ids":["BIOINST-U06"]},
    {"id":"nist-piston-gauges-2026","title":"Piston gauges and pressure transducers","organization":"National Institute of Standards and Technology","url":"https://www.nist.gov/laboratories/tools-instruments/piston-gauges-and-pressure-transducers","type":"institutional_metrology_reference","verification_status":"verified_directly","locator":"Description of gauge mode versus absolute mode; updated 2026-01-15","curricular_function":"Distinguir modo manométrico respecto de atmósfera y modo absoluto con evacuación de la referencia.","limitations":"Describe estándares de presión NIST; no generaliza exactitud ni desempeño dinámico a sensores de campo.","coverage":[6],"used_by_unit_ids":["BIOINST-U06"]},
    {"id":"nist-liquid-flow-sp250-98","title":"Liquid Flow Meter Calibrations with NIST's 15 kg/s Water Flow Standard","organization":"National Institute of Standards and Technology","url":"https://www.nist.gov/publications/liquid-flow-meter-calibrations-nists-15-kgs-water-flow-standard","type":"nist_special_publication","verification_status":"verified_directly","locator":"Abstract and NIST SP 250-98; dynamic gravimetric standard, mass and volume flow","curricular_function":"Respaldar la separación entre caudal másico y volumétrico, la calibración de caudal y el papel de densidad/condiciones.","limitations":"El estándar NIST usa agua y una instalación específica; no prescribe medición biomédica ni convierte una velocidad local en caudal total.","coverage":[6],"used_by_unit_ids":["BIOINST-U06"]},
    {"id":"iupac-transmittance-2025","title":"IUPAC Gold Book — transmittance","organization":"International Union of Pure and Applied Chemistry","url":"https://goldbook.iupac.org/terms/view/T06484","type":"official_terminology","verification_status":"verified_directly","locator":"Gold Book 5th ed., T06484","curricular_function":"Definir transmitancia como razón entre potencia radiante transmitida e incidente y distinguir pérdidas por absorción, reflexión y dispersión.","limitations":"La definición no resuelve por sí sola geometría tisular, concentración ni validación de un sensor óptico.","coverage":[6],"used_by_unit_ids":["BIOINST-U06"]},
    {"id":"iupac-beer-lambert-2025","title":"IUPAC Gold Book — Beer–Lambert law","organization":"International Union of Pure and Applied Chemistry","url":"https://goldbook.iupac.org/terms/view/B00626","type":"official_terminology","verification_status":"verified_directly","locator":"Gold Book 5th ed., B00626","curricular_function":"Respaldar A=log10(P0/P)=εcl y sus condiciones de medio homogéneo/isotrópico y radiación espectral estrecha.","limitations":"No autoriza aplicar Beer–Lambert sin verificar dispersión, geometría, trayectoria, composición y otras desviaciones del modelo.","coverage":[6],"used_by_unit_ids":["BIOINST-U06"]},
    {"id":"iupac-reflectance-2025","title":"IUPAC Gold Book — reflectance","organization":"International Union of Pure and Applied Chemistry","url":"https://goldbook.iupac.org/terms/view/R05235","type":"official_terminology","verification_status":"verified_directly","locator":"Gold Book 5th ed., R05235","curricular_function":"Definir reflectancia como fracción de potencia radiante incidente reflejada.","limitations":"La definición no especifica geometría de colección ni convierte reflectancia en concentración o diagnóstico.","coverage":[6],"used_by_unit_ids":["BIOINST-U06"]},
    {"id":"iupac-scattering-2025","title":"IUPAC Gold Book — scattering","organization":"International Union of Pure and Applied Chemistry","url":"https://goldbook.iupac.org/terms/view/S05487","type":"official_terminology","verification_status":"verified_directly","locator":"Gold Book 5th ed., S05487","curricular_function":"Definir dispersión como cambio de dirección o energía de radiación por interacción.","limitations":"No proporciona un modelo completo de transporte óptico en tejido ni una inversión única desde señal detectada a composición.","coverage":[6],"used_by_unit_ids":["BIOINST-U06"]},
]
for s in new_sources:
    upsert_source(s)
for sid in ["vishay-ntc-thermistor-u2","jcgm-gum-1-2023","jcgm-gum-6-2020","bipm-vim-calibration","bipm-vim-traceability"]:
    existing = next((s for s in sources["sources"] if s["id"] == sid), None)
    assert existing is not None, sid
    existing["used_by_unit_ids"] = sorted(set(existing.get("used_by_unit_ids", [])) | {"BIOINST-U06"})
sources["consulted_on"] = "2026-08-24"

claim_specs = [
("La interpretación de una presión depende de su referencia: el modo absoluto se relaciona con una referencia evacuada, mientras el modo manométrico se relaciona con la presión atmosférica.","nist-piston-gauges-2026","Gauge mode versus absolute mode","interpretation_boundary","medium","direct"),
("Una presión diferencial compara dos presiones y debe conservar qué puerto o referencia define el signo.","nist-pressure-vacuum-calibrations","Low Pressure Manometry: absolute and differential pressure","methodological_requirement","medium","direct"),
("Una calibración de presión es válida para un rango, configuración y condiciones documentadas; no elimina dependencias de temperatura, montaje o dinámica fuera de lo evaluado.","nist-pressure-vacuum-calibrations","Calibration service ranges and conditions","interpretation_boundary","high","indirect"),
("La temperatura del elemento sensible puede diferir de la del objeto y del ambiente durante un transitorio o cuando existe autocalentamiento.","vishay-ntc-thermistor-u2","Datasheet/application-note response and dissipation specifications","interpretation_boundary","medium","direct"),
("En un modelo térmico de primer orden, la constante de tiempo caracteriza la escala de aproximación al equilibrio bajo las condiciones del modelo y no es universal para cualquier montaje.","vishay-ntc-thermistor-u2","Response-time conditions and thermal behavior","interpretation_boundary","medium","direct"),
("Después de una constante de tiempo, un primer orden ideal completa aproximadamente el 63.2% del cambio total y conserva cerca del 36.8% del error inicial.","jcgm-gum-6-2020","Use of explicit measurement models and model assumptions","methodological_requirement","low","indirect"),
("Velocidad local, caudal volumétrico y caudal másico son magnitudes diferentes y no deben intercambiarse.","nist-liquid-flow-sp250-98","Mass-flow and volume-flow calibration quantities","definition","medium","direct"),
("Relacionar caudal volumétrico y másico requiere densidad compatible con las condiciones del fluido; relacionar velocidad local y caudal requiere además área y un modelo del perfil de velocidad.","nist-liquid-flow-sp250-98","Flow equations and uncertainty context","methodological_requirement","high","indirect"),
("Una calibración de caudal conserva método, fluido, rango y presupuesto de incertidumbre; no convierte cualquier lectura puntual en una estimación trazable del caudal total.","nist-liquid-flow-sp250-98","Calibration method and uncertainty","interpretation_boundary","high","indirect"),
("La transmitancia es la razón entre potencia radiante transmitida e incidente y el valor total puede incorporar pérdidas por absorción, reflexión y dispersión.","iupac-transmittance-2025","T06484","definition","low","direct"),
("La absorbancia de Beer–Lambert se relaciona con log10(P0/P), longitud de trayectoria y concentración bajo condiciones de validez que deben verificarse.","iupac-beer-lambert-2025","B00626","methodological_requirement","medium","direct"),
("La reflectancia es una fracción de la radiación incidente reflejada y depende de la configuración óptica; no es sinónimo de transmitancia ni absorbancia.","iupac-reflectance-2025","R05235","definition","low","direct"),
("La dispersión cambia la dirección o energía de la radiación y puede romper una interpretación simple basada solo en absorción.","iupac-scattering-2025","S05487 and Beer–Lambert limitations","interpretation_boundary","medium","direct"),
("Calibración, trazabilidad e incertidumbre responden a preguntas diferentes y deben conservarse como conceptos separados.","bipm-vim-calibration","VIM calibration plus traceability/uncertainty concepts","interpretation_boundary","high","indirect"),
("Un presupuesto de incertidumbre combina contribuciones solo después de definir el mensurando, el modelo, las unidades y las dependencias relevantes.","jcgm-gum-6-2020","Developing and using measurement models","methodological_requirement","high","direct"),
("Combinar modalidades puede aumentar la descripción disponible de un sistema, pero no convierte asociaciones entre presión, temperatura, flujo u óptica en diagnóstico o mecanismo clínico demostrado.","jcgm-gum-1-2023","Measurement-result and inference boundary used in educational context","interpretation_boundary","high","indirect"),
("Una práctica sintética de sensores no caracteriza automáticamente hardware físico, seguridad, conformidad o desempeño clínico.","jcgm-gum-1-2023","Scope boundary between measurement model and use decision","interpretation_boundary","high","indirect"),
("La decisión de seleccionar una modalidad debe explicitar magnitud, referencia, rango, dinámica, geometría, calibración, incertidumbre y evidencia faltante para el uso previsto.","jcgm-gum-6-2020","Measurement-model development and fitness-for-purpose context","decision_principle","high","direct"),
]


def p(tid, sid, text):
    return {"id":f"BIOINST-U06-T{tid}-ST{sid:02d}-B01","type":"paragraph","text":text}
def st(tid,sid,title,text):
    return {"id":f"BIOINST-U06-T{tid}-ST{sid:02d}","title":title,"blocks":[p(tid,sid,text)]}
def tp(tid,title,subs,points,blocks=None):
    return {"id":f"BIOINST-U06-T{tid}","title":title,"blocks":blocks or [],"key_points":points,"subtopics":subs}

unit["topics"] = [
    tp("01","1. Presión, referencia e interfaz mecánica",[
        st("01",1,"La referencia define qué presión se está midiendo","Una cifra en pascales no especifica por sí sola la magnitud completa. Debe declararse si la referencia es vacío, ambiente o un segundo puerto, además del signo, el intervalo y el estado dinámico. La conversión entre referencias requiere que la referencia exista y sea temporalmente compatible."),
        st("01",2,"La transducción añade geometría y carga","Membranas, diafragmas y elementos piezorresistivos o capacitivos responden mediante deformación y una cadena eléctrica posterior. Área efectiva, rigidez, temperatura, montaje y distribución de carga pueden modificar la indicación sin cambiar el nombre comercial del sensor."),
        st("01",3,"Calibración de presión no garantiza cualquier uso","Una relación obtenida en un rango y configuración definidos no demuestra comportamiento fuera de ese rango, durante transitorios rápidos o con otra interfaz mecánica. El expediente debe separar calibración, corrección, deriva y evidencia de aptitud."),
    ],[claim_specs[0][0],claim_specs[1][0],claim_specs[2][0]],[{"id":"BIOINST-U06-T01-B01","type":"equation","latex":"P=F/A","label":"Definición ideal de presión media normal sobre un área efectiva.","variables":{"P":"presión","F":"fuerza normal","A":"área efectiva"}}]),
    tp("02","2. Temperatura, equilibrio y respuesta dinámica",[
        st("02",1,"Sensor, objeto y ambiente son temperaturas distintas","El elemento sensible intercambia energía con el objeto y con el ambiente. Contacto, convección, radiación, encapsulado y potencia de lectura pueden hacer que su temperatura no coincida con la que se pretende estimar."),
        st("02",2,"La constante de tiempo pertenece al modelo y al montaje","Un primer orden aproxima la transición con una escala temporal tau. Cambiar medio, flujo, encapsulado, masa térmica o contacto puede cambiar la respuesta; por eso un tiempo de hoja de datos debe conservar sus condiciones de ensayo."),
        st("02",3,"El tiempo de espera debe derivarse del error permitido","A una tau aún queda una fracción importante del error inicial. El criterio útil no es 'esperar hasta que parezca estable', sino declarar un error residual tolerable, el modelo que lo relaciona con el tiempo y las perturbaciones que pueden invalidarlo."),
    ],[claim_specs[3][0],claim_specs[4][0],claim_specs[5][0]],[{"id":"BIOINST-U06-T02-B01","type":"equation","latex":"T_s(t)=T_f+(T_0-T_f)e^{-t/\\tau}","label":"Respuesta ideal de primer orden hacia un equilibrio térmico.","variables":{"T_s":"temperatura del sensor","T_f":"equilibrio final","T_0":"estado inicial","tau":"constante de tiempo"}}]),
    tp("03","3. Velocidad local, caudal volumétrico y caudal másico",[
        st("03",1,"Una velocidad puntual no es el caudal de un conducto","El caudal volumétrico integra la componente normal del campo de velocidad sobre un área. Sustituir esa integral por velocidad por área exige una velocidad media representativa y una geometría definida."),
        st("03",2,"La densidad añade condiciones termodinámicas","El paso de caudal volumétrico a másico requiere densidad. En líquidos puede aproximarse como constante en ciertos rangos; en gases depende de presión, temperatura y composición y puede requerir una ecuación de estado."),
        st("03",3,"El principio de medida condiciona el modelo","Presión diferencial, transferencia térmica, desplazamiento, ultrasonido u otros métodos observan variables distintas. Cada uno necesita una calibración, un modelo de instalación y un análisis de perturbaciones propio."),
    ],[claim_specs[6][0],claim_specs[7][0],claim_specs[8][0]],[{"id":"BIOINST-U06-T03-B01","type":"equation","latex":"Q=\\int_A \\mathbf{v}\\cdot d\\mathbf{A},\\quad \\dot{m}=\\rho Q","label":"Relación entre campo de velocidad, caudal volumétrico y caudal másico.","variables":{"Q":"caudal volumétrico","v":"campo de velocidad","rho":"densidad","m_dot":"caudal másico"}}]),
    tp("04","4. Transmitancia, absorbancia, reflectancia y dispersión",[
        st("04",1,"Cada modalidad óptica tiene una razón y una geometría","Transmitancia compara potencia transmitida con incidente; reflectancia compara potencia reflejada con incidente; la dispersión describe redirección o cambio de energía. Longitud de onda, apertura, ángulos, trayectoria y referencia forman parte de la medición."),
        st("04",2,"Beer–Lambert es un modelo con condiciones explícitas","La relación lineal entre absorbancia, concentración y longitud de trayectoria presupone un medio y una iluminación compatibles con el modelo. Dispersión, luz parásita, heterogeneidad, saturación u otras interacciones pueden introducir desviaciones."),
        st("04",3,"Una intensidad detectada no identifica una causa única","Cambios de fuente, geometría, detector, trayectoria, absorción, reflectancia o dispersión pueden alterar la misma lectura. Antes de atribuir un cambio a composición deben controlarse o modelarse esas rutas alternativas."),
    ],[claim_specs[9][0],claim_specs[10][0],claim_specs[11][0],claim_specs[12][0]],[{"id":"BIOINST-U06-T04-B01","type":"equation","latex":"T=P/P_0,\\quad A=-\\log_{10}(T)","label":"Transmitancia y absorbancia decádica bajo una referencia óptica definida.","variables":{"P":"potencia transmitida","P_0":"potencia incidente de referencia","T":"transmitancia","A":"absorbancia"}}]),
    tp("05","5. Calibración, incertidumbre y comparación de modalidades",[
        st("05",1,"Una lista de especificaciones no es un presupuesto metrológico","Sensibilidad, resolución, repetibilidad, histéresis, deriva, tiempo de respuesta e incertidumbre describen propiedades diferentes. La comparación requiere definiciones y condiciones compatibles, no una sola cifra de catálogo."),
        st("05",2,"La incertidumbre empieza por el modelo","Antes de combinar términos deben definirse mensurando, ecuación, entradas, correcciones, dependencias y unidades. La combinación RSS solo es defendible cuando la representación probabilística y las dependencias usadas la justifican."),
        st("05",3,"La calibración no sustituye la aptitud para el uso","Una cadena puede estar calibrada y seguir siendo inadecuada por rango, dinámica, geometría, perturbación o incertidumbre. La decisión debe comparar evidencia con requisitos explícitos del propósito educativo o técnico."),
    ],[claim_specs[13][0],claim_specs[14][0]],[]),
    tp("06","6. Integración multimodal y límites de inferencia",[
        st("06",1,"Integrar no significa fusionar magnitudes","Presión, temperatura, flujo y óptica conservan unidades, referencias, tiempos de respuesta y geometrías propias. Un expediente multimodal debe alinear tiempo y contexto sin transformar automáticamente una modalidad en otra."),
        st("06",2,"Concordancia entre sensores no demuestra mecanismo clínico","Dos o más modalidades pueden cambiar juntas por una causa común, por una perturbación compartida o por el diseño del escenario sintético. La asociación es evidencia para investigar, no un diagnóstico ni una prueba causal suficiente."),
        st("06",3,"La selección se cierra con una matriz de requisitos y evidencia","Para cada modalidad deben registrarse magnitud, referencia, rango, dinámica, geometría, calibración, incertidumbre, perturbaciones, procedencia y evidencia faltante. Esa matriz permite justificar selección o descarte sin convertir una comparación educativa en validación de dispositivo."),
    ],[claim_specs[15][0],claim_specs[16][0],claim_specs[17][0]],[]),
]

unit["examples"] = [
    {"id":"BIOINST-U06-EJ01","title":"Presión manométrica a absoluta","scenario":"Un caso sintético indica 18 kPa manométricos y una referencia atmosférica simultánea de 101 kPa.","reasoning_steps":["Declarar ambas referencias y unidades.","Aplicar P_abs=P_gauge+P_atm.","Obtener 119 kPa.","Registrar que cambiar la referencia temporal cambia el resultado."],"interpretation":"La conversión es defendible solo porque la referencia atmosférica está disponible y es compatible.","limitations":["No describe un sensor físico ni una presión fisiológica."]},
    {"id":"BIOINST-U06-EJ02","title":"Respuesta térmica a una constante de tiempo","scenario":"Sensor ideal de 20 °C hacia 50 °C con tau=10 s.","reasoning_steps":["Aplicar el primer orden.","Usar 1-e^-1≈0.632.","Obtener 38.96 °C a 10 s.","Cuantificar el error residual de 11.04 °C respecto del equilibrio."],"interpretation":"Una tau no equivale a equilibrio; el tiempo requerido depende del error permitido.","limitations":["Modelo concentrado sin contacto variable ni autocalentamiento."]},
    {"id":"BIOINST-U06-EJ03","title":"De velocidad media a caudal","scenario":"v_media=0.50 m/s, A=0.002 m² y rho=1000 kg/m³.","reasoning_steps":["Justificar que v es media representativa.","Calcular Q=vA=0.001 m³/s.","Calcular m_dot=rho Q=1 kg/s.","Registrar constancia de área y densidad."],"interpretation":"Los resultados dependen de los supuestos de perfil y densidad, no solo de la aritmética.","limitations":["Sin pulsatilidad, compresibilidad ni perfil espacial complejo."]},
    {"id":"BIOINST-U06-EJ04","title":"Transmitancia a absorbancia","scenario":"La potencia transmitida es 25% de la referencia incidente bajo la misma geometría.","reasoning_steps":["Definir T=P/P0=0.25.","Calcular A=-log10(T)=0.602.","Registrar longitud de onda y trayectoria.","Revisar si dispersión/luz parásita violan el modelo simple."],"interpretation":"0.602 es una absorbancia matemática bajo la referencia dada; no identifica concentración sin un modelo adicional válido.","limitations":["No se presupone tejido homogéneo ni Beer–Lambert válido automáticamente."]},
    {"id":"BIOINST-U06-EJ05","title":"Presupuesto educativo de incertidumbre","scenario":"Tres contribuciones estándar independientes de 0.20, 0.10 y 0.05 kPa.","reasoning_steps":["Comprobar que comparten magnitud/unidades.","Combinar por RSS bajo independencia declarada.","Obtener u_c≈0.229 kPa.","Con k=2, obtener U≈0.458 kPa y declarar que el factor necesita justificación."],"interpretation":"El cálculo ilustra combinación de un modelo; no constituye calibración acreditada ni certificado.","limitations":["Independencia y distribuciones son supuestos educativos."]},
    {"id":"BIOINST-U06-EJ06","title":"Patrón multimodal sintético","scenario":"Aumentan presión y temperatura, cambia el caudal y disminuye transmitancia en un simulador.","reasoning_steps":["Describir cada observación por separado.","Alinear escalas temporales y unidades.","Proponer hipótesis comunes y alternativas.","Separar hipótesis de diagnóstico o mecanismo no demostrado."],"interpretation":"La integración organiza evidencia, pero no convierte correlación sintética en validez clínica.","limitations":["Sin personas, hardware ni resultado clínico."]},
]

unit["activities"] = [{
    "id":"BIOINST-U06-ACT01","title":"Matriz multimodal de sensores y evidencia","purpose":"Comparar presión, temperatura, flujo y óptica mediante magnitudes, referencias, dinámica, geometría, calibración e incertidumbre usando exclusivamente las prácticas sintéticas históricas U5-P1/U5-P2/U5-P3.","prerequisite_unit_ids":["BIOINST-U05"],"estimated_duration_minutes":240,
    "instructions":["Registrar primero el crosswalk `legacy U5 → canonical U6` y conservar los identificadores históricos U5-P1/U5-P2/U5-P3.","Ejecutar o reconstruir las tres prácticas sintéticas sin conectar sensores, hardware biomédico ni personas.","Para cada modalidad separar observación, transformación matemática, supuesto, incertidumbre y límite de inferencia.","Usar una matriz común de comparación sin forzar una única métrica: rango, referencia, sensibilidad, dinámica, geometría, calibración, incertidumbre y perturbaciones.","Cerrar con una selección o descarte justificado para un propósito educativo explícito y una lista de evidencia que faltaría para cualquier sistema real."],
    "tasks":["Resolver un caso de presión absoluta/manométrica/diferencial con signo, referencia y rango explícitos.","Auditar una curva sintética de presión con offset, histéresis y saturación sin confundirlos con ruido.","Estimar tau de la práctica térmica y calcular error residual a 1τ, 2τ y 3τ.","Separar temperatura de objeto, sensor y ambiente e identificar una ruta de autocalentamiento o contacto que sesgaría la lectura.","Calcular caudal volumétrico y másico desde un perfil sintético y demostrar por qué una velocidad local aislada no basta.","Calcular transmitancia/absorbancia y comparar un cambio de geometría o luz parásita que produzca una interpretación alternativa.","Construir un presupuesto de incertidumbre educativo y señalar qué contribuciones son correlacionadas, modeladas o todavía desconocidas.","Integrar las cuatro modalidades en una matriz de requisitos y redactar una inferencia permitida, una hipótesis pendiente y tres afirmaciones clínicas/seguridad/conformidad que no pueden sostenerse."],
    "deliverables":["Tabla de procedencia legacy U5 → canonical U6 y mapa de las tres prácticas históricas.","Informe de presión con referencia, curva carga-descarga y diagnóstico de no idealidades.","Informe térmico con tau, error residual, ambiente y autocalentamiento.","Informe de flujo con velocidad, área, densidad, caudal volumétrico/másico y supuestos.","Informe óptico con geometría, longitud de onda, referencia, transmitancia/absorbancia y rutas alternativas.","Matriz multimodal final con presupuesto de incertidumbre, decisión, evidencia faltante y límites de inferencia."],
    "checking_criteria":["El crosswalk histórico está explícito y no se renombran retroactivamente U5-P1/U5-P2/U5-P3.","Toda presión conserva referencia, signo, unidades y rango.","Histéresis, saturación, offset, ruido y deriva no se colapsan en una sola categoría.","La respuesta térmica separa sensor, objeto y ambiente y vincula tiempo con error residual.","Velocidad local, caudal volumétrico y caudal másico permanecen diferenciados dimensionalmente.","Toda conversión de caudal declara área/perfil y densidad/condiciones cuando corresponda.","Transmitancia, absorbancia, reflectancia y dispersión se mantienen como conceptos distintos y con geometría explícita.","Beer–Lambert se usa solo bajo supuestos declarados y no como inversión universal de concentración.","El presupuesto de incertidumbre declara modelo, unidades, dependencias y supuestos antes de combinar términos.","La integración multimodal no afirma diagnóstico, seguridad, conformidad ni desempeño clínico."],"status":"curated_pending_expert_review"
}]
unit["status"].update({"content":"in_review","sources":"traceable","pedagogy":"in_review","multimedia":"planned","internal_review":"pending","external_review":"pending","publication":"published_provisional"})
unit["purpose"] = "Promover legacy U5 como canonical U6 y comparar sensores mecánicos, térmicos, de flujo y ópticos mediante magnitud, referencia, dinámica, geometría, calibración, incertidumbre y límites de inferencia, preservando la evidencia histórica y sin extrapolar prácticas sintéticas a hardware o clínica."


def q(i,prompt,los,answer,explain,mis,source_ids,difficulty="advanced",level="evaluate"):
    return {"id":f"BIOINST-U06-Q{i:02d}","type":"case_analysis","prompt":prompt,"linked_learning_outcome_ids":los,"difficulty":difficulty,"cognitive_level":level,"answer_key":{"expected_answer":answer,"explanation":explain,"common_misconceptions":mis},"feedback":{"correct":"La respuesta conserva magnitud, referencia, modelo, condiciones y límite de inferencia.","incorrect":"Reformula primero qué se mide, respecto de qué referencia, con qué geometría/dinámica y qué evidencia falta antes de interpretar."},"source_ids":source_ids,"status":"curated_pending_expert_review"}
assessment["purpose"]="Evaluar la comparación metrológica de presión, temperatura, flujo y óptica preservando la procedencia legacy U5 → canonical U6 y exigiendo límites explícitos de inferencia."
assessment["student_payload_policy"]="Las respuestas completas no se muestran antes del intento; el caso integrador y cualquier juicio de aptitud requieren revisión humana." 
assessment["items"]=[
q(1,"Un sensor marca 18 kPa manométricos y el ambiente simultáneo es 101 kPa. Otro informe compara directamente esos 18 kPa con un sensor absoluto. ¿Qué corrección conceptual y numérica necesitas?",["BIOINST-U06-LO01"],"Declarar referencia y convertir: 18 kPa manométricos corresponden aproximadamente a 119 kPa absolutos si la referencia atmosférica compatible es 101 kPa. No comparar cifras con referencias distintas sin conversión.","La referencia es parte de la definición operacional de la presión y puede cambiar en el tiempo.",["pressure-reference-omitted","gauge-equals-absolute"],["nist-piston-gauges-2026","nist-pressure-vacuum-calibrations"]),
q(2,"Un sensor térmico de primer orden con tau=10 s se inserta en un objeto que pasa de 20 a 50 °C. A los 10 s se lee 38.96 °C y el informe declara 'temperatura del objeto =38.96 °C'. Evalúa.",["BIOINST-U06-LO02"],"La lectura es la temperatura modelada del sensor durante el transitorio, no necesariamente la del objeto. A 1τ queda ~36.8% del error inicial y además contacto, ambiente y autocalentamiento pueden modificar la relación.","El modelo describe la dinámica del elemento sensible bajo supuestos; no identifica automáticamente la temperatura del objeto.",["one-tau-is-equilibrium","sensor-temperature-equals-object"],["vishay-ntc-thermistor-u2","jcgm-gum-6-2020"]),
q(3,"Una sonda mide 0.50 m/s en un punto de un conducto de 0.002 m² y se reporta Q=0.001 m³/s sin más datos. ¿Cuándo es defendible y qué falta?",["BIOINST-U06-LO03"],"Solo si 0.50 m/s representa adecuadamente la velocidad media normal al área y la geometría está definida. Una velocidad local aislada no determina la integral de flujo; falta perfil/representatividad y, para flujo másico, densidad compatible.","Q=vA es una simplificación de la integral de velocidad y requiere supuestos espaciales.",["point-velocity-equals-flow","density-unnecessary"],["nist-liquid-flow-sp250-98"]),
q(4,"Dos medidores entregan el mismo valor numérico de caudal, uno en L/min y otro en kg/min. Un equipo concluye que son equivalentes. ¿Qué datos necesitas para compararlos?",["BIOINST-U06-LO03"],"Son magnitudes distintas. Para relacionarlas hace falta densidad bajo presión, temperatura y composición compatibles; también deben compararse intervalos y condiciones de calibración.","El flujo másico y volumétrico solo se relacionan mediante propiedades del fluido y condiciones declaradas.",["mass-flow-equals-volume-flow","density-is-constant-universally"],["nist-liquid-flow-sp250-98"]),
q(5,"Una muestra presenta T=0.25. Calcula A y explica por qué A=0.602 no permite por sí sola calcular concentración en un tejido heterogéneo.",["BIOINST-U06-LO04"],"A=-log10(0.25)=0.602. Obtener concentración por Beer–Lambert requiere trayectoria, coeficiente, longitud de onda y condiciones de validez; dispersión, heterogeneidad o luz parásita pueden romper el modelo simple.","La absorbancia es una razón transformada; la inversión a concentración exige un modelo físico adicional válido.",["absorbance-directly-is-concentration","beer-lambert-universal"],["iupac-transmittance-2025","iupac-beer-lambert-2025","iupac-scattering-2025"]),
q(6,"Un cambio de intensidad óptica se atribuye automáticamente a absorción. Enumera al menos tres rutas alternativas que deben auditarse y una prueba que mejore la discriminación.",["BIOINST-U06-LO04"],"Revisar cambios de fuente, geometría/alineación, reflectancia, dispersión, luz parásita, detector o trayectoria. Repetir con referencia y geometría controladas y, cuando proceda, variar longitud de onda/ángulo para contrastar hipótesis.","La intensidad detectada mezcla varias rutas ópticas y no identifica de forma única el mecanismo.",["all-optical-loss-is-absorption","geometry-does-not-matter"],["iupac-transmittance-2025","iupac-reflectance-2025","iupac-scattering-2025"]),
q(7,"Un presupuesto contiene 0.20, 0.10 y 0.05 kPa y aplica RSS sin indicar qué representan. ¿Qué debe documentarse antes de aceptar 0.229 kPa?",["BIOINST-U06-LO05"],"Definir mensurando/modelo, unidades y naturaleza de cada contribución, su evaluación estándar y dependencias/correlaciones. RSS directo solo es coherente bajo supuestos adecuados, por ejemplo contribuciones estándar independientes.","La aritmética de incertidumbre depende del modelo y de las relaciones entre entradas; una lista de números no basta.",["rss-always-valid","calibration-eliminates-uncertainty"],["jcgm-gum-6-2020","jcgm-gum-1-2023"]),
q(8,"En un simulador aumentan presión y temperatura, cambia el flujo y disminuye transmitancia. El informe concluye un diagnóstico clínico. Redacta una conclusión defendible y la evidencia que faltaría.",["BIOINST-U06-LO01","BIOINST-U06-LO02","BIOINST-U06-LO03","BIOINST-U06-LO04","BIOINST-U06-LO05"],"Conclusión defendible: varias modalidades sintéticas cambiaron de forma temporalmente asociada bajo las condiciones del simulador y son compatibles con una perturbación común. No identifica diagnóstico, mecanismo biológico, seguridad ni desempeño clínico. Harían falta definición de uso, datos/mediciones válidas, validación del sistema y revisión competente.","La integración multimodal organiza evidencia, pero no cambia el nivel de inferencia autorizado por los datos.",["multimodal-means-clinically-valid","synthetic-pattern-is-diagnosis"],["jcgm-gum-1-2023","jcgm-gum-6-2020"])
]
assessment["status"]="curated_pending_expert_review"

term_specs=[
("Presión absoluta","Presión referida a una referencia de vacío o modo absoluto definido.",["nist-piston-gauges-2026"]),
("Presión manométrica","Presión expresada respecto de la presión atmosférica de referencia en el modo declarado.",["nist-piston-gauges-2026"]),
("Presión diferencial","Diferencia entre dos presiones o puertos con signo y referencia explícitos.",["nist-pressure-vacuum-calibrations"]),
("Área efectiva","Área utilizada por el modelo para relacionar fuerza y presión o velocidad media y caudal; debe derivarse de la geometría pertinente, no elegirse arbitrariamente.",["nist-pressure-vacuum-calibrations","nist-liquid-flow-sp250-98"]),
("Constante de tiempo térmica","Parámetro de un primer orden que caracteriza la escala temporal de aproximación al equilibrio bajo condiciones de montaje y medio especificadas.",["vishay-ntc-thermistor-u2"]),
("Autocalentamiento","Elevación o perturbación de la temperatura del elemento sensible causada por la energía disipada durante su excitación o lectura.",["vishay-ntc-thermistor-u2"]),
("Velocidad local","Velocidad del fluido asociada a una posición; no equivale al caudal total sin integración o un modelo del perfil.",["nist-liquid-flow-sp250-98"]),
("Caudal volumétrico","Volumen de fluido que atraviesa una superficie por unidad de tiempo.",["nist-liquid-flow-sp250-98"]),
("Caudal másico","Masa de fluido que atraviesa una superficie por unidad de tiempo.",["nist-liquid-flow-sp250-98"]),
("Transmitancia","Razón entre potencia radiante transmitida e incidente bajo una referencia definida.",["iupac-transmittance-2025"]),
("Absorbancia","Logaritmo decádico de la razón entre potencia incidente de referencia y transmitida, bajo la definición óptica correspondiente.",["iupac-beer-lambert-2025"]),
("Reflectancia","Fracción de radiación incidente reflejada por una superficie o discontinuidad.",["iupac-reflectance-2025"]),
("Dispersión","Proceso en el que la radiación cambia de dirección o energía por interacción con materia.",["iupac-scattering-2025"]),
("Trayectoria óptica","Camino geométrico de propagación usado por el modelo de medición; su longitud y geometría condicionan relaciones de absorbancia/transmitancia.",["iupac-beer-lambert-2025"]),
("Presupuesto de incertidumbre","Representación documentada de las contribuciones, modelo y combinación usados para evaluar incertidumbre de un resultado.",["jcgm-gum-6-2020"]),
("Integración multimodal","Organización conjunta de resultados de modalidades distintas preservando sus magnitudes, referencias, tiempos, incertidumbres y límites de inferencia.",["jcgm-gum-1-2023","jcgm-gum-6-2020"]),
]
locator={
"nist-piston-gauges-2026":"Gauge mode and absolute mode description","nist-pressure-vacuum-calibrations":"Low Pressure Manometry and calibration services","nist-liquid-flow-sp250-98":"NIST SP 250-98 abstract and calibration method","vishay-ntc-thermistor-u2":"Product response/dissipation documentation","iupac-transmittance-2025":"Gold Book T06484","iupac-beer-lambert-2025":"Gold Book B00626","iupac-reflectance-2025":"Gold Book R05235","iupac-scattering-2025":"Gold Book S05487","jcgm-gum-6-2020":"Measurement-model clauses","jcgm-gum-1-2023":"Introduction to measurement uncertainty and use"}
entries=glossary["entries"]
max_id=max([int(m.group(1)) for e in entries if (m:=re.search(r"(\d+)$",e["id"]))] or [0])
selected=[]
for term,definition,sids in term_specs:
    e=next((x for x in entries if x["term"].strip().casefold()==term.casefold()),None)
    if e is None:
        max_id+=1; e={"id":f"BIOINST-GLO-{max_id:03d}","term":term}; entries.append(e)
    e.update({"definition":definition,"unit_ids":sorted(set(e.get("unit_ids",[]))|{"BIOINST-U06"}),"source_ids":sids,"verification_status":"verified_directly" if len(sids)==1 else "verified_contextually","source_locators":[{"source_id":sid,"locator":locator[sid]} for sid in sids]})
    selected.append(e["id"])
unit["glossary_entry_ids"]=selected

claims["claims"]=[c for c in claims["claims"] if c.get("unit_id")!="BIOINST-U06"]
new_claims=[]
for i,(text,sid,loc,ctype,risk,support) in enumerate(claim_specs,1):
    cid=f"BIOINST-U06-C{i:03d}"; new_claims.append({"claim_id":cid,"unit":6,"text":text,"claim_type":ctype,"risk":risk,"context":"Aplicado a comparación educativa de sensores mecánicos, térmicos, de flujo y ópticos; la conclusión depende de referencia, geometría, condiciones, calibración y uso previsto.","source_id":sid,"locator":{"section":loc},"support":support,"source_verification_status":"verified_directly","review_state":"ai_review_provisional","reviewer_validation_id":None,"reviewed_at":"2026-08-24","id":cid,"unit_id":"BIOINST-U06"})
claims["claims"].extend(new_claims); claims["scope"]="Afirmaciones centrales de Bioinstrumentación con fuente y localizador; Unidades 1–6 integradas y revisión disciplinaria humana pendiente."; claims["review_state"]="ai_review_provisional"; unit["claim_ids"]=[c["id"] for c in new_claims]

unit["source_ids"]=["nist-pressure-vacuum-calibrations","nist-piston-gauges-2026","vishay-ntc-thermistor-u2","nist-liquid-flow-sp250-98","iupac-transmittance-2025","iupac-beer-lambert-2025","iupac-reflectance-2025","iupac-scattering-2025","jcgm-gum-1-2023","jcgm-gum-6-2020","bipm-vim-calibration","bipm-vim-traceability"]
for sid in unit["source_ids"]:
    s=next((x for x in sources["sources"] if x["id"]==sid),None); assert s is not None,sid; s["used_by_unit_ids"]=sorted(set(s.get("used_by_unit_ids",[]))|{"BIOINST-U06"})

dump(unit_path,unit); dump(assessment_path,assessment); dump(glossary_path,glossary); dump(sources_path,sources); dump(claims_path,claims)
print("Curated canonical Bioinstrumentation U6 from preserved legacy U5 provenance")
