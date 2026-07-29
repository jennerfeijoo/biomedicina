# Auditoría global del catálogo y del currículo

**Fecha:** 29 de julio de 2026  
**Estado de referencia validado:** `2d034c9e30cb0dbdbef25d3f0dfb0e83b1b1a77f`  
**Integración previa en `main`:** `e2db709caf90d7f9c58c1cba1f7be3cb57ab6820`

## 1. Propósito

Esta auditoría verifica el estado real del catálogo después de reconstruir las últimas asignaturas provisionales. Distingue presencia en el catálogo, existencia de páginas, desarrollo lectivo, cobertura curricular, calidad bibliográfica y revisión disciplinar.

No utiliza CI como sustituto de revisión académica y no interpreta una página generada como evidencia de que una asignatura esté terminada.

## 2. Fuentes de evidencia

Se utilizaron los artefactos producidos por los workflows verdes del estado de referencia:

- inventario de finalización de asignaturas;
- auditoría de arquitectura y preparación de cursos;
- auditoría de completitud curricular;
- auditoría de expansiones disciplinares;
- auditoría transversal del portfolio;
- auditoría bibliográfica de Biología del Desarrollo;
- auditoría léxica de redundancia de Biología del Desarrollo;
- validación de enlaces, catálogo, prerrequisitos y sincronización pública.

Las auditorías bibliográfica y de redundancia mencionadas son específicas de Biología del Desarrollo. No deben presentarse como auditorías exhaustivas de las 94 asignaturas.

## 3. Resultado ejecutivo

| Indicador | Resultado |
|---|---:|
| Asignaturas centrales catalogadas | 94 |
| Áreas académicas | 4 |
| Unidades esperadas | 607 |
| Asignaturas completamente desarrolladas | 40 |
| Asignaturas pendientes | 54 |
| Unidades avanzadas | 283 |
| Unidades autorales registradas | 0 |
| Unidades fallback | 324 |
| Páginas de unidad ausentes | 0 |
| Asignaturas provisionales | 0 |
| Asignaturas con estado `complete` | 0 |

### Interpretación

- Las **40 asignaturas desarrolladas** tienen todas sus unidades avanzadas y no contienen fallback.
- Las **54 asignaturas pendientes** existen en el currículo y en el sitio, pero sus 324 unidades siguen siendo contenido de respaldo.
- `provisional_subjects.json` vacío indica que no quedan overlays provisionales; no significa que las 94 asignaturas estén desarrolladas.
- `complete` permanece vacío porque no existe revisión disciplinar documentada.

## 4. Distribución del trabajo pendiente

| Área | Asignaturas pendientes | Unidades fallback |
|---|---:|---:|
| Biológicas y Médicas | 4 | 24 |
| Ciencias Básicas | 9 | 54 |
| Gestión, Ética y Comunicación | 9 | 54 |
| Ingeniería Biomédica Aplicada | 32 | 192 |
| **Total** | **54** | **324** |

La mayor deuda curricular se concentra en Ingeniería Biomédica Aplicada, que reúne el 59,3 % de las asignaturas pendientes y el mismo porcentaje de unidades fallback.

## 5. Asignaturas pendientes por área

### Biológicas y Médicas

- Fisiología de Sistemas (`fisiologia-sistemas`)
- Histoanatomía Humana (`histoanatomia-humana`)
- Ingeniería de Tejidos (`ingenieria-tejidos`)
- Nanobiotecnología (`nanobiotecnologia`)

### Ciencias Básicas

- Análisis Estadístico Multivariado (`analisis-estadistico-multivariado`)
- Métodos Matemáticos (`metodos-matematicos`)
- Modelos Numéricos en Biomedicina (`modelos-numericos-biomedicina`)
- Química Medicinal (`quimica-medicinal`)
- Redes y Comunicaciones (`redes-comunicaciones`)
- Redes y Servicios (`redes-servicios`)
- Sistemas Electrónicos (`sistemas-electronicos`)
- Sistemas y Señales (`sistemas-senales`)
- Teoría de Señal y Biocomputación (`teoria-senal-biocomputacion`)

### Gestión, Ética y Comunicación

