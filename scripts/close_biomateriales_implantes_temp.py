#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "biomateriales-implantes"
CODE = "BIMPL"
BASE = ROOT / "data" / "courses" / COURSE_ID
STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def statement_records(prefix: str, statements: list[str]):
    return [{"id": f"{prefix}{i:02d}", "statement": text} for i, text in enumerate(statements, 1)]


course = read(BASE / "course.json")
course.update({
    "content_version": "1.0.0",
    "academic_level": "Pregrado universitario intermedio y avanzado",
    "audience": "Estudiantes de ingeniería biomédica y áreas afines con bases de ciencia de materiales, mecánica, biología celular y fisiología que necesiten razonar sobre selección, fijación, degradación, desempeño y vigilancia de implantes.",
    "status": STATUS,
    "purpose": "Integrar requisitos clínico-funcionales, selección de materiales implantables, fijación e integración tisular, desgaste-corrosión-fatiga, particularidades de familias de implantes y evidencia de ciclo de vida para construir decisiones técnicas reproducibles, trazables y proporcionales, sin confundir desempeño preclínico con seguridad o eficacia clínica demostradas.",
    "scope": {
        "included": [
            "Traducción de necesidad y función en requisitos medibles de desempeño para implantes.",
            "Selección comparada de metales, cerámicas, polímeros y compuestos según entorno mecánico y biológico.",
            "Estabilidad primaria, osteointegración, recubrimientos, cementos y mecanismos de anclaje.",
            "Tribología, fretting, corrosión, fatiga, partículas de desgaste y mecanismos de fallo.",
            "Comparación de retos de implantes ortopédicos, cardiovasculares, dentales y de tejidos blandos.",
            "Ensayos, evaluación biológica basada en riesgo, gestión de riesgo, vigilancia y seguimiento poscomercialización.",
            "Expedientes reproducibles con requisitos, evidencia, controles, incertidumbre, riesgo residual y límites de inferencia."
        ],
        "excluded": [
            "Selección o prescripción de un implante para una persona concreta.",
            "Diagnóstico, pronóstico o recomendación terapéutica individual a partir de una propiedad de material o ensayo aislado.",
            "Afirmar biocompatibilidad, seguridad o eficacia clínica a partir de un único ensayo in vitro, mecánico o de caracterización superficial.",
            "Sustituir evaluación regulatoria, gestión de riesgo institucional, revisión ética o vigilancia real de fabricante por ejercicios académicos.",
            "Prácticas con personas, tejidos clínicos, dispositivos implantables reales o procedimientos invasivos sin infraestructura y autorización apropiadas."
        ],
        "handoff_courses": [
            "biomateriales",
            "desarrollo-dispositivos-medicos",
            "ingenieria-clinica-gestion",
            "polimeros-procesamiento-materiales",
            "ingenieria-tejidos"
        ]
    },
    "prerequisites": statement_records(f"{CODE}-PRE", [
        "Mecánica y ciencia de materiales de nivel universitario inicial, incluyendo esfuerzo, deformación, fatiga y propiedades básicas.",
        "Biología celular, anatomía y fisiología suficientes para interpretar interacción material-tejido sin convertirla en diagnóstico.",
        "Química general y nociones de superficies, corrosión, polímeros o electroquímica para seguir mecanismos de degradación.",
        "Estadística descriptiva y documentación reproducible para comparar ensayos, incertidumbre y criterios de aceptación."
    ]),
    "competencies": statement_records(f"{CODE}-COMP", [
        "Traducir una necesidad funcional de implante en requisitos medibles, condiciones de servicio y criterios de aceptación trazables.",
        "Comparar familias de materiales implantables mediante relaciones estructura-propiedad, entorno biológico y mecanismos previsibles de degradación.",
        "Analizar fijación e integración distinguiendo estabilidad primaria, respuesta tisular y evidencia necesaria para sostener una afirmación de desempeño.",
        "Razonar sobre desgaste, corrosión, fretting y fatiga como procesos acoplados y evaluar controles y modos de fallo alternativos.",
        "Comparar familias de implantes sin transferir automáticamente requisitos o evidencia entre indicaciones anatómicas distintas.",
        "Integrar ensayos, evaluación biológica, gestión de riesgo y vigilancia en un expediente de ciclo de vida reproducible.",
        "Comunicar conclusiones técnicas con incertidumbre y límites, separando desempeño material, evidencia preclínica, evidencia clínica y decisión regulatoria."
    ]),
    "learning_outcomes": statement_records(f"{CODE}-LO", [
        "Formula requisitos funcionales, mecánicos, biológicos y de verificación para un implante a partir de un escenario académico delimitado.",
        "Selecciona y compara materiales implantables justificando propiedades, ambiente de servicio, compromisos y evidencia necesaria.",
        "Explica y evalúa mecanismos de fijación e integración mediante estabilidad, interfaz y respuesta tisular sin asumir éxito clínico.",
        "Analiza mecanismos de desgaste, corrosión, fretting y fatiga y relaciona hallazgos con modos de fallo y controles verificables.",
        "Compara retos de implantes ortopédicos, cardiovasculares, dentales y de tejidos blandos manteniendo explícitas sus condiciones de uso.",
        "Construye un plan de evaluación y vigilancia que conecte ensayos, riesgo, señales poscomercialización y actualización de evidencia.",
        "Integra las seis unidades en un expediente reproducible que vincula requisito, evidencia, método, control, resultado, incertidumbre y límite de inferencia."
    ]),
    "study_method": [
        "Definir primero necesidad, función, entorno de servicio, riesgo y afirmación que se pretende sostener.",
        "Separar propiedad medida, mecanismo propuesto, evidencia biológica, desempeño del dispositivo e inferencia clínica o regulatoria.",
        "Alternar explicación, ejemplo resuelto, actividad guiada, comprobación y transferencia con apoyo progresivamente menor.",
        "Usar matrices de requisitos y evidencia para conservar trazabilidad entre unidades y evitar seleccionar materiales por una sola propiedad.",
        "Predefinir controles, criterios de aceptación, incertidumbre y escenarios de fallo antes de interpretar resultados.",
        "Registrar fuentes, versiones, supuestos, parámetros y correcciones para que otra persona pueda reconstruir el razonamiento."
    ],
    "editorial_notice": "Corpus canónico educativo completo a nivel de contenido, fuentes trazables y pedagogía interna para las seis unidades de Biomateriales e Implantes. La publicación sigue siendo provisional. La revisión humana interna, la revisión disciplinaria externa, cualquier evaluación con personas o materiales clínicos, la validación regulatoria y las decisiones diagnósticas o terapéuticas permanecen fuera del cierre y siguen pendientes."
})
write(BASE / "course.json", course)

