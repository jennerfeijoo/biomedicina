# Auditoría del contenido y de la evaluación — 11 de octubre de 2026

Alcance: todas las asignaturas y unidades del corpus JSON publicado. La lectura censal mide estructura, preguntas, explicaciones, fuentes, recurrencia de enunciados y suficiencia de bancos. No verifica una por una las afirmaciones biomédicas ni demuestra dominio, validez o dificultad de los ítems. La corrección científica y la alineación semántica requieren revisión disciplinar.

## Resultados del censo

- courses: **94**
- units: **617**
- questions: **24174**
- usable_questions: **21757**
- blocked_units: **95**
- final_tests_available: **78**
- unit_tests_available: **522**
- units_under_60: **545**
- self_assessments: **5698**
- answers_without_reasoning: **2804**
- repeated_prompts_5plus: **4**
- claim_registries: **20**
- registered_claims: **894**
- traceability_findings: **1677**

## Diagnóstico y decisiones

1. **P0 — Contenido de plantilla.** Las unidades señaladas requieren reescritura disciplinar antes de habilitar su examen. Sus candidatos no se cuentan como preguntas utilizables.
2. **P1 — Profundidad desigual.** Presencia de una sección, longitud o ausencia del marcador conocido no demuestran suficiencia. Revisar explicaciones causales, prerrequisitos, cálculos, ejemplos de transferencia y límites por objetivo.
3. **P1 — Evaluación insuficiente.** Las respuestas breves sin razonamiento necesitan criterios observables y retroalimentación específica. Los bancos iniciales recuperan preguntas y convierten errores, casos y glosarios del contenido existente: no son miles de preguntas nuevas redactadas y validadas.
4. **P1 — Alineación no demostrada.** Un ID de objetivo enlazado no prueba que el ítem lo evalúe. Por ejemplo, en RM U3, Q03 sobre T2* está enlazado con LO03, que exige predecir contraste con parámetros, mientras LO02 distingue relajaciones. Debe revisarse el vínculo y la demanda cognitiva, no solo su sintaxis.
5. **P1 — Muestreo de contenidos.** El final representa todas las unidades y reserva comprensión, análisis de errores y casos cuando están disponibles. Un máximo del 40 % corresponde a reconocimiento del glosario. No se afirma cobertura de cada subtema u objetivo: falta una matriz de especificación revisada.
6. **P1 — Dominio práctico.** Un test de 50 preguntas debe acompañarse de problemas nuevos, análisis de datos, interpretación de figuras y proyectos con rúbricas. Aprobar preguntas de reconocimiento no demuestra saber ejecutar un método.
7. **P2 — Variedad visual.** Añadir preguntas apoyadas en figuras, gráficos y datos reales/sintéticos verificables; no inferir diagnóstico ni magnitudes a partir de imágenes sin metadatos.

## Trazabilidad científica

El inventario de afirmaciones registra 20 asignaturas y 894 afirmaciones; conserva 1677 hallazgos de contrato o trazabilidad. Son carencias documentales detectadas por el validador, no 1677 errores científicos demostrados. Las restantes asignaturas no quedan validadas por estar fuera de ese registro. Cinco registros no presentan esos hallazgos; esto tampoco equivale a revisión científica completa. El detalle por afirmación se conserva en el informe JSON.

## Contrato de los bancos y exámenes

- Banco virtual versionado: fuente JSON, huella SHA-256 y puntero exacto a cada ítem. Una pregunta tiene un ID estable mientras se mantenga su posición; un cambio del corpus cambia la huella y debe tratarse como una nueva versión.
- Meta editorial propuesta: **60–100 preguntas distintas por unidad**, incluyendo comprensión, aplicación, interpretación y transferencia. Es una meta de autoría, no un umbral de calidad validado. El censo informa cuántas unidades todavía no llegan.
- Test de unidad: **15 preguntas** sin reemplazo. Final de asignatura: **50 preguntas** sin reemplazo; todos los bancos de unidad deben estar disponibles. No se recorta silenciosamente un examen insuficiente.
- Nueva semilla produce una nueva selección y reordena opciones. Se garantiza ausencia de IDs y enunciados repetidos en un intento, no ausencia de repetición entre intentos.
- Correspondencia de término y definición: corrección automática, limitada a reconocimiento. Respuestas abiertas, análisis y casos: solución orientativa y rúbrica de autoevaluación; nunca se simula corrección semántica automática.
- La puntuación automática y la autoevaluación se informan por separado. No hay nota certificadora ni umbral de dominio calibrado.
- Soluciones ocultas hasta finalizar en la interfaz, pero públicas en los archivos de un sitio estático. Adecuado para práctica, no para exámenes de alto impacto.
- Las respuestas permanecen en memoria de la pestaña y no se envían a un servidor. No se prometen persistencia ni autenticación.

## Hoja de ruta de revisión disciplinar

Para cada objetivo: definir prerrequisitos → revisar mecanismo y fuentes primarias → resolver al menos un caso guiado → proponer un problema nuevo → añadir interpretación de evidencia/figuras → construir ítems de distinta demanda → revisar clave y distractores → pilotar y analizar dificultad/discriminación → corregir y documentar. Priorizar las unidades P0 y después las P1. No elevar estados editoriales por aprobar pruebas de software.

## Inventario por asignatura