- Comunicación Científica (`comunicacion-cientifica`)
- Economía y Gestión de Empresas (`economia-gestion-empresas`)
- Ética y Responsabilidad Social (`etica-responsabilidad-social`)
- Historia y Filosofía de la Ciencia (`historia-filosofia-ciencia`)
- Innovación y Emprendimiento (`innovacion-emprendimiento`)
- Laboratorio de Globalización y Emprendimiento (`laboratorio-globalizacion-emprendimiento`)
- Políticas Públicas de Ciencia y Tecnología (`politicas-publicas-ciencia-tecnologia`)
- Tecnologías de Administración (`tecnologias-administracion`)
- Uso Profesional del Inglés (`uso-profesional-ingles`)

### Ingeniería Biomédica Aplicada

- Análisis Instrumental (`analisis-instrumental`)
- Aplicaciones de Salud Digital (`aplicaciones-salud-digital`)
- Biofotónica (`biofotonica`)
- Bioinstrumentación (`bioinstrumentacion`)
- Biomateriales (`biomateriales`)
- Biomateriales e Implantes (`biomateriales-implantes`)
- Biomecánica (`biomecanica`)
- Biomecánica de Medios Continuos (`biomecanica-medios-continuos`)
- Biosensores (`biosensores`)
- Desarrollo de Dispositivos Médicos (`desarrollo-dispositivos-medicos`)
- Electrofísica y Electromecánica (`electrofisica-electromecanica`)
- Electrónica (`electronica`)
- Fundamentos de Biomecánica (`fundamentos-biomecanica`)
- Historias Clínicas, Terminologías y Estándares (`historias-clinicas-terminologias-estandares`)
- Imágenes Biomédicas (`imagenes-biomedicas`)
- Imágenes Biomédicas Avanzadas I (`imagenes-biomedicas-avanzadas-i`)
- Informática Biomédica (`informatica-biomedica`)
- Ingeniería Clínica y Gestión (`ingenieria-clinica-gestion`)
- Ingeniería de Datos Biomédicos (`ingenieria-datos-biomedicos`)
- Ingeniería Neurosensorial (`ingenieria-neurosensorial`)
- Interfaces Hombre-Máquina (`interfaces-hombre-maquina`)
- Laboratorio de Bioinstrumentación (`laboratorio-bioinstrumentacion`)
- Laboratorio de Biomecánica (`laboratorio-biomecanica`)
- Laboratorio de Imágenes Biomédicas (`laboratorio-imagenes-biomedicas`)
- Laboratorio de Señales Biomédicas (`laboratorio-senales-biomedicas`)
- Modelado y Simulación en Biomedicina (`modelado-simulacion-biomedicina`)
- NLP y Recuperación de Información (`nlp-recuperacion-informacion`)
- Polímeros y Procesamiento de Materiales (`polimeros-procesamiento-materiales`)
- Señales Biomédicas (`senales-biomedicas`)
- Simulación y Planificación Quirúrgica (`simulacion-planificacion-quirurgica`)
- Sistemas de Ayuda a la Decisión Médica (`sistemas-ayuda-decision-medica`)
- Tratamiento Digital de Imágenes (`tratamiento-digital-imagenes`)

## 6. Cobertura curricular de las asignaturas desarrolladas

Las 40 asignaturas desarrolladas tienen arquitectura válida. Sus matrices de cobertura se distribuyen así:

- `implemented`: 20 asignaturas;
- `partial`: 20 asignaturas;
- errores de cobertura: 0.

Las asignaturas con cobertura `partial` son:

- `algebra`
- `algoritmos-estructuras-datos`
- `arquitectura-computadores`
- `bases-datos`
- `bioestadistica`
- `biofisica`
- `biologia-celular-tisular`
- `biologia-desarrollo`
- `biologia-i`
- `biologia-ii`
- `biologia-molecular`
- `biologia-molecular-celular-aplicada`
- `bioquimica`
- `calculo`
- `fisica-i`
- `fisica-ii`
- `fundamentos-programacion`
- `probabilidad-estadistica`
- `quimica-i`
- `quimica-ii`

Una matriz `partial` no constituye un fallo técnico. Indica que la asignatura todavía no debe presentarse como cobertura disciplinar implementada.

## 7. Preparación académica y revisión humana

El auditor de arquitectura reportó:

- 40 arquitecturas válidas;
- 0 estructuras pendientes;
- 283 unidades avanzadas con esquema 2.0.

El auditor de expansiones encontró 24 expansiones implementadas, todas con la advertencia de que la implementación completa continúa pendiente de revisión académica externa.

Por tanto:

- `developed` describe desarrollo lectivo;
- `review` describe estado editorial;
- `complete` requiere evidencia de revisión humana;
- ningún curso debe promoverse por inferencia a partir de CI.

