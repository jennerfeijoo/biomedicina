#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-04.json"
GENERIC = "Concepto de la unidad que debe definirse mediante entidades observables"


def dump(payload: dict) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    SOURCE.write_text(text, encoding="utf-8")
    MIRROR.write_text(text, encoding="utf-8")


def main() -> None:
    unit = json.loads(SOURCE.read_text(encoding="utf-8"))
    unit["purpose"] = (
        "Construir una estrategia de mercado reproducible para una tecnología médica sintética mediante definición del problema, "
        "segmentación de mercado, selección del segmento objetivo, análisis de alternativas y competencia, propuesta de valor y "
        "posicionamiento. La unidad distingue usuario, comprador, pagador, decisor y beneficiario; documenta supuestos y sensibilidad; "
        "y separa explícitamente atractivo comercial, valor clínico, aprobación regulatoria, evaluación de tecnologías sanitarias y decisión real de compra."
    )
    unit["learning_objectives"] = [
        "Definir el mercado relevante y segmentarlo en grupos de organizaciones o usuarios con necesidades, comportamientos o características comunes, sin confundir segmentación de mercado con segmentación de imágenes biomédicas.",
        "Seleccionar un segmento objetivo usando criterios explícitos de necesidad, accesibilidad, tamaño aproximado, capacidad de adopción, ajuste con la solución y calidad de la evidencia, diferenciando descripción de recomendación comercial real.",
        "Mapear el centro de compra de una organización sanitaria distinguiendo iniciador, usuario, influenciador, comprador, decisor y gatekeeper, y explicar por qué paciente, usuario, comprador y pagador pueden no coincidir.",
        "Analizar competencia y sustitutos mediante alternativas relevantes, dimensiones de comparación y fuentes verificables, evitando tratar ausencia de datos como ausencia de competencia.",
        "Redactar y someter a prueba una propuesta de valor y un posicionamiento que conecten necesidad, beneficio, evidencia, alternativa de referencia y límites sin convertir una promesa de mercado en afirmación clínica no demostrada.",
        "Construir escenarios sintéticos de tamaño y prioridad de mercado con supuestos trazables y análisis de sensibilidad, comunicando qué cambia al variar penetración, población accesible, precio o tasa de adopción."
    ]
    unit["theory_sections"] = [
        {
            "heading": "1. Mercado relevante, segmentación y selección del objetivo",
            "paragraphs": [
                "En estrategia, segmentar significa dividir un mercado en grupos más homogéneos respecto de necesidades, características o respuesta esperada a una acción de marketing. No significa etiquetar píxeles ni vóxeles. El primer requisito es definir qué se segmenta: personas, organizaciones, servicios, centros sanitarios o procesos de compra. En tecnología médica suele ser útil comenzar por organizaciones y contextos de uso, porque la compra es frecuentemente B2B y la persona que usa la tecnología puede no ser quien autoriza o paga la adquisición.",
                "Un segmento útil debe describirse con variables que puedan observarse o justificarse. En B2B pueden incluir tipo de institución, tamaño, especialidad, infraestructura, tecnologías instaladas, volumen de actividad, necesidades operativas o comportamiento de compra. La segmentación basada en necesidades pregunta qué problema intenta resolver el cliente organizacional y qué requisitos considera decisivos. Un grupo creado solo porque comparte una etiqueta administrativa puede no responder de forma suficientemente similar como para sostener una estrategia diferenciada.",
                "Segmentar no equivale a seleccionar. Después de describir grupos, el equipo decide qué segmento analizar como objetivo y documenta los criterios usados: magnitud y urgencia de la necesidad, posibilidad de acceso, ajuste técnico de la solución, recursos del proveedor, evidencia disponible, barreras de adopción y sostenibilidad. Esta selección es una decisión estratégica bajo incertidumbre; no demuestra que ese mercado vaya a comprar ni que la tecnología produzca valor clínico.",
                "En salud, el lenguaje de segmentación exige cautela ética. Una estrategia académica puede describir instituciones o escenarios sintéticos, pero no debe utilizar datos personales para perfilar pacientes ni convertir vulnerabilidad clínica en criterio de explotación comercial. Para esta unidad se emplean exclusivamente organizaciones ficticias, agregados públicos o cifras sintéticas. Cuando una característica afecta acceso, equidad o seguridad, se registra como restricción del análisis y no como simple oportunidad de mercado.",
                "La salida mínima de esta etapa es una tabla de segmentos con definición, necesidad, evidencia, tamaño aproximado, acceso y barreras, seguida de una justificación del segmento objetivo. Otra persona debe poder reconstruir por qué dos organizaciones fueron agrupadas o separadas y qué dato podría cambiar la elección. La trazabilidad evita que etiquetas intuitivas se conviertan en hechos sin fundamento."
            ],
            "key_points": [
                "Segmentación de mercado agrupa clientes u organizaciones; no tiene relación con segmentar imágenes.",
                "La unidad de segmentación y las variables usadas deben declararse antes de comparar grupos.",
                "Seleccionar un segmento objetivo es una decisión posterior y distinta de segmentar.",
                "La elección del objetivo debe conservar incertidumbre, barreras de adopción y límites éticos."
            ]
        },
        {
            "heading": "2. Centro de compra, competencia, sustitutos y marco de referencia",
            "paragraphs": [
                "Las compras organizacionales suelen involucrar varias personas con papeles diferentes. Un centro de compra puede incluir iniciadores que detectan una necesidad, usuarios que operarán la solución, influenciadores técnicos o clínicos, gatekeepers que controlan información, compradores que gestionan proveedores y decisores que autorizan la elección. En tecnología médica también puede existir un pagador distinto del comprador y un paciente beneficiario que no participa directamente en la transacción. Confundir estos roles puede producir una propuesta de valor dirigida a la persona equivocada.",
                "Analizar competencia no consiste en listar marcas. La pregunta es qué alternativas compiten por resolver la misma necesidad y por los mismos recursos. Una solución puede competir contra otro dispositivo, una prueba diferente, software, externalización, un proceso manual o incluso la decisión de mantener el estado actual. Por ello se define primero el problema y luego se buscan alternativas directas, indirectas y sustitutos. La ausencia de un producto idéntico no implica ausencia de competencia.",
                "Una matriz competitiva compara alternativas sobre dimensiones previamente justificadas: desempeño para el uso previsto, integración, formación, mantenimiento, tiempo de implementación, coste total, evidencia, interoperabilidad o requisitos de infraestructura. Las puntuaciones deben enlazarse a una fuente o marcarse como supuesto. No se asigna una puntuación cero cuando falta información; se registra 'desconocido'. Esta regla evita convertir vacíos de evidencia en ventajas artificiales.",
                "El marco de las cinco fuerzas de Porter amplía la mirada más allá de rivales actuales al considerar también compradores, proveedores, entrantes potenciales y sustitutos. En U4 se utiliza cualitativamente para preguntar dónde existe presión estructural y qué supuestos deberían investigarse; no se usa como algoritmo que entregue una estrategia correcta. La importancia de cada fuerza depende del mercado definido y puede variar entre países, sistemas de salud y canales de compra.",
                "El resultado de esta etapa es un mapa de actores y alternativas con fuente, fecha, nivel de confianza y pregunta pendiente. La comparación debe distinguir datos observados, inferencias y escenarios. En particular, una diferencia comercial favorable no autoriza afirmar superioridad clínica, seguridad, aprobación regulatoria o elegibilidad para reembolso. Esas preguntas pertenecen a procesos de evidencia y decisión diferentes."
            ],
            "key_points": [
                "Usuario, comprador, pagador, decisor y beneficiario pueden ser actores diferentes.",
                "La competencia incluye sustitutos y el estado actual, no solo productos similares.",
                "Una matriz competitiva debe distinguir evidencia de supuesto y desconocido de desempeño deficiente.",
                "El análisis competitivo no demuestra superioridad clínica ni acceso regulatorio."
            ]
        },
        {
            "heading": "3. Propuesta de valor, posicionamiento y escenarios de tamaño de mercado",
            "paragraphs": [
                "Una propuesta de valor conecta un segmento definido con un problema relevante y explica qué beneficio espera ofrecer una solución frente a una alternativa de referencia. Debe ser específica respecto del actor: el usuario puede valorar facilidad de uso, el comprador coste total, el decisor compatibilidad institucional y el paciente un resultado de salud. Una sola frase que mezcla beneficios para todos los actores suele ocultar conflictos y evidencia insuficiente.",
                "El posicionamiento describe cómo se quiere que el segmento objetivo entienda una solución en relación con alternativas. Una formulación auditable identifica segmento, necesidad, categoría o marco de referencia, beneficio diferencial y evidencia que lo respalda. Un mapa perceptual puede representar dos dimensiones relevantes, pero sus ejes y posiciones son hipótesis si no proceden de investigación de mercado. La visualización no convierte opiniones internas en percepción real del mercado.",
                "Los claims de la propuesta de valor deben clasificarse. Un claim operativo —por ejemplo, menor tiempo de preparación en una prueba controlada— necesita evidencia diferente de un claim clínico sobre resultados en pacientes. Del mismo modo, una afirmación de ahorro requiere definir perspectiva, horizonte y componentes de coste. La unidad obliga a redactar una versión fuerte del claim y luego una versión proporcional a la evidencia disponible; si la evidencia no existe, la afirmación queda como hipótesis a probar.",
                "El tamaño de mercado se trabaja como escenario, no como pronóstico. Un enfoque descendente puede partir de un universo amplio y aplicar filtros justificados; uno ascendente puede contar organizaciones accesibles, unidades por organización y una hipótesis de adopción. TAM, SAM y SOM son etiquetas útiles solo si cada conjunto tiene una definición operacional. Un SOM no debe ser un porcentaje arbitrario del TAM: requiere una justificación basada en acceso, capacidad comercial, tiempo, competencia y restricciones.",
                "Los escenarios deben someterse a sensibilidad. Si un mercado accesible contiene 120 centros sintéticos, la adopción esperada cambia de 12 a 36 centros al variar una hipótesis de penetración de 10 % a 30 %. El resultado útil no es escoger el número más atractivo, sino mostrar qué supuestos dominan la estimación y qué evidencia reduciría la incertidumbre. U4 evita presentar estas cifras como previsiones financieras reales."
            ],
            "equations": [
                {"latex": "N_{adoptantes}=N_{accesibles}\\times p_{adopcion}", "meaning": "Escenario elemental de adopción para explorar sensibilidad; no es un pronóstico de ventas.", "variables": {"N_{adoptantes}": "número sintético de organizaciones adoptantes", "N_{accesibles}": "organizaciones que cumplen la definición de mercado accesible", "p_{adopcion}": "hipótesis explícita de proporción de adopción"}},
                {"latex": "V_{escenario}=N_{adoptantes}\\times q\\times P", "meaning": "Valor monetario sintético del escenario bajo cantidad y precio declarados; excluye costes, descuentos, impuestos y dinámica temporal salvo que se modelen aparte.", "variables": {"V_{escenario}": "valor bruto sintético", "q": "unidades por organización", "P": "precio hipotético por unidad"}}
            ],
            "key_points": [
                "La propuesta de valor debe especificar segmento, problema, beneficio, alternativa y evidencia.",
                "Posicionamiento es una hipótesis sobre percepción relativa y no demuestra desempeño clínico.",
                "TAM, SAM y SOM requieren definiciones operacionales y supuestos trazables.",
                "El análisis de sensibilidad es más informativo que una única cifra de mercado."
            ]
        },
        {
            "heading": "4. Estrategia de adopción responsable y límites frente a regulación, HTA y compra real",
            "paragraphs": [
                "Una estrategia de mercado en tecnología médica debe reconocer que acceso al mercado, adopción por un sistema sanitario y gestión de la tecnología son decisiones relacionadas pero distintas. La OMS describe la aprobación regulatoria, la evaluación de tecnologías sanitarias y la gestión de tecnologías como funciones complementarias. Por tanto, un buen posicionamiento no reemplaza autorización regulatoria, evaluación clínica, HTA, contratación ni procedimientos locales de compra.",
                "La evaluación de tecnologías sanitarias examina de forma multidisciplinaria propiedades y consecuencias de una tecnología para informar decisiones de política, adopción o reembolso. U4 utiliza esta frontera para enseñar modestia inferencial: demostrar que un segmento tiene una necesidad y que una solución parece atractiva comercialmente no establece efectividad comparativa, coste-efectividad, impacto presupuestario ni valor social. Esos dominios requieren métodos específicos y U5 profundiza en evaluación económica.",
                "La estrategia de adopción se formula como una cadena de hipótesis verificables: necesidad → actor → barrera → propuesta → evidencia requerida → prueba de aprendizaje → criterio de revisión. En lugar de recomendar un lanzamiento real, la actividad académica diseña entrevistas sintéticas, escenarios o pruebas de mensaje con criterios previos. Cada paso registra qué resultado apoyaría la hipótesis, qué resultado la debilitaría y qué riesgo impediría avanzar.",
                "Una tecnología puede ser atractiva para un usuario y poco viable para un comprador; puede ahorrar tiempo local y aumentar carga en otra unidad; o puede tener evidencia clínica pero no encajar con infraestructura o presupuesto. Por eso la estrategia incluye al menos una medida de beneficio, una barrera, una consecuencia distributiva y una alternativa de referencia. La mejor conclusión puede ser 'evidencia insuficiente para priorizar' cuando el supuesto dominante no está verificado.",
                "El entregable final es un memorando estratégico reproducible para un caso sintético. Incluye mercado definido, segmentos, objetivo, actores de compra, alternativas, propuesta de valor, posicionamiento, escenario de tamaño, sensibilidad, claims y fuentes. También separa explícitamente lo que el ejercicio permite afirmar de lo que requeriría investigación clínica, regulación, HTA, contratación, aprobación institucional o datos reales."
            ],
            "key_points": [
                "Acceso regulatorio, HTA, adopción y gestión tecnológica son procesos distintos aunque relacionados.",
                "Atractivo de mercado no equivale a efectividad, coste-efectividad ni valor para el sistema sanitario.",
                "La estrategia debe expresarse como hipótesis verificables con criterios de revisión.",
                "El memorando final separa hechos, supuestos, sensibilidad y evidencia pendiente."
            ]
        }
    ]
    unit["glossary"] = [
        {"term": "mercado relevante", "definition": "Conjunto explícitamente delimitado de clientes, organizaciones, necesidades, alternativas y ámbito geográfico o institucional para los que se realiza el análisis."},
        {"term": "segmentación de mercado", "definition": "División de un mercado en grupos con características, necesidades o respuestas suficientemente comunes para analizarlos de forma diferenciada."},
        {"term": "segmento objetivo", "definition": "Segmento seleccionado para concentrar el análisis o los recursos según criterios explícitos de ajuste, necesidad, acceso y evidencia."},
        {"term": "B2B", "definition": "Relación de mercado entre organizaciones; en salud puede involucrar procesos de compra con múltiples actores y reglas institucionales."},
        {"term": "centro de compra", "definition": "Conjunto de personas que participan o influyen en una decisión de compra organizacional con roles distintos."},
        {"term": "usuario", "definition": "Actor que utiliza directamente la solución; no necesariamente compra, paga o autoriza su adquisición."},
        {"term": "comprador", "definition": "Actor u organización con responsabilidad sobre selección de proveedor, negociación o ejecución de la compra."},
        {"term": "pagador", "definition": "Actor que financia total o parcialmente una tecnología o servicio y cuyos incentivos pueden diferir de los del usuario."},
        {"term": "decisor", "definition": "Actor con autoridad para aprobar o rechazar una alternativa dentro del proceso de compra definido."},
        {"term": "gatekeeper", "definition": "Actor que controla el acceso a información, personas o etapas del proceso de compra."},
        {"term": "competidor directo", "definition": "Alternativa que ofrece una solución comparable para la misma necesidad dentro del mercado definido."},
        {"term": "sustituto", "definition": "Alternativa diferente que puede satisfacer la misma necesidad o evitar la compra de la solución analizada."},
        {"term": "estado actual", "definition": "Forma vigente de resolver o no resolver el problema; debe considerarse una alternativa de referencia cuando corresponda."},
        {"term": "propuesta de valor", "definition": "Explicación del beneficio relevante que una solución pretende aportar a un segmento específico frente a una alternativa, junto con la evidencia y límites disponibles."},
        {"term": "posicionamiento", "definition": "Hipótesis estratégica sobre cómo debe entenderse una solución en relación con alternativas dentro de la mente del segmento objetivo."},
        {"term": "mapa perceptual", "definition": "Representación de alternativas sobre dimensiones relevantes para explorar posicionamiento; requiere datos externos si pretende representar percepciones reales."},
        {"term": "claim", "definition": "Afirmación verificable sobre una característica, beneficio o resultado cuya fuerza debe ser proporcional a la evidencia que la respalda."},
        {"term": "TAM", "definition": "Mercado total direccionable según una definición explícita del universo que podría necesitar o adquirir una solución bajo supuestos idealizados."},
        {"term": "SAM", "definition": "Parte del TAM que puede atenderse dadas restricciones de producto, geografía, canal, regulación, infraestructura u otras condiciones declaradas."},
        {"term": "SOM", "definition": "Parte del mercado accesible que se modela como capturable en un horizonte y con recursos definidos; es un escenario, no una garantía."},
        {"term": "sensibilidad", "definition": "Evaluación de cuánto cambia una conclusión cuando se modifican supuestos o parámetros plausibles."},
        {"term": "HTA", "definition": "Evaluación multidisciplinaria de tecnologías sanitarias que examina propiedades y consecuencias para informar decisiones; no equivale a marketing ni aprobación regulatoria."}
    ]
    unit["worked_examples"] = [
        {
            "title": "Corregir una segmentación contaminada por otro dominio",
            "scenario": "Un borrador define segmentación como clasificación de píxeles y propone usarla para posicionar un monitor médico.",
            "reasoning_steps": ["Identificar que la definición pertenece a procesamiento de imágenes y no a marketing.", "Definir la unidad de análisis como organizaciones sanitarias ficticias.", "Crear segmentos por necesidad, infraestructura y proceso de compra.", "Separar segmentación de selección del objetivo.", "Registrar qué dato faltaría para validar los grupos con mercado real."],
            "answer": "La segmentación correcta agrupa organizaciones o clientes por diferencias relevantes para necesidad y respuesta comercial; los píxeles/vóxeles quedan fuera del dominio de U4.",
            "interpretation": "La corrección restablece coherencia disciplinar, pero no demuestra que los segmentos sintéticos existan con la misma estructura en un mercado real."
        },
        {
            "title": "Centro de compra de un dispositivo sintético",
            "scenario": "Un hospital ficticio evalúa un sistema de monitorización. Enfermería lo usaría, ingeniería clínica revisa integración, compras negocia y una dirección autoriza.",
            "reasoning_steps": ["Identificar usuario, influenciador técnico, comprador y decisor.", "Añadir pagador o presupuesto si difiere del comprador.", "Escribir una necesidad distinta para cada actor.", "Detectar conflictos entre facilidad de uso, integración y coste.", "Redactar qué actor debe aportar evidencia para cada decisión."],
            "answer": "No existe un único 'cliente': el centro de compra contiene roles con criterios distintos y la propuesta debe declarar a cuál responde cada beneficio.",
            "interpretation": "Mapear roles ayuda a formular hipótesis de adopción; no reemplaza entrevistas, contratación ni gobernanza institucional."
        },
        {
            "title": "Competidor, sustituto y estado actual",
            "scenario": "Una herramienta sintética automatiza una medición que hoy se realiza manualmente; existe además un servicio externalizado.",
            "reasoning_steps": ["Definir la necesidad sin mencionar la solución propia.", "Clasificar una herramienta similar como competidor directo.", "Clasificar la externalización como sustituto.", "Incluir proceso manual como estado actual.", "Comparar dimensiones y marcar desconocidos sin convertirlos en ceros."],
            "answer": "El conjunto competitivo incluye alternativas que resuelven la misma necesidad aunque utilicen tecnologías diferentes.",
            "interpretation": "Una matriz competitiva organiza evidencia; no demuestra superioridad clínica ni futura cuota de mercado."
        },
        {
            "title": "Propuesta de valor proporcional a la evidencia",
            "scenario": "Una prueba sintética muestra 20 % menos tiempo de preparación, pero no midió desenlaces clínicos ni costes totales.",
            "reasoning_steps": ["Separar el hallazgo operativo de claims clínicos y económicos.", "Identificar el actor para quien el tiempo tiene valor.", "Elegir el proceso actual como referencia.", "Redactar un claim limitado al tiempo de preparación en las condiciones estudiadas.", "Listar evidencia adicional necesaria antes de afirmar ahorro o beneficio clínico."],
            "answer": "La propuesta puede destacar reducción observada del tiempo de preparación bajo el escenario probado, pero no afirmar mejor resultado clínico ni ahorro total.",
            "interpretation": "El posicionamiento debe ser proporcional a la evidencia y actualizarse cuando cambie el conjunto de datos."
        },
        {
            "title": "Escenario TAM–SAM–SOM con sensibilidad",
            "scenario": "Un ejercicio contiene 500 centros potenciales, 120 con infraestructura compatible y una penetración hipotética de 10–30 %.",
            "reasoning_steps": ["Definir TAM como los 500 centros según el universo del ejercicio.", "Definir SAM como los 120 centros compatibles, documentando filtros.", "Calcular SOM de escenario: 12–36 centros para 10–30 %.", "Evitar presentar 12–36 como pronóstico.", "Identificar penetración e infraestructura como supuestos que dominan la cifra."],
            "answer": "El SOM sintético varía entre 12 y 36 centros; el intervalo expresa sensibilidad a una hipótesis, no incertidumbre estadística ni ventas esperadas.",
            "interpretation": "El ejercicio enseña trazabilidad de supuestos; una estimación comercial real exigiría investigación, horizonte temporal, competencia, capacidad y datos de mercado."
        }
    ]
    unit["guided_activities"] = [
        {
            "title": "Actividad guiada: estrategia de mercado para una tecnología médica sintética",
            "duration_minutes": 270,
            "instructions": [
                "Trabaja únicamente con el caso sintético proporcionado; no uses datos personales, historias clínicas ni información confidencial de organizaciones reales.",
                "Define la necesidad antes de nombrar la solución y fija una frontera geográfica/institucional ficticia.",
                "Construye al menos cuatro segmentos usando variables observables y explica por qué pertenecen juntos.",
                "Selecciona un segmento objetivo mediante una matriz de criterios y conserva una alternativa razonable.",
                "Mapea el centro de compra y distingue usuario, comprador, pagador, influenciador, gatekeeper y decisor cuando apliquen.",
                "Lista competidores directos, sustitutos y estado actual; marca como desconocida toda característica sin evidencia.",
                "Redacta una propuesta de valor y clasifica cada claim como operativo, económico, clínico u otro.",
                "Construye un posicionamiento y un mapa perceptual hipotético, etiquetándolo explícitamente como hipótesis.",
                "Calcula un TAM, SAM y SOM sintéticos con definiciones operacionales y muestra al menos tres escenarios de adopción.",
                "Cierra separando mercado, evidencia clínica, regulación, HTA, compra y adopción real; indica qué evidencia adicional necesitaría cada transición."
            ],
            "problems": [
                "Definir en una frase la necesidad central sin mencionar producto ni marca.",
                "Definir la unidad de segmentación.",
                "Proponer cuatro variables de segmentación B2B relevantes.",
                "Crear cuatro segmentos mutuamente comprensibles y describir su necesidad.",
                "Identificar una variable que no sería útil para segmentar y justificar por qué.",
                "Construir una matriz de selección con al menos cinco criterios.",
                "Elegir un segmento objetivo y justificar la renuncia a otro.",
                "Dibujar el centro de compra del segmento elegido.",
                "Distinguir usuario, comprador, pagador y decisor.",
                "Identificar dos competidores directos ficticios.",
                "Identificar dos sustitutos o alternativas de no compra.",
                "Construir una matriz competitiva con cinco dimensiones.",
                "Marcar explícitamente tres datos desconocidos.",
                "Redactar una propuesta de valor de una frase.",
                "Descomponerla en problema, beneficio, alternativa y evidencia.",
                "Detectar y corregir un claim clínico no respaldado.",
                "Construir un mapa perceptual con dos ejes justificados.",
                "Definir TAM y aplicar filtros para obtener SAM.",
                "Calcular SOM para tres hipótesis de adopción.",
                "Realizar sensibilidad a una segunda variable crítica.",
                "Explicar por qué el SOM no es un pronóstico de ventas.",
                "Separar atractivo de mercado de aprobación regulatoria.",
                "Separar atractivo de mercado de HTA o reembolso.",
                "Escribir una conclusión limitada y tres preguntas pendientes."
            ],
            "deliverables": [
                "Definición del mercado y de la necesidad.",
                "Tabla de segmentos y variables.",
                "Matriz de selección del segmento objetivo.",
                "Mapa del centro de compra.",
                "Mapa de competencia y sustitutos.",
                "Matriz competitiva con fuentes/supuestos/desconocidos.",
                "Propuesta de valor y tabla de claims.",
                "Mapa de posicionamiento hipotético.",
                "Hoja TAM–SAM–SOM con tres escenarios y sensibilidad.",
                "Memorando final con límites y evidencia pendiente."
            ],
            "checking_criteria": [
                "La segmentación se refiere a mercado y no contiene píxeles, vóxeles ni procesamiento de imagen.",
                "La unidad de segmentación y el mercado relevante están definidos.",
                "Los segmentos se basan en diferencias relevantes y no en etiquetas arbitrarias.",
                "La selección del objetivo usa criterios explícitos y no confunde tamaño con atractivo total.",
                "El centro de compra distingue roles y no supone que usuario y comprador son la misma persona.",
                "La competencia incluye sustitutos y estado actual.",
                "Los desconocidos se conservan como desconocidos y no se puntúan como ausencia de desempeño.",
                "Cada claim está vinculado a evidencia o marcado como hipótesis.",
                "El posicionamiento no afirma superioridad clínica sin evidencia.",
                "TAM, SAM y SOM tienen definiciones y filtros reproducibles.",
                "La sensibilidad modifica al menos dos supuestos plausibles.",
                "El memorando separa mercado, regulación, HTA, compra real y evidencia clínica.",
                "No se usan datos personales ni confidenciales.",
                "La conclusión indica límites y siguiente evidencia necesaria."
            ]
        }
    ]
    unit["common_errors"] = [
        {"error": "Definir segmentación como clasificación de píxeles o vóxeles.", "correction": "Usar segmentación de mercado: grupos de clientes u organizaciones con necesidades o características relevantes comunes."},
        {"error": "Elegir un segmento antes de definir el mercado.", "correction": "Fijar primero unidad, necesidad, ámbito y alternativas; después segmentar y seleccionar."},
        {"error": "Suponer que usuario, comprador y pagador son el mismo actor.", "correction": "Mapear el centro de compra y asignar a cada rol sus criterios y evidencia."},
        {"error": "Listar solo productos idénticos como competencia.", "correction": "Incluir sustitutos, soluciones alternativas y estado actual."},
        {"error": "Puntuar como cero una característica desconocida del competidor.", "correction": "Registrar 'desconocido' y mantener la incertidumbre visible."},
        {"error": "Presentar una propuesta de valor como hecho clínico.", "correction": "Separar promesa estratégica de claim verificable y limitarla a la evidencia disponible."},
        {"error": "Confundir posicionamiento deseado con percepción real.", "correction": "Etiquetar el mapa como hipótesis hasta disponer de investigación externa."},
        {"error": "Definir SOM como un porcentaje arbitrario del TAM.", "correction": "Derivarlo de mercado accesible, recursos, adopción, horizonte y restricciones documentadas."},
        {"error": "Usar una sola cifra de tamaño de mercado.", "correction": "Mostrar escenarios y sensibilidad a supuestos dominantes."},
        {"error": "Confundir atractivo comercial con aprobación regulatoria.", "correction": "Tratar regulación como proceso separado con requisitos propios."},
        {"error": "Confundir atractivo comercial con HTA o reembolso.", "correction": "Reconocer que HTA evalúa evidencia y consecuencias para decisiones sanitarias mediante métodos específicos."},
        {"error": "Usar datos de pacientes para un ejercicio de marketing académico.", "correction": "Trabajar con datos sintéticos, agregados públicos o escenarios ficticios y respetar gobernanza de datos."},
        {"error": "Ocultar barreras o segmentos desfavorables para fortalecer la narrativa.", "correction": "Conservar evidencia negativa, alternativas y razones por las que una estrategia podría fallar."}
    ]
    unit["self_assessment"] = [
        {"question": "¿Qué significa segmentación en U4?", "answer": "Dividir un mercado en grupos de clientes u organizaciones con características, necesidades o respuestas relevantes comunes.", "reasoning": "La unidad trata estrategia de mercado, no procesamiento de imágenes.", "common_error": "Responder con regiones de interés, píxeles o vóxeles."},
        {"question": "¿Segmentar y seleccionar mercado objetivo son lo mismo?", "answer": "No. Primero se describen segmentos; después se elige cuál analizar o priorizar con criterios explícitos.", "reasoning": "La separación evita construir segmentos para justificar una elección ya tomada.", "common_error": "Llamar segmento a cualquier grupo elegido por conveniencia."},
        {"question": "¿Por qué un dispositivo médico puede tener varios 'clientes'?", "answer": "Porque usuario, influenciador, comprador, pagador y decisor pueden ser personas u organizaciones diferentes.", "reasoning": "Las compras B2B complejas distribuyen roles y criterios.", "common_error": "Dirigir toda la propuesta únicamente al usuario final."},
        {"question": "¿Qué es un sustituto?", "answer": "Una alternativa diferente que resuelve la misma necesidad o evita comprar la solución analizada.", "reasoning": "La competencia se define por la necesidad, no solo por similitud tecnológica.", "common_error": "Ignorar procesos manuales o externalización."},
        {"question": "¿Qué hacer si falta un dato de un competidor?", "answer": "Marcarlo como desconocido y buscar evidencia; no convertirlo en cero.", "reasoning": "Ausencia de información no equivale a mal desempeño.", "common_error": "Favorecer artificialmente la solución propia."},
        {"question": "¿Qué debe contener una propuesta de valor auditable?", "answer": "Segmento, problema, beneficio, alternativa de referencia, evidencia y límites.", "reasoning": "Estos elementos permiten evaluar si la promesa está respaldada.", "common_error": "Usar adjetivos como innovador o superior sin criterio verificable."},
        {"question": "¿Un mapa perceptual interno demuestra cómo piensa el mercado?", "answer": "No. Es una hipótesis hasta obtener datos de percepción relevantes.", "reasoning": "La visualización no crea evidencia externa.", "common_error": "Tratar posiciones elegidas por el equipo como datos medidos."},
        {"question": "¿Qué distingue TAM de SAM?", "answer": "TAM representa el universo direccionable definido; SAM aplica restricciones que determinan qué parte puede atenderse.", "reasoning": "Los filtros deben ser explícitos y reproducibles.", "common_error": "Usar ambos términos como sinónimos de mercado grande y pequeño."},
        {"question": "¿Qué representa SOM en esta unidad?", "answer": "Un escenario de parte accesible/capturable bajo supuestos de adopción, recursos, tiempo y competencia.", "reasoning": "No es una garantía ni un pronóstico de ventas.", "common_error": "Elegir 1 %, 5 % o 10 % del TAM sin justificación."},
        {"question": "¿Por qué hacer sensibilidad?", "answer": "Para identificar qué supuestos cambian más la conclusión y priorizar la evidencia que reduciría incertidumbre.", "reasoning": "Una cifra única oculta dependencia de hipótesis.", "common_error": "Cambiar solo supuestos que mejoran el resultado."},
        {"question": "¿Mercado atractivo implica aprobación regulatoria?", "answer": "No. Son evaluaciones distintas con criterios diferentes.", "reasoning": "Una oportunidad comercial no demuestra seguridad, desempeño ni cumplimiento regulatorio.", "common_error": "Usar interés de compradores como prueba de autorización."},
        {"question": "¿Mercado atractivo implica HTA favorable o reembolso?", "answer": "No. HTA evalúa propiedades y consecuencias de la tecnología para decisiones sanitarias mediante evidencia específica.", "reasoning": "Adopción/reembolso requieren procesos que no se sustituyen con marketing.", "common_error": "Presentar willingness-to-buy como coste-efectividad."},
        {"question": "¿Qué conclusión es válida si el supuesto dominante no está verificado?", "answer": "Que la prioridad estratégica permanece incierta y que se necesita evidencia adicional sobre ese supuesto.", "reasoning": "La incertidumbre debe cambiar la fuerza de la recomendación.", "common_error": "Elegir el escenario optimista como conclusión final."}
    ]
    unit["biomedical_connections"] = [
        {"connection": "Compra hospitalaria de tecnologías", "explanation": "Permite distinguir usuario, ingeniería clínica, compras, dirección y pagador dentro de decisiones organizacionales complejas."},
        {"connection": "Innovación medtech", "explanation": "Ayuda a formular propuesta de valor y posicionamiento sin confundir necesidades de mercado con evidencia clínica o regulatoria."},
        {"connection": "Evaluación de tecnologías sanitarias", "explanation": "Introduce la frontera entre atractivo comercial y evaluación multidisciplinaria de valor, que requiere métodos propios."},
        {"connection": "Implementación en sistemas sanitarios", "explanation": "Hace visibles infraestructura, integración, mantenimiento, formación y barreras organizacionales que pueden condicionar adopción."}
    ]
    unit["sources"] = [
        {"title": "Market Segmentation and Consumer Markets", "authors": "Gomez Albrecht, Green y Hoffman / OpenStax", "year": 2023, "url": "https://openstax.org/books/principles-marketing/pages/5-1-market-segmentation-and-consumer-markets", "type": "libro universitario abierto", "verification_status": "verified_directly"},
        {"title": "Segmentation of B2B Markets", "authors": "Gomez Albrecht, Green y Hoffman / OpenStax", "year": 2023, "url": "https://openstax.org/books/principles-marketing/pages/5-2-segmentation-of-b2b-markets", "type": "libro universitario abierto", "verification_status": "verified_directly"},
        {"title": "Buyers and Buying Situations in a B2B Market", "authors": "Gomez Albrecht, Green y Hoffman / OpenStax", "year": 2023, "url": "https://openstax.org/books/principles-marketing/pages/4-2-buyers-and-buying-situations-in-a-b2b-market", "type": "libro universitario abierto", "verification_status": "verified_directly"},
        {"title": "Selecting Target Markets", "authors": "Gomez Albrecht, Green y Hoffman / OpenStax", "year": 2023, "url": "https://openstax.org/books/principles-marketing/pages/5-5-selecting-target-markets", "type": "libro universitario abierto", "verification_status": "verified_directly"},
        {"title": "Product Positioning", "authors": "Gomez Albrecht, Green y Hoffman / OpenStax", "year": 2023, "url": "https://openstax.org/books/principles-marketing/pages/5-6-product-positioning", "type": "libro universitario abierto", "verification_status": "verified_directly"},
        {"title": "Determining Consumer Needs and Wants — Value Proposition", "authors": "Gomez Albrecht, Green y Hoffman / OpenStax", "year": 2023, "url": "https://openstax.org/books/principles-marketing/pages/1-5-determining-consumer-needs-and-wants", "type": "libro universitario abierto", "verification_status": "verified_directly"},
        {"title": "The Five Competitive Forces That Shape Strategy", "authors": "Michael E. Porter", "year": 2008, "url": "https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy", "type": "artículo de estrategia", "verification_status": "verified_directly"},
        {"title": "Health technology assessment of medical devices, 2nd ed", "authors": "World Health Organization", "year": 2025, "url": "https://www.who.int/publications/i/item/9789240110878", "type": "publicación institucional", "verification_status": "verified_directly"}
    ]
    unit["editorial_notice"] = (
        "Unidad académica en revisión. La curación interna y sus comprobaciones automáticas no constituyen revisión disciplinar externa, "
        "validación clínica, asesoría comercial, recomendación de inversión, aprobación regulatoria, HTA ni decisión de compra. Los casos, "
        "segmentos, competidores, precios y tasas de adopción son sintéticos y no deben sustituir investigación de mercado, evidencia clínica, "
        "gobernanza institucional ni requisitos regulatorios aplicables."
    )
    unit["status"] = "review"

    serialized = json.dumps(unit, ensure_ascii=False).casefold()
    assert GENERIC.casefold() not in serialized
    assert "píxeles" not in serialized and "vóxeles" not in serialized
    assert len(unit["glossary"]) >= 20
    assert len(unit["worked_examples"]) >= 5
    assert len(unit["common_errors"]) >= 12
    assert len(unit["self_assessment"]) >= 12
    assert all(s.get("verification_status") == "verified_directly" for s in unit["sources"])
    dump(unit)
    print("[ok] Economía y Gestión de Empresas U4 curada y espejo sincronizado")


if __name__ == "__main__":
    main()