| Asignatura | Unidades | Candidatos de banco | Final 50 | Unidades con plantilla |
|---|---:|---:|---|---:|
| Algoritmos y Estructuras de Datos | 6 | 194 | Disponible para práctica | 0 |
| Ampliación de Cálculo | 6 | 177 | Disponible para práctica | 0 |
| Análisis Estadístico Multivariado | 8 | 216 | Disponible para práctica | 0 |
| Arquitectura de Computadores | 6 | 180 | Disponible para práctica | 0 |
| Bases de Datos | 6 | 198 | Disponible para práctica | 0 |
| Bioestadística | 8 | 240 | Disponible para práctica | 0 |
| Biofísica | 6 | 177 | Disponible para práctica | 0 |
| Cálculo | 6 | 192 | Disponible para práctica | 0 |
| Ecuaciones Diferenciales | 10 | 220 | Disponible para práctica | 0 |
| Epidemiología y Métodos de Investigación Clínica | 8 | 216 | Disponible para práctica | 0 |
| Fundamentos de Programación | 6 | 174 | Disponible para práctica | 0 |
| Física I | 7 | 243 | Disponible para práctica | 0 |
| Física II | 6 | 188 | Disponible para práctica | 0 |
| Modelos Numéricos en Biomedicina | 6 | 184 | Disponible para práctica | 0 |
| Métodos Matemáticos | 6 | 190 | Disponible para práctica | 0 |
| Métodos Numéricos | 6 | 180 | Disponible para práctica | 0 |
| Probabilidad y Estadística | 6 | 204 | Disponible para práctica | 0 |
| Química I | 6 | 229 | Disponible para práctica | 0 |
| Química II | 6 | 202 | Disponible para práctica | 0 |
| Química Medicinal | 6 | 153 | Bloqueado | 6 |
| Redes y Comunicaciones | 6 | 151 | Bloqueado | 6 |
| Redes y Servicios | 6 | 152 | Bloqueado | 6 |
| Sistemas Electrónicos | 6 | 152 | Bloqueado | 6 |
| Sistemas y Señales | 8 | 232 | Disponible para práctica | 0 |
| Teoría de Señal y Biocomputación | 6 | 154 | Bloqueado | 6 |
| Álgebra | 6 | 232 | Disponible para práctica | 0 |
| Biología Celular y Tisular | 10 | 320 | Disponible para práctica | 0 |
| Biología de Sistemas y Modelado Cuantitativo | 8 | 216 | Disponible para práctica | 0 |
| Biología del Desarrollo | 14 | 550 | Disponible para práctica | 0 |
| Biología I | 6 | 197 | Disponible para práctica | 0 |
| Biología II | 6 | 192 | Disponible para práctica | 0 |
| Biología Molecular | 6 | 198 | Disponible para práctica | 0 |
| Biología Molecular y Celular Aplicada | 6 | 180 | Disponible para práctica | 0 |
| Biología Sintética | 8 | 216 | Disponible para práctica | 0 |
| Biomarcadores y Diagnóstico Molecular | 8 | 230 | Disponible para práctica | 0 |
| Bioquímica | 6 | 174 | Disponible para práctica | 0 |
| Farmacología, Farmacocinética y Farmacodinámica | 8 | 232 | Disponible para práctica | 0 |
| Fisiología de Sistemas | 6 | 493 | Disponible para práctica | 0 |
| Fisiología Humana I | 6 | 162 | Disponible para práctica | 0 |
| Fisiología Humana II | 6 | 171 | Disponible para práctica | 0 |
| Fisiopatología Humana | 6 | 162 | Disponible para práctica | 0 |
| Genética | 6 | 162 | Disponible para práctica | 0 |
| Histoanatomía Humana | 6 | 530 | Disponible para práctica | 0 |
| Ingeniería de Tejidos | 6 | 289 | Disponible para práctica | 0 |
| Inmunología e Inmunopatología | 8 | 216 | Disponible para práctica | 0 |
| Microbiología Médica y Enfermedades Infecciosas | 8 | 232 | Disponible para práctica | 0 |
| Nanobiotecnología | 6 | 151 | Bloqueado | 6 |
| Ómicas de Célula Única y Biología Espacial | 8 | 216 | Disponible para práctica | 0 |
| Análisis Instrumental | 8 | 216 | Disponible para práctica | 0 |
| Aplicaciones de Salud Digital | 6 | 312 | Disponible para práctica | 0 |
| Biofotónica | 6 | 295 | Disponible para práctica | 0 |
| Bioinformática | 6 | 162 | Disponible para práctica | 0 |
| Bioinstrumentación | 10 | 274 | Disponible para práctica | 0 |
| Biomateriales | 6 | 293 | Disponible para práctica | 0 |
| Biomateriales e Implantes | 6 | 316 | Disponible para práctica | 0 |
| Biomecánica | 6 | 251 | Disponible para práctica | 0 |
| Biomecánica de Medios Continuos | 6 | 287 | Disponible para práctica | 0 |
| Biosensores | 6 | 279 | Disponible para práctica | 0 |
| Desarrollo de Dispositivos Médicos | 6 | 291 | Disponible para práctica | 0 |
| Electrofísica y Electromecánica | 6 | 394 | Disponible para práctica | 0 |
| Electrónica | 6 | 304 | Disponible para práctica | 0 |
| Evaluación Computacional de Evidencia Terapéutica | 8 | 234 | Disponible para práctica | 0 |
| Fundamentos de Biomecánica | 6 | 257 | Disponible para práctica | 0 |
| Historias Clínicas, Terminologías y Estándares | 6 | 527 | Disponible para práctica | 0 |
| Imágenes Biomédicas | 6 | 327 | Disponible para práctica | 0 |
| Imágenes Biomédicas Avanzadas I | 6 | 529 | Disponible para práctica | 0 |
| Imágenes Biomédicas Avanzadas II | 8 | 216 | Disponible para práctica | 0 |
| Informática Biomédica | 6 | 553 | Disponible para práctica | 0 |
| Ingeniería Clínica y Gestión | 6 | 296 | Disponible para práctica | 0 |
| Ingeniería de Datos Biomédicos | 6 | 556 | Disponible para práctica | 0 |
| Ingeniería Neurosensorial | 6 | 522 | Disponible para práctica | 0 |
| Interfaces Hombre-Máquina | 6 | 504 | Disponible para práctica | 0 |
| Laboratorio de Bioinstrumentación | 6 | 322 | Disponible para práctica | 0 |
| Laboratorio de Biomecánica | 6 | 302 | Disponible para práctica | 0 |
| Laboratorio de Imágenes Biomédicas | 6 | 433 | Disponible para práctica | 0 |
| Laboratorio de Señales Biomédicas | 6 | 162 | Disponible para práctica | 0 |
| Machine Learning Biomédico y Validación de Modelos Clínicos | 8 | 216 | Disponible para práctica | 0 |
| Modelado y Simulación en Biomedicina | 6 | 153 | Bloqueado | 6 |
| NLP y Recuperación de Información | 6 | 153 | Bloqueado | 6 |
| Polímeros y Procesamiento de Materiales | 6 | 152 | Bloqueado | 6 |
| Señales Biomédicas | 6 | 288 | Disponible para práctica | 0 |
| Simulación y Planificación Quirúrgica | 6 | 153 | Bloqueado | 6 |
| Sistemas de Ayuda a la Decisión Médica | 6 | 153 | Bloqueado | 6 |
| Tratamiento Digital de Imágenes | 6 | 153 | Bloqueado | 6 |
| Ciencia Regulatoria, Calidad y Seguridad de Tecnologías Médicas | 8 | 232 | Disponible para práctica | 0 |
| Comunicación Científica | 6 | 278 | Disponible para práctica | 0 |
| Economía y Gestión de Empresas | 6 | 310 | Disponible para práctica | 0 |
| Historia y Filosofía de la Ciencia | 6 | 513 | Disponible para práctica | 0 |
| Innovación y Emprendimiento | 6 | 492 | Disponible para práctica | 0 |
| Laboratorio de Globalización y Emprendimiento | 6 | 213 | Bloqueado | 5 |
| Políticas Públicas de Ciencia y Tecnología | 6 | 154 | Bloqueado | 6 |
| Tecnologías de Administración | 6 | 153 | Bloqueado | 6 |
| Uso Profesional del Inglés | 6 | 152 | Bloqueado | 6 |
| Ética y Responsabilidad Social | 6 | 323 | Disponible para práctica | 0 |

