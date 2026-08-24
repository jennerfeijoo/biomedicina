from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomecanica" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biomecanica" / "unit-01.json"
MARKER = "Concepto de la unidad que debe definirse mediante entidades observables"

unit = json.loads(SOURCE.read_text(encoding="utf-8"))

unit["purpose"] = (
    "Construir una descripción cinemática reproducible del movimiento humano mediante marcos de referencia, "
    "posición y orientación segmentaria, velocidad y aceleración, comparación 2D/3D y análisis explícito de error de medición, "
    "sin confundir la descripción del movimiento con sus causas dinámicas ni con una decisión clínica."
)
unit["learning_objectives"] = [
    "Definir marcos globales, locales y anatómicos y transformar posiciones entre ellos sin perder unidades ni convención de ejes.",
    "Representar orientación segmentaria y movimiento articular distinguiendo traslación, rotación, ángulos absolutos y relativos.",
    "Calcular velocidad y aceleración a partir de trayectorias discretas y explicar por qué la diferenciación amplifica ruido.",
    "Comparar análisis 2D y 3D identificando cuándo la proyección fuera del plano invalida una interpretación angular.",
    "Identificar errores instrumentales, de calibración, colocación de marcadores y artefacto de tejido blando y propagarlos hasta la conclusión.",
    "Documentar un análisis cinemático sintético con datos, transformación, procesamiento, controles, resultados y límites reproducibles."
]

