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


unit_path = COURSE / "units" / "unit-07.json"
unit = load(unit_path)
unit["prerequisite_unit_ids"] = [f"MLBIO-U0{i}" for i in range(1, 7)]

# Repair inherited heading/content mismatches.
by_topic = {t["id"]: t for t in unit["topics"]}
sub2 = {s["id"]: s for s in by_topic["MLBIO-U07-T02"]["subtopics"]}
sub2["MLBIO-U07-T02-ST03"]["title"] = "Eliminar una variable sensible no elimina proxies ni desigualdad"
sub3 = {s["id"]: s for s in by_topic["MLBIO-U07-T03"]["subtopics"]}
sub3["MLBIO-U07-T03-ST03"]["title"] = "La incertidumbre necesita reglas de abstención o revisión"

activity = unit["activities"][0]
activity.update({
    "purpose": "Auditar validez, aplicabilidad, equidad, proxies, explicaciones y factores humanos de un sistema predictivo, convirtiendo hallazgos en acciones verificables antes de su uso clínico.",
    "prerequisite_unit_ids": [f"MLBIO-U0{i}" for i in range(1, 7)],
    "instructions": [
        "Definir el uso previsto, población, usuarios y decisión del sistema; aplicar PROBAST+AI separando calidad del desarrollo, riesgo de sesgo de la evaluación y aplicabilidad.",
        "Preespecificar subgrupos clínicamente relevantes, daños y métricas; reportar denominadores, eventos e incertidumbre y distinguir diferencias observadas de explicaciones causales no demostradas.",
        "Auditar predictores sensibles, proxies y atajos mediante procedencia, distribución, perturbaciones y validación entre entornos; documentar qué señales podrían reflejar acceso, dispositivo o proceso asistencial.",
        "Evaluar explicaciones locales y globales por fidelidad, estabilidad, dependencia de referencia y utilidad para una tarea concreta, evitando interpretar atribuciones como mecanismos causales.",
        "Diseñar una evaluación del equipo humano-IA que compare profesional, modelo y combinación, mida automatización, rechazo, tiempos, discrepancias y recuperación de fallos y defina reglas de abstención y contingencia."
    ],
    "tasks": [
        "Separar en un caso clínico calidad del desarrollo, riesgo de sesgo de la evaluación y aplicabilidad, justificando cada juicio con evidencia observable.",
        "Evaluar si un estudio de un hospital terciario es aplicable a atención primaria aunque su estimación de desempeño tenga bajo riesgo de sesgo.",
        "Analizar una brecha de sensibilidad entre dos subgrupos con tamaños y eventos distintos, incorporando intervalos y evitando equiparar diferencia puntual con inequidad demostrada.",
        "Identificar proxies de acceso, centro, dispositivo o frecuencia de medición y proponer pruebas para distinguir señal clínica estable de atajo de proceso.",
        "Explicar por qué calibración, igualdad de sensibilidad y paridad de valores predictivos pueden entrar en conflicto cuando los riesgos basales difieren entre grupos.",
        "Auditar una explicación SHAP local: especificar referencia, variables correlacionadas, estabilidad ante perturbaciones y qué afirmaciones causales están prohibidas.",
        "Diseñar una regla de abstención o revisión humana para entradas fuera de distribución, información incompleta o incertidumbre insuficientemente controlada.",
        "Comparar profesional solo, modelo solo y equipo humano-IA en casos representativos y difíciles, midiendo aciertos, errores, tiempo, confianza, discrepancias y recuperación."
    ],
    "deliverables": [
        "Matriz PROBAST+AI con dominio, evidencia, juicio separado de calidad/sesgo/aplicabilidad, limitación y acción correctiva.",
        "Plan de análisis de subgrupos con definición previa, denominadores, eventos, métricas, incertidumbre, daños relevantes y regla para interpretar diferencias.",
        "Registro de proxies y atajos con origen de la señal, riesgo de degradación o inequidad, prueba propuesta y decisión de conservar, restringir o eliminar.",
        "Ficha de explicabilidad con método, referencia, alcance local/global, pruebas de fidelidad y estabilidad, limitaciones y afirmaciones que no pueden inferirse.",
        "Protocolo de factores humanos que compare profesional, modelo y equipo combinado e incluya automatización, rechazo, carga cognitiva, tiempos y recuperación de fallos.",
        "Plan de seguridad con abstención, escalado, responsable final, documentación de discrepancias, formación, contingencia sin sistema y criterios de reevaluación."
    ],
    "checking_criteria": [
        "Calidad del desarrollo, riesgo de sesgo y aplicabilidad se reportan como juicios distintos y no como una puntuación total.",
        "Los análisis de subgrupos incluyen tamaño, eventos, estimación e incertidumbre y no usan ausencia de significación como prueba de igualdad.",
        "Las métricas de fairness se vinculan con daño y decisión y se reconoce que algunos criterios pueden ser incompatibles.",
        "Eliminar una variable sensible no se considera suficiente para eliminar proxies o desigualdades asociadas.",
        "Los atajos se investigan con procedencia, perturbación o evaluación entre entornos y no solo con importancia de variables.",
        "Las explicaciones se describen como atribuciones del modelo, no como causas biológicas ni razonamiento humano equivalente.",
        "Fidelidad, estabilidad y referencia de las explicaciones están documentadas antes de usarlas para generar confianza.",
        "La probabilidad predicha no se interpreta automáticamente como incertidumbre epistemológica y existe una conducta definida para entradas fuera de alcance.",
        "La evaluación incluye al equipo humano-IA, no solo al algoritmo, y mide automatización, rechazo, tiempos y recuperación de errores.",
        "Responsabilidad, formación, contingencia, abstención y escalado quedan explícitos para el uso previsto."
    ],
    "estimated_duration_minutes": 240,
    "status": "curated_pending_expert_review",
})

