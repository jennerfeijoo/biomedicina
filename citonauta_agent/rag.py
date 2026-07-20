from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

from .catalog import CurriculumCatalog, SubjectRef
from .ollama_gateway import OllamaGateway


def _cosine(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right, strict=False))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def _short_list(value: Any, limit: int) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item)[:180] for item in value[:limit] if str(item).strip()]


class CatalogRAG:
    def __init__(
        self,
        catalog: CurriculumCatalog,
        ollama: OllamaGateway,
        cache_path: Path,
    ):
        self.catalog = catalog
        self.ollama = ollama
        self.cache_path = cache_path

    def _fingerprint(self, subjects: list[SubjectRef], texts: list[str]) -> str:
        payload = {
            "model": self.ollama.config.embedding,
            "subjects": [subject.id for subject in subjects],
            "texts": texts,
        }
        return hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def _load_or_build(self) -> tuple[list[SubjectRef], list[list[float]]]:
        subjects = self.catalog.all_subjects()
        texts = [self.catalog.descriptor(subject) for subject in subjects]
        fingerprint = self._fingerprint(subjects, texts)
        if self.cache_path.exists():
            try:
                cached = json.loads(self.cache_path.read_text(encoding="utf-8"))
                if cached.get("fingerprint") == fingerprint:
                    return subjects, cached["embeddings"]
            except (OSError, ValueError, KeyError):
                pass

        embeddings = self.ollama.embed(texts)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(
                {"fingerprint": fingerprint, "embeddings": embeddings},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        return subjects, embeddings

    def related(self, subject: SubjectRef, limit: int) -> list[dict[str, Any]]:
        subjects, embeddings = self._load_or_build()
        by_id = {item.id: index for index, item in enumerate(subjects)}
        query_index = by_id[subject.id]
        query = embeddings[query_index]
        ranking = sorted(
            (
                (_cosine(query, vector), candidate)
                for candidate, vector in zip(subjects, embeddings, strict=True)
                if candidate.id != subject.id
            ),
            key=lambda item: item[0],
            reverse=True,
        )[:limit]

        results: list[dict[str, Any]] = []
        for score, candidate in ranking:
            baseline = self.catalog.baseline(candidate.id)
            results.append(
                {
                    "similarity": round(score, 4),
                    **candidate.as_prompt_dict(),
                    "baseline_summary": {
                        "modules": _short_list(baseline.get("modules"), 6),
                        "key_concepts": _short_list(baseline.get("key_concepts"), 10),
                        "learning_objectives": _short_list(
                            baseline.get("learning_objectives"), 6
                        ),
                    },
                }
            )
        return results