unit["theory_sections"] = [
    {
        "heading": "1. Marcos de referencia, posición y orientación",
        "paragraphs": [
            "La cinemática describe cómo cambia la configuración de un sistema con el tiempo sin atribuir todavía las causas mecánicas de ese cambio. En movimiento humano, una coordenada solo es interpretable si se declara el marco de referencia al que pertenece. Un laboratorio puede definir ejes distintos de un modelo musculoesquelético; por ello, una trayectoria válida en el sistema de cámaras puede quedar rotada, reflejada o con la gravedad apuntando en otra dirección si se importa sin transformación. OpenSim, por ejemplo, exige compatibilizar el sistema del laboratorio con el del modelo antes de interpretar marcadores o fuerzas externas.",
            "Un marco cartesiano tridimensional queda definido por un origen y tres ejes ortogonales con una orientación coherente. Para describir un segmento corporal conviene distinguir el marco global del laboratorio, un marco técnico construido con marcadores y un marco anatómico ligado a referencias óseas. La posición de un punto es un vector expresado en un marco; la orientación de un segmento requiere una rotación entre marcos. Cambiar de coordenadas no cambia el fenómeno físico, pero sí cambia los componentes numéricos que lo representan, por lo que la convención forma parte del dato y debe conservarse con el archivo.",
            "Una transformación rígida combina rotación y traslación. Si un punto tiene coordenadas r_A en el marco A, puede expresarse en B mediante r_B = R_BA r_A + p_BA, donde R_BA es una matriz de rotación y p_BA es la posición del origen de A expresada en B. Una matriz de rotación válida conserva longitudes y ángulos, cumple RᵀR = I y tiene determinante +1. Una matriz con determinante −1 introduce una reflexión: puede producir una figura visualmente plausible y, sin embargo, invertir lateralidad o el signo de una rotación.",
            "En biomecánica articular no basta con decir que una rodilla tiene cierto ángulo. Deben declararse los segmentos usados, los ejes anatómicos, la secuencia o convención de rotación y el sentido positivo. Las recomendaciones de la International Society of Biomechanics existen precisamente para mejorar la comparabilidad del reporte. La orientación puede parametrizarse con matrices, cuaterniones o secuencias angulares; cada representación tiene ventajas y singularidades. El curso usa matrices para razonar sobre marcos y reserva las convenciones articulares específicas para interpretar ángulos con el estándar declarado."
        ],
        "equations": [
            {"latex": "\\mathbf r_B=\\mathbf R_{BA}\\mathbf r_A+\\mathbf p_{BA}", "meaning": "Transformación rígida de las coordenadas de un punto entre dos marcos de referencia."},
            {"latex": "\\mathbf R^T\\mathbf R=\\mathbf I,\\quad \\det(\\mathbf R)=+1", "meaning": "Condiciones que debe cumplir una matriz de rotación propia."}
        ],
        "key_points": [
            "Una coordenada sin marco de referencia declarado está incompleta.",
            "Posición y orientación son propiedades distintas y requieren representaciones distintas.",
            "La transformación entre marcos debe conservar geometría y lateralidad.",
            "Los ángulos articulares dependen de ejes y convenciones de reporte explícitas."
        ]
    },
    {
        "heading": "2. Trayectorias, velocidad, aceleración y procesamiento",
        "paragraphs": [
            "Una trayectoria es la secuencia temporal de posiciones de un punto o de configuraciones de un segmento. La velocidad lineal es la derivada temporal de la posición y la aceleración es la derivada de la velocidad. En datos digitales no se dispone de una función continua perfecta, sino de muestras separadas por un intervalo Δt. Las derivadas se estiman numéricamente, por ejemplo mediante diferencias centrales. El resultado depende de la frecuencia de muestreo, de la regularidad temporal y del ruido de posición; por eso no debe presentarse una derivada como si fuera una medición directa independiente del procesamiento.",
            "La diferenciación amplifica las componentes de alta frecuencia. Un error de pocos milímetros que apenas se aprecia en una trayectoria puede producir oscilaciones grandes en velocidad y todavía mayores en aceleración. Este problema está documentado desde los primeros trabajos de análisis de locomoción y sigue siendo relevante con sistemas modernos. Filtrar puede reducir ruido, pero también puede atenuar picos, desplazar características o eliminar contenido real si el corte se elige de manera automática. El filtro, orden, frecuencia de corte, tratamiento de extremos y dirección de aplicación deben registrarse como parte del método.",
            "Para una serie uniformemente muestreada, una aproximación central de velocidad en el instante i usa las posiciones anterior y posterior; la aceleración puede estimarse con la segunda diferencia. Estas expresiones son útiles para comprender el cálculo, pero no constituyen una receta universal. En extremos de la serie faltan vecinos simétricos; en movimientos con impactos o cambios rápidos, una estrategia de suavizado elegida para marcha lenta puede resultar inadecuada. Antes de fijar parámetros conviene inspeccionar la naturaleza del movimiento, la frecuencia de muestreo y la sensibilidad de las variables finales.",
            "La cinemática angular requiere la misma disciplina. Una orientación puede convertirse en un ángulo articular y luego derivarse para obtener velocidad angular, pero cada paso introduce decisiones. Las discontinuidades de representación, el desenrollado de ángulos y las singularidades de ciertas secuencias pueden generar saltos numéricos que no corresponden a un movimiento físico. Un control básico consiste en reconstruir o visualizar el movimiento tras cada transformación y verificar rangos, continuidad y signos antes de calcular métricas resumen."
        ],
        "equations": [
            {"latex": "\\mathbf v_i\\approx\\frac{\\mathbf r_{i+1}-\\mathbf r_{i-1}}{2\\Delta t}", "meaning": "Diferencia central para estimar velocidad a partir de posiciones discretas."},
            {"latex": "\\mathbf a_i\\approx\\frac{\\mathbf r_{i+1}-2\\mathbf r_i+\\mathbf r_{i-1}}{\\Delta t^2}", "meaning": "Segunda diferencia central para estimar aceleración."}
        ],
        "key_points": [
            "Velocidad y aceleración calculadas heredan el ruido y las decisiones de procesamiento de la posición.",
            "La diferenciación numérica amplifica especialmente las componentes de alta frecuencia.",
            "El filtrado debe justificarse por señal, tarea y variable final, no por una frecuencia fija universal.",
            "Visualizar y verificar continuidad, rango y signo es un control previo a la interpretación."
        ]
    },
    {
        "heading": "3. Análisis 2D y reconstrucción 3D",
        "paragraphs": [
            "El análisis bidimensional representa el movimiento en un plano de imagen. Puede ser suficiente cuando la tarea es aproximadamente planar, la cámara está adecuadamente alineada y la variable de interés tolera la pérdida de profundidad. La ventaja es una adquisición y procesamiento más simples; la limitación fundamental es geométrica: una coordenada fuera del plano no se conserva en la proyección. Una rotación del cuerpo respecto a la cámara puede cambiar un ángulo proyectado aunque la configuración tridimensional de los segmentos no haya cambiado en la misma magnitud.",
            "Un análisis tridimensional estima la posición espacial a partir de múltiples vistas calibradas, sensores inerciales u otras tecnologías. En sistemas ópticos multicámara, la reconstrucción depende de calibración, sincronización, visibilidad de marcadores o puntos clave y definición del modelo corporal. Tener tres coordenadas no elimina el error: los centros articulares suelen inferirse a partir de marcadores superficiales y parámetros antropométricos, no observarse directamente. La salida 3D es por tanto el resultado de una cadena de medición y modelado que debe documentarse.",
            "Los ángulos calculados a partir de vectores permiten ilustrar la diferencia entre geometría espacial y proyección. Para dos vectores u y v, el ángulo geométrico puede obtenerse a partir del producto escalar. Si primero se descarta una componente para simular una cámara 2D, el ángulo calculado puede cambiar. Esta comparación es un control pedagógico útil: si una conclusión sobre flexión, valgo o rotación depende mucho de la orientación respecto a la cámara, el análisis 2D no está midiendo de forma estable la magnitud tridimensional que se pretende interpretar.",
            "La elección entre 2D y 3D debe partir del uso previsto y de una tolerancia de error, no de la idea de que una tecnología es siempre superior. Medidas espaciotemporales como velocidad de marcha pueden ser robustas con métodos sencillos, mientras que algunas rotaciones articulares, especialmente fuera del plano sagital, son más sensibles a la técnica. La literatura reciente sobre captura sin marcadores muestra precisamente que el desempeño varía por variable y plano; por ello una validación para una métrica no autoriza a asumir validez equivalente para todas las demás."
        ],
        "equations": [
            {"latex": "\\theta=\\arccos\\left(\\frac{\\mathbf u\\cdot\\mathbf v}{\\lVert\\mathbf u\\rVert\\,\\lVert\\mathbf v\\rVert}\\right)", "meaning": "Ángulo geométrico entre dos vectores; la proyección previa de esos vectores puede cambiar el resultado."}
        ],
        "key_points": [
            "2D elimina información fuera del plano y su validez depende de la geometría de la tarea y la cámara.",
            "3D añade información espacial pero también depende de calibración, sincronización y modelo corporal.",
            "Un ángulo proyectado no debe interpretarse automáticamente como el ángulo articular tridimensional.",
            "La suficiencia del método se decide variable por variable y según el uso previsto."
        ]
    },
    {
        "heading": "4. Error de medición, artefacto de tejido blando y reproducibilidad",
        "paragraphs": [
            "En captura de movimiento con marcadores, el sistema óptico mide centros de marcadores adheridos a la piel, no la pose ósea directamente. Entre la piel y el hueso existen tejidos que se deforman y desplazan; esta movilidad relativa produce artefacto de tejido blando. Estudios con referencias rígidas al hueso y revisiones posteriores muestran que el error puede afectar posiciones y orientaciones segmentarias de manera dependiente de la tarea y del sitio anatómico. Por eso un modelo que dibuja un esqueleto suave no debe confundirse con una observación exacta de los huesos.",
            "También aparecen errores por identificación de referencias anatómicas, colocación repetida de marcadores, oclusiones, reconstrucción óptica, calibración, desincronización y elección del modelo. Algunos son predominantemente aleatorios y otros pueden introducir sesgos sistemáticos. Repetir una medición puede caracterizar parte de la variabilidad, pero no revela por sí sola un sesgo común a todas las repeticiones. Cuando la magnitud esperada del cambio es similar a la incertidumbre del método, una diferencia numérica pequeña no debe convertirse automáticamente en una diferencia biomecánica significativa.",
            "La reproducibilidad exige conservar datos crudos o su procedencia, unidades, frecuencia de muestreo, convención de ejes, parámetros de calibración disponibles, definición de segmentos, transformaciones, algoritmo de filtrado, tratamiento de datos faltantes y código o procedimiento. Para cada variable derivada conviene mantener una cadena desde la observación hasta el resultado. Si se cambia el filtro o el marco de referencia durante el análisis, el cambio debe quedar registrado y la variable final recalcularse de forma coherente.",
            "El cierre de una unidad de cinemática debe separar cuatro niveles: qué se midió, qué se calculó, qué se infiere biomecánicamente y qué decisión queda fuera de alcance. Una trayectoria puede demostrar que un marcador se desplazó de cierta forma bajo un protocolo; no demuestra por sí sola lesión, causa de dolor ni eficacia terapéutica. En un contexto clínico, la utilidad de una métrica necesita evidencia adicional sobre fiabilidad, validez, población y capacidad de modificar decisiones. Aquí el objetivo es dominar la medición y el razonamiento cinemático antes de dar ese salto."
        ],
        "equations": [
            {"latex": "RMSE=\\sqrt{\\frac{1}{n}\\sum_{i=1}^{n}(x_i-x_i^{ref})^2}", "meaning": "Ejemplo de métrica de discrepancia respecto a una referencia; debe interpretarse junto con el diseño de comparación y no como validez universal."}
        ],
        "key_points": [
            "Los marcadores cutáneos aproximan el movimiento óseo y pueden presentar artefacto de tejido blando.",
            "Repetibilidad y ausencia de sesgo son propiedades distintas.",
            "El procesamiento completo debe quedar trazable desde datos crudos hasta variables derivadas.",
            "La descripción cinemática no equivale a diagnóstico, causalidad ni eficacia de una intervención."
        ]
    }
]

