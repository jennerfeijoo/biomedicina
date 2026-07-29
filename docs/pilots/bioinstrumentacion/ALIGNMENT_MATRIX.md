# Matriz de alineación — Ruta piloto de Bioinstrumentación

**Estado:** arquitectura en revisión; unidades aún no redactadas.  
**Fuente curricular:** `data/course_planning/bioinstrumentacion-excellence.json`.  
**Contrato:** `docs/COURSE_EXCELLENCE_CONTRACT.md`.

## Principio de alineación

Una unidad no se considera desarrollada por contener teoría y preguntas. Cada resultado debe producir evidencia observable, incluir un criterio de logro, anticipar errores y ofrecer una recuperación concreta.

## Matriz por unidad

| U | Resultado dominante | Evidencia evaluable | Error crítico | Feedback diagnóstico | Recuperación | Criterio para continuar |
|---:|---|---|---|---|---|---|
| 1 | Especificar mensurando y cadena de medición | Especificación, diagrama de trazabilidad y análisis de influencias | Confundir fenómeno, señal, indicación y resultado | Contrastar la respuesta con un caso en que el instrumento modifica el fenómeno | Física I y Análisis Instrumental: unidades, medición e incertidumbre | Define cantidad, estado, condiciones, unidad, procedimiento y uso previsto sin ambigüedad |
| 2 | Relacionar transducción con respuesta estática y dinámica | Curva estática, modelo de primer orden y selección razonada | Elegir solo por sensibilidad nominal | Comparar sensores con compromisos opuestos de rango, carga, deriva y dinámica | Sistemas y Señales: sistemas de primer orden; Física II: mecanismos físicos | Justifica la selección con dominio de validez y una prueba que podría refutarla |
| 3 | Interpretar biopotenciales e interfaz electrodo-tejido | Modelo equivalente, mapa de referencia y diagnóstico de artefactos | Tratar el electrodo como conductor ideal o asumir que señal limpia implica origen fisiológico | Clasificar cada alteración como interfaz, movimiento, interferencia, referencia o fisiología | Fisiología y circuitos RC | Explica origen, camino de carga, referencia, impedancia y limitaciones |
| 4 | Diseñar acondicionamiento sin saturación ni ocultamiento | Presupuesto de rango y ruido, ganancia y respuesta en frecuencia | Usar ganancia o filtrado como solución universal | Mostrar recorte, desplazamiento de fase y pérdida de contenido en casos límite | Electrónica; Sistemas y Señales | La cadena mantiene margen, ancho de banda y trazabilidad de transformaciones |
| 5 | Justificar muestreo, ADC y adquisición | Diseño de adquisición, simulación de aliasing y diccionario de datos | Confundir bits con exactitud o usar Nyquist como regla mecánica | Comparar señal original, espectro, filtro y señal aliased | Sistemas y Señales; Fundamentos de Programación | Documenta frecuencia, anti-alias, rango, resolución, reloj, canales y unidades |
| 6 | Seleccionar familias de sensores por mecanismo y contexto | Matriz magnitud–mecanismo–desempeño–interferencia | Seleccionar por nombre comercial o por una única métrica | Obligar a reformular mensurando, entorno y dinámica | Física I/II, Biofísica y Análisis Instrumental | La selección cubre carga, rango, dinámica, matriz, calibración y riesgos |
| 7 | Analizar seguridad y compatibilidad sin inventar requisitos | Diagrama de peligros y matriz peligro–control–prueba | Suponer que baja tensión, tierra o una prueba aislada garantizan seguridad | Identificar la ruta de daño y qué barrera controla cada parte | Revisión de circuitos y consulta normativa supervisada | Distingue principio de seguridad de requisito normativo y declara lo no verificado |
| 8 | Caracterizar desempeño e incertidumbre | Curva, residuos, presupuesto de incertidumbre e informe | Usar R² o repetibilidad como validación total | Diagnosticar residuos, rango, deriva, referencias y componentes omitidos | Probabilidad/Estadística y Análisis Instrumental | Criterios definidos antes del análisis y conclusión limitada al rango probado |
| 9 | Distinguir verificación, validación, riesgo y utilidad | Matriz necesidad–requisito–peligro–control–prueba | Afirmar utilidad clínica desde desempeño técnico | Reclasificar cada evidencia y localizar el salto inferencial | Desarrollo de Dispositivos Médicos, después de completar Bioinstrumentación | Cada afirmación tiene uso, población, entorno, evidencia y limitación explícitos |
| 10 | Integrar una cadena completa de forma reproducible | Expediente, datos/código, defensa y revisión por pares | Equiparar prototipo o simulación con dispositivo validado | Auditoría por capas que reabre la unidad responsable de cada laguna | Recuperación selectiva por unidades 1–9 | El expediente es reproducible, trazable y no excede la evidencia |

