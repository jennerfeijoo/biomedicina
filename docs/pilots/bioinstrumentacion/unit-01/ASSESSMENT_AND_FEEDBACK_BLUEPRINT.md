# Blueprint de evaluación y feedback — Bioinstrumentación, Unidad 1

**Estado:** preparación de autoría; ninguna actividad se considera todavía publicada.

## Principio

La unidad debe evaluar si el estudiante puede construir y auditar una medición, no si puede repetir definiciones. El vocabulario metrológico funciona como sistema de restricciones: una respuesta solo es válida si mantiene separadas cantidad, mensurando, señal, indicación, valor medido, resultado, modelo, influencia y trazabilidad.

## Resultados y evidencias

| Resultado | Evidencia principal | Error crítico | Criterio de dominio |
|---|---|---|---|
| Especificar el mensurando | ficha de especificación comparativa | usar una etiqueta clínica o el método como mensurando | cantidad, portador, estado, localización, tiempo, condiciones, unidad y uso previsto explícitos |
| Separar las capas de la medición | clasificación y corrección de cadenas | tratar señal, display o archivo como resultado completo | cada elemento clasificado por función y justificado |
| Representar sistema y cadena | diagrama funcional auditado | confundir cadena física y modelo de medición | fronteras, ruta, transformaciones, unidades, metadatos e influencias visibles |
| Formular un modelo introductorio | red de cantidades o ecuación comentada | omitir influencias o suponer identidad entre indicación y mensurando | variables, relaciones, correcciones, supuestos y dominio definidos |
| Auditar trazabilidad | revisión de afirmaciones y evidencia | atribuir trazabilidad al instrumento o al laboratorio | resultado, referencia, cadena, incertidumbre, procedimiento, tiempo y condiciones identificados |

## Secuencia de evaluación

### A1. Clasificación diagnóstica

**Formato:** 18 tarjetas distribuidas entre fenómeno, cantidad, mensurando, señal, indicación, valor medido, resultado, cantidad de entrada, influencia y referencia.

**Función:** detectar si el estudiante está usando la terminología por apariencia. Los distractores deben incluir:

- “actividad cardíaca”;
- “voltaje de salida del amplificador”;
- “código 2048 del ADC”;
- “temperatura del sensor”;
- “temperatura cutánea en el antebrazo a los 30 segundos de contacto”;
- “37,1 °C con incertidumbre y método documentados”;
- “certificado de calibración del termómetro”.

**Criterio:** al menos 15 clasificaciones correctas y explicación válida de los tres distractores críticos.

**Recuperación:** nueva clasificación con fuerza, flujo y concentración; no se reutilizan las mismas tarjetas.

### A2. Especificación de mensurandos

**Consigna:** transformar tres etiquetas vagas en especificaciones defendibles:

1. temperatura corporal;
2. presión arterial;
3. actividad eléctrica cardíaca.

El estudiante debe declarar qué información falta y proponer dos mensurandos diferentes compatibles con cada etiqueta.

**Rúbrica, 0–2 por criterio:**

- clase de cantidad;
- sistema o portador;
- localización;
- tiempo o agregación temporal;
- estado y condiciones;
- unidad o escala;
- método solo cuando forme parte de la definición;
- uso previsto y límite de inferencia.

**Error crítico:** usar “normal”, “alta”, “fiebre”, “saludable” o “arritmia” como si fueran cantidades.

### A3. Auditoría de una cadena de medición

Se entrega una cadena deliberadamente defectuosa:

> corazón → electrodo → ECG → diagnóstico

El estudiante debe reconstruirla en dos representaciones:

1. ruta de señal;
2. modelo de cantidades y resultado.

Debe localizar al menos seis problemas, entre ellos:

- fenómeno demasiado amplio;
- mensurando ausente;
- interacción electrodo-piel omitida;
- indicación y resultado fusionados;
- transformaciones no documentadas;
- inferencia diagnóstica no justificada;
- referencia y metadatos ausentes;
- influencias omitidas.