## Anexo: hallazgos por unidad

### Algoritmos y Estructuras de Datos

- **U1: Pensamiento algorítmico** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Complejidad y eficiencia** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Estructuras lineales** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Árboles y grafos** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Ordenamiento y búsqueda** — 33 candidatos; 10 autoevaluaciones; 3 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Diseño, pruebas y reproducibilidad** — 33 candidatos; 10 autoevaluaciones; 3 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Ampliación de Cálculo

- **U1: Funciones multivariables, derivadas parciales y sensibilidad** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Optimización multivariable y restricciones** — 30 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Integración múltiple y cambio de variables** — 30 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Campos vectoriales, circulación y flujo** — 30 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Series, Taylor y control del error** — 30 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Computación científica, convergencia y proyecto integrador** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Análisis Estadístico Multivariado

- **U1: Geometría de datos multivariados y preprocesamiento** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Covarianza, correlación parcial y regularización** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: PCA, SVD y representación de baja dimensión** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Distancias, agrupamiento y estabilidad** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Inferencia multivariada y pruebas conjuntas** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Discriminación clásica y evaluación predictiva** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Asociación e integración entre bloques de variables** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Flujo biomédico reproducible en alta dimensión** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Arquitectura de Computadores

- **U1: Representación de información** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Procesador e instrucciones** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Jerarquía de memoria** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Entrada, salida e interrupciones** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Paralelismo y aceleración** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Sistemas embebidos y confiabilidad** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Bases de Datos

- **U1: Modelado de datos** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Modelo relacional y normalización** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: SQL para consulta y análisis** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Transacciones y concurrencia** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Índices, seguridad y rendimiento** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Datos biomédicos heterogéneos** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Bioestadística

- **U1: Preguntas, datos y diseños biomédicos** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Descripción, visualización y calidad de los datos** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Probabilidad, distribuciones y variabilidad muestral** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Estimación, intervalos de confianza y pruebas de hipótesis** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Comparación de grupos y métodos no paramétricos** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Correlación y regresión lineal y logística** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U7: Tamaño del efecto, potencia, tamaño muestral y multiplicidad** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U8: Lectura crítica, reporte y reproducibilidad** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Biofísica

- **U1: Escalas y energía en sistemas vivos** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Difusión, transporte y membranas** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Electricidad celular** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Mecánica de biomoléculas y células** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Óptica y espectroscopía biológica** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Modelos biofísicos integradores** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Cálculo

- **U1: Funciones, escalas y modelos** — 32 candidatos; 9 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Límites y continuidad** — 31 candidatos; 9 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Derivadas y tasas de cambio** — 32 candidatos; 9 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Aplicaciones de la derivada** — 32 candidatos; 9 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Integrales y acumulación** — 32 candidatos; 9 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Métodos numéricos y modelos dinámicos** — 33 candidatos; 9 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Ecuaciones Diferenciales

- **U1: De una pregunta biomédica a un modelo dinámico** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: EDO de primer orden: soluciones, interpretación y comprobación** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Análisis cualitativo de modelos escalares** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Sistemas lineales y modelos compartimentales** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Sistemas no lineales y plano de fase** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Retroalimentación, oscilaciones y bifurcaciones** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Dinámica de segundo orden, amortiguamiento y forzamiento** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Integración numérica y verificación computacional** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U9: Parámetros, sensibilidad, identificabilidad y validación** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U10: Dinámica espacial: difusión, advección y reacción-difusión** — 22 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Epidemiología y Métodos de Investigación Clínica

- **U1: Pregunta clínica, población, protocolo y estimando** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Frecuencia, asociación, efecto y comparabilidad** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Diseños observacionales, muestreo y sesgos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Confusión, causalidad, modificación y ensayo objetivo** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Medición clínica, desenlaces, datos faltantes y datos rutinarios** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Ensayos aleatorizados y estimación de efectos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Ética, GCP, registro, calidad y supervisión** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Plan de análisis, reporte, reproducibilidad y síntesis** — 27 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Fundamentos de Programación

- **U1: Algoritmos y tipos de datos** — 30 candidatos; 10 autoevaluaciones; 2 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Control de flujo** — 28 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Funciones y modularidad** — 29 candidatos; 10 autoevaluaciones; 2 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Colecciones y archivos** — 29 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Análisis y visualización** — 29 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Calidad de software** — 29 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Física I

- **U1: Medición, vectores y cinemática** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Dinámica: fuerzas, interacción y modelos** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Trabajo, energía y potencia** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Momento lineal, rotación y equilibrio** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Fluidos: presión, flujo y resistencia** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Oscilaciones, ondas y ultrasonido** — 36 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Termodinámica, transferencia de calor y sistemas abiertos** — 37 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Física II

- **U1: Campo y potencial eléctrico** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Circuitos eléctricos** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Magnetismo e inducción** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Ondas electromagnéticas** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Óptica geométrica y física** — 32 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Física moderna biomédica** — 36 candidatos; 10 autoevaluaciones; 2 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Modelos Numéricos en Biomedicina

- **U1: De problema biomédico a modelo** — 31 candidatos; 8 autoevaluaciones; 3 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Geometría y discretización** — 30 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Modelos de transporte** — 31 candidatos; 8 autoevaluaciones; 3 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Mecánica computacional** — 30 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Calibración e incertidumbre** — 31 candidatos; 8 autoevaluaciones; 3 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Validación y comunicación** — 31 candidatos; 8 autoevaluaciones; 3 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Métodos Matemáticos

- **U1: Álgebra lineal aplicada** — 34 candidatos; 10 autoevaluaciones; 3 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Cálculo vectorial** — 34 candidatos; 10 autoevaluaciones; 4 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Series y transformadas** — 30 candidatos; 8 autoevaluaciones; 3 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Ecuaciones diferenciales** — 30 candidatos; 8 autoevaluaciones; 3 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Variables complejas y funciones especiales** — 31 candidatos; 8 autoevaluaciones; 3 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Formulación y validación de modelos** — 31 candidatos; 8 autoevaluaciones; 3 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Métodos Numéricos

