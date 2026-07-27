#!/usr/bin/env python3
"""Detect duplicated or generic pedagogical text across developed courses.

The audit scans canonical unit JSON sources. It reports exact cross-course
blocks, near-duplicate candidates and recurrent phrases for human review. Shared
terminology is not treated as an error automatically.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATED_UNITS = ROOT / "data" / "generated_units"
REDEVELOPMENT = ROOT / "data" / "course_redevelopment"
NON_ALNUM_RE = re.compile(r"[^a-z0-9áéíóúüñ]+", re.IGNORECASE)
SPACE_RE = re.compile(r"\s+")
MIN_TOKENS = 10
NEAR_MIN_TOKENS = 18
SHINGLE_SIZE = 5
NEAR_SEQUENCE_THRESHOLD = 0.84
NEAR_JACCARD_THRESHOLD = 0.72
PHRASE_TOKENS = 7
PHRASE_MIN_SUBJECTS = 4


@dataclass(frozen=True)
class TextBlock:
    subject_id: str
    unit: int
    file: str
    path: str
    category: str
    text: str
    normalized: str
    tokens: tuple[str, ...]


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKD", text.lower())
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = NON_ALNUM_RE.sub(" ", value)
    return SPACE_RE.sub(" ", value).strip()


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: la raíz debe ser un objeto JSON")
    return data


def add_block(output: list[TextBlock], subject_id: str, unit: int, file: str, path: str, category: str, value: Any) -> None:
    if not isinstance(value, str):
        return
    text = SPACE_RE.sub(" ", value).strip()
    normalized = normalize(text)
    tokens = tuple(normalized.split())
    if len(tokens) < MIN_TOKENS:
        return
    output.append(TextBlock(subject_id, unit, file, path, category, text, normalized, tokens))


def add_list(output: list[TextBlock], subject_id: str, unit: int, file: str, path: str, category: str, values: Any) -> None:
    if not isinstance(values, list):
        return
    for index, value in enumerate(values):
        add_block(output, subject_id, unit, file, f"{path}[{index}]", category, value)


def extract_blocks(path: Path, subject_id: str) -> list[TextBlock]:
    data = load_json(path)
    unit = int(data.get("unit") or 0)
    file = str(path.relative_to(ROOT))
    output: list[TextBlock] = []
    add_block(output, subject_id, unit, file, "purpose", "purpose", data.get("purpose"))
    add_list(output, subject_id, unit, file, "learning_objectives", "learning_objective", data.get("learning_objectives"))

    for section_index, section in enumerate(data.get("theory_sections", [])):
        if not isinstance(section, dict):
            continue
        add_list(output, subject_id, unit, file, f"theory_sections[{section_index}].paragraphs", "theory_paragraph", section.get("paragraphs"))
        add_list(output, subject_id, unit, file, f"theory_sections[{section_index}].key_points", "key_point", section.get("key_points"))

    for index, example in enumerate(data.get("worked_examples", [])):
        if not isinstance(example, dict):
            continue
        for field in ("scenario", "solution", "interpretation"):
            add_block(output, subject_id, unit, file, f"worked_examples[{index}].{field}", f"worked_example_{field}", example.get(field))
        add_list(output, subject_id, unit, file, f"worked_examples[{index}].reasoning_steps", "worked_example_reasoning", example.get("reasoning_steps"))

    for index, activity in enumerate(data.get("guided_activities", [])):
        if not isinstance(activity, dict):
            continue
        for field, category in (("instructions", "activity_instruction"), ("problems", "activity_problem"), ("checking_criteria", "activity_criterion")):
            add_list(output, subject_id, unit, file, f"guided_activities[{index}].{field}", category, activity.get(field))

    for index, item in enumerate(data.get("common_errors", [])):
        if isinstance(item, dict):
            add_block(output, subject_id, unit, file, f"common_errors[{index}].error", "common_error", item.get("error"))
            add_block(output, subject_id, unit, file, f"common_errors[{index}].correction", "common_error_correction", item.get("correction"))

    for index, item in enumerate(data.get("self_assessment", [])):
        if isinstance(item, dict):
            add_block(output, subject_id, unit, file, f"self_assessment[{index}].question", "self_assessment_question", item.get("question"))
            add_block(output, subject_id, unit, file, f"self_assessment[{index}].answer", "self_assessment_answer", item.get("answer"))

    for index, item in enumerate(data.get("biomedical_connections", [])):
        if isinstance(item, dict):
            add_block(output, subject_id, unit, file, f"biomedical_connections[{index}].connection", "biomedical_connection", item.get("connection"))
    return output


def canonical_unit_dirs() -> list[tuple[str, Path]]:
    subjects = {path.name for path in GENERATED_UNITS.iterdir() if path.is_dir()} if GENERATED_UNITS.exists() else set()
    subjects.update(path.name for path in REDEVELOPMENT.iterdir() if path.is_dir()) if REDEVELOPMENT.exists() else None
    output: list[tuple[str, Path]] = []
    for subject_id in sorted(subjects):
        redevelopment_dir = REDEVELOPMENT / subject_id / "units"
        generated_dir = GENERATED_UNITS / subject_id
        if redevelopment_dir.exists() and list(redevelopment_dir.glob("unit-*.json")):
            output.append((subject_id, redevelopment_dir))
        elif generated_dir.exists() and list(generated_dir.glob("unit-*.json")):
            output.append((subject_id, generated_dir))
    return output


def serialize(block: TextBlock) -> dict[str, Any]:
    return {
        "subject_id": block.subject_id,
        "unit": block.unit,
        "file": block.file,
        "path": block.path,
        "category": block.category,
        "text": block.text,
        "token_count": len(block.tokens),
    }


def token_jaccard(left: TextBlock, right: TextBlock) -> float:
    left_set, right_set = set(left.tokens), set(right.tokens)
    union = left_set | right_set
    return len(left_set & right_set) / len(union) if union else 0.0


def exact_groups(blocks: list[TextBlock]) -> list[dict[str, Any]]:
    groups: dict[str, list[TextBlock]] = defaultdict(list)
    for block in blocks:
        groups[block.normalized].append(block)
    result: list[dict[str, Any]] = []
    for normalized, occurrences in groups.items():
        subjects = sorted({item.subject_id for item in occurrences})
        if len(subjects) < 2:
            continue
        result.append({
            "normalized_text": normalized,
            "subjects": subjects,
            "occurrences": [serialize(item) for item in occurrences],
        })
    result.sort(key=lambda item: (-len(item["subjects"]), -len(item["normalized_text"])))
    return result


def shingles(block: TextBlock) -> set[tuple[str, ...]]:
    return {
        block.tokens[index:index + SHINGLE_SIZE]
        for index in range(len(block.tokens) - SHINGLE_SIZE + 1)
    }


def near_pairs(blocks: list[TextBlock], limit: int) -> list[dict[str, Any]]:
    eligible = [block for block in blocks if len(block.tokens) >= NEAR_MIN_TOKENS]
    shingle_index: dict[tuple[str, tuple[str, ...]], list[int]] = defaultdict(list)
    block_shingles: list[set[tuple[str, ...]]] = []
    for index, block in enumerate(eligible):
        current = shingles(block)
        block_shingles.append(current)
        for shingle in current:
            shingle_index[(block.category, shingle)].append(index)

    candidate_counts: Counter[tuple[int, int]] = Counter()
    for indices in shingle_index.values():
        if len(indices) > 80:
            continue
        for left_pos, left in enumerate(indices):
            for right in indices[left_pos + 1:]:
                if eligible[left].subject_id == eligible[right].subject_id:
                    continue
                candidate_counts[(left, right)] += 1

    output: list[dict[str, Any]] = []
    for (left_index, right_index), shared in candidate_counts.most_common():
        if shared < 2:
            break
        left, right = eligible[left_index], eligible[right_index]
        if left.normalized == right.normalized:
            continue
        length_ratio = min(len(left.tokens), len(right.tokens)) / max(len(left.tokens), len(right.tokens))
        if length_ratio < 0.65:
            continue
        jaccard = token_jaccard(left, right)
        if jaccard < 0.5:
            continue
        sequence = difflib.SequenceMatcher(None, left.normalized, right.normalized, autojunk=False).ratio()
        if sequence < NEAR_SEQUENCE_THRESHOLD and jaccard < NEAR_JACCARD_THRESHOLD:
            continue
        output.append({
            "score": round(max(sequence, jaccard), 4),
            "sequence_ratio": round(sequence, 4),
            "token_jaccard": round(jaccard, 4),
            "shared_shingles": shared,
            "left": serialize(left),
            "right": serialize(right),
        })
        if len(output) >= limit:
            break
    output.sort(key=lambda item: (-item["score"], -item["shared_shingles"]))
    return output


def recurrent_phrases(blocks: list[TextBlock], limit: int) -> list[dict[str, Any]]:
    groups: dict[tuple[str, ...], dict[str, Any]] = {}
    for block in blocks:
        seen: set[tuple[str, ...]] = set()
        for index in range(len(block.tokens) - PHRASE_TOKENS + 1):
            phrase = block.tokens[index:index + PHRASE_TOKENS]
            if phrase in seen:
                continue
            seen.add(phrase)
            entry = groups.setdefault(phrase, {"subjects": set(), "occurrences": []})
            entry["subjects"].add(block.subject_id)
            if len(entry["occurrences"]) < 8:
                entry["occurrences"].append(serialize(block))
    candidates = []
    for phrase, entry in groups.items():
        if len(entry["subjects"]) < PHRASE_MIN_SUBJECTS:
            continue
        candidates.append({
            "phrase": " ".join(phrase),
            "subjects": sorted(entry["subjects"]),
            "subject_count": len(entry["subjects"]),
            "examples": entry["occurrences"],
        })
    candidates.sort(key=lambda item: (-item["subject_count"], item["phrase"]))
    return candidates[:limit]


def audit(near_limit: int, phrase_limit: int) -> dict[str, Any]:
    blocks: list[TextBlock] = []
    technical_errors: list[str] = []
    subject_counts: dict[str, int] = {}
    for subject_id, unit_dir in canonical_unit_dirs():
        before = len(blocks)
        for path in sorted(unit_dir.glob("unit-*.json")):
            try:
                blocks.extend(extract_blocks(path, subject_id))
            except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                technical_errors.append(str(exc))
        subject_counts[subject_id] = len(blocks) - before

    exact = exact_groups(blocks)
    near = near_pairs(blocks, near_limit)
    phrases = recurrent_phrases(blocks, phrase_limit)
    return {
        "summary": {
            "subjects_scanned": len(subject_counts),
            "text_blocks_scanned": len(blocks),
            "exact_cross_course_groups": len(exact),
            "near_duplicate_pairs_reported": len(near),
            "recurrent_phrase_groups_reported": len(phrases),
            "technical_errors": len(technical_errors),
            "disclaimer": "Los resultados son candidatos para revisión editorial; no convierten terminología compartida en un defecto automático.",
        },
        "subject_block_counts": subject_counts,
        "exact_cross_course_duplicates": exact,
        "near_duplicate_pairs": near,
        "recurrent_phrases": phrases,
        "technical_errors": technical_errors,
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Auditoría de especificidad entre asignaturas",
        "",
        summary["disclaimer"],
        "",
        f"- Asignaturas con unidades JSON: {summary['subjects_scanned']}",
        f"- Bloques pedagógicos analizados: {summary['text_blocks_scanned']}",
        f"- Grupos exactos entre asignaturas: {summary['exact_cross_course_groups']}",
        f"- Pares casi duplicados reportados: {summary['near_duplicate_pairs_reported']}",
        f"- Frases recurrentes reportadas: {summary['recurrent_phrase_groups_reported']}",
        f"- Errores técnicos: {summary['technical_errors']}",
        "",
        "## Duplicados exactos",
        "",
    ]
    if not report["exact_cross_course_duplicates"]:
        lines.append("No se detectaron bloques exactos compartidos entre asignaturas.")
    for group in report["exact_cross_course_duplicates"][:50]:
        lines.append(f"### {', '.join(group['subjects'])}")
        for occurrence in group["occurrences"]:
            lines.append(f"- `{occurrence['file']}::{occurrence['path']}` — {occurrence['text']}")
        lines.append("")

    lines.extend(["## Pares casi duplicados", ""])
    if not report["near_duplicate_pairs"]:
        lines.append("No se detectaron pares sobre los umbrales configurados.")
    for pair in report["near_duplicate_pairs"]:
        lines.append(f"- `{pair['left']['subject_id']}` ↔ `{pair['right']['subject_id']}` · score {pair['score']}: {pair['left']['text']} / {pair['right']['text']}")

    lines.extend(["", "## Frases recurrentes", ""])
    if not report["recurrent_phrases"]:
        lines.append("No se detectaron frases recurrentes en cuatro o más asignaturas.")
    for item in report["recurrent_phrases"]:
        lines.append(f"- **{item['phrase']}** — {item['subject_count']} asignaturas: {', '.join(item['subjects'])}")

    if report["technical_errors"]:
        lines.extend(["", "## Errores técnicos", ""])
        lines.extend(f"- {error}" for error in report["technical_errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--near-limit", type=int, default=100)
    parser.add_argument("--phrase-limit", type=int, default=100)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--fail-on-technical-errors", action="store_true")
    args = parser.parse_args()
    report = audit(args.near_limit, args.phrase_limit)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 1 if args.fail_on_technical_errors and report["summary"]["technical_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
