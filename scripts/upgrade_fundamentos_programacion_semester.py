#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
UNIT_DIR = ROOT / "data" / "generated_units" / "fundamentos-programacion"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)

META: dict[int, dict[str, Any]] = {
    1: {
        "hours": 24,
        "weeks": [1, 2, 3],
        "difficulty": "Fundamental",
        "prerequisites": [
            "Aritmética y porcentajes elementales.",
            "Manejo básico de archivos y carpetas.",
            "Lectura de fórmulas y tablas sencillas.",
            "No se requiere programación previa.",
        ],
        "previous": "El diagnóstico de prerrequisitos y la preparación del entorno Python.",
        "next": "Decisiones, repetición y validación sistemática mediante estructuras de control.",
    },
    2: {
        "hours": 16,
        "weeks": [4, 5],
        "difficulty": "Fundamental-intermedia",
        "prerequisites": [
            "Variables, expresiones y tipos básicos de Python.",
            "Comparaciones y valores booleanos.",
            "Contratos de entrada y salida.",
        ],
        "previous": "Algoritmos secuenciales, tipos y validación elemental.",
        "next": "Encapsulación del comportamiento mediante funciones y módulos comprobables.",
    },
    3: {
        "hours": 24,
        "weeks": [6, 7, 8],
        "difficulty": "Intermedia",
        "prerequisites": [
            "Algoritmos secuenciales y estructuras de control.",
            "Listas básicas y manejo de excepciones elemental.",
            "Capacidad para escribir y ejecutar scripts Python.",
        ],
        "previous": "Control explícito de ramas, iteraciones, errores y trazabilidad.",
        "next": "Representación persistente de colecciones y datos tabulares en archivos.",
    },
    4: {
        "hours": 24,
        "weeks": [9, 10, 11],
        "difficulty": "Intermedia",
        "prerequisites": [
            "Funciones, contratos y excepciones.",
            "Bucles y comprensión de colecciones.",
            "Uso básico de pathlib y del sistema de archivos.",
        ],
        "previous": "Funciones modulares que separan validación, cálculo y efectos.",
        "next": "Análisis tabular, resúmenes y visualización reproducible.",
    },
    5: {
        "hours": 16,
        "weeks": [12, 13],
        "difficulty": "Intermedia",
        "prerequisites": [
            "Colecciones, CSV, JSON y esquemas de datos.",
            "Funciones y excepciones.",
            "Estadística descriptiva elemental.",
        ],
        "previous": "Ingestión, validación y persistencia trazable de datos.",
        "next": "Pruebas, control de versiones, entornos y entrega mantenible.",
    },
    6: {
        "hours": 24,
        "weeks": [14, 15, 16],
        "difficulty": "Intermedia-integradora",
        "prerequisites": [
            "Dominio funcional de las unidades 1–5.",
            "Capacidad para organizar un proyecto Python pequeño.",
            "Lectura de mensajes de error y documentación técnica.",
        ],
        "previous": "Construcción de análisis y figuras reproducibles a partir de datos validados.",
        "next": "Algoritmos y Estructuras de Datos, Bases de Datos y programación científica avanzada.",
    },
}

