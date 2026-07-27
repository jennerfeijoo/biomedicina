#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOLERANCE = 1e-9
EXPECTED_UNIT_NUMBERS = list(range(1, 15))


class WorkloadAuditError(ValueError):
    """Raised when the workload source cannot be audited safely."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise WorkloadAuditError(f"falta {path.relative_to(ROOT)}") from error
    except json.JSONDecodeError as error:
        raise WorkloadAuditError(
            f"JSON inválido en {path.relative_to(ROOT)}: línea {error.lineno}, columna {error.colno}"
        ) from error
    if not isinstance(data, dict):
        raise WorkloadAuditError(f"la raíz de {path.relative_to(ROOT)} debe ser un objeto JSON")
    return data


def as_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise WorkloadAuditError(f"{label} debe ser numérico")
    number = float(value)
    if number < 0:
        raise WorkloadAuditError(f"{label} no puede ser negativo")
    return number


def format_hours(value: float) -> str:
    return str(int(value)) if value.is_integer() else f"{value:g}"


def compare_declared(
    issues: list[str], declared: dict[str, Any], key: str, calculated: float
) -> None:
    try:
        declared_value = as_number(declared.get(key), f"declared_totals.{key}")
    except WorkloadAuditError as error:
        issues.append(str(error))
        return
    if abs(declared_value - calculated) > TOLERANCE:
        issues.append(
            f"declared_totals.{key}={declared_value:g}, pero el cálculo produce {calculated:g}"
        )


def audit(subject_id: str) -> tuple[dict[str, float], list[str]]:
    course_root = ROOT / "data" / "course_redevelopment" / subject_id
    workload_path = course_root / "workload.json"
    alignment_path = course_root / "CURRICULUM_ALIGNMENT_MATRIX.md"
    course_path = course_root / "course.json"

    workload = load_object(workload_path)
    issues: list[str] = []

    if workload.get("schema_version") != "1.0":
        issues.append("workload.json debe usar schema_version 1.0")
    if workload.get("course_id") != subject_id:
        issues.append("course_id de workload.json no coincide con --subject-id")
    if workload.get("status") != "provisional":
        issues.append("status de workload.json debe ser provisional hasta la adaptación institucional")

    baseline = as_number(
        workload.get("baseline_autonomous_hours_per_unit"),
        "baseline_autonomous_hours_per_unit",
    )

    raw_units = workload.get("units")
    if not isinstance(raw_units, list):
        raise WorkloadAuditError("units debe ser una lista")

    unit_numbers: list[int] = []
    contact_hours = 0.0
    unit_autonomous_hours = 0.0
    calculated_intensified_units: list[int] = []

    for index, raw_unit in enumerate(raw_units, start=1):
        if not isinstance(raw_unit, dict):
            issues.append(f"units[{index}] debe ser un objeto")
            continue
        unit_value = raw_unit.get("unit")
        if isinstance(unit_value, bool) or not isinstance(unit_value, int):
            issues.append(f"units[{index}].unit debe ser entero")
            continue
        unit_numbers.append(unit_value)
        try:
            unit_contact = as_number(
                raw_unit.get("contact_hours"), f"unidad {unit_value}.contact_hours"
            )
            unit_autonomous = as_number(
                raw_unit.get("autonomous_hours"), f"unidad {unit_value}.autonomous_hours"
            )
        except WorkloadAuditError as error:
            issues.append(str(error))
            continue
        contact_hours += unit_contact
        unit_autonomous_hours += unit_autonomous
        if unit_autonomous > baseline + TOLERANCE:
            calculated_intensified_units.append(unit_value)

    if sorted(unit_numbers) != EXPECTED_UNIT_NUMBERS:
        issues.append(
            "las unidades deben ser exactamente 1–14, sin duplicados ni omisiones; "
            f"se obtuvo {sorted(unit_numbers)}"
        )

    declared_intensified = workload.get("intensified_units")
    if not isinstance(declared_intensified, list) or not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in declared_intensified
    ):
        issues.append("intensified_units debe ser una lista de enteros")
    elif sorted(declared_intensified) != sorted(calculated_intensified_units):
        issues.append(
            "intensified_units no coincide con las unidades cuya carga autónoma supera la línea base: "
            f"declaradas={sorted(declared_intensified)}, calculadas={sorted(calculated_intensified_units)}"
        )

    project = workload.get("project_review_defense")
    if not isinstance(project, dict):
        raise WorkloadAuditError("project_review_defense debe ser un objeto")
    project_contact_hours = as_number(
        project.get("contact_hours"), "project_review_defense.contact_hours"
    )
    project_autonomous_hours = as_number(
        project.get("autonomous_hours"), "project_review_defense.autonomous_hours"
    )

    contact_hours += project_contact_hours
    autonomous_hours = unit_autonomous_hours + project_autonomous_hours
    total_hours = contact_hours + autonomous_hours
    baseline_total_hours = (
        contact_hours + len(EXPECTED_UNIT_NUMBERS) * baseline + project_autonomous_hours
    )
    delta_from_baseline_hours = total_hours - baseline_total_hours

    calculated = {
        "contact_hours": contact_hours,
        "unit_autonomous_hours": unit_autonomous_hours,
        "project_autonomous_hours": project_autonomous_hours,
        "autonomous_hours": autonomous_hours,
        "total_hours": total_hours,
        "baseline_total_hours": baseline_total_hours,
        "delta_from_baseline_hours": delta_from_baseline_hours,
    }

    declared = workload.get("declared_totals")
    if not isinstance(declared, dict):
        issues.append("declared_totals debe ser un objeto")
    else:
        for key, value in calculated.items():
            compare_declared(issues, declared, key, value)

    try:
        alignment = alignment_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(f"falta {alignment_path.relative_to(ROOT)}")
    else:
        expected_fragments = [
            f"trabajo autónomo de las 14 unidades: **{format_hours(unit_autonomous_hours)} horas**",
            f"proyecto, revisión por pares y defensa: **{format_hours(project_autonomous_hours)} horas**",
            f"trabajo autónomo total: **{format_hours(autonomous_hours)} horas**",
            (
                f"**{format_hours(contact_hours)} horas presenciales + "
                f"{format_hours(autonomous_hours)} horas autónomas = "
                f"{format_hours(total_hours)} horas**"
            ),
            f"supera en **{format_hours(delta_from_baseline_hours)} horas**",
        ]
        for fragment in expected_fragments:
            if fragment not in alignment:
                issues.append(
                    "CURRICULUM_ALIGNMENT_MATRIX.md no refleja el cálculo vigente: "
                    f"falta `{fragment}`"
                )

    try:
        course = load_object(course_path)
    except WorkloadAuditError as error:
        issues.append(str(error))
    else:
        assessment = course.get("assessment")
        if not isinstance(assessment, list) or not assessment:
            issues.append("course.json debe contener una lista assessment no vacía")
        else:
            weight_sum = 0.0
            for index, item in enumerate(assessment, start=1):
                if not isinstance(item, dict):
                    issues.append(f"assessment[{index}] debe ser un objeto")
                    continue
                raw_weight = item.get("weight")
                if not isinstance(raw_weight, str) or not raw_weight.endswith("%"):
                    issues.append(f"assessment[{index}].weight debe usar el formato 'N%'")
                    continue
                try:
                    weight_sum += float(raw_weight[:-1])
                except ValueError:
                    issues.append(f"assessment[{index}].weight no es numérico: {raw_weight!r}")
            if abs(weight_sum - 100.0) > TOLERANCE:
                issues.append(f"las ponderaciones de course.json suman {weight_sum:g} %, no 100 %")

    return calculated, issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Recalcula la carga de una reconstrucción curricular y exige coherencia entre "
            "workload.json, course.json y la matriz de alineación."
        )
    )
    parser.add_argument("--subject-id", required=True, help="Identificador del curso.")
    args = parser.parse_args()

    try:
        calculated, issues = audit(args.subject_id)
    except WorkloadAuditError as error:
        print(f"ERROR: {error}")
        return 1

    print(f"Curso: {args.subject_id}")
    for key, value in calculated.items():
        print(f"  {key}: {format_hours(value)}")

    if issues:
        print("\nINCONSISTENCIAS:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("\nCarga académica coherente entre fuente estructurada y documentación.")
    print("Nota: el auditor no valida equivalencia institucional de créditos ni viabilidad pedagógica.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
