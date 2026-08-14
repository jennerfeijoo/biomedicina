# Protocolo de acuerdo entre revisores — Bioinstrumentación, Unidad 1

**Estado:** `protocol_ready_pending_human_execution`  
**Revisores requeridos:** 2  
**Escala ordinal:** 0–2  
**Efecto editorial:** ninguno

> **Interpretación vigente:** este protocolo es parte del comparador humano para validar el sistema revisor IA. El estado histórico se conserva, pero su ejecución no constituye un gate humano permanente de publicación. El gate futuro es `reviewer_validation_pending` hasta demostrar equivalencia o no inferioridad.

## Propósito

El protocolo comprueba si dos personas aplican de forma suficientemente consistente las rúbricas de `U1-A2`, `U1-A3` y `U1-A5`. El análisis debe realizarse antes de cualquier conciliación para que los desacuerdos no queden ocultos por discusión posterior.

El acuerdo no demuestra exactitud científica, validez de contenido ni competencia de los revisores. Es una comprobación separada de la estabilidad de aplicación de las rúbricas.

## Competencia mínima

Cada revisor debe poder documentar:

- formación o experiencia en metrología, instrumentación biomédica o área técnicamente equivalente;
- capacidad para aplicar una rúbrica analítica;
- independencia durante la primera ronda;
- ausencia de participación directa en la respuesta evaluada.

## Materiales

- contrato de evaluación de la Unidad 1;
- rúbricas de `U1-A2`, `U1-A3` y `U1-A5`;
- al menos seis respuestas retenidas o sintéticas;
- un ejemplo de calibración excluido de las métricas;
- plantilla `inter-rater-round-template.json`;
- calculador `calculate_bioinstrumentation_u1_agreement.py`.

## Flujo de trabajo

1. Revisar conjuntamente las definiciones de puntuación 0, 1 y 2.
2. Puntuar un ejemplo de calibración y discutir únicamente ese ejemplo.
3. Excluir el ejemplo de calibración de la muestra analítica.
4. Puntuar de manera independiente al menos seis objetos de revisión.
5. Registrar por criterio la puntuación ordinal y el flag de error crítico.
6. Ejecutar el calculador antes de la conciliación.
7. Inspeccionar la matriz de confusión y cada desacuerdo crítico.
8. Conciliar los casos y documentar si el problema estaba en la respuesta, la rúbrica o la formación del revisor.
9. Revisar la rúbrica y repetir una nueva ronda cuando el gate falle.

## Métricas

### Acuerdo exacto ordinal

Proporción de puntuaciones idénticas en la escala 0–2. Debe informarse junto con la matriz de confusión.

### Diferencia absoluta media

Promedio de `|puntuación A − puntuación B|`. Conserva el tamaño del desacuerdo en unidades de la rúbrica.

### Kappa ponderado lineal

Aplica pesos lineales: un desacuerdo entre 1 y 2 recibe una penalización menor que un desacuerdo entre 0 y 2. El coeficiente se declara indefinible cuando el acuerdo esperado hace cero el denominador.

### Flags críticos

Los errores críticos se analizan por separado mediante:

- acuerdo exacto;
- kappa nominal cuando es definible;
- conteo y listado de desacuerdos no resueltos.

Un promedio ordinal alto no puede compensar un desacuerdo sobre un error crítico.

## Gate interno del piloto

- acuerdo exacto ordinal ≥ 0,80;
- diferencia absoluta media ≤ 0,25;
- kappa ponderado lineal ≥ 0,70;
- acuerdo exacto de flags críticos = 1,00;
- cero desacuerdos críticos no resueltos.

Estos valores son umbrales operativos internos. No son estándares universales y no deben interpretarse sin revisar la distribución de puntuaciones, la matriz de confusión y los casos concretos.

## Ejecución reproducible

```bash
python scripts/calculate_bioinstrumentation_u1_agreement.py \
  data/review_fixtures/bioinstrumentacion/unit-01/high-agreement-synthetic.json
```

Para exigir el gate:

```bash
python scripts/calculate_bioinstrumentation_u1_agreement.py \
  data/review_fixtures/bioinstrumentacion/unit-01/high-agreement-synthetic.json \
  --enforce
```

CI utiliza dos fixtures sintéticos:

- control positivo con acuerdo alto;
- control negativo con desacuerdos ordinales y críticos.

El control positivo debe aprobar y el negativo debe fallar. Ninguno constituye evidencia humana.

## Interpretación de fallos

El gate debe fallar cuando:

- la escala o los identificadores son inconsistentes;
- el kappa ponderado es indefinible;
- el acuerdo ordinal no alcanza el umbral;
- existe cualquier desacuerdo crítico;
- faltan objetos o revisores;
- se intenta presentar datos sintéticos como revisión humana.

## Privacidad y almacenamiento

El repositorio no debe contener nombres de revisores ni estudiantes. Las rondas reales usarán identificadores seudónimos y se almacenarán fuera del repositorio cuando incluyan respuestas educativas reales.

## Estado real

El calculador y el protocolo están implementados. La ronda con dos revisores competentes permanece **pendiente de ejecución humana** como evidencia comparativa. Un workflow verde valida el software y los contratos, no el acuerdo real ni la equivalencia del revisor IA.
