from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_exact(value, mapping):
    if isinstance(value, str):
        return mapping.get(value, value)
    if isinstance(value, list):
        return [replace_exact(item, mapping) for item in value]
    if isinstance(value, dict):
        return {key: replace_exact(item, mapping) for key, item in value.items()}
    return value


# ---------------------------------------------------------------------------
# 1. Consolidate accidental duplicate CONSORT-AI / SPIRIT-AI source IDs.
# ---------------------------------------------------------------------------
sources_path = COURSE / "sources.json"
sources_doc = load(sources_path)
sources = sources_doc["sources"]
by_id = {item["id"]: item for item in sources}
source_mapping = {"consort-ai-2020": "consort-ai", "spirit-ai-2020": "spirit-ai"}

for duplicate_id, canonical_id in source_mapping.items():
    duplicate = by_id.get(duplicate_id)
    canonical = by_id.get(canonical_id)
    if duplicate is None:
        continue
    if canonical is None:
        duplicate["id"] = canonical_id
        duplicate["registry_id"] = canonical_id
        by_id[canonical_id] = duplicate
        del by_id[duplicate_id]
    else:
        # Preserve the established canonical ID while enriching incomplete metadata.
        for key, value in duplicate.items():
            if key in {"id", "registry_id", "used_by_unit_ids"}:
                continue
            if not canonical.get(key):
                canonical[key] = value
        canonical_units = list(canonical.get("used_by_unit_ids", []))
        for unit_id in duplicate.get("used_by_unit_ids", []):
            if unit_id not in canonical_units:
                canonical_units.append(unit_id)
        canonical["used_by_unit_ids"] = canonical_units

sources_doc["sources"] = [item for item in sources if item["id"] not in source_mapping]
# If a duplicate was renamed because canonical was absent, normalize registry IDs.
for item in sources_doc["sources"]:
    if item["id"] in {"consort-ai", "spirit-ai"}:
        item["registry_id"] = item["id"]
save(sources_path, sources_doc)

# Rewrite duplicate source references everywhere else in the canonical course.
for path in sorted(COURSE.rglob("*.json")):
    if path == sources_path:
        continue
    data = load(path)
    rewritten = replace_exact(data, source_mapping)
    if rewritten != data:
        save(path, rewritten)

# ---------------------------------------------------------------------------
# 2. Complete course metadata without claiming human review.
# ---------------------------------------------------------------------------
course_path = COURSE / "course.json"
course = load(course_path)
course["content_version"] = "0.2.0"
course["status"].update({
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
})
course["scope"] = {
    "included": [
        "Formulación de problemas de predicción clínica con uso previsto, población, momento índice, horizonte, desenlace y estimando explícitos.",
        "Construcción y auditoría de cohortes, etiquetas, predictores, faltantes, procedencia y particiones con prevención de fuga de información.",
        "Desarrollo reproducible de baselines y modelos candidatos mediante pipelines, regularización, ensambles y selección de hiperparámetros dentro del desarrollo.",
        "Validación interna con bootstrap, validación cruzada y diseños anidados, incluyendo optimismo, incertidumbre, estabilidad y suficiencia de información.",
        "Validación externa, transportabilidad, heterogeneidad entre entornos, recalibración y actualización con separación entre adaptación y confirmación.",
        "Evaluación multidimensional de discriminación, calibración, error probabilístico, umbrales, precision-recall, decision curve analysis y net benefit.",
        "Riesgo de sesgo, aplicabilidad, subgrupos, fairness, proxies, atajos, explicabilidad y factores humanos del equipo humano-IA.",
        "Evaluación prospectiva, integración, monitorización, drift, control de cambios, PCCP, incidentes, retirada y ciclo de vida del sistema clínico.",
    ],
    "excluded": [
        "Estimación causal de efectos de tratamiento como objetivo principal; la predicción no se presenta como sustituto de inferencia causal.",
        "Desarrollo exhaustivo de arquitecturas profundas, visión por computador, NLP o modelos fundacionales; se prioriza el procedimiento de validación clínica sobre una familia algorítmica concreta.",
        "Autorización regulatoria, certificación de dispositivos médicos o asesoría jurídica; las guías regulatorias se usan con finalidad educativa y de diseño responsable.",
        "Despliegue real sobre pacientes o sistemas hospitalarios; las actividades emplean escenarios educativos, datos sintéticos, abiertos o debidamente autorizados.",
    ],
    "handoff_courses": [
        "bioestadistica",
        "epidemiologia-metodos-investigacion-clinica",
        "sistemas-ayuda-decision-medica",
        "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas",
    ],
}
course["editorial_notice"] = (
    "Curso completo en contenido y pedagogía canónicos, pendiente de revisión humana interna y externa. "
    "Las fuentes y afirmaciones están trazadas de forma provisional; el material es educativo y no autoriza "
    "decisiones clínicas, despliegues ni conclusiones regulatorias."
)
save(course_path, course)

