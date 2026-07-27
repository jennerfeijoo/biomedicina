#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PARTIAL_ROOT = ROOT / "partial-recovery" / "data"
REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"
SOURCE_REGISTRY_ROOT = ROOT / "data" / "source_registry"
DECISION_ROOT = ROOT / "data" / "curriculum_decisions"
REVIEW_ROOT = ROOT / "data" / "course_reviews"
AUDIT_ROOT = ROOT / "data" / "course_audits"
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)

EDITORIAL_NOTICE = (
    "Material educativo en estado review. Los resultados computacionales no sustituyen "
    "validación analítica, revisión disciplinar, asesoramiento genético, diagnóstico, "
    "decisiones terapéuticas ni evaluación regulatoria."
)


def section(
    heading: str,
    concept: str,
    mechanism: str,
    quantitative: str,
    validation: str,
    limitations: str,
    key_points: list[str],
    equations: list[dict[str, Any]],
) -> dict[str, Any]:
    paragraphs = [
        (
            f"{heading} organiza el problema alrededor de {concept}. {mechanism} "
            "La representación elegida determina qué comparaciones son posibles, qué información "
            "se pierde y qué supuestos quedan incorporados antes de ejecutar cualquier algoritmo. "
            "Por eso el análisis debe comenzar con una pregunta explícita, una unidad de observación "
            "definida y un resultado admisible, en lugar de comenzar por una herramienta o por el archivo disponible."
        ),
        (
            f"La dimensión cuantitativa de esta sección se resume mediante {quantitative} "
            "Cada variable necesita escala, unidades o codificación, denominador y referencia. "
            "Una puntuación, probabilidad o distancia solo adquiere significado cuando se conoce el modelo "
            "que la produce y la población de alternativas con la que se compara. La precisión numérica no "
            "corrige un modelo mal especificado, una referencia inadecuada ni datos que no representan la pregunta biológica."
        ),
        (
            f"La validación reproducible requiere {validation} "
            "Los controles deben detectar errores de identidad, orientación, formato, versión, cobertura y contaminación, "
            "además de comprobar que los resultados cambian de forma coherente ante perturbaciones conocidas. "
            "Cuando sea posible, conviene usar datos sintéticos, truth sets o métodos ortogonales para separar un fallo "
            "del algoritmo de un fallo de preparación, muestreo o anotación."
        ),
        (
            f"La interpretación integrada debe considerar {limitations} "
            "Una salida bioinformática puede describir similitud, asociación o compatibilidad con un modelo, pero no demuestra "
            "automáticamente homología funcional, mecanismo causal, validez clínica ni beneficio para una persona. "
            "La conclusión final debe identificar qué fue medido, qué fue inferido, qué alternativas permanecen abiertas y "
            "qué evidencia independiente sería necesaria para cambiar una decisión biomédica."
        ),
    ]
    return {
        "heading": heading,
        "paragraphs": paragraphs,
        "key_points": key_points,
        "equations": equations,
    }


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "ncbi-guide": {
        "title": "NCBI Resource Guide",
        "organization": "National Center for Biotechnology Information",
        "url": "https://www.ncbi.nlm.nih.gov/guide/",
        "type": "documentación oficial",
        "verification_status": "verified_directly",
    },
    "ensembl-docs": {
        "title": "Ensembl Documentation",
        "organization": "Ensembl",
        "url": "https://www.ensembl.org/info/docs/index.html",
        "type": "documentación oficial",
        "verification_status": "verified_directly",
    },
    "uniprot-help": {
        "title": "UniProt Help and Documentation",
        "organization": "UniProt Consortium",
        "url": "https://www.uniprot.org/help/",
        "type": "documentación oficial",
        "verification_status": "verified_directly",
    },
    "fair-principles": {
        "title": "The FAIR Guiding Principles for scientific data management and stewardship",
        "authors_or_organization": "Wilkinson MD et al.",
        "year": 2016,
        "doi": "10.1038/sdata.2016.18",
        "type": "artículo de principios de datos",
        "verification_status": "metadata_verified",
    },
    "ga4gh": {
        "title": "GA4GH Technical Standards and Policy Frameworks",
        "organization": "Global Alliance for Genomics and Health",
        "url": "https://www.ga4gh.org/genomic-data-toolkit/",
        "type": "estándares internacionales",
        "verification_status": "verified_directly",
    },
    "blast-help": {
        "title": "BLAST Help and Documentation",
        "organization": "National Center for Biotechnology Information",
        "url": "https://blast.ncbi.nlm.nih.gov/doc/blast-help/",
        "type": "documentación oficial",
        "verification_status": "verified_directly",
    },
    "blast-paper": {
        "title": "Basic local alignment search tool",
        "authors_or_organization": "Altschul SF et al.",
        "year": 1990,
        "doi": "10.1016/S0022-2836(05)80360-2",
        "type": "artículo metodológico",
        "verification_status": "metadata_verified",
    },
    "ebi-alignments": {
        "title": "Sequence Analysis Training",
        "organization": "EMBL-EBI Training",
        "url": "https://www.ebi.ac.uk/training/online/courses/sequence-analysis-introduction/",
        "type": "formación oficial",
        "verification_status": "verified_directly",
    },
    "clustalo": {
        "title": "Fast, scalable generation of high-quality protein multiple sequence alignments using Clustal Omega",
        "authors_or_organization": "Sievers F et al.",
        "year": 2011,
        "doi": "10.1038/msb.2011.75",
        "type": "artículo metodológico",
        "verification_status": "metadata_verified",
    },
    "iqtree": {
        "title": "IQ-TREE Documentation",
        "organization": "IQ-TREE Development Team",
        "url": "https://iqtree.github.io/doc/",
        "type": "documentación de software",
        "verification_status": "verified_directly",
    },
    "fastqc": {
        "title": "FastQC: A Quality Control Tool for High Throughput Sequence Data",
        "organization": "Babraham Bioinformatics",
        "url": "https://www.bioinformatics.babraham.ac.uk/projects/fastqc/",
        "type": "documentación de software",
        "verification_status": "verified_directly",
    },
    "hts-specs": {
        "title": "SAM/BAM, CRAM and VCF Specifications",
        "organization": "Global Alliance for Genomics and Health / samtools",
        "url": "https://samtools.github.io/hts-specs/",
        "type": "especificaciones técnicas",
        "verification_status": "verified_directly",
    },
    "gatk": {
        "title": "GATK Best Practices Workflows",
        "organization": "Broad Institute",
        "url": "https://gatk.broadinstitute.org/hc/en-us/categories/360002310591",
        "type": "documentación oficial",
        "verification_status": "verified_directly",
    },
    "giab": {
        "title": "Genome in a Bottle",
        "organization": "National Institute of Standards and Technology",
        "url": "https://www.nist.gov/programs-projects/genome-bottle",
        "type": "materiales de referencia",
        "verification_status": "verified_directly",
    },
    "acmg": {
        "title": "Standards and guidelines for the interpretation of sequence variants",
        "authors_or_organization": "Richards S et al.",
        "year": 2015,
        "doi": "10.1038/gim.2015.30",
        "type": "guía profesional",
        "verification_status": "metadata_verified",
    },
    "encode-rna": {
        "title": "ENCODE RNA-seq Standards and Processing Information",
        "organization": "ENCODE Project Consortium",
        "url": "https://www.encodeproject.org/data-standards/rna-seq/",
        "type": "estándar de consorcio",
        "verification_status": "verified_directly",
    },
    "star": {
        "title": "STAR: ultrafast universal RNA-seq aligner",
        "authors_or_organization": "Dobin A et al.",
        "year": 2013,
        "doi": "10.1093/bioinformatics/bts635",
        "type": "artículo metodológico",
        "verification_status": "metadata_verified",
    },
    "salmon": {
        "title": "Salmon provides fast and bias-aware quantification of transcript expression",
        "authors_or_organization": "Patro R et al.",
        "year": 2017,
        "doi": "10.1038/nmeth.4197",
        "type": "artículo metodológico",
        "verification_status": "metadata_verified",
    },
    "deseq2": {
        "title": "Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2",
        "authors_or_organization": "Love MI, Huber W, Anders S",
        "year": 2014,
        "doi": "10.1186/s13059-014-0550-8",
        "type": "artículo metodológico",
        "verification_status": "metadata_verified",
    },
    "bioc-rnaseq": {
        "title": "RNA-seq workflow: gene-level exploratory analysis and differential expression",
        "organization": "Bioconductor",
        "url": "https://bioconductor.org/help/workflows/rnaseqGene/",
        "type": "workflow reproducible",
        "verification_status": "verified_directly",
    },
    "go-docs": {
        "title": "Gene Ontology Documentation",
        "organization": "Gene Ontology Consortium",
        "url": "https://geneontology.org/docs/",
        "type": "documentación de ontología",
        "verification_status": "verified_directly",
    },
    "go-paper": {
        "title": "Gene ontology: tool for the unification of biology",
        "authors_or_organization": "The Gene Ontology Consortium",
        "year": 2000,
        "doi": "10.1038/75556",
        "type": "artículo de referencia",
        "verification_status": "metadata_verified",
    },
    "gsea": {
        "title": "Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles",
        "authors_or_organization": "Subramanian A et al.",
        "year": 2005,
        "doi": "10.1073/pnas.0506580102",
        "type": "artículo metodológico",
        "verification_status": "metadata_verified",
    },
    "reactome": {
        "title": "Reactome User Guide",
        "organization": "Reactome",
        "url": "https://reactome.org/userguide",
        "type": "base de conocimiento",
        "verification_status": "verified_directly",
    },
    "string": {
        "title": "STRING Database Documentation",
        "organization": "STRING Consortium",
        "url": "https://string-db.org/cgi/help",
        "type": "base de datos de redes",
        "verification_status": "verified_directly",
    },
    "nextflow": {
        "title": "Nextflow Documentation",
        "organization": "Seqera / Nextflow",
        "url": "https://www.nextflow.io/docs/latest/",
        "type": "documentación de workflow",
        "verification_status": "verified_directly",
    },
    "nfcore": {
        "title": "nf-core Documentation",
        "organization": "nf-core community",
        "url": "https://nf-co.re/docs/",
        "type": "estándares comunitarios de pipelines",
        "verification_status": "verified_directly",
    },
    "apptainer": {
        "title": "Apptainer User Guide",
        "organization": "Apptainer Project",
        "url": "https://apptainer.org/docs/user/latest/",
        "type": "documentación de contenedores",
        "verification_status": "verified_directly",
    },
    "w3c-prov": {
        "title": "PROV-O: The PROV Ontology",
        "organization": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/prov-o/",
        "type": "recomendación técnica",
        "verification_status": "verified_directly",
    },
    "rocrate": {
        "title": "RO-Crate Specification",
        "organization": "Research Object Crate community",
        "url": "https://www.researchobject.org/ro-crate/specification/",
        "type": "especificación de objetos de investigación",
        "verification_status": "verified_directly",
    },
}


