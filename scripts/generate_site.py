#!/usr/bin/env python3
"""Generador estático para páginas de asignatura de CitoNauta.

El script lee data/citonauta_curriculum.json y usa templates/asignatura.html
para generar páginas HTML de asignaturas. Por defecto funciona en modo seguro:
no sobrescribe archivos existentes salvo que se use --force.

También puede enriquecer asignaturas con archivos opcionales en:

data/subjects/<area_id>/<subject_id>.json
"""

from __future__ import annotations

import argparse
import html
import json
import os
from functools import cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "citonauta_curriculum.json"
OUTLINES_PATH = ROOT / "data" / "course_outlines.json"
TEMPLATE_PATH = ROOT / "templates" / "asignatura.html"
AREA_TEMPLATE_PATH = ROOT / "templates" / "area.html"
UNIT_TEMPLATE_PATH = ROOT / "templates" / "unidad.html"
UNITS_TEMPLATE_PATH = ROOT / "templates" / "unidades.html"
SUBJECT_DATA_DIR = ROOT / "data" / "subjects"
REQUIRED_TEMPLATE_KEYS = {
    "subject_title",
    "area_title",
    "subject_description",
    "css_path",
    "editorial_css_path",
    "home_path",
    "area_path",
    "previous_link",
    "next_link",
    "biomedical_connection",
    "level",
    "estimated_workload",
    "status",
    "status_label",
    "prerequisites",
    "course_competencies",
    "learning_objectives",
    "learning_outcomes",
    "modules",
    "detailed_units",
    "practical_activities",
    "assessment",
    "key_concepts",
    "related_subjects",
    "suggested_resources",
}

STATUS_LABELS = {
    "placeholder": "Contenido pendiente",
    "draft": "Borrador inicial",
    "review": "Programa curricular estructurado · revisión pendiente",
    "generated": "Unidades desarrolladas · revisión experta pendiente",
    "complete": "Contenido revisado por especialista",
}

REQUIRED_UNIT_TEMPLATE_KEYS = {
    "unit_number", "unit_count", "unit_title", "unit_description",
    "subject_title", "area_title", "css_path", "editorial_css_path",
    "home_path", "area_path", "subject_path", "units_index_path",
    "previous_unit_link", "next_unit_link", "learning_outcomes", "topics",
    "theory_sections", "worked_case", "guided_activity", "self_assessment",
    "glossary", "resources", "synthesis",
}

REQUIRED_UNITS_TEMPLATE_KEYS = {
    "subject_title", "subject_description", "area_title", "unit_count",
    "css_path", "editorial_css_path", "home_path", "area_path",
    "subject_path", "unit_cards",
}

STATISTICS_SUBJECTS = {
    "probabilidad-estadistica", "bioestadistica", "analisis-estadistico-multivariado",
    "ingenieria-datos-biomedicos", "sistemas-ayuda-decision-medica",
}
COMPUTING_SUBJECTS = {
    "fundamentos-programacion", "algoritmos-estructuras-datos", "arquitectura-computadores",
    "bases-datos", "redes-comunicaciones", "redes-servicios", "bioinformatica",
    "nlp-recuperacion-informacion",
}
BIOLOGY_SUBJECTS = {
    "biologia-i", "biologia-ii", "biologia-celular-tisular", "biologia-molecular",
    "biologia-molecular-celular-aplicada", "genetica", "biologia-desarrollo",
    "biologia-sintetica", "bioquimica", "nanobiotecnologia",
}
PHYSIOLOGY_SUBJECTS = {
    "histoanatomia-humana", "fisiologia-humana-i", "fisiologia-humana-ii",
    "fisiologia-sistemas", "fisiopatologia-humana", "ingenieria-neurosensorial",
}
SIGNAL_IMAGING_SUBJECTS = {
    "sistemas-senales", "teoria-senal-biocomputacion", "senales-biomedicas",
    "laboratorio-senales-biomedicas", "imagenes-biomedicas",
    "imagenes-biomedicas-avanzadas-i", "imagenes-biomedicas-avanzadas-ii",
    "tratamiento-digital-imagenes", "laboratorio-imagenes-biomedicas", "biofotonica",
}
MATERIALS_SUBJECTS = {
    "quimica-i", "quimica-ii", "quimica-medicinal", "biomateriales",
    "biomateriales-implantes", "polimeros-procesamiento-materiales",
    "ingenieria-tejidos", "biosensores",
}
DEVICE_SUBJECTS = {
    "sistemas-electronicos", "electronica", "electrofisica-electromecanica",
    "bioinstrumentacion", "laboratorio-bioinstrumentacion", "desarrollo-dispositivos-medicos",
    "ingenieria-clinica-gestion", "analisis-instrumental", "interfaces-hombre-maquina",
}
DIGITAL_HEALTH_SUBJECTS = {
    "informatica-biomedica", "historias-clinicas-terminologias-estandares",
    "aplicaciones-salud-digital", "ingenieria-datos-biomedicos",
    "sistemas-ayuda-decision-medica", "interfaces-hombre-maquina",
}

PEDAGOGICAL_FRAMES = {
    "quantitative": {
        "name": "razonamiento cuantitativo",
        "central_question": "qué magnitudes intervienen, cómo se relacionan y bajo qué supuestos",
        "sequence": ["definir variables y unidades", "elegir una representación", "derivar o ejecutar el método", "comprobar el resultado", "interpretar su alcance"],
        "evidence": "coherencia dimensional, derivación, cálculo reproducible y contraste con casos límite",
        "caution": "un resultado numérico puede ser correcto y, aun así, responder a un modelo inadecuado",
        "product": "modelo, cálculo o simulación comentada",
    },
    "statistics": {
        "name": "inferencia basada en datos",
        "central_question": "qué población, variable, comparación y estimando representan los datos",
        "sequence": ["formular la pregunta", "identificar el proceso de generación de datos", "explorar calidad y distribución", "estimar con incertidumbre", "evaluar sensibilidad y sesgo"],
        "evidence": "diseño del estudio, calidad de datos, tamaño de efecto, incertidumbre y análisis de sensibilidad",
        "caution": "asociación, predicción y causalidad son afirmaciones diferentes",
        "product": "informe reproducible con datos, código, estimaciones y limitaciones",
    },
    "computing": {
        "name": "diseño computacional",
        "central_question": "qué entradas, transformaciones, salidas e invariantes definen el problema",
        "sequence": ["especificar entradas y salidas", "representar los datos", "diseñar el procedimiento", "probar casos normales y límite", "medir corrección, coste y reproducibilidad"],
        "evidence": "código legible, pruebas, trazas de ejecución, control de versiones y evaluación con datos separados",
        "caution": "que un programa ejecute sin errores no demuestra que su resultado sea válido",
        "product": "prototipo documentado con pruebas y registro de versiones",
    },
    "biology": {
        "name": "razonamiento mecanístico",
        "central_question": "qué estructura, proceso, regulación y contexto producen el fenómeno observado",
        "sequence": ["delimitar la escala biológica", "describir componentes", "proponer relaciones mecanísticas", "identificar evidencia experimental", "conectar mecanismo, fenotipo y contexto"],
        "evidence": "controles, perturbaciones, mediciones complementarias y convergencia entre métodos",
        "caution": "una imagen, correlación o marcador aislado no demuestra por sí solo un mecanismo",
        "product": "modelo causal anotado con evidencias, incertidumbres y predicciones comprobables",
    },
    "physiology": {
        "name": "integración fisiológica",
        "central_question": "qué variable se regula, qué órganos participan y cómo actúa la retroalimentación",
        "sequence": ["definir la variable y su rango", "identificar sensores, integradores y efectores", "seguir flujos y retroalimentación", "comparar reposo, demanda y alteración", "relacionar medición con función"],
        "evidence": "mediciones temporales, relaciones dosis-respuesta, perturbaciones controladas y coherencia entre escalas",
        "caution": "un valor fuera de rango requiere contexto, método de medición y evaluación profesional",
        "product": "diagrama funcional con variables, flujos, controles y puntos de medición",
    },
    "signals": {
        "name": "cadena de señal e imagen",
        "central_question": "cómo se adquiere, representa, transforma y valida la información biomédica",
        "sequence": ["caracterizar la fuente y el sensor", "revisar muestreo, resolución y ruido", "preprocesar sin ocultar artefactos", "extraer una representación útil", "validar contra una referencia pertinente"],
        "evidence": "datos de calibración, métricas explícitas, conjuntos independientes y análisis de artefactos",
        "caution": "filtrar o mejorar una señal puede eliminar información o introducir patrones artificiales",
        "product": "pipeline trazable con señal original, transformaciones, métricas y comparación final",
    },
    "materials": {
        "name": "relación proceso–estructura–propiedad",
        "central_question": "cómo composición y procesamiento determinan propiedades y respuesta biológica",
        "sequence": ["definir composición y estructura", "describir el procesamiento", "medir propiedades relevantes", "analizar interacción con el entorno biológico", "comparar desempeño, degradación y riesgo"],
        "evidence": "caracterización fisicoquímica, ensayos controlados, controles, trazabilidad de lote y evaluación biológica escalonada",
        "caution": "una propiedad favorable en laboratorio no garantiza seguridad ni desempeño clínico",
        "product": "matriz de trazabilidad entre material, proceso, propiedad, prueba y riesgo",
    },
    "devices": {
        "name": "ingeniería orientada a necesidades y riesgo",
        "central_question": "qué necesidad, requisito, peligro y evidencia determinan un diseño aceptable",
        "sequence": ["definir usuario, uso y entorno", "traducir necesidades en requisitos medibles", "diseñar y analizar riesgos", "verificar requisitos", "validar el uso previsto"],
        "evidence": "trazabilidad, calibración, pruebas de banco, análisis de riesgo y validación con usuarios representativos",
        "caution": "verificación técnica y validación del uso son procesos relacionados, pero no equivalentes",
        "product": "expediente de diseño resumido con requisitos, riesgos, pruebas y criterios de aceptación",
    },
    "digital_health": {
        "name": "sistemas de información en salud",
        "central_question": "cómo fluyen los datos y cómo afectan seguridad, interoperabilidad y decisiones",
        "sequence": ["mapear actores y flujo de trabajo", "definir datos y significado", "aplicar estándares e interoperabilidad", "evaluar calidad, privacidad y seguridad", "medir utilidad y efectos no deseados"],
        "evidence": "procedencia de datos, pruebas de interoperabilidad, evaluación externa, auditoría y desempeño por subgrupos",
        "caution": "la precisión técnica no garantiza utilidad clínica, equidad ni integración segura en el trabajo real",
        "product": "mapa de flujo con estándares, controles, riesgos y métricas de utilidad",
    },
    "management": {
        "name": "análisis sociotécnico y ético",
        "central_question": "qué actores, evidencias, valores, incentivos y consecuencias intervienen en la decisión",
        "sequence": ["definir el problema público u organizacional", "mapear actores y derechos", "comparar evidencia y alternativas", "anticipar impactos y compensaciones", "establecer responsabilidad y seguimiento"],
        "evidence": "fuentes trazables, argumentos explícitos, indicadores, participación de afectados y revisión de consecuencias",
        "caution": "una solución técnicamente posible puede ser injusta, inviable o socialmente indeseable",
        "product": "informe de decisión con alternativas, criterios, impactos y plan de seguimiento",
    },
}

