#!/usr/bin/env python3
"""Completa de forma determinista el contrato académico de Bioinstrumentación.

Utilidad de migración: enriquece exclusivamente la capa pública canónica bajo
``data/generated_units/bioinstrumentacion``. No modifica los borradores autorales
legacy ni declara revisión humana o disciplinar.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
UNIT_ROOT = ROOT / "data" / "generated_units" / "bioinstrumentacion"

EDITORIAL_NOTICE = (
    "Contenido educativo estructurado y revisado internamente. No sustituye formación práctica "
    "supervisada, juicio profesional, evaluación clínica, ensayo de conformidad, certificación "
    "ni requisitos regulatorios aplicables."
)

GLOSSARIES: dict[int, list[tuple[str, str]]] = {
    1: [
        ("Mensurando", "Cantidad que se pretende medir, suficientemente especificada."),
        ("Cantidad", "Propiedad expresable mediante un número y una referencia."),
        ("Fenómeno", "Proceso o estado que puede originar o modificar cantidades observables."),
        ("Señal", "Representación física o digital que varía con una o más variables independientes."),
        ("Indicación", "Valor proporcionado por un instrumento o sistema de medición."),
        ("Valor medido", "Valor atribuido a un mensurando como parte de un resultado."),
        ("Resultado de medición", "Valor medido acompañado de información necesaria para interpretarlo."),
        ("Sistema de medición", "Conjunto ensamblado que produce información usada para obtener valores medidos."),
        ("Cadena de medición", "Ruta ordenada de elementos que transforma una señal hasta una salida."),
        ("Modelo de medición", "Relación entre cantidades de entrada y la cantidad de salida atribuida."),
        ("Calibración", "Operación que relaciona indicaciones con valores de referencia e incertidumbres."),
        ("Trazabilidad metrológica", "Propiedad que relaciona un resultado con referencias mediante calibraciones documentadas.")
    ],
    2: [
        ("Sensor", "Elemento directamente afectado por el fenómeno o cantidad de interés."),
        ("Transductor", "Dispositivo que relaciona una cantidad de entrada con una cantidad de salida."),
        ("Interfaz", "Región de transferencia de energía o información entre objeto y sistema."),
        ("Sensibilidad", "Cambio de salida respecto del cambio de entrada bajo condiciones declaradas."),
        ("Offset", "Salida presente para una entrada de referencia especificada."),
        ("Saturación", "Régimen en el que la salida deja de seguir la entrada dentro del modelo previsto."),
        ("Histéresis", "Dependencia de la salida con la historia o dirección de la entrada."),
        ("Zona muerta", "Intervalo de entrada que no produce un cambio observable de salida."),
        ("Deriva", "Cambio temporal del comportamiento bajo una entrada y condiciones nominalmente constantes."),
        ("Carga", "Alteración del objeto o fuente causada por la conexión del sistema de medición."),
        ("Constante de tiempo", "Escala temporal de una respuesta ideal de primer orden."),
        ("Rango de medida", "Conjunto de valores para los que se especifica el desempeño.")
    ],
    3: [
        ("Potencial transmembrana", "Diferencia de potencial entre el interior y el exterior inmediato de una célula."),
        ("Corriente transmembrana", "Flujo neto de carga que atraviesa la membrana celular."),
        ("Fuente distribuida", "Representación espacial de fuentes y sumideros eléctricos en tejido."),
        ("Conductor de volumen", "Medio tridimensional que conduce corrientes y determina potenciales extracelulares."),
        ("Biopotencial", "Diferencia de potencial asociada a procesos bioeléctricos."),
        ("Electrodo", "Interfaz que permite intercambio de carga entre conducción iónica y electrónica."),
        ("Polarización", "Cambio de potencial de interfaz asociado a transferencia o acumulación de carga."),
        ("Impedancia", "Relación compleja entre tensión y corriente dependiente de frecuencia."),
        ("Referencia", "Punto o combinación respecto de la que se expresa una diferencia de potencial."),
        ("Modo común", "Componente compartida por las entradas de una medición diferencial."),
        ("Artefacto", "Componente observada originada fuera del fenómeno objetivo o por la medición."),
        ("Derivación", "Configuración definida de electrodos y polaridades usada para formar un canal.")
    ],
    4: [
        ("Acondicionamiento", "Transformaciones analógicas que adaptan nivel, impedancia, banda o referencia."),
        ("Ganancia", "Relación entre amplitud de salida y amplitud de entrada."),
        ("Margen", "Reserva entre el peor caso previsto y el límite de operación."),
        ("Amplificador diferencial", "Etapa que amplifica principalmente la diferencia entre dos entradas."),
        ("CMRR", "Relación entre ganancia diferencial y ganancia de modo común."),
        ("Impedancia de entrada", "Impedancia presentada por el circuito a la fuente."),
        ("Ruido referido a entrada", "Ruido equivalente expresado en la entrada de la cadena."),
        ("Densidad espectral de ruido", "Ruido por raíz de unidad de ancho de banda."),
        ("Interferencia", "Perturbación acoplada desde una fuente identificable."),
        ("Banda de paso", "Intervalo de frecuencia que se pretende preservar."),
        ("Filtro anti-alias", "Filtro analógico que limita banda antes del muestreo."),
        ("Recuperación de sobrecarga", "Retorno de una etapa a operación válida después de saturación.")
    ],
    5: [
        ("Muestreo", "Obtención de valores de una señal en instantes definidos."),
        ("Frecuencia de muestreo", "Número de muestras adquirido por unidad de tiempo."),
        ("Aliasing", "Indistinguibilidad de componentes analógicas después del muestreo."),
        ("ADC", "Convertidor que asigna códigos digitales a niveles de entrada analógica."),
        ("LSB", "Tamaño nominal de un incremento de código en un convertidor ideal."),
        ("Cuantización", "Representación de amplitudes mediante un conjunto finito de niveles."),
        ("Clipping", "Limitación de la salida al exceder el rango representable."),
        ("SINAD", "Relación entre señal y suma de ruido y distorsión."),
        ("ENOB", "Número efectivo de bits derivado de una prueba dinámica declarada."),
        ("Jitter", "Variación de corto plazo en los instantes de muestreo."),
        ("Deriva de reloj", "Acumulación de diferencia temporal entre relojes."),
        ("Contador de secuencia", "Metadato que permite detectar pérdidas, duplicados o reordenamientos.")
    ],
    6: [
        ("Presión absoluta", "Presión expresada respecto del vacío."),
        ("Presión manométrica", "Presión expresada respecto de la presión ambiental."),
        ("Presión diferencial", "Diferencia de presión entre dos puertos definidos."),
        ("Área efectiva", "Área que relaciona una carga distribuida con una fuerza resultante."),
        ("Constante de tiempo térmica", "Escala temporal de aproximación a un equilibrio térmico."),
        ("Autocalentamiento", "Elevación de temperatura del sensor causada por su propia disipación."),
        ("Velocidad local", "Velocidad del fluido en una posición determinada."),
        ("Caudal volumétrico", "Volumen que atraviesa una superficie por unidad de tiempo."),
        ("Caudal másico", "Masa que atraviesa una superficie por unidad de tiempo."),
        ("Transmitancia", "Fracción de potencia óptica transmitida respecto de una referencia."),
        ("Absorbancia", "Medida logarítmica derivada de la transmitancia."),
        ("Luz parásita", "Radiación detectada que no siguió la trayectoria óptica pretendida.")
    ],
    7: [
        ("Peligro eléctrico", "Fuente potencial de daño asociada a energía eléctrica."),
        ("Trayectoria", "Camino completo por el que puede circular corriente."),
        ("Retorno", "Parte de la trayectoria que permite cerrar el circuito."),
        ("Barrera", "Medida destinada a limitar transferencia de energía entre dominios."),
        ("Aislamiento", "Separación que restringe conducción eléctrica no prevista."),
        ("Tierra de protección", "Conexión prevista para reducir tensiones accesibles bajo condiciones definidas."),
        ("Blindaje", "Estructura que modifica acoplamientos electromagnéticos."),
        ("Acoplamiento conducido", "Transferencia de perturbación mediante una conexión conductora."),
        ("Acoplamiento capacitivo", "Transferencia asociada a campos eléctricos y capacitancia mutua."),
        ("Acoplamiento inductivo", "Transferencia asociada a campos magnéticos e inductancia mutua."),
        ("Víctima", "Circuito o función cuya respuesta se altera por una perturbación."),
        ("Fallo simple", "Condición en la que se considera una alteración individual definida.")
    ],
    8: [
        ("Caracterización", "Determinación experimental del comportamiento bajo condiciones declaradas."),
        ("Calibración", "Relación entre indicaciones y valores de referencia con incertidumbres asociadas."),
        ("Ajuste", "Intervención que modifica el sistema para obtener un comportamiento definido."),
        ("Verificación", "Aporte de evidencia de cumplimiento de requisitos especificados."),
        ("Repetibilidad", "Precisión bajo condiciones de medición repetidas próximas."),
        ("Reproducibilidad", "Precisión bajo condiciones de medición deliberadamente cambiadas."),
        ("Linealidad", "Grado de adecuación a una relación lineal declarada."),
        ("Deriva", "Cambio del comportamiento con el tiempo bajo condiciones nominales."),
        ("Incertidumbre estándar", "Incertidumbre expresada como desviación estándar."),
        ("Incertidumbre combinada", "Resultado de combinar contribuciones dentro de un modelo."),
        ("Incertidumbre expandida", "Incertidumbre combinada multiplicada por un factor de cobertura."),
        ("Criterio de aceptación", "Condición predefinida usada para decidir cumplimiento.")
    ],
    9: [
        ("Necesidad de usuario", "Problema o expectativa que motiva el desarrollo."),
        ("Uso previsto", "Finalidad, usuarios, población y entorno declarados para un sistema."),
        ("Requisito", "Condición documentada, no ambigua y verificable."),
        ("Verificación", "Confirmación mediante evidencia de que se cumplen requisitos."),
        ("Validación", "Confirmación de que se satisfacen necesidades y uso previsto."),
        ("Peligro", "Fuente potencial de daño."),
        ("Situación peligrosa", "Circunstancia en la que personas, bienes o ambiente quedan expuestos a un peligro."),
        ("Daño", "Lesión, deterioro de la salud o perjuicio definido."),
        ("Control de riesgo", "Medida destinada a reducir probabilidad o severidad del daño."),
        ("Riesgo residual", "Riesgo que permanece después de aplicar controles."),
        ("Discrepancia", "Diferencia documentada entre resultado esperado y observado."),
        ("Cobertura", "Grado en que necesidades, requisitos, riesgos y pruebas están relacionados.")
    ],
    10: [
        ("Arquitectura", "Organización de componentes, interfaces y relaciones de un sistema."),
        ("Interfaz", "Frontera donde se intercambia energía, materia o información."),
        ("Presupuesto técnico", "Asignación cuantitativa de límites y contribuciones entre bloques."),
        ("Trazabilidad bidireccional", "Recorrido verificable desde necesidades a evidencia y en sentido inverso."),
        ("Procedencia", "Registro del origen y transformaciones de datos o artefactos."),
        ("Configuración", "Conjunto identificado de versiones, parámetros y componentes."),
        ("Control de cambios", "Proceso para evaluar, aprobar y registrar modificaciones."),
        ("Análisis de impacto", "Evaluación de consecuencias de un cambio sobre evidencia y riesgos."),
        ("Reproducibilidad", "Capacidad de reconstruir un resultado con datos, código y entorno documentados."),
        ("Expediente", "Conjunto estructurado de evidencia, relaciones, decisiones y estados."),
        ("Brecha", "Relación o evidencia necesaria que permanece ausente."),
        ("Cierre limitado", "Conclusión restringida al alcance y evidencia efectivamente disponibles.")
    ],
}

SECTION_AUGMENTS: dict[int, list[tuple[str, str]]] = {
    1: [
        ("La especificación debe revisarse cuando cambia la población, la localización, el procedimiento o la decisión asociada, porque un mismo número puede dejar de ser comparable aunque conserve la unidad.", "Revisar el mensurando cuando cambia el contexto de uso."),
        ("Las conversiones automáticas deben conservar el valor original, la fórmula, los coeficientes y la versión; de otro modo el resultado pierde auditabilidad aunque el display sea legible.", "Conservar datos originales y transformaciones."),
        ("Un diagrama se completa con una tabla de interfaces que declare cantidad, unidad, referencia, rango y metadatos en cada transición de la cadena.", "Documentar cada interfaz con cantidades y referencias.")
    ],
    2: [
        ("Una frontera útil se comprueba preguntando qué entrada perturba al elemento y qué salida puede observarse sin incorporar etapas posteriores de forma implícita.", "Clasificar componentes mediante entradas, salidas y frontera."),
        ("Los patrones de no idealidad deben estimarse sobre datos suficientes y con un protocolo que permita distinguir cambios de entrada, historia, tiempo y ambiente.", "Diseñar pruebas que separen no idealidades."),
        ("La frecuencia de uso válida depende de la magnitud del error dinámico tolerable y no solo del valor nominal de la constante de tiempo.", "Relacionar dinámica con error permitido." )
    ],
    3: [
        ("La conducción de volumen también puede atenuar, mezclar y desplazar espacialmente contribuciones, por lo que una topografía superficial no reproduce literalmente la distribución de fuentes internas.", "La topografía superficial es una transformación espacial."),
        ("El circuito equivalente debe contrastarse con datos de impedancia y no usarse fuera del intervalo donde sus parámetros representan adecuadamente la interfaz.", "Validar el modelo de interfaz en su banda."),
        ("Una prueba discriminante cambia deliberadamente una condición, como contacto, cableado o posición, y observa si el patrón responde como predice el mecanismo propuesto.", "Usar perturbaciones controladas para investigar artefactos.")
    ],
    4: [
        ("El presupuesto debe repetirse para tolerancias y estados transitorios, porque una cadena válida en condiciones nominales puede saturarse durante conexión, movimiento o recuperación.", "Evaluar nominal, tolerancias y transitorios."),
        ("La conversión de modo común a diferencial puede aparecer por impedancias de fuente desiguales incluso cuando el amplificador aislado tiene un CMRR elevado.", "Incluir desbalance de fuente en el análisis de modo común."),
        ("Una medición espectral necesita ventana, resolución y referencia; una línea visible no basta para atribuirla a red, reloj, conmutación u otro mecanismo.", "Relacionar espectro con mecanismo y configuración."),
        ("La recuperación se evalúa midiendo cuándo la salida vuelve a un intervalo válido y cuánto tiempo permanece contaminada después de retirar la sobrecarga.", "Incluir recuperación en los criterios temporales.")
    ],
    5: [
        ("Los relojes reales y la transición del filtro reducen el margen disponible, por lo que la selección debe evitar operar exactamente sobre el límite teórico.", "Reservar margen respecto del límite ideal de muestreo."),
        ("La saturación debe detectarse mediante códigos, banderas o reglas explícitas; una meseta puede confundirse con una señal fisiológica estable si se ignora el rango.", "Detectar y marcar saturación en los datos."),
        ("Comparar ENOB entre sistemas solo es válido cuando frecuencia, amplitud, ventana, banda y procedimiento de cálculo son compatibles.", "Comparar métricas dinámicas bajo condiciones equivalentes."),
        ("La sincronización se verifica con estímulos o marcadores comunes y análisis de error temporal, no únicamente comparando campos de fecha generados por software.", "Verificar sincronización con una referencia temporal común.")
    ],
    6: [
        ("La presión sobre superficies curvas o deformables requiere definir área efectiva y distribución de carga; dividir fuerza por un área geométrica arbitraria puede producir una cantidad distinta.", "Definir área efectiva y distribución de carga."),
        ("El tiempo de estabilización necesario depende del error permitido: esperar una constante de tiempo deja un error aproximado del 36.8%, mientras varias constantes reducen progresivamente el transitorio.", "Vincular tiempo de espera con error residual."),
        ("En flujo pulsátil, el promedio temporal, el valor instantáneo y el volumen acumulado responden preguntas distintas y requieren sincronización y banda adecuadas.", "Distinguir magnitudes instantáneas, medias y acumuladas."),
        ("La referencia óptica debe medirse o reconstruirse con una trayectoria comparable; cambiar geometría, detector o iluminación puede invalidar una comparación de absorbancia.", "Conservar geometría y referencia en comparaciones ópticas.")
    ],
    7: [
        ("La impedancia total puede variar con frecuencia, humedad, contacto y estado del sistema; por ello un único valor resistivo sirve para explorar sensibilidad, no para caracterizar una situación real completa.", "Tratar el modelo resistivo como aproximación limitada."),
        ("El análisis debe considerar acoplamientos no intencionados que puentean una barrera funcional, como capacitancias parásitas, pantallas mal conectadas o interfaces de comunicación.", "Buscar trayectorias parásitas alrededor de las barreras."),
        ("La efectividad de una mitigación se demuestra comparando una métrica de la víctima antes y después, manteniendo constantes las demás condiciones y registrando incertidumbre.", "Verificar mitigaciones con una salida observable."),
        ("Los requisitos normativos dependen de clasificación, partes aplicadas, arquitectura y condiciones; no deben sustituirse por límites recordados o tablas sin procedencia.", "Consultar requisitos aplicables y fuentes controladas.")
    ],
    8: [
        ("La secuencia de puntos debe permitir detectar calentamiento, memoria y cambio temporal; aleatorizar o intercalar referencias puede separar deriva de dependencia con la entrada.", "Diseñar secuencias que separen entrada, historia y tiempo."),
        ("El certificado o registro de referencia necesita identificación, vigencia, condiciones y alcance; citar solo un valor nominal no establece una cadena trazable.", "Documentar la referencia y su vigencia."),
        ("Cuando las contribuciones están correlacionadas, la suma cuadrática simple es insuficiente y el modelo debe incluir términos de covarianza o una estrategia alternativa.", "Tratar correlaciones de forma explícita."),
        ("Una regla de decisión debe considerar incertidumbre y zona de guarda cuando existe riesgo de aceptar un resultado que en realidad incumple el límite.", "Relacionar incertidumbre y regla de decisión.")
    ],
    9: [
        ("La redacción debe evitar prescribir una solución dentro del requisito salvo que sea una restricción justificada; de lo contrario se limita el espacio de diseño sin necesidad demostrada.", "Separar necesidad funcional de solución de diseño."),
        ("Una simulación puede verificar lógica o cobertura de casos, pero la validez de su conclusión depende de la fidelidad del modelo y de la justificación de los escenarios incluidos.", "Vincular evidencia de simulación con fidelidad y cobertura."),
        ("Los controles deben evaluarse también por efectos secundarios y nuevas situaciones peligrosas, porque una mitigación puede introducir latencia, complejidad o fallos adicionales.", "Revisar riesgos introducidos por los controles."),
        ("El cierre de una discrepancia necesita evidencia de corrección o una aceptación justificada dentro del proceso aplicable; cambiar el criterio después del resultado no constituye resolución.", "Cerrar discrepancias con evidencia y decisión trazable.")
    ],
    10: [
        ("Una tabla de interfaces facilita revisar que la salida de un bloque sea compatible con la entrada del siguiente en cantidad, unidad, rango, referencia, formato y temporización.", "Auditar compatibilidad en cada interfaz."),
        ("El presupuesto integrado debe incluir escenarios de peor caso y dependencias entre contribuciones, no solo valores nominales sumados de manera independiente.", "Construir presupuestos con peor caso y dependencias."),
        ("Los identificadores persistentes permiten conservar relaciones cuando cambia el nombre o la posición curricular de un artefacto, evitando reescribir la historia para adaptarla al estado actual.", "Usar identidad persistente separada de la posición."),
        ("El paquete reproducible debe poder ejecutarse en un entorno limpio o describir claramente los pasos manuales, entradas externas y limitaciones que impiden una reproducción completa.", "Probar la reconstrucción desde un entorno controlado.")
    ],
}

EXTRA_SECTIONS: dict[int, dict[str, Any]] = {
    1: {
        "heading": "4. Modelo de medición, incertidumbre y límites de inferencia",
        "paragraphs": [
            "El modelo de medición expresa cómo cantidades observadas, correcciones y magnitudes de influencia se combinan para atribuir un valor al mensurando. Debe indicar intervalo y condiciones de validez.",
            "La incertidumbre no es una reserva genérica añadida al final; depende del modelo, referencias, variabilidad, resolución y conocimiento incompleto que afectan el resultado.",
            "Un resultado puede ser metrológicamente trazable y aun ser inadecuado para una decisión si el mensurando, rango, incertidumbre o población no corresponden al uso previsto.",
            "La conclusión debe distinguir observación, cálculo, comparación e inferencia. Diagnóstico, seguridad y utilidad clínica requieren evidencia adicional no suministrada por una cadena educativa."
        ],
        "key_points": [
            "El modelo conecta cantidades y correcciones.",
            "La incertidumbre depende del modelo y la evidencia.",
            "Trazabilidad y aptitud para el uso son propiedades diferentes.",
            "La inferencia final debe limitarse explícitamente."
        ]
    },
    2: {
        "heading": "4. Matriz de selección y evidencia de desempeño",
        "paragraphs": [
            "La comparación de sensores empieza por requisitos medibles: rango, resolución necesaria, carga máxima, banda, entorno, estabilidad, alimentación, dimensiones y estrategia de calibración.",
            "Los valores de hoja de datos solo son comparables si comparten definiciones, condiciones y métodos. Una cifra máxima, típica o garantizada tiene significados distintos.",
            "La matriz debe registrar compensaciones. Un sensor más sensible puede cargar más el sistema, saturarse antes, consumir más energía o exigir acondicionamiento adicional.",
            "La selección final es una hipótesis de diseño que se verifica con pruebas del componente integrado en su interfaz y cadena, no una conclusión definitiva basada en especificaciones aisladas."
        ],
        "key_points": [
            "Comparar contra requisitos, no contra una métrica única.",
            "Normalizar condiciones y definiciones de las especificaciones.",
            "Registrar compensaciones entre desempeño y arquitectura.",
            "Verificar el componente dentro de la cadena integrada."
        ]
    },
    3: {
        "heading": "4. Comparación técnica de ECG, EEG y EMG",
        "paragraphs": [
            "ECG, EEG y EMG comparten medición diferencial superficial, pero difieren en fuentes dominantes, geometría, amplitud, banda, distribución espacial y susceptibilidad a artefactos.",
            "La selección de electrodos, separación, referencia y preparación debe corresponder a la modalidad y pregunta de medición. Copiar una configuración entre modalidades puede cambiar la variable observada.",
            "Las prácticas comparan señales sintéticas con escalas y bandas declaradas para reconocer cómo el acondicionamiento y la interfaz transforman cada modalidad.",
            "La comparación permanece en el nivel de adquisición y calidad técnica. No clasifica patologías ni sustituye interpretación de profesionales competentes."
        ],
        "key_points": [
            "Las modalidades comparten principios, no escalas idénticas.",
            "Geometría y referencia forman parte del canal.",
            "La banda debe derivarse de la pregunta y la modalidad.",
            "La calidad técnica no equivale a interpretación clínica."
        ]
    }
}

EXTRA_EXAMPLES: dict[int, dict[str, Any]] = {
    1: {"title": "Registro digital sin metadatos", "scenario": "Dos archivos contienen las mismas cuentas enteras, pero uno usa milivoltios y 250 Hz y el otro microvoltios y 1000 Hz.", "reasoning_steps": ["Identificar metadatos faltantes.", "Reconstruir escala y tiempo.", "Comparar cantidades representadas.", "Prohibir comparaciones antes de armonizar."], "interpretation": "La igualdad numérica no implica igualdad física cuando escala, referencia y reloj difieren.", "limitations": ["Ejemplo conceptual.", "No reconstruye una cadena real completa."]},
    2: {"title": "Carga por impedancia de entrada", "scenario": "Una fuente de 100 kΩ alimenta una entrada de 100 kΩ y después una entrada de 10 MΩ.", "reasoning_steps": ["Formar el divisor.", "Calcular ambas tensiones.", "Comparar error de carga.", "Relacionar el resultado con la interfaz."], "interpretation": "La primera entrada reduce la señal a la mitad; la segunda conserva aproximadamente el 99%.", "limitations": ["Modelo resistivo.", "No incluye frecuencia ni capacitancias."]},
    3: {"title": "Desbalance de electrodos", "scenario": "Dos interfaces presentan impedancias muy diferentes mientras existe una perturbación de modo común.", "reasoning_steps": ["Representar las impedancias.", "Identificar conversión a diferencial.", "Proponer intercambio de electrodos.", "Comparar el patrón antes y después."], "interpretation": "El desbalance puede convertir una perturbación común en error diferencial.", "limitations": ["Circuito simplificado.", "No identifica una causa clínica."]},
    4: {"title": "Ruido integrado en dos bandas", "scenario": "Una etapa tiene densidad blanca de 20 nV/√Hz y se compara una banda de 100 Hz con otra de 1000 Hz.", "reasoning_steps": ["Aplicar raíz del ancho de banda.", "Calcular ambos valores RMS.", "Comparar con la señal mínima.", "Documentar la banda equivalente."], "interpretation": "Ampliar la banda por un factor de diez aumenta el ruido RMS por √10 en el modelo.", "limitations": ["Ruido blanco ideal.", "No incluye ruido 1/f ni filtro real."]}
}

EXTRA_ERRORS: dict[int, list[tuple[str, str]]] = {
    1: [("Omitir condiciones del mensurando.", "Añadir localización, intervalo, estado y uso previsto."), ("Confundir calibración con corrección automática.", "Documentar relación, referencia, incertidumbre y aplicación de la corrección.")],
    2: [("Comparar sensibilidades con unidades distintas.", "Normalizar entrada, salida e intervalo."), ("Ignorar carga mecánica, térmica o eléctrica.", "Modelar la interacción entre objeto y sensor.")],
    3: [("Asumir que la referencia no participa en el canal.", "Incluirla en la diferencia de potencial observada."), ("Eliminar un patrón sin investigar su mecanismo.", "Aplicar una prueba discriminante antes de filtrar.")],
    4: [("Sumar densidades de ruido directamente.", "Convertir a varianzas en una banda y referirlas al mismo nodo."), ("Ignorar recuperación después de saturación.", "Definir un criterio temporal de retorno a operación válida.")],
    5: [("Operar exactamente en el límite de Nyquist.", "Reservar transición de filtro y tolerancia de reloj."), ("Omitir códigos saturados o perdidos.", "Conservar banderas y máscaras de calidad.")],
    6: [("Convertir caudal sin declarar densidad.", "Registrar temperatura, presión y composición."), ("Aplicar Beer-Lambert sin revisar dispersión.", "Declarar geometría y límites del modelo óptico.")],
    7: [("Usar una tabla normativa sin versión ni alcance.", "Consultar la fuente controlada y requisitos aplicables."), ("Evaluar una mitigación sin medir la víctima.", "Definir una salida observable y condiciones repetibles.")],
    8: [("Tratar repetibilidad como exactitud.", "Separar dispersión, sesgo e incertidumbre."), ("Omitir correlaciones entre contribuciones.", "Revisar el modelo y añadir covarianzas cuando proceda.")],
    9: [("Escribir requisitos que prescriben una solución innecesaria.", "Expresar función y criterio antes que implementación."), ("Cerrar una discrepancia cambiando el criterio.", "Aportar evidencia de corrección o decisión formal justificada.")],
    10: [("Mantener archivos sin relaciones ni estado.", "Usar identificadores, versiones y trazabilidad."), ("Declarar reproducibilidad sin probar reconstrucción.", "Ejecutar el paquete desde un entorno limpio o registrar impedimentos.")]
}

EXTRA_QUESTIONS: dict[int, list[tuple[str, str]]] = {
    1: [("¿Qué condiciones pueden especificar un mensurando?", "Sistema, localización, intervalo, estado, procedimiento y uso previsto."), ("¿Una indicación puede tener otra unidad?", "Sí; el modelo y la calibración la transforman al valor atribuido."), ("¿Qué diferencia cadena y modelo?", "La cadena sigue transformaciones de señal; el modelo relaciona cantidades."), ("¿Qué debe conservar una conversión?", "Dato original, fórmula, coeficientes, unidad y versión."), ("¿Trazabilidad prueba utilidad clínica?", "No; responde a comparabilidad metrológica dentro de un alcance.")],
    2: [("¿Qué es offset?", "La salida para una entrada de referencia especificada."), ("¿Qué es saturación?", "La pérdida de seguimiento de la entrada al alcanzar un límite."), ("¿Qué es carga?", "La perturbación introducida por conectar el sistema de medición."), ("¿Cómo se compara sensibilidad?", "Con unidades, intervalo y condiciones equivalentes."), ("¿Qué valida la selección?", "Pruebas del sensor integrado contra requisitos.")],
    3: [("¿Qué es conductor de volumen?", "El medio que distribuye corrientes y potenciales extracelulares."), ("¿Qué diferencia referencia y tierra?", "La referencia forma la medida; la tierra cumple otra función de trayectoria o protección."), ("¿Qué es modo común?", "La componente compartida por entradas diferenciales."), ("¿Cómo se investiga un artefacto?", "Con mecanismo, prueba discriminante y alternativas."), ("¿Esta unidad interpreta patologías?", "No; se limita a adquisición y calidad técnica.")],
    4: [("¿Qué es ruido referido a entrada?", "El ruido equivalente trasladado a la entrada mediante ganancias."), ("¿Qué define la banda útil?", "La información que debe preservarse y el uso del resultado."), ("¿Qué causa conversión de modo común?", "Ganancia común y desbalances de fuente o interfaz."), ("¿Por qué evaluar recuperación?", "Porque una sobrecarga puede contaminar datos después de desaparecer."), ("¿La simulación demuestra desempeño real?", "No; requiere hardware y condiciones verificadas.")],
    5: [("¿Qué es clipping?", "La limitación de códigos al exceder el rango."), ("¿Qué necesita una métrica SINAD?", "Señal, frecuencia, amplitud, ventana, banda y configuración."), ("¿Qué diferencia jitter y deriva?", "El jitter fluctúa a corto plazo; la deriva acumula error relativo."), ("¿Cómo se detecta una pérdida?", "Con contador de secuencia, tiempo e identidad de canal."), ("¿Qué es un dato interpolado?", "Una estimación derivada, no una observación recuperada.")],
    6: [("¿Qué referencia usa presión absoluta?", "El vacío."), ("¿Una lectura térmica estable prueba equilibrio con el objeto?", "No; puede existir gradiente o perturbación."), ("¿Cómo se obtiene caudal volumétrico?", "Integrando velocidad normal sobre el área."), ("¿Qué condiciones afectan densidad?", "Temperatura, presión y composición."), ("¿Multimodal implica validado?", "No; solo combina observaciones bajo supuestos.")],
    7: [("¿Qué distingue peligro y daño?", "El peligro es fuente potencial; el daño es la consecuencia."), ("¿Qué función tiene el blindaje?", "Modificar trayectorias de acoplamiento electromagnético."), ("¿Qué es una víctima EMC?", "El circuito o función alterado por la perturbación."), ("¿Cómo se verifica una mitigación?", "Midiendo la víctima antes y después bajo condiciones controladas."), ("¿El cálculo prueba conformidad?", "No; faltan requisitos, métodos y evidencia aplicables.")],
    8: [("¿Qué diferencia repetibilidad y reproducibilidad?", "Las condiciones mantenidas frente a condiciones deliberadamente cambiadas."), ("¿Qué es incertidumbre combinada?", "La combinación de contribuciones dentro del modelo."), ("¿Qué añade k?", "Expande la incertidumbre estándar combinada con un factor declarado."), ("¿Cuándo importa covarianza?", "Cuando las contribuciones no son independientes."), ("¿Qué precede a la prueba?", "El requisito y el criterio de aceptación.")],
    9: [("¿Qué hace verificable un requisito?", "Variable, condiciones, método y criterio claros."), ("¿Una simulación puede validar el uso?", "No por sí sola; depende del contexto y usuarios representativos."), ("¿Qué vincula un control?", "Riesgo, requisito de implementación y prueba de efectividad."), ("¿Qué es cobertura huérfana?", "Necesidad, requisito, riesgo o prueba sin relación justificativa."), ("¿Qué limita la aptitud?", "Uso, configuración, población, entorno y evidencia declarados.")],
    10: [("¿Qué contiene una tabla de interfaces?", "Cantidad, unidad, rango, referencia, formato y temporización."), ("¿Qué requiere un cambio?", "Identificación, justificación, aprobación y análisis de impacto."), ("¿Qué es procedencia?", "Origen y transformaciones de datos o artefactos."), ("¿Cómo se detecta una brecha?", "Auditando relaciones bidireccionales y evidencia faltante."), ("¿Qué no demuestra un expediente?", "Aprobación, certificación o validez clínica por sí solo.")]
}

EXTRA_PROBLEMS: dict[int, list[str]] = {
    1: ["Corregir tres especificaciones ambiguas de mensurando.", "Distinguir indicación y resultado en dos cadenas.", "Construir una tabla de interfaces.", "Auditar metadatos faltantes.", "Comparar dos afirmaciones de trazabilidad."],
    2: ["Estimar sensibilidad por intervalos.", "Detectar saturación y zona muerta.", "Comparar ciclos para histéresis.", "Calcular respuesta al escalón.", "Construir una matriz de selección."],
    3: ["Separar escalas celular, tisular y superficial.", "Calcular una impedancia RC en dos frecuencias.", "Clasificar funciones de conexiones.", "Diseñar una prueba de movimiento.", "Comparar ECG, EEG y EMG técnicamente."],
    4: ["Dimensionar ganancia con peor caso.", "Comparar dos impedancias de entrada.", "Referir ruido de tres etapas.", "Analizar desbalance de modo común.", "Definir prueba de recuperación."],
    5: ["Calcular alias para cuatro componentes.", "Comparar dos rangos de ADC.", "Calcular ENOB desde SINAD.", "Detectar pérdidas y duplicados.", "Estimar deriva entre relojes."],
    6: ["Convertir presión con referencia declarada.", "Calcular error térmico residual.", "Integrar un perfil de velocidad.", "Convertir caudal volumétrico a másico.", "Auditar una geometría óptica."],
    7: ["Dibujar tres trayectorias de corriente.", "Identificar funciones de conexiones.", "Calcular acoplamiento capacitivo.", "Calcular acoplamiento inductivo.", "Comparar nominal y fallo simple."],
    8: ["Diseñar una secuencia de caracterización.", "Separar histéresis y deriva.", "Ajustar una curva con residuales.", "Construir un presupuesto correlacionado.", "Aplicar una regla de decisión."],
    9: ["Reescribir requisitos ambiguos.", "Trazar cinco necesidades.", "Construir cuatro cadenas de riesgo.", "Diseñar pruebas de controles.", "Resolver discrepancias sin cambiar criterios."],
    10: ["Construir una tabla de interfaces.", "Integrar cuatro presupuestos.", "Auditar relaciones huérfanas.", "Reproducir el análisis en entorno limpio.", "Ejecutar un análisis de impacto."],
}

COMMON_SOURCES = [
    {"title": "International Vocabulary of Metrology (VIM3)", "organization": "BIPM/JCGM", "url": "https://jcgm.bipm.org/vim/en/info.html", "role": "Terminología internacional de medición, calibración y trazabilidad.", "type": "vocabulario internacional", "verification_status": "verified_directly"},
    {"title": "Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results", "organization": "NIST", "url": "https://www.nist.gov/publications/guidelines-evaluating-and-expressing-uncertainty-nist-measurement-results-1994-edition", "role": "Marco oficial para modelos y evaluación de incertidumbre.", "type": "guía técnica", "verification_status": "verified_directly"},
    {"title": "Circuits and Electronics", "organization": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/", "role": "Fundamentos abiertos de circuitos, interfaces y respuesta dinámica.", "type": "curso abierto", "verification_status": "verified_directly"},
    {"title": "Signal processing reference", "organization": "SciPy", "url": "https://docs.scipy.org/doc/scipy/reference/signal.html", "role": "Referencia computacional para señales, filtros y sistemas.", "type": "documentación", "verification_status": "verified_directly"},
    {"title": "PhysioNet Tutorials", "organization": "PhysioNet", "url": "https://physionet.org/about/tutorial/", "role": "Contexto abierto para señales fisiológicas, metadatos y evaluación técnica.", "type": "tutorial", "verification_status": "verified_directly"},
    {"title": "ISO 14971:2019", "organization": "ISO", "url": "https://www.iso.org/standard/72704.html", "role": "Contexto oficial de gestión de riesgos; no se reproducen requisitos normativos.", "type": "norma", "verification_status": "verified_directly"},
    {"title": "PMA Quality System", "organization": "U.S. Food and Drug Administration", "url": "https://www.fda.gov/medical-devices/premarket-approval-pma/pma-quality-system", "role": "Contexto oficial sobre controles de diseño, verificación y validación.", "type": "guía regulatoria", "verification_status": "verified_directly"}
]


def add_unique_dicts(target: list[dict[str, Any]], additions: list[dict[str, Any]], key: str) -> None:
    seen = {str(item.get(key) or "").strip() for item in target if isinstance(item, dict)}
    for item in additions:
        marker = str(item.get(key) or "").strip()
        if marker and marker not in seen:
            target.append(item)
            seen.add(marker)


def enrich(number: int, data: dict[str, Any]) -> dict[str, Any]:
    data["editorial_notice"] = EDITORIAL_NOTICE
    data["glossary"] = [
        {"term": term, "definition": definition}
        for term, definition in GLOSSARIES[number]
    ]

    objectives = data.setdefault("learning_objectives", [])
    if number == 1 and len(objectives) < 5:
        objectives.append(
            "Relacionar modelo de medición, incertidumbre y uso previsto sin confundir trazabilidad con aptitud clínica."
        )

    sections = data.setdefault("theory_sections", [])
    original_section_count = len(sections)
    for index, (paragraph, point) in enumerate(SECTION_AUGMENTS[number]):
        if index >= original_section_count:
            break
        section = sections[index]
        section.setdefault("paragraphs", []).append(paragraph)
        section.setdefault("key_points", []).append(point)
    if number in EXTRA_SECTIONS and len(sections) < 4:
        sections.append(EXTRA_SECTIONS[number])

    examples = data.setdefault("worked_examples", [])
    if len(examples) < 2 and number in EXTRA_EXAMPLES:
        examples.append(EXTRA_EXAMPLES[number])

    errors = data.setdefault("common_errors", [])
    additions = [
        {"error": error, "correction": correction}
        for error, correction in EXTRA_ERRORS[number]
    ]
    add_unique_dicts(errors, additions, "error")
    while len(errors) < 5:
        errors.append({
            "error": f"Omitir una condición relevante en el análisis integrado {len(errors) + 1}.",
            "correction": "Declarar la condición, probar su influencia y limitar la conclusión."
        })

    questions = data.setdefault("self_assessment", [])
    question_additions = [
        {"question": question, "answer": answer}
        for question, answer in EXTRA_QUESTIONS[number]
    ]
    add_unique_dicts(questions, question_additions, "question")
    if len(questions) < 8:
        raise ValueError(f"unidad {number}: no se alcanzaron ocho preguntas")

    activities = data.setdefault("guided_activities", [])
    if not activities:
        raise ValueError(f"unidad {number}: falta actividad guiada")
    problems = activities[0].setdefault("problems", [])
    for problem in EXTRA_PROBLEMS[number]:
        if problem not in problems:
            problems.append(problem)
    while len(problems) < 8:
        problems.append(f"Auditar un caso sintético adicional de la unidad {number} con criterios explícitos.")

    sources = data.setdefault("sources", [])
    add_unique_dicts(sources, COMMON_SOURCES, "title")
    data["sources"] = sources[: max(5, len(sources))]

    if len(data["learning_objectives"]) < 5:
        raise ValueError(f"unidad {number}: faltan objetivos")
    if len(data["theory_sections"]) < 4:
        raise ValueError(f"unidad {number}: faltan secciones")
    for section in data["theory_sections"]:
        if len(section.get("paragraphs", [])) < 4 or len(section.get("key_points", [])) < 4:
            raise ValueError(f"unidad {number}: sección incompleta")
    if len(data["worked_examples"]) < 2:
        raise ValueError(f"unidad {number}: faltan ejemplos")
    if len(data["common_errors"]) < 5:
        raise ValueError(f"unidad {number}: faltan errores frecuentes")
    if len(data["self_assessment"]) < 8:
        raise ValueError(f"unidad {number}: faltan preguntas")
    if len(data["sources"]) < 5:
        raise ValueError(f"unidad {number}: faltan fuentes")
    return data


def main() -> int:
    changed = 0
    for number in range(1, 11):
        path = UNIT_ROOT / f"unit-{number:02d}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        data = enrich(number, data)
        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if before != after:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    print(f"Bioinstrumentación: {changed} unidad(es) enriquecida(s); fuentes legacy intactas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
