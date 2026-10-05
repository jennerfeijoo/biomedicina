# Amplitud disciplinar de la portada y las rutas

Revisión: 5 de octubre de 2026.

La portada anterior presentaba biología humana, biomedicina computacional y el catálogo como tres opciones del mismo nivel. El título y el lema reforzaban esa especialización, aunque el proyecto abarca biomedicina e ingeniería biomédica. Las nueve rutas existentes omitían 14 asignaturas.

Se sustituyen esas entradas por ocho familias de navegación. Sus 18 rutas reúnen las 94 asignaturas actuales; cada asignatura puede participar en varias rutas. El catálogo completo sigue siendo una herramienta de navegación, no una disciplina.

| Familia | Rutas |
| --- | --- |
| Fundamentos científicos | Fundamentos matemáticos, físicos y químicos; sistemas biológicos y modelado |
| Ciencias biológicas y médicas | Biología, anatomía, fisiología y enfermedad; inmunología, microbiología y diagnóstico |
| Terapias y bioingeniería | Farmacología y evaluación de terapias; biotecnología celular, molecular y sintética; biomateriales, tejidos y medicina regenerativa |
| Instrumentación y dispositivos | Biosensores y bioinstrumentación; dispositivos médicos e ingeniería clínica |
| Señales, imágenes y neuroingeniería | Señales, neuroingeniería e interfaces; imágenes y biofotónica |
| Movimiento, rehabilitación y asistencia | Biomecánica; rehabilitación, robótica y tecnologías asistivas |
| Datos y computación biomédica | Bioinformática y ómicas; IA clínica y datos de salud |
| Salud, investigación y sociedad | Epidemiología, salud pública e investigación clínica; tecnología sanitaria e innovación; método científico, ética y comunicación |

## Contraste curricular

Se consultaron fuentes institucionales de cuatro regiones. La agrupación es una síntesis editorial propia, no una reproducción de un plan ni una equivalencia académica.

- [Johns Hopkins University — Undergraduate Focus Areas & Courses](https://www.bme.jhu.edu/academics/undergraduate/undergraduate-focus-areas-courses/): relaciones entre disciplinas de ingeniería y ciencias biomédicas.
- [National University of Singapore — Specialisations](https://cde.nus.edu.sg/bme/undergraduate/degree-programme/beng-bme/specializations/): materiales, tejidos, robótica y tecnología para salud comunitaria.
- [Universitat Politècnica de Catalunya — Grado en Ingeniería Biomédica](https://www.upc.edu/es/grados/ingenieria-biomedica-barcelona-eebe-1): fundamentos y aplicaciones tecnológicas; plan visible por cuatrimestres.
- [University of Melbourne — Biomedicine Majors](https://biomedicalsciences.unimelb.edu.au/study/current-student-information/plan-your-bachelor-of-biomedicine/majors): amplitud de ciencias biomédicas, farmacología y salud poblacional.

Las páginas de Imperial, UPM y el folleto de Tec de Monterrey no se recuperaron íntegramente durante esta consulta; no se usan como fundamento del mapeo publicado.

## Alcance y mantenimiento

Estas familias no agotan todos los subcampos de la biomedicina ni convierten las rutas en especializaciones completas. La ruta de robótica declara que ofrece fundamentos relacionados y que no existe todavía una asignatura específica de robótica médica. No se crean asignaturas vacías ni se eleva su estado editorial al ampliar la navegación.

Los identificadores de las nueve rutas previas se conservan para mantener enlaces. `data/tracks.json` es la fuente compartida para portada y catálogo. La generación incorpora las tarjetas y sus enlaces en HTML, accesibles sin JavaScript; el buscador conserva sus filtros dinámicos. Los prerrequisitos siguen en el mapa curricular.

Las pruebas verifican que toda asignatura esté representada, que cada ruta tenga familia y enlace público, que los destinos internos existan y que la generación sea reproducible. La validación completa comprueba también catálogo, enlaces y sintaxis.