def eq(latex: str, meaning: str, variables: dict[str, str] | None = None) -> dict[str, Any]:
    return {"latex": latex, "meaning": meaning, "variables": variables or {}}


UNIT_CONTENT: list[dict[str, Any]] = [
    {
        "slug": "datos-bases-reproducibilidad",
        "sections": [
            section(
                "Preguntas biológicas y representaciones computacionales",
                "la traducción entre entidades biológicas y objetos computables, como secuencias, intervalos, tablas, grafos y matrices",
                "Una muestra puede representarse como una fila, una secuencia como una cadena ordenada y una red como nodos y aristas; cada transformación conserva algunas relaciones y descarta otras. Definir qué constituye una réplica, una característica y una etiqueta impide mezclar niveles como célula, muestra, paciente o cohorte.",
                "una matriz de datos X con n observaciones y p características, junto con tasas de datos ausentes, cardinalidad de identificadores y proporción de registros utilizables.",
                "comprobar dimensiones, tipos, rangos, identificadores únicos, duplicados y correspondencia entre filas y metadatos; además, un conjunto sintético pequeño debe producir un resultado conocido antes de analizar datos reales.",
                "que una misma pregunta puede admitir representaciones alternativas y que una codificación conveniente puede ocultar orientación, isoformas, dependencia jerárquica o información temporal.",
                [
                    "La representación computacional debe derivarse de la pregunta biológica.",
                    "La unidad de observación define independencia y denominadores.",
                    "Toda transformación puede conservar y perder información.",
                    "Herramienta y pregunta no son términos intercambiables.",
                ],
                [eq("X\\in\\mathbb{R}^{n\\times p}", "Representación matricial con n observaciones y p variables; la pertenencia real puede ser categórica, discreta o mixta.")],
            ),
            section(
                "Bases de datos, identificadores y anotaciones",
                "la recuperación de registros mediante accesiones estables, versiones, referencias cruzadas y evidencia de anotación",
                "Los archivos primarios preservan observaciones, mientras las bases curadas integran nomenclatura, función y relaciones derivadas. Una accesión identifica un registro, pero su versión identifica el contenido concreto; los identificadores de genes, transcritos y proteínas no deben mezclarse sin una tabla de correspondencias y reglas de especie.",
                "la cobertura de mapeo entre espacios de identificadores, calculada como la fracción de entradas con una correspondencia válida y no ambigua.",
                "registrar consulta, fecha, versión, especie, ensamblaje y reglas de filtrado; las correspondencias uno-a-muchos deben revisarse en vez de descartarse silenciosamente, y una muestra de registros debe verificarse manualmente contra la fuente.",
                "que las anotaciones cambian, tienen códigos de evidencia heterogéneos y pueden propagarse por similitud; una etiqueta funcional no equivale a demostración experimental en la especie o tejido analizado.",
                [
                    "Accesión y versión cumplen funciones diferentes.",
                    "Genes, transcritos y proteínas requieren espacios identificadores explícitos.",
                    "Las anotaciones contienen procedencia y niveles de evidencia.",
                    "Un mapeo ambiguo debe conservarse como incertidumbre.",
                ],
                [eq("c=\\frac{N_{mapeados}}{N_{entrada}}", "Cobertura de mapeo de identificadores; debe acompañarse del número de mapeos ambiguos y no encontrados.")],
            ),
            section(
                "Formatos, calidad y metadatos",
                "la relación entre estructura de archivo, semántica de campos, calidad de medición y contexto de muestra",
                "FASTA conserva secuencias, FASTQ añade calidades por base, GFF/GTF describe características genómicas, SAM/BAM registra alineamientos y VCF representa variantes. El mismo carácter o coordenada puede tener significado distinto según formato, convención de base cero o uno, ensamblaje y orientación.",
                "la escala Phred, proporciones de lecturas filtradas, distribución de longitudes y completitud de campos obligatorios, sin reducir el control de calidad a un único umbral.",
                "validar sintaxis con herramientas específicas, inspeccionar cabeceras y referencias, contrastar conteos antes y después de cada conversión y conservar metadatos de muestra, plataforma, biblioteca, lote y consentimiento.",
                "que un archivo sintácticamente válido puede ser biológicamente incorrecto; el recorte excesivo, la conversión de coordenadas o la pérdida de etiquetas puede introducir sesgos que no aparecen en un resumen agregado.",
                [
                    "El formato define la semántica de cada campo.",
                    "Las coordenadas necesitan ensamblaje y convención explícitos.",
                    "Calidad técnica y adecuación biológica son dimensiones distintas.",
                    "Los metadatos forman parte del dato analizable.",
                ],
                [eq("Q=-10\\log_{10}P(error)", "Puntuación Phred que relaciona calidad y probabilidad estimada de error; presupone calibración adecuada.")],
            ),
            section(
                "Flujo reproducible, validación e interpretación",
                "la procedencia completa desde datos de entrada hasta artefactos, parámetros, resultados y decisiones de exclusión",
                "Un análisis reproducible puede modelarse como un grafo dirigido acíclico donde cada tarea consume artefactos versionados y produce salidas identificables. Los entornos, referencias y parámetros son dependencias del resultado, no detalles secundarios que puedan omitirse del informe.",
                "funciones hash, manifiestos de archivos, conteos de registros y comparaciones de regresión que permiten detectar cambios inesperados entre ejecuciones.",
                "repetir el flujo en un entorno limpio, fijar semillas cuando corresponda, conservar logs y comprobar que una modificación controlada en la entrada genera el cambio esperado en la salida.",
                "que reproducibilidad técnica no garantiza validez biológica; datos sesgados pueden producir exactamente el mismo resultado en todas las ejecuciones, y datos sensibles requieren controles de acceso y minimización.",
                [
                    "La procedencia debe conectar entradas, tareas y resultados.",
                    "Versiones y parámetros son parte del método.",
                    "Reproducibilidad técnica no equivale a validez científica.",
                    "Los datos sensibles requieren gobernanza desde el diseño.",
                ],
                [eq("h=H(D)", "Una función hash H resume el contenido D para detectar cambios; no evalúa calidad ni significado biológico.")],
            ),
        ],
        "glossary": [
            ("Unidad de observación", "Entidad sobre la que se registra una medición independiente o jerárquica."),
            ("Característica", "Variable computacional derivada o medida para describir una observación."),
            ("Accesión", "Identificador asignado por una base a un registro."),
            ("Versión", "Estado específico del contenido asociado a una accesión o recurso."),
            ("Anotación", "Información interpretativa vinculada a una entidad biológica y su evidencia."),
            ("FASTA", "Formato textual para secuencias y sus identificadores."),
            ("FASTQ", "Formato que combina secuencia y calidades por posición."),
            ("Metadato", "Dato que describe procedencia, contexto, método o condiciones de otro dato."),
            ("Procedencia", "Registro de origen y transformaciones de un artefacto."),
            ("Checksum", "Resumen criptográfico utilizado para detectar cambios de contenido."),
            ("Esquema", "Reglas que definen campos, tipos y relaciones de un conjunto de datos."),
            ("FAIR", "Principios para datos localizables, accesibles, interoperables y reutilizables."),
        ],
        "examples": [
            {
                "title": "Pérdida de registros al mapear identificadores",
                "scenario": "Una lista de 1200 transcritos se convierte a genes y solo 850 obtienen una correspondencia única.",
                "reasoning_steps": [
                    "Registrar versiones de los identificadores de origen y destino.",
                    "Separar correspondencias únicas, múltiples, obsoletas y ausentes.",
                    "Calcular cobertura y evaluar si la pérdida se concentra en una categoría biológica.",
                    "Repetir con una tabla de correspondencias específica de especie y versión.",
                ],
                "interpretation": "La lista convertida no representa automáticamente el universo original; la pérdida y ambigüedad deben acompañar cualquier análisis posterior.",
                "limitations": ["La cobertura no mide corrección funcional.", "Un identificador puede cambiar sin que cambie la entidad biológica."],
            },
            {
                "title": "Archivo reproducible con referencia incorrecta",
                "scenario": "Un pipeline se ejecuta de forma idéntica, pero mezcla coordenadas de dos ensamblajes humanos.",
                "reasoning_steps": [
                    "Comparar cabeceras y nombres de contigs con la referencia declarada.",
                    "Identificar el punto de conversión donde se perdió la versión del ensamblaje.",
                    "Usar regiones control para comprobar coordenadas conocidas.",
                    "Corregir la referencia y registrar un test de regresión.",
                ],
                "interpretation": "La repetibilidad del error no lo convierte en un resultado válido; la identidad de la referencia es parte del método.",
                "limitations": ["Un lift-over también puede ser ambiguo.", "No todas las regiones tienen correspondencia entre ensamblajes."],
            },
        ],
        "biomedical": [
            ("Genómica clínica", "Las versiones de referencia e identificadores condicionan la interpretación de variantes."),
            ("Datos ómicos", "Metadatos de muestra, plataforma y lote determinan comparabilidad y reutilización."),
            ("Bases de conocimiento", "Las anotaciones deben conservar evidencia, fecha y procedencia."),
            ("Gobernanza", "Privacidad, licencia, acceso y retención forman parte del flujo analítico."),
        ],
        "sources": ["ncbi-guide", "ensembl-docs", "uniprot-help", "fair-principles", "ga4gh"],
    },
    {
        "slug": "alineamiento-homologia-filogenia",
        "sections": [
            section(
                "Puntuación, sustituciones y brechas",
                "la definición explícita de coincidencias, sustituciones y eventos de inserción o eliminación",
                "Una función de puntuación combina recompensas por coincidencia, penalizaciones por sustitución y costes de brecha. En proteínas, matrices como PAM o BLOSUM resumen patrones evolutivos observados, mientras que en ADN la composición y el objetivo determinan si una puntuación simple es suficiente.",
                "un score aditivo y una penalización afín de brecha que separa el coste de abrir una brecha del coste de extenderla.",
                "examinar alineamientos simulados con tasas conocidas, comprobar simetría y unidades de la matriz, variar penalizaciones y verificar que regiones no homólogas no reciben puntuaciones altas por composición sesgada.",
                "que el mejor score depende de los parámetros y no es una probabilidad directa; secuencias repetitivas, baja complejidad y sesgo composicional pueden producir alineamientos plausibles pero espurios.",
                [
                    "La función de puntuación expresa un modelo de cambio.",
                    "Abrir y extender una brecha representan costes diferentes.",
                    "Matrices proteicas dependen del contexto evolutivo.",
                    "Un score alto necesita una referencia estadística.",
                ],
                [eq("g(k)=g_o+(k-1)g_e", "Penalización afín para una brecha de longitud k, con costes separados de apertura y extensión.", {"g_o": "coste de apertura", "g_e": "coste de extensión"})],
            ),
            section(
                "Alineamiento global, local y programación dinámica",
                "la optimización de correspondencias entre secuencias completas o regiones con similitud localizada",
                "Needleman-Wunsch busca una solución global y Smith-Waterman reinicia puntuaciones negativas para identificar segmentos locales. Ambos algoritmos descomponen el problema en subproblemas y almacenan soluciones parciales en una matriz, lo que garantiza el óptimo respecto de la función de puntuación declarada.",
                "una recurrencia dinámica que compara diagonal, inserción y eliminación, seguida de traceback para reconstruir uno o varios alineamientos óptimos.",
                "probar secuencias cortas con solución manual, verificar bordes e inicialización, comparar score y traceback y repetir con parámetros alternativos para evaluar estabilidad.",
                "que óptimo algorítmico no significa homología biológica; varios tracebacks pueden compartir score y la complejidad cuadrática limita el uso directo con secuencias largas.",
                [
                    "Global y local responden preguntas distintas.",
                    "La recurrencia depende de una función de puntuación declarada.",
                    "El traceback traduce el óptimo en correspondencias explícitas.",
                    "Puede existir más de un alineamiento óptimo.",
                ],
                [eq("F_{i,j}=\\max(F_{i-1,j-1}+s_{i,j},F_{i-1,j}-g,F_{i,j-1}-g)", "Recurrencia simplificada de alineamiento global con penalización lineal de brecha.")],
            ),
            section(
                "Búsqueda de similitud, BLAST y homología",
                "la exploración eficiente de bases extensas mediante palabras semilla, extensión local y calibración estadística",
                "BLAST reduce el espacio de búsqueda identificando coincidencias iniciales y extendiéndolas bajo umbrales definidos. El resultado informa query, subject, score, E-value, identidad, cobertura y orientación; ninguno de estos campos por separado establece homología funcional.",
                "el valor esperado de alineamientos con score al menos S en un espacio de búsqueda de tamaños m y n, ajustado por parámetros estadísticos de la matriz.",
                "usar controles positivos y secuencias aleatorias con composición comparable, inspeccionar cobertura y dominios, repetir contra bases versionadas y confirmar hits críticos con alineamiento independiente y arquitectura proteica.",
                "que bases redundantes, contaminación, baja complejidad y secuencias cortas alteran la significancia; homología es una relación histórica y no un porcentaje graduable.",
                [
                    "BLAST es heurístico y no garantiza el óptimo global.",
                    "E-value depende del score y del espacio de búsqueda.",
                    "Cobertura e identidad deben interpretarse conjuntamente.",
                    "Homología no es sinónimo de función equivalente.",
                ],
                [eq("E=Kmn e^{-\\lambda S}", "Número esperado de alineamientos con score al menos S bajo el modelo estadístico de BLAST.", {"m,n": "tamaños efectivos", "K,lambda": "parámetros de calibración"})],
            ),
            section(
                "Alineamiento múltiple, perfiles y filogenia",
                "la comparación simultánea de familias de secuencias y la inferencia explícita de relaciones evolutivas",
                "Los alineamientos múltiples suelen usar estrategias progresivas o iterativas porque optimizar todas las secuencias simultáneamente es costoso. El alineamiento alimenta perfiles, identificación de motivos y modelos filogenéticos, pero errores tempranos pueden propagarse al árbol y a la transferencia funcional.",
                "distancias por sitio, modelos de sustitución, verosimilitud de árboles y soportes por remuestreo que cuantifican aspectos diferentes de la incertidumbre.",
                "comparar algoritmos y órdenes de entrada, recortar regiones ambiguas con criterios declarados, evaluar modelos de sustitución y examinar estabilidad de clados mediante bootstrap o métodos equivalentes.",
                "que un árbol de genes no es automáticamente un árbol de especies; recombinación, duplicación, transferencia horizontal, muestreo y mala alineación pueden cambiar la topología.",
                [
                    "El alineamiento múltiple es una hipótesis de correspondencia.",
                    "Los perfiles resumen conservación y variación posicional.",
                    "Soporte de rama no equivale a probabilidad causal.",
                    "Árboles de genes y especies pueden diferir.",
                ],
                [eq("p=\\frac{d}{L}", "Distancia p como fracción de posiciones diferentes d sobre L sitios comparables; subestima sustituciones múltiples.")],
            ),
        ],
        "glossary": [
            ("Alineamiento", "Hipótesis de correspondencia entre posiciones de secuencias."),
            ("Score", "Valor de una función de puntuación aplicada a un alineamiento."),
            ("Matriz de sustitución", "Tabla de puntuaciones para reemplazos entre residuos."),
            ("Brecha afín", "Modelo con costes separados para apertura y extensión de una brecha."),
            ("Programación dinámica", "Método que resuelve un problema mediante subproblemas superpuestos."),
            ("Traceback", "Recorrido que reconstruye una solución desde la matriz de puntuación."),
            ("Alineamiento local", "Comparación centrada en segmentos de alta similitud."),
            ("E-value", "Número esperado de hits con score comparable bajo un modelo nulo."),
            ("Cobertura", "Fracción de una secuencia incluida en el alineamiento."),
            ("Homología", "Relación de descendencia desde un ancestro común."),
            ("Ortología", "Homología derivada de un evento de especiación."),
            ("Bootstrap filogenético", "Remuestreo de sitios para evaluar estabilidad de agrupamientos."),
        ],
        "examples": [
            {
                "title": "Hit corto con identidad alta",
                "scenario": "Una proteína de 500 aminoácidos tiene un hit con 95 % de identidad sobre 22 residuos.",
                "reasoning_steps": [
                    "Examinar cobertura de query y subject además de identidad.",
                    "Comprobar si el segmento corresponde a baja complejidad o motivo frecuente.",
                    "Evaluar E-value con la base y parámetros utilizados.",
                    "Buscar dominios y evidencia funcional independiente.",
                ],
                "interpretation": "La identidad local alta no justifica transferir la función de la proteína completa.",
                "limitations": ["Un motivo corto puede ser funcional.", "La ausencia de cobertura no descarta una relación de dominio."],
            },
            {
                "title": "Topología sensible al alineamiento",
                "scenario": "Dos alineadores producen árboles con posiciones distintas para un clado de interés.",
                "reasoning_steps": [
                    "Localizar columnas que cambian entre alineamientos.",
                    "Evaluar regiones ambiguas, gaps y composición.",
                    "Repetir inferencia con modelos de sustitución apropiados.",
                    "Reportar clados estables y dependientes del método.",
                ],
                "interpretation": "La discrepancia muestra incertidumbre de preprocesamiento que debe propagarse a la conclusión evolutiva.",
                "limitations": ["El bootstrap no corrige sesgo sistemático.", "Un conjunto taxonómico limitado puede distorsionar la topología."],
            },
        ],
        "biomedical": [
            ("Anotación de proteínas", "La transferencia funcional requiere cobertura, dominios y contexto evolutivo."),
            ("Diagnóstico molecular", "La similitud prioriza regiones, pero no clasifica variantes por sí sola."),
            ("Vigilancia genómica", "Árboles y clados dependen de muestreo, recombinación y calidad."),
            ("Diseño de dianas", "La conservación orienta hipótesis que requieren validación funcional y selectividad."),
        ],
        "sources": ["blast-help", "blast-paper", "ebi-alignments", "clustalo", "iqtree"],
    },
    {
        "slug": "genomica-mapeo-variantes",
        "sections": [
            section(
                "Lecturas, control de calidad y referencia",
                "la evaluación conjunta de señal, errores de secuenciación, preparación de biblioteca y adecuación de la referencia",
                "Las lecturas contienen bases, calidades y patrones derivados de la plataforma y la preparación. Adaptadores, sesgo de contenido, duplicación, contaminación y degradación alteran el conjunto observable. La referencia incluye ensamblaje, contigs, secuencias alternativas y archivos auxiliares que deben ser coherentes con la anotación.",
                "cobertura nominal y efectiva, distribución de profundidad, fracción duplicada y tasa de bases con calidad superior a un umbral declarado.",
                "inspeccionar reportes por muestra, controles negativos, composición y longitudes; comparar métricas antes y después de filtrar y verificar que la referencia y los índices comparten checksum y versión.",
                "que más profundidad no corrige sesgo de biblioteca, regiones no mapeables o referencia inadecuada; el filtrado puede eliminar señal real si se aplica sin considerar el diseño.",
                [
                    "Calidad de lectura y calidad de muestra son diferentes.",
                    "La referencia es una dependencia versionada del análisis.",
                    "Cobertura media puede ocultar regiones sin datos.",
                    "Filtrar requiere comparar señal retenida y perdida.",
                ],
                [eq("C=\\frac{NL}{G}", "Cobertura nominal aproximada para N lecturas de longitud L sobre un genoma de tamaño G; ignora sesgos y duplicados.")],
            ),
            section(
                "Mapeo, SAM/BAM/CRAM y ambigüedad",
                "la asignación de cada lectura a una o varias posiciones compatibles de una referencia",
                "Los mapeadores usan índices y heurísticas para encontrar candidatos, puntuar alineamientos y representar operaciones mediante CIGAR. SAM/BAM conserva coordenadas, flags, MAPQ, grupos de lectura y etiquetas; CRAM además depende explícitamente de una referencia para reconstruir el contenido.",
                "la calidad de mapeo como transformación logarítmica de la probabilidad estimada de asignación incorrecta, junto con tasas de mapeo único, multimapeo y discordancia de pares.",
                "verificar flags y orientaciones en regiones conocidas, inspeccionar lecturas en un visor, comparar mapeadores o parámetros y conservar lecturas no asignadas para evaluar contaminación o referencia incompleta.",
                "que MAPQ no está calibrado idénticamente entre herramientas; repeticiones, pseudogenes, variantes estructurales y secuencias alternativas producen ambigüedad real que no debe transformarse en certeza.",
                [
                    "CIGAR describe operaciones respecto de la referencia.",
                    "MAPQ es una estimación dependiente del mapeador.",
                    "Multimapeo representa ambigüedad biológica o técnica.",
                    "CRAM requiere conservar la referencia compatible.",
                ],
                [eq("MAPQ=-10\\log_{10}P(mapeo\\ incorrecto)", "Definición idealizada de calidad de mapeo; la calibración práctica depende de la herramienta.")],
            ),
            section(
                "Llamado y filtrado de variantes",
                "la comparación probabilística entre genotipos o estados somáticos compatibles con las bases observadas",
                "Los llamadores combinan calidad de base, calidad de mapeo, orientación, posición en lectura y modelo de ploidía. En germinal se estiman genotipos; en tumor se deben considerar pureza, contaminación normal, subclonalidad y cambios de número de copias.",
                "profundidad alélica, fracción de alelo variante, verosimilitudes de genotipo y métricas de precisión, sensibilidad y F1 contra un truth set apropiado.",
                "usar controles de muestra, replicados o materiales de referencia, separar calibración de evaluación, estratificar por tipo de variante y contexto genómico y confirmar variantes relevantes mediante un método ortogonal cuando el uso lo exige.",
                "que los umbrales modifican el equilibrio entre falsos positivos y falsos negativos; un filtro entrenado en una tecnología o población puede no generalizar a otra.",
                [
                    "El llamado de variantes es una inferencia probabilística.",
                    "VAF depende de pureza, ploidía y subclonalidad.",
                    "Truth sets deben corresponder al tipo de variante evaluado.",
                    "Sensibilidad y precisión cambian con el umbral.",
                ],
                [eq("VAF=\\frac{AD_{alt}}{AD_{ref}+AD_{alt}}", "Fracción observada de lecturas alternativas; no equivale directamente a frecuencia celular o germinal.")],
            ),
            section(
                "Anotación, priorización y límites clínicos",
                "la integración de consecuencia molecular, frecuencia poblacional, herencia, fenotipo y evidencia experimental",
                "La anotación asigna transcritos, consecuencias, frecuencias y predicciones, pero diferentes versiones pueden cambiar el efecto principal. La priorización combina filtros y modelos; la clasificación clínica exige marcos profesionales, revisión de evidencia y contexto del individuo.",
                "razones de verosimilitud, probabilidades posteriores o sistemas de evidencia que deben evitar sumar señales dependientes como si fueran observaciones independientes.",
                "comparar anotadores y transcritos, conservar evidencia a favor y en contra, revisar bases poblacionales y fenotípicas y documentar fecha, versión y criterios de clasificación.",
                "que una predicción in silico no demuestra patogenicidad, accionabilidad ni respuesta terapéutica; la reanálisis puede cambiar conclusiones cuando aparecen nuevas evidencias.",
                [
                    "La consecuencia depende del transcrito y la versión.",
                    "Frecuencia poblacional necesita ancestría y calidad contextualizadas.",
                    "Predicción computacional es una línea de evidencia.",
                    "Clasificación clínica requiere revisión multidimensional.",
                ],
                [eq("Odds_{post}=Odds_{pre}\\prod_i LR_i", "Actualización de odds con razones de verosimilitud independientes; la dependencia entre evidencias invalida una multiplicación ingenua.")],
            ),
        ],
        "glossary": [
            ("Lectura", "Secuencia observada producida por una plataforma de secuenciación."),
            ("Referencia", "Conjunto versionado de secuencias usado para comparación y coordenadas."),
            ("Cobertura", "Número o profundidad de observaciones sobre una región."),
            ("Duplicado", "Lectura o par compatible con una misma molécula o evento de amplificación."),
            ("MAPQ", "Estimación de confianza en la posición de mapeo."),
            ("CIGAR", "Cadena que resume operaciones del alineamiento respecto de la referencia."),
            ("Grupo de lectura", "Metadato que vincula lecturas con biblioteca, plataforma y muestra."),
            ("Genotipo", "Estado alélico inferido en un locus para una muestra."),
            ("VAF", "Fracción de lecturas que contienen el alelo alternativo."),
            ("Truth set", "Conjunto de variantes de referencia para evaluación."),
            ("Anotación de variante", "Asignación de consecuencias, frecuencias y evidencia a una variante."),
            ("Validación ortogonal", "Confirmación mediante un método con errores diferentes."),
        ],
        "examples": [
            {
                "title": "VAF baja en una muestra tumoral",
                "scenario": "Una variante somática aparece con VAF de 0,08 y profundidad 120 en un tumor con pureza incierta.",
                "reasoning_steps": [
                    "Inspeccionar conteos por orientación, posición y calidad.",
                    "Considerar pureza, número de copias y subclonalidad.",
                    "Comparar con normal pareado y artefactos recurrentes.",
                    "Confirmar con un método ortogonal si la decisión depende del hallazgo.",
                ],
                "interpretation": "La VAF observada es compatible con varios escenarios y no identifica por sí sola la fracción de células portadoras.",
                "limitations": ["La profundidad no garantiza independencia de moléculas.", "La pureza estimada también tiene incertidumbre."],
            },
            {
                "title": "Variante discordante entre referencias",
                "scenario": "Una coordenada produce consecuencias diferentes al anotarse sobre dos ensamblajes y transcritos.",
                "reasoning_steps": [
                    "Verificar alelos de referencia y orientación.",
                    "Documentar el método de conversión de coordenadas.",
                    "Comparar transcritos clínicamente relevantes y expresión tisular.",
                    "Conservar ambas representaciones y su procedencia.",
                ],
                "interpretation": "La variante no cambió, pero su representación y consecuencia dependen del sistema de referencia.",
                "limitations": ["Algunas regiones no convierten unívocamente.", "La relevancia del transcrito requiere evidencia adicional."],
            },
        ],
        "biomedical": [
            ("Medicina genómica", "La clasificación exige evidencia poblacional, funcional, fenotípica y profesional."),
            ("Oncología molecular", "Pureza, copias y subclonalidad modifican VAF y priorización."),
            ("Enfermedades raras", "Herencia y fenotipo complementan frecuencia y predicción."),
            ("Validación analítica", "Truth sets y métodos ortogonales cuantifican límites del pipeline."),
        ],
        "sources": ["fastqc", "hts-specs", "gatk", "giab", "acmg"],
    },
    {
        "slug": "transcriptomica-expresion-diferencial",
        "sections": [
            section(
                "Diseño experimental, conteos y unidad de replicación",
                "la separación entre unidades biológicas independientes, observaciones técnicas, covariables y contrastes preespecificados",
                "Una matriz de conteos resume fragmentos asignados a genes o transcritos, pero la inferencia depende del diseño que produjo esas columnas. Células, lecturas o réplicas técnicas de una misma muestra no reemplazan individuos o cultivos independientes cuando la intervención se aplicó a ese nivel.",
                "un modelo de diseño que incluye condición, lote y covariables, junto con potencia, tamaño de muestra y distribución de profundidad entre bibliotecas.",
                "aleatorizar cuando sea posible, balancear lotes, registrar exclusiones, inspeccionar metadatos y PCA y verificar que el contraste estadístico coincide con la pregunta biológica.",
                "que confusión perfecta entre condición y lote no puede corregirse computacionalmente; aumentar el número de lecturas no aumenta el número de réplicas independientes.",
                [
                    "La unidad experimental deriva del nivel de intervención.",
                    "Lecturas no son réplicas biológicas.",
                    "El contraste debe declararse antes de interpretar resultados.",
                    "Confusión de lote puede ser no identificable.",
                ],
                [eq("y_{gi}\\sim NB(\\mu_{gi},\\alpha_g)", "Modelo de conteos del gen g en muestra i mediante distribución binomial negativa con media y dispersión específicas.")],
            ),
            section(
                "Alineamiento, pseudoalineamiento y cuantificación",
                "la asignación de fragmentos a genoma, transcritos o clases de equivalencia con tratamiento explícito de multimapeo e isoformas",
                "El alineamiento genómico conserva coordenadas y uniones de splicing; la cuantificación transcriptómica puede usar índices y compatibilidad con transcritos. La elección depende de si la pregunta requiere descubrir uniones, inspeccionar variantes o estimar abundancias conocidas.",
                "conteos, TPM y abundancias corregidas por longitud efectiva, reconociendo que estas escalas responden a comparaciones distintas.",
                "usar transcriptoma y anotación compatibles, evaluar tasas de asignación y sesgos, comparar agregación a gen con inferencia a transcrito y realizar análisis de sensibilidad ante versiones alternativas.",
                "que genes homólogos, isoformas compartidas, fragmentos cortos y anotación incompleta limitan la identificabilidad; un valor preciso de abundancia puede esconder alta incertidumbre de asignación.",
                [
                    "Alineamiento y pseudoalineamiento conservan información diferente.",
                    "TPM no sustituye conteos en todos los modelos.",
                    "Longitud efectiva depende de biblioteca y fragmentos.",
                    "Isoformas pueden no ser identificables con lecturas cortas.",
                ],
                [eq("TPM_i=10^6\\frac{c_i/l_i}{\\sum_j c_j/l_j}", "Abundancia relativa corregida por longitud efectiva; no es un conteo bruto para modelos de muestreo.")],
            ),
            section(
                "Normalización y expresión diferencial",
                "la comparación de conteos bajo diferencias de profundidad, composición y dispersión entre genes y muestras",
                "La normalización estima factores de tamaño o escalas comparables sin asumir que todas las moléculas permanecen constantes. Los modelos binomiales negativos estiman dispersión y contrastes; el fold change expresa magnitud, mientras el valor p y el FDR se refieren a incertidumbre bajo un conjunto de hipótesis.",
                "una relación varianza-media sobredispersa, log2 fold change y ajuste de multiplicidad mediante procedimientos como Benjamini-Hochberg.",
                "examinar MA plots, dispersión, muestras influyentes, estabilidad de rankings y genes control; repetir con especificaciones razonables y validar resultados prioritarios por método independiente o cohorte externa.",
                "que significancia estadística no implica relevancia biológica o clínica; cambios globales de composición pueden violar supuestos de normalización y el filtrado posterior puede inflar evidencia.",
                [
                    "Normalización corrige escalas, no todo sesgo experimental.",
                    "Dispersión modela variabilidad adicional a Poisson.",
                    "Fold change y significancia describen dimensiones distintas.",
                    "FDR depende del conjunto de hipótesis evaluado.",
                ],
                [eq("Var(Y)=\\mu+\\alpha\\mu^2", "Relación varianza-media de una binomial negativa parametrizada por dispersión alpha.")],
            ),
            section(
                "Lotes, heterogeneidad y validación",
                "la descomposición de variación técnica, composición celular y estados biológicos dentro y entre muestras",
                "PCA y modelos de covariables ayudan a detectar estructura, pero no identifican automáticamente su causa. En tejido, una diferencia de expresión puede reflejar regulación dentro de un tipo celular o cambio en proporciones; single-cell reduce algunas mezclas y añade dropout, dobletes y dependencia jerárquica.",
                "un modelo lineal o generalizado con efectos de condición, lote y covariables, acompañado de análisis estratificados y métricas de generalización.",
                "visualizar metadatos sobre componentes, evaluar interacción entre lote y condición, usar deconvolución con referencias apropiadas y validar firmas en cohortes, plataformas y subgrupos independientes.",
                "que corregir demasiado puede eliminar biología real, mientras omitir variables deja confusión; clustering y pseudotiempo son construcciones analíticas, no tipos celulares inmutables ni linaje causal.",
                [
                    "PCA revela estructura sin asignar causalidad.",
                    "Composición y regulación pueden producir señales similares.",
                    "Corrección de lote requiere diseño identificable.",
                    "La validación externa prueba transportabilidad contextual.",
                ],
                [eq("g(\\mu_i)=\\beta_0+\\beta_1 Condicion_i+\\beta_2 Lote_i", "Esquema de modelo con condición y lote; requiere que los efectos sean estimables a partir del diseño.")],
            ),
        ],
        "glossary": [
            ("Unidad experimental", "Entidad independiente a la que se aplica una condición o intervención."),
            ("Conteo", "Número de fragmentos asignados a una característica."),
            ("Pseudoalineamiento", "Asignación a clases de transcritos compatibles sin alineamiento base a base completo."),
            ("Longitud efectiva", "Longitud ajustada por distribución de fragmentos y sesgos de cuantificación."),
            ("TPM", "Escala relativa de abundancia corregida por longitud y biblioteca."),
            ("Factor de tamaño", "Escala estimada para comparar conteos entre bibliotecas."),
            ("Dispersión", "Variabilidad extra respecto de un modelo Poisson."),
            ("Log2 fold change", "Logaritmo base dos de la razón de expresión entre condiciones."),
            ("FDR", "Proporción esperada de falsos descubrimientos entre resultados declarados."),
            ("Batch effect", "Variación sistemática asociada a procesamiento o contexto técnico."),
            ("Deconvolución", "Estimación de componentes celulares o moleculares mezclados."),
            ("Pseudorreplicación", "Tratamiento de observaciones dependientes como réplicas independientes."),
        ],
        "examples": [
            {
                "title": "Quinientas células no son quinientas réplicas",
                "scenario": "Se secuencian 500 células de cada uno de tres pacientes por grupo.",
                "reasoning_steps": [
                    "Identificar al paciente como unidad biológica independiente.",
                    "Modelar células anidadas o agregar evidencia por paciente.",
                    "Separar variación entre pacientes de variación entre células.",
                    "Validar subpoblaciones sin usar cada célula como n independiente.",
                ],
                "interpretation": "El número de células mejora resolución de estados, pero la inferencia poblacional depende principalmente de pacientes independientes.",
                "limitations": ["La agregación puede ocultar subpoblaciones raras.", "Los modelos jerárquicos requieren suficiente replicación superior."],
            },
            {
                "title": "Firma dominada por composición",
                "scenario": "Un tejido inflamado muestra aumento de genes inmunitarios y descenso de genes epiteliales.",
                "reasoning_steps": [
                    "Examinar marcadores de composición y metadatos histológicos.",
                    "Comparar bulk con referencia single-cell o deconvolución.",
                    "Separar cambio de proporción y regulación intrínseca.",
                    "Validar genes prioritarios en células o regiones específicas.",
                ],
                "interpretation": "La firma bulk es compatible con infiltración, regulación o ambas; no identifica el mecanismo sin evidencia adicional.",
                "limitations": ["Las referencias de deconvolución pueden no representar el tejido.", "Los marcadores también cambian con activación."],
            },
        ],
        "biomedical": [
            ("Biomarcadores", "Una firma necesita validación analítica, externa y clínica antes de uso."),
            ("Oncología", "Composición tumoral, pureza y lote condicionan perfiles de expresión."),
            ("Single-cell", "Clustering y trayectorias deben distinguirse de linaje y causalidad."),
            ("Farmacología", "Cambios de expresión pueden reflejar respuesta, toxicidad o composición."),
        ],
        "sources": ["encode-rna", "star", "salmon", "deseq2", "bioc-rnaseq"],
    },
    {
        "slug": "analisis-funcional-rutas-redes",
        "sections": [
            section(
                "Ontologías, anotación funcional y universo",
                "la organización de conceptos biológicos mediante términos relacionados y anotaciones con evidencia explícita",
                "Gene Ontology usa un grafo dirigido acíclico para representar procesos, funciones y componentes. Una entidad puede tener múltiples términos y las anotaciones se propagan según relaciones definidas, lo que produce dependencia entre categorías y sesgo hacia genes muy estudiados.",
                "frecuencias de anotación dentro de un universo de genes medidos y proporciones de cobertura por código de evidencia, especie y fecha.",
                "definir el universo a partir de genes realmente detectables, conservar versión y evidencia, inspeccionar términos muy generales y comprobar si los resultados dependen de retirar anotaciones inferidas electrónicamente.",
                "que una ontología organiza conocimiento y no demuestra actividad en la muestra; ausencia de anotación puede significar falta de estudio, no ausencia de función.",
                [
                    "Las ontologías representan relaciones entre conceptos.",
                    "El universo debe reflejar genes que podían ser seleccionados.",
                    "Códigos de evidencia modifican la confianza de anotación.",
                    "Sesgo de estudio afecta enriquecimientos funcionales.",
                ],
                [eq("f_t=\\frac{N_{anotados\\ a\\ t}}{N_{universo}}", "Frecuencia de un término t en el universo analizable; cambia con versión, especie y evidencia.")],
            ),
            section(
                "Sobre-representación y enriquecimiento por ranking",
                "la comparación entre genes seleccionados y un universo mediante pruebas discretas o estadísticas de listas ordenadas",
                "El análisis de sobre-representación usa una tabla de contingencia para preguntar si un término aparece más de lo esperado. Los métodos de ranking evitan un corte único y evalúan acumulación de genes de un conjunto en extremos de una lista ordenada.",
                "la distribución hipergeométrica para ORA, estadísticas de enriquecimiento acumulativo y corrección por múltiples términos dependientes.",
                "preespecificar universo y criterio de ranking, probar sensibilidad al umbral, usar permutaciones compatibles con la unidad experimental y comparar términos redundantes mediante estructura ontológica.",
                "que términos pequeños son inestables y términos grandes poco específicos; el valor p depende del universo y no mide tamaño de efecto, coherencia mecanística ni relevancia clínica.",
                [
                    "ORA depende del umbral y del universo.",
                    "Los métodos de ranking conservan información ordinal.",
                    "Términos ontológicos no son hipótesis independientes.",
                    "Significancia funcional no demuestra causalidad.",
                ],
                [eq("P(X\\ge k)=\\sum_{i=k}^{min(K,n)}\\frac{\\binom{K}{i}\\binom{N-K}{n-i}}{\\binom{N}{n}}", "Probabilidad hipergeométrica de observar al menos k genes del término en una lista de tamaño n.")],
            ),
            section(
                "Rutas, redes e interacción molecular",
                "la representación de entidades como nodos y relaciones experimentales, funcionales o predictivas como aristas tipadas",
                "Las rutas curadas organizan reacciones y regulación; las redes pueden combinar interacción física, coexpresión, texto y predicción. El significado de una arista debe conservarse, porque una puntuación integrada no equivale necesariamente a contacto molecular ni dirección causal.",
                "grado, componentes, caminos y medidas de centralidad calculadas sobre un grafo cuya construcción y densidad condicionan el resultado.",
                "comparar redes con y sin fuentes de evidencia, usar controles de grado, evaluar estabilidad de módulos y verificar relaciones prioritarias en bases primarias o experimentos.",
                "que genes muy estudiados acumulan aristas, centralidad no implica esencialidad terapéutica y una red estática puede ignorar tejido, tiempo, dosis y dirección.",
                [
                    "Cada arista necesita un significado y una fuente.",
                    "Centralidad depende de la construcción del grafo.",
                    "Redes integradas mezclan evidencias heterogéneas.",
                    "Módulos son hipótesis que requieren validación.",
                ],
                [eq("k_i=\\sum_j A_{ij}", "Grado del nodo i en una matriz de adyacencia A; no mide por sí solo importancia causal.")],
            ),
            section(
                "Integración, causalidad y comunicación",
                "la conversión de patrones funcionales en hipótesis mecanísticas falsables y proporcionales a la evidencia",
                "Integrar expresión, variantes, proteínas y fenotipos exige alinear identificadores, dirección de efecto, contexto y nivel de medición. Una convergencia entre capas aumenta plausibilidad, pero puede reflejar sesgos compartidos de anotación o selección.",
                "modelos de evidencia que separan tamaño de efecto, incertidumbre, replicación y coherencia entre fuentes, sin sumar resultados dependientes como observaciones nuevas.",
                "formular predicciones de perturbación, definir controles positivos y negativos, validar en cohortes o sistemas independientes y registrar resultados que contradicen la hipótesis.",
                "que una narrativa coherente puede ser retrospectiva y no predictiva; priorización de dianas requiere eficacia, selectividad, toxicidad, población y factibilidad más allá de la red.",
                [
                    "Integración requiere alinear contexto y dirección de efecto.",
                    "Convergencia de capas no elimina sesgos compartidos.",
                    "Una hipótesis útil produce predicciones de perturbación.",
                    "Priorizar una diana no demuestra utilidad terapéutica.",
                ],
                [eq("P(H\\mid D)\\propto P(D\\mid H)P(H)", "Actualización conceptual de una hipótesis H con datos D; exige declarar dependencias y priors.")],
            ),
        ],
        "glossary": [
            ("Ontología", "Sistema formal de conceptos y relaciones en un dominio."),
            ("Código de evidencia", "Etiqueta que describe el fundamento de una anotación."),
            ("Universo", "Conjunto de entidades que podían ser seleccionadas en el análisis."),
            ("ORA", "Análisis de sobre-representación de categorías en una lista seleccionada."),
            ("Hipergeométrica", "Distribución para muestreo sin reemplazo usada en ORA."),
            ("Enriquecimiento por ranking", "Prueba de acumulación de un conjunto a lo largo de una lista ordenada."),
            ("Ruta", "Conjunto curado de reacciones o relaciones biológicas contextualizadas."),
            ("Red", "Grafo de entidades y relaciones definidas."),
            ("Arista", "Relación tipada entre dos nodos."),
            ("Centralidad", "Familia de medidas estructurales de posición en una red."),
            ("Módulo", "Subconjunto de nodos con patrón de conectividad o función compartida."),
            ("Hipótesis falsable", "Proposición que genera observaciones capaces de refutarla."),
        ],
        "examples": [
            {
                "title": "Universo incorrecto en enriquecimiento",
                "scenario": "Se comparan 300 genes detectados contra todos los genes humanos, aunque el ensayo solo podía medir 8000.",
                "reasoning_steps": [
                    "Definir el conjunto de genes que superó filtros de detectabilidad.",
                    "Recalcular ORA con el universo analizable.",
                    "Comparar tamaño de efecto y términos que cambian.",
                    "Documentar versión de anotación y multiplicidad.",
                ],
                "interpretation": "Usar un universo demasiado amplio puede inflar enriquecimientos porque incluye genes que nunca podían aparecer en la lista.",
                "limitations": ["La detectabilidad también puede depender de condición.", "Los términos siguen siendo dependientes entre sí."],
            },
            {
                "title": "Diana central sin efecto terapéutico",
                "scenario": "Una proteína tiene alta centralidad en una red integrada y se propone como diana farmacológica.",
                "reasoning_steps": [
                    "Identificar qué tipos de arista generan la centralidad.",
                    "Controlar sesgo por grado y literatura.",
                    "Evaluar dirección causal y dependencia en modelos pertinentes.",
                    "Considerar selectividad, toxicidad y posibilidad de intervención.",
                ],
                "interpretation": "La centralidad prioriza una entidad para estudio, pero no demuestra eficacia, seguridad ni ventana terapéutica.",
                "limitations": ["La red puede omitir interacciones contextuales.", "La perturbación puede activar compensación."],
            },
        ],
        "biomedical": [
            ("Descubrimiento de mecanismos", "El enriquecimiento prioriza procesos que requieren perturbación experimental."),
            ("Biomarcadores", "Una firma funcional necesita validación externa y métricas predefinidas."),
            ("Drug discovery", "Las redes priorizan dianas sin demostrar eficacia ni seguridad."),
            ("Medicina de sistemas", "La integración debe conservar procedencia y significado de relaciones."),
        ],
        "sources": ["go-docs", "go-paper", "gsea", "reactome", "string"],
    },
    {
        "slug": "pipelines-pruebas-escalabilidad",
        "sections": [
            section(
                "Workflows como grafos de dependencias",
                "la descomposición de un análisis en tareas con entradas, salidas, dependencias y condiciones de ejecución explícitas",
                "Un workflow representa tareas como nodos y dependencias de datos como aristas. Esta estructura permite paralelizar tareas independientes, reanudar ejecuciones y evitar recomputación mediante caché, siempre que los artefactos y parámetros formen parte de la identidad de cada tarea.",
                "un grafo dirigido acíclico, tiempos por tarea, ruta crítica y tasas de reutilización de resultados que explican el rendimiento mejor que un tiempo total aislado.",
                "probar el DAG con datos mínimos, interrumpir y reanudar, modificar una entrada y verificar qué tareas se invalidan y comprobar que los nombres de canales no sustituyen contratos de tipo y contenido.",
                "que una dependencia implícita puede producir resultados obsoletos; el orden de finalización no debe alterar el resultado y los efectos laterales dificultan idempotencia y auditoría.",
                [
                    "Un workflow explicita tareas y dependencias de datos.",
                    "La caché requiere identidad completa de entradas y parámetros.",
                    "La ruta crítica limita el tiempo mínimo alcanzable.",
                    "Los efectos laterales reducen reproducibilidad.",
                ],
                [eq("T_{DAG}\\ge\\max_{p\\in caminos}\\sum_{i\\in p}t_i", "El tiempo del workflow no puede ser menor que la duración de su ruta crítica.")],
            ),
            section(
                "Entornos, contenedores y versiones",
                "la fijación de dependencias ejecutables, bibliotecas, imágenes, referencias y configuraciones",
                "Los gestores de entornos resuelven paquetes; los contenedores encapsulan sistemas de archivos y dependencias, pero comparten o interactúan con kernel, hardware y almacenamiento. Un tag mutable como latest no identifica una imagen; un digest y un lockfile aportan una referencia más estable.",
                "identificadores de imagen, checksums de referencia y matrices de compatibilidad entre versión de herramienta, formato y recurso de hardware.",
                "construir desde recetas versionadas, escanear dependencias, ejecutar smoke tests, registrar digest y comparar resultados en al menos dos entornos compatibles cuando la portabilidad sea relevante.",
                "que contenedores no garantizan determinismo ni seguridad absoluta; fuentes externas, paralelismo, bibliotecas numéricas y arquitectura pueden producir variación.",
                [
                    "Un tag mutable no fija una imagen.",
                    "Entorno y referencia son dependencias del resultado.",
                    "Contenedores mejoran portabilidad sin garantizar determinismo.",
                    "Las recetas deben ser auditables y reconstruibles.",
                ],
                [eq("I=(digest,versiones,referencias,parametros)", "Identidad conceptual de una ejecución reproducible; omitir un componente dificulta auditoría.")],
            ),
            section(
                "Pruebas, procedencia y control de calidad",
                "la verificación automática de funciones, integración, resultados de referencia y contratos de datos",
                "Las pruebas unitarias aíslan transformaciones; las de integración recorren varios pasos; las de regresión comparan resultados esperados. Los tests deben incluir errores conocidos y datos mínimos que permitan diagnóstico, no únicamente comprobar que el proceso termina sin excepción.",
                "tolerancias numéricas, tasas de aprobación, cobertura de casos y diferencias estructuradas entre artefactos de referencia y nuevos resultados.",
                "ejecutar tests en integración continua, validar esquemas y rangos, conservar logs y manifiestos, comprobar resultados negativos y usar procedencia para enlazar cada salida con código, entrada y entorno.",
                "que snapshots excesivamente rígidos bloquean mejoras y tolerancias amplias ocultan regresiones; un test refleja lo que fue especificado y no descubre automáticamente errores científicos no contemplados.",
                [
                    "Terminar sin error no demuestra corrección.",
                    "Pruebas unitarias e integración detectan fallos diferentes.",
                    "La procedencia conecta artefactos con decisiones reproducibles.",
                    "Los tests necesitan datos positivos, negativos y límites.",
                ],
                [eq("\\Delta=metric(resultado_nuevo,resultado_referencia)", "Diferencia de regresión que debe compararse con una tolerancia justificada por el método.")],
            ),
            section(
                "Escalabilidad, seguridad y entrega responsable",
                "la asignación eficiente de CPU, memoria, almacenamiento y red bajo restricciones de privacidad, coste y gobernanza",
                "El profiling identifica cuellos de botella antes de paralelizar. La escalabilidad puede limitarse por fracción serial, comunicación, I/O o memoria; en datos sensibles también importan identidad, permisos, cifrado, localización y auditoría de accesos.",
                "speedup, eficiencia paralela, memoria máxima, volumen de transferencia y coste por muestra o cohorte, acompañados de intervalos y carga de prueba representativa.",
                "comparar tamaños crecientes, medir uso real, imponer límites de recursos, probar fallos y reintentos, aplicar mínimo privilegio y revisar que artefactos, logs y cachés no expongan información sensible.",
                "que acelerar una etapa puede trasladar el cuello de botella; el cloud no elimina gobernanza y una salida agregada todavía puede permitir reidentificación o fuga de información.",
                [
                    "El profiling debe preceder a la optimización.",
                    "La fracción serial limita el speedup máximo.",
                    "Seguridad incluye datos, logs, cachés y resultados.",
                    "Escalabilidad debe evaluarse con cargas representativas.",
                ],
                [eq("S(N)=\\frac{1}{f+(1-f)/N}", "Ley de Amdahl para speedup con fracción serial f y N recursos, ignorando comunicación adicional.")],
            ),
        ],
        "glossary": [
            ("Workflow", "Definición ejecutable de tareas y dependencias de un análisis."),
            ("DAG", "Grafo dirigido acíclico usado para representar dependencias."),
            ("Ruta crítica", "Camino de tareas que limita la duración mínima del workflow."),
            ("Caché", "Reutilización de resultados previamente calculados bajo identidad compatible."),
            ("Idempotencia", "Propiedad por la que repetir una operación produce el mismo estado esperado."),
            ("Contenedor", "Entorno empaquetado con sistema de archivos y dependencias ejecutables."),
            ("Digest", "Identificador criptográfico del contenido de una imagen o archivo."),
            ("Lockfile", "Registro fijado de versiones y dependencias resueltas."),
            ("Prueba de regresión", "Comparación automática con resultados de referencia."),
            ("Procedencia", "Relación trazable entre entradas, tareas, agentes y salidas."),
            ("Profiling", "Medición del uso de tiempo y recursos para localizar cuellos de botella."),
            ("Speedup", "Razón entre tiempo de ejecución de referencia y tiempo paralelo."),
        ],
        "examples": [
            {
                "title": "Caché que reutiliza una referencia obsoleta",
                "scenario": "Un pipeline cambia el FASTA de referencia, pero una tarea no se invalida porque la referencia no forma parte de su firma.",
                "reasoning_steps": [
                    "Inspeccionar dependencias declaradas y artefactos consumidos.",
                    "Añadir referencia y checksum a la identidad de tarea.",
                    "Eliminar caché afectada y repetir el análisis.",
                    "Crear una prueba que detecte cambios de referencia.",
                ],
                "interpretation": "La caché era técnicamente funcional, pero su contrato incompleto produjo un resultado obsoleto.",
                "limitations": ["Invalidar toda la caché puede ser costoso.", "Algunas dependencias se introducen mediante variables externas."],
            },
            {
                "title": "Más núcleos sin aceleración",
                "scenario": "Una tarea tarda casi lo mismo con 8 y 32 núcleos y aumenta el uso de memoria.",
                "reasoning_steps": [
                    "Medir fracción serial, I/O y utilización de CPU.",
                    "Evaluar escalabilidad por tamaño de entrada.",
                    "Comparar paralelismo interno y paralelismo entre muestras.",
                    "Seleccionar recursos que minimicen tiempo y coste sin inestabilidad.",
                ],
                "interpretation": "El límite puede estar en I/O, memoria o fracción serial; solicitar más CPU no garantiza speedup.",
                "limitations": ["La carga del sistema compartido afecta mediciones.", "Un dataset pequeño puede no revelar escalabilidad útil."],
            },
        ],
        "biomedical": [
            ("Análisis ómico", "Workflows versionados permiten repetir cohortes y actualizar referencias controladamente."),
            ("Clinical AI", "Procedencia y pruebas ayudan a prevenir fuga de datos y detectar drift."),
            ("HPC biomédico", "Profiling y paralelismo deben justificarse por carga, memoria y coste."),
            ("Datos sensibles", "Acceso, cifrado, auditoría y retención forman parte del diseño."),
        ],
        "sources": ["nextflow", "nfcore", "apptainer", "w3c-prov", "rocrate"],
    },
]


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_unit(course: dict[str, Any], index: int, content: dict[str, Any]) -> dict[str, Any]:
    declared = course["detailed_units"][index - 1]
    sections = content["sections"]
    activity_problems: list[str] = []
    for item in sections:
        activity_problems.extend(
            [
                f"Construye un esquema reproducible para «{item['heading']}» e identifica entradas, transformaciones, controles y salidas.",
                f"Propón un análisis de sensibilidad para «{item['heading']}» y explica qué cambio invalidaría la conclusión principal.",
            ]
        )
    common_errors = [
        {
            "error": f"Interpretar «{item['heading']}» como una etiqueta sin declarar datos, modelo y controles.",
            "correction": item["key_points"][0],
        }
        for item in sections
    ]
    common_errors.append(
        {
            "error": "Convertir una salida algorítmica o estadística en una decisión clínica directa.",
            "correction": "Separar observación, inferencia, mecanismo, validación externa y utilidad clínica.",
        }
    )
    self_assessment: list[dict[str, str]] = []
    for item in sections:
        self_assessment.append(
            {
                "question": f"¿Qué principio central resume {item['heading']}?",
                "answer": item["key_points"][0],
            }
        )
    for item in sections:
        self_assessment.append(
            {
                "question": f"¿Qué limitación debe controlarse al estudiar {item['heading']}?",
                "answer": item["key_points"][-1],
            }
        )

    unit = {
        "schema_version": "2.0",
        "subject_id": "bioinformatica",
        "area_id": "ingenieria-biomedica",
        "unit": index,
        "slug": content["slug"],
        "title": declared["title"],
        "status": "review",
        "purpose": declared["description"],
        "learning_objectives": declared["learning_outcomes"],
        "theory_sections": sections,
        "glossary": [{"term": term, "definition": definition} for term, definition in content["glossary"]],
        "worked_examples": content["examples"],
        "guided_activities": [
            {
                "title": f"Práctica reproducible: {declared['title']}",
                "instructions": [
                    "Define la pregunta, la unidad de observación y el resultado que la evidencia puede sostener.",
                    "Construye un flujo con versiones, parámetros, controles y un conjunto mínimo de prueba.",
                    "Ejecuta al menos una comprobación cuantitativa y conserva el código o procedimiento necesario para repetirla.",
                    "Compara una explicación principal con una alternativa y especifica qué dato permitiría distinguirlas.",
                ],
                "problems": activity_problems,
                "checking_criteria": [
                    "Las entradas, referencias, versiones y transformaciones están declaradas.",
                    "Los cálculos y decisiones pueden reproducirse desde los artefactos entregados.",
                    "La conclusión es proporcional al diseño, los controles y la incertidumbre.",
                    "Se separan salida computacional, hipótesis biológica y posible utilidad biomédica.",
                ],
            }
        ],
        "common_errors": common_errors,
        "self_assessment": self_assessment,
        "biomedical_connections": [
            {"topic": topic, "connection": connection} for topic, connection in content["biomedical"]
        ],
        "sources": [dict(SOURCE_CATALOG[key]) for key in content["sources"]],
        "editorial_notice": EDITORIAL_NOTICE,
    }
    return unit


