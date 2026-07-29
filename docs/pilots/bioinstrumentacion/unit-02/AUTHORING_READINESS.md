# Readiness de autoría · Bioinstrumentación Unidad 2

## Estado

```text
preparation_status: authoring_preparation_review
course_editorial_state: pending
unit_authoral_file: absent
controlled_authoring_authorized: false
unit_developed: false
public_release_authorized: false
disciplinary_review: pending_human_review
```

## Material disponible

- contrato estructurado de preparación;
- cinco resultados de aprendizaje observables;
- modelo conceptual de 17 nodos y 12 relaciones;
- tres casos limitados: termistor, galga extensométrica y fotodiodo;
- doce errores conceptuales;
- cinco evaluaciones alineadas;
- tres prácticas planificadas sin datos humanos;
- registro de once fuentes directamente consultadas;
- especificación visual con errores prohibidos.

## Qué está autorizado

- revisar alcance, resultados, modelos y fuentes;
- mejorar el banco de errores conceptuales;
- seleccionar componentes y fixtures sintéticos;
- preparar scripts de simulación en una fase posterior;
- solicitar revisión disciplinar inicial;
- ejecutar gates documentales.

## Qué no está autorizado

- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json`;
- redactar la teoría completa;
- publicar una página nueva;
- promover el curso a `developed` o `complete`;
- usar datos de personas o conectar sensores a sujetos;
- presentar especificaciones de fabricante como validación del sistema;
- declarar utilidad clínica, conformidad normativa o seguridad.

## Riesgos abiertos

1. **Dinámica:** el modelo de primer orden está delimitado, pero falta seleccionar el generador, método de estimación y controles negativos.
2. **Ancho de banda:** debe revisarse la relación entre dominio temporal y frecuencia antes de incluir equivalencias cuantitativas.
3. **Carga:** faltan casos cuantitativos revisados para interacción eléctrica, térmica, mecánica y óptica.
4. **Componentes:** deben fijarse modelos, versiones, condiciones y campos comparables.
5. **Revisión humana:** no existe aprobación disciplinar externa.

## Gate antes de implementar prácticas

Se requiere:

- ecuaciones generadoras versionadas;
- tolerancias justificadas;
- control positivo y negativo para ajuste dinámico;
- auditoría de unidades y condiciones;
- revisión de que ningún fixture simule datos humanos;
- decisión explícita de que CI valida reproducibilidad, no verdad clínica.

## Gate antes de autoría completa

Se requiere además:

- resolución documentada de los cinco riesgos abiertos;
- revisión disciplinar inicial por competencia en instrumentación y sistemas dinámicos;
- fuentes especializadas suficientes para los modelos enseñados;
- rúbricas y retroalimentación revisadas;
- autorización explícita y limitada del propietario o del proceso humano definido.

## Próximo bloque recomendado

Resolver los bloqueos técnicos de la Unidad 2: fijar generadores estático y dinámico, componentes exactos, pruebas de carga y solicitud de revisión disciplinar. La teoría completa debe continuar bloqueada durante ese bloque.
