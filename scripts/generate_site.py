#!/usr/bin/env python3
"""Generador estático para páginas de asignatura de CitoNauta.

El script lee data/citonauta_curriculum.json y usa templates/asignatura.html
para generar páginas HTML de asignaturas. Por defecto funciona en modo seguro:
no sobrescribe archivos existentes salvo que se use --force.

También puede enriquecer asignaturas con archivos opcionales en:

data/subjects/<area_id>/<subject_id>.json
"""

from __future__ import annotations

import argparse
import html
import json
import os
from functools import cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "citonauta_curriculum.json"
OUTLINES_PATH = ROOT / "data" / "course_outlines.json"
TEMPLATE_PATH = ROOT / "templates" / "asignatura.html"
AREA_TEMPLATE_PATH = ROOT / "templates" / "area.html"
SUBJECT_DATA_DIR = ROOT / "data" / "subjects"
REQUIRED_TEMPLATE_KEYS = {
    "subject_title",
    "area_title",
    "subject_description",
    "css_path",
    "editorial_css_path",
    "home_path",
    "area_path",
    "previous_link",
    "next_link",
    "biomedical_connection",
    "level",
    "estimated_workload",
    "status",
    "status_label",
    "prerequisites",
    "course_competencies",
    "learning_objectives",
    "learning_outcomes",
    "modules",
    "detailed_units",
    "practical_activities",
    "assessment",
    "key_concepts",
    "related_subjects",
    "suggested_resources",
}

STATUS_LABELS = {
    "placeholder": "Contenido pendiente",
    "draft": "Borrador inicial",
    "review": "Curso completo · revisión editorial recomendada",
    "complete": "Curso revisado y completo",
}

COURSE_FAMILIES = (
    {
        "algebra", "calculo", "ampliacion-calculo", "ecuaciones-diferenciales",
        "metodos-matematicos", "metodos-numericos", "modelos-numericos-biomedicina",
        "modelado-simulacion-biomedicina",
    },
    {
        "probabilidad-estadistica", "bioestadistica", "analisis-estadistico-multivariado",
        "ingenieria-datos-biomedicos", "sistemas-ayuda-decision-medica",
    },
    {
        "fundamentos-programacion", "algoritmos-estructuras-datos", "arquitectura-computadores",
        "bases-datos", "redes-comunicaciones", "redes-servicios", "informatica-biomedica",
        "ingenieria-datos-biomedicos", "nlp-recuperacion-informacion", "bioinformatica",
    },
    {
        "fisica-i", "fisica-ii", "biofisica", "sistemas-electronicos", "electronica",
        "electrofisica-electromecanica", "biofotonica", "analisis-instrumental",
    },
    {
        "quimica-i", "quimica-ii", "quimica-medicinal", "bioquimica", "biomateriales",
        "polimeros-procesamiento-materiales", "nanobiotecnologia", "biosensores",
    },
    {
        "biologia-i", "biologia-ii", "biologia-celular-tisular", "biologia-molecular",
        "biologia-molecular-celular-aplicada", "genetica", "biologia-desarrollo",
        "biologia-sintetica", "bioquimica", "ingenieria-tejidos", "nanobiotecnologia",
    },
    {
        "fisiologia-humana-i", "fisiologia-humana-ii", "fisiologia-sistemas",
        "fisiopatologia-humana", "histoanatomia-humana", "senales-biomedicas",
        "bioinstrumentacion", "imagenes-biomedicas",
    },
    {
        "fundamentos-biomecanica", "biomecanica", "biomecanica-medios-continuos",
        "laboratorio-biomecanica", "interfaces-hombre-maquina", "ingenieria-neurosensorial",
        "simulacion-planificacion-quirurgica",
    },
    {
        "sistemas-senales", "teoria-senal-biocomputacion", "senales-biomedicas",
        "laboratorio-senales-biomedicas", "bioinstrumentacion", "laboratorio-bioinstrumentacion",
        "biosensores",
    },
    {
        "imagenes-biomedicas", "imagenes-biomedicas-avanzadas-i", "imagenes-biomedicas-avanzadas-ii",
        "tratamiento-digital-imagenes", "laboratorio-imagenes-biomedicas",
        "simulacion-planificacion-quirurgica", "biofotonica",
    },
    {
        "biomateriales", "biomateriales-implantes", "polimeros-procesamiento-materiales",
        "ingenieria-tejidos", "desarrollo-dispositivos-medicos", "ingenieria-clinica-gestion",
    },
    {
        "informatica-biomedica", "historias-clinicas-terminologias-estandares",
        "aplicaciones-salud-digital", "ingenieria-datos-biomedicos",
        "sistemas-ayuda-decision-medica", "interfaces-hombre-maquina",
    },
    {
        "comunicacion-cientifica", "uso-profesional-ingles", "etica-responsabilidad-social",
        "historia-filosofia-ciencia", "politicas-publicas-ciencia-tecnologia",
    },
    {
        "economia-gestion-empresas", "innovacion-emprendimiento",
        "laboratorio-globalizacion-emprendimiento", "tecnologias-administracion",
        "politicas-publicas-ciencia-tecnologia", "desarrollo-dispositivos-medicos",
    },
)