## 8. Calidad bibliográfica transversal

La auditoría del portfolio examinó 40 cursos desarrollados y no encontró hallazgos críticos. Registró 294 advertencias no bloqueantes:

| Categoría | Advertencias |
|---|---:|
| URL genérica en recurso o fuente | 268 |
| Bibliografía concentrada en pocos orígenes | 14 |
| Bibliografía muy repetitiva entre unidades | 12 |
| **Total** | **294** |

Las mayores concentraciones de advertencias por asignatura fueron:

- Biología Celular: 29;
- Biología de Sistemas y Modelado Cuantitativo: 29;
- Bioquímica: 25;
- Química II: 18;
- Biofísica: 16;
- Física I: 15;
- Genética: 14;
- Bioestadística: 13;
- Biología del Desarrollo: 12.

Estas advertencias no implican que las fuentes sean falsas. Señalan deuda de precisión bibliográfica: enlaces a portales generales en lugar de documentos específicos, baja diversidad editorial o reutilización excesiva de referencias.

## 9. Auditorías específicas de Biología del Desarrollo

### Bibliografía

- 109 fuentes canónicas en el registro;
- 117 ocurrencias de fuentes en unidades;
- 117 ocurrencias resueltas contra el registro;
- 0 ocurrencias sin correspondencia;
- 0 grupos duplicados no resueltos;
- 0 referencias ambiguas;
- 0 ocurrencias incompletas después de la resolución.

### Redundancia

- 14 unidades analizadas;
- 1.838 bloques de texto;
- 0 grupos exactos duplicados entre unidades;
- 0 pares casi duplicados;
- 2 frases recurrentes relacionadas con trazado de linaje y perturbación.

La repetición detectada es terminología metodológica transversal y requiere juicio editorial, no eliminación automática.

## 10. Correcciones derivadas de esta auditoría

1. El manifiesto `data/catalog_statuses.json` debe registrar explícitamente `pending`, además de `developed` y `complete`.
2. La suma de `developed` y `pending` debe cubrir exactamente las 94 asignaturas centrales.
3. `complete` debe ser subconjunto de `developed`.
4. Los conteos del manifiesto deben comprobarse automáticamente.
5. El roadmap debe utilizar el inventario real de 94 asignaturas y 607 unidades, no el estado histórico de 84 asignaturas y 508 unidades.
6. La documentación debe diferenciar asignaturas provisionales, páginas fallback, desarrollo lectivo y revisión disciplinar.

## 11. Backlog priorizado

### Prioridad 1 — Dependencias fundamentales

Desarrollar asignaturas pendientes que alimentan múltiples rutas:

- Sistemas y Señales;
- Análisis Estadístico Multivariado;
- Métodos Matemáticos;
- Modelos Numéricos en Biomedicina;
- Fisiología de Sistemas;
- Histoanatomía Humana.

### Prioridad 2 — Núcleo de ingeniería biomédica

- Bioinstrumentación;
- Señales Biomédicas;
- Imágenes Biomédicas;
- Biomateriales;
- Biomecánica;
- Biosensores;
- Ingeniería Clínica y Gestión;
- Desarrollo de Dispositivos Médicos.

### Prioridad 3 — Biomedicina computacional aplicada

- Ingeniería de Datos Biomédicos;
- Informática Biomédica;
- Historias Clínicas, Terminologías y Estándares;
- Aplicaciones de Salud Digital;
- Sistemas de Ayuda a la Decisión Médica;
- NLP y Recuperación de Información;
- Modelado y Simulación en Biomedicina.

### Prioridad 4 — Cobertura y bibliografía

- resolver las 20 matrices `partial` con evidencia de cobertura;
- sustituir URLs genéricas por documentos específicos;
- diversificar bibliografías concentradas;
- revisar repetición de fuentes entre unidades.

### Prioridad 5 — Revisión disciplinar

Organizar revisión documentada por especialistas antes de promover cualquier asignatura a `complete`.

## 12. Conclusión

El catálogo está técnicamente íntegro, navegable y sin páginas ausentes. El trabajo curricular, sin embargo, está completado en **40 de 94 asignaturas**, equivalentes al **42,6 %** del catálogo. El **57,4 %** restante conserva contenido fallback.

El estado correcto del proyecto es:

> plataforma editorial operativa, catálogo completo como inventario, cuarenta asignaturas desarrolladas, cincuenta y cuatro pendientes y ninguna asignatura con revisión disciplinar completa.