SECTION_ADDITIONS: dict[int, list[str]] = {
    1: [
        "El entorno de ejecución forma parte del algoritmo observable. Un mismo archivo puede comportarse de manera diferente si cambia la versión de Python, la codificación, la configuración regional o la carpeta de trabajo. Por eso el estudiante debe aprender a distinguir intérprete, terminal, editor, cuaderno y script. Ejecutar una celda aislada puede depender de variables creadas anteriormente; ejecutar un script desde el inicio obliga a declarar el estado necesario y es una comprobación básica de reproducibilidad.",
        "La elección de tipo también es una decisión semántica. Un identificador numérico no debe convertirse en entero si los ceros iniciales tienen significado; una fecha no debería almacenarse como un número sin formato; una categoría codificada con 0 y 1 no se vuelve una magnitud continua. Los tipos incorporados permiten comenzar, pero el programa debe conservar la diferencia entre cantidad, etiqueta, ausencia y estado lógico para evitar operaciones que sean sintácticamente válidas y conceptualmente absurdas.",
        "La validación se beneficia de separar sintaxis, dominio y coherencia. La cadena '37.2' puede convertirse a float y superar la validación sintáctica; después debe comprobarse si pertenece al dominio aceptado y si su unidad es la esperada. Una tercera capa puede revisar coherencia con otros campos, por ejemplo que un tiempo final no preceda al inicial. Esta secuencia produce mensajes de error más útiles y evita mezclar todos los fallos bajo una sola condición genérica.",
    ],
    2: [
        "Las expresiones lógicas tienen precedencia y evaluación de cortocircuito. En A and B, Python no evalúa B cuando A ya es falso; en A or B, no evalúa B cuando A es verdadero. Este comportamiento permite proteger operaciones, como comprobar primero que una lista no esté vacía antes de acceder a su primer elemento. También puede ocultar efectos secundarios si una función se llama dentro de la condición. Las condiciones deberían ser principalmente descriptivas y libres de cambios de estado.",
        "La selección del bucle afecta claridad y coste. Recorrer una colección una vez suele ser lineal en su tamaño; anidar recorridos puede elevar el trabajo de forma cuadrática. En un curso inicial no se requiere un análisis formal completo, pero sí reconocer que repetir búsquedas dentro de cada iteración puede ser innecesario. Usar un diccionario o conjunto para pertenencia, precalcular valores invariantes y terminar temprano bajo una condición documentada son decisiones que mejoran eficiencia sin sacrificar legibilidad.",
        "Las pruebas de flujo deben derivarse de una tabla de decisión o de particiones del dominio. Para cada condición se identifican combinaciones relevantes, límites y rutas imposibles. La cobertura de ramas indica qué caminos se ejecutaron, pero no confirma que las condiciones expresen la regla correcta. En datos biomédicos, el programa debe devolver conteos y razones de exclusión para que un filtro pueda auditarse y no transforme silenciosamente la población analizada.",
    ],
    3: [
        "Una interfaz de función debe ser pequeña pero suficiente. Pasar diez argumentos relacionados puede indicar que falta una estructura de configuración; pasar un diccionario genérico puede ocultar campos obligatorios. Los parámetros solo posicionales, nombrados y con valores por defecto permiten diseñar llamadas legibles. Las decisiones que alteran unidades, fórmulas o exclusiones deben aparecer explícitamente, mientras que opciones de presentación inocuas pueden tener un valor predeterminado documentado.",
        "La mutabilidad de los argumentos exige atención. Aunque la variable local tenga un nombre distinto, una lista recibida sigue siendo el mismo objeto si se modifica in situ. Una función pura que devuelve una nueva lista facilita pruebas y composición, pero copiar datos grandes tiene coste. La elección debe declararse en el contrato. Los valores por defecto mutables se crean una sola vez al definir la función; usar None y crear la colección dentro evita compartir estado accidental entre llamadas.",
        "Los módulos convierten un conjunto de funciones en una interfaz reutilizable. El bloque if __name__ == '__main__' separa la ejecución como programa de la importación como biblioteca. Los imports deben ser explícitos y no producir cálculos costosos ni modificar archivos. Una organización elemental puede separar io.py, validation.py, analysis.py y cli.py. Esta estructura no es burocracia: permite probar la lógica sin depender del teclado o del sistema de archivos.",
    ],
    4: [
        "La elección de colección también tiene implicaciones de eficiencia. Buscar por posición en una lista es directo, pero encontrar repetidamente un identificador requiere recorrerla; un diccionario permite acceso promedio por clave. Un conjunto es apropiado para detectar duplicados o pertenencia, pero no conserva el orden semántico de una serie. Estas propiedades deben subordinarse al significado: optimizar destruyendo secuencia, multiplicidad o procedencia produce un resultado más rápido y menos válido.",
        "Las estructuras anidadas deberían representar una jerarquía real, no crecer sin diseño. Una lista de diccionarios puede servir para una tabla pequeña, pero permite registros con claves diferentes. TypedDict, dataclasses o validadores de esquema hacen visibles campos y tipos, aunque no reemplazan reglas de dominio. La normalización tabular evita repetir datos de participante en cada medición, pero introduce relaciones que deben reconstruirse mediante claves estables.",
        "La persistencia necesita decisiones sobre formato, versión y procedencia. JSON no admite directamente fechas, NaN o arreglos de NumPy sin conversión; CSV no distingue números de texto ni listas anidadas. El programa debe registrar versión del esquema y no asumir que todo archivo futuro tendrá la misma estructura. Para resultados importantes conviene escribir a una ruta nueva o temporal y reemplazar de forma controlada, reduciendo el riesgo de dejar un archivo incompleto tras un fallo.",
    ],
    5: [
        "NumPy y pandas introducen operaciones vectorizadas que actúan sobre conjuntos de valores. Una operación vectorizada suele ser más breve y eficiente que un bucle Python, pero requiere comprender forma, alineación y difusión. Dos Series se alinean por índice, no solamente por posición; índices duplicados pueden multiplicar filas durante combinaciones. Antes de calcular se inspeccionan shape, dtypes, índices y valores faltantes, porque una expresión compacta puede propagar un error estructural a toda una tabla.",
        "Los datos ordenados o tidy asignan una variable a cada columna, una observación a cada fila y una unidad observacional a cada tabla. Este principio facilita filtros, agrupaciones y gráficos, pero depende de definir correctamente la unidad de observación. Una tabla de formato ancho puede ser adecuada para presentación y otra de formato largo para análisis. Transformar entre ambas exige comprobar identificadores, duplicados y número de filas.",
        "La figura final debe acompañarse de una tabla de control y de código que reconstruya sus datos. Guardar solo una imagen rompe la trazabilidad. El flujo reproducible conserva datos de origen, transformación, resumen y parámetros visuales. Los cuadernos son útiles para narrar, pero deben reiniciarse y ejecutarse de principio a fin; una celda que depende de un orden oculto de ejecución es un defecto reproducible aunque la figura se vea correcta.",
    ],
    6: [
        "Los requisitos deben conectarse con pruebas mediante trazabilidad. Si el requisito dice que ninguna fila inválida se descarta sin registro, una prueba de integración debe comprobar los conteos y mensajes. Una prueba que replica la implementación línea por línea aporta poca independencia. Las pruebas basadas en propiedades, como verificar que una conversión seguida de su inversa recupera el valor dentro de tolerancia, examinan familias de casos y complementan ejemplos concretos.",
        "La depuración es un proceso de formulación y contraste de hipótesis. Primero se reproduce el fallo con la entrada mínima, se observa el traceback, se inspecciona el estado y se localiza la primera desviación respecto al contrato. Añadir prints indiscriminadamente puede alterar el comportamiento y generar ruido; un depurador, logging estructurado o aserciones temporales permiten observar con propósito. Después de corregir, el caso se conserva como prueba de regresión.",
        "La reproducibilidad incluye configuración y datos, no solo dependencias. Los parámetros no deberían quedar dispersos como números mágicos; pueden centralizarse en argumentos o archivos de configuración versionados. Las semillas controlan parte de la aleatoriedad, pero no garantizan resultados idénticos entre bibliotecas, hardware o paralelismo. El informe debe distinguir repetibilidad en el mismo entorno, reproducibilidad en otro entorno y validez del resultado científico.",
    ],
}

