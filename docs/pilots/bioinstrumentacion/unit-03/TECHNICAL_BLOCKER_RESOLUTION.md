# Resolución de bloqueos técnicos · Bioinstrumentación Unidad 3

## Resultado

```text
status: technical_blockers_resolved_internal_review
practice_implementation_authorized: true
assessment_implementation_authorized: false
full_theory_drafting_authorized: false
public_release_authorized: false
```

Esta resolución permite implementar únicamente las prácticas reproducibles `U3-P1`, `U3-P2` y `U3-P3`. No crea la unidad autoral, no publica contenido y no constituye revisión profesional, aprobación institucional, seguridad o conformidad.

## U3-B01 · Interfaz electrodo-tejido

Se adopta un circuito equivalente didáctico con potencial de media celda, resistencia del medio y una rama paralela `Rct-Cdl`. El circuito representa comportamiento agregado bajo condiciones declaradas. No es una anatomía física exacta ni una propiedad invariable del contacto.

La práctica deberá producir impedancia compleja y fase durante un barrido de frecuencia, mostrar sensibilidad a `Rct` y `Cdl` y declarar material, área, preparación y tiempo como variables omitidas o controladas.

## U3-B02 · Fuentes distribuidas

La señal superficial sintética se modelará como superposición temporal de fuentes ponderadas por geometría y distancia. El modelo sirve para demostrar que posición, orientación y referencia modifican un canal.

Quedan prohibidas las afirmaciones de localización celular, solución inversa, equivalencia con potencial transmembrana o realismo anatómico completo.

## U3-B03 · Datos abiertos

`U3-P3` podrá usar segmentos abiertos cuya procedencia y licencia estén registradas. Siempre debe existir una alternativa sintética offline. Los segmentos se emplean para clasificación técnica de patrones, no para diagnóstico, pronóstico o inferencia clínica.

## U3-B04 · Taxonomía de artefactos

Cada diagnóstico debe combinar:

1. patrón observado;
2. mecanismo plausible;
3. prueba discriminante;
4. limitaciones y causas alternativas.

Se separan movimiento, contacto, cable, interferencia de red, desbalance de impedancias, saturación y actividad biológica no objetivo. Artefacto, ruido e interferencia no son sinónimos.

## U3-B05 · Referencia, retorno, tierra y blindaje

La función debe declararse antes del nombre del nodo. Una entrada de referencia participa en la diferencia medida; un retorno establece una ruta funcional; el blindaje reduce ciertos acoplamientos; la tierra de protección pertenece a una arquitectura de seguridad. No se presupone que estos nodos sean equivalentes o equipotenciales.

## U3-B06 · Seguridad documental

Las prácticas son exclusivamente offline. No autorizan adquisición humana ni conexión física de electrodos. Ninguna simulación demuestra seguridad, conformidad con IEC 60601, aptitud clínica o autorización institucional.

## Próxima fase

Implementar:

- `U3-P1`: superposición y geometría de fuentes sintéticas;
- `U3-P2`: barrido de impedancia compleja del modelo equivalente;
- `U3-P3`: clasificación reproducible de artefactos con controles negativos.

La evaluación, teoría completa, revisión humana y publicación permanecen bloqueadas.