- **U1: Error, aritmética computacional y condicionamiento** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Raíces, optimización y criterios de parada** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Álgebra lineal numérica: factorizaciones y métodos iterativos** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Interpolación, splines y ajuste por mínimos cuadrados** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Cuadratura e integración numérica de ecuaciones diferenciales** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Verificación numérica, sensibilidad y reproducibilidad** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Probabilidad y Estadística

- **U1: Fundamentos de probabilidad y simulación** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Probabilidad condicional, Bayes y diagnóstico** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Variables aleatorias, momentos y transformaciones** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Distribuciones, muestreo y teorema central** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Estimación, pruebas y decisiones inferenciales** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Regresión, validación y comunicación reproducible** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Química I

- **U1: Materia, medición y estequiometría** — 36 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Estructura atómica** — 37 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Enlace y estructura molecular** — 38 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Estados de la materia y soluciones** — 38 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Termoquímica y cinética** — 39 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Equilibrios ácido-base** — 41 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Química II

- **U1: Equilibrio químico avanzado** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Ácidos, bases, buffers y solubilidad** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Termodinámica química y acoplamiento** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Cinética, mecanismos y catálisis** — 34 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Electroquímica, interfaces y sensores** — 34 candidatos; 10 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Química orgánica y biomolecular** — 32 candidatos; 10 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Química Medicinal

- **U1: Dianas y descubrimiento de fármacos** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Relación estructura-actividad** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Propiedades fisicoquímicas** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: ADME y metabolismo** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Optimización y seguridad temprana** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Métodos computacionales y translación** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Redes y Comunicaciones

- **U1: Modelos y medios de comunicación** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Enlace y acceso al medio** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Internet y direccionamiento** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Transporte y aplicaciones** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Rendimiento y calidad de servicio** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Seguridad y diseño** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Redes y Servicios

- **U1: Servicios de infraestructura** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Servicios web y APIs** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Virtualización y contenedores** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Disponibilidad y observabilidad** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Identidad y seguridad** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Diseño de servicio sanitario** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Sistemas Electrónicos

- **U1: Magnitudes y análisis de circuitos** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Dispositivos semiconductores** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Amplificadores operacionales** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Filtros y respuesta en frecuencia** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Conversión y control** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Seguridad y verificación** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Sistemas y Señales

- **U1: Señales, variables independientes y modelos** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Sistemas LTI, impulso y convolución** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Series y transformada de Fourier en tiempo continuo** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Transformada de Laplace, funciones de transferencia y estabilidad** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Muestreo, reconstrucción y aliasing** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Sistemas discretos, DTFT y transformada Z** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Filtrado digital y respuesta en frecuencia** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Validación reproducible en señales biomédicas** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Teoría de Señal y Biocomputación

- **U1: Señales biológicas como información** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Muestreo y preprocesamiento** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Representaciones tiempo-frecuencia** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Extracción de características** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Modelos biocomputacionales** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Reproducibilidad e interpretación** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Álgebra

- **U1: Lenguaje algebraico, ecuaciones y modelado** — 38 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Sistemas de ecuaciones lineales** — 37 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Vectores, bases y ortogonalidad** — 37 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Matrices y transformaciones lineales** — 38 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Autovalores, modos y descomposición en valores singulares** — 38 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Mínimos cuadrados, modelos lineales y validación** — 44 candidatos; 12 autoevaluaciones; 2 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Biología Celular y Tisular

- **U1: La célula como sistema vivo organizado** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Membrana plasmática, transporte y gradientes** — 32 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Organelos, compartimentalización y tráfico intracelular** — 32 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Núcleo, cromatina y expresión génica en contexto celular** — 32 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Citoesqueleto, forma celular, adhesión y organización tisular** — 32 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Comunicación celular y transducción de señales** — 32 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U7: Metabolismo celular, mitocondria, estrés y control de calidad** — 32 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U8: Ciclo celular, proliferación, diferenciación y muerte celular** — 32 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U9: Métodos experimentales en biología celular** — 32 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U10: Biología celular aplicada a enfermedad, tecnología y medicina regenerativa** — 32 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Biología de Sistemas y Modelado Cuantitativo

- **U1: Pensamiento sistémico, escalas y formulación de modelos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Cinética bioquímica y modelos deterministas** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Retroalimentación, estabilidad y dinámica no lineal** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Modelos estocásticos y ruido biológico** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Redes biológicas, motivos y modelos nulos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Metabolismo constraint-based y análisis de flujo** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Estimación, identificabilidad, sensibilidad y validación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Modelos multiescala, estándares y traslación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Biología del Desarrollo

- **U1: Principios, modelos y evidencia en biología del desarrollo** — 36 candidatos; 10 autoevaluaciones; 3 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Línea germinal, determinación sexual y gametogénesis** — 35 candidatos; 10 autoevaluaciones; 3 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Fecundación, activación y transición materno-cigótica** — 36 candidatos; 10 autoevaluaciones; 3 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Segmentación, blastulación, implantación y tejidos extraembrionarios** — 35 candidatos; 10 autoevaluaciones; 3 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Gastrulación, capas germinales y ejes corporales** — 33 candidatos; 10 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Redes reguladoras, señalización, morfógenos y segmentación** — 38 candidatos; 10 autoevaluaciones; 3 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U7: Morfogénesis, mecánica y comportamientos celulares** — 37 candidatos; 10 autoevaluaciones; 3 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U8: Neurodesarrollo, cresta neural, placodas y sistemas sensoriales** — 48 candidatos; 13 autoevaluaciones; 4 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito
- **U9: Somitas, músculo, esqueleto y extremidades** — 38 candidatos; 10 autoevaluaciones; 3 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U10: Corazón, sangre, vasculatura y riñón** — 46 candidatos; 12 autoevaluaciones; 4 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito
- **U11: Intestino, hígado, páncreas, pulmón y gónadas** — 38 candidatos; 10 autoevaluaciones; 3 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U12: Células madre, regeneración, organoides y modelos embrionarios** — 38 candidatos; 10 autoevaluaciones; 3 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U13: Desarrollo humano, placenta, anomalías congénitas y teratología** — 53 candidatos; 14 autoevaluaciones; 4 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito
- **U14: Evo-devo, plasticidad, ambiente y síntesis ética** — 39 candidatos; 10 autoevaluaciones; 3 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Biología I

- **U1: La vida y el método científico** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Química de la vida** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Célula y membranas** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Metabolismo celular** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Información genética** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Diversidad y evolución** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Biología II