REQUIRED_AREA_TEMPLATE_KEYS = {
    "area_title",
    "area_description",
    "css_path",
    "editorial_css_path",
    "home_path",
    "subject_count",
    "subject_cards",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo de datos: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"No existe la plantilla: {path}")
    return path.read_text(encoding="utf-8")


@cache
def load_outlines() -> dict[str, dict[str, list[list[str]]]]:
    return load_json(OUTLINES_PATH)


@cache
def subject_catalog() -> dict[str, dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}
    for area in load_json(DATA_PATH).get("areas", []):
        for order, subject in enumerate(area.get("subjects", [])):
            catalog[subject["id"]] = {
                **subject,
                "area_id": area["id"],
                "area_title": area["title"],
                "order": order,
            }
    return catalog


def unique_strings(items: list[str], limit: int | None = None) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        cleaned = str(item).strip()
        normalized = cleaned.casefold()
        if not cleaned or normalized in seen:
            continue
        seen.add(normalized)
        result.append(cleaned)
        if limit is not None and len(result) >= limit:
            break
    return result


def prerequisites_for(area_id: str, subject_id: str) -> list[str]:
    statistics = {"probabilidad-estadistica", "bioestadistica", "analisis-estadistico-multivariado"}
    computing = {
        "algoritmos-estructuras-datos", "arquitectura-computadores", "bases-datos",
        "redes-comunicaciones", "redes-servicios", "ingenieria-datos-biomedicos",
        "nlp-recuperacion-informacion", "bioinformatica", "informatica-biomedica",
    }
    quantitative_engineering = {
        "biofisica", "sistemas-electronicos", "sistemas-senales", "teoria-senal-biocomputacion",
        "bioinstrumentacion", "biomecanica", "biomecanica-medios-continuos", "biofotonica",
        "imagenes-biomedicas-avanzadas-i", "imagenes-biomedicas-avanzadas-ii",
        "modelado-simulacion-biomedicina", "tratamiento-digital-imagenes",
    }
    if subject_id == "algebra":
        return [
            "Aritmética, fracciones, potencias y proporcionalidad de nivel preuniversitario.",
            "Lectura de tablas, ejes cartesianos y expresiones cuantitativas sencillas.",
            "Disposición para justificar cada procedimiento y comprobar unidades y resultados.",
        ]
    if subject_id == "fundamentos-programacion":
        return [
            "Manejo básico de archivos y carpetas en un computador.",
            "Razonamiento lógico y capacidad para descomponer problemas en pasos.",
            "No se requiere experiencia previa en programación.",
        ]
    if subject_id in statistics:
        return [
            "Álgebra elemental, funciones y lectura de gráficos.",
            "Conceptos básicos de diseño de estudios y tipos de variables.",
            "Manejo introductorio de hojas de cálculo o un lenguaje como R o Python.",
        ]
    if subject_id in computing:
        return [
            "Fundamentos de programación: variables, control de flujo, funciones y archivos.",
            "Álgebra y razonamiento lógico de nivel universitario inicial.",
            "Uso básico de terminal, control de versiones y documentación técnica.",
        ]
    if subject_id in quantitative_engineering:
        return [
            "Álgebra, cálculo y física de nivel universitario inicial.",
            "Programación básica para análisis numérico y visualización.",
            "Fundamentos de biología o fisiología pertinentes al sistema estudiado.",
        ]
    if area_id == "biologicas-medicas":
        return [
            "Biología general y química de nivel universitario inicial.",
            "Bases de estructura celular, biomoléculas y homeostasis.",
            "Lectura de figuras científicas y estadística descriptiva elemental.",
        ]
    if area_id == "ingenieria-biomedica":
        return [
            "Matemáticas, física y programación de nivel universitario inicial.",
            "Bases de biología celular, anatomía o fisiología humana.",
            "Capacidad para documentar requisitos, supuestos, mediciones y resultados.",
        ]
    if area_id == "gestion-etica-comunicacion":
        return [
            "Comprensión lectora y escritura académica de nivel universitario.",
            "Familiaridad introductoria con ciencia, tecnología y salud.",
            "Disposición para analizar perspectivas, evidencia, incertidumbre y consecuencias sociales.",
        ]
    return [
        "Matemáticas y razonamiento cuantitativo de nivel preuniversitario.",
        "Lectura de gráficos, tablas, fórmulas y unidades científicas.",
        "Capacidad para documentar procedimientos y comprobar la coherencia de resultados.",
    ]


