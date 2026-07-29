# Complemento del banco de misconceptions — Bioinstrumentación, Unidad 1

El primer ciclo de CI detectó que cinco errores evaluados no tenían todavía una ficha explícita. Este documento completa su feedback; no elimina las pruebas que los discriminan.

## M9. “La señal registrada es el resultado completo”

**Diagnóstico:** secuencia de valores confundida con resultado de medición.

**Por qué falla:** una señal no especifica por sí sola el mensurando, las unidades, las condiciones, el modelo, la incertidumbre, la procedencia ni los límites de interpretación.

**Pista 1:** enumera qué información desaparece al conservar solo una columna de valores.

**Pista 2:** añade mensurando, tiempo, unidad, cadena, transformaciones y metadatos al objeto entregado.

**Recuperación:** reconstruir el significado de una serie sintética cuya escala, frecuencia y canal se entregan por separado.

**Continuar cuando:** distingue señal, indicación, valor medido y resultado sin usar su formato digital como criterio.

## M10. “El nombre habitual especifica el mensurando”

**Diagnóstico:** etiqueta coloquial tratada como especificación completa.

**Por qué falla:** expresiones como temperatura corporal o presión arterial pueden referirse a cantidades diferentes según localización, intervalo temporal, estado, método y uso previsto.

**Pista 1:** pregunta dónde, cuándo y sobre qué sistema se atribuirá el valor.

**Pista 2:** construye dos mensurandos incompatibles que compartan la misma etiqueta habitual.

**Recuperación:** diferenciar saturación periférica de oxígeno, presión parcial de oxígeno y contenido arterial de oxígeno sin interpretar clínicamente los valores.

**Continuar cuando:** la especificación permite decidir qué observaciones son pertinentes y cuáles no.

## M11. “El método es el mensurando”

**Diagnóstico:** procedimiento o dispositivo confundido con cantidad pretendida.

**Por qué falla:** es posible medir una misma cantidad mediante principios distintos; en otros casos, el procedimiento forma parte necesaria de una definición operacional. La relación debe explicitarse, no asumirse.

**Pista 1:** imagina reemplazar el dispositivo por otro principio y pregunta qué cantidad seguiría siendo el objetivo.

**Pista 2:** identifica si el método modifica la definición o solo la realización de la medición.

**Recuperación:** comparar temperatura por contacto y estimación radiométrica, declarando qué mensurando pretende cada caso.

**Continuar cuando:** separa cantidad, procedimiento y resultado dependiente del método.

## M12. “Los metadatos son accesorios”

**Diagnóstico:** valores almacenados interpretados sin escala, reloj, canales, versión o procedencia.

**Por qué falla:** sin metadatos, una secuencia puede perder su unidad, orden temporal, identidad de canal y relación con la cadena de adquisición.

**Pista 1:** elimina la frecuencia de muestreo y determina qué afirmaciones temporales sobreviven.

**Pista 2:** elimina ganancia y baseline y determina si los códigos conservan significado físico.

**Recuperación:** auditar dos archivos numéricamente idénticos con diccionarios de datos incompatibles.

**Continuar cuando:** identifica qué metadatos son necesarios para cada inferencia y no solo enumera campos.

## M13. “Conocer definiciones demuestra transferencia”

**Diagnóstico:** uso de palabras clave confundido con capacidad para construir o auditar una medición nueva.

**Por qué falla:** una respuesta puede repetir mensurando, indicación y trazabilidad mientras conserva relaciones incorrectas entre esos conceptos.

**Pista 1:** resuelve un caso nuevo sin recibir la lista de categorías.

**Pista 2:** justifica cada relación mediante una evidencia o una limitación observable.

**Recuperación:** analizar una plataforma de fuerza plantar simulada después de estudiar ejemplos térmicos y bioeléctricos.

**Continuar cuando:** obtiene al menos cuatro de cinco criterios de transferencia y no comete ningún error crítico.

## Resultado del hallazgo

El banco estructurado contiene ahora trece misconceptions. Todas las referencias de las evaluaciones apuntan a identificadores existentes, y cada nuevo error tiene diagnóstico, explicación, pistas, recuperación y criterio de continuación.
