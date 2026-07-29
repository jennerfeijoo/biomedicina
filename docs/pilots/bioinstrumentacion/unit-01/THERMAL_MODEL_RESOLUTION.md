# Resolución del modelo térmico sintético — Bioinstrumentación, Unidad 1

**Estado:** resuelto para diseñar el dataset; pendiente de revisión disciplinar humana.  
**Alcance:** simulación didáctica de una cadena de medición, no modelo fisiológico validado.

## Problema que debe enseñar

Un sensor de contacto no observa necesariamente la temperatura superficial no perturbada. El contacto, la fijación, la transferencia de calor y el ambiente pueden modificar la temperatura local, mientras que el sensor posee una respuesta dinámica propia.

La práctica debe separar cuatro variables:

- `T_u(t)`: temperatura superficial no perturbada;
- `T_d(t)`: temperatura superficial perturbada por el sistema de medición;
- `T_s(t)`: temperatura del elemento sensible;
- `y(t)`: indicación simulada después de offset y ruido.

## Modelo autorizado

### Perturbación de contacto

```text
T_d(t) = T_u(t) + b_contact(t)
```

`b_contact(t)` representa de manera sintética la perturbación local asociada con contacto, fijación y gradiente térmico. No se interpreta como parámetro fisiológico universal.

### Dinámica de primer orden

```text
dT_s/dt = [T_d(t) - T_s(t)] / tau
```

`tau > 0` es una constante de tiempo didáctica. Bajo una entrada escalón constante, sin ruido ni no linealidades, el sensor se aproxima exponencialmente a `T_d`.

### Indicación

```text
y(t) = T_s(t) + b_cal + epsilon(t)
```

`b_cal` representa offset de calibración y `epsilon(t)` ruido sintético. Ambos deben mantenerse separados del retardo dinámico y de la perturbación de contacto.

## Propiedades que el código debe verificar

1. Con entrada constante, `T_s` converge hacia `T_d`.
2. Tras una constante de tiempo, la respuesta ideal alcanza aproximadamente 63,2 % del cambio total.
3. Tras cinco constantes de tiempo, supera 99 % del cambio total en el modelo ideal.
4. El modelo ideal de primer orden no produce sobreimpulso.
5. Cambiar `tau` modifica la rapidez, no el valor estacionario ideal.
6. Cambiar `b_cal` desplaza la indicación sin modificar la dinámica interna.
7. Cambiar `b_contact` modifica la superficie perturbada y demuestra que el sistema puede alterar el fenómeno local.

## Escenarios sintéticos

### Escenario 1 — respuesta ideal

- escalón conocido en `T_d`;
- `b_contact = 0`;
- `b_cal = 0`;
- `epsilon = 0`.

Objetivo: verificar la definición operacional de `tau`.

### Escenario 2 — perturbación de contacto

`T_u` permanece fija y `b_contact` cambia al colocar el sensor. El estudiante debe explicar por qué una indicación estable puede diferir de la superficie no perturbada.

### Escenario 3 — misma calibración, distinta dinámica

Dos sensores comparten offset y ganancia estáticos, pero tienen constantes de tiempo diferentes. El estudiante debe identificar cuándo el muestreo ocurre antes del estado estacionario.

### Escenario 4 — offset frente a retardo

Se combinan un offset constante y una respuesta lenta. La evaluación debe impedir que ambos errores se corrijan con una única operación no justificada.

### Escenario 5 — gradiente ambiente-superficie

El sesgo de contacto cambia con un gradiente sintético. No se asignan valores universales ni se afirma equivalencia con piel humana.

## Política de parámetros

Los parámetros se generarán mediante una semilla fija y rangos etiquetados como **didácticos**. No se tomarán valores de pacientes, dispositivos comerciales ni artículos para presentarlos como distribuciones fisiológicas.

Cada dataset debe conservar:

- semilla;
- ecuaciones;
- unidades;
- paso temporal;
- `tau`;
- offsets y ruido;
- escenario;
- limitaciones;
- versión del generador.

## Fuentes autorizadas

- MacRae et al., *A Thermal Skin Model for Comparing Contact Skin Temperature Sensors and Assessing Measurement Errors* (2021), DOI `10.3390/s21144906`.
- *Temperature Dependence of the Dynamic Parameters of Contact Thermometers* (2019), para la representación resistencia-capacidad y la constante de tiempo.

La primera fuente distingue temperatura no perturbada, perturbada y del sensor. La segunda respalda el uso limitado de una aproximación dinámica de primer orden. Ninguna valida parámetros universales para piel o dispositivos.

## Exclusiones

La Unidad 1 no modelará:

- perfusión;
- evaporación;
- conducción espacial distribuida;
- radiación detallada;
- geometría anatómica;
- estimación de temperatura central;
- decisiones clínicas.

## Criterio de aceptación

El modelo queda listo para implementación cuando las pruebas automáticas confirman las propiedades anteriores, las cuatro variables permanecen separadas y la documentación declara explícitamente que se trata de una simulación conceptual.