unit["glossary"] = [
    {"term": "Cinemática", "definition": "Descripción matemática de posición, orientación y sus cambios temporales sin atribuir todavía las fuerzas o momentos que producen el movimiento."},
    {"term": "Marco de referencia", "definition": "Origen y conjunto de ejes respecto a los cuales se expresan las coordenadas de puntos, vectores y orientaciones."},
    {"term": "Marco global", "definition": "Sistema de coordenadas fijo al laboratorio o entorno usado como referencia común para describir el movimiento."},
    {"term": "Marco local de segmento", "definition": "Sistema de coordenadas unido conceptualmente a un segmento corporal y usado para expresar su pose respecto a otro marco."},
    {"term": "Posición", "definition": "Vector que localiza un punto respecto al origen de un marco de referencia declarado."},
    {"term": "Orientación", "definition": "Relación rotacional entre dos marcos de referencia; no queda determinada solo por la posición de un punto."},
    {"term": "Transformación rígida", "definition": "Operación compuesta por rotación y traslación que cambia la representación de una geometría sin deformarla."},
    {"term": "Matriz de rotación", "definition": "Matriz ortogonal de determinante +1 que representa una rotación propia entre marcos tridimensionales."},
    {"term": "Ángulo articular", "definition": "Medida de orientación relativa entre segmentos cuya interpretación depende de ejes anatómicos y una convención de rotación declarada."},
    {"term": "Velocidad", "definition": "Tasa temporal de cambio de la posición; en datos discretos suele estimarse numéricamente a partir de muestras de trayectoria."},
    {"term": "Aceleración", "definition": "Tasa temporal de cambio de la velocidad o segunda derivada de la posición, especialmente sensible al ruido de alta frecuencia."},
    {"term": "Proyección 2D", "definition": "Representación de una geometría espacial en un plano de imagen, con pérdida de la componente perpendicular a ese plano."},
    {"term": "Reconstrucción 3D", "definition": "Estimación de coordenadas espaciales a partir de observaciones calibradas de múltiples vistas o de otras modalidades de medición."},
    {"term": "Artefacto de tejido blando", "definition": "Movimiento relativo entre marcadores o sensores superficiales y el hueso subyacente que introduce error en la pose estimada del segmento."},
    {"term": "Filtrado", "definition": "Procesamiento destinado a atenuar componentes no deseadas de una señal; sus parámetros pueden modificar amplitudes y derivadas y deben documentarse."},
    {"term": "Frecuencia de muestreo", "definition": "Número de muestras adquiridas por unidad de tiempo; condiciona la resolución temporal y el procesamiento posterior."}
]

