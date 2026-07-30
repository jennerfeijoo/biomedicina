# Preparación autoral — Bioinstrumentación Unidad 4

## Unidad

**Conversión y procesamiento de señales biomédicas**

La unidad conecta el acondicionamiento analógico con la representación digital. Su eje no es memorizar una frecuencia de muestreo o un número de bits, sino justificar qué información debe conservarse, qué errores pueden introducirse y qué evidencia permite aceptar una cadena de digitalización.

## Pregunta central

¿Cómo convertir una señal biomédica analógica en datos digitales preservando la información relevante y manteniendo explícitos los límites de muestreo, cuantización, sincronización, aislamiento y comunicación?

## Resultados previstos

- `U4-LO1`: relacionar banda, filtro anti-alias y frecuencia de muestreo;
- `U4-LO2`: interpretar rango, LSB, cuantización, saturación, bits nominales y ENOB;
- `U4-LO3`: diseñar una cadena trazable de digitalización;
- `U4-LO4`: distinguir aislamiento, comunicación, sincronización e integridad;
- `U4-LO5`: diagnosticar fallos digitales mediante pruebas discriminantes.

## Prácticas planificadas

- `U4-P1`: aliasing y filtro anti-alias con señales sintéticas;
- `U4-P2`: presupuesto de rango, cuantización y saturación de un ADC ideal;
- `U4-P3`: integridad temporal y pérdida de muestras en una cadena multicanal.

Todas las prácticas permanecen sin implementar y usarán datos sintéticos. No se autoriza adquisición con personas ni conexión física de equipos.

## Bloqueos técnicos pendientes

1. especificar un generador sintético con componentes dentro y fuera de banda;
2. fijar un modelo ideal de ADC y separar resolución nominal de desempeño efectivo;
3. definir patrones reproducibles de jitter, pérdida, duplicación y reordenamiento;
4. distinguir aislamiento funcional, barrera de seguridad y separación lógica;
5. definir criterios de aceptación sin convertirlos en requisitos clínicos universales;
6. preservar metadatos de tasa, unidad, escala, tiempo y procedencia.

## Límites obligatorios

- una frecuencia de muestreo no se selecciona con una regla aislada de `2 × fmax`;
- el filtrado digital posterior no repara de forma general el aliasing ya ocurrido;
- más bits no implican automáticamente mayor exactitud;
- un LSB ideal no equivale al menor cambio detectable del sistema;
- una marca de tiempo no demuestra sincronización física;
- un aislador no demuestra por sí solo seguridad o conformidad;
- una señal digital limpia no prueba fidelidad ni origen fisiológico.

## Estado editorial

```text
source_registry: verified_direct_sources
technical_blockers: pending
practice_implementation_authorized: false
full_theory_drafting_authorized: false
public_release_authorized: false
human_or_professional_review_claimed: false
course_state: pending
```