NEW_SECTIONS: dict[int, dict[str, Any]] = {
    1: {
        "heading": "4. Ejecución, errores y depuración elemental",
        "paragraphs": [
            "Python debe analizar la sintaxis antes de ejecutar un programa. Un SyntaxError indica que el texto no forma una instrucción válida; un error en tiempo de ejecución aparece después, por ejemplo al convertir texto no numérico o dividir por cero. Un error lógico es más difícil: el programa termina, pero implementa una fórmula, unidad o condición equivocada. Distinguir estas categorías orienta la búsqueda y evita corregir la sintaxis cuando el problema está en el modelo.",
            "El traceback muestra la cadena de llamadas y la línea donde se detectó la excepción. La última línea identifica el tipo y mensaje, pero la causa puede haberse originado antes. Leerlo de abajo hacia arriba ayuda a ubicar la operación, y después se revisan valores y tipos. El objetivo no es silenciar el error, sino comprender qué contrato se incumplió y decidir si corresponde corregir datos, código o especificación.",
            "La depuración incremental ejecuta una parte pequeña, inspecciona su salida y la compara con un valor esperado. Las aserciones expresan propiedades internas que deberían cumplirse durante el desarrollo. No sustituyen la validación de entradas externas y pueden desactivarse, pero son útiles para detectar estados imposibles. Los mensajes deben incluir significado y no exponer información sensible.",
            "Un programa inicial debería poder ejecutarse desde una terminal, aceptar datos de ejemplo y terminar con un código de salida coherente. Los cuadernos facilitan exploración, pero una entrega reproducible necesita un orden claro. Guardar el script, registrar la versión de Python y conservar casos de prueba convierte una demostración interactiva en un artefacto que otra persona puede revisar.",
        ],
        "key_points": [
            "Sintaxis, ejecución y lógica producen clases distintas de fallo.",
            "El traceback localiza dónde se detectó una excepción, no siempre su causa original.",
            "La depuración contrasta estados observados con un contrato esperado.",
            "Un artefacto reproducible se ejecuta desde un estado inicial documentado.",
        ],
    },
    2: {
        "heading": "4. Tablas de decisión y máquinas de estados sencillas",
        "paragraphs": [
            "Cuando varias condiciones interactúan, una tabla de decisión enumera factores y acciones antes de escribir if anidados. Permite detectar combinaciones no cubiertas, reglas contradictorias y prioridades implícitas. El código puede traducir la tabla mediante ramas ordenadas o mediante datos de configuración. La tabla sigue siendo parte de la especificación y debe versionarse junto al programa.",
            "Algunos procesos dependen del estado previo, no solo de la entrada actual. Una máquina de estados finita representa estados permitidos, eventos y transiciones. Por ejemplo, un archivo puede pasar de recibido a validado, rechazado o procesado. Impedir transiciones imposibles es más claro que dispersar booleanos como validado, procesado y error que pueden adoptar combinaciones incoherentes.",
            "Los bucles que procesan eventos pueden conservar un estado y aplicar una transición por iteración. La invariante incluye que el estado pertenezca al conjunto permitido y que cada evento se registre. Esta estructura es útil para pipelines educativos, pero no convierte el sistema en un dispositivo seguro: faltan concurrencia, persistencia, recuperación y análisis de riesgos.",
            "Las decisiones dirigidas por datos reducen cadenas extensas de elif cuando la correspondencia es simple, por ejemplo un diccionario de códigos a funciones. Sin embargo, las reglas con rangos, prioridades o efectos requieren una representación más explícita. Elegir entre código y datos depende de legibilidad, validación y frecuencia de cambio, no de minimizar líneas.",
        ],
        "key_points": [
            "Las tablas de decisión revelan huecos y contradicciones antes de programar.",
            "Una máquina de estados controla transiciones y combinaciones permitidas.",
            "El estado y los eventos deben conservar trazabilidad.",
            "La configuración basada en datos necesita validación y límites claros.",
        ],
    },
    3: {
        "heading": "4. Módulos, dependencias e interfaces mantenibles",
        "paragraphs": [
            "Un módulo es un archivo importable y un paquete organiza módulos relacionados. La interfaz pública debería ser menor que la implementación interna: otras partes del proyecto dependen de nombres estables, mientras los detalles pueden cambiar. Prefijar helpers internos y exportar funciones centrales reduce acoplamiento, aunque Python confía principalmente en convenciones.",
            "Las dependencias deben apuntar hacia componentes más generales. La lógica de cálculo no debería importar una interfaz gráfica ni conocer una ruta fija. En su lugar recibe datos y configuración. Esta inversión sencilla permite que una prueba suministre datos en memoria y que la aplicación real use archivos. No exige un framework: basta con evitar que las funciones puras creen directamente sus dependencias externas.",
            "Las excepciones forman parte de la interfaz. Una función de bajo nivel puede producir ValueError o FileNotFoundError; una capa superior decide si añade contexto, reintenta o termina. Capturar y reemplazar una excepción debería preservar su causa mediante raise ... from ..., facilitando el diagnóstico. Devolver None para cualquier fallo pierde información cuando None también puede ser un resultado válido.",
            "La documentación de una interfaz incluye ejemplo mínimo, tipos, unidades, efectos, excepciones y estabilidad. Los doctests pueden comprobar ejemplos simples, pero no reemplazan una suite. Mantener una API pequeña y coherente prepara al estudiante para paquetes científicos y evita que el proyecto final se convierta en un único script imposible de probar por partes.",
        ],
        "key_points": [
            "La interfaz pública debe ser estable y menor que los detalles internos.",
            "La lógica de cálculo recibe dependencias en lugar de crearlas ocultamente.",
            "Las excepciones específicas y encadenadas conservan contexto.",
            "Una API documentada mejora prueba, reutilización y mantenimiento.",
        ],
    },
    4: {
        "heading": "4. Esquemas, procedencia y persistencia segura",
        "paragraphs": [
            "Un esquema especifica nombres, tipos, obligatoriedad, unidades y restricciones. Puede expresarse en documentación, código o un formato formal. Validar solo que una columna exista es insuficiente si contiene otra unidad o si el identificador dejó de ser único. La versión del esquema permite detectar cambios deliberados y diseñar migraciones en lugar de interpretar silenciosamente un formato nuevo como antiguo.",
            "La procedencia registra de dónde proviene un archivo, cuándo se obtuvo, qué versión tiene y qué transformaciones se aplicaron. Un hash puede detectar cambios de bytes, aunque no demuestra calidad ni autenticidad por sí solo. En un proyecto educativo, un manifiesto con ruta, tamaño, fecha, licencia y hash enseña a tratar los datos como una entrada versionada, no como un objeto intercambiable.",
            "Las escrituras deberían evitar corrupción parcial. Un patrón sencillo genera la salida en un archivo temporal, fuerza el cierre y después reemplaza el destino. Las copias de seguridad y la escritura atómica dependen del sistema de archivos, pero el principio es no destruir la última versión válida antes de verificar la nueva. Para formatos grandes, bases de datos y concurrencia se requieren mecanismos más avanzados.",
            "Los datos humanos necesitan minimización, seudonimización, control de acceso y políticas de retención. Eliminar el nombre no garantiza anonimato, porque fechas, ubicaciones y combinaciones raras pueden reidentificar. Este curso usará datos sintéticos o públicos apropiados. Las decisiones de privacidad pertenecen al diseño del flujo, no a una limpieza final después de programar.",
        ],
        "key_points": [
            "Un esquema incluye significado, tipos, unidades y restricciones.",
            "La procedencia conecta cada resultado con su fuente y transformaciones.",
            "La persistencia debe evitar destruir una versión válida ante fallos.",
            "La privacidad se diseña desde la recogida y no se resuelve solo quitando nombres.",
        ],
    },
    5: {
        "heading": "4. Arreglos, tablas y cuadernos reproducibles",
        "paragraphs": [
            "Un ndarray de NumPy tiene forma y dtype comunes. La vectorización permite operar sobre ejes completos, pero una suma por el eje equivocado puede producir un resultado numéricamente válido y semánticamente incorrecto. El código debe nombrar ejes en la explicación, comprobar shapes y usar ejemplos pequeños donde el resultado pueda verificarse manualmente.",
            "pandas añade etiquetas y manejo de faltantes. La selección con loc usa etiquetas y con iloc posiciones; confundirlas puede extraer filas distintas. Las operaciones groupby separan, aplican y combinan, pero la función de agregación debe corresponder a la pregunta. El recuento de valores no faltantes puede diferir del número de filas, por lo que count, size y número de participantes deben distinguirse.",
            "Una visualización puede construirse desde una tabla de análisis explícita. Preparar esa tabla por separado facilita auditar qué filas, grupos y transformaciones alimentan la figura. El título no debería contener la conclusión causal; el pie puede describir tamaño, unidad, tratamiento de faltantes y método de resumen. Mostrar datos individuales cuando es posible evita que una barra o una media oculte la distribución.",
            "Los cuadernos combinan narrativa, código y resultados, pero también acumulan estado oculto. La entrega debe reiniciar kernel, ejecutar todas las celdas y comprobar que los archivos de entrada están disponibles mediante rutas relativas o configuración. Para automatización, la lógica central se extrae a funciones o módulos y el cuaderno queda como interfaz narrativa reproducible.",
        ],
        "key_points": [
            "Forma, dtype y eje son parte del significado de un arreglo.",
            "Las etiquetas de pandas pueden alinear o duplicar datos inesperadamente.",
            "La tabla que alimenta una figura debe ser auditable.",
            "Un cuaderno reproducible se ejecuta completo desde un estado limpio.",
        ],
    },
    6: {
        "heading": "4. Del prototipo al proyecto mantenible",
        "paragraphs": [
            "Un proyecto mantenible tiene una estructura predecible: código fuente, pruebas, documentación, configuración y datos de ejemplo separados. El README explica instalación, ejecución, entradas, salidas y límites. Un archivo pyproject.toml puede centralizar metadatos y herramientas. La estructura debe ser proporcional al tamaño; el objetivo es hacer visibles las responsabilidades, no imitar una empresa con carpetas vacías.",
            "Los commits registran unidades de razonamiento. Un buen commit modifica un propósito, incluye pruebas relevantes y deja el proyecto ejecutable. Una rama facilita experimentar y un pull request reúne explicación, diff y evidencia automática. Reescribir el historial compartido o mezclar refactorización con cambios científicos dificulta revisar qué alteró el resultado.",
            "La integración continua ejecuta formato, linting, análisis de tipos, pruebas y validaciones de artefactos. Cada control tiene alcance: un linter encuentra patrones, mypy evalúa anotaciones bajo supuestos y pytest ejecuta casos. Pasar todos no demuestra que la pregunta sea correcta ni que el software sea seguro. El pipeline debe fallar de forma comprensible y producir registros suficientes para investigar.",
            "La entrega final incluye una declaración de finalidad. Un prototipo educativo puede explorar datos sintéticos; una herramienta de investigación necesita validación metodológica y gestión de datos; software destinado a decisiones clínicas entra en procesos de calidad, riesgo y regulación. Etiquetar versión, uso previsto y limitaciones reduce la posibilidad de que un resultado se reutilice fuera de alcance.",
        ],
        "key_points": [
            "La estructura del proyecto hace visibles código, pruebas, datos y configuración.",
            "Los commits y PR deben facilitar revisión causal de los cambios.",
            "CI automatiza evidencia parcial, no certifica validez total.",
            "La finalidad declarada delimita qué usos están respaldados.",
        ],
    },
}