def resources_for(area_id: str, subject_id: str) -> list[dict[str, str]]:
    statistics = {"probabilidad-estadistica", "bioestadistica", "analisis-estadistico-multivariado"}
    computing = {
        "fundamentos-programacion", "algoritmos-estructuras-datos", "arquitectura-computadores",
        "bases-datos", "redes-comunicaciones", "redes-servicios", "ingenieria-datos-biomedicos",
        "nlp-recuperacion-informacion", "teoria-senal-biocomputacion",
    }
    chemistry = {"quimica-i", "quimica-ii", "quimica-medicinal", "bioquimica"}
    imaging = {
        "imagenes-biomedicas", "imagenes-biomedicas-avanzadas-i", "imagenes-biomedicas-avanzadas-ii",
        "laboratorio-imagenes-biomedicas", "tratamiento-digital-imagenes",
        "simulacion-planificacion-quirurgica",
    }
    informatics = {
        "bioinformatica", "informatica-biomedica", "historias-clinicas-terminologias-estandares",
        "aplicaciones-salud-digital", "sistemas-ayuda-decision-medica",
    }
    if subject_id in statistics:
        return [
            {"title": "OpenIntro Statistics", "description": "Texto abierto con datos, ejercicios y fundamentos de inferencia.", "type": "libro abierto", "url": "https://www.openintro.org/book/os/"},
            {"title": "NIST/SEMATECH e-Handbook", "description": "Manual oficial de métodos estadísticos y control de procesos.", "type": "manual", "url": "https://www.itl.nist.gov/div898/handbook/"},
            {"title": "R Project Manuals", "description": "Documentación oficial para análisis estadístico reproducible con R.", "type": "documentación", "url": "https://cran.r-project.org/manuals.html"},
            {"title": "EQUATOR Network", "description": "Guías para reportar estudios de salud de forma transparente.", "type": "guías", "url": "https://www.equator-network.org/"},
            {"title": "NCBI Bookshelf", "description": "Capítulos abiertos de bioestadística, epidemiología y medicina basada en evidencia.", "type": "biblioteca", "url": "https://www.ncbi.nlm.nih.gov/books/"},
        ]
    if subject_id in computing:
        return [
            {"title": "Python Documentation", "description": "Tutorial y referencia oficial del lenguaje Python.", "type": "documentación", "url": "https://docs.python.org/3/"},
            {"title": "Software Carpentry Lessons", "description": "Lecciones abiertas sobre programación, terminal, Git y trabajo reproducible.", "type": "curso abierto", "url": "https://software-carpentry.org/lessons/"},
            {"title": "MIT OpenCourseWare", "description": "Cursos abiertos de programación, algoritmos, redes y matemáticas.", "type": "cursos abiertos", "url": "https://ocw.mit.edu/"},
            {"title": "PhysioNet", "description": "Datos y herramientas abiertas para practicar con señales y registros fisiológicos.", "type": "datos abiertos", "url": "https://physionet.org/"},
            {"title": "The Turing Way", "description": "Guía abierta de ciencia de datos reproducible, colaborativa y ética.", "type": "guía", "url": "https://book.the-turing-way.org/"},
        ]
    if subject_id in chemistry:
        return [
            {"title": "OpenStax Chemistry 2e", "description": "Texto abierto de química general con ejercicios y fundamentos.", "type": "libro abierto", "url": "https://openstax.org/details/books/chemistry-2e"},
            {"title": "IUPAC Gold Book", "description": "Compendio oficial de terminología química.", "type": "referencia", "url": "https://goldbook.iupac.org/"},
            {"title": "PubChem", "description": "Base de datos pública de compuestos, propiedades y bioactividad.", "type": "base de datos", "url": "https://pubchem.ncbi.nlm.nih.gov/"},
            {"title": "NCBI Bookshelf", "description": "Libros abiertos de bioquímica, farmacología y ciencias biomédicas.", "type": "biblioteca", "url": "https://www.ncbi.nlm.nih.gov/books/"},
            {"title": "ChEMBL", "description": "Base de datos curada de moléculas bioactivas y dianas.", "type": "base de datos", "url": "https://www.ebi.ac.uk/chembl/"},
        ]
    if subject_id in imaging:
        return [
            {"title": "3D Slicer Documentation", "description": "Plataforma abierta para visualización, segmentación y análisis de imagen médica.", "type": "software abierto", "url": "https://slicer.readthedocs.io/"},
            {"title": "ITK Documentation", "description": "Biblioteca abierta para registro, segmentación y procesamiento de imágenes.", "type": "documentación", "url": "https://docs.itk.org/"},
            {"title": "DICOM Standard", "description": "Fuente oficial del estándar de imagen y comunicación médica.", "type": "estándar", "url": "https://www.dicomstandard.org/current"},
            {"title": "NIBIB Science Topics", "description": "Introducciones oficiales a modalidades y tecnologías de imagen biomédica.", "type": "recurso educativo", "url": "https://www.nibib.nih.gov/science-education/science-topics"},
            {"title": "The Cancer Imaging Archive", "description": "Colecciones públicas de imágenes oncológicas para investigación y docencia.", "type": "datos abiertos", "url": "https://www.cancerimagingarchive.net/"},
        ]
    if subject_id in informatics:
        return [
            {"title": "HL7 FHIR Specification", "description": "Especificación oficial para intercambio de información sanitaria.", "type": "estándar", "url": "https://hl7.org/fhir/"},
            {"title": "SNOMED CT", "description": "Información oficial sobre la terminología clínica internacional.", "type": "terminología", "url": "https://www.snomed.org/"},
            {"title": "LOINC", "description": "Estándar para identificar mediciones, observaciones y documentos clínicos.", "type": "terminología", "url": "https://loinc.org/"},
            {"title": "WHO Digital Health", "description": "Recursos de la OMS sobre estrategia, gobernanza y salud digital.", "type": "recurso institucional", "url": "https://www.who.int/health-topics/digital-health"},
            {"title": "PhysioNet", "description": "Datos clínicos y fisiológicos abiertos para aprendizaje y validación.", "type": "datos abiertos", "url": "https://physionet.org/"},
        ]
    if area_id == "biologicas-medicas":
        return [
            {"title": "OpenStax Biology 2e", "description": "Texto abierto para fundamentos celulares, genéticos y fisiológicos.", "type": "libro abierto", "url": "https://openstax.org/details/books/biology-2e"},
            {"title": "NCBI Bookshelf", "description": "Biblioteca pública de libros y capítulos biomédicos.", "type": "biblioteca", "url": "https://www.ncbi.nlm.nih.gov/books/"},
            {"title": "PubMed", "description": "Buscador de literatura biomédica para ampliar y contrastar contenidos.", "type": "literatura", "url": "https://pubmed.ncbi.nlm.nih.gov/"},
            {"title": "EMBL-EBI Training", "description": "Cursos abiertos sobre biología molecular, datos y bioinformática.", "type": "cursos abiertos", "url": "https://www.ebi.ac.uk/training/"},
            {"title": "Human Protein Atlas", "description": "Datos abiertos de expresión y localización de proteínas humanas.", "type": "atlas", "url": "https://www.proteinatlas.org/"},
        ]
    if area_id == "gestion-etica-comunicacion":
        return [
            {"title": "World Health Organization", "description": "Informes, políticas y recursos institucionales sobre salud global.", "type": "fuente institucional", "url": "https://www.who.int/"},
            {"title": "UNESCO Bioethics", "description": "Instrumentos y recursos sobre ética de ciencia, tecnología y salud.", "type": "recurso institucional", "url": "https://www.unesco.org/en/ethics-science-technology/bioethics"},
            {"title": "EQUATOR Network", "description": "Guías de reporte para investigación en salud.", "type": "guías", "url": "https://www.equator-network.org/"},
            {"title": "Committee on Publication Ethics", "description": "Orientación sobre integridad, autoría y publicación científica.", "type": "guías", "url": "https://publicationethics.org/"},
            {"title": "OECD Science, Technology and Innovation", "description": "Datos y análisis de políticas de ciencia, tecnología e innovación.", "type": "fuente institucional", "url": "https://www.oecd.org/sti/"},
        ]
    return [
        {"title": "MIT OpenCourseWare", "description": "Cursos abiertos de ciencias e ingeniería para reforzar fundamentos.", "type": "cursos abiertos", "url": "https://ocw.mit.edu/"},
        {"title": "NIBIB Science Topics", "description": "Recursos oficiales sobre tecnologías biomédicas y sus aplicaciones.", "type": "recurso educativo", "url": "https://www.nibib.nih.gov/science-education/science-topics"},
        {"title": "FDA CDRH Learn", "description": "Módulos oficiales sobre dispositivos médicos, calidad y regulación.", "type": "formación oficial", "url": "https://www.fda.gov/training-and-continuing-education/cdrh-learn"},
        {"title": "WHO Medical Devices", "description": "Recursos sobre selección, gestión y acceso a dispositivos médicos.", "type": "recurso institucional", "url": "https://www.who.int/health-topics/medical-devices"},
        {"title": "PhysioNet", "description": "Datos fisiológicos abiertos para docencia, análisis y validación.", "type": "datos abiertos", "url": "https://physionet.org/"},
    ]


