# Actualización de auditoría curricular — 2026-07-27

## 1. Estado del bloque

La fase posterior a la redacción de las 14 unidades resolvió las decisiones de alcance y las integró en la ficha y en los JSON de unidad correspondientes. Los archivos públicos continúan sin modificaciones.

Artefactos de trazabilidad:

- `SCOPE_RESOLUTIONS.md`;
- `CURRICULUM_ALIGNMENT_MATRIX.md`;
- `data/source_registry/biologia-desarrollo-scope-addendum.json`;
- `course.json`;
- `units/unit-08.json`;
- `units/unit-10.json`;
- `units/unit-13.json`.

## 2. Brechas de alcance

### DOHaD

**Estado de decisión:** resuelto.  
**Estado de integración en `unit-13.json`:** completo.

La Unidad 13 incluye una sección autónoma que distingue periodo crítico y sensible, trayectoria de curso de vida, mediación placentaria, biomarcador, asociación epidemiológica, epigenética e inferencia causal. La redacción evita determinismo, predicción individual injustificada y culpabilización materna.

La integración también alcanza objetivos, glosario, ejemplo trabajado, actividad guiada, errores frecuentes, autoevaluación, conexión biomédica y bibliografía.

### Epidermis y anexos

**Estado de decisión:** resuelto.  
**Estado de integración en `unit-08.json`:** completo.

La Unidad 8 conserva `epidermis` dentro del alcance y añade ectodermo superficial, peridermo, estratificación, membrana basal, barrera e interacción epitelio–mesénquima en folículos y glándulas. Se distingue marcador epidérmico de arquitectura y función de barrera.

La integración también alcanza objetivos, glosario, ejemplo trabajado, actividad guiada, errores frecuentes, autoevaluación, conexión biomédica y bibliografía.

### Desarrollo inmunitario

**Estado de decisión:** resuelto y delimitado.  
**Estado de integración en `unit-10.json`:** completo.

La Unidad 10 incorpora un puente sobre primordio epitelial tímico, colonización linfoide, organización estromal y cortico-medular, y selección de timocitos. Activación inmunitaria, efectores, memoria, vacunología e inmunopatología permanecen formalmente fuera y pertenecen a Inmunología.

La integración también alcanza objetivos, glosario, ejemplo trabajado, actividad guiada, errores frecuentes, autoevaluación, conexión biomédica y bibliografía.

### Desarrollo vegetal e invertebrados

**Estado de decisión:** resuelto.  
**Estado de integración en `course.json`:** completo.

La ficha define el curso como biología del desarrollo animal con énfasis vertebrado, humano y biomédico. Los invertebrados se utilizan como sistemas comparativos; desarrollo vegetal no forma parte del alcance.

## 3. Bibliografía

El addendum registra las fuentes específicas utilizadas en las tres integraciones. Los estados `verified_directly` y `verified_metadata` se mantienen separados y cada fuente incluye función curricular y limitaciones.

Avance:

- [x] nuevas fuentes registradas con función curricular y limitaciones;
- [x] guía WHO 2025 de curso de vida consultada directamente;
- [x] atlas del timo humano del Human Cell Atlas consultado directamente;
- [x] fuentes incorporadas en las unidades correspondientes;
- [ ] fusionar el addendum con el registro central;
- [ ] deduplicar todas las fuentes de las 14 unidades;
- [ ] normalizar autores, DOI, PMID, años y tipos;
- [ ] seleccionar lecturas obligatorias y complementarias;
- [ ] auditar licencias de figuras y materiales.

## 4. Alineación curricular

Se creó una matriz `resultado → unidades → evidencia → actividad → evaluación → criterio` y una estimación provisional de carga.

Avance:

- [x] porcentajes de evaluación suman 100%;
- [x] diez resultados globales están mapeados a unidades y evidencias;
- [x] criterios transversales de especie, estadio, réplica, causalidad y validez están incorporados;
- [x] carga provisional documentada con supuestos;
- [x] ficha del curso alineada con las resoluciones de alcance;
- [ ] adaptar horas a créditos y calendario institucional;
- [ ] crear rúbricas analíticas completas;
- [ ] confirmar viabilidad de densidad mediante revisión disciplinar.

## 5. Criterios de salida actualizados

- [x] Arquitectura curricular justificada.
- [x] Catorce unidades redactadas.
- [x] Producción aislada durante el desarrollo.
- [x] Validaciones técnicas superadas en el bloque previo.
- [x] Brechas DOHaD, epidermis e inmunidad resueltas a nivel de decisión.
- [x] Alcance vertebrado y biomédico delimitado formalmente.
- [x] Matriz inicial de alineación y carga creada.
- [x] Resoluciones integradas en `unit-08.json`, `unit-10.json`, `unit-13.json` y `course.json`.
- [ ] Consolidar y verificar bibliografía completa.
- [ ] Completar auditoría de repetición y progresión.
- [ ] Completar rúbricas y adaptar carga institucional.
- [ ] Obtener revisión disciplinar externa.
- [ ] Incorporar correcciones de revisión.
- [ ] Documentar migración, generación y reversión.

## 6. Veredicto actualizado

El curso ha avanzado a una arquitectura completa con **brechas de alcance resueltas e integradas**. La ficha curricular y las unidades afectadas ahora representan el mismo alcance.

Aún no debe migrarse a producción. La siguiente fase correcta es validar técnicamente estos cambios, consolidar bibliografía y comenzar la auditoría transversal de repetición y progresión. La revisión disciplinar externa continúa siendo un requisito independiente de CI.