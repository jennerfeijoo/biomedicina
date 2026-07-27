# Auditoría de asignaturas desarrolladas — 2026-07-27

## Alcance

Esta auditoría distingue tres dimensiones que no deben confundirse:

1. **desarrollo lectivo:** existencia de unidades avanzadas o autorales;
2. **publicación técnica:** sincronización entre fuente, JSON públicos y páginas HTML;
3. **madurez académica:** revisión disciplinar documentada y estado editorial `complete`.

Una página de catálogo o una unidad generada mediante fallback no cuenta como desarrollo académico completo.

## Resumen del catálogo

- Asignaturas catalogadas: **84**.
- Asignaturas con algún contenido desarrollado: **29**.
- Asignaturas completamente desarrolladas a nivel lectivo: **27**.
- Asignaturas parcialmente desarrolladas: **2**.
- Unidades desarrolladas: **180**.
- Unidades avanzadas: **179**.
- Unidades autorales: **1**.
- Unidades fallback dentro de asignaturas parcialmente desarrolladas: **9**.
- Páginas ausentes dentro de asignaturas con contenido desarrollado: **0**.

## Asignaturas completamente desarrolladas

1. Biología Celular.
2. Biología del Desarrollo.
3. Biología I.
4. Biología II.
5. Biología Molecular.
6. Biología Molecular y Celular Aplicada.
7. Biología Sintética.
8. Bioquímica.
9. Fisiología Humana II.
10. Fisiopatología Humana.
11. Genética.
12. Álgebra.
13. Algoritmos y Estructuras de Datos.
14. Ampliación de Cálculo.
15. Arquitectura de Computadores.
16. Bases de Datos.
17. Bioestadística.
18. Biofísica.
19. Cálculo.
20. Ecuaciones Diferenciales.
21. Física I.
22. Física II.
23. Fundamentos de Programación.
24. Métodos Numéricos.
25. Probabilidad y Estadística.
26. Química I.
27. Química II.

## Asignaturas parcialmente desarrolladas

### Fisiología Humana I

- Unidades esperadas: 6.
- Unidades avanzadas: 2.
- Unidades fallback: 4.
- Desarrollo lectivo: **33,33 %**.

La asignatura no debe declararse terminada hasta sustituir las cuatro unidades fallback por contenido avanzado o autoral validado.

### Bioinformática

- Unidades esperadas: 6.
- Unidades autorales: 1.
- Unidades fallback: 5.
- Desarrollo lectivo: **16,67 %**.

La asignatura no debe declararse terminada hasta desarrollar las cinco unidades restantes y verificar progresión, bibliografía y prácticas reproducibles.

## Paquetes reconstruidos

Actualmente existe un paquete formal bajo `data/course_redevelopment`:

### Biología del Desarrollo

- Fuente válida: sí.
- Unidades: 14.
- Promoción JSON sincronizada: sí.
- Páginas HTML sincronizadas: sí.
- Publicación técnica: completa.
- Artefactos académicos requeridos: presentes.
- Estado editorial: `review`.
- Revisión disciplinar completa: no.

La asignatura está publicada y completamente desarrollada a nivel lectivo, pero continúa correctamente en `review`. Los controles técnicos no constituyen revisión disciplinar externa ni permiten promocionarla automáticamente a `complete`.

## Hallazgos de infraestructura

Durante la auditoría se identificaron y corrigieron dos restricciones incompatibles con el protocolo académico:

- el publicador estaba especializado exclusivamente en Biología del Desarrollo;
- el validador curricular imponía un máximo arbitrario de diez unidades, pese a que el protocolo exige decidir la extensión según la disciplina.

El nuevo flujo descubre paquetes, calcula área y número de unidades desde la fuente, publica una asignatura o todas, regenera los índices afectados y comprueba la sincronización completa.

## Prioridad curricular siguiente

1. Completar Fisiología Humana I.
2. Reconstruir Bioinformática con arquitectura, fuentes y unidades avanzadas.
3. Incorporar progresivamente las 27 asignaturas desarrolladas al formato formal de `course_redevelopment`, sin asumir que su completitud lectiva equivale a revisión académica documentada.