def related_subjects_for(subject_id: str, area_id: str) -> list[str]:
    catalog = subject_catalog()
    current_families = [family for family in COURSE_FAMILIES if subject_id in family]
    ranked: list[tuple[int, int, str]] = []
    for candidate_id, candidate in catalog.items():
        if candidate_id == subject_id:
            continue
        shared_families = sum(candidate_id in family for family in current_families)
        same_area = candidate["area_id"] == area_id
        if not shared_families and not same_area:
            continue
        score = shared_families * 10 + int(same_area)
        ranked.append((-score, candidate["order"], candidate_id))
    ranked.sort()
    result: list[str] = []
    for _, _, candidate_id in ranked:
        candidate = catalog[candidate_id]
        result.append(f"{candidate['title']}: {candidate['description']}")
        if len(result) == 6:
            break
    return result


def synthesize_course(area: dict[str, Any], subject: dict[str, Any]) -> dict[str, Any]:
    outlines = load_outlines()
    try:
        raw_units = outlines[area["id"]][subject["id"]]
    except KeyError as exc:
        raise ValueError(f"Falta temario para {area['id']}/{subject['id']} en {OUTLINES_PATH.relative_to(ROOT)}") from exc

    title = subject["title"]
    connection = subject["biomedical_connection"]
    units: list[dict[str, Any]] = []
    concepts: list[str] = []
    for number, raw_unit in enumerate(raw_units, start=1):
        if len(raw_unit) != 3:
            raise ValueError(f"Unidad inválida en {area['id']}/{subject['id']}: se esperaban título, temas y aplicación")
        unit_title, topic_text, application = raw_unit
        topics = [topic.strip() for topic in topic_text.split(";") if topic.strip()]
        if len(topics) < 3:
            raise ValueError(f"La unidad {number} de {area['id']}/{subject['id']} requiere al menos tres temas")
        concepts.extend([unit_title, *topics])
        units.append({
            "unit": number,
            "title": unit_title,
            "description": (
                f"Desarrolla {', '.join(topics[:-1])} y {topics[-1]}, conectando los fundamentos "
                f"de {title} con problemas verificables y decisiones propias del ámbito biomédico."
            ),
            "topics": [topic[0].upper() + topic[1:] + "." for topic in topics],
            "learning_outcomes": [
                f"Explicar las relaciones principales entre {', '.join(topics)}.",
                f"Aplicar estos conceptos a un caso relacionado con {application}.",
            ],
            "activities": [
                f"Construir un esquema razonado de {unit_title.lower()} que identifique variables, relaciones y supuestos.",
                f"Resolver y documentar un caso breve sobre {application}, indicando evidencia necesaria y limitaciones.",
            ],
            "biomedical_applications": [
                application[0].upper() + application[1:] + ".",
                connection,
            ],
        })

    modules = [f"{unit['title']}: {'; '.join(item.rstrip('.') for item in unit['topics'])}." for unit in units]
    practical_activities = [
        {
            "title": f"Taller {number}: {unit['title']}",
            "description": (
                f"Producto individual o colaborativo que integra {', '.join(topic.rstrip('.').lower() for topic in unit['topics'])}; "
                "debe documentar procedimiento, supuestos, resultados y limitaciones."
            ),
            "type": "actividad aplicada",
        }
        for number, unit in enumerate(units, start=1)
    ]
    return {
        **subject,
        "status": "review",
        "level": (
            "Pregrado universitario inicial e intermedio"
            if area["id"] == "ciencias-basicas"
            else "Pregrado universitario intermedio y avanzado"
        ),
        "estimated_workload": "16 semanas; 6-8 horas semanales; 120-150 horas totales de estudio, práctica y evaluación",
        "prerequisites": prerequisites_for(area["id"], subject["id"]),
        "course_competencies": [
            f"Explicar con precisión los principios, métodos y límites de {title}.",
            f"Aplicar herramientas de {title} a preguntas científicas, tecnológicas o sanitarias bien definidas.",
            "Interpretar datos, modelos, mediciones o argumentos distinguiendo resultado, inferencia y limitación.",
            "Seleccionar métodos y recursos apropiados, justificando supuestos, criterios de calidad y riesgos.",
            "Integrar fundamentos cuantitativos, biológicos, técnicos y éticos en problemas biomédicos.",
            "Comunicar procedimientos y conclusiones de forma clara, trazable y reproducible.",
        ],
        "learning_objectives": [
            f"Comprender el vocabulario, los modelos y los principios fundamentales de {title}.",
            "Relacionar los contenidos de las unidades en una visión progresiva y coherente del campo.",
            "Resolver problemas aplicados documentando datos, supuestos, procedimientos y comprobaciones.",
            "Interpretar evidencia y resultados sin confundir asociación, predicción, mecanismo o causalidad.",
            f"Conectar {title} con necesidades reales de investigación, tecnología, salud y enfermedad.",
            "Desarrollar autonomía para continuar aprendiendo con fuentes abiertas y documentación primaria.",
        ],
        "learning_outcomes": [
            *[
                f"Describir y aplicar los conceptos de {unit['title'].lower()} en un ejercicio o caso biomédico."
                for unit in units
            ],
            "Comparar al menos dos métodos o explicaciones, justificando su elección con criterios explícitos.",
            "Entregar un análisis reproducible que incluya procedimiento, resultados, incertidumbre y limitaciones.",
        ],
        "modules": modules,
        "detailed_units": units,
        "practical_activities": practical_activities,
        "assessment": [
            {"title": "Pruebas conceptuales", "description": "Problemas breves que evalúan comprensión, relaciones entre conceptos y detección de errores frecuentes.", "weight": "20%"},
            {"title": "Talleres aplicados", "description": "Entregas de las unidades con procedimiento, comprobaciones, resultados y reflexión sobre limitaciones.", "weight": "25%"},
            {"title": "Análisis de evidencia", "description": "Lectura crítica de datos, figuras, métodos o casos relevantes para la asignatura.", "weight": "20%"},
            {"title": "Proyecto integrador", "description": f"Resolución documentada de un problema de {title} conectado con una aplicación biomédica realista.", "weight": "25%"},
            {"title": "Comunicación y bitácora", "description": "Presentación clara del trabajo y registro de decisiones, dudas, correcciones y aprendizajes.", "weight": "10%"},
        ],
        "key_concepts": unique_strings(concepts, limit=24),
        "related_subjects": related_subjects_for(subject["id"], area["id"]),
        "suggested_resources": resources_for(area["id"], subject["id"]),
    }


