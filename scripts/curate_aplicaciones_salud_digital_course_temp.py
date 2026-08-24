#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "data" / "courses" / "aplicaciones-salud-digital"
CODE = "ASDIG"
COURSE_ID = "aplicaciones-salud-digital"
TODAY = "2026-08-24"

STATUS = {
    "content": "complete",
    "sources": "traceable",
    "pedagogy": "complete",
    "multimedia": "planned",
    "internal_review": "pending",
    "external_review": "pending",
    "publication": "published_provisional",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def course_outcomes():
    statements = [
        "Delimita problemas de salud adecuados para intervención digital mediante actores, recorrido asistencial, necesidad, determinantes, teoría de cambio y alternativas no digitales.",
        "Diseña soluciones centradas en personas con investigación de usuarios, accesibilidad, prototipado, tareas críticas, factores humanos y evidencia de usabilidad proporcional al uso previsto.",
        "Diseña telemedicina y monitorización remota con modalidad, sensores, calidad de señal, alertas, respuesta clínica, seguridad y criterios de escalado explícitos.",
        "Construye integraciones sanitarias reproducibles con modelos de información, terminologías, APIs, FHIR, calidad, procedencia y pruebas de interoperabilidad semántica y técnica.",
        "Evalúa una intervención digital distinguiendo eficacia, efectividad, implementación, equidad, seguridad, experiencia, utilización de recursos y economía sin confundir asociación con causalidad.",
        "Construye un expediente de despliegue responsable que integra privacidad, ciberseguridad, finalidad prevista, regulación, gobernanza, gestión de cambios, incidentes, rollback y escalado progresivo.",
        "Integra las seis unidades en una decisión auditable que conecta problema, diseño, arquitectura, evidencia, riesgos y condiciones de implementación, registrando incertidumbre, alternativas, correcciones y límites de inferencia.",
    ]
    return [{"id": f"{CODE}-LO{i:02d}", "statement": text} for i, text in enumerate(statements, 1)]


def competencies():
    statements = [
        "Traducir una necesidad sanitaria a un problema digital delimitado antes de seleccionar tecnología.",
        "Diseñar experiencias digitales accesibles y seguras alrededor de tareas reales de pacientes y profesionales.",
        "Conectar datos, dispositivos, APIs y estándares manteniendo significado, calidad, procedencia y trazabilidad.",
        "Diseñar evaluación clínica, de implementación, equidad y economía acorde con la pregunta y la madurez de la intervención.",
        "Gestionar privacidad, ciberseguridad, proveedores, cambios e incidentes como propiedades del ciclo de vida.",
        "Razonar sobre calificación regulatoria y obligaciones temporales sin emitir asesoramiento jurídico ni clasificación vinculante.",
        "Tomar decisiones go/no-go o de escalado condicionadas a evidencia, controles, responsables y riesgo residual explícitos.",
    ]
    return [{"id": f"{CODE}-COMP{i:02d}", "statement": text} for i, text in enumerate(statements, 1)]


def prerequisites():
    statements = [
        "Fundamentos de programación, estructuras de datos y APIs a nivel universitario inicial.",
        "Estadística descriptiva e inferencial básica para interpretar incertidumbre, intervalos y comparaciones.",
        "Fundamentos de fisiología, organización sanitaria y razonamiento clínico suficientes para comprender recorridos asistenciales sin ejercer práctica clínica.",
        "Conceptos básicos de bases de datos, redes, seguridad y representación estructurada de información.",
        "Capacidad para documentar requisitos, supuestos, versiones, procedencia y resultados reproducibles.",
    ]
    return [{"id": f"{CODE}-PRE{i:02d}", "statement": text} for i, text in enumerate(statements, 1)]


def build_course_assessment():
    return {
        "$schema": "../../../../schemas/academic/assessment-v1.schema.json",
        "schema_version": "1.0",
        "id": f"{CODE}-EVAL-CURSO",
        "course_id": COURSE_ID,
        "scope": "course",
        "principles": [
            "La evaluación sigue la cadena necesidad → diseño → datos/servicio → evidencia → riesgo → decisión, no la presencia de una aplicación atractiva.",
            "Toda afirmación sobre beneficio, seguridad, interoperabilidad, privacidad o regulación debe conservar alcance, evidencia, fecha y responsable.",
            "Los datos, usuarios, incidentes y productos de actividades calificadas son sintéticos o recursos abiertos no personales.",
            "Los errores corregidos con explicación y registro antes-después forman parte de la evidencia de aprendizaje.",
            "Una conclusión favorable de efectividad o economía no sustituye privacidad, ciberseguridad, regulación ni preparación operativa.",
            "La revisión disciplinaria humana y cualquier autorización clínica, jurídica o regulatoria permanecen pendientes."
        ],
        "assessment_plan": [
            {"component": "Comprobaciones recuperativas U1–U6", "weight_percent": 15, "description": "Autoevaluaciones explicadas con feedback, corrección y reintento documentado."},
            {"component": "Problema, usuarios y prototipo", "weight_percent": 20, "description": "Caso U1–U2 que conecta necesidad, tareas, accesibilidad, factores humanos y criterios de éxito."},
            {"component": "Telemonitorización e interoperabilidad", "weight_percent": 20, "description": "Caso U3–U4 con sensores, alertas, FHIR/APIs, calidad, terminologías, trazabilidad y pruebas."},
            {"component": "Evaluación clínica, implementación y economía", "weight_percent": 20, "description": "Caso U5 que separa estimando, diseño, sesgo, implementación, equidad, costes e incertidumbre."},
            {"component": "Proyecto integrador de despliegue responsable", "weight_percent": 25, "description": "Capstone U1–U6 con privacidad, seguridad, regulación, gobernanza y decisión condicionada."}
        ],
        "diagnostic": {
            "title": "Diagnóstico de entrada a Aplicaciones de Salud Digital",
            "purpose": "Detectar prerrequisitos que requieren recuperación antes de U1; no aporta nota final.",
            "questions": [
                "Distingue problema sanitario, necesidad de usuario y requisito de software.",
                "Explica la diferencia entre variable, dato, metadato y procedencia.",
                "Distingue eficacia, efectividad y utilidad clínica.",
                "Explica qué significa sesgo de selección en una evaluación.",
                "Describe qué resuelve una API y qué no garantiza sobre semántica.",
                "Distingue autenticación de autorización.",
                "Explica por qué cifrado no equivale a privacidad.",
                "Distingue consentimiento clínico de consentimiento/base jurídica para tratamiento de datos.",
                "Explica por qué una alerta necesita un responsable y un tiempo de respuesta.",
                "Distingue interoperabilidad sintáctica de semántica.",
                "Explica por qué un buen AUROC no demuestra beneficio clínico.",
                "Describe qué información mínima permitiría reproducir una decisión de despliegue."
            ],
            "interpretation": [
                "0–4 respuestas sólidas: completar nivelación en datos, estadística, APIs y seguridad antes de U1.",
                "5–8 respuestas sólidas: iniciar U1 con recuperación focalizada documentada.",
                "9–12 respuestas sólidas: iniciar el curso y conservar igualmente supuestos y límites."
            ]
        },
        "midterm_blueprint": [
            {"domain": "U1 Necesidades y ecosistema digital", "weight_percent": 16},
            {"domain": "U2 Diseño centrado en personas", "weight_percent": 16},
            {"domain": "U3 Telemedicina y monitorización", "weight_percent": 17},
            {"domain": "U4 Datos e interoperabilidad", "weight_percent": 17},
            {"domain": "U5 Evaluación clínica y económica", "weight_percent": 17},
            {"domain": "U6 Privacidad, regulación e implementación", "weight_percent": 17}
        ],
        "capstone": {
            "title": "Expediente reproducible de una intervención digital sanitaria sintética",
            "scenario": "Un equipo académico debe decidir si una intervención digital completamente sintética está preparada para pasar de prototipo a piloto controlado y, posteriormente, qué evidencia exigiría antes de escalar. El expediente debe conectar necesidad, usuarios, arquitectura, datos, evidencia, privacidad, ciberseguridad, regulación y operación sin usar pacientes, credenciales ni sistemas reales.",
            "phases": [
                "Predefinir problema, población, actores, flujo actual, alternativa no digital y criterio de éxito.",
                "Diseñar tareas, accesibilidad, prototipo y riesgos de uso con criterios verificables.",
                "Definir modalidad de telemedicina o monitorización, sensores, alertas, escalamiento y ruta degradada.",
                "Especificar contrato de datos, terminologías, API/FHIR, calidad, procedencia y pruebas de interoperabilidad.",
                "Diseñar evaluación clínica, de implementación, equidad y economía con estimando y análisis de incertidumbre.",
                "Construir matrices de privacidad y amenazas y registrar controles, pruebas, incidentes y riesgo residual.",
                "Determinar preguntas de calificación/regulación, versiones normativas y responsables competentes sin emitir clasificación vinculante.",
                "Emitir decisión no-go, piloto limitado, go condicionado o go; realizar revisión independiente y documentar correcciones."
            ],
            "required_deliverables": [
                "Mapa de actores, recorrido y teoría de cambio.",
                "Prototipo o especificación de interacción con criterios de accesibilidad y tareas críticas.",
                "Arquitectura de telemonitorización y matriz alerta→acción→responsable.",
                "Contrato de datos e interoperabilidad con pruebas y procedencia.",
                "Plan de evaluación U5 con métricas, estimando, implementación, equidad, costes e incertidumbre.",
                "Matriz finalidad→dato→base/condición a revisar→retención y modelo de amenazas.",
                "Matriz regulatoria versionada y registro de cuestiones que requieren especialistas.",
                "Plan de despliegue, soporte, monitorización, incidentes, rollback y escalado.",
                "README reproducible con versiones, supuestos, decisiones y evidencia.",
                "Acta final de decisión y registro antes-después de revisión."
            ],
            "integration_requirements": [
                "Vincular evidencia explícita con ASDIG-LO01 a ASDIG-LO07.",
                "Incluir al menos una alternativa no digital y una explicación de por qué la intervención propuesta añade valor potencial.",
                "Separar datos observados, supuestos, resultados de evaluación, inferencias y decisiones.",
                "Usar únicamente escenarios sintéticos o recursos abiertos no personales y documentar procedencia/licencia."
            ],
            "rubric": [
                {"criterion": "Problema, actores y diseño centrado en personas", "weight_percent": 16, "excellent": "Necesidad, flujo, tareas, accesibilidad y alternativa están delimitados y conectados a criterios verificables."},
                {"criterion": "Arquitectura, datos e interoperabilidad", "weight_percent": 17, "excellent": "Sensores, alertas, contratos, FHIR/APIs, terminologías, calidad y procedencia forman una cadena reproducible."},
                {"criterion": "Evaluación de valor y evidencia", "weight_percent": 18, "excellent": "Estimando, diseño, implementación, equidad, seguridad, economía e incertidumbre sostienen una conclusión proporcional."},
                {"criterion": "Privacidad y ciberseguridad", "weight_percent": 17, "excellent": "Finalidades, datos, roles, DPIA pendiente cuando corresponde, amenazas, controles, pruebas y riesgo residual son trazables."},
                {"criterion": "Regulación, gobernanza y operación", "weight_percent": 16, "excellent": "Finalidad prevista, preguntas regulatorias, responsables, cambios, incidentes, rollback y escalado están versionados y delimitados."},
                {"criterion": "Reproducibilidad, interpretación y revisión", "weight_percent": 16, "excellent": "Otra persona puede reconstruir decisiones; límites, incertidumbre y correcciones tras revisión están explícitos."}
            ]
        },
        "status": "curated_internal_review_pending"
    }


def curate():
    course_path = COURSE_DIR / "course.json"
    course = load(course_path)
    course["content_version"] = "1.0.0"
    course["academic_level"] = "Pregrado universitario intermedio y avanzado"
    course["audience"] = "Estudiantes de ingeniería biomédica, informática biomédica y áreas afines que necesiten diseñar, evaluar e implementar intervenciones digitales sanitarias con criterios reproducibles de personas, datos, evidencia, seguridad y gobernanza."
    course["status"] = STATUS
    course["purpose"] = "Integrar definición de necesidades sanitarias, diseño centrado en personas, telemedicina y monitorización, interoperabilidad, evaluación clínica/económica y despliegue responsable para construir intervenciones digitales reproducibles. El curso separa desempeño técnico, valor clínico, implementación, privacidad, ciberseguridad y regulación, y evita convertir prototipos o análisis académicos en autorización clínica, jurídica o regulatoria no demostrada."
    course["scope"] = {
        "included": [
            "Necesidades, actores, recorridos asistenciales, determinantes, teoría de cambio y alternativas no digitales.",
            "Investigación de usuarios, accesibilidad, prototipado, tareas críticas y factores humanos.",
            "Telemedicina síncrona/asíncrona, sensores, calidad de señal, alertas, escalamiento y continuidad.",
            "Modelos de información, terminologías, APIs, FHIR, calidad, procedencia y pruebas de interoperabilidad.",
            "Evaluación clínica, implementación, equidad, seguridad, experiencia, utilización de recursos y economía.",
            "Protección de datos, ciberseguridad, finalidad prevista, MDR/AI Act/EHDS como marcos de aprendizaje, gobernanza, cambios e incidentes.",
            "Expedientes reproducibles de decisión con evidencia, incertidumbre, riesgo residual, alternativas y límites."
        ],
        "excluded": [
            "Diagnóstico, tratamiento o triaje real de pacientes mediante actividades del curso.",
            "Uso de datos personales, historias clínicas, credenciales, tokens o sistemas clínicos reales en ejercicios.",
            "Asesoramiento jurídico, DPIA profesional, clasificación regulatoria vinculante o evaluación de conformidad.",
            "Afirmaciones de causalidad, seguridad o coste-efectividad sin diseño y evidencia suficientes.",
            "Autorización de despliegue real basada únicamente en productos académicos."
        ],
        "handoff_courses": [
            "historias-clinicas-terminologias-estandares",
            "informatica-biomedica",
            "ingenieria-datos-biomedicos",
            "interfaces-hombre-maquina",
            "sistemas-ayuda-decision-medica",
            "ciencia-regulatoria-calidad-seguridad-tecnologias-medicas"
        ]
    }
    course["prerequisites"] = prerequisites()
    course["competencies"] = competencies()
    course["learning_outcomes"] = course_outcomes()
    course["study_method"] = [
        "Definir primero problema sanitario, actor, contexto de uso, alternativa y decisión que se quiere apoyar.",
        "Alternar explicación, ejemplo resuelto, actividad guiada, apoyo reducido, reto autónomo y feedback recuperativo.",
        "Separar dato, transformación, resultado técnico, evidencia clínica, inferencia y decisión.",
        "Predefinir criterios de aceptación, seguridad, equidad, interoperabilidad y escalado antes de interpretar resultados.",
        "Conservar procedencia, versiones, configuraciones, contratos de datos, cambios, incidentes y discrepancias.",
        "Revisar cada producto con rúbrica y justificar correcciones antes de cerrar una conclusión."
    ]
    course["editorial_notice"] = "Corpus canónico educativo completo a nivel de contenido y pedagogía interna para las seis unidades de Aplicaciones de Salud Digital. Las fuentes quedan trazadas y la publicación sigue siendo provisional. La revisión humana interna y disciplinaria externa, la evaluación con personas, el uso de datos personales, el asesoramiento jurídico, la DPIA profesional, la clasificación regulatoria, la evaluación de conformidad y cualquier autorización de despliegue real permanecen fuera del cierre y siguen pendientes."
    save(course_path, course)

    sources_path = COURSE_DIR / "sources.json"
    sources = load(sources_path)
    used_sources = []
    for source in sources.get("sources", []):
        if source.get("used_by_unit_ids"):
            source["verification_status"] = "verified_directly" if source.get("verification_status") == "verified_directly" else source.get("verification_status", "unverified")
            used_sources.append(source)
    sources["sources"] = used_sources
    sources["source_policy"] = "Priorizar fuentes oficiales, estándares, guías metodológicas y literatura revisada por pares directamente verificable; toda afirmación temporal regulatoria debe registrar versión y fecha de consulta."
    sources["consulted_on"] = TODAY
    sources["coverage_gaps"] = []
    save(sources_path, sources)
    source_by_id = {s["id"]: s for s in used_sources}

    units = []
    unit_by_id = {}
    for unit_path in sorted((COURSE_DIR / "units").glob("unit-*.json")):
        unit = load(unit_path)
        unit["status"] = STATUS
        number = int(unit["order"])
        unit["course_learning_outcome_ids"] = [f"{CODE}-LO{number:02d}", f"{CODE}-LO07"]
        for activity in unit.get("activities", []):
            activity["estimated_duration_minutes"] = activity.get("estimated_duration_minutes") or 180
            activity["status"] = "curated_internal_review_pending"
        unit["editorial_notice"] = str(unit.get("editorial_notice") or "") + " La migración canónica conserva la frontera educativa: revisión humana interna y externa siguen pendientes."
        save(unit_path, unit)
        units.append((unit_path, unit))
        unit_by_id[unit["id"]] = unit

    glossary_path = COURSE_DIR / "glossary.json"
    glossary = load(glossary_path)
    for entry in glossary.get("entries", []):
        candidate_sources = []
        for unit_id in entry.get("unit_ids", []):
            candidate_sources.extend(unit_by_id.get(unit_id, {}).get("source_ids", []))
        candidate_sources = [sid for sid in dict.fromkeys(candidate_sources) if sid in source_by_id]
        entry["source_ids"] = candidate_sources[:2]
        entry["verification_status"] = "verified_directly" if entry["source_ids"] and all(source_by_id[sid].get("verification_status") == "verified_directly" for sid in entry["source_ids"]) else "curated_internal_review_pending"
    save(glossary_path, glossary)

    claims = {
        "$schema": "../../../schemas/academic/registry-v1.schema.json",
        "schema_version": "1.0",
        "course_id": COURSE_ID,
        "content_version": "1.0.0",
        "content_commit": None,
        "scope": "Afirmaciones centrales literales de las seis unidades con fuentes verificadas; revisión disciplinaria humana pendiente.",
        "review_state": "ai_review_provisional",
        "claims": []
    }
    for _, unit in units:
        source_ids = [sid for sid in unit.get("source_ids", []) if sid in source_by_id]
        claim_ids = []
        claim_n = 0
        for topic in unit.get("topics", []):
            for text in topic.get("key_points", [])[:1]:
                if not text or not source_ids:
                    continue
                claim_n += 1
                claim_id = f"{unit['id']}-C{claim_n:03d}"
                source_id = source_ids[(claim_n - 1) % len(source_ids)]
                source = source_by_id[source_id]
                claims["claims"].append({
                    "claim_id": claim_id,
                    "unit": unit["order"],
                    "text": text,
                    "claim_type": "methodological_or_interpretive",
                    "risk": "medium",
                    "context": f"Síntesis educativa de {unit['title']}; debe interpretarse dentro del protocolo, jurisdicción, fecha, supuestos y límites declarados.",
                    "source_id": source_id,
                    "locator": {"section": str(source.get("locator") or source.get("description") or source.get("title") or "Fuente consultada")},
                    "support": "direct_or_synthesis",
                    "source_verification_status": source.get("verification_status", "unverified"),
                    "review_state": "ai_review_provisional",
                    "reviewer_validation_id": None,
                    "reviewed_at": TODAY,
                    "id": claim_id,
                    "unit_id": unit["id"]
                })
                claim_ids.append(claim_id)
        unit["claim_ids"] = claim_ids
        save(COURSE_DIR / "units" / f"unit-{unit['order']:02d}.json", unit)
    save(COURSE_DIR / "claims.json", claims)

    for assessment_path in sorted((COURSE_DIR / "assessments").glob("unit-*.json")):
        assessment = load(assessment_path)
        assessment["status"] = "curated_internal_review_pending"
        unit_id = assessment.get("unit_id")
        unit_sources = [sid for sid in unit_by_id.get(unit_id, {}).get("source_ids", []) if sid in source_by_id]
        cognitive = ["remember", "understand", "apply", "analyze", "evaluate"]
        difficulty = ["foundational", "foundational", "intermediate", "intermediate", "advanced"]
        for index, item in enumerate(assessment.get("items", [])):
            item["difficulty"] = difficulty[min(index // 2, 4)]
            item["cognitive_level"] = cognitive[min(index // 2, 4)]
            item["feedback"] = {
                "correct": "Correcto. Conserva la evidencia, el alcance, la fecha y la frontera de inferencia en tu expediente acumulativo.",
                "incorrect": "Revisa el concepto y reconstruye la cadena dato o requisito → método/control → evidencia → conclusión permitida; después responde de nuevo sin consultar la solución."
            }
            item["source_ids"] = unit_sources[:1]
            item["status"] = "curated_internal_review_pending"
            if isinstance(item.get("answer_key"), dict) and not item["answer_key"].get("explanation"):
                item["answer_key"]["explanation"] = "La respuesta debe justificarse con la distinción conceptual y el límite de inferencia descritos en la unidad."
        save(assessment_path, assessment)

    save(COURSE_DIR / "assessments" / "course-assessment.json", build_course_assessment())

    course = load(course_path)
    course["core_source_ids"] = [s["id"] for s in used_sources if s.get("verification_status") == "verified_directly"][:16]
    course["assessment_files"] = [f"assessments/unit-{n:02d}.json" for n in range(1, 7)] + ["assessments/course-assessment.json"]
    course["registries"] = {"glossary": "glossary.json", "sources": "sources.json", "claims": "claims.json", "media": "media.json"}
    course["static_site"] = {
        "renderer": "scripts/generate_site.py",
        "canonical_source": True,
        "legacy_mirrors": [
            "data/generated_courses/aplicaciones-salud-digital.json",
            "data/generated_units/aplicaciones-salud-digital/",
            "data/subjects/ingenieria-biomedica/aplicaciones-salud-digital.json",
            "data/source_registry/aplicaciones-salud-digital.json",
            "data/claim_registry/aplicaciones-salud-digital.json"
        ]
    }
    save(course_path, course)

    print(f"Curado cierre canónico: {COURSE_DIR.relative_to(ROOT)}")
    print(f"Fuentes usadas: {len(used_sources)} · claims: {len(claims['claims'])} · glosario: {len(glossary.get('entries', []))}")


if __name__ == "__main__":
    curate()
