#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data/courses/machine-learning-biomedico-validacion-clinica"
TODAY = "2026-08-23"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(records: list[dict], item: dict, key: str = "id") -> None:
    value = item[key]
    for index, current in enumerate(records):
        if current.get(key) == value or current.get("registry_id") == value:
            records[index] = item
            return
    records.append(item)


# ---------- Fuentes metodológicas específicas ----------
sources_path = COURSE / "sources.json"
sources = load(sources_path)
new_sources = [
    {
        "registry_id": "riley-external-validation-2024",
        "id": "riley-external-validation-2024",
        "title": "Evaluation of clinical prediction models (part 2): how to undertake an external validation study",
        "authors": [
            "Richard D Riley",
            "Lucinda Archer",
            "Kym I E Snell",
            "Joie Ensor",
            "Paula Dhiman",
            "Glen P Martin",
            "Laura J Bonnett",
            "Gary S Collins"
        ],
        "organization": "The BMJ",
        "year": 2024,
        "url": "https://www.bmj.com/content/384/bmj-2023-074820",
        "doi": "10.1136/bmj-2023-074820",
        "type": "guía metodológica",
        "verification_status": "verified_directly",
        "locator": "Summary points; ‘What do we mean by external validation?’; Steps 1–5; sections on calibration and discrimination",
        "role": "Define la validación externa como aplicación del modelo previamente especificado en datos relevantes no usados en desarrollo y detalla dataset objetivo, predicción, calibración, discriminación, utilidad e informe.",
        "curricular_function": "Sustentar el diseño de la cohorte externa, el bloqueo del modelo y la evaluación multidimensional sin refitting sobre la cohorte de validación.",
        "limitations": "Guía metodológica general; el diseño concreto depende del desenlace, censura, competidores, intervención y contexto clínico.",
        "used_by_unit_ids": ["MLBIO-U05"]
    },
    {
        "registry_id": "riley-external-validation-sample-size-2024",
        "id": "riley-external-validation-sample-size-2024",
        "title": "Evaluation of clinical prediction models (part 3): calculating the sample size required for an external validation study",
        "authors": [
            "Richard D Riley",
            "Kym I E Snell",
            "Lucinda Archer",
            "Joie Ensor",
            "Thomas P A Debray",
            "Ben van Calster",
            "Maarten van Smeden",
            "Gary S Collins"
        ],
        "organization": "The BMJ",
        "year": 2024,
        "url": "https://www.bmj.com/content/384/bmj-2023-074821",
        "doi": "10.1136/bmj-2023-074821",
        "type": "guía metodológica",
        "verification_status": "verified_directly",
        "locator": "Summary points and sections on target precision for calibration, discrimination and overall performance",
        "role": "Describe planificación del tamaño muestral de validación externa basada en precisión esperada de medidas de desempeño, evitando reglas fijas como criterio suficiente.",
        "curricular_function": "Exigir que la incertidumbre de desempeño externo y por centro se planifique según la precisión necesaria y no solo por un número mínimo arbitrario de eventos.",
        "limitations": "La planificación requiere supuestos sobre desempeño y distribución del predictor lineal; no garantiza representatividad ni ausencia de sesgo.",
        "used_by_unit_ids": ["MLBIO-U05"]
    },
    {
        "registry_id": "riley-external-validation-ipd-2016",
        "id": "riley-external-validation-ipd-2016",
        "title": "External validation of clinical prediction models using big datasets from e-health records or IPD meta-analysis: opportunities and challenges",
        "authors": [
            "Richard D Riley",
            "Joie Ensor",
            "Kym I E Snell",
            "Thomas P A Debray",
            "Doug G Altman",
            "Karel G M Moons",
            "Gary S Collins"
        ],
        "organization": "The BMJ",
        "year": 2016,
        "url": "https://www.bmj.com/content/353/bmj.i3140",
        "doi": "10.1136/bmj.i3140",
        "type": "artículo metodológico",
        "verification_status": "verified_directly",
        "locator": "Sections on heterogeneity in baseline risk and predictor effects; recommendations for cluster-specific performance, forest/funnel plots and model updating",
        "role": "Explica cómo estudiar heterogeneidad de desempeño entre centros, poblaciones y subgrupos y cómo distinguir validación de estrategias posteriores de recalibración o actualización.",
        "curricular_function": "Sustentar análisis multicéntrico, forest plots, heterogeneidad, transportabilidad parcial y necesidad de evidencia nueva tras una actualización.",
        "limitations": "Se centra en grandes bases multicéntricas e IPD; algunos métodos requieren suficientes centros y eventos para estimar heterogeneidad con precisión.",
        "used_by_unit_ids": ["MLBIO-U05"]
    },
    {
        "registry_id": "moreno-torres-dataset-shift-2012",
        "id": "moreno-torres-dataset-shift-2012",
        "title": "A unifying view on dataset shift in classification",
        "authors": [
            "Jose G Moreno-Torres",
            "Troy Raeder",
            "Rocío Alaiz-Rodríguez",
            "Nitesh V Chawla",
            "Francisco Herrera"
        ],
        "organization": "Pattern Recognition",
        "year": 2012,
        "url": "https://www.sciencedirect.com/science/article/pii/S0031320311002901",
        "doi": "10.1016/j.patcog.2011.06.019",
        "type": "artículo metodológico",
        "verification_status": "verified_directly",
        "locator": "Section 4 and concluding framework, pp. 521–530",
        "role": "Formaliza covariate shift, prior probability shift, concept shift y dataset shift mediante cambios de distribuciones entre entrenamiento y prueba.",
        "curricular_function": "Dar una taxonomía precisa para distinguir cambios de covariables, prevalencia y relación predictor-desenlace antes de atribuir una degradación a una causa concreta.",
        "limitations": "Marco general de clasificación, no específico de medicina; en datos clínicos pueden coexistir varios mecanismos y cambios de medición o flujo.",
        "used_by_unit_ids": ["MLBIO-U05"]
    }
]
for record in new_sources:
    upsert(sources["sources"], record)
