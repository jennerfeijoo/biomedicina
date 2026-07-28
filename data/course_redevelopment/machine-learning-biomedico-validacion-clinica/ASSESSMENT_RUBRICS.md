# Rúbricas de evaluación

## Prácticas reproducibles — 30 %

| Criterio | Excelente | Aceptable | Insuficiente |
|---|---|---|---|
| Trazabilidad | Datos, versiones, semillas, parámetros y exclusiones pueden reconstruirse. | La mayor parte del flujo está documentada. | No es posible reproducir decisiones o resultados. |
| Particiones | Respeta paciente, tiempo, centro y disponibilidad de variables. | La partición principal es correcta con omisiones menores. | Existe fuga o reutilización del conjunto de prueba. |
| Métricas | Selecciona e interpreta métricas según prevalencia y uso previsto. | Calcula métricas correctas con interpretación parcial. | Usa una métrica aislada o concluye más de lo que permite. |
| Incertidumbre | Presenta intervalos, variabilidad y análisis de sensibilidad. | Incluye incertidumbre limitada. | Reporta solo estimaciones puntuales. |

## Críticas TRIPOD+AI y PROBAST+AI — 20 %

- 30 %: identificación correcta del tipo de estudio y alcance.
- 30 %: evaluación de participantes, predictores, desenlace y análisis.
- 20 %: distinción entre calidad del desarrollo, riesgo de sesgo y aplicabilidad.
- 20 %: recomendaciones concretas y proporcionales a la evidencia.

## Proyecto acumulativo — 40 %

| Criterio | Peso |
|---|---:|
| Uso previsto, población y estimando | 15 % |
| Calidad de datos y prevención de leakage | 15 % |
| Baseline, pipeline y reproducibilidad | 15 % |
| Validación interna y externa | 20 % |
| Calibración, utilidad y subgrupos | 15 % |
| Evaluación prospectiva y ciclo de vida | 10 % |
| Comunicación de límites y riesgos | 10 % |

## Defensa crítica — 10 %

La defensa no premia complejidad algorítmica. Evalúa si el estudiante puede justificar:

- por qué el problema es predictivo y no causal;
- qué información existe en el momento de uso;
- por qué las particiones son independientes;
- qué aporta el modelo frente al baseline;
- qué evidencia falta para uso clínico;
- qué condiciones obligarían a recalibrar, restringir o retirar el sistema.