# ---------------------------------------------------------------------------
# 3. Replace the migrated course assessment with a complete assessment system.
# ---------------------------------------------------------------------------
assessment_path = COURSE / "assessments" / "course-assessment.json"
assessment = {
    "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
    "schema_version": "1.0",
    "id": "MLBIO-EVAL-CURSO",
    "course_id": "machine-learning-biomedico-validacion-clinica",
    "scope": "course",
    "principles": [
        "La evaluación comienza por el uso previsto, la decisión clínica, la población, el momento índice y el desenlace; una métrica aislada nunca sustituye esa especificación.",
        "Toda transformación, selección, ajuste, calibración o elección de umbral se considera parte del procedimiento y debe respetar la separación entre desarrollo y evaluación.",
        "El desempeño se interpreta de forma multidimensional mediante discriminación, calibración, error probabilístico, umbrales, utilidad, incertidumbre y comparación con alternativas reales.",
        "Las conclusiones de transportabilidad se limitan a poblaciones, periodos y entornos evaluados; adaptar un modelo consume independencia y crea una versión nueva que necesita evidencia propia.",
        "Las auditorías de sesgo, aplicabilidad y subgrupos incluyen denominadores, incertidumbre y contexto y no convierten diferencias observadas en explicaciones causales automáticas.",
        "Las explicaciones del modelo se evalúan por fidelidad, estabilidad y utilidad para una tarea; no se aceptan como evidencia causal ni como sustituto de validación.",
        "El objeto clínico final es un sistema sociotécnico: modelo, datos, interfaz, usuarios, flujo, contingencia, monitorización, cambios e incidentes forman parte de la evidencia.",
        "Código, versiones, semillas, procedencia, decisiones, desviaciones del protocolo y limitaciones deben quedar registrados para que el trabajo pueda auditarse y reproducirse.",
        "La retroalimentación formativa precede a la evaluación sumativa y las correcciones se conservan como versiones trazables en lugar de sobrescribir silenciosamente decisiones previas.",
        "Todo ejercicio tiene finalidad educativa; ningún resultado de curso constituye recomendación clínica, autorización de despliegue ni asesoría regulatoria."
    ],
    "assessment_plan": [
        {
            "id": "MLBIO-PLAN-01",
            "component": "Autoevaluaciones razonadas de las ocho unidades",
            "type": "formative_with_low_stakes_grade",
            "weight_percent": 15,
            "linked_learning_outcome_ids": [f"MLBIO-LO{i:02d}" for i in range(1, 9)],
            "evidence_files": [f"assessments/unit-{i:02d}.json" for i in range(1, 9)],
            "description": "Ocho evaluaciones por casos que exigen cálculo, análisis o decisión y una justificación compatible con el uso previsto, las fuentes y los límites de inferencia.",
            "feedback_and_revision": "La clave razonada se consulta después del primer intento. Cada error importante se clasifica —diseño, fuga, métrica, interpretación, aplicabilidad, factores humanos o ciclo de vida— y se corrige antes de cerrar la unidad."
        },
        {
            "id": "MLBIO-PLAN-02",
            "component": "Portafolio de actividades aplicadas",
            "type": "performance_tasks",
            "weight_percent": 25,
            "linked_learning_outcome_ids": [f"MLBIO-LO{i:02d}" for i in range(1, 9)],
            "evidence_ids": [f"MLBIO-U{i:02d}-ACT01" for i in range(1, 9)],
            "description": "Portafolio progresivo con protocolo, auditoría de datos, comparación reproducible de modelos, validación interna, validación externa, informe de desempeño, auditoría humano-IA y plan prospectivo de ciclo de vida.",
            "feedback_and_revision": "Cada actividad se entrega con sus criterios de comprobación. La versión revisada conserva la versión inicial y una nota de cambios que explica qué evidencia motivó cada corrección."
        },
        {
            "id": "MLBIO-PLAN-03",
            "component": "Examen integrador intermedio",
            "type": "individual_integrative_exam",
            "weight_percent": 20,
            "linked_learning_outcome_ids": ["MLBIO-LO01", "MLBIO-LO02", "MLBIO-LO03", "MLBIO-LO04"],
            "evidence_reference": "midterm_blueprint",
            "description": "Examen individual después de la Unidad 4 con un caso nuevo que obliga a formular el problema, auditar datos, construir el procedimiento y diseñar validación interna sin fuga.",
            "feedback_and_revision": "Se devuelve retroalimentación por dominio. Errores que comprometan temporalidad, independencia, fuga o evaluación requieren una corrección razonada antes de avanzar al bloque de validación externa."
        },
        {
            "id": "MLBIO-PLAN-04",
            "component": "Proyecto integrador de validación clínica",
            "type": "capstone_project",
            "weight_percent": 30,
            "linked_learning_outcome_ids": [f"MLBIO-LO{i:02d}" for i in range(1, 9)],
            "evidence_reference": "capstone",
            "description": "Evaluación completa de un sistema predictivo biomédico desde protocolo y cohorte hasta validación externa, utilidad, auditoría humano-IA y plan prospectivo de ciclo de vida.",
            "feedback_and_revision": "El protocolo, el modelo bloqueado y el plan prospectivo reciben una ronda de revisión antes del informe final. Toda modificación inducida por resultados de evaluación se registra como nueva versión y se distingue de la evidencia independiente."
        },
        {
            "id": "MLBIO-PLAN-05",
            "component": "Defensa crítica y bitácora de decisiones",
            "type": "oral_and_process_evidence",
            "weight_percent": 10,
            "linked_learning_outcome_ids": ["MLBIO-LO01", "MLBIO-LO04", "MLBIO-LO05", "MLBIO-LO06", "MLBIO-LO07", "MLBIO-LO08"],
            "evidence_ids": ["MLBIO-CAP-D07", "MLBIO-CAP-D08", "MLBIO-CAP-D09"],
            "description": "Defensa individual de decisiones metodológicas, comparación con alternativas, límites de transportabilidad, riesgos, cambios y criterios que impedirían desplegar el sistema.",
            "feedback_and_revision": "La defensa puede identificar una corrección final, pero una nueva cifra obtenida tras modificar el sistema no se presenta como evidencia independiente si reutiliza datos ya inspeccionados."
        }
    ],
    "diagnostic": {
        "id": "MLBIO-DIAG-01",
        "title": "Diagnóstico de prerrequisitos para Machine Learning Biomédico",
        "purpose": "Detectar brechas en probabilidad, regresión, programación reproducible, diseño de estudios y razonamiento clínico predictivo. No aporta calificación.",
        "administration": {
            "timing": "Antes de iniciar la Unidad 1.",
            "conditions": "Intento individual sin consultar la clave; se solicita una justificación breve cuando una respuesta depende de supuestos.",
            "use_of_results": "Los dominios fallados generan rutas de nivelación y no excluyen del curso ni reducen la calificación."
        },
        "scoring": {
            "points_per_question": 1,
            "maximum_points": 10,
            "rule": "Se concede el punto cuando la respuesta contiene la distinción conceptual indicada en evidence_of_readiness; diferencias de redacción no penalizan.",
            "partial_credit": "La respuesta parcial se conserva para orientar la nivelación, aunque la clasificación diagnóstica utiliza puntos enteros."
        },
        "questions": [
            {"id":"MLBIO-DIAG-Q01","domain":"predicción y causalidad","prerequisite_ids":["MLBIO-PRE03","MLBIO-PRE05"],"question":"¿Por qué un predictor asociado con un desenlace no identifica automáticamente una intervención eficaz?","answer":"Porque la capacidad predictiva describe asociación útil fuera de muestra; estimar el efecto de intervenir exige un contraste causal, diseño y supuestos adicionales.","evidence_of_readiness":"Distingue predicción de efecto causal."},
            {"id":"MLBIO-DIAG-Q02","domain":"unidad independiente","prerequisite_ids":["MLBIO-PRE03"],"question":"Un paciente aporta cinco ingresos. ¿Por qué una división aleatoria por filas puede ser inválida?","answer":"Porque ingresos del mismo paciente pueden quedar en entrenamiento y evaluación, compartiendo información y rompiendo la independencia relevante.","evidence_of_readiness":"Identifica dependencia y riesgo de fuga entre particiones."},
            {"id":"MLBIO-DIAG-Q03","domain":"regresión probabilística","prerequisite_ids":["MLBIO-PRE01","MLBIO-PRE04"],"question":"¿Qué diferencia existe entre una probabilidad predicha y una clasificación binaria?","answer":"La probabilidad expresa riesgo en una escala continua; la clasificación aparece al aplicar un umbral y depende de la acción y consecuencias definidas.","evidence_of_readiness":"Separa estimación de riesgo y regla de decisión."},
            {"id":"MLBIO-DIAG-Q04","domain":"reproducibilidad","prerequisite_ids":["MLBIO-PRE02"],"question":"¿Qué elementos mínimos permiten reconstruir un pipeline entrenado?","answer":"Código y dependencias versionados, datos o procedencia, transformaciones, parámetros e hiperparámetros, particiones o semillas y artefacto final identificable.","evidence_of_readiness":"Reconoce la versión del procedimiento completo y no solo el archivo del modelo."},
            {"id":"MLBIO-DIAG-Q05","domain":"regularización","prerequisite_ids":["MLBIO-PRE01","MLBIO-PRE04"],"question":"¿Qué problema intenta controlar una penalización L1 o L2?","answer":"Controla complejidad y magnitud efectiva de parámetros para reducir sobreajuste; L1 puede llevar coeficientes a cero y L2 contrae magnitudes.","evidence_of_readiness":"Comprende regularización como control de complejidad."},
            {"id":"MLBIO-DIAG-Q06","domain":"validación","prerequisite_ids":["MLBIO-PRE01","MLBIO-PRE03"],"question":"¿Por qué ajustar hiperparámetros y reportar la misma validación cruzada produce optimismo?","answer":"Porque los resultados de esa validación influyeron en la selección del ganador; se necesita una capa de evaluación que no participe en la elección.","evidence_of_readiness":"Distingue selección de evaluación."},
            {"id":"MLBIO-DIAG-Q07","domain":"discriminación y calibración","prerequisite_ids":["MLBIO-PRE01"],"question":"¿Puede un modelo mantener AUC alta y estar mal calibrado?","answer":"Sí. AUC resume ranking, mientras calibración evalúa correspondencia de probabilidades con frecuencias observadas.","evidence_of_readiness":"Distingue dos dimensiones de desempeño."},
            {"id":"MLBIO-DIAG-Q08","domain":"prevalencia y PPV","prerequisite_ids":["MLBIO-PRE01"],"question":"Si sensibilidad y especificidad permanecen iguales pero el evento se vuelve mucho más raro, ¿qué suele ocurrir con PPV?","answer":"Disminuye porque entre las predicciones positivas aumenta la contribución relativa de falsos positivos provenientes del gran número de no eventos.","evidence_of_readiness":"Relaciona valores predictivos con prevalencia."},
            {"id":"MLBIO-DIAG-Q09","domain":"fuga temporal","prerequisite_ids":["MLBIO-PRE03","MLBIO-PRE05"],"question":"¿Qué pregunta permite detectar fuga temporal en un predictor clínico?","answer":"Si el valor estaría realmente disponible, con la misma definición, en el momento exacto en que el sistema debería emitir la predicción prospectiva.","evidence_of_readiness":"Evalúa disponibilidad desde el momento de uso previsto."},
            {"id":"MLBIO-DIAG-Q10","domain":"ciclo de vida","prerequisite_ids":["MLBIO-PRE03","MLBIO-PRE05"],"question":"¿Por qué una actualización del umbral crea una versión clínicamente relevante aunque los pesos del modelo no cambien?","answer":"Porque modifica quién recibe una acción y puede alterar beneficio, daño, carga y desempeño operacional; debe versionarse y reevaluarse.","evidence_of_readiness":"Entiende el sistema como algo más amplio que los parámetros del algoritmo."}
        ],
        "interpretation": [
            {"range":"8–10 respuestas correctas","readiness":"preparado","action":"Iniciar la Unidad 1 y revisar únicamente los dominios fallados."},
            {"range":"5–7 respuestas correctas","readiness":"nivelación paralela","action":"Completar repaso de probabilidad, regresión, particiones, pipelines y diseño clínico mientras se inicia la Unidad 1."},
            {"range":"0–4 respuestas correctas","readiness":"nivelación prioritaria","action":"Revisar Bioestadística, programación reproducible y fundamentos de estudios predictivos antes de avanzar a desarrollo de modelos."}
        ]
    },
    "midterm_blueprint": [
        {
            "id": "MLBIO-MID-01",
            "domain": "Uso previsto y protocolo predictivo",
            "weight_percent": 20,
            "linked_learning_outcome_ids": ["MLBIO-LO01"],
            "task": "A partir de una necesidad clínica nueva, definir población, usuario, momento índice, horizonte, desenlace, unidad independiente, acción y criterio de éxito sin elegir todavía el algoritmo.",
            "evidence_of_mastery": ["La pregunta es prospectivamente evaluable.", "No confunde predicción con causalidad.", "Predictores y desenlace tienen temporalidad reproducible."]
        },
        {
            "id": "MLBIO-MID-02",
            "domain": "Cohorte, etiquetas y fuga",
            "weight_percent": 25,
            "linked_learning_outcome_ids": ["MLBIO-LO02"],
            "task": "Auditar una cohorte con mediciones repetidas, faltantes, códigos administrativos y variables posteriores al tiempo cero; corregir selección, etiquetas y particiones.",
            "evidence_of_mastery": ["La partición respeta la unidad independiente.", "Distingue proceso asistencial de señal biológica.", "Toda transformación aprendida se mantiene dentro del desarrollo."]
        },
        {
            "id": "MLBIO-MID-03",
            "domain": "Pipeline, baseline y selección",
            "weight_percent": 25,
            "linked_learning_outcome_ids": ["MLBIO-LO03"],
            "task": "Diseñar un pipeline reproducible que compare una referencia simple con un modelo candidato y seleccione hiperparámetros sin tocar la evaluación reservada.",
            "evidence_of_mastery": ["Existe baseline defendible.", "Preprocesamiento y selección viven dentro del pipeline.", "La regla de selección considera incertidumbre, simplicidad y relevancia clínica."]
        },
        {
            "id": "MLBIO-MID-04",
            "domain": "Validación interna, optimismo e incertidumbre",
            "weight_percent": 30,
            "linked_learning_outcome_ids": ["MLBIO-LO04"],
            "task": "Elegir bootstrap, validación cruzada o diseño anidado para un caso con pocos eventos y múltiples candidatos; explicar qué se estima y cómo se cuantifica estabilidad.",
            "evidence_of_mastery": ["Selección y evaluación están separadas.", "El remuestreo repite el procedimiento completo.", "La incertidumbre no trata folds como réplicas independientes.", "La decisión reconoce estabilidad y suficiencia de información."]
        }
    ],
    "capstone": {
        "id": "MLBIO-CAP-01",
        "title": "Evaluación completa y plan de ciclo de vida de un modelo predictivo biomédico",
        "purpose": "Integrar las ocho unidades en un producto auditable que permita decidir si una versión predictiva merece avanzar desde desarrollo hacia evaluación clínica prospectiva, incluyendo las razones para no avanzar.",
        "data_policy": "Usar datos sintéticos, abiertos o debidamente autorizados. No incorporar información clínica identificable ni desplegar resultados sobre pacientes reales como parte del curso.",
        "linked_learning_outcome_ids": [f"MLBIO-LO{i:02d}" for i in range(1, 9)],
        "phases": [
            {"id":"MLBIO-CAP-P01","title":"Protocolo y uso previsto","linked_learning_outcome_ids":["MLBIO-LO01"],"exit_criterion":"La pregunta, población, temporalidad, desenlace, acción, comparador y criterio de éxito están bloqueados antes del análisis."},
            {"id":"MLBIO-CAP-P02","title":"Cohorte y auditoría de datos","linked_learning_outcome_ids":["MLBIO-LO02"],"exit_criterion":"Diccionario, procedencia, faltantes, etiquetas, unidad independiente y particiones permiten reconstruir la cohorte sin fuga."},
            {"id":"MLBIO-CAP-P03","title":"Desarrollo reproducible","linked_learning_outcome_ids":["MLBIO-LO03"],"exit_criterion":"Baseline y candidato se comparan dentro de pipelines reproducibles y el modelo final queda bloqueado y versionado."},
            {"id":"MLBIO-CAP-P04","title":"Validación interna","linked_learning_outcome_ids":["MLBIO-LO04"],"exit_criterion":"Optimismo, incertidumbre, estabilidad y suficiencia de información se cuantifican mediante un diseño coherente con la unidad independiente."},
            {"id":"MLBIO-CAP-P05","title":"Validación externa y desempeño decisional","linked_learning_outcome_ids":["MLBIO-LO05","MLBIO-LO06"],"exit_criterion":"La versión bloqueada se evalúa sin refitting y se reportan transportabilidad, calibración, discriminación, utilidad, umbrales e incertidumbre."},
            {"id":"MLBIO-CAP-P06","title":"Sesgo, subgrupos y equipo humano-IA","linked_learning_outcome_ids":["MLBIO-LO07"],"exit_criterion":"PROBAST+AI, subgrupos, proxies, explicaciones y factores humanos producen juicios separados, trazables y accionables."},
            {"id":"MLBIO-CAP-P07","title":"Evaluación prospectiva y ciclo de vida","linked_learning_outcome_ids":["MLBIO-LO08"],"exit_criterion":"Existe escalera de evidencia, mapa operacional, monitorización accionable, control de cambios e incidentes y criterio explícito de suspensión o retirada."}
        ],
        "deliverables": [
            {"id":"MLBIO-CAP-D01","title":"Protocolo predictivo y ficha de uso previsto","linked_learning_outcome_ids":["MLBIO-LO01"]},
            {"id":"MLBIO-CAP-D02","title":"Diccionario, procedencia y mapa de riesgos de datos","linked_learning_outcome_ids":["MLBIO-LO02"]},
            {"id":"MLBIO-CAP-D03","title":"Repositorio reproducible, baseline, modelo candidato y manifiesto de versión bloqueada","linked_learning_outcome_ids":["MLBIO-LO03"]},
            {"id":"MLBIO-CAP-D04","title":"Informe de validación interna, incertidumbre y estabilidad","linked_learning_outcome_ids":["MLBIO-LO04"]},
            {"id":"MLBIO-CAP-D05","title":"Informe de validación externa, calibración, discriminación y utilidad clínica","linked_learning_outcome_ids":["MLBIO-LO05","MLBIO-LO06"]},
            {"id":"MLBIO-CAP-D06","title":"Auditoría PROBAST+AI, subgrupos, proxies, explicabilidad y factores humanos","linked_learning_outcome_ids":["MLBIO-LO07"]},
            {"id":"MLBIO-CAP-D07","title":"Plan prospectivo, integración y monitorización","linked_learning_outcome_ids":["MLBIO-LO08"]},
            {"id":"MLBIO-CAP-D08","title":"Bitácora de decisiones, versiones, desviaciones y limitaciones","linked_learning_outcome_ids":["MLBIO-LO01","MLBIO-LO04","MLBIO-LO05","MLBIO-LO08"]},
            {"id":"MLBIO-CAP-D09","title":"Defensa crítica con decisión de avanzar, limitar, actualizar o detener","linked_learning_outcome_ids":["MLBIO-LO05","MLBIO-LO06","MLBIO-LO07","MLBIO-LO08"]}
        ],
        "rubric": [
            {"id":"MLBIO-RUB-01","criterion":"Pregunta, uso previsto y protocolo","weight_percent":12,"linked_learning_outcome_ids":["MLBIO-LO01"],"performance_levels":{"insufficient":"La pregunta cambia con los resultados o no define temporalidad, población, desenlace y acción.","developing":"Define la pregunta principal, pero deja ambiguos uno o más elementos que impiden evaluar prospectivamente el uso.","competent":"Define y bloquea población, usuario, momento índice, horizonte, desenlace, unidad independiente, acción, comparador y criterio de éxito.","excellent":"Además anticipa escenarios de no pertinencia, límites de inferencia y decisiones que harían innecesario el modelo."}},
            {"id":"MLBIO-RUB-02","criterion":"Cohorte, etiquetas, procedencia y fuga","weight_percent":12,"linked_learning_outcome_ids":["MLBIO-LO02"],"performance_levels":{"insufficient":"No puede reconstruirse la cohorte o existe fuga material entre desarrollo y evaluación.","developing":"La cohorte es parcialmente reproducible, pero faltan controles de temporalidad, dependencia o procedencia.","competent":"Diccionario, criterios, etiquetas, faltantes, procedencia y particiones son reproducibles y respetan la unidad independiente.","excellent":"Además audita señales de proceso, sensibilidad a definiciones y riesgos de medición o selección con acciones concretas."}},
            {"id":"MLBIO-RUB-03","criterion":"Desarrollo reproducible y comparación con baseline","weight_percent":13,"linked_learning_outcome_ids":["MLBIO-LO03"],"performance_levels":{"insufficient":"Preprocesamiento o selección usan evaluación; no existe baseline defendible ni versión reproducible.","developing":"Existe pipeline y candidato, pero la selección o documentación deja decisiones implícitas.","competent":"Pipeline, baseline, candidato, tuning y regla de selección están separados de la evaluación y producen una versión bloqueada identificable.","excellent":"Además demuestra estabilidad de decisiones, simplicidad justificable, mantenibilidad y sensibilidad razonable a elecciones de modelado."}},
            {"id":"MLBIO-RUB-04","criterion":"Validación interna, optimismo e incertidumbre","weight_percent":13,"linked_learning_outcome_ids":["MLBIO-LO04"],"performance_levels":{"insufficient":"Reporta rendimiento aparente o reutiliza la selección como evaluación independiente.","developing":"Aplica remuestreo pero no repite el procedimiento completo o interpreta mal la incertidumbre.","competent":"Elige bootstrap/CV/anidación coherentes, repite el pipeline y reporta optimismo, incertidumbre y estabilidad.","excellent":"Además relaciona tamaño muestral, variabilidad de selección y riesgos individuales con la decisión de bloquear o simplificar el modelo."}},
            {"id":"MLBIO-RUB-05","criterion":"Validación externa, calibración y utilidad","weight_percent":15,"linked_learning_outcome_ids":["MLBIO-LO05","MLBIO-LO06"],"performance_levels":{"insufficient":"Ajusta con la prueba externa o reduce la conclusión a AUC sin calibración ni consecuencias.","developing":"Mantiene independencia pero el análisis de transportabilidad, umbrales o utilidad es incompleto.","competent":"Evalúa versión bloqueada, diferencias de contexto, discriminación, calibración, error, umbrales, net benefit e incertidumbre y separa actualización de confirmación.","excellent":"Además caracteriza heterogeneidad, capacidad asistencial y criterios explícitos para restringir, recalibrar o rechazar la versión."}},
            {"id":"MLBIO-RUB-06","criterion":"Sesgo, subgrupos, explicabilidad y factores humanos","weight_percent":13,"linked_learning_outcome_ids":["MLBIO-LO07"],"performance_levels":{"insufficient":"Usa una puntuación superficial de sesgo o interpreta brechas/explicaciones como causalidad demostrada.","developing":"Identifica riesgos principales pero sin incertidumbre, pruebas de proxy o evaluación de interacción humana suficiente.","competent":"Separa calidad, sesgo y aplicabilidad; reporta subgrupos con denominadores; audita proxies/explicaciones y diseña evaluación del equipo humano-IA.","excellent":"Además conecta cada hallazgo con daño, decisión, mitigación, límites éticos y evidencia adicional necesaria."}},
            {"id":"MLBIO-RUB-07","criterion":"Evaluación prospectiva y ciclo de vida","weight_percent":12,"linked_learning_outcome_ids":["MLBIO-LO08"],"performance_levels":{"insufficient":"Propone despliegue directo o monitorización sin denominadores, contingencia ni control de cambios.","developing":"Incluye monitorización y versiones, pero faltan acciones predefinidas, evidencia por fases o respuesta a incidentes.","competent":"Diseña fase silenciosa/temprana/impacto, mapa operacional, monitorización accionable, cambios versionados y retirada segura.","excellent":"Además anticipa contaminación, etiquetas retrasadas, drift no clínico, rollback y criterios verificables de reintroducción o retirada definitiva."}},
            {"id":"MLBIO-RUB-08","criterion":"Reproducibilidad, comunicación y límites","weight_percent":10,"linked_learning_outcome_ids":["MLBIO-LO01","MLBIO-LO05","MLBIO-LO06","MLBIO-LO08"],"performance_levels":{"insufficient":"No puede reconstruirse qué versión produjo los resultados o se omiten limitaciones materiales.","developing":"La documentación permite seguir el análisis, pero faltan decisiones, desviaciones o mensajes adaptados a usuarios.","competent":"Versiones, procedencia, decisiones, desviaciones, incertidumbre y límites son auditables y la comunicación distingue evidencia de hipótesis.","excellent":"Además la defensa identifica activamente condiciones que invalidarían conclusiones, cambiarían el uso previsto o impedirían el avance del sistema."}}
        ],
        "source_ids": ["tripod-ai", "probast-ai", "decide-ai", "imdrf-fda-gmlp", "fda-transparency-mlmd", "fda-pccp-mlmd", "consort-ai", "spirit-ai"]
    },
    "status": "curated_pending_expert_review"
}
save(assessment_path, assessment)

