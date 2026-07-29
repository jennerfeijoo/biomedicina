# Rúbricas de evaluación — Sistemas y Señales

## Principios

La evaluación separa exactitud matemática, implementación, validación e interpretación. Una respuesta numérica correcta sin unidades, convención o comprobación no recibe la puntuación completa.

## Problemas analíticos — 25 %

| Criterio | Peso |
|---|---:|
| Definición de dominio, unidades y supuestos | 20 % |
| Desarrollo matemático correcto | 35 % |
| Interpretación de propiedades y límites | 25 % |
| Verificación por caso límite o segunda representación | 20 % |

## Prácticas reproducibles — 30 %

| Criterio | Peso |
|---|---:|
| Datos y metadatos trazables | 20 % |
| Implementación y versiones registradas | 25 % |
| Controles sintéticos y baselines | 25 % |
| Figuras, unidades y parámetros reproducibles | 15 % |
| Limitaciones y fallos documentados | 15 % |

## Auditorías de procesamiento — 15 %

Se evalúa la capacidad para detectar convenciones ambiguas, leakage temporal, errores de muestreo, distorsión, filtros no causales presentados como tiempo real, normalizaciones incompatibles y afirmaciones que exceden la evidencia.

## Proyecto integrador — 30 %

| Criterio | Peso |
|---|---:|
| Ficha de señal y cadena de adquisición | 15 % |
| Fundamento matemático | 20 % |
| Pipeline reproducible | 20 % |
| Validación y sensibilidad | 20 % |
| Interpretación biomédica limitada | 15 % |
| Comunicación | 10 % |

## Condiciones de devolución

- unidades o frecuencia de muestreo ausentes;
- FFT sin convención de normalización o eje físico;
- selección de filtro por apariencia sin especificación;
- modificación del pipeline después de evaluar sin declararlo;
- exclusiones sin denominador;
- afirmaciones clínicas no sustentadas.
