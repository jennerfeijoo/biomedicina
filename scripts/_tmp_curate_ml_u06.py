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


unit_path = COURSE / "units" / "unit-06.json"
unit = load(unit_path)
unit["prerequisite_unit_ids"] = [f"MLBIO-U0{i}" for i in range(1, 6)]

# Repair two inherited heading/content mismatches in the calibration topic.
calibration_topic = next(t for t in unit["topics"] if t["id"] == "MLBIO-U06-T03")
subtopics = {s["id"]: s for s in calibration_topic["subtopics"]}
subtopics["MLBIO-U06-T03-ST02"]["title"] = "Brier y log-loss evalúan probabilidades pero dependen del contexto"
subtopics["MLBIO-U06-T03-ST03"]["title"] = "La calibración puede variar por población, tiempo y subgrupo"

activity = unit["activities"][0]
activity.update({
    "purpose": "Construir un informe multidimensional de desempeño que conecte discriminación, calibración, prevalencia, umbrales, net benefit y capacidad asistencial con una decisión clínica explícita.",
    "prerequisite_unit_ids": [f"MLBIO-U0{i}" for i in range(1, 6)],
    "instructions": [
        "Definir el uso previsto, la prevalencia observada y al menos dos umbrales clínicamente plausibles, indicando qué acción activa cada uno y qué consecuencias tienen falsos positivos y falsos negativos.",
        "Construir para cada umbral la matriz de confusión y derivar sensibilidad, especificidad, PPV y NPV con denominadores explícitos; traducir los resultados a eventos y alertas por cada 100 o 1000 pacientes.",
        "Evaluar discriminación mediante ROC/AUC y precision-recall, justificando qué información aporta cada representación y cómo la prevalencia y la mezcla de casos condicionan su interpretación.",
        "Evaluar probabilidades con curva de calibración, calibración en el grande, pendiente y Brier score frente a un referente; localizar si el error es global o concentrado en rangos de riesgo.",
        "Comparar modelo, práctica habitual, treat-all y treat-none mediante net benefit en un rango de umbrales relevante, incorporando capacidad operativa y redactando una conclusión que separe utilidad estimada de impacto clínico demostrado."
    ],
    "tasks": [
        "Construir matrices de confusión para dos umbrales sobre la misma cohorte y explicar qué pacientes cambian de acción al mover el punto de corte.",
        "Calcular PPV y NPV cuando la prevalencia cambia manteniendo sensibilidad y especificidad constantes, e interpretar por qué no deben transportarse valores predictivos sin más.",
        "Comparar ROC y precision-recall para un evento del 2% y explicar por qué una AUC alta puede coexistir con una carga elevada de falsos positivos.",
        "Interpretar una AUC de 0,90 sin convertirla en una afirmación sobre calibración, utilidad, causalidad o beneficio para pacientes.",
        "Calcular Brier score del modelo y de un referente que predice riesgo basal para todos, explicando qué información añade y qué no localiza el promedio.",
        "Interpretar conjuntamente una curva de calibración, calibración en el grande y pendiente, distinguiendo sobrepredicción global de predicciones demasiado extremas.",
        "Calcular net benefit para un umbral y compararlo con treat-all, treat-none y la alternativa clínica real, explicitando la ponderación implícita entre falsos positivos y falsos negativos.",
        "Traducir la opción de umbral elegida a alertas, verdaderos positivos, falsos positivos, evaluaciones adicionales y capacidad requerida por cada 1000 pacientes."
    ],
    "deliverables": [
        "Ficha del escenario con uso previsto, población, prevalencia, acción clínica, alternativa real y rango de umbrales justificable.",
        "Tabla de desempeño por umbral con TP, FP, TN, FN, sensibilidad, especificidad, PPV, NPV e intervalos o incertidumbre cuando corresponda.",
        "Comparación de discriminación con ROC/AUC y precision-recall acompañada de una interpretación que incluya prevalencia y mezcla de casos.",
        "Panel de calibración con curva, calibración en el grande, pendiente y Brier score frente a un referente, señalando dónde aparecen los principales errores probabilísticos.",
        "Análisis de decision curve con net benefit del modelo, treat-all, treat-none y práctica habitual en el rango de umbrales clínicamente relevante.",
        "Conclusión operacional que seleccione o rechace un umbral y traduzca la decisión a carga asistencial, limitaciones y evidencia prospectiva todavía necesaria."
    ],
    "checking_criteria": [
        "La prevalencia y los denominadores de cada métrica están explícitos y corresponden a la cohorte evaluada.",
        "Sensibilidad, especificidad, PPV y NPV se interpretan para un umbral concreto y no como propiedades universales del algoritmo.",
        "La AUC se describe como discriminación o ranking y no se usa como sustituto de calibración o utilidad.",
        "La precision-recall se interpreta reconociendo que su baseline y precisión dependen de la prevalencia del evento.",
        "La calibración incluye una representación gráfica y medidas complementarias; no se reduce a una prueba global de bondad de ajuste.",
        "El Brier score se compara con un referente pertinente y no se interpreta aisladamente entre poblaciones con prevalencias distintas.",
        "Los umbrales se justifican por acciones, consecuencias y capacidad, no solo por Youden, F1 u optimización retrospectiva.",
        "El net benefit se compara con treat-all, treat-none y la alternativa clínica real dentro de un rango plausible de umbrales.",
        "La carga operativa se expresa como números de alertas, evaluaciones o intervenciones además de métricas abstractas.",
        "La conclusión distingue utilidad retrospectiva estimada de impacto clínico prospectivo demostrado."
    ],
    "estimated_duration_minutes": 240,
    "status": "curated_pending_expert_review",
})

