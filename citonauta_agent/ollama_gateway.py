from __future__ import annotations

import json
from collections.abc import Sequence
from typing import Any

from ollama import Client
from pydantic import BaseModel

from .config import ModelConfig
from .prompts import SYSTEM_PROMPT, generation_prompt, repair_prompt, review_prompt
from .schemas import CourseContent, CourseReview


class OllamaGateway:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.client = Client(host=config.host, timeout=config.timeout_seconds)

    def available_models(self) -> set[str]:
        response = self.client.list()
        models = getattr(response, "models", None) or response.get("models", [])
        names: set[str] = set()
        for model in models:
            name = getattr(model, "model", None) or getattr(model, "name", None)
            if name is None and isinstance(model, dict):
                name = model.get("model") or model.get("name")
            if name:
                names.add(str(name))
        return names

    def require_models(self) -> None:
        available = self.available_models()
        required = {self.config.content, self.config.review, self.config.embedding}
        missing = sorted(model for model in required if model not in available)
        if missing:
            raise RuntimeError(
                "Faltan modelos en Ollama: " + ", ".join(missing)
                + ". Instálalos con `ollama pull <modelo>`."
            )

    @staticmethod
    def _is_grammar_error(exc: Exception) -> bool:
        message = str(exc).casefold()
        return "failed to parse grammar" in message or (
            "failed to initialize samplers" in message and "grammar" in message
        )

    @staticmethod
    def _schema_fallback_prompt(user_prompt: str, schema: dict[str, Any]) -> str:
        schema_text = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
        return (
            user_prompt
            + "\n\nDEVUELVE UN ÚNICO OBJETO JSON VÁLIDO, SIN MARKDOWN NI TEXTO EXTERNO. "
            + "Respeta exactamente los nombres, tipos y campos obligatorios del siguiente esquema. "
            + "Las restricciones adicionales serán verificadas después con Pydantic.\n\n"
            + "ESQUEMA JSON:\n"
            + schema_text
        )

    def _structured_chat(
        self,
        model: str,
        schema: type[BaseModel],
        user_prompt: str,
        temperature: float | None = None,
    ) -> BaseModel:
        schema_json = schema.model_json_schema()
        options = {
            "temperature": self.config.temperature if temperature is None else temperature,
            "num_ctx": self.config.context_tokens,
        }
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = self.client.chat(
                model=model,
                messages=messages,
                format=schema_json,
                options=options,
            )
        except Exception as exc:
            if not self._is_grammar_error(exc):
                raise
            print(
                f"[{model}] el backend no pudo compilar el esquema; "
                "se usa JSON validado por Pydantic."
            )
            response = self.client.chat(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": self._schema_fallback_prompt(user_prompt, schema_json),
                    },
                ],
                format="json",
                options=options,
            )

        content = response.message.content
        return schema.model_validate_json(content)

    def generate_course(
        self,
        subject: dict[str, Any],
        baseline: dict[str, Any],
        sources: list[dict[str, Any]],
        related_context: list[dict[str, Any]],
    ) -> CourseContent:
        prompt = generation_prompt(
            subject,
            baseline,
            sources,
            related_context,
            self.config.content,
            self.config.review,
        )
        result = self._structured_chat(self.config.content, CourseContent, prompt)
        assert isinstance(result, CourseContent)
        return result

    def review_course(self, course: CourseContent, sources: list[dict[str, Any]]) -> CourseReview:
        prompt = review_prompt(
            course.model_dump_json(indent=2),
            json.dumps(sources, ensure_ascii=False, indent=2),
        )
        result = self._structured_chat(self.config.review, CourseReview, prompt, temperature=0.0)
        assert isinstance(result, CourseReview)
        return result

    def repair_course(
        self,
        course: CourseContent,
        review: CourseReview,
        validator_errors: str = "",
        *,
        technical: bool = False,
    ) -> CourseContent:
        model = self.config.technical if technical else self.config.content
        if model not in self.available_models():
            model = self.config.content
        prompt = repair_prompt(
            course.model_dump_json(indent=2),
            review.model_dump_json(indent=2),
            validator_errors,
        )
        result = self._structured_chat(model, CourseContent, prompt)
        assert isinstance(result, CourseContent)
        return result

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.client.embed(model=self.config.embedding, input=list(texts))
        embeddings = getattr(response, "embeddings", None)
        if embeddings is None and isinstance(response, dict):
            embeddings = response.get("embeddings")
        if not embeddings:
            raise RuntimeError("Ollama no devolvió embeddings")
        return [list(map(float, vector)) for vector in embeddings]