sources["consulted_on"] = TODAY
save(sources_path, sources)

# ---------- Unidad ----------
unit_path = COURSE / "units/unit-05.json"
unit = load(unit_path)
unit["prerequisite_unit_ids"] = ["MLBIO-U01", "MLBIO-U02", "MLBIO-U03", "MLBIO-U04"]

# Normaliza ecuaciones para MathJax y mejora una formulación de calibración.
equations = [
    r"\widehat{\mathrm{Perf}}_{\mathrm{ext}} = M\!\left(f_{\mathrm{frozen}}, D_{\mathrm{target}}\right)",
    r"P_{\mathrm{target}}(X,Y) \neq P_{\mathrm{development}}(X,Y)",
    r"\operatorname{logit}(Y)=\alpha+\beta\,\operatorname{logit}(\hat p)",
    r"\hat p_{\mathrm{updated}}=\operatorname{logit}^{-1}\!\left(\alpha_{\mathrm{new}}+\beta_{\mathrm{new}}\operatorname{logit}(\hat p_{\mathrm{original}})\right)"
]
for topic, latex in zip(unit["topics"], equations):
    topic["blocks"][0]["latex"] = latex

for block in unit["topics"][2]["subtopics"][0]["blocks"]:
    if block.get("type") == "paragraph":
        block["text"] = (
            "La validación externa debe evaluar discriminación, calibración, error probabilístico, umbrales y utilidad. "
            "La calibración en el grande detecta desajuste del riesgo promedio y la pendiente de calibración resume si las predicciones son demasiado extremas o demasiado moderadas. "
            "Los análisis por subgrupos y centros requieren intervalos y número de eventos. Una métrica global puede ocultar que el modelo falla sistemáticamente en un entorno con proceso distinto."
        )