# Definiciones originales y breves para los conceptos que aparecen con mayor
# frecuencia en los temarios. Se buscan por subcadena, de la expresión más
# específica a la más general; el texto restante usa una definición operacional.
CONCEPT_DEFINITIONS = {
    "ecuaciones e inecuaciones": "Relaciones algebraicas que imponen, respectivamente, igualdades o desigualdades y definen valores o regiones que satisfacen esas condiciones.",
    "heredabilidad y riesgo poligénico": "La heredabilidad cuantifica variación poblacional asociada a diferencias genéticas; un puntaje de riesgo poligénico combina efectos estimados de múltiples variantes para estratificar propensión, no destino individual.",
    "explicabilidad y responsabilidad": "La explicabilidad permite comprender razones, límites y comportamiento de un sistema; la responsabilidad asigna deberes de diseño, decisión, supervisión y reparación a actores identificables.",
    "equilibrio de hardy-weinberg": "Modelo nulo de genética de poblaciones que relaciona frecuencias alélicas y genotípicas bajo supuestos explícitos de apareamiento, tamaño poblacional y ausencia de fuerzas evolutivas.",
    "intervalos de confianza": "Rangos calculados mediante un procedimiento que, bajo repeticiones hipotéticas y supuestos definidos, contiene el parámetro verdadero con una frecuencia determinada.",
    "pruebas de hipótesis": "Procedimientos que comparan la compatibilidad de los datos con una hipótesis nula y controlan una tasa de error previamente especificada.",
    "potencial de membrana": "Diferencia de potencial eléctrico entre ambos lados de una membrana, originada por gradientes iónicos y permeabilidades selectivas.",
    "potencial de acción": "Cambio rápido y regenerativo del potencial de membrana producido por la apertura y cierre coordinados de canales iónicos dependientes de voltaje.",
    "transformada de fourier": "Representación de una señal como combinación de componentes sinusoidales, útil para estudiar cómo se distribuye su contenido en frecuencia.",
    "descomposición en valores singulares": "Factorización matricial que expresa una matriz mediante direcciones ortogonales y valores singulares, revelando rango, estructura y aproximaciones de baja dimensión.",
    "ecuaciones diferenciales": "Ecuaciones que relacionan una función desconocida con sus derivadas y permiten describir tasas de cambio en el tiempo o el espacio.",
    "valores propios": "Escalares asociados a direcciones que una transformación lineal conserva, salvo un cambio de magnitud y eventualmente de sentido.",
    "vectores propios": "Direcciones no nulas que una transformación lineal mantiene alineadas y escala mediante su valor propio correspondiente.",
    "conjuntos numéricos": "Clasificaciones de números —naturales, enteros, racionales, reales o complejos— definidas por sus propiedades y operaciones válidas.",
    "expresiones algebraicas": "Combinaciones de números, variables y operaciones que representan relaciones cuantitativas sin afirmar todavía una igualdad.",
    "sistemas de ecuaciones": "Conjuntos de igualdades que deben satisfacerse simultáneamente y cuya solución representa valores compatibles con todas las restricciones.",
    "transformaciones lineales": "Funciones entre espacios vectoriales que preservan suma y multiplicación por escalares.",
    "producto interno": "Operación que asigna un escalar a dos vectores y permite definir longitud, ángulo y ortogonalidad.",
    "métodos numéricos": "Algoritmos que aproximan soluciones matemáticas cuando una forma analítica exacta no existe o no resulta práctica.",
    "error de truncamiento": "Diferencia introducida al reemplazar un proceso matemático infinito o continuo por una aproximación finita.",
    "convergencia": "Propiedad de una sucesión o algoritmo cuyas aproximaciones se acercan a un valor límite bajo condiciones definidas.",
    "interpolación": "Estimación de valores dentro del rango cubierto por observaciones conocidas mediante una función ajustada.",
    "optimización": "Búsqueda de valores que minimizan o maximizan una función objetivo respetando restricciones.",
    "derivadas": "Medidas de la tasa de cambio local de una función respecto a una variable.",
    "integrales": "Operaciones que acumulan cantidades continuas y relacionan tasas de cambio con variaciones totales.",
    "límites": "Valores a los que se aproxima una función o sucesión cuando su argumento se acerca a un punto o crece sin cota.",
    "matrices": "Arreglos rectangulares de elementos que representan datos, sistemas lineales y transformaciones entre espacios.",
    "vectores": "Objetos ordenados con magnitud y componentes que representan estados, direcciones o colecciones de variables.",
    "ecuaciones": "Igualdades entre expresiones que imponen condiciones sobre una o más incógnitas.",
    "inecuaciones": "Desigualdades que describen conjuntos de valores permitidos en lugar de una igualdad exacta.",
    "probabilidad condicional": "Probabilidad de un evento cuando se conoce que otro evento ha ocurrido, definida respecto al nuevo espacio de información.",
    "variables aleatorias": "Funciones que asignan valores numéricos a resultados de un experimento aleatorio.",
    "distribuciones de probabilidad": "Modelos que asignan probabilidades a los valores o intervalos posibles de una variable aleatoria.",
    "tamaño de efecto": "Medida cuantitativa de la magnitud de una diferencia, asociación o relación, distinta de su significación estadística.",
    "regresión lineal": "Modelo que expresa el valor medio de una variable de respuesta como combinación lineal de predictores y un término de error.",
    "regresión logística": "Modelo que relaciona predictores con el logaritmo de las probabilidades relativas de un resultado binario.",
    "validación cruzada": "Estrategia de remuestreo que alterna subconjuntos de entrenamiento y evaluación para estimar desempeño fuera de muestra.",
    "sensibilidad": "Proporción de casos positivos de referencia que una prueba identifica correctamente.",
    "especificidad": "Proporción de casos negativos de referencia que una prueba clasifica correctamente.",
    "muestreo": "Proceso de seleccionar unidades de una población para obtener información sobre ella, idealmente con un mecanismo de selección conocido.",
    "sesgo": "Desviación sistemática entre una estimación o conclusión y el valor o relación que se pretende conocer.",
    "varianza": "Promedio teórico de las desviaciones cuadráticas respecto a la media; cuantifica dispersión en una distribución.",
    "incertidumbre": "Conocimiento incompleto sobre el valor de una medición, parámetro, modelo o conclusión, que debe expresarse y propagarse.",
    "algoritmos": "Secuencias finitas y no ambiguas de operaciones que transforman entradas en salidas para resolver una clase de problemas.",
    "estructuras de datos": "Formas de organizar información junto con las operaciones permitidas para accederla y modificarla eficientemente.",
    "complejidad computacional": "Análisis de los recursos, como tiempo y memoria, que requiere un algoritmo según el tamaño de la entrada.",
    "control de flujo": "Mecanismos que determinan el orden de ejecución de instrucciones mediante secuencias, decisiones y repeticiones.",
    "recursión": "Técnica en la que una función resuelve un problema mediante instancias menores del mismo problema y un caso base.",
    "normalización de bases": "Organización de tablas para reducir redundancia y anomalías de actualización mediante dependencias bien definidas.",
    "transacciones": "Unidades lógicas de trabajo en una base de datos que preservan propiedades de atomicidad, consistencia, aislamiento y durabilidad.",
    "bases de datos": "Sistemas organizados para almacenar, consultar y mantener información con reglas de integridad y control de acceso.",
    "protocolos": "Conjuntos de reglas que especifican formato, orden y significado de los mensajes intercambiados entre sistemas.",
    "interoperabilidad": "Capacidad de sistemas distintos para intercambiar información y utilizarla conservando estructura, significado y contexto.",
    "ontologías": "Representaciones formales de entidades, relaciones y restricciones de un dominio que permiten compartir significado computable.",
    "fhir": "Estándar de HL7 que representa e intercambia información de salud mediante recursos modulares y interfaces web.",
    "snomed": "Terminología clínica composicional que asigna identificadores a conceptos y relaciones para registrar significado de forma consistente.",
    "loinc": "Sistema de identificadores para observaciones, mediciones, documentos y preguntas clínicas o de laboratorio.",
    "aprendizaje supervisado": "Enfoque que ajusta un modelo a ejemplos con entradas y resultados conocidos para predecir nuevas observaciones.",
    "sobreajuste": "Situación en la que un modelo aprende peculiaridades del conjunto de entrenamiento y pierde desempeño en datos nuevos.",
    "señalización celular": "Procesos mediante los que una célula detecta señales, las transmite por redes moleculares y modifica su comportamiento.",
    "expresión génica": "Uso regulado de la información de un gen para producir ARN funcional y, cuando corresponde, proteína.",
    "ciclo celular": "Secuencia regulada de crecimiento, replicación del ADN, preparación y división celular.",
    "replicación del adn": "Copia semiconservativa del ADN mediante síntesis dirigida por molde y mecanismos de corrección y reparación.",
    "transcripción": "Síntesis de ARN a partir de una plantilla de ADN por una ARN polimerasa.",
    "traducción": "Síntesis de una cadena polipeptídica por el ribosoma a partir de la secuencia de codones de un ARN mensajero.",
    "apoptosis": "Programa celular regulado que desmantela la célula y facilita su eliminación con daño tisular limitado.",
    "homeostasis": "Mantenimiento dinámico de variables internas dentro de rangos funcionales mediante regulación y retroalimentación.",
    "membrana plasmática": "Bicapa lipídica con proteínas y carbohidratos que delimita la célula y regula transporte, adhesión y señalización.",
    "organelos": "Compartimentos o complejos celulares especializados que organizan procesos como síntesis, degradación y producción de energía.",
    "mutaciones": "Cambios heredables en la secuencia del material genético cuyo efecto depende de ubicación, contexto y función.",
    "heredabilidad": "Proporción de la variación fenotípica de una población atribuible a diferencias genéticas bajo un ambiente y modelo determinados.",
    "frecuencias alélicas": "Proporciones de las distintas variantes de un locus dentro del conjunto de copias génicas de una población.",
    "diferenciación celular": "Proceso por el que una célula adopta una identidad funcional estable mediante cambios coordinados de expresión y organización.",
    "metabolismo": "Red de reacciones que transforma materia y energía para sostener mantenimiento, crecimiento y respuesta celular.",
    "enzimas": "Catalizadores biológicos que aceleran reacciones al reducir la barrera energética sin consumirse netamente.",
    "tejidos": "Conjuntos organizados de células y matriz extracelular que cooperan para cumplir funciones especializadas.",
    "retroalimentación negativa": "Control en el que la respuesta se opone a la perturbación inicial y favorece la estabilidad de una variable.",
    "retroalimentación positiva": "Proceso en el que una respuesta amplifica el cambio inicial hasta que otro mecanismo lo detiene.",
    "gasto cardíaco": "Volumen de sangre bombeado por un ventrículo por unidad de tiempo, igual al producto de frecuencia y volumen sistólico.",
    "filtración glomerular": "Paso de agua y solutos pequeños desde capilares glomerulares al espacio de Bowman impulsado por presiones netas.",
    "ventilación": "Movimiento de aire entre atmósfera y alvéolos producido por gradientes de presión.",
    "contracción muscular": "Generación de fuerza por interacción regulada de filamentos y consumo de energía química.",
    "enlace covalente": "Unión química en la que átomos comparten pares de electrones.",
    "equilibrio químico": "Estado dinámico en el que las velocidades de las reacciones directa e inversa son iguales y las concentraciones macroscópicas permanecen constantes.",
    "cinética química": "Estudio de la velocidad de las reacciones, sus mecanismos y la influencia de concentración, temperatura y catalizadores.",
    "solubilidad": "Cantidad máxima de un soluto que puede disolverse en condiciones especificadas de solvente, temperatura y presión.",
    "ph": "Medida logarítmica relacionada con la actividad de iones hidrógeno en una solución.",
    "polímeros": "Macromoléculas formadas por unidades repetidas cuya arquitectura y procesamiento determinan propiedades finales.",
    "biocompatibilidad": "Capacidad de un material o dispositivo para cumplir su función con una respuesta biológica aceptable en un contexto específico.",
    "viscoelasticidad": "Comportamiento dependiente del tiempo que combina respuesta elástica recuperable y disipación viscosa.",
    "degradación": "Cambio progresivo de estructura o propiedades por procesos químicos, físicos o biológicos.",
    "corrosión": "Deterioro de un material, especialmente metálico, por reacciones electroquímicas con su entorno.",
    "leyes de newton": "Principios que relacionan movimiento, fuerza neta, masa y pares de acción y reacción en sistemas mecánicos.",
    "conservación de energía": "Principio según el cual la energía total de un sistema aislado permanece constante aunque cambie de forma.",
    "campo eléctrico": "Campo vectorial que asigna a cada punto la fuerza por unidad de carga que experimentaría una carga de prueba positiva.",
    "resistencia eléctrica": "Oposición de un elemento al paso de corriente, definida por la relación entre tensión y corriente bajo condiciones especificadas.",
    "capacitancia": "Capacidad de almacenar carga eléctrica por unidad de diferencia de potencial.",
    "inductancia": "Propiedad por la que una variación de corriente induce una tensión que se opone al cambio.",
    "convolución": "Operación que combina una entrada con la respuesta impulsional de un sistema lineal e invariante para obtener su salida.",
    "aliasing": "Distorsión por la que componentes de frecuencia diferentes resultan indistinguibles cuando el muestreo es insuficiente.",
    "muestreo": "Conversión de una señal continua en una secuencia de valores tomados en instantes o posiciones definidos.",
    "filtros": "Sistemas que atenúan, preservan o modifican componentes de una señal según una respuesta especificada.",
    "ruido": "Variación no deseada que se superpone a una medición y limita la recuperación de la información de interés.",
    "calibración": "Comparación documentada de un instrumento con referencias trazables para establecer la relación entre indicación y valor de referencia.",
    "transductor": "Elemento que convierte una magnitud o forma de energía en otra, normalmente para facilitar medición o actuación.",
    "tomografía computarizada": "Técnica que reconstruye cortes a partir de múltiples mediciones de atenuación de rayos X alrededor del objeto.",
    "resonancia magnética": "Modalidad que codifica señales de núcleos excitados en un campo magnético mediante gradientes y pulsos de radiofrecuencia.",
    "ultrasonido": "Modalidad que emite ondas acústicas de alta frecuencia y forma imágenes o mediciones a partir de ecos y cambios de propagación.",
    "segmentación": "Asignación de píxeles o vóxeles a regiones de interés según criterios anatómicos, funcionales o algorítmicos.",
    "registro de imágenes": "Estimación de una transformación que alinea imágenes adquiridas en momentos, sujetos o modalidades diferentes.",
    "resolución espacial": "Capacidad de un sistema para distinguir estructuras cercanas como entidades separadas.",
    "artefactos": "Patrones de una medición o imagen producidos por adquisición, movimiento o procesamiento y no por la estructura de interés.",
    "requisitos": "Declaraciones medibles y verificables de una necesidad, función, interfaz, desempeño o restricción de diseño.",
    "gestión de riesgos": "Proceso sistemático para identificar peligros, estimar y evaluar riesgos, aplicar controles y vigilar el riesgo residual.",
    "verificación": "Comprobación mediante evidencia objetiva de que una salida cumple los requisitos especificados.",
    "validación": "Comprobación mediante evidencia objetiva de que una solución satisface el uso previsto y las necesidades del usuario.",
    "usabilidad": "Grado en que usuarios especificados logran objetivos con efectividad, eficiencia y satisfacción en un contexto definido.",
    "mantenimiento preventivo": "Intervenciones planificadas para reducir la probabilidad de fallo y conservar desempeño y seguridad.",
    "ciclo de vida": "Conjunto de etapas desde la concepción y desarrollo hasta operación, mantenimiento y retiro de un producto o sistema.",
    "consentimiento informado": "Proceso de decisión voluntaria basado en información comprensible, capacidad, oportunidad de preguntar y ausencia de coerción.",
    "privacidad": "Facultad y conjunto de condiciones para controlar el acceso y uso de información y aspectos de la vida personal.",
    "equidad": "Criterio que considera diferencias de necesidad y barreras para evitar desigualdades injustas en oportunidades o resultados.",
    "ética": "Análisis razonado de deberes, valores, consecuencias y relaciones de poder para orientar acciones justificables.",
    "política pública": "Curso de acción, norma o decisión institucional dirigido a abordar un problema colectivo mediante instrumentos y recursos.",
    "comunicación científica": "Proceso de adaptar y transmitir métodos, resultados, incertidumbre y relevancia a audiencias con necesidades distintas.",
    "revisión por pares": "Evaluación crítica de un trabajo por personas con conocimiento pertinente antes o después de su difusión.",
    "modelo de negocio": "Descripción de cómo una organización crea, entrega y sostiene valor para usuarios y otras partes interesadas.",
    "propiedad intelectual": "Marco de derechos sobre creaciones y signos distintivos que incluye patentes, derechos de autor, marcas y secretos empresariales.",
    "evaluación de tecnologías sanitarias": "Proceso multidisciplinario que valora evidencia clínica, económica, ética y organizacional para orientar decisiones de salud.",
    "exactitud": "Cercanía entre un resultado de medición y el valor de referencia aceptado para la magnitud medida.",
    "precisión": "Grado de concordancia entre resultados obtenidos al repetir una medición bajo condiciones especificadas.",
    "trazabilidad": "Capacidad de reconstruir el origen, las transformaciones y las decisiones asociadas a un dato, requisito, medición o resultado.",
    "linealidad": "Propiedad por la que la respuesta de un sistema mantiene una relación proporcional o aditiva dentro de un intervalo definido.",
    "selectividad": "Capacidad de un método o sistema para responder al analito, señal o característica de interés frente a interferencias.",
    "robustez": "Capacidad de un método para conservar desempeño aceptable ante variaciones pequeñas y plausibles de condiciones o parámetros.",
    "reproducibilidad": "Grado en que un resultado puede obtenerse de nuevo con información suficiente sobre datos, método, software y condiciones.",
    "documentación": "Registro estructurado de requisitos, métodos, decisiones, cambios y resultados que permite revisión y continuidad del trabajo.",
    "control de calidad": "Conjunto de comprobaciones operativas destinadas a detectar desviaciones y mantener resultados dentro de criterios definidos.",
    "calidad de datos": "Adecuación de los datos para un uso previsto considerando completitud, consistencia, validez, procedencia y oportunidad.",
    "análisis de riesgo": "Identificación de peligros y estimación de la probabilidad y gravedad de sus posibles daños antes de seleccionar controles.",
    "riesgo": "Combinación de la probabilidad de que ocurra un daño y la gravedad de sus consecuencias.",
    "seguridad": "Condición en la que los riesgos conocidos se han reducido y controlado hasta un nivel aceptable para el contexto de uso.",
    "desempeño": "Grado en que un método, modelo o dispositivo cumple funciones y criterios medibles en condiciones especificadas.",
    "eficacia": "Capacidad de una intervención para producir un efecto beneficioso en condiciones controladas y para una población definida.",
    "efectividad": "Resultado de una intervención en condiciones reales de uso, con la diversidad y limitaciones del entorno habitual.",
    "evaluación": "Proceso sistemático de comparar evidencia con criterios explícitos para emitir un juicio limitado al contexto estudiado.",
    "pruebas": "Procedimientos planificados que producen evidencia sobre cumplimiento, comportamiento o error respecto a criterios definidos.",
    "ensayos": "Pruebas realizadas bajo condiciones controladas para medir una propiedad, respuesta o desempeño mediante un protocolo.",
    "modelos": "Representaciones simplificadas de un sistema que conectan variables o mecanismos y permiten explicar, predecir o explorar escenarios.",
    "modelado": "Proceso de construir, ajustar, comprobar e interpretar una representación simplificada de un sistema real.",
    "simulación": "Ejecución de un modelo para estudiar su comportamiento bajo condiciones, parámetros y escenarios definidos.",
    "parámetros": "Valores que caracterizan un modelo o sistema y determinan su comportamiento sin actuar como variables de entrada ordinarias.",
    "variables": "Propiedades que pueden tomar distintos valores y que deben definirse con escala, unidad, procedencia y función en el análisis.",
    "datos": "Representaciones registradas de observaciones o mediciones cuyo significado depende de contexto, metadatos y proceso de obtención.",
    "evidencia": "Conjunto de observaciones, mediciones o resultados documentados que permite apoyar, debilitar o revisar una afirmación.",
    "hipótesis": "Proposición provisional y comprobable que anticipa una relación o explicación susceptible de contrastarse con evidencia.",
    "inferencia": "Paso razonado desde datos y supuestos hacia una conclusión cuyo alcance debe declararse.",
    "interpretación": "Asignación de significado a un resultado mediante teoría, contexto, supuestos y comparación con explicaciones alternativas.",
    "mecanismos": "Secuencias de entidades, interacciones y cambios que explican cómo se produce un fenómeno.",
    "sistemas": "Conjuntos de componentes relacionados que intercambian materia, energía o información y producen comportamientos conjuntos.",
    "estructura": "Organización espacial o lógica de componentes que condiciona relaciones, propiedades y función.",
    "función": "Papel o resultado que cumple un componente o sistema dentro de un contexto y nivel de organización definidos.",
    "regulación": "Modificación coordinada de la actividad de un proceso para responder a señales y mantener o cambiar un estado.",
    "transporte": "Movimiento de materia, carga, energía o información entre ubicaciones mediante fuerzas y mecanismos definidos.",
    "energía": "Magnitud conservada que cuantifica la capacidad de producir cambios o realizar trabajo y que puede transferirse o transformarse.",
    "potencia": "Tasa a la que se transfiere energía o se realiza trabajo.",
    "equilibrio": "Estado en el que fuerzas, flujos o velocidades opuestas se compensan según el modelo considerado.",
    "estabilidad": "Capacidad de un sistema o resultado para permanecer cerca de un estado o recuperar su comportamiento tras perturbaciones.",
    "dinámica": "Estudio de cómo cambia un sistema en el tiempo debido a interacciones, fuerzas, flujos o reglas de evolución.",
    "flujo": "Cantidad de materia, energía, carga o información que atraviesa una frontera por unidad de tiempo.",
    "difusión": "Transporte neto originado por movimiento aleatorio y gradientes de concentración o potencial químico.",
    "fuerza": "Interacción vectorial capaz de cambiar el movimiento o deformar un cuerpo.",
    "presión": "Fuerza normal distribuida por unidad de área.",
    "elasticidad": "Capacidad de un material para deformarse bajo carga y recuperar su forma al retirarla dentro de su régimen elástico.",
    "absorción": "Transferencia de energía o materia desde un medio incidente hacia el interior de otro sistema.",
    "fluorescencia": "Emisión de luz posterior a la absorción de energía, normalmente con longitud de onda mayor que la excitación.",
    "resolución": "Capacidad de distinguir cambios o elementos próximos como resultados separados de una medición.",
    "detección": "Proceso de decidir si una señal, entidad o evento está presente respecto a un criterio y un nivel de incertidumbre.",
    "clasificación": "Asignación de observaciones a categorías mediante reglas o modelos evaluados contra referencias pertinentes.",
    "selección": "Proceso de escoger elementos o alternativas de acuerdo con criterios explícitos y consecuencias conocidas.",
    "organización": "Disposición coordinada de componentes, funciones y relaciones que permite operar como un conjunto.",
    "comunicación": "Intercambio de información mediante un código, canal y contexto compartidos, con posibilidad de ruido y retroalimentación.",
    "actores": "Personas, grupos o instituciones con intereses, capacidades, derechos o responsabilidades respecto a una decisión.",
    "gobernanza": "Conjunto de reglas, responsabilidades y mecanismos de decisión, supervisión y rendición de cuentas de un sistema.",
    "accesibilidad": "Diseño de entornos, información o tecnologías para que puedan ser utilizados por personas con capacidades y contextos diversos.",
    "coste": "Valor de los recursos consumidos o de la mejor alternativa sacrificada al elegir una acción.",
    "indicadores": "Medidas definidas para observar estado, progreso o desempeño respecto a una meta y un periodo.",
    "kpis": "Indicadores priorizados que conectan desempeño operativo con objetivos estratégicos y criterios de decisión.",
    "estándares": "Acuerdos técnicos documentados que establecen vocabulario, requisitos, interfaces o métodos comunes.",
    "roles": "Conjuntos definidos de responsabilidades, permisos y expectativas asignados a participantes de un sistema.",
    "procesos": "Secuencias de actividades con entradas, responsables, controles y salidas orientadas a un resultado.",
    "ciclo": "Secuencia de estados o etapas que regresa a una condición comparable y puede repetirse bajo reglas definidas.",
    "representación": "Forma simbólica, gráfica, física o computacional de expresar un objeto o relación conservando la información relevante para una tarea.",
    "operaciones": "Transformaciones definidas que actúan sobre objetos y producen resultados sujetos a reglas de composición y validez.",
    "base": "Conjunto independiente de elementos a partir del cual pueden representarse de forma única los elementos de un espacio.",
    "dimensión": "Número de direcciones o grados de libertad independientes necesarios para describir un espacio o sistema.",
    "gradiente": "Vector de derivadas parciales que señala la dirección de crecimiento local más rápido de una función escalar.",
    "hessiano": "Matriz de segundas derivadas parciales que describe la curvatura local de una función multivariable.",
    "jacobiano": "Matriz de derivadas parciales de una transformación vectorial, usada para aproximación local y cambios de variables.",
    "series de taylor": "Representaciones locales de funciones mediante sumas de términos construidos con derivadas alrededor de un punto.",
    "correlación": "Medida de asociación entre variables que cuantifica covariación, sin establecer por sí misma una relación causal.",
    "colinealidad": "Dependencia fuerte entre predictores que dificulta separar sus efectos y puede volver inestables las estimaciones.",
    "pca": "Transformación lineal que proyecta datos correlacionados en componentes ortogonales ordenados por varianza explicada.",
    "clustering": "Agrupamiento de observaciones por similitud sin utilizar etiquetas de clase conocidas durante el ajuste.",
    "multiplicidad": "Aumento de oportunidades de obtener resultados extremos cuando se realizan muchas comparaciones o decisiones analíticas.",
    "población": "Conjunto de unidades sobre el que se desea formular una conclusión estadística o científica.",
    "muestra": "Subconjunto observado de una población, seleccionado mediante un diseño que condiciona la generalización.",
    "distribuciones": "Descripciones de cómo se reparten los valores posibles y sus frecuencias o probabilidades.",
    "potencia estadística": "Probabilidad de detectar un efecto de magnitud especificada cuando realmente existe, bajo un diseño y umbral dados.",
    "codificación": "Representación de información mediante símbolos y reglas que permiten almacenamiento, transmisión o procesamiento.",
    "memoria": "Recurso que conserva instrucciones y datos con una capacidad, latencia, persistencia y jerarquía determinadas.",
    "concurrencia": "Ejecución coordinada de múltiples tareas cuyos intervalos se solapan y pueden compartir recursos.",
    "entidades": "Objetos distinguibles de un dominio acerca de los cuales se almacenan atributos y relaciones.",
    "claves": "Atributos o conjuntos de atributos que identifican registros o enlazan entidades en una base de datos.",
    "índices": "Estructuras auxiliares que aceleran búsquedas a cambio de espacio y coste de mantenimiento.",
    "búsqueda": "Proceso sistemático de localizar un elemento, estado o solución dentro de un espacio definido.",
    "código": "Representación ejecutable o interpretable de un procedimiento mediante un lenguaje formal.",
    "api": "Interfaz documentada que define cómo componentes de software solicitan operaciones e intercambian datos.",
    "membrana": "Barrera organizada, normalmente lipídica y proteica, que separa compartimentos y regula intercambio y señalización.",
    "células": "Unidades vivas delimitadas que integran información, metabolismo, estructura, regulación y respuesta al entorno.",
    "adn": "Polímero de nucleótidos que almacena información hereditaria en su secuencia y se organiza con proteínas en el genoma.",
    "arn": "Polímero de ribonucleótidos con funciones de mensajería, estructura, catálisis y regulación.",
    "proteínas": "Polímeros de aminoácidos que se pliegan en estructuras capaces de catalizar, transportar, señalizar y sostener células.",
    "lípidos": "Familia diversa de moléculas poco solubles en agua que forman membranas, almacenan energía y participan en señalización.",
    "carbohidratos": "Moléculas de azúcares y sus polímeros que participan en energía, estructura y reconocimiento celular.",
    "aminoácidos": "Moléculas con grupos amino y carboxilo que actúan como monómeros de proteínas y metabolitos.",
    "cromatina": "Complejo de ADN, histonas y otras proteínas que empaqueta el genoma y regula su accesibilidad.",
    "receptores": "Moléculas que reconocen señales y convierten su unión en cambios bioquímicos, eléctricos o de expresión.",
    "microtúbulos": "Polímeros polares de tubulina que organizan transporte, forma celular, cilios y segregación cromosómica.",
    "microfilamentos": "Polímeros de actina que participan en forma, contracción, adhesión, migración y división celular.",
    "matriz extracelular": "Red de macromoléculas secretadas que proporciona soporte, señales y propiedades mecánicas a los tejidos.",
    "inmunidad": "Conjunto de barreras, células y moléculas que reconocen alteraciones y coordinan defensa, tolerancia y reparación.",
    "evolución": "Cambio heredable de poblaciones a lo largo de generaciones mediante mutación, selección, deriva, flujo génico y otros procesos.",
    "selección natural": "Diferencias heredables en supervivencia o reproducción que cambian frecuencias de variantes en una población.",
    "filogenia": "Historia de relaciones evolutivas entre linajes representada y estimada mediante caracteres y modelos.",
    "respiración celular": "Conjunto de rutas que transfieren energía de nutrientes a formas utilizables, frecuentemente mediante gradientes y ATP.",
    "gametogénesis": "Proceso de formación y maduración de gametos mediante proliferación, meiosis y diferenciación.",
    "fecundación": "Unión de gametos que combina genomas e inicia el desarrollo de un nuevo organismo.",
    "morfógenos": "Señales distribuidas en gradientes que especifican respuestas celulares dependientes de concentración y contexto.",
    "células madre": "Células capaces de autorrenovarse y producir uno o más tipos celulares diferenciados.",
    "pcr": "Técnica que amplifica regiones específicas de ADN mediante ciclos de desnaturalización, alineamiento y extensión enzimática.",
    "secuenciación": "Determinación del orden de monómeros, especialmente nucleótidos, junto con medidas de calidad y contexto de referencia.",
    "edición génica": "Modificación dirigida de secuencias o regulación genómica mediante herramientas que requieren evaluar especificidad y efectos no deseados.",
    "cultivo celular": "Mantenimiento de células fuera del organismo bajo condiciones controladas que modelan solo parte de su entorno natural.",
    "sinapsis": "Unión especializada por la que una célula transmite información a otra mediante señales químicas o eléctricas.",
    "presión arterial": "Presión ejercida por la sangre sobre la pared arterial, determinada por interacción entre bombeo cardíaco y resistencia vascular.",
    "hormonas": "Señales químicas producidas por células que regulan tejidos diana mediante receptores y circuitos de retroalimentación.",
    "sensores": "Elementos que responden a una magnitud y generan una señal utilizable para medición o control.",
    "electrodos": "Conductores que permiten intercambio de carga con un medio electrónico, iónico o biológico mediante una interfaz.",
    "impedancia": "Oposición compleja al paso de corriente alterna, que combina magnitud y fase dependientes de frecuencia.",
    "corriente": "Flujo de carga eléctrica por unidad de tiempo.",
    "contraste": "Diferencia de señal entre regiones o estados que permite distinguirlos en una medición o imagen.",
    "formatos": "Convenciones que definen estructura, codificación y metadatos de un archivo o mensaje para permitir intercambio correcto.",
    "anotación": "Asignación documentada de características, funciones o significado a datos mediante evidencia y vocabularios definidos.",
    "variantes": "Diferencias de secuencia respecto a una referencia cuya interpretación depende de calidad, frecuencia, contexto y evidencia.",
    "materiales": "Sustancias con composición, estructura y propiedades que determinan su procesamiento, función y respuesta al entorno.",
    "metales": "Materiales de enlace metálico con electrones deslocalizados, generalmente conductores y capaces de deformación plástica.",
    "cerámicas": "Materiales inorgánicos no metálicos, a menudo duros y resistentes a corrosión pero frágiles bajo tracción.",
    "microestructura": "Organización de fases, granos, poros y defectos a escala microscópica que condiciona propiedades macroscópicas.",
    "adhesión": "Interacción que mantiene unidas superficies, células o componentes mediante fuerzas físicas y enlaces específicos.",
    "inflamación": "Respuesta coordinada a daño o señales de peligro que recluta mediadores y células para defensa y reparación.",
    "desgaste": "Pérdida o deformación progresiva de material por contacto, fricción y movimiento relativo.",
    "esterilización": "Proceso validado destinado a eliminar microorganismos viables hasta un nivel de aseguramiento especificado.",
    "interfaz": "Frontera de interacción entre componentes, sistemas, materiales o usuarios donde se intercambia información, energía o carga.",
    "accesibilidad": "Propiedad de un producto o entorno que permite uso por personas con diversidad funcional, tecnológica y contextual.",
    "autonomía": "Capacidad y derecho de una persona para tomar decisiones informadas y voluntarias sobre asuntos que le afectan.",
    "beneficencia": "Deber de promover beneficios razonables para las personas afectadas por una acción.",
    "justicia": "Criterio ético sobre distribución equitativa de beneficios, cargas, oportunidades y protección.",
    "conflictos de interés": "Situaciones en las que intereses secundarios pueden influir o parecer influir sobre una responsabilidad principal.",
    "citación": "Referencia explícita que atribuye una idea o resultado y permite localizar y evaluar su fuente.",
    "autoría": "Reconocimiento de contribuciones sustanciales acompañado de responsabilidad sobre la integridad del trabajo.",
    "escasez": "Condición en la que recursos limitados obligan a priorizar entre usos alternativos.",
    "oferta y demanda": "Modelo que relaciona cantidades ofrecidas y demandadas con precios y otras condiciones de un mercado.",
    "flujo de caja": "Entradas y salidas de efectivo durante un periodo, distintas del beneficio contable.",
    "propuesta de valor": "Descripción del problema atendido, el beneficio diferencial y las razones por las que un usuario adoptaría una solución.",
    "presupuesto": "Plan cuantificado de ingresos, gastos y recursos para un periodo y objetivos determinados.",
    "transparencia": "Disponibilidad comprensible de información sobre criterios, procesos, intereses, decisiones y resultados.",
}

