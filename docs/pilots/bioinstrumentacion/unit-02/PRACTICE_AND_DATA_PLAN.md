# Plan de prácticas y datos · Bioinstrumentación Unidad 2

## Principio operativo

Las prácticas deben demostrar propiedades de transducción sin adquirir datos de personas ni depender de hardware clínico. Los datos serán sintéticos o procederán de documentación pública de componentes con modelo, versión, condiciones y localizador registrados.

## U2-P1 — Banco sintético de características estáticas

### Datos

Se generarán curvas deterministas con:

- entrada creciente y decreciente;
- relación lineal local y no lineal global;
- offset;
- saturación;
- zona muerta;
- histéresis dependiente de trayectoria;
- ruido añadido con semilla fija.

### Tareas

1. Calcular sensibilidad local y promedio con unidades.
2. Identificar el intervalo en que una aproximación lineal cumple una tolerancia definida.
3. Separar patrón observable de mecanismo causal.
4. Proponer una prueba adicional para distinguir histéresis, deriva y ruido.

### Controles automáticos previstos

- la sensibilidad analítica coincide con la numérica en puntos de control;
- la región de saturación reduce la pendiente;
- invertir la trayectoria conserva el bucle de histéresis;
- eliminar la memoria del generador destruye el bucle;
- el mismo seed produce hash idéntico.

## U2-P2 — Respuesta dinámica de primer orden

### Modelo

```text
τ dy/dt + y = Kx
```

Se usarán entradas escalonadas, rampas y cambios más rápidos que la escala temporal del modelo.

### Tareas

1. Estimar `K` y `τ` desde datos sintéticos.
2. Calcular tiempo de asentamiento para límites explícitos.
3. Mostrar que distintos criterios producen distintos tiempos de respuesta.
4. Comparar error dinámico para entradas lentas y rápidas.
5. Inspeccionar residuos antes de aceptar el modelo.

### Controles automáticos previstos

- solución analítica y solución discreta coinciden dentro de tolerancia;
- a una constante de tiempo, la salida ideal alcanza aproximadamente 63,2 % del cambio;
- el estimador recupera `τ` dentro de una tolerancia declarada;
- un fixture de segundo orden no debe aprobar el gate de primer orden cuando los residuos muestran estructura;
- la calibración estática puede coincidir aunque las respuestas dinámicas difieran.

## U2-P3 — Auditoría comparativa de hojas de datos

### Componentes iniciales

- termistor NTC Vishay;
- galga extensométrica documentada por NI;
- fotodiodo PIN Hamamatsu.

### Extracción obligatoria

| Campo | Requisito |
|---|---|
| modelo | identificador exacto |
| cantidad de entrada | nombre y unidad |
| cantidad de salida | nombre y unidad |
| sensibilidad o relación | con condición e intervalo |
| dinámica | parámetro y criterio documentado |
| influencias | temperatura, montaje, polarización u otras |
| límites | máximos, rango o condiciones nominales |
| procedencia | URL, fecha y localizador |

### Tareas

- marcar propiedades que no son directamente comparables;
- detectar cifras sin condiciones suficientes;
- separar componente, cadena y uso previsto;
- redactar una decisión limitada y una lista de evidencia faltante.

## Gobierno de datos

- no se versionan datos humanos;
- no se registran nombres, identificadores o información clínica;
- los datasets generados no se consideran observaciones fisiológicas;
- las hojas de datos se citan, no se redistribuyen íntegramente;
- cada salida sintética incluye parámetros, seed, versión y hash;
- los artefactos temporales de CI no se incorporan al repositorio.

## Frontera de seguridad

No se conectan sensores a personas, animales, muestras o equipos clínicos. No se construyen circuitos energizados para partes aplicadas. No se emiten interpretaciones diagnósticas ni recomendaciones clínicas.

## Criterio antes de implementación

La implementación queda bloqueada hasta seleccionar:

1. ecuaciones exactas del generador estático;
2. tolerancias y controles negativos;
3. modelo dinámico y método de estimación;
4. componentes exactos y condiciones comparables;
5. revisión disciplinar de carga, respuesta temporal y límites de inferencia.