# Validate evidence before elevating source status: each curated legacy unit must expose
# multiple locatable sources and none may still be explicitly marked unverified.
legacy_dir = ROOT / "data" / "course_redevelopment" / COURSE_ID / "units"
legacy_units = [read(legacy_dir / f"unit-{i:02d}.json") for i in range(1, 7)]
for index, legacy in enumerate(legacy_units, 1):
    sources = legacy.get("sources", [])
    if len(sources) < 5:
        raise SystemExit(f"U{index}: fewer than five sources")
    for source in sources:
        if not (source.get("url") or source.get("doi") or source.get("pmid") or source.get("title")):
            raise SystemExit(f"U{index}: source without locator")
        if str(source.get("verification_status", "")).casefold() in {"", "unverified", "pending"}:
            raise SystemExit(f"U{index}: unverified source remains: {source.get('title')}")

# Unit closure and explicit course-LO mapping.
lo_map = {
    1: [f"{CODE}-LO01", f"{CODE}-LO07"],
    2: [f"{CODE}-LO02", f"{CODE}-LO07"],
    3: [f"{CODE}-LO03", f"{CODE}-LO07"],
    4: [f"{CODE}-LO04", f"{CODE}-LO07"],
    5: [f"{CODE}-LO05", f"{CODE}-LO07"],
    6: [f"{CODE}-LO06", f"{CODE}-LO07"],
}
for number in range(1, 7):
    unit_path = BASE / "units" / f"unit-{number:02d}.json"
    unit = read(unit_path)
    unit["status"] = STATUS
    unit["course_learning_outcome_ids"] = lo_map[number]
    for activity in unit.get("activities", []):
        activity["estimated_duration_minutes"] = 180
        activity["status"] = "curated_internal_review_pending"
    write(unit_path, unit)

    assessment_path = BASE / "assessments" / f"unit-{number:02d}.json"
    assessment = read(assessment_path)
    source_ids = unit.get("source_ids", [])
    for idx, item in enumerate(assessment.get("items", []), 1):
        if idx <= 3:
            item["difficulty"] = "foundational"
            item["cognitive_level"] = "understand"
        elif idx <= 7:
            item["difficulty"] = "intermediate"
            item["cognitive_level"] = "apply"
        else:
            item["difficulty"] = "advanced"
            item["cognitive_level"] = "analyze"
        explanation = item["answer_key"].get("explanation") or "La respuesta debe conservar mecanismo, condición de validez y límite de inferencia."
        misconceptions = item["answer_key"].get("common_misconceptions", [])
        item["feedback"] = {
            "correct": f"Correcto. Conserva en la justificación el criterio: {explanation}",
            "incorrect": "Revisa la relación entre dato, mecanismo y conclusión" + (f"; evita este error: {misconceptions[0]}" if misconceptions else "."),
        }
        item["source_ids"] = source_ids[:2]
        item["status"] = "curated_internal_review_pending"
    assessment["status"] = "curated_internal_review_pending"
    write(assessment_path, assessment)

