# Dossier de fuentes — Bioinstrumentación, Unidad 1

**Unidad:** Mensurando, sistema de medición y cadena de trazabilidad  
**Estado:** preparación de autoría; la unidad aún no está desarrollada  
**Fecha de consulta:** 29 de julio de 2026

## Propósito

Este dossier limita qué afirmaciones pueden entrar en la Unidad 1 y con qué alcance. No sustituye las fuentes originales. Durante la autoría, cada definición, relación formal y afirmación sobre trazabilidad deberá enlazarse con un localizador preciso.

## Jerarquía de evidencia

1. **JCGM/BIPM:** autoridad terminológica y metodológica para metrología.
2. **NIST:** interpretación institucional y checklist operativo de trazabilidad, coherente con el VIM.
3. **PhysioNet:** fuente de datos fisiológicos abiertos y metadatos para una práctica reproducible; no es fuente de terminología metrológica ni de interpretación clínica.
4. **Cursos universitarios:** referencias de cobertura y pedagogía, no autoridades para definiciones o requisitos.

## Afirmaciones autorizadas

### 1. Mensurando

**Afirmación autorizada:** el mensurando es la cantidad que se pretende medir. Su especificación requiere identificar la clase de cantidad, el fenómeno, cuerpo o sustancia que la porta y el estado relevante. El sistema y las condiciones de medición pueden modificar el fenómeno, de modo que la cantidad efectivamente medida no coincida sin corrección con la cantidad pretendida.

**Fuentes y localizadores:**

- VIM3, entrada 2.3, definición y notas 1, 3 y 4.
- JCGM GUM-6:2020, cláusulas 6.1–6.4.

**Uso en la unidad:** checklist para especificar mensurandos; contraste entre temperatura cutánea, temperatura del sensor y estimación de temperatura central; distinción entre una sustancia y una cantidad de esa sustancia.

**Límite:** no enseñar que existe una única especificación universal. La especificación depende del uso previsto y de las condiciones bajo las que el resultado debe ser válido.

### 2. Medición y resultado

**Afirmación autorizada:** una medición es un proceso experimental o computacional que obtiene valores razonablemente atribuibles a una cantidad. Un resultado de medición no se reduce necesariamente a un número: comprende valores atribuidos al mensurando y la información relevante disponible, normalmente un valor medido y su incertidumbre.

**Fuentes y localizadores:**

- VIM3, entradas 2.1, 2.9 y 2.10.
- JCGM GUM-1:2023, cláusulas 2.1 y 3.1–3.5.

**Uso en la unidad:** separar lectura, valor medido y resultado; exigir condiciones, unidad, metadatos e incertidumbre introductoria.

**Límite:** la Unidad 1 introduce incertidumbre como componente del resultado, pero no desarrolla todavía su evaluación cuantitativa completa.

### 3. Indicación

**Afirmación autorizada:** una indicación es el valor de cantidad proporcionado por un instrumento o sistema. La indicación y la cantidad que se está midiendo no tienen que ser cantidades del mismo tipo.

**Fuente y localizador:** VIM3, entrada 4.1 y notas.

**Uso en la unidad:** interpretar un número de ADC, un voltaje, una posición de aguja o un código como salida instrumental, no como equivalentes automáticos del mensurando.

**Límite:** no usar “señal”, “indicación” y “valor medido” como sinónimos.

### 4. Sistema y cadena de medición

**Afirmación autorizada:** un sistema de medición es el conjunto organizado de instrumentos y otros dispositivos que genera información para obtener valores medidos. Una cadena de medición es una ruta única de señal desde el sensor hasta un elemento de salida.

**Fuentes y localizadores:**

- VIM3, entrada 3.2.
- VIM3, entrada 3.10.

**Uso en la unidad:** dibujar fronteras del sistema y rutas de señal; mostrar que un sistema puede contener varias cadenas, referencias, fuentes de alimentación, software y metadatos.

**Límite:** la cadena de medición no es el modelo de medición. Un diagrama de bloques de hardware puede omitir las cantidades y relaciones necesarias para inferir el mensurando.

### 5. Modelo de medición

**Afirmación autorizada:** el modelo de medición expresa una relación matemática o algorítmica entre las cantidades conocidas que intervienen. Su desarrollo comienza con la especificación del mensurando, continúa con el principio de medición, identifica efectos de la implementación y evalúa la adecuación del modelo.

**Fuentes y localizadores:**

- VIM3, entradas 2.48, 2.50 y 2.52.
- JCGM GUM-6:2020, cláusulas 5–10, especialmente 5.3, 6.2, 7.1 y 9.1.

