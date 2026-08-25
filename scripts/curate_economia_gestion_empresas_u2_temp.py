#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-02.json"
TEST = ROOT / "tests" / "test_economia_gestion_empresas_unit_02_curated.py"
GENERIC = "Concepto de la unidad que debe definirse mediante entidades observables"

unit = {
  "schema_version": "2.0",
  "subject_id": "economia-gestion-empresas",
  "area_id": "gestion-etica-comunicacion",
  "unit": 2,
  "slug": "contabilidad-y-finanzas",
  "title": "Contabilidad y finanzas",
  "status": "review",
  "purpose": "Construir e interpretar un modelo financiero básico y reproducible de un proyecto biomédico sintético mediante estados financieros, base de devengo, estructura de costes, margen de contribución, punto de equilibrio, flujo de caja, capital de trabajo, liquidez y presupuesto, distinguiendo resultado contable de efectivo y sostenibilidad financiera de valor sanitario, sin presentar el ejercicio como estados IFRS, asesoría contable, decisión de inversión o evaluación económica sanitaria formal.",
  "learning_objectives": [
    "Relacionar estado de situación financiera, estado de resultados y estado de flujos de efectivo mediante la ecuación contable y distinguir magnitudes de fecha de magnitudes de periodo.",
    "Explicar la diferencia entre base de devengo y movimientos de efectivo y reconstruir por qué beneficio contable y variación de caja pueden divergir.",
    "Clasificar costes directos e indirectos y fijos y variables para una pregunta de gestión concreta, declarando objeto de coste, periodo y rango relevante.",
    "Calcular margen de contribución y punto de equilibrio en un escenario sintético y evaluar cómo cambian ante precio, coste variable, coste fijo o capacidad.",
    "Clasificar flujos de caja en actividades operativas, de inversión y financiación y calcular capital de trabajo y razón corriente sin convertir una razón aislada en diagnóstico financiero completo.",
    "Preparar un presupuesto y un análisis de sensibilidad de sostenibilidad financiera para un proyecto biomédico ficticio, documentando supuestos, variaciones, restricciones y límites y reservando la evaluación económica de resultados sanitarios para U5."
  ],
  "theory_sections": [
    {
      "heading": "1. Estados financieros, ecuación contable y base de devengo",
      "paragraphs": [
        "La contabilidad financiera organiza transacciones y otros hechos en representaciones que permiten describir posición financiera y desempeño. Una lectura mínima necesita distinguir magnitudes de fecha y de periodo. El estado de situación financiera resume activos, pasivos y patrimonio en una fecha concreta; el estado de resultados resume ingresos y gastos durante un periodo; el estado de flujos de efectivo explica entradas y salidas de efectivo durante un periodo. Estas piezas se conectan, pero no son intercambiables. Un proyecto puede mostrar resultado positivo y, al mismo tiempo, afrontar una tensión de caja si cobra tarde o realiza una inversión relevante.",
        "La ecuación activos = pasivos + patrimonio expresa que los recursos reconocidos tienen fuentes o derechos asociados. Un activo no significa simplemente 'algo valioso' ni un pasivo simplemente 'un gasto'. El Marco Conceptual de IFRS define elementos y criterios de reconocimiento para información financiera de propósito general. En esta unidad se usan versiones educativas simplificadas para razonar sobre relaciones; no se afirma que una hoja de cálculo del curso cumpla IFRS ni que una clasificación sea suficiente para preparar estados financieros reglamentarios.",
        "La base de devengo reconoce los efectos de transacciones cuando ocurren según las reglas contables aplicables, aunque el efectivo se cobre o pague en otro momento. Por eso pueden existir cuentas por cobrar, cuentas por pagar, depreciación y otros ajustes que separan resultado contable de caja. Un ingreso registrado sin cobro inmediato puede aumentar el resultado antes de aumentar efectivo; una depreciación reduce resultado sin representar una salida de caja del mismo periodo. Confundir ambos planos puede ocultar problemas de liquidez o atribuir a caja movimientos que pertenecen al reconocimiento contable.",
        "A agosto de 2026 existe además una transición normativa relevante: IAS 1 continúa siendo la referencia de presentación para entidades que aún no aplican anticipadamente IFRS 18, mientras IFRS 18 será obligatoria para periodos anuales que comiencen el 1 de enero de 2027 o después y permite aplicación anticipada. Esta fecha debe declararse cuando se use la terminología IFRS. La unidad enseña estructura conceptual y lectura, no preparación reglamentaria; una aplicación real debe verificar el marco contable, jurisdicción, periodo y políticas vigentes.",
        "La utilidad de los estados aparece al conectarlos mediante una cadena de transacciones. Comprar un equipo al contado reduce efectivo y aumenta otro activo; financiarlo con deuda aumenta activo y pasivo; prestar un servicio a crédito puede reconocer ingreso y una cuenta por cobrar antes del cobro. Ninguna transacción debe interpretarse con una sola cifra. El método reproducible registra fecha, cuenta o categoría afectada, signo, documento o supuesto del caso y efecto sobre posición, resultado y efectivo por separado."
      ],
      "equations": [
        {"latex": "A=L+E", "meaning": "Ecuación contable simplificada: los activos se financian mediante pasivos y patrimonio; sirve como control de consistencia, no como estado financiero completo.", "variables": {"A": "activos", "L": "pasivos", "E": "patrimonio"}}
      ],
      "key_points": [
        "Situación financiera es una fotografía a una fecha; resultados y flujos describen un periodo.",
        "Resultado contable y efectivo pueden divergir por devengo, crédito, inversión y partidas no monetarias.",
        "La ecuación contable es un control estructural, no una medida de solvencia, valor o calidad de gestión.",
        "En 2026 debe distinguirse IAS 1 de la transición a IFRS 18 efectiva obligatoriamente desde periodos iniciados el 1 de enero de 2027."
      ]
    },
    {
      "heading": "2. Costes para decisiones de gestión y punto de equilibrio",
      "paragraphs": [
        "Una clasificación de costes solo es útil si declara para qué decisión se construye. El coste directo puede rastrearse de manera económicamente razonable a un objeto de coste definido —por ejemplo, una prueba, una sesión o un proyecto— mientras un coste indirecto necesita una regla de asignación. Esta frontera depende del objeto y del sistema de información: un técnico puede ser directo para un proyecto dedicado e indirecto para una cartera de servicios. Presentar una asignación como si fuera una medición física exacta oculta el juicio incorporado en la regla elegida.",
        "La distinción fijo-variable responde al comportamiento frente a un nivel de actividad y dentro de un rango relevante. Un coste fijo permanece aproximadamente constante en total dentro de ese rango, mientras un coste variable cambia con el volumen según la relación asumida. Ninguna etiqueta es eterna. Al superar capacidad, un coste fijo puede crecer por escalones; descuentos, horas extra o restricciones pueden romper linealidad. Por eso el análisis coste-volumen-resultados debe declarar periodo, capacidad y rango antes de extrapolar.",
        "El margen de contribución unitario es precio o ingreso unitario menos coste variable unitario bajo la convención del modelo. Indica cuánto aporta cada unidad adicional a cubrir costes fijos y, después de cubrirlos, al resultado operativo simplificado. No es margen bruto contable universal ni beneficio neto. En servicios biomédicos ficticios, la unidad también debe definirse —muestra, sesión, mantenimiento o contrato— porque mezclar productos con consumos diferentes puede invalidar un punto de equilibrio único.",
        "El punto de equilibrio en unidades divide costes fijos por margen de contribución unitario cuando se cumplen los supuestos de linealidad, precio y coste variable unitario estables y mezcla de servicios definida. El cálculo responde cuántas unidades necesita el modelo para que ingresos y costes considerados sean iguales; no demuestra que exista demanda suficiente, capacidad clínica, reembolso, seguridad, valor sanitario ni permiso para operar. Si el punto de equilibrio excede la capacidad física, esa incompatibilidad es un resultado importante y obliga a replantear el modelo.",
        "La sensibilidad evita tratar el punto de equilibrio como un número exacto. Variar precio, volumen máximo, coste variable y coste fijo dentro de rangos trazados muestra qué supuesto domina la conclusión. Una opción puede parecer sostenible solo porque se asumió ocupación alta o cobro inmediato. La entrega debe conservar escenarios desfavorables además del escenario nominal y distinguir datos observados de supuestos. El análisis formal de coste-efectividad y consecuencias sanitarias se reserva para U5."
      ],
      "equations": [
        {"latex": "CM_u=P-V_u", "meaning": "Margen de contribución unitario simplificado.", "variables": {"CM_u": "margen de contribución por unidad", "P": "ingreso o precio por unidad definido en el caso", "V_u": "coste variable por unidad"}},
        {"latex": "Q_{BE}=\\frac{F}{P-V_u}", "meaning": "Punto de equilibrio en unidades bajo supuestos de coste-volumen-resultados y margen de contribución positivo.", "variables": {"Q_BE": "unidades de equilibrio", "F": "costes fijos del periodo", "P": "ingreso por unidad", "V_u": "coste variable por unidad"}}
      ],
      "key_points": [
        "Directo/indirecto depende del objeto de coste y fijo/variable depende del comportamiento y rango relevante.",
        "Una regla de asignación de costes indirectos es una decisión metodológica que debe documentarse.",
        "Margen de contribución y punto de equilibrio son herramientas de gestión simplificadas, no medidas de valor sanitario.",
        "Capacidad, mezcla de servicios y sensibilidad deben comprobarse antes de interpretar sostenibilidad."
      ]
    },
    {
      "heading": "3. Flujo de caja, capital de trabajo y liquidez",
      "paragraphs": [
        "El estado de flujos de efectivo responde de dónde provino y en qué se utilizó el efectivo durante un periodo. IAS 7 clasifica flujos en actividades operativas, de inversión y de financiación. En términos pedagógicos, operaciones representan la actividad principal generadora de ingresos y otros flujos no clasificados como inversión o financiación; inversión incluye adquisición o disposición de activos de largo plazo; financiación cambia la composición de aportes de capital y préstamos. Clasificar correctamente ayuda a distinguir una operación que genera caja de una entidad que se sostiene temporalmente mediante nueva deuda.",
        "El efectivo final puede reconstruirse desde efectivo inicial más flujos netos operativos, de inversión y financiación. El signo y la clasificación importan. Comprar un equipo al contado suele producir una salida de inversión; recibir un préstamo genera una entrada de financiación; cobrar servicios o pagar salarios forma parte del flujo operativo bajo el esquema simplificado del caso. Una entrada de financiación puede mejorar caja sin convertir una operación deficitaria en rentable, y una inversión grande puede reducir caja aun cuando la actividad operativa sea positiva.",
        "El capital de trabajo neto se aproxima como activos corrientes menos pasivos corrientes y ofrece una vista de recursos de corto plazo frente a obligaciones de corto plazo. La razón corriente expresa activos corrientes divididos por pasivos corrientes. Ambas medidas son fotografías contables: no garantizan caja futura ni consideran automáticamente la calidad o convertibilidad de cada activo. Un inventario obsoleto o una cuenta por cobrar de cobro incierto puede hacer que una razón aparente más holgura de la que existe en términos de efectivo disponible.",
        "Para un proyecto biomédico ficticio, la liquidez se estudia mediante un calendario mensual de cobros y pagos. Dos escenarios con el mismo resultado anual pueden tener necesidades de financiación distintas si uno cobra a 90 días y paga proveedores al contado. El saldo mínimo de caja y el mes en que aparece un déficit son salidas operativas útiles. No deben ocultarse con promedios anuales. Si la simulación permite deuda adicional, debe registrarse por separado para no confundir financiación con generación de efectivo del servicio.",
        "Las métricas de liquidez se interpretan en conjunto con contexto, tendencias y composición. Una razón corriente mayor que uno no es una garantía universal de solvencia; una razón menor que uno tampoco demuestra por sí sola insolvencia. El horizonte, estacionalidad, acceso a financiación, vencimientos y naturaleza de activos corrientes importan. Esta unidad exige formular preguntas de seguimiento en lugar de etiquetar una organización como sana o inviable a partir de un único cociente."
      ],
      "equations": [
        {"latex": "Cash_{end}=Cash_{begin}+CF_O+CF_I+CF_F", "meaning": "Reconciliación simplificada de la variación de efectivo por actividades operativas, de inversión y financiación.", "variables": {"Cash_end": "efectivo final", "Cash_begin": "efectivo inicial", "CF_O": "flujo neto operativo", "CF_I": "flujo neto de inversión", "CF_F": "flujo neto de financiación"}},
        {"latex": "NWC=CA-CL", "meaning": "Capital de trabajo neto simplificado.", "variables": {"NWC": "capital de trabajo neto", "CA": "activos corrientes", "CL": "pasivos corrientes"}},
        {"latex": "CR=\\frac{CA}{CL}", "meaning": "Razón corriente; indicador puntual de liquidez que requiere interpretar composición y contexto.", "variables": {"CR": "razón corriente", "CA": "activos corrientes", "CL": "pasivos corrientes"}}
      ],
      "key_points": [
        "Flujos operativos, de inversión y financiación responden a fuentes distintas de cambios en efectivo.",
        "Beneficio y caja no son equivalentes; deuda o aportes pueden aumentar caja sin mejorar el desempeño operativo.",
        "Capital de trabajo y razón corriente son indicadores de corto plazo y no diagnósticos completos de solvencia.",
        "Un calendario mensual revela déficits de caja que un total anual puede ocultar."
      ]
    },
    {
      "heading": "4. Presupuesto, variaciones y sostenibilidad financiera de un proyecto biomédico",
      "paragraphs": [
        "Un presupuesto transforma supuestos operativos en una expectativa cuantificada para un periodo. El presupuesto operativo organiza volumen, ingresos y gastos asociados a la actividad; el presupuesto de caja organiza cuándo se espera cobrar y pagar. Un presupuesto estático usa un nivel previsto, mientras uno flexible ajusta partidas variables al nivel real de actividad. Comparar un gasto real contra un presupuesto estático sin corregir una diferencia importante de volumen puede atribuir a mala gestión lo que en realidad corresponde a más o menos actividad.",
        "Una variación presupuestaria necesita una convención de signo explícita. Para esta unidad se define variación = real − presupuestado; por tanto, una variación positiva en gasto significa gasto superior al plan, mientras una variación positiva en ingreso significa ingreso superior al plan. Llamar favorable o desfavorable a una cifra requiere saber de qué partida se trata y por qué cambió. Dividir la variación en volumen, precio o coste unitario puede ser más informativo que un total agregado.",
        "La sostenibilidad financiera básica del proyecto ficticio se analiza combinando resultado operativo, punto de equilibrio, caja, capital de trabajo, capacidad y escenarios. Ninguna métrica aislada decide. Un servicio puede alcanzar punto de equilibrio anual y aun así quedarse sin caja en el mes cuatro; otro puede tener caja positiva gracias a un préstamo pero margen de contribución negativo. La coherencia exige que supuestos de volumen sean compatibles con capacidad, calendario de cobros y costes del mismo modelo.",
        "El análisis de escenarios define al menos un caso nominal y uno adverso con cambios documentados de volumen, retraso de cobro, costes o capacidad. El objetivo no es elegir el escenario más conveniente, sino localizar qué variable amenaza primero la continuidad financiera y qué dato real sería necesario medir. La incertidumbre puede presentarse mediante rangos y sensibilidad; no se añade una probabilidad inventada para producir falsa precisión. Un proyecto robusto conserva suficiente margen operativo y de caja bajo perturbaciones plausibles del caso.",
        "El producto final es un informe financiero educativo y auditable. Debe contener supuestos, miniestados vinculados, estructura de costes, punto de equilibrio, flujo mensual, liquidez, presupuesto, variaciones y sensibilidad, además de una sección 'qué no sabemos'. No es una auditoría, estado IFRS, valoración de empresa ni recomendación de inversión. Tampoco determina si una tecnología mejora salud o es coste-efectiva: esas preguntas requieren resultados sanitarios y métodos de evaluación económica que se desarrollan en U5."
      ],
      "equations": [
        {"latex": "Var=Actual-Budget", "meaning": "Convención de variación usada en la unidad; su interpretación favorable o desfavorable depende de si la partida es ingreso, gasto u otra magnitud.", "variables": {"Var": "variación", "Actual": "valor observado del escenario", "Budget": "valor presupuestado"}}
      ],
      "key_points": [
        "Presupuesto operativo y presupuesto de caja responden a preguntas distintas y deben compartir supuestos coherentes.",
        "Una variación necesita convención de signo, nivel de actividad y explicación causal antes de etiquetarse como favorable o desfavorable.",
        "Sostenibilidad financiera combina resultado, caja, liquidez, capacidad y sensibilidad; ninguna cifra aislada decide.",
        "U2 no sustituye auditoría, cumplimiento IFRS, valoración financiera ni evaluación económica sanitaria de U5."
      ]
    }
  ],
  "glossary": [
    {"term": "activo", "definition": "Recurso económico presente controlado por una entidad como resultado de sucesos pasados, usado aquí según el marco conceptual contable y no como sinónimo de cualquier objeto valioso."},
    {"term": "pasivo", "definition": "Obligación presente de transferir un recurso económico como resultado de sucesos pasados, según el marco conceptual aplicable."},
    {"term": "patrimonio", "definition": "Interés residual en los activos después de deducir pasivos dentro de la ecuación contable simplificada."},
    {"term": "estado de situación financiera", "definition": "Estado que presenta activos, pasivos y patrimonio en una fecha determinada."},
    {"term": "estado de resultados", "definition": "Estado que presenta ingresos y gastos y el desempeño contable durante un periodo bajo el marco aplicable."},
    {"term": "estado de flujos de efectivo", "definition": "Estado que presenta entradas y salidas de efectivo y equivalentes y las clasifica por actividades según las reglas aplicables."},
    {"term": "base de devengo", "definition": "Reconocimiento de efectos económicos cuando ocurren conforme a las reglas contables, no únicamente cuando se cobra o paga efectivo."},
    {"term": "cuenta por cobrar", "definition": "Derecho reconocido a recibir efectivo u otra contraprestación de un tercero; no equivale a efectivo disponible."},
    {"term": "cuenta por pagar", "definition": "Obligación corriente derivada de bienes o servicios recibidos y pendiente de pago."},
    {"term": "depreciación", "definition": "Asignación sistemática del importe depreciable de un activo a lo largo de su vida útil; es un gasto contable que no implica necesariamente salida de efectivo en el mismo periodo."},
    {"term": "coste directo", "definition": "Coste trazable de manera económicamente razonable al objeto de coste definido."},
    {"term": "coste indirecto", "definition": "Coste que requiere una base o regla de asignación para atribuirse al objeto de coste."},
    {"term": "coste fijo", "definition": "Coste que permanece aproximadamente constante en total dentro de un periodo y rango relevante definidos."},
    {"term": "coste variable", "definition": "Coste cuyo total cambia con el nivel de actividad según la relación asumida dentro del rango relevante."},
    {"term": "rango relevante", "definition": "Intervalo de actividad dentro del cual se consideran razonables los supuestos de comportamiento de costes y capacidad."},
    {"term": "margen de contribución", "definition": "Diferencia entre ingreso unitario y coste variable unitario en un modelo coste-volumen-resultados simplificado."},
    {"term": "punto de equilibrio", "definition": "Nivel de actividad en el que ingresos y costes incluidos en el modelo son iguales bajo los supuestos declarados."},
    {"term": "flujo operativo", "definition": "Flujo de efectivo asociado a las actividades principales generadoras de ingresos y otras actividades no clasificadas como inversión o financiación, según el marco usado."},
    {"term": "flujo de inversión", "definition": "Flujo de efectivo relacionado con adquisición o disposición de activos de largo plazo y otras inversiones según la clasificación aplicable."},
    {"term": "flujo de financiación", "definition": "Flujo que cambia la composición de patrimonio aportado y endeudamiento de la entidad."},
    {"term": "capital de trabajo neto", "definition": "Diferencia simplificada entre activos corrientes y pasivos corrientes."},
    {"term": "razón corriente", "definition": "Cociente entre activos corrientes y pasivos corrientes usado como indicador puntual de liquidez."},
    {"term": "presupuesto flexible", "definition": "Presupuesto que ajusta partidas dependientes del volumen al nivel real o alternativo de actividad."},
    {"term": "variación presupuestaria", "definition": "Diferencia entre resultado real o simulado y presupuesto bajo una convención de signo explícita."},
    {"term": "liquidez", "definition": "Capacidad de atender necesidades de efectivo de corto plazo, evaluada con caja, activos convertibles, obligaciones, calendario y contexto."}
  ],
  "worked_examples": [
    {
      "title": "Un equipo financiado con efectivo y deuda",
      "scenario": "Un proyecto ficticio compra un analizador por 60 000 unidades monetarias: paga 20 000 al contado y financia 40 000 con un préstamo. Se ignoran impuestos e intereses en este paso.",
      "reasoning_steps": [
        "Antes: efectivo 80 000, otros activos 0, pasivos 0 y patrimonio 80 000.",
        "La compra reduce efectivo en 20 000 y aumenta equipo en 60 000; activos netos aumentan 40 000.",
        "El préstamo aumenta pasivos en 40 000.",
        "Después: efectivo 60 000 + equipo 60 000 = activos 120 000; pasivos 40 000 + patrimonio 80 000 = 120 000."
      ],
      "interpretation": "La ecuación contable permanece equilibrada y muestra que parte del activo se financió con deuda; la compra no implica por sí sola un gasto de 60 000 en el resultado del mismo periodo.",
      "limitations": ["Caso educativo sin reglas detalladas de reconocimiento, depreciación, intereses o impuestos.", "No constituye un asiento ni estado IFRS real."]
    },
    {
      "title": "Beneficio positivo con caja retrasada",
      "scenario": "Un servicio ficticio reconoce ingresos de 30 000 por servicios a crédito y gastos en efectivo de 18 000 durante el mes; ningún cliente paga aún dentro del periodo y se omiten otros ajustes.",
      "reasoning_steps": [
        "Resultado simplificado por devengo: 30 000 − 18 000 = 12 000.",
        "Cobros del periodo: 0; pagos operativos: 18 000.",
        "Flujo operativo de caja simplificado: −18 000, pese al resultado positivo.",
        "Registrar una cuenta por cobrar de 30 000 explica parte de la divergencia entre resultado y caja."
      ],
      "interpretation": "Rentabilidad contable y liquidez responden a preguntas diferentes; el calendario de cobro puede crear tensión de caja aun con resultado positivo.",
      "limitations": ["No incluye impuestos, deterioro de cuentas por cobrar ni otras partidas de devengo.", "No predice si la cuenta será finalmente cobrada."]
    },
    {
      "title": "Punto de equilibrio de un servicio técnico sintético",
      "scenario": "Un servicio ficticio cobra 250 por intervención, incurre en 100 de coste variable por intervención y tiene 18 000 de costes fijos mensuales; capacidad máxima 140 intervenciones.",
      "reasoning_steps": [
        "Margen de contribución unitario = 250 − 100 = 150.",
        "Punto de equilibrio = 18 000 / 150 = 120 intervenciones.",
        "Comparar con capacidad: 120 ≤ 140, por lo que el punto es físicamente alcanzable en el escenario.",
        "Queda un margen de capacidad de 20 intervenciones, pero falta comprobar demanda y calendario de cobro."
      ],
      "interpretation": "El modelo cubre los costes considerados a 120 intervenciones; no demuestra demanda, valor sanitario ni sostenibilidad de caja.",
      "limitations": ["Supone precio y coste variable constantes y costes fijos estables dentro del rango.", "No incluye mezcla de servicios ni retrasos de cobro."]
    },
    {
      "title": "Clasificación de flujos: operar, invertir o financiar",
      "scenario": "En un mes sintético se cobran 50 000 por servicios, se pagan 32 000 en gastos operativos, se compra equipo por 25 000 y se recibe un préstamo de 20 000.",
      "reasoning_steps": [
        "Flujo operativo neto simplificado: 50 000 − 32 000 = +18 000.",
        "Flujo de inversión: −25 000 por compra de equipo.",
        "Flujo de financiación: +20 000 por préstamo.",
        "Cambio neto de caja = 18 000 − 25 000 + 20 000 = +13 000."
      ],
      "interpretation": "La caja aumenta 13 000, pero 20 000 provienen de financiación; separar categorías evita atribuir toda la mejora a operaciones.",
      "limitations": ["Clasificación simplificada para aprendizaje; una aplicación real debe seguir el estándar y hechos contractuales aplicables.", "No incluye intereses ni impuestos."]
    },
    {
      "title": "Liquidez: razón corriente y composición",
      "scenario": "Un proyecto ficticio tiene activos corrientes de 90 000, de los cuales 55 000 son cuentas por cobrar; pasivos corrientes de 60 000 y efectivo de solo 10 000.",
      "reasoning_steps": [
        "Capital de trabajo neto = 90 000 − 60 000 = 30 000.",
        "Razón corriente = 90 000 / 60 000 = 1,5.",
        "La razón parece superior a uno, pero más de la mitad de activos corrientes son cuentas por cobrar.",
        "Preguntar calendario y cobrabilidad antes de concluir que existen 30 000 disponibles para pagos inmediatos."
      ],
      "interpretation": "Los indicadores sugieren cobertura contable de corto plazo, pero la composición puede limitar la liquidez inmediata.",
      "limitations": ["No incluye vencimientos exactos, calidad crediticia ni líneas de financiación.", "Una razón aislada no diagnostica solvencia."]
    },
    {
      "title": "Presupuesto flexible frente a variación de volumen",
      "scenario": "Se presupuestaron 100 sesiones con coste variable de 40 por sesión y costes fijos de 6 000. Finalmente se realizan 120 sesiones y el gasto total real es 11 100.",
      "reasoning_steps": [
        "Presupuesto estático = 6 000 + 100×40 = 10 000.",
        "Presupuesto flexible a 120 sesiones = 6 000 + 120×40 = 10 800.",
        "Variación frente a presupuesto estático = 11 100 − 10 000 = +1 100; mezcla efecto volumen y otros efectos.",
        "Variación frente a presupuesto flexible = 11 100 − 10 800 = +300, que aísla mejor el exceso respecto al coste esperado al volumen real."
      ],
      "interpretation": "Comparar con un presupuesto flexible evita atribuir al control de costes una diferencia causada principalmente por mayor actividad.",
      "limitations": ["Supone linealidad y coste fijo estable en 120 sesiones.", "No explica por sí solo la causa de los 300 restantes."]
    }
  ],
  "guided_activities": [
    {
      "title": "Actividad guiada: expediente financiero sintético de un servicio biomédico",
      "instructions": [
        "Usa exclusivamente la empresa y las transacciones ficticias entregadas; no incorpores estados, precios, contratos ni datos confidenciales de una organización real.",
        "Define periodo, moneda/unidad, objeto de coste, unidad de actividad y convención de signos antes de calcular.",
        "Registra cada transacción en una tabla que separe efecto sobre activos, pasivos, patrimonio, resultado y efectivo.",
        "Construye primero el escenario basal y después un escenario adverso; no ajustes supuestos para forzar una conclusión favorable.",
        "Conserva fórmulas o celdas de cálculo y un diccionario de variables para que otra persona pueda reproducir el expediente.",
        "Marca qué salidas son contables, cuáles son de caja y cuáles son inferencias de gestión; no uses ninguna como sustituto de resultados sanitarios.",
        "Cierra con una recomendación condicionada al caso y una sección de límites, datos faltantes y decisiones reservadas para U5 o para profesionales competentes."
      ],
      "problems": [
        "Verifica la ecuación contable inicial y final después de cinco transacciones sintéticas.",
        "Clasifica cada transacción por efecto en estado de situación, resultado y flujo de caja y explica al menos dos divergencias devengo-caja.",
        "Clasifica diez costes como directos/indirectos respecto del objeto elegido y justifica dos casos ambiguos.",
        "Clasifica esos costes como fijos/variables dentro de un rango relevante y señala al menos un coste escalonado o no lineal.",
        "Calcula margen de contribución y punto de equilibrio del servicio principal y compáralo con capacidad máxima.",
        "Recalcula el punto de equilibrio tras un aumento del 15 % en coste variable y una caída del 10 % en ingreso unitario.",
        "Clasifica los flujos del trimestre en operación, inversión y financiación y reconcilia efectivo inicial y final.",
        "Construye un calendario mensual de caja e identifica el saldo mínimo y el primer mes con déficit, si existe.",
        "Calcula capital de trabajo neto y razón corriente y evalúa la composición de activos corrientes antes de interpretarlos.",
        "Prepara un presupuesto estático y uno flexible para el nivel real de actividad y calcula variaciones bajo la convención real − presupuestado.",
        "Diseña un escenario adverso de retraso de cobro o menor volumen y determina qué variable cambia primero la sostenibilidad financiera.",
        "Explica por qué un resultado operativo positivo no prueba liquidez y por qué una caja positiva financiada con deuda no prueba rentabilidad.",
        "Enumera qué preguntas sobre valor sanitario, coste-efectividad o decisión de inversión quedan fuera de U2 y deben revalidarse en U5 o con especialistas.",
        "Redacta un resumen ejecutivo de máximo 180 palabras con resultado, caja, punto de equilibrio, liquidez, sensibilidad y límites del caso."
      ],
      "deliverables": [
        "Libro de transacciones sintéticas con ecuación contable y efectos por estado.",
        "Miniestado de situación financiera y miniestado de resultados del periodo con supuestos explícitos.",
        "Tabla de costes con objeto, clasificación, regla de asignación y rango relevante.",
        "Hoja de margen de contribución, punto de equilibrio, capacidad y sensibilidad.",
        "Estado de flujos simplificado y calendario mensual de caja con reconciliación.",
        "Cálculo comentado de capital de trabajo, razón corriente y composición de activos corrientes.",
        "Presupuesto estático/flexible con variaciones y escenario adverso.",
        "Resumen ejecutivo y registro final de límites, datos faltantes y preguntas reservadas a U5."
      ],
      "checking_criteria": [
        "La ecuación contable cuadra antes y después de las transacciones.",
        "Resultado y efectivo se mantienen separados y las divergencias se explican.",
        "Las clasificaciones de costes declaran objeto, periodo y rango relevante.",
        "El punto de equilibrio usa margen de contribución positivo y se contrasta con capacidad.",
        "Los flujos operativos, de inversión y financiación reconcilian con el cambio de caja.",
        "Liquidez se interpreta con composición y vencimientos, no solo con una razón.",
        "Presupuesto estático y flexible no se confunden y la convención de variación está escrita.",
        "Existe al menos un escenario adverso y se conserva aunque debilite la conclusión.",
        "Toda cifra está en unidades coherentes y procede del caso o está marcada como supuesto.",
        "La entrega no afirma cumplimiento IFRS, auditoría, solvencia, inversión óptima ni coste-efectividad sanitaria.",
        "El handoff hacia U5 identifica explícitamente qué resultados sanitarios y métodos económicos aún faltan."
      ]
    }
  ],
  "common_errors": [
    {"error": "Tratar activos como ingresos o pasivos como gastos.", "correction": "Separar elementos de posición financiera de ingresos/gastos del periodo y seguir el efecto de cada transacción."},
    {"error": "Asumir que beneficio positivo implica aumento de caja.", "correction": "Reconstruir cobros, pagos, crédito, inversión, financiación y partidas no monetarias."},
    {"error": "Llamar estado IFRS a una hoja educativa simplificada.", "correction": "Presentarla como modelo didáctico y verificar estándares, jurisdicción, periodo y requisitos completos antes de cualquier afirmación de cumplimiento."},
    {"error": "Clasificar un coste como directo o indirecto sin declarar objeto de coste.", "correction": "Definir primero servicio, proyecto, unidad o centro al que se desea atribuir el coste."},
    {"error": "Suponer que fijo y variable son propiedades permanentes.", "correction": "Declarar periodo y rango relevante y comprobar escalones de capacidad o no linealidades."},
    {"error": "Calcular punto de equilibrio sin verificar que el margen de contribución sea positivo o que exista capacidad suficiente.", "correction": "Validar denominador, unidades, rango y capacidad antes de interpretar Q_BE."},
    {"error": "Contar un préstamo como ingreso operativo.", "correction": "Separar financiación de operaciones; caja adicional no equivale a ingreso ni rentabilidad operativa."},
    {"error": "Interpretar razón corriente >1 como garantía de liquidez.", "correction": "Examinar composición, cobrabilidad, inventario, vencimientos, estacionalidad y calendario de caja."},
    {"error": "Comparar gasto real con presupuesto estático cuando cambió mucho el volumen.", "correction": "Construir un presupuesto flexible al volumen real antes de atribuir la variación a eficiencia o control."},
    {"error": "Usar sostenibilidad financiera como sinónimo de valor sanitario o coste-efectividad.", "correction": "Mantener resultados de salud y evaluación económica formal fuera de U2 y tratarlos en U5 con métodos y evidencia apropiados."}
  ],
  "self_assessment": [
    {"question": "¿Qué diferencia temporal básica existe entre estado de situación financiera y estado de resultados?", "answer": "El primero presenta posición en una fecha; el segundo presenta ingresos y gastos durante un periodo.", "reasoning": "Una fotografía de saldos no debe confundirse con flujos o desempeño acumulado durante un intervalo.", "common_error": "Describir ambos como resúmenes del mismo tipo de periodo."},
    {"question": "¿Por qué A=L+E no demuestra que una entidad sea solvente?", "answer": "Porque es una identidad estructural contable; no informa por sí sola vencimientos, liquidez, calidad de activos, flujos futuros ni capacidad de pago.", "reasoning": "La ecuación puede cuadrar tanto en una entidad saludable como en una con problemas financieros.", "common_error": "Interpretar igualdad contable como señal de buen desempeño."},
    {"question": "¿Puede existir ingreso reconocido sin entrada de caja en el mismo periodo?", "answer": "Sí, por ejemplo una venta o servicio a crédito bajo base de devengo puede generar una cuenta por cobrar antes del cobro.", "reasoning": "Devengo y caja usan momentos de reconocimiento distintos.", "common_error": "Registrar cualquier ingreso como efectivo recibido."},
    {"question": "¿Un coste es siempre directo o indirecto?", "answer": "No. La clasificación depende del objeto de coste y de si puede rastrearse razonablemente a ese objeto.", "reasoning": "Cambiar de proyecto a cartera puede cambiar la trazabilidad del mismo recurso.", "common_error": "Memorizar una etiqueta sin definir el objeto."},
    {"question": "Con P=200, V_u=80 y F=12 000, ¿cuál es Q_BE?", "answer": "100 unidades.", "reasoning": "CM_u=120 y Q_BE=12 000/120=100, siempre que se cumplan supuestos y capacidad.", "common_error": "Dividir F por P o ignorar el coste variable."},
    {"question": "¿Qué ocurre si P−V_u≤0?", "answer": "El modelo no tiene un punto de equilibrio positivo mediante aumento de unidades bajo esos supuestos; cada unidad no contribuye a cubrir costes fijos.", "reasoning": "El denominador del cálculo debe ser positivo para interpretar Q_BE de forma habitual.", "common_error": "Reportar un número negativo de unidades como solución válida."},
    {"question": "¿Cómo se clasifica normalmente la compra al contado de equipo de largo plazo en el estado de flujos?", "answer": "Como salida de actividad de inversión bajo el marco simplificado de IAS 7.", "reasoning": "La adquisición de activos de largo plazo se separa de operación y financiación.", "common_error": "Clasificarla como gasto operativo solo porque sale efectivo."},
    {"question": "Activos corrientes 75 000 y pasivos corrientes 50 000: ¿capital de trabajo y razón corriente?", "answer": "NWC=25 000 y CR=1,5.", "reasoning": "NWC=CA−CL y CR=CA/CL; aún debe evaluarse la composición de activos y vencimientos.", "common_error": "Concluir automáticamente que existe efectivo libre de 25 000."},
    {"question": "¿Por qué usar presupuesto flexible cuando el volumen real difiere del plan?", "answer": "Porque ajusta los costes dependientes de actividad y permite separar mejor efecto volumen de otras variaciones.", "reasoning": "Un presupuesto estático mezcla diferencias de actividad con diferencias de precio o eficiencia.", "common_error": "Etiquetar toda desviación contra el plan inicial como mala gestión."},
    {"question": "¿Qué NO puede concluir U2 aunque un proyecto tenga caja positiva y supere el punto de equilibrio?", "answer": "No puede concluir que sea clínicamente eficaz, coste-efectivo, éticamente preferible, una buena inversión real o conforme a IFRS; esas conclusiones requieren evidencia y métodos adicionales.", "reasoning": "Sostenibilidad financiera es una dimensión distinta de resultados sanitarios, valoración, auditoría y evaluación económica formal.", "common_error": "Convertir indicadores financieros básicos en decisión sanitaria o de inversión."}
  ],
  "biomedical_connections": [
    {"topic": "Gestión de servicios biomédicos", "connection": "Permite separar capacidad, estructura de costes, resultado y caja al planificar un servicio técnico ficticio."},
    {"topic": "Tecnología médica", "connection": "Distingue compra de equipo como inversión de largo plazo, gasto del periodo y financiación asociada."},
    {"topic": "Startups y proyectos de salud", "connection": "Introduce punto de equilibrio, calendario de caja y capital de trabajo sin sustituir valoración de empresa ni due diligence."},
    {"topic": "Evaluación de tecnologías sanitarias", "connection": "Prepara costes y flujos, pero reserva comparación formal de costes y resultados sanitarios para U5."},
    {"topic": "Gobernanza y auditoría", "connection": "Promueve trazabilidad de supuestos y transacciones sin afirmar cumplimiento IFRS ni auditoría profesional."}
  ],
  "sources": [
    {"title": "Conceptual Framework for Financial Reporting", "organization": "IFRS Foundation", "year": 2021, "url": "https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2021/issued/part-a/conceptual-framework-for-financial-reporting.pdf", "type": "marco conceptual normativo", "description": "Definiciones y principios conceptuales de activos, pasivos, patrimonio, ingresos, gastos y reconocimiento.", "verification_status": "verified_directly"},
    {"title": "IAS 1 Presentation of Financial Statements", "organization": "IFRS Foundation", "url": "https://www.ifrs.org/issued-standards/list-of-standards/ias-1-presentation-of-financial-statements.html/", "type": "estándar y resumen oficial", "description": "Estructura del conjunto completo de estados y advertencia de que cumplimiento IFRS requiere satisfacer todos los requisitos aplicables.", "verification_status": "verified_directly"},
    {"title": "IFRS 18 Presentation and Disclosure in Financial Statements", "organization": "IFRS Foundation", "year": 2024, "url": "https://www.ifrs.org/issued-standards/list-of-standards/ifrs-18-presentation-and-disclosure-in-financial-statements/", "type": "estándar y resumen oficial", "description": "Reemplaza IAS 1 y es efectivo para periodos anuales iniciados el 1 de enero de 2027 o después, con aplicación anticipada permitida.", "verification_status": "verified_directly"},
    {"title": "IAS 7 Statement of Cash Flows", "organization": "IFRS Foundation", "year": 2022, "url": "https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2022/issued/part-a/ias-7-statement-of-cash-flows.pdf?bypass=on", "type": "estándar oficial", "description": "Define efectivo, equivalentes y actividades operativas, de inversión y financiación y la utilidad de relacionar beneficio y flujo neto de caja.", "verification_status": "verified_directly"},
    {"title": "Chapter 2 Summary — Principles of Accounting, Volume 1: Financial Accounting", "organization": "OpenStax", "year": 2019, "url": "https://openstax.org/books/principles-financial-accounting/pages/2-summary", "type": "texto universitario abierto", "description": "Relación entre estados financieros, ecuación contable, capital de trabajo y razón corriente.", "verification_status": "verified_directly"},
    {"title": "Explain the Purpose of the Statement of Cash Flows", "organization": "OpenStax", "year": 2019, "url": "https://openstax.org/books/principles-financial-accounting/pages/16-1-explain-the-purpose-of-the-statement-of-cash-flows", "type": "texto universitario abierto", "description": "Explica por qué beneficio por devengo y flujos de efectivo pueden diferir.", "verification_status": "verified_directly"},
    {"title": "Explain Contribution Margin and Calculate Contribution Margin", "organization": "OpenStax", "year": 2019, "url": "https://openstax.org/books/principles-managerial-accounting/pages/3-1-explain-contribution-margin-and-calculate-contribution-margin-per-unit-contribution-margin-ratio-and-total-contribution-margin", "type": "texto universitario abierto", "description": "Costes fijos/variables, rango relevante y margen de contribución.", "verification_status": "verified_directly"},
    {"title": "Calculate a Break-Even Point in Units and Dollars", "organization": "OpenStax", "year": 2019, "url": "https://openstax.org/books/principles-managerial-accounting/pages/3-2-calculate-a-break-even-point-in-units-and-dollars", "type": "texto universitario abierto", "description": "Supuestos y cálculo de punto de equilibrio mediante margen de contribución.", "verification_status": "verified_directly"},
    {"title": "Chapter 7 Summary — Managerial Accounting", "organization": "OpenStax", "year": 2019, "url": "https://openstax.org/books/principles-managerial-accounting/pages/7-summary", "type": "texto universitario abierto", "description": "Presupuestos operativos, financieros, de caja, estáticos y flexibles y variaciones.", "verification_status": "verified_directly"},
    {"title": "What Is Working Capital? — Principles of Finance 2e", "organization": "OpenStax", "year": 2026, "url": "https://openstax.org/books/principles-finance-2e/pages/19-1-what-is-working-capital", "type": "texto universitario abierto", "description": "Capital de trabajo, liquidez, razón corriente y límites de interpretación de indicadores puntuales.", "verification_status": "verified_directly"}
  ],
  "editorial_notice": "Material educativo curado internamente y mantenido en estado review. Las fuentes se verificaron directamente para este alcance, incluida la transición IAS 1→IFRS 18 vigente a agosto de 2026, pero esto no constituye revisión disciplinar externa, preparación o auditoría de estados financieros, afirmación de cumplimiento IFRS, asesoría contable/fiscal, valoración, recomendación de inversión ni evaluación económica sanitaria. Todas las actividades usan entidades y datos sintéticos."
}

