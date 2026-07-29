# Rúbricas de evaluación

## Principios

Las evaluaciones miden calidad de razonamiento, trazabilidad, validación e incertidumbre. No se premia producir candidatos, estructuras o recomendaciones de uso. Cualquier entrega que incluya procedimientos operativos de síntesis, fabricación, adquisición, dosificación o administración queda fuera de alcance y debe reformularse como auditoría metodológica.

## 1. Prácticas reproducibles de datos y modelado — 30 %

### Evidencia esperada

- diccionario de datos y dataset card;
- mapa de procedencia y dependencia;
- comparación controlada de representaciones;
- baseline y partición justificados;
- reporte de calibración, estabilidad, incertidumbre y aplicabilidad;
- registro de versiones, exclusiones y resultados desfavorables.

### Criterios

| Criterio | Excelente | Adecuado | Insuficiente | Error crítico |
|---|---|---|---|---|
| Procedencia | Cada dato y transformación es trazable | La mayor parte es trazable | Existen lagunas relevantes | No puede reconstruirse el origen |
| Unidad independiente | Dependencias y réplicas están correctamente tratadas | Se reconocen dependencias principales | La partición conserva dependencia | Se presenta pseudorreplicación como evidencia |
| Validación | Separación, baseline y evaluación responden al uso previsto | El diseño es razonable con límites | La evaluación es optimista o incompleta | Existe leakage o reutilización de prueba |
| Incertidumbre | Se clasifica, cuantifica cuando corresponde y modifica conclusiones | Se reportan intervalos y límites básicos | Se menciona sin efecto decisional | Se presenta certeza injustificada |
| Reproducibilidad | Versiones, reglas y resultados pueden reconstruirse | La mayoría de artefactos está documentada | Faltan pasos o versiones | El resultado depende de decisiones no registradas |

## 2. Auditorías de evidencia y modelos — 20 %

### Evidencia esperada

- cadena de evidencia y alternativas;
- auditoría estructural o predictiva;
- análisis de objetivos, oráculos y reward hacking;
- identificación de fuentes compartidas de error;
- recomendación limitada al alcance de los datos.

### Criterios

| Criterio | Excelente | Adecuado | Insuficiente | Error crítico |
|---|---|---|---|---|
| Tipo de inferencia | Separa asociación, mecanismo, predicción y decisión | Distingue categorías principales | Mezcla algunos niveles | Presenta una puntuación como mecanismo o eficacia |
| Independencia | Rastrea duplicados y fuentes compartidas | Reconoce dependencias principales | Sobreestima convergencia | Cuenta evidencia duplicada como replicación |
| Controles | Relaciona controles con modos de fallo | Propone controles pertinentes | Controles genéricos | No contempla alternativas ni negativos |
| IA generativa | Trata salidas como propuestas y audita oráculos | Reconoce límites y circularidad | Se centra en ejemplos favorables | Presenta generación como descubrimiento confirmado |
| Comunicación | Incluye contradicciones, fallos y límites | Expresa límites principales | Minimiza incertidumbre | Excede deliberadamente el alcance de evidencia |

## 3. Proyecto acumulativo — 40 %

### Entregables

1. ficha de necesidad, hipótesis y criterios de abandono;
2. dataset card y diccionario de datos;
3. informe de representación, cobertura y atajos;
4. auditoría estructural o predictiva;
5. matriz de incertidumbre, riesgo y guardrails;
6. auditoría de un sistema de IA ficticio;
7. plan experimental exclusivamente conceptual;
8. memorando de decisión.

### Rúbrica

| Dimensión | Peso | Dominio esperado |
|---|---:|---|
| Pregunta y jerarquía de evidencia | 15 % | La decisión, la hipótesis y las alternativas son explícitas y refutables |
| Datos y reproducibilidad | 20 % | Procedencia, unidades, dependencia, versiones y exclusiones son auditables |
| Representación y validación | 20 % | La comparación usa baselines, particiones realistas, calibración e incertidumbre |
| Riesgo y decisión multiobjetivo | 15 % | Los proxies, guardrails, conflictos y análisis de sensibilidad permanecen visibles |
| Validación experimental conceptual | 20 % | Controles, comparadores, criterios e independencia pueden confirmar o refutar sin protocolo operativo |
| Comunicación y límites | 10 % | Se distinguen datos, predicciones, interpretaciones y decisiones; se declara el alcance |

### Criterios de dominio

- 85–100: razonamiento reproducible, evidencia independiente, incertidumbre integrada y decisión robusta;
- 70–84: arquitectura correcta con limitaciones menores o análisis incompleto de sensibilidad;
- 55–69: entrega funcional, pero con trazabilidad, independencia o aplicabilidad insuficientes;
- menos de 55: la inferencia no puede sostenerse o no puede reproducirse.

### Fallos no compensables

- data leakage no reconocido;
- uso de resultados de prueba para ajustar la versión evaluada;
- ocultamiento de resultados desfavorables o inválidos;
- presentación de una salida generativa como evidencia confirmada;
- confusión explícita entre puntuación computacional y seguridad, eficacia o utilidad clínica;
- inclusión de procedimientos operativos para crear, obtener, dosificar o utilizar sustancias.

## 4. Defensa crítica — 10 %

La defensa evalúa si el estudiante puede justificar decisiones y modificar su conclusión ante evidencia nueva.

### Preguntas obligatorias

- ¿Qué resultado refutaría la hipótesis?
- ¿Qué fuente de incertidumbre domina la decisión?
- ¿Qué evidencia parece independiente, pero comparte origen?
- ¿Dónde comienza la extrapolación?
- ¿Qué guardrail impediría continuar?
- ¿Qué parte necesita revisión de un especialista diferente?

### Criterio de logro

La defensa es satisfactoria cuando la persona reconoce límites sin intentar proteger retrospectivamente el proyecto, distingue evidencia de recomendación y acepta detener o reformular cuando los datos no sostienen continuidad.

## Regla editorial

Superar estas rúbricas no promueve automáticamente el curso a `complete`. La madurez académica requiere revisión disciplinar documentada de contenidos, actividades, fuentes y fronteras de seguridad.