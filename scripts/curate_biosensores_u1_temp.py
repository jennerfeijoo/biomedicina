from __future__ import annotations

import json
from pathlib import Path

SOURCE = Path("data/course_redevelopment/biosensores/units/unit-01.json")
MIRROR = Path("data/generated_units/biosensores/unit-01.json")
GENERIC = "Concepto de la unidad que debe definirse mediante entidades observables"

unit = {
    "schema_version": "2.0",
    "subject_id": "biosensores",
    "area_id": "ingenieria-biomedica",
    "unit": 1,
    "slug": "arquitectura-de-un-biosensor",
    "title": "Arquitectura de un biosensor",
    "status": "review",
    "purpose": "Construir y auditar la arquitectura de un biosensor como una cadena de medición que conecta mensurando o analito, matriz de muestra, reconocimiento biológico, transducción fisicoquímica, acondicionamiento y procesamiento con un resultado reportado, identificando controles, fondo, saturación, incertidumbre y límites de inferencia sin confundir detección analítica con utilidad clínica.",
    "learning_objectives": [
        "Distinguir mensurando, analito, matriz de muestra, bioreceptor, evento de reconocimiento, transductor, indicación y resultado de medición dentro de una arquitectura de biosensor.",
        "Representar un biosensor mediante un diagrama de bloques que muestre la dirección de información desde la muestra hasta el resultado e identifique qué magnitudes se observan, transforman o infieren.",
        "Explicar por qué el reconocimiento biológico y la transducción son funciones distintas y cómo una misma estrategia de reconocimiento puede combinarse con diferentes principios de transducción.",
        "Usar modelos simples de respuesta, fondo y saturación para interpretar una curva concentración-señal dentro de un intervalo declarado sin convertir la pendiente en una medida de especificidad clínica.",
        "Diseñar controles de blanco, superficie sin bioreceptor, analito no diana o interferente, adición positiva y saturación que permitan localizar respuestas inespecíficas o fallos de la cadena.",
        "Documentar un expediente arquitectónico reproducible con pregunta analítica, diagrama, variables, unidades, controles, cálculos, incertidumbre, supuestos y límites de uso."
    ],
    "theory_sections": [
        {
            "heading": "1. Qué hace que un sistema sea un biosensor",
            "paragraphs": [
                "Un biosensor no es simplemente cualquier instrumento utilizado sobre una muestra biológica. Su arquitectura incorpora un componente de reconocimiento biológico y un mecanismo de transducción capaz de convertir el evento de reconocimiento o una consecuencia fisicoquímica asociada en una señal medible. Las definiciones de IUPAC enfatizan esa integración y ayudan a separar el biosensor de un ensayo bioanalítico en el que el reconocimiento y la lectura ocurren como etapas independientes. Para estudiar un diseño con rigor conviene declarar qué componente reconoce, qué fenómeno cambia y qué elemento convierte ese cambio en una indicación cuantificable.",
                "El primer término que debe fijarse es la cantidad que se pretende medir. En muchos ejercicios se habla de analito para referirse a la especie química o biológica de interés, pero la pregunta metrológica debe ser más explícita: concentración, actividad, cantidad de sustancia u otra magnitud, en una matriz definida y bajo condiciones declaradas. La matriz importa porque proteínas, sales, células, viscosidad, pH u otras especies pueden alterar transporte, unión, transducción o fondo. Por eso detectar una molécula en tampón no equivale automáticamente a medirla con el mismo desempeño en sangre, saliva u otra muestra compleja.",
                "El bioreceptor aporta reconocimiento molecular o biológico. Puede ser una enzima, anticuerpo, ácido nucleico, aptámero, receptor celular u otro elemento, pero esta unidad no profundiza todavía en su química: ese análisis corresponde a U2. Aquí interesa comprender su función arquitectónica. El bioreceptor crea una relación entre la presencia o actividad del analito y un evento susceptible de transducción. Ese evento puede ser una reacción catalítica, una unión de afinidad o un cambio asociado. El transductor, en cambio, no decide por sí mismo qué especie es la diana; convierte un fenómeno físico o químico en una señal instrumental.",
                "Esta separación funcional permite comparar arquitecturas sin confundir componentes. Un mismo anticuerpo podría emplearse en una plataforma óptica o electroquímica; un mismo principio amperométrico podría combinarse con diferentes reacciones enzimáticas. La selectividad global emerge de la arquitectura completa, no de una sola etiqueta. Además del bioreceptor y el transductor suelen existir membranas, superficies, electrónica, óptica, adquisición digital y algoritmos. En U1 se representan como bloques funcionales para localizar dónde se introduce información, dónde puede aparecer respuesta inespecífica y qué parte del resultado depende de una transformación posterior."
            ],
            "key_points": [
                "Un biosensor integra reconocimiento biológico y transducción en una arquitectura de medición.",
                "El analito debe vincularse con una magnitud y una matriz de muestra explícitas.",
                "Bioreceptor y transductor cumplen funciones diferentes y no deben tratarse como sinónimos.",
                "El desempeño observado pertenece a la cadena completa y no puede atribuirse automáticamente a un único componente."
            ]
        },
        {
            "heading": "2. De la muestra al resultado: cadena de medición",
            "paragraphs": [
                "Una arquitectura útil se dibuja como una cadena dirigida: muestra y mensurando → reconocimiento → transducción → acondicionamiento y adquisición → procesamiento → indicación o resultado. El Vocabulario Internacional de Metrología denomina cadena de medición a la serie de elementos que constituye un camino de la señal desde el sensor hasta la salida. En un biosensor, el dibujo debe añadir explícitamente el reconocimiento biológico porque es la interfaz que vincula el mensurando con el fenómeno que el transductor puede detectar. Cada flecha representa una transformación y debe tener unidades, condiciones y supuestos identificables cuando sea posible.",
                "La señal cruda no es necesariamente el resultado de medición. Un electrodo puede entregar corriente o potencial; un fotodetector, intensidad o cuentas digitales; un resonador, frecuencia. Después pueden aplicarse correcciones de blanco, normalizaciones, filtrado, conversión analógico-digital o una función de calibración. El VIM define un modelo de medición como una relación matemática entre cantidades conocidas como participantes en la medición, y esta idea obliga a declarar cómo una indicación instrumental termina expresándose en concentración u otra magnitud. Saltar directamente de una señal a una interpretación biomédica oculta pasos que deben auditarse.",
                "La calibración relaciona indicaciones con valores conocidos o asignados de la cantidad medida, pero una curva de calibración por sí sola no contiene toda la incertidumbre del resultado. En una región aproximadamente lineal puede usarse el modelo y = y0 + S c, donde y0 representa el fondo o intercepto, c la concentración y S la sensibilidad local de la respuesta. Esta relación es una aproximación válida solo dentro del intervalo comprobado. En U5 se estudiarán formalmente sensibilidad, límite de detección, rango y validación; en U1 la ecuación sirve para comprender dónde entra cada componente del modelo.",
                "Una arquitectura reproducible conserva la procedencia de cada transformación. Debe indicar qué dato es directo, qué corrección se aplicó, qué parámetros proceden de una calibración y qué decisión se tomó por diseño. También debe distinguir el resultado analítico de su interpretación posterior. Un biosensor puede mostrar una respuesta reproducible a un analito en un escenario sintético y aun así no existir evidencia suficiente para afirmar desempeño en una muestra clínica, capacidad diagnóstica, beneficio para pacientes o conformidad regulatoria. Estas capas se examinan más adelante y requieren evidencia adicional."
            ],
            "equations": [
                {
                    "latex": "y=y_0+S\\,c",
                    "meaning": "Modelo lineal local de una respuesta de biosensor; solo es defendible dentro de un intervalo de calibración previamente comprobado.",
                    "variables": {
                        "y": "indicación o señal procesada",
                        "y_0": "intercepto o respuesta de fondo",
                        "S": "sensibilidad local de la respuesta, expresada como pendiente",
                        "c": "concentración del analito en la matriz declarada"
                    }
                },
                {
                    "latex": "y_{obs}=y_{blanco}+y_{espec}(c)+y_{inesp}+\\varepsilon",
                    "meaning": "Descomposición conceptual de la señal observada para localizar fondo, respuesta específica, contribución inespecífica y variación residual.",
                    "variables": {
                        "y_obs": "señal observada",
                        "y_blanco": "respuesta medida en ausencia del analito diana",
                        "y_espec(c)": "componente dependiente del reconocimiento específico",
                        "y_inesp": "respuesta debida a procesos no específicos o interferentes",
                        "epsilon": "variación instrumental y residual no explicada"
                    }
                }
            ],
            "key_points": [
                "La indicación instrumental y el resultado de medición no son necesariamente la misma magnitud.",
                "Cada transformación de la cadena debe declarar entradas, unidades, parámetros y supuestos.",
                "Una pendiente de calibración describe sensibilidad local, no especificidad clínica ni utilidad diagnóstica.",
                "El resultado analítico debe separarse de cualquier interpretación clínica, causal o regulatoria posterior."
            ]
        },
        {
            "heading": "3. Fondo, unión inespecífica, saturación y controles",
            "paragraphs": [
                "Toda señal de biosensor tiene un contexto de fondo. El blanco de reactivos o de matriz estima qué indicación aparece cuando la diana no está presente o se omite de forma controlada. Una superficie preparada sin bioreceptor puede mostrar cuánto de la señal proviene del material, adsorción inespecífica o del propio transductor. Un analito no diana o un interferente plausible ayuda a evaluar si la arquitectura responde de manera diferencial. Ningún control aislado demuestra selectividad universal, pero varios controles bien elegidos permiten localizar qué bloque debe revisarse cuando aparece señal donde no se esperaba.",
                "La saturación es otra propiedad arquitectónica importante. Muchos sistemas de reconocimiento tienen un número finito de sitios o una respuesta instrumental limitada, por lo que aumentar la concentración no produce indefinidamente un aumento proporcional de señal. Como modelo conceptual de unión en equilibrio puede usarse la fracción theta = c/(KD + c). Este modelo de Langmuir ideal supone, entre otras simplificaciones, sitios equivalentes y una forma particular de equilibrio; no describe todos los biosensores. Su valor pedagógico es mostrar por qué una arquitectura puede ser casi lineal a bajas concentraciones y comprimirse al aproximarse a saturación.",
                "Los controles deben diseñarse antes de interpretar la salida. Un blanco informa sobre fondo; un control sin bioreceptor ayuda a detectar contribuciones que no requieren reconocimiento; un no-diana desafía la selectividad; una adición conocida o control positivo comprueba que la cadena puede responder; y una condición de alta concentración explora saturación o límites del intervalo. La pregunta correcta no es simplemente si el control salió bien, sino qué explicación alternativa habría sido compatible con otro patrón y qué bloque de la arquitectura habría quedado bajo sospecha.",
                "La incertidumbre puede originarse en preparación de muestra, concentración asignada, estabilidad del bioreceptor, variación de superficie, deriva del transductor, electrónica, tiempo de incubación, temperatura o procesamiento. U1 no pretende construir todavía un presupuesto metrológico completo, pero sí exigir que la conclusión cambie si una perturbación plausible altera el resultado. Una estrategia útil es variar una contribución de fondo o una pendiente dentro de un rango razonable y observar si cambia la clasificación del diseño. Si cambia, esa dependencia debe aparecer en el informe en lugar de esconderse."
            ],
            "equations": [
                {
                    "latex": "\\theta=\\frac{c}{K_D+c}",
                    "meaning": "Modelo conceptual de ocupación de sitios para una unión ideal en equilibrio; ilustra saturación, no constituye una ley universal para biosensores.",
                    "variables": {
                        "theta": "fracción idealizada de sitios ocupados",
                        "c": "concentración de ligando o analito libre bajo las condiciones del modelo",
                        "K_D": "constante de disociación del modelo ideal"
                    }
                }
            ],
            "key_points": [
                "El blanco y el control sin bioreceptor responden preguntas diferentes sobre el origen del fondo.",
                "Un interferente o analito no diana sirve para desafiar la selectividad dentro de condiciones concretas.",
                "La saturación limita la proporcionalidad entre concentración y señal y debe reconocerse antes de extrapolar una calibración.",
                "La incertidumbre relevante incluye muestra, reconocimiento, superficie, transducción, electrónica y procesamiento."
            ]
        },
        {
            "heading": "4. Decisiones de arquitectura y límites de inferencia",
            "paragraphs": [
                "Elegir una arquitectura implica resolver compromisos. Un diseño puede priorizar simplicidad, respuesta rápida, bajo volumen, lectura directa, integración electrónica o compatibilidad con una matriz concreta. Otro puede aceptar más etapas para mejorar separación de fondo o amplificación. En U1 no se decide cuál plataforma es universalmente mejor; se aprende a justificar qué cadena responde a una pregunta analítica definida. U2 estudiará el reconocimiento, U3 comparará principios de transducción, U4 abordará inmovilización y microfluídica, y U5 formalizará desempeño analítico. Esa separación evita adelantar conclusiones sin los conceptos necesarios.",
                "La historia de los biosensores ilustra esta integración. Los trabajos de Clark y Lyons sobre sistemas de electrodos y el concepto de electrodo enzimático para glucosa combinaron una reacción biológica con una señal electroquímica. El valor del ejemplo no es memorizar una fecha, sino identificar los bloques: especie o actividad de interés, enzima, reacción asociada, electrodo, electrónica e interpretación de la señal. Las arquitecturas actuales pueden ser mucho más complejas, pero el principio de seguir la procedencia de la información desde el reconocimiento hasta la salida permanece esencial.",
                "También es posible construir arquitecturas de afinidad en las que un anticuerpo o aptámero reconozca una diana y el evento se observe mediante un principio óptico, electroquímico u otro. El resultado no permite afirmar que el bioreceptor sea específico en cualquier matriz ni que el transductor sea inmune a interferencias. Tampoco puede inferirse concentración únicamente porque exista una señal: es necesario un modelo, controles y condiciones de calibración. Esta disciplina conceptual previene uno de los errores más frecuentes en prototipos: llamar detección a cualquier diferencia entre dos grupos de señales.",
                "El producto final de U1 es un expediente de arquitectura, no un dispositivo clínicamente validado. Debe responder qué se mide, dónde ocurre el reconocimiento, qué fenómeno se transduce, qué salida se adquiere, cómo se transforma, qué controles localizan fondos e interferencias y qué afirmaciones siguen fuera de alcance. Un resultado educativo sintético puede demostrar que el estudiante comprende la cadena y calcula una respuesta bajo supuestos; no demuestra diagnóstico, seguridad, estabilidad en uso, desempeño con pacientes, comparabilidad con un método de referencia ni cumplimiento regulatorio."
            ],
            "key_points": [
                "La arquitectura se selecciona para una pregunta analítica y una matriz, no por prestigio de una tecnología.",
                "Los compromisos entre reconocimiento, transducción, procesamiento y formato deben documentarse y verificarse por etapas.",
                "Una diferencia de señal no es por sí sola evidencia suficiente de detección específica ni de cuantificación.",
                "U1 termina en un expediente arquitectónico reproducible; validación analítica, clínica y regulatoria requieren etapas posteriores."
            ]
        }
    ],
    "glossary": [
        {"term": "Biosensor", "definition": "Dispositivo analítico que integra un elemento de reconocimiento biológico con una forma de transducción para producir información a partir de un proceso bioquímico o de afinidad."},
        {"term": "Mensurando", "definition": "Cantidad que se pretende medir; debe especificarse con suficiente detalle para que quede claro qué valor se desea obtener y bajo qué condiciones."},
        {"term": "Analito", "definition": "Especie química, biomolécula, actividad u otra entidad relacionada con la cantidad de interés en una muestra; no sustituye por sí sola la definición del mensurando."},
        {"term": "Matriz de muestra", "definition": "Conjunto de componentes de la muestra que acompañan al analito y que pueden modificar reconocimiento, transporte, fondo, transducción o procesamiento."},
        {"term": "Bioreceptor", "definition": "Elemento biológico o biomimético responsable del reconocimiento funcional de la diana, como una enzima, anticuerpo, ácido nucleico, aptámero o receptor."},
        {"term": "Evento de reconocimiento", "definition": "Interacción o reacción mediante la cual el bioreceptor responde a la diana y genera o modifica una propiedad susceptible de transducción."},
        {"term": "Transductor", "definition": "Elemento que convierte una magnitud o fenómeno asociado al reconocimiento en otra señal utilizable por la cadena de medición."},
        {"term": "Cadena de medición", "definition": "Serie de elementos que constituye un camino de la señal desde el sensor hasta un elemento de salida, incluyendo las transformaciones necesarias para producir una indicación."},
        {"term": "Indicación", "definition": "Valor o señal proporcionado por un instrumento o sistema de medición antes de asumir que equivale directamente al valor final del mensurando."},
        {"term": "Modelo de medición", "definition": "Relación matemática entre las cantidades conocidas como involucradas en una medición y utilizada para inferir la cantidad de salida o mensurando."},
        {"term": "Curva de calibración", "definition": "Relación entre una indicación y valores correspondientes de la cantidad medida; por sí sola no incorpora toda la incertidumbre del resultado."},
        {"term": "Sensibilidad", "definition": "Cambio de indicación de un sistema de medición dividido por el cambio correspondiente de la cantidad medida; localmente puede representarse mediante una pendiente."},
        {"term": "Selectividad", "definition": "Capacidad de un sistema de medición para proporcionar valores para uno o más mensurandos sin que otras cantidades presentes produzcan interferencias inadmisibles para el uso definido."},
        {"term": "Blanco", "definition": "Condición preparada para estimar la indicación que aparece sin la contribución intencionada del analito diana y así caracterizar parte del fondo."},
        {"term": "Respuesta inespecífica", "definition": "Componente de señal generado por adsorción, interferentes, superficie u otros procesos que no dependen del reconocimiento específico pretendido."},
        {"term": "Saturación", "definition": "Región en la que aumentar la entrada o concentración ya no produce un incremento proporcional de la señal debido a límites del reconocimiento, transducción o lectura."},
        {"term": "Intervalo de trabajo", "definition": "Intervalo de valores para el que una relación de medición y sus criterios de desempeño han sido establecidos bajo condiciones declaradas."},
        {"term": "Interferente", "definition": "Cantidad o especie distinta de la diana que altera la indicación o la inferencia del mensurando en las condiciones del análisis."}
    ],
    "worked_examples": [
        {
            "title": "Descomponer un biosensor en bloques: electrodo enzimático de glucosa",
            "scenario": "Se analiza como ejemplo histórico una arquitectura en la que una enzima reacciona con glucosa y una señal electroquímica informa sobre una especie consumida o producida por la reacción. El objetivo es identificar funciones, no evaluar un producto clínico.",
            "reasoning_steps": [
                "Definir la pregunta como medición de una cantidad relacionada con glucosa en una matriz y no como diagnóstico de diabetes.",
                "Identificar la enzima como bioreceptor catalítico y separar la reacción bioquímica del electrodo que realiza la transducción electroquímica.",
                "Dibujar la cadena muestra → reacción enzimática → especie electroactiva o consumo asociado → electrodo → corriente → procesamiento → resultado.",
                "Añadir blanco, control sin enzima y una adición conocida para localizar fondo, contribución no enzimática y capacidad de respuesta.",
                "Registrar que la relación corriente-concentración depende de condiciones de transporte, reacción, electrodo y calibración."
            ],
            "interpretation": "El ejemplo muestra por qué reconocimiento y transducción deben describirse por separado y cómo el resultado final depende de toda la cadena, no únicamente de la enzima.",
            "limitations": [
                "El esquema simplificado no representa todas las generaciones ni configuraciones de biosensores de glucosa.",
                "No estima exactitud clínica, interferencias reales, estabilidad ni seguridad de un dispositivo comercial.",
                "La relación señal-concentración debe establecerse para la matriz y condiciones de uso específicas."
            ]
        },
        {
            "title": "Misma diana, distinta transducción",
            "scenario": "Un biomarcador sintético X se reconoce con el mismo anticuerpo en dos diseños hipotéticos: uno mide un cambio óptico y otro una respuesta electroquímica.",
            "reasoning_steps": [
                "Mantener idénticos analito, matriz y bioreceptor para aislar conceptualmente el efecto de cambiar el transductor.",
                "Definir como indicación del diseño A una intensidad óptica y del diseño B una corriente, con unidades diferentes y cadenas de acondicionamiento propias.",
                "Asignar a cada arquitectura un blanco, control sin bioreceptor, no-diana y control positivo equivalentes en propósito.",
                "Comparar qué bloques cambian y cuáles permanecen invariantes; evitar concluir que una señal mayor implica mejor selectividad.",
                "Indicar qué datos de U3 serían necesarios para elegir entre principios de transducción en una aplicación real."
            ],
            "interpretation": "El bioreceptor define una parte del reconocimiento, mientras que el transductor determina cómo ese evento se convierte en una indicación; ambos deben evaluarse dentro de la arquitectura completa.",
            "limitations": [
                "Los valores son sintéticos y no representan plataformas comerciales.",
                "No se compara formalmente límite de detección, precisión ni robustez, que corresponden a U5.",
                "La utilidad clínica no puede deducirse de esta comparación arquitectónica."
            ]
        },
        {
            "title": "Fondo y saturación en una curva concentración-señal",
            "scenario": "Un biosensor sintético entrega 0.11, 0.34, 0.61, 1.09 y 1.95 unidades de señal para 0, 1, 2, 4 y 8 nM. La región de 0 a 4 nM parece aproximadamente lineal, pero el punto de 8 nM se desvía de la extrapolación.",
            "reasoning_steps": [
                "Usar el valor a 0 nM como estimación inicial del fondo, sin asumir que representa todas las fuentes de blanco.",
                "Estimar una pendiente local con los puntos de 0 a 4 nM y escribir explícitamente sus unidades de señal por nM.",
                "Comparar la señal esperada por extrapolación a 8 nM con la observada y reconocer la pérdida de proporcionalidad.",
                "Proponer saturación del reconocimiento o de la lectura como hipótesis, sin elegir una causa sin controles adicionales.",
                "Limitar la interpretación lineal al intervalo probado y proponer datos adicionales cerca del cambio de régimen."
            ],
            "interpretation": "Una curva útil no autoriza extrapolación indefinida. El intervalo, el fondo y las posibles fuentes de saturación forman parte de la arquitectura y de la conclusión.",
            "limitations": [
                "El conjunto de datos es sintético y pequeño.",
                "No se calcula un límite de detección ni se valida formalmente el modelo.",
                "La desviación a alta concentración no identifica por sí sola el mecanismo que la causa."
            ]
        }
    ],
    "guided_activities": [
        {
            "title": "Actividad guiada: expediente arquitectónico de un biosensor para biomarcador sintético X",
            "instructions": [
                "Trabaja únicamente con el escenario y los datos sintéticos proporcionados; no recolectes muestras humanas, no contactes participantes y no conectes dispositivos a personas.",
                "Antes de calcular, escribe una pregunta analítica de una frase que incluya la cantidad de interés, la matriz sintética y el tipo de resultado que se desea reportar.",
                "Dibuja la cadena muestra → reconocimiento → transducción → adquisición → procesamiento → resultado y anota en cada bloque qué entra, qué sale y qué unidades se conservan o cambian.",
                "Marca cada elemento como observado directamente, asignado por diseño, calculado o inferido; si una clasificación es dudosa, justifícala.",
                "Predefine qué resultado esperarías en cada control antes de mirar o calcular su señal y explica qué fallo revelaría un resultado contrario.",
                "Conserva una tabla de cálculos, supuestos y correcciones para que otra persona pueda reconstruir la actividad sin consultar tu razonamiento original."
            ],
            "problems": [
                "Define mensurando, analito y matriz para un biomarcador sintético X medido en una matriz artificial, y explica por qué los tres términos no son equivalentes.",
                "Propón un bioreceptor hipotético de afinidad y un transductor genérico; describe por separado el evento de reconocimiento y la magnitud que el transductor convertiría en señal.",
                "Construye un diagrama de bloques completo e identifica al menos dos lugares donde podría aparecer fondo o interferencia.",
                "Con los pares concentración-señal 0 nM→0.11, 1 nM→0.34, 2 nM→0.61 y 4 nM→1.09, estima una pendiente local aproximada y expresa sus unidades.",
                "Usa el modelo lineal obtenido para predecir la señal a 8 nM y compárala con la observación sintética de 1.95; explica por qué la diferencia obliga a revisar la extrapolación.",
                "Calcula con el modelo ideal theta=c/(KD+c) la ocupación relativa para c=1, 4 y 8 nM usando KD=2 nM, y relaciona el resultado con el concepto de saturación sin afirmar que esos datos siguen exactamente Langmuir.",
                "Diseña un blanco de matriz y un control de superficie sin bioreceptor; para cada uno indica qué componente de la señal observada ayuda a localizar.",
                "Diseña un control con analito no diana o interferente y un control positivo por adición conocida; escribe antes de calcular qué patrón apoyaría el funcionamiento esperado.",
                "Supón que la respuesta inespecífica aumenta en 0.20 unidades de señal. Reevalúa qué concentraciones quedarían más afectadas en términos relativos y qué conclusión sobre la arquitectura se debilita.",
                "Compara dos alternativas: conservar el mismo bioreceptor y cambiar el transductor, o conservar el transductor y cambiar el bioreceptor. Indica qué preguntas pertenecen a U2 y cuáles a U3.",
                "Redacta una conclusión de máximo 120 palabras que indique qué demuestra el ejercicio y enumere al menos tres afirmaciones que siguen fuera de alcance, incluida cualquier afirmación diagnóstica o de utilidad clínica."
            ],
            "deliverables": [
                "Pregunta analítica y definición de mensurando, analito y matriz.",
                "Diagrama de bloques de la arquitectura con entradas, salidas y unidades.",
                "Tabla de datos sintéticos, cálculo de pendiente, predicción y análisis de saturación.",
                "Matriz de controles con objetivo, resultado esperado y fallo que detectaría.",
                "Análisis de sensibilidad a fondo inespecífico y comparación de dos alternativas de arquitectura.",
                "Conclusión limitada y lista explícita de afirmaciones no demostradas.",
                "Registro reproducible de supuestos, cálculos y correcciones."
            ],
            "checking_criteria": [
                "Mensurando, analito y matriz están definidos sin tratarlos como sinónimos.",
                "Reconocimiento y transducción aparecen como funciones distintas y conectadas.",
                "La cadena incluye adquisición o procesamiento antes del resultado final.",
                "La pendiente conserva unidades y se interpreta solo en el intervalo usado.",
                "La desviación a 8 nM se trata como evidencia contra una extrapolación lineal automática.",
                "Blanco, superficie sin bioreceptor, no-diana y control positivo tienen propósitos diferenciados.",
                "El análisis de fondo muestra cómo una perturbación puede cambiar la interpretación.",
                "Las alternativas se asignan correctamente a reconocimiento o transducción.",
                "Los cálculos pueden reconstruirse a partir del expediente entregado.",
                "La conclusión no afirma diagnóstico, desempeño en pacientes, utilidad clínica ni conformidad regulatoria."
            ]
        }
    ],
    "common_errors": [
        {"error": "Llamar biosensor a cualquier instrumento que analiza una muestra biológica.", "correction": "Identificar explícitamente el elemento de reconocimiento biológico, el fenómeno asociado y el principio de transducción integrado en la cadena."},
        {"error": "Usar analito y mensurando como sinónimos en cualquier contexto.", "correction": "Definir la cantidad que se mide, la especie relacionada y la matriz; una etiqueta molecular no sustituye la especificación de la magnitud."},
        {"error": "Confundir bioreceptor con transductor.", "correction": "Separar quién reconoce o reacciona con la diana de qué elemento convierte el fenómeno en una señal instrumental."},
        {"error": "Interpretar una señal mayor como mayor especificidad.", "correction": "La amplitud no demuestra selectividad; usar controles no-diana, blancos y superficies de control para estudiar contribuciones alternativas."},
        {"error": "Aplicar una calibración lineal fuera del intervalo comprobado.", "correction": "Declarar el intervalo, inspeccionar saturación y no extrapolar una pendiente local cuando la arquitectura deja de responder proporcionalmente."},
        {"error": "Usar un único blanco como prueba completa de ausencia de interferencias.", "correction": "Combinar controles que separen fondo de matriz, superficie, reconocimiento inespecífico, interferentes y capacidad positiva de respuesta."},
        {"error": "Tratar la curva de calibración como un resultado con incertidumbre completa.", "correction": "La curva describe una relación indicación-valor; el resultado requiere además modelo, correcciones, fuentes de incertidumbre y condiciones de medición."},
        {"error": "Convertir detección analítica sintética en conclusión diagnóstica o clínica.", "correction": "Limitar la conclusión al escenario analítico; desempeño clínico, utilidad, seguridad y regulación requieren evidencia y etapas independientes."}
    ],
    "self_assessment": [
        {"question": "¿Qué distingue arquitectónicamente a un biosensor de un sensor que solo mide una propiedad física de una muestra?", "answer": "La integración de un elemento de reconocimiento biológico con una transducción que convierte el evento o una consecuencia asociada en información medible.", "reasoning": "La definición debe identificar funciones y su integración, no limitarse a decir que el dispositivo se usa en biología.", "common_error": "Definir biosensor únicamente por el tipo de muestra."},
        {"question": "¿Por qué analito y mensurando no son siempre equivalentes?", "answer": "El analito identifica una especie de interés, mientras que el mensurando especifica la cantidad que se pretende medir y sus condiciones relevantes.", "reasoning": "La medición exige una cantidad bien definida, por ejemplo concentración de una especie en una matriz concreta.", "common_error": "Nombrar una molécula y asumir que la magnitud medida queda implícita."},
        {"question": "¿Qué función corresponde al bioreceptor y cuál al transductor?", "answer": "El bioreceptor participa en el reconocimiento o reacción de la diana; el transductor convierte un fenómeno asociado en una señal utilizable.", "reasoning": "Separar funciones permite comparar arquitecturas y localizar fallos.", "common_error": "Atribuir selectividad molecular al transductor por sí solo."},
        {"question": "¿Por qué una indicación eléctrica u óptica no es automáticamente una concentración?", "answer": "Porque debe existir un modelo o función de medición que relacione la indicación con el mensurando y considere las condiciones y correcciones pertinentes.", "reasoning": "Entre sensor y resultado pueden existir varias transformaciones auditables.", "common_error": "Etiquetar el eje de señal como concentración sin calibración ni modelo."},
        {"question": "¿Qué significa S en y=y0+Sc?", "answer": "La pendiente o sensibilidad local de la respuesta dentro del intervalo donde el modelo lineal ha sido comprobado.", "reasoning": "La pendiente expresa cambio de indicación por cambio de concentración, no especificidad clínica.", "common_error": "Llamar especificidad a una pendiente grande."},
        {"question": "¿Qué diferencia existe entre un blanco y una superficie sin bioreceptor?", "answer": "El blanco caracteriza señal sin la contribución intencionada de la diana, mientras que la superficie sin bioreceptor ayuda a localizar señal que no requiere el reconocimiento diseñado.", "reasoning": "Los controles responden preguntas causales distintas dentro de la cadena.", "common_error": "Usarlos como controles intercambiables sin declarar qué bloque evalúan."},
        {"question": "¿Qué enseña el modelo theta=c/(KD+c) en esta unidad?", "answer": "Ilustra que una respuesta basada en ocupación de sitios puede saturarse y dejar de crecer proporcionalmente con la concentración.", "reasoning": "Es un modelo ideal conceptual y sus supuestos deben declararse.", "common_error": "Usarlo como ley universal para cualquier biosensor o estimar KD sin datos adecuados."},
        {"question": "¿Por qué un no-diana es útil pero no demuestra selectividad universal?", "answer": "Porque desafía una interferencia concreta bajo condiciones concretas; otras especies, matrices o concentraciones pueden producir comportamientos diferentes.", "reasoning": "La fuerza de una conclusión depende del espacio de interferentes y condiciones realmente evaluado.", "common_error": "Generalizar un control negativo a todas las interferencias posibles."},
        {"question": "¿Qué evidencia justificaría revisar una extrapolación lineal?", "answer": "Una desviación sistemática de la señal respecto al modelo al aumentar la concentración, especialmente si coincide con saturación u otro límite reproducible.", "reasoning": "Los modelos se validan dentro de un dominio y deben abandonarse o modificarse cuando los residuos muestran estructura relevante.", "common_error": "Forzar una recta porque los primeros puntos eran aproximadamente lineales."},
        {"question": "¿Qué puede concluirse después de completar el expediente sintético de U1?", "answer": "Que la arquitectura y su razonamiento pueden reconstruirse y que ciertos controles y modelos se aplicaron correctamente al escenario sintético.", "reasoning": "El alcance educativo no incluye desempeño clínico, diagnóstico, seguridad de producto ni conformidad regulatoria.", "common_error": "Presentar un ejercicio de arquitectura como validación de un biosensor real."}
    ],
    "biomedical_connections": [
        {"topic": "Monitoreo bioquímico", "connection": "La arquitectura de reconocimiento y transducción es la base conceptual para sistemas que miden especies bioquímicas, pero cada matriz y uso requieren caracterización independiente."},
        {"topic": "Diagnóstico in vitro", "connection": "Un biosensor puede formar parte de un ensayo diagnóstico, aunque demostrar señal analítica no demuestra por sí sola sensibilidad o especificidad diagnóstica."},
        {"topic": "Point-of-care", "connection": "La cadena de medición ayuda a identificar qué etapas deben integrarse para una lectura cercana al lugar de atención; su utilidad se estudia en U6."},
        {"topic": "Wearables", "connection": "Los sensores portátiles añaden restricciones de matriz, deriva, biointerfaz y contexto de uso que no pueden inferirse a partir de una calibración de laboratorio."},
        {"topic": "Ingeniería de medición", "connection": "Modelos de medición, calibración, controles y trazabilidad permiten distinguir señal instrumental de un resultado defendible y conectan Biosensores con Bioinstrumentación."}
    ],
    "sources": [
        {"title": "IUPAC Gold Book — biosensor (B00663)", "organization": "International Union of Pure and Applied Chemistry", "url": "https://goldbook.iupac.org/terms/view/B00663", "type": "terminología oficial", "description": "Definición vigente de biosensor en el Compendium of Chemical Terminology, 5.ª edición en línea.", "doi": "10.1351/goldbook.B00663", "verification_status": "verified_directly"},
        {"title": "Electrochemical Biosensors: Recommended Definitions and Classification", "organization": "IUPAC / Pure and Applied Chemistry", "url": "https://publications.iupac.org/pac/71/12/2333/index.html", "type": "informe técnico y recomendaciones", "description": "Thévenot, Tóth, Durst y Wilson (1999); definición, componentes, clasificación y criterios de reporte para biosensores electroquímicos.", "doi": "10.1351/pac199971122333", "verification_status": "verified_directly"},
        {"title": "Biosensors: sense and sensibility", "organization": "Chemical Society Reviews / PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/23420144/", "type": "revisión", "description": "Turner (2013); revisión general del campo y de la integración entre elementos biológicos de sensado y transductores fisicoquímicos.", "doi": "10.1039/C3CS35528D", "verification_status": "verified_directly"},
        {"title": "Electrochemical Biosensors — Sensor Principles and Architectures", "organization": "Sensors / PubMed Central", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3663003/", "type": "revisión abierta", "description": "Grieshaber et al. (2008); principios y arquitecturas electroquímicas con énfasis en el camino desde reconocimiento a señal electrónica.", "doi": "10.3390/s80314000", "verification_status": "verified_directly"},
        {"title": "VIM3 2.48 — measurement model", "organization": "JCGM / BIPM", "url": "https://jcgm.bipm.org/vim/en/2.48.html", "type": "vocabulario metrológico oficial", "description": "Define modelo de medición como relación matemática entre las cantidades conocidas como involucradas en una medición.", "verification_status": "verified_directly"},
        {"title": "VIM3 3.10 — measuring chain", "organization": "JCGM / BIPM", "url": "https://jcgm.bipm.org/vim/en/3.10.html", "type": "vocabulario metrológico oficial", "description": "Define cadena de medición como serie de elementos de un sistema que constituye un camino único de señal desde sensor hasta salida.", "verification_status": "verified_directly"},
        {"title": "VIM3 4.31 — calibration curve", "organization": "JCGM / BIPM", "url": "https://jcgm.bipm.org/vim/en/4.31.html", "type": "vocabulario metrológico oficial", "description": "Define la curva de calibración y aclara que la relación indicación-valor no contiene por sí sola información completa de incertidumbre.", "verification_status": "verified_directly"},
        {"title": "Electrode systems for continuous monitoring in cardiovascular surgery", "organization": "Annals of the New York Academy of Sciences / PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/14021529/", "type": "artículo histórico primario", "description": "Clark y Lyons (1962); referencia histórica sobre sistemas de electrodos y el concepto de acoplar reacciones biológicas con lectura electroquímica.", "doi": "10.1111/j.1749-6632.1962.tb13623.x", "verification_status": "verified_directly"}
    ],
    "editorial_notice": "Material educativo de Biosensores U1 con curación académica interna y estado review. No constituye revisión disciplinar externa, validación clínica, validación de un dispositivo, certificación ni conformidad regulatoria. Las actividades usan exclusivamente datos sintéticos y no autorizan recoger muestras humanas, medir participantes, diagnosticar, prescribir ni inferir utilidad clínica a partir de una señal analítica."
}

text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
assert GENERIC.casefold() not in text.casefold()
assert len(unit["learning_objectives"]) >= 5
assert len(unit["theory_sections"]) == 4
assert len(unit["glossary"]) >= 16
assert len(unit["worked_examples"]) >= 3
assert len(unit["common_errors"]) >= 8
assert len(unit["self_assessment"]) >= 10
assert len(unit["sources"]) >= 6
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
