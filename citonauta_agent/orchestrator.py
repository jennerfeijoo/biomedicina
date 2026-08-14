from __future__ import annotations

import hashlib
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
from .reviewer_validation import find_applicable_validation
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
        if not self.config.reviewer_validation_path.exists():
            raise RuntimeError(
                "Falta el directorio de registros de validez del revisor: "
                + str(self.config.reviewer_validation_path)
            )

    @staticmethod
    def _resource_description(item: dict[str, Any]) -> str:
        abstract = str(item.get("abstract_excerpt") or "").strip()
        if len(abstract) >= 40:
            return abstract[:500]
        description = str(item.get("description") or "").strip()
        if len(description) >= 40:
            return description[:500]
        return "Recurso académico seleccionado para ampliar y contrastar los contenidos de esta asignatura."

    @staticmethod
    def _combine_reviews(primary: CourseReview, adversarial: CourseReview) -> CourseReview:
        def unique(left: list[str], right: list[str]) -> list[str]:
            return list(dict.fromkeys([*left, *right]))

        return CourseReview(
            approved=primary.approved and adversarial.approved,
            clarity_score=min(primary.clarity_score, adversarial.clarity_score),
            scientific_score=min(primary.scientific_score, adversarial.scientific_score),
            pedagogical_score=min(primary.pedagogical_score, adversarial.pedagogical_score),
            completeness_score=min(
                primary.completeness_score, adversarial.completeness_score
            ),
            blocking_issues=unique(primary.blocking_issues, adversarial.blocking_issues),
            improvements=unique(primary.improvements, adversarial.improvements),
            unsupported_claims=unique(
                primary.unsupported_claims, adversarial.unsupported_claims
            ),
        )

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
        course.status = "ai_draft"
        course.generation_metadata = GenerationMetadata(
            content_model=self.config.models.content,
            review_model=self.config.models.review,
            review_provider=self.config.reviewer_validation.provider,
            review_model_version=self.config.reviewer_validation.model_version,
            review_prompt_id=self.config.reviewer_validation.prompt_id,
            review_rubric_version=self.config.reviewer_validation.rubric_version,
            review_domain=self.config.reviewer_validation.domain,
            review_risk_level=self.config.reviewer_validation.risk_level,
            review_claim_types=self.config.reviewer_validation.claim_types,
            source_access=self.config.reviewer_validation.source_access,
        )

        source_records: list[SourceRecord] = []
        resources: list[RichItem] = []
        for item in source_pool:
            normalized_source = dict(item)
            url = str(normalized_source.get("url") or "")
            normalized_source["source_id"] = str(
                normalized_source.get("source_id")
                or "SRC-" + hashlib.sha256(url.encode("utf-8")).hexdigest()[:12].upper()
            )
            status_aliases = {
                "metadata_verified": "verified_metadata",
                "official_or_open_resource_checked_2026-08": "verified_metadata",
                "consulted_full_text": "verified_directly",
                "verified_from_repository_or_provided_source": "verified_directly",
                "consulted_uploaded_source": "verified_directly",
                "verified_from_supplied_source": "verified_directly",
                "verified_with_correction": "verified_directly",
                "identified_for_future_full_review": "recommended_future_review",
            }
            raw_status = str(normalized_source.get("verification_status") or "unverified")
            normalized_source["verification_status"] = status_aliases.get(
                raw_status, raw_status
            )
            source = SourceRecord.model_validate(normalized_source)
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

    def _finalize_review(self, course: CourseContent) -> CourseContent:
        settings = self.config.reviewer_validation
        validation = find_applicable_validation(
            self.config.reviewer_validation_path,
            provider=settings.provider,
            model=self.config.models.review,
            model_version=settings.model_version,
            prompt_id=settings.prompt_id,
            rubric_version=settings.rubric_version,
            domain=settings.domain,
            risk_level=settings.risk_level,
            claim_types=settings.claim_types,
            language=settings.language,
            source_access=settings.source_access,
            author_context_isolated=True,
            blind_to_author_rationale=True,
        )
        if validation is None:
            course.status = "review"
            course.generation_metadata.review_state = "ai_review_provisional"
            course.generation_metadata.reviewer_validation_id = None
            course.generation_metadata.reviewer_auto_merge_authorized = False
        else:
            course.status = "complete"
            course.generation_metadata.review_state = "ai_review_validated"
            course.generation_metadata.reviewer_validation_id = str(
                validation["validation_id"]
            )
            course.generation_metadata.reviewer_auto_merge_authorized = bool(
                (validation.get("authorization") or {}).get("can_auto_merge")
            )
        return CourseContent.model_validate(course.model_dump(mode="json"))

    def _candidate_path(self, subject: SubjectRef) -> Path:
        return self.config.state_path / "candidates" / f"{subject.id}.json"

    def _load_candidate(
        self,
        subject: SubjectRef,
        source_pool: list[dict[str, Any]],
    ) -> CourseContent | None:
        path = self._candidate_path(subject)
        if not path.exists():
            return None
        try:
            course = CourseContent.model_validate_json(path.read_text(encoding="utf-8"))
            course = self._normalize_course(course, subject, source_pool)
            semantic_errors = validate_semantics(
                course, self.config.generation.minimum_course_words
            )
            if semantic_errors:
                raise ValueError("; ".join(semantic_errors))
        except Exception as exc:
            print(f"[{subject.id}] candidato descartado: {type(exc).__name__}: {exc}")
            path.unlink(missing_ok=True)
            return None
        print(f"[{subject.id}] candidato recuperado: {path}")
        return course

    def _save_candidate(self, subject: SubjectRef, course: CourseContent) -> Path:
        path = self._candidate_path(subject)
        write_preview(path, course)
        print(f"[{subject.id}] checkpoint: {path}")
        return path

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

        candidate_path = self._candidate_path(subject)
        course = self._load_candidate(subject, source_pool)
        review: CourseReview | None = None
        last_generation_error = ""
        for attempt in range(1, self.config.generation.maximum_generation_attempts + 1):
            if course is not None and review is None:
                print(f"[{subject.id}] se reutiliza el candidato validado")
            else:
                print(f"[{subject.id}] generación {attempt}")
            try:
                if course is None:
                    course = self.ollama.generate_course(
                        subject.as_prompt_dict(), baseline, source_pool, related
                    )
                elif review is not None:
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

            self._save_candidate(subject, course)
            print(f"[{subject.id}] revisión independiente")
            primary_review = self.ollama.review_course(course, source_pool)
            if primary_review.passes_gate:
                print(f"[{subject.id}] revisión adversarial independiente")
                adversarial_review = self.ollama.adversarial_review_course(
                    course, source_pool
                )
                review = self._combine_reviews(primary_review, adversarial_review)
            else:
                review = primary_review
            if review.passes_gate:
                candidate_path.unlink(missing_ok=True)
                return self._finalize_review(course), review, source_pool
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
        course: CourseContent,
        review: CourseReview,
        sources: list[dict[str, Any]],
        check_results: list[tuple[str, str]],
    ) -> Path:
        path = self.config.state_path / "pr-body.md"
        source_lines = "\n".join(
            f"- [{item['title']}]({item['url']})" for item in sources[:12]
        )
        review_state = course.generation_metadata.review_state
        validation_id = course.generation_metadata.reviewer_validation_id or "ninguno"
        body = f"""## Propuesta de contenido académico

**{subject.title}** (`{subject.area_id}/{subject.id}`)

### Contenido incorporado

- Explicaciones conceptuales extensas por unidad.
- Ejemplos guiados con razonamiento paso a paso.
- Actividades, errores frecuentes y preguntas de autoevaluación.
- Aplicaciones biomédicas y evaluación alineada con los resultados de aprendizaje.
- Metadatos de generación y procedencia de fuentes.

### Estado de revisión IA

- Decisión: `{review_state}`
- Estado editorial resultante: `{course.status}`
- Registro de validez aplicable: `{validation_id}`
- Una revisión provisional no constituye validación científica ni autoriza fusión automática.

### Resultado de la rúbrica automática

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
                sorted(expected), f"Generate {subject.title} course content for review"
            )
            print(f"[{subject.id}] commit {commit}")

            if self.config.git.auto_push:
                assert branch is not None
                self.git.push(branch)
            if self.config.git.create_pull_request:
                assert branch is not None
                body_path = self._write_pr_body(
                    subject, course, review, sources, check_results
                )
                pr_url = self.git.create_pr(
                    branch, f"Propose {subject.title} course content", body_path
                )
                self.state.update(subject.id, "pull_request", pr_url=pr_url)
                print(f"[{subject.id}] PR: {pr_url}")
                if self.config.git.wait_for_checks:
                    self.git.wait_for_checks(pr_url)
                can_auto_merge = (
                    course.generation_metadata.review_state == "ai_review_validated"
                    and bool(course.generation_metadata.reviewer_validation_id)
                    and course.generation_metadata.reviewer_auto_merge_authorized
                )
                if self.config.git.auto_merge and can_auto_merge:
                    self.git.merge(pr_url)
                    self.git.checkout_base()
                    self.state.update(subject.id, "published", pr_url=pr_url)
                else:
                    if self.config.git.auto_merge and not can_auto_merge:
                        print(
                            f"[{subject.id}] auto-merge bloqueado: "
                            "el revisor no está validado para este alcance"
                        )
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