unit["worked_examples"] = [
    {
        "title": "Transformar del laboratorio al modelo sin invertir lateralidad",
        "scenario": "El laboratorio usa X hacia delante, Y hacia la izquierda y Z hacia arriba; el modelo usa X hacia delante, Y hacia arriba y Z hacia la derecha. Un marcador está en (1.20, 0.15, 0.90) m en el laboratorio.",
        "reasoning_steps": [
            "Escribir ambas convenciones antes de transformar y mantener metros como unidad.",
            "Conservar X porque ambos sistemas lo definen hacia delante.",
            "Asignar Z del laboratorio a Y del modelo porque ambos apuntan hacia arriba.",
            "Cambiar el signo de Y del laboratorio al construir Z del modelo, porque izquierda y derecha tienen sentidos opuestos.",
            "Obtener (1.20, 0.90, -0.15) m y verificar que la matriz usada es ortogonal y tiene determinante +1."
        ],
        "interpretation": "El marcador no se ha movido físicamente: solo cambió su representación. El control de determinante evita introducir una reflexión que podría intercambiar derecha e izquierda.",
        "limitations": ["El ejemplo usa ejes perfectamente alineados y no incluye traslación entre orígenes.", "En datos reales deben transformarse de forma coherente marcadores, vectores y cualquier otra magnitud espacial compatible."]
    },
    {
        "title": "Derivar una trayectoria discreta y reconocer amplificación del ruido",
        "scenario": "La coordenada anterior de un marcador vale 0.00, 0.06 y 0.14 m en t = 0.00, 0.10 y 0.20 s.",
        "reasoning_steps": [
            "Usar Δt = 0.10 s y una diferencia central para el instante intermedio.",
            "Calcular v(0.10) = (0.14 - 0.00)/(0.20) = 0.70 m/s.",
            "Calcular a(0.10) = (0.14 - 2·0.06 + 0.00)/(0.10²) = 2.0 m/s².",
            "Perturbar la posición central en solo +0.002 m y repetir la aceleración: cambia a 1.6 m/s².",
            "Concluir que una perturbación milimétrica puede tener un efecto proporcionalmente mucho mayor sobre una segunda derivada."
        ],
        "interpretation": "La aritmética ilustra por qué el tratamiento del ruido debe decidirse antes de interpretar aceleraciones y no después de observar un resultado atractivo.",
        "limitations": ["Tres muestras no bastan para diseñar un filtro real.", "La diferencia central no resuelve por sí sola extremos, datos faltantes ni movimientos no estacionarios."]
    },
    {
        "title": "Comprobar si un ángulo 2D representa una configuración 3D",
        "scenario": "Se calcula el ángulo entre muslo y pierna desde una cámara lateral y luego se repite después de rotar virtualmente el mismo conjunto de puntos 20° alrededor del eje vertical.",
        "reasoning_steps": [
            "Calcular primero el ángulo usando los vectores 3D completos.",
            "Proyectar los mismos vectores en el plano de la cámara y calcular el ángulo 2D.",
            "Rotar virtualmente el sistema completo sin cambiar el ángulo relativo 3D.",
            "Volver a proyectar y observar si el ángulo 2D cambia por la nueva orientación respecto a la cámara.",
            "Usar la diferencia como evidencia de error de proyección y no como cambio articular real."
        ],
        "interpretation": "Una medición 2D puede ser adecuada para una tarea casi planar, pero debe demostrarse que el movimiento fuera del plano no domina la variable de interés.",
        "limitations": ["El ejercicio usa geometría sintética y no cuantifica errores de calibración de una cámara real.", "La validez debe evaluarse para cada variable y población objetivo."]
    }
]

