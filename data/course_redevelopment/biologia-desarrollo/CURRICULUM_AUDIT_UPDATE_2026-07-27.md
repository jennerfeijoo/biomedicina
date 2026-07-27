# Actualización de auditoría curricular — 2026-07-27

## 1. Estado del bloque

La reconstrucción contiene 14 unidades completas, decisiones de alcance integradas, registro bibliográfico canónico, matriz de alineación, auditoría estructural de progresión y cribado léxico de redundancia. Los archivos públicos continúan sin modificaciones.

Artefactos principales:

- `SCOPE_RESOLUTIONS.md`;
- `CURRICULUM_ALIGNMENT_MATRIX.md`;
- `CURRICULUM_AUDIT.md`;
- `BIBLIOGRAPHY_POLICY.md`;
- `BIBLIOGRAPHY_AUDIT_2026-07-27.md`;
- `PROGRESSION_AND_REDUNDANCY_AUDIT.md`;
- `LEXICAL_REDUNDANCY_AUDIT_2026-07-27.md`;
- `data/source_registry/biologia-desarrollo.json`;
- `course.json`;
- `units/unit-01.json` a `units/unit-14.json`.

## 2. Brechas de alcance

### DOHaD

**Estado de decisión:** resuelto.  
**Estado de integración en `unit-13.json`:** completo.

La Unidad 13 distingue periodo crítico y sensible, trayectoria de curso de vida, mediación placentaria, biomarcador, asociación epidemiológica, epigenética e inferencia causal. Evita determinismo, predicción individual injustificada y culpabilización materna.

### Epidermis y anexos

**Estado de decisión:** resuelto.  
**Estado de integración en `unit-08.json`:** completo.

La Unidad 8 incluye ectodermo superficial, peridermo, estratificación, membrana basal, función de barrera e interacción epitelio–mesénquima en folículos y glándulas, con límites de extrapolación entre modelos y humano.

### Desarrollo inmunitario

**Estado de decisión:** resuelto y delimitado.  
**Estado de integración en `unit-10.json`:** completo.

La Unidad 10 incorpora primordio epitelial tímico, colonización linfoide, organización cortico-medular y selección de timocitos. Activación, efectores, memoria, vacunología e inmunopatología permanecen fuera y corresponden a Inmunología.

### Alcance animal, vertebrado y humano

**Estado de decisión:** resuelto.  
**Estado de integración en `course.json`:** completo.

El curso se define como biología del desarrollo animal con énfasis vertebrado, humano y biomédico. Los invertebrados funcionan como sistemas comparativos; desarrollo vegetal no forma parte del alcance.

## 3. Bibliografía

### Integridad registral

**Estado:** completo.

Resultados finales:

- 109 fuentes canónicas;
- 117 usos bibliográficos en las unidades;
- 117 usos resueltos contra el registro;
- 0 usos sin registro canónico;
- 0 duplicados exactos no resueltos;
- 0 referencias ambiguas;
- 0 coincidencias de título pendientes;
- 0 metadatos obligatorios ausentes después de resolución;
- 1 registro central activo.

El workflow `Audit course bibliography` exige:

- JSON válido en las 14 unidades;
- escapes LaTeX correctos;
- registro consolidado;
- cobertura canónica de toda referencia local;
- ausencia de colisiones, ambigüedad e incompletitud.

### Curación académica

**Estado:** pendiente.

La integridad registral no sustituye:

- revisión a texto completo de fuentes con verificación limitada;
- normalización editorial final de tipos históricos;
- selección de lecturas obligatorias, avanzadas y de consulta;
- equilibrio entre síntesis, estudios primarios, atlas, métodos y guías;
- verificación de licencias para figuras, tablas y capturas;
- revisión disciplinar de suficiencia y actualidad.

## 4. Reparación técnica de unidades

La auditoría bibliográfica detectó defectos que los controles previos no cubrían:

- JSON inválido en unidades 1–7 y 14;
- barras invertidas LaTeX no escapadas;
- secuencias como `\frac`, `\nabla` y `\tau` interpretadas como controles JSON;
- objetos finales sin llave de cierre.

