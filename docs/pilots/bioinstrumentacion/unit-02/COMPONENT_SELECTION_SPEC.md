# Especificación de componentes fijados · Bioinstrumentación U2

Estado: `resolved_and_pinned`

La auditoría U2-P3 comparará tres componentes exactos. Las cifras se conservarán con su categoría —nominal, típica, máxima o tolerada— y con sus condiciones. Ningún dato se trasladará automáticamente al desempeño de una cadena biomédica.

## Termistor

- Fabricante: Vishay BCcomponents.
- Modelo: `NTCLG100E2103JB`.
- Documento: NTCLG100E2, documento 29050, revisión 29-Jun-2017.
- Campos fijados:
  - `R25 = 10 kΩ`;
  - tolerancia de `R25 = ±5 %`;
  - `B25/85 = 3977 K`;
  - tolerancia de `B25/85 = ±1,3 %`;
  - tiempo de respuesta declarado `0,9 s`;
  - constante de tiempo térmica declarada `6 s`;
  - factor de disipación `2,5 mW/K`.

El tiempo de respuesta y la constante de tiempo permanecen como especificaciones diferentes. La práctica debe conservar las definiciones y condiciones del documento.

## Galga extensométrica

- Fabricante: Micro-Measurements.
- Modelo: `CEA-06-125UNA-350`.
- Entrada de catálogo: patrón `125UNA`, artículo `MMF404325`.
- Campos fijados:
  - serie CEA;
  - patrón lineal de una rejilla;
  - resistencia nominal `350 Ω`;
  - STC `06`;
  - materiales objetivo declarados: acero, hierro fundido, compuestos y PCB.

No se asignará un factor de galga numérico desde una página genérica. El factor real debe proceder del paquete o certificado del lote. Adhesivo, orientación, conductores, puente, excitación y temperatura permanecen como elementos separados de la cadena.

## Fotodiodo

- Fabricante: Hamamatsu Photonics.
- Modelo: `S5821-03`.
- Campos fijados:
  - área fotosensible de `1,2 mm` de diámetro;
  - respuesta espectral `320–1100 nm`;
  - fotosensibilidad típica `0,52 A/W` a `780 nm`;
  - corriente oscura máxima `2000 pA` a `V_R = 10 V`;
  - frecuencia de corte típica `25 MHz` a `V_R = 10 V`;
  - capacitancia terminal típica `3 pF` a `V_R = 10 V` y `1 MHz`.

Los valores típicos y máximos no son intercambiables. Longitud de onda, polarización, temperatura, carga y amplificador forman parte de la interpretación.

## Tabla de extracción obligatoria

Cada componente debe documentar:

- cantidad de entrada y salida;
- principio de transducción;
- unidad;
- categoría del valor;
- condición de medida;
- rango o dominio;
- propiedad dinámica;
- carga o perturbación;
- información ausente;
- afirmaciones que no pueden transferirse al sistema.

## Transferencias prohibidas

- propiedad del componente = desempeño del sistema;
- valor típico = garantía;
- condición de laboratorio = condición biomédica;
- respuesta rápida del componente = ancho de banda de toda la cadena;
- especificación comercial = validación clínica.