SECOND_EXAMPLES: dict[int, dict[str, Any]] = {
    1: {
        "title": "Conversión trazable de concentración y detección de entrada inválida",
        "scenario": "Una función educativa recibe masa en miligramos y volumen en mililitros, calcula mg/mL y rechaza texto no numérico, valores negativos y volumen cero.",
        "pseudocode": [
            "Convertir masa y volumen a float dentro de una capa de entrada.",
            "Comprobar que masa sea no negativa y volumen estrictamente positivo.",
            "Calcular concentración como masa/volumen.",
            "Retornar el número y añadir la unidad solo en la presentación.",
            "Probar un caso conocido, volumen cero y texto inválido.",
        ],
        "code": "def concentracion_mg_ml(masa_mg: float, volumen_ml: float) -> float:\n    if not isinstance(masa_mg, (int, float)) or not isinstance(volumen_ml, (int, float)):\n        raise TypeError('masa y volumen deben ser numéricos')\n    if masa_mg < 0:\n        raise ValueError('masa_mg no puede ser negativa')\n    if volumen_ml <= 0:\n        raise ValueError('volumen_ml debe ser positivo')\n    return float(masa_mg) / float(volumen_ml)\n\nassert abs(concentracion_mg_ml(25, 10) - 2.5) < 1e-12",
        "reasoning_steps": [
            "Los tipos se validan antes de las comparaciones.",
            "Masa cero es admisible en este contrato; volumen cero no.",
            "El retorno numérico permite reutilizar la salida.",
            "La aserción usa un caso cuyo resultado manual es conocido.",
            "La función no interpreta la concentración ni prescribe uso.",
        ],
        "expected_output": "2.5 mg/mL al presentar el resultado del caso válido.",
        "limitations": [
            "No incorpora incertidumbre de masa o volumen.",
            "No valida pureza ni comportamiento físico de la solución.",
            "No sustituye un procedimiento de laboratorio.",
        ],
    },
    2: {
        "title": "Procesamiento mediante estados de un lote de archivos",
        "scenario": "Cada archivo sintético debe pasar de recibido a validado o rechazado; solo los validados pueden procesarse. El historial de transiciones se conserva.",
        "code": "TRANSICIONES = {\n    ('recibido', 'validar_ok'): 'validado',\n    ('recibido', 'validar_error'): 'rechazado',\n    ('validado', 'procesar'): 'procesado',\n}\n\ndef transicionar(estado: str, evento: str) -> str:\n    try:\n        return TRANSICIONES[(estado, evento)]\n    except KeyError as error:\n        raise ValueError(f'transición no permitida: {estado} + {evento}') from error\n\nhistorial = ['recibido']\nhistorial.append(transicionar(historial[-1], 'validar_ok'))\nhistorial.append(transicionar(historial[-1], 'procesar'))",
        "reasoning_steps": [
            "Los estados permitidos se representan explícitamente.",
            "La tabla impide procesar un archivo rechazado.",
            "La excepción conserva la transición imposible.",
            "El historial permite auditar el camino seguido.",
            "Una implementación real necesitaría persistencia y recuperación.",
        ],
        "expected_output": "['recibido', 'validado', 'procesado']",
        "limitations": [
            "No gestiona concurrencia ni reinicios.",
            "Los eventos son ejemplos educativos.",
            "No constituye un sistema clínico de trazabilidad.",
        ],
    },
    3: {
        "title": "Composición de parser, validador y cálculo",
        "scenario": "Un módulo recibe texto con una concentración, lo convierte, valida el dominio y aplica una conversión de mmol/L a mol/L sin mezclar lectura con cálculo.",
        "code": "def parsear_float(texto: str) -> float:\n    try:\n        return float(texto)\n    except ValueError as error:\n        raise ValueError(f'no es un número: {texto!r}') from error\n\ndef validar_no_negativo(valor: float, nombre: str) -> float:\n    if valor < 0:\n        raise ValueError(f'{nombre} debe ser no negativo')\n    return valor\n\ndef mmol_l_a_mol_l(valor: float) -> float:\n    return validar_no_negativo(valor, 'concentración') / 1000.0\n\nresultado = mmol_l_a_mol_l(parsear_float('2.5'))",
        "reasoning_steps": [
            "Cada función representa una etapa y puede probarse sola.",
            "La excepción de conversión conserva su causa.",
            "La validación recibe el nombre para producir contexto.",
            "La conversión retorna un número sin imprimir.",
            "La composición produce 0.0025 mol/L.",
        ],
        "expected_output": "0.0025 mol/L.",
        "limitations": [
            "No maneja separadores decimales regionales.",
            "La unidad de entrada debe estar fijada por el contrato.",
            "No incluye incertidumbre ni metadatos de la medición.",
        ],
    },
    4: {
        "title": "Validación de un documento JSON con versión de esquema",
        "scenario": "Un archivo sintético debe contener schema_version, sample_id y measurements. Se conserva una lista de errores en lugar de aceptar parcialmente el documento.",
        "code": "def validar_documento(doc: object) -> list[str]:\n    errores: list[str] = []\n    if not isinstance(doc, dict):\n        return ['la raíz debe ser un objeto']\n    if doc.get('schema_version') != '1.0':\n        errores.append('schema_version no soportada')\n    if not isinstance(doc.get('sample_id'), str) or not doc.get('sample_id'):\n        errores.append('sample_id inválido')\n    mediciones = doc.get('measurements')\n    if not isinstance(mediciones, list):\n        errores.append('measurements debe ser una lista')\n    elif not all(isinstance(x, (int, float)) for x in mediciones):\n        errores.append('cada medición debe ser numérica')\n    return errores",
        "reasoning_steps": [
            "La raíz se valida antes de acceder a claves.",
            "La versión evita interpretar formatos incompatibles.",
            "Identificador y mediciones tienen contratos separados.",
            "La función acumula errores útiles para corrección.",
            "La ausencia de errores no demuestra calidad científica de las mediciones.",
        ],
        "expected_output": "Una lista vacía para documentos estructuralmente válidos o mensajes específicos.",
        "limitations": [
            "Es un esquema manual y pequeño.",
            "No valida unidades, procedencia ni privacidad.",
            "Sistemas reales pueden usar JSON Schema o modelos tipados.",
        ],
    },
    5: {
        "title": "Resumen por participante sin duplicar observaciones",
        "scenario": "Una tabla contiene mediciones repetidas. Se calcula primero una media por participante y luego el resumen de participantes, evitando que quienes tienen más visitas pesen más.",
        "code": "import pandas as pd\n\ndef resumen_por_participante(datos: pd.DataFrame) -> pd.DataFrame:\n    requeridas = {'participante', 'valor'}\n    if not requeridas.issubset(datos.columns):\n        raise ValueError('faltan columnas')\n    limpio = datos.dropna(subset=['participante', 'valor']).copy()\n    por_persona = (\n        limpio.groupby('participante', as_index=False)['valor']\n        .mean()\n        .rename(columns={'valor': 'media_personal'})\n    )\n    return por_persona\n",
        "reasoning_steps": [
            "Las columnas se comprueban antes del análisis.",
            "La copia evita modificar la tabla recibida.",
            "La primera agregación produce una fila por participante.",
            "Un resumen poblacional posterior ponderaría a cada participante una vez.",
            "La decisión sobre faltantes debe documentarse y analizarse.",
        ],
        "expected_output": "Una tabla con participante y media_personal.",
        "limitations": [
            "La media personal puede no representar trayectorias temporales.",
            "Eliminar faltantes puede introducir sesgo.",
            "No realiza inferencia ni ajusta covariables.",
        ],
    },
    6: {
        "title": "Pruebas unitarias e integración para un importador",
        "scenario": "Se prueba una función pura de conversión y después el flujo que lee un archivo temporal, valida filas y devuelve datos y errores.",
        "code": "import math\n\ndef porcentaje_cambio(inicial: float, final: float) -> float:\n    if inicial == 0:\n        raise ValueError('inicial no puede ser cero')\n    return 100.0 * (final - inicial) / inicial\n\ndef test_porcentaje_cambio():\n    assert math.isclose(porcentaje_cambio(10, 12), 20.0)\n\ndef test_inicial_cero():\n    try:\n        porcentaje_cambio(0, 1)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError('se esperaba ValueError')",
        "reasoning_steps": [
            "El contrato define el comportamiento para denominador cero.",
            "El caso conocido se calcula manualmente.",
            "math.isclose expresa una comparación numérica aproximada.",
            "La prueba inválida exige la excepción específica.",
            "Una prueba de integración añadirá el archivo y los conteos de filas.",
        ],
        "expected_output": "Las pruebas terminan sin fallos para la implementación mostrada.",
        "limitations": [
            "Faltan pruebas de tipos, infinitos y NaN.",
            "El ejemplo no mide cobertura ni propiedades.",
            "Pruebas superadas no equivalen a validación clínica.",
        ],
    },
}

