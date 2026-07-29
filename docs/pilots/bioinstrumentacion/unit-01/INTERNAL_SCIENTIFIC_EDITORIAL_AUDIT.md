# Auditoría científica y editorial interna — Bioinstrumentación, Unidad 1

Fecha: 2026-07-29

Estado: **aprobada con correcciones aplicadas**.

## Alcance

La auditoría revisó precisión terminológica, continuidad pedagógica, consistencia entre teoría, glosario, ejemplos y evaluación, resolución de referencias, accesibilidad lingüística y límites de inferencia biomédica.

Las autoridades principales fueron VIM3, JCGM GUM-6:2020 y NIST TN 2156. La revisión mantiene explícitamente su carácter interno: no sustituye revisión profesional externa, prueba cognitiva ni acuerdo real entre revisores.

## Correcciones principales

### 1. Sistema de medición frente a proceso de medición

La definición anterior podía incorporar operador y procedimiento dentro del sistema. Se corrigió para conservar la distinción de VIM3 3.2: el sistema está compuesto por instrumentos y otros dispositivos ensamblados; el operador, el procedimiento y las condiciones pertenecen al proceso de medición circundante, aunque puedan afectar decisivamente el resultado.

### 2. Modelo de medición frente a cualquier algoritmo

Se reemplazó la formulación amplia por la definición metrológica: una relación matemática entre las cantidades conocidas que intervienen en la medición. Un algoritmo puede implementar esa relación, pero una salida de clasificación, riesgo o decisión no se convierte automáticamente en valor medido.

### 3. Magnitud de influencia

Se añadió la diferencia entre el sentido restringido de VIM3 2.52 y el uso más amplio del GUM. Las variables contextuales deben clasificarse por mecanismo: influencia, perturbación de la cantidad, condición del mensurando o cantidad de entrada.

### 4. Aptitud para el uso

La comparación entre incertidumbre del resultado e incertidumbre objetivo quedó definida como condición necesaria, no suficiente. La aptitud también exige revisar intervalo, dinámica, selectividad, condiciones, riesgo de decisión y capacidad operativa.

### 5. Accesibilidad editorial

Se sustituyeron anglicismos innecesarios en instrucciones y explicaciones dirigidas al estudiante. Los identificadores técnicos y nombres de campos de archivos permanecen sin traducir cuando su modificación rompería reproducibilidad.

### 6. Trazabilidad de las referencias

Se añadió un gate que comprueba que cada `source_link` de las seis secciones teóricas se resuelva contra una fuente localizada o contra las afirmaciones C1–C5 del contrato de preparación.

La unidad canónica fue regenerada desde los fragmentos autorales y quedó sincronizada mediante el constructor determinista del repositorio.

## Resultado

- Hallazgos críticos sin resolver: **0**
- Hallazgos mayores sin resolver: **0**
- Curso: **pending**
- Unidad: **review**, no `developed`
- Publicación: **bloqueada**
- Revisión profesional externa: **pending_human_review**
- Prueba cognitiva: **pending_human_execution**
- Acuerdo entre revisores: **pending_human_execution**

La versión estructurada y auditable se encuentra en:

`data/course_audits/bioinstrumentacion/UNIT_01_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json`
