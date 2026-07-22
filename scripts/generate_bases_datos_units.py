#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "generated_units" / "bases-datos"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)

UNITS: list[dict[str, Any]] = [
    {
        "unit": 1,
        "slug": "modelado-de-datos",
        "title": "Modelado de datos",
        "weeks": [1, 2],
        "hours": 16,
        "purpose": "Construir modelos conceptuales y lógicos que preserven identidad, relaciones, temporalidad, procedencia e integridad en conjuntos de datos biomédicos antes de elegir tablas o escribir SQL.",
        "artifact": "modelo trazable de personas ficticias, visitas, muestras y resultados de laboratorio",
        "sections": [
            {
                "heading": "Datos, información y contexto biomédico",
                "core": "distinguir observaciones, entidades, eventos y metadatos para evitar que una fila sea confundida con la realidad biológica o clínica que intenta representar",
                "entities": "personas ficticias, episodios, especímenes, pruebas, dispositivos y vocabularios deben tener identidades separadas y relaciones explícitas",
                "mechanism": "el análisis comienza identificando la unidad de observación, el proceso que generó cada dato y las reglas que determinan cuándo dos registros representan el mismo objeto",
                "decision": "la granularidad se elige según las preguntas y operaciones dominantes; mezclar niveles como paciente, visita y medición produce duplicaciones y denominadores ambiguos",
                "risk": "pérdida de contexto, confusión entre ausencia y valor cero, y sobreinterpretación de códigos aislados",
                "biomedical": "un resultado solo es interpretable junto con muestra, método, unidad, intervalo de referencia, instante y procedencia",
                "validation": "comprobar que cada atributo tiene significado, dominio, unidad y propietario semántico definidos",
                "equation": {"latex": "\lvert E \rvert = \text{número de entidades distintas}", "description": "La cardinalidad de una entidad no debe inferirse contando filas de una tabla con varias observaciones por entidad."},
            },
            {
                "heading": "Entidades, atributos, relaciones y cardinalidades",
                "core": "representar objetos mediante entidades, propiedades mediante atributos y asociaciones mediante relaciones con cardinalidades y obligatoriedad explícitas",
                "entities": "una persona puede tener muchas visitas, una visita muchas muestras y una muestra varios resultados, mientras que cada resultado debe conservar su muestra de origen",
                "mechanism": "los identificadores estables conectan entidades; las claves externas materializan relaciones y las restricciones impiden referencias inexistentes",
                "decision": "una relación muchos-a-muchos debe convertirse en una entidad asociativa cuando posee fecha, rol, cantidad, procedencia u otros atributos propios",
                "risk": "identificadores naturales inestables, relaciones implícitas en texto y multiplicación accidental de filas",
                "biomedical": "el vínculo entre muestra, alícuota, ensayo y resultado permite reconstruir qué material biológico produjo cada observación",
                "validation": "probar cardinalidades con casos mínimos, repetidos, ausentes y longitudinales, no solo con un diagrama ideal",
                "equation": {"latex": "1:N \Rightarrow \text{clave foránea en el lado }N", "description": "Regla práctica para materializar una relación uno-a-muchos en el modelo relacional."},
            },
            {
                "heading": "Temporalidad, versiones y procedencia",
                "core": "separar tiempo del fenómeno, tiempo de registro y tiempo de vigencia para reconstruir historias sin sobrescribir evidencia previa",
                "entities": "eventos, versiones, autores, sistemas de origen y transformaciones forman parte del modelo cuando la trazabilidad es un requisito",
                "mechanism": "cada cambio relevante se registra como nuevo estado o evento, enlazado con el estado anterior y con el proceso que lo produjo",
                "decision": "se elige entre instantáneas, historial de cambios o modelado bitemporal según las preguntas de auditoría y corrección retrospectiva",
                "risk": "usar una sola columna de fecha, actualizar valores destructivamente y mezclar correcciones con nuevas mediciones",
                "biomedical": "la fecha de toma de una muestra, la fecha de análisis y la fecha de carga pueden diferir y tener consecuencias analíticas distintas",
                "validation": "reconstruir el estado conocido en una fecha pasada y verificar que ninguna actualización borre la procedencia",
                "equation": {"latex": "t_{evento} \neq t_{registro} \neq t_{vigencia}", "description": "Los tres tiempos pueden coincidir, pero el modelo no debe asumirlo."},
            },
            {
                "heading": "Integridad, diccionario de datos y revisión del modelo",
                "core": "convertir supuestos del dominio en restricciones verificables y documentar cada variable para que el modelo sea auditable",
                "entities": "dominios, catálogos, unidades, identificadores, reglas de obligatoriedad y responsables de calidad complementan el diagrama",
                "mechanism": "las reglas se distribuyen entre tipos, restricciones, catálogos, validaciones de aplicación y controles periódicos de calidad",
                "decision": "una regla debe ubicarse lo más cerca posible del dato sin impedir cambios legítimos ni ocultar excepciones que requieren revisión",
                "risk": "documentación separada del esquema, listas de valores libres y reglas críticas aplicadas solo en hojas de cálculo",
                "biomedical": "el diccionario debe distinguir dato crudo, derivado, imputado, validado y excluido, además de explicar unidades y codificación",
                "validation": "realizar revisión por escenarios, consultar a especialistas del dominio y ejecutar pruebas de integridad sobre datos sintéticos adversariales",
                "equation": {"latex": "\text{calidad} = f(\text{validez},\text{completitud},\text{consistencia},\text{procedencia})", "description": "La calidad no es una propiedad única ni puede resumirse solo con ausencia de valores nulos."},
            },
        ],
        "glossary": [
            ["Entidad", "Objeto o concepto con identidad propia dentro del dominio."], ["Atributo", "Propiedad que describe una entidad o relación."],
            ["Relación", "Asociación semántica entre entidades."], ["Cardinalidad", "Número permitido de instancias relacionadas."],
            ["Identificador", "Valor estable que distingue una instancia de las demás."], ["Unidad de observación", "Nivel al que corresponde cada registro analítico."],
            ["Procedencia", "Información sobre origen y transformaciones de un dato."], ["Temporalidad", "Representación explícita de instantes, intervalos y versiones."],
            ["Dominio", "Conjunto de valores admisibles para un atributo."], ["Integridad", "Conjunto de propiedades que preservan coherencia estructural y semántica."],
            ["Diccionario de datos", "Documento que define variables, tipos, unidades, códigos y reglas."], ["Modelo conceptual", "Representación independiente de una tecnología concreta."],
        ],
        "examples": [
            ["Del formulario al modelo de biobanco", "Un formulario registra persona ficticia, visita, extracción, muestra, alícuota y ensayo en una sola hoja.", "Separar entidades, definir identificadores, convertir repeticiones en relaciones y añadir procedencia.", "El modelo evita duplicar datos personales y permite seguir cada resultado hasta su alícuota.", "No cubre consentimiento real ni requisitos regulatorios de un biobanco operativo."],
            ["Reconstrucción temporal de un resultado corregido", "Un laboratorio sustituye un resultado después de detectar un problema de calibración.", "Conservar el valor original, registrar una nueva versión, enlazar motivo, autor e instante de vigencia.", "La consulta puede mostrar el valor vigente y la auditoría puede reconstruir lo conocido previamente.", "El ejemplo no establece políticas clínicas de corrección ni comunicación."],
        ],
        "sources": [
            ["PostgreSQL — Data Definition", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/ddl.html"],
            ["SQLite — Foreign Key Support", "SQLite Consortium", "https://www.sqlite.org/foreignkeys.html"],
            ["Database Design — 2nd Edition", "BCcampus", "https://opentextbc.ca/dbdesign01/"],
            ["PROV-O: The PROV Ontology", "W3C", "https://www.w3.org/TR/prov-o/"],
            ["FHIR Resource", "HL7 International", "https://hl7.org/fhir/resource.html"],
            ["Data Quality", "National Library of Medicine", "https://www.nlm.nih.gov/oet/ed/stats/02-100.html"],
        ],
    },
    {
        "unit": 2,
        "slug": "modelo-relacional-y-normalizacion",
        "title": "Modelo relacional y normalización",
        "weeks": [3, 4, 5],
        "hours": 24,
        "purpose": "Aplicar claves, dependencias funcionales y normalización para reducir anomalías sin fragmentar innecesariamente el significado de los datos biomédicos.",
        "artifact": "esquema normalizado para cohortes, visitas, muestras, pruebas y resultados",
        "sections": [
            {
                "heading": "Relaciones, tuplas, dominios y claves",
                "core": "comprender el modelo relacional como un sistema de conjuntos de tuplas definidos por atributos y dominios, no como una colección informal de hojas",
                "entities": "cada relación representa un predicado; sus filas afirman hechos y sus claves identifican hechos o entidades sin depender del orden físico",
                "mechanism": "claves candidatas, primaria y foráneas permiten identificar tuplas y conectar relaciones manteniendo integridad referencial",
                "decision": "la clave primaria se selecciona por estabilidad, minimalidad y disponibilidad, no por conveniencia visual",
                "risk": "usar posiciones, nombres mutables o combinaciones no únicas como identificadores",
                "biomedical": "un identificador interno evita exponer identificadores directos y permite separar identidad operativa de claves analíticas",
                "validation": "buscar duplicados, valores nulos indebidos y referencias huérfanas antes de declarar una clave",
                "equation": {"latex": "K \rightarrow R", "description": "Una clave candidata K determina funcionalmente todos los atributos de la relación R."},
            },
            {
                "heading": "Dependencias funcionales y cierres",
                "core": "expresar qué atributos determinan a otros para razonar sobre redundancia, claves y descomposición",
                "entities": "determinantes, atributos dependientes, dependencias triviales, parciales y transitivas describen reglas del dominio",
                "mechanism": "el cierre de un conjunto de atributos se calcula aplicando dependencias hasta que no aparecen atributos nuevos",
                "decision": "una dependencia solo se acepta si es verdadera para todos los estados válidos del dominio y no por coincidencia en una muestra pequeña",
                "risk": "inferir reglas desde datos actuales, confundir correlación con determinación y omitir condiciones temporales",
                "biomedical": "el código de una prueba puede determinar analito y unidad esperada dentro de una versión concreta del catálogo, pero no necesariamente entre versiones",
                "validation": "documentar el alcance de cada dependencia y probar contra contraejemplos sintéticos",
                "equation": {"latex": "X^{+}_{F}=\{A\mid F\models X\rightarrow A\}", "description": "El cierre X+ reúne los atributos implicados por X bajo el conjunto F de dependencias."},
            },
            {
                "heading": "Formas normales y anomalías",
                "core": "reducir redundancia y anomalías de inserción, actualización y borrado mediante descomposiciones justificadas",
                "entities": "primera, segunda, tercera forma normal y BCNF establecen condiciones progresivas sobre claves y dependencias",
                "mechanism": "se identifican dependencias problemáticas y se descompone la relación preservando hechos en tablas con responsabilidades claras",
                "decision": "la forma objetivo depende de las dependencias reales, el coste de consulta y la necesidad de preservar reglas",
                "risk": "normalizar por ritual, crear tablas sin significado o desnormalizar sin controles de consistencia",
                "biomedical": "separar catálogo de pruebas, solicitudes y resultados evita modificar miles de filas al actualizar una descripción",
                "validation": "demostrar unión sin pérdida y evaluar si las dependencias necesarias pueden imponerse sin reconstrucciones costosas",
                "equation": {"latex": "R_1 \bowtie R_2 = R", "description": "Una descomposición sin pérdida permite reconstruir exactamente la relación válida original."},
            },
            {
                "heading": "Descomposición, integración y decisiones de diseño",
                "core": "equilibrar normalización, legibilidad, rendimiento y mantenimiento mediante decisiones explícitas y medibles",
                "entities": "tablas base, vistas, dimensiones, hechos y materializaciones cumplen funciones diferentes dentro de una arquitectura",
                "mechanism": "el esquema normalizado conserva la fuente de verdad y las vistas o tablas derivadas ofrecen formas de consumo controladas",
                "decision": "desnormalizar solo después de medir una carga concreta, definir sincronización y mantener pruebas de equivalencia",
                "risk": "copias divergentes, columnas derivadas sin fórmula y dependencias ocultas en procesos manuales",
                "biomedical": "una vista de cohorte puede reunir persona, visita y resultado sin convertir esa combinación en la fuente primaria",
                "validation": "comparar conteos, claves y agregados entre tablas base y productos derivados después de cada cambio",
                "equation": {"latex": "\text{redundancia controlada} \neq \text{duplicación sin gobierno}", "description": "La desnormalización requiere propósito, sincronización y validación explícitos."},
            },
        ],
        "glossary": [
            ["Relación", "Conjunto de tuplas sobre atributos definidos."], ["Tupla", "Registro lógico perteneciente a una relación."],
            ["Clave candidata", "Conjunto mínimo de atributos que identifica una tupla."], ["Clave primaria", "Clave candidata elegida como identificador principal."],
            ["Clave foránea", "Atributo que referencia una clave de otra relación."], ["Dependencia funcional", "Regla por la que un conjunto de atributos determina otro."],
            ["Cierre", "Conjunto de atributos deducibles mediante dependencias."], ["Anomalía de actualización", "Inconsistencia causada por repetir el mismo hecho."],
            ["Primera forma normal", "Condición de atributos atómicos dentro del modelo adoptado."], ["Tercera forma normal", "Forma que limita dependencias transitivas no justificadas."],
            ["BCNF", "Forma normal donde todo determinante no trivial es superclave."], ["Unión sin pérdida", "Propiedad que permite reconstruir exactamente la relación original."],
        ],
        "examples": [
            ["Normalización de resultados longitudinales", "Una tabla repite nombre de prueba, unidad y rango por cada resultado.", "Identificar dependencias, separar catálogo de pruebas y conservar en resultados la clave del catálogo y el valor observado.", "Las descripciones se actualizan una vez y cada resultado mantiene su identidad y tiempo.", "Los intervalos de referencia pueden depender de método, población y versión; requieren modelado adicional."],
            ["Evaluación de una descomposición", "Se propone separar solicitud, muestra y resultado para eliminar nulos.", "Calcular claves, revisar dependencias, verificar intersecciones y ensayar la unión con datos adversariales.", "La descomposición es aceptable cuando no genera tuplas espurias y preserva reglas críticas.", "La prueba con pocos datos no sustituye la demostración estructural."],
        ],
        "sources": [
            ["PostgreSQL — Constraints", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/ddl-constraints.html"],
            ["Database Design — Normalization", "BCcampus", "https://opentextbc.ca/dbdesign01/chapter/chapter-12-normalization/"],
            ["SQLite — Foreign Keys", "SQLite Consortium", "https://www.sqlite.org/foreignkeys.html"],
            ["The Relational Model for Database Management", "Association for Computing Machinery", "https://doi.org/10.1145/362384.362685"],
            ["PostgreSQL — Views", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/sql-createview.html"],
            ["OMOP Common Data Model", "OHDSI", "https://ohdsi.github.io/CommonDataModel/"],
        ],
    },
    {
        "unit": 3,
        "slug": "sql-para-consulta-y-analisis",
        "title": "SQL para consulta y análisis",
        "weeks": [6, 7, 8],
        "hours": 24,
        "purpose": "Escribir consultas SQL correctas, legibles y comprobables para seleccionar, combinar, resumir y auditar datos biomédicos estructurados.",
        "artifact": "colección reproducible de consultas para una cohorte longitudinal sintética",
        "sections": [
            {
                "heading": "Modelo declarativo y orden lógico de una consulta",
                "core": "formular qué conjunto de resultados se necesita sin confundir el orden textual de SQL con su orden lógico de evaluación",
                "entities": "FROM, JOIN, WHERE, GROUP BY, HAVING, SELECT y ORDER BY transforman progresivamente una relación lógica",
                "mechanism": "la consulta construye primero fuentes y uniones, filtra filas, forma grupos, filtra grupos, proyecta expresiones y ordena al final",
                "decision": "cada cláusula debe responder una pregunta concreta y los alias deben hacer visible la procedencia de las columnas",
                "risk": "filtrar demasiado tarde, usar alias fuera de alcance y depender de un orden no declarado",
                "biomedical": "una cohorte reproducible requiere expresar explícitamente periodo, evento índice, criterios de inclusión y unidad de observación",
                "validation": "inspeccionar resultados intermedios y construir casos pequeños con salida conocida",
                "equation": {"latex": "Q = \pi_{columnas}(\sigma_{criterios}(R))", "description": "Una consulta simple puede interpretarse como selección seguida de proyección."},
            },
            {
                "heading": "NULL, lógica ternaria y comparaciones",
                "core": "tratar la ausencia o desconocimiento mediante la lógica de tres valores de SQL en lugar de equipararla con cero o cadena vacía",
                "entities": "TRUE, FALSE y UNKNOWN gobiernan comparaciones, filtros, restricciones y agregados cuando interviene NULL",
                "mechanism": "las comparaciones ordinarias con NULL producen UNKNOWN; IS NULL, COALESCE y expresiones CASE modelan decisiones explícitas",
                "decision": "la estrategia depende de si el dato es desconocido, no aplicable, no medido o suprimido; estos estados pueden requerir códigos separados",
                "risk": "usar = NULL, rellenar ausencias sin justificación o contar columnas nulas como observaciones completas",
                "biomedical": "no medir una prueba es diferente de obtener un resultado negativo y debe conservarse en el análisis",
                "validation": "añadir casos con NULL a cada prueba y verificar denominadores de COUNT, AVG y filtros",
                "equation": {"latex": "x = NULL \Rightarrow UNKNOWN", "description": "En SQL, la igualdad ordinaria no determina si un valor es nulo."},
            },
            {
                "heading": "JOIN, agregación y cardinalidad",
                "core": "combinar relaciones sin multiplicar hechos accidentalmente y resumir datos con denominadores explícitos",
                "entities": "INNER, LEFT, semiuniones conceptuales, claves y niveles de granularidad controlan qué filas sobreviven y cuántas aparecen",
                "mechanism": "cada coincidencia produce una combinación; las agregaciones reducen conjuntos mediante funciones y grupos definidos",
                "decision": "antes de unir se declara la cardinalidad esperada y se decide si se necesita una fila por persona, visita, muestra o resultado",
                "risk": "uniones muchos-a-muchos involuntarias, COUNT(*) engañoso y filtros en WHERE que convierten LEFT JOIN en INNER JOIN",
                "biomedical": "unir diagnósticos y medicamentos por persona puede crear productos cartesianos si no se alinea el tiempo o el episodio",
                "validation": "comparar conteos antes y después, probar unicidad de claves y revisar entidades con cero, una y múltiples coincidencias",
                "equation": {"latex": "\lvert R \bowtie S \rvert \leq \lvert R \rvert\,\lvert S \rvert", "description": "El límite recuerda que una unión puede multiplicar filas drásticamente."},
            },
            {
                "heading": "CTE, ventanas, vistas y pruebas de consultas",
                "core": "organizar análisis complejos en etapas nombradas, preservar filas con funciones de ventana y encapsular contratos mediante vistas",
                "entities": "CTE, particiones, marcos de ventana, vistas y consultas de control separan transformación, cálculo y presentación",
                "mechanism": "las ventanas calculan rankings, acumulados o valores previos sin colapsar filas; las CTE hacen visibles pasos lógicos",
                "decision": "se elige una CTE para claridad, una vista para reutilización y una materialización solo cuando la medición justifica su coste de mantenimiento",
                "risk": "consultas monolíticas, ventanas sin orden total y vistas que ocultan filtros críticos",
                "biomedical": "LAG puede calcular el cambio entre mediciones consecutivas, siempre que el orden temporal y los empates estén definidos",
                "validation": "crear oráculos manuales, propiedades de conservación y pruebas de regresión para cada consulta publicada",
                "equation": {"latex": "\Delta x_i = x_i - LAG(x_i)", "description": "Una función de ventana permite calcular cambios longitudinales manteniendo cada observación."},
            },
        ],
        "glossary": [
            ["Consulta declarativa", "Expresión del resultado deseado sin fijar un algoritmo físico."], ["Proyección", "Selección de columnas o expresiones de salida."],
            ["Selección", "Filtrado de filas mediante un predicado."], ["NULL", "Marcador SQL de valor ausente o desconocido."],
            ["Lógica ternaria", "Lógica con TRUE, FALSE y UNKNOWN."], ["JOIN", "Operación que combina filas relacionadas."],
            ["Granularidad", "Nivel de detalle representado por cada fila."], ["Agregación", "Reducción de un conjunto a estadísticas por grupo."],
            ["CTE", "Expresión de tabla común que nombra una etapa de consulta."], ["Función de ventana", "Cálculo sobre filas relacionadas sin colapsarlas."],
            ["Vista", "Consulta almacenada que presenta una relación virtual."], ["Oráculo", "Resultado o propiedad usada para comprobar una consulta."],
        ],
        "examples": [
            ["Cohorte con evento índice", "Se requieren personas ficticias con una prueba concreta durante 2025 y al menos seis meses de seguimiento.", "Definir evento índice por persona, filtrar periodo, calcular seguimiento y evitar duplicados con una etapa de ranking.", "La consulta devuelve una fila por persona con fechas y criterios auditables.", "No valida la pertinencia clínica de la definición de cohorte."],
            ["Cambio entre resultados consecutivos", "Se necesita calcular la diferencia temporal y numérica entre mediciones del mismo analito.", "Particionar por persona y analito, ordenar por fecha e identificador, usar LAG y conservar la primera observación con diferencia nula.", "Cada fila mantiene su resultado y añade contexto longitudinal.", "Los intervalos irregulares y cambios de método requieren análisis adicional."],
        ],
        "sources": [
            ["PostgreSQL — SELECT", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/sql-select.html"],
            ["PostgreSQL — Window Functions", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/tutorial-window.html"],
            ["PostgreSQL — Aggregate Functions", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/functions-aggregate.html"],
            ["PostgreSQL — Using EXPLAIN", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/using-explain.html"],
            ["SQLite — SELECT", "SQLite Consortium", "https://www.sqlite.org/lang_select.html"],
            ["OMOP CDM SQL Resources", "OHDSI", "https://ohdsi.github.io/CommonDataModel/"],
        ],
    },
    {
        "unit": 4,
        "slug": "transacciones-y-concurrencia",
        "title": "Transacciones y concurrencia",
        "weeks": [9, 10, 11],
        "hours": 24,
        "purpose": "Razonar sobre atomicidad, aislamiento, bloqueos, MVCC y recuperación para mantener datos coherentes bajo fallos y operaciones concurrentes.",
        "artifact": "prototipo transaccional de recepción, procesamiento y corrección de muestras sintéticas",
        "sections": [
            {
                "heading": "ACID y límites de una transacción",
                "core": "agrupar operaciones que representan un único cambio lógico y definir qué debe ocurrir completamente o no ocurrir",
                "entities": "atomicidad, consistencia, aislamiento y durabilidad describen propiedades distintas que cooperan pero no sustituyen reglas del dominio",
                "mechanism": "BEGIN delimita trabajo, COMMIT publica cambios y ROLLBACK restaura el estado previo ante error",
                "decision": "el límite transaccional debe corresponder a una invariancia del negocio y mantenerse suficientemente corto",
                "risk": "transacciones parciales, confirmaciones prematuras y trabajo externo irreversible dentro de una transacción larga",
                "biomedical": "registrar una muestra y sus identificadores asociados debe evitar estados donde la muestra exista sin trazabilidad mínima",
                "validation": "inyectar fallos en cada paso y comprobar que solo existen estados completos permitidos",
                "equation": {"latex": "T: S_{válido} \rightarrow S_{válido}", "description": "Una transacción correcta transforma un estado válido en otro estado válido."},
            },
            {
                "heading": "Anomalías y niveles de aislamiento",
                "core": "comprender cómo lecturas y escrituras concurrentes producen fenómenos que no aparecen en ejecuciones secuenciales",
                "entities": "lectura sucia, lectura no repetible, fantasma, actualización perdida y write skew representan patrones diferentes",
                "mechanism": "cada nivel de aislamiento restringe historias permitidas, mientras la implementación usa bloqueos, versiones o validación",
                "decision": "el nivel se selecciona a partir de invariantes concretas y no solo por una etiqueta de rendimiento",
                "risk": "suponer que READ COMMITTED serializa decisiones o que evitar lecturas sucias impide actualizaciones perdidas",
                "biomedical": "dos procesos que asignan simultáneamente la última alícuota disponible pueden violar una regla aunque cada consulta aislada sea correcta",
                "validation": "ejecutar pruebas concurrentes coordinadas que reproduzcan historias adversariales y verifiquen el estado final",
                "equation": {"latex": "H \equiv H_s", "description": "La serializabilidad exige que la historia concurrente H sea equivalente a alguna historia serial Hs."},
            },
            {
                "heading": "Bloqueos, MVCC y deadlocks",
                "core": "analizar cómo el motor coordina acceso concurrente mediante bloqueos y múltiples versiones de filas",
                "entities": "bloqueos compartidos, exclusivos, de fila y tabla; instantáneas; versiones; esperas y ciclos de dependencia",
                "mechanism": "MVCC permite que lectores observen una instantánea mientras escritores crean nuevas versiones; los bloqueos protegen conflictos no resueltos por visibilidad",
                "decision": "se bloquea el recurso mínimo suficiente y se accede a recursos en orden estable para reducir contención",
                "risk": "transacciones inactivas, bloqueos amplios, reintentos no idempotentes y deadlocks ignorados",
                "biomedical": "procesadores paralelos de eventos deben reservar trabajo sin duplicar el procesamiento ni mantener bloqueos durante tareas lentas",
                "validation": "medir espera, abortos, duración y consistencia bajo cargas repetibles, no solo tiempo promedio",
                "equation": {"latex": "G_{espera}\text{ contiene ciclo} \Rightarrow \text{deadlock}", "description": "Un ciclo en el grafo de espera indica interbloqueo."},
            },
            {
                "heading": "WAL, recuperación, idempotencia y mensajería",
                "core": "preservar cambios confirmados y coordinar base de datos con procesos externos frente a fallos parciales",
                "entities": "write-ahead log, checkpoints, copias de seguridad, reintentos, claves idempotentes y patrón outbox",
                "mechanism": "el WAL registra intención antes de modificar páginas; la recuperación reproduce o revierte operaciones según su estado",
                "decision": "las operaciones susceptibles de reintento deben diseñarse para producir el mismo estado una o varias veces",
                "risk": "enviar mensajes antes del commit, asumir exactamente una entrega y confundir replicación con copia de seguridad",
                "biomedical": "una notificación de resultado sintético debe corresponder a un registro confirmado y no duplicarse tras una interrupción",
                "validation": "simular caída, restauración y repetición de mensajes, y documentar objetivos RPO y RTO del ejercicio",
                "equation": {"latex": "f(f(x)) = f(x)", "description": "Una operación idempotente conserva el mismo resultado al repetirse."},
            },
        ],
        "glossary": [
            ["Transacción", "Unidad lógica de trabajo confirmada o revertida en conjunto."], ["Atomicidad", "Propiedad de todo o nada."],
            ["Aislamiento", "Control de los efectos visibles entre transacciones concurrentes."], ["Durabilidad", "Persistencia de cambios confirmados frente a fallos."],
            ["Serializabilidad", "Equivalencia con alguna ejecución serial."], ["MVCC", "Control de concurrencia mediante múltiples versiones."],
            ["Bloqueo", "Mecanismo que restringe acceso incompatible a un recurso."], ["Deadlock", "Ciclo de espera que impide progreso."],
            ["WAL", "Registro escrito antes de aplicar cambios a páginas de datos."], ["Checkpoint", "Punto que limita trabajo necesario durante recuperación."],
            ["Idempotencia", "Propiedad de repetir una operación sin alterar el resultado final."], ["Outbox", "Patrón que registra cambios y mensajes en una misma transacción."],
        ],
        "examples": [
            ["Reserva concurrente de una alícuota", "Dos procesos intentan reservar la misma alícuota disponible.", "Reproducir actualización perdida, elegir bloqueo o actualización condicional y comprobar filas afectadas.", "Solo una reserva se confirma y el segundo proceso recibe un resultado controlado.", "El ejemplo no representa un sistema real de laboratorio."],
            ["Publicación transaccional de un evento", "Un proceso guarda un resultado y debe emitir un evento para otro servicio.", "Insertar resultado y registro outbox en una transacción; publicar después y marcar de forma idempotente.", "Un fallo entre commit y publicación no pierde el evento ni duplica el efecto final.", "La entrega y seguridad de mensajería requieren arquitectura adicional."],
        ],
        "sources": [
            ["PostgreSQL — Transaction Isolation", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/transaction-iso.html"],
            ["PostgreSQL — Explicit Locking", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/explicit-locking.html"],
            ["PostgreSQL — Concurrency Control", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/mvcc.html"],
            ["PostgreSQL — WAL", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/wal.html"],
            ["SQLite — Isolation", "SQLite Consortium", "https://www.sqlite.org/isolation.html"],
            ["PostgreSQL — Backup and Restore", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/backup.html"],
        ],
    },
    {
        "unit": 5,
        "slug": "indices-seguridad-y-rendimiento",
        "title": "Índices, seguridad y rendimiento",
        "weeks": [12, 13],
        "hours": 16,
        "purpose": "Seleccionar índices, interpretar planes, medir cargas y aplicar controles de seguridad sin sacrificar integridad ni trazabilidad.",
        "artifact": "informe reproducible de optimización y control de acceso sobre una base biomédica sintética",
        "sections": [
            {
                "heading": "Índices, selectividad y patrones de acceso",
                "core": "entender un índice como estructura auxiliar que acelera operaciones específicas a cambio de espacio y coste de mantenimiento",
                "entities": "B-tree, índices compuestos, parciales y de cobertura responden a predicados, órdenes y proyecciones diferentes",
                "mechanism": "el índice organiza claves para reducir páginas examinadas; su utilidad depende de selectividad, correlación y distribución",
                "decision": "se diseña desde consultas reales y se ordenan columnas según igualdad, rango, ordenación y reutilización",
                "risk": "indexar cada columna, ignorar escrituras o creer que cualquier índice obliga al optimizador a usarlo",
                "biomedical": "consultas por persona, analito y tiempo pueden beneficiarse de un índice compuesto alineado con ese patrón",
                "validation": "comparar planes y tiempos con datos de escala y distribución representativas, incluyendo caché fría y caliente",
                "equation": {"latex": "s = \frac{\text{filas seleccionadas}}{\text{filas totales}}", "description": "La selectividad s ayuda a estimar si un acceso indexado puede reducir trabajo."},
            },
            {
                "heading": "Optimizador, estadísticas y planes de ejecución",
                "core": "interpretar el plan como una hipótesis de ejecución basada en estimaciones, no como garantía abstracta de rendimiento",
                "entities": "escaneos, joins, ordenamientos, agregaciones, costes, filas estimadas y filas reales forman el lenguaje del plan",
                "mechanism": "el optimizador compara alternativas utilizando estadísticas de distribución, selectividad y coste del sistema",
                "decision": "antes de reescribir SQL se localiza la mayor discrepancia entre estimaciones y observaciones y se identifica su causa",
                "risk": "optimizar por intuición, comparar tiempos únicos y ocultar filtros dentro de funciones no indexables",
                "biomedical": "distribuciones muy sesgadas por analito o centro pueden invalidar estimaciones basadas en promedios",
                "validation": "usar EXPLAIN ANALYZE con precaución, registrar versión, parámetros, datos y variabilidad entre repeticiones",
                "equation": {"latex": "E = \frac{\text{filas reales}}{\max(1,\text{filas estimadas})}", "description": "Una razón E extrema señala problemas de estimación que pueden cambiar el plan."},
            },
            {
                "heading": "Benchmarks, capacidad y regresión",
                "core": "medir rendimiento mediante experimentos controlados que separen complejidad, constantes, caché, concurrencia y entorno",
                "entities": "latencia, throughput, percentiles, utilización, tamaño de datos y tasa de errores describen dimensiones distintas",
                "mechanism": "un benchmark define carga, calentamiento, repeticiones, estado inicial y estadísticos antes de ejecutar",
                "decision": "la métrica principal se elige según el objetivo operativo y se acompaña de límites de recursos y precisión",
                "risk": "usar promedios sin dispersión, datos diminutos o resultados de una máquina como verdad universal",
                "biomedical": "una consulta de cohorte puede ser rápida en una muestra y degradarse al incorporar longitudinalidad y múltiples centros",
                "validation": "guardar scripts, semillas, planes y resultados para detectar regresiones después de cambios",
                "equation": {"latex": "\text{throughput}=\frac{\text{operaciones completadas}}{\Delta t}", "description": "El throughput debe interpretarse junto con latencia y tasa de errores."},
            },
            {
                "heading": "Seguridad, privilegios, pseudonimización y respaldo",
                "core": "aplicar defensa en profundidad y mínimo privilegio, diferenciando confidencialidad, integridad, disponibilidad y privacidad",
                "entities": "roles, esquemas, vistas, seguridad por fila, cifrado, auditoría, pseudónimos, copias y restauración cubren capas distintas",
                "mechanism": "los permisos se conceden a roles según función; los identificadores directos se separan y los accesos quedan registrados",
                "decision": "cada control se vincula con una amenaza y se prueba sin asumir que cifrado o pseudonimización eliminan todo riesgo",
                "risk": "cuentas compartidas, privilegios acumulados, copias no probadas y publicación de datos reidentificables",
                "biomedical": "los ejercicios usan datos ficticios; cualquier tratamiento de datos reales exige gobierno, base legal y revisión institucional",
                "validation": "probar denegaciones, restaurar copias, revisar privilegios efectivos y documentar RPO, RTO y límites de anonimización",
                "equation": {"latex": "\text{riesgo}=\text{probabilidad}\times\text{impacto}", "description": "La priorización de controles considera probabilidad e impacto, sin convertir la fórmula en una medida exacta."},
            },
        ],
        "glossary": [
            ["Índice", "Estructura auxiliar para acelerar patrones de acceso."], ["Selectividad", "Fracción de filas que satisface un predicado."],
            ["Índice compuesto", "Índice definido sobre varias columnas ordenadas."], ["Plan de ejecución", "Estrategia física elegida para una consulta."],
            ["Estadística", "Resumen usado por el optimizador para estimar cardinalidades."], ["Latencia", "Tiempo requerido por una operación."],
            ["Throughput", "Número de operaciones completadas por unidad de tiempo."], ["Percentil", "Valor por debajo del cual cae una proporción de observaciones."],
            ["Mínimo privilegio", "Concesión exclusiva de permisos necesarios."], ["Pseudonimización", "Sustitución controlada de identificadores directos."],
            ["RPO", "Pérdida máxima de datos tolerada medida en tiempo."], ["RTO", "Tiempo objetivo para restaurar un servicio."],
        ],
        "examples": [
            ["Optimización de una consulta longitudinal", "Una consulta filtra por analito, persona y periodo y ordena resultados por tiempo.", "Capturar plan base, medir distribución, crear índice compuesto justificado y repetir el benchmark.", "El plan reduce páginas y latencia bajo la carga estudiada sin afirmar mejora universal.", "El índice añade coste de almacenamiento y escritura."],
            ["Diseño de acceso por roles", "Investigación, operación y auditoría requieren vistas distintas de datos ficticios.", "Definir roles, revocar permisos implícitos, crear vistas limitadas y probar accesos permitidos y denegados.", "Cada función recibe solo datos y operaciones necesarios.", "No sustituye una evaluación legal ni de seguridad institucional."],
        ],
        "sources": [
            ["PostgreSQL — Indexes", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/indexes.html"],
            ["PostgreSQL — Using EXPLAIN", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/using-explain.html"],
            ["PostgreSQL — Planner Statistics", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/planner-stats.html"],
            ["PostgreSQL — Database Roles", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/user-manag.html"],
            ["PostgreSQL — Row Security", "PostgreSQL Global Development Group", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html"],
            ["NIST Privacy Framework", "National Institute of Standards and Technology", "https://www.nist.gov/privacy-framework"],
        ],
    },
    {
        "unit": 6,
        "slug": "datos-biomedicos-heterogeneos",
        "title": "Datos biomédicos heterogéneos",
        "weeks": [14, 15, 16],
        "hours": 24,
        "purpose": "Integrar datos clínicos, ómicos, de imagen y laboratorio mediante contratos, estándares, procedencia y controles de calidad que preserven significado y tiempo.",
        "artifact": "pipeline reproducible que integra recursos FHIR, tablas OMOP y metadatos DICOM sintéticos",
        "sections": [
            {
                "heading": "Heterogeneidad estructural, semántica y temporal",
                "core": "distinguir diferencias de formato, significado, escala, granularidad y tiempo antes de combinar fuentes",
                "entities": "tablas, JSON, mensajes, imágenes, vocabularios, unidades, eventos y versiones representan capas heterogéneas",
                "mechanism": "la integración perfila cada fuente, declara contratos y transforma hacia un modelo común sin perder el original",
                "decision": "se decide qué armonizar, qué conservar como fuente y qué incertidumbre no puede resolverse automáticamente",
                "risk": "alinear columnas por nombre, convertir unidades sin contexto o mezclar eventos futuros con información disponible en el índice",
                "biomedical": "un código local de laboratorio puede parecer equivalente a un concepto estándar y aun diferir en método o muestra",
                "validation": "comparar distribuciones, unidades, tiempos y vocabularios antes y después de cada mapeo",
                "equation": {"latex": "D_{integrado}=T_1(D_1)\cup\cdots\cup T_n(D_n)", "description": "Cada transformación Ti debe ser explícita, versionada y reversible cuando sea posible."},
            },
            {
                "heading": "FHIR, OMOP, DICOM y modelos complementarios",
                "core": "comprender que los estándares responden a finalidades diferentes y no son sustitutos intercambiables",
                "entities": "FHIR organiza intercambio mediante recursos, OMOP estructura análisis observacional y DICOM representa objetos e información de imagen médica",
                "mechanism": "perfiles, vocabularios, identificadores y relaciones convierten datos locales en representaciones interoperables",
                "decision": "el estándar se elige según intercambio, análisis, archivo o investigación, y se documentan pérdidas durante la conversión",
                "risk": "reducir interoperabilidad a sintaxis, ignorar perfiles locales y asumir equivalencia semántica por compartir un código",
                "biomedical": "una observación FHIR puede mapearse a OMOP para análisis, pero el proceso necesita reglas para persona, visita, concepto, unidad y procedencia",
                "validation": "usar ejemplos oficiales, validadores, tablas de correspondencia y revisión de especialistas del dominio",
                "equation": {"latex": "\text{interoperabilidad}=\text{sintaxis}+\text{semántica}+\text{contexto}", "description": "Compartir formato no garantiza interpretación equivalente."},
            },
            {
                "heading": "ETL, ELT, contratos y procedencia",
                "core": "diseñar pipelines repetibles que separen extracción, conservación cruda, transformación, carga y productos analíticos",
                "entities": "fuentes, zonas crudas, tablas intermedias, modelos finales, contratos, versiones y registros de ejecución forman el linaje",
                "mechanism": "cada ejecución identifica entradas, código, parámetros, ambiente, salidas y métricas de calidad",
                "decision": "ETL o ELT se selecciona por gobernanza, volumen, capacidades del motor y necesidad de conservar evidencia original",
                "risk": "transformaciones manuales, sobrescritura de fuentes y pipelines que no pueden reanudarse ni reproducirse",
                "biomedical": "los datos identificables deben permanecer fuera del ejercicio educativo; los ejemplos usan identificadores ficticios y reglas transparentes",
                "validation": "ejecutar dos veces, comparar hashes y conteos, probar reanudación y reconstruir el linaje de una fila seleccionada",
                "equation": {"latex": "\text{salida}=f(\text{entrada},\text{código},\text{parámetros},\text{versión})", "description": "La reproducibilidad exige registrar todos los componentes de la transformación."},
            },
            {
                "heading": "Calidad, leakage y validación de productos integrados",
                "core": "evaluar completitud, validez, consistencia, unicidad, plausibilidad temporal y representatividad en cada etapa",
                "entities": "reglas, métricas, umbrales, cuarentena, informes, subgrupos y conjuntos de referencia convierten calidad en evidencia revisable",
                "mechanism": "las pruebas detectan valores, relaciones y secuencias imposibles; los registros fallidos se conservan con motivo",
                "decision": "un umbral se establece según uso previsto y coste del error, sin ocultar variación entre centros o periodos",
                "risk": "filtrar silenciosamente, usar información posterior al evento índice y confundir ausencia de error técnico con validez científica",
                "biomedical": "el leakage temporal puede inflar modelos predictivos cuando una variable registrada después del desenlace entra como predictor",
                "validation": "separar periodos, centros y subgrupos; revisar procedencia; comparar contra casos conocidos y documentar limitaciones",
                "equation": {"latex": "\text{completitud}=\frac{\text{valores presentes esperados}}{\text{valores esperados}}", "description": "La completitud requiere definir primero qué valores se esperaban en ese contexto."},
            },
        ],
        "glossary": [
            ["Heterogeneidad", "Diferencias estructurales, semánticas, temporales o técnicas entre fuentes."], ["Interoperabilidad", "Capacidad de intercambiar e interpretar datos de forma coherente."],
            ["FHIR", "Estándar HL7 basado en recursos para intercambio de información sanitaria."], ["OMOP CDM", "Modelo común de datos orientado a análisis observacional."],
            ["DICOM", "Estándar para objetos, metadatos y comunicación de imagen médica."], ["ETL", "Extracción, transformación y carga."],
            ["ELT", "Extracción, carga y transformación posterior."], ["Contrato de datos", "Especificación versionada de estructura, significado y calidad esperada."],
            ["Linaje", "Rastro de fuentes y transformaciones que originaron un dato."], ["Armonización", "Proceso de hacer comparables representaciones heterogéneas."],
            ["Leakage temporal", "Uso de información no disponible en el momento de predicción."], ["Cuarentena", "Separación de registros que no superan controles para su revisión."],
        ],
        "examples": [
            ["Mapeo FHIR a OMOP", "Recursos sintéticos Patient, Encounter y Observation deben transformarse a tablas analíticas.", "Definir correspondencias, resolver identificadores, conceptos, unidades y fechas, y conservar referencias al recurso fuente.", "El producto OMOP permite consultas de cohorte sin perder el linaje del mapeo.", "Un mapeo real requiere perfiles locales, vocabularios y validación institucional."],
            ["Detección de leakage temporal", "Una tabla de entrenamiento contiene variables registradas antes y después del evento índice.", "Calcular disponibilidad temporal, excluir variables posteriores, crear pruebas y comparar rendimiento del pipeline.", "La diferencia revela cuánto dependía el resultado de información no disponible prospectivamente.", "No demuestra utilidad clínica del modelo restante."],
        ],
        "sources": [
            ["FHIR Specification", "HL7 International", "https://hl7.org/fhir/"],
            ["OMOP Common Data Model", "OHDSI", "https://ohdsi.github.io/CommonDataModel/"],
            ["DICOM Standard", "DICOM Standards Committee", "https://www.dicomstandard.org/current"],
            ["PROV-O", "W3C", "https://www.w3.org/TR/prov-o/"],
            ["GA4GH Data Use Ontology", "Global Alliance for Genomics and Health", "https://github.com/EBISPOT/DUO"],
            ["CDISC Standards", "Clinical Data Interchange Standards Consortium", "https://www.cdisc.org/standards"],
        ],
    },
]


def theory_paragraphs(unit: dict[str, Any], section: dict[str, Any]) -> list[str]:
    heading = section["heading"]
    return [
        (
            f"El núcleo de {heading.lower()} es {section['core']}. En una base de datos científica, una estructura no es correcta solo porque permite guardar filas: debe representar con precisión qué existe, qué ocurrió, qué se observó y bajo qué condiciones. {section['entities']}. Esta separación evita que una conveniencia del software se convierta en una afirmación biológica falsa. El modelo funciona como un contrato entre quienes producen datos, quienes mantienen el sistema y quienes analizan resultados. Por ello, cada término debe tener una definición operacional, un alcance temporal y un nivel de granularidad. Cuando estos elementos quedan implícitos, dos consultas sintácticamente válidas pueden responder preguntas diferentes. La práctica recomendada consiste en escribir primero ejemplos positivos y negativos, declarar la unidad de observación y justificar cada relación antes de implementar el esquema. Los datos son mapas del proceso observado, no la realidad completa; la claridad estructural permite conocer qué parte del territorio quedó representada y cuál permanece fuera del modelo."
        ),
        (
            f"El mecanismo de trabajo puede resumirse así: {section['mechanism']}. Esta operación debe traducirse en tipos, claves, restricciones, transformaciones o consultas observables. La expresión {section['equation']['latex']} resume una relación útil: {section['equation']['description']} Sin embargo, una fórmula o regla aislada no sustituye el análisis del dominio. Deben especificarse supuestos, condiciones de aplicación y comportamiento ante entradas vacías, duplicadas, tardías o contradictorias. En sistemas biomédicos, la misma etiqueta puede ocultar métodos, unidades o momentos distintos; por eso la semántica debe acompañar a la estructura. También debe distinguirse una regla universal de una convención local o de una regularidad provisional encontrada en los datos. La implementación se prueba con instancias pequeñas calculables manualmente y con conjuntos adversariales que activen cada rama relevante. Esta combinación de razonamiento formal y experimentación controlada convierte el diseño en una hipótesis verificable, no en una colección de decisiones estéticas."
        ),
        (
            f"La decisión principal en esta sección es que {section['decision']}. No existe una estructura óptima con independencia de las operaciones dominantes, el volumen, la frecuencia de actualización y la necesidad de auditoría. Una solución puede acelerar una consulta y, al mismo tiempo, aumentar escrituras, complejidad o riesgo de divergencia. El análisis debe separar corrección, rendimiento y mantenibilidad: primero se garantiza que el resultado expresa la pregunta correcta; después se mide su coste; finalmente se decide si la complejidad adicional está justificada. Deben registrarse alternativas descartadas y criterios de elección para que otra persona pueda revisar el razonamiento. El diseño también debe anticipar evolución: nuevos centros, versiones de catálogos, periodos más largos o fuentes con diferente calidad pueden invalidar supuestos iniciales. Una base de datos robusta no elimina el cambio, sino que hace visibles sus efectos mediante contratos, migraciones y pruebas de regresión. La optimización prematura suele ocultar problemas de identidad o significado que ningún índice puede corregir posteriormente."
        ),
        (
            f"El riesgo característico es {section['risk']}. Para reducirlo, {section['validation']}. La validación no debe limitarse a ejecutar una consulta sin errores: incluye comparar conteos, revisar claves, inspeccionar casos extremos, comprobar unidades, reconstruir procedencia y confirmar que los filtros preservan el denominador esperado. Las reglas críticas deben convertirse en pruebas automáticas y también en informes comprensibles para revisión humana. Cuando un registro falla, conviene conservarlo en cuarentena con el motivo, en lugar de eliminarlo silenciosamente y alterar la población analizada. Los resultados de calidad deben desagregarse por fuente, periodo y subgrupo, porque un promedio global puede ocultar fallos sistemáticos. La evidencia debe incluir versión del esquema, código, parámetros y datos de prueba. De este modo, un cambio posterior puede evaluarse contra una línea base y no mediante impresiones. Predecir o consultar no basta; hay que validar que la representación, el proceso y la salida mantienen el significado pretendido."
        ),
        (
            f"En el caso biomédico de esta unidad, {section['biomedical']}. El objetivo educativo es aprender a preservar contexto y trazabilidad, no convertir un prototipo en sistema asistencial. Los ejemplos utilizan personas, muestras y resultados ficticios, sin identificadores reales ni recomendaciones médicas. Incluso con datos sintéticos, el estudiante debe documentar procedencia, supuestos y limitaciones, porque esos hábitos determinan la reproducibilidad posterior. Una conexión biomédica útil no consiste en añadir terminología clínica a una consulta genérica: debe cambiar el modelo, las restricciones o la interpretación. El producto final de la sección debe poder ser revisado por otra persona que no participó en su construcción. Esa revisión debe distinguir qué está respaldado por el esquema, qué depende de una regla local y qué requiere conocimiento experto adicional. El sistema conserva evidencia suficiente para repetir el análisis, explicar exclusiones y corregir errores sin borrar el historial. Esta disciplina permite que los algoritmos actúen como instrumentos y que la validación sea la prueba de navegación."
        ),
    ]


def make_objectives(unit: dict[str, Any]) -> list[str]:
    return [
        f"Explicar los conceptos y límites de {section['heading'].lower()}." for section in unit["sections"]
    ] + [
        f"Construir y documentar un {unit['artifact']}.",
        "Diseñar casos normales, límite, inválidos y adversariales.",
        "Justificar decisiones mediante propiedades, consultas y mediciones reproducibles.",
        "Distinguir corrección estructural, utilidad analítica y validación clínica.",
    ]


def make_examples(unit: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for title, scenario, method, interpretation, limitation in unit["examples"]:
        result.append({
            "title": title,
            "scenario": scenario,
            "reasoning_steps": [
                "Definir la pregunta, la unidad de observación y el estado inicial.",
                method,
                "Construir un conjunto sintético mínimo con casos normales, duplicados, nulos y fronteras temporales.",
                "Ejecutar la solución y comparar con un resultado calculado manualmente.",
                "Registrar supuestos, conteos, excepciones y decisiones de diseño.",
            ],
            "interpretation": interpretation,
            "limitations": [limitation, "El ejemplo es educativo y utiliza datos ficticios.", "La corrección técnica no demuestra utilidad clínica."],
        })
    return result


def make_activity(unit: dict[str, Any]) -> list[dict[str, Any]]:
    return [{
        "title": f"Construcción guiada: {unit['artifact']}",
        "instructions": [
            "Definir pregunta, usuarios, unidad de observación, fuentes y criterios de aceptación.",
            "Dibujar el modelo o flujo antes de implementar y enumerar supuestos verificables.",
            "Crear datos sintéticos que incluyan casos normales, ausentes, duplicados, longitudinales y contradictorios.",
            "Implementar por etapas con nombres explícitos y conservar una referencia sencilla como oráculo.",
            "Añadir restricciones, pruebas de propiedades, conteos de control y registro de procedencia.",
            "Revisar el trabajo de otra persona y responder a sus observaciones con cambios trazables.",
        ],
        "deliverables": ["Diagrama o mapa lógico", "Esquema y consultas versionados", "Datos sintéticos reproducibles", "Pruebas automatizadas", "Informe de decisiones y limitaciones"],
        "checking_criteria": ["Identidad y granularidad explícitas", "Reglas críticas verificables", "Resultados reproducibles", "Conexión biomédica funcional", "Límites de uso documentados"],
    }]


def make_practice(unit: dict[str, Any]) -> list[dict[str, Any]]:
    headings = [section["heading"] for section in unit["sections"]]
    return [
        {"level": "Fundamentos", "problems": [
            f"Define con tus palabras {headings[0]} y construye un contraejemplo.",
            f"Representa una instancia mínima de {headings[1]} con datos sintéticos.",
            "Identifica una ambigüedad de identidad o granularidad y propón cómo documentarla.",
            "Explica una ecuación de la unidad e indica cuándo no debe aplicarse.",
        ]},
        {"level": "Aplicación", "problems": [
            f"Implementa una solución para {unit['artifact']} y conserva una versión de referencia.",
            f"Diseña una prueba adversarial relacionada con {headings[2]}.",
            "Compara dos alternativas y justifica la elegida mediante operaciones dominantes y riesgos.",
            "Añade procedencia, versionado y un informe de registros rechazados.",
        ]},
        {"level": "Integración crítica", "problems": [
            f"Audita un diseño que afirma resolver {headings[3]} e identifica supuestos ocultos.",
            "Propón un cambio de requisitos que rompa el diseño actual y diseña una migración.",
            "Separa qué evidencia demuestra corrección, rendimiento y utilidad en el caso estudiado.",
            "Redacta una revisión técnica que incluya riesgos, limitaciones y pruebas faltantes.",
        ]},
    ]


def make_errors(unit: dict[str, Any]) -> list[dict[str, str]]:
    errors = [
        (section["risk"].capitalize() + ".", section["validation"].capitalize() + ".")
        for section in unit["sections"]
    ]
    errors.extend([
        ("Optimizar antes de demostrar corrección.", "Mantener una referencia simple, probarla y medir antes de añadir complejidad."),
        ("Usar datos reales o identificables en ejercicios.", "Trabajar con datos sintéticos o abiertos adecuadamente gobernados."),
        ("Confundir una salida técnicamente válida con una conclusión clínica.", "Limitar la interpretación al contrato del dato y exigir validación externa para cualquier uso clínico."),
    ])
    return [{"error": error, "correction": correction} for error, correction in errors]


def make_self_assessment(unit: dict[str, Any]) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []
    for section in unit["sections"]:
        questions.append({"question": f"¿Cuál es la idea central de {section['heading']}?", "answer": section["core"].capitalize() + "."})
        questions.append({"question": f"¿Qué riesgo debe controlarse en {section['heading']}?", "answer": section["risk"].capitalize() + "."})
    questions.extend([
        {"question": "¿Por qué una consulta sin errores puede seguir siendo incorrecta?", "answer": "Porque puede usar identidad, granularidad, tiempo, denominadores o semántica distintos de la pregunta pretendida."},
        {"question": "¿Qué distingue un prototipo educativo de un sistema clínico validado?", "answer": "El prototipo demuestra conceptos con alcance limitado; un sistema clínico requiere evidencia, seguridad, gobernanza, validación externa y evaluación en el flujo real."},
    ])
    return questions


def make_unit(unit: dict[str, Any]) -> dict[str, Any]:
    theory = []
    for section in unit["sections"]:
        theory.append({
            "heading": section["heading"],
            "paragraphs": theory_paragraphs(unit, section),
            "key_points": [section["core"].capitalize() + ".", section["decision"].capitalize() + ".", section["risk"].capitalize() + ".", section["validation"].capitalize() + "."],
            "equations": [section["equation"]],
        })
    sources = [{"title": title, "organization": organization, "url": url, "type": "fuente académica o institucional"} for title, organization, url in unit["sources"]]
    return {
        "schema_version": "2.0",
        "subject_id": "bases-datos",
        "area_id": "ciencias-basicas",
        "unit": unit["unit"],
        "slug": unit["slug"],
        "title": unit["title"],
        "status": "review",
        "weeks": unit["weeks"],
        "estimated_hours": unit["hours"],
        "purpose": unit["purpose"],
        "learning_objectives": make_objectives(unit),
        "theory_sections": theory,
        "glossary": [{"term": term, "definition": definition} for term, definition in unit["glossary"]],
        "worked_examples": make_examples(unit),
        "guided_activities": make_activity(unit),
        "practice_sets": make_practice(unit),
        "common_errors": make_errors(unit),
        "self_assessment": make_self_assessment(unit),
        "biomedical_connections": [
            "Diseño de repositorios longitudinales con identidad, tiempo y procedencia explícitos.",
            "Preparación de datos para bioinformática, epidemiología, laboratorio e investigación reproducible.",
            "Auditoría de transformaciones, exclusiones y cambios de vocabulario.",
            "Separación entre resultado técnico, evidencia científica y utilidad clínica.",
            f"Aplicación integradora mediante un {unit['artifact']}.",
        ],
        "sources": sources,
        "editorial_notice": "Material educativo en estado de revisión. Requiere revisión docente experta antes de considerarse versión académica definitiva. Los ejemplos utilizan datos ficticios o abiertos y no constituyen software clínico validado, consejo médico ni recomendación asistencial.",
    }


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    generated = [make_unit(unit) for unit in UNITS]
    assert sum(item["estimated_hours"] for item in generated) == 128
    assert sorted(week for item in generated for week in item["weeks"]) == list(range(1, 17))
    total_words = 0
    for item in generated:
        serialized = json.dumps(item, ensure_ascii=False)
        words = len(WORD_RE.findall(serialized))
        if not 2000 <= words <= 5000:
            raise ValueError(f"unit-{item['unit']:02d}: extensión {words} fuera de 2000–5000")
        total_words += words
        path = DEST / f"unit-{item['unit']:02d}.json"
        path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Generada {path.relative_to(ROOT)}: {words} palabras")
    if total_words < 15000:
        raise ValueError(f"curso incompleto: {total_words} palabras; mínimo 15000")
    print(f"Bases de Datos: 6 unidades, 128 horas, {total_words} palabras")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