EXTRA_ASSESSMENT: dict[int, list[dict[str, str]]] = {
    1: [
        {"question": "¿Qué diferencia existe entre intérprete, script y cuaderno?", "answer": "El intérprete ejecuta instrucciones; un script declara una ejecución ordenada; un cuaderno combina celdas y puede conservar estado entre ejecuciones."},
        {"question": "¿Qué indica un traceback?", "answer": "La cadena de llamadas y el punto donde se detectó una excepción, junto con su tipo y mensaje."},
        {"question": "¿Por qué un identificador con ceros iniciales puede ser str?", "answer": "Porque funciona como etiqueta y convertirlo a número destruiría parte de su representación."},
    ],
    2: [
        {"question": "¿Qué es evaluación de cortocircuito?", "answer": "La omisión del segundo operando cuando el primero ya determina el resultado de and u or."},
        {"question": "¿Qué aporta una tabla de decisión?", "answer": "Expone combinaciones, prioridades, huecos y contradicciones antes de escribir ramas."},
        {"question": "¿Cuándo conviene una máquina de estados?", "answer": "Cuando las acciones permitidas dependen del estado previo y de eventos definidos."},
        {"question": "¿Por qué cobertura de ramas no demuestra corrección?", "answer": "Porque puede ejecutar todas las ramas aunque las reglas implementadas sean conceptualmente erróneas."},
    ],
    3: [
        {"question": "¿Qué problema causa un argumento por defecto mutable?", "answer": "El mismo objeto se reutiliza entre llamadas y puede acumular estado inesperado."},
        {"question": "¿Para qué sirve if __name__ == '__main__'?", "answer": "Separa la ejecución como programa de la importación como módulo."},
        {"question": "¿Qué significa inyectar una dependencia?", "answer": "Recibirla como argumento o interfaz en lugar de crearla ocultamente dentro de la lógica."},
    ],
    4: [
        {"question": "¿Por qué versionar un esquema?", "answer": "Para detectar cambios incompatibles y migrar datos de forma explícita."},
        {"question": "¿Qué registra la procedencia?", "answer": "Origen, versión, licencia y transformaciones que conectan una fuente con un resultado."},
        {"question": "¿Qué ventaja tiene escribir primero a un archivo temporal?", "answer": "Reduce el riesgo de reemplazar una salida válida por un archivo incompleto tras un fallo."},
    ],
    5: [
        {"question": "¿Qué es broadcasting en NumPy?", "answer": "Una regla para combinar arreglos de formas compatibles sin copiar explícitamente cada valor."},
        {"question": "¿Por qué count y size pueden diferir en pandas?", "answer": "count excluye faltantes de la variable; size cuenta filas del grupo."},
        {"question": "¿Qué condición debe cumplir un cuaderno antes de entregarse?", "answer": "Reiniciarse y ejecutarse completamente desde un estado limpio sin dependencias ocultas."},
    ],
    6: [
        {"question": "¿Qué diferencia existe entre repetibilidad y reproducibilidad?", "answer": "Repetibilidad busca el mismo resultado en condiciones cercanas; reproducibilidad evalúa reconstrucción en otro entorno o por otra persona."},
        {"question": "¿Qué es una prueba basada en propiedades?", "answer": "Una prueba que verifica una propiedad general sobre múltiples entradas, no un único ejemplo."},
        {"question": "¿Por qué un commit debe tener un propósito coherente?", "answer": "Porque facilita revisar qué cambio causó una modificación del comportamiento."},
    ],
}