def escape(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def normalize_output(value: str) -> str:
    """Normaliza espacios finales y garantiza un único salto de línea al final."""
    return "\n".join(line.rstrip() for line in value.splitlines()).rstrip() + "\n"


def rel_path(from_file: Path, to_file: Path) -> str:
    """Devuelve una ruta relativa POSIX desde un HTML generado hacia otro archivo."""
    start_dir = from_file.parent
    return Path(os.path.relpath(to_file, start=start_dir)).as_posix()


def render_list(items: list[Any], empty_message: str) -> str:
    if not items:
        return f'<p class="muted">{escape(empty_message)}</p>'
    rendered = "\n".join(f"        <li>{escape(item)}</li>" for item in items)
    return f"<ul>\n{rendered}\n      </ul>"


def render_key_value_list(items: list[dict[str, Any]], empty_message: str) -> str:
    if not items:
        return f'<p class="muted">{escape(empty_message)}</p>'
    rendered_items = []
    for item in items:
        title = escape(item.get("title", item.get("name", "Elemento")))
        description = escape(item.get("description", ""))
        extra = escape(item.get("weight", item.get("type", "")))
        url = str(item.get("url", "")).strip()
        if url.startswith(("https://", "http://")):
            title_html = f'<a class="resource-link" href="{escape(url)}">{title}</a>'
        else:
            title_html = title
        meta = f'<span class="course-tag">{extra}</span>' if extra else ""
        rendered_items.append(
            "        <li>"
            f"<strong>{title_html}</strong>{meta}"
            f"<p>{description}</p>"
            "</li>"
        )
    return '<ul class="rich-list">\n' + "\n".join(rendered_items) + "\n      </ul>"


def render_units(units: list[dict[str, Any]], empty_message: str) -> str:
    if not units:
        return f'<p class="muted">{escape(empty_message)}</p>'
    rendered_units = []
    for unit in units:
        number = escape(unit.get("unit", ""))
        title = escape(unit.get("title", "Unidad"))
        description = escape(unit.get("description", ""))
        topics = render_list(unit.get("topics", []), "Temas pendientes.")
        outcomes = render_list(unit.get("learning_outcomes", []), "Resultados pendientes.")
        activities = render_list(unit.get("activities", []), "Actividades pendientes.")
        applications = render_list(unit.get("biomedical_applications", []), "Aplicaciones pendientes.")
        rendered_units.append(
            "      <article class=\"course-unit\">\n"
            f"        <h3>Unidad {number}. {title}</h3>\n"
            f"        <p>{description}</p>\n"
            "        <h4>Temas</h4>\n"
            f"        {topics}\n"
            "        <h4>Resultados esperados</h4>\n"
            f"        {outcomes}\n"
            "        <h4>Actividades</h4>\n"
            f"        {activities}\n"
            "        <h4>Aplicaciones biomédicas</h4>\n"
            f"        {applications}\n"
            "      </article>"
        )
    return '<div class="course-units">\n' + "\n".join(rendered_units) + "\n      </div>"


def subject_neighbors(subjects: list[dict[str, Any]], index: int) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    previous_subject = subjects[index - 1] if index > 0 else None
    next_subject = subjects[index + 1] if index < len(subjects) - 1 else None
    return previous_subject, next_subject


def render_nav_link(
    current_file: Path,
    subject: dict[str, Any] | None,
    label_prefix: str,
    css_class: str,
    label_suffix: str = "",
) -> str:
    if subject is None:
        return ""
    target = ROOT / subject["path"]
    href = rel_path(current_file, target)
    title = escape(subject.get("title", subject.get("id", "Asignatura")))
    css_classes = f"btn-link {css_class}".strip()
    label = f"{label_prefix} {title} {label_suffix}".strip()
    return f'<a class="{css_classes}" href="{href}">{label}</a>'


def validate_template(template: str) -> None:
    missing = [key for key in REQUIRED_TEMPLATE_KEYS if "{{ " + key + " }}" not in template]
    if missing:
        raise ValueError("La plantilla no contiene estas variables requeridas: " + ", ".join(sorted(missing)))


def validate_area_template(template: str) -> None:
    missing = [key for key in REQUIRED_AREA_TEMPLATE_KEYS if "{{ " + key + " }}" not in template]
    if missing:
        raise ValueError("La plantilla de área no contiene estas variables requeridas: " + ", ".join(sorted(missing)))


def subject_overlay_path(area_id: str, subject_id: str) -> Path:
    return SUBJECT_DATA_DIR / area_id / f"{subject_id}.json"


def merge_subject_overlay(area: dict[str, Any], subject: dict[str, Any]) -> dict[str, Any]:
    """Combina metadatos centrales con contenido editorial opcional por asignatura."""
    merged = synthesize_course(area, subject)
    overlay_path = subject_overlay_path(area["id"], subject["id"])
    if not overlay_path.exists():
        merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])
        return merged

    overlay = load_json(overlay_path)
    if overlay.get("id") != subject["id"]:
        raise ValueError(f"Overlay con id inconsistente en {overlay_path.relative_to(ROOT)}")
    if overlay.get("area_id") != area["id"]:
        raise ValueError(f"Overlay con area_id inconsistente en {overlay_path.relative_to(ROOT)}")

    list_minimums = {
        "prerequisites": 3,
        "course_competencies": 4,
        "learning_objectives": 4,
        "learning_outcomes": 6,
        "modules": 6,
        "detailed_units": 6,
        "practical_activities": 4,
        "assessment": 3,
        "key_concepts": 10,
        "related_subjects": 4,
        "suggested_resources": 5,
    }
    for key, value in overlay.items():
        if key in {"id", "area_id"} or value in (None, "", []):
            continue
        minimum = list_minimums.get(key)
        if minimum is not None and isinstance(value, list) and len(value) < minimum:
            combined = list(value)
            seen = {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in combined}
            for item in merged.get(key, []):
                marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if marker not in seen:
                    combined.append(item)
                    seen.add(marker)
                if len(combined) >= minimum:
                    break
            merged[key] = combined
        else:
            merged[key] = value
    if merged.get("status") in {"placeholder", "draft"}:
        merged["status"] = "review"
    merged["status_label"] = STATUS_LABELS.get(merged["status"], merged["status"])
    return merged


