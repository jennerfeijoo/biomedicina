#!/usr/bin/env python3
"""Generate deterministic first-order and negative-control datasets for Bioinstrumentation U2."""
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

FIRST_ORDER_FIELDS = (
    "time_s",
    "input_unit",
    "y_infinite_output_unit",
    "y_ideal_output_unit",
    "noise_output_unit",
    "y_output_unit",
)
NEGATIVE_FIELDS = (
    "control_id",
    "time_s",
    "input_unit",
    "y_output_unit",
)


@dataclass(frozen=True)
class DynamicParameters:
    seed: int = 20260729
    gain_k: float = 1.5
    offset_b: float = 0.2
    tau_s: float = 2.0
    dt_s: float = 0.02
    duration_s: float = 16.0
    step_time_s: float = 2.0
    step_amplitude: float = 1.0
    noise_sd: float = 0.003
    pure_delay_s: float = 0.4
    second_order_zeta: float = 0.3
    second_order_wn_rad_s: float = 2.5

    def validate(self) -> None:
        if self.tau_s <= 0 or self.dt_s <= 0 or self.duration_s <= 0:
            raise ValueError("tau_s, dt_s and duration_s must be positive")
        if not 0 <= self.step_time_s < self.duration_s:
            raise ValueError("step_time_s must lie inside the simulation interval")
        if self.noise_sd < 0:
            raise ValueError("noise_sd must be non-negative")
        if self.pure_delay_s <= 5 * self.dt_s:
            raise ValueError("pure_delay_s must exceed the rejection threshold")
        if not 0 < self.second_order_zeta < 1:
            raise ValueError("second_order_zeta must be between zero and one")
        if self.second_order_wn_rad_s <= 0:
            raise ValueError("second_order_wn_rad_s must be positive")


def _time_grid(parameters: DynamicParameters) -> list[float]:
    count = int(round(parameters.duration_s / parameters.dt_s))
    return [index * parameters.dt_s for index in range(count + 1)]


def simulate_first_order(parameters: DynamicParameters = DynamicParameters()) -> list[dict[str, float]]:
    parameters.validate()
    rng = random.Random(parameters.seed)
    alpha = math.exp(-parameters.dt_s / parameters.tau_s)
    times = _time_grid(parameters)
    y_state = parameters.offset_b
    rows: list[dict[str, float]] = []
    for index, time_s in enumerate(times):
        input_value = parameters.step_amplitude if time_s >= parameters.step_time_s else 0.0
        y_infinite = parameters.gain_k * input_value + parameters.offset_b
        noise = rng.gauss(0.0, parameters.noise_sd)
        rows.append(
            {
                "time_s": time_s,
                "input_unit": input_value,
                "y_infinite_output_unit": y_infinite,
                "y_ideal_output_unit": y_state,
                "noise_output_unit": noise,
                "y_output_unit": y_state + noise,
            }
        )
        if index < len(times) - 1:
            y_state = y_infinite + (y_state - y_infinite) * alpha
    return rows


def simulate_negative_controls(parameters: DynamicParameters = DynamicParameters()) -> list[dict[str, object]]:
    parameters.validate()
    rows: list[dict[str, object]] = []
    times = _time_grid(parameters)
    alpha = math.exp(-parameters.dt_s / parameters.tau_s)
    delayed_state = parameters.offset_b
    for index, time_s in enumerate(times):
        input_value = parameters.step_amplitude if time_s >= parameters.step_time_s else 0.0
        effective_input = (
            parameters.step_amplitude
            if time_s >= parameters.step_time_s + parameters.pure_delay_s
            else 0.0
        )
        rows.append(
            {
                "control_id": "pure-delay",
                "time_s": time_s,
                "input_unit": input_value,
                "y_output_unit": delayed_state,
            }
        )
        if index < len(times) - 1:
            delayed_target = parameters.offset_b + parameters.gain_k * effective_input
            delayed_state = delayed_target + (delayed_state - delayed_target) * alpha

    zeta = parameters.second_order_zeta
    wn = parameters.second_order_wn_rad_s
    wd = wn * math.sqrt(1.0 - zeta * zeta)
    phase_factor = zeta / math.sqrt(1.0 - zeta * zeta)
    for time_s in times:
        input_value = parameters.step_amplitude if time_s >= parameters.step_time_s else 0.0
        if time_s < parameters.step_time_s:
            response = 0.0
        else:
            elapsed = time_s - parameters.step_time_s
            response = 1.0 - math.exp(-zeta * wn * elapsed) * (
                math.cos(wd * elapsed) + phase_factor * math.sin(wd * elapsed)
            )
        rows.append(
            {
                "control_id": "underdamped-second-order",
                "time_s": time_s,
                "input_unit": input_value,
                "y_output_unit": parameters.offset_b + parameters.gain_k * response,
            }
        )
    return rows


def _csv_bytes(rows: Iterable[dict[str, object]], fieldnames: tuple[str, ...]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                key: f"{value:.10f}" if isinstance(value, float) else value
                for key, value in row.items()
            }
        )
    return buffer.getvalue().encode("utf-8")


def first_order_csv_bytes(rows: Iterable[dict[str, float]]) -> bytes:
    return _csv_bytes(rows, FIRST_ORDER_FIELDS)


def negative_csv_bytes(rows: Iterable[dict[str, object]]) -> bytes:
    return _csv_bytes(rows, NEGATIVE_FIELDS)


