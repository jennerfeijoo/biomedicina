#!/usr/bin/env python3
"""Generate a deterministic synthetic contact-thermometry dataset for Bioinstrumentation U1.

The model is deliberately didactic. It separates:
- T_u: prescribed unperturbed surface temperature,
- T_d: contact-perturbed surface temperature,
- T_s: internal sensor temperature,
- y: reported indication after calibration offset and synthetic noise.

It is not a validated physiological or clinical model.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SCHEMA_VERSION = "1.0"
MODEL_ID = "contact_thermometry_first_order_didactic"
CSV_NAME = "thermal_chain.csv"
MANIFEST_NAME = "thermal_chain_manifest.json"
FIELDNAMES = [
    "time_s",
    "T_u_C",
    "T_d_C",
    "T_s_C",
    "indication_C",
    "contact_bias_C",
    "calibration_offset_C",
    "noise_C",
]


@dataclass(frozen=True)
class ThermalParameters:
    duration_s: float = 60.0
    dt_s: float = 0.1
    step_time_s: float = 10.0
    initial_temperature_c: float = 32.0
    target_temperature_c: float = 36.0
    contact_bias_c: float = -0.4
    tau_s: float = 5.0
    calibration_offset_c: float = 0.15
    noise_std_c: float = 0.02
    seed: int = 20260729

    def validate(self) -> None:
        finite_values = {
            "duration_s": self.duration_s,
            "dt_s": self.dt_s,
            "step_time_s": self.step_time_s,
            "initial_temperature_c": self.initial_temperature_c,
            "target_temperature_c": self.target_temperature_c,
            "contact_bias_c": self.contact_bias_c,
            "tau_s": self.tau_s,
            "calibration_offset_c": self.calibration_offset_c,
            "noise_std_c": self.noise_std_c,
        }
        for name, value in finite_values.items():
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.duration_s <= 0:
            raise ValueError("duration_s must be > 0")
        if self.dt_s <= 0:
            raise ValueError("dt_s must be > 0")
        if self.tau_s <= 0:
            raise ValueError("tau_s must be > 0")
        if self.noise_std_c < 0:
            raise ValueError("noise_std_c must be >= 0")
        if not 0 <= self.step_time_s < self.duration_s:
            raise ValueError("step_time_s must satisfy 0 <= step_time_s < duration_s")
        ratio = self.duration_s / self.dt_s
        if abs(ratio - round(ratio)) > 1e-9:
            raise ValueError("duration_s must be an integer multiple of dt_s")
        step_ratio = self.step_time_s / self.dt_s
        if abs(step_ratio - round(step_ratio)) > 1e-9:
            raise ValueError("step_time_s must be an integer multiple of dt_s")


def _format_float(value: float) -> str:
    return f"{value:.6f}"


def simulate(params: ThermalParameters) -> list[dict[str, float]]:
    """Return deterministic rows for a piecewise-constant thermal input."""
    params.validate()
    rng = random.Random(params.seed)
    sample_count = int(round(params.duration_s / params.dt_s)) + 1
    decay = math.exp(-params.dt_s / params.tau_s)

    def unperturbed_temperature(t: float) -> float:
        return (
            params.initial_temperature_c
            if t < params.step_time_s
            else params.target_temperature_c
        )

    initial_u = unperturbed_temperature(0.0)
    previous_d = initial_u + params.contact_bias_c
    sensor_temperature = previous_d
    rows: list[dict[str, float]] = []

    for index in range(sample_count):
        t = index * params.dt_s
        if index > 0:
            sensor_temperature = previous_d + (
                sensor_temperature - previous_d
            ) * decay

        unperturbed = unperturbed_temperature(t)
        disturbed = unperturbed + params.contact_bias_c
        noise = rng.gauss(0.0, params.noise_std_c)
        indication = sensor_temperature + params.calibration_offset_c + noise

        rows.append(
            {
                "time_s": t,
                "T_u_C": unperturbed,
                "T_d_C": disturbed,
                "T_s_C": sensor_temperature,
                "indication_C": indication,
                "contact_bias_C": params.contact_bias_c,
                "calibration_offset_C": params.calibration_offset_c,
                "noise_C": noise,
            }
        )
        previous_d = disturbed

    return rows


def csv_bytes(rows: Iterable[dict[str, float]]) -> bytes:
    """Serialize rows with stable ordering and Unix newlines."""
    from io import StringIO

    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: _format_float(float(row[field])) for field in FIELDNAMES})
    return buffer.getvalue().encode("utf-8")


def build_manifest(
    params: ThermalParameters,
    rows: list[dict[str, float]],
    payload: bytes,
) -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "model_id": MODEL_ID,
        "generated_by": "scripts/generate_bioinstrumentation_thermal_dataset.py",
        "parameters": asdict(params),
        "outputs": {
            "csv": CSV_NAME,
            "row_count": len(rows),
            "columns": FIELDNAMES,
            "sha256": hashlib.sha256(payload).hexdigest(),
        },
        "variable_semantics": {
            "T_u_C": "prescribed unperturbed surface temperature; not a patient measurement",
            "T_d_C": "surface temperature after the declared synthetic contact bias",
            "T_s_C": "first-order internal sensor state",
            "indication_C": "sensor state plus declared calibration offset and synthetic noise",
        },
        "limitations": [
            "didactic synthetic model only",
            "not validated for skin, core temperature, any population, or any device",
            "does not include perfusion, evaporation, distributed geometry, or nonlinear sensor effects",
            "must not be used for diagnosis, treatment, device validation, or physiological inference",
        ],
        "reproducibility": {
            "random_generator": "python random.Random",
            "seed": params.seed,
            "numeric_serialization": "six decimal places",
            "line_endings": "LF",
        },
    }


def write_outputs(output_dir: Path, params: ThermalParameters) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = simulate(params)
    payload = csv_bytes(rows)
    csv_path = output_dir / CSV_NAME
    manifest_path = output_dir / MANIFEST_NAME
    csv_path.write_bytes(payload)
    manifest = build_manifest(params, rows, payload)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return csv_path, manifest_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--duration-s", type=float, default=60.0)
    parser.add_argument("--dt-s", type=float, default=0.1)
    parser.add_argument("--step-time-s", type=float, default=10.0)
    parser.add_argument("--initial-temperature-c", type=float, default=32.0)
    parser.add_argument("--target-temperature-c", type=float, default=36.0)
    parser.add_argument("--contact-bias-c", type=float, default=-0.4)
    parser.add_argument("--tau-s", type=float, default=5.0)
    parser.add_argument("--calibration-offset-c", type=float, default=0.15)
    parser.add_argument("--noise-std-c", type=float, default=0.02)
    parser.add_argument("--seed", type=int, default=20260729)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    params = ThermalParameters(
        duration_s=args.duration_s,
        dt_s=args.dt_s,
        step_time_s=args.step_time_s,
        initial_temperature_c=args.initial_temperature_c,
        target_temperature_c=args.target_temperature_c,
        contact_bias_c=args.contact_bias_c,
        tau_s=args.tau_s,
        calibration_offset_c=args.calibration_offset_c,
        noise_std_c=args.noise_std_c,
        seed=args.seed,
    )
    try:
        csv_path, manifest_path = write_outputs(args.output_dir, params)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print(f"Wrote {csv_path}")
    print(f"Wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
