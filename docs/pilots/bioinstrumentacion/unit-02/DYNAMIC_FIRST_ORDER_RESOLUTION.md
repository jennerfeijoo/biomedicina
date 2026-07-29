# Resolución del modelo dinámico de primer orden · Bioinstrumentación U2

Estado: `resolved_for_practice_implementation`

## Modelo autorizado

La práctica U2-P2 utilizará exclusivamente el modelo lineal:

`τ·dy/dt + y = K·x(t) + b`

con `K = 1,5`, `b = 0,2`, `τ = 2 s`, `Δt = 0,02 s`, duración `16 s` y escalón unitario aplicado en `t = 2 s`.

Para una entrada constante durante cada intervalo se usará la actualización exacta:

`y[n+1] = y∞[n] + (y[n] - y∞[n])·exp(-Δt/τ)`

`y∞[n] = K·x[n] + b`

Esto evita confundir error de integración numérica con dinámica del modelo.

## Constante de tiempo y tiempo de respuesta

Ante un escalón, la fracción alcanzada después de un tiempo `t` es:

`1 - exp(-t/τ)`

Por tanto:

- a `t = τ`: `63,212 %`;
- a `t = 5τ`: más de `99,3 %`;
- banda de asentamiento de 5 %: `-τ ln(0,05) ≈ 2,996τ`;
- banda de asentamiento de 2 %: `-τ ln(0,02) ≈ 3,912τ`.

El **tiempo de respuesta** exige especificar el escalón y la banda de asentamiento. No se tratará como sinónimo universal de `τ`.

## Relación tiempo–frecuencia

Solo para `H(s)=K/(τs+1)`, la magnitud normalizada es:

`|H(j2πf)|/K = 1/sqrt(1+(2πfτ)^2)`

Bajo el criterio de magnitud `1/sqrt(2)` —equivalente a `-3 dB`— se obtiene:

`f_c = 1/(2πτ)`

Esta igualdad no se generaliza a sistemas con retardos, polos múltiples, ceros, resonancia, saturación o dinámica distribuida.

## Controles positivos

- respuesta monótona y sin sobreimpulso ante un escalón positivo;
- fracción a `τ` dentro de 0,5 puntos porcentuales de `63,212 %`;
- fracción a `5τ` superior a `99,3 %`;
- estimación de `τ` con error máximo de 1 % sin ruido y 5 % con ruido fijado;
- magnitud en `f_c` dentro de 1 % de `1/sqrt(2)`.

## Controles negativos

### Retardo puro más primer orden

Debe rechazarse el modelo simple si aparece un intervalo inicial plano mayor que `5Δt` no explicado por condiciones iniciales.

### Segundo orden subamortiguado

Una respuesta sintética con sobreimpulso superior a 1 % del cambio final debe ser rechazada por el gate de primer orden.

### Curva estática sin tiempo

No puede estimarse `τ` si faltan marcas temporales. Una calibración estática correcta no demuestra fidelidad dinámica.

## Límite editorial

Este modelo es una aproximación didáctica. Los parámetros no corresponden a un sensor, tejido o dispositivo real y el bloque no autoriza todavía la teoría completa de la Unidad 2.