new_source_ids = [
    "steyerberg-performance-2010",
    "van-calster-calibration-2019",
    "saito-rehmsmeier-pr-2015",
    "vickers-elkin-dca-2006",
]
for sid in new_source_ids:
    if sid not in unit["source_ids"]:
        unit["source_ids"].append(sid)
unit["claim_ids"] = [f"MLBIO-U06-C{i:03d}" for i in range(1, 15)]
save(unit_path, unit)

# Assessment: eight applied cases, with all six outcomes covered.
assessment_path = COURSE / "assessments" / "unit-06.json"
assessment = load(assessment_path)
assessment["purpose"] = "Evaluar si el estudiante puede interpretar desempeño predictivo de forma multidimensional, elegir umbrales por consecuencias y capacidad y usar decision curve analysis sin confundir utilidad estimada con impacto clínico demostrado."
assessment["status"] = "curated_pending_expert_review"
assessment["items"] = [
    {
        "id": "MLBIO-U06-Q01",
        "type": "case_analysis",
        "prompt": "Un modelo de sepsis se evalúa en 1000 pacientes: 100 presentan el evento. Con umbral 0,20 detecta 80 eventos y genera 180 falsos positivos. Calcule sensibilidad, especificidad y PPV. Después explique qué ocurriría con el PPV si sensibilidad y especificidad se mantuvieran pero la prevalencia bajara al 2%.",
        "linked_learning_outcome_ids": ["MLBIO-U06-LO01"],
        "difficulty": "intermediate",
        "cognitive_level": "apply",
        "answer_key": {
            "expected_answer": "TP=80, FN=20, FP=180 y TN=720. Sensibilidad=80/100=0,80; especificidad=720/900=0,80; PPV=80/260≈0,308. Si la prevalencia baja al 2% manteniendo sensibilidad y especificidad, la mayoría de positivos disponibles son no eventos y el PPV cae de forma marcada. Por ello los valores predictivos deben estimarse en la población objetivo y no transportarse como constantes.",
            "explanation": "Sensibilidad y especificidad condicionan el clasificador en un umbral, mientras PPV y NPV incorporan la frecuencia del evento en la población evaluada.",
            "common_misconceptions": ["Confundir PPV con sensibilidad.", "Suponer que PPV permanece fijo cuando cambia la prevalencia."]
        },
        "feedback": {"correct": "Ha conectado la matriz de confusión con prevalencia y valores predictivos.", "incorrect": "Reconstruya primero TP, FN, FP y TN; después pregunte qué proporción de predicciones positivas puede ser verdadera cuando el evento es mucho menos frecuente."},
        "source_ids": ["steyerberg-performance-2010"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U06-Q02",
        "type": "case_analysis",
        "prompt": "Dos modelos para un evento del 1% tienen AUC ROC 0,92 y 0,90. En el umbral operativo, el primero produce PPV 6% y el segundo 14% con sensibilidad similar. ¿Puede declararse superior el modelo de AUC 0,92? Diseñe la comparación que falta.",
        "linked_learning_outcome_ids": ["MLBIO-U06-LO02", "MLBIO-U06-LO04"],
        "difficulty": "advanced",
        "cognitive_level": "evaluate",
        "answer_key": {
            "expected_answer": "No. La diferencia de AUC resume ranking global y no determina por sí sola el rendimiento en el rango operativo. Deben compararse curvas precision-recall, desempeño e incertidumbre en umbrales clínicos, calibración, número de alertas y utilidad. En un evento raro, el PPV y la curva PR hacen visible la proporción de alertas verdaderas que puede quedar oculta por una ROC aparentemente excelente.",
            "explanation": "La ROC pondera sensibilidad frente a tasa de falsos positivos; con muchos no eventos una tasa pequeña puede generar gran número absoluto de falsos positivos.",
            "common_misconceptions": ["Elegir automáticamente el mayor AUC.", "Interpretar una AUC elevada como PPV elevado."]
        },
        "feedback": {"correct": "Ha situado ROC/AUC dentro del problema operativo y ha añadido PR y umbrales.", "incorrect": "Compare qué responde AUC con lo que necesita el servicio: cuántas alertas son verdaderas y qué ocurre en el umbral que activa una acción."},
        "source_ids": ["saito-rehmsmeier-pr-2015", "steyerberg-performance-2010"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U06-Q03",
        "type": "case_analysis",
        "prompt": "Un modelo conserva AUC 0,84, pero su curva de calibración muestra sobrepredicción en casi todo el rango. La calibración en el grande es -0,35 y la pendiente 1,02. Interprete cada hallazgo y explique por qué el AUC no detecta el problema.",
        "linked_learning_outcome_ids": ["MLBIO-U06-LO03"],
        "difficulty": "advanced",
        "cognitive_level": "analyze",
        "answer_key": {
            "expected_answer": "La discriminación sigue siendo razonable porque el ranking se mantiene. El intercepto negativo en la parametrización logística habitual indica sobrepredicción global; la pendiente cercana a uno sugiere que la extensión global de las predicciones no está muy deformada. La curva confirma dónde ocurre el desajuste. AUC solo depende del orden relativo y puede permanecer idéntica aunque todas las probabilidades se desplacen sistemáticamente.",
            "explanation": "Ranking y calibración son dimensiones diferentes; una transformación monotónica puede conservar el orden y cambiar las probabilidades absolutas.",
            "common_misconceptions": ["Concluir que AUC estable implica probabilidades fiables.", "Usar intercepto y pendiente como sustituto completo de la curva de calibración."]
        },
        "feedback": {"correct": "Ha separado discriminación, nivel medio de riesgo, pendiente y forma de la curva.", "incorrect": "Pregunte qué métricas cambiarían si todos los riesgos se multiplicaran o desplazaran manteniendo exactamente el mismo orden entre pacientes."},
        "source_ids": ["van-calster-calibration-2019", "steyerberg-performance-2010"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U06-Q04",
        "type": "case_analysis",
        "prompt": "El Brier score de un modelo es 0,071 y el de predecir 0,08 para todos los pacientes es 0,074. Un colega afirma que 0,071 demuestra excelente calibración. Evalúe la afirmación y especifique qué análisis adicionales exigiría.",
        "linked_learning_outcome_ids": ["MLBIO-U06-LO03"],
        "difficulty": "intermediate",
        "cognitive_level": "evaluate",
        "answer_key": {
            "expected_answer": "La afirmación es excesiva. El Brier resume error probabilístico y combina componentes de calibración y discriminación; que mejore modestamente al referente basal no demuestra calibración excelente ni muestra dónde aparecen errores. Deben añadirse curva de calibración, calibración en el grande, pendiente, incertidumbre y distribución de predicciones; la comparación entre poblaciones también requiere cautela porque el Brier depende del contexto y prevalencia.",
            "explanation": "Una métrica promedio puede ser útil para comparar pronósticos probabilísticos, pero no sustituye un diagnóstico de calibración a lo largo del rango de riesgo.",
            "common_misconceptions": ["Interpretar Brier como medida pura de calibración.", "Comparar Brier sin referente o entre poblaciones distintas como si la escala fuera universal."]
        },
        "feedback": {"correct": "Ha usado Brier como componente del panel y no como diagnóstico único.", "incorrect": "Separe la pregunta ‘¿cuánto error probabilístico promedio hay?’ de ‘¿en qué rangos las probabilidades corresponden a frecuencias observadas?’."},
        "source_ids": ["steyerberg-performance-2010", "van-calster-calibration-2019"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U06-Q05",
        "type": "case_analysis",
        "prompt": "Para activar una evaluación clínica se consideran umbrales 0,05, 0,10 y 0,20. El umbral 0,05 maximiza sensibilidad pero genera 420 alertas por cada 1000 pacientes y el servicio solo puede revisar 120. El umbral 0,20 genera 90 alertas pero pierde muchos eventos. ¿Cómo elegiría un rango operativo defendible?",
        "linked_learning_outcome_ids": ["MLBIO-U06-LO04"],
        "difficulty": "advanced",
        "cognitive_level": "evaluate",
        "answer_key": {
            "expected_answer": "No existe un umbral óptimo puramente estadístico. Deben explicitarse consecuencias de falsos negativos y falsos positivos, capacidad disponible, ruta confirmatoria, tiempo de respuesta y alternativa actual. El rango operativo debe excluir opciones inviables por capacidad o daño, y dentro del rango restante comparar sensibilidad, PPV, calibración y net benefit. Si ningún umbral satisface seguridad y capacidad, el modelo no debe forzarse al flujo.",
            "explanation": "Un umbral es una regla de decisión: su valor depende de cuánto daño o beneficio se atribuye a cada error y de si la acción puede ejecutarse.",
            "common_misconceptions": ["Elegir Youden o F1 sin traducirlo a acciones.", "Tratar la capacidad del servicio como problema posterior a la validación."]
        },
        "feedback": {"correct": "Ha integrado consecuencias y capacidad en la selección del umbral.", "incorrect": "Convierta cada umbral en número de alertas y acciones; después determine qué costes clínicos y operativos son aceptables."},
        "source_ids": ["vickers-elkin-dca-2006", "decide-ai"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U06-Q06",
        "type": "case_analysis",
        "prompt": "A un umbral de 10%, un modelo produce 70 verdaderos positivos y 180 falsos positivos en 1000 pacientes. Calcule net benefit con NB=TP/N-(FP/N)×pt/(1-pt) e interprete el resultado frente a treat-none; indique qué comparación adicional falta para decidir si usarlo.",
        "linked_learning_outcome_ids": ["MLBIO-U06-LO05", "MLBIO-U06-LO06"],
        "difficulty": "advanced",
        "cognitive_level": "apply",
        "answer_key": {
            "expected_answer": "NB=0,07-0,18×0,10/0,90=0,07-0,02=0,05. Es superior a treat-none, cuyo net benefit es cero, bajo la ponderación de daños implícita en pt=0,10. Esto no basta: debe compararse también con treat-all y con la práctica habitual o alternativa real en un rango plausible de umbrales, además de comprobar calibración y factibilidad operacional.",
            "explanation": "El umbral traduce la relación de intercambio entre falsos positivos y verdaderos positivos; net benefit solo es interpretable respecto de alternativas.",
            "common_misconceptions": ["Interpretar NB=0,05 como 5% de pacientes beneficiados directamente.", "Comparar solo contra treat-none y declarar utilidad clínica suficiente."]
        },
        "feedback": {"correct": "Ha calculado net benefit y lo ha situado frente a alternativas y supuestos.", "incorrect": "Aplique primero la ponderación pt/(1-pt); después recuerde que una estrategia es útil solo en comparación con otras decisiones disponibles."},
        "source_ids": ["vickers-elkin-dca-2006"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U06-Q07",
        "type": "case_analysis",
        "prompt": "La decision curve de un modelo está por encima de treat-all y treat-none entre 8% y 18%. El artículo concluye que ‘el modelo mejora resultados clínicos’. ¿Qué permite afirmar realmente el análisis y qué evidencia faltaría?",
        "linked_learning_outcome_ids": ["MLBIO-U06-LO05", "MLBIO-U06-LO06"],
        "difficulty": "advanced",
        "cognitive_level": "evaluate",
        "answer_key": {
            "expected_answer": "Puede afirmarse que el modelo presenta mayor net benefit estimado que esas estrategias en ese rango de umbrales, bajo los supuestos de la DCA y si esos umbrales son clínicamente plausibles. No demuestra por sí solo que usuarios sigan la recomendación, que el flujo funcione, que no haya daños operativos ni que mejoren resultados de pacientes. Se necesita evaluación prospectiva del sistema humano-IA y, según la decisión, un estudio de impacto comparativo.",
            "explanation": "DCA incorpora consecuencias mediante el umbral, pero sigue siendo una evaluación decisional basada en predicciones y supuestos, no una intervención clínica observada.",
            "common_misconceptions": ["Equiparar net benefit retrospectivo con efecto causal del despliegue.", "Ignorar si el rango de umbrales corresponde a decisiones reales."]
        },
        "feedback": {"correct": "Ha delimitado correctamente utilidad estimada e impacto prospectivo.", "incorrect": "Separe el cálculo contrafactual sobre predicciones de lo que ocurre cuando personas, interfaces y recursos actúan sobre ellas en la práctica."},
        "source_ids": ["vickers-elkin-dca-2006", "decide-ai"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U06-Q08",
        "type": "case_analysis",
        "prompt": "Un nuevo modelo supera a la práctica habitual en AUC (0,87 vs 0,80), pero tiene peor calibración cerca del umbral de tratamiento y no mejora net benefit entre 10% y 20%. Redacte una decisión de adopción defendible.",
        "linked_learning_outcome_ids": ["MLBIO-U06-LO02", "MLBIO-U06-LO03", "MLBIO-U06-LO05", "MLBIO-U06-LO06"],
        "difficulty": "advanced",
        "cognitive_level": "create",
        "answer_key": {
            "expected_answer": "No debe adoptarse solo por la mayor AUC. En el rango donde se toman decisiones, la calibración es peor y no hay ganancia de net benefit frente a la práctica habitual, por lo que no existe evidencia suficiente de mejor decisión clínica. Puede investigarse recalibración o una versión modificada con datos de desarrollo apropiados y reevaluación independiente, o conservar la práctica actual. La conclusión debe incluir incertidumbre, capacidad y necesidad de evaluación prospectiva antes de atribuir beneficio real.",
            "explanation": "El criterio de adopción debe corresponder a la tarea clínica: probabilidades y decisiones en el rango relevante pesan más que una mejora global de ranking aislada.",
            "common_misconceptions": ["Adoptar porque la AUC aumentó siete centésimas.", "Recalibrar sobre la misma prueba y presentar de nuevo el resultado como confirmación independiente."]
        },
        "feedback": {"correct": "Ha priorizado desempeño decisional y calibración sobre el ranking aislado.", "incorrect": "Pregunte qué métrica está más cerca de la decisión real y si el nuevo modelo mejora efectivamente esa decisión frente a la alternativa disponible."},
        "source_ids": ["steyerberg-performance-2010", "van-calster-calibration-2019", "vickers-elkin-dca-2006"],
        "status": "curated_pending_expert_review"
    }
]
save(assessment_path, assessment)

# Sources.
sources_path = COURSE / "sources.json"
sources_doc = load(sources_path)
sources = sources_doc["sources"]
by_id = {s["id"] for s in sources}
new_sources = [
    {
        "registry_id": "steyerberg-performance-2010",
        "id": "steyerberg-performance-2010",
        "title": "Assessing the performance of prediction models: a framework for traditional and novel measures",
        "authors": ["Ewout W. Steyerberg", "Andrew J. Vickers", "Nancy R. Cook", "Thomas Gerds", "Mithat Gonen", "Nancy Obuchowski", "Michael J. Pencina", "Michael W. Kattan"],
        "organization": "Epidemiology",
        "year": 2010,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3575184/",
        "doi": "10.1097/EDE.0b013e3181c30fb2",
        "type": "artículo metodológico",
        "verification_status": "verified_directly",
        "locator": "Abstract; sections on overall performance, discrimination, calibration and decision-analytic measures, pp. 128–138",
        "role": "Integra Brier score, discriminación, calibración y medidas de decisión dentro de un marco común de evaluación de modelos predictivos.",
        "curricular_function": "Sustentar que la evaluación clínica no debe reducirse a AUC y que calibración y utilidad decisional son dimensiones complementarias.",
        "limitations": "Es un marco metodológico general; la elección de métricas, umbrales y comparadores debe adaptarse al desenlace, uso previsto y diseño concreto.",
        "used_by_unit_ids": ["MLBIO-U06"]
    },
    {
        "registry_id": "van-calster-calibration-2019",
        "id": "van-calster-calibration-2019",
        "title": "Calibration: the Achilles heel of predictive analytics",
        "authors": ["Ben Van Calster", "David J. McLernon", "Maarten van Smeden", "Laure Wynants", "Ewout W. Steyerberg"],
        "organization": "BMC Medicine",
        "year": 2019,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6912996/",
        "doi": "10.1186/s12916-019-1466-7",
        "type": "artículo metodológico",
        "verification_status": "verified_directly",
        "locator": "Main text; sections on calibration hierarchy, calibration plots and external validation",
        "role": "Define y organiza la evaluación de calibración, explica por qué buena discriminación no garantiza probabilidades fiables y discute actualización cuando la calibración falla.",
        "curricular_function": "Sustentar curva de calibración, calibración en el grande, pendiente y la necesidad de evaluar probabilidades en la población objetivo.",
        "limitations": "Se centra en calibración de modelos de riesgo; no sustituye evaluación de discriminación, utilidad, flujo asistencial ni impacto prospectivo.",
        "used_by_unit_ids": ["MLBIO-U06"]
    },
    {
        "registry_id": "saito-rehmsmeier-pr-2015",
        "id": "saito-rehmsmeier-pr-2015",
        "title": "The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets",
        "authors": ["Takaya Saito", "Marc Rehmsmeier"],
        "organization": "PLOS ONE",
        "year": 2015,
        "url": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432",
        "doi": "10.1371/journal.pone.0118432",
        "type": "artículo metodológico",
        "license": "CC BY",
        "verification_status": "verified_directly",
        "locator": "Abstract; theoretical background; Results and Discussion",
        "role": "Compara ROC y precision-recall bajo fuerte desbalance y muestra por qué PR representa directamente la fracción de positivos verdaderos entre predicciones positivas.",
        "curricular_function": "Fundamentar la lectura de precision-recall en eventos infrecuentes y advertir contra interpretar ROC de forma aislada.",
        "limitations": "El artículo usa escenarios de clasificación binaria y no convierte PR en una medida de utilidad clínica ni elimina la necesidad de calibración y análisis por umbral.",
        "used_by_unit_ids": ["MLBIO-U06"]
    },
    {
        "registry_id": "vickers-elkin-dca-2006",
        "id": "vickers-elkin-dca-2006",
        "title": "Decision Curve Analysis: A Novel Method for Evaluating Prediction Models",
        "authors": ["Andrew J. Vickers", "Elena B. Elkin"],
        "organization": "Medical Decision Making",
        "year": 2006,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC2577036/",
        "doi": "10.1177/0272989X06295361",
        "type": "artículo metodológico",
        "verification_status": "verified_directly",
        "locator": "Methods; derivation of threshold probability, net benefit and decision curves; pp. 565–574",
        "role": "Introduce decision curve analysis y deriva net benefit a partir del umbral como expresión de la relación entre consecuencias de falsos positivos y falsos negativos.",
        "curricular_function": "Sustentar la comparación de modelos con treat-all y treat-none a través de umbrales clínicamente plausibles.",
        "limitations": "DCA estima valor decisional bajo supuestos; no demuestra adherencia, seguridad del flujo, efecto causal del despliegue ni resultados clínicos reales.",
        "used_by_unit_ids": ["MLBIO-U06"]
    }
]
for src in new_sources:
    if src["id"] not in by_id:
        sources.append(src)
save(sources_path, sources_doc)

# Glossary verification for Unit 6.
glossary_path = COURSE / "glossary.json"
glossary = load(glossary_path)
updates = {
    "MLBIO-GLO-059": ("Proporción de pacientes con el evento que son clasificados como positivos en un umbral especificado: TP/(TP+FN).", ["steyerberg-performance-2010"], [("steyerberg-performance-2010", "Sections on classification measures and discrimination")]),
    "MLBIO-GLO-060": ("Proporción de pacientes sin el evento que son clasificados como negativos en un umbral especificado: TN/(TN+FP).", ["steyerberg-performance-2010"], [("steyerberg-performance-2010", "Sections on classification measures and discrimination")]),
    "MLBIO-GLO-061": ("Valor predictivo positivo o precisión: proporción de predicciones positivas en las que se observa el evento; depende del umbral y de la prevalencia de la población evaluada.", ["saito-rehmsmeier-pr-2015", "steyerberg-performance-2010"], [("saito-rehmsmeier-pr-2015", "Abstract and theoretical background"), ("steyerberg-performance-2010", "Sections on classification measures")]),
    "MLBIO-GLO-062": ("Valor predictivo negativo: proporción de predicciones negativas en las que no se observa el evento; depende del umbral y de la prevalencia de la población evaluada.", ["steyerberg-performance-2010"], [("steyerberg-performance-2010", "Sections on classification measures")]),
    "MLBIO-GLO-063": ("Probabilidad o puntuación a partir de la cual la predicción desencadena una acción; en decision curve analysis, el umbral representa la relación entre consecuencias de falsos positivos y falsos negativos.", ["vickers-elkin-dca-2006"], [("vickers-elkin-dca-2006", "Methods; threshold probability and net benefit derivation")]),
    "MLBIO-GLO-064": ("Curva receiver operating characteristic que representa sensibilidad frente a 1-especificidad a través de posibles umbrales de clasificación.", ["steyerberg-performance-2010"], [("steyerberg-performance-2010", "Sections on discrimination and ROC analysis")]),
    "MLBIO-GLO-065": ("Curva que representa precisión o PPV frente a recall o sensibilidad a través de umbrales; su baseline depende de la prevalencia del evento.", ["saito-rehmsmeier-pr-2015"], [("saito-rehmsmeier-pr-2015", "Theoretical background and Results")]),
    "MLBIO-GLO-066": ("Área bajo la curva ROC; resume discriminación o ranking y puede interpretarse como la probabilidad de asignar mayor puntuación a un caso con evento que a uno sin evento bajo las condiciones de evaluación.", ["steyerberg-performance-2010"], [("steyerberg-performance-2010", "Sections on discrimination and c-statistic")]),
    "MLBIO-GLO-067": ("Correspondencia entre probabilidades predichas y frecuencias observadas en la población objetivo, evaluable mediante curva de calibración y medidas complementarias como calibración en el grande y pendiente.", ["van-calster-calibration-2019"], [("van-calster-calibration-2019", "Main text; calibration hierarchy and plots")]),
    "MLBIO-GLO-068": ("Promedio del error cuadrático entre probabilidad predicha y desenlace binario; resume calidad probabilística global y depende del contexto y prevalencia.", ["steyerberg-performance-2010"], [("steyerberg-performance-2010", "Overall model performance; Brier score")]),
    "MLBIO-GLO-069": ("Curva que representa net benefit de una estrategia predictiva a través de un rango de probabilidades umbral y permite compararla con alternativas como treat-all y treat-none.", ["vickers-elkin-dca-2006"], [("vickers-elkin-dca-2006", "Methods and Results; decision curves")]),
    "MLBIO-GLO-070": ("Medida de utilidad decisional que combina verdaderos positivos y falsos positivos, ponderando estos últimos por la relación de consecuencias implícita en el umbral.", ["vickers-elkin-dca-2006"], [("vickers-elkin-dca-2006", "Methods; net benefit formula")]),
}
for entry in glossary["entries"]:
    if entry["id"] in updates:
        definition, source_ids, locators = updates[entry["id"]]
        entry["definition"] = definition
        entry["source_ids"] = source_ids
        entry["source_locators"] = [{"source_id": sid, "locator": loc} for sid, loc in locators]
        entry["verification_status"] = "verified_directly"
save(glossary_path, glossary)

# Claims: exact sentences already present in the canonical Unit 6 content.
claims_path = COURSE / "claims.json"
claims_doc = load(claims_path)
claims_doc["scope"] = "Afirmaciones centrales de las Unidades 1–6 con fuente primaria o metodológica, localizador, alcance y revisión humana pendiente."
claims_doc["claims"] = [c for c in claims_doc["claims"] if c.get("unit") != 6]
claim_specs = [
    ("La sensibilidad es la proporción de eventos detectados y la especificidad la proporción de no eventos correctamente descartados.", "definition", "medium", "steyerberg-performance-2010", "Sections on classification measures"),
    ("Ambos dependen de prevalencia y no se transportan automáticamente entre poblaciones.", "interpretation_boundary", "high", "steyerberg-performance-2010", "Sections on classification measures and predictive values"),
    ("El umbral convierte probabilidad en acción y debe relacionarse con consecuencias.", "decision_principle", "high", "vickers-elkin-dca-2006", "Methods; threshold probability"),
    ("El AUC ROC puede interpretarse como la probabilidad de que un caso con evento reciba una puntuación mayor que uno sin evento.", "definition", "medium", "steyerberg-performance-2010", "Discrimination; c-statistic and ROC area"),
    ("Resume todos los umbrales, pero no indica calibración ni consecuencias.", "interpretation_boundary", "high", "steyerberg-performance-2010", "Framework for discrimination, calibration and decision measures"),
    ("En eventos raros, la curva precision-recall muestra la relación entre sensibilidad y valor predictivo positivo.", "methodological_interpretation", "medium", "saito-rehmsmeier-pr-2015", "Abstract and theoretical background"),
    ("Su baseline depende de prevalencia, por lo que comparar áreas entre poblaciones requiere cautela.", "methodological_caution", "high", "saito-rehmsmeier-pr-2015", "Theoretical background and Results"),
    ("La calibración evalúa si las probabilidades predichas corresponden a frecuencias observadas.", "definition", "high", "van-calster-calibration-2019", "Main text; definition of calibration"),
    ("La calibración en el grande compara riesgo promedio; la pendiente resume si las predicciones son demasiado extremas o conservadoras.", "definition", "high", "van-calster-calibration-2019", "Calibration hierarchy and calibration slope"),
    ("El Brier score es el promedio del error cuadrático entre probabilidad y desenlace.", "definition", "medium", "steyerberg-performance-2010", "Overall model performance; Brier score"),
    ("Decision curve analysis expresa consecuencias mediante un umbral de probabilidad que representa la relación entre daño de falsos positivos y beneficio de verdaderos positivos.", "definition", "high", "vickers-elkin-dca-2006", "Methods; threshold probability and net benefit"),
    ("El net benefit combina ambos en una escala comparable con estrategias de tratar a todos o a nadie.", "definition", "high", "vickers-elkin-dca-2006", "Methods and decision-curve comparison strategies"),
    ("Una curva de decisión no demuestra efecto real sobre pacientes; estima utilidad bajo supuestos de acción correcta, adherencia y consecuencias.", "interpretation_boundary", "high", "vickers-elkin-dca-2006", "Decision-analytic assumptions and interpretation"),
    ("La comparación principal debe incluir práctica habitual y baseline.", "methodological_requirement", "high", "steyerberg-performance-2010", "Framework for model comparison and decision-analytic measures"),
]
for i, (text, ctype, risk, source_id, locator) in enumerate(claim_specs, start=1):
    cid = f"MLBIO-U06-C{i:03d}"
    claims_doc["claims"].append({
        "claim_id": cid,
        "unit": 6,
        "text": text,
        "claim_type": ctype,
        "risk": risk,
        "context": "Aplicado a evaluación de modelos predictivos biomédicos; la interpretación concreta depende de población, prevalencia, uso previsto, umbral y alternativa clínica.",
        "source_id": source_id,
        "locator": {"section": locator},
        "support": "direct" if ctype in {"definition", "methodological_interpretation"} else "indirect",
        "source_verification_status": "verified_directly",
        "review_state": "ai_review_provisional",
        "reviewer_validation_id": None,
        "reviewed_at": DATE,
        "id": cid,
        "unit_id": "MLBIO-U06",
    })
save(claims_path, claims_doc)

# Regression coverage: make Unit 6 part of the durable canonical contract.
test_path = ROOT / "tests" / "test_academic_course_schema.py"
text = test_path.read_text(encoding="utf-8")
text = text.replace('self.assertEqual(report.counts["claims"], 70)', 'self.assertEqual(report.counts["claims"], 84)')
text = text.replace('for unit_number in (1, 2, 3, 4, 5):', 'for unit_number in (1, 2, 3, 4, 5, 6):')
text = text.replace('{"MLBIO-U02", "MLBIO-U03", "MLBIO-U04", "MLBIO-U05"}.intersection', '{"MLBIO-U02", "MLBIO-U03", "MLBIO-U04", "MLBIO-U05", "MLBIO-U06"}.intersection')
if "test_renderer_includes_curated_machine_learning_unit_6" not in text:
    marker = "    def test_every_assessment_item_maps_to_a_unit_outcome(self) -> None:\n"
    addition = '''    def test_renderer_includes_curated_machine_learning_unit_6(self) -> None:\n        unit = RENDERER.load_advanced_unit(\n            ROOT, "machine-learning-biomedico-validacion-clinica", 6\n        )\n        self.assertIsNotNone(unit)\n        assert unit is not None\n        self.assertEqual(unit["schema_version"], "canonical-1.0")\n        self.assertEqual(unit["unit"], 6)\n        self.assertEqual(unit["title"], "Discriminación, calibración y utilidad clínica")\n        self.assertEqual(len(unit["self_assessment"]), 8)\n        self.assertEqual(len(unit["guided_activities"][0]["deliverables"]), 6)\n        self.assertEqual(unit["guided_activities"][0]["estimated_duration_minutes"], 240)\n        self.assertEqual(len(unit["guided_activities"][0]["checking_criteria"]), 10)\n\n'''
    if marker not in text:
        raise RuntimeError("No se encontró el punto de inserción de la regresión U06")
    text = text.replace(marker, addition + marker)
test_path.write_text(text, encoding="utf-8")

print("Unidad 6 curada: teoría corregida, actividad, evaluación, glosario, fuentes, claims y regresiones actualizados.")
