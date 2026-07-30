# Preparación autoral · Bioinstrumentación Unidad 3

## Estado

```text
preparation_status: authoring_preparation_review
technical_blockers_resolved: false
practice_implementation_authorized: false
full_theory_drafting_authorized: false
public_release_authorized: false
course_state: pending
```

## Unidad

**Biopotenciales, electrodos e interfaz electrodo-tejido**

Pregunta central: **¿Cómo se origina una diferencia de potencial fisiológica, cómo alcanza la superficie corporal y qué transforma o perturba su registro mediante electrodos?**

## Arquitectura conceptual

La unidad debe conservar cinco niveles distintos:

1. potencial transmembrana y corrientes iónicas;
2. activación de células y tejidos como fuentes distribuidas;
3. conducción de volumen y potencial extracelular;
4. interfaz electrodo–electrolito–tejido;
5. medición diferencial, referencia, artefactos e indicación.

No debe trazarse una flecha directa desde «potencial de acción» hasta «ECG/EEG/EMG» sin declarar superposición, geometría, conductor de volumen, contactos y referencia.

## Resultados previstos

- `U3-LO1`: conectar electrofisiología y diferencia superficial sin confundir escalas;
- `U3-LO2`: interpretar un modelo equivalente limitado de interfaz;
- `U3-LO3`: distinguir electrodo de medida, referencia, retorno, blindaje y tierra;
- `U3-LO4`: diagnosticar artefactos por mecanismo y prueba discriminante;
- `U3-LO5`: comparar ECG, EEG y EMG sin inferencia clínica.

## Prácticas previstas

- `U3-P1`: superposición y geometría de fuentes bioeléctricas sintéticas;
- `U3-P2`: barrido de impedancia de una interfaz equivalente;
- `U3-P3`: diagnóstico de artefactos con señales abiertas o sintéticas no clínicas.

Ninguna práctica autoriza conectar electrodos a una persona, usar equipos clínicos ni recopilar señales nuevas.

## Bloqueos técnicos pendientes

1. Fijar un modelo equivalente concreto de la interfaz, sus parámetros, unidades, dominio de frecuencia y límites.
2. Fijar un modelo sintético de fuentes distribuidas que no se presente como reconstrucción anatómica.
3. Seleccionar y congelar subconjuntos abiertos para artefactos con metadatos y licencia adecuados.
4. Definir taxonomía operativa de artefacto, interferencia y ruido.
5. Definir exactamente las funciones de referencia, retorno, blindaje y tierra en los diagramas didácticos.
6. Vincular seguridad a documentación normativa sin convertir CI o simulación en evidencia de conformidad.

## Fuentes

El registro inicial contiene fisiología de membrana, documentación de PhysioNet, un estudio reciente de impedancia de electrodo-piel y la página oficial de IEC 60601-1. Persisten vacíos especializados para el circuito equivalente de interfaz y la conducción de volumen.

## Límites editoriales

- sin interpretación diagnóstica;
- sin adquisición con personas;
- sin recomendaciones de colocación clínica;
- sin afirmar que una señal limpia es fisiológica;
- sin tratar referencia, tierra y retorno como sinónimos;
- sin declarar seguridad, desempeño esencial o conformidad.

## Próximo gate

Resolver los seis bloqueos técnicos mediante contratos deterministas antes de implementar `U3-P1` a `U3-P3` o redactar la teoría completa.
