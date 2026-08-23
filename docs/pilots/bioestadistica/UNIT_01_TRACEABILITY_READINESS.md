# Preparación de trazabilidad — Bioestadística, Unidad 1

## Resultado del piloto

La Unidad 1 conserva el estado editorial `review`. El piloto enlaza catorce afirmaciones centrales con una fuente canónica, un localizador exacto y el texto vigente de la unidad. El estado de revisión científica es `ai_review_provisional`: no se declara validación del curso ni equivalencia con revisión independiente.

## Alcance comprobado

- definición introductoria de estimando;
- población, muestra y límites del tamaño muestral ante selección sistemática;
- tipos de variables y diferencia entre significado y codificación;
- distinción entre observación y experimento;
- función y límites básicos de aleatorización y cegamiento;
- dependencia, réplicas dentro de participante y pseudorreplicación;
- reporte de pérdidas por grupo y motivo en ensayos aleatorizados.

El registro cubre afirmaciones seleccionadas de la Unidad 1. No prueba trazabilidad exhaustiva de todos los párrafos, ecuaciones, ejemplos, preguntas ni unidades posteriores.

## Procedencia y derechos

`Introduction to Modern Statistics`, segunda edición, se consultó directamente y se usa conforme a su licencia CC BY-SA 3.0. Los apuntes de Yachay aportados para el proyecto se usaron como comparadores de cobertura; el repositorio conserva solo metadata, paginación y sumas SHA-256. No se copian ni se publican esos archivos.

Las fuentes oficiales o abiertas enlazadas por la unidad son el registro canónico. Una fuente con estado `verified_metadata` puede orientar la revisión, pero no respaldar una afirmación registrada como verificada directamente.

## Control automático añadido

El validador ahora comprueba tres relaciones, además del esquema:

1. que el `source_id` exista en el registro canónico de la asignatura;
2. que una afirmación declarada como verificada directamente no apunte a una fuente solo verificada por metadata;
3. que el texto exacto de la afirmación aparezca en la unidad declarada.

Así, renombrar una fuente, alterar un enunciado o moverlo de unidad sin actualizar su evidencia falla en CI. La sincronización del catálogo usa el mismo control reforzado antes de contar una asignatura como trazada.

## Brechas que bloquean trazabilidad completa

- mediadores, colisionadores y reglas de ajuste causal;
- consecuencias y supuestos del análisis de casos completos;
- ecuación de correlación intraclase y aproximación de tamaño efectivo;
- sensibilidad, especificidad y error de clasificación;
- afirmaciones sobre validez externa y transportabilidad;
- revisión separada de ecuaciones, ejemplos y autoevaluaciones.

## Decisión editorial

La unidad puede presentarse como piloto de trazabilidad central en estado provisional. No puede promoverse a `complete` ni a `ai_review_validated` hasta cerrar las brechas, registrar una validación de revisor científico independiente según el protocolo vigente y volver a ejecutar los gates del repositorio.
