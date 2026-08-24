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

unit_path = COURSE / "units" / "unit-09.json"
assessment_path = COURSE / "assessments" / "unit-09.json"
glossary_path = COURSE / "glossary.json"
sources_path = COURSE / "sources.json"
claims_path = COURSE / "claims.json"
unit, assessment, glossary, sources, claims = map(load, [unit_path, assessment_path, glossary_path, sources_path, claims_path])
migration = load(ROOT / "data/course_migrations/bioinstrumentacion-numbering-v1.json")
row = next(x for x in migration["canonical_sequence"] if x["canonical_unit"] == 9)
assert row["origin"] == "new" and row["action"] == "author"
assert not (ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-09.json").exists()


def upsert_source(record: dict) -> None:
    old = next((x for x in sources["sources"] if x["id"] == record["id"]), None)
    if old is None:
        sources["sources"].append(record)
    else:
        used = sorted(set(old.get("used_by_unit_ids", [])) | set(record.get("used_by_unit_ids", [])))
        old.update(record)
        old["used_by_unit_ids"] = used

source_records = [
    {"id":"nasa-se-handbook-vv-2016","title":"NASA Systems Engineering Handbook, Rev 2 — Product Verification and Product Validation","organization":"NASA","url":"https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf","type":"manual público de ingeniería de sistemas","verification_status":"verified_directly","locator":"Sections 2.4, 5.3 and 5.4; verification against requirements and validation against stakeholder expectations/intended environment","curricular_function":"Separar verificación de producto, validación e intención/entorno de uso y documentar discrepancias.","coverage":[9,10],"limitations":"Marco de ingeniería de sistemas, no regulación de dispositivos médicos.","used_by_unit_ids":["BIOINST-U09"]},
    {"id":"nasa-requirements-traceability","title":"NASA Software Engineering Handbook SWE-047 — Traceability Data","organization":"NASA","url":"https://swehb.nasa.gov/spaces/7150/pages/16449982/SWE-047%2B-%2BTraceability%2BData","type":"guía pública de ingeniería","verification_status":"verified_directly","locator":"Rationale: preferred bidirectional traceability and detection of missing/orphan requirements","curricular_function":"Sustentar trazabilidad bidireccional y auditoría de relaciones faltantes.","coverage":[9,10],"limitations":"Contexto NASA/software; se usa como principio general de trazabilidad.","used_by_unit_ids":["BIOINST-U09"]},
    {"id":"nasa-requirements-appendix","title":"NASA Systems Engineering Handbook Appendix C/D/E — Requirements, verification and validation matrices","organization":"NASA","url":"https://www.nasa.gov/reference/system-engineering-handbook-appendix/","type":"guía pública de ingeniería","verification_status":"verified_directly","locator":"Appendix C How to Write a Good Requirement; Appendix D Requirements Verification Matrix; Appendix E Validation Requirements Matrix","curricular_function":"Guiar requisitos no ambiguos, verificables y matrices de V&V.","coverage":[9,10],"limitations":"No define requisitos regulatorios biomédicos específicos.","used_by_unit_ids":["BIOINST-U09"]},
    {"id":"fda-qmsr-2026","title":"FDA Quality Management System Regulation (QMSR)","organization":"U.S. Food and Drug Administration","url":"https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr","type":"página regulatoria oficial","verification_status":"verified_directly","locator":"Updated 2026-02-02; QMSR effective 2026-02-02, incorporates ISO 13485:2016; design and development under 21 CFR 820.10(c)/ISO 13485 clause 7","curricular_function":"Mantener actualizada la frontera regulatoria de calidad/diseño en EE. UU.","coverage":[9,10],"limitations":"No se usa para afirmar conformidad del curso ni para reproducir texto normativo de ISO 13485.","used_by_unit_ids":["BIOINST-U09"]},
    {"id":"fda-qmsr-risk-design-2026","title":"FDA Town Hall — QMSR: Risk and Design and Development","organization":"U.S. Food and Drug Administration","url":"https://www.fda.gov/medical-devices/medical-devices-news-and-events/town-hall-quality-management-system-regulation-risk-and-design-and-development-01142026","type":"material regulatorio/educativo oficial","verification_status":"verified_directly","locator":"2026-01-14 summary: QMSR risk management, risk-based decisions, design and development","curricular_function":"Contextualizar la relación vigente entre gestión de riesgos, decisiones basadas en riesgo y desarrollo de dispositivos.","coverage":[9],"limitations":"Resumen educativo; requisitos jurídicos se consultan en las fuentes regulatorias aplicables.","used_by_unit_ids":["BIOINST-U09"]},
    {"id":"fda-human-factors-2026","title":"Applying Human Factors and Usability Engineering to Medical Devices","organization":"U.S. Food and Drug Administration","url":"https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices","type":"guía FDA vigente","verification_status":"verified_directly","locator":"Final Guidance, August 2026; intended users, uses and use environments; use-related risk","curricular_function":"Sustentar que la evidencia de uso necesita usuarios, tareas, interfaz y entornos representativos.","coverage":[9],"limitations":"Guía no vinculante; no sustituye requisitos regulatorios aplicables ni demuestra validación clínica.","used_by_unit_ids":["BIOINST-U09"]},
    {"id":"fda-human-factors-content-2026","title":"Content of Human Factors Information in Medical Device Marketing Submissions","organization":"U.S. Food and Drug Administration","url":"https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-human-factors-information-medical-device-marketing-submissions","type":"guía FDA vigente","verification_status":"verified_directly","locator":"Final Guidance, May 2026; risk-based framework for human factors information","curricular_function":"Distinguir evidencia técnica del expediente de factores humanos y su justificación basada en riesgo.","coverage":[9],"limitations":"No se usa para simular una presentación regulatoria ni aprobación de mercado.","used_by_unit_ids":["BIOINST-U09"]},
]
for r in source_records: upsert_source(r)
# Refresh the already existing risk source with current status.
upsert_source({"id":"iso-14971-2019-current","title":"ISO 14971:2019 — Medical devices — Application of risk management to medical devices","organization":"International Organization for Standardization","url":"https://www.iso.org/standard/72704.html","type":"norma internacional — metadatos/alcance oficial","verification_status":"verified_directly","locator":"ISO official page: Edition 3 (2019), confirmed 2025, current; overview of hazard identification, risk estimation/evaluation, control and life-cycle monitoring","curricular_function":"Sustentar el proceso general de gestión de riesgos sin reproducir requisitos de pago ni declarar conformidad.","coverage":[7,9],"limitations":"La página pública da alcance y estado, no sustituye el texto completo de la norma ni revisión profesional.","used_by_unit_ids":["BIOINST-U07","BIOINST-U09"]})
sources["consulted_on"] = "2026-08-24"

claim_specs = [
("Una necesidad de usuario describe el problema, expectativa o resultado buscado; debe convertirse en requisitos suficientemente claros y verificables antes de diseñar pruebas de aceptación.","nasa-requirements-appendix","Appendix C: How to Write a Good Requirement","methodological_requirement","medium","direct"),
("El uso previsto debe declarar al menos propósito, usuarios relevantes, tareas y entorno suficientes para delimitar qué evidencia de validación es pertinente.","fda-human-factors-2026","August 2026 guidance: intended users, uses and use environments","methodological_requirement","high","direct"),
("Un requisito útil para verificación identifica la función o propiedad, las condiciones y un criterio observable sin esconder una solución de diseño innecesaria.","nasa-requirements-appendix","Appendix C requirement quality/checklists","methodological_requirement","medium","direct"),
("La trazabilidad bidireccional permite recorrer la evidencia hacia adelante y hacia atrás y ayuda a detectar requisitos perdidos o funciones sin una necesidad documentada.","nasa-requirements-traceability","SWE-047 rationale","methodological_requirement","medium","direct"),
("La verificación de producto aporta evidencia de cumplimiento con requisitos aprobados y puede utilizar pruebas, análisis, inspecciones o demostraciones apropiadas al requisito.","nasa-se-handbook-vv-2016","Sections 2.4 and 5.3","definition","medium","direct"),
("Un resultado fuera de criterio no desaparece porque otra prueba pase; debe conservarse como discrepancia hasta que exista resolución y evidencia trazables.","nasa-se-handbook-vv-2016","Section 5.3 criteria include closure of discrepancy/nonconformance reports","methodological_requirement","medium","direct"),
("La validación de producto evalúa si el producto cumple su propósito y expectativas de las partes interesadas en el entorno previsto, no solo si satisface cada requisito técnico aislado.","nasa-se-handbook-vv-2016","Sections 2.4 and 5.4","definition","high","direct"),
("Una simulación puede contribuir a verificación o validación, pero el alcance de la conclusión depende de la fidelidad del modelo, la cobertura de escenarios y la correspondencia con el uso que se pretende representar.","nasa-se-handbook-vv-2016","Sections 2.4, 5.3 and 5.4 on methods and realistic/simulated conditions","interpretation_boundary","medium","indirect"),
("En dispositivos médicos, la evidencia de factores humanos debe considerar la interacción entre usuarios previstos, entornos de uso e interfaz porque esos elementos pueden modificar los riesgos relacionados con el uso.","fda-human-factors-2026","August 2026 guidance and FDA human-factors framework","methodological_requirement","high","direct"),
("ISO 14971:2019 sigue siendo la edición vigente confirmada en 2025 y establece un proceso de ciclo de vida para identificar peligros, estimar y evaluar riesgos, controlarlos y vigilar la efectividad de los controles.","iso-14971-2019-current","ISO official page, current edition confirmed 2025","regulatory_context","high","direct"),
("Una cadena de riesgo útil separa peligro, secuencia de eventos, situación peligrosa y daño para evitar tratar un fallo o una anomalía como si fuera automáticamente el daño final.","iso-14971-2019-current","ISO 14971 risk-management terminology/process context; educational causal decomposition","methodological_requirement","high","indirect"),
("Un control de riesgo no se da por efectivo porque esté escrito en una matriz: necesita evidencia de implementación y una prueba o análisis que demuestre el efecto previsto dentro del alcance declarado.","iso-14971-2019-current","ISO overview: risk control and monitoring effectiveness","methodological_requirement","high","indirect"),
("Los controles pueden introducir nuevas interacciones o riesgos y por eso deben reevaluarse dentro del sistema y no únicamente como componentes aislados.","fda-human-factors-2026","Use-related risk and user-interface interactions","risk_principle","high","indirect"),
("El riesgo residual se documenta después de aplicar controles; una actividad educativa puede describirlo, pero no autoriza por sí sola una decisión profesional de aceptabilidad.","iso-14971-2019-current","ISO risk-management lifecycle/benefit-risk context","interpretation_boundary","high","indirect"),
("La cobertura de V&V debe auditar relaciones faltantes: necesidades sin requisitos, requisitos sin evidencia, riesgos sin controles y controles sin verificación son brechas diferentes.","nasa-requirements-traceability","SWE-047 bidirectional traceability rationale","methodological_requirement","medium","direct"),
("Cambiar el criterio después de observar un resultado fuera de especificación no constituye cierre de una discrepancia; cambia la pregunta y debe gestionarse como un cambio controlado.","jcgm-106-2012","Pre-established decision-rule principle; applied as methodological boundary","decision_principle","medium","indirect"),
("Desde el 2 de febrero de 2026 la FDA aplica la QMSR, que incorpora ISO 13485:2016 por referencia y mantiene requisitos de diseño y desarrollo para los fabricantes a los que aplica.","fda-qmsr-2026","FDA QMSR updated/effective 2026-02-02","regulatory_context","high","direct"),
("Cumplir una matriz educativa de requisitos, riesgos y pruebas no equivale a demostrar cumplimiento de QMSR, ISO 13485, ISO 14971, seguridad clínica ni autorización de comercialización.","fda-qmsr-2026","QMSR applicability and regulatory scope","interpretation_boundary","high","direct"),
]


def para(tid, sid, title, text):
    return {"id":f"BIOINST-U09-T{tid}-ST{sid:02d}","title":title,"blocks":[{"id":f"BIOINST-U09-T{tid}-ST{sid:02d}-B01","type":"paragraph","text":text}]}

def topic(tid,title,subs,points):
    return {"id":f"BIOINST-U09-T{tid}","title":title,"blocks":[],"key_points":points,"subtopics":subs}

unit["status"]={"content":"in_review","sources":"traceable","pedagogy":"in_review","multimedia":"planned","internal_review":"pending","external_review":"pending","publication":"published_provisional"}
unit["purpose"]="Conectar necesidades, uso previsto, requisitos, riesgos, controles y evidencia mediante trazabilidad bidireccional, diferenciando verificación técnica, validación del uso y evidencia clínica, y cerrando solo conclusiones justificadas por el alcance disponible."
unit["topics"]=[
    topic("01","1. Necesidad, uso previsto y requisito verificable",[
        para("01",1,"De la necesidad a una afirmación comprobable",claim_specs[0][0]+" La necesidad conserva el porqué; el requisito define qué comportamiento o propiedad debe poder evaluarse."),
        para("01",2,"El uso previsto delimita la validación",claim_specs[1][0]+" Cambiar usuario, tarea, población o entorno puede cambiar tanto el requisito pertinente como el riesgo y la evidencia necesaria."),
        para("01",3,"Un requisito no debe esconder una solución sin justificación",claim_specs[2][0]+" Debe poder leerse de forma consistente por quien diseña, quien prueba y quien revisa la evidencia."),
    ],[claim_specs[0][0],claim_specs[1][0],claim_specs[2][0]]),
    topic("02","2. Trazabilidad y verificación",[
        para("02",1,"La trazabilidad es una red de razones y evidencia",claim_specs[3][0]+" Una matriz útil conserva identificadores estables y enlaces explícitos, no solo una lista de documentos."),
        para("02",2,"Verificar significa demostrar cumplimiento con requisitos",claim_specs[4][0]+" El método se elige según la propiedad: una inspección puede bastar para una etiqueta, mientras latencia o exactitud requieren evidencia cuantitativa."),
        para("02",3,"Las discrepancias son evidencia, no basura",claim_specs[5][0]+" Deben registrar configuración, condición, resultado, impacto, disposición, responsable y estado para que el expediente pueda auditarse."),
    ],[claim_specs[3][0],claim_specs[4][0],claim_specs[5][0]]),
    topic("03","3. Validación y representatividad del uso",[
        para("03",1,"Validar no es repetir la verificación",claim_specs[6][0]+" Un sistema puede cumplir su especificación y aun así no resolver la necesidad correcta o no funcionar adecuadamente en el contexto de uso."),
        para("03",2,"La simulación necesita una frontera de inferencia",claim_specs[7][0]+" La simulación debe declarar qué comportamiento representa, qué no modela y por qué los casos cubren —o no— el espacio de uso previsto."),
        para("03",3,"Usuarios y entorno cambian la evidencia",claim_specs[8][0]+" Una interfaz evaluada solo por desarrolladores no sustituye evidencia con usuarios representativos cuando el riesgo depende de percepción, decisión o manipulación."),
    ],[claim_specs[6][0],claim_specs[7][0],claim_specs[8][0]]),
    topic("04","4. Riesgo, controles y evidencia",[
        para("04",1,"El riesgo se gestiona a lo largo del ciclo de vida",claim_specs[9][0]+" El expediente debe poder actualizarse cuando aparece nueva evidencia de producción, uso o cambios del sistema."),
        para("04",2,"Separar la cadena causal evita saltos",claim_specs[10][0]+" Esta descomposición permite ubicar controles en más de un punto y distinguir prevención, detección, protección e información."),
        para("04",3,"Todo control requiere evidencia y reevaluación",claim_specs[11][0]+" "+claim_specs[12][0]),
    ],[claim_specs[9][0],claim_specs[10][0],claim_specs[11][0]]),
    topic("05","5. Riesgo residual, cobertura y discrepancias",[
        para("05",1,"Residual no significa automáticamente aceptable",claim_specs[13][0]+" El curso conserva la diferencia entre describir el riesgo restante y autorizar una decisión regulatoria o clínica."),
        para("05",2,"Cobertura es más que porcentaje de pruebas ejecutadas",claim_specs[14][0]+" También deben buscarse evidencias huérfanas y relaciones que no justifican una decisión."),
        para("05",3,"Los criterios no se reescriben para hacer pasar el resultado",claim_specs[15][0]+" Si cambia legítimamente un requisito, se registra la razón, se analiza impacto y se reevalúa la evidencia afectada."),
    ],[claim_specs[13][0],claim_specs[14][0],claim_specs[15][0]]),
    topic("06","6. Aptitud limitada y frontera regulatoria",[
        para("06",1,"El marco regulatorio también cambia",claim_specs[16][0]+" Por eso una unidad académica debe fechar la fuente normativa y evitar presentar documentos obsoletos como requisitos vigentes."),
        para("06",2,"La conclusión debe conservar configuración y alcance","Una conclusión de aptitud solo es defendible para la configuración, requisitos, usuarios, entorno y evidencia efectivamente evaluados. Extenderla a otra población, versión, interfaz o entorno exige analizar qué relaciones y riesgos cambian."),
        para("06",3,"La práctica no es una aprobación",claim_specs[17][0]+" La salida correcta de U9 es un expediente educativo con brechas explícitas y preguntas de revisión, no una etiqueta de 'aprobado para uso clínico'."),
    ],[claim_specs[16][0],"Una conclusión de aptitud solo es defendible para la configuración, requisitos, usuarios, entorno y evidencia efectivamente evaluados.",claim_specs[17][0]]),
]

unit["examples"]=[
    {"id":"BIOINST-U09-EJ01","title":"Necesidad ambigua convertida en requisito","scenario":"Necesidad: «la alarma debe avisar rápido». Se propone verificar una alarma sintética.","reasoning_steps":["Definir evento que inicia el cronómetro.","Definir evento que lo termina y la configuración.","Especificar distribución de casos y criterio, por ejemplo percentil/umbral.","Separar latencia técnica de utilidad de la alarma."],"interpretation":"El requisito verificable puede evaluarse en banco; la necesidad completa requiere validación del uso.","limitations":["No determina umbrales clínicos ni seguridad de una alarma real."]},
    {"id":"BIOINST-U09-EJ02","title":"Prueba huérfana","scenario":"Existe una prueba de «modo nocturno» que pasa, pero no hay necesidad ni requisito que justifique esa función.","reasoning_steps":["Buscar trazabilidad hacia requisito y necesidad.","Clasificar la prueba como evidencia huérfana.","Investigar si falta documentación o existe funcionalidad no autorizada.","Resolver mediante requisito justificado o retirada/control de la función."],"interpretation":"Que una prueba pase no demuestra que la función deba existir.","limitations":["Caso educativo de configuración."]},
    {"id":"BIOINST-U09-EJ03","title":"Verificación aprobada, validación insuficiente","scenario":"Un algoritmo cumple latencia y exactitud sintéticas, pero solo fue evaluado por desarrolladores en escritorio.","reasoning_steps":["Separar requisitos técnicos ya verificados.","Definir usuarios/tareas/entorno del uso previsto.","Identificar riesgos relacionados con interfaz y errores de uso.","Listar evidencia de validación todavía necesaria."],"interpretation":"El éxito técnico no basta para una conclusión amplia de uso.","limitations":["No diseña un estudio clínico real ni autoriza exposición humana."]},
    {"id":"BIOINST-U09-EJ04","title":"Cadena de riesgo por dato faltante","scenario":"Se pierde un paquete y la interfaz interpola sin marcar el dato como derivado.","reasoning_steps":["Peligro: información incorrecta/no identificada.","Secuencia: pérdida → interpolación silenciosa → visualización plausible.","Situación peligrosa: usuario confía en un dato no observado.","Control: detección de secuencia + marca de calidad + prueba de fallo."],"interpretation":"El fallo de transporte no es el daño; la cadena explica cómo podría habilitar una decisión incorrecta.","limitations":["No estima probabilidad clínica."]},
    {"id":"BIOINST-U09-EJ05","title":"Control que introduce una nueva latencia","scenario":"Un filtro de confirmación reduce falsas alarmas sintéticas pero añade 3 s de retraso.","reasoning_steps":["Documentar el riesgo que motivó el filtro.","Verificar reducción del evento objetivo.","Identificar latencia como efecto nuevo.","Reevaluar requisito temporal y cadena de riesgo."],"interpretation":"Un control puede reducir un riesgo y crear otro modo de fallo que debe analizarse.","limitations":["Valores sintéticos; no implica aceptabilidad clínica."]},
    {"id":"BIOINST-U09-EJ06","title":"Discrepancia que no se cierra cambiando el criterio","scenario":"Requisito bloqueado: latencia ≤2 s. El resultado es 2.4 s y se propone editar el requisito a ≤3 s sin análisis.","reasoning_steps":["Registrar la discrepancia contra el requisito vigente.","Investigar causa e impacto.","Si se propone cambiar el requisito, justificar la necesidad y analizar impacto en uso/riesgo.","Repetir evidencia afectada antes de cerrar."],"interpretation":"Modificar retrospectivamente el criterio no convierte el resultado original en evidencia conforme.","limitations":["Ejemplo de control de cambios, no disposición regulatoria real."]},
]

unit["activities"]=[{"id":"BIOINST-U09-ACT01","title":"Expediente necesidad–requisito–riesgo–V&V","purpose":"Construir sobre un sistema biomédico sintético una matriz trazable que distinga verificación, validación, riesgo, controles y discrepancias sin afirmar aprobación clínica o regulatoria.","prerequisite_unit_ids":["BIOINST-U08"],"estimated_duration_minutes":240,"instructions":["Definir y bloquear un uso previsto educativo con propósito, usuarios simulados, tareas, entorno, configuración y exclusiones antes de redactar pruebas.","Redactar cinco necesidades y convertirlas en requisitos identificables, medibles y verificables; conservar el enlace necesidad↔requisito.","Construir al menos cuatro cadenas de riesgo separando peligro, secuencia de eventos, situación peligrosa, daño posible, control y riesgo residual descriptivo.","Diseñar evidencia de verificación para cada requisito/control y un plan de validación conceptual que identifique qué usuarios, tareas y entorno tendrían que ser representativos; no ejecutar estudios con personas.","Registrar toda discrepancia sin eliminarla ni cambiar criterios retrospectivamente y cerrar con una matriz de evidencia disponible, brechas y conclusión limitada."],"tasks":["Corregir tres requisitos ambiguos y explicar por qué cada redacción original no era verificable.","Construir una matriz bidireccional de cinco necesidades, al menos ocho requisitos y sus métodos/criterios de verificación.","Clasificar ocho evidencias propuestas como verificación, validación conceptual, ambas con alcance limitado o evidencia insuficiente.","Construir cuatro cadenas completas `peligro → secuencia → situación peligrosa → daño posible → control → evidencia del control`.","Introducir dos fallos sintéticos y comprobar que los controles detectan/reducen el mecanismo previsto sin asumir que el riesgo residual es aceptable.","Auditar factores humanos: listar usuarios, tareas críticas, interfaz y condiciones ambientales que una futura validación representativa tendría que cubrir.","Resolver tres discrepancias sintéticas mediante corrección/reprueba o cambio controlado con análisis de impacto; prohibido borrar resultados o mover criterios para hacerlos pasar.","Ejecutar una auditoría de cobertura buscando necesidades sin requisitos, requisitos sin evidencia, pruebas huérfanas, riesgos sin controles, controles sin prueba y cambios sin reevaluación."],"deliverables":["Ficha de uso previsto educativo y configuración bloqueada.","Matriz bidireccional necesidad–requisito–prueba con criterios de aceptación.","Registro de cuatro cadenas de riesgo y controles con evidencia asociada.","Plan conceptual de validación de uso con usuarios/tareas/entornos representativos, explícitamente no ejecutado.","Registro de discrepancias y cambios con estado, impacto y re-prueba.","Informe final de 2–3 páginas con cobertura, riesgo residual descriptivo, brechas y afirmaciones no permitidas."],"checking_criteria":["El uso previsto está delimitado antes de diseñar la evidencia.","Cada requisito es identificable, no ambiguo y verificable con condición y criterio.","La trazabilidad funciona necesidad→requisito→evidencia y en sentido inverso.","Verificación y validación se distinguen por la pregunta que responden, no solo por el tipo de prueba.","Usuarios, tareas, entorno e interfaz se incluyen en la frontera de una futura validación de uso.","Cada cadena separa peligro, eventos, situación peligrosa y daño posible.","Cada control tiene requisito/evidencia y se revisa por riesgos o efectos introducidos.","El riesgo residual se describe sin declarar aceptabilidad profesional.","Las discrepancias permanecen trazables y los criterios no se cambian retrospectivamente para cerrar fallos.","La conclusión niega que el expediente educativo demuestre QMSR/ISO 13485/ISO 14971, seguridad clínica o autorización de comercialización."],"status":"curated_pending_expert_review"}]

assessment["purpose"]="Evaluar traducción de necesidades a requisitos, trazabilidad, V&V, riesgo, controles y discrepancias mediante casos que obligan a limitar la conclusión al alcance de la evidencia."
assessment["student_payload_policy"]="Las claves y explicaciones se excluyen del payload inicial; no se simula juicio regulatorio, clínico o revisión profesional humana."
items=[
("Q01","Necesidad: «el monitor debe responder rápido». El equipo propone como requisito «usar un microcontrolador de 200 MHz». Evalúa y reescribe el enfoque.",["BIOINST-U09-LO01"],"La necesidad debe traducirse a una propiedad observable —por ejemplo latencia entre eventos definidos bajo condiciones y distribución de casos declaradas— con criterio de aceptación. Imponer un microcontrolador es una solución de diseño salvo que exista una restricción justificada.","Un requisito verificable expresa qué debe cumplirse y bajo qué condiciones, sin prescribir implementación innecesaria.",["solution-equals-requirement","fast-without-metric-is-testable"],["nasa-requirements-appendix"]),
("Q02","Una prueba pasa y demuestra latencia ≤2 s, pero no existe enlace a ninguna necesidad o requisito. ¿Es evidencia suficiente?",["BIOINST-U09-LO01","BIOINST-U09-LO05"],"No. Es una prueba huérfana hasta justificar qué requisito evalúa y por qué ese requisito deriva del uso/necesidad. Puede revelar documentación faltante o funcionalidad no justificada.","La trazabilidad bidireccional detecta tanto requisitos perdidos como funciones/evidencias sin razón de origen.",["passing-test-proves-need","traceability-only-forward"],["nasa-requirements-traceability"]),
("Q03","Todos los requisitos técnicos pasan en simulación. El equipo concluye «sistema validado para uso clínico». ¿Qué falta?",["BIOINST-U09-LO02","BIOINST-U09-LO05"],"La simulación puede contribuir a verificación y validación limitada, pero no demuestra por sí sola que el producto satisfaga necesidades en usuarios, tareas y entornos representativos ni constituye validación clínica. Deben declararse fidelidad/cobertura y evidencia adicional necesaria.","Verificación contra requisitos y validación del propósito/entorno son objetivos diferentes.",["all-verification-equals-validation","simulation-equals-clinical-validation"],["nasa-se-handbook-vv-2016","fda-human-factors-2026"]),
("Q04","Un paquete se pierde, el software interpola silenciosamente y un usuario podría interpretar la curva como observada. Construye la cadena de riesgo mínima.",["BIOINST-U09-LO03"],"Peligro informacional/resultado incorrecto; evento de pérdida; interpolación no marcada; situación peligrosa de confianza en dato no observado; daño posible dependiente del uso; controles como detección de secuencia, bandera de calidad y presentación explícita, con pruebas de efectividad.","El fallo inicial no debe saltarse las condiciones intermedias hasta el daño.",["failure-is-harm","interpolation-recovers-observation"],["iso-14971-2019-current"]),
("Q05","Se añade confirmación temporal para reducir falsas alarmas, pero introduce 3 s extra de latencia. ¿Puede cerrarse el riesgo original sin más?",["BIOINST-U09-LO03","BIOINST-U09-LO04"],"No. Debe verificarse el efecto del control sobre el riesgo original y reevaluar la nueva latencia como posible riesgo/impacto sobre requisitos y uso. Un control no se evalúa aislado del sistema.","Los controles requieren evidencia y pueden cambiar otras interacciones o riesgos.",["control-written-means-effective","risk-controls-cannot-create-new-risk"],["iso-14971-2019-current","fda-human-factors-2026"]),
("Q06","El requisito bloqueado es latencia ≤2 s; se observa 2.4 s y el equipo propone cambiarlo a ≤3 s para cerrar la discrepancia. Evalúa.",["BIOINST-U09-LO01","BIOINST-U09-LO05"],"El resultado debe registrarse como discrepancia respecto del criterio vigente. Cambiar el requisito exige una razón independiente, análisis de impacto sobre necesidad/riesgo y reevaluación de evidencia; no puede usarse como edición retrospectiva para hacer pasar el caso.","Criterios preestablecidos y control de cambios protegen la trazabilidad de la decisión.",["criterion-can-follow-result","editing-requirement-erases-failure"],["nasa-se-handbook-vv-2016","jcgm-106-2012"]),
("Q07","Una validación de interfaz fue realizada solo por desarrolladores en oficina, aunque el uso previsto incluye personal con guantes, ruido y alarmas simultáneas. ¿Qué conclusión es defendible?",["BIOINST-U09-LO02","BIOINST-U09-LO04"],"La prueba aporta evidencia limitada al escenario evaluado. No representa adecuadamente los usuarios/tareas/entornos descritos; se necesita un plan de validación representativo y basado en riesgos de uso antes de una conclusión más amplia.","Factores humanos dependen de usuario, entorno e interfaz, no solo de que la función se ejecute.",["developers-are-always-representative-users","office-test-covers-clinical-environment"],["fda-human-factors-2026","fda-human-factors-content-2026"]),
("Q08","La matriz educativa tiene 100 % de requisitos con pruebas y cuatro riesgos con controles. ¿Puede declararse cumplimiento QMSR/ISO 13485/ISO 14971 y aptitud clínica?",["BIOINST-U09-LO04","BIOINST-U09-LO05"],"No. La matriz demuestra únicamente la cobertura educativa definida. Cumplimiento regulatorio, gestión de riesgos completa, sistema de calidad, seguridad y aptitud clínica requieren requisitos aplicables, procesos controlados, evidencia completa y revisión competente fuera del alcance de la práctica.","La QMSR vigente tiene un ámbito regulatorio real y no puede satisfacerse por una simulación académica.",["course-matrix-equals-qms-compliance","risk-table-equals-clinical-approval"],["fda-qmsr-2026","iso-14971-2019-current"]),
]
assessment["items"]=[]
for qid,prompt,los,expected,explanation,mis,source_ids in items:
    assessment["items"].append({"id":f"BIOINST-U09-{qid}","type":"case_analysis","prompt":prompt,"linked_learning_outcome_ids":los,"difficulty":"advanced","cognitive_level":"evaluate","answer_key":{"expected_answer":expected,"explanation":explanation,"common_misconceptions":mis},"feedback":{"correct":"La respuesta mantiene trazabilidad entre uso, requisito, evidencia y riesgo sin exceder el alcance.","incorrect":"Reconstruye la cadena: necesidad/uso → requisito → evidencia → riesgo/control → discrepancia → conclusión permitida."},"source_ids":source_ids,"status":"curated_pending_expert_review"})
assessment["status"]="curated_pending_expert_review"


def norm(s): return re.sub(r"\s+"," ",s.strip().casefold())
def next_gid():
    nums=[int(m.group(1)) for e in glossary["entries"] if (m:=re.fullmatch(r"BIOINST-GLO-(\d+)",e.get("id","")))]
    return f"BIOINST-GLO-{max(nums)+1:03d}"
def ensure(term,definition,source_ids,locators,status="verified_contextually"):
    e=next((x for x in glossary["entries"] if norm(x.get("term",""))==norm(term)),None)
    if e is None:
        e={"id":next_gid(),"term":term,"definition":definition,"unit_ids":[],"source_ids":[],"verification_status":status}
        glossary["entries"].append(e)
    e["definition"]=definition
    e["unit_ids"]=sorted(set(e.get("unit_ids",[]))|{"BIOINST-U09"})
    e["source_ids"]=source_ids;e["verification_status"]=status
    e["source_locators"]=[{"source_id":s,"locator":l} for s,l in locators]
    return e["id"]

gspec=[
("Necesidad de usuario","Problema, expectativa o resultado buscado por una parte interesada que motiva requisitos y decisiones de diseño.",["nasa-requirements-appendix"],[('nasa-requirements-appendix','Requirements quality and validation checklists')]),
("Uso previsto","Finalidad y contexto declarados que delimitan usuarios, usos, tareas y entornos relevantes para la validación.",["fda-human-factors-2026"],[('fda-human-factors-2026','Intended users, uses and use environments')],"verified_directly"),
("Requisito","Condición documentada suficientemente clara, consistente y verificable para guiar diseño y evidencia.",["nasa-requirements-appendix"],[('nasa-requirements-appendix','Appendix C')]),
("Verificación","Obtención de evidencia de que un producto o artefacto cumple requisitos o especificaciones aprobadas.",["nasa-se-handbook-vv-2016"],[('nasa-se-handbook-vv-2016','Sections 2.4 and 5.3')],"verified_directly"),
("Validación","Obtención de evidencia de que el producto cumple el propósito y expectativas pertinentes en su entorno o aplicación prevista.",["nasa-se-handbook-vv-2016"],[('nasa-se-handbook-vv-2016','Sections 2.4 and 5.4')],"verified_directly"),
("Trazabilidad bidireccional","Relación navegable hacia adelante y atrás entre artefactos del ciclo de vida, usada para detectar elementos perdidos o huérfanos.",["nasa-requirements-traceability"],[('nasa-requirements-traceability','SWE-047 rationale')],"verified_directly"),
("Peligro","Fuente potencial de daño dentro de un proceso de gestión de riesgos; debe mantenerse separada del daño y de la situación peligrosa.",["iso-14971-2019-current"],[('iso-14971-2019-current','ISO official scope/current edition confirmed 2025')],"verified_directly"),
("Situación peligrosa","Estado o circunstancia de exposición a un peligro usado como capa causal entre eventos y daño potencial.",["iso-14971-2019-current"],[('iso-14971-2019-current','ISO 14971 risk terminology/process context')]),
("Daño","Consecuencia adversa potencial que se documenta separada del fallo o peligro que puede contribuir a ella.",["iso-14971-2019-current"],[('iso-14971-2019-current','ISO 14971 risk terminology/process context')]),
("Riesgo","Combinación contextual de la probabilidad de ocurrencia de daño y la severidad de ese daño dentro de un proceso de gestión de riesgos.",["iso-14971-2019-current"],[('iso-14971-2019-current','ISO 14971 risk-management scope')]),
("Control de riesgo","Medida destinada a reducir un riesgo y que requiere evidencia de implementación y efectividad dentro del proceso aplicable.",["iso-14971-2019-current"],[('iso-14971-2019-current','ISO overview: risk control and effectiveness monitoring')]),
("Riesgo residual","Riesgo que permanece después de aplicar controles; describirlo no equivale a declarar su aceptabilidad profesional.",["iso-14971-2019-current"],[('iso-14971-2019-current','Risk control/benefit-risk lifecycle context')]),
("Discrepancia","Diferencia documentada entre resultado esperado o criterio y resultado observado que permanece abierta hasta una resolución trazable.",["nasa-se-handbook-vv-2016"],[('nasa-se-handbook-vv-2016','Verification completion and discrepancy closure')]),
("Cobertura","Grado en que las relaciones necesarias entre necesidades, requisitos, riesgos, controles y evidencia están presentes y justificadas.",["nasa-requirements-traceability"],[('nasa-requirements-traceability','Bidirectional traceability rationale')]),
("Criterio de aceptación","Condición predefinida usada para decidir si una evidencia satisface un requisito, sin modificarse retrospectivamente para acomodar resultados.",["jcgm-106-2012"],[('jcgm-106-2012','Previously established decision-rule principle')]),
("Factores humanos","Disciplina que estudia la interacción entre usuarios, entorno e interfaz para reducir errores de uso y riesgos asociados.",["fda-human-factors-2026"],[('fda-human-factors-2026','August 2026 guidance scope')],"verified_directly"),
("Usuario previsto","Población de usuarios cuyas capacidades, experiencia y características deben corresponder al uso que una validación pretende representar.",["fda-human-factors-2026"],[('fda-human-factors-2026','Device users/intended users')],"verified_directly"),
("Entorno de uso","Condiciones físicas, sociales y operativas donde el dispositivo se pretende utilizar y que pueden afectar interacción y desempeño.",["fda-human-factors-2026"],[('fda-human-factors-2026','Use environments')],"verified_directly"),
]
unit["glossary_entry_ids"]=[ensure(*x) for x in gspec]

claims["claims"]=[c for c in claims["claims"] if c.get("unit_id")!="BIOINST-U09"]
new=[]
for i,(text,sid,loc,ctype,risk,support) in enumerate(claim_specs,1):
    src=next(s for s in sources["sources"] if s["id"]==sid)
    cid=f"BIOINST-U09-C{i:03d}"
    new.append({"claim_id":cid,"unit":9,"text":text,"claim_type":ctype,"risk":risk,"context":"Aplicado a U9 como marco educativo de V&V y riesgo; decisiones clínicas/regulatorias requieren fuentes y revisión competentes adicionales.","source_id":sid,"locator":{"section":loc},"support":support,"source_verification_status":src["verification_status"],"review_state":"ai_review_provisional","reviewer_validation_id":None,"reviewed_at":"2026-08-24","id":cid,"unit_id":"BIOINST-U09"})
claims["claims"].extend(new)
claims["content_version"]="units-01-09-review-2026-08-24"
unit["claim_ids"]=[c["id"] for c in new]
unit["source_ids"]=["nasa-se-handbook-vv-2016","nasa-requirements-traceability","nasa-requirements-appendix","bipm-vim-verification","bipm-vim-validation","iso-14971-2019-current","fda-qmsr-2026","fda-qmsr-risk-design-2026","fda-human-factors-2026","fda-human-factors-content-2026","jcgm-106-2012"]
unit["common_errors"]=[
{"error":"Usar necesidad y requisito como sinónimos.","correction":"Conservar la necesidad como justificación y redactar uno o más requisitos verificables con condiciones y criterios."},
{"error":"Llamar validación a cualquier prueba que pase.","correction":"Preguntar si la evidencia demuestra cumplimiento de requisito o satisfacción del propósito/uso previsto."},
{"error":"Saltar del fallo al daño.","correction":"Documentar eventos y situación peligrosa antes del daño posible."},
{"error":"Dar un control por efectivo porque aparece en la matriz.","correction":"Vincular requisito de control, evidencia de implementación y prueba de efectividad."},
{"error":"Borrar discrepancias o editar el criterio después del resultado.","correction":"Conservar el resultado, gestionar cambio e impacto y volver a probar cuando corresponda."},
{"error":"Confundir cobertura documental con aprobación clínica/regulatoria.","correction":"Limitar la conclusión a configuración, uso, requisitos y evidencia evaluados."},
]
unit["biomedical_connections"]=["Alarmas y software biomédico: la verificación de latencia no demuestra por sí sola que la alarma sea útil o segura para usuarios reales.","Integridad de señales: huecos, interpolaciones y metadatos pueden entrar en cadenas de riesgo que necesitan controles verificables.","Factores humanos: usuarios, tareas, entornos e interfaz forman parte de la evidencia necesaria cuando el riesgo depende de la interacción de uso."]
unit["editorial_notice"]="Autoría canónica nueva conforme al mapa de migración: canonical U9 tiene origin=new y action=author, sin unidad autoral histórica equivalente. La unidad usa fuentes actuales de V&V, riesgo, QMSR y factores humanos, pero mantiene revisión disciplinaria humana, validación clínica, conformidad y autorización regulatoria fuera de cualquier afirmación de cierre."
unit["legacy_origin"]="data/generated_units/bioinstrumentacion/unit-09.json (bootstrap público; no existe equivalente autoral legacy)"

assert len(unit["topics"])==6 and sum(len(t["subtopics"]) for t in unit["topics"])==18
assert len(unit["examples"])==6
act=unit["activities"][0]; assert (len(act["instructions"]),len(act["tasks"]),len(act["deliverables"]),len(act["checking_criteria"]))==(5,8,6,10)
assert len(assessment["items"])==8 and len(unit["glossary_entry_ids"])==18 and len(new)==18
serialized=json.dumps(unit,ensure_ascii=False)
for c in new: assert c["text"] in serialized

dump(unit_path,unit);dump(assessment_path,assessment);dump(glossary_path,glossary);dump(sources_path,sources);dump(claims_path,claims)
print("Curated canonical Bioinstrumentation U9 as new authoring unit")
