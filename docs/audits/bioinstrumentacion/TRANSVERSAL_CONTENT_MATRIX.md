# Matriz transversal de contenido — Bioinstrumentación

## Propósito

Evaluar el curso completo antes de modificar contenido académico. Esta matriz compara la arquitectura curricular aprobada con las unidades autorales existentes, sus prácticas, evaluaciones, revisión interna y publicación pública.

## Decisión general

**Conservar el contenido existente y completar la arquitectura faltante.**

No procede reescribir las unidades ya desarrolladas. El principal hallazgo es una discrepancia estructural entre la planificación de diez unidades y la implementación autoral actual de seis unidades.

## Arquitectura curricular aprobada

El plan `data/course_planning/bioinstrumentacion-excellence.json` selecciona diez unidades y rechaza explícitamente una arquitectura de seis u ocho unidades porque comprime dominios que deben permanecer separados.

| Unidad planificada | Dominio principal | Cobertura autoral actual | Decisión |
|---:|---|---|---|
| 1 | Mensurando, sistema de medición y trazabilidad | Unidad 1 existente | Conservar |
| 2 | Sensores, transductores y modelos estáticos/dinámicos | Unidad 2 existente | Conservar |
| 3 | Biopotenciales, electrodos e interfaz electrodo-tejido | Unidad 3 existente | Conservar |
| 4 | Acondicionamiento analógico, ruido y rechazo de interferencias | Parcialmente absorbida por la Unidad 4 existente | Separar y completar |
| 5 | Muestreo, conversión y adquisición digital | Parcialmente absorbida por la Unidad 4 existente | Separar y completar |
| 6 | Sensores mecánicos, térmicos, de flujo y ópticos | Unidad 5 existente | Renumerar o mapear sin perder contenido |
| 7 | Aislamiento, seguridad eléctrica y compatibilidad electromagnética | Unidad 6 existente | Renumerar o mapear sin perder contenido |
| 8 | Caracterización de desempeño, calibración e incertidumbre | No existe como unidad autoral independiente | Crear |
| 9 | Verificación, validación, riesgo y aptitud para el uso | No existe como unidad autoral independiente | Crear |
| 10 | Integración y expediente reproducible | No existe como unidad autoral independiente | Crear |

## Hallazgo crítico de arquitectura

La Unidad 4 existente, titulada **Conversión y procesamiento de señales biomédicas**, combina contenidos que el plan de excelencia separa en:

- acondicionamiento analógico, ruido y rechazo de interferencias;
- muestreo, ADC, sincronización e integridad digital.

La Unidad 5 existente corresponde funcionalmente a la unidad planificada 6. La Unidad 6 existente corresponde funcionalmente a la unidad planificada 7. Por ello, el curso no está simplemente pendiente de un cambio de estado: faltan dominios curriculares independientes y existe un desplazamiento de numeración.

## Evaluación de las unidades existentes

### Unidad 1 — Mensurando, sistema de medición y cadena de trazabilidad

**Fortalezas**

- especificación rigurosa del mensurando;
- distinción entre fenómeno, cantidad, señal, indicación, valor medido y resultado;
- modelo de cadena de medición y metadatos;
- límites de inferencia explícitos;
- prácticas y evaluación estructuradas.

**Acción**: conservar. Solo requiere revisión transversal de redundancia y referencias cruzadas.

### Unidad 2 — Sensores, transductores y modelos estáticos y dinámicos

**Fortalezas**

- separación de sensor, transductor y acondicionamiento;
- sensibilidad, offset, saturación, histéresis y carga;
- respuesta de primer orden y dominio dinámico;
- prácticas y feedback ya implementados.

**Acción**: conservar. Revisar solapamiento con la futura unidad 8 sobre caracterización de desempeño.

### Unidad 3 — Biopotenciales, electrodos e interfaz electrodo-tejido

**Fortalezas**

- origen fisiológico y conductor volumétrico;
- modelo equivalente limitado de interfaz;
- distinción entre referencia, tierra, retorno y blindaje;
- análisis técnico no diagnóstico de ECG, EEG y EMG;
- artefactos tratados por mecanismo y prueba discriminante.

**Acción**: conservar. Mantener revisión humana pendiente para evaluaciones abiertas.

### Unidad 4 — Conversión y procesamiento de señales biomédicas

**Fortalezas**

- muestreo y anti-aliasing;
- rango, LSB, cuantización, saturación, SINAD y ENOB;
- sincronización, timestamps e integridad temporal;
- prácticas reproducibles y evaluación determinista.

