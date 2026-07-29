# Resolución del modelo estático sintético · Bioinstrumentación U2

Estado: `resolved_for_practice_implementation`

## Decisión

La práctica U2-P1 no intentará imitar un sensor comercial. Utilizará cuatro generadores sintéticos separados para que el estudiante pueda distinguir **sensibilidad local**, desplazamiento de cero, saturación, zona muerta, histéresis y ruido sin atribuir automáticamente un mecanismo físico.

Todas las curvas usarán `x` en `unidad_de_entrada` y `y` en `unidad_de_salida`, dominio `[-10, 10]`, paso `0,1` y semilla `20260729`.

## Generadores fijados

### Control lineal

`y = b + K·x + ε`, con `K = 1,8`, `b = 0,4` y desviación estándar de ruido `0,02`.

Sirve como control positivo para pendiente constante y offset dentro del dominio declarado.

### Saturación

`y = b + A·tanh(K·x/A) + ε`, con `A = 8`.

La pendiente central se aproxima a `K`, pero disminuye en los extremos. La gráfica no se describirá como lineal de manera global.

### Zona muerta

`y = b + K·sign(x)·max(|x|-d, 0) + ε`, con `d = 1,2`.

Permite distinguir una región sin respuesta utilizable de una sensibilidad global baja.

### Histéresis

`y = b + K·x + h·direction + ε`, con `h = 0,25`.

La entrada asciende de `-10` a `10` y después desciende. `direction` vale `+1` en ascenso y `-1` en descenso. La dirección del barrido será una columna obligatoria.

## Controles de aceptación

- Igual semilla y parámetros producen las mismas filas y el mismo hash.
- En el control lineal, `K` y `b` se recuperan con error máximo de 1 % sin ruido y 3 % con ruido.
- En saturación, la sensibilidad local de los extremos es menor que 20 % de la central.
- Dentro de `|x| ≤ d`, la variación de la zona muerta es menor que 10 % del cambio lineal esperado.
- La separación media de las ramas de histéresis recupera `2h` con error máximo de 5 %.
- Un ajuste lineal agrupado que ignora la dirección debe fallar el control por rama.

## Control negativo

Un `R²` alto no aprobará por sí solo una curva. En la histéresis, el gate debe detectar residuos sistemáticos opuestos entre ascenso y descenso aunque el ajuste agrupado parezca bueno.

## Límites

Los patrones son datos sintéticos. No demuestran el mecanismo de un componente real, no representan tejido, no son resultados de una persona y no constituyen validación biomédica o clínica.
