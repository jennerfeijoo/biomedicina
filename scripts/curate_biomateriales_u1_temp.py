#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales" / "unit-01.json"
GENERIC = "Concepto de la unidad que debe definirse mediante entidades observables"

unit = json.loads(SOURCE.read_text(encoding="utf-8"))
unit.update({
    "purpose": "Comparar metales, cerámicas, polímeros y compuestos como familias de diseño para una función biomédica definida, traduciendo el uso previsto en requisitos de propiedades y realizando una selección reproducible con análisis de sensibilidad, sin tratar la clase de material ni la palabra biocompatible como garantía de seguridad, desempeño clínico o conformidad regulatoria de un dispositivo.",
    "learning_objectives": [
        "Definir biomaterial, uso previsto y familia de materiales distinguiendo composición, estructura, procesamiento, propiedades y desempeño del dispositivo.",
        "Comparar metales, cerámicas, polímeros y compuestos mediante mecanismos estructurales y propiedades relevantes, evitando reglas absolutas sobre qué familia es mejor.",
        "Calcular esfuerzo, deformación, módulo elástico y módulo específico en casos sintéticos y distinguir rigidez, resistencia, ductilidad, tenacidad, fatiga y desgaste.",
        "Relacionar propiedades mecánicas, físicas, químicas y superficiales con requisitos de carga, geometría, ambiente, duración y procesamiento.",
        "Construir una matriz requisito-propiedad, aplicar filtros y una ponderación explícita, y evaluar si la selección cambia al perturbar pesos o datos inciertos.",
        "Explicar por qué la biocompatibilidad y la seguridad biológica se evalúan para un dispositivo y uso definidos, y delimitar qué evidencia adicional falta después del cribado de materiales."
    ],
    "theory_sections": [
        {
            "heading": "1. Biomaterial, uso previsto y familias de materiales",
            "paragraphs": [
                "Un biomaterial no se define únicamente por su composición química ni por pertenecer a una lista de materiales usados en medicina. En ingeniería biomédica interesa la materia, superficie o constructo que interactúa con un sistema biológico para cumplir una función definida. La misma sustancia puede resultar adecuada en una geometría y duración de contacto y ser inadecuada en otra. Por eso, antes de comparar candidatos se declara el uso previsto, el tipo de componente, las cargas, el ambiente, la duración, la vía de contacto y qué resultado técnico se pretende conseguir. Esta formulación evita convertir la etiqueta «biomaterial» en una garantía de desempeño o seguridad.",
                "Los metales y aleaciones presentan enlace metálico y una microestructura que puede modificarse mediante composición, solidificación, deformación y tratamientos térmicos. En muchas aplicaciones estructurales se aprovechan su resistencia, tenacidad, capacidad de deformación plástica y, en determinadas aleaciones, la formación de capas pasivas que limitan la corrosión. Sin embargo, «metal» no implica una propiedad única: el módulo, la resistencia a fatiga, la susceptibilidad a corrosión, la densidad y la respuesta de la superficie dependen de la aleación, el estado metalúrgico, la fabricación y el ambiente. La selección debe hacerse con propiedades del material concreto y no con promedios de una familia.",
                "Las cerámicas biomédicas comprenden materiales inorgánicos no metálicos con enlaces predominantemente iónicos o covalentes. Muchas muestran alta dureza, estabilidad química y resistencia al desgaste, pero su escasa deformación plástica hace que defectos y grietas sean especialmente relevantes bajo tracción o flexión. Alumina y zirconia se han usado como cerámicas estructurales, mientras que fosfatos de calcio y vidrios bioactivos representan otras estrategias con interacciones y degradación diferentes. Por tanto, «cerámica» no significa necesariamente inerte, bioactiva, reabsorbible o frágil en el mismo grado; esas afirmaciones requieren identificar composición, microestructura, porosidad y modo de carga.",
                "Los polímeros están formados por macromoléculas cuya arquitectura, masa molecular, cristalinidad, reticulación y temperatura condicionan un rango muy amplio de comportamientos, desde elastómeros blandos hasta termoplásticos de ingeniería. Pueden ofrecer baja densidad, flexibilidad, procesabilidad y degradación programable, pero también viscoelasticidad, fluencia, absorción de fluidos o cambios de propiedad con el tiempo. Un compuesto combina al menos dos fases distinguibles —por ejemplo, una matriz polimérica y un refuerzo fibroso o una fase cerámica— para obtener un conjunto de propiedades que una fase aislada no proporciona. Su desempeño depende de la orientación, fracción, distribución e interfaz entre fases, de modo que puede ser anisótropo y no debe describirse como un simple promedio."
            ],
            "key_points": [
                "La selección comienza por el uso previsto y los requisitos, no por una familia favorita de materiales.",
                "Las propiedades se atribuyen a una composición, microestructura, procesamiento y condición concretos, no a una etiqueta de familia.",
                "Metales, cerámicas, polímeros y compuestos ofrecen espacios de diseño con compromisos distintos y solapamientos importantes.",
                "La geometría y el procesamiento pertenecen al sistema de diseño y pueden cambiar el desempeño aun cuando la composición nominal no cambie."
            ]
        },
        {
            "heading": "2. Propiedades mecánicas, físicas y químicas: qué se mide y qué se infiere",
            "paragraphs": [
                "Las propiedades mecánicas deben separarse de la respuesta de una pieza. En un ensayo de tracción idealizado, el esfuerzo ingenieril se obtiene dividiendo la fuerza por el área inicial y la deformación ingenieril relaciona el cambio de longitud con la longitud inicial. En el tramo aproximadamente lineal y reversible, la pendiente esfuerzo-deformación define el módulo de Young. Estas magnitudes permiten comparar materiales bajo un protocolo definido, pero una fuerza máxima medida en una pieza también depende de dimensiones, defectos, acabado, velocidad de ensayo y condiciones ambientales. Un diseño reproducible conserva unidades, orientación de la muestra y método de ensayo.",
                "Rigidez, resistencia y tenacidad responden a preguntas diferentes. El módulo elástico describe cuánto esfuerzo se necesita para producir una deformación elástica determinada; el límite elástico marca el inicio convencional de deformación plástica en materiales que presentan ese régimen; la resistencia última es un máximo de esfuerzo bajo el ensayo; y la tenacidad describe la capacidad de absorber energía antes de fracturar. En materiales frágiles resultan especialmente importantes la distribución de defectos y la tenacidad a fractura. Comparar únicamente un número de resistencia puede ocultar un modo de fallo dominante o usar una métrica que ni siquiera es equivalente entre familias.",
                "Muchos dispositivos están sometidos a cargas repetidas, contacto y movimiento, por lo que una medición monotónica no caracteriza toda la vida en servicio. La fatiga describe la nucleación y propagación de daño bajo ciclos y depende de amplitud, tensión media, frecuencia, ambiente, superficie y defectos. El desgaste implica pérdida o modificación de material por interacción mecánica y puede acoplarse con corrosión. Estos fenómenos no se resumen de forma responsable con «más fuerte» o «más duro»: requieren un modo de carga y un criterio de fallo explícitos. La unidad usa indicadores sintéticos para aprender a seleccionar qué propiedad debe medirse, no para predecir la vida de un implante real.",
                "La densidad afecta masa y propiedades específicas; la conductividad térmica y eléctrica puede importar en dispositivos con transferencia de calor o señales; la mojabilidad y la energía superficial influyen en interacciones de interfaz; y corrosión, hidrólisis, oxidación o degradación enzimática pueden modificar composición y propiedades con el tiempo. Esterilización, fabricación aditiva, mecanizado, moldeo, recubrimientos y almacenamiento también pueden cambiar microestructura o superficie. Por ello, una tabla de propiedades tomada de una ficha genérica es un punto de partida: la selección final exige datos del grado, orientación, procesamiento y condición relevantes."
            ],
            "equations": [
                {"latex": "\\sigma=\\frac{F}{A_0}", "meaning": "Esfuerzo ingenieril axial calculado con la fuerza F y el área transversal inicial A0.", "variables": {"F": "fuerza axial", "A_0": "área transversal inicial"}},
                {"latex": "\\varepsilon=\\frac{L-L_0}{L_0}", "meaning": "Deformación ingenieril axial respecto a la longitud inicial.", "variables": {"L": "longitud instantánea", "L_0": "longitud inicial"}},
                {"latex": "E=\\frac{\\Delta\\sigma}{\\Delta\\varepsilon}", "meaning": "Módulo de Young estimado como pendiente en el régimen elástico aproximadamente lineal.", "variables": {"E": "módulo de Young", "\\sigma": "esfuerzo", "\\varepsilon": "deformación"}}
            ],
            "key_points": [
                "Propiedad del material y desempeño de una pieza no son sinónimos: la geometría y el protocolo importan.",
                "Rigidez, resistencia, ductilidad y tenacidad describen aspectos distintos del comportamiento mecánico.",
                "Fatiga, desgaste, corrosión y degradación requieren condiciones temporales y ambientales explícitas.",
                "Los datos de selección deben corresponder al grado, procesamiento, orientación y estado relevantes."
            ]
        },
        {
            "heading": "3. De requisitos a una selección reproducible",
            "paragraphs": [
                "Una selección defendible traduce primero la función en requisitos verificables. Para un componente estructural hipotético pueden existir límites de rigidez, resistencia, masa, deformación admisible, estabilidad química, esterilización y manufacturabilidad. Algunos son restricciones de exclusión y otros son objetivos que compiten. La matriz requisito-propiedad debe indicar para cada requisito la métrica, unidad, dirección deseada, umbral, fuente del dato y nivel de incertidumbre. Si un criterio no puede expresarse todavía de forma medible, se registra como necesidad de evidencia en vez de introducir una puntuación arbitraria.",
                "El filtrado por restricciones precede a la ponderación. Un candidato que no cumple una condición esencial no debería recuperar el primer puesto porque puntúa bien en atributos secundarios. Después del filtrado puede construirse una puntuación multicriterio normalizada para explorar compromisos, siempre que se documenten la normalización y los pesos. La puntuación no es una propiedad física ni una probabilidad de éxito: es un artefacto del criterio de decisión. Dos equipos con pesos diferentes pueden obtener rankings distintos sin que ninguno haya cometido un error matemático, por lo que los pesos deben justificarse a partir del uso previsto.",
                "La comparación entre familias exige reconocer métricas no equivalentes. Un límite elástico útil en un metal dúctil no tiene el mismo significado en una cerámica que fractura antes de un régimen plástico apreciable; un módulo longitudinal de un compuesto unidireccional no describe su módulo transversal; y una propiedad de un polímero puede depender fuertemente de temperatura y tiempo. En vez de forzar todos los candidatos a una única columna, se declara «no aplicable» cuando corresponde y se elige una propiedad funcional comparable —por ejemplo, deformación admisible, resistencia en el modo de carga pertinente o cumplimiento de un umbral de rigidez—.",
                "El análisis de sensibilidad comprueba si la decisión depende de supuestos frágiles. Se repite el ranking con intervalos plausibles de propiedades, pesos alternativos y escenarios de carga. Si el ganador cambia con una variación pequeña, la conclusión correcta no es ocultar la inestabilidad sino identificar qué dato o requisito discriminaría mejor entre candidatos. También es útil reconocer frentes de Pareto: puede no existir un material que minimice densidad, maximice rigidez específica, maximice tenacidad y simplifique procesamiento al mismo tiempo. Una buena selección hace visibles esos compromisos y conserva candidatos alternativos cuando la evidencia no permite resolverlos."
            ],
            "equations": [
                {"latex": "E_s=\\frac{E}{\\rho}", "meaning": "Módulo específico: rigidez normalizada por densidad, útil solo cuando masa y rigidez son criterios pertinentes.", "variables": {"E": "módulo de Young", "\\rho": "densidad"}},
                {"latex": "S=\\sum_{i=1}^{n}w_i x_i^*", "meaning": "Puntuación multicriterio de cribado con propiedades normalizadas x*i y pesos explícitos wi; no es una medida de seguridad ni eficacia.", "variables": {"w_i": "peso del criterio i", "x_i^*": "valor normalizado del criterio i"}}
            ],
            "key_points": [
                "Las restricciones esenciales se aplican antes de una puntuación compensatoria.",
                "Una matriz de decisión debe conservar métrica, unidad, fuente, incertidumbre y regla de normalización.",
                "No deben forzarse métricas mecánicas no equivalentes entre materiales con modos de fallo diferentes.",
                "La sensibilidad de pesos y propiedades forma parte del resultado y puede convertir un ranking en una decisión provisional."
            ]
        },
        {
            "heading": "4. Biocompatibilidad, seguridad biológica y límite de la selección de materiales",
            "paragraphs": [
                "Biocompatibilidad no es una propiedad intrínseca que pueda marcarse con una casilla junto al módulo o la densidad. El concepto depende de la función que debe realizar un material o dispositivo y de la respuesta del sistema biológico en ese contexto. La literatura de biomateriales ha insistido en pasar de definiciones genéricas basadas solo en el material a definiciones ligadas a la aplicación. Un polímero, metal o cerámica con una historia extensa de uso no queda automáticamente validado para otra formulación, superficie, proceso, localización o duración de contacto. En U1 esta idea funciona como frontera conceptual: el cribado de propiedades reduce candidatos, pero no demuestra seguridad biológica.",
                "La evaluación biológica de un dispositivo se integra en gestión de riesgos y considera el dispositivo final, los materiales constituyentes, el tipo y duración de contacto, la composición química, el procesamiento y la evidencia disponible. ISO 10993-1:2025 actualiza los requisitos y principios generales para evaluar seguridad biológica dentro de ese proceso. La guía FDA de 2023 sobre ISO 10993-1 sigue siendo una referencia regulatoria estadounidense para preparar información de biocompatibilidad y enfatiza un enfoque basado en riesgo. Estas fuentes se usan aquí para enseñar el límite de inferencia, no para certificar un diseño ni sustituir asesoría regulatoria.",
                "Procesamiento y superficie pueden alterar la pregunta biológica aun cuando el nombre del material permanezca igual. Impurezas, aditivos, productos de degradación, residuos de fabricación o esterilización, rugosidad, porosidad y recubrimientos pueden cambiar la exposición. Del mismo modo, un compuesto introduce interfaces y constituyentes adicionales. Por ello, la selección inicial debe registrar no solo «titanio», «polímero» o «cerámica», sino el grado o formulación, la ruta de fabricación prevista y qué características de superficie o degradación son relevantes. Las unidades posteriores desarrollarán estructura-propiedad, interfaz biológica, degradación, caracterización y evaluación preclínica con mayor profundidad.",
                "El producto válido de esta unidad es una selección de familia o candidato para continuar la investigación, acompañada por requisitos, datos, sensibilidad y una lista de evidencia pendiente. No es válido afirmar que un candidato es clínicamente superior, que será seguro en pacientes, que cumple una norma o que un dispositivo puede comercializarse. Esas conclusiones requieren diseño final, caracterización, evaluación biológica y mecánica apropiadas, gestión de riesgos, evidencia preclínica o clínica según corresponda y revisión regulatoria. Mantener esta frontera desde U1 evita que una matriz de materiales se convierta indebidamente en una recomendación clínica o de producto."
            ],
            "key_points": [
                "Biocompatibilidad depende del uso y del sistema material-dispositivo-biología; no es una propiedad absoluta de una familia.",
                "La evaluación biológica se integra en gestión de riesgos y depende del dispositivo final, contacto, duración, composición y procesamiento.",
                "Superficie, fabricación, esterilización y degradación pueden cambiar la exposición aunque la composición nominal parezca igual.",
                "Una selección de materiales es evidencia de ingeniería para continuar el desarrollo, no validación clínica, certificación normativa ni autorización de uso."
            ]
        }
    ],
    "glossary": [
        {"term": "biomaterial", "definition": "Materia, superficie o constructo que interactúa con sistemas biológicos en una aplicación definida; la etiqueta no implica por sí sola seguridad o eficacia."},
        {"term": "uso previsto", "definition": "Función, población o contexto, condiciones y propósito para los que se diseña un componente o dispositivo y que delimitan sus requisitos."},
        {"term": "familia de materiales", "definition": "Agrupación por estructura y enlace predominantes, como metales, cerámicas o polímeros; no sustituye los datos del material concreto."},
        {"term": "metal", "definition": "Material con enlace metálico y electrones deslocalizados; sus propiedades dependen de composición, microestructura y procesamiento."},
        {"term": "cerámica", "definition": "Material inorgánico no metálico de enlace principalmente iónico o covalente, con comportamiento dependiente de composición, porosidad, defectos y procesamiento."},
        {"term": "polímero", "definition": "Material formado por macromoléculas cuyas propiedades dependen de arquitectura molecular, masa molecular, cristalinidad, reticulación, temperatura y tiempo."},
        {"term": "compuesto", "definition": "Material con dos o más fases distinguibles diseñado para combinar o adaptar propiedades; la interfaz y orientación de fases son parte de su comportamiento."},
        {"term": "matriz", "definition": "Fase continua de un compuesto que rodea o transfiere carga hacia otras fases como fibras o partículas."},
        {"term": "refuerzo", "definition": "Fase añadida a un compuesto para modificar propiedades como rigidez, resistencia, tenacidad, desgaste o respuesta funcional."},
        {"term": "densidad", "definition": "Masa por unidad de volumen; permite comparar masa y calcular propiedades específicas cuando ese criterio es pertinente."},
        {"term": "esfuerzo ingenieril", "definition": "Fuerza axial dividida por el área transversal inicial de la probeta bajo la convención declarada."},
        {"term": "deformación ingenieril", "definition": "Cambio de longitud dividido por la longitud inicial de una probeta."},
        {"term": "módulo de Young", "definition": "Pendiente esfuerzo-deformación en un régimen elástico aproximadamente lineal; cuantifica rigidez, no resistencia a rotura."},
        {"term": "límite elástico", "definition": "Esfuerzo asociado al inicio convencional de deformación plástica permanente en materiales donde esa descripción es aplicable."},
        {"term": "resistencia última", "definition": "Máximo esfuerzo ingenieril registrado bajo un ensayo y modo de carga definidos."},
        {"term": "ductilidad", "definition": "Capacidad de acumular deformación plástica antes de fracturar, evaluada con una métrica y ensayo declarados."},
        {"term": "tenacidad", "definition": "Capacidad de absorber energía antes de fracturar; no es sinónimo de dureza ni de resistencia máxima."},
        {"term": "tenacidad a fractura", "definition": "Medida de resistencia a la propagación de una grieta bajo una geometría y modo de carga definidos."},
        {"term": "fatiga", "definition": "Daño y posible fallo producido por cargas cíclicas, dependiente de amplitud, tensión media, superficie, ambiente y número de ciclos."},
        {"term": "desgaste", "definition": "Pérdida o modificación de material por interacción mecánica entre superficies; puede acoplarse con fenómenos químicos."},
        {"term": "corrosión", "definition": "Degradación de un material, especialmente metálico, por reacciones químicas o electroquímicas con el ambiente."},
        {"term": "degradación", "definition": "Cambio progresivo de composición, masa, estructura o propiedades por mecanismos físicos, químicos o biológicos."},
        {"term": "propiedad superficial", "definition": "Característica de la interfaz, como química, energía, carga, rugosidad o porosidad, que puede diferir del volumen del material."},
        {"term": "módulo específico", "definition": "Relación E/ρ que normaliza rigidez por densidad; solo es útil cuando ambos atributos son relevantes para la decisión."},
        {"term": "matriz requisito-propiedad", "definition": "Registro que vincula cada necesidad funcional con una propiedad medible, unidad, umbral, fuente e incertidumbre."},
        {"term": "análisis de sensibilidad", "definition": "Reevaluación de una conclusión al variar datos o supuestos plausibles para identificar decisiones frágiles."},
        {"term": "biocompatibilidad", "definition": "Capacidad contextual de un material o dispositivo para desempeñar una función prevista con una respuesta biológica apropiada; no es una etiqueta universal."},
        {"term": "evaluación biológica", "definition": "Proceso basado en riesgo para identificar y evaluar peligros biológicos asociados con un dispositivo y su uso previsto."}
    ],
    "worked_examples": [
        {
            "title": "Esfuerzo, deformación y módulo en una probeta sintética",
            "scenario": "Una probeta sintética de área inicial 20 mm² y longitud inicial 50 mm soporta 4.0 kN y se alarga elásticamente 0.10 mm.",
            "reasoning_steps": ["Convertir 4.0 kN a 4000 N y conservar el área en mm² para obtener MPa.", "Calcular σ=4000/20=200 N/mm²=200 MPa.", "Calcular ε=0.10/50=0.002.", "Estimar E=200 MPa/0.002=100000 MPa=100 GPa y declarar que se supone un tramo lineal elástico."],
            "interpretation": "La probeta tiene una rigidez elástica sintética de aproximadamente 100 GPa bajo los supuestos del ejercicio; ese número no informa por sí solo resistencia, fatiga ni biocompatibilidad.",
            "limitations": ["El caso es sintético y supone carga axial uniforme.", "No incluye incertidumbre dimensional, no linealidad, plasticidad ni efectos ambientales."]
        },
        {
            "title": "Rigidez no equivale a resistencia",
            "scenario": "Dos candidatos sintéticos tienen E de 200 y 70 GPa, pero sus resistencias últimas son 500 y 900 MPa respectivamente.",
            "reasoning_steps": ["Separar el requisito de deformación elástica del requisito de fallo.", "Reconocer que el candidato con mayor E es más rígido, no necesariamente más resistente.", "Comprobar geometría y modo de carga antes de traducir propiedades a desempeño de una pieza.", "Registrar ambos criterios por separado en la matriz."],
            "interpretation": "Un único descriptor como «más fuerte» oculta propiedades físicamente distintas y puede invertir una selección.",
            "limitations": ["No se especifican fatiga, tenacidad, superficie ni ambiente.", "Los valores son educativos y no identifican aleaciones reales."]
        },
        {
            "title": "Cerámica estructural: detectar una métrica no comparable",
            "scenario": "Una tabla intenta comparar el límite elástico de dos metales con el de una cerámica que fractura sin deformación plástica apreciable.",
            "reasoning_steps": ["Identificar que el límite elástico no es una métrica equivalente para todos los candidatos.", "Definir el modo de carga y el criterio funcional de fallo.", "Sustituir la comparación forzada por resistencia en el modo pertinente, distribución de defectos o tenacidad a fractura según la pregunta.", "Marcar la celda original como no aplicable en vez de inventar un valor."],
            "interpretation": "La comparabilidad de la métrica es un requisito metodológico previo al ranking de materiales.",
            "limitations": ["No reemplaza un diseño estadístico de resistencia de cerámicas.", "El ejercicio no selecciona una cerámica para un dispositivo real."]
        },
        {
            "title": "Módulo específico y masa",
            "scenario": "Un material A tiene E=110 GPa y ρ=4.5 g/cm³; B tiene E=25 GPa y ρ=1.6 g/cm³. Se quiere comparar rigidez por densidad.",
            "reasoning_steps": ["Calcular EA/ρA≈24.4 GPa·cm³/g.", "Calcular EB/ρB≈15.6 GPa·cm³/g.", "Concluir que A tiene mayor módulo específico bajo esta métrica.", "Verificar si masa y rigidez son realmente los criterios dominantes antes de usar el cociente para decidir."],
            "interpretation": "Normalizar una propiedad puede ser útil, pero no elimina la necesidad de restricciones de resistencia, fatiga, geometría, procesamiento o superficie.",
            "limitations": ["No compara direccionalidad ni modos de fallo.", "Los valores son sintéticos y no constituyen datos de diseño."]
        },
        {
            "title": "Ranking sensible a los pesos",
            "scenario": "Tras aplicar restricciones, dos candidatos obtienen puntuaciones cercanas en rigidez específica, tenacidad y procesabilidad.",
            "reasoning_steps": ["Documentar normalización y pesos antes de calcular.", "Calcular el ranking nominal.", "Repetir aumentando y disminuyendo cada peso relevante un 20 % y renormalizar.", "Si cambia el primer puesto, informar una decisión provisional y señalar qué requisito o dato adicional reduciría la ambigüedad."],
            "interpretation": "La inestabilidad del ranking es información de ingeniería y no debe ocultarse con más decimales.",
            "limitations": ["Una puntuación multicriterio depende del modelo de decisión.", "No representa probabilidad de éxito, seguridad ni utilidad clínica."]
        }
    ],
    "guided_activities": [
        {
            "title": "Actividad guiada: selección trazable de una familia de biomateriales",
            "instructions": [
                "Trabaja solo con el escenario y la tabla sintética; no ensayes, contactes ni expongas personas, animales o muestras biológicas.",
                "Antes de mirar los candidatos, convierte el uso hipotético en requisitos esenciales y criterios deseables con unidades.",
                "Distingue propiedades del material de variables de geometría, procesamiento y superficie.",
                "Aplica primero restricciones de exclusión y solo después una puntuación multicriterio.",
                "Declara qué métricas no son directamente comparables entre familias y evita rellenarlas con valores inventados.",
                "Realiza al menos dos análisis de sensibilidad y limita la conclusión a un cribado educativo de candidatos."
            ],
            "problems": [
                "Escenario: se estudia un componente estructural hipotético y no implantable en este ejercicio. El requisito educativo pide módulo efectivo entre 15 y 130 GPa, densidad menor de 5 g/cm³, estabilidad química ≥3/5 y comportamiento bajo carga cíclica que deberá verificarse después.",
                "Tabla sintética: Metal-A E=110 GPa, ρ=4.5, resistencia a tracción=900 MPa, elongación=12 %, estabilidad=4/5; Metal-B E=200 GPa, ρ=7.9, resistencia=700 MPa, elongación=25 %, estabilidad=4/5; Cerámica-C E=280 GPa, ρ=3.9, resistencia a tracción=450 MPa, elongación<1 %, estabilidad=5/5; Polímero-P E=3.5 GPa, ρ=1.3, resistencia=90 MPa, elongación=20 %, estabilidad=4/5; Compuesto-X E longitudinal/transversal=25/10 GPa, ρ=1.6, resistencia longitudinal/transversal=350/120 MPa, elongación=2 %, estabilidad=4/5.",
                "Clasifica cada candidato por familia y señala qué dato muestra anisotropía o un modo de fallo que requiere cautela.",
                "Aplica las restricciones de módulo y densidad. Documenta por qué cada candidato pasa o queda fuera sin usar una puntuación para rescatar un incumplimiento esencial.",
                "Para los candidatos restantes, calcula E/ρ y explica qué pregunta responde y cuál no.",
                "Define tres criterios deseables adicionales y pesos que sumen 1. Justifica los pesos por el escenario, no por el candidato que prefieras.",
                "Normaliza los criterios con una regla explícita y calcula una puntuación S. Conserva la tabla antes de ordenar.",
                "Repite el ranking aumentando un 20 % el peso del criterio más importante y renormalizando los demás. Indica si cambia la decisión.",
                "Supón una incertidumbre de ±10 % en E del Compuesto-X y determina si puede cruzar el límite inferior de rigidez en alguna orientación.",
                "Explica por qué el límite elástico sería una mala columna común si la tabla incluyera una cerámica sin régimen plástico apreciable.",
                "Añade una columna de evidencia pendiente con al menos fatiga, desgaste/corrosión o degradación, efecto del procesamiento y condición de superficie.",
                "Redacta una conclusión de máximo 150 palabras que nombre un candidato para continuar el estudio o declare empate técnico, y enumere por qué esa conclusión no demuestra biocompatibilidad, seguridad de un dispositivo ni desempeño clínico."
            ],
            "deliverables": [
                "Matriz necesidad-requisito-propiedad-unidad-umbral antes de evaluar candidatos.",
                "Tabla de cribado por restricciones con justificación de cada exclusión.",
                "Cálculo de módulo específico para los candidatos pertinentes.",
                "Matriz multicriterio con normalización, pesos y puntuación reproducible.",
                "Dos análisis de sensibilidad, incluido el efecto de incertidumbre/orientación del compuesto.",
                "Lista de métricas no comparables y evidencia material pendiente.",
                "Conclusión acotada con límites de inferencia y siguiente ensayo o dato necesario."
            ],
            "checking_criteria": [
                "Los requisitos están definidos antes del ranking y conservan unidades.",
                "Las restricciones esenciales se aplican antes de la ponderación.",
                "E, resistencia, ductilidad y tenacidad no se tratan como sinónimos.",
                "Se reconoce la anisotropía del compuesto y la no equivalencia de ciertas métricas entre familias.",
                "La puntuación puede reconstruirse a partir de normalización y pesos explícitos.",
                "La sensibilidad muestra si el primer puesto es estable o provisional.",
                "La evidencia pendiente incluye comportamiento temporal, superficie/procesamiento y evaluación biológica posterior.",
                "No se afirma que un material sea clínicamente superior, seguro o conforme con una norma.",
                "No se utilizan personas, animales ni muestras biológicas.",
                "Otra persona puede repetir el cribado con la entrega sin decisiones ocultas."
            ]
        }
    ],
    "common_errors": [
        {"error": "Elegir primero una familia y luego adaptar los requisitos para justificarla.", "correction": "Definir uso, restricciones y métricas antes de inspeccionar candidatos."},
        {"error": "Usar rigidez, resistencia, dureza y tenacidad como sinónimos.", "correction": "Vincular cada propiedad con su definición, ensayo y modo de fallo."},
        {"error": "Comparar límite elástico de un metal con una cerámica que fractura sin plasticidad apreciable.", "correction": "Elegir una métrica funcional comparable o declarar no aplicable."},
        {"error": "Usar un valor de ficha técnica sin grado, orientación, procesamiento o condición.", "correction": "Registrar material específico, estado, método de ensayo y procedencia."},
        {"error": "Ignorar geometría porque ya se conoce el módulo del material.", "correction": "Separar propiedad del material de rigidez y resistencia de la pieza."},
        {"error": "Dar una puntuación alta a un candidato que incumple un requisito esencial.", "correction": "Aplicar restricciones de exclusión antes de criterios compensatorios."},
        {"error": "Ocultar que el ranking cambia al variar los pesos.", "correction": "Informar sensibilidad y mantener alternativas cuando la decisión sea frágil."},
        {"error": "Tratar un compuesto como isotrópico por defecto.", "correction": "Declarar orientación, arquitectura de refuerzo y propiedad direccional pertinente."},
        {"error": "Etiquetar un material como biocompatible de forma universal.", "correction": "Vincular la evaluación biológica al dispositivo, uso, contacto, duración, composición y procesamiento."},
        {"error": "Convertir una matriz educativa de materiales en una recomendación clínica o regulatoria.", "correction": "Limitarla a cribado de ingeniería y enumerar las verificaciones posteriores necesarias."}
    ],
    "self_assessment": [
        {"question": "¿Por qué una sustancia usada previamente en medicina no es automáticamente adecuada para cualquier dispositivo?", "answer": "Porque función, geometría, superficie, procesamiento, ambiente, tipo y duración de contacto cambian los requisitos y la exposición.", "reasoning": "La adecuación es contextual y debe evaluarse para el uso definido.", "common_error": "Tratar el nombre del material como una certificación universal."},
        {"question": "¿Qué diferencia existe entre módulo de Young y resistencia última?", "answer": "El módulo cuantifica rigidez elástica; la resistencia última es el máximo esfuerzo ingenieril de un ensayo definido.", "reasoning": "Un material puede ser más rígido y, sin embargo, tener menor resistencia última que otro.", "common_error": "Llamar al material con mayor E «más fuerte»."},
        {"question": "Una probeta de 10 mm² recibe 2 kN. ¿Cuál es el esfuerzo ingenieril?", "answer": "200 MPa.", "reasoning": "2000 N/10 mm²=200 N/mm²=200 MPa.", "common_error": "No convertir kN o confundir área inicial con longitud."},
        {"question": "¿Por qué el límite elástico puede ser una mala métrica común para metal y cerámica?", "answer": "Porque una cerámica puede fracturar sin un régimen de deformación plástica comparable al usado para definir el límite elástico de un metal.", "reasoning": "La métrica debe corresponder al mecanismo y modo de fallo.", "common_error": "Forzar un número para llenar todas las celdas de la tabla."},
        {"question": "¿Qué aporta E/ρ?", "answer": "Compara rigidez por unidad de densidad cuando masa y rigidez son criterios pertinentes.", "reasoning": "Es una propiedad específica, no un índice universal de desempeño.", "common_error": "Elegir automáticamente el mayor E/ρ aunque falle otras restricciones."},
        {"question": "¿Por qué las restricciones se aplican antes que una puntuación ponderada?", "answer": "Porque un incumplimiento esencial no debe compensarse con buen desempeño en criterios secundarios.", "reasoning": "Separar restricciones de objetivos evita rankings matemáticamente atractivos pero funcionalmente inválidos.", "common_error": "Permitir compensación total entre todos los criterios."},
        {"question": "¿Qué significa que un ranking sea sensible a los pesos?", "answer": "Que candidatos cercanos cambian de orden cuando se modifican supuestos razonables sobre la importancia de los criterios.", "reasoning": "La decisión debe presentarse como provisional o requerir evidencia adicional.", "common_error": "Añadir decimales para aparentar precisión."},
        {"question": "¿Qué característica de un compuesto obliga a declarar orientación?", "answer": "Las propiedades pueden ser anisotrópicas porque dependen de la arquitectura y dirección del refuerzo.", "reasoning": "Un único módulo puede no representar todas las direcciones de carga.", "common_error": "Usar el valor longitudinal como si fuera isotrópico."},
        {"question": "¿Por qué biocompatibilidad no funciona como una propiedad absoluta de un material?", "answer": "Porque la respuesta apropiada depende de la función y del sistema dispositivo-material-biología, incluido contacto, duración y procesamiento.", "reasoning": "La evaluación biológica se integra en un contexto de uso y riesgo.", "common_error": "Escribir simplemente «biocompatible: sí/no» sin contexto."},
        {"question": "¿Qué puede concluirse al final de U1?", "answer": "Puede justificarse qué candidatos merecen continuar a caracterización y evaluación; no puede demostrarse seguridad, desempeño clínico ni conformidad regulatoria.", "reasoning": "El cribado de propiedades es solo una etapa de un proceso de diseño y evaluación más amplio.", "common_error": "Convertir la selección material en autorización de un dispositivo."}
    ],
    "biomedical_connections": [
        {"topic": "Implantes estructurales", "connection": "La selección combina requisitos de carga, fatiga, desgaste, densidad, superficie y ambiente; U1 solo realiza el cribado inicial."},
        {"topic": "Dispositivos cardiovasculares", "connection": "Flexibilidad, fatiga, superficie y procesamiento pueden dominar la selección y muestran por qué una familia no tiene ventaja universal."},
        {"topic": "Prótesis y órtesis", "connection": "Propiedades específicas, anisotropía y manufactura permiten razonar sobre masa, rigidez y durabilidad sin inferir beneficio clínico."},
        {"topic": "Ingeniería de tejidos", "connection": "Polímeros, cerámicas y compuestos pueden diseñarse con degradación y arquitectura funcionales, pero la respuesta biológica se estudia en unidades posteriores."},
        {"topic": "Desarrollo de dispositivos médicos", "connection": "La matriz requisito-propiedad conecta ciencia de materiales con diseño, gestión de riesgos y evidencia de verificación posterior."}
    ],
    "sources": [
        {"title": "Biomaterial Technologies", "organization": "National Institute of Biomedical Imaging and Bioengineering (NIH)", "url": "https://www.nibib.nih.gov/science-education/science-topics/biomaterial-technologies", "type": "recurso oficial", "description": "Panorama oficial de biomateriales, materiales sintéticos y relación entre propiedades y funciones de dispositivos biomédicos.", "verification_status": "verified_directly", "locator": "NIBIB Science Education, Biomaterial Technologies; consultado 2026-08-24."},
        {"title": "Biomaterials: Been There, Done That, and Evolving into the Future", "organization": "Annual Review of Biomedical Engineering / PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/31167106/", "type": "revisión disciplinar", "description": "Evolución del campo de biomateriales y relación entre ciencia de materiales, biointerfaz y aplicaciones.", "verification_status": "verified_directly", "doi": "10.1146/annurev-bioeng-062117-120940", "locator": "Annu Rev Biomed Eng. 2019;21:171-191; PMID 31167106."},
        {"title": "Design and development of metallic biomaterials with biological and mechanical biocompatibility", "organization": "Journal of Biomedical Materials Research Part A / PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/30861312/", "type": "revisión disciplinar", "description": "Discute diseño de biomateriales metálicos, módulo de Young, resistencia a fatiga y compatibilidad mecánica.", "verification_status": "verified_directly", "doi": "10.1002/jbm.a.36667", "locator": "J Biomed Mater Res A. 2019;107(5):944-954; PMID 30861312."},
        {"title": "Ceramic Materials for Biomedical Applications: An Overview on Properties and Fabrication Processes", "organization": "Journal of Functional Biomaterials / PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/36976070/", "type": "revisión disciplinar", "description": "Propiedades físicas, químicas y mecánicas de biocerámicas y relación con procesos de fabricación.", "verification_status": "verified_directly", "doi": "10.3390/jfb14030146", "locator": "J Funct Biomater. 2023;14(3):146; PMID 36976070; PMCID PMC10052110."},
        {"title": "Polymeric Biomaterials for Medical Implants and Devices", "organization": "ACS Biomaterials Science & Engineering / PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/33465850/", "type": "revisión disciplinar", "description": "Revisa polímeros empleados en implantes y dispositivos y los requisitos mecánicos, químicos y de procesamiento asociados.", "verification_status": "verified_directly", "doi": "10.1021/acsbiomaterials.5b00429", "locator": "ACS Biomater Sci Eng. 2016;2(4):454-472; PMID 33465850."},
        {"title": "A comprehensive review of biodegradable synthetic polymer-ceramic composites and their manufacture for biomedical applications", "organization": "Bioactive Materials / PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/30533554/", "type": "revisión disciplinar", "description": "Compara metales, cerámicas, polímeros y compuestos y muestra cómo los compuestos combinan fases para adaptar propiedades.", "verification_status": "verified_directly", "doi": "10.1016/j.bioactmat.2018.11.003", "locator": "Bioact Mater. 2019;4:22-36; PMID 30533554; PMCID PMC6258879."},
        {"title": "On the mechanisms of biocompatibility", "organization": "Biomaterials / PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/18440630/", "type": "revisión conceptual", "description": "Analiza mecanismos y definiciones contextuales de biocompatibilidad y su relación con la función del dispositivo.", "verification_status": "verified_directly", "doi": "10.1016/j.biomaterials.2008.04.023", "locator": "Biomaterials. 2008;29(20):2941-2953; PMID 18440630."},
        {"title": "ISO 10993-1:2025 Biological evaluation of medical devices — Part 1", "organization": "International Organization for Standardization", "url": "https://www.iso.org/standard/10993-1", "type": "norma internacional", "description": "Edición 2025: requisitos y principios generales para evaluación de seguridad biológica dentro de un proceso de gestión de riesgos.", "verification_status": "verified_directly", "locator": "ISO 10993-1:2025, edition 6, published 2025-11."},
        {"title": "Use of International Standard ISO 10993-1 — Guidance for Industry and FDA Staff", "organization": "U.S. Food and Drug Administration", "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-international-standard-iso-10993-1-biological-evaluation-medical-devices-part-1-evaluation-and", "type": "guía regulatoria", "description": "Guía FDA final de 2023 sobre evaluación biológica basada en riesgo para dispositivos en contacto con el cuerpo; se usa aquí para delimitar inferencias regulatorias.", "verification_status": "verified_directly", "locator": "FDA final guidance, issued September 8, 2023; docket FDA-2013-D-0350."}
    ],
    "editorial_notice": "Material educativo de Biomateriales U1 con contenido disciplinar curado y estado review. Los valores de los ejemplos y de la actividad son sintéticos salvo cuando se identifica una fuente. La unidad no constituye revisión disciplinar externa, selección profesional de material para un dispositivo real, validación preclínica o clínica, evaluación de seguridad biológica, recomendación terapéutica ni demostración de conformidad regulatoria. La referencia a ISO 10993-1:2025 y a la guía FDA se utiliza para enseñar el límite de inferencia y no certifica ningún diseño."
})

text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
assert GENERIC.casefold() not in text.casefold(), "generic template marker remains"
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
print("Curated Biomateriales U1 and synchronized exact generated mirror")
