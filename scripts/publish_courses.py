#!/usr/bin/env python3
"""Promueve reconstrucciones académicas a las capas públicas de CitoNauta.

El publicador descubre paquetes en ``data/course_redevelopment/<subject>`` y
sincroniza, para una o varias asignaturas:

- el overlay editorial de ``data/subjects``;
- el descriptor avanzado de ``data/generated_courses``;
- las unidades avanzadas de ``data/generated_units``;
- el contrato verificable de las páginas HTML generadas.

La generación HTML permanece en ``scripts/generate_site.py``. Este módulo no
concede madurez académica: conserva los estados editoriales declarados por la
fuente y solo comprueba integridad, trazabilidad y sincronización técnica.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "data" / "course_redevelopment"
SUBJECT_ROOT = ROOT / "data" / "subjects"
GENERATED_COURSE_ROOT = ROOT / "data" / "generated_courses"
GENERATED_UNIT_ROOT = ROOT / "data" / "generated_units"
ADVANCED_MARKER = "<!-- advanced-unit-renderer:v1 -->"
GENERATED_MARKER = 'data-generated="citonauta-unit"'
SUPPORTED_COURSE_STATUSES = {"draft", "review", "generated", "complete"}
SUPPORTED_UNIT_STATUSES = {"review", "complete"}


@dataclass(frozen=True)
class CoursePackage:
    subject_id: str
    area_id: str
    source_dir: Path
    course_path: Path
    units_dir: Path
    overlay_path: Path
    generated_course_path: Path
    generated_units_dir: Path
    public_dir: Path
    course: dict[str, Any]
    units: tuple[dict[str, Any], ...]

    @property
    def unit_numbers(self) -> tuple[int, ...]:
        return tuple(int(unit["unit"]) for unit in self.units)

    @property
    def public_path(self) -> str:
        return self.public_dir.relative_to(ROOT).as_posix()


def load_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)}: la raíz debe ser un objeto JSON")
    return data


def write_object(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_weight(value: Any) -> float:
    match = re.search(r"-?\d+(?:[.,]\d+)?", str(value or ""))
    if not match:
        raise ValueError(f"ponderación inválida: {value!r}")
    return float(match.group(0).replace(",", "."))


def source_directories() -> list[Path]:
    if not SOURCE_ROOT.exists():
        return []
    return sorted(path for path in SOURCE_ROOT.iterdir() if path.is_dir() and (path / "course.json").exists())


def requested_source_directories(subjects: Iterable[str], publish_all: bool) -> list[Path]:
    normalized = sorted({str(subject).strip() for subject in subjects if str(subject).strip()})
    if publish_all:
        directories = source_directories()
        if not directories:
            raise FileNotFoundError("no se encontraron paquetes con course.json en data/course_redevelopment")
        return directories
    if not normalized:
        raise ValueError("indique --subject al menos una vez o use --all")
    directories: list[Path] = []
    for subject_id in normalized:
        directory = SOURCE_ROOT / subject_id
        if not (directory / "course.json").exists():
            raise FileNotFoundError(f"no existe un paquete reconstruido para {subject_id}")
        directories.append(directory)
    return directories


def validate_course_document(path: Path, course: dict[str, Any]) -> tuple[str, str, list[dict[str, Any]]]:
    subject_id = str(course.get("id") or course.get("subject_id") or "").strip()
    area_id = str(course.get("area_id") or "").strip()
    status = str(course.get("status") or "").strip()
    if not subject_id:
        raise ValueError(f"{path.relative_to(ROOT)}: falta id o subject_id")
    if path.parent.name != subject_id:
        raise ValueError(f"{path.relative_to(ROOT)}: el identificador no coincide con la carpeta")
    if not area_id:
        raise ValueError(f"{path.relative_to(ROOT)}: falta area_id")
    if status not in SUPPORTED_COURSE_STATUSES:
        raise ValueError(
            f"{path.relative_to(ROOT)}: status {status!r} no es publicable; "
            f"use uno de {sorted(SUPPORTED_COURSE_STATUSES)}"
        )
    for key in (
        "title",
        "description",
        "level",
        "prerequisites",
        "course_competencies",
        "learning_outcomes",
        "detailed_units",
        "assessment",
    ):
        if course.get(key) in (None, "", []):
            raise ValueError(f"{path.relative_to(ROOT)}: falta contenido en {key}")
    detailed_units = course["detailed_units"]
    if not isinstance(detailed_units, list) or not all(isinstance(item, dict) for item in detailed_units):
        raise ValueError(f"{path.relative_to(ROOT)}: detailed_units debe ser una lista de objetos")
    numbers = [int(item.get("unit", 0)) for item in detailed_units]
    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        raise ValueError(f"{path.relative_to(ROOT)}: secuencia {numbers}; se esperaba {expected}")
    return subject_id, area_id, detailed_units


def validate_assessment(course_path: Path, course: dict[str, Any]) -> None:
    components = [item for item in course.get("assessment", []) if isinstance(item, dict)]
    if len(components) < 3:
        raise ValueError(f"{course_path.relative_to(ROOT)}: se requieren al menos tres componentes de evaluación")
    total = sum(parse_weight(item.get("weight")) for item in components)
    if abs(total - 100.0) > 1e-9:
        raise ValueError(f"{course_path.relative_to(ROOT)}: la evaluación suma {total:g} %, no 100 %")


def load_package(source_dir: Path) -> CoursePackage:
    course_path = source_dir / "course.json"
    course = load_object(course_path)
    subject_id, area_id, detailed_units = validate_course_document(course_path, course)
    validate_assessment(course_path, course)
    units_dir = source_dir / "units"
    if not units_dir.is_dir():
        raise FileNotFoundError(f"{source_dir.relative_to(ROOT)}: falta la carpeta units")

    units: list[dict[str, Any]] = []
    declared_by_number = {int(item["unit"]): item for item in detailed_units}
    expected_names: list[str] = []
    for number in range(1, len(detailed_units) + 1):
        filename = f"unit-{number:02d}.json"
        expected_names.append(filename)
        unit_path = units_dir / filename
        if not unit_path.exists():
            raise FileNotFoundError(f"falta {unit_path.relative_to(ROOT)}")
        unit = load_object(unit_path)
        if str(unit.get("schema_version")) != "2.0":
            raise ValueError(f"{unit_path.relative_to(ROOT)}: schema_version debe ser 2.0")
        if str(unit.get("subject_id") or "").strip() != subject_id:
            raise ValueError(f"{unit_path.relative_to(ROOT)}: subject_id inconsistente")
        if str(unit.get("area_id") or "").strip() != area_id:
            raise ValueError(f"{unit_path.relative_to(ROOT)}: area_id inconsistente")
        if int(unit.get("unit", 0)) != number:
            raise ValueError(f"{unit_path.relative_to(ROOT)}: número de unidad inconsistente")
        if str(unit.get("status") or "").strip() not in SUPPORTED_UNIT_STATUSES:
            raise ValueError(f"{unit_path.relative_to(ROOT)}: status debe ser review o complete")
        for key in ("title", "purpose", "learning_objectives", "theory_sections", "sources"):
            if unit.get(key) in (None, "", []):
                raise ValueError(f"{unit_path.relative_to(ROOT)}: falta contenido en {key}")
        declared_title = str(declared_by_number[number].get("title") or "").strip()
        if not declared_title:
            raise ValueError(f"{course_path.relative_to(ROOT)}: la unidad {number} no declara título")
        if str(unit["title"]).strip() != declared_title:
            print(
                f"AVISO {subject_id}: unidad {number:02d} usa el título canónico del archivo lectivo "
                f"{unit['title']!r}; course.json declara {declared_title!r}."
            )
        units.append(unit)

    actual_names = sorted(path.name for path in units_dir.glob("unit-*.json"))
    if actual_names != expected_names:
        raise ValueError(
            f"{units_dir.relative_to(ROOT)}: contiene {actual_names}; se esperaba exactamente {expected_names}"
        )

    return CoursePackage(
        subject_id=subject_id,
        area_id=area_id,
        source_dir=source_dir,
        course_path=course_path,
        units_dir=units_dir,
        overlay_path=SUBJECT_ROOT / area_id / f"{subject_id}.json",
        generated_course_path=GENERATED_COURSE_ROOT / f"{subject_id}.json",
        generated_units_dir=GENERATED_UNIT_ROOT / subject_id,
        public_dir=ROOT / area_id / subject_id,
        course=course,
        units=tuple(units),
    )


def discover_packages(subjects: Iterable[str] = (), publish_all: bool = False) -> list[CoursePackage]:
    return [load_package(path) for path in requested_source_directories(subjects, publish_all)]


def public_overlay(package: CoursePackage) -> dict[str, Any]:
    overlay = json.loads(json.dumps(package.course, ensure_ascii=False))
    by_number = {int(unit["unit"]): unit for unit in package.units}
    for item in overlay["detailed_units"]:
        number = int(item["unit"])
        unit = by_number[number]
        item["title"] = str(unit["title"]).strip()
        item["description"] = str(unit["purpose"]).strip()
    return overlay


def assessment_plan(course: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in course.get("assessment", []):
        if not isinstance(item, dict):
            continue
        result.append(
            {
                "component": str(item.get("title") or "Componente").strip(),
                "weight_percent": parse_weight(item.get("weight")),
                "description": str(item.get("description") or "").strip(),
            }
        )
    return result


def expected_generated_course(package: CoursePackage, existing: dict[str, Any]) -> dict[str, Any]:
    course = package.course
    updated = dict(existing)
    updated.update(
        {
            "schema_version": "2.0",
            "subject_id": package.subject_id,
            "title": course["title"],
            "status": course["status"],
            "academic_level": course["level"],
            "course_purpose": course["description"],
            "prerequisites": course["prerequisites"],
            "course_competencies": course["course_competencies"],
            "learning_outcomes": course["learning_outcomes"],
            "assessment_plan": assessment_plan(course),
        }
    )
    return updated


def promote_package(package: CoursePackage) -> None:
    package.generated_units_dir.mkdir(parents=True, exist_ok=True)
    expected_names = {f"unit-{number:02d}.json" for number in package.unit_numbers}
    for stale in package.generated_units_dir.glob("unit-*.json"):
        if stale.name not in expected_names:
            stale.unlink()
    for number in package.unit_numbers:
        shutil.copyfile(
            package.units_dir / f"unit-{number:02d}.json",
            package.generated_units_dir / f"unit-{number:02d}.json",
        )
    write_object(package.overlay_path, public_overlay(package))
    existing = load_object(package.generated_course_path) if package.generated_course_path.exists() else {}
    write_object(package.generated_course_path, expected_generated_course(package, existing))
    print(
        f"[ok] {package.subject_id}: overlay, descriptor avanzado y "
        f"{len(package.units)} unidades promovidas"
    )


def promotion_errors(package: CoursePackage) -> list[str]:
    errors: list[str] = []
    expected_overlay = public_overlay(package)
    if not package.overlay_path.exists() or load_object(package.overlay_path) != expected_overlay:
        errors.append("overlay editorial desincronizado")
    expected_names = [f"unit-{number:02d}.json" for number in package.unit_numbers]
    actual_names = sorted(path.name for path in package.generated_units_dir.glob("unit-*.json"))
    if actual_names != expected_names:
        errors.append(f"generated_units contiene {actual_names}; se esperaba {expected_names}")
    for number in package.unit_numbers:
        source = package.units_dir / f"unit-{number:02d}.json"
        target = package.generated_units_dir / f"unit-{number:02d}.json"
        if not target.exists() or target.read_bytes() != source.read_bytes():
            errors.append(f"unidad {number:02d}: la copia pública no coincide con la fuente")
    if not package.generated_course_path.exists():
        errors.append("falta descriptor en data/generated_courses")
    else:
        generated = load_object(package.generated_course_path)
        expected = expected_generated_course(package, generated)
        for key in (
            "schema_version",
            "subject_id",
            "title",
            "status",
            "academic_level",
            "course_purpose",
            "prerequisites",
            "course_competencies",
            "learning_outcomes",
            "assessment_plan",
        ):
            if generated.get(key) != expected.get(key):
                errors.append(f"generated_courses: campo {key} desincronizado")
    return errors


def public_page_errors(package: CoursePackage) -> list[str]:
    errors: list[str] = []
    course_index = package.public_dir / "index.html"
    units_index = package.public_dir / "unidades" / "index.html"
    if not course_index.exists():
        errors.append("falta la página pública de la asignatura")
    if not units_index.exists():
        errors.append("falta el índice público de unidades")
    course_text = course_index.read_text(encoding="utf-8", errors="replace") if course_index.exists() else ""
    units_text = units_index.read_text(encoding="utf-8", errors="replace") if units_index.exists() else ""
    final_number = package.unit_numbers[-1]
    if f"Unidad {final_number}" not in course_text:
        errors.append(f"la página de asignatura no presenta la Unidad {final_number}")
    if str(len(package.units)) not in units_text:
        errors.append(f"el índice no declara una ruta de {len(package.units)} unidades")
    for unit in package.units:
        number = int(unit["unit"])
        page = package.public_dir / "unidades" / f"unidad-{number:02d}.html"
        if not page.exists():
            errors.append(f"falta {page.relative_to(ROOT)}")
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        if GENERATED_MARKER not in text:
            errors.append(f"{page.relative_to(ROOT)}: falta marcador de página generada")
        if ADVANCED_MARKER not in text:
            errors.append(f"{page.relative_to(ROOT)}: falta renderer avanzado")
        title = str(unit["title"]).strip()
        if title and title.casefold() not in text.casefold():
            errors.append(f"{page.relative_to(ROOT)}: no contiene el título canónico")
    return errors


def package_manifest(package: CoursePackage) -> dict[str, Any]:
    return {
        "subject_id": package.subject_id,
        "area_id": package.area_id,
        "status": package.course["status"],
        "unit_count": len(package.units),
        "source_path": package.source_dir.relative_to(ROOT).as_posix(),
        "overlay_path": package.overlay_path.relative_to(ROOT).as_posix(),
        "generated_course_path": package.generated_course_path.relative_to(ROOT).as_posix(),
        "generated_units_path": package.generated_units_dir.relative_to(ROOT).as_posix(),
        "public_path": package.public_path,
    }


def write_manifest(path: Path, packages: list[CoursePackage]) -> None:
    data = {
        "schema_version": "1.0",
        "course_count": len(packages),
        "courses": [package_manifest(package) for package in packages],
    }
    write_object(path, data)


def enforce(errors_by_subject: dict[str, list[str]], heading: str) -> None:
    entries = [f"{subject}: {error}" for subject, errors in errors_by_subject.items() for error in errors]
    if entries:
        raise SystemExit(heading + ":\n- " + "\n- ".join(entries))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Publica reconstrucciones académicas de forma reutilizable.")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all", action="store_true", help="Selecciona todos los paquetes reconstruidos válidos.")
    selection.add_argument("--subject", action="append", default=[], help="Selecciona una asignatura; puede repetirse.")
    parser.add_argument("--check", action="store_true", help="Comprueba la promoción sin escribir archivos.")
    parser.add_argument("--check-public", action="store_true", help="Comprueba promoción y páginas públicas.")
    parser.add_argument("--manifest", type=Path, help="Escribe un manifiesto de rutas y asignaturas seleccionadas.")
    parser.add_argument("--list-subjects", action="store_true", help="Imprime un identificador por línea.")
    parser.add_argument("--print-public-paths", action="store_true", help="Imprime una ruta pública por línea.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    packages = discover_packages(args.subject, args.all)
    if args.list_subjects:
        for package in packages:
            print(package.subject_id)
        return 0
    if args.print_public_paths:
        for package in packages:
            print(package.public_path)
        return 0
    if args.check_public:
        promotion = {package.subject_id: promotion_errors(package) for package in packages}
        enforce(promotion, "Promoción desincronizada")
        public = {package.subject_id: public_page_errors(package) for package in packages}
        enforce(public, "Publicación incompleta")
        print(f"Publicación verificada: {len(packages)} asignatura(s).")
    elif args.check:
        promotion = {package.subject_id: promotion_errors(package) for package in packages}
        enforce(promotion, "Promoción desincronizada")
        print(f"Promoción verificada: {len(packages)} asignatura(s).")
    else:
        for package in packages:
            promote_package(package)
    if args.manifest:
        write_manifest(args.manifest, packages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
