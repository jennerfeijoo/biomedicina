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
    def _schema_contract(schema: type[BaseModel]) -> str:
        if schema is CourseContent:
            return """
CourseContent = {
  id:string, area_id:string, status:"complete", description:string, level:string,
  estimated_workload:string, biomedical_connection:string,
  prerequisites:[string], course_competencies:[string], learning_objectives:[string],
  learning_outcomes:[string], modules:[string],
  detailed_units:[{
    unit:integer, title:string, description:string,
    explanations:[{title:string, paragraphs:[string], key_points:[string]}],
    topics:[string], learning_outcomes:[string],
    worked_examples:[{title:string, scenario:string, reasoning_steps:[string], conclusion:string}],
    activities:[string], self_check:[{question:string, answer:string}],
    common_misconceptions:[string], biomedical_applications:[string]
  }],
  practical_activities:[{title:string, description:string, weight:string|null, type:string|null, url:string|null}],
  assessment:[{title:string, description:string, weight:"NN%", type:string|null, url:string|null}],
  key_concepts:[string], related_subjects:[string],
  suggested_resources:[{title:string, description:string, weight:string|null, type:string|null, url:string|null}],
  sources_used:[{title:string, url:string, year:integer|null, type:string, authors:[string], abstract_excerpt:string}],
  generation_metadata:{autonomous_agent:true, content_model:string, review_model:string, generated_at:string, schema_version:string}
}
""".strip()
        if schema is CourseReview:
            return """
CourseReview = {
  approved:boolean,
  clarity_score:integer,
  scientific_score:integer,
  pedagogical_score:integer,
  completeness_score:integer,
  blocking_issues:[string],
  improvements:[string],
  unsupported_claims:[string]
}
""".strip()
        return "Devuelve un objeto JSON con todos los campos solicitados en el mensaje."

    @classmethod
    def _schema_fallback_prompt(
        cls,
        user_prompt: str,
        schema: type[BaseModel],
    ) -> str:
        return (
            user_prompt
            + "\n\nDEVUELVE UN ÚNICO OBJETO JSON VÁLIDO, SIN MARKDOWN NI TEXTO EXTERNO. "
            + "Respeta exactamente los nombres y tipos del contrato compacto siguiente. "
            + "Las longitudes, cardinalidades y demás restricciones se verificarán después con Pydantic. "
            + "Debes cerrar todas las cadenas, listas y llaves antes de terminar.\n\n"
            + "CONTRATO DE SALIDA:\n"
            + cls._schema_contract(schema)
        )

    @staticmethod
    def _chunk_content(chunk: Any) -> str:
        message = getattr(chunk, "message", None)
        content = getattr(message, "content", None) if message is not None else None
        if content is None and isinstance(chunk, dict):
            raw_message = chunk.get("message") or {}
            if isinstance(raw_message, dict):
                content = raw_message.get("content")
        return str(content or "")

    @staticmethod
    def _chunk_thinking(chunk: Any) -> str:
        message = getattr(chunk, "message", None)
        thinking = getattr(message, "thinking", None) if message is not None else None
        if thinking is None and isinstance(chunk, dict):
            raw_message = chunk.get("message") or {}
            if isinstance(raw_message, dict):
                thinking = raw_message.get("thinking")
        return str(thinking or "")

    @staticmethod
    def _chunk_field(chunk: Any, name: str) -> Any:
        value = getattr(chunk, name, None)
        if value is None and isinstance(chunk, dict):
            value = chunk.get(name)
        return value

    def _stream_chat_content(
        self,
        *,
        model: str,
        messages: list[dict[str, str]],
        output_format: dict[str, Any] | str,
        options: dict[str, Any],
        think: bool | str | None = None,
    ) -> str:
        request: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "format": output_format,
            "options": options,
            "stream": True,
        }
        if think is not None:
            request["think"] = think
        stream = self.client.chat(**request)

        pieces: list[str] = []
        received_chars = 0
        thinking_chars = 0
        next_progress = 5000
        done_reason: str | None = None
        prompt_tokens: int | None = None
        output_tokens: int | None = None

        for chunk in stream:
            current_reason = self._chunk_field(chunk, "done_reason")
            current_prompt_tokens = self._chunk_field(chunk, "prompt_eval_count")
            current_output_tokens = self._chunk_field(chunk, "eval_count")
            if current_reason:
                done_reason = str(current_reason)
            if current_prompt_tokens is not None:
                prompt_tokens = int(current_prompt_tokens)
            if current_output_tokens is not None:
                output_tokens = int(current_output_tokens)

            thinking_chars += len(self._chunk_thinking(chunk))
            text = self._chunk_content(chunk)
            if not text:
                continue
            pieces.append(text)
            received_chars += len(text)
            if received_chars >= next_progress:
                print(
                    f"[{model}] JSON recibido: {received_chars:,} caracteres",
                    flush=True,
                )
                while next_progress <= received_chars:
                    next_progress += 5000

        content = "".join(pieces).strip()
        metrics = [f"{len(content):,} caracteres"]
        if prompt_tokens is not None:
            metrics.append(f"entrada={prompt_tokens:,} tokens")
        if output_tokens is not None:
            metrics.append(f"salida={output_tokens:,} tokens")
        if thinking_chars:
            metrics.append(f"razonamiento={thinking_chars:,} caracteres")
        if done_reason:
            metrics.append(f"fin={done_reason}")

        if not content:
            detail = ", ".join(metrics)
            raise RuntimeError(f"{model} no devolvió contenido JSON ({detail})")

        print(f"[{model}] respuesta completa: " + ", ".join(metrics), flush=True)

        if done_reason and done_reason.casefold() in {"length", "max_tokens"}:
            raise RuntimeError(
                f"{model} agotó el presupuesto de salida ({output_tokens or 'desconocido'} tokens) "
                "antes de completar el JSON"
            )
        return content

    def _structured_chat(
        self,
        model: str,
        schema: type[BaseModel],
        user_prompt: str,
        temperature: float | None = None,
        *,
        think: bool | str | None = None,
    ) -> BaseModel:
        schema_json = schema.model_json_schema()
        output_budget = 2048 if schema is CourseReview else self.config.output_tokens
        options = {
            "temperature": self.config.temperature if temperature is None else temperature,
            "num_ctx": self.config.context_tokens,
            "num_predict": output_budget,
        }
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        try:
            content = self._stream_chat_content(
                model=model,
                messages=messages,
                output_format=schema_json,
                options=options,
                think=think,
            )
        except Exception as exc:
            if not self._is_grammar_error(exc):
                raise
            print(
                f"[{model}] el backend no pudo compilar el esquema; "
                "se usa JSON validado por Pydantic.",
                flush=True,
            )
            content = self._stream_chat_content(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": self._schema_fallback_prompt(user_prompt, schema),
                    },
                ],
                output_format="json",
                options=options,
                think=think,
            )

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
        result = self._structured_chat(
            self.config.review,
            CourseReview,
            prompt,
            temperature=0.0,
            think=False,
        )
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
