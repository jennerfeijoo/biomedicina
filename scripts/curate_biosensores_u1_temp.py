#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biosensores" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biosensores" / "unit-01.json"

unit = json.loads(SOURCE.read_text(encoding="utf-8"))
unit.update({
    "schema_version": "2.0",
    "subject_id": "biosensores",
    "area_id": "ingenieria-biomedica",
    "unit": 1,
    "slug": "arquitectura-de-un-biosensor",
    "title": "Arquitectura de un biosensor",
    "status": "review",
    "purpose": (
        "Construir y auditar la arquitectura funcional de un biosensor distinguiendo muestra y matriz, analito o mensurando, "
        "elemento de reconocimiento biológico, transductor, acondicionamiento, lectura y modelo de respuesta; diseñar controles "
        "básicos y reconocer interferencias y fallos sin confundir una señal detectable con selectividad analítica, validez clínica "
        "o utilidad diagnóstica."
    ),
    "learning_objectives": [
        "Distinguir muestra, matriz, analito y mensurando y explicar por qué definirlos precede a seleccionar el elemento de reconocimiento o el transductor.",
        "Representar un biosensor como una cadena funcional que conecta reconocimiento biológico, transducción, acondicionamiento, lectura y resultado mediante entradas, salidas y unidades explícitas.",
        "Diferenciar la selectividad aportada por el reconocimiento de la respuesta física del transductor y distinguir medición directa, indirecta y sistemas bioanalíticos con procesamiento adicional.",
        "Aplicar un modelo local de respuesta y una calibración elemental para estimar una cantidad dentro del intervalo justificado, detectando desviaciones por no linealidad o saturación.",
        "Diseñar blancos, controles negativos, positivos o de referencia y condiciones de interferencia que permitan localizar fallos en la cadena del biosensor.",
        "Construir un expediente sintético reproducible de arquitectura de biosensor que separe observación, cálculo, inferencia y decisión y limite sus afirmaciones al uso previsto evaluado."
    ],
    "theory_sections": [
        {
            "heading": "1. ¿Qué es un biosensor y dónde empieza y termina el sistema?",
            "paragraphs": [
                "Un biosensor combina reconocimiento de origen biológico con una forma de transducción capaz de producir una señal medible. Esta idea parece simple, pero obliga a declarar la frontera del sistema. El objeto de interés no es únicamente una molécula ni únicamente un electrodo: es una cadena funcional en la que una muestra entra bajo condiciones definidas, una interacción o reacción aporta información química o bioquímica, un transductor convierte esa información en una magnitud accesible y una etapa de lectura entrega un resultado interpretable. Dibujar esa frontera evita llamar biosensor a cualquier ensayo que incluya biología y electrónica sin especificar cómo se conectan.",
                "Antes de elegir una arquitectura se debe distinguir muestra, matriz, analito y mensurando. La muestra es la porción material sometida al procedimiento y la matriz comprende sus demás componentes. El analito es el componente o especie de interés, mientras que el mensurando debe describir con suficiente precisión la cantidad que se pretende determinar, incluidas condiciones relevantes cuando corresponda. En un ejercicio educativo sobre lactato, por ejemplo, decir solo «medir lactato» es incompleto: conviene declarar una concentración en una matriz artificial, un intervalo de trabajo y un procedimiento de lectura. Esta precisión impide que una etiqueta química sustituya a una especificación de medición.",
                "La definición clásica de IUPAC del biosensor destaca reacciones bioquímicas específicas y señales eléctricas, térmicas u ópticas. Las recomendaciones de Thévenot y colaboradores para biosensores electroquímicos añaden una frontera útil: un biosensor integrado y autocontenido se distingue de un sistema bioanalítico que necesita pasos adicionales de procesamiento o adición de reactivos. Esa distinción es contextual y no debe usarse como una etiqueta de prestigio. Lo importante en ingeniería es documentar qué etapas están físicamente integradas, cuáles ocurren fuera del dispositivo y qué transformación aporta cada etapa al resultado final.",
                "El uso previsto condiciona toda la arquitectura. Un sistema destinado a demostrar un principio en una matriz artificial, otro destinado a monitorización ambiental y otro evaluado para una decisión clínica pueden compartir un mecanismo de reconocimiento y, sin embargo, requerir especificaciones, controles y evidencia muy diferentes. Por eso esta unidad no tratará «detectar una señal» como sinónimo de «detectar específicamente el analito», y tampoco presentará una respuesta frente a estándares como validación en muestras clínicas. La arquitectura se considera suficiente solo cuando sus entradas, transformaciones, salidas, supuestos y límites pueden ser examinados por otra persona."
            ],
            "key_points": [
                "Un biosensor es una cadena funcional integrada; su frontera debe declararse antes de evaluar el desempeño.",
                "Muestra, matriz, analito y mensurando describen entidades distintas y no deben intercambiarse como sinónimos.",
                "La integración del reconocimiento y la transducción no elimina pasos de acondicionamiento, calibración o interpretación.",
                "El uso previsto determina qué evidencia y qué controles son suficientes para sostener una afirmación."
            ]
        },
        {
            "heading": "2. Elemento de reconocimiento, transductor y cadena de señal",
            "paragraphs": [
                "El elemento de reconocimiento biológico aporta una interacción con selectividad definida en el dominio bioquímico. IUPAC incluye entre los ejemplos biocatalizadores, receptores inmunitarios y ácidos nucleicos. La palabra «reconocimiento» no significa selectividad perfecta: una enzima puede reaccionar con más de un sustrato, un anticuerpo puede presentar reactividad cruzada y una matriz compleja puede modificar disponibilidad o unión. La pregunta de diseño es qué interacción se espera, qué especies alternativas podrían producir una respuesta y qué control permitiría distinguirlas. Los mecanismos concretos de enzimas, anticuerpos, ácidos nucleicos y aptámeros se desarrollarán en la unidad 2.",
                "El transductor cumple otra función. En la terminología de sensores químicos, receptor y transductor son unidades funcionales diferentes: el receptor transforma información química y el transductor genera una señal analítica a partir de la magnitud resultante. Un transductor no adquiere selectividad biológica por sí solo. La misma plataforma electroquímica u óptica puede responder a fenómenos no específicos, cambios de temperatura, ensuciamiento o especies interferentes. Por tanto, observar corriente, potencial, intensidad óptica, frecuencia o temperatura no demuestra qué componente molecular originó la señal; esa atribución necesita el diseño del reconocimiento y controles adecuados.",
                "Entre el transductor y el resultado puede existir una cadena de señal: excitación cuando aplique, conversión, amplificación, filtrado, digitalización, compensación, cálculo y presentación. Para razonar sobre ella es útil un modelo por bloques, no una ecuación física universal: la entrada química modifica una respuesta de reconocimiento R(c), la transducción T y una ganancia global G contribuyen a la salida, mientras un término basal y el ruido también afectan la observación. Este modelo ayuda a localizar dónde podría surgir una diferencia, pero cada arquitectura real requiere ecuaciones y parámetros específicos que se estudiarán con mayor detalle al tratar los modos de transducción.",
                "Una medición puede ser directa respecto del analito o indirecta respecto de una especie consumida, producida, inhibida o activada por la interacción biológica. Esta diferencia modifica la inferencia. Si una enzima produce una especie electroactiva y el electrodo responde a esa especie, el transductor no está observando la molécula objetivo de manera directa; el vínculo se sostiene mediante el mecanismo bioquímico y sus condiciones. Documentar esa cadena evita una frase frecuente pero imprecisa: «el sensor mide la molécula». Una descripción más rigurosa especifica qué fenómeno reconoce el biocomponente, qué magnitud detecta el transductor y qué modelo relaciona esa salida con el mensurando."
            ],
            "equations": [
                {
                    "latex": "y = G\\,T\\!\\left[R(c)\\right] + b + n",
                    "meaning": "Modelo conceptual por bloques: no es una ley universal; representa reconocimiento, transducción, ganancia, basal y ruido para localizar dependencias de la salida.",
                    "variables": {
                        "c": "cantidad o concentración de interés en el modelo",
                        "R(c)": "respuesta del elemento de reconocimiento bajo condiciones definidas",
                        "T": "transformación del transductor",
                        "G": "ganancia o escala global de la cadena",
                        "b": "componente basal",
                        "n": "ruido o perturbación no modelada"
                    }
                }
            ],
            "key_points": [
                "El reconocimiento biológico y la transducción cumplen funciones distintas y deben auditarse por separado.",
                "Selectividad de reconocimiento no equivale a ausencia de reactividad cruzada o interferencias de matriz.",
                "La salida observada puede incluir basal, ruido y transformaciones posteriores al transductor.",
                "Una medición indirecta requiere declarar la cadena mecanística que conecta la salida con el analito o mensurando."
            ]
        },
        {
            "heading": "3. Modelo de respuesta y calibración básica",
            "paragraphs": [
                "Un biosensor cuantitativo necesita relacionar una salida con valores conocidos de una cantidad de referencia. En un intervalo limitado puede ser razonable aproximar la respuesta con una recta y = b + S c, donde S es una sensibilidad local de calibración y b representa la respuesta basal. Este modelo sirve para aprender la arquitectura de una calibración, pero no debe convertirse en la afirmación de que todo biosensor es lineal. Cinética de unión, agotamiento de reactivos, saturación del transductor, limitaciones de transporte, electrónica y algoritmos pueden curvar la relación o producir regiones con distinta sensibilidad.",
                "La calibración exige conservar condiciones comparables: matriz, temperatura, tiempo de incubación, volumen, geometría, lote, protocolo y configuración de lectura pueden afectar la respuesta. Si los estándares se preparan en un medio simple y la muestra pertenece a una matriz compleja, una recta ajustada con precisión puede seguir siendo inapropiada para esa muestra. La unidad 5 abordará de manera específica selectividad, sensibilidad, intervalo, límites de detección y cuantificación, precisión y comparación con métodos de referencia. Aquí el objetivo es más básico: reconocer que una cifra obtenida por inversión de una curva depende del modelo y del contexto que produjeron esa curva.",
                "Cuando el modelo local es lineal, una respuesta desconocida puede transformarse en una estimación mediante ĉ = (y-b)/S. La operación algebraica es sencilla; la decisión difícil es si la respuesta desconocida está dentro del intervalo justificado y si las condiciones son comparables. Extrapolar más allá del último estándar o usar una respuesta próxima a saturación añade dependencia de un modelo que no ha sido comprobado. Por eso cada estimación debe acompañarse de la ubicación dentro del intervalo, la unidad de c y una advertencia cuando el dato sugiera no linealidad.",
                "La terminología metrológica moderna separa características de desempeño de un procedimiento y la incertidumbre de un resultado. Esta distinción evita usar «sensibilidad» como una palabra genérica para calidad, o interpretar una pendiente alta como garantía de exactitud, selectividad o utilidad. En esta unidad, la pendiente describe cuánto cambia la salida por unidad de entrada dentro del modelo adoptado. Para comparar arquitecturas se deben observar además el basal, el ruido, los controles, la estabilidad y la respuesta a interferentes. Un único número no resume la calidad de un biosensor."
            ],
            "equations": [
                {
                    "latex": "y = b + S c",
                    "meaning": "Modelo lineal local de calibración. Solo debe usarse en un intervalo y bajo condiciones donde la aproximación haya sido justificada.",
                    "variables": {
                        "y": "respuesta medida",
                        "b": "intercepto o respuesta basal",
                        "S": "pendiente o sensibilidad local de calibración",
                        "c": "cantidad o concentración de referencia"
                    }
                },
                {
                    "latex": "\\hat{c} = \\frac{y-b}{S}",
                    "meaning": "Estimación inversa bajo el modelo lineal local; no autoriza extrapolación ni corrige por sí sola efectos de matriz o interferencias.",
                    "variables": {
                        "\\hat{c}": "cantidad estimada",
                        "y": "respuesta del desconocido",
                        "b": "intercepto de la calibración",
                        "S": "pendiente de la calibración"
                    }
                }
            ],
            "key_points": [
                "Una curva de calibración es parte de un procedimiento y depende de condiciones experimentales declaradas.",
                "La linealidad es una aproximación local que debe comprobarse; no es una propiedad universal de los biosensores.",
                "Invertir una curva no resuelve problemas de matriz, interferencia, saturación o transferencia entre protocolos.",
                "Sensibilidad de calibración, selectividad, incertidumbre y utilidad son dimensiones diferentes."
            ]
        },
        {
            "heading": "4. Controles, interferencias, fallos e interpretación proporcional",
            "paragraphs": [
                "Los controles convierten una arquitectura en una hipótesis comprobable. Un blanco permite observar respuesta basal asociada a reactivos, matriz o instrumentación sin la cantidad objetivo añadida; un control negativo puede retirar o inactivar el componente de reconocimiento para explorar respuesta no específica; un control positivo o de referencia confirma que una etapa capaz de producir señal sigue funcionando. Ningún control es universal. Debe seleccionarse según la ruta causal que se quiere examinar y debe definirse de antemano qué patrón apoyaría o cuestionaría la interpretación principal.",
                "Una interferencia es relevante cuando modifica la respuesta o la inferencia en condiciones plausibles para la muestra y el uso. Puede actuar en el reconocimiento, en el transporte, en la superficie del transductor, en la reacción electroquímica u óptica o en el procesamiento. También puede existir deriva temporal, ensuciamiento, memoria, saturación o pérdida de actividad biológica. Localizar el nivel del fallo es más informativo que etiquetar todo desvío como «ruido». Un buen expediente muestra la cadena y anota en cada bloque fallos posibles, observables de diagnóstico y controles discriminantes.",
                "El desempeño de una arquitectura en estándares o datos sintéticos es evidencia técnica limitada al experimento. No demuestra por sí solo validez en muestras reales, precisión entre lotes, robustez de fabricación, estabilidad de almacenamiento, seguridad, beneficio clínico o aptitud regulatoria. Incluso una respuesta claramente dependiente de concentración puede provenir de una vía distinta de la pretendida si faltan controles de reconocimiento e interferencia. La conclusión debe indicar qué se midió directamente, qué se calculó con la calibración y qué explicación sigue siendo inferida.",
                "La práctica responsable consiste en formular la conclusión más fuerte que la evidencia permite y no una más atractiva. En un ejercicio sintético es legítimo decir que una arquitectura produjo una respuesta aproximadamente proporcional dentro de 0–4 mM y que un interferente modificó la salida. No sería legítimo concluir que el dispositivo diagnostica una enfermedad, que funciona en sangre humana o que es seguro para uso clínico. Esas afirmaciones necesitan diseños y evidencia adicionales. Esta frontera entre señal técnica y consecuencia biomédica se mantendrá durante todo el curso."
            ],
            "key_points": [
                "Cada control debe corresponder a una hipótesis de fallo concreta y a un resultado esperado predefinido.",
                "Interferencias pueden surgir en reconocimiento, transporte, transducción, superficie o procesamiento.",
                "Una respuesta en estándares o matrices sintéticas no equivale a validación en muestras clínicas.",
                "La conclusión debe separar observación, cálculo, mecanismo inferido y decisión fuera de alcance."
            ]
        }
    ],
    "glossary": [
        {"term": "Biosensor", "definition": "Dispositivo que integra reconocimiento biológico y transducción para producir información analítica a partir de una interacción bioquímica bajo condiciones definidas."},
        {"term": "Muestra", "definition": "Porción material sometida al procedimiento de medición o análisis; su preparación y procedencia condicionan la interpretación."},
        {"term": "Matriz", "definition": "Conjunto de componentes de la muestra distintos del analito que pueden influir en reconocimiento, transporte, transducción o lectura."},
        {"term": "Analito", "definition": "Componente o especie química o bioquímica de interés en un procedimiento analítico; no sustituye la especificación completa del mensurando."},
        {"term": "Mensurando", "definition": "Cantidad que se pretende medir, descrita con las condiciones necesarias para que su significado sea suficientemente específico."},
        {"term": "Elemento de reconocimiento biológico", "definition": "Componente de origen biológico o derivado de él que aporta una interacción selectiva y traduce información del dominio bioquímico hacia una forma física o química susceptible de transducción."},
        {"term": "Transductor", "definition": "Elemento que proporciona una cantidad de salida relacionada con una cantidad de entrada; en un biosensor convierte el fenómeno asociado al reconocimiento en una señal accesible."},
        {"term": "Señal analítica", "definition": "Magnitud observable generada por la cadena de medición y usada para obtener información sobre la cantidad de interés mediante un modelo o procedimiento."},
        {"term": "Acondicionamiento de señal", "definition": "Transformaciones aplicadas a la salida del transductor, como amplificación, filtrado, compensación o digitalización, antes del cálculo o presentación."},
        {"term": "Lectura", "definition": "Representación final de la señal o del resultado calculado que el sistema entrega al usuario o a una etapa posterior."},
        {"term": "Función de respuesta", "definition": "Relación entre la salida del sistema y una cantidad de entrada bajo condiciones definidas; puede ser lineal o no lineal."},
        {"term": "Calibración", "definition": "Operación que establece una relación entre valores de referencia y las indicaciones correspondientes para permitir obtener resultados a partir de indicaciones."},
        {"term": "Blanco", "definition": "Condición preparada para caracterizar una respuesta basal o contribuciones ajenas a la cantidad objetivo, según el diseño del procedimiento."},
        {"term": "Control negativo", "definition": "Condición diseñada para no contener o no activar el mecanismo específico que se quiere demostrar y que permite detectar respuesta no específica o contaminación."},
        {"term": "Control positivo", "definition": "Condición que debe producir una respuesta conocida y que comprueba que una etapa o cadena puede funcionar bajo el protocolo."},
        {"term": "Interferencia", "definition": "Componente o condición que modifica la respuesta o la inferencia sobre la cantidad objetivo de una forma relevante para el procedimiento."},
        {"term": "Selectividad", "definition": "Capacidad de un procedimiento o elemento de reconocimiento para obtener información sobre una cantidad de interés en presencia de otras cantidades o componentes relevantes."},
        {"term": "Sensibilidad de calibración", "definition": "Cambio de la indicación respecto del cambio de la cantidad medida; en una región lineal corresponde a la pendiente local de calibración."},
        {"term": "Uso previsto", "definition": "Propósito y contexto para los cuales se pretende interpretar una salida; determina requisitos, controles y evidencia necesaria."},
        {"term": "Sistema bioanalítico", "definition": "Conjunto de operaciones bioanalíticas que puede incluir pasos externos adicionales de procesamiento o reactivos y que no debe confundirse automáticamente con un biosensor integrado."}
    ],
    "worked_examples": [
        {
            "title": "Del ensayo general a una arquitectura de biosensor",
            "scenario": "Se propone detectar lactato en una matriz artificial con una enzima y un electrodo, pero la propuesta solo enumera componentes sin explicar la cadena funcional.",
            "reasoning_steps": [
                "Definir la entrada como una concentración de lactato en matriz artificial y fijar el intervalo educativo que se estudiará.",
                "Ubicar la enzima como elemento de reconocimiento biocatalítico y declarar qué reacción o especie secundaria conecta el lactato con la transducción.",
                "Ubicar el electrodo como transductor y especificar qué magnitud eléctrica produce como salida.",
                "Añadir acondicionamiento y lectura sin atribuir a esas etapas la selectividad que corresponde al reconocimiento y al protocolo.",
                "Definir blanco, control sin enzima y condición con interferente antes de interpretar una curva de respuesta."
            ],
            "interpretation": "La arquitectura es auditable porque cada bloque tiene una función y una salida; todavía no demuestra desempeño clínico ni selectividad en matrices biológicas reales.",
            "limitations": [
                "El ejemplo no prescribe un diseño de glucosa o lactato clínico real.",
                "No se evalúan estabilidad, fabricación ni validación analítica completa."
            ]
        },
        {
            "title": "Reconocimiento de afinidad y transducción no son la misma evidencia",
            "scenario": "Un receptor de afinidad se une a un analito y un transductor óptico registra un cambio de intensidad. El equipo afirma que el aumento óptico prueba por sí solo unión específica.",
            "reasoning_steps": [
                "Separar la hipótesis de unión específica de la observación física de intensidad.",
                "Identificar respuestas alternativas: adsorción no específica, cambio de índice de refracción, deriva o variación de iluminación.",
                "Añadir una condición sin receptor funcional y una molécula interferente estructuralmente relacionada.",
                "Interpretar el transductor como detector del fenómeno óptico, no como fuente automática de selectividad molecular."
            ],
            "interpretation": "La señal óptica es compatible con la hipótesis de reconocimiento, pero la atribución molecular depende del conjunto de controles.",
            "limitations": ["No se comparan químicas de afinidad específicas; ese detalle pertenece a la unidad 2."]
        },
        {
            "title": "¿Biosensor integrado o sistema bioanalítico más amplio?",
            "scenario": "Un protocolo requiere incubar la muestra, añadir dos reactivos en tubos separados, lavar y luego introducir el producto en un lector electrónico.",
            "reasoning_steps": [
                "Dibujar todos los pasos desde muestra hasta señal y no solo el lector final.",
                "Identificar qué etapas de reconocimiento y preparación ocurren fuera del elemento de transducción.",
                "Comparar la arquitectura con la recomendación de distinguir un biosensor integrado de sistemas que requieren procesamiento adicional.",
                "Describir el sistema por sus operaciones reales en lugar de forzar una etiqueta."
            ],
            "interpretation": "La denominación debe reflejar el grado de integración; la utilidad del sistema no depende de que reciba o no la etiqueta de biosensor.",
            "limitations": ["La frontera exacta puede variar con definiciones y tecnologías; debe citarse la convención usada."]
        },
        {
            "title": "Diagnóstico de una cadena con deriva e interferencia",
            "scenario": "En datos sintéticos el blanco permanece cerca de 0.10 unidades, la respuesta aumenta hasta 4 mM, pero 8 mM se desvía de la tendencia y un interferente eleva la respuesta de una muestra de 2 mM.",
            "reasoning_steps": [
                "Usar el blanco para estimar si existe una gran contribución basal en el ejemplo.",
                "Ajustar conceptualmente la región 0–4 mM antes de utilizar la respuesta de 8 mM como si fuera lineal.",
                "Tratar el cambio con interferente como evidencia contra la idea de una respuesta completamente específica bajo esas condiciones.",
                "Separar no linealidad de rango y falta de selectividad porque son mecanismos de fallo diferentes."
            ],
            "interpretation": "La cadena puede ser útil para estudiar calibración local, pero necesita caracterización adicional antes de extrapolar o atribuir toda la señal al analito.",
            "limitations": ["Los valores son sintéticos y no representan desempeño de un dispositivo comercial o clínico."]
        }
    ],
    "guided_activities": [
        {
            "title": "Actividad guiada: expediente sintético de arquitectura de un biosensor para lactato",
            "instructions": [
                "Trabaja únicamente con los datos sintéticos proporcionados; no recolectes muestras humanas, no grabes participantes y no uses datos personales.",
                "Define primero el uso educativo: estimar lactato en una matriz artificial entre 0 y 4 mM para estudiar la arquitectura, no diagnosticar ni monitorizar a una persona.",
                "Usa la tabla sintética de calibración: c (mM) = [0, 1, 2, 4, 8] y y (u.a.) = [0.10, 0.78, 1.48, 2.90, 5.20]. Los blancos replicados son [0.09, 0.11, 0.10].",
                "Para el cálculo guiado usa solo 0–4 mM como región local de trabajo y aproxima la pendiente con los extremos: S=(2.90-0.10)/(4-0)=0.70 u.a./mM y b=0.10 u.a.",
                "Considera además un desconocido sintético con y=1.83 u.a. y una condición de 2 mM + interferente con y=1.82 u.a.; registra qué observación apoya o cuestiona cada inferencia.",
                "Entrega el expediente con diagrama, cálculos, controles, tabla de fallos y una conclusión limitada al experimento sintético."
            ],
            "problems": [
                "Escribe el uso previsto, la matriz artificial, el analito y un mensurando suficientemente específico para el ejercicio.",
                "Dibuja una cadena funcional con al menos: muestra → reconocimiento → transducción → acondicionamiento/lectura → resultado; indica una entrada y una salida para cada bloque.",
                "Explica qué parte de la cadena podría aportar selectividad y por qué el transductor no demuestra por sí solo identidad molecular.",
                "Con S=0.70 u.a./mM y b=0.10 u.a., calcula la concentración estimada del desconocido y conserva unidades.",
                "Compara la respuesta de 8 mM con la extrapolación lineal y explica por qué no debe usarse automáticamente la misma relación fuera del intervalo adoptado.",
                "Calcula la media simple de los tres blancos y explica qué información aporta y qué información no aporta sobre selectividad.",
                "Compara el valor de 2 mM sin interferente (1.48) con el de 2 mM + interferente (1.82) y formula una hipótesis de fallo sin afirmar el mecanismo como probado.",
                "Propón un control negativo de reconocimiento, un control positivo o de referencia y una condición de interferencia; para cada uno escribe el patrón esperado.",
                "Construye una tabla con cuatro localizaciones posibles de fallo: reconocimiento, transductor, acondicionamiento y modelo de calibración; añade un observable o prueba para cada una.",
                "Compara esta arquitectura con una alternativa que use otro modo de transducción, manteniendo constante el problema analítico, e indica qué aspectos tendrían que revalidarse.",
                "Clasifica como observación, cálculo, inferencia o decisión cada una de estas frases: «y=1.83», «ĉ≈2.47 mM», «la respuesta es específica para lactato», «el dispositivo serviría para diagnóstico».",
                "Redacta una conclusión de máximo 120 palabras que diga qué funcionó en el ejercicio, qué falló o quedó incierto y qué evidencia sería necesaria para avanzar."
            ],
            "deliverables": [
                "Ficha de uso previsto, muestra/matriz, analito y mensurando.",
                "Diagrama de bloques con entradas, salidas y unidades.",
                "Tabla de calibración local y cálculo del desconocido.",
                "Análisis del blanco, la posible no linealidad y la interferencia.",
                "Matriz control → hipótesis de fallo → resultado esperado.",
                "Tabla de localización de fallos y pruebas discriminantes.",
                "Comparación breve con una arquitectura alternativa.",
                "Conclusión limitada y lista de evidencia pendiente."
            ],
            "checking_criteria": [
                "El uso previsto está limitado a una matriz artificial y no contiene afirmaciones diagnósticas o terapéuticas.",
                "Analito, mensurando, muestra y matriz están diferenciados explícitamente.",
                "El diagrama separa reconocimiento, transducción, acondicionamiento y resultado.",
                "El cálculo del desconocido usa el modelo local con unidades y no extrapola sin justificación.",
                "La desviación a 8 mM se reconoce como señal de que el modelo lineal local puede no transferirse.",
                "El efecto del interferente se interpreta como una amenaza a la inferencia y no como un mecanismo molecular demostrado.",
                "Cada control tiene una hipótesis y un patrón esperado predefinidos.",
                "Las posibles fuentes de fallo se localizan por bloque en vez de agruparse como ruido genérico.",
                "Observaciones, cálculos, inferencias y decisiones se mantienen separados.",
                "La conclusión declara límites y siguiente evidencia necesaria para cualquier uso más exigente."
            ]
        }
    ],
    "common_errors": [
        {"error": "Usar analito y mensurando como sinónimos.", "correction": "Definir la especie de interés y, por separado, la cantidad concreta que se pretende medir bajo condiciones declaradas."},
        {"error": "Afirmar que el transductor aporta selectividad molecular por sí solo.", "correction": "Separar la función de reconocimiento de la conversión física y comprobar respuestas no específicas con controles."},
        {"error": "Llamar biosensor solo al lector electrónico y omitir preparación o reconocimiento externos.", "correction": "Dibujar la cadena completa y declarar la frontera de integración usada."},
        {"error": "Asumir linealidad en todo el rango porque cinco puntos producen una tendencia ascendente.", "correction": "Justificar un intervalo local y revisar saturación o curvatura antes de invertir la respuesta."},
        {"error": "Confundir pendiente de calibración con calidad global del biosensor.", "correction": "Evaluar selectividad, basal, ruido, estabilidad, rango y controles como dimensiones diferentes."},
        {"error": "Interpretar un blanco bajo como prueba de selectividad.", "correction": "Un blanco informa sobre basal bajo esa condición; la selectividad requiere desafíos con interferentes y controles de reconocimiento."},
        {"error": "Etiquetar todo desvío como ruido.", "correction": "Localizar si el fallo proviene de reconocimiento, matriz, superficie, transducción, electrónica o modelo."},
        {"error": "Pasar de una curva sintética o de estándar a una afirmación clínica.", "correction": "Restringir la conclusión a las condiciones evaluadas y separar desempeño técnico de evidencia clínica o regulatoria."}
    ],
    "self_assessment": [
        {"question": "¿Por qué «lactato» no especifica por sí solo el mensurando?", "answer": "Porque identifica una especie o analito, pero faltan la cantidad, matriz y condiciones relevantes que definen qué se pretende medir.", "explanation": "Una medición reproducible necesita una especificación suficientemente precisa del objeto cuantitativo.", "common_error": "Responder que analito y mensurando son siempre equivalentes."},
        {"question": "¿Qué función principal aporta el elemento de reconocimiento biológico?", "answer": "Relaciona la presencia o actividad del objetivo con una interacción bioquímica dotada de selectividad definida y accesible a una etapa de transducción.", "explanation": "La selectividad no es perfecta y debe comprobarse frente a alternativas pertinentes.", "common_error": "Afirmar que elimina toda interferencia de la matriz."},
        {"question": "¿Qué hace el transductor y qué no demuestra por sí solo?", "answer": "Convierte una magnitud de entrada en una salida relacionada; por sí solo no demuestra la identidad molecular que originó esa entrada.", "explanation": "La atribución molecular depende del reconocimiento, del protocolo y de controles.", "common_error": "Confundir señal eléctrica u óptica con reconocimiento específico."},
        {"question": "¿Cuándo es razonable usar y=b+Sc?", "answer": "Cuando una relación lineal local ha sido justificada dentro de un intervalo y bajo condiciones comparables.", "explanation": "La ecuación es una aproximación de calibración, no una ley universal de biosensores.", "common_error": "Extrapolar a cualquier concentración porque la pendiente ya fue calculada."},
        {"question": "¿Qué información aporta un blanco?", "answer": "Ayuda a caracterizar respuesta basal o contribuciones presentes en ausencia de la cantidad objetivo según el diseño del procedimiento.", "explanation": "No prueba por sí solo que el reconocimiento sea selectivo.", "common_error": "Concluir selectividad porque el blanco es pequeño."},
        {"question": "¿Por qué una condición con interferente es útil?", "answer": "Porque prueba si otra especie o condición relevante modifica la respuesta y cuestiona la atribución exclusiva al objetivo.", "explanation": "El resultado debe interpretarse dentro de una matriz y concentración definidas.", "common_error": "Generalizar una sola interferencia ensayada a todas las posibles interferencias."},
        {"question": "¿Cuál es la diferencia entre un biosensor integrado y un sistema bioanalítico con procesamiento adicional?", "answer": "La diferencia se refiere a la frontera e integración de reconocimiento, transducción y operaciones necesarias para producir la información analítica.", "explanation": "La etiqueta no determina por sí sola calidad o utilidad.", "common_error": "Suponer que cualquier lector utilizado después de un ensayo convierte todo el protocolo en biosensor."},
        {"question": "Si el punto de 8 mM se desvía de la recta local 0–4 mM, ¿qué conclusión mínima corresponde?", "answer": "Que la aproximación lineal local no debe extenderse automáticamente a 8 mM y que se necesita caracterizar la respuesta en esa región.", "explanation": "La desviación puede tener varias causas y no identifica una por sí sola.", "common_error": "Afirmar inmediatamente que el transductor está averiado."},
        {"question": "¿Qué diferencia hay entre observar y=1.83 y estimar ĉ=2.47 mM?", "answer": "La primera es una indicación observada; la segunda es un cálculo dependiente de una calibración y de sus supuestos.", "explanation": "Separar observación y cálculo hace visible la dependencia del modelo.", "common_error": "Tratar la concentración estimada como una observación directa."},
        {"question": "¿Qué falta para afirmar que un biosensor sintético es útil clínicamente?", "answer": "Evidencia apropiada para el uso clínico: desempeño en muestras y condiciones relevantes, validación del procedimiento, robustez, seguridad y evaluación del contexto de decisión, entre otros requisitos aplicables.", "explanation": "Una demostración técnica no sustituye una validación clínica o regulatoria.", "common_error": "Usar una buena curva de calibración como evidencia suficiente de utilidad clínica."}
    ],
    "biomedical_connections": [
        {"topic": "Monitorización metabólica", "connection": "La arquitectura de reconocimiento y transducción permite razonar sobre sensores de metabolitos sin asumir que una demostración educativa reproduce un dispositivo clínico."},
        {"topic": "Diagnóstico in vitro", "connection": "Separar analito, matriz, calibración y controles es requisito conceptual para evaluar ensayos, aunque la validación clínica y regulatoria excede esta unidad."},
        {"topic": "Point-of-care", "connection": "La integración de muestra, reconocimiento, transducción y lectura condiciona usabilidad y flujo, que se abordarán con mayor profundidad en la unidad 6."},
        {"topic": "Wearables", "connection": "La frontera entre señal, calibración, interferencias y decisión es esencial cuando la medición ocurre de forma repetida o continua, sin que ello pruebe equivalencia con una variable clínica."},
        {"topic": "Medicina personalizada", "connection": "Un biosensor puede aportar datos a una decisión, pero la utilidad de personalizar una intervención requiere evidencia clínica adicional y un contexto de decisión definido."}
    ],
    "sources": [
        {
            "title": "IUPAC Gold Book: biosensor",
            "organization": "International Union of Pure and Applied Chemistry",
            "year": 2025,
            "url": "https://goldbook.iupac.org/terms/view/B00663",
            "type": "terminología oficial",
            "description": "Definición de biosensor en el Gold Book, con fuente original IUPAC Recommendations 1992.",
            "verification_status": "verified_directly",
            "locator": "Gold Book term B00663",
            "limitations": "La entrada remite a una definición histórica; debe leerse junto con terminología y recomendaciones posteriores."
        },
        {
            "title": "IUPAC Gold Book: biological recognition element",
            "organization": "International Union of Pure and Applied Chemistry",
            "year": 2025,
            "url": "https://goldbook.iupac.org/terms/view/09655",
            "type": "terminología oficial",
            "description": "Define el elemento de reconocimiento biológico y enumera categorías de reconocimiento.",
            "verification_status": "verified_directly",
            "locator": "Gold Book term 09655; source PAC 2018, 90, 1121",
            "limitations": "La definición no caracteriza por sí sola desempeño o selectividad de un bioreceptor concreto."
        },
        {
            "title": "Chemical sensors: definitions and classification",
            "organization": "IUPAC / Pure and Applied Chemistry",
            "year": 1991,
            "url": "https://publications.iupac.org/pac/63/9/1247/index.html",
            "doi": "10.1351/pac199163091247",
            "type": "recomendación terminológica",
            "description": "Distingue las unidades funcionales receptor y transductor en sensores químicos y describe la conversión a señal analítica.",
            "verification_status": "verified_directly",
            "locator": "Pure Appl Chem. 1991;63(9):1247-1250",
            "limitations": "Clasificación histórica; tecnologías posteriores añaden arquitecturas y modalidades, pero la separación funcional sigue siendo útil."
        },
        {
            "title": "Electrochemical biosensors: recommended definitions and classification",
            "organization": "Biosensors and Bioelectronics / IUPAC",
            "year": 2001,
            "url": "https://pubmed.ncbi.nlm.nih.gov/11261847/",
            "pmid": "11261847",
            "doi": "10.1016/S0956-5663(01)00115-4",
            "type": "recomendación y artículo técnico",
            "description": "Recomendaciones de definición, integración, clasificación y criterios de desempeño para biosensores electroquímicos.",
            "verification_status": "verified_directly",
            "locator": "Biosens Bioelectron. 2001;16(1-2):121-131; PMID 11261847",
            "limitations": "Se centra en biosensores electroquímicos; la unidad usa sus fronteras conceptuales sin generalizar todos sus detalles a otras transducciones."
        },
        {
            "title": "IUPAC Gold Book: transducer",
            "organization": "International Union of Pure and Applied Chemistry",
            "url": "https://goldbook.iupac.org/terms/view/T06437",
            "type": "terminología oficial",
            "description": "Define transductor como instrumento que proporciona una cantidad de salida relacionada con una cantidad de entrada.",
            "verification_status": "verified_directly",
            "locator": "Gold Book term T06437; source PAC 1989, 61, 1657",
            "limitations": "Definición instrumental general; el mecanismo específico depende de la modalidad de transducción."
        },
        {
            "title": "Biosensors: sense and sensibility",
            "organization": "Chemical Society Reviews",
            "year": 2013,
            "url": "https://pubmed.ncbi.nlm.nih.gov/23420144/",
            "pmid": "23420144",
            "doi": "10.1039/C3CS35528D",
            "type": "revisión",
            "description": "Revisión del desarrollo del campo, logros, aplicaciones y retos de los biosensores.",
            "verification_status": "verified_directly",
            "locator": "Chem Soc Rev. 2013;42(8):3184-3196; PMID 23420144",
            "limitations": "Es una revisión panorámica y no sustituye recomendaciones metrológicas o validación específica de una plataforma."
        },
        {
            "title": "Electrode systems for continuous monitoring in cardiovascular surgery",
            "organization": "Annals of the New York Academy of Sciences",
            "year": 1962,
            "url": "https://pubmed.ncbi.nlm.nih.gov/14021529/",
            "pmid": "14021529",
            "doi": "10.1111/j.1749-6632.1962.tb13623.x",
            "type": "artículo histórico",
            "description": "Trabajo histórico de Clark y Lyons relevante para la evolución de sistemas electroquímicos de monitorización y biosensores enzimáticos posteriores.",
            "verification_status": "verified_directly",
            "locator": "Ann N Y Acad Sci. 1962;102:29-45; PMID 14021529",
            "limitations": "Se utiliza únicamente como contexto histórico, no como estándar actual de desempeño ni seguridad."
        },
        {
            "title": "IUPAC Gold Book: performance characteristic of a measurement procedure",
            "organization": "International Union of Pure and Applied Chemistry",
            "year": 2025,
            "url": "https://goldbook.iupac.org/terms/view/08094/html",
            "type": "terminología metrológica oficial",
            "description": "Distingue características de desempeño de un procedimiento de medición e indica que la incertidumbre del resultado es un concepto distinto.",
            "verification_status": "verified_directly",
            "locator": "Gold Book term 08094; source PAC 2021, 93, 997",
            "limitations": "Los criterios detallados de validación se desarrollan en la unidad 5 y no se cierran en esta introducción."
        },
        {
            "title": "IUPAC Gold Book: electrochemical biosensor",
            "organization": "International Union of Pure and Applied Chemistry",
            "year": 2025,
            "url": "https://goldbook.iupac.org/terms/view/09071",
            "type": "terminología oficial",
            "description": "Define un biosensor electroquímico como sensor electroquímico que incorpora un elemento de reconocimiento biológico.",
            "verification_status": "verified_directly",
            "locator": "Gold Book term 09071; source PAC 2020, 92, 641",
            "limitations": "Es una modalidad concreta; no representa por sí sola las arquitecturas ópticas, térmicas o mecánicas."
        }
    ],
    "editorial_notice": (
        "Unidad en estado de revisión académica interna. La selección y verificación de fuentes y los controles automáticos no "
        "constituyen revisión disciplinaria externa ni validación clínica. Los ejemplos y la actividad usan datos sintéticos o "
        "contexto histórico; no autorizan diagnóstico, tratamiento, monitorización de pacientes, toma de muestras humanas ni "
        "recomendaciones regulatorias o de producto. La revisión humana interna y externa permanecen pendientes."
    )
})

text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
marker = "concepto de la unidad que debe definirse mediante entidades observables"
assert marker not in text.casefold()
assert SOURCE.read_bytes() == MIRROR.read_bytes()
print("Biosensores U1 curated and mirrored exactly")
