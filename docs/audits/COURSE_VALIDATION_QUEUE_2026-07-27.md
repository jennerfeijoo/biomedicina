# Cola de validación de asignaturas

**Fecha:** 2026-07-27  
**Estado:** priorización inicial basada en riesgo, dependencia curricular y madurez observable

## 1. Principios de priorización

La auditoría no seguirá el orden alfabético ni el número de archivos existentes. La prioridad depende de:

1. impacto sobre cursos posteriores;
2. relevancia para biomedicina computacional;
3. discrepancia entre estado público y contenido real;
4. riesgo científico, clínico, cuantitativo o regulatorio;
5. cantidad de unidades ya desarrolladas que podrían contener plantillas o errores sistemáticos;
6. existencia de una reconstrucción lista para migración;
7. necesidad de prerrequisitos coherentes.

Cada asignatura pasará por:

- delimitación disciplinar;
- revisión externa de arquitectura;
- decisión de unidades;
- registro canónico de fuentes;
- auditoría de especificidad;
- alineación de resultados, actividades y evaluación;
- revisión disciplinar;
- corrección;
- validación técnica;
- migración o sincronización pública.

## 2. Lote 0 — Bloqueadores inmediatos

### 0.1 Biología del Desarrollo

**Motivo:** existe una reconstrucción de 14 unidades fusionada en `main`, pero la web mantiene seis unidades.

**Acciones:**

- [ ] integrar prácticas y evaluación en el contrato canónico del curso;
- [ ] completar revisión disciplinar externa;
- [ ] preparar plan de migración y reversión;
- [ ] regenerar catálogo, JSON públicos y 14 páginas;
- [ ] comprobar navegación, referencias y paridad semántica.

### 0.2 Fisiología Humana I

**Motivo:** estado `generated` con solo dos de seis unidades desarrolladas. Es prerrequisito para Fisiología Humana II, Fisiopatología y contenidos clínicos.

**Acciones:**

- [ ] corregir estado editorial;
- [ ] revisar límites con Biología II, Anatomía, Biofísica y Fisiología II;
- [ ] decidir arquitectura antes de completar unidades;
- [ ] reconstruir cuatro unidades faltantes.

### 0.3 Bioinformática

**Motivo:** una de seis unidades desarrollada; asignatura central para Citonauta y para cursos ómicos, transcriptómicos y de IA biomédica.

**Acciones:**

- [ ] definir alcance frente a algoritmos, bases de datos, genómica y biología computacional;
- [ ] construir matriz de cobertura y fuentes actuales;
- [ ] decidir balance entre fundamentos, secuencias, alineamiento, anotación, ómicas y reproducibilidad;
- [ ] completar cinco unidades pendientes.

## 3. Lote 1 — Fundamentos que condicionan el resto

### 1.1 Biología I — auditoría iniciada

**Estado:** no validada; cambios requeridos.

Bloqueantes:

- expansión con Unidad 7 inexistente;
- solapamiento con Biología II;
- texto de plantilla repetido;
- ejemplo casi duplicado con Química II.

### 1.2 Biología II

Revisar después de fijar la frontera de Biología I. Debe concentrar fisiología comparada, organismos, poblaciones, ecología y One Health sin duplicar Fisiología Humana ni Ecología especializada.

### 1.3 Química I y Química II

Revisar alcance, progresión, cálculo químico, equilibrio, termodinámica y frontera con Bioquímica. Corregir el ejercicio casi duplicado con Biología I.

### 1.4 Matemáticas y estadística

Orden sugerido:

1. Álgebra;
2. Cálculo;
3. Probabilidad y Estadística;
4. Bioestadística;
5. Ecuaciones Diferenciales;
6. Métodos Numéricos;
7. Ampliación de Cálculo.

Validar que cada curso aporte prerrequisitos reales para modelado, señales, ómicas e IA biomédica y no repita ejercicios genéricos sin contexto.

### 1.5 Programación y datos

Orden sugerido:

1. Fundamentos de Programación;
2. Algoritmos y Estructuras de Datos;
3. Bases de Datos;
4. Arquitectura de Computadores.