- **U1: Genética y variación** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Evolución y filogenia** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Forma y función animal** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Regulación y respuesta** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Ecología y salud** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Integración experimental** — 32 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Biología Molecular

- **U1: Genomas y ácidos nucleicos** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Replicación y reparación** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Transcripción y procesamiento de ARN** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Traducción y proteostasis** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Regulación y epigenética** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Tecnologías moleculares** — 33 candidatos; 10 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Biología Molecular y Celular Aplicada

- **U1: Diseño experimental molecular y celular** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Cuantificación de ADN y ARN** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Análisis de proteínas** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Manipulación celular** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Fenotipado funcional** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Traslación, reproducibilidad y bioseguridad** — 30 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Biología Sintética

- **U1: Diseño de sistemas biológicos y ciclo DBTL** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Partes, expresión y contexto celular** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Circuitos genéticos, dinámica y comportamiento poblacional** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Modelado, identificabilidad y control** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Construcción conceptual, edición y verificación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Ingeniería metabólica y bioproducción** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Aplicaciones biomédicas y validación traslacional** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Biocontención, bioseguridad y gobernanza responsable** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Biomarcadores y Diagnóstico Molecular

- **U1: Biomarcadores, categorías y contextos de uso** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Biospecímenes, fase preanalítica y variación biológica** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Plataformas de medición y diseño de ensayos moleculares** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Validación analítica y calidad de la medición** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Desempeño clínico y exactitud diagnóstica** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Descubrimiento, ómicas y modelos multivariables** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Utilidad clínica, cualificación y regulación** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Implementación, regulación y vigilancia del ciclo de vida** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Bioquímica

- **U1: Estructura de biomoléculas** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Enzimas y regulación** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Bioenergética** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Metabolismo central** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Metabolismo integrado** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Bioquímica clínica y experimental** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Farmacología, Farmacocinética y Farmacodinámica

- **U1: Dianas farmacológicas, receptores y transducción** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Dosis, concentración, respuesta y ventana terapéutica** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Absorción, distribución, metabolismo y excreción** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Parámetros farmacocinéticos, modelos y regímenes** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Modelos PK/PD y relaciones exposición-respuesta** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Variabilidad, poblaciones especiales e interacciones** — 29 candidatos; 8 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Seguridad farmacológica, reacciones adversas y monitorización** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Desarrollo clínico, selección de dosis y farmacología de precisión** — 29 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Fisiología de Sistemas

- **U1: Pensamiento sistémico y homeostasis** — 80 candidatos; 12 autoevaluaciones; 5 casos; 15 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U2: Integración neuroendocrina** — 80 candidatos; 12 autoevaluaciones; 5 casos; 15 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U3: Acoplamiento cardiorrespiratorio** — 84 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U4: Balance renal y metabólico** — 84 candidatos; 12 autoevaluaciones; 5 casos; 15 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U5: Inflamación e inmunidad sistémica** — 95 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Modelos integradores y datos** — 70 candidatos; 12 autoevaluaciones; 5 casos; 15 fuentes. Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Fisiología Humana I

- **U1: Homeostasis, compartimentos y transporte** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Neurofisiología: excitabilidad, sinapsis e integración** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Fisiología muscular: activación, fuerza, fatiga y adaptación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Fisiología cardiovascular: bomba, vasos y regulación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Fisiología respiratoria: ventilación, intercambio y transporte** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Integración cardiorrespiratoria, ejercicio, altitud y recuperación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Fisiología Humana II

- **U1: Fisiología renal y balance hidroelectrolítico** — 28 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Equilibrio ácido-base y compensación** — 28 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Motilidad, secreción, digestión y absorción** — 28 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Endocrinología integrada: ejes, ritmos y respuesta tisular** — 29 candidatos; 8 autoevaluaciones; 2 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Fisiología reproductiva, embarazo y lactancia** — 29 candidatos; 8 autoevaluaciones; 2 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Integración fisiológica: ejercicio, temperatura, estrés y envejecimiento** — 29 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Fisiopatología Humana

- **U1: Lesión celular, inflamación y reparación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Aterosclerosis, trombosis, insuficiencia cardiaca y shock** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Fisiopatología respiratoria y renal** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Fisiopatología endocrina y metabólica** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Cáncer e inmunopatología** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Casos integrados, biomarcadores y evidencia** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Genética

- **U1: Organización cromosómica, meiosis y recombinación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Herencia mendeliana, probabilidad y pedigríes** — 27 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Variación genética, mutación y detección** — 27 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Relación genotipo-fenotipo y regulación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Genética de poblaciones y rasgos complejos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Medicina genómica, interpretación y ética** — 27 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Histoanatomía Humana

- **U1: Métodos y organización corporal** — 69 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U2: Tejidos básicos** — 71 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U3: Sistema musculoesquelético** — 85 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U4: Sistemas cardiovascular y respiratorio** — 92 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U5: Sistemas digestivo, renal y endocrino** — 100 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Sistemas nervioso y reproductor** — 113 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.

### Ingeniería de Tejidos

- **U1: Tríada de ingeniería de tejidos** — 46 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Células y fuentes** — 46 candidatos; 10 autoevaluaciones; 4 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Biomateriales y andamios** — 48 candidatos; 10 autoevaluaciones; 4 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Transporte y biorreactores** — 51 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Evaluación preclínica** — 51 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Traslación y manufactura** — 47 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Inmunología e Inmunopatología

- **U1: Arquitectura inmunitaria, reconocimiento y homeostasis** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Inmunidad innata, barreras, complemento e inflamación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Antígeno, HLA y activación de linfocitos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Células B, anticuerpos, centros germinales y memoria humoral** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Células T, funciones efectoras, regulación y memoria** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Defensa del huésped, inmunidad mucosal y vacunación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Hipersensibilidad, autoinmunidad, autoinflamación e inmunodeficiencia** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Trasplante, inmunidad tumoral, inmunoterapia y medición clínica** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Microbiología Médica y Enfermedades Infecciosas

- **U1: Fundamentos microbianos, ecología y relación con el huésped** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Interacción huésped-patógeno y mecanismos de daño** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Diagnóstico microbiológico y gestión de la incertidumbre** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Susceptibilidad antimicrobiana y mecanismos de resistencia** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Bacteriología clínica y razonamiento sindrómico** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Virología, micología y parasitología médicas** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Prevención, control de infecciones, bioseguridad y brotes** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Vigilancia, epidemiología genómica, One Health y gobernanza de AMR** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Nanobiotecnología

- **U1: Escala nanométrica y propiedades** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Nanomateriales** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Interfaz nano-bio** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Liberación y direccionamiento** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Nanosensores e imagen** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Nanoseguridad y traslación** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Ómicas de Célula Única y Biología Espacial

