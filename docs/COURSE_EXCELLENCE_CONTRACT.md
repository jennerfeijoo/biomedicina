# Contrato de excelencia académica de CitoNauta

## Propósito

Este contrato define las condiciones mínimas para que una asignatura pase de inventario curricular a recurso educativo desarrollado y, posteriormente, a contenido revisado. Complementa el protocolo de desarrollo académico y convierte sus principios críticos en requisitos verificables.

Su primer caso de aplicación es la ruta piloto de Bioinstrumentación. El contrato es disciplinariamente neutral: cada curso debe adaptarlo a sus mecanismos, métodos, riesgos y formas de evidencia.

## 1. Verdad editorial

Los estados públicos deben derivarse de una única fuente de verdad:

- `material_available`: existen páginas y actividades; no implica especificidad ni validez;
- `template_detected`: existe texto genérico conocido y se requiere reconstrucción;
- `review`: el contenido es sustantivo, pero la revisión sigue siendo provisional;
- `complete`: existe una revisión documentada por un sistema validado para el alcance y se resolvieron los hallazgos bloqueantes.

Una página generada, un JSON válido, un número mínimo de palabras o un workflow verde no permiten promover una asignatura. Catálogo, curso, unidades, mapa, metadatos y rutas deben mostrar el mismo estado.

## 2. Delimitación disciplinar

Antes de redactar unidades, el paquete debe registrar:

- propósito y público;
- nivel académico;
- conocimientos de entrada observables;
- competencias terminales;
- dominios nucleares y aplicaciones legítimas;
- límites con asignaturas vecinas;
- contenidos excluidos;
- riesgos biomédicos, técnicos, éticos o regulatorios;
- arquitectura seleccionada y alternativas rechazadas.

El número y orden de unidades se justifican mediante cobertura y dependencias, no mediante una plantilla fija.

## 3. Trazabilidad de evidencia

Cada afirmación central debe poder auditarse. Las fuentes se clasifican como:

- `verified_directly`: se consultó la sección relevante;
- `verified_metadata`: se verificaron identidad y pertinencia general, pero no el contenido necesario para respaldar una afirmación detallada;
- `recommended_future_review`: fuente identificada para una revisión posterior;
- `superseded`, `excluded`: fuente reemplazada o descartada con justificación.

Definiciones normativas, ecuaciones, cifras, requisitos de seguridad, criterios regulatorios y afirmaciones clínicas requieren `verified_directly` y un localizador estable antes de publicarse como contenido desarrollado. Una norma accesible solo mediante metadata no autoriza reproducir requisitos detallados.

## 4. Contrato de unidad

Cada unidad desarrollada debe contener, cuando sea aplicable:

1. pregunta central y propósito;
2. resultados de aprendizaje observables;
3. conocimientos previos y ruta de recuperación;
4. teoría específica con intuición, formalización, supuestos y límites;
5. mecanismo, cadena de medición o procedimiento paso a paso;
6. modelo mental o representación visual funcional;
7. al menos dos ejemplos razonados;
8. práctica graduada y actividad reproducible;
9. errores frecuentes y misconceptions verificables;
10. autoevaluación alineada con los resultados;
11. retroalimentación específica por tipo de error;
12. fuentes con función curricular y localizadores;
13. conexiones biomédicas limitadas por evidencia;
14. síntesis y criterio para continuar.

No se permite texto intercambiable entre conceptos, actividades genéricas, bibliografía decorativa ni densidad añadida solo para superar validadores.

## 5. Alineación educativa

Cada resultado de aprendizaje debe estar conectado con:

- explicación o mecanismo;
- ejemplo;
- práctica;
- evidencia evaluable;
- criterio de logro;
- error crítico;
- feedback;
- actividad de recuperación;
- siguiente decisión de aprendizaje.

Una respuesta revelada no constituye retroalimentación. El feedback debe explicar por qué una respuesta es incorrecta, qué misconception indica y qué debe revisar o resolver el estudiante.

## 6. Progresión y autonomía

Una asignatura no puede declararse autosuficiente hasta demostrar que un estudiante puede:

- reconocer si posee los prerrequisitos;
- localizar el punto de entrada adecuado;
- detectar una comprensión insuficiente;
- practicar con dificultad creciente;
- recibir feedback accionable;
- recuperar una brecha;
- demostrar dominio;
- identificar el siguiente paso;
- verificar las fuentes principales.

Las rutas deben distinguir `navegable`, `desarrollada` y `autosuficiente`. Una ruta con nodos `pending` no es autosuficiente.

## 7. Modelos mentales y visualización

Toda representación debe registrar:

- objetivo pedagógico;
- entidades y variables representadas;
- escala espacial, temporal o cuantitativa;
- correspondencias entre imagen y modelo;
- elementos omitidos;
- punto de fallo;
- texto alternativo;
- fuente y licencia;
- retorno explícito al lenguaje científico formal.

Una figura decorativa no satisface este requisito.

## 8. Reproducibilidad

Cálculos, código y análisis deben conservar:

- datos o generador de datos;
- versión de herramientas;
- parámetros;
- unidades;
- semilla cuando corresponda;
- salida esperada;
- comprobaciones;
- limitaciones.

Los ejemplos ejecutables deben validarse automáticamente o marcarse de forma explícita como pseudocódigo no ejecutado.

## 9. Accesibilidad y resiliencia

Las páginas deben ser utilizables mediante teclado, tecnologías asistivas y pantallas estrechas. La publicación debe conservar contenido esencial sin depender de un enriquecimiento silencioso. Los fallos de JSON, notación matemática o recursos externos deben producir un aviso accesible, no únicamente un mensaje de consola.

## 10. Validez del sistema revisor

La promoción a `complete` requiere un registro que identifique:

- sistema revisor y configuración exacta;
- fecha y versión revisada;
- alcance de la revisión;
- hallazgos y resolución;
- evidencia de validez para ese dominio y riesgo;
- limitaciones no resueltas;
- decisión editorial.

Una revisión IA puede constituir el gate autónomo si demostró equivalencia o no inferioridad mediante el protocolo preespecificado. Durante la validación se emplean varias personas competentes como comparador y para adjudicar desacuerdos; después participan en vigilancia, incidentes, abstenciones y casos fuera de alcance, no como autorización obligatoria de cada unidad.

## 11. Gates de publicación

### Arquitectura aprobada para autoría

- alcance, exclusiones y prerrequisitos definidos;
- matriz de cobertura completa;
- secuencia justificada;
- registro de fuentes clasificado;
- matriz resultado–evaluación–feedback;
- criterios de revisión definidos.

### Curso desarrollado

- todas las unidades cumplen el contrato;
- no existe contenido fallback;
- fuentes centrales verificadas directamente;
- pruebas técnicas y editoriales verdes;
- estado público coherente;
- revisión interna de continuidad y redundancia.

### Curso completo

- afirmaciones de riesgo medio y alto con fuentes y localizadores;
- `ai_review_validated` y registro `validated_for_scope` coincidente;
- hallazgos bloqueantes resueltos;
- prueba de accesibilidad definida;
- prueba de autonomía con usuarios;
- mantenimiento y fecha de próxima revisión establecidos.

## 12. Regla de escalamiento

El contrato se valida primero en una ruta piloto. Solo después de demostrar consistencia editorial, aprendizaje recuperable, trazabilidad y validez del sistema revisor debe replicarse en el resto del catálogo.
