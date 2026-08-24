from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBJECT = "ingenieria-datos-biomedicos"
SOURCE = ROOT / "data" / "course_redevelopment" / SUBJECT / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / SUBJECT / "unit-01.json"
TEST = ROOT / "tests" / "test_ingenieria_datos_biomedicos_unit_01_curated.py"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"

unit = json.loads(SOURCE.read_text(encoding="utf-8"))

unit.update({
    "purpose": "Diseñar una arquitectura de entrada reproducible para datos biomédicos heterogéneos distinguiendo fuente, objeto de datos, granularidad, identidad, tiempo, semántica y procedencia en registros clínicos, dispositivos, imagen y ómicas, sin confundir un formato de intercambio con un modelo analítico ni adelantar las transformaciones, almacenamiento, control de calidad, operación o privacidad de las unidades posteriores.",
    "learning_objectives": [
        "Distinguir fuente de datos, sistema fuente, objeto o evento observado y representación digital en registros clínicos, dispositivos, imagen médica y datos ómicos.",
        "Caracterizar cada fuente mediante unidad de observación, identificadores, tiempos, unidades, codificación, versión, contexto de adquisición y procedencia antes de diseñar una integración.",
        "Explicar el papel y los límites de FHIR, DICOM/DICOMweb, ISO/IEEE 11073 y formatos genómicos como FASTQ, SAM/BAM y VCF sin tratarlos como modelos equivalentes.",
        "Diferenciar una representación de intercambio o archivo nativo de un modelo analítico común, y justificar cuándo conservar la representación original junto con una capa de acceso o normalización.",
        "Diseñar para un caso completamente sintético un mapa fuente → interfaz → zona de aterrizaje lógica → consumidor, con claves de enlace, relojes y metadatos explícitos y sin fusionar identidades por intuición.",
        "Auditar los límites de una arquitectura multimodal y documentar qué decisiones se delegan deliberadamente a U2 transformación, U3 almacenamiento, U4 calidad, U5 orquestación y U6 privacidad y productos de datos."
    ],
    "theory_sections": [
        {
            "heading": "1. Fuente biomédica, granularidad y representación",
            "paragraphs": [
                "Una fuente biomédica no es simplemente un archivo. Es un sistema o proceso que produce observaciones con una granularidad, una semántica y un contexto de adquisición determinados. Una historia clínica puede producir encuentros, órdenes, resultados y documentos; un dispositivo puede producir muestras o eventos temporales; un sistema de imagen produce objetos DICOM organizados en estudios y series; y un ensayo de secuenciación produce lecturas, alineamientos o llamadas de variantes. Antes de integrar cualquiera de ellos debe declararse qué entidad es observada y qué representa exactamente cada registro.",
                "La unidad de observación cambia entre dominios y no debe inferirse por el nombre de una columna. Un recurso clínico puede describir una observación asociada a una persona y a un encuentro; una muestra de ECG pertenece a un canal y a un instante; un objeto de imagen tiene identidad propia dentro de una jerarquía; una lectura FASTQ pertenece a una preparación y ejecución de secuenciación. Tratar todos esos registros como filas equivalentes crea pseudorreplicación, enlaces falsos y pérdidas de significado antes incluso de ejecutar una transformación.",
                "También debe separarse el fenómeno biomédico de su representación digital. Una presión arterial no es un recurso FHIR, una imagen anatómica no es un archivo PNG y una variante biológica no es una línea VCF. FHIR, DICOM y VCF son representaciones estandarizadas que codifican parte del significado necesario para intercambio o análisis. Esta distinción permite cambiar de herramienta sin afirmar que el formato agota el fenómeno medido.",
                "Una ficha mínima de fuente debe registrar sistema productor, responsable técnico, tipo de objeto, unidad de observación, identificadores, tiempo relevante, unidades o sistema de códigos, versión de formato o estándar, contexto de adquisición y procedencia. Esa ficha es el contrato conceptual de U1: todavía no transforma los datos, pero establece qué información debe sobrevivir cuando U2 diseñe la ingesta y la transformación.",
                "La arquitectura comienza, por tanto, con un inventario de fuentes y no con una base de datos elegida de antemano. La pregunta correcta es qué objetos llegan, qué significado tienen, con qué frecuencia cambian, qué claves son locales, qué relojes existen y qué metadatos son indispensables. Solo después se decide cómo exponerlos a las capas posteriores del curso."
            ],
            "key_points": [
                "Definir sistema fuente, objeto y unidad de observación antes de integrar.",
                "Separar fenómeno biomédico de representación digital.",
                "Registrar identidad, tiempo, semántica, versión y procedencia en la frontera de entrada.",
                "Diseñar desde las fuentes y el uso, no desde una tecnología de almacenamiento elegida prematuramente."
            ]
        },
        {
            "heading": "2. Cuatro familias de fuentes: clínica, dispositivos, imagen y ómicas",
            "paragraphs": [
                "En datos clínicos interoperables, HL7 FHIR organiza el intercambio alrededor de recursos enlazables como Patient, Encounter, Observation, DiagnosticReport o MedicationRequest. FHIR es un estándar de intercambio y representación, no una copia universal del esquema interno de cada historia clínica. Por ello una arquitectura debe conservar la procedencia del recurso, su versión y sus referencias, y no asumir que un identificador local de paciente es global o que dos sistemas usan las mismas reglas de codificación.",
                "Los dispositivos y sensores añaden una dimensión temporal y de adquisición. La familia ISO/IEEE 11073 modela contenido y comunicación de observaciones de dispositivos de salud; por ejemplo, existen especializaciones para ECG y otros dispositivos personales. En una fuente de alta frecuencia deben declararse dispositivo, canal, frecuencia o patrón de muestreo, reloj, unidades y eventos de pérdida o desconexión. Un vector de valores sin esos metadatos no permite reconstruir de forma fiable cuándo ni cómo se obtuvo la señal.",
                "La imagen médica utiliza DICOM para representar objetos de información, metadatos, identificadores únicos y servicios de comunicación. La edición vigente consultada, DICOM 2026c, mantiene la jerarquía y el modelo de objetos, mientras que PS3.18 define servicios web para gestionar y distribuir objetos DICOM. Convertir prematuramente una imagen DICOM a un formato gráfico puede conservar píxeles visibles y perder identidad, geometría, modalidad, parámetros de adquisición o relaciones entre objetos; por eso la arquitectura debe distinguir el objeto nativo de sus derivados.",
                "En secuenciación, el linaje también forma parte del dato. NCBI describe FASTQ como una representación textual de lecturas con bases y puntuaciones de calidad; GA4GH mantiene especificaciones SAM/BAM para alineamientos y VCF para variación genética. FASTQ, BAM y VCF no son tres copias de la misma tabla: corresponden a etapas y objetos distintos. El identificador de muestra, la ejecución, el genoma de referencia y la versión de las herramientas deben acompañar el recorrido para que una llamada de variante pueda rastrearse hasta sus entradas.",
                "Estas familias no se integran borrando sus diferencias. Se integran mediante una arquitectura que conserva el objeto nativo y añade una capa explícita de relación. Una persona sintética puede tener recursos clínicos, un flujo de dispositivo, un estudio DICOM y una muestra de secuenciación, pero cada dominio mantiene identificadores y granularidades propias. La unión entre dominios debe documentarse como una relación construida, no como igualdad implícita de nombres o números."
            ],
            "key_points": [
                "FHIR representa e intercambia recursos clínicos; no prescribe el esquema interno de toda historia clínica.",
                "Una serie de sensor necesita dispositivo, canal, reloj, unidades y contexto además de valores.",
                "DICOM combina objetos, metadatos e identidad; un derivado visual no sustituye el objeto fuente.",
                "FASTQ, SAM/BAM y VCF representan etapas diferentes y requieren linaje de muestra y referencia."
            ]
        },
        {
            "heading": "3. Identidad, tiempo y fronteras arquitectónicas",
            "paragraphs": [
                "El problema más peligroso de una arquitectura multimodal suele ser la identidad. Un MRN local, un identificador FHIR, un UID DICOM, un número de serie de dispositivo y un identificador de muestra pertenecen a espacios de nombres diferentes. Que dos campos contengan el mismo texto no demuestra que representen la misma entidad. Una tabla de enlace o servicio de identidad debe declarar sistema emisor, tipo de identificador, ámbito y regla de correspondencia, además de permitir que el vínculo sea desconocido o ambiguo.",
                "El tiempo tampoco es una sola columna. Deben distinguirse, según la fuente, tiempo clínico del evento, tiempo de adquisición, tiempo del dispositivo, tiempo de creación del objeto y tiempo de llegada al sistema. En una señal uniformemente muestreada puede reconstruirse idealmente el tiempo como t_i = t_0 + i/f_s, pero esa relación solo es válida si el reloj está definido, no existen huecos no documentados y la frecuencia real corresponde a la declarada. Los datos con deriva, reinicios o paquetes perdidos requieren conservar timestamps y eventos de adquisición.",
                "Una arquitectura de U1 puede representarse como fuente → interfaz o exportación → aterrizaje lógico → consumidor, pero cada flecha debe conservar metadatos de procedencia. El aterrizaje lógico significa aquí una frontera donde la representación fuente queda accesible y versionada; la elección concreta de base de datos, lago o almacén pertenece a U3. Del mismo modo, parsear, convertir unidades o mapear códigos pertenece a U2 y no debe esconderse dentro de un diagrama de U1.",
                "También debe distinguirse un estándar de intercambio de un modelo común para análisis. FHIR y DICOM se diseñan principalmente para representar e intercambiar información de sus dominios; OMOP CDM organiza datos observacionales para análisis bajo un modelo común. Transformar una fuente a OMOP puede ser útil en una fase posterior, pero no vuelve innecesario conservar la procedencia ni convierte el CDM en sustituto del objeto fuente. Esta separación evita elegir una única representación como si sirviera igualmente para captura, intercambio, archivo, análisis y auditoría.",
                "La frontera de U1 debe ser deliberada: aquí se decide qué llega y qué significado debe preservarse. U2 resolverá transformaciones y validación de esquemas; U3 la arquitectura física de almacenamiento y modelado; U4 métricas de calidad, linaje y versionado operacional; U5 orquestación y observabilidad; y U6 controles de acceso, seudonimización, documentación y contratos de productos. Adelantar esos temas diluye la progresión y dificulta localizar responsabilidades."
            ],
            "equations": [
                {
                    "latex": "t_i=t_0+\\frac{i}{f_s}",
                    "meaning": "Tiempo ideal de la muestra i en una señal uniformemente muestreada; solo es reconstruible si el origen temporal y la frecuencia son válidos y no hay huecos no documentados.",
                    "variables": {
                        "t_i": "tiempo ideal de la muestra i",
                        "t_0": "tiempo de la primera muestra",
                        "i": "índice entero de muestra",
                        "f_s": "frecuencia de muestreo en muestras por segundo"
                    }
                }
            ],
            "key_points": [
                "No unir identidades de distintos sistemas sin ámbito y regla de correspondencia explícitos.",
                "Distinguir tiempo del evento, adquisición y llegada; documentar relojes y huecos.",
                "Conservar una frontera fuente antes de las transformaciones de U2 y el almacenamiento de U3.",
                "Diferenciar estándares de intercambio de modelos comunes orientados al análisis."
            ]
        },
        {
            "heading": "4. Contrato de fuente, controles y arquitectura reproducible",
            "paragraphs": [
                "El producto técnico de U1 es un contrato de fuente y un mapa arquitectónico, no un pipeline ejecutado. Para cada fuente el contrato declara objetos esperados, identificadores y su ámbito, campos o metadatos indispensables, semántica temporal, unidades o códigos, versión del estándar o formato, procedencia y política ante objetos desconocidos. Debe ser suficientemente preciso para que U2 pueda implementar la ingesta sin redescubrir qué significaba cada elemento.",
                "Los controles de U1 prueban supuestos arquitectónicos antes de transformar. Un identificador clínico que no aparece en la tabla de enlace debe quedar sin resolver; un flujo de sensor con un salto temporal debe conservar el hueco; un estudio DICOM debe mantener UIDs y metadatos esenciales aunque exista un derivado; y un VCF asociado a una referencia diferente de la esperada debe marcar la incompatibilidad. El objetivo no es corregir todavía el dato, sino impedir que la arquitectura lo acepte silenciosamente como equivalente.",
                "La reproducibilidad exige una matriz de fuentes con versión, ejemplo sintético, contrato, propietario lógico, interfaz y consumidor previsto. Un diagrama bonito sin esa tabla puede ocultar supuestos decisivos. A la inversa, una tabla aislada puede dificultar ver recorridos y dependencias. El estudiante debe mantener ambos artefactos sincronizados y versionados, de forma que otra persona pueda reconstruir por qué una fuente entra por determinada frontera y qué metadatos se preservan.",
                "El caso integrador de la unidad usa exclusivamente entidades ficticias: un registro clínico FHIR, una serie de dispositivo, un estudio DICOM y una muestra genómica. La tarea consiste en describir sus objetos y relaciones, no en combinar datos reales ni en construir una identidad clínica. Los enlaces entre dominios son claves sintéticas documentadas y cualquier incertidumbre de correspondencia debe representarse explícitamente en lugar de resolverse por aproximación.",
                "Una arquitectura que pasa estos controles solo demuestra coherencia técnica del diseño para el escenario sintético. No demuestra interoperabilidad real entre productos, calidad del dato en producción, validez clínica, seguridad, privacidad, cumplimiento regulatorio ni idoneidad para una decisión asistencial. Esas capas requieren pruebas y gobernanza adicionales, varias de las cuales aparecen en U2–U6 o en otras asignaturas del currículo."
            ],
            "key_points": [
                "El contrato de fuente define qué debe preservarse antes de implementar la ingesta.",
                "Los controles deben hacer visibles enlaces desconocidos, huecos temporales y versiones incompatibles.",
                "Diagrama y matriz de fuentes deben ser reproducibles, versionados y mutuamente coherentes.",
                "La coherencia arquitectónica de un caso sintético no equivale a interoperabilidad, calidad o validez clínica real."
            ]
        }
    ],
    "glossary": [
        {"term": "Sistema fuente", "definition": "Sistema, dispositivo, instrumento o proceso que origina un objeto o evento de datos antes de su integración."},
        {"term": "Fuente biomédica", "definition": "Conjunto de objetos u observaciones producidos por un sistema fuente con granularidad, semántica, identidad, tiempo y procedencia definidos."},
        {"term": "Unidad de observación", "definition": "Entidad o evento al que corresponde un registro; debe diferenciarse de sujetos, muestras, encuentros, dispositivos u objetos relacionados."},
        {"term": "Granularidad", "definition": "Nivel de detalle al que una fuente representa información, por ejemplo encuentro, observación, muestra temporal, objeto de imagen o lectura de secuenciación."},
        {"term": "FHIR", "definition": "Estándar HL7 basado en recursos para representar e intercambiar información sanitaria; no es el esquema interno universal de una historia clínica."},
        {"term": "Recurso FHIR", "definition": "Unidad estructurada de información definida por FHIR, con identidad, elementos y referencias según el tipo de recurso."},
        {"term": "ISO/IEEE 11073", "definition": "Familia de estándares de informática sanitaria orientada a modelos y comunicación interoperable de información de dispositivos de salud."},
        {"term": "Serie temporal", "definition": "Secuencia de observaciones asociadas a instantes u orden temporal; requiere declarar reloj, frecuencia o timestamps y eventos de adquisición."},
        {"term": "Tiempo de evento", "definition": "Instante al que corresponde el fenómeno u observación representada, que puede diferir del tiempo de transmisión o ingreso."},
        {"term": "Tiempo de ingesta", "definition": "Instante en que un objeto llega a una frontera de datos; no debe sustituir silenciosamente al tiempo clínico o de adquisición."},
        {"term": "DICOM", "definition": "Estándar para información y comunicaciones de imagen médica que define objetos, metadatos, identificadores y servicios además de los datos de imagen."},
        {"term": "DICOMweb", "definition": "Servicios web REST definidos en DICOM PS3.18 para gestionar y distribuir objetos DICOM mediante HTTP."},
        {"term": "UID DICOM", "definition": "Identificador único usado por DICOM para identificar objetos y entidades dentro de su modelo; no equivale a un identificador clínico de persona."},
        {"term": "FASTQ", "definition": "Formato textual usado para lecturas de secuenciación que incluye secuencia y puntuaciones de calidad por base."},
        {"term": "SAM/BAM", "definition": "Formatos estandarizados para representar alineamientos de secuencias; SAM es textual y BAM su representación binaria habitual."},
        {"term": "VCF", "definition": "Formato de texto estandarizado para representar variantes genéticas y metadatos relacionados con muestras y llamadas."},
        {"term": "Muestra biológica", "definition": "Material biológico obtenido para una medición o ensayo; su identificador debe conservarse separado de la identidad de la persona y del run analítico."},
        {"term": "Genoma de referencia", "definition": "Secuencia de referencia y versión frente a la que pueden alinearse lecturas o describirse variantes; forma parte de la interpretación del resultado."},
        {"term": "Procedencia", "definition": "Información que permite reconstruir origen, contexto, versión y relaciones de derivación de un objeto de datos."},
        {"term": "Espacio de nombres", "definition": "Ámbito en el que un identificador es único; dos valores iguales en espacios distintos no prueban identidad de entidad."},
        {"term": "Tabla de enlace", "definition": "Representación explícita de correspondencias entre identificadores de dominios o sistemas diferentes, con reglas y ambigüedad documentadas."},
        {"term": "Contrato de fuente", "definition": "Especificación de objetos, identificadores, tiempos, semántica, versiones y metadatos que una fuente debe exponer o preservar en su frontera."},
        {"term": "Representación nativa", "definition": "Forma en la que el dominio o sistema fuente expresa el objeto antes de normalizaciones posteriores, por ejemplo un objeto DICOM o un archivo FASTQ."},
        {"term": "Modelo común analítico", "definition": "Estructura normalizada diseñada para análisis comparables entre fuentes, como OMOP CDM; no sustituye por sí misma la procedencia del dato fuente."},
        {"term": "OMOP CDM", "definition": "Modelo común de datos mantenido por la comunidad OHDSI para organizar datos observacionales de salud con fines analíticos."}
    ],
    "worked_examples": [
        {
            "title": "Recurso clínico: una presión arterial no es una fila universal",
            "scenario": "Un caso sintético contiene un recurso FHIR Observation de presión arterial vinculado a un Encounter y a un identificador local del sujeto.",
            "steps": [
                "Identificar el objeto fuente: Observation, no 'paciente' como unidad genérica.",
                "Registrar servidor o sistema emisor, versión FHIR, identificador y referencias del recurso.",
                "Declarar tiempo efectivo de la observación, unidades y sistema de códigos de los componentes.",
                "Mantener separado el identificador local de cualquier clave analítica sintética posterior."
            ],
            "result": "El contrato de fuente describe qué elementos clínicos y semánticos debe preservar U2 al ingerir el recurso.",
            "interpretation": "La arquitectura puede ubicar el recurso y sus referencias sin asumir que FHIR reproduce el esquema interno del EHR.",
            "limitation": "No demuestra que otra implementación FHIR sea interoperable sin perfiles, terminologías y pruebas de conformidad compatibles."
        },
        {
            "title": "Serie de dispositivo: distinguir índice de muestra y reloj",
            "scenario": "Un dispositivo sintético registra 12 muestras de frecuencia cardiaca a 1 Hz, pero falta el dato que correspondería al índice 5.",
            "steps": [
                "Registrar identificador y modelo del dispositivo, canal, unidad y tiempo inicial t0.",
                "Usar t_i=t_0+i/f_s solo como expectativa para muestreo uniforme.",
                "Comparar timestamps observados con la expectativa e identificar el hueco en vez de desplazar las muestras siguientes.",
                "Conservar el evento de pérdida para que U2 y U4 puedan decidir cómo tratarlo posteriormente."
            ],
            "result": "La arquitectura preserva valores, timestamps, frecuencia declarada y un evento explícito de pérdida.",
            "interpretation": "El tiempo puede reconstruirse únicamente bajo supuestos de reloj y muestreo que deben quedar documentados.",
            "limitation": "El ejercicio no valida precisión del sensor ni autoriza interpolar la muestra faltante."
        },
        {
            "title": "Imagen médica: conservar DICOM antes de crear un derivado",
            "scenario": "Un estudio CT sintético contiene un Study Instance UID, dos Series Instance UIDs y múltiples SOP Instance UIDs; se desea mostrar una miniatura en una aplicación.",
            "steps": [
                "Registrar la jerarquía y los UIDs como identidad de los objetos DICOM.",
                "Separar metadatos y datos de imagen de la miniatura derivada.",
                "Mantener la referencia desde el derivado al objeto fuente y la versión del proceso que lo generó.",
                "Describir DICOMweb como una posible interfaz, no como sustituto de la semántica DICOM."
            ],
            "result": "El diseño permite usar un derivado visual sin perder el vínculo con los objetos DICOM originales.",
            "interpretation": "El objeto fuente conserva información que una exportación gráfica puede no representar.",
            "limitation": "No se evalúan diagnóstico, calidad de imagen ni desidentificación del estudio real."
        },
        {
            "title": "Ómicas: FASTQ, BAM y VCF son etapas diferentes",
            "scenario": "Una muestra genómica ficticia produce FASTQ, se alinea contra GRCh38 y genera posteriormente un VCF.",
            "steps": [
                "Asignar identificadores distintos a muestra, ejecución, archivos y análisis.",
                "Registrar FASTQ como lecturas y calidad, BAM como alineamientos y VCF como variantes llamadas.",
                "Conservar referencia GRCh38 y versiones de herramientas como parte del linaje.",
                "Relacionar los objetos mediante procedencia, no reemplazando el FASTQ por el VCF."
            ],
            "result": "Se obtiene un grafo simple de procedencia muestra → FASTQ → alineamiento BAM → VCF con referencia y versiones explícitas.",
            "interpretation": "Cada representación responde a preguntas diferentes y el resultado final depende de sus antecedentes.",
            "limitation": "No se interpreta significancia clínica de variantes ni se evalúa calidad bioinformática profunda."
        },
        {
            "title": "Arquitectura multimodal sin fusionar identidades por intuición",
            "scenario": "Un sujeto completamente sintético tiene recursos FHIR, una serie de dispositivo, un estudio DICOM y una muestra genómica; cada fuente usa un identificador distinto.",
            "steps": [
                "Construir una matriz con sistema fuente, objeto, granularidad, identificador, tiempo, formato/estándar y procedencia.",
                "Crear una clave analítica sintética y una tabla de enlace que relacione de forma explícita cada identificador local.",
                "Dibujar fuente → interfaz → aterrizaje lógico → consumidor sin especificar aún transformaciones o tecnología física de almacenamiento.",
                "Marcar como no resuelta cualquier correspondencia ausente en la tabla de enlace."
            ],
            "result": "La arquitectura conserva cuatro dominios diferenciados y una capa de relación explícita y auditable.",
            "interpretation": "La integración empieza preservando diferencias y procedencia, no eliminándolas.",
            "limitation": "Una arquitectura coherente sobre datos sintéticos no demuestra calidad, privacidad, interoperabilidad de producción ni validez clínica."
        }
    ],
    "guided_activities": [
        {
            "title": "Actividad guiada: arquitectura de entrada para un caso biomédico multimodal sintético",
            "instructions": [
                "Trabaja únicamente con el escenario ficticio proporcionado por la actividad; no uses historias clínicas, imágenes, señales, secuencias, identificadores ni contratos reales.",
                "Mantén separadas las cuatro fuentes: clínica/FHIR, dispositivo, imagen/DICOM y ómicas; no conviertas todavía los datos ni elijas una base de datos física.",
                "Para cada objeto declara unidad de observación, identificador y espacio de nombres, tiempo relevante, unidades/códigos, versión y procedencia.",
                "Documenta explícitamente las correspondencias de identidad en una tabla de enlace; permite estados 'desconocido' y 'ambiguo'.",
                "Separa qué resuelve U1 de qué deberá resolver U2, U3, U4, U5 y U6.",
                "Entrega diagrama y matriz de fuentes versionados y verifica que ambos describen la misma arquitectura."
            ],
            "problems": [
                "Clasifica un recurso FHIR Observation, un stream de dispositivo, una serie DICOM, un FASTQ, un BAM y un VCF por objeto y granularidad.",
                "Para la fuente clínica, identifica qué referencias deben conservarse para no convertir una observación en una fila aislada.",
                "Para el dispositivo, distingue tiempo de adquisición, tiempo de llegada y frecuencia declarada; introduce un hueco temporal sintético y decide qué debe conservar U1.",
                "Para imagen, construye la jerarquía sintética Study → Series → Instance e identifica qué se pierde si solo se conserva una miniatura PNG.",
                "Para ómicas, dibuja la procedencia muestra → FASTQ → BAM → VCF e incluye versión del genoma de referencia.",
                "Crea una tabla de enlace entre cuatro identificadores locales y una clave analítica sintética; añade un caso sin correspondencia conocida.",
                "Distingue qué elementos del diseño son representación nativa, estándar de intercambio y modelo común analítico.",
                "Compara FHIR con OMOP CDM y explica por qué no deben presentarse como sustitutos equivalentes.",
                "Propón una interfaz de acceso para FHIR, DICOM y una fuente de archivos ómicos sin prescribir todavía la transformación interna.",
                "Define un contrato de fuente mínimo para cada dominio con al menos ocho campos o metadatos obligatorios.",
                "Ejecuta cuatro controles: identificador no enlazado, hueco temporal, UID/objeto derivado y referencia genómica incompatible; especifica el comportamiento esperado.",
                "Redacta una conclusión de máximo 180 palabras que separe coherencia arquitectónica, interoperabilidad, calidad, privacidad y validez clínica."
            ],
            "deliverables": [
                "Matriz de inventario de fuentes con cuatro dominios y objetos principales.",
                "Diagrama fuente → interfaz → aterrizaje lógico → consumidor.",
                "Tabla de identidad con espacios de nombres, correspondencias y casos no resueltos.",
                "Tabla de semántica temporal con tiempo de evento, adquisición e ingesta cuando corresponda.",
                "Grafo de procedencia de imagen derivada y de datos genómicos.",
                "Cuatro contratos de fuente con campos, significado, versión y metadatos mínimos.",
                "Registro de controles con entrada sintética, resultado esperado y razón del control.",
                "Matriz de handoff U1→U2/U3/U4/U5/U6 y conclusión limitada al escenario."
            ],
            "checking_criteria": [
                "Cada registro tiene una unidad de observación explícita y no confunde sujeto, encuentro, muestra, dispositivo u objeto.",
                "Los identificadores declaran su espacio de nombres y no se unen por coincidencia textual.",
                "FHIR se presenta como representación/intercambio y no como esquema universal de EHR.",
                "La señal conserva reloj, frecuencia o timestamps y eventos de pérdida relevantes.",
                "DICOM conserva identidad y metadatos del objeto además de cualquier derivado.",
                "El linaje ómico distingue FASTQ, BAM y VCF e incluye referencia y versiones.",
                "La arquitectura no oculta transformaciones de U2 ni decisiones de almacenamiento de U3.",
                "Los cuatro controles pueden detectar un supuesto arquitectónico roto antes de una integración silenciosa.",
                "Diagrama, matriz, contratos y tabla de enlace son mutuamente coherentes y versionados.",
                "La conclusión no afirma interoperabilidad, privacidad, calidad o validez clínica que no hayan sido evaluadas."
            ]
        }
    ],
    "common_errors": [
        {"error": "Llamar 'dato clínico' a cualquier fila asociada a una persona.", "correction": "Identificar el objeto clínico concreto, su evento, referencias y contexto antes de integrarlo."},
        {"error": "Tratar FHIR como el esquema interno universal de una historia clínica.", "correction": "Usar FHIR como estándar de representación/intercambio y conservar procedencia, perfiles, versiones y semántica del sistema fuente."},
        {"error": "Unir MRN, identificador FHIR, UID DICOM, serial de dispositivo o sample ID por coincidencia de texto.", "correction": "Declarar espacios de nombres y usar una tabla o servicio explícito de correspondencias."},
        {"error": "Guardar solo valores de un sensor sin reloj, canal, unidad ni eventos de pérdida.", "correction": "Conservar metadatos de adquisición suficientes para reconstruir temporalidad y significado."},
        {"error": "Convertir DICOM a PNG y descartar el objeto original.", "correction": "Mantener el objeto DICOM y su identidad/procedencia; registrar los derivados como objetos separados."},
        {"error": "Tratar FASTQ, BAM y VCF como versiones intercambiables del mismo dato.", "correction": "Modelar cada etapa y conservar muestra, referencia, herramientas y relaciones de derivación."},
        {"error": "Usar el tiempo de ingesta como si fuera el tiempo del evento.", "correction": "Nombrar y conservar por separado los relojes relevantes de cada fuente."},
        {"error": "Elegir una base de datos física antes de caracterizar las fuentes.", "correction": "Cerrar U1 con objetos, contratos y fronteras; decidir almacenamiento en U3."},
        {"error": "Introducir limpieza, conversión de unidades o mapeo semántico dentro de U1 sin registrarlo.", "correction": "Delegar esas transformaciones a U2 y dejar en U1 los requisitos que deben preservarse."},
        {"error": "Concluir que una arquitectura sintética coherente es clínicamente válida o interoperable en producción.", "correction": "Limitar la conclusión a coherencia del diseño y enumerar pruebas pendientes de calidad, privacidad, interoperabilidad y uso clínico."}
    ],
    "self_assessment": [
        {"question": "¿Cuál es la diferencia entre sistema fuente y representación digital?", "answer": "El sistema fuente origina el evento u objeto; la representación digital es la forma concreta en que parte de ese significado se codifica o intercambia.", "reasoning": "Separarlos evita creer que un formato como FHIR, DICOM o VCF agota el fenómeno biomédico.", "common_error": "Definir la fuente únicamente por la extensión del archivo."},
        {"question": "¿Por qué no debe unirse un MRN con un sample ID solo porque tienen el mismo valor?", "answer": "Porque pertenecen a espacios de nombres y entidades potencialmente diferentes; la correspondencia requiere una regla o tabla de enlace explícita.", "reasoning": "La identidad es contextual y debe conservar ámbito y emisor.", "common_error": "Usar igualdad de cadenas como prueba de identidad."},
        {"question": "¿Qué papel tiene FHIR en U1?", "answer": "Representar e intercambiar recursos clínicos con estructura y referencias; no imponer el esquema interno universal de todos los EHR.", "reasoning": "Permite diseñar una interfaz sin borrar la procedencia del sistema fuente.", "common_error": "Equiparar FHIR con una base de datos clínica universal."},
        {"question": "¿Qué metadatos mínimos necesita una serie de sensor?", "answer": "Dispositivo, canal o magnitud, unidad, reloj o timestamps, frecuencia/patrón de muestreo, contexto de adquisición y procedencia, además de los valores.", "reasoning": "Sin ellos no puede reconstruirse con fiabilidad qué se midió ni cuándo.", "common_error": "Guardar solo un vector numérico."},
        {"question": "¿Por qué una miniatura PNG no sustituye un estudio DICOM?", "answer": "Porque puede perder UIDs, jerarquía, geometría, modalidad, parámetros de adquisición y otros metadatos del objeto fuente.", "reasoning": "El derivado y el objeto nativo tienen funciones diferentes y deben relacionarse por procedencia.", "common_error": "Suponer que conservar los píxeles visibles conserva todo el dato de imagen."},
        {"question": "¿Qué relación existe entre FASTQ, BAM y VCF?", "answer": "Representan etapas distintas: lecturas con calidad, alineamientos y variantes; deben conectarse mediante linaje de muestra, referencia y herramientas.", "reasoning": "La interpretación del producto derivado depende de sus entradas y versiones.", "common_error": "Tratar VCF como reemplazo autosuficiente de las lecturas originales."},
        {"question": "¿Cuándo es válida t_i=t_0+i/f_s?", "answer": "En un muestreo idealmente uniforme con origen temporal y frecuencia válidos y sin huecos no documentados.", "reasoning": "Deriva, reinicios o pérdida de paquetes rompen la reconstrucción puramente por índice.", "common_error": "Asignar tiempos regulares a una serie con pérdidas sin conservar la discontinuidad."},
        {"question": "¿FHIR y OMOP CDM son equivalentes?", "answer": "No. FHIR se orienta a representación e intercambio clínico; OMOP CDM es un modelo común orientado a organizar datos observacionales para análisis.", "reasoning": "Una arquitectura puede usar ambos en capas distintas y conservar el dato fuente.", "common_error": "Elegir uno como sustituto universal de captura, intercambio, archivo y análisis."},
        {"question": "¿Qué debe contener un contrato de fuente en U1?", "answer": "Objetos esperados, granularidad, identificadores y ámbito, tiempos, unidades/códigos, versión, procedencia y comportamiento ante objetos o enlaces desconocidos.", "reasoning": "U2 necesita esas condiciones para transformar sin redescubrir el significado.", "common_error": "Definir el contrato solo como una lista de nombres de columnas."},
        {"question": "¿Qué puede concluirse al completar la actividad multimodal?", "answer": "Que el diseño sintético mantiene objetos, identidades, tiempos, versiones y procedencia de forma coherente; no que sea interoperable, privado, de alta calidad o clínicamente válido en producción.", "reasoning": "Cada una de esas propiedades necesita evidencia y pruebas adicionales.", "common_error": "Convertir una demostración arquitectónica educativa en validación del sistema real."}
    ],
    "biomedical_connections": [
        {"topic": "Historia clínica e interoperabilidad", "connection": "Modelar recursos clínicos y referencias sin confundir el estándar de intercambio con la base de datos del EHR."},
        {"topic": "Monitorización fisiológica", "connection": "Preservar canal, reloj, frecuencia, unidades y procedencia de flujos de dispositivos para análisis posterior reproducible."},
        {"topic": "Imagen médica", "connection": "Mantener objetos DICOM, jerarquías, UIDs y metadatos junto con derivados destinados a visualización o análisis."},
        {"topic": "Genómica", "connection": "Conservar linaje de muestra y proceso entre lecturas FASTQ, alineamientos SAM/BAM y variantes VCF."},
        {"topic": "Datos multimodales para investigación", "connection": "Relacionar dominios con claves y contratos explícitos antes de diseñar transformaciones, almacenamiento o modelos analíticos."}
    ],
    "sources": [
        {"title": "FHIR R5 v5.0.0", "organization": "HL7 International", "year": 2023, "url": "https://hl7.org/fhir/R5/", "type": "estándar de interoperabilidad sanitaria", "description": "Versión publicada permanente de FHIR R5; define recursos y marco de intercambio de información sanitaria.", "verification_status": "verified_directly"},
        {"title": "DICOM PS3.1 2026c — Introduction and Overview", "organization": "DICOM Standards Committee / NEMA", "year": 2026, "url": "https://dicom.nema.org/medical/dicom/current/output/html/part01.html", "type": "estándar de imagen médica", "description": "Introducción y principios del estándar DICOM, incluidos objetos de información, identificación única y modelo de comunicación.", "verification_status": "verified_directly"},
        {"title": "DICOM PS3.18 2026c — Web Services", "organization": "DICOM Standards Committee / NEMA", "year": 2026, "url": "https://dicom.nema.org/medical/dicom/current/output/chtml/part18/ps3.18.html", "type": "estándar de servicios web de imagen médica", "description": "Define servicios web DICOM para gestionar y distribuir objetos DICOM mediante protocolos web.", "verification_status": "verified_directly"},
        {"title": "ISO/IEEE 11073-10206-2024 — Abstract content information model", "organization": "IEEE Standards Association / ISO", "year": 2024, "url": "https://standards.ieee.org/ieee/11073-10206/11702/", "type": "estándar de interoperabilidad de dispositivos de salud", "description": "Modelo abstracto de estructura y contenido para información generada por dispositivos personales de salud.", "verification_status": "verified_directly"},
        {"title": "SRA File Format Guide", "organization": "National Center for Biotechnology Information", "url": "https://www.ncbi.nlm.nih.gov/sra/docs/submitformats/", "type": "guía técnica institucional", "description": "Describe formatos aceptados por SRA, incluido FASTQ con lecturas y puntuaciones de calidad.", "verification_status": "verified_directly"},
        {"title": "SAM/BAM", "organization": "Global Alliance for Genomics and Health", "year": 2022, "url": "https://www.ga4gh.org/product/sam-bam/", "type": "especificación de formato genómico", "description": "Producto GA4GH vigente para representar datos de alineamiento de secuencias en SAM/BAM.", "verification_status": "verified_directly"},
        {"title": "Genetic Variation Formats (VCF)", "organization": "Global Alliance for Genomics and Health", "year": 2024, "url": "https://www.ga4gh.org/product/genetic-variation-formats-vcf/", "type": "especificación de formato genómico", "description": "Producto GA4GH para representación de variación genética; VCF 4.5 es la versión publicada señalada por GA4GH.", "verification_status": "verified_directly"},
        {"title": "OMOP Common Data Model v5.4", "organization": "Observational Health Data Sciences and Informatics", "url": "https://ohdsi.github.io/CommonDataModel/", "type": "modelo común de datos observacionales", "description": "Documentación oficial de OHDSI que identifica CDM v5.4 como versión actual y describe su estructura para análisis observacionales.", "verification_status": "verified_directly"}
    ],
    "editorial_notice": "Unidad educativa curada internamente y mantenida en estado review. Las fuentes citadas respaldan estándares, formatos y modelos enseñados, pero esta curación no constituye revisión disciplinar externa ni certificación de interoperabilidad. La actividad usa exclusivamente datos e identidades sintéticas y no autoriza acceso, integración, transformación, almacenamiento, seudonimización ni uso clínico de datos reales."
})