COURSE_FAMILIES = (
    {
        "algebra", "calculo", "ampliacion-calculo", "ecuaciones-diferenciales",
        "metodos-matematicos", "metodos-numericos", "modelos-numericos-biomedicina",
        "modelado-simulacion-biomedicina",
    },
    {
        "probabilidad-estadistica", "bioestadistica", "analisis-estadistico-multivariado",
        "ingenieria-datos-biomedicos", "sistemas-ayuda-decision-medica",
    },
    {
        "fundamentos-programacion", "algoritmos-estructuras-datos", "arquitectura-computadores",
        "bases-datos", "redes-comunicaciones", "redes-servicios", "informatica-biomedica",
        "ingenieria-datos-biomedicos", "nlp-recuperacion-informacion", "bioinformatica",
    },
    {
        "fisica-i", "fisica-ii", "biofisica", "sistemas-electronicos", "electronica",
        "electrofisica-electromecanica", "biofotonica", "analisis-instrumental",
    },
    {
        "quimica-i", "quimica-ii", "quimica-medicinal", "bioquimica", "biomateriales",
        "polimeros-procesamiento-materiales", "nanobiotecnologia", "biosensores",
    },
    {
        "biologia-i", "biologia-ii", "biologia-celular-tisular", "biologia-molecular",
        "biologia-molecular-celular-aplicada", "genetica", "biologia-desarrollo",
        "biologia-sintetica", "bioquimica", "ingenieria-tejidos", "nanobiotecnologia",
    },
    {
        "fisiologia-humana-i", "fisiologia-humana-ii", "fisiologia-sistemas",
        "fisiopatologia-humana", "histoanatomia-humana", "senales-biomedicas",
        "bioinstrumentacion", "imagenes-biomedicas",
    },
    {
        "fundamentos-biomecanica", "biomecanica", "biomecanica-medios-continuos",
        "laboratorio-biomecanica", "interfaces-hombre-maquina", "ingenieria-neurosensorial",
        "simulacion-planificacion-quirurgica",
    },
    {
        "sistemas-senales", "teoria-senal-biocomputacion", "senales-biomedicas",
        "laboratorio-senales-biomedicas", "bioinstrumentacion", "laboratorio-bioinstrumentacion",
        "biosensores",
    },
    {
        "imagenes-biomedicas", "imagenes-biomedicas-avanzadas-i", "imagenes-biomedicas-avanzadas-ii",
        "tratamiento-digital-imagenes", "laboratorio-imagenes-biomedicas",
        "simulacion-planificacion-quirurgica", "biofotonica",
    },
    {
        "biomateriales", "biomateriales-implantes", "polimeros-procesamiento-materiales",
        "ingenieria-tejidos", "desarrollo-dispositivos-medicos", "ingenieria-clinica-gestion",
    },
    {
        "informatica-biomedica", "historias-clinicas-terminologias-estandares",
        "aplicaciones-salud-digital", "ingenieria-datos-biomedicos",
        "sistemas-ayuda-decision-medica", "interfaces-hombre-maquina",
    },
    {
        "comunicacion-cientifica", "uso-profesional-ingles", "etica-responsabilidad-social",
        "historia-filosofia-ciencia", "politicas-publicas-ciencia-tecnologia",
    },
    {
        "economia-gestion-empresas", "innovacion-emprendimiento",
        "laboratorio-globalizacion-emprendimiento", "tecnologias-administracion",
        "politicas-publicas-ciencia-tecnologia", "desarrollo-dispositivos-medicos",
    },
)