**Criterio:** corrige los dos diagramas y explica por qué no son equivalentes.

### A4. Modelo de medición introductorio

**Caso:** sensor térmico con respuesta dependiente de la temperatura del objeto, ambiente, tiempo de contacto, offset y parámetros de calibración.

**Producto:** modelo conceptual y, opcionalmente, una ecuación simple. Cada variable debe tener:

- nombre;
- símbolo;
- unidad;
- origen;
- incertidumbre o estado de conocimiento;
- función dentro del modelo.

**Criterio:** explica qué se observa, qué se infiere, qué se corrige y qué permanece incierto.

**Error crítico:** escribir una ecuación sin definir el mensurando o sin intervalo de validez.

### A5. Auditoría de trazabilidad

Se presentan cuatro afirmaciones:

1. “El termómetro es trazable a NIST”.
2. “El certificado demuestra que todos los resultados futuros son correctos”.
3. “La calibración vigente basta para cualquier intervalo y entorno”.
4. “Un resultado trazable es apto para cualquier decisión”.

Para cada una, el estudiante debe:

- identificar el sujeto correcto de la afirmación;
- localizar la referencia especificada;
- reconstruir o declarar ausente la cadena de calibraciones;
- identificar incertidumbre y condiciones;
- separar trazabilidad de aptitud para el uso;
- redactar una versión limitada y defendible.

**Criterio:** ningún instrumento, laboratorio o certificado se presenta como “trazable” sin referirse a un resultado concreto.

### A6. Caso de transferencia

**Caso no usado en teoría:** medición de fuerza plantar mediante una plataforma instrumentada simulada.

**Producto integrado:**

- mensurando;
- frontera del sistema;
- cadena de señal;
- modelo cualitativo;
- cantidades de influencia;
- indicación y resultado;
- afirmación de trazabilidad condicional;
- límites de interpretación.

**Regla:** el estudiante debe aplicar la estructura sin recibir la lista de categorías.

## Banco de misconceptions y feedback

### M1. “El número digital es el mensurando”

**Diagnóstico:** confusión entre indicación y cantidad pretendida.

**Por qué falla:** el número puede ser un código, una tensión convertida o una cantidad intermedia. Para atribuir un valor al mensurando hacen falta modelo, calibración, correcciones y condiciones.

**Pista 1:** pregunta qué cantidad proporciona directamente la etapa de salida.

**Pista 2:** dibuja una frontera entre display y resultado; añade las operaciones necesarias para cruzarla.

**Recuperación:** analizar un ADC que entrega códigos para un sensor de temperatura con offset.

**Continuar cuando:** puede nombrar la indicación y el mensurando con unidades distintas sin contradicción.

### M2. “El nombre del analito o del órgano es el mensurando”

**Diagnóstico:** propiedad nominal usada como cantidad.

**Por qué falla:** “glucosa”, “corazón” o “temperatura corporal” no especifican cantidad, sistema, estado, localización ni tiempo.

**Pista 1:** completar la frase “cantidad de ___ en ___ bajo ___”.

**Pista 2:** comparar concentración, cantidad de sustancia y tasa de cambio.

**Recuperación:** especificar dos mensurandos diferentes relacionados con oxígeno.

**Continuar cuando:** la especificación produce una cantidad medible y no una etiqueta clínica.

### M3. “La cadena de hardware es el modelo de medición”

**Diagnóstico:** confusión entre ruta de señal y relación entre cantidades.

**Por qué falla:** los bloques no indican por sí solos cómo se infiere el mensurando, qué correcciones se aplican ni qué influencias importan.

**Pista 1:** señalar dónde están las variables y sus relaciones.

**Pista 2:** añadir una red paralela con entrada, salida, parámetros e influencias.

**Recuperación:** transformar una cadena de pesaje en un modelo con indicación, gravedad, calibración y corrección.

**Continuar cuando:** presenta dos diagramas distintos y explica su conexión.

### M4. “Repetibilidad demuestra ausencia de sesgo”