def estimate_tau_seconds(
    rows: Iterable[dict[str, float]],
    step_time_s: float,
    value_field: str = "y_output_unit",
) -> float:
    selected = list(rows)
    before = [float(row[value_field]) for row in selected if row["time_s"] < step_time_s]
    after = [float(row[value_field]) for row in selected if row["time_s"] >= step_time_s]
    if len(before) < 2 or len(after) < 10:
        raise ValueError("insufficient temporal data for tau estimation")
    baseline_values = before[-max(5, len(before) // 5) :]
    baseline = sum(baseline_values) / len(baseline_values)
    tail_count = max(10, len(after) // 10)
    final = sum(after[-tail_count:]) / tail_count
    change = final - baseline
    if change == 0:
        raise ValueError("step response has zero final change")
    target = baseline + (1.0 - math.exp(-1.0)) * change
    post = [row for row in selected if row["time_s"] >= step_time_s]
    for previous, current in zip(post, post[1:]):
        y0 = float(previous[value_field])
        y1 = float(current[value_field])
        if (y0 - target) * (y1 - target) <= 0 and y1 != y0:
            fraction = (target - y0) / (y1 - y0)
            crossing = float(previous["time_s"]) + fraction * (
                float(current["time_s"]) - float(previous["time_s"])
            )
            return crossing - step_time_s
    raise ValueError("the response never crosses the 63.212 percent target")


def normalized_magnitude(frequency_hz: float, tau_s: float) -> float:
    if frequency_hz < 0 or tau_s <= 0:
        raise ValueError("frequency must be non-negative and tau positive")
    return 1.0 / math.sqrt(1.0 + (2.0 * math.pi * frequency_hz * tau_s) ** 2)


def reject_simple_first_order(
    rows: Iterable[dict[str, object]],
    step_time_s: float,
    dt_s: float,
    control_id: str,
) -> list[str]:
    selected = [row for row in rows if row.get("control_id") == control_id]
    if not selected:
        return ["control dataset is missing"]
    values = [float(row["y_output_unit"]) for row in selected]
    baseline_rows = [row for row in selected if float(row["time_s"]) < step_time_s]
    baseline_values = [float(row["y_output_unit"]) for row in baseline_rows[-10:]]
    baseline = sum(baseline_values) / len(baseline_values)
    post = [row for row in selected if float(row["time_s"]) >= step_time_s]
    final_values = [float(row["y_output_unit"]) for row in post[-20:]]
    final = sum(final_values) / len(final_values)
    change = final - baseline
    reasons: list[str] = []
    if change == 0:
        return ["zero final change"]
    flat_samples = 0
    threshold = abs(change) * 0.001
    for row in post[1:]:
        if abs(float(row["y_output_unit"]) - baseline) <= threshold:
            flat_samples += 1
        else:
            break
    if flat_samples * dt_s > 5 * dt_s:
        reasons.append("unmodelled pure delay exceeds 5*dt")
    overshoot = (max(values) - final) / abs(change)
    if overshoot > 0.01:
        reasons.append("overshoot exceeds 1 percent of final change")
    return reasons


def static_only_curve(parameters: DynamicParameters = DynamicParameters()) -> list[dict[str, float]]:
    return [
        {"input_unit": x / 10.0, "output_unit": parameters.offset_b + parameters.gain_k * x / 10.0}
        for x in range(11)
    ]


def require_time_axis(rows: Iterable[dict[str, object]]) -> None:
    selected = list(rows)
    if not selected or any("time_s" not in row for row in selected):
        raise ValueError("time axis is required to estimate tau")


def write_outputs(output_dir: Path, parameters: DynamicParameters = DynamicParameters()) -> tuple[Path, Path, Path]:
    first_rows = simulate_first_order(parameters)
    negative_rows = simulate_negative_controls(parameters)
    first_payload = first_order_csv_bytes(first_rows)
    negative_payload = negative_csv_bytes(negative_rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    first_path = output_dir / "first_order_response.csv"
    negative_path = output_dir / "dynamic_negative_controls.csv"
    manifest_path = output_dir / "dynamic_response_manifest.json"
    first_path.write_bytes(first_payload)
    negative_path.write_bytes(negative_payload)
    fc = 1.0 / (2.0 * math.pi * parameters.tau_s)
    manifest = {
        "schema_version": "1.0",
        "practice_id": "U2-P2",
        "dataset_type": "deterministic_first_order_and_negative_controls",
        "parameters": asdict(parameters),
        "continuous_model": "tau*dy/dt + y = K*x(t) + b",
        "exact_discrete_update": "y[n+1] = y_inf[n] + (y[n] - y_inf[n])*exp(-dt/tau), with x[n] held constant during the interval",
        "derived_relations": {
            "fraction_at_tau": 1.0 - math.exp(-1.0),
            "corner_frequency_hz": fc,
            "normalized_magnitude_at_corner": normalized_magnitude(fc, parameters.tau_s),
        },
        "outputs": {
            "first_order_csv": first_path.name,
            "first_order_rows": len(first_rows),
            "first_order_sha256": hashlib.sha256(first_payload).hexdigest(),
            "negative_controls_csv": negative_path.name,
            "negative_control_rows": len(negative_rows),
            "negative_controls_sha256": hashlib.sha256(negative_payload).hexdigest(),
        },
        "negative_controls": ["pure-delay", "underdamped-second-order", "static-only"],
        "limitations": [
            "The tau-bandwidth relation is limited to this linear first-order model and the -3 dB criterion.",
            "Response time depends on the declared settling band and is not universally equal to tau.",
            "The datasets are synthetic and do not describe a person, tissue, sensor or clinical device.",
            "The outputs must not support clinical, regulatory, safety or device-performance claims.",
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return first_path, negative_path, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=DynamicParameters.seed)
    parser.add_argument("--noise-sd", type=float, default=DynamicParameters.noise_sd)
    args = parser.parse_args()
    parameters = DynamicParameters(seed=args.seed, noise_sd=args.noise_sd)
    for path in write_outputs(args.output_dir, parameters):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