## Alineación de competencias terminales

| Competencia | Unidades que la introducen | Unidades que la practican | Evidencia terminal |
|---|---|---|---|
| Especificación del mensurando y la cadena | 1 | 2–8 | Expediente U10 |
| Transducción y dinámica | 2 | 3, 6, 8 | Selección y caracterización U10 |
| Biopotenciales | 3 | 4, 5, 7 | Subcaso fisiológico o análisis comparativo |
| Acondicionamiento y adquisición | 4, 5 | 6–8 | Arquitectura y datos reproducibles |
| Selección de sensores | 2, 6 | 8, 9 | Matriz de selección defendida |
| Metrología y desempeño | 1, 8 | 2–7, 9 | Calibración e incertidumbre del proyecto |
| Seguridad, verificación y validación | 7, 9 | 10 | Matriz de trazabilidad y límites |
| Comunicación reproducible | 1 | 2–9 | Expediente y defensa U10 |

## Contrato de feedback

Cada comprobación de dominio debe almacenar o renderizar, como mínimo:

1. respuesta esperada o criterio de solución;
2. error o misconception discriminado;
3. explicación de por qué el razonamiento falla;
4. pista inicial que no revele toda la solución;
5. segunda pista más específica;
6. sección o prerrequisito para revisar;
7. problema de recuperación diferente del original;
8. criterio objetivo para continuar.

No es suficiente desplegar la respuesta dentro de un elemento `<details>`.

## Evaluación del curso

| Componente | Peso de referencia | Función |
|---|---:|---|
| Comprobaciones conceptuales con recuperación | 15 % | Detectar vocabulario, modelos y misconceptions |
| Problemas cuantitativos y de diseño | 20 % | Aplicar circuitos, señales, dinámica y metrología |
| Prácticas reproducibles con datos simulados o abiertos | 25 % | Documentar adquisición, procesamiento y validación |
| Auditorías de evidencia, riesgo y uso previsto | 15 % | Limitar afirmaciones y distinguir tipos de validación |
| Proyecto integrador y defensa | 25 % | Integrar la cadena completa y demostrar autonomía |

Los pesos no se publicarán como obligatorios hasta revisar carga, dificultad y representatividad de las tareas.

## Gates de alineación

Antes de autorizar una unidad:

- cada resultado tiene evidencia, error, feedback y recuperación;
- la práctica exige usar el mecanismo central, no solo repetir terminología;
- el ejemplo resuelto y el problema de evaluación no son el mismo caso con números cambiados;
- las fuentes utilizadas para corrección están verificadas directamente;
- el criterio de dominio permite decidir continuar o recuperar;
- la conexión biomédica no introduce interpretación clínica no enseñada.

Antes de autorizar el curso:

- las diez unidades cubren las ocho competencias terminales;
- no quedan resultados evaluados solo una vez;
- el proyecto no compensa lagunas de unidades previas;
- existe al menos una prueba de usuario por perfil objetivo;
- las remediaciones conducen a contenido disponible y suficientemente maduro.