activity = unit["activities"][0]
activity.update({
    "purpose": "Diseñar una validación externa de una versión bloqueada, demostrar la compatibilidad del contexto objetivo, cuantificar desempeño e heterogeneidad y definir una ruta de actualización que preserve una evaluación independiente posterior.",
    "prerequisite_unit_ids": ["MLBIO-U01", "MLBIO-U02", "MLBIO-U03", "MLBIO-U04"],
    "instructions": [
        "Definir el uso previsto que se quiere transportar y seleccionar un contexto externo relevante por tiempo, centro, región o dominio, explicando qué diferencia aporta respecto del desarrollo.",
        "Congelar antes de inspeccionar resultados el pipeline, coeficientes o pesos, hiperparámetros, categorías, manejo de faltantes, umbral, exclusiones y plan de análisis; registrar una versión identificable.",
        "Auditar la compatibilidad entre desarrollo y validación: población, severidad, prevalencia, unidades, dispositivos, tiempos, definiciones, faltantes, codificación y proceso asistencial.",
        "Aplicar la versión bloqueada sin refitting y estimar desempeño con incertidumbre: calibración, discriminación, error probabilístico y utilidad en los umbrales del uso previsto, incluyendo resultados por centro cuando corresponda.",
        "Si aparece degradación, formular hipótesis sobre su mecanismo y preespecificar si procede restricción de uso, recalibración o actualización; reservar datos independientes para evaluar cualquier nueva versión."
    ],
    "tasks": [
        "Distinguir qué pregunta responden una validación temporal, una geográfica y una de dominio para el mismo modelo clínico.",
        "Definir un manifiesto de los artefactos y decisiones que deben bloquearse antes de acceder al resultado externo.",
        "Comparar la mezcla de casos, prevalencia y proceso asistencial entre dos centros y anticipar qué métricas podrían cambiar aunque el algoritmo sea idéntico.",
        "Auditar una variable de laboratorio con distinto ensayo, unidad o límite de detección y decidir si puede transformarse sin cambiar el uso previsto.",
        "Interpretar conjuntamente AUC, calibración en el grande, pendiente de calibración y net benefit cuando el ranking permanece estable pero las probabilidades se desplazan.",
        "Diseñar un forest plot conceptual por centro que muestre estimación, intervalo e información suficiente para no sobreinterpretar centros pequeños.",
        "Elegir entre no modificar, recalibrar intercepto, recalibrar intercepto y pendiente, revisar coeficientes, restringir el uso o reconstruir el modelo para tres patrones de degradación.",
        "Definir cómo separar una cohorte usada para actualización de una cohorte independiente posterior que evalúe la nueva versión."
    ],
    "deliverables": [
        "Protocolo de validación externa con uso previsto, población y entorno objetivo, tipo de validación, fechas, unidad independiente y justificación de relevancia externa.",
        "Manifiesto de bloqueo con identificador de versión, pipeline, parámetros, dependencias, reglas de faltantes, umbral, exclusiones y análisis preespecificado.",
        "Matriz de compatibilidad desarrollo-validación que compare definiciones, unidades, dispositivos, prevalencia, severidad, faltantes, flujo y temporalidad, con decisión explícita para cada diferencia.",
        "Informe de desempeño externo con estimaciones e incertidumbre para calibración, discriminación, error probabilístico y utilidad, más análisis por centro o subgrupo cuando sea informativo.",
        "Diagnóstico de transportabilidad que separe hallazgos observados de hipótesis sobre dataset shift, mezcla de casos, medición o proceso y delimite dónde la evidencia permite usar el modelo.",
        "Plan de actualización y reevaluación que indique qué datos se consumirían para adaptar el modelo, qué crea una nueva versión y qué cohorte permanecerá independiente para confirmarla."
    ],
    "checking_criteria": [
        "La cohorte externa corresponde a una población y un entorno relevantes para el uso previsto y su relación con los datos de desarrollo está documentada.",
        "La evaluación aplica una versión identificable y bloqueada sin refitting, selección de umbral ni correcciones motivadas por los resultados externos.",
        "La auditoría compara definiciones, unidades, dispositivos, temporalidad, faltantes, prevalencia, severidad y flujo asistencial antes de interpretar métricas.",
        "Las métricas incluyen calibración, discriminación, error probabilístico y utilidad cuando hay decisiones clínicas, con intervalos o incertidumbre apropiados.",
        "Las diferencias de AUC entre centros no se atribuyen automáticamente al algoritmo sin considerar mezcla de casos y precisión de las estimaciones.",
        "Los resultados multicéntricos muestran heterogeneidad y evitan clasificar centros pequeños como fallidos por una estimación puntual extrema.",
        "Las explicaciones de degradación distinguen observación de hipótesis y no convierten asociaciones post hoc en causas demostradas.",
        "La estrategia de recalibración o actualización es proporcional al patrón de degradación, tamaño muestral y uso previsto; también contempla restringir o retirar el modelo.",
        "Los datos usados para adaptar el modelo no se reutilizan como confirmación independiente y la nueva versión queda versionada con evidencia propia."
    ],
    "estimated_duration_minutes": 240,
    "status": "curated_pending_expert_review"
})
unit["source_ids"] = [
    "tripod-ai",
    "probast-ai",
    "decide-ai",
    "imdrf-fda-gmlp",
    "fda-transparency-mlmd",
    "riley-external-validation-2024",
    "riley-external-validation-sample-size-2024",
    "riley-external-validation-ipd-2016",
    "moreno-torres-dataset-shift-2012"
]
unit["claim_ids"] = [f"MLBIO-U05-C{i:03d}" for i in range(1, 15)]
save(unit_path, unit)

