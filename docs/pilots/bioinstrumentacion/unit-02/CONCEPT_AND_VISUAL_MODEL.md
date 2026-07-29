# Modelo conceptual y visual · Bioinstrumentación Unidad 2

## Pregunta de diseño

¿Cómo mostrar simultáneamente **qué transforma el transductor**, **cómo se comporta en estado estacionario** y **cómo responde en el tiempo**, sin convertir esas tres vistas en una sola propiedad?

## Plano 1 — Función en la cadena

```text
cantidad de entrada
        ↓
interfaz y transferencia de energía
        ↓
elemento sensible
        ↓
transducción
        ↓
cantidad de salida
        ↓
acondicionamiento posterior
```

La frontera debe aparecer dibujada. El sensor es el elemento directamente afectado. El transductor es el dispositivo que establece una relación especificada entre una cantidad de entrada y una cantidad de salida. El acondicionamiento no se incorporará al sensor por conveniencia narrativa.

## Plano 2 — Caracterización estática

La curva entrada–salida debe mostrar:

- variables y unidades en ambos ejes;
- intervalo medido y regiones no evaluadas;
- sensibilidad local como pendiente en un punto;
- sensibilidad promedio como secante en un intervalo;
- offset respecto de una condición de referencia;
- región de saturación;
- trayectorias ascendente y descendente para histéresis;
- modelo de referencia usado para hablar de no linealidad.

La gráfica no debe sugerir que una curva suave es exacta ni que una pendiente grande es superior.

## Plano 3 — Caracterización dinámica

Para un modelo didáctico de primer orden:

```text
τ dy/dt + y = Kx
```

Toda aparición de esta ecuación debe declarar:

- qué representan `x`, `y`, `K` y `τ`;
- unidades;
- condición inicial;
- tipo de estímulo;
- intervalo de validez;
- efectos omitidos;
- criterio usado para medir asentamiento.

La constante de tiempo pertenece al modelo. El tiempo de respuesta al escalón pertenece a una definición operacional con límites especificados. No deben aparecer como etiquetas intercambiables.

## Plano 4 — Carga e influencias

Flechas laterales mostrarán interacciones bidireccionales:

- **eléctrica:** impedancia de entrada, excitación y conductores;
- **mecánica:** masa, rigidez, adhesión y geometría;
- **térmica:** capacidad, resistencia térmica, contacto y autocalentamiento;
- **óptica:** potencia incidente, geometría, absorción y luz ambiental.

La carga modifica el sistema observado o la cantidad disponible en la interfaz. No es solo un «error del sensor».

## Casos coordinados

### Termistor

Entrada: temperatura del elemento sensible. Salida primaria: resistencia. La curva estática es no lineal; la respuesta dinámica depende del intercambio térmico y del montaje.

### Galga extensométrica

Entrada: deformación transferida. Salida primaria: cambio relativo de resistencia. El puente y la excitación pertenecen a la lectura; fuerza o presión requieren modelo estructural adicional.

### Fotodiodo

Entrada: potencia radiante con espectro y geometría definidos. Salida primaria: corriente. Responsividad, corriente oscura, capacitancia y velocidad no representan una única escala de calidad.

## Errores visuales prohibidos

1. Sensor conectado directamente a una etiqueta clínica.
2. Entrada y salida sin cantidades ni unidades.
3. Curva estática usada para declarar respuesta temporal.
4. Histéresis dibujada como una nube aleatoria sin dirección de barrido.
5. Constante de tiempo rotulada como tiempo de respuesta universal.
6. Ancho de banda sin criterio de amplitud, fase o error permitido.
7. Hoja de datos de componente presentada como validación del sistema.

## Accesibilidad

El significado no dependerá solo del color. Se usarán posición, contorno, patrón, flechas y rótulos. Cada figura tendrá descripción textual equivalente.

## Criterio de aceptación

Un estudiante debe poder usar la figura para responder, sin memorizar una leyenda:

- qué cantidad afecta directamente al sensor;
- qué cantidad sale del transductor;
- dónde se define la sensibilidad;
- qué evidencia pertenece al régimen estático;
- qué parámetro pertenece al modelo dinámico;
- cómo la interfaz puede perturbar la medición;
- qué afirmaciones no pueden sostenerse desde una hoja de datos.