- **U1: Diseño experimental, tecnologías y objetos de datos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Procesamiento inicial y control de calidad** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Normalización, selección de características y representación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Clustering, marcadores, anotación y atlas de referencia** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Inferencia entre muestras y composición celular** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Integración, multimodalidad y dinámica celular** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Arquitectura espacial, imágenes, registro y segmentación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Estadística espacial, nichos y validación traslacional** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Análisis Instrumental

- **U1: Metrología, muestreo y sistema de medición** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Calibración, incertidumbre y límites analíticos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Absorción, fluorescencia y detección óptica** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Espectroscopía vibracional e identidad molecular** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Métodos electroanalíticos y transducción** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Cromatografía, electroforesis y ciencia de separación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Espectrometría de masas y métodos acoplados** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Validación, control de calidad y decisión biomédica** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Aplicaciones de Salud Digital

- **U1: Necesidades y ecosistema digital** — 48 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Diseño centrado en personas** — 48 candidatos; 10 autoevaluaciones; 4 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Telemedicina y monitorización** — 49 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Datos e interoperabilidad** — 51 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Evaluación clínica y económica** — 59 candidatos; 12 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Privacidad, regulación e implementación** — 57 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Biofotónica

- **U1: Interacción luz-tejido** — 47 candidatos; 10 autoevaluaciones; 5 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Fuentes y detectores** — 39 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Óptica de tejidos** — 51 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Microscopía y espectroscopía** — 55 candidatos; 10 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Fototerapia y dosimetría** — 51 candidatos; 10 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Validación y traslación** — 52 candidatos; 10 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Bioinformática

- **U1: Datos biológicos, bases y reproducibilidad** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U2: Alineamiento, similitud, homología y filogenia** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U3: Genómica, mapeo y análisis de variantes** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U4: Transcriptómica, cuantificación y expresión diferencial** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U5: Análisis funcional, rutas y redes biológicas** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos
- **U6: Pipelines reproducibles, pruebas y escalabilidad** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos

### Bioinstrumentación

- **U1: Mensurando, sistema de medición y cadena de trazabilidad** — 27 candidatos; 8 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Sensores, transductores y modelos estáticos y dinámicos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Biopotenciales, electrodos e interfaz electrodo-tejido** — 27 candidatos; 8 autoevaluaciones; 2 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Acondicionamiento analógico, ruido y rechazo de interferencias** — 27 candidatos; 8 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Muestreo, conversión y adquisición digital** — 27 candidatos; 8 autoevaluaciones; 2 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Sensores mecánicos, térmicos, de flujo y ópticos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Aislamiento, seguridad eléctrica y compatibilidad electromagnética** — 27 candidatos; 8 autoevaluaciones; 2 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Caracterización de desempeño, calibración e incertidumbre** — 27 candidatos; 8 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U9: Verificación, validación, riesgo y aptitud para el uso** — 29 candidatos; 9 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U10: Integración y expediente reproducible** — 29 candidatos; 9 autoevaluaciones; 2 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Biomateriales

- **U1: Clases y propiedades** — 43 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Estructura-propiedad** — 43 candidatos; 10 autoevaluaciones; 4 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Interfaz material-biología** — 48 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Degradación y corrosión** — 55 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Caracterización** — 51 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Diseño y evaluación preclínica** — 53 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Biomateriales e Implantes

- **U1: Implantes y requisitos clínicos** — 48 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Materiales implantables** — 50 candidatos; 10 autoevaluaciones; 4 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Fijación e integración** — 57 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Desgaste, corrosión y fatiga** — 55 candidatos; 10 autoevaluaciones; 5 casos; 14 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Implantes específicos** — 53 candidatos; 10 autoevaluaciones; 5 casos; 15 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Evaluación y vigilancia** — 53 candidatos; 10 autoevaluaciones; 5 casos; 13 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Biomecánica

- **U1: Cinemática del movimiento humano** — 37 candidatos; 10 autoevaluaciones; 3 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Cinética** — 39 candidatos; 10 autoevaluaciones; 5 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Mecánica musculoesquelética** — 41 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Tejidos biológicos** — 41 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Medición y modelado** — 44 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Aplicaciones clínicas** — 49 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Biomecánica de Medios Continuos

- **U1: Descripción continua de tejidos** — 33 candidatos; 8 autoevaluaciones; 3 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Esfuerzo y equilibrio** — 45 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Elasticidad** — 51 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Viscoelasticidad y poroelasticidad** — 51 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Fluidos biológicos** — 51 candidatos; 10 autoevaluaciones; 5 casos; 17 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Elementos finitos y validación** — 56 candidatos; 10 autoevaluaciones; 5 casos; 15 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Biosensores

- **U1: Arquitectura de un biosensor** — 40 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Reconocimiento biológico** — 40 candidatos; 10 autoevaluaciones; 4 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Transducción** — 49 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Inmovilización y microfluídica** — 49 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Desempeño analítico** — 49 candidatos; 10 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Biosensores clínicos y portátiles** — 52 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Desarrollo de Dispositivos Médicos

- **U1: Necesidad clínica y usuarios** — 43 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Requisitos y arquitectura** — 47 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Gestión de riesgos** — 49 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito
- **U4: Prototipado y verificación** — 50 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Validación y evidencia** — 51 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Regulación y transferencia** — 51 candidatos; 10 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Electrofísica y Electromecánica

- **U1: Campos y propiedades eléctricas** — 49 candidatos; 10 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Magnetismo e inducción** — 50 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Circuitos electromecánicos** — 62 candidatos; 12 autoevaluaciones; 5 casos; 12 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U4: Transductores** — 68 candidatos; 12 autoevaluaciones; 5 casos; 15 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U5: Actuadores y control** — 80 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Seguridad e integración** — 85 candidatos; 12 autoevaluaciones; 5 casos; 15 fuentes. Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Electrónica

- **U1: Diodos y rectificación** — 47 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Transistores** — 49 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Amplificación analógica** — 51 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Filtros y osciladores** — 49 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Electrónica digital** — 53 candidatos; 10 autoevaluaciones; 6 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Diseño y prueba** — 55 candidatos; 10 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Evaluación Computacional de Evidencia Terapéutica

- **U1: Pregunta terapéutica y jerarquía de evidencia** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Gobernanza de datos químicos y bioactivos** — 29 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Representaciones, similitud y validez de medición** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Evaluación crítica de evidencia estructural** — 29 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Validación de modelos predictivos y aplicabilidad** — 31 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Incertidumbre, riesgo y decisión multiobjetivo** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Auditoría de IA generativa y aprendizaje activo** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Validación experimental conceptual y reporte responsable** — 29 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Fundamentos de Biomecánica