# ---------- Glosario ----------
glossary_path = COURSE / "glossary.json"
glossary = load(glossary_path)
glossary_updates = {
    "MLBIO-GLO-047": {
        "definition": "Evaluación del desempeño predictivo de una versión previamente especificada en un conjunto de datos diferente y relevante que no participó en su desarrollo ni se usa para refitting durante esa evaluación.",
        "source_ids": ["riley-external-validation-2024"],
        "source_locators": [{"source_id": "riley-external-validation-2024", "locator": "Summary points; ‘What do we mean by external validation?’"}]
    },
    "MLBIO-GLO-048": {
        "definition": "Validación externa en pacientes de un periodo posterior al desarrollo, útil para estudiar transportabilidad frente a cambios temporales de población, práctica, medición o riesgo basal.",
        "source_ids": ["riley-external-validation-2024", "tripod-ai"],
        "source_locators": [
            {"source_id": "riley-external-validation-2024", "locator": "Step 1 and discussion of different target populations/settings"},
            {"source_id": "tripod-ai", "locator": "Expanded checklist: source of data, dates and setting"}
        ]
    },
    "MLBIO-GLO-049": {
        "definition": "Validación externa realizada en uno o más centros, regiones o sistemas sanitarios distintos de los utilizados para desarrollar el modelo.",
        "source_ids": ["riley-external-validation-2024", "riley-external-validation-ipd-2016"],
        "source_locators": [
            {"source_id": "riley-external-validation-2024", "locator": "Step 1; target population and setting"},
            {"source_id": "riley-external-validation-ipd-2016", "locator": "Sections on clusters, settings and between-cluster heterogeneity"}
        ]
    },
    "MLBIO-GLO-050": {
        "definition": "Grado en que un modelo conserva desempeño y utilidad suficientes al aplicarse en poblaciones, periodos, centros o procesos relevantes distintos de aquellos que informaron su desarrollo.",
        "source_ids": ["riley-external-validation-2024", "riley-external-validation-ipd-2016"],
        "source_locators": [
            {"source_id": "riley-external-validation-2024", "locator": "Target validity and multiple external validation studies"},
            {"source_id": "riley-external-validation-ipd-2016", "locator": "Conclusions on reliability and transportability across settings/populations"}
        ]
    },
    "MLBIO-GLO-051": {
        "definition": "Diferencia entre las distribuciones que generan los datos de desarrollo y los datos de aplicación o evaluación; puede involucrar covariables, prevalencia, relación predictor-desenlace o varias de ellas.",
        "source_ids": ["moreno-torres-dataset-shift-2012"],
        "source_locators": [{"source_id": "moreno-torres-dataset-shift-2012", "locator": "Section 4 and concluding framework, pp. 521–530"}]
    },
    "MLBIO-GLO-052": {
        "definition": "Cambio de la frecuencia o riesgo basal del desenlace entre desarrollo y aplicación; puede desplazar las probabilidades absolutas aunque otras relaciones predictivas se mantengan.",
        "source_ids": ["moreno-torres-dataset-shift-2012", "riley-external-validation-ipd-2016"],
        "source_locators": [
            {"source_id": "moreno-torres-dataset-shift-2012", "locator": "Section 4.2, prior probability shift"},
            {"source_id": "riley-external-validation-ipd-2016", "locator": "Heterogeneity in baseline risk and model updating"}
        ]
    },
    "MLBIO-GLO-053": {
        "definition": "Cambio de la distribución condicional del desenlace dados los predictores, de modo que una relación aprendida durante el desarrollo deja de representar la relación del contexto objetivo.",
        "source_ids": ["moreno-torres-dataset-shift-2012"],
        "source_locators": [{"source_id": "moreno-torres-dataset-shift-2012", "locator": "Section 4.3, concept shift"}]
    },
    "MLBIO-GLO-054": {
        "definition": "Composición de una cohorte respecto a riesgo, severidad y distribución de predictores; sus diferencias entre poblaciones pueden modificar medidas como la discriminación sin implicar por sí solas un cambio del algoritmo.",
        "source_ids": ["riley-external-validation-2024", "riley-external-validation-ipd-2016"],
        "source_locators": [
            {"source_id": "riley-external-validation-2024", "locator": "Discrimination section: c statistic depends on case mix distribution"},
            {"source_id": "riley-external-validation-ipd-2016", "locator": "Sections on heterogeneity in case mix and predictive performance"}
        ]
    },
    "MLBIO-GLO-055": {
        "definition": "Componente de calibración que resume si, en promedio, las predicciones son sistemáticamente demasiado altas o demasiado bajas; para modelos logísticos suele expresarse mediante un intercepto ideal de cero.",
        "source_ids": ["riley-external-validation-2024"],
        "source_locators": [{"source_id": "riley-external-validation-2024", "locator": "Quantifying calibration performance: calibration-in-the-large ideal value 0"}]
    },
    "MLBIO-GLO-056": {
        "definition": "Coeficiente que relaciona el desenlace con el predictor lineal o logit del riesgo previsto durante la evaluación; un valor ideal de uno indica extensión apropiada de las predicciones, mientras valores menores de uno sugieren predicciones demasiado extremas.",
        "source_ids": ["riley-external-validation-2024"],
        "source_locators": [{"source_id": "riley-external-validation-2024", "locator": "Quantifying calibration performance: calibration slope ideal value 1"}]
    },
    "MLBIO-GLO-057": {
        "definition": "Actualización limitada de probabilidades que modifica el riesgo basal y, cuando procede, la pendiente global del predictor original sin necesariamente cambiar el orden de riesgo entre individuos.",
        "source_ids": ["riley-external-validation-ipd-2016"],
        "source_locators": [{"source_id": "riley-external-validation-ipd-2016", "locator": "Sections discussing recalibration of intercept/baseline risk and predictor effects"}]
    },
    "MLBIO-GLO-058": {
        "definition": "Modificación de una versión predictiva después de su desarrollo, desde recalibración hasta revisión de coeficientes, extensión con predictores o reconstrucción; la versión resultante requiere documentación y evaluación propias.",
        "source_ids": ["riley-external-validation-ipd-2016", "imdrf-fda-gmlp"],
        "source_locators": [
            {"source_id": "riley-external-validation-ipd-2016", "locator": "Recommendations on model updating and tailoring across settings"},
            {"source_id": "imdrf-fda-gmlp", "locator": "Guiding principles on lifecycle, monitoring and retraining/change management"}
        ]
    }
}
for entry in glossary["entries"]:
    update = glossary_updates.get(entry.get("id"))
    if update:
        entry.update(update)
        entry["verification_status"] = "verified_directly"