def validate_unit_locally(unit: dict[str, Any]) -> None:
    if len(unit["learning_objectives"]) < 5:
        raise ValueError("objetivos insuficientes")
    if len(unit["theory_sections"]) < 4:
        raise ValueError("secciones insuficientes")
    words = 0
    seen: set[str] = set()
    for section_data in unit["theory_sections"]:
        if len(section_data["paragraphs"]) < 3 or len(section_data["key_points"]) < 3:
            raise ValueError("densidad por sección insuficiente")
        for paragraph in section_data["paragraphs"]:
            count = len(WORD_RE.findall(paragraph))
            if count < 20:
                raise ValueError(f"párrafo demasiado breve: {count}")
            marker = " ".join(paragraph.casefold().split())
            if marker in seen:
                raise ValueError("párrafo duplicado")
            seen.add(marker)
            words += count
    if words < 750:
        raise ValueError(f"teoría insuficiente: {words}")
    if len(unit["glossary"]) < 12 or len(unit["worked_examples"]) < 2:
        raise ValueError("componentes pedagógicos insuficientes")
    if len(unit["common_errors"]) < 5 or len(unit["self_assessment"]) < 8:
        raise ValueError("evaluación insuficiente")
    if len(unit["sources"]) < 5:
        raise ValueError("fuentes insuficientes")
    activity = unit["guided_activities"][0]
    if sum(len(activity[key]) for key in ("instructions", "problems", "checking_criteria")) < 8:
        raise ValueError("actividad insuficiente")