EXTRA_SOURCES: dict[int, list[dict[str, str]]] = {
    1: [
        {"title": "The Python Language Reference — Data model", "organization": "Python Software Foundation", "url": "https://docs.python.org/3/reference/datamodel.html", "type": "referencia oficial"},
        {"title": "Floating-Point Arithmetic: Issues and Limitations", "organization": "Python Software Foundation", "url": "https://docs.python.org/3/tutorial/floatingpoint.html", "type": "documentación oficial"},
    ],
    2: [
        {"title": "Python Language Reference — Compound statements", "organization": "Python Software Foundation", "url": "https://docs.python.org/3/reference/compound_stmts.html", "type": "referencia oficial"},
        {"title": "Control Flow", "organization": "Software Carpentry", "url": "https://swcarpentry.github.io/python-novice-inflammation/07-cond.html", "type": "lección abierta"},
        {"title": "Looping Over Data Sets", "organization": "Software Carpentry", "url": "https://swcarpentry.github.io/python-novice-inflammation/05-loop.html", "type": "lección abierta"},
    ],
    3: [
        {"title": "Python Modules", "organization": "Python Software Foundation", "url": "https://docs.python.org/3/tutorial/modules.html", "type": "documentación oficial"},
        {"title": "Errors and Exceptions", "organization": "Python Software Foundation", "url": "https://docs.python.org/3/tutorial/errors.html", "type": "documentación oficial"},
    ],
    4: [
        {"title": "Python Data Model — Objects, values and types", "organization": "Python Software Foundation", "url": "https://docs.python.org/3/reference/datamodel.html#objects-values-and-types", "type": "referencia oficial"},
        {"title": "JSON Schema Specification", "organization": "JSON Schema", "url": "https://json-schema.org/specification", "type": "especificación"},
        {"title": "Data Organization in Spreadsheets", "organization": "The American Statistician", "url": "https://doi.org/10.1080/00031305.2017.1375989", "type": "artículo académico"},
    ],
    5: [
        {"title": "NumPy Fundamentals", "organization": "NumPy", "url": "https://numpy.org/doc/stable/user/basics.html", "type": "documentación oficial"},
        {"title": "Tidy Data", "organization": "Journal of Statistical Software", "url": "https://www.jstatsoft.org/article/view/v059i10", "type": "artículo académico"},
    ],
    6: [
        {"title": "pytest Documentation", "organization": "pytest development team", "url": "https://docs.pytest.org/en/stable/", "type": "documentación oficial"},
        {"title": "logging — Logging facility for Python", "organization": "Python Software Foundation", "url": "https://docs.python.org/3/library/logging.html", "type": "documentación oficial"},
    ],
}