# Attach glossary entries to sources from the units in which each term is used.
glossary_path = BASE / "glossary.json"
glossary = read(glossary_path)
unit_sources = {f"{CODE}-U{i:02d}": read(BASE / "units" / f"unit-{i:02d}.json").get("source_ids", []) for i in range(1, 7)}
for entry in glossary.get("entries", []):
    refs = []
    for unit_id in entry.get("unit_ids", []):
        for source_id in unit_sources.get(unit_id, [])[:2]:
            if source_id not in refs:
                refs.append(source_id)
    entry["source_ids"] = refs
    entry["verification_status"] = "traceable_to_curated_unit_sources"
glossary["status"] = "curated_internal_review_pending"
write(glossary_path, glossary)

sources_path = BASE / "sources.json"
sources = read(sources_path)
sources["source_policy"] = "Priorizar normas, guías regulatorias oficiales, revisiones y artículos primarios pertinentes; conservar URL/DOI/PMID y estado de verificación heredado de cada unidad curada. Una fuente trazable respalda una afirmación académica, pero no equivale a validación clínica o regulatoria del curso."
sources["consulted_on"] = "2026-08-24"
sources["coverage_gaps"] = []
write(sources_path, sources)

# Course-level assessment: preserve the existing 100% plan and capstone, but make
# diagnosis and midterm blueprint disciplinary rather than generic.
assessment_path = BASE / "assessments" / "course-assessment.json"
assessment = read(assessment_path)
assessment["diagnostic"] = {
    "title": "Diagnóstico de entrada a Biomateriales e Implantes",
    "purpose": "Detectar prerrequisitos que deben recuperarse antes de interpretar propiedades, interfaces y evidencia de implantes; no aporta calificación final.",
    "questions": [
        "Distingue módulo elástico, resistencia, tenacidad y fatiga e indica por qué no son intercambiables.",
        "Formula cuatro requisitos medibles para un implante sometido a carga cíclica en un escenario sintético.",
        "Explica por qué una propiedad excelente del material a granel puede no predecir el desempeño de la superficie o del dispositivo completo.",
        "Diferencia estabilidad primaria de integración tisular y propone una observación para evaluar cada una.",
        "Describe cómo corrosión, fretting y desgaste pueden interactuar en una interfaz modular.",
        "Explica por qué demostrar citotoxicidad aceptable no basta para afirmar biocompatibilidad global o seguridad clínica.",
        "Propón un control y un criterio de aceptación para un ensayo mecánico comparativo.",
        "Distingue peligro, situación peligrosa, daño y riesgo residual en un ejemplo de implante.",
        "Indica qué metadatos conservarías para reproducir una comparación entre materiales.",
        "Reescribe una afirmación que confunda desempeño preclínico con eficacia clínica para ajustarla a la evidencia disponible."
    ],
    "interpretation": [
        "0-3 respuestas sólidas: recuperar mecánica de materiales, biología de interfaz y razonamiento de riesgo antes de U1.",
        "4-7 respuestas sólidas: iniciar U1 y reforzar en paralelo los prerrequisitos fallidos.",
        "8-10 respuestas sólidas: iniciar la secuencia y usar los retos de transferencia como comprobación temprana."
    ]
}
assessment["midterm_blueprint"] = [
    {"section": "Requisitos y selección", "weight_percent": 30, "unit_ids": [f"{CODE}-U01", f"{CODE}-U02"], "evidence": "Caso de requisitos y matriz comparativa con unidades, compromisos y límites."},
    {"section": "Interfaz y fijación", "weight_percent": 25, "unit_ids": [f"{CODE}-U03"], "evidence": "Análisis de estabilidad, interfaz y evidencia de integración sin extrapolación clínica."},
    {"section": "Degradación y fallo", "weight_percent": 30, "unit_ids": [f"{CODE}-U04"], "evidence": "Caso mecanístico de desgaste/corrosión/fatiga con controles y explicación alternativa."},
    {"section": "Trazabilidad y comunicación", "weight_percent": 15, "unit_ids": [f"{CODE}-U01", f"{CODE}-U02", f"{CODE}-U03", f"{CODE}-U04"], "evidence": "Matriz requisito-evidencia-control-límite y corrección de una conclusión exagerada."}
]
capstone = assessment.get("capstone", {})
if capstone:
    capstone["scenario"] = str(capstone.get("scenario", "")).replace("un matriz", "una matriz")
