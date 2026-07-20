from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import tomllib


@dataclass(slots=True)
class ModelConfig:
    content: str = "qwen3.6:27b"
    review: str = "qwen3.6:27b"
    technical: str = "ornith:9b"
    embedding: str = "qwen3-embedding:0.6b"
    host: str = "http://127.0.0.1:11434"
    context_tokens: int = 32768
    temperature: float = 0.2
    timeout_seconds: float = 900.0


@dataclass(slots=True)
class GenerationConfig:
    minimum_course_words: int = 2200
    maximum_generation_attempts: int = 3
    maximum_validation_repairs: int = 3
    related_courses: int = 4
    research_results: int = 8
    openalex_enabled: bool = True
    europe_pmc_enabled: bool = True


@dataclass(slots=True)
class GitConfig:
    default_branch: str = "main"
    remote: str = "origin"
    branch_prefix: str = "agent/course"
    auto_push: bool = True
    create_pull_request: bool = True
    wait_for_checks: bool = True
    auto_merge: bool = True
    merge_method: str = "squash"
    delete_branch: bool = True
    require_clean_worktree: bool = True


@dataclass(slots=True)
class AgentConfig:
    root: Path
    state_directory: Path = Path(".citonauta-agent")
    models: ModelConfig = field(default_factory=ModelConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    git: GitConfig = field(default_factory=GitConfig)

    @property
    def state_path(self) -> Path:
        path = self.state_directory
        if not path.is_absolute():
            path = self.root / path
        return path


def _merge_dataclass(instance: Any, values: dict[str, Any]) -> Any:
    for key, value in values.items():
        if not hasattr(instance, key):
            raise ValueError(f"Opción desconocida en la configuración: {key}")
        setattr(instance, key, value)
    return instance


def load_config(root: Path, config_path: Path | None = None) -> AgentConfig:
    root = root.resolve()
    path = (config_path or root / "agent-config.toml").resolve()
    config = AgentConfig(root=root)

    if path.exists():
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
        _merge_dataclass(config.models, raw.get("models", {}))
        _merge_dataclass(config.generation, raw.get("generation", {}))
        _merge_dataclass(config.git, raw.get("git", {}))
        if "agent" in raw and "state_directory" in raw["agent"]:
            config.state_directory = Path(raw["agent"]["state_directory"])

    config.state_path.mkdir(parents=True, exist_ok=True)
    (config.state_path / "logs").mkdir(parents=True, exist_ok=True)
    (config.state_path / "previews").mkdir(parents=True, exist_ok=True)
    return config