unit["guided_activities"] = [
    {
        "title": "Actividad guiada: expediente cinemático sintético de una zancada",
        "instructions": [
            "Trabaja únicamente con el conjunto sintético descrito en la actividad; no grabes personas ni recopiles datos personales.",
            "Antes de calcular, crea una hoja de trazabilidad con columnas: dato original, marco, unidad, transformación, variable derivada, control y límite.",
            "Usa como convención de laboratorio X hacia delante, Y hacia la izquierda y Z hacia arriba; para el modelo usa X hacia delante, Y hacia arriba y Z hacia la derecha.",
            "Para derivadas usa diferencias centrales solo en muestras interiores y marca los extremos como no estimados con ese método.",
            "Conserva una versión sin filtrar; cualquier suavizado debe documentar método y parámetro y compararse con el resultado original."
        ],
        "problems": [
            "Dibuja ambos marcos con sus ejes y escribe la matriz que transforma [x,y,z]lab en [x,z,-y]modelo; comprueba RᵀR = I y det(R) = +1.",
            "Transforma los puntos sintéticos P1=(1.20,0.15,0.90), P2=(1.25,0.15,0.55) y P3=(1.38,0.13,0.20) m al marco del modelo.",
            "Calcula la longitud de los segmentos P1-P2 y P2-P3 antes y después de la transformación y confirma que una rotación rígida conserva distancias.",
            "Con las posiciones x = [0.00,0.06,0.14,0.23,0.31] m a intervalos de 0.10 s, estima las velocidades en las tres muestras interiores mediante diferencia central.",
            "Estima las aceleraciones en las tres muestras interiores y repite el cálculo después de añadir +0.002 m a la muestra central; cuantifica la sensibilidad.",
            "Construye dos vectores de segmento con P1, P2 y P3 y calcula su ángulo 3D mediante producto escalar.",
            "Proyecta los vectores eliminando una componente, recalcula el ángulo 2D y explica qué información se perdió.",
            "Propón un criterio para decidir si la diferencia 2D-3D sería aceptable para una pregunta descriptiva concreta; no uses un umbral universal sin fuente.",
            "Enumera al menos cuatro fuentes de error de una captura con marcadores y clasifica cuáles podría detectar una repetición y cuáles podrían persistir como sesgo.",
            "Redacta una conclusión de máximo 180 palabras separando observación, cálculo, inferencia biomecánica y afirmaciones clínicas fuera de alcance."
        ],
        "deliverables": [
            "Diagrama de marcos y matriz de transformación verificada.",
            "Tabla de coordenadas originales y transformadas con unidades.",
            "Cálculos de velocidad y aceleración con análisis de sensibilidad.",
            "Comparación de ángulos 2D y 3D con interpretación geométrica.",
            "Registro de fuentes de error y controles.",
            "Conclusión final con límites explícitos y archivo de procedimiento reproducible."
        ],
        "checking_criteria": [
            "Los ejes y sentidos están declarados antes de transformar datos.",
            "La matriz conserva distancias y no introduce reflexión.",
            "Todas las magnitudes numéricas llevan unidades.",
            "Las derivadas no se presentan como mediciones directas.",
            "Se muestra cómo una perturbación pequeña afecta especialmente a la aceleración.",
            "La comparación 2D/3D usa los mismos puntos y distingue proyección de cambio físico.",
            "No se impone una frecuencia de filtro ni un umbral de error como regla universal.",
            "El artefacto de tejido blando se reconoce como una limitación de la estimación de pose ósea.",
            "La conclusión diferencia resultado técnico de interpretación y decisión clínica.",
            "Otra persona podría reconstruir el cálculo a partir de los entregables."
        ]
    }
]

