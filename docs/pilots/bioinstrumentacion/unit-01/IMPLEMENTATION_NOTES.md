# Notas de implementación — Bioinstrumentación, Unidad 1

Este archivo registra decisiones técnicas del bloque de preparación y evita que la futura autoría reabra problemas ya resueltos sin documentarlos.

## Estado

- Rama: `agent/prepare-bioinstrumentacion-unit-01`
- Fase: `authoring_preparation_review`
- Efecto editorial: ninguno
- Bioinstrumentación permanece `pending`
- No existe todavía una unidad autoral en `data/course_redevelopment/bioinstrumentacion/units/`

## Decisiones

1. La unidad se organiza alrededor de una doble representación: ruta de señal y modelo de cantidades.
2. La trazabilidad se atribuye al resultado específico, nunca al instrumento por sí solo.
3. La aptitud para el uso se evalúa después de establecer resultado, incertidumbre, intervalo y necesidad.
4. Los casos de temperatura, ECG y presión se usan para distinguir mensurandos, no para enseñar interpretación clínica.
5. PhysioNet se utilizará solo para auditar metadatos y procedencia de señales abiertas.
6. Toda práctica será sintética, abierta o documental; no habrá adquisición humana autónoma.
7. El futuro contenido deberá implementar feedback estructurado, no respuestas desplegables como sustituto.

## Dependencias futuras

- revisión del caso de presión;
- revisión del modelo térmico;
- selección exacta del registro de PhysioNet;
- revisión disciplinar inicial;
- implementación y prueba del feedback;
- creación posterior de la unidad autoral mediante un PR separado.

## Criterio de estabilidad

Este paquete es estable si:

- el validador de preparación pasa;
- los artefactos se mantienen sincronizados;
- el curso continúa `pending`;
- no se añaden afirmaciones clínicas o normativas no respaldadas;
- cualquier cambio de alcance actualiza contrato, fuentes, evaluación y readiness en el mismo PR.
