#!/usr/bin/env python3
"""Generate deterministic synthetic static-characteristic datasets for Bioinstrumentation U2."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

FIELDNAMES = (
    "model",
    "branch",
    "direction",
    "x_input_unit",
    "y_ideal_output_unit",
    "noise_output_unit",
    "y_output_unit",
)


@dataclass(frozen=True)
class StaticParameters:
    seed: int = 20260729
    x_min: float = -10.0
    x_max: float = 10.0
    grid_step: float = 0.1
    sensitivity_k: float = 1.8
    offset_b: float = 0.4
    saturation_a: float = 8.0
    dead_zone_d: float = 1.2
    hysteresis_h: float = 0.25
    noise_sd: float = 0.02

    def validate(self) -> None:
        if self.grid_step <= 0:
            raise ValueError("grid_step must be positive")
        if self.x_max <= self.x_min:
            raise ValueError("x_max must exceed x_min")
        if self.saturation_a <= 0:
            raise ValueError("saturation_a must be positive")
        if self.dead_zone_d < 0:
            raise ValueError("dead_zone_d must be non-negative")
        if self.hysteresis_h < 0:
            raise ValueError("hysteresis_h must be non-negative")
        if self.noise_sd < 0:
            raise ValueError("noise_sd must be non-negative")


def _grid(start: float, stop: float, step: float) -> list[float]:
    count = int(round((stop - start) / step))
    values = [start + index * step for index in range(count + 1)]
    if not math.isclose(values[-1], stop, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("grid endpoints are inconsistent with grid_step")
    return values


def _row(
    model: str,
    branch: str,
    direction: int,
    x: float,
    y_ideal: float,
    noise: float,
) -> dict[str, object]:
    return {
        "model": model,
        "branch": branch,
        "direction": direction,
        "x_input_unit": x,
        "y_ideal_output_unit": y_ideal,
        "noise_output_unit": noise,
        "y_output_unit": y_ideal + noise,
    }


def simulate(parameters: StaticParameters = StaticParameters()) -> list[dict[str, object]]:
    parameters.validate()
    rng = random.Random(parameters.seed)
    ascending = _grid(parameters.x_min, parameters.x_max, parameters.grid_step)
    rows: list[dict[str, object]] = []

    for model in ("linear-local", "saturation", "dead-zone"):
        for x in ascending:
            if model == "linear-local":
                y_ideal = parameters.offset_b + parameters.sensitivity_k * x
            elif model == "saturation":
                y_ideal = parameters.offset_b + parameters.saturation_a * math.tanh(
                    parameters.sensitivity_k * x / parameters.saturation_a
                )
            else:
                signed = math.copysign(max(abs(x) - parameters.dead_zone_d, 0.0), x)
                if x == 0:
                    signed = 0.0
                y_ideal = parameters.offset_b + parameters.sensitivity_k * signed
            noise = rng.gauss(0.0, parameters.noise_sd)
            rows.append(_row(model, "single", 0, x, y_ideal, noise))

    for branch, direction, values in (
        ("ascending", 1, ascending),
        ("descending", -1, list(reversed(ascending))),
    ):
        for x in values:
            y_ideal = (
                parameters.offset_b
                + parameters.sensitivity_k * x
                + parameters.hysteresis_h * direction
            )
            noise = rng.gauss(0.0, parameters.noise_sd)
            rows.append(_row("hysteresis", branch, direction, x, y_ideal, noise))
    return rows


def csv_bytes(rows: Iterable[dict[str, object]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                key: f"{value:.10f}" if isinstance(value, float) else value
                for key, value in row.items()
            }
        )
    return buffer.getvalue().encode("utf-8")


def fit_line(rows: Iterable[dict[str, object]], value_field: str = "y_output_unit") -> tuple[float, float]:
    selected = list(rows)
    if len(selected) < 2:
        raise ValueError("at least two rows are required for a line fit")
    xs = [float(row["x_input_unit"]) for row in selected]
    ys = [float(row[value_field]) for row in selected]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    if denominator == 0:
        raise ValueError("line fit requires non-zero x variance")
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denominator
    intercept = y_mean - slope * x_mean
    return slope, intercept


def branch_residual_means(rows: Iterable[dict[str, object]]) -> dict[str, float]:
    selected = [row for row in rows if row["model"] == "hysteresis"]
    slope, intercept = fit_line(selected)
    result: dict[str, float] = {}
    for branch in ("ascending", "descending"):
        residuals = [
            float(row["y_output_unit"])
            - (intercept + slope * float(row["x_input_unit"]))
            for row in selected
            if row["branch"] == branch
        ]
        result[branch] = sum(residuals) / len(residuals)
    return result


def write_outputs(output_dir: Path, parameters: StaticParameters = StaticParameters()) -> tuple[Path, Path]:
    rows = simulate(parameters)
    payload = csv_bytes(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "static_characteristics.csv"
    manifest_path = output_dir / "static_characteristics_manifest.json"
    csv_path.write_bytes(payload)
    manifest = {
        "schema_version": "1.0",
        "practice_id": "U2-P1",
        "dataset_type": "deterministic_synthetic_static_characteristics",
        "parameters": asdict(parameters),
        "outputs": {
            "csv": csv_path.name,
            "row_count": len(rows),
            "sha256": hashlib.sha256(payload).hexdigest(),
        },
        "models": ["linear-local", "saturation", "dead-zone", "hysteresis"],
        "units": {
            "x_input_unit": "didactic input unit",
            "y_output_unit": "didactic output unit",
        },
        "limitations": [
            "Synthetic didactic curves; they are not observations from people, tissue or devices.",
            "A curve shape does not identify a unique physical mechanism.",
            "A high coefficient of determination is not complete validation.",
            "The dataset must not be used for clinical, regulatory, safety or device-performance claims.",
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return csv_path, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=StaticParameters.seed)
    parser.add_argument("--noise-sd", type=float, default=StaticParameters.noise_sd)
    args = parser.parse_args()
    parameters = StaticParameters(seed=args.seed, noise_sd=args.noise_sd)
    csv_path, manifest_path = write_outputs(args.output_dir, parameters)
    print(csv_path)
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
