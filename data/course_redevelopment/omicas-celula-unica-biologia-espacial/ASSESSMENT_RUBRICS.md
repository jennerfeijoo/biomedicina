# Rúbricas de evaluación

## Prácticas reproducibles — 30 %

| Criterio | Excelente | Aceptable | Insuficiente |
|---|---|---|---|
| Procedencia | Conserva conteos, metadatos, versiones, parámetros, semillas y transformaciones. | Documenta la mayor parte del flujo. | No puede reconstruirse el objeto analizado. |
| Control de calidad | Justifica decisiones por muestra y aporta sensibilidad. | Aplica controles correctos con justificación parcial. | Usa umbrales universales o elimina señal sin auditoría. |
| Representación | Separa normalización, vecinos, visualización e inferencia. | Construye una representación razonable. | Interpreta UMAP o clusters como evidencia suficiente. |
| Inferencia | Respeta muestras, donantes, covariables y multiplicidad. | El contraste principal es válido con omisiones menores. | Usa células como réplicas o ignora la estructura del diseño. |

## Auditorías de diseño e inferencia — 20 %

- 25 %: unidad experimental, réplicas, lotes y balance.
- 20 %: metadatos y procedencia.
- 20 %: riesgos de RNA ambiente, doublets, disociación y anotación.
- 20 %: pseudorreplicación, integración y multiplicidad.
- 15 %: conclusiones proporcionales y propuesta de validación.

## Proyecto acumulativo — 40 %

| Criterio | Peso |
|---|---:|
| Diseño, metadatos y pregunta | 15 % |
| Control de calidad por muestra | 15 % |
| Representación y anotación | 15 % |
| Inferencia entre muestras | 20 % |
| Integración multimodal o espacial | 20 % |
| Validación, sensibilidad y comunicación | 15 % |

## Defensa crítica — 10 %

La defensa evalúa si el estudiante puede justificar:

- por qué una célula no equivale a una réplica biológica;
- qué decisiones alteran el número y la identidad de las poblaciones;
- qué señal pudo borrarse durante integración;
- qué etiquetas son seguras y cuáles permanecen inciertas;
- qué inferencias dependen de UMAP, clustering, trayectoria o proximidad;
- qué experimento, tinción, cohorte o tecnología validaría el hallazgo principal.
