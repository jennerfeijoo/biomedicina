# Protocolo de prueba cognitiva — Bioinstrumentación, Unidad 1

**Estado:** `protocol_ready_pending_human_execution`  
**Efecto editorial:** ninguno  
**Datos humanos incluidos en el repositorio:** ninguno

## Propósito

La prueba cognitiva busca detectar problemas en las instrucciones, categorías de respuesta, pistas y problemas de recuperación de la Unidad 1. No evalúa la capacidad general de la persona, no estima el rendimiento de una población y no sustituye la revisión disciplinar.

La pregunta central es:

> ¿La persona interpreta cada consigna y cada etapa de feedback como fue diseñada, sin que el material revele la respuesta ni induzca inferencias clínicas?

## Perfil y selección

La selección es intencional para detección de problemas. La sesión piloto requiere al menos una persona del perfil objetivo que:

- tenga conocimientos básicos de física, biología o ingeniería;
- no haya participado en la redacción de los ítems;
- sea adulta o participe bajo las salvaguardas institucionales aplicables;
- acepte que se está evaluando el material y no su inteligencia o desempeño académico.

Una sola sesión puede abrir o cerrar hallazgos preliminares, pero no permite estimar frecuencias poblacionales ni declarar validación pedagógica general.

## Materiales

- `data/assessment_implementations/bioinstrumentacion-unit-01.json`
- `data/assessment_implementations/bioinstrumentacion-unit-01-feedback.json`
- `data/review_templates/bioinstrumentacion/unit-01/cognitive-session-template.json`
- evaluación cerrada `U1-A1`;
- auditoría de trazabilidad `U1-A4`;
- instrucciones de `U1-A2`, sin calificación automática de la respuesta abierta.

## Secuencia de sesión

1. Documentar consentimiento y asignar un identificador seudónimo.
2. Explicar que el objetivo es encontrar defectos en el material.
3. Resolver `U1-A1` y `U1-A4` sin reparación inicial del moderador.
4. Solicitar una paráfrasis de cada consigna.
5. Aplicar probes de comprensión, recuperación, juicio y selección de respuesta.
6. Mostrar progresivamente primera pista, segunda pista y recuperación.
7. Observar si el feedback cambia el razonamiento sin revelar la clave.
8. Presentar las instrucciones de `U1-A2` y pedir que la persona explique qué producto debería entregar.
9. Realizar debriefing sobre ambigüedad, carga, terminología y posibles interpretaciones clínicas.
10. Registrar hallazgos y decisiones de revisión; no registrar nombres ni datos clínicos.

## Probes obligatorios

### Comprensión

- ¿Qué entiende que debe hacer?
- ¿Qué significa la categoría que eligió?
- ¿Qué diferencia percibe entre señal, indicación y resultado?

### Recuperación

- ¿Qué información utilizó para construir la respuesta?
- ¿Qué parte tuvo que recordar o inferir?

### Juicio

- ¿Qué parte le produjo mayor incertidumbre?
- ¿Qué evidencia consideró suficiente para decidir?

### Selección de respuesta

- ¿Cómo eligió entre las opciones?
- ¿La pista orientó el razonamiento o reveló una respuesta?
- ¿El problema de recuperación exige una relación nueva o solo repetir el ejercicio?

## Tipos de problema que deben codificarse

- interpretación incompatible con el propósito;
- término técnico no comprendido;
- opción elegida por apariencia textual;
- carga excesiva o instrucción demasiado larga;
- pista insuficiente;
- pista que revela la respuesta;
- recuperación equivalente al problema original;
- ambigüedad entre contexto educativo y conclusión clínica;
- problema no atribuible al material.

## Criterios de aceptación del piloto

La sesión puede apoyar el paso al siguiente gate cuando:

- ninguna consigna requiere reparación sustantiva del moderador para comprender el formato;
- ninguna etapa de feedback revela una clave o solución completa;
- la persona puede explicar qué debe cambiar en su razonamiento;
- al menos un problema de recuperación puede intentarse sin copiar la respuesta original;
- no aparecen instrucciones que soliciten interpretación clínica o adquisición con personas.

Estos criterios son internos y deben acompañarse de notas cualitativas. Un resultado binario no sustituye la descripción del problema observado.

## Triggers de revisión

Se debe revisar el material cuando ocurra cualquiera de los siguientes eventos:

- dos interpretaciones incompatibles de una misma consigna;
- uso de una etiqueta clínica como cantidad por efecto de la redacción;
- feedback que permite deducir directamente la opción correcta;
- recuperación que cambia solo palabras o números;
- necesidad de explicar verbalmente una regla que debería estar en la instrucción;
- inferencia clínica no prevista.

## Gobierno de datos

El repositorio solo contiene una plantilla vacía y fixtures sintéticos. No deben versionarse:

- nombres, correos, teléfonos o direcciones;
- historia médica, diagnóstico o información clínica;
- audio o video sin consentimiento específico;
- respuestas brutas identificables;
- observaciones que permitan reidentificar a la persona.

Los archivos de sesión reales deben almacenarse fuera del repositorio con acceso restringido y política de retención definida antes de la ejecución.

## Estado real

La prueba cognitiva está **pendiente de ejecución humana**. CI solo puede comprobar que el protocolo, la plantilla y los límites existen; no puede producir evidencia de comprensión de usuarios.