# ---------------------------------------------------------------------------
# 4. Add durable tests for course-level completion.
# ---------------------------------------------------------------------------
test_path = ROOT / "tests" / "test_academic_course_schema.py"
text = test_path.read_text(encoding="utf-8")
if "test_machine_learning_course_assessment_is_complete" not in text:
    marker = "    def test_renderer_prefers_the_canonical_unit(self) -> None:\n"
    addition = '''    def test_machine_learning_course_assessment_is_complete(self) -> None:\n        course_dir = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"\n        course = json.loads((course_dir / "course.json").read_text(encoding="utf-8"))\n        assessment = json.loads((course_dir / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))\n        outcomes = {item["id"] for item in course["learning_outcomes"]}\n        plan_outcomes = {outcome_id for item in assessment["assessment_plan"] for outcome_id in item["linked_learning_outcome_ids"]}\n        capstone_outcomes = set(assessment["capstone"]["linked_learning_outcome_ids"])\n        self.assertEqual(assessment["status"], "curated_pending_expert_review")\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)\n        self.assertEqual(plan_outcomes, outcomes)\n        self.assertEqual(capstone_outcomes, outcomes)\n        self.assertTrue(assessment["midterm_blueprint"])\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["midterm_blueprint"]), 100)\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["capstone"]["rubric"]), 100)\n        self.assertTrue(all(len(item["performance_levels"]) == 4 for item in assessment["capstone"]["rubric"]))\n        self.assertGreaterEqual(len(assessment["capstone"]["deliverables"]), 8)\n        self.assertEqual(course["status"]["content"], "complete")\n        self.assertEqual(course["status"]["pedagogy"], "complete")\n        self.assertEqual(course["status"]["sources"], "traceable")\n        source_ids = [item["id"] for item in json.loads((course_dir / "sources.json").read_text(encoding="utf-8"))["sources"]]\n        self.assertEqual(len(source_ids), len(set(source_ids)))\n        self.assertNotIn("consort-ai-2020", source_ids)\n        self.assertNotIn("spirit-ai-2020", source_ids)\n\n'''
    if marker not in text:
        raise RuntimeError("No se encontró punto de inserción para prueba de cierre ML")
    text = text.replace(marker, addition + marker)
test_path.write_text(text, encoding="utf-8")

print("Curso ML biomédico cerrado: metadatos, evaluación integradora, rúbrica y fuentes consolidadas.")