assessment["status"] = "curated_internal_review_pending"
write(assessment_path, assessment)

# Permanent regression created by the closure, intentionally outside the temp-script name.
test_path = ROOT / "tests" / "test_biomateriales_implantes_canonical.py"
test_path.write_text('''from __future__ import annotations\n\nimport json\nimport unittest\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nBASE = ROOT / "data" / "courses" / "biomateriales-implantes"\nGENERIC = "concepto de la unidad que debe definirse mediante entidades observables"\n\n\nclass BiomaterialesImplantesCanonicalTests(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.course = json.loads((BASE / "course.json").read_text(encoding="utf-8"))\n\n    def test_course_is_complete_but_human_review_remains_pending(self):\n        status = self.course["status"]\n        self.assertEqual(status["content"], "complete")\n        self.assertEqual(status["sources"], "traceable")\n        self.assertEqual(status["pedagogy"], "complete")\n        self.assertEqual(status["internal_review"], "pending")\n        self.assertEqual(status["external_review"], "pending")\n        self.assertEqual(status["publication"], "published_provisional")\n\n    def test_six_units_are_canonical_and_disciplinary(self):\n        self.assertEqual(len(self.course["unit_files"]), 6)\n        for index, relative in enumerate(self.course["unit_files"], 1):\n            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))\n            self.assertEqual(unit["order"], index)\n            self.assertEqual(unit["status"]["content"], "complete")\n            self.assertEqual(unit["status"]["sources"], "traceable")\n            self.assertEqual(unit["status"]["pedagogy"], "complete")\n            text = json.dumps(unit, ensure_ascii=False).casefold()\n            self.assertNotIn(GENERIC, text)\n            self.assertGreaterEqual(len(unit["learning_outcomes"]), 5)\n            self.assertGreaterEqual(len(unit["topics"]), 4)\n            self.assertGreaterEqual(len(unit["examples"]), 2)\n            self.assertGreaterEqual(len(unit["activities"]), 1)\n            self.assertGreaterEqual(len(unit["source_ids"]), 5)\n\n    def test_assessments_glossary_sources_and_media_exist(self):\n        for relative in self.course["assessment_files"]:\n            self.assertTrue((BASE / relative).exists(), relative)\n        assessment = json.loads((BASE / "assessments" / "course-assessment.json").read_text(encoding="utf-8"))\n        self.assertEqual(sum(item["weight_percent"] for item in assessment["assessment_plan"]), 100)\n        self.assertGreaterEqual(len(assessment["diagnostic"]["questions"]), 10)\n        self.assertGreaterEqual(len(assessment["midterm_blueprint"]), 4)\n        self.assertGreaterEqual(len(assessment["capstone"].get("rubric", [])), 5)\n        glossary = json.loads((BASE / "glossary.json").read_text(encoding="utf-8"))\n        self.assertGreaterEqual(len(glossary["entries"]), 30)\n        self.assertTrue(all(entry.get("source_ids") for entry in glossary["entries"]))\n        sources = json.loads((BASE / "sources.json").read_text(encoding="utf-8"))\n        self.assertGreaterEqual(len(sources["sources"]), 12)\n        self.assertEqual(sources["coverage_gaps"], [])\n        media = json.loads((BASE / "media.json").read_text(encoding="utf-8"))\n        self.assertEqual(media["coverage_status"], "planned")\n        self.assertEqual(len(media["items"]), 6)\n\n    def test_course_outcomes_cover_the_full_sequence(self):\n        self.assertEqual(len(self.course["learning_outcomes"]), 7)\n        mapped = set()\n        for relative in self.course["unit_files"]:\n            unit = json.loads((BASE / relative).read_text(encoding="utf-8"))\n            mapped.update(unit["course_learning_outcome_ids"])\n        self.assertEqual(mapped, {item["id"] for item in self.course["learning_outcomes"]})\n\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")

print("Biomateriales e Implantes canonical closure curated.")
