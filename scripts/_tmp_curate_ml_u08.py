from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"
DATE = "2026-08-23"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


unit_path = COURSE / "units" / "unit-08.json"
unit = load(unit_path)
unit["prerequisite_unit_ids"] = [f"MLBIO-U0{i}" for i in range(1, 8)]

# Repair inherited heading/content mismatches so the conceptual map matches the prose.
by_topic = {t["id"]: t for t in unit["topics"]}
sub2 = {s["id"]: s for s in by_topic["MLBIO-U08-T02"]["subtopics"]}
sub2["MLBIO-U08-T02-ST03"]["title"] = "Seguridad, trazabilidad y transparencia acompañan la operación"
sub3 = {s["id"]: s for s in by_topic["MLBIO-U08-T03"]["subtopics"]}
sub3["MLBIO-U08-T03-ST03"]["title"] = "La monitorización debe activar acciones predefinidas"
sub4 = {s["id"]: s for s in by_topic["MLBIO-U08-T04"]["subtopics"]}
sub4["MLBIO-U08-T04-ST03"]["title"] = "Incidentes y retirada requieren contención, trazabilidad y reversión"

activity = unit["activities"][0]
activity.update({
    "purpose": "Diseñar la transición completa desde un modelo retrospectivamente validado hasta evaluación prospectiva, operación monitorizada, cambios controlados y retirada segura, manteniendo trazabilidad de versiones, decisiones e incidentes.",
    "prerequisite_unit_ids": [f"MLBIO-U0{i}" for i in range(1, 8)],
    "instructions": [
        "Construir una escalera de evidencia que separe validación retrospectiva, fase silenciosa, evaluación clínica temprana y ensayo de impacto; para cada fase definir pregunta, usuarios, exposición a la salida, comparador y criterio de avance.",
        "Mapear el flujo operacional de extremo a extremo desde elegibilidad y captura de datos hasta inferencia, presentación, revisión, acción y documentación, incluyendo interfaces, responsables, latencia, abstención y flujo alternativo durante fallos.",
        "Definir contratos de datos y un panel de monitorización con denominadores explícitos para elegibilidad, cobertura, fallos, latencia, calidad de datos, desempeño, calibración, subgrupos, uso y seguridad; vincular cada indicador con una acción predefinida.",
        "Diseñar control de cambios y versiones para datos, modelo, umbral, interfaz e infraestructura, especificando pruebas de regresión, evidencia requerida, aprobación, trazabilidad, reversión y qué modificaciones podrían entrar en un PCCP.",
        "Redactar un procedimiento de incidentes, suspensión, retirada y reintroducción que preserve evidencia, identifique pacientes afectados, restaure un flujo clínico seguro y exija nueva verificación antes de reactivar una versión corregida."
    ],
    "tasks": [
        "Distinguir qué puede y qué no puede concluirse de una fase silenciosa frente a una evaluación clínica temprana y un ensayo de impacto.",
        "Elegir y justificar la unidad de asignación de un ensayo de impacto cuando profesionales pueden aprender del sistema y contaminar la comparación entre pacientes.",
        "Mapear elegibilidad, datos, procesamiento, inferencia, alerta, revisión, acción, documentación y alternativa de fallo para un sistema clínico concreto.",
        "Definir un contrato de datos con campos, unidades, rangos, temporalidad, faltantes, códigos, compatibilidad y conducta segura ante entradas inválidas.",
        "Proponer indicadores con denominadores que distingan disponibilidad técnica, cobertura operacional, drift de datos, desempeño clínico, calibración, uso humano e incidentes.",
        "Diseñar una alerta de drift o degradación con volumen mínimo, incertidumbre, severidad, responsable y acción asociada, evitando que un cambio estadístico irrelevante active una respuesta desproporcionada.",
        "Clasificar un cambio de umbral, una actualización de interfaz y un reentrenamiento según su posible impacto, y definir evidencia, prueba de regresión, aprobación y versión requerida para cada uno.",
        "Redactar el procedimiento para contener un incidente grave, suspender inferencias, volver al flujo alternativo, evaluar afectados y decidir retirada o reintroducción."
    ],
    "deliverables": [
        "Escalera de evidencia con fases retrospectiva, silenciosa, clínica temprana e impacto, indicando pregunta, diseño, comparador, desenlaces, riesgos y criterio de avance de cada etapa.",
        "Mapa de flujo e interfaces con usuarios, decisiones, latencias, dependencias, puntos de fallo, abstención, contingencia y responsable de cada transición.",
        "Contrato de datos y especificación de cobertura operacional con elegibilidad, unidades, rangos, temporalidad, faltantes, validaciones, errores y denominadores auditables.",
        "Plan de monitorización con indicadores técnicos, de datos, desempeño, calibración, subgrupos, uso y seguridad, cada uno con frecuencia, ventana, umbral, incertidumbre, responsable y acción.",
        "Matriz de control de cambios y versiones que clasifique modificaciones, exija pruebas de regresión y evidencia, documente aprobación/reversión e identifique el alcance de un eventual PCCP.",
        "Runbook de incidentes y retirada con detección, severidad, contención, preservación de evidencia, identificación de afectados, comunicación, flujo alternativo y criterios de reintroducción."
    ],
    "checking_criteria": [
        "La fase silenciosa se utiliza para operación y desempeño contemporáneo sin atribuir efecto sobre decisiones que nunca recibieron la salida.",
        "La evaluación clínica temprana y el ensayo de impacto tienen preguntas, comparadores, usuarios y desenlaces acordes con el grado de exposición real al sistema.",
        "La unidad de asignación y el diseño del estudio consideran contaminación, aprendizaje de usuarios y dependencia entre observaciones.",
        "El mapa operacional cubre todo el trayecto desde elegibilidad hasta acción y contiene un flujo alternativo seguro para caída, abstención o entrada inválida.",
        "Cobertura, fallos, alertas, acciones e incidentes se expresan con denominadores explícitos; los conteos aislados no sustituyen tasas ni riesgo.",
        "La monitorización separa indicadores técnicos, de datos, desempeño clínico, calibración, subgrupos, interacción humana y seguridad.",
        "Cada señal de monitorización tiene severidad, incertidumbre, responsable y acción predefinida; drift estadístico no se trata automáticamente como daño clínico.",
        "Todo cambio relevante en datos, modelo, umbral, interfaz o infraestructura está versionado, probado, aprobado y puede revertirse.",
        "Un PCCP delimita cambios previstos y su protocolo de control; no se interpreta como permiso para aprendizaje continuo sin supervisión.",
        "El procedimiento de incidentes permite suspender, preservar evidencia, identificar afectados, volver al flujo alternativo y exigir verificación antes de reintroducir el sistema."
    ],
    "estimated_duration_minutes": 240,
    "status": "curated_pending_expert_review",
})

