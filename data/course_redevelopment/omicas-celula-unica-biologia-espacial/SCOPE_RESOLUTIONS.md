# Resoluciones de alcance

## Propósito central

La asignatura enseña a diseñar, procesar e interpretar estudios de célula única y espaciales como experimentos multimuesta. La meta no es producir un UMAP atractivo, sino construir inferencias biológicas reproducibles y proporcionales a las réplicas, la tecnología y los metadatos disponibles.

## Incluye

- scRNA-seq y snRNA-seq basados en UMI;
- principios de scATAC-seq, CITE-seq y multiome;
- objetos `SingleCellExperiment`, `AnnData` y `SpatialData`;
- control de calidad, RNA ambiente y doublets;
- normalización, representación, clustering y anotación;
- inferencia pseudobulk, estado y abundancia diferencial;
- integración, transferencia de etiquetas y referencias;
- trayectorias y dinámica con límites explícitos;
- transcriptómica espacial spot-based e imaging-based;
- imágenes, segmentación, registro, grafos, nichos y validación ortogonal.

## No incluye como núcleo

- protocolos wet-lab detallados de disociación, citometría o construcción de bibliotecas;
- desarrollo exhaustivo de algoritmos de alineamiento y cuantificación, cubierto por Bioinformática;
- patología diagnóstica autónoma ni toma de decisiones clínicas;
- inferencia causal de efectos terapéuticos sin diseño apropiado;
- certificación de competencias regulatorias o clínicas.

## Relación con asignaturas vecinas

- **Bioinformática:** aporta secuencias, cuantificación, workflows y bases de datos.
- **Bioestadística:** aporta modelos, diseño, multiplicidad, incertidumbre y covariables.
- **Biología Celular y Molecular:** aporta identidad, estados, regulación y mecanismos.
- **Imágenes Biomédicas Avanzadas II:** aporta registro, segmentación, métricas y validación de imagen.
- **Machine Learning Biomédico:** aporta validación, generalización, sesgo y ciclo de vida de modelos.

## Reglas editoriales

- Las células de una misma muestra no son réplicas biológicas independientes.
- Un cluster no equivale automáticamente a un tipo celular.
- UMAP no se interpreta como distancia biológica global ni trayectoria temporal.
- La corrección de batch no debe borrar la condición de interés.
- La proximidad espacial o coexpresión ligando-receptor no demuestra comunicación funcional.
- Toda afirmación traslacional debe indicar la validación ortogonal que todavía falta.