def slugify(text: str) -> str:
    text = text.casefold()
    replacements = str.maketrans("áéíóúüñ", "aeiouun")
    text = text.translate(replacements)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def collect_sources(subject_id: str) -> list[dict[str, Any]]:
    units_dir = REDEVELOPMENT_ROOT / subject_id / "units"
    unique: dict[str, dict[str, Any]] = {}
    for unit_path in sorted(units_dir.glob("unit-*.json")):
        unit = json.loads(unit_path.read_text(encoding="utf-8"))
        for source in unit.get("sources", []):
            locator = str(source.get("doi") or source.get("pmid") or source.get("isbn") or source.get("url") or source.get("title"))
            if locator not in unique:
                item = dict(source)
                item["id"] = f"{slugify(str(source.get('title') or 'source'))}-{len(unique)+1:02d}"
                unique[locator] = item
    return list(unique.values())


def build_registry(subject_id: str, course: dict[str, Any]) -> None:
    write_json(
        SOURCE_REGISTRY_ROOT / f"{subject_id}.json",
        {
            "schema_version": "1.0",
            "subject_id": subject_id,
            "last_reviewed": "2026-07-27",
            "purpose": f"Registro consolidado de fuentes curriculares y metodológicas para {course['title']}.",
            "sources": collect_sources(subject_id),
        },
    )


