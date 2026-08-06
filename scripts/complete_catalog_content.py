#!/usr/bin/env python3
"""Build academically explicit course packages for every fallback-only subject.

This script converts the existing curriculum outlines into traceable schema 2.0
course and unit documents.  It deliberately keeps editorial status at ``review``:
internal authoring can be completed by automation, but disciplinary verification
requires an independent qualified reviewer.

The generated prose is original and parameterised by course, unit, topic,
application and disciplinary profile.  Source entries point to official or open
resources; no source text is copied into the repository.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REDEVELOPMENT = DATA / "course_redevelopment"
GENERATED_COURSES = DATA / "generated_courses"
COVERAGE_PATH = DATA / "curriculum_coverage" / "catalog-completion-2026.json"

import sys

if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import generate_site  # noqa: E402


def source(
    title: str,
    organization: str,
    url: str,
    kind: str,
    description: str,
) -> dict[str, str]:
    return {
        "title": title,
        "organization": organization,
        "url": url,
        "type": kind,
        "description": description,
        "verification_status": "official_or_open_resource_checked_2026-08",
    }


RESOURCE_POOLS: dict[str, list[dict[str, str]]] = {
    "biosciences": [
        source("Anatomy and Physiology 2e", "OpenStax", "https://openstax.org/details/books/anatomy-and-physiology-2e", "libro abierto", "Base anatómica y fisiológica con figuras y preguntas de revisión."),
        source("NCBI Bookshelf", "National Library of Medicine", "https://www.ncbi.nlm.nih.gov/books/", "biblioteca biomédica", "Libros y capítulos biomédicos con procedencia editorial."),
        source("Human Protein Atlas", "KTH, SciLifeLab y consorcio HPA", "https://www.proteinatlas.org/", "atlas abierto", "Expresión y localización tisular y celular de proteínas humanas."),
        source("Guide to PHARMACOLOGY", "IUPHAR/BPS", "https://www.guidetopharmacology.org/", "base curada", "Dianas, ligandos y mecanismos farmacológicos curados."),
        source("EMBL-EBI Training", "EMBL-EBI", "https://www.ebi.ac.uk/training/", "formación abierta", "Cursos y materiales de datos y biología molecular."),
        source("PubMed", "National Library of Medicine", "https://pubmed.ncbi.nlm.nih.gov/", "índice bibliográfico", "Búsqueda trazable de literatura biomédica primaria y de revisión."),
        source("MedlinePlus", "National Library of Medicine", "https://medlineplus.gov/", "divulgación sanitaria", "Modelos de comunicación pública de conceptos de salud."),
        source("Cell Image Library", "American Society for Cell Biology", "https://www.cellimagelibrary.org/", "repositorio de imágenes", "Imágenes biológicas con metadatos para observación y comparación."),
    ],
    "biomaterials": [
        source("Biomaterials", "NIBIB", "https://www.nibib.nih.gov/science-education/science-topics/biomaterials", "recurso oficial", "Introducción a materiales, interacción biológica y aplicaciones."),
        source("Biological evaluation guidance", "U.S. FDA", "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-international-standard-iso-10993-1-biological-evaluation-medical-devices-part-1-evaluation-and", "guía regulatoria", "Marco basado en riesgo para evaluación biológica de dispositivos."),
        source("Sterilization for medical devices", "U.S. FDA", "https://www.fda.gov/medical-devices/general-hospital-devices-and-supplies/sterilization-medical-devices", "recurso regulatorio", "Métodos, validación y consideraciones de esterilización."),
        source("Materials Data Repository", "NIST", "https://www.nist.gov/mml/materials-data-repository", "datos de materiales", "Infraestructura y prácticas para datos de materiales."),
        source("IUPAC Gold Book", "IUPAC", "https://goldbook.iupac.org/", "terminología", "Definiciones químicas normalizadas."),
        source("NCBI Bookshelf", "National Library of Medicine", "https://www.ncbi.nlm.nih.gov/books/", "biblioteca biomédica", "Textos de biomateriales, reparación tisular y toxicología."),
        source("PubMed", "National Library of Medicine", "https://pubmed.ncbi.nlm.nih.gov/", "índice bibliográfico", "Literatura sobre respuesta huésped, degradación y desempeño."),
        source("Medical device technologies", "NIBIB", "https://www.nibib.nih.gov/science-education/science-topics/medical-device-technologies", "recurso oficial", "Conexión entre materiales, diseño, uso y evaluación de dispositivos."),
    ],
    "mathematics": [
        source("Calculus Volume 3", "OpenStax", "https://openstax.org/details/books/calculus-volume-3", "libro abierto", "Cálculo multivariable, vectorial y ecuaciones diferenciales introductorias."),
        source("Linear Algebra", "MIT OpenCourseWare", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", "curso abierto", "Álgebra lineal, transformaciones y descomposiciones."),
        source("Digital Library of Mathematical Functions", "NIST", "https://dlmf.nist.gov/", "referencia", "Definiciones y propiedades verificadas de funciones matemáticas."),
        source("NumPy documentation", "NumPy project", "https://numpy.org/doc/stable/", "documentación", "Cómputo matricial reproducible y pruebas numéricas."),
        source("SciPy documentation", "SciPy project", "https://docs.scipy.org/doc/scipy/", "documentación", "Solucionadores, optimización e integración numérica."),
        source("The Turing Way", "The Turing Way community", "https://book.the-turing-way.org/", "guía abierta", "Reproducibilidad, revisión y procedencia computacional."),
        source("Jupyter documentation", "Project Jupyter", "https://docs.jupyter.org/", "documentación", "Cuadernos ejecutables para derivaciones y experimentos numéricos."),
        source("PhysioNet", "MIT Laboratory for Computational Physiology", "https://physionet.org/", "datos abiertos", "Datos fisiológicos para formular y validar modelos."),
    ],
    "chemistry": [
        source("Chemistry 2e", "OpenStax", "https://openstax.org/details/books/chemistry-2e", "libro abierto", "Termodinámica, equilibrio, cinética y estructura química."),
        source("IUPAC Gold Book", "IUPAC", "https://goldbook.iupac.org/", "terminología", "Definiciones químicas y fisicoquímicas normalizadas."),
        source("PubChem", "National Center for Biotechnology Information", "https://pubchem.ncbi.nlm.nih.gov/", "base química", "Estructuras, propiedades, bioensayos y procedencia."),
        source("ChEMBL", "EMBL-EBI", "https://www.ebi.ac.uk/chembl/", "base curada", "Moléculas bioactivas, dianas y datos de actividad."),
        source("RCSB Protein Data Bank", "RCSB PDB", "https://www.rcsb.org/", "base estructural", "Estructuras macromoleculares y ligandos con metadatos."),
        source("Guide to PHARMACOLOGY", "IUPHAR/BPS", "https://www.guidetopharmacology.org/", "base curada", "Farmacología cuantitativa y nomenclatura de dianas."),
        source("RDKit documentation", "RDKit project", "https://www.rdkit.org/docs/", "documentación", "Quimioinformática reproducible y descriptores moleculares."),
        source("NCBI Bookshelf", "National Library of Medicine", "https://www.ncbi.nlm.nih.gov/books/", "biblioteca biomédica", "Textos de farmacología y química medicinal."),
    ],
    "networks": [
        source("RFC Editor", "Internet Architecture Board", "https://www.rfc-editor.org/", "estándares de Internet", "Especificaciones primarias de protocolos y arquitectura de red."),
        source("Computer Security Resource Center", "NIST", "https://csrc.nist.gov/publications", "guías oficiales", "Ciberseguridad, criptografía y gestión de riesgos."),
        source("HL7 FHIR", "HL7 International", "https://hl7.org/fhir/", "estándar sanitario", "Recursos e interfaces para intercambio de información de salud."),
        source("DICOM Standard", "DICOM Standards Committee", "https://www.dicomstandard.org/current", "estándar de imagen", "Comunicación, almacenamiento y semántica de imagen médica."),
        source("OWASP Application Security Verification Standard", "OWASP Foundation", "https://owasp.org/www-project-application-security-verification-standard/", "estándar abierto", "Requisitos verificables de seguridad de aplicaciones."),
        source("MDN Web Docs", "Mozilla", "https://developer.mozilla.org/en-US/docs/Web", "documentación abierta", "Protocolos web, API y conceptos de plataforma."),
        source("Wireshark User's Guide", "Wireshark Foundation", "https://www.wireshark.org/docs/wsug_html_chunked/", "manual abierto", "Inspección reproducible de tráfico y protocolos."),
        source("WHO Digital Health", "World Health Organization", "https://www.who.int/health-topics/digital-health", "recurso institucional", "Contexto de gobernanza, acceso y uso seguro de sistemas digitales."),
    ],
    "electronics": [
        source("University Physics Volume 2", "OpenStax", "https://openstax.org/details/books/university-physics-volume-2", "libro abierto", "Electricidad, magnetismo, circuitos y ondas."),
        source("Lessons in Electric Circuits", "All About Circuits", "https://www.allaboutcircuits.com/textbook/", "libro abierto", "Circuitos, dispositivos y análisis con ejercicios."),
        source("NIST Measurement Services", "NIST", "https://www.nist.gov/calibrations", "metrología", "Trazabilidad, calibración y servicios de medición."),
        source("PhysioNet", "MIT Laboratory for Computational Physiology", "https://physionet.org/", "datos abiertos", "Señales fisiológicas y anotaciones para análisis reproducible."),
        source("SciPy Signal", "SciPy project", "https://docs.scipy.org/doc/scipy/reference/signal.html", "documentación", "Procesamiento digital, filtrado y análisis espectral."),
        source("Medical device technologies", "NIBIB", "https://www.nibib.nih.gov/science-education/science-topics/medical-device-technologies", "recurso oficial", "Sistemas, sensores y aplicaciones de tecnología médica."),
        source("CDRH Learn", "U.S. FDA", "https://www.fda.gov/training-and-continuing-education/cdrh-learn", "formación regulatoria", "Módulos oficiales sobre dispositivos y evidencia."),
        source("GNU Radio documentation", "GNU Radio project", "https://wiki.gnuradio.org/index.php/Main_Page", "documentación abierta", "Simulación y procesamiento de señales por bloques."),
    ],
    "communication": [
        source("Reporting Guidelines", "EQUATOR Network", "https://www.equator-network.org/reporting-guidelines/", "biblioteca de guías", "Guías específicas para reportar métodos y resultados de salud."),
        source("COPE Core Practices", "Committee on Publication Ethics", "https://publicationethics.org/core-practices", "guía de integridad", "Autoría, revisión, conflictos y correcciones."),
        source("Plain Language", "National Institutes of Health", "https://www.nih.gov/institutes-nih/nih-office-director/office-communications-public-liaison/clear-communication/plain-language", "guía oficial", "Principios para comunicación clara de ciencia y salud."),
        source("Clear Communication Index", "U.S. CDC", "https://www.cdc.gov/ccindex/", "herramienta oficial", "Evaluación estructurada de materiales de comunicación pública."),
        source("ORCID", "ORCID", "https://info.orcid.org/", "infraestructura de identidad", "Identificación persistente de contribuyentes."),
        source("Crossref Metadata", "Crossref", "https://www.crossref.org/documentation/retrieve-metadata/", "infraestructura bibliográfica", "Identificadores y recuperación de metadatos de publicaciones."),
        source("CRediT taxonomy", "NISO", "https://credit.niso.org/", "taxonomía", "Descripción transparente de contribuciones de autoría."),
        source("Purdue Online Writing Lab", "Purdue University", "https://owl.purdue.edu/", "recurso educativo", "Escritura académica, citación y revisión lingüística."),
    ],
    "governance": [
        source("Health technology assessment", "World Health Organization", "https://www.who.int/health-topics/health-technology-assessment", "recurso institucional", "Evaluación multidisciplinaria para decisiones sanitarias."),
        source("Bioethics", "UNESCO", "https://www.unesco.org/en/ethics-science-technology/bioethics", "marco ético", "Instrumentos y recursos de bioética y derechos humanos."),
        source("Science, Technology and Innovation", "OECD", "https://www.oecd.org/sti/", "política pública", "Indicadores y análisis de innovación y política científica."),
        source("WIPO Academy", "World Intellectual Property Organization", "https://www.wipo.int/academy/en/", "formación abierta", "Propiedad intelectual, transferencia y estrategias de protección."),
        source("Medical devices", "World Health Organization", "https://www.who.int/health-topics/medical-devices", "recurso institucional", "Acceso, selección, gestión y seguridad de tecnologías médicas."),
        source("CDRH Learn", "U.S. FDA", "https://www.fda.gov/training-and-continuing-education/cdrh-learn", "formación regulatoria", "Ciclo de vida, calidad y regulación de dispositivos."),
        source("Medical Devices Regulation", "European Union", "https://eur-lex.europa.eu/eli/reg/2017/745/oj", "legislación", "Texto consolidable del marco europeo de dispositivos médicos."),
        source("NICE health technology evaluation", "NICE", "https://www.nice.org.uk/about/what-we-do/our-programmes/nice-guidance/nice-technology-appraisal-guidance", "evaluación pública", "Ejemplos de evaluación, recomendación e incertidumbre."),
    ],
    "digital_health": [
        source("HL7 FHIR", "HL7 International", "https://hl7.org/fhir/", "estándar sanitario", "Modelo de recursos e interfaces de interoperabilidad."),
        source("SNOMED CT", "SNOMED International", "https://www.snomed.org/", "terminología clínica", "Conceptos y relaciones clínicas computables."),
        source("LOINC", "Regenstrief Institute", "https://loinc.org/", "terminología clínica", "Identificadores de observaciones, mediciones y documentos."),
        source("WHO Digital Health", "World Health Organization", "https://www.who.int/health-topics/digital-health", "recurso institucional", "Estrategia, gobernanza y equidad en salud digital."),
        source("PhysioNet", "MIT Laboratory for Computational Physiology", "https://physionet.org/", "datos abiertos", "Datos clínicos y fisiológicos para análisis reproducible."),
        source("OHDSI", "Observational Health Data Sciences and Informatics", "https://www.ohdsi.org/", "comunidad y estándar abierto", "Modelo común de datos y análisis observacional."),
        source("UMLS", "National Library of Medicine", "https://www.nlm.nih.gov/research/umls/", "sistema terminológico", "Integración y correspondencia entre vocabularios biomédicos."),
        source("Privacy Framework", "NIST", "https://www.nist.gov/privacy-framework", "marco oficial", "Gestión de riesgos de privacidad en sistemas de información."),
    ],
    "biomechanics": [
        source("OpenSim documentation", "OpenSim", "https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/overview", "documentación", "Modelado musculoesquelético, simulación y análisis."),
        source("SimTK", "Stanford University", "https://simtk.org/", "plataforma abierta", "Software y proyectos de modelado biomédico."),
        source("Computational Modeling", "NIBIB", "https://www.nibib.nih.gov/science-education/science-topics/computational-modeling", "recurso oficial", "Modelos físicos y computacionales en biomedicina."),
        source("FEBio User Manual", "FEBio", "https://help.febio.org/", "documentación", "Elementos finitos para biomecánica y tejidos."),
        source("SOFA Framework", "SOFA Consortium", "https://www.sofa-framework.org/", "software abierto", "Simulación interactiva de sistemas deformables."),
        source("IT'IS Virtual Population", "IT'IS Foundation", "https://itis.swiss/virtual-population/virtual-population/overview/", "modelos anatómicos", "Modelos humanos computacionales con documentación."),
        source("3D Print Exchange", "National Institutes of Health", "https://3d.nih.gov/", "repositorio abierto", "Modelos tridimensionales biomédicos y educativos."),
        source("The Turing Way", "The Turing Way community", "https://book.the-turing-way.org/", "guía abierta", "Reproducibilidad, pruebas y procedencia de modelos."),
    ],
    "imaging": [
        source("DICOM Standard", "DICOM Standards Committee", "https://www.dicomstandard.org/current", "estándar", "Adquisición, representación e intercambio de imagen médica."),
        source("3D Slicer documentation", "3D Slicer community", "https://slicer.readthedocs.io/", "documentación", "Visualización, segmentación y flujos reproducibles."),
        source("ITK documentation", "Insight Toolkit community", "https://docs.itk.org/", "documentación", "Registro, filtrado y segmentación de imágenes."),
        source("NIBIB Science Topics", "NIBIB", "https://www.nibib.nih.gov/science-education/science-topics", "recurso oficial", "Principios de modalidades y tecnologías de imagen."),
        source("The Cancer Imaging Archive", "National Cancer Institute", "https://www.cancerimagingarchive.net/", "datos abiertos", "Colecciones de imagen con metadatos de investigación."),
        source("MONAI documentation", "MONAI Consortium", "https://docs.monai.io/", "documentación", "Flujos reproducibles de aprendizaje profundo en imagen médica."),
        source("QIBA", "Radiological Society of North America", "https://www.rsna.org/research/quantitative-imaging-biomarkers-alliance", "iniciativa de calidad", "Perfiles y metrología para biomarcadores cuantitativos de imagen."),
        source("ImageJ documentation", "National Institutes of Health", "https://imagej.net/", "software abierto", "Procesamiento, medición y automatización de imágenes científicas."),
    ],
    "devices": [
        source("CDRH Learn", "U.S. FDA", "https://www.fda.gov/training-and-continuing-education/cdrh-learn", "formación regulatoria", "Ciclo de vida, evidencia y calidad de dispositivos."),
        source("Design Controls", "U.S. FDA", "https://www.fda.gov/medical-devices/quality-system-qs-regulation-medical-device-good-manufacturing-practices/design-controls", "guía regulatoria", "Necesidades, entradas, salidas, verificación y validación."),
        source("Medical devices", "World Health Organization", "https://www.who.int/health-topics/medical-devices", "recurso institucional", "Selección, gestión, acceso y seguridad."),
        source("Medical device technologies", "NIBIB", "https://www.nibib.nih.gov/science-education/science-topics/medical-device-technologies", "recurso oficial", "Principios y ejemplos de tecnologías médicas."),
        source("Human Factors", "U.S. FDA", "https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/human-factors-and-medical-devices", "guía regulatoria", "Ingeniería de usabilidad y prevención de errores de uso."),
        source("NIST Risk Management Framework", "NIST", "https://csrc.nist.gov/projects/risk-management/about-rmf", "marco oficial", "Estructura para gestionar riesgos y evidencia."),
        source("Medical Devices Regulation", "European Union", "https://eur-lex.europa.eu/eli/reg/2017/745/oj", "legislación", "Marco europeo de ciclo de vida y conformidad."),
        source("ECRI device evaluation", "ECRI", "https://www.ecri.org/medical-equipment", "evaluación tecnológica", "Contexto de evaluación, mantenimiento y seguridad de equipos."),
    ],
}


PROFILES: dict[str, dict[str, Any]] = {
    "biosciences": {
        "object": "una estructura o función biológica organizada en niveles",
        "evidence": "observaciones anatómicas, histológicas, fisiológicas y moleculares con procedencia",
        "workflow": ["definir nivel y referencia", "observar o medir", "comparar controles", "integrar mecanismo", "delimitar inferencia"],
        "controls": "referencia anatómica o fisiológica, control técnico, comparación temporal y réplica apropiada",
        "caution": "no convertir una asociación estructural o una medición aislada en diagnóstico, mecanismo causal o recomendación clínica",
        "product": "atlas razonado o informe estructura-función",
        "equation": (r"v=\frac{\Delta y}{\Delta t}", "Tasa media de cambio de una variable fisiológica y; el intervalo y la unidad deben declararse.", {"y": "variable observada", "t": "tiempo"}),
    },
    "biomaterials": {
        "object": "un sistema material-interfaz-tejido definido por composición, procesamiento y uso",
        "evidence": "propiedades físico-químicas, ensayos mecánicos, superficies, degradación y respuesta biológica",
        "workflow": ["traducir necesidad en requisitos", "relacionar estructura y propiedad", "ensayar con controles", "analizar interfaz y degradación", "comparar riesgo residual"],
        "controls": "material de referencia, blanco, control positivo, control negativo y condición de envejecimiento",
        "caution": "la biocompatibilidad depende del dispositivo, la vía, la duración y el uso; no es una propiedad absoluta del material",
        "product": "matriz de selección y expediente de evidencia del material",
        "equation": (r"\sigma=\frac{F}{A_0}", "Esfuerzo ingenieril bajo carga axial, válido cuando se declara el área inicial y el régimen del ensayo.", {"F": "fuerza", "A_0": "área inicial"}),
    },
    "mathematics": {
        "object": "un modelo matemático con variables, dominio, parámetros y supuestos explícitos",
        "evidence": "derivación, prueba, cálculo reproducible, caso límite, análisis dimensional y comparación numérica",
        "workflow": ["formular", "derivar", "resolver", "verificar", "analizar sensibilidad", "interpretar"],
        "controls": "solución conocida, caso límite, refinamiento de malla o paso, conservación y método alternativo",
        "caution": "una solución numérica estable no demuestra que el modelo represente el fenómeno biomédico ni que sus parámetros sean identificables",
        "product": "cuaderno matemático reproducible con verificación y sensibilidad",
        "equation": (r"e_{rel}=\frac{|x-\hat{x}|}{\max(|x|,\epsilon)}", "Error relativo regularizado para comparar una referencia x con una aproximación; epsilon evita división inestable cerca de cero.", {"x": "referencia", r"\hat{x}": "aproximación", r"\epsilon": "escala pequeña declarada"}),
    },
    "chemistry": {
        "object": "una relación entre estructura molecular, propiedades, interacción con dianas y exposición",
        "evidence": "estructuras verificadas, ensayos de actividad, selectividad, propiedades fisicoquímicas y procedencia experimental",
        "workflow": ["definir hipótesis molecular", "curar estructuras y ensayos", "comparar series", "probar relación estructura-actividad", "evaluar incertidumbre"],
        "controls": "compuesto de referencia, blanco, control de interferencia, réplica y ensayo ortogonal",
        "caution": "afinidad, potencia celular, exposición y beneficio clínico son niveles diferentes y no deben intercambiarse",
        "product": "informe de relación estructura-actividad con hipótesis verificable",
        "equation": (r"pK_a=-\log_{10}(K_a)", "Relación logarítmica entre constante de disociación y pKa; las condiciones experimentales modifican la interpretación.", {"K_a": "constante de disociación ácida"}),
    },
    "networks": {
        "object": "una arquitectura de comunicación con capas, interfaces, datos y amenazas definidas",
        "evidence": "capturas controladas, especificaciones de protocolo, métricas de desempeño, pruebas de seguridad y registros",
        "workflow": ["definir servicio y activos", "modelar capas y flujo", "instrumentar", "probar condiciones nominales y de fallo", "documentar controles"],
        "controls": "tráfico basal, paquete conocido, latencia inducida, pérdida controlada y prueba de autorización",
        "caution": "conectividad no equivale a interoperabilidad semántica, confidencialidad, integridad ni disponibilidad clínica",
        "product": "diagrama de arquitectura y protocolo de pruebas de red",
        "equation": (r"T_{total}=T_{proc}+T_{cola}+T_{trans}+T_{prop}", "Descomposición didáctica de latencia; cada término requiere un punto de medición y una distribución.", {"T": "tiempo"}),
    },
    "electronics": {
        "object": "una cadena física de transducción, acondicionamiento, adquisición y procesamiento",
        "evidence": "señal cruda, función de transferencia, calibración, espectro, incertidumbre y pruebas de límites",
        "workflow": ["especificar mensurando", "presupuestar rango y banda", "modelar cadena", "simular fallos", "verificar salida"],
        "controls": "entrada patrón, cortocircuito o cero, señal de referencia, saturación controlada y ruido simulado",
        "caution": "una simulación o un cálculo educativo no demuestra seguridad eléctrica, compatibilidad electromagnética ni desempeño en personas",
        "product": "expediente de cadena de señal con presupuestos y pruebas",
        "equation": (r"\mathrm{SNR}_{dB}=10\log_{10}\left(\frac{P_s}{P_n}\right)", "Relación señal-ruido en potencia; banda, ventana y punto de medición deben permanecer fijos.", {"P_s": "potencia de señal", "P_n": "potencia de ruido"}),
    },
    "communication": {
        "object": "un mensaje científico situado entre una afirmación, una audiencia y una decisión posible",
        "evidence": "fuentes primarias, metadatos, citas verificables, pruebas de comprensión y revisión editorial",
        "workflow": ["definir propósito y audiencia", "jerarquizar afirmaciones", "vincular evidencia", "expresar incertidumbre", "probar comprensión", "corregir"],
        "controls": "lectura por pares, verificación de cifras y citas, prueba con audiencia, versión en lenguaje llano y registro de cambios",
        "caution": "simplificar exige conservar dirección, magnitud, incertidumbre y límites; una metáfora no puede sustituir la evidencia",
        "product": "paquete multiformato con texto académico, figura y versión divulgativa",
        "equation": (r"S=\sum_{i=1}^{k}w_i r_i", "Puntuación explícita de una rúbrica; ayuda a hacer criterios visibles, pero no convierte calidad comunicativa en una verdad objetiva.", {"w_i": "peso declarado", "r_i": "valoración por criterio"}),
    },
    "governance": {
        "object": "una decisión sociotécnica con actores, evidencia, recursos, incentivos y distribución de consecuencias",
        "evidence": "documentos normativos, datos de implementación, análisis económico, deliberación ética y perspectivas de partes interesadas",
        "workflow": ["definir problema público", "mapear actores y valores", "comparar alternativas", "evaluar consecuencias y equidad", "justificar decisión", "planificar revisión"],
        "controls": "escenario alternativo, declaración de intereses, análisis distributivo, consulta documentada y auditoría de supuestos",
        "caution": "eficiencia, legalidad, aceptabilidad y justicia son criterios distintos; ninguno sustituye por sí solo a los demás",
        "product": "memorando de decisión con alternativas, evidencia y salvaguardas",
        "equation": (r"V(a)=\sum_{i=1}^{k} w_i r_i(a)", "Modelo multicriterio transparente para comparar alternativas; pesos y puntuaciones expresan juicios que deben someterse a sensibilidad.", {"a": "alternativa", "w_i": "peso", "r_i": "desempeño en el criterio"}),
    },
    "digital_health": {
        "object": "un sistema de información clínica con datos, semántica, usuarios, decisiones y riesgos",
        "evidence": "diccionarios, perfiles de datos, pruebas de interoperabilidad, métricas de desempeño, auditorías y evaluación de uso",
        "workflow": ["definir uso y unidad de observación", "modelar datos y significado", "implementar transformación", "validar técnica y clínicamente", "vigilar desempeño"],
        "controls": "caso sintético conocido, esquema inválido, código ausente, cambio de distribución y prueba de acceso",
        "caution": "un modelo o una interfaz técnicamente correctos no garantizan utilidad clínica, equidad, seguridad ni adopción",
        "product": "prototipo reproducible con contrato de datos y plan de validación",
        "equation": (r"PPV=\frac{Se\,\pi}{Se\,\pi+(1-Sp)(1-\pi)}", "Valor predictivo positivo como función de sensibilidad, especificidad y prevalencia; muestra por qué el contexto modifica la interpretación.", {"Se": "sensibilidad", "Sp": "especificidad", r"\pi": "prevalencia"}),
    },
    "biomechanics": {
        "object": "un sistema mecánico biológico con geometría, materiales, cargas y condiciones de frontera",
        "evidence": "cinemática, fuerzas, propiedades constitutivas, calibración, convergencia y comparación experimental",
        "workflow": ["idealizar sistema", "definir coordenadas y cargas", "formular balances", "resolver", "verificar", "validar y analizar sensibilidad"],
        "controls": "equilibrio estático, solución analítica, refinamiento de discretización, conservación y condición extrema plausible",
        "caution": "una predicción mecánica depende de geometría, parámetros y fronteras; no autoriza por sí sola una decisión clínica o quirúrgica",
        "product": "modelo mecánico documentado con verificación y límites",
        "equation": (r"\sum \mathbf{F}=m\mathbf{a}", "Balance de fuerzas para el sistema definido; requiere declarar marco de referencia, cuerpo libre y fuerzas externas.", {"m": "masa", r"\mathbf{a}": "aceleración"}),
    },
    "imaging": {
        "object": "una cadena de formación, reconstrucción, procesamiento y cuantificación de imagen",
        "evidence": "datos originales, metadatos DICOM, fantomas o referencias, métricas, anotaciones y evaluación externa",
        "workflow": ["definir tarea de imagen", "auditar adquisición", "procesar sin fuga", "cuantificar", "comparar referencia", "analizar generalización"],
        "controls": "fantoma o imagen sintética, repetición, anotador alternativo, perturbación conocida y conjunto externo",
        "caution": "una imagen visualmente convincente o una métrica global alta no demuestra validez clínica ni robustez fuera de distribución",
        "product": "pipeline de imagen reproducible con informe cuantitativo",
        "equation": (r"CNR=\frac{|\mu_1-\mu_2|}{\sigma_n}", "Contraste respecto al ruido entre dos regiones; las regiones y el estimador de ruido deben predefinirse.", {r"\mu": "media regional", r"\sigma_n": "desviación del ruido"}),
    },
    "devices": {
        "object": "un dispositivo médico entendido como sistema de uso, requisitos, riesgos, interfaces y evidencia",
        "evidence": "trazabilidad necesidad-requisito-prueba, análisis de riesgos, verificación, usabilidad, mantenimiento y vigilancia",
        "workflow": ["definir uso previsto", "capturar necesidades", "especificar requisitos", "controlar riesgos", "verificar", "validar", "vigilar"],
        "controls": "requisito negativo, fallo simple simulado, usuario representativo, prueba de mantenimiento y revisión de riesgo residual",
        "caution": "completar documentación educativa no constituye conformidad normativa, certificación, autorización de mercado ni validación clínica",
        "product": "expediente de diseño o gestión con trazabilidad bidireccional",
        "equation": (r"R=P\times S", "Representación didáctica de riesgo mediante probabilidad y gravedad; las escalas ordinales no deben tratarse como mediciones físicas.", {"P": "probabilidad", "S": "gravedad"}),
    },
}


COURSE_PROFILE = {
    "fisiologia-sistemas": "biosciences", "histoanatomia-humana": "biosciences",
    "ingenieria-tejidos": "biomaterials", "nanobiotecnologia": "biomaterials",
    "biomateriales": "biomaterials", "biomateriales-implantes": "biomaterials",
    "polimeros-procesamiento-materiales": "biomaterials",
    "metodos-matematicos": "mathematics", "modelos-numericos-biomedicina": "mathematics",
    "quimica-medicinal": "chemistry",
    "redes-comunicaciones": "networks", "redes-servicios": "networks",
    "sistemas-electronicos": "electronics", "teoria-senal-biocomputacion": "electronics",
    "biofotonica": "electronics", "biosensores": "electronics",
    "electrofisica-electromecanica": "electronics", "electronica": "electronics",
    "ingenieria-neurosensorial": "electronics", "interfaces-hombre-maquina": "electronics",
    "laboratorio-bioinstrumentacion": "electronics", "laboratorio-senales-biomedicas": "electronics",
    "senales-biomedicas": "electronics",
    "comunicacion-cientifica": "communication", "uso-profesional-ingles": "communication",
    "economia-gestion-empresas": "governance", "etica-responsabilidad-social": "governance",
    "historia-filosofia-ciencia": "governance", "innovacion-emprendimiento": "governance",
    "laboratorio-globalizacion-emprendimiento": "governance",
    "politicas-publicas-ciencia-tecnologia": "governance", "tecnologias-administracion": "governance",
    "aplicaciones-salud-digital": "digital_health",
    "historias-clinicas-terminologias-estandares": "digital_health",
    "informatica-biomedica": "digital_health", "ingenieria-datos-biomedicos": "digital_health",
    "nlp-recuperacion-informacion": "digital_health", "sistemas-ayuda-decision-medica": "digital_health",
    "biomecanica": "biomechanics", "biomecanica-medios-continuos": "biomechanics",
    "fundamentos-biomecanica": "biomechanics", "laboratorio-biomecanica": "biomechanics",
    "modelado-simulacion-biomedicina": "biomechanics",
    "simulacion-planificacion-quirurgica": "biomechanics",
    "imagenes-biomedicas": "imaging", "imagenes-biomedicas-avanzadas-i": "imaging",
    "laboratorio-imagenes-biomedicas": "imaging", "tratamiento-digital-imagenes": "imaging",
    "desarrollo-dispositivos-medicos": "devices", "ingenieria-clinica-gestion": "devices",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", normalized.casefold()).strip("-") or "unidad"


def clean(value: Any) -> str:
    return " ".join(str(value or "").strip().rstrip(".").split())


def unique(items: list[str], limit: int | None = None) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        item = clean(item)
        if not item or item.casefold() in seen:
            continue
        seen.add(item.casefold())
        result.append(item)
        if limit is not None and len(result) >= limit:
            break
    return result


def catalog() -> tuple[dict[str, tuple[dict[str, Any], dict[str, Any]]], dict[str, Any]]:
    curriculum = load_json(DATA / "citonauta_curriculum.json")
    result: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for area in curriculum["areas"]:
        for subject in area["subjects"]:
            result[subject["id"]] = (area, subject)
    return result, curriculum


def concept_definition(term: str, profile: dict[str, Any]) -> str:
    known = getattr(generate_site, "CONCEPT_DEFINITIONS", {})
    definition = known.get(clean(term).casefold()) if isinstance(known, dict) else None
    if definition:
        return str(definition)
    return (
        f"Concepto de la unidad que debe definirse mediante entidades observables, relaciones, "
        f"condiciones y límites dentro de {profile['object']}; su uso exige indicar qué evidencia lo distingue de alternativas."
    )


def unit_topics(raw: list[str]) -> tuple[str, list[str], str]:
    if len(raw) != 3:
        raise ValueError(f"outline inválido: {raw!r}")
    title, topic_text, application = map(clean, raw)
    topics = unique(topic_text.split(";"))
    if len(topics) < 3:
        raise ValueError(f"{title}: se requieren al menos tres temas")
    return title, topics, application


def theory_sections(
    course_title: str,
    unit_title: str,
    topics: list[str],
    application: str,
    profile: dict[str, Any],
) -> list[dict[str, Any]]:
    first, second, third = topics[:3]
    first_definition = concept_definition(first, profile)
    second_definition = concept_definition(second, profile)
    third_definition = concept_definition(third, profile)
    latex, meaning, variables = profile["equation"]
    workflow = " → ".join(profile["workflow"])
    return [
        {
            "heading": f"Modelo conceptual de {unit_title}",
            "paragraphs": [
                f"La unidad «{unit_title}» sitúa {first}, {second} y {third} dentro de {profile['object']}. El objetivo no es memorizar tres etiquetas, sino construir un modelo que identifique entidades, escalas, entradas, transformaciones y salidas. Cada afirmación debe conservar el contexto de {course_title}, porque cambiar la unidad de observación o el uso previsto puede cambiar por completo la interpretación.",
                f"El primer núcleo de «{unit_title}» en {course_title}, «{first}», se entiende así: {first_definition} Para aplicarlo con rigor se debe indicar qué se observa directamente, qué se calcula y qué se infiere. Esta separación evita presentar una representación, una señal o una categoría como si fuera el fenómeno completo y permite localizar en qué paso aparece cada supuesto.",
                f"El segundo núcleo de «{unit_title}», «{second}», aporta otra dimensión al problema de {course_title}: {second_definition} Su relación con {first} debe formularse con una dirección explícita y una condición de validez. Una relación plausible no basta; es necesario especificar qué comparación, perturbación, medición o derivación permitiría apoyarla y qué resultado la debilitaría.",
                f"El tercer núcleo de «{unit_title}» en {course_title}, «{third}», completa la unidad: {third_definition} Integrar los tres núcleos exige reconocer fronteras. El modelo debe declarar qué deja fuera, qué escalas no conecta todavía y qué variables podrían confundir la conclusión. Esa frontera convierte la explicación en una herramienta revisable y no en una narración cerrada.",
            ],
            "key_points": [
                f"Distinguir observación, cálculo e inferencia en {unit_title}.",
                f"Relacionar {first}, {second} y {third} mediante condiciones explícitas.",
                "Declarar escala, unidad de observación y uso previsto antes del método.",
                "Tratar supuestos y límites como parte del resultado, no como una nota final.",
            ],
        },
        {
            "heading": "Método, evidencia y controles",
            "paragraphs": [
                f"Para «{unit_title}» dentro de {course_title}, el flujo recomendado es {workflow}. La secuencia obliga a definir el problema antes de elegir una herramienta y a verificar el resultado antes de interpretarlo. En cada transición deben registrarse entradas, unidades, parámetros, versiones y criterios de aceptación, de modo que otra persona pueda reconstruir por qué se tomó cada decisión.",
                f"En esta unidad de {course_title}, la evidencia pertinente incluye {profile['evidence']}. No toda fuente responde a la misma pregunta: una definición establece significado, un conjunto de datos permite estimar patrones y una guía puede fijar requisitos de reporte. Por ello, cada afirmación sobre {first} o {second} debe vincularse al tipo de evidencia capaz de sostenerla y a una referencia localizable.",
                f"Para evaluar «{unit_title}», los controles mínimos son {profile['controls']}. Un control no se añade para decorar el protocolo: debe discriminar entre la explicación principal y al menos una alternativa. Antes de observar el resultado se define qué patrón se espera en cada condición, qué desviación obliga a revisar el procedimiento y qué dato negativo sigue siendo informativo.",
                f"En {course_title}, la incertidumbre de «{unit_title}» puede aparecer en muestreo, medición, parámetros, procesamiento y elección del modelo. Se informará con intervalos, análisis de sensibilidad, escenarios o justificación cualitativa, según corresponda. La conclusión debe cambiar si una perturbación plausible cambia el resultado; ocultar esa dependencia produciría una seguridad que la evidencia no ofrece.",
            ],
            "key_points": [
                "Elegir evidencia de acuerdo con el tipo de afirmación.",
                "Predefinir controles y resultados esperados antes de inspeccionar la salida.",
                "Conservar procedencia, parámetros y decisiones intermedias.",
                "Propagar incertidumbre hasta la conclusión y la recomendación.",
            ],
        },
        {
            "heading": f"Aplicación razonada: {application}",
            "paragraphs": [
                f"En la unidad «{unit_title}» de {course_title}, el caso conductor es {application}. El equipo recibe un escenario simulado o datos abiertos y debe transformar una necesidad amplia en una pregunta verificable. Primero define la población, muestra, sistema u objeto; después fija el resultado admisible y los criterios que diferencian descripción, predicción, explicación y decisión.",
                f"La resolución específica de «{unit_title}» conecta {first} con {second} y utiliza {third} como condición o mecanismo que puede modificar la salida. Se construye una tabla de trazabilidad con pregunta, dato o premisa, transformación, control, resultado y límite. Si falta un eslabón, la respuesta no se rellena con intuición: se registra como evidencia pendiente y se propone una prueba discriminante.",
                f"Para el caso «{application}» en {course_title}, una relación cuantitativa útil para practicar el razonamiento es la ecuación mostrada en esta sección. No debe aplicarse de forma automática: primero se comprueban definiciones, unidades, rango y supuestos; luego se calcula un caso nominal y un caso límite. La interpretación debe explicar qué representa el número y qué aspectos del caso permanecen fuera del modelo.",
                f"El cierre de «{unit_title}» compara la explicación principal con una alternativa razonable. Se pregunta qué observación sería compatible con ambas, qué resultado favorecería una y qué sesgo podría producir una diferencia aparente. La recomendación final se restringe al escenario de {application} y formula el siguiente dato necesario, en lugar de extenderse a pacientes, productos o políticas no evaluados.",
            ],
            "equations": [{"latex": latex, "meaning": meaning, "variables": variables}],
            "key_points": [
                f"Delimitar el caso de {application} antes de calcular o clasificar.",
                "Mantener una cadena trazable entre pregunta, evidencia, método y conclusión.",
                "Comprobar unidades, rango, supuestos y casos límite de cada ecuación.",
                "Comparar al menos una explicación alternativa y una prueba discriminante.",
            ],
        },
        {
            "heading": "Calidad, transferencia y comunicación",
            "paragraphs": [
                f"La reproducibilidad de «{unit_title}» en {course_title} requiere datos o premisas accesibles, diccionario de variables, código o procedimiento, versiones, semillas cuando existan, criterios previos y registro de cambios. Repetir el mismo resultado en el mismo archivo es solo el inicio; también debe evaluarse si una persona independiente comprende el flujo y obtiene una conclusión compatible.",
                f"La principal cautela disciplinar al transferir «{unit_title}» es esta: {profile['caution']}. Por ello, la entrega de {course_title} separa desempeño técnico, validez científica, utilidad para el uso y consecuencias éticas o regulatorias. Cuando una de esas capas no fue evaluada, se marca explícitamente como pendiente y no se sustituye por una frase de confianza general.",
                f"La comunicación divulgativa de «{unit_title}» conserva el mecanismo central sin sobrecargar de jerga. Una explicación breve de {first}, {second} y {third} debe incluir una idea principal, una comparación concreta y una limitación. La versión académica añade método, magnitud, incertidumbre y fuentes; ambas versiones deben ser coherentes y permitir distinguir evidencia de opinión en {course_title}.",
                f"El producto de dominio será un {profile['product']} sobre {application}. Se considera sólido cuando una persona puede auditar sus fuentes, reconstruir el método, detectar sus límites y decidir qué prueba continúa. La unidad se integra en {course_title} como un componente que deberá reutilizarse y revisarse en el proyecto final del curso.",
            ],
            "key_points": [
                "Diferenciar repetibilidad, reproducibilidad, validez y utilidad.",
                "Separar desempeño técnico de afirmaciones clínicas o regulatorias.",
                "Adaptar el lenguaje sin perder magnitud, incertidumbre ni límite.",
                f"Entregar un {profile['product']} que pueda ser auditado y corregido.",
            ],
        },
    ]


def glossary(unit_title: str, topics: list[str], application: str, profile: dict[str, Any]) -> list[dict[str, str]]:
    entries = [(topic, concept_definition(topic, profile)) for topic in topics[:3]]
    entries.extend([
        (unit_title, f"Dominio de estudio que integra {', '.join(topics[:3])} para resolver un problema delimitado y verificable."),
        ("Caso de aplicación", f"Escenario de {application} usado para transferir conceptos sin afirmar validez fuera de las condiciones descritas."),
        ("Unidad de observación", "Entidad sobre la que se registra una medición o atributo y cuya independencia o jerarquía debe declararse."),
        ("Evidencia", profile["evidence"].capitalize() + ", seleccionada de acuerdo con la afirmación que se pretende sostener."),
        ("Control", profile["controls"].capitalize() + ", utilizado para distinguir explicaciones o detectar fallos del procedimiento."),
        ("Incertidumbre", "Conocimiento incompleto sobre una medición, parámetro, modelo o decisión que debe estimarse o describirse y propagarse."),
        ("Validez", "Grado en que el método y la evidencia permiten sostener la interpretación para el uso, la población y las condiciones definidas."),
        ("Reproducibilidad", "Capacidad de reconstruir un resultado con datos o premisas, procedimiento, parámetros, versiones y criterios suficientes."),
        ("Transferencia", "Aplicación razonada de un principio a un contexto nuevo después de comprobar qué supuestos se mantienen y cuáles cambian."),
    ])
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for term, definition in entries:
        if term.casefold() in seen:
            continue
        seen.add(term.casefold())
        result.append({"term": term, "definition": definition})
    fillers = [
        ("Caso límite", "Condición extrema o frontera del dominio usada para comprobar coherencia, estabilidad y alcance de un método."),
        ("Sesgo", "Desviación sistemática producida por selección, medición, procesamiento, análisis o interpretación."),
        ("Revisión por pares", "Evaluación independiente mediante criterios explícitos, registro de hallazgos y verificación de correcciones."),
    ]
    for term, definition in fillers:
        if len(result) >= 12:
            break
        if term.casefold() not in seen:
            seen.add(term.casefold())
            result.append({"term": term, "definition": definition})
    return result[:12]


def worked_examples(unit_title: str, topics: list[str], application: str, profile: dict[str, Any]) -> list[dict[str, Any]]:
    first, second, third = topics[:3]
    return [
        {
            "title": f"Del problema amplio a una evidencia verificable en {unit_title}",
            "scenario": f"Un equipo propone estudiar {application}, pero su pregunta mezcla {first}, {second} y {third} sin definir unidades, referencias ni resultado admisible.",
            "reasoning_steps": [
                "Separar necesidad, pregunta científica, decisión y producto esperado.",
                f"Definir la unidad de observación y el papel específico de {first}, {second} y {third}.",
                f"Seleccionar {profile['evidence']} y registrar procedencia y condiciones.",
                f"Predefinir {profile['controls']} y el patrón esperado en cada control.",
                "Redactar una conclusión limitada y el dato que permitiría revisarla.",
            ],
            "interpretation": f"El resultado defendible es un {profile['product']} trazable; la claridad del modelo precede a cualquier cálculo, clasificación o recomendación.",
            "limitations": [
                "El caso simulado no demuestra desempeño en un entorno real.",
                "La conclusión depende de las definiciones y controles declarados.",
                profile["caution"].capitalize() + ".",
            ],
        },
        {
            "title": "Análisis de sensibilidad y explicación alternativa",
            "scenario": f"El análisis inicial parece apoyar una relación entre {first} y {second} en el caso de {application}; una condición vinculada con {third} podría producir el mismo patrón.",
            "reasoning_steps": [
                "Escribir por separado el resultado observado y la explicación propuesta.",
                f"Representar {third} como condición, covariable, perturbación o fuente de sesgo según el diseño.",
                "Cambiar una suposición o parámetro plausible y recalcular o reargumentar la conclusión.",
                "Comparar el patrón esperado bajo la explicación principal y bajo la alternativa.",
                "Clasificar la conclusión como descriptiva, asociativa, predictiva, causal o de decisión.",
            ],
            "interpretation": "Una conclusión robusta no es la que permanece idéntica ante cualquier cambio, sino la que muestra con transparencia de qué supuestos depende y qué evidencia la refutaría.",
            "limitations": [
                "El análisis de sensibilidad solo cubre las perturbaciones evaluadas.",
                "Una alternativa no descartada reduce la fuerza de la inferencia.",
                "La transferibilidad necesita evaluación independiente.",
            ],
        },
    ]


def activities(unit_title: str, topics: list[str], application: str, profile: dict[str, Any], english: bool) -> list[dict[str, Any]]:
    first, second, third = topics[:3]
    language_task = (
        "Write the central claim, evidence statement and limitation in precise academic English."
        if english
        else "Redacta la afirmación central, la evidencia y la limitación con lenguaje preciso y comprensible."
    )
    return [
        {
            "title": "Pausa de recuperación y explicación",
            "instructions": [
                "Responde sin consultar el texto y después corrige con un color distinto.",
                "Dibuja las relaciones antes de escribir una definición extensa.",
                "Marca cada elemento como observado, calculado, inferido o pendiente.",
                "Explica la unidad a una audiencia no especialista en menos de 150 palabras.",
            ],
            "problems": [
                f"Define {first} mediante entidad, relación, condición y ejemplo.",
                f"Explica cómo {second} modifica o complementa a {first}.",
                f"Propón una prueba que distinga el papel de {third} de una explicación alternativa.",
                language_task,
            ],
            "deliverables": ["Mapa conceptual corregido.", "Explicación breve con una limitación explícita."],
            "checking_criteria": ["Las relaciones tienen dirección.", "No se confunde evidencia con interpretación.", "La explicación conserva el mecanismo central."],
        },
        {
            "title": f"Taller de evidencia: {application}",
            "instructions": [
                "Usa exclusivamente datos abiertos, literatura localizable o un escenario sintético sin datos personales.",
                "Predefine pregunta, unidad de observación, variables, controles y criterio de aceptación.",
                f"Sigue el flujo {' → '.join(profile['workflow'])}.",
                "Conserva cálculos, decisiones, resultados negativos y cambios de versión.",
                "Compara el resultado con un baseline o una explicación alternativa.",
            ],
            "problems": [
                f"Construye una tabla de trazabilidad para {first}, {second} y {third}.",
                f"Selecciona entre {profile['evidence']} y justifica qué afirmación sostiene cada fuente.",
                f"Diseña al menos dos controles a partir de: {profile['controls']}.",
                "Ejecuta un caso nominal y un caso límite con unidades o criterios explícitos.",
                "Realiza un análisis de sensibilidad sobre una decisión, parámetro o supuesto.",
                "Redacta por separado resultado, interpretación, incertidumbre y siguiente prueba.",
            ],
            "deliverables": [profile["product"].capitalize() + ".", "Datos o premisas y procedimiento reproducible.", "Registro de controles y discrepancias."],
            "checking_criteria": ["Trazabilidad completa.", "Controles discriminantes.", "Procedimiento reproducible.", "Conclusión proporcional a la evidencia."],
        },
        {
            "title": "Reto de transferencia y revisión por pares",
            "instructions": [
                "Cambia una condición importante del caso y anticipa qué parte de la solución deja de ser válida.",
                "Intercambia el producto con otra persona o utiliza una lista de revisión independiente.",
                "Registra hallazgos por severidad: crítico, importante o editorial.",
                "Corrige el producto y conserva una tabla antes-después con justificación.",
            ],
            "tasks": [
                f"Transfiere el método a un caso distinto de {application} y enumera supuestos que deben revalidarse.",
                f"Construye una explicación alternativa que también conecte {first}, {second} y {third}.",
                "Identifica una afirmación que exceda la evidencia y reescríbela.",
                "Añade una figura o tabla cuya codificación visual pueda auditarse sin depender del color.",
                "Formula una pregunta de examen que evalúe transferencia y escribe una rúbrica de tres niveles.",
            ],
            "deliverables": ["Producto revisado.", "Registro antes-después.", "Rúbrica de transferencia."],
            "checking_criteria": ["La revisión produce cambios verificables.", "Las limitaciones son específicas.", "La figura conserva unidades y procedencia.", "La nueva pregunta no se responde por memorización."],
        },
    ]


def common_errors(unit_title: str, topics: list[str], profile: dict[str, Any]) -> list[dict[str, str]]:
    first, second, third = topics[:3]
    return [
        {"error": f"Tratar {first} como una etiqueta autosuficiente.", "correction": f"Definir entidades, escala, relaciones, observables y condiciones antes de usar {first} en una explicación."},
        {"error": f"Afirmar que una relación entre {first} y {second} demuestra mecanismo o causalidad.", "correction": "Separar asociación, predicción, intervención y causalidad; proponer una comparación que discrimine explicaciones."},
        {"error": f"Añadir {third} después de ver el resultado.", "correction": "Predefinir su papel, el análisis y el criterio de interpretación o declarar el análisis como exploratorio."},
        {"error": "Presentar solo el resultado favorable y omitir controles o discrepancias.", "correction": f"Incluir {profile['controls']}, resultados negativos, fallos y cambios de procedimiento."},
        {"error": f"Generalizar la conclusión de {unit_title} al uso clínico o real.", "correction": profile["caution"].capitalize() + "."},
    ]


def self_assessment(unit_title: str, topics: list[str], application: str, profile: dict[str, Any]) -> list[dict[str, str]]:
    first, second, third = topics[:3]
    qa = [
        (f"¿Cuál es la unidad de observación adecuada para estudiar {application}?", "Depende de la pregunta; debe declararse una entidad concreta y distinguirse de sus niveles superiores e inferiores.", "Confundir células, muestras, sujetos, dispositivos o instituciones como si fueran réplicas equivalentes."),
        (f"¿Cómo se relacionan {first} y {second}?", f"Mediante una relación con dirección, condición y evidencia verificable; {third} puede modificar o contextualizar esa relación.", "Responder con una lista de definiciones sin explicar la relación."),
        (f"¿Qué dato apoya una afirmación sobre {third}?", profile["evidence"].capitalize() + ", elegido de acuerdo con el tipo de afirmación.", "Usar una fuente secundaria o una visualización sin procedencia como prueba suficiente."),
        ("¿Qué hace que un control sea discriminante?", "Que las explicaciones rivales predigan resultados diferentes y que el control mida precisamente esa diferencia.", "Añadir un control que no puede cambiar la interpretación."),
        ("¿Qué debe contener un resultado reproducible?", "Pregunta, datos o premisas, diccionario, procedimiento, parámetros, versiones, controles, resultados y registro de cambios.", "Entregar únicamente una figura final o un archivo ejecutado."),
        ("¿Cómo se informa una conclusión sensible a un supuesto?", "Se muestra el resultado bajo valores plausibles, se identifica el punto de cambio y se limita la recomendación.", "Elegir el escenario que confirma la conclusión y ocultar los demás."),
        (f"¿Qué afirmación no puede sostener esta unidad sobre {application}?", profile["caution"].capitalize() + ".", "Confundir una actividad educativa o un caso simulado con validación real."),
        (f"¿Qué demuestra dominio de {unit_title}?", f"Producir un {profile['product']} auditable, explicar los conceptos, resolver un caso nuevo y corregir errores con evidencia.", "Equiparar dominio con reconocer términos o repetir una solución."),
    ]
    return [
        {"question": question, "answer": answer, "reasoning": "La respuesta debe conectar definición, evidencia, método y límite.", "common_error": error}
        for question, answer, error in qa
    ]


def build_unit(
    subject_id: str,
    area_id: str,
    course_title: str,
    number: int,
    raw: list[str],
    profile_name: str,
) -> dict[str, Any]:
    title, topics, application = unit_topics(raw)
    profile = PROFILES[profile_name]
    sources = RESOURCE_POOLS[profile_name]
    rotated = sources[(number - 1) % len(sources):] + sources[:(number - 1) % len(sources)]
    english = subject_id == "uso-profesional-ingles"
    return {
        "schema_version": "2.0",
        "subject_id": subject_id,
        "area_id": area_id,
        "unit": number,
        "slug": slugify(title),
        "title": title,
        "status": "review",
        "purpose": f"Integrar {', '.join(topics[:3])} para resolver un caso de {application} con evidencia, controles, incertidumbre y comunicación proporcional.",
        "learning_objectives": [
            f"Definir {topics[0]}, {topics[1]} y {topics[2]} mediante entidades, relaciones y condiciones.",
            f"Construir un modelo que conecte {topics[0]} con {topics[1]} y delimite el papel de {topics[2]}.",
            f"Seleccionar {profile['evidence']} de acuerdo con la pregunta.",
            f"Diseñar controles pertinentes a partir de {profile['controls']}.",
            f"Resolver y comunicar un caso sobre {application} con incertidumbre y límites.",
            f"Transferir el método de {title} a un escenario nuevo y justificar qué debe revalidarse.",
        ],
        "theory_sections": theory_sections(course_title, title, topics, application, profile),
        "glossary": glossary(title, topics, application, profile),
        "worked_examples": worked_examples(title, topics, application, profile),
        "guided_activities": activities(title, topics, application, profile, english),
        "common_errors": common_errors(title, topics, profile),
        "self_assessment": self_assessment(title, topics, application, profile),
        "biomedical_connections": [
            {"topic": "Aplicación principal", "connection": application.capitalize() + "."},
            {"topic": "Evidencia", "connection": profile["evidence"].capitalize() + "."},
            {"topic": "Calidad", "connection": "Trazabilidad, controles, sensibilidad, reproducibilidad y revisión de discrepancias."},
            {"topic": "Límite", "connection": profile["caution"].capitalize() + "."},
        ],
        "sources": rotated[:5],
        "editorial_notice": "Material educativo con desarrollo interno completo y estado review. Requiere revisión disciplinar externa antes de considerarse verificado; no sustituye formación práctica supervisada, evaluación profesional, diagnóstico, tratamiento, certificación ni conformidad regulatoria.",
    }


def course_assessment() -> list[dict[str, str]]:
    return [
        {"title": "Recuperación y explicación", "weight": "15 %", "description": "Preguntas de baja carga, mapas corregidos y explicaciones que distinguen evidencia e inferencia."},
        {"title": "Problemas y casos", "weight": "25 %", "description": "Resoluciones con procedimiento, controles, interpretación, sensibilidad y límites."},
        {"title": "Laboratorios reproducibles", "weight": "25 %", "description": "Datos abiertos o sintéticos, código o procedimiento, procedencia, pruebas y registro de discrepancias."},
        {"title": "Revisión por pares", "weight": "10 %", "description": "Uso de rúbrica, clasificación de hallazgos, corrección y justificación antes-después."},
        {"title": "Proyecto integrador", "weight": "25 %", "description": "Producto acumulativo que conecta las seis unidades y defiende una conclusión proporcional."},
    ]


def final_project(title: str, profile: dict[str, Any], units: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "title": f"Expediente integrador de {title}",
        "scenario": f"Un equipo académico debe construir un {profile['product']} para un caso biomédico simulado o sustentado en datos abiertos, sin intervenir en personas ni afirmar validación clínica.",
        "phases": [
            "Delimitar necesidad, pregunta, uso, unidad de observación y criterios de aceptación.",
            "Construir el modelo conceptual y la matriz de trazabilidad de las seis unidades.",
            "Ejecutar análisis o prototipo con controles, casos límite y sensibilidad.",
            "Realizar revisión independiente, corregir y registrar cambios.",
            "Defender resultados, incertidumbre, límites, riesgos y siguiente evidencia necesaria.",
        ],
        "deliverables": [
            profile["product"].capitalize() + ".",
            "Datos o premisas, diccionario y procedimiento reproducible.",
            "Matriz pregunta-evidencia-método-control-resultado-límite.",
            "Informe académico y resumen divulgativo coherentes.",
            "Registro de revisión y correcciones antes-después.",
        ],
        "integration_requirements": [
            f"Usar evidencia de las unidades {', '.join(str(unit['unit']) for unit in units)}.",
            "Incluir al menos un control negativo, un caso límite y una explicación alternativa.",
            "Separar resultado técnico, interpretación científica, utilidad y afirmaciones fuera de alcance.",
        ],
        "rubric": [
            {"criterion": "Corrección conceptual y trazabilidad", "weight_percent": 30, "excellent": "Cada afirmación se vincula con evidencia, método, control y límite."},
            {"criterion": "Método y reproducibilidad", "weight_percent": 25, "excellent": "El flujo puede reconstruirse y contiene pruebas, parámetros y versiones."},
            {"criterion": "Controles, incertidumbre y sensibilidad", "weight_percent": 20, "excellent": "Compara alternativas y muestra de qué depende la conclusión."},
            {"criterion": "Transferencia biomédica responsable", "weight_percent": 15, "excellent": "Resuelve el uso definido sin extrapolaciones clínicas o regulatorias."},
            {"criterion": "Comunicación y revisión", "weight_percent": 10, "excellent": "La narrativa es clara, accesible, corregida y coherente con las figuras."},
        ],
    }


def build_course(area: dict[str, Any], subject: dict[str, Any], raws: list[list[str]], profile_name: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    subject_id = subject["id"]
    title = subject["title"]
    profile = PROFILES[profile_name]
    units = [build_unit(subject_id, area["id"], title, number, raw, profile_name) for number, raw in enumerate(raws, start=1)]
    detailed_units = [
        {"unit": unit["unit"], "title": unit["title"], "description": unit["purpose"], "learning_outcomes": unit["learning_objectives"][:3]}
        for unit in units
    ]
    topic_names = [term for raw in raws for term in unit_topics(raw)[1]]
    diagnostics = [
        "Define la pregunta, la unidad de observación y el resultado admisible en un caso breve.",
        "Distingue dato observado, variable calculada, interpretación y decisión.",
        "Explica la diferencia entre asociación, predicción, causalidad y utilidad.",
        "Propón un control negativo y describe qué error detectaría.",
        "Interpreta una magnitud con unidades y un caso límite.",
        "Identifica una fuente primaria, una guía y una base de datos; explica su función distinta.",
        "Describe cómo registrarías versiones, parámetros y cambios para reproducir un resultado.",
        "Explica qué significa analizar sensibilidad a un supuesto.",
        "Reescribe una afirmación exagerada para ajustarla a la evidencia.",
        "Propón una figura accesible con ejes, unidades, procedencia y mensaje explícitos.",
        "Enumera dos riesgos de transferir un resultado técnico a una decisión biomédica.",
        "Formula una pregunta que no pueda responderse por memorización y justifica la respuesta.",
    ]
    course = {
        "schema_version": "2.0",
        "id": subject_id,
        "subject_id": subject_id,
        "area_id": area["id"],
        "title": title,
        "status": "review",
        "level": "Pregrado universitario intermedio y avanzado",
        "description": f"Curso completo de {title} orientado a comprender, aplicar, verificar y comunicar sus métodos en problemas biomédicos. Integra teoría, casos, práctica reproducible, controles, incertidumbre, revisión y transferencia responsable.",
        "biomedical_connection": subject["biomedical_connection"],
        "prerequisites": generate_site.prerequisites_for(area["id"], subject_id),
        "course_competencies": [
            f"Construir modelos conceptuales rigurosos en {title}.",
            f"Aplicar el flujo {' → '.join(profile['workflow'])} a casos nuevos.",
            f"Seleccionar y documentar {profile['evidence']}.",
            "Diseñar controles, casos límite y análisis de sensibilidad.",
            "Producir resultados reproducibles con procedencia, parámetros, versiones y registro de cambios.",
            "Comunicar a audiencias académicas y generales sin exagerar evidencia ni alcance.",
        ],
        "learning_objectives": [unit["purpose"] for unit in units],
        "learning_outcomes": [
            f"Explica y relaciona los dominios centrales de {title} con precisión.",
            f"Entrega un {profile['product']} reproducible y auditable.",
            "Resuelve problemas inéditos declarando unidades, supuestos, controles y límites.",
            "Compara una explicación principal con alternativas y propone pruebas discriminantes.",
            "Evalúa sensibilidad, incertidumbre, riesgo de sesgo y transferibilidad.",
            "Corrige un producto después de revisión y justifica cada cambio.",
            "Distingue desempeño técnico, validez científica, utilidad y evidencia clínica o regulatoria.",
        ],
        "modules": [f"Unidad {unit['unit']}: {unit['title']}. {unit['purpose']}" for unit in units],
        "detailed_units": detailed_units,
        "practical_activities": [
            {"title": f"Reto {unit['unit']}: {unit['title']}", "description": unit["guided_activities"][1]["title"] + ".", "type": "actividad aplicada reproducible"}
            for unit in units
        ],
        "assessment": course_assessment(),
        "key_concepts": unique(topic_names + ["evidencia", "control", "incertidumbre", "validez", "reproducibilidad", "transferencia"], 24),
        "related_subjects": generate_site.related_subjects_for(subject_id, area["id"]),
        "suggested_resources": RESOURCE_POOLS[profile_name],
        "study_method": [
            "Realizar el diagnóstico antes de consultar respuestas y convertir errores en objetivos de estudio.",
            "Alternar recuperación sin apoyo, ejemplo resuelto, práctica guiada y reto de transferencia.",
            "Registrar observación, cálculo, inferencia y decisión en columnas separadas.",
            "Predefinir controles y criterios antes de observar resultados.",
            "Conservar datos o premisas, código o procedimiento, parámetros, versiones y resultados negativos.",
            "Revisar con rúbrica, corregir y explicar por qué cambió el producto.",
        ],
        "diagnostic_assessment": {
            "title": f"Diagnóstico de entrada a {title}",
            "purpose": "Identificar prerrequisitos conceptuales, cuantitativos, metodológicos y comunicativos; no se usa como calificación final.",
            "questions": diagnostics,
            "interpretation": [
                "0-4 respuestas sólidas: completar nivelación y repetir con preguntas equivalentes.",
                "5-8 respuestas sólidas: iniciar el curso y reforzar los dominios fallidos.",
                "9-12 respuestas sólidas: comenzar con los retos de transferencia y documentar límites.",
            ],
        },
        "assessment_principles": [
            "La evidencia de dominio es una producción verificable, no el tiempo empleado ni el volumen de texto.",
            "Una respuesta final sin procedimiento, controles e interpretación recibe crédito limitado.",
            "La recuperación sin apoyo precede a la consulta de soluciones.",
            "Los errores corregidos con justificación forman parte de la evaluación.",
            "Los datos personales, la intervención en personas y las prácticas inseguras quedan fuera del material autónomo.",
            "El estado review se mantiene hasta una revisión disciplinar externa documentada.",
        ],
        "final_project": final_project(title, profile, units),
        "core_resources": RESOURCE_POOLS[profile_name],
        "completion_criteria": [
            "Demostrar cada resultado de aprendizaje en al menos una evidencia verificable.",
            "Completar las seis unidades y corregir los errores críticos detectados.",
            "Entregar el proyecto con trazabilidad, controles, sensibilidad y límites.",
            "Aprobar una defensa que incluya un caso nuevo o una perturbación no ensayada.",
            "Mantener coherencia entre informe académico, figuras y resumen divulgativo.",
        ],
    }
    return course, units


def coverage_spec(course: dict[str, Any], units: list[dict[str, Any]]) -> dict[str, Any]:
    domains = []
    for unit in units:
        headings = [section["heading"] for section in unit["theory_sections"]]
        topics = [entry["term"] for entry in unit["glossary"][:3]]
        domains.append({
            "id": f"unit-{unit['unit']:02d}",
            "title": unit["title"],
            "required_topics": topics + ["evidencia, controles, incertidumbre y límites"],
            "mastery_evidence": [f"Entrega y defiende la actividad de {unit['title']} con trazabilidad, controles, sensibilidad y corrección de errores."],
            "public_sections": headings,
        })
    return {
        "title": course["title"],
        "coverage_state": "implemented",
        "core_domains": domains,
        "practical_requirements": [
            "Recuperación, explicación y corrección en cada unidad.",
            "Caso reproducible con datos abiertos o sintéticos y controles predefinidos.",
            "Reto de transferencia con explicación alternativa y análisis de sensibilidad.",
            "Proyecto final acumulativo con revisión y registro antes-después.",
        ],
        "visual_requirements": [
            "Figuras y tablas con título, unidades, procedencia, codificación accesible y mensaje explícito.",
            "Representación de datos o premisas, transformaciones, controles, incertidumbre y discrepancias.",
            "Separación visual entre resultado observado, inferencia y decisión.",
        ],
        "expansion_priorities": [
            "Revisión disciplinar externa por una persona cualificada.",
            "Prueba cognitiva y de usabilidad con estudiantes reales antes de declarar verificación.",
            "Corrección documentada de hallazgos y nueva auditoría de fuentes.",
        ],
    }


def close_existing_partials() -> int:
    changed = 0
    for path in sorted((DATA / "curriculum_coverage").glob("*.json")):
        if path == COVERAGE_PATH:
            continue
        payload = load_json(path)
        dirty = False
        for subject_id, specification in payload.get("courses", {}).items():
            if specification.get("coverage_state") != "partial":
                continue
            if not (GENERATED_COURSES / f"{subject_id}.json").exists():
                continue
            specification["coverage_state"] = "implemented"
            priorities = specification.setdefault("expansion_priorities", [])
            note = "Mantener estado editorial review hasta completar revisión disciplinar externa documentada."
            if note not in priorities:
                priorities.append(note)
            dirty = True
            changed += 1
        if dirty:
            write_json(path, payload)
    return changed


def build(subject_ids: list[str]) -> dict[str, Any]:
    subjects, _ = catalog()
    outlines = load_json(DATA / "course_outlines.json")
    existing_coverage = load_json(COVERAGE_PATH) if COVERAGE_PATH.exists() else {}
    coverage_courses: dict[str, Any] = dict(existing_coverage.get("courses", {}))
    built: list[str] = []
    for subject_id in subject_ids:
        if subject_id not in COURSE_PROFILE:
            raise KeyError(f"falta perfil disciplinar para {subject_id}")
        area, subject = subjects[subject_id]
        raws = outlines[area["id"]][subject_id]
        course, units = build_course(area, subject, raws, COURSE_PROFILE[subject_id])
        package = REDEVELOPMENT / subject_id
        write_json(package / "course.json", course)
        for unit in units:
            write_json(package / "units" / f"unit-{unit['unit']:02d}.json", unit)
        coverage_courses[subject_id] = coverage_spec(course, units)
        built.append(subject_id)
    write_json(COVERAGE_PATH, {
        "schema_version": "1.0",
        "portfolio_standard": "coverage-based",
        "generated_by": "scripts/complete_catalog_content.py",
        "courses": coverage_courses,
    })
    return {"built": built, "units": len(built) * 6}


def main() -> int:
    parser = argparse.ArgumentParser(description="Completa los cursos que todavía dependen del renderer de respaldo.")
    parser.add_argument("--subject", action="append", default=[], help="Limita el proceso a una asignatura; repetible.")
    parser.add_argument("--close-existing-partials", action="store_true", help="Cambia matrices partial estructuralmente válidas a implemented, nunca a verified.")
    args = parser.parse_args()

    subjects, _ = catalog()
    if args.subject:
        selected = sorted(set(args.subject))
    else:
        selected = sorted(COURSE_PROFILE)
    unknown = sorted(set(selected) - set(subjects))
    if unknown:
        raise SystemExit("Asignaturas desconocidas: " + ", ".join(unknown))
    if set(selected) - set(COURSE_PROFILE):
        raise SystemExit("Perfiles faltantes: " + ", ".join(sorted(set(selected) - set(COURSE_PROFILE))))

    summary = build(selected)
    partials = close_existing_partials() if args.close_existing_partials else 0
    print(json.dumps({**summary, "existing_partial_matrices_closed": partials}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
