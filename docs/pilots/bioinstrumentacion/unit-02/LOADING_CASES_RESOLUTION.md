# Resolución de casos de carga · Bioinstrumentación U2

Estado: `resolved_for_safe_cases`

La carga se tratará como interacción causal: el sistema de medición puede modificar el objeto, la interfaz o la variable que intenta observar. Los cuatro casos son de banco o simulación y no incluyen personas, muestras ni equipos clínicos.

## Carga térmica

Ruta causal:

`corriente de lectura → potencia I²R → autocalentamiento → temperatura del termistor → resistencia indicada`

Variables obligatorias: corriente o tensión de excitación, resistencia, potencia, factor de disipación, temperatura ambiente y tiempo.

La práctica comparará una condición de baja potencia con otra de excitación mayor mediante un modelo sintético. No se estimará temperatura corporal.

## Carga mecánica

Ruta causal:

`campo de deformación de la viga → adhesivo y portador → transferencia espacial → rejilla → cambio de resistencia`

La salida de una galga corresponde a la deformación transferida y promediada sobre su rejilla. Fuerza, presión o tensión mecánica requieren además geometría, propiedades del material y modelo estructural.

Variables obligatorias: geometría, campo de deformación, longitud y orientación de rejilla, adhesión, temperatura y excitación.

## Carga eléctrica

Ruta causal:

`capacitancia del fotodiodo → impedancia de entrada o realimentación → constante de tiempo eléctrica → respuesta de la cadena`

La frecuencia de corte declarada para el fotodiodo no se copiará como ancho de banda automático del sistema. Deben declararse polarización, capacitancia, resistencia o transimpedancia y ancho de banda del amplificador.

## Interacción óptica

Ruta causal:

`fuente y geometría → potencia incidente y espectro → fotocorriente → saturación o modificación del campo óptico`

Variables obligatorias: potencia radiante, longitud de onda, área iluminada, alineación, distancia, luz ambiental y responsividad.

La fotocorriente no se convertirá en concentración fisiológica ni oximetría.

## Criterio de aceptación

Cada caso debe identificar:

1. la ruta causal de carga;
2. la variable perturbada;
3. una observación que permitiría detectar el efecto;
4. una mitigación limitada, no una garantía;
5. una conclusión que permanece prohibida.

## Límites

Los ejemplos permiten razonar sobre interacción, pero no demuestran seguridad, exactitud de una cadena biomédica, utilidad clínica o conformidad normativa.