Revisar reproducibilidad, pruebas, Git, complejidad, SQL, modelos de datos y límites con cursos de software científico.

## 4. Lote 2 — Núcleo biomédico y molecular

Orden propuesto:

1. Biología Celular y Tisular;
2. Bioquímica;
3. Biología Molecular;
4. Genética;
5. Fisiología Humana II;
6. Fisiopatología Humana;
7. Biofísica;
8. Biología Molecular y Celular Aplicada;
9. Biología Sintética.

### Criterios particulares

- **Biología Celular y Tisular:** separar organelos, tejidos, señalización y métodos; evitar duplicar Biología I.
- **Bioquímica:** distinguir termodinámica, cinética, metabolismo y regulación; delimitarse frente a Química II.
- **Biología Molecular:** cubrir información, regulación, métodos y evidencia sin convertirse en lista de técnicas.
- **Genética:** distinguir herencia, variación, poblaciones, genómica y utilidad clínica.
- **Fisiología Humana II:** revisar integración por sistemas, homeostasis y cuantificación.
- **Fisiopatología:** separar mecanismo de enfermedad, biomarcadores y decisión clínica.
- **Biofísica:** revisar escalas, modelos, unidades y validez experimental.
- **Biología Sintética:** incluir diseño, caracterización, biosafety, biosecurity y límites traslacionales.

## 5. Lote 3 — Computación biomédica, ómicas e IA

Después de Bioinformática y fundamentos cuantitativos:

- genómica;
- transcriptómica;
- proteómica;
- metabolómica;
- biología de sistemas;
- machine learning biomédico;
- IA clínica;
- análisis de imágenes;
- procesamiento de señales;
- modelado y simulación;
- computational drug discovery.

Para IA clínica se exigirá, cuando corresponda:

- discriminación y calibración;
- sensibilidad y especificidad;
- umbrales;
- validación externa;
- subgrupos y sesgo;
- representatividad;
- utilidad clínica;
- seguridad y flujo clínico;
- drift y monitorización.

## 6. Lote 4 — Ingeniería biomédica, dispositivos y regulación

Priorizar cursos que puedan inducir afirmaciones de seguridad, desempeño o cumplimiento:

- instrumentación;
- biomateriales e implantes;
- dispositivos médicos;
- imágenes biomédicas;
- planificación quirúrgica;
- ingeniería de tejidos;
- salud digital;
- calidad y regulación.

Debe diferenciarse validación técnica, preclínica, clínica, regulatoria y postmercado.

## 7. Lote 5 — Gestión, ética y comunicación

Auditar después de estabilizar los contenidos científicos que utilizan como casos:

- ética biomédica;
- comunicación científica;
- políticas públicas;
- inglés profesional;
- gestión de proyectos e innovación.

Las unidades deben evitar generalidades de productividad o liderazgo y mantener conexión directa con investigación, industria, clínica, datos y regulación biomédica.

## 8. Lote 6 — Asignaturas de catálogo o placeholder

Las 55 asignaturas sin desarrollo real no deben rellenarse automáticamente. Para cada una se realizará primero:

1. análisis independiente;
2. revisión de programas y estándares;
3. matriz de cobertura;
4. decisión justificada del número de unidades;
5. aprobación de arquitectura;
6. producción por bloques revisables.

## 9. Condición para declarar una asignatura validada

Una asignatura no se validará hasta que:

- el alcance y las exclusiones estén documentados;
- el número de unidades esté justificado;
- las fuentes sean trazables y suficientes;
- las unidades sean específicas y no plantilladas;
- prácticas y evaluación midan resultados reales;
- exista revisión disciplinar documentada;
- las correcciones estén incorporadas;
- los controles técnicos pasen;
- la publicación coincida con el paquete aprobado.

## 10. Próximo trabajo aprobado

1. Reescribir Biología I según su decisión de seis unidades.
2. Auditar la frontera y arquitectura de Biología II.
3. Resolver el estado de publicación de Biología del Desarrollo.
4. Iniciar en paralelo las decisiones curriculares de Fisiología Humana I y Bioinformática.

La cola podrá cambiar si una auditoría encuentra un error científico, clínico o técnico bloqueante.