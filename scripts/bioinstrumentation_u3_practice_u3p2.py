#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import cmath
import math
from pathlib import Path


def impedance(frequency_hz: float, rs_ohm: float = 1200.0, rct_ohm: float = 180000.0, cdl_f: float = 2.2e-6) -> complex:
    omega = 2.0 * math.pi * frequency_hz
    zc = 1.0 / (1j * omega * cdl_f)
    z_parallel = 1.0 / (1.0 / rct_ohm + 1.0 / zc)
    return rs_ohm + z_parallel


def sweep() -> list[dict[str, float]]:
    frequencies = [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    rows: list[dict[str, float]] = []
    for f in frequencies:
        z = impedance(f)
        rows.append({
            "frequency_hz": f,
            "real_ohm": z.real,
            "imag_ohm": z.imag,
            "magnitude_ohm": abs(z),
            "phase_deg": math.degrees(cmath.phase(z)),
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = sweep()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} impedance points to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
