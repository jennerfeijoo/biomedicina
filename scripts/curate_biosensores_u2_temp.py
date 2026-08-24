from __future__ import annotations

import json
from pathlib import Path

SOURCE = Path("data/course_redevelopment/biosensores/units/unit-02.json")
MIRROR = Path("data/generated_units/biosensores/unit-02.json")
GENERIC = "Concepto de la unidad que debe definirse mediante entidades observables"

unit = {
  "schema_version": "2.0",
  "subject_id": "biosensores",
  "area_id": "ingenieria-biomedica",
  "unit": 2,
  "slug": "reconocimiento-biologico",
  "title": "Reconocimiento biológico",
  "status": "review",
  "purpose": "Seleccionar y evaluar elementos de reconocimiento biológico para biosensores —enzimas, anticuerpos, sondas de ácidos nucleicos y aptámeros— relacionando mecanismo, afinidad o actividad, cinética, selectividad, estabilidad, matriz y regeneración con controles discriminantes, sin confundir afinidad con especificidad, K_m con K_D ni reconocimiento molecular con desempeño analítico o clínico del dispositivo completo.",
  "learning_objectives": [
    "Distinguir reconocimiento catalítico, reconocimiento de afinidad e hibridación y asociar cada mecanismo con observables, supuestos y controles apropiados.",
    "Interpretar una unión reversible 1:1 mediante K_D, k_on, k_off y ocupación fraccional, explicando cuándo el equilibrio y el modelo dejan de ser defendibles.",
    "Aplicar el modelo de Michaelis–Menten a un reconocimiento enzimático simple y explicar por qué K_m no debe interpretarse automáticamente como constante de afinidad.",
    "Comparar anticuerpos, sondas de ácidos nucleicos y aptámeros por afinidad, selectividad, estabilidad, reactividad cruzada, condiciones de plegamiento o hibridación y posibilidad de regeneración.",
    "Diseñar controles negativos, no-diana, mutantes o scrambled, inactivos y de matriz que discriminen reconocimiento específico de unión o actividad inespecífica.",
    "Construir una decisión reproducible de selección de bioreceptor para un caso sintético, separando propiedad molecular, desempeño del biosensor, evidencia clínica y requisitos regulatorios."
  ],
  "theory_sections": [
    {
      "heading": "1. Cuatro familias de reconocimiento y una misma pregunta de diseño",
      "paragraphs": [
        "El elemento de reconocimiento convierte la presencia, cantidad o actividad de una diana en un evento molecular suficientemente selectivo para que el resto del biosensor pueda observarlo. No existe un bioreceptor universalmente superior. La elección depende de qué es la diana, qué matriz la contiene, qué intervalo y tiempo de respuesta se esperan, qué condiciones químicas pueden mantenerse y si el sistema debe regenerarse. La revisión de Morales y Halpern resume precisamente esta decisión como un compromiso entre mecanismo de unión, selectividad, reproducibilidad, sensibilidad del sistema y reusabilidad. U2 estudia esas propiedades del reconocimiento; la física del transductor se reserva para U3.",
        "Las enzimas reconocen sustratos dentro de un mecanismo catalítico. El evento útil no es solamente la unión: el complejo enzima–sustrato progresa hacia producto y la velocidad de reacción puede proporcionar la variable vinculada al analito. Esta amplificación química intrínseca puede ser ventajosa, pero introduce dependencia de actividad enzimática, temperatura, pH, cofactores, inhibidores y estabilidad. Una enzima que conserva estructura pero pierde actividad no es un receptor funcional equivalente. Por ello sus controles deben incluir actividad y alternativas catalíticas, no únicamente evidencia de unión.",
        "Los anticuerpos reconocen epítopos mediante regiones de unión cuya afinidad y selectividad dependen de la interacción molecular y de la conformación del antígeno. En un biosensor de afinidad, la unión puede detectarse directamente o mediante un formato adicional, pero U2 no confunde señal con afinidad. Reactividad cruzada, orientación, agregación, estabilidad y multivalencia pueden alterar la respuesta aparente. Una K_D baja para el objetivo no demuestra que especies parecidas no se unan ni garantiza que la molécula siga funcional después de almacenamiento o integración superficial.",
        "Las sondas de ácidos nucleicos explotan complementariedad y condiciones de hibridación para reconocer secuencias, mientras los aptámeros son oligonucleótidos seleccionados para plegarse en estructuras capaces de unirse a dianas. Los trabajos fundacionales de Tuerk y Gold y de Ellington y Szostak establecieron selección in vitro de ligandos de RNA; variantes posteriores extendieron el concepto a DNA. En ambos casos, secuencia, estructura, fuerza iónica, temperatura y composición de la matriz pueden cambiar el reconocimiento. Una secuencia escrita en un archivo no garantiza la conformación o la selectividad observadas en el entorno del sensor."
      ],
      "key_points": [
        "Enzimas combinan reconocimiento con catálisis; anticuerpos y aptámeros son principalmente receptores de afinidad; sondas nucleicas reconocen mediante hibridación.",
        "No existe un bioreceptor universalmente mejor: la elección depende de diana, matriz, condiciones y uso previsto.",
        "Afinidad, selectividad, estabilidad y regeneración son dimensiones distintas y pueden entrar en conflicto.",
        "U2 estudia el reconocimiento; la elección y modelado físico del transductor pertenecen a U3."
      ]
    },
    {
      "heading": "2. Afinidad y cinética: qué significan K_D, k_on y k_off",
      "paragraphs": [
        "Para una interacción reversible idealizada R + L ⇌ RL, la constante de disociación en equilibrio puede escribirse K_D = [R][L]/[RL]. IUPAC la define para una interacción reversible de unión y señala que, bajo el modelo cinético simple, K_D = k_off/k_on. Una K_D menor corresponde a mayor ocupación a una concentración libre dada dentro de ese modelo. Sin embargo, el número solo es interpretable si la especie, estado, temperatura, composición del tampón, tiempo de equilibrio y modelo de unión están suficientemente definidos.",
        "La ocupación fraccional ideal θ = [L]/(K_D + [L]) ayuda a visualizar el significado de K_D: cuando [L] = K_D, la mitad de los sitios está ocupada en un sistema 1:1 simple. Esta ecuación no convierte cualquier curva de biosensor en una isoterma de Langmuir. Superficies heterogéneas, multivalencia, transporte de masa, cooperatividad, rebinding, inmovilización o agotamiento de ligando pueden producir respuestas que no representan directamente la fracción de receptores ocupados. El modelo sirve para enseñar y contrastar hipótesis, no para forzar todos los datos a una forma conveniente.",
        "La cinética aporta información que K_D por sí sola oculta. Dos receptores pueden compartir K_D y tener combinaciones muy diferentes de k_on y k_off: uno puede asociarse y disociarse rápidamente; otro, hacerlo lentamente. Esto modifica el tiempo necesario para aproximarse al equilibrio y la posibilidad de regenerar el sensor. Una unión muy estable puede favorecer retención, pero también dificultar ciclos rápidos de uso. Jarmoskaite y colaboradores muestran que medir afinidad de forma fiable requiere controlar regímenes de concentración, tiempo de incubación y evidencia de equilibrio en lugar de asumir que una señal estable equivale automáticamente a una K_D válida.",
        "Afinidad tampoco es sinónimo de especificidad. K_D describe una interacción concreta; la selectividad requiere comparar la respuesta frente a especies alternativas relevantes en condiciones definidas. Si un anticuerpo tiene K_D = 1 nM para P y 2 nM para una proteína homóloga Q, su afinidad por P es alta pero la discriminación entre P y Q puede ser insuficiente. El mismo razonamiento vale para aptámeros y sondas. La evaluación debe incluir no-dianas plausibles, concentraciones comparables y la matriz de interés, no una única molécula irrelevante elegida como control fácil."
      ],
      "equations": [
        {
          "latex": "K_D=\\frac{[R][L]}{[RL]}=\\frac{k_{off}}{k_{on}}",
          "meaning": "Constante de disociación para un modelo de unión reversible 1:1; su interpretación exige condiciones y modelo explícitos.",
          "variables": {"R": "receptor libre", "L": "ligando libre", "RL": "complejo", "k_on": "constante de asociación", "k_off": "constante de disociación"}
        },
        {
          "latex": "\\theta=\\frac{[L]}{K_D+[L]}",
          "meaning": "Ocupación fraccional ideal para una interacción 1:1 en equilibrio; no es una ley universal de respuesta del biosensor.",
          "variables": {"theta": "fracción de sitios ocupados", "[L]": "concentración de ligando libre", "K_D": "constante de disociación"}
        }
      ],
      "key_points": [
        "K_D describe afinidad dentro de un modelo y condiciones definidos; no mide por sí sola selectividad.",
        "k_on y k_off distinguen interacciones con la misma afinidad de equilibrio pero tiempos de respuesta diferentes.",
        "Una señal superficial no debe identificarse automáticamente con ocupación 1:1.",
        "Los controles de no-diana deben representar alternativas plausibles y concentraciones informativas."
      ]
    },
    {
      "heading": "3. Catálisis, hibridación y plegamiento: modelos que no deben confundirse",
      "paragraphs": [
        "En reconocimiento enzimático, una relación frecuente entre velocidad inicial y concentración de sustrato es la ecuación de Michaelis–Menten v_0 = V[S]/(K_m + [S]). IUPAC recalca que K_m tiene dimensión de concentración y no es, en general, una constante de equilibrio. Incluso cuando una reacción sigue cinética de Michaelis–Menten, ello no prueba un mecanismo único. Para un biosensor, el parámetro útil depende de actividad enzimática, cantidad de enzima, temperatura, pH y otros componentes. Por eso no debe compararse numéricamente un K_m con una K_D de anticuerpo como si midieran la misma propiedad.",
        "Las sondas de DNA o RNA destinadas a reconocer una secuencia dependen de complementariedad, longitud, composición, temperatura, fuerza iónica y accesibilidad del objetivo. Un mismatch puede desestabilizar la hibridación, pero su efecto depende de posición y condiciones; no existe una penalización universal por cada base incorrecta. Los biosensores de ácidos nucleicos aprovechan estas diferencias para discriminación, pero deben evaluar controles de secuencia no complementaria y mismatches relevantes bajo el mismo protocolo. El principio de transducción que convierte la hibridación en señal se desarrolla en U3.",
        "Los aptámeros combinan secuencia y estructura tridimensional. SELEX enriquece secuencias que cumplen un criterio de unión dentro de un proceso de selección, pero el resultado puede depender de cómo se presentaron diana y competidores y de la composición del medio. La afinidad medida después de seleccionar un aptámero debe verificarse en condiciones cercanas al uso. Cationes, pH, temperatura, nucleasas y componentes de la matriz pueden alterar plegamiento y accesibilidad. Un aptámero con K_D excelente en buffer de selección puede rendir peor en una muestra distinta sin que la literatura original sea incorrecta.",
        "En anticuerpos también existe una distinción entre afinidad molecular y respuesta aparente multivalente. Una inmunoglobulina completa puede establecer más de una interacción y producir avididad; fragmentos monovalentes simplifican algunos análisis pero cambian tamaño, estabilidad y opciones de orientación. Además, optimizar afinidad puede introducir compromisos con estabilidad o solubilidad. La selección para biosensor debe documentar qué formato se usó y qué propiedad se midió, en vez de trasladar automáticamente una cifra obtenida con otra construcción molecular."
      ],
      "equations": [
        {
          "latex": "v_0=\\frac{V\\,[S]}{K_m+[S]}",
          "meaning": "Ecuación de Michaelis–Menten para velocidad inicial en condiciones compatibles; K_m no es en general una constante de afinidad.",
          "variables": {"v_0": "velocidad inicial", "V": "velocidad límite del modelo", "[S]": "concentración de sustrato", "K_m": "constante de Michaelis"}
        }
      ],
      "key_points": [
        "K_m y K_D responden preguntas distintas y no deben compararse como métricas universales de afinidad.",
        "La discriminación por hibridación depende de secuencia y condiciones, no solo del número de mismatches.",
        "La función de un aptámero depende de plegamiento y del entorno químico en el que se evalúa.",
        "Formato, multivalencia y estabilidad pueden cambiar la respuesta de un anticuerpo aunque el epítopo sea el mismo."
      ]
    },
    {
      "heading": "4. Controles, estabilidad y selección responsable del bioreceptor",
      "paragraphs": [
        "Los controles deben corresponder al mecanismo. Para una enzima, una versión inactiva o una condición sin cofactor puede separar catálisis de una señal no catalítica; un sustrato análogo desafía selectividad. Para un anticuerpo o aptámero, una no-diana estructuralmente relacionada y una concentración competitiva pueden revelar reactividad cruzada. Para una sonda nucleica, una secuencia no complementaria y uno o varios mismatches informativos ayudan a evaluar discriminación. Un control scrambled puede ser útil para aptámeros, pero solo si conserva propiedades relevantes y su interpretación no se reduce a que cualquier secuencia aleatoria sea equivalente.",
        "La estabilidad debe evaluarse en el estado y condiciones en que se utilizará el receptor. Anticuerpos pueden perder actividad por desnaturalización, agregación o cambios de formulación; enzimas pueden perder actividad catalítica; RNA puede degradarse por nucleasas; aptámeros de DNA suelen ser químicamente más resistentes, aunque su plegamiento sigue dependiendo del entorno. La revisión sobre estabilidad de anticuerpos destaca que estabilidad influye directamente en desempeño. Por tanto, retener concentración total de proteína no basta: se necesita una medida funcional antes y después del estrés pertinente.",
        "La matriz puede afectar al receptor antes de que intervenga el transductor. Proteínas y lípidos pueden competir o adsorberse; sales y pH pueden cambiar afinidad o plegamiento; nucleasas pueden degradar sondas; inhibidores pueden modificar actividad enzimática. La evaluación de selectividad en buffer simple y la evaluación en matriz responden preguntas diferentes. U4 abordará inmovilización, superficies y microfluídica con mayor detalle, pero U2 debe registrar ya qué propiedad del bioreceptor podría cambiar cuando se integra en una interfaz.",
        "La decisión final se documenta como una matriz de requisitos, evidencia y riesgos. Para cada candidato se registran mecanismo, diana, condiciones de afinidad o actividad, cinética cuando esté disponible, no-dianas ensayadas, estabilidad funcional, regeneración, compatibilidad de matriz, evidencia pendiente y razón de selección. La conclusión no afirma que el biosensor completo tenga determinada sensibilidad, límite de detección o desempeño clínico: esas propiedades dependen también de transducción, superficie, procesamiento y validación. Una buena U2 termina con un bioreceptor justificable y una lista explícita de pruebas que todavía faltan."
      ],
      "key_points": [
        "Cada mecanismo necesita controles que desafíen una alternativa plausible al reconocimiento específico.",
        "La estabilidad relevante es funcional, no solo presencia física de la molécula.",
        "La matriz puede modificar reconocimiento antes de la transducción y debe formar parte de la evidencia.",
        "Seleccionar un bioreceptor no equivale a validar el desempeño analítico o clínico del biosensor completo."
      ]
    }
  ],
  "glossary": [
    {"term": "Bioreceptor", "definition": "Elemento biológico o biomolecular que aporta reconocimiento de una diana mediante unión, hibridación, catálisis u otro mecanismo definido."},
    {"term": "Afinidad", "definition": "Fuerza de una interacción de unión bajo un modelo y condiciones determinados; puede resumirse mediante una constante como K_D cuando el modelo es apropiado."},
    {"term": "Selectividad", "definition": "Capacidad de discriminar la diana frente a especies o condiciones alternativas relevantes para el uso previsto."},
    {"term": "Reactividad cruzada", "definition": "Respuesta del elemento de reconocimiento frente a una especie distinta de la diana que comparte o presenta determinantes reconocibles."},
    {"term": "K_D", "definition": "Constante de disociación en equilibrio para una interacción reversible; en el modelo 1:1 simple es [R][L]/[RL] y k_off/k_on."},
    {"term": "k_on", "definition": "Constante de velocidad de asociación de una interacción de unión dentro de un modelo cinético especificado."},
    {"term": "k_off", "definition": "Constante de velocidad de disociación de un complejo dentro de un modelo cinético especificado."},
    {"term": "Ocupación fraccional", "definition": "Fracción idealizada de sitios de unión ocupados; su relación con señal instrumental depende de la arquitectura."},
    {"term": "K_m", "definition": "Constante de Michaelis en una ecuación de Michaelis–Menten; es una concentración característica y no es en general una constante de afinidad."},
    {"term": "V", "definition": "Velocidad límite del modelo de Michaelis–Menten a saturación de sustrato bajo condiciones definidas."},
    {"term": "Epítopo", "definition": "Determinante molecular del antígeno reconocido por un sitio de unión de anticuerpo."},
    {"term": "Avididad", "definition": "Efecto combinado de múltiples interacciones de unión en un sistema multivalente; no es equivalente a afinidad monovalente."},
    {"term": "Hibridación", "definition": "Asociación de cadenas de ácidos nucleicos mediante apareamiento de bases bajo condiciones que determinan estabilidad y especificidad."},
    {"term": "Mismatch", "definition": "Emparejamiento no complementario en una región de hibridación cuya consecuencia depende de secuencia, posición y condiciones."},
    {"term": "Aptámero", "definition": "Oligonucleótido seleccionado para adoptar estructuras capaces de reconocer una diana mediante interacción molecular."},
    {"term": "SELEX", "definition": "Proceso iterativo de selección y amplificación de secuencias de ácidos nucleicos enriquecidas por una propiedad de unión o función definida."},
    {"term": "Estabilidad funcional", "definition": "Conservación de la actividad de reconocimiento o catálisis relevante después de almacenamiento, estrés o exposición a condiciones de uso."},
    {"term": "Regeneración", "definition": "Restauración de un elemento de reconocimiento o interfaz a un estado utilizable para un nuevo ciclo sin pérdida inadmisible de función."}
  ],
  "worked_examples": [
    {
      "title": "Dos anticuerpos con afinidad similar pero cinética distinta",
      "scenario": "El candidato A tiene k_on=2×10^5 M^-1 s^-1 y k_off=2×10^-4 s^-1; B tiene k_on=2×10^4 M^-1 s^-1 y k_off=2×10^-5 s^-1.",
      "reasoning_steps": [
        "Calcular K_D=A: (2×10^-4)/(2×10^5)=1×10^-9 M = 1 nM.",
        "Calcular K_D=B: (2×10^-5)/(2×10^4)=1×10^-9 M = 1 nM.",
        "Reconocer que ambos comparten afinidad de equilibrio bajo el modelo, pero B asocia y disocia diez veces más lentamente.",
        "Relacionar la cinética con tiempo de incubación y regeneración: una K_D idéntica no implica operación temporal idéntica.",
        "Solicitar datos de reactividad cruzada y estabilidad antes de declarar un candidato superior."
      ],
      "interpretation": "K_D no resume por sí sola el comportamiento temporal. La selección debe integrar cinética, selectividad y requisitos operativos.",
      "limitations": ["Los valores son sintéticos y suponen un modelo 1:1.", "No se modela transporte de masa ni multivalencia.", "No se infiere desempeño del biosensor completo."]
    },
    {
      "title": "K_m no es K_D: interpretar un receptor enzimático",
      "scenario": "Una enzima sintética sigue v0=V[S]/(K_m+[S]) con V=120 unidades/min y K_m=3 mM.",
      "reasoning_steps": [
        "Para [S]=3 mM, calcular v0=120×3/(3+3)=60 unidades/min.",
        "Para [S]=12 mM, calcular v0=120×12/(3+12)=96 unidades/min.",
        "Reconocer el comportamiento saturable y que K_m corresponde a la concentración que produce V/2 en este modelo.",
        "Evitar interpretar 3 mM como K_D o como prueba directa de afinidad enzima–sustrato.",
        "Proponer un análogo de sustrato y una enzima inactiva como controles para separar selectividad catalítica de señal inespecífica."
      ],
      "interpretation": "Michaelis–Menten describe una relación cinética; K_m no debe usarse como ranking universal de afinidad frente a anticuerpos o aptámeros.",
      "limitations": ["El modelo asume condiciones compatibles con velocidad inicial.", "No se incluyen inhibición ni múltiples sustratos.", "La transducción del producto queda fuera del ejemplo."]
    },
    {
      "title": "Una sonda de DNA cambia de discriminación con la condición de hibridación",
      "scenario": "Bajo condición A, señales normalizadas son objetivo=1.00, un mismatch=0.32 y no complementaria=0.06; bajo condición B son 1.00, 0.70 y 0.10.",
      "reasoning_steps": [
        "Mantener el objetivo normalizado para comparar la discriminación relativa entre condiciones.",
        "Observar que el mismatch produce 32 % de la señal objetivo en A y 70 % en B.",
        "Concluir que A discrimina mejor este mismatch concreto, no que sea universalmente superior.",
        "Proponer repetir con mismatches en otras posiciones y con la matriz prevista.",
        "Separar el fenómeno de hibridación de la forma en que U3 convertiría esa hibridación en señal."
      ],
      "interpretation": "La especificidad de secuencia depende de condiciones y del mismatch ensayado; debe verificarse en el protocolo real.",
      "limitations": ["Las señales son sintéticas.", "No se infiere energía libre ni temperatura de fusión.", "No se compara límite de detección."]
    },
    {
      "title": "Aptámero excelente en buffer, mediocre en matriz",
      "scenario": "Un aptámero presenta K_D aparente de 2 nM en buffer de selección y 20 nM en matriz sintética; un control scrambled permanece débil en ambos medios.",
      "reasoning_steps": [
        "No atribuir el cambio automáticamente a degradación; considerar plegamiento, fuerza iónica, competencia y accesibilidad.",
        "Calcular θ ideal a [L]=10 nM: 10/(2+10)=0.83 en buffer y 10/(20+10)=0.33 en matriz.",
        "Usar la diferencia solo como ilustración del efecto que tendría el K_D aparente bajo el modelo simple.",
        "Confirmar que el control scrambled no resuelve por sí solo todas las alternativas de matriz.",
        "Solicitar estabilidad funcional, no-dianas y cinética en matriz antes de seleccionar el aptámero."
      ],
      "interpretation": "La afinidad medida en condiciones de selección no se transfiere automáticamente al entorno del biosensor.",
      "limitations": ["K_D es sintética y se trata como aparente.", "No se identifica el mecanismo del cambio.", "No se evalúa transducción ni superficie."]
    }
  ],
  "guided_activities": [
    {
      "title": "Actividad guiada: selección reproducible de bioreceptores para tres dianas sintéticas",
      "instructions": [
        "Usa exclusivamente los datos sintéticos proporcionados; no recolectes muestras, no trabajes con participantes y no interpretes resultados como diagnóstico.",
        "Antes de calcular, clasifica cada caso como reconocimiento catalítico, afinidad o hibridación y escribe qué propiedad molecular debe verificarse.",
        "Mantén K_D, K_m, k_on, k_off, actividad y señal como magnitudes distintas con sus unidades.",
        "Para cada candidato predefine al menos un control que desafíe una explicación alternativa antes de decidir.",
        "Conserva cálculos, supuestos, tabla de decisión y razones de descarte para que otra persona pueda reconstruir la selección.",
        "No elijas el transductor ni calcules límite de detección: esos pasos corresponden a U3 y U5."
      ],
      "problems": [
        "Caso P, proteína: anticuerpo A tiene k_on=2×10^5 M^-1 s^-1 y k_off=2×10^-4 s^-1; aptámero B tiene k_on=5×10^4 M^-1 s^-1 y k_off=1×10^-4 s^-1. Calcula K_D de ambos.",
        "Calcula ocupación ideal de A y B a 5 nM de P y explica por qué la ocupación no es todavía una señal de biosensor.",
        "En matriz sintética, el K_D aparente de B pasa a 20 nM mientras A se mantiene en 1.5 nM. Recalcula ocupación a 5 nM y registra qué evidencia adicional pedirías antes de elegir.",
        "La proteína homóloga Q produce 18 % de unión relativa con A y 6 % con B. Interpreta estos datos como un control de reactividad cruzada limitado a Q, no como especificidad universal.",
        "Caso M, metabolito: enzima E tiene V=100 unidades/min y K_m=2 mM. Calcula v0 a 0.5, 2 y 8 mM y explica por qué K_m no es K_D.",
        "Un análogo M2 produce una velocidad equivalente al 15 % de la obtenida con M a la misma concentración. Diseña un control adicional que permita distinguir actividad catalítica de señal instrumental no relacionada.",
        "Caso N, secuencia: una sonda complementaria produce señales normalizadas objetivo=1.00, mismatch central=0.30 y no complementaria=0.05 bajo condición A; bajo B el mismatch=0.68. Decide qué condición discrimina mejor este mismatch y qué falta probar.",
        "Propón un control scrambled para un aptámero y explica por qué debe interpretarse junto con una no-diana relevante y no como prueba única de especificidad.",
        "Compara estabilidad funcional después de un estrés sintético: A conserva 82 %, B 94 % y E 70 % de su respuesta inicial. Explica por qué la concentración molecular remanente no sería un sustituto suficiente de esta prueba.",
        "Construye una matriz de decisión para P, M y N con mecanismo, propiedad cuantitativa, selectividad, estabilidad, matriz, regeneración y evidencia pendiente.",
        "Señala qué decisiones deben aplazarse a U3, U4 y U5 y por qué.",
        "Redacta una conclusión de máximo 180 palabras que seleccione provisionalmente un bioreceptor por caso y limite la afirmación al reconocimiento molecular estudiado."
      ],
      "deliverables": [
        "Tabla de mecanismos de reconocimiento y magnitudes relevantes.",
        "Cálculos de K_D y ocupación para el caso P.",
        "Cálculos Michaelis–Menten y explicación K_m versus K_D para M.",
        "Comparación de hibridación y controles de mismatch para N.",
        "Matriz de controles por mecanismo y explicación alternativa que desafían.",
        "Matriz de decisión con afinidad o actividad, selectividad, estabilidad, matriz y regeneración.",
        "Mapa de transferencia a U3, U4 y U5.",
        "Conclusión final limitada, reproducible y sin afirmaciones clínicas."
      ],
      "checking_criteria": [
        "K_D se calcula como k_off/k_on con unidades de concentración.",
        "K_m no se describe como constante de afinidad universal.",
        "Ocupación, actividad enzimática y señal instrumental permanecen separadas.",
        "La reactividad frente a una sola no-diana no se generaliza a especificidad universal.",
        "El efecto de matriz sobre el aptámero cambia la decisión o se registra como incertidumbre relevante.",
        "Los controles corresponden al mecanismo: catalítico, afinidad o hibridación.",
        "La estabilidad se evalúa funcionalmente.",
        "No se selecciona transductor ni se calcula límite de detección en U2.",
        "La matriz de decisión conserva condiciones y evidencia pendiente.",
        "La conclusión no afirma desempeño clínico, seguridad ni conformidad regulatoria."
      ]
    }
  ],
  "common_errors": [
    {"error": "Elegir el bioreceptor únicamente por tener la K_D más baja.", "correction": "Integrar cinética, selectividad frente a alternativas, estabilidad, matriz, regeneración y condiciones de medida."},
    {"error": "Usar afinidad y especificidad como sinónimos.", "correction": "Afinidad describe una interacción; selectividad exige comparaciones frente a especies alternativas relevantes."},
    {"error": "Interpretar K_m como K_D de una enzima.", "correction": "K_m pertenece a una relación cinética de Michaelis–Menten y no es en general una constante de equilibrio de unión."},
    {"error": "Suponer que el equilibrio se alcanzó porque la señal parece estable.", "correction": "Verificar tiempos, concentraciones y dependencia temporal compatibles con el modelo de unión."},
    {"error": "Considerar cualquier secuencia scrambled un control perfecto de aptámero.", "correction": "Comprobar que el control desafía una alternativa relevante y complementarlo con no-dianas y condiciones de matriz."},
    {"error": "Generalizar un resultado de hibridación de un mismatch a todas las variantes.", "correction": "Evaluar posición, secuencia y condiciones de hibridación relevantes."},
    {"error": "Medir proteína o ácido nucleico remanente y llamarlo estabilidad funcional.", "correction": "Evaluar conservación de actividad de reconocimiento o catálisis después del estrés pertinente."},
    {"error": "Confundir avididad multivalente con afinidad monovalente.", "correction": "Declarar formato molecular y modelo de interacción antes de comparar constantes."},
    {"error": "Trasladar una K_D obtenida en buffer directamente a una biomatriz.", "correction": "Revalidar afinidad, selectividad y estabilidad en condiciones representativas o declarar la transferencia como pendiente."},
    {"error": "Concluir que un buen bioreceptor implica un buen biosensor clínico.", "correction": "Separar reconocimiento molecular de transducción, superficie, desempeño analítico, evidencia clínica y regulación."
  ],
  "self_assessment": [
    {"question": "¿Qué relación existe entre K_D, k_on y k_off en el modelo reversible 1:1?", "answer": "K_D=k_off/k_on.", "reasoning": "La relación vincula equilibrio y cinética dentro del modelo simple.", "common_error": "Invertir la razón o ignorar las unidades."},
    {"question": "¿Qué significa θ cuando [L]=K_D en el modelo 1:1?", "answer": "θ=0.5, es decir, la mitad de los sitios está ocupada idealmente.", "reasoning": "Sustituir [L]=K_D da K_D/(K_D+K_D).", "common_error": "Interpretar θ como señal normalizada sin justificar el acoplamiento del sensor."},
    {"question": "¿Una K_D baja demuestra alta especificidad?", "answer": "No; demuestra afinidad alta para la interacción medida, mientras la selectividad requiere comparar no-dianas relevantes.", "reasoning": "Una molécula puede unirse fuertemente a más de una especie.", "common_error": "Usar una sola curva objetivo como prueba de especificidad."},
    {"question": "¿Por qué K_m no es generalmente K_D?", "answer": "Porque K_m es un parámetro de una relación cinética y depende del mecanismo; IUPAC señala que no es en general una constante de equilibrio.", "reasoning": "Catálisis y unión reversible pura no describen el mismo proceso.", "common_error": "Comparar K_m de una enzima con K_D de un anticuerpo como si fueran equivalentes."},
    {"question": "¿Qué diferencia aporta k_off al diseño aunque K_D sea igual?", "answer": "La velocidad de disociación afecta tiempo de retención y regeneración; dos receptores con la misma K_D pueden tener cinéticas muy distintas.", "reasoning": "K_D resume una razón, no los valores individuales de las constantes de velocidad.", "common_error": "Elegir por K_D sin considerar tiempo de respuesta."},
    {"question": "¿Qué control es especialmente informativo para una enzima?", "answer": "Una versión o condición catalíticamente inactiva, junto con un análogo de sustrato relevante.", "reasoning": "Permite separar catálisis específica de señal que no requiere actividad enzimática.", "common_error": "Usar solo un blanco sin enzima."},
    {"question": "¿Por qué un mismatch no tiene un efecto universal sobre hibridación?", "answer": "Porque depende de secuencia, posición, longitud, temperatura, fuerza iónica y otras condiciones.", "reasoning": "La estabilidad del dúplex es contextual.", "common_error": "Asignar la misma penalización a cualquier mismatch."},
    {"question": "¿Qué puede cambiar la afinidad aparente de un aptámero en una matriz distinta?", "answer": "Plegamiento, iones, pH, competencia, degradación o accesibilidad, entre otros factores.", "reasoning": "El reconocimiento de aptámeros depende de estructura y entorno.", "common_error": "Suponer que la secuencia garantiza la misma K_D en cualquier medio."},
    {"question": "¿Qué diferencia existe entre estabilidad física y funcional?", "answer": "La molécula puede seguir presente pero haber perdido capacidad de unión o catálisis; estabilidad funcional evalúa la actividad relevante.", "reasoning": "El biosensor necesita función, no solo masa molecular detectable.", "common_error": "Usar concentración remanente como único indicador de estabilidad."},
    {"question": "¿Qué deja pendiente U2 después de seleccionar un bioreceptor?", "answer": "Transducción detallada, inmovilización/superficie, caracterización analítica y evaluación clínica o regulatoria.", "reasoning": "El desempeño del biosensor emerge de más capas que el reconocimiento.", "common_error": "Presentar la selección molecular como validación del dispositivo."}
  ],
  "biomedical_connections": [
    {"topic": "Biosensores enzimáticos", "connection": "El reconocimiento catalítico es útil para metabolitos y otras dianas que participan en reacciones medibles, pero su desempeño depende de actividad, interferentes y condiciones de reacción."},
    {"topic": "Inmunosensores", "connection": "Anticuerpos y fragmentos permiten reconocer epítopos proteicos; afinidad, reactividad cruzada, formato y estabilidad condicionan el diseño antes de la transducción."},
    {"topic": "Diagnóstico molecular", "connection": "Sondas de ácidos nucleicos pueden discriminar secuencias mediante hibridación, pero la capacidad de distinguir variantes debe demostrarse bajo condiciones relevantes."},
    {"topic": "Aptasensores", "connection": "Aptámeros permiten reconocimiento de diversas dianas mediante estructuras seleccionadas in vitro; su función debe revalidarse en el medio y formato de uso."},
    {"topic": "Medicina de precisión", "connection": "La selección del receptor puede habilitar medición de biomarcadores específicos, pero utilidad clínica exige validación posterior y no se deriva de afinidad molecular aislada."
  ],
  "sources": [
    {"title": "Guide to Selecting a Biorecognition Element for Biosensors", "authors": "Morales MA, Halpern JM", "year": 2018, "journal": "Bioconjugate Chemistry", "url": "https://pubmed.ncbi.nlm.nih.gov/30216055/", "doi": "10.1021/acs.bioconjchem.8b00592", "type": "revisión metodológica", "description": "Compara características y mecanismos de elementos de bioreconocimiento y su relación con desempeño de biosensores.", "verification_status": "verified_directly"},
    {"title": "equilibrium dissociation constant", "organization": "IUPAC Gold Book", "year": 2025, "url": "https://goldbook.iupac.org/terms/view/14132", "doi": "10.1351/goldbook.14132", "type": "terminología oficial", "description": "Define K_D para unión reversible y su relación con k_off/k_on.", "verification_status": "verified_directly"},
    {"title": "Michaelis–Menten equation", "organization": "IUPAC Gold Book", "year": 2025, "url": "https://goldbook.iupac.org/terms/view/11546", "doi": "10.1351/goldbook.11546", "type": "terminología oficial", "description": "Define la ecuación de Michaelis–Menten y aclara que K_m no es en general una constante de equilibrio.", "verification_status": "verified_directly"},
    {"title": "How to measure and evaluate binding affinities", "authors": "Jarmoskaite I, AlSadhan I, Vaidyanathan PP, Herschlag D", "year": 2020, "journal": "eLife", "url": "https://pubmed.ncbi.nlm.nih.gov/32758356/", "doi": "10.7554/eLife.57264", "type": "artículo metodológico", "description": "Marco para medir y reportar afinidades, con énfasis en equilibrio, concentraciones, controles y calidad de la inferencia.", "verification_status": "verified_directly"},
    {"title": "Systematic evolution of ligands by exponential enrichment: RNA ligands to bacteriophage T4 DNA polymerase", "authors": "Tuerk C, Gold L", "year": 1990, "journal": "Science", "url": "https://pubmed.ncbi.nlm.nih.gov/2200121/", "doi": "10.1126/science.2200121", "type": "artículo primario histórico", "description": "Trabajo fundacional de SELEX para selección in vitro de ligandos de RNA.", "verification_status": "verified_directly"},
    {"title": "In vitro selection of RNA molecules that bind specific ligands", "authors": "Ellington AD, Szostak JW", "year": 1990, "journal": "Nature", "url": "https://pubmed.ncbi.nlm.nih.gov/1697402/", "doi": "10.1038/346818a0", "type": "artículo primario histórico", "description": "Trabajo fundacional de selección in vitro de RNA con unión específica a ligandos.", "verification_status": "verified_directly"},
    {"title": "DNA-Based Biosensors for the Biochemical Analysis: A Review", "year": 2022, "journal": "Biosensors", "url": "https://pubmed.ncbi.nlm.nih.gov/35323453/", "doi": "10.3390/bios12030183", "type": "revisión abierta", "description": "Revisa biosensores basados en DNA, hibridación, DNA funcional y retos de implementación.", "verification_status": "verified_directly"},
    {"title": "Antibody stability: A key to performance - Analysis, influences and improvement", "authors": "Ma H, Ó'Fágáin C, O'Kennedy R", "year": 2020, "journal": "Biochimie", "url": "https://pubmed.ncbi.nlm.nih.gov/32891698/", "doi": "10.1016/j.biochi.2020.08.019", "type": "revisión", "description": "Analiza cómo la estabilidad de anticuerpos influye en afinidad, especificidad y desempeño funcional.", "verification_status": "verified_directly"},
    {"title": "Aptamers, antibody scFv, and antibody Fab' fragments: An overview and comparison of three of the most versatile biosensor biorecognition elements", "year": 2016, "journal": "Biosensors and Bioelectronics", "url": "https://pubmed.ncbi.nlm.nih.gov/27155114/", "type": "revisión comparativa", "description": "Compara aptámeros y fragmentos de anticuerpo en afinidad, estabilidad, desarrollo e inmovilización.", "verification_status": "verified_directly"},
    {"title": "Enhancing Selectivity in Affinity Biosensors through Biorecognition-Driven Suppression of Nonspecific Binding", "year": 2026, "journal": "ACS Sensors", "url": "https://pubmed.ncbi.nlm.nih.gov/41591850/", "doi": "10.1021/acssensors.5c03955", "type": "revisión reciente", "description": "Revisa selectividad y unión inespecífica en biosensores de afinidad, especialmente bajo matrices complejas.", "verification_status": "verified_directly"}
  ],
  "editorial_notice": "Material educativo con curación académica interna y estado review. No constituye revisión disciplinar externa, validación analítica o clínica, recomendación diagnóstica o terapéutica, certificación de bioreceptor o conformidad regulatoria. Las actividades usan datos y escenarios sintéticos y no autorizan trabajo con muestras humanas ni participantes."
}

text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
assert GENERIC.casefold() not in text.casefold()
assert len(unit["theory_sections"]) == 4
assert len(unit["glossary"]) >= 16
assert len(unit["worked_examples"]) >= 4
assert len(unit["guided_activities"][0]["problems"]) >= 10
assert len(unit["common_errors"]) >= 8
assert len(unit["self_assessment"]) >= 10
assert len(unit["sources"]) >= 8
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
