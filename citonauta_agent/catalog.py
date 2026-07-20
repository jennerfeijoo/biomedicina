from __future__ import annotations

import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class SubjectRef:
    id: str
    title: str
    area_id: str
    area_title: str
    path: str
    description: str
    biomedical_connection: str

    def as_prompt_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "title": self.title,
            "area_id": self.area_id,
            "area_title": self.area_title,
            "path": self.path,
            "description": self.description,
            "biomedical_connection": self.biomedical_connection,
        }


class CurriculumCatalog:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.data_path = self.root / "data" / "citonauta_curriculum.json"
        self.data = json.loads(self.data_path.read_text(encoding="utf-8"))
        self._subjects: dict[str, SubjectRef] = {}
        self._areas: dict[str, dict[str, Any]] = {}
        self._raw_subjects: dict[str, dict[str, Any]] = {}
        for area in self.data.get("areas", []):
            self._areas[area["id"]] = area
            for subject in area.get("subjects", []):
                ref = SubjectRef(
                    id=subject["id"],
                    title=subject["title"],
                    area_id=area["id"],
                    area_title=area["title"],
                    path=subject["path"],
                    description=subject["description"],
                    biomedical_connection=subject["biomedical_connection"],
                )
                self._subjects[ref.id] = ref
                self._raw_subjects[ref.id] = subject
        self._generator = self._load_generator()

    def _load_generator(self):
        path = self.root / "scripts" / "generate_site.py"
        spec = importlib.util.spec_from_file_location("citonauta_generate_site", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"No se pudo cargar {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def all_subjects(self) -> list[SubjectRef]:
        return list(self._subjects.values())

    def select(self, subject_ids: list[str] | None = None, area_id: str | None = None) -> list[SubjectRef]:
        selected = self.all_subjects()
        if area_id:
            selected = [subject for subject in selected if subject.area_id == area_id]
        if subject_ids:
            wanted = set(subject_ids)
            unknown = wanted - set(self._subjects)
            if unknown:
                raise KeyError("Asignaturas desconocidas: " + ", ".join(sorted(unknown)))
            selected = [subject for subject in selected if subject.id in wanted]
        return selected

    def baseline(self, subject_id: str) -> dict[str, Any]:
        ref = self._subjects[subject_id]
        area = self._areas[ref.area_id]
        subject = self._raw_subjects[subject_id]
        return self._generator.merge_subject_overlay(area, subject)

    def overlay_path(self, subject: SubjectRef) -> Path:
        return self.root / "data" / "subjects" / subject.area_id / f"{subject.id}.json"

    def html_path(self, subject: SubjectRef) -> Path:
        return self.root / subject.path

    def write_overlay(self, subject: SubjectRef, payload: dict[str, Any]) -> Path:
        path = self.overlay_path(subject)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
        return path

    def descriptor(self, subject: SubjectRef) -> str:
        return (
            f"{subject.title}. Área: {subject.area_title}. "
            f"{subject.description} {subject.biomedical_connection}"
        )

    def context_for(self, subject_id: str) -> dict[str, Any]:
        ref = self._subjects[subject_id]
        result = ref.as_prompt_dict()
        result["current_overlay"] = self.baseline(subject_id)
        return result
