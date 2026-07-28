# Rúbricas de evaluación

## Prácticas reproducibles — 30 %

| Criterio | Excelente | Aceptable | Insuficiente |
|---|---|---|---|
| Formulación | Variables, unidades, balances y supuestos están completos. | La estructura principal es correcta con omisiones menores. | Existen incoherencias dimensionales o variables ambiguas. |
| Implementación | Código, solver, eventos, tolerancias y pruebas son reproducibles. | La simulación funciona con documentación parcial. | El resultado depende de pasos manuales o no puede verificarse. |
| Análisis | Estabilidad, sensibilidad o flujos se interpretan con límites. | Aplica métodos correctos con interpretación incompleta. | Confunde simulación, ajuste y evidencia mecanística. |
| Evidencia | Compara modelos, incertidumbre y datos independientes. | Incluye controles limitados. | Reporta una curva ajustada sin diagnóstico ni validación. |

## Auditorías de modelos — 20 %

- 20 %: frontera, escalas, unidades y conservación.
- 20 %: estructura, cinética y método numérico.
- 20 %: identificabilidad, sensibilidad e incertidumbre.
- 20 %: comparación con modelos rivales y datos.
- 20 %: dominio de validez, falsabilidad y comunicación.

## Proyecto acumulativo — 40 %

| Criterio | Peso |
|---|---:|
| Pregunta, diagrama, balances y unidades | 15 % |
| Implementación y verificación numérica | 20 % |
| Análisis dinámico, estocástico o de flujo | 20 % |
| Estimación, sensibilidad e incertidumbre | 20 % |
| Validación y experimento discriminante | 15 % |
| Estándar interoperable y reproducibilidad | 10 % |

## Defensa crítica — 10 %

La defensa evalúa si el estudiante puede justificar:

- por qué la frontera y escala elegidas son suficientes;
- qué parámetros son identificables y cuáles no;
- qué comportamiento depende de una función objetivo o condición inicial;
- qué modelo rival explica los mismos datos;
- qué experimento distinguiría ambos mecanismos;
- qué parte del modelo puede reutilizarse y qué parte depende del contexto;
- qué conclusión sería inválida fuera del dominio de calibración.