text = json.dumps(unit, ensure_ascii=False)
assert GENERIC.casefold() not in text.casefold()
assert "V(a)=" not in text
assert len(unit["theory_sections"]) == 4
assert len(unit["worked_examples"]) >= 5
assert len(unit["glossary"]) >= 20
assert len(unit["self_assessment"]) >= 10
assert len(unit["sources"]) >= 9

serialized = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
SOURCE.write_text(serialized, encoding="utf-8")
MIRROR.parent.mkdir(parents=True, exist_ok=True)
MIRROR.write_text(serialized, encoding="utf-8")

TEST.write_text(r'''from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-02.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EconomiaGestionEmpresasUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_mirror_and_review_status(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_and_premature_mcda_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("v(a)=", text)
        for concept in ("base de devengo", "margen de contribución", "punto de equilibrio", "capital de trabajo", "presupuesto flexible"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_keeps_u5_boundary(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("1 de enero de 2027", theory)
        self.assertIn("se reserva para u5", theory)
        self.assertIn("no es una auditoría", theory)

    def test_core_equations_are_present(self):
        equations = {e["latex"] for section in self.unit["theory_sections"] for e in section.get("equations", [])}
        for equation in ("A=L+E", "CM_u=P-V_u", r"Q_{BE}=\frac{F}{P-V_u}", "NWC=CA-CL", r"CR=\frac{CA}{CL}", "Var=Actual-Budget"):
            self.assertIn(equation, equations)

    def test_examples_and_guided_activity_are_scaffolded_and_synthetic(self):
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 7)
        self.assertGreaterEqual(len(activity["problems"]), 14)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("fictici", text)
        self.assertIn("no incorpores", text)

    def test_glossary_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("estado de situación financiera", "base de devengo", "margen de contribución", "punto de equilibrio", "razón corriente", "presupuesto flexible"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_time_aware(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://www.ifrs.org/issued-standards/list-of-standards/ifrs-18-presentation-and-disclosure-in-financial-statements/", urls)
        self.assertIn("https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2022/issued/part-a/ias-7-statement-of-cash-flows.pdf?bypass=on", urls)
        self.assertIn("https://openstax.org/books/principles-finance-2e/pages/19-1-what-is-working-capital", urls)

    def test_professional_boundaries_are_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in ("no constituye revisión disciplinar externa", "cumplimiento ifrs", "recomendación de inversión", "evaluación económica sanitaria"):
            self.assertIn(phrase, notice)
        self.assertIn("sin presentar", purpose)


if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8")

print("Economía y Gestión de Empresas U2 curada y espejo sincronizado")