def build_decision(subject_id: str, course: dict[str, Any]) -> None:
    write_json(
        DECISION_ROOT / f"{subject_id}.json",
        {
            "schema_version": "1.0",
            "subject_id": subject_id,
            "decision_date": "2026-07-27",
            "status": "approved_for_redevelopment",
            "academic_level": course["level"],
            "decision": {
                "selected_unit_count": len(course["detailed_units"]),
                "delivery_model": "aprendizaje autogestionado organizado por resultados y artefactos reproducibles",
                "rationale": (
                    f"La arquitectura de {len(course['detailed_units'])} unidades preserva la progresión declarada "
                    "en el curso, separa dominios metodológicos y permite validar cada unidad sin imponer una duración estándar."
                ),
                "source_registry": f"data/source_registry/{subject_id}.json",
            },
            "scope": {
                "included": [item["title"] for item in course["detailed_units"]],
                "transversal": [
                    "reproducibilidad y procedencia",
                    "control de calidad",
                    "análisis cuantitativo",
                    "validación y límites de inferencia",
                ],
                "excluded_or_redirected": [
                    {
                        "topic": "uso clínico individual o decisión terapéutica",
                        "destination": "programas clínicos, validación regulatoria y supervisión profesional",
                    }
                ],
            },
            "units": [
                {
                    "unit": item["unit"],
                    "title": item["title"],
                    "central_question": item["description"],
                    "domains": item["topics"],
                }
                for item in course["detailed_units"]
            ],
            "external_review": {
                "status": "pending",
                "note": "La integridad técnica no sustituye revisión disciplinar externa.",
            },
        },
    )


