from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path
from typing import Any

from .catalog import CurriculumCatalog, SubjectRef
from .config import AgentConfig
from .git_workflow import GitWorkflow
from .ollama_gateway import OllamaGateway
from .quality import (
    generate_subject,
    run_repository_checks,
    serialize_check_results,
    validate_semantics,
    write_preview,
)
from .rag import CatalogRAG
from .research import ResearchClient
from .schemas import (
    CourseContent,
    CourseReview,
    GenerationMetadata,
    RichItem,
    SourceRecord,
)
from .state import AgentState


class CitonautaAgent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.catalog = CurriculumCatalog(config.root)
        self.ollama = OllamaGateway(config.models)
        self.research = ResearchClient()
        self.state = AgentState(config.state_path / "state.sqlite3")
        self.git = GitWorkflow(config.root, config.git)
        self.rag = CatalogRAG(
            self.catalog,
            self.ollama,
            config.state_path / "catalog_embeddings.json",
        )

    def preflight(self, publish: bool = True) -> None:
        self.ollama.require_models()
        if publish:
            self.git.preflight()
        required_files = [
            self.config.root / "scripts" / "generate_site.py",
            self.config.root / "scripts" / "validate_curriculum.py",
            self.config.root / "data" / "citonauta_curriculum.json",
            self.config.root / "templates" / "asignatura.html",
        ]
        missing = [str(path) for path in required_files if not path.exists()]
        if missing:
            raise RuntimeError("Faltan archivos requeridos:\n- " + "\n- ".join(missing))

    @staticmethod
    def _resource_description(item: dict[str, Any]) -> str:
        abstract = str(item.get("abstract_excerpt") or "").strip()
        if len(abstract) >= 40:
            return abstract[:500]
        description = str(item.get("description") or "").strip()
        if len(description) >= 40:
            return description[:500]
        return "Recurso académico seleccionado para ampliar y contrastar los contenidos de esta asignatura."

    def _source_pool(
        self,
        baseline: dict[str, Any],
        research: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        combined: list[dict[str, Any]] = []
        for item in baseline.get("suggested_resources", []):
            url = str(item.get("url") or "").strip()
            if not url.startswith(("https://", "http://")):
                continue
            combined.append(
                {
                    "title": str(item.get("title") or "Recurso académico"),
                    "url": url,
                    "year": None,
                    "type": str(item.get("type") or "recurso abierto"),
                    "authors": [],
                    "abstract_excerpt": self._resource_description(item),
                }
            )
        combined.extend(research)

        unique: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in combined:
            url = str(item.get("url") or "").strip()
            marker = url.casefold()
            if not marker or marker in seen:
                continue
            seen.add(marker)
            unique.append(item)
        if len(unique) < 5:
            raise RuntimeError("No se pudo construir un conjunto mínimo de cinco fuentes válidas.")
        return unique[:20]

    def _normalize_course(
        self,
        course: CourseContent,
        subject: SubjectRef,
        source_pool: list[dict[str, Any]],
    ) -> CourseContent:
        course.id = subject.id
        course.area_id = subject.area_id
        course.status = "complete"
        course.generation_metadata = GenerationMetadata(
            content_model=self.config.models.content,
            review_model=self.config.models.review,
        )

        source_records: list[SourceRecord] = []
        resources: list[RichItem] = []
        for item in source_pool:
            source = SourceRecord.model_validate(item)
            source_records.append(source)
            resources.append(
                RichItem(
                    title=source.title,
                    description=self._resource_description(item),
                    type=source.type,
                    url=source.url,
                )
            )
        course.sources_used = source_records[:15]
        course.suggested_resources = resources[:12]
        return CourseContent.model_validate(course.model_dump(mode="json"))

    def _produce_course(
        self,
        subject: SubjectRef,
    ) -> tuple[CourseContent, CourseReview, list[dict[str, Any]]]:
        baseline = self.catalog.baseline(subject.id)
        research = self.research.collect(
            subject.title,
            subject.description,
            self.config.generation.research_results,
            self.config.generation.openalex_enabled,
            self.config.generation.europe_pmc_enabled,
        )
        source_pool = self._source_pool(baseline, research)
        related = self.rag.related(subject, self.config.generation.related_courses)

        course: CourseContent | None = None
        review: CourseReview | None = None
        last_generation_error = ""
        for attempt in range(1, self.config.generation.maximum_generation_attempts + 1):
            print(f"[{subject.id}] generación {attempt}")
            try:
                if course is None:
                    course = self.ollama.generate_course(
                        subject.as_prompt_dict(), baseline, source_pool, related
                    )
                else:
                    assert review is not None
                    course = self.ollama.repair_course(course, review, technical=False)
                course = self._normalize_course(course, subject, source_pool)
            except Exception as exc:
                last_generation_error = f"{type(exc).__name__}: {exc}"
                print(f"[{subject.id}] salida inválida: {last_generation_error}")
                course = None
                review = None
                continue

            semantic_errors = validate_semantics(
                course, self.config.generation.minimum_course_words
            )
            if semantic_errors:
                review = CourseReview(
                    approved=False,
                    clarity_score=6,
                    scientific_score=7,
                    pedagogical_score=6,
                    completeness_score=5,
                    blocking_issues=semantic_errors,
                    improvements=[],
                    unsupported_claims=[],
                )
                continue

            print(f"[{subject.id}] revisión independiente")
            review = self.ollama.review_course(course, source_pool)
            if review.passes_gate:
                return course, review, source_pool
            print(
                f"[{subject.id}] revisión rechazada: "
                + "; ".join(review.blocking_issues + review.unsupported_claims)
            )

        if course is None or review is None:
            raise RuntimeError(
                "El modelo no produjo JSON válido después de "
                f"{self.config.generation.maximum_generation_attempts} intentos. "
                + last_generation_error
            )
        raise RuntimeError(
            "El contenido no superó la revisión después de "
            f"{self.config.generation.maximum_generation_attempts} intentos. "
            + "; ".join(review.blocking_issues + review.unsupported_claims)
        )

    def _write_pr_body(
        self,
        subject: SubjectRef,
        review: CourseReview,
        sources: list[dict[str, Any]],
        check_results: list[tuple[str, str]],
    ) -> Path:
        path = self.config.state_path / "pr-body.md"
        source_lines = "\n".join(
            f"- [{item['title']}]({item['url']})" for item in sources[:12]
        )
        body = f"""## Asignatura completada

**{subject.title}** (`{subject.area_id}/{subject.id}`)

### Contenido incorporado

- Explicaciones conceptuales extensas por unidad.
- Ejemplos guiados con razonamiento paso a paso.
- Actividades, errores frecuentes y preguntas de autoevaluación.
- Aplicaciones biomédicas y evaluación alineada con los resultados de aprendizaje.
- Metadatos de generación y trazabilidad de fuentes.

### Revisión automática

- Claridad: {review.clarity_score}/10
- Rigor científico: {review.scientific_score}/10
- Calidad pedagógica: {review.pedagogical_score}/10
- Completitud: {review.completeness_score}/10

### Fuentes utilizadas

{source_lines}

### Validaciones

{serialize_check_results(check_results)}
"""
        path.write_text(body, encoding="utf-8")
        return path

    def process_subject(
        self,
        subject: SubjectRef,
        *,
        dry_run: bool = False,
        publish: bool = True,
    ) -> None:
        branch: str | None = None
        self.state.update(subject.id, "generating", increment_attempt=True)
        try:
            course, review, sources = self._produce_course(subject)
            preview_path = self.config.state_path / "previews" / f"{subject.id}.json"
            write_preview(preview_path, course)
            print(f"[{subject.id}] vista previa: {preview_path}")
            if dry_run:
                self.state.update(subject.id, "previewed")
                return

            if publish:
                self.git.checkout_base()
                branch = self.git.create_branch(subject)
                self.state.update(subject.id, "integrating", branch=branch)

            overlay_path = self.catalog.write_overlay(
                subject, course.model_dump(mode="json", exclude_none=True)
            )
            generate_subject(self.config.root, sys.executable, subject.id)

            check_results: list[tuple[str, str]] = []
            for repair_number in range(
                self.config.generation.maximum_validation_repairs + 1
            ):
                try:
                    check_results = run_repository_checks(self.config.root, sys.executable)
                    break
                except RuntimeError as exc:
                    last_error = str(exc)
                    if repair_number >= self.config.generation.maximum_validation_repairs:
                        raise
                    print(f"[{subject.id}] reparación técnica {repair_number + 1}")
                    technical_review = CourseReview(
                        approved=False,
                        clarity_score=7,
                        scientific_score=7,
                        pedagogical_score=7,
                        completeness_score=6,
                        blocking_issues=[last_error],
                        improvements=[],
                        unsupported_claims=[],
                    )
                    course = self.ollama.repair_course(
                        course, technical_review, validator_errors=last_error, technical=True
                    )
                    course = self._normalize_course(course, subject, sources)
                    self.catalog.write_overlay(
                        subject, course.model_dump(mode="json", exclude_none=True)
                    )
                    generate_subject(self.config.root, sys.executable, subject.id)

            if not publish:
                self.state.update(subject.id, "validated")
                return

            expected = {
                overlay_path.relative_to(self.config.root).as_posix(),
                self.catalog.html_path(subject).relative_to(self.config.root).as_posix(),
            }
            self.git.ensure_expected_changes(expected)
            commit = self.git.commit(
                sorted(expected), f"Complete {subject.title} course content"
            )
            print(f"[{subject.id}] commit {commit}")

            if self.config.git.auto_push:
                assert branch is not None
                self.git.push(branch)
            if self.config.git.create_pull_request:
                assert branch is not None
                body_path = self._write_pr_body(subject, review, sources, check_results)
                pr_url = self.git.create_pr(
                    branch, f"Complete {subject.title} course", body_path
                )
                self.state.update(subject.id, "pull_request", pr_url=pr_url)
                print(f"[{subject.id}] PR: {pr_url}")
                if self.config.git.wait_for_checks:
                    self.git.wait_for_checks(pr_url)
                if self.config.git.auto_merge:
                    self.git.merge(pr_url)
                    self.git.checkout_base()
                    self.state.update(subject.id, "published", pr_url=pr_url)
                else:
                    self.state.update(subject.id, "awaiting_merge", pr_url=pr_url)
            else:
                self.state.update(subject.id, "committed")
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.state.update(subject.id, "failed", error=error)
            log_path = self.config.state_path / "logs" / f"{subject.id}.log"
            log_path.write_text(traceback.format_exc(), encoding="utf-8")
            print(f"[{subject.id}] ERROR: {error}\nRegistro: {log_path}")
            if publish and branch is not None:
                try:
                    self.git.recover_base()
                except Exception as recovery_error:
                    print(f"[{subject.id}] no se pudo recuperar main: {recovery_error}")

    def run(
        self,
        *,
        subject_ids: list[str] | None = None,
        area_id: str | None = None,
        limit: int | None = None,
        dry_run: bool = False,
        publish: bool = True,
        retry_failed: bool = False,
    ) -> dict[str, int]:
        self.preflight(publish=publish and not dry_run)
        subjects = self.catalog.select(subject_ids, area_id)
        self.state.register(self.catalog.all_subjects())
        if retry_failed:
            self.state.reset_failed()
        selected: list[SubjectRef] = []
        explicit = bool(subject_ids)
        for subject in subjects:
            status = self.state.status(subject.id)
            if not explicit and status in {"published", "awaiting_merge", "pull_request"}:
                continue
            if status == "failed" and not retry_failed and not explicit:
                continue
            selected.append(subject)
        if limit is not None:
            selected = selected[:limit]

        print(f"Asignaturas seleccionadas: {len(selected)}")
        for index, subject in enumerate(selected, start=1):
            print(f"\n=== {index}/{len(selected)} · {subject.title} ===")
            self.process_subject(subject, dry_run=dry_run, publish=publish)
        summary = self.state.summary()
        print("\nEstado final:")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return summary