REQUIRED_AREA_TEMPLATE_KEYS = {
    "area_title",
    "area_description",
    "css_path",
    "editorial_css_path",
    "home_path",
    "subject_count",
    "subject_cards",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo de datos: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"No existe la plantilla: {path}")
    return path.read_text(encoding="utf-8")


@cache
def load_outlines() -> dict[str, dict[str, list[list[str]]]]:
    return load_json(OUTLINES_PATH)


@cache
def subject_catalog() -> dict[str, dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}
    for area in load_json(DATA_PATH).get("areas", []):
        for order, subject in enumerate(area.get("subjects", [])):
            catalog[subject["id"]] = {
                **subject,
                "area_id": area["id"],
                "area_title": area["title"],
                "order": order,
            }
    return catalog


def unique_strings(items: list[str], limit: int | None = None) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        cleaned = str(item).strip()
        normalized = cleaned.casefold()
        if not cleaned or normalized in seen:
            continue
        seen.add(normalized)
        result.append(cleaned)
        if limit is not None and len(result) >= limit:
            break
    return result


def prerequisites_for(area_id: str, subject_id: str) -> list[str]:
    statistics = {"probabilidad-estadistica", "bioestadistica", "analisis-estadistico-multivariado"}
    computing = {
        "algoritmos-estructuras-datos", "arquitectura-computadores", "bases-datos",
        "redes-comunicaciones", "redes-servicios", "ingenieria-datos-biomedicos",
        "nlp-recuperacion-informacion", "bioinformatica", "informatica-biomedica",
    }
    quantitative_engineering = {
        "biofisica", "sistemas-electronicos", "sistemas-senales", "teoria-senal-biocomputacion",
        "bioinstrumentacion", "biomecanica", "biomecanica-medios-continuos", "biofotonica",
        "imagenes-biomedicas-avanzadas-i", "imagenes-biomedicas-avanzadas-ii",
        "modelado-simulacion-biomedicina", "tratamiento-digital-imagenes",
    }
    if subject_id == "algebra":
        return [
            "Aritmética, fracciones, potencias y proporcionalidad de nivel preuniversitario.",
            "Lectura de tablas, ejes cartesianos y expresiones cuantitativas sencillas.",
            "Disposición para justificar cada procedimiento y comprobar unidades y resultados.",
        ]
    if subject_id == "fundamentos-programacion":
        return [
            "Manejo básico de archivos y carpetas en un computador.",
            "Razonamiento lógico y capacidad para descomponer problemas en pasos.",
            "No se requiere experiencia previa en programación.",
        ]
    if subject_id in statistics:
        return [
            "Álgebra elemental, funciones y lectura de gráficos.",
            "Conceptos básicos de diseño de estudios y tipos de variables.",
            "Manejo introductorio de hojas de cálculo o un lenguaje como R o Python.",
        ]
    if subject_id in computing:
        return [
            "Fundamentos de programación: variables, control de flujo, funciones y archivos.",
            "Álgebra y razonamiento lógico de nivel universitario inicial.",
            "Uso básico de terminal, control de versiones y documentación técnica.",
        ]
    if subject_id in quantitative_engineering:
        return [
            "Álgebra, cálculo y física de nivel universitario inicial.",
            "Programación básica para análisis numérico y visualización.",
            "Fundamentos de biología o fisiología pertinentes al sistema estudiado.",
        ]
    if area_id == "biologicas-medicas":
        return [
            "Biología general y química de nivel universitario inicial.",
            "Bases de estructura celular, biomoléculas y homeostasis.",
            "Lectura de figuras científicas y estadística descriptiva elemental.",
        ]
    if area_id == "ingenieria-biomedica":
        return [
            "Matemáticas, física y programación de nivel universitario inicial.",
            "Bases de biología celular, anatomía o fisiología humana.",
            "Capacidad para documentar requisitos, supuestos, mediciones y resultados.",
        ]
    if area_id == "gestion-etica-comunicacion":
        return [
            "Comprensión lectora y escritura académica de nivel universitario.",
            "Familiaridad introductoria con ciencia, tecnología y salud.",
            "Disposición para analizar perspectivas, evidencia, incertidumbre y consecuencias sociales.",
        ]
    return [
        "Matemáticas y razonamiento cuantitativo de nivel preuniversitario.",
        "Lectura de gráficos, tablas, fórmulas y unidades científicas.",
        "Capacidad para documentar procedimientos y comprobar la coherencia de resultados.",
    ]


