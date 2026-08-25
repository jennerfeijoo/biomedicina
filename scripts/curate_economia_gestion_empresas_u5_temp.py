#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-05.json"
GENERIC = "Concepto de la unidad que debe definirse mediante entidades observables"


def dump(payload: dict) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    SOURCE.write_text(text, encoding="utf-8")
    MIRROR.write_text(text, encoding="utf-8")


def main() -> None:
    unit = json.loads(SOURCE.read_text(encoding="utf-8"))
    unit["purpose"] = (
        "Construir e interpretar una evaluación económica sanitaria reproducible para alternativas sintéticas mediante un problema de decisión explícito, "
        "comparadores relevantes, perspectiva, horizonte temporal, costes y consecuencias, análisis incremental, impacto presupuestario y análisis de incertidumbre. "
        "La unidad separa coste-efectividad de asequibilidad y de decisión de financiación, y evita confundir análisis de sensibilidad económica con sensibilidad diagnóstica."
    )
    unit["learning_objectives"] = [
        "Definir una evaluación económica como comparación de alternativas en términos de costes y consecuencias, especificando población o contexto, comparadores, perspectiva, horizonte temporal y medida de resultado.",
        "Calcular diferencias incrementales de costes y efectos, reconocer dominancia y obtener un ICER cuando sea interpretable, conservando unidades y evitando usar un umbral de disposición a pagar como si fuera universal.",
        "Usar beneficio monetario neto con un valor umbral explícitamente hipotético o jurisdiccional para comparar alternativas y explicar cómo cambia la decisión cuando cambia ese valor.",
        "Distinguir evaluación de coste-efectividad de análisis de impacto presupuestario, identificando población elegible, adopción, mezcla tecnológica, recursos, costes y perspectiva del responsable del presupuesto.",
        "Aplicar análisis de sensibilidad determinista, de escenarios, de umbral y probabilístico de forma proporcional al modelo, diferenciando incertidumbre de parámetros, estructural, metodológica y heterogeneidad.",
        "Comunicar un análisis económico sintético con trazabilidad de fuentes, supuestos, incertidumbre y límites, sin convertir una razón coste-efectividad favorable en recomendación automática de reembolso, compra o uso clínico."
    ]
    unit["theory_sections"] = [
        {
            "heading": "1. Problema de decisión, comparadores, perspectiva y horizonte",
            "paragraphs": [
                "Una evaluación económica sanitaria compara cursos de acción alternativos en términos de costes y consecuencias. El análisis empieza antes de cualquier fórmula: debe declarar qué decisión se estudia, para qué población o contexto, qué alternativas son relevantes y qué resultado se pretende informar. Si se compara una tecnología nueva solo contra una alternativa débil y se omite el estándar de cuidado pertinente, el cálculo puede ser impecable y la pregunta seguir siendo inadecuada.",
                "La perspectiva determina qué costes y consecuencias entran en el análisis. Una perspectiva del sistema sanitario puede incluir recursos sanitarios asumidos por ese sistema; una perspectiva social puede incorporar consecuencias fuera del sector sanitario según las reglas metodológicas aplicables. No existe una lista universal de costes válida para cualquier contexto: la perspectiva y el marco de referencia deben declararse, y las exclusiones relevantes deben justificarse.",
                "El horizonte temporal debe ser suficientemente largo para capturar las diferencias importantes entre alternativas. Un dispositivo con un coste inicial alto y beneficios distribuidos durante años puede parecer desfavorable si se analiza únicamente el primer mes. A la inversa, extrapolar durante décadas sin evidencia suficiente puede crear precisión aparente. El horizonte, los supuestos de extrapolación y las fuentes que sostienen la persistencia de efectos deben quedar visibles.",
                "Las consecuencias pueden medirse de distintas formas según la pregunta. En análisis de coste-utilidad se usan con frecuencia años de vida ajustados por calidad, QALYs, que combinan tiempo y utilidad relacionada con salud. Un QALY no es una medida directa de dinero ni una valoración moral de una persona; es una unidad analítica de resultado sanitario. Otros análisis pueden utilizar desenlaces naturales o comparar costes cuando los efectos relevantes se consideran suficientemente similares bajo un marco metodológico justificado.",
                "El descuento lleva costes o efectos futuros a valor presente mediante una tasa definida por el marco metodológico aplicable. La tasa no debe memorizarse como constante universal: distintas jurisdicciones establecen referencias diferentes y pueden cambiarlas. En esta unidad se practica con tasas sintéticas y se documenta siempre el año, la tasa, la convención y si se descontaron costes, efectos o ambos."
            ],
            "equations": [
                {"latex": "QALY=\\sum_j u_j\\,\\Delta t_j", "meaning": "Aproximación discreta de QALYs como suma del tiempo en cada estado ponderado por su utilidad relacionada con salud.", "variables": {"u_j": "utilidad del estado j", "\\Delta t_j": "duración en años del estado j"}},
                {"latex": "PV(X_t)=\\frac{X_t}{(1+r)^t}", "meaning": "Valor presente de un coste o efecto futuro bajo una tasa de descuento declarada.", "variables": {"X_t": "coste o efecto en el periodo t", "r": "tasa de descuento por periodo", "t": "número de periodos"}}
            ],
            "key_points": [
                "La evaluación económica es comparativa: la selección del comparador forma parte del método.",
                "Perspectiva y horizonte determinan qué costes y consecuencias son relevantes.",
                "QALY es una unidad de resultado sanitario utilizada en coste-utilidad, no una cantidad monetaria.",
                "La tasa de descuento depende del marco metodológico y debe declararse, no suponerse universal."
            ]
        },
        {
            "heading": "2. Análisis incremental, dominancia, ICER y beneficio monetario neto",
            "paragraphs": [
                "El análisis económico se centra en diferencias entre alternativas, no en cocientes aislados de coste total por efecto total. Para dos opciones A y B se calculan el coste incremental y el efecto incremental. Estos incrementos indican qué se gana o pierde al pasar del comparador a la alternativa evaluada. Mantener la dirección de la resta es esencial: cambiar el orden a mitad del cálculo cambia los signos y puede invertir la interpretación.",
                "Una alternativa es estrictamente dominante cuando produce mejores resultados y menor coste que otra dentro del modelo; una alternativa dominada es más costosa y menos efectiva. Con más de dos opciones, el análisis completamente incremental ordena alternativas y puede detectar dominancia extendida. Antes de calcular un ICER se debe comprobar si la comparación está dominada y si el denominador tiene una magnitud que permita una interpretación estable.",
                "El ICER expresa el coste adicional por unidad adicional de efecto: por ejemplo, euros por QALY ganado. No es una probabilidad de que una tecnología sea coste-efectiva y no debe interpretarse sin sus unidades. Además, un ICER no decide por sí mismo: su relevancia depende del marco de decisión, del umbral o coste de oportunidad utilizado, de incertidumbre, equidad, evidencia y otros criterios que la institución considere.",
                "El beneficio monetario neto transforma efectos y costes a una escala común mediante un valor lambda que representa cuánto se valora una unidad adicional de efecto dentro de un marco de decisión. El NMB incremental positivo favorece económicamente a la alternativa bajo ese lambda y esos supuestos, pero lambda no es una constante universal. En ejercicios docentes se usa un valor hipotético explícito; en evaluaciones reales debe justificarse según el contexto y la autoridad correspondiente.",
                "Una cifra favorable no autoriza afirmar que una tecnología sea clínicamente superior, asequible para un presupuesto concreto o recomendada para reembolso. El análisis económico depende de la evidencia de efectos, costes, estructura del modelo y supuestos. Por eso el resultado se comunica junto con el comparador, perspectiva, horizonte, incertidumbre y datos faltantes, y nunca como una etiqueta descontextualizada de 'rentable' o 'no rentable'."
            ],
            "equations": [
                {"latex": "\\Delta C=C_A-C_B", "meaning": "Coste incremental de A respecto de B.", "variables": {"C_A": "coste esperado de A", "C_B": "coste esperado del comparador B"}},
                {"latex": "\\Delta E=E_A-E_B", "meaning": "Efecto incremental de A respecto de B.", "variables": {"E_A": "efecto esperado de A", "E_B": "efecto esperado del comparador B"}},
                {"latex": "ICER=\\frac{\\Delta C}{\\Delta E}", "meaning": "Razón coste-efectividad incremental cuando la comparación y el denominador admiten interpretación.", "variables": {"\\Delta C": "coste incremental", "\\Delta E": "efecto incremental"}},
                {"latex": "INMB=\\lambda\\Delta E-\\Delta C", "meaning": "Beneficio monetario neto incremental para un valor lambda explícito; positivo favorece A bajo ese marco.", "variables": {"\\lambda": "valor por unidad de efecto definido para el escenario", "\\Delta E": "efecto incremental", "\\Delta C": "coste incremental"}}
            ],
            "key_points": [
                "El análisis debe ser incremental y conservar una dirección de comparación consistente.",
                "Dominancia se revisa antes de interpretar un ICER.",
                "ICER tiene unidades y no es una probabilidad ni una decisión automática.",
                "INMB depende de un lambda explícito y no convierte un umbral contextual en ley universal."
            ]
        },
        {
            "heading": "3. Impacto presupuestario y asequibilidad: una pregunta diferente",
            "paragraphs": [
                "El análisis de impacto presupuestario pregunta cómo cambia el gasto de un responsable del presupuesto cuando una tecnología se introduce en una población concreta durante un horizonte operativo. Aunque comparte datos con la evaluación de coste-efectividad, responde una pregunta diferente. Una intervención puede ofrecer buen valor relativo a largo plazo y requerir, al mismo tiempo, un desembolso agregado que el presupuesto de corto plazo no pueda absorber.",
                "Un BIA debe declarar la perspectiva del pagador o decisor presupuestario, el tamaño y características de la población elegible, la mezcla actual de tecnologías, la mezcla esperada tras la introducción, la adopción por periodo, los recursos utilizados y los costes relevantes. La población no se obtiene multiplicando una prevalencia genérica sin comprobar elegibilidad, cobertura, canal y restricciones. Cada paso de población debe ser auditable.",
                "La adopción cambia con el tiempo y debe modelarse como escenario, no como certeza. Para una tecnología médica, instalación, formación, mantenimiento, consumibles, sustitución de equipos y cambios de flujo pueden alterar el presupuesto además del precio de compra. Incluir únicamente el precio del dispositivo suele subestimar o distorsionar el impacto de implementación.",
                "Las recomendaciones ISPOR de buena práctica enfatizan que el BIA debe responder a las necesidades de información del decisor específico y presentar escenarios. Por ello se exploran tasas de adopción, población, precio, utilización y sustitución alternativas. Los escenarios no deben manipularse para producir un resultado favorable: su objetivo es hacer visibles los impulsores de gasto y los rangos plausibles.",
                "Coste-efectividad y asequibilidad se reportan por separado. Un ICER favorable no demuestra que exista presupuesto disponible; un impacto presupuestario bajo tampoco demuestra que la alternativa produzca suficiente beneficio sanitario. La eventual decisión de compra o financiación incorpora además reglas institucionales, evidencia, equidad, prioridades y restricciones que están fuera del alcance de un ejercicio sintético aislado."
            ],
            "equations": [
                {"latex": "N_{tratados,t}=N_{elegibles,t}\\times p_{adopcion,t}", "meaning": "Escenario de población tratada bajo una tasa de adopción explícita por periodo.", "variables": {"N_{elegibles,t}": "población elegible en t", "p_{adopcion,t}": "proporción de adopción en t"}},
                {"latex": "BI_t=C_{nuevo,t}-C_{actual,t}", "meaning": "Impacto presupuestario incremental del escenario nuevo frente al escenario actual en el periodo t.", "variables": {"C_{nuevo,t}": "coste total del escenario con la tecnología", "C_{actual,t}": "coste total del escenario comparador"}}
            ],
            "key_points": [
                "Impacto presupuestario y coste-efectividad responden preguntas distintas.",
                "El BIA debe representar la población y las mezclas tecnológica actual y futura del decisor relevante.",
                "Precio de adquisición no equivale a coste total de implementación.",
                "Los escenarios de adopción muestran asequibilidad potencial; no son predicciones garantizadas."
            ]
        },
        {
            "heading": "4. Incertidumbre, análisis de sensibilidad, transparencia y límites de decisión",
            "paragraphs": [
                "En evaluación económica, análisis de sensibilidad significa estudiar cómo cambian los resultados al variar parámetros, supuestos, fuentes de datos o estructura del modelo. No significa sensibilidad diagnóstica. Esta distinción es crítica porque ambos términos aparecen en salud pero responden a conceptos completamente diferentes. La unidad registra explícitamente qué parámetro se modifica, por qué rango y qué resultado cambia.",
                "El análisis determinista de una vía modifica un parámetro a la vez y ayuda a identificar impulsores; el análisis de escenarios cambia conjuntos coherentes de supuestos; el análisis de umbral busca el valor en que una conclusión cambia. Estas técnicas son útiles para explicar el modelo, pero no representan necesariamente la incertidumbre conjunta de todos los parámetros. Un gráfico tornado puede resumir sensibilidad determinista, siempre que sus rangos tengan una justificación.",
                "El análisis probabilístico asigna distribuciones justificadas a parámetros inciertos y propaga conjuntamente esa incertidumbre a costes y efectos. No se eligen distribuciones por conveniencia visual. Los resultados pueden expresarse mediante nubes de coste-efecto, curvas de aceptabilidad u otras representaciones apropiadas, pero una probabilidad de coste-efectividad sigue condicionada al modelo, los datos, el lambda y los supuestos estructurales.",
                "La incertidumbre no es solo paramétrica. Puede provenir de la estructura del modelo, selección de fuentes, extrapolación, heterogeneidad o decisiones metodológicas. ISPOR-SMDM recomienda examinar y reportar estas capas y mantener transparencia suficiente para que el modelo pueda evaluarse. La validación incluye comprobación interna y comparación con evidencia o modelos externos cuando proceda; repetir un cálculo no prueba que la estructura represente adecuadamente el problema real.",
                "CHEERS 2022 orienta la transparencia del reporte de evaluaciones económicas, incluyendo contexto, métodos, resultados, incertidumbre y participación de partes interesadas. Es una guía de reporte, no un sello que garantice que un análisis sea correcto. El cierre de U5 exige un memorando sintético que permita reconstruir pregunta, comparadores, perspectiva, horizonte, fuentes, cálculos, sensibilidad y límites, y que declare qué evidencia adicional sería necesaria antes de informar una decisión real."
            ],
            "key_points": [
                "Sensibilidad económica explora incertidumbre de parámetros y supuestos; no es sensibilidad diagnóstica.",
                "Determinista, escenarios, umbral y probabilístico responden preguntas complementarias.",
                "La incertidumbre estructural y metodológica no desaparece al ejecutar una simulación probabilística.",
                "CHEERS mejora transparencia de reporte, pero no certifica validez ni justifica una decisión real por sí solo."
            ]
        }
    ]
    unit["glossary"] = [
        {"term": "evaluación económica sanitaria", "definition": "Análisis comparativo de alternativas en términos de sus costes y consecuencias para informar una decisión delimitada."},
        {"term": "problema de decisión", "definition": "Definición explícita de población o contexto, alternativas, perspectiva, horizonte, resultados y decisión que el análisis pretende informar."},
        {"term": "comparador", "definition": "Alternativa relevante frente a la que se estiman costes y consecuencias incrementales."},
        {"term": "perspectiva", "definition": "Punto de vista que determina qué categorías de costes y consecuencias son pertinentes para el análisis."},
        {"term": "horizonte temporal", "definition": "Periodo sobre el que se acumulan costes y consecuencias, suficientemente largo para captar diferencias importantes entre alternativas."},
        {"term": "coste", "definition": "Valoración de recursos consumidos según la perspectiva, fuente y método de valoración declarados; no es sinónimo automático de precio o cargo."},
        {"term": "efecto", "definition": "Consecuencia sanitaria u otro resultado definido que se utiliza para comparar alternativas."},
        {"term": "utilidad", "definition": "Valor numérico de preferencia asociado a un estado de salud dentro del método de valoración utilizado."},
        {"term": "QALY", "definition": "Año de vida ajustado por calidad; combina tiempo y utilidad relacionada con salud como unidad de resultado en análisis de coste-utilidad."},
        {"term": "coste-utilidad", "definition": "Forma de evaluación económica en la que los efectos sanitarios se expresan habitualmente en QALYs y se comparan con costes."},
        {"term": "coste incremental", "definition": "Diferencia de costes entre una alternativa y su comparador, manteniendo una dirección de comparación explícita."},
        {"term": "efecto incremental", "definition": "Diferencia de efectos entre una alternativa y su comparador."},
        {"term": "ICER", "definition": "Razón coste-efectividad incremental: coste adicional por unidad adicional de efecto cuando la comparación admite esa interpretación."},
        {"term": "dominancia", "definition": "Situación en la que una alternativa es menos costosa y más efectiva que otra dentro del modelo y la evidencia considerados."},
        {"term": "beneficio monetario neto", "definition": "Transformación de costes y efectos mediante un valor lambda explícito para facilitar comparación bajo un marco de decisión definido."},
        {"term": "descuento", "definition": "Procedimiento que expresa costes o efectos futuros en valor presente mediante una tasa declarada."},
        {"term": "impacto presupuestario", "definition": "Cambio esperado en el gasto de un responsable de presupuesto al introducir una tecnología en una población y horizonte concretos."},
        {"term": "asequibilidad", "definition": "Capacidad de absorber un impacto de gasto dentro de restricciones presupuestarias concretas; no es sinónimo de coste-efectividad."},
        {"term": "análisis de sensibilidad", "definition": "Exploración de cómo cambian resultados económicos al variar parámetros, supuestos, fuentes o estructura del modelo."},
        {"term": "análisis determinista", "definition": "Sensibilidad en la que uno o varios parámetros toman valores definidos para examinar su influencia sobre el resultado."},
        {"term": "análisis probabilístico", "definition": "Propagación conjunta de incertidumbre asignando distribuciones justificadas a parámetros inciertos."},
        {"term": "análisis de umbral", "definition": "Búsqueda del valor de un parámetro en el que cambia una conclusión o clasificación del modelo."},
        {"term": "incertidumbre estructural", "definition": "Incertidumbre asociada a cómo se representa el problema, sus estados, relaciones, extrapolaciones o mecanismos en el modelo."},
        {"term": "CHEERS 2022", "definition": "Guía de reporte para evaluaciones económicas sanitarias destinada a mejorar transparencia e interpretabilidad; no es una certificación de calidad."}
    ]
    unit["worked_examples"] = [
        {
            "title": "ICER incremental con unidades explícitas",
            "scenario": "En un caso sintético, A cuesta 1 000 unidades monetarias y produce 0,80 QALY; B cuesta 800 y produce 0,75 QALY.",
            "reasoning_steps": ["Fijar A respecto de B.", "Calcular ΔC=1000−800=200.", "Calcular ΔE=0,80−0,75=0,05 QALY.", "Verificar que A es más costosa y más efectiva, sin dominancia estricta.", "Calcular ICER=200/0,05=4 000 unidades monetarias por QALY.", "Evitar decidir sin un marco explícito para interpretar ese ICER."],
            "answer": "ICER sintético: 4 000 unidades monetarias por QALY adicional de A respecto de B.",
            "interpretation": "El número describe una relación incremental dentro del escenario; no demuestra por sí solo coste-efectividad aceptable, reembolso ni superioridad clínica."
        },
        {
            "title": "Detectar dominancia antes del cociente",
            "scenario": "A cuesta 900 y produce 0,82 QALY; B cuesta 1 000 y produce 0,80 QALY.",
            "reasoning_steps": ["Comparar costes: A cuesta 100 menos.", "Comparar efectos: A produce 0,02 QALY más.", "Reconocer que A es menos costosa y más efectiva.", "Clasificar B como dominada en este modelo.", "No presentar un ICER negativo ambiguo como conclusión principal."],
            "answer": "A domina estrictamente a B en los valores sintéticos proporcionados.",
            "interpretation": "La dominancia depende de estimaciones y supuestos; incertidumbre en costes o efectos puede modificar la clasificación."
        },
        {
            "title": "Beneficio monetario neto bajo un lambda hipotético",
            "scenario": "Una alternativa tiene ΔC=500 y ΔE=0,04 QALY. Para enseñanza se fija λ=20 000 unidades monetarias/QALY.",
            "reasoning_steps": ["Declarar que lambda es hipotético y no universal.", "Calcular λΔE=20 000×0,04=800.", "Restar ΔC: INMB=800−500=300.", "Interpretar signo positivo solo bajo ese lambda.", "Repetir con otros valores de lambda para ver el punto de cambio."],
            "answer": "INMB=+300 unidades monetarias bajo λ=20 000 por QALY.",
            "interpretation": "El resultado favorece A económicamente bajo ese valor y el modelo; no constituye una recomendación institucional."
        },
        {
            "title": "Coste-efectividad no equivale a impacto presupuestario",
            "scenario": "Una tecnología sintética tiene un resultado económico favorable, 100 personas elegibles y adopción del 20 %. Su coste incremental anual por persona es 1 500.",
            "reasoning_steps": ["Calcular tratados: 100×0,20=20.", "Calcular impacto incremental simplificado: 20×1 500=30 000 al año.", "Identificar que este cálculo requiere además costes de implementación si existen.", "Separar valor relativo de capacidad de pago del presupuesto.", "Explorar adopción del 10 % y 40 % como escenarios."],
            "answer": "Impacto presupuestario simplificado del primer escenario: +30 000 unidades monetarias/año.",
            "interpretation": "Un análisis de coste-efectividad favorable puede coexistir con un impacto agregado difícil de financiar."
        },
        {
            "title": "Sensibilidad económica, no sensibilidad diagnóstica",
            "scenario": "El caso base tiene ΔC=400 y ΔE=0,05 QALY, pero el efecto incremental plausible varía entre 0,02 y 0,08 QALY.",
            "reasoning_steps": ["Calcular ICER base: 8 000 por QALY.", "Mantener ΔC y usar ΔE=0,02: ICER=20 000.", "Usar ΔE=0,08: ICER=5 000.", "Concluir que el efecto es un impulsor importante.", "Explicar que este ejercicio varía un parámetro económico y no calcula verdaderos positivos ni sensibilidad de una prueba."],
            "answer": "El ICER varía de 5 000 a 20 000 por QALY en el rango explorado.",
            "interpretation": "El rango muestra sensibilidad determinista al efecto incremental; no representa por sí solo la incertidumbre conjunta del modelo."
        }
    ]
    unit["guided_activities"] = [
        {
            "title": "Actividad guiada: evaluación económica reproducible de dos alternativas sanitarias sintéticas",
            "duration_minutes": 300,
            "instructions": [
                "Usa exclusivamente el conjunto sintético de la actividad; no incorpores datos identificables de pacientes ni costes confidenciales de instituciones reales.",
                "Define el problema de decisión con población/contexto, alternativa A, comparador B y resultado que se desea informar.",
                "Fija perspectiva y horizonte temporal y justifica qué categorías de costes y consecuencias entran o quedan fuera.",
                "Construye una tabla de costes y efectos por alternativa con unidad, periodo, fuente sintética y supuesto.",
                "Calcula costes y efectos incrementales con una dirección de comparación constante.",
                "Comprueba dominancia antes de calcular e interpretar un ICER.",
                "Calcula ICER e INMB con al menos tres valores hipotéticos de lambda, etiquetándolos como escenarios y no como umbrales universales.",
                "Aplica descuento a una corriente sintética multianual y documenta la tasa utilizada únicamente como supuesto docente.",
                "Construye un análisis de impacto presupuestario con población elegible, adopción por periodo, costes de implementación y escenario actual.",
                "Ejecuta sensibilidad determinista, un escenario estructural o metodológico y un análisis de umbral sobre un parámetro influyente.",
                "Diseña conceptualmente un análisis probabilístico indicando qué parámetros tendrían distribuciones y por qué; no inventes distribuciones sin evidencia.",
                "Redacta un memorando final que separe resultado económico, asequibilidad, incertidumbre y decisiones de reembolso/compra que permanecen fuera del ejercicio."
            ],
            "problems": [
                "Redactar el problema de decisión en una frase verificable.",
                "Identificar el comparador relevante y justificar por qué no debe omitirse.",
                "Elegir una perspectiva y listar cuatro costes incluidos.",
                "Listar dos costes excluidos y justificar la exclusión.",
                "Definir un horizonte temporal y un riesgo de usar uno demasiado corto.",
                "Calcular QALYs sintéticos para dos estados y periodos.",
                "Calcular el valor presente de un coste futuro con una tasa docente declarada.",
                "Calcular ΔC para A respecto de B.",
                "Calcular ΔE para A respecto de B.",
                "Determinar si existe dominancia.",
                "Calcular el ICER si procede y escribir sus unidades.",
                "Explicar por qué un ICER negativo puede ser ambiguo sin revisar cuadrantes y dominancia.",
                "Calcular INMB para tres lambdas hipotéticos.",
                "Identificar el valor de lambda en que el INMB cambia de signo si existe.",
                "Construir la población elegible de un BIA sintético.",
                "Aplicar tres escenarios de adopción.",
                "Añadir costes de instalación, formación o mantenimiento cuando correspondan.",
                "Calcular impacto presupuestario anual frente al escenario actual.",
                "Explicar por qué buen ICER y bajo impacto presupuestario son afirmaciones diferentes.",
                "Seleccionar cinco parámetros para sensibilidad determinista y justificar rangos.",
                "Construir un escenario alternativo de horizonte o fuente de datos.",
                "Realizar un análisis de umbral de un parámetro dominante.",
                "Clasificar incertidumbre en parámetro, estructura, metodología y heterogeneidad.",
                "Describir qué distribuciones requeriría un PSA sin asignarlas arbitrariamente.",
                "Detectar una frase que confunda sensibilidad económica con sensibilidad diagnóstica y corregirla.",
                "Auditar el informe con una selección de elementos CHEERS 2022.",
                "Escribir una conclusión que no afirme reembolso, compra o uso clínico automático.",
                "Enumerar tres piezas de evidencia que reducirían incertidumbre antes de una evaluación real."
            ],
            "deliverables": [
                "Ficha del problema de decisión, comparadores, perspectiva y horizonte.",
                "Tabla trazable de costes, efectos, unidades, fuentes y supuestos.",
                "Hoja de cálculo incremental con ΔC, ΔE, dominancia e ICER cuando proceda.",
                "Tabla de INMB para tres valores hipotéticos de lambda.",
                "Cálculo de descuento documentado.",
                "Modelo simplificado de impacto presupuestario con tres escenarios de adopción.",
                "Tabla de sensibilidad determinista y análisis de umbral.",
                "Mapa de incertidumbre paramétrica, estructural, metodológica y heterogeneidad.",
                "Especificación conceptual del PSA y variables que requerirían distribuciones.",
                "Memorando final con resultados, asequibilidad, incertidumbre, límites y evidencia pendiente."
            ],
            "checking_criteria": [
                "Problema de decisión y comparadores están definidos antes del cálculo.",
                "Perspectiva y horizonte son explícitos y coherentes con costes y consecuencias incluidos.",
                "Las unidades de costes, efectos e ICER son visibles.",
                "La dirección A−B se conserva en ΔC y ΔE.",
                "Se comprueba dominancia antes de interpretar el ICER.",
                "Los valores de lambda se identifican como hipótesis o reglas contextuales, nunca universales.",
                "El descuento usa una tasa documentada y no una constante implícita.",
                "Impacto presupuestario se informa por separado de coste-efectividad.",
                "El BIA incluye población, adopción y costes de implementación pertinentes.",
                "La sensibilidad varía parámetros o supuestos económicos y no se define como métrica diagnóstica.",
                "Los rangos de sensibilidad tienen justificación.",
                "El PSA conceptual no asigna distribuciones arbitrarias.",
                "La incertidumbre estructural y metodológica permanece visible.",
                "CHEERS se usa como apoyo de transparencia y no como certificación de validez.",
                "No se usan datos personales o confidenciales.",
                "La conclusión no convierte un resultado económico sintético en decisión clínica, de reembolso o compra."
            ]
        }
    ]
    unit["common_errors"] = [
        {"error": "Definir sensibilidad como proporción de verdaderos positivos.", "correction": "En U5, análisis de sensibilidad explora cambios del resultado económico ante parámetros, supuestos, fuentes o estructura; la sensibilidad diagnóstica es otro concepto."},
        {"error": "Calcular coste total/efecto total en lugar de análisis incremental.", "correction": "Comparar diferencias ΔC y ΔE respecto de un comparador explícito."},
        {"error": "Interpretar cualquier ICER negativo como favorable.", "correction": "Revisar signos de ΔC y ΔE y cuadrante; identificar dominancia antes de usar el cociente."},
        {"error": "Omitir el comparador relevante.", "correction": "Definir el problema de decisión y justificar todos los comparadores pertinentes."},
        {"error": "Usar un umbral de coste-efectividad como constante universal.", "correction": "Documentar el valor y su contexto o usar lambdas sintéticos solo para análisis docente."},
        {"error": "Confundir precio con coste.", "correction": "Valorar los recursos pertinentes según perspectiva, método y periodo; el precio puede ser solo un componente."},
        {"error": "Elegir un horizonte demasiado corto para favorecer una alternativa.", "correction": "Usar un horizonte capaz de capturar diferencias importantes y explorar extrapolación en sensibilidad."},
        {"error": "Aplicar una tasa de descuento sin citar marco o supuesto.", "correction": "Declarar tasa, periodo, qué magnitudes se descuentan y sensibilidad cuando corresponda."},
        {"error": "Concluir que coste-efectivo significa asequible.", "correction": "Realizar y reportar impacto presupuestario por separado."},
        {"error": "Modelar adopción del BIA como una certeza.", "correction": "Usar escenarios plausibles y documentar población, mezcla tecnológica y tasa de adopción."},
        {"error": "Hacer sensibilidad solo con un escenario optimista.", "correction": "Explorar rangos plausibles y escenarios que puedan fortalecer o debilitar la conclusión."},
        {"error": "Elegir distribuciones del PSA por conveniencia.", "correction": "Relacionar cada distribución con evidencia, dominio del parámetro y justificación metodológica."},
        {"error": "Tratar CHEERS como validación del modelo.", "correction": "Usarlo como guía de reporte; evaluar además estructura, datos, verificación, validación e incertidumbre."},
        {"error": "Convertir un resultado económico en recomendación automática de reembolso o compra.", "correction": "Comunicar el alcance del análisis y reconocer criterios institucionales, clínicos, éticos y de evidencia adicionales."}
    ]
    unit["self_assessment"] = [
        {"question": "¿Qué hace económica a una evaluación sanitaria?", "answer": "Compara alternativas considerando conjuntamente costes y consecuencias para una decisión delimitada.", "reasoning": "Un estudio de costes sin consecuencias o de efectos sin costes responde una pregunta distinta.", "common_error": "Llamar coste-efectividad a cualquier cálculo monetario."},
        {"question": "¿Qué define la perspectiva?", "answer": "Qué costes y consecuencias son pertinentes desde el punto de vista elegido.", "reasoning": "Cambiar perspectiva puede cambiar las categorías incluidas y el resultado.", "common_error": "Usar todos los costes disponibles sin declarar para quién importan."},
        {"question": "¿Por qué importa el horizonte temporal?", "answer": "Porque debe capturar diferencias relevantes de costes y resultados entre alternativas.", "reasoning": "Un horizonte corto puede omitir beneficios o costes futuros.", "common_error": "Elegir el periodo por conveniencia del resultado."},
        {"question": "¿Cómo se calcula el ICER?", "answer": "ICER=ΔC/ΔE, con ΔC y ΔE definidos en la misma dirección de comparación.", "reasoning": "Es una relación incremental, no un cociente de totales.", "common_error": "Mezclar A−B en costes y B−A en efectos."},
        {"question": "¿Qué debe revisarse antes de interpretar un ICER?", "answer": "Dominancia, signos, unidades, magnitud de ΔE y validez de la comparación.", "reasoning": "Un cociente puede ocultar que una alternativa es dominada o dominante.", "common_error": "Interpretar el signo del ICER sin revisar cuadrantes."},
        {"question": "¿Qué significa INMB positivo?", "answer": "Que la alternativa es favorecida económicamente bajo el lambda, datos y supuestos especificados.", "reasoning": "El resultado depende del valor asignado a la unidad de efecto.", "common_error": "Tratar lambda como universal."},
        {"question": "¿Coste-efectivo significa asequible?", "answer": "No. Coste-efectividad evalúa valor relativo; impacto presupuestario examina gasto agregado para un decisor concreto.", "reasoning": "Una alternativa puede ofrecer valor a largo plazo y aun así requerir un gasto inmediato elevado.", "common_error": "Usar ICER para responder directamente cuánto dinero necesita un presupuesto anual."},
        {"question": "¿Qué entradas mínimas necesita un BIA?", "answer": "Perspectiva del presupuesto, población elegible, mezcla actual y futura, adopción, uso de recursos, costes y horizonte.", "reasoning": "El impacto depende de quién paga y de cuántas personas cambian de alternativa.", "common_error": "Multiplicar precio por población total sin modelar elegibilidad ni adopción."},
        {"question": "¿Qué significa sensibilidad en U5?", "answer": "Explorar cómo cambian los resultados económicos al variar parámetros, supuestos, fuentes o estructura.", "reasoning": "Es un concepto de incertidumbre del modelo económico.", "common_error": "Definirla como verdaderos positivos de una prueba diagnóstica."},
        {"question": "¿Qué aporta un análisis determinista de una vía?", "answer": "Identifica cómo cambia el resultado cuando se modifica un parámetro dentro de un rango justificado.", "reasoning": "Es útil para localizar impulsores, pero no representa toda la incertidumbre conjunta.", "common_error": "Presentarlo como sustituto completo del PSA."},
        {"question": "¿Qué diferencia incertidumbre paramétrica de estructural?", "answer": "La paramétrica afecta valores de entradas; la estructural afecta cómo se representa el problema y sus relaciones.", "reasoning": "Cambiar una distribución no resuelve una estructura incorrecta.", "common_error": "Llamar paramétrica a cualquier incertidumbre del modelo."},
        {"question": "¿Qué garantiza CHEERS 2022?", "answer": "Ofrece estándares de reporte para mejorar transparencia e interpretabilidad; no garantiza que el modelo sea válido ni que la decisión sea correcta.", "reasoning": "La calidad de reporte y la validez metodológica son relacionadas pero diferentes.", "common_error": "Usar cumplimiento de checklist como sello de aprobación."},
        {"question": "¿Puede U5 recomendar reembolso real?", "answer": "No a partir del ejercicio sintético. Una decisión real requiere evidencia, proceso institucional y criterios del contexto correspondiente.", "reasoning": "La unidad enseña método y límites, no sustituye una HTA o deliberación real.", "common_error": "Convertir un resultado favorable del caso docente en recomendación externa."}
    ]
    unit["biomedical_connections"] = [
        {"connection": "Evaluación de tecnologías sanitarias", "explanation": "La evaluación económica aporta evidencia sobre costes y consecuencias dentro de HTA, pero no sustituye evaluación clínica, ética, organizativa o deliberación."},
        {"connection": "Tecnologías médicas y dispositivos", "explanation": "Permite modelar costes de adquisición, instalación, mantenimiento, formación y cambios de flujo junto con resultados sanitarios."},
        {"connection": "Gestión hospitalaria y pagadores", "explanation": "Separa valor relativo de impacto presupuestario y hace visible la población y adopción que determinan asequibilidad."},
        {"connection": "Investigación clínica y resultados", "explanation": "Las estimaciones económicas dependen de evidencia de efectos y calidad de vida, por lo que su incertidumbre debe propagarse al resultado económico."}
    ]
    unit["sources"] = [
        {"title": "Consolidated Health Economic Evaluation Reporting Standards 2022 (CHEERS 2022)", "authors": "Husereau et al.", "year": 2022, "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8755935/", "type": "guía de reporte revisada por pares", "verification_status": "verified_directly"},
        {"title": "Economic evaluation — NICE technology appraisal and highly specialised technologies guidance: the manual", "authors": "National Institute for Health and Care Excellence", "year": 2022, "url": "https://www.nice.org.uk/process/pmg36/chapter/economic-evaluation-2/", "type": "manual metodológico institucional", "verification_status": "verified_directly"},
        {"title": "Budget impact analysis—principles of good practice: ISPOR 2012 Budget Impact Analysis Good Practice II Task Force", "authors": "Sullivan et al.", "year": 2014, "url": "https://pubmed.ncbi.nlm.nih.gov/24438712/", "type": "recomendación metodológica revisada por pares", "verification_status": "verified_directly"},
        {"title": "Recommendations for Conduct, Methodological Practices, and Reporting of Cost-effectiveness Analyses: Second Panel", "authors": "Sanders et al.", "year": 2016, "url": "https://pubmed.ncbi.nlm.nih.gov/27623463/", "type": "recomendación metodológica revisada por pares", "verification_status": "verified_directly"},
        {"title": "Model parameter estimation and uncertainty: ISPOR-SMDM Modeling Good Research Practices Task Force 6", "authors": "Briggs et al.", "year": 2012, "url": "https://pubmed.ncbi.nlm.nih.gov/22999133/", "type": "recomendación metodológica revisada por pares", "verification_status": "verified_directly"},
        {"title": "Model transparency and validation: ISPOR-SMDM Modeling Good Research Practices Task Force 7", "authors": "Eddy et al.", "year": 2012, "url": "https://pubmed.ncbi.nlm.nih.gov/22999134/", "type": "recomendación metodológica revisada por pares", "verification_status": "verified_directly"},
        {"title": "Modeling good research practices—overview: ISPOR-SMDM Modeling Good Research Practices Task Force 1", "authors": "Caro et al.", "year": 2012, "url": "https://pubmed.ncbi.nlm.nih.gov/22999128/", "type": "recomendación metodológica revisada por pares", "verification_status": "verified_directly"},
        {"title": "Health technology assessment of medical devices, 2nd ed", "authors": "World Health Organization", "year": 2025, "url": "https://www.who.int/publications/i/item/9789240110878", "type": "publicación institucional", "verification_status": "verified_directly"}
    ]
    unit["editorial_notice"] = (
        "Unidad académica en revisión. La curación interna y sus comprobaciones automáticas no constituyen revisión disciplinar externa, "
        "evaluación económica oficial, HTA, recomendación de reembolso, asesoría de compra ni decisión clínica. Todos los costes, QALYs, "
        "tasas, umbrales, poblaciones y escenarios numéricos de las actividades son sintéticos salvo que una fuente se cite explícitamente."
    )
    unit["status"] = "review"

    serialized = json.dumps(unit, ensure_ascii=False).casefold()
    assert GENERIC.casefold() not in serialized
    assert "proporción de casos positivos" not in serialized
    assert len(unit["glossary"]) >= 20
    assert len(unit["worked_examples"]) >= 5
    assert len(unit["common_errors"]) >= 12
    assert len(unit["self_assessment"]) >= 12
    assert all(s.get("verification_status") == "verified_directly" for s in unit["sources"])
    dump(unit)
    print("[ok] Economía y Gestión de Empresas U5 curada y espejo sincronizado")


if __name__ == "__main__":
    main()
