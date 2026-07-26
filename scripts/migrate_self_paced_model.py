#!/usr/bin/env python3
"""One-off migration from fixed academic pacing to a self-paced course model."""
from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".py", ".js", ".css", ".html", ".md", ".yml", ".yaml", ".json"}

COURSE_TIME_KEYS = {
    "estimated_workload",
    "duration_weeks",
    "weekly_hours",
    "total_workload_hours",
    "course_plan",
}
UNIT_TIME_KEYS = {"estimated_hours", "weeks"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rename(old_rel: str, new_rel: str) -> None:
    if old_rel == new_rel:
        return
    old = ROOT / old_rel
    new = ROOT / new_rel
    if old.exists():
        new.parent.mkdir(parents=True, exist_ok=True)
        if new.exists():
            new.unlink()
        old.rename(new)


def replace_file(path: Path, replacements: list[tuple[str, str]]) -> None:
    if not path.exists():
        return
    text = read(path)
    for old, new in replacements:
        text = text.replace(old, new)
    write(path, text)


def normalize_pacing_text(value: str) -> str:
    replacements = {
        "Antes de iniciar una unidad:": "Antes de iniciar una unidad:",
        "antes de iniciar una unidad:": "antes de iniciar una unidad:",
        "De forma periódica:": "De forma periódica:",
        "de forma periódica:": "de forma periódica:",
        "nivelación previa": "nivelación previa",
        "nivelación previa": "nivelación previa",
        "al completar el recorrido": "al completar el recorrido",
        "a lo largo del recorrido": "a lo largo del recorrido",
        "Plan de evaluación": "Plan de evaluación",
        "plan de evaluación": "plan de evaluación",
        "ruta del curso": "ruta del curso",
        "Ruta del curso": "Ruta del curso",
        "del curso": "del curso",
        "del curso": "del curso",
        "recorridos": "recorridos",
        "recorrido": "recorrido",
        "Course": "Course",
        "course": "course",
    }
    text = value
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\bpor semana\b", "según la necesidad", text, flags=re.IGNORECASE)
    return text


def clean_json_value(value: Any, *, course_file: bool, unit_file: bool) -> Any:
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        for key, child in value.items():
            if key == "estimated_workload":
                continue
            if course_file and key in COURSE_TIME_KEYS:
                continue
            if unit_file and key in UNIT_TIME_KEYS:
                continue
            output[key] = clean_json_value(child, course_file=course_file, unit_file=unit_file)
        return output
    if isinstance(value, list):
        return [clean_json_value(item, course_file=course_file, unit_file=unit_file) for item in value]
    if isinstance(value, str):
        return normalize_pacing_text(value).replace("que", "que")
    return value


def migrate_json() -> None:
    for path in sorted((ROOT / "data").rglob("*.json")):
        try:
            data = json.loads(read(path))
        except json.JSONDecodeError:
            continue
        course_file = (ROOT / "data" / "generated_courses") in path.parents
        unit_file = (ROOT / "data" / "generated_units") in path.parents
        cleaned = clean_json_value(data, course_file=course_file, unit_file=unit_file)
        write(path, json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n")


def migrate_templates_and_generators() -> None:
    replace_file(
        ROOT / "templates" / "asignatura.html",
        [
            ('        <div><dt>Carga estimada</dt><dd>{{ estimated_workload }}</dd></div>\n', ''),
            ('../../assets/js/course.js', '../../assets/js/course.js'),
        ],
    )
    replace_file(
        ROOT / "templates" / "unidad.html",
        [('        <div><dt>Tiempo sugerido</dt><dd>8–12 horas</dd></div>\n', '')],
    )

    generator = ROOT / "scripts" / "generate_site.py"
    replace_file(
        generator,
        [
            ('    "estimated_workload",\n', ''),
            ('        "estimated_workload": "16 semanas; 6-8 horas semanales; 120-150 horas totales de estudio, práctica y evaluación",\n', ''),
            ('        "estimated_workload": escape(subject.get("estimated_workload", "12-16 semanas; 90-150 horas de trabajo total")),\n', ''),
        ],
    )

    replace_file(
        ROOT / "scripts" / "validate_curriculum.py",
        [('    "estimated_workload",\n', '')],
    )
    replace_file(
        ROOT / "citonauta_agent" / "schemas.py",
        [('    estimated_workload: str = Field(min_length=15)\n', '')],
    )
    replace_file(
        ROOT / "citonauta_agent" / "prompts.py",
        [('        "estimated_workload": _text(baseline.get("estimated_workload"), 160),\n', '')],
    )
    replace_file(
        ROOT / "citonauta_agent" / "ollama_gateway.py",
        [('  estimated_workload:string, biomedical_connection:string,\n', '  biomedical_connection:string,\n')],
    )
    replace_file(
        ROOT / "scripts" / "validate_agent_content.py",
        [('        "estimated_workload",\n', '')],
    )


def migrate_course_assets() -> None:
    rename("assets/js/course.js", "assets/js/course.js")
    rename("assets/css/course.css", "assets/css/course.css")

    js_path = ROOT / "assets" / "js" / "course.js"
    if js_path.exists():
        text = read(js_path)
        text = re.sub(
            r"  function renderCourseHeader\(course\) \{.*?\n  \}\n\n  function renderPurpose",
            textwrap.dedent(
                """
                  function renderCourseHeader(course) {
                    const meta = document.querySelector(".course-meta");
                    if (!meta) return;
                    const values = meta.querySelectorAll("dd");
                    if (values[0] && course.academic_level) values[0].textContent = course.academic_level;
                  }

                  function renderPurpose"""
            ).rstrip(),
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            r"\n  function renderCoursePlan\(course\) \{.*?\n  \}\n\n  function renderAssessment",
            "\n\n  function renderAssessment",
            text,
            flags=re.DOTALL,
        )
        text = text.replace("    renderCoursePlan(course);\n", "")
        text = text.replace("Plan de evaluación", "Plan de evaluación")
        text = text.replace("course-course", "course")
        text = text.replace("assets/css/course.css", "assets/css/course.css")
        write(js_path, text)

    css_path = ROOT / "assets" / "css" / "course.css"
    if css_path.exists():
        write(css_path, read(css_path).replace("course-course", "course"))

    units_js = ROOT / "assets" / "js" / "generated-units.js"
    if units_js.exists():
        text = read(units_js)
        text = text.replace('    if (unit.estimated_hours) values.push(`${unit.estimated_hours} horas estimadas`);\n', '')
        text = text.replace('    if (unit.weeks?.length) values.push(`Semanas ${unit.weeks.join("–")}`);\n', '')
        text = text.replace("loadCourseCourseEnhancer", "loadCourseEnhancer")
        text = text.replace('script[data-course-course="true"]', 'script[data-course="true"]')
        text = text.replace("assets/js/course.js", "assets/js/course.js")
        text = text.replace('script.dataset.courseCourse = "true";', 'script.dataset.course = "true";')
        write(units_js, text)


def migrate_validators_and_audits() -> None:
    unit_validator = ROOT / "scripts" / "validate_generated_units.py"
    if unit_validator.exists():
        text = read(unit_validator)
        text = text.replace("def validate_course(data: dict[str, Any]) -> None:", "def validate_course(data: dict[str, Any]) -> None:")
        text = text.replace("        validate_course(data)\n", "        validate_course(data)\n")
        text = re.sub(
            r"    if int\(data\.get\(\"estimated_hours\", 0\) or 0\) < 12:\n"
            r"        raise ValueError\(\"schema 2\.0 requiere al menos 12 horas estimadas\"\)\n"
            r"    if not isinstance\(data\.get\(\"weeks\"\), list\) or not data\[\"weeks\"\]:\n"
            r"        raise ValueError\(\"schema 2\.0 requiere semanas asignadas\"\)\n",
            "",
            text,
        )
        marker = "    missing = sorted(required - data.keys())\n    if missing:\n        raise ValueError(\"faltan campos: \" + \", \".join(missing))\n"
        insertion = marker + "    forbidden_time_fields = sorted({\"estimated_hours\", \"weeks\"} & data.keys())\n    if forbidden_time_fields:\n        raise ValueError(\"metadatos temporales no permitidos: \" + \", \".join(forbidden_time_fields))\n"
        text = text.replace(marker, insertion)
        write(unit_validator, text)

    rename("scripts/audit_course_readiness.py", "scripts/audit_course_readiness.py")
    readiness = ROOT / "scripts" / "audit_course_readiness.py"
    if readiness.exists():
        text = read(readiness)
        for line in (
            "MIN_DURATION_WEEKS = 12\n",
            "MAX_DURATION_WEEKS = 16\n",
            "MIN_TOTAL_HOURS = 90\n",
            "MIN_SEMESTER_PLAN_ROWS = 12\n",
        ):
            text = text.replace(line, "")
        text = re.sub(
            r"\n    duration = int\(data\.get\(\"duration_weeks\", 0\) or 0\).*?"
            r"\n    if len\(data\.get\(\"course_competencies\", \[\]\)\) < MIN_COURSE_COMPETENCIES:",
            "\n    forbidden = sorted(COURSE_TIME_KEYS & data.keys())\n    if forbidden:\n        issues.append(\"conserva metadatos temporales: \" + \", \".join(forbidden))\n    if len(data.get(\"course_competencies\", [])) < MIN_COURSE_COMPETENCIES:",
            text,
            flags=re.DOTALL,
        )
        text = text.replace(
            "URL_RE = re.compile(r\"^https?://\", re.IGNORECASE)\n",
            "URL_RE = re.compile(r\"^https?://\", re.IGNORECASE)\nCOURSE_TIME_KEYS = {\"estimated_workload\", \"duration_weeks\", \"weekly_hours\", \"total_workload_hours\", \"course_plan\"}\nUNIT_TIME_KEYS = {\"estimated_hours\", \"weeks\"}\n",
        )
        text = text.replace(
            "    issues: list[str] = []\n    if len(data.get(\"learning_objectives\", [])) < MIN_OBJECTIVES:\n",
            "    issues: list[str] = []\n    forbidden = sorted(UNIT_TIME_KEYS & data.keys())\n    if forbidden:\n        issues.append(\"conserva metadatos temporales: \" + \", \".join(forbidden))\n    if len(data.get(\"learning_objectives\", [])) < MIN_OBJECTIVES:\n",
        )
        text = normalize_pacing_text(text)
        text = text.replace("arquitectura course", "arquitectura del curso")
        text = text.replace("ARQUITECTURA COURSE VÁLIDA", "ARQUITECTURA DEL CURSO VÁLIDA")
        text = text.replace("arquitecturas course", "arquitecturas de curso")
        write(readiness, text)

    rename("scripts/audit_course_portfolio.py", "scripts/audit_course_portfolio.py")
    portfolio = ROOT / "scripts" / "audit_course_portfolio.py"
    if portfolio.exists():
        text = read(portfolio)
        text = text.replace("MAX_HOUR_MISMATCH = 8\n", "")
        text = text.replace(
            "SPACE_RE = re.compile(r\"\\s+\")\n",
            "SPACE_RE = re.compile(r\"\\s+\")\nCOURSE_TIME_KEYS = {\"estimated_workload\", \"duration_weeks\", \"weekly_hours\", \"total_workload_hours\", \"course_plan\"}\nUNIT_TIME_KEYS = {\"estimated_hours\", \"weeks\"}\n",
        )
        text = re.sub(
            r"\n    duration = int\(course\.get\(\"duration_weeks\", 0\) or 0\).*?"
            r"\n    assessment = course\.get\(\"assessment_plan\", \[\]\)",
            "\n    forbidden = sorted(COURSE_TIME_KEYS & course.keys())\n    if forbidden:\n        errors.append(f\"{prefix}: conserva metadatos temporales: {', '.join(forbidden)}\")\n\n    assessment = course.get(\"assessment_plan\", [])",
            text,
            flags=re.DOTALL,
        )
        text = text.replace(
            "        number = int(unit[\"unit\"])\n        unit_prefix = f\"{prefix}/unit-{number:02d}\"\n",
            "        number = int(unit[\"unit\"])\n        unit_prefix = f\"{prefix}/unit-{number:02d}\"\n        forbidden = sorted(UNIT_TIME_KEYS & unit.keys())\n        if forbidden:\n            errors.append(f\"{unit_prefix}: conserva metadatos temporales: {', '.join(forbidden)}\")\n",
        )
        text = text.replace('        "course_hours": course_hours,\n', '')
        text = text.replace('        "unit_hours": unit_hours,\n', '')
        text = text.replace(
            "            f\"horas={data['unit_hours']}/{data['course_hours']} · ecuaciones={data['equations']} · \"\n",
            "            f\"ecuaciones={data['equations']} · \"\n",
        )
        text = normalize_pacing_text(text)
        text = text.replace("cursos course", "cursos")
        text = text.replace("PORTAFOLIO COURSE", "PORTAFOLIO DE CURSOS")
        write(portfolio, text)


def update_references_and_docs() -> None:
    replacements = {
        "audit_course_readiness.py": "audit_course_readiness.py",
        "audit_course_portfolio.py": "audit_course_portfolio.py",
        "course.js": "course.js",
        "course.css": "course.css",
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts:
            continue
        text = read(path)
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = text.replace("que", "que")
        if path.suffix.lower() != ".json":
            text = normalize_pacing_text(text)
        write(path, text)

    for path in sorted((ROOT / "docs").glob("*.md")) + [ROOT / "README.md"]:
        if not path.exists():
            continue
        lines = []
        for line in read(path).splitlines():
            lowered = line.casefold()
            if any(token in lowered for token in (
                "estimated_workload",
                "duration_weeks",
                "weekly_hours",
                "total_workload_hours",
                "estimated_hours",
                "12-16 semanas",
                "16 semanas",
                "120-150 horas",
                "carga horaria sugerida",
                "carga estimada",
            )):
                continue
            lines.append(line)
        write(path, "\n".join(lines).rstrip() + "\n")

    readme = ROOT / "README.md"
    if readme.exists():
        text = read(readme)
        heading = "## Modelo de aprendizaje autogestionado"
        if heading not in text:
            block = textwrap.dedent(
                """

                ## Modelo de aprendizaje autogestionado

                CitoNauta organiza contenidos, prerrequisitos, actividades y criterios de dominio, pero no asigna duraciones, cargas horarias ni calendarios estándar. Cada persona avanza según sus conocimientos previos, profundidad requerida, práctica y necesidad de revisión. Completar una asignatura significa demostrar los resultados de aprendizaje y no cumplir una cantidad predeterminada de tiempo.
                """
            )
            marker = "## Generación y validación"
            text = text.replace(marker, block + "\n" + marker) if marker in text else text + block
        write(readme, text)


def clean_public_html() -> None:
    block_re = re.compile(
        r"\s*<div>\s*<dt>(?:Carga estimada|Tiempo sugerido)</dt>\s*<dd>.*?</dd>\s*</div>",
        flags=re.DOTALL | re.IGNORECASE,
    )
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        text = block_re.sub("", read(path))
        text = text.replace("que", "que")
        text = text.replace("course.js", "course.js")
        text = text.replace("course.css", "course.css")
        text = normalize_pacing_text(text)
        write(path, text)


def write_policy_and_audit_review() -> None:
    policy = textwrap.dedent(
        """
        # Modelo de aprendizaje autogestionado

        CitoNauta estructura el conocimiento por asignaturas, unidades, prerrequisitos, resultados, actividades y evidencias de dominio. No presupone un calendario académico uniforme.

        ## Principios

        - No se publican duraciones, cargas horarias ni ritmos estándar para asignaturas o unidades.
        - El avance depende de conocimientos previos, profundidad buscada, práctica necesaria y retroalimentación.
        - La secuencia de unidades expresa dependencia conceptual, no una obligación temporal.
        - Los diagnósticos de prerrequisitos orientan la entrada; no asignan plazos de nivelación.
        - La finalización se define mediante resultados observables, productos, autoevaluación y criterios de calidad.
        - La plataforma puede registrar progreso por unidades completadas, pero no convertir ese progreso en una estimación universal de tiempo.

        ## Consecuencia editorial

        Los campos temporales quedan fuera del esquema de datos, las plantillas, el agente generativo y los validadores. Cualquier nueva contribución que reintroduzca calendarios o cargas estándar debe ser rechazada por los quality gates.
        """
    ).strip() + "\n"
    write(ROOT / "docs" / "SELF_PACED_LEARNING_MODEL.md", policy)

    review = textwrap.dedent(
        """
        # Evaluación crítica de la auditoría externa del 26 de julio de 2026

        La auditoría externa se usa como insumo de contraste, no como especificación automática. Sus cifras y calificaciones solo deben aceptarse cuando puedan reproducirse con scripts, datos y definiciones disponibles en el repositorio.

        ## Hallazgos aceptados

        1. **Metadatos temporales uniformes.** La asignación generalizada de calendarios y cargas producía una falsa precisión. Este hallazgo se corrige con el modelo autogestionado y con validación automática para impedir su reaparición.
        2. **Duplicación tipográfica consecutiva de «que».** El defecto estaba presente en contenido publicado y se corrige en fuentes y salidas generadas.
        3. **Texto conceptual genérico.** El fallback operacional puede mantener una estructura completa sin aportar suficiente contenido disciplinar. La cobertura del diccionario es una señal de mantenimiento, no una medida de aprendizaje ni de calidad científica.
        4. **Disparidad entre material manual y automático.** Es válido evaluar por separado profundidad conceptual, estructura, fuentes, práctica y revisión humana; ninguna de esas dimensiones sustituye a las demás.
        5. **Rigor cuantitativo desigual.** Las ecuaciones y los casos numéricos deben aparecer cuando son necesarios para explicar el mecanismo o método, especialmente en señales, biomecánica, biofísica, modelado y estadística.
        6. **Navegación plana.** Buscador, filtros, niveles y rutas interdisciplinarias pueden reducir la carga de exploración del catálogo.

        ## Hallazgos parcialmente válidos

        - **Prerrequisitos y andamiaje.** El repositorio ya publica prerrequisitos; el trabajo pendiente es convertirlos en dependencias navegables y verificar su coherencia entre asignaturas.
        - **Taxonomía cognitiva.** Es útil diversificar acciones cognitivas, pero no imponer que una unidad inicial solo recuerde ni que la última siempre cree. El nivel depende del objetivo y del tipo de evidencia.
        - **Cantidad de unidades.** Debe adaptarse a la estructura disciplinar. Aumentar unidades solo para alcanzar una cifra puede fragmentar artificialmente el aprendizaje.
        - **Retroalimentación de autoevaluación.** Conviene incluir razonamiento y errores frecuentes; una consecuencia clínica solo debe añadirse cuando sea real, pertinente y sustentada.

        ## Recomendaciones rechazadas como cuotas automáticas

        - Ampliar un diccionario hasta una cifra arbitraria sin revisión disciplinar.
        - Exigir tres ecuaciones en cada unidad de ingeniería independientemente del contenido.
        - Forzar niveles cognitivos por número de unidad.
        - Convertir toda asignatura densa en nueve o diez unidades sin análisis curricular.
        - Declarar una calificación potencial casi perfecta como si fuera una métrica reproducible.

        ## Uso futuro

        La auditoría sirve para priorizar problemas verificables: densidad conceptual, ejemplos cuantitativos pertinentes, fuentes específicas, navegación, dependencias y revisión humana. Las transformaciones masivas deben demostrar mejora mediante muestras editoriales, validadores y revisión por disciplina; no mediante volumen de texto o cumplimiento mecánico de cuotas.
        """
    ).strip() + "\n"
    write(ROOT / "docs" / "EXTERNAL_AUDIT_CRITICAL_REVIEW_2026-07-26.md", review)


def write_validator() -> None:
    content = textwrap.dedent(
        r'''
        #!/usr/bin/env python3
        """Enforce the self-paced learning model and reject fixed study-time metadata."""
        from __future__ import annotations

        import json
        import re
        from pathlib import Path
        from typing import Any

        ROOT = Path(__file__).resolve().parents[1]
        COURSE_KEYS = {"estimated_workload", "duration_weeks", "weekly_hours", "total_workload_hours", "course_plan"}
        UNIT_KEYS = {"estimated_hours", "weeks"}
        TEXT_SUFFIXES = {".py", ".js", ".css", ".html", ".md", ".yml", ".yaml", ".json"}
        FORBIDDEN_UI = ("Carga estimada", "Tiempo sugerido", "horas estimadas", "horas semanales", "horas totales de estudio")
        DUPLICATE_QUE = re.compile(r"\bque\s+que\b", re.IGNORECASE)

        def find_keys(value: Any, forbidden: set[str], prefix: str = "") -> list[str]:
            errors: list[str] = []
            if isinstance(value, dict):
                for key, child in value.items():
                    current = f"{prefix}.{key}" if prefix else key
                    if key in forbidden:
                        errors.append(current)
                    errors.extend(find_keys(child, forbidden, current))
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    errors.extend(find_keys(child, forbidden, f"{prefix}[{index}]"))
            return errors

        def main() -> int:
            errors: list[str] = []
            old_paths = (
                "assets/js/course.js",
                "assets/css/course.css",
                "scripts/audit_course_readiness.py",
                "scripts/audit_course_portfolio.py",
            )
            for relative in old_paths:
                if (ROOT / relative).exists():
                    errors.append(f"ruta temporal obsoleta presente: {relative}")

            for path in sorted((ROOT / "data" / "generated_courses").glob("*.json")):
                data = json.loads(path.read_text(encoding="utf-8"))
                for location in find_keys(data, COURSE_KEYS):
                    errors.append(f"{path.relative_to(ROOT)} conserva {location}")
            for path in sorted((ROOT / "data" / "generated_units").glob("*/unit-*.json")):
                data = json.loads(path.read_text(encoding="utf-8"))
                for location in find_keys(data, UNIT_KEYS):
                    errors.append(f"{path.relative_to(ROOT)} conserva {location}")
            for path in sorted((ROOT / "data" / "subjects").glob("*/*.json")):
                data = json.loads(path.read_text(encoding="utf-8"))
                for location in find_keys(data, {"estimated_workload"}):
                    errors.append(f"{path.relative_to(ROOT)} conserva {location}")

            for path in ROOT.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES or ".git" in path.parts:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                if DUPLICATE_QUE.search(text):
                    errors.append(f"duplicación tipográfica en {path.relative_to(ROOT)}")
                lowered = text.casefold()
                if "course-course" in lowered or "audit_course" in lowered or "course_plan" in lowered:
                    errors.append(f"nomenclatura temporal obsoleta en {path.relative_to(ROOT)}")
                if path.suffix.lower() in {".html", ".js"} or path.name in {"asignatura.html", "unidad.html"}:
                    for phrase in FORBIDDEN_UI:
                        if phrase.casefold() in lowered:
                            errors.append(f"referencia temporal pública en {path.relative_to(ROOT)}: {phrase}")

            if errors:
                print("Errores del modelo autogestionado:\n")
                for error in sorted(set(errors)):
                    print(f"- {error}")
                return 1
            print("Modelo de aprendizaje autogestionado validado.")
            print("- sin cargas horarias ni calendarios estándar")
            print("- sin nomenclatura interna basada en cursos temporizados")
            print("- sin duplicación tipográfica consecutiva de 'que'")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        '''
    ).lstrip()
    write(ROOT / "scripts" / "validate_self_paced_model.py", content)


def main() -> int:
    migrate_json()
    migrate_templates_and_generators()
    migrate_course_assets()
    migrate_validators_and_audits()
    update_references_and_docs()
    clean_public_html()
    write_policy_and_audit_review()
    write_validator()
    print("Migración al modelo autogestionado aplicada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