def render_subject(template: str, area: dict[str, Any], subject: dict[str, Any], subjects: list[dict[str, Any]], index: int) -> str:
    subject = merge_subject_overlay(area, subject)
    output_path = ROOT / subject["path"]
    home_path = rel_path(output_path, ROOT / "index.html")
    area_path = rel_path(output_path, ROOT / area["path"])
    css_path = rel_path(output_path, ROOT / "assets" / "css" / "style.css")
    editorial_css_path = rel_path(output_path, ROOT / "assets" / "css" / "editorial.css")
    previous_subject, next_subject = subject_neighbors(subjects, index)

    replacements = {
        "subject_title": escape(subject.get("title", subject.get("id", "Asignatura"))),
        "area_title": escape(area.get("title", area.get("id", "Área"))),
        "subject_description": escape(subject.get("description", "Página de asignatura de CitoNauta Biomedicina.")),
        "css_path": css_path,
        "editorial_css_path": editorial_css_path,
        "home_path": home_path,
        "area_path": area_path,
        "previous_link": render_nav_link(output_path, previous_subject, "←", "secondary"),
        "next_link": render_nav_link(output_path, next_subject, "", "", "→"),
        "biomedical_connection": escape(subject.get("biomedical_connection", "Conexión biomédica pendiente de desarrollo.")),
        "level": escape(subject.get("level", "Pregrado universitario")),
        "estimated_workload": escape(subject.get("estimated_workload", "12-16 semanas; 90-150 horas de trabajo total")),
        "status": escape(subject.get("status", "placeholder")),
        "status_label": escape(subject.get("status_label", STATUS_LABELS["placeholder"])),
        "prerequisites": render_list(subject.get("prerequisites", []), "Prerrequisitos pendientes de desarrollo."),
        "course_competencies": render_list(subject.get("course_competencies", []), "Competencias pendientes de desarrollo."),
        "learning_objectives": render_list(subject.get("learning_objectives", []), "Objetivos de aprendizaje pendientes de desarrollo."),
        "learning_outcomes": render_list(subject.get("learning_outcomes", []), "Resultados de aprendizaje pendientes de desarrollo."),
        "modules": render_list(subject.get("modules", []), "Módulos pendientes de desarrollo."),
        "detailed_units": render_units(subject.get("detailed_units", []), "Unidades detalladas pendientes de desarrollo."),
        "practical_activities": render_key_value_list(subject.get("practical_activities", []), "Actividades prácticas pendientes de desarrollo."),
        "assessment": render_key_value_list(subject.get("assessment", []), "Evaluación sugerida pendiente de desarrollo."),
        "key_concepts": render_list(subject.get("key_concepts", []), "Conceptos clave pendientes de desarrollo."),
        "related_subjects": render_list(subject.get("related_subjects", []), "Relaciones curriculares pendientes de desarrollo."),
        "suggested_resources": render_key_value_list(subject.get("suggested_resources", []), "Recursos sugeridos pendientes de desarrollo."),
    }

    html_output = template
    for key, value in replacements.items():
        html_output = html_output.replace("{{ " + key + " }}", value)
    return html_output