def write_review_files(subject_id: str, course: dict[str, Any]) -> None:
    review_path = REVIEW_ROOT / subject_id / "REVIEW_STATUS.md"
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(
        "\n".join(
            [
                f"# Estado de revisión — {course['title']}",
                "",
                "- Estado editorial: `review`.",
                "- Integridad técnica: pendiente de confirmación por CI después de publicación.",
                "- Revisión disciplinar externa: pendiente.",
                "- Acreditación o validación clínica: no aplica.",
                "",
                "El curso no debe cambiar a `complete` hasta documentar revisión humana externa y resolver sus observaciones.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    audit_path = AUDIT_ROOT / subject_id / "AUDIT_2026-07-27.md"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(
        "\n".join(
            [
                f"# Auditoría técnica inicial — {course['title']}",
                "",
                f"- Unidades declaradas: {len(course['detailed_units'])}.",
                "- Fuente canónica: `data/course_redevelopment`.",
                "- Estado esperado: `review`.",
                "- Publicación y alineación: deben ser confirmadas por los workflows del repositorio.",
                "- Revisión externa: pendiente; no se afirma madurez académica completa.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_from_partial_recovery() -> None:
    source = PARTIAL_ROOT / "course_redevelopment"
    if not source.exists():
        raise FileNotFoundError("No existe la recuperación parcial de course_redevelopment")
    shutil.copytree(source, REDEVELOPMENT_ROOT, dirs_exist_ok=True)

    bio_course_path = REDEVELOPMENT_ROOT / "bioinformatica" / "course.json"
    bio_course = json.loads(bio_course_path.read_text(encoding="utf-8"))
    if len(UNIT_CONTENT) != len(bio_course["detailed_units"]):
        raise ValueError("La arquitectura de Bioinformática no coincide con el constructor")
    units_dir = bio_course_path.parent / "units"
    units_dir.mkdir(parents=True, exist_ok=True)
    for index, content in enumerate(UNIT_CONTENT, start=1):
        unit = build_unit(bio_course, index, content)
        validate_unit_locally(unit)
        write_json(units_dir / f"unit-{index:02d}.json", unit)

    for subject_id in ("fisiologia-humana-i", "bioinformatica"):
        course_path = REDEVELOPMENT_ROOT / subject_id / "course.json"
        course = json.loads(course_path.read_text(encoding="utf-8"))
        build_registry(subject_id, course)
        build_decision(subject_id, course)
        write_review_files(subject_id, course)

    print("[ok] recuperación parcial copiada")
    print("[ok] seis unidades de Bioinformática reconstruidas")
    print("[ok] registros de fuentes, decisiones y estado de revisión generados")


def main() -> int:
    build_from_partial_recovery()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