new_source_ids = [
    "chouldechova-fairness-2017",
    "lundberg-lee-shap-2017",
    "ghassemi-xai-healthcare-2021",
    "parasuraman-manzey-automation-2010",
    "adebayo-saliency-sanity-2018",
]
for sid in new_source_ids:
    if sid not in unit["source_ids"]:
        unit["source_ids"].append(sid)
unit["claim_ids"] = [f"MLBIO-U07-C{i:03d}" for i in range(1, 15)]
save(unit_path, unit)

assessment_path = COURSE / "assessments" / "unit-07.json"
assessment = load(assessment_path)
assessment["purpose"] = "Evaluar si el estudiante puede distinguir sesgo, aplicabilidad e inequidad, auditar subgrupos, proxies y explicaciones y diseñar una evaluación segura del equipo humano-IA."
assessment["status"] = "curated_pending_expert_review"
assessment["items"] = [
    {
        "id": "MLBIO-U07-Q01", "type": "case_analysis",
        "prompt": "Un modelo se desarrolló con procedimientos reproducibles y se evalúa en una cohorte externa, pero el desenlace fue adjudicado por revisores que conocían la predicción. Distinga calidad del desarrollo, riesgo de sesgo de la evaluación y aplicabilidad, y proponga una acción.",
        "linked_learning_outcome_ids": ["MLBIO-U07-LO01", "MLBIO-U07-LO02"], "difficulty": "advanced", "cognitive_level": "analyze",
        "answer_key": {"expected_answer": "La calidad del desarrollo puede ser alta, pero conocer la predicción al adjudicar el desenlace introduce riesgo de sesgo en la evaluación. La aplicabilidad se juzga aparte comparando población, predictores, desenlace y entorno con el uso previsto. Debe repetirse o complementar la evaluación con adjudicación cegada o una referencia independiente y limitar la conclusión actual.", "explanation": "PROBAST+AI separa el proceso que produjo el modelo, la validez de la estimación de desempeño y la correspondencia con el uso objetivo.", "common_misconceptions": ["Convertir todos los dominios en una puntuación única.", "Suponer que un buen desarrollo garantiza una evaluación sin sesgo."]},
        "feedback": {"correct": "Ha separado los tres juicios y ha propuesto una corrección accionable.", "incorrect": "Pregunte por separado cómo se desarrolló el modelo, cómo se obtuvo la estimación de desempeño y si ese estudio representa el uso previsto."},
        "source_ids": ["probast-ai"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U07-Q02", "type": "case_analysis",
        "prompt": "Una validación rigurosa en un centro oncológico terciario muestra buena calibración y bajo riesgo de sesgo. Se pretende desplegar el modelo en atención primaria. ¿Puede considerarse aplicable? Diseñe la comprobación necesaria.",
        "linked_learning_outcome_ids": ["MLBIO-U07-LO01", "MLBIO-U07-LO02"], "difficulty": "intermediate", "cognitive_level": "evaluate",
        "answer_key": {"expected_answer": "No automáticamente. Bajo riesgo de sesgo indica que la estimación en el centro terciario puede ser válida, pero la aplicabilidad exige correspondencia con población, prevalencia, medición de predictores, definición del desenlace, flujo y decisión de atención primaria. Se necesita una evaluación externa relevante y una auditoría de diferencias de proceso antes de generalizar.", "explanation": "Validez interna de la evidencia y transportabilidad al uso previsto son dimensiones distintas.", "common_misconceptions": ["Usar bajo riesgo de sesgo como sinónimo de universalidad.", "Considerar suficiente que ambos entornos pertenezcan al mismo sistema de salud."]},
        "feedback": {"correct": "Ha limitado correctamente la aplicabilidad al contexto evaluado.", "incorrect": "Compare explícitamente quiénes son los pacientes, cómo se miden los predictores, qué desenlace se confirma y qué acción se toma en ambos entornos."},
        "source_ids": ["probast-ai", "tripod-ai"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U07-Q03", "type": "case_analysis",
        "prompt": "La sensibilidad es 0,86 en un grupo con 240 eventos y 0,61 en otro con 12 eventos. Un informe declara inequidad porque la diferencia es 0,25. Evalúe la conclusión y describa qué debe añadirse.",
        "linked_learning_outcome_ids": ["MLBIO-U07-LO03"], "difficulty": "advanced", "cognitive_level": "evaluate",
        "answer_key": {"expected_answer": "La diferencia es una señal que merece investigación, pero la segunda estimación tendrá gran incertidumbre con solo 12 eventos. Deben mostrarse intervalos, denominadores, mezcla de casos, prevalencia, medición y consecuencias del error; además revisar casos individuales y replicar en más datos. No significación tampoco demostraría igualdad. La inequidad clínica requiere conectar la brecha con daño y mecanismo, no solo con una resta puntual.", "explanation": "Los análisis de subgrupos son estimaciones sujetas a varianza, confusión por case mix y diferencias de proceso.", "common_misconceptions": ["Declarar inequidad solo por una diferencia de puntos.", "Descartar una brecha porque el intervalo sea amplio."]},
        "feedback": {"correct": "Ha tratado la brecha como señal con incertidumbre y contexto.", "incorrect": "Antes de etiquetar inequidad, cuantifique cuánta información contiene cada grupo y qué mecanismos alternativos pueden producir la diferencia."},
        "source_ids": ["tripod-ai", "probast-ai"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U07-Q04", "type": "case_analysis",
        "prompt": "Dos grupos tienen prevalencias distintas. El equipo exige simultáneamente calibración dentro de cada grupo, igual PPV e iguales tasas de falsos positivos y falsos negativos. Explique por qué esos objetivos pueden entrar en conflicto y cómo elegir un criterio clínicamente defendible.",
        "linked_learning_outcome_ids": ["MLBIO-U07-LO02", "MLBIO-U07-LO03"], "difficulty": "advanced", "cognitive_level": "evaluate",
        "answer_key": {"expected_answer": "Cuando los riesgos basales difieren y la predicción no es perfecta, varios criterios de fairness no pueden satisfacerse simultáneamente. Debe elegirse qué error o consecuencia importa para la decisión clínica, justificarlo con pacientes y usuarios, reportar las métricas que entran en tensión y evaluar efectos de cualquier umbral específico por grupo. Fairness no es una propiedad escalar universal.", "explanation": "Los criterios matemáticos codifican objetivos distintos; elegir uno implica una prioridad normativa y clínica.", "common_misconceptions": ["Buscar una única métrica técnica que resuelva equidad.", "Cambiar umbrales por grupo sin revisar consecuencias éticas, legales y operativas."]},
        "feedback": {"correct": "Ha reconocido incompatibilidad y necesidad de justificar el criterio por daño y decisión.", "incorrect": "Identifique qué cantidad intenta igualar cada métrica y qué ocurre cuando las prevalencias son distintas."},
        "source_ids": ["chouldechova-fairness-2017"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U07-Q05", "type": "case_analysis",
        "prompt": "Se elimina la variable de seguro médico para reducir sesgo, pero permanecen hospital, código postal, frecuencia de pruebas y vía de ingreso. El desempeño por grupos apenas cambia. Interprete el resultado y diseñe una auditoría de proxies y atajos.",
        "linked_learning_outcome_ids": ["MLBIO-U07-LO04"], "difficulty": "advanced", "cognitive_level": "create",
        "answer_key": {"expected_answer": "Eliminar una variable sensible o social no elimina la información correlacionada. Hospital, código postal, frecuencia de medición o vía de ingreso pueden actuar como proxies de acceso o proceso. Deben revisar procedencia, correlaciones y distribuciones, perturbar o ablar señales, validar entre centros y periodos y examinar errores clínicamente. Una señal puede ser predictiva y aun ser inestable o reproducir desigualdades.", "explanation": "Los modelos pueden aprender el proceso de atención además de la biología; retirar una columna no borra señales redundantes.", "common_misconceptions": ["Asumir fairness through unawareness.", "Considerar toda variable proxy automáticamente ilegítima sin analizar uso, estabilidad y daño."]},
        "feedback": {"correct": "Ha transformado el hallazgo en pruebas concretas de proxy y atajo.", "incorrect": "Pregunte qué otras variables permiten reconstruir indirectamente la información retirada y si esas señales se mantienen al cambiar el entorno."},
        "source_ids": ["agniel-ehr-process-bias-2018", "degrave-shortcuts-covid-cxr-2021"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U07-Q06", "type": "case_analysis",
        "prompt": "Una explicación SHAP local asigna gran contribución a creatinina y edad. El equipo concluye que ambas variables causan el riesgo y que el modelo razona como un nefrólogo. Corrija la interpretación y especifique qué debe auditarse antes de mostrar esa explicación a usuarios.",
        "linked_learning_outcome_ids": ["MLBIO-U07-LO05"], "difficulty": "advanced", "cognitive_level": "analyze",
        "answer_key": {"expected_answer": "SHAP atribuye una predicción del modelo respecto de una referencia bajo supuestos del método; no identifica efectos causales ni reproduce razonamiento humano. Deben documentarse baseline o referencia, dependencia entre variables, fidelidad, estabilidad ante perturbaciones y si la explicación ayuda a la tarea prevista sin aumentar confianza injustificada. La validez predictiva del modelo sigue requiriendo evaluación independiente.", "explanation": "Una explicación post hoc describe comportamiento del predictor; la causalidad exige un diseño y supuestos distintos.", "common_misconceptions": ["Convertir contribución SHAP en efecto biológico causal.", "Suponer que una explicación plausible es fiel o útil por ser intuitiva."]},
        "feedback": {"correct": "Ha limitado SHAP a atribución del modelo y ha definido pruebas de explicación.", "incorrect": "Separe tres preguntas: qué predijo el modelo, qué atribuye el método de explicación y qué evidencia demostraría una causa real."},
        "source_ids": ["lundberg-lee-shap-2017", "ghassemi-xai-healthcare-2021"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U07-Q07", "type": "case_analysis",
        "prompt": "Un mapa de saliencia parece clínicamente plausible incluso después de aleatorizar los pesos del modelo. ¿Qué implica este resultado y qué principio general debe aplicarse a explicaciones visuales?",
        "linked_learning_outcome_ids": ["MLBIO-U07-LO05"], "difficulty": "advanced", "cognitive_level": "evaluate",
        "answer_key": {"expected_answer": "Si la explicación permanece similar al aleatorizar el modelo, puede no reflejar lo que el predictor aprendió y falla una prueba de fidelidad básica. La apariencia plausible no basta. Deben aplicarse sanity checks, perturbaciones y comparaciones que prueben dependencia del modelo y de los datos antes de usar la visualización para depuración o confianza clínica.", "explanation": "Las explicaciones pueden ser visualmente convincentes sin estar conectadas al comportamiento aprendido del modelo.", "common_misconceptions": ["Validar explicaciones por inspección visual de expertos únicamente.", "Interpretar estabilidad frente a aleatorización como una virtud."]},
        "feedback": {"correct": "Ha reconocido que plausibilidad visual y fidelidad son propiedades distintas.", "incorrect": "Una explicación debe cambiar cuando cambia de forma sustancial aquello que supuestamente explica; si no lo hace, cuestione su fidelidad."},
        "source_ids": ["adebayo-saliency-sanity-2018"], "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U07-Q08", "type": "case_analysis",
        "prompt": "Un sistema de alerta reduce tiempo de decisión, pero los clínicos aceptan el 96% de recomendaciones incluso en casos adversariales donde el modelo se equivoca. Diseñe una evaluación del equipo humano-IA y una mitigación segura.",
        "linked_learning_outcome_ids": ["MLBIO-U07-LO06"], "difficulty": "advanced", "cognitive_level": "create",
        "answer_key": {"expected_answer": "El patrón sugiere automatización o dependencia excesiva. Debe compararse profesional solo, modelo solo y equipo combinado en casos representativos y difíciles; medir exactitud, omisiones, comisiones, tiempo, confianza, discrepancias y recuperación. La mitigación puede incluir interfaz que muestre límites, formación, fricción o revisión en casos de riesgo, abstención y escalado, pero debe probarse empíricamente porque más explicación no garantiza menos automatización.", "explanation": "El desempeño clínico emerge de la interacción entre usuarios, interfaz, tarea y modelo; no es suma automática de dos precisiones independientes.", "common_misconceptions": ["Interpretar mayor velocidad como mejora neta del sistema.", "Añadir explicaciones y asumir que con ello desaparece el sesgo de automatización."]},
        "feedback": {"correct": "Ha diseñado una prueba del equipo y una mitigación evaluable.", "incorrect": "Mida no solo si el modelo acierta, sino qué hace la persona cuando el modelo se equivoca y qué elementos de interfaz cambian esa conducta."},
        "source_ids": ["parasuraman-manzey-automation-2010", "decide-ai", "imdrf-fda-gmlp"], "status": "curated_pending_expert_review"
    }
]
save(assessment_path, assessment)

sources_path = COURSE / "sources.json"
sources_doc = load(sources_path)
known = {s["id"] for s in sources_doc["sources"]}
new_sources = [
    {"registry_id":"chouldechova-fairness-2017","id":"chouldechova-fairness-2017","title":"Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments","authors":["Alexandra Chouldechova"],"organization":"Big Data","year":2017,"url":"https://pubmed.ncbi.nlm.nih.gov/28632438/","doi":"10.1089/big.2016.0047","type":"artículo metodológico","verification_status":"verified_directly","locator":"Abstract; theoretical results on calibration and error-rate criteria, pp. 153–163","role":"Demuestra incompatibilidades entre criterios de fairness cuando las prevalencias difieren y la predicción no es perfecta.","curricular_function":"Fundamentar que fairness no se resuelve con una única métrica y que elegir un criterio implica prioridades sobre errores y consecuencias.","limitations":"El caso aplicado es recidivismo y no atención sanitaria; el resultado matemático orienta tensiones entre métricas, pero no determina qué criterio ético o clínico debe adoptarse.","used_by_unit_ids":["MLBIO-U07"]},
    {"registry_id":"lundberg-lee-shap-2017","id":"lundberg-lee-shap-2017","title":"A Unified Approach to Interpreting Model Predictions","authors":["Scott M. Lundberg","Su-In Lee"],"organization":"Advances in Neural Information Processing Systems","year":2017,"url":"https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html","type":"artículo metodológico","verification_status":"verified_directly","locator":"Abstract; Sections 2–4, NeurIPS 2017","role":"Introduce SHAP como marco de atribución aditiva de características para explicar predicciones de modelos.","curricular_function":"Definir qué representa una contribución SHAP y separar atribución del modelo de inferencia causal o razonamiento clínico humano.","limitations":"El marco explica predicciones del modelo bajo una referencia y supuestos; no identifica causas ni garantiza utilidad clínica, fidelidad práctica o estabilidad en todas las implementaciones.","used_by_unit_ids":["MLBIO-U07"]},
    {"registry_id":"ghassemi-xai-healthcare-2021","id":"ghassemi-xai-healthcare-2021","title":"The false hope of current approaches to explainable artificial intelligence in health care","authors":["Marzyeh Ghassemi","Luke Oakden-Rayner","Andrew L. Beam"],"organization":"The Lancet Digital Health","year":2021,"url":"https://pubmed.ncbi.nlm.nih.gov/34711379/","doi":"10.1016/S2589-7500(21)00208-9","type":"viewpoint metodológico clínico","verification_status":"verified_directly","locator":"Summary and discussion, pp. e745–e750","role":"Analiza limitaciones de explicaciones post hoc en salud y advierte que no garantizan confianza apropiada, transparencia, mitigación de sesgo ni seguridad.","curricular_function":"Evitar usar explicabilidad como sustituto de validación y exigir que una explicación se evalúe por la tarea y consecuencias para usuarios clínicos.","limitations":"Es un Viewpoint argumentativo, no un ensayo de una técnica concreta; sus advertencias deben combinarse con evidencia empírica específica del método y tarea.","used_by_unit_ids":["MLBIO-U07"]},
    {"registry_id":"parasuraman-manzey-automation-2010","id":"parasuraman-manzey-automation-2010","title":"Complacency and bias in human use of automation: an attentional integration","authors":["Raja Parasuraman","Dietrich H. Manzey"],"organization":"Human Factors","year":2010,"url":"https://pubmed.ncbi.nlm.nih.gov/21077562/","doi":"10.1177/0018720810376055","type":"revisión y modelo teórico de factores humanos","verification_status":"verified_directly","locator":"Abstract; review of automation complacency and automation bias, pp. 381–410","role":"Revisa evidencia sobre complacencia y sesgo de automatización y los relaciona con atención, carga de tarea y dependencia del sistema.","curricular_function":"Fundamentar la evaluación de aceptación excesiva, omisiones, comisiones y recuperación cuando profesionales trabajan con apoyo automatizado.","limitations":"La revisión abarca dominios de automatización diversos y no se limita a IA clínica; la magnitud y forma del efecto deben medirse en el flujo sanitario concreto.","used_by_unit_ids":["MLBIO-U07"]},
    {"registry_id":"adebayo-saliency-sanity-2018","id":"adebayo-saliency-sanity-2018","title":"Sanity Checks for Saliency Maps","authors":["Julius Adebayo","Justin Gilmer","Michael Muelly","Ian Goodfellow","Moritz Hardt","Been Kim"],"organization":"Advances in Neural Information Processing Systems","year":2018,"url":"https://papers.neurips.cc/paper_files/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html","type":"artículo metodológico experimental","verification_status":"verified_directly","locator":"Abstract; model-parameter and data-randomization tests, NeurIPS 2018","role":"Propone pruebas de sanidad para explicaciones visuales y muestra que algunas saliency maps pueden ser poco dependientes del modelo o datos aprendidos.","curricular_function":"Sustentar que plausibilidad visual no demuestra fidelidad y que explicaciones deben someterse a pruebas perturbacionales.","limitations":"Se centra en métodos de saliencia sobre modelos e imágenes concretas; no demuestra que todo método de explicación falle ni sustituye validación específica de SHAP u otras técnicas.","used_by_unit_ids":["MLBIO-U07"]}
]
for src in new_sources:
    if src["id"] not in known:
        sources_doc["sources"].append(src)
save(sources_path, sources_doc)

glossary_path = COURSE / "glossary.json"
glossary = load(glossary_path)
updates = {
    "MLBIO-GLO-071": ("Posibilidad de que una estimación de desempeño esté sistemáticamente distorsionada por el diseño, medición, análisis o evaluación; debe distinguirse de aplicabilidad y de la calidad del proceso de desarrollo.", ["probast-ai"], [("probast-ai","Domains for risk of bias, quality and applicability")]),
    "MLBIO-GLO-072": ("Conjunto de criterios y decisiones normativas usados para examinar cómo desempeño, errores, calibración y consecuencias se distribuyen entre grupos; varios criterios pueden ser incompatibles cuando los riesgos basales difieren.", ["chouldechova-fairness-2017"], [("chouldechova-fairness-2017","Abstract and theoretical results")]),
    "MLBIO-GLO-073": ("Variable o señal que porta indirectamente información sobre otra característica o proceso, como acceso, centro o práctica clínica, y puede permitir al modelo reconstruir información no incluida explícitamente.", ["agniel-ehr-process-bias-2018","degrave-shortcuts-covid-cxr-2021"], [("agniel-ehr-process-bias-2018","Healthcare-process analyses"),("degrave-shortcuts-covid-cxr-2021","Results and Discussion on source-specific shortcuts")]),
    "MLBIO-GLO-074": ("Grado en que la estructura, parámetros o relaciones de un modelo pueden ser comprendidos directamente por una audiencia definida; no implica causalidad ni utilidad clínica por sí mismo.", ["ghassemi-xai-healthcare-2021"], [("ghassemi-xai-healthcare-2021","Overview and limitations of explainability approaches")]),
    "MLBIO-GLO-075": ("Conjunto de métodos que generan representaciones sobre el comportamiento o una predicción de un modelo; su fidelidad, estabilidad y utilidad deben evaluarse para la tarea concreta.", ["ghassemi-xai-healthcare-2021","adebayo-saliency-sanity-2018"], [("ghassemi-xai-healthcare-2021","Summary and discussion"),("adebayo-saliency-sanity-2018","Abstract and sanity-check methodology")]),
    "MLBIO-GLO-076": ("SHapley Additive exPlanations: marco de atribución aditiva que asigna a cada característica una contribución a una predicción respecto de una referencia bajo los supuestos del método.", ["lundberg-lee-shap-2017"], [("lundberg-lee-shap-2017","Abstract and additive feature attribution framework")]),
    "MLBIO-GLO-077": ("Conducta predefinida por la que el sistema no emite una recomendación accionable o exige revisión cuando la entrada, cobertura o incertidumbre no satisfacen condiciones de uso.", ["imdrf-fda-gmlp","fda-transparency-mlmd"], [("imdrf-fda-gmlp","Guiding principles on intended use, performance and monitoring"),("fda-transparency-mlmd","Relevant information on limitations and workflow")]),
    "MLBIO-GLO-078": ("Tendencia a favorecer una recomendación automatizada y omitir o cometer errores cuando el sistema se equivoca, especialmente bajo determinadas condiciones de atención, carga o confianza.", ["parasuraman-manzey-automation-2010"], [("parasuraman-manzey-automation-2010","Abstract and review of automation bias")]),
    "MLBIO-GLO-079": ("Propiedades de usuarios, tareas, interfaz, organización y entorno que modifican cómo se interpreta y usa un sistema y, por tanto, su desempeño y seguridad reales.", ["decide-ai"], [("decide-ai","Checklist and explanation on human factors and clinical workflow")]),
    "MLBIO-GLO-080": ("Sistema sociotécnico formado por modelo, usuarios, interfaz, reglas de uso y flujo clínico cuyo desempeño puede diferir del observado para el algoritmo o el profesional por separado.", ["imdrf-fda-gmlp","decide-ai"], [("imdrf-fda-gmlp","Guiding principle on human-AI team performance"),("decide-ai","Human factors and early clinical evaluation")]),
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
claims_doc["scope"] = "Afirmaciones centrales de las Unidades 1–7 con fuente primaria o metodológica, localizador, alcance y revisión humana pendiente."
claims_doc["claims"] = [c for c in claims_doc["claims"] if c.get("unit") != 7]
specs = [
    ("PROBAST+AI distingue la calidad del proceso de desarrollo de la estimación del riesgo de sesgo en la evaluación del desempeño.","definition","high","probast-ai","Quality, risk of bias and applicability framework"),
    ("La aplicabilidad pregunta si la población, predictores, desenlace y contexto corresponden al uso previsto.","definition","high","probast-ai","Applicability domains"),
    ("La auditoría se realiza con preguntas de señalización y justificación, no como puntuación decorativa.","methodological_requirement","medium","probast-ai","Signalling questions and domain judgements"),
    ("Una diferencia puntual puede deberse al azar, mezcla de casos, medición o acceso.","interpretation_boundary","high","tripod-ai","Subgroup performance and uncertainty reporting"),
    ("Las métricas de fairness pueden ser incompatibles.","methodological_interpretation","high","chouldechova-fairness-2017","Abstract and theoretical results"),
    ("Eliminar una variable sensible no elimina necesariamente la información asociada.","interpretation_boundary","high","agniel-ehr-process-bias-2018","Healthcare-process signals and correlated information"),
    ("Los proxies y atajos aparecen cuando el modelo utiliza señales correlacionadas con el desenlace pero no estables o no deseadas: hospital, equipo, idioma, seguro, frecuencia de medición o marcas de documentación.","definition","high","degrave-shortcuts-covid-cxr-2021","Source-specific shortcuts and discussion"),
    ("La interpretabilidad puede referirse a una estructura comprensible, mientras la explicabilidad suele describir métodos que resumen el comportamiento de un modelo.","definition","medium","ghassemi-xai-healthcare-2021","Overview of explainability approaches"),
    ("Ninguna explicación demuestra que el modelo haya identificado un mecanismo biológico ni que su razonamiento sea equivalente al de un profesional.","interpretation_boundary","high","ghassemi-xai-healthcare-2021","Limitations and failure cases of XAI in health care"),
    ("Las explicaciones dependen del modelo, la distribución de referencia y las correlaciones.","methodological_caution","high","lundberg-lee-shap-2017","Additive feature attribution framework and reference assumptions"),
    ("Una probabilidad predicha no es automáticamente una medida de incertidumbre epistemológica.","interpretation_boundary","high","imdrf-fda-gmlp","Performance limitations and intended use"),
    ("En clínica, el objeto de evaluación suele ser el equipo humano-IA.","decision_principle","high","imdrf-fda-gmlp","Guiding principle on human-AI team performance"),
    ("El sesgo de automatización ocurre cuando se acepta una recomendación incorrecta por confianza excesiva.","definition","high","parasuraman-manzey-automation-2010","Automation bias review"),
    ("Las interfaces y explicaciones se prueban con usuarios previstos.","methodological_requirement","high","decide-ai","Human factors and intended users")
]
for i, (text, ctype, risk, sid, locator) in enumerate(specs, start=1):
    cid = f"MLBIO-U07-C{i:03d}"
    claims_doc["claims"].append({"claim_id":cid,"unit":7,"text":text,"claim_type":ctype,"risk":risk,"context":"Aplicado a evaluación de IA clínica; la conclusión concreta depende de población, uso previsto, grupos, interfaz, usuarios y diseño de evaluación.","source_id":sid,"locator":{"section":locator},"support":"direct" if ctype in {"definition","methodological_interpretation"} else "indirect","source_verification_status":"verified_directly","review_state":"ai_review_provisional","reviewer_validation_id":None,"reviewed_at":DATE,"id":cid,"unit_id":"MLBIO-U07"})
save(claims_path, claims_doc)

test_path = ROOT / "tests" / "test_academic_course_schema.py"
text = test_path.read_text(encoding="utf-8")
text = text.replace('self.assertEqual(report.counts["claims"], 84)', 'self.assertEqual(report.counts["claims"], 98)')
text = text.replace('for unit_number in (1, 2, 3, 4, 5, 6):', 'for unit_number in (1, 2, 3, 4, 5, 6, 7):')
text = text.replace('{"MLBIO-U02", "MLBIO-U03", "MLBIO-U04", "MLBIO-U05", "MLBIO-U06"}.intersection', '{"MLBIO-U02", "MLBIO-U03", "MLBIO-U04", "MLBIO-U05", "MLBIO-U06", "MLBIO-U07"}.intersection')
if "test_renderer_includes_curated_machine_learning_unit_7" not in text:
    marker = "    def test_every_assessment_item_maps_to_a_unit_outcome(self) -> None:\n"
    addition = '''    def test_renderer_includes_curated_machine_learning_unit_7(self) -> None:\n        unit = RENDERER.load_advanced_unit(ROOT, "machine-learning-biomedico-validacion-clinica", 7)\n        self.assertIsNotNone(unit)\n        assert unit is not None\n        self.assertEqual(unit["schema_version"], "canonical-1.0")\n        self.assertEqual(unit["unit"], 7)\n        self.assertEqual(unit["title"], "Sesgo, equidad, explicabilidad y equipo humano-IA")\n        self.assertEqual(len(unit["self_assessment"]), 8)\n        self.assertEqual(len(unit["guided_activities"][0]["deliverables"]), 6)\n        self.assertEqual(unit["guided_activities"][0]["estimated_duration_minutes"], 240)\n        self.assertEqual(len(unit["guided_activities"][0]["checking_criteria"]), 10)\n\n'''
    if marker not in text:
        raise RuntimeError("No se encontró punto de inserción U07")
    text = text.replace(marker, addition + marker)
test_path.write_text(text, encoding="utf-8")

print("Unidad 7 curada: teoría, actividad, evaluación, glosario, fuentes, claims y regresiones actualizados.")