def resources_for(area_id: str, subject_id: str) -> list[dict[str, str]]:
    statistics = {"probabilidad-estadistica", "bioestadistica", "analisis-estadistico-multivariado"}
    computing = {
        "fundamentos-programacion", "algoritmos-estructuras-datos", "arquitectura-computadores",
        "bases-datos", "redes-comunicaciones", "redes-servicios", "ingenieria-datos-biomedicos",
        "nlp-recuperacion-informacion", "teoria-senal-biocomputacion",
    }
    chemistry = {"quimica-i", "quimica-ii", "quimica-medicinal", "bioquimica"}
    imaging = {
        "imagenes-biomedicas", "imagenes-biomedicas-avanzadas-i", "imagenes-biomedicas-avanzadas-ii",
        "laboratorio-imagenes-biomedicas", "tratamiento-digital-imagenes",
        "simulacion-planificacion-quirurgica",
    }
    informatics = {
        "bioinformatica", "informatica-biomedica", "historias-clinicas-terminologias-estandares",
        "aplicaciones-salud-digital", "sistemas-ayuda-decision-medica",
    }
    if subject_id in statistics:
        return [
            {"title": "OpenIntro Statistics", "description": "Texto abierto con datos, ejercicios y fundamentos de inferencia.", "type": "libro abierto", "url": "https://www.openintro.org/book/os/"},
            {"title": "NIST/SEMATECH e-Handbook", "description": "Manual oficial de métodos estadísticos y control de procesos.", "type": "manual", "url": "https://www.itl.nist.gov/div898/handbook/"},
            {"title": "R Project Manuals", "description": "Documentación oficial para análisis estadístico reproducible con R.", "type": "documentación", "url": "https://cran.r-project.org/manuals.html"},
            {"title": "EQUATOR Network", "description": "Guías para reportar estudios de salud de forma transparente.", "type": "guías", "url": "https://www.equator-network.org/"},
            {"title": "NCBI Bookshelf", "description": "Capítulos abiertos de bioestadística, epidemiología y medicina basada en evidencia.", "type": "biblioteca", "url": "https://www.ncbi.nlm.nih.gov/books/"},
        ]
    if subject_id in computing:
        return [
            {"title": "Python Documentation", "description": "Tutorial y referencia oficial del lenguaje Python.", "type": "documentación", "url": "https://docs.python.org/3/"},
            {"title": "Software Carpentry Lessons", "description": "Lecciones abiertas sobre programación, terminal, Git y trabajo reproducible.", "type": "curso abierto", "url": "https://software-carpentry.org/lessons/"},
            {"title": "MIT OpenCourseWare", "description": "Cursos abiertos de programación, algoritmos, redes y matemáticas.", "type": "cursos abiertos", "url": "https://ocw.mit.edu/"},
            {"title": "PhysioNet", "description": "Datos y herramientas abiertas para practicar con señales y registros fisiológicos.", "type": "datos abiertos", "url": "https://physionet.org/"},
            {"title": "The Turing Way", "description": "Guía abierta de ciencia de datos reproducible, colaborativa y ética.", "type": "guía", "url": "https://book.the-turing-way.org/"},
        ]
    if subject_id in chemistry:
        return [
            {"title": "OpenStax Chemistry 2e", "description": "Texto abierto de química general con ejercicios y fundamentos.", "type": "libro abierto", "url": "https://openstax.org/details/books/chemistry-2e"},
            {"title": "IUPAC Gold Book", "description": "Compendio oficial de terminología química.", "type": "referencia", "url": "https://goldbook.iupac.org/"},
            {"title": "PubChem", "description": "Base de datos pública de compuestos, propiedades y bioactividad.", "type": "base de datos", "url": "https://pubchem.ncbi.nlm.nih.gov/"},
            {"title": "NCBI Bookshelf", "description": "Libros abiertos de bioquímica, farmacología y ciencias biomédicas.", "type": "biblioteca", "url": "https://www.ncbi.nlm.nih.gov/books/"},
            {"title": "ChEMBL", "description": "Base de datos curada de moléculas bioactivas y dianas.", "type": "base de datos", "url": "https://www.ebi.ac.uk/chembl/"},
        ]
    if subject_id in imaging:
        return [
            {"title": "3D Slicer Documentation", "description": "Plataforma abierta para visualización, segmentación y análisis de imagen médica.", "type": "software abierto", "url": "https://slicer.readthedocs.io/"},
            {"title": "ITK Documentation", "description": "Biblioteca abierta para registro, segmentación y procesamiento de imágenes.", "type": "documentación", "url": "https://docs.itk.org/"},
            {"title": "DICOM Standard", "description": "Fuente oficial del estándar de imagen y comunicación médica.", "type": "estándar", "url": "https://www.dicomstandard.org/current"},
            {"title": "NIBIB Science Topics", "description": "Introducciones oficiales a modalidades y tecnologías de imagen biomédica.", "type": "recurso educativo", "url": "https://www.nibib.nih.gov/science-education/science-topics"},
            {"title": "The Cancer Imaging Archive", "description": "Colecciones públicas de imágenes oncológicas para investigación y docencia.", "type": "datos abiertos", "url": "https://www.cancerimagingarchive.net/"},
        ]
    if subject_id in informatics:
        return [
            {"title": "HL7 FHIR Specification", "description": "Especificación oficial para intercambio de información sanitaria.", "type": "estándar", "url": "https://hl7.org/fhir/"},
            {"title": "SNOMED CT", "description": "Información oficial sobre la terminología clínica internacional.", "type": "terminología", "url": "https://www.snomed.org/"},
            {"title": "LOINC", "description": "Estándar para identificar mediciones, observaciones y documentos clínicos.", "type": "terminología", "url": "https://loinc.org/"},
            {"title": "WHO Digital Health", "description": "Recursos de la OMS sobre estrategia, gobernanza y salud digital.", "type": "recurso institucional", "url": "https://www.who.int/health-topics/digital-health"},
            {"title": "PhysioNet", "description": "Datos clínicos y fisiológicos abiertos para aprendizaje y validación.", "type": "datos abiertos", "url": "https://physionet.org/"},
        ]
    if area_id == "biologicas-medicas":
        return [
            {"title": "OpenStax Biology 2e", "description": "Texto abierto para fundamentos celulares, genéticos y fisiológicos.", "type": "libro abierto", "url": "https://openstax.org/details/books/biology-2e"},
            {"title": "NCBI Bookshelf", "description": "Biblioteca pública de libros y capítulos biomédicos.", "type": "biblioteca", "url": "https://www.ncbi.nlm.nih.gov/books/"},
            {"title": "PubMed", "description": "Buscador de literatura biomédica para ampliar y contrastar contenidos.", "type": "literatura", "url": "https://pubmed.ncbi.nlm.nih.gov/"},
            {"title": "EMBL-EBI Training", "description": "Cursos abiertos sobre biología molecular, datos y bioinformática.", "type": "cursos abiertos", "url": "https://www.ebi.ac.uk/training/"},
            {"title": "Human Protein Atlas", "description": "Datos abiertos de expresión y localización de proteínas humanas.", "type": "atlas", "url": "https://www.proteinatlas.org/"},
        ]
    if area_id == "gestion-etica-comunicacion":
        return [
            {"title": "World Health Organization", "description": "Informes, políticas y recursos institucionales sobre salud global.", "type": "fuente institucional", "url": "https://www.who.int/"},
            {"title": "UNESCO Bioethics", "description": "Instrumentos y recursos sobre ética de ciencia, tecnología y salud.", "type": "recurso institucional", "url": "https://www.unesco.org/en/ethics-science-technology/bioethics"},
            {"title": "EQUATOR Network", "description": "Guías de reporte para investigación en salud.", "type": "guías", "url": "https://www.equator-network.org/"},
            {"title": "Committee on Publication Ethics", "description": "Orientación sobre integridad, autoría y publicación científica.", "type": "guías", "url": "https://publicationethics.org/"},
            {"title": "OECD Science, Technology and Innovation", "description": "Datos y análisis de políticas de ciencia, tecnología e innovación.", "type": "fuente institucional", "url": "https://www.oecd.org/sti/"},
        ]
    return [
        {"title": "MIT OpenCourseWare", "description": "Cursos abiertos de ciencias e ingeniería para reforzar fundamentos.", "type": "cursos abiertos", "url": "https://ocw.mit.edu/"},
        {"title": "NIBIB Science Topics", "description": "Recursos oficiales sobre tecnologías biomédicas y sus aplicaciones.", "type": "recurso educativo", "url": "https://www.nibib.nih.gov/science-education/science-topics"},
        {"title": "FDA CDRH Learn", "description": "Módulos oficiales sobre dispositivos médicos, calidad y regulación.", "type": "formación oficial", "url": "https://www.fda.gov/training-and-continuing-education/cdrh-learn"},
        {"title": "WHO Medical Devices", "description": "Recursos sobre selección, gestión y acceso a dispositivos médicos.", "type": "recurso institucional", "url": "https://www.who.int/health-topics/medical-devices"},
        {"title": "PhysioNet", "description": "Datos fisiológicos abiertos para docencia, análisis y validación.", "type": "datos abiertos", "url": "https://physionet.org/"},
    ]


def related_subjects_for(subject_id: str, area_id: str) -> list[str]:
    catalog = subject_catalog()
    current_families = [family for family in COURSE_FAMILIES if subject_id in family]
    ranked: list[tuple[int, int, str]] = []
    for candidate_id, candidate in catalog.items():
        if candidate_id == subject_id:
            continue
        shared_families = sum(candidate_id in family for family in current_families)
        same_area = candidate["area_id"] == area_id
        if not shared_families and not same_area:
            continue
        score = shared_families * 10 + int(same_area)
        ranked.append((-score, candidate["order"], candidate_id))
    ranked.sort()
    result: list[str] = []
    for _, _, candidate_id in ranked:
        candidate = catalog[candidate_id]
        result.append(f"{candidate['title']}: {candidate['description']}")
        if len(result) == 6:
            break
    return result


