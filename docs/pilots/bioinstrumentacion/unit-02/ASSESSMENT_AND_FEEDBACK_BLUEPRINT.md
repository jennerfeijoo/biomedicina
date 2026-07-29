# Evaluación y retroalimentación · Bioinstrumentación Unidad 2

## Secuencia de evaluación

### U2-A1 — Fronteras funcionales

Clasifica 16 elementos entre sensor, transductor, interfaz, acondicionamiento y salida. Dos cadenas deben redibujarse con fronteras alternativas para comprobar que la clasificación depende de la función y no de una etiqueta fija.

**Dominio:** al menos 13 clasificaciones coherentes y explicación correcta de las dos fronteras.

### U2-A2 — Auditoría de curvas estáticas

Cuatro curvas sintéticas contienen combinaciones de:

- sensibilidad variable;
- offset;
- saturación;
- histéresis;
- no linealidad respecto de un modelo declarado;
- ruido.

El estudiante debe diferenciar patrón observado, mecanismo plausible y prueba adicional necesaria.

### U2-A3 — Modelo dinámico de primer orden

A partir de entradas escalonadas y salidas sintéticas, se estima `τ`, se verifica el modelo y se comparan tiempos de asentamiento bajo límites especificados. Una entrada rápida muestra el error dinámico que la calibración estática no revela.

### U2-A4 — Revisión de carga

Cuatro afirmaciones cubren carga eléctrica, mecánica, térmica y óptica. La respuesta debe identificar ruta de interacción, cantidad perturbada, evidencia faltante y mitigación limitada.

### U2-A5 — Transferencia por selección multicriterio

Caso nuevo con tres transductores. La decisión usa rango, sensibilidad, selectividad, carga, dinámica, entorno y calidad de evidencia. Debe incluir una sección «lo que esta evidencia no demuestra».

## Banco de errores conceptuales y retroalimentación

| ID | Error conceptual | Pregunta discriminante | Recuperación |
|---|---|---|---|
| `sensor-equals-system` | El sensor contiene toda la cadena. | ¿Qué elemento está directamente afectado y cuáles transforman después? | Redibujar una cadena con fronteras. |
| `sensor-equals-transducer-always` | Sensor y transductor siempre son sinónimos. | ¿La pieza sensible produce por sí sola la cantidad de salida definida? | Comparar termistor desnudo y módulo de temperatura. |
| `higher-sensitivity-is-better` | Más pendiente implica mejor sensor. | ¿Qué sacrificios aparecen en rango, saturación, ruido y carga? | Seleccionar entre dos curvas con compromisos opuestos. |
| `sensitivity-equals-resolution` | Sensibilidad y resolución son lo mismo. | ¿Una pendiente alta permite distinguir cualquier cambio pequeño? | Combinar pendiente y cuantización en un problema distinto. |
| `static-calibration-covers-dynamics` | La curva estática describe cualquier señal. | ¿Dónde aparecen almacenamiento, retardo y condición inicial? | Comparar dos sensores con igual curva y distinto `τ`. |
| `response-time-equals-time-constant` | Tiempo de respuesta y `τ` son idénticos. | ¿Qué límites de asentamiento se usaron? | Calcular varios tiempos de asentamiento para el mismo `τ`. |
| `fast-means-accurate` | Rapidez demuestra exactitud. | ¿Qué evidencia existe sobre sesgo y selectividad? | Contrastar respuesta rápida desplazada y respuesta lenta sin desplazamiento. |
| `linearity-is-intrinsic-global` | Existe una linealidad única global. | ¿Respecto de qué modelo e intervalo? | Ajustar dos intervalos de la misma curva. |
| `hysteresis-is-random-noise` | El bucle es ruido. | ¿La diferencia depende de la dirección de barrido? | Reordenar datos preservando o destruyendo la trayectoria. |
| `loading-is-negligible` | El sensor no modifica el objeto. | ¿Qué energía o impedancia introduce la interfaz? | Analizar autocalentamiento y divisor cargado. |
| `datasheet-is-system-proof` | La hoja de datos valida la cadena. | ¿Coinciden montaje, condiciones y electrónica? | Auditar dos especificaciones no comparables. |
| `component-performance-is-clinical-utility` | Buen componente demuestra utilidad clínica. | ¿Qué población y decisión fueron evaluadas? | Clasificar evidencia como componente, sistema, uso o clínica. |

## Contrato de retroalimentación

Cada respuesta de recuperación debe contener:

1. error conceptual diagnosticado;
2. explicación de por qué falla el razonamiento;
3. primera pista sin revelar la solución;
4. segunda pista más específica;
5. sección o fuente a revisar;
6. problema de recuperación diferente;
7. criterio objetivo para continuar.

## Prohibiciones

- Retroalimentación reducida a «correcto/incorrecto».
- Aceptar «mejor sensor» sin requisitos priorizados.
- Llamar mecanismo a un patrón que no lo identifica.
- Usar números de fabricante sin condiciones.
- Calificar automáticamente argumentos abiertos mediante coincidencia de palabras.
- Presentar una simulación o selección de componente como validación clínica.

## Gate de autoría

La teoría completa continúa bloqueada hasta que:

- las fuentes dinámicas y de carga estén revisadas;
- las prácticas sintéticas tengan generadores y controles positivos/negativos;
- las rúbricas discriminen los doce errores conceptuales;
- una revisión disciplinar inicial examine modelos, unidades y límites;
- el curso permanezca `pending` y la publicación continúe bloqueada.