- **U1: Vectores, fuerzas y momentos** — 40 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Cinemática** — 40 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Dinámica y energía** — 40 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Propiedades mecánicas de tejidos** — 42 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Antropometría y articulaciones** — 42 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Medición biomecánica** — 53 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Historias Clínicas, Terminologías y Estándares

- **U1: Historia clínica electrónica** — 85 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U2: Modelos de información** — 85 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U3: Terminologías clínicas** — 90 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U4: Interoperabilidad** — 88 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U5: Calidad, privacidad y gobernanza** — 90 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Implementación y validación** — 89 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.

### Imágenes Biomédicas

- **U1: Formación y representación de imagen** — 48 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Radiografía y tomografía** — 49 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Resonancia magnética** — 55 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Ultrasonido** — 58 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Medicina nuclear y óptica** — 62 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Calidad, artefactos y seguridad** — 55 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Imágenes Biomédicas Avanzadas I

- **U1: Reconstrucción tomográfica** — 83 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U2: MRI avanzada** — 90 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U3: Ultrasonido avanzado** — 94 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U4: Imagen nuclear cuantitativa** — 94 candidatos; 12 autoevaluaciones; 5 casos; 19 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U5: Registro y fusión** — 93 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Control de calidad cuantitativo** — 75 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.

### Imágenes Biomédicas Avanzadas II

- **U1: Medición cuantitativa, incertidumbre y biomarcadores de imagen** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Mapas paramétricos y modelos dinámicos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Segmentación avanzada y referencia estándar** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Radiomics estandarizada y estabilidad de características** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Aprendizaje automático para clasificación, detección y pronóstico** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Generalización, sesgo y evaluación externa** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Imagen guiada, navegación e intervención** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Despliegue clínico y ciclo de vida** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Informática Biomédica

- **U1: Datos, información y conocimiento en salud** — 88 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U2: Sistemas de información clínica** — 91 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U3: Interoperabilidad y terminologías** — 113 candidatos; 14 autoevaluaciones; 5 casos; 23 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U4: Analítica y apoyo a decisiones** — 81 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U5: Interacción y factores humanos** — 89 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Gobernanza e implementación** — 91 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.

### Ingeniería Clínica y Gestión

- **U1: Función de ingeniería clínica** — 45 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Inventario y criticidad** — 47 candidatos; 10 autoevaluaciones; 4 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Mantenimiento y metrología** — 49 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Adquisición y evaluación** — 49 candidatos; 10 autoevaluaciones; 5 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Seguridad y incidentes** — 53 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Proyectos y mejora** — 53 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Ingeniería de Datos Biomédicos

- **U1: Fuentes y arquitectura de datos** — 95 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U2: Ingesta y transformación** — 95 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U3: Almacenamiento y modelado** — 87 candidatos; 12 autoevaluaciones; 5 casos; 14 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U4: Calidad y procedencia** — 97 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U5: Orquestación y observabilidad** — 97 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U6: Privacidad y productos de datos** — 85 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. P1: autoevaluaciones sin razonamiento explícito

### Ingeniería Neurosensorial

- **U1: Sistemas sensoriales** — 82 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U2: Registro neural** — 88 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U3: Estimulación** — 88 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U4: Prótesis sensoriales** — 85 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U5: Interfaces y decodificación** — 86 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U6: Validación y neuroética** — 93 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. P1: autoevaluaciones sin razonamiento explícito

### Interfaces Hombre-Máquina

- **U1: Factores humanos** — 83 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U2: Investigación de usuarios** — 80 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. P1: autoevaluaciones sin razonamiento explícito
- **U3: Diseño de interacción** — 91 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U4: Accesibilidad y diseño inclusivo** — 85 candidatos; 12 autoevaluaciones; 5 casos; 19 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U5: Evaluación de usabilidad** — 82 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Interfaces avanzadas** — 83 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.

### Laboratorio de Bioinstrumentación

- **U1: Seguridad, metrología y bitácora** — 49 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Caracterización de sensores** — 49 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Amplificación de biopotenciales** — 50 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Filtrado y adquisición** — 58 candidatos; 11 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Integración de prototipo** — 58 candidatos; 11 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Verificación y reporte** — 58 candidatos; 11 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Laboratorio de Biomecánica

- **U1: Protocolo y calibración** — 53 candidatos; 12 autoevaluaciones; 4 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Análisis cinemático** — 41 candidatos; 10 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito
- **U3: Plataformas de fuerza** — 41 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito
- **U4: EMG de superficie** — 53 candidatos; 10 autoevaluaciones; 5 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Dinámica inversa** — 58 candidatos; 12 autoevaluaciones; 6 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Informe y reproducibilidad** — 56 candidatos; 12 autoevaluaciones; 6 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Laboratorio de Imágenes Biomédicas

- **U1: Datos DICOM y visualización** — 94 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U2: Calidad de imagen** — 85 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U3: Preprocesamiento reproducible sin fuga de información** — 39 candidatos; 8 autoevaluaciones; 2 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Segmentación reproducible y evaluación de máscaras** — 60 candidatos; 12 autoevaluaciones; 4 casos; 17 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U5: Registro espacial y medición longitudinal reproducible** — 65 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Proyecto de análisis** — 90 candidatos; 15 autoevaluaciones; 5 casos; 18 fuentes. Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Laboratorio de Señales Biomédicas

- **U1: Adquisición y seguridad** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Inspección y calidad** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Preprocesamiento** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Extracción de eventos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Características y comparación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Pipeline reproducible** — 27 candidatos; 8 autoevaluaciones; 2 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Machine Learning Biomédico y Validación de Modelos Clínicos

- **U1: Pregunta clínica, uso previsto y estimando predictivo** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Datos clínicos, cohortes, etiquetas y fuga de información** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Desarrollo de modelos y referentes clínicos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Validación interna, optimismo e incertidumbre** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Validación externa, transportabilidad y actualización** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Discriminación, calibración y utilidad clínica** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Sesgo, equidad, explicabilidad y equipo humano-IA** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Evaluación prospectiva, despliegue y ciclo de vida** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Modelado y Simulación en Biomedicina

- **U1: Formulación del modelo** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Modelos deterministas** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Modelos estocásticos y de agentes** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Estimación y sensibilidad** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Verificación y validación** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Simulación para decisiones** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### NLP y Recuperación de Información

- **U1: Texto biomédico y representación** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Recuperación de información** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Clasificación y extracción** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Modelos de lenguaje** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Evaluación** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Privacidad, sesgo y despliegue** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Polímeros y Procesamiento de Materiales