def synthesize_course(area: dict[str, Any], subject: dict[str, Any]) -> dict[str, Any]:
    outlines = load_outlines()
    try:
        raw_units = outlines[area["id"]][subject["id"]]
    except KeyError as exc:
        raise ValueError(f"Falta temario para {area['id']}/{subject['id']} en {OUTLINES_PATH.relative_to(ROOT)}") from exc

    title = subject["title"]
    connection = subject["biomedical_connection"]
    units: list[dict[str, Any]] = []
    concepts: list[str] = []
    for number, raw_unit in enumerate(raw_units, start=1):
        if len(raw_unit) != 3:
            raise ValueError(f"Unidad inválida en {area['id']}/{subject['id']}: se esperaban título, temas y aplicación")
        unit_title, topic_text, application = raw_unit
        topics = [topic.strip() for topic in topic_text.split(";") if topic.strip()]
        if len(topics) < 3:
            raise ValueError(f"La unidad {number} de {area['id']}/{subject['id']} requiere al menos tres temas")
        concepts.extend([unit_title, *topics])
        units.append({
            "unit": number,
            "title": unit_title,
            "description": (
                f"Desarrolla {', '.join(topics[:-1])} y {topics[-1]}, conectando los fundamentos "
                f"de {title} con problemas verificables y decisiones propias del ámbito biomédico."
            ),
            "topics": [topic[0].upper() + topic[1:] + "." for topic in topics],
            "learning_outcomes": [
                f"Explicar las relaciones principales entre {', '.join(topics)}.",
                f"Aplicar estos conceptos a un caso relacionado con {application}.",
            ],
            "activities": [
                f"Construir un esquema razonado de {unit_title.lower()} que identifique variables, relaciones y supuestos.",
                f"Resolver y documentar un caso breve sobre {application}, indicando evidencia necesaria y limitaciones.",
            ],
            "biomedical_applications": [
                application[0].upper() + application[1:] + ".",
                connection,
            ],
        })

    modules = [f"{unit['title']}: {'; '.join(item.rstrip('.') for item in unit['topics'])}." for unit in units]
    practical_activities = [
        {
            "title": f"Taller {number}: {unit['title']}",
            "description": (
                f"Producto individual o colaborativo que integra {', '.join(topic.rstrip('.').lower() for topic in unit['topics'])}; "
                "debe documentar procedimiento, supuestos, resultados y limitaciones."
            ),
            "type": "actividad aplicada",
        }
        for number, unit in enumerate(units, start=1)
    ]
    return {
        **subject,
        "status": "generated",
        "level": (
            "Pregrado universitario inicial e intermedio"
            if area["id"] == "ciencias-basicas"
            else "Pregrado universitario intermedio y avanzado"
        ),
        "estimated_workload": "16 semanas; 6-8 horas semanales; 120-150 horas totales de estudio, práctica y evaluación",
        "prerequisites": prerequisites_for(area["id"], subject["id"]),
        "course_competencies": [
            f"Explicar con precisión los principios, métodos y límites de {title}.",
            f"Aplicar herramientas de {title} a preguntas científicas, tecnológicas o sanitarias bien definidas.",
            "Interpretar datos, modelos, mediciones o argumentos distinguiendo resultado, inferencia y limitación.",
            "Seleccionar métodos y recursos apropiados, justificando supuestos, criterios de calidad y riesgos.",
            "Integrar fundamentos cuantitativos, biológicos, técnicos y éticos en problemas biomédicos.",
            "Comunicar procedimientos y conclusiones de forma clara, trazable y reproducible.",
        ],
        "learning_objectives": [
            f"Comprender el vocabulario, los modelos y los principios fundamentales de {title}.",
            "Relacionar los contenidos de las unidades en una visión progresiva y coherente del campo.",
            "Resolver problemas aplicados documentando datos, supuestos, procedimientos y comprobaciones.",
            "Interpretar evidencia y resultados sin confundir asociación, predicción, mecanismo o causalidad.",
            f"Conectar {title} con necesidades reales de investigación, tecnología, salud y enfermedad.",
            "Desarrollar autonomía para continuar aprendiendo con fuentes abiertas y documentación primaria.",
        ],
        "learning_outcomes": [
            *[
                f"Describir y aplicar los conceptos de {unit['title'].lower()} en un ejercicio o caso biomédico."
                for unit in units
            ],
            "Comparar al menos dos métodos o explicaciones, justificando su elección con criterios explícitos.",
            "Entregar un análisis reproducible que incluya procedimiento, resultados, incertidumbre y limitaciones.",
        ],
        "modules": modules,
        "detailed_units": units,
        "practical_activities": practical_activities,
        "assessment": [
            {"title": "Pruebas conceptuales", "description": "Problemas breves que evalúan comprensión, relaciones entre conceptos y detección de errores frecuentes.", "weight": "20%"},
            {"title": "Talleres aplicados", "description": "Entregas de las unidades con procedimiento, comprobaciones, resultados y reflexión sobre limitaciones.", "weight": "25%"},
            {"title": "Análisis de evidencia", "description": "Lectura crítica de datos, figuras, métodos o casos relevantes para la asignatura.", "weight": "20%"},
            {"title": "Proyecto integrador", "description": f"Resolución documentada de un problema de {title} conectado con una aplicación biomédica realista.", "weight": "25%"},
            {"title": "Comunicación y bitácora", "description": "Presentación clara del trabajo y registro de decisiones, dudas, correcciones y aprendizajes.", "weight": "10%"},
        ],
        "key_concepts": unique_strings(concepts, limit=24),
        "related_subjects": related_subjects_for(subject["id"], area["id"]),
        "suggested_resources": resources_for(area["id"], subject["id"]),
    }


