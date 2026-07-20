from __future__ import annotations

import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Iterable

from .schemas import CourseContent


WORD_RE = re.compile(r"\b[\wáéíóúüñÁÉÍÓÚÜÑ]+\b", re.UNICODE)


def substantive_word_count(course: CourseContent) -> int:
    text_parts: list[str] = [
        course.description,
        course.biomedical_connection,
        *course.prerequisites,
        *course.course_competencies,
        *course.learning_objectives,
        *course.learning_outcomes,
        *course.modules,
    ]
    for unit in course.detailed_units:
        text_parts.extend([unit.title, unit.description])
        text_parts.extend(unit.topics)
        text_parts.extend(unit.learning_outcomes)
        text_parts.extend(unit.activities)
        text_parts.extend(unit.common_misconceptions)
        text_parts.extend(unit.biomedical_applications)
        for block in unit.explanations:
            text_parts.extend([block.title, *block.paragraphs, *block.key_points])
        for example in unit.worked_examples:
            text_parts.extend(
                [example.title, example.scenario, *example.reasoning_steps, example.conclusion]
            )
        for question in unit.self_check:
            text_parts.extend([question.question, question.answer])
    return len(WORD_RE.findall(" ".join(text_parts)))


def validate_semantics(course: CourseContent, minimum_words: int) -> list[str]:
    errors: list[str] = []
    words = substantive_word_count(course)
    if words < minimum_words:
        errors.append(
            f"El curso contiene {words} palabras sustantivas; se requieren al menos {minimum_words}."
        )

    descriptions = [unit.description.strip().casefold() for unit in course.detailed_units]
    repeated = [text for text, count in Counter(descriptions).items() if count > 1]
    if repeated:
        errors.append("Hay descripciones de unidades duplicadas.")

    paragraph_markers: Counter[str] = Counter()
    for unit in course.detailed_units:
        for block in unit.explanations:
            for paragraph in block.paragraphs:
                marker = " ".join(paragraph.casefold().split())
                paragraph_markers[marker] += 1
    duplicate_paragraphs = [text for text, count in paragraph_markers.items() if count > 1]
    if duplicate_paragraphs:
        errors.append("Hay párrafos explicativos repetidos entre unidades.")

    if len({concept.casefold() for concept in course.key_concepts}) != len(course.key_concepts):
        errors.append("La lista de conceptos clave contiene duplicados.")
    return errors


def run_command(root: Path, command: list[str], timeout: int = 600) -> str:
    completed = subprocess.run(
        command,
        cwd=root,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    output = (completed.stdout + "\n" + completed.stderr).strip()
    if completed.returncode != 0:
        raise RuntimeError(
            f"Falló el comando ({completed.returncode}): {' '.join(command)}\n{output}"
        )
    return output


def generate_subject(root: Path, python: str, subject_id: str) -> str:
    generated = run_command(
        root,
        [python, "scripts/generate_site.py", "--force", "--subject", subject_id],
    )
    enriched = run_command(
        root,
        [python, "scripts/enrich_generated_pages.py", "--subject", subject_id],
    )
    return generated + "\n" + enriched


def run_repository_checks(root: Path, python: str) -> list[tuple[str, str]]:
    commands = [
        ("curriculum", [python, "scripts/validate_curriculum.py"]),
        ("agent-content", [python, "scripts/validate_agent_content.py"]),
        ("preview", [python, "scripts/check_generated_preview.py", "--limit", "84"]),
        ("links", [python, "scripts/validate_links.py", "--quiet"]),
    ]
    results: list[tuple[str, str]] = []
    for name, command in commands:
        results.append((name, run_command(root, command)))
    return results


def write_preview(path: Path, course: CourseContent) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(course.model_dump_json(indent=2) + "\n", encoding="utf-8")


def serialize_check_results(results: Iterable[tuple[str, str]]) -> str:
    return "\n\n".join(f"## {name}\n\n```text\n{output}\n```" for name, output in results)