def render_area(template: str, area: dict[str, Any]) -> str:
    output_path = ROOT / area["path"]
    cards: list[str] = []
    for subject in area.get("subjects", []):
        complete_subject = merge_subject_overlay(area, subject)
        href = rel_path(output_path, ROOT / subject["path"])
        title = escape(complete_subject.get("title", subject["title"]))
        description = escape(complete_subject.get("description", subject["description"]))
        status_label = "Curso completo" if complete_subject.get("status") in {"review", "complete"} else "En desarrollo"
        cards.append(
            f'      <a class="link-card course-card" href="{href}">\n'
            f"        <strong>{title}</strong>\n"
            f"        <p>{description}</p>\n"
            f'        <span class="course-tag">{status_label}</span>\n'
            "      </a>"
        )
    replacements = {
        "area_title": escape(area["title"]),
        "area_description": escape(area["description"]),
        "css_path": rel_path(output_path, ROOT / "assets" / "css" / "style.css"),
        "editorial_css_path": rel_path(output_path, ROOT / "assets" / "css" / "editorial.css"),
        "home_path": rel_path(output_path, ROOT / "index.html"),
        "subject_count": str(len(area.get("subjects", []))),
        "subject_cards": "\n".join(cards),
    }
    html_output = template
    for key, value in replacements.items():
        html_output = html_output.replace("{{ " + key + " }}", value)
    return html_output