PRACTICE: dict[int, list[dict[str, Any]]] = {
    1: [
        {"title": "Nivel 1 · Representación", "purpose": "Consolidar contratos, tipos y expresiones.", "problems": [
            {"prompt": "Define entradas, salida y restricciones para convertir miligramos a gramos.", "solution": "Entrada masa_mg numérica y no negativa; salida masa_g=masa_mg/1000; misma cantidad expresada en gramos."},
            {"prompt": "Predice tipo y valor de 7 // 2, 7 / 2 y 7 % 2.", "solution": "3 int, 3.5 float y 1 int."},
            {"prompt": "Explica por qué sample_id='0042' no debería convertirse necesariamente a int.", "solution": "Es una etiqueta; la conversión perdería ceros iniciales y permitiría operaciones sin significado."},
            {"prompt": "Escribe una expresión para el área de un círculo y prueba radio cero.", "solution": "area=pi*radio**2 con radio>=0; para cero devuelve cero."},
        ]},
        {"title": "Nivel 2 · Validación", "purpose": "Gestionar conversión, dominio y errores.", "problems": [
            {"prompt": "Diseña casos para una función que calcula masa/volumen.", "solution": "Caso normal, masa cero, volumen muy pequeño positivo, volumen cero, valor negativo y texto no numérico."},
            {"prompt": "Corrige una comparación float 0.1+0.2==0.3.", "solution": "Usar math.isclose con tolerancias apropiadas al cálculo."},
            {"prompt": "Distingue None, 0, '' y float('nan').", "solution": "Ausencia explícita, número cero, texto vacío y valor numérico especial no disponible; requieren políticas distintas."},
            {"prompt": "Lee dos cadenas, conviértelas y conserva mensajes diferentes para cada fallo.", "solution": "Convertir cada campo en bloques identificables y encadenar ValueError con el nombre del campo."},
        ]},
        {"title": "Nivel 3 · Depuración", "purpose": "Analizar fallos y reproducibilidad.", "problems": [
            {"prompt": "Clasifica un paréntesis faltante, una división por cero y una fórmula invertida.", "solution": "Error de sintaxis, error de ejecución y error lógico, respectivamente."},
            {"prompt": "Explica cómo reducir una entrada que provoca un fallo.", "solution": "Eliminar elementos irrelevantes conservando el fallo hasta obtener el caso mínimo reproducible."},
            {"prompt": "Propón tres aserciones internas para un cálculo de promedio.", "solution": "Lista no vacía, conteo positivo y resultado dentro del mínimo y máximo para datos finitos."},
            {"prompt": "Documenta versión y comando de ejecución de un script.", "solution": "Registrar python --version, ruta relativa de entrada y comando exacto en README o bitácora."},
        ]},
    ],
    2: [
        {"title": "Nivel 1 · Condiciones", "purpose": "Construir ramas completas y legibles.", "problems": [
            {"prompt": "Escribe una condición para aceptar x en [0,100].", "solution": "0 <= x <= 100."},
            {"prompt": "Construye una tabla de verdad para A and not B.", "solution": "Solo es verdadera cuando A es True y B es False."},
            {"prompt": "Ordena ramas para clasificar negativo, cero y positivo.", "solution": "if x<0; elif x==0; else."},
            {"prompt": "Explica un uso seguro de cortocircuito.", "solution": "if valores and valores[0]>0 evita indexar una lista vacía."},
        ]},
        {"title": "Nivel 2 · Iteración", "purpose": "Usar invariantes y finalización.", "problems": [
            {"prompt": "Suma solo valores numéricos y reporta rechazados.", "solution": "Recorrer, comprobar tipo, acumular suma y contador; devolver ambos."},
            {"prompt": "Define la invariante al buscar el máximo.", "solution": "Tras k elementos, max_actual es el máximo de los k ya procesados."},
            {"prompt": "Transforma un while potencialmente infinito en uno con máximo de intentos.", "solution": "Añadir contador, actualizarlo y exigir contador<limite en la condición."},
            {"prompt": "Compara coste de buscar n identificadores en lista y conjunto.", "solution": "Búsquedas repetidas en lista pueden ser O(n²); construir conjunto y consultar suele ser O(n) promedio total."},
        ]},
        {"title": "Nivel 3 · Decisiones auditables", "purpose": "Diseñar flujos y estados.", "problems": [
            {"prompt": "Crea una tabla de decisión para dato ausente, no numérico, fuera de rango y válido.", "solution": "Cada categoría debe ser excluyente, con acción y mensaje definidos."},
            {"prompt": "Detecta estados imposibles en validado=True, rechazado=True.", "solution": "Ambos no deberían coexistir; usar un único estado enumerado evita la combinación."},
            {"prompt": "Diseña pruebas para un intervalo con límites inclusivos.", "solution": "Un caso interior, ambos límites, justo fuera de cada límite y tipo inválido."},
            {"prompt": "Explica por qué filtrar cambia denominadores.", "solution": "El resultado se calcula sobre menos registros; deben reportarse recibidos, válidos y excluidos."},
        ]},
    ],
    3: [
        {"title": "Nivel 1 · Contratos", "purpose": "Diseñar funciones claras.", "problems": [
            {"prompt": "Diseña la firma de una función que convierte segundos a minutos.", "solution": "def segundos_a_minutos(segundos: float) -> float, con segundos>=0 según contrato."},
            {"prompt": "Distingue print y return en una función de media.", "solution": "return entrega el número; print solo presenta texto."},
            {"prompt": "Identifica el efecto de append sobre una lista recibida.", "solution": "Modifica el objeto externo y constituye un efecto secundario."},
            {"prompt": "Corrige def agregar(x, valores=[]).", "solution": "Usar valores=None y crear una lista dentro cuando sea None."},
        ]},
        {"title": "Nivel 2 · Modularidad", "purpose": "Separar responsabilidades.", "problems": [
            {"prompt": "Divide lectura, validación, cálculo y presentación en funciones.", "solution": "Cada capa recibe y retorna datos explícitos; solo lectura/presentación realizan E/S."},
            {"prompt": "Explica cuándo usar argumento nombrado.", "solution": "Cuando el significado o varias opciones pueden confundirse por posición."},
            {"prompt": "Diseña una excepción con contexto y causa encadenada.", "solution": "Capturar ValueError de float y lanzar ValueError('campo X inválido') from error."},
            {"prompt": "Organiza validation.py, analysis.py y cli.py.", "solution": "validation contiene reglas, analysis cálculos puros y cli interacción/archivos."},
        ]},
        {"title": "Nivel 3 · Pruebas e interfaces", "purpose": "Evaluar composición y mantenibilidad.", "problems": [
            {"prompt": "Escribe pruebas para una función inversa de conversión.", "solution": "Casos conocidos y propiedad inversa dentro de tolerancia."},
            {"prompt": "Detecta acoplamiento en una función que abre una ruta fija.", "solution": "La ruta es dependencia oculta; recibir datos o ruta como argumento facilita pruebas."},
            {"prompt": "Explica por qué devolver None para todo error es ambiguo.", "solution": "None puede ser salida válida y no informa causa; usar excepción o resultado estructurado."},
            {"prompt": "Propón la API mínima de un módulo de resúmenes.", "solution": "Funciones públicas validar_datos y resumir; helpers internos no exportados."},
        ]},
    ],
    4: [
        {"title": "Nivel 1 · Colecciones", "purpose": "Conservar estructura y significado.", "problems": [
            {"prompt": "Elige lista, conjunto o diccionario para una serie temporal.", "solution": "Lista de registros ordenados; un conjunto perdería orden y duplicados."},
            {"prompt": "Detecta aliasing tras b=a; b.append(1).", "solution": "a también cambia porque ambos nombres apuntan a la misma lista."},
            {"prompt": "Explica una copia superficial de lista de diccionarios.", "solution": "La lista exterior es nueva, pero los diccionarios internos siguen compartidos."},
            {"prompt": "Usa un conjunto para detectar identificadores duplicados.", "solution": "Comparar cada id con vistos; si existe, registrar duplicado; si no, añadir."},
        ]},
        {"title": "Nivel 2 · Archivos", "purpose": "Leer y escribir con trazabilidad.", "problems": [
            {"prompt": "Abre un CSV UTF-8 mediante with y pathlib.", "solution": "ruta.open(encoding='utf-8', newline='') dentro de with."},
            {"prompt": "Distingue fila vacía, cero y no aplicable.", "solution": "Son estados semánticos distintos y deben codificarse/documentarse por separado."},
            {"prompt": "Valida columnas obligatorias antes de iterar.", "solution": "Comparar conjunto requerido con fieldnames y fallar si falta alguna."},
            {"prompt": "Diseña una salida que no sobrescriba la fuente.", "solution": "Escribir a directorio processed con nombre/version/hash derivados."},
        ]},
        {"title": "Nivel 3 · Esquema y procedencia", "purpose": "Auditar formatos y transformaciones.", "problems": [
            {"prompt": "Especifica un esquema para muestra, tiempo_s y valor.", "solution": "Tipos, obligatoriedad, unidad de tiempo, rango del valor y unicidad de claves."},
            {"prompt": "Explica por qué un hash no valida calidad.", "solution": "Solo identifica bytes; no demuestra exactitud, licencia ni adecuación científica."},
            {"prompt": "Diseña un manifiesto de datos mínimo.", "solution": "Ruta, hash, tamaño, fecha, licencia, origen y versión de esquema."},
            {"prompt": "Describe una escritura segura.", "solution": "Escribir, cerrar y validar un temporal antes de reemplazar el destino."},
        ]},
    ],
    5: [
        {"title": "Nivel 1 · Tablas y arreglos", "purpose": "Inspeccionar estructura antes de analizar.", "problems": [
            {"prompt": "Distingue shape (10,3) de diez participantes.", "solution": "Shape solo indica diez filas y tres columnas; la unidad de observación debe verificarse."},
            {"prompt": "Explica alineación por índice al sumar Series.", "solution": "pandas empareja etiquetas; índices distintos producen faltantes o reordenación."},
            {"prompt": "Compara count y size en un groupby.", "solution": "count omite NaN de la columna; size cuenta todas las filas."},
            {"prompt": "Convierte una tabla ancha de tiempos a formato largo.", "solution": "Usar melt conservando id y creando columnas tiempo y valor."},
        ]},
        {"title": "Nivel 2 · Resumen", "purpose": "Elegir estadísticas y conservar denominadores.", "problems": [
            {"prompt": "Selecciona media o mediana para distribución muy asimétrica.", "solution": "La mediana es resistente; reportar distribución y, si procede, ambas."},
            {"prompt": "Resume mediciones repetidas sin ponderar más a quien tiene más visitas.", "solution": "Agrega primero por participante o usa un modelo que represente dependencia."},
            {"prompt": "Audita un join que duplica filas.", "solution": "Revisar unicidad de claves y cardinalidad uno-a-uno, uno-a-muchos o muchos-a-muchos."},
            {"prompt": "Documenta un filtro.", "solution": "Registrar regla, filas antes/después y motivos de exclusión."},
        ]},
        {"title": "Nivel 3 · Visualización", "purpose": "Construir figuras honestas y reproducibles.", "problems": [
            {"prompt": "Elige gráfico para trayectorias individuales.", "solution": "Líneas por individuo con orden temporal y resumen opcional."},
            {"prompt": "Explica cuándo una escala log es útil.", "solution": "Para órdenes de magnitud y relaciones multiplicativas, con valores positivos y etiqueta explícita."},
            {"prompt": "Critica una barra de media sin datos ni n.", "solution": "Oculta distribución, tamaño y dependencia; mostrar puntos, intervalos y denominadores."},
            {"prompt": "Define una prueba de reproducibilidad de figura.", "solution": "Recrear desde datos limpios en entorno limpio y comparar archivo/metadatos o elementos esperados."},
        ]},
    ],
    6: [
        {"title": "Nivel 1 · Pruebas", "purpose": "Relacionar requisitos y evidencia.", "problems": [
            {"prompt": "Distingue prueba unitaria, integración y regresión.", "solution": "Componente aislado, interacción de componentes y prevención de un fallo previo."},
            {"prompt": "Selecciona tolerancia para una conversión exacta en float.", "solution": "Usar math.isclose con tolerancia mucho menor que la precisión científicamente relevante."},
            {"prompt": "Convierte un bug en prueba de regresión.", "solution": "Guardar la entrada mínima y el resultado/error esperado antes de corregir."},
            {"prompt": "Escribe una propiedad para normalizar una lista.", "solution": "Si la suma es positiva, la suma de proporciones debe aproximar uno."},
        ]},
        {"title": "Nivel 2 · Proyecto", "purpose": "Organizar entorno e historial.", "problems": [
            {"prompt": "Propón estructura mínima de proyecto.", "solution": "src, tests, README, pyproject/configuración y datos de ejemplo separados."},
            {"prompt": "Divide un cambio en commits revisables.", "solution": "Primero refactor sin cambiar comportamiento, luego funcionalidad y pruebas/documentación."},
            {"prompt": "Explica qué fijar en dependencias.", "solution": "Versiones o rangos compatibles y una forma reproducible de instalar; documentar Python."},
            {"prompt": "Diseña niveles de logging sin datos sensibles.", "solution": "INFO para conteos, WARNING para filas inválidas, ERROR para fallo; usar ids sintéticos o hash seguros."},
        ]},
        {"title": "Nivel 3 · Auditoría", "purpose": "Delimitar calidad y uso.", "problems": [
            {"prompt": "Traza requisito→función→prueba para no sobrescribir datos.", "solution": "Requisito de preservación, función write_output y prueba que verifica fuente intacta y salida nueva."},
            {"prompt": "Explica qué no demuestra CI verde.", "solution": "No demuestra ausencia de fallos, validez científica, seguridad ni utilidad clínica."},
            {"prompt": "Redacta una declaración de finalidad educativa.", "solution": "Indicar datos sintéticos, propósito formativo, usos excluidos y ausencia de validación clínica."},
            {"prompt": "Propón revisión final de reproducibilidad.", "solution": "Clonar limpio, instalar, ejecutar pruebas y pipeline, regenerar resultados y comparar con documentación."},
        ]},
    ],
}