unit["common_errors"] = [
    {"error": "Informar coordenadas sin indicar el marco de referencia.", "correction": "Declarar origen, ejes, sentidos y unidades antes de interpretar cualquier trayectoria."},
    {"error": "Intercambiar ejes mediante una reflexión y tratarla como una rotación.", "correction": "Verificar ortogonalidad y determinante +1 de la matriz de rotación y comprobar lateralidad con un punto conocido."},
    {"error": "Usar ΣF = ma como ecuación central de una unidad de cinemática.", "correction": "Reservar fuerzas y causas dinámicas para cinética; aquí describir pose, trayectoria y derivadas temporales."},
    {"error": "Diferenciar coordenadas ruidosas y asumir que la aceleración resultante es estable.", "correction": "Evaluar ruido, frecuencia de muestreo y sensibilidad del procesamiento antes de interpretar derivadas."},
    {"error": "Aplicar siempre el mismo filtro o frecuencia de corte.", "correction": "Justificar el procesamiento según tarea, señal, muestreo y variable final y reportar análisis de sensibilidad cuando sea necesario."},
    {"error": "Interpretar un ángulo 2D como si fuera automáticamente el ángulo articular 3D.", "correction": "Comprobar movimiento fuera del plano y definir la variable geométrica que realmente mide la proyección."},
    {"error": "Suponer que un marcador cutáneo reproduce exactamente la pose del hueso.", "correction": "Reconocer el artefacto de tejido blando y la incertidumbre de referencias anatómicas y modelos segmentarios."},
    {"error": "Convertir una diferencia cinemática en diagnóstico o efecto terapéutico.", "correction": "Limitar la conclusión a la variable y protocolo medidos; la utilidad clínica requiere evidencia adicional independiente."}
]

