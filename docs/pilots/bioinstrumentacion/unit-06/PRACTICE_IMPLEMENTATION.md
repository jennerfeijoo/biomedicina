# Implementación de prácticas · Bioinstrumentación Unidad 6

## Estado

`implemented_internal_review`

Las prácticas `U6-P1` a `U6-P3` se implementan exclusivamente con datos y modelos sintéticos. No requieren red, participantes humanos, equipos médicos energizados ni acceso a infraestructura clínica.

## U6-P1 · Mapa de rutas de corriente y barreras

El estudiante representa una fuente de 5 V RMS, una trayectoria equivalente de 10 MΩ y las barreras conceptuales entre dominios. El cálculo determinista es:

`I = V / Z = 5 / 10 000 000 = 0.5 µA RMS`

El objetivo no es comparar con un límite normativo, sino distinguir fuente, trayectoria, retorno, impedancia, referencia, tierra de protección, blindaje y barrera.

## U6-P2 · Mecanismos de acoplamiento EMC

Se implementan cuatro casos reproducibles:

- conducido: `V_error = I_interference × Z_common`;
- capacitivo: `I_c = 2πfC_mutualV_source`;
- inductivo: `V_induced = 2πfMI_source`;
- radiado: `V_victim = coupling_gain × V_source`.

Cada caso declara fuente, víctima, trayectoria, frecuencia, amplitud, parámetros y salida esperada. Los resultados sirven para razonar sobre mecanismos y mitigaciones conceptuales; no constituyen ensayos de inmunidad, emisiones o conformidad EMC.

## U6-P3 · Fallo simple sintético

Se comparan dos estados de un modelo equivalente:

- nominal: 5 V / 10 MΩ = 0.5 µA;
- fallo simple: 5 V / 1 MΩ = 5.0 µA.

El incremento es de un factor 10. El estudiante debe separar peligro, situación peligrosa, daño posible y evidencia faltante. No se autoriza extrapolar el ejemplo a seguridad real de un dispositivo.

## Criterios de implementación

- cálculo determinista y reproducible;
- unidades explícitas;
- sin valores normativos presentados como límites;
- sin personas ni equipos médicos energizados;
- sin afirmaciones de seguridad, certificación o conformidad;
- sin aprobación profesional simulada.

## Estado editorial

La implementación de prácticas no autoriza evaluaciones, teoría completa, publicación ni finalización de Bioinstrumentación. `unit-06.json` debe permanecer ausente.
