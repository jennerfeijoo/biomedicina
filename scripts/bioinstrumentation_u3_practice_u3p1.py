#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def generate(duration: float = 2.0, fs: int = 250) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    electrodes = (-0.8, -0.2, 0.4, 0.9)
    sources = [(-0.45, 1.0, 7.0), (0.35, 0.65, 11.0)]
    for i in range(int(duration * fs)):
        t = i / fs
        values: list[float] = []
        for x in electrodes:
            v = 0.0
            for sx, amplitude, frequency in sources:
                spatial_weight = 1.0 / (1.0 + 8.0 * (x - sx) ** 2)
                v += amplitude * spatial_weight * math.sin(2.0 * math.pi * frequency * t)
            values.append(v)
        rows.append({
            "time_s": t,
            "e1_v": values[0],
            "e2_v": values[1],
            "e3_v": values[2],
            "e4_v": values[3],
            "lead_12_v": values[0] - values[1],
            "lead_34_v": values[2] - values[3],
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = generate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} synthetic samples to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