**Déficit relativo al plan**

- acondicionamiento analógico y presupuesto de ganancia no tienen una unidad independiente;
- ruido, interferencia, CMRR, impedancia de entrada y filtrado analógico quedan comprimidos;
- el título mezcla conversión con procesamiento, aumentando solapamiento con Sistemas y Señales y Señales Biomédicas.

**Acción**: dividir conceptualmente en unidades 4 y 5. Preservar íntegramente el contenido digital existente y crear la parte analógica faltante.

### Unidad 5 — Sensores no eléctricos

**Fortalezas**

- presión absoluta, manométrica y diferencial;
- dinámica térmica;
- flujo volumétrico, másico y velocidad local;
- transmitancia, absorbancia, reflectancia y dispersión;
- incertidumbre introductoria e integración multimodal con límites.

**Acción**: conservar como futura unidad 6. Evitar que el ejemplo de incertidumbre sustituya la futura unidad 8.

### Unidad 6 — Aislamiento, seguridad eléctrica y compatibilidad electromagnética

**Fortalezas**

- análisis de trayectorias y barreras;
- modelos sintéticos de acoplamiento conducido, capacitivo, inductivo y radiado;
- fallo simple;
- separación explícita entre modelo didáctico y conformidad normativa.

**Acción**: conservar como futura unidad 7. No ampliar con límites regulatorios sin fuentes normativas y revisión profesional.

## Unidades faltantes

### Nueva Unidad 4 — Acondicionamiento analógico, ruido y rechazo de interferencias

Debe cubrir:

- amplificación diferencial e instrumentación;
- presupuesto de rango y ganancia;
- impedancia de entrada y carga;
- ruido térmico, electrónico e interferencia;
- CMRR dependiente de frecuencia y desbalance;
- filtrado analógico y anti-aliasing como parte de una cadena;
- saturación y recuperación;
- prácticas sintéticas, sin conexión a personas.

### Nueva Unidad 8 — Caracterización de desempeño, calibración e incertidumbre

Debe separar:

- calibración y verificación;
- sensibilidad, linealidad y resolución;
- repetibilidad, reproducibilidad, histéresis y deriva;
- respuesta dinámica y ancho de banda;
- incertidumbre estándar y expandida;
- presupuesto de incertidumbre;
- trazabilidad y aptitud para el uso;
- criterios de aceptación sin presentar el material como acreditación.

### Nueva Unidad 9 — Verificación, validación, riesgo y aptitud para el uso

Debe cubrir:

- requisito, especificación y evidencia;
- verificación técnica frente a validación del uso;
- peligro, situación peligrosa, daño y control;
- fallo simple y riesgo residual a nivel educativo;
- desempeño analítico/técnico frente a utilidad clínica;
- límites de simulación y pruebas de banco;
- documentación de discrepancias y decisiones.

### Nueva Unidad 10 — Integración y expediente reproducible

Debe exigir un expediente que conecte:

- necesidad y uso previsto;
- mensurando;
- arquitectura de medición;
- selección de sensores;
- acondicionamiento y adquisición;
- datos de prueba;
- calibración e incertidumbre;
- criterios de aceptación;
- riesgos y limitaciones;
- trazabilidad de archivos, versiones y decisiones.

## Decisión de numeración

No se debe renombrar ni mover archivos existentes antes de preparar una migración atómica. La opción recomendada es:

1. crear la nueva unidad analógica como unidad 4;
2. migrar la unidad digital existente de 4 a 5;
3. migrar sensores no eléctricos de 5 a 6;
4. migrar seguridad y EMC de 6 a 7;
5. crear unidades 8, 9 y 10;
6. regenerar índice, navegación y HTML en el mismo PR;
7. conservar redirecciones o alias si existen enlaces públicos previos.

## Gates antes de editar contenido

- [x] evaluar contenido existente;
- [x] comparar contra arquitectura aprobada;
- [x] identificar unidades faltantes y desplazamiento;
- [ ] inventariar enlaces internos hacia unidades 4–6;
- [ ] comprobar páginas HTML públicas y navegación;
- [ ] comprobar referencias cruzadas en prácticas, evaluaciones y auditorías;
- [ ] diseñar plan de migración atómica;
- [ ] editar contenido únicamente después de completar los puntos anteriores.

## Estado

```text
content_evaluation: completed
academic_content_modified: false
recommended_action: preserve_split_complete_and_migrate
planned_units: 10
existing_authoral_units: 6
missing_independent_units: 4
numbering_migration_required: true
```
