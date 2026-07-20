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
        return [
            {
                "similarity": round(score, 4),
                **candidate.as_prompt_dict(),
                "baseline_summary": self.catalog.baseline(candidate.id),
            }
            for score, candidate in ranking
        ]