- **U1: Estructura y síntesis de polímeros** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Propiedades térmicas y mecánicas** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Procesamiento** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Superficies y aditivos** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Polímeros biomédicos** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Caracterización y calidad** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Señales Biomédicas

- **U1: Origen y adquisición** — 45 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Calidad y preprocesamiento** — 45 candidatos; 10 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Análisis temporal** — 47 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Análisis frecuencial** — 47 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Características y modelos** — 49 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Interpretación y despliegue** — 55 candidatos; 10 autoevaluaciones; 5 casos; 12 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Simulación y Planificación Quirúrgica

- **U1: Flujo de planificación** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Segmentación y modelos 3D** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Planificación geométrica** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Simulación física** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Navegación y realidad extendida** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Validación y factores humanos** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Sistemas de Ayuda a la Decisión Médica

- **U1: Decisión clínica y casos de uso** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Conocimiento y reglas** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Modelos predictivos** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Integración e interfaz** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Validación clínica** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Gobernanza y monitorización** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Tratamiento Digital de Imágenes

- **U1: Imagen digital** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Transformaciones de intensidad** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Filtrado espacial** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Procesamiento frecuencial** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Morfología y segmentación** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Evaluación y reproducibilidad** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Ciencia Regulatoria, Calidad y Seguridad de Tecnologías Médicas

- **U1: Ciencia regulatoria, propósito previsto y clasificación** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U2: Rutas regulatorias y estrategia de evidencia** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U3: Sistemas de gestión de calidad y controles de diseño** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U4: Gestión de riesgos, beneficio-riesgo y factores humanos** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U5: Evaluación clínica, desempeño y evidencia** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U6: Software, SaMD, IA y ciberseguridad** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U7: Fabricación, proveedores, validación y cambios** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)
- **U8: Vigilancia, incidentes, acciones de campo y ciclo de vida** — 29 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: autoevaluaciones sin razonamiento explícito; P1: menos de cuatro casos resueltos; Revisar profundidad: menos de 1000 palabras de teoría (indicador, no veredicto)

### Comunicación Científica

- **U1: Pregunta, audiencia y propósito** — 45 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Estructura de argumentos** — 46 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Escritura académica** — 46 candidatos; 10 autoevaluaciones; 5 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Visualización y presentaciones** — 46 candidatos; 10 autoevaluaciones; 5 casos; 6 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Divulgación y medios** — 47 candidatos; 10 autoevaluaciones; 5 casos; 7 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Integridad, revisión y publicación** — 48 candidatos; 10 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Economía y Gestión de Empresas

- **U1: Economía y valor en salud** — 43 candidatos; 10 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Contabilidad y finanzas** — 51 candidatos; 10 autoevaluaciones; 6 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Operaciones y procesos** — 54 candidatos; 11 autoevaluaciones; 6 casos; 11 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Mercado y estrategia** — 53 candidatos; 13 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Evaluación económica** — 56 candidatos; 13 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Gobernanza y desempeño** — 53 candidatos; 12 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad

### Historia y Filosofía de la Ciencia

- **U1: Orígenes y transformación de la ciencia** — 83 candidatos; 12 autoevaluaciones; 5 casos; 15 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U2: Método, explicación y causalidad** — 85 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U3: Paradigmas y cambio científico** — 85 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U4: Medición, clasificación y objetividad** — 81 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U5: Ciencia, sociedad y poder** — 87 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Ciencia contemporánea** — 92 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.

### Innovación y Emprendimiento

- **U1: Problema y necesidad** — 82 candidatos; 12 autoevaluaciones; 5 casos; 15 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U2: Propuesta de valor** — 84 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U3: Prototipo y experimentos** — 79 candidatos; 12 autoevaluaciones; 5 casos; 17 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U4: Modelo de negocio y acceso** — 86 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U5: Propiedad intelectual y regulación** — 76 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U6: Financiación y comunicación** — 85 candidatos; 12 autoevaluaciones; 5 casos; 18 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.

### Laboratorio de Globalización y Emprendimiento

- **U1: Retos globales de salud** — 85 candidatos; 12 autoevaluaciones; 5 casos; 16 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.
- **U2: Investigación de contexto** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Codiseño de solución** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Validación de campo** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Escalado responsable** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Proyecto integrador** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Políticas Públicas de Ciencia y Tecnología

- **U1: Sistemas de ciencia, tecnología e innovación** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Formulación de políticas** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Evidencia para decisiones** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Regulación de tecnologías sanitarias** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Equidad, propiedad intelectual y acceso** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Evaluación y rendición de cuentas** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Tecnologías de Administración

- **U1: Procesos e información organizativa** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Planificación y colaboración** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Sistemas empresariales** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Analítica de gestión** — 27 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Automatización de procesos** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Seguridad y cambio organizativo** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Uso Profesional del Inglés

- **U1: Comunicación científica esencial** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U2: Lectura crítica** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U3: Escritura profesional** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U4: Presentaciones y reuniones** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U5: Documentación técnica** — 26 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos
- **U6: Carrera y colaboración intercultural** — 25 candidatos; 8 autoevaluaciones; 2 casos; 5 fuentes. P0: contenido de plantilla; examen bloqueado; P1: banco inferior a la meta editorial de 60 preguntas por unidad; P1: menos de cuatro casos resueltos

### Ética y Responsabilidad Social

- **U1: Teorías y principios éticos** — 51 candidatos; 12 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U2: Ética de investigación** — 56 candidatos; 12 autoevaluaciones; 5 casos; 8 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U3: Datos e inteligencia artificial** — 50 candidatos; 12 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U4: Tecnologías y acceso** — 52 candidatos; 12 autoevaluaciones; 5 casos; 9 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U5: Ambiente y cadena de suministro** — 54 candidatos; 12 autoevaluaciones; 5 casos; 10 fuentes. P1: banco inferior a la meta editorial de 60 preguntas por unidad
- **U6: Deliberación y rendición de cuentas** — 60 candidatos; 14 autoevaluaciones; 5 casos; 11 fuentes. Sin alertas de los indicadores examinados; revisión científica pendiente.

## Referencia metodológica

NBME, recursos públicos sobre blueprinting y construcción de ítems: https://www.nbme.org/news/nbme-educator-guides-now-available-test-blueprinting-and-osce-topic-areas/ y https://www.nbme.org/institutions/nbme-item-writing-guide/ (consultados 2026-10-11). Se consultaron las páginas de presentación; no se afirma haber revisado el manual completo ni que estos bancos tengan validación NBME.