for sid in ["consort-ai-2020", "spirit-ai-2020"]:
    if sid not in unit["source_ids"]:
        unit["source_ids"].append(sid)
unit["claim_ids"] = [f"MLBIO-U08-C{i:03d}" for i in range(1, 15)]
save(unit_path, unit)

assessment_path = COURSE / "assessments" / "unit-08.json"
assessment = load(assessment_path)
assessment["purpose"] = "Evaluar si el estudiante puede diseñar evaluación prospectiva e impacto, mapear una operación segura, construir monitorización accionable y gobernar cambios, incidentes y retirada durante el ciclo de vida de IA clínica."
assessment["status"] = "curated_pending_expert_review"
assessment["items"] = [
    {
        "id": "MLBIO-U08-Q01", "type": "case_analysis",
        "prompt": "Un modelo ya validado retrospectivamente comienza a ejecutarse cada cinco minutos con datos reales, pero su salida permanece oculta a los clínicos. Durante seis semanas se miden cobertura, latencia, fallos de integración, calibración y errores. ¿Qué tipo de evidencia produce esta fase y qué conclusión sobre impacto clínico sigue prohibida?",
        "linked_learning_outcome_ids": ["MLBIO-U08-LO01", "MLBIO-U08-LO04"], "difficulty": "intermediate", "cognitive_level": "analyze",
        "answer_key": {"expected_answer": "Es una fase silenciosa prospectiva: permite conocer operación contemporánea, cobertura, integración, latencia y desempeño sin alterar la atención. No puede demostrar que mostrar la predicción mejore decisiones, procesos o resultados, porque los usuarios nunca estuvieron expuestos a la salida. Para impacto se necesita una fase en uso con comparador y diseño apropiado.", "explanation": "La evidencia depende de qué componente del sistema estuvo activo y qué pudo modificar causalmente la atención.", "common_misconceptions": ["Llamar ensayo prospectivo de impacto a cualquier ejecución con datos futuros.", "Atribuir beneficio clínico porque la calibración prospectiva sea buena."]},
        "feedback": {"correct": "Ha separado operación prospectiva de efecto sobre decisiones.", "incorrect": "Pregunte si la salida pudo cambiar lo que hizo algún profesional. Si nadie la vio, esa fase no estima el efecto del uso del sistema."},
        "source_ids": ["decide-ai", "imdrf-fda-gmlp"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U08-Q02", "type": "case_analysis",
        "prompt": "En una evaluación clínica temprana, diez profesionales reciben una alerta de deterioro. El modelo conserva buen AUC, pero algunos usuarios ignoran alertas, otros solicitan pruebas innecesarias y el tiempo de decisión aumenta. Diseñe qué debe medir y reportar el estudio antes de ampliar el despliegue.",
        "linked_learning_outcome_ids": ["MLBIO-U08-LO02", "MLBIO-U08-LO03"], "difficulty": "advanced", "cognitive_level": "create",
        "answer_key": {"expected_answer": "Además del desempeño del modelo deben medirse usuarios y formación, contexto, disponibilidad y latencia, aceptación/rechazo, discrepancias, pruebas o acciones generadas, errores, daño, carga y variabilidad entre profesionales. Deben documentarse modificaciones del sistema durante la fase, flujo alternativo y problemas de seguridad. La ampliación requiere criterios de avance predefinidos y no solo mantener AUC.", "explanation": "DECIDE-AI orienta evaluación clínica temprana del sistema humano-IA, incluyendo interacción, flujo, seguridad y aprendizaje de usuarios.", "common_misconceptions": ["Considerar suficiente que el algoritmo mantenga discriminación.", "Interpretar uso heterogéneo como problema exclusivo de formación sin evaluar interfaz y flujo."]},
        "feedback": {"correct": "Ha evaluado el sistema humano-IA y no solo el predictor.", "incorrect": "Enumere qué cambia cuando la salida llega a una persona: comprensión, confianza, acción, tiempo, errores, recursos y seguridad."},
        "source_ids": ["decide-ai", "fda-transparency-mlmd"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U08-Q03", "type": "case_analysis",
        "prompt": "Se quiere probar una alerta en una UCI donde los mismos médicos atienden simultáneamente pacientes asignados a intervención y control. Compare aleatorización por paciente y por unidad/periodo y explique el riesgo de contaminación.",
        "linked_learning_outcome_ids": ["MLBIO-U08-LO01", "MLBIO-U08-LO03"], "difficulty": "advanced", "cognitive_level": "evaluate",
        "answer_key": {"expected_answer": "Aleatorizar pacientes puede ser eficiente, pero los médicos pueden aprender de la alerta y cambiar su conducta también con controles, contaminando la comparación. Una asignación por unidad, profesional o periodo puede reducir ese aprendizaje cruzado, a costa de menos unidades independientes y necesidad de análisis por conglomerados y efectos temporales. La elección depende del mecanismo de intervención, flujo y factibilidad y debe preespecificarse en el protocolo.", "explanation": "Un ensayo de impacto evalúa una intervención sociotécnica; la unidad de asignación debe corresponder a cómo el sistema puede modificar conducta.", "common_misconceptions": ["Elegir paciente individual por defecto sin analizar contaminación.", "Tratar observaciones de un mismo servicio o periodo como independientes después de una asignación por conglomerados."]},
        "feedback": {"correct": "Ha vinculado unidad de asignación con contaminación y estructura del análisis.", "incorrect": "Pregunte quién aprende del sistema. Si la misma persona atiende ambos brazos, el efecto puede cruzar de intervención a control."},
        "source_ids": ["spirit-ai-2020", "consort-ai-2020"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U08-Q04", "type": "case_analysis",
        "prompt": "Después de una actualización de la interfaz, los falsos positivos observados caen un 40%. Sin embargo, el sistema dejó de procesar estudios de un dispositivo antiguo que concentra pacientes mayores. Diseñe el análisis que evita declarar una mejora falsa.",
        "linked_learning_outcome_ids": ["MLBIO-U08-LO04"], "difficulty": "advanced", "cognitive_level": "analyze",
        "answer_key": {"expected_answer": "Debe reconstruirse la cadena de denominadores: elegibles, recibidos, procesados, rechazados, abstenciones, alertas y desenlaces, estratificada por dispositivo y edad. La caída de falsos positivos puede reflejar pérdida selectiva de cobertura y no mejor desempeño. Se debe tratar la exclusión como incidente o cambio operacional, restaurar un flujo seguro y evaluar pacientes afectados antes de comparar métricas condicionadas a los pocos casos procesados.", "explanation": "Sin denominadores, mejorar una métrica entre casos procesados puede ocultar selección operacional y reducción de acceso al sistema.", "common_misconceptions": ["Celebrar menor número de errores sin revisar cuántos pacientes dejaron de evaluarse.", "Calcular cobertura solo sobre casos que llegaron al modelo y excluir silenciosamente los rechazados."]},
        "feedback": {"correct": "Ha usado denominadores y subgrupos para detectar pérdida de cobertura.", "incorrect": "Empiece antes de la inferencia: ¿cuántos pacientes eran elegibles y cuántos dejaron de atravesar cada interfaz después del cambio?"},
        "source_ids": ["imdrf-fda-gmlp", "fda-transparency-mlmd"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U08-Q05", "type": "case_analysis",
        "prompt": "Las etiquetas clínicas definitivas llegan con 60 días de retraso. Esta semana cambian las distribuciones de dos laboratorios y aumenta la latencia, pero todavía no puede recalcularse AUC ni calibración. Diseñe una monitorización que responda sin confundir ausencia de etiquetas con estabilidad demostrada.",
        "linked_learning_outcome_ids": ["MLBIO-U08-LO04"], "difficulty": "advanced", "cognitive_level": "create",
        "answer_key": {"expected_answer": "Debe combinar indicadores tempranos de operación y datos —cobertura, faltantes, unidades, rangos, dispositivo, latencia, errores, volumen, población y uso— con una revisión diferida de desempeño cuando lleguen etiquetas. Cada señal necesita ventana, volumen mínimo, incertidumbre, severidad, responsable y acción provisional. El cambio de distribución inicia investigación, no prueba por sí solo degradación clínica; la falta de etiquetas tampoco autoriza concluir estabilidad.", "explanation": "La monitorización posdespliegue trabaja con señales a diferentes velocidades y debe distinguir proxy operacional de desenlace clínico confirmado.", "common_misconceptions": ["Esperar 60 días sin ninguna vigilancia porque todavía no hay AUC.", "Suspender o reentrenar automáticamente por cualquier test de drift estadístico."]},
        "feedback": {"correct": "Ha diseñado capas de indicadores y acciones proporcionales a la evidencia disponible.", "incorrect": "Separe qué puede observar hoy de lo que requiere desenlaces tardíos y defina qué acción provisional es segura para cada nivel de evidencia."},
        "source_ids": ["imdrf-fda-gmlp", "fda-pccp-mlmd"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U08-Q06", "type": "case_analysis",
        "prompt": "Un hospital quiere reducir el umbral de alerta de 0,20 a 0,12 y, por separado, reentrenar el modelo cada trimestre con casos locales. Explique por qué ambos son cambios del sistema y qué debe existir antes de desplegarlos; indique el papel de un PCCP.",
        "linked_learning_outcome_ids": ["MLBIO-U08-LO05"], "difficulty": "advanced", "cognitive_level": "evaluate",
        "answer_key": {"expected_answer": "Cambiar el umbral altera quién recibe una acción aunque los pesos sean iguales; reentrenar modifica directamente el modelo. Ambos requieren clasificación de impacto, versión, evidencia, pruebas de regresión, aprobación, trazabilidad y reversión. Un PCCP puede describir de antemano tipos de modificación previstos, límites y protocolo para implementarlos y evaluarlos, pero no convierte cualquier cambio futuro en actualización automática sin control.", "explanation": "La versión clínica incluye decisiones y componentes alrededor del algoritmo; gobernar cambios significa controlar cómo cada modificación puede alterar seguridad y desempeño.", "common_misconceptions": ["Versionar solo cuando cambian los coeficientes o pesos.", "Interpretar PCCP como autorización general para aprendizaje continuo no supervisado."]},
        "feedback": {"correct": "Ha tratado umbral y reentrenamiento como cambios versionados y ha delimitado el PCCP.", "incorrect": "Pregunte si la modificación puede cambiar qué paciente recibe qué recomendación. Si sí, necesita análisis de impacto y evidencia aunque el archivo del modelo no cambie."},
        "source_ids": ["fda-pccp-mlmd", "imdrf-fda-gmlp"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U08-Q07", "type": "case_analysis",
        "prompt": "Se propone que el sistema se reentrene cada noche con los últimos casos y sustituya automáticamente la versión anterior si mejora una métrica interna. Evalúe la propuesta y redacte un flujo de cambio seguro.",
        "linked_learning_outcome_ids": ["MLBIO-U08-LO05"], "difficulty": "advanced", "cognitive_level": "create",
        "answer_key": {"expected_answer": "La propuesta no preserva una versión clínica controlada ni una evaluación independiente y puede introducir degradación, sesgo o cambios inesperados. El flujo seguro debe definir modificaciones permitidas, datos y referencia, particiones independientes, criterios múltiples de aceptación, pruebas de regresión y subgrupos, revisión/aprobación, identificador de versión, despliegue controlado, monitorización y rollback. Si existe PCCP, el cambio debe permanecer dentro de su alcance y protocolo.", "explanation": "Aprendizaje continuo no significa publicación continua: el ciclo de vida exige gobernanza, evidencia y capacidad de revertir.", "common_misconceptions": ["Usar mejora de una sola métrica interna como gate suficiente.", "Eliminar supervisión porque el reentrenamiento esté automatizado técnicamente."]},
        "feedback": {"correct": "Ha convertido reentrenamiento automático en un proceso versionado y reevaluable.", "incorrect": "Separe automatizar el cálculo de un candidato de autorizar que ese candidato se convierta en la nueva versión clínica."},
        "source_ids": ["imdrf-fda-gmlp", "fda-pccp-mlmd"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U08-Q08", "type": "case_analysis",
        "prompt": "Una actualización del sistema empieza a intercambiar unidades de una variable y emite recomendaciones potencialmente dañinas durante cuatro horas. Diseñe las primeras acciones, la retirada temporal y los requisitos mínimos para una eventual reintroducción.",
        "linked_learning_outcome_ids": ["MLBIO-U08-LO06"], "difficulty": "advanced", "cognitive_level": "create",
        "answer_key": {"expected_answer": "Debe contenerse el incidente: suspender inferencias o la función afectada, restaurar el flujo alternativo seguro, preservar logs/versiones/entradas/salidas, identificar periodo y pacientes potencialmente afectados, comunicar a responsables y evaluar daño. La causa y controles correctivos deben documentarse. La versión no se reintroduce solo tras corregir el bug: necesita pruebas de regresión, compatibilidad de unidades, revisión de evidencia, aprobación y despliegue/monitorización controlados; si no se recupera seguridad o beneficio, procede retirada prolongada o definitiva.", "explanation": "La retirada es una herramienta de seguridad planificada; preservar evidencia y mantener una alternativa clínica permiten investigar sin continuar exponiendo pacientes.", "common_misconceptions": ["Corregir el código y reiniciar inmediatamente sin analizar pacientes afectados.", "Borrar logs o sobrescribir la versión defectuosa, perdiendo trazabilidad del incidente."]},
        "feedback": {"correct": "Ha priorizado contención, trazabilidad, flujo alternativo y verificación antes de reintroducir.", "incorrect": "Ordene la respuesta: detener daño, conservar evidencia, saber a quién afectó, restaurar atención segura y solo después evaluar una versión corregida."},
        "source_ids": ["imdrf-fda-gmlp", "fda-pccp-mlmd", "fda-transparency-mlmd"], "status": "curated_pending_expert_review"
    }
]
save(assessment_path, assessment)

sources_path = COURSE / "sources.json"
sources_doc = load(sources_path)
known = {s["id"] for s in sources_doc["sources"]}
new_sources = [
    {
        "registry_id": "consort-ai-2020", "id": "consort-ai-2020",
        "title": "Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension",
        "authors": ["Xiaoxuan Liu", "Samantha Cruz Rivera", "David Moher", "Melanie J. Calvert", "Alastair K. Denniston", "SPIRIT-AI and CONSORT-AI Working Group"],
        "organization": "Nature Medicine", "year": 2020,
        "url": "https://www.nature.com/articles/s41591-020-1034-x", "doi": "10.1038/s41591-020-1034-x",
        "type": "guía de reporte para ensayos clínicos con IA", "verification_status": "verified_directly",
        "locator": "Abstract; CONSORT-AI extension checklist and explanation, Nature Medicine 26:1364–1374",
        "role": "Extiende CONSORT para reportar ensayos clínicos de intervenciones con componente de IA, incluyendo sistema, entradas/salidas, interacción humano-IA, errores y análisis.",
        "curricular_function": "Sustentar el diseño y reporte del ensayo de impacto como evaluación del sistema en uso frente a un comparador, no solo de la predicción aislada.",
        "limitations": "Es una guía de reporte para ensayos; no determina por sí sola la elección del diseño, regulación aplicable, monitorización posdespliegue ni eficacia clínica.",
        "used_by_unit_ids": ["MLBIO-U08"]
    },
    {
        "registry_id": "spirit-ai-2020", "id": "spirit-ai-2020",
        "title": "Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI extension",
        "authors": ["Samantha Cruz Rivera", "Xiaoxuan Liu", "An-Wen Chan", "Alastair K. Denniston", "Melanie J. Calvert", "SPIRIT-AI and CONSORT-AI Working Group"],
        "organization": "Nature Medicine", "year": 2020,
        "url": "https://www.nature.com/articles/s41591-020-1037-7", "doi": "10.1038/s41591-020-1037-7",
        "type": "guía de protocolo para ensayos clínicos con IA", "verification_status": "verified_directly",
        "locator": "Abstract; SPIRIT-AI extension checklist and explanation, Nature Medicine 26:1351–1363",
        "role": "Extiende SPIRIT para protocolos de ensayos de intervenciones con IA, exigiendo especificación del sistema, uso, interacción, adquisición de datos y manejo de errores.",
        "curricular_function": "Fundamentar la preespecificación de un estudio prospectivo o ensayo de impacto antes de exponer usuarios y pacientes a una nueva versión del sistema.",
        "limitations": "Es una guía de protocolo y reporte; no sustituye gestión de riesgos, requisitos regulatorios, evaluación temprana ni vigilancia del ciclo de vida.",
        "used_by_unit_ids": ["MLBIO-U08"]
    }
]
for src in new_sources:
    if src["id"] not in known:
        sources_doc["sources"].append(src)
save(sources_path, sources_doc)

glossary_path = COURSE / "glossary.json"
glossary = load(glossary_path)
updates = {
    "MLBIO-GLO-081": ("Ejecución prospectiva de una versión del sistema con datos contemporáneos sin mostrar su salida ni permitir que modifique decisiones clínicas; sirve para evaluar operación, cobertura e integración, no impacto sobre la atención.", ["decide-ai","imdrf-fda-gmlp"], [("decide-ai","Early-stage clinical evaluation context and workflow"),("imdrf-fda-gmlp","Principles on testing under clinically relevant conditions")]),
    "MLBIO-GLO-082": ("Evaluación planificada hacia adelante en el tiempo en la que datos, operación, usuarios o resultados se observan conforme ocurre el uso definido del sistema.", ["spirit-ai-2020","decide-ai"], [("spirit-ai-2020","Protocol requirements for prospective AI intervention trials"),("decide-ai","Early-stage clinical evaluation")]),
    "MLBIO-GLO-083": ("Estudio comparativo que estima el efecto de utilizar el sistema completo sobre procesos, decisiones o resultados frente a una alternativa especificada.", ["consort-ai-2020","spirit-ai-2020"], [("consort-ai-2020","Clinical trial reporting for AI interventions"),("spirit-ai-2020","Clinical trial protocol requirements")]),
    "MLBIO-GLO-084": ("Capacidad de componentes y sistemas para intercambiar datos y utilizarlos conservando la semántica, unidades, temporalidad y condiciones necesarias para la función clínica prevista.", ["imdrf-fda-gmlp","fda-transparency-mlmd"], [("imdrf-fda-gmlp","Principles on representative data and relevant testing"),("fda-transparency-mlmd","Relevant information on inputs, workflow and limitations")]),
    "MLBIO-GLO-085": ("Proporción de casos elegibles que atraviesan correctamente el sistema operacional hasta el punto definido de procesamiento o decisión, con numerador y denominador explícitos.", ["decide-ai","imdrf-fda-gmlp"], [("decide-ai","Workflow, failures and clinical evaluation"),("imdrf-fda-gmlp","Monitoring and clinically relevant performance")]),
    "MLBIO-GLO-086": ("Cambio a lo largo del tiempo en datos, población, proceso, relaciones predictivas, uso o desempeño que puede o no tener consecuencias clínicas y requiere interpretación contextual.", ["imdrf-fda-gmlp","fda-pccp-mlmd"], [("imdrf-fda-gmlp","Monitoring and retraining principles"),("fda-pccp-mlmd","Change control and modification protocols")]),
    "MLBIO-GLO-087": ("Seguimiento planificado de operación, datos, desempeño, uso humano y seguridad durante el ciclo de vida, con indicadores vinculados a umbrales, responsables y acciones.", ["imdrf-fda-gmlp"], [("imdrf-fda-gmlp","Guiding principles on real-world monitoring and retraining risks")]),
    "MLBIO-GLO-088": ("Good Machine Learning Practice: principios para desarrollar, evaluar, desplegar y mantener sistemas de aprendizaje automático médico a lo largo del ciclo de vida, considerando datos, referencia, independencia, equipo humano-IA y monitorización.", ["imdrf-fda-gmlp"], [("imdrf-fda-gmlp","Introduction and guiding principles 1 and 3–9")]),
    "MLBIO-GLO-089": ("Comprobación preespecificada de que una modificación no degrada funciones, desempeño, interfaces o condiciones previamente aceptadas y que los riesgos relevantes siguen controlados.", ["imdrf-fda-gmlp","fda-pccp-mlmd"], [("imdrf-fda-gmlp","Testing under clinically relevant conditions and lifecycle monitoring"),("fda-pccp-mlmd","Modification protocol, validation and risk management")]),
    "MLBIO-GLO-090": ("Predetermined Change Control Plan: plan que delimita modificaciones previstas de un dispositivo habilitado por machine learning y describe cómo se desarrollarán, validarán, controlarán y comunicarán dentro de condiciones especificadas.", ["fda-pccp-mlmd"], [("fda-pccp-mlmd","Guiding principles for predetermined change control plans")]),
    "MLBIO-GLO-091": ("Evento o condición del sistema que causó o pudo causar daño, pérdida de control o degradación relevante y que requiere detección, contención, trazabilidad, evaluación y acción correctiva según severidad.", ["imdrf-fda-gmlp","fda-pccp-mlmd"], [("imdrf-fda-gmlp","Lifecycle risk, monitoring and human-AI performance"),("fda-pccp-mlmd","Risk management and modification controls")]),
    "MLBIO-GLO-092": ("Suspensión temporal o definitiva del uso de una versión cuando no puede mantenerse seguridad, compatibilidad, desempeño, beneficio o control aceptables, acompañada de un flujo alternativo seguro.", ["imdrf-fda-gmlp","fda-transparency-mlmd"], [("imdrf-fda-gmlp","Lifecycle monitoring and risk management principles"),("fda-transparency-mlmd","Limitations, risks and information for safe use")]),
}
for entry in glossary["entries"]:
    if entry["id"] in updates:
        definition, sids, locs = updates[entry["id"]]
        entry["definition"] = definition
        entry["source_ids"] = sids
        entry["source_locators"] = [{"source_id": sid, "locator": loc} for sid, loc in locs]
        entry["verification_status"] = "verified_directly"
save(glossary_path, glossary)

claims_path = COURSE / "claims.json"
claims_doc = load(claims_path)
claims_doc["scope"] = "Afirmaciones centrales de las Unidades 1–8 con fuente primaria, metodológica o regulatoria, localizador, alcance y revisión humana pendiente."
claims_doc["claims"] = [c for c in claims_doc["claims"] if c.get("unit") != 8]
specs = [
    ("Una fase silenciosa ejecuta el sistema prospectivamente sin mostrar resultados a los usuarios.","definition","medium","decide-ai","Early-stage clinical evaluation and workflow context"),
    ("Permite medir cobertura, fallos de integración, retrasos y desempeño bajo datos contemporáneos, aunque no estima el efecto sobre decisiones porque la salida no modifica la atención.","interpretation_boundary","high","decide-ai","Clinical workflow, safety and early evaluation"),
    ("La evaluación clínica temprana muestra la salida a usuarios en un entorno limitado y estudia seguridad, flujo, aprendizaje y variabilidad.","definition","high","decide-ai","Checklist and explanation on early-stage clinical evaluation"),
    ("Los ensayos de impacto evalúan si utilizar el sistema mejora procesos, decisiones o resultados frente a una alternativa.","definition","high","consort-ai-2020","Clinical trials evaluating interventions with an AI component"),
    ("Cada interfaz puede fallar.","safety_principle","high","imdrf-fda-gmlp","Testing under clinically relevant conditions and lifecycle risk"),
    ("La alternativa durante caída o abstención se diseña antes del uso.","safety_requirement","high","fda-transparency-mlmd","Limitations, workflow and safe-use information"),
    ("La monitorización comienza con denominadores.","methodological_principle","medium","imdrf-fda-gmlp","Monitoring under real-world conditions"),
    ("Los indicadores técnicos incluyen disponibilidad, latencia, fallos e integridad; los de datos incluyen distribución, faltantes, calidad, centro, dispositivo y población.","monitoring_requirement","high","imdrf-fda-gmlp","Monitoring and representative-data principles"),
    ("Los indicadores se vinculan con acciones predefinidas: investigar, restringir, recalibrar, suspender o retirar.","lifecycle_requirement","high","imdrf-fda-gmlp","Monitoring and management of retraining risks"),
    ("Los principios de Good Machine Learning Practice consideran el ciclo de vida completo: equipos multidisciplinarios, datos representativos, independencia entre conjuntos, referencia adecuada, desempeño del equipo humano-IA, pruebas bajo condiciones relevantes y monitorización.","definition","high","imdrf-fda-gmlp","Introduction and guiding principles 1 and 3–9"),
    ("Cada cambio en datos, modelo, umbral, interfaz o infraestructura puede modificar el sistema.","lifecycle_principle","high","fda-pccp-mlmd","Predetermined modifications and change-control principles"),
    ("Un plan de cambios predeterminados describe modificaciones previstas, protocolo de implementación, controles y límites.","definition","high","fda-pccp-mlmd","Guiding principles for predetermined change control plans"),
    ("El aprendizaje continuo no significa actualizar sin supervisión; cada versión necesita evidencia, aprobación, trazabilidad y capacidad de reversión.","lifecycle_requirement","high","fda-pccp-mlmd","Modification protocol, evidence, validation and risk controls"),
    ("La retirada temporal o definitiva es una medida de seguridad cuando se pierde calibración, compatibilidad, beneficio o control.","safety_principle","high","imdrf-fda-gmlp","Lifecycle monitoring, performance and risk management principles"),
]
for i, (text, ctype, risk, sid, locator) in enumerate(specs, start=1):
    cid = f"MLBIO-U08-C{i:03d}"
    claims_doc["claims"].append({
        "claim_id": cid, "unit": 8, "text": text, "claim_type": ctype, "risk": risk,
        "context": "Aplicado al ciclo de vida de sistemas predictivos biomédicos; la acción concreta depende del uso previsto, riesgo, jurisdicción, flujo, evidencia y versión del sistema.",
        "source_id": sid, "locator": {"section": locator},
        "support": "direct" if ctype == "definition" else "indirect",
        "source_verification_status": "verified_directly", "review_state": "ai_review_provisional",
        "reviewer_validation_id": None, "reviewed_at": DATE, "id": cid, "unit_id": "MLBIO-U08"
    })
save(claims_path, claims_doc)

# Extend durable canonical regression coverage through the final unit.
test_path = ROOT / "tests" / "test_academic_course_schema.py"
text = test_path.read_text(encoding="utf-8")
text = text.replace('self.assertEqual(report.counts["claims"], 98)', 'self.assertEqual(report.counts["claims"], 112)')
text = text.replace('for unit_number in (1, 2, 3, 4, 5, 6, 7):', 'for unit_number in (1, 2, 3, 4, 5, 6, 7, 8):')
text = text.replace('{"MLBIO-U02", "MLBIO-U03", "MLBIO-U04", "MLBIO-U05", "MLBIO-U06", "MLBIO-U07"}.intersection', '{"MLBIO-U02", "MLBIO-U03", "MLBIO-U04", "MLBIO-U05", "MLBIO-U06", "MLBIO-U07", "MLBIO-U08"}.intersection')
if "test_renderer_includes_curated_machine_learning_unit_8" not in text:
    marker = "    def test_every_assessment_item_maps_to_a_unit_outcome(self) -> None:\n"
    addition = '''    def test_renderer_includes_curated_machine_learning_unit_8(self) -> None:\n        unit = RENDERER.load_advanced_unit(ROOT, "machine-learning-biomedico-validacion-clinica", 8)\n        self.assertIsNotNone(unit)\n        assert unit is not None\n        self.assertEqual(unit["schema_version"], "canonical-1.0")\n        self.assertEqual(unit["unit"], 8)\n        self.assertEqual(unit["title"], "Evaluación prospectiva, despliegue y ciclo de vida")\n        self.assertEqual(len(unit["self_assessment"]), 8)\n        self.assertEqual(len(unit["guided_activities"][0]["deliverables"]), 6)\n        self.assertEqual(unit["guided_activities"][0]["estimated_duration_minutes"], 240)\n        self.assertEqual(len(unit["guided_activities"][0]["checking_criteria"]), 10)\n\n'''
    if marker not in text:
        raise RuntimeError("No se encontró punto de inserción U08")
    text = text.replace(marker, addition + marker)
test_path.write_text(text, encoding="utf-8")

print("Unidad 8 curada: teoría, actividad, evaluación, glosario, fuentes, claims y regresiones actualizados.")
