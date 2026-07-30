#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def low_pass(values: list[float], alpha: float) -> list[float]:
    out: list[float] = []
    state = 0.0
    for value in values:
        state += alpha * (value - state)
        out.append(state)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source_rate = 4000.0
    sample_rate = 200.0
    duration = 1.0
    high_frequency = 170.0
    low_frequency = 12.0
    source_count = int(source_rate * duration)
    source = [
        math.sin(2 * math.pi * low_frequency * i / source_rate)
        + 0.45 * math.sin(2 * math.pi * high_frequency * i / source_rate)
        for i in range(source_count)
    ]
    filtered = low_pass(source, alpha=0.025)
    stride = int(source_rate / sample_rate)
    alias_frequency = abs(high_frequency - round(high_frequency / sample_rate) * sample_rate)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["time_s", "input_signal", "sampled_unfiltered", "sampled_filtered", "alias_frequency_hz"])
        for index in range(0, source_count, stride):
            writer.writerow([
                f"{index / source_rate:.6f}",
                f"{source[index]:.9f}",
                f"{source[index]:.9f}",
                f"{filtered[index]:.9f}",
                f"{alias_frequency:.6f}",
            ])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