unit["self_assessment"] = [
    {"question": "¿Por qué una coordenada x,y,z no está completamente definida por sus tres números?", "answer": "Porque necesita un marco de referencia con origen, ejes, sentidos y unidades; los mismos números representan posiciones distintas en marcos distintos.", "reasoning": "La representación numérica es relativa a un sistema de coordenadas.", "common_error": "Asumir que todos los sistemas de captura usan la misma convención."},
    {"question": "¿Qué propiedades debe cumplir una matriz de rotación 3D propia?", "answer": "Debe ser ortogonal, de modo que RᵀR=I, y tener determinante +1.", "reasoning": "Estas propiedades preservan longitud y orientación sin introducir reflexión.", "common_error": "Aceptar una permutación de ejes con determinante −1 porque visualmente parece correcta."},
    {"question": "¿Cuál es la diferencia conceptual entre posición y orientación?", "answer": "La posición localiza un punto; la orientación describe cómo está rotado un marco o segmento respecto a otro.", "reasoning": "Un solo punto no determina la rotación completa de un cuerpo rígido.", "common_error": "Tratar el desplazamiento de un marcador como orientación segmentaria completa."},
    {"question": "¿Por qué la aceleración calculada suele ser más sensible al ruido que la posición?", "answer": "Porque requiere una segunda diferenciación temporal, operación que amplifica componentes de alta frecuencia y errores muestra a muestra.", "reasoning": "Cada derivación aumenta la influencia relativa del ruido de posición.", "common_error": "Interpretar una curva de aceleración irregular como movimiento real sin revisar el procesamiento."},
    {"question": "¿Por qué no existe una frecuencia de corte única válida para toda cinemática humana?", "answer": "Porque el contenido de señal y ruido depende de tarea, muestreo, variable, sensor y objetivo; un corte fijo puede atenuar movimiento real o dejar ruido.", "reasoning": "El filtrado es una decisión de medición y análisis, no una constante fisiológica universal.", "common_error": "Copiar 6 Hz de otro estudio sin justificar equivalencia de condiciones."},
    {"question": "¿Cuándo puede ser razonable un análisis 2D?", "answer": "Cuando la tarea y la variable son aproximadamente planares, la cámara y calibración son adecuadas y el error fuera del plano es aceptable para el uso previsto.", "reasoning": "La suficiencia depende de la pregunta y la geometría, no del número de cámaras por sí solo.", "common_error": "Asumir que 2D siempre es inválido o que siempre es suficiente."},
    {"question": "¿Qué demuestra comparar un ángulo 2D con el ángulo 3D de los mismos vectores?", "answer": "Permite cuantificar el efecto de la proyección para esa configuración y orientación concreta.", "reasoning": "Si el sistema cambia respecto a la cámara, el ángulo proyectado puede variar sin el mismo cambio en 3D.", "common_error": "Generalizar una buena concordancia en un caso a todos los planos y movimientos."},
    {"question": "¿Qué es el artefacto de tejido blando?", "answer": "Es el movimiento de piel y tejidos, y por tanto de marcadores superficiales, respecto al hueso que se intenta representar.", "reasoning": "El sistema óptico observa el marcador, mientras la pose ósea es una inferencia modelada.", "common_error": "Considerar los marcadores una referencia rígida al hueso."},
    {"question": "¿Repetibilidad alta garantiza ausencia de sesgo?", "answer": "No. Un método puede repetir de forma consistente una medición desplazada respecto a la magnitud de referencia.", "reasoning": "Variabilidad aleatoria y error sistemático son dimensiones distintas.", "common_error": "Usar solo repetición para declarar exactitud."},
    {"question": "¿Qué debe conservar un expediente cinemático reproducible?", "answer": "Datos o procedencia, unidades, marcos, muestreo, calibración relevante, transformaciones, procesamiento, código o procedimiento, controles, resultados y límites.", "reasoning": "La variable final debe poder reconstruirse desde la observación original.", "common_error": "Guardar únicamente la figura final o una tabla ya procesada."}
]

unit["biomedical_connections"] = [
    {"topic": "Análisis de marcha", "connection": "Las trayectorias segmentarias y medidas espaciotemporales describen patrones de movimiento, pero su interpretación depende de protocolo, modelo y error de medición."},
    {"topic": "Rehabilitación", "connection": "La cinemática puede cuantificar cambios de movimiento entre sesiones; atribuirlos a recuperación o tratamiento exige diseño y evidencia adicionales."},
    {"topic": "Prótesis y órtesis", "connection": "Comparar configuraciones puede revelar cambios mecánicos observables, siempre que los marcos, tareas y métricas sean equivalentes."},
    {"topic": "Modelado musculoesquelético", "connection": "Los modelos requieren que datos experimentales y coordenadas del modelo compartan una convención compatible antes de ejecutar cinemática inversa."},
    {"topic": "Captura sin marcadores", "connection": "Los métodos de visión reducen algunas cargas de adquisición, pero su validez debe evaluarse por variable, plano y población y no asumirse por similitud visual."}
]