save(glossary_path, glossary)

# ---------- Evaluación formativa ----------
assessment_path = COURSE / "assessments/unit-05.json"
assessment = load(assessment_path)
assessment["purpose"] = "Evaluar si el estudiante puede diseñar una validación externa verdaderamente independiente, diagnosticar transportabilidad y heterogeneidad y decidir cuándo y cómo actualizar sin reutilizar la evidencia de confirmación."
assessment["items"] = [
    {
        "id": "MLBIO-U05-Q01",
        "type": "case_analysis",
        "prompt": "Un modelo de reingreso se desarrolló con altas de 2024–2025 en Hospital A. El equipo propone tres evaluaciones: pacientes de 2026 del Hospital A, pacientes de 2025 del Hospital B y pacientes de 2026 del Hospital B. Clasifique qué dimensión externa aporta cada cohorte y explique cuál responde mejor a una futura implantación en Hospital B durante 2026.",
        "linked_learning_outcome_ids": ["MLBIO-U05-LO01", "MLBIO-U05-LO06"],
        "difficulty": "intermediate",
        "cognitive_level": "analyze",
        "answer_key": {
            "expected_answer": "Hospital A-2026 aporta validación temporal; Hospital B-2025 aporta validación geográfica; Hospital B-2026 combina diferencia geográfica y temporal y es la más próxima al contexto de implantación descrito. Ninguna etiqueta garantiza por sí sola transportabilidad: deben compararse población, flujo, medición y desenlace con el uso previsto y cuantificarse desempeño e incertidumbre.",
            "explanation": "La externalidad debe expresarse respecto de la fuente de desarrollo y, sobre todo, de la población y entorno objetivo; una cohorte más distinta no es automáticamente mejor si no representa el uso previsto.",
            "common_misconceptions": ["Llamar ‘externa’ a cualquier partición no usada en el ajuste.", "Suponer que la validación geográfica siempre es superior a una temporal independientemente del objetivo de despliegue."]
        },
        "feedback": {
            "correct": "Ha relacionado tipo de validación, contexto objetivo y límites de la etiqueta ‘externa’.",
            "incorrect": "Compare cada cohorte con el desarrollo en dos ejes: cuándo fue observada y dónde/proceso en que fue generada; después compárela con el uso previsto."
        },
        "source_ids": ["riley-external-validation-2024", "tripod-ai"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U05-Q02",
        "type": "case_analysis",
        "prompt": "Antes de validar un modelo de deterioro, el equipo carga la cohorte externa, observa sensibilidad baja y decide cambiar el umbral de 0,20 a 0,12 antes de calcular el resto de métricas. ¿Qué se ha perdido y cómo reorganizaría el estudio?",
        "linked_learning_outcome_ids": ["MLBIO-U05-LO02", "MLBIO-U05-LO05"],
        "difficulty": "advanced",
        "cognitive_level": "evaluate",
        "answer_key": {
            "expected_answer": "La cohorte externa informó una decisión del sistema, por lo que ya no puede confirmar independientemente el desempeño del nuevo umbral. Debe conservarse y reportarse la evaluación de la versión originalmente bloqueada; el umbral 0,12 define una versión adaptada que se desarrolla con datos de actualización y necesita otra cohorte independiente posterior. El manifiesto previo debe incluir pipeline, parámetros, categorías, faltantes, umbral, exclusiones y análisis.",
            "explanation": "La independencia se pierde cuando la evaluación influye en una decisión que luego se vuelve a medir en los mismos pacientes, aunque no se reentrenen los pesos del modelo.",
            "common_misconceptions": ["Creer que solo modificar coeficientes cuenta como refitting.", "Borrar el primer análisis y seguir llamando prueba a la misma cohorte."]
        },
        "feedback": {
            "correct": "Ha tratado el umbral como parte de la versión bloqueada y ha separado actualización de confirmación.",
            "incorrect": "Pregunte qué decisiones del sistema conocieron el resultado externo. Cualquier decisión modificada consume independencia para la nueva versión."
        },
        "source_ids": ["riley-external-validation-2024", "imdrf-fda-gmlp"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U05-Q03",
        "type": "case_analysis",
        "prompt": "El mismo modelo obtiene AUC 0,76 en un hospital terciario con pacientes muy heterogéneos y AUC 0,68 en una clínica especializada con un rango de gravedad estrecho. El equipo concluye que el modelo ‘se degradó’ en la clínica. Evalúe esa conclusión y proponga qué comparar antes de aceptarla.",
        "linked_learning_outcome_ids": ["MLBIO-U05-LO03", "MLBIO-U05-LO04"],
        "difficulty": "advanced",
        "cognitive_level": "evaluate",
        "answer_key": {
            "expected_answer": "La diferencia de AUC no demuestra por sí sola degradación intrínseca porque la discriminación depende de la mezcla de casos y de cuán separables sean los riesgos presentes. Deben compararse distribución de predictores, severidad, prevalencia, medición, calibración, error probabilístico, utilidad e intervalos de las diferencias. También puede considerarse una medida ajustada por case mix si el estimando lo justifica.",
            "explanation": "Una población más homogénea puede reducir la variación del riesgo y, con ella, el c-statistic incluso cuando el modelo mantiene relaciones útiles.",
            "common_misconceptions": ["Interpretar la AUC como propiedad fija del algoritmo.", "Atribuir toda diferencia entre centros a dataset shift causalmente dañino sin describir la población."]
        },
        "feedback": {
            "correct": "Ha situado la AUC dentro de la mezcla de casos y ha exigido una evaluación multidimensional.",
            "incorrect": "La AUC se calcula sobre pares de pacientes de esa cohorte. Pregunte cómo cambia la separabilidad de esos pares cuando cambia la población."
        },
        "source_ids": ["riley-external-validation-2024", "riley-external-validation-ipd-2016"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U05-Q04",
        "type": "case_analysis",
        "prompt": "En un centro externo, la AUC permanece en 0,81, la calibración en el grande es -0,45 y la pendiente es 0,98. Interprete el patrón y proponga la actualización mínima razonable sin afirmar más de lo que permiten esos resultados.",
        "linked_learning_outcome_ids": ["MLBIO-U05-LO04", "MLBIO-U05-LO05"],
        "difficulty": "advanced",
        "cognitive_level": "analyze",
        "answer_key": {
            "expected_answer": "El ranking se conserva razonablemente y la pendiente cercana a uno no sugiere un problema global fuerte de extremidad, pero el intercepto negativo indica sobrepredicción sistemática en promedio en la parametrización logística habitual. Una actualización mínima candidata es recalibrar el intercepto con datos de actualización adecuados, manteniendo los efectos originales. Debe comprobarse la curva de calibración completa y la utilidad; la versión recalibrada necesita evaluación independiente posterior.",
            "explanation": "Intercepto y pendiente responden a preguntas distintas. Corregir riesgo basal no implica que el ranking cambie ni que se hayan resuelto defectos locales o de subgrupos.",
            "common_misconceptions": ["Reentrenar todo el modelo solo porque el intercepto se aleja de cero.", "Declarar que AUC estable significa probabilidades bien calibradas."]
        },
        "feedback": {
            "correct": "Ha separado ranking, nivel medio de riesgo, pendiente y necesidad de reevaluación.",
            "incorrect": "Compare cada estadístico con su valor ideal: intercepto 0 y pendiente 1; después elija la modificación más limitada compatible con el patrón."
        },
        "source_ids": ["riley-external-validation-2024", "riley-external-validation-ipd-2016"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U05-Q05",
        "type": "case_analysis",
        "prompt": "Cinco hospitales aportan validación. La AUC agrupada es 0,79, pero por centro varía entre 0,62 y 0,84; el centro con 0,62 tiene 18 eventos y un intervalo muy amplio. Diseñe cómo comunicaría la heterogeneidad y qué evitaría concluir.",
        "linked_learning_outcome_ids": ["MLBIO-U05-LO04", "MLBIO-U05-LO06"],
        "difficulty": "advanced",
        "cognitive_level": "create",
        "answer_key": {
            "expected_answer": "Debe mostrarse desempeño por centro con intervalos y número de eventos, por ejemplo mediante forest plots, además del resumen global. Si hay suficientes centros puede cuantificarse heterogeneidad y un intervalo de predicción para un centro nuevo. El centro con AUC 0,62 no debe declararse fallido por su punto estimado sin considerar la gran incertidumbre. La investigación de causas debe comparar case mix, medición y flujo y tratar explicaciones post hoc como hipótesis.",
            "explanation": "El promedio puede ocultar heterogeneidad y las estimaciones de centros pequeños son ruidosas; ambas dimensiones son necesarias para juzgar transportabilidad.",
            "common_misconceptions": ["Ocultar centros individuales porque el promedio global es aceptable.", "Ordenar hospitales por estimación puntual ignorando precisión y tamaño."
            ]
        },
        "feedback": {
            "correct": "Ha combinado visualización por centro, incertidumbre y cautela causal.",
            "incorrect": "Un forest plot debe mostrar tanto el punto como su incertidumbre; pregunte cuánto sabe realmente el centro con solo 18 eventos."
        },
        "source_ids": ["riley-external-validation-ipd-2016", "riley-external-validation-sample-size-2024"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U05-Q06",
        "type": "case_analysis",
        "prompt": "Un laboratorio del centro externo registra creatinina en µmol/L y el centro de desarrollo en mg/dL. El equipo convierte las unidades antes de predecir y afirma que ‘el dataset ya es equivalente’. Audite esa afirmación.",
        "linked_learning_outcome_ids": ["MLBIO-U05-LO03", "MLBIO-U05-LO06"],
        "difficulty": "intermediate",
        "cognitive_level": "analyze",
        "answer_key": {
            "expected_answer": "La conversión de unidades puede ser necesaria pero no demuestra equivalencia. Deben verificarse analito, método/ensayo, calibración del laboratorio, momento de medición, límite de detección, redondeo, rangos, faltantes y cualquier regla del pipeline. La transformación debe estar versionada y aplicarse de forma reproducible. Si la variable no es semántica o metrológicamente compatible, la transportabilidad está limitada aunque las unidades coincidan.",
            "explanation": "Una misma etiqueta de variable puede ocultar diferencias del proceso de medición que el modelo no vio durante desarrollo.",
            "common_misconceptions": ["Tratar nombres de columnas iguales como garantía de equivalencia.", "Modificar silenciosamente la extracción para hacer encajar el modelo."
            ]
        },
        "feedback": {
            "correct": "Ha distinguido conversión matemática de compatibilidad de medición y procedencia.",
            "incorrect": "Después de convertir unidades, pregunte si realmente se midió la misma cantidad, con el mismo significado clínico y en el mismo momento."
        },
        "source_ids": ["probast-ai", "tripod-ai", "riley-external-validation-2024"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U05-Q07",
        "type": "case_analysis",
        "prompt": "Tras una validación externa se detecta pendiente de calibración 0,63, AUC menor, nuevas terapias que alteraron la relación de varios predictores con el desenlace y 75 eventos locales disponibles. Compare recalibrar intercepto, recalibrar intercepto+pendiente y reconstruir o revisar el modelo.",
        "linked_learning_outcome_ids": ["MLBIO-U05-LO05"],
        "difficulty": "advanced",
        "cognitive_level": "evaluate",
        "answer_key": {
            "expected_answer": "Un ajuste solo del intercepto corrige riesgo basal y no aborda la pendiente 0,63. Intercepto+pendiente corrige una sobreextensión global pero no necesariamente cambios específicos de asociaciones ni pérdida de discriminación. Revisar coeficientes o reconstruir puede ser conceptualmente necesario si las terapias cambiaron relaciones, pero 75 eventos pueden ser insuficientes para una actualización compleja estable. Deben considerarse restricción temporal del uso, recopilación de más datos o actualización regularizada y, en todos los casos, una evaluación independiente posterior.",
            "explanation": "La complejidad de la actualización debe corresponder al mecanismo de degradación y a la información disponible; ‘actualizar más’ no es automáticamente mejor.",
            "common_misconceptions": ["Elegir siempre reconstrucción ante cualquier degradación.", "Usar los mismos 75 eventos para ajustar una revisión compleja y presentarla como validada."
            ]
        },
        "feedback": {
            "correct": "Ha vinculado patrón de degradación, complejidad de actualización, tamaño muestral y evidencia posterior.",
            "incorrect": "Pregunte qué problema puede corregir cada nivel de actualización y cuántos parámetros nuevos pretende estimar con 75 eventos."
        },
        "source_ids": ["riley-external-validation-ipd-2016", "riley-external-validation-sample-size-2024", "imdrf-fda-gmlp"],
        "status": "curated_pending_expert_review"
    },
    {
        "id": "MLBIO-U05-Q08",
        "type": "case_analysis",
        "prompt": "Un modelo funciona adecuadamente en tres hospitales, pero en un cuarto el predictor principal se obtiene con una tecnología distinta y la relación con el desenlace cambió tras una nueva vía asistencial. El patrocinador propone recalibrar para mantener despliegue nacional. Redacte una decisión de transportabilidad responsable.",
        "linked_learning_outcome_ids": ["MLBIO-U05-LO05", "MLBIO-U05-LO06"],
        "difficulty": "advanced",
        "cognitive_level": "evaluate",
        "answer_key": {
            "expected_answer": "La evidencia apoya uso solo en los contextos evaluados donde desempeño y utilidad son aceptables. En el cuarto hospital existen diferencias de medición y de relación predictor-desenlace que una recalibración simple puede no corregir. Debe limitarse o suspenderse el uso allí, investigar y documentar el cambio, y si se desarrolla una adaptación tratarla como una nueva versión con datos de actualización y validación posterior independiente. No debe extrapolarse el promedio nacional para ocultar el fallo local.",
            "explanation": "Transportabilidad es dependiente del contexto y la decisión puede ser restringir o retirar; preservar el modelo no es el objetivo metodológico.",
            "common_misconceptions": ["Asumir que recalibrar siempre resuelve dataset shift.", "Declarar universalidad porque la mayoría de centros obtienen buenas métricas."
            ]
        },
        "feedback": {
            "correct": "Ha delimitado la evidencia y ha priorizado restricción de uso y nueva evaluación sobre preservar una versión inadecuada.",
            "incorrect": "Separe qué cambió: nivel de riesgo, medición o relación predictor-desenlace. La recalibración solo resuelve una parte de esos problemas."
        },
        "source_ids": ["riley-external-validation-ipd-2016", "moreno-torres-dataset-shift-2012", "imdrf-fda-gmlp", "fda-transparency-mlmd"],
        "status": "curated_pending_expert_review"
    }
]
assessment["status"] = "curated_pending_expert_review"
save(assessment_path, assessment)

# ---------- Afirmaciones trazadas ----------
claims_path = COURSE / "claims.json"
claims = load(claims_path)
claims["scope"] = "Afirmaciones centrales de las Unidades 1–5 con fuente primaria o metodológica, localizador, alcance y revisión humana pendiente."
claims["review_state"] = "ai_review_provisional"
claims["claims"] = [item for item in claims["claims"] if item.get("unit_id") != "MLBIO-U05"]
claim_specs = [
    ("Una evaluación externa aplica un modelo completamente definido a datos que no participaron en su desarrollo.", "methodological_requirement", "high", "riley-external-validation-2024", "‘What do we mean by external validation?’", "direct"),
    ("La validación temporal usa un periodo posterior y prueba cambios de práctica, prevalencia o tecnología.", "definition", "medium", "riley-external-validation-2024", "Step 1; target population and setting", "indirect"),
    ("Antes de acceder a resultados deben bloquearse pipeline, coeficientes, hiperparámetros, categorías, manejo de faltantes, umbral y plan de análisis.", "methodological_requirement", "high", "riley-external-validation-2024", "Definition of external validation; Steps 2–3", "indirect"),
    ("Si se corrige el modelo después de observar la cohorte, esa cohorte se convierte en datos de actualización y deja de evaluar la versión corregida.", "methodological_requirement", "high", "riley-external-validation-2024", "External validation does not involve refitting; Step 2", "direct"),
    ("La degradación puede surgir por cambio de prevalencia, severidad, criterios de derivación, tratamientos, dispositivos, codificación o relación entre predictores y desenlace.", "interpretation_boundary", "high", "riley-external-validation-2024", "Calibration plots section: differences in case mix, outcome proportion, timing and measurement", "direct"),
    ("La mezcla de casos modifica métricas.", "methodological_interpretation", "medium", "riley-external-validation-2024", "Quantifying discrimination performance: c statistic depends on case mix distribution", "direct"),
    ("Los predictores pueden tener el mismo nombre y diferente significado.", "methodological_caution", "high", "probast-ai", "Predictor domain: definition, measurement and availability", "indirect"),
    ("La validación externa debe evaluar discriminación, calibración, error probabilístico, umbrales y utilidad.", "methodological_requirement", "high", "riley-external-validation-2024", "Summary points; Steps 3–4", "direct"),
    ("En estudios multicéntricos, reportar solo el promedio agrupado oculta heterogeneidad.", "methodological_caution", "high", "riley-external-validation-ipd-2016", "Recommendations for cluster-specific performance and heterogeneity", "direct"),
    ("La transportabilidad no es una propiedad binaria.", "interpretation_boundary", "medium", "riley-external-validation-2024", "Multiple external validation studies; conclusions", "indirect"),
    ("La recalibración ajusta probabilidades sin reconstruir completamente el modelo.", "definition", "medium", "riley-external-validation-ipd-2016", "Sections on model updating and recalibration", "direct"),
    ("Los datos utilizados para recalibrar o actualizar se separan de la evaluación posterior.", "methodological_requirement", "high", "riley-external-validation-2024", "External validation does not involve refitting", "indirect"),
    ("Un modelo actualizado es una nueva versión con procedencia, fecha, población y condiciones propias.", "lifecycle_requirement", "high", "imdrf-fda-gmlp", "Guiding principles on lifecycle, monitoring and retraining", "indirect"),
    ("Si la degradación refleja cambios estructurales del flujo o del desenlace, recalibrar puede ser insuficiente y el sistema debe rediseñarse o retirarse.", "decision_principle", "high", "imdrf-fda-gmlp", "Guiding principles on performance, monitoring and change management", "indirect")
]
for index, (text, claim_type, risk, source_id, locator, support) in enumerate(claim_specs, 1):
    cid = f"MLBIO-U05-C{index:03d}"
    claims["claims"].append({
        "claim_id": cid,
        "unit": 5,
        "text": text,
        "claim_type": claim_type,
        "risk": risk,
        "context": "Aplicado a validación externa y actualización de modelos predictivos biomédicos; la conclusión concreta depende del uso previsto, población, desenlace y diseño.",
        "source_id": source_id,
        "locator": {"section": locator},
        "support": support,
        "source_verification_status": "verified_directly",
        "review_state": "ai_review_provisional",
        "reviewer_validation_id": None,
        "reviewed_at": TODAY,
        "id": cid,
        "unit_id": "MLBIO-U05"
    })
save(claims_path, claims)

print("Unidad 5 curada: actividad, evaluación, glosario, fuentes y afirmaciones actualizados.")
