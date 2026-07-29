# Modelo conceptual y visual — Bioinstrumentación, Unidad 1

**Estado:** preparación de autoría; no es una unidad desarrollada.

## Pregunta estructural

¿Cómo pasa un fenómeno biológico a convertirse en un resultado de medición defendible?

La unidad no debe presentar una cadena lineal simplificada como si el sensor capturara directamente una propiedad clínica. El modelo debe mostrar dos estructuras relacionadas pero distintas:

1. **ruta física y digital de la señal**;
2. **modelo de cantidades y evidencia que permite atribuir un resultado al mensurando**.

## Capas del modelo

### Capa 1 — Sistema biológico y fenómeno

Representa el cuerpo, tejido, fluido o proceso donde existe la cantidad de interés. Debe separar:

- objeto o sistema portador;
- fenómeno físico o fisiológico;
- cantidad que se pretende medir;
- condiciones de espacio, tiempo y estado.

Ejemplo correcto: diferencia de potencial entre dos sitios corporales definidos como función del tiempo.

Ejemplo incorrecto: “actividad del corazón” presentada como una cantidad suficientemente especificada.

### Capa 2 — Interacción de medición

Muestra que el sistema de medición interactúa con el objeto y puede perturbarlo. Según el caso, esta capa puede incluir:

- transferencia térmica;
- acoplamiento mecánico;
- contacto electrodo-piel;
- propagación óptica;
- toma o preparación de una muestra.

Esta capa impide que el sensor aparezca como observador transparente.

### Capa 3 — Sensor y transducción

Representa el elemento sensible y la conversión inicial. La Unidad 1 solo identifica su función; los mecanismos y modelos dinámicos se desarrollarán en la Unidad 2.

Debe quedar claro que la salida del sensor puede ser:

- resistencia;
- carga;
- tensión;
- corriente;
- desplazamiento;
- intensidad óptica;
- frecuencia;
- código.

Ninguna de estas salidas equivale automáticamente al mensurando.

### Capa 4 — Cadena de medición

Ruta única de señal formada por etapas funcionales:

> sensor → acondicionamiento → conversión → procesamiento → elemento de salida

Cada etapa debe declarar:

- tipo de entrada y salida;
- unidades o códigos;
- transformación aplicada;
- rango o dominio válido;
- metadatos necesarios;
- posibles saturaciones o pérdidas.

La cadena puede mostrarse como una trayectoria espacial continua. No debe contener todavía todas las relaciones del modelo de medición.

### Capa 5 — Indicación

Es la salida que proporciona el instrumento o sistema. Puede ser un voltaje, un número, una secuencia de muestras o un código. Visualmente debe situarse antes del resultado y tener una forma distinta.

Regla gráfica:

- **indicación:** objeto puntual o secuencia producida por el sistema;
- **resultado:** paquete de información atribuido al mensurando.

### Capa 6 — Modelo de medición

Debe aparecer como una red o espacio paralelo a la cadena física. Conecta:

- mensurando como cantidad de salida;
- indicaciones;
- cantidades de entrada;
- parámetros de calibración;
- correcciones;
- magnitudes de influencia;
- supuestos y dominio de validez.

Forma general introductoria:

> resultado del mensurando = función de indicaciones, cantidades de entrada, correcciones y parámetros del modelo

La unidad no necesita derivar todavía propagación de incertidumbre, pero sí mostrar que el resultado se infiere mediante un modelo.

### Capa 7 — Resultado de medición

Se representa como un expediente compacto que contiene:

- identidad del mensurando;
- valor o conjunto de valores;
- unidad o escala de referencia;
- incertidumbre o declaración de credibilidad disponible;
- condiciones y método;
- fecha, versión y metadatos relevantes;
- límites de interpretación.

No debe representarse solo como un número grande en pantalla.

### Capa 8 — Trazabilidad metrológica

Debe aparecer separada de la ruta de señal. Es una red de referencias y calibraciones conectada al resultado mediante:

- referencia especificada;
- cadena documentada;
- resultados de calibración;
- incertidumbre aportada por cada enlace;
- estado temporal y condiciones.

La red se conecta al **resultado**, no se dibuja como una etiqueta adherida al instrumento.

### Capa 9 — Aptitud para el uso

Última capa de decisión. Recibe:

- resultado;
- incertidumbre;
- intervalo de validez;
- necesidad del usuario;
- consecuencias de decisiones erróneas.

Debe mostrarse como evaluación contextual. No es sinónimo de trazabilidad ni utilidad clínica demostrada.

## Magnitudes de influencia

Las influencias entran lateralmente a las relaciones que modifican. No se dibujan como ruido decorativo alrededor del sistema.

Ejemplos:

- temperatura ambiente modifica la relación entre temperatura del objeto, transferencia y sensor;
- movimiento modifica el acoplamiento electrodo-piel y la indicación;
- posición corporal y altura relativa modifican el contexto de una medición de presión;
- tiempo de contacto modifica el estado térmico del sensor.

Cada influencia debe responder:

1. ¿qué relación modifica?;
2. ¿en qué dirección o mecanismo?;
3. ¿se mide, controla, corrige o se incorpora a la incertidumbre?;
4. ¿en qué intervalo importa?

## Tres recorridos de zoom para la futura visualización

### Recorrido A — Del fenómeno a la señal

1. plano general del sistema biológico;
2. acercamiento a la cantidad y sus condiciones;
3. interacción con el sensor;
4. salida física inicial;
5. cadena de acondicionamiento y conversión.

Objetivo: desmontar la idea de medición directa.

### Recorrido B — De la indicación al resultado

1. indicación cruda;
2. cantidades de entrada y metadatos;
3. modelo de medición;
4. correcciones e influencias;
5. resultado con incertidumbre y límites.

Objetivo: mostrar que un número de display no es el producto final completo.

### Recorrido C — Del resultado a la trazabilidad y al uso

1. resultado específico;
2. cadena de calibraciones y referencia;
3. contribuciones de incertidumbre;
4. necesidad de medición;
5. juicio de aptitud para el uso.

Objetivo: separar trazabilidad, calidad del resultado y utilidad contextual.

## Convenciones visuales obligatorias

- La ruta de señal será continua y unidireccional.
- El modelo de medición será una red de cantidades, no una segunda cadena de hardware.
- Las influencias usarán entradas laterales con punto de acción explícito.
- Las correcciones se mostrarán como operaciones en el modelo, no como borrado de error.
- La incertidumbre acompañará al resultado y a los enlaces de trazabilidad.
- La aptitud para el uso estará después del resultado, nunca antes.
- La descripción textual permitirá comprender la figura sin depender del color.

## Errores visuales prohibidos

- conectar el sensor directamente a “diagnóstico”, “salud” o “enfermedad”;
- hacer que una indicación digital y el mensurando tengan la misma etiqueta;
- representar trazabilidad como un sello de calidad pegado al instrumento;
- dibujar incertidumbre como ruido aleatorio únicamente;
- ocultar las condiciones de medición;
- usar flechas decorativas sin variable, transformación o función;
- mezclar referencia eléctrica, referencia metrológica y referencia clínica.

## Criterio de aceptación

El modelo visual se considera apto para autoría cuando una persona puede señalar, sin leer el texto principal:

1. qué cantidad se pretende medir;
2. dónde ocurre la interacción;
3. cuál es la ruta de señal;
4. cuál es la indicación;
5. qué elementos forman el modelo;
6. dónde entran las influencias;
7. qué constituye el resultado;
8. por qué la trazabilidad pertenece al resultado;
9. por qué la aptitud para el uso requiere una evaluación adicional.