**Diagnóstico:** precisión confundida con veracidad.

**Por qué falla:** lecturas agrupadas pueden compartir el mismo desplazamiento sistemático.

**Pista 1:** imaginar un cero desplazado que no cambia entre repeticiones.

**Pista 2:** añadir una referencia externa y comparar el promedio.

**Recuperación:** dos series con igual dispersión y diferente offset.

**Continuar cuando:** identifica por separado dispersión, sesgo y incertidumbre.

### M5. “El instrumento es trazable”

**Diagnóstico:** propiedad del resultado atribuida al objeto.

**Por qué falla:** la trazabilidad depende del resultado, procedimiento, referencias, calibraciones, incertidumbres, tiempo y condiciones.

**Pista 1:** completar “el resultado ___ está relacionado con la referencia ___ mediante ___”.

**Pista 2:** localizar qué cambiaría si el instrumento se usa fuera del intervalo calibrado.

**Recuperación:** comparar dos resultados producidos por el mismo instrumento bajo condiciones distintas.

**Continuar cuando:** la afirmación tiene un resultado concreto como sujeto.

### M6. “Un certificado garantiza cualquier resultado futuro”

**Diagnóstico:** calibración pasada tratada como garantía universal.

**Por qué falla:** el certificado corresponde a condiciones, fecha, intervalo y estado determinados; la medición posterior añade otras contribuciones.

**Pista 1:** separar el resultado de calibración del resultado de uso.

**Pista 2:** identificar transporte, deriva, configuración, operador, entorno y modelo.

**Recuperación:** auditar un instrumento calibrado usado fuera de rango.

**Continuar cuando:** documenta los enlaces entre calibración y medición posterior.

### M7. “Trazable significa apto para cualquier decisión”

**Diagnóstico:** trazabilidad confundida con fitness for purpose.

**Por qué falla:** una cadena válida puede conducir a una incertidumbre demasiado grande para la necesidad concreta.

**Pista 1:** comparar incertidumbre con la diferencia que la decisión necesita resolver.

**Pista 2:** formular una incertidumbre objetivo y un intervalo de uso.

**Recuperación:** elegir entre dos métodos, uno trazable pero insuficiente para discriminar el umbral del caso.

**Continuar cuando:** justifica aptitud con necesidad, incertidumbre, intervalo y riesgo.

### M8. “Una señal limpia demuestra origen fisiológico”

**Diagnóstico:** apariencia de señal usada como evidencia causal.

**Por qué falla:** interferencia, simulación, saturación, filtrado o artefacto pueden producir formas plausibles.

**Pista 1:** preguntar qué evidencia conecta la forma de onda con el fenómeno.

**Pista 2:** revisar adquisición, referencia, sincronización, controles y metadatos.

**Recuperación:** comparar una señal fisiológica y una señal sintética sin etiquetas.

**Continuar cuando:** solicita evidencia de procedencia y cadena, no solo morfología.

## Contrato de feedback en la futura implementación

Cada respuesta evaluada debe producir un objeto con:

```text
diagnosed_misconception
why_the_reasoning_fails
first_hint
second_hint
source_or_section_to_review
different_recovery_problem
objective_continue_criterion
```

No se aceptará como feedback:

- mostrar únicamente la respuesta correcta;
- indicar “revisa la teoría” sin localizador;
- repetir la definición;
- cambiar solo los números del mismo problema;
- aprobar una respuesta que use terminología correcta pero relaciones equivocadas.

## Gate de autoría

La evaluación puede incorporarse a la unidad cuando:

1. todos los distractores correspondan a misconceptions documentadas;
2. las respuestas correctas puedan justificarse con fuentes directas;
3. las rúbricas tengan errores críticos y criterios observables;
4. cada error crítico tenga un problema de recuperación distinto;
5. el caso de transferencia no aparezca resuelto en la teoría;
6. ninguna tarea solicite interpretación clínica;
7. al menos una persona del perfil objetivo complete una prueba cognitiva de instrucciones y feedback.
