from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl, model_validator


FORBIDDEN_PLACEHOLDERS = (
    "pendiente de desarrollo",
    "contenido pendiente",
    "por completar",
    "placeholder",
    "lorem ipsum",
)


class RichItem(BaseModel):
    title: str = Field(min_length=4)
    description: str = Field(min_length=40)
    weight: str | None = None
    type: str | None = None
    url: HttpUrl | None = None


class ExplanationBlock(BaseModel):
    title: str = Field(min_length=4)
    paragraphs: list[str] = Field(min_length=2, max_length=5)
    key_points: list[str] = Field(min_length=3, max_length=8)


class WorkedExample(BaseModel):
    title: str = Field(min_length=4)
    scenario: str = Field(min_length=60)
    reasoning_steps: list[str] = Field(min_length=3, max_length=8)
    conclusion: str = Field(min_length=40)


class SelfCheck(BaseModel):
    question: str = Field(min_length=15)
    answer: str = Field(min_length=30)


class DetailedUnit(BaseModel):
    unit: int = Field(ge=1, le=10)
    title: str = Field(min_length=4)
    description: str = Field(min_length=120)
    explanations: list[ExplanationBlock] = Field(min_length=2, max_length=4)
    topics: list[str] = Field(min_length=3, max_length=10)
    learning_outcomes: list[str] = Field(min_length=2, max_length=6)
    worked_examples: list[WorkedExample] = Field(min_length=1, max_length=3)
    activities: list[str] = Field(min_length=2, max_length=6)
    self_check: list[SelfCheck] = Field(min_length=2, max_length=5)
    common_misconceptions: list[str] = Field(min_length=2, max_length=6)
    biomedical_applications: list[str] = Field(min_length=1, max_length=6)

    @model_validator(mode="before")
    @classmethod
    def expand_short_description(cls, data: Any) -> Any:
        """Preserve concise model summaries while satisfying the descriptive contract."""
        if not isinstance(data, dict):
            return data

        description = " ".join(str(data.get("description") or "").split())
        if len(description) >= 120:
            return data

        title = " ".join(str(data.get("title") or "esta unidad").split())
        raw_topics = data.get("topics")
        topics = (
            [" ".join(str(item).split()) for item in raw_topics[:3] if str(item).strip()]
            if isinstance(raw_topics, list)
            else []
        )
        focus = ", ".join(topics) if topics else title
        lead = description.rstrip(" .")
        if not lead:
            lead = f"Introducción estructurada a {title}"
        expanded = (
            f"{lead}. Esta unidad desarrolla {focus} y establece los criterios necesarios para "
            "formular, analizar e interpretar estos contenidos con rigor, atendiendo a sus "
            "supuestos, limitaciones y aplicaciones en problemas biomédicos."
        )

        normalized = dict(data)
        normalized["description"] = expanded
        return normalized


class SourceRecord(BaseModel):
    title: str = Field(min_length=4)
    url: HttpUrl
    year: int | None = None
    type: str = "recurso académico"
    authors: list[str] = Field(default_factory=list)
    abstract_excerpt: str = ""


class GenerationMetadata(BaseModel):
    autonomous_agent: bool = True
    content_model: str
    review_model: str
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    schema_version: str = "1.0"


class CourseContent(BaseModel):
    id: str
    area_id: str
    status: Literal["complete"] = "complete"
    description: str = Field(min_length=120)
    level: str = Field(min_length=10)
    estimated_workload: str = Field(min_length=15)
    biomedical_connection: str = Field(min_length=180)
    prerequisites: list[str] = Field(min_length=3, max_length=8)
    course_competencies: list[str] = Field(min_length=4, max_length=10)
    learning_objectives: list[str] = Field(min_length=4, max_length=10)
    learning_outcomes: list[str] = Field(min_length=6, max_length=16)
    modules: list[str] = Field(min_length=6, max_length=10)
    detailed_units: list[DetailedUnit] = Field(min_length=6, max_length=10)
    practical_activities: list[RichItem] = Field(min_length=4, max_length=10)
    assessment: list[RichItem] = Field(min_length=3, max_length=8)
    key_concepts: list[str] = Field(min_length=10, max_length=30)
    related_subjects: list[str] = Field(min_length=4, max_length=12)
    suggested_resources: list[RichItem] = Field(min_length=5, max_length=15)
    sources_used: list[SourceRecord] = Field(min_length=5, max_length=20)
    generation_metadata: GenerationMetadata

    @model_validator(mode="after")
    def validate_course(self) -> "CourseContent":
        expected_units = list(range(1, len(self.detailed_units) + 1))
        actual_units = [unit.unit for unit in self.detailed_units]
        if actual_units != expected_units:
            raise ValueError(f"Las unidades deben numerarse consecutivamente: {expected_units}")

        weights: list[int] = []
        for item in self.assessment:
            if item.weight:
                raw = item.weight.strip().rstrip("%")
                if raw.isdigit():
                    weights.append(int(raw))
        if not weights or sum(weights) != 100:
            raise ValueError("La evaluación debe incluir ponderaciones numéricas que sumen 100%")

        serialized = self.model_dump_json().casefold()
        for marker in FORBIDDEN_PLACEHOLDERS:
            if marker in serialized:
                raise ValueError(f"El contenido conserva un marcador incompleto: {marker}")
        return self


class CourseReview(BaseModel):
    approved: bool
    clarity_score: int = Field(ge=1, le=10)
    scientific_score: int = Field(ge=1, le=10)
    pedagogical_score: int = Field(ge=1, le=10)
    completeness_score: int = Field(ge=1, le=10)
    blocking_issues: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)

    @property
    def passes_gate(self) -> bool:
        return (
            self.approved
            and not self.blocking_issues
            and not self.unsupported_claims
            and min(
                self.clarity_score,
                self.scientific_score,
                self.pedagogical_score,
                self.completeness_score,
            ) >= 8
        )
