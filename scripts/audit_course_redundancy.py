#!/usr/bin/env python3
"""Audit exact and near-duplicate educational text across course units.

The audit extracts pedagogical prose from redevelopment JSON files, excludes
bibliography and metadata, and reports cross-unit candidates for human review.
It does not edit content and does not treat shared terminology as an error.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"
NON_ALNUM_RE = re.compile(r"[^a-z0-9áéíóúüñ]+", re.IGNORECASE)
SPACE_RE = re.compile(r"\s+")
MIN_TOKENS = 8
NEAR_MIN_TOKENS = 16
NEAR_SEQUENCE_THRESHOLD = 0.82
NEAR_JACCARD_THRESHOLD = 0.68
PHRASE_TOKENS = 6
PHRASE_MIN_UNITS = 3


@dataclass(frozen=True)
class TextBlock:
    unit: int
    path: str
    category: str
    text: str
    normalized: str
    tokens: tuple[str, ...]


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: la unidad debe ser un objeto JSON")
    return data


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKD", text.lower())
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = NON_ALNUM_RE.sub(" ", value)
    return SPACE_RE.sub(" ", value).strip()


def add_block(
    output: list[TextBlock], unit: int, path: str, category: str, value: Any
) -> None:
    if not isinstance(value, str):
        return
    text = SPACE_RE.sub(" ", value).strip()
    normalized = normalize(text)
    tokens = tuple(normalized.split())
    if len(tokens) < MIN_TOKENS:
        return
    output.append(TextBlock(unit, path, category, text, normalized, tokens))


def add_string_list(
    output: list[TextBlock], unit: int, base_path: str, category: str, values: Any
) -> None:
    if not isinstance(values, list):
        return
    for index, value in enumerate(values):
        add_block(output, unit, f"{base_path}[{index}]", category, value)


def extract_blocks(unit_path: Path) -> list[TextBlock]:
    data = load_json(unit_path)
    unit = int(data.get("unit"))
    blocks: list[TextBlock] = []
    add_block(blocks, unit, "purpose", "purpose", data.get("purpose"))
    add_string_list(
        blocks, unit, "learning_objectives", "learning_objective", data.get("learning_objectives")
    )

    for section_index, section in enumerate(data.get("theory_sections", [])):
        if not isinstance(section, dict):
            continue
        add_string_list(
            blocks,
            unit,
            f"theory_sections[{section_index}].paragraphs",
            "theory_paragraph",
            section.get("paragraphs"),
        )
        add_string_list(
            blocks,
            unit,
            f"theory_sections[{section_index}].key_points",
            "key_point",
            section.get("key_points"),
        )

    for index, item in enumerate(data.get("glossary", [])):
        if isinstance(item, dict):
            add_block(
                blocks,
                unit,
                f"glossary[{index}].definition",
                "glossary_definition",
                item.get("definition"),
            )

    for index, example in enumerate(data.get("worked_examples", [])):
        if not isinstance(example, dict):
            continue
        for field in ("scenario", "solution", "interpretation"):
            add_block(
                blocks,
                unit,
                f"worked_examples[{index}].{field}",
                f"worked_example_{field}",
                example.get(field),
            )
        add_string_list(
            blocks,
            unit,
            f"worked_examples[{index}].reasoning_steps",
            "worked_example_reasoning",
            example.get("reasoning_steps"),
        )
        add_string_list(
            blocks,
            unit,
            f"worked_examples[{index}].limitations",
            "worked_example_limitation",
            example.get("limitations"),
        )

    for index, activity in enumerate(data.get("guided_activities", [])):
        if not isinstance(activity, dict):
            continue
        for field, category in (
            ("instructions", "activity_instruction"),
            ("problems", "activity_problem"),
            ("checking_criteria", "activity_criterion"),
        ):
            add_string_list(
                blocks,
                unit,
                f"guided_activities[{index}].{field}",
                category,
                activity.get(field),
            )

    for index, item in enumerate(data.get("common_errors", [])):
        if not isinstance(item, dict):
            continue
        add_block(blocks, unit, f"common_errors[{index}].error", "common_error", item.get("error"))
        add_block(
            blocks,
            unit,
            f"common_errors[{index}].correction",
            "common_error_correction",
            item.get("correction"),
        )

    for index, item in enumerate(data.get("self_assessment", [])):
        if not isinstance(item, dict):
            continue
        add_block(
            blocks,
            unit,
            f"self_assessment[{index}].question",
            "self_assessment_question",
            item.get("question"),
        )
        add_block(
            blocks,
            unit,
            f"self_assessment[{index}].answer",
            "self_assessment_answer",
            item.get("answer"),
        )

    for index, item in enumerate(data.get("biomedical_connections", [])):
        if isinstance(item, dict):
            add_block(
                blocks,
                unit,
                f"biomedical_connections[{index}].connection",
                "biomedical_connection",
                item.get("connection"),
            )
    return blocks


def serialize(block: TextBlock) -> dict[str, Any]:
    return {
        "unit": block.unit,
        "path": block.path,
        "category": block.category,
        "text": block.text,
        "token_count": len(block.tokens),
    }


def exact_duplicate_groups(blocks: list[TextBlock]) -> list[dict[str, Any]]:
    groups: dict[str, list[TextBlock]] = defaultdict(list)
    for block in blocks:
        groups[block.normalized].append(block)
    output: list[dict[str, Any]] = []
    for normalized, occurrences in groups.items():
        units = sorted({block.unit for block in occurrences})
        if len(units) < 2:
            continue
        output.append(
            {
                "normalized_text": normalized,
                "units": units,
                "occurrences": [serialize(block) for block in occurrences],
            }
        )
    output.sort(key=lambda group: (-len(group["units"]), -len(group["normalized_text"])))
    return output


def token_jaccard(left: TextBlock, right: TextBlock) -> float:
    left_set = set(left.tokens)
    right_set = set(right.tokens)
    union = left_set | right_set
    return len(left_set & right_set) / len(union) if union else 0.0


def sequence_ratio(left: TextBlock, right: TextBlock) -> float:
    return difflib.SequenceMatcher(None, left.normalized, right.normalized, autojunk=False).ratio()


def near_duplicate_pairs(blocks: list[TextBlock], limit: int) -> list[dict[str, Any]]:
    eligible = [block for block in blocks if len(block.tokens) >= NEAR_MIN_TOKENS]
    pairs: list[dict[str, Any]] = []
    for left_index, left in enumerate(eligible):
        for right in eligible[left_index + 1 :]:
            if left.unit == right.unit or left.normalized == right.normalized:
                continue
            if left.category != right.category:
                continue
            length_ratio = min(len(left.tokens), len(right.tokens)) / max(
                len(left.tokens), len(right.tokens)
            )
            if length_ratio < 0.65:
                continue
            jaccard = token_jaccard(left, right)
            if jaccard < 0.45:
                continue
            sequence = sequence_ratio(left, right)
            if sequence < NEAR_SEQUENCE_THRESHOLD and jaccard < NEAR_JACCARD_THRESHOLD:
                continue
            pairs.append(
                {
                    "score": round(max(sequence, jaccard), 4),
                    "sequence_ratio": round(sequence, 4),
                    "token_jaccard": round(jaccard, 4),
                    "left": serialize(left),
                    "right": serialize(right),
                }
            )
    pairs.sort(key=lambda pair: (-pair["score"], -pair["token_jaccard"]))
    return pairs[:limit]


def phrase_candidates(blocks: list[TextBlock], limit: int) -> list[dict[str, Any]]:
    groups: dict[tuple[str, ...], list[TextBlock]] = defaultdict(list)
    for block in blocks:
        seen_in_block: set[tuple[str, ...]] = set()
        for index in range(len(block.tokens) - PHRASE_TOKENS + 1):
            phrase = block.tokens[index : index + PHRASE_TOKENS]
            if phrase in seen_in_block:
                continue
            seen_in_block.add(phrase)
            groups[phrase].append(block)

    candidates: list[dict[str, Any]] = []
    for phrase, occurrences in groups.items():
        units = sorted({block.unit for block in occurrences})
        if len(units) < PHRASE_MIN_UNITS:
            continue
        candidates.append(
            {
                "phrase": " ".join(phrase),
                "units": units,
                "unit_count": len(units),
                "occurrence_count": len(occurrences),
                "examples": [serialize(block) for block in occurrences[:6]],
            }
        )
    candidates.sort(
        key=lambda item: (-item["unit_count"], -item["occurrence_count"], item["phrase"])
    )

    selected: list[dict[str, Any]] = []
    for candidate in candidates:
        words = set(candidate["phrase"].split())
        if any(
            candidate["units"] == existing["units"]
            and len(words & set(existing["phrase"].split())) / len(words | set(existing["phrase"].split()))
            >= 0.8
            for existing in selected
        ):
            continue
        selected.append(candidate)
        if len(selected) >= limit:
            break
    return selected


def audit(subject_id: str, near_limit: int, phrase_limit: int) -> dict[str, Any]:
    unit_dir = REDEVELOPMENT_ROOT / subject_id / "units"
    if not unit_dir.exists():
        raise FileNotFoundError(f"No existe {unit_dir}")
    blocks: list[TextBlock] = []
    for unit_path in sorted(unit_dir.glob("unit-*.json")):
        blocks.extend(extract_blocks(unit_path))
    exact = exact_duplicate_groups(blocks)
    near = near_duplicate_pairs(blocks, near_limit)
    phrases = phrase_candidates(blocks, phrase_limit)
    return {
        "summary": {
            "subject_id": subject_id,
            "units_scanned": len({block.unit for block in blocks}),
            "text_blocks_scanned": len(blocks),
            "exact_cross_unit_duplicate_groups": len(exact),
            "near_duplicate_pairs_reported": len(near),
            "recurrent_phrase_groups_reported": len(phrases),
            "near_sequence_threshold": NEAR_SEQUENCE_THRESHOLD,
            "near_jaccard_threshold": NEAR_JACCARD_THRESHOLD,
            "phrase_token_length": PHRASE_TOKENS,
            "phrase_min_units": PHRASE_MIN_UNITS,
        },
        "exact_cross_unit_duplicates": exact,
        "near_duplicate_pairs": near,
        "recurrent_phrases": phrases,
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        f"# Auditoría léxica de redundancia — {summary['subject_id']}",
        "",
        "El informe identifica candidatos para revisión humana. La repetición de terminología o de un principio transversal no constituye por sí sola un defecto.",
        "",
        "## Resumen",
        "",
        f"- Unidades: {summary['units_scanned']}",
        f"- Bloques de texto: {summary['text_blocks_scanned']}",
        f"- Grupos exactos entre unidades: {summary['exact_cross_unit_duplicate_groups']}",
        f"- Pares casi duplicados reportados: {summary['near_duplicate_pairs_reported']}",
        f"- Frases recurrentes reportadas: {summary['recurrent_phrase_groups_reported']}",
        "",
        "## Duplicados exactos entre unidades",
        "",
    ]
    if not report["exact_cross_unit_duplicates"]:
        lines.append("No se detectaron bloques exactos compartidos entre unidades.")
    for index, group in enumerate(report["exact_cross_unit_duplicates"], start=1):
        lines.extend([f"### Exacto {index} — unidades {', '.join(map(str, group['units']))}", ""])
        for occurrence in group["occurrences"]:
            lines.append(
                f"- U{occurrence['unit']} `{occurrence['path']}`: {occurrence['text']}"
            )
        lines.append("")

    lines.extend(["## Pares casi duplicados", ""])
    if not report["near_duplicate_pairs"]:
        lines.append("No se detectaron pares que superen los umbrales configurados.")
    for index, pair in enumerate(report["near_duplicate_pairs"], start=1):
        lines.extend(
            [
                f"### Par {index} — puntuación {pair['score']}",
                "",
                f"- U{pair['left']['unit']} `{pair['left']['path']}`: {pair['left']['text']}",
                f"- U{pair['right']['unit']} `{pair['right']['path']}`: {pair['right']['text']}",
                f"- Sequence ratio: {pair['sequence_ratio']}; Jaccard: {pair['token_jaccard']}",
                "",
            ]
        )

    lines.extend(["## Frases recurrentes", ""])
    if not report["recurrent_phrases"]:
        lines.append("No se detectaron frases recurrentes según los criterios configurados.")
    for item in report["recurrent_phrases"]:
        lines.append(
            f"- **{item['phrase']}** — {item['unit_count']} unidades; {item['occurrence_count']} bloques"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", default="biologia-desarrollo")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--near-limit", type=int, default=100)
    parser.add_argument("--phrase-limit", type=int, default=100)
    args = parser.parse_args()
    try:
        report = audit(args.subject_id, args.near_limit, args.phrase_limit)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
