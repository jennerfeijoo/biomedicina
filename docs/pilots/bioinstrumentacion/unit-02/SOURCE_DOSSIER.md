# Dossier de fuentes · Bioinstrumentación Unidad 2

## Propósito

Este dossier delimita qué afirmaciones pueden sostener la preparación de **Sensores, transductores y modelos estáticos y dinámicos**. No autoriza todavía la teoría completa ni convierte documentación de un componente en evidencia sobre una cadena biomédica.

## Fuentes terminológicas primarias

### VIM3 3.7 — transductor de medición

Permite afirmar que un transductor proporciona una cantidad de salida con una relación especificada respecto de una cantidad de entrada. Sus ejemplos incluyen termopar, galga extensométrica y tubo de Bourdon.

No permite afirmar que la relación sea lineal, exacta, rápida o adecuada para un uso clínico.

### VIM3 3.8 — sensor

Permite definir el sensor como el elemento directamente afectado por el fenómeno, cuerpo o sustancia que porta la cantidad que se pretende medir.

La frontera funcional debe declararse: un elemento sensible puede formar parte de un transductor más amplio y el transductor puede ser solo una etapa de la cadena.

### VIM3 4.12 — sensibilidad

La sensibilidad relaciona un cambio de indicación con el cambio correspondiente de la cantidad medida. Puede depender del valor de entrada y debe interpretarse con unidades e intervalo.

**Afirmación prohibida:** «mayor sensibilidad significa mejor sensor» sin analizar rango, resolución, selectividad, saturación, ruido, carga y dinámica.

### VIM3 4.13 — selectividad

La selectividad trata la independencia de las respuestas frente a distintas cantidades presentes. No es sinónimo de sensibilidad ni posee una métrica universal independiente del sistema y del ensayo.

### VIM3 4.23 — tiempo de respuesta al escalón

El término requiere un cambio abrupto especificado y límites de asentamiento especificados alrededor del valor final. No puede sustituirse automáticamente por una constante de tiempo.

## Fuente de modelado

### JCGM GUM-6:2020

Se usa para exigir:

- cantidades de entrada y salida definidas;
- relación y parámetros identificables;
- supuestos y condiciones iniciales;
- efectos omitidos y dominio de adecuación;
- justificación del nivel de simplificación.

Un modelo de primer orden es una aproximación didáctica válida solo cuando sus supuestos y pruebas se documentan.

## Fuentes de mecanismos y componentes

### Termistor NTC · Vishay

La documentación primaria permite trabajar con una relación resistencia–temperatura no lineal y con tiempos de respuesta condicionados por construcción y ensayo. No se trasladarán cifras de un componente a otro ni a temperatura tisular.

### Galga extensométrica · National Instruments

La documentación permite representar la deformación transferida a una rejilla resistiva y su lectura mediante puente. Temperatura, excitación, conductores, montaje y geometría permanecen como partes de la cadena, no como detalles accesorios.

### Fotodiodo · Hamamatsu Photonics

La documentación permite mostrar que responsividad espectral, corriente oscura, capacitancia y frecuencia de corte son propiedades distintas y dependientes de condiciones. La salida del fotodiodo no equivale a una concentración fisiológica.

## Fuentes curriculares y contextuales

MIT OpenCourseWare 20.309 y NIBIB se usan para contrastar alcance pedagógico y aplicaciones. No sustituyen definiciones metrológicas, hojas de datos ni revisión disciplinar.

## Afirmaciones autorizadas

1. Sensor y transductor pueden coincidir físicamente, pero deben distinguirse por su función en la frontera declarada.
2. La sensibilidad puede ser local y depender del punto de operación.
3. La curva estática no caracteriza por sí sola el seguimiento temporal.
4. El tiempo de respuesta depende de un estímulo y criterio definidos.
5. Un modelo dinámico debe declarar supuestos, estados, parámetros y dominio.
6. La carga puede ser eléctrica, mecánica, térmica u óptica.
7. Las especificaciones de componente no validan una cadena completa.

## Afirmaciones prohibidas

- «La hoja de datos demuestra que el sistema es exacto».
- «Un sensor rápido es exacto».
- «Sensibilidad, resolución y exactitud son equivalentes».
- «La calibración estática demuestra ancho de banda».
- «La constante de tiempo siempre es el tiempo de respuesta».
- «La corriente del fotodiodo mide directamente saturación de oxígeno».
- «La galga mide directamente fuerza o presión sin modelo estructural».

## Brechas que permanecen abiertas

- modelos de segundo orden y distribuidos;
- relación cuantitativa entre respuesta temporal y ancho de banda para casos no ideales;
- ejemplos revisados de carga sobre sistemas biológicos;
- selección de componentes exactos para la práctica comparativa;
- revisión humana por competencia en instrumentación y sistemas dinámicos.

Estas brechas bloquean la autoría completa, no la preparación documental.
