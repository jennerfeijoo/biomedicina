# Auditoría científica y editorial interna — Bioinstrumentación, Unidad 2

Fecha: 2026-07-29

Estado: **aprobada con correcciones aplicadas**.

## Alcance

La auditoría revisó conjuntamente U2-P1 a U2-P3, U2-A1 a U2-A5 y las doce rutas de feedback. Se evaluaron exactitud de modelos, separación de mecanismos de carga, alineación pedagógica, trazabilidad de evidencia, ausencia de filtración de claves, accesibilidad editorial y límites de inferencia biomédica.

Las bases principales fueron VIM3, JCGM GUM-6:2020, las resoluciones técnicas de la Unidad 2 y la documentación fijada de los tres componentes. La revisión es interna y no sustituye revisión profesional externa, prueba cognitiva ni acuerdo real entre revisores.

## Correcciones principales

### 1. Carga eléctrica y transferencia mecánica

`LG01` combinaba la tensión del puente con la transferencia de deformación. Se corrigió a `bridge_output_voltage`: la impedancia de entrada perturba la salida eléctrica de la red; la transferencia de deformación se analiza en el caso mecánico de galga, adhesivo y estructura.

### 2. Alcance del rechazo del primer orden

`reject_first_order` podía interpretarse como rechazo universal. Se sustituyó por `reject_declared_simple_first_order`: el control invalida el modelo simple declarado, pero no excluye un modelo compuesto con retardo, segundo orden u otros subsistemas.

### 3. Feedback diagnóstico de SC01

SC01 activaba una ruta sobre superioridad de sensibilidad sin que el caso presentara una decisión de sensibilidad. Se eliminó esa asociación. La ruta permanece en SC02 y U2-A5, donde sí se examinan saturación, compromisos y selección.

### 4. Cruce de evidencia

Se añadió un `evidence_crosswalk` para U2-A1 a U2-A5. Cada evaluación queda vinculada a resultados, prácticas, claims U2-C1 a U2-C6 y artefactos localizados. El gate rechaza referencias inexistentes o cobertura incompleta.

### 5. Gobierno de claves

Los campos esperados son necesarios para regresión interna, pero no deben llegar al payload del estudiante. Se añadió una política que exige almacenamiento interno, exclusión del cliente, bloqueo de bundles públicos y revisión de despliegue separada.

### 6. Accesibilidad editorial

Los identificadores de máquina permanecen estables en inglés para reproducibilidad. Las explicaciones e instrucciones dirigidas al estudiante usan terminología española y explican el significado de cada decisión técnica.

## Resultado

- Hallazgos críticos sin resolver: **0**
- Hallazgos mayores sin resolver: **0**
- Prácticas internas: **implemented_internal_review**
- Evaluaciones internas: **implemented_internal_review**
- Curso: **pending**
- Unidad autoral 02: **ausente**
- Teoría completa: **no autorizada**
- Publicación: **bloqueada**
- Revisión profesional externa: **pending_human_review**
- Prueba cognitiva: **pending_human_execution**
- Usabilidad del feedback: **pending_human_execution**
- Acuerdo entre revisores: **pending_human_execution**

La versión estructurada y auditable se encuentra en:

`data/course_audits/bioinstrumentacion/UNIT_02_PRACTICES_ASSESSMENT_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json`