def iter_subjects(data: dict[str, Any]):
    for area in data.get("areas", []):
        subjects = area.get("subjects", [])
        for index, subject in enumerate(subjects):
            yield area, subjects, index, subject


def should_include_subject(subject: dict[str, Any], only_subjects: set[str]) -> bool:
    if not only_subjects:
        return True
    return subject.get("id") in only_subjects or subject.get("path") in only_subjects


def generate(dry_run: bool, force: bool, only_missing: bool, only_subjects: set[str]) -> dict[str, int]:
    data = load_json(DATA_PATH)
    template = load_template(TEMPLATE_PATH)
    area_template = load_template(AREA_TEMPLATE_PATH)
    validate_template(template)
    validate_area_template(area_template)
    summary = {
        "generated": 0,
        "generated_areas": 0,
        "skipped_existing": 0,
        "skipped_existing_areas": 0,
        "skipped_filter": 0,
        "would_generate": 0,
        "would_generate_areas": 0,
        "errors": 0,
    }

    for area, subjects, index, subject in iter_subjects(data):
        if not should_include_subject(subject, only_subjects):
            summary["skipped_filter"] += 1
            continue

        target_path = ROOT / subject["path"]
        exists = target_path.exists()

        if exists and only_missing:
            summary["skipped_existing"] += 1
            continue
        if exists and not force:
            summary["skipped_existing"] += 1
            continue

        rendered = render_subject(template, area, subject, subjects, index)

        if dry_run:
            print(f"[dry-run] generaría: {target_path.relative_to(ROOT)}")
            summary["would_generate"] += 1
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(normalize_output(rendered), encoding="utf-8")
        print(f"[ok] generado: {target_path.relative_to(ROOT)}")
        summary["generated"] += 1

    if not only_subjects:
        for area in data.get("areas", []):
            target_path = ROOT / area["path"]
            if target_path.exists() and not force:
                summary["skipped_existing_areas"] += 1
                continue
            rendered = render_area(area_template, area)
            if dry_run:
                print(f"[dry-run] generaría área: {target_path.relative_to(ROOT)}")
                summary["would_generate_areas"] += 1
                continue
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(normalize_output(rendered), encoding="utf-8")
            print(f"[ok] generada área: {target_path.relative_to(ROOT)}")
            summary["generated_areas"] += 1

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera páginas HTML de asignaturas para CitoNauta.")
    parser.add_argument("--dry-run", action="store_true", help="Muestra qué se generaría sin escribir archivos.")
    parser.add_argument("--force", action="store_true", help="Sobrescribe páginas existentes. Usar solo con revisión previa.")
    parser.add_argument("--only-missing", action="store_true", help="Genera solo páginas que no existan.")
    parser.add_argument("--subject", action="append", default=[], help="Genera solo una asignatura por id o ruta. Puede repetirse.")
    args = parser.parse_args()

    summary = generate(
        dry_run=args.dry_run,
        force=args.force,
        only_missing=args.only_missing,
        only_subjects=set(args.subject),
    )
    print("\nResumen:")
    for key, value in summary.items():
        print(f"- {key}: {value}")

    if not args.force:
        print("\nModo seguro activo: las páginas existentes no se sobrescriben sin --force.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