text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
assert GENERIC not in text.casefold()
assert "PPV=" not in text
SOURCE.write_text(text, encoding="utf-8")
MIRROR.parent.mkdir(parents=True, exist_ok=True)
MIRROR.write_text(text, encoding="utf-8")

TEST.write_text('''from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-datos-biomedicos" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-datos-biomedicos" / "unit-01.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"

class IngenieriaDatosBiomedicosUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_mirror_and_status(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "ingenieria-datos-biomedicos")
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_wrong_ppv_equation_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("ppv=", text)
        self.assertIn("t_i=t_0", text)

    def test_theory_covers_four_source_families_and_boundaries(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(s["paragraphs"]) >= 5 for s in sections))
        self.assertTrue(all(len(s["key_points"]) >= 4 for s in sections))
        theory = json.dumps(sections, ensure_ascii=False).casefold()
        for concept in ("fhir", "iso/ieee 11073", "dicom", "fastq", "sam/bam", "vcf", "omop cdm", "espacio de nombres", "tiempo de ingesta"):
            self.assertIn(concept, theory)
        for boundary in ("u2", "u3", "u4", "u5", "u6"):
            self.assertIn(boundary, theory)

    def test_pedagogy_is_substantive_and_synthetic(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["problems"]), 12)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        activity_text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintét", activity_text)
        self.assertIn("no uses", activity_text)

    def test_sources_are_directly_verified_primary_or_authoritative_records(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in sources))
        urls = {s["url"] for s in sources}
        self.assertIn("https://hl7.org/fhir/R5/", urls)
        self.assertIn("https://dicom.nema.org/medical/dicom/current/output/html/part01.html", urls)
        self.assertIn("https://standards.ieee.org/ieee/11073-10206/11702/", urls)
        self.assertIn("https://www.ncbi.nlm.nih.gov/sra/docs/submitformats/", urls)
        self.assertIn("https://www.ga4gh.org/product/sam-bam/", urls)
        self.assertIn("https://www.ga4gh.org/product/genetic-variation-formats-vcf/", urls)
        self.assertIn("https://ohdsi.github.io/CommonDataModel/", urls)

    def test_editorial_boundary_is_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("datos e identidades sintéticas", notice)
        self.assertIn("u2 transformación", purpose)
        self.assertIn("u6 privacidad", purpose)

if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8")

print("Curated Biomedical Data Engineering U1 and exact generated mirror")