def escape(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def normalize_output(value: str) -> str:
    """Normaliza espacios finales y garantiza un único salto de línea al final."""
    return "\n".join(line.rstrip() for line in value.splitlines()).rstrip() + "\n"


def rel_path(from_file: Path, to_file: Path) -> str:
    """Devuelve una ruta relativa POSIX desde un HTML generado hacia otro archivo."""
    start_dir = from_file.parent
    return Path(os.path.relpath(to_file, start=start_dir)).as_posix()


def render_list(items: list[Any], empty_message: str) -> str:
    if not items:
        return f'<p class="muted">{escape(empty_message)}</p>'
    rendered = "\n".join(f"        <li>{escape(item)}</li>" for item in items)
    return f"<ul>\n{rendered}\n      </ul>"


def render_key_value_list(items: list[dict[str, Any]], empty_message: str) -> str:
    if not items:
        return f'<p class="muted">{escape(empty_message)}</p>'
    rendered_items = []
    for item in items:
        title = escape(item.get("title", item.get("name", "Elemento")))
        description = escape(item.get("description", ""))
        extra = escape(item.get("weight", item.get("type", "")))
        url = str(item.get("url", "")).strip()
        if url.startswith(("https://", "http://")):
            title_html = f'<a class="resource-link" href="{escape(url)}" rel="noopener noreferrer">{title}</a>'
        else:
            title_html = title
        meta = f'<span class="course-tag">{extra}</span>' if extra else ""
        rendered_items.append(
            "        <li>"
            f"<strong>{title_html}</strong>{meta}"
            f"<p>{description}</p>"
            "</li>"
        )
    return '<ul class="rich-list">\n' + "\n".join(rendered_items) + "\n      </ul>"


def render_units(units: list[dict[str, Any]], empty_message: str) -> str:
    if not units:
        return f'<p class="muted">{escape(empty_message)}</p>'
    rendered_units = []
    for unit in units:
        number = escape(unit.get("unit", ""))
        title = escape(unit.get("title", "Unidad"))
        description = escape(unit.get("description", ""))
        topics = render_list(unit.get("topics", []), "Temas pendientes.")
        outcomes = render_list(unit.get("learning_outcomes", []), "Resultados pendientes.")
        activities = render_list(unit.get("activities", []), "Actividades pendientes.")
        applications = render_list(unit.get("biomedical_applications", []), "Aplicaciones pendientes.")
        unit_href = f"unidades/unidad-{int(unit.get('unit', 0)):02d}.html"
        rendered_units.append(
            "      <article class=\"course-unit\">\n"
            f"        <h3>Unidad {number}. {title}</h3>\n"
            f"        <p>{description}</p>\n"
            "        <h4>Temas</h4>\n"
            f"        {topics}\n"
            "        <h4>Resultados esperados</h4>\n"
            f"        {outcomes}\n"
            "        <h4>Actividades</h4>\n"
            f"        {activities}\n"
            "        <h4>Aplicaciones biomédicas</h4>\n"
            f"        {applications}\n"
            f'        <a class="btn-link unit-link" href="{unit_href}">Abrir unidad completa →</a>\n'
            "      </article>"
        )
    return '<div class="course-units">\n' + "\n".join(rendered_units) + "\n      </div>"


def pedagogical_frame_for(area_id: str, subject_id: str) -> dict[str, Any]:
    """Selecciona una estructura de razonamiento coherente con la disciplina."""
    if subject_id in STATISTICS_SUBJECTS:
        key = "statistics"
    elif subject_id in DIGITAL_HEALTH_SUBJECTS:
        key = "digital_health"
    elif subject_id in COMPUTING_SUBJECTS:
        key = "computing"
    elif subject_id in SIGNAL_IMAGING_SUBJECTS:
        key = "signals"
    elif subject_id in DEVICE_SUBJECTS:
        key = "devices"
    elif subject_id in MATERIALS_SUBJECTS:
        key = "materials"
    elif subject_id in PHYSIOLOGY_SUBJECTS:
        key = "physiology"
    elif subject_id in BIOLOGY_SUBJECTS:
        key = "biology"
    elif area_id == "gestion-etica-comunicacion":
        key = "management"
    else:
        key = "quantitative"
    return PEDAGOGICAL_FRAMES[key]


def clean_topic(value: Any) -> str:
    return str(value or "").strip().rstrip(".")


def concept_definition(topic: str, course: dict[str, Any], frame: dict[str, Any]) -> tuple[str, bool]:
    normalized = clean_topic(topic).casefold()
    if "muestreo" in normalized and frame["name"] == "inferencia basada en datos":
        return (
            "Proceso de seleccionar unidades de una población para obtener información sobre ella mediante un mecanismo de selección que permita evaluar representatividad y error.",
            True,
        )
    if normalized == "validación" or normalized.startswith("validación "):
        return (
            f"Proceso de reunir evidencia de que un resultado es adecuado para el uso previsto dentro de {frame['name']}, con criterios definidos antes de evaluar el resultado.",
            True,
        )
    for pattern in sorted(CONCEPT_DEFINITIONS, key=len, reverse=True):
        if pattern in normalized:
            return CONCEPT_DEFINITIONS[pattern], True
    return (
        f"Tema de {course['title']} que organiza entidades, relaciones o procedimientos propios de {frame['name']}; "
        "su significado operativo se fija indicando qué representa, cómo se observa o calcula y en qué condiciones deja de ser aplicable.",
        False,
    )


def natural_join(items: list[str]) -> str:
    cleaned = [clean_topic(item) for item in items if clean_topic(item)]
    if not cleaned:
        return "los contenidos de la unidad"
    if len(cleaned) == 1:
        return cleaned[0]
    return ", ".join(cleaned[:-1]) + " y " + cleaned[-1]


def render_theory_sections(area: dict[str, Any], course: dict[str, Any], unit: dict[str, Any]) -> str:
    frame = pedagogical_frame_for(area["id"], course["id"])
    topics = [clean_topic(topic) for topic in unit.get("topics", [])]
    application = clean_topic((unit.get("biomedical_applications") or [course["biomedical_connection"]])[0])
    sections: list[str] = []
    for index, topic in enumerate(topics, start=1):
        related = [item for item in topics if item != topic]
        relation_text = natural_join(related)
        sequence = " → ".join(frame["sequence"])
        definition, _ = concept_definition(topic, course, frame)
        sections.append(
            '      <article class="lesson-topic">\n'
            f"        <p class=\"eyebrow\">Concepto {index}</p>\n"
            f"        <h3>{escape(topic)}</h3>\n"
            f"        <p><strong>Definición.</strong> {escape(definition)}</p>\n"
            f"        <p><strong>Alcance.</strong> En {escape(course['title'])}, el tema de {escape(topic.lower())} se estudia dentro de {escape(unit['title'].lower())}. "
            f"Dominarlo exige responder {escape(frame['central_question'])}; además de la definición hay que reconocer componentes, relaciones, condiciones de aplicación y señales de error.</p>\n"
            f"        <p><strong>Relaciones.</strong> Este concepto se interpreta junto con {escape(relation_text)}. La conexión debe expresarse como una cadena explicable: "
            f"qué información entra, qué transformación o mecanismo ocurre, qué resultado se observa y qué evidencia permitiría comprobarlo. La ruta recomendada es: {escape(sequence)}.</p>\n"
            f"        <p><strong>Aplicación.</strong> En el caso de {escape(application.lower())}, el concepto ayuda a formular una pregunta precisa y a seleccionar observaciones o mediciones pertinentes. "
            f"La conclusión debe apoyarse en {escape(frame['evidence'])}. Debe recordarse que {escape(frame['caution'])}.</p>\n"
            "        <h4>Comprobación de dominio</h4>\n"
            "        <ul>\n"
            f"          <li>Definir {escape(topic.lower())} con palabras propias y delimitar qué queda fuera del concepto.</li>\n"
            f"          <li>Representar su relación con {escape(relation_text)} mediante un esquema, tabla, modelo o procedimiento.</li>\n"
            f"          <li>Proponer una evidencia que apoyaría la interpretación y otra observación que la debilitaría.</li>\n"
            "          <li>Identificar al menos un supuesto, una fuente de incertidumbre y un caso límite.</li>\n"
            "        </ul>\n"
            "      </article>"
        )
    return '<div class="lesson-topics">\n' + "\n".join(sections) + "\n      </div>"


def render_worked_case(area: dict[str, Any], course: dict[str, Any], unit: dict[str, Any]) -> str:
    frame = pedagogical_frame_for(area["id"], course["id"])
    topics = [clean_topic(topic) for topic in unit.get("topics", [])]
    application = clean_topic((unit.get("biomedical_applications") or [course["biomedical_connection"]])[0])
    steps = [
        ("Pregunta", f"Determinar cómo {unit['title'].lower()} puede aportar a {application.lower()}, sin convertir un resultado educativo en una decisión clínica."),
        ("Representación", f"Organizar {natural_join(topics)} en un mapa que muestre entradas, relaciones, resultados y supuestos."),
        ("Método", f"Seguir la secuencia de {frame['name']}: {'; '.join(frame['sequence'])}."),
        ("Evidencia", f"Solicitar {frame['evidence']}; registrar procedencia, unidades, parámetros y criterios de aceptación."),
        ("Conclusión", f"Redactar por separado lo observado, lo inferido y lo que todavía requiere verificación. La propuesta queda limitada al uso educativo y al contexto descrito."),
    ]
    rendered_steps = "\n".join(
        f"        <li><strong>{escape(title)}.</strong> {escape(description)}</li>" for title, description in steps
    )
    return (
        f"      <p class=\"case-prompt\"><strong>Situación.</strong> Un equipo académico necesita estudiar {escape(application.lower())}. "
        f"Debe integrar {escape(natural_join(topics))} y producir una recomendación verificable sin usar datos personales ni intervenir en pacientes.</p>\n"
        "      <ol class=\"case-steps\">\n"
        f"{rendered_steps}\n"
        "      </ol>\n"
        "      <details class=\"answer-panel\"><summary>Ver criterio de solución</summary>\n"
        f"        <p>Una solución sólida entrega un {escape(frame['product'])}; declara la pregunta, los datos o evidencias necesarios, el procedimiento, los criterios de calidad, el resultado y sus límites. "
        f"No afirma causalidad, eficacia o seguridad más allá de la evidencia disponible y explica cómo se comprobaría cada afirmación.</p>\n"
        "      </details>"
    )


def render_guided_activity(area: dict[str, Any], course: dict[str, Any], unit: dict[str, Any]) -> str:
    frame = pedagogical_frame_for(area["id"], course["id"])
    topics = [clean_topic(topic) for topic in unit.get("topics", [])]
    application = clean_topic((unit.get("biomedical_applications") or [course["biomedical_connection"]])[0])
    return (
        f"      <p><strong>Producto:</strong> {escape(frame['product'].capitalize())} sobre {escape(application.lower())}.</p>\n"
        "      <ol class=\"activity-steps\">\n"
        f"        <li><strong>Delimita.</strong> Formula una pregunta, el contexto de uso y el resultado esperado. Incluye {escape(natural_join(topics))}.</li>\n"
        "        <li><strong>Prepara.</strong> Usa un caso simulado, literatura o datos abiertos sin identificadores personales. Registra fuente, licencia, versión y diccionario de variables.</li>\n"
        f"        <li><strong>Resuelve.</strong> Aplica esta secuencia: {escape(' → '.join(frame['sequence']))}. Conserva cálculos, decisiones y resultados intermedios.</li>\n"
        f"        <li><strong>Verifica.</strong> Contrasta con {escape(frame['evidence'])}; incluye un control, un caso límite o una comparación alternativa.</li>\n"
        "        <li><strong>Comunica.</strong> Entrega una página con método, resultado, interpretación, incertidumbre, limitaciones y siguiente prueba necesaria.</li>\n"
        "      </ol>\n"
        "      <div class=\"rubric-grid\">\n"
        "        <div><strong>40%</strong><span>Corrección conceptual y método</span></div>\n"
        "        <div><strong>25%</strong><span>Evidencia y trazabilidad</span></div>\n"
        "        <div><strong>20%</strong><span>Interpretación y límites</span></div>\n"
        "        <div><strong>15%</strong><span>Claridad y reproducibilidad</span></div>\n"
        "      </div>"
    )


def render_self_assessment(area: dict[str, Any], course: dict[str, Any], unit: dict[str, Any]) -> str:
    frame = pedagogical_frame_for(area["id"], course["id"])
    topics = [clean_topic(topic) for topic in unit.get("topics", [])]
    application = clean_topic((unit.get("biomedical_applications") or [course["biomedical_connection"]])[0])
    first, second, third = (topics + [unit["title"]] * 3)[:3]
    questions = [
        (f"¿Qué significa dominar {first.lower()} en esta unidad?", f"Poder definirlo, delimitarlo, relacionarlo con {natural_join([second, third])}, aplicarlo a un caso y reconocer supuestos y límites."),
        (f"¿Cómo se relacionan {first.lower()} y {second.lower()}?", f"La respuesta debe mostrar dirección y mecanismo o procedimiento: qué entra, qué cambia, qué sale y qué evidencia permite verificar la relación."),
        ("¿Qué secuencia de trabajo evita saltar directamente a una conclusión?", " → ".join(item.capitalize() for item in frame["sequence"]) + "."),
        (f"¿Qué evidencia sería pertinente para {application.lower()}?", f"{frame['evidence'].capitalize()}, elegida de acuerdo con la pregunta, el contexto y el tipo de afirmación."),
        ("¿Cuál es el principal límite de interpretación?", frame["caution"].capitalize() + "."),
        ("¿Qué debe contener una entrega reproducible?", "Pregunta, fuente y versión de datos, supuestos, procedimiento, parámetros, resultados intermedios, comprobaciones, conclusión y limitaciones."),
    ]
    panels = []
    for number, (question, answer) in enumerate(questions, start=1):
        panels.append(
            f'      <details class="answer-panel"><summary>{number}. {escape(question)}</summary>'
            f"<p><strong>Respuesta esperada:</strong> {escape(answer)}</p></details>"
        )
    return '<div class="assessment-panels">\n' + "\n".join(panels) + "\n      </div>"


def render_glossary(area: dict[str, Any], course: dict[str, Any], unit: dict[str, Any]) -> str:
    frame = pedagogical_frame_for(area["id"], course["id"])
    topics = [clean_topic(topic) for topic in unit.get("topics", [])]
    entries = []
    for topic in topics:
        definition, _ = concept_definition(topic, course, frame)
        entries.append({
            "title": topic.capitalize(),
            "description": definition,
            "type": "concepto",
        })
    entries.extend([
        {"title": "Supuesto", "description": "Condición aceptada para construir un modelo o argumento y que debe declararse para poder evaluar su alcance.", "type": "razonamiento"},
        {"title": "Evidencia", "description": "Observación, medición o resultado documentado que apoya o contradice una afirmación.", "type": "método"},
        {"title": "Incertidumbre", "description": "Grado de conocimiento incompleto sobre una medición, parámetro, modelo o conclusión.", "type": "calidad"},
        {"title": "Validación", "description": f"Proceso para comprobar que el resultado es adecuado para el uso previsto dentro de {frame['name']}.", "type": "calidad"},
    ])
    return render_key_value_list(entries, "Glosario pendiente.")


def render_unit_nav_link(unit_number: int, unit_title: str, direction: str) -> str:
    href = f"unidad-{unit_number:02d}.html"
    arrow = "← " if direction == "previous" else " →"
    label = f"Unidad {unit_number}: {unit_title}"
    css_class = "btn-link secondary" if direction == "previous" else "btn-link"
    return f'<a class="{css_class}" href="{href}">{arrow if direction == "previous" else ""}{escape(label)}{" →" if direction == "next" else ""}</a>'


def render_unit_page(template: str, area: dict[str, Any], course: dict[str, Any], unit: dict[str, Any], index: int) -> str:
    units = course.get("detailed_units", [])
    output_path = ROOT / area["id"] / course["id"] / "unidades" / f"unidad-{int(unit['unit']):02d}.html"
    previous_unit = units[index - 1] if index > 0 else None
    next_unit = units[index + 1] if index < len(units) - 1 else None
    previous_link = render_unit_nav_link(int(previous_unit["unit"]), previous_unit["title"], "previous") if previous_unit else ""
    next_link = render_unit_nav_link(int(next_unit["unit"]), next_unit["title"], "next") if next_unit else ""
    frame = pedagogical_frame_for(area["id"], course["id"])
    replacements = {
        "unit_number": str(unit["unit"]),
        "unit_count": str(len(units)),
        "unit_title": escape(unit["title"]),
        "unit_description": escape(unit["description"]),
        "subject_title": escape(course["title"]),
        "area_title": escape(area["title"]),
        "css_path": rel_path(output_path, ROOT / "assets" / "css" / "style.css"),
        "editorial_css_path": rel_path(output_path, ROOT / "assets" / "css" / "editorial.css"),
        "home_path": rel_path(output_path, ROOT / "index.html"),
        "area_path": rel_path(output_path, ROOT / area["path"]),
        "subject_path": rel_path(output_path, ROOT / course["path"]),
        "units_index_path": "index.html",
        "previous_unit_link": previous_link,
        "next_unit_link": next_link,
        "learning_outcomes": render_list(unit.get("learning_outcomes", []), "Resultados pendientes."),
        "topics": render_list(unit.get("topics", []), "Temas pendientes."),
        "theory_sections": render_theory_sections(area, course, unit),
        "worked_case": render_worked_case(area, course, unit),
        "guided_activity": render_guided_activity(area, course, unit),
        "self_assessment": render_self_assessment(area, course, unit),
        "glossary": render_glossary(area, course, unit),
        "resources": render_key_value_list(course.get("suggested_resources", []), "Recursos pendientes."),
        "synthesis": escape(
            f"La unidad integra {natural_join(unit.get('topics', []))} mediante {frame['name']}. "
            f"El criterio de cierre es poder explicar, aplicar, comprobar y limitar una conclusión vinculada con "
            f"{clean_topic((unit.get('biomedical_applications') or [course['biomedical_connection']])[0]).lower()}."
        ),
    }
    output = template
    for key, value in replacements.items():
        output = output.replace("{{ " + key + " }}", value)
    return normalize_output(output)


def render_units_index(template: str, area: dict[str, Any], course: dict[str, Any]) -> str:
    output_path = ROOT / area["id"] / course["id"] / "unidades" / "index.html"
    cards = []
    for unit in course.get("detailed_units", []):
        cards.append(
            f'        <a class="link-card unit-index-card" href="unidad-{int(unit["unit"]):02d}.html">'
            f'<span class="course-tag">Unidad {int(unit["unit"])}</span>'
            f'<strong>{escape(unit["title"])}</strong><p>{escape(unit["description"])}</p>'
            '<span class="unit-index-action">Abrir lección →</span></a>'
        )
    replacements = {
        "subject_title": escape(course["title"]),
        "subject_description": escape(course["description"]),
        "area_title": escape(area["title"]),
        "unit_count": str(len(course.get("detailed_units", []))),
        "css_path": rel_path(output_path, ROOT / "assets" / "css" / "style.css"),
        "editorial_css_path": rel_path(output_path, ROOT / "assets" / "css" / "editorial.css"),
        "home_path": rel_path(output_path, ROOT / "index.html"),
        "area_path": rel_path(output_path, ROOT / area["path"]),
        "subject_path": rel_path(output_path, ROOT / course["path"]),
        "unit_cards": "\n".join(cards),
    }
    output = template
    for key, value in replacements.items():
        output = output.replace("{{ " + key + " }}", value)
    return normalize_output(output)


def subject_neighbors(subjects: list[dict[str, Any]], index: int) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    previous_subject = subjects[index - 1] if index > 0 else None
    next_subject = subjects[index + 1] if index < len(subjects) - 1 else None
    return previous_subject, next_subject


def render_nav_link(
    current_file: Path,
    subject: dict[str, Any] | None,
    label_prefix: str,
    css_class: str,
    label_suffix: str = "",
) -> str:
    if subject is None:
        return ""
    target = ROOT / subject["path"]
    href = rel_path(current_file, target)
    title = escape(subject.get("title", subject.get("id", "Asignatura")))
    css_classes = f"btn-link {css_class}".strip()
    label = f"{label_prefix} {title} {label_suffix}".strip()
    return f'<a class="{css_classes}" href="{href}">{label}</a>'


def validate_template(template: str) -> None:
    missing = [key for key in REQUIRED_TEMPLATE_KEYS if "{{ " + key + " }}" not in template]
    if missing:
        raise ValueError("La plantilla no contiene estas variables requeridas: " + ", ".join(sorted(missing)))


def validate_area_template(template: str) -> None:
    missing = [key for key in REQUIRED_AREA_TEMPLATE_KEYS if "{{ " + key + " }}" not in template]
    if missing:
        raise ValueError("La plantilla de área no contiene estas variables requeridas: " + ", ".join(sorted(missing)))


def validate_unit_templates(unit_template: str, units_template: str) -> None:
    missing_unit = [key for key in REQUIRED_UNIT_TEMPLATE_KEYS if "{{ " + key + " }}" not in unit_template]
    if missing_unit:
        raise ValueError("La plantilla de unidad no contiene: " + ", ".join(sorted(missing_unit)))
    missing_index = [key for key in REQUIRED_UNITS_TEMPLATE_KEYS if "{{ " + key + " }}" not in units_template]
    if missing_index:
        raise ValueError("La plantilla de índice de unidades no contiene: " + ", ".join(sorted(missing_index)))


def subject_overlay_path(area_id: str, subject_id: str) -> Path:
    return SUBJECT_DATA_DIR / area_id / f"{subject_id}.json"


def merge_subject_overlay(area: dict[str, Any], subject: dict[str, Any]) -> dict[str, Any]:
    """Combina metadatos centrales con contenido editorial opcional por asignatura."""
    merged = synthesize_course(area, subject)
    overlay_path = subject_overlay_path(area["id"], subject["id"])
    if not overlay_path.exists():
        merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])
        return merged

    overlay = load_json(overlay_path)
    if overlay.get("id") != subject["id"]:
        raise ValueError(f"Overlay con id inconsistente en {overlay_path.relative_to(ROOT)}")
    if overlay.get("area_id") != area["id"]:
        raise ValueError(f"Overlay con area_id inconsistente en {overlay_path.relative_to(ROOT)}")

    list_minimums = {
        "prerequisites": 3,
        "course_competencies": 4,
        "learning_objectives": 4,
        "learning_outcomes": 6,
        "modules": 6,
        "detailed_units": 6,
        "practical_activities": 4,
        "assessment": 3,
        "key_concepts": 10,
        "related_subjects": 4,
        "suggested_resources": 5,
    }
    for key, value in overlay.items():
        if key in {"id", "area_id"} or value in (None, "", []):
            continue
        minimum = list_minimums.get(key)
        if minimum is not None and isinstance(value, list) and len(value) < minimum:
            combined = list(value)
            seen = {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in combined}
            for item in merged.get(key, []):
                marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if marker not in seen:
                    combined.append(item)
                    seen.add(marker)
                if len(combined) >= minimum:
                    break
            merged[key] = combined
        else:
            merged[key] = value
    if merged.get("status") != "complete":
        merged["status"] = "generated"
    merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])
    return merged


