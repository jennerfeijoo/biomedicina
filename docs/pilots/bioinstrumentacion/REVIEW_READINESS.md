# Preparación para revisión — Ruta piloto de Bioinstrumentación

## Estado de este bloque

**Fase:** base curricular y editorial.  
**Estado del curso en el catálogo:** `pending`.  
**Estado del paquete piloto:** `foundation_review`.  
**Unidades desarrolladas en este bloque:** ninguna.  
**Promoción autorizada:** ninguna.

Este bloque corrige la interpretación editorial del contenido de respaldo y define las condiciones necesarias antes de redactar las unidades.

## Artefactos incluidos

- contrato transversal de excelencia académica;
- arquitectura de diez unidades;
- alcance, exclusiones y conocimientos de entrada;
- decisión documentada del número de unidades;
- registro inicial de fuentes y estado de verificación;
- matriz resultado–evidencia–error–feedback–recuperación;
- paquete incremental de planificación;
- validador automático de la base piloto;
- corrección del estado público de cursos y unidades pendientes.

## Decisiones curriculares

### Estructura seleccionada

Se seleccionan diez unidades porque permiten separar:

1. definición de la medición;
2. transducción y dinámica;
3. biopotenciales;
4. acondicionamiento analógico;
5. adquisición digital;
6. familias de sensores;
7. seguridad;
8. metrología de desempeño;
9. verificación, validación y riesgo;
10. integración.

La estructura histórica de seis unidades se rechaza como base de autoría porque comprime dominios heterogéneos y favorece contenido genérico.

### Fronteras

- procesamiento digital profundo: Sistemas y Señales / Señales Biomédicas;
- reconocimiento biológico y química de superficies: Biosensores;
- ciclo completo de producto: Desarrollo de Dispositivos Médicos;
- mantenimiento y gestión hospitalaria: Ingeniería Clínica y Gestión;
- decisiones diagnósticas: fuera de alcance;
- prácticas con personas, muestras o equipos clínicos: solo bajo supervisión institucional y fuera del modo autónomo de la plataforma.

## Estado de las fuentes

### Consultadas directamente

- entradas y estructura del VIM en BIPM;
- descripciones curriculares oficiales de UC San Diego y Georgia Tech;
- descripciones y materiales índice de MIT OpenCourseWare;
- recurso institucional de NIBIB sobre sensores.

### Solo metadata

- IEC 60601-1 edición consolidada 3.2. La página oficial permite identificar edición, alcance general y ciclo de estabilidad, pero no autoriza reproducir límites, ensayos o requisitos.

### Brechas antes de autoría completa

- modelos de respuesta dinámica de transductores;
- interfaz electrodo-tejido y electrofisiología de medición;
- seguridad y compatibilidad electromagnética con acceso normativo;
- incertidumbre aplicada a cadenas fisiológicas;
- casos reproducibles y datasets abiertos adecuados.

## Revisiones humanas requeridas

| Revisión | Alcance | Bloquea |
|---|---|---|
| Bioinstrumentación | transducción, electrónica, sensores, cadena completa | autoría final de todas las unidades |
| Electrofisiología | biopotenciales, electrodos, artefactos | unidad 3 |
| Señales y adquisición | ruido, filtros, muestreo, ADC | unidades 4 y 5 |
| Metrología | mensurando, calibración, incertidumbre | unidades 1 y 8 |
| Seguridad de equipo electromédico | aislamiento, riesgos, normas | unidad 7 y afirmaciones normativas |
| Diseño y regulación | verificación, validación, riesgo | unidad 9 |
| Ciencias del aprendizaje | feedback, misconceptions y recuperación | contrato de todas las unidades |
| Accesibilidad | navegación, notación, visuales y feedback | publicación piloto autosuficiente |
| Licencias | figuras, datos y recursos | publicación de activos externos |

## Gates antes de comenzar la autoría

- [x] alcance y exclusiones definidos;
- [x] conocimientos de entrada observables;
- [x] diez unidades justificadas;
- [x] matriz de alineación creada;
- [x] fuentes iniciales registradas y clasificadas;
- [x] el curso permanece `pending`;
- [x] contrato de feedback definido;
- [ ] brechas bibliográficas centrales resueltas;
- [ ] revisión de arquitectura por especialista;
- [ ] diseño del esquema de feedback implementable en la plataforma;
- [ ] decisión sobre datasets y simulaciones del proyecto.

## Gates antes de cambiar a developed/review

- diez unidades específicas y sin fallback;
- todas las afirmaciones centrales con fuente directamente verificada;
- ejemplos y prácticas reproducibles;
- feedback específico por misconception;
- auditoría de redundancia intraunidad y entre unidades;
- enlaces y páginas sincronizados;
- validación de accesibilidad en páginas representativas;
- revisión interna de continuidad;
- ninguna cifra normativa no verificada;
- el proyecto integrador se completa sin conexión a personas o equipos clínicos.

## Gates antes de complete

- revisión disciplinar documentada;
- revisión de seguridad y metrología documentada;
- hallazgos bloqueantes resueltos;
- prueba de autonomía con los perfiles objetivo;
- mantenimiento, versión y fecha de próxima revisión;
- decisión editorial explícita.

## Riesgos abiertos

1. Los prerrequisitos Electrónica y varios cursos aplicados permanecen `pending`; la ruta completa todavía no es autosuficiente.
2. La norma de seguridad central no ha sido consultada en texto completo.
3. La plataforma actual revela respuestas, pero aún no implementa feedback diagnóstico.
4. No se han ejecutado pruebas de usuario.
5. La arquitectura necesita revisión de una persona con experiencia real en bioinstrumentación.

## Decisión editorial

El paquete puede entrar en revisión de arquitectura y preparación bibliográfica. No está autorizado para cambiar Bioinstrumentación a `developed`, `review` ni `complete`. La autoría comenzará solo después de resolver los gates señalados para esa fase.