Se repararon los archivos y se añadieron comprobaciones permanentes mediante:

- `scripts/repair_course_redevelopment_json.py`;
- `scripts/audit_course_bibliography.py`;
- `scripts/consolidate_course_source_registry.py`;
- `scripts/promote_unit_sources_to_registry.py`.

## 5. Repetición y progresión

### Auditoría estructural

**Estado:** completada como primera revisión editorial.

Se asignaron fronteras canónicas para los principales solapamientos:

- Unidad 1 frente al resto: jerarquía de evidencia;
- Unidades 2 y 11: línea germinal frente a organogénesis gonadal;
- Unidades 4 y 13: implantación frente a placenta posterior;
- Unidades 6 y 9: osciladores frente a somitogénesis anatómica;
- Unidad 7 frente a 8–11: principios mecánicos frente a implementación por órgano;
- Unidad 12 frente a menciones de organoides por sistema;
- Unidades 13 y 14: DOHaD frente a plasticidad evolutiva.

### Auditoría léxica

**Estado:** completada.

Resultados:

- 14 unidades;
- 1.838 bloques pedagógicos;
- 0 grupos exactos entre unidades;
- 0 pares casi duplicados sobre los umbrales configurados;
- 2 ventanas de frase solapadas correspondientes al mismo patrón de actividad experimental.

El único patrón recurrente combina trazado de linaje y perturbación en las unidades 4, 8 y 11. Se conserva porque aplica una competencia transversal a sistemas diferentes y no repite contenido teórico.

### Revisión restante

Permanece pendiente una lectura disciplinar completa para valorar:

- densidad por unidad;
- continuidad entre prerrequisitos y aplicaciones;
- suficiencia de referencias cruzadas;
- equilibrio entre intuición, mecanismo, cuantificación e integración;
- carga cognitiva real del estudiante.

## 6. Alineación curricular

Se creó una matriz `resultado → unidades → evidencia → actividad → evaluación → criterio` y una estimación provisional de carga.

Avance:

- [x] porcentajes de evaluación suman 100%;
- [x] diez resultados globales están mapeados a unidades y evidencias;
- [x] criterios de especie, estadio, réplica, causalidad y validez están incorporados;
- [x] carga provisional de 42 horas presenciales y 62 autónomas documentada;
- [x] ficha alineada con las resoluciones de alcance;
- [ ] adaptar horas a créditos y calendario institucional;
- [ ] crear rúbricas analíticas completas;
- [ ] confirmar viabilidad de densidad mediante revisión disciplinar.

## 7. Criterios de salida actualizados

- [x] Arquitectura curricular justificada.
- [x] Catorce unidades redactadas.
- [x] Producción aislada durante el desarrollo.
- [x] Brechas DOHaD, epidermis e inmunidad resueltas e integradas.
- [x] Alcance vertebrado y biomédico delimitado.
- [x] Matriz inicial de alineación y carga creada.
- [x] JSON de reconstrucción válido y ecuaciones LaTeX protegidas.
- [x] Registro bibliográfico único y cobertura canónica completa.
- [x] Duplicados, ambigüedad e incompletitud bibliográfica controlados por CI.
- [x] Auditoría estructural de repetición y progresión realizada.
- [x] Cribado léxico de redundancia realizado.
- [ ] Curar lecturas obligatorias, avanzadas y de consulta.
- [ ] Auditar licencias de materiales visuales previstos.
- [ ] Completar rúbricas y adaptar carga institucional.
- [ ] Obtener revisión disciplinar externa.
- [ ] Incorporar correcciones de revisión.
- [ ] Documentar migración, generación y reversión.

## 8. Veredicto actualizado

El curso es un borrador avanzado con arquitectura, alcance, integridad técnica, trazabilidad bibliográfica y control de redundancia sustancialmente resueltos. La siguiente fase ya no consiste en añadir contenido indiscriminadamente, sino en curación pedagógica y revisión externa.

Aún no debe migrarse a producción. CI demuestra integridad estructural y registral; no certifica suficiencia disciplinar, factibilidad de carga, calidad de rúbricas, licencias ni utilidad clínica.