unit["sources"] = [
    {"title": "Standards: Joint coordinate systems", "organization": "International Society of Biomechanics", "year": 2026, "url": "https://www.isbweb.org/activities/standards", "type": "estándares y recomendaciones profesionales", "description": "Portal de la ISB que reúne propuestas y recomendaciones para sistemas de coordenadas articulares y terminología de movimiento humano.", "verification_status": "verified_directly", "locator": "Standards → Joint coordinate systems", "limitations": "El portal enlaza recomendaciones por articulación; la implementación debe respetar la publicación y versión concreta aplicable."},
    {"title": "ISB recommendation on definitions of joint coordinate system—part I: ankle, hip, and spine", "organization": "Journal of Biomechanics / International Society of Biomechanics", "year": 2002, "url": "https://pubmed.ncbi.nlm.nih.gov/11934426/", "doi": "10.1016/S0021-9290(01)00222-6", "type": "recomendación de estandarización", "description": "Propone sistemas de coordenadas para reportar cinemática de tobillo, cadera y columna.", "verification_status": "verified_directly", "locator": "J Biomech. 2002;35(4):543-548; PMID 11934426", "limitations": "No sustituye la descripción del protocolo experimental ni elimina diferencias entre modelos musculoesqueléticos."},
    {"title": "Position and orientation in space of bones during movement: anatomical frame definition and determination", "organization": "Clinical Biomechanics", "year": 1995, "url": "https://pubmed.ncbi.nlm.nih.gov/11415549/", "doi": "10.1016/0268-0033(95)91394-T", "type": "artículo metodológico", "description": "Formaliza referencias anatómicas y reconstrucción de posición y orientación ósea en análisis de movimiento.", "verification_status": "verified_directly", "locator": "Clin Biomech. 1995;10(4):171-178; PMID 11415549", "limitations": "Describe un marco metodológico clásico basado en estereofotogrametría; tecnologías posteriores requieren validación específica."},
    {"title": "Coordinate Systems in OpenSim", "organization": "OpenSim", "year": 2024, "url": "https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53090629", "type": "documentación técnica oficial", "description": "Explica compatibilidad y transformaciones entre coordenadas de laboratorio, modelo y sensores en OpenSim.", "verification_status": "verified_directly", "locator": "Introduction; Simple Coordinate Transformations; How to Apply Transformations to Data", "limitations": "Documenta convenciones de OpenSim; otros sistemas pueden usar ejes y convenciones diferentes."},
    {"title": "Measurement and reduction of noise in kinematics of locomotion", "organization": "Journal of Biomechanics", "year": 1974, "url": "https://pubmed.ncbi.nlm.nih.gov/4837552/", "doi": "10.1016/0021-9290(74)90056-6", "type": "artículo metodológico", "description": "Demuestra que el ruido de posición puede producir errores grandes al obtener velocidades y aceleraciones por diferenciación.", "verification_status": "verified_directly", "locator": "J Biomech. 1974;7(2):157-159; PMID 4837552", "limitations": "El hardware es histórico; el principio de amplificación del ruido por diferenciación sigue siendo relevante, pero los parámetros concretos no deben copiarse como regla moderna."},
    {"title": "Filtering Biomechanical Signals in Movement Analysis", "organization": "Sensors", "year": 2021, "url": "https://pubmed.ncbi.nlm.nih.gov/34283131/", "doi": "10.3390/s21134580", "type": "estudio metodológico abierto", "description": "Compara procesamiento y filtrado para mediciones biomecánicas y derivadas con atención a incertidumbre.", "verification_status": "verified_directly", "locator": "Sensors. 2021;21(13):4580; PMID 34283131", "limitations": "No establece un único filtro universal; las condiciones experimentales y la señal determinan la estrategia apropiada."},
    {"title": "Position and orientation in space of bones during movement: experimental artefacts", "organization": "Clinical Biomechanics", "year": 1996, "url": "https://pubmed.ncbi.nlm.nih.gov/11415604/", "doi": "10.1016/0268-0033(95)00046-1", "type": "artículo experimental", "description": "Analiza movimiento relativo entre marcadores cutáneos y hueso y su efecto en la reconstrucción segmentaria.", "verification_status": "verified_directly", "locator": "Clin Biomech. 1996;11(2):90-100; PMID 11415604", "limitations": "Resultados cuantitativos dependen de segmentos, participantes, tarea y protocolo; no son un error fijo universal."},
    {"title": "Applications and limitations of current markerless motion capture methods for clinical gait biomechanics", "organization": "PeerJ", "year": 2022, "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8884063/", "type": "revisión de alcance abierta", "description": "Revisa métodos de captura sin marcadores y diferencia desempeño espaciotemporal, localización articular y cinemática en aplicaciones de marcha.", "verification_status": "verified_directly", "locator": "Abstract; Marker-Based Motion Capture; Markerless Motion Capture", "limitations": "La tecnología evoluciona rápidamente; resultados de algoritmos y configuraciones concretas no deben generalizarse a nuevos sistemas sin validación."}
]

unit["editorial_notice"] = (
    "Unidad curada académicamente con fuentes metodológicas y profesionales verificadas directamente. "
    "El contenido permanece en estado review y no constituye revisión disciplinar externa, validación clínica ni recomendación diagnóstica o terapéutica. "
    "Las actividades son sintéticas y reproducibles; no requieren registrar personas ni utilizar equipamiento biomédico con participantes."
)

serialized = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
if MARKER.casefold() in serialized.casefold():
    raise SystemExit("El marcador genérico sigue presente en Biomecánica U1")
SOURCE.write_text(serialized, encoding="utf-8")
MIRROR.write_text(serialized, encoding="utf-8")
print("Curated Biomecanica U1 and synchronized exact redevelopment mirror")
