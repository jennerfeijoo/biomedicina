# Desarrollo de Dispositivos Médicos: revisión documental

Integración: 7 de octubre de 2026. Consulta documental: 5 de octubre de 2026.

Se revisan las 24 afirmaciones ancla (cuatro por unidad), sus localizadores y su correspondencia con las seis unidades. El registro pasa de 48 errores de contrato a cero; esto no equivale a una revisión exhaustiva del curso ni a validación científica humana. Los estados provisionales y los campos de validación humana se conservan.

## Cambios y límites

- U1: separar la organización docente de observación, interpretación, necesidad y solución del proceso Biodesign. Distinguir actores y triangulación de las inferencias añadidas por el curso.
- U2: respaldar entradas de diseño y trazabilidad bidireccional; reconocer que extrapolar una guía de arquitectura de software a arquitectura general tiene apoyo parcial.
- U3: usar las definiciones y principios públicos de IMDRF para peligros, riesgo, jerarquía de controles y riesgo residual global. No atribuir lectura de cláusulas completas de ISO 14971 a partir de su ficha pública.
- U4: identificar configuración y especificaciones de verificación; conservar controles de seguridad y versiones en prototipos exploratorios. La conservación de datos crudos y código es una exigencia docente de reproducibilidad adicional al alcance explícito de la guía FDA.
- U5: separar verificación y validación, factores humanos, ensayos no clínicos de banco e investigación clínica. La afirmación sobre banco no pretende describir toda la evidencia preclínica.
- U6: limitar la afirmación sobre clasificación a Estados Unidos. Precisar transferencia de diseño y control de cambios; distinguir armonización IMDRF de legislación aplicable.

Apoyo parcial: DDM-U01-C001, DDM-U01-C002, DDM-U01-C004, DDM-U02-C003 y DDM-U04-C004. Las otras 19 afirmaciones tienen apoyo directo dentro de los límites indicados. Se conservan los niveles de riesgo.

## Documentos consultados

Los localizadores exactos están en `data/courses/desarrollo-dispositivos-medicos/claims.json` y las referencias en `sources.json`.

- Stanford Biodesign: proceso Identify/Invent y *Choosing a Need*, páginas 3–6.
- FDA: guía de factores humanos, secciones 5, 6.1 y 8; arquitectura de funciones de software; transcripción QMSR de diseño y desarrollo, diapositivas 15–16, 27 y 29–32.
- FDA: *Recommended Content and Format of Non-Clinical Bench Performance Testing Information*, secciones II.A.6, II.B.2–3 y II.C; *Design Considerations for Pivotal Clinical Investigations*, secciones 6.3, 7.1, 9.3 y 10.
- FDA: *Overview of Device Regulation* y guía de cambios que pueden requerir un nuevo 510(k). Esta última se publicó antes de QMSR; no se usa para presentar antiguas referencias a 21 CFR 820.30 como legislación actual.
- IMDRF N47, edición 2 (2024), secciones 3.35 y 5.1.2–5.1.3.
- NASA: gestión de requisitos 6.2, verificación 5.3 y matriz de verificación del apéndice D.
- JCGM 106:2012, secciones 3.2.4 y 5.1.

No se declara una nueva revisión del resto de referencias históricas del curso. El texto consolidado EUR-Lex no pudo consultarse íntegramente y no se utilizó como apoyo directo de estas afirmaciones. Esta revisión tampoco certifica cumplimiento regulatorio, seguridad de dispositivos ni aptitud de uso clínico.

## Verificación

Pruebas de correspondencia entre afirmaciones, fuentes y contenido; regresiones de alcance jurisdiccional y reproducibilidad; regeneración de las seis páginas públicas y ejecución del control completo del repositorio. La auditoría global queda en 20 registros, 894 afirmaciones, 1677 errores pendientes y cinco registros sin errores de contrato.

Resultado: 98 controles sin fallos, 1905 pruebas unittest y 2054 pruebas pytest (274 subpruebas), y dos regeneraciones sin cambios.