**Uso en la unidad:** representar modelos cualitativos y algebraicos simples; identificar indicaciones, cantidades de entrada, influencias, correcciones y salida.

**Límite:** no presentar un modelo como verdadero fuera del intervalo y las condiciones en que fue desarrollado y evaluado.

### 6. Magnitudes de influencia

**Afirmación autorizada:** una magnitud de influencia puede afectar la relación entre la indicación y el resultado sin ser la cantidad pretendida en la medición directa.

**Fuente y localizador:** VIM3, entrada 2.52 y ejemplos.

**Uso en la unidad:** temperatura ambiente, tiempo de contacto, posición de electrodos, movimiento, altura relativa o presión de contacto.

**Límite:** no convertir toda variable contextual en magnitud de influencia sin explicar qué relación modifica.

### 7. Trazabilidad metrológica

**Afirmación autorizada:** la trazabilidad metrológica es una propiedad de un resultado de medición mediante la cual puede relacionarse con una referencia por una cadena documentada e ininterrumpida de calibraciones, cada una contribuyendo a la incertidumbre. No es una propiedad universal del instrumento, laboratorio o certificado. Tampoco garantiza por sí sola una incertidumbre adecuada ni ausencia de equivocaciones.

**Fuentes y localizadores:**

- VIM3, entrada 2.41 y notas 2–5.
- NIST TN 2156, secciones 3.2, 5.1.1, 5.1.3, 5.1.7 y 5.2.1.

**Uso en la unidad:** auditoría de afirmaciones como “equipo trazable” o “calibrado por NIST”; checklist de resultado, referencia, cadena, incertidumbre, procedimiento y estado del sistema.

**Límite:** no enseñar la frase “trazable a NIST” sin especificar la referencia y la cadena concreta.

### 8. Aptitud para el uso

**Afirmación autorizada:** la trazabilidad no demuestra automáticamente que un resultado sea adecuado para una decisión. La aptitud requiere considerar la necesidad de medición, el intervalo, la incertidumbre, el modelo, las condiciones y los riesgos de decisión.

**Fuentes y localizadores:**

- VIM3, entrada 2.41, nota 5.
- NIST Policy on Metrological Traceability, principio 5.
- JCGM GUM-1:2023, cláusulas 2.3–2.5 y 3.5.

**Uso en la unidad:** contrastar un resultado trazable pero demasiado incierto con otro adecuado para una necesidad definida.

**Límite:** no convertir la Unidad 1 en una unidad de evaluación de conformidad; ese desarrollo pertenece a unidades posteriores.

## Fuente de datos para la práctica

### MIT-BIH Arrhythmia Database, PhysioNet, versión 1.0.0

Se autoriza usar un segmento únicamente para estudiar:

- canales y unidades;
- frecuencia de muestreo;
- resolución y rango documentados;
- ganancia y conversión entre valores almacenados y magnitud física;
- identificador, versión y licencia;
- qué información no puede inferirse del archivo.

No se autoriza usar el dataset para enseñar diagnóstico, clasificación de arritmias o decisiones clínicas dentro de esta unidad.

## Afirmaciones prohibidas durante la autoría

- “El sensor mide directamente la salud cardíaca, la fiebre o la presión clínica”.
- “La lectura del display es el mensurando”.
- “Una señal digital es el resultado completo”.
- “Un instrumento calibrado produce automáticamente resultados trazables”.
- “Trazable significa exacto, correcto o apto para cualquier uso”.
- “Una curva limpia demuestra que la señal es fisiológica”.
- “La incertidumbre es solo la desviación estándar de lecturas repetidas”.

## Brechas que permanecen abiertas

1. Revisión disciplinar del tratamiento de presión arterial no invasiva, evitando introducir estándares o algoritmos no consultados.
2. Revisión de un especialista en metrología para el checklist de trazabilidad y el lenguaje de aptitud para el uso.
3. Confirmación del registro concreto de PhysioNet que se usará y de todos sus metadatos antes de escribir código.
4. Selección de una fuente abierta adicional para un caso no eléctrico, preferiblemente temperatura o fuerza, sin depender de documentación comercial.

## Criterio de cierre del dossier

El dossier puede considerarse suficiente para iniciar la redacción cuando:

- cada afirmación central tenga fuente directa y localizador;
- el revisor pueda reconstruir la diferencia entre mensurando, indicación, valor medido y resultado;
- los casos biomédicos no excedan la evidencia;
- la práctica tenga versión, licencia, diccionario de datos y límites explícitos;
- las brechas abiertas no sean necesarias para corregir las evaluaciones de la unidad.