ADDITIONAL_OBJECTIVES: dict[int, list[str]] = {
    1: ["Interpretar tracebacks y clasificar errores de sintaxis, ejecución y lógica.", "Ejecutar un script desde un entorno documentado y reproducir un caso de prueba."],
    2: ["Diseñar tablas de decisión y estados simples antes de implementar ramas complejas.", "Estimar cualitativamente el coste de recorridos y búsquedas repetidas."],
    3: ["Organizar funciones en módulos con interfaces públicas y dependencias explícitas.", "Encadenar excepciones conservando contexto y causa original."],
    4: ["Definir esquemas versionados y manifiestos de procedencia para archivos.", "Aplicar estrategias de escritura que preserven datos originales y salidas válidas."],
    5: ["Inspeccionar forma, dtype, índice y unidad de observación antes del análisis.", "Reconstruir un análisis y una figura desde un estado limpio."],
    6: ["Relacionar requisitos, código, pruebas y cambios mediante trazabilidad.", "Distinguir repetibilidad computacional, reproducibilidad y validación científica."],
}

ADDITIONAL_ERRORS: dict[int, dict[str, str]] = {
    1: {"error": "Ejecutar celdas fuera de orden y asumir que el cuaderno es reproducible.", "correction": "Reiniciar el entorno y ejecutar todo desde un estado limpio."},
    2: {"error": "Usar condiciones con efectos secundarios.", "correction": "Separar la decisión de las modificaciones de estado y documentar cada acción."},
    3: {"error": "Importar un módulo que ejecuta análisis al cargarse.", "correction": "Proteger la ejecución principal y limitar los imports a definiciones."},
    4: {"error": "Aceptar cualquier JSON porque pudo decodificarse.", "correction": "Validar versión, campos, tipos, unidades y restricciones del esquema."},
    5: {"error": "Confiar en la alineación posicional de pandas.", "correction": "Revisar índices y usar merges o reinicios de índice explícitos cuando corresponda."},
    6: {"error": "Mezclar refactorización y cambio de fórmula en un commit.", "correction": "Separar cambios para que la revisión identifique qué alteró el resultado."},
}


def word_count(value: Any) -> int:
    def collect(item: Any, key: str = "") -> list[str]:
        if isinstance(item, str):
            return [] if key == "url" or item.startswith("http") else [item]
        if isinstance(item, list):
            return [text for child in item for text in collect(child, key)]
        if isinstance(item, dict):
            return [text for child_key, child in item.items() for text in collect(child, child_key)]
        return []
    return len(WORD_RE.findall(" ".join(collect(value))))


def upgrade(unit: int) -> dict[str, Any]:
    path = UNIT_DIR / f"unit-{unit:02d}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    meta = META[unit]
    data["schema_version"] = "2.0"
    data["status"] = "review"
    data["estimated_hours"] = meta["hours"]
    data["weeks"] = meta["weeks"]
    data["difficulty"] = meta["difficulty"]
    data["prerequisite_knowledge"] = meta["prerequisites"]
    data["progression"] = {"previous": meta["previous"], "next": meta["next"]}
    data["learning_objectives"].extend(ADDITIONAL_OBJECTIVES[unit])

    for section, paragraph in zip(data["theory_sections"], SECTION_ADDITIONS[unit], strict=True):
        section["paragraphs"].append(paragraph)
    data["theory_sections"].append(NEW_SECTIONS[unit])

    original_example = data.pop("worked_example")
    data["worked_examples"] = [original_example, SECOND_EXAMPLES[unit]]

    original_activity = data.pop("guided_activity")
    original_activity.setdefault("purpose", "Aplicar el contenido mediante un flujo verificable y documentado.")
    original_activity["problems"] = [problem["prompt"] for group in PRACTICE[unit] for problem in group["problems"][:2]]
    data["guided_activities"] = [original_activity]
    data["practice_sets"] = PRACTICE[unit]

    data["common_errors"].append(ADDITIONAL_ERRORS[unit])
    data["self_assessment"].extend(EXTRA_ASSESSMENT[unit])
    data["sources"].extend(EXTRA_SOURCES[unit])
    data["editorial_notice"] = (
        "Material educativo para programación científica y biomédica. Requiere revisión docente experta. "
        "Los ejemplos emplean datos sintéticos o abiertos y no constituyen software clínico validado, "
        "ni deben utilizarse para diagnóstico, triaje, tratamiento o decisiones asistenciales."
    )

    assert data["schema_version"] == "2.0"
    assert data["status"] == "review"
    assert data["estimated_hours"] >= 12
    assert len(data["theory_sections"]) >= 4
    assert all(len(section.get("paragraphs", [])) >= 4 for section in data["theory_sections"])
    assert all(len(section.get("key_points", [])) >= 4 for section in data["theory_sections"])
    assert len(data["worked_examples"]) >= 2
    assert sum(len(group["problems"]) for group in data["practice_sets"]) >= 8
    assert len(data["self_assessment"]) >= 8
    assert len(data["sources"]) >= 5
    assert word_count(data) >= 2000, (unit, word_count(data))
    return data


def main() -> int:
    total = 0
    for unit in range(1, 7):
        data = upgrade(unit)
        total += word_count(data)
        path = UNIT_DIR / f"unit-{unit:02d}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Unidad {unit}: {word_count(data)} palabras")
    assert total >= 15000, total
    print(f"Total Fundamentos de Programación: {total} palabras")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
