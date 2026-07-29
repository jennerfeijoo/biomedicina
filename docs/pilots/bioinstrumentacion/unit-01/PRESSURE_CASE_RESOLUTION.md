# Resolución del caso de presión — Bioinstrumentación, Unidad 1

**Estado:** resuelto para autoría controlada; pendiente de revisión disciplinar humana.  
**Propósito:** impedir que “presión arterial” se trate como una única cantidad independiente del sitio, método, referencia y tiempo.

## Decisión central

La unidad presentará tres resultados de medición conceptualmente distintos:

1. una presión intravascular en un sitio arterial especificado y referida al nivel del transductor;
2. estimaciones auscultatorias de presión sistólica y diastólica en la arteria braquial bajo condiciones estandarizadas;
3. estimaciones oscilométricas generadas a partir de oscilaciones del manguito y un algoritmo del dispositivo.

No se enseñará que estos tres resultados sean idénticos o intercambiables. La comparación entre ellos exige declarar el mensurando, el sitio, la referencia, la dinámica, el procedimiento y la incertidumbre.

## Caso A — Presión intraarterial

### Especificación mínima

- cantidad: presión intravascular;
- sitio: arteria y localización anatómica especificadas;
- referencia: nivel del transductor y referencia de cero documentados;
- tiempo: forma de onda o estadístico definido sobre un intervalo;
- cadena: interfaz hidráulica, transductor, acondicionamiento, conversión y registro;
- resultado: valor o serie temporal con unidades, condiciones, transformaciones y limitaciones.

### Límite didáctico

La Unidad 1 no describe inserción, conexión, nivelación clínica ni mantenimiento de sistemas invasivos. El caso existe solo para mostrar que la presión depende del sitio, de la referencia y de la dinámica de la cadena.

## Caso B — Estimación auscultatoria

El manguito modifica temporalmente el flujo arterial. Los eventos acústicos observados durante la deflación se utilizan para estimar presión sistólica y diastólica. El resultado depende de postura, brazo, nivel respecto del atrio, dimensiones y colocación del manguito, velocidad del procedimiento, repetición y documentación.

La unidad debe decir **estimación auscultatoria**, no “presión directa”.

## Caso C — Estimación oscilométrica

El sistema registra oscilaciones de presión en el manguito. Un algoritmo transforma esas señales en estimaciones reportadas. La señal del manguito es una indicación intermedia; la presión sistólica y diastólica reportadas son resultados dependientes del modelo y del dispositivo.

Dos dispositivos o algoritmos no se consideran intercambiables por compartir unidades o apariencia de salida.

## Magnitudes de influencia obligatorias

- postura;
- altura del brazo o del transductor respecto de la referencia;
- sitio anatómico;
- dimensiones y colocación del manguito;
- movimiento y conversación;
- intervalo entre mediciones;
- variabilidad temporal;
- estado, calibración y algoritmo del sistema.

## Errores que la evaluación debe discriminar

- “La presión del manguito es la presión arterial sistólica”.
- “Una salida de 120/80 identifica completamente el mensurando”.
- “La presión intraarterial y la estimación braquial son el mismo resultado”.
- “PPG o tiempo de tránsito miden directamente presión”.
- “Un resultado plausible autoriza interpretación clínica”.

## Producto esperado del estudiante

Para cada método, el estudiante debe producir:

1. especificación del mensurando;
2. cadena física y digital;
3. modelo de medición cualitativo;
4. magnitudes de influencia;
5. resultado defendible;
6. afirmaciones que no pueden realizarse.

## Fuentes autorizadas

- AHA, *Measurement of Blood Pressure in Humans* (2019), DOI `10.1161/HYP.0000000000000087`.
- AHA/ACC, guideline de presión arterial en adultos (2025), DOI `10.1161/HYP.0000000000000249`.
- AHA, statement sobre dispositivos sin manguito (2026), DOI `10.1161/HYP.0000000000000254`.

Los localizadores y límites están registrados en `data/source_registry/bioinstrumentacion-unit-01-blockers.json`.

## Criterio de aceptación

El caso está listo para autoría cuando ningún diagrama o pregunta:

- mezcla sitio arterial con método;
- presenta una estimación como medición directa;
- omite la referencia espacial;
- elimina el algoritmo de la cadena oscilométrica;
- salta de desempeño de medición a utilidad clínica.
