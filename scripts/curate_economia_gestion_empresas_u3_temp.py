#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-03.json"
GENERIC = "Concepto de la unidad que debe definirse mediante entidades observables"


def dump(payload: dict) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    SOURCE.write_text(text, encoding="utf-8")
    MIRROR.write_text(text, encoding="utf-8")


def main() -> None:
    unit = json.loads(SOURCE.read_text(encoding="utf-8"))
    unit["purpose"] = (
        "Analizar y mejorar operaciones biomédicas sintéticas mediante mapas de proceso, unidades de flujo, tiempos de ciclo, "
        "throughput, trabajo en proceso, capacidad, cuellos de botella, utilización, inventario y medidas de calidad. La unidad "
        "usa la Ley de Little y modelos introductorios de reposición solo bajo supuestos declarados y enseña a probar cambios con "
        "PDSA y medidas de resultado, proceso y equilibrio. No constituye un procedimiento operativo institucional, una recomendación "
        "de dotación o agenda clínica, ni evidencia de acreditación de un laboratorio real."
    )
    unit["learning_objectives"] = [
        "Representar un proceso de laboratorio o servicio mediante límites, unidad de flujo, etapas, colas, recursos, entradas, salidas y eventos temporales, distinguiendo tiempo de proceso, espera y tiempo total de flujo.",
        "Calcular capacidad por etapa, identificar el cuello de botella de un proceso secuencial y diferenciar capacidad, throughput, demanda y utilización con unidades temporales coherentes.",
        "Aplicar L=λW en sistemas estables y bien delimitados para relacionar trabajo en proceso, tasa de flujo y tiempo medio, explicando cuándo la relación no debe usarse de forma mecánica.",
        "Construir un modelo introductorio de inventario con demanda, lead time, punto de reposición y stock de seguridad, incorporando caducidad, lotes y riesgo de stock-out como supuestos explícitos en contextos biomédicos.",
        "Diseñar una mejora de proceso con objetivo operacional, teoría de cambio, ciclo PDSA y familia de medidas de resultado, proceso y equilibrio, interpretando los datos a lo largo del tiempo sin confundir una mejora local con causalidad clínica.",
        "Resolver y comunicar un caso sintético de gestión operativa con mapa de proceso, capacidad, inventario, calidad, sensibilidad y límites, preservando datos, definiciones operacionales, versiones y decisiones antes–después."
    ]
    unit["theory_sections"] = [
        {
            "heading": "1. Flujo de proceso, tiempo de ciclo, throughput y Ley de Little",
            "paragraphs": [
                "Una operación se entiende mejor cuando se dibuja antes de resumirse con indicadores. El mapa debe declarar qué unidad fluye —por ejemplo, una muestra sintética, una orden o un equipo de mantenimiento—, dónde comienza y termina el proceso, qué etapas transforman la unidad y dónde puede esperar. Esta frontera evita mezclar tiempos de procesos distintos. El tiempo de proceso es el tiempo en que una etapa trabaja activamente sobre la unidad; el tiempo de espera es tiempo dentro del sistema sin procesamiento; y el tiempo de flujo o lead time interno suma todos los intervalos desde entrada hasta salida según la definición adoptada.",
                "Throughput o tasa de flujo expresa cuántas unidades completan el sistema por unidad de tiempo. No es sinónimo de capacidad. La capacidad es el máximo sostenible bajo recursos, reglas y condiciones declaradas, mientras el throughput observado también depende de demanda, disponibilidad, fallos, mezcla de casos y otras restricciones. Un laboratorio con capacidad efectiva de 60 muestras por hora puede completar 40 porque solo recibió 40, o completar menos por indisponibilidad. Reportar utilización sin decir qué capacidad sirve de denominador puede producir porcentajes aparentemente precisos pero metodológicamente ambiguos.",
                "El trabajo en proceso —WIP— es el número de unidades que han entrado al sistema y todavía no lo han abandonado, incluyendo las que están siendo procesadas y, si la frontera así lo define, las que esperan. En servicios sanitarios puede ser tentador llamar WIP a cualquier persona o muestra presente, pero la unidad y el instante de conteo deben estar operacionalizados. Para este curso se usan únicamente datos sintéticos y se evita representar individuos reales. Una cola grande puede elevar WIP y tiempo de flujo sin aumentar el throughput cuando el cuello de botella permanece igual.",
                "La Ley de Little relaciona tres promedios de largo plazo: L=λW, donde L es el número medio de unidades en el sistema, λ la tasa media de flujo y W el tiempo medio que una unidad permanece en el sistema. Little demostró la relación bajo condiciones de estabilidad y existencia de los promedios pertinentes. Su fuerza es que no exige una distribución particular de tiempos de servicio; su límite pedagógico es igualmente importante: los tres términos deben referirse a la misma frontera, mismas unidades y un sistema suficientemente estable. Mezclar llegadas por hora con permanencia en días o usar una semana de crecimiento explosivo de cola sin advertir la inestabilidad invalida la interpretación simple.",
                "La relación sirve como control de coherencia y para explorar escenarios, no como una orden automática de reducir WIP. Si λ=12 muestras/h y W=1,5 h en un sistema estable, L=18 muestras en promedio. Si se supone que λ permanece en 12 y un rediseño reduce WIP medio a 12, el W compatible sería 1 h; pero esto no demuestra que retirar físicamente muestras de una cola cause esa mejora. El equipo debe identificar qué cambio de proceso permitiría mantener throughput con menos espera y comprobarlo con datos temporales."
            ],
            "equations": [
                {"latex": "L=\\lambda W", "meaning": "Ley de Little para promedios coherentes de un sistema estable y una misma frontera operacional.", "variables": {"L": "trabajo en proceso medio, unidades", "\\lambda": "tasa media de flujo o throughput, unidades/tiempo", "W": "tiempo medio en el sistema, tiempo"}},
                {"latex": "Throughput=\\frac{Unidades\\ completadas}{Tiempo\\ observado}", "meaning": "Tasa de salida observada durante una ventana definida; no equivale automáticamente a capacidad máxima.", "variables": {"Unidades completadas": "unidades que cruzan la salida definida", "Tiempo observado": "duración de la ventana de observación"}}
            ],
            "key_points": [
                "Mapa, frontera y unidad de flujo deben definirse antes de calcular tiempos o tasas.",
                "Throughput observado y capacidad son magnitudes distintas aunque compartan unidades.",
                "WIP incluye unidades dentro del sistema según una regla de conteo explícita.",
                "L=λW exige coherencia de frontera, unidades, promedios y estabilidad; no prueba causalidad de una intervención."
            ]
        },
        {
            "heading": "2. Capacidad, cuello de botella, utilización y variabilidad de la demanda",
            "paragraphs": [
                "En un proceso secuencial simple, cada etapa tiene una capacidad efectiva expresada como unidades por tiempo bajo condiciones normales declaradas. Si una etapa tarda cuatro minutos por unidad durante 480 minutos disponibles, su capacidad teórica del turno es 120 unidades antes de considerar pérdidas adicionales. Cuando las unidades deben pasar por todas las etapas y no existen rutas paralelas que cambien el modelo, la etapa de menor capacidad limita el throughput máximo del proceso y se denomina cuello de botella. Aumentar capacidad en una etapa no limitante puede no cambiar la salida total.",
                "La capacidad de diseño y la capacidad efectiva no son necesariamente iguales. Mantenimiento, cambios de lote, controles, pausas, mezcla de casos, formación, restricciones de calidad y disponibilidad de insumos reducen la salida sostenible. El libro abierto Fundamentals of Operations Management distingue explícitamente estos conceptos y muestra que factores operativos y de calidad pueden afectar la capacidad efectiva. En un servicio biomédico, estas pérdidas no deben tratarse como desperdicio eliminable por defecto: algunas representan controles esenciales y no pueden recortarse sin evaluar calidad, seguridad y cumplimiento.",
                "La utilización compara una carga o tasa de demanda con una capacidad de referencia. En un modelo introductorio, u=λ_d/C. Una utilización del 90 % significa que la demanda media usa una gran fracción de la capacidad modelada, no que cada recurso esté ocupado exactamente 90 % del tiempo. Si la demanda media supera de forma sostenida la capacidad de un sistema sin mecanismo de rechazo o desvío, la cola tenderá a crecer. Incluso por debajo de 100 %, la variabilidad de llegadas y tiempos de servicio puede generar esperas; por eso perseguir utilización máxima no equivale a optimizar un servicio.",
                "La variabilidad hace que los promedios escondan episodios de congestión. Dos procesos con la misma demanda media pueden experimentar esperas diferentes si uno recibe llegadas uniformes y el otro concentra unidades en picos. U3 no desarrolla teoría de colas avanzada, pero exige representar escenarios de pico, indisponibilidad y mezcla de casos. Un plan de capacidad debe distinguir qué es dato histórico, qué es capacidad nominal, qué es estimación y qué es margen de protección. Esta transparencia evita presentar una plantilla de personal o equipo como una recomendación clínica real.",
                "Mejorar el cuello de botella requiere identificar la restricción real y medir el efecto sistémico. Si un proceso tiene capacidades de 120, 60 y 96 unidades/turno, la segunda etapa limita la salida a 60 en el modelo. Duplicar la capacidad de la primera etapa no cambia ese límite y probablemente aumenta WIP antes de la segunda. Una intervención sobre el cuello puede desplazar la restricción a otra etapa; por eso se recalculan capacidad, cola y medidas de equilibrio después del cambio. El objetivo no es mantener todos los recursos ocupados, sino conseguir un flujo compatible con calidad y demanda."
            ],
            "equations": [
                {"latex": "C_i=\\frac{T_{disponible,i}}{t_{ciclo,i}}", "meaning": "Capacidad simplificada de una etapa cuando el tiempo de ciclo es aproximadamente constante y las unidades son homogéneas dentro del escenario.", "variables": {"C_i": "capacidad de la etapa i, unidades/periodo", "T_{disponible,i}": "tiempo efectivo disponible", "t_{ciclo,i}": "tiempo de ciclo por unidad"}},
                {"latex": "C_{proceso}=\\min_i(C_i)", "meaning": "Capacidad de un proceso estrictamente secuencial simple limitada por la etapa de menor capacidad; no aplica sin revisar rutas paralelas, lotes, reentrada o mezcla de productos.", "variables": {"C_{proceso}": "capacidad máxima del proceso modelado", "C_i": "capacidad de cada etapa"}},
                {"latex": "u=\\frac{\\lambda_d}{C}", "meaning": "Utilización o carga relativa introductoria basada en demanda media y una capacidad definida de forma coherente.", "variables": {"u": "utilización modelada", "\\lambda_d": "tasa media de demanda", "C": "capacidad de referencia"}}
            ],
            "key_points": [
                "El cuello de botella limita la capacidad de un proceso secuencial simple y puede desplazarse después de una mejora.",
                "Capacidad efectiva incorpora condiciones normales y restricciones reales; no es necesariamente capacidad de diseño.",
                "Utilización alta no implica flujo óptimo y la variabilidad puede generar espera antes de llegar a 100 %.",
                "Toda propuesta de capacidad debe conservar controles de calidad y declararse como análisis sintético, no como dotación institucional."
            ]
        },
        {
            "heading": "3. Inventario, lead time, punto de reposición y riesgo de stock-out",
            "paragraphs": [
                "Inventario desacopla momentos de suministro y consumo, pero también inmoviliza recursos y puede caducar, deteriorarse u obsolescer. En laboratorios biomédicos son especialmente relevantes reactivos, controles, consumibles, repuestos y material de protección, cada uno con restricciones distintas de almacenamiento y vida útil. La OMS incluye compras e inventario entre los elementos esenciales de un sistema de gestión de calidad de laboratorio. U3 no enseña una política institucional de stock: construye modelos sintéticos para comprender qué datos hacen falta antes de decidir cuánto y cuándo reponer.",
                "El lead time es el intervalo desde emitir una orden hasta disponer realmente del material para uso bajo la definición del proceso. Puede incluir aprobación, preparación, transporte, recepción, inspección o cuarentena. Si la demanda fuera estable y conocida, un punto de reposición elemental cubriría el consumo esperado durante el lead time. Cuando existe variabilidad o se desea protección adicional, se añade stock de seguridad. La fórmula ROP=dL+SS es una aproximación transparente siempre que d y L estén expresados en unidades compatibles y se declaren los supuestos de variabilidad.",
                "Stock de seguridad no significa stock sin límite. Aumentarlo puede reducir probabilidad de stock-out bajo el modelo, pero eleva inventario medio, espacio utilizado, capital inmovilizado y riesgo de vencimiento. Para materiales perecederos, los lotes, fechas de caducidad y política de rotación pueden dominar la decisión. Un escenario biomédico debe incluir al menos un control de caducidad y una perturbación del lead time; de lo contrario un punto de reposición matemáticamente correcto puede producir desperdicio o falta de material en condiciones plausibles.",
                "El inventario de trabajo en proceso y el inventario físico de suministros comparten la idea de unidades que esperan, pero responden a preguntas operativas distintas. Una cola de muestras sintéticas delante de un analizador es WIP del proceso; cajas de reactivo disponibles son stock de suministro. Reducir uno no necesariamente reduce el otro. El mapa de U3 etiqueta ambos explícitamente y evita usar la palabra inventario como categoría única, porque los mecanismos de capacidad, caducidad y reposición son diferentes.",
                "Las decisiones reales de inventario de un laboratorio dependen además de requisitos locales, contratos, criticidad, almacenamiento, trazabilidad de lotes, continuidad operativa y gestión de riesgos. ISO 15189:2022 establece requisitos de calidad y competencia para laboratorios médicos, pero esta unidad no reproduce cláusulas ni demuestra conformidad con la norma. Los modelos de reposición son ejercicios de razonamiento y deben someterse a procedimientos institucionales y conocimiento profesional antes de cualquier uso real."
            ],
            "equations": [
                {"latex": "ROP=dL+SS", "meaning": "Punto de reposición introductorio: consumo esperado durante el lead time más stock de seguridad definido por el modelo.", "variables": {"ROP": "nivel de inventario que dispara la reposición", "d": "demanda media por unidad de tiempo", "L": "lead time en la misma unidad temporal", "SS": "stock de seguridad"}}
            ],
            "key_points": [
                "Inventario protege continuidad pero introduce coste, espacio, caducidad y obsolescencia.",
                "Lead time debe incluir las etapas reales hasta que el material está disponible según la definición operacional.",
                "ROP=dL+SS es un modelo introductorio que necesita demanda, lead time, unidades y supuestos explícitos.",
                "WIP de proceso y stock de suministros son inventarios distintos y requieren métricas y decisiones diferentes."
            ]
        },
        {
            "heading": "4. Calidad operacional y mejora: PDSA, medidas de equilibrio y datos en el tiempo",
            "paragraphs": [
                "Calidad operacional no se reduce a velocidad. El manual de gestión de calidad de laboratorios de la OMS subraya exactitud, fiabilidad y oportunidad dentro de un sistema de procesos. Acelerar una etapa mientras aumentan repeticiones, errores de identificación, desperdicio o carga de trabajo puede ser una degradación sistémica. Por eso cualquier objetivo de mejora de U3 incluye una familia de medidas y no un único KPI. En un escenario sintético pueden combinarse tiempo de flujo como resultado, cumplimiento de un paso crítico como medida de proceso y tasa de reproceso como medida de equilibrio.",
                "El Model for Improvement de IHI comienza preguntando qué se quiere lograr, cómo se sabrá que un cambio es una mejora y qué cambio podría producirla. Después utiliza ciclos Plan-Do-Study-Act para probar y adaptar cambios. La prueba pequeña es diferente de la implementación permanente: un resultado favorable en un ciclo no autoriza desplegar el cambio en todas las condiciones. En el curso, los PDSA se simulan con datos sintéticos y se documentan predicción, cambio, medida, observación, aprendizaje y siguiente decisión.",
                "Las medidas de resultado describen el efecto final que interesa al objetivo del proceso; las de proceso comprueban si el mecanismo propuesto se ejecuta; y las de equilibrio buscan daños o desplazamientos hacia otra parte del sistema. IHI recomienda explícitamente usar estas perspectivas conjuntamente. La selección necesita definiciones operacionales: numerador, denominador, inclusión, exclusión, unidad y frecuencia. Cambiar la definición de turnaround time entre semanas puede fabricar una aparente mejora sin que el proceso haya cambiado.",
                "La mejora es temporal y debe observarse a lo largo del tiempo. Un gráfico de ejecución ordena medidas cronológicamente y permite visualizar nivel, tendencias y patrones alrededor de una referencia. IHI lo usa como herramienta central para valorar cambios. U3 enseña una lectura introductoria: anotar cuándo ocurrió cada cambio, conservar los puntos desfavorables y evitar concluir causalidad por una sola comparación antes–después. Un cambio de demanda, mezcla de casos, instrumento o regla de medición puede explicar parte de la diferencia.",
                "La secuencia final de U3 es mapear → medir → localizar restricción → proponer cambio → predecir → probar a pequeña escala → estudiar resultado/proceso/equilibrio → adaptar. Una mejora sólida debe poder ser auditada por otra persona y debe declarar qué condiciones no fueron probadas. En servicios sanitarios reales, rediseñar agendas, flujos de pacientes, dotación, prioridades o procedimientos requiere gobernanza, datos protegidos, participación de partes afectadas y controles locales; el ejercicio académico no sustituye ninguno de esos procesos."
            ],
            "key_points": [
                "Calidad operacional combina oportunidad con exactitud, fiabilidad y consecuencias del proceso; velocidad aislada es insuficiente.",
                "PDSA prueba cambios y produce aprendizaje iterativo; probar no equivale a implementar permanentemente.",
                "Resultado, proceso y equilibrio deben medirse con definiciones operacionales estables.",
                "Los datos se trazan en el tiempo y los cambios se anotan; una comparación antes–después no demuestra causalidad por sí sola."
            ]
        }
    ]
    unit["glossary"] = [
        {"term": "Proceso", "definition": "Secuencia delimitada de actividades y esperas que transforma entradas en salidas para una unidad de flujo definida."},
        {"term": "Unidad de flujo", "definition": "Entidad cuyo recorrido se sigue a través del proceso, por ejemplo una muestra sintética, una orden o un equipo."},
        {"term": "Tiempo de proceso", "definition": "Tiempo durante el cual una actividad trabaja activamente sobre la unidad de flujo según la definición del análisis."},
        {"term": "Tiempo de espera", "definition": "Tiempo que una unidad permanece dentro de la frontera del sistema sin ser procesada."},
        {"term": "Tiempo de flujo", "definition": "Tiempo total desde la entrada hasta la salida definidas, incluyendo proceso y espera."},
        {"term": "Throughput", "definition": "Tasa observada de unidades que completan un proceso por unidad de tiempo durante una ventana especificada."},
        {"term": "Trabajo en proceso (WIP)", "definition": "Número de unidades que han entrado en el sistema y todavía no han salido según una regla de conteo explícita."},
        {"term": "Ley de Little", "definition": "Relación L=λW entre WIP medio, tasa media de flujo y tiempo medio en un sistema estable y coherentemente delimitado."},
        {"term": "Capacidad", "definition": "Tasa máxima sostenible de salida bajo recursos, reglas y condiciones declaradas."},
        {"term": "Capacidad efectiva", "definition": "Capacidad alcanzable bajo condiciones normales después de considerar restricciones operativas pertinentes."},
        {"term": "Cuello de botella", "definition": "Etapa o recurso que limita la capacidad de un proceso dentro del modelo y demanda considerados."},
        {"term": "Utilización", "definition": "Carga o demanda relativa a una capacidad de referencia definida con unidades compatibles."},
        {"term": "Variabilidad", "definition": "Cambios en llegadas, tiempos, mezcla de casos, recursos u otras condiciones que alteran desempeño alrededor de un promedio."},
        {"term": "Inventario", "definition": "Unidades físicas almacenadas o en tránsito que se mantienen para uso futuro; debe distinguirse del WIP del proceso."},
        {"term": "Lead time de suministro", "definition": "Intervalo desde emitir una orden hasta disponer del material para uso bajo una definición operacional declarada."},
        {"term": "Punto de reposición", "definition": "Nivel de inventario que, bajo una política de revisión, desencadena una orden de reabastecimiento."},
        {"term": "Stock de seguridad", "definition": "Inventario adicional incluido para proteger frente a incertidumbre de demanda o lead time según un modelo y nivel de riesgo declarados."},
        {"term": "Stock-out", "definition": "Situación en la que el inventario disponible es insuficiente para una demanda que el sistema pretende atender."},
        {"term": "Medida de resultado", "definition": "Indicador del efecto final que el proyecto de mejora intenta modificar."},
        {"term": "Medida de proceso", "definition": "Indicador de si los pasos o mecanismos propuestos se ejecutan como se definieron."},
        {"term": "Medida de equilibrio", "definition": "Indicador destinado a detectar consecuencias adversas o desplazamientos de problema hacia otra parte del sistema."},
        {"term": "PDSA", "definition": "Ciclo Plan-Do-Study-Act para planificar, probar, estudiar y adaptar un cambio de forma iterativa."},
        {"term": "Gráfico de ejecución", "definition": "Serie temporal de una medida utilizada para observar patrones y aprendizaje de mejora a lo largo del tiempo."}
    ]
    unit["worked_examples"] = [
        {
            "title": "Localizar el cuello de botella de un flujo sintético de muestras",
            "scenario": "Tres etapas secuenciales tardan 4, 8 y 5 minutos por muestra y disponen de 480 minutos efectivos por turno.",
            "reasoning_steps": [
                "Entrada: t1=4, t2=8, t3=5 min/unidad; T=480 min por etapa.",
                "Capacidades: C1=480/4=120, C2=480/8=60 y C3=480/5=96 muestras/turno.",
                "El mínimo es 60; la etapa 2 es el cuello de botella del modelo secuencial.",
                "Acelerar la etapa 1 a 2 minutos aumenta C1 a 240 pero deja Cproceso=60.",
                "Control: comprobar que no existan rutas paralelas, lotes ni restricciones adicionales antes de usar la regla del mínimo."
            ],
            "interpretation": "La capacidad sistémica no aumenta por mejorar una etapa que no limita el flujo; puede aumentar WIP antes del cuello.",
            "limitations": ["Modelo determinista sin variabilidad, fallos, cambios de lote ni mezcla de muestras."]
        },
        {
            "title": "Usar la Ley de Little como control de coherencia",
            "scenario": "Un sistema sintético estable completa 12 muestras/h y el tiempo medio desde entrada hasta salida es 1,5 h.",
            "reasoning_steps": [
                "Entrada: λ=12 muestras/h y W=1,5 h.",
                "Aplicar L=λW: L=12×1,5=18 muestras de WIP medio.",
                "Si el WIP observado fuera 36 con los otros promedios estables, revisar frontera, unidades, ventana o estabilidad antes de aceptar el conjunto de métricas.",
                "Escenario: mantener λ=12 y reducir WIP medio a 12 sería compatible con W=1 h.",
                "No inferir que retirar seis unidades de la cola causa automáticamente el nuevo tiempo; hace falta un cambio de proceso que preserve throughput."
            ],
            "interpretation": "Little relaciona promedios coherentes y permite detectar inconsistencias o explorar escenarios de flujo.",
            "limitations": ["No se aplica mecánicamente durante crecimiento sostenido de cola o con fronteras/ventanas incompatibles."]
        },
        {
            "title": "Utilización media y riesgo de congestión",
            "scenario": "Un equipo tiene capacidad efectiva modelada de 60 órdenes/h. La demanda media base es 54/h y en un escenario de pico sostenido llega a 63/h.",
            "reasoning_steps": [
                "Base: u=54/60=0,90 o 90 %.",
                "Pico: u=63/60=1,05 o 105 % respecto de la capacidad definida.",
                "Si no existe rechazo, desvío o capacidad adicional, una entrada sostenida mayor que la salida máxima hace crecer la cola.",
                "Incluso al 90 %, variabilidad en llegadas o tiempos puede generar espera; no se supone cola cero.",
                "Control: añadir un escenario de indisponibilidad que reduzca temporalmente C y observar cómo cambia la conclusión."
            ],
            "interpretation": "La utilización ayuda a detectar presión de capacidad, pero no determina por sí sola tiempos de espera ni calidad.",
            "limitations": ["No es un modelo de colas completo y no debe usarse para programar personal o pacientes reales."]
        },
        {
            "title": "Punto de reposición de un reactivo sintético",
            "scenario": "Un laboratorio simulado consume 20 kits/día, el lead time esperado es 4 días y el ejercicio fija 30 kits de stock de seguridad.",
            "reasoning_steps": [
                "Entrada: d=20 kits/día, L=4 días, SS=30 kits.",
                "Demanda esperada durante lead time: dL=80 kits.",
                "ROP=80+30=110 kits.",
                "Escenario: si el lead time sube a 6 días y SS no cambia, ROP=150 kits.",
                "Control de caducidad: comprobar si mantener ese nivel podría exceder consumo antes de vencimiento bajo los lotes sintéticos."
            ],
            "interpretation": "El ROP hace explícito cuánto depende la reposición de demanda, lead time y protección adicional.",
            "limitations": ["SS se proporciona como supuesto; un sistema real requiere estimar variabilidad, criticidad, caducidad y política local."]
        },
        {
            "title": "PDSA sintético con medida de equilibrio",
            "scenario": "Un flujo simulado prueba durante cinco periodos una reorganización de bandejas para reducir turnaround time; se registran también reprocesos.",
            "reasoning_steps": [
                "Objetivo: reducir tiempo mediano sin aumentar reproceso; definir ambas métricas antes del cambio.",
                "Plan: predecir reducción de espera entre etapas, ejecutar la prueba en una pequeña serie sintética y anotar el momento del cambio.",
                "Study: comparar el patrón temporal, no solo la media global; conservar puntos desfavorables.",
                "Balancing: si el tiempo baja pero el reproceso aumenta, no declarar éxito basado solo en velocidad.",
                "Act: adaptar, abandonar o ampliar la prueba según el conjunto de medidas y documentar qué condición todavía no fue probada."
            ],
            "interpretation": "Una mejora operacional exige objetivo, predicción, prueba temporal y medidas que detecten efectos no deseados.",
            "limitations": ["Una serie antes–después sintética no demuestra causalidad ni seguridad de una intervención en un laboratorio real."]
        }
    ]
    unit["guided_activities"] = [
        {
            "title": "Actividad guiada: rediseñar el flujo sintético de un laboratorio diagnóstico",
            "instructions": [
                "Trabaja únicamente con el conjunto sintético proporcionado; no uses datos de pacientes, trabajadores ni operaciones privadas de una institución real.",
                "Define la unidad de flujo, entrada, salida y ventana temporal antes de calcular cualquier KPI.",
                "Dibuja el proceso actual incluyendo etapas activas, colas, retrabajos y recursos simulados.",
                "Conserva por separado tiempo de proceso, tiempo de espera, WIP, throughput, demanda y capacidad.",
                "Calcula la capacidad de cada etapa y localiza el cuello de botella en el escenario base y en al menos una perturbación.",
                "Comprueba la Ley de Little solo después de justificar que frontera, unidades, promedios y estabilidad son compatibles.",
                "Modela un reactivo sintético con demanda, lead time, stock de seguridad, punto de reposición y fecha de caducidad.",
                "Formula un objetivo de mejora y selecciona una medida de resultado, una de proceso y una de equilibrio con definición operacional.",
                "Diseña un PDSA sintético y escribe la predicción antes de generar o inspeccionar el escenario posterior al cambio.",
                "Compara escenario base y alternativo, registra efectos favorables y desfavorables y termina con límites de transferencia."
            ],
            "problems": [
                "Identificar la unidad de flujo y justificar por qué no se mezclan muestras, lotes y personas.",
                "Construir un mapa con al menos cinco etapas y dos puntos de espera.",
                "Calcular tiempo de proceso total de una unidad sin incluir esperas.",
                "Calcular tiempo de flujo total incluyendo las esperas suministradas.",
                "Calcular throughput en tres ventanas y explicar por qué no equivale a capacidad.",
                "Calcular WIP medio con la regla de conteo declarada.",
                "Comprobar L=λW y diagnosticar una versión deliberadamente incoherente del conjunto de métricas.",
                "Calcular capacidad de cada etapa y capacidad del proceso secuencial.",
                "Identificar el cuello de botella y predecir dónde se acumulará WIP.",
                "Comparar demanda base, demanda pico y una indisponibilidad de recurso mediante utilización.",
                "Explicar por qué perseguir 100 % de utilización puede aumentar espera bajo variabilidad.",
                "Clasificar existencias sintéticas como suministros, WIP o material en tránsito.",
                "Calcular ROP base y recalcularlo con un lead time adverso.",
                "Detectar un escenario donde más stock de seguridad aumenta riesgo de caducidad.",
                "Definir una medida de resultado con numerador/unidad/ventana cuando corresponda.",
                "Definir una medida de proceso que represente el mecanismo del cambio.",
                "Definir una medida de equilibrio capaz de detectar un efecto no deseado.",
                "Escribir objetivo, predicción, plan de prueba y criterio para adaptar/adoptar/abandonar el cambio.",
                "Construir un gráfico de ejecución sintético y anotar el momento del cambio.",
                "Redactar una conclusión que no se convierta en recomendación de agenda, plantilla, inventario o SOP real."
            ],
            "deliverables": [
                "Mapa de proceso con frontera, unidad de flujo, recursos y colas.",
                "Diccionario de métricas con unidades y definiciones operacionales.",
                "Tabla tiempo de proceso/espera/flujo/WIP/throughput con control de Little.",
                "Tabla de capacidad, cuello de botella y utilización en escenarios base y adverso.",
                "Modelo de inventario con demanda, lead time, SS, ROP y caducidad.",
                "Objetivo y familia de medidas resultado/proceso/equilibrio.",
                "Ficha PDSA con predicción y criterio de decisión previos.",
                "Gráfico temporal anotado con resultados favorables y desfavorables.",
                "Registro de supuestos, sensibilidad y datos pendientes.",
                "Memorando operacional de máximo dos páginas con límites y siguiente prueba."
            ],
            "checking_criteria": [
                "La unidad de flujo y la frontera son constantes en todas las métricas comparadas.",
                "Throughput, capacidad y demanda no se usan como sinónimos.",
                "La Ley de Little conserva unidades y se aplica solo a un escenario justificadamente estable.",
                "El cuello de botella se deriva de capacidades de etapa y se recalcula después del cambio.",
                "La utilización usa una capacidad identificada y no se interpreta como tiempo ocupado individual.",
                "El ROP conserva unidades y distingue demanda de lead time y stock de seguridad.",
                "Caducidad y stock-out aparecen como riesgos contrapuestos en el escenario de inventario.",
                "Las medidas resultado/proceso/equilibrio tienen definiciones operacionales independientes.",
                "La predicción PDSA fue registrada antes del escenario posterior al cambio.",
                "El gráfico conserva la secuencia temporal y no borra puntos desfavorables.",
                "La conclusión distingue aprendizaje local de causalidad y transferencia.",
                "No se presentan datos sintéticos como evidencia de acreditación, dotación, agenda o procedimiento institucional real."
            ]
        }
    ]
    unit["common_errors"] = [
        "Calcular indicadores antes de definir la unidad de flujo y las fronteras del proceso.",
        "Confundir throughput observado con capacidad máxima sostenible.",
        "Contar solo tiempo de proceso y llamar al resultado turnaround time aunque existan esperas.",
        "Aplicar L=λW con fronteras o unidades temporales diferentes.",
        "Usar la Ley de Little durante crecimiento sostenido de cola sin discutir estabilidad.",
        "Mejorar una etapa no limitante y asumir que aumentó la capacidad del proceso.",
        "Interpretar utilización del 100 % como objetivo universal de eficiencia.",
        "Ignorar variabilidad y picos porque la demanda media es menor que la capacidad media.",
        "Confundir WIP de muestras con inventario físico de reactivos o consumibles.",
        "Calcular ROP sin incluir lead time o sin comprobar compatibilidad de unidades.",
        "Aumentar stock de seguridad sin analizar caducidad, almacenamiento o desperdicio.",
        "Declarar mejora porque una media antes–después disminuyó sin medidas de equilibrio ni serie temporal.",
        "Cambiar la definición operacional de una métrica durante el PDSA y comparar como si fuera la misma variable.",
        "Convertir un ejercicio sintético en una recomendación de plantilla, agenda, stock o SOP para un servicio sanitario real."
    ]
    unit["self_assessment"] = [
        {"question": "¿Qué debe definirse antes de calcular turnaround time?", "answer": "La unidad de flujo, el evento de entrada, el evento de salida, la ventana y la regla de inclusión.", "reasoning": "Sin una frontera común dos tiempos con el mismo nombre pueden medir procesos distintos.", "common_error": "Usar cualquier marca temporal disponible sin especificar el intervalo."},
        {"question": "¿Throughput y capacidad son lo mismo?", "answer": "No. Throughput es la tasa de salida observada; capacidad es la tasa máxima sostenible bajo condiciones declaradas.", "reasoning": "La salida puede ser menor que la capacidad por demanda baja o restricciones temporales.", "common_error": "Llamar capacidad al número producido ayer."},
        {"question": "Con λ=12 muestras/h y W=1,5 h, ¿qué L predice Little?", "answer": "18 muestras de WIP medio.", "reasoning": "L=λW=12×1,5 y las horas se cancelan.", "common_error": "Dividir 12 entre 1,5."},
        {"question": "¿Cuándo no debe usarse mecánicamente L=λW?", "answer": "Cuando frontera, unidades o promedios no son coherentes o el sistema no es suficientemente estable para la interpretación propuesta.", "reasoning": "La relación requiere medias pertinentes del mismo sistema.", "common_error": "Aplicarla a una cola que crece sin límite como si estuviera en estado estable."},
        {"question": "Etapas con capacidades 120, 60 y 96 unidades/turno: ¿cuál es la capacidad del proceso secuencial simple?", "answer": "60 unidades/turno y la segunda etapa es el cuello de botella.", "reasoning": "Todas las unidades deben atravesar la etapa de menor capacidad.", "common_error": "Promediar las tres capacidades."},
        {"question": "¿Aumentar C1 de 120 a 240 mejora ese proceso si C2 permanece en 60?", "answer": "No aumenta la capacidad máxima modelada; puede aumentar acumulación antes de C2.", "reasoning": "La restricción sigue siendo la segunda etapa.", "common_error": "Suponer que cualquier inversión local mejora la salida sistémica."},
        {"question": "¿Qué significa u=0,90 en el modelo u=λd/C?", "answer": "Que la demanda media equivale al 90 % de la capacidad de referencia usada; no describe exactamente la ocupación de cada recurso.", "reasoning": "La definición depende del numerador y denominador y no incorpora por sí sola variabilidad.", "common_error": "Interpretarlo como 10 % de tiempo libre garantizado."},
        {"question": "Con d=20 kits/día, L=4 días y SS=30, ¿cuál es el ROP?", "answer": "110 kits.", "reasoning": "ROP=dL+SS=80+30.", "common_error": "Multiplicar también el stock de seguridad por el lead time."},
        {"question": "¿Por qué más stock de seguridad no es siempre mejor?", "answer": "Porque reduce ciertos stock-outs bajo el modelo pero aumenta inventario, espacio, capital, caducidad y desperdicio.", "reasoning": "La decisión tiene riesgos contrapuestos.", "common_error": "Tratar continuidad de suministro como único criterio."},
        {"question": "¿Qué tres tipos de medidas usa IHI para aprender de una mejora?", "answer": "Medidas de resultado, proceso y equilibrio.", "reasoning": "Permiten observar objetivo, mecanismo y efectos no deseados desde perspectivas complementarias.", "common_error": "Usar un único KPI de velocidad."},
        {"question": "¿Un PDSA favorable equivale a implementación?", "answer": "No. Es una prueba orientada al aprendizaje; la implementación requiere evidencia y condiciones adicionales.", "reasoning": "IHI diferencia probar cambios a pequeña escala de hacerlos permanentes y extenderlos.", "common_error": "Convertir el primer ciclo positivo en política definitiva."},
        {"question": "¿Por qué se necesita un gráfico temporal y no solo una media antes–después?", "answer": "Porque la secuencia revela variación, tendencias, cambios de nivel y coincidencia temporal con las pruebas.", "reasoning": "La mejora ocurre en el tiempo y un promedio puede ocultar patrones o puntos adversos.", "common_error": "Eliminar días desfavorables del resumen."},
        {"question": "¿Una reducción sintética de turnaround time autoriza cambiar la agenda o dotación de un laboratorio real?", "answer": "No. El ejercicio demuestra razonamiento operacional en un escenario delimitado, no seguridad, causalidad ni idoneidad institucional.", "reasoning": "Las operaciones reales requieren datos locales, gobernanza, participación, riesgos y requisitos aplicables.", "common_error": "Convertir una simulación académica en SOP o recomendación de gestión real."}
    ]
    unit["biomedical_connections"] = [
        {"topic": "Laboratorios diagnósticos", "connection": "Permite modelar de forma sintética recepción, preparación, análisis y liberación como un flujo con colas, capacidad y calidad, sin utilizar datos de pacientes."},
        {"topic": "Servicios de imagen", "connection": "La distinción demanda-capacidad-throughput ayuda a estudiar escenarios ficticios de slots y cuellos de botella sin recomendar agendas clínicas reales."},
        {"topic": "Mantenimiento de tecnología médica", "connection": "Las órdenes de mantenimiento pueden representarse como unidades de flujo para estudiar WIP, prioridades y capacidad en datos sintéticos."},
        {"topic": "Gestión de reactivos y consumibles", "connection": "Lead time, punto de reposición, stock de seguridad y caducidad permiten razonar sobre continuidad y desperdicio bajo supuestos explícitos."},
        {"topic": "Mejora de calidad", "connection": "PDSA, medidas de resultado/proceso/equilibrio y gráficos temporales conectan cambios operativos con aprendizaje auditable sin confundir mejora con investigación o acreditación."}
    ]
    unit["sources"] = [
        {"title": "A Proof for the Queuing Formula: L = λW", "organization": "INFORMS / Operations Research", "url": "https://pubsonline.informs.org/doi/abs/10.1287/opre.9.3.383", "type": "artículo metodológico primario", "description": "Demostración original de la relación de Little y condiciones sobre promedios y estacionariedad.", "verification_status": "verified_directly"},
        {"title": "The Bottleneck Phenomenon and Its Impact on Process Capacity", "organization": "eCampusOntario Pressbooks", "url": "https://ecampusontario.pressbooks.pub/fundamentalsopsmgmt/chapter/4-9-the-bottleneck-phenomenon-and-its-impact-on-process-capacity/", "type": "libro universitario abierto", "description": "Capacidad de etapas, procesos secuenciales y efecto del cuello de botella sobre la capacidad total.", "verification_status": "verified_directly"},
        {"title": "Inventory Management", "organization": "Seneca Polytechnic Open Textbook Project", "url": "https://pressbooks.senecapolytechnic.ca/operationsmanagementintro/chapter/inventory-management/", "type": "libro universitario abierto", "description": "Inventario, lead time, revisión, punto de reposición y compensaciones entre stock y servicio.", "verification_status": "verified_directly"},
        {"title": "Laboratory quality management system: handbook", "organization": "World Health Organization", "url": "https://www.who.int/publications/i/item/9789241548274", "type": "manual técnico institucional", "description": "Sistema de gestión de calidad de laboratorio, procesos, compras/inventario y mejora de procesos.", "verification_status": "verified_directly"},
        {"title": "ISO 15189:2022 — Medical laboratories — Requirements for quality and competence", "organization": "International Organization for Standardization", "url": "https://www.iso.org/standard/76677.html", "type": "página oficial de norma", "description": "Alcance oficial de los requisitos de calidad y competencia de laboratorios médicos; la unidad no reproduce cláusulas ni afirma conformidad.", "verification_status": "verified_directly"},
        {"title": "Model for Improvement", "organization": "Institute for Healthcare Improvement", "url": "https://www.ihi.org/library/model-for-improvement", "type": "marco institucional de mejora", "description": "Tres preguntas fundamentales y ciclos PDSA para probar, adaptar e implementar cambios.", "verification_status": "verified_directly"},
        {"title": "Model for Improvement: Establishing Measures", "organization": "Institute for Healthcare Improvement", "url": "https://www.ihi.org/library/model-for-improvement/establishing-measures", "type": "guía institucional de medición", "description": "Medidas de resultado, proceso y equilibrio y seguimiento de datos a lo largo del tiempo para mejora.", "verification_status": "verified_directly"},
        {"title": "Run Chart Tool", "organization": "Institute for Healthcare Improvement", "url": "https://www.ihi.org/library/tools/run-chart-tool", "type": "herramienta institucional de mejora", "description": "Uso de gráficos de ejecución para observar desempeño y cambios a lo largo del tiempo.", "verification_status": "verified_directly"},
        {"title": "Laboratory quality manual template", "organization": "World Health Organization", "url": "https://www.who.int/publications/m/item/laboratory-quality-manual", "type": "plantilla técnica institucional", "description": "Ejemplos de políticas y procesos de un sistema de calidad de laboratorio; requiere adaptación al contexto local.", "verification_status": "verified_directly"}
    ]
    unit["editorial_notice"] = (
        "Unidad educativa en revisión interna. Esta curación no constituye revisión disciplinar externa, consultoría de operaciones, "
        "procedimiento operativo estándar, recomendación de plantilla o agenda clínica ni evidencia de acreditación ISO 15189. Todas las "
        "actividades usan procesos, muestras, inventarios y series temporales sintéticos; no requieren datos personales ni información operativa "
        "confidencial. Las mejoras propuestas son hipótesis de aprendizaje que deben probarse y gobernarse localmente antes de cualquier aplicación real."
    )
    dump(unit)
    text = SOURCE.read_text(encoding="utf-8")
    assert GENERIC.casefold() not in text.casefold()
    assert SOURCE.read_bytes() == MIRROR.read_bytes()
    assert len(unit["worked_examples"]) >= 5
    assert len(unit["glossary"]) >= 20
    assert len(unit["common_errors"]) >= 12
    assert len(unit["self_assessment"]) >= 12
    assert len(unit["sources"]) >= 8
    assert all(source["verification_status"] == "verified_directly" for source in unit["sources"])
    print("[ok] Economía y Gestión de Empresas U3 curada y espejo sincronizado")


if __name__ == "__main__":
    main()
