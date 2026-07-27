# Actualización de auditoría curricular — 2026-07-27

## 1. Estado del bloque

La fase posterior a la redacción de las 14 unidades resolvió las decisiones de alcance que estaban abiertas y creó los artefactos necesarios para la integración editorial. Los archivos públicos continúan sin modificaciones.

Artefactos añadidos:

- `SCOPE_RESOLUTIONS.md`;
- `CURRICULUM_ALIGNMENT_MATRIX.md`;
- `data/source_registry/biologia-desarrollo-scope-addendum.json`.

## 2. Brechas de alcance

### DOHaD

**Estado de decisión:** resuelto.  
**Estado de integración en `unit-13.json`:** pendiente.

Se aprobó una sección autónoma que distingue periodo sensible, trayectoria de curso de vida, mediación placentaria, asociación epidemiológica, epigenética y causalidad. La redacción evita determinismo y culpabilización materna.

### Epidermis y anexos

**Estado de decisión:** resuelto.  
**Estado de integración en `unit-08.json`:** pendiente.

Se mantiene `epidermis` dentro del alcance de la Unidad 8 y se aprobó una subsección compacta sobre ectodermo superficial, peridermo, estratificación, barrera e interacción epitelio–mesénquima en folículos y glándulas.

### Desarrollo inmunitario

**Estado de decisión:** resuelto y delimitado.  
**Estado de integración en `unit-10.json`:** pendiente.

Se incorporará un puente sobre organogénesis tímica, colonización linfoide, organización cortico-medular y selección de timocitos. Activación inmunitaria, efectores, memoria, vacunología e inmunopatología quedan formalmente fuera y pertenecen a Inmunología.

### Desarrollo vegetal e invertebrados

**Estado de decisión:** resuelto.  
**Estado de integración en `course.json`:** pendiente.

El curso queda definido como biología del desarrollo animal con énfasis vertebrado, humano y biomédico. Los invertebrados se utilizan como sistemas comparativos; desarrollo vegetal no forma parte del alcance.

## 3. Bibliografía

Se creó un addendum con fuentes específicas para las tres brechas. Los estados `verified_directly` y `verified_metadata` se mantienen separados.

Avance:

- [x] nuevas fuentes registradas con función curricular y limitaciones;
- [x] guía WHO 2025 de curso de vida consultada directamente;
- [x] atlas del timo humano del Human Cell Atlas consultado directamente;
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
- [ ] Integrar las resoluciones en `unit-08.json`, `unit-10.json`, `unit-13.json` y `course.json`.
- [ ] Consolidar y verificar bibliografía completa.
- [ ] Completar auditoría de repetición y progresión.
- [ ] Completar rúbricas y adaptar carga institucional.
- [ ] Obtener revisión disciplinar externa.
- [ ] Incorporar correcciones de revisión.
- [ ] Documentar migración, generación y reversión.

## 6. Veredicto actualizado

El curso ha avanzado de una arquitectura completa con brechas abiertas a una arquitectura completa con **decisiones de alcance resueltas y textos preparados para integración**. Aún no debe migrarse a producción porque los JSON principales no incorporan esos cambios y la bibliografía global no está consolidada.

El siguiente bloque correcto es integrar las resoluciones en las unidades y en `course.json`, ejecutar validación, y después comenzar la auditoría de repetición y progresión.