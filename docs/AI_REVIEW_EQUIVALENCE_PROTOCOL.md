# Protocolo de equivalencia entre revisión IA y revisión humana

## Propósito

CitoNauta adopta como hipótesis científica que un sistema de revisión mediante inteligencia artificial puede alcanzar una validez igual o no inferior a la revisión humana dentro de un alcance definido. La identidad del revisor no determina por sí sola la validez: esta debe demostrarse mediante un estudio ciego, reproducible y preespecificado.

Este protocolo regula cuándo una revisión IA es provisional y cuándo puede autorizar contenido de forma autónoma. Las personas expertas participan durante la comparación, adjudicación de desacuerdos, vigilancia e investigación de incidentes; no constituyen un gate permanente de cada unidad.

## Hipótesis primaria

> Para un dominio, nivel de riesgo, tipo de afirmación y configuración congelados, la sensibilidad del sistema IA para detectar errores críticos no es inferior a la del panel humano de referencia por más del margen definido antes de observar los resultados.

La hipótesis debe formularse por separado para cada alcance. Un resultado favorable en Bioestadística introductoria no autoriza automáticamente revisión clínica, regulatoria, de seguridad o de otra disciplina.

## Unidad de validación

La validez pertenece a una configuración completa, no al nombre comercial de un modelo. Deben congelarse:

- proveedor, modelo y versión;
- prompt del sistema y prompt de revisión;
- rúbrica, escala y definición de error crítico;
- herramientas, recuperación de información y acceso a fuentes;
- idioma, disciplina, tipo de afirmación y nivel de riesgo;
- reglas de abstención y manejo de contradicciones;
- commit del corpus y del código evaluado.

Cualquier cambio sustantivo produce una configuración nueva y requiere revalidación o un estudio de puente previamente definido.

## Comparador humano

Una sola persona no se tratará como verdad absoluta. El comparador debe incluir al menos dos revisores competentes que trabajen de forma independiente y ciega antes de conciliar. Deben conservarse:

- puntuaciones originales;
- hallazgos críticos por revisor;
- acuerdo humano–humano;
- desacuerdos y su adjudicación;
- conflictos de interés y competencia declarada;
- decisión conciliada y justificación.

La adjudicación establece el conjunto de referencia para el análisis, pero no elimina las puntuaciones originales.

## Corpus de evaluación

La muestra debe estratificarse por:

- disciplina;
- riesgo bajo, medio o alto;
- tipo de afirmación;
- dificultad;
- presencia de cálculos, código, tablas o ecuaciones;
- evidencia directa, parcial, contradictoria o ausente.

Debe combinar errores naturales con defectos sembrados de respuesta conocida. Los defectos sembrados no pueden ser visibles por su formato ni conocidos por quienes revisan. Los errores críticos se analizan por separado de problemas de estilo o claridad.

## Procedimiento ciego

1. Registrar hipótesis, margen de no inferioridad, exclusiones y análisis.
2. Congelar corpus, configuración del sistema y commit.
3. Asignar identificadores sin revelar autoría ni condición experimental.
4. Obtener revisiones IA repetidas y revisiones humanas independientes.
5. Bloquear resultados antes de conciliación.
6. Adjudicar desacuerdos sin sustituir los datos originales.
7. Ejecutar el análisis preespecificado y análisis de sensibilidad.
8. Publicar resultados positivos, negativos e inciertos.

## Variables principales y secundarias

La variable primaria es la sensibilidad para errores críticos. Deben informarse además:

- falsos negativos críticos;
- precisión de hallazgos;
- acuerdo ponderado por severidad;
- calibración de confianza;
- estabilidad IA–IA entre ejecuciones;
- acuerdo IA–humano y humano–humano;
- cobertura de afirmaciones y fuentes;
- tasa de abstención;
- detección de casos fuera de alcance;
- tiempo y coste, solo como resultados secundarios.

Cada estimación debe incluir incertidumbre. Una mayor velocidad no compensa la omisión de un error crítico.

## Decisión de no inferioridad

Antes del estudio se debe fijar un margen clínico o científicamente justificable. No se admite escoger el margen después de observar resultados. La autorización requiere simultáneamente:

- resultado de no inferioridad favorable para la variable primaria;
- cero hallazgos críticos conocidos sin una regla explícita de manejo;
- estabilidad suficiente entre ejecuciones;
- abstención segura fuera de alcance;
- trazabilidad completa de configuración, corpus y análisis;
- intervalo de validez y plan de monitorización.

Si el estudio es insuficiente, negativo o inconcluso, el estado permanece `unvalidated`.

## Estados operativos

| Estado | Significado | Puede autorizar publicación |
|---|---|---:|
| `unvalidated` | No existe evidencia comparativa suficiente | No |
| `validated_for_scope` | Se demostró validez para el alcance congelado | Sí, solo dentro del alcance |
| `expired` | Terminó el periodo de validez o cambió una dependencia crítica | No |
| `out_of_scope` | El objeto no coincide con el alcance validado | No |

La revisión de un curso usa `ai_review_provisional` mientras el revisor esté `unvalidated`. Solo una coincidencia exacta con un registro `validated_for_scope` puede producir `ai_review_validated`.

## Publicación y fusión automática

La integración automática solo se permite cuando:

- el autor y el revisor tienen contextos separados;
- el revisor aplicable está `validated_for_scope` y vigente;
- modelo, prompt, rúbrica, dominio, riesgo e infraestructura coinciden;
- las fuentes exigidas están disponibles con localizadores;
- no existen hallazgos críticos ni contradicciones abiertas;
- las pruebas deterministas son satisfactorias;
- el sistema no se abstuvo.

En cualquier otro caso puede abrirse una propuesta de cambio, pero no fusionarse automáticamente ni presentarse como validada.

## Vigilancia posterior

Después de la validación se requiere:

- muestreo periódico de contenido ya publicado;
- registro de falsos negativos e incidentes;
- revalidación ante cambios de modelo, prompt, fuentes o dominio;
- retirada o degradación inmediata del estado cuando aparece un riesgo nuevo;
- auditoría humana puntual para incidentes, abstenciones y casos fuera de alcance.

## Evidencia educativa separada

La validez del revisor demuestra capacidad para evaluar el contenido dentro de un alcance. No demuestra que las personas aprendan. La eficacia educativa requiere estudios independientes de comprensión, transferencia, retención, accesibilidad y abandono.
