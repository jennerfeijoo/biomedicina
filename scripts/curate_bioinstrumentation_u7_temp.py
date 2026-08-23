#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "bioinstrumentacion"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

unit_path = COURSE / "units" / "unit-07.json"
assessment_path = COURSE / "assessments" / "unit-07.json"
glossary_path = COURSE / "glossary.json"
sources_path = COURSE / "sources.json"
claims_path = COURSE / "claims.json"
unit = load(unit_path)
assessment = load(assessment_path)
glossary = load(glossary_path)
sources = load(sources_path)
claims = load(claims_path)
legacy = load(ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-06.json")
migration = load(ROOT / "data/course_migrations/bioinstrumentacion-numbering-v1.json")
blockers = load(ROOT / "data/unit_preparation/bioinstrumentacion-unit-06-blocker-resolution.json")
practices = load(ROOT / "data/practice_implementations/bioinstrumentacion-unit-06.json")
legacy_assessment = load(ROOT / "data/assessment_implementations/bioinstrumentacion-unit-06.json")

row = next(x for x in migration["canonical_sequence"] if x["canonical_unit"] == 7)
assert row["origin"] == "legacy_unit_6" and row["action"] == "migrate_without_rewriting"
assert legacy["unit"] == 6
assert legacy["safety_boundary"]["synthetic_offline_only"] is True
assert legacy["safety_boundary"]["human_participants_allowed"] is False
assert legacy["safety_boundary"]["energized_medical_devices_allowed"] is False
assert legacy["safety_boundary"]["professional_review_claimed"] is False
assert legacy["editorial_decision"]["human_review_executed"] is False
assert legacy["editorial_decision"]["professional_review_executed"] is False
assert legacy["editorial_decision"]["public_release_authorized"] is False
assert blockers["authorization_decision"]["human_or_energized_medical_device_work_authorized"] is False
assert practices["synthetic_only"] is True and practices["human_participants"] is False and practices["energized_medical_devices"] is False
assert next(a for a in legacy_assessment["assessments"] if a["id"] == "U6-A5")["status"] == "pending_human_execution"


def upsert_source(record: dict) -> None:
    existing = next((s for s in sources["sources"] if s["id"] == record["id"]), None)
    if existing is None:
        sources["sources"].append(record)
        return
    for key, value in record.items():
        if key == "used_by_unit_ids":
            existing[key] = sorted(set(existing.get(key, [])) | set(value))
        elif key not in existing or existing[key] in (None, "", [], {}):
            existing[key] = value
    existing["used_by_unit_ids"] = sorted(set(existing.get("used_by_unit_ids", [])) | {"BIOINST-U07"})

# Existing IEC 60601-1 record is preserved; only usage is extended.
base_iec = next((s for s in sources["sources"] if s["id"] == "iec-60601-1-edition-3-2"), None)
assert base_iec is not None
base_iec["used_by_unit_ids"] = sorted(set(base_iec.get("used_by_unit_ids", [])) | {"BIOINST-U07"})

for record in [
    {
        "id":"iec-60601-1-2-edition-4-1",
        "title":"IEC 60601-1-2:2014+AMD1:2020 CSV — Electromagnetic disturbances — Requirements and tests",
        "organization":"International Electrotechnical Commission",
        "url":"https://webstore.iec.ch/en/publication/67554",
        "type":"standard_metadata",
        "verification_status":"verified_directly",
        "locator":"IEC Webstore: consolidated edition 4.1, publication 2020-09-01, stability date 2028; scope and overview",
        "curricular_function":"Establecer que EMC de equipos electromédicos incluye emisiones e inmunidad frente a perturbaciones, y que la norma complementa IEC 60601-1.",
        "limitations":"Se usa metadata y alcance público. No se reproducen niveles de ensayo, tablas ni criterios normativos de pago, y la unidad no afirma conformidad.",
        "coverage":[7],"used_by_unit_ids":["BIOINST-U07"]
    },
    {
        "id":"iso-14971-2019-current",
        "title":"ISO 14971:2019 — Medical devices — Application of risk management to medical devices",
        "organization":"International Organization for Standardization",
        "url":"https://www.iso.org/standard/72704.html",
        "type":"standard_metadata",
        "verification_status":"verified_directly",
        "locator":"ISO official page; Edition 3 (2019), reviewed and confirmed in 2025; overview of risk-management process",
        "curricular_function":"Respaldar la cadena peligro → riesgo → control → seguimiento y separar análisis educativo de una decisión regulatoria de aceptabilidad.",
        "limitations":"La página pública resume alcance y proceso; no se reproducen requisitos detallados ni se fijan niveles universales de riesgo aceptable.",
        "coverage":[7,9,10],"used_by_unit_ids":["BIOINST-U07"]
    },
    {
        "id":"fda-emc-guidance-2022",
        "title":"Electromagnetic Compatibility (EMC) of Medical Devices — Guidance for Industry and FDA Staff",
        "organization":"U.S. Food and Drug Administration",
        "url":"https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electromagnetic-compatibility-emc-medical-devices",
        "type":"regulatory_guidance",
        "verification_status":"verified_directly",
        "locator":"Final Guidance, June 2022; introduction and scope",
        "curricular_function":"Documentar que la evaluación EMC requiere evidencia de ensayo y documentación apropiada para el dispositivo y su entorno, no solo una simulación conceptual.",
        "limitations":"Guía no vinculante estadounidense; no sustituye normas aplicables, evaluación regulatoria ni un plan de ensayos para un dispositivo concreto.",
        "coverage":[7],"used_by_unit_ids":["BIOINST-U07"]
    },
    {
        "id":"fda-emc-overview-2026",
        "title":"Electromagnetic Compatibility (EMC)",
        "organization":"U.S. Food and Drug Administration",
        "url":"https://www.fda.gov/radiation-emitting-products/radiation-safety/electromagnetic-compatibility-emc",
        "type":"regulatory_overview",
        "verification_status":"verified_directly",
        "locator":"FDA EMC overview; emissions, immunity and examples of conducted/radiated/electrostatic disturbances; accessed 2026-08-24",
        "curricular_function":"Definir EMC como coexistencia sin interferencia inaceptable e introducir emisiones, inmunidad y perturbaciones electromagnéticas.",
        "limitations":"Página general de FDA; no ofrece por sí sola criterios de aceptación o niveles de ensayo para un producto concreto.",
        "coverage":[7],"used_by_unit_ids":["BIOINST-U07"]
    },
]:
    upsert_source(record)
sources["consulted_on"] = "2026-08-24"

claim_specs = [
("La presencia de una tensión no determina por sí sola el riesgo: el modelo debe declarar fuente, energía disponible, trayectoria, impedancia, retorno y elemento potencialmente afectado.","iso-14971-2019-current","Risk-management overview applied to electrical hazard chain","interpretation_boundary","high","indirect"),
("Peligro, situación peligrosa, daño y riesgo no son términos intercambiables y deben mantenerse separados en el análisis.","iso-14971-2019-current","Official overview: hazards, risk estimation/evaluation and controls","definition","high","direct"),
("ISO 14971 organiza la gestión de riesgos como un proceso de ciclo de vida que incluye identificación de peligros, evaluación, control y seguimiento de la efectividad de los controles.","iso-14971-2019-current","Official description of the risk-management framework","methodological_requirement","high","direct"),
("IEC 60601-1 establece requisitos generales de seguridad básica y desempeño esencial para equipos electromédicos, pero normas colaterales o particulares pueden complementar o modificar ese marco.","iec-60601-1-edition-3-2","IEC Webstore scope and relation to collateral/particular standards","interpretation_boundary","high","direct"),
("Dibujar una barrera de aislamiento en un esquema solo declara una intención funcional; no demuestra el desempeño físico ni la conformidad de esa barrera.","iec-60601-1-edition-3-2","General safety/essential-performance scope used as evidence boundary","interpretation_boundary","high","indirect"),
("Referencia de señal, tierra de protección y blindaje cumplen funciones diferentes y no deben tratarse como nodos intercambiables por conveniencia gráfica.","iec-60601-1-edition-3-2","General electrical safety architecture; terminology boundary","interpretation_boundary","high","indirect"),
("Una corriente calculada con I=V/Z describe el modelo y sus unidades; no constituye por sí sola un límite regulatorio ni una conclusión de seguridad.","iec-60601-1-edition-3-2","Standards-scope boundary; no normative limits reproduced","interpretation_boundary","high","indirect"),
("En un modelo sinusoidal ideal, una trayectoria capacitiva depende de frecuencia, capacitancia y tensión, por lo que una resistencia equivalente constante puede ocultar dependencia espectral.","fda-emc-overview-2026","EMI mechanisms include conducted/radiated/electrostatic disturbances; educational circuit model","methodological_requirement","medium","indirect"),
("La compatibilidad electromagnética incluye tanto limitar emisiones que interfieran con otros equipos como mantener desempeño aceptable frente a perturbaciones electromagnéticas.","iec-60601-1-2-edition-4-1","Official scope: emitted disturbances and performance in presence of disturbances","definition","high","direct"),
("IEC 60601-1-2:2014+A1:2020 complementa IEC 60601-1 con requisitos y ensayos relativos a perturbaciones electromagnéticas y emisiones.","iec-60601-1-2-edition-4-1","IEC Webstore consolidated edition 4.1 scope","methodological_requirement","high","direct"),
("La FDA describe entre las fuentes de interferencia electromagnética perturbaciones conducidas, radiadas y descargas electrostáticas.","fda-emc-overview-2026","FDA EMC overview","definition","medium","direct"),
("El esquema fuente–trayectoria–víctima es útil para formular hipótesis de acoplamiento, pero una forma de onda observada no identifica por sí sola el mecanismo.","fda-emc-overview-2026","EMI complexity and environmental sources","interpretation_boundary","medium","indirect"),
("Una mitigación EMC debe verificarse mediante una salida observable y condiciones de ensayo documentadas; reducir una señal en una simulación no demuestra inmunidad o emisiones conformes.","fda-emc-guidance-2022","Guidance scope: EMC testing and information for submissions","methodological_requirement","high","direct"),
("Un análisis de fallo simple compara un estado nominal con una alteración definida para estudiar cómo cambia la cadena de riesgo; el cambio relativo no fija por sí solo aceptabilidad.","iso-14971-2019-current","Risk estimation/evaluation and control process","interpretation_boundary","high","indirect"),
("Los controles de riesgo deben evaluarse dentro de un proceso documentado y su efectividad debe ser objeto de seguimiento; una medida propuesta no es automáticamente un control verificado.","iso-14971-2019-current","Risk-control and monitoring overview","methodological_requirement","high","direct"),
("ISO 14971 no especifica niveles universales de riesgo aceptable; los criterios dependen del dispositivo, el contexto y el proceso definido.","iso-14971-2019-current","Official ISO overview: objective criteria without universal acceptable-risk levels","interpretation_boundary","high","direct"),
("La aplicabilidad normativa depende del equipo, su uso previsto, entorno y estándares colaterales o particulares pertinentes; no debe inferirse desde una lista genérica de normas.","iec-60601-1-edition-3-2","IEC general standard scope and particular-standard caveat","decision_principle","high","direct"),
("Una simulación offline puede apoyar aprendizaje y detectar incoherencias de un modelo, pero no sustituye ensayo, trazabilidad, evaluación profesional, certificación ni evidencia de conformidad.","fda-emc-guidance-2022","Guidance recommends EMC testing/documentation; educational inference boundary","interpretation_boundary","high","indirect"),
]


def block(tid, sid, text):
    return {"id":f"BIOINST-U07-T{tid}-ST{sid:02d}-B01","type":"paragraph","text":text}
def sub(tid,sid,title,text):
    return {"id":f"BIOINST-U07-T{tid}-ST{sid:02d}","title":title,"blocks":[block(tid,sid,text)]}
def topic(tid,title,subs,points,blocks=None):
    return {"id":f"BIOINST-U07-T{tid}","title":title,"blocks":blocks or [],"key_points":points,"subtopics":subs}

unit["topics"] = [
    topic("01","1. De la fuente a la situación peligrosa",[
        sub("01",1,"El riesgo se analiza como cadena causal","Un análisis útil empieza por identificar una fuente de energía o peligro, la trayectoria por la que podría propagarse, el retorno, las barreras y el elemento potencialmente afectado. Una tensión aislada o un número de corriente sin contexto no representa toda la cadena de riesgo."),
        sub("01",2,"Peligro, situación peligrosa, daño y riesgo son capas distintas","El peligro describe una fuente potencial de daño; la situación peligrosa describe exposición a ese peligro; el daño es la consecuencia posible y el riesgo combina probabilidad y severidad según el marco utilizado. Mezclarlos oculta qué evidencia corresponde a cada afirmación."),
        sub("01",3,"La gestión de riesgos no termina en un cálculo","Identificar el peligro es solo el inicio. Un proceso de gestión de riesgos requiere evaluación, controles, verificación de esos controles y seguimiento durante el ciclo de vida, con criterios y documentación apropiados al sistema."),
    ],[claim_specs[0][0],claim_specs[1][0],claim_specs[2][0]]),
    topic("02","2. Barreras, referencia de señal, tierra de protección y blindaje",[
        sub("02",1,"Una barrera define dominios y una función","El diagrama debe declarar qué dominios separa una barrera, qué transferencia de energía o información pretende limitar y qué trayectorias parásitas quedan fuera del modelo. El símbolo no aporta por sí solo tensión soportada, corriente admisible, distancia física o certificación."),
        sub("02",2,"Las conexiones se nombran por función, no por apariencia","La referencia de señal participa en una medición; una tierra de protección pertenece a una arquitectura de protección; un blindaje modifica acoplamientos electromagnéticos. Unirlos o separarlos exige una justificación del sistema, no una regla gráfica universal."),
        sub("02",3,"La norma general no elimina el contexto del equipo","IEC 60601-1 proporciona un marco general de seguridad básica y desempeño esencial. La aplicabilidad concreta puede requerir normas colaterales y particulares según el tipo de equipo, entorno y funciones."),
    ],[claim_specs[3][0],claim_specs[4][0],claim_specs[5][0],claim_specs[16][0]]),
    topic("03","3. Modelos sintéticos de trayectoria e impedancia",[
        sub("03",1,"Ley de Ohm sirve para explorar un modelo, no para declarar seguridad","En una trayectoria resistiva ideal I=V/R permite comprobar dimensiones y sensibilidad a parámetros. La conclusión válida se limita al circuito descrito; no se compara con límites regulatorios recordados ni se extrapola a una persona o equipo real."),
        sub("03",2,"La frecuencia revela trayectorias que un modelo puramente resistivo oculta","Una capacitancia parásita introduce una admitancia dependiente de frecuencia. En el modelo sinusoidal Ic=2πfCV, duplicar frecuencia o capacitancia duplica la corriente calculada, pero los parámetros reales necesitarían medición y geometría documentada."),
        sub("03",3,"Los ejercicios de la unidad son de baja energía y offline","U6-P1/U6-P2/U6-P3 se conservan como escenarios matemáticos históricos. No autorizan construir conexiones, energizar equipos médicos, conectar electrodos ni probar barreras físicas."),
    ],[claim_specs[6][0],claim_specs[7][0]],blocks=[{"id":"BIOINST-U07-T03-B01","type":"equation","latex":"I=V/Z,\\qquad I_c=2\\pi fCV","label":"Modelos lineales sintéticos de trayectoria resistiva/capacitiva; no son límites normativos.","variables":{"I":"corriente modelada","V":"tensión del modelo","Z":"impedancia total modelada","f":"frecuencia","C":"capacitancia de acoplamiento"}}]),
    topic("04","4. Compatibilidad electromagnética como emisiones e inmunidad",[
        sub("04",1,"EMC tiene dos direcciones de evidencia","Un sistema puede perturbar a otros mediante emisiones y también ser vulnerable a perturbaciones externas. La evaluación debe formular qué desempeño se observa, qué entorno se considera y qué perturbación se aplica, en lugar de reducir EMC a 'no ver ruido'."),
        sub("04",2,"Fuente–trayectoria–víctima organiza mecanismos, no los demuestra","Acoplamiento conducido, capacitivo, inductivo o radiado puede producir efectos parecidos en una víctima. Frecuencia, geometría, impedancias y configuración ayudan a construir hipótesis y pruebas discriminantes."),
        sub("04",3,"Una mitigación necesita verificación reproducible","Modificar fuente, trayectoria o susceptibilidad puede reducir una salida del modelo. Para afirmar efectividad se debe medir una variable predefinida antes/después bajo condiciones controladas y conservar incertidumbre, configuración y limitaciones."),
    ],[claim_specs[8][0],claim_specs[9][0],claim_specs[10][0],claim_specs[11][0],claim_specs[12][0]],blocks=[{"id":"BIOINST-U07-T04-B01","type":"equation","latex":"V_{err}=I_s Z_c,\\quad I_c=2\\pi fC_mV_s,\\quad V_i=2\\pi fMI_s","label":"Modelos sintéticos mínimos para explorar acoplamientos conducido, capacitivo e inductivo.","variables":{"Z_c":"impedancia común","C_m":"capacitancia mutua","M":"inductancia mutua","f":"frecuencia"}}]),
    topic("05","5. Fallo simple, controles y cadena de riesgo",[
        sub("05",1,"El fallo debe definirse antes de recalcular","Un análisis de fallo simple cambia una condición concreta respecto del nominal y rastrea su efecto en trayectoria, barrera, salida observable y cadena de riesgo. Introducir múltiples cambios simultáneos dificulta atribuir causalidad."),
        sub("05",2,"Un factor de diez sigue siendo un resultado del modelo","Si una impedancia sintética disminuye diez veces con la misma fuente, la corriente ideal aumenta diez veces. Ese cambio muestra sensibilidad del modelo, pero no etiqueta por sí solo el estado como aceptable, peligroso o conforme."),
        sub("05",3,"Control propuesto y control verificado no son equivalentes","Una mitigación se formula contra un mecanismo y luego necesita evidencia de implementación y efectividad. El expediente debe conservar riesgos residuales, supuestos y lo que todavía no se ha verificado."),
    ],[claim_specs[13][0],claim_specs[14][0],claim_specs[15][0]]),
    topic("06","6. De la evidencia educativa a la conformidad: frontera explícita",[
        sub("06",1,"Una norma aplicable debe identificarse por edición y alcance","El nombre 'IEC 60601' no basta. La edición general, normas colaterales/particulares, entorno de uso, clasificación y requisitos aplicables deben identificarse en un proceso profesional y controlado."),
        sub("06",2,"EMC conforme exige más que un circuito o FFT","IEC 60601-1-2 y la guía FDA tratan EMC mediante requisitos, ensayos, criterios y documentación contextual. Esta unidad solo enseña mecanismos y razonamiento; no ejecuta ensayos de conformidad ni produce un expediente regulatorio."),
        sub("06",3,"La salida correcta es una lista de evidencia faltante","Al finalizar un caso, el estudiante debe separar: resultado matemático, interpretación física, riesgo hipotético, control propuesto y evidencia que aún haría falta. El cierre académico nunca se convierte en autorización de uso con personas."),
    ],[claim_specs[17][0]]),
]

unit["examples"] = [
    {"id":"BIOINST-U07-EJ01","title":"Trayectoria resistiva sintética","scenario":"Modelo abstracto de 5 V RMS y 10 MΩ, sin persona ni dispositivo físico.","reasoning_steps":["Identificar fuente, impedancia y retorno del modelo.","Calcular I=V/R=0.5 µA RMS.","Revisar coherencia dimensional.","Escribir explícitamente que el valor no es un límite normativo ni evidencia de seguridad."],"interpretation":"El cálculo verifica el circuito matemático y permite analizar sensibilidad a R.","limitations":["Solo circuito sintético.","No representa impedancia corporal, fuga real ni criterio de aceptación."]},
    {"id":"BIOINST-U07-EJ02","title":"Trayectoria capacitiva ideal","scenario":"Caso histórico abstracto de C=100 pF, f=50 Hz y V=230 V RMS en una fuente matemática, sin conexión física.","reasoning_steps":["Aplicar Ic=2πfCV.","Obtener aproximadamente 7.23 µA RMS.","Variar f y C para observar sensibilidad.","Negar cualquier comparación con límites regulatorios no proporcionados por una fuente normativa aplicable."],"interpretation":"El ejemplo muestra dependencia con frecuencia y capacitancia, no seguridad de un sistema.","limitations":["Capacitancia ideal concentrada.","No representa un ensayo de fuga ni un equipo energizado."]},
    {"id":"BIOINST-U07-EJ03","title":"Acoplamiento conducido por impedancia común","scenario":"I_interference=2 mA RMS y Z_common=4 Ω en un modelo sintético.","reasoning_steps":["Identificar fuente y trayectoria compartida.","Calcular Verr=8 mV RMS.","Definir una métrica de víctima.","Proponer reducir I o Z y volver a calcular como hipótesis."],"interpretation":"La ecuación muestra cómo una trayectoria común convierte corriente perturbadora en tensión de error.","limitations":["Modelo lineal concentrado; no demuestra mecanismo real ni EMC conforme."]},
    {"id":"BIOINST-U07-EJ04","title":"Acoplamiento inductivo sintético","scenario":"f=1 kHz, M=2 µH e Is=0.1 A RMS en un modelo matemático.","reasoning_steps":["Calcular Vi=2πfMIs≈1.257 mV RMS.","Duplicar separación conceptual reduciendo M como escenario hipotético.","Comparar salida antes/después.","Mantener constante el resto del modelo."],"interpretation":"Una mitigación conceptual cambia el acoplamiento modelado; no es una prueba EMC.","limitations":["M se supone conocida y concentrada."]},
    {"id":"BIOINST-U07-EJ05","title":"Fallo simple de impedancia","scenario":"El modelo nominal 5 V/10 MΩ cambia a 5 V/1 MΩ por un fallo definido.","reasoning_steps":["Calcular 0.5 µA y 5 µA.","Registrar factor 10.","Describir qué barrera/impedancia cambió.","Separar peligro hipotético, situación peligrosa y evidencia faltante."],"interpretation":"El factor 10 cuantifica sensibilidad del modelo; no fija aceptabilidad.","limitations":["No representa un dispositivo o parte aplicada real."]},
    {"id":"BIOINST-U07-EJ06","title":"De simulación EMC a evidencia faltante","scenario":"Una simulación reduce 80% una tensión de error al cambiar un parámetro de acoplamiento.","reasoning_steps":["Confirmar que la métrica y condiciones son comparables.","Describir la mitigación como hipótesis.","Listar ensayo, configuración, criterio, trazabilidad y documentación todavía necesarios.","Evitar la frase 'cumple IEC 60601-1-2'."],"interpretation":"La simulación ayuda a priorizar una estrategia, no a demostrar conformidad.","limitations":["No hay hardware, laboratorio acreditado ni criterio normativo aplicado."]},
]

unit["activities"] = [{
    "id":"BIOINST-U07-ACT01","title":"Expediente sintético de rutas, EMC y fallo simple","purpose":"Integrar las prácticas históricas U6-P1/U6-P2/U6-P3 en un expediente conceptual que separe modelo físico, cadena de riesgo, mitigación y evidencia de conformidad todavía ausente.","prerequisite_unit_ids":["BIOINST-U06"],"estimated_duration_minutes":240,
    "instructions":["Registrar primero el crosswalk `legacy U6 → canonical U7` y conservar U6-P1/U6-P2/U6-P3 como identificadores históricos.","Trabajar únicamente con los parámetros sintéticos ya definidos; no montar circuitos, no energizar equipos médicos y no conectar personas, electrodos o partes aplicadas.","En cada escenario completar una ficha `fuente → trayectoria → retorno/víctima → barrera/control → salida observable → límite de inferencia`.","Usar IEC 60601-1, IEC 60601-1-2, ISO 14971 y FDA solo para alcance/vocabulario/evidencia requerida; no copiar ni inventar límites numéricos regulatorios.","Cerrar con una matriz que separe resultado matemático, riesgo hipotético, control propuesto, evidencia verificada y trabajo profesional todavía pendiente."],
    "tasks":["Reconstruir U6-P1 y calcular el caso 5 V/10 MΩ con unidades; identificar fuente, trayectoria, retorno y barrera conceptual.","Clasificar referencia de señal, tierra de protección y blindaje por función en tres diagramas abstractos sin proponer conexiones físicas.","Analizar el modelo capacitivo 100 pF/50 Hz/230 V como sensibilidad matemática a f y C y declarar por qué no es un ensayo de corriente de fuga.","Con U6-P2, resolver los cuatro mecanismos de acoplamiento y representar fuente, trayectoria, víctima y variable observable para cada uno.","Elegir dos mitigaciones conceptuales distintas —una sobre fuente/trayectoria y otra sobre susceptibilidad— y definir cómo se verificaría su efecto sin afirmar cumplimiento EMC.","Con U6-P3, comparar nominal y fallo simple, cuantificar el factor de cambio y construir la secuencia peligro → situación peligrosa → daño posible → evidencia faltante.","Construir un registro de riesgo educativo con control propuesto, estado de verificación y riesgo residual no evaluado; no asignar aceptabilidad normativa.","Crear una tabla de frontera normativa: qué aporta el modelo, qué exigiría una evaluación IEC/FDA/ISO real y qué requiere revisión profesional antes de cualquier uso con hardware o personas."],
    "deliverables":["Mapa de procedencia legacy U6 → canonical U7 y trazabilidad de U6-P1/U6-P2/U6-P3.","Tres diagramas abstractos de barrera/referencia/tierra/blindaje con funciones, no instrucciones de cableado.","Hoja de cálculos sintéticos resistivo/capacitivo con análisis dimensional y límites explícitos.","Matriz EMC de cuatro mecanismos con fuente, trayectoria, víctima, ecuación, salida y mitigación conceptual.","Registro de fallo simple y cadena de riesgo con control propuesto/evidencia pendiente.","Informe final de 1–2 páginas que diferencie aprendizaje, evidencia técnica, gestión de riesgo y conformidad regulatoria."],
    "checking_criteria":["El crosswalk histórico está explícito y no se renombran U6-P1/U6-P2/U6-P3.","No aparece ninguna instrucción de conexión a personas, electrodos o equipo médico energizado.","Los valores sintéticos se presentan como cálculos del modelo y nunca como límites regulatorios.","Peligro, situación peligrosa, daño y riesgo permanecen diferenciados.","Referencia de señal, tierra de protección y blindaje se explican por función y no como sinónimos.","Cada caso EMC contiene fuente, trayectoria, víctima, frecuencia/configuración y salida observable.","Emisiones e inmunidad se mantienen como dimensiones distintas de EMC.","Toda mitigación se etiqueta como propuesta hasta que exista verificación bajo condiciones definidas.","El fallo simple cuantifica cambio sin etiquetarlo automáticamente como seguro/inseguro o conforme/no conforme.","La conclusión niega explícitamente que la práctica demuestre seguridad, EMC, certificación, conformidad o autorización clínica."],
    "status":"curated_pending_expert_review"
}]
unit["status"].update({"content":"in_review","sources":"traceable","pedagogy":"in_review","multimedia":"planned","internal_review":"pending","external_review":"pending","publication":"published_provisional"})
unit["purpose"] = "Promover legacy U6 como canonical U7 y enseñar razonamiento conceptual sobre trayectorias, barreras, gestión de riesgos y EMC mediante modelos sintéticos offline, preservando la frontera entre aprendizaje, evidencia técnica y conformidad profesional."


def q(i,prompt,los,answer,explain,mis,sids,difficulty="advanced",level="evaluate"):
    return {"id":f"BIOINST-U07-Q{i:02d}","type":"case_analysis","prompt":prompt,"linked_learning_outcome_ids":los,"difficulty":difficulty,"cognitive_level":level,"answer_key":{"expected_answer":answer,"explanation":explain,"common_misconceptions":mis},"feedback":{"correct":"La respuesta distingue modelo, cadena de riesgo, mecanismo EMC y evidencia de conformidad.","incorrect":"Reconstruye fuente, trayectoria/retorno, víctima, barrera y evidencia faltante; no conviertas un cálculo sintético en límite normativo o autorización de uso."},"source_ids":sids,"status":"curated_pending_expert_review"}
assessment["purpose"] = "Evaluar razonamiento sobre barreras, trayectorias, EMC, fallo simple y frontera normativa usando exclusivamente escenarios sintéticos y conservando la revisión humana pendiente."
assessment["student_payload_policy"] = "No se exponen claves completas antes del intento; los juicios de riesgo/conformidad y U6-A5 permanecen sujetos a revisión humana real."
assessment["items"] = [
    q(1,"Un informe ve 12 V en un nodo y concluye 'es peligroso' sin describir nada más. ¿Qué elementos faltan para formular una cadena de riesgo técnicamente defendible?",["BIOINST-U07-LO01"],"Faltan al menos fuente/energía disponible, trayectoria, impedancia, retorno, elemento expuesto, barreras, situación peligrosa, daño posible y contexto de uso. La tensión aislada no determina por sí sola el riesgo.","ISO 14971 obliga a razonar sobre peligros/riesgos y controles como proceso; una magnitud aislada no sustituye la cadena causal.",["voltage-alone-is-risk","hazard-equals-harm"],["iso-14971-2019-current"]),
    q(2,"En un diagrama se unen referencia de señal, tierra de protección y blindaje porque todos usan el símbolo de tierra. Evalúa la decisión sin diseñar una conexión real.",["BIOINST-U07-LO02"],"No es defendible por el símbolo. Debe declararse la función de cada nodo, qué corrientes/información maneja, qué dominio pertenece y qué arquitectura de seguridad/EMC lo justifica. Pueden relacionarse en un diseño concreto, pero no son sinónimos.","Los nombres y símbolos gráficos no sustituyen funciones eléctricas o de protección.",["all-grounds-are-same","shield-is-measurement-reference"],["iec-60601-1-edition-3-2"]),
    q(3,"En el caso sintético 5 V RMS/10 MΩ se obtiene 0.5 µA RMS. Un estudiante afirma que ese valor demuestra que un dispositivo sería seguro. Corrige la conclusión.",["BIOINST-U07-LO03"],"0.5 µA es el resultado del circuito ideal declarado. No demuestra impedancias reales, condiciones de fallo, barreras, métodos de medida, criterios normativos ni conformidad de ningún dispositivo. Solo valida la aritmética del modelo.","Un cálculo físico puede ser correcto y la inferencia de seguridad seguir siendo inválida.",["calculated-current-is-safety-limit","simulation-is-conformity"],["iec-60601-1-edition-3-2","iso-14971-2019-current"]),
    q(4,"Una víctima muestra 8 mV RMS cuando circulan 2 mA por una impedancia común de 4 Ω. Clasifica el mecanismo y propone una prueba conceptual que discrimine la hipótesis.",["BIOINST-U07-LO04"],"Es compatible con acoplamiento conducido por impedancia común: Verr=I·Z. Una prueba conceptual es variar de forma controlada I o Z en el modelo y comprobar si Verr escala según la relación, manteniendo el resto fijo. No demuestra que ese sea el mecanismo de un equipo real.","La ecuación genera una predicción que puede contrastarse, pero no identifica automáticamente la causa observada.",["equation-proves-mechanism","all-emc-is-radiated"],["fda-emc-overview-2026","iec-60601-1-2-edition-4-1"]),
    q(5,"Una simulación reduce 80% la tensión de error al disminuir la capacitancia mutua. El informe escribe 'cumple IEC 60601-1-2'. ¿Qué debe decir en su lugar?",["BIOINST-U07-LO04","BIOINST-U07-LO05"],"Debe decir que el modelo predice una reducción de la métrica bajo parámetros/condiciones sintéticas y que la mitigación es una hipótesis. La conformidad requeriría normas aplicables, ensayo, criterios, configuración, trazabilidad y documentación apropiados.","IEC 60601-1-2 trata requisitos/ensayos de EMC; una simulación conceptual no equivale a esos ensayos.",["simulation-proves-emc","relative-improvement-is-compliance"],["iec-60601-1-2-edition-4-1","fda-emc-guidance-2022"]),
    q(6,"El modelo nominal 5 V/10 MΩ pasa por un fallo a 5 V/1 MΩ. Se obtiene un incremento 10×. ¿Qué puede y qué no puede concluirse?",["BIOINST-U07-LO03","BIOINST-U07-LO05"],"Puede concluirse que, bajo el modelo resistivo, la corriente aumenta de 0.5 a 5 µA y que la salida es diez veces más sensible al cambio de impedancia. No puede concluirse aceptabilidad, seguridad, cumplimiento o severidad clínica sin el proceso/evidencia correspondiente.","El factor relativo pertenece al modelo; la evaluación de riesgo y conformidad requiere contexto adicional.",["tenfold-means-unsafe","single-fault-calculation-is-certification"],["iso-14971-2019-current","iec-60601-1-edition-3-2"]),
    q(7,"Un equipo propone un blindaje y marca el riesgo como 'cerrado' antes de medir ningún resultado. ¿Cómo debe registrarse el estado?",["BIOINST-U07-LO02","BIOINST-U07-LO04","BIOINST-U07-LO05"],"Como control propuesto/no verificado. Debe existir una métrica de víctima, condiciones reproducibles y evidencia antes/después; después se evalúan efectividad y riesgo residual dentro del proceso aplicable.","Proponer una mitigación no demuestra su implementación ni efectividad.",["proposed-control-equals-verified","shield-always-solves-emc"],["iso-14971-2019-current","fda-emc-guidance-2022"]),
    q(8,"Tras completar U7, alguien quiere conectar el circuito a una persona para 'validar lo aprendido'. Redacta la respuesta técnicamente correcta y el siguiente paso académico permitido.",["BIOINST-U07-LO01","BIOINST-U07-LO02","BIOINST-U07-LO03","BIOINST-U07-LO04","BIOINST-U07-LO05"],"No está autorizado: U7 es sintética/offline y no demuestra seguridad ni conformidad. El siguiente paso académico permitido es ampliar el expediente documental, revisar requisitos aplicables y preparar preguntas/evidencia para revisión profesional, sin conectar personas ni equipo médico energizado.","La finalización del contenido educativo no cambia el alcance de seguridad ni sustituye revisión profesional.",["course-completion-authorizes-human-test","offline-model-validates-hardware"],["iec-60601-1-edition-3-2","iec-60601-1-2-edition-4-1","iso-14971-2019-current"]),
]
assessment["status"] = "curated_pending_expert_review"

term_specs = [
("Peligro","Fuente potencial de daño; debe distinguirse de la situación peligrosa, del daño y del riesgo.",["iso-14971-2019-current"]),
("Situación peligrosa","Circunstancia en la que personas, propiedad o entorno quedan expuestos a uno o más peligros; se usa aquí como capa causal, no como sinónimo de daño.",["iso-14971-2019-current"]),
("Daño","Consecuencia adversa posible dentro de una cadena de riesgo; no se infiere solo a partir de una magnitud eléctrica.",["iso-14971-2019-current"]),
("Riesgo","Combinación evaluada dentro de un proceso de gestión de riesgos; la norma no fija un nivel universal aceptable para todos los dispositivos.",["iso-14971-2019-current"]),
("Barrera de aislamiento","Elemento o conjunto conceptual que separa dominios y limita transferencia no deseada de energía; su dibujo no demuestra desempeño o conformidad.",["iec-60601-1-edition-3-2"]),
("Referencia de señal","Nodo o potencial de referencia usado para expresar una señal o medición; no debe confundirse automáticamente con tierra de protección.",["iec-60601-1-edition-3-2"]),
("Tierra de protección","Función de protección dentro de una arquitectura eléctrica; no es sinónimo universal de referencia de señal o blindaje.",["iec-60601-1-edition-3-2"]),
("Blindaje","Elemento destinado a controlar acoplamiento electromagnético; su función y conexión dependen de la arquitectura y no lo convierten automáticamente en referencia de medida.",["fda-emc-overview-2026"]),
("EMC","Compatibilidad electromagnética: capacidad de coexistir en un entorno electromagnético controlando emisiones y manteniendo desempeño frente a perturbaciones.",["fda-emc-overview-2026","iec-60601-1-2-edition-4-1"]),
("Emisiones electromagnéticas","Perturbaciones electromagnéticas emitidas por un equipo o sistema y relevantes para su coexistencia con otros equipos.",["iec-60601-1-2-edition-4-1"]),
("Inmunidad electromagnética","Capacidad evaluada de mantener el desempeño requerido en presencia de perturbaciones electromagnéticas definidas.",["iec-60601-1-2-edition-4-1"]),
("Acoplamiento conducido","Transferencia de perturbación a través de una trayectoria conductora o impedancia compartida en el modelo.",["fda-emc-overview-2026"]),
("Acoplamiento capacitivo","Transferencia modelada mediante un campo eléctrico/capacitancia mutua dependiente de frecuencia y geometría.",["fda-emc-overview-2026"]),
("Acoplamiento inductivo","Transferencia modelada mediante campo magnético/inductancia mutua dependiente de frecuencia, corriente y geometría.",["fda-emc-overview-2026"]),
("Acoplamiento radiado","Transferencia electromagnética sin una trayectoria conductora directa, representada aquí solo mediante un modelo abstracto de acoplamiento.",["fda-emc-overview-2026"]),
("Fallo simple","Alteración única y definida usada para comparar el estado nominal y explorar cambios de la cadena de riesgo; no equivale por sí sola a un ensayo normativo completo.",["iso-14971-2019-current","iec-60601-1-edition-3-2"]),
("Control de riesgo","Medida destinada a reducir un riesgo y cuya implementación/efectividad deben documentarse antes de considerarla verificada.",["iso-14971-2019-current"]),
("Conformidad","Demostración frente a requisitos aplicables mediante evidencia y proceso apropiados; una simulación educativa no constituye una declaración de conformidad.",["fda-emc-guidance-2022","iec-60601-1-2-edition-4-1"]),
]
locators = {
"iso-14971-2019-current":"ISO official page; current 2019 edition confirmed 2025",
"iec-60601-1-edition-3-2":"IEC Webstore consolidated edition 3.2 scope",
"iec-60601-1-2-edition-4-1":"IEC Webstore consolidated edition 4.1 scope",
"fda-emc-guidance-2022":"FDA Final Guidance, June 2022",
"fda-emc-overview-2026":"FDA Electromagnetic Compatibility overview, accessed 2026-08-24",
}
entries = glossary["entries"]
max_id = max([int(m.group(1)) for e in entries if (m := re.search(r"(\d+)$", e["id"]))] or [0])
selected=[]
for term, definition, sids in term_specs:
    entry = next((e for e in entries if e["term"].strip().casefold() == term.casefold()), None)
    if entry is None:
        max_id += 1
        entry={"id":f"BIOINST-GLO-{max_id:03d}","term":term}
        entries.append(entry)
    entry.update({"definition":definition,"unit_ids":sorted(set(entry.get("unit_ids",[]))|{"BIOINST-U07"}),"source_ids":sids,"verification_status":"verified_directly" if len(sids)==1 else "verified_contextually","source_locators":[{"source_id":sid,"locator":locators[sid]} for sid in sids]})
    selected.append(entry["id"])
unit["glossary_entry_ids"] = selected

claims["claims"] = [c for c in claims["claims"] if c.get("unit_id") != "BIOINST-U07"]
new_claims=[]
for i,(text,sid,locator,ctype,risk,support) in enumerate(claim_specs,1):
    cid=f"BIOINST-U07-C{i:03d}"
    new_claims.append({"claim_id":cid,"unit":7,"text":text,"claim_type":ctype,"risk":risk,"context":"Aplicado a modelos educativos sintéticos/offline de seguridad eléctrica y EMC; no autoriza trabajo con personas, equipo energizado, límites normativos ni afirmaciones de conformidad.","source_id":sid,"locator":{"section":locator},"support":support,"source_verification_status":"verified_directly","review_state":"ai_review_provisional","reviewer_validation_id":None,"reviewed_at":"2026-08-24","id":cid,"unit_id":"BIOINST-U07"})
claims["claims"].extend(new_claims)
claims["scope"] = "Afirmaciones centrales de Bioinstrumentación con fuente y localizador; Unidades 1–7 integradas y revisión disciplinaria humana pendiente."
claims["review_state"] = "ai_review_provisional"
unit["claim_ids"] = [c["id"] for c in new_claims]
unit["source_ids"] = ["iec-60601-1-edition-3-2","iec-60601-1-2-edition-4-1","iso-14971-2019-current","fda-emc-guidance-2022","fda-emc-overview-2026"]
for sid in unit["source_ids"]:
    src=next((s for s in sources["sources"] if s["id"] == sid),None)
    assert src is not None, sid
    src["used_by_unit_ids"] = sorted(set(src.get("used_by_unit_ids",[]))|{"BIOINST-U07"})

dump(unit_path,unit)
dump(assessment_path,assessment)
dump(glossary_path,glossary)
dump(sources_path,sources)
dump(claims_path,claims)
print("Curated canonical Bioinstrumentation U7 from preserved legacy U6 provenance")