def render_subject(template: str, area: dict[str, Any], subject: dict[str, Any], subjects: list[dict[str, Any]], index: int) -> str:
    subject = merge_subject_overlay(area, subject)
    output_path = ROOT / subject["path"]
    home_path = rel_path(output_path, ROOT / "index.html")
    area_path = rel_path(output_path, ROOT / area["path"])
    css_path = rel_path(output_path, ROOT / "assets" / "css" / "style.css")
    editorial_css_path = rel_path(output_path, ROOT / "assets" / "css" / "editorial.css")
    previous_subject, next_subject = subject_neighbors(subjects, index)

    replacements = {
        "subject_title": escape(subject.get("title", subject.get("id", "Asignatura"))),
        "area_title": escape(area.get("title", area.get("id", "Área"))),
        "subject_description": escape(subject.get("description", "Página de asignatura de CitoNauta Biomedicina.")),
        "css_path": css_path,
        "editorial_css_path": editorial_css_path,
        "home_path": home_path,
        "area_path": area_path,
        "previous_link": render_nav_link(output_path, previous_subject, "←", "secondary"),
        "next_link": render_nav_link(output_path, next_subject, "", "", "→"),
        "biomedical_connection": escape(subject.get("biomedical_connection", "Conexión biomédica pendiente de desarrollo.")),
        "level": escape(subject.get("level", "Pregrado universitario")),
        "estimated_workload": escape(subject.get("estimated_workload", "12-16 semanas; 90-150 horas de trabajo total")),
        "status": escape(subject.get("status", "placeholder")),
        "status_label": escape(subject.get("status_label", STATUS_LABELS["placeholder"])),
        "prerequisites": render_list(subject.get("prerequisites", []), "Prerrequisitos pendientes de desarrollo."),
        "course_competencies": render_list(subject.get("course_competencies", []), "Competencias pendientes de desarrollo."),
        "learning_objectives": render_list(subject.get("learning_objectives", []), "Objetivos de aprendizaje pendientes de desarrollo."),
        "learning_outcomes": render_list(subject.get("learning_outcomes", []), "Resultados de aprendizaje pendientes de desarrollo."),
        "modules": render_list(subject.get("modules", []), "Módulos pendientes de desarrollo."),
        "detailed_units": render_units(subject.get("detailed_units", []), "Unidades detalladas pendientes de desarrollo."),
        "practical_activities": render_key_value_list(subject.get("practical_activities", []), "Actividades prácticas pendientes de desarrollo."),
        "assessment": render_key_value_list(subject.get("assessment", []), "Evaluación sugerida pendiente de desarrollo."),
        "key_concepts": render_list(subject.get("key_concepts", []), "Conceptos clave pendientes de desarrollo."),
        "related_subjects": render_list(subject.get("related_subjects", []), "Relaciones curriculares pendientes de desarrollo."),
        "suggested_resources": render_key_value_list(subject.get("suggested_resources", []), "Recursos sugeridos pendientes de desarrollo."),
    }

    html_output = template
    for key, value in replacements.items():
        html_output = html_output.replace("{{ " + key + " }}", value)
    return html_output


def render_area(template: str, area: dict[str, Any]) -> str:
    output_path = ROOT / area["path"]
    cards: list[str] = []
    for subject in area.get("subjects", []):
        complete_subject = merge_subject_overlay(area, subject)
        href = rel_path(output_path, ROOT / subject["path"])
        title = escape(complete_subject.get("title", subject["title"]))
        description = escape(complete_subject.get("description", subject["description"]))
        if complete_subject.get("status") == "complete":
            status_label = "Revisado por especialista"
        elif complete_subject.get("status") == "generated":
            status_label = "Unidades desarrolladas"
        else:
            status_label = "En desarrollo"
        cards.append(
            f'      <a class="link-card course-card" href="{href}">\n'
            f"        <strong>{title}</strong>\n"
            f"        <p>{description}</p>\n"
            f'        <span class="course-tag">{status_label}</span>\n'
            "      </a>"
        )
    replacements = {
        "area_title": escape(area["title"]),
        "area_description": escape(area["description"]),
        "css_path": rel_path(output_path, ROOT / "assets" / "css" / "style.css"),
        "editorial_css_path": rel_path(output_path, ROOT / "assets" / "css" / "editorial.css"),
        "home_path": rel_path(output_path, ROOT / "index.html"),
        "subject_count": str(len(area.get("subjects", []))),
        "subject_cards": "\n".join(cards),
    }
    html_output = template
    for key, value in replacements.items():
        html_output = html_output.replace("{{ " + key + " }}", value)
    return html_output


def iter_subjects(data: dict[str, Any]):
    for area in data.get("areas", []):
        subjects = area.get("subjects", [])
        for index, subject in enumerate(subjects):
            yield area, subjects, index, subject


def should_include_subject(subject: dict[str, Any], only_subjects: set[str]) -> bool:
    if not only_subjects:
        return True
    return subject.get("id") in only_subjects or subject.get("path") in only_subjects


def generate(
    dry_run: bool,
    force: bool,
    only_missing: bool,
    only_subjects: set[str],
    with_units: bool = False,
    force_authored_units: bool = False,
) -> dict[str, int]:
    data = load_json(DATA_PATH)
    template = load_template(TEMPLATE_PATH)
    area_template = load_template(AREA_TEMPLATE_PATH)
    unit_template = load_template(UNIT_TEMPLATE_PATH) if with_units else ""
    units_template = load_template(UNITS_TEMPLATE_PATH) if with_units else ""
    validate_template(template)
    validate_area_template(area_template)
    if with_units:
        validate_unit_templates(unit_template, units_template)
    summary = {
        "generated": 0,
        "generated_areas": 0,
        "generated_units": 0,
        "generated_unit_indexes": 0,
        "preserved_authored_units": 0,
        "skipped_existing_units": 0,
        "skipped_existing": 0,
        "skipped_existing_areas": 0,
        "skipped_filter": 0,
        "would_generate": 0,
        "would_generate_areas": 0,
        "would_generate_units": 0,
        "would_generate_unit_indexes": 0,
        "errors": 0,
    }

    for area, subjects, index, subject in iter_subjects(data):
        if not should_include_subject(subject, only_subjects):
            summary["skipped_filter"] += 1
            continue

        target_path = ROOT / subject["path"]
        exists = target_path.exists()

        skip_course = False
        if exists and only_missing:
            summary["skipped_existing"] += 1
            skip_course = True
        elif exists and not force:
            summary["skipped_existing"] += 1
            skip_course = True

        if not skip_course:
            rendered = render_subject(template, area, subject, subjects, index)
            if dry_run:
                print(f"[dry-run] generaría: {target_path.relative_to(ROOT)}")
                summary["would_generate"] += 1
            else:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(normalize_output(rendered), encoding="utf-8")
                print(f"[ok] generado: {target_path.relative_to(ROOT)}")
                summary["generated"] += 1

        if not with_units:
            continue

        course = merge_subject_overlay(area, subject)
        units_dir = target_path.parent / "unidades"
        index_path = units_dir / "index.html"
        if not index_path.exists() or force:
            if dry_run:
                print(f"[dry-run] generaría índice: {index_path.relative_to(ROOT)}")
                summary["would_generate_unit_indexes"] += 1
            else:
                units_dir.mkdir(parents=True, exist_ok=True)
                index_path.write_text(render_units_index(units_template, area, course), encoding="utf-8")
                summary["generated_unit_indexes"] += 1

        for unit_index, unit in enumerate(course.get("detailed_units", [])):
            unit_path = units_dir / f"unidad-{int(unit['unit']):02d}.html"
            existing_text = unit_path.read_text(encoding="utf-8", errors="ignore") if unit_path.exists() else ""
            authored = bool(existing_text) and 'data-generated="citonauta-unit"' not in existing_text
            if authored and not force_authored_units:
                summary["preserved_authored_units"] += 1
                continue
            if unit_path.exists() and (only_missing or not force) and not force_authored_units:
                summary["skipped_existing_units"] += 1
                continue
            if dry_run:
                print(f"[dry-run] generaría unidad: {unit_path.relative_to(ROOT)}")
                summary["would_generate_units"] += 1
                continue
            units_dir.mkdir(parents=True, exist_ok=True)
            unit_path.write_text(render_unit_page(unit_template, area, course, unit, unit_index), encoding="utf-8")
            summary["generated_units"] += 1

    if not only_subjects:
        for area in data.get("areas", []):
            target_path = ROOT / area["path"]
            if target_path.exists() and not force:
                summary["skipped_existing_areas"] += 1
                continue
            rendered = render_area(area_template, area)
            if dry_run:
                print(f"[dry-run] generaría área: {target_path.relative_to(ROOT)}")
                summary["would_generate_areas"] += 1
                continue
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(normalize_output(rendered), encoding="utf-8")
            print(f"[ok] generada área: {target_path.relative_to(ROOT)}")
            summary["generated_areas"] += 1

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera páginas HTML de asignaturas para CitoNauta.")
    parser.add_argument("--dry-run", action="store_true", help="Muestra qué se generaría sin escribir archivos.")
    parser.add_argument("--force", action="store_true", help="Sobrescribe páginas existentes. Usar solo con revisión previa.")
    parser.add_argument("--only-missing", action="store_true", help="Genera solo páginas que no existan.")
    parser.add_argument("--subject", action="append", default=[], help="Genera solo una asignatura por id o ruta. Puede repetirse.")
    parser.add_argument("--with-units", action="store_true", help="Genera también las páginas lectivas e índices de todas las unidades.")
    parser.add_argument(
        "--force-authored-units",
        action="store_true",
        help="Sobrescribe unidades redactadas manualmente. No se recomienda para una regeneración normal.",
    )
    args = parser.parse_args()

    summary = generate(
        dry_run=args.dry_run,
        force=args.force,
        only_missing=args.only_missing,
        only_subjects=set(args.subject),
        with_units=args.with_units,
        force_authored_units=args.force_authored_units,
    )
    print("\nResumen:")
    for key, value in summary.items():
        print(f"- {key}: {value}")

    if not args.force:
        print("\nModo seguro activo: las páginas existentes no se sobrescriben sin --force.